"""Corpus status of every native address a pipeline doc cites.

Extracts every 0x token from the doc, drops values below 0x100000 (offsets, sizes and
enum values) and the flag 0x40000000, and queries the decompilation corpus read-only for
each remaining RVA. Used for the RVA status tables on the docs/evidence/ pages.

    python -I _tools/rva_status.py pipelines/Wardogs_VehicleDamagePipeline_v1.md
    python -I _tools/rva_status.py pipelines/Wardogs_GameplayEffectsPipeline_v1.md --rev 479c6c1 --exe

One tab-separated line per RVA:

1. the RVA;
2. the sections that cite it, with doc line numbers;
3. the PE section it falls in (--exe only, read from the restored executable with pefile);
4. "body" when a functions row at that exact RVA is decompiled with a code path, has no
   JUMPOUT or inline assembly and a non-empty body, otherwise "-";
5. the row's status and reason, or "no row";
6. the number of direct calls in the calls table that target the RVA;
7. the enclosing row when there is no exact one;
8. aliases (vtable slots, registration pairs);
9. flags: Hex-Rays warning lines ("positive sp value" usually means the row starts at the
   wrong byte; "may be wrong" means variable allocation failed) and "empty" for a
   nullsub row whose body is blank.

--rev reads the doc as of a commit instead of the working tree. Nothing is written. The
corpus and executable paths below are local; edit them to rerun elsewhere.
"""
import argparse
import os
import re
import sqlite3
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = "E:/Reverse_Engineer/wardogs_analysis/decompiled_cl516586_20261017_mmvpuc__"
EXE = "E:/Reverse_Engineer/wardogs_analysis/WardogsClient-Win64-Shipping.restored.exe"
WARN = re.compile(r"JUMPOUT|__asm|positive sp value|may be wrong")


def cited(text):
    """{rva: {section: [line numbers]}} for every 0x token >= 0x100000 in the doc."""
    out, section = {}, "intro"
    for n, line in enumerate(text.splitlines(), 1):
        h = re.match(r"#{2,3}\s+(\d+(?:\.\d+)*)\.?\s", line)
        if h:
            section = "§" + h.group(1)
        elif re.match(r"#{2,3}\s+", line):
            section = line.strip("# ")
        for tok in re.findall(r"0x[0-9A-Fa-f]+", line):
            v = int(tok, 16)
            if v >= 0x100000 and v != 0x40000000:
                lines = out.setdefault(v, {}).setdefault(section, [])
                if n not in lines:
                    lines.append(n)
    return out


def body_text(row):
    path, off, length = row[4:7]
    if not path:
        return ""
    p = path if os.path.isabs(path) else os.path.join(CORPUS, path)
    with open(p, "rb") as f:
        f.seek(off)
        return f.read(length).decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", help="doc path relative to the repository root")
    ap.add_argument("--rev", help="read the doc at this git commit")
    ap.add_argument("--exe", action="store_true", help="also report the PE section of each RVA")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.rev:
        text = subprocess.run(["git", "-C", ROOT, "show", f"{a.rev}:{a.doc}"], check=True,
                              capture_output=True).stdout.decode("utf-8")
    else:
        with open(os.path.join(ROOT, a.doc), encoding="utf-8") as f:
            text = f.read()
    rvas = cited(text)
    db = sqlite3.connect(f"file:///{CORPUS}/corpus.sqlite?mode=ro", uri=True)
    sections = []
    if a.exe:
        import pefile
        pe = pefile.PE(EXE, fast_load=True)
        sections = [(s.VirtualAddress, s.VirtualAddress + s.Misc_VirtualSize,
                     s.Name.rstrip(b"\0").decode()) for s in pe.sections]
    for v in sorted(rvas):
        fn = db.execute("select rva,name,status,reason,code_path,code_offset,code_length "
                        "from functions where rva=?", (v,)).fetchone()
        tr = db.execute("select has_inline_assembly,has_jumpout from traits where rva=?", (v,)).fetchone()
        inside = None if fn else db.execute(
            "select rva,status from functions where rva<? and end_rva>? order by rva desc limit 1",
            (v, v)).fetchone()
        calls = db.execute("select count(*) from calls where target_rva=?", (v,)).fetchone()[0]
        al = db.execute("select name,kind,slot from aliases where rva=? limit 3", (v,)).fetchall()
        text = body_text(fn) if fn else ""
        flags = sorted({m.group(0) for m in WARN.finditer(text)})
        if fn and fn[1].startswith("nullsub") and re.search(r"\{\s*;?\s*\}", text):
            flags.append("empty")
        body = bool(fn and fn[2] in ("decompiled", "decompiled_with_jumps") and fn[4]
                    and tr == (0, 0) and not {"JUMPOUT", "__asm", "empty"} & set(flags))
        where = ", ".join(f"{k} (L{','.join(map(str, ls))})" for k, ls in rvas[v].items())
        print(f"0x{v:X}", where,
              next((n for lo, hi, n in sections if lo <= v < hi), "?") if a.exe else "",
              "body" if body else "-",
              f"{fn[2]}:{fn[3] or ''}" if fn else "no row",
              f"calls={calls}",
              f"in 0x{inside[0]:X} ({inside[1]})" if inside else "-",
              "; ".join(f"{n}[{k}{'' if s is None else ' ' + str(s)}]" for n, k, s in al) or "-",
              "flags=" + "|".join(flags) if flags else "-",
              sep="\t")
    print(f"{len(rvas)} RVAs")


if __name__ == "__main__":
    main()
