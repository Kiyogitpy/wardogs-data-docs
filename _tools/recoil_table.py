"""Per-weapon recoil table for content/Wardogs_Weapons_v2.md §5a, rebuilt from data/.

Reads each infantry weapon's WDWeaponStatsData asset. Cooked assets omit fields that
keep the native default, so those come from the FWDWeaponStats constructor
(0x699E6C0) and are marked with a dagger. How the inputs combine into each shot's
view kick is in the doc (§5a).

    python _tools/recoil_table.py          # print the table
    python _tools/recoil_table.py --write  # refresh the marked table in the doc
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = "content/Wardogs_Weapons_v2.md"
BLOCK = re.compile(r"<!-- recoil_table -->.*?<!-- /recoil_table -->", re.S)
# Vehicle, stationary and test weapons are left out. Vehicle-extension and mounted weapons use the
# IWDWeaponOwner default (x1, 0x19A4A50); fists have no ranged-weapon extension (Weapons §5b).
SKIP = re.compile(r"Vehicles|VehicleWeaponry|Stationary|Gunsmith|BarrelTest|BuildTool|Fists")
FOCUS_WINDOW = "_aaabimbpohdlmnphjbidm"  # stats +0x98 (hashed in this build; v2 usmap token)
DEFAULTS = {  # FWDWeaponStats constructor 0x699E6C0
    "RandomDeviationDegree": 5.0,
    "RecoilPatternResetTime": 0.5,
    "ViewKickMagnitudeMultiplier": 1.0,
    "PostPatternRandomYawRecoil": {"X": -1.0, "Y": 1.0},
    "PostPatternRandomPitchRecoil": {"X": 1.0, "Y": 2.0},
    "RecoilReductionWhenFocussing": 0.0,
    "FocusEnergyReductionPerShot": 0.0,
    # +0x98, unnamed: the focus-drain window after focus ends (s)
    FOCUS_WINDOW: 0.5,
}


def stats_assets():
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "**", "DA_*_Stats.json"), recursive=True)):
        if SKIP.search(path.replace("\\", "/")):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for part in re.split(r"^--- export:.*---\s*$", text, flags=re.M):
            if part.strip():
                obj = json.loads(part)
                if obj.get("Type") == "WDWeaponStatsData":
                    yield path, obj
                break


def num(x):
    return f"{x:g}"


def value(ws, key):
    """The field's value and whether it is the native default."""
    return (ws[key], False) if key in ws else (DEFAULTS[key], True)


def keys(curve):
    return [(k["Time"], k["Value"]) for k in (curve or {}).get("EditorCurveData", {}).get("Keys", [])]


def kick_curve(ws):
    k = keys(ws.get("ViewKickCurve"))
    if not k:
        return "none (no curve)"
    return ", ".join(f"{num(v)} at {num(t)} s" for t, v in k if t > 0) or "none"


def recovery(ws):
    k = keys(ws.get("RecoveryKickCurve"))
    if not k or all(v == 0 for _, v in k):
        return "none"
    t, v = k[-1]
    return f"{num(round(v * 100, 1))}% over {num(t)} s"


def rows():
    out = []
    for path, obj in stats_assets():
        name = os.path.basename(path)[3:-len("_Stats.json")]
        tag = ((obj["Properties"].get("WeaponId") or {}).get("TagName") or "").rsplit(".", 1)[-1]
        if tag and tag != name:
            name += f" ({tag})"
        ws = obj["Properties"].get("WeaponStats", {})
        pattern = ws.get("RecoilPattern") or []
        dev, dev_d = value(ws, "RandomDeviationDegree")
        reset, reset_d = value(ws, "RecoilPatternResetTime")
        mult, mult_d = value(ws, "ViewKickMagnitudeMultiplier")
        yaw, yaw_d = value(ws, "PostPatternRandomYawRecoil")
        pitch, pitch_d = value(ws, "PostPatternRandomPitchRecoil")
        cut, cut_d = value(ws, "RecoilReductionWhenFocussing")
        drain, drain_d = value(ws, "FocusEnergyReductionPerShot")
        window, window_d = value(ws, FOCUS_WINDOW)
        d = lambda flag: "†" if flag else ""
        first = f"{num(pattern[0]['X'])}, {num(pattern[0]['Y'])}" if pattern else "—"
        out.append(
            f"| `{name}` | {len(pattern)} | {first} | ±{num(dev)}{d(dev_d)} "
            f"| {num(yaw['X'])} … {num(yaw['Y'])}{d(yaw_d)} | {num(pitch['X'])} … {num(pitch['Y'])}{d(pitch_d)} "
            f"| {num(reset)}{d(reset_d)} | ×{num(mult)}{d(mult_d)} | {kick_curve(ws)} | {recovery(ws)} "
            f"| {num(cut)}{d(cut_d)} / {num(drain)}{d(drain_d)} / {num(window)}{d(window_d)} |")
    return out


def table():
    head = ["| Weapon | Pattern shots | Shot 1 (yaw, pitch) | Deviation (°) | After pattern: yaw | After pattern: pitch "
            "| Reset (s) | Kick × | Kick curve | Recovery | Focus: recoil cut % / energy % per shot / drain window (s) |",
            "|---|---:|---|---:|---|---|---:|---:|---|---|---|"]
    return "\n".join(head + rows())


def write_doc():
    path = os.path.join(ROOT, DOC)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    block = nl.join(["<!-- recoil_table -->"] + table().split("\n") + ["<!-- /recoil_table -->"])
    new, n = BLOCK.subn(lambda m: block, text)
    if not n:
        sys.exit(f"no <!-- recoil_table --> block in {DOC}")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print(f"{DOC}: table {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv:
        write_doc()
    else:
        print(table())


if __name__ == "__main__":
    main()
