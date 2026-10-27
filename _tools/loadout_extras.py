"""Extra data for the Weapon Loadout Calculator: role unlock gates, reticles, icons and ballistics.

Writes assets/data/loadout-extras.json, read by assets/js/loadout-calculator.js next to
weapon-loadouts.json. Every value is copied from data already in this repository:

  unlocks    DT_MetaTree_Roles: per calculator item id, {role: [MinLevel, cash cost]} for each role tree
             that has the item as a node. Items in no tree are not gated by a role level.
  reticles   per sight item: "scope" = the through-the-scope HUD reticle (assets/data/scope-reticles.json,
             _tools/scope_reticles.py) and "entries" = the lens reticle per sight entry (item-icons.json keys
             "<ItemId tag>.<sight entry>", the Gunsmith default reticles).
  icons      assets/data/item-icons.json vendor (else inventory) icon per item.
  ballistics weapon-damage-locations.json (point-blank damage per hit location and armor class) and
             weapon-damage-falloff.json (curve x speed scale per distance; null where the shot does not
             reach), plus rpm from weapon-damage.json. Damage at d = location damage x factor[d], the same
             linear assumption wiki_ttk.py and damage_tables.py --falloff make.

  python -I _tools/loadout_extras.py          write the file
  python -I _tools/loadout_extras.py --check  exit 1 if the written file is stale
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "data", "loadout-extras.json")
TREE = os.path.join(ROOT, "data", "Wardogs", "Content", "Meta", "CharacterSkills", "DT_MetaTree_Roles.json")


def jload(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def export_json(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    return json.loads(s[s.index("{"):])


def round6(x):
    return None if x is None else round(x, 6)


def build():
    loadouts = jload("assets/data/weapon-loadouts.json")
    items = loadouts["items"]
    by_tag = {v["itemId"].lower(): k for k, v in items.items() if v.get("itemId")}

    unlocks, roles = {}, []
    for role, row in export_json(TREE)["Rows"].items():
        name = role.rsplit(".", 1)[-1]
        hit = False
        for node in row["Nodes"]:
            item_id = by_tag.get(node["ID"]["TagName"].lower())
            if not item_id:
                continue
            level = node["LevelsData"][0]
            conds = level["Prerequisites"]["QueryDefinition"]["SharedDefinition"]["Conditions"]["Structs"]
            min_level = min((c.get("MinLevel", 0) for c in conds), default=0)
            cost = sum(c["Value"] for c in level.get("Cost", []) if c["Key"]["TagName"].endswith("Currency.Cash"))
            unlocks.setdefault(item_id, {})[name] = [min_level, cost]
            hit = True
        if hit:
            roles.append(name)

    icons_doc = jload("assets/data/item-icons.json")["items"]
    scope_doc = {k.lower(): v for k, v in jload("assets/data/scope-reticles.json")["items"].items()}
    icons, reticles = {}, {}
    for item_id, it in items.items():
        tag = it.get("itemId")
        if not tag:
            continue
        rec = icons_doc.get(tag) or next((v for k, v in icons_doc.items() if k.lower() == tag.lower()), None)
        if rec:
            ref = rec.get("vendor") or rec.get("inventory")
            if ref and ref.get("png"):
                icons[item_id] = ref["png"]
        rec = {}
        if tag.lower() in scope_doc:
            rec["scope"] = scope_doc[tag.lower()]["png"]
        for entry, _ in it.get("sights") or []:
            r = icons_doc.get(f"{tag}.{entry}")
            if r and (r.get("inventory") or {}).get("png"):
                rec.setdefault("entries", {})[entry] = r["inventory"]["png"]
        if rec:
            reticles[item_id] = rec

    dmg = jload("assets/data/weapon-damage-locations.json")
    fall = jload("assets/data/weapon-damage-falloff.json")
    rpm = {w["id"]: w["rpm"] for w in jload("assets/data/weapon-damage.json")["weapons"]}
    fall_by = {w["id"]: w for w in fall["weapons"]}
    ballistics = {}
    for w in dmg["weapons"]:
        # damage tables use the definition's short name (WEPN_017 -> ID_WEPN_017, whose tag is Id.Item.Mosin)
        item_id = "ID_" + w["id"] if "ID_" + w["id"] in items else by_tag.get(("Id.Item." + w["id"]).lower())
        f = fall_by.get(w["id"])
        if not item_id or not f:
            continue
        f_ammo = {a["id"]: a for a in f["ammo"]}
        ammo = []
        for a in w["ammo"]:
            fa = f_ammo.get(a["id"])
            factor = None
            if fa:
                factor = [None if s == "not_reached_in_model" else round6(c * (sc if sc is not None else 1.0))
                          for c, sc, s in zip(fa["curve_multiplier"], fa["speed_scale"], fa["status"])]
            ammo.append({"id": a["id"], "label": a["label"], "pellets": a.get("pellets") or 1,
                         "damage": a["damage_raw"], "factor": factor})
        ballistics[item_id] = {"rpm": rpm.get(w["id"]), "effectiveRange": f.get("effective_range_m"), "ammo": ammo}

    return {
        "meta": {
            "generator": "python -I _tools/loadout_extras.py",
            "hp": 100.0,
            "distances": fall["meta"]["distances_m"],
            "locations": dmg["meta"]["locations"],
            "armorKind": {k: v["kind"] for k, v in dmg["meta"]["armor_effect"].items()},
            "roles": roles,
            "notes": [
                "unlocks: {role: [MinLevel, cash cost]} from DT_MetaTree_Roles; items in no role tree are not level-gated",
                "damage: point-blank HP per hit (per pellet) by location and armor class; a location missing an armor "
                "class is not covered by it and takes the None value",
                "factor: falloff curve x speed scale per distance; null where the modelled shot does not reach",
            ],
        },
        "unlocks": unlocks,
        "reticles": reticles,
        "icons": icons,
        "ballistics": ballistics,
    }


def main():
    text = json.dumps(build(), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
    if "--check" in sys.argv:
        old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if old != text:
            sys.exit("assets/data/loadout-extras.json is stale: run python -I _tools/loadout_extras.py")
        print("loadout-extras.json is current")
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    d = json.loads(text)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(d['unlocks'])} gated items, {len(d['reticles'])} sights with "
          f"reticles, {len(d['icons'])} icons, {len(d['ballistics'])} weapons with ballistics; roles {d['meta']['roles']}")


if __name__ == "__main__":
    main()
