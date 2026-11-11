"""Hashed property names hard-coded in _tools/*.py that a data export does not contain.

    python -I _tools/hashed_names_check.py --data DIR [--json OUT] [--tools DIR]

A hashed name is an underscore plus 21 letters a-p. Some exports add a suffix such as _$...$_$22$; the
22-character stem is what is matched, in both the scripts and the JSON. String literals are read with
ast (comments and code are ignored). Every *.json under DIR is read once with one regex pass, and the
stems found there are compared with each distinct script name. Scripts named test_*.py and this file
are skipped. Prints `script:line name` for each missing name, then a summary line. Exit 0 when none
are missing, 1 otherwise.
"""
import argparse
import ast
import glob
import json
import os
import re
import sys

STEM = re.compile(r"(?<![A-Za-z0-9_])_[a-p]{21}(?![a-p])")
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = os.path.basename(__file__)


def say(msg=""):
    print(msg, flush=True)


def write_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")


def hardcoded(tools):
    """(script, line, name) for every stem in a string literal; a name keeps its first occurrence."""
    first = {}
    for path in sorted(glob.glob(os.path.join(tools, "*.py"))):
        script = os.path.basename(path)
        if script == SELF or script.startswith("test_"):
            continue
        with open(path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                for m in STEM.finditer(node.value):
                    line = node.lineno + node.value.count("\n", 0, m.start())
                    first.setdefault(m.group(0), (script, line))
    return first


def data_names(data):
    found = set()
    for root, _, files in os.walk(data):
        for fn in files:
            if fn.endswith(".json"):
                with open(os.path.join(root, fn), encoding="utf-8", errors="replace") as f:
                    found.update(STEM.findall(f.read()))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", required=True, help="folder searched recursively for *.json")
    ap.add_argument("--json", metavar="OUT", help="also write {hardcoded, missing} as JSON")
    ap.add_argument("--tools", default=HERE, help="folder of scripts to scan (default: this folder)")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.data):
        ap.error(f"--data is not a folder: {a.data}")
    names = hardcoded(a.tools)
    found = data_names(a.data)
    missing = [{"script": s, "line": l, "name": n}
               for n, (s, l) in sorted(names.items(), key=lambda kv: kv[1]) if n not in found]
    for m in missing:
        say(f"{m['script']}:{m['line']} {m['name']}")
    say(f"hashed names: {len(names)} hard-coded, {len(missing)} missing from {a.data}")
    if a.json:
        write_json(a.json, {"hardcoded": len(names), "missing": missing})
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
