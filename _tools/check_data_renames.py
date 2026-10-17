"""Proves that a data/ re-export changed only property names, never values.

For every data/ file that differs between a base revision and the working tree, both
versions are split into their '--- export: ... ---' blocks and parsed with duplicate keys
kept. The two trees are walked in parallel: each object must have the same number of
members in the same order, each array the same length, and each leaf the same type and
value. Only member names may differ; every (old name -> new name) pair is tallied. Any
other difference is a failure, and the script exits 1.

With --log <_deobfuscate_log.txt> (written by WdExtract deobfuscate --sdk), each name pair
is also classified against the log's 'sdk correct' / 'sdk name' / 'sdk withdraw' lines.

    python -I _tools/check_data_renames.py [--base 5f5533c] [--log <path>] [--json out.json]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT = re.compile(r"^--- export: (.*) ---\r?$", re.M)
HASHED = re.compile(r"^(_[a-p]{21})")


def blocks(text):
    heads = list(EXPORT.finditer(text))
    out = []
    for i, m in enumerate(heads):
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        out.append((m.group(1), json.loads(body, object_pairs_hook=lambda p: ("obj", p))))
    return out


def walk(a, b, path, ren, bad):
    if isinstance(a, tuple) and isinstance(b, tuple):
        if len(a[1]) != len(b[1]):
            bad.append(f"{path}: {len(a[1])} vs {len(b[1])} members")
            return
        for (ka, va), (kb, vb) in zip(a[1], b[1]):
            if ka != kb:
                ren.append((ka, kb))
            walk(va, vb, f"{path}/{kb}", ren, bad)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            bad.append(f"{path}: array {len(a)} vs {len(b)}")
            return
        for x, y in zip(a, b):
            walk(x, y, path + "[]", ren, bad)
    elif type(a) is not type(b) or a != b:
        bad.append(f"{path}: {a!r} vs {b!r}")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], check=True, capture_output=True).stdout


def read_log(path):
    corr, named, withdrawn = defaultdict(set), set(), set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"sdk (correct|name|withdraw) (\w+)\[(\d+)\] (\S+) -> (\S+)", line)
            if not m:
                continue
            kind, struct, _, a, b = m.groups()
            if kind == "correct":
                corr[(a, b)].add(struct)
            elif kind == "name":
                named.add(b)
            else:
                withdrawn.add((a, b))
    return corr, named, withdrawn


def classify(a, b, log):
    ha, hb = HASHED.match(a), HASHED.match(b)
    if ha and hb:
        return "placeholder -> live token"
    if a.lower() == b.lower():
        return "case only"
    if log is None:
        return "name change"
    corr, named, withdrawn = log
    if ha:
        return "placeholder -> name (sdk restore)" if b in named else "placeholder -> name (donor)"
    if hb:
        return "name -> hashed (sdk withdraw)" if (a, b) in withdrawn else "name -> hashed (not in v2)"
    return "name -> name (sdk correct)" if (a, b) in corr else "name -> name (NOT IN LOG)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="5f5533c")
    ap.add_argument("--log")
    ap.add_argument("--json")
    o = ap.parse_args()
    log = read_log(o.log) if o.log else None
    changed = [p for p in git("diff", "--name-only", "-z", o.base, "--", "data").decode().split("\0")
               if p.endswith(".json")]
    pairs, files_per, failed = Counter(), defaultdict(set), {}
    for rel in changed:
        old = git("show", f"{o.base}:{rel}").decode("utf-8-sig")
        with open(os.path.join(ROOT, rel), encoding="utf-8-sig") as f:
            new = f.read()
        ea, eb = blocks(old), blocks(new)
        ren, bad = [], []
        if [h for h, _ in ea] != [h for h, _ in eb]:
            bad.append("export headers differ")
        else:
            for (h, a), (_, b) in zip(ea, eb):
                walk(a, b, h, ren, bad)
        if bad:
            failed[rel] = bad[:10]
        for p in ren:
            pairs[p] += 1
            files_per[p].add(rel)
    cats = Counter()
    inst = Counter()
    rows = []
    for (a, b), n in pairs.most_common():
        c = classify(a, b, log)
        cats[c] += 1
        inst[c] += n
        rows.append({"old": a, "new": b, "class": c, "count": n, "files": len(files_per[(a, b)]),
                     "structs": sorted(log[0].get((a, b), ())) if log else []})
    print(f"changed files: {len(changed)}; value or shape differences: {len(failed)} files")
    print(f"distinct renames: {len(pairs)}; renamed keys: {sum(pairs.values())}")
    for c in sorted(cats):
        print(f"  {c}: {cats[c]} distinct, {inst[c]} keys")
    if log:
        per_struct = Counter()
        for r in rows:
            for s in r["structs"]:
                per_struct[s] += r["count"]
        print("sdk corrections applied, keys per struct:")
        for s, n in sorted(per_struct.items()):
            print(f"  {s}: {n}")
    if o.json:
        with open(o.json, "w", encoding="utf-8") as f:
            json.dump({"failed": failed, "renames": rows}, f, indent=1)
    for rel, bad in list(failed.items())[:20]:
        print("FAIL", rel, bad[0])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
