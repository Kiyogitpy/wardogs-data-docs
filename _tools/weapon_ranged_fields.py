"""Per-weapon RangedWeapon and Holdable extension fields for content/Wardogs_RangedWeaponFields_v1.md.

Scans data/ for ID_*.json items that carry WDItemExtensionData_RangedWeapon (rechamber flags and delay, iron-sight
camera offset, sight position offset, fire-animation blend values, trace radius) and WDItemExtensionData_Holdable
(crosshair override). Names come from assets/data/loadout-builder.json. Test barrels (ID_*BarrelTest) are skipped.

    python -I _tools/weapon_ranged_fields.py --write   # refresh the marked blocks
    python -I _tools/weapon_ranged_fields.py --check   # exit 1 when a block is stale
    python -I _tools/weapon_ranged_fields.py weapons|crosshair   # print one block
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = os.path.join(ROOT, "content/Wardogs_RangedWeaponFields_v1.md")
BLOCK = re.compile(r"<!-- ranged_fields (\w+) -->\r?\n.*?<!-- /ranged_fields -->", re.S)
N = ct.n


def names():
    d = json.load(open(os.path.join(ROOT, "assets/data/loadout-builder.json"), encoding="utf-8"))["items"]
    return {k: v.get("name") for k, v in d.items()}


def load():
    rw, ho = {}, {}
    for f in sorted(glob.glob(os.path.join(DATA, "**", "ID_*.json"), recursive=True)):
        base = os.path.basename(f)[:-5]
        if "BarrelTest" in base:
            continue
        try:
            es = ct.exports(f)
        except Exception:
            continue
        for e in es:
            t = e.get("Type")
            if t == "WDItemExtensionData_RangedWeapon":
                rw[base] = e.get("Properties", {})
            elif t == "WDItemExtensionData_Holdable" and "CrosshairSettings" in e.get("Properties", {}):
                ho[base] = e["Properties"]
    return rw, ho


def vec(v):
    if not v:
        return "-"
    return "(" + ", ".join(N(v.get(a, 0)) for a in "XYZ") + ")"


def yn(p, k):
    return "yes" if p.get(k) else "-"


def num(p, k):
    return N(p[k]) if k in p else "-"


def weapons_block(rw, nm):
    h = ["| Weapon | Item | Rechamber after each shot | Rechamber delay (s) | Unchamber on reload | Iron-sight camera offset (X, Y, Z) | Sight position offset (X, Y, Z) | Fire blend targets | Buffered fire blend (s) | Trace radius |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(rw, key=lambda x: (nm.get(x, x) or x).lower()):
        p = rw[k]
        h.append(f"| {nm.get(k, '-')} | `{k}` | {yn(p, 'bRequiresRechamberAfterFire')} | {num(p, 'TimeAfterFireToRechamber')} | "
                 f"{yn(p, 'bShouldUnchamberDuringReload')} | {vec(p.get('IronSightCameraOffset'))} | {vec(p.get('SightPositionOffset'))} | "
                 f"{num(p, 'FireAnimBlendTargets')} | {num(p, 'BufferedFireAnimBlendTime')} | {num(p, 'WeaponTraceRadius')} |")
    return "\n".join(h)


def crosshair_block(ho, nm):
    h = ["| Item | Name | Override default crosshair | Shows crosshair | Type | Dot | Hair length | Gap | Opacity | Spread multiplier | Buildable check radius (cm) |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(ho):
        p = ho[k]
        c = p["CrosshairSettings"]
        sc = p.get("bShowCrosshair")
        h.append(f"| `{k}` | {nm.get(k, '-')} | {yn(p, 'bOverrideDefaultCrosshairSettings')} | {'-' if sc is None else ('yes' if sc else 'no')} | "
                 f"{c.get('Type', '-').split('::')[-1]} | {yn(c, 'bShowDot')} | {num(c, 'HairLength')} | {num(c, 'Gap')} | "
                 f"{num(c, 'Opacity')} | {num(c, 'SpreadMultiplier')} | {num(c, 'BuildableCheckRadius')} |")
    return "\n".join(h)


def curves_block():
    rows = ["| Curve | Used by | Keys (time or FOV in, value out) |", "|---|---|---|"]
    items = json.load(open(os.path.join(ROOT, "assets/data/loadout-builder.json"), encoding="utf-8"))["items"]
    pat = os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Weapons/**/*.json")
    for f in sorted(glob.glob(pat, recursive=True)):
        b = os.path.basename(f)[:-5]
        if not (b.startswith("CRV_FGRP_") or b.startswith("CF_WEPN_")):
            continue
        e = ct.exports(f)[0]
        keys = e["Properties"]["FloatCurve"]["Keys"]
        item = "ID_" + b.split("_")[1] + "_" + b.split("_")[2]
        who = items.get(item, {}).get("name", item)
        pts = ", ".join("(%g, %g)" % (k["Time"] + 0.0, round(k["Value"], 4) + 0.0) for k in keys)
        rows.append("| `%s` | %s | %s |" % (b, who, pts))
    return chr(10).join(rows)


def magazines_block():
    items = json.load(open(os.path.join(ROOT, "assets/data/loadout-builder.json"), encoding="utf-8"))["items"]
    cols = ["base", "FMJ", "FMJTracer", "HollowPoint", "HollowPointTracer", "ArmorPiercing", "ArmorPiercingTracer"]
    rows = ["| Magazine | Item | Standard | FMJ | FMJ tracer | Hollow point | Hollow point tracer | Armor piercing | Armor piercing tracer |",
            "|---|---|---|---|---|---|---|---|---|"]
    out = []
    for f in glob.glob(os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Weapons/**/DT_VendorData_Ext_MAGZ*.json"), recursive=True):
        for k, r in ct.exports(f)[0]["Rows"].items():
            d = {}
            for v in r["VendorItemVariations"]:
                tg = v["VariationTag"]["TagName"]
                d["base" if tg == k else tg.split(".")[-1]] = v["Price"]
            short = "ID_" + k.split(".")[-1]
            out.append((short, d))
    for short, d in sorted(out):
        rows.append("| %s | `%s` | " % (items.get(short, {}).get("name", "-"), short) +
                    " | ".join(N(d[c]) if c in d else "-" for c in cols) + " |")
    return chr(10).join(rows)


def blocks():
    rw, ho = load()
    nm = names()
    return {"weapons": weapons_block(rw, nm), "crosshair": crosshair_block(ho, nm), "curves": curves_block(), "magazines": magazines_block(),
            "counts": f"{len(rw)} ranged-weapon items and {len(ho)} items with a crosshair override"}


def render(text, b):
    return BLOCK.sub(lambda m: f"<!-- ranged_fields {m.group(1)} -->\n{b[m.group(1)]}\n<!-- /ranged_fields -->", text)


def main():
    b = blocks()
    a = sys.argv[1:]
    if a and a[0] in b:
        print(b[a[0]])
        return 0
    text = open(PAGE, encoding="utf-8", newline="").read()
    new = render(text.replace("\r\n", "\n"), b)
    if "--check" in a:
        if new != text.replace("\r\n", "\n"):
            print("stale: " + PAGE)
            return 1
        print("ok")
        return 0
    if "--write" in a:
        open(PAGE, "w", encoding="utf-8", newline="\n").write(new)
        print("written")
        return 0
    print(b["counts"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
