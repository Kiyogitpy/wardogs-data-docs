"""Recoil (spray) patterns for every weapon in Season 1 and Season 2, rebuilt from the data exports.

Writes assets/data/spray-patterns.json, one entry per WDWeaponStatsData asset (the same 61 weapons as
assets/data/weapon-spread-recoil.json), with the per-shot kick vectors, the expected cumulative path, a
seeded Monte Carlo spread band, the final default-attachment recoil multipliers and the in-game name.

    python -I _tools/spray_patterns.py --write            # regenerate assets/data/spray-patterns.json
    python -I _tools/spray_patterns.py --check            # recompute, exit 1 if the committed file differs
    python -I _tools/spray_patterns.py --s1 DIR           # other Season 1 data/ folder (default below)
    python -I _tools/spray_patterns.py --print A91        # one weapon, human readable

Semantics: content/Wardogs_Weapons_v2.md section 5a (kick function 0x6B95C50). Shot n inside the pattern kicks
RecoilPattern[n] turned by a uniform random angle in +-RandomDeviationDegree; past the pattern (and on every shot
of a weapon without one) yaw and pitch are uniform draws in the PostPattern ranges. X is yaw (right +), Y is pitch
(up +), degrees. Omitted stats fields take the FWDWeaponStats constructor defaults (0x699E6C0, see recoil_table.py).
expectedPath and band are the sums of the authored kicks only: the horizontal/vertical multipliers, the stance
multiplier, the focus cut and ViewKickMagnitudeMultiplier are listed beside them for the viewer to apply, and the
ViewKickCurve time shape is not applied. Firearms have no self recovery (section 5a), so nothing is subtracted.

Seasons. Season 2 is this repo's data/. Season 1 is the pre-update export (see season_diff.py; default
S1_DEFAULT). Both are read by the same code. The multipliers use the effect formulas in assets/data/ge-values.json
(Season 2 effect values) on each season's own item data, so a Season 1 multiplier difference comes from item
changes only. The Season 1 weapon whose id changed (Mosin -> WEPN_017) is paired by its WeaponId tag.

Names. The display name is the item's DisplayName (BHInventoryItemDefinition); vehicle weapons use
WeaponExtensionName of the vehicle weapon extension that links their stats. A weapon with neither is marked
nameSource "none" with a labelled fallback.
"""
import collections
import glob
import json
import math
import os
import random
import re
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recoil_table  # noqa: E402
import weapon_attributes as wa  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "spray-patterns.json")
S1_DEFAULT = "E:/r22/s1/data"
RUNS = 2000
MIN_SHOTS = 40
EXPORT = re.compile(r"^--- export:.*---\s*$", re.M)
DEFAULTS = recoil_table.DEFAULTS
DEFAULT_RPM = 600.0  # FWDWeaponStats ctor: RoundsPerMinute +0x138 (Weapons game-feature page, class defaults)
STANCES = ("Stand", "Crouch", "Prone")
CLASS_BY_ARCHETYPE = {"AR": "AR", "DMR": "DMR", "LMG": "LMG", "SMG": "SMG", "Sniper": "Sniper", "Shotgun": "Shotgun",
                      "Pistol": "Pistol", "Launcher": "Launcher", "Bow": "Bow"}
ATTR = "Attribute.Gameplay.Weapon."


def exports(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        parts = EXPORT.split(f.read())
    out = []
    for p in parts:
        if p.strip():
            try:
                out.append(json.loads(p))
            except ValueError:
                pass
    return out


def rel(path, base):
    return os.path.relpath(path, base).replace(os.sep, "/")


# --------------------------------------------------------------------------- one season's data
class Season:
    def __init__(self, data_dir):
        self.dir = data_dir
        self.stats = {}   # asset -> dict(path, props, tag)
        for p in sorted(glob.glob(os.path.join(data_dir, "**", "DA_*_Stats.json"), recursive=True)):
            for o in exports(p):
                if o.get("Type") == "WDWeaponStatsData":
                    props = o.get("Properties", {})
                    self.stats[o["Name"]] = {"path": rel(p, os.path.dirname(data_dir)), "props": props,
                                             "tag": ((props.get("WeaponId") or {}).get("TagName") or "")}
        self.items_by_stats = collections.defaultdict(list)   # stats asset -> [ID_ item objects]
        self.items_by_tag = {}                                  # ItemId lower -> item
        self.vehicle_ext = collections.defaultdict(list)      # stats asset -> [(extension tag, WeaponExtensionName, folder)]
        ref = re.compile(r"WDWeaponStatsData'(DA_\w+_Stats)'")
        for p in sorted(glob.glob(os.path.join(data_dir, "**", "*.json"), recursive=True)):
            base = os.path.basename(p)
            if not (base.startswith("ID_") or base.startswith("WE_") or base == "GrenadeLauncher.json"):
                continue
            with open(p, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            objs = [json.loads(x) for x in EXPORT.split(text) if x.strip()]
            for o in objs:
                if o.get("Type") == "BHInventoryItemDefinition":
                    pr = o.get("Properties", {})
                    disp = pr.get("DisplayName") or {}
                    name = disp.get("LocalizedString") or disp.get("SourceString") or ""
                    item = {"asset": o["Name"], "id": (pr.get("ItemId") or {}).get("TagName", ""), "name": name,
                            "path": rel(p, os.path.dirname(data_dir)), "ctx": list(pr.get("ItemContext", [])), "obj": objs}
                    self.items_by_tag[item["id"].lower()] = item
                    for r in set(ref.findall(text)):
                        self.items_by_stats[r].append(item)
                elif o.get("Type") == "WDVehicleWeaponExtensionDataAsset":
                    pr = o.get("Properties", {})
                    folder = re.search(r"/Vehicles/([^/]+)/", rel(p, os.path.dirname(data_dir)))
                    rec = ((pr.get("WeaponExtensionTag") or {}).get("TagName", ""), pr.get("WeaponExtensionName"),
                           folder.group(1) if folder else "")
                    for r in set(ref.findall(text)):
                        if rec not in self.vehicle_ext[r]:
                            self.vehicle_ext[r].append(rec)
        self.ui_name = {}        # tag lower -> FriendlyName (BHEntityData_UI rows)
        self.vehicle_name = {}   # Vehicles/<folder> -> default variant name
        for p in sorted(glob.glob(os.path.join(data_dir, "**", "DT_EntityData_UI*.json"), recursive=True)):
            folder = re.search(r"/Vehicles/([^/]+)/", rel(p, os.path.dirname(data_dir)))
            for o in exports(p):
                for key, row in (o.get("Rows") or {}).items():
                    fn = row.get("FriendlyName") or {}
                    nm = fn.get("LocalizedString") or fn.get("SourceString") or fn.get("CultureInvariantString")
                    if nm:
                        self.ui_name[key.lower()] = nm
                        if folder and key.startswith("Vehicle.Variant.") and folder.group(1) not in self.vehicle_name:
                            self.vehicle_name[folder.group(1)] = re.sub(r" \[.*\]$", "", nm)
        self.vendor_type = {}   # ItemId lower -> Weapon.Type.X
        for p in glob.glob(os.path.join(data_dir, "**", "DT_*Vendor*.json"), recursive=True):
            for o in exports(p):
                for row in (o.get("Rows") or {}).values():
                    for var in row.get("VendorItemVariations", []) or []:
                        tag = (var.get("VariationTag") or {}).get("TagName")
                        for sc in var.get("Subcategories", []) or []:
                            m = re.search(r"Weapon\.Type\.\w+", sc)
                            if tag and m:
                                self.vendor_type.setdefault(tag.lower(), m.group(0))
        self.attr = None

    def attributes(self):
        """weapon_attributes.Data over this season's items (effects: assets/data/ge-values.json)."""
        if self.attr is None:
            d = wa.Data.__new__(wa.Data)
            with open(wa.SRC, encoding="utf-8") as f:
                d.effects = {e["name"]: e for e in json.load(f)["effects"]}
            d.items = {}
            # Item.path is made relative to wa.ROOT, which must share a drive with the folder
            saved, wa.ROOT = wa.ROOT, os.path.dirname(self.dir)
            legacy = os.path.abspath(self.dir) != os.path.join(ROOT, "data")
            keys = (wa.BIPOD_WEAPON, wa.BIPOD_CHARACTER)
            if legacy:   # Season 1 export: the two hashed bipod keys carry their pre-v2-usmap names
                wa.BIPOD_WEAPON = "_aaabgocclgplfdmmfjefm_$E22B6FB53CC5945C$_$22$"
                wa.BIPOD_CHARACTER = "_aaabpgfgnkcdbhhlgdhmb_$656DA23177B637C1$_$31$"
            for p in sorted(glob.glob(os.path.join(self.dir, "**", "ID_*.json"), recursive=True)):
                objs = exports(p)
                if any(o.get("Type") == "BHInventoryItemDefinition" for o in objs):
                    it = wa.Item(p, objs)
                    d.items[it.key] = it
            wa.ROOT = saved
            wa.BIPOD_WEAPON, wa.BIPOD_CHARACTER = keys
            d.by_asset = {it.asset.lower(): it for it in d.items.values()}
            d.weapons = sorted((it for it in d.items.values() if it.ranged and it.base and not wa.SKIP.search(it.path)),
                               key=lambda it: (it.archetype, it.display.lower(), it.asset))
            d.attachments = []
            self.attr = d
        return self.attr


def stats_id(asset):
    return asset[3:-len("_Stats")]


def pair_assets(s1, s2):
    """S2 asset -> S1 asset (same name, else same unique WeaponId tag among the leftovers)."""
    pairs = {a: a for a in s2.stats if a in s1.stats}
    left1 = [a for a in s1.stats if a not in pairs.values()]
    left2 = [a for a in s2.stats if a not in pairs]
    for a in left2:
        tag = s2.stats[a]["tag"]
        if not tag:
            continue
        c1 = [b for b in left1 if s1.stats[b]["tag"] == tag]
        c2 = [b for b in left2 if s2.stats[b]["tag"] == tag]
        if len(c1) == 1 and len(c2) == 1:
            pairs[a] = c1[0]
    return pairs


# --------------------------------------------------------------------------- names, categories
def resolve_item(season, asset, st):
    """The item for a stats asset: one that links it (not an attachment grant), else the item whose id is WeaponId."""
    tag = st["tag"].lower()
    cands = season.items_by_stats.get(asset, [])
    if len(cands) == 1:
        return cands[0]
    own = [c for c in cands if c["id"].lower() == tag]
    if own:
        return own[0]
    return season.items_by_tag.get(tag) if tag else None


def info(season, asset):
    """Name, nameSource, category, class, type for one stats asset of a season."""
    st = season.stats[asset]
    ident = stats_id(asset)
    path = st["path"]
    item = resolve_item(season, asset, st)
    ext = season.vehicle_ext.get(asset, [])
    vehicle = bool(re.search(r"/Vehicles/|VehicleWeaponry", path)) or (not item and bool(ext))
    ui = season.ui_name.get((item["id"] if item else st["tag"]).lower()) if (item or st["tag"]) else None
    veh_names = []
    for tag, nm, folder in ext:
        wn = season.ui_name.get(tag.lower()) or nm
        vn = season.vehicle_name.get(folder)
        label = f"{wn} ({vn})" if wn and vn and vn.lower() not in wn.lower() else wn
        if label and label not in veh_names:
            veh_names.append(label)
    if item and item["name"]:
        name, source = item["name"], "item.DisplayName"
    elif ui:
        name, source = ui, "BHEntityData_UI.FriendlyName"
    elif veh_names:
        name, source = " / ".join(veh_names), "vehicle weapon extension (UI FriendlyName / WeaponExtensionName)"
    else:
        name, source = f"Unnamed ({ident})", "none"
    if vehicle and veh_names:
        name, source = " / ".join(veh_names), "vehicle weapon extension (UI FriendlyName / WeaponExtensionName)"
    if "Stationary" in path:
        cat = "stationary"
    elif vehicle:
        cat = "vehicle"
    elif re.search(r"BarrelTest|Gunsmith", path) or name.upper().startswith("TEST"):
        cat = "test"
    elif re.search(r"BuildTool|Fists", path):
        cat = "tool"
    elif item is None:
        cat = "test"   # a stats asset no item in the export links to
    else:
        cat = "infantry"
    arch = next((t.split(".", 2)[2] for t in (item["ctx"] if item else []) if t.startswith("Item.Archetype.")), None)
    dmg = None
    if item:
        for o in item["obj"]:
            m = re.search(r"Meta\.Damage\.Weapon\.(\w+)\.", json.dumps(o.get("Properties", {})))
            if m:
                dmg = m.group(1)
                break
    cls = dmg or CLASS_BY_ARCHETYPE.get(arch or "", None) or {"vehicle": "Vehicle", "stationary": "Stationary"}.get(cat, "Other")
    if cls == "Other" and re.search(r"Launcher", path):
        cls = "Launcher"
    typ = season.vendor_type.get(item["id"].lower()) if item else None
    return {"name": name, "nameSource": source, "category": cat, "class": cls, "type": typ,
            "item": item["asset"] if item else None, "path": path}


# --------------------------------------------------------------------------- the numbers
def keys_of(curve):
    return (curve or {}).get("EditorCurveData", {}).get("Keys", [])


def get(ws, key):
    return ws[key] if key in ws else DEFAULTS[key]


def multipliers(season, item_id):
    """Final default-attachment vertical/horizontal recoil multiplier (standing) and the stance ratios."""
    one = {"horizontal": 1.0, "vertical": 1.0, "stance": {"stand": 1.0, "crouch": 1.0, "prone": 1.0}}
    if not item_id:
        return one, "no item: 1"
    data = season.attributes()
    w = data.by_asset.get(item_id.lower()) or data.items.get(item_id.lower())
    if w is None or w not in data.weapons:
        return one, "item has no DefaultAttributes: 1"
    vals = {}
    for stance in STANCES:
        _, _, _, attrs, _ = wa.compute(data, w, stance=stance)
        vals[stance] = {k: (attrs[ATTR + k]["final"] if ATTR + k in attrs else None)
                        for k in ("VerticalRecoilMultiplier", "HorizontalRecoilMultiplier")}
    v0 = vals["Stand"]["VerticalRecoilMultiplier"]
    h0 = vals["Stand"]["HorizontalRecoilMultiplier"]
    v0 = 1.0 if v0 is None else v0
    h0 = 1.0 if h0 is None else h0
    st = {"stand": 1.0}
    for s in ("Crouch", "Prone"):
        v = vals[s]["VerticalRecoilMultiplier"]
        st[s.lower()] = round(v / v0, 6) if v is not None and v0 else 1.0
    return {"horizontal": r6(h0), "vertical": r6(v0), "stance": st}, "weapon_attributes final value, default loadout"


def r6(x):
    return round(float(x), 6)


def r5(x):
    return round(float(x), 5)


def simulate(pattern, dev, yaw, pitch, n, seed):
    """Expected cumulative path and the per-shot 10th/90th percentile of the cumulative position."""
    mean_x, mean_y = (yaw[0] + yaw[1]) / 2.0, (pitch[0] + pitch[1]) / 2.0
    path, cx, cy = [], 0.0, 0.0
    for i in range(n):
        if i < len(pattern):
            cx, cy = cx + pattern[i]["x"], cy + pattern[i]["y"]
        else:
            cx, cy = cx + mean_x, cy + mean_y
        path.append({"shot": i + 1, "x": r5(cx), "y": r5(cy)})
    rng = random.Random(seed)
    xs = [[] for _ in range(n)]
    ys = [[] for _ in range(n)]
    for _ in range(RUNS):
        cx = cy = 0.0
        for i in range(n):
            if i < len(pattern):
                a = math.radians(rng.uniform(-dev, dev))
                kx, ky = pattern[i]["x"], pattern[i]["y"]
                cx += kx * math.cos(a) - ky * math.sin(a)
                cy += kx * math.sin(a) + ky * math.cos(a)
            else:
                cx += rng.uniform(yaw[0], yaw[1])
                cy += rng.uniform(pitch[0], pitch[1])
            xs[i].append(cx)
            ys[i].append(cy)

    def q(vals, p):
        vals.sort()
        k = p * (len(vals) - 1)
        lo = int(math.floor(k))
        hi = min(lo + 1, len(vals) - 1)
        return vals[lo] + (vals[hi] - vals[lo]) * (k - lo)

    band = {"p10": [{"shot": i + 1, "x": r5(q(xs[i], 0.10)), "y": r5(q(ys[i], 0.10))} for i in range(n)],
            "p90": [{"shot": i + 1, "x": r5(q(xs[i], 0.90)), "y": r5(q(ys[i], 0.90))} for i in range(n)]}
    return path, band


def season_entry(season, asset, wid, inf):
    st = season.stats[asset]
    ws = st["props"].get("WeaponStats", {})
    pattern = [{"x": p["X"], "y": p["Y"]} for p in (ws.get("RecoilPattern") or [])]
    yaw = get(ws, "PostPatternRandomYawRecoil")
    pitch = get(ws, "PostPatternRandomPitchRecoil")
    dev = float(get(ws, "RandomDeviationDegree"))
    keys = keys_of(ws.get("ViewKickCurve"))
    rpm = ws.get("RoundsPerMinute")
    mult, mnote = multipliers(season, inf["item"])
    n = max(len(pattern), MIN_SHOTS)
    path, band = simulate(pattern, dev, [yaw["X"], yaw["Y"]], [pitch["X"], pitch["Y"]], n,
                          zlib.crc32(f"{wid}|{asset}".encode()))
    defaulted = [k for k in ("RandomDeviationDegree", "RecoilPatternResetTime", "PostPatternRandomYawRecoil",
                             "PostPatternRandomPitchRecoil", "ViewKickMagnitudeMultiplier",
                             "RecoilReductionWhenFocussing") if k not in ws]
    if rpm is None:
        defaulted.append("RoundsPerMinute")
    note = f"{st['path']}"
    if defaulted:
        note += "; native defaults (FWDWeaponStats ctor) for: " + ", ".join(defaulted)
    note += "; multipliers: " + mnote
    return {
        "present": True,
        "rpm": float(rpm) if rpm is not None else DEFAULT_RPM,
        "rpmSource": "asset" if rpm is not None else "native default 600 (asset omits it)",
        "recoilPatternResetTime_s": float(get(ws, "RecoilPatternResetTime")),
        "randomDeviationDeg": dev,
        "pattern": pattern,
        "postPattern": {"yaw": [yaw["X"], yaw["Y"]], "pitch": [pitch["X"], pitch["Y"]]},
        "viewKick": {"durationS": max([k["Time"] for k in keys], default=0.0),
                     "curveKeys": [{"time": k["Time"], "value": k["Value"], "interp": k.get("InterpMode"),
                                    "arriveTangent": k.get("ArriveTangent"), "leaveTangent": k.get("LeaveTangent")}
                                   for k in keys]},
        "multipliers": mult,
        "focusReductionPct": float(get(ws, "RecoilReductionWhenFocussing")),
        "viewKickMagnitudeMultiplier": float(get(ws, "ViewKickMagnitudeMultiplier")),
        "expectedPath": path,
        "band": band,
        "sourceNote": note,
    }


COMPARE = ("rpm", "recoilPatternResetTime_s", "randomDeviationDeg", "pattern", "postPattern", "viewKick",
           "multipliers", "focusReductionPct", "viewKickMagnitudeMultiplier")


def changes(a, b):
    return [k for k in COMPARE if a[k] != b[k]]


def build(s1_dir):
    s2 = Season(os.path.join(ROOT, "data"))
    s1 = Season(s1_dir) if s1_dir and os.path.isdir(s1_dir) else None
    pairs = pair_assets(s1, s2) if s1 else {}
    s1_used = set(pairs.values())
    weapons = []
    for asset in sorted(s2.stats, key=lambda a: stats_id(a).lower()):
        wid = stats_id(asset)
        inf = info(s2, asset)
        e2 = season_entry(s2, asset, wid, inf)
        e1 = None
        if s1 and asset in pairs:
            a1 = pairs[asset]
            e1 = season_entry(s1, a1, wid, info(s1, a1))
            e1["asset"] = a1
        w = {"id": wid, "name": inf["name"], "nameSource": inf["nameSource"], "category": inf["category"],
             "class": inf["class"], "type": inf["type"], "statsAsset": asset, "itemAsset": inf["item"],
             "seasons": {"s2": e2, "s1": e1}}
        w["changedS1toS2"] = changes(e1, e2) if e1 else None
        weapons.append(w)
    if s1:   # weapons only in Season 1
        for a1 in sorted(s1.stats):
            if a1 in s1_used:
                continue
            wid = stats_id(a1)
            inf = info(s1, a1)
            e1 = season_entry(s1, a1, wid, inf)
            e1["asset"] = a1
            weapons.append({"id": wid, "name": inf["name"], "nameSource": inf["nameSource"], "category": inf["category"],
                            "class": inf["class"], "type": inf["type"], "statsAsset": a1, "itemAsset": inf["item"],
                            "seasons": {"s2": {"present": False}, "s1": e1}, "changedS1toS2": None})
    meta = {
        "generator": "python -I _tools/spray_patterns.py --write",
        "seasons": {"s1": "Season 1: pre-update export (see season_diff.py)",
                    "s2": "Season 2: build ++Wardogs+Live-CL-516586, this repo's data/"},
        "units": "degrees of view rotation; x = yaw (right +), y = pitch (up +)",
        "monteCarlo": {"runs": RUNS, "seed": "crc32(id|statsAsset)", "band": "per-shot 10th and 90th percentile of the "
                       "cumulative x and y independently (linear interpolation)"},
        "notes": [
            "pattern is RecoilPattern[n] as authored; shot n turns it by a uniform random angle in +-randomDeviationDeg; "
            "past the pattern (and for every shot of a weapon without one) yaw and pitch are uniform draws in postPattern "
            "(Weapons v2 section 5a, 0x6B95C50).",
            "expectedPath and band sum the authored kicks for max(pattern length, 40) shots with no recovery (firearms "
            "have no self recovery); after the pattern the mean of the post-pattern ranges is used for the path.",
            "multipliers.horizontal/vertical are the standing default-loadout Attribute.Gameplay.Weapon.*RecoilMultiplier "
            "values, stance.crouch/prone the vertical ratio to standing; the viewer applies them with "
            "viewKickMagnitudeMultiplier and focusReductionPct; paths and bands are not scaled by them.",
            "Season 1 multipliers use the Season 2 effect values (assets/data/ge-values.json) on Season 1 item data.",
            "rpm is RoundsPerMinute from the stats asset; where the asset omits it the constructor default 600 applies "
            "(rpmSource says which).",
            "category: infantry | vehicle | stationary | test (test assets and stats assets no item links) | tool "
            "(Fists, BuildTool). nameSource none marks a weapon whose in-game name is not in the exported data.",
            "changedS1toS2 lists the fields that differ between seasons (null when a season is absent); a weapon "
            "present in only one season has the other season null (s1) or present false (s2).",
        ],
    }
    return {"meta": meta, "weapons": weapons}


def dumps(obj):
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    s1 = S1_DEFAULT
    if "--s1" in args:
        s1 = args[args.index("--s1") + 1]
    if "--print" in args:
        want = args[args.index("--print") + 1].lower()
        for w in build(s1)["weapons"]:
            if w["id"].lower() == want:
                for s in ("s1", "s2"):
                    e = w["seasons"][s]
                    if e and e.get("present"):
                        print(w["id"], w["name"], s, "pattern", len(e["pattern"]), "rpm", e["rpm"], "dev", e["randomDeviationDeg"])
                        print("  path end", e["expectedPath"][-1], "mult", e["multipliers"])
        return
    if "--write" in args or "--check" in args:
        have_s1 = os.path.isdir(s1)
        data = build(s1)
        text = dumps(data)
        if "--write" in args:
            if not have_s1:
                sys.exit(f"Season 1 folder {s1} not found; pass --s1 DIR (refusing to write without Season 1)")
            with open(OUT, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(data['weapons'])} weapons")
            return
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
        if have_s1:
            ok = old == data
        else:
            strip = lambda d: [(w["id"], w["seasons"]["s2"]) for w in d["weapons"]]  # noqa: E731
            ok = strip(old) == strip(data)
            print(f"Season 1 folder {s1} not found: compared Season 2 only")
        print("spray-patterns.json is up to date" if ok else "spray-patterns.json DIFFERS; rerun with --write")
        sys.exit(0 if ok else 1)
    print(__doc__)


if __name__ == "__main__":
    main()
