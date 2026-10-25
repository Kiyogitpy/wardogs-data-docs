"""Shots to kill and time to kill for every weapon, from the damage and falloff data.

Used by _tools/wiki_weapons.py (the "Time to kill" section of each weapon article and the
Weapon Comparison page). It has no output of its own except:

  python -I _tools/wiki_ttk.py --check          verify the written wiki files match the data
  python -I _tools/wiki_ttk.py --table CODE     print the full 5-range matrix for one weapon (e.g. M4)

Model: 100 HP, every shot hits the stated part, no reload, spread or recoil.
Damage per hit at distance d comes from assets/data/weapon-damage-falloff.json (grid 0, 25, 50, 100, 150,
200, 300 m ...; distance is measured from the muzzle). 10 m lies between the 0 m and 25 m grid points and is
interpolated linearly, which is exact because the falloff curve is linear between its keys and flat early on.
Shots = ceil(100 / damage). TTK = (shots - 1) x 60 / rpm.
"""
import json
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HP = 100.0
RANGES = [10, 50, 100, 200, 300]
ARMOR_LEVELS = [("None", None), ("Light", 1), ("Medium", 2), ("Heavy", 3), ("SuperHeavy", 4)]
AMMO_LABEL = {"FMJ": "Standard (FMJ)", "ArmorPiercing": "Armor Piercing (AP)", "Buckshot": "Buckshot", "Slug": "Rifled slug"}


def _jload(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


_DMG = {w["id"]: w for w in _jload("assets/data/weapon-damage.json")["weapons"]}
_FALL_DOC = _jload("assets/data/weapon-damage-falloff.json")
_FALL = {w["id"]: w for w in _FALL_DOC["weapons"]}
_DIST = _FALL_DOC["meta"]["distances_m"]
_CAP = {w["id"].split("Id.Item.", 1)[1]: w for w in _jload("assets/data/weapon-capacity.json")["weapons"]}


def has_data(code):
    return code in _DMG and code in _FALL


def ammo_ids(code):
    """Standard ammo first, then the second type (AP or slug); tracers and hollow points are left out."""
    ids = [a["id"] for a in _DMG[code]["ammo"]]
    out = [a for a in ("FMJ", "Buckshot") if a in ids][:1]
    out += [a for a in ("ArmorPiercing", "Slug") if a in ids]
    return out


def pellets(code, ammo):
    a = next(x for x in _DMG[code]["ammo"] if x["id"] == ammo)
    return a.get("pellets") or 1


def effective_range(code):
    cap = _CAP.get(code)
    if cap and cap.get("effective_range_m") is not None:
        return cap["effective_range_m"]
    return None


def rpm(code):
    return _DMG[code]["rpm"]


def damage_at(code, ammo, part, armor, d):
    """HP per shot (all pellets) at distance d metres, or None if the projectile does not reach d."""
    a = next(x for x in _FALL[code]["ammo"] if x["id"] == ammo)
    series = a["damage"][part][armor]
    if d in _DIST:
        v = series[_DIST.index(d)]
    else:
        lo = max(x for x in _DIST if x < d)
        hi = min(x for x in _DIST if x > d)
        v0, v1 = series[_DIST.index(lo)], series[_DIST.index(hi)]
        if v0 is None or v1 is None:
            return None
        v = v0 + (v1 - v0) * (d - lo) / (hi - lo)
    return None if v is None else v * pellets(code, ammo)


def kill(code, ammo, part, armor, d):
    """(shots, ttk seconds) or None when the shot does not reach or does no damage."""
    dmg = damage_at(code, ammo, part, armor, d)
    if dmg is None or dmg <= 0:
        return None
    shots = math.ceil(HP / dmg - 1e-9)
    return shots, (shots - 1) * 60.0 / rpm(code)


def cell(code, ammo, part, armor, d):
    k = kill(code, ammo, part, armor, d)
    er = effective_range(code)
    mark = "*" if er is not None and d > er else ""
    if k is None:
        return "not reached" + mark
    n, t = k
    return f"{n} {'shot' if n == 1 else 'shots'}, {t:.2f} s{mark}"


def _armor_name(level, part):
    if level is None:
        return "No armor" if part == "torso" else "No helmet"
    return f"Level {level} " + ("vest" if part == "torso" else "helmet")


def _row_label(level, part):
    if level is None:
        return "No armor" if part == "torso" else "No helmet"
    slug = "armor" if part == "torso" else "helmet"
    return f"[Level {level} {'vest' if part == 'torso' else 'helmet'}](../equipment/level-{level}-{slug}.md)"


def section_lines(code):
    """The "## Time to kill" section as written in a weapon article (links relative to _wiki/weapons/)."""
    out = ["## Time to kill", ""]
    if not has_data(code):
        out += ["Time to kill is not computed for launchers: the data treats the shot as an explosion.", ""]
        return out
    ids = ammo_ids(code)
    n_pel = pellets(code, ids[0])
    out += ["Shots and time to kill (TTK) against a character with 100 HP. TTK runs from the first shot to the killing shot, "
            "so it is (shots - 1) x 60 / fire rate: one shot kills in 0 s.", ""]
    for ammo in ids:
        label = AMMO_LABEL[ammo]
        out += [f"**Upper torso hits, {label}**", "", "| Vest | 10 m | 100 m | 300 m |", "|---|---|---|---|"]
        for armor, level in ARMOR_LEVELS:
            cells = [cell(code, ammo, "torso", armor, d) for d in (10, 100, 300)]
            out.append(f"| {_row_label(level, 'torso')} | " + " | ".join(cells) + " |")
        out += ["", f"**Head hits, {label}**", ""]
        for d in (10, 100):
            parts = [f"{_armor_name(level, 'head').lower() if level is None else _armor_name(level, 'head')}: "
                     f"{cell(code, ammo, 'head', armor, d)}" for armor, level in ARMOR_LEVELS]
            out.append(f"- At {d} m, " + "; ".join(parts) + ".")
        out.append("")
    notes = ["Derived from the game data, not from play testing. It assumes every shot hits the stated part and that armor stays intact, and it ignores reload time, "
             "spread and recoil, so real fights take longer. Damage after the first 10 m comes from the range falloff curve."]
    if n_pel > 1:
        notes.append(f"Shotgun figures add up all {n_pel} pellets of a shell and assume every pellet hits; at range the pellets spread out and some will miss.")
    er = effective_range(code)
    if er is not None:
        notes.append(f"A * marks a distance beyond the weapon's effective range of {er:.0f} m, where damage falls with distance.")
    out += [" ".join(notes), ""]
    return out


def comparison_cells(code):
    """Numbers for the comparison table, or None for launchers. Standard ammo (FMJ or buckshot)."""
    if not has_data(code):
        return None
    ammo = ammo_ids(code)[0]
    dm = damage_at(code, ammo, "torso", "None", 10)
    r = {"dmg10": dm, "ammo": ammo, "pellets": pellets(code, ammo)}
    for key, armor in (("none", "None"), ("l3", "Heavy")):
        r[key] = kill(code, ammo, "torso", armor, 100)
    r["beyond100"] = effective_range(code) is not None and 100 > effective_range(code)
    return r


def check():
    """Verify that every weapon article and the comparison page on disk match what the data gives."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import wiki_weapons as ww
    bad = []
    for wid in ww.loadouts["weapons"]:
        code = ww.code_for(wid)
        if code in ww.SKIP:
            continue
        title = ww.page_title(wid)
        path = os.path.join(ww.OUT, ww.slugify(title) + ".md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        block = "\n".join(section_lines(code))
        if block not in text:
            bad.append(f"{path}: Time to kill section is out of date")
        if has_data(code):
            for ammo in ammo_ids(code):
                for armor, _ in ARMOR_LEVELS:
                    for part in ("torso", "head"):
                        for d in RANGES:
                            k = kill(code, ammo, part, armor, d)
                            if k and k[0] * damage_at(code, ammo, part, armor, d) < HP - 1e-6:
                                bad.append(f"{code} {ammo} {part} {armor} {d} m: {k[0]} shots do not reach {HP:g} HP")
                            if k and k[0] > 1 and (k[0] - 1) * damage_at(code, ammo, part, armor, d) >= HP:
                                bad.append(f"{code} {ammo} {part} {armor} {d} m: {k[0] - 1} shots already kill")
    cpath = os.path.join(ww.OUT, "weapon-comparison.md")
    try:
        with open(cpath, encoding="utf-8") as f:
            if f.read() != ww.comparison_page():
                bad.append(f"{cpath}: out of date")
    except FileNotFoundError:
        bad.append(f"{cpath}: missing")
    hub = os.path.join(ww.WIKI, "weapons.md")
    with open(hub, encoding="utf-8") as f:
        if "weapon-comparison.md" not in f.read():
            bad.append(f"{hub}: no link to the comparison page")
    return bad


def main(argv):
    if "--check" in argv:
        bad = check()
        for b in bad:
            print("FAIL", b)
        print("ttk check: " + ("FAILED" if bad else "ok"))
        return 1 if bad else 0
    if "--table" in argv:
        code = argv[argv.index("--table") + 1]
        for ammo in ammo_ids(code):
            for part in ("torso", "head"):
                print(f"{code} {ammo} {part}  (rpm {rpm(code):g}, effective range {effective_range(code)})")
                for armor, level in ARMOR_LEVELS:
                    print(f"  {str(level or '-'):>2} " + " | ".join(f"{d} m: {cell(code, ammo, part, armor, d)}" for d in RANGES))
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
