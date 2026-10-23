"""Per-weapon spread inputs for pipelines/Wardogs_WeaponSpread_v1.md (section 8), rebuilt from data/.

Reads each infantry weapon's item extension (SpreadValues rows, InAirHipFireSpread), its WDWeaponStatsData
asset (WeaponAccuracy, ShotgunData) and CT_Weapon_Spread. Cooked assets omit fields that equal the native
default, so those come from the constructors read in the executable: FWDWeaponStats 0x699E6C0
(WeaponAccuracy.AccuracyType = Milliradians, AccuracyValue = 1.0; ShotgunData ChokeFactor 0.8, outer cone 10,
InnerConeHalfAngleMultiplier 0.5, random ranges 0) and the ranged-weapon data constructor (InAirHipFireSpread
10.0, immediate at 0x6C9102D). Defaults are marked with a dagger.

    python _tools/spread_table.py          # print the table
    python _tools/spread_table.py --write  # refresh the marked block in the page
"""
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = "pipelines/Wardogs_WeaponSpread_v1.md"
BLOCK = re.compile(r"<!-- spread_table -->.*?<!-- /spread_table -->", re.S)
SKIP = re.compile(r"Vehicles|VehicleWeaponry|Stationary|Gunsmith|BarrelTest|BuildTool|Fists")
UNIT = {"MinutesOfAngle": math.pi / 10800.0, "Milliradians": 0.001}  # rad per unit, 0x6BBD3D0
SHOTGUN_DEFAULTS = {"ChokeFactor": 0.8, "OuterConeHalfAngle": 10.0, "InnerConeHalfAngleMultiplier": 0.5}


def parts(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for part in re.split(r"^--- export:.*---\s*$", text, flags=re.M):
        if part.strip():
            try:
                yield json.loads(part)
            except ValueError:
                pass


def walk(x):
    if isinstance(x, dict):
        if "SpreadValues" in x and "WeaponStats" in x:
            yield x
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)


def curve_rows():
    path = os.path.join(ROOT, "data", "Wardogs", "Content", "Items", "Weapons", "Curves", "CT_Weapon_Spread.json")
    obj = next(parts(path))
    return {n: [(k["Time"], k["Value"]) for k in r["Keys"]] for n, r in obj["Rows"].items()}


def stats_assets():
    out = {}
    for path in glob.glob(os.path.join(ROOT, "data", "**", "DA_*_Stats.json"), recursive=True):
        for obj in parts(path):
            if obj.get("Type") == "WDWeaponStatsData":
                out[obj["Name"]] = obj["Properties"].get("WeaponStats", {})
            break
    return out


def items():
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "**", "*.json"), recursive=True)):
        p = path.replace("\\", "/")
        base = os.path.basename(p)
        if base.startswith("DA_") or SKIP.search(p) or "Attachments" in p:
            continue
        with open(path, encoding="utf-8") as f:
            if "SpreadValues" not in (head := f.read()) or "WeaponStats" not in head:
                continue
        for obj in parts(path):
            for x in walk(obj):
                yield base[:-5], x


def num(v):
    return f"{v:g}"


def rows():
    ct = curve_rows()
    stats = stats_assets()
    out = []
    for name, x in items():
        ref = x["WeaponStats"]
        asset = ref.get("ObjectPath", "").rsplit("/", 1)[-1].split(".")[0] if isinstance(ref, dict) else ""
        ws = stats.get(asset)
        if ws is None:
            continue
        acc = ws.get("WeaponAccuracy", {})
        a_type = acc.get("AccuracyType", "EWDWeaponAccuracyType::Milliradians").split("::")[-1]
        a_val = acc.get("AccuracyValue", 1.0)
        a_dag = "†" if "AccuracyType" not in acc else ""
        half = math.degrees(0.5 * a_val * UNIT[a_type])
        by = {e["Key"].split("::")[-1]: e["Value"] for e in x["SpreadValues"]}
        cells = []
        for st in ("Stand", "Crouch", "Prone"):
            v = by[st]
            keys = ct[v["Curve"]["RowName"]]
            m = v.get("Value", 1.0)
            cells.append(f"{num(m * keys[0][1])} → {num(m * keys[-1][1])}")
        row = by["Stand"]["Curve"]["RowName"].split(".")[0]
        sg = ws.get("ShotgunData")
        shot = "—"
        if sg is not None:
            ch = sg.get("ChokeFactor", SHOTGUN_DEFAULTS["ChokeFactor"])
            oc = sg.get("OuterConeHalfAngle", SHOTGUN_DEFAULTS["OuterConeHalfAngle"])
            inn = sg.get("InnerConeHalfAngleMultiplier", SHOTGUN_DEFAULTS["InnerConeHalfAngleMultiplier"])
            rr = sg.get("RandomConeHalfAngleRange", {"X": 0.0, "Y": 0.0})
            shot = "zeroed (choke 0, outer 0)" if ch == 0 and oc == 0 else f"choke {num(ch)}, outer {num(oc)}°, inner ×{num(inn)}, centre jitter {num(rr['X'])}…{num(rr['Y'])}°"
        out.append((name[3:] if name.startswith("ID_") else name, a_type, a_val, a_dag, half, row, cells, shot))
    return sorted(out, key=lambda r: r[0].lower())


def table():
    head = ["| Weapon | Accuracy | Accuracy half-angle (°) | Curve class | Hip half-angle, Stand: still → full speed (°) "
            "| Crouch | Prone | Shotgun data |",
            "|---|---|---:|---|---|---|---|---|"]
    body = []
    for name, a_type, a_val, a_dag, half, row, cells, shot in rows():
        body.append(f"| `{name}` | {num(a_val)} {'mrad' if a_type == 'Milliradians' else 'MOA'}{a_dag} | {half:.4f} | {row} "
                    f"| {cells[0]} | {cells[1]} | {cells[2]} | {shot} |")
    return "\n".join(head + body)


def write_doc():
    path = os.path.join(ROOT, DOC)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    block = nl.join(["<!-- spread_table -->"] + table().split("\n") + ["<!-- /spread_table -->"])
    new, n = BLOCK.subn(lambda m: block, text)
    if not n:
        sys.exit("markers not found in " + DOC)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    print("refreshed", DOC)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv:
        write_doc()
    else:
        print(table())
