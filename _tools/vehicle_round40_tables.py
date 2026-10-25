"""Round 40 vehicle control tables: wheeled arcade-assist settings and helicopter flight-assist objects, rebuilt from data/.

Writes three files under assets/data/ and one page (idempotent; rerun gives byte-identical output):

    vehicle-arcade-controls.json   every MWheeledVehicleArcadeDataAsset (DA_ArcadeControls_*): the properties the asset stores, nothing else.
    vehicle-rotary-assists.json    every BHRotaryFlightDataAsset (ROT_02, ROT_03, ROT_04 flight characteristics): rotor settings, control
                                   forces, and for each of the four controls (pitch, roll, yaw, collective) the assist list with category,
                                   label, enabled flag, output mode, the condition objects and the body object (resolved by object name).
    vehicle-tire-models.json       every MWheeledVehicleTireModelSimpleDataAsset: the eight coefficients and the peaks of the preview curves.
    game-features/Wardogs_VehicleControlAssists_v1.md   the page built from the two files.

    python _tools/vehicle_round40_tables.py --write     # (re)write both JSON files and the page
    python _tools/vehicle_round40_tables.py --check      # exit 1 when a file is stale
    python _tools/vehicle_round40_tables.py              # print counts

Inputs: data/Wardogs/Plugins/GameFeatures/Vehicles/**. Evidence: docs/evidence/round40-vehicles-explosives.md.
Standard library only; run with python -I.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VEH = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Vehicles")
OUT = os.path.join(ROOT, "assets", "data")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_VehicleControlAssists_v1.md")
REPO = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"
CONTROLS = ("PitchControl", "RollControl", "YawControl", "CollectiveControl")


def load(path):
    """Read a dumped package: one JSON value or several concatenated ones, optionally after a '--- export:' line."""
    text = open(path, encoding="utf8").read()
    dec, i, out = json.JSONDecoder(), 0, []
    while i < len(text):
        while i < len(text) and text[i] in " \r\n\t,[]":
            i += 1
        if i >= len(text):
            break
        if text.startswith("---", i):
            i = text.index("\n", i) + 1
            continue
        obj, i = dec.raw_decode(text, i)
        out.append(obj)
    return out


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def short(v):
    """EBHFoo::Bar -> Bar."""
    return v.split("::")[-1] if isinstance(v, str) else v


def obj_key(ref):
    """'Type'Asset:Outer.Name'' -> (Outer, Name) so a reference finds its sub-object."""
    m = re.search(r":([^.']+)\.([^']+)'", (ref or {}).get("ObjectName", ""))
    return (m.group(1), m.group(2)) if m else None


def clean(props):
    out = {}
    for k, v in props.items():
        if isinstance(v, str):
            v = short(v)
        elif isinstance(v, dict):
            v = clean(v)
        out[k] = v
    return out


def arcade():
    rows = []
    for path in sorted(glob.glob(os.path.join(VEH, "*", "Content", "Data", "DA_ArcadeControls_*.json"))):
        for o in load(path):
            if o.get("Type") == "MWheeledVehicleArcadeDataAsset":
                rows.append({"asset": o["Name"], "vehicle": rel(path).split("/Vehicles/")[1].split("/")[0],
                             "properties": o.get("Properties", {})})
    return rows


def curve_summary(c):
    """Peak of an editor float curve: (slip at peak force, peak force, first key time, last key time, key count)."""
    keys = c.get("EditorCurveData", {}).get("Keys", [])
    if not keys:
        return None
    best = max(keys, key=lambda k: abs(k["Value"]))
    return {"keys": len(keys), "from": keys[0]["Time"], "to": keys[-1]["Time"], "peakAt": round(best["Time"], 3), "peakValue": round(best["Value"], 1)}


def tires():
    rows = []
    for path in sorted(glob.glob(os.path.join(VEH, "*", "Content", "Data", "*Tire*Model*.json"))):
        for o in load(path):
            if o.get("Type") == "MWheeledVehicleTireModelSimpleDataAsset":
                p = o["Properties"]
                rows.append({"asset": o["Name"], "vehicle": rel(path).split("/Vehicles/")[1].split("/")[0],
                             "coefficients": {k: v for k, v in p.items() if not isinstance(v, (dict, list))},
                             "longitudinalCurve": curve_summary(p.get("LongitudinalPreviewCurve", {})),
                             "lateralCurve": curve_summary(p.get("LateralPreviewCurve", {}))})
    return rows


def describe_condition(o):
    t = short(o["Type"]).replace("BH", "", 1).replace("RotaryMovementControlAssist", "").replace("ControlAssist", "")
    for suf in ("Condition", "Body"):
        if t.endswith(suf):
            t = t[:-len(suf)]
    p = clean(o.get("Properties", {}))
    d = {"type": t}
    d.update(p)
    return d


def rotary():
    rows = []
    paths = sorted(glob.glob(os.path.join(VEH, "ROT_0*", "Content", "Data", "*FlightCharacteristics*.json")))
    for path in paths:
        objs = load(path)
        top = next(o for o in objs if o.get("Type") == "BHRotaryFlightDataAsset")
        sub = {}
        for o in objs:
            k = obj_key({"ObjectName": "x:%s.%s'" % (o.get("Outer", {}).get("ObjectName", "").split(":")[-1].rstrip("'"), o.get("Name"))})
            if k:
                sub[k] = o
        p = top["Properties"]
        entry = {"asset": top["Name"], "vehicle": rel(path).split("/Vehicles/")[1].split("/")[0],
                 "rotorSettings": p.get("RotorSettings", {}),
                 "forces": {k: clean(p[k]) for k in p if k.endswith("Force") and isinstance(p[k], dict)},
                 "controls": {}}
        for cname in CONTROLS:
            ref = p.get(cname)
            ctl = next((o for o in objs if o.get("Name", "").startswith(cname + "_") and "Assists" in o.get("Properties", {})), None)
            if not ref or not ctl:
                continue
            assists = []
            for a in ctl["Properties"].get("Assists", []):
                conds = []
                for c in a.get("Conditions", []):
                    k = obj_key(c)
                    conds.append(describe_condition(sub[k]) if k in sub else {"type": "unresolved"})
                body = a.get("Body")
                bk = obj_key(body) if body else None
                bd = describe_condition(sub[bk]) if bk in sub else None
                assists.append({"label": a.get("Label", ""), "category": short(a.get("Category", "")), "enabled": a.get("bEnabled", False),
                                "outputMode": short(a.get("OutputMode", "")), "conditions": conds, "body": bd})
            entry["controls"][cname] = {"assists": assists}
        rows.append(entry)
    return rows


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def g(v):
    return ("%g" % v) if isinstance(v, float) else str(v)


ARC_COLS = [
    ("UnderSteerRecoverPower", "Understeer recover"), ("OverSteerRecoverPower", "Oversteer recover"),
    ("MinRecoverAssistSpeed", "Recover min speed"), ("FullRecoverAssistSpeed", "Recover full speed"),
    ("bEnableDriftAssist", "Drift assist"), ("DriftAssistFrontRatio", "Drift front"), ("DriftAssistRearRatio", "Drift rear"),
    ("FrontAntiRollPower", "Front anti-roll"), ("RearAntiRollPower", "Rear anti-roll"), ("AntiRollSpring", "Anti-roll spring"),
    ("DamperSmooth", "Damper smooth"), ("TractionAssistRatio", "Traction ratio"), ("TractionAssistMaxSpeed", "Traction max speed"),
    ("TorqueSplitterRatio", "Torque splitter"), ("bEnableBalanceAssist", "Balance assist"),
    ("MinLeanSpeed", "Lean min speed"), ("MaxLeanAngle", "Max lean angle"), ("MaxPitchAngle", "Max pitch angle"), ("bCanLeanInAir", "Lean in air"),
    ("bEnablePredictiveLanding", "Predictive landing"), ("MaxPredictTime", "Predict time (s)"), ("ExtraTimeBuffer", "Extra time buffer (s)"),
    ("MaxRollTorque", "Air roll torque"), ("MaxPitchTorque", "Air pitch torque"), ("AirborneDamping", "Airborne damping"),
]


def cond_text(c):
    t = c["type"]
    if t == "ControlValueSatisfies":
        txt = "%s %s %s %s" % (short(c.get("ControlValueType", "")), short(c.get("ControlValueComponent", "")),
                               {"GreaterThan": ">", "LessThan": "<", "Equal": "="}.get(short(c.get("TestOperator", "")), short(c.get("TestOperator", ""))),
                               g(c.get("TestValue", 0.0)))
        return txt + (" (%s)" % c["Label"] if c.get("Label") else "")
    if t == "InputState":
        return "input %s %s %s" % (short(c.get("ControlType", "")), "=" if short(c.get("Operator", "")) == "Equal" else short(c.get("Operator", "")), g(c.get("Threshold", 0.0)))
    if t == "StabilizedAfterInputReleased":
        return "stable (%s %s below %s%s)" % (short(c.get("StabilityControlValueType", "")), short(c.get("StabilityControlValueComponent", "")),
                                             g(c.get("StabilityThreshold", 0.0)), ", for %s s" % g(c["TimeThresholdS"]) if "TimeThresholdS" in c else "")
    return {"IsOnGround": "on ground", "WasOnGroundAtStart": "was on ground at start", "HasPilot": "has pilot"}.get(t, t)


def body_text(b):
    if not b:
        return "-"
    t = b["type"]
    if t.startswith("PID"):
        pid = b.get("PID", {})
        s = "PID P %s I %s D %s" % (g(pid.get("ProportionalGain", 0.0)), g(pid.get("IntegralGain", 0.0)), g(pid.get("DerivativeGain", 0.0)))
        cv = b.get("ControlValueParams", {})
        s += " on %s %s" % (short(cv.get("Type", "")), short(cv.get("Component", "")))
        tv = b.get("TargetParams", {}).get("Value")
        if tv is not None:
            s += " target %s" % g(tv)
        mo = b.get("OutputParams", {}).get("MaxPIDOutput")
        if mo is not None:
            s += " max out %s" % g(mo)
        return s
    if t.startswith("SetToValue"):
        return "set to %s" % g(b.get("Value", 0.0))
    if t.startswith("Damping"):
        i = b.get("Interpolation", {})
        s = "damp via %s" % short(i.get("InterpolationMethod", "?"))
        for k in ("InterpTimeS", "InterpSpeed", "exp"):
            if k in i:
                s += " %s %s" % (k, g(i[k]))
        return s
    return t


def render_page(a, r, t):
    L = []
    L.append('---\ntitle: "Vehicle control assists"\n'
             'redirect_from: ["/Wardogs_VehicleControlAssists_v1.html", "/Wardogs_VehicleControlAssists_v1"]\n'
             'parent: "Vehicles"\n'
             'description: "Wheeled arcade-assist settings and the helicopter flight-assist objects (pitch, roll, yaw, collective) as stored in the game data"\n---\n')
    L.append("# Wardogs: Vehicle Control Assists\n")
    L.append("*Generated by [`_tools/vehicle_round40_tables.py`](" + REPO + "_tools/vehicle_round40_tables.py) (`--write` refreshes this page and "
             "`assets/data/vehicle-arcade-controls.json` / `vehicle-rotary-assists.json`). Values are shown as stored in the cooked data; `-` means the asset does not "
             "set the field (the native default applies, not read). Evidence: [round 40](" + REPO + "docs/evidence/round40-vehicles-explosives.md).*\n")
    L.append("## 1. Wheeled arcade controls (`DA_ArcadeControls_*`)\n")
    L.append("Each wheeled vehicle names one `MWheeledVehicleArcadeDataAsset`. The names are the engine's own: recover power pushes the car back on line after under- or "
             "oversteer between the minimum and full recover speeds; anti-roll powers resist body roll per axle; drift ratios shape the drift assist; lean and pitch "
             "angles limit body lean; predictive landing and airborne damping act while airborne. How each number maps to the feel of the car is native and not traced.\n")
    cols = [c for c in ARC_COLS if any(c[0] in x["properties"] for x in a)]
    rows = []
    for x in a:
        rows.append(["`%s`" % x["asset"]] + [g(x["properties"][k]) if k in x["properties"] else "-" for k, _ in cols])
    L.append(md_table(["Asset"] + [h for _, h in cols], rows) + "\n")
    L.append("Fields set by no asset appear nowhere in the table. The Kodiak/SUV (`WHL_02`) and Ural (`WHL_07`) set no anti-roll power; the Wolf-110 (`WHL_08`) and Humvee (`WHL_05`) share the same values.\n")
    L.append("## 2. Wheeled tyre models (`MWheeledVehicleTireModelSimpleDataAsset`)\n")
    L.append("Only three wheeled vehicles name a simple tyre model asset: `WHL_01`, `WHL_02` (Kodiak and Pickup) and `WHL_07` (Ural). The eight coefficients are the "
             "engine's own names (`Ln*` longitudinal, `Lt*` lateral; b, c, d, e follow the stiffness, shape, peak and curvature pattern of a Pacejka-style magic formula; "
             "that reading comes from the names, it is not confirmed in code). The asset also stores two editor preview curves (force against slip); the largest magnitude and the slip it occurs at are listed.\n")
    rows = []
    for x in t:
        c = x["coefficients"]
        lo, la = x["longitudinalCurve"], x["lateralCurve"]
        rows.append(["`%s`" % x["asset"]] + [g(c.get(k, "-")) for k in ("Lnb", "Lnc", "Lnd", "Lne", "Ltb", "Ltc", "Ltd", "Lte")]
                    + ["%s at slip %s" % (g(lo["peakValue"]), g(lo["peakAt"])) if lo else "-", "%s at slip %s" % (g(la["peakValue"]), g(la["peakAt"])) if la else "-"])
    L.append(md_table(["Asset", "Lnb", "Lnc", "Lnd", "Lne", "Ltb", "Ltc", "Ltd", "Lte", "Longitudinal preview peak", "Lateral preview peak"], rows) + "\n")
    L.append("The other wheeled vehicles (`WHL_05`, `WHL_06`, `WHL_08`) name no tyre model asset in the exported data.\n")
    L.append("## 3. Helicopter flight assists\n")
    L.append("Each helicopter has one `BHRotaryFlightDataAsset`. The pitch, roll, yaw and collective controls each hold a list of assists. An assist is on or off in the data "
             "(`Enabled`), belongs to a category (`Core`, `Stability`, `AutoHover`, `EnvelopeLimits`, `TurnCoordination`), runs when all its conditions are true, and its body "
             "computes the control value (a PID loop, a damping interpolation, or a fixed value). Speeds are km/h, angular rates deg/s, as the condition names state.\n")
    for e in r:
        L.append("### %s (`%s`)\n" % (e["vehicle"], e["asset"]))
        rs = e["rotorSettings"]
        L.append("Rotor: " + ", ".join("%s %s" % (k, g(v)) for k, v in rs.items() if not k.startswith("_")) + ".  ")
        L.append("Control force: " + "; ".join("%s %s" % (k, ", ".join("%s %s" % (kk, g(vv)) for kk, vv in v.items())) for k, v in e["forces"].items()) + ".\n")
        for cname in CONTROLS:
            c = e["controls"].get(cname)
            if not c:
                continue
            L.append("**%s**\n" % cname.replace("Control", ""))
            rows = []
            for s in c["assists"]:
                rows.append([s["label"] or "-", s["category"], "yes" if s["enabled"] else "no",
                             "; ".join(cond_text(x) for x in s["conditions"]) or "-", body_text(s["body"])])
            L.append(md_table(["Assist", "Category", "Enabled", "Conditions", "Body"], rows) + "\n")
    return "\n".join(L)


def build():
    return {"vehicle-arcade-controls.json": arcade(), "vehicle-rotary-assists.json": rotary(), "vehicle-tire-models.json": tires()}


def dumps(o):
    return json.dumps(o, indent=1, ensure_ascii=False) + "\n"


def main():
    b = build()
    page = render_page(b["vehicle-arcade-controls.json"], b["vehicle-rotary-assists.json"], b["vehicle-tire-models.json"])
    if "--write" in sys.argv:
        for name, obj in b.items():
            with open(os.path.join(OUT, name), "w", encoding="utf8", newline="\n") as fh:
                fh.write(dumps(obj))
        with open(PAGE, "w", encoding="utf8", newline="\n") as fh:
            fh.write(page)
        print("wrote", ", ".join(b), "and", rel(PAGE))
        return 0
    if "--check" in sys.argv:
        bad = [n for n, o in b.items() if not os.path.exists(os.path.join(OUT, n))
               or open(os.path.join(OUT, n), encoding="utf8", newline="").read() != dumps(o)]
        if not os.path.exists(PAGE) or open(PAGE, encoding="utf8", newline="").read() != page:
            bad.append(rel(PAGE))
        print("stale:", bad or "none")
        return 1 if bad else 0
    for n, o in b.items():
        print(n, len(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
