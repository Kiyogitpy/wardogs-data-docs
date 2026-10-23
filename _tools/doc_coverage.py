"""Documentation-coverage census: which asset names under data/ appear in a published page.

    python _tools/doc_coverage.py [--depth N] [--top K] [--list GROUP_PREFIX]

An asset counts as mentioned when its file name without extension appears as a whole identifier
([A-Za-z0-9_]+ token) in any published page (every .md outside the paths excluded in _config.yml, so
docs/, sdk/, tools/, mappings/ and _tools/ do not count). Audio and UI-widget assets are reported
separately and left out of the headline "data" figure (project scope: all data tables, no audio, no UI widgets).
Groups are directories under data/ truncated to --depth components below data/Wardogs|Engine (default 5).
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
EXCLUDE = {"data", "docs", "sdk", "tools", "_tools", "mappings", "graphify-out", "worker", ".git", "_includes",
           "_sass", "node_modules"}
EXCLUDE_FILES = {"README.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE", "Note_Template.md", "aes.md"}
TOKEN = re.compile(r"[A-Za-z0-9_]+")
SKIP_RE = re.compile(r"(^|/)(Audio|UI|Sounds?|Wwise|Music|Vox)(/|$)|/Audio/|/UI/|Widgets?/", re.I)


def published_tokens():
    toks = set()
    for base, dirs, files in os.walk(ROOT):
        rel = os.path.relpath(base, ROOT).replace("\\", "/")
        if rel == ".":
            dirs[:] = [d for d in dirs if d not in EXCLUDE and not d.startswith(".")]
        for f in files:
            if f.endswith(".md") and (rel != "." or f not in EXCLUDE_FILES):
                with open(os.path.join(base, f), encoding="utf-8", errors="replace") as fh:
                    toks.update(TOKEN.findall(fh.read()))
    return toks


def assets():
    for base, _, files in os.walk(DATA):
        for f in files:
            full = os.path.join(base, f)
            yield os.path.relpath(full, ROOT).replace("\\", "/"), os.path.splitext(f)[0]


def group_of(path, depth):
    parts = path.split("/")[1:-1]  # drop data/ and file
    return "/".join(parts[:depth]) or "(root)"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    depth = int(a[a.index("--depth") + 1]) if "--depth" in a else 5
    top = int(a[a.index("--top") + 1]) if "--top" in a else 15
    toks = published_tokens()
    tot = hit = 0
    dtot = dhit = 0
    per = defaultdict(lambda: [0, 0])
    grp = defaultdict(lambda: [0, 0])
    unc = defaultdict(list)
    for path, name in assets():
        skipped = bool(SKIP_RE.search(path))
        m = name in toks
        tot += 1
        hit += m
        top1 = "/".join(path.split("/")[1:4])
        per[top1][0] += 1
        per[top1][1] += m
        if not skipped:
            dtot += 1
            dhit += m
            g = group_of(path, depth)
            grp[g][0] += 1
            grp[g][1] += m
            if not m:
                unc[g].append(path)
    print(f"all assets : {hit}/{tot} mentioned ({100*hit/tot:.1f}%)")
    print(f"data only (audio/UI-widget paths excluded): {dhit}/{dtot} mentioned ({100*dhit/dtot:.1f}%)")
    print("\nper folder (all assets, three levels under data/):")
    for k, (t, h) in sorted(per.items()):
        print(f"  {k:60s} {h:5d}/{t:5d} {100*h/t:5.1f}%")
    print(f"\ntop {top} uncovered groups (data only, depth {depth}):")
    for g, (t, h) in sorted(grp.items(), key=lambda kv: kv[1][1] - kv[1][0])[:top]:
        print(f"  {t-h:5d} uncovered of {t:5d}  {g}")
    if "--list" in a:
        p = a[a.index("--list") + 1]
        for g, v in unc.items():
            if g.startswith(p):
                print("\n".join(v))


if __name__ == "__main__":
    main()
