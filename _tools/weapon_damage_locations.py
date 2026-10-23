"""Damage by weapon, ammo type, hit location and armor condition, for every infantry hit location.

Extends weapon_damage_tables.py (imported, not modified): the same weapons, ammo options, projectile
contexts and damage_tables.evaluate() rule engine, but armor is applied at every location. The game
keeps an armor piece in the target context only when that piece's CoveredHitLocations contains the hit
location (DamagePipeline v2 section 7.6, round 8), so each armor item is evaluated only at the
locations its own data lists; at any other location the item has no effect and the result equals the
unarmored one. Coverage is read from the Armor item files (WDInventoryFragment_Armor.CoveredHitLocations),
not assumed.

    python _tools/weapon_damage_locations.py --json                       # write assets/data/weapon-damage-locations.json
    python _tools/weapon_damage_locations.py --rank ArmorPiercing Heavy Torso.Middle
    python _tools/weapon_damage_locations.py --check                      # PASS/FAIL, non-zero exit on FAIL

Same assumptions as weapon-damage.json: hostile alignment, direct hit at point blank, no ricochet or
penetration, target outside any vehicle, no instigator tags, one hit.

JSON schema (assets/data/weapon-damage-locations.json)
    meta        generator, source_data_tree, assumptions, unit, locations[12], armor_items[], armor_effect{}
    meta.armor_items[]   id, context_tag, kind ("vest" | "helmet"), class, durability_reduction_pct (R),
                         covered_locations[] (short names, read from the item data)
    meta.armor_effect    {location: {kind, covering: {class: {item, reduction_pct, fmj_multiplier}},
                         not_covering: [classes of that kind that leave the location unarmored]}}
                         fmj_multiplier is M4 FMJ damage with the item over M4 FMJ unarmored. Other
                         ammo types scale the reduction through the per-ammo table: use each row's own
                         damage / damage["None"].
    weapons[]   id, name, caliber, ammo[]: id, label, items, modifier_tag, projectile, base_damage, pellets, note
        damage      {location: {condition: value}} rounded to 1 decimal. Conditions per location:
                    "None" plus the class names of the armor items that cover that location
                    (vest classes for body locations, helmet classes for Head and Neck).
        damage_raw  same shape, unrounded
    Damage is health points per hit; for shotguns it is per pellet.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402
import weapon_damage_tables as wdt  # noqa: E402

ROOT = dt.ROOT
OUT = os.path.join(ROOT, "assets", "data", "weapon-damage-locations.json")
OLD = os.path.join(ROOT, "assets", "data", "weapon-damage.json")
ARMOR_DIR = os.path.join(dt.DATA, "Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data")
HIT_PREFIX = dt.HIT
LOCS = ["Head", "Neck", "Torso.Upper", "Torso.Middle", "Torso.Lower", "Pelvis", "Arm.Upper", "Arm.Lower",
        "Arm.Hand", "Leg.Thigh", "Leg.Calf", "Leg.Foot"]


def armor_items():
    """Every armor or helmet item with a WDInventoryFragment_Armor: class, kind, R, covered locations."""
    items = []
    for name in sorted(os.listdir(ARMOR_DIR)):
        if not (name.startswith("ID_") and name.endswith(".json")):
            continue
        for o in dt.exports(os.path.join(ARMOR_DIR, name)):
            if o.get("Type") != "WDInventoryFragment_Armor":
                continue
            p = o["Properties"]
            ctx = dt.tag(p["DamageContextTag"])
            stages = p.get("DurabilityStagesSetupData", [])
            red = sorted({s.get("DamagePercentageReduction", 0.0) for s in stages})
            cov = [dt.tag(t)[len(HIT_PREFIX):] for t in p.get("CoveredHitLocations", [])]
            items.append({"id": name[:-5], "context_tag": ctx,
                          "kind": "helmet" if ".Helmet." in ctx else "vest", "class": ctx.split(".")[-1],
                          "durability_reduction_pct": red[0] if len(red) == 1 else (red or None),
                          "covered_locations": [l for l in LOCS if l in cov] + [l for l in cov if l not in LOCS]})
    return items


ITEMS = armor_items()


def conditions(loc):
    """Armor items that cover loc, keyed by class."""
    return {i["class"]: i for i in ITEMS if loc in i["covered_locations"]}


def hit_values(src, ctx, base, wtag, pid, modifier):
    context = ctx + ([modifier] if modifier else []) + [wtag, pid, "Meta.Damage.DamageType.Projectile"]
    raw = {}
    for loc in LOCS:
        cells = {"None": base * dt.evaluate(src, context, dt.HIT + loc, [])[0]}
        for cls, it in conditions(loc).items():
            cells[cls] = base * dt.evaluate(src, context, dt.HIT + loc, [it["context_tag"]])[0]
        raw[loc] = cells
    return raw


def build():
    j = wdt.build()
    proj = dt.projectiles()
    weapons = []
    for w in j["weapons"]:
        wtag = "Meta.Damage.Weapon." + w["weapon_tag"]
        ammo = []
        for a in w["ammo"]:
            src, ctx, base = proj[a["projectile"]]
            raw = hit_values(src, ctx, base, wtag, a["projectile"], a["modifier_tag"])
            ammo.append({k: a[k] for k in ("id", "label", "items", "modifier_tag", "projectile", "base_damage",
                                           "pellets", "note")} |
                        {"damage": {l: {c: round(v, 1) for c, v in d.items()} for l, d in raw.items()},
                         "damage_raw": raw})
        weapons.append({"id": w["id"], "name": w["name"], "caliber": w["caliber"], "ammo": ammo})
    m4 = next(w for w in j["weapons"] if w["id"] == "M4")
    fmj = next(a for a in m4["ammo"] if a["id"] == "FMJ")
    s4, c4, b4 = proj[fmj["projectile"]]
    ref = hit_values(s4, c4, b4, "Meta.Damage.Weapon." + m4["weapon_tag"], fmj["projectile"], fmj["modifier_tag"])
    effect = {}
    for loc in LOCS:
        kind = "helmet" if loc in ("Head", "Neck") else "vest"
        cov = conditions(loc)
        classes = sorted({i["class"] for i in ITEMS if i["kind"] == kind and i["class"] != "Ghillie"})
        effect[loc] = {"kind": kind,
                       "covering": {c: {"item": it["id"], "reduction_pct": it["durability_reduction_pct"],
                                        "fmj_multiplier": round(ref[loc][c] / ref[loc]["None"], 4)}
                                    for c, it in cov.items()},
                       "not_covering": [c for c in classes if c not in cov]}
    tree = subprocess.run(["git", "rev-parse", "HEAD:data"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    meta = {"generator": "python _tools/weapon_damage_locations.py --json", "source_data_tree": tree,
            "unit": j["meta"]["unit"], "locations": LOCS,
            "assumptions": [a for a in j["meta"]["assumptions"] if not a.startswith("armor classes are evaluated")] + [
                "armor is applied at a location only when the armor item's CoveredHitLocations lists it (read from the item data); a vest and a helmet never cover the same location, so one covering piece is in play at a time",
                "Ghillie armor and helmets have no stages and no covered locations: no effect at any location"],
            "armor_items": ITEMS, "armor_effect": effect}
    return {"meta": meta, "weapons": weapons}


def write_json():
    j = build()
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(j, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(j['weapons'])} weapons, "
          f"{sum(len(w['ammo']) for w in j['weapons'])} weapon x ammo rows")


def rank(ammo, armor, loc):
    j = build()
    key = {a.lower(): a for a in wdt.OPTION_ORDER}
    ammo = wdt.ALIASES.get(ammo.lower(), key.get(ammo.lower(), ammo))
    loc = {"torso": "Torso.Upper", "head": "Head", "hand": "Arm.Hand"}.get(
        loc.lower(), next((x for x in LOCS if x.lower() == loc.lower()), loc))
    if loc not in LOCS:
        sys.exit(f"location must be one of {LOCS}")
    cov = conditions(loc)
    names = {c.lower(): c for c in ["None", *cov]}
    all_classes = {i["class"].lower(): i["class"] for i in ITEMS}
    a_l = armor.lower()
    note = ""
    if a_l in names:
        cond = names[a_l]
    elif a_l in all_classes:
        cond = "None"
        note = f" ({all_classes[a_l]} armor does not cover {loc}: unarmored result)"
    else:
        sys.exit(f"armor must be None or one of {sorted(set(all_classes.values()))}")
    rows = []
    for w in j["weapons"]:
        a = next((x for x in w["ammo"] if x["id"] == ammo), None)
        if a:
            rows.append((a["damage_raw"][loc][cond], w, a))
    rows.sort(key=lambda r: (-r[0], r[1]["id"]))
    print(f"{ammo} vs {armor} at {loc}{note}: damage per hit, {len(rows)} weapons (shotgun values are per pellet)")
    print("| Rank | Weapon | Name | Caliber | Damage | Pellets |")
    print("|---:|---|---|---|---:|---:|")
    n, last = 0, None
    for i, (v, w, a) in enumerate(rows, 1):
        if last is None or round(v, 6) != round(last, 6):
            n = i
        last = v
        print(f"| {n} | {w['id']} | {w['name']} | {w['caliber']} | {v:.1f} | {a['pellets'] or ''} |")


def check():
    j = build()
    old = json.load(open(OLD, encoding="utf-8"))
    fails = 0

    def report(ok, msg):
        nonlocal fails
        fails += not ok
        print(("PASS " if ok else "FAIL ") + msg)

    mine = {(w["id"], a["id"]): a for w in j["weapons"] for a in w["ammo"]}
    theirs = {(w["id"], a["id"]): a for w in old["weapons"] for a in w["ammo"]}
    report(set(mine) == set(theirs), f"same weapon x ammo rows as weapon-damage.json ({len(mine)} vs {len(theirs)})")
    bad_t, bad_h, bad_l, n = [], [], [], 0
    for k, o in theirs.items():
        m = mine.get(k)
        if not m:
            continue
        n += 1
        for c, v in o["damage_raw"]["torso_armor"].items():
            if m["damage_raw"]["Torso.Upper"][c] != v:
                bad_t.append((k, c))
        for c, v in o["damage_raw"]["head_armor"].items():
            if m["damage_raw"]["Head"][c] != v:
                bad_h.append((k, c))
        for loc, v in o["damage_raw"]["location"].items():
            if m["damage_raw"][loc]["None"] != v:
                bad_l.append((k, loc))
    report(not bad_t, f"torso_armor cells (Torso.Upper x None..SuperHeavy) reproduced exactly for {n} rows"
           + (f"; differs {bad_t[:5]}" if bad_t else ""))
    report(not bad_h, f"head_armor cells (Head x None..SuperHeavy helmet) reproduced exactly for {n} rows"
           + (f"; differs {bad_h[:5]}" if bad_h else ""))
    report(not bad_l, f"unarmored location cells (Head, Neck, Torso.Upper, Torso.Middle, Arm.Upper, Leg.Thigh) reproduced exactly for {n} rows"
           + (f"; differs {bad_l[:5]}" if bad_l else ""))
    m4 = mine[("M4", "FMJ")]["damage_raw"]
    for loc, cls, want in [("Torso.Middle", "Heavy", 13.6), ("Neck", "Heavy", 24.7), ("Arm.Upper", "SuperHeavy", 6.05)]:
        got = m4[loc][cls]
        report(abs(got - want) < 0.06, f"M4 FMJ {loc} into {cls}: {got:.3f} (verifier {want}); unarmored {m4[loc]['None']:.2f}")
    hb = json.load(open(os.path.join(ROOT, "assets", "data", "infantry-hitboxes.json"), encoding="utf-8"))
    bad = []
    for h in hb["hit_locations"]:
        want = sorted(h["covered_by"])
        got = sorted(i["id"] for i in ITEMS if h["short"] in i["covered_locations"])
        if want != got:
            bad.append((h["short"], want, got))
    report(not bad, "coverage matches infantry-hitboxes.json covered_by for all 12 locations"
           + (f"; differs {bad}" if bad else ""))
    over = [l for l in LOCS if len({i["kind"] for i in ITEMS if l in i["covered_locations"]}) > 1]
    report(not over, "no location is covered by both a vest and a helmet" + (f": {over}" if over else ""))
    print("FAILED" if fails else "ALL PASSED")
    sys.exit(1 if fails else 0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if "--check" in a:
        check()
    elif "--json" in a:
        write_json()
    elif "--rank" in a and len(a) >= 4:
        rank(*a[a.index("--rank") + 1:a.index("--rank") + 4])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
