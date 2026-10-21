"""Native class defaults for WDWeaponStatsData, and the doc cells that depend on them.

An exported asset omits every property that equals the class default, so a missing
`RoundsPerMinute` means the constructor value, not "no value". The defaults below were read from the
restored exe constructors (see the **Native** note in game-features/Wardogs_GameFeatures_Weapons_v2.md
section 3):

    UWDWeaponStatsData ctor wrapper   RVA 0x6BBCDF0  (sets vtable 0xB32BAB0, calls the struct ctor at +0x38)
    FWDWeaponStats ctor (0xE48 bytes) RVA 0x699E6C0   (writes every default below, offsets inside the struct)

    python _tools/weapon_stats_defaults.py            # resolved rows for every WDWeaponStatsData asset
    python _tools/weapon_stats_defaults.py --missing  # only the omitted properties
    python _tools/weapon_stats_defaults.py --check    # doc cells that still show a dash for a resolvable value
    python _tools/weapon_stats_defaults.py --write    # fill those cells (class default shown as `600*` or `600 (class default)`)
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
sys.stdout.reconfigure(encoding="utf-8")

# column -> (path inside Properties.WeaponStats, struct offset, native default, ctor evidence)
COLS = {
    "RPM": (["RoundsPerMinute"], 0x138, 600.0, "dword 0x44160000"),
    "Muzzle": (["InitialBulletSpeed"], 0xDA0, 100000.0, "dword 0x47C35000"),
    "EffRange": (["EffectiveRange"], 0xDA4, 100.0, "dword 0x42C80000"),
    "Accuracy": (["WeaponAccuracy", "AccuracyValue"], 0x4, 1.0, "dword 0x3F800000 (AccuracyType byte = 1)"),
    "Deviation": (["RandomDeviationDegree"], 0xCE0, 5.0, "dword 0x40A00000"),
    "PitchMax": (["RecoilPatternPitchMax"], 0xCB8, 1.0, "dword 0x3F800000"),
    "Focus": (["FocusEnergyReductionPerShot"], 0x94, 0.0, "high half of qword at +0x90 = 0"),
    "Relief": (["RecoilReductionWhenFocussing"], 0x9C, 0.0, "high half of qword at +0x98 = 0"),
    "ViewKick": (["ViewKickMagnitudeMultiplier"], 0xB78, 1.0, "dword 0x3F800000"),
    "AdsStab": (["AimSwayData", "AdsStabilizationData", "AdsStabilizeTime"], 0xAC0, 0.5, "dword 0x3F000000"),
    "Suppr": (["SuppressionMultiplier"], 0xDA8, 1.0, "dword 0x3F800000"),
    "Burst": (["RoundsPerBurst"], 0x150, 3, "byte 3"),
    "Melee": (["MeleeDamage"], 0xDAC, 25.0, "dword 0x41C80000"),
    "FireModes": (["SupportedFireModes"], 0x140, "none", "TArray zeroed at +0x140"),
    "MinZero": (["MinZeroingRange"], 0x160, 100, "dword 100"),
    "MaxZero": (["MaxZeroingRange"], 0x164, 100, "dword 100"),
    "ZeroStep": (["ZeroingStep"], 0x168, 100, "dword 100"),
}
MARK = "(class default)"


def fmt(v, comma=False):
    if isinstance(v, list):
        return ", ".join(x.split("::")[-1] for x in v) if v else "none"
    if isinstance(v, float):
        if v == int(v) and abs(v) >= 1:
            v = int(v)
        else:
            s = f"{v:.4g}"
            return s
    if isinstance(v, int) and comma and abs(v) >= 1000:
        return f"{v:,}"
    return str(v)


def load():
    out = {}
    for f in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
        try:
            with open(f, encoding="utf-8") as fh:
                head = fh.read(400)
                if "WDWeaponStatsData" not in head:
                    continue
                fh.seek(0)
                d = json.loads(fh.read().split("\n", 1)[1])
        except Exception:
            continue
        for it in (d if isinstance(d, list) else [d]):
            if it.get("Type") != "WDWeaponStatsData":
                continue
            ws = it.get("Properties", {}).get("WeaponStats", {})
            row = {}
            for col, (path, _o, df, _e) in COLS.items():
                o = ws
                for k in path:
                    o = o.get(k) if isinstance(o, dict) else None
                    if o is None:
                        break
                row[col] = (o, "Data") if o is not None else (df, "Native default")
            tag = it.get("Properties", {}).get("WeaponId", {}).get("TagName", "")
            out[it["Name"]] = {"file": os.path.relpath(f, ROOT).replace("\\", "/"), "tag": tag, "cols": row}
    return out


def resolve_asset(assets, row_text, first_cell):
    m = re.search(r"DA_\w+?_Stats\b", row_text)
    if m and m.group(0) in assets:
        return m.group(0)
    k = "DA_" + first_cell + "_Stats"
    if k in assets:
        return k
    for n, a in assets.items():
        if a["tag"].split(".")[-1] == first_cell:
            return n
    return None


DASH = {"-", "—", "none", "n/a", ""}

# (file, header-prefix, {column header: stats column}, style)
#   style "star": defaults shown as `600*`; "words": `600 (class default)`
TABLES = [
    ("game-features/Wardogs_GameFeatures_Weapons_v2.md", "| ID | RPM |",
     {"RPM": "RPM", "Muzzle spd": "Muzzle", "Eff. range": "EffRange", "Accuracy": "Accuracy", "Deviation (deg)": "Deviation",
      "Pitch recoil max": "PitchMax", "Focus / shot": "Focus", "Recoil relief": "Relief", "View kick x": "ViewKick",
      "ADS stab. (s)": "AdsStab", "Suppression x": "Suppr", "Burst": "Burst", "Melee": "Melee"}, "star"),
    ("content/Wardogs_InfantryWeapons_Stats_v1.md", "| Asset | Package | WeaponId | RPM |",
     {"RPM": "RPM", "Fire modes": "FireModes", "Accuracy": "Accuracy"}, "words"),
    ("content/Wardogs_AllVehicles_Stats_Damage_v1.md", "| Asset | Package | WeaponId | RPM |",
     {"RPM": "RPM", "Fire modes": "FireModes"}, "words"),
    ("game-features/Wardogs_GameFeatures_Vehicles_v2.md", "| Stats asset | Family | RPM |",
     {"RPM": "RPM", "Burst": "Burst", "Fire modes": "FireModes", "Muzzle speed": "Muzzle", "Effective range": "EffRange",
      "Accuracy": "Accuracy"}, "words"),
    ("content/Wardogs_Weapons_v2.md", "| Asset | WeaponId tag | Caliber | RPM |",
     {"RPM": "RPM", "Fire modes": "FireModes", "Init. bullet speed": "Muzzle", "Effective range": "EffRange",
      "Melee dmg": "Melee"}, "words"),
]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def patch(assets, write):
    changes = []
    for rel, head, colmap, style in TABLES:
        path = os.path.join(ROOT, rel)
        lines = open(path, encoding="utf-8").read().split("\n")
        i = next((j for j, l in enumerate(lines) if l.startswith(head)), None)
        if i is None:
            changes.append((rel, "header not found", head))
            continue
        hdr = cells(lines[i])
        idx = {h: hdr.index(h) for h in colmap if h in hdr}
        comma = rel in ("game-features/Wardogs_GameFeatures_Vehicles_v2.md", "content/Wardogs_Weapons_v2.md")
        j = i + 2
        while j < len(lines) and lines[j].startswith("|"):
            cs = cells(lines[j])
            name = resolve_asset(assets, lines[j], cs[0].strip("`[]").split("](")[0])
            if name:
                before = list(cs)
                for h, ix in idx.items():
                    col = colmap[h]
                    cur = cs[ix]
                    if cur.strip("`") not in DASH:
                        continue
                    v, src = assets[name]["cols"][col]
                    if col == "FireModes" and src == "Native default":
                        new = "none " + MARK
                    elif src == "Native default":
                        new = fmt(v, comma=comma) + ("*" if style == "star" else " " + MARK)
                    else:
                        new = fmt(v, comma=comma)
                    if cur != new:
                        cs[ix] = new
                        changes.append((rel, name, f"{h}: {cur!r} -> {new!r}"))
                if write and cs != before:
                    lines[j] = "| " + " | ".join(cs) + " |"
            elif lines[j].split("|")[1].strip():
                pass
            j += 1
        if write:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lines))
    return changes


def main():
    assets = load()
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg in ("--check", "--write"):
        ch = patch(assets, arg == "--write")
        for c in ch:
            print(*c, sep=" | ")
        print(f"{len(ch)} cell(s) {'rewritten' if arg == '--write' else 'still show a dash for a resolvable value'}")
        sys.exit(0 if arg == "--write" or not ch else 1)
    print(f"{len(assets)} WDWeaponStatsData assets")
    tot = 0
    for n, a in sorted(assets.items()):
        miss = {c: v[0] for c, v in a["cols"].items() if v[1] != "Data"}
        tot += len(miss)
        if arg == "--missing" and not miss:
            continue
        print(n.ljust(44), "omitted:", ", ".join(f"{c}={fmt(v)}" for c, v in miss.items()))
    print(f"{tot} omitted properties resolved to native defaults")


if __name__ == "__main__":
    main()
