"""Damage by weapon, ammo type and distance: the distance curve and the speed scale applied to the
point-blank table.

Builds on weapon_damage_tables.py (the point-blank per-hit damage) and damage_tables.py (data readers);
nothing of their logic is copied or changed.

    python _tools/weapon_damage_falloff.py --json                            # write assets/data/weapon-damage-falloff.json
    python _tools/weapon_damage_falloff.py --rank FMJ None Torso 600         # rank weapons at 600 m
    python _tools/weapon_damage_falloff.py --check                           # PASS/FAIL

Model (per weapon x ammo row, all inputs from data/ and the native findings cited in the docs):
    damage(d) = point_blank_damage x curve(d) x speed_scale(d)
  * curve(d): the weapon's DistanceDamageFalloffCurve, evaluated as Unreal's FRichCurve::Eval does. Keys are
    in centimetres. Before the first key and after the last key the value is held (the export sets no
    extrapolation mode, which is the engine default, constant). Between keys the segment uses the INTERP MODE OF
    ITS FIRST KEY: RCIM_Linear lerps; RCIM_Constant holds that key's value; RCIM_Cubic is a cubic Hermite spline
    with tangents Key0.LeaveTangent x dt and Key1.ArriveTangent x dt (all keys here have TangentWeightMode
    RCTWM_WeightedNone, so the weights are not used). The curve is applied only when the weapon stats set
    bUseDistanceDamageFalloffCurve (DamagePipeline v2 section 7.6); a stored curve with the flag absent
    (M500, MP43) is reported but not applied, as damage_tables.py does.
  * speed_scale(d) = clamp(speed(d) / reference, 0, 1) (DamagePipeline v2 section 7.6). reference is the weapon's
    TypicalSpeed when bOverrideTypicalSpeed is set and > 0, else the projectile asset's TypicalSpeed.
  * speed(d): the projectile's speed after flying distance d along the line of sight, from InitialBulletSpeed,
    with drag only (gravity left out: a level shot drops out of reach; compensated_speed() solves the elevated
    shot for the sensitivity check), drag per Projectile Flight section 5
    (rho 1.2, Cd = DragModel.Value x Curve(|v| in m/s), linear key interpolation of the CT_Projectile_
    DragCoefficients row, constant beyond its ends), trapezoid step as Projectile Flight section 1, step 1 ms,
    no wind, no thrust.
    Where a projectile asset lacks Length, Diameter, Mass or a resolvable drag row, the row is marked
    derived_no_drag and keeps the curve-only value.

JSON schema (assets/data/weapon-damage-falloff.json)
    meta        generator, source_data_tree, distances_m, assumptions, status vocabulary, unit, drag settings
    weapons[]   one per weapon in weapon-damage.json:
        id, name, caliber, effective_range_m (stats EffectiveRange, informational, not applied or null),
        initial_bullet_speed_cm_s, override_typical_speed ({enabled, value_cm_s}),
        curve {stored, used, applied_exactly, keys[], range_end_m, cubic_vs_linear, note}
            keys[]   time_cm, distance_m, value, interp (RCIM_*), arrive_tangent, leave_tangent
            applied_exactly  true when every segment interp mode was evaluated as the engine does
            cubic_vs_linear  null, or {max_abs_multiplier_diff, max_relative_damage_diff_pct, at_m}: the largest
                             difference between the exact curve and the linear approximation damage_tables.py
                             --falloff prints, over 0..range_end at 10 cm steps
        ammo[]: one per ammo row of weapon-damage.json:
            id, pellets, projectile, base_damage, modifier_stats_note (null, or the unmodeled ammo-modifier note)
            drag {value, curve_row, diameter_cm, length_cm, mass_kg, usable, reason}
            reference_speed {cm_s, source ("weapon_override" | "projectile_TypicalSpeed")}
            speed_scale_bites_at_m  first modelled distance at which speed < reference (null if never within
                                    the range of the model, or not computable)
            curve_multiplier[]      aligned to meta.distances_m
            speed_cm_s[]            projectile speed at each distance (null when not computable)
            speed_scale[]           clamp(speed / reference, 0, 1) (null when not computable)
            status[]                "not_reached_in_model" (flight ends before that distance within 12 s; damage null),
                                    "curve_only_exact" (speed scale proven 1 at that distance),
                                    "curve_x_speed_scale", "derived_no_drag" (curve-only value kept),
                                    "no_curve" (multiplier 1, no curve)
            damage {torso: {None, Light, Medium, Heavy, SuperHeavy: []}, head: {same}}
                        per hit, rounded to 1 decimal; per pellet for shotgun rounds
Unit: health points per hit. Point blank (0 m) uses the muzzle speed, so a weapon whose muzzle speed is below
its reference speed already has a scale below 1 at 0 m; speed_scale[0] says so.
"""
import json
import math
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402
import weapon_damage_tables as wd  # noqa: E402

ROOT, DATA = dt.ROOT, dt.DATA
OUT = os.path.join(ROOT, "assets", "data", "weapon-damage-falloff.json")
POINT_BLANK = os.path.join(ROOT, "assets", "data", "weapon-damage.json")
DISTANCES_M = [0, 25, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500]
DRAG_TABLE = os.path.join(DATA, "Wardogs/Content/Items/Resources/Ammo/Curves/CT_Projectile_DragCoefficients.json")
RHO = 1.2
GRAVITY = -980.0
STEP_S = 0.001
MAX_FLIGHT_S = 12.0
ARMOR = wd.ARMOR_CLASSES


# ---------------------------------------------------------------- distance curve
def eval_curve(keys, cm):
    """FRichCurve::Eval for non-weighted keys, constant extrapolation. keys: dicts sorted by Time."""
    if not keys:
        return 1.0
    if cm <= keys[0]["Time"]:
        return keys[0]["Value"]
    if cm >= keys[-1]["Time"]:
        return keys[-1]["Value"]
    for k0, k1 in zip(keys, keys[1:]):
        if cm < k1["Time"]:
            break
    d = k1["Time"] - k0["Time"]
    a = (cm - k0["Time"]) / d
    mode = k0.get("InterpMode", "RCIM_Linear")
    if mode == "RCIM_Constant":
        return k0["Value"]
    if mode == "RCIM_Cubic":
        t0, t1 = k0.get("LeaveTangent", 0.0) * d, k1.get("ArriveTangent", 0.0) * d
        a2, a3 = a * a, a * a * a
        return ((2 * a3 - 3 * a2 + 1) * k0["Value"] + (a3 - 2 * a2 + a) * t0 + (a3 - a2) * t1
                + (-2 * a3 + 3 * a2) * k1["Value"])
    return k0["Value"] + (k1["Value"] - k0["Value"]) * a


def cubic_vs_linear(keys, base_scale=1.0):
    """Largest difference between the exact curve and damage_tables.falloff (linear through every key)."""
    if not any(k.get("InterpMode") == "RCIM_Cubic" for k in keys):
        return None
    worst = (0.0, 0.0, 0)
    for cm in range(0, int(keys[-1]["Time"]) + 1, 10):
        e, l = eval_curve(keys, cm), dt.falloff(keys, cm)
        diff = abs(e - l)
        if diff > worst[0]:
            worst = (diff, diff / e if e else 0.0, cm)
    return {"max_abs_multiplier_diff": round(worst[0], 5), "max_relative_damage_diff_pct": round(100 * worst[1], 2),
            "at_m": worst[2] / 100}


# ---------------------------------------------------------------- weapon / projectile data
def weapon_stats(stats_path):
    ex = dt.exports(stats_path)

    def first(key):
        return next((v for o in ex for v in dt.walk(o, key)), None)
    curve = first("DistanceDamageFalloffCurve")
    keys = sorted(curve.get("EditorCurveData", {}).get("Keys", []), key=lambda k: k["Time"]) if curve else []
    return {"use": bool(first("bUseDistanceDamageFalloffCurve")), "keys": keys,
            "ibs": first("InitialBulletSpeed"), "override": bool(first("bOverrideTypicalSpeed")),
            "typical": first("TypicalSpeed"), "range": first("EffectiveRange")}


_PROJ = {}


def projectile_stats():
    """ProjectileId -> dims, drag model, TypicalSpeed from the same asset dt.projectiles() picks."""
    if _PROJ:
        return _PROJ
    import glob
    pattern = os.path.join(DATA, "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json")
    for path in sorted(glob.glob(pattern, recursive=True)):
        for o in dt.exports(path):
            props = o.get("Properties", {})
            pid, stats = dt.tag(props.get("ProjectileId")), props.get("ProjectileStats")
            if not pid or not stats:
                continue
            if pid not in _PROJ or os.path.basename(path).count("_") <= 2:
                dims = stats.get("ProjectileDimensions", {})
                dm = dims.get("DragModel", {})
                _PROJ[pid] = {"typical": stats.get("TypicalSpeed"), "length": dims.get("Length"),
                              "diameter": dims.get("Diameter"), "mass": dims.get("Mass"),
                              "value": dm.get("Value", 1.0 if dm else None),
                              "row": (dm.get("Curve") or {}).get("RowName"), "asset": os.path.basename(path)}
    return _PROJ


_DRAG = {}


def drag_rows():
    if not _DRAG:
        t = open(DRAG_TABLE, encoding="utf8").read()
        for row, v in json.loads(t[t.index("{"):])["Rows"].items():
            _DRAG[row] = ([k["Time"] for k in v["Keys"]], [k["Value"] for k in v["Keys"]], v["InterpMode"])
    return _DRAG


def drag_cd(row, speed_ms):
    xs, ys, _ = drag_rows()[row]
    if speed_ms <= xs[0]:
        return ys[0]
    if speed_ms >= xs[-1]:
        return ys[-1]
    for i in range(1, len(xs)):
        if speed_ms <= xs[i]:
            return ys[i - 1] + (ys[i] - ys[i - 1]) * (speed_ms - xs[i - 1]) / (xs[i] - xs[i - 1])


def drag_usable(p):
    if p is None:
        return False, "no projectile data asset for the ProjectileId"
    for f in ("length", "diameter", "mass"):
        if not isinstance(p[f], (int, float)):
            return False, f"projectile asset sets no {f}"
    if not p["row"] or p["row"] not in drag_rows():
        return False, "no resolvable drag curve row"
    if not drag_rows()[p["row"]][2].endswith("RCIM_Linear"):
        return False, "drag row is not linear"
    return True, None


_FLIGHT = {}


def step_drag(p, area, mass, vx, vz, g):
    s2 = vx * vx + vz * vz
    ax = az = 0.0
    if s2 > 1e-8:
        s = math.sqrt(s2)
        force = 0.5 * RHO * p["value"] * drag_cd(p["row"], s * 0.01) * area * (s / 100) ** 2
        a = -100.0 * force / mass
        ax, az = a * vx / s, a * vz / s
    return ax, az + g


def flight(pid, v0, max_m, gravity=False, step=STEP_S):
    """Samples (distance_cm, speed_cm_s, time_s) of a shot along the line of sight (launch angle 0, gravity
    omitted unless gravity=True), trapezoid steps of `step` seconds, until max_m or MAX_FLIGHT_S."""
    key = (pid, v0, max_m, gravity, step)
    if key in _FLIGHT:
        return _FLIGHT[key]
    p = projectile_stats()[pid]
    area = math.pi / 4 * (p["diameter"] / 100) ** 2
    mass = max(p["mass"], 0.001)
    g = GRAVITY if gravity else 0.0
    x, z, vx, vz, t = 0.0, 0.0, v0, 0.0, 0.0
    out = [(0.0, v0, 0.0)]
    while t < MAX_FLIGHT_S and math.hypot(x, z) < max_m * 100:
        ax, az = step_drag(p, area, mass, vx, vz, g)
        vx1, vz1 = vx + ax * step, vz + az * step
        x += 0.5 * (vx + vx1) * step
        z += 0.5 * (vz + vz1) * step
        vx, vz = vx1, vz1
        t += step
        out.append((math.hypot(x, z), math.hypot(vx, vz), t))
    _FLIGHT[key] = out
    return out


def compensated_speed(pid, v0, range_m, step=STEP_S):
    """Impact speed (cm/s) of a shot elevated to land at the muzzle height range_m away (gravity on)."""
    p = projectile_stats()[pid]
    area = math.pi / 4 * (p["diameter"] / 100) ** 2
    mass = max(p["mass"], 0.001)

    def land(theta):
        x, z, vx, vz = 0.0, 0.0, v0 * math.cos(theta), v0 * math.sin(theta)
        for _ in range(int(40.0 / step)):
            ax, az = step_drag(p, area, mass, vx, vz, GRAVITY)
            vx1, vz1 = vx + ax * step, vz + az * step
            nx, nz = x + 0.5 * (vx + vx1) * step, z + 0.5 * (vz + vz1) * step
            if nz <= 0 and vz1 < 0:
                f = z / (z - nz)
                return x + f * (nx - x), math.hypot(vx1, vz1)
            x, z, vx, vz = nx, nz, vx1, vz1
        return None, None
    lo, hi = 0.0, math.radians(30)
    if (land(hi)[0] or 0) < range_m * 100:
        return None
    for _ in range(40):
        mid = (lo + hi) / 2
        r, _s = land(mid)
        if r is None or r > range_m * 100:
            hi = mid
        else:
            lo = mid
    return land((lo + hi) / 2)[1]


def at_distance(samples, cm):
    """(speed, time) at straight-line distance cm, None if the flight ends first."""
    if cm > samples[-1][0]:
        return None
    lo, hi = 0, len(samples) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if samples[mid][0] <= cm:
            lo = mid
        else:
            hi = mid
    (d0, v0, t0), (d1, v1, t1) = samples[lo], samples[hi]
    f = 0.0 if d1 == d0 else (cm - d0) / (d1 - d0)
    return v0 + (v1 - v0) * f, t0 + (t1 - t0) * f


# ---------------------------------------------------------------- build
def build():
    pb = wd.build()
    files = wd.weapon_files()
    proj = projectile_stats()
    weapons = []
    summary = {"speed_scale_bites": [], "cubic": [], "no_drag": []}
    far = max(DISTANCES_M)
    for w in pb["weapons"]:
        st = weapon_stats(files[w["id"]][1])
        keys = st["keys"]
        used = st["use"] and bool(keys)
        interp = sorted({k.get("InterpMode") for k in keys})
        exact = all(m in ("RCIM_Linear", "RCIM_Constant", "RCIM_Cubic") for m in interp)
        cub = cubic_vs_linear(keys) if used else None
        if used:
            note = ("cubic segments evaluated as a Hermite spline from the stored tangents" if cub
                    else "all segments linear")
        elif keys:
            note = "curve stored but bUseDistanceDamageFalloffCurve is absent (false): not applied, multiplier 1"
        else:
            note = "no distance curve in the stats asset: multiplier 1"
        override = st["override"] and isinstance(st["typical"], (int, float)) and st["typical"] > 0
        cw = {"id": w["id"], "name": w["name"], "caliber": w["caliber"],
              "effective_range_m": st["range"], "initial_bullet_speed_cm_s": st["ibs"],
              "override_typical_speed": {"enabled": bool(override), "value_cm_s": st["typical"] if override else None},
              "curve": {"stored": bool(keys), "used": used, "applied_exactly": exact if used else None,
                        "keys": [{"time_cm": k["Time"], "distance_m": k["Time"] / 100, "value": k["Value"],
                                  "interp": k.get("InterpMode"), "arrive_tangent": k.get("ArriveTangent"),
                                  "leave_tangent": k.get("LeaveTangent")} for k in keys],
                        "range_end_m": keys[-1]["Time"] / 100 if keys else None,
                        "cubic_vs_linear": cub, "note": note},
              "ammo": []}
        if cub:
            summary["cubic"].append({"weapon": w["id"], **cub})
        mult = [eval_curve(keys, d * 100) if used else 1.0 for d in DISTANCES_M]
        for a in w["ammo"]:
            p = proj.get(a["projectile"])
            ok, why = drag_usable(p)
            ref = st["typical"] if override else (p or {}).get("typical")
            ref_src = "weapon_override" if override else "projectile_TypicalSpeed"
            valid = ok and isinstance(ref, (int, float)) and ref > 0 and isinstance(st["ibs"], (int, float))
            if ok and not valid:
                why = "no usable reference speed or InitialBulletSpeed"
            speeds, scales, status, bites = [], [], [], None
            samples = flight(a["projectile"], st["ibs"], max(far, math.ceil((keys[-1]["Time"] / 100) if keys else 0))) if valid else None
            for d, m in zip(DISTANCES_M, mult):
                got = at_distance(samples, d * 100) if valid else None
                if got is None:
                    speeds.append(None)
                    scales.append(None)
                    status.append("not_reached_in_model" if valid else "derived_no_drag")
                    continue
                v = got[0]
                s = min(max(v / ref, 0.0), 1.0)
                speeds.append(round(v, 1))
                scales.append(round(s, 5))
                status.append("curve_only_exact" if s >= 1.0 else "curve_x_speed_scale")
            if valid:
                for cm in range(0, int(samples[-1][0]) + 1, 100):
                    got = at_distance(samples, cm)
                    if got and got[0] < ref:
                        bites = cm / 100
                        break
            if not used:
                status = ["no_curve" if s == "curve_only_exact" else s for s in status]
            note = None
            if a["modifier_tag"]:
                note = ("ammo-modifier multipliers on projectile stats (native 0x6BBAB70, 'CachedModifiedProjectileStats') "
                        "are not in the data: drag and reference speed use the base projectile asset")
            dmg = {"torso": {}, "head": {}}
            for grp, src in (("torso", "torso_armor"), ("head", "head_armor")):
                for c in ARMOR:
                    base = a["damage_raw"][src][c]
                    dmg[grp][c] = [None if st_ == "not_reached_in_model" else
                                   round(base * m * (s if s is not None else 1.0), 1)
                                   for m, s, st_ in zip(mult, scales, status)]
            if valid and bites is not None:
                summary["speed_scale_bites"].append({"weapon": w["id"], "ammo": a["id"], "from_m": bites,
                                                     "reference_cm_s": ref, "reference_source": ref_src})
            if not valid:
                summary["no_drag"].append({"weapon": w["id"], "ammo": a["id"], "reason": why})
            cw["ammo"].append({
                "id": a["id"], "pellets": a["pellets"], "projectile": a["projectile"], "base_damage": a["base_damage"],
                "modifier_stats_note": note,
                "drag": {"value": (p or {}).get("value"), "curve_row": (p or {}).get("row"),
                         "diameter_cm": (p or {}).get("diameter"), "length_cm": (p or {}).get("length"),
                         "mass_kg": (p or {}).get("mass"), "usable": valid, "reason": why},
                "reference_speed": {"cm_s": ref, "source": ref_src},
                "speed_scale_bites_at_m": bites,
                "curve_multiplier": [round(m, 5) for m in mult], "speed_cm_s": speeds, "speed_scale": scales,
                "status": status, "damage": dmg})
        weapons.append(cw)
    tree = subprocess.run(["git", "rev-parse", "HEAD:data"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    return {"meta": {
        "generator": "python _tools/weapon_damage_falloff.py --json",
        "source_data_tree": tree, "distances_m": DISTANCES_M,
        "unit": "health points per hit (per pellet for shotgun rounds; multiply by `pellets`)",
        "assumptions": [
            "damage(d) = point-blank damage x curve(d) x speed_scale(d); the factor chain in the rule table is linear in the starting amount (damage_tables.evaluate), the same assumption damage_tables.py --falloff makes",
            "speed along the line of sight: drag only, gravity left out (a flat shot cannot reach 1200 m); d is the distance from the muzzle; no spread, wind or thrust; the effect of gravity with the shot elevated to hit at the muzzle height is quantified in docs/evidence/round25-falloff.md",
            "drag integrated in 1 ms steps; the game's step is floor(1000/Rate) ms with Rate unread (Projectile Flight open item 3); see docs/evidence/round25-falloff.md for the step sensitivity",
            "armor classes and hit locations as in weapon-damage.json: torso is Torso.Upper, head is Head with a helmet of the named class",
            "curve extrapolation is constant before the first and after the last key (the export names no mode; engine default)"],
        "status_vocabulary": {"curve_only_exact": "speed scale is 1 at that distance; value = point blank x curve",
                              "curve_x_speed_scale": "speed has fallen below the reference speed; value = point blank x curve x scale",
                              "derived_no_drag": "the drag model could not be applied; value keeps the curve-only number",
                              "not_reached_in_model": "the modelled projectile has not flown that far within max_flight_s; damage is null",
                              "no_curve": "weapon has no applied distance curve and the speed scale is 1"},
        "drag": {"rho_kg_m3": RHO, "gravity_cm_s2": GRAVITY, "step_s": STEP_S, "max_flight_s": MAX_FLIGHT_S},
        "summary": summary},
        "weapons": weapons}


def write_json():
    j = build()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(j, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(j['weapons'])} weapons, "
          f"{sum(len(w['ammo']) for w in j['weapons'])} weapon x ammo rows")


# ---------------------------------------------------------------- rank
def rank(ammo, armor, loc, dist):
    j = build()
    key = {a.lower(): a for a in wd.OPTION_ORDER}
    ammo = wd.ALIASES.get(ammo.lower(), key.get(ammo.lower(), ammo))
    armor = {c.lower(): c for c in ARMOR}.get(armor.lower(), armor)
    grp = {"torso": "torso", "torso.upper": "torso", "head": "head"}.get(loc.lower())
    if grp is None or armor not in ARMOR:
        sys.exit(f"location must be Torso or Head; armor one of {ARMOR}")
    dist = float(dist)
    ds = j["meta"]["distances_m"]
    rows = []
    for w in j["weapons"]:
        a = next((x for x in w["ammo"] if x["id"] == ammo), None)
        if not a:
            continue
        if dist in ds:
            i = ds.index(dist)
            val, st = a["damage"][grp][armor][i], a["status"][i]
        else:
            sys.exit(f"distance must be one of {ds} (metres)")
        if val is not None:
            rows.append((val, w, a, st))
    rows.sort(key=lambda r: (-r[0], r[1]["id"]))
    print(f"{ammo} vs {armor} {grp} at {dist:g} m: damage per hit, {len(rows)} weapons "
          "(shotgun values are per pellet; identical values share a rank)")
    print("| Rank | Weapon | Name | Caliber | Damage | Status | Curve end (m) |")
    print("|---:|---|---|---|---:|---|---:|")
    n, last = 0, None
    for i, (v, w, a, st) in enumerate(rows, 1):
        if last is None or round(v, 1) != round(last, 1):
            n = i
        last = v
        end = w["curve"]["range_end_m"] if w["curve"]["used"] else None
        print(f"| {n} | {w['id']} | {w['name']} | {w['caliber']} | {v:.1f} | {st} | {'' if end is None else format(end, 'g')} |")


# ---------------------------------------------------------------- check
def check():
    sys.stdout.reconfigure(encoding="utf-8")
    j = build()
    pb = wd.build()
    pb_by = {w["id"]: w for w in pb["weapons"]}
    fails = 0

    def report(ok, msg):
        nonlocal fails
        fails += not ok
        print(("PASS " if ok else "FAIL ") + msg)

    # (a) damage_tables.py --falloff: torso unarmored, every weapon it prints, at its six ranges.
    run = subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "damage_tables.py"), "--falloff"],
                         capture_output=True, encoding="utf-8", check=True)
    old = {}
    for line in run.stdout.splitlines()[2:]:
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) == 8:
            old[c[0].rstrip("†")] = (c[0].endswith("†"), c[2:])
    ranges = [50, 100, 200, 400, 800, 1200]
    by = {w["id"]: w for w in j["weapons"]}
    bad, n_lin, n_cub, cubic_names = [], 0, 0, []
    for name, (cubic, cells) in old.items():
        w = by.get(name)
        if not w:
            continue
        a = next(x for x in w["ammo"] if x["id"] in ("FMJ", "Buckshot"))
        base = pb_by[name]["ammo"][[x["id"] for x in pb_by[name]["ammo"]].index(a["id"])]["damage_raw"]["torso_armor"]["None"]
        keys = weapon_stats(wd.weapon_files()[name][1])["keys"]
        if cubic:
            n_cub += 1
            cubic_names.append(name)
            continue
        n_lin += 1
        mine = [f"{base * dt.falloff(keys, r * 100):.1f}" for r in ranges]
        # the JSON's own multipliers must give the same cells
        idx = [j["meta"]["distances_m"].index(r) for r in ranges]
        mine_json = [f"{base * a['curve_multiplier'][i]:.1f}" for i in idx]
        if not w["curve"]["used"]:
            mine = mine_json = [f"{base:.1f}"] * len(ranges)
        if mine_json != cells:
            bad.append(f"{name}: json {mine_json} vs table {cells}")
    report(not bad and n_lin > 0, f"{n_lin} linear-key weapons reproduce damage_tables.py --falloff at {ranges} m"
           + (f"; differs: {bad}" if bad else ""))
    # cubic weapons: the Hermite evaluation passes through every key, and the dagger rows agree with it at the
    # distances where both lie on a linear segment or a key. The size of the difference is reported, not asserted.
    worst = {c["weapon"]: c for c in j["meta"]["summary"]["cubic"]}
    through = all(abs(eval_curve(k_, k["Time"]) - k["Value"]) < 1e-9
                  for n in cubic_names
                  for k_ in [weapon_stats(wd.weapon_files()[n][1])["keys"]] for k in k_)
    report(through and set(cubic_names) <= set(worst),
           f"{n_cub} cubic-key weapons: exact curve passes through every key; largest multiplier difference from the "
           "linear approximation: " + ", ".join(f"{n} {worst[n]['max_abs_multiplier_diff']} at {worst[n]['at_m']} m"
                                                for n in cubic_names if n in worst))
    # (b) point blank.
    bad = []
    n = 0
    for w in j["weapons"]:
        pw = pb_by[w["id"]]
        for a in w["ammo"]:
            pa = next(x for x in pw["ammo"] if x["id"] == a["id"])
            assert a["curve_multiplier"][0] == 1.0, (w["id"], a["curve_multiplier"][0])
            for grp, src in (("torso", "torso_armor"), ("head", "head_armor")):
                for c in ARMOR:
                    n += 1
                    mine = round(pa["damage_raw"][src][c] * a["curve_multiplier"][0], 1)
                    if mine != pa["damage"][src][c]:
                        bad.append(f"{w['id']}:{a['id']}:{grp}:{c}")
    report(not bad, f"curve-only value at 0 m equals weapon-damage generator output for {n} cells" + (f"; differs {bad[:5]}" if bad else ""))
    if os.path.exists(POINT_BLANK):
        stored = json.load(open(POINT_BLANK, encoding="utf-8"))
        sb = {w["id"]: w for w in stored["weapons"]}
        bad, n = [], 0
        for w in j["weapons"]:
            for a in w["ammo"]:
                sa = next((x for x in sb[w["id"]]["ammo"] if x["id"] == a["id"]), None)
                if sa is None:
                    bad.append(f"{w['id']}:{a['id']} missing")
                    continue
                for grp, src in (("torso", "torso_armor"), ("head", "head_armor")):
                    for c in ARMOR:
                        n += 1
                        s0 = a["speed_scale"][0] if a["speed_scale"][0] is not None else 1.0
                        mine = a["damage"][grp][c][0]
                        expect = round(sa["damage_raw"][src][c] * s0, 1)
                        if abs(mine - expect) > 1e-9:
                            bad.append(f"{w['id']}:{a['id']}:{grp}:{c}")
        report(not bad, f"0 m damage equals assets/data/weapon-damage.json x muzzle speed scale for {n} cells"
               + (f"; differs {bad[:5]}" if bad else ""))
        at0 = [(w["id"], a["id"], a["speed_scale"][0]) for w in j["weapons"] for a in w["ammo"]
               if a["speed_scale"][0] not in (1.0, None)]
        report(not at0, "speed scale is 1 at 0 m for every row (muzzle speed at or above the reference speed)"
               + (f"; below 1 for {at0}" if at0 else ""))
        keys_ok = [w["id"] for w in j["weapons"] if w["id"] in sb] == [w["id"] for w in stored["weapons"]]
        report(keys_ok and len(j["weapons"]) == len(stored["weapons"]),
               f"same {len(stored['weapons'])} weapons as weapon-damage.json")
    else:
        print("SKIP assets/data/weapon-damage.json not found")
    print("FAILED" if fails else "ALL PASSED")
    sys.exit(1 if fails else 0)


def sensitivity():
    """Speed at distance for the default round: line of sight (1 ms), line of sight (10 and 16 ms steps), and the
    shot elevated to land at the muzzle height with gravity on (1 ms)."""
    pb = wd.build()
    files = wd.weapon_files()
    seen = set()
    print("| Weapon | Round | Ref cm/s | m | LOS 1 ms | LOS 10 ms | LOS 16 ms | Elevated shot |")
    print("|---|---|---:|---:|---:|---:|---:|---:|")
    for w in pb["weapons"]:
        st = weapon_stats(files[w["id"]][1])
        a = next(x for x in w["ammo"] if x["id"] in ("FMJ", "Buckshot"))
        key = (a["projectile"], st["ibs"])
        if key in seen:
            continue
        seen.add(key)
        p = projectile_stats()[a["projectile"]]
        ref = st["typical"] if st["override"] and st["typical"] else p["typical"]
        for m in (200, 400, 800, 1200):
            cells = []
            for step in (0.001, 0.01, 0.016):
                got = at_distance(flight(a["projectile"], st["ibs"], 1200, step=step), m * 100)
                cells.append(f"{got[0]:.0f}" if got else "-")
            cs = compensated_speed(a["projectile"], st["ibs"], m, 0.004)
            print(f"| {w['id']} | {a['id']} | {ref:g} | {m} | " + " | ".join(cells) + f" | {cs:.0f} |" if cs else
                  f"| {w['id']} | {a['id']} | {ref:g} | {m} | " + " | ".join(cells) + " | unreachable |")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if "--sensitivity" in a:
        sensitivity()
    elif "--check" in a:
        check()
    elif "--json" in a:
        write_json()
    elif "--rank" in a:
        i = a.index("--rank")
        if len(a) < i + 5:
            sys.exit("usage: --rank AMMO ARMOR LOCATION DISTANCE_M   e.g. --rank FMJ None Torso 600")
        rank(*a[i + 1:i + 5])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
