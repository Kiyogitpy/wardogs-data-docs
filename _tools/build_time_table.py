#!/usr/bin/env python3
"""Round 38: hits, supplies and seconds to build, repair and dismantle every buildable, per hammer.

Rebuilds the table in game-features/Wardogs_Buildables_v1.md section 13 from data/ and the constants
read from native code (docs/evidence/round38-building-native.md). Labelled Derived: it applies the
single-hit formulas of the hammer path (`0x85EAAA0` -> `0x85F1D90` -> `0x85F1F20`):

    A      = hammer BuildAmount * StructureBuildAmountFactor       (build hit; data asset +0x60, default 1)
    A_crit = hammer BuildAmountWhenTargetIsHit                     (hit on a critical spot; no factor)
    A_rep  = A * RepairSpeedMultiplier                             (hit on a finished structure)
    T      = max(1, round_half_up(Cost * S))                       (GetTotalBuildCost, S = build cost scale)
    build  : progress += A / T per hit,  hits = ceil(T / A),       supplies spent = T in total
    repair : health   += A_rep / T * MaxHealth per hit
    place  : PlacementCost * S supplies at placement (GetPlacementCost), 0 for most structures
    dismantle: damage RatePerHit * 1.0 (the builder's own structure) or * 0.5 (anyone else's)

S is a live-curve value sampled on the player; it is 1.0 when the curve is absent and its contents are not in the
client, so the table uses S = 1 (the --scale option shows the effect). The seconds column multiplies the hits by
the swing loop length of the hammer's use montage (assets/data/bp-defaults.json); that is an assumption about the
swing period, not a native value.

    python -I _tools/build_time_table.py                print the table
    python -I _tools/build_time_table.py --write        refresh the block in the page (idempotent)
    python -I _tools/build_time_table.py --scale 0.8    show the effect of a different scale S
    python -I _tools/build_time_table.py --check        assert the key values (exit 1 on mismatch)
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buildable_tables as bt  # noqa: E402
import bp_defaults as bpd  # noqa: E402

ROOT = bt.ROOT
PAGE = os.path.join(ROOT, bt.PAGE)
BLOCK = re.compile(r"<!-- build_time_table -->\r?\n.*?<!-- /build_time_table -->", re.S)
FACTOR = "_aaabkhhnlcojdebfcnjfd"  # WDBuildableDataAsset +0x60, native default 1.0
HAMMERS = (("Small", "ID_SmallHammer", "AM_FP_Small_Hammer_Use"),
           ("Medium", "ID_MediumHammer", "AM_FP_BuildTool_Use"),
           ("Large", "ID_LargeHammer", "AM_FP_Large_Hammer_Use"))


def rnd(x):
    """Round half up, minimum 1 for a positive value (the rounding of 0x858D1D0)."""
    return max(1, int(math.floor(abs(x) + 0.5))) if x > 0 else 0


def hammer_data():
    out = {}
    for name, idn, mon in HAMMERS:
        rel = bt.DATA + f"{name}Hammer/{idn}.json"
        props = {}
        for e in bt.exports(rel):
            if e["Type"] in ("WDItemExtensionData_BuildTool", "WDItemExtensionData_CriticalHitSpotManager",
                             "WDItemExtensionData_BuildableDismantle"):
                props.update(e["Properties"])
        ls, le = bpd.get("buildables", mon, "Section:LoopStart"), bpd.get("buildables", mon, "Section:LoopEnd")
        out[name] = {"build": props["BuildAmount"], "crit": props["BuildAmountWhenTargetIsHit"],
                     "dismantle": props["DismantleRatePerHit"],
                     "loop": round(le["value"] - ls["value"], 3)}
    return out


def rows(scale=1.0):
    d = bt.load()
    hd = hammer_data()
    res = []
    for rel, name, typ, p in d["assets"]:
        cost = p.get("Cost", 0)
        if not cost:
            continue
        T = rnd(cost * scale)
        place = rnd(p.get("PlacementCost", 0) * scale)
        f = p.get(FACTOR, 1.0)
        rep = p.get("RepairSpeedMultiplier", 1.0)
        hp = p.get("MaxHealth", 0)
        r = {"name": name, "tag": bt.tag_of(p), "T": T, "place": place, "factor": f, "rep": rep, "hp": hp,
             "instant": bool(p.get("bInstantFinish")), "placeable": bt.hammers(d, bt.tag_of(p))}
        for h, v in hd.items():
            a = v["build"] * f
            hits = math.ceil(T / a - 1e-9)
            r[h] = {"hits": hits, "sec": hits * v["loop"], "rep_hits": math.ceil(T / (a * rep) - 1e-9),
                    "dis": math.ceil(hp / v["dismantle"] - 1e-9), "dis_other": math.ceil(hp / (v["dismantle"] * 0.5) - 1e-9)}
        res.append(r)
    return res, hd


def fmt(x):
    return f"{x:,.1f}".rstrip("0").rstrip(".") if isinstance(x, float) else f"{x:,}"


def table(scale=1.0):
    res, hd = rows(scale)
    out = ["| Structure | Tag | Build Supplies to finish (`T`) | Placement supplies | Build factor | Repair multiplier | Max health | Placed with | "
           "Hits S / M / L | Seconds S / M / L | Full repair hits S / M / L | Dismantle hits S / M / L (own) |",
           "|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|"]
    for r in res:
        if r["instant"]:
            hits = secs = "instant"
        else:
            hits = " / ".join(fmt(r[h]["hits"]) for h in ("Small", "Medium", "Large"))
            secs = " / ".join(fmt(r[h]["sec"]) for h in ("Small", "Medium", "Large"))
        rep = " / ".join(fmt(r[h]["rep_hits"]) for h in ("Small", "Medium", "Large"))
        dis = " / ".join(fmt(r[h]["dis"]) for h in ("Small", "Medium", "Large"))
        out.append(f"| `{r['name']}` | `{bt.short(r['tag'])}` | {r['T']} | {r['place']} | {fmt(r['factor'])} | {fmt(r['rep'])} | "
                   f"{fmt(r['hp'])} | {r['placeable']} | {hits} | {secs} | {rep} | {dis} |")
    out.append("")
    out.append("Hammer constants used (`BuildAmount`, critical-spot amount, dismantle damage per hit, swing loop in seconds): " + "; ".join(
        f"{h} {fmt(v['build'])}, {fmt(v['crit'])}, {fmt(v['dismantle'])}, {v['loop']}" for h, v in hd.items()) + ".")
    return "\n".join(out)


def write():
    text = open(PAGE, encoding="utf-8").read()
    new = "<!-- build_time_table -->\n" + table() + "\n<!-- /build_time_table -->"
    if not BLOCK.search(text):
        sys.exit("markers <!-- build_time_table --> not found in " + PAGE)
    out = BLOCK.sub(lambda m: new, text)
    if out != text:
        with open(PAGE, "w", encoding="utf-8", newline="") as f:
            f.write(out)
        print("page updated")
    else:
        print("page already current")


def check():
    res, hd = rows()
    by = {r["name"]: r for r in res}
    assert hd["Large"]["build"] == 1.5 and hd["Medium"]["build"] == 1.0 and hd["Small"]["build"] == 0.5, hd
    sb = by["DA_Buildable_SandbagWall"]
    assert sb["T"] == 15 and sb["Large"]["hits"] == 10 and sb["Medium"]["hits"] == 15 and sb["Small"]["hits"] == 30, sb
    bw = by["DA_Buildable_BarbedWire"]
    assert bw["factor"] == 3.5, bw
    assert rnd(0) == 0 and rnd(0.2) == 1 and rnd(2.5) == 3
    print("ok")


def main():
    args = sys.argv[1:]
    if "--check" in args:
        check()
    elif "--write" in args:
        write()
    elif "--scale" in args:
        print(table(float(args[args.index("--scale") + 1])))
    else:
        print(table())


if __name__ == "__main__":
    main()
