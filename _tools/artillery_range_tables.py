#!/usr/bin/env python3
"""Read the game's ArtilleryRangeData tables and compare them with other sources.

The game ships a table of (Milliradians, ImpactDistance m, TravelTime s) in three
weapon extension data assets:

  SPH-2       Vehicles/TNK_01/.../WeaponExtensions/Artillery/WE_TNK_01_Artillery.json
  L81 Mortar  Vehicles/STN_03/.../WeaponExtensions/WE_STN_03_Heavy_MainBarrel.json
  Stingray    Vehicles/STN_05/.../WeaponExtensions/WE_STN_05_Heavy_MainBarrel.json

Without arguments the script prints the three tables.  Nothing is fitted.

  python -I _tools/artillery_range_tables.py
  python -I _tools/artillery_range_tables.py --calc path/to/weapons.json

With --calc (the community wardogs-calculator weapons.json, read only;
weapons[id].ballistics are [range_m, dial_mil] pairs; "spg" has low and high
arcs, "mortar" has "single") the script also reports, row by row, the game
table's mrad minus the calculator's dial mil at the same range (calculator
interpolated linearly between its rows; rows outside the calculator's range are
skipped).  For the SPH-2 it also flies the Expensive shell in shell_sim.py at the
game row's own elevation (mrad / 1000 rad, a true milliradian) and compares the
simulated flight time and range with the game row's TravelTime and
ImpactDistance.  The mortar and Stingray are not simulated: their shells are not
described by the 155 mm flight data.
"""
import argparse
import json
import math
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VEH = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Vehicles")
SOURCES = {
    "spg": ("SPH-2", "TNK_01", "Content", "Weapons", "WeaponExtensions", "Artillery", "WE_TNK_01_Artillery.json"),
    "mortar": ("L81 Mortar", "STN_03", "Content", "Weapons", "WeaponExtensions", "WE_STN_03_Heavy_MainBarrel.json"),
    "stingray": ("Stingray", "STN_05", "Content", "Weapons", "WeaponExtensions", "WE_STN_05_Heavy_MainBarrel.json"),
}


def find_table(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "ArtilleryRangeData":
                return v
            r = find_table(v)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_table(v)
            if r:
                return r
    return None


def load_game(key):
    parts = SOURCES[key]
    path = os.path.join(VEH, *parts[1:])
    t = open(path, encoding="utf8").read()
    j = json.loads(t[t.index("\n") + 1:] if t.startswith("---") else t)
    rows = [(r["Milliradians"], r["ImpactDistance"], r["TravelTime"]) for r in find_table(j)]
    return rows


def split_arcs(rows):
    """SPH-2 table: the low arc runs up to the row with the longest impact."""
    peak = max(range(len(rows)), key=lambda i: rows[i][1])
    return rows[:peak + 1], rows[peak + 1:]


def interp(pairs, x):
    """pairs: (x, y) sorted by x; None outside the covered x range."""
    pairs = sorted(pairs)
    if x < pairs[0][0] or x > pairs[-1][0]:
        return None
    for (x0, y0), (x1, y1) in zip(pairs, pairs[1:]):
        if x0 <= x <= x1:
            return y0 if x1 == x0 else y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None


def spread(v):
    return "n=%d min %.1f median %.1f max %.1f" % (len(v), min(v), st.median(v), max(v)) if v else "n=0"


def print_tables():
    for key in SOURCES:
        rows = load_game(key)
        print("\n== %s: %d rows, %g to %g mrad, %g to %g m, %g to %g s" % (
            SOURCES[key][0], len(rows), min(r[0] for r in rows), max(r[0] for r in rows),
            min(r[1] for r in rows), max(r[1] for r in rows),
            min(r[2] for r in rows), max(r[2] for r in rows)))
        print("   mrad   impact_m  travel_s")
        for m, d, t in rows:
            print("%7.0f  %8.0f  %8.2f" % (m, d, t))


def compare_calc(path):
    calc = {w["id"]: w for w in json.load(open(path, encoding="utf8"))["weapons"]}
    print("\n== game mrad minus calculator dial mil, same range (calculator interpolated)")
    # SPH-2
    low, high = split_arcs(load_game("spg"))
    for arc, rows in (("low", low), ("high", high)):
        pairs = [(r, m) for r, m in calc["spg"]["ballistics"][arc]]
        diffs = []
        print("\nSPH-2 %s arc  (range m, game mrad, calc mil, game-calc)" % arc)
        for m, d, _ in rows:
            c = interp(pairs, d)
            if c is None:
                continue
            diffs.append(m - c)
            print("%8.0f %8.0f %9.1f %+9.1f" % (d, m, c, m - c))
        print("difference: " + spread(diffs))
    # Mortar
    pairs = [(r, m) for r, m in calc["mortar"]["ballistics"]["single"]]
    diffs = []
    print("\nL81 Mortar  (range m, game mrad, calc mil, game-calc)")
    for m, d, _ in load_game("mortar"):
        c = interp(pairs, d)
        if c is None:
            continue
        diffs.append(m - c)
        print("%8.0f %8.0f %9.1f %+9.1f" % (d, m, c, m - c))
    print("difference: " + spread(diffs))
    print("\nStingray: no calculator table; the calculator's mortar table is not the Stingray's.")


def compare_sim():
    sys.path.insert(0, HERE)
    import shell_sim as S
    low, high = split_arcs(load_game("spg"))
    print("\n== SPH-2 game rows against shell_sim.py, Expensive shell, elevation = mrad/1000 rad")
    for arc, rows in (("low", low), ("high", high)):
        print("\nSPH-2 %s arc  (game mrad, game range, sim range, sim-game m, game time, sim time, sim-game s)" % arc)
        dr, dt = [], []
        for m, d, t in rows:
            r = S.fly(math.degrees(m / 1000.0), "Expensive", dt_ms=1.0)
            if r is None:
                print("%7.0f %8.0f   no landing" % (m, d))
                continue
            dr.append(r[0] - d)
            dt.append(r[1] - t)
            print("%7.0f %8.0f %8.1f %+8.1f %8.2f %8.2f %+7.2f" % (m, d, r[0], r[0] - d, t, r[1], r[1] - t))
        print("range difference (m): " + spread(dr))
        print("time difference (s):  " + spread(dt))
        print("time ratio sim/game:  " + "min %.3f max %.3f" % (
            min(1 + a / b for a, b in zip(dt, [r[2] for r in rows])), max(1 + a / b for a, b in zip(dt, [r[2] for r in rows]))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--calc", help="path to the community calculator's weapons.json (read only)")
    ap.add_argument("--no-sim", action="store_true", help="skip the shell_sim.py comparison")
    a = ap.parse_args()
    print_tables()
    if a.calc:
        compare_calc(a.calc)
    if not a.no_sim:
        compare_sim()
    return 0


if __name__ == "__main__":
    sys.exit(main())
