"""Tables for fire, smoke, throw mechanics, placement and trigger data of throwables, mines and detonators.

Sources (exported JSON under data/Wardogs/ and assets/data/):
  - `ID_*` item definitions: `WDItemExtensionData_Throwable` (throw actions), `WDItemExtensionData_Placeable`
    (placement limits), `BH_*ExtensionData_C` / `BH_C4_Data_C` (trigger data) and the stack fragment;
  - `CRV_Throw*` curve assets (Content/Items/Throwable/Curves);
  - `DT_PostProcessEffects_Molotov`, `DA_CharacterModifierState_MolotovBurning`;
  - `DA_SmokeGrenade_*` and `DA_SmokeScreen` smoke data assets;
  - `assets/data/ge-values.json` (GE_MolotovBurning, GE_UsePlaceable, GE_Weapons_DetonatorRangeMultiplier);
  - `assets/data/explosive-actors.json` (reviewed Molotov fire-field defaults).
Blast damage, radius and falloff are not repeated here (see the Explosives page and the damage pipeline).

    python _tools/utility_throwable_tables.py            # summary counts
    python _tools/utility_throwable_tables.py --write    # refresh <!-- utility_throwable_tables NAME --> blocks

Page: game-features/Wardogs_FireAndUtility_v1.md.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_FireAndUtility_v1.md")
ITEMS = os.path.join(DATA, "Plugins", "GameFeatures", "Items")
BLOCKS = ["counts", "throw", "curves", "smoke", "molotov_pp", "molotov_state", "molotov_bp", "place", "trigger"]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bp_defaults as bpd  # noqa: E402

TOPIC = "fire_utility"


def bpv(asset, prop):
    """Entry from assets/data/bp-defaults.json (round 17) or None."""
    return bpd.get(TOPIC, asset, prop)


SPLIT = re.compile(r"^--- export: .*? ---$", re.M)


def exports(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    out = []
    for part in SPLIT.split(text):
        part = part.strip()
        if part:
            try:
                out.append(json.loads(part))
            except ValueError:
                pass
    return out


def rel(p):
    return os.path.relpath(p, DATA).replace(os.sep, "/")


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def num(x):
    if isinstance(x, float):
        return str(int(x)) if x == int(x) else f"{x:g}"
    return str(x)


def tag(t):
    return (t or {}).get("TagName", "-") if isinstance(t, dict) else str(t)


def short(t, prefix):
    s = tag(t)
    return s[len(prefix):] if s.startswith(prefix) else s


def vec(v, keys="XYZ"):
    if not v:
        return "-"
    return ", ".join(num(v.get(k, 0)) for k in keys)


def item_files():
    files = glob.glob(os.path.join(ITEMS, "**", "ID_*.json"), recursive=True)
    files += glob.glob(os.path.join(DATA, "Content", "Items", "Throwable", "**", "ID_*.json"), recursive=True)
    return sorted(f for f in files if not f.endswith("_Audio.json"))


class Item:
    def __init__(self, path):
        self.path = path
        self.objs = exports(path)
        self.defn = next((o for o in self.objs if o.get("Type") == "BHInventoryItemDefinition"), None)
        props = (self.defn or {}).get("Properties", {})
        self.id = tag(props.get("ItemId")) if self.defn else "-"
        dn = props.get("DisplayName") or {}
        self.name = dn.get("SourceString") or ("[key `%s`]" % dn.get("Key") if dn.get("Key") else "-")

    def of(self, typ):
        return [o.get("Properties") or {} for o in self.objs if o.get("Type") == typ]


def load_items():
    return [Item(p) for p in item_files()]


def stack_of(it):
    s = it.of("BHInventoryFragment_Stackable")
    return (s[0] or {}).get("MaxStackSize") if s and s[0] else None


# -- throw ------------------------------------------------------------------------------------------
def throw_rows(items):
    rows = []
    for it in items:
        for th in it.of("WDItemExtensionData_Throwable"):
            cls = ((th.get("ThrowableClass") or {}).get("AssetPathName") or "").split("/")[-1].split(".")[0] or "-"
            for act in th.get("ThrowActions") or []:
                v = act["Value"]
                rows.append((it, cls, short(act["Key"], "Action.Throw."), v, th))
    return rows


def throw(items):
    out = ["| Item id | Thrown actor | Throw action | Velocity | Constant velocity | Velocity curve | Owner velocity influence (vertical / horizontal) | Angular velocity Y (min-max) | Spawn offset (X, Z) | Equip blocked after (s) | Consumes |",
           "|---|---|---|---:|---|---|---|---|---|---:|---|"]
    for it, cls, act, v, th in throw_rows(items):
        crv = ((v.get("VelocityCurve") or {}).get("ObjectName") or "-")
        crv = crv.split("'")[1] if "'" in crv else crv
        so = v.get("SpawnOffset") or {}
        out.append("| `%s` | `%s` | %s | %s | %s | %s | %s / %s | %s-%s | %s, %s | %s | %s |" % (
            it.id, cls, act, num(v.get("ThrowVelocity")), "yes" if v.get("bUseConsistentVelocity") else "no",
            ("`%s`" % crv) if crv != "-" else "-", num(v.get("OwnerVerticalVelocityInfluence", 0)),
            num(v.get("OwnerHorizontalVelocityInfluence", 0)), num((v.get("MinAngularVelocity") or {}).get("Y", 0)),
            num((v.get("MaxAngularVelocity") or {}).get("Y", 0)), num(so.get("X", 0)), num(so.get("Z", 0)),
            num(v.get("BlockEquipAfterDestroyTime", 0)), "`%s`" % tag(th.get("ItemToConsume")) if th.get("ItemToConsume") else "(the item itself)"))
    return "\n".join(out)


def curves():
    out = ["| Curve | Keys (input, value) |", "|---|---|"]
    for p in sorted(glob.glob(os.path.join(DATA, "Content", "Items", "Throwable", "Curves", "CRV_*.json"))):
        for o in exports(p):
            keys = ((o.get("Properties") or {}).get("FloatCurve") or {}).get("Keys") or []
            if keys:
                out.append("| `%s` | %s |" % (o.get("Name"), "; ".join("%s: %s" % (num(k["Time"]), num(round(k["Value"], 3))) for k in keys)))
    return "\n".join(out)


# -- smoke ------------------------------------------------------------------------------------------
def smoke_assets():
    paths = glob.glob(os.path.join(DATA, "Content", "VFX", "Shared", "**", "DA_SmokeGrenade_*.json"), recursive=True)
    paths.append(os.path.join(DATA, "Content", "GameplayCues", "Vehicles", "Countermeasures", "DA_SmokeScreen.json"))
    rows = []
    for p in sorted(paths):
        for o in exports(p):
            if o.get("Type") == "PDA_SmokeGrenade_C":
                rows.append((o["Name"], p, o.get("Properties") or {}))
    return rows


def smoke(items):
    names = {}
    for it in items:
        m = re.match(r"(?i)id\.item\.smokegrenade\.(\w+)", it.id)
        if m:
            names[m.group(1)] = (it, throw_rows([it]))
    out = ["| Asset | Item | Total duration (s) | Sprite max size | Smoke type | Colour (RGBA) | Fade |",
           "|---|---|---:|---:|---|---|---|"]
    for name, p, pr in smoke_assets():
        colour = pr.get("SmokeColor")
        var = name.replace("DA_SmokeGrenade_", "")
        it = names.get(var)
        item = ("`%s` (%s)" % (it[0].id, cell(it[0].name))) if it else ("vehicle countermeasure (`Id.Item.VehicleSmoke`)" if name == "DA_SmokeScreen" else "-")
        td, sm = bpv(name, "Total Duration"), bpv(name, "SpriteMaxSize")
        fi, fo = bpv("PDA_SmokeGrenade", "Fade In Time"), bpv("PDA_SmokeGrenade", "Fade Out Time")
        out.append("| `%s` | %s | %s | %s | %s | %s | %s |" % (
            name, item, num(pr["Total Duration"]) if "Total Duration" in pr else ("%s (class default)" % num(td["value"]) if td else "not serialized"),
            num(pr["SpriteMaxSize"]) if "SpriteMaxSize" in pr else ("%s (class default)" % num(sm["value"]) if sm else "not serialized"),
            "`%s`" % pr["SmokeType"].split("::")[-1] if pr.get("SmokeType") else "not serialized",
            ("%s, %s, %s, %s" % tuple(num(round(colour[k], 3)) for k in "RGBA")) if colour else "not serialized",
            ("fade in %s / fade out %s" % (num(pr.get("Fade In Time", 0)), num(pr.get("Fade Out Time", 0)))) if "Fade In Time" in pr
            else ("fade in %s / fade out %s (class default)" % (num(fi["value"]), num(fo["value"])) if fi and fo and name != "DA_SmokeScreen" else "-")))
    return "\n".join(out)


# -- Molotov ----------------------------------------------------------------------------------------
def molotov_pp():
    p = os.path.join(ITEMS, "Molotov", "Content", "Data", "DT_PostProcessEffects_Molotov.json")
    o = exports(p)[0]
    out = ["| Row | Material | Duration (s) | Progress parameter | Curve keys | Curve time span (s) | Curve value range |", "|---|---|---:|---|---:|---|---|"]
    for row, r in (o.get("Rows") or {}).items():
        mat = ((r.get("MaterialClass") or {}).get("ObjectName") or "-")
        mat = mat.split("'")[1] if "'" in mat else mat
        pps = r.get("ProgressParams") or []
        if not pps:
            out.append("| `%s` | `%s` | %s | - | - | - | - |" % (row, mat, num(r.get("Duration", 0))))
        for pp in pps:
            keys = ((pp.get("ProgressEvaluationCurve") or {}).get("EditorCurveData") or {}).get("Keys") or []
            ts = [k["Time"] for k in keys]
            vs = [k["Value"] for k in keys]
            out.append("| `%s` | `%s` | %s | `%s` | %d | %s-%s | %s-%s |" % (
                row, mat, num(r.get("Duration", 0)), pp.get("ProgressParameterName"), len(keys),
                num(round(min(ts), 3)) if ts else "-", num(round(max(ts), 3)) if ts else "-",
                num(round(min(vs), 3)) if vs else "-", num(round(max(vs), 3)) if vs else "-"))
    return "\n".join(out)


def ge(name):
    with open(os.path.join(ROOT, "assets", "data", "ge-values.json"), encoding="utf-8") as f:
        return next(e for e in json.load(f)["effects"] if e["name"] == name)


def molotov_state():
    mb = ge("GE_MolotovBurning")
    st = None
    for o in exports(os.path.join(ITEMS, "Molotov", "Content", "Data", "DA_CharacterModifierState_MolotovBurning.json")):
        if o.get("Type") == "WDCharacterModifierStateDefinition":
            st = o.get("Properties") or {}
        if o.get("Type") == "WDCharacterModifierCondition_Tags":
            cond = (o.get("Properties") or {}).get("Requirements") or {}
        if o.get("Type") == "B_CameraModifier_MolotovBurning_C":
            cam = o.get("Properties") or {}
    with open(os.path.join(ROOT, "assets", "data", "explosive-actors.json"), encoding="utf-8") as f:
        sf = json.load(f)["actors"]["Molotov"]["sustained_fire"]
    rows = [
        ("`GE_MolotovBurning` (Data, `assets/data/ge-values.json`)", "granted tags `%s`; modifiers: %s; duration, stacking and requirements not serialized (native `UBHGameplayEffect` defaults)" % (
            ", ".join(mb["granted_tags"]), "none" if not mb["modifiers"] else mb["modifiers"])),
        ("Character modifier state `%s` (Data)" % tag(st.get("StateTag")),
         "active while `%s`; ignored while `%s`; camera modifier removal blends out over %s s (`bBlendedRemoval` %s)" % (
             ", ".join(cond.get("RequireTags", [])), ", ".join(cond.get("IgnoreTags", [])), num(cam.get("RemovalTime", 0)),
             str(cam.get("bBlendedRemoval", False)).lower())),
        ("Fire-field player damage (Data, `explosive-actors.json`)", "%s per attempt, damage type `%s`, every %s s" % (
            num(sf["player_starting_damage"]), sf["player_damage_type"], num(sf["timer_period_seconds"]))),
        ("Fire-field vehicle damage (Data, `explosive-actors.json`)", "%s `Attribute.Gameplay.Health` per attempt, every %s s" % (
            num(sf["vehicle_health_delta"]), num(sf["timer_period_seconds"]))),
        ("Per-second rate (Derived)", "player %s per second, vehicle %s per second, before downstream handling" % (
            num(round(sf["player_starting_damage"] / sf["timer_period_seconds"], 3)),
            num(round(sf["vehicle_health_delta"] / sf["timer_period_seconds"], 3)))),
    ]
    return "| Item | Value |\n|---|---|\n" + "\n".join("| %s | %s |" % (a, cell(b)) for a, b in rows)


# -- place / trigger --------------------------------------------------------------------------------
def place(items):
    out = ["| Item id | Name | Placed actor | Max placement distance | Max placement angle | Collision size (X, Y, Z) | Can sit on another placeable | Health override | Blocked by | Applied effect | Progress text |",
           "|---|---|---|---:|---:|---|---|---:|---|---|---|"]
    for it in items:
        for pl in it.of("WDItemExtensionData_Placeable"):
            if not re.search(r"AT_mine|Claymore|IED", rel(it.path)):
                continue
            cls = (pl.get("PlaceableClass") or {}).get("ObjectName", "-")
            cls = cls.split("'")[1] if "'" in cls else cls
            blocked = ", ".join(sorted((b.get("ObjectName") or "").split("'")[1] for b in pl.get("BlockedActorClasses") or [] if "'" in (b.get("ObjectName") or "")))
            eff = ", ".join((e.get("ObjectName") or "").split("'")[1] for e in pl.get("AppliedEffects") or [] if "'" in (e.get("ObjectName") or ""))
            vit = ((pl.get("PlaceableInitData") or {}).get("VitalityComponentParams") or {})
            size = pl.get("PlacementCollisionSize")
            dist = pl.get("MaxPlacementDistance")
            out.append("| `%s` | %s | `%s` | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                it.id, cell(it.name), cls, num(dist) if dist is not None else "not set", num(pl.get("MaxPlacementAngle", 0)),
                vec(size) if size else "not serialized", "yes" if pl.get("bCanPlaceOnOtherPlaceable") else "no",
                num(vit.get("BaseHealthOverride")) if vit.get("bOverrideBaseHealth") else "-", cell(blocked) or "-",
                cell(eff) or "-", cell((pl.get("ProgressWheelText") or {}).get("SourceString") or "-")))
    return "\n".join(out)


TRIGGER_FIELDS = {
    "BH_AT_MineExtensionData_C": ["UniversalVehicleSpeed", "TriggerLocation", "TriggerBoxExtends", "ArmingDelay", "TraceCheckTime", "DetectFriendlyVehicles", "PerVehicleSpeedListDetection"],
    "BH_ClaymoreExtensionData_C": ["TriggerBoxExtends", "ActivationDelayTimer", "ShouldDetectVehicle_", "DetectFriendlyTeammates_"],
    "BH_C4_Data_C": ["MaxDetonationDistance", "DelayTillExplosion"],
}


def trigger_default(stem, f):
    """Blueprint-resolved text for a field the item definition does not set (round 17), or None."""
    e = bpv(stem, f[:-1] + "?" if f.endswith("_") else f)
    if e is None or e["value"] is None:
        return None
    return "%s (Blueprint default, `%s`)" % (bpd.fmt(e["value"]) if not isinstance(e["value"], dict) else "(%s)" % vec(e["value"]),
                                           e["from_asset"])


def trigger(items):
    out = ["| Item id | Extension data class | Field | Value in the item definition |", "|---|---|---|---|"]
    n = 0
    for it in items:
        for o in it.objs:
            t = o.get("Type")
            if t in TRIGGER_FIELDS:
                pr = o.get("Properties") or {}
                for f in TRIGGER_FIELDS[t]:
                    val = pr.get(f)
                    if isinstance(val, dict):
                        val = "(%s)" % vec(val)
                    dflt = trigger_default(os.path.splitext(os.path.basename(it.path))[0], f) if f not in pr else None
                    out.append("| `%s` | `%s` | `%s` | %s |" % (it.id, t, f, (dflt or "not serialized (class default)") if f not in pr else num(val) if not isinstance(val, (list, str)) else cell(val)))
                    n += 1
    return "\n".join(out)


def molotov_bp():
    """B_Molotov and B_Molotov_FireField Blueprint values against the native constructor defaults (round 17)."""
    out = ["| Class | Field | Offset | Blueprint value | Native ctor default | Derived role (native page) |", "|---|---|---|---:|---:|---|"]
    roles = {"0x670": "scale of the patch offset from the impact point", "0x674": "scale of the patch offset from the impact point",
             "0x678": "patch count", "0x67C": "not matched to a use", "0x680": "scales a reduced count",
             "0x684": "copied into each spawned patch"}
    # AWDMolotovFireField: +0x2D4/2D8/2DC read by the point-clustering function at RVA 0x86A0E20 (round 86); +0x2D0 read by 0x86A3D70 / 0x86A40E0 (round 88), both static reads
    fire_roles = {"0x2D4": "horizontal merge radius of a fire cluster (cm)", "0x2D8": "vertical tolerance of a cluster (cm)",
                  "0x2DC": "maximum number of clusters", "0x2D0": "fire spread speed in cm per second (function 0x86A40E0; static read, round 88)"}
    for asset, cls in (("B_Molotov", "AWDMolotovGrenade"), ("B_Molotov_FireField", "AWDMolotovFireField")):
        for e in bpd.topic_entries(TOPIC):
            if e["asset"] != asset or not e["property"].startswith("_aaa"):
                continue
            nd = e.get("native_default")
            out.append("| `%s` | `%s` | `+%s` | %s (%s) | %s | %s |" % (
                asset, e["property"], "0x%X" % int(e["sdk_offset"], 16),
                bpd.fmt(e["value"]), "Blueprint CDO" if e["resolved_from"] == "export" else "native, not set in the Blueprint",
                bpd.fmt(nd) if nd is not None else "-", (roles if cls == "AWDMolotovGrenade" else fire_roles).get("0x%X" % int(e["sdk_offset"], 16), "not decoded")))
    return "\n".join(out)


def counts(items):
    tr = throw_rows(items)
    thr_items = sorted({r[0].id for r in tr})
    pl = [1 for it in items if re.search(r"AT_mine|Claymore|IED", rel(it.path)) for _ in it.of("WDItemExtensionData_Placeable")]
    smk = len([1 for a in smoke_assets()])
    with open(os.path.join(DATA, "Plugins", "GameFeatures", "Items", "Molotov", "Content", "Data", "DT_PostProcessEffects_Molotov.json"), encoding="utf-8") as f:
        nrows = len(exports(f.name)[0].get("Rows") or {})
    return "\n".join([
        "- Item definitions scanned: **%d** (`ID_*.json`, audio files excluded)." % len(items),
        "- Throwable items: **%d** (%s), **%d** throw actions." % (len(thr_items), ", ".join("`%s`" % i for i in thr_items), len(tr)),
        "- Placeable explosives: **%d** (AT mine, Claymore, placed IED)." % len(pl),
        "- Smoke data assets: **%d** (`DA_SmokeGrenade_*` and `DA_SmokeScreen`)." % smk,
        "- Molotov post-process rows: **%d**." % nrows,
    ])


RENDER = {
    "counts": lambda it: counts(it), "throw": lambda it: throw(it), "curves": lambda it: curves(),
    "smoke": lambda it: smoke(it), "molotov_pp": lambda it: molotov_pp(), "molotov_state": lambda it: molotov_state(),
    "place": lambda it: place(it), "trigger": lambda it: trigger(it), "molotov_bp": lambda it: molotov_bp(),
}


def write(items):
    with open(PAGE, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    for name in BLOCKS:
        pat = re.compile(rf"<!-- utility_throwable_tables {name} -->.*?<!-- /utility_throwable_tables {name} -->", re.S)
        if not pat.search(text):
            raise SystemExit(f"error: no markers for {name} in {os.path.basename(PAGE)}")
        body = RENDER[name](items).replace("\n", nl)
        text = pat.sub(lambda _: f"<!-- utility_throwable_tables {name} -->{nl}{body}{nl}<!-- /utility_throwable_tables {name} -->", text)
    with open(PAGE, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    items = load_items()
    if "--write" in sys.argv:
        write(items)
        return
    print(counts(items))


if __name__ == "__main__":
    main()
