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
      middles fall back to index pairing.
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
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S1_DEFAULT = "E:/r22/s1/data"
S2_DEFAULT = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(ROOT, "assets", "data", "season-diff")
GENERATED_BY = "_tools/season_diff.py"
SPLIT_BYTES = 5 * 1024 * 1024
REL_TOL = 1e-6

HEADER = re.compile(r"^--- export: (.*?) ---\r?\n", re.M)
HASHED = re.compile(r"^_aaa[a-z]{10,}(?:_\$[0-9A-F]+\$_\$\d+\$)?$")
DUP_SUFFIX = re.compile(r"#\d+$")
INDEX_SUFFIX = re.compile(r"\.\d+$")
ID_KEYS = ("RowName", "Name", "Key", "Id", "ItemId", "Tag", "TagName", "GameplayTag", "ObjectName")

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
        if not isinstance(b, dict) or set(a) != set(b):
            return False
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

    def add(self, path, op, before, after):
        self.changes.append({"path": path, "op": op, "before": before, "after": after})


def unnamed(k):
    """A hashed name, or a Key#2 duplicate (Season 1 duplicate names were usmap artifacts)."""
    return bool(HASHED.match(k) or DUP_SUFFIX.search(k))


def match_renames(a, b, only_a, only_b, common_a, common_b):
    """Pair hashed keys with their named counterparts. Returns {old_key: new_key}."""
    pairs = {}
    used = set()
    # 1. identical values
    for ka in only_a:
        for kb in only_b:
            if kb in used:
                continue
            if (unnamed(ka) or unnamed(kb)) and deep_same(a[ka], b[kb]):
                pairs[ka] = kb
                used.add(kb)
                break
    # 2. same gap between common keys, same kind of value
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
        for ka, kb in zip(la, lb):
            if (unnamed(ka) or unnamed(kb)) and kind(a[ka]) == kind(b[kb]):
                pairs[ka] = kb
    return pairs


def kind(v):
    return "dict" if isinstance(v, dict) else "list" if isinstance(v, list) else "scalar"


def diff_dict(a, b, path, ctx):
    ka, kb = list(a), list(b)
    only_a = [k for k in ka if k not in b]
    only_b = [k for k in kb if k not in a]
    pairs = {}
    if only_a and only_b:
        common_a = [k for k in ka if k in b]
        common_b = [k for k in kb if k in a]
        pairs = match_renames(a, b, only_a, only_b, common_a, common_b)
    new_to_old = {v: k for k, v in pairs.items()}
    for k in kb:
        p = join(path, k)
        if k in a:
            va, vb = a[k], b[k]
            if k == "ObjectPath" and isinstance(va, str) and isinstance(vb, str) and va != vb:
                if ref_shift(va, vb, a, b):
                    ctx.shifts += 1
                    continue
            diff_value(va, vb, p, ctx)
        elif k in new_to_old:
            ctx.renamed += 1
            diff_value(a[new_to_old[k]], b[k], p, ctx)
        else:
            ctx.add(p, "added", None, b[k])
    for k in only_a:
        if k not in pairs:
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
    extra = [k for k in (a[0] if a else b[0]) if k not in ID_KEYS and k.endswith(("Tag", "Id", "Name"))]
    for key in ID_KEYS + tuple(extra):
        ok = True
        for lst in (a, b):
            ids = [ident(e.get(key)) if key in e else None for e in lst]
            if any(i is None for i in ids) or len(set(ids)) != len(ids):
                ok = False
                break
        if ok:
            return key
    return None


def diff_list(a, b, path, ctx):
    key = identity_key(a, b)
    if key:
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


def diff_value(a, b, path, ctx):
    if isinstance(a, dict) and isinstance(b, dict):
        diff_dict(a, b, path, ctx)
    elif isinstance(a, list) and isinstance(b, list):
        diff_list(a, b, path, ctx)
    elif isinstance(a, (dict, list)) or isinstance(b, (dict, list)):
        ctx.add(path, "changed", a, b)
    elif not same_scalar(a, b):
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


def diff_assets(ex1, ex2):
    ctx = Ctx()
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
            diff_value(o1, o2, "", sub)
            for c in sub.changes:
                c["path"] = prefixed(pre, multi, c["path"])
                ctx.changes.append(c)
            ctx.renamed += sub.renamed
            ctx.shifts += sub.shifts
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
                               {"renamed_keys": 0, "ref_shifts": 0}, classify(rel, ex2),
                               note="not compared: " + (("Season 1 file is truncated in the source commit (%s)" % err1)
                                                         if err1 else ("Season 2 " + err2))))
            continue
        ctx = diff_assets(ex1, ex2)
        if not ctx.changes and not ctx.renamed and not ctx.shifts:
            # equal up to formatting or float noise only
            stats["identical"] += 1
            continue
        assets.append(make(name, rel, None, "modified", main_type(rel, ex2), None, ctx.changes,
                           {"renamed_keys": ctx.renamed, "ref_shifts": ctx.shifts}, classify(rel, ex2)))

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
            ctx = diff_assets(ex1, ex2)
        stats["paired"][new] = (old, how)
        assets.append(make(name, new, old, "moved", main_type(new, ex2), how, ctx.changes,
                           {"renamed_keys": ctx.renamed, "ref_shifts": ctx.shifts}, classify(new, ex2)))
    stats["rejected_renames"] = rejected

    # added
    for rel in sorted(add_left):
        ex2, err2 = parsed(files2[rel])
        name = os.path.splitext(os.path.basename(rel))[0]
        assets.append(make(name, rel, None, "added", main_type(rel, ex2), None, [],
                           {"renamed_keys": 0, "ref_shifts": 0}, classify(rel, ex2), exports=len(ex2)))
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
                           {"renamed_keys": 0, "ref_shifts": 0}, classify(rel, ex1)))
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
              "noise_renamed_keys": 0, "noise_ref_shifts": 0}
    for aid, title in AREAS:
        mine = [a for a in assets if a["_area"] == aid]
        mine.sort(key=lambda a: (STATUS_ORDER[a["status"]], a["name"].lower(), a["path"]))
        counts = {"added": 0, "removed": 0, "modified": 0, "moved": 0, "property_changes": 0, "removed_values": 0}
        for a in mine:
            counts[a["status"]] += 1
            counts["property_changes"] += count_changes(a)
            if a["status"] == "removed":
                counts["removed_values"] += len(a["changes"])
            if a["status"] == "modified" and not a["changes"] and (a["noise"]["renamed_keys"] or a["noise"]["ref_shifts"]):
                totals["noise_only_assets"] += 1
            totals["noise_renamed_keys"] += a["noise"]["renamed_keys"]
            totals["noise_ref_shifts"] += a["noise"]["ref_shifts"]
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
                    out[f] = fh.read().replace("
", "
")   # git autocrlf may rewrite line endings
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--s1", default=S1_DEFAULT)
    ap.add_argument("--s2", default=S2_DEFAULT)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args(argv)
    assets, stats = build(args.s1, args.s2)
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
