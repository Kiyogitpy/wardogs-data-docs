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
    python _tools/infantry_damage.py --vehicles # rule factor per vehicle row and caliber
    python _tools/infantry_damage.py --survive  # hits to destroy six vehicles, per section hit

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


VEHICLE_CALIBERS = ["Item.Caliber.556mm", "Item.Caliber.762mm", "Item.Caliber.762x54mm", "Item.Caliber.308Win",
                    "Item.Caliber.50Cal", "Item.Caliber.20x102mm", "Item.Caliber.30mm", "Item.Caliber.35x228mm"]


def vehicle_table(proj):
    """Rule factor per vehicle row and caliber: FMJ direct hit, entries without a hit-location filter."""
    vehicle_rows = []
    for path in sorted(glob.glob(os.path.join(DATA, "Wardogs/Plugins/**/DT_GlobalDamage_VehicleData_*.json"), recursive=True)):
        vehicle_rows += list(exports(path)[0]["Rows"].items())
    generic = rows("DT_GlobalDamage_VehicleData.json")["Meta.Damage.Vehicle"]["DamageModificationEntries"]
    cals = [c for c in VEHICLE_CALIBERS if c in proj]
    print("| Vehicle row (`Meta.Damage.Vehicle.` omitted) | " + " | ".join(f"`{c.replace('Item.Caliber.', '')}`" for c in cals) + " |")
    print("|---|" + "---:|" * len(cals))
    for key, row in vehicle_rows:
        cells = []
        for cal in cals:
            src, ctx, _ = proj[cal]
            source = expand(ctx + [src, cal, "Meta.Damage.DamageType.Projectile"])
            total = 1.0
            for e in row["DamageModificationEntries"] + generic:  # own row, then the generic parent level
                m = e["OutModification"]
                if e["PossibleHitLocations"] or e["InstigatorRequirements"] or e["TargetRequirements"]:
                    continue
                if not e["SourceRequirements"] or not set(e["SourceRequirements"]) <= source:
                    continue
                if m["Operation"].endswith("Percentage_Ongoing"):
                    total *= 1 + m["Amount"] / 100
            cells.append(f"×{max(total, 0):.3g}")
        print(f"| `{key.replace('Meta.Damage.Vehicle.', '')}` | " + " | ".join(cells) + " |")


# Platform modules assembled per vehicle (chosen by name; the composition asset is not traced).
SURVIVE = {
    "Land.Wheeled.Bobcat": ["VP_WHL_01", "VP_WHL_01_Wheels"],
    "Land.Wheeled.Humvee.Default": ["VP_WHL_05", "VP_WHL_05_MainBody_Default", "VP_WHL_05_Wheels_Humvee"],
    "Land.Wheeled.Ural": ["VP_WHL_07", "VP_WHL_07_MainBody_Default", "VP_WHL_07_Rearback", "VP_WHL_07_Wheels"],
    "Air.Rotary.Havoc": ["VP_ROT_02", "VP_ROT_02_MainBody_Default"],
    "Air.Rotary.LittleBird": ["VP_ROT_03", "VP_ROT_03_Body"],
    "Land.Tracked.TNK_01.Heavy": ["VP_TNK_01_Heavy", "VP_TNK_01_Turret_Heavy"],
}
MAIN = "Attribute.Gameplay.Health"


def sections(modules):
    """Section tag -> (max health, hit-location tag, pre, post, simultaneous) from the platform modules."""
    files = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(DATA, "**/VP_*.json"), recursive=True)}
    out = {}
    for name in modules:
        for o in exports(files[name]):
            for kv in o.get("Properties", {}).get("HealthSections", []):
                v = kv["Value"]
                routes = lambda key: [(tag(r["Key"]), r["Value"]["Scalar"]["Value"], r["Value"]["bOnlyWhenDepleted"])
                                      for r in v.get(key, [])]
                hit = next((t for t in v.get("Tags", []) if t.startswith("Meta.Damage.HitLocation.")), None)
                out[tag(kv["Key"])] = (v["MaxHealth"], hit, routes("PreDamageRouting"),
                                       routes("PostDamageRouting"), routes("SimultaneousDamageRouting"))
    return out


def apply_section(secs, health, key, amount, depth=0):
    """One point-damage application to a section (0x53205D0 / 0x5339DD0); returns the amount absorbed.

    Assumes section health stops at 0 (the attribute hook is not traced; the depleted-only post
    routes in the data only carry damage if it does)."""
    if key not in secs or depth > 10 or amount <= 0:
        return 0.0
    _, _, pre, post, simul = secs[key]
    handled = 0.0

    def reroute(routes):
        nonlocal handled
        for target, scalar, only_depleted in routes:
            if (health[key] <= 0) == only_depleted and amount - handled > 0:
                handled += apply_section(secs, health, target, (amount - handled) * min(max(scalar, 0), 1), depth + 1)

    reroute(pre)
    own = min(max(amount - handled, 0), max(health[key], 0))
    health[key] -= own
    handled += own
    if key == MAIN and health[MAIN] <= 0:
        return handled  # vehicle destroyed: no simultaneous or post routing
    for target, scalar, only_depleted in simul:
        if not only_depleted or health[key] <= 0:
            apply_section(secs, health, target, own * min(max(scalar, 0), 1), depth + 1)
    reroute(post)
    return handled


def survive_table(proj):
    generic = rows("DT_GlobalDamage_VehicleData.json")["Meta.Damage.Vehicle"]["DamageModificationEntries"]
    vrows = {}
    for path in glob.glob(os.path.join(DATA, "Wardogs/Plugins/**/DT_GlobalDamage_VehicleData_*.json"), recursive=True):
        vrows.update(exports(path)[0]["Rows"])
    cals = ["Item.Caliber.556mm", "Item.Caliber.50Cal", "Item.Caliber.20x102mm", "Item.Caliber.30mm"]
    print("| Vehicle | Section hit (max health) | " + " | ".join(f"`{c.replace('Item.Caliber.', '')}`" for c in cals) + " |")
    print("|---|---|" + "---:|" * len(cals))
    for key, modules in SURVIVE.items():
        secs = sections(modules)
        entries = vrows["Meta.Damage.Vehicle." + key]["DamageModificationEntries"] + generic
        for sec, (hp, hit, *_) in secs.items():
            if not hit:
                continue
            cells = []
            for cal in cals:
                src, ctx, base = proj[cal]
                source = expand(ctx + [src, cal, "Meta.Damage.DamageType.Projectile"])
                f = 1.0
                for e in entries:
                    m = e["OutModification"]
                    if e["InstigatorRequirements"] or e["TargetRequirements"] or not e["SourceRequirements"]:
                        continue
                    if not set(e["SourceRequirements"]) <= source:
                        continue
                    if e["PossibleHitLocations"] and not set(e["PossibleHitLocations"]) & set(lineage(hit)):
                        continue
                    if m["Operation"].endswith("Percentage_Ongoing"):
                        f *= 1 + m["Amount"] / 100
                dmg = base * max(f, 0)
                health = {k: v[0] for k, v in secs.items()}
                hits = 0
                while health.get(MAIN, 0) > 0 and hits < 2000 and dmg > 0:
                    apply_section(secs, health, sec, dmg)
                    hits += 1
                cells.append("—" if dmg <= 0 or hits >= 2000 else str(hits))
            print(f"| `{key}` | {sec.replace('Attribute.Gameplay.', '')} ({hp:g}) | " + " | ".join(cells) + " |")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    proj = projectiles()
    if "--survive" in sys.argv:
        survive_table(proj)
        return
    if "--vehicles" in sys.argv:
        vehicle_table(proj)
        return
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
