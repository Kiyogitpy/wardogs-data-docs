"""Resolve Blueprint class defaults and write assets/data/bp-defaults.json (round 17).

A cooked Blueprint stores only the values that differ from its parent. Every value below is therefore
resolved up the chain  instance export -> Blueprint CDO (Default__X_C) -> parent Blueprint(s) -> native class:

  export          found on the named export (CDO or instance) of the named asset
  parent          not on the asset, found on a parent Blueprint (or the listed fallback asset)
  bp-default      a variable declared by the Blueprint itself that no export sets: the type default (0, false, empty)
  engine-default  an engine property left at its engine default (animation montage RateScale 1.0)
  native-pending  no Blueprint in the chain sets it; the value is the native class default (constructor). The
                  entry names the native class, property and SDK offset so the native constructor value can be
                  joined from the round 17 native defaults pass.

Montage values (SequenceLength, notify times, section starts) are read from the cooked AnimMontage exports.

Dumps come from the extractor (tools/cue4parse_extractor, `dump` mode) written OUTSIDE this repository:

    WdExtract <Paks> <keyfile> <usmap> <dumpdir> <oo2core> dump <files.txt>

Run (idempotent):

    python _tools/bp_defaults.py                 # read DUMP_DIR if it exists, rewrite assets/data/bp-defaults.json
    python _tools/bp_defaults.py --dump DIR      # another dump folder (searched recursively)
    python _tools/bp_defaults.py --check         # fail if the committed JSON differs from what would be written

If the dump folder is absent the committed JSON is left untouched (and, for importers, is the source).
Importers: `import bp_defaults as bpd; bpd.load()`, `bpd.get(topic, asset, prop)`.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "bp-defaults.json")
DUMP_DIR = "E:/Reverse_Engineer/wardogs_analysis/round17_bp_defaults_20261022"
# Round 86 dump: B_Action_*, placement conditions, Sniper Showdown components, spawner, Molotov Blueprints
# (WdExtract list/dump, see docs/evidence/round86-bp.md). Searched after DUMP_DIR; the first file of a name wins.
DUMP_DIR_R86 = "E:/r86/work/bp/dump1"
SDK_DIR = "E:/Reverse_Engineer/wardogs_analysis/CppSDK/SDK"

W = "Wardogs/"
PG = W + "Plugins/GameFeatures/Items/"

# ---------------------------------------------------------------------------------------------------------------
# Specs. Each: (topic, asset, property, options). Options:
#   kind     cdo (default) | len | rate | notify:<Name> | section:<Name>
#   etype    export Type to read instead of the CDO (instance fragments, components)
#   fallback assets to try next (after the asset's own Blueprint parent chain is not wanted first)
#   native   (native class, SDK offset) used when nothing in the chain sets the property
#   note     short free text
# ---------------------------------------------------------------------------------------------------------------
SPECS = []


def S(topic, asset, prop, **o):
    SPECS.append((topic, asset, prop, o))


# ---- Medical: item use montages (first-person) and notify times ------------------------------------------------
MED_MONTAGES = [
    "AM_FP_Bandage_Self_Heal", "AM_FP_Bandage_Teammate_Heal", "AM_FP_IFAK_Self_Heal", "AM_FP_IFAK_Teammate_Heal",
    "AM_FP_Medkit_Use", "AM_FP_Medkit_Use_Self", "AM_FP_Enox_Use", "AM_FP_StimPen_Use", "AM_FP_StimPen_Use_Teammate",
    "AM_Resuscitator_Use", "AM_FP_Defib_Use", "AM_FP_Revive",
]
for m in MED_MONTAGES:
    S("medical", m, "SequenceLength", kind="len", unit="s")
    S("medical", m, "RateScale", kind="rate")
S("medical", "AM_FP_IFAK_Self_Heal", "Notify:Heal", kind="notify:Heal", unit="s")
S("medical", "AM_FP_IFAK_Teammate_Heal", "Notify:Heal", kind="notify:Heal", unit="s")
S("medical", "AM_FP_Revive", "Notify:Complete", kind="notify:Complete", unit="s")
for m, sec in (("AM_FP_Defib_Use", "LoopStart"), ("AM_FP_Defib_Use", "LoopEnd"), ("AM_FP_Medkit_Use", "LoopStart"),
               ("AM_FP_Medkit_Use", "LoopEnd"), ("AM_FP_Medkit_Use_Self", "LoopStart"), ("AM_FP_Medkit_Use_Self", "LoopEnd"),
               ("AM_FP_Enox_Use", "LoopStart"), ("AM_FP_Enox_Use", "LoopEnd")):
    S("medical", m, "Section:" + sec, kind="section:" + sec, unit="s")

# ---- Medical: defibrillator ------------------------------------------------------------------------------------
DEFIB_DATA = "BH_Defibrillator_WattsExtensionData"
for p in ("ChargeDuration", "BatteryChargesUsed", "Damage", "TraceDistance", "HitBoxSize"):
    S("medical", "ID_Defibrillator_Standard", p, etype=DEFIB_DATA + "_C", fallback=[DEFIB_DATA],
      unit="s" if p == "ChargeDuration" else "")
S("medical", "ID_Defibrillator_Standard", "AttributeValue", etype="WDItemExtensionData_Appliable",
  note="passed as the revive health: ReviveCharacter calls RevivePlayer(..., AttributeValue, ...)")

# ---- Medical: player character (bleed-out, revive) ------------------------------------------------------------
PC = "B_WDCore_MoverPlayerCharacter"
for p, off in (("BaseBleedOutTime", "0x0980"), ("MinBleedOutTime", "0x0984"), ("BleedOutRevivePenaltyOffset", "0x0988"),
               ("DefaultBleedOutRate", "0x098C"), ("HoldOnBleedOutRate", "0x0990"), ("GiveUpBleedOutRate", "0x0994")):
    S("medical", PC, p, native=("AWDMoverCharacter", off), unit="" if "Rate" in p or "Offset" in p else "s")
S("medical", PC, "CriticalReviveHoldThreshold", native=("AWDMoverCharacter", "0x0970"))
VC = "WDCharacterVitalityComponent"
for p, off in (("DefaultHealthToReviveTo", "0x0160"), ("MaxOverhealHealth", "0x0164"), ("MaxDecayHealth", "0x0168"),
               ("DecayRate", "0x016C"), ("DecayMagnitude", "0x0170")):
    S("medical", PC, p, etype=VC, native=("UWDCharacterVitalityComponent", off), note="VitalityComponent subobject")
for p, off in (("MaxHealth", "0x0134"), ("RegenDelay", "0x0138")):
    S("medical", PC, p, etype=VC, native=("UWDVitalityComponent", off), note="VitalityComponent subobject")
S("medical", "B_Action_Revive", "ReviveHoldTime", unit="s")

# ---- Fire, smoke, throwing and mines ---------------------------------------------------------------------------
AT = "BH_AT_MineExtensionData"
for p in ("ArmingDelay", "TraceCheckTime", "DetectFriendlyVehicles", "PerVehicleSpeedListDetection", "UniversalVehicleSpeed"):
    S("fire_utility", "ID_AT_Mine", p, etype=AT + "_C", fallback=[AT], unit="s" if p in ("ArmingDelay", "TraceCheckTime") else "")
CM = "BH_ClaymoreExtensionData"
for p in ("ActivationDelayTimer", "ShouldDetectVehicle?", "DetectFriendlyTeammates?"):
    S("fire_utility", "ID_Claymore", p, etype=CM + "_C", fallback=[CM], unit="s" if p == "ActivationDelayTimer" else "")
S("fire_utility", "ID_Claymore", "TriggerBoxExtends", etype=CM + "_C", fallback=[CM])
S("fire_utility", "ID_C4_Trigger", "DelayTillExplosion", etype="BH_C4_Data_C", fallback=["BH_C4_Data"], unit="s")
S("fire_utility", "ID_C4_Trigger", "MaxDetonationDistance", etype="BH_C4_Data_C", fallback=["BH_C4_Data"])
S("fire_utility", "ID_IED_Trigger", "DelayTillExplosion", etype="BH_C4_Data_C", fallback=["BH_C4_Data"], unit="s")
S("fire_utility", "B_ThrowableC4", "TimerBeforeExplosion", unit="s")
S("fire_utility", "B_ThrowableC4", "MaxDetonationDistance")
S("fire_utility", "B_ThrowableIED", "TimerBeforeExplosion", unit="s")
COLOURS = ("White", "Black", "Blue", "Green", "Orange", "Purple", "Red", "Yellow")
for c in COLOURS:
    S("fire_utility", "B_SmokeGrenade_" + c, "BaseFuseTime", unit="s", native=("AWDGrenade", "0x0620"))
    S("fire_utility", "DA_SmokeGrenade_" + c, "Total Duration", fallback=["PDA_SmokeGrenade"], unit="s")
    S("fire_utility", "DA_SmokeGrenade_" + c, "SpriteMaxSize", fallback=["PDA_SmokeGrenade"])
S("fire_utility", "B_SmokeGrenade_White", "PostExplodeLifespan", unit="s", native=("AWDExplosive", "0x4B4"))
S("fire_utility", "B_WorldSmokeGrenade_White", "InitialLifeSpan", unit="s")
S("fire_utility", "B_WorldSmokeGrenade_Red", "InitialLifeSpan", unit="s")
for p in ("Fade In Time", "Fade Out Time", "Diameter"):
    S("fire_utility", "PDA_SmokeGrenade", p, unit="s" if "Time" in p else "")
for p, off in (("Density", None), ("Height", None), ("SphereTraceRadius", "0x2B8"), ("WallHitPosOffset", "0x2BC"),
               ("OriginOffset", None)):
    S("fire_utility", "BP_SmokeGrenadeVFX", p, native=("AWDSmokeGrenadeVFXActor", off) if off else None)
S("fire_utility", "B_Molotov", "BaseFuseTime", unit="s", native=("AWDGrenade", "0x0620"))
S("fire_utility", "B_Molotov", "bCanBeCooked", native=("AWDGrenade", "0x0624"))
for p, off in (("_aaaamejojopeijafgdjkf", "0x670"), ("_aaaakffacidhmniagfchm", "0x674"), ("_aaaakmpdngpdcdjfoghgn", "0x678"),
               ("_aaabefnnihkojobdfojbk", "0x67C"), ("_aaaamiahcncilelhidghh", "0x680"), ("_aaabclpkjcpbbjcpncgfa", "0x684")):
    S("fire_utility", "B_Molotov", p, native=("AWDMolotovGrenade", off),
      note="obfuscated AWDMolotovGrenade field at +" + off[2:] + "; meaning not decoded")
for p in ("FlatPlayerDamage", "FlatVehicleDamage", "InitialLifeSpan"):
    S("fire_utility", "B_Molotov_FireField", p, unit="s" if p == "InitialLifeSpan" else "")
for p, off in (("_aaaalampbnfacakccbbcd", "0x2D0"), ("_aaabdgioabebpkhhmcglm", "0x2D4"), ("_aaabknhhcfikfkdfeephh", "0x2D8"),
               ("_aaabakopnbgagdbajfflp", "0x2DC")):
    S("fire_utility", "B_Molotov_FireField", p, native=("AWDMolotovFireField", off),
      note="obfuscated AWDMolotovFireField field at +" + off[2:] + "; meaning not decoded")
S("fire_utility", "B_Molotov_TriggerVolume", "InitialLifeSpan", unit="s")
for p, off in (("Duration", "0x0030"), ("MaxStacks", "0x0034"), ("StackDurationRefreshPolicy", "0x0036")):
    S("fire_utility", "GE_MolotovBurning", p, native=("UBHGameplayEffect", off),
      note="burning tag duration after leaving the fire; the Blueprint effect sets only GrantedTags")

# ---- Explosives: fuses -----------------------------------------------------------------------------------------
S("explosives", "B_FragGrenade", "BaseFuseTime", unit="s", native=("AWDGrenade", "0x0620"))
S("explosives", "B_FragGrenade", "bCanBeCooked", native=("AWDGrenade", "0x0624"))
S("explosives", "B_FragGrenade", "bCanThrowBack")
S("explosives", "B_FragGrenade", "GrenadeInteractionData")
S("explosives", "B_GoldFragGrenade", "BaseFuseTime", unit="s", native=("AWDGrenade", "0x0620"))
S("explosives", "B_Molotov", "BaseFuseTime", unit="s", native=("AWDGrenade", "0x0620"))
S("explosives", "B_SmokeGrenade_Red", "BaseFuseTime", unit="s", native=("AWDGrenade", "0x0620"))
S("explosives", "B_ThrowableC4", "TimerBeforeExplosion", unit="s")
S("explosives", "B_ThrowableIED", "TimerBeforeExplosion", unit="s")
S("explosives", "ID_C4_Trigger", "DelayTillExplosion", etype="BH_C4_Data_C", fallback=["BH_C4_Data"], unit="s")
S("explosives", "ID_IED_Trigger", "DelayTillExplosion", etype="BH_C4_Data_C", fallback=["BH_C4_Data"], unit="s")
S("explosives", "ID_AT_Mine", "ArmingDelay", etype=AT + "_C", fallback=[AT], unit="s")
S("explosives", "ID_Claymore", "ActivationDelayTimer", etype=CM + "_C", fallback=[CM], unit="s")

# ---- Item actions: use, throw and place montages ---------------------------------------------------------------
THROW = ["AM_FP_Grenade_Throw_Overhand", "AM_FP_Grenade_Throw_Underhand", "AM_FP_Grenade_Throw_It_Back",
         "AM_FP_SmokeGrenade_Throw_Overarm", "AM_FP_SmokeGrenade_Throw_Underarm", "AM_FP_Molotov_Throw_Overarm",
         "AM_FP_Molotov_Throw_Underarm", "AM_FP_C4_Throw"]
for m in THROW:
    S("item_actions", m, "SequenceLength", kind="len", unit="s")
    S("item_actions", m, "RateScale", kind="rate")
    for nm in ("Prime", "Ready", "Throw", "Complete"):
        S("item_actions", m, "Notify:" + nm, kind="notify:" + nm, unit="s")
    S("item_actions", m, "Section:LoopStart", kind="section:LoopStart", unit="s")
    S("item_actions", m, "Section:LoopEnd", kind="section:LoopEnd", unit="s")
for m, nm in (("AM_FP_AT_Mine_Place", "Activate"), ("AM_FP_Claymore_Deploy", "Activate"), ("AM_FP_IED_Plant", "Activate"),
              ("AM_FP_IED_Dial_and_Ring", "Ring"), ("AM_FP_IED_Dial_and_Ring", "Discard")):
    S("item_actions", m, "SequenceLength", kind="len", unit="s")
    S("item_actions", m, "RateScale", kind="rate")
    S("item_actions", m, "Notify:" + nm, kind="notify:" + nm, unit="s")
S("item_actions", "AM_FP_C4_Use", "SequenceLength", kind="len", unit="s")
S("item_actions", "AM_FP_C4_Use", "RateScale", kind="rate")
for m in MED_MONTAGES:
    S("item_actions", m, "SequenceLength", kind="len", unit="s")
    S("item_actions", m, "RateScale", kind="rate")
for m, nm in (("AM_FP_IFAK_Self_Heal", "Heal"), ("AM_FP_IFAK_Self_Heal", "Activate"), ("AM_FP_IFAK_Teammate_Heal", "Heal"),
              ("AM_FP_Revive", "Complete")):
    S("item_actions", m, "Notify:" + nm, kind="notify:" + nm, unit="s")
for m, sec in (("AM_FP_Defib_Use", "LoopStart"), ("AM_FP_Defib_Use", "LoopEnd"), ("AM_FP_Medkit_Use", "LoopStart"),
               ("AM_FP_Medkit_Use", "LoopEnd"), ("AM_FP_Medkit_Use_Self", "LoopStart"), ("AM_FP_Medkit_Use_Self", "LoopEnd"),
               ("AM_FP_Enox_Use", "LoopStart"), ("AM_FP_Enox_Use", "LoopEnd")):
    S("item_actions", m, "Section:" + sec, kind="section:" + sec, unit="s")
S("item_actions", "B_Action_Appliable_Base", "AppliableContainerData")
S("item_actions", "B_Action_ThrowExplosive", "BaseFuseTime", unit="s")

# ---- Buildables: hammers ---------------------------------------------------------------------------------------
HAMMER_USE = {"Large": "AM_FP_Large_Hammer_Use", "Medium": "AM_FP_BuildTool_Use", "Small": "AM_FP_Small_Hammer_Use"}
for size, m in HAMMER_USE.items():
    S("buildables", m, "SequenceLength", kind="len", unit="s")
    S("buildables", m, "RateScale", kind="rate")
    S("buildables", m, "Notify:Hit", kind="notify:Hit", unit="s")
    S("buildables", m, "Section:LoopStart", kind="section:LoopStart", unit="s")
    S("buildables", m, "Section:LoopEnd", kind="section:LoopEnd", unit="s")
    S("buildables", "ID_%sHammer" % size, "BuildAmount", etype="WDItemExtensionData_BuildTool")
    S("buildables", "ID_%sHammer" % size, "BuildAmountWhenTargetIsHit", etype="WDItemExtensionData_CriticalHitSpotManager")
    S("buildables", "ID_%sHammer" % size, "DismantleRatePerSecond", etype="WDItemExtensionData_BuildableDismantle")
    S("buildables", "ID_%sHammer" % size, "DismantleRatePerHit", etype="WDItemExtensionData_BuildableDismantle")


# ---- Round 86: action Blueprints, placement conditions, Sniper Showdown components ------------------------------
# Hold times, cancel flags and thresholds that live on the B_Action_* Blueprint class defaults (the logic is in
# docs/evidence/round86-bp.md). Topic "actions".
for a, props in (
    ("B_Action_ForceOpenDoor", ("ForceOpenDoorHoldTime", "ForceOpenGateHoldTime", "DurabilityCost", "bCancelOnTargetLost")),
    ("B_Action_ForceUnlockVehicle", ("ForceOpenDoorHoldTime", "DurabilityCost", "bCancelOnTargetLost")),
    ("B_Action_Melee", ("MeleeAction",)),
    ("B_Action_Stance_Base", ("SubmersionTolerance",)),
    ("B_Action_Mantling", ("HolsterHeight",)),
    ("B_Action_StimPen", ("DecayAmount_0", "ReviveHealth")),
    ("B_Action_MedKit_MultiUse", ("SimulatedReviveHealthTimer", "bCancelOnTargetLost")),
    ("B_Action_Bandage_Use", ("bCancelOnTargetLost",)),
    ("B_Action_Enox_Use", ("bCancelOnTargetLost",)),
    ("B_Action_FuelCan_Refuel", ("bCancelOnTargetLost",)),
    ("B_Action_Resuscitator", ("bCancelOnTargetLost",)),
    ("B_Action_VehicleRepairTool", ("bCancelOnTargetLost",)),
    ("B_Action_ChamberWeapon", ("bCanActivateDuringItemEquippingOnServer",)),
    ("B_Action_Defibrillator", ("bCanActivateDuringItemEquippingOnServer",)),
    ("B_Action_Vehicle_Reload", ("ReloadSetupData",)),
    ("B_Action_ThrowExplosive", ("ThrowSettings",)),
):
    for p in props:
        S("actions", a, p, unit="s" if "Time" in p or "Timer" in p else "")
# Placement conditions (topic "placement"): the two condition classes shared by buildables, mines, Claymore and IED.
S("placement", "B_SafeZonePlacementCondition", "MinDistanceToSafezone", unit="cm")
S("placement", "B_WithinLadderBoundsPlacementCondition", "BlockRadius", unit="cm")
# Sniper Showdown player components (topic "sniper_showdown").
for p in ("ExplosionDamageValues", "DamageEntityData", "ExplodeGameplayCueTag"):
    S("sniper_showdown", "B_SniperShowdown_ExplodeComponent", p)
S("sniper_showdown", "B_SniperShowdown_OOBComponent", "ItemsToStartWith")


# ---------------------------------------------------------------------------------------------------------------
def load(path=OUT):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get(topic, asset, prop, path=OUT, _cache={}):
    """Return the committed entry for (topic, asset, property) or None."""
    if path not in _cache:
        _cache[path] = {(e["topic"], e["asset"], e["property"]): e for e in load(path)["entries"]}
    return _cache[path].get((topic, asset, prop))


def topic_entries(topic, path=OUT):
    return [e for e in load(path)["entries"] if e["topic"] == topic]


def fmt(v):
    """Compact text for a value (used by the page generators)."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return ("%.4f" % v).rstrip("0").rstrip(".")
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x) for x in v) + "]" if v else "[] (empty)"
    if isinstance(v, dict):
        return "(" + ", ".join(fmt(x) for x in v.values()) + ")"
    return str(v)


# ---------------------------------------------------------------------------------------------------------------
class Index:
    def __init__(self, roots):
        self.files = {}
        self._data = {}
        self.pkg = {}
        for root in ([roots] if isinstance(roots, str) else roots):
            for p in sorted(glob.glob(os.path.join(root, "**", "*.json"), recursive=True)):
                stem = os.path.basename(p)[:-5]
                if stem.startswith("_") or stem in ("manifest",):
                    continue
                self.files.setdefault(stem, p)
            for lf in glob.glob(os.path.join(root, "*.txt")):
                if os.path.basename(lf).startswith("t") and os.path.basename(lf)[1:2].isdigit():
                    for line in open(lf, encoding="utf-8"):
                        line = line.strip()
                        if line:
                            self.pkg.setdefault(line.rsplit("/", 1)[-1], line)

    def data(self, stem):
        if stem not in self.files:
            return None
        if stem not in self._data:
            with open(self.files[stem], encoding="utf-8") as f:
                self._data[stem] = json.load(f)
        return self._data[stem]

    def parent(self, stem):
        d = self.data(stem)
        for e in d or []:
            if e.get("Type") == "BlueprintGeneratedClass":
                s = (e.get("Super") or e.get("SuperStruct") or {}).get("ObjectName", "")
                m = re.match(r"(\w+)'(\w+)'", s)
                if not m:
                    return None, None
                kind, name = m.groups()
                if kind == "BlueprintGeneratedClass" and name.endswith("_C"):
                    return name[:-2], None
                return None, name
        return None, None


def declared(idx, stem, prop):
    d = idx.data(stem) or []
    for e in d:
        if e.get("Type") == "BlueprintGeneratedClass":
            for cp in e.get("ChildProperties", []):
                if cp.get("Name") == prop:
                    return cp.get("Type")
    return None


ZERO = {"DoubleProperty": 0.0, "FloatProperty": 0.0, "BoolProperty": False, "ArrayProperty": [], "IntProperty": 0}


def find_export(d, etype, stem=None):
    """Export carrying properties: by Type (instance/component), the data asset itself, or the class default object."""
    if etype is None:
        for e in d:
            if stem and e.get("Name") == stem and e.get("Properties") and not e.get("Type", "").endswith("Class"):
                return e
        for e in d:
            if e.get("Name", "").startswith("Default__") and "Properties" in e:
                return e
        return None
    for e in d:
        if e.get("Type") == etype and e.get("Properties"):
            return e
    for e in d:
        if e.get("Type") == etype:
            return e
    return None


def lookup(idx, stem, prop, etype, seen=None):
    """Walk stem and its Blueprint parents; return (value, found_in, how) or None."""
    chain = []
    cur = stem
    while cur:
        chain.append(cur)
        cur, _ = idx.parent(cur)
    for i, s in enumerate(chain):
        d = idx.data(s)
        if d is None:
            continue
        e = find_export(d, etype, s)
        if e is not None and prop in (e.get("Properties") or {}):
            return e["Properties"][prop], s, i
    return None


def montage_value(idx, stem, kind):
    d = idx.data(stem)
    if d is None:
        return None
    for e in d:
        if e.get("Type") == "AnimMontage":
            p = e["Properties"]
            if kind == "len":
                return round(p["SequenceLength"], 4)
            if kind == "rate":
                return p.get("RateScale", 1.0)
            if kind.startswith("notify:"):
                nm = kind.split(":", 1)[1]
                for n in p.get("Notifies", []):
                    if n.get("NotifyName") == nm:
                        return round(n.get("LinkValue", 0.0), 4)
                return None
            if kind.startswith("section:"):
                nm = kind.split(":", 1)[1]
                for s in p.get("CompositeSections", []):
                    if s.get("SectionName") == nm:
                        return round(s["SegmentBeginTime"], 4)
                return None
    return None


def resolve(idx, topic, asset, prop, o):
    kind = o.get("kind", "cdo")
    pkg = idx.pkg.get(asset, "")
    base = {"topic": topic, "asset": asset, "class": None, "property": prop, "package": pkg}
    if idx.data(asset) is None:
        return None
    if kind in ("len", "rate") or kind.startswith(("notify:", "section:")):
        v = montage_value(idx, asset, kind)
        if v is None and kind != "rate":
            return "skip"
        base.update(class_="AnimMontage")
        base["class"] = "AnimMontage"
        base["value"] = v
        base["resolved_from"] = "engine-default" if (kind == "rate" and v == 1.0 and not _montage_has_rate(idx, asset)) else "export"
        base["from_asset"] = asset
        return _finish(base, o)
    etype = o.get("etype")
    stems = [asset] + list(o.get("fallback", []))
    res = None
    for k, s in enumerate(stems):
        et = etype if k == 0 else (None if s != asset else etype)
        # fallback assets are class Blueprints: read their CDO
        r = lookup(idx, s, prop, et if k == 0 else None)
        if r is not None:
            res = (r, s, k)
            break
    # the class of the export that was read
    d = idx.data(asset)
    ex = find_export(d, etype, asset)
    base["class"] = (ex or {}).get("Type") or asset
    if res is not None:
        (value, found, depth), s, k = res
        base["value"] = value
        base["from_asset"] = found
        base["resolved_from"] = "export" if (k == 0 and depth == 0) else "parent"
        return _finish(base, o)
    # not set anywhere: Blueprint-declared variable -> type default; otherwise native
    for s in stems:
        chain, cur = [], s
        while cur:
            chain.append(cur)
            cur, _ = idx.parent(cur)
        for c in chain:
            t = declared(idx, c, prop)
            if t in ZERO:
                base["value"] = ZERO[t]
                base["from_asset"] = c
                base["resolved_from"] = "bp-default"
                return _finish(base, o)
    nat = o.get("native")
    if nat:
        base["value"] = None
        base["resolved_from"] = "native-pending"
        base["native_class"], base["sdk_offset"] = nat
        base["from_asset"] = None
        return _finish(base, o)
    return None


def _montage_has_rate(idx, stem):
    for e in idx.data(stem) or []:
        if e.get("Type") == "AnimMontage":
            return "RateScale" in e["Properties"]
    return False


def _finish(base, o):
    base.pop("class_", None)
    if o.get("native") and "native_class" not in base:
        base["native_class"], base["sdk_offset"] = o["native"]
    if o.get("unit"):
        base["unit"] = o["unit"]
    if o.get("note"):
        base["note"] = o["note"]
    order = ["topic", "asset", "class", "property", "value", "unit", "resolved_from", "from_asset", "native_class",
             "sdk_offset", "package", "note"]
    return {k: base[k] for k in order if k in base}


def sdk_check():
    """Optional: confirm the SDK offsets of the native-pending entries when the SDK dump is present."""
    out = []
    if not os.path.isdir(SDK_DIR):
        return out
    cache = {}
    for _, asset, prop, o in SPECS:
        nat = o.get("native")
        if not nat or nat[1] == "?":
            continue
        cls, off = nat
        found = None
        for fn in glob.glob(os.path.join(SDK_DIR, "*_classes.hpp")):
            if fn not in cache:
                cache[fn] = open(fn, encoding="utf-8", errors="ignore").read().split("\n")
            cur = None
            for line in cache[fn]:
                m = re.match(r"class (\w+)", line)
                if m:
                    cur = m.group(1)
                if cur == cls:
                    m = re.search(r"\s" + re.escape(prop) + r";\s+//\s+(0x[0-9A-Fa-f]+)", line)
                    if m:
                        found = m.group(1)
        if found is not None and int(found, 16) != int(off, 16):
            out.append((cls, prop, off, found))
    return out


def native_index():
    path = os.path.join(ROOT, "assets", "data", "native-defaults.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return {(e["class"], int(e["offset"], 16)): e for e in json.load(f)["entries"]}


def join_native(entries):
    """Attach the native constructor default (assets/data/native-defaults.json) to every entry that names a native
    class. A native-pending entry whose value is found there becomes resolved_from 'native'."""
    nd = native_index()
    for e in entries:
        if "sdk_offset" not in e:
            continue
        n = nd.get((e["native_class"], int(e["sdk_offset"], 16))) if e["sdk_offset"] != "?" else None
        if n is None:
            continue
        e["native_default"] = n["value"]
        e["native_ctor_rva"] = n["ctor_rva"]
        if e["resolved_from"] == "native-pending":
            e["value"] = n["value"]
            e["resolved_from"] = "native"


def build(dump):
    idx = Index(dump)
    entries, missing = [], []
    for topic, asset, prop, o in SPECS:
        e = resolve(idx, topic, asset, prop, o)
        if e == "skip":
            continue
        if e is None:
            missing.append((topic, asset, prop))
        else:
            entries.append(e)
    join_native(entries)
    entries.sort(key=lambda e: (e["topic"], e["asset"], e["property"]))
    return entries, missing


def main():
    args = sys.argv[1:]
    dump = [DUMP_DIR, DUMP_DIR_R86]
    if "--dump" in args:
        dump = [args[i + 1] for i, a in enumerate(args) if a == "--dump"]
    for d in dump:
        if not os.path.isdir(d):
            print("dump folder absent (%s): keeping the committed %s" % (d, os.path.relpath(OUT, ROOT)))
            return 0
    entries, missing = build(dump)
    doc = {
        "meta": {
            "source": "Blueprint class defaults and montage values exported with tools/cue4parse_extractor (dump mode), "
                      "resolved up the parent chain by _tools/bp_defaults.py (round 17)",
            "resolved_from": {
                "export": "set on the named export",
                "parent": "set on a parent Blueprint or the class Blueprint behind an item instance",
                "bp-default": "declared by a Blueprint, never set: type default",
                "engine-default": "engine property left at its engine default",
                "native": "not set by any Blueprint: the native constructor default from assets/data/native-defaults.json (native_ctor_rva)",
                "native-pending": "not set by any Blueprint and not in native-defaults.json",
            },
            "count": len(entries),
        },
        "entries": entries,
    }
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if "--check" in args:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("up to date" if cur == text else "DIFFERS")
        return 0 if cur == text else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    by = {}
    for e in entries:
        by[e["resolved_from"]] = by.get(e["resolved_from"], 0) + 1
    print("wrote %d entries: %s" % (len(entries), ", ".join("%s %d" % kv for kv in sorted(by.items()))))
    for m in missing:
        print("UNRESOLVED", *m)
    for m in sdk_check():
        print("SDK offset mismatch", *m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
