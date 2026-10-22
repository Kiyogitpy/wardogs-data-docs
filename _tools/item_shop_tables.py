"""Item shop tables for every non-weapon item: gear, medical, explosives, tools, vehicle items, bow.

Sources (exported JSON under data/Wardogs/):
  - `WDVendorData` tables (price, unlock level, required items, buy limit, variations, categories);
  - `BHEntityData_UI` tables (display name, description, subtitle, category tag);
  - `ID_*` item definitions (`BHInventoryItemDefinition` and the fragments/extension objects in the same file):
    weight, inventory size, stack size, armor, durability, quick slots, grid capacity, heal amounts, throw
    velocity, placement limits, and so on.
Weapons and weapon parts (Plugins/GameFeatures/Weapons, `DT_WeaponMarket`, `DT_AttachmentMarket`) belong to
weapon_vendor_tables.py and are not repeated; the coverage block lists their tables only by name.
Ammo prices stay in resource_tables.py; buildables in buildable_tables.py (their vendor row is shown here too).

    python _tools/item_shop_tables.py            # summary counts
    python _tools/item_shop_tables.py --write    # refresh <!-- item_shop_tables NAME --> blocks

Page: game-features/Wardogs_ItemShop_v1.md.
"""
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weapon_vendor_tables as wv  # noqa: E402

ROOT = wv.ROOT
DATA = os.path.join(ROOT, "data", "Wardogs")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_ItemShop_v1.md")
GROUPS = collections.OrderedDict([
    ("gear", "Gear: armor, helmets, vests, backpacks, parachutes"),
    ("medical", "Medical"),
    ("explosives", "Throwables, mines and explosives"),
    ("tools", "Tools and utility"),
    ("bow", "Bow and arrows"),
    ("vehicle", "Vehicle items and vehicles"),
])
BLOCKS = ["coverage"] + [f"{p}_{g}" for g in GROUPS for p in ("shop", "stats")] + ["entities"]
# Tables whose rows belong to the weapon shop, the ammo table or other pages and are not repeated here.
SKIP_VENDOR = {"DT_WeaponMarket", "DT_AttachmentMarket"}

cell = wv.cell
loc = wv.loc
num = wv.num
short_tag = wv.short_tag


def rel(p):
    return os.path.relpath(p, DATA).replace(os.sep, "/")


def find_tables():
    """All DataTables with RowStruct WDVendorData or BHEntityData_UI: (kind, name, rel path, rows)."""
    out = []
    for p in sorted(glob.glob(os.path.join(DATA, "**", "DT_*.json"), recursive=True)):
        with open(p, encoding="utf-8", errors="ignore") as f:
            head = f.read(4000)
        m = re.search(r"Class'(WDVendorData|BHEntityData_UI)'", head)
        if '"Type": "DataTable"' not in head or not m:
            continue
        for o in wv.exports(p):
            if o.get("Type") == "DataTable":
                out.append(("V" if m.group(1) == "WDVendorData" else "E", o["Name"], rel(p), o.get("Rows", {})))
    return out


def group_of(key):
    k = key.lower()
    if k.startswith("vehicle.variant") or re.search(r"vehiclesupplycrate|flares|vehiclesmoke", k):
        return "vehicle"
    if re.search(r"combatbow|\.arrow", k):
        return "bow"
    if re.search(r"bandage|medkit|stimpen|defibrillator|resuscitator|enox", k):
        return "medical"
    if re.search(r"armor|helmet|backpack|tacvest|pouch|parachute|bpak", k):
        return "gear"
    if re.search(r"grenade|molotov|c4|claymore|\.ied\b|atmine", k):
        return "explosives"
    return "tools"


class Ctx:
    def __init__(self):
        self.tables = find_tables()
        self.vendor = collections.OrderedDict()  # lower id -> (table, rid, row, path)
        self.entity = collections.defaultdict(list)  # lower id -> [(table, row, path)]
        for kind, name, path, rows in self.tables:
            if "GameFeatures/Weapons/" in path:
                continue
            for rid, row in rows.items():
                if kind == "V":
                    if name not in SKIP_VENDOR:
                        self.vendor[rid.lower()] = (name, rid, row, path)
                else:
                    self.entity[rid.lower()].append((name, row, path))
        self.defs = {}
        for p in glob.glob(os.path.join(DATA, "**", "ID_*.json"), recursive=True):
            ex = wv.exports(p)
            for o in ex:
                if o.get("Type") == "BHInventoryItemDefinition":
                    tag = ((o.get("Properties") or {}).get("ItemId") or {}).get("TagName", "").lower()
                    self.defs[tag] = (o, ex, rel(p))
        self.matched_entities = set()
        self.items = []
        for k, (vt, rid, row, vpath) in self.vendor.items():
            ents = self.entity.get(k, [])
            vdir = os.path.dirname(vpath)
            ents = sorted(ents, key=lambda e: (os.path.dirname(e[2]) != vdir, e[0]))
            for e in ents:
                self.matched_entities.add((e[0], k))
            self.items.append({"key": k, "rid": rid, "vt": vt, "row": row, "vpath": vpath, "ents": ents,
                               "def": self.defs.get(k), "group": group_of(rid)})

    # -- text -----------------------------------------------------------------------------------
    def text(self, t):
        """Localized text of an FText dict; an empty export shows the string-table key instead."""
        s = loc(t)
        if s:
            return s
        if t and t.get("Key"):
            return f"[key `{t['Key']}`]"
        return ""

    def entity_text(self, it, suffix):
        for _, row, _ in it["ents"]:
            for kv in row.get("AdditionalTexts", []):
                if kv["Key"]["TagName"].endswith(suffix):
                    s = self.text(kv["Value"])
                    if s:
                        return s
        return ""

    def name(self, it):
        v = self.shown(it)
        if v.get("bOverwriteFriendlyName") and loc(v.get("OverwrittenFriendlyName")):
            return loc(v["OverwrittenFriendlyName"])
        for _, row, _ in it["ents"]:
            s = self.text(row.get("FriendlyName"))
            if s:
                return s
        if it["def"]:
            s = self.text((it["def"][0].get("Properties") or {}).get("DisplayName"))
            if s:
                return s
        return "-"

    def description(self, it):
        v = self.shown(it)
        if v.get("bOverwriteDescription") and loc(v.get("OverwrittenDescription")):
            return loc(v["OverwrittenDescription"])
        for _, row, _ in it["ents"]:
            s = self.text(row.get("Description"))
            if s:
                return s
        return self.entity_text(it, "ItemDescription") or "-"

    def shown(self, it):
        vs = it["row"]["VendorItemVariations"]
        return next((v for v in vs if v.get("bShowInVendor")), vs[0])

    def category(self, it):
        v = self.shown(it)
        parts = [short_tag(c, "Vendor.Category.") for c in v.get("Subcategories", [])]
        for _, row, _ in it["ents"]:
            c = (row.get("Category") or {}).get("TagName", "None")
            if c != "None":
                parts.append(short_tag(c, "Item.Category."))
                break
        return ", ".join(dict.fromkeys(parts)) or "-"

    # -- item definition --------------------------------------------------------------------------
    def frag(self, it, typ):
        if not it["def"]:
            return []
        return [o for o in it["def"][1] if o.get("Type") == typ]

    def props(self, it, typ):
        for o in self.frag(it, typ):
            return o.get("Properties") or {}
        return None

    def stats(self, it):
        out = []
        a = self.props(it, "WDInventoryFragment_Armor")
        if a is not None:
            dur = (a.get("ReplicatedData") or {}).get("Durability")
            if dur is not None:
                out.append(f"durability {num(dur)}")
            st = a.get("DurabilityStagesSetupData") or []
            if st:
                out.append(f"{len(st)} stages, reduction % " + "/".join(num(s.get("DamagePercentageReduction")) for s in st)
                           + ", thickness " + "/".join(num(s.get("Thickness")) for s in st)
                           + ", density " + "/".join(num(s.get("Density")) for s in st))
            cov = [short_tag(c, "Meta.Damage.HitLocation.Infantry.") for c in a.get("CoveredHitLocations", [])]
            if cov:
                out.append("covers " + ", ".join(cov))
            ctx = (a.get("DamageContextTag") or {}).get("TagName")
            if ctx:
                out.append(f"context {short_tag(ctx, 'Meta.Damage.')}")
            eff = [self.objname(e) for e in a.get("AppliedEffects", [])]
            if eff:
                out.append("effects " + ", ".join(eff))
        d = self.props(it, "WDInventoryFragment_Durability")
        if d is not None:
            out.append(f"durability {num((d.get('ReplicatedData') or {}).get('Durability'))}")
        q = self.props(it, "WDInventoryFragment_QuickSlots")
        if q is not None:
            out.append(f"+{q.get('NumberOfAddedQuickSlots')} quick slots")
        e = self.props(it, "WDInventoryFragment_EquippedEffects")
        if e is not None:
            out.append("equipped effects " + ", ".join(self.objname(x) for x in e.get("AppliedEffects", [])))
        s = self.props(it, "BHInventoryFragment_SubSlotSupport")
        if s is not None:
            grids = collections.Counter()
            for c in s.get("Containers", []):
                if c.get("SizeType", "").endswith("Grid"):
                    g = c.get("GridSize") or {}
                    grids[f"{num(g.get('X'))}x{num(g.get('Y'))}"] += 1
            for g, n in grids.items():
                out.append(f"grid {g}" if n == 1 else f"{n} grids {g}")
        pa = self.props(it, "WDInventoryFragment_Parachute")
        if pa is not None:
            out.append("movement " + self.objname(pa.get("ParachuteData")))
        ap = self.props(it, "WDItemExtensionData_Appliable")
        if ap is not None and ap.get("Attribute"):
            attr = short_tag(ap["Attribute"]["TagName"], "Attribute.Gameplay.")
            if ap.get("AttributeValue") is not None:
                out.append(f"applies {attr} {'+' if ap.get('bApplyAsDelta') else '='}{num(ap.get('AttributeValue'))}")
            else:
                out.append(f"applies {attr} (no value on the item)")
        at = self.props(it, "WDInventoryFragment_Attachment")
        if at is not None:
            out.append("fits as " + short_tag(((at.get("AttachmentData") or {}).get("AttachmentType") or {}).get("TagName", "-"), "Item.Attachment."))
        mk = self.props(it, "WDItemExtensionData_MedKit")
        if mk is not None:
            out.append(f"self {num(mk.get('HealSelfAmount'))} over {num(mk.get('HealSelfDuration'))} s (cost {num(mk.get('HealSelfDurabilityCost'))}); "
                       f"other {num(mk.get('HealOtherAmount'))} over {num(mk.get('HealOtherDuration'))} s (cost {num(mk.get('HealOtherDurabilityCost'))}); "
                       f"revive {num(mk.get('ReviveOtherHealthAmount'))} (cost {num(mk.get('ReviveOtherDurabilityCost'))})")
        th = self.props(it, "WDItemExtensionData_Throwable")
        if th is not None:
            cls = (th.get("ThrowableClass") or {}).get("AssetPathName", "").split("/")[-1].split(".")[0]
            vel = {short_tag(a["Key"]["TagName"], "Action.Throw."): a["Value"].get("ThrowVelocity") for a in th.get("ThrowActions", [])}
            out.append(f"thrown actor {cls}; throw velocity " + ", ".join(f"{k} {num(v)}" for k, v in vel.items()))
        pl = self.props(it, "WDItemExtensionData_Placeable")
        if pl is not None:
            out.append(f"place within {num(pl.get('MaxPlacementDistance'))} units" if pl.get("MaxPlacementDistance") else "placement distance not set")
            out[-1] += f", max angle {num(pl.get('MaxPlacementAngle'))}; actor {self.objname(pl.get('PlaceableClass'))}"
        bt = self.props(it, "WDItemExtensionData_Battery")
        if bt is not None:
            out.append(f"battery use {num(bt.get('ChargesPerSecondConsumption'))}/s")
        me = self.props(it, "WDItemExtensionData_CharacterMelee")
        if me is not None:
            for a in me.get("MeleeActions", []):
                out.append(f"melee {short_tag(a['Key']['TagName'], 'Action.')} damage {num(a['Value'].get('Damage'))}")
        bw = self.props(it, "WDItemExtensionData_RangedBow_C")
        if bw is not None:
            out.append(f"full draw {num(bw.get('FullDrawTime'))} s")
        sc = self.props(it, "WDItemExtensionData_VehicleSupplyCrate")
        if sc is not None:
            out.append("crate actor " + self.objname(sc.get("BaseClass")))
        return "; ".join(out) or "-"

    @staticmethod
    def objname(o):
        if not o:
            return "-"
        if isinstance(o, dict):
            n = o.get("ObjectName") or o.get("AssetPathName") or ""
            m = re.search(r"'([^']*)'", n)
            return (m.group(1) if m else n.split("/")[-1].split(".")[0]) or "-"
        return str(o)


def tbl(*names):
    return ", ".join(f"`{n}`" for n in dict.fromkeys(names) if n)


def shop(c, g):
    rows = ["| Item id | Name | Subtitle | Description | Category | Price | Unlock lvl | Req. items | Buy limit | Amount | Variations | Tables |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for it in c.items:
        if it["group"] != g:
            continue
        v = c.shown(it)
        vs = it["row"]["VendorItemVariations"]
        req = [x if isinstance(x, str) else x.get("TagName", str(x)) for x in v.get("UnlockRequiredItems", [])]
        hidden = "" if v.get("bShowInVendor") else " (hidden)"
        rows.append(f"| `{it['rid']}` | {cell(c.name(it))} | {cell(c.entity_text(it, 'ItemSubtitle')) or '-'} | {cell(c.description(it))} | "
                    f"{cell(c.category(it))} | {num(v.get('Price'))}{hidden} | {num(v.get('LevelToUnlock'))} | {cell(', '.join(req) or '-')} | "
                    f"{num(v.get('LifeTimeBuyLimit')) if v.get('LifeTimeBuyLimit') else '-'} | {num(v.get('Amount'))} | {len(vs)} | "
                    f"{tbl(it['vt'], *[e[0] for e in it['ents']])} |")
    return "\n".join(rows)


def stats(c, g):
    rows = ["| Item id | Name | Weight | Inventory size | Max stack | Key stats | Definition |", "|---|---|---|---|---|---|---|"]
    for it in c.items:
        if it["group"] != g:
            continue
        if g == "vehicle" and it["key"].startswith("vehicle.variant"):
            v = c.shown(it)
            asset = c.objname(v.get("VehicleStatsDataAsset"))
            rows.append(f"| `{it['rid']}` | {cell(c.name(it))} | - | - | - | stats asset `{asset}` (see [Vehicles](Wardogs_GameFeatures_Vehicles_v2.md) section 3) | "
                        f"{'`' + it['def'][2] + '`' if it['def'] else '-'} |")
            continue
        w = c.props(it, "BHInventoryFragment_Weight")
        sh = c.props(it, "BHInventoryFragment_CustomShape")
        st = c.props(it, "BHInventoryFragment_Stackable")
        dim = (sh or {}).get("Dimensions") or {}
        rows.append(f"| `{it['rid']}` | {cell(c.name(it))} | {num(w.get('Weight')) if w else '-'} | "
                    f"{(num(dim.get('X')) + 'x' + num(dim.get('Y'))) if dim else '-'} | "
                    f"{num(st.get('MaxStackSize')) if st else '-'} | {cell(c.stats(it))} | "
                    f"{'`' + it['def'][2] + '`' if it['def'] else '-'} |")
    return "\n".join(rows)


def entities(c):
    """Entity rows from feature plugins (not Weapons) that no vendor row in this page uses."""
    rows = ["| Table | Row key | Name | Subtitle | Description |", "|---|---|---|---|---|"]
    for kind, name, path, trows in c.tables:
        if kind != "E" or "GameFeatures/Weapons/" in path or "Plugins/GameFeatures/" not in path or "Items/Buildables/" in path:
            continue
        for rid, row in trows.items():
            if (name, rid.lower()) in c.matched_entities:
                continue
            sub = ""
            for kv in row.get("AdditionalTexts", []):
                if kv["Key"]["TagName"].endswith("ItemSubtitle"):
                    sub = c.text(kv["Value"])
            rows.append(f"| `{name}` | `{rid}` | {cell(c.text(row.get('FriendlyName'))) or '-'} | {cell(sub) or '-'} | "
                        f"{cell(c.text(row.get('Description'))) or '-'} |")
    return "\n".join(rows)


def coverage(c):
    used_v = {it["vt"] for it in c.items}
    used_e = {n for n, _ in c.matched_entities}
    rows = ["| Kind | Table | Rows | Where the rows are written up |", "|---|---|---|---|"]
    weapon = collections.defaultdict(lambda: ([], [], 0, 0))
    plain = []
    for kind, name, path, trows in c.tables:
        if "GameFeatures/Weapons/" in path:
            fam = path.split("GameFeatures/Weapons/")[1].split("/")[0]
            v, e, nv, ne = weapon[fam]
            (v if kind == "V" else e).append(name)
            weapon[fam] = (v, e, nv + (len(trows) if kind == "V" else 0), ne + (len(trows) if kind == "E" else 0))
            continue
        if kind == "V":
            where = "this page" if name in used_v else "empty table (0 rows)" if not trows else "[Weapon Shop](Wardogs_WeaponShop_v1.md) / [Game Mechanics](../content/Wardogs_GameMechanics_v2.md) (weapon, magazine, ammo and attachment markets)"
        elif name in used_e:
            where = "this page (name and text of sold items)"
        elif "Items/Buildables/" in path:
            where = "[Buildables](Wardogs_Buildables_v1.md)"
        elif "Plugins/GameFeatures/" in path:
            where = "this page, section 'Entity text without a vendor row'"
        else:
            where = "shared UI text table outside the feature plugins; documented on other pages and not repeated here"
        plain.append((kind, name, len(trows), where))
    for kind, name, n, where in plain:
        rows.append(f"| {'WDVendorData' if kind == 'V' else 'BHEntityData_UI'} | `{name}` | {n} | {where} |")
    for fam in sorted(weapon):
        v, e, nv, ne = weapon[fam]
        for label, names, n in (("WDVendorData", v, nv), ("BHEntityData_UI", e, ne)):
            if names:
                rows.append(f"| {label} | {len(names)} table(s) in `Weapons/{fam}`: " + " ".join(f"`{x}`" for x in names)
                            + f" | {n} | [Weapon Shop](Wardogs_WeaponShop_v1.md) |")
    nv = sum(1 for t in c.tables if t[0] == "V")
    ne = sum(1 for t in c.tables if t[0] == "E")
    rows.append("")
    rows.append(f"Totals: {nv} `WDVendorData` tables ({sum(len(t[3]) for t in c.tables if t[0] == 'V')} rows) and {ne} `BHEntityData_UI` tables "
                f"({sum(len(t[3]) for t in c.tables if t[0] == 'E')} rows).")
    return "\n".join(rows)


def render(c, name):
    if name == "coverage":
        return coverage(c)
    if name == "entities":
        return entities(c)
    p, g = name.split("_", 1)
    return shop(c, g) if p == "shop" else stats(c, g)


def write(c):
    with open(PAGE, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    for name in BLOCKS:
        pat = re.compile(rf"<!-- item_shop_tables {name} -->.*?<!-- /item_shop_tables {name} -->", re.S)
        if not pat.search(text):
            raise SystemExit(f"error: no markers for {name} in {os.path.basename(PAGE)}")
        body = render(c, name).replace("\n", nl)
        text = pat.sub(lambda _: f"<!-- item_shop_tables {name} -->{nl}{body}{nl}<!-- /item_shop_tables {name} -->", text)
    with open(PAGE, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    c = Ctx()
    if "--write" in sys.argv:
        write(c)
        return
    cnt = collections.Counter(it["group"] for it in c.items)
    nodef = [it["rid"] for it in c.items if not it["def"]]
    noent = [it["rid"] for it in c.items if not it["ents"]]
    print(f"tables {len(c.tables)}, vendor items {len(c.items)}, by group {dict(cnt)}, without definition {nodef}, without entity {noent}")


if __name__ == "__main__":
    main()
