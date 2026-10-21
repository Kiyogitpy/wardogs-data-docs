"""Vehicle part and handling tables, rebuilt from data/.

Reads every ModularVehiclePart (VP_*) and every variant (VV_*) under
data/Wardogs/Plugins/GameFeatures/Vehicles, assembles each variant with the same slot rules as
_tools/damage_tables.py (pipelines/Wardogs_VehicleDamagePipeline_v1.md section 5.4) and follows the
variant's vehicle config to the handling assets.

    python _tools/vehicle_part_tables.py --parts      # every part: slot, what it adds, variants that use it
    python _tools/vehicle_part_tables.py --common     # seats, stats-sheet speed/fuel, masses, per variant
    python _tools/vehicle_part_tables.py --wheeled    # wheeled drivetrain, axles and suspension
    python _tools/vehicle_part_tables.py --tracked    # tracked engine, dynamics and suspension
    python _tools/vehicle_part_tables.py --air        # rotary body mass, drag and engine asset
    python _tools/vehicle_part_tables.py --prediction # network-prediction resimulation thresholds
    python _tools/vehicle_part_tables.py --coverage   # part count and the parts no variant places
    python _tools/vehicle_part_tables.py --write      # refresh every marked block in the docs, in place

Blocks are written between `<!-- vehicle_part_tables MODE -->` and `<!-- /vehicle_part_tables -->`.
"""
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as D  # noqa: E402

ROOT = D.ROOT
VEH = os.path.join(D.DATA, "Wardogs", "Plugins", "GameFeatures", "Vehicles")
DOCS = ["game-features/Wardogs_VehicleHandling_v1.md"]
BLOCK = re.compile(r"<!-- vehicle_part_tables (.+?) -->\r?\n.*?<!-- /vehicle_part_tables -->", re.S)

_cache = {}


def exp(path):
    if path not in _cache:
        _cache[path] = D.exports(path)
    return _cache[path]


def main_obj(path):
    ex = exp(path)
    name = os.path.basename(path)[:-5]
    return next((o for o in ex if o.get("Name") == name), ex[0] if ex else {})


def short(ref):
    """Asset or object name from an ObjectName / AssetPathName reference."""
    if not ref:
        return None
    if isinstance(ref, dict):
        if "ExternalCurve" in ref:
            return short(ref["ExternalCurve"])
        s = ref.get("ObjectName") or ref.get("AssetPathName") or ref.get("ObjectPath") or ""
    else:
        s = str(ref)
    m = re.search(r"'([^']+)'", s)
    if m:
        return m.group(1).split(":")[-1]
    return s.rsplit("/", 1)[-1].split(".")[0]


def props_of(ref):
    f = D.asset_file(short(ref)) if ref else None
    return (main_obj(f).get("Properties") or {}) if f else {}


def first(v):
    """Intact-tyre value of a per-state array stored as {Values, Values[1], ...}."""
    if isinstance(v, dict):
        for k in ("Values", "Values[0]"):
            if k in v:
                return v[k]
        return next(iter(v.values()), None)
    if isinstance(v, list):
        return v[0] if v else None
    return v


def num(v, nd=3):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (int, float)):
        if abs(v) >= 1e5 and float(v).is_integer():
            return f"{v:,.0f}"
        s = f"{v:,.{nd}f}"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s if s not in ("", "-0") else "0"
    return str(v)


def keys_of(curve):
    """(time, value) keys of a curve reference or inline curve, or None."""
    if not curve:
        return None
    if isinstance(curve, dict) and "ExternalCurve" in curve:
        curve = curve["ExternalCurve"]
    if isinstance(curve, dict) and ("ObjectName" in curve or "AssetPathName" in curve):
        p = props_of(curve)
        curve = p.get("FloatCurve") or p
    if isinstance(curve, dict) and "EditorCurveData" in curve:
        curve = curve["EditorCurveData"]
    ks = curve.get("Keys") if isinstance(curve, dict) else None
    return [(k["Time"], k["Value"]) for k in ks] if ks else None


def curve_peak(curve):
    ks = keys_of(curve)
    if not ks:
        return "—"
    t, v = max(ks, key=lambda k: k[1])
    return f"{num(v)} @ {num(t, 0)} ({num(ks[0][0], 0)} to {num(ks[-1][0], 0)})"


def esc(s):
    return str(s).replace("|", "\\|")


# ---- variants, assembly ----------------------------------------------------------------------

def assemble_slots(variant_path):
    """Like damage_tables.assemble, but also records where each part is placed:
    [(slot path, part name, asset file)], platform name, variant tag."""
    v = next(o for o in exp(variant_path) if o.get("Type") == "ModularVehicleVariant")["Properties"]
    data = v["AssemblyData"]
    overrides = {s["Path"]["Path"]: s["Part"]["AssetPathName"]
                 for s in data.get("CustomData", {}).get("SlotOverrides", [])}
    placed, files = [], []

    def visit(path, prefix, slot):
        f = D.asset_file(path)
        if not f:
            return
        files.append(f)
        placed.append((slot, short(path), f))
        objs = {o.get("Name"): o for o in exp(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for s in (owner or {}).get("Properties", {}).get("Slots", []):
            if not s["Value"].get("bEnabled", True):
                continue
            name = prefix + s["Key"]
            sl = objs.get(s["Value"]["Slot"]["ObjectName"].split(":")[-1].rstrip("'"), {})
            part = overrides.get(name) or sl.get("Properties", {}).get("DefaultPart", {}).get("AssetPathName")
            if part:
                visit(part, name + ".", name)

    base = data["VehicleBase"]["ObjectPath"].split(".")[0]
    visit(base, "", "(platform)")
    return placed, files, short(base), D.tag(v["VariantID"])


def variant_info():
    out = []
    for vp in D.variants():
        placed, files, platform, vtag = assemble_slots(vp)
        out.append({"name": os.path.basename(vp)[3:-5], "tag": vtag, "platform": platform,
                    "placed": placed, "files": files})
    return out


def frag_objs(files):
    """(fragment key, fragment object) of the enabled fragments, in assembly order."""
    for f in files:
        objs = {o.get("Name"): o for o in exp(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for fr in (owner or {}).get("Properties", {}).get("Fragments", []):
            if fr["Value"].get("bEnabled", True):
                yield fr["Key"], objs.get(fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'"), {})


def last_frag(files, typ, field):
    """Reference held by the last enabled fragment of this type; later modules replace earlier ones."""
    val = None
    for _, o in frag_objs(files):
        if o.get("Type") == typ and (o.get("Properties") or {}).get(field):
            val = o["Properties"][field]
    return val


def seat_total(files):
    """Seat setups across the assembled modules: one count per Seats-type fragment key, later modules replace earlier ones."""
    by_key = {}
    for key, o in frag_objs(files):
        if o.get("Type") == "MVF_Seats":
            by_key[key] = seat_count(o["Properties"].get("SeatSettingsDataAsset"))
    return sum(by_key.values()) if by_key else None


def seat_count(ref):
    return len(props_of(ref).get("SeatSetups", [])) if ref else None


# ---- parts -----------------------------------------------------------------------------------

def part_files():
    out = []
    for p in sorted(glob.glob(os.path.join(VEH, "**", "*.json"), recursive=True)):
        if os.path.basename(p).startswith("VP_") and any(o.get("Type") == "ModularVehiclePart" for o in exp(p)):
            out.append(p)
    return out


def vehicle_folder(p):
    return os.path.relpath(p, VEH).replace("\\", "/").split("/")[0]


def adds(path):
    """Short list of what a part contributes, by fragment type."""
    objs = {o.get("Name"): o for o in exp(path)}
    part = next(o for o in objs.values() if o.get("Type") == "ModularVehiclePart")
    items = []
    for fr in part.get("Properties", {}).get("Fragments", []):
        o = objs.get(fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'"), {})
        t, p = o.get("Type", ""), o.get("Properties") or {}
        off = "" if fr["Value"].get("bEnabled", True) else " (disabled)"
        if t == "MVF_Seats":
            n = seat_count(p.get("SeatSettingsDataAsset"))
            items.append(f"seats ×{n} (`{short(p['SeatSettingsDataAsset'])}`)" + off)
        elif t == "MVF_HealthSections":
            hs = ", ".join(f"{D.tag(h['Key']).replace('Attribute.Gameplay.Health.', '')} {num(h['Value']['MaxHealth'], 0)}"
                           for h in p.get("HealthSections", []))
            items.append(f"health: {hs}" + off)
        elif t == "MVF_VehicleConfig":
            items.append(f"config `{short(p['VehicleConfig'])}`" + off)
        elif t == "WD_MVF_WeaponFragment":
            items.append(f"weapon `{short(p.get('WeaponDataAsset'))}`" + off)
        elif t == "MVF_InstancedWheels":
            items.append(f"wheels (`{short(p.get('WheelMesh'))}`)" + off)
        elif t in ("MVF_StaticMesh", "MVF_SkeletalMesh"):
            m = short(p.get("StaticMesh") or p.get("SkeletalMesh"))
            items.append(f"mesh `{m}`" + off)
        elif t == "MVF_DestructibleMeshes":
            items.append("destructible meshes" + off)
        elif t == "MVF_DeployStateCollision":
            items.append("deploy-state collision" + off)
        elif t == "MVF_ActorFragment":
            items.append(f"actor `{short(p.get('ActorData', {}).get('Actor'))}`" + off)
        elif t == "WD_MVF_VehicleWeatherResponse":
            items.append("weather response" + off)
        elif t == "WD_MVF_Interactions":
            items.append(f"interactions `{short(p.get('VehicleInteractionsDataAsset'))}`" + off)
        elif t == "WD_MVF_VehicleStats":
            items.append(f"stats `{short(p.get('VehiclesStatsDataAsset'))}`" + off)
        elif t:
            items.append(t + off)
    for s in part.get("Properties", {}).get("Slots", []):
        sl = objs.get(s["Value"]["Slot"]["ObjectName"].split(":")[-1].rstrip("'"), {})
        dp = short(sl.get("Properties", {}).get("DefaultPart"))
        items.append(f"slot `{s['Key']}`" + (f" (default `{dp}`)" if dp else ""))
    return items


def other_refs(names):
    """For parts no variant places: the other vehicle files that name them."""
    refs = {n: set() for n in names}
    for p in glob.glob(os.path.join(VEH, "**", "*.json"), recursive=True):
        base = os.path.basename(p)[:-5]
        text = open(p, encoding="utf-8").read()
        for n in names:
            if base != n and n in text:
                refs[n].add(base)
    return refs


def parts_table():
    vi = variant_info()
    placed = {}
    for v in vi:
        for slot, part, _ in v["placed"]:
            placed.setdefault(part, {}).setdefault(slot, []).append(v["name"])
    pf = part_files()
    unplaced = [os.path.basename(p)[:-5] for p in pf if os.path.basename(p)[:-5] not in placed]
    refs = other_refs(unplaced) if unplaced else {}
    print("| Part | Folder | Slot | Adds | Variants |")
    print("|---|---|---|---|---|")
    for p in pf:
        n = os.path.basename(p)[:-5]
        if n in placed:
            slots = sorted(placed[n])
            slot = ", ".join(f"`{s}`" for s in slots)
            vs = sorted({x for s in slots for x in placed[n][s]})
            vtxt = ", ".join(v.replace("VV_", "") for v in vs)
        else:
            slot = "—"
            r = sorted(refs.get(n, []))
            vtxt = "none by assembly" + (f"; named in {', '.join('`' + x + '`' for x in r)}" if r else "")
        print(f"| `{n}` | {vehicle_folder(p)} | {esc(slot)} | {esc('; '.join(adds(p)))} | {esc(vtxt)} |")


def coverage():
    vi = variant_info()
    placed = {part for v in vi for _, part, _ in v["placed"]}
    pf = [os.path.basename(p)[:-5] for p in part_files()]
    print(f"{len(pf)} parts, {len(vi)} variants; {sum(1 for n in pf if n in placed)} parts placed by at least one variant, "
          f"{sum(1 for n in pf if n not in placed)} not.")
    for n in pf:
        if n not in placed:
            print("  not placed:", n)


# ---- handling --------------------------------------------------------------------------------

def family(cfg_type):
    return {"MWheeledVehicleConfigDataAsset": "wheeled", "MTrackedVehicleConfigDataAsset": "tracked",
            "BHRotaryVehicleConfigDataAsset": "air"}.get(cfg_type)


def handling():
    """Per variant: family, config properties, stats properties, seat counts, masses."""
    rows = []
    for v in variant_info():
        cfg_ref = last_frag(v["files"], "MVF_VehicleConfig", "VehicleConfig")
        if not cfg_ref:
            continue
        f = D.asset_file(short(cfg_ref))
        cfg_obj = main_obj(f) if f else {}
        fam = family(cfg_obj.get("Type"))
        if not fam:
            continue
        stats_ref = last_frag(v["files"], "WD_MVF_VehicleStats", "VehiclesStatsDataAsset")
        coll_mass = None
        for _, o in frag_objs(v["files"]):
            if o.get("Type") == "WD_MVF_DestructionInvokerFragment":
                coll_mass = (o.get("Properties") or {}).get("VehicleMass", coll_mass)
        rows.append({**v, "family": fam, "cfg": cfg_obj.get("Properties") or {}, "cfg_name": short(cfg_ref),
                     "stats": props_of(stats_ref), "stats_name": short(stats_ref),
                     "seat_setups": seat_total(v["files"]), "coll_mass": coll_mass})
    return rows


def common_table():
    rows = handling()
    print("| Variant | Family | Seat setups | Stats MaxSeats | Max speed | Fuel | Fuel economy | Body mass | Collision-fragment mass | Config |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        c, s = r["cfg"], r["stats"]
        if r["family"] == "wheeled":
            mass = props_of(c.get("CharacteristicsDataAsset")).get("Mass")
        elif r["family"] == "air":
            b = props_of(c.get("RotaryVehicleBodyDataAsset"))
            mass = b.get("MassOverride") if b.get("bEnableMassOverride") else None
        else:
            mass = None
        print(f"| {r['name']} | {r['family']} | {num(r['seat_setups'])} | {num(s.get('MaxSeats'))} | {num(s.get('MaxSpeed'))} | "
              f"{num(s.get('MaxFuel'))} | {num(s.get('FuelEconomy'))} | {num(mass)} | {num(r['coll_mass'])} | `{r['cfg_name']}` |")


def wheeled_tables():
    rows = [r for r in handling() if r["family"] == "wheeled"]
    print("Drivetrain")
    print()
    print("| Variant | Torque curve peak value @ RPM (RPM range) | Torque scale | Idle RPM | Gear ratios | Final ratio | Boost | Torque share F/R | Steer F (deg) |")
    print("|---|---|---:|---:|---|---:|---:|---|---:|")
    axles = {}
    for r in rows:
        c = r["cfg"]
        et = props_of(c.get("EngineTransmissionDataAsset"))
        ed, td = et.get("EngineData", {}), et.get("TransmissionData", {})
        ax = [props_of(a) for a in c.get("AxleDataAssets", [])]
        axles[r["name"]] = ax
        share = " / ".join(num(a.get("TorqueShare")) for a in ax)
        steer = " / ".join(num(a.get("MaxSteerAngle", 0)) for a in ax[:1])
        gears = ", ".join(num(g, 2) for g in td.get("GearRatios", []))
        print(f"| {r['name']} | {curve_peak(ed.get('TorqueCurve'))} | {num(ed.get('TorqueScale'))} | {num(ed.get('IdleRPM'))} | "
              f"{gears} | {num(td.get('FinalGearRatio'))} | {num(ed.get('BoostScale'))} | {share} | {steer} |")
    print()
    print("Chassis and suspension")
    print()
    print("| Variant | Mass | Hand brake | ABS | ASR | Brake torque F/R (intact tyre) | Spring F/R | Up travel F/R (m) | Compression / relaxation damper F | Tyre radius F (m) |")
    print("|---|---:|---:|---:|---:|---|---|---|---|---:|")
    for r in rows:
        ch = props_of(r["cfg"].get("CharacteristicsDataAsset"))
        ax = axles[r["name"]]
        wh = [props_of(a.get("WheelDataAsset")) for a in ax]
        bt = " / ".join(num(first(w.get("BrakeTorque")), 0) for w in wh)
        sp = " / ".join(num(first(w.get("SuspensionSpring"))) for w in wh)
        ut = " / ".join(num(first(w.get("SuspensionUpTravel"))) for w in wh)
        dm = f"{num(first(wh[0].get('CompressionDamper')), 0)} / {num(first(wh[0].get('RelaxationDamper')), 0)}" if wh else "—"
        rad = num(first(wh[0].get("Radius"))) if wh else "—"
        print(f"| {r['name']} | {num(ch.get('Mass'))} | {num(ch.get('HandBrakePower'))} | {num(ch.get('Abs'))} | {num(ch.get('ASR'))} | "
              f"{bt} | {sp} | {ut} | {dm} | {rad} |")


def tracked_tables():
    rows = [r for r in handling() if r["family"] == "tracked"]
    print("Engine and transmission")
    print()
    print("| Variant | EngineData torque curve peak value @ RPM (RPM range) | Dynamics torque curve peak value @ RPM (RPM range) | Max RPM | EngineData gears | Dynamics gears | Differential ratio (EngineData / Dynamics) | Extra power ratio | Boost | Brake force |")
    print("|---|---|---|---:|---:|---:|---|---:|---:|---:|")
    for r in rows:
        c = r["cfg"]
        en = props_of(c.get("TrackedVehicleEngineData"))
        dy = props_of(c.get("TrackedVehicleDynamicsData"))
        dd = (dy.get("DifferentialData") or [{}])[0]
        print(f"| {r['name']} | {curve_peak(en.get('TorqueCurve'))} | {curve_peak(dy.get('EngineTorqueCurve'))} | {num(dy.get('MaxRPM'))} | "
              f"{len(en.get('GearRatios', []))} | {len(dy.get('Gears', []))} | {num(en.get('DifferentialRatio'))} / {num(dd.get('DifferentialRatio'))} | "
              f"{num(en.get('EngineExtraPowerRatio'))} | {num(en.get('BoostScale'))} | {num(en.get('BrakeForce'))} |")
    print()
    print("Steering, suspension and tracks")
    print()
    print("| Variant | Steer input rise / fall | Idle brake input | Track mass | Sprocket mass | Suspension up / down travel | Stiffness / damp (suspension) | Wheel spring rate | Damping compress / rebound | Suspension length | Max incline (deg) | Tread count |")
    print("|---|---|---:|---:|---:|---|---|---:|---|---:|---:|---:|")
    for r in rows:
        c = r["cfg"]
        en = props_of(c.get("TrackedVehicleEngineData"))
        dy = props_of(c.get("TrackedVehicleDynamicsData"))
        su = props_of(c.get("TrackedVehicleSuspensionData"))
        wd = props_of(c.get("TrackedVehicleWheelData"))
        print(f"| {r['name']} | {num(dy.get('SteerInputRise'))} / {num(dy.get('SteerInputFall'))} | {num(dy.get('IdleBrakeInput'))} | "
              f"{num(en.get('TrackMass'))} | {num(en.get('SprocketMass'))} | {num(su.get('SuspensionUpTravel'))} / {num(su.get('SuspensionDownTravel'))} | "
              f"{num(su.get('StiffnessForce'))} / {num(su.get('DampenForce'))} | {num(wd.get('SpringRate'))} | "
              f"{num(wd.get('DampingCompress'))} / {num(wd.get('DampingRebound'))} | {num(wd.get('SuspensionLength'))} | "
              f"{num(wd.get('MaxInclineAngle'))} | {num(su.get('TreadsOnSpline') or c.get('TreadsOnSpline'))} |")


def air_tables():
    rows = [r for r in handling() if r["family"] == "air"]
    print("| Variant | Mass override | Front / rear / side drag area | Drag coefficient | Engine asset properties | Flight-characteristics asset |")
    print("|---|---:|---|---:|---|---|")
    for r in rows:
        c = r["cfg"]
        b = props_of(c.get("RotaryVehicleBodyDataAsset"))
        d = props_of(c.get("RotaryVehicleDragDataAsset"))
        e = props_of(c.get("RotaryEngineDataAsset"))
        mass = b.get("MassOverride") if b.get("bEnableMassOverride") else None
        eng = ", ".join(sorted(e)) if e else "none exported (native defaults)"
        print(f"| {r['name']} | {num(mass)} | {num(d.get('FrontDragArea'))} / {num(d.get('RearDragArea'))} / {num(d.get('SideArea'))} | "
              f"{num(d.get('DragCoefficient'))} | {eng} | `{short(c.get('RotaryVehicleFlightCharacteristicsDataAsset'))}` |")


def prediction_table():
    print("| Variant | Prediction asset | Position / rotation / linear vel / angular vel error thresholds | Position / rotation / velocity stability multiplier |")
    print("|---|---|---|---|")
    seen = set()
    for r in handling():
        ref = next((v for k, v in r["cfg"].items() if isinstance(v, dict) and "PredictionSettings" in str(v.get("ObjectName", ""))), None)
        if not ref:
            continue
        s = props_of(ref).get("Settings", {}).get("ResimulationSettings", {})
        print(f"| {r['name']} | `{short(ref)}` | {num(s.get('ResimulationErrorPositionThreshold'))} / {num(s.get('ResimulationErrorRotationThreshold'))} / "
              f"{num(s.get('ResimulationErrorLinearVelocityThreshold'))} / {num(s.get('ResimulationErrorAngularVelocityThreshold'))} | "
              f"{num(s.get('PosStabilityMultiplier'))} / {num(s.get('RotStabilityMultiplier'))} / {num(s.get('VelStabilityMultiplier'))} |")


MODES = {"prediction": prediction_table, "parts": parts_table, "common": common_table, "wheeled": wheeled_tables,
         "tracked": tracked_tables, "air": air_tables, "coverage": coverage}


def write_docs():
    for doc in DOCS:
        path = os.path.join(ROOT, doc)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        nl = "\r\n" if "\r\n" in text else "\n"

        def regen(m):
            mode = m.group(1)
            out = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--" + mode],
                                 capture_output=True, text=True, encoding="utf-8", check=True).stdout.strip()
            return nl.join([f"<!-- vehicle_part_tables {mode} -->"] + out.split("\n") + ["<!-- /vehicle_part_tables -->"])

        new, n = BLOCK.subn(regen, text)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        print(f"{doc}: {n} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv:
        write_docs()
        return
    for k, fn in MODES.items():
        if "--" + k in sys.argv:
            fn()
            return
    print(__doc__)


if __name__ == "__main__":
    main()
