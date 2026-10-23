"""Byte-level comparison of doc-cited functions between the analysis and reference images.

Companion to _tools/ida_claim_exposure.py, which it imports (page classes, citation
collection, the per-address classifier). For every cited address that has a corpus function
row inside .text, the function's own bytes are compared between the analysis image and the
reference image. For the functions classified 'stub' or 'differs', the immediately preceding
corpus function (the row with the largest rva below the cited function's start) is compared
too, because round 19 found page differences that were the previous function's tail.

Section offsets come from pefile (the .text raw pointer of each image); both files are read
through mmap. Both images are read only; the .i64 database is never opened.

    python -I _tools/ida_claim_bytes.py          > section.md   (markdown section for the doc)
    python -I _tools/ida_claim_bytes.py --tsv    > rows.tsv     (one line per cited function)
"""
import bisect
import mmap
import os
import sqlite3
import sys
from collections import Counter

import pefile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ida_claim_exposure import NEW, REF, classify, collect_cites, page_classes  # noqa: E402
from rva_status import CORPUS  # noqa: E402

TABLE_CAP = 60


def text_section(path):
    """(va, size, raw_pointer) of the .text section, read with pefile."""
    pe = pefile.PE(path, fast_load=True)
    try:
        s = next(x for x in pe.sections if x.Name.rstrip(b"\0") == b".text")
        return s.VirtualAddress, min(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData
    finally:
        pe.close()


def span(sec, lo, hi):
    """File offsets of [lo, hi) when the range lies wholly inside .text, else None."""
    va, size, raw = sec
    if lo < va or hi > va + size or hi <= lo:
        return None
    return raw + (lo - va), raw + (hi - va)


def diff_bytes(a, b, lo):
    """(identical?, number of differing bytes, first differing rva) for two equal-length buffers."""
    if a == b:
        return True, 0, None
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    return False, len(diff), lo + diff[0]


def main():
    tsv = "--tsv" in sys.argv
    sys.stdout.reconfigure(encoding="utf-8")
    cls = page_classes()
    cites = collect_cites()
    db = sqlite3.connect(f"file:///{CORPUS}/corpus.sqlite?mode=ro", uri=True)
    new_sec, ref_sec = text_section(NEW), text_section(REF)
    fa, fb = open(NEW, "rb"), open(REF, "rb")
    ma = mmap.mmap(fa.fileno(), 0, access=mmap.ACCESS_READ)
    mb = mmap.mmap(fb.fileno(), 0, access=mmap.ACCESS_READ)

    def compare(lo, hi):
        """Own-bytes status of [lo, hi): 'same', 'differs' (count, first rva) or 'n/a'."""
        a, b = span(new_sec, lo, hi), span(ref_sec, lo, hi)
        if a is None or b is None:
            return "n/a", 0, None
        eq, n, first = diff_bytes(ma[a[0]:a[1]], mb[b[0]:b[1]], lo)
        return ("same" if eq else "differs"), n, first

    rows, no_row = [], 0
    for r in classify(cls, cites, fa, db):
        if r["lo"] is None:
            no_row += 1
            continue
        lo, hi = r["lo"], r["hi"]
        own, own_n, own_first = compare(lo, hi)
        prev = db.execute("select rva,end_rva from functions where rva<? order by rva desc limit 1", (lo,)).fetchone()
        if prev:
            p_own, p_n, _ = compare(prev[0], prev[1])
        else:
            p_own, p_n = "no row", 0
        rows.append(dict(r, own=own, own_n=own_n, own_first=own_first, prev=prev,
                         prev_own=p_own, prev_n=p_n, contig=bool(prev) and prev[1] == lo))

    # Several cited addresses often fall in one function: merge to one row per function.
    funcs = {}
    for x in rows:
        key = (x["lo"], x["hi"])
        if key in funcs:
            funcs[key]["docs"] = funcs[key]["docs"] | x["docs"]
        else:
            funcs[key] = dict(x)
    rows = sorted(funcs.values(), key=lambda x: x["lo"])

    table = db.execute("select rva,end_rva from functions order by rva").fetchall()
    starts = [t[0] for t in table]

    def owner_row(v):
        """The corpus row containing rva v (largest start <= v with end > v), or None."""
        i = bisect.bisect_right(starts, v) - 1
        for j in range(i, max(i - 64, -1), -1):
            if table[j][1] > v:
                return table[j]
        return None

    # Where do the differing bytes of a function with identical own bytes lie? Scan its pages
    # outside its own range and name the corpus row that owns each differing byte (None = no row).
    for x in rows:
        x["owners"] = {}
        if x["class"] not in ("stub", "differs") or x["own"] == "differs":
            continue
        pg0, pg1 = x["lo"] & ~0xFFF, ((x["hi"] - 1) | 0xFFF) + 1
        a, b = span(new_sec, pg0, pg1), span(ref_sec, pg0, pg1)
        if a is None or b is None:
            continue
        ba, bb = ma[a[0]:a[1]], mb[b[0]:b[1]]
        for i in range(len(ba)):
            r = pg0 + i
            if x["lo"] <= r < x["hi"] or ba[i] == bb[i]:
                continue
            ow = owner_row(r)
            key = (ow[0], ow[1]) if ow else None
            x["owners"][key] = x["owners"].get(key, 0) + 1
        owned = [k for k in x["owners"] if k is not None]
        if any(compare(*k)[0] == "differs" for k in owned):
            x["owner_kind"] = "neighbour differs" + (" + gap" if None in x["owners"] else "")
        elif None in x["owners"]:
            x["owner_kind"] = "gap only"
        else:
            x["owner_kind"] = "other"

    cls_counts = Counter(x["class"] for x in rows)
    own_counts = Counter(x["own"] for x in rows)
    risk = [x for x in rows if x["class"] in ("stub", "differs")]
    risk_own = sum(1 for x in risk if x["own"] == "differs")
    ident = [x for x in risk if x["own"] != "differs"]
    kind = Counter(x.get("owner_kind", "none") for x in ident)
    risk_prev = sum(1 for x in ident if x["prev_own"] == "differs")
    risk_owner = sum(n for k, n in kind.items() if k.startswith("neighbour"))
    risk_gap = kind["gap only"]
    risk_other = len(ident) - risk_owner - risk_gap
    unk_diff = sum(1 for x in rows if x["class"] == "unknown" and x["own"] == "differs")
    diff_rows = [x for x in rows if x["own"] == "differs"]

    if tsv:
        print("cited\tclass\tfunc\tfunc_end\tstub_in_body\town\town_ndiff\town_first\tprev\tprev_own\tprev_ndiff\tcontig\towner_kind\towners\tdocs")
        for x in rows:
            d = ";".join(sorted({f"{a}:{b}" for a, b in x["docs"]}))
            prev = hex(x["prev"][0]) if x["prev"] else "-"
            print(hex(x["rva"]), x["class"], hex(x["lo"]), hex(x["hi"]), x["fstub"], x["own"], x["own_n"],
                  hex(x["own_first"]) if x["own_first"] is not None else "-", prev, x["prev_own"], x["prev_n"],
                  "yes" if x["contig"] else "no", x.get("owner_kind", "-"),
                  ";".join(f"{hex(k[0])}-{hex(k[1])}:{n}" if k else f"gap:{n}"
                           for k, n in x.get("owners", {}).items()) or "-",
                  d, sep="\t")
        return

    o = print
    o("### Byte-level comparison\n")
    o("The own bytes of each cited function that has a corpus row in `.text` were compared between the analysis image and the reference image (file offsets from each image's `.text` section). "
      "For the functions in the 'stub' and 'differs' categories the immediately preceding corpus function was compared the same way.\n")
    o("| Measure | Count |")
    o("|---|---:|")
    o(f"| Cited functions in `.text` (distinct corpus rows) | {len(rows)} |")
    o(f"| Cited addresses with no function row (not compared) | {no_row} |")
    o(f"| Own bytes identical | {own_counts['same']} |")
    o(f"| Own bytes differ (any category) | {own_counts['differs']} |")
    o(f"| Not comparable (range outside the reference `.text`) | {own_counts['n/a']} |")
    o(f"| Own bytes differ, category 'unknown' (page not in the recovered table) | {unk_diff} |")
    o(f"| Category clean | {cls_counts['clean']} |")
    o(f"| Category stub or differs | {len(risk)} |")
    o(f"| &nbsp;&nbsp;of which own bytes differ | {risk_own} |")
    o(f"| &nbsp;&nbsp;of which own bytes identical | {len(ident)} |")
    o(f"| &nbsp;&nbsp;&nbsp;&nbsp;differing bytes outside its range lie in a corpus row whose own bytes differ | {risk_owner} |")
    o(f"| &nbsp;&nbsp;&nbsp;&nbsp;differing bytes outside its range lie in no corpus row | {risk_gap} |")
    o(f"| &nbsp;&nbsp;&nbsp;&nbsp;other | {risk_other} |")
    o(f"| &nbsp;&nbsp;&nbsp;&nbsp;(immediately preceding row has differing own bytes, for reference) | {risk_prev} |")
    o("")
    if not diff_rows:
        o("No cited function has differing own bytes.\n")
    else:
        o(f"Cited functions whose own bytes differ between the images ({len(diff_rows)} rows, by start address; at most {TABLE_CAP} shown). "
          "'Preceding' is the corpus function immediately below the cited start, with its own-bytes status.\n")
        o("| Function | Category | Stub in body | Differing own bytes (first rva) | Preceding function | Preceding own bytes | Cited at |")
        o("|---|---|---|---|---|---|---|")
        for x in diff_rows[:TABLE_CAP]:
            docs = sorted({f"{a}:{b}" for a, b in x["docs"]})
            cited_at = "; ".join(f"`{d}`" for d in docs[:2]) + (f" +{len(docs) - 2}" if len(docs) > 2 else "")
            prev = f"`{hex(x['prev'][0])}`–`{hex(x['prev'][1])}`" if x["prev"] else "no row"
            o(f"| `{hex(x['lo'])}`–`{hex(x['hi'])}` | {x['class']} | {x['fstub']} | {x['own_n']} (`{hex(x['own_first'])}`) | "
              f"{prev} | {x['prev_own']} | {cited_at} |")
        if len(diff_rows) > TABLE_CAP:
            o(f"\n{len(diff_rows) - TABLE_CAP} more rows are in the `--tsv` output of `_tools/ida_claim_bytes.py`.")
    print("#", dict(cls_counts), file=sys.stderr)


if __name__ == "__main__":
    main()
