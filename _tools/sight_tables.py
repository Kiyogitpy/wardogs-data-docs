"""Tables for content/Wardogs_Sights_v1.md and assets/data/sights.json: every sight attachment with its numbers.

Reads the sight items (`Item.Attachment.Sight`) from data/ through _tools/weapon_attributes.py (item loading,
sub-slot filters, effects), the sight entries' zoom data (`SightsData`: VariableZoomData and the stored
AdsZoomMultiplier), and assets/data/ loadout-builder.json (names, shop prices), loadout-extras.json (unlock
levels, reticle images) and scope-reticles.json. Each table sits between

    <!-- sight_tables MODE -->  ...  <!-- /sight_tables -->

on the page. Rerun after a data update (idempotent):

    python -I _tools/sight_tables.py --write     # refresh the JSON and every block in place
    python -I _tools/sight_tables.py --check     # exit 1 when the JSON or a block is stale
    python -I _tools/sight_tables.py MODE        # print one block (main, fits, reticles)

ADS field of view (docs/evidence/round46-a.md, round79-sight-zoom.md): aimed angle = base / magnification, base =
the Field of view setting (default 90) unless the sight's "test value" is 3.25 or more, then 72. The test value is
the stored AdsZoomMultiplier of the sight's first entry, or max(stored, ZoomMultiplierMax) for a variable-zoom
sight. Apparent zoom = tan(45 deg) / tan(aimed angle / 2). Derived from the camera code, not measured on screen.
"""
import argparse
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weapon_attributes as wa  # noqa: E402

ROOT = wa.ROOT
PAGE = os.path.join(ROOT, "content/Wardogs_Sights_v1.md")
OUT = os.path.join(ROOT, "assets/data/sights.json")
BLOCK = re.compile(r"<!-- sight_tables (\w+) -->\r?\n.*?<!-- /sight_tables -->", re.S)
SIGHT_TAG = "Item.Attachment.Sight"
BASE_FOV = 90.0          # default Field of view setting
INDEPENDENT_FOV = 72.0   # base for the Independent mode and for test values >= 3.25
TEST_LIMIT = 3.25
ENTRY_NAMES = {"S_Aim01": "Main sight", "S_Aim02": "Second sight", "S_AimCanted1": "Canted sight"}
ATTR = "Attribute.Gameplay.Weapon."
EVID = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/"


def g(x):
    return f"{x:.4g}" if abs(x) < 1000 else f"{x:,.0f}"


def load_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def raw_sights(item):
    """{entry: (stored AdsZoomMultiplier, VariableZoomData)} from the item's export."""
    with open(os.path.join(ROOT, item.path), encoding="utf-8") as f:
        objs = [json.loads(p) for p in wa.EXPORT.split(f.read()) if p.strip()]
    out = {}
    for o in objs:
        ad = (o.get("Properties") or {}).get("AttachmentData")
        if ad:
            for s in ad.get("SightsData", []):
                v = s["Value"]
                out[s["Key"]] = (v.get("AdsZoomMultiplier"), v.get("VariableZoomData") or {})
    return out


def modifiers(data, effects, attr):
    """The modifiers an ordered effect list applies to one attribute."""
    out = []
    for e in effects:
        eff = data.effects.get(e)
        for m in (eff["modifiers"] if eff else []):
            if m["attribute"] == ATTR + attr:
                out.append(m)
    return out


def describe_time(mods):
    parts = []
    for m in mods:
        v = m.get("value", 0.0)
        if m["op"] in ("Multiply", "MultiplyCompound", "Divide") and v == 1.0:
            continue  # x1 changes nothing
        parts.append({"Override": f"set to {g(v)} s", "Add": f"{v:+g} s", "AddFinal": f"{v:+g} s",
                      "Multiply": f"x{g(v)}", "MultiplyCompound": f"x{g(v)}", "Divide": f"/{g(v)}"}[m["op"]])
    return ", ".join(parts) if parts else "no change"


def zeroing(mods_min, mods_max):
    def one(mods):
        for m in mods:
            if m["op"] == "Override":
                return {"value": m["value"]} if m["kind"] == "Scalar" else {"follows": m.get("backing_attribute", "").split(".")[-1]}
        return None
    return one(mods_min), one(mods_max)


def zeroing_text(zmin, zmax):
    if zmin is None and zmax is None:
        return "weapon's own"
    a = g(zmin["value"]) if zmin else "weapon's own"
    b = "weapon's own" if zmax is None else ("same as min" if "follows" in zmax else g(zmax["value"]))
    return f"min {a}, max {b}"


def fov_for(mag, base):
    ang = base / mag
    return round(ang, 2), round(math.tan(math.radians(45)) / math.tan(math.radians(ang / 2)), 2)


def collect():
    data = wa.Data()
    builder = load_json("assets/data/loadout-builder.json")["items"]
    extras = load_json("assets/data/loadout-extras.json")
    scope = load_json("assets/data/scope-reticles.json")["items"]
    sights = [it for it in data.attachments if SIGHT_TAG.lower() in [c for c in it.context] or it.att_type == SIGHT_TAG]
    sights = [it for it in sights if it.att_type == SIGHT_TAG]
    weapons = [w for w in data.weapons if w.asset in builder or True]
    wname = {w.asset: (builder.get(w.asset) or {}).get("name") or w.display for w in weapons}
    fits = {}
    for w in weapons:
        cont = wa.reachable_containers(data, w)
        for s in sights:
            if any(wa.accepts(c, s) for c in cont):
                fits.setdefault(s.asset, []).append(w.asset)
    rows = []
    for it in sights:
        rs = raw_sights(it)
        b = builder.get(it.asset) or {}
        entries = []
        first_key = "S_Aim01" if "S_Aim01" in it.sights else next(iter(it.sights), None)
        stored, vz = rs.get(first_key, (None, {}))
        can = bool(vz.get("bCanVariableZoom"))
        test = max(stored or 0, vz.get("ZoomMultiplierMax") or 0) if can else (stored or 0)
        base = INDEPENDENT_FOV if test >= TEST_LIMIT else BASE_FOV
        for key, effs in it.sights.items():
            chain = it.applied + effs
            zoom = [m for m in modifiers(data, chain, "AdsZoomMultiplier") if m["op"] == "Override" and m["kind"] == "Scalar"]
            mag = zoom[0]["value"] if zoom else None
            ent = {"entry": key, "name": ENTRY_NAMES.get(key, key), "effects": it.applied + effs, "magnification": mag,
                   "aimTime": describe_time(modifiers(data, chain, "AimTime"))}
            zmin, zmax = zeroing(modifiers(data, chain, "MinZeroingRange"), modifiers(data, chain, "MaxZeroingRange"))
            ent["zeroing"] = {"min": zmin, "max": zmax}
            if mag:
                top = vz.get("ZoomMultiplierMax") if (can and key == first_key) else None
                lo, hi = (mag, top if top and top > mag else mag)
                ent["zoomRange"] = [lo, hi]
                ent["adsFov"] = [fov_for(lo, base)[0], fov_for(hi, base)[0]]
                ent["apparent"] = [fov_for(lo, base)[1], fov_for(hi, base)[1]]
            entries.append(ent)
        unl = extras["unlocks"].get(it.asset)
        tree = next(iter(unl)) if unl else None
        ret = extras["reticles"].get(it.asset) or {}
        sc = scope.get(it.item_id)
        rows.append({
            "id": it.asset, "itemId": it.item_id, "name": b.get("name") or it.display or it.asset,
            "icon": b.get("icon") or extras["icons"].get(it.asset),
            "price": b.get("price"), "unlock": ({"tree": tree, "level": unl[tree][0], "cost": unl[tree][1]} if unl else None),
            "variableZoom": can, "storedAdsZoom": stored, "testValue": test, "baseFov": base,
            "entries": entries,
            "reticles": {"entries": ret.get("entries") or {}, "scope": ret.get("scope") or (sc or {}).get("png")},
            "fits": [wname[a] for a in fits.get(it.asset, [])], "fitIds": fits.get(it.asset, []),
        })
    rows.sort(key=lambda r: (r["entries"][0]["magnification"] or 0, r["name"].lower()))
    return {"meta": {"generator": "python -I _tools/sight_tables.py --write", "baseFov": BASE_FOV, "independentFov": INDEPENDENT_FOV,
                     "testLimit": TEST_LIMIT, "rule": "ADS FOV = base / magnification; base = Field of view setting (default 90), "
                     "or 72 when the sight's test value is 3.25 or more; apparent zoom = tan(45) / tan(ADS FOV / 2)",
                     "evidence": [EVID + "round46-a.md", EVID + "round79-sight-zoom.md"]},
            "sights": rows, "weapons": {w.asset: wname[w.asset] for w in weapons}}


# --- rendering ----------------------------------------------------------------------------------

def img(path, alt, w=72):
    return "![" + alt + "]({{ '/" + path + "' | relative_url }}){: width=\"" + str(w) + "\" }"


def fov_text(e):
    if "adsFov" not in e:
        return "none"
    a, b = e["adsFov"], e["apparent"]
    if a[0] == a[1]:
        return f"{g(a[0])}° ({g(b[0])}x)"
    return f"{g(a[0])}° to {g(a[1])}° ({g(b[0])}x to {g(b[1])}x)"


def mag_text(e):
    if not e["magnification"]:
        return "none"
    lo, hi = e["zoomRange"]
    return f"{g(lo)}x" if lo == hi else f"{g(lo)}x to {g(hi)}x"


def unlock_text(r):
    u = r["unlock"]
    if not u:
        return "no class gate", ""
    who = "Wardog level" if u["tree"] == "Wardog" else f"{u['tree']} level"
    return f"{who} {u['level']}", f"{u['cost']:,}" if u["cost"] else "free"


def block_main(d):
    out = ["| | Sight | Magnification | ADS FOV (apparent zoom) | ADS time | Zeroing range (m) | Sight entries | Shop price | Unlock | Unlock cost | Id |",
           "|---|---|---:|---|---|---|---|---:|---|---:|---|"]
    for r in d["sights"]:
        e = r["entries"][0]
        extra = []
        for x in r["entries"][1:]:
            extra.append(f"{x['name']} ({mag_text(x)}, ADS FOV {fov_text(x)}, ADS time {x['aimTime']})")
        ents = "; ".join([f"{x['name']}" for x in r["entries"][:1]] + extra) if extra else e["name"]
        lvl, cost = unlock_text(r)
        icon = img(r["icon"], r["name"], 48) if r["icon"] else ""
        out.append("| " + " | ".join([
            icon, r["name"], mag_text(e), fov_text(e), e["aimTime"], zeroing_text(e["zeroing"]["min"], e["zeroing"]["max"]),
            ents, f"{r['price']:,}" if r["price"] else "not in shop", lvl, cost, f"`{r['id']}`"]) + " |")
    return "\n".join(out)


def block_fits(d):
    by_w = {}
    for r in d["sights"]:
        for a in r["fitIds"]:
            by_w.setdefault(a, []).append(r["name"])
    out = ["| Weapon | Sights | Sights that fit |", "|---|---:|---|"]
    for a, name in sorted(d["weapons"].items(), key=lambda kv: kv[1].lower()):
        names = by_w.get(a, [])
        out.append(f"| {name} | {len(names)} | {', '.join(sorted(names, key=str.lower)) or 'none'} |")
    nofit = [r["name"] for r in d["sights"] if not r["fitIds"]]
    return "\n".join(out) + ("\n\nFit no weapon: " + ", ".join(nofit) + "." if nofit else "")


def block_reticles(d):
    out = ["| Sight | Reticle | Image |", "|---|---|---|"]
    for r in d["sights"]:
        for k, p in r["reticles"]["entries"].items():
            out.append(f"| {r['name']} | {ENTRY_NAMES.get(k, k)} (HUD reticle) | {img(p, r['name'] + ' reticle', 96)} |")
        if r["reticles"]["scope"]:
            out.append(f"| {r['name']} | Scope view overlay | {img(r['reticles']['scope'], r['name'] + ' scope view', 96)} |")
    return "\n".join(out)


BLOCKS = {"main": block_main, "fits": block_fits, "reticles": block_reticles}


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def read(path):
    try:
        with open(path, encoding="utf-8", newline="") as f:
            return f.read()
    except FileNotFoundError:
        return None


def render(page, d):
    return BLOCK.sub(lambda m: f"<!-- sight_tables {m.group(1)} -->\n{BLOCKS[m.group(1)](d)}\n<!-- /sight_tables -->", page)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mode", nargs="?", choices=sorted(BLOCKS))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    d = collect()
    if a.mode:
        print(BLOCKS[a.mode](d))
        return 0
    page = read(PAGE)
    new_page = render(page, d) if page is not None else None
    new_json = dump(d)
    if a.write:
        for path, text in ((OUT, new_json), (PAGE, new_page)):
            if text is not None and read(path) != text:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
                print("wrote", os.path.relpath(path, ROOT))
        return 0
    if a.check:
        stale = [os.path.relpath(p, ROOT) for p, t in ((OUT, new_json), (PAGE, new_page)) if t is None or read(p) != t]
        if stale:
            print("stale:", ", ".join(stale))
            return 1
        print("sight_tables: up to date")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
