"""Generate the Weapons section of the wiki: _wiki/weapons.md and _wiki/weapons/*.md.

Numbers come from assets/data/*.json and the data pages cited in each article's Sources.
Per-weapon tables, infobox rows and Season 2 bullets are computed here so they match the data.
Short fixed prose (class blurbs, lead sentences) lives in this file.

Run from the repo root:  python _tools/wiki_weapons.py
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wiki_icons  # noqa: E402
import wiki_ttk  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GH = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"
WIKI = os.path.join(ROOT, "_wiki")
OUT = os.path.join(WIKI, "weapons")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def jload(rel):
    return json.loads(read(rel))


loadouts = jload("assets/data/weapon-loadouts.json")
EFFECTS = loadouts["effects"]  # GE name -> list of modifiers
wdamage = {w["id"]: w for w in jload("assets/data/weapon-damage.json")["weapons"]}
falloff_doc = jload("assets/data/weapon-damage-falloff.json")
# Faction signature rifles: the economy settings price them at 0 for one faction (assets/data/price-modifiers.json),
# and the weapon vendor lists them as faction-specific with a buy limit of one.
FACTION_NAMES = {"Meta.Alignment.Faction.Alpha": "Lonestar", "Meta.Alignment.Faction.Bravo": "Valkyra",
                 "Meta.Alignment.Faction.Charlie": "Manticore"}
FACTION_WEAPONS = {}
for _m in jload("assets/data/price-modifiers.json")["modifiers"]:
    if _m["kind"] == "Faction" and _m.get("entityMultipliers") and all(x == 0 for x in _m["entityMultipliers"]):
        for _e in _m["entities"]:
            FACTION_WEAPONS[_e.split("Id.Item.", 1)[1]] = FACTION_NAMES[_m["faction"]]
# muzzle speed, effective range (with its source), chamber and magazine per weapon, from the cooked export
CAP = {w["id"].split("Id.Item.", 1)[1]: w for w in jload("assets/data/weapon-capacity.json")["weapons"]}
# Some capacity rows are keyed by a friendly item name (for example Mosin) while the
# loadout code is the platform code (WEPN_017). Add the platform code as an alias.
for _w in list(CAP.values()):
    _m = re.match(r"DA_(WEPN_\d+)_Stats", _w.get("stats_asset") or "")
    if _m and _m.group(1) not in CAP:
        CAP[_m.group(1)] = _w
falloff = {w["id"]: w for w in falloff_doc["weapons"]}
DIST = falloff_doc["meta"]["distances_m"]
TAG_TEXT = read("content/Wardogs_TagDisplayText_v1.md")
SHOP = read("game-features/Wardogs_WeaponShop_v1.md")
ROSTER = read("content/Wardogs_InfantryWeapons_Stats_v1.md")
S2 = read("season-2-changes/weapons-ammo.md")

# Compound Bow: not a firearm (no caliber, spray pattern or damage table). Its article is
# hand-written (_wiki/weapons/compound-bow.md); the hub gets its row from BOW_ROWS below.
SKIP = {"CombatBow"}
BOW_ROWS = ["| [Compound Bow](weapons/compound-bow.md) | Broadhead Arrow, Rambo Explosive Arrow | 160 m/s | 1.4 s | 1350 |"]

CLASS_NAME = {
    "AR": "Assault rifle", "DMR": "Marksman rifle", "LMG": "Light machine gun",
    "Pistol": "Pistol", "SMG": "Submachine gun", "Shotgun": "Shotgun",
    "Sniper": "Sniper rifle", "Launcher": "Launcher",
}
CLASS_ORDER = ["AR", "DMR", "LMG", "SMG", "Pistol", "Shotgun", "Sniper", "Launcher"]


def class_group(arch):
    """Navbox and hub group name; the order is set in _data/wiki_groups.yml."""
    return CLASS_NAME[arch] + "s"


CLASS_BLURB = {
    "DMR": "Most marksman rifles are semi-automatic.",
    "Shotgun": "Shotguns fire shells rather than single bullets.",
    "Launcher": "Launchers fire explosive rounds rather than bullets.",
}
FIRE_PLAIN = {"Automatic": "fully automatic", "SemiAutomatic": "semi-automatic", "Burst": "burst fire"}
AMMO_NAME = {
    "FMJ": "Standard (FMJ)", "Tracer": "Standard (FMJ) with tracer",
    "HollowPoint": "Flesh Damage (HP)", "HollowPoint.Tracer": "Flesh Damage (HP) with tracer",
    "ArmorPiercing": "Armor Piercing (AP)", "ArmorPiercing.Tracer": "Armor Piercing (AP) with tracer",
    "Buckshot": "Buckshot", "Slug": "Rifled slug",
}
ARMOR_NAME = {"None": "No armor", "Light": "Light", "Medium": "Medium", "Heavy": "Heavy", "SuperHeavy": "Super heavy"}
LOC_NAME = {"Head": "Head", "Neck": "Neck", "Torso.Upper": "Upper torso", "Torso.Middle": "Middle torso",
            "Arm.Upper": "Upper arm", "Leg.Thigh": "Thigh"}
ATTR_PLAIN = [
    "vertical recoil", "horizontal recoil", "ADS zoom", "aim-down-sights time", "spread",
    "accuracy", "weapon length", "minimum zeroing range", "maximum zeroing range", "equip speed",
    "holster speed", "sway stabilisation time", "sway rotation stabilisation", "sway translation stabilisation",
    "aim sway amount", "aim sway speed", "sway while moving (horizontal)", "sway while moving (vertical)",
]
ATTACH_CAT_TEXT = {
    "Muzzle": "Brakes, flash hiders, compensators and suppressors that fit the end of the barrel.",
    "Barrel": "Replacement barrels. Some carry a muzzle slot of their own.",
    "Sight": "Optics and iron sights on top of the weapon. They change zoom and aim time.",
    "Magazine": "Magazines hold the rounds. Some weapons use an internal magazine instead of a swappable one.",
    "Grip": "Pistol grips and foregrips. They change how the weapon is held.",
    "Stock": "Stocks fit at the back of the weapon.",
    "Handguard": "Covers over the barrel. They carry further slots.",
    "Bipod": "Folding legs that mount under the weapon.",
    "Underbarrel": "Mounts on the bottom rail, for grips and bipods.",
}


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fmt_int(v):
    v = float(v)
    if v.is_integer():
        return f"{int(v):,}"
    return f"{v:,.1f}"


def caliber_names():
    names = {}
    for m in re.finditer(r"\| `Item\.Caliber\.([^`]+)` \| ([^|]+) \|", TAG_TEXT):
        key = m.group(1).split(" ")[0]
        names.setdefault(key, m.group(2).strip())
    return names


CAL = caliber_names()


def caliber_display(key):
    if key is None:
        return "None (explosive)"
    return CAL_OVERRIDE.get(key) or CAL.get(key, key)


# Player-facing names for calibers whose display text is a bare code ("50AE", ".50Cal", "12g").
CAL_OVERRIDE = {"50AE": ".50 AE", "50Cal": ".50 Cal", "12g": "12 gauge"}


def caliber_slug(key):
    """Slug of a caliber article (_wiki/ammunition/<slug>.md), written by _tools/wiki_calibers.py."""
    return slugify(caliber_display(key))


def caliber_link(key):
    """Link to a caliber article from a page in _wiki/weapons/."""
    return f"../ammunition/{caliber_slug(key)}.md"


LINK_RE = re.compile(r"\]\(([^)\s#]+\.md)(#[^)\s]*)?\)")


def rebase_links(text, from_dir, to_dir):
    """Rewrite relative .md links written for a page in _wiki/<from_dir>/ so they work from _wiki/<to_dir>/."""
    def fix(m):
        target, anchor = m.group(1), m.group(2) or ""
        if "://" in target or target.startswith("/"):
            return m.group(0)
        absolute = os.path.normpath(os.path.join("_wiki", from_dir, target))
        new = os.path.relpath(absolute, os.path.join("_wiki", to_dir)).replace(os.sep, "/")
        return f"]({new}{anchor})"
    return LINK_RE.sub(fix, text)


# ---- Weapon Shop rows: price, unlock level, default magazine ----
shop_rows = {}
sec = SHOP.split("## 1. Weapon platforms", 1)[1].split("## 2.", 1)[0]
for line in sec.splitlines():
    if not line.startswith("| ") or line.startswith("| Weapon ") or line.startswith("|---"):
        continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) < 10:
        continue
    shop_rows[c[0]] = {
        "price": re.sub(r"\s*\(hidden\)", "", c[5]),
        "unlock": c[6],
        "defaults": c[9],
    }

# ---- Infantry stats roster: rate fallback, keyed by weapon code ----
roster_rate = {}
for line in ROSTER.split("## 2. Raw properties", 1)[0].splitlines():
    if not line.startswith(("| [`DA_", "| `DA_")):
        continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) >= 6:
        code = re.sub(r"^(Id|ID)\.Item\.", "", c[2])
        roster_rate[code] = {"rpm": c[3], "modes": c[4]}

S2_LINES = [l for l in S2.splitlines() if l.startswith("| DA_") or l.startswith("| DT_")]


def s2_for(code):
    pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(code) + r"(?![A-Za-z0-9])")
    out, recoil_rows, falloff_rows = [], 0, 0
    for l in S2_LINES:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 4 or not pat.search(l):
            continue
        m = re.match(r"[A-Za-z]+", c[1])
        prop = m.group(0) if m else c[1]
        old, new = c[2], c[3]
        if prop in ("Name", "Package"):
            continue
        if prop == "Price":
            if old in ("—", "-"):
                out.append(f"Vendor price: {new}")
            else:
                out.append(f"Vendor price: {fmt_int(float(old))} to {fmt_int(float(new))}")
        elif prop == "InitialBulletSpeed":
            out.append(f"Muzzle velocity: {float(old)/100:.0f} m/s to {float(new)/100:.0f} m/s")
        elif prop == "SuppressionMultiplier":
            out.append(f"Suppression effect multiplier: {'none' if old in ('—', '-') else old} to {new}")
        elif prop == "ViewKickMagnitudeMultiplier":
            out.append("View kick multiplier removed" if new in ("—", "-") else f"View kick multiplier: {old} to {new}")
        elif prop == "RecoilPattern":
            recoil_rows += 1
        elif prop == "DistanceDamageFalloffCurve":
            falloff_rows += 1
        else:
            out.append("Aim or handling tuning changed")
    res = []
    for o in out:
        if o not in res:
            res.append(o)
    if recoil_rows:
        res.append("Recoil pattern reworked")
    if falloff_rows:
        res.append("Damage falloff curve reshaped")
    return res


def attach_effects():
    per = {}
    for iid, it in loadouts["items"].items():
        typ = it.get("type") or ""
        if "Attachment" not in typ:
            continue
        cat = typ.split(".")[-1]
        entry = per.setdefault(cat, {"count": 0, "attrs": {}})
        entry["count"] += 1
        for ge in it.get("applied", []):
            for m in EFFECTS.get(ge, []):
                if 0 <= m.get("attr", -1) < len(ATTR_PLAIN):
                    attr = ATTR_PLAIN[m["attr"]]
                    entry["attrs"][attr] = entry["attrs"].get(attr, 0) + 1
    return per


ATTACH = attach_effects()


def code_for(wid):
    return wid[3:] if wid.startswith("ID_") else wid


def page_title(wid):
    if code_for(wid) == "AK74M":
        return "AK74"  # the shop and in-game display name
    return loadouts["items"][wid]["display"]


def magazine_text(defaults):
    m = re.search(r"Magazine: ([^,]+)", defaults or "")
    return m.group(1).strip() if m else "not yet known"


def ammo_names(code):
    w = wdamage.get(code)
    return [AMMO_NAME.get(a["id"], a["id"]) for a in w["ammo"]] if w else []


def ammo_base_names(code):
    w = wdamage.get(code)
    if not w:
        return []
    return [AMMO_NAME.get(a["id"], a["id"]) for a in w["ammo"] if "Tracer" not in a["id"]]


def lock_on(code):
    """Lock-on rule from the weapon's item definition, or None if it can fire freely."""
    import glob
    for path in glob.glob(os.path.join(ROOT, "data/Wardogs/Plugins/GameFeatures/Weapons/**", f"ID_{code}.json"), recursive=True):
        text = read(os.path.relpath(path, ROOT))
        if '"bOnlyFireWhenLockedOn": true' not in text:
            continue
        lock = re.search(r'"TimeToTarget":\s*([\d.]+)', text)
        delay = re.search(r'"FireDelayAfterLock":\s*([\d.]+)', text)
        targets = re.findall(r'"Vehicle\.Variant\.([A-Za-z]+)\.', text)
        return {"lock": lock and float(lock.group(1)), "delay": delay and float(delay.group(1)),
                "air_only": bool(targets) and set(targets) == {"Air"}}
    return None


def stats(wid):
    """Every number a weapon article or hub row shows, in display form."""
    code = code_for(wid)
    it = loadouts["items"][wid]
    dmg = wdamage.get(code)
    fo = falloff.get(code)
    ro = roster_rate.get(code, {"rpm": "", "modes": ""})
    shop = shop_rows.get(it["display"], {"price": "not yet known", "unlock": "not yet known", "defaults": ""})

    if dmg and dmg.get("rpm") is not None:
        rpm = f"{fmt_int(dmg['rpm'])} rounds/min"
    else:
        m = re.match(r"([0-9.]+)", ro["rpm"] or "")
        if m:
            rpm = f"{fmt_int(float(m.group(1)))} rounds/min"
        else:
            rpm = "not yet known"

    if dmg:
        modes = [FIRE_PLAIN.get(x, x) for x in dmg["fire_modes"]]
    elif ro["modes"]:
        modes = [FIRE_PLAIN.get(x.strip(), x.strip()) for x in ro["modes"].split(",")]
    else:
        modes = []
    modes_txt = " and ".join(modes) if modes else "not yet known"
    modes_cap = modes_txt[:1].upper() + modes_txt[1:]

    cal = caliber_display(dmg["caliber"]) if dmg else "None (explosive)"
    cap = CAP.get(code)
    if cap and cap.get("muzzle_m_s"):
        speed = f"{cap['muzzle_m_s']:.0f} m/s"
    else:
        speed = f"{fo['initial_bullet_speed_cm_s']/100:.0f} m/s" if fo and fo.get("initial_bullet_speed_cm_s") else "not yet known"
    if cap and cap.get("effective_range_m") is not None:
        rng = f"{cap['effective_range_m']:.0f} m"
        if cap.get("effective_range_source") == "class_default_native":
            rng += " (game default)"
    else:
        rng = f"{fo['effective_range_m']:.0f} m" if fo and fo.get("effective_range_m") is not None else "not yet known"
    mag = magazine_text(shop["defaults"])
    has_mag = mag != "not yet known"
    mag_row = mag
    if cap and cap.get("magazine"):
        cap_n = cap["magazine"]["capacity"]
        if has_mag and not re.search(r"[0-9]", mag):
            mag_row = f"{mag} ({cap_n} rounds)"
    elif cap and cap.get("rounds_held"):
        # no magazine container: the chamber holds the rounds (launchers, single-shot and internal-magazine weapons)
        n = cap["rounds_held"]
        cal_key = (cap.get("calibers") or [None])[0]
        cal_name = caliber_display(cal_key.split("Item.Caliber.", 1)[1]) if cal_key else cal
        mag = "none (chamber only)"
        has_mag = False
        mag_row = f"None, the chamber holds {n} ({cal_name})"
    return {
        "cls": CLASS_NAME[it["archetype"]], "arch": it["archetype"], "cal": cal,
        "modes": modes_txt, "modes_cap": modes_cap, "rpm": rpm, "speed": speed, "range": rng,
        "mag": mag, "mag_row": mag_row, "has_mag": has_mag, "price": shop["price"], "unlock": shop["unlock"], "defaults": shop["defaults"],
    }


# ---- Recoil and spread (assets/data/weapon-spread-recoil.json, assets/data/spray-patterns.json) ----
SPREAD_DOC = jload("assets/data/weapon-spread-recoil.json")
SPRAY_DOC = jload("assets/data/spray-patterns.json")
SPREAD_BY_ITEM = {}
for _w in SPREAD_DOC["weapons"]:
    _iid = (_w.get("item") or {}).get("id")
    if _iid:
        SPREAD_BY_ITEM.setdefault(_iid, _w)
SPRAY_BY_ITEM = {w["itemAsset"]: w for w in SPRAY_DOC["weapons"] if w.get("itemAsset")}
# row -> [[x, degrees], ...]; x is the speed ratio, 0 = still, 1 = full speed (linear)
SPREAD_CURVES = SPREAD_DOC["spreadCurveTable"]
# radians per unit of WeaponAccuracy.AccuracyValue (pipeline doc, accuracy getter)
RAD_PER_UNIT = {"Milliradians": 0.001, "MinutesOfAngle": 0.000290888}
UNIT_NAME = {"Milliradians": "mrad", "MinutesOfAngle": "MOA"}
# airborne hip fire: InAirHipFireSpread, native default 10 degrees, only GrenadeLauncher sets it (pipeline doc, section 6)
AIR_HIP_DEG = 10.0
RECOIL_VIEWER = "https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html"


def _deg(v):
    return f"{v:.4f}°" if abs(v) < 0.1 else f"{v:.1f}°"


def _metres(v):
    return f"{v:.2f} m" if abs(v) < 1 else f"{v:.1f} m"


def _radius_100m(half_deg):
    return _metres(100 * math.tan(math.radians(half_deg)))


def _curve_at(row, x):
    pts = sorted(SPREAD_CURVES[row], key=lambda p: p[0])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    raise ValueError(f"{row} has no value at x={x}")


def _hip(spread, stance):
    """(still, full speed) cone half-angles in degrees for one stance, or None if the data has no curve for it."""
    spv = spread["item"]["spreadValues"].get(stance)
    if not spv:
        return None
    return spv["value"] * _curve_at(spv["row"], 0.0), spv["value"] * _curve_at(spv["row"], 1.0)


def _path(season, n):
    """Yaw and pitch in degrees after n shots, from the pattern points. Shots past the pattern use the
    mean of the post-pattern range (the same rule as expectedPath in the spray data). Yaw + is right, pitch + is up."""
    pat = [(p["x"], p["y"]) for p in season["pattern"]]
    mean_yaw = sum(season["postPattern"]["yaw"]) / 2
    mean_pitch = sum(season["postPattern"]["pitch"]) / 2
    extra = max(0, n - len(pat))
    x = sum(a for a, _ in pat[:n]) + extra * mean_yaw
    y = sum(b for _, b in pat[:n]) + extra * mean_pitch
    return x, y


def _drift(x):
    if abs(x) < 0.05:
        return "none"
    return f"{abs(x):.1f}° {'right' if x > 0 else 'left'}"


def _season_sentence(spray):
    s1 = spray["seasons"].get("s1")
    s2 = spray["seasons"]["s2"]
    if not s1 or not s1.get("present"):
        return "The Season 1 data has no entry for this weapon, so there is nothing to compare."
    changed = spray.get("changedS1toS2") or []
    if "pattern" not in changed and "viewKickMagnitudeMultiplier" not in changed:
        return "Season 2 did not change the recoil pattern."
    parts = []
    if "pattern" in changed:
        c1, c2 = _path(s1, 10)[1], _path(s2, 10)[1]
        d1, d2 = _path(s1, 30)[1], _path(s2, 30)[1]
        if abs(c1 - c2) < 0.05 and abs(d1 - d2) < 0.05:
            parts.append("Season 2 changed the shape of the recoil pattern, but the climb after 10 and 30 shots is the same")
        else:
            parts.append(f"Season 2 changed the recoil pattern: the climb after 10 shots went from {c1:.1f}° to {c2:.1f}°, "
                         f"and after 30 shots from {d1:.1f}° to {d2:.1f}°")
    if "viewKickMagnitudeMultiplier" in changed:
        parts.append(f"the view kick multiplier went from {s1['viewKickMagnitudeMultiplier']:g} to {s2['viewKickMagnitudeMultiplier']:g}")
    return parts[0] + ("; and " + parts[1] if len(parts) > 1 else "") + "."


def recoil_section(wid, title, multi_pellet=False):
    spread = SPREAD_BY_ITEM.get(wid)
    spray = SPRAY_BY_ITEM.get(wid)
    if spread is None or spray is None:
        raise SystemExit(f"no spread or spray data for {wid}")
    season = spray["seasons"].get("s2")
    if not season or not season.get("present"):
        raise SystemExit(f"no Season 2 spray data for {wid}")

    # Aimed spread: the accuracy value is a full cone angle; the half-angle is half of it.
    acc = spread["fields"]["WeaponAccuracy.AccuracyValue"]
    unit = spread["fields"]["WeaponAccuracy.AccuracyType"]["value"].split("::")[-1]  # "EWDWeaponAccuracyType::Milliradians"
    aimed = 0.5 * acc["value"] * RAD_PER_UNIT[unit] * 180 / math.pi

    out = ["## Recoil and spread", "",
           "Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. "
           "Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. "
           "Every shot also pushes the view up and to the side, following the weapon's recoil pattern.", "",
           "**Spread**", "",
           "| Situation | Still | Moving at full speed |", "|---|---|---|"]
    stand_hip = None
    for stance, label in [("Stand", "Standing, hip fire"), ("Crouch", "Crouching, hip fire"), ("Prone", "Prone, hip fire")]:
        hip = _hip(spread, stance)
        if hip is None:
            out.append(f"| {label} | not in the data | not in the data |")
            continue
        if stance == "Stand":
            stand_hip = hip
        out.append(f"| {label} | {_deg(hip[0])} | {_deg(hip[1])} |")
    out.append(f"| In the air, hip fire | {_deg(AIR_HIP_DEG)} | {_deg(AIR_HIP_DEG)} |")
    out.append(f"| Aimed down sights | {_deg(aimed)} | {_deg(aimed)} |")
    out += ["", "Cone half-angles in degrees: a bullet can land up to that far from the aim point. "]
    if stand_hip:
        out[-1] += (f"At 100 m, standing hip fire has a radius of {_radius_100m(stand_hip[0])} when still and "
                    f"{_radius_100m(stand_hip[1])} at full speed; aimed, it is {_radius_100m(aimed)}. "
                    "Half of the shots land within half that radius.")
    out.append("")
    if acc.get("source") == "native default":
        out.append(f"The data leaves the accuracy value out for this weapon, so the game default of {acc['value']:g} {UNIT_NAME[unit]} is used "
                   "(a full cone angle; the aimed row is half of it, in degrees).")
    else:
        out.append(f"Accuracy is {acc['value']:g} {UNIT_NAME[unit]}, a full cone angle; the aimed row is half of it, in degrees.")
    out += [""]
    if multi_pellet:
        out += ["Buckshot fires several pellets per shot. For a multi-pellet round the hip spread rows above are not used; "
                "the pellet pattern comes from the weapon's shotgun data instead (see [Weapon Spread pipeline](../../pipelines/Wardogs_WeaponSpread_v1.md)). "
                "The hip rows apply to single-projectile ammunition such as the rifled slug.", ""]
    out += ["- The data has no per-shot bloom and no recovery timer: nothing found in the spread data makes firing widen the spread, "
            "and spread changes only with speed, stance, being in the air and aiming. This comes from reading the game files, not from testing in game.",
            "- Hip spread eases toward its new value with a time constant of about 0.04 s (a native default found by static reading).",
            "- The 10° in-air figure is a native default found by static reading; only the grenade launcher's data sets it, to the same 10°.",
            "- At full aim (aim blend exactly 1.0) hip spread is set to zero, so only the aimed row applies. A partly aimed weapon counts as hip fire.",
            "- \"Full speed\" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; between still and that speed the hip spread is a straight line.",
            "- The figures are before attachments, which can change spread (see [Attachments](../attachments.md)).", ""]

    # Recoil
    pat = season["pattern"]
    post = season["postPattern"]
    out += ["**Recoil**", "", "| Measure | Value |", "|---|---|"]
    if pat:
        out.append(f"| Shots in the recoil pattern | {len(pat)} |")
        out.append(f"| Kick on the first shot | {pat[0]['y']:.2f}° up |")
    else:
        out.append("| Shots in the recoil pattern | none, each shot kicks at random |")
        out.append(f"| Random kick per shot | up {min(post['pitch']):.2f}° to {max(post['pitch']):.2f}°, "
                   f"sideways {min(post['yaw']):.2f}° to {max(post['yaw']):.2f}° |")
    y10 = _path(season, 10)[1]
    y30 = _path(season, 30)[1]
    out.append(f"| Climb after 10 shots | {y10:.1f}° up |")
    out.append(f"| Climb after 30 shots | {y30:.1f}° up |")
    out.append(f"| Average climb per shot over 30 shots | {y30 / 30:.2f}° up |")
    out.append(f"| Sideways drift after 30 shots | {_drift(_path(season, 30)[0])} |")
    out.append(f"| Pattern resets after | {season['recoilPatternResetTime_s']:g} s without firing |")
    stance = season["multipliers"]["stance"]
    out.append(f"| Vertical kick crouching / prone, compared with standing | {stance['crouch']:.2f}× / {stance['prone']:.2f}× |")
    mult = season["multipliers"]
    out.append(f"| Default-loadout recoil multiplier, vertical / horizontal | {mult['vertical']:g} / {mult['horizontal']:g} |")
    out.append("")
    note = "Climb and drift figures are computed from the pattern points, before the recoil multiplier. "
    if pat:
        note += (f"The game turns each authored kick by up to {season['randomDeviationDeg']:g}° per shot, so the real sideways drift "
                 f"varies from burst to burst. After shot {len(pat)} each kick is random inside the post-pattern range.")
    else:
        note += "This weapon has no authored pattern, so the climb figures use the middle of its random range."
    out += [note, "", _season_sentence(spray), "",
            f"To see the whole pattern as a picture, open the [Weapon Spray Viewer]({RECOIL_VIEWER}) and pick the {title} in the viewer.", ""]
    return "\n".join(out)


def price_display(code, price):
    """Vendor price as players read it: faction weapons cost 0 once per life for their faction."""
    if code in FACTION_WEAPONS:
        return f"Free ({FACTION_WEAPONS[code]} faction, one per life)"
    return price or "not yet known"


def build_weapon(wid):
    code = code_for(wid)
    title = page_title(wid)
    it = loadouts["items"][wid]
    s = stats(wid)
    dmg = wdamage.get(code)
    fo = falloff.get(code)
    is_launcher = it["archetype"] == "Launcher"
    cls_l = s["cls"].lower()
    art = "an" if cls_l[:1] in "aeiou" else "a"

    # A ("**Band**", "") row is drawn as a group band inside the infobox.
    cal_cell = f"[{s['cal']}]({caliber_link(dmg['caliber'])})" if dmg else s["cal"]
    infobox_rows = [
        ("**General**", ""),
        ("Class", s["cls"]),
        ("Caliber", cal_cell),
        ("Fire modes", s["modes_cap"]),
        ("**Performance**", ""),
        ("Fire rate", s["rpm"]),
        ("Muzzle velocity", s["speed"]),
        ("Effective range", s["range"]),
        ("Standard magazine", s["mag_row"]),
        ("**Availability**", ""),
        ("Vendor price", price_display(code, s["price"])),
        ("Unlock level", s["unlock"] or "not yet known"),
        ("Internal name", code),
    ]
    infobox = [f"| {title} | |", "|---|---|"] + [f"| {a} | {b} |" for a, b in infobox_rows] + ["{: .wiki-infobox }"]

    group_link = f"[{cls_l}](../weapons.md#{slugify(class_group(it['archetype']))})"
    if is_launcher:
        lead = f"The {title} is {art} {group_link} in Wardogs that fires explosive rounds rather than bullets."
        if s["rpm"] != "not yet known":
            lead += f" Its fire rate is {s['rpm']}."
        lk = lock_on(code)
        if lk:
            lead += (f" It fires only while locked on to a target ({lk['lock']:g} s to lock, {lk['delay']:g} s delay)"
                     + (", and it can lock on to helicopters and the airplane only, so it cannot be used against ground vehicles." if lk["air_only"] else "."))
    else:
        lead = (f"The {title} is {art} {group_link} in Wardogs, chambered in {s['cal']}. It fires {s['modes']} at {s['rpm']}.")
        if s["has_mag"]:
            lead += f" Its standard magazine is the {s['mag']}."
    blurb = CLASS_BLURB.get(it["archetype"], "")
    if dmg:
        is_shell = any(a["id"] in ("Buckshot", "Slug") for a in dmg["ammo"])
        kind = "shells" if is_shell else "bullet types"
        blurb = (blurb + " " if blurb else "") + f"It takes the {kind} described on the [Ammunition](../ammunition.md) page: {', '.join(ammo_base_names(code))}. Each has a tracer version."
    if code == "Launcher_04":
        blurb += (" " if blurb else "") + "The muzzle velocity is the launch speed. The rocket has its own thrust after launch, so its speed in flight is higher than this."

    out = [f"# {title}", ""] + infobox + ["", lead, ""] + ([blurb, ""] if blurb else [])

    # Damage
    out += ["## Damage", ""]
    if dmg and dmg["ammo"]:
        base = next((a for a in dmg["ammo"] if a["id"] in ("FMJ", "Buckshot")), dmg["ammo"][0])
        pell = base.get("pellets")
        if pell:
            out += [f"Figures are for {AMMO_NAME[base['id']]} at point blank range, per pellet ({pell} pellets per shot), "
                    "against a character without armor, before any falloff.", ""]
        else:
            out += [f"Figures are for {AMMO_NAME[base['id']]} at point blank range, per hit, against a character without armor.", ""]
        loc = base["damage"]["location"]
        out += ["**By body part (no armor)**", "", "| Body part | Damage |", "|---|---|"]
        for k in ["Head", "Neck", "Torso.Upper", "Torso.Middle", "Arm.Upper", "Leg.Thigh"]:
            if k in loc:
                out.append(f"| {LOC_NAME[k]} | {loc[k]:.1f} |")
        out.append("")
        ta, ha = base["damage"]["torso_armor"], base["damage"]["head_armor"]
        out += ["**Armor (torso and head hits)**", "", "| Armor class | Torso | Head |", "|---|---|---|"]
        for k in ["None", "Light", "Medium", "Heavy", "SuperHeavy"]:
            if k in ta:
                out.append(f"| {ARMOR_NAME[k]} | {ta[k]:.1f} | {ha[k]:.1f} |")
        out.append("")
        if fo:
            tor = fo["ammo"][0]["damage"]["torso"]["None"]
            out += ["**Range falloff (upper torso, no armor)**", "", "| Distance | Damage |", "|---|---|"]
            for d in [0, 50, 100, 200, 300, 400, 600, 800, 1000]:
                v = tor[DIST.index(d)]
                out.append(f"| {d} m | {('not reached' if v is None else f'{v:.1f}')} |")
            out.append("")
        ammo_rows = [a for a in dmg["ammo"] if a["id"] in ("FMJ", "HollowPoint", "ArmorPiercing", "Buckshot", "Slug")]
        if len(ammo_rows) > 1 or ammo_rows[0]["id"] != "FMJ":
            out += ["**Upper torso, no armor, by ammo type**", "", "| Ammo | Damage per hit |", "|---|---|"]
            for a in ammo_rows:
                dv = a["damage"]["location"]["Torso.Upper"]
                p = f" ({a['pellets']} pellets)" if a.get("pellets") else ""
                out.append(f"| {AMMO_NAME[a['id']]} | {dv:.1f}{p} |")
            out.append("")
        out += ["See [Ammunition](../ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.", ""]
    else:
        out += ["The damage data pages do not compute body-part damage for launchers. The data treats the shot as an explosion; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).", ""]

    # Time to kill (after Damage)
    out += wiki_ttk.section_lines(code)
    # Recoil and spread (after Time to kill, before Ammunition)
    out += recoil_section(wid, title, bool(dmg) and any(a.get("pellets") for a in dmg["ammo"])).rstrip("\n").split("\n") + [""]
    # Ammunition
    out += ["## Ammunition", ""]
    if dmg:
        out += [f"Ammo types for this weapon: {', '.join(ammo_names(code))}. See [Ammunition](../ammunition.md).", ""]
    else:
        out += ["Launchers do not use the bullet types on the [Ammunition](../ammunition.md) page.", ""]

    # Attachments
    out += ["## Attachments", ""]
    slots = sorted({sl["tag"].split(".")[-1] for sl in it["slots"] if sl["tag"].split(".")[-1] != "Chamber"})
    out += [f"Slots on this weapon: {', '.join(slots)}. See [Attachments](../attachments.md) for what each part changes.", ""]
    defaults = []
    for sl in it["slots"]:
        d = sl.get("default")
        disp = loadouts["items"].get(d, {}).get("display") if d else None
        if disp:
            disp = re.sub(r"\s+", " ", re.sub(r"\s*\(?WEPN_\d+\)?", " ", disp)).strip()
            defaults.append(f"{sl['tag'].split('.')[-1].lower()} ({disp})")
    if defaults:
        out += ["Default parts: " + ", ".join(defaults) + ".", ""]

    # Cost and unlocking
    out += ["## Cost and unlocking", "",
            f"- Vendor price: {s['price'] or 'not yet known'}. The data pages do not decode the currency, so the price is shown as a plain number.",
            *([f"- Faction weapon: the weapon vendor lists it only for the {FACTION_WEAPONS[code]} faction, at price 0 with a buy limit of one per life (the same limit field the Emergency Resuscitator uses for its one per life), and the economy settings also price it at 0 for that faction. A {FACTION_WEAPONS[code]} player can therefore take it from the vendor for free at level 1 (inferred from the vendor and economy settings; the game was not run)."] if code in FACTION_WEAPONS else []),
            f"- Unlock level: {s['unlock'] or 'not yet known'}.", ""]

    # Season 2 changes
    s2 = s2_for(code)
    out += ["## Season 2 changes", ""]
    if s2:
        out += [f"- {x}" for x in s2] + [""]
    else:
        out += ["The Season 2 changes page lists no changes for this weapon.", ""]

    out += ["## See also", "", "- [Weapons](../weapons.md)", "- [Ammunition](../ammunition.md)", "- [Attachments](../attachments.md)", "- [Choosing Ammo](../guides/choosing-ammo.md)", "- [Ballistics](../game-mechanics/ballistics.md)", "- [Health and Damage](../game-mechanics/health-and-damage.md)", "- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)", ""]

    out += ["## Sources", "",
            "- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): price, unlock level, default magazine",
            "- [Infantry Weapon Stats](../../content/Wardogs_InfantryWeapons_Stats_v1.md): fire rate and fire modes",
            "- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part, armor and falloff numbers",
            "- [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md): spread and recoil inputs",
            "- [Weapon Spread pipeline](../../pipelines/Wardogs_WeaponSpread_v1.md): how the aim cone and hip spread are computed",
            "- [Spray Patterns Gallery](../../game-features/Wardogs_SprayPatterns_v1.md): recoil patterns, Season 1 and Season 2",
            f"- [weapon-spread-recoil.json]({GH}assets/data/weapon-spread-recoil.json): accuracy and hip spread curves",
            f"- [spray-patterns.json]({GH}assets/data/spray-patterns.json): recoil pattern points, Season 1 and Season 2",
            "- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)",
            "- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names",
            f"- [weapon-loadouts.json]({GH}assets/data/weapon-loadouts.json): names, slots and effects",
            f"- [weapon-damage.json]({GH}assets/data/weapon-damage.json): body-part and armor damage",
            f"- [weapon-damage-falloff.json]({GH}assets/data/weapon-damage-falloff.json): falloff curves, also used for the time to kill table",
            f"- [weapon-capacity.json]({GH}assets/data/weapon-capacity.json): muzzle speed, effective range, chamber and magazine",
            f"- [Round 39 weapon evidence]({GH}docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate",
            ""]
    desc = f"The {title} {cls_l}: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
    return title, desc, "\n".join(out)


def front_matter(title, desc, group):
    return f"---\ntitle: \"{title}\"\nparent: \"Weapons\"\ngroup: \"{group}\"\ndescription: \"{desc}\"\n---\n\n"


def ammo_page():
    body = ["# Ammunition", "",
            "Bullet weapons use one of four bullet types, and each has a tracer version that does the same damage with a visible trail. "
            "The shotgun fires two shell types. The type changes how much damage a hit does, most of all against armor.", "",
            "| Type | What it does | Against no armor | Against armor |",
            "|---|---|---|---|",
            "| Standard (FMJ) | The baseline round. | Baseline. | Baseline. |",
            "| Flesh Damage (HP) | Does more damage to unarmored targets. | About double the standard damage. | Much weaker than standard against every armor class. |",
            "| Armor Piercing (AP) | Built to get through armor. | About 0.8 times the standard damage. | Overtakes standard from Medium armor for rifle calibers, and from Heavy armor for pistol and SMG calibers. |",
            "", "Tracer versions of each type do the same damage as their base type. They load into the normal magazines for their caliber, since loading checks the magazine and its caliber, not an ammo tag.", ""]
    rifle = wdamage["A91"]
    body += ["## Torso damage by type: 5.56mm rifle example", "",
             "A-91 chambered in 5.56mm, upper torso hits:", "",
             "| Ammo | No armor | Light | Medium | Heavy | Super heavy |", "|---|---|---|---|---|---|"]
    for aid in ["FMJ", "HollowPoint", "ArmorPiercing"]:
        a = next(x for x in rifle["ammo"] if x["id"] == aid)
        ta = a["damage"]["torso_armor"]
        body.append(f"| {AMMO_NAME[aid]} | {ta['None']:.1f} | {ta['Light']:.1f} | {ta['Medium']:.1f} | {ta['Heavy']:.1f} | {ta['SuperHeavy']:.1f} |")
    body += ["", "Head hits follow the same pattern with higher numbers. Armor covers different body parts by type; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).", ""]
    body += ["## Shotgun shells", ""]
    for a in wdamage["M500"]["ammo"]:
        dv = a["damage"]["location"]["Torso.Upper"]
        p = f" per pellet, {a['pellets']} pellets per shot" if a.get("pellets") else " per hit"
        body.append(f"- {AMMO_NAME[a['id']]}: {dv:.1f} upper torso damage, no armor,{p}.")
    body += ["", "## Which weapons use each caliber", "", "| Caliber | Weapons |", "|---|---|"]
    by_cal = {}
    for wid in loadouts["weapons"]:
        code = code_for(wid)
        if code in SKIP or code not in wdamage:
            continue
        by_cal.setdefault(wdamage[code]["caliber"], []).append(
            f"[{page_title(wid)}]({slugify(page_title(wid))}.md)")
    for key in sorted(by_cal, key=caliber_display):
        body.append(f"| [{caliber_display(key)}]({caliber_link(key)}) | {', '.join(by_cal[key])} |")
    body += ["", "## See also", "",
             "- [Choosing Ammo](../guides/choosing-ammo.md), which round to load against each armor level",
             "- [Ammo Packing](../ammunition/ammo-packing.md), how long loading and unloading magazines takes",
             "- [Armor](../game-mechanics/armor.md)",
             "- [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md)",
             "- [Ballistics](../game-mechanics/ballistics.md)",
             "", "## Sources", "",
             f"- [weapon-damage.json]({GH}assets/data/weapon-damage.json)",
             f"- [ammo-availability.json]({GH}assets/data/ammo-availability.json)",
             "- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md)",
             "- [Ammo Game Feature](../../game-features/Wardogs_GameFeatures_Ammo_v2.md)",
             "- [Round 45 wiki evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-a.md): tracer loading rule",
             ""]
    return "\n".join(body)


ATTACH_ARTICLE = {"Magazine": "magazines.md", "Muzzle": "muzzle-devices.md",
                  "Barrel": "barrels.md", "Stock": "stocks.md",
                  "Grip": "grips.md", "Sight": "sights-and-optics.md",
                  "Handguard": "handguards.md", "Bipod": "bipods.md"}


def attachments_page():
    cats = sorted(ATTACH, key=lambda c: -ATTACH[c]["count"])
    body = ["# Attachments", "",
            "Attachments are parts that fit onto a weapon. While a part is fitted, it changes some of the weapon's numbers. "
            "The table lists each slot type in the data, how many parts it has and what it is for. "
            "The list after it shows which numbers the parts in each category change, and how many parts change each one. Each category name links to its own article.", "",
            "| Category | Parts | What it is |", "|---|---|---|"]
    for cat in cats:
        label = f"[{cat}](attachments/{ATTACH_ARTICLE[cat]})" if cat in ATTACH_ARTICLE else cat
        body.append(f"| {label} | {ATTACH[cat]['count']} | {ATTACH_CAT_TEXT.get(cat, 'Other slot type.')} |")
    body += ["", "## What the parts change", ""]
    for cat in cats:
        attrs = ATTACH[cat]["attrs"]
        if attrs:
            effects = ", ".join(f"{k} ({v} modifier{'s' if v != 1 else ''})" for k, v in sorted(attrs.items(), key=lambda kv: -kv[1]))
            body.append(f"- **{cat}**: {effects}.")
        else:
            body.append(f"- **{cat}**: no effect entries in the loadout data.")
    body += ["", "Each weapon article lists its own slots and default parts under its Attachments section.", "",
             "## See also", "",
             "- [Choosing Attachments](guides/choosing-attachments.md), which part to pick in each category and the cheapest useful picks",
             "- [Spread and Recoil](game-mechanics/spread-and-recoil.md), where bipods, muzzle devices and foregrips change spread",
             "- [Underbarrel Grenade Launcher (test item)](attachments/underbarrel-grenade-launcher.md), a 40 mm launcher attachment named as a test item in the data",
             "- [Weapons](weapons.md)",
             "",
             "## Sources", "",
             f"- [weapon-loadouts.json]({GH}assets/data/weapon-loadouts.json): slot, part and effect data",
             "- [Attachments and Platforms](../game-features/Wardogs_AttachmentsPlatforms_v1.md)",
             "- [Weapon Shop and Parts](../game-features/Wardogs_WeaponShop_v1.md)",
             ""]
    return "\n".join(body)


def hub_page(sections):
    head = ("---\ntitle: Weapons\nnav_order: 1\nwiki_hub: true\nhas_children: true\n"
            "description: \"Every player weapon, the ammunition they use and the attachments that change them.\"\n---\n\n")
    body = ["# Weapons", "",
            "Every rifle, marksman rifle, light machine gun, pistol, submachine gun, shotgun, sniper rifle, launcher and bow "
            "that a player can get, grouped by class. Each name links to its article; click a column heading to sort. "
            "[Ammunition](ammunition.md) and [Attachments](attachments.md) have their own sections. "
            "To compare weapons side by side, see the [Weapon Comparison](weapons/weapon-comparison.md) table of damage, shots to kill and recoil.", ""]
    for arch in CLASS_ORDER:
        if sections.get(arch):
            if arch == "Launcher":
                head_rows = ["| Weapon | Muzzle velocity | Effective range | Fire rate | Standard magazine | Vendor price |",
                             "|---|---:|---:|---:|---|---:|"]
            else:
                head_rows = ["| Weapon | Caliber | Fire rate | Standard magazine | Vendor price |",
                             "|---|---|---:|---|---:|"]
            body += [f"## {class_group(arch)}", ""] + head_rows + sections[arch] + [""]
    body += ["## Bows", "", "| Weapon | Ammunition | Arrow speed | Full draw | Item shop price |", "|---|---|---:|---:|---:|"] + BOW_ROWS + [""]
    return head + "\n".join(body)


def comparison_page():
    rows = []
    for arch in CLASS_ORDER:
        for wid in loadouts["weapons"]:
            code = code_for(wid)
            if code in SKIP or loadouts["items"][wid]["archetype"] != arch:
                continue
            c = wiki_ttk.comparison_cells(code)
            if c is None:
                continue
            s = stats(wid)
            title = page_title(wid)
            cap = CAP.get(code) or {}
            mag = (cap.get("magazine") or {}).get("capacity") or cap.get("rounds_held")
            sp = SPRAY_BY_ITEM.get(wid)
            season = sp["seasons"].get("s2") if sp else None
            climb = f"{_path(season, 10)[1]:.1f}" if season and season.get("present") else "not yet known"
            star = "*" if c["beyond100"] else ""

            def kc(k):
                return (f"{k[0]}{star}", f"{k[1]:.2f}{star}") if k else ("not reached", "not reached")
            n0, t0 = kc(c["none"])
            n3, t3 = kc(c["l3"])
            cells = [f"[{title}]({slugify(title)}.md)", CLASS_NAME[arch], s["cal"], fmt_int(wdamage[code]["rpm"]),
                     str(mag) if mag is not None else "not yet known", s["price"] or "not yet known",
                     f"{c['dmg10']:.1f}", n0, t0, n3, t3, climb]
            rows.append("| " + " | ".join(cells) + " |")
    head = ("---\ntitle: \"Weapon Comparison\"\nparent: \"Weapons\"\ngroup: \"Reference\"\n"
            "description: \"Every weapon in one sortable table: damage, shots and time to kill, fire rate, magazine, price and recoil.\"\n---\n\n")
    body = ["# Weapon Comparison", "",
            "One table for every weapon that fires bullets or shells. Click a column heading to sort. "
            "Each weapon links to its article, which has the full damage, time to kill and recoil sections. Launchers are left out because the data treats their shots as explosions.", "",
            "| Weapon | Class | Caliber | Fire rate (rounds/min) | Magazine (rounds) | Price | Upper-torso damage at 10 m (HP) | Shots, no armor, 100 m | TTK, no armor, 100 m (s) | Shots, Level 3 vest, 100 m | TTK, Level 3 vest, 100 m (s) | Recoil climb after 10 shots (degrees) |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    body += rows
    body += ["", "**How to read it**", "",
             "- Damage and kill figures use the standard bullet (FMJ), or buckshot for shotguns, on upper-torso hits. Shotgun damage is the sum of all 8 pellets and assumes every pellet hits.",
             "- Shots to kill are for a character with 100 HP: 100 divided by the damage per hit, rounded up. Time to kill (TTK) is (shots - 1) x 60 / fire rate, because the first shot fires at 0 s.",
             "- A * marks a 100 m figure that is beyond the weapon's effective range, where damage falls with distance. Damage at 100 m uses the range falloff curve.",
             "- A Level 3 vest cuts upper-torso damage by 50%. See [Body Armor](../equipment/body-armor.md) for all four levels.",
             "- Recoil climb is how far the view rises over the first 10 shots of the Season 2 pattern, before attachments. See [Spread and Recoil](../game-mechanics/spread-and-recoil.md).",
             "- Everything is derived from game data. It assumes every shot hits and armor stays intact, and it ignores reload, spread and recoil. Real fights take longer.", "",
             "## See also", "", "- [Weapons](../weapons.md)", "- [Ammunition](../ammunition.md)", "- [Choosing Ammo](../guides/choosing-ammo.md)", "- [Health and Damage](../game-mechanics/health-and-damage.md)", "",
             "## Sources", "",
             "- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part, armor and falloff numbers",
             "- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): price",
             "- [Spray Patterns Gallery](../../game-features/Wardogs_SprayPatterns_v1.md): recoil patterns",
             f"- [weapon-damage.json]({GH}assets/data/weapon-damage.json)",
             f"- [weapon-damage-falloff.json]({GH}assets/data/weapon-damage-falloff.json)",
             f"- [weapon-capacity.json]({GH}assets/data/weapon-capacity.json): magazine and effective range",
             f"- [spray-patterns.json]({GH}assets/data/spray-patterns.json)",
             f"- [wiki_ttk.py]({GH}_tools/wiki_ttk.py): how the shots and times are computed",
             ""]
    return head + "\n".join(body)


def main():
    os.makedirs(OUT, exist_ok=True)
    sections, count = {}, 0
    for wid in loadouts["weapons"]:
        code = code_for(wid)
        if code in SKIP:
            continue
        title, desc, text = build_weapon(wid)
        slug = slugify(title)
        arch = loadouts["items"][wid]["archetype"]
        page = os.path.join(OUT, slug + ".md")
        full = wiki_icons.inject(front_matter(title, desc, class_group(arch)) + text, page)[0]  # icon row
        with open(page, "w", encoding="utf-8", newline="\n") as f:
            f.write(full)
        s = stats(wid)
        if arch == "Launcher":
            row = (f"| [{title}](weapons/{slug}.md) | {s['speed']} | {s['range']} | {s['rpm']} | {s['mag_row']} "
                   f"| {price_display(code, s['price'])} |")
        else:
            row = (f"| [{title}](weapons/{slug}.md) | {s['cal']} | {s['rpm']} | {s['mag_row']} | {price_display(code, s['price'])} |")
        sections.setdefault(arch, []).append(row)
        count += 1
    ammo = ("---\ntitle: Ammunition\nnav_order: 1.2\nwiki_hub: true\nhas_children: true\n"
            "redirect_from: [\"/wiki/weapons/ammunition/\"]\n"
            "description: \"Bullet and shell types, what each does to armor and flesh, and which weapons use them.\"\n---\n\n") + rebase_links(ammo_page(), "weapons", "")
    with open(os.path.join(WIKI, "ammunition.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(wiki_icons.add_icon_columns(ammo, os.path.join(WIKI, "ammunition.md")))
    att = ("---\ntitle: Attachments\nnav_order: 1.5\nwiki_hub: true\nhas_children: true\n"
           "redirect_from: [\"/wiki/weapons/attachments/\"]\n"
           "description: \"The parts that fit on weapons, the slots they go into and what each category changes.\"\n---\n\n") + attachments_page()
    with open(os.path.join(WIKI, "attachments.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(att)
    with open(os.path.join(OUT, "weapon-comparison.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(comparison_page())
    with open(os.path.join(WIKI, "weapons.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(wiki_icons.add_icon_columns(hub_page(sections), os.path.join(WIKI, "weapons.md")))  # thumbnail column
    print(f"wrote {count} weapon articles, ammunition, attachments and the hub")


if __name__ == "__main__":
    main()
