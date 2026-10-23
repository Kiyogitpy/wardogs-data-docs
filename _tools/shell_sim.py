#!/usr/bin/env python3
"""Artillery shell flight simulator built only from the documented equations.

Source of every term: pipelines/Wardogs_ProjectileFlight_v1.md (sections 1, 4, 5, 8)
and game-features/Wardogs_ArtilleryShellFlight_v1.md.  There are NO fitted
parameters in this file.  The inputs are:

  * launch speed        InitialBulletSpeed of DA_TNK_01_Artillery_Weapon_Stats (30000 cm/s)
  * gravity             -980 cm/s^2 (BaseEngine.ini, PhysicsSettings)
  * drag                a = -(100/m) * 0.5*rho*Cd*(pi/4)*(D/100)^2*(|v|/100)^2 * v_hat
                        rho = 1.2, Cd = DragModel.Value * Curve(|v| in m/s)
  * 155 mm variants     Standard  Value 80,  m 70 kg, D 8.4 cm
                        Expensive Value 2.5, m 19 kg, D 10.5 cm
  * thrust, wind        none (155 mm sets no bShouldThrust; wind taken as zero)

The step length is the one unknown of the documented model (open item 3 on the
projectile-flight page: Rate, dt = floor(1000/Rate) ms).  `dt_ms` is therefore an
argument; the sensitivity to it is reported by the analysis, not tuned.

Integration (page section 1), per step:
    a  = g + a_drag(v)
    v1 = v + a*dt
    dx = (v + v1)/2 * dt
The motion is planar (no wind), so only (horizontal, vertical) are simulated.

Run `python -I _tools/shell_sim.py` for a self-test table (flat-ground range
versus elevation at fine dt).  The measured-shot comparison is not in the
repository (the shots are private); see docs/evidence/round21-artillery-range-check.md
for the aggregate statistics.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CURVE_PATH = os.path.join(ROOT, "data", "Wardogs", "Content", "Items", "Resources",
                          "Ammo", "Curves", "CT_Projectile_DragCoefficients.json")

RHO = 1.2                 # kg/m^3, page section 5
GRAVITY_CMS2 = -980.0     # page section 4
MUZZLE_SPEED_CMS = 30000.0  # DA_TNK_01_Artillery_Weapon_Stats.InitialBulletSpeed
MAX_LIFETIME_S = 40.0     # MaxProjectileLifetime of the 155 mm data assets

VARIANTS = {
    "Standard": {"value": 80.0, "mass": 70.0, "diam": 8.4},
    "Expensive": {"value": 2.5, "mass": 19.0, "diam": 10.5},
}


def load_curve(row="GC (Cylinder)"):
    t = open(CURVE_PATH, encoding="utf8").read()
    j = json.loads(t[t.index("{"):])
    keys = j["Rows"][row]["Keys"]
    return [(k["Time"], k["Value"]) for k in keys]


_CURVE = load_curve()
_T = [k[0] for k in _CURVE]
_V = [k[1] for k in _CURVE]


def curve(speed_ms):
    """Linear interpolation, constant extrapolation (RichCurve default)."""
    if speed_ms <= _T[0]:
        return _V[0]
    if speed_ms >= _T[-1]:
        return _V[-1]
    lo, hi = 0, len(_T) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _T[mid] <= speed_ms:
            lo = mid
        else:
            hi = mid
    f = (speed_ms - _T[lo]) / (_T[hi] - _T[lo])
    return _V[lo] + f * (_V[hi] - _V[lo])


def drag_accel(vx, vz, p):
    """Drag acceleration in cm/s^2 for velocity (vx, vz) in cm/s."""
    s2 = vx * vx + vz * vz
    if s2 <= 1e-8:
        return 0.0, 0.0
    s = math.sqrt(s2)
    cd = p["value"] * curve(s * 0.01)
    area = math.pi / 4.0 * (p["diam"] / 100.0) ** 2
    force = 0.5 * RHO * cd * area * (s / 100.0) ** 2          # newtons
    a = -100.0 * force / max(p["mass"], 0.001)                # cm/s^2 along v_hat
    return a * vx / s, a * vz / s


def fly(elev_deg, variant="Standard", dt_ms=1.0, muzzle_h_m=0.0, target_dz_m=0.0,
        speed_cms=MUZZLE_SPEED_CMS, drag=True, want_path=False):
    """Fly one shell.  Returns (horizontal_m, flight_time_s, apex_m, impact_speed_ms).

    The shell lands when it crosses height muzzle_h_m + target_dz_m going down
    (target_dz_m is the target height relative to the barrel root; 0 = flat).
    Returns None if it never comes down to that height within the lifetime.
    """
    p = VARIANTS[variant] if isinstance(variant, str) else variant
    dt = dt_ms * 0.001
    th = math.radians(elev_deg)
    x, z = 0.0, muzzle_h_m * 100.0
    vx, vz = speed_cms * math.cos(th), speed_cms * math.sin(th)
    zt = (muzzle_h_m + target_dz_m) * 100.0
    t = 0.0
    apex = z
    while t < MAX_LIFETIME_S:
        ax, az = (drag_accel(vx, vz, p) if drag else (0.0, 0.0))
        az += GRAVITY_CMS2
        vx1, vz1 = vx + ax * dt, vz + az * dt
        nx = x + 0.5 * (vx + vx1) * dt
        nz = z + 0.5 * (vz + vz1) * dt
        if vz1 < 0 and nz <= zt < z + 1e-9 or (nz <= zt and z > zt and vz1 < 0):
            f = (z - zt) / (z - nz) if z != nz else 1.0
            hx = x + f * (nx - x)
            return hx / 100.0, t + f * dt, max(apex, z) / 100.0, math.hypot(vx1, vz1) / 100.0
        x, z, vx, vz = nx, nz, vx1, vz1
        apex = max(apex, z)
        t += dt
    return None


def flat_range(elev_deg, variant="Standard", dt_ms=1.0, muzzle_h_m=0.0, **kw):
    r = fly(elev_deg, variant, dt_ms, muzzle_h_m, 0.0, **kw)
    return None if r is None else r[0]


def max_range(variant="Standard", dt_ms=1.0, lo=2.0, hi=80.0, muzzle_h_m=0.0, **kw):
    """Golden-section search for the elevation of maximum flat range."""
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = flat_range(c, variant, dt_ms, muzzle_h_m, **kw), flat_range(d, variant, dt_ms, muzzle_h_m, **kw)
    for _ in range(40):
        if (fc or 0) > (fd or 0):
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = flat_range(c, variant, dt_ms, muzzle_h_m, **kw)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = flat_range(d, variant, dt_ms, muzzle_h_m, **kw)
    e = 0.5 * (a + b)
    return e, flat_range(e, variant, dt_ms, muzzle_h_m, **kw)


def main():
    print("flat-ground range (m), muzzle speed 300 m/s, dt 1 ms, muzzle height 0")
    print("elev_deg  Standard  Expensive  no-drag")
    for e in (2, 5, 10, 15, 20, 25, 30, 34, 40, 45, 50, 60, 70, 80):
        row = [flat_range(e, v) for v in ("Standard", "Expensive")]
        nd = flat_range(e, "Standard", drag=False)
        print("%7.1f  %8.1f  %9.1f  %8.1f" % (e, row[0] or 0, row[1] or 0, nd or 0))
    for v in ("Standard", "Expensive"):
        e, r = max_range(v)
        print(v, "max range %.1f m at %.2f deg" % (r, e))


if __name__ == "__main__":
    sys.exit(main())
