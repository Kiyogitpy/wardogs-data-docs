#!/usr/bin/env python3
"""Round 36 combat: print the values behind docs/evidence/round36-combat.md from the exported data.

Reads only files under data/ and assets/data/ in this repository. Nothing is written.

  python -I _tools/round36_combat.py            print all sections
  python -I _tools/round36_combat.py --check    assert the key values (exit 1 on mismatch)

Sections: fob (Refuel and Repair Station restock table), canister (Fuel Canister rate),
multiplier (RepairSpeedMultiplier against Cost), hits (derived hits to destroy a structure),
stationary (restock and reload fields of the stationary weapons), health (buildable health
against vehicle health), flares (per-vehicle flare settings), ghillie (Ghillie effect),
mortar (reticle label offset, pitch limits, minimum range).
"""
import glob
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GF = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures")
BUILD = os.path.join(GF, "Items", "Buildables", "Content", "Data")


def load(path):
    """Load one exported asset (several JSON objects, the first with the properties)."""
    text = open(path, encoding="utf-8").read()
    dec = json.JSONDecoder()
    out = []
    i = 0
    while True:
        j = text.find("{", i)
        if j < 0:
            break
        try:
            obj, k = dec.raw_decode(text[j:])
        except ValueError:
            break
        out.append(obj)
        i = j + k
    return out


def props(path, typ=None):
    for o in load(path):
        if isinstance(o, dict) and "Properties" in o and (typ is None or o.get("Type") == typ):
            return o["Properties"]
    return None


def fob():
    p = props(os.path.join(BUILD, "UI", "FobRefuelRepair", "DA_Scene_FobRefuelRepair.json"))
    rows = []
    for st in p["StationData"]:
        v = st["Value"]
        for sp in v["RestockData"]:
            r = sp["Value"]
            rows.append((st["Key"]["TagName"], sp["Key"].split("::")[-1], v["MatchingResource"]["TagName"],
                         v["ItemCostPerSingleRestock"], r["MaxAmount"], r["Cost"], r["RestockTime"]))
    return rows


def canister():
    out = {}
    for name in ("ID_FuelCan_40L", "ID_FuelCan_20L"):
        text = open(os.path.join(GF, "Items", "FuelCanister", "Content", "Data", name + ".json"), encoding="utf-8").read()
        m = re.search(r'"ContainerData":\s*\{([^}]*)\}', text)
        out[name] = {k: float(v) for k, v in re.findall(r'"(\w+)":\s*([\d.]+)', m.group(1))}
    return out


def buildables():
    rows = {}
    for f in glob.glob(os.path.join(GF, "**", "DA_Buildable_*.json"), recursive=True):
        if f.endswith("_Stages.json"):
            continue
        p = props(f, "WDBuildableDataAsset")
        if p and "RepairSpeedMultiplier" in p:
            rows[os.path.basename(f)[len("DA_Buildable_"):-5]] = p
    return rows


def multiplier():
    out = []
    for n, p in sorted(buildables().items()):
        c = p.get("Cost", 0)
        out.append((n, c, p["RepairSpeedMultiplier"], round(c / 15.0, 2) if c else None))
    return out


def hits():
    """Derived hits to destroy: ceil(MaxHealth / (base * (1 + pct/100))), point blank, no falloff."""
    text = open(os.path.join(ROOT, "game-features", "Wardogs_Buildables_v1.md"), encoding="utf-8").read()
    i = text.find("<!-- buildable_tables damage -->")
    j = text.find("<!-- /buildable_tables -->", i)
    srcs = [("M4 5.56 FMJ", 28, 1), ("M67 frag", 100, 2), ("120 mm rocket", 150, 3), ("C4", 250, 4)]
    rows = []
    for line in text[i:j].split("\n")[3:]:
        c = [x.strip() for x in line.split("|")]
        if len(c) < 9:
            continue
        m = re.search(r"`DA_Buildable_([^`]+)`", c[1])
        if not m:
            continue
        hp = float(c[2].replace(",", ""))
        pct = c[5:11]
        row = [m.group(1), hp]
        for _, base, k in srcs:
            if pct[k] == "-":
                row.append(None)
                continue
            f = 1 + float(pct[k].replace("%", "")) / 100.0
            row.append(math.ceil(hp / (base * f)) if f > 0 else None)
        rows.append(row)
    return [s[0] for s in srcs], rows


def stationary():
    out = []
    for s in ("STN_01", "STN_02", "STN_03", "STN_05", "STN_06"):
        for f in glob.glob(os.path.join(GF, "Vehicles", s, "**", "WE_*.json"), recursive=True):
            t = open(f, encoding="utf-8").read()
            g = lambda k: (re.search(r'"%s":\s*("?[^,\n]+)' % k, t) or [None, None])[1]
            out.append((s, g("ReloadTime"), g("StartDelayTime"), g("EndDelayTime"), g("RestockSuppliesNeeded"),
                        g("_aaabbaggelnmdnpaealoj"), g("ResultingAmmoAmount"),
                        (re.search(r'"RestockSuppliesTag":\s*\{\s*"TagName":\s*"([^"]+)"', t) or [None, None])[1]))
    return out


def health():
    out = []
    for s in ("STN_01", "STN_02", "STN_03", "STN_04", "STN_05", "STN_06"):
        gs = glob.glob(os.path.join(GF, "Vehicles", s, "**", "DA_GameplaySystems_%s.json" % s), recursive=True)
        v = re.search(r'"InitialVehicleHealth":\s*([\d.]+)', open(gs[0], encoding="utf-8").read()).group(1) if gs else None
        b = None
        for f in glob.glob(os.path.join(GF, "Vehicles", s, "**", "DA_Buildable_*.json"), recursive=True):
            if "Stages" in f or "Radial" in f:
                continue
            m = re.search(r'"MaxHealth":\s*([\d.]+)', open(f, encoding="utf-8").read())
            b = m.group(1) if m else b
        out.append((s, v, b))
    return out


def flares():
    out = []
    for f in glob.glob(os.path.join(ROOT, "data", "**", "*GameplaySystems*.json"), recursive=True):
        t = open(f, encoding="utf-8").read()
        i = t.find('"FlaresSettings"')
        if i < 0:
            continue
        blk = t[i:i + 2500]
        v = {k: (re.search(r'"%s":\s*([\d.]+)' % k, blk) or [None, None])[1]
             for k in ("StartingFlaresAmount", "FlaresActiveTime", "FlaresEffectiveRangeMin", "FlaresEffectiveRangeMax")}
        out.append((os.path.basename(f), v))
    return sorted(out)


def ghillie():
    d = json.load(open(os.path.join(ROOT, "assets", "data", "ge-values.json"), encoding="utf-8"))
    for e in d["effects"]:
        if e["name"] == "GE_Player_GhilliEffects":
            return [(m["attribute"].split(".")[-1], m["op"], m["value"]) for m in e["modifiers"]], e["application_requirements"]


def mortar():
    p = props(os.path.join(GF, "Vehicles", "STN_03", "Content", "Weapons", "WeaponExtensions", "WE_STN_03_Heavy_MainBarrel.json"))
    tbl = [(r["Milliradians"], r["ImpactDistance"], r["TravelTime"]) for r in p["ArtilleryRangeData"]]
    t = open(os.path.join(GF, "Vehicles", "STN_03", "Content", "Weapons", "W_STN_03_MainBarrel.json"), encoding="utf-8").read()
    lo = float(re.search(r'"MinWeaponPitchAngle":\s*([-\d.]+)', t).group(1))
    hi = float(re.search(r'"MaxWeaponPitchAngle":\s*([-\d.]+)', t).group(1))
    hi_mrad = math.radians(hi) * 1000
    # linear interpolation between the neighbouring table rows (the HUD's pointer interpolates the same way)
    d = None
    for a, b in zip(tbl, tbl[1:]):
        if a[0] <= hi_mrad <= b[0]:
            d = a[1] + (b[1] - a[1]) * (hi_mrad - a[0]) / (b[0] - a[0])
    return tbl, lo, hi, math.radians(lo) * 1000, hi_mrad, d


def main():
    check = "--check" in sys.argv
    f = fob()
    print("## fob")
    for r in f:
        print("  ", r)
    c = canister()
    print("## canister", c)
    m = multiplier()
    print("## multiplier (name, Cost, RepairSpeedMultiplier, Cost/15)")
    for r in m:
        print("  ", r)
    names, hrows = hits()
    print("## hits", names)
    for r in hrows:
        print("  ", r)
    print("## stationary")
    for r in stationary():
        print("  ", r)
    h = health()
    print("## health (stn, vehicle InitialVehicleHealth, buildable MaxHealth)", h)
    print("## flares")
    for r in flares():
        print("  ", r)
    g = ghillie()
    print("## ghillie", g)
    tbl, lo, hi, lo_m, hi_m, d = mortar()
    print("## mortar pitch limits deg", lo, hi, "mrad", round(lo_m, 1), round(hi_m, 1), "interpolated range at max pitch m", round(d, 1))
    print("   label = table mrad + 650: 200 mrad ->", 200 + 650, "mils at", dict((a, b) for a, b, _ in tbl)[200.0], "m")
    if check:
        assert ("Buildable.RefuelStation", "Fast", "Id.Item.FuelSupplies", 5, 0.05, 75, 3.0) in f
        assert ("Buildable.RepairStation", "Max", "Id.Item.SparePartsSupplies", 5, 1.0, 2000, 9.0) in f
        assert c["ID_FuelCan_40L"]["UpdateAmount"] == 2.0 and c["ID_FuelCan_40L"]["UpdateTime"] == 0.75
        assert any(r[0] == "RefuelStation" and r[2] == 13.33 and r[3] == 13.33 for r in m)
        assert dict((s, (v, b)) for s, v, b in h)["STN_06"] == ("1800.0", "3000.0")
        assert abs(hi_m - 261.8) < 0.1 and 102 < d < 104
        print("ok")


if __name__ == "__main__":
    main()
