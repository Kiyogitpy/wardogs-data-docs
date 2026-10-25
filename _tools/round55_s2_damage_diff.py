"""Round 55: Season 1 -> Season 2 changes in the infantry and buildable global damage tables.

Compares the entries of DT_GlobalDamage_InfantryData and DT_GlobalDamage_BuildableData by content
(requirements, operation, amount, category), not by index, because Season 2 inserted entries and
every later index moved. An entry present on only one side is printed as ADDED or REMOVED with its
index on that side. For the buildable table it also prints the damage factor (damage / base) that the
three cannon and shell sources get on every row in both seasons, using the round 42 evaluator
(_tools/structure_hits.py: every matching entry multiplies by 1 + Amount/100).

    python -I _tools/round55_s2_damage_diff.py [--s1 DIR]    # DIR = Season 1 data/ (default E:/r22/s1/data)

Read-only. Needs the Season 1 export used by _tools/season_diff.py.
"""
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import structure_hits as sh  # noqa: E402

ROOT = sh.ROOT
S1 = "E:/r22/s1/data"
if "--s1" in sys.argv:
    S1 = sys.argv[sys.argv.index("--s1") + 1]
INF = "Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json"
BLD = "Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/DT_GlobalDamage_BuildableData.json"


def rows(root, rel):
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    return json.loads(re.split(r"^--- export: .* ---\r?\n", text, flags=re.M)[1])["Rows"]


def key(e):
    o = e["OutModification"]
    return (tuple(e["InstigatorRequirements"]), tuple(e["TargetRequirements"]), tuple(e["SourceRequirements"]),
            tuple(e["PossibleHitLocations"]), e["AlignmentRequired"], o["Operation"], o["Amount"],
            o["bUseCustomOperation"], str(o["CustomOperationClass"]), o["PriorityCategory"]["TagName"])


def show(i, e):
    o = e["OutModification"]
    short = lambda xs, p: [x.replace(p, "") for x in xs]
    return (f"  {i}: target={short(e['TargetRequirements'], 'Meta.Damage.')} source={short(e['SourceRequirements'], 'Meta.Damage.')} "
            f"where={short(e['PossibleHitLocations'], 'Meta.Damage.HitLocation.')} {o['Operation'].split('::')[-1]} {o['Amount']} "
            f"custom={(o['CustomOperationClass'] or {}).get('ObjectName')} category={o['PriorityCategory']['TagName'].replace('Meta.Damage.Category.', '')}")


def content_diff(rel):
    a, b = rows(S1, rel), rows(os.path.join(ROOT, "data"), rel)
    for rk in b:
        A = a.get(rk, {}).get("DamageModificationEntries", [])
        B = b[rk]["DamageModificationEntries"]
        print(f"{rk}: Season 1 {len(A)} entries, Season 2 {len(B)} entries")
        c = Counter(key(e) for e in B)
        for i, e in enumerate(A):
            if c[key(e)] <= 0:
                print("  REMOVED" + show(i, e))
            else:
                c[key(e)] -= 1
        c = Counter(key(e) for e in A)
        for i, e in enumerate(B):
            if c[key(e)] <= 0:
                print("  ADDED" + show(i, e))
            else:
                c[key(e)] -= 1


def factors():
    r2, r1 = sh.load_rows(), rows(S1, BLD)
    for label, _kind, base, tags in sh.sources():
        if label not in ("125x570mm", "20x102mm", "35x228mm"):
            continue
        parts = []
        for row in r2:
            d2 = sh.apply(r2[row]["DamageModificationEntries"], tags, base)[0]
            d1 = sh.apply(r1[row]["DamageModificationEntries"], tags, base)[0] if row in r1 else None
            parts.append(f"{row.split('.')[-1]} {'n/a' if d1 is None else round(d1 / base, 4)} -> {round(d2 / base, 4)}")
        print(f"{label} damage factor (Season 1 -> Season 2): " + "; ".join(parts))


if __name__ == "__main__":
    print("== infantry table ==")
    content_diff(INF)
    print("== buildable table ==")
    content_diff(BLD)
    print("== cannon and shell factors on buildables ==")
    factors()
