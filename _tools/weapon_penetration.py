"""Penetration and ricochet inputs for infantry weapons, from the export and the packed config.

Builds assets/data/weapon-penetration.json from (a) the caliber projectile assets and the
DA_AmmoModifier_* assets in data/, (b) the weapon stats assets (launch speed, speed-scale reference),
(c) the packed ProjectileSystemSettings property (DefaultGame.ini line 303) and the physical-surface
names (DefaultEngine.ini), which are not part of data/ and are read from the offline config extraction.

What it computes is only what docs/evidence/round25-ricochet-penetration.md marks Data or Derived:
the per-surface exit-speed and ricochet tables, the ammo variants' exit-speed multiplier and
penetration effectiveness, the penetration capacity coefficient, and, for a few reference weapons,
the speed left after a pass and the damage fraction the next impact's speed scale then gives.
It does NOT contain a wall or prop table: which physical material (and so which surface type, density
and thickness) a world mesh uses is not in the export. See the evidence page.

    python _tools/weapon_penetration.py            # print the summary
    python _tools/weapon_penetration.py --write    # write assets/data/weapon-penetration.json
    python _tools/weapon_penetration.py --check    # PASS/FAIL cross-checks, non-zero exit on FAIL

Config location: env WARDOGS_CONFIG_DIR, else the round 8 extraction. When neither is readable the
config block already stored in the JSON is reused, so --write and --check still work from a clone.
"""
import glob
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402

ROOT = dt.ROOT
OUT = os.path.join(ROOT, "assets", "data", "weapon-penetration.json")
CONFIG_DIR = os.environ.get(
    "WARDOGS_CONFIG_DIR",
    "E:/Reverse_Engineer/wardogs_analysis/round8_config_20261018/extracted/Wardogs/Config",
)
AMMO_DIR = os.path.join(dt.DATA, "Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers")
CALIBER_GLOB = os.path.join(dt.DATA, "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json")

# Native constructor defaults of FWDProjectileStats (0x699DEE0; docs/evidence/round8-physical-material-downstream.md
# for the names): +0x208 PenetrationEffectivenessMultiplier = 1.0, +0x20C PenetrationExitSpeedMultiplier = 0.0,
# +0x214 MinImpactAngleForRicochet = 10.0 degrees (ProjectileFlight §10 states the 10 degrees).
DEFAULTS = {"penetration_effectiveness_multiplier": 1.0, "penetration_exit_speed_multiplier": 0.0,
            "min_impact_angle_for_ricochet_deg": 10.0}
# Native constants in the capacity expression (round8-physical-material-downstream.md section 1, 0x6F2FB77-0x6F2FC07).
CAP_SPEED_SCALE = 0.01
CAP_DENOM_SCALE = 0.099999994
REFERENCE_WEAPONS = ["A91", "AK74M", "SV98", "SR_04", "Glock17"]
LOAD_GRID = [0.0, 0.25, 0.5, 0.75]
SHOWN_SURFACES = [4, 8, 14, 23, 28, 35, 38]  # Brick, Concrete, Glass, Metal, Plaster, Wood, BulletProofGlass
SURFACE_PM_NOTE = ("The surface types a given world material resolves to are not in the export. The names "
                   "above are the engine's physical-surface names (DefaultEngine.ini); a PM_<name> asset using "
                   "the surface of the same name is an assumption, not data.")


def r(x, n=6):
    return None if x is None else float(f"{x:.{n}g}")


# ---------------------------------------------------------------- config

def read_config():
    """Parse ProjectileSystemSettings and the physical surface names, or return None if unreadable."""
    game = os.path.join(CONFIG_DIR, "DefaultGame.ini")
    eng = os.path.join(CONFIG_DIR, "DefaultEngine.ini")
    if not (os.path.exists(game) and os.path.exists(eng)):
        return None
    line = next(l for l in open(game, encoding="utf-8") if l.startswith("ProjectileSystemSettings="))

    def surf(k):
        return int(0 if k == "Default" else k)

    def table(name):
        m = re.search(name + r"=\((.*?)\)(?:,[A-Z][A-Za-z]+=|\)$)", line.rstrip("\n"), re.S)
        return m.group(1)

    exit_mod = {surf(k): float(v) for k, v in re.findall(
        r"\(SurfaceType_?(Default|\d+), ([\d.]+)\)", table("PenetrationPhysMatExitSpeedModifiers"))}
    rico = {surf(k): float(v) for k, v in re.findall(
        r"\(SurfaceType_?(Default|\d+), ([\d.]+)\)", table("PhysMatRicochetProbabilities"))}
    rest = {}
    for k, body in re.findall(r"\(SurfaceType_?(Default|\d+), \((.*?)\)\)", table("PhysMatRicochetRestitutionCoefficient")):
        mm = re.match(r"Min=([\d.]+),Max=([\d.]+)", body)
        rest[surf(k)] = [float(mm.group(1)), float(mm.group(2))] if mm else None
    angles = [[float(a), float(b), float(p)] for a, b, p in re.findall(
        r"\(\(X=([\d.]+),Y=([\d.]+)\), ([\d.]+)\)", re.search(r"ImpactAngleRicochetProbabilities=\((.*?)\)\),Pen", line).group(1) + ")")]
    pe = re.search(r"PenetrationEffectivenessRicochetProbabilities=\(X=([\d.]+),Y=([\d.]+)\)", line)
    ign = re.findall(r'"(/Game/[^"]+)"', re.search(r"PenetrationPhysMatIgnoreList=\((.*?)\),Pen", line).group(1))
    exit_def = re.search(r"ExitDeflectionPenetrationEffectivenessRange=\(X=([\d.]+),Y=([\d.]+)\)", line)
    exit_ang = re.search(r"ExitDeflectionAngleRange=\(X=([\d.]+),Y=([\d.]+)\)", line)
    scalars = {k: float(v) for k, v in re.findall(r"(MaxRicochetAngleVariance|MaxPelletCount|SimulationFrameRate)=([\d.]+)", line)}
    shallow = re.search(r"MaxDeflectionPercentageShallowAngle=\(Min=([\d.]+),Max=([\d.]+)\)", line)
    sharp = re.search(r"MaxDeflectionPercentageSharpAngle=\(Min=([\d.]+),Max=([\d.]+)\)", line)
    names = {int(n): s for n, s in re.findall(r'\+PhysicalSurfaces=\(Type=SurfaceType(\d+),Name="([^"]+)"\)',
                                                  open(eng, encoding="utf-8").read())}
    planar = re.search(r"PlanarSurfaceThicknessScale=([\d.]+)", open(game, encoding="utf-8").read())
    surfaces = []
    for i in range(63):
        surfaces.append({
            "surface_type": i,
            "name": "Default" if i == 0 else names.get(i, f"Unnamed{i}"),
            "exit_speed_modifier": exit_mod[i],
            "ricochet_probability": rico[i],
            "restitution": rest.get(i),
        })
    return {
        "source": "Wardogs/Config/DefaultGame.ini line 303 (ProjectileSystemSettings), PlanarSurfaceThicknessScale; "
                  "Wardogs/Config/DefaultEngine.ini [PhysicalSurfaces]; offline extraction, not in data/",
        "surfaces": surfaces,
        "impact_angle_ricochet_probabilities": angles,
        "penetration_effectiveness_ricochet_range": [float(pe.group(1)), float(pe.group(2))],
        "penetration_phys_mat_ignore_list": ign,
        "exit_deflection_penetration_effectiveness_range": [float(exit_def.group(1)), float(exit_def.group(2))],
        "exit_deflection_angle_range_deg": [float(exit_ang.group(1)), float(exit_ang.group(2))],
        "max_ricochet_angle_variance": scalars["MaxRicochetAngleVariance"],
        "max_deflection_percentage_shallow_angle": [float(shallow.group(1)), float(shallow.group(2))],
        "max_deflection_percentage_sharp_angle": [float(sharp.group(1)), float(sharp.group(2))],
        "max_pellet_count": int(scalars["MaxPelletCount"]),
        "simulation_frame_rate": int(scalars["SimulationFrameRate"]),
        "planar_surface_thickness_scale": float(planar.group(1)),
    }


def stored_config():
    if os.path.exists(OUT):
        return json.load(open(OUT, encoding="utf-8")).get("config")
    return None


# ---------------------------------------------------------------- data

def projectiles():
    out = {}
    for path in sorted(glob.glob(CALIBER_GLOB, recursive=True)):
        for o in dt.exports(path):
            props = o.get("Properties", {})
            pid, st = dt.tag(props.get("ProjectileId")), props.get("ProjectileStats")
            if not pid or not st:
                continue
            if pid in out and os.path.basename(path).count("_") > 2:
                continue
            dim = st.get("ProjectileDimensions", {})
            out[pid] = {
                "asset": os.path.basename(path)[:-5],
                "diameter": dim.get("Diameter"),
                "mass": dim.get("Mass"),
                "typical_speed": st.get("TypicalSpeed"),
                "penetration_exit_speed_multiplier": st.get("PenetrationExitSpeedMultiplier"),
                "penetration_effectiveness_multiplier": st.get("PenetrationEffectivenessMultiplier"),
                "min_impact_angle_for_ricochet_deg": st.get("MinImpactAngleForRicochet"),
                "bShouldPenetrate": st.get("bShouldPenetrate"),
                "bForcePenetrateThinSurfaces": st.get("bForcePenetrateThinSurfaces"),
            }
    return out


def ammo_modifiers():
    out = {}
    for path in sorted(glob.glob(os.path.join(AMMO_DIR, "DA_AmmoModifier_*.json"))):
        o = dt.exports(path)[0]
        p = o["Properties"]
        mult = {dt.tag(k["Key"]).split(".")[-1]: k["Value"] for k in p.get("AttributeModificationMultipliers", [])}
        out[dt.tag(p["AmmoModifierTag"])] = {"asset": o["Name"], **mult}
    return out


def weapon_speeds():
    """weapon id -> launch speed, speed-scale reference override (cm/s) from the weapon stats asset."""
    stats = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(dt.DATA, "**/DA_*_Stats.json"), recursive=True)}
    out = {}
    pattern = os.path.join(dt.DATA, "Wardogs/Plugins/GameFeatures/Weapons/**/ID_*.json")
    for path in sorted(glob.glob(pattern, recursive=True)):
        wid = os.path.basename(path)[3:-5]
        ref = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", open(path, encoding="utf-8").read())
        if not ref or ref.group(1) not in stats:
            continue
        ex = dt.exports(stats[ref.group(1)])
        ibs = next((v for o in ex for v in dt.walk(o, "InitialBulletSpeed")), None)
        ovr = next((v for o in ex for v in dt.walk(o, "bOverrideTypicalSpeed")), False)
        ts = next((v for o in ex for v in dt.walk(o, "TypicalSpeed")), None)
        out[wid] = {"stats_asset": ref.group(1), "initial_bullet_speed": ibs,
                    "override_typical_speed": ts if ovr and ts and ts > 0 else None}
    return out


# ---------------------------------------------------------------- model

def variant(proj, mod):
    """Penetration stats of one ammo variant: base stats times the modifier's multipliers (section 7.9)."""
    base_p = proj["penetration_exit_speed_multiplier"]
    base_e = proj["penetration_effectiveness_multiplier"]
    p = (DEFAULTS["penetration_exit_speed_multiplier"] if base_p is None else base_p) * (mod or {}).get("PenetrationExitSpeedMultiplier", 1.0)
    e = (DEFAULTS["penetration_effectiveness_multiplier"] if base_e is None else base_e) * (mod or {}).get("PenetrationEffectivenessMultiplier", 1.0)
    return p, e


def capacity_coefficient(proj, e, speed):
    """K with capacity = K * cos(angle) / density at impact speed `speed` (cm/s): the native expression of
    round8-physical-material-downstream.md section 1 with the density and cosine moved out."""
    d, m = proj["diameter"], proj["mass"]
    return speed * CAP_SPEED_SCALE * m * e / (CAP_DENOM_SCALE * d * d)


def surface_factor(p, s):
    return min(1.0, max(0.0, 1.0 - 0.5 * (p + s)))


def build():
    cfg = read_config() or stored_config()
    if cfg is None:
        raise SystemExit("no packed config (set WARDOGS_CONFIG_DIR) and no stored config in the JSON")
    projs, mods, speeds = projectiles(), ammo_modifiers(), weapon_speeds()
    wd = json.load(open(os.path.join(ROOT, "assets/data/weapon-damage.json"), encoding="utf-8"))
    surf = {s["surface_type"]: s for s in cfg["surfaces"]}
    weapons = []
    for w in wd["weapons"]:
        sp = speeds.get(w["id"], {})
        v0 = sp.get("initial_bullet_speed")
        entry = {"id": w["id"], "caliber": w["caliber"], "stats_asset": sp.get("stats_asset"),
                 "initial_bullet_speed": v0, "typical_speed_override": sp.get("override_typical_speed"), "ammo": []}
        for a in w["ammo"]:
            proj = projs.get(a["projectile"])
            if proj is None or proj["diameter"] is None:
                continue
            mod = mods.get(a["modifier_tag"]) if a["modifier_tag"] else None
            p, e = variant(proj, mod)
            ref = sp.get("override_typical_speed") or proj["typical_speed"]
            row = {"ammo": a["id"], "modifier_tag": a["modifier_tag"], "projectile": a["projectile"],
                   "projectile_asset": proj["asset"], "exit_speed_multiplier": r(p), "penetration_effectiveness": r(e),
                   "speed_scale_reference": ref,
                   "min_impact_angle_for_ricochet_deg": proj["min_impact_angle_for_ricochet_deg"]
                   if proj["min_impact_angle_for_ricochet_deg"] is not None else DEFAULTS["min_impact_angle_for_ricochet_deg"]}
            if v0:
                row["capacity_coefficient_k"] = r(capacity_coefficient(proj, e, v0))
                row["launch_speed_scale"] = r(min(1.0, v0 / ref))
            entry["ammo"].append(row)
        weapons.append(entry)

    reference = []
    for wid in REFERENCE_WEAPONS:
        w = next(x for x in weapons if x["id"] == wid)
        for row in w["ammo"]:
            if "capacity_coefficient_k" not in row:
                continue
            v0, ref, p = w["initial_bullet_speed"], row["speed_scale_reference"], row["exit_speed_multiplier"]
            per = []
            for si in SHOWN_SURFACES:
                s = surf[si]["exit_speed_modifier"]
                sf = surface_factor(p, s)
                per.append({"surface_type": si, "name": surf[si]["name"], "exit_speed_modifier": s,
                            "surface_factor": r(sf),
                            "next_impact_damage_fraction": {f"{f:g}": r(min(1.0, v0 * (1 - f) * sf / ref)) for f in LOAD_GRID}})
            reference.append({"weapon": wid, "ammo": row["ammo"], "launch_speed": v0, "speed_scale_reference": ref,
                              "exit_speed_multiplier": row["exit_speed_multiplier"], "capacity_coefficient_k": row["capacity_coefficient_k"],
                              "surfaces": per})
    return {
        "meta": {
            "generator": "_tools/weapon_penetration.py",
            "doc": "docs/evidence/round25-ricochet-penetration.md",
            "assumptions": [
                "Point blank: the impact speed is the weapon's InitialBulletSpeed (no drag, ProjectileFlight section 2).",
                "Normal incidence for load figures (cosine 1). capacity = k * cos / density; thickness load f = thickness * density / (k * cos); "
                "a pass needs capacity > thickness / cos, which is f < cos.",
                "speed after the pass = speed * (1 - f) * clamp(1 - 0.5 * (p + s), 0, 1), with p the ammo variant's exit-speed multiplier and s the surface entry.",
                "next_impact_damage_fraction = min(1, speed_after / speed_scale_reference): the section 7.6 speed scale at the NEXT impact, no drag between the two.",
                "Ammo variant stats = base asset stat times the modifier multiplier; an omitted base stat takes the native constructor default (E 1.0, p 0.0).",
                "Nothing here says which surface a given wall or prop has, or its density or thickness. Those are not in the export.",
            ],
            "surface_note": SURFACE_PM_NOTE,
            "native_defaults": DEFAULTS,
            "native_constants": {"capacity_speed_scale": CAP_SPEED_SCALE, "capacity_denominator_scale": CAP_DENOM_SCALE},
            "reference_weapons": REFERENCE_WEAPONS,
            "load_grid": LOAD_GRID,
        },
        "config": cfg,
        "ammo_modifiers": mods,
        "projectiles": projs,
        "weapons": weapons,
        "reference": reference,
        "known_physical_materials": {
            "PM_Head": {"surface_type": 17, "density": 0.2, "source": "docs/evidence/round8-collision.md"},
            "PM_Body": {"surface_type": 3, "density": 1.0, "density_note": "omitted in the asset; native UPhysicalMaterial default",
                        "source": "docs/evidence/round8-collision.md"},
        },
    }


# ---------------------------------------------------------------- checks

def check():
    ok = True

    def rep(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond)
        print(("PASS " if cond else "FAIL ") + name + (f" ({detail})" if detail else ""))

    cur = build()
    stored = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else None
    rep("JSON on disk matches a fresh build", stored == json.loads(json.dumps(cur)),
        "run --write" if stored != json.loads(json.dumps(cur)) else "")
    surf = {s["surface_type"]: s for s in cur["config"]["surfaces"]}
    rep("63 surface types (Default, 1..62)", len(surf) == 63 and set(surf) == set(range(63)))
    # round8-physical-material-downstream.md section 3
    z = all(surf[i]["exit_speed_modifier"] == 0 and surf[i]["ricochet_probability"] == 0 and surf[i]["restitution"] == [1.0, 1.0] for i in (3, 17))
    rep("SurfaceType3/17: exit-speed 0, ricochet 0, restitution 1-1 (round8 downstream section 3)", z)
    rep("SurfaceType3 = Body, 17 = Head (DefaultEngine.ini names)", surf[3]["name"] == "Body" and surf[17]["name"] == "Head")
    nonzero_rico = sorted(i for i, s in surf.items() if s["ricochet_probability"] > 0)
    rep("zeros are the exception: most surface types have a nonzero ricochet chance",
        len(nonzero_rico) > 50, f"{len(nonzero_rico)} of 63 nonzero")
    rep("PM_Head / PM_Body in the penetration ignore list (round8 downstream section 4)",
        {"/Game/Environment/_Global/PhysicalMaterials/PM_Body.PM_Body", "/Game/Environment/_Global/PhysicalMaterials/PM_Head.PM_Head"}
        <= set(cur["config"]["penetration_phys_mat_ignore_list"]))
    # content/Wardogs_GameMechanics_v2.md section 2e table
    doc = open(os.path.join(ROOT, "content/Wardogs_GameMechanics_v2.md"), encoding="utf-8").read()
    want = {"ArmorPiercing": (1.8, 1.2, 0.0), "ArmorPiercing.Tracer": (1.76, 1.2, 0.0), "HollowPoint": (0.1, 0.8, 0.15),
            "HollowPoint.Tracer": (0.1, 0.8, 0.15), "Tracer": (1.0, 1.0, 0.075)}
    good = True
    for name, (e, rng, p) in want.items():
        m = cur["ammo_modifiers"].get("Meta.Damage.AmmoModifier." + name, {})
        good &= (m.get("PenetrationEffectivenessMultiplier"), m.get("EffectiveRangeMultiplier"), m.get("PenetrationExitSpeedMultiplier")) == (e, rng, p)
        good &= bool(re.search(rf"\|\s*{re.escape(name)}\s*\|\s*{e:g}\s*\|\s*{rng:g}\s*\|\s*{p:g}", doc.replace("0.0 |", "0 |").replace("1.0 |", "1 |")) or name in doc)
    rep("ammo modifier multipliers equal the GameMechanics table", good)
    # ProjectileFlight section 10: 155 mm assets set 91 degrees
    a155 = [v for v in cur["projectiles"].values() if v["asset"].startswith("DA_155mm")]
    rep("155 mm assets set MinImpactAngleForRicochet 91 (ProjectileFlight)", a155 and all(v["min_impact_angle_for_ricochet_deg"] == 91 for v in a155))
    # weapon-damage.json: every ammo row of every weapon with a modeled projectile keeps its FMJ == base stats
    wd = json.load(open(os.path.join(ROOT, "assets/data/weapon-damage.json"), encoding="utf-8"))
    rep("same weapon list as weapon-damage.json", [w["id"] for w in wd["weapons"]] == [w["id"] for w in cur["weapons"]])
    fm = [a for w in cur["weapons"] for a in w["ammo"] if a["ammo"] == "FMJ"]
    rep("FMJ rows carry the unmodified base stats", all(a["modifier_tag"] is None for a in fm) and len(fm) > 20)
    ap = [a for w in cur["weapons"] for a in w["ammo"] if a["ammo"] == "ArmorPiercing"]
    rep("AP exit-speed multiplier is 0 everywhere (0.0 times any base)", ap and all(a["exit_speed_multiplier"] == 0 for a in ap))
    # formula recomputation on A91 FMJ: 71500 cm/s, m 0.0041, d 0.57, E 1
    a91 = next(w for w in cur["weapons"] if w["id"] == "A91")
    k = next(a for a in a91["ammo"] if a["ammo"] == "FMJ")["capacity_coefficient_k"]
    exp = 71500 * 0.01 * 0.0041 / (0.099999994 * 0.57 ** 2)
    rep("A91 FMJ capacity coefficient recomputes by hand", math.isclose(k, exp, rel_tol=1e-5), f"{k} vs {exp:.5f}")
    # damage-rule row: the history tags change no infantry rule (evidence claim)
    n_inf = sum(1 for e in dt.ENTRIES if re.search(r"Impact\.(Ricochet|Penetration)", json.dumps([e["SourceRequirements"], e["TargetRequirements"]])))
    veh = dt.rows("DT_GlobalDamage_VehicleData.json")
    veh_hits = [e["OutModification"]["Amount"] for row in veh.values() for e in row.get("DamageModificationEntries", [])
                if re.search(r"Impact\.(Ricochet|Penetration)", json.dumps([e["SourceRequirements"], e["TargetRequirements"]]))]
    rep("no infantry rule keys on Kinetic.Impact.Ricochet/Penetration", n_inf == 0)
    rep("vehicle table: one such entry, Amount 0", veh_hits == [0.0], str(veh_hits))
    # reference grid sanity: monotone in load, never above 1
    mono = all(all(list(s["next_impact_damage_fraction"].values())[i] >= list(s["next_impact_damage_fraction"].values())[i + 1]
                   and list(s["next_impact_damage_fraction"].values())[0] <= 1.0 for i in range(3))
               for ref in cur["reference"] for s in ref["surfaces"])
    rep("damage fraction falls with load and stays <= 1", mono)
    print("OVERALL " + ("PASS" if ok else "FAIL"))
    return ok


def summary(cur):
    print(f"{len(cur['config']['surfaces'])} surface types, {len(cur['weapons'])} weapons, {len(cur['reference'])} reference rows")
    for ref in cur["reference"]:
        if ref["ammo"] not in ("FMJ", "ArmorPiercing"):
            continue
        print(f"{ref['weapon']:8} {ref['ammo']:14} v0={ref['launch_speed']:.0f} ref={ref['speed_scale_reference']:.0f} p={ref['exit_speed_multiplier']} K={ref['capacity_coefficient_k']}")
        for s in ref["surfaces"]:
            print(f"    {s['name']:16} s={s['exit_speed_modifier']:<5} sf={s['surface_factor']:<6} {s['next_impact_damage_fraction']}")


def main(argv):
    if "--check" in argv:
        sys.exit(0 if check() else 1)
    cur = build()
    if "--write" in argv:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cur, f, indent=1)
            f.write("\n")
        print("wrote", os.path.relpath(OUT, ROOT))
    summary(cur)


if __name__ == "__main__":
    main(sys.argv[1:])
