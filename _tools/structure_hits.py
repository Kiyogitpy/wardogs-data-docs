"""Round 42: hits to destroy every buildable, for every projectile and explosive in the data.

Extends the four-source estimate of round 36 (docs/evidence/round36-combat.md section 2) to every
projectile (bullets with FMJ / armor-piercing / hollow-point, cannons, rockets, the 12 gauge) and
every explosive actor in assets/data/explosive-actors.json. For each buildable it takes the damage
row named by the asset (DT_GlobalDamage_BuildableData), selects the entries whose SourceRequirements
are all in the lineage of the source tags (the matching rule of damage_tables.matches) and applies
them as the game does (DamagePipeline v2 section 6): Percentage_Ongoing multiplies the running amount
by 1 + Amount/100, Add adds Amount (only the tracked-vehicle entry), the result is clamped at 0.

    hits = ceil(MaxHealth / damage)       damage = base * product(1 + Amount/100) [+ flat Add]

Derived: point blank, full base damage at the centre of an explosion, no falloff, no ricochet, no
penetration, no instigator rule (the buildable rows have none), one hit, finished structure.
The buildable rows have no instigator, target or hit-location requirements and no custom operation
(checked here), so the combine is exact for the entries present.

    python -I _tools/structure_hits.py            print the table
    python -I _tools/structure_hits.py --json     write assets/data/structure-hits.json (idempotent)
    python -I _tools/structure_hits.py --check    assert key values (exit 1 on mismatch)
"""
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402

ROOT = dt.ROOT
BUILD = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Items", "Buildables", "Content", "Data")
OUT = os.path.join(ROOT, "assets", "data", "structure-hits.json")
MODS = ["FMJ", "ArmorPiercing", "HollowPoint"]


def load_rows():
    path = os.path.join(BUILD, "DT_GlobalDamage_BuildableData.json")
    text = open(path, encoding="utf-8").read()
    return json.JSONDecoder().raw_decode(text[text.index("{"):])[0]["Rows"]


def buildables():
    out = {}
    for f in sorted(glob.glob(os.path.join(BUILD, "Buildables", "**", "DA_Buildable_*.json"), recursive=True)):
        if f.endswith("_Stages.json"):
            continue
        for o in dt.exports(f):
            p = o.get("Properties", {})
            if o.get("Type") == "WDBuildableDataAsset" and "MaxHealth" in p:
                row = None
                for v in dt.walk(p, "TagName"):
                    if isinstance(v, str) and v.startswith("Meta.Damage.Buildable."):
                        row = v
                        break
                if row:
                    out[os.path.basename(f)[len("DA_Buildable_"):-5]] = (p["MaxHealth"], row)
    return out


def sources():
    """(label, kind, base, set of source tags) for every projectile variant and explosive actor."""
    res = []
    for pid, (src, ctx, base) in sorted(dt.projectiles().items()):
        if base is None or not src:
            continue
        label = pid.replace("Item.Caliber.", "")
        if src.startswith("Meta.Damage.Bullet"):
            for m in MODS:
                tags = dt.expand(ctx + [src, "Meta.Damage.AmmoModifier." + m])
                res.append((f"{label} {m}", "bullet", float(base), tags))
        else:
            kind = "cannon" if src.startswith("Meta.Damage.Cannon") else "rocket" if "Rocket" in src else "other"
            res.append((label, kind, float(base), dt.expand(ctx + [src])))
    ex = json.load(open(os.path.join(ROOT, "assets", "data", "explosive-actors.json"), encoding="utf-8"))["actors"]
    for name, a in sorted(ex.items()):
        base = (a.get("damage_values") or {}).get("BaseDamage")
        if base is None or not a.get("source_tag"):
            continue
        res.append((name, "explosive", float(base), dt.expand(list(a.get("source_context", [])) + [a["source_tag"]])))
    return res


def apply(entries, tags, base):
    cur, hit = base, []
    for i, e in enumerate(entries):
        m = e["OutModification"]
        if m["bUseCustomOperation"]:
            raise SystemExit("custom operation in buildable rows: tool assumption broken")
        if not set(e["SourceRequirements"]) <= tags:
            continue
        if e["InstigatorRequirements"] or e["TargetRequirements"] or e["PossibleHitLocations"]:
            raise SystemExit("requirement beyond source in buildable rows: tool assumption broken")
        op = m["Operation"].split("::")[-1]
        if op == "Percentage_Ongoing" and m["Amount"]:
            cur += cur * m["Amount"] / 100.0
            hit.append(i)
        elif op == "Add" and m["Amount"]:
            cur += m["Amount"]
            hit.append(i)
        elif op == "Percentage_Starting" and m["Amount"]:
            cur += base * m["Amount"] / 100.0
            hit.append(i)
    return max(cur, 0.0), hit


def build():
    rows, bld, srcs = load_rows(), buildables(), sources()
    res = {"meta": {
        "generator": "python -I _tools/structure_hits.py --json",
        "unit": "hits to destroy a finished structure; damage per hit in health points",
        "assumptions": ["point blank, full base damage at the centre of an explosion, no falloff, no ricochet or penetration",
                        "the buildable damage rows have only source requirements and no custom operation (asserted)",
                        "no pellet multiplication: 12 gauge values are per pellet",
                        "Derived (DamagePipeline v2 section 6 arithmetic over the matching entries)"]},
        "structures": {k: {"max_health": v[0], "row": v[1]} for k, v in bld.items()},
        "sources": [], "damage": {}, "hits": {}}
    for label, kind, base, tags in srcs:
        res["sources"].append({"id": label, "kind": kind, "base": base})
        res["damage"][label] = {}
        res["hits"][label] = {}
        for name, (hp, row) in bld.items():
            d, applied = apply(rows[row]["DamageModificationEntries"], tags, base)
            res["damage"][label][name] = round(d, 3)
            res["hits"][label][name] = math.ceil(hp / d - 1e-9) if d > 0 else None
    return res


def main():
    res = build()
    if "--json" in sys.argv:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(res, f, indent=1, sort_keys=False)
            f.write("\n")
        print("wrote", OUT, len(res["sources"]), "sources x", len(res["structures"]), "structures")
        return
    if "--check" in sys.argv:
        h = res["hits"]
        want = [("5.56mm FMJ".replace("5.56mm", "556mm"), "SandbagWall")]
        ok = True
        # round 36 values for the four sources on the Sandbag Wall (M4 175, M67 8, 120 mm rocket 1, C4 1)
        m4 = next(k for k in h if k.endswith("556mm FMJ"))
        ok &= h[m4]["SandbagWall"] == 175
        ok &= h["C4"]["SandbagWall"] == 1 if "C4" in h else True
        print("PASS" if ok else "FAIL", m4, h[m4]["SandbagWall"])
        sys.exit(0 if ok else 1)
    names = list(res["structures"])
    print("source".ljust(34), *[n[:9].ljust(9) for n in names])
    for s in res["sources"]:
        print(s["id"][:33].ljust(34), *[str(res["hits"][s["id"]][n]).ljust(9) for n in names])


if __name__ == "__main__":
    main()
