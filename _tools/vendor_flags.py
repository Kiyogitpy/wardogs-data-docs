"""Round 43: vendor variation flags (bShowInVendor, bIsPreviewOnly, LevelToUnlock) for every vendor row.

Reads every DataTable under data/ whose rows carry WDVendorItemVariationData (VendorItemVariations) and
writes assets/data/vendor-flags.json: totals, the LevelToUnlock histogram, and one record per hidden or
preview-only variation (table, row, variation tag, price, amount, level, categories).

    python -I _tools/vendor_flags.py            # rewrite assets/data/vendor-flags.json (idempotent)
    python -I _tools/vendor_flags.py --check    # exit 1 if the file is stale
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "vendor-flags.json")
SPLIT = re.compile(r"^--- export:.*---\s*$", re.M)


def tag(o):
    return o.get("TagName") if isinstance(o, dict) else None


def build():
    tables, hidden, preview = {}, [], []
    lv = {}
    wt = {}
    files = sorted(glob.glob(os.path.join(ROOT, "data", "**", "*.json"), recursive=True))
    for f in files:
        txt = open(f, encoding="utf8", errors="ignore").read()
        if "bShowInVendor" not in txt:
            continue
        name = os.path.relpath(f, ROOT).replace("\\", "/")
        short = name.split("/")[-1][:-5]
        for part in SPLIT.split(txt):
            part = part.strip()
            if not part.startswith("{"):
                continue
            try:
                d = json.loads(part)
            except ValueError:
                continue
            for row, rv in (d.get("Rows") or {}).items():
                for i, v in enumerate(rv.get("VendorItemVariations") or []):
                    if "bShowInVendor" not in v:
                        continue
                    t = tables.setdefault(short, {"variations": 0, "hidden": 0, "previewOnly": 0})
                    t["variations"] += 1
                    L = v.get("LevelToUnlock")
                    lv[str(L)] = lv.get(str(L), 0) + 1
                    if v.get("bOverwriteWeight"):
                        wt[v.get("OverwrittenWeight")] = wt.get(v.get("OverwrittenWeight"), 0) + 1
                    rec = {"table": short, "row": row, "index": i, "variation": tag(v.get("VariationTag")),
                           "price": v.get("Price"), "amount": v.get("Amount"), "level": L,
                           "showInVendor": v.get("bShowInVendor"), "previewOnly": v.get("bIsPreviewOnly"),
                           "categories": [c if isinstance(c, str) else tag(c) for c in v.get("Categories", [])]}
                    if v.get("bShowInVendor") is False:
                        t["hidden"] += 1
                        hidden.append(rec)
                    if v.get("bIsPreviewOnly"):
                        t["previewOnly"] += 1
                        preview.append(rec)
    both = sum(1 for r in hidden if r["previewOnly"])
    return {"meta": {"source": "data/**/ DataTables with WDVendorItemVariationData (bShowInVendor +0x188, bIsPreviewOnly +0x189, LevelToUnlock +0xEC)",
                     "variations": sum(t["variations"] for t in tables.values()),
                     "hidden": len(hidden), "previewOnly": len(preview), "hiddenAndPreviewOnly": both,
                     "levelToUnlockHistogram": dict(sorted(lv.items())),
                     "overwrittenWeightUsed": {str(k): v for k, v in sorted(wt.items(), key=lambda x: str(x[0]))}},
            "tables": dict(sorted(tables.items())), "hidden": hidden}


def main():
    out = json.dumps(build(), indent=1, sort_keys=False) + "\n"
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else ""
        if cur != out:
            print("vendor-flags.json is stale")
            sys.exit(1)
        print("ok")
        return
    with open(OUT, "w", encoding="utf8", newline="\n") as fh:
        fh.write(out)
    m = json.loads(out)["meta"]
    print({k: m[k] for k in ("variations", "hidden", "previewOnly", "hiddenAndPreviewOnly", "levelToUnlockHistogram")})


if __name__ == "__main__":
    main()
