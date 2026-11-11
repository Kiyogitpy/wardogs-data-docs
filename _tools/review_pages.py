"""Which published pages may be wrong after a patch? Reads patch-diff.json (from `update_pipeline.py diff`).

    python -I _tools/review_pages.py PATCH_DIFF_JSON [--repo DIR] [--out DIR]     writes review-pages.md / .json (default: next to the diff)

`regen` rewrites the generated blocks (`<!-- name mode --> ... <!-- /name -->`) and assets/data/*.json, but never the
hand-written prose: about 100 `_wiki/` articles type speeds, damage and prices by hand. For every changed or removed
asset this finds the pages that refer to it, the way coverage_census.py does (the asset file name is a whole
[A-Za-z0-9_] token; a bare one-word name such as `Claymore` counts only in backticks or in a path), plus the export
names inside the file (link_sources.py aliases). Each page is classed:
  hand-written   a hit sits outside every generated block, so only a person can refresh it (wiki articles first)
  generated      every hit sits in a generated block or a generated data file: regen refreshes it
  indirect       a _wiki/ article that does not name the asset but cites a reference page that does (Sources links,
                 or a link to a data folder holding the asset): wiki articles usually say "Frag Grenade", not the asset name
Hand-written hits show the changed fields (old -> new) and the page lines that name the asset or contain an old value.
Old/new values are recomputed from the "old"/"new" data directories recorded in the diff when they still exist;
otherwise only the 3 examples kept in patch-diff.json are available. Exit code is 0: this is a report, not a gate.
"""
import argparse
import collections
import importlib.util
import json
import math
import os
import posixpath
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
REPO_URL = "https://github.com/Kiyogitpy/wardogs-data-docs/"
TOKEN = re.compile(r"[A-Za-z0-9_]+")
OPEN = re.compile(r"<!--\s*([A-Za-z_]\w*)(?:\s[^>]*?)?-->")
CLOSE = re.compile(r"<!--\s*/([A-Za-z_]\w*)\s*-->")
EXPORT = re.compile(r"^--- export: [^/\r\n]+/ (.*?) ---\s*$", re.M)
LINK = re.compile(r"\]\(\s*<?([^)\s>]+)")
REPO_LINK = re.compile(r"^" + re.escape(REPO_URL) + r"(blob|tree)/main/(.+)$")
HISTORICAL = re.compile(r"^(season-\d+-changes/|_wiki/patch-notes/)")
GENERATED_DATA = ("assets/data", "_data")
MAX_FIELDS = 40          # fields kept per asset
MAX_LINES = 8            # lines shown per asset per page, per reason
LINE_CHARS = 240
NEAR = 10                # a value is shown for a direct hit only this close to a line naming the asset


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def say(msg=""):
    print(msg, flush=True)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")


# ------------------------------------------------------------------------------------------------ assets
def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def asset_stem(rel):
    return os.path.basename(rel).split(".")[0]


def norm_rel(rel):
    rel = rel.replace("\\", "/").lstrip("/")
    return rel[5:] if rel.startswith("data/") else rel


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def needle_forms(v):
    """Text forms in which a page could quote an old value; [] when the value is too common to search for."""
    if isinstance(v, bool) or v is None:
        return []
    if isinstance(v, str):
        n = num(v)
        if n is None:
            return [v] if 4 <= len(v) <= 40 and "/" not in v and v != "<absent>" else []
        v = n
    if not isinstance(v, (int, float)) or not math.isfinite(v):
        return []
    if v == int(v):
        i = int(abs(v))
        return [str(i), "{:,}".format(i)] if i >= 100 else []
    s = ("%.6f" % abs(v)).rstrip("0")
    return [s] if len(s.replace(".", "")) >= 3 else []


def parse_example(ex):
    m = re.match(r"^(.*?): (.*) -> (.*)$", ex)
    if not m:
        return None
    a, b = m.group(2), m.group(3)
    return {"path": m.group(1), "field": m.group(1).split("/")[-1], "old": num(a) if num(a) is not None else a,
            "new": num(b) if num(b) is not None else b}


def recompute_fields(P, od, nd, rel):
    """Every changed leaf of one asset as {export, path, field, old, new}, using update_pipeline's own diff helpers."""
    po, pn = os.path.join(od, rel), os.path.join(nd, rel)
    if not (rel.endswith(".json") and os.path.isfile(po) and os.path.isfile(pn)):
        return None
    eo = P.split_exports(read_text(po))
    en = P.split_exports(read_text(pn))
    out = []
    for name in sorted(set(eo) | set(en)):
        if name not in eo or name not in en:
            out.append({"export": name, "path": "", "field": "(export %s)" % ("added" if name in en else "removed"), "old": None, "new": None})
            continue
        fo, fn = P.flatten(eo[name]), P.flatten(en[name])
        for p in sorted(set(fo) | set(fn)):
            a, b = fo.get(p, "<absent>"), fn.get(p, "<absent>")
            if not P.num_changed(a, b) or (P.HASHED.search(p) and "<absent>" in (a, b)):
                continue
            out.append({"export": name, "path": p, "field": P.field_key(p), "old": a, "new": b})
    return out


def read_aliases(rel, dirs, stem):
    """Export names inside the asset file (link_sources.py treats them as asset names too)."""
    for d in dirs:
        p = os.path.join(d, rel)
        if d and os.path.isfile(p):
            try:
                text = read_text(p)
            except OSError:
                return []
            # numbered exports (`Foo_0`) are sub-objects whose names repeat across hundreds of assets
            names = {n for n in EXPORT.findall(text) if TOKEN.fullmatch(n) and n != stem and len(n) >= 5 and not n.startswith("Default__") and not re.search(r"_\d+$", n)}
            return sorted(names)
    return []


def load_assets(diff, repo):
    P = None
    try:
        P = _load("update_pipeline")
    except Exception:
        pass
    od, nd = diff.get("old") or "", diff.get("new") or ""
    od, nd = (od if os.path.isdir(od) else ""), (nd if os.path.isdir(nd) else "")
    rdata = os.path.join(repo, "data")
    by = {}
    for c in diff.get("changed", []):
        by[norm_rel(c["file"]).lower()] = {"file": norm_rel(c["file"]), "status": "changed", "area": c.get("area", ""),
                                           "nchanges": c.get("nchanges", 0), "top_fields": c.get("top_fields", []), "examples": c.get("examples", [])}
    for f in diff.get("removed", []):
        by.setdefault(norm_rel(f).lower(), {"file": norm_rel(f), "status": "removed", "area": "", "nchanges": 0, "top_fields": [], "examples": []})
    assets = [by[k] for k in sorted(by)]
    for a in assets:
        stem = asset_stem(a["file"])
        a["stem"] = stem
        a["aliases"] = read_aliases(a["file"], ([nd, od, rdata] if a["status"] == "changed" else [od, rdata]), stem)
        fields, src = None, "examples"
        if a["status"] == "changed" and P and od and nd:
            try:
                fields = recompute_fields(P, od, nd, a["file"])
            except Exception:
                fields = None
        if fields is not None:
            src = "recomputed"
        else:
            fields = [f for f in (parse_example(e) for e in a["examples"]) if f]
        a["fields_total"] = len(fields)
        a["fields"] = fields[:MAX_FIELDS]
        a["value_source"] = src if a["status"] == "changed" else "removed"
        forms = collections.OrderedDict()
        for f in fields:
            for t in needle_forms(f["old"]):
                forms.setdefault(t, f["field"])
        a["needles"] = forms
        del a["examples"]
    return assets, len(diff.get("added", []))


# ------------------------------------------------------------------------------------------------ pages
def generated_lines(lines):
    """Line numbers inside `<!-- name ... -->` ... `<!-- /name -->` pairs (a lone comment with no closer is prose)."""
    closes = collections.defaultdict(list)
    for i, l in enumerate(lines):
        for m in CLOSE.finditer(l):
            closes[m.group(1)].append(i)
    gen, i = set(), 0
    while i < len(lines):
        m = OPEN.search(lines[i])
        j = next((c for c in closes.get(m.group(1), ()) if c >= i), None) if m else None
        if j is None:
            i += 1
            continue
        gen.update(range(i, j + 1))
        i = j + 1
    return gen


def front_title(lines):
    if lines and lines[0].strip() == "---":
        for l in lines[1:30]:
            if l.strip() == "---":
                break
            m = re.match(r"^title:\s*(.+?)\s*$", l)
            if m:
                return m.group(1).strip("\"'")
    return ""


def wiki_keys(lines, title):
    """Lower-case strings that tie a wiki article to a reference-page line: its title and its `Internal name` tags."""
    keys = {title.lower()} if title else set()
    for l in lines:
        if "Internal name" in l:
            keys.update(k.lower() for k in re.findall(r"`([^`]+)`", l) if len(k) >= 6)
    return keys


def page_list(repo):
    out = []

    def walk(d, exts):
        for base, dirs, files in os.walk(os.path.join(repo, d)):
            dirs.sort()
            for f in sorted(files):
                if f.endswith(exts):
                    out.append(os.path.relpath(os.path.join(base, f), repo).replace("\\", "/"))

    try:
        census = _load("coverage_census")
        dirs, skip = [d.replace("\\", "/") for d in census.DOC_DIRS], set(census.ROOT_MD_EXCLUDE)
    except Exception:
        dirs, skip = ["content", "game-features", "pipelines", "plugins", "_wiki", "season-2-changes", "categories", "assets/data", "_data"], set()
    for d in dirs:
        walk(d, (".json", ".yml", ".csv") if d in GENERATED_DATA else (".md",))
    out += [f for f in sorted(os.listdir(repo)) if f.endswith(".md") and f not in skip]
    return sorted(set(out))


def kind_of(page):
    if page.startswith(tuple(d + "/" for d in GENERATED_DATA)):
        return "data"
    return "wiki" if page.startswith("_wiki/") else "reference"


def is_dir_part(text, m):
    """`.../Items/AT_mine/Content/...`: a folder in somebody else's path is not a mention of AT_mine.json."""
    return text[m.start() - 1:m.start()] == "/" and text[m.end():m.end() + 1] == "/"


def bare_ok(text, m):
    a = text[m.start() - 1] if m.start() else ""
    b = text[m.end()] if m.end() < len(text) else ""
    return a in ("`", "/") or b == "`" or text.startswith((".json", ".uasset"), m.end())


class Index:
    """token -> asset numbers. A bare name (no underscore) is a one-word common noun and needs backticks or a path around it."""
    def __init__(self, assets):
        self.tok = collections.defaultdict(set)
        for i, a in enumerate(assets):
            for t in [a["stem"]] + a["aliases"]:
                self.tok[t].add(i)

    def hits(self, text):
        found = []
        for m in TOKEN.finditer(text):
            t = m.group()
            if t in self.tok and not is_dir_part(text, m) and ("_" in t or bare_ok(text, m)):
                found.append((t, self.tok[t]))
        return found


def scan_pages(repo, assets):
    idx = Index(assets)
    pages = {}
    for rel in page_list(repo):
        try:
            with open(os.path.join(repo, rel), encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        kind = kind_of(rel)
        rec = {"page": rel, "kind": kind, "hits": collections.defaultdict(list), "lines": [], "gen": set(), "title": "", "links": []}
        if kind == "data":
            for t, ids in idx.hits(text):
                for i in ids:
                    rec["hits"][i].append(None)
        else:
            lines = text.splitlines()
            rec["lines"], rec["gen"], rec["title"] = lines, generated_lines(lines), front_title(lines)
            for n, l in enumerate(lines):
                for t, ids in idx.hits(l):
                    for i in ids:
                        rec["hits"][i].append(n)
            if kind == "wiki":
                rec["links"] = LINK.findall(text)
        if rec["hits"] or kind == "wiki":
            pages[rel] = rec
    return pages


def resolve_links(page, links):
    """-> (set of repo-relative page paths, set of data folders) a wiki page points at."""
    pages, folders = set(), set()
    for t in links:
        t = unquote(t.split("#")[0])
        m = REPO_LINK.match(t)
        if m:
            path = m.group(2).rstrip("/")
            if m.group(1) == "tree" and path.startswith("data/") and path.count("/") >= 3:
                folders.add(path[5:])
            elif not path.startswith("data/"):
                pages.add(path)
        elif t and "://" not in t and not t.startswith(("{", "/", "mailto:")):
            p = posixpath.normpath(posixpath.join(posixpath.dirname(page), t))
            if not p.startswith(".."):
                pages.add(p)
    return pages, folders


# ------------------------------------------------------------------------------------------------ review
def clip(s):
    s = s.strip()
    return s if len(s) <= LINE_CHARS else s[:LINE_CHARS - 3] + "..."


def line_hits(rec, ids, assets, manual_only=True, near=None):
    """Page lines for the given assets: those naming one, and those carrying an old value of one
    (with near=N, only within N lines of a line that names one: a 600-line reference page holds many unrelated 100s)."""
    out = collections.OrderedDict()
    for i in ids:
        for n in rec["hits"].get(i, ()):
            if n is not None and not (manual_only and n in rec["gen"]):
                out.setdefault(n, "names `%s`" % assets[i]["stem"])
    named = dict(out)
    needles = collections.OrderedDict()
    for i in ids:
        for t, field in assets[i]["needles"].items():
            needles.setdefault(t, (field, assets[i]["stem"]))
    values = {}
    if needles:
        rx = re.compile(r"(?<![\w.,])(%s)(?![\w]|[.,]\d)" % "|".join(re.escape(t) for t in sorted(needles, key=lambda t: (-len(t), t))))
        for n, l in enumerate(rec["lines"]):
            if (manual_only and n in rec["gen"]) or (near is not None and not any(abs(n - k) <= near for k in named)):
                continue
            found = []
            for m in rx.finditer(l):
                if m.group(1) not in [f[0] for f in found]:
                    found.append((m.group(1), needles[m.group(1)][0]))
            if found:
                values[n] = "old value " + ", ".join("%s (%s)" % f for f in found[:3])
    rows = [(n, w, "name") for n, w in named.items()][:MAX_LINES] + [(n, w, "value") for n, w in values.items() if n not in named][:MAX_LINES]
    rows.sort()
    return [{"n": n + 1, "text": clip(rec["lines"][n]), "why": w} for n, w, _ in rows], len(named), len(values)


def review(assets, pages):
    direct = {}      # page -> {asset: [manual line numbers]}
    gen_only = {}    # page -> set(assets)
    for rel, rec in pages.items():
        for i, ns in rec["hits"].items():
            manual = [n for n in ns if n is not None and n not in rec["gen"]]
            if rec["kind"] != "data" and manual:
                direct.setdefault(rel, {})[i] = manual
            elif ns:
                gen_only.setdefault(rel, set()).add(i)
    records = []
    for rel in sorted(direct):
        rec = pages[rel]
        ids = sorted(direct[rel])
        lines = {}
        for i in ids:
            lines[i], _, _ = line_hits(rec, [i], assets, near=NEAR)
        records.append({"page": rel, "kind": rec["kind"], "class": "hand-written", "relation": "direct",
                        "historical": bool(HISTORICAL.match(rel)),
                        "generated_block_assets": sorted(assets[i]["file"] for i in gen_only.get(rel, ())),
                        "assets": [{"file": assets[i]["file"], "status": assets[i]["status"], "lines": lines[i]} for i in ids]})
    for rel in sorted(set(gen_only) - set(direct)):
        rec = pages[rel]
        records.append({"page": rel, "kind": rec["kind"], "class": "generated", "relation": "direct", "historical": bool(HISTORICAL.match(rel)),
                        "assets": [{"file": assets[i]["file"], "status": assets[i]["status"], "lines": []} for i in sorted(gen_only[rel])]})
    # indirect: a wiki article that cites a reference page (or data folder) that names a changed asset
    # change logs are cited by nearly every article and describe an older patch, so they do not make an article stale
    named_on = {rel: set(r["hits"]) for rel, r in pages.items() if r["kind"] != "wiki" and r["hits"] and not HISTORICAL.match(rel)}
    for rel in sorted(p for p, r in pages.items() if r["kind"] == "wiki"):
        rec = pages[rel]
        if HISTORICAL.match(rel):
            continue
        own = set(direct.get(rel, ())) | set(gen_only.get(rel, ()))
        refs, folders = resolve_links(rel, rec["links"])
        via = []        # (cited page or folder, asset numbers)
        for ref in sorted(refs & set(named_on)):
            ids = sorted(named_on[ref] - own)
            if ids:
                via.append((ref, ids))
        for fol in sorted(folders):
            ids = sorted(i for i, a in enumerate(assets) if a["file"].lower().startswith(fol.lower() + "/") and i not in own)
            if ids:
                via.append(("data/" + fol + "/ (folder)", ids))
        if not via:
            continue
        # a shared reference page names many assets; the ones on a line that holds this article's title or internal name are the likely ones
        keys = wiki_keys(rec["lines"], rec["title"])
        strong = set()
        for cites, ids in via:
            ref = pages.get(cites)
            if keys and ref and ref["lines"]:
                strong.update(i for i in ids if any(n is not None and any(k in ref["lines"][n].lower() for k in keys) for n in ref["hits"].get(i, ())))
        keep = strong or {i for _, ids in via for i in ids}
        via = [{"cites": c, "assets": [assets[i]["file"] for i in ids if i in keep]} for c, ids in via if keep & set(ids)]
        ids = sorted(keep)
        vl, _, nvalue = line_hits(rec, ids, assets)
        lines = [l for l in vl if l["why"].startswith("old value")]
        strong = bool(strong)
        records.append({"page": rel, "kind": "wiki", "class": "hand-written", "relation": "indirect", "historical": False,
                        "title": rec["title"], "title_match": strong, "value_lines": nvalue, "via": via, "lines": lines,
                        "assets": [{"file": assets[i]["file"], "status": assets[i]["status"]} for i in ids]})
    return records


def order(rec):
    cls = 0 if rec["class"] == "hand-written" else 1
    rel = 0 if rec["relation"] == "direct" else 1
    tier = {"wiki": 0, "reference": 1, "data": 2}[rec["kind"]]
    ind = (0 if rec.get("title_match") else 1, 0 if rec.get("value_lines") else 1) if rec["relation"] == "indirect" else (0, 0)
    return (cls, rec["historical"], rel, ind, tier, rec["page"])


# ------------------------------------------------------------------------------------------------ output
def fv(v):
    return "<absent>" if v == "<absent>" else ("%g" % v if isinstance(v, float) else str(v))[:60]


def render(diff_path, diff, assets, n_added, records):
    by_file = {a["file"]: a for a in assets}
    hand = [r for r in records if r["class"] == "hand-written"]
    cur = [r for r in hand if not r["historical"]]
    gen = [r for r in records if r["class"] == "generated"]
    referenced = {a["file"] for r in records for a in r["assets"]}
    L = ["# Pages to review after the patch: %s -> %s" % (os.path.basename(os.path.dirname(diff.get("old", "")) or "old"), os.path.basename(os.path.dirname(diff.get("new", "")) or "new")), "",
         "Generated by `_tools/review_pages.py` from `%s`. `regen` refreshes generated blocks and `assets/data`; **hand-written prose is only ever fixed by a person**, so it is listed first." % os.path.basename(diff_path), "",
         "| | Count |", "|---|---:|",
         "| Changed assets | %d |" % sum(1 for a in assets if a["status"] == "changed"),
         "| Removed assets | %d |" % sum(1 for a in assets if a["status"] == "removed"),
         "| Added assets (not scanned: no page can describe them yet) | %d |" % n_added,
         "| Assets referred to by at least one page | %d |" % len(referenced),
         "| Assets no page refers to | %d |" % (len(assets) - len(referenced)),
         "| **Hand-written pages naming a changed asset** (wiki: %d, other: %d) | %d |" % (sum(r["kind"] == "wiki" for r in cur if r["relation"] == "direct"), sum(r["kind"] != "wiki" for r in cur if r["relation"] == "direct"), sum(r["relation"] == "direct" for r in cur)),
         "| **Wiki articles citing a reference page that names one** (indirect; likely: %d, weaker: %d) | %d |" % (sum(r["title_match"] for r in cur if r["relation"] == "indirect"), sum(not r["title_match"] for r in cur if r["relation"] == "indirect"), sum(r["relation"] == "indirect" for r in cur)),
         "| Historical change-log pages naming one (usually leave alone) | %d |" % sum(r["historical"] for r in hand),
         "| Generated pages and data files (regen refreshes) | %d |" % len(gen), ""]
    if not assets:
        L += ["No changed or removed assets in the diff.", ""]

    def fields_block(a):
        out = []
        if a["status"] == "removed":
            return ["  - REMOVED from the game data: the page text may describe something that no longer exists"]
        for f in a["fields"][:12]:
            out.append("  - `%s`: %s -> %s" % (f["field"] if not f["path"] else f["path"].lstrip("/")[-90:], fv(f["old"]), fv(f["new"])))
        if a["fields_total"] > 12:
            out.append("  - ... %d more changed fields (see review-pages.json)" % (a["fields_total"] - 12))
        if a["value_source"] == "examples":
            out.append("  - (old data directory gone: only the examples kept in patch-diff.json are shown)")
        return out

    def names_list(names, n=6):
        return ", ".join("`%s`" % os.path.basename(x) for x in names[:n]) + (" and %d more" % (len(names) - n) if len(names) > n else "")

    def lines_block(lines):
        if not lines:
            return []
        return ["  ~~~~"] + ["  L%d (%s): %s" % (l["n"], l["why"], l["text"]) for l in lines] + ["  ~~~~"]

    L += ["## 1. Hand-written pages that name a changed or removed asset", "",
          "Check each: the page may quote a value that has since changed. Wiki articles first.", ""]
    direct = [r for r in sorted(cur, key=order) if r["relation"] == "direct"]
    if not direct:
        L += ["None.", ""]
    for r in direct:
        L += ["### `%s` (%s)" % (r["page"], "wiki article" if r["kind"] == "wiki" else "reference page"), ""]
        for a in r["assets"]:
            A = by_file[a["file"]]
            L += ["- `%s` (%s)" % (a["file"], a["status"])] + fields_block(A) + lines_block(a["lines"])
        if r["generated_block_assets"]:
            L.append("- also named inside generated blocks (regen refreshes): %d asset(s)" % len(r["generated_block_assets"]))
        L.append("")

    L += ["## 2. Wiki articles that cite a reference page naming a changed asset (indirect)", "",
          "These articles do not name the asset, but a page they cite does; the article may describe the item by its player name. "
          "**Likely**: the cited page names the asset on a line that holds the article title or its `Internal name` tag. "
          "**Weaker**: the cited page only names the asset somewhere (broad catalogs such as the item shop cite many articles).", ""]
    ind = [r for r in sorted(cur, key=order) if r["relation"] == "indirect"]
    if not ind:
        L += ["None.", ""]
    for r in (r for r in ind if r["title_match"]):
        L += ["### `%s`%s" % (r["page"], " (likely; quotes an old value)" if r["lines"] else " (likely)"), ""]
        for v in r["via"]:
            L.append("- cites `%s`, which names: %s" % (v["cites"], names_list(v["assets"])))
        L += lines_block(r["lines"]) + [""]
    weak = [r for r in ind if not r["title_match"]]
    if weak:
        L += ["### Weaker matches (%d)" % len(weak), ""]
        for r in weak:
            L.append("- `%s`%s: cites %s" % (r["page"], " (quotes an old value)" if r["lines"] else "", "; ".join("`%s` (%s)" % (v["cites"], names_list(v["assets"], 3)) for v in r["via"][:3]) + (" and %d more" % (len(r["via"]) - 3) if len(r["via"]) > 3 else "")))
        L.append("")

    hist = [r for r in sorted(hand, key=order) if r["historical"]]
    if hist:
        L += ["## 3. Historical change-log pages (written for an earlier patch; normally left alone)", ""]
        L += ["- `%s`: %d asset(s)" % (r["page"], len(r["assets"])) for r in hist] + [""]

    L += ["## 4. Generated pages and data files (regen refreshes these; check the diff after regen)", ""]
    L += ["- `%s`: %d asset(s)" % (r["page"], len(r["assets"])) for r in sorted(gen, key=order)[:80]] or ["None."]
    if len(gen) > 80:
        L.append("- ... %d more (see review-pages.json)" % (len(gen) - 80))
    L.append("")

    pg = collections.defaultdict(list)
    for r in sorted(records, key=order):
        for a in r["assets"]:
            pg[a["file"]].append(r["page"] + (" (indirect)" if r["relation"] == "indirect" else ""))
    L += ["## 5. By asset", ""]
    for a in assets:
        if a["file"] in pg:
            L.append("- `%s` (%s): %s" % (a["file"], a["status"], ", ".join("`%s`" % p for p in pg[a["file"]][:12]) + (" and %d more" % (len(pg[a["file"]]) - 12) if len(pg[a["file"]]) > 12 else "")))
    none = [a["file"] for a in assets if a["file"] not in pg]
    if none:
        L += ["", "No page refers to %d asset(s)%s." % (len(none), ": " + ", ".join("`%s`" % os.path.basename(x) for x in none[:10]) + (", ..." if len(none) > 10 else ""))]
    L.append("")
    return L


def run(diff_path, repo=REPO, out=None):
    with open(diff_path, encoding="utf-8") as f:
        diff = json.load(f)
    assets, n_added = load_assets(diff, repo)
    records = sorted(review(assets, scan_pages(repo, assets)), key=order)
    out = out or os.path.dirname(os.path.abspath(diff_path))
    referenced = {a["file"] for r in records for a in r["assets"]}
    cur = [r for r in records if r["class"] == "hand-written" and not r["historical"]]
    summary = {"changed": sum(a["status"] == "changed" for a in assets), "removed": sum(a["status"] == "removed" for a in assets), "added_not_scanned": n_added,
               "assets_with_pages": len(referenced), "assets_without_pages": len(assets) - len(referenced),
               "hand_written_direct": sum(r["relation"] == "direct" for r in cur), "hand_written_direct_wiki": sum(r["relation"] == "direct" and r["kind"] == "wiki" for r in cur),
               "hand_written_indirect_wiki": sum(r["relation"] == "indirect" for r in cur),
               "hand_written_indirect_wiki_likely": sum(r["relation"] == "indirect" and r["title_match"] for r in cur),
               "historical": sum(r["historical"] for r in records if r["class"] == "hand-written"), "generated": sum(r["class"] == "generated" for r in records)}
    by_asset = collections.defaultdict(list)
    for r in records:
        for a in r["assets"]:
            by_asset[a["file"]].append({"page": r["page"], "class": r["class"], "relation": r["relation"]})
    write_json(os.path.join(out, "review-pages.json"), {
        "source": os.path.basename(diff_path), "summary": summary,
        "assets": [{k: a[k] for k in ("file", "status", "area", "stem", "aliases", "nchanges", "fields_total", "fields", "value_source")} | {"pages": by_asset.get(a["file"], [])} for a in assets],
        "pages": records})
    with open(os.path.join(out, "review-pages.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(render(diff_path, diff, assets, n_added, records)) + "\n")
    return summary, out


def main(argv=None):
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("diff", help="patch-diff.json written by update_pipeline.py diff")
    ap.add_argument("--repo", default=REPO, help="repository whose pages are scanned (default: this one)")
    ap.add_argument("--out", help="output directory (default: next to the diff)")
    args = ap.parse_args(argv)
    s, out = run(args.diff, args.repo, args.out)
    say("review-pages: %d changed, %d removed asset(s); hand-written pages to check: %d direct (%d wiki) + %d wiki indirect (%d likely); generated: %d; wrote %s"
        % (s["changed"], s["removed"], s["hand_written_direct"], s["hand_written_direct_wiki"], s["hand_written_indirect_wiki"], s["hand_written_indirect_wiki_likely"], s["generated"], os.path.join(out, "review-pages.md")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
