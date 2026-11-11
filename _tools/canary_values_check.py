"""Canary values: a curated list of known data values, checked against an export.

    python -I _tools/canary_values_check.py --check [--data DIR]    exit 0 clean, 1 changed values only, 2 missing / wrong type
    python -I _tools/canary_values_check.py --accept [--data DIR]   rewrite canary_values.json with the current values

Why: a stale usmap (or a changed pak format) can misread values without any CUE4Parse warning: properties shift, tables
vanish. Each canary is a value the site already publishes, read from the export by file, export name and path:

    missing     the file, export or path is gone                -> the export was probably misread
    wrong type  the path holds another kind of value             -> the export was probably misread
    changed     same kind of value, different number or text     -> "changed, review": usually a real balance patch

`--accept` takes over changed values after you reviewed them. It refuses (writes nothing) while any canary is missing or
has the wrong type: fix the canary by hand once you know the game really moved that value. `update_pipeline.py extract`
runs the same check against the fresh export (missing / wrong type fail the extract with the stale-usmap exit code,
changed values only warn) and `regen` runs `--check` as a registered checker.

A canary is {id, area, file, export, path, expected}: `file` is relative to data/, `export` the "Name" of the export
inside it, `path` the "/"-separated keys down from that export (a list index is its number).
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANARIES = os.path.join(HERE, "canary_values.json")
HEADER = re.compile(r"^--- export: .*? ---\r?\n", re.M)
RC_OK, RC_CHANGED, RC_BAD = 0, 1, 2


def kind(v):
    """JSON kind of a value; int and float are both 'number', a bool is not a number."""
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, (int, float)):
        return "number"
    return {str: "string", list: "list", dict: "object", type(None): "null"}[type(v)]


def same(a, b):
    if kind(a) == "number" and kind(b) == "number":
        return abs(a - b) <= 1e-6 * max(1.0, abs(a), abs(b))
    return a == b


def read_exports(path):
    """Export objects of a CueDump file (`--- export: ... ---` blocks) or of a plain JSON file. Unreadable block -> None."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    heads = list(HEADER.finditer(text))
    if not heads:
        return [json.loads(text)]
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        try:
            out.append(json.loads(text[m.end():end]))
        except ValueError:
            out.append(None)
    return out


def walk(node, path):
    """(found, value) for a '/'-separated path below `node`."""
    for key in path.split("/"):
        if isinstance(node, list) and key.isdigit() and int(key) < len(node):
            node = node[int(key)]
        elif isinstance(node, dict) and key in node:
            node = node[key]
        else:
            return False, key
    return True, node


def evaluate(data_dir, canaries):
    """One result per canary: {id, area, status ok|changed|missing|type, expected, actual, detail}."""
    cache, out = {}, []
    for c in canaries:
        r = {"id": c["id"], "area": c["area"], "status": "ok", "expected": c["expected"], "actual": None, "detail": ""}
        out.append(r)
        p = os.path.join(data_dir, c["file"])
        if c["file"] not in cache:
            try:
                cache[c["file"]] = read_exports(p) if os.path.isfile(p) else None
            except (ValueError, OSError):
                cache[c["file"]] = False
        exports = cache[c["file"]]
        if exports is None or exports is False:
            r["status"], r["detail"] = "missing", "file %s %s" % (c["file"], "not in the export" if exports is None else "unreadable")
            continue
        exp = next((e for e in exports if isinstance(e, dict) and e.get("Name") == c["export"]), None)
        if exp is None:
            r["status"], r["detail"] = "missing", "no export named %s" % c["export"]
            continue
        found, v = walk(exp, c["path"])
        if not found:
            r["status"], r["detail"] = "missing", "path stops at %r" % v
            continue
        r["actual"] = v
        if kind(v) != kind(c["expected"]):
            r["status"], r["detail"] = "type", "%s, expected %s" % (kind(v), kind(c["expected"]))
        elif not same(v, c["expected"]):
            r["status"] = "changed"
    return out


def load_canaries(path=CANARIES):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    for c in doc["canaries"]:
        if kind(c["expected"]) in ("list", "object"):
            raise SystemExit("canary %s: expected must be a number, string, bool or null" % c["id"])
    return doc


def summarize(results):
    """{'missing': [...], 'wrong_type': [...], 'changed': [...]} of canary ids (+ old/new for changed)."""
    return {"checked": len(results),
            "missing": [r["id"] for r in results if r["status"] == "missing"],
            "wrong_type": [r["id"] for r in results if r["status"] == "type"],
            "changed": [{"id": r["id"], "old": r["expected"], "new": r["actual"]} for r in results if r["status"] == "changed"]}


def exit_code(results):
    st = {r["status"] for r in results}
    return RC_BAD if st & {"missing", "type"} else (RC_CHANGED if "changed" in st else RC_OK)


def report(results):
    for r in results:
        if r["status"] == "missing":
            print("MISSING       %-34s [%s] %s" % (r["id"], r["area"], r["detail"]))
        elif r["status"] == "type":
            print("WRONG TYPE    %-34s [%s] %s (value %r)" % (r["id"], r["area"], r["detail"], r["actual"]))
        elif r["status"] == "changed":
            print("changed, review %-32s [%s] %r -> %r" % (r["id"], r["area"], r["expected"], r["actual"]))
    s = summarize(results)
    print("canaries: %d checked, %d missing, %d wrong type, %d changed" % (s["checked"], len(s["missing"]), len(s["wrong_type"]), len(s["changed"])))
    if s["missing"] or s["wrong_type"]:
        print("Missing or mistyped canaries mean the export was probably misread (stale usmap, shifted properties).")
    elif s["changed"]:
        print("Changed values are usually a balance patch: review them, then run --accept.")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--accept", action="store_true", help="rewrite the expected values with the current ones (after review)")
    ap.add_argument("--data", default=os.path.join(ROOT, "data"))
    ap.add_argument("--canaries", default=CANARIES)
    a = ap.parse_args(argv)
    doc = load_canaries(a.canaries)
    results = evaluate(a.data, doc["canaries"])
    report(results)
    rc = exit_code(results)
    if a.check:
        return rc
    if rc == RC_BAD:
        print("not accepted: fix the missing / mistyped canaries by hand first")
        return rc
    for c, r in zip(doc["canaries"], results):
        c["expected"] = r["actual"] if r["status"] == "changed" else c["expected"]
    with open(a.canaries, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1)
        f.write("\n")
    print("accepted %d changed value(s) into %s" % (len(summarize(results)["changed"]), a.canaries))
    return RC_OK


if __name__ == "__main__":
    sys.exit(main())
