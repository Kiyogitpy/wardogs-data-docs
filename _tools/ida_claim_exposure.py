"""Exposure of cited native addresses to the protection layer's indirect dispatch stubs.

For every docs/ pipelines/ content/ game-features/ page, extracts the 0x tokens that
_tools/rva_status.py treats as RVAs (>= 0x100000), resolves each to its corpus function
(exact row, else the enclosing row) and classifies the function by the 4 KiB code pages it
spans in the static-analysis image, compared with the older reference image:

    exceptional  a spanned page is one of the eleven separately captured pages
    stub         a spanned page differs and contains a differing indirect dispatch stub
    differs      a spanned page differs and contains no recognised stub
    clean        every spanned page is byte-identical to the reference
    unknown      not in a recovered protected page (other section, unprotected text, no row)

"stub" means the page holds a stub; it does not say the claim is wrong. The page set is
rebuilt here from the two images so no private capture file is read at classification time
beyond the page list (--pages cache). Local paths below; edit to rerun elsewhere.

    python -I _tools/ida_claim_exposure.py > out.tsv
"""
import glob
import json
import os
import re
import sqlite3
import sys

import capstone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rva_status import CORPUS, ROOT, cited  # noqa: E402

BASE = "E:/Reverse_Engineer/wardogs_analysis/"
FIX = BASE + "_RE_bench/findings/remaining_fixes_20261018/"
NEW = FIX + "fresh_build/analysis_with_filtered_partial_unwind.exe"
REF = BASE + "WardogsClient-Win64-Shipping.restored.exe"
TEXT_END, REF_RAW = 0x9A27000, 0x600
DIRS = ("docs", "pipelines", "content", "game-features")
SKIP = {"docs/IDA_CLAIM_EXPOSURE.md"}


def stubs(data, rva):
    """mov reg,[rip+x] ; jmp [reg+disp] pairs (same recogniser as the supplement classifier)."""
    dec = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    dec.detail = True
    out = []
    for o in range(len(data) - 16):
        if not (0x48 <= data[o] <= 0x4F and data[o + 1] == 0x8B and data[o + 2] & 0xC7 == 5):
            continue
        ins = list(dec.disasm(data[o:o + 24], rva + o, count=2))
        if len(ins) != 2 or ins[0].mnemonic != "mov" or ins[1].mnemonic != "jmp":
            continue
        (d, s), j = ins[0].operands, ins[1].operands[0]
        if (d.type == capstone.x86.X86_OP_REG and s.type == capstone.x86.X86_OP_MEM
                and s.mem.base == capstone.x86.X86_REG_RIP and j.type == capstone.x86.X86_OP_MEM
                and j.mem.base == d.reg and not j.mem.index):
            out.append(rva + o)
    return out


def page_classes():
    prot = set()
    for f in glob.glob(FIX + "fresh_collection/*/pages_pages.jsonl"):
        for line in open(f):
            prot.add(int(json.loads(line)["rva"], 16))
    exc = {int(p["rva"], 16) for p in json.load(open(FIX + "metadata/supplement_page_classification.json"))["pages"]}
    a, b = open(NEW, "rb"), open(REF, "rb")
    cls = {}
    for rva in sorted(prot | exc):
        a.seek(rva); x = a.read(0x1000); a.read(0)
        a.seek(rva + 0x1000); xn = a.read(24)
        b.seek(rva - 0x1000 + REF_RAW); y = b.read(0x1000)
        b.seek(rva + REF_RAW); yn = b.read(24)
        if rva in exc:
            cls[rva] = "exceptional"
        elif x == y:
            cls[rva] = "clean"
        else:
            s = set(stubs(x + xn, rva)) | set(stubs(y + yn, rva))
            hit = any((x + xn)[r - rva:r - rva + 16] != (y + yn)[r - rva:r - rva + 16] for r in s)
            cls[rva] = "stub" if hit else "differs"
    return cls


def collect_cites():
    cites = {}
    for d in DIRS:
        for p in glob.glob(os.path.join(ROOT, d, "**", "*.md"), recursive=True):
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            if rel in SKIP:
                continue
            for v, secs in cited(open(p, encoding="utf-8", errors="replace").read()).items():
                for ls in secs.values():
                    for n in ls:
                        cites.setdefault(v, set()).add((rel, n))
    return cites


def classify(cls, cites, img, db):
    """Yield one dict per cited address: its worst page class and its containing function row."""
    rank = ["exceptional", "stub", "differs", "clean"]
    for v in sorted(cites):
        fn = db.execute("select rva,end_rva from functions where rva<=? and end_rva>? order by rva desc limit 1", (v, v)).fetchone()
        own = cls.get(v & ~0xFFF, "unknown") if v < TEXT_END else "unknown"
        row = {"rva": v, "own_page": own, "lo": None, "hi": None, "fstub": "-", "docs": cites[v]}
        if v >= TEXT_END:
            row["class"] = "unknown"
        else:
            lo, hi = (fn if fn else (v, v + 1))
            pgs = [cls.get(p, "unknown") for p in range(lo & ~0xFFF, ((hi - 1) | 0xFFF) + 1, 0x1000)]
            row["class"] = "unknown" if "unknown" in pgs else next(r for r in rank if r in pgs)
            if fn and hi - lo <= 0x40000:
                img.seek(lo); row["fstub"] = "yes" if stubs(img.read(hi - lo), lo) else "no"
            if fn:
                row["lo"], row["hi"] = lo, hi
        yield row


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cls = page_classes()
    from collections import Counter
    print("#pages", dict(Counter(cls.values())), file=sys.stderr)
    cites = collect_cites()
    db = sqlite3.connect(f"file:///{CORPUS}/corpus.sqlite?mode=ro", uri=True)
    img = open(NEW, "rb")
    print("rva	class	own_page	func	func_end	func_has_stub	docs")
    for r in classify(cls, cites, img, db):
        fr, fe = (hex(r["lo"]), hex(r["hi"])) if r["lo"] is not None else (("-", "-") if r["rva"] >= TEXT_END else ("no row", "-"))
        docs = ";".join(sorted({f"{d}:{n}" for d, n in r["docs"]}))
        print(hex(r["rva"]), r["class"], r["own_page"], fr, fe, r["fstub"], docs, sep="	")


if __name__ == "__main__":
    main()
