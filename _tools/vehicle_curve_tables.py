"""Tables for game-features/Wardogs_VehicleCurves_v1.md: every vehicle CurveFloat (CRV_*), rebuilt from data/.

Scope: every CRV_* export whose path contains "Vehicles" (the per-vehicle plugin folders under
Plugins/GameFeatures/Vehicles and Content/Vehicles). Each row lists the curve's keys as time -> value, its
interpolation, and the assets that reference it (the referencing property name is the one stored in the
export; "ExternalCurve" is a generic slot name, so the referencing asset is the better hint).
Blocks sit between

    <!-- vehicle_curve_tables MODE -->  ...  <!-- /vehicle_curve_tables -->

    python _tools/vehicle_curve_tables.py --write      # refresh every block in place
    python _tools/vehicle_curve_tables.py --check      # exit 1 when a block is stale
    python _tools/vehicle_curve_tables.py MODE         # print one block (counts, collision, drive, steer, brake,
                                                       #   camera, other)
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = "game-features/Wardogs_VehicleCurves_v1.md"
BLOCK = re.compile(r"<!-- vehicle_curve_tables (\w+) -->\r?\n.*?<!-- /vehicle_curve_tables -->", re.S)

FAMILIES = [  # (mode, title, name regex)
    ("collision", "Collision damage and player collision", r"Collision"),
    ("drive", "Drivetrain: torque and pedal engagement", r"Torque|Engagement"),
    ("steer", "Steering limits and speed", r"Steer"),
    ("brake", "Brake ratio", r"BrakeRatio"),
    ("camera", "Camera: free-look range and field of view", r"FreeLook|FOV"),
]


def family(name):
    for mode, _, rx in FAMILIES:
        if re.search(rx, name):
            return mode
    return "other"


def load():
    curves = {}
    for f in sorted(glob.glob(os.path.join(DATA, "**", "CRV_*.json"), recursive=True)):
        rel = ct.rel_of(f)
        if "Vehicles" not in rel:
            continue
        for e in ct.exports(f):
            if e.get("Type") == "CurveFloat":
                curves[e["Package"]] = {"name": e["Name"], "rel": rel, "keys": e["Properties"]["FloatCurve"].get("Keys", []), "refs": set()}
    names = set(curves)

    def walk(o, key, src):
        if isinstance(o, dict):
            pkg = str(o.get("ObjectPath", "")).rsplit(".", 1)[0]
            if pkg in names:
                curves[pkg]["refs"].add((key, src))
            for k, v in o.items():
                walk(v, k, src)
        elif isinstance(o, list):
            for v in o:
                walk(v, key, src)
    for f in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
        if os.path.basename(f).startswith("CRV_"):
            continue
        try:
            for e in ct.exports(f):
                walk(e, None, os.path.basename(f)[:-5])
        except ValueError:
            pass
    return curves


def folder(rel):
    parts = rel.split("/")
    return parts[parts.index("Vehicles") + 1] if "Plugins" in parts else "/".join(parts[parts.index("Vehicles") + 1:-1])


def points(keys):
    return ", ".join(f"{ct.n(k['Time'])} -> {ct.n(k['Value'])}" for k in keys)


def table(d, mode):
    out = ["| Curve | Folder | Keys (time -> value) | Interp | Referenced by |", "|---|---|---|---|---|"]
    for pkg in sorted(d, key=lambda p: (d[p]["name"], p)):
        c = d[pkg]
        if family(c["name"]) != mode:
            continue
        interp = ", ".join(sorted({k["InterpMode"].replace("RCIM_", "") for k in c["keys"]})) or "-"
        refs = sorted(c["refs"], key=lambda r: (str(r[0]), r[1]))
        slots = sorted({r[0] for r in refs if r[0]})
        who = ", ".join(f"`{s}`" for s in sorted({r[1] for r in refs}))
        if slots and slots != ["ExternalCurve"]:
            who += " (slot " + ", ".join(f"`{s}`" for s in slots) + ")"
        out.append(f"| {ct.link(c['rel'])} | `{folder(c['rel'])}` | {points(c['keys']) or '-'} | {interp} | {who or 'no asset in data/'} |")
    return "\n".join(out)


def counts(d):
    cnt = collections.Counter(family(c["name"]) for c in d.values())
    titles = {m: t for m, t, _ in FAMILIES}
    titles["other"] = "Other"
    out = ["| Family | Curves |", "|---|---|"]
    for m in [m for m, _, _ in FAMILIES] + ["other"]:
        out.append(f"| {titles[m]} | {cnt[m]} |")
    out.append(f"| **Total** | **{len(d)}** |")
    return "\n".join(out)


MODES = {"counts": counts}
for _m, _t, _r in FAMILIES + [("other", "Other", "")]:
    MODES[_m] = (lambda m: lambda d: table(d, m))(_m)


def regenerate(d, text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = MODES[m.group(1)](d).split("\n")
        return nl.join([f"<!-- vehicle_curve_tables {m.group(1)} -->"] + body + ["<!-- /vehicle_curve_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    d = load()
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(d, text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(MODES[next((a for a in args if a in MODES), "counts")](d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
