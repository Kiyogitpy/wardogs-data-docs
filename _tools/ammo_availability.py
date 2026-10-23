"""Which ammo each weapon caliber can load, and how each ammo item resolves to a damage modifier tag.

Rebuilt from data/ only. Rules (pipelines/Wardogs_DamagePipeline_v2.md section 7.9): the modifier tag is built
from the ammo item's ItemId tag. <type> is the tag's last name, or its last two names for a five-level tag
(Id.Item.<caliber>.<type>.Tracer). It counts only if it is in the fixed map below (taken from the five
DA_AmmoModifier_* assets). Anything else gives no tag, so the round behaves as plain FMJ.

    python _tools/ammo_availability.py            # write assets/data/ammo-availability.json
    python _tools/ammo_availability.py --out PATH # write somewhere else too
    python _tools/ammo_availability.py --check    # print counts and flag inconsistencies
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402

ROOT, DATA = dt.ROOT, dt.DATA
PREFIX = "Meta.Damage.AmmoModifier."
CAL = "Item.Caliber."
OUT = os.path.join(ROOT, "assets", "data", "ammo-availability.json")


def modifier_map():
    """type -> modifier tag, read from the DA_AmmoModifier_* assets (the fixed map filled in 0x6F2AAA0)."""
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "Wardogs/Content/GameMechanics/DamageSystem/AmmoModifiers/DA_AmmoModifier_*.json"))):
        for o in dt.exports(p):
            t = dt.tag(o.get("Properties", {}).get("AmmoModifierTag"))
            if t and t.startswith(PREFIX):
                out[t[len(PREFIX):]] = t
    return out


def item_type(item_id):
    """<type> per native 0x6C98496: last name, or last two for a five-level tag."""
    parts = item_id.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 5 else parts[-1]


def short(c):
    return c[len(CAL):] if c.startswith(CAL) else c


def exports_of(p):
    return dt.exports(p)


def projectile_assets():
    """asset name -> (ProjectileId, BaseDamage, Context tags) for every caliber data asset."""
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/**/DA_*.json"), recursive=True)):
        for o in dt.exports(p):
            pr = o.get("Properties", {})
            st = pr.get("ProjectileStats")
            if pr.get("ProjectileId") and st:
                ent = st.get("DamageEntityData", {})
                out[o.get("Name")] = {"projectileId": dt.tag(pr["ProjectileId"]), "baseDamage": st.get("DamageValues", {}).get("BaseDamage"),
                                      "context": [dt.tag(t) for t in ent.get("Context", [])]}
    return out


def ammo_items():
    out = []
    for p in sorted(glob.glob(os.path.join(DATA, "Wardogs/**/ID_*.json"), recursive=True)):
        for o in dt.exports(p):
            pr = o.get("Properties", {})
            if o.get("Type") != "BHInventoryItemDefinition" or "ItemId" not in pr:
                continue
            ctx = [dt.tag(c) for c in pr.get("ItemContext", [])]
            in_ammo_dir = "/Resources/Ammo/" in p.replace(os.sep, "/")
            if "Item.Ammo" not in ctx and not in_ammo_dir:
                continue
            iid = dt.tag(pr["ItemId"])
            cals = [c for c in ctx if c.startswith(CAL)]
            name = pr.get("DisplayName", {})
            proj = next((q["Properties"]["ProjectileData"]["ObjectName"].split("'")[1] for q in exports_of(p) if "ProjectileData" in q.get("Properties", {})
                         and isinstance(q["Properties"]["ProjectileData"], dict)), None)
            out.append({"file": os.path.basename(p)[3:-5], "path": os.path.relpath(p, DATA).replace(os.sep, "/"),
                        "itemId": iid, "noAmmoCtx": "Item.Ammo" not in ctx, "projAsset": proj, "caliberCtx": cals, "typeCtx": [c for c in ctx if c.startswith("Item.Ammo.Type")],
                        "display": name.get("SourceString") if isinstance(name, dict) else None})
    return out


def vendor_rows():
    """ItemId (lower case) -> vendor listing, from the four VendorEquipment tables."""
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_*.json"))):
        for o in dt.exports(p):
            for v in dt.walk(o, "VendorItemVariations"):
                for var in v:
                    t = dt.tag(var.get("VariationTag"))
                    if t and t.lower().startswith("id.item.") and "Vendor.Category.Vehicle.Ammo" in var.get("Categories", []) + [dt.tag(c) for c in var.get("Categories", [])] or (t and "Ammo" in " ".join(dt.tag(c) or "" for c in var.get("Categories", []))):
                        out[t.lower()] = {"table": os.path.basename(p)[3:-5], "categories": [dt.tag(c) for c in var.get("Categories", [])],
                                          "subcategories": [dt.tag(c) for c in var.get("Subcategories", [])],
                                          "price": var.get("Price"), "amount": var.get("Amount"),
                                          "showInVendor": var.get("bShowInVendor"), "previewOnly": var.get("bIsPreviewOnly"),
                                          "levelToUnlock": var.get("LevelToUnlock")}
    return out


def weapon_loading():
    """weapon item name -> chamber caliber filter and the resource its primary use consumes, from the weapon item file."""
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "Wardogs/Plugins/GameFeatures/Weapons/**/ID_*.json"), recursive=True)):
        name = os.path.basename(p)[3:-5]
        info = {"chamberAllowed": [], "chamberBlocked": [], "defaultAmmo": [], "resource": []}
        for o in dt.exports(p):
            for c in dt.walk(o, "Containers"):
                for cont in c:
                    if dt.tag(cont.get("ContainerIdentifier")) in ("Item.Attachment.Chamber", "Item.Ammo"):
                        f = cont.get("Filter", {})
                        info["chamberAllowed"] += [short(dt.tag(x)) for x in f.get("AllowedSubSlotContext", [])]
                        info["chamberBlocked"] += [short(dt.tag(x)) for x in f.get("BlockedSubSlotContext", [])]
                        info["defaultAmmo"] += [dt.tag(x) for x in cont.get("DefaultItems", [])]
            for r in dt.walk(o, "RequiredResource"):
                info["resource"].append(dt.tag(r))
        info["resource"] = sorted(set(info["resource"]))
        out.setdefault(name, info)
    return out


def build():
    mods = modifier_map()
    items = ammo_items()
    vend = vendor_rows()
    pa = projectile_assets()
    calibers = {}
    for it in items:
        if not it["caliberCtx"]:
            continue
        c = short(it["caliberCtx"][0])
        t = item_type(it["itemId"])
        tag_ = mods.get(t)
        notes = []
        if tag_ is None:
            if t.lower() in ("armourpiercing", "armourpiercing.tracer"):
                notes.append("British spelling: not in the fixed map, no modifier, behaves as FMJ")
            elif len(it["itemId"].split(".")) >= 4 and t != "Tracer":
                notes.append("tag does not resolve through the fixed map: no modifier")
        if it["noAmmoCtx"]:
            notes.append("item context lacks Item.Ammo (caliber context present)")
        if len(it["caliberCtx"]) > 1:
            notes.append("several caliber contexts: " + ", ".join(it["caliberCtx"]))
        if tag_:
            typ = t
        elif len(it["itemId"].split(".")) <= 3:
            typ = "FMJ"  # plain round: Id.Item.<caliber>, no type name
        elif t.lower().startswith("armourpiercing"):
            typ = t
        else:
            typ = next((x[len("Item.Ammo.Type."):] for x in it["typeCtx"] if x[len("Item.Ammo.Type."):] in ("Buckshot", "Slug")), t)
        if not (pa.get(it["projAsset"]) or {}).get("projectileId") and typ == "FMJ" and c not in ("DroneProjectile",) and not it["projAsset"] is None:
            notes.append("projectile asset has no caliber ProjectileId; not a plain bullet round")
        elif it["projAsset"] is None:
            notes.append("no projectile fragment on the item (trigger or charge item)")
        calibers.setdefault(c, {"id": CAL + c, "ammo": []})["ammo"].append(
            {"item": it["itemId"], "type": typ, "modifierTag": tag_, "note": "; ".join(notes) or None, "file": it["path"],
             "contextType": [x[len("Item.Ammo.Type."):] for x in it["typeCtx"]], "vendor": vend.get(it["itemId"].lower()),
             "projectileAsset": it["projAsset"], "projectile": pa.get(it["projAsset"])})
    users = {}
    weapons = {}
    loading = weapon_loading()
    for name, wtag, cals, _ in dt.weapons():
        sc = [short(c) for c in cals]
        ld = loading.get(name, {})
        notes = []
        if ld.get("chamberAllowed") and set(ld["chamberAllowed"]) != set(sc):
            notes.append("weapon item chamber filter allows " + ", ".join(ld["chamberAllowed"]) + " while the stats asset lists " + ", ".join(sc))
        weapons[name] = {"caliber": sc[0] if sc else None, "acceptsCalibers": sc, "damageTag": wtag,
                         "chamberAllowed": ld.get("chamberAllowed"), "chamberBlocked": ld.get("chamberBlocked"),
                         "primaryUseResource": ld.get("resource"), "note": "; ".join(notes) or None}
        for c in sc:
            users.setdefault(c, []).append(name)
    for name, w in weapons.items():
        if "7mmBuck" in w["acceptsCalibers"]:
            w["note"] = "; ".join(filter(None, [w["note"], "the chamber takes 12g ammo (plain 12g and 7mm buckshot fire the 7mmBuck projectile, the rifled slug fires Item.Caliber.12g.RifledSlug, which the stats asset does not list)"]))
    # A weapon's stats asset can list a projectile caliber that no ammo item names in its caliber context
    # (7mmBuck: the plain 12g round and the 7mm buckshot round both fire the 7mmBuck projectile).
    for c in sorted(users):
        if c in calibers:
            continue
        hits = [dict(a, note=("; ".join(filter(None, [a["note"], "listed here because its projectile is " + CAL + c])))) for v in calibers.values()
                for a in v["ammo"] if (a.get("projectile") or {}).get("projectileId") == CAL + c]
        if hits:
            calibers[c] = {"id": CAL + c, "alias": True, "ammo": hits}
    return items, calibers, weapons, users


def main():
    items, calibers, weapons, users = build()
    if "--check" in sys.argv:
        check(items, calibers, weapons, users)
        return
    doc = {"meta": {"build": "data/ snapshot of this repository", "notes": [
        "Generated by _tools/ammo_availability.py.",
        "modifierTag is derived from the ItemId tag (DamagePipeline section 7.9); null means no modifier, i.e. FMJ behavior.",
        "Caliber keys are the Item.Caliber.<key> names used by damage_tables.py; each caliber carries its full id."]},
        "calibers": calibers, "weapons": weapons}
    for path in [OUT] + [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--out"]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=1)
            f.write("\n")
        print("wrote", path)


def check(items, calibers, weapons, users):
    print(f"ammo items: {len(items)}; with caliber: {sum(1 for i in items if i['caliberCtx'])}; calibers: {len(calibers)}; weapons: {len(weapons)}")
    for i in items:
        if not i["caliberCtx"]:
            print("ammo item with no caliber:", i["itemId"], i["path"])
    for c in sorted(calibers):
        if c not in users and not calibers[c].get("alias"):
            print("caliber with no weapon:", c, "(", len(calibers[c]["ammo"]), "ammo items )")
    for w, v in sorted(weapons.items()):
        for c in v["acceptsCalibers"]:
            if c not in calibers:
                print("weapon with no ammo:", w, "caliber", c)
    for c, v in sorted(calibers.items()):
        for a in v["ammo"]:
            if a["note"]:
                print("note:", c, a["item"], "->", a["type"], "|", a["note"])


if __name__ == "__main__":
    main()
