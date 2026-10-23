"""Generated tables for game-features/Wardogs_WeaponDamage_v1.md, read from assets/data/weapon-damage.json.

Every table is one marked block; the prose around them is hand-written:

    <!-- weapon_damage_tables MODE -->  ...  <!-- /weapon_damage_tables -->

    python _tools/weapon_damage_page.py --write   # refresh every block in place (idempotent)
    python _tools/weapon_damage_page.py MODE      # print one block: rank_ap_torso, rank_ap_head, rank_hp_torso,
                                                  # rank_hp_head, rank_fmj_torso, rank_fmj_head, all, location,
                                                  # dist_fmj, dist_ap, dist_weapons, dist_cubic, armor_cover,
                                                  # armor_m4, armor_rank_neck, pen_ammo, pen_surfaces

Sections 1 to 4 read weapon-damage.json. Sections 5 to 7 read weapon-damage-falloff.json,
weapon-damage-locations.json and weapon-penetration.json from assets/data (round 25 outputs).

The JSON is read as it is; run `python _tools/weapon_damage_tables.py --json` first if the game data changed.
Ranking rules: damage is the unrounded value (damage_raw), ties are equal after rounding to 6 decimals, identical
weapons share one rank and are named together, the top 5 distinct values are shown per column. Shotgun values
are per pellet. Distance and armor-location rankings use the stored damage at one decimal (falloff JSON has no
damage_raw); the armor-location ranking uses damage_raw.
"""
import json
import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data", "weapon-damage.json")
PAGE = "game-features/Wardogs_WeaponDamage_v1.md"
BLOCK = re.compile(r"<!-- weapon_damage_tables (\w+) -->\r?\n.*?<!-- /weapon_damage_tables -->", re.S)

AMMO = {"ap": "ArmorPiercing", "hp": "HollowPoint", "fmj": "FMJ"}
AMMO_LABEL = {"FMJ": "FMJ", "Tracer": "Tracer", "HollowPoint": "HP", "HollowPoint.Tracer": "HP tracer",
              "ArmorPiercing": "AP", "ArmorPiercing.Tracer": "AP tracer", "ArmourPiercing": "AP (ArmourPiercing)",
              "ArmourPiercing.Tracer": "AP tracer (ArmourPiercing)", "Buckshot": "Buckshot", "Slug": "Slug"}
TORSO_COLS = [("no armor", "location", "Torso.Upper"), ("Medium", "torso_armor", "Medium"),
              ("SuperHeavy", "torso_armor", "SuperHeavy")]
HEAD_COLS = [("no helmet", "location", "Head"), ("Heavy", "head_armor", "Heavy")]
TOP = 5
LOCS = ["Head", "Neck", "Torso.Upper", "Torso.Middle", "Arm.Upper", "Leg.Thigh"]


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def label(w):
    return w["name"] if w["name"] == w["id"] else f"{w['name']} ({w['id']})"


def ammo_of(w, ammo_id):
    return next((a for a in w["ammo"] if a["id"] == ammo_id), None)


def fmt(v):
    return f"{v:.1f}"


def ammo_cell(a):
    name = AMMO_LABEL.get(a["id"], a["id"])
    return f"{name} ({a['pellets']} pellets)" if a.get("pellets") else name


def top_groups(pairs):
    """pairs: [(value, weapon)]. Distinct values, highest first: [(value, [weapon, ...])], at most TOP entries."""
    pairs = sorted(pairs, key=lambda r: (-r[0], r[1]["id"]))
    groups, last = [], None
    for v, w in pairs:
        key = round(v, 6)
        if last is None or key != last:
            groups.append((v, []))
            last = key
        groups[-1][1].append(w)
    return groups[:TOP]


def ranked_groups(j, ammo_id, group, sub):
    """Distinct damage values, highest first: [(value, [weapon, ...])], at most TOP entries."""
    vals = []
    for w in j["weapons"]:
        a = ammo_of(w, ammo_id)
        if a:
            vals.append((a["damage_raw"][group][sub], w))
    return top_groups(vals)


def rank_block(j, short, loc):
    ammo_id = AMMO[short]
    cols = TORSO_COLS if loc == "torso" else HEAD_COLS
    where = "Torso.Upper" if loc == "torso" else "Head"
    name = {"ap": "AP", "hp": "HP", "fmj": "FMJ"}[short]
    tables = [(c, ranked_groups(j, ammo_id, g, s)) for c, g, s in cols]
    lead = []
    for c, groups in tables:
        v, ws = groups[0]
        lead.append(f"{c}: {', '.join(label(w) for w in ws)} at {fmt(v)}")
    out = [f"**Leader.** {name} against {where}, " + "; ".join(lead) + "."]
    if short != "fmj":
        out[0] += " Shotguns have no AP or HP round, so they are not in this ranking."
    out.append("")
    out.append("| Rank | " + " | ".join(c for c, _, _ in cols) + " |")
    out.append("|---:|" + "|".join("---" for _ in cols) + "|")
    for r in range(TOP):
        cells = []
        for _, groups in tables:
            if r < len(groups):
                v, ws = groups[r]
                cells.append(f"{', '.join(label(w) for w in ws)}: {fmt(v)}")
            else:
                cells.append("")
        out.append(f"| {r + 1} | " + " | ".join(cells) + " |")
    return out


def merged_rows(j):
    """One entry per set of weapons with identical damage for every ammo option (same_damage_as groups)."""
    groups = OrderedDict()
    for w in j["weapons"]:
        key = json.dumps([(a["id"], a["damage_raw"]) for a in w["ammo"]], sort_keys=True)
        groups.setdefault(key, []).append(w)
    return list(groups.values())


def all_block(j):
    head = ["| Weapon | Caliber | Ammo | Base damage | Torso: no armor | Torso: Light | Torso: Medium | "
            "Torso: Heavy | Torso: SuperHeavy | Head: no helmet | Head: Heavy |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    out = list(head)
    for ws in merged_rows(j):
        ws = sorted(ws, key=lambda w: w["id"])
        names = ", ".join(label(w) for w in ws)
        cal = ", ".join(sorted({w["caliber"] for w in ws}))
        for a in ws[0]["ammo"]:
            d = a["damage"]
            cells = [fmt(d["location"]["Torso.Upper"])] + [fmt(d["torso_armor"][c]) for c in ["Light", "Medium", "Heavy", "SuperHeavy"]]
            cells += [fmt(d["head_armor"]["None"]), fmt(d["head_armor"]["Heavy"])]
            out.append(f"| {names} | {cal} | {ammo_cell(a)} | {fmt(a['base_damage'])} | " + " | ".join(cells) + " |")
    return out


def location_block(j):
    out = ["| Weapon | Caliber | Ammo | " + " | ".join(LOCS) + " |",
           "|---|---|---|" + "---:|" * len(LOCS)]
    by_vals = OrderedDict()
    for w in j["weapons"]:
        a = ammo_of(w, "FMJ") or ammo_of(w, "Buckshot")
        key = json.dumps([a["damage"]["location"][k] for k in LOCS] + [a["id"]])
        by_vals.setdefault(key, []).append((w, a))
    for rows in by_vals.values():
        ws = sorted((w for w, _ in rows), key=lambda w: w["id"])
        a = rows[0][1]
        cal = ", ".join(sorted({w["caliber"] for w in ws}))
        vals = [fmt(a["damage"]["location"][k]) for k in LOCS]
        out.append(f"| {', '.join(label(w) for w in ws)} | {cal} | {ammo_cell(a)} | " + " | ".join(vals) + " |")
    return out


def read_json(rel):
    with open(os.path.join(ROOT, "assets", "data", rel), encoding="utf-8") as f:
        return json.load(f)


# Round 25 sections. Each reads its own JSON, so the weapon-damage JSON argument is unused for them.
DIST_STEPS = [100, 400, 800, 1200]
DIST_COLS = [("Torso, no armor", "torso", "None"), ("Torso, Medium", "torso", "Medium"),
             ("Head, no helmet", "head", "None")]
CLASS_ORDER = ["Light", "Medium", "Pilot", "Heavy", "SuperHeavy", "Tank", "Ghillie"]
KIND_ORDER = {"vest": 0, "helmet": 1}
MODIFIERS = [("Meta.Damage.AmmoModifier.Tracer", "Tracer"),
             ("Meta.Damage.AmmoModifier.HollowPoint", "HP"),
             ("Meta.Damage.AmmoModifier.HollowPoint.Tracer", "HP tracer"),
             ("Meta.Damage.AmmoModifier.ArmorPiercing", "AP"),
             ("Meta.Damage.AmmoModifier.ArmorPiercing.Tracer", "AP tracer")]
SURFACE_SELECTION = ["Body", "Head", "Default", "Brick", "Concrete", "Glass", "Metal", "Plaster", "Wood",
                     "BulletProofGlass", "Ice"]


def fx(v):
    return f"{v:.3f}"


def g(v):
    return f"{v:g}"


def falloff_multipliers(w, a):
    """Damage multiplier per distance: the curve (only where the weapon applies it) times the speed scale.
    None where the model does not reach the distance."""
    out = []
    for i in range(len(a["speed_scale"])):
        s = a["speed_scale"][i]
        c = a["curve_multiplier"][i] if w["curve"]["used"] else 1.0
        out.append(None if s is None else c * s)
    return out


def dist_index(fo, m):
    return fo["meta"]["distances_m"].index(m)


def distance_rank_block(short):
    fo = read_json("weapon-damage-falloff.json")
    ammo_id = AMMO[short]
    name = {"fmj": "FMJ", "ap": "AP"}[short]
    out = []
    for m in DIST_STEPS:
        i = dist_index(fo, m)
        tables = []
        for c, loc, cls in DIST_COLS:
            pairs = []
            for w in fo["weapons"]:
                a = ammo_of(w, ammo_id)
                if a and a["damage"][loc][cls][i] is not None:
                    pairs.append((a["damage"][loc][cls][i], w))
            tables.append((c, top_groups(pairs)))
        lead = [f"{c}: {', '.join(label(w) for w in ws)} at {fmt(v)}" for c, groups in tables
                for v, ws in [groups[0]]]
        note = " Shotguns have no FMJ or AP round, so they are not in this ranking." if m == DIST_STEPS[0] else ""
        out.append(f"**{m} m.** {name} leader. " + "; ".join(lead) + "." + note)
        out.append("")
        out.append("| Rank | " + " | ".join(c for c, _ in tables) + " |")
        out.append("|---:|" + "|".join("---" for _ in tables) + "|")
        for r in range(TOP):
            cells = []
            for _, groups in tables:
                if r < len(groups):
                    v, ws = groups[r]
                    cells.append(f"{', '.join(label(w) for w in ws)}: {fmt(v)}")
                else:
                    cells.append("")
            out.append(f"| {r + 1} | " + " | ".join(cells) + " |")
        out.append("")
    return out[:-1]


def distance_weapon_block():
    fo = read_json("weapon-damage-falloff.json")
    out = ["| Weapon | Caliber | Default round | Effective range end (m) | Speed scale below 1 from (m) | "
           "100 m | 400 m | 800 m | 1200 m |",
           "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for w in fo["weapons"]:
        a = ammo_of(w, "FMJ") or ammo_of(w, "Buckshot")
        mult = falloff_multipliers(w, a)
        er = w["effective_range_m"]
        bites = a["speed_scale_bites_at_m"]
        cells = []
        for m in DIST_STEPS:
            v = mult[dist_index(fo, m)]
            cells.append("not reached" if v is None else fx(v))
        out.append(f"| {label(w)} | {w['caliber']} | {ammo_cell(a)} | "
                   f"{'not stated' if er is None else f'{er:.0f}'} | "
                   f"{'none' if bites is None else f'{bites:.0f}'} | " + " | ".join(cells) + " |")
    return out


def cubic_block():
    fo = read_json("weapon-damage-falloff.json")
    out = ["| Weapon | Largest gap between the linear and exact curve (multiplier) | At (m) |", "|---|---:|---:|"]
    for w in fo["weapons"]:
        cv = w["curve"].get("cubic_vs_linear")
        if cv:
            out.append(f"| {label(w)} | {fx(cv['max_abs_multiplier_diff'])} | {cv['at_m']:.0f} |")
    return out


def armor_cover_block():
    L = read_json("weapon-damage-locations.json")
    meta = L["meta"]
    locs = meta["locations"]
    items = meta["armor_items"]
    covered = [loc for loc in locs if any(loc in it["covered_locations"] for it in items)]
    groups = OrderedDict()
    for it in sorted(items, key=lambda it: (KIND_ORDER[it["kind"]], CLASS_ORDER.index(it["class"]), it["id"])):
        key = (it["kind"], it["class"], it["durability_reduction_pct"], tuple(it["covered_locations"]))
        groups.setdefault(key, []).append(it["id"])
    out = ["| Item | Kind | Class | " + " | ".join(covered) + " |",
           "|---|---|---|" + "|".join("---:" for _ in covered) + "|"]
    for (kind, cls, red, cov), ids in groups.items():
        cells = []
        for loc in covered:
            cells.append(f"{red:.0f}%" if loc in cov else "")
        cls_text = cls if red is not None else f"{cls} (effect not determined, treated as none)"
        out.append(f"| {', '.join(ids)} | {kind} | {cls_text} | " + " | ".join(cells) + " |")
    vest = {loc for it in items if it["kind"] == "vest" for loc in it["covered_locations"]}
    helm = {loc for it in items if it["kind"] == "helmet" for loc in it["covered_locations"]}
    both = [loc for loc in locs if loc in vest and loc in helm]
    nothing = [loc for loc in locs if loc not in vest and loc not in helm]
    out.append("")
    out.append("No location is covered by both a vest and a helmet." if not both
               else f"Covered by both a vest and a helmet: {', '.join(both)}.")
    out.append(f"Covered by no item ({len(nothing)}): {', '.join(nothing)}.")
    return out


def armor_m4_block():
    L = read_json("weapon-damage-locations.json")
    meta = L["meta"]
    items = meta["armor_items"]
    covered = {(loc, it["class"]) for it in items for loc in it["covered_locations"]}
    w = next(x for x in L["weapons"] if x["id"] == "M4")
    a = ammo_of(w, "FMJ")
    cols = ["None", "Light", "Medium", "Pilot", "Heavy", "SuperHeavy", "Tank"]
    out = ["| Location | no armor | Light | Medium | Pilot | Heavy | SuperHeavy | Tank |",
           "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for loc in meta["locations"]:
        cells = []
        for c in cols:
            if c == "None" or (loc, c) in covered:
                cells.append(fmt(a["damage"][loc][c]))
            else:
                cells.append("no cover")
        out.append(f"| {loc} | " + " | ".join(cells) + " |")
    return out


def armor_rank_block():
    L = read_json("weapon-damage-locations.json")
    loc, cls = "Neck", "Heavy"
    tables = [("AP", ranked_groups(L, AMMO["ap"], loc, cls)), ("FMJ", ranked_groups(L, AMMO["fmj"], loc, cls))]
    lead = [f"{n}: {', '.join(label(w) for w in groups[0][1])} at {fmt(groups[0][0])}" for n, groups in tables]
    out = [f"**Leader.** {loc} with a {cls} helmet. " + "; ".join(lead) + ". Shotguns have no AP or FMJ round, "
           "so they are not in this ranking.", "",
           "| Rank | AP | FMJ |", "|---:|---|---|"]
    for r in range(TOP):
        cells = []
        for _, groups in tables:
            if r < len(groups):
                v, ws = groups[r]
                cells.append(f"{', '.join(label(w) for w in ws)}: {fmt(v)}")
            else:
                cells.append("")
        out.append(f"| {r + 1} | " + " | ".join(cells) + " |")
    return out


def penetration_ammo_block():
    P = read_json("weapon-penetration.json")
    out = ["| Ammo | Penetration effectiveness | Exit speed | Effective range | Tracer chance |",
           "|---|---:|---:|---:|---:|",
           "| FMJ (no modifier asset) | x1 | x1 | x1 | none |"]
    for key, name in MODIFIERS:
        m = P["ammo_modifiers"][key]
        tracer = m.get("TracerChance")
        out.append(f"| {name} | x{g(m['PenetrationEffectivenessMultiplier'])} | "
                   f"x{g(m['PenetrationExitSpeedMultiplier'])} | x{g(m['EffectiveRangeMultiplier'])} | "
                   f"{'none' if tracer is None else g(tracer)} |")
    return out


def penetration_surfaces_block():
    P = read_json("weapon-penetration.json")
    S = P["config"]["surfaces"]
    named = [s for s in S if s["surface_type"] <= 38]
    unnamed = [s for s in S if s["surface_type"] >= 39]
    n_rz = sum(1 for s in S if s["ricochet_probability"] != 0)
    zero_rz = [s["name"] for s in S if s["ricochet_probability"] == 0]
    n_ex = sum(1 for s in S if s["exit_speed_modifier"] != 0)
    zero_ex = [s["name"] for s in S if s["exit_speed_modifier"] == 0]
    un_p = sorted({s["ricochet_probability"] for s in unnamed})
    un_s = sorted({s["exit_speed_modifier"] for s in unnamed})
    un_r = sorted({tuple(s["restitution"]) for s in unnamed if s["restitution"] is not None})
    named_zero_ex = [s["name"] for s in named if s["exit_speed_modifier"] == 0]
    out = ["| Measure | Result |", "|---|---|",
           f"| Surface types in the export | {len(S)}: {len(named)} named (SurfaceType0 to 38), "
           f"{len(unnamed)} unnamed (39 to 62) |",
           f"| Nonzero ricochet probability | {n_rz} of {len(S)}. Zero for {len(zero_rz)}: {', '.join(zero_rz)} |",
           f"| Nonzero exit-speed modifier | {n_ex} of {len(S)}. Zero for {len(zero_ex)}: "
           f"{', '.join(named_zero_ex)}, and the {len(unnamed)} unnamed types |",
           f"| Unnamed types 39 to 62 | ricochet probability {', '.join(f'{v:g}' for v in un_p)}; "
           f"exit-speed modifier {', '.join(f'{v:g}' for v in un_s)}; restitution "
           f"{', '.join(f'{a:g} to {b:g}' for a, b in un_r)} |",
           "", "| Type | Name | Exit-speed modifier | Ricochet probability | Restitution (min to max) |",
           "|---:|---|---:|---:|---|"]
    by_name = {s["name"]: s for s in S}
    for name in SURFACE_SELECTION:
        s = by_name[name]
        r = s["restitution"]
        rtext = "empty" if r is None else f"{r[0]:g} to {r[1]:g}"
        out.append(f"| {s['surface_type']} | {name} | {g(s['exit_speed_modifier'])} | "
                   f"{g(s['ricochet_probability'])} | {rtext} |")
    return out


MODES = {}
for _s in ("ap", "hp", "fmj"):
    for _l in ("torso", "head"):
        MODES[f"rank_{_s}_{_l}"] = (lambda s, l: (lambda j: rank_block(j, s, l)))(_s, _l)
MODES["all"] = all_block
MODES["location"] = location_block
MODES["dist_fmj"] = lambda j: distance_rank_block("fmj")
MODES["dist_ap"] = lambda j: distance_rank_block("ap")
MODES["dist_weapons"] = lambda j: distance_weapon_block()
MODES["dist_cubic"] = lambda j: cubic_block()
MODES["armor_cover"] = lambda j: armor_cover_block()
MODES["armor_m4"] = lambda j: armor_m4_block()
MODES["armor_rank_neck"] = lambda j: armor_rank_block()
MODES["pen_ammo"] = lambda j: penetration_ammo_block()
MODES["pen_surfaces"] = lambda j: penetration_surfaces_block()


def write(j):
    path = os.path.join(ROOT, PAGE)
    if not os.path.exists(path):
        print(f"{PAGE}: not found, nothing written")
        return
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        mode = m.group(1)
        if mode not in MODES:
            sys.exit(f"unknown table mode in page: {mode}")
        body = MODES[mode](j)
        return nl.join([f"<!-- weapon_damage_tables {mode} -->"] + body + ["<!-- /weapon_damage_tables -->"])
    new, count = BLOCK.subn(regen, text)
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    j = load()
    args = sys.argv[1:]
    if "--write" in args:
        write(j)
    elif args and args[0] in MODES:
        print("\n".join(MODES[args[0]](j)))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
