"""Damage by weapon and ammo type, for every infantry bullet or pellet weapon.

Reuses the damage-event rebuild in damage_tables.py (evaluate(), projectiles(), weapons()); nothing of
its logic is copied. For each weapon it finds the ammo items the weapon's SupportedCaliber can load,
resolves each item's ammo-modifier tag the way the game does (DamagePipeline v2 section 7.9: the last
name of the item tag, or the last two for a five-level tag, looked up in a fixed map), and evaluates
the hit for every hit location and armor class.

    python _tools/weapon_damage_tables.py --json                       # write assets/data/weapon-damage.json
    python _tools/weapon_damage_tables.py --rank ArmorPiercing Medium Torso
    python _tools/weapon_damage_tables.py --check                      # PASS/FAIL against damage_tables.py

Assumptions (also in the JSON's meta): hostile alignment, a direct hit at point blank (no distance
falloff), no ricochet or penetration, a target outside any vehicle, no instigator tags (entries that
need them are counted as unknown and not applied), one hit.

JSON schema (assets/data/weapon-damage.json)
    meta        generator, source_data_tree, assumptions, unit, rules, armor/location vocabularies, exclusions
    weapons[]   one per weapon:
        id, name, archetype, weapon_tag, caliber (primary caliber key), calibers[] (stats SupportedCaliber),
        base_damage (of the default FMJ round), rpm (RoundsPerMinute when the stats asset sets it, else the native struct default 600, ctor RVA 0x699E6C0),
        rpm_source ("asset" | "class_default_native"), fire_modes[], same_damage_as[] (other weapons with
        identical damage cells for every ammo option),
        ammo[]: one per loadable round:
            id          FMJ | Tracer | HollowPoint | HollowPoint.Tracer | ArmorPiercing | ArmorPiercing.Tracer
                        | ArmourPiercing[.Tracer] (item tag spelled the British way: no modifier) | Buckshot | Slug
            label, items[] (ItemId tags), modifier_tag (null = no modifier asset, FMJ behaviour),
            projectile (ProjectileId), base_damage, pellets (NumberOfPellets, null for single bullets),
            note (quirks, else null),
            damage       {location: {location: value}} rounded to 1 decimal, three groups:
                           "location": Head, Neck, Torso.Upper, Torso.Middle, Arm.Upper, Leg.Thigh (unarmored)
                           "torso_armor": None, Light, Medium, Heavy, SuperHeavy (hit on Torso.Upper)
                           "head_armor": None, Light, Medium, Heavy, SuperHeavy helmet (hit on Head)
            damage_raw   same shape, unrounded
            entries_applied  indexes of the infantry rule entries that changed the result
    Damage is health points per hit; for shotguns it is per pellet (multiply by pellets).
"""
import contextlib
import glob
import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402

ROOT, DATA = dt.ROOT, dt.DATA
OUT = os.path.join(ROOT, "assets", "data", "weapon-damage.json")
SHARED = os.environ.get("AMMO_AVAILABILITY", "E:/r24/shared/ammo-availability.json")
AMMO_DIR = os.path.join(DATA, "Wardogs/Content/Items/Resources/Ammo")
CAL_DIR = os.path.join(DATA, "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber")
WEAPON_DIR = os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Weapons")
MOD = "Meta.Damage.AmmoModifier."
MODIFIERS = ["Tracer", "HollowPoint", "HollowPoint.Tracer", "ArmorPiercing", "ArmorPiercing.Tracer"]
ARMOR_CLASSES = ["None"] + dt.CLASSES
OPTION_ORDER = ["FMJ", "Tracer", "HollowPoint", "HollowPoint.Tracer", "ArmorPiercing", "ArmorPiercing.Tracer",
                "ArmourPiercing", "ArmourPiercing.Tracer", "Buckshot", "Slug"]

EXCLUDED = [
    ("Launcher_04, RPG7, MMGL, CGM4", "Launchers: the shot is a rocket or grenade (Meta.Damage.Explosive.*), not a bullet"),
    ("GrenadeLauncher (underbarrel, DA_GrenadeLauncher_Stats)", "Grenade launcher attachment; explosive"),
    ("AT4 (DA_AT4_Stats)", "Rocket launcher stats asset; explosive"),
    ("Fists", "Melee; no bullet or weapon damage tag"),
    ("BuildTool, Small/Medium/LargeHammer", "Build tools, not weapons with a caliber"),
    ("ArtilleryBarrelTest, TankBarrelTest", "Test and artillery/tank barrels (explosive rockets)"),
    ("M2Browning (Stationary)", "Mounted weapon. It fires bullets; it is left out as a scope choice, not computed"),
    ("MWSY_001_Heavy_MountedMachineGun and other vehicle weapons", "Mounted vehicle weapons. They fire bullets; left out as a scope choice, not computed"),
    ("CombatBow", "Fires arrows (Item.Caliber.Arrow), not bullets"),
]


def ids(o, key):
    return [dt.tag(x) for x in dt.walk(o, key)]


def weapon_files():
    """Weapon name -> (ID path, stats export list) for the weapons damage_tables.weapons() returns."""
    stats = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(DATA, "**/DA_*_Stats.json"), recursive=True)}
    out = {}
    for path in sorted(glob.glob(os.path.join(WEAPON_DIR, "**/ID_*.json"), recursive=True)):
        text = open(path, encoding="utf-8").read()
        ref = re.search(r"WDWeaponStatsData'(DA_\w+_Stats)'", text)
        if ref and ref.group(1) in stats:
            out[os.path.basename(path)[3:-5]] = (path, stats[ref.group(1)])
    return out


def weapon_meta(name, files):
    path, stats_path = files[name]
    item = next(o for o in dt.exports(path) if o.get("Type") == "BHInventoryItemDefinition")["Properties"]
    ctx = [dt.tag(t) for t in item.get("ItemContext", [])]
    arch = next((t.split(".")[-1] for t in ctx if t.startswith("Item.Archetype.")), None)
    disp = item.get("DisplayName", {})
    st = dt.exports(stats_path)
    rpm = next((v for o in st for v in dt.walk(o, "RoundsPerMinute")), None)
    modes = next((m for o in st for m in dt.walk(o, "SupportedFireModes")), [])
    return {"name": disp.get("LocalizedString") or disp.get("SourceString") or name, "archetype": arch,
            "rpm": rpm if rpm is not None else 600.0,
            "rpm_source": "asset" if rpm is not None else "class_default_native",
            "fire_modes": [m.split("::")[-1] for m in modes]}


def projectile_assets():
    """Caliber data asset name -> (ProjectileId, NumberOfPellets)."""
    out = {}
    for path in glob.glob(os.path.join(CAL_DIR, "**/DA_*.json"), recursive=True):
        for o in dt.exports(path):
            props = o.get("Properties", {})
            pid = dt.tag(props.get("ProjectileId"))
            if pid:
                pel = next((v for v in dt.walk(props, "NumberOfPellets")), None)
                out[o.get("Name")] = (pid, pel)
    return out


def ammo_items():
    """Every ammo item: id tag, caliber tag, projectile asset, display name."""
    items = []
    for path in sorted(glob.glob(os.path.join(AMMO_DIR, "**/ID_*.json"), recursive=True)):
        objs = dt.exports(path)
        d = next((o for o in objs if o.get("Type") == "BHInventoryItemDefinition"), None)
        f = next((o for o in objs if o.get("Type") == "WDInventoryFragment_Projectile"), None)
        if not d or not f:
            continue
        p = d["Properties"]
        ctx = [dt.tag(t) for t in p.get("ItemContext", [])]
        cal = next((t for t in ctx if t.startswith("Item.Caliber.")), None)
        asset = re.search(r"'(DA_[\w]+)'", f["Properties"]["ProjectileData"]["ObjectName"]).group(1)
        items.append({"item": dt.tag(p["ItemId"]), "caliber": cal, "asset": asset,
                      "label": p.get("DisplayName", {}).get("SourceString"),
                      "file": os.path.relpath(path, DATA).replace("\\", "/")})
    return items


def resolve_modifier(item_tag):
    """DamagePipeline v2 section 7.9: last name, or last two names of a five-level tag, in the fixed map."""
    parts = item_tag.split(".")
    cand = ".".join(parts[-2:]) if len(parts) == 5 else parts[-1]
    return MOD + cand if cand in MODIFIERS else None


def option_id(item_tag, caliber_key, projectile):
    parts = item_tag.split(".")
    suffix = ".".join(parts[3:])
    if not suffix:
        return "FMJ"
    if suffix == "7mmBuck":
        return "Buckshot"
    if suffix == "RifledSlug":
        return "Slug"
    return suffix


def hit_values(src, ctx, base, wtag, pid, modifier):
    context = ctx + ([modifier] if modifier else []) + [wtag, pid, "Meta.Damage.DamageType.Projectile"]
    used = set()

    def run(loc, piece=None):
        f, _, applied = dt.evaluate(src, context, dt.HIT + loc, [piece] if piece else [])
        used.update(applied)
        return base * f

    raw = {"location": {loc: run(loc) for loc in dt.LOCATIONS},
           "torso_armor": {c: run("Torso.Upper", None if c == "None" else f"Meta.Damage.Armor.{c}") for c in ARMOR_CLASSES},
           "head_armor": {c: run("Head", None if c == "None" else f"Meta.Damage.Helmet.{c}") for c in ARMOR_CLASSES}}
    rounded = {g: {k: round(v, 1) for k, v in d.items()} for g, d in raw.items()}
    return raw, rounded, sorted(used)


def build():
    proj = dt.projectiles()
    files = weapon_files()
    assets = projectile_assets()
    items = ammo_items()
    excluded, weapons_out = [], []
    for name, wtag, cals, keys in sorted(dt.weapons(), key=lambda w: (w[1], w[0])):
        opts = {}
        for it in items:
            if it["caliber"] not in cals or it["asset"] not in assets:
                continue
            pid, pellets = assets[it["asset"]]
            if pid not in proj or not (proj[pid][0] or "").startswith("Meta.Damage.Bullet"):
                continue
            src, ctx, base = proj[pid]
            modifier = resolve_modifier(it["item"])
            oid = option_id(it["item"], it["caliber"], pid)
            note = None
            if modifier is None and oid not in ("FMJ", "Buckshot", "Slug"):
                note = (f"item tag spells '{oid}', which is not in the fixed ammo-modifier map: no modifier, "
                        "behaves as FMJ")
            if oid == "FMJ" and it["caliber"] == "Item.Caliber.12g":
                oid = "Buckshot"
                note = "the generic 12g item (Id.Item.12g) carries the buckshot projectile"
            o = opts.setdefault(oid, {"id": oid, "label": it["label"], "items": [], "modifier_tag": modifier,
                                      "projectile": pid, "base_damage": base, "pellets": pellets, "note": note,
                                      "_cal": it["caliber"].replace("Item.Caliber.", "")})
            o["items"].append(it["item"])
            o["note"] = o["note"] or note
            if oid == "Buckshot" and it["item"].endswith(".7mmBuck"):
                o["label"] = it["label"]
        if not opts:
            excluded.append((name, "no loadable bullet projectile for its calibers: " + ", ".join(
                c.replace("Item.Caliber.", "") for c in cals)))
            continue
        meta = weapon_meta(name, files)
        ammo = []
        for oid in sorted(opts, key=lambda k: OPTION_ORDER.index(k) if k in OPTION_ORDER else 99):
            o = opts[oid]
            src, ctx, base = proj[o["projectile"]]
            raw, rounded, used = hit_values(src, ctx, base, wtag, o["projectile"], o["modifier_tag"])
            o = {k: v for k, v in o.items() if k != "_cal"}
            ammo.append({**o, "items": sorted(o["items"]), "damage": rounded, "damage_raw": raw, "entries_applied": used})
        default = next(a for a in ammo if a["id"] in ("FMJ", "Buckshot"))
        sig = json.dumps([(a["id"], a["damage_raw"]) for a in ammo], sort_keys=True)
        weapons_out.append({
            "id": name, **meta, "weapon_tag": wtag.replace("Meta.Damage.Weapon.", ""),
            "caliber": opts[default["id"]]["_cal"],
            "calibers": [c.replace("Item.Caliber.", "") for c in cals], "base_damage": default["base_damage"],
            "same_damage_as": [], "ammo": ammo, "_sig": sig})
    by_sig = {}
    for w in weapons_out:
        by_sig.setdefault(w.pop("_sig"), []).append(w)
    for group in by_sig.values():
        for w in group:
            w["same_damage_as"] = sorted(x["id"] for x in group if x is not w)
    tree = subprocess.run(["git", "rev-parse", "HEAD:data"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or None
    return {"meta": {
        "generator": "python _tools/weapon_damage_tables.py --json",
        "source_data_tree": tree,
        "source_data_tree_note": "git tree id of data/ when generated; equals `git rev-parse <commit>:data` for any commit with the same data",
        "unit": "health points per hit (per pellet for shotgun rounds; multiply by `pellets`)",
        "assumptions": [
            "hostile alignment; a direct hit at point blank: no distance falloff, no ricochet, no penetration",
            "target is a character outside any vehicle; one hit; no instigator tags (entries needing them are not applied)",
            "ammo type changes the result through the HP/AP rule entries and the ammo scalar against armor (DamagePipeline v2 sections 7.3, 7.9)",
            "armor classes are evaluated for Torso.Upper (torso_armor) and Head (head_armor, helmets); the location columns are for an unarmored target. In the game, vests also cover Torso.Middle and Torso.Lower, SuperHeavy armor also covers Pelvis and Arm.Upper, and Heavy, SuperHeavy and Tank helmets also cover Neck, so those locations take less damage on an armored target than their columns show",
            "damage is rounded to one decimal; damage_raw is unrounded",
            "rpm is RoundsPerMinute from the weapon's stats asset; where the asset omits it (LMG_02, Glock17) the native struct default 600 is used (rpm_source class_default_native; FWDWeaponStats ctor RVA 0x699E6C0, docs/evidence/round39-weapons.md)"],
        "rules": ("Armor piercing does not add damage. Against an unarmored target it deals 0.8 times FMJ. Against armor it cuts the armor reduction by an amount that depends on the bullet's arms class (a per-class scalar), so it overtakes FMJ from Medium armor for rifle calibers and the Deagle (50AE) and from Heavy armor for 9mm, 45ACP and 45Colt. "
                  "Where the arms class gives AP a scalar of 1.0 (the 50Cal SR_04) it never beats FMJ. "
                  "Hollow point doubles unarmored damage, but the HP rule entries (-70, -55, -40 and -40 percent against the armor classes) together with armor scalar 1.5 make it far weaker than FMJ against any armor. "
                  "Tracer and FMJ are identical. Item tags spelled ArmourPiercing resolve to no modifier and behave as FMJ."),
        "locations": dt.LOCATIONS, "armor_classes": ARMOR_CLASSES,
        "ammo_availability": "derived from the ammo items under Content/Items/Resources/Ammo whose Item.Caliber tag is in the weapon's SupportedCaliber",
        "excluded": [{"what": a, "why": b} for a, b in EXCLUDED] + [{"what": a, "why": b} for a, b in excluded if not any(a in what for what, _ in EXCLUDED)]},
        "weapons": weapons_out}


def load():
    return build()


def write_json():
    j = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(j, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(j['weapons'])} weapons, "
          f"{sum(len(w['ammo']) for w in j['weapons'])} weapon x ammo rows")


ALIASES = {"ap": "ArmorPiercing", "hp": "HollowPoint", "fmj": "FMJ", "aptracer": "ArmorPiercing.Tracer"}


def rank(ammo, armor, loc):
    j = build()
    key = {a.lower(): a for a in OPTION_ORDER}
    ammo = ALIASES.get(ammo.lower(), key.get(ammo.lower(), ammo))
    armor = {c.lower(): c for c in ARMOR_CLASSES}.get(armor.lower(), armor)
    short = {"torso": "Torso.Upper", "head": "Head"}
    loc = short.get(loc.lower(), next((x for x in dt.LOCATIONS if x.lower() == loc.lower()), loc))
    if loc not in dt.LOCATIONS or armor not in ARMOR_CLASSES:
        sys.exit(f"location must be one of {dt.LOCATIONS} (or Torso, Head); armor one of {ARMOR_CLASSES}")
    if armor != "None" and loc not in ("Torso.Upper", "Head"):
        sys.exit("armor classes are only evaluated for Torso (Torso.Upper) and Head")
    group = "location" if armor == "None" else ("torso_armor" if loc == "Torso.Upper" else "head_armor")
    sub = loc if group == "location" else armor
    rows = []
    for w in j["weapons"]:
        a = next((x for x in w["ammo"] if x["id"] == ammo), None)
        if a:
            rows.append((a["damage_raw"][group][sub], w, a))
    rows.sort(key=lambda r: (-r[0], r[1]["id"]))
    print(f"{ammo} vs {armor} at {loc}: damage per hit, {len(rows)} weapons "
          f"(shotgun values are per pellet; identical weapons share a rank)")
    print("| Rank | Weapon | Name | Caliber | Damage | Pellets | RPM |")
    print("|---:|---|---|---|---:|---:|---:|")
    rank_no, last = 0, None
    for i, (v, w, a) in enumerate(rows, 1):
        if last is None or round(v, 6) != round(last, 6):
            rank_no = i
        last = v
        rpm = "" if w["rpm"] is None else format(w["rpm"], "g")
        print(f"| {rank_no} | {w['id']} | {w['name']} | {w['caliber']} | {v:.1f} | {a['pellets'] or ''} | {rpm} |")


def table_rows(name, proj):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        dt.ammo_table(name, proj)
    out = {}
    for line in buf.getvalue().splitlines()[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        out[cells[0]] = (cells[1:-1], cells[-1])
    return out


def default_rows(proj):
    run = subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "damage_tables.py")], capture_output=True,
                         encoding="utf-8", check=True)
    out = {}
    for line in run.stdout.splitlines()[2:]:
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) >= 10:
            out[c[0].rstrip("†")] = [re.match(r"[\d.]+", x).group(0) for x in c[4:10]]
    return out


def check():
    j = build()
    proj = dt.projectiles()
    by_id = {w["id"]: w for w in j["weapons"]}
    fails = 0

    def report(ok, msg):
        nonlocal fails
        fails += not ok
        print(("PASS " if ok else "FAIL ") + msg)

    def compare_ammo(name):
        w, tab, bad, n = by_id[name], table_rows(name, proj), [], 0
        for ammo in dt.AMMO:
            opt = next((a for a in w["ammo"] if a["id"] == ammo), None)
            if opt is None:
                continue
            n += 1
            d = opt["damage"]
            mine = [f"{opt['damage_raw']['torso_armor'][c]:.1f}" for c in ARMOR_CLASSES] + \
                   [f"{opt['damage_raw']['head_armor'][c]:.1f}" for c in ARMOR_CLASSES]
            cells, entries = tab[ammo]
            # entries_applied here also covers Neck, Torso.Middle, Arm and Leg, so it may list more entries
            # than the --ammo table (which covers only the torso and head columns): require a superset.
            theirs = {int(x) for x in entries.split(",") if x.strip()}
            if mine != cells or not theirs <= set(opt["entries_applied"]):
                bad.append(ammo)
        return n, bad

    for name in ["M4", "AK74M", "SVDM", "Glock17"]:
        n, bad = compare_ammo(name)
        report(n > 0 and not bad, f"{name} ({by_id[name]['caliber']}): {n} ammo rows match damage_tables.py --ammo {name}"
               + (f"; differs: {bad}" if bad else ""))
    bad_all, n_all = [], 0
    for name in by_id:
        n, bad = compare_ammo(name)
        n_all += n
        bad_all += [f"{name}:{b}" for b in bad]
    report(not bad_all, f"all {len(by_id)} weapons: {n_all} ammo rows (those damage_tables.py can print) match --ammo output"
           + (f"; differs: {bad_all}" if bad_all else ""))
    drows, bad = default_rows(proj), []
    for name, w in by_id.items():
        fm = next((a for a in w["ammo"] if a["id"] in ("FMJ", "Buckshot")), None)
        mine = [f"{fm['damage_raw']['location'][loc]:.1f}" for loc in dt.LOCATIONS]
        if name in drows and mine != drows[name]:
            bad.append(name)
    report(not bad, f"default damage_tables.py per-location table matches the default round's location cells for {len(drows)} weapons"
           + (f"; differs: {bad}" if bad else ""))
    if os.path.exists(SHARED):
        sh = json.load(open(SHARED, encoding="utf-8"))
        diffs = []
        for name, w in by_id.items():
            info = sh["weapons"].get(name)
            if not info:
                diffs.append(f"{name}: not in shared file")
                continue
            theirs = set()
            for c in info["chamberAllowed"]:
                for a in sh["calibers"].get(c, {}).get("ammo", []):
                    theirs.add((a["item"].lower(), a["modifierTag"]))
            mine = {(i.lower(), a["modifier_tag"]) for a in w["ammo"] for i in a["items"]}
            if theirs and theirs != mine:
                diffs.append(f"{name}: only theirs {sorted(theirs - mine)}, only mine {sorted(mine - theirs)}")
        report(not diffs, "ammo availability agrees with E:/r24/shared/ammo-availability.json (items and modifier tags)"
               + ("; " + " | ".join(diffs) if diffs else ""))
    else:
        print("SKIP shared ammo-availability.json not found; availability derived from ammo items")
    print("FAILED" if fails else "ALL PASSED")
    sys.exit(1 if fails else 0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if "--check" in a:
        check()
    elif "--json" in a:
        write_json()
    elif "--rank" in a:
        i = a.index("--rank")
        if len(a) < i + 4:
            sys.exit("usage: --rank AMMO ARMOR LOCATION   e.g. --rank ArmorPiercing Medium Torso")
        rank(*a[i + 1:i + 4])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
