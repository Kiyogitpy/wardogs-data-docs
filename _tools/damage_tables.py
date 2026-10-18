"""Damage tables for the pipeline docs, rebuilt from data/ with the pipeline's own rules.

Rebuilds the damage event a bullet hit produces (Wardogs_DamagePipeline_v2.md §7.7) and
runs it through the infantry rule row the way the native collector and evaluator do
(§4-§7): requirement matching on explicit-or-parent tags, every non-custom entry as
1 + Amount/100, and each custom operation's factor. Everything multiplies, so order
does not matter.

Assumptions, printed with the table: hostile alignment, FMJ ammo, a direct hit with no
ricochet or penetration, an unarmored target outside any vehicle, and no instigator
tags. Entries that need instigator tags are counted as unknown instead of applied.

    python _tools/damage_tables.py            # per-location table (point blank)
    python _tools/damage_tables.py --falloff  # upper-torso damage by distance
    python _tools/damage_tables.py --ammo M4  # one weapon: ammo type x armor class
    python _tools/damage_tables.py --vehicles # rule factor per vehicle row and caliber
    python _tools/damage_tables.py --survive  # hits to destroy every vehicle variant
    python _tools/damage_tables.py --hitboxes # collision slot -> section map and damage ratios per vehicle, unreachable keys marked
    python _tools/damage_tables.py --json     # assets/data/vehicle-hitboxes.json for the hitbox viewer
    python _tools/damage_tables.py --write    # refresh every marked table in the docs (and the JSON) after a data update

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
PEN = {k: (v.get("Modifier", 1.0), tag_map(next((x for f, x in v.items() if f.startswith("_aaabcfjheicbfejiaihii")), [])))
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
    # The native class (PlayerArmorDurability) is named only in ObjectName; its ObjectPath is /Script/WDGame.
    cls = " ".join((m["CustomOperationClass"] or {}).get(k, "") for k in ("ObjectPath", "ObjectName"))
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


MAIN = "Attribute.Gameplay.Health"
_FILES = {}


def asset_file(path_or_name):
    """Export file for an asset path like /WHL_05/Parts/VP_X.VP_X or a bare asset name."""
    if not _FILES:
        for p in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
            _FILES.setdefault(os.path.basename(p)[:-5], p)
    name = path_or_name.rsplit("/", 1)[-1].split(".")[0]
    return _FILES.get(name)


def assemble(variant_path):
    """A variant's modules: its platform plus every slot's part (variant override, else the slot default),
    recursing into parts' own slots. Override paths are dotted slot names (e.g. Rearback.Chassis)."""
    v = next(o for o in exports(variant_path) if o.get("Type") == "ModularVehicleVariant")["Properties"]
    data = v["AssemblyData"]
    overrides = {s["Path"]["Path"]: s["Part"]["AssetPathName"]
                 for s in data.get("CustomData", {}).get("SlotOverrides", [])}
    modules, missing = [], []

    def visit(path, prefix):
        f = asset_file(path)
        if not f:
            missing.append(path)
            return
        modules.append(f)
        objs = {o.get("Name"): o for o in exports(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for s in (owner or {}).get("Properties", {}).get("Slots", []):
            if not s["Value"].get("bEnabled", True):
                continue
            name = prefix + s["Key"]
            slot = objs.get(s["Value"]["Slot"]["ObjectName"].split(":")[-1].rstrip("'"), {})
            part = overrides.get(name) or slot.get("Properties", {}).get("DefaultPart", {}).get("AssetPathName")
            if part:
                visit(part, name + ".")

    visit(data["VehicleBase"]["ObjectPath"].split(".")[0], "")
    return modules, missing, tag(v["VariantID"])


def sections(module_files):
    """Section tag -> (max health, hit-location tag, pre, post, simultaneous) from enabled health fragments."""
    out = {}
    for f in module_files:
        objs = {o.get("Name"): o for o in exports(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for fr in (owner or {}).get("Properties", {}).get("Fragments", []):
            obj = objs.get(fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'"), {})
            if not fr["Value"].get("bEnabled", True) or obj.get("Type") != "MVF_HealthSections":
                continue
            for kv in obj.get("Properties", {}).get("HealthSections", []):
                val = kv["Value"]
                routes = lambda key: [(tag(r["Key"]), r["Value"]["Scalar"]["Value"], r["Value"]["bOnlyWhenDepleted"])
                                      for r in val.get(key, [])]
                hit = next((t for t in val.get("Tags", []) if t.startswith("Meta.Damage.HitLocation.")), None)
                out[tag(kv["Key"])] = (val["MaxHealth"], hit, routes("PreDamageRouting"),
                                       routes("PostDamageRouting"), routes("SimultaneousDamageRouting"))
    return out


def damage_tag(module_files):
    """VehicleDamageTag from DA_GameplaySystems_*, found through the modules' DA_*Config references."""
    seen = set()
    queue = list(module_files)
    while queue:
        f = queue.pop(0)
        if f in seen or not f:
            continue
        seen.add(f)
        if "GameplaySystems" in os.path.basename(f):
            for o in exports(f):
                t = next(walk(o, "VehicleDamageTag"), None)
                if t:
                    return tag(t)
        text = open(f, encoding="utf-8").read()
        for ref in set(re.findall(r"(DA_[A-Za-z0-9_]*(?:Config|GameplaySystems)[A-Za-z0-9_]*)", text)):
            queue.append(asset_file(ref))
    return None


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


def vehicle_rule_factor(entries, cal, hit, proj):
    """Product of the vehicle-row (and generic-row) factors for an FMJ direct hit of caliber `cal` on a
    section whose hit-location tag is `hit` (entries without instigator/target requirements)."""
    src, ctx, _ = proj[cal]
    source = expand(ctx + [src, cal, "Meta.Damage.DamageType.Projectile"])
    f = 1.0
    for e in entries:
        m = e["OutModification"]
        if e["InstigatorRequirements"] or e["TargetRequirements"] or not e["SourceRequirements"]:
            continue
        if not set(e["SourceRequirements"]) <= source:
            continue
        if e["PossibleHitLocations"] and not (hit and set(e["PossibleHitLocations"]) & set(lineage(hit))):
            continue
        if m["Operation"].endswith("Percentage_Ongoing"):
            f *= 1 + m["Amount"] / 100
    return max(f, 0.0)


def fragments(module_files):
    """The enabled fragment objects of the assembled modules."""
    for f in module_files:
        objs = {o.get("Name"): o for o in exports(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for fr in (owner or {}).get("Properties", {}).get("Fragments", []):
            if fr["Value"].get("bEnabled", True):
                yield objs.get(fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'"), {})


def surface_maps(module_files):
    """(surface group, collision slot or '(default)') -> section tag, from enabled health fragments."""
    out = {}
    for obj in fragments(module_files):
        if obj.get("Type") != "MVF_HealthSections":
            continue
        for g in obj.get("Properties", {}).get("ComplexSurfaceMappings", {}).get("SurfaceGroups", []):
            group, val = tag(g["Key"]), g["Value"]
            for s in val.get("SlotMap", []):
                out[(group, s["Key"])] = tag(s["Value"])
            if val.get("bUseDefault"):
                out[(group, "(default)")] = tag(val.get("Default"))
    return out


def registered(module_files):
    """Surface groups registered by the variant's mesh components and by its instanced wheels, and
    the slot names the wheels suffix with their DataIndex (VehicleDamagePipeline §3.2)."""
    meshes, wheels, indexed = set(), set(), set()
    for obj in fragments(module_files):
        kind, p = obj.get("Type"), obj.get("Properties", {})
        if kind == "MVF_StaticMesh" and p.get("bRegisterComplexSurface", True):
            meshes.add(tag(p.get("SurfaceGroup")) or "ComplexSurface.Group.Default")
        elif kind == "MVF_InstancedWheels":
            wheels.add("ComplexSurface.Group.Wheel")
            indexed.update(p.get("IndexedSlotNames", []))
        elif kind == "MVF_DestructibleMeshes":
            for d in p.get("DestructibleMeshesData", []):
                for s in d.get("DestructibleMeshesSettings", []):
                    if s.get("bRegisterComplexSurface") and tag(s.get("SurfaceGroup")) not in (None, "None"):
                        meshes.add(tag(s.get("SurfaceGroup")))
    return meshes, wheels, indexed


def unreachable(group, slot, meshes, wheels, indexed):
    """Why no registered component can produce this map key, or None. A lookup starts at the hit
    component's group and walks up to parent groups, so the key's group must be on such a walk.
    Wheel hits on an indexed slot always carry the instance suffix; mesh hits never do."""
    by_mesh = any(group in lineage(g) for g in meshes)
    by_wheel = any(group in lineage(g) for g in wheels)
    if not by_mesh and not by_wheel:
        return "no component registers this group"
    base = re.sub(r"_\d+$", "", slot)
    if base != slot:
        if not (by_wheel and base in indexed):
            return "an indexed name, but no instanced wheel indexes this slot"
    elif slot in indexed and not by_mesh:
        return "instanced wheels add their index to this slot"
    return None


def row_entries(dtag, vrows):
    """The entries of every per-vehicle row on the target tag's parent walk, most specific first."""
    return [e for t in lineage(dtag) if t in vrows for e in vrows[t]["DamageModificationEntries"]]


def vehicle_tables():
    generic = rows("DT_GlobalDamage_VehicleData.json")["Meta.Damage.Vehicle"]["DamageModificationEntries"]
    vrows = {}
    for path in glob.glob(os.path.join(DATA, "Wardogs/Plugins/**/DT_GlobalDamage_VehicleData_*.json"), recursive=True):
        vrows.update(exports(path)[0]["Rows"])
    return generic, vrows


def variants():
    """Every vehicle variant file, in name order."""
    return sorted(glob.glob(os.path.join(DATA, "**", "Variants", "VV_*.json"), recursive=True))


def vehicle_groups(vrows):
    """Variants that share a damage tag and slot map, in variant order: [(damage tag, sections, slot map,
    registered surfaces, variant names)]. Variants without a slot map or a damage tag are left out."""
    seen = {}
    for vpath in variants():
        modules, _, _ = assemble(vpath)
        secs, dtag, smap = sections(modules), damage_tag(modules), surface_maps(modules)
        if not smap or not dtag:
            continue
        key = (dtag, tuple(sorted(smap.items())))
        seen.setdefault(key, (dtag, secs, smap, registered(modules), []))[4].append(os.path.basename(vpath)[3:-5])
    return list(seen.values())


def hits_to_destroy(secs, sec, dmg, cap=5000):
    """Direct hits of `dmg` on section `sec` until the main health reaches 0 (§4 order and routing),
    or None when it never does (no damage, or the section does not route to the main health)."""
    health = {k: v[0] for k, v in secs.items()}
    hits = 0
    while health.get(MAIN, 0) > 0 and hits < cap and dmg > 0:
        apply_section(secs, health, sec, dmg)
        hits += 1
    return hits if dmg > 0 and hits < cap else None


def hitbox_table(proj):
    """Collision slot -> section map per vehicle, with section health, routing to the main health and the
    rule factor per caliber at that hitbox. Variants sharing a damage row and map are listed once."""
    generic, vrows = vehicle_tables()
    cals = ["Item.Caliber.556mm", "Item.Caliber.50Cal", "Item.Caliber.30mm"]
    print("| Vehicle (variants) | Collision slot | Section (max health) | Routing to main health | "
          + " | ".join(f"`{c.replace('Item.Caliber.', '')}`" for c in cals) + " |")
    print("|---|---|---|---|" + "---:|" * len(cals))
    for dtag, secs, smap, reg, names in vehicle_groups(vrows):
        entries = row_entries(dtag, vrows) + generic
        own = "" if dtag in vrows else ", no row of its own"
        label = f"`{dtag.replace('Meta.Damage.Vehicle.', '')}` ({', '.join(names)}{own})"
        for (group, slot), sec in sorted(smap.items(), key=lambda kv: (kv[0][1] == "(default)", kv[0])):
            hp, hit, pre, post, simul = secs.get(sec, (None, None, [], [], []))
            routes = [f"pre {s:g}" for t2, s, _ in pre if t2 == MAIN] +                      [f"post {s:g} when depleted" if d else f"post {s:g}" for t2, s, d in post if t2 == MAIN] +                      [f"simultaneous {s:g}" for t2, s, _ in simul if t2 == MAIN]
            routing = "is the main health" if sec == MAIN else (", ".join(routes) or "none")
            cells = [f"×{vehicle_rule_factor(entries, c, hit, proj):.3g}" for c in cals]
            grp = "" if group == "ComplexSurface.Group.Default" else f" [{group.replace('ComplexSurface.Group.', '')}]"
            why = unreachable(group, slot, *reg) if slot != "(default)" else unreachable(group, "", *reg)
            note = f" (unreachable: {why})" if why else ""
            hp_s = f"{hp:g}" if hp is not None else "?"
            print(f"| {label} | `{slot}`{grp}{note} | {sec.replace('Attribute.Gameplay.', '')} ({hp_s}) | {routing} | "
                  + " | ".join(cells) + " |")
            label = ""


def survive_table(proj):
    """Hits to destroy every vehicle variant: main body, and the fastest section, per caliber."""
    generic, vrows = vehicle_tables()
    cals = ["Item.Caliber.556mm", "Item.Caliber.50Cal", "Item.Caliber.20x102mm", "Item.Caliber.30mm"]
    print("| Variant | Damage row (`Meta.Damage.Vehicle.` omitted) | Main health | "
          + " | ".join(f"`{c.replace('Item.Caliber.', '')}`" for c in cals) + " |")
    print("|---|---|---:|" + "---|" * len(cals))
    for vpath in variants():
        modules, missing, _ = assemble(vpath)
        secs, dtag = sections(modules), damage_tag(modules)
        if MAIN not in secs or not dtag:
            continue  # no health model or no damage tag for this variant
        entries = row_entries(dtag, vrows) + generic
        cells = []
        for cal in cals:
            base = proj[cal][2]
            results = {}
            for sec, (hp, hit, *_) in secs.items():
                if not hit:
                    continue
                hits = hits_to_destroy(secs, sec, base * vehicle_rule_factor(entries, cal, hit, proj))
                if hits is not None:
                    results[sec] = hits
            main = results.get(MAIN)
            best = min(results.items(), key=lambda kv: kv[1]) if results else None
            cell = "—" if main is None else str(main)
            if best and best[0] != MAIN and (main is None or best[1] < main):
                cell += f" / {best[1]} ({best[0].replace(MAIN + '.', '')})"
            cells.append(cell)
        name = os.path.basename(vpath)[3:-5]
        print(f"| `{name}` | `{dtag.replace('Meta.Damage.Vehicle.', '')}` | {secs[MAIN][0]:g} | " + " | ".join(cells) + " |")


JSON_OUT = os.path.join(ROOT, "assets", "data", "vehicle-hitboxes.json")
MODELS = "assets/models/vehicles"
JSON_CALIBERS = {"Item.Caliber.556mm": "5.56mm", "Item.Caliber.762mm": "7.62mm", "Item.Caliber.50Cal": ".50Cal",
                 "Item.Caliber.20x102mm": "20x102mm", "Item.Caliber.30mm": "30mm", "Item.Caliber.35x228mm": "35x228mm"}


def glb_summary(path):
    """(variants the GLB depicts, notes on it, from asset.extras; material name -> world-space bounding-box centre
    [x, y, z] in metres, glTF axes, of the primitives that use it; asset.extras.damage_state or None). Reads the
    GLB's JSON chunk alone: POSITION
    accessors must carry min/max, so no buffer decoding."""
    import struct
    with open(path, "rb") as f:
        f.seek(12)
        size, kind = struct.unpack("<II", f.read(8))
        gltf = json.loads(f.read(size)) if kind == 0x4E4F534A else {}
    norm = {5120: 127, 5121: 255, 5122: 32767, 5123: 65535}

    def mul(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

    def local(n):
        if "matrix" in n:
            m = n["matrix"]  # column-major
            return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
        x, y, z, w = n.get("rotation", [0, 0, 0, 1])
        sx, sy, sz = n.get("scale", [1, 1, 1])
        tx, ty, tz = n.get("translation", [0, 0, 0])
        r = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
             [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
             [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
        return [[r[i][0] * sx, r[i][1] * sy, r[i][2] * sz, (tx, ty, tz)[i]] for i in range(3)] + [[0, 0, 0, 1]]

    boxes = {}

    def visit(i, parent):
        n = gltf["nodes"][i]
        world = mul(parent, local(n))
        for p in gltf["meshes"][n["mesh"]]["primitives"] if "mesh" in n else []:
            if "material" not in p or "POSITION" not in p["attributes"]:
                continue
            acc = gltf["accessors"][p["attributes"]["POSITION"]]
            d = norm.get(acc["componentType"]) if acc.get("normalized") else None
            lo, hi = ([max(v / d, -1.0) if d else v for v in acc[k]] for k in ("min", "max"))
            name = gltf["materials"][p["material"]].get("name", "")
            box = boxes.setdefault(name, [[float("inf")] * 3, [float("-inf")] * 3])
            for corner in ([(lo, hi)[(c >> a) & 1][a] for a in range(3)] for c in range(8)):
                pt = [sum(world[r][k] * (corner + [1])[k] for k in range(4)) for r in range(3)]
                box[0] = [min(a, b) for a, b in zip(box[0], pt)]
                box[1] = [max(a, b) for a, b in zip(box[1], pt)]
        for c in n.get("children", []):
            visit(c, world)

    identity = [[float(r == c) for c in range(4)] for r in range(4)]
    for i in gltf.get("scenes", [{}])[gltf.get("scene", 0)].get("nodes", []):
        visit(i, identity)
    extras = gltf.get("asset", {}).get("extras", {})
    return (extras.get("variants", []), extras.get("notes", []),
            {k: [round((a + b) / 2, 4) for a, b in zip(*v)] for k, v in boxes.items()}, extras.get("damage_state"))


def hitbox_json(proj):
    """assets/data/vehicle-hitboxes.json for the hitbox viewer: the --hitboxes map with full routing, the rule
    factor and the hits to destroy through each slot for every caliber, and the vehicle's GLBs (one per
    distinct variant geometry, matched by the variants each GLB declares) with each slot's centre on them."""
    import subprocess
    glbs = {}
    for p in sorted(glob.glob(os.path.join(ROOT, MODELS, "*.glb"))):
        glbs[f"{MODELS}/{os.path.basename(p)}"] = glb_summary(p)
    generic, vrows = vehicle_tables()
    cals = [c for c in JSON_CALIBERS if c in proj]
    # The data/ tree id names the exact input in any clone, shallow ones included (a commit lookup there can
    # stop at the shallow boundary).
    tree = subprocess.run(["git", "rev-parse", "HEAD:data"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    out = {"meta": {
        "source_data_tree": tree,
        "source_data_tree_note": "git tree id of data/ when generated; equals `git rev-parse <commit>:data` for any commit with the same data",
        "generator": "python _tools/damage_tables.py --json",
        "assumptions": ["FMJ direct hit at point blank: no falloff, ricochet or penetration",
                        "hostile instigator with no instigator tags; rules that need instigator or target tags are skipped",
                        "section health stops at 0; routing as in Vehicle §4.2",
                        "a hit takes the section of its triangle's slot as in Vehicle §3.1 (projectile and radial hits); "
                        "unreachable names why no registered component can produce a slot key",
                        "hits_to_destroy counts hits through that slot until the main health reaches 0; "
                        "null when it never does (no damage, or no route to the main health)"],
        "docs": {"hitboxes": "Wardogs_VehicleDamagePipeline_v1.html#31-hitboxes",
                 "routing": "Wardogs_VehicleDamagePipeline_v1.html#42-routing-semantics",
                 "hits_to_destroy": "Wardogs_VehicleDamagePipeline_v1.html#54-hits-to-destroy"},
        "main_section": MAIN,
        "calibers": [{"id": c, "label": JSON_CALIBERS[c], "base_damage": proj[c][2]} for c in cals]},
        "vehicles": []}
    groups = vehicle_groups(vrows)
    shared = {d for d in (g[0] for g in groups) if sum(g[0] == d for g in groups) > 1}
    for dtag, secs, smap, reg, names in groups:
        entries = row_entries(dtag, vrows) + generic
        # One file per damage row and slot map: a row with several maps adds its first variant's name.
        slug = re.sub(r"[^a-z0-9]+", "-", (dtag.replace("Meta.Damage.Vehicle.", "")
                                            + ("." + names[0] if dtag in shared else "")).lower())
        # A GLB without declared variants counts as <id>.glb showing the group's first variant.
        models, damaged = [], []
        for path, (declared, notes, centres, damage) in glbs.items():
            shown = [n for n in names if n in (declared or ([names[0]] if path == f"{MODELS}/{slug}.glb" else []))]
            if shown:
                (damaged if damage else models).append((path, shown, notes, centres, damage))
        models.sort(key=lambda m: names.index(m[1][0]))
        slots = []
        for (group, slot), sec in sorted(smap.items(), key=lambda kv: (kv[0][1] == "(default)", kv[0])):
            hp, hit, pre, post, simul = secs.get(sec, (None, None, [], [], []))
            factors = {c: round(vehicle_rule_factor(entries, c, hit, proj), 6) for c in cals}
            slots.append({
                "slot": slot, "group": group, "section": sec, "max_health": hp, "hit_location": hit,
                "unreachable": unreachable(group, "" if slot == "(default)" else slot, *reg),
                "routing": {k: [{"to": t, "scalar": s, "only_when_depleted": d} for t, s, d in r]
                            for k, r in (("pre", pre), ("post", post), ("simultaneous", simul))},
                "rule_factor": factors,
                "hits_to_destroy": {c: hits_to_destroy(secs, sec, proj[c][2] * factors[c]) if sec in secs else None
                                    for c in cals}})
        # GLB materials outside the Default surface group are named "<slot>|<Group>".
        keys = [s["slot"] if s["group"] == "ComplexSurface.Group.Default"
                else f"{s['slot']}|{s['group'].rsplit('.', 1)[-1]}" for s in slots]
        entries_out = []
        for path, vs, notes, centres, _ in models:
            m = {"variants": vs, "path": path, "notes": notes, "centres": [centres.get(k) for k in keys]}
            # The same model with every wheel destroyed (a GLB with damage_state declaring its first variant).
            d = next((x for x in damaged if x[4] == "wheels_destroyed" and vs[0] in x[1]), None)
            if d:
                m["wheels_destroyed"] = {"variants": vs, "path": d[0], "notes": d[2], "centres": [d[3].get(k) for k in keys]}
            entries_out.append(m)
        out["vehicles"].append({"id": slug, "damage_row": dtag, "variants": names, "main_health": secs.get(MAIN, (None,))[0],
                                "models": entries_out, "slots": slots})
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    with open(JSON_OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{os.path.relpath(JSON_OUT, ROOT)}: {len(out['vehicles'])} vehicles, "
          f"{sum(len(v['slots']) for v in out['vehicles'])} slots, {sum(len(v['models']) for v in out['vehicles'])} models")


BLOCK = re.compile(r"<!-- damage_tables (.+?) -->\r?\n.*?<!-- /damage_tables -->", re.S)
DOCS = ["Wardogs_DamagePipeline_v2.md", "Wardogs_VehicleDamagePipeline_v1.md", "vehicle-viewer.md"]


def write_docs():
    """Regenerate every <!-- damage_tables MODE --> block in the docs in place."""
    import subprocess
    for doc in DOCS:
        path = os.path.join(ROOT, doc)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        nl = "\r\n" if "\r\n" in text else "\n"

        def regen(m):
            mode = m.group(1)
            args = [] if mode == "default" else mode.split()
            out = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + args,
                                 capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
            return nl.join([f"<!-- damage_tables {mode} -->"] + out.split("\n") + ["<!-- /damage_tables -->"])

        new, n = BLOCK.subn(regen, text)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"{doc}: {n} tables {'updated' if new != text else 'unchanged'}")
    hitbox_json(projectiles())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv:
        write_docs()
        return
    proj = projectiles()
    if "--json" in sys.argv:
        hitbox_json(proj)
        return
    if "--hitboxes" in sys.argv:
        hitbox_table(proj)
        return
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
