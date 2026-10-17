"""Per-weapon infantry damage multipliers, rebuilt from data/ with the pipeline's own rules.

Rebuilds the damage event a bullet hit produces (Wardogs_DamagePipeline_v2.md §7.7) and
runs it through the infantry rule row the way the native collector and evaluator do
(§4-§7): requirement matching on explicit-or-parent tags, every non-custom entry as
1 + Amount/100, and each custom operation's factor. Everything multiplies, so order
does not matter.

Assumptions, printed with the table: hostile alignment, FMJ ammo, a direct hit with no
ricochet or penetration, an unarmored target outside any vehicle, and no instigator
tags. Entries that need instigator tags are counted as unknown instead of applied.

    python _tools/infantry_damage.py            # per-location table (point blank)
    python _tools/infantry_damage.py --falloff  # upper-torso damage by distance
    python _tools/infantry_damage.py --ammo M4  # one weapon: ammo type x armor class

The distance curve's Time axis is centimetres: the native code evaluates it with the
straight-line distance between shot origin and hit point in engine units.
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
PEN = {k: (v.get("Modifier", 1.0), tag_map(next((x for f, x in v.items() if f.startswith("_aaabckamhakccdhbomlfj")), [])))
       for k, v in rows("DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json").items()}


def armor_reduction():
    """Armor context tag -> DamagePercentageReduction (every item's stages share one value)."""
    out = {}
    for path in glob.glob(os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_*.json")):
        for o in exports(path):
            if o.get("Type") == "WDInventoryFragment_Armor":
                p = o["Properties"]
                stages = p.get("DurabilityStagesSetupData", [])
                out[tag(p.get("DamageContextTag"))] = stages[0].get("DamagePercentageReduction", 0.0) if stages else 0.0
    return out


ARMOR = armor_reduction()


def first_under(tags, roots):
    return next((t for t in tags if any(t == r or t.startswith(r + ".") for r in roots)), None)


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
        st = exports(stats[ref.group(1)])
        cals = next((c for o in st for c in walk(o, "SupportedCaliber")), [])
        use = next((b for o in st for b in walk(o, "bUseDistanceDamageFalloffCurve")), False)
        curve = next((c for o in st for c in walk(o, "DistanceDamageFalloffCurve")), {})
        keys = curve.get("EditorCurveData", {}).get("Keys", []) if use else []
        out.append((os.path.basename(path)[3:-5], wtag, cals, keys))
    return out


def falloff(keys, cm):
    """Linear evaluation of the distance curve (exact for RCIM_Linear keys), clamped at the ends."""
    if not keys:
        return 1.0
    pts = sorted((k["Time"], k["Value"]) for k in keys)
    if cm <= pts[0][0]:
        return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if cm <= t1:
            return v0 + (v1 - v0) * (cm - t0) / (t1 - t0)
    return pts[-1][1]


def matches(e, source, target, hit, alignment="Hostile"):
    need = e["AlignmentRequired"].split("::")[-1]
    if need != "None" and need != alignment:
        return False
    if not set(e["TargetRequirements"]) <= target or not set(e["SourceRequirements"]) <= source:
        return False
    locs = e["PossibleHitLocations"]
    return not locs or bool(set(locs) & set(lineage(hit)))


def factor(e, hit, source_tag, context, target=()):
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
    piece = first_under(target, ("Meta.Damage.Armor", "Meta.Damage.Helmet"))
    r = ARMOR.get(piece, 0.0) if piece else 0.0
    if "B_AmmoTypeEffectiveness" in cls:
        ammo = first_under(context, ("Meta.Damage.AmmoModifier",)) or "Meta.Damage.AmmoModifier.FMJ"
        if ammo not in PEN:
            return 1 - r / 100
        modifier, overrides = PEN[ammo]
        arms = first_under(context, ("Meta.Damage.Arms",))
        return 1 - r * overrides.get(arms, modifier) / 100
    if "PlayerArmorDurability" in cls:
        return 1 - r / 100
    return 1.0  # vehicle seat: target not in a vehicle


def evaluate(source_tag, context, hit, target=()):
    """Factor on S for one hit; target lists the covering armor tag, if any."""
    source, tgt = expand(context + [source_tag]), expand(target)
    total, unknown, applied = 1.0, 0, []
    for i, e in enumerate(ENTRIES):
        m = e["OutModification"]
        empty = not any(e[k] for k in ("InstigatorRequirements", "TargetRequirements",
                                       "SourceRequirements", "PossibleHitLocations"))
        if empty and m["Amount"] == 0:
            continue
        if not matches(e, source, tgt, hit):
            continue
        if e["InstigatorRequirements"]:
            unknown += 1
            continue
        f = factor(e, hit, source_tag, context, list(target))
        if f != 1.0:
            applied.append(i)
        total *= f
    return max(total, 0.0), unknown, applied


RANGES_M = [50, 100, 200, 400, 800, 1200]
AMMO = ["FMJ", "Tracer", "HollowPoint", "ArmorPiercing"]
CLASSES = ["Light", "Medium", "Heavy", "SuperHeavy"]


def ammo_table(name, proj):
    """One weapon: damage per ammo type against each armor class (torso) and helmet class (head)."""
    w = next(w for w in weapons() if w[0] == name)
    cal = next(c for c in w[2] if c in proj)
    src, ctx, base = proj[cal]
    cols = [("Torso.Upper", None)] + [("Torso.Upper", f"Meta.Damage.Armor.{c}") for c in CLASSES] \
        + [("Head", None)] + [("Head", f"Meta.Damage.Helmet.{c}") for c in CLASSES]
    print("| Ammo | Torso, no armor | " + " | ".join(f"Torso, {c}" for c in CLASSES)
          + " | Head, no helmet | " + " | ".join(f"Head, {c} helmet" for c in CLASSES) + " | Entries applied |")
    print("|---|" + "---:|" * len(cols) + "---|")
    for ammo in AMMO:
        # FMJ has no ammo-modifier asset, so its stats are the plain copy without a tag.
        extra = [] if ammo == "FMJ" else [f"Meta.Damage.AmmoModifier.{ammo}"]
        context = ctx + extra + [w[1], cal, "Meta.Damage.DamageType.Projectile"]
        cells, used = [], set()
        for loc, piece in cols:
            f, _, applied = evaluate(src, context, HIT + loc, [piece] if piece else [])
            used.update(applied)
            cells.append(f"{base * f:.1f}")
        print(f"| {ammo} | " + " | ".join(cells) + f" | {', '.join(map(str, sorted(used)))} |")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    proj = projectiles()
    if "--ammo" in sys.argv:
        ammo_table(sys.argv[sys.argv.index("--ammo") + 1], proj)
        return
    by_range = "--falloff" in sys.argv
    if by_range:
        print("| Weapon | Curve keys (m → ×) | " + " | ".join(f"{r} m" for r in RANGES_M) + " |")
        print("|---|---|" + "---:|" * len(RANGES_M))
    else:
        print("| Weapon | Weapon tag | Caliber | Base | " + " | ".join(LOCATIONS) + " | Entries applied |")
        print("|---|---|---|---:|" + "---:|" * len(LOCATIONS) + "---|")
    for name, wtag, cals, keys in sorted(weapons(), key=lambda w: (w[1], w[0])):
        cal = next((c for c in cals if c in proj), None)  # first supported caliber with projectile data
        if not cal or not (proj[cal][0] or "").startswith("Meta.Damage.Bullet"):
            continue  # launchers: their direct impact is not the bullet case
        src, ctx, base = proj[cal]
        context = ctx + [wtag, cal, "Meta.Damage.DamageType.Projectile"]
        if by_range:
            torso = base * evaluate(src, context, HIT + "Torso.Upper")[0]
            cubic = "†" if any(k.get("InterpMode") != "RCIM_Linear" for k in keys) else ""
            shown = ", ".join(f"{k['Time'] / 100:g}: {k['Value']:g}" for k in sorted(keys, key=lambda k: k["Time"])) or "none"
            cells = [f"{torso * falloff(keys, r * 100):.1f}" for r in RANGES_M]
            print(f"| {name}{cubic} | {shown} | " + " | ".join(cells) + " |")
            continue
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
