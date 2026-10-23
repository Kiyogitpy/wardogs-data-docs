"""Tables for game-features/Wardogs_AmmoPacking_v1.md: the inventory ammo-packing curves, rebuilt from data/.

Reads every CurveFloat under Content/GameMechanics/Inventory/InventoryMagPacking, CR_CombineAmmoCurve, the
DA_InventoryMagPackingData asset and the magazine multiplier fields (FWDMagazineAttachmentData +0x68 / +0x6C).
Blocks sit between

    <!-- ammo_packing_tables MODE -->  ...  <!-- /ammo_packing_tables -->

    python _tools/ammo_packing_tables.py --write      # refresh every block in place
    python _tools/ammo_packing_tables.py --check      # exit 1 when a block is stale
    python _tools/ammo_packing_tables.py MODE         # print one block (counts, asset, maps, combine, loose,
                                                      #   extract, load, mags, examples)
"""
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import challenge_tables as ct  # noqa: E402

ROOT, DATA = ct.ROOT, ct.DATA
PAGE = "game-features/Wardogs_AmmoPacking_v1.md"
BLOCK = re.compile(r"<!-- ammo_packing_tables (\w+) -->\r?\n.*?<!-- /ammo_packing_tables -->", re.S)
BASE = "Wardogs/Content/GameMechanics/Inventory/"
DA = BASE + "InventoryMagPacking/DA_InventoryMagPackingData.json"
F1, F2 = "_aaabfbhbgfmafmfmaajnd", "_aaabcedhgdocfgafjkign"  # +0x6C, +0x68
SLOTS = [  # property, offset, kind
    ("_aaabllnojcfhdgeommfma", "0x30", "default curve"),
    ("_aaabimpbjloglbhgafela", "0xB8", "default curve"),
    ("_aaacacabcoegcjlfdjelm", "0x140", "default curve"),
    ("_aaaboilmcjjfcpblfgjjf", "0x1C8", "per-caliber map"),
    ("_aaablhndpcjmcdfploclj", "0x218", "per-caliber map"),
    ("_aaacdfgmjbjbcodlbnooi", "0x268", "per-caliber map"),
]
FAMILIES = [("combine", "Default combine curve", "CR_CombineAmmoCurve"), ("loose", "Combine loose ammo", "CR_CombineLooseAmmoCurve"),
            ("extract", "Extract ammo", "CR_ExtractAmmoCurve"), ("load", "Load ammo", "CR_LoadAmmoCurve")]
TITLES = {m: t for m, t, _ in FAMILIES}


def load_da():
    with open(os.path.join(DATA, DA), encoding="utf-8") as f:
        t = f.read()
    return json.loads(t[t.index("{"):])["Properties"]


def curves():
    out = {}
    for f in sorted(glob.glob(os.path.join(DATA, BASE, "**", "CR_*.json"), recursive=True)):
        e = ct.exports(f)[0]
        fc = e["Properties"]["FloatCurve"]
        out[e["Name"]] = {"rel": ct.rel_of(f), "keys": [(k["Time"], k["Value"]) for k in fc.get("Keys", [])],
                          "default": fc.get("DefaultValue"), "interp": sorted({k["InterpMode"].replace("RCIM_", "") for k in fc.get("Keys", [])})}
    return out


def family(name):
    for m, _, p in FAMILIES:
        if name.startswith(p):
            return m


def ev(keys, x):
    """Linear interpolation, constant outside the key range (the assets store RCIM_Linear keys)."""
    if x <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if x <= t1:
            return v0 + (v1 - v0) * (x - t0) / (t1 - t0)
    return keys[-1][1]


def points(keys):
    return ", ".join(f"{ct.n(t)} -> {ct.n(v)}" for t, v in keys)


def magazines():
    res = []
    for f in sorted(glob.glob(os.path.join(DATA, "**", "ID_*.json"), recursive=True)):
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        if F1 not in t:
            continue
        a = re.search(r'"%s": ([\d.]+)' % F1, t)
        b = re.search(r'"%s": ([\d.]+)' % F2, t)
        tags = sorted(set(re.findall(r'"TagName": "(Id\.Item\.[^"]*)"', t)))
        res.append({"name": os.path.basename(f)[:-5], "rel": ct.rel_of(f), "m6c": float(a.group(1)), "m68": float(b.group(1)), "tags": tags})
    return res


def asset_tab(c):
    d = load_da()
    rows = ["| Offset | Property (obfuscated) | Kind | Content |", "|---|---|---|---|"]
    for prop, off, kind in SLOTS:
        v = d[prop]
        if isinstance(v, list):
            fam = family(v[0]["Value"]["ExternalCurve"]["ObjectName"].split("'")[1])
            content = f"{len(v)} caliber-tag entries, each pointing at a per-caliber curve ({TITLES[fam].lower()} family)"
        else:
            content = f"`{v['ExternalCurve']['ObjectName'].split(chr(39))[1]}`"
        rows.append(f"| `+{off}` | `{prop}` | {kind} | {content} |")
    rows.append(f"| `+0x2C4` | `_aaaamidkofoncinfnlfeg` | int32 | {d['_aaaamidkofoncinfnlfeg']} (the only scalar stored in the asset; the bool at `+0x2B8`, the int at `+0x2BC` and the float at `+0x2C0` are at their defaults; meaning not traced) |")
    return "\n".join(rows)


def maps_tab(c):
    d = load_da()
    tags = [e["Key"]["TagName"] for e in d[SLOTS[3][0]]]
    rows = ["| Caliber tag | Extract map (`+0x1C8`) | Load map (`+0x218`) | Combine-loose map (`+0x268`) | Inline keys (all three maps) |", "|---|---|---|---|---|"]
    for i, tag in enumerate(tags):
        cells, inline = [], []
        for prop, _, _ in SLOTS[3:]:
            e = d[prop][i]
            assert e["Key"]["TagName"] == tag
            nm = e["Value"]["ExternalCurve"]["ObjectName"].split("'")[1]
            cells.append(ct.link(c[nm]["rel"]))
            k = e["Value"]["EditorCurveData"]["Keys"]
            inline.append(points([(x["Time"], x["Value"]) for x in k]) if k else "none")
        rows.append(f"| `{tag}` | {' | '.join(cells)} | {'; '.join(sorted(set(inline)))} |")
    return "\n".join(rows)


def fam_tab(c, mode):
    rows = ["| Curve | Keys (rounds -> time) | Interp | Default value |", "|---|---|---|---|"]
    for n in sorted(c):
        if family(n) == mode:
            x = c[n]
            rows.append(f"| {ct.link(x['rel'])} | {points(x['keys'])} | {', '.join(x['interp']) or '-'} | {ct.n(x['default'])} |")
    return "\n".join(rows)


def counts(c):
    k = collections.Counter(family(n) for n in c)
    rows = ["| Family | Curves |", "|---|---|"] + [f"| {t} | {k[m]} |" for m, t, _ in FAMILIES] + [f"| **Total** | **{len(c)}** |"]
    return "\n".join(rows)


def mags_tab(c):
    ms = magazines()
    odd = [m for m in ms if m["m6c"] != 1.0 or m["m68"] != 1.0]
    rows = [f"{len(ms)} magazine items carry the two fields; {len(ms) - len(odd)} hold 1.0 in both and {len(odd)} hold a lower value (the two fields are equal on every item).", "",
            "| Magazine | `+0x68` | `+0x6C` | Ammo / item tags in the export |", "|---|---|---|---|"]
    for m in odd:
        rows.append(f"| {ct.link(m['rel'])} | {ct.n(m['m68'])} | {ct.n(m['m6c'])} | {', '.join(f'`{t}`' for t in m['tags'])} |")
    return "\n".join(rows)


def examples(c):
    def K(n):
        return c[n]["keys"]
    cases = [("5.56 mm, `ID_M249_Mag_Standard` (0.6)", "556mm", 0.6, 100),
             ("5.56 mm, `ID_M249_Mag_Standard` (0.6)", "556mm", 0.6, 200),
             ("5.56 mm, `ID_556STANAG_Mag_Standard` (1.0)", "556mm", 1.0, 30),
             ("5.56 mm, `ID_MAGZ_062` (0.8)", "556mm", 0.8, 100),
             ("7.62x54 mm, `ID_LMG_02_Magazine_Standard` (0.7)", "762x54mm", 0.7, 100)]
    rows = ["| Case (multiplier) | Rounds | Load curve | Extract curve | Load x mult | Extract x mult |", "|---|---|---|---|---|---|"]
    for lab, cal, mult, r in cases:
        ld, ex = ev(K(f"CR_LoadAmmoCurve_{cal}"), r), ev(K(f"CR_ExtractAmmoCurve_{cal}"), r)
        rows.append(f"| {lab} | {r} | {ld:.2f} | {ex:.2f} | {ld * mult:.2f} | {ex * mult:.2f} |")
    comb = K("CR_CombineAmmoCurve")
    rows += ["", "Fallback combine curve `CR_CombineAmmoCurve` (used only when no caliber entry matches): "
             + ", ".join(f"{r} rounds -> {ev(comb, r):.2f}" for r in (30, 60, 100)) + "."]
    return "\n".join(rows)


MODES = {"counts": counts, "asset": asset_tab, "maps": maps_tab, "mags": mags_tab, "examples": examples}
for _m, _t, _p in FAMILIES:
    MODES[_m] = (lambda m: lambda c: fam_tab(c, m))(_m)


def regenerate(c, text):
    nl = "\r\n" if "\r\n" in text else "\n"

    def regen(m):
        body = MODES[m.group(1)](c).split("\n")
        return nl.join([f"<!-- ammo_packing_tables {m.group(1)} -->"] + body + ["<!-- /ammo_packing_tables -->"])
    return BLOCK.subn(regen, text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    c = curves()
    if "--write" in args or "--check" in args:
        path = os.path.join(ROOT, PAGE)
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
        new, count = regenerate(c, text)
        if "--check" in args:
            print(f"{PAGE}: {count} tables, {'stale' if new != text else 'current'}")
            return 1 if new != text else 0
        if new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
        print(f"{PAGE}: {count} tables {'updated' if new != text else 'unchanged'}")
        return 0
    print(MODES[next((a for a in args if a in MODES), "counts")](c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
