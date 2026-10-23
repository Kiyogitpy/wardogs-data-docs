"""Independent verifier for assets/data/weapon-damage.json (round 24, teammate D).

Recomputes per-hit damage from the raw data/ export only. It does NOT import
weapon_damage_tables.py or damage_tables.py. Rules follow
pipelines/Wardogs_DamagePipeline_v2.md sections 4-7:
  C = BaseDamage; for every infantry rule entry that matches (hostile alignment,
  source tags, target tags, hit location, no instigator tags) multiply C by its
  factor; clamp at 0.
Run:  python _tools/verify_weapon_damage.py        (from anywhere)
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs")
DMG = os.path.join(DATA, "Content/GameMechanics/DamageSystem/DamageDataTables")
HIT = "Meta.Damage.HitLocation.Infantry."
TOL = 1e-6


def exports(path):
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"^--- export:.*---\s*$", text, flags=re.M)
    return [json.loads(p) for p in parts[1:] if p.strip()]


def table(name):
    return exports(os.path.join(DMG, name))[0]["Rows"]


def tg(x):
    return x.get("TagName") if isinstance(x, dict) else x


def expand(tags):
    """Tags plus every parent tag (down to two levels, e.g. Meta.Damage)."""
    out = set()
    for t in tags:
        parts = t.split(".")
        for i in range(2, len(parts) + 1):
            out.add(".".join(parts[:i]))
    return out


def parent(t):
    return t.rsplit(".", 1)[0] if "." in t else None


def kv(lst):
    return {tg(x["Key"]): x["Value"] for x in lst}


def first_list(row):
    return next((val for val in row.values() if isinstance(val, list)), [])


# ---------------------------------------------------------------- rule tables
ENTRIES = table("DT_GlobalDamage_InfantryData.json")["Meta.Damage.Infantry"]["DamageModificationEntries"]
BONE = {k: kv(v["HitLocations"]) for k, v in table("DT_Helpers/DT_InfantryData_BoneDamageModifiers.json").items()}
CAL = {k: kv(first_list(v)) for k, v in table("DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json").items()}
PEN = {k: (v.get("Modifier", 1.0), kv(first_list(v)))
       for k, v in table("DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json").items()}

# armor: context tag -> DamagePercentageReduction of the first (undamaged) durability stage
DPR = {}
for p in glob.glob(os.path.join(DATA, "Plugins/GameFeatures/Items/Armor/Content/Data/ID_*.json")):
    for o in exports(p):
        if o.get("Type") == "WDInventoryFragment_Armor":
            st = o["Properties"].get("DurabilityStagesSetupData") or []
            if st:
                DPR[tg(o["Properties"]["DamageContextTag"])] = st[0]["DamagePercentageReduction"]

# ---------------------------------------------------------------- ammo items and projectiles
PROJ = {}  # DA name -> (source tag, [context], base damage, pellets)
for p in glob.glob(os.path.join(DATA, "Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json"), recursive=True):
    for o in exports(p):
        s = o.get("Properties", {}).get("ProjectileStats")
        if s:
            e = s["DamageEntityData"]
            pel = o["Properties"].get("NumberOfPellets") or s.get("NumberOfPellets")
            PROJ[o["Name"]] = (tg(e["Tag"]), [tg(c) for c in e.get("Context", [])], s["DamageValues"]["BaseDamage"], pel)

ITEMS = {}  # item id tag -> dict
for p in glob.glob(os.path.join(DATA, "Content/Items/Resources/Ammo/**/ID_*.json"), recursive=True):
    ex = exports(p)
    d = next((o for o in ex if o.get("Type") == "BHInventoryItemDefinition"), None)
    pr = next((o for o in ex if o.get("Type") == "WDInventoryFragment_Projectile"), None)
    if not d or not pr:
        continue
    pd = re.search(r"'(DA_\w+)'", pr["Properties"]["ProjectileData"]["ObjectName"]).group(1)
    cal = [c for c in d["Properties"]["ItemContext"] if c.startswith("Item.Caliber.")]
    ITEMS[tg(d["Properties"]["ItemId"])] = {"cal": cal[0] if cal else None, "proj": pd, "file": os.path.basename(p)}

AMMO_MAP = {"Tracer", "HollowPoint", "HollowPoint.Tracer", "ArmorPiercing", "ArmorPiercing.Tracer"}


def modifier_tag(item_id):
    """Section 7.9: last name, or last two names for a five-level tag ending in Tracer; fixed map only."""
    parts = item_id.split(".")
    key = ".".join(parts[-2:]) if len(parts) == 5 and parts[-1] == "Tracer" else parts[-1]
    return "Meta.Damage.AmmoModifier." + key if key in AMMO_MAP else None


# ---------------------------------------------------------------- weapons
STATS = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(DATA, "**/DA_*_Stats.json"), recursive=True)}


def walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                yield v
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)


def weapon_info(wid):
    path = next(iter(glob.glob(os.path.join(DATA, "Plugins/GameFeatures/Weapons/**/ID_%s.json" % wid), recursive=True)))
    text = open(path, encoding="utf-8").read()
    wtag = None
    for o in exports(path):
        for d in walk(o, "DamageEntityData"):
            t = tg(d.get("Tag", {}))
            if t and t.startswith("Meta.Damage.Weapon"):
                wtag = t
    stats = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", text).group(1)
    cals = next(c for o in exports(STATS[stats]) for c in walk(o, "SupportedCaliber"))
    return wtag, list(cals)


# ---------------------------------------------------------------- the rule engine
def damage(wtag, item_id, hit, armor_tag=None):
    it = ITEMS[item_id]
    stag, ctx, base, _ = PROJ[it["proj"]]
    mod = modifier_tag(item_id)
    context = list(ctx) + ([mod] if mod else []) + [wtag]
    source = expand([stag] + context)
    target = expand([armor_tag]) if armor_tag else set()
    hitfull = HIT + hit
    lineage = expand([hitfull])
    c = float(base)
    used = []
    for i, e in enumerate(ENTRIES):
        m = e["OutModification"]
        reqs = [e["InstigatorRequirements"], e["TargetRequirements"], e["SourceRequirements"], e["PossibleHitLocations"]]
        if not any(reqs) and m["Amount"] == 0:
            continue
        if e["AlignmentRequired"].split("::")[-1] not in ("None", "Hostile"):
            continue
        if e["InstigatorRequirements"]:
            continue  # instigator tags are not supplied
        if not set(e["TargetRequirements"]) <= target or not set(e["SourceRequirements"]) <= source:
            continue
        if e["PossibleHitLocations"] and not set(e["PossibleHitLocations"]) & lineage:
            continue
        f = 1.0
        if m["bUseCustomOperation"]:
            cls = (m["CustomOperationClass"] or {}).get("ObjectName", "")
            if "BoneDamage" in cls:
                u = BONE["Universal"][hitfull]
                row = next((BONE[t] for t in context if t in BONE), None) or \
                    next((BONE[parent(t)] for t in context if parent(t) in BONE), None)
                f = u * (row[hitfull] if row else 1.0)
            elif "ArchetypeCaliber" in cls:
                row = next((CAL[t] for t in context if t in CAL), None) or \
                    next((CAL[parent(t)] for t in context if parent(t) in CAL), None)
                f = 1.0 if row is None else row.get(stag, row.get(parent(stag), 1.0))
            elif "AmmoTypeEffectiveness" in cls:
                piece = next((t for t in sorted(target) if t.startswith(("Meta.Damage.Armor.", "Meta.Damage.Helmet."))), None)
                r = DPR.get(piece, 0.0) if piece else 0.0
                ammo = mod or "Meta.Damage.AmmoModifier.FMJ"
                arms = next((t for t in context if t.startswith("Meta.Damage.Arms")), None)
                mo, ov = PEN.get(ammo, (1.0, {}))
                f = 1 - r * ov.get(arms, mo) / 100
            else:
                continue  # armor durability / seat reduction need explosive-blunt, melee or vehicle sources
        elif m["Operation"].endswith("Percentage_Ongoing"):
            f = 1 + m["Amount"] / 100
        else:
            continue
        c *= f
        used.append(i)
    return max(c, 0.0), used


def cells():
    """(group, key), hit location, armor tag for every cell the JSON publishes."""
    out = []
    for loc in ("Head", "Neck", "Torso.Upper", "Torso.Middle", "Arm.Upper", "Leg.Thigh"):
        out.append((("location", loc), loc, None))
    for cls in ("None", "Light", "Medium", "Heavy", "SuperHeavy"):
        out.append((("torso_armor", cls), "Torso.Upper", None if cls == "None" else "Meta.Damage.Armor." + cls))
        out.append((("head_armor", cls), "Head", None if cls == "None" else "Meta.Damage.Helmet." + cls))
    return out


SAMPLE = [
    ("M4", "FMJ", "location", "Torso.Upper"), ("M4", "ArmorPiercing", "location", "Torso.Upper"),
    ("M4", "HollowPoint", "location", "Torso.Upper"), ("M4", "Tracer", "location", "Head"),
    ("M4", "HollowPoint", "torso_armor", "SuperHeavy"), ("M4", "ArmorPiercing", "torso_armor", "Medium"),
    ("M4", "FMJ", "torso_armor", "Light"), ("M4", "FMJ", "head_armor", "Heavy"),
    ("M4", "HollowPoint.Tracer", "head_armor", "SuperHeavy"), ("M4", "ArmorPiercing.Tracer", "head_armor", "Medium"),
    ("AK74M", "FMJ", "location", "Neck"), ("WEPN_030", "FMJ", "location", "Torso.Upper"),
    ("SVDM", "ArmorPiercing", "torso_armor", "Heavy"), ("WEPN_017", "FMJ", "head_armor", "None"),
    ("Glock17", "FMJ", "location", "Arm.Upper"), ("Glock17", "ArmorPiercing", "torso_armor", "Medium"),
    ("Glock17", "ArmorPiercing", "torso_armor", "Heavy"), ("WEPN_026", "FMJ", "location", "Torso.Upper"),
    ("WEPN_026", "HollowPoint", "head_armor", "Light"), ("WEPN_027", "ArmorPiercing", "torso_armor", "Heavy"),
    ("WEPN_027", "FMJ", "location", "Leg.Thigh"), ("SR_04", "FMJ", "torso_armor", "Heavy"),
    ("SR_04", "ArmorPiercing", "torso_armor", "Heavy"), ("SR_04", "ArmorPiercing", "head_armor", "SuperHeavy"),
    ("SR_04", "FMJ", "location", "Torso.Middle"), ("WEPN_035", "FMJ", "location", "Torso.Upper"),
    ("WEPN_035", "ArmorPiercing", "head_armor", "Medium"), ("MK22", "HollowPoint", "location", "Head"),
    ("M500", "Buckshot", "location", "Torso.Upper"), ("M500", "Slug", "location", "Torso.Upper"),
    ("M500", "Slug", "torso_armor", "Heavy"), ("M500", "Buckshot", "head_armor", "Medium"),
    ("Judge", "FMJ", "location", "Head"), ("SKS", "HollowPoint", "head_armor", "Heavy"),
    ("WEPN_037", "ArmorPiercing", "torso_armor", "Medium"), ("AK74M", "ArmorPiercing", "torso_armor", "Light"),
]


def main():
    wd = json.load(open(os.path.join(ROOT, "assets/data/weapon-damage.json"), encoding="utf-8"))
    W = {w["id"]: w for w in wd["weapons"]}
    fails = 0
    maxdiff = 0.0
    total = 0
    rows = {}
    ties = set()

    for wid, w in W.items():
        wtag, cals = weapon_info(wid)
        if wtag.replace("Meta.Damage.Weapon.", "") != w["weapon_tag"]:
            print("FAIL weapon tag", wid, wtag, w["weapon_tag"])
            fails += 1
        for a in w["ammo"]:
            for item_id in a["items"]:
                if modifier_tag(item_id) != a["modifier_tag"]:
                    print("FAIL modifier tag", wid, item_id, modifier_tag(item_id), a["modifier_tag"])
                    fails += 1
                bd = PROJ[ITEMS[item_id]["proj"]][2]
                if bd != a["base_damage"]:
                    print("FAIL base damage", wid, item_id, bd, a["base_damage"])
                    fails += 1
                for (grp, key), hit, armor in cells():
                    mine, used = damage(wtag, item_id, hit, armor)
                    theirs = a["damage_raw"][grp][key]
                    d = abs(mine - theirs)
                    total += 1
                    maxdiff = max(maxdiff, d)
                    rows[(wid, a["id"], grp, key)] = (mine, theirs, d, a["damage"][grp][key])
                    if d > TOL:
                        fails += 1
                        print("FAIL", wid, a["id"], grp, key, mine, theirs)
                    shown = a["damage"][grp][key]
                    if abs(round(mine, 1) - shown) > 1e-9:
                        if abs(mine * 10 - round(mine * 10) - 0.0) < 1e-6 or abs(abs(mine * 10 - int(mine * 10)) - 0.5) < 1e-6:
                            ties.add((wid, a["id"], grp, key, round(mine, 6), shown))
                        else:
                            fails += 1
                            print("FAIL rounding", wid, a["id"], grp, key, mine, shown)
    for t in sorted(ties):
        print("TIE (exact value ends in 5 at the second decimal; json rounds the other way):", *t)
    print("full sweep: %d cells, max abs diff %.3e, failures %d" % (total, maxdiff, fails))

    print("\nnamed sample (PASS/FAIL weapon ammo group key: mine / json damage_raw / diff / json rounded)")
    sfail = 0
    for k in SAMPLE:
        mine, theirs, d, rnd = rows[k]
        ok = d <= TOL
        sfail += not ok
        print("%s %-9s %-20s %-12s %-12s %10.4f %10.4f %.1e %6.1f" % ("PASS" if ok else "FAIL", *k, mine, theirs, d, rnd))
    print("sample: %d cells, %d failures" % (len(SAMPLE), sfail))
    fails += sfail

    eb = 0
    ids = set()
    for wid, w in W.items():
        for o in w["same_damage_as"]:
            ids.add(o)
            ids.add(wid)
            for a, b in zip(w["ammo"], W[o]["ammo"]):
                if a["id"] != b["id"] or a["damage_raw"] != b["damage_raw"] or a["base_damage"] != b["base_damage"]:
                    eb += 1
                    print("FAIL same_damage_as", wid, o, a["id"])
    print("(e) same_damage_as: %d weapons in groups, mismatches %d" % (len(ids), eb))
    fails += eb
    sig = {}
    for wid, w in W.items():
        sig.setdefault(json.dumps([a["damage_raw"] for a in w["ammo"]], sort_keys=True), []).append(wid)
    for g in sig.values():
        for x in g:
            if set(g) - {x} != set(W[x]["same_damage_as"]):
                print("NOTE group listing differs from identical-value group:", x, g, W[x]["same_damage_as"])

    print("(g) .338 items:", {k: modifier_tag(k) for k in ITEMS if ".338Nor" in k})
    print("(g) weapons among the 33 chambering .338:", [w for w in W if "Item.Caliber.338Nor" in weapon_info(w)[1]])
    for k, v in sorted(ITEMS.items()):
        if "12g" in k or "7mmBuck" in k:
            print("(h)", k, PROJ[v["proj"]])
    # ammo-availability.json (teammate B): item tags -> resolved modifier tag -> projectile, every caliber
    av = json.load(open(os.path.join(ROOT, "assets/data/ammo-availability.json"), encoding="utf-8"))
    afail = 0
    seen_items = set()
    for ckey, c in av["calibers"].items():
        mine_items = {k for k, it in ITEMS.items() if it["cal"] == c["id"]}
        theirs = {a["item"] for a in c["ammo"]}
        if c.get("alias"):
            # an alias lists items filed under another Item.Caliber key because their projectile id differs
            if not theirs <= set(ITEMS):
                afail += 1
                print("FAIL alias items unknown", ckey, theirs - set(ITEMS))
        elif mine_items != theirs and not (theirs - set(ITEMS) and mine_items <= theirs):
            # (items without a projectile fragment: arrows, charges, drone shot: not in my ITEMS table)
            afail += 1
            print("FAIL ammo items", ckey, sorted(mine_items ^ theirs))
        for a in c["ammo"]:
            seen_items.add(a["item"])
            if a["item"] not in ITEMS:
                continue
            it = ITEMS[a["item"]]
            if modifier_tag(a["item"]) != a["modifierTag"]:
                afail += 1
                print("FAIL ammo modifier", a["item"], modifier_tag(a["item"]), a["modifierTag"])
            st = PROJ.get(it["proj"])
            if st and (it["proj"] != a["projectileAsset"] or st[2] != a["projectile"]["baseDamage"]
                       or st[1] != a["projectile"]["context"]):
                afail += 1
                print("FAIL ammo projectile", a["item"], it["proj"], st)
    for k in ITEMS:
        if k not in seen_items:
            afail += 1
            print("FAIL ammo item missing from ammo-availability.json:", k)
    print("ammo-availability: %d calibers, %d items, failures %d" % (len(av["calibers"]), len(seen_items), afail))
    fails += afail

    print("\nRESULT:","PASS" if fails == 0 else "FAIL (%d)" % fails, "max diff %.3e" % maxdiff)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
