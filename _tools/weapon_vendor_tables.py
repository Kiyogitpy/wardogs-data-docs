"""Weapon shop tables: platforms, attachments and components, rebuilt from data/.

Sources (all exported JSON under data/Wardogs/Plugins/GameFeatures/Weapons/):
  - `ID_*` item definitions (`BHInventoryItemDefinition`): item id, context tags, sub-slot containers
    (what the item accepts), `WDInventoryFragment_Attachment` type tag;
  - `DT_EntityData_*` (`BHEntityData_UI`): display name, subtitle, description;
  - `DT_VendorData_*` / `DT_WeaponVendor*` (`WDVendorData`): price, unlock level, requirements, limits.
Fit ("compatible weapons") is derived with the slot filter of weapon_attributes.py (accepts / reachable_containers,
3 levels deep); it is not read from a table.

    python _tools/weapon_vendor_tables.py            # summary counts
    python _tools/weapon_vendor_tables.py --write    # refresh <!-- weapon_vendor_tables NAME --> blocks

Page: game-features/Wardogs_WeaponShop_v1.md.
"""
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weapon_attributes as wa  # noqa: E402

ROOT = wa.ROOT
WROOT = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Weapons")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_WeaponShop_v1.md")
EXPORT = wa.EXPORT
BLOCKS = ("platforms", "platformparts", "attachments", "components", "fitgroups", "shoptext", "files")


def exports(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        parts = EXPORT.split(f.read())
    out = []
    for p in parts:
        if p.strip():
            try:
                out.append(json.loads(p))
            except ValueError:
                pass
    return out


def loc(t):
    if not t:
        return ""
    return (t.get("LocalizedString") or t.get("SourceString") or t.get("CultureInvariantString") or "").strip()


def cell(s):
    return str(s).replace("|", "\\|").replace("\r\n", "; ").replace("\n", "; ").replace("\r", "; ").strip("; ")


def short_tag(t, prefix):
    return t[len(prefix):] if t.startswith(prefix) else t


def load_tables():
    """Vendor and entity rows by lower-case item id, with the table each came from."""
    vendor, entity = {}, {}
    for path in sorted(glob.glob(os.path.join(WROOT, "**", "DT_*.json"), recursive=True)):
        for o in exports(path):
            if o.get("Type") != "DataTable":
                continue
            for rid, row in o.get("Rows", {}).items():
                if "VendorItemVariations" in row:
                    vendor[rid.lower()] = (o["Name"], row)
                elif "FriendlyName" in row:
                    entity[rid.lower()] = (o["Name"], row)
    return vendor, entity


def vendor_info(vrow):
    if not vrow:
        return None
    name, row = vrow
    vs = row["VendorItemVariations"]
    shown = next((v for v in vs if v.get("bShowInVendor")), None)
    v = shown or vs[0]
    return {
        "table": name, "n": len(vs), "shown": shown is not None,
        "price": v.get("Price"), "level": v.get("LevelToUnlock"),
        "req": [x if isinstance(x, str) else x.get("TagName", str(x)) for x in v.get("UnlockRequiredItems", [])],
        "limit": v.get("LifeTimeBuyLimit"), "ent": v.get("bRequiresAccountEntitlement"),
        "sub": ", ".join(short_tag(s, "Vendor.Category.") for s in v.get("Subcategories", [])),
    }


def num(x):
    if x is None:
        return "-"
    return str(int(x)) if float(x) == int(x) else str(x)


class Ctx:
    def __init__(self):
        self.data = wa.Data()
        self.vendor, self.entity = load_tables()
        self.weapons = list(self.data.weapons)
        self.fit = {}
        self.chamber = {}
        for w in self.weapons:
            conts = wa.reachable_containers(self.data, w)
            for it in self.data.attachments:
                if any(wa.accepts(c, it) for c in conts):
                    self.fit.setdefault(it.key, []).append(w)
            for c in w.containers:
                if c["ContainerIdentifier"]["TagName"].endswith("Chamber"):
                    self.chamber[w.key] = [short_tag(t, "Item.Caliber.") for t in c["Filter"].get("AllowedSubSlotContext", [])]
        self.groups = collections.OrderedDict()
        for fam in ("Attachments", "Components", "Platforms"):
            self.groups[fam] = collections.defaultdict(list)
        for it in self.data.items.values():
            m = re.search(r"Weapons/(Attachments|Components|Platforms)/(.*?)/Content/", it.path)
            if m:
                self.groups[m.group(1)][m.group(2)].append(it)

    def wname(self, w):
        return w.display or w.asset

    def fit_group(self, it):
        return tuple(sorted(w.key for w in self.fit.get(it.key, [])))

    def entity_text(self, it, suffix):
        e = self.entity.get(it.item_id.lower())
        if not e:
            return ""
        for kv in e[1].get("AdditionalTexts", []):
            if kv["Key"]["TagName"].endswith(suffix):
                return loc(kv["Value"])
        return ""

    def display(self, it):
        e = self.entity.get(it.item_id.lower())
        return (loc(e[1].get("FriendlyName")) if e else "") or it.display or ""

    def slot(self, it):
        if it.att_type:
            return short_tag(it.att_type, "Item.Attachment.")
        for c in it.context_tags:
            if c.startswith("Item.Attachment."):
                return c[len("Item.Attachment."):].split(".")[0] + "*"
        return "-"

    def provides(self, it):
        out = []
        for c in it.containers:
            tag = short_tag(c["ContainerIdentifier"]["TagName"], "Item.Attachment.")
            fl = c.get("Filter", {})
            n = len(fl.get("AllowedSubSlotItems", [])) + len(fl.get("AllowedSubSlotContext", []))
            out.append(f"{tag} ({fl.get('SupportFilter', '').split('::')[-1]}, {n} allow)")
        return ", ".join(out) or "-"

    def attachment_items(self, fam, everything=False):
        for rest in sorted(self.groups[fam]):
            for it in sorted(self.groups[fam][rest], key=lambda i: i.asset):
                if it.attachment or (everything and not it.ranged):
                    yield rest, it

    def groupmap(self):
        sigs = set()
        for fam in ("Attachments", "Components", "Platforms"):
            for _, it in self.attachment_items(fam, True):
                sigs.add(self.fit_group(it))
        order = sorted(sigs, key=lambda s: (-len(s), s))
        return {s: f"G{i + 1}" for i, s in enumerate(order)}


def platforms(c):
    rows = ["| Weapon | Item id | Folder | Class | Caliber | Price | Unlock lvl | Shop category | Vendor table | Default attachments |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for w in sorted(c.weapons, key=lambda w: (w.archetype, c.wname(w).lower())):
        v = vendor_info(c.vendor.get(w.item_id.lower()))
        m = re.search(r"Weapons/(.*?)/Content/", w.path)
        folder = m.group(1) if m else ""
        lo = wa.Loadout(c.data, w)
        defaults = ", ".join(f"{wa.short_slot(t)}: {c.display(i) or i.asset}" for t, i in lo.attachments()) or "-"
        cal = ", ".join(c.chamber.get(w.key, [])) or "-"
        if v:
            pr = num(v["price"]) + ("" if v["shown"] else " (hidden)")
            vt, ul, sub = f"`{v['table']}`", num(v["level"]), v["sub"]
        else:
            pr, vt, ul, sub = "-", "-", "-", "-"
        rows.append(f"| {cell(c.wname(w))} | `{w.item_id}` | `{folder}` | {w.archetype} | {cell(cal)} | {pr} | {ul} | {cell(sub)} | {vt} | {cell(defaults)} |")
    return "\n".join(rows)


def attachments(c):
    gm = c.groupmap()
    rows = ["| Folder | Item id | Name | Subtitle | Slot | Price | Unlock lvl | Req. items | Buy limit | Variations | Fit | Assets |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for rest, it in c.attachment_items("Attachments"):
        folder = rest.split("/")[-1]
        grp = gm[c.fit_group(it)] if c.fit.get(it.key) else "none"
        v = vendor_info(c.vendor.get(it.item_id.lower()))
        names = [f"`{it.asset}`"]
        for src in (c.entity.get(it.item_id.lower()), c.vendor.get(it.item_id.lower())):
            if src:
                names.append(f"`{src[0]}`")
        if v:
            shop = [num(v["price"]) + ("" if v["shown"] else " (hidden)"), num(v["level"]), cell(", ".join(v["req"]) or "-"),
                    num(v["limit"]) if v["limit"] else "-", str(v["n"])]
        else:
            shop = ["-"] * 5
        rows.append(f"| `{folder}` | `{it.item_id}` | {cell(c.display(it))} | {cell(c.entity_text(it, 'ItemSubtitle')) or '-'} | "
                    f"{c.slot(it)} | " + " | ".join(shop) + f" | {grp} | {' '.join(names)} |")
    return "\n".join(rows)


def components(c, fam="Components"):
    gm = c.groupmap()
    rows = ["| Folder | Asset | Item id | Name | Slot | Provides sub-slots | Fit | Weapons |",
            "|---|---|---|---|---|---|---|---|"]
    for rest, it in c.attachment_items(fam, True):
        folder = rest.split("/")[-1]
        n = len(c.fit.get(it.key, []))
        grp = gm[c.fit_group(it)] if n else "none"
        rows.append(f"| `{folder}` | `{it.asset}` | `{it.item_id}` | {cell(c.display(it)) or '-'} | {c.slot(it)} | "
                    f"{cell(c.provides(it))} | {grp} | {n} |")
    return "\n".join(rows)


def platformparts(c):
    return components(c, "Platforms")


def fitgroups(c):
    gm = c.groupmap()
    counts = collections.Counter()
    for fam in ("Attachments", "Components", "Platforms"):
        for _, it in c.attachment_items(fam, True):
            counts[c.fit_group(it)] += 1
    rows = ["| Fit | Weapons | Items | Weapons that accept the item |", "|---|---|---|---|"]
    for sig, g in sorted(gm.items(), key=lambda kv: int(kv[1][1:])):
        names = ", ".join(sorted(c.wname(c.data.items[k]) for k in sig)) or "none"
        rows.append(f"| {g} | {len(sig)} | {counts[sig]} | {cell(names)} |")
    return "\n".join(rows)


def shoptext(c):
    rows = ["| Item id | Name | Shop text |", "|---|---|---|"]
    for _, it in c.attachment_items("Attachments"):
        d = c.entity_text(it, "ItemDescription")
        if d:
            rows.append(f"| `{it.item_id}` | {cell(c.display(it))} | {cell(d)} |")
    return "\n".join(rows)


def files(c):
    rows = ["| Family | Folder | Files (anim sets omitted) |", "|---|---|---|"]
    for fam in ("Attachments", "Components", "Platforms"):
        base = os.path.join(WROOT, fam)
        by = collections.defaultdict(list)
        for p in sorted(glob.glob(os.path.join(base, "**", "*.json"), recursive=True)):
            stem = os.path.basename(p)[:-5]
            if stem.startswith("AnimSet_"):
                continue
            rel = os.path.relpath(p, base).replace(os.sep, "/")
            by[rel.split("/Content/")[0]].append(stem)
        for folder in sorted(by):
            rows.append(f"| {fam} | `{folder}` | {' '.join('`' + s + '`' for s in by[folder])} |")
    return "\n".join(rows)


RENDER = {"platforms": platforms, "platformparts": platformparts, "attachments": attachments, "components": components,
          "fitgroups": fitgroups, "shoptext": shoptext, "files": files}


def write(c):
    with open(PAGE, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    for name in BLOCKS:
        pat = re.compile(rf"<!-- weapon_vendor_tables {name} -->.*?<!-- /weapon_vendor_tables {name} -->", re.S)
        if not pat.search(text):
            raise SystemExit(f"error: no markers for {name} in {os.path.basename(PAGE)}")
        body = RENDER[name](c).replace("\n", nl)
        text = pat.sub(lambda _: f"<!-- weapon_vendor_tables {name} -->{nl}{body}{nl}<!-- /weapon_vendor_tables {name} -->", text)
    with open(PAGE, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    c = Ctx()
    if "--write" in sys.argv:
        write(c)
        return
    n_att = sum(1 for _ in c.attachment_items("Attachments"))
    n_cmp = sum(1 for _ in c.attachment_items("Components"))
    print(f"weapons {len(c.weapons)}, attachment items {n_att}, component items {n_cmp}, "
          f"vendor rows {len(c.vendor)}, entity rows {len(c.entity)}, fit groups {len(c.groupmap())}")


if __name__ == "__main__":
    main()
