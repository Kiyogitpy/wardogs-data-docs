"""Build assets/data/ai-detection.json: how AI soldiers turn sight, hearing and damage into a detection level.

    python -I _tools/ai_detection.py [--check] [<round36_ai dir>]

Inputs (cooked data, read from <dir>/dump): BP_CoreAIController (perception multipliers, sense radii),
BP_PlayerCharacterDetectabilityComponent (stance, hearing, firing), WDAIThreatDetectionMonitor values,
AlertStateThreashold_DataConfig. The formulas themselves come from static reading of the native code
(round 41, CL516586; RVAs in docs/evidence/round41-modes-ai-other.md) and are written here as constants.
Native defaults for values the Blueprints leave unset: MovementSpeedMultiplier 1.0, WeaponFiringMultiplier 1.0,
VisionAngleMultiplier 1.0, VisionPlayerConcealmentMultiplier 1.0, MaxDetectionLevel 1.0.

Output: parameters, formulas as text, and sample tables (per-second detection gain by distance for a standing,
crouching or running target seen head-on and unconcealed; per-second gain from gunfire, a vehicle occupant and
running footsteps). Idempotent. --check exits 1 if the committed file differs. Exits 0 if the input is absent.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "ai-detection.json")
DIST_M = [10, 25, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000]


def load(base, name):
    with open(os.path.join(base, "dump", name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def cdo(doc, typ):
    for o in doc:
        if o.get("Type") == typ and "Properties" in o:
            return o["Properties"]
    return {}


def main():
    check = "--check" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = args[0] if args else r"E:/Reverse_Engineer/wardogs_analysis/round36_ai"
    if not os.path.isdir(os.path.join(base, "dump")):
        print(f"input not found ({base}); skipping")
        return 0
    ctl = load(base, "BP_CoreAIController")
    perc = cdo(ctl, "WDAIPerceptionComponent")
    sight = cdo(ctl, "AISenseConfig_Sight")
    hear = cdo(ctl, "AISenseConfig_Hearing")
    dmg = cdo(ctl, "AISenseConfig_Damage")
    mon = cdo(ctl, "WDAIThreatDetectionMonitorComponent")
    det = {}
    for o in load(base, "BP_PlayerCharacterDetectabilityComponent"):
        if o["Name"].startswith("Default__"):
            det = o["Properties"]
    stance = {k["Key"].split("::")[1]: k["Value"] for k in det["StanceDetectability"]}
    stance_mult = det.get("StanceDetectabilityMultiplier", 1.0)
    hear_move = det.get("HearingMovementSpeedMultiplier", 1.0)
    firing = det.get("WeaponFiring", 1.0)
    firing_mult = det.get("WeaponFiringMultiplier", 1.0)
    move_mult = det.get("MovementSpeedMultiplier", 1.0)
    vrm = perc["VisionRangeMultiplier"]
    hrm = perc["HearingRangeMultiplier"]
    angm = perc.get("VisionAngleMultiplier", 1.0)
    sight_r = sight["SightRadius"]
    hear_r = hear["HearingRange"]
    max_level = mon.get("MaxDetectionLevel", 1.0)
    decay = mon["DetectionDecayRate"]
    wait = mon["TimeBeforeStartDecay"]

    def sight_gain(d_m, det_s):
        x = min(max(d_m * 100.0 / sight_r, 0.0), 1.0)
        if x <= 0:
            return None
        return (x ** (-2.0 * vrm) - 1.0) * det_s  # angle factor 1, concealment factor 1

    def hear_gain(d_m, det_h):
        x = min(max(d_m * 100.0 / hear_r, 0.0), 1.0)
        if x <= 0:
            return None
        return (1.0 / (x * x) - 1.0) * hrm * det_h

    def r(v):
        return None if v is None else float(f"{v:.4g}")

    rows = []
    for d in DIST_M:
        row = {"distanceMeters": d}
        for name in ("Stand", "Crouch", "Prone"):
            s = stance[name] * stance_mult
            row[f"sight{name}Still"] = r(sight_gain(d, s))
        row["sightStandRunning"] = r(sight_gain(d, stance["Stand"] * stance_mult + move_mult))
        row["hearFiring"] = r(hear_gain(d, firing * firing_mult))
        row["hearVehicleOccupant"] = r(hear_gain(d, 1.0))
        row["hearRunning"] = r(hear_gain(d, hear_move))
        rows.append(row)
    out = {
        "source": "round 41: cooked Blueprint values (round36_ai dump) + static native formulas (CL516586)",
        "parameters": {
            "SightRadius": sight_r, "LoseSightRadius": sight["LoseSightRadius"], "HearingRange": hear_r,
            "VisionRangeMultiplier": vrm, "HearingRangeMultiplier": hrm, "VisionAngleMultiplier": angm,
            "VisionPlayerConcealmentMultiplier": perc.get("VisionPlayerConcealmentMultiplier", 1.0),
            "StanceDetectability": stance, "StanceDetectabilityMultiplier": stance_mult,
            "MovementSpeedMultiplier": move_mult, "HearingMovementSpeedMultiplier": hear_move,
            "WeaponFiring": firing, "WeaponFiringMultiplier": firing_mult,
            "MaxDetectionLevel": max_level, "DetectionDecayRate": decay, "TimeBeforeStartDecay": wait,
            "DamageSenseMaxAge": dmg["MaxAge"],
        },
        "formulas": {
            "sightStrength": "angle * (x^(-2*VisionRangeMultiplier) - 1) * concealment * detectabilitySight; x = clamp(distance / SightRadius, 0, 1); angle = dot(facing, direction to target)^VisionAngleMultiplier (0 if dot <= 0); concealment = (visible points / total points)^VisionPlayerConcealmentMultiplier",
            "detectabilitySight": "StanceDetectability[stance] * StanceDetectabilityMultiplier + clamp(speed / maxSpeed, 0, 1) * MovementSpeedMultiplier",
            "hearingStrength": "detectabilityHearing * (1 / x^2 - 1) * HearingRangeMultiplier; x = clamp(distance / HearingRange, 0, 1); zero at or beyond HearingRange",
            "detectabilityHearing": "1.0 if the character operates a vehicle; else max(WeaponFiring * WeaponFiringMultiplier if firing, clamp(speed / maxSpeed, 0, 1)^2 * HearingMovementSpeedMultiplier)",
            "damageSense": "a damage stimulus adds a fixed strength of 1.0",
            "detectionLevel": "each tick, per tracked target: level = clamp(level + deltaTime * sum of the sense strengths, 0, MaxDetectionLevel); decays by deltaTime * DetectionDecayRate once TimeBeforeStartDecay has passed without an update; the entry is removed at level <= 0",
        },
        "sampleTables": {
            "unit": "detection level gained per second (1.0 = a full level), target facing the AI head-on, unconcealed",
            "rows": rows,
        },
    }
    text = json.dumps(out, indent=1) + "\n"
    if check:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("ok" if cur == text else "DIFFERS")
        return 0 if cur == text else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
