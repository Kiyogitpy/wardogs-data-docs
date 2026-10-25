#!/usr/bin/env python3
"""The game's own artillery range function, re-implemented from static disassembly.

Source: the body of WDArtilleryRangeLibrary::SimulateImpactDistance, RVA 0x761D180
(exec thunk 0x69A0900; round 40, docs/evidence/round40-weapons.md item A5).
Read from the code, not fitted:

  * elevation  = dial_mil * 0.001 + 0.016808 rad    (constants 0x9AAFD68, 0xB62DCCC)
  * launch     = InitialBulletSpeed * 0.01 m/s      (getter 0x6BBD500)
  * gravity    = 9.8 m/s^2                          (0.049 per half step, 0.098 per step)
  * step       = 10 ms, midpoint (two drag evaluations per step)
  * drag accel = Cd(v) * (rho/2) * (pi/4 d^2 * 1e-4) * v^2 / m   (d in cm, m in kg)
                 Cd = DragModel.Value * curve(v), the same as shell_sim.py
  * loop ends at the first step with height <= 0; no interpolation; limit 100000 steps
  * the result is the horizontal distance in metres

`--check` compares it with the SPH-2 ArtilleryRangeData rows (start height 3 m,
Expensive 155 mm shell): mean absolute error 5.1 m over 40 rows, against 77 m
without the 16.808 mrad term.  Usage:  python -I _tools/artillery_range_native.py [--check] [mil ...]
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell_sim as S  # noqa: E402

ELEV_OFFSET_RAD = 0.016808   # 16.808 mrad, 0.9630 degrees
SPEED_MS = 300.0             # DA_TNK_01_Artillery_Weapon_Stats.InitialBulletSpeed 30000 cm/s
START_HEIGHT_M = 3.0         # best fit to the table; the real HUD passes the altitude above sea level


def impact_distance(dial_mil, variant="Expensive", altitude_m=START_HEIGHT_M, rho=1.2,
                    offset=ELEV_OFFSET_RAD, speed=SPEED_MS):
    p = S.VARIANTS[variant]
    area = math.pi / 4.0 * p["diam"] ** 2 * 1e-4

    def drag(v):
        return p["value"] * S.curve(v) * (rho * 0.5) * (v * v * area) / p["mass"]

    ang = dial_mil * 0.001 + offset
    vx, vz = math.cos(ang) * speed, math.sin(ang) * speed
    x, z = 0.0, altitude_m
    for _ in range(100000):
        v = math.hypot(vx, vz)
        a = drag(v)
        hx, hz = (vx / v, vz / v) if v * v > 1e-8 else (0.0, 0.0)
        mx, mz = vx - a * hx * 0.005, vz - a * hz * 0.005 - 0.049
        m = math.hypot(mx, mz)
        a2 = drag(m)
        gx, gz = (mx / m, mz / m) if m * m > 1e-8 else (0.0, 0.0)
        z += mz * 0.01
        x += mx * 0.01
        vx -= a2 * gx * 0.01
        vz -= a2 * gz * 0.01 + 0.098
        if z <= 0.0:
            break
    return x


def check():
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([sys.executable, "-I", os.path.join(here, "artillery_range_tables.py")],
                         capture_output=True, text=True).stdout
    sec = out.split("== L81")[0]
    rows = [(int(a), int(b)) for a, b, _ in re.findall(r"^\s+(\d+)\s+(\d+)\s+([\d.]+)$", sec, re.M)]
    for off in (0.0, ELEV_OFFSET_RAD):
        err = [abs(impact_distance(m, offset=off) - d) for m, d in rows]
        print(f"offset {off:.6f} rad: {len(rows)} rows, mean abs error {sum(err)/len(err):.1f} m, max {max(err):.1f} m")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--check" in args or not args:
        check()
    for a in args:
        if a != "--check":
            print(a, round(impact_distance(float(a)), 1))
