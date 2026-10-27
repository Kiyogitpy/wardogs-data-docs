"""Round 85 vehicle pages, rebuilt from data/ (V4-03, V4-07, V4-14, V4-15).

Writes three whole pages (the pages hold no hand-written table; edit the text in this file):

    game-features/Wardogs_FixedWingFlightModel_v1.md    FWG_01 flight model: engine, drag, lift and drag curves,
                                                        the 22-row auto-trim table, control assists, and a derived
                                                        speed figures read from the table
    game-features/Wardogs_VehicleConfigFields_v1.md     config sub-fields (wheeled, tracked, rotary), tracked wheel
                                                        data, rotary flight data, air drag, fuel settings
    game-features/Wardogs_VehicleTurretControls_v1.md   the six vehicle crosshair tables and the 23
                                                        WDVehicleWeaponDataAsset assets

    python _tools/vehicle_round85_tables.py --write     # rewrite the three pages
    python _tools/vehicle_round85_tables.py --check     # exit 1 when a page is stale (line endings ignored)
"""
import collections
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs")
EXPORT = re.compile(r"^--- export: .* ---\n", re.M)
GH = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"
EVID = GH + "docs/evidence/round85-veh.md"
AIR = os.path.join(DATA, "Content/Vehicles/Pawns/Air/Airplane/FWG_01/Data")
VEH = os.path.join(DATA, "Plugins/GameFeatures/Vehicles")


# ---------------------------------------------------------------- reading
def exports(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        out = []
        for part in EXPORT.split(f.read())[1:]:
            try:
                out.append(json.loads(part))
            except ValueError:
                pass
        return out


def air(name):
    return exports(os.path.join(AIR, name + ".json"))


def props(name):
    return air(name)[0]["Properties"]


def veh_exports():
    """(relative path, export) for every export under the vehicle plugins and Content/Vehicles."""
    for base in (VEH, os.path.join(DATA, "Content/Vehicles")):
        for p in sorted(glob.glob(os.path.join(base, "**", "*.json"), recursive=True)):
            for e in exports(p):
                yield os.path.relpath(p, DATA).replace("\\", "/"), e


def num(v, nd=4):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "-"
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        if v != 0 and (abs(v) >= 1e7 or abs(v) < 1e-2):
            return f"{v:.4g}"
        s = f"{v:,.{nd}f}"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s if s not in ("", "-0") else "0"
    return str(v)


def short(ref):
    """Asset name from an ObjectName or AssetPathName reference."""
    if not ref:
        return "-"
    if isinstance(ref, dict):
        ref = ref.get("ObjectName") or ref.get("AssetPathName") or ""
    m = re.search(r"'([^':]+)'$", ref)
    if m:
        return m.group(1)
    return ref.rsplit("/", 1)[-1].split(".")[0] or "-"


def tag(v):
    return v.get("TagName", "-") if isinstance(v, dict) else "-"


def vec(v):
    if not isinstance(v, dict):
        return "-"
    return "(" + ", ".join(num(v[k]) for k in "XYZ" if k in v) + ")"


def table(head, rows, align=None):
    align = align or ["---"] * len(head)
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(align) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


# ---------------------------------------------------------------- curves (Unreal rich curve evaluation)
def _segment(k1, k2, t):
    x = k2["Time"] - k1["Time"]

    def handle(k, side):
        tan = k["LeaveTangent" if side == "L" else "ArriveTangent"]
        wm = k["TangentWeightMode"]
        weighted = wm == "RCTWM_WeightedBoth" or wm == ("RCTWM_WeightedLeave" if side == "L" else "RCTWM_WeightedArrive")
        w = k["LeaveTangentWeight" if side == "L" else "ArriveTangentWeight"] if weighted else math.sqrt(x * x + (tan * x) ** 2) / 3
        a = math.atan(tan)
        return math.cos(a) * w / x, math.sin(a) * w

    x1, y1 = handle(k1, "L")
    x2, y2 = handle(k2, "A")
    px = [0, x1, 1 - x2, 1]
    py = [k1["Value"], k1["Value"] + y1, k2["Value"] - y2, k2["Value"]]
    al = (t - k1["Time"]) / x
    lo, hi = 0.0, 1.0
    for _ in range(60):
        s = (lo + hi) / 2
        u = 1 - s
        bx = u ** 3 * px[0] + 3 * u * u * s * px[1] + 3 * u * s * s * px[2] + s ** 3 * px[3]
        if bx < al:
            lo = s
        else:
            hi = s
    s = (lo + hi) / 2
    u = 1 - s
    return u ** 3 * py[0] + 3 * u * u * s * py[1] + 3 * u * s * s * py[2] + s ** 3 * py[3]


def curve_value(keys, t):
    """Value of a rich curve at t (clamped at both ends; cubic keys use Bezier handles as Unreal does)."""
    if t <= keys[0]["Time"]:
        return keys[0]["Value"]
    if t >= keys[-1]["Time"]:
        return keys[-1]["Value"]
    for a, b in zip(keys, keys[1:]):
        if a["Time"] <= t <= b["Time"]:
            mode = a["InterpMode"]
            if mode == "RCIM_Linear":
                return a["Value"] + (b["Value"] - a["Value"]) * (t - a["Time"]) / (b["Time"] - a["Time"])
            if mode == "RCIM_Constant":
                return a["Value"]
            return _segment(a, b, t)


def curve_keys(name):
    return props(name)["FloatCurve"]["Keys"]


def key_row(k):
    return f"{num(k['Time'])} -> {num(k['Value'], 4)}"


# ---------------------------------------------------------------- derived envelope
G = 9.81  # m/s^2, assumed
RHO = 1.25  # kg/m3: AirDensityAtSeaLevel 0.00125 read as g/cm3 (assumed unit)


def envelope():
    fc = props("DA_FWG_01_FlightCharacteristics")["AerodynamicSettings"]
    cl, cd = curve_keys("Curve_Symmetrical_LiftCoefFromAngleOfAttackDeg"), curve_keys("Curve_DragCoefFromAngleOfAttackDeg")
    foils = [a for a in fc["Airfoils"] if a["Name"] != "Airbrake"]  # airbrake force is 0 while retracted
    mult = fc["MainLiftMultiplier"]
    mass = props("DA_FWG_01_Body")["MassOverride"]
    thrust = props("DA_FWG_01_Engine")["MaxEngineThrust_n"]

    def sums(alpha):
        lift = sum(a["SurfaceArea_m"] * curve_value(cl, alpha + a["IncidenceAngle_deg"]) for a in foils if a["LiftForceDirection_LS"]["Z"] == 1.0) * mult
        drag = sum(a["SurfaceArea_m"] * curve_value(cd, alpha + a["IncidenceAngle_deg"]) for a in foils)
        return lift, drag

    best = max((sums(a / 10)[0], a / 10) for a in range(0, 300))
    smax, a_stall = best
    v_stall = math.sqrt(2 * mass * G / (RHO * smax))
    rows = []

    def level(v_ms):
        q = 0.5 * RHO * v_ms ** 2
        lo, hi = -2.0, a_stall
        for _ in range(60):
            a = (lo + hi) / 2
            if q * sums(a)[0] < mass * G:
                lo = a
            else:
                hi = a
        a = (lo + hi) / 2
        return a, q * sums(a)[1]

    for kmh in list(range(100, 1000, 50)):
        a, d = level(kmh / 3.6)
        rows.append((kmh, a, d, d / thrust))
    # speed where drag equals a given thrust fraction
    def speed_for(frac):
        lo, hi = v_stall, 400.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if level(mid)[1] < frac * thrust:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2 * 3.6

    by_thrust = [(p, speed_for(p / 100)) for p in range(10, 101, 10)]
    area_lift = sum(a["SurfaceArea_m"] for a in foils if a["LiftForceDirection_LS"]["Z"] == 1.0)
    return dict(mass=mass, thrust=thrust, mult=mult, smax=smax, a_stall=a_stall, v_stall=v_stall, rows=rows,
                by_thrust=by_thrust, area_lift=area_lift, area_all=sum(a["SurfaceArea_m"] for a in foils))


def trim_cross(keys):
    """Airspeed (km/h) where the auto-trim value reaches 0 after the plateau (linear between keys)."""
    for a, b in zip(keys, keys[1:]):
        if a["Time"] > 10 and a["Value"] > 1e-9 and b["Value"] <= 1e-9:
            return a["Time"] + (b["Time"] - a["Time"]) * a["Value"] / (a["Value"] - b["Value"])
    return None


# ---------------------------------------------------------------- page A: fixed wing
FM_HEAD = """---
title: "Fixed-wing flight model"
parent: "Vehicles"
description: "Every flight-model field of the fixed-wing airplane FWG_01 (engine, drag, lift and drag curves, nose-wheel steering, the 22-row auto-trim table, control assists)."
---

# Fixed-wing flight model (FWG_01)

*Source: the five `DA_FWG_01_*` flight assets, `Curve_Symmetrical_LiftCoefFromAngleOfAttackDeg`, `Curve_DragCoefFromAngleOfAttackDeg`, `Curve_FWG_01_NoseCenterWheel_SteeringInfluenceByForwardSpeedKmPH` and `CurveTable_FWG_01_AutoTrimByAirspeedKmPH` under `Content/Vehicles/Pawns/Air/Airplane/FWG_01/Data`. Generated by [`_tools/vehicle_round85_tables.py`](""" + GH + """_tools/vehicle_round85_tables.py). Evidence and status: [round 85 vehicles](""" + EVID + """).*

FWG_01 is the unfinished two-seat airplane described in [Fixed-wing airplane](../_wiki/vehicles/fixed-wing-airplane.md). [Vehicles (reference)](../content/Wardogs_Vehicles_v2.md) section 3 and 4 list its mass, thrust, airfoil areas and control mapping. This page adds the rest: the property names, the full drag and torque set, the curve keys, the auto-trim table and the control-assist stacks. The data stores **no top speed and no stall speed**; the speed figures in section 6 are read from the auto-trim table.
"""


def page_fixed_wing():
    out = [FM_HEAD]
    eng, drag, body = props("DA_FWG_01_Engine"), props("DA_FWG_01_Drag"), props("DA_FWG_01_Body")
    fch = air("DA_FWG_01_FlightCharacteristics")
    fp = fch[0]["Properties"]
    out.append("\n## 1. Engine and body (stored property names)\n")
    out.append(table(["Asset", "Property", "Value"],
                     [["`DA_FWG_01_Engine`", f"`{k}`", vec(v) if isinstance(v, dict) else num(v)] for k, v in eng.items()] +
                     [["`DA_FWG_01_Body`", f"`{k}`", vec(v) if isinstance(v, dict) else num(v)] for k, v in body.items()]))
    out.append("\nThe engine has one thrust vector and two limits, no thrust-by-speed curve and no fuel use of its own. Thrust is a straight 0 to 226,800 N range, scaled by the throttle control. Mass, inertia and thrust units are not stated in the export (read as kg and N below).\n")

    out.append("\n## 2. Drag (`DA_FWG_01_Drag`, `BHAirplaneDragDataAsset`)\n")
    rows = []
    for k, v in drag.items():
        rows.append([f"`{k}`", short(v) if isinstance(v, dict) else num(v)])
    out.append(table(["Property", "Value"], rows))
    out.append("\nThe two skid-angle curves live in the helicopter folder (`CF_YawDragAngle_AggressiveNearZero`, `CF_PitchDragAngle`); the airplane borrows them. The air density of 0.00125 is the sea-level value in g/cm3 (1.25 kg/m3) (unit reading assumed). How the native code multiplies the six area fields and the coefficient is not decoded.\n")

    lc, dc = curve_keys("Curve_Symmetrical_LiftCoefFromAngleOfAttackDeg"), curve_keys("Curve_DragCoefFromAngleOfAttackDeg")
    out.append("\n## 3. Lift and drag curves (angle of attack in degrees)\n")
    out.append("All twelve airfoils share these two curves (`LiftCoeffFromAngleOfAttackDeg_Curve`, `DragCoeffFromAngleOfAttackDeg_Curve`). The airfoil angle of attack is the airplane angle plus the airfoil `IncidenceAngle_deg` (wings and flaps 2 degrees, the airbrake -45).\n")
    out.append("\n**Lift coefficient** (`Curve_Symmetrical_LiftCoefFromAngleOfAttackDeg`, symmetric about 0):\n")
    out.append(table(["Angle (deg)", "Key value", "Interpolation"], [[num(k["Time"]), num(k["Value"], 3), k["InterpMode"].replace("RCIM_", "")] for k in lc]))
    out.append("\nDerived values between the keys (evaluated as an Unreal rich curve, cubic keys with their tangents):\n")
    angles = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 30, 35, 40, 45, 60, 90]
    out.append(table(["Angle (deg)"] + [str(x) for x in angles], [["Lift coefficient"] + [num(curve_value(lc, x), 2) for x in angles], ["Drag coefficient"] + [num(curve_value(dc, x), 3) for x in angles]]))
    out.append("\nThe curve climbs to 1.0 at 16 degrees, falls to 0.5 at 25 degrees (the stall) and rises again to 1.1 at 45 degrees (flat-plate behaviour), then returns to 0 at 90 degrees.\n")
    out.append("\n**Drag coefficient** (`Curve_DragCoefFromAngleOfAttackDeg`, five keys over -180 to 180 degrees):\n")
    out.append(table(["Angle (deg)", "Value", "Interpolation"], [[num(k["Time"], 4), num(k["Value"], 3), k["InterpMode"].replace("RCIM_", "")] for k in dc]))
    out.append("\nDrag is 0.01 edge-on and 2.5 broadside (90 degrees); the cubic keys make it rise slowly (see the derived row above).\n")

    sc = curve_keys("Curve_FWG_01_NoseCenterWheel_SteeringInfluenceByForwardSpeedKmPH")
    out.append("\n**Nose-wheel steering influence by forward speed** (`Curve_FWG_01_NoseCenterWheel_SteeringInfluenceByForwardSpeedKmPH`, km/h):\n")
    out.append(table(["Forward speed (km/h)", "Steering influence", "Interpolation"], [[num(k["Time"]), num(k["Value"], 3), k["InterpMode"].replace("RCIM_", "")] for k in sc]))
    out.append("\nThe value at 100 km/h is 4.8e-07, effectively 0. The nose wheel keeps full steering to 50 km/h and fades out by 100 km/h.\n")

    # landing gear
    out.append("\n## 4. Landing gear and other flight fields\n")
    gear = fp["LandingGear"]["WheelSystems"]
    out.append(table(["Side", "Braking strength", "Steering strength", "Steering damping", "Max steering angle (deg)", "Brake steering influence", "Bones (wheel / suspension / steer)"],
                     [[w["Side"].split("::")[-1], num(w.get("BrakingStrength")), num(w.get("SteeringStrength")), num(w.get("SteeringDamping")),
                       num(w.get("SteeringMaxAngleDeg")), num(w.get("BrakeSteeringInfluence")),
                       f"`{w.get('WheelBoneName')}` / `{w.get('SuspensionBoneName')}` / `{w.get('SteeringBoneName', '-')}`"] for w in gear]))
    out.append("\n" + table(["Property", "Value"], [
        ["`bEnableMaxAngularVelocity`", num(fp["bEnableMaxAngularVelocity"])],
        ["`MaxAngularVelocityDegPerS`", num(fp["MaxAngularVelocityDegPerS"])],
        ["`TranslationalLiftPercent`", num(fp["TranslationalLiftPercent"])],
        ["`TranslationalLiftMinAtHorizSpeed_mps` / `MaxAt`", f"{num(fp['TranslationalLiftMinAtHorizSpeed_mps'])} / {num(fp['TranslationalLiftMaxAtHorizSpeed_mps'])}"],
        ["`GroundEffectAltitude_m` / `GroundEffectFalloff_m` / `GroundEffectStrengthPercent`", f"{num(fp['GroundEffectAltitude_m'])} / {num(fp['GroundEffectFalloff_m'])} / {num(fp['GroundEffectStrengthPercent'])}"],
        ["`DefaultFMAssistanceLevel`", ", ".join(f"{k} = {num(v)}" for k, v in fp["DefaultFMAssistanceLevel"].items())],
        ["`PitchHoverAssistanceCurve`", f"`{short(fp['PitchHoverAssistanceCurve'])}` (helicopter folder)"],
        ["`RearRotorEfficiencyCurve`", f"`{short(fp['RearRotorEfficiencyCurve'])}` (helicopter folder)"],
        ["`GForceControlFalloffCurve`", f"`{short(fp['GForceControlFalloffCurve'])}` (helicopter folder)"],
        ["`AerodynamicSettings.MainLiftMultiplier`", num(fp["AerodynamicSettings"]["MainLiftMultiplier"])],
    ]))
    out.append("\nThe helicopter fields (translational lift, ground effect, rear rotor, hover assistance) were copied from the helicopter flight asset and carry helicopter values; ground effect is switched off (strength 0). The maximum angular velocity limit is disabled.\n")

    # assists
    byname = {}
    for e in fch[1:]:
        outer = e.get("Outer", {}).get("ObjectName", "")
        key = outer.split(":")[-1].rstrip("'") + "." + e["Name"] if outer else e["Name"]
        byname[key] = e

    def resolve(ref):
        key = ref["ObjectName"].split(":")[-1].rstrip("'")
        return byname.get(key)

    def describe(e):
        if not e:
            return "-"
        p = e.get("Properties") or {}
        t = e["Type"]
        t = t.replace("BH", "").replace("RotaryMovementControlAssist", "").replace("ControlAssist", "")
        bits = []
        for k, v in p.items():
            if isinstance(v, dict) and "ObjectName" in v:
                bits.append(f"{k} `{short(v)}`")
            elif isinstance(v, dict):
                bits.append(f"{k} " + ", ".join(f"{a}={num(b) if not isinstance(b, str) else b.split('::')[-1]}" for a, b in v.items()))
            elif isinstance(v, list):
                bits.append(f"{k} ({len(v)})")
            elif isinstance(v, str):
                bits.append(f"{k} {v.split('::')[-1]}")
            else:
                bits.append(f"{k} {num(v)}")
        return f"{t}: " + "; ".join(bits) if bits else t

    out.append("\n## 5. Control assists\n")
    out.append("Each control is a `BHRotaryMovementControl` with a stack of assists (a category, a label, optional conditions, and a body). Flap and airbrake controls have none. Values are as stored; the gain units are not stated.\n")
    arows = []
    for cname, ctrl in (("Throttle", "ThrottleControl"), ("Pitch", "PitchControl"), ("Roll", "RollControl"), ("Yaw", "YawControl"), ("Wheel brake", "WheelBrakeControl")):
        ref = fp[ctrl]
        c = resolve(ref) if False else None
        ckey = ref["ObjectName"].split(":")[-1].rstrip("'")
        for e in fch[1:]:
            if e["Name"] == ckey and e["Type"] == "BHRotaryMovementControl":
                c = e
        for a in (c.get("Properties") or {}).get("Assists", []) if c else []:
            conds = "; ".join(describe(resolve(r)) for r in a.get("Conditions", [])) or "none"
            body = describe(resolve(a["Body"])) if a.get("Body") else "-"
            arows.append([cname, a.get("Label", "-"), "on" if a.get("bEnabled") else "off", conds.replace("|", "/"), body.replace("|", "/")])
    out.append(table(["Control", "Assist label", "Enabled", "Conditions", "Body"], arows))
    out.append("\nThe pitch auto-trim assist is the one that samples the 22-row table in section 6a.\n")

    # auto trim
    ct = air("CurveTable_FWG_01_AutoTrimByAirspeedKmPH")[0]
    rows = ct["Rows"]
    out.append("\n## 6. Auto-trim table and speed figures\n")
    out.append("### 6a. Auto-trim table (`CurveTable_FWG_01_AutoTrimByAirspeedKmPH`)\n")
    out.append("The pitch assist samples one of 22 curves; the row names are `Gear_{0,1}_Thrust_{0..100 step 10}`, so the curve is picked by landing-gear state and throttle in tens of percent (the pick rule is native and not decoded). Each curve maps airspeed in km/h to a pitch-control trim value (stored as shown, unit not stated). Every curve rises to +0.2 within 10 km/h, holds it up to a throttle-dependent speed, then falls through 0 and ends at -0.08 or -0.09 at 1200 km/h. The throttle-0 rows are flat at -0.09. All keys are linear.\n")
    gear = {"Gear_1": "1", "Gear_0": "0"}
    trows = []
    cross = {}
    for g in ("Gear_1", "Gear_0"):
        for p in range(100, -1, -10):
            r = rows[f"{g}_Thrust_{p}"]["Keys"]
            x = trim_cross(r) if p else None
            cross[(g, p)] = x
            plateau = [k for k in r if k["Value"] >= 0.2 - 1e-6]
            trows.append([f"`{g}_Thrust_{p}`", len(r),
                          num(plateau[-1]["Time"]) if plateau and p else "-",
                          num(x, 0) if x is not None else "-",
                          num(r[-1]["Value"], 2)])
    out.append(table(["Row", "Keys", "Holds +0.2 up to (km/h)", "Falls to 0 at (km/h, derived)", "Value at 1200 km/h"], trows))
    out.append("\nThe zero crossing is the airspeed where the assist asks for no pitch trim at that throttle, which is the speed the designers expected the airplane to hold level at that throttle. It rises from about 140 km/h at 10% to 430 km/h at 100% with the gear up (gear down: 135 to 430 km/h). At 100% the curve reaches zero at 430 and stays there until 440, which is the value the table column shows; at lower throttles the column is the point where the curve leaves zero. Which of the two row sets is the gear-up one is read from the row names (`Gear_1`) and was not confirmed in code. The full key list of every row is in the export; keys are 10 km/h apart or wider.\n")

    out.append("\n### 6b. Speed figures\n")
    out.append("The data stores no top speed and no stall speed. The only speed figures it gives are the zero crossings read from the auto-trim table in 6a: the speed where no pitch trim is asked for, 140 km/h at 10% throttle and 430 km/h at 100% throttle with the gear up (135 and 430 km/h with the gear down). They are read from the table, not stored as a limit.\n")
    out.append("\n## See also\n\n- [Fixed-wing airplane](../_wiki/vehicles/fixed-wing-airplane.md)\n- [Vehicles (reference)](../content/Wardogs_Vehicles_v2.md)\n- [Vehicle parts and handling](Wardogs_VehicleHandling_v1.md)\n- [Vehicle curves](Wardogs_VehicleCurves_v1.md)\n- [Vehicle config fields](Wardogs_VehicleConfigFields_v1.md)\n")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- page B: config fields
CFG_HEAD = """---
title: "Vehicle config fields"
parent: "Vehicles"
description: "Config sub-fields for wheeled, tracked and rotary vehicles, tracked wheel data, helicopter flight and drag assets, and the fuel settings (km per litre, idle burn, boost) for every vehicle."
---

# Vehicle config fields

*Source: the `*VehicleConfigDataAsset`, `MTrackedVehicleWheelData`, `BHRotaryFlightDataAsset`, `BHAirVehicleDragDataAsset` and `WDVehicleGameplayComponentsDataAsset` exports under the vehicle plugins. Generated by [`_tools/vehicle_round85_tables.py`](""" + GH + """_tools/vehicle_round85_tables.py). Evidence and status: [round 85 vehicles](""" + EVID + """).*

[Vehicle parts and handling](Wardogs_VehicleHandling_v1.md) holds the engine, axle, wheel and suspension tables. This page adds the fields it leaves out. `-` means the asset does not set the field (a native default applies, see the defaults section of that page).
"""

# fuel formulas are derived from the native tick at RVA 0x7666FA0 (sub_147666FA0) and sub_147665DB0
def page_config():
    allx = list(veh_exports())
    out = [CFG_HEAD]

    def by_type(t):
        return [(p, e) for p, e in allx if e.get("Type") == t]

    def vname(p, e):
        return e["Name"]

    # wheeled
    out.append("\n## 1. Wheeled vehicle config (`MWheeledVehicleConfigDataAsset`)\n")
    rows = []
    for p, e in by_type("MWheeledVehicleConfigDataAsset"):
        P = e["Properties"]
        tr = P.get("FirstPersonSpringArmComponentTransform", {}).get("Translation")
        rows.append([f"`{e['Name']}`", num(P.get("HornMinimumHoldTime")), num(P.get("LengthOfGroundTrace")), num(P.get("bHideOccupantsInFirstPerson")),
                     num(P.get("MovingEffectSpeedThreshold")), vec(tr), f"`{short(P.get('ExitVehicleDamageType'))}`",
                     f"`{short(P.get('_aaabljnlghahlkidgdeii'))}`", f"`{short(P.get('VehicleExitDamageCurve'))}`"])
    out.append(table(["Asset", "Horn min hold (s)", "Ground trace length", "Hide occupants in first person", "Moving-effect speed threshold", "First-person camera offset", "Exit damage type", "Prediction settings", "Exit damage curve"], rows))
    out.append("\nThe exit damage type is the same `WDImpactDamageType` everywhere. Gameplay cue tags (engine, collision, moving, horn, destroyed) are cosmetic and are listed in the export only.\n")

    out.append("\n## 2. Tracked vehicle config (`MTrackedVehicleConfigDataAsset`)\n")
    rows = []
    for p, e in by_type("MTrackedVehicleConfigDataAsset"):
        P = e["Properties"]
        tr = P.get("ThirdPersonSpringArmComponentTransform", {}).get("Translation")
        rows.append([f"`{e['Name']}`", num(P.get("HornMinimumHoldTime")), num(P.get("MovingEffectSpeedThreshold")), num(P.get("MovingEffectAngularSpeedThreshold")), vec(tr),
                     (f"`{short(P.get('_aaabljnlghahlkidgdeii'))}`" if P.get('_aaabljnlghahlkidgdeii') else "-")])
    out.append(table(["Asset", "Horn min hold (s)", "Moving-effect speed threshold", "Moving-effect angular threshold", "Third-person camera offset", "Prediction settings"], rows))

    out.append("\n### Tracked wheel data (`MTrackedVehicleWheelData`)\n")
    rows = []
    for p, e in by_type("MTrackedVehicleWheelData"):
        P = e["Properties"]
        tm = P.get("TireModel", {})
        rows.append([f"`{e['Name']}`", num(P.get("SuspensionLength")), num(P.get("WheelRadius")), num(P.get("SpringRate")), num(P.get("DampingCompress")), num(P.get("DampingRebound")),
                     num(P.get("MaxInclineAngle")), vec(P.get("InclineGripMultiplier")), num(tm.get("FrictionMultiplierLateral")), num(tm.get("SteeringFrictionReductionMultiplier")), num(P.get("_aaabodchgifaioegpnmah"))])
    out.append(table(["Asset", "Suspension length", "Wheel radius", "Spring rate", "Damping compress", "Damping rebound", "Max incline (deg)", "Incline grip multiplier (X, Y, Z)", "Lateral friction", "Steering friction reduction", "Unnamed float (`_aaabodchgifaioegpnmah`)"], rows))
    out.append("\nThe tracks share the spring rate (112,500), damping (12,000 / 17,000), suspension length (40) and 50 degree incline limit; they differ in wheel radius (SPW 38, TNK_01 35, TNK_04 40.5) and lateral friction (3.5, 3.25, 3.335). SPW_01 sets no steering friction reduction (native default).\n")

    out.append("\n## 3. Rotary vehicle config and flight (`BHRotaryVehicleConfigDataAsset`, `BHRotaryFlightDataAsset`)\n")
    rows = []
    for p, e in by_type("BHRotaryVehicleConfigDataAsset"):
        P = e["Properties"]
        rows.append([f"`{e['Name']}`", f"`{short(P.get('RotaryEngineDataAsset'))}`", f"`{short(P.get('RotaryVehicleDragDataAsset'))}`", f"`{short(P.get('RotaryVehicleFlightCharacteristicsDataAsset'))}`",
                     f"`{short(P.get('RotorMaterialCurve'))}`", f"`{short(P.get('RotorReturnMeshCurve'))}`", f"`{short(P.get('TailRotorMaterialCurve'))}`"])
    out.append(table(["Asset", "Engine", "Drag", "Flight characteristics", "Rotor material curve", "Rotor return mesh curve", "Tail rotor material curve"], rows))
    out.append("\n**Flight characteristics scalars:**\n")
    rows = []
    for p, e in by_type("BHRotaryFlightDataAsset"):
        P = e["Properties"]
        rs = P.get("RotorSettings", {})
        rows.append([f"`{e['Name']}`", num(rs.get("RotorRadius")), num(rs.get("MaxLiftCoeff")), num(rs.get("BladeAngleOfAttackForStall_deg")), num(rs.get("LowAltitude_m")), num(rs.get("HighAltitude_m")),
                     num(P.get("CyclicAttenuationFactor")), num(P.get("GroundEffectStrengthPercent")), num(P.get("GroundEffectFalloff_m")), num(P.get("GroundEffectExp")),
                     f"{num(P.get('TranslationalLiftPercent'))}% over {num(P.get('TranslationalLiftMinAtHorizSpeed_mps'))} to {num(P.get('TranslationalLiftMaxAtHorizSpeed_mps'))} m/s",
                     num(P.get("MaxAngularVelocityDegPerS")) + (" (on)" if P.get("bEnableMaxAngularVelocity") else " (off)")])
    out.append(table(["Asset", "Rotor radius", "Max lift coeff", "Stall blade angle (deg)", "Low alt (m)", "High alt (m)", "Cyclic attenuation", "Ground effect %", "Falloff (m)", "Exponent", "Translational lift", "Max angular velocity (deg/s)"], rows))
    out.append("\n**Control forces:**\n")
    rows = []
    for p, e in by_type("BHRotaryFlightDataAsset"):
        P = e["Properties"]
        for c in ("PitchControlForce", "RollControlForce", "YawControlForce", "CollectiveControlForce"):
            f = P.get(c)
            if f:
                rows.append([f"`{e['Name']}`", c.replace("ControlForce", ""), (f.get("Type") or "-").split("::")[-1], num(f.get("MaxTorque")), num(f.get("MinForce")), num(f.get("MaxForce")),
                             num(f.get("MinRotorBladeAngleDelta")), num(f.get("MaxRotorBladeAngleDelta"))])
    out.append(table(["Asset", "Control", "Type", "Max torque", "Min force", "Max force", "Min blade delta", "Max blade delta"], rows))

    out.append("\n## 4. Air drag (`BHAirVehicleDragDataAsset`, `BHAirplaneDragDataAsset`)\n")
    cols = ["AirDensityAtSeaLevel", "FrontDragArea", "RearDragArea", "SideArea", "BottomArea", "TopArea", "DragCoefficient", "YawAngularVelocityInducedDragTorqueCoef", "PitchAngularVelocityInducedDragTorqueCoef",
            "RollAngularVelocityInducedDragTorqueCoef", "YawLinearVelocityInducedDragTorqueCoef", "PitchLinearVelocityInducedDragTorqueCoef", "RollLinearVelocityInducedDragTorqueCoef", "ReverseYawCorrectionCoef"]
    dr = by_type("BHAirVehicleDragDataAsset") + by_type("BHAirplaneDragDataAsset")
    names = [e["Name"].replace("DA_", "").replace("DragDataAsset", "Drag") for p, e in dr]
    out.append(table(["Property"] + [f"`{n}`" for n in names], [[f"`{c}`"] + [num(e["Properties"].get(c)) for p, e in dr] for c in cols]))
    out.append("\nThe 2000 KG light drag asset is shared by ROT_03 and its rocket-pod variant (identical values). All five assets have `bDrawDragDebugLines` true. Against Havoc (ROT_02) the airplane has the same front area and coefficient, a 4 times larger top and bottom area (2,800,000 against 700,000), 10 times larger angular-velocity torque coefficients (yaw, pitch, roll) and a smaller rear and side area. What the area fields mean in the native formula is not decoded.\n")

    # fuel
    out.append("\n## 5. Fuel settings (`FuelSettings` in each `*GameplaySystems` asset)\n")
    rows = []
    kml_all = []
    for p, e in allx:
        if e.get("Type") == "WDVehicleGameplayComponentsDataAsset":
            fs = (e.get("Properties") or {}).get("FuelSettings")
            if fs:
                kml = fs.get("KML")
                mf = fs.get("MaxFuel")
                rows.append([f"`{e['Name']}`", num(mf), num(kml), num(1 / kml, 2) if kml else "-", num(mf * kml, 1) if (kml and mf) else "-", num(fs.get("RPML")),
                             num(fs.get("FuelConsumptionOnBoostMultiplier")), num(fs.get("FuelInteractionRange"))])
    out.append(table(["Asset", "Max fuel (L)", "KML (km per litre)", "Listed economy = 1/KML (L/km, derived)", "Range on a full tank (km, derived)", "RPML", "Boost multiplier", "Refuel interaction range"], rows))
    out.append("\n**What the fields do.** The fuel component's tick (native `0x7666FA0`, round 85) subtracts `rate x dt + leak x dt` from the fuel attribute each frame while the owning vehicle is in state 3 (presumably the running state; the state names were not traced) and the component is not flagged off. The `rate` term is only added when one more owner check passes (a native call that was not decoded); the `leak` term does not depend on it. `rate` comes from `0x7665DB0`:\n")
    out.append("- Moving: `rate = speed(km/h) / 3600 / KML` litres per second, so a vehicle burns 1/KML litres per kilometre and `Max fuel x KML` kilometres is the range on a full tank (derived).\n- At or below the idle speed threshold the rate switches to a second per-vehicle reading (probably engine RPM, read through another virtual call) divided by `RPML` instead of `KML`; the threshold is a native field (`IdleSpeedThreshold`) the cooked assets never set, so its default is not known here.\n- The rate is multiplied by the boost multiplier while boosting, and by a fuel-usage multiplier from character skills (`FuelUsageReduction`, see the Driver and Pilot skill tables).\n- `leak` is the stored fuel-leak value set by the fuel-tank damage effects (0.1 to 3.0 litres per second, see [Fuel and refueling](../_wiki/vehicles/fuel-and-refueling.md)).\n")
    out.append("\nWhich settings field each native slot holds is inferred from how the value is used, not from a decoded constructor. The listed economy in the vendor stats equals 1/KML for most vehicles (Havoc 4.4, Humvee 3.3, Kodiak 2.9, Bobcat 2.2, Dune Buggy 5.0, Ural 4.0, M113 5.7, SPH-2 and L2A6 8.0, Gepard 10.0); the T-72B3 is the exception (vendor 8.5, 1/KML 6.96). The airplane sets no fuel settings at all.\n")
    out.append("\n## See also\n\n- [Vehicle parts and handling](Wardogs_VehicleHandling_v1.md)\n- [Fixed-wing flight model](Wardogs_FixedWingFlightModel_v1.md)\n- [Fuel and refueling](../_wiki/vehicles/fuel-and-refueling.md)\n- [Refuel and Repair Stations](../_wiki/building/refuel-and-repair-stations.md)\n")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- page C: turrets
TUR_HEAD = """---
title: "Vehicle turret controls"
parent: "Vehicles"
description: "The 23 vehicle weapon data assets (mouse and gamepad rotation limits, yaw and pitch limits, muzzle sockets, aim cameras with zeroing distance) and the vehicle crosshair tables."
---

# Vehicle turret controls

*Source: every `WDVehicleWeaponDataAsset` and every `DT_VehicleCrosshair_*` table under `Plugins/GameFeatures/Vehicles`. Generated by [`_tools/vehicle_round85_tables.py`](""" + GH + """_tools/vehicle_round85_tables.py). Evidence and status: [round 85 vehicles](""" + EVID + """).*

Each vehicle weapon is a `WDVehicleWeaponDataAsset` (`W_*`) that holds the weapon tag, the turret mesh, the muzzle sockets, the aim-rotation settings and the camera for each aim state. The damage and ballistics are on the `WE_*` weapon-extension assets, which are covered in [Vehicle weapons and effects](Wardogs_VehicleWeaponsEffects_v1.md). `-` means the asset does not set the field.
"""


def page_turrets():
    out = [TUR_HEAD]
    ws = []
    for p, e in veh_exports():
        if e.get("Type") == "WDVehicleWeaponDataAsset":
            ws.append((p, e))
    ws.sort(key=lambda x: x[0])

    def vehicle(p):
        return p.split("/GameFeatures/Vehicles/")[1].split("/")[0] if "/GameFeatures/Vehicles/" in p else p

    out.append("\n## 1. Rotation sensitivity and limits\n")
    out.append("Sensitivity and update-max values are per input device (X, Y). Yaw and pitch limits are in degrees; a limit is only enforced when its `bLimit...` flag is true. Rotation speed is the turret slew speed in degrees per second.\n")
    rows = []
    for p, e in ws:
        P = e["Properties"]
        R = P.get("WeaponRotationComponentData", {})
        gm, mm = P.get("GamepadRotationUpdateMax"), P.get("MouseRotationUpdateMax")
        rows.append([f"`{e['Name']}`", vehicle(p), f"`{tag(P.get('WeaponTag'))}`", num(P.get("MouseRotationSensitivity")), f"{num(mm['X']) if mm else '-'} / {num(mm['Y']) if mm else '-'}",
                     num(P.get("GamepadRotationSensitivity")), f"{num(gm['X']) if gm else '-'} / {num(gm['Y']) if gm else '-'}", num(P.get("KeyRotationSensitivity")),
                     num(P.get("bAllowKeyRotation")), num(P.get("bApplyFovScale"))])
    out.append(table(["Asset", "Vehicle", "Weapon tag", "Mouse sens.", "Mouse update max (X / Y)", "Gamepad sens.", "Gamepad update max (X / Y)", "Key sens.", "Key rotation allowed", "Apply FOV scale"], rows))
    out.append("")
    rows = []
    for p, e in ws:
        P = e["Properties"]
        R = P.get("WeaponRotationComponentData", {})

        def lim(flag, lo, hi):
            return f"{num(R.get(lo))} to {num(R.get(hi))}" + ("" if R.get(flag) else " (limit flag not set)")
        rows.append([f"`{e['Name']}`", lim("bLimitWeaponYaw", "MinWeaponYawAngle", "MaxWeaponYawAngle"), lim("bLimitWeaponPitch", "MinWeaponPitchAngle", "MaxWeaponPitchAngle"),
                     num(R.get("RotationSpeed")), (R.get("SimulationType") or "-").split("::")[-1],
                     num(R.get("YawDriveStrength")) + " / " + num(R.get("PitchDriveStrength")), num(R.get("bStabilisationPermitted")), num(R.get("CollisionTargetFactor"))])
    out.append(table(["Asset", "Yaw (deg)", "Pitch (deg)", "Rotation speed", "Simulation", "Yaw / pitch drive strength", "Stabilisation permitted", "Collision target factor"], rows))
    out.append("\n`FullSim` (a physically simulated turret with drive strength and damping) is used by the Havoc 30 mm cannon and the four tank main guns (TNK_03, TNK_01 Artillery and Heavy, TNK_04); every other weapon uses a plain rotation speed. Where the minimum yaw is larger than the maximum (STN_01: 90 and -90) the pair is stored in that order and the limit flag is unset; read it as a +/- 90 degree arc (the engine behaviour for an unset flag is not traced).\n")

    out.append("\n## 2. Sockets, view and HUD\n")
    rows = []
    for p, e in ws:
        P = e["Properties"]
        pa = P.get("PlayerAttachSocket") or {}
        rows.append([f"`{e['Name']}`", ", ".join(f"`{s}`" for s in P.get("MuzzleSockets", [])) or "-", f"`{pa.get('SourceId', '-')}` / `{pa.get('SocketName', '-')}`",
                     f"`{short(P.get('SkeletalMeshAsset'))}`", tag(P.get("HUDLayoutTag")).replace("UI.HUD.Layout.Vehicle.", ""), num(P.get("HUDScopeBlurAlpha")),
                     num(P.get("bUseWeaponAsViewTarget")), num(P.get("InitialWeaponPossessFovLerpTime")), len(P.get("WeaponExtensionsDataAssets", []))])
    out.append(table(["Asset", "Muzzle sockets", "Player attach (source / socket)", "Turret mesh", "HUD layout", "Scope blur alpha", "Weapon as view target", "Possess FOV lerp (s)", "Weapon extensions"], rows))

    out.append("\n## 3. Aim cameras\n")
    out.append("`WeaponStatesCameraData` has one entry per aim state (`State.Vehicle.Weapon.HipFire`, `.ADS`). `Zeroing` is the distance the aim point is aligned to when `bAlignWithTarget` is true; `FOV x` is the field-of-view multiplier of that state.\n")
    rows = []
    for p, e in ws:
        for ent in e["Properties"].get("WeaponStatesCameraData", []):
            v = ent["Value"]
            q = v.get("AttachQuery", {})
            rows.append([f"`{e['Name']}`", tag(ent["Key"]).split(".")[-1], num(v.get("bSupported")), f"`{q.get('SocketName', '-')}`", num(v.get("bAlignWithTarget")), num(v.get("ZeroingDistance")), num(v.get("FOVMultiplier")),
                         f"`{short(v.get('CameraBehaviourData'))}`" if v.get("CameraBehaviourData") else "-"])
    out.append(table(["Asset", "State", "Supported", "Camera socket", "Align with target", "Zeroing", "FOV x", "Camera behaviour"], rows))
    with_cam = {e["Name"] for p, e in ws if e["Properties"].get("WeaponStatesCameraData")}
    out.append("\nWeapons with no camera states: " + ", ".join(f"`{e['Name']}`" for p, e in ws if e["Name"] not in with_cam) + ".\n")

    out.append("\n## 4. Crosshair tables (`DT_VehicleCrosshair_*`)\n")
    out.append("There are eight `DT_VehicleCrosshair_*` tables. Each is a `DataTable` of `WDUIVehicleCrosshairDataTableRow`: a row per weapon-extension tag, with the widget class that draws the reticle, the view model class, and an unnamed flag. Only the names are listed; the reticle art is out of scope.\n")
    rows = []
    for p in sorted(glob.glob(os.path.join(VEH, "**", "DT_VehicleCrosshair_*.json"), recursive=True)):
        for e in exports(p):
            for rn, r in e.get("Rows", {}).items():
                pr = r["Params"]
                w = pr.get("WidgetClass", {}).get("AssetPathName", "")
                vm = pr.get("ViewModelParams", {}).get("ViewModelClass", {}).get("AssetPathName", "")
                rows.append([f"`{e['Name']}`", f"`{rn}`", f"`{short(w.split('.')[-1])}`" if w else "none (default reticle)", f"`{vm.split('.')[-1]}`" if vm else "-",
                             num(pr.get("_aaabkejhohfkdpglkgkep"))])
    out.append(table(["Table", "Row (weapon extension tag)", "Reticle widget", "View model", "Unnamed flag"], rows))
    n_none = sum(1 for r in rows if r[2].startswith("none"))
    tabs = sorted({r[0] for r in rows})
    empty = [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(VEH, "**", "DT_VehicleCrosshair_*.json"), recursive=True)) if f"`{os.path.basename(p)[:-5]}`" not in tabs]
    out.append(f"\n{len(rows)} rows in {len(tabs)} tables with rows; the tables {', '.join('`' + t + '`' for t in empty)} exist but have no rows. {n_none} row has no widget class and uses the default reticle. All rows use the same view model class and have the unnamed flag false.\n")
    out.append("\n## See also\n\n- [Vehicle weapons and effects](Wardogs_VehicleWeaponsEffects_v1.md)\n- [Data tables](../content/Wardogs_DataTables_v1.md)\n- [Vehicle config fields](Wardogs_VehicleConfigFields_v1.md)\n")
    return "\n".join(out) + "\n"


PAGES = {
    "game-features/Wardogs_FixedWingFlightModel_v1.md": page_fixed_wing,
    "game-features/Wardogs_VehicleConfigFields_v1.md": page_config,
    "game-features/Wardogs_VehicleTurretControls_v1.md": page_turrets,
}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--write"
    stale = 0
    for rel, fn in PAGES.items():
        text = fn()
        path = os.path.join(ROOT, rel)
        old = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8", newline="") as f:
                old = f.read().replace("\r\n", "\n")
        if mode == "--check":
            if old != text:
                print("stale:", rel)
                stale += 1
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("wrote", rel, len(text.splitlines()), "lines")
    if mode == "--check":
        sys.exit(1 if stale else 0)


if __name__ == "__main__":
    main()
