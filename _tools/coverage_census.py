"""Coverage census v4: asset families under data/ vs. names mentioned in published docs.

    python -I _tools/coverage_census.py [--json PATH] [--top N] [--list FAMILY]

Family = "<area>|<prefix>", area = the first folders under data/ (Wardogs/Content/<X>, Engine/<X>, Plugins/<X>,
Config), prefix = leading token of the file name up to the first "_" when it is a short upper-case type prefix
(DT_, DA_, GE_, BP_, B_, W_, ST_, CT_ ...), else "(none)". An asset counts as mentioned when its file name
(no extension) is a whole [A-Za-z0-9_] token in a published page: content/, game-features/, pipelines/, plugins/,
_wiki/, season-2-changes/, categories/, root *.md, plus generated JSON under assets/data/ (and _data/).
Audio and UI-widget paths are reported separately and excluded from the headline "data" figure.
"""
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOC_DIRS = ["content", "game-features", "pipelines", "plugins", "_wiki", "season-2-changes", "categories",
            os.path.join("assets", "data"), "_data"]
ROOT_MD_EXCLUDE = {"README.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE", "Note_Template.md"}
TOKEN = re.compile(r"[A-Za-z0-9_]+")
SKIP_RE = re.compile(r"(^|/)(Audio|UI|Sounds?|Wwise|Music|Vox)(/|$)|Widgets?/", re.I)
PREFIX = re.compile(r"^([A-Za-z]{1,6})_")


CATALOGS = ("Wardogs_DataTables_v1.md", "Wardogs_Audio_v2.md", "season-diff")


def published_tokens():
    """Return (all_tokens, deep_tokens, page_count). deep = tokens in a Markdown page that is not a catalog
    page and not generated JSON; page_count[token] = distinct pages."""
    toks = set()
    deep = set()
    pages = defaultdict(int)

    def add(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            t = set(TOKEN.findall(fh.read()))
        toks.update(t)
        for x in t:
            pages[x] += 1
        if p.endswith(".md") and not any(c in p.replace("\\", "/") for c in CATALOGS):
            deep.update(t)

    for d in DOC_DIRS:
        for base, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if f.endswith((".md", ".json", ".yml", ".html", ".csv")):
                    add(os.path.join(base, f))
    for f in os.listdir(ROOT):
        if f.endswith(".md") and f not in ROOT_MD_EXCLUDE:
            add(os.path.join(ROOT, f))
    return toks, deep, pages


def doc_text():
    """Concatenated text of non-catalog Markdown pages plus generated JSON (for row-name substring tests)."""
    chunks = []
    for d in DOC_DIRS:
        for base, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                p = os.path.join(base, f)
                if f.endswith((".md", ".json")) and not any(c in p.replace("\\", "/") for c in CATALOGS):
                    with open(p, encoding="utf-8", errors="replace") as fh:
                        chunks.append(fh.read())
    for f in os.listdir(ROOT):
        if f.endswith(".md") and f not in ROOT_MD_EXCLUDE:
            with open(os.path.join(ROOT, f), encoding="utf-8", errors="replace") as fh:
                chunks.append(fh.read())
    return "\n".join(chunks)


def row_census(text):
    """Row-level: for each DataTable export, rows whose full row name appears in docs text. Row names shorter
    than 4 characters or purely numeric are counted as generic and not tested (reported as 'generic')."""
    out = {}
    for base, _, files in os.walk(DATA):
        for f in files:
            if not f.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/")
            if SKIP_RE.search(rel):
                continue
            with open(os.path.join(base, f), encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
            if '"Rows"' not in raw:
                continue
            for part in re.split(r"^--- export:.*---\n", raw, flags=re.M):
                if '"Rows"' not in part:
                    continue
                try:
                    j = json.loads(part)
                except ValueError:
                    continue
                rows = j.get("Rows") if isinstance(j, dict) else None
                if not isinstance(rows, dict):
                    continue
                tested = [r for r in rows if len(r) >= 4 and not r.isdigit()]
                hit = [r for r in tested if r in text]
                out[rel + "#" + j.get("Name", "")] = {"rows": len(rows), "generic": len(rows) - len(tested),
                                                   "tested": len(tested), "rows_mentioned": len(hit),
                                                   "missing_sample": [r for r in tested if r not in text][:8]}
    return out


def prop_census(toks):
    """Field level: per export Type, distinct top-level Properties keys and how many appear as a token in docs.
    Hashed names (_aaa...) are counted separately as hashed."""
    types = {}
    for base, _, files in os.walk(DATA):
        for f in files:
            if not f.endswith(".json"):
                continue
            rel = os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/")
            if SKIP_RE.search(rel):
                continue
            with open(os.path.join(base, f), encoding="utf-8", errors="replace") as fh:
                raw = fh.read()
            for part in re.split(r"^--- export:.*---\n", raw, flags=re.M):
                if not part.strip().startswith("{"):
                    continue
                try:
                    j = json.loads(part)
                except ValueError:
                    continue
                if not isinstance(j, dict):
                    continue
                props = j.get("Properties")
                if not isinstance(props, dict):
                    continue
                t = types.setdefault(j.get("Type", "?"), {"assets": 0, "props": {}, "example": rel})
                t["assets"] += 1
                for k in props:
                    t["props"][k] = t["props"].get(k, 0) + 1
    out = {}
    for ty, t in types.items():
        names = list(t["props"])
        hashed = [k for k in names if k.startswith("_aaa")]
        real = [k for k in names if not k.startswith("_aaa")]
        miss = [k for k in real if k not in toks]
        out[ty] = {"assets": t["assets"], "props": len(real), "hashed": len(hashed), "props_mentioned": len(real) - len(miss),
                   "missing": sorted(miss, key=lambda k: -t["props"][k])[:12], "example": t["example"]}
    return out


def area_of(rel):
    p = rel.split("/")[1:-1]
    if p[:2] == ["Wardogs", "Content"]:
        return "/".join(p[2:4]) if len(p) > 3 and p[2] in ("Items", "Characters", "GameMechanics", "Vehicles") else "/".join(p[2:3]) or "Content"
    if p[:1] == ["Wardogs"]:
        return "/".join(p[:3])
    if p[:2] == ["Engine", "Plugins"]:
        return "/".join(p[:3])
    return "/".join(p[:2]) or "(root)"


def prefix_of(name):
    m = PREFIX.match(name)
    return (m.group(1).upper() + "_") if m else "(none)"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    top = int(a[a.index("--top") + 1]) if "--top" in a else 25
    toks, deep, pages = published_tokens()
    fam = defaultdict(lambda: {"total": 0, "mentioned": 0, "deep": 0, "scope": "data", "unmentioned": []})
    for base, _, files in os.walk(DATA):
        for f in files:
            rel = os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/")
            name = os.path.splitext(f)[0]
            if name.endswith(".uasset") or name.endswith(".umap"):
                name = os.path.splitext(name)[0]
            scope = "audio-ui" if SKIP_RE.search(rel) else ("engine" if rel.startswith("data/Engine/") else "data")
            key = "%s|%s|%s" % (scope, area_of(rel), prefix_of(name))
            e = fam[key]
            e["scope"] = scope
            e["total"] += 1
            if name in deep:
                e["deep"] += 1
            if name in toks:
                e["mentioned"] += 1
            else:
                e["unmentioned"].append(rel)
            if name not in deep:
                e.setdefault("catalog_only", []).append(rel)
    tot = defaultdict(lambda: [0, 0, 0])
    for k, e in fam.items():
        tot[e["scope"]][0] += e["total"]
        tot[e["scope"]][1] += e["mentioned"]
        tot[e["scope"]][2] += e["deep"]
    allt = sum(v[0] for v in tot.values())
    allm = sum(v[1] for v in tot.values())
    print("families: %d  assets: %d  mentioned: %d (%.1f%%)" % (len(fam), allt, allm, 100 * allm / max(allt, 1)))
    for s, (t, m, d) in sorted(tot.items()):
        print("  %-9s %5d assets, %5d mentioned (%.1f%%), %5d in a non-catalog Markdown page (%.1f%%)"
              % (s, t, m, 100 * m / max(t, 1), d, 100 * d / max(t, 1)))
    rows = [(k, e) for k, e in fam.items() if e["scope"] == "data"]
    rows.sort(key=lambda kv: kv[1]["deep"] - kv[1]["total"])
    print("\ntop %d families by unmentioned count (scope=data):" % top)
    for k, e in rows[:top]:
        print("  %5d unmentioned of %5d  %s" % (e["total"] - e["mentioned"], e["total"], k))
    if "--list" in a:
        want = a[a.index("--list") + 1]
        for k, e in fam.items():
            if want in k:
                print("\n".join(e["unmentioned"]))
    rc = row_census(doc_text())
    rt = sum(v["tested"] for v in rc.values())
    rm = sum(v["rows_mentioned"] for v in rc.values())
    print("\nrow level: %d DataTables, %d rows tested (%d generic skipped), %d row names mentioned (%.1f%%)"
          % (len(rc), rt, sum(v["generic"] for v in rc.values()), rm, 100 * rm / max(rt, 1)))
    worst = sorted(rc.items(), key=lambda kv: kv[1]["rows_mentioned"] - kv[1]["tested"])[:top]
    print("tables with most unmentioned rows:")
    for k, v in worst:
        print("  %5d of %5d  %s" % (v["tested"] - v["rows_mentioned"], v["tested"], k))
    pc = prop_census(toks)
    print("\nfield level: %d export types, %d distinct property names, %d mentioned"
          % (len(pc), sum(v["props"] for v in pc.values()), sum(v["props_mentioned"] for v in pc.values())))
    print("types with most unmentioned property names:")
    for ty, v in sorted(pc.items(), key=lambda kv: kv[1]["props_mentioned"] - kv[1]["props"])[:top]:
        print("  %4d of %4d props (%d assets, %d hashed)  %s  e.g. %s" % (v["props"] - v["props_mentioned"], v["props"], v["assets"], v["hashed"], ty, ", ".join(v["missing"][:4])))
    if "--json" in a:
        out = a[a.index("--json") + 1]
        with open(out, "w", encoding="utf-8") as fh:
            json.dump({"families": {k: dict(e) for k, e in sorted(fam.items())}, "datatables": rc, "types": pc}, fh, indent=1)


if __name__ == "__main__":
    main()
