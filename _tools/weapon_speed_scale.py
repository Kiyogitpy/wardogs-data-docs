#!/usr/bin/env python3
"""Speed scale after drag for every weapon (damage-pipeline section 7.8), round 41 item 49.

The damage pipeline multiplies base damage by clamp(impact speed / reference speed, 0, 1), where the reference
is the weapon's TypicalSpeed when bOverrideTypicalSpeed is set and > 0, else the projectile asset's TypicalSpeed
(0x6C255B0).  The tables in weapon_damage_tables.py leave this factor at 1.  This script flies each weapon's
bullet with the game's drag term (shell_sim.py: Cd = DragModel.Value * curve(v), rho 1.2, g 9.8 m/s^2, 1 ms
step, launched level) and reports the horizontal distance at which the speed first drops below the reference
(speed scale < 1) and the scale at 100, 200, 300, 400 and 600 m.  Nothing is fitted; ammunition variants
(tracer, AP, ...) that change TypicalSpeed through DA_AmmoModifier are not applied.

    python -I _tools/weapon_speed_scale.py            # markdown table
"""
import glob
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import shell_sim as ss  # noqa: E402
import projectile_drag_survey as ds  # noqa: E402

DISTS = (100, 200, 300, 400, 600)


def exports(path):
    text = open(path, encoding="utf-8").read()
    return list(ds.split_exports(text))


def weapons():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "**", "DA_*_Stats.json"), recursive=True)):
        for o in exports(p):
            if o.get("Type") != "WDWeaponStatsData":
                continue
            txt = json.dumps(o)
            ibs = re.search(r'"InitialBulletSpeed": ([0-9.]+)', txt)
            cal = re.search(r'"SupportedCaliber": \["(Item\.Caliber\.[^"]+)"', txt)
            if not ibs or not cal:
                continue
            ov = re.search(r'"bOverrideTypicalSpeed": true,\s*"TypicalSpeed": ([0-9.]+)', txt)
            out.append({"name": o["Name"].replace("DA_", "").replace("_Stats", ""), "speed": float(ibs.group(1)),
                        "caliber": cal.group(1), "typ_w": float(ov.group(1)) if ov else None})
    return out


def projectiles():
    res = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "**", "*.json"), recursive=True)):
        t = open(p, encoding="utf-8").read(800)
        if "WDProjectileData" not in t:
            continue
        for o in exports(p):
            if o.get("Type") != "WDProjectileData":
                continue
            ps = o["Properties"]["ProjectileStats"]
            d = ps.get("ProjectileDimensions", {})
            dm = d.get("DragModel", {})
            tag = (o["Properties"].get("ProjectileId") or {}).get("TagName", "")
            if tag and tag not in res:
                res[tag] = {"value": dm.get("Value", ds.DEFAULTS["value"]), "diam": d.get("Diameter", ds.DEFAULTS["diam"]),
                            "mass": d.get("Mass", ds.DEFAULTS["mass"]), "row": (dm.get("Curve") or {}).get("RowName"),
                            "typ": ps.get("TypicalSpeed"), "asset": o["Name"]}
    return res


def profile(speed_cms, p, row):
    """Speed (cm/s) at each requested horizontal distance, level launch."""
    ds.set_row(row or "GC (Cylinder)")
    x, z, vx, vz, dt = 0.0, 0.0, speed_cms, 0.0, 0.001
    out, want = {}, list(DISTS)
    for _ in range(4000):
        ax, az = ss.drag_accel(vx, vz, p)
        vx += ax * dt
        vz += (az + ss.GRAVITY_CMS2) * dt
        x += vx * dt
        z += vz * dt
        while want and x >= want[0] * 100.0:
            out[want.pop(0)] = math.hypot(vx, vz)
        if not want:
            break
    return out


def below(speed_cms, p, row, ref):
    ds.set_row(row or "GC (Cylinder)")
    x, vx, vz, dt = 0.0, speed_cms, 0.0, 0.001
    if speed_cms < ref:
        return 0.0
    for _ in range(20000):
        ax, az = ss.drag_accel(vx, vz, p)
        vx += ax * dt
        vz += (az + ss.GRAVITY_CMS2) * dt
        x += vx * dt
        if math.hypot(vx, vz) < ref:
            return x / 100.0
    return None


def main():
    pr = projectiles()
    print("| Weapon | Ammo | Muzzle (m/s) | Reference (m/s) | Speed scale below 1 beyond (m) | " + " | ".join(f"{d} m" for d in DISTS) + " |")
    print("|---|---|---:|---:|---:|" + "---:|" * len(DISTS))
    for w in sorted(weapons(), key=lambda w: w["name"]):
        a = pr.get(w["caliber"])
        if not a:
            continue
        ref = w["typ_w"] if w["typ_w"] else a["typ"]
        if not ref:
            continue
        prof = profile(w["speed"], a, a["row"])
        b = below(w["speed"], a, a["row"], ref)
        sc = ["%.2f" % min(1.0, prof[d] / ref) if d in prof else "-" for d in DISTS]
        print(f"| {w['name']} | {w['caliber'].split('.')[-1]} | {w['speed']/100:.0f} | {ref/100:.0f}{' (weapon)' if w['typ_w'] else ''} | "
              f"{'from the muzzle' if b == 0 else ('%.0f' % b if b else 'beyond 2 km')} | " + " | ".join(sc) + " |")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
