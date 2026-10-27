"""Lootable container spawn lists (round 85, V4-01), rebuilt from data/ into assets/data/loot-tables.json
and the generated tables of game-features/Wardogs_LootContainers_v1.md.

Reads DT_LootableDataTable (52 rows) and DT_LootableDataTable_VIPEscort_01 (2 rows). For each row:
the row settings and every ItemsToSpawn entry with its weight, the chance (weight / sum of weights),
and its sub-items. Display names come from DT_EntityData_UI_Items, else assets/data/loadout-builder.json,
else the name of the item's ID_ asset (FALLBACK below).
The selection rules (chance roll, weighted pick, previous-item exclusion) are from the native reads in
docs/evidence/round59-open-questions.md section 4; the chance column here is Derived from them.

    python -I _tools/loot_tables.py            # rewrite the JSON and the marker blocks
    python -I _tools/loot_tables.py --check    # exit 1 if either is stale
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data", "Wardogs")
TABLES = [
    ("DT_LootableDataTable", "Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json"),
    ("DT_LootableDataTable_VIPEscort_01", "Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json"),
]
NAMES = os.path.join(D, "Content/UI/Data/Entities/DT_EntityData_UI_Items.json")
OUT = os.path.join(ROOT, "assets", "data", "loot-tables.json")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_LootContainers_v1.md")

# Items with no UI or shop name row (filled in below after checking the ID_ assets).
FALLBACK = {
    # WEPN_023 has no display name of its own (its UI row is the generic "Submachine Gun"); the loot row is Lootable.PP19.
    "id.item.wepn_023": "Submachine Gun (WEPN_023, row PP19)",
    # no UI or shop row exists for the cheap defibrillator; named from its tag
    "id.item.defibrillator.cheap": "Cheap Defibrillator",
}


def load(path):
    t = open(path, encoding="utf-8").read()
    return json.loads(t[t.index("{"):])


def text(v):
    if not isinstance(v, dict):
        return None
    return v.get("LocalizedString") or v.get("SourceString") or v.get("CultureInvariantString")


def name_map():
    m = {}
    for k, v in load(NAMES)["Rows"].items():
        n = text(v.get("FriendlyName"))
        if n:
            m[k.lower()] = n
    for path in glob.glob(os.path.join(D, "Plugins", "GameFeatures", "**", "DT_EntityData_UI_Ext_*.json"), recursive=True):
        try:
            rows = load(path).get("Rows", {})
        except ValueError:
            continue
        for k, v in rows.items():
            n = text(v.get("FriendlyName")) if isinstance(v, dict) else None
            if n:
                m.setdefault(k.lower(), n)
    lb = json.load(open(os.path.join(ROOT, "assets", "data", "loadout-builder.json"), encoding="utf-8"))["items"]
    for v in lb.values():
        m.setdefault(v["itemId"].lower(), v["name"])
    return m


NAMES_MAP = name_map()


def nm(tag):
    return NAMES_MAP.get(tag.lower()) or FALLBACK.get(tag.lower()) or tag


def num(x):
    return "%g" % x


def chance_roll(sc):
    """Chance one spawn roll passes (AWDLootable roll 0x855B6A0, round 59)."""
    if sc <= 0:
        return 0.0
    n = int(200 / sc + 0.5) >> 1
    return 1.0 / max(n, 1)


def build():
    out = {"tables": {}}
    for tname, rel in TABLES:
        rows = load(os.path.join(D, rel))["Rows"]
        res = {}
        for rid, row in rows.items():
            L = row["LootableData"]
            ents = L["ItemsToSpawn"]
            tot = sum(e["ItemSpawnWeight"] for e in ents)
            items = []
            for e in ents:
                w = e["ItemSpawnWeight"]
                subs = [{"tag": s["SubItemTag"]["TagName"], "name": nm(s["SubItemTag"]["TagName"]),
                         "chancePct": s["SubSpawnChance"], "amount": s["SubItemAmount"]}
                        for s in e["SubItemsSpawnData"]]
                items.append({"tag": e["ItemTag"]["TagName"], "name": nm(e["ItemTag"]["TagName"]),
                              "amount": e["ItemAmount"], "weight": w,
                              "chancePct": round(100 * w / tot, 2) if tot else 0, "subItems": subs})
            res[rid] = {
                "spawnChance": L["SpawnChance"],
                "effectiveRollPct": round(100 * chance_roll(L["SpawnChance"]), 2),
                "spawnByDefault": L["bSpawnByDefault"], "spawnByPoints": L["bSpawnByPoints"],
                "initialSpawnTime": L["InitialSpawnTime"], "initialSpawnPoints": L["InitialSpawnPoints"],
                "canRespawn": L["bCanRespawn"], "respawnTime": L["RespawnTime"],
                "neverSelectPreviousItem": L["bNeverSelectPreviousItem"],
                "insideControlZoneOnly": row.get("bSpawnInsideControlZoneOnly", False),
                "weightSum": tot, "items": items,
            }
        out["tables"][tname] = res
    out["meta"] = {"generator": "python -I _tools/loot_tables.py",
                   "notes": ["chancePct = ItemSpawnWeight / sum of weights of the row (Derived; with neverSelectPreviousItem the entry chosen last is left out of the next draw, so the chance of the others rises)",
                             "effectiveRollPct = 1 / (int(200 / SpawnChance + 0.5) >> 1), the chance one spawn roll passes (native read, round 59)"]}
    return out


def esc(s):
    return str(s).replace("|", "\\|")


def sublist(subs):
    if not subs:
        return "none"
    parts = []
    for s in subs:
        a = "%s x%d" % (s["name"], s["amount"])
        if s["chancePct"] != 100:
            a += " (%s%%)" % num(s["chancePct"])
        parts.append(a)
    return "; ".join(parts)


def blocks(data):
    b = {}
    t = data["tables"]["DT_LootableDataTable"]
    multi = {k: v for k, v in t.items() if len(v["items"]) > 1}
    single = {k: v for k, v in t.items() if len(v["items"]) == 1}
    L = ["| Row | Items | Spawn chance | Respawn | Spawns | Control zone only |", "|---|---|---|---|---|---|"]
    for k, v in t.items():
        rs = ("%s s" % num(v["respawnTime"])) if v["canRespawn"] else "no"
        sp = "at match start" if v["spawnByDefault"] else "after %s s" % num(v["initialSpawnTime"])
        L.append("| `%s` | %d | %s%% | %s | %s | %s |" % (k, len(v["items"]), num(v["spawnChance"]), rs, sp,
                                                         "yes" if v["insideControlZoneOnly"] else "no"))
    b["overview"] = "\n".join(L)
    L = []
    for k, v in multi.items():
        L.append("### `%s`" % k)
        L.append("")
        L.append("Spawn chance %s%%, respawn %s, never repeats the previous item: %s. Weight sum %s." % (
            num(v["spawnChance"]), ("%s s" % num(v["respawnTime"])) if v["canRespawn"] else "none",
            "yes" if v["neverSelectPreviousItem"] else "no", num(v["weightSum"])))
        L.append("")
        L.append("| Item | Amount | Weight | Chance per draw | Sub-items (always with it unless a chance is shown) |")
        L.append("|---|---|---|---|---|")
        for e in v["items"]:
            L.append("| %s | %d | %s | %s%% | %s |" % (esc(e["name"]), e["amount"], num(e["weight"]),
                                                      num(e["chancePct"]), esc(sublist(e["subItems"]))))
        L.append("")
    b["multi"] = "\n".join(L).rstrip()
    L = ["| Row | Item | Amount | Sub-items |", "|---|---|---|---|"]
    for k, v in single.items():
        e = v["items"][0]
        L.append("| `%s` | %s | %d | %s |" % (k, esc(e["name"]), e["amount"], esc(sublist(e["subItems"]))))
    b["single"] = "\n".join(L)
    L = ["| Row | Item | Amount | Spawn chance | Respawn | Sub-items |", "|---|---|---|---|---|---|"]
    for k, v in data["tables"]["DT_LootableDataTable_VIPEscort_01"].items():
        for e in v["items"]:
            L.append("| `%s` | %s | %d | %s%% | %s | %s |" % (
                k, esc(e["name"]), e["amount"], num(v["spawnChance"]),
                ("%s s" % num(v["respawnTime"])) if v["canRespawn"] else "none", esc(sublist(e["subItems"]))))
    b["vip"] = "\n".join(L)
    return b


def apply(txt, bl):
    for name, body in bl.items():
        pat = re.compile(r"<!-- loot_tables %s -->.*?<!-- /loot_tables %s -->" % (name, name), re.S)
        if not pat.search(txt):
            raise SystemExit("error: no markers for %s in %s" % (name, PAGE))
        txt = pat.sub(lambda _: "<!-- loot_tables %s -->\n%s\n<!-- /loot_tables %s -->" % (name, body, name), txt)
    return txt


def main():
    data = build()
    js = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    page = open(PAGE, encoding="utf-8", newline="").read() if os.path.exists(PAGE) else None
    if page is None:
        raise SystemExit("error: page missing: " + PAGE)
    nl = "\r\n" if "\r\n" in page else "\n"
    new_page = apply(page.replace("\r\n", "\n"), blocks(data)).replace("\n", nl)
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != js or new_page != page:
            print("stale: run python -I _tools/loot_tables.py")
            sys.exit(1)
        print("ok")
        return
    open(OUT, "w", encoding="utf-8", newline="\n").write(js)
    open(PAGE, "w", encoding="utf-8", newline="").write(new_page)
    print("wrote", OUT, "and", PAGE)


if __name__ == "__main__":
    main()
