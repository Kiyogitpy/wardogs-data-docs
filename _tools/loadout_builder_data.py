"""Slot membership, shop names, prices, weights and icons for the Loadout Builder page.

Writes assets/data/loadout-builder.json, read by assets/js/loadout-builder.js next to weapon-loadouts.json and
loadout-extras.json. Every value is copied from data already in this repository; null where the data has none.

Sources:
  slots      Inventory.Slot.* tag in the ItemContext of each BHInventoryItemDefinition (the ID_* files under
             data/Wardogs). The loadout screen's slot names are in DT_GameplayTagToText_InventorySlots
             (Primary Weapon, Secondary Weapon, Spec. Item, Sidearm, Armor, Helmet, Tac-Vest, Backpack, Traversal...).
             primary = Inventory.Slot.Primary, sidearm = .Sidearm, special = .Specialist ("Spec. Item"),
             armor/helmet/vest/backpack = the like-named tag. An item is listed only when it has a vendor row.
  items      weapons and attachments of weapon-loadouts.json (every id there gets an entry), plus every
             slot item. Names, prices, subtitles come from weapon_vendor_tables.py (weapon/attachment
             DT_EntityData / DT_VendorData) and item_shop_tables.py (gear and tools); weight from
             BHInventoryFragment_Weight, armor from WDInventoryFragment_Armor, vest quick slots from
             WDInventoryFragment_QuickSlots, backpack grids from BHInventoryFragment_SubSlotSupport; icons from
             assets/data/item-icons.json (vendor png, else inventory png); armor coverage and durability reduction
             from assets/data/weapon-damage-locations.json meta.armor_items.

  python -I _tools/loadout_builder_data.py          write the file
  python -I _tools/loadout_builder_data.py --check  exit 1 if the written file is stale
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import item_shop_tables as ist  # noqa: E402
import weapon_vendor_tables as wv  # noqa: E402

ROOT = wv.ROOT
OUT = os.path.join(ROOT, "assets", "data", "loadout-builder.json")
SLOT_TAG = {"primary": "Inventory.Slot.Primary", "sidearm": "Inventory.Slot.Sidearm", "special": "Inventory.Slot.Specialist",
            "helmet": "Inventory.Slot.Helmet", "armor": "Inventory.Slot.Armor", "vest": "Inventory.Slot.Vest",
            "backpack": "Inventory.Slot.Backpack"}
WEAPON_SLOTS = ("primary", "sidearm", "special")
LEVEL = {"Light": 1, "Medium": 2, "Heavy": 3, "SuperHeavy": 4}


def jload(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def clean(x):
    """Whole floats as ints, other floats rounded to 6 places."""
    if x is None:
        return None
    x = float(x)
    return int(x) if x == int(x) else round(x, 6)


def split_camel(s):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)


def build():
    loadouts = jload("assets/data/weapon-loadouts.json")
    icons = {k.lower(): v for k, v in jload("assets/data/item-icons.json")["items"].items()}
    armor_meta = {a["id"]: a for a in jload("assets/data/weapon-damage-locations.json")["meta"]["armor_items"]}
    wc = wv.Ctx()
    ic = ist.Ctx()
    weapon_by_asset = {w.asset: w for w in wc.weapons}
    item_by_asset = {i.asset: i for i in wc.data.items.values()}
    shop = {it["key"]: it for it in ic.items}

    def icon(tag):
        rec = icons.get(tag.lower()) or {}
        for k in ("vendor", "inventory"):
            if (rec.get(k) or {}).get("png"):
                return rec[k]["png"]
        return None

    def weight(tag):
        d = ic.defs.get(tag.lower())
        for o in (d[1] if d else []):
            if o.get("Type") == "BHInventoryFragment_Weight":
                return clean((o.get("Properties") or {}).get("Weight"))
        return None

    def frag(tag, typ):
        d = ic.defs.get(tag.lower())
        for o in (d[1] if d else []):
            if o.get("Type") == typ:
                return o.get("Properties") or {}
        return None

    def shop_row(tag):
        """(price, hidden, name, subtitle, category, shop item) from the weapon tables, else the item shop tables."""
        key = tag.lower()
        v = wv.vendor_info(wc.vendor.get(key))
        if v:
            e = wc.entity.get(key)
            sub = ""
            for kv in (e[1].get("AdditionalTexts", []) if e else []):
                if kv["Key"]["TagName"].endswith("ItemSubtitle"):
                    sub = wv.loc(kv["Value"])
            name = wv.loc(e[1].get("FriendlyName")) if e else ""
            return clean(v["price"]), not v["shown"], name or None, sub or None, v["sub"], None
        it = shop.get(key)
        if it:
            sv = ic.shown(it)
            name = ic.name(it)
            return (clean(sv.get("Price")), not sv.get("bShowInVendor"), None if name == "-" else name,
                    ic.entity_text(it, "ItemSubtitle") or None, ic.category(it), it)
        return None, None, None, None, "", None

    items = {}

    # every weapon and attachment of weapon-loadouts.json
    for aid, rec in loadouts["items"].items():
        tag = rec["itemId"]
        price, hidden, name, sub, cat, _ = shop_row(tag)
        e = {"itemId": tag, "name": name or rec.get("display"), "price": price,
             "priceHidden": hidden if price is not None else None,
             "weightKg": weight(tag), "icon": icon(tag), "text": sub}
        if aid in weapon_by_asset:
            m = re.search(r"Weapon\.Type\.(\w+)", cat)
            e.update(kind="weapon", archetype=rec.get("archetype"), **{"class": split_camel(m.group(1)) if m else None})
        else:
            it = item_by_asset.get(aid)
            e.update(kind="attachment", slot=wc.slot(it) if it else None)
        items[aid] = e

    # Magazine capacity: the Item.Ammo container's MaxSlotAmountStackSize, as weapon_capacity_tables.py reads it.
    import weapon_capacity_tables as wct
    id_paths = {os.path.basename(p)[:-5]: p for p in glob.glob(os.path.join(ROOT, "data", "Wardogs", "**", "ID_*.json"), recursive=True)}
    for aid, e in items.items():
        if e.get("kind") == "attachment" and e.get("slot") == "Magazine" and aid in id_paths:
            ammo = next((c for c in map(wct.cinfo, wct.containers(id_paths[aid])) if c["container"] == "Item.Ammo"), None)
            e["capacity"] = ammo["stack"] if ammo else None

    # Parts with no shop name (mostly default barrels, stocks, grips): "<owner> <slot>" from the item whose
    # sub-slot starts with the part, else "<slot> <code>"; nameDerived marks the name as not the game's.
    owners = {}
    for oid, rec in loadouts["items"].items():
        for s in rec.get("slots") or []:
            if s.get("default"):
                owners.setdefault(s["default"], []).append((oid, s["tag"]))
    for aid, e in items.items():
        if e["name"] and e["name"] != aid and not e["name"].startswith("ID_"):
            continue
        own = sorted(owners.get(aid, []), key=lambda o: str(items.get(o[0], {}).get("name") or o[0]))
        slot_label = (own[0][1] if own else e.get("slot") or "Item.Part").rsplit(".", 1)[-1]
        owner_name = own and items.get(own[0][0], {}).get("name")
        if owner_name and not owner_name.startswith("ID_"):
            e["name"] = f"{owner_name} {split_camel(slot_label).lower()}"
        else:
            e["name"] = f"{split_camel(slot_label)} {aid[3:]}"
        e["nameDerived"] = True

    # slot membership from the Inventory.Slot.* context tags
    slots = {k: [] for k in SLOT_TAG}
    for aid, w in weapon_by_asset.items():
        for slot in WEAPON_SLOTS:
            if SLOT_TAG[slot] in w.context_tags:
                slots[slot].append(aid)
    for it in ic.items:
        d = it["def"]
        if not d:
            continue
        asset = os.path.basename(d[2])[:-5]
        if asset in weapon_by_asset:
            continue
        ctx = d[0]["Properties"].get("ItemContext") or []
        tg = d[0]["Properties"]["ItemId"]["TagName"]
        for slot, tag in SLOT_TAG.items():
            if tag not in ctx:
                continue
            slots[slot].append(asset)
            if asset in items:
                continue
            price, hidden, name, sub, cat, _ = shop_row(tg)
            e = {"itemId": tg, "name": name, "price": price, "priceHidden": hidden if price is not None else None,
                 "weightKg": weight(tg), "icon": icon(tg), "text": sub}
            if slot in ("armor", "helmet"):
                am = armor_meta[asset]
                a = frag(tg, "WDInventoryFragment_Armor") or {}
                e.update(kind=slot, armorClass=am["class"], level=LEVEL.get(am["class"]),
                         covers=am["covered_locations"], durabilityReductionPct=clean(am["durability_reduction_pct"]),
                         durability=clean((a.get("ReplicatedData") or {}).get("Durability")))
            elif slot == "vest":
                q = frag(tg, "WDInventoryFragment_QuickSlots")
                e.update(kind="vest", quickSlots=q.get("NumberOfAddedQuickSlots") if q else None)
            elif slot == "backpack":
                s = frag(tg, "BHInventoryFragment_SubSlotSupport") or {}
                raw = [[int(c["GridSize"]["X"]), int(c["GridSize"]["Y"])] for c in s.get("Containers", [])
                       if c.get("SizeType", "").endswith("Grid") and c.get("GridSize")]
                m = re.search(r"Grid:\s*(\d+)x(\d+)", ic.description(it))
                if m:
                    grid = [int(m.group(1)), int(m.group(2))]
                elif len(raw) == 1:
                    grid = [raw[0][1], raw[0][0]]
                else:
                    grid = None
                e.update(kind="backpack", grid=grid, grids=raw)
            else:
                e["kind"] = "tool"
            items[asset] = e
    for k in slots:
        slots[k] = sorted(set(slots[k]), key=lambda a: (items[a]["price"] is None, items[a]["price"] or 0, a))

    return {
        "meta": {
            "generator": "python -I _tools/loadout_builder_data.py",
            "slotCounts": {k: len(v) for k, v in slots.items()},
            "notes": [
                "slots: membership is the Inventory.Slot.* tag in the ItemContext of each item definition (ID_*.json); the loadout "
                "screen names them Primary Weapon, Sidearm, Spec. Item, Armor, Helmet, Tac-Vest, Backpack "
                "(DT_GameplayTagToText_InventorySlots). An item is listed only when a vendor row exists for it.",
                "primary = Inventory.Slot.Primary: 26 of the 29 also carry Inventory.Slot.Secondary (a second main weapon slot at "
                "runtime, not offered by the builder); the Compound Bow is Primary only. sidearm = Inventory.Slot.Sidearm "
                "(pistols and revolvers). special = Inventory.Slot.Specialist, the Spec. Item slot: the four launchers plus "
                "tools sold in the item shop (binoculars, range finders, hammers, wrench, drills, crowbar, fuel can, medical "
                "bag, defibrillator, remote detonators); those have kind tool, no class and no attachments.",
                "kind: weapon, attachment, tool, armor, helmet, vest, backpack. class is the shop category (Weapon.Type.*) of "
                "weapons and can differ from archetype, the loadout archetype code (ID_WEPN_037 is shop class Assault Rifle, "
                "archetype DMR).",
                "price: first shown vendor variation (else the first variation) from the weapon or item shop tables; "
                "priceHidden = no variation is shown in the shop. null price: no vendor row (most attachments).",
                "weightKg: BHInventoryFragment_Weight on the item definition, null when the definition has none.",
                "armor/helmet: armorClass is the Meta.Damage.Armor/Helmet context class; level Light=1, Medium=2, Heavy=3, "
                "SuperHeavy=4, null for Ghillie, Pilot, Tank. covers and durabilityReductionPct come from "
                "weapon-damage-locations.json meta.armor_items; durability is WDInventoryFragment_Armor.",
                "backpack: grid [w,h] is the shop text ('Grid: 4x2'); the definition stores the same grid as X,Y = 2,4 "
                "(columns and rows swapped), so a single-grid pack without shop text uses [Y,X]; grids lists the raw X,Y of "
                "every grid container (side pockets and slings are extra grids); grid is null for a multi-grid bag with no "
                "shop text.",
                "vest quickSlots: NumberOfAddedQuickSlots of WDInventoryFragment_QuickSlots.",
                "icon: assets/data/item-icons.json vendor png, else inventory png.",
            ],
        },
        "slots": slots,
        "items": items,
    }


def main():
    text = json.dumps(build(), ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
    if "--check" in sys.argv:
        old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if old != text:
            sys.exit("assets/data/loadout-builder.json is stale: run python -I _tools/loadout_builder_data.py")
        print("loadout-builder.json is current")
        return
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    d = json.loads(text)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(d['items'])} items; slots {d['meta']['slotCounts']}")


if __name__ == "__main__":
    main()
