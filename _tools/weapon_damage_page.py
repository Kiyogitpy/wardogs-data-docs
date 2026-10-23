"""Generated tables for game-features/Wardogs_WeaponDamage_v1.md, read from assets/data/weapon-damage.json.

Every table is one marked block; the prose around them is hand-written:

    <!-- weapon_damage_tables MODE -->  ...  <!-- /weapon_damage_tables -->

    python _tools/weapon_damage_page.py --write   # refresh every block in place (idempotent)
    python _tools/weapon_damage_page.py MODE      # print one block: rank_ap_torso, rank_ap_head, rank_hp_torso,
                                                  # rank_hp_head, rank_fmj_torso, rank_fmj_head, all, location

The JSON is read as it is; run `python _tools/weapon_damage_tables.py --json` first if the game data changed.
Ranking rules: damage is the unrounded value (damage_raw), ties are equal after rounding to 6 decimals, identical
weapons share one rank and are named together, the top 5 distinct values are shown per column. Shotgun values
are per pellet.
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


def ranked_groups(j, ammo_id, group, sub):
    """Distinct damage values, highest first: [(value, [weapon, ...])], at most TOP entries."""
    vals = []
    for w in j["weapons"]:
        a = ammo_of(w, ammo_id)
        if a:
            vals.append((a["damage_raw"][group][sub], w))
    vals.sort(key=lambda r: (-r[0], r[1]["id"]))
    groups, last = [], None
    for v, w in vals:
        key = round(v, 6)
        if last is None or key != last:
            groups.append((v, []))
            last = key
        groups[-1][1].append(w)
    return groups[:TOP]


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


MODES = {}
for _s in ("ap", "hp", "fmj"):
    for _l in ("torso", "head"):
        MODES[f"rank_{_s}_{_l}"] = (lambda s, l: (lambda j: rank_block(j, s, l)))(_s, _l)
MODES["all"] = all_block
MODES["location"] = location_block


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
