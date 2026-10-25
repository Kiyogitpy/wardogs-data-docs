"""assets/data/vehicle-native-defaults.json: native constructor defaults of the vehicle data assets and the
cooked values with those defaults filled in (round 45).

A cooked data asset stores only the properties that differ from the class default, so a field the handling page
shows as an em dash (not set) takes the value the native constructor writes. Those constructors were read
statically with `_tools/ctor_defaults.py` and are kept here as a snapshot (ctor RVA, class, values); this tool
only needs `data/`:

    python -I _tools/r45_vehicle_defaults.py            # rewrite assets/data/vehicle-native-defaults.json
    python -I _tools/r45_vehicle_defaults.py --check    # exit 1 when the file is stale

Wheel assets store three values per field (`Values`, `Values[1]`, `Values[2]`): intact tyre, damaged (health at
or below the trigger), destroyed (health 0). A missing key is the default value, not zero.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "vehicle-native-defaults.json")
VEH = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Vehicles")

# Constructor snapshot: read with _tools/ctor_defaults.py (RVAs of WardogsClient-Win64-Shipping.restored.exe,
# SHA-256 a5c3db10...0cc37). Values are what the constructor stores; fields it does not store are zero.
CTORS = {
    "MWheeledVehicleWheelDataAsset": {
        "ctor": "0x5311EB0",
        "perState": {  # three floats each: [intact, damaged, destroyed]
            "LateralFriction": 1.0, "LongitudinalFriction": 1.0, "LateralScale": 1.0, "LongitudinalScale": 1.0,
            "OverturnScale": 0.0, "RollMomentScale": 0.0, "SelfAlignScale": 0.0, "TirePressure": 2.0,
            "Radius": 0.25, "Width": 0.2, "RimOffset": 0.0, "ForwardOffset": 0.0, "VerticalOffset": 0.0,
            "CastOffset": 0.0, "Mass": 10.0, "BrakeTorque": 1000.0, "SuspensionUpTravel": 0.1,
            "SuspensionDownTravel": 0.1, "SuspensionSpring": 5000.0, "CompressionDamper": 1000.0,
            "RelaxationDamper": 1000.0, "SuspensionPreload": 0.0, "PhysMatLerpValue": 1.0},
        "scalar": {"bPhysicsSurfaceUpdate": False},
    },
    "MWheeledVehicleEngineTransmissionDataAsset": {
        "ctor": "0x530F660",
        "EngineData": {"TorqueScale": 1.0, "FrictionTorque": 50.0, "IdleRPM": 1000.0, "LimitRpm": 6500.0,
                       "LimiterTime": 100.0, "EngineInertia": 0.25, "bEnableBoost": False, "BoostScale": 1.0},
        "TransmissionData": {"bUseAutoChange": True, "bUseAutoReverse": True, "bUseAutoClutch": True,
                             "bUseRevMatching": True, "bEnableCrawling": False, "CrawlingGear": 1,
                             "ChangeTime": 100.0, "GearUpRatio": 90.0, "GearDownRatio": 80.0,
                             "GearUpVelocityBias": 1.0, "GearDownVelocityBias": 1.0, "ClutchTime": 100.0,
                             "ClutchScale": 100.0, "GearRatios": [3.0, 5.0], "FinalGearRatio": 3.0,
                             "bUseClutchAssist": False, "ClutchScaleMin": 0.0, "ClutchScaleMax": 0.0},
    },
    "MWheeledVehicleInputDataAsset": {
        "ctor": "0x530F7A0",
        "values": {"SteerSensivity": 5.0, "SteerInputGravity": 1.5, "SteerRange": 100.0, "SteerDeadzone": 0.01,
                   "SteeringAssist": 0.0, "SteeringAssistThresholdAngle": 1.0, "ThrottleSensivity": 3.0,
                   "ThrottleRange": 100.0, "ThrottleDeadzone": 0.01, "BrakingSensivity": 3.0,
                   "BrakingRange": 100.0, "BrakingDeadzone": 0.01, "ClutchSensivity": 3.0, "ClutchRange": 100.0,
                   "ClutchDeadzone": 0.01},
    },
    "MWheeledVehicleAxlesDataAsset": {
        "ctor": "0x530F5A0",
        "values": {"DiffStrength": 0.25, "TorqueShare": 0.5, "MaxSteerAngle": 0.0, "AckermanCoefficient": 1.0,
                   "AckermanReferenceIndex": 1, "bHasHandbrake": False, "CamberAngle": 0.0, "ToeAngle": 0.0},
        "note": "DifferentialType byte at +0x50 is set to 1 by the constructor (enum EMDifferential, member names not mapped).",
    },
    "MWheeledVehicleCharacteristicsDataAsset": {
        "ctor": "0x5384E80",
        "values": {"UpdateRate": 250, "Mass": 1000.0, "ReverseBrakeSpeed": 1.0, "DrivetrainInertia": 1.0,
                   "DrivetrainFriction": 50.0, "RollingResistanceCoefficient": 0.0, "HandBrakePower": 0.0,
                   "DragCoefficient": 0.8, "DownForceCoefficient": 0.2, "MinAbsSpeed": 10.0, "Abs": 0.0,
                   "Asr": 0.0, "Rays": 1, "LateralRays": 1, "SleepWaitingTime": 1.0},
    },
    "MTrackedVehicleEngineData": {
        "ctor": "0x5304980",
        "values": {"UpdateRate": 250, "Mass": 20000.0, "TrackMass": 600.0, "SprocketMass": 64.0,
                   "SprocketRadius": 32.5, "HullForce": 200.0, "GravityOnSlope": 0.25, "BrakeForce": 20.0,
                   "DifferentialRatio": 10.0, "TransmissionEfficiency": 1.0, "ChangeTime": 10000.0,
                   "RetarderUpRatio": 0.85, "RetarderDownRatio": 0.5, "ThrottleIncrement": 1.0,
                   "ThrottleDecrement": -0.5, "EngineExtraPowerRatio": 5.0, "BoostScale": 1.0, "CrawlGear": 1,
                   "RollingFrictionCoefficient": 0.8, "MuXStatic": 0.75, "MuYStatic": 0.75, "MuXKinetic": 1.5,
                   "MuYKinetic": 1.5},
    },
    "BHHelicopterEngineDataAsset": {
        "ctor": "0x53846F0",
        "note": "Chosen among three functions that store the same vtable by value coherence (rotor RPMs near the "
                "cooked 270 and 850 values); the other two (0x5270180, 0x52705F0) store 200 / 100 / 2 / 45 and "
                "may belong to another class.",
        "values": {"EngineOperatingRPM": 15000.0, "EngineRPMIncreaseRatePerSecond": 1000.0,
                   "EngineRPMDecreaseRatePerSecond": 1000.0, "MainRotorCriticalLowRPM": 400.0,
                   "MainRotorOperatingRPM": 500.0, "TailRotorOperatingRPM": 1500.0},
    },
}


def load(path):
    t = open(path, encoding="utf8").read()
    t = t[t.index("{"):]
    return json.JSONDecoder().raw_decode(t)[0]


def assets(kind):
    for f in sorted(glob.glob(os.path.join(VEH, "**", "*.json"), recursive=True)):
        with open(f, encoding="utf8") as fh:
            head = fh.read(400)
        if '"Type": "%s"' % kind not in head:
            continue
        d = load(f)
        yield os.path.basename(f)[:-5], d.get("Properties", {})


def tri(p, key, default):
    v = p.get(key, {})
    return [v.get("Values", default), v.get("Values[1]", default), v.get("Values[2]", default)]


def merged(kind, p):
    base = dict(CTORS[kind]["values"])
    filled = sorted(k for k in base if k not in p)
    base.update({k: v for k, v in p.items() if k in base})
    return {"values": base, "defaultFilled": filled}


def build():
    out = {"source": "ctor snapshot read with _tools/ctor_defaults.py; cooked values from "
                     "data/Wardogs/Plugins/GameFeatures/Vehicles",
           "ctors": CTORS, "wheelAssets": {}, "engineTransmission": {}, "input": {}, "axles": {},
           "characteristics": {}}
    w = CTORS["MWheeledVehicleWheelDataAsset"]
    for name, p in assets("MWheeledVehicleWheelDataAsset"):
        row = {"bPhysicsSurfaceUpdate": p.get("bPhysicsSurfaceUpdate", False)}
        notset = []
        for k, dv in w["perState"].items():
            row[k] = tri(p, k, dv)
            for i, key in enumerate(("Values", "Values[1]", "Values[2]")):
                if key not in p.get(k, {}):
                    notset.append("%s[%d]" % (k, i))
        row["defaultFilled"] = notset
        out["wheelAssets"][name] = row
    et = CTORS["MWheeledVehicleEngineTransmissionDataAsset"]
    for name, p in assets("MWheeledVehicleEngineTransmissionDataAsset"):
        eng = dict(et["EngineData"])
        eng.update({k: v for k, v in p.get("EngineData", {}).items() if k != "TorqueCurve"})
        tr = dict(et["TransmissionData"])
        tr.update(p.get("TransmissionData", {}))
        out["engineTransmission"][name] = {
            "EngineData": eng, "TransmissionData": tr,
            "defaultFilled": sorted(k for k in et["EngineData"] if k not in p.get("EngineData", {}))}
    for name, p in assets("MWheeledVehicleInputDataAsset"):
        out["input"][name] = merged("MWheeledVehicleInputDataAsset", p)
    for name, p in assets("MWheeledVehicleAxlesDataAsset"):
        out["axles"][name] = merged("MWheeledVehicleAxlesDataAsset", p)
    for name, p in assets("MWheeledVehicleCharacteristicsDataAsset"):
        out["characteristics"][name] = merged("MWheeledVehicleCharacteristicsDataAsset", p)
    return out


def main():
    text = json.dumps(build(), indent=1, sort_keys=True) + "\n"
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else ""
        sys.exit(0 if cur == text else 1)
    with open(OUT, "w", encoding="utf8", newline="\n") as fh:
        fh.write(text)
    d = json.loads(text)
    print("wrote %s: %d wheel assets, %d engine/transmission, %d input, %d axle, %d characteristics" % (
        os.path.relpath(OUT, ROOT), len(d["wheelAssets"]), len(d["engineTransmission"]), len(d["input"]),
        len(d["axles"]), len(d["characteristics"])))


if __name__ == "__main__":
    main()
