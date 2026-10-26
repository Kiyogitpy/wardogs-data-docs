"""Item icon textures: build the extractor list, collect the PNGs and write assets/data/item-icons.json.

    python -I _tools/item_icons.py list  <files.txt> <list.txt>   # file paths to extract (one per line)
    python -I _tools/item_icons.py build <files.txt> <extractor-out>   # copy PNGs to assets/img/icons/<category>/ + write the JSON

files.txt is WdExtract's `list ""` output (cooked package file paths); the packages are matched to it
case-insensitively (plugin mount points such as /Buildables/ live under Wardogs/Plugins/**/Content/).
    python -I _tools/item_icons.py --check                 # every referenced icon has a PNG (exit 1 otherwise)

Sources (all under data/): the `Icons` struct of every entity-data row (FallbackIcon, TaggedIcons) and the
vendor-row `OverwrittenIcon` variations (DT_*Market and mode weapon-select tables). Static data only.
Display names are the rows' FriendlyName strings (the names the wiki uses). See
game-features/Wardogs_AttachmentsPlatforms_v1.md ("Icon textures") for the extraction command.
"""
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT_IMG = os.path.join(ROOT, "assets", "img", "icons")
OUT_JSON = os.path.join(ROOT, "assets", "data", "item-icons.json")
ICON_ROOT = "/Game/UI/Shared/Icons/"


def load(path):
    s = open(path, encoding="utf8").read()
    return json.loads(s[s.index("{"):])


def pkg(p):
    """'/Game/X/T_A.T_A' -> '/Game/X/T_A'; empty/None stays ''."""
    return p.rsplit(".", 1)[0] if p else ""


def category(package):
    d = package.rsplit("/", 1)[0]
    if package.startswith(ICON_ROOT):
        rel = d[len(ICON_ROOT):].strip("/") or "generic"
        return re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")
    parts = [x for x in d.split("/") if x]
    return "other-" + re.sub(r"[^a-z0-9]+", "-", "-".join(parts[-2:]).lower()).strip("-")


def walk_files():
    for dp, _, fs in os.walk(DATA):
        for f in sorted(fs):
            if f.endswith(".json"):
                yield os.path.join(dp, f)


def name_of(row):
    fn = row.get("FriendlyName")
    if isinstance(fn, dict):
        return fn.get("LocalizedString") or fn.get("SourceString") or ""
    return ""


def collect():
    items = {}
    overrides = {}
    for path in walk_files():
        base = os.path.basename(path)
        if "EntityData" in base:
            try:
                rows = load(path).get("Rows") or {}
            except Exception:
                continue
            for rid, r in rows.items():
                ic = r.get("Icons") if isinstance(r, dict) else None
                if not isinstance(ic, dict):
                    continue
                fb = pkg((ic.get("FallbackIcon") or {}).get("AssetPathName", ""))
                tagged = {}
                for t in ic.get("TaggedIcons") or []:
                    tagged[pkg(t["Key"])] = list(t["Value"])
                vendor = next((k for k, v in tagged.items() if "UI.Icon.Vendor" in v), "")
                inv = next((k for k, v in tagged.items() if any(x.startswith("UI.Icon.Inventory") for x in v)), "") or fb
                items[rid] = {"name": name_of(r), "vendor": vendor, "inventory": inv,
                              "fallback": fb, "tagged": tagged}
        elif "OverwrittenIcon" in open(path, encoding="utf8", errors="ignore").read():
            rows = load(path).get("Rows") or {}
            for rid, r in rows.items():
                found = set()

                def w(o):
                    if isinstance(o, dict):
                        oi = o.get("OverwrittenIcon")
                        if isinstance(oi, dict) and o.get("bOverwriteIcon") and oi.get("AssetPathName"):
                            found.add(pkg(oi["AssetPathName"]))
                        for v in o.values():
                            w(v)
                    elif isinstance(o, list):
                        for v in o:
                            w(v)
                w(r)
                if found:
                    overrides.setdefault(rid, set()).update(found)
    return items, overrides


def all_packages(items, overrides):
    s = set()
    for it in items.values():
        for k in ("vendor", "inventory", "fallback"):
            if it[k]:
                s.add(it[k])
        s.update(k for k in it["tagged"] if k)
    for v in overrides.values():
        s.update(v)
    return sorted(x for x in s if x)


def index_files(path):
    """lower-case package name -> cooked file path, e.g. /game/ui/x -> Wardogs/Content/UI/x."""
    idx = {}
    for line in open(path, encoding="utf8"):
        f = line.strip()
        if not f:
            continue
        if f.startswith("Wardogs/Content/"):
            idx[("/Game/" + f[len("Wardogs/Content/"):]).lower()] = f
        elif f.startswith("Wardogs/Plugins/") and "/Content/" in f:
            head, rest = f.split("/Content/", 1)
            idx[("/" + head.rsplit("/", 1)[1] + "/" + rest).lower()] = f
    return idx


def png_rel(package):
    return f"assets/img/icons/{category(package)}/{package.rsplit('/', 1)[1]}.png"


def main():
    a = sys.argv[1:]
    items, overrides = collect()
    pk = all_packages(items, overrides)
    if a[:1] == ["list"]:
        idx = index_files(a[1])
        res = [idx[p.lower()] for p in pk if p and p.lower() in idx]
        for p in pk:
            if p.lower() not in idx:
                print("not in paks:", p)
        open(a[2], "w").write("\n".join(res) + "\n")
        print(f"{len(res)} resolved of {len(pk)} texture packages, {len(items)} items with icons, {len(overrides)} vendor rows with overrides")
        return 0
    if a[:1] == ["build"]:
        idx = index_files(a[1])
        src = a[2]
        ok, miss = [], []
        for p in pk:
            f = os.path.join(src, idx.get(p.lower(), "?") + ".png")
            if os.path.exists(f):
                dst = os.path.join(ROOT, png_rel(p))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(f, dst)
                ok.append(p)
            else:
                miss.append(p)
        have = set(ok)

        def ref(p):
            return {"texture": p, "png": png_rel(p) if p in have else None} if p else None
        out = {"_note": "Icon textures per item id. vendor = shop icon, inventory = inventory icon, "
                        "overrides = vendor-market OverwrittenIcon variations. Regenerate with _tools/item_icons.py.",
               "items": {}}
        for rid in sorted(items):
            it = items[rid]
            e = {"name": it["name"], "vendor": ref(it["vendor"]), "inventory": ref(it["inventory"])}
            if it["fallback"] and it["fallback"] != it["inventory"]:
                e["fallback"] = ref(it["fallback"])
            others = [ref(k) for k in it["tagged"] if k not in (it["vendor"], it["inventory"])]
            if others:
                e["other"] = others
            if rid in overrides:
                e["overrides"] = [ref(k) for k in sorted(overrides[rid])]
            out["items"][rid] = e
        for rid in sorted(overrides):
            if rid not in items:
                out["items"][rid] = {"name": "", "vendor": None, "inventory": None,
                                     "overrides": [ref(k) for k in sorted(overrides[rid])]}
        out["missing"] = miss
        with open(OUT_JSON, "w", encoding="utf8") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"{len(ok)} PNGs copied, {len(miss)} missing")
        return 0
    if a[:1] == ["--check"]:
        bad = [p for p in pk if not os.path.exists(os.path.join(ROOT, png_rel(p)))]
        for p in bad:
            print("no PNG:", p)
        print(f"{len(pk) - len(bad)}/{len(pk)} referenced icons have a PNG")
        return 1 if bad else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
