#!/usr/bin/env python3
"""Aggregate comparison of shell_sim.py against (a) logged impacts and (b) a
calculator's mil/range table.  Prints aggregate statistics only.

The logged shots and the calculator table are private inputs and are NOT in the
repository; pass them on the command line:

    python -I _tools/artillery_range_check.py --shots shots.csv --calc calculator_weapons.json

Shots CSV columns used: dz_m, dial_mil, fired_arc, impact_distance_m, long_m,
right_m, tilt_pitch_deg.  Calculator JSON: weapons[id == "spg"].ballistics.low/high
as [range_m, mil] pairs.
"""
import argparse
import csv
import json
import math
import os
import random
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell_sim as S  # noqa: E402

CONVENTIONS = {"NATO 6400/rev": 6400.0, "Warsaw 6000/rev": 6000.0, "milliradian 2000*pi/rev": 2000.0 * math.pi}


def fnum(x):
    return float(x) if x not in ("", None) else None


def quart(v):
    v = sorted(v)
    n = len(v)
    if n == 0:
        return (float("nan"),) * 3
    return st.quantiles(v, n=4, method="inclusive")[0] if n > 1 else v[0], st.median(v), \
        (st.quantiles(v, n=4, method="inclusive")[2] if n > 1 else v[0])


def summarize(label, res):
    if not res:
        return "| %s | 0 | - | - | - | - | - |" % label
    q1, med, q3 = quart(res)
    ab = sorted(abs(x) for x in res)
    return "| %s | %d | %+.1f | %+.1f to %+.1f | %.1f | %.1f |" % (
        label, len(res), med, q1, q3, st.median(ab), ab[-1])


def predict(shots, conv, variant, dt_ms, h0, dz_sign, offset_mil=0.0, tilt=False):
    res = []
    for r in shots:
        dz = fnum(r["dz_m"]) or 0.0
        th = (fnum(r["dial_mil"]) + offset_mil) * 360.0 / conv
        if tilt:
            th += fnum(r["tilt_pitch_deg"]) or 0.0
        o = S.fly(th, variant, dt_ms, h0, dz_sign * dz - h0)  # dz is ground-to-ground, muzzle sits h0 above the gun ground
        if o is None:
            res.append(None)
        else:
            res.append(o[0] - fnum(r["impact_distance_m"]))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", required=True)
    ap.add_argument("--calc", required=True)
    ap.add_argument("--dt", type=float, default=4.0, help="exploration dt in ms (finals use 1 ms)")
    ap.add_argument("--only", default="ABCD", help="sections to run, e.g. D")
    a = ap.parse_args()
    if a.only == "D":
        section_d(a)
        return
    rows = list(csv.DictReader(open(a.shots, encoding="utf8")))
    shots = [r for r in rows if r["dial_mil"] and r["fired_arc"]]
    nonzero = [r for r in shots if not (fnum(r["long_m"]) == 0 and fnum(r["right_m"]) == 0)]
    print("shots total %d, with dial+arc %d, of which exact-zero-error %d" % (
        len(rows), len(shots), len(shots) - len(nonzero)))
    print("distinct (planned distance, dial) pairs:", len({(r["distance_m"], r["dial_mil"]) for r in shots}))
    print()
    hdr = "| Hypothesis | N | median pred-meas (m) | IQR (m) | median abs (m) | max abs (m) |\n|---|---:|---:|---|---:|---:|"

    print("## A. no free parameter: variant x mil convention (dz target above gun, h0=0)")
    print(hdr)
    for var in ("Expensive", "Standard"):
        for name, conv in CONVENTIONS.items():
            res = predict(nonzero, conv, var, a.dt, 0.0, +1)
            print(summarize("%s, %s" % (var, name), [x for x in res if x is not None]),
                  "(never lands: %d)" % sum(1 for x in res if x is None) if None in res else "")

    print("\n## E. replicate scatter of the log itself (same planned distance and dial)")
    groups = {}
    for r in nonzero:
        groups.setdefault((r["distance_m"], r["dial_mil"], r["dz_m"]), []).append(fnum(r["impact_distance_m"]))
    devs = [x - st.mean(g) for g in groups.values() if len(g) >= 3 for x in g]
    big = [len(g) for g in groups.values() if len(g) >= 3]
    if devs:
        ad = sorted(abs(x) for x in devs)
        print("groups with >=3 replicates: %d (sizes %s); deviation from group mean: median abs %.1f m, max abs %.1f m, N %d" % (
            len(big), sorted(big), st.median(ad), ad[-1], len(ad)))
    if a.only == "E":
        return

    print("\n## B. Expensive, milliradian: robustness to the unknowns")
    print(hdr)
    conv = 2000.0 * math.pi
    for dz_sign in (+1, -1):
        res = predict(nonzero, conv, "Expensive", a.dt, 0.0, dz_sign)
        print(summarize("dz sign %+d" % dz_sign, [x for x in res if x is not None]))
    for h0 in (0.0, 2.0, 3.0):
        res = predict(nonzero, conv, "Expensive", a.dt, h0, +1)
        print(summarize("muzzle height %.0f m" % h0, [x for x in res if x is not None]))
    res = predict(nonzero, conv, "Expensive", a.dt, 0.0, +1, tilt=True)
    print(summarize("dial + logged tilt", [x for x in res if x is not None]))
    for dt in (1.0, 4.0, 8.0, 16.0, 33.0):
        res = predict(nonzero, conv, "Expensive", dt, 0.0, +1)
        print(summarize("step %g ms (Rate=%d)" % (dt, round(1000 / dt)), [x for x in res if x is not None]))
    for arc in ("low", "high"):
        sub = [r for r in nonzero if r["fired_arc"] == arc]
        res = predict(sub, conv, "Expensive", a.dt, 0.0, +1)
        print(summarize("arc %s" % arc, [x for x in res if x is not None]))
    for lab, sub in (("dz given", [r for r in nonzero if r["dz_m"] != ""]),
                     ("dz blank (treated 0)", [r for r in nonzero if r["dz_m"] == ""])):
        res = predict(sub, conv, "Expensive", a.dt, 0.0, +1)
        print(summarize(lab, [x for x in res if x is not None]))

    print("\n## C. one measured offset (the only free parameter), per convention")
    random.seed(1)
    for name, conv in CONVENTIONS.items():
        grid = [o * 10.0 for o in range(-30, 31)]
        # residual matrix once (shots x offsets); None (never lands) counts as a 5 km miss
        mat = {o: [abs(x) if x is not None else 5000.0
                   for x in predict(nonzero, conv, "Expensive", 8.0, 0.0, +1, o)] for o in grid}

        def med_abs_idx(o, idx):
            return st.median([mat[o][i] for i in idx])
        idx_all = list(range(len(nonzero)))
        best = min(grid, key=lambda o: med_abs_idx(o, idx_all))
        boots = []
        for _ in range(100):
            idx = [random.randrange(len(nonzero)) for _ in nonzero]
            boots.append(min(grid, key=lambda o: med_abs_idx(o, idx)))
        boots.sort()
        res = predict(nonzero, conv, "Expensive", a.dt, 0.0, +1, best)
        print("%s: best offset %+.0f mil (bootstrap 2.5-97.5%%: %+.0f to %+.0f)" % (
            name, best, boots[1], boots[-2]))
        print(hdr.split("\n")[0]); print(summarize("  at best offset", [x for x in res if x is not None]))

    section_d(a)


def section_d(a):
    print("\n## D. flat-ground curve vs calculator table")
    calc = json.load(open(a.calc, encoding="utf8"))
    tab = [w for w in calc["weapons"] if w["id"] == "spg"][0]["ballistics"]
    for var in ("Expensive", "Standard"):
        for h0 in (0.0, 3.0):
            e, r = S.max_range(var, 1.0, 2.0, 80.0, h0)
            print("%s h0=%g: max range %.1f m at %.2f deg = %.0f mil(6400) = %.0f mrad" % (
                var, h0, r, e, e * 6400 / 360, e * math.pi / 180 * 1000))
    for dt in (1.0, 8.0, 16.0, 33.0):
        e, r = S.max_range("Expensive", dt)
        print("Expensive dt %g ms: max range %.1f m at %.2f deg" % (dt, r, e))
    allr = [p[0] for arc in tab.values() for p in arc]
    pk = max(allr)
    pm = [p[1] for p in tab["low"] + tab["high"] if p[0] == pk]
    print("table: max range %d m at dial %s mil; extent low %s..%s, high %s..%s" % (
        pk, pm, tab["low"][0], tab["low"][-1], tab["high"][0], tab["high"][-1]))
    e0, r0 = S.max_range("Expensive", 1.0)

    def sim_elev(rng, arc):
        lo, hi = (0.2, e0) if arc == "low" else (e0, 89.5)
        for _ in range(45):
            m = 0.5 * (lo + hi)
            r = S.flat_range(m, "Expensive", 2.0) or 0.0
            too_short = r < rng
            if arc == "low":      # range rises with elevation below the peak
                lo, hi = (m, hi) if too_short else (lo, m)
            else:                 # range falls with elevation above the peak
                lo, hi = (lo, m) if too_short else (m, hi)
        return 0.5 * (lo + hi)

    print("\nper-point dial offset needed (sim elevation expressed in the convention, minus table dial), mil")
    print("| Convention | Arc | points used | median offset | IQR | min..max |\n|---|---|---:|---|---|---|")
    elev = {arc: [(sim_elev(rng, arc), mil) for rng, mil in tab[arc] if 0 < rng < r0 - 1]
            for arc in ("low", "high")}
    for name, conv in CONVENTIONS.items():
        for arc in ("low", "high"):
            offs = [e * conv / 360.0 - mil for e, mil in elev[arc]]
            q1, med, q3 = quart(offs)
            print("| %s | %s | %d | %+.0f | %+.0f to %+.0f | %+.0f..%+.0f |" % (
                name, arc, len(offs), med, q1, q3, min(offs), max(offs)))


if __name__ == "__main__":
    main()
