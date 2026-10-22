"""Generated glossary of gameplay-tag display text.

Reads every DataTable whose RowStruct is WDUIGameplayTagToTextTableRow under data/
(multi-export files are split on their `--- export: <Class> / <Name> ---` headers,
the same way the other generators do). One markdown section per table: the row's
gameplay tag, the display text (Text.SourceString, else the string-table key), and
any TaggedText entries that carry text.

    python _tools/tag_text_tables.py            # all tables to stdout
    python _tools/tag_text_tables.py --write    # refresh the marker block in the doc, in place

Block in the doc looks like:
    <!-- tag_text_tables all --> ... <!-- /tag_text_tables -->
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOC = "content/Wardogs_TagDisplayText_v1.md"
ROW_STRUCT = "WDUIGameplayTagToTextTableRow"

EXPORT_HDR = re.compile(r"^--- export: .*?---\s*$", re.M)


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


def md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def text_of(val):
    """A localized value: SourceString, else CultureInvariantString, else empty."""
    if not isinstance(val, dict):
        return ""
    return val.get("SourceString") or val.get("CultureInvariantString") or ""


def tables():
    """Return [(table name, data path, [row dicts sorted by tag])], sorted by table name."""
    out = []
    for f in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        with open(f, encoding="utf-8") as fh:
            head = fh.read()
        if ROW_STRUCT not in head:
            continue
        for ex in exports(f):
            if ex.get("Type") != "DataTable":
                continue
            rs = (ex.get("Properties") or {}).get("RowStruct") or {}
            if ROW_STRUCT not in rs.get("ObjectName", ""):
                continue
            rows = []
            for name, row in (ex.get("Rows") or {}).items():
                tag = (row.get("Tag") or {}).get("TagName", "")
                text = row.get("Text") or {}
                src = text.get("SourceString") or ""
                key = text.get("Key") or ""
                extra = []
                for entry in row.get("TaggedText") or []:
                    val = text_of(entry.get("Value"))
                    if val:
                        extra.append(f"{entry.get('Key', '')}: {val}")
                rows.append({
                    "row": name,
                    "tag": tag,
                    "display": src,
                    "key": key,
                    "extra": extra,
                })
            rows.sort(key=lambda r: (r["tag"] if r["tag"] not in ("", "None") else r["row"], r["row"]))
            out.append((ex.get("Name"), f, rows))
    return sorted(out, key=lambda t: t[0])


def render():
    """Return (lines, table count, row count)."""
    lines = []
    n_tables = 0
    n_rows = 0
    for name, path, rows in tables():
        n_tables += 1
        n_rows += len(rows)
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"Source: `{rel(path)}` ({len(rows)} rows)")
        lines.append("")
        lines.append("| Gameplay tag | Display text | Other text |")
        lines.append("|---|---|---|")
        for r in rows:
            if r["tag"] in ("", "None"):
                tag_cell = f"`{r['row']}` (tag None)"
            else:
                tag_cell = f"`{r['tag']}`"
            if r["display"]:
                disp = md(r["display"].strip())
            elif r["key"]:
                disp = f"`{r['key']}` (string key, no source text)"
            else:
                disp = "—"
            extra = md("; ".join(r["extra"])) or "—"
            lines.append(f"| {tag_cell} | {disp} | {extra} |")
        lines.append("")
    return lines, n_tables, n_rows


BLOCK = re.compile(r"<!-- tag_text_tables all -->\r?\n.*?<!-- /tag_text_tables -->", re.S)


def write_doc():
    path = os.path.join(ROOT, DOC)
    with open(path, encoding="utf-8", newline="") as fh:
        text = fh.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    lines, n_tables, n_rows = render()
    block = nl.join(["<!-- tag_text_tables all -->"] + lines + ["<!-- /tag_text_tables -->"])
    new, n = BLOCK.subn(lambda m: block, text)
    if n != 1:
        raise SystemExit(f"expected one tag_text_tables block in {DOC}, found {n}")
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
    print(f"{n_tables} tables, {n_rows} rows")
    print(f"{DOC}: {'updated' if new != text else 'unchanged'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--write" in sys.argv[1:]:
        write_doc()
        return
    lines, n_tables, n_rows = render()
    print("\n".join(lines))
    print(f"{n_tables} tables, {n_rows} rows", file=sys.stderr)


if __name__ == "__main__":
    main()
