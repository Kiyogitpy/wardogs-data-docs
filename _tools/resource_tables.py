"""Generated table of resource and ammunition item definitions.

Reads the exported JSON under data/Wardogs/Content/Items/Resources/ (multi-export
files are split on their `--- export: <Class> / <Name> ---` headers, the same way
the other generators do). One row per BHInventoryItemDefinition asset. The other
files in the folder (audio data, projectile data, curve table) are not item
definitions and get no row.

Columns come from the item's fragments and tags:
    Item tag      ItemId.TagName
    Display name  UI row in data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_*.json
                  (FriendlyName, matched on the row key = item tag; tags compared
                  without case, as gameplay tags are), else the item's DisplayName
    Kind          "ammo" when ItemContext has Item.Ammo (or an Item.Ammo.* tag), "supplies" / "currency" for
                  Item.Supplies / Item.Currency, else "other"
    Max stack     BHInventoryFragment_Stackable.MaxStackSize, plus any MaxStackSizeOverrides
    Inventory     BHInventoryFragment_CustomShape.Dimensions as X x Y
    Weight        BHInventoryFragment_Weight.Weight
    Caliber tag   ItemContext entries starting with Item.Caliber.
    Vendor price  VendorItemVariations.Price where VariationTag equals the item tag
                  (vendor tables under GameMechanics/WorldInteractable/NPCs/Vendor)

A cell is "—" when the data does not have the value. Nothing is inferred.

    python _tools/resource_tables.py            # table to stdout
    python _tools/resource_tables.py --write    # refresh the marker block in the doc, in place

Block in the doc looks like:
    <!-- resource_tables items --> ... <!-- /resource_tables -->
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOC = "content/Wardogs_Items_v2.md"
RESOURCES = "Wardogs/Content/Items/Resources"
UI_ENTITIES = "Wardogs/Content/UI/Data/Entities"
VENDOR = "Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor"

EXPORT_HDR = re.compile(r"^--- export: .*?---\s*$", re.M)
REF = re.compile(r"'([^']*)'")
FRAGMENT_PREFIXES = ("BHInventoryFragment_", "WDInventoryFragment_")


def exports(path):
    """Return the list of export dicts in one data file."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    out = []
    for blk in EXPORT_HDR.split(text):
        blk = blk.strip()
        if blk.startswith("{"):
            out.append(json.loads(blk))
    return out


def json_files(rel):
    return sorted(glob.glob(os.path.join(DATA, rel, "**", "*.json"), recursive=True))


def tag_of(val):
    if isinstance(val, dict):
        return val.get("TagName", "") or ""
    return ""


def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def fmt_num(v):
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def ui_names():
    """Map lower-cased item tag -> display string from the UI entity tables."""
    names = {}
    for f in json_files(UI_ENTITIES):
        for ex in exports(f):
            if ex.get("Type") != "DataTable":
                continue
            for key, row in (ex.get("Rows") or {}).items():
                fn = row.get("FriendlyName") or {}
                txt = fn.get("SourceString") or fn.get("CultureInvariantString") or ""
                if txt:
                    names.setdefault(key.lower(), txt)
    return names


def vendor_prices():
    """Map lower-cased item tag -> list of vendor prices (as written in the table)."""
    prices = {}
    for f in json_files(VENDOR):
        for ex in exports(f):
            if ex.get("Type") != "DataTable":
                continue
            for row in (ex.get("Rows") or {}).values():
                for var in row.get("VendorItemVariations") or []:
                    tag = tag_of(var.get("VariationTag")).lower()
                    if tag and var.get("Price") is not None:
                        vals = prices.setdefault(tag, [])
                        p = fmt_num(var["Price"])
                        if p not in vals:
                            vals.append(p)
    return prices


def item_row(path, ex, exps_by_type, names, prices):
    p = ex.get("Properties") or {}
    tag = tag_of(p.get("ItemId"))
    ctx = [c for c in p.get("ItemContext") or [] if isinstance(c, str)]
    if any(c == "Item.Ammo" or c.startswith("Item.Ammo.") for c in ctx):
        kind = "ammo"
    elif "Item.Supplies" in ctx:
        kind = "supplies"
    elif "Item.Currency" in ctx:
        kind = "currency"
    else:
        kind = "other"

    def frag(ftype):
        found = exps_by_type.get(ftype) or []
        return (found[0].get("Properties") or {}) if found else None

    stack = frag("BHInventoryFragment_Stackable")
    max_stack = "—"
    if stack is not None and "MaxStackSize" in stack:
        max_stack = fmt_num(stack["MaxStackSize"])
        ovr = stack.get("MaxStackSizeOverrides") or []
        if ovr:
            parts = [f"{tag_of(o.get('Key'))} {fmt_num(o.get('Value'))}" for o in ovr]
            max_stack += " (overrides: " + ", ".join(parts) + ")"

    shape = frag("BHInventoryFragment_CustomShape")
    dims = (shape or {}).get("Dimensions") or {}
    inv = f"{fmt_num(dims['X'])} x {fmt_num(dims['Y'])}" if "X" in dims and "Y" in dims else "—"

    weight_frag = frag("BHInventoryFragment_Weight")
    weight = fmt_num(weight_frag["Weight"]) if weight_frag and "Weight" in weight_frag else "—"

    calibers = [c for c in ctx if c.startswith("Item.Caliber.")]
    display = names.get(tag.lower()) or ((p.get("DisplayName") or {}).get("SourceString") or "")
    vp = prices.get(tag.lower())

    return {
        "asset": ex.get("Name", ""),
        "folder": os.path.relpath(os.path.dirname(path), os.path.join(DATA, RESOURCES)).replace("\\", "/"),
        "tag": tag,
        "display": display,
        "kind": kind,
        "stack": max_stack,
        "inv": inv,
        "weight": weight,
        "caliber": ", ".join(calibers),
        "price": " / ".join(vp) if vp else "",
    }


def rows():
    names = ui_names()
    prices = vendor_prices()
    out = []
    for f in json_files(RESOURCES):
        exps = exports(f)
        exps_by_type = {}
        for e in exps:
            t = e.get("Type", "")
            if t.startswith(FRAGMENT_PREFIXES):
                exps_by_type.setdefault(t, []).append(e)
        for ex in exps:
            if ex.get("Type") == "BHInventoryItemDefinition":
                out.append(item_row(f, ex, exps_by_type, names, prices))
    return sorted(out, key=lambda r: (r["folder"], r["asset"]))


def table():
    rs = rows()
    lines = ["| Asset | Folder | Item tag | Display name | Kind | Max stack | Inventory (X x Y) | Weight | Caliber tag | Vendor price |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rs:
        lines.append(
            f"| `{r['asset']}` | {md(r['folder'])} | `{r['tag'] or '—'}` | {md(r['display']) or '—'} | {r['kind']} | "
            f"{md(r['stack'])} | {r['inv']} | {r['weight']} | {md(r['caliber']) or '—'} | {r['price'] or '—'} |")
    return lines, len(rs)


BLOCK = re.compile(r"<!-- resource_tables items -->\r?\n.*?<!-- /resource_tables -->", re.S)


def write_doc():
    path = os.path.join(ROOT, DOC)
    with open(path, encoding="utf-8", newline="") as fh:
        text = fh.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    lines, n = table()

    def regen(m):
        return nl.join(["<!-- resource_tables items -->"] + lines + ["<!-- /resource_tables -->"])

    new, count = BLOCK.subn(regen, text)
    if count != 1:
        raise SystemExit(f"{DOC}: expected 1 resource_tables block, found {count}")
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
    print(f"{n} item rows")
    print(f"{DOC}: 1 table {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv[1:]:
        write_doc()
        return
    lines, n = table()
    print("\n".join(lines))
    print(f"\n{n} rows", file=sys.stderr)


if __name__ == "__main__":
    main()
