"""Independent verifier for the round 25 data (teammates F falloff, G locations, H penetration).

Recomputes from the raw data/ export only. It does NOT import damage_tables.py,
weapon_damage_tables.py, weapon_damage_falloff.py, weapon_damage_locations.py or
weapon_penetration.py. Each check prints PASS or FAIL; exit status is 1 on any FAIL.
Run:  python _tools/verify_round25.py [falloff|locations|penetration]
"""
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs")
FAILS = []
RESULTS = {}


def exports(path):
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"^--- export:.*---\s*$", text, flags=re.M)
    return [json.loads(p) for p in parts[1:] if p.strip()]


def tg(x):
    return x.get("TagName") if isinstance(x, dict) else x


def check(name, ok, detail=""):
    print("%s %s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)
    return ok


def load_json(rel):
    return json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))


def walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                yield v
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)


# =============================================================== F, falloff
STATS = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(DATA, "**/DA_*_Stats.json"), recursive=True)}
_WS = {}


def weapon_stats(wid):
    if wid in _WS:
        return _WS[wid]
    path = next(iter(glob.glob(os.path.join(DATA, "Plugins/GameFeatures/Weapons/**/ID_%s.json" % wid), recursive=True)))
    name = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", open(path, encoding="utf-8").read()).group(1)
    for o in exports(STATS[name]):
        p = (o.get("Properties") or {}).get("WeaponStats") or {}
        if "InitialBulletSpeed" in p:
            _WS[wid] = p
            return p
    raise KeyError(wid)


def curve_keys(props):
    c = props.get("DistanceDamageFalloffCurve")
    if not c:
        return None
    return c.get("EditorCurveData", {}).get("Keys") or None


def hermite(p0, t0, p1, t1, a):
    a2, a3 = a * a, a * a * a
    return (2 * a3 - 3 * a2 + 1) * p0 + (a3 - 2 * a2 + a) * t0 + (a3 - a2) * t1 + (-2 * a3 + 3 * a2) * p1


def eval_curve(keys, x):
    """Unreal FRichCurve::Eval, constant extrapolation before the first and after the last key."""
    if x <= keys[0]["Time"]:
        return keys[0]["Value"]
    if x >= keys[-1]["Time"]:
        return keys[-1]["Value"]
    for k1, k2 in zip(keys, keys[1:]):
        if k1["Time"] <= x < k2["Time"]:
            diff = k2["Time"] - k1["Time"]
            mode = k1.get("InterpMode", "RCIM_Linear")
            if mode == "RCIM_Constant":
                return k1["Value"]
            al = (x - k1["Time"]) / diff
            if mode == "RCIM_Linear":
                return k1["Value"] + (k2["Value"] - k1["Value"]) * al
            return hermite(k1["Value"], k1.get("LeaveTangent", 0.0) * diff,
                           k2["Value"], k2.get("ArriveTangent", 0.0) * diff, al)
    return keys[-1]["Value"]


def lin_only(keys, x):
    return eval_curve([dict(k, InterpMode="RCIM_Linear") for k in keys], x)


_DR = {}


def drag_rows():
    if not _DR:
        p = os.path.join(DATA, "Content/Items/Resources/Ammo/Curves/CT_Projectile_DragCoefficients.json")
        for name, r in exports(p)[0]["Rows"].items():
            _DR[name] = (r.get("InterpMode", ""), [(k["Time"], k["Value"]) for k in r["Keys"]])
    return _DR


def drag_eval(row, v):
    mode, ks = row
    if v <= ks[0][0]:
        return ks[0][1]
    if v >= ks[-1][0]:
        return ks[-1][1]
    for (t1, v1), (t2, v2) in zip(ks, ks[1:]):
        if t1 <= v < t2:
            if "Constant" in mode:
                return v1
            return v1 + (v2 - v1) * (v - t1) / (t2 - t1)
    return ks[-1][1]


def projectile_assets():
    out = {}
    for p in glob.glob(os.path.join(DATA, "Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json"), recursive=True):
        for o in exports(p):
            pr = o.get("Properties", {})
            if pr.get("ProjectileStats") and pr.get("ProjectileId"):
                out.setdefault(tg(pr["ProjectileId"]), []).append((os.path.basename(p), pr["ProjectileStats"]))
    return out


def fly(dim, v0, row, x_target_m, dt=0.0005):
    """RK4 along the line of sight, drag only. Returns [(distance m, speed cm/s)]."""
    D = dim["Diameter"]
    m = max(dim["Mass"], 0.001)
    val = dim["DragModel"].get("Value", 1.0)

    def acc(v):
        cd = val * drag_eval(row, v * 0.01)
        F = 0.5 * 1.2 * cd * (math.pi / 4) * (D / 100.0) ** 2 * (v / 100.0) ** 2
        return 100.0 * F / m

    v, x, t = v0, 0.0, 0.0
    pts = [(0.0, v0)]
    while x < x_target_m * 100.0 and t < 12.0:
        k1v = -acc(v); k1x = v
        k2v = -acc(v + 0.5 * dt * k1v); k2x = v + 0.5 * dt * k1v
        k3v = -acc(v + 0.5 * dt * k2v); k3x = v + 0.5 * dt * k2v
        k4v = -acc(v + dt * k3v); k4x = v + dt * k3v
        v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        x += dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        t += dt
        pts.append((x / 100.0, v))
    return pts


def interp_pts(pts, xm):
    for (x1, v1), (x2, v2) in zip(pts, pts[1:]):
        if x1 <= xm <= x2:
            return v1 + (v2 - v1) * (xm - x1) / (x2 - x1) if x2 > x1 else v1
    return None


def cross_distance(pts, ref):
    for (x1, v1), (x2, v2) in zip(pts, pts[1:]):
        if v1 >= ref > v2:
            return x1 + (x2 - x1) * (v1 - ref) / (v1 - v2)
    return None


def run_falloff():
    print("== F falloff ==")
    fo = load_json("assets/data/weapon-damage-falloff.json")
    dists = fo["meta"]["distances_m"]
    check("F distances list", dists == [0, 25, 50, 100, 150, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500], str(dists))
    W = {w["id"]: w for w in fo["weapons"]}
    check("F weapon count 33", len(W) == 33, str(len(W)))
    projs = projectile_assets()
    rows = drag_rows()
    check("F drag curve rows all linear", all("Linear" in m for m, _ in rows.values()), str({m for m, _ in rows.values()}))

    maxall = 0.0
    per = {}
    n_stored = n_none = 0
    for wid, w in W.items():
        props = weapon_stats(wid)
        keys = curve_keys(props)
        used_raw = bool(props.get("bUseDistanceDamageFalloffCurve", False))
        c = w["curve"]
        if keys is None:
            n_none += 1
            check("F %s no stored curve" % wid, not c["stored"], "json stored=%s used=%s" % (c["stored"], c["used"]))
            for a in w["ammo"]:
                if any(abs(m - 1.0) > 1e-9 for m in a["curve_multiplier"]):
                    check("F %s curve multiplier 1" % wid, False)
            continue
        n_stored += 1
        check("F %s used flag" % wid, c["used"] == used_raw, "raw %s json %s" % (used_raw, c["used"]))
        jk = c["keys"]
        okk = len(jk) == len(keys) and all(abs(a["time_cm"] - b["Time"]) < 1e-3 and abs(a["value"] - b["Value"]) < 1e-6
                                           and a["interp"] == b["InterpMode"]
                                           and abs(a["arrive_tangent"] - b.get("ArriveTangent", 0)) <= 1e-9 + 1e-6 * abs(b.get("ArriveTangent", 0))
                                           and abs(a["leave_tangent"] - b.get("LeaveTangent", 0)) <= 1e-9 + 1e-6 * abs(b.get("LeaveTangent", 0))
                                           for a, b in zip(jk, keys))
        check("F %s curve keys/interp/tangents match raw" % wid, okk)
        md = 0.0
        for a in w["ammo"]:
            for d, jm in zip(dists, a["curve_multiplier"]):
                mine = eval_curve(keys, d * 100.0) if used_raw else 1.0
                md = max(md, abs(mine - jm))
        per[wid] = md
        maxall = max(maxall, md)
    print("   weapons with a stored curve: %d, without: %d" % (n_stored, n_none))
    RESULTS["F_curve_max_diff"] = maxall
    check("F curve multiplier at the 14 distances, all %d weapons x all ammo rows (max abs diff %.2e)" % (len(W), maxall), maxall < 5e-5)
    print("   per weapon max diff:", ", ".join("%s %.1e" % (k, v) for k, v in per.items()))

    # ---- linear versus cubic
    print("-- linear approximation vs exact, four cubic SMGs")
    cub = ["WEPN_028", "MP9", "SMG_03", "WEPN_031"]
    claim_min = 1e9
    claim800 = 1e9
    for wid in cub:
        keys = curve_keys(weapon_stats(wid))
        assert any(k["InterpMode"] == "RCIM_Cubic" for k in keys), wid
        for d in (400, 600, 800, 1000):
            ex, li = eval_curve(keys, d * 100.0), lin_only(keys, d * 100.0)
            print("   %-9s %4d m exact %.4f linear %.4f overstatement %+.1f%%" % (wid, d, ex, li, (li / ex - 1) * 100))
            if d == 800:
                claim800 = min(claim800, li / ex - 1)
        worst = min((lin_only(keys, d * 100.0) / eval_curve(keys, d * 100.0) - 1, d) for d in range(400, 1001))
        print("   %-9s smallest overstatement over 400..1000 m (1 m steps): %+.1f%% at %d m" % (wid, worst[0] * 100, worst[1]))
        claim_min = min(claim_min, worst[0])
    RESULTS["F_linear_overstate_min_pct"] = claim_min * 100
    RESULTS["F_linear_overstate_800_min_pct"] = claim800 * 100
    check("F claim: linear overstates the 4 SMGs by >= 18%% over 400..1000 m (min %.1f%%)" % (claim_min * 100), claim_min >= 0.18)
    check("F claim: overstatement > 100%% at 800 m for all four (min %.1f%%)" % (claim800 * 100), claim800 > 1.0)
    for wid, claim, at in (("MP9", 0.218, 608.8), ("WEPN_028", 0.207, 673.0), ("SMG_03", 0.175, 691.6), ("WEPN_031", 0.175, 691.6)):
        ks = curve_keys(weapon_stats(wid))
        b = max((abs(lin_only(ks, x) - eval_curve(ks, x)), x) for x in [i * 10.0 for i in range(0, 120001)])
        check("F claim: %s largest |linear-exact| %.3f at %.1f m (mine %.4f at %.1f m)" % (wid, claim, at, b[0], b[1] / 100),
              abs(b[0] - claim) < 0.001 and abs(b[1] / 100 - at) < 1.0)
    claims = {("WEPN_028", 400): (0.442, 0.544), ("MP9", 400): (0.333, 0.500), ("SMG_03", 400): (0.462, 0.544),
              ("WEPN_028", 800): (0.133, 0.322), ("MP9", 800): (0.115, 0.300), ("SMG_03", 800): (0.158, 0.322)}
    for (wid, d), (e, l) in claims.items():
        ks = curve_keys(weapon_stats(wid))
        me, ml = eval_curve(ks, d * 100.0), lin_only(ks, d * 100.0)
        check("F claim: %s %d m exact %.3f linear %.3f (mine %.4f %.4f)" % (wid, d, e, l, me, ml), abs(me - e) < 6e-4 and abs(ml - l) < 6e-4)
    ks = curve_keys(weapon_stats("MP9"))
    print("   MP9 spline at 1000 m: %.4f (doc: 0.098); minimum over 100..1200 m: %s" % (eval_curve(ks, 100000.0), min((eval_curve(ks, float(x)), x / 100.0) for x in range(10000, 120001, 10))))

    # ---- structural claims
    ends = {wid: (curve_keys(weapon_stats(wid)) or [{"Time": None}])[-1]["Time"] for wid in W}
    e1200 = [w for w, t in ends.items() if t == 120000.0 and weapon_stats(w).get("bUseDistanceDamageFalloffCurve")]
    print("   last key 1200 m among weapons that apply a curve: %d; others: %s" % (len(e1200), {w: t for w, t in ends.items() if t != 120000.0}))
    check("F claim: last key at 1200 m for 25 weapons (counting curves that are applied; 27 store one)", len(e1200) == 25, str(len(e1200)))
    check("F claim: LMG_02, WEPN_036, SV98 end 1500 m; MK22 1600; SR_04 2500",
          ends["LMG_02"] == ends["WEPN_036"] == ends["SV98"] == 150000.0 and ends["MK22"] == 160000.0 and ends["SR_04"] == 250000.0)
    check("F claim: Judge has no curve; M500 and MP43 store a curve without the flag",
          curve_keys(weapon_stats("Judge")) is None
          and all(curve_keys(weapon_stats(x)) and not weapon_stats(x).get("bUseDistanceDamageFalloffCurve") for x in ("M500", "MP43")))
    check("F claim: Vector has six keys, all linear",
          len(curve_keys(weapon_stats("Vector"))) == 6 and all(k["InterpMode"] == "RCIM_Linear" for k in curve_keys(weapon_stats("Vector"))))
    cubw = sorted(w for w in W if curve_keys(weapon_stats(w)) and any(k["InterpMode"] == "RCIM_Cubic" for k in curve_keys(weapon_stats(w))))
    check("F claim: cubic weapons are exactly WEPN_028, MP9, SMG_03, WEPN_031", cubw == sorted(cub), str(cubw))
    for n in cub:
        print("   key modes %-9s %s" % (n, [(k["Time"] / 100, k["InterpMode"][5:9]) for k in curve_keys(weapon_stats(n))]))
    # 30 of 33 apply a curve
    applied = sum(1 for w in W if curve_keys(weapon_stats(w)) and weapon_stats(w).get("bUseDistanceDamageFalloffCurve"))
    check("F claim: 30 of 33 weapons apply a distance curve", applied == 30, str(applied))
    nov = [w for w in W if weapon_stats(w).get("bOverrideTypicalSpeed")]
    print("   weapons with bOverrideTypicalSpeed among the 33: %d (pipeline 7.8 text says 24 overrides in the data)" % len(nov))

    # ---- drag and speed scale
    print("-- drag model and speed scale bite distance (first whole metre where speed < reference)")
    maxbite = 0
    maxspd = 0.0
    allbite = []
    for wid, w in W.items():
        props = weapon_stats(wid)
        v0 = props["InitialBulletSpeed"]
        for a in w["ammo"]:
            cands = projs.get(a["projectile"], [])
            if not cands:
                check("F %s %s projectile asset" % (wid, a["id"]), False, a["projectile"])
                continue
            ps = cands[0][1]
            dim = ps["ProjectileDimensions"]
            row = rows[dim["DragModel"]["Curve"]["RowName"]]
            ref = props["TypicalSpeed"] if props.get("bOverrideTypicalSpeed") and props.get("TypicalSpeed", 0) > 0 else ps["TypicalSpeed"]
            if abs(ref - a["reference_speed"]["cm_s"]) > 1e-6:
                check("F %s %s reference speed" % (wid, a["id"]), False, "%s vs %s" % (ref, a["reference_speed"]["cm_s"]))
            if a["id"] not in ("FMJ", "Buckshot", "Slug"):
                continue
            pts = fly(dim, v0, row, 2200)
            cx = cross_distance(pts, ref)
            mine_bite = None if cx is None else math.floor(cx) + 1
            jb = a["speed_scale_bites_at_m"]
            diff = None if (mine_bite is None or jb is None) else mine_bite - jb
            allbite.append((wid, a["id"], jb, cx, mine_bite, diff))
            if diff is not None:
                maxbite = max(maxbite, abs(diff))
            for d, js in zip(dists, a["speed_cm_s"]):
                if js is None:
                    continue
                ms = interp_pts(pts, float(d))
                if ms is not None:
                    maxspd = max(maxspd, abs(ms - js) / js)
    for r in allbite:
        if r[0] in ("M4", "Glock17", "SV98", "MP9", "A91", "SR_04", "M500", "SMG_03", "LMG_02") and r[1] in ("FMJ", "Buckshot"):
            print("   %-9s %-9s json %-6s mine (continuous %s -> whole metre %s) diff %s" %
                  (r[0], r[1], r[2], None if r[3] is None else "%.2f" % r[3], r[4], r[5]))
    RESULTS["F_bite_max_diff_m"] = maxbite
    RESULTS["F_speed_max_rel"] = maxspd
    n_off = sum(1 for r in allbite if r[5] not in (0, None))
    print("   %d FMJ/Buckshot/Slug rows; rows differing by 1 m or more: %d; max |diff| %d m; max relative speed difference %.2e" %
          (len(allbite), n_off, maxbite, maxspd))
    check("F bite distance agrees within 1 m for all rows (max %d m)" % maxbite, maxbite <= 1)
    check("F modelled speed at the 14 distances within 0.5%% (max %.2e)" % maxspd, maxspd < 0.005)
    for n in ("M4", "Glock17", "SV98", "MP9"):
        r = next(r for r in allbite if r[0] == n and r[1] == "FMJ")
        check("F bite %s json %s mine %s" % (n, r[2], r[4]), r[5] is not None and abs(r[5]) <= 1)

    # ---- 12 s flight cap and step-size sensitivity
    print("-- flight cap and step size")
    for wid, tag in (("Glock17", "FMJ"), ("WEPN_026", "FMJ"), ("M500", "Buckshot")):
        a = next(x for x in W[wid]["ammo"] if x["id"] == tag)
        dim = projs[a["projectile"]][0][1]["ProjectileDimensions"]
        pts = fly(dim, weapon_stats(wid)["InitialBulletSpeed"], rows[dim["DragModel"]["Curve"]["RowName"]], 5000)
        print("   %s %s: distance after 12 s = %.0f m (doc: 9mm 1285, 45 1318, 7mm buckshot 1065)" % (wid, tag, pts[-1][0]))
    rates = {}
    for ms in (1, 16, 33):
        dt = ms / 1000.0
        worst = 0.0
        worst_row = None
        for wid in ("M4", "Glock17", "SV98", "MP9", "M500", "A91", "SMG_03"):
            w = W[wid]
            a = next(x for x in w["ammo"] if x["id"] in ("FMJ", "Buckshot"))
            props = weapon_stats(wid)
            dim = projs[a["projectile"]][0][1]["ProjectileDimensions"]
            row = rows[dim["DragModel"]["Curve"]["RowName"]]
            D, m, val = dim["Diameter"], max(dim["Mass"], 0.001), dim["DragModel"].get("Value", 1.0)
            v, x = props["InitialBulletSpeed"], 0.0
            ref = a["reference_speed"]["cm_s"]
            bite = None
            while x < 150000 and bite is None:
                cd = val * drag_eval(row, v * 0.01)
                acc = 100.0 * 0.5 * 1.2 * cd * (math.pi / 4) * (D / 100) ** 2 * (v / 100) ** 2 / m
                v2 = max(v - acc * dt, 0.0)
                x += 0.5 * (v + v2) * dt
                v = v2
                if v < ref:
                    bite = math.floor(x / 100.0) + 1
            if bite is not None:
                dif = bite - a["speed_scale_bites_at_m"]
                if abs(dif) / a["speed_scale_bites_at_m"] > worst:
                    worst, worst_row = abs(dif) / a["speed_scale_bites_at_m"], (wid, a["speed_scale_bites_at_m"], bite)
        rates[ms] = (worst, worst_row)
        print("   explicit-Euler %2d ms step: largest relative bite-distance change vs JSON %.1f%% at %s (json, mine)" % (ms, worst * 100, worst_row))
    RESULTS["F_step33_bite_change_pct"] = rates[33][0] * 100
    # ---- doc table
    doc = open(os.path.join(ROOT, "docs/evidence/round25-falloff.md"), encoding="utf-8").read()
    bad = 0
    nrows = 0
    for line in doc.splitlines():
        m = re.match(r"\| (\w+) \| (\d+) \| (\d+) \| (projectile TypicalSpeed|weapon override) \| (\d+) \| (\d*) \|", line)
        if not m:
            continue
        nrows += 1
        wid, v0, ref, src, bite, cend = m.groups()
        a = W[wid]["ammo"][0]
        props = weapon_stats(wid)
        want_src = "weapon override" if props.get("bOverrideTypicalSpeed") and props.get("TypicalSpeed", 0) > 0 else "projectile TypicalSpeed"
        kk = curve_keys(props)
        want_end = "" if kk is None else str(int(kk[-1]["Time"] / 100))
        if (float(v0) != props["InitialBulletSpeed"] or float(ref) != a["reference_speed"]["cm_s"]
                or float(bite) != a["speed_scale_bites_at_m"] or want_src != src or want_end != cend):
            bad += 1
            print("   doc row mismatch", wid, v0, ref, src, bite, cend)
    check("F doc speed table (%d rows) matches JSON and raw stats" % nrows, bad == 0 and nrows == 33, "%d mismatches" % bad)


# =============================================================== G, locations
ARMOR_DIR = os.path.join(DATA, "Plugins/GameFeatures/Items/Armor")
DMG = os.path.join(DATA, "Content/GameMechanics/DamageSystem/DamageDataTables")
HIT = "Meta.Damage.HitLocation.Infantry."


def dmg_table(name):
    return exports(os.path.join(DMG, name))[0]["Rows"]


def expand(tags):
    out = set()
    for t in tags:
        parts = t.split(".")
        for i in range(2, len(parts) + 1):
            out.add(".".join(parts[:i]))
    return out


def parent(t):
    return t.rsplit(".", 1)[0] if "." in t else None


def kv(lst):
    return {tg(x["Key"]): x["Value"] for x in lst}


def first_list(row):
    return next((val for val in row.values() if isinstance(val, list)), [])


_ENG = {}


def engine():
    if _ENG:
        return _ENG
    _ENG["ENTRIES"] = dmg_table("DT_GlobalDamage_InfantryData.json")["Meta.Damage.Infantry"]["DamageModificationEntries"]
    _ENG["BONE"] = {k: kv(v["HitLocations"]) for k, v in dmg_table("DT_Helpers/DT_InfantryData_BoneDamageModifiers.json").items()}
    _ENG["CAL"] = {k: kv(first_list(v)) for k, v in dmg_table("DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json").items()}
    _ENG["PEN"] = {k: (v.get("Modifier", 1.0), kv(first_list(v))) for k, v in dmg_table("DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json").items()}
    return _ENG


def armor_items():
    """Every WDInventoryFragment_Armor in the Armor plugin: id -> dict(tag, covered, stages R list)."""
    out = {}
    for p in sorted(glob.glob(os.path.join(ARMOR_DIR, "**/*.json"), recursive=True)):
        try:
            exs = exports(p)
        except Exception:
            continue
        for o in exs:
            if o.get("Type") == "WDInventoryFragment_Armor":
                pr = o["Properties"]
                st = pr.get("DurabilityStagesSetupData") or []
                out[os.path.basename(p)[:-5]] = {
                    "path": os.path.relpath(p, ROOT),
                    "tag": tg(pr.get("DamageContextTag")),
                    "covered": [tg(x).replace(HIT, "") for x in pr.get("CoveredHitLocations", [])],
                    "stages": [s.get("DamagePercentageReduction") for s in st],
                    "keys": sorted(pr.keys()),
                }
    return out


_PROJ = {}


def ammo_tables():
    if _PROJ:
        return _PROJ
    P, ITEMS = {}, {}
    for p in glob.glob(os.path.join(DATA, "Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json"), recursive=True):
        for o in exports(p):
            s = o.get("Properties", {}).get("ProjectileStats")
            if s:
                e = s["DamageEntityData"]
                P[o["Name"]] = (tg(e["Tag"]), [tg(c) for c in e.get("Context", [])], s["DamageValues"]["BaseDamage"])
    for p in glob.glob(os.path.join(DATA, "Content/Items/Resources/Ammo/**/ID_*.json"), recursive=True):
        ex = exports(p)
        d = next((o for o in ex if o.get("Type") == "BHInventoryItemDefinition"), None)
        pr = next((o for o in ex if o.get("Type") == "WDInventoryFragment_Projectile"), None)
        if d and pr:
            pd = re.search(r"'(DA_\w+)'", pr["Properties"]["ProjectileData"]["ObjectName"]).group(1)
            ITEMS[tg(d["Properties"]["ItemId"])] = pd
    _PROJ["P"], _PROJ["ITEMS"] = P, ITEMS
    return _PROJ


AMMO_MAP = {"Tracer", "HollowPoint", "HollowPoint.Tracer", "ArmorPiercing", "ArmorPiercing.Tracer"}


def modifier_tag(item_id):
    parts = item_id.split(".")
    key = ".".join(parts[-2:]) if len(parts) == 5 and parts[-1] == "Tracer" else parts[-1]
    return "Meta.Damage.AmmoModifier." + key if key in AMMO_MAP else None


def weapon_tag(wid):
    path = next(iter(glob.glob(os.path.join(DATA, "Plugins/GameFeatures/Weapons/**/ID_%s.json" % wid), recursive=True)))
    wtag = None
    for o in exports(path):
        for d in walk(o, "DamageEntityData"):
            t = tg(d.get("Tag", {}))
            if t and t.startswith("Meta.Damage.Weapon"):
                wtag = t
    return wtag


def rule_damage(wtag, item_id, hit, armor_tag, dpr_override=None, covering=True):
    """Damage of one hit by my own rule walk. armor_tag is the context tag of the covering piece, or None."""
    E = engine()
    A = ammo_tables()
    stag, ctx, base = A["P"][A["ITEMS"][item_id]]
    mod = modifier_tag(item_id)
    context = list(ctx) + ([mod] if mod else []) + [wtag]
    source = expand([stag] + context)
    target = expand([armor_tag]) if armor_tag else set()
    hitfull = HIT + hit
    lineage = expand([hitfull])
    c = float(base)
    for e in E["ENTRIES"]:
        m = e["OutModification"]
        reqs = [e["InstigatorRequirements"], e["TargetRequirements"], e["SourceRequirements"], e["PossibleHitLocations"]]
        if not any(reqs) and m["Amount"] == 0:
            continue
        if e["AlignmentRequired"].split("::")[-1] not in ("None", "Hostile"):
            continue
        if e["InstigatorRequirements"]:
            continue
        if not set(e["TargetRequirements"]) <= target or not set(e["SourceRequirements"]) <= source:
            continue
        if e["PossibleHitLocations"] and not set(e["PossibleHitLocations"]) & lineage:
            continue
        f = 1.0
        if m["bUseCustomOperation"]:
            cls = (m["CustomOperationClass"] or {}).get("ObjectName", "")
            if "BoneDamage" in cls:
                u = E["BONE"]["Universal"][hitfull]
                row = next((E["BONE"][t] for t in context if t in E["BONE"]), None) or \
                    next((E["BONE"][parent(t)] for t in context if parent(t) in E["BONE"]), None)
                f = u * (row[hitfull] if row else 1.0)
            elif "ArchetypeCaliber" in cls:
                row = next((E["CAL"][t] for t in context if t in E["CAL"]), None) or \
                    next((E["CAL"][parent(t)] for t in context if parent(t) in E["CAL"]), None)
                f = 1.0 if row is None else row.get(stag, row.get(parent(stag), 1.0))
            elif "AmmoTypeEffectiveness" in cls:
                piece = next((t for t in sorted(target) if t.startswith(("Meta.Damage.Armor.", "Meta.Damage.Helmet."))), None)
                r = dpr_override.get(piece, 0.0) if piece else 0.0
                ammo = mod or "Meta.Damage.AmmoModifier.FMJ"
                arms = next((t for t in context if t.startswith("Meta.Damage.Arms")), None)
                mo, ov = E["PEN"].get(ammo, (1.0, {}))
                f = 1 - r * ov.get(arms, mo) / 100
            else:
                continue
        elif m["Operation"].endswith("Percentage_Ongoing"):
            f = 1 + m["Amount"] / 100
        else:
            continue
        c *= f
    return max(c, 0.0)


def run_locations():
    print("== G locations ==")
    items = armor_items()
    jl = load_json("assets/data/weapon-damage-locations.json")
    meta = jl["meta"]
    mi = {a["id"]: a for a in meta["armor_items"]}
    print("   armor fragments found in the Armor plugin: %d; JSON armor_items: %d" % (len(items), len(mi)))
    check("G item set equal to JSON armor_items", set(items) == set(mi), str(sorted(set(items) ^ set(mi))))
    # other files in the plugin that mention CoveredHitLocations
    extra = []
    for p in glob.glob(os.path.join(DATA, "**/*.json"), recursive=True):
        if os.path.basename(p) in [i + ".json" for i in items]:
            continue
        with open(p, encoding="utf-8", errors="ignore") as f:
            if "WDInventoryFragment_Armor" in f.read():
                extra.append(os.path.relpath(p, DATA))
    check("G no armor fragment outside the 14 known files", not extra, str(extra))
    for iid, it in sorted(items.items()):
        j = mi.get(iid)
        if not j:
            continue
        r_set = set(it["stages"])
        ok = (it["tag"] == j["context_tag"] and set(it["covered"]) == set(j["covered_locations"]) and
              ((not r_set and j["durability_reduction_pct"] is None) or (len(r_set) == 1 and j["durability_reduction_pct"] == next(iter(r_set)))))
        check("G %s tag/coverage/R match JSON" % iid, ok, "raw tag %s R %s cover %s" % (it["tag"], sorted(r_set), it["covered"]))
    ghil = [i for i in items if "Ghillie" in i]
    check("G Ghillie items: no stages, no coverage in data", all(not items[i]["stages"] and not items[i]["covered"] for i in ghil), str(ghil))
    print("   Ghillie fragment property keys:", {i: items[i]["keys"] for i in ghil})
    # all four stages same R
    check("G every armored item has 4 stages of one R", all(len(it["stages"]) == 4 and len(set(it["stages"])) == 1 for i, it in items.items() if "Ghillie" not in i),
          str({i: it["stages"] for i, it in items.items() if "Ghillie" not in i and (len(it["stages"]) != 4 or len(set(it["stages"])) != 1)}))
    # a location covered by two items of the same kind? or by both vest and helmet
    kind = lambda i: "helmet" if "Helmet" in i else "vest"
    bad = []
    locs = meta["locations"]
    for loc in locs:
        cov = [i for i, it in items.items() if loc in it["covered"]]
        kinds = {kind(i) for i in cov}
        if len(kinds) > 1:
            bad.append((loc, cov))
    check("G no location covered by both a vest and a helmet", not bad, str(bad))
    print("   per location covering items:")
    for loc in locs:
        print("     %-13s %s" % (loc, [i for i, it in sorted(items.items()) if loc in it["covered"]]))
    # the doc table (item x location)
    ae = meta["armor_effect"]
    maxcmp = 0
    for loc in locs:
        cov_items = {it["tag"].split(".")[-1]: (i, it) for i, it in items.items() if loc in it["covered"] and it["stages"]}
        j = ae[loc]["covering"]
        ok = set(j) == set(cov_items) and all(j[c]["item"] == cov_items[c][0] and j[c]["reduction_pct"] == cov_items[c][1]["stages"][0] and
                                               abs(j[c]["fmj_multiplier"] - (1 - cov_items[c][1]["stages"][0] / 100)) < 1e-9 for c in j)
        check("G armor_effect %s rebuilt from raw" % loc, ok)
    # ---- recompute cells
    dpr = {it["tag"]: it["stages"][0] for it in items.values() if it["stages"]}
    A = ammo_tables()
    kinds = {loc: ae[loc]["kind"] for loc in locs}
    W = {w["id"]: w for w in jl["weapons"]}
    check("G JSON weapon count 33", len(W) == 33, str(len(W)))
    maxd = 0.0
    maxr = 0.0
    n = 0
    bad = 0
    store = {}
    for wid, w in W.items():
        wtag = weapon_tag(wid)
        for a in w["ammo"]:
            item_id = a["items"][0]
            if A["P"][A["ITEMS"][item_id]][2] != a["base_damage"]:
                bad += 1
                print("   base damage mismatch", wid, a["id"])
            for loc in locs:
                covering = {it["tag"].split(".")[-1]: it["tag"] for i, it in items.items()
                            if loc in it["covered"] and it["stages"]}
                classes = list(a["damage_raw"][loc].keys())
                # classes in JSON must equal None + my covering classes
                if set(classes) != {"None"} | set(covering):
                    bad += 1
                    print("   class set mismatch", wid, a["id"], loc, classes, sorted(covering))
                for cls in classes:
                    tag = None if cls == "None" else covering.get(cls)
                    mine = rule_damage(wtag, item_id, loc, tag, dpr)
                    theirs = a["damage_raw"][loc][cls]
                    d = abs(mine - theirs)
                    maxd = max(maxd, d)
                    n += 1
                    store[(wid, a["id"], loc, cls)] = (mine, theirs, a["damage"][loc][cls])
                    if d > 1e-6:
                        bad += 1
                        print("   cell mismatch", wid, a["id"], loc, cls, mine, theirs)
                    if abs(round(mine, 1) - a["damage"][loc][cls]) > 0.100001 and abs(round(mine, 1) - a["damage"][loc][cls]) > 1e-9:
                        bad += 1
                        print("   rounded mismatch", wid, a["id"], loc, cls, mine, a["damage"][loc][cls])
                    maxr = max(maxr, abs(round(mine + 1e-12, 1) - a["damage"][loc][cls]))
    RESULTS["G_cells"] = n
    RESULTS["G_max_diff"] = maxd
    check("G full sweep: %d cells (33 weapons, all ammo rows, 12 locations, covering classes) max abs diff %.2e, problems %d" % (n, maxd, bad), bad == 0 and maxd < 1e-6)
    # armored never above unarmored; non-covering classes equal unarmored by construction (class absent)
    worse = [k for k, v in store.items() if k[3] != "None" and v[0] > store[(k[0], k[1], k[2], "None")][0] + 1e-9]
    check("G no armored cell above its unarmored cell", not worse, str(worse[:3]))
    # named sample of non-torso cells
    SAMPLE = [("M4", "FMJ", "Neck", "Heavy"), ("M4", "FMJ", "Neck", "Tank"), ("M4", "FMJ", "Neck", "SuperHeavy"),
              ("M4", "FMJ", "Torso.Middle", "Heavy"), ("M4", "FMJ", "Torso.Middle", "Light"), ("M4", "FMJ", "Torso.Lower", "Medium"),
              ("M4", "FMJ", "Torso.Lower", "SuperHeavy"), ("M4", "FMJ", "Pelvis", "SuperHeavy"), ("M4", "FMJ", "Arm.Upper", "SuperHeavy"),
              ("M4", "ArmorPiercing", "Neck", "Heavy"), ("M4", "ArmorPiercing", "Neck", "SuperHeavy"), ("M4", "HollowPoint", "Torso.Middle", "SuperHeavy"),
              ("SR_04", "HollowPoint", "Neck", "SuperHeavy"), ("SR_04", "HollowPoint", "Neck", "Tank"), ("SR_04", "HollowPoint", "Neck", "Heavy"),
              ("SR_04", "ArmorPiercing", "Pelvis", "SuperHeavy"), ("Glock17", "FMJ", "Head", "Pilot"), ("Glock17", "FMJ", "Head", "Tank"),
              ("Glock17", "ArmorPiercing", "Torso.Lower", "Heavy"), ("WEPN_026", "HollowPoint", "Head", "Pilot"), ("WEPN_026", "FMJ", "Head", "Tank"),
              ("AK74M", "Tracer", "Arm.Upper", "SuperHeavy"), ("SVDM", "ArmorPiercing", "Torso.Middle", "Heavy"), ("M500", "Buckshot", "Neck", "Tank"),
              ("M500", "Slug", "Pelvis", "SuperHeavy"), ("WEPN_035", "FMJ", "Torso.Lower", "Light"), ("MK22", "HollowPoint", "Neck", "Heavy"),
              ("Judge", "FMJ", "Arm.Upper", "SuperHeavy"), ("SKS", "HollowPoint.Tracer", "Neck", "SuperHeavy"),
              ("M4", "FMJ", "Arm.Hand", "None"), ("M4", "FMJ", "Leg.Calf", "None"), ("M4", "FMJ", "Leg.Foot", "None"), ("M4", "FMJ", "Arm.Lower", "None"),
              ("WEPN_017", "ArmorPiercing", "Leg.Calf", "None"), ("Glock17", "FMJ", "Arm.Hand", "None")]
    sfail = 0
    print("   sample: weapon ammo location class: mine / json damage_raw / diff / rounded in json")
    for k in SAMPLE:
        mine, theirs, rnd = store[k]
        ok = abs(mine - theirs) <= 1e-6
        sfail += not ok
        print("   %s %-8s %-18s %-13s %-10s %9.4f %9.4f %.1e %6.1f" % ("PASS" if ok else "FAIL", *k, mine, theirs, abs(mine - theirs), rnd))
    check("G named sample of %d cells (non-torso locations, Pilot, Tank, SuperHeavy, hands/feet)" % len(SAMPLE), sfail == 0)
    # Ghillie effect on the rule engine (as a covering tag): R is absent, so factor 1 in the ammo-effectiveness entry
    gh = rule_damage(weapon_tag("M4"), "Id.Item.556mm", "Torso.Upper", "Meta.Damage.Armor.Ghillie", dpr)
    base = rule_damage(weapon_tag("M4"), "Id.Item.556mm", "Torso.Upper", None, dpr)
    check("G Ghillie as covering target gives unarmored damage in the infantry table (%.4f vs %.4f)" % (gh, base), abs(gh - base) < 1e-9)
    # where does Ghillie appear in damage tables
    hits = []
    for pth in glob.glob(os.path.join(DMG, "**/*.json"), recursive=True):
        txt = open(pth, encoding="utf-8").read()
        if "Ghillie" in txt:
            hits.append(os.path.relpath(pth, DMG))
    print("   damage data tables mentioning Ghillie:", hits)
    at = dmg_table("DT_GlobalDamage_ArmorData.json")
    ghe = []
    for row, r in at.items():
        for i, e in enumerate(r.get("DamageModificationEntries", [])):
            if any("Ghillie" in t for t in e["TargetRequirements"]):
                ghe.append((row, i, e["OutModification"]["Amount"]))
    print("   DT_GlobalDamage_ArmorData entries that require a Ghillie target tag:", ghe)
    check("G Ghillie tags appear in no infantry-table entry (only in the armor-entity table: %s)" % ghe,
          "Ghillie" not in json.dumps(dmg_table("DT_GlobalDamage_InfantryData.json")))
    gf = [i for i in items if "Ghillie" in i]
    print("   Ghillie fragments carry AppliedEffects:", {i: [x["ObjectPath"].split("/")[-1] for x in json.loads(json.dumps(next(o for o in exports(items[i]["path"].replace("\\", "/") and os.path.join(ROOT, items[i]["path"])) if o.get("Type") == "WDInventoryFragment_Armor")["Properties"]["AppliedEffects"]))] for i in gf})
    ge = glob.glob(os.path.join(DATA, "**/GE_Player_Ghilli*.json"), recursive=True)
    print("   GE_Player_Ghilli* assets present in data/:", len(ge))
    wd24 = {w["id"]: w for w in load_json("assets/data/weapon-damage.json")["weapons"]}
    mism = 0
    for wid, w in W.items():
        for a in w["ammo"]:
            b = next(x for x in wd24[wid]["ammo"] if x["id"] == a["id"])
            for cls in ("None", "Light", "Medium", "Heavy", "SuperHeavy"):
                if abs(a["damage_raw"]["Torso.Upper"][cls] - b["damage_raw"]["torso_armor"][cls]) > 1e-9 or abs(a["damage_raw"]["Head"][cls] - b["damage_raw"]["head_armor"][cls]) > 1e-9:
                    mism += 1
            for loc in ("Neck", "Torso.Middle", "Arm.Upper", "Leg.Thigh"):
                if abs(a["damage_raw"][loc]["None"] - b["damage_raw"]["location"][loc]) > 1e-9:
                    mism += 1
    check("G round 24 Torso.Upper, Head and four unarmored location cells reproduced for all rows", mism == 0, "%d mismatches" % mism)
    # numbers quoted in docs/evidence/round25-armor-coverage.md
    def v1(w, a, l, c):
        return round(store[(w, a, l, c)][0], 1)
    quoted = [("M4", "FMJ", "Neck", "None", 49.4), ("M4", "FMJ", "Neck", "Heavy", 24.7), ("M4", "FMJ", "Neck", "Tank", 22.2),
              ("M4", "FMJ", "Neck", "SuperHeavy", 19.7), ("M4", "FMJ", "Torso.Middle", "None", 27.2), ("M4", "FMJ", "Torso.Middle", "Light", 19.0),
              ("M4", "FMJ", "Torso.Middle", "Medium", 16.3), ("M4", "FMJ", "Torso.Middle", "Heavy", 13.6), ("M4", "FMJ", "Torso.Middle", "SuperHeavy", 10.9),
              ("M4", "FMJ", "Pelvis", "None", 25.2), ("M4", "FMJ", "Pelvis", "SuperHeavy", 10.1), ("M4", "FMJ", "Arm.Upper", "None", 15.1),
              ("M4", "FMJ", "Arm.Upper", "SuperHeavy", 6.0), ("SR_04", "HollowPoint", "Neck", "None", 486.1), ("SR_04", "HollowPoint", "Neck", "SuperHeavy", 7.0),
              ("SR_04", "HollowPoint", "Neck", "Tank", 15.3), ("SR_04", "HollowPoint", "Neck", "Heavy", 19.7), ("M4", "ArmorPiercing", "Neck", "None", 39.5),
              ("M4", "ArmorPiercing", "Neck", "Heavy", 27.6), ("M4", "ArmorPiercing", "Neck", "SuperHeavy", 25.3)]
    qbad = [(q, v1(*q[:4])) for q in quoted if abs(v1(*q[:4]) - q[4]) > 1e-9]
    check("G doc quoted values (%d) reproduce" % len(quoted), not qbad, str(qbad))
    top = sorted(((store[(w, a, "Neck", "None")][0] - min(v[0] for k, v in store.items() if k[:3] == (w, a, "Neck")), w, a)
                  for (w, a, l, c) in store if l == "Neck" and c == "None"), reverse=True)[:3]
    print("   largest absolute Neck drops (unarmored minus best armor):", [("%.2f" % t[0], t[1], t[2]) for t in top])
    check("G doc claim: largest absolute drop is SR_04 hollow point at the Neck (ties with HollowPoint.Tracer)",
          top[0][1] == "SR_04" and top[0][2].startswith("HollowPoint"))
    hb = load_json("assets/data/infantry-hitboxes.json")
    hbok = all([i + ".json" and i for i in items] is not None for _ in [0])
    mine_cov = [sorted(i for i, it in items.items() if loc in it["covered"]) for loc in locs]
    check("G infantry-hitboxes.json covered_by equals the coverage rebuilt from raw", [h["covered_by"] for h in hb["hit_locations"]] == mine_cov)
    check("G doc claim: 12 locations", len(locs) == 12)
    return W, items


# =============================================================== H, penetration
CFG_DIR = "E:/Reverse_Engineer/wardogs_analysis/round8_config_20261018/extracted/Wardogs/Config"


def paren_section(line, key):
    j = line.find(key + "=")
    if j < 0:
        return ""
    j += len(key) + 1
    depth = 0
    for e in range(j, len(line)):
        if line[e] == "(":
            depth += 1
        elif line[e] == ")":
            depth -= 1
            if depth == 0:
                return line[j:e + 1]
    return ""


def surf_key(x):
    return 0 if x == "Default" else int(x)


def run_penetration():
    print("== H penetration ==")
    pj = load_json("assets/data/weapon-penetration.json")
    cfg = pj["config"]
    ini = os.path.join(CFG_DIR, "DefaultGame.ini")
    eng = os.path.join(CFG_DIR, "DefaultEngine.ini")
    have_cfg = os.path.exists(ini) and os.path.exists(eng)
    print("   packed config extraction available (outside data/): %s" % have_cfg)
    if have_cfg:
        ini_text = open(ini, encoding="utf-8", errors="ignore").read()
        line = [l for l in ini_text.split("\n") if l.startswith("ProjectileSystemSettings=")][0]
        pat2 = r"\(SurfaceType_?(\w+), ([\d.\-]+)\)"
        P = {surf_key(a): float(b) for a, b in re.findall(pat2, paren_section(line, "PhysMatRicochetProbabilities"))}
        X = {surf_key(a): float(b) for a, b in re.findall(pat2, paren_section(line, "PenetrationPhysMatExitSpeedModifiers"))}
        R = {surf_key(a): (float(b), float(c)) for a, b, c in re.findall(
            r"\(SurfaceType_?(\w+), \(Min=([\d.\-]+),Max=([\d.\-]+)\)\)", paren_section(line, "PhysMatRicochetRestitutionCoefficient"))}
        names = {0: "Default"}
        for t, n in re.findall(r'^\+PhysicalSurfaces=\(Type=SurfaceType(\d+),Name="(\w+)"\)',
                               open(eng, encoding="utf-8", errors="ignore").read(), flags=re.M):
            names[int(t)] = n
        check("H (a) raw surface table has 63 ricochet and 63 exit-speed entries", len(P) == 63 and len(X) == 63, "%d %d" % (len(P), len(X)))
        zr = sorted(k for k, v in P.items() if v == 0)
        nzr = sum(1 for v in P.values() if v != 0)
        nzx = sum(1 for v in X.values() if v != 0)
        zx = sorted(k for k, v in X.items() if v == 0)
        print("   ricochet probability zero for SurfaceType:", zr, "nonzero count", nzr)
        print("   exit-speed modifier zero for SurfaceType:", zx, "nonzero count", nzx)
        check("H (a) ricochet probability nonzero for 57 of 63", nzr == 57, str(nzr))
        check("H (a) ricochet zero only for SurfaceType3 and 17 (doc: 'zero only for')", zr == [3, 17],
              "zero at %s: %s; 57 nonzero means 6 zeros, not 2" % (zr, [(k, names.get(k)) for k in zr]))
        check("H (a) exit-speed modifier nonzero for 36 of 63", nzx == 36, str(nzx))
        named = sorted(names)
        zero_named = [(k, names[k]) for k in named if X[k] == 0]
        print("   named surface types (incl Default):", len(named), "; named with s == 0:", zero_named)
        check("H (a) doc phrase 'every named type except Body and Head' has nonzero exit speed",
              all(X[k] != 0 for k in named if k not in (3, 17)), "named types with zero s besides 3 and 17: %s" % [z for z in zero_named if z[0] not in (3, 17)])
        check("H (a) types 39..62 have s = 0, P = 0.5, restitution 0.4-0.6", all(X[k] == 0 and P[k] == 0.5 and R[k] == (0.4, 0.6) for k in range(39, 63)))
        check("H (a) SurfaceType19 has no restitution entry", 19 not in R and len(R) == 62)
        js = {e["surface_type"]: e for e in cfg["surfaces"]}
        bad = []
        for k in range(0, 63):
            e = js.get(k)
            if e is None:
                bad.append(k)
                continue
            if abs(e["exit_speed_modifier"] - X[k]) > 1e-9 or abs(e["ricochet_probability"] - P[k]) > 1e-9:
                bad.append(("val", k))
            r = R.get(k)
            if (e["restitution"] is None) != (r is None) or (r and (abs(e["restitution"][0] - r[0]) > 1e-9 or abs(e["restitution"][1] - r[1]) > 1e-9)):
                bad.append(("rest", k))
            if 0 <= k <= 38 and e["name"] != names.get(k, e["name"]):
                bad.append(("name", k))
        check("H (a) JSON surfaces equal the raw 63-entry tables (values, restitution, names)", not bad and len(js) == 63, str(bad))
        ang = [(float(a), float(b), float(c)) for a, b, c in
               re.findall(r"\(\(X=([\d.]+),Y=([\d.]+)\), ([\d.]+)\)", paren_section(line, "ImpactAngleRicochetProbabilities"))]
        check("H (d) angle table: nine 10-degree bins 0.08..0.92 equals JSON",
              ang == [tuple(x) for x in cfg["impact_angle_ricochet_probabilities"]] and len(ang) == 9 and ang[0][2] == 0.08 and ang[-1][2] == 0.92,
              str([a[2] for a in ang]))
        pe = re.search(r"PenetrationEffectivenessRicochetProbabilities=\(X=([\d.]+),Y=([\d.]+)\)", line)
        check("H (d) PenetrationEffectivenessRicochetProbabilities = (2, 1)",
              (float(pe.group(1)), float(pe.group(2))) == (2.0, 1.0) and cfg["penetration_effectiveness_ricochet_range"] == [2.0, 1.0])
        for key, jk in (("MaxRicochetAngleVariance", "max_ricochet_angle_variance"), ("MaxPelletCount", "max_pellet_count"),
                        ("SimulationFrameRate", "simulation_frame_rate")):
            m = re.search(key + r"=([\d.]+)", line)
            check("H config %s equals JSON" % key, float(m.group(1)) == float(cfg[jk]), m.group(1))
        m = re.search(r"MaxConsecutiveFullRefundedSubsteps=(\d+)", line)
        print("   MaxConsecutiveFullRefundedSubsteps raw:", m and m.group(1))
        ignores = re.findall(r'"(/Game/[^"]+)"', paren_section(line, "PenetrationPhysMatIgnoreList"))
        check("H penetration ignore list length equals JSON (%d)" % len(ignores), len(ignores) == len(cfg["penetration_phys_mat_ignore_list"]))
        pst = re.search(r"PlanarSurfaceThicknessScale=([\d.]+)", ini_text)
        check("H PlanarSurfaceThicknessScale = 10", bool(pst) and float(pst.group(1)) == cfg["planar_surface_thickness_scale"] == 10.0, str(pst and pst.group(1)))
        print("   largest raw exit-speed modifier:", max((X[k], k) for k in X))
    else:
        print("UNDETERMINED H (a)/(d): packed config extraction not found at", CFG_DIR)

    # (b) ammo modifier assets
    am = {}
    for pth in glob.glob(os.path.join(DATA, "Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_*.json")):
        for o in exports(pth):
            if o.get("Type") == "WDAmmoModifierDataAsset":
                pr = o["Properties"]
                am[tg(pr["AmmoModifierTag"])] = {tg(x["Key"]).split(".")[-1]: x["Value"] for x in pr["AttributeModificationMultipliers"]}
    check("H (b) five DA_AmmoModifier_* assets", len(am) == 5, str(len(am)))
    exp = {"ArmorPiercing": (1.8, 0.0), "ArmorPiercing.Tracer": (1.76, 0.0), "HollowPoint": (0.1, 0.15),
           "HollowPoint.Tracer": (0.1, 0.15), "Tracer": (1.0, 0.075)}
    for k, (e, p) in exp.items():
        r = am.get("Meta.Damage.AmmoModifier." + k, {})
        print("   %-22s raw %s" % (k, r))
        check("H (b) %s E=%s exit-speed=%s" % (k, e, p), r.get("PenetrationEffectivenessMultiplier") == e and r.get("PenetrationExitSpeedMultiplier") == p)
    check("H (b) EffectiveRange x1.2 AP, x0.8 HP, x1.0 Tracer; TracerChance 1.0 on the Tracer variants",
          am["Meta.Damage.AmmoModifier.ArmorPiercing"]["EffectiveRangeMultiplier"] == 1.2
          and am["Meta.Damage.AmmoModifier.HollowPoint"]["EffectiveRangeMultiplier"] == 0.8
          and am["Meta.Damage.AmmoModifier.Tracer"]["EffectiveRangeMultiplier"] == 1.0
          and all(am["Meta.Damage.AmmoModifier." + k].get("TracerChance") == 1.0 for k in ("Tracer", "HollowPoint.Tracer", "ArmorPiercing.Tracer")))
    check("H (b) JSON ammo_modifiers equal raw", all(
        all(pj["ammo_modifiers"][t].get(f) == v.get(f) for f in ("PenetrationEffectivenessMultiplier", "PenetrationExitSpeedMultiplier", "EffectiveRangeMultiplier"))
        for t, v in am.items()))
    print("   note: AP.Tracer stores E 1.76, not AP 1.8 x Tracer 1.0 = 1.8; the doc table shows 1.76, as in the data")

    # (c) K for every weapon and ammo row
    projs = projectile_assets()
    byid = {tag: lst[0][1] for tag, lst in projs.items()}
    maxk = maxp = 0.0
    nrows = 0
    for w in pj["weapons"]:
        props = weapon_stats(w["id"])
        for a in w["ammo"]:
            ps = byid[a["projectile"]]
            dim = ps["ProjectileDimensions"]
            mod = am.get(a["modifier_tag"], {}) if a["modifier_tag"] else {}
            E = ps.get("PenetrationEffectivenessMultiplier", 1.0) * mod.get("PenetrationEffectivenessMultiplier", 1.0)
            pp = ps.get("PenetrationExitSpeedMultiplier", 0.0) * mod.get("PenetrationExitSpeedMultiplier", 1.0)
            K = props["InitialBulletSpeed"] * 0.01 * dim["Mass"] * E / (0.099999994 * dim["Diameter"] ** 2)
            nrows += 1
            maxk = max(maxk, abs(K - a["capacity_coefficient_k"]) / K)
            maxp = max(maxp, abs(pp - a["exit_speed_multiplier"]))
            if abs(E - a["penetration_effectiveness"]) > 1e-9:
                check("H %s %s E" % (w["id"], a["ammo"]), False, "%s vs %s" % (E, a["penetration_effectiveness"]))
    RESULTS["H_K_max_rel"] = maxk
    check("H (c) K and exit-speed multiplier recomputed for %d weapon x ammo rows (max relative K difference %.2e)" % (nrows, maxk), maxk < 1e-5 and maxp < 1e-9)
    K91 = 71500 * 0.01 * 0.0041 * 1.0 / (0.099999994 * 0.57 ** 2)
    print("   A91 FMJ K = %.4f (stated 90.2278); AP %.4f (162.41); AP.Tracer %.4f (158.801)" % (K91, K91 * 1.8, K91 * 1.76))
    check("H (c) A91 FMJ K = 90.2278", abs(K91 - 90.2278) < 5e-4)

    # (d) min impact angle and projectile flags across all projectile assets
    vals = {}
    flags = {"nopen": [], "force": []}
    for pth in glob.glob(os.path.join(DATA, "Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json"), recursive=True):
        for o in exports(pth):
            ps = (o.get("Properties") or {}).get("ProjectileStats")
            if ps:
                vals[o["Name"]] = ps.get("MinImpactAngleForRicochet")
                if ps.get("bShouldPenetrate") is False:
                    flags["nopen"].append(o["Name"])
                if ps.get("bForcePenetrateThinSurfaces"):
                    flags["force"].append(o["Name"])
    nonnull = {k: v for k, v in vals.items() if v is not None}
    print("   MinImpactAngleForRicochet set on:", nonnull)
    print("   bShouldPenetrate false:", flags["nopen"])
    print("   bForcePenetrateThinSurfaces true:", flags["force"])
    check("H (d) 155 mm assets carry MinImpactAngleForRicochet 91", any("155" in k for k in nonnull) and all(v == 91.0 for k, v in nonnull.items() if "155" in k))
    n155 = sum(1 for k in nonnull if "155" not in k)
    check("H (d) doc says 91 on the 155 mm assets; raw also sets it on %d other assets, values %s" % (n155, sorted(set(nonnull.values()))), n155 == 0)
    check("H (d) every stored min angle on the 155 mm assets is above 90 (never ricochets)", all(v > 90 for k, v in nonnull.items() if "155" in k))
    print("   min angle at or below 90 (so ricochet is possible) on:", {k: v for k, v in nonnull.items() if v <= 90})
    doc_np = {"70", "72", "84", "93", "120", "122", "125", "155"}
    extra_np = [k for k in flags["nopen"] if not any(("DA_%smm" % n in k or "DA_%sx" % n in k or "DA_%s_mm" % n in k) for n in doc_np)]
    print("   bShouldPenetrate=false assets beyond the doc list (70, 72, 84, 93, 120, 122, 125, 155 mm):", extra_np)
    arrow = [o for pth in glob.glob(os.path.join(DATA, "Plugins/GameFeatures/Items/CombatBow/**/DA_Arrow_Combat_ProjectileData.json"), recursive=True) for o in exports(pth)]
    ap = next(o for o in arrow if (o.get("Properties") or {}).get("ProjectileStats"))["Properties"]["ProjectileStats"]
    check("H doc claim: arrow exit-speed 0.55 (p + s max 1.55 on BulletProofGlass, factor floor 0.225) and E 0.5",
          ap.get("PenetrationExitSpeedMultiplier") == 0.55 and ap.get("PenetrationEffectivenessMultiplier") == 0.5 and abs((1 - 0.5 * (0.55 + 1.0)) - 0.225) < 1e-12,
          "arrow min ricochet angle %s" % ap.get("MinImpactAngleForRicochet"))
    print("   the 10-degree default for assets that omit the field is a native constructor value, not in data (not verifiable here)")

    # reference block and worked examples
    def after(v0, f, p, s):
        return v0 * (1 - f) * max(0.0, min(1.0, 1 - 0.5 * (p + s)))
    chk = []
    for r in pj["reference"]:
        w = next(x for x in pj["weapons"] if x["id"] == r["weapon"])
        a = next(x for x in w["ammo"] if x["ammo"] == r["ammo"])
        for sr in r["surfaces"]:
            sf = max(0.0, min(1.0, 1 - 0.5 * (a["exit_speed_multiplier"] + sr["exit_speed_modifier"])))
            chk.append(abs(sf - sr["surface_factor"]))
            for fk, fv in sr["next_impact_damage_fraction"].items():
                mine = min(1.0, after(r["launch_speed"], float(fk), a["exit_speed_multiplier"], sr["exit_speed_modifier"]) / r["speed_scale_reference"])
                chk.append(abs(mine - fv))
    RESULTS["H_reference_max_diff"] = max(chk)
    check("H reference block: %d surface factors and next-impact fractions, max abs diff %.2e" % (len(chk), max(chk)), max(chk) < 1e-5)
    K, Kap = 90.2278, 162.41
    ex = [("FMJ speed after, X=45", after(71500, 45 / K, 0.18, 0.4), 25447), ("AP speed after, X=45", after(71500, 45 / Kap, 0.0, 0.4), 41351),
          ("FMJ struggling speed, X=70", after(71500, 70 / K, 0.18, 0.4), 11366)]
    for n, mine, claim in ex:
        print("   doc example %-28s mine %.0f doc %d (diff %.0f)" % (n, mine, claim, mine - claim))
    check("H doc worked-example speeds within 20 cm/s of the doc (rounding of f)", all(abs(m - c) < 20 for _, m, c in ex))
    print("   next-impact fraction X=45 FMJ %.3f (doc 0.630); X=70 FMJ %.3f (doc 0.281); X=70 AP %.3f (doc 0.806)" %
          (after(71500, 45 / K, .18, .4) / 40400, after(71500, 70 / K, .18, .4) / 40400, after(71500, 70 / Kap, 0, .4) / 40400))
    eff = K / 70
    t = max(0.0, min(1.0, (eff - 2) / (1 - 2)))
    print("   ricochet chance X=70, 35 deg, Concrete: eff %.3f t %.3f chance %.4f (doc 0.104)" % (eff, t, 0.35 * 0.42 * t))

    # other data claims in the evidence doc
    n_over = nulls = 0
    names_c = {}
    for root, _, fs in os.walk(DATA):
        for fn in fs:
            if not fn.endswith(".json"):
                continue
            txt = open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()
            if "PhysicalMaterialOverride" not in txt:
                continue
            n_over += 1
            for m in re.finditer(r'"PhysicalMaterialOverride":\s*(null|\{[^}]*\})', txt):
                if m.group(1) == "null":
                    nulls += 1
                else:
                    nm = re.search(r"(PM_\w+)", m.group(1)).group(1)
                    names_c[nm] = names_c.get(nm, 0) + 1
    check("H doc claim: 156 files with PhysicalMaterialOverride, 9076 null, 125 named (Metal 90, Concrete 24, Plaster 9, Brick 1, Glass 1)",
          (n_over, nulls) == (156, 9076) and names_c == {"PM_Metal": 90, "PM_Concrete": 24, "PM_Plaster": 9, "PM_Brick": 1, "PM_Glass": 1}, str((n_over, nulls, names_c)))
    ents = dmg_table("DT_GlobalDamage_InfantryData.json")["Meta.Damage.Infantry"]["DamageModificationEntries"]
    hits = [i for i, e in enumerate(ents) if "Kinetic.Impact.Ricochet" in json.dumps(e) or "Kinetic.Impact.Penetration" in json.dumps(e)]
    check("H doc claim: 0 of 146 infantry entries key on Kinetic.Impact.Ricochet/.Penetration", len(ents) == 146 and not hits, "%d entries, %d matching" % (len(ents), len(hits)))
    pm = glob.glob(os.path.join(DATA, "**/PM_*.json"), recursive=True)
    print("   PM_*.json files in data/:", [os.path.basename(x) for x in pm])
    jp = pj["projectiles"]
    bad = []
    for tag, e in jp.items():
        cands = projs.get(tag)
        if not cands:
            bad.append(tag)
            continue
        ps = cands[0][1]
        if (ps.get("MinImpactAngleForRicochet") != e["min_impact_angle_for_ricochet_deg"] or ps.get("bShouldPenetrate") != e["bShouldPenetrate"]
                or ps.get("bForcePenetrateThinSurfaces") != e["bForcePenetrateThinSurfaces"]
                or abs(ps["ProjectileDimensions"]["Diameter"] - e["diameter"]) > 1e-9 or abs(ps["ProjectileDimensions"]["Mass"] - e["mass"]) > 1e-9):
            bad.append(tag)
    check("H JSON projectiles (%d) equal raw dimensions and flags" % len(jp), not bad, str(bad))


def main():
    sel = sys.argv[1] if len(sys.argv) > 1 else "all"
    if sel in ("all", "falloff"):
        run_falloff()
    if sel in ("all", "locations"):
        run_locations()
    if sel in ("all", "penetration"):
        run_penetration()
    print("\nsummary", {k: (("%.3g" % v) if isinstance(v, float) else v) for k, v in RESULTS.items()})
    print("RESULT:", "PASS" if not FAILS else "FAIL (%d): %s" % (len(FAILS), "; ".join(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
