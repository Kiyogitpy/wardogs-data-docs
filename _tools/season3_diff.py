"""Literal Season 2 -> Season 3 saved-export comparison (stdlib only).

Run with --s2 DIR --s3 DIR --out DIR and one of --write/--check/--stats.
Both --s2-manifest and --s3-manifest are required frozen input inventories:
{"source": {...public provenance...}, "files": [{"path": relative POSIX path,
"bytes": integer, "sha256": hex digest}, ...]}. They cover ALL files, including
non-JSON files (hashed/accounted, not property-compared). Missing, extra, changed,
duplicate or malformed evidence rejects the entire run before output writes.
No acquisition, Git operations, mapping repair or inferred identity matching.

Public reproduction (extract Git 8d0d6a9a:data into an S2 data directory):
python -I -B _tools/season3_diff.py --s2 S2_DATA --s3 data --out assets/data/season3-diff
  --s2-manifest assets/data/season3-diff/manifest-s2.json
  --s3-manifest assets/data/season3-diff/manifest-s3.json --check
Use --write instead to regenerate. Input/output JSON is UTF-8; no private defaults.
"""

import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
# Only presentation taxonomy is shared; never call the historical comparator.
from season_diff import AREAS, classify

HEADER = re.compile(r"^--- export: (.+?) ---\r?$", re.M)
MISSING = object()
SPLIT_BYTES = 5 * 1024 * 1024
INLINE_BYTES = 1024
NOISE = dict.fromkeys(("renamed_keys", "ref_shifts", "dup_keys", "swapped_keys",
                       "type_reinterpret"), 0)
LIMITS = [
    "Public scope is the committed S2 and S3 Git data trees only. The 31 ignored local supplemental non-JSON files are excluded and must not be published or supplied as public comparison input.",
    "File-only counts describe saved-snapshot presence, not game removals or additions.",
    "Old saved JSON was not independently reparsed from its original containers.",
    "Current CL533731/hotfix533689 uses preferred map21234bab: 7082 Cue outputs plus curated config; broad parse still has 3 UI errors and 5 warnings.",
    "Absent output is not evidence of game removal. Mapping effects remain unresolved; literal label/value differences do not prove field renames, swapped fields, native semantics or gameplay.",
    "Files pair only by exact relative path; exports by exact full header and occurrence; arrays by ordered index. No tolerance, aliasing, reference-index suppression or inferred identities.",
    "Non-JSON input files are fully inventoried and hashed, but not property-compared.",
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dumps(value):
    """Emit exact JSON decimals without a float round-trip, including typed 1.0."""
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("non-finite number")
        text = str(value)
        return text if any(c in text for c in ".eE") else text + ".0"
    if isinstance(value, dict):
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + dumps(v)
                                for k, v in value.items()) + "}"
    if isinstance(value, list):
        return "[" + ",".join(dumps(v) for v in value) + "]"
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def pairs_hook(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate object key: " + repr(key))
        out[key] = value
    return out


def reject_constant(value):
    raise ValueError("non-JSON constant: " + value)


def load_json(text):
    return json.loads(text, object_pairs_hook=pairs_hook, parse_float=Decimal,
                      parse_constant=reject_constant)


def parse_exports(text):
    """Fully consume ordinary JSON or header-delimited JSON; retain identity/order."""
    headers = list(HEADER.finditer(text))
    if not headers:
        return [("$document", load_json(text))]
    if text[:headers[0].start()].strip():
        raise ValueError("unexpected content before first export")
    out = []
    for i, header in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        out.append((header.group(1), load_json(text[header.end():end])))
    return out


def kind(value):
    if value is MISSING:
        return "missing"
    return {type(None): "null", bool: "boolean", int: "integer", Decimal: "decimal",
            str: "string", dict: "object", list: "array"}[type(value)]


def diff_value(before, after, tokens, export, changes):
    """Walk literal properties and array indexes; containers appear only once."""
    bk, ak = kind(before), kind(after)
    if bk == ak == "object":
        for key in sorted(before.keys() | after.keys()):
            diff_value(before.get(key, MISSING), after.get(key, MISSING),
                       tokens + [key], export, changes)
        return
    if bk == ak == "array":
        for i in range(max(len(before), len(after))):
            diff_value(before[i] if i < len(before) else MISSING,
                       after[i] if i < len(after) else MISSING,
                       tokens + [i], export, changes)
        return
    if bk == ak and before == after:
        if bk != "decimal" or before.is_signed() == after.is_signed() or before != 0:
            return
    pointer = "/" + "/".join(str(t).replace("~", "~0").replace("/", "~1") for t in tokens) if tokens else ""
    change = {"path": dumps(export) + "::" + (pointer or "$"),
              "pointer": pointer, "tokens": tokens, "export": export,
              "op": "added" if before is MISSING else "removed" if after is MISSING else "changed",
              "before_type": bk, "after_type": ak}
    for label, value in (("before", before), ("after", after)):
        if value is not MISSING:
            change[label] = value
            if kind(value) in ("integer", "decimal"):
                change[label + "_literal"] = str(value)
    changes.append(change)


def export_map(exports):
    counts = Counter()
    out = {}
    for header, obj in exports:
        counts[header] += 1
        out[(header, counts[header])] = obj
    return out


def value_summary(value):
    data = dumps(value).encode()
    return {"type": kind(value), "count": len(value), "json_bytes": len(data), "content_sha256": sha(data)}


def browser_safe(value):
    if type(value) is int:
        return abs(value) <= 2 ** 53
    if isinstance(value, Decimal):
        return Decimal(str(float(value))) == value and not (value.is_zero() and value.is_signed())
    if isinstance(value, dict):
        return all(browser_safe(v) for v in value.values())
    if isinstance(value, list):
        return all(browser_safe(v) for v in value)
    return True


def compact_changes(asset):
    """Share export identities and replace large values with lossless source references."""
    identities = sorted({tuple(c["export"]) for c in asset["changes"]})
    indexes = {identity: i for i, identity in enumerate(identities)}
    rows = []
    for change in asset["changes"]:
        row = {k: v for k, v in change.items() if k not in ("export", "tokens", "pointer")}
        row["path"] = str(indexes[tuple(change["export"])]) + "::" + (change["pointer"] or "$")
        for label, side in (("before", "s2"), ("after", "s3")):
            if label not in row:
                continue
            value = row[label]
            if isinstance(value, (dict, list, str)) and len(dumps(value).encode()) > INLINE_BYTES:
                ref = {"side": side, "file": asset["path"], "file_sha256": asset[label + "_sha256"],
                       "export": change["export"], "pointer": change["pointer"]}
                ref.update(value_summary(value))
                row[label] = {"$saved_export": ref}
            elif kind(value) in ("integer", "decimal"):
                if browser_safe(value):
                    row.pop(label + "_literal", None)
            elif isinstance(value, (dict, list)) and not browser_safe(value):
                row[label + "_literal"] = dumps(value)
        rows.append(row)
    return [list(identity) for identity in identities], rows


def resolve_reference(wrapper, root, manifest):
    """Resolve and validate a public reference against a supplied pinned saved-input tree."""
    ref = wrapper["$saved_export"]
    if ref["side"] not in ("s2", "s3"):
        raise ValueError("invalid source-reference side")
    pins = {r["path"]: r for r in manifest["files"]}
    pin = pins[ref["file"]]
    path = Path(ref["file"])
    if path.is_absolute() or ".." in path.parts or ":" in ref["file"] or "\\" in ref["file"]:
        raise ValueError("invalid reference path")
    data = (Path(root) / path).read_bytes()
    if sha(data) != pin["sha256"] or ref["file_sha256"] != pin["sha256"] or len(data) != pin["bytes"]:
        raise ValueError("source-reference file hash mismatch")
    value = export_map(parse_exports(data.decode("utf-8-sig")))[tuple(ref["export"])]
    pointer = ref["pointer"]
    if pointer:
        if not pointer.startswith("/"):
            raise ValueError("invalid reference JSON pointer")
        for token in pointer[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            value = value[int(token)] if isinstance(value, list) else value[token]
    if value_summary(value) != {k: ref[k] for k in ("type", "count", "json_bytes", "content_sha256")}:
        raise ValueError("source-reference value summary mismatch")
    return value


def inventory(root):
    root = Path(root)
    if not root.is_dir():
        raise ValueError("input directory is missing")
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("symlink input is not supported")
        if path.is_file():
            data = path.read_bytes()
            rows.append({"path": path.relative_to(root).as_posix(),
                         "bytes": len(data), "sha256": sha(data)})
    if not any(r["path"].lower().endswith(".json") for r in rows):
        raise ValueError("input contains no JSON files")
    return sorted(rows, key=lambda row: row["path"])


def validate_manifest(root, manifest):
    rows = manifest["files"]
    paths = [r["path"] for r in rows]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate manifest path")
    for row in rows:
        path = row["path"]
        if not isinstance(path, str) or "\\" in path or ":" in path or path.startswith("/") or any(p in ("", ".", "..") for p in path.split("/")):
            raise ValueError("manifest path must be relative POSIX")
        if set(row) != {"path", "bytes", "sha256"} or type(row["bytes"]) is not int or row["bytes"] < 0 or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise ValueError("invalid manifest row")
    actual = inventory(root)
    if sorted(rows, key=lambda r: r["path"]) != actual:
        raise ValueError("input differs from frozen all-path manifest (missing, extra or changed file)")
    return actual


def snapshot(root, manifest, side):
    rows = validate_manifest(root, manifest)
    source = manifest["source"]
    if not isinstance(source, dict) or not source.get("revision"):
        raise ValueError("manifest source requires a public revision label")
    # Provenance is explicit allowlisted public metadata; never copy arbitrary paths.
    public_source = {k: source[k] for k in ("revision", "build", "schema", "provenance") if k in source}
    if any(not isinstance(v, str) or re.search(r"(?:(?<![A-Za-z])[A-Za-z]:[/\\]|/Users/|/home/|file://)", v) for v in public_source.values()):
        raise ValueError("source metadata must contain public labels, not local paths")
    public_source.update(label="Season 2" if side == "s2" else "Season 3",
                         content_sha256=sha(dumps(rows).encode()), files=len(rows))
    return rows, public_source


def render(s2, s3, manifest2, manifest3):
    rows2, source2 = snapshot(s2, manifest2, "s2")
    rows3, source3 = snapshot(s3, manifest3, "s3")
    maps = [{r["path"]: r for r in rows} for rows in (rows2, rows3)]
    assets = []
    accounting = Counter({prefix + status: 0 for prefix in ("json_", "non_json_")
                          for status in ("added", "removed", "modified", "unchanged")})
    accounting.update(dict.fromkeys(("json_paired", "json_literal_equal", "json_literal_changed",
                                     "json_format_only", "json_export_order_changed"), 0))
    file_rows = []
    for path in sorted(maps[0].keys() | maps[1].keys()):
        old, new = maps[0].get(path), maps[1].get(path)
        is_json = path.lower().endswith(".json")
        ex = []
        for root, row in ((s2, old), (s3, new)):
            if row and is_json:
                data = (Path(root) / path).read_bytes()
                if sha(data) != row["sha256"]:
                    raise ValueError("input changed during read: " + path)
                try:
                    ex.append(parse_exports(data.decode("utf-8-sig")))
                except (ValueError, UnicodeError) as error:
                    raise ValueError(path + ": " + str(error)) from error
            else:
                ex.append([])
        status = "added" if old is None else "removed" if new is None else "unchanged" if old["sha256"] == new["sha256"] else "modified"
        file_rows.append({"path": path, "status": status, "comparison": "literal-json" if is_json else "hash-only",
                          "before": old, "after": new})
        accounting[("json_" if is_json else "non_json_") + status] += 1
        if not is_json:
            continue
        em2, em3 = [export_map(e) for e in ex]
        changes = []
        for identity in sorted(em2.keys() | em3.keys()):
            diff_value(em2.get(identity, MISSING), em3.get(identity, MISSING), [],
                       list(identity), changes)
        order2, order3 = [list(e) for e in em2], [list(e) for e in em3]
        order_changed = order2 != order3
        if old and new:
            accounting["json_paired"] += 1
            accounting["json_literal_equal" if not changes and not order_changed else "json_literal_changed"] += 1
            accounting["json_export_order_changed"] += int(order_changed)
        file_rows[-1].update(exports_before=order2, exports_after=order3,
                             literal_changes=len(changes), export_order_changed=order_changed)
        if status == "unchanged":
            continue
        if old and new and not changes and not order_changed:
            accounting["json_format_only"] += 1
        present = ex[1] or ex[0]
        typ = next((o.get("Type") for _, o in present if isinstance(o, dict) and o.get("Type")), None)
        area = classify(path, [(h, o) for h, o in present if isinstance(o, dict)])
        assets.append({"name": Path(path).stem, "path": path, "old_path": None,
                       "status": status, "type": typ, "paired_by": None,
                       "changes": changes, "noise": NOISE.copy(), "exports": len(ex[1] or ex[0]),
                       "export_order_before": order2, "export_order_after": order3,
                       "export_order_changed": order_changed,
                       "before_sha256": old["sha256"] if old else None,
                       "after_sha256": new["sha256"] if new else None,
                       "source_before": source2, "source_after": source3,
                       "note": "Snapshot presence only; not a game removal/addition." if not (old and new) else "Literal saved-export comparison; schema/mapping effects unresolved.",
                       "_area": area})
    # Recheck both complete inventories before returning anything writeable.
    validate_manifest(s2, manifest2)
    validate_manifest(s3, manifest3)
    files, areas = {}, []
    totals = dict.fromkeys(("assets_added", "assets_removed", "assets_modified", "assets_moved",
                            "noise_only_assets", "property_changes", "removed_values", "added_values"), 0)
    totals.update({"noise_" + key: 0 for key in NOISE})
    for area, title in AREAS:
        mine = [a for a in assets if a["_area"] == area]
        counts = dict.fromkeys(("added", "removed", "modified", "moved", "property_changes", "removed_values", "added_values"), 0)
        chunks, chunk, size = [], [], 0
        for asset in mine:
            counts[asset["status"]] += 1
            if asset["status"] == "modified":
                counts["property_changes"] += len(asset["changes"])
            elif asset["status"] == "removed":
                counts["removed_values"] += len(asset["changes"])
            elif asset["status"] == "added":
                counts["added_values"] += len(asset["changes"])
            public = {k: v for k, v in asset.items() if k != "_area"}
            public["change_exports"], public["changes"] = compact_changes(asset)
            line = dumps(public)
            if chunk and size + len(line.encode()) > SPLIT_BYTES:
                chunks.append(chunk)
                chunk, size = [], 0
            chunk.append(line)
            size += len(line.encode()) + 2
        chunks.append(chunk)
        names = []
        for i, chunk in enumerate(chunks, 1):
            name = area + ("-" + str(i) if len(chunks) > 1 else "") + ".json"
            names.append(name)
            files[name] = '{"area":' + dumps(area) + ',"assets":[\n' + ",\n".join(chunk) + "\n]}\n"
        areas.append({"id": area, "title": title, "file": names[0] if len(names) == 1 else names,
                      "counts": counts, "count_semantics": "saved-snapshot presence only"})
        for status in ("added", "removed", "modified", "moved"):
            totals["assets_" + status] += counts[status]
        for key in ("property_changes", "removed_values", "added_values"):
            totals[key] += counts[key]
    files["manifest-s2.json"] = dumps({"source": source2, "files": rows2}) + "\n"
    files["manifest-s3.json"] = dumps({"source": source3, "files": rows3}) + "\n"
    files["files.json"] = dumps({"count_semantics": "saved-snapshot presence only", "files": file_rows}) + "\n"
    index = {"from": source2, "to": source3, "generated_by": "_tools/season3_diff.py",
             "generator_sha256": sha(Path(__file__).read_bytes()),
             "schema": "literal-saved-exports-v1", "totals": totals, "areas": areas,
             "accounting": dict(sorted(accounting.items())), "limits": LIMITS,
             "count_semantics": "added/removed mean present only in one saved snapshot, not game additions/removals",
             "count_definitions": {"property_changes": "Literal change operations in common-path JSON files only; common containers recurse through every property/index.",
                 "path": "Index into asset.change_exports followed by :: and RFC6901 pointer ($ means export root). Each identity is [full export header, occurrence]; array tokens are ordered indexes.",
                 "source_references": "Values over 1024 JSON bytes use $saved_export with side, pinned file hash, exact export identity, RFC6901 pointer, type/count, byte length and content SHA256. Hash serialization is _tools/season3_diff.py dumps(): UTF8 compact JSON with exact decimals and source object key order. Resolve with resolve_reference(wrapper, saved_input_root, manifest). No source values are discarded.",
                 "numeric_literals": "Small numeric values remain inline with explicit integer/decimal type. Additional literal strings are retained where IEEE754 cannot represent the value exactly.",
                 "added_values": "Grouped export operations for S3-only JSON files, counted separately.",
                 "removed_values": "Grouped export operations for S2-only JSON files, counted separately.",
                 "containers": "Added/removed containers and type changes retain one full value, without per-leaf duplication.",
                 "export_order": "Preserved separately per file; order-only changes are not field-change operations.",
                 "assets_modified": "Common-path JSON files whose raw hashes differ, including formatting-only differences."},
             "source_scoped_comparisons": {"source": "docs/evidence/hotfix-cl533731.md",
                 "scope": "Separate existing nine-selected-export comparison; not established by this literal diff or promoted into native rename claims."},
             "manifests": ["manifest-s2.json", "manifest-s3.json"], "file_accounting": "files.json"}
    index["artifacts"] = [{"path": name, "bytes": len(content.encode()), "sha256": sha(content.encode())}
                          for name, content in sorted(files.items())]
    files["index.json"] = dumps(index) + "\n"
    return files, index


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("s2", "s3", "out", "s2-manifest", "s3-manifest"):
        parser.add_argument("--" + name, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    for name in ("write", "check", "stats"):
        mode.add_argument("--" + name, action="store_true")
    args = parser.parse_args(argv)
    try:
        out = Path(args.out)
        for root in (Path(args.s2).resolve(), Path(args.s3).resolve()):
            if out.resolve() == root or root in out.resolve().parents or out.resolve() in root.parents:
                raise ValueError("output must be disjoint from input trees")
        manifests = [load_json(Path(p).read_text(encoding="utf-8"))
                     for p in (args.s2_manifest, args.s3_manifest)]
        files, index = render(args.s2, args.s3, *manifests)
        if args.check or args.write:
            actual = {p.name: p.read_bytes() for p in out.glob("*.json")}
            extra = actual.keys() - files.keys()
            if extra:
                raise ValueError("unexpected output files; refusing to delete: " + ", ".join(sorted(extra)))
            if args.check:
                if actual != {name: text.encode() for name, text in files.items()}:
                    raise ValueError("generated output differs")
            else:
                out.mkdir(parents=True, exist_ok=True)
                for name, text in sorted(files.items()):
                    (out / name).write_bytes(text.encode())
        print(dumps({"totals": index["totals"], "accounting": index["accounting"],
                     "artifacts": len(files)}))
        return 0
    except (ValueError, OSError, KeyError, TypeError, RecursionError) as error:
        print("season3_diff: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
