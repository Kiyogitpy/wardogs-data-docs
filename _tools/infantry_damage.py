"""Per-weapon infantry damage multipliers, rebuilt from data/ with the pipeline's own rules.

Rebuilds the damage event a bullet hit produces (Wardogs_DamagePipeline_v2.md §7.7) and
runs it through the infantry rule row the way the native collector and evaluator do
(§4-§7): requirement matching on explicit-or-parent tags, every non-custom entry as
1 + Amount/100, and each custom operation's factor. Everything multiplies, so order
does not matter.

Assumptions, printed with the table: hostile alignment, FMJ ammo, a direct hit with no
ricochet or penetration, an unarmored target outside any vehicle, and no instigator
tags. Entries that need instigator tags are counted as unknown instead of applied.

    python _tools/infantry_damage.py            # markdown table on stdout
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
EXPORT = re.compile(r"^--- export: .* ---\r?\n", re.M)
DS = "Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/"
LOCATIONS = ["Head", "Neck", "Torso.Upper", "Torso.Middle", "Arm.Upper", "Leg.Thigh"]
HIT = "Meta.Damage.HitLocation.Infantry."


def exports(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(part) for part in EXPORT.split(f.read())[1:]]


def walk(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            yield obj[key]
        for v in obj.values():
            yield from walk(v, key)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v, key)


def tag(t):
    return t.get("TagName") if isinstance(t, dict) else t


def parent(t):
    return t.rsplit(".", 1)[0] if "." in t else None


def lineage(t):
    out = []
    while t:
        out.append(t)
        t = parent(t)
    return out


def expand(tags):
    return {p for t in tags for p in lineage(t)}


def tag_map(pairs):
    return {tag(p["Key"]): p["Value"] for p in pairs}


def rows(name):
    return exports(os.path.join(DATA, DS, name))[0]["Rows"]


def first_row(table, context):
    """The Blueprints' row search: first context tag naming a row, else its direct parent."""
    for t in context:
        for key in (t, parent(t)):
            if key in table:
                return table[key]
    return None


ENTRIES = rows("DT_GlobalDamage_InfantryData.json")["Meta.Damage.Infantry"]["DamageModificationEntries"]
BONE = {k: tag_map(v["HitLocations"]) for k, v in rows("DT_Helpers/DT_InfantryData_BoneDamageModifiers.json").items()}
CALIBER = {k: tag_map(next(x for f, x in v.items() if f.startswith("_aaabapbnbhiopifeenjml")))
           for k, v in rows("DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json").items()}


def projectiles():
    """ProjectileId -> (source tag, source context, BaseDamage) from the caliber data assets."""
    out = {}
    pattern = os.path.join(DATA, "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json")
    for path in sorted(glob.glob(pattern, recursive=True)):
        for o in exports(path):
            props = o.get("Properties", {})
            pid, stats = tag(props.get("ProjectileId")), props.get("ProjectileStats")
            if not pid or not stats:
                continue
            ent = stats.get("DamageEntityData", {})
            base = stats.get("DamageValues", {}).get("BaseDamage")
            # Prefer the plain DA_<caliber>_ProjectileData asset when a caliber has variants.
            if pid not in out or os.path.basename(path).count("_") <= 2:
                out[pid] = (tag(ent.get("Tag")), [tag(t) for t in ent.get("Context", [])], base)
    return out


def weapons():
    """(item name, weapon damage tag, supported calibers) for every weapon item."""
    stats = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(DATA, "**/DA_*_Stats.json"), recursive=True)}
    out = []
    for path in sorted(glob.glob(os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Weapons/**/ID_*.json"), recursive=True)):
        text = open(path, encoding="utf-8").read()
        wtag = next((tag(d.get("Tag")) for o in exports(path) for d in walk(o, "DamageEntityData")
                     if (tag(d.get("Tag")) or "").startswith("Meta.Damage.Weapon")), None)
        ref = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", text)
        if not wtag or not ref or ref.group(1) not in stats:
            continue
        cals = next((c for o in exports(stats[ref.group(1)]) for c in walk(o, "SupportedCaliber")), [])
        out.append((os.path.basename(path)[3:-5], wtag, cals))
    return out


def matches(e, source, target, hit, alignment="Hostile"):
    need = e["AlignmentRequired"].split("::")[-1]
    if need != "None" and need != alignment:
        return False
    if not set(e["TargetRequirements"]) <= target or not set(e["SourceRequirements"]) <= source:
        return False
    locs = e["PossibleHitLocations"]
    return not locs or bool(set(locs) & set(lineage(hit)))


def factor(e, hit, source_tag, context):
    m = e["OutModification"]
    if not m["bUseCustomOperation"]:
        return 1 + m["Amount"] / 100 if m["Operation"].endswith("Percentage_Ongoing") else 1.0
    cls = (m["CustomOperationClass"] or {}).get("ObjectPath", "")
    if "B_BoneDamageModifiers" in cls:
        if source_tag == "Meta.Damage.Explosive.Drone":
            return 1.0
        u = BONE["Universal"].get(hit, 0.0)
        row = first_row(BONE, context)
        w = row.get(hit, 0.0) if row is not None else 1.0
        return u * w
    if "B_ArchetypeCaliberModifiers" in cls:
        row = first_row(CALIBER, context)
        if row is None:
            return 1.0
        return row.get(source_tag, row.get(parent(source_tag), 1.0))
    return 1.0  # ammo/armor, seat and armor durability: no armor, not in a vehicle


def evaluate(source_tag, context, hit):
    source = expand(context + [source_tag])
    total, unknown, applied = 1.0, 0, []
    for i, e in enumerate(ENTRIES):
        m = e["OutModification"]
        empty = not any(e[k] for k in ("InstigatorRequirements", "TargetRequirements",
                                       "SourceRequirements", "PossibleHitLocations"))
        if empty and m["Amount"] == 0:
            continue
        if not matches(e, source, set(), hit):
            continue
        if e["InstigatorRequirements"]:
            unknown += 1
            continue
        f = factor(e, hit, source_tag, context)
        if f != 1.0:
            applied.append(i)
        total *= f
    return max(total, 0.0), unknown, applied


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    proj = projectiles()
    print("| Weapon | Weapon tag | Caliber | Base | " + " | ".join(LOCATIONS) + " | Entries applied |")
    print("|---|---|---|---:|" + "---:|" * len(LOCATIONS) + "---|")
    for name, wtag, cals in sorted(weapons(), key=lambda w: (w[1], w[0])):
        cal = next((c for c in cals if c in proj), None)  # first supported caliber with projectile data
        if not cal or not (proj[cal][0] or "").startswith("Meta.Damage.Bullet"):
            continue  # launchers: their direct impact is not the bullet case
        src, ctx, base = proj[cal]
        context = ctx + [wtag, cal, "Meta.Damage.DamageType.Projectile"]
        cells, used, unk = [], set(), 0
        for loc in LOCATIONS:
            f, unk, applied = evaluate(src, context, HIT + loc)
            used.update(applied)
            cells.append(f"{base * f:.1f} (×{f:.3g})")
        short = wtag.replace("Meta.Damage.Weapon.", "")
        note = ", ".join(map(str, sorted(used))) + (f"; {unk} need instigator tags" if unk else "")
        print(f"| {name} | `{short}` | `{cal.replace('Item.Caliber.', '')}` | {base:g} | " + " | ".join(cells) + f" | {note} |")


if __name__ == "__main__":
    main()
