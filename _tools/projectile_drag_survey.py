"""DragModel.Value across every projectile data asset, with the outliers and what they imply.

    python -I _tools/projectile_drag_survey.py            # survey table, outliers, implied terminal speed and range

Reads every WDProjectileData asset under data/ (the Caliber folders plus the few item-folder ones), fills the
fields an asset omits from the FWDProjectileStats constructor defaults (pipelines/Wardogs_ProjectileFlight_v1.md
section 5: DragModel.Value 1.0, Length 1.5, Diameter 0.9, Mass 0.00746), and runs _tools/shell_sim.py's drag
term and integrator on each. Nothing is fitted: the inputs are the asset values, rho 1.2, gravity -980 cm/s^2 and
the asset's own CT_Projectile_DragCoefficients row. The launch speed for the range figure is the 155 mm
artillery's 300 m/s, used only as a common yardstick (other weapons launch at other speeds).
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

DEFAULTS = {"value": 1.0, "length": 1.5, "diam": 0.9, "mass": 0.00746}
OUTLIER_FACTOR = 3.0  # more than 3x the median of the assets that set a Value


def split_exports(text):
    for part in re.split(r"^--- export:.*---\s*$", text, flags=re.M):
        part = part.strip()
        if part:
            try:
                obj = json.loads(part)
            except ValueError:
                continue
            yield from (obj if isinstance(obj, list) else [obj])


def load():
    rows = []
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "**", "*.json"), recursive=True)):
        with open(p, encoding="utf-8") as f:
            text = f.read()
        if "WDProjectileData" not in text[:800]:
            continue
        for o in split_exports(text):
            if o.get("Type") != "WDProjectileData":
                continue
            ps = o["Properties"]["ProjectileStats"]
            d = ps.get("ProjectileDimensions", {})
            dm = d.get("DragModel", {})
            row = (dm.get("Curve") or {}).get("RowName")
            rows.append({
                "asset": o["Name"], "path": os.path.relpath(p, ROOT).replace("\\", "/"),
                "tag": (o["Properties"].get("ProjectileId") or {}).get("TagName", ""),
                "value": dm.get("Value", DEFAULTS["value"]), "value_set": "Value" in dm,
                "diam": d.get("Diameter", DEFAULTS["diam"]), "mass": d.get("Mass", DEFAULTS["mass"]),
                "length": d.get("Length", DEFAULTS["length"]), "row": row,
                "actor_moves": bool(ps.get("bActorHandlesProjectileMovement")),
                "thrust": bool(ps.get("bShouldThrust")), "lifetime": ps.get("MaxProjectileLifetime"),
            })
    return rows


def set_row(row):
    ss._CURVE = ss.load_curve(row)
    ss._T = [k[0] for k in ss._CURVE]
    ss._V = [k[1] for k in ss._CURVE]


def terminal_speed(p):
    """Lowest vertical speed (m/s) at which the drag deceleration equals gravity, or None."""
    g = -ss.GRAVITY_CMS2
    prev = 0.0
    for i in range(1, 6001):
        v = i * 0.1
        a = ss.drag_accel(0.0, -v * 100.0, p)[1]
        if a >= g:
            return v
    return None


def main():
    rows = load()
    vals = sorted(r["value"] for r in rows if r["value_set"])
    med = vals[len(vals) // 2]
    print(f"{len(rows)} projectile data assets; {len(vals)} set DragModel.Value (median {med:g}); "
          f"the others use the constructor default {DEFAULTS['value']:g}\n")
    print("| Asset | Calibre tag | DragModel.Value | Curve row | Mass (kg) | Diameter (cm) | Length (cm) | Actor moves it |")
    print("|---|---|---:|---|---:|---:|---:|---|")
    for r in sorted(rows, key=lambda r: -r["value"]):
        print(f"| `{r['asset']}` | `{r['tag']}` | {r['value']:g}{'' if r['value_set'] else ' (default)'} | {r['row']} | "
              f"{r['mass']:g} | {r['diam']:g} | {r['length']:g} | {'yes' if r['actor_moves'] else 'no'} |")
    out = [r for r in rows if r["value_set"] and r["value"] > OUTLIER_FACTOR * med]
    print(f"\nOutliers (Value above {OUTLIER_FACTOR:g} x the median {med:g}): " + ", ".join(f"{r['asset']} ({r['value']:g})" for r in out))
    print("\n| Asset | Value | Mass | Diameter | Terminal speed (m/s) | Drag decel at 300 m/s (m/s^2) | Max flat range at 300 m/s (m) |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    peers = [r for r in rows if r["row"] == "GC (Cylinder)" and r["mass"] >= 1.0]
    for r in sorted(peers, key=lambda r: -r["value"]):
        set_row(r["row"])
        p = {"value": r["value"], "mass": r["mass"], "diam": r["diam"]}
        ts = terminal_speed(p)
        a300 = -ss.drag_accel(300.0 * 100.0, 0.0, p)[0] / 100.0
        e, rng = ss.max_range(p, dt_ms=1.0)
        print(f"| `{r['asset']}` | {r['value']:g} | {r['mass']:g} | {r['diam']:g} | {'above 600' if ts is None else format(ts, '.1f')} | {a300:.1f} | {rng:.0f} (at {e:.1f} deg) |")
    set_row("GC (Cylinder)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
