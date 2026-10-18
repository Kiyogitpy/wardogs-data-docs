"""Infantry hitbox tables for the infantry viewer, rebuilt from data/ with the documented rules only.

The bone -> hit-location map is DA_GlobalDamage_HitLocations_Player as exported (GameMechanics §2b).
Damage per hit location reuses _tools/damage_tables.py: the §7.6 bullet event, the rule row
DT_GlobalDamage_InfantryData (§3-§7) and the §7.7 / §7.8 generators' helpers (weapons, projectiles,
evaluate, falloff). Every source of character damage named in DamagePipeline §1.1 gets an entry; a path
the docs do not trace shows what the data says and is listed under not_traced instead of guessed.

    python _tools/infantry_tables.py              # hit-location table (same as --zones)
    python _tools/infantry_tables.py --zones      # hit location -> bones, Universal value, covering armor
    python _tools/infantry_tables.py --bones      # bone -> hit location, DamageImpactRemap, physics body
    python _tools/infantry_tables.py --multipliers  # bone factor Universal x row, per BoneDamageModifiers row
    python _tools/infantry_tables.py --sources    # every damage source: rule entries, hit location, armor
    python _tools/infantry_tables.py --explosives # launcher, cannon and shell rounds: direct and radial data
    python _tools/infantry_tables.py --armor      # helmet and armor items: tag, durability, R, coverage
    python _tools/infantry_tables.py --not-traced # the paths the docs leave open, with the data
    python _tools/infantry_tables.py --verified   # round-6 verifier answers cited by RVA (doc text pending)
    python _tools/infantry_tables.py --json       # assets/data/infantry-hitboxes.json for the viewer
    python _tools/infantry_tables.py --check      # compare the JSON with the doc tables
    python _tools/infantry_tables.py --write      # refresh <!-- infantry_tables MODE --> blocks and the JSON

Assumptions are the §7.7 ones (hostile alignment, FMJ, direct hit without ricochet or penetration, no
instigator tags, target outside any vehicle) and are written into the JSON's meta.
"""
import glob
import json
import os
import re
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402  (shared helpers: exports, rule row, evaluate, weapons, falloff)
from check_links import slug  # noqa: E402  (the site's GitHub-style heading ids)

ROOT, DATA = dt.ROOT, dt.DATA
DS = "Wardogs/Content/GameMechanics/DamageSystem/"
HITLOC_FILE = DS + "HitLocationDataAssets/DA_GlobalDamage_HitLocations_Player.json"
BONE_FILE = DS + "DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json"
RULE_FILE = DS + "DamageDataTables/DT_GlobalDamage_InfantryData.json"
ARMOR_GLOB = "Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_*.json"
JSON_OUT = os.path.join(ROOT, "assets", "data", "infantry-hitboxes.json")
MODEL = "assets/models/infantry/player.glb"
PAGE = "pipelines/infantry-viewer.md"
DP, GM, VDP = "pipelines/Wardogs_DamagePipeline_v2.md", "content/Wardogs_GameMechanics_v2.md", "pipelines/Wardogs_VehicleDamagePipeline_v1.md"

HIT = dt.HIT
PROJECTILE = "Meta.Damage.DamageType.Projectile"
BLUNT = "Meta.Damage.Kinetic.Impact.ExplosiveBlunt"
INNER, OUTER = "Meta.Damage.Explosive.Radius.Inner", "Meta.Damage.Explosive.Radius.Outer"
DRONE = "Meta.Damage.Explosive.Drone"
BONE_ENTRIES = (5, 7, 10)
REQS = ("InstigatorRequirements", "TargetRequirements", "SourceRequirements", "PossibleHitLocations")
LABELS = {"Head": "Head", "Neck": "Neck", "Torso.Upper": "Upper torso", "Torso.Middle": "Middle torso",
          "Torso.Lower": "Lower torso", "Pelvis": "Pelvis", "Arm.Upper": "Upper arm", "Arm.Lower": "Lower arm",
          "Arm.Hand": "Hand", "Leg.Thigh": "Thigh", "Leg.Calf": "Calf", "Leg.Foot": "Foot"}

def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def data_path(sub):
    return "data/" + sub


def rnd(x, n=None):
    """Computed values stay at full precision (rounding twice would move .3g / .1f cells off the doc tables)."""
    return None if x is None else (x + 0.0 if n is None else round(x + 0.0, n))


# --- docs ---------------------------------------------------------------------------------------

_HEAD = {}


def section(page, number):
    """(heading title, body) of the numbered heading `number` ("7.1", "2b") on a doc page."""
    if page not in _HEAD:
        with open(os.path.join(ROOT, page), encoding="utf-8") as f:
            text = f.read()
        _HEAD[page] = (text, list(re.finditer(r"^(#{1,6})\s+(.*?)\s*$", text, re.M)))
    text, heads = _HEAD[page]
    for i, m in enumerate(heads):
        first = m.group(2).split()[0].rstrip(".")
        if first == number:
            end = next((h.start() for h in heads[i + 1:] if len(h.group(1)) <= len(m.group(1))), len(text))
            return m.group(2), text[m.end():end]
    raise KeyError(f"{page}: no heading {number}")


def anchor(page, number):
    rel = os.path.relpath(page, os.path.dirname(PAGE)).replace(os.sep, "/")  # page-relative, like the viewer page
    return f"{rel[:-3]}.html#{slug(section(page, number)[0])}"


DOCS = {"callers": (DP, "1.1"), "custom_entries": (DP, "3.1"), "selection": (DP, "4"), "arithmetic": (DP, "6"),
        "bone_operation": (DP, "7.1"), "ammo_vs_armor": (DP, "7.3"), "armor_durability": (DP, "7.5"),
        "bullet_event": (DP, "7.6"), "per_weapon": (DP, "7.7"), "falloff": (DP, "7.8"), "ammo_types": (DP, "7.9"),
        "bone_table": (DP, "8.1"), "open_questions": (DP, "9"), "health": (DP, "10"),
        "hit_locations": (GM, "2b"), "bone_multipliers": (GM, "2c"),
        "radial_gather": (VDP, "3.2"), "vehicle_open_questions": (VDP, "7")}


def doc(key):
    return anchor(*DOCS[key])


# --- data ---------------------------------------------------------------------------------------

def hit_map():
    """(bone -> tag, bone -> remapped bone) from DA_GlobalDamage_HitLocations_Player, in export order."""
    p = dt.exports(os.path.join(DATA, HITLOC_FILE))[0]["Properties"]
    return ({h["Key"]: dt.tag(h["Value"]) for h in p["DamageHitLocations"]},
            {r["Key"]: r["Value"] for r in p.get("DamageImpactRemap", [])})


ZONES = list(dt.BONE["Universal"])  # the 12 tags in the table's (and §8.1's) order


def armor_items():
    out = []
    for path in sorted(glob.glob(os.path.join(DATA, ARMOR_GLOB))):
        for o in dt.exports(path):
            if o.get("Type") != "WDInventoryFragment_Armor":
                continue
            p = o["Properties"]
            t = dt.tag(p.get("DamageContextTag"))
            stages = [s.get("DamagePercentageReduction", 0.0) for s in p.get("DurabilityStagesSetupData", [])]
            covers = [c for c in ZONES if c in p.get("CoveredHitLocations", [])]
            entries = [i for i, e in enumerate(dt.ENTRIES)
                       if e["TargetRequirements"] and set(e["TargetRequirements"]) <= dt.expand([t])]
            out.append({"item": os.path.basename(path)[:-5], "tag": t,
                        "kind": "helmet" if t.startswith("Meta.Damage.Helmet") else "armor", "covers": covers,
                        "max_durability": (p.get("ReplicatedData") or {}).get("Durability"),
                        "reduction_pct": stages[0] if stages else 0.0, "stage_reductions": stages,
                        "entries": entries,
                        "custom_entries": [i for i in entries if dt.ENTRIES[i]["OutModification"]["bUseCustomOperation"]],
                        "path": rel(path)})
    return out


ARMOR_ITEMS = armor_items()


def projectile_assets():
    """ProjectileId -> asset record for every WDProjectileData export in data/. Same preference as
    damage_tables.projectiles(): the plain DA_<caliber>_ProjectileData asset when a caliber has variants."""
    out = {}
    caliber = sorted(glob.glob(os.path.join(DATA, "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json"),
                               recursive=True))
    rest = [p for p in sorted(glob.glob(os.path.join(DATA, "**", "DA_*.json"), recursive=True)) if p not in set(caliber)]
    for path in caliber + rest:  # the caliber assets first; elsewhere only ids they lack (debug assets reuse ids)
        with open(path, encoding="utf-8") as f:
            if '"ProjectileStats"' not in f.read():
                continue
        in_caliber = path in caliber
        for o in dt.exports(path):
            props = o.get("Properties", {})
            pid, st = dt.tag(props.get("ProjectileId")), props.get("ProjectileStats")
            if not pid or not st:
                continue
            ent, vals = st.get("DamageEntityData", {}), st.get("DamageValues", {})
            if pid not in out or (in_caliber and os.path.basename(path).count("_") <= 2):
                out[pid] = {"id": pid, "path": rel(path), "source_tag": dt.tag(ent.get("Tag")),
                            "context": [dt.tag(t) for t in ent.get("Context", [])],
                            "values": {k: v for k, v in vals.items() if isinstance(v, (int, float)) and not isinstance(v, bool)},
                            # An absent property is the class default (false / 0) in a cooked export.
                            "has_arming_delay": bool(st.get("bHasArmingDelay", False)),
                            "arming_delay": st.get("ArmingDelay")}
    return out


PROJ = projectile_assets()
_STATS = {}


def stats_file(name):
    if not _STATS:
        _STATS.update({os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(DATA, "**/DA_*_Stats.json"), recursive=True)})
    return _STATS.get(name)


def weapon_record(path, name=None):
    """(weapon tag or None, stats path, supported calibers, falloff keys, BackBlast config) for a weapon-like file."""
    text = open(path, encoding="utf-8").read()
    objs = dt.exports(path)
    wtag = next((dt.tag(d.get("Tag")) for o in objs for d in dt.walk(o, "DamageEntityData")
                 if (dt.tag(d.get("Tag")) or "").startswith("Meta.Damage.Weapon")), None)
    ref = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", text)
    sp = stats_file(ref.group(1)) if ref else None
    st = dt.exports(sp) if sp else []
    cals = next((c for o in st for c in dt.walk(o, "SupportedCaliber")), [])
    use = next((b for o in st for b in dt.walk(o, "bUseDistanceDamageFalloffCurve")), False)
    curve = next((c for o in st for c in dt.walk(o, "DistanceDamageFalloffCurve")), {})
    keys = curve.get("EditorCurveData", {}).get("Keys", []) if use else []
    back = next((b for o in st for b in dt.walk(o, "BackBlast")), None)
    return wtag, sp, cals, keys, back


def infantry_weapons():
    """damage_tables.weapons() (the §7.7 list), with each item's file for citations."""
    files = {os.path.basename(p)[3:-5]: p for p in
             glob.glob(os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Weapons/**/ID_*.json"), recursive=True)}
    out = []
    for name, wtag, cals, keys in dt.weapons():
        path = files[name]
        _, sp, _, _, back = weapon_record(path)
        out.append({"name": name, "wtag": wtag, "cals": cals, "keys": keys, "path": rel(path),
                    "stats": rel(sp) if sp else None, "backblast": back})
    return out


def other_weapons():
    """Weapon items and vehicle weapon extensions outside the Weapons plugin (bow, vehicle guns, the
    underbarrel launcher). Test items under VehicleBarrelLaunchersTests are left out."""
    out = []
    for path in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        r = rel(path)
        if "/GameFeatures/Weapons/" in r or "VehicleBarrelLaunchersTests" in r or "/DT_" in r:
            continue
        with open(path, encoding="utf-8") as f:
            if "WDWeaponStatsData'" not in f.read():
                continue
        wtag, sp, cals, keys, back = weapon_record(path)
        if not sp or not cals:
            continue
        out.append({"name": os.path.basename(path)[:-5], "wtag": wtag, "cals": cals, "keys": keys, "path": r,
                    "stats": rel(sp), "backblast": back})
    return out


def melee_items():
    out = []
    for path in sorted(glob.glob(os.path.join(DATA, "**", "ID_*.json"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            if "WDItemExtensionData_CharacterMelee" not in f.read():
                continue
        for o in dt.exports(path):
            if o.get("Type") != "WDItemExtensionData_CharacterMelee":
                continue
            p = o.get("Properties", {})
            out.append({"item": os.path.basename(path)[:-5], "path": rel(path),
                        "tag": dt.tag((p.get("DamageEntityData") or {}).get("Tag")),
                        "actions": [{"action": dt.tag(a["Key"]), "damage": a["Value"].get("Damage"),
                                     "trace_distance": a["Value"].get("TraceDistance"),
                                     "hit_box": a["Value"].get("HitBoxSize")} for a in p.get("MeleeActions", [])]})
    return out


def actor_class(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r'"(ThrowableClass|PlaceableClass)": \{\s*"(?:AssetPathName|ObjectName)": "([^"]+)"', text)
    return (m.group(1), m.group(2)) if m else (None, None)


def tag_defined(t):
    with open(os.path.join(DATA, "Wardogs/Config/DefaultGameplayTags.ini"), encoding="utf-8") as f:
        return f'Tag="{t}"' in f.read()


# --- rules --------------------------------------------------------------------------------------

def selected(src, context, hit, target=()):
    """[(entry, factor)] for one event, the selection and factors of damage_tables.evaluate (§4-§7);
    factor None marks an entry that needs instigator tags (none in the infantry row)."""
    source, tgt = dt.expand(context + [src]), dt.expand(target)
    out = []
    for i, e in enumerate(dt.ENTRIES):
        if not any(e[k] for k in REQS) and e["OutModification"]["Amount"] == 0:
            continue
        if not dt.matches(e, source, tgt, hit):
            continue
        out.append((i, None if e["InstigatorRequirements"] else dt.factor(e, hit, src, context, list(target))))
    total = 1.0
    for _, f in out:
        total *= f if f is not None else 1.0
    assert abs(max(total, 0.0) - dt.evaluate(src, context, hit, list(target))[0]) < 1e-9
    return out, max(total, 0.0)


def bone_row(context):
    """Key of the BoneDamageModifiers row §7.1 picks for this source context, or None (W = 1)."""
    for t in context:
        for key in (t, dt.parent(t)):
            if key in dt.BONE:
                return key
    return None


def candidates(tags, extra=()):
    """Entries whose source requirements `tags` (and their parents) meet, split into (hostile, armor-target,
    friendly). Used where the event's other fields are not traced."""
    source = dt.expand(list(tags) + list(extra))
    hostile, armor, friendly = [], [], []
    for i, e in enumerate(dt.ENTRIES):
        if not any(e[k] for k in REQS) and e["OutModification"]["Amount"] == 0:
            continue
        if not e["SourceRequirements"] or not set(e["SourceRequirements"]) <= source:
            continue
        if e["AlignmentRequired"].split("::")[-1] == "Friendly":
            friendly.append(i)
        elif e["TargetRequirements"]:
            armor.append(i)
        else:
            hostile.append(i)
    return hostile, armor, friendly


def entry_note(i):
    e = dt.ENTRIES[i]
    m = e["OutModification"]
    short = lambda xs: ", ".join(x.replace("Meta.Damage.", "") for x in xs) or "—"
    if m["bUseCustomOperation"]:
        obj = (m["CustomOperationClass"] or {}).get("ObjectName", "")
        change = "custom: " + (re.search(r"'([^']+)'", obj).group(1) if "'" in obj else obj)
    else:
        change = f"{m['Amount']:+g}%" if m["Operation"].endswith("Percentage_Ongoing") else "no change"
    return {"entry": i, "source": short(e["SourceRequirements"]), "target": short(e["TargetRequirements"]),
            "hit": short(e["PossibleHitLocations"]), "alignment": e["AlignmentRequired"].split("::")[-1],
            "custom": m["bUseCustomOperation"], "change": change}


# --- verified and not traced --------------------------------------------------------------------

R6 = "verifier round 6 (doc text pending)"


def verified():
    """Round-6 verifier answers, cited by RVA until the DamagePipeline text lands."""
    return [
        {"id": "hit-location-asset", "rvas": ["0x6F01BB0"],
         "text": "The hit-location asset is picked by the target actor's class (ClassToHitLocations)."},
        {"id": "bone-lookup", "rvas": ["0x6BB8D00"],
         "text": "The hit location is an exact FName match of the raw FHitResult.BoneName in DamageHitLocations: no "
                 "parent walk, and an unmapped bone gives an empty tag (no hit location)."},
        {"id": "impact-remap", "rvas": ["0x6BB8D40"],
         "text": "DamageImpactRemap is never applied for damage: its reader has 3 callers, all animation or ragdoll. "
                 "spine_05 is Torso.Upper for damage."},
        {"id": "physics-asset", "rvas": [],
         "text": "The hit bodies are PA_TPCharacter_Simplified's; all 20 map to a hit location. spine_01 and spine_02 have "
                 "no body, so a live player never produces them. Mutable adds each helmet's single head body, which "
                 "maps to Head."},
        {"id": "radial-hits", "rvas": ["0x6F06540", "0x6E6DCC0"],
         "text": "Radial damage: the gathered hits pass the character's IWDDamageable filter (dropped in one seat state, "
                 "otherwise one hit per component). Each kept hit is its own evaluation, tagged Radius.Inner or .Outer, "
                 "with that hit's bone as the hit location."},
        {"id": "blunt-direct-only", "rvas": ["0x6B725B0"],
         "text": "Kinetic.Impact.ExplosiveBlunt is added only on a projectile's direct-impact path, so entries 7, 117, "
                 "142 and 143 never apply to blast damage; entries 102–116 do."},
        {"id": "thrown-contact", "rvas": ["0x6CA8730"],
         "text": "Against a character, the explosive-actor path is the thrown object's contact damage (source "
                 "Kinetic.Impact.Throwable, DamageType.Impact), applied once per contact on the contacted bone."},
        {"id": "backblast-paths", "rvas": ["0x6F042A0", "0x6F06EB0"],
         "text": "On foot, 0x6F042A0 traces the back-blast cone. In a seat, 0x6F06EB0 hits the occupants of the shooter's "
                 "vehicle with synthetic hits, the shooter included. Only Launcher_04, RPG7 and CGM4 enable back-blast."},
    ]


def not_traced():
    return [
        {"id": "radial-amount",
         "text": "Blast damage: which DamageValues field is the starting amount, the falloff arithmetic, and which radius "
                 "separates Meta.Damage.Explosive.Radius.Inner from .Outer. GameMechanics §14 says BaseDamage and "
                 "ExplosiveRadius feed the Calibre rules and falloff is ExplosiveDamageFallOff, without a formula.",
         "data": "Projectile assets carry BaseDamage, ExplosiveRadius, EffectiveExplosiveRadius, ExplosiveDamageFallOff "
                 "and on some MinimumExplosiveDamage (values per source)."},
        {"id": "radial-split",
         "text": "Which of the character's components the radial gather hits. Known (" + R6 + "): one hit per component "
                 "after the IWDDamageable filter 0x6E6DCC0, each hit its own evaluation with its bone's hit location.",
         "data": "No data field describes the gather."},
        {"id": "radial-context",
         "text": "Which tags a blast hit's source context carries besides the source tag and the radius tag (weapon tag, "
                 "caliber id). The blast factors here use the projectile's source tag, its DamageEntityData.Context and "
                 "the radius tag, so the bone factor's W is 1 on blast hits.",
         "data": "Entries 108–116 need only the source tag and a radius tag."},
        {"id": "exploding-hit",
         "text": "When a projectile hit is bExploding. §7.6: an exploding hit skips both scales, the armor hook and "
                 "ModifyDamage on the projectile path; what sets bExploding is not stated, so whether an armed launcher, "
                 "shell or cannon round ever deals the direct-hit amount is open.",
         "data": "Projectile assets carry bHasArmingDelay and ArmingDelay (seconds of flight time, §7.6)."},
        {"id": "explosive-actors",
         "text": "Detonation damage of grenades, C4, mines, claymores, IEDs and the Molotov. Against a character "
                 "0x6CA8730 is only the thrown object's contact damage (" + R6 + "); the detonation's path, amount and "
                 "tags are not traced.",
         "data": "The items reference actor Blueprints (B_FragGrenade, B_ThrowableC4, B_AT_Mine, B_Claymore, B_Molotov) "
                 "that are not in the data export, so no damage value is in data/."},
        {"id": "armor-hook-paths",
         "text": "Whether the target hook Auth_GetArmorDamageEvent (§7.6) runs on paths other than the projectile's "
                 "direct impact (blast, back-blast, melee, actor impact, thrown contact). It decides whether an armor tag "
                 "reaches entries 102–106 and 138–144.",
         "data": "Armor items list CoveredHitLocations (see armor)."},
        {"id": "armor-data-rows",
         "text": "Whether DT_GlobalDamage_ArmorData's rows are evaluated for a character hit. §5's walk for a character "
                 "starts at Meta.Damage.Infantry and gives one group; the armor rows are keyed by armor tags.",
         "data": "DT_GlobalDamage_ArmorData has rows Meta.Damage.Armor, Meta.Damage.Helmet and the two Ghillie rows."},
        {"id": "vehicle-weapon-tag",
         "text": "Whether a vehicle weapon extension (WE_*) puts its DamageEntityData.Tag into the source context as a "
                 "weapon item does. §7.6 identifies the weapon tag by value for weapon items; the vehicle rows of "
                 "BoneDamageModifiers are only reached if it does.",
         "data": "Every WE_* file carries a Meta.Damage.Weapon.* tag (values per source)."},
        {"id": "underbarrel-weapon-tag",
         "text": "Which weapon tag an underbarrel grenade launcher shot carries.",
         "data": "GrenadeLauncher.json has no Meta.Damage.Weapon tag; its stats are DA_GrenadeLauncher_Stats."},
        {"id": "melee-path",
         "text": "The melee caller: §1.1 names no melee path, so the event's source (the item's Utility tag, whether "
                 "Meta.Damage.DamageType.Melee is added), its hit location and the armor hook are not traced.",
         "data": "Melee items carry WDItemExtensionData_CharacterMelee.MeleeActions[].Damage and DamageEntityData.Tag; "
                 "entry 144 requires Meta.Damage.DamageType.Melee; BoneDamageModifiers has a "
                 "Meta.Damage.DamageType.Melee row that no bone entry (5, 7, 10) selects for a melee-only source."},
        {"id": "impact-amount",
         "text": "The starting amount of actor impact (0x6E72D90, §1.1) and of a thrown object's contact (0x6CA8730), and "
                 "what the hitting actor's entity data holds.",
         "data": "No infantry rule entry requires Meta.Damage.DamageType.Impact or Kinetic.Impact.Throwable."},
        {"id": "backblast",
         "text": "Back-blast: the event's source tag and amount, and the hit location of the seated path's synthetic "
                 "hits. The two paths are known (" + R6 + ").",
         "data": "Launcher stats carry a BackBlast config (FWDBackBlastConfig) whose field names are hashed in the "
                 "export and the SDK; no infantry rule entry requires Meta.Damage.DamageType.BackBlast."},
        {"id": "occupant-damage",
         "text": "Damage to vehicle occupants from UWDVehicleOperatorComponent slots 160/161 (§1.1; VehicleDamagePipeline "
                 "§1): the amount and hit location.",
         "data": "Source tags Meta.Damage.Explosive.VehicleExplosion + DamageType.Explosive, and Meta.Damage.Vehicle + "
                 "DamageType.Enviroment."},
        {"id": "helmet-merge",
         "text": "The rule by which Mutable merges a helmet's physics asset into the character's. Known (" + R6 + "): each "
                 "helmet adds its single head body, which maps to Head. The model shows PA_TPCharacter_Simplified "
                 "without helmet bodies.",
         "data": "MUT_TP_Character lists five helmet physics assets (PA_Helmet_*), one Sphyl body on head each "
                 f"({MODEL} asset.extras.notes; MUT_TP_Character is not in the data/ JSON export)."},
        {"id": "tapered-capsule-query",
         "text": "Whether Chaos builds query shapes from tapered-capsule bodies, i.e. whether these six bodies can be hit "
                 "by a trace at all.",
         "data": "calf_l, calf_r, lowerarm_l, lowerarm_r, thigh_l and thigh_r are TaperedCapsule bodies "
                 f"(QueryAndPhysics) in PA_TPCharacter_Simplified ({MODEL} asset.extras.bodies[].shapes)."},
        {"id": "collision-channels",
         "text": "Which trace channels hit the character's bodies. The CharacterMesh component uses collision profile "
                 "Custom, whose per-channel responses are native class defaults, not stored in the cooked Blueprint.",
         "data": "CharacterMesh.BodyInstance.CollisionEnabled is QueryOnly (profile Custom); every body is "
                 f"QueryAndPhysics with BodyCollision_Enabled ({MODEL} asset.extras.notes and node extras)."},
        {"id": "physical-material",
         "text": "Data only, no documented use: no doc uses a body's physical material or surface type for infantry "
                 "damage (VFX uses physical materials for impact effects; VehicleDamagePipeline §3.2 says vehicle hits "
                 "read neither physical materials nor bone names).",
         "data": f"The head body uses PM_Head, the other 19 bodies PM_Body ({MODEL} asset.extras.bodies[].phys_material; "
                 "the body export gives SurfaceType17 and SurfaceType3; the PM_* assets are not in the data/ JSON export)."},
        {"id": "caliber-parent-match",
         "text": "Whether a weapon whose SupportedCaliber is a parent tag fires the child projectiles: the bow lists "
                 "Item.Caliber.Arrow (child Arrow.Explosive), the M500 / MP43 Item.Caliber.12g (child 12g.RifledSlug), "
                 "the artillery Item.Caliber.155mm (155mm.Standard, .Expensive), STN_03 Item.Caliber.120x800mm "
                 "(120x800mm.Standard), CGM4 Item.Caliber.84mm (child 84mm.TVGuided). How SupportedCaliber is matched "
                 "is not traced.",
         "data": "No WDProjectileData asset has ProjectileId Item.Caliber.12g, .155mm or .120x800mm; the child ids "
                 "each have one (Sandbox copies left out)."},
    ]


# --- sources ------------------------------------------------------------------------------------
#
# Compact encoding. Zone lists follow hit_locations order. A source's zone_multiplier {"row": R} means
# B[z] = Universal[z] x bone_rows[R][z] (R null: Universal[z] alone); null means B[z] = 1. A factor {"k": k}
# means factor[z] = k x B[z]; {"zones": [...]} lists the 12 factors. Damage = S x factor. An armor item's
# {"k": k} multiplies the unarmored factor on the hit locations the item covers. File references are
# [index into meta.files, field].

FILES = []


def ref(path, field=None):
    if not path:
        return None
    if path not in FILES:
        FILES.append(path)
    return [FILES.index(path), field] if field else FILES.index(path)


def same(xs):
    return all(abs(x - xs[0]) <= 1e-12 * max(1.0, abs(xs[0])) for x in xs)


def bone_vector(src, context, sel):
    """(B per hit location, zone_multiplier) for an event whose selected entries are `sel` (§7.1)."""
    if not sel & set(BONE_ENTRIES) or src == DRONE:
        return [1.0] * len(ZONES), None
    row = bone_row(context)
    return ([dt.BONE["Universal"][z] * (dt.BONE[row][z] if row else 1.0) for z in ZONES], {"row": row})


def encode_zones(src, context, armored=True):
    """Factors of one event on every hit location, and per armor piece on the locations it covers (the covering
    piece alone reaches the rules, §7.6), in the compact encoding. Also returns the full-precision factors."""
    fs, applied, sel = [], [], set()
    for z in ZONES:
        s_, f = selected(src, context, z)
        fs.append(f)
        applied.append({i for i, x in s_ if x != 1.0 or i in BONE_ENTRIES})
        sel.update(i for i, _ in s_)
    b, zm = bone_vector(src, context, sel)
    ks = [f / x for f, x in zip(fs, b)]
    enc = {"factor": {"k": ks[0]} if same(ks) else {"zones": fs}}
    common = set.intersection(*applied)
    enc["entries"] = sorted(common)
    extra = {short(z): sorted(a - common) for z, a in zip(ZONES, applied) if a - common}
    if extra:
        enc["zone_entries"] = extra
    armor, aused = {}, set()
    for a in ARMOR_ITEMS if armored else []:
        idx = [ZONES.index(z) for z in a["covers"]]
        if not idx:
            continue
        fa, ea = [], set()
        for i in idx:
            s_, f = selected(src, context, ZONES[i], [a["tag"]])
            fa.append(f)
            ea.update(j for j, x in s_ if x != 1.0 and j not in applied[i])
            aused.update(j for j, _ in s_ if dt.ENTRIES[j]["TargetRequirements"])
        ka = [x / fs[i] if fs[i] else 0.0 for x, i in zip(fa, idx)]
        if same(ka) and ka[0] == 1.0 and not ea:
            continue
        armor[a["item"]] = dict({"k": ka[0]} if same(ka) else {"zones": {short(ZONES[i]): x for x, i in zip(fa, idx)}},
                                entries=sorted(ea))
    if armor:
        enc["armor"] = armor
    return enc, zm, sel, aused, fs


def decode(enc, zm, bone_rows):
    """The 12 factors of an encoded event (the page's arithmetic)."""
    if "zones" in enc["factor"]:
        return list(enc["factor"]["zones"])
    u = bone_rows["Universal"]
    b = [u[z] * (bone_rows[zm["row"]][z] if zm["row"] else 1.0) for z in ZONES] if zm else [1.0] * len(ZONES)
    return [enc["factor"]["k"] * x for x in b]


def projectile_source(w, cal, category, label, sub, nt_extra=()):
    proj = PROJ[cal]
    src, vals = proj["source_tag"], proj["values"]
    blunt = [BLUNT] if proj["has_arming_delay"] else []  # §7.6: direct-impact path only (blunt-direct-only)
    ctx = proj["context"] + ([w["wtag"]] if w["wtag"] else []) + [cal, PROJECTILE] + blunt
    explosive = vals.get("ExplosiveRadius", 0) > 0  # an absent ExplosiveRadius is the class default 0: no blast
    cases = []
    if proj["has_arming_delay"] and "ExplosiveBluntDamage" in vals:
        cases.append(("before_arming", "Before arming (flight time below ArmingDelay): S = ExplosiveBluntDamage",
                      "ExplosiveBluntDamage"))
    cases.append(("direct_not_exploding", "Direct hit that is not exploding: S = BaseDamage (when a hit explodes is "
                  "not traced)", "BaseDamage") if explosive or proj["has_arming_delay"]
                 else ("direct", "Direct hit: S = BaseDamage", "BaseDamage"))
    enc, zm, sel, aused, fs = encode_zones(src, ctx)  # S does not enter the factors, so the cases share them
    direct = [{"case": cid, "S": vals.get(field), "S_src": ref(proj["path"], f"ProjectileStats.DamageValues.{field}")}
              for cid, text, field in cases]
    falloff = {"src": ref(w["stats"], "DistanceDamageFalloffCurve") if w["keys"] else None,
               "keys_m": [[t / 100, v] for t, v in sorted((k["Time"], k["Value"]) for k in w["keys"])],
               "cubic": any(k.get("InterpMode") != "RCIM_Linear" for k in w["keys"])}
    radial, rsel, rzm = None, set(), None
    nt = list(nt_extra)
    if explosive:
        rings = {}
        for name, rtag in (("inner", INNER), ("outer", OUTER)):
            r_enc, r_zm, r_sel, r_aused, _ = encode_zones(src, proj["context"] + [rtag])
            rsel |= r_sel | r_aused
            rzm = r_zm
            rings[name] = dict(tag=rtag, **r_enc)
        radial = {"zone_multiplier": rzm, "rings": rings}
        nt += ["radial-amount", "radial-split", "radial-context", "exploding-hit", "armor-hook-paths"]
    if proj["has_arming_delay"] and "exploding-hit" not in nt:
        nt.append("exploding-hit")
    kind = "Bullet" if src.startswith("Meta.Damage.Bullet") else "Cannon" if src.startswith("Meta.Damage.Cannon") else "ExplosiveBlunt"
    if zm is not None:
        row = zm["row"]
        why = (f"Entry {next(i for i in BONE_ENTRIES if i in sel)} selects the bone operation for a direct hit ({kind}), "
               f"so the hit location sets the factor Universal × {'row ' + row if row else 'W = 1 (no row matches)'} (§7.1).")
    elif src == DRONE:
        why = "Entry 7 matches the blunt hit, but §7.1 exempts the source tag Meta.Damage.Explosive.Drone: the bone factor is 1 everywhere."
    else:
        why = ("No bone entry matches a direct hit: entries 5, 7 and 10 need Meta.Damage.Bullet, Kinetic.Impact.ExplosiveBlunt "
               "or Meta.Damage.Cannon in the source (§3.1), so every hit location gets the same rule factor.")
    if radial:
        why += (" Blast hits carry the hit bone's location but never ExplosiveBlunt, so entries 7, 117, 142 and 143 do not "
                "apply to them (" + R6 + ")" + (f"; entry {next(i for i in (5, 10) if i in rsel)} still gives the bone "
                                                "factor, with W = 1." if rzm else "."))
    sid = re.sub(r"[^a-z0-9]+", "-", f"{category}-{label}".lower()).strip("-")
    return {"id": sid, "category": category, "group": sub, "label": label,
            "damage_tags": sorted({src} | set(blunt)),
            "uses_hit_location": zm is not None, "radial_uses_hit_location": rzm is not None if radial else None,
            "why": why,
            "rule_entries": sorted(i for i in sel if not dt.ENTRIES[i]["TargetRequirements"]),
            "armor_entries": sorted(aused),
            "radial_entries": sorted(rsel) if radial else [],
            "zone_multiplier": zm,
            "values": {"weapon": ref(w["path"]), "weapon_tag": w["wtag"], "stats": ref(w["stats"]), "caliber": cal,
                       "projectile": ref(proj["path"]), "source_tag": src, "source_context": proj["context"],
                       "has_arming_delay": proj["has_arming_delay"], "arming_delay": proj["arming_delay"],
                       "damage_values": vals, "damage_values_src": ref(proj["path"], "ProjectileStats.DamageValues"),
                       "direct": direct, "direct_zones": enc, "falloff": falloff, "radial": radial},
            "not_traced": sorted(set(nt)), "doc": "bullet_event", "_fs": fs}


def tagged_source(sid, category, group, label, tags, why, values, nt, docref, extra=(), uses_hit=False):
    hostile, armor, friendly = candidates(tags, extra)
    return {"id": sid, "category": category, "group": group, "label": label, "damage_tags": list(tags),
            "uses_hit_location": uses_hit, "why": why, "rule_entries": hostile, "armor_entries": armor,
            "friendly_entries": friendly, "zone_multiplier": None,
            "values": values, "not_traced": nt, "doc": docref}


def child_calibers(w):
    """Projectile ids under a supported caliber tag that the weapon does not list exactly (12g -> 12g.RifledSlug,
    155mm -> 155mm.Standard). Sandbox copies are left out."""
    exact = set(w["cals"])
    return [pid for pid in sorted(PROJ) if pid not in exact and "Sandbox" not in pid
            and any(pid.startswith(c + ".") for c in w["cals"])]


def sources():
    out = []
    inf = infantry_weapons()
    for w in sorted(inf, key=lambda w: (w["wtag"], w["name"])):
        cal = next((c for c in w["cals"] if c in PROJ), None)  # the §7.7 choice: first supported caliber with data
        if cal and (PROJ[cal]["source_tag"] or "").startswith("Meta.Damage.Bullet"):
            s = projectile_source(w, cal, "bullets", w["name"], w["wtag"].split(".")[3])
            s["in_doc_table"] = True
            out.append(s)
        elif cal:
            out.append(projectile_source(w, cal, "explosives", w["name"], "Launcher"))
        for child in child_calibers(w):
            cat = "bullets" if (PROJ[child]["source_tag"] or "").startswith("Meta.Damage.Bullet") \
                and not PROJ[child]["values"].get("ExplosiveRadius", 0) > 0 else "explosives"
            out.append(projectile_source(w, child, cat, f"{w['name']} ({child.replace('Item.Caliber.', '')})",
                                         w["wtag"].split(".")[3], ["caliber-parent-match"]))
    seen, oth = {}, other_weapons()
    for w in oth:
        for cal in [c for c in w["cals"] if c in PROJ][:1] + child_calibers(w):
            seen.setdefault((w["wtag"], cal, w["stats"]), []).append(w)
    for (wtag, cal, _), ws in sorted(seen.items(), key=lambda kv: (kv[0][1], kv[0][0] or "")):
        w = ws[0]
        names = [x["name"].replace("WE_", "").replace("ID_", "") for x in ws]
        src = PROJ[cal]["source_tag"] or ""
        nt = ["vehicle-weapon-tag"] if "/Vehicles/" in w["path"] else []
        if not wtag:
            nt.append("underbarrel-weapon-tag")
        if cal not in w["cals"]:
            nt.append("caliber-parent-match")
        label = names[0].replace("_", " ") + f" ({cal.replace('Item.Caliber.', '')})" \
            + (f" +{len(names) - 1} more" if len(names) > 1 else "")
        bow = wtag == "Meta.Damage.Weapon.CombatBow"
        if src.startswith("Meta.Damage.Bullet") and not PROJ[cal]["values"].get("ExplosiveRadius", 0) > 0:
            s = projectile_source(w, cal, "bullets", label, "Bow" if bow else "Vehicle", nt)
        else:
            sub = "Cannon" if src.startswith("Meta.Damage.Cannon") else "Bow" if bow else \
                "Launcher" if "underbarrel-weapon-tag" in nt else "Vehicle"
            s = projectile_source(w, cal, "explosives", label, sub, nt)
        s["values"]["items"] = [ref(x["path"]) for x in ws]
        out.append(s)
    # Thrown and placed explosives: their detonation is not traced and their values are not in the export.
    actors = [("M67 frag grenade", "Wardogs/Content/Items/Throwable/Grenades/M67_Grenade/ID_M67Grenade.json", "Meta.Damage.Explosive.Grenade"),
              ("C4", "Wardogs/Plugins/GameFeatures/Items/C4/Content/Data/ID_C4_Trigger.json", "Meta.Damage.Explosive.Utility.C4"),
              ("AT mine", "Wardogs/Plugins/GameFeatures/Items/AT_mine/Content/Data/ID_AT_Mine.json", "Meta.Damage.Explosive.Utility.ATMine"),
              ("Claymore", "Wardogs/Plugins/GameFeatures/Items/Claymore/Content/Data/ID_Claymore.json", "Meta.Damage.Explosive.Utility.Claymore"),
              ("IED", "Wardogs/Plugins/GameFeatures/Items/IED/Content/Data/ID_IED_Explosive.json", "Meta.Damage.Explosive.Utility.IED"),
              ("Molotov", "Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/ID_Molotov.json", "Meta.Damage.Explosive.Utility.Molotov")]
    for label, path, t in actors:
        kind, cls = actor_class(os.path.join(DATA, path))
        values = {"item": ref(data_path(path)), "actor_class_field": kind, "actor_class": cls, "actor_class_in_data": False,
                  "tag": t, "tag_in_DefaultGameplayTags": tag_defined(t),
                  "entries_naming_tag": [i for i, e in enumerate(dt.ENTRIES) if t in e["SourceRequirements"]],
                  "tag_note": "the gameplay tag named after this item; which tags the detonation carries is not traced",
                  "ring_entries": {"inner": candidates([t], [INNER])[0], "outer": candidates([t], [OUTER])[0]}}
        out.append(tagged_source(re.sub(r"[^a-z0-9]+", "-", f"explosives-{label}".lower()).strip("-"), "explosives",
                                 "Thrown and placed", label, [t],
                                 "The detonation is not traced: no amount, tags or path (0x6CA8730 against a character is "
                                 "only the thrown object's contact, see Thrown object contact). The entries listed are "
                                 "those whose source requirements this tag meets.",
                                 values, ["explosive-actors", "armor-hook-paths"], "callers", [INNER, OUTER]))
    for w in sorted(inf + oth, key=lambda w: w["name"]):
        if w["backblast"] is not None:
            out.append(tagged_source(re.sub(r"[^a-z0-9]+", "-", f"explosives-backblast-{w['name']}".lower()), "explosives",
                                     "Back-blast", f"{w['name']} back-blast", ["Meta.Damage.DamageType.BackBlast"],
                                     "On foot the back-blast traces a cone (0x6F042A0); in a seat it hits the occupants of "
                                     "the shooter's vehicle, the shooter included, with synthetic hits (0x6F06EB0) (" + R6 +
                                     "). No infantry rule entry requires Meta.Damage.DamageType.BackBlast; the source tag "
                                     "and amount are not traced.",
                                     {"weapon": ref(w["path"]), "config": ref(w["stats"], "BackBlast"),
                                      "enabled": bool(w["backblast"].get("bEnabled")),
                                      "on_foot": "0x6F042A0: cone trace", "seated": "0x6F06EB0: synthetic hits on the "
                                      "occupants of the shooter's vehicle, shooter included",
                                      "field_names": "hashed in the export and the SDK (FWDBackBlastConfig)"},
                                     ["backblast", "armor-hook-paths"], "callers"))
    out.append(tagged_source("explosives-vehicle-explosion-occupants", "explosives", "Vehicle", "Vehicle explosion (occupants)",
                             ["Meta.Damage.Explosive.VehicleExplosion", "Meta.Damage.DamageType.Explosive"],
                             "Built by UWDVehicleOperatorComponent (§1.1, VehicleDamagePipeline §1); amount and hit location "
                             "are not traced. No bone entry matches these tags.",
                             {"caller": "UWDVehicleOperatorComponent slots 160/161 (0x7692B60, 0x768ED20)"},
                             ["occupant-damage", "armor-hook-paths"], "callers"))
    for m in melee_items():
        out.append(tagged_source(re.sub(r"[^a-z0-9]+", "-", f"other-melee-{m['item']}".lower()), "other", "Melee",
                                 m["item"].replace("ID_", ""), [m["tag"], "Meta.Damage.DamageType.Melee"],
                                 "No bone entry matches a melee source (entries 5, 7, 10 need Bullet, ExplosiveBlunt or Cannon, "
                                 "§3.1), so the body takes the same factor everywhere. Entry 144 applies armor durability "
                                 "(1 − R/100, §7.5) to an armored target if the DamageType.Melee tag and the armor tag reach "
                                 "the event, which is not traced.",
                                 {"item": ref(m["path"]),
                                  "actions": [{"action": a["action"], "damage": a["damage"],
                                               "src": ref(m["path"], f"WDItemExtensionData_CharacterMelee.MeleeActions[{a['action']}].Damage")}
                                              for a in m["actions"]],
                                  "armor_factor_entry_144": {a["item"]: 1 - a["reduction_pct"] / 100
                                                             for a in ARMOR_ITEMS if a["kind"] == "armor" and a["covers"]}},
                                 ["melee-path", "armor-hook-paths"], "armor_durability"))
    out.append(tagged_source("other-thrown-contact", "other", "Impact", "Thrown object contact",
                             ["Meta.Damage.Kinetic.Impact.Throwable", "Meta.Damage.DamageType.Impact"],
                             "0x6CA8730 against a character is the thrown object's contact damage, applied once per contact on "
                             "the contacted bone (" + R6 + "). No infantry entry requires these tags, so the hit location "
                             "changes no factor. The amount is not traced.",
                             {"caller": "0x6CA8730 (AWDExplosive, AWDC4, AWDGrenade, AWDLandmine slot 236)"},
                             ["impact-amount", "armor-hook-paths"], "callers"))
    out.append(tagged_source("other-actor-impact", "other", "Impact", "Actor or vehicle impact",
                             ["Meta.Damage.DamageType.Impact"],
                             "0x6E72D90 (§1.1) builds the event from the hitting actor's entity data plus DamageType.Impact; "
                             "no infantry entry requires Impact, so nothing depends on the hit location. The amount is not traced.",
                             {"caller": "0x6E72D90 (AWDMoverCharacter slot 169 delegate); skips dead characters"},
                             ["impact-amount", "armor-hook-paths"], "callers"))
    order = {"bullets": 0, "explosives": 1, "other": 2}
    return sorted(out, key=lambda x: order[x["category"]])


# --- model --------------------------------------------------------------------------------------

def glb_json(path):
    """The GLB's JSON chunk alone, as damage_tables.glb_summary reads it: no buffer decoding."""
    with open(path, "rb") as f:
        f.seek(12)
        size, kind = struct.unpack("<II", f.read(8))
        return json.loads(f.read(size)) if kind == 0x4E4F534A else {}


def node_centres(gltf):
    """Node name -> world-space bounding-box centre [x, y, z] (metres, glTF axes) of the node's own mesh, the way
    damage_tables.glb_summary computes slot centres: POSITION accessor min/max (normalized quantized values
    scaled back) through the composed node TRS. meshopt quantization folds a scale and offset into each node,
    so node transforms alone are not bone frames."""
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

    out = {}

    def visit(i, parent):
        n = gltf["nodes"][i]
        world = mul(parent, local(n))
        box = [[float("inf")] * 3, [float("-inf")] * 3]
        for p in gltf["meshes"][n["mesh"]]["primitives"] if "mesh" in n else []:
            if "POSITION" not in p["attributes"]:
                continue
            acc = gltf["accessors"][p["attributes"]["POSITION"]]
            d = norm.get(acc["componentType"]) if acc.get("normalized") else None
            lo, hi = ([max(v / d, -1.0) if d else v for v in acc[k]] for k in ("min", "max"))
            for corner in ([(lo, hi)[(c >> a) & 1][a] for a in range(3)] for c in range(8)):
                pt = [sum(world[r][k] * (corner + [1])[k] for k in range(4)) for r in range(3)]
                box[0] = [min(a, b) for a, b in zip(box[0], pt)]
                box[1] = [max(a, b) for a, b in zip(box[1], pt)]
        if "mesh" in n:
            out[n.get("name")] = [round((a + b) / 2, 4) for a, b in zip(*box)]
        for c in n.get("children", []):
            visit(c, world)

    identity = [[float(r == c) for c in range(4)] for r in range(4)]
    for i in gltf.get("scenes", [{}])[gltf.get("scene", 0)].get("nodes", []):
        visit(i, identity)
    return out


def model():
    path = os.path.join(ROOT, MODEL)
    if not os.path.exists(path):
        return None
    gltf = glb_json(path)
    extras = gltf.get("asset", {}).get("extras", {})
    bodies = extras.get("bodies") or [{"bone": n.get("name")} for n in gltf.get("nodes", []) if "mesh" in n]
    names = [b["bone"] for b in bodies]
    centres = node_centres(gltf)
    return {"path": MODEL, "physics_asset": extras.get("physics_asset"), "skeletal_mesh": extras.get("skeletal_mesh"),
            "bodies": names, "body_count": len(names),
            "body_shapes": {b["bone"]: b.get("shapes") for b in bodies if "shapes" in b},
            "phys_materials": {b["bone"]: b.get("phys_material") for b in bodies if "phys_material" in b},
            "centres": {b: centres.get(b) for b in names},
            "centres_note": "world-space bounding-box centre of each body's mesh, metres, glTF axes (+Y up, facing +Z, "
                            "origin at the feet), from accessor min/max through the composed node transforms",
            "notes": extras.get("notes", []),
            "images": len(gltf.get("images", [])), "textures": len(gltf.get("textures", []))}


# --- JSON ---------------------------------------------------------------------------------------

def build():
    """The viewer JSON at full precision (write_json rounds when serialising; --check reads this)."""
    FILES.clear()
    bones, remap = hit_map()
    mdl = model()
    bodies = set(mdl["bodies"]) if mdl else set()
    names = list(bones) + sorted(b for b in bodies if b not in bones)
    if mdl:
        mdl["mapped_without_body"] = [b for b in bones if b not in bodies]
        mdl["bodies_without_mapping"] = [b for b in mdl["bodies"] if b not in bones]
    tree = subprocess.run(["git", "rev-parse", "HEAD:data"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    srcs = sources()
    armor = [{k: a[k] for k in ("item", "tag", "kind", "covers", "max_durability", "reduction_pct", "stage_reductions",
                                "entries", "custom_entries", "path")} for a in ARMOR_ITEMS]
    used_entries = sorted({i for s in srcs for i in s["rule_entries"] + s["armor_entries"] + s.get("radial_entries", [])
                           + s.get("friendly_entries", [])} | {i for a in ARMOR_ITEMS for i in a["entries"]})
    return {
        "meta": {
            "source_data_tree": tree,
            "source_data_tree_note": "git tree id of data/ when generated; equals `git rev-parse <commit>:data` for any commit with the same data",
            "generator": "python _tools/infantry_tables.py --json",
            "encoding": "Zone lists follow hit_locations order. zone_multiplier {row: R}: B[z] = bone_rows.Universal[z] × "
                        "bone_rows[R][z] (R null: Universal alone); zone_multiplier null: B[z] = 1. A factor {k} gives "
                        "factor[z] = k × B[z]; {zones} lists the 12 factors. Damage = S × factor[z] (× the falloff curve "
                        "at the distance, keys in metres). Armor {k} multiplies the unarmored factor on the hit locations the "
                        "item covers; {zones} gives those factors. entries are the entries with a factor other than 1 on "
                        "every hit location, zone_entries the extra ones per hit location. A file reference is "
                        "[index into meta.files, field] or an index. A source's doc is a key of meta.docs and a direct case's "
                        "case a key of meta.cases. A direct hit's source context is source_context, weapon_tag, caliber, "
                        "Meta.Damage.DamageType.Projectile and, when has_arming_delay, Kinetic.Impact.ExplosiveBlunt (§7.6); "
                        "a blast hit's is source_context and the ring's radius tag. Blast armor factors apply only if the "
                        "armor tag reaches a blast hit (armor-hook-paths). Numbers are rounded to 6 significant digits.",
            "files": FILES,
            "cases": {"direct": "Direct hit: S = BaseDamage",
                      "direct_not_exploding": "Direct hit that is not exploding: S = BaseDamage (when a hit explodes "
                                              "is not traced)",
                      "before_arming": "Before arming (flight time below ArmingDelay): S = ExplosiveBluntDamage"},
            "docs": {k: doc(k) for k in DOCS},
            "verified": {"status": R6, "items": verified()},
            "assumptions": [
                "rules from DamagePipeline §4-§7 only, through _tools/damage_tables.py: every selected entry multiplies "
                "the running amount, the total is clamped at 0 (§6)",
                "§7.7 event: hostile alignment, FMJ (no ammo-modifier tag), a direct hit with no ricochet or penetration, "
                "no instigator tags, target outside any vehicle; point blank unless the falloff curve is applied",
                "speed scale left at 1 (§7.8)",
                "armor: only the piece whose CoveredHitLocations holds the hit location reaches the rules "
                "(Auth_GetArmorDamageEvent, §7.6); every durability stage has the same R in the data (§7.5)",
                "an absent cooked property is its class default (bHasArmingDelay false)",
                "bone factor U × W: U from row Universal, W from the first source-context tag naming a row or its "
                "direct parent, 1.0 with none (§7.1); Meta.Damage.Explosive.Drone is exempt",
                "blast hits: one evaluation per hit with that hit's bone as the hit location and no ExplosiveBlunt (" + R6 +
                "); source context = the projectile's source tag, DamageEntityData.Context and the radius tag "
                "(radial-context), so W = 1; the blast amount itself is not traced (radial-amount)",
                "shotgun values are per pellet"],
            "not_traced": not_traced(),
            "categories": [
                {"id": "bullets", "label": "Bullets",
                 "note": "One event per hit from the projectile data and the firing weapon (§7.6): S = BaseDamage × speed "
                         "scale × distance curve. Entry 5 multiplies by Universal × weapon row for the hit location (§7.1); "
                         "a covering helmet or armor piece adds entries 138/140 (§7.3)."},
                {"id": "explosives", "label": "Explosives and launchers",
                 "note": "A direct impact goes through the projectile path: before arming S is ExplosiveBluntDamage and the "
                         "source carries Kinetic.Impact.ExplosiveBlunt, so entry 7 applies the bone factor and entries "
                         "142–143 armor durability; cannon rounds take entry 10. An exploding hit skips ModifyDamage there "
                         "(§7.6). The blast goes through the radial path: one evaluation per hit component, tagged "
                         "Radius.Inner or .Outer, with the hit bone's location and without ExplosiveBlunt, so entries 7, "
                         "117, 142 and 143 never apply to it and 102–116 do (" + R6 + "). The blast amount and falloff are "
                         "not traced. Grenades, C4 and mines detonate through a path that is not traced."},
                {"id": "other", "label": "Other",
                 "note": "Melee, actor impact and thrown-object contact match no bone entry (5, 7, 10 need Bullet, "
                         "ExplosiveBlunt or Cannon, §3.1), so the factor is the same on every hit location. Entry 144 "
                         "reduces melee damage on an armored target by R (§7.5)."}],
            "entries": {str(i): entry_note(i) for i in used_entries},
        },
        "model": mdl,
        "hit_locations": [{"tag": z, "short": z[len(HIT):], "label": LABELS[z[len(HIT):]],
                           "universal": dt.BONE["Universal"][z],
                           "bones": [b for b, t in bones.items() if t == z],
                           "covered_by": [a["item"] for a in ARMOR_ITEMS if z in a["covers"]]} for z in ZONES],
        "bones": [{"bone": b, "hit_location": bones.get(b), "impact_remap": remap.get(b),
                   "has_body": (b in bodies) if mdl else None} for b in names],
        "bone_rule": {"data": f"DamageHitLocations maps {len(bones)} bone names to tags",
                      "runtime": "exact FName match of FHitResult.BoneName in the asset picked by the actor's class; no "
                                 "parent walk; an unmapped bone gives no hit location (0x6F01BB0, 0x6BB8D00; " + R6 + ")",
                      "unmapped": "with no hit location, entries with a hit-location filter are not selected (§4 rule 4) "
                                  "and all armor tags are removed (§7.6)",
                      "impact_remap": "DamageImpactRemap (" + ", ".join(f"{a} → {b}" for a, b in remap.items()) +
                                      ") is used by animation and ragdoll only, never for damage (0x6BB8D40; " + R6 + ")",
                      "live_player": "spine_01 and spine_02 have no body in PA_TPCharacter_Simplified, so a live player "
                                     "never produces them; a helmet adds its own head body, which maps to Head (" + R6 + ")",
                      "path": data_path(HITLOC_FILE)},
        "bone_rows": {k: dict(v) for k, v in dt.BONE.items()},
        "bone_rows_path": data_path(BONE_FILE),
        "rule_table_path": data_path(RULE_FILE),
        "sources": srcs,
        "armor": armor,
    }


def sig(o):
    """Round every float to 6 significant digits and drop private (_) keys, for serialising only."""
    if isinstance(o, float):
        return float(f"{o:.6g}")
    if isinstance(o, dict):
        return {k: sig(v) for k, v in o.items() if not k.startswith("_")}
    if isinstance(o, list):
        return [sig(v) for v in o]
    return o


def dumps(o, level=0):
    """Indented JSON with lists of scalars and small flat objects kept on one line."""
    flat = json.dumps(o, ensure_ascii=False, separators=(", ", ": "))
    scalar = lambda v: not isinstance(v, (dict, list))
    if scalar(o) or not o:
        return flat
    vals = list(o.values()) if isinstance(o, dict) else o
    simple = all(scalar(v) or (isinstance(v, list) and all(scalar(x) for x in v)) for v in vals)
    if simple and (isinstance(o, list) or len(flat) <= 700):
        return flat
    if isinstance(o, list) and all(isinstance(v, list) and all(scalar(x) for x in v) for v in o) and len(flat) <= 100:
        return flat
    pad, inner = " " * level, " " * (level + 1)
    if isinstance(o, dict):
        body = (f"{inner}{json.dumps(k, ensure_ascii=False)}: {dumps(v, level + 1)}" for k, v in o.items())
        return "{\n" + ",\n".join(body) + "\n" + pad + "}"
    return "[\n" + ",\n".join(inner + dumps(v, level + 1) for v in o) + "\n" + pad + "]"


def write_json():
    out = build()
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    with open(JSON_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps(sig(out)) + "\n")
    cats = {}
    for s in out["sources"]:
        cats[s["category"]] = cats.get(s["category"], 0) + 1
    print(f"{rel(JSON_OUT)}: {os.path.getsize(JSON_OUT) / 1024:.0f} KiB, {len(out['hit_locations'])} hit locations, "
          f"{len(out['bones'])} bones, {len(out['sources'])} sources ({', '.join(f'{k} {v}' for k, v in cats.items())}), "
          f"{len(out['armor'])} armor items, {len(out['meta']['not_traced'])} not traced, model {'yes' if out['model'] else 'none'}")
    return out


# --- tables -------------------------------------------------------------------------------------

def short(z):
    return z[len(HIT):] if z and z.startswith(HIT) else z


def zones_table():
    bones, _ = hit_map()
    print("| Hit location (`Meta.Damage.HitLocation.Infantry.*`) | Bones | `Universal` | Covered by |")
    print("|---|---|---:|---|")
    for z in ZONES:
        bs = ", ".join(f"`{b}`" for b, t in bones.items() if t == z)
        cov = ", ".join(a["item"].replace("ID_", "") for a in ARMOR_ITEMS if z in a["covers"]) or "—"
        print(f"| `{short(z)}` | {bs} | {dt.BONE['Universal'][z]:g} | {cov} |")


def bones_table():
    out = build()
    print("| Bone | Hit location | `DamageImpactRemap` (animation and ragdoll only) | Physics body |")
    print("|---|---|---|---|")
    for b in out["bones"]:
        body = "—" if b["has_body"] is None else ("yes" if b["has_body"] else "**no**")
        print(f"| `{b['bone']}` | {('`' + short(b['hit_location']) + '`') if b['hit_location'] else '**none**'} | "
              f"{('`' + b['impact_remap'] + '`') if b['impact_remap'] else '—'} | {body} |")


def multipliers_table():
    print("| Row (`Meta.Damage.` omitted) | " + " | ".join(short(z) for z in ZONES) + " |")
    print("|---|" + "---:|" * len(ZONES))
    u = dt.BONE["Universal"]
    for k, row in dt.BONE.items():
        cells = [f"{u[z]:.3g}" if k == "Universal" else f"{u[z] * row[z]:.3g}" for z in ZONES]
        print(f"| `{k.replace('Meta.Damage.', '')}` | " + " | ".join(cells) + " |")


def zm_text(zm):
    if zm is None:
        return "no"
    return f"yes (`{zm['row'].replace('Meta.Damage.', '')}` row)" if zm["row"] else "yes (W = 1)"


def sources_table():
    out = build()
    cat = {c["id"]: c["label"] for c in out["meta"]["categories"]}
    print("| Category | Source | Damage tags | Hit location matters (direct) | Rule entries | Armor entries | "
          "Blast entries | Not traced |")
    print("|---|---|---|---|---|---|---|---|")
    for s in out["sources"]:
        tags = ", ".join(f"`{t.replace('Meta.Damage.', '')}`" for t in s["damage_tags"])
        print(f"| {cat[s['category']]} | {s['label']} | {tags} | {zm_text(s['zone_multiplier'])} | "
              f"{', '.join(map(str, s['rule_entries'])) or '—'} | {', '.join(map(str, s['armor_entries'])) or '—'} | "
              f"{', '.join(map(str, s.get('radial_entries', []))) or '—'} | {', '.join(s['not_traced']) or '—'} |")


def explosives_table():
    out = build()
    print("| Source | Projectile | Source tag | Blunt S (before arming) | Direct S | Arming delay (s) | `ExplosiveRadius` | "
          "`EffectiveExplosiveRadius` | `ExplosiveDamageFallOff` | `MinimumExplosiveDamage` | Blast bone factor | "
          "Inner: factor (entries) | Outer: factor (entries) |")
    print("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|")
    for s in out["sources"]:
        v = s["values"]
        if s["category"] != "explosives" or "direct" not in v:
            continue
        cases = {c["case"]: c["S"] for c in v["direct"]}
        r = v["radial"] or {"rings": {}, "zone_multiplier": None}
        f = lambda k: f"{v['damage_values'][k]:g}" if k in v["damage_values"] else "—"

        def ring(k):
            if k not in r["rings"]:
                return "—"
            g = r["rings"][k]
            fac = f"×{g['factor']['k']:.3g}" if "k" in g["factor"] else "per hit location"
            return f"{fac} ({', '.join(map(str, g['entries'])) or '—'})"

        blunt = cases.get("before_arming")
        print(f"| {s['label']} | `{v['caliber'].replace('Item.Caliber.', '')}` | `{v['source_tag'].replace('Meta.Damage.', '')}` | "
              f"{'—' if blunt is None else f'{blunt:g}'} | {cases.get('direct_not_exploding', cases.get('direct')):g} | "
              f"{v['arming_delay'] if v['has_arming_delay'] else '—'} | {f('ExplosiveRadius')} | {f('EffectiveExplosiveRadius')} | "
              f"{f('ExplosiveDamageFallOff')} | {f('MinimumExplosiveDamage')} | "
              f"{zm_text(r['zone_multiplier']) if v['radial'] else '—'} | {ring('inner')} | {ring('outer')} |")


def armor_table():
    print("| Item | Context tag | Kind | Max durability | `R` (%) | Covered hit locations | Entries (custom in bold) |")
    print("|---|---|---|---:|---:|---|---|")
    for a in ARMOR_ITEMS:
        ent = ", ".join(f"**{i}**" if i in a["custom_entries"] else str(i) for i in a["entries"])
        print(f"| `{a['item']}` | `{a['tag']}` | {a['kind']} | {format(a['max_durability'], 'g') if a['max_durability'] is not None else '—'} | "
              f"{a['reduction_pct']:g}{'' if a['stage_reductions'] else ' (no stages)'} | "
              f"{', '.join(short(z) for z in a['covers']) or '—'} | {ent or '—'} |")


def verified_table():
    print("| Id | Fact (" + R6 + ") | RVAs |")
    print("|---|---|---|")
    for v in verified():
        print(f"| `{v['id']}` | {v['text']} | {', '.join(f'`{r}`' for r in v['rvas']) or '—'} |")


def not_traced_table():
    print("| Id | Open question | What the data says |")
    print("|---|---|---|")
    for n in not_traced():
        print(f"| `{n['id']}` | {n['text']} | {n['data']} |")


# --- checker ------------------------------------------------------------------------------------

class Check:
    def __init__(self):
        self.ok, self.bad = 0, []

    def eq(self, what, doc_value, data_value):
        if doc_value == data_value:
            self.ok += 1
        else:
            self.bad.append(f"{what}: doc {doc_value!r}, data {data_value!r}")


def table_rows(body, header_start):
    """Rows (cells) of the first markdown table in `body` whose header line starts with `header_start`."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(header_start):
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append([c.strip() for c in row.strip().strip("|").split("|")])
            return rows
    raise KeyError(header_start)


def num_eq(doc_text, value):
    """The doc's number equals the data value at the doc's own precision."""
    d = doc_text.strip()
    places = len(d.split(".")[1]) if "." in d else 0
    return round(value, places) == round(float(d), places)


def block(page, mode):
    with open(os.path.join(ROOT, page), encoding="utf-8") as f:
        m = re.search(rf"<!-- damage_tables {re.escape(mode)} -->\r?\n(.*?)<!-- /damage_tables -->", f.read(), re.S)
    return [[c.strip() for c in r.strip().strip("|").split("|")] for r in m.group(1).strip().splitlines()[2:]]


GM_ROWS = {"Universal": "Universal"}


def gm_row_key(name):
    if name == "Universal":
        return name
    return "Meta.Damage." + name if name.startswith("DamageType.") else "Meta.Damage.Weapon." + name


def coverage(text):
    out = []
    for part in re.split(r",\s*(?![^()]*\))", text):
        p = part.strip().lower()
        if p.startswith("torso"):
            out += ["Torso.Upper", "Torso.Middle", "Torso.Lower"]
        elif p in ("—", "-", ""):
            continue
        else:
            out.append({"head": "Head", "neck": "Neck", "pelvis": "Pelvis", "upper arm": "Arm.Upper"}[p])
    return sorted(HIT + z for z in out)


def check():
    out = build()
    c = Check()
    contradictions = []
    bones, remap = hit_map()
    # DamagePipeline §8.1: Universal row and the archetype Head column.
    _, body = section(DP, "8.1")
    for name, val in table_rows(body, "| Hit location"):
        c.eq(f"§8.1 Universal {name}", True, num_eq(val, out["bone_rows"]["Universal"][HIT + name.strip("`")]))
    for name, val in table_rows(body, "| Row | Head"):
        c.eq(f"§8.1 Head {name}", True, num_eq(val, out["bone_rows"][name.strip("`")][HIT + "Head"]))
    n_ = r"(\d+(?:\.\d+)?)"
    m = re.search(rf"AR upper-torso hit therefore gets {n_} × {n_} = {n_}, and an AR headshot {n_} × {n_} = {n_}",
                  re.sub(r"\s+", " ", body))
    ar = dt.BONE["Meta.Damage.Weapon.AR"]
    c.eq("§8.1 worked AR upper torso", True, num_eq(m.group(3), dt.BONE["Universal"][HIT + "Torso.Upper"] * ar[HIT + "Torso.Upper"]))
    c.eq("§8.1 worked AR head", True, num_eq(m.group(6), dt.BONE["Universal"][HIT + "Head"] * ar[HIT + "Head"]))
    # GameMechanics §2c: the full table, every row and column.
    _, body = section(GM, "2c")
    rows = table_rows(body, "| Row |")
    header = [h.strip() for h in body[body.index("| Row |"):].splitlines()[0].strip().strip("|").split("|")][1:]
    expand_col = {"Torso.Up": "Torso.Upper", "Torso.Mid": "Torso.Middle", "Torso.Low": "Torso.Lower",
                  "Arm.Up": "Arm.Upper", "Arm.Low": "Arm.Lower"}
    cols = [HIT + expand_col.get(h, h) for h in header]
    c.eq("§2c columns", ZONES, cols)
    c.eq("§2c row count", len(out["bone_rows"]), len(rows))
    for r in rows:
        key = gm_row_key(r[0])
        c.eq(f"§2c row name {r[0]}", True, key in out["bone_rows"])
        if key not in out["bone_rows"]:  # compare the values with the data row ending in the same name
            key = next((k for k in out["bone_rows"] if k.endswith("." + r[0].rsplit(".", 2)[-2] + "." + r[0].rsplit(".", 1)[-1])), key)
        for col, val in zip(cols, r[1:]):
            c.eq(f"§2c {r[0]} {short(col)}", True, key in out["bone_rows"] and num_eq(val, out["bone_rows"][key][col]))
    # GameMechanics §2b: bone map and remap.
    _, body = section(GM, "2b")
    doc_map = {}
    for bs, cls in table_rows(body, "| Bone(s)"):
        for b in re.findall(r"`(\w+)`", bs):
            doc_map[b] = HIT + cls
    c.eq("§2b bone set", sorted(bones), sorted(doc_map))
    for b, t in bones.items():
        c.eq(f"§2b {b}", doc_map.get(b), t)
    pairs = dict(re.findall(r"`(\w+)`(?: is remapped)? to `(\w+)`", body))
    c.eq("§2b remap", remap, pairs)
    n = re.search(r"has (\d+) `DamageImpactRemap` entries", body)
    c.eq("§2b remap count", int(n.group(1)), len(remap))
    c.eq("§2b class count", len(set(bones.values())), int(re.search(r"map to (\d+) hit-location classes", body).group(1)))
    # DamagePipeline §7.5 armor table.
    _, body = section(DP, "7.5")
    by_item = {a["item"]: a for a in out["armor"]}
    for item, ctag, dur, r, cov in table_rows(body, "| Item | Context tag"):
        if item.startswith("Ghillie"):
            ghillie = [a for a in out["armor"] if a["tag"].endswith(".Ghillie")]
            c.eq("§7.5 Ghillie items", 4, len(ghillie))
            c.eq("§7.5 Ghillie R/stages", True, all(a["reduction_pct"] == 0 and not a["stage_reductions"] for a in ghillie))
            c.eq("§7.5 Ghillie coverage", True, all(not a["covers"] for a in ghillie))
            continue
        a = by_item.get(item.strip("`"))
        c.eq(f"§7.5 {item} exists", True, a is not None)
        if not a:
            continue
        c.eq(f"§7.5 {item} tag", ctag.strip("`"), a["tag"])
        c.eq(f"§7.5 {item} max durability", True, num_eq(dur, a["max_durability"]))
        c.eq(f"§7.5 {item} R", True, num_eq(r, a["reduction_pct"]) and len(set(a["stage_reductions"])) == 1)
        c.eq(f"§7.5 {item} covers", coverage(cov), sorted(a["covers"]))
    c.eq("§7.5 item count (non-Ghillie)", len([a for a in out["armor"] if not a["tag"].endswith(".Ghillie")]),
         len([r for r in table_rows(body, "| Item | Context tag") if not r[0].startswith("Ghillie")]))
    # DamagePipeline §3.1: the custom entries the source list is built from.
    _, body = section(DP, "3.1")
    for ents, cls, *_ in table_rows(body, "| Entries | Class"):
        for i in map(int, re.findall(r"\d+", ents)):
            obj = (dt.ENTRIES[i]["OutModification"]["CustomOperationClass"] or {}).get("ObjectName", "")
            c.eq(f"§3.1 entry {i} class", True, cls.strip("`").replace("_C", "") in obj)
    for i, need in ((5, "Meta.Damage.Bullet"), (7, BLUNT), (10, "Meta.Damage.Cannon")):
        c.eq(f"§3.1 entry {i} source", [need], dt.ENTRIES[i]["SourceRequirements"])
    # DamagePipeline §7.7 and §7.8: the bullet values this JSON reuses, decoded from the compact encoding.
    bullets = {s["label"]: s for s in out["sources"] if s.get("in_doc_table")}
    doc77 = block(DP, "default")
    c.eq("§7.7 weapon set", sorted(r[0] for r in doc77), sorted(bullets))
    for r in doc77:
        s = bullets.get(r[0])
        if not s:
            continue
        S, fz = s["values"]["direct"][0]["S"], decode(s["values"]["direct_zones"], s["zone_multiplier"], out["bone_rows"])
        c.eq(f"§7.7 {r[0]} base", True, num_eq(r[3], S))
        for loc, cell in zip(dt.LOCATIONS, r[4:10]):
            f = fz[ZONES.index(HIT + loc)]
            c.eq(f"§7.7 {r[0]} {loc}", cell, f"{S * f:.1f} (×{f:.3g})")
    for r in block(DP, "--falloff"):
        s = bullets.get(r[0].rstrip("†"))
        if not s:
            c.eq(f"§7.8 {r[0]}", "present", "missing")
            continue
        v = s["values"]
        torso = v["direct"][0]["S"] * decode(v["direct_zones"], s["zone_multiplier"], out["bone_rows"])[ZONES.index(HIT + "Torso.Upper")]
        keys = [{"Time": t * 100, "Value": x} for t, x in v["falloff"]["keys_m"]]
        for m, cell in zip(dt.RANGES_M, r[2:]):
            c.eq(f"§7.8 {r[0]} {m} m", cell, f"{torso * dt.falloff(keys, m * 100):.1f}")
    # Internal: the compact encoding gives back every factor the rules give, for every projectile source.
    for s in out["sources"]:
        if "_fs" in s:
            got = decode(s["values"]["direct_zones"], s["zone_multiplier"], out["bone_rows"])
            c.eq(f"encoding {s['id']}", True, all(abs(a - b) <= 1e-12 * max(1, abs(b)) for a, b in zip(got, s["_fs"])))
    # Round 6: blast hits never carry ExplosiveBlunt, so entries 7, 117, 142, 143 are absent from every blast;
    # back-blast is enabled on Launcher_04, RPG7 and CGM4 only.
    blast = [s for s in out["sources"] if s["values"].get("radial")]
    c.eq("blast sources without entries 7/117/142/143", [], [s["id"] for s in blast if set(s["radial_entries"]) & {7, 117, 142, 143}])
    bb = sorted(s["label"].replace(" back-blast", "") for s in out["sources"] if s["group"] == "Back-blast" and s["values"]["enabled"])
    c.eq("back-blast enabled (round 6)", ["CGM4", "Launcher_04", "RPG7"], bb)
    # Internal: the projectile loader agrees with damage_tables.projectiles() on every caliber it knows.
    for pid, (src, ctx, base) in dt.projectiles().items():
        p = PROJ.get(pid)
        c.eq(f"projectile {pid}", (src, ctx, base), (p["source_tag"], p["context"], p["values"].get("BaseDamage")) if p else None)
    # Doc-vs-doc notes the checker can see.
    _, gm2f = section(GM, "2f")
    if "whether percentages stack additively or multiplicatively is not verified" in gm2f:
        contradictions.append("GameMechanics §2f: \"The exact evaluation order and whether percentages stack additively or "
                              "multiplicatively is not verified from the data.\" DamagePipeline §5-§6 (Native): every entry "
                              "multiplies, order does not change an infantry result")
    if re.search(r"\| Bone \| Bullet \(hits Infantry\) \| — \| −75% \| Custom operation", gm2f):
        contradictions.append("GameMechanics §2f lists the custom entries' literals as changes (Bone −75%, Penetration "
                              "−50%, Melee/Armor −50%); DamagePipeline §2: those literals have no effect, the operation "
                              "decides (§7.1, §7.4, §7.5)")
    if "Friendly-fire and melee rules use the `Friendly` alignment" in gm2f:
        contradictions.append("GameMechanics §2f: \"Friendly-fire and melee rules use the Friendly alignment.\" Data: only "
                              "entries 8 and 9 are Friendly; the melee armor entry 144 has alignment None")
    _, gm2j = section(GM, "2j")
    if "per-hit-location values" in gm2j:
        contradictions.append("GameMechanics §2j: ArchetypeCaliberModifiers rows hold \"per-hit-location values\"; "
                              "DamagePipeline §7.2 and §8.2: each row is a caliber → value map (CaliberModifiers)")
    _, gm2c = section(GM, "2c")
    if "Each row is a damage-type tag" in gm2c:
        contradictions.append("GameMechanics §2c: \"Each row is a damage-type tag.\" Data: 18 of the 20 rows are weapon "
                              "tags (Meta.Damage.Weapon.*), plus Universal and Meta.Damage.DamageType.Melee; §7.1 picks the "
                              "row by source-context tag. The DamageType.Melee row is never selected for a melee-only source "
                              "(entries 5, 7, 10 need Bullet, ExplosiveBlunt or Cannon)")
    # The model, when present: no images or textures, and the bone map against its bodies.
    if out["model"]:
        c.eq("GLB images", 0, out["model"]["images"])
        c.eq("GLB textures", 0, out["model"]["textures"])
        c.eq("GLB bodies with no hit-location mapping", [], out["model"]["bodies_without_mapping"])
        c.eq("GLB centre per body", True, all(out["model"]["centres"].get(b) for b in out["model"]["bodies"]))
        print(f"MODEL {out['model']['physics_asset']}: {out['model']['body_count']} bodies; mapped bones with no body: "
              f"{', '.join(out['model']['mapped_without_body']) or 'none'}; bodies with no mapping: "
              f"{', '.join(out['model']['bodies_without_mapping']) or 'none'}")
    for line in c.bad:
        print("MISMATCH " + line)
    for line in contradictions:
        print("NOTE " + line)
    print(f"checks ok={c.ok} mismatched={len(c.bad)}")
    return not c.bad


# --- blocks -------------------------------------------------------------------------------------

BLOCK = re.compile(r"<!-- infantry_tables (.+?) -->\r?\n.*?<!-- /infantry_tables -->", re.S)
MODES = {"--zones": zones_table, "--bones": bones_table, "--multipliers": multipliers_table, "--sources": sources_table,
         "--explosives": explosives_table, "--armor": armor_table, "--not-traced": not_traced_table,
         "--verified": verified_table}


def write_docs():
    path = os.path.join(ROOT, PAGE)
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        nl = "\r\n" if "\r\n" in text else "\n"

        def regen(m):
            mode = m.group(1)
            args = [] if mode == "default" else mode.split()
            res = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + args,
                                 capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
            return nl.join([f"<!-- infantry_tables {mode} -->"] + res.split("\n") + ["<!-- /infantry_tables -->"])

        new, n = BLOCK.subn(regen, text)
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {n} tables {'updated' if new != text else 'unchanged'}")
    else:
        print(f"{PAGE}: not found, no tables written")
    write_json()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if "--write" in args:
        write_docs()
    elif "--json" in args:
        write_json()
    elif "--check" in args:
        sys.exit(0 if check() else 1)
    else:
        mode = next((a for a in args if a in MODES), "--zones")
        MODES[mode]()


if __name__ == "__main__":
    main()
