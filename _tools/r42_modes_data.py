"""Build assets/data/r42-modes.json: round-42 findings read from cooked data and config.

    python -I _tools/r42_modes_data.py [--check] [<round42_modes scratch dir>]

Reads, under the scratch directory (default E:/Reverse_Engineer/wardogs_analysis/round42_modes):
  sv/*.json   WdExtract dump of the 61 packages whose name map holds WDSpawnVolume
  ex/GC_Vehicle_Destroyed.json, ex/BP_Explosions.json   explosion-sequence mapping
  k/ABP_*.json   Kawaii physics nodes of the ghillie and bobblehead animation blueprints
and, from this repository, the water height grids and flux states, the caliber projectile assets (arm class)
and the alert-state threshold asset. Static findings (RVAs, rules, defaults) are fixed constants taken from the
decompiled corpus and are written verbatim. Idempotent; --check exits 1 on difference. Exits 0 with a message
if the scratch input is absent.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "r42-modes.json")
DATA = os.path.join(ROOT, "data", "Wardogs")
CFG = "E:/Reverse_Engineer/wardogs_analysis/round39_modes/cfgc/raw/Wardogs/Config"


def props(path):
    t = open(path, encoding="utf-8").read()
    d = json.loads(t[t.index("{"):])
    return d.get("Properties", d)


def r1(x):
    return None if x is None else round(x, 1)


# ---- spawn volumes -------------------------------------------------------------------------
_cache = {}


def _pkg(sv, path):
    b = path.rsplit("/", 1)[1]
    if b not in _cache:
        fn = os.path.join(sv, b + ".json")
        _cache[b] = json.load(open(fn, encoding="utf-8")) if os.path.exists(fn) else None
    return _cache[b]


def _res(sv, ref):
    if not ref or not ref.get("ObjectPath"):
        return None
    pth, n = ref["ObjectPath"].rsplit(".", 1)
    try:
        return _pkg(sv, pth)[int(n)]
    except Exception:
        return None


def _loc(sv, ref):
    c = _res(sv, ref)
    v = c.get("Properties", {}).get("RelativeLocation") if c else None
    return None if v is None else [r1(v["X"]), r1(v["Y"]), r1(v["Z"])]


def spawn_volumes(scratch):
    sv = os.path.join(scratch, "sv")
    rows = []
    for f in sorted(glob.glob(os.path.join(sv, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        world = next((e["Name"] for e in d if e["Type"] == "World"), "")
        for e in d:
            if e.get("Type") != "WDSpawnVolume":
                continue
            p = e["Properties"]
            rows.append({
                "world": world,
                "package": os.path.basename(f)[:-5],
                "actor": e["Name"],
                "faction": ((p.get("FactionTag") or {}).get("TagName") or "").split(".")[-1] or None,
                "allowed_vehicles": [a.replace("Vehicle.Variant.", "") for a in p.get("AllowedObjectsToSpawn", [])],
                "disallowed_count": len(p.get("DisallowedObjectsToSpawn", [])),
                "max_spawn_points": p.get("MaxSpawnPoints"),
                "horizontal_spacing": p.get("HorizontalSpacing"),
                "vertical_spacing": p.get("VerticalSpacing"),
                "spawn_point_offset_z": p.get("SpawnPointOffsetZ"),
                "location": _loc(sv, p.get("RootComponent")),
                "target_points": [_loc(sv, t) for t in p.get("TargetPoints", [])],
            })
    rows.sort(key=lambda r: (r["world"], r["faction"] or "", r["actor"]))
    cnt = collections.Counter()
    for r in rows:
        cnt["%s|%s|%s" % (r["world"], r["faction"], "vehicle" if r["allowed_vehicles"] else "no_vehicle_list")] += 1
    return {"count": len(rows), "by_world_faction_kind": dict(sorted(cnt.items())), "volumes": rows}


# ---- explosion sequences -------------------------------------------------------------------
def explosion_map(scratch):
    out = {"vehicle_destroyed": {}, "caliber": {}, "other_cues": {
        "GameplayCue.IED.Explode": "DA_IEDExplosionSequence",
        "GameplayCue.FOB.DamageStateChanged": "DA_FOBDestroyed_ExplosionSequence"}}
    d = json.load(open(os.path.join(scratch, "ex", "GC_Vehicle_Destroyed.json"), encoding="utf-8"))
    for e in d:
        for it in e.get("Properties", {}).get("TagsToExplosionSequence", []):
            v = it["Value"]["ObjectName"].split("'")[-2] if it.get("Value") else None
            out["vehicle_destroyed"][it["Key"]["TagName"].split(".")[-1]] = v
    d = json.load(open(os.path.join(scratch, "ex", "BP_Explosions.json"), encoding="utf-8"))
    for e in d:
        for it in e.get("Properties", {}).get("TagToExplosionSequence", []):
            v = it["Value"]["ObjectName"].split("'")[-2] if it.get("Value") else None
            out["caliber"][it["Key"]["TagName"]] = v
    out["vehicle_destroyed"] = dict(sorted(out["vehicle_destroyed"].items()))
    return out


# ---- Kawaii physics ------------------------------------------------------------------------
def kawaii(scratch):
    rows = []
    for f in sorted(glob.glob(os.path.join(scratch, "k", "ABP_*.json"))):
        for e in json.load(open(f, encoding="utf-8")):
            for k, v in e.get("Properties", {}).items():
                if "Kawaii" in k and isinstance(v, dict) and "PhysicsSettings" in v:
                    ps = v["PhysicsSettings"]
                    rows.append({
                        "blueprint": os.path.basename(f)[:-5], "node": k,
                        "root_bone": v["RootBone"]["BoneName"],
                        "extra_root_chains": len(v.get("AdditionalRootBones", [])),
                        "excluded_bones": len(v.get("ExcludeBones", [])),
                        "damping": ps["Damping"], "stiffness": ps["Stiffness"],
                        "world_damping_location": ps["WorldDampingLocation"],
                        "world_damping_rotation": ps["WorldDampingRotation"],
                        "radius": ps["Radius"], "limit_angle": ps["LimitAngle"],
                        "forward_axis": v["BoneForwardAxis"].split("::")[-1],
                        "simulation_space": v["SimulationSpace"].split("::")[-1],
                        "target_framerate": v["TargetFramerate"],
                        "teleport_distance": v["TeleportDistanceThreshold"],
                        "teleport_rotation": v["TeleportRotationThreshold"],
                    })
    return rows


# ---- water grids and flux states -----------------------------------------------------------
def water():
    root = os.path.join(DATA, "Content", "Environment", "Water", "FluidFlux")
    rows, delta = [], collections.Counter()
    for f in sorted(glob.glob(os.path.join(root, "**", "WHG_*.json"), recursive=True)):
        g = props(f)
        h = g.get("Heights", [])
        sp = g["_aaabflcohlopnaadhglfk"]["AssetPathName"].split("/Game/")[1].split(".")[0]
        sf = os.path.join(DATA, "Content", sp + ".json")
        s = props(sf) if os.path.exists(sf) else {}
        a, b = g["_aaaajahedjfgkemenmnfj"], g["_aaaajbpajedfcbkcoihjn"]
        delta[s.get("IterationDeltaTime")] += 1
        wm, ws, loc, sz = g["worldmin"], g["WorldSize"], s.get("AreaLocation"), s.get("AreaSize")
        c = collections.Counter(h)
        rows.append({
            "grid": os.path.basename(f)[4:-5], "state": os.path.basename(sf)[:-5],
            "grid_wh": [g["GridWidth"], g["GridHeight"]], "world_size": [ws["X"], ws["Y"]],
            "cell_cm": [ws["X"] / g["GridWidth"], ws["Y"] / g["GridHeight"]],
            "double_58": r1(a), "double_60": r1(b), "range": r1(b - a),
            "samples_65535": c[65535], "samples": len(h),
            "worldmin_equals_area_minus_half": bool(loc and abs(wm["X"] - (loc["X"] - sz["X"] / 2)) < 1 and abs(wm["Y"] - (loc["Y"] - sz["Y"] / 2)) < 1),
            "double_60_below_area_z": bool(loc and b < loc["Z"]),
            "capture_offset": r1(s.get("CaptureOffset")), "iteration": s.get("Iteration"),
            "resolution": [s["Resolution"]["X"], s["Resolution"]["Y"]] if s.get("Resolution") else None,
        })
    return {"grids": len(rows), "iteration_delta_time_values": {str(k): v for k, v in delta.items()}, "rows": rows}


# ---- arm class of calibers -----------------------------------------------------------------
def arm_class():
    out = {}
    for f in glob.glob(os.path.join(DATA, "**", "DA_*ProjectileData.json"), recursive=True):
        t = open(f, encoding="utf-8").read()
        tags = sorted(set(re.findall(r"Meta\.Damage\.Arms\.[A-Za-z]+", t)))
        if tags:
            out[os.path.basename(f)[:-5]] = [x.split(".")[-1] for x in tags]
    return dict(sorted(out.items()))


def streaming():
    out = {}
    p = os.path.join(CFG, "DefaultScalability.ini")
    if os.path.exists(p):
        sec = None
        for line in open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line.startswith("["):
                sec = line.strip("[]")
            elif line.startswith("r.Streaming.PoolSize") and sec and sec.startswith("TextureQuality"):
                out[sec] = int(line.split("=")[1].split(";")[0].strip())
    return {"texture_pool_mb_by_scalability": out,
            "device_profile_note": "r.Streaming.PoolSize 1280 and r.Nanite.Streaming.StreamingPoolSize 256 or 512 only in console device profiles",
            "default_engine": {"r.MeshStreaming": True, "r.Nanite.Streaming.StreamingPoolSize": 256,
                               "r.Nanite.Streaming.NumInitialRootPages": 4096}}


STATIC = {
    "alert_state_update": {
        "function": "UWDAIAlertStateComponent_VFT slot 131 = 0x887C140 (tick); state setter 0x887C000",
        "rule": "level = max(highest detection level among this AI's own perceived targets, highest level among the AIs returned by 0x8870590 for the target); walk the threshold list in file order (Relaxed, Alert, Combat); a candidate passes if level >= LowerThreshold and, when its sight flag applies, the sight strength stored for the current target is above 0.0001; the walk stops at the first failure; the state is the last passing entry (Relaxed when none pass).",
        "sight_flag_choice": "bRequireSightToTransitionFromHigher is used when the current state is at or above the candidate, bRequireSightToTransitionFromLower otherwise",
        "thresholds_asset": "AlertStateThreashold_DataConfig: Relaxed 0.0, Alert 0.8, Combat 1.0 (sight required only to rise into Combat)",
    },
    "is_firing_test": {
        "field": "UWDWeaponComponent byte at +0xFE1",
        "reader": "0x6B96BF0 (returns the byte); IsCurrentlyFiring BP getter 0x6B99300; variant 0x6B96C00 / 0x6B99320 also needs the byte at +0xFEC above 0",
        "writers": "slot 175 (0x6B980A0) sets the word at +0xFE1 to 0x0101; slot 176 (0x6B98560) and the tail of 0x6B980A0 clear it",
        "target_weapon_lookup": "AI reads it from the target character's weapon component via the character's component getter (vtable +1848)",
    },
    "vehicle_noise_defaults": {
        "class": "UBHBaseVehicleConfigDataAsset, constructor 0x5300B10",
        "AIEngineLoudnessMaxRange_cm": 10000.0, "AIHornLoudnessMaxRange_cm": 50000.0,
        "AIVehicleDestroyedLoudnessMaxRange_cm": 80000.0,
        "overrides_in_cooked_data": 0,
    },
    "significance_rules": {
        "sphere_0x50D30B0": "per object, squared distance d2 to the nearest viewer; level = highest index i whose squared threshold is at or below d2 (0 when none; also 0 when d2 <= LowestNonZeroSignificanceDistance squared); the object keeps the lower of its stored level and the new one",
        "fov_0x50D2CE0": "per object and viewer: unit direction to the object; dot with the viewer facing; d2 as above; level 0 when dot >= HighestConeCosAngle and d2 <= FurthestDistanceSquared; otherwise the first setting index 1.. whose cone cosine <= dot and squared distance >= d2 (only if dot > LowestConeCosAngle and d2 <= FurthestDistanceSquared); keeps the lower of stored and new",
        "combination": "every evaluator only lowers the stored level, so the result is the minimum over evaluators and viewers; level 0 is the nearest or most central band",
        "setup": "0x50D2FC0 (FOV) and 0x50D32E0 (Sphere) square the distances and cache the min and max cone cosine",
    },
}


def build(scratch):
    thr = props(os.path.join(DATA, "Plugins", "GameFeatures", "AI", "WDAIPvEAICore", "Content", "DataAssets", "AlertStateThreashold_DataConfig.json"))
    return {
        "note": "round 42 (RE42-MODES). Static entries are RVAs of WardogsClient-Win64-Shipping.restored.exe; data entries are read from cooked packages.",
        "static": STATIC,
        "alert_thresholds": thr["AlertStatesWithThreashold"],
        "spawn_volumes": spawn_volumes(scratch),
        "explosion_sequences": explosion_map(scratch),
        "kawaii_physics": kawaii(scratch),
        "water": water(),
        "arm_class_by_projectile": arm_class(),
        "streaming": streaming(),
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    scratch = args[0] if args else "E:/Reverse_Engineer/wardogs_analysis/round42_modes"
    if not os.path.isdir(os.path.join(scratch, "sv")):
        print("scratch input absent:", scratch)
        return 0
    text = json.dumps(build(scratch), indent=1) + "\n"
    if check:
        old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        print("same" if old == text else "DIFFERENT")
        return 0 if old == text else 1
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", OUT, len(text), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
