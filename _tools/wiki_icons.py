"""Put the item icon at the top of each wiki infobox.

Matches every article under _wiki/ that has an infobox (a table ending in `{: .wiki-infobox }`)
to assets/data/item-icons.json: first by the backticked ids in the infobox "Internal name"
row, then by the article title against the icon file's FriendlyName. The icon is the vendor
texture, else the inventory (3D) one, else the fallback. It is written as the first body row
of the table, `| ![Title]({{ '/assets/img/icons/...png' | relative_url }}){: .wiki-infobox-img } | |`, and is
replaced in place on re-runs, so the tool is idempotent.

    python _tools/wiki_icons.py            # insert or update the image rows
    python _tools/wiki_icons.py --check    # change nothing; exit 1 if any row is out of date

Generated articles (_tools/wiki_weapons.py) call image_row() themselves, so the generator
output and this tool agree.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "assets", "data", "item-icons.json")
ITEM_DIRS = ("weapons", "attachments", "equipment", "vehicles", "building", "ammunition")
IMG_ROW = re.compile(r"^\| !\[[^\]]*\]\([^)]*\)\{: \.wiki-infobox-img \} \| \|[ \t]*$")
TICKS = re.compile(r"`([^`]+)`")

# Articles whose name or id does not line up with the icon file; hand-picked item ids.
OVERRIDES = {}

_items = None


def items():
    global _items
    if _items is None:
        with open(ICONS, encoding="utf-8") as f:
            raw = json.load(f)["items"]
        _items = {k.lower(): v for k, v in raw.items()}
    return _items


def best_png(entry):
    """Vendor icon, else inventory/3D, else fallback; None when the item has none."""
    for key in ("vendor", "inventory", "fallback"):
        v = entry.get(key)
        if v and v.get("png") and os.path.exists(os.path.join(ROOT, v["png"])):
            return v["png"]
    return None


def candidates(i):
    """Spellings an infobox id may have in the data: as written, Id.Item./Id.Buildable. prefixed,
    DA_Buildable_X as Id.Buildable.X, and a vehicle code like ROT_01 as its default variant."""
    yield i
    yield "Id.Item." + i
    yield "Id.Buildable." + i
    m = re.match(r"DA_Buildable_(.+)$", i)
    if m:
        yield "Id.Buildable." + m.group(1)
        yield "Id.Buildable." + m.group(1).replace("_", "")
    for k in items():
        if re.fullmatch(r"vehicle\.variant\..*\." + re.escape(i.lower()) + r"\.default", k):
            yield k


def lookup(ids, title=None):
    table = items()
    for i in ids:
        for c in candidates(i):
            e = table.get(c.lower())
            if e and best_png(e):
                return best_png(e)
    if title:
        t = title.lower()
        hits = {}
        for k, e in table.items():
            if e.get("name", "").lower() == t and best_png(e):
                hits.setdefault(best_png(e), k)
        if len(hits) > 1:  # the same name on map markers and variants: keep the Id.* item itself
            hits = {p: k for p, k in hits.items() if k.startswith("id.")}
        if len(hits) == 1:
            return next(iter(hits))
    return None


def site_url(png):
    """Liquid that resolves to the icon under the site's baseurl. Document-relative paths break
    because a page at _wiki/x/y.md is served one folder deeper, at /wiki/x/y/."""
    return "{{ '/" + png + "' | relative_url }}"


def image_row(page_path, title, ids=(), key=None):
    """The markdown row for a page, or None. page_path is the article's own path."""
    png = lookup(ids, title)
    if not png:
        return None
    rel = site_url(png)
    alt = title.replace("[", "").replace("]", "")
    return f"| ![{alt}]({rel}){{: .wiki-infobox-img }} | |"


def split_front(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    return (m.group(1), m.end()) if m else ("", 0)


def inject(text, path):
    """Return (new_text, has_icon, has_infobox) for an article's text. path locates the page for
    the relative image link; the generators call this on their own output."""
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    end = next((i for i, l in enumerate(lines) if l.strip() == "{: .wiki-infobox }"), None)
    if end is None:
        return text, False, False
    start = end
    while start > 0 and lines[start - 1].startswith("|"):
        start -= 1
    table = lines[start:end]
    ids = []
    for l in table:
        if l.startswith("| Internal name"):
            cell = l.split("|")[2].strip() if l.count("|") >= 3 else ""
            ids += TICKS.findall(cell) or ([cell] if cell else [])
    front, _ = split_front(text)
    tm = re.search(r'^title:\s*"?(.*?)"?\s*$', front, re.M)
    title = tm.group(1) if tm else os.path.splitext(os.path.basename(path))[0]
    key = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if key.split("/")[1] not in ITEM_DIRS:  # only item sections get icons; a title like "Wagers" is not an item
        return nl.join([l for l in lines if not IMG_ROW.match(l)]), False, True
    row = image_row(path, title, OVERRIDES.get(key, []) + ids)
    body = [l for l in table if not IMG_ROW.match(l)]
    new = body[:2] + [row] + body[2:] if row else body
    return nl.join(lines[:start] + new + lines[end:]), bool(row), True


# ---- small icon column in the part tables and the Vehicles hub ------------------------------

ICON_CELL = re.compile(r"^\| (?:!\[[^\]]*\]\([^)]*\)\{: \.wiki-icon \})? \|")
LINK_CELL = re.compile(r"^\| \[([^\]]+(?:\[[^\]]*\])?[^\]]*)\]\(([^)\s]+\.md)\)")
SEP_ROW = re.compile(r"^\|[-: |]+\|?\s*$")
# page -> (first-column header the icon column goes in front of, how a row finds its icon)
ICON_TABLES = {
    "attachments": ("Part", "name"),
    "vehicles.md": ("Vehicle", "link"),
}


def name_icons():
    """Part name -> icon png, only where the name is unique among items that have an icon."""
    by = {}
    for k, e in items().items():
        n, png = e.get("name", "").strip().lower(), best_png(e)
        if n and png:
            by.setdefault(n, set()).add(png)
    return {n: next(iter(v)) for n, v in by.items() if len(v) == 1}


def article_png(page_dir, target):
    """The icon an article already carries in its infobox, as a repo-relative png path."""
    path = os.path.normpath(os.path.join(page_dir, target))
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    m = re.search(r"^\| !\[[^\]]*\]\(([^)]+)\)\{: \.wiki-infobox-img \} \| \|", text, re.M)
    if not m:
        return None
    lm = re.match(r"\{\{ '/([^']+)' \| relative_url \}\}", m.group(1))
    if lm:
        return lm.group(1)
    return os.path.relpath(os.path.normpath(os.path.join(os.path.dirname(path), m.group(1))), ROOT).replace(os.sep, "/")


def add_icon_columns(text, path):
    """Put a 48px icon in front of the first column of the named tables. Idempotent: an existing
    icon column is stripped and rebuilt."""
    key = os.path.relpath(path, ROOT).replace(os.sep, "/").split("/")
    spec = ICON_TABLES.get(key[1]) if len(key) > 2 or key[1] in ICON_TABLES else None
    if not spec:
        return text
    head, mode = spec
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    names = name_icons() if mode == "name" else None
    page_dir = os.path.dirname(os.path.abspath(path))
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        has = l.startswith("| | ")
        orig = l[2:] if has else l
        if orig.startswith(f"| {head} |") and i + 1 < len(lines) and SEP_ROW.match(lines[i + 1]):
            sep = lines[i + 1][4:] if has else lines[i + 1]
            head_rows, body_rows, any_icon = ["| " + orig, "|---" + sep], [], False
            plain = [orig, sep]  # the table without the icon column
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                r = lines[i]
                if has and ICON_CELL.match(r):
                    r = "|" + r[ICON_CELL.match(r).end():]
                plain.append(r)
                cell = r[1:].lstrip()
                png, name = None, ""
                if mode == "name":
                    name = cell.split(" |", 1)[0].strip()
                    png = names.get(name.lower())
                else:
                    m = LINK_CELL.match(r)
                    if m:
                        name, png = m.group(1), article_png(page_dir, m.group(2))
                if png:
                    any_icon = True
                    rel = site_url(png)
                    alt = name.replace("[", "").replace("]", "")
                    body_rows.append(f"| ![{alt}]({rel}){{: .wiki-icon }} {r}")
                else:
                    body_rows.append(f"|  {r}")
                i += 1
            out += (head_rows + body_rows) if any_icon else plain  # no icon in the table: no column
            continue
        out.append(l)
        i += 1
    return nl.join(out)


def process(path, write):
    """Return (status, changed). status: 'none' no infobox, 'missing', 'ok'."""
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    new_text, has_icon, has_box = inject(text, path)
    new_text = add_icon_columns(new_text, path)
    if not has_box:
        if new_text == text:
            return "none", False
        if write:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_text)
        return "none", True
    changed = new_text != text
    if changed and write:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)
    return ("ok" if has_icon else "missing"), changed




def main(argv):
    check = "--check" in argv
    with_img, missing, stale, other = 0, [], [], 0
    for path in sorted(glob.glob(os.path.join(ROOT, "_wiki", "**", "*.md"), recursive=True)):
        status, changed = process(path, write=not check)
        if status == "none":
            continue
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        if status == "ok":
            with_img += 1
            if changed and check:
                stale.append(rel)
        elif rel.split("/")[1] in ITEM_DIRS:
            missing.append(rel)
        else:
            other += 1
        if status == "missing" and changed and check:
            stale.append(rel)
    print(f"{with_img} infobox articles with an image")
    print(f"{other} infobox articles outside the item sections (no icon expected)")
    print(f"{len(missing)} item-section infobox articles without an icon:")
    for m in missing:
        print("  " + m)
    if stale:
        print(f"{len(stale)} out of date (run without --check):")
        for m in stale:
            print("  " + m)
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
