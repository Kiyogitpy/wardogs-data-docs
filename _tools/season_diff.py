"""Season 1 -> Season 2 differ for every game-data JSON export (round 22).

Compares each JSON export under a Season 1 data/ folder with the Season 2 one and writes machine-readable
results to assets/data/season-diff/ (index.json plus one <area-id>.json per site area). The "Season 2 Changes"
pages read these files. Standard library only; output is deterministic.

    python _tools/season_diff.py --write                 # regenerate the committed files
    python _tools/season_diff.py --check                 # regenerate in memory, exit 1 if the files differ
    python _tools/season_diff.py --s1 DIR --s2 DIR       # other inputs (default S1 below, S2 = repo data/)
    python _tools/season_diff.py --stats                 # print totals and noise counters, write nothing

Inputs. Season 1 is the pre-update export (commit bea446b of the old clone, extracted to S1_DEFAULT); Season 2 is
this repo's data/ (build ++Wardogs+Live-CL-516586, 2026-10-15, re-exported with the v2 usmap). Config/*.ini was
kept from Season 1 and not re-exported, so it is byte-identical on both sides and is not compared (the script
only reads *.json and verifies the .ini files match, reporting if they do not).

File format. A *.json export file holds one or more exports, each introduced by a "--- export: Class / Name ---"
line and followed by one JSON object. Every export is parsed with an object_pairs_hook so DUPLICATE KEYS in
one object survive: the first keeps its name, later ones become "Key#2", "Key#3" (Season 1 has 1,718 such objects).

Asset pairing (file level).
  1. same relative path                                   -> paired_by null
  2. removed and added file with the same file name       -> status "moved", paired_by "same-name"
  3. git rename (table GIT_RENAMES, from `git diff -M bea446b 0b608e1`) accepted only when the file names agree
     after substituting the old folder-before-Content name by the new one (Mosin -> WEPN_017), or when exactly one
     folder of the path was renamed and the file names share an 8+ character stem (Flares -> Countermeasures)
     -> "git-rename".
     The other git renames pair unrelated curves by text similarity and are rejected (listed in REJECTED).
  4. remaining removed/added pairs with the same main export Type and the same identifying id (a
     Properties.<X>Id.TagName value that is unique on both sides)  -> status "moved", paired_by "inferred"
  Everything else is "removed" or "added".

Value comparison (diff_value).
  Numbers equal within 1e-6 relative are unchanged; raw values are reported as stored.
  Dicts: keys compared by name. Keys only on one side are first matched as RENAMES (noise): a key that looks
    hashed ("_aaa...", optionally "_$HEX$_$n$") or a Key#2 duplicate on one side, paired with a key on the other side whose value is
    identical (any position), or, failing that, a key in the same gap between common keys with the same kind of
    value (then the pair is diffed as a normal property and the rename itself is noise). Counted in
    noise.renamed_keys; paths use the Season 2 name.
    Swapped keys: sibling keys whose values are exchanged exactly (2-cycles, 3-cycles) are noise.swapped_keys.
    A vector-valued S1 key whose name says another shape (RelativeScale3D) paired with an identical S2 key
    (RelativeLocation) is a renamed key.
    Season 1 duplicate keys: the occurrence matching Season 2's Key (by value, then by neighbouring common keys)
    keeps the name Key; the others become rename candidates. An unpaired empty []/{}/"NaN" duplicate is noise.dup_keys.
  Object references: a dict with ObjectName and ObjectPath whose ObjectName is equal and whose ObjectPath differs
    only in the trailing export index (".123") is a REF SHIFT (noise.ref_shifts). If the name differs, or the
    path differs beyond the index, it is a real change.
  Arrays, alignment rules:
    * all elements are dicts with a natural identity (first of RowName, Name, Key, Id, ItemId, Tag, TagName,
      GameplayTag, ObjectName, then any other key ending in Tag/Id/Name, whose value is a unique string/int/tag/object name on both sides) -> aligned BY
      IDENTITY, paths read "Path[Name=Foo].Field"; elements only on one side are added/removed; a different order
      of the common identities is one "resequenced" op listing the identity order before and after.
    * equal length otherwise -> aligned BY INDEX ("Path[3].Field"); a scalar array holding the same values in a
      different order is one "resequenced" op.
    * different length otherwise -> the common prefix and suffix are matched, the middle is aligned with difflib on
      normalised element text; equal runs are unchanged, replaced runs are paired by index, extra elements are
      added/removed ("Path[index]" with the Season 2 index for added, Season 1 index for removed). Oversized
      middles fall back to index pairing. When the leftover elements are all structs they are re-aligned: exact
      matches anywhere in the array are unchanged, then the most similar pairs (>= 50% identical leaf values) are
      diffed, the rest are removed + added. Equal-length arrays get the same treatment when an element merely moved.
  A change of kind (scalar vs object vs array) is one "changed" op with both whole values.
  Added/removed sub-objects are one op carrying the whole compact value.
  Multi-export files prefix every path with "ExportName::" (exports are matched by name, then by occurrence;
  exports left over on both sides are paired in order when their Type is equal, which covers renamed assets).

Areas: AREA_RULES maps each asset path (first matching regex) to one of the ten site areas.
"""
import argparse
import difflib
import json
import math
import os
import re
import struct
import subprocess
import sys

SWITCHED = []
SWAPS = []
PERM_INSTANCES = []
CANDS = None   # list when --named-candidates is given

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S1_DEFAULT = "E:/wardogs_builds/season1/data"
S2_DEFAULT = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(ROOT, "assets", "data", "season-diff")
GENERATED_BY = "_tools/season_diff.py"
SPLIT_BYTES = 5 * 1024 * 1024
REL_TOL = 1e-6

HEADER = re.compile(r"^--- export: (.*?) ---\r?\n", re.M)
HASHED = re.compile(r"^_aaa[a-z]{10,}(?:_\$[0-9A-F]+\$_\$\d+\$)?$")
DUP_SUFFIX = re.compile(r"#\d+$")
INDEX_SUFFIX = re.compile(r"\.\d+$")
ID_KEYS_OLD = ("RowName", "Name", "Key", "Id", "ItemId", "Tag", "TagName", "GameplayTag", "ObjectName")
ID_KEYS = ID_KEYS_OLD + ("ID", "NodeId", "NodeID")

AREAS = [
    ("weapons-ammo", "Weapons & Ammo"),
    ("vehicles", "Vehicles"),
    ("damage-combat-systems", "Damage & Combat Systems"),
    ("player-movement", "Player & Movement"),
    ("items-equipment", "Items & Equipment"),
    ("rewards-unlocks", "Rewards & Unlocks"),
    ("game-modes-maps", "Game Modes & Maps"),
    ("world-visuals-audio", "World, Visuals & Audio"),
    ("data-tables-tags", "Data Tables & Tags"),
    ("engine-tooling-data", "Engine & Tooling Data"),
]
STATUS_ORDER = {"modified": 0, "moved": 1, "added": 2, "removed": 3}

G = "Wardogs/Plugins/GameFeatures/"
C = "Wardogs/Content/"
# First matching rule wins. Pattern is matched against the path relative to data/.
AREA_RULES = [
    (r"^Engine/", "engine-tooling-data"),
    # --- audio and world ---
    (C + r"Audio/", "world-visuals-audio"),
    (C + r"VFX/", "world-visuals-audio"),
    (C + r"(Environment|FluidFlux|ExternalAssets)/", "world-visuals-audio"),
    (G + r"(WorldFeatures|FlyByManager|ArtWorld)/", "world-visuals-audio"),
    # --- weapons and ammo ---
    (C + r"Weapons/", "weapons-ammo"),
    (C + r"Items/(Weapons|Attachments|Throwable)/", "weapons-ammo"),
    (G + r"(Ammo|Gunsmith|UnderbarrelGrenadeLauncher|PrototypeMaskedScopes)/", "weapons-ammo"),
    (G + r"Weapons/VehicleWeaponry/", "vehicles"),
    (G + r"Weapons/", "weapons-ammo"),
    (G + r"Items/(AT_mine|C4|Claymore|IED|Landmine|Molotov|SmokeGrenade)/", "weapons-ammo"),
    (G + r"Utility/Throwables/", "weapons-ammo"),
    (r"^Wardogs/Plugins/BHAimAssist/", "weapons-ammo"),
    # --- vehicles ---
    (C + r"Vehicles/", "vehicles"),
    (C + r"Items/Vehicles/", "vehicles"),
    (C + r"GameplayCues/Vehicles/", "vehicles"),
    (G + r"(Vehicles|Vehiclesmith|Skins|Taxi_SkinsData)/", "vehicles"),
    # --- damage and combat ---
    (C + r"(Demolition|Destruction)/", "damage-combat-systems"),
    (C + r"GameMechanics/(DamageSystem|GameplayEffects)/", "damage-combat-systems"),
    (G + r"(DamageExporter|DestructionPlayground)/", "damage-combat-systems"),
    # --- rewards and unlocks ---
    (C + r"Meta/", "rewards-unlocks"),
    (G + r"(Rewards|Challenges_KOTH|MoneyMan|FactoryInvestment\w*)/", "rewards-unlocks"),
    # --- items and equipment ---
    (C + r"Items/", "items-equipment"),
    (C + r"GameMechanics/(Inventory|Actions)/", "items-equipment"),
    (G + r"(Items|Itemsmith|Utility)/", "items-equipment"),
    # --- player and movement ---
    (C + r"(Animation|Characters|MoverTesting)/", "player-movement"),
    (C + r"GameMechanics/(Player|Communication)/", "player-movement"),
    (G + r"(Character|CharacterCustomiser|Customization|Emotes|Parachutes|PlayerHealthBar|BHMotionWarping|Mover|"
         r"AlternativeCriticalCamera|Spotting|WDCharacterComponents)/", "player-movement"),
    (r"^Wardogs/Plugins/BHSpectatorCamera/", "player-movement"),
    # --- modes and maps ---
    (C + r"Maps/", "game-modes-maps"),
    (C + r"GameMechanics/(Gamemode|AI)/", "game-modes-maps"),
    (G + r"(AI|ControlZone|ControlZoneRegions|Deathmatch|Experiences|HotPotato|PvE|ShootingRange|ShootingRangeTutorial|"
         r"TeamOffence|ServerSeeding|MonkeyScore|TeamkillTracking)/", "game-modes-maps"),
    # --- data tables and settings ---
    (C + r"GameMechanics/(Settings|WorldInteractable)/", "data-tables-tags"),
    # --- engine and tooling (UI lands here unless it is a data table, see classify) ---
    (C + r"(UI|Significance|Tools|Tests|Developers)/", "engine-tooling-data"),
    (r"^Wardogs/Plugins/BHFramework/", "engine-tooling-data"),
    (G + r"(WDCore|WDAutomation|DispatchMetricsGame|PerformanceCaptures|RegistryExporter|ReportTracking|Developer|"
         r"HighPingKick|AccountWatermark|\w+)/", "engine-tooling-data"),
]
AREA_RULES = [(re.compile(p), a) for p, a in AREA_RULES]

# `git -C <old clone> diff -M --name-status --diff-filter=R bea446b 0b608e1 -- data/` (paths relative to data/).
# A rename is accepted (paired_by "git-rename") only when accept_rename() agrees; the rest pair unrelated curves.
GIT_RENAMES = [
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_Shotgun.json", "Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_DamageIndicator_IntensityResponse.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_SMG_Hipfire.json", "Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Shotgun_Hipfire.json", "Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DestroySupplyCrate_Cash.json"),
    ("Wardogs/Content/UI/Features/HUD/Vehicles/NEWHUD/Flares/Data/DA_VehicleFlares.json", "Wardogs/Content/UI/Features/HUD/Vehicles/NEWHUD/Countermeasures/Data/DA_VehicleCountermeasure.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_AR.json", "Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Default.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_SMG.json", "Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_Default.json"),
    ("Wardogs/Content/GameMechanics/Inventory/AR_SuppressionCurve.json", "Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Curves/CRV_FreeLookPitchRange_STN_06.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_LMG.json", "Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_CollisionDamage_WHL_08.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Melee_Hipfire.json", "Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_ForeignVehicleCollisionDamage_WHL_08.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_LMG_Hipfire.json", "Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_Torque_WHL_08.json"),
    ("Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_Pistol.json", "Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_VehicleCollisionDamage_WHL_08.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/AnimSet_Mosin.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/AnimSet_Mosin.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Attachments/ID_SR_02_BRL_04.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Attachments/ID_SR_02_BRL_04.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Attachments/ID_SR_02_GRP_02.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Attachments/ID_SR_02_GRP_02.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Attachments/ID_SR_02_STK_01.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Attachments/ID_SR_02_STK_01.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Components/ID_MosinBarrel.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Components/ID_MosinBarrel.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Components/ID_MosinStock.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Components/ID_MosinStock.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/DA_Mosin_Stats.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DA_WEPN_017_Stats.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/DT_VendorData_Weapon_Mosin.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_VendorData_Weapon_Mosin.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/ID_Mosin_MagInternal.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_Mosin_MagInternal.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/ID_Mosin.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_WEPN_017.json"),
    ("Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/ID_Mosin_Audio.json", "Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_WEPN_017_Audio.json"),
]


# --- parsing --------------------------------------------------------------------------------------
def _pairs_hook(pairs):
    """Build a dict keeping duplicate keys (second occurrence becomes Key#2, third Key#3, ...)."""
    out = {}
    for k, v in pairs:
        if k in out:
            n = 2
            while "%s#%d" % (k, n) in out:
                n += 1
            k = "%s#%d" % (k, n)
        out[k] = v
    return out


_DECODER = json.JSONDecoder(object_pairs_hook=_pairs_hook, parse_constant=lambda s: s)


def parse_exports(text):
    """Return ([(header, obj), ...], error_or_None) for one *.json export file."""
    parts = HEADER.split(text)
    exports = []
    err = None
    for i in range(1, len(parts), 2):
        body = parts[i + 1].lstrip()
        try:
            obj, _end = _DECODER.raw_decode(body)
        except ValueError as e:
            err = "export %r unparseable: %s" % (parts[i], e)
            break
        exports.append((parts[i], obj))
    return exports, err


def read_file(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def list_json(root):
    out = {}
    for d, _dirs, files in os.walk(root):
        for f in files:
            if f.endswith(".json"):
                full = os.path.join(d, f)
                out[os.path.relpath(full, root).replace(os.sep, "/")] = full
    return out


# --- value comparison -----------------------------------------------------------------------------
def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def same_scalar(a, b):
    if is_num(a) and is_num(b):
        if a == b:
            return True
        try:
            return math.isclose(a, b, rel_tol=REL_TOL, abs_tol=1e-12)
        except (OverflowError, ValueError):
            return False
    return type(a) is type(b) and a == b


def is_ref(d):
    return isinstance(d, dict) and "ObjectName" in d and "ObjectPath" in d


def ref_shift(a, b, parent_a, parent_b):
    """True if a/b are ObjectPath strings differing only by the trailing export index with the same ObjectName."""
    return (isinstance(a, str) and isinstance(b, str) and a != b
            and parent_a.get("ObjectName") == parent_b.get("ObjectName")
            and INDEX_SUFFIX.sub("", a) == INDEX_SUFFIX.sub("", b))


def deep_same(a, b):
    """Equality modulo float tolerance and ref shifts (no counting)."""
    if isinstance(a, dict):
        if not isinstance(b, dict):
            return False
        if set(a) != set(b):
            # keys that differ only by unknown (hashed / duplicate) names are compared by position
            ua = [k for k in a if k not in b]
            ub = [k for k in b if k not in a]
            if len(ua) != len(ub) or not all(unnamed(k) for k in ua + ub):
                return False
            return all(deep_same(a[k], b[k]) for k in a if k in b) and                 all(deep_same(a[x], b[y]) for x, y in zip(ua, ub))
        for k, v in a.items():
            if k == "ObjectPath" and ref_shift(v, b[k], a, b):
                continue
            if not deep_same(v, b[k]):
                return False
        return True
    if isinstance(a, list):
        return isinstance(b, list) and len(a) == len(b) and all(deep_same(x, y) for x, y in zip(a, b))
    if isinstance(b, (dict, list)):
        return False
    return same_scalar(a, b)


def norm_text(v):
    """Stable text for an element, used only to align arrays (floats rounded, ref index dropped)."""
    if isinstance(v, dict):
        return "{" + ",".join("%s:%s" % (k, norm_text(x) if k != "ObjectPath" or not isinstance(x, str) else INDEX_SUFFIX.sub("", x))
                              for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ",".join(norm_text(x) for x in v) + "]"
    if is_num(v):
        return "n%.6g" % v
    return json.dumps(v)


def join(path, key):
    return key if not path else path + "." + key


class Ctx:
    def __init__(self):
        self.changes = []
        self.renamed = 0
        self.shifts = 0
        self.dups = 0
        self.swapped = 0
        self.reinterp = 0
        self.mark = 0
        self.perm_instances = []
        self.swaps = []
        self.cands = []
        self.switched = []
        self.collect = False

    def add(self, path, op, before, after):
        row = {"path": path, "op": op, "before": before, "after": after}
        if self.mark:
            row["matched"] = "position"
        self.changes.append(row)


def unnamed(k):
    """A hashed name, or a Key#2 duplicate (Season 1 duplicate names were usmap artifacts)."""
    return bool(HASHED.match(k) or DUP_SUFFIX.search(k))


def hash_body(k):
    return re.sub(r"_\$[0-9A-F]+\$_\$\d+\$$", "", k)


def named_keys(d):
    return frozenset(k for k in d if not unnamed(k))


def _dict_shape(x, y):
    """Same number of keys, and the named keys of one side are contained in the other's (hashed names are unknown)."""
    nx, ny = named_keys(x), named_keys(y)
    return len(x) == len(y) and (nx <= ny or ny <= nx)


def shape_same(x, y):
    """Same JSON shape: same type; objects the same key count with compatible named keys; struct arrays likewise."""
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and _dict_shape(x, y)
    if isinstance(x, list) or isinstance(y, list):
        if not (isinstance(x, list) and isinstance(y, list)):
            return False
        dx = [e for e in x if isinstance(e, dict)]
        dy = [e for e in y if isinstance(e, dict)]
        if dx and dy:
            return _dict_shape(dx[0], dy[0])
        return not dx and not dy or not x or not y
    if x is None or y is None:
        return x is y
    for typ in (bool, str):
        if isinstance(x, typ) or isinstance(y, typ):
            return isinstance(x, typ) and isinstance(y, typ)
    return is_num(x) and is_num(y)


def match_renames(a, b, only_a, only_b, common_a, common_b):
    """Pair unnamed keys (hashed or Key#n) with their other-usmap counterparts. Returns {old_key: new_key}.

    Noise pairing needs equal values, except where identity is certain: the same hash body on both sides, or one
    named side and exactly one candidate in the gap. Otherwise the keys are left to show as removed + added."""
    pairs = {}
    pos = set()    # pairs matched by position with differing values (flagged matched=position)
    used = set()
    # 0. same hash body (the hashed name differs only by the _$HEX$_$n$ suffix)
    for ka in only_a:
        for kb in only_b:
            if kb not in used and HASHED.match(ka) and hash_body(ka) == hash_body(kb):
                pairs[ka] = kb
                used.add(kb)
                break
    # 1. identical values
    for ka in only_a:
        if ka in pairs:
            continue
        for kb in only_b:
            if kb in used:
                continue
            if (unnamed(ka) or unnamed(kb)) and (deep_same(a[ka], b[kb]) or reinterpreted(a[ka], b[kb])):
                pairs[ka] = kb
                used.add(kb)
                break
    # 1b. each side has exactly one unpaired unknown key, with the same shape of value
    rest_a = [k for k in only_a if k not in pairs and unnamed(k)]
    rest_b = [k for k in only_b if k not in used and unnamed(k)]
    if len(rest_a) == 1 and len(rest_b) == 1 and shape_same(a[rest_a[0]], b[rest_b[0]]):
        pairs[rest_a[0]] = rest_b[0]
        used.add(rest_b[0])
        pos.add(rest_a[0])
    # 2. same gap between common keys, same shape of value, one named side, unambiguous
    def gaps(keys, only, common):
        out = {}
        idx = {k: i for i, k in enumerate(common)}
        last = -1
        for k in keys:
            if k in idx:
                last = idx[k]
            elif k in only:
                out.setdefault(last, []).append(k)
        return out
    ga = gaps(list(a), set(only_a) - set(pairs), common_a)
    gb = gaps(list(b), set(only_b) - used, common_b)
    for gap, la in ga.items():
        lb = gb.get(gap, [])
        if any(k in pairs for k in la) or any(k in used for k in lb):
            continue
        if len(la) == 1 and len(lb) == 1:
            ka, kb = la[0], lb[0]
            one_named = not HASHED.match(ka) or not HASHED.match(kb)
            if (unnamed(ka) or unnamed(kb)) and one_named and shape_same(a[ka], b[kb]):
                pairs[ka] = kb
                pos.add(ka)
    return pairs, pos


def kind(v):
    return "dict" if isinstance(v, dict) else "list" if isinstance(v, list) else "scalar"


SHAPE_WORDS = ("scale", "location", "translation", "rotation", "extent", "offset", "size", "color")


def shape_of(name):
    n = name.lower()
    return next((w for w in SHAPE_WORDS if w in n), None)


def collect_named(a, b, only_a, only_b, pairs, path, ctx):
    """Report-only: named-to-named keys with an identical value (not suppressed, see --named-candidates)."""
    left_a = [k for k in only_a if k not in pairs and not unnamed(k)]
    left_b = [k for k in only_b if k not in pairs.values() and not unnamed(k)]
    for ka in left_a:
        for kb in left_b:
            if deep_same(a[ka], b[kb]):
                v = a[ka]
                sa, sb = shape_of(ka), shape_of(kb)
                ctx.cands.append({
                    "parent": path, "old_key": ka, "new_key": kb, "value": v,
                    "trivial_value": not isinstance(v, (dict, list)) and v in (0, 1, True, False, "", "None", 0.0),
                    "shape_mismatch": bool(sa and sb and sa != sb and isinstance(v, dict)),
                })


COMPONENT_KEYS = {"X", "Y", "Z", "W", "R", "G", "B", "A", "Pitch", "Yaw", "Roll"}
KEPT_MINMAX = []
OBS_ON = False


def _greater(x, y):
    if isinstance(x, dict) and isinstance(y, dict):
        nums = [q for q in x if q in y and is_num(x[q]) and is_num(y[q])]
        return bool(nums) and all(x[q] >= y[q] for q in nums) and any(x[q] > y[q] for q in nums)
    return is_num(x) and is_num(y) and x > y


def minmax_ok(k, j, a):
    """A Min*/Max* pair is suppressed as a naming swap only if Season 1 had Min greater than Max."""
    kl, jl = k.lower(), j.lower()
    for lo, hi in ((k, j), (j, k)):
        if "min" in lo.lower() and lo.lower().replace("min", "max", 1) == hi.lower().replace("imum", "imum"):
            return _greater(a[lo], a[hi])
        if "minimum" in lo.lower() and lo.lower().replace("minimum", "maximum", 1) == hi.lower():
            return _greater(a[lo], a[hi])
    return True


LEARNED = []      # [{S1 name: S2 name}], one permutation per learned key set, filled between the two passes
OBSERVED = []     # (key set, ((s1 name, s2 name), ...)) per exact cycle (pass 1)
UNAFFECTED = []   # instances of a learned permutation left alone because S1 already matched S2 name for name


def apply_learned(a, b, path, ctx):
    """Rename S1 keys by the learned permutations, so real value changes survive under the right name.

    A permutation applies to a parent that has at least one of its keys in S1 and at least one in S2 (so a
    Min-only S1 against a Max-only S2 is covered). Skipped when every key in both is already unchanged."""
    if not LEARNED:
        return a
    ren = {}
    for perm in LEARNED:
        in_a = [k for k in perm if k in a]
        if not in_a or not any(v in b for v in perm.values()):
            continue
        both = [k for k in perm if k in a and k in b]
        if both and len(both) == len(in_a) and all(deep_same(a[k], b[k]) for k in both):
            UNAFFECTED.append(path)
            continue
        ren.update({k: perm[k] for k in in_a})
    if not ren:
        return a
    ctx.swapped += len(ren)
    ctx.perm_instances.append({"parent": path, "mapping": dict(ren)})
    return {ren.get(k, k): v for k, v in a.items()}


def learn(observed):
    """Accept a mapping seen >= 2 times exactly where no source key maps to two targets and no target has two sources."""
    support, targets, sources = {}, {}, {}
    for ks, mp in observed:
        support.setdefault((ks, mp), 0)
        support[(ks, mp)] += 1
        for k, j in mp:
            targets.setdefault(k, set()).add(j)
            sources.setdefault(j, set()).add(k)
    learned, refused = [], []
    for (ks, mp), n in sorted(support.items(), key=lambda kv: sorted(kv[0][0])):
        bad = any(len(targets[k]) > 1 for k, _ in mp) or any(len(sources[j]) > 1 for _, j in mp)
        if n >= 2 and not bad:
            learned.append(dict(mp))
        else:
            refused.append({"keys": sorted(ks), "mapping": dict(mp), "count": n,
                            "reason": "contradicting exact instances" if bad else "single exact instance"})
    return learned, refused


def find_swaps(a, b, path, ctx):
    """Sibling keys whose values are exchanged exactly between the seasons (S1 usmap misassigned the names).

    Finds exact 2-cycles and 3-cycles among common keys that changed. Nothing is suppressed here: cycles feed
    the learning pass (OBSERVED), and cycles still present in pass 2 (not learned) are only listed in ctx.swaps."""
    ch = [k for k in a if k in b and not deep_same(a[k], b[k]) and k not in COMPONENT_KEYS]
    if len(ch) < 2 or len(ch) > 200:
        return set()
    to = {k: [j for j in ch if j != k and deep_same(a[k], b[j])] for k in ch}
    used, cycles, mp = set(), [], {}
    for k in ch:
        if k in used:
            continue
        for j in to[k]:
            if j not in used and k in to[j]:
                used |= {k, j}
                cycles.append([k, j])
                mp[k], mp[j] = j, k
                break
    for k in ch:
        if k in used:
            continue
        for j in to[k]:
            if j in used:
                continue
            for m in to[j]:
                if m not in used and m not in (k, j) and k in to[m]:
                    used |= {k, j, m}
                    cycles.append([k, j, m])
                    mp[k], mp[j], mp[m] = j, m, k
                    break
            if k in used:
                break
    if OBS_ON:
        for cyc in cycles:
            OBSERVED.append((frozenset(cyc), tuple(sorted((k, mp[k]) for k in cyc))))
    # Exact cycles of a key set that was not learned (one-off or contradicted) are NOT suppressed: they are diffed
    # normally and only listed (in the --swaps file) so a reader can judge them.
    for cyc in cycles:
        ctx.swaps.append({"parent": path, "keys": cyc, "s1": [a[k] for k in cyc], "s2": [b[k] for k in cyc]})
    return set()


def resolve_dups(a, b):
    """Season 1 duplicate keys (Key, Key#2, ...): pick the occurrence that corresponds to Season 2's Key.

    Value match first, then the occurrence whose nearest earlier common key equals Season 2's. The chosen one is
    renamed to Key and the others to Key#2.. so the rest become rename candidates for hashed Season 2 keys."""
    ka = list(a)
    groups = {}
    for k in ka:
        base = DUP_SUFFIX.sub("", k)
        if base != k or any(x.startswith(k + "#") for x in ka):
            groups.setdefault(base, []).append(k)
    groups = {g: m for g, m in groups.items() if len(m) > 1 and g in b and g in a}
    if not groups:
        return a
    kb = list(b)
    members = {m for ms in groups.values() for m in ms}

    def pred(keys, k, other):
        i = keys.index(k)
        for x in reversed(keys[:i]):
            if x in other and x not in members:
                return x
        return None
    rename = {}
    for g, ms in groups.items():
        chosen = next((m for m in ms if deep_same(a[m], b[g])), None)
        if chosen is None:
            want = pred(kb, g, a)
            chosen = next((m for m in ms if pred(ka, m, b) == want), ms[0])
        rest = [m for m in ms if m != chosen]
        rename[chosen] = g
        for n, m in enumerate(rest, 2):
            rename[m] = "%s#%d" % (g, n)
    if all(rename[k] == k for k in rename):
        return a
    return {rename.get(k, k): v for k, v in a.items()}


def diff_dict(a, b, path, ctx):
    a = resolve_dups(a, b)
    a = apply_learned(a, b, path, ctx)
    ka, kb = list(a), list(b)
    only_a = [k for k in ka if k not in b]
    only_b = [k for k in kb if k not in a]
    pairs, pos = {}, set()
    if only_a and only_b:
        common_a = [k for k in ka if k in b]
        common_b = [k for k in kb if k in a]
        pairs, pos = match_renames(a, b, only_a, only_b, common_a, common_b)
    for ka in [k for k in only_a if k not in pairs and not unnamed(k)]:
        for kb_ in [k for k in only_b if k not in pairs.values() and not unnamed(k)]:
            sa, sb = shape_of(ka), shape_of(kb_)
            if sa and sb and sa != sb and isinstance(a[ka], dict) and deep_same(a[ka], b[kb_]):
                pairs[ka] = kb_   # S1 usmap misnamed a vector (RelativeScale3D holding a location)
                break
    if OBS_ON:
        la_ = [k for k in only_a if k not in pairs and not unnamed(k)]
        lb_ = [k for k in only_b if k not in pairs.values() and not unnamed(k)]
        for ka_ in la_:
            hits = [kb_ for kb_ in lb_ if deep_same(a[ka_], b[kb_])]
            if len(hits) == 1 and sum(deep_same(a[x], b[hits[0]]) for x in la_) == 1                     and not (not isinstance(a[ka_], (dict, list)) and a[ka_] in (0, 1, True, False, "", "None")):
                OBSERVED.append((frozenset((ka_, hits[0])), ((ka_, hits[0]),)))
    new_to_old = {v: k for k, v in pairs.items()}
    skip = find_swaps(a, b, path, ctx)
    if ctx.collect:
        collect_named(a, b, only_a, only_b, pairs, path, ctx)
    for k in kb:
        p = join(path, k)
        if k in skip:
            continue
        if k in a:
            va, vb = a[k], b[k]
            if k == "ObjectPath" and isinstance(va, str) and isinstance(vb, str) and va != vb:
                if ref_shift(va, vb, a, b):
                    ctx.shifts += 1
                    continue
            diff_value(va, vb, p, ctx)
        elif k in new_to_old:
            ctx.renamed += 1
            flagged = new_to_old[k] in pos
            ctx.mark += flagged
            diff_value(a[new_to_old[k]], b[k], p, ctx)
            ctx.mark -= flagged
        else:
            ctx.add(p, "added", None, b[k])
    for k in only_a:
        if k not in pairs:
            if DUP_SUFFIX.search(k) and a[k] in ([], {}, "NaN"):
                ctx.dups += 1   # empty/NaN duplicate from the old usmap, no Season 2 counterpart
                continue
            ctx.add(join(path, k), "removed", a[k], None)


def ident(v):
    if isinstance(v, (str, int)) and not isinstance(v, bool):
        return str(v)
    if isinstance(v, dict):
        if isinstance(v.get("TagName"), str):
            return v["TagName"]
        if isinstance(v.get("ObjectName"), str):
            return v["ObjectName"]
    return None


def identity_key(a, b):
    """The ID_KEYS entry that identifies every element of both lists uniquely, else None."""
    if not a and not b:
        return None
    if not all(isinstance(e, dict) for e in a) or not all(isinstance(e, dict) for e in b):
        return None
    extra = [k for k in (a[0] if a else b[0]) if k not in ID_KEYS and k.lower().endswith(("tag", "id", "name"))]
    for key in ID_KEYS + tuple(extra):
        ok = True
        for lst in (a, b):
            ids = [ident(e.get(key)) if key in e else None for e in lst]
            if any(i is None for i in ids) or len(set(ids)) != len(ids):
                ok = False
                break
        if ok and a and b and not ({ident(e[key]) for e in a} & {ident(e[key]) for e in b}):
            ok = False   # disjoint ids: not an identity field across seasons
        if ok:
            return key
    return None


SIM_MIN = 0.5


def leaves(v, prefix, out):
    """Flat {path: value text}; hashed key names become positional placeholders so renamed keys still compare."""
    if isinstance(v, dict):
        n = 0
        for k, x in v.items():
            if unnamed(k):
                k = "?%d" % n
                n += 1
            if k == "ObjectPath" and isinstance(x, str):
                x = INDEX_SUFFIX.sub("", x)
            leaves(x, prefix + "." + k, out)
    elif isinstance(v, list):
        for i, x in enumerate(v):
            leaves(x, "%s[%d]" % (prefix, i), out)
    else:
        out[prefix] = v if is_num(v) else json.dumps(v)
    return out


def leaf_eq(x, y, tol):
    if is_num(x) and is_num(y):
        return x == y or math.isclose(x, y, rel_tol=tol, abs_tol=1e-9)
    return not is_num(x) and not is_num(y) and x == y


def leaves_same(lx, ly):
    return lx.keys() == ly.keys() and all(leaf_eq(lx[k], ly[k], REL_TOL) for k in lx)


def similarity(lx, ly):
    keys = set(lx) | set(ly)
    # requirement / tag fields identify an element: if any differs these are different elements
    for k in keys:
        if ("Requirement" in k or "Tag" in k) and not (k in lx and k in ly and leaf_eq(lx[k], ly[k], 1e-3)):
            return 0.0
    return sum(1 for k in keys if k in lx and k in ly and leaf_eq(lx[k], ly[k], 1e-3)) / len(keys) if keys else 1.0


def align_unmatched(a, b, ua, ub, path, ctx):
    """Align the elements left over after the sequence match: exact matches anywhere first (no change), then the
    most similar pairs (>= SIM_MIN share of identical leaf values), the rest are removed + added."""
    la_ = {i: leaves(a[i], "", {}) for i in ua}
    lb_ = {j: leaves(b[j], "", {}) for j in ub}
    left_a, left_b = set(ua), set(ub)
    for j in ub:
        cands = [i for i in left_a if leaves_same(la_[i], lb_[j])]
        if cands:
            i = min(cands, key=lambda i: abs(i - j))
            left_a.discard(i)
            left_b.discard(j)
    pairs = []
    if len(left_a) * len(left_b) <= 250_000:
        scored = sorted(((similarity(la_[i], lb_[j]), -abs(i - j), i, j) for i in left_a for j in left_b), reverse=True)
        for s, _d, i, j in scored:
            if s < SIM_MIN:
                break
            if i in left_a and j in left_b:
                left_a.discard(i)
                left_b.discard(j)
                pairs.append((i, j))
    ev = [(j, "pair", i) for i, j in pairs] + [(j, "added", None) for j in left_b]
    for j, how, i in sorted(ev):
        if how == "pair":
            diff_value(a[i], b[j], "%s[%d]" % (path, j), ctx)
        else:
            ctx.add("%s[%d]" % (path, j), "added", None, b[j])
    for i in sorted(left_a):
        ctx.add("%s[%d]" % (path, i), "removed", a[i], None)


def scratch_of(ctx):
    s = Ctx()
    s.collect = ctx.collect
    s.mark = ctx.mark
    return s


def merge_ctx(ctx, s):
    ctx.changes.extend(s.changes)
    for f in ("renamed", "shifts", "dups", "swapped", "reinterp"):
        setattr(ctx, f, getattr(ctx, f) + getattr(s, f))
    for f in ("cands", "swaps", "switched", "perm_instances"):
        getattr(ctx, f).extend(getattr(s, f))


def diff_list(a, b, path, ctx):
    key = identity_key(a, b)
    if key:
        if ctx.collect and (len(a) != len(b) or any(ident(x[key]) != ident(y[key]) for x, y in zip(a, b))):
            ctx.switched.append({"path": path, "key": key, "new_rule": not (key in ID_KEYS_OLD or key.endswith(("Tag", "Id", "Name"))),
                                 "s1_len": len(a), "s2_len": len(b)})
        ia = {ident(e[key]): e for e in a}
        ib = {ident(e[key]): e for e in b}
        for i, e in ib.items():
            p = "%s[%s=%s]" % (path, key, i)
            if i in ia:
                diff_value(ia[i], e, p, ctx)
            else:
                ctx.add(p, "added", None, e)
        for i, e in ia.items():
            if i not in ib:
                ctx.add("%s[%s=%s]" % (path, key, i), "removed", e, None)
        oa = [i for i in ia if i in ib]
        ob = [i for i in ib if i in ia]
        if oa != ob:
            ctx.add(path, "resequenced", list(ia), list(ib))
        return
    if len(a) == len(b):
        if a != b and all(not isinstance(x, (dict, list)) for x in a + b) \
                and sorted(map(norm_text, a)) == sorted(map(norm_text, b)):
            ctx.add(path, "resequenced", a, b)
            return
        bad = [i for i, (x, y) in enumerate(zip(a, b)) if not deep_same(x, y)]
        if len(bad) > 1 and all(isinstance(a[i], dict) and isinstance(b[i], dict) for i in bad):
            ta = {i: leaves(a[i], "", {}) for i in bad}
            tb = {i: leaves(b[i], "", {}) for i in bad}
            bad = [i for i in bad if not leaves_same(ta[i], tb[i])]
            if len(bad) > 1 and any(leaves_same(ta[i], tb[j]) for i in bad for j in bad if i != j):
                s_idx, s_al = scratch_of(ctx), scratch_of(ctx)
                for i, (x, y) in enumerate(zip(a, b)):
                    diff_value(x, y, "%s[%d]" % (path, i), s_idx)
                align_unmatched(a, b, bad, bad, path, s_al)   # elements moved within the array
                merge_ctx(ctx, s_al if len(s_al.changes) < len(s_idx.changes) else s_idx)
                return
        for i, (x, y) in enumerate(zip(a, b)):
            diff_value(x, y, "%s[%d]" % (path, i), ctx)
        return
    # different length: trim common prefix/suffix, align the middle
    na, nb = [norm_text(x) for x in a], [norm_text(x) for x in b]
    lo = 0
    while lo < len(a) and lo < len(b) and na[lo] == nb[lo]:
        lo += 1
    ea, eb = len(a), len(b)
    while ea > lo and eb > lo and na[ea - 1] == nb[eb - 1]:
        ea -= 1
        eb -= 1
    ma, mb = na[lo:ea], nb[lo:eb]
    if len(ma) * len(mb) > 4_000_000:
        ops = [("replace", 0, len(ma), 0, len(mb))]
    else:
        ops = difflib.SequenceMatcher(None, ma, mb, autojunk=False).get_opcodes()
    ua = [lo + i for tag, i1, i2, j1, j2 in ops if tag != "equal" for i in range(i1, i2)]
    ub = [lo + j for tag, i1, i2, j1, j2 in ops if tag != "equal" for j in range(j1, j2)]
    if (ua or ub) and all(isinstance(a[i], dict) for i in ua) and all(isinstance(b[j], dict) for j in ub):
        align_unmatched(a, b, ua, ub, path, ctx)
        return
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        n = min(i2 - i1, j2 - j1) if tag == "replace" else 0
        for t in range(n):
            diff_value(a[lo + i1 + t], b[lo + j1 + t], "%s[%d]" % (path, lo + j1 + t), ctx)
        for i in range(i1 + n, i2):
            ctx.add("%s[%d]" % (path, lo + i), "removed", a[lo + i], None)
        for j in range(j1 + n, j2):
            ctx.add("%s[%d]" % (path, lo + j), "added", None, b[lo + j])


def reinterpreted(a, b):
    """One side int, the other float, and the int is the IEEE754 float32 bit pattern of the float."""
    if isinstance(a, float) and is_num(b) and isinstance(b, int):
        a, b = b, a
    if not (isinstance(a, int) and not isinstance(a, bool) and isinstance(b, float)):
        return False
    if not -0x80000000 <= a <= 0xFFFFFFFF:
        return False
    try:
        f = struct.unpack("<f", struct.pack("<I", a & 0xFFFFFFFF))[0]
    except struct.error:
        return False
    return math.isfinite(f) and same_scalar(f, b)


def diff_value(a, b, path, ctx):
    if isinstance(a, dict) and isinstance(b, dict):
        diff_dict(a, b, path, ctx)
    elif isinstance(a, list) and isinstance(b, list):
        diff_list(a, b, path, ctx)
    elif isinstance(a, (dict, list)) or isinstance(b, (dict, list)):
        ctx.add(path, "changed", a, b)
    elif not same_scalar(a, b):
        if reinterpreted(a, b):
            ctx.reinterp += 1   # int holding the float32 bit pattern of the float (old usmap typed it as int)
            return
        ctx.add(path, "changed", a, b)


def flatten(v, path, out):
    """Every leaf of v as a removed op (used for removed assets)."""
    if isinstance(v, dict) and v:
        for k, x in v.items():
            flatten(x, join(path, k), out)
    elif isinstance(v, list) and v:
        for i, x in enumerate(v):
            flatten(x, "%s[%d]" % (path, i), out)
    else:
        out.append({"path": path, "op": "removed", "before": v, "after": None})


# --- assets ---------------------------------------------------------------------------------------
def export_map(exports):
    """{(name, occurrence): obj} in file order."""
    seen = {}
    out = {}
    for hdr, obj in exports:
        name = obj.get("Name") if isinstance(obj, dict) else None
        if name is None:
            name = hdr
        n = seen.get(name, 0)
        seen[name] = n + 1
        out[(name, n)] = obj
    return out


def main_type(path, exports):
    base = os.path.splitext(os.path.basename(path))[0]
    for _h, o in exports:
        if o.get("Name") == base:
            return o.get("Type")
    return exports[0][1].get("Type") if exports else None


def classify(path, exports):
    for rx, area in AREA_RULES:
        if rx.search(path):
            if area == "engine-tooling-data" and "/UI/" in path \
                    and any("Rows" in o for _h, o in exports):
                return "data-tables-tags"
            return area
    return "engine-tooling-data"


def asset_ids(exports):
    """Identifying ids: every <X>Id property whose value is a gameplay tag, from the main exports."""
    out = set()
    for _h, o in exports:
        props = o.get("Properties") if isinstance(o, dict) else None
        if isinstance(props, dict):
            for k, v in props.items():
                if k.endswith("Id") and isinstance(v, dict) and isinstance(v.get("TagName"), str) \
                        and v["TagName"] not in ("", "None"):
                    out.add((k, v["TagName"]))
    return out


def prefixed(name, multi, path):
    return "%s::%s" % (name, path) if multi else path


def diff_assets(ex1, ex2, collect=False):
    ctx = Ctx()
    ctx.collect = collect
    m1, m2 = export_map(ex1), export_map(ex2)
    multi = len(m1) > 1 or len(m2) > 1
    # exports renamed with their asset (DA_Mosin_Stats -> DA_WEPN_017_Stats): pair leftovers in order by Type
    left1 = [k for k in m1 if k not in m2]
    left2 = [k for k in m2 if k not in m1]
    alias = {}
    for k2 in left2:
        for k1 in left1:
            if m1[k1].get("Type") == m2[k2].get("Type"):
                alias[k2] = k1
                left1.remove(k1)
                break
    for key, o2 in m2.items():
        pre = key[0] if key[1] == 0 else "%s#%d" % key
        if key in m1 or key in alias:
            o1 = m1[alias.get(key, key)]
            sub = Ctx()
            sub.collect = collect
            diff_value(o1, o2, "", sub)
            for c in sub.changes:
                c["path"] = prefixed(pre, multi, c["path"])
                ctx.changes.append(c)
            ctx.renamed += sub.renamed
            ctx.shifts += sub.shifts
            ctx.dups += sub.dups
            ctx.swapped += sub.swapped
            ctx.reinterp += sub.reinterp
            for pi in sub.perm_instances:
                pi["parent"] = prefixed(pre, multi, pi["parent"])
                ctx.perm_instances.append(pi)
            for sp in sub.swaps:
                sp["parent"] = prefixed(pre, multi, sp["parent"])
                ctx.swaps.append(sp)
            for sw in sub.switched:
                sw["path"] = prefixed(pre, multi, sw["path"])
                ctx.switched.append(sw)
            for cd in sub.cands:
                cd["parent"] = prefixed(pre, multi, cd["parent"])
                ctx.cands.append(cd)
        else:
            ctx.add(pre if multi else "", "added", None, o2)
    for key, o1 in m1.items():
        if key not in m2 and key not in alias.values():
            ctx.add(key[0] if key[1] == 0 else "%s#%d" % key, "removed", o1, None)
    return ctx


def accept_rename(old, new):
    """Accept a git rename only if the file names agree after replacing the old content folder name."""
    def folder(p):
        parts = p.split("/")
        return parts[parts.index("Content") - 1] if "Content" in parts and parts.index("Content") > 0 else None
    fo, fn = folder(old), folder(new)
    bo, bn = os.path.basename(old), os.path.basename(new)
    do, dn = old.split("/")[:-1], new.split("/")[:-1]
    if len(do) == len(dn) and sum(x != y for x, y in zip(do, dn)) == 1             and os.path.commonprefix([bo, bn]) .__len__() >= 8:
        return True   # same place, one folder renamed (Flares -> Countermeasures), names share a stem
    if bo == bn:
        return fo != fn
    return bool(fo and fn and fo != fn and bo.replace(fo, fn) == bn)


def build(s1_dir, s2_dir, log=print):
    files1, files2 = list_json(s1_dir), list_json(s2_dir)
    common = sorted(set(files1) & set(files2))
    removed = sorted(set(files1) - set(files2))
    added = sorted(set(files2) - set(files1))
    assets = []   # dicts with extra private keys "_area"
    stats = {"identical": 0, "unparsed": [], "dup_objects": 0, "paired": {}}

    def parsed(full):
        text = read_file(full)
        ex, err = parse_exports(text)
        return ex, err

    def make(name, path, old_path, status, typ, paired, changes, noise, area, **extra):
        a = {"name": name, "path": path, "old_path": old_path, "status": status, "type": typ,
             "paired_by": paired, "changes": changes, "noise": noise}
        a.update(extra)
        a["_area"] = area
        return a

    # modified (same path)
    for rel in common:
        t1, t2 = read_file(files1[rel]), read_file(files2[rel])
        if t1 == t2:
            stats["identical"] += 1
            continue
        ex1, err1 = parse_exports(t1)
        ex2, err2 = parse_exports(t2)
        name = os.path.splitext(os.path.basename(rel))[0]
        if err1 or err2:
            stats["unparsed"].append((rel, err1 or err2))
            assets.append(make(name, rel, None, "modified", main_type(rel, ex2), None, [],
                               {"renamed_keys": 0, "ref_shifts": 0, "dup_keys": 0, "swapped_keys": 0, "type_reinterpret": 0}, classify(rel, ex2),
                               note="not compared: " + (("Season 1 file is truncated in the source commit (%s)" % err1)
                                                         if err1 else ("Season 2 " + err2))))
            continue
        ctx = diff_assets(ex1, ex2, CANDS is not None)
        for cd in ctx.cands:
            CANDS.append(dict(asset=name, path=rel, **cd))
        for pi in ctx.perm_instances:
            PERM_INSTANCES.append(dict(asset=name, path=rel, **pi))
        for sp in ctx.swaps:
            SWAPS.append(dict(asset=name, path=rel, **sp))
        for sw in ctx.switched:
            SWITCHED.append(dict(asset=name, file=rel, **sw))
        if not ctx.changes and not ctx.renamed and not ctx.shifts and not ctx.dups and not ctx.swapped and not ctx.reinterp:
            # equal up to formatting or float noise only
            stats["identical"] += 1
            continue
        assets.append(make(name, rel, None, "modified", main_type(rel, ex2), None, ctx.changes,
                           {"renamed_keys": ctx.renamed, "ref_shifts": ctx.shifts, "dup_keys": ctx.dups, "swapped_keys": ctx.swapped, "type_reinterpret": ctx.reinterp}, classify(rel, ex2)))

    # moved
    pairs = []   # (old, new, paired_by)
    rem_left, add_left = set(removed), set(added)
    by_name = {}
    for p in sorted(add_left):
        by_name.setdefault(os.path.basename(p), []).append(p)
    for p in sorted(rem_left):
        cands = by_name.get(os.path.basename(p), [])
        if len(cands) == 1 and sum(1 for q in rem_left if os.path.basename(q) == os.path.basename(p)) == 1:
            pairs.append((p, cands[0], "same-name"))
    for old, new, _b in pairs:
        rem_left.discard(old)
        add_left.discard(new)
    rejected = []
    for old, new in GIT_RENAMES:
        if old in rem_left and new in add_left:
            if accept_rename(old, new):
                pairs.append((old, new, "git-rename"))
                rem_left.discard(old)
                add_left.discard(new)
            else:
                rejected.append((old, new))
    # inferred by identifying id
    ids_new = {}
    for p in sorted(add_left):
        ex, err = parsed(files2[p])
        for i in asset_ids(ex):
            ids_new.setdefault((main_type(p, ex), i), []).append(p)
    ids_old = {}
    for p in sorted(rem_left):
        ex, err = parsed(files1[p])
        for i in asset_ids(ex):
            ids_old.setdefault((main_type(p, ex), i), []).append(p)
    for key, olds in sorted(ids_old.items()):
        news = ids_new.get(key, [])
        if len(olds) == 1 and len(news) == 1 and olds[0] in rem_left and news[0] in add_left:
            pairs.append((olds[0], news[0], "inferred"))
            rem_left.discard(olds[0])
            add_left.discard(news[0])
    for old, new, how in sorted(pairs, key=lambda t: t[1]):
        ex1, err1 = parsed(files1[old])
        ex2, err2 = parsed(files2[new])
        name = os.path.splitext(os.path.basename(new))[0]
        if err1 or err2:
            stats["unparsed"].append((new, err1 or err2))
            ctx = Ctx()
        else:
            ctx = diff_assets(ex1, ex2, CANDS is not None)
        stats["paired"][new] = (old, how)
        assets.append(make(name, new, old, "moved", main_type(new, ex2), how, ctx.changes,
                           {"renamed_keys": ctx.renamed, "ref_shifts": ctx.shifts, "dup_keys": ctx.dups, "swapped_keys": ctx.swapped, "type_reinterpret": ctx.reinterp}, classify(new, ex2)))
    stats["rejected_renames"] = rejected

    # added
    for rel in sorted(add_left):
        ex2, err2 = parsed(files2[rel])
        name = os.path.splitext(os.path.basename(rel))[0]
        assets.append(make(name, rel, None, "added", main_type(rel, ex2), None, [],
                           {"renamed_keys": 0, "ref_shifts": 0, "dup_keys": 0, "swapped_keys": 0, "type_reinterpret": 0}, classify(rel, ex2), exports=len(ex2)))
    # removed
    for rel in sorted(rem_left):
        ex1, err1 = parsed(files1[rel])
        name = os.path.splitext(os.path.basename(rel))[0]
        out = []
        multi = len(ex1) > 1
        for key, o in export_map(ex1).items():
            pre = key[0] if key[1] == 0 else "%s#%d" % key
            flatten(o, pre if multi else "", out)
        assets.append(make(name, rel, None, "removed", main_type(rel, ex1), None, out,
                           {"renamed_keys": 0, "ref_shifts": 0, "dup_keys": 0, "swapped_keys": 0, "type_reinterpret": 0}, classify(rel, ex1)))
    # Config check
    stats["config_same"] = config_same(s1_dir, s2_dir)
    return assets, stats


def config_same(s1_dir, s2_dir):
    def inis(root):
        out = {}
        for d, _dirs, files in os.walk(root):
            for f in files:
                if f.endswith(".ini"):
                    full = os.path.join(d, f)
                    with open(full, "rb") as fh:
                        out[os.path.relpath(full, root).replace(os.sep, "/")] = fh.read()
        return out
    return inis(s1_dir) == inis(s2_dir)


# --- output ---------------------------------------------------------------------------------------
def dumps(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def count_changes(a):
    return 0 if a["status"] in ("added", "removed") else len(a["changes"])


def render(assets):
    """Return {filename: text}."""
    files = {}
    index_areas = []
    totals = {"assets_added": 0, "assets_removed": 0, "assets_modified": 0, "assets_moved": 0,
              "noise_only_assets": 0, "property_changes": 0, "removed_values": 0,
              "noise_renamed_keys": 0, "noise_ref_shifts": 0, "noise_dup_keys": 0, "noise_swapped_keys": 0, "noise_type_reinterpret": 0}
    for aid, title in AREAS:
        mine = [a for a in assets if a["_area"] == aid]
        mine.sort(key=lambda a: (STATUS_ORDER[a["status"]], a["name"].lower(), a["path"]))
        counts = {"added": 0, "removed": 0, "modified": 0, "moved": 0, "property_changes": 0, "removed_values": 0}
        for a in mine:
            counts[a["status"]] += 1
            counts["property_changes"] += count_changes(a)
            if a["status"] == "removed":
                counts["removed_values"] += len(a["changes"])
            if a["status"] == "modified" and not a["changes"] and (a["noise"]["renamed_keys"] or a["noise"]["ref_shifts"] or a["noise"]["dup_keys"] or a["noise"]["swapped_keys"] or a["noise"]["type_reinterpret"]):
                totals["noise_only_assets"] += 1
            totals["noise_renamed_keys"] += a["noise"]["renamed_keys"]
            totals["noise_ref_shifts"] += a["noise"]["ref_shifts"]
            totals["noise_dup_keys"] += a["noise"]["dup_keys"]
            totals["noise_swapped_keys"] += a["noise"]["swapped_keys"]
            totals["noise_type_reinterpret"] += a["noise"]["type_reinterpret"]
        lines = [dumps({k: v for k, v in a.items() if not k.startswith("_")}) for a in mine]
        # split if too big
        chunks, cur, size = [], [], 0
        for ln in lines:
            if cur and size + len(ln.encode("utf-8")) > SPLIT_BYTES:
                chunks.append(cur)
                cur, size = [], 0
            cur.append(ln)
            size += len(ln.encode("utf-8")) + 2
        chunks.append(cur)
        names = []
        for n, chunk in enumerate(chunks, 1):
            fname = "%s.json" % aid if len(chunks) == 1 else "%s-%d.json" % (aid, n)
            names.append(fname)
            files[fname] = '{"area":%s,"assets":[\n%s\n]}\n' % (dumps(aid), ",\n".join(chunk))
        index_areas.append({"id": aid, "title": title, "file": names[0] if len(names) == 1 else names, "counts": counts})
        totals["assets_added"] += counts["added"]
        totals["assets_removed"] += counts["removed"]
        totals["assets_modified"] += counts["modified"]
        totals["assets_moved"] += counts["moved"]
        totals["property_changes"] += counts["property_changes"]
        totals["removed_values"] += counts["removed_values"]
    index = {
        "from": {"label": "Season 1", "source": "bea446b"},
        "to": {"label": "Season 2", "build": "++Wardogs+Live-CL-516586", "date": "2026-10-15"},
        "generated_by": GENERATED_BY,
        "totals": totals,
        "areas": index_areas,
    }
    files["index.json"] = json.dumps(index, ensure_ascii=False, indent=1) + "\n"
    return files


def existing(out_dir):
    out = {}
    if os.path.isdir(out_dir):
        for f in os.listdir(out_dir):
            if f.endswith(".json"):
                with open(os.path.join(out_dir, f), encoding="utf-8", newline="") as fh:
                    out[f] = fh.read().replace(chr(13) + chr(10), chr(10))   # git autocrlf may rewrite line endings
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--s1", default=S1_DEFAULT)
    ap.add_argument("--s2", default=S2_DEFAULT)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--swaps", metavar="FILE", help="write the suppressed swapped-key cycles")
    ap.add_argument("--switched", metavar="FILE", help="write arrays whose index alignment would have misaligned identities")
    ap.add_argument("--named-candidates", metavar="FILE", help="also write report-only named-to-named rename candidates")
    args = ap.parse_args(argv)
    global CANDS
    CANDS = [] if (args.named_candidates or args.switched or args.swaps) else None
    global OBS_ON
    OBS_ON = True                      # pass 1: learn the per-schema key permutations from exact cycles
    build(args.s1, args.s2)
    del LEARNED[:]
    learned, refused = learn(OBSERVED)
    LEARNED.extend(learned)
    OBS_ON = False
    for lst in (SWAPS, KEPT_MINMAX, SWITCHED, PERM_INSTANCES, UNAFFECTED, OBSERVED):
        del lst[:]
    if CANDS is not None:
        del CANDS[:]
    assets, stats = build(args.s1, args.s2)   # pass 2: apply them
    if args.swaps:
        with open(args.swaps.replace(".json", "_permutations.json"), "w", encoding="utf-8") as fh:
            json.dump({"learned": learned,
                       "refused": refused, "instances_renamed": PERM_INSTANCES,
                       "unaffected_instances": UNAFFECTED}, fh, ensure_ascii=False, indent=1)
        with open(args.swaps, "w", encoding="utf-8") as fh:
            json.dump(SWAPS, fh, ensure_ascii=False, indent=1)
        with open(args.swaps.replace(".json", "_kept_minmax.json"), "w", encoding="utf-8") as fh:
            json.dump(KEPT_MINMAX, fh, ensure_ascii=False, indent=1)
    if args.switched:
        with open(args.switched, "w", encoding="utf-8") as fh:
            json.dump(SWITCHED, fh, ensure_ascii=False, indent=1)
    if args.named_candidates:
        os.makedirs(os.path.dirname(os.path.abspath(args.named_candidates)), exist_ok=True)
        with open(args.named_candidates, "w", encoding="utf-8") as fh:
            json.dump(CANDS, fh, ensure_ascii=False, indent=1)
    files = render(assets)
    idx = json.loads(files["index.json"])
    t = idx["totals"]
    print("totals:", json.dumps(t))
    for a in idx["areas"]:
        print("  %-24s %s" % (a["id"], json.dumps(a["counts"])))
    print("identical files: %d; config .ini identical: %s" % (stats["identical"], stats["config_same"]))
    for rel, err in stats["unparsed"]:
        print("not compared:", rel, err)
    if args.stats:
        for new, (old, how) in sorted(stats["paired"].items()):
            print("paired[%s] %s -> %s" % (how, old, new))
        for old, new in stats["rejected_renames"]:
            print("rejected git rename:", old, "->", new)
        return 0
    if args.write:
        os.makedirs(args.out, exist_ok=True)
        for f in os.listdir(args.out):
            if f.endswith(".json") and f not in files:
                os.remove(os.path.join(args.out, f))
        for f, text in files.items():
            with open(os.path.join(args.out, f), "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
        for f, text in sorted(files.items()):
            print("wrote %s (%d bytes)" % (f, len(text.encode("utf-8"))))
    if args.check:
        have = existing(args.out)
        bad = sorted(f for f in set(files) | set(have) if files.get(f) != have.get(f))
        if bad:
            print("season-diff files differ:", ", ".join(bad))
            return 1
        print("season-diff files up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
