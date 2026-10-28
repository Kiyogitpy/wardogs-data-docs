"""Build assets/data/vehicle-spawns.json and game-features/Wardogs_VehicleSpawns_v1.md: vehicle deployment points and infantry spawn areas per map.

    python -I _tools/vehicle_spawns.py [--check] [<round42 scratch dir> [<board blueprint dump dir>]]

Inputs (read-only; absent inputs make the script exit 0 with a message):
  <round42>/sv/*.json   WdExtract dump of the 61 packages whose name map holds WDSpawnVolume
                        (the 5 world packages plus 56 World Partition cells; see docs/evidence/round42-modes-ai-other.md)
  <boards>/../sv_extra/*.json   cells that hold a board or spawn manager but no spawn volume (findname B_SpawnManager_C and
                        B_VehicleDeploymentBoard_{Lonestar,Manticore,Valkrya}_C, minus the cells already in sv)
  <boards>/*.json       WdExtract dump of the board Blueprint defaults and B_SpawnManager
                        (list prefix B_VehicleDeploymentBoard, plus Wardogs/Content/GameMechanics/Gamemode/Objects/B_SpawnManager)
and, from this repository, DefaultVehicleUtility.ini (MaxVehiclesPerPlayer).

Regenerate the dumps (see tools/cue4parse_extractor/README.md for the arguments):
  WdExtract <Paks> <key> <usmap> <out> <oo2core> findname Wardogs WDSpawnVolume    -> <out>/findname.txt
  WdExtract <Paks> <key> <usmap> <out>/sv <oo2core> dump <package list from findname.txt>
  WdExtract <Paks> <key> <usmap> <out> <oo2core> list B_VehicleDeploymentBoard     -> files.txt (add B_SpawnManager path)
  WdExtract <Paks> <key> <usmap> <out>/bd <oo2core> dump files.txt

Everything is read from cooked data. Tag-to-vehicle-name mapping and the faction-to-tag pairing are labelled
as inferred where the data does not state them. Idempotent; --check exits 1 on difference.
"""
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "vehicle-spawns.json")
INI = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Vehicles", "VehicleUtility", "Config",
                   "DefaultVehicleUtility.ini")

# Native constructor defaults of AWDVehicleDeploymentBoard (constructor RVA 0x7708A00, static disassembly of the restored
# executable, round 53; docs/evidence/round53-spawn-board-defaults.md). Fields the Blueprint does not set keep these values.
# (field, offset, native default, unit, Blueprint override or None). The constructor is plain code, not behind the protection layer.
BOARD_NATIVE = [
    ("VehicleHealthThreshold", 0x3F8, 0.3, "fraction of health", None),
    ("RadarRestoreHealthThreshold", 0x3FC, 0.5, "fraction of health", 0.55),
    ("VehicleSpeedThreshold", 0x400, 10.0, "speed units (not shown to be km/h)", None),
    ("MinRequiredScore", 0x404, 20.0, "score", None),
    ("VehicleRespawnTimer", 0x408, 300.0, "s", None),
    ("LosingVehicleRespawnTimer", 0x40C, 60.0, "s", None),
    ("LosingScoreThreshold", 0x410, 15, "score", None),
    ("SpawnFailedRetryTime", 0x414, 10.0, "s", None),
    ("PlayerDeployCooldown", 0x418, 120.0, "s", 600.0),
    ("MaxInteractionDistance", 0x358, 500.0, "cm", None),
    ("SpawnVehicleStateRetryDelay", 0x3C0, 1.0, "s", None),
    ("StreamingTimer", 0x3C4, 5.0, "s", None),
    ("LookbackSeconds", 0x3D4, 30.0, "s", None),
    ("DamageLookBackSeconds", 0x3D8, 10.0, "s", None),
    ("MinRiskDisplaySeconds", 0x3DC, 15.0, "s", None),
    ("ContestedThreshold", 0x3CC, 1, "count", None),
    ("LethalThreshold", 0x3D0, 2, "count", None),
]

MAP_NAMES = {  # world package -> map article name (zone config / minimap folder pairing, see the map articles)
    "Kavkazi": "Bakurani", "Europe": "Ozeti", "NorthAmerica": "Zestafona", "Russia": "Saburtulo",
    "Gym_Minimal": "Gym (test area)"}
FACTION_BY_BOARD = {"Lonestar": "Alpha", "Manticore": "Charlie", "Valkrya": "Bravo"}  # checked against the data below

# Vehicle tag (after "Vehicle.Variant.") -> display names (from _wiki/vehicles.md). Parent tags cover a whole family.
TAG_NAMES = {
    "Air": ["any air vehicle (every helicopter and the airplane, minus anything the volume excludes)"],
    "Air.Rotary.Havoc": ["Havoc"],
    "Air.Rotary.Littlebird": ["MH-6", "AH-6M [Miniguns]", "AH-6R [Rockets]"],
    "Air.Rotary.ROT_01": ["Huey"],
    "Air.Rotary.ROT_04": ["Z20 Lakota", "Z20 Lakota [Miniguns]"],
    "Land": ["any land vehicle"],
    "Land.Tracked": ["any tracked vehicle (minus the excluded faction APCs)"],
    "Land.Tracked.TNK_01": ["L2A6", "Flakpanzer Gepard", "SPH-2"],
    "Land.Tracked.TNK_04": ["T-72B3"],
    "Land.Tracked.SpawnVehicle.Lonestar": ["M113 APC SV (Lonestar version)"],
    "Land.Tracked.SpawnVehicle.Manticore": ["M113 APC SV (Manticore version)"],
    "Land.Tracked.SpawnVehicle.Valkyra": ["M113 APC SV (Valkyra version)"],
    "Land.Wheeled.Azar": ["Azar (test vehicle, no wiki article)"],
    "Land.Wheeled.Bobcat": ["Bobcat"],
    "Land.Wheeled.DuneBuggy": ["Dune Buggy"],
    "Land.Wheeled.Humvee": ["Humvee", "Humvee [M249]", "Humvee [Minigun]"],
    "Land.Wheeled.Kodiak": ["Kodiak", "Kodiak [M249]", "Kodiak [Pickup]"],
    "Land.Wheeled.Ural": ["Ural", "Ural Defender", "Ural Defender [M249]"],
    "Land.Wheeled.WHL_08": ["Wolf 110", "Wolf 110 [M2 Browning]"],
}


def r1(x):
    return None if x is None else round(x, 1)


_cache = {}
EXTRA = ""  # set in main(): <boards dir>/../sv_extra


def _pkg(sv, path):
    b = path.rsplit("/", 1)[1]
    if b not in _cache:
        _cache[b] = None
        for dd in (sv, EXTRA):
            fn = os.path.join(dd, b + ".json")
            if os.path.exists(fn):
                _cache[b] = json.load(open(fn, encoding="utf-8"))
                break
    return _cache[b]


def _res(sv, ref):
    if not ref or not ref.get("ObjectPath"):
        return None
    pth, n = ref["ObjectPath"].rsplit(".", 1)
    try:
        return _pkg(sv, pth)[int(n)]
    except Exception:
        return None


def _loc(sv, ref):
    c = _res(sv, ref)
    v = c.get("Properties", {}).get("RelativeLocation") if c else None
    return None if v is None else [r1(v["X"]), r1(v["Y"]), r1(v["Z"])]


def short(tags):
    return [t.replace("Vehicle.Variant.", "") for t in tags]


def kind_of(allowed):
    if not allowed:
        return "infantry"  # no vehicle list
    if any("SpawnVehicle" in t for t in allowed):
        return "apc"
    if any(t == "Air" or t.startswith("Air.") for t in allowed):
        return "air"
    if allowed == ["Land.Wheeled.Bobcat"]:
        return "light"
    return "ground"


def cell_layers(sv, world):
    """cell package name -> sorted data-layer asset names, read from the world package's streaming cells."""
    fn = os.path.join(sv, world + ".json")
    out = {}
    if not os.path.exists(fn):
        return out
    d = json.load(open(fn, encoding="utf-8"))
    inst = {}
    for e in d:
        if e["Type"] == "DataLayerInstanceWithAsset":
            inst[e["Name"]] = e["Properties"]["DataLayerAsset"]["ObjectName"].split("'")[1]
    for e in d:
        if e["Type"] == "WorldPartitionRuntimeLevelStreamingCell":
            lv = e["Properties"].get("LevelStreaming", {}).get("ObjectName", "")
            m = re.search(r"WorldPartitionLevelStreaming_(\w+)'", lv)
            if m:
                out[m.group(1)] = sorted(inst.get(x, x) for x in (e["Properties"].get("DataLayers") or {}).get("DataLayers", []))
    return out


def collect(scratch, boards_dir):
    sv = os.path.join(scratch, "sv")
    layers = {}
    vols, boards, mgrs = [], [], []
    for f in sorted(glob.glob(os.path.join(sv, "*.json")) + glob.glob(os.path.join(EXTRA, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        world = next((e["Name"] for e in d if e["Type"] == "World"), "")
        cell = os.path.basename(f)[:-5]
        if world not in layers:
            layers[world] = cell_layers(sv, world)
        dl = layers[world].get(cell, [])
        edl = sorted({(e.get("Outer") or {}).get("ObjectPath", "").split("/_Generated_")[0].split("/Game/")[0]
                      for e in d if (e.get("Outer") or {}).get("ObjectPath", "").startswith("/")
                      and not e["Outer"]["ObjectPath"].startswith("/Game/")})
        for e in d:
            t, p = e["Type"], e.get("Properties", {})
            if t == "WDSpawnVolume":
                allowed = short(p.get("AllowedObjectsToSpawn", []))
                tps = [x["ObjectPath"] for x in p.get("TargetPoints", []) if x]
                vols.append({
                    "world": world, "cell": cell, "data_layers": dl, "external_layer": edl[0] if edl else None, "actor": e["Name"], "label": e.get("ActorLabel"),
                    "faction": ((p.get("FactionTag") or {}).get("TagName") or "").split(".")[-1] or None,
                    "kind": kind_of(allowed),
                    "allowed": allowed, "disallowed": short(p.get("DisallowedObjectsToSpawn", [])),
                    "vehicle_spots": len(p.get("TargetPoints", [])), "max_spawn_points": p.get("MaxSpawnPoints"),
                    "horizontal_spacing": p.get("HorizontalSpacing"), "vertical_spacing": p.get("VerticalSpacing"),
                    "location": _loc(sv, p.get("RootComponent")), "_tps": tps,
                })
            elif t.startswith("B_VehicleDeploymentBoard"):
                cls = t.split("_")[2]
                boards.append({
                    "world": world, "cell": cell, "data_layers": dl, "actor": e["Name"], "board_class": cls,
                    "vehicle_spots": len(p.get("VehicleSpawnLocations", [])),
                    "instance_overrides": {k: p[k] for k in ("VehicleHealthThreshold", "VehicleSpeedThreshold",
                                                              "VehicleRespawnTimer", "PlayerDeployCooldown") if k in p},
                    "location": _loc(sv, p.get("RootComponent")),
                    "_tps": [x["ObjectPath"] for x in p.get("VehicleSpawnLocations", []) if x],
                })
            elif t == "B_SpawnManager_C":
                mgrs.append({
                    "world": world, "cell": cell, "data_layers": dl, "actor": e["Name"],
                    "faction": ((p.get("FactionTag") or {}).get("TagName") or "").split(".")[-1] or None,
                    "spawn_points": len(p.get("SpawnTransforms", [])),
                    "query": ((p.get("SpawnFinderQuery") or {}).get("ObjectName") or "").replace("EnvQuery'", "").rstrip("'") or None,
                    "location": _loc(sv, p.get("RootComponent") or p.get("DefaultSceneRoot")),
                    "external_layer": edl[0] if edl else None,
                })
    return vols, boards, mgrs


def board_defaults(boards_dir):
    out = {}
    for f in sorted(glob.glob(os.path.join(boards_dir, "B_VehicleDeploymentBoard*.json"))):
        for e in json.load(open(f, encoding="utf-8")):
            if e.get("Name", "").startswith("Default__"):
                p = e.get("Properties", {})
                row = {}
                for k, v in p.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        row[k] = v
                    elif isinstance(v, dict) and "TagName" in v:
                        row[k] = v["TagName"]
                    elif isinstance(v, list) and v and all(isinstance(x, str) for x in v):
                        row["rejection_reasons"] = v
                if row:
                    out[os.path.basename(f)[:-5]] = row
    return out


EXP_DIR = os.path.join(ROOT, "data", "Wardogs", "Config", "Experiences")
MODE_NAMES = {  # experience alias -> map name used in the wiki (or the server browser name when the wiki has no article)
    "Bakurani_KOTH_01": "Bakurani", "Bakurani_KOTH_02": "Bakurani", "Madrid_KOTH_01": "Ozeti",
    "Detroit_KOTH_01": "Zestafona", "Moscow_KOTH_01": "Saburtulo", "Kenya_KOTH_01": "Kenya",
    "ED_Detroit_KOTH_01": "Zestafona", "Bakurani_SniperShowdown_01": "Bakurani Outskirts - Jutari",
    "Detroit_SniperShowdown_01": "Detroit Sniper Showdown", "Moscow_SniperShowdown_01": "Moscow Sniper Showdown",
    "Berlin_KOTH_01": "Berlin", "Paris_KOTH_01": "Paris", "Mindori_KOTH_01": "Mindori", "Tevza_KOTH_01": "Tevza"}


def layer_summaries(vols, boards, mgrs):
    def key(x):
        return (x["world"], x["data_layers"][0] if x["data_layers"] else None)
    groups = collections.defaultdict(lambda: {"v": [], "b": [], "m": []})
    for k, lst in (("v", vols), ("b", boards), ("m", mgrs)):
        for x in lst:
            groups[key(x)][k].append(x)
    out = {}
    for (w, layer), g in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1] or "")):
        if w == "Gym_Minimal":
            continue
        fc = collections.Counter(v["faction"] for v in g["v"])
        main = fc.most_common(1)[0][0] if fc else None
        mine = [v for v in g["v"] if v["faction"] == main]
        stray = [{"faction": v["faction"], "kind": v["kind"], "allowed": v["allowed"], "vehicle_spots": v["vehicle_spots"]}
                 for v in g["v"] if v["faction"] != main]
        tags = collections.Counter(t for v in mine if v["kind"] != "apc" for t in v["allowed"])
        out["%s/%s" % (w, layer or "(no data layer)")] = {
            "world": w, "layer": layer, "faction": main,
            "volumes": len(mine), "by_kind": dict(sorted(collections.Counter(v["kind"] for v in mine).items())),
            "vehicle_spots": sum(v["vehicle_spots"] for v in mine),
            "volumes_offering_tag": dict(sorted(tags.items())),
            "apc_volume_tags": sorted({t for v in mine if v["kind"] == "apc" for t in v["allowed"]}),
            "boards": [{"class": b["board_class"], "vehicle_spots": b["vehicle_spots"]} for b in g["b"]],
            "infantry_spawn_managers": [{"faction": m["faction"], "points": m["spawn_points"], "query": m["query"]}
                                        for m in g["m"]],
            "stray_volumes": stray,
        }
    return out


def experiences(layers, vols):
    out = {}
    files = [f for w in ("Africa", "Europe", "Kavkazi", "NorthAmerica", "Russia")
             for f in sorted(glob.glob(os.path.join(EXP_DIR, w, "*.json")))]
    for f in files:
        d = json.load(open(f, encoding="utf-8-sig"))
        alias = (d.get("Aliases") or [os.path.basename(f)[:-5]])[0]
        world = os.path.basename(os.path.dirname(f))
        rows, missing = [], []
        for dl in d.get("EnabledDataLayers", []):
            if not dl.endswith("Spawn"):
                continue
            hit = layers.get("%s/%s" % (world, dl))
            if hit:
                rows.append(hit)
            else:
                missing.append(dl)
        base = [v for v in vols if v["world"] == world and not v["data_layers"] and not v["external_layer"]
                and v["kind"] != "infantry"]
        extra = base + [x for r in rows for x in r["stray_volumes"]]
        tot = {"extra_volumes": len(extra), "extra_vehicle_spots": sum(x["vehicle_spots"] for x in extra),
               "volumes": sum(r["volumes"] for r in rows), "vehicle_spots": sum(r["vehicle_spots"] for r in rows),
               "boards": sum(len(r["boards"]) for r in rows),
               "infantry_spawn_managers": sum(len(r["infantry_spawn_managers"]) for r in rows)}
        out[alias] = {"map": MODE_NAMES.get(alias, alias), "world": world,
                      "enabled_data_layers": d.get("EnabledDataLayers", []),
                      "spawn_layers_with_volumes": [r["layer"] for r in rows],
                      "spawn_layers_without_volumes": missing,
                      "teams": {(r["faction"] or "none"): r["layer"] for r in rows},
                      "totals": tot}
    return out


def build(scratch, boards_dir):
    vols, boards, mgrs = collect(scratch, boards_dir)
    # link each board to the volume it serves: shared target-point actors; else the APC volume of the same data layer
    tp_owner = {}
    for i, v in enumerate(vols):
        for t in v["_tps"]:
            tp_owner[t] = i
    for b in boards:
        owners = {tp_owner[t] for t in b["_tps"] if t in tp_owner}
        b["volume_faction"] = vols[owners.pop()]["faction"] if len(owners) == 1 else None
        b["link"] = "target points" if b["volume_faction"] else None
        if b["volume_faction"] is None and b["data_layers"]:
            m = [v for v in vols if v["world"] == b["world"] and v["data_layers"] == b["data_layers"] and v["kind"] == "apc"]
            if len(m) == 1:
                b["volume_faction"], b["link"] = m[0]["faction"], "same data layer"
    for v in vols:
        del v["_tps"]
    for b in boards:
        del b["_tps"]
    pair = collections.Counter("%s|%s" % (b["board_class"], b["volume_faction"]) for b in boards
                               if b["world"] != "Gym_Minimal")
    apc_mismatch = []
    want = {"Alpha": "Lonestar", "Bravo": "Valkyra", "Charlie": "Manticore"}
    for v in vols:
        for t in v["allowed"]:
            if "SpawnVehicle." in t and want.get(v["faction"]) != t.split(".")[-1]:
                apc_mismatch.append({"world": v["world"], "layer": (v["data_layers"] or [None])[0],
                                     "volume_faction": v["faction"], "apc_tag": t})
    vols.sort(key=lambda v: (v["world"], v["faction"] or "", v["kind"], v["actor"]))
    boards.sort(key=lambda v: (v["world"], v["board_class"], v["actor"]))
    mgrs.sort(key=lambda v: (v["world"], v["faction"] or "", v["actor"]))
    layers = layer_summaries(vols, boards, mgrs)

    worlds = {}
    for w in sorted({v["world"] for v in vols}):
        wv = [v for v in vols if v["world"] == w]
        worlds[w] = {"map": MAP_NAMES.get(w, w), "volumes": len(wv),
                     "boards": sum(1 for b in boards if b["world"] == w),
                     "infantry_spawn_managers": sum(1 for m in mgrs if m["world"] == w),
                     "vehicle_spots": sum(v["vehicle_spots"] for v in wv),
                     "spawn_layers": sorted(k.split("/", 1)[1] for k in layers if k.startswith(w + "/"))}

    ini = open(INI, encoding="utf-8-sig").read()
    mvp = int(re.search(r"MaxVehiclesPerPlayer=(\d+)", ini).group(1))
    return {
        "note": "Vehicle deployment volumes (WDSpawnVolume), deployment boards and infantry spawn managers placed in the "
                "world levels, grouped by the data layer of their streaming cell. A match enables one base-map data layer "
                "plus three spawn layers (one per team slot); see 'experiences'. Generated by _tools/vehicle_spawns.py.",
        "map_names": {w: MAP_NAMES.get(w, w) for w in worlds},
        "faction_pairing_board_class_to_volume_faction": dict(sorted(pair.items())),
        "apc_tag_disagrees_with_volume_faction": apc_mismatch,
        "tag_display_names": TAG_NAMES,
        "tag_display_names_basis": "inferred from the internal-name rows of the vehicle articles; Havoc, Littlebird, "
                                   "ROT_01 and ROT_04 pairings follow the explosion and spotting tables",
        "vehicle_limits": {"MaxVehiclesPerPlayer": mvp,
                           "source": "VehicleUtility plugin ini (WDVehicleUtilityComponent)"},
        "board_blueprint_defaults": board_defaults(boards_dir),
        "board_native_defaults": {
            "constructor_rva": "0x7708A00", "status": "FOUND (static disassembly)",
            "note": "Fields the board Blueprint and the map boards leave unset keep these constructor values. The Blueprint "
                    "overrides PlayerDeployCooldown (600 s) and RadarRestoreHealthThreshold (0.55); only the Gym test boards "
                    "override the respawn timer (240 s) and the deploy cooldown (120 s). The consumers of the respawn timers "
                    "were not located, so what exactly the game does with them is inferred from the field names.",
            "fields": [{"field": f, "offset": "0x%X" % o, "native_default": v, "unit": u, "blueprint_override": b}
                       for f, o, v, u, b in BOARD_NATIVE]},
        "vehicle_limits_native": {"MaxVehiclesPerPlayer": {"native_default": 2, "constructor_rva": "0x893EDE0",
                                                           "status": "FOUND (static disassembly)"}},
        "board_timer_note": "Map boards carry no instance overrides, so the blueprint default applies for PlayerDeployCooldown "
                            "(600 s). VehicleRespawnTimer (300 s), LosingVehicleRespawnTimer (60 s), VehicleHealthThreshold "
                            "(0.3) and VehicleSpeedThreshold (10) are not set in the blueprint or in any map instance, so the "
                            "native class defaults read in round 53 apply; only the Gym test area overrides them (240 s respawn, "
                            "120 s deploy cooldown).",
        "worlds": worlds,
        "spawn_layers": layers,
        "experiences": experiences(layers, vols),
        "volumes": vols,
        "boards": boards,
        "infantry_spawn_managers": mgrs,
    }


PAGE = os.path.join(ROOT, "game-features", "Wardogs_VehicleSpawns_v1.md")
TEAM = {"Alpha": "A", "Bravo": "B", "Charlie": "C"}
SIDE = {"Alpha": "Lonestar", "Bravo": "Valkyra", "Charlie": "Manticore"}
SHORT = {
    "Air": "any air vehicle", "Land": "any land vehicle", "Land.Tracked": "any tracked vehicle",
    "Air.Rotary.Havoc": "Havoc", "Air.Rotary.Littlebird": "Little Bird family", "Air.Rotary.ROT_01": "Huey",
    "Air.Rotary.ROT_04": "Z20 Lakota family", "Land.Tracked.TNK_01": "L2A6 family", "Land.Tracked.TNK_04": "T-72B3",
    "Land.Wheeled.Azar": "Azar (test)", "Land.Wheeled.Bobcat": "Bobcat", "Land.Wheeled.DuneBuggy": "Dune Buggy",
    "Land.Wheeled.Humvee": "Humvee family", "Land.Wheeled.Kodiak": "Kodiak family", "Land.Wheeled.Ural": "Ural family",
    "Land.Wheeled.WHL_08": "Wolf 110 family"}


def _names(tags):
    return ", ".join(SHORT.get(t, t) for t in tags) or "none"


def render_page(data):
    L = data["spawn_layers"]
    E = data["experiences"]
    apc_vols = [v for v in data["volumes"] if v["kind"] == "apc"]
    apc_bad = len(data["apc_tag_disagrees_with_volume_faction"])
    maps_mgr = [m for m in data["infantry_spawn_managers"] if m["world"] != "Gym_Minimal" and m["spawn_points"]]
    q_n = sum(1 for m in maps_mgr if m["query"])
    pts = sorted(m["spawn_points"] for m in maps_mgr)
    nl = sorted(len(x["spawn_layers"]) for wn, x in data["worlds"].items() if wn != "Gym_Minimal")
    pr = data["faction_pairing_board_class_to_volume_faction"]
    pair_n = sum(n for k, n in pr.items() if not k.endswith("None"))
    pair_ok = sum(n for k, n in pr.items() if k in ("Lonestar|Alpha", "Manticore|Charlie", "Valkrya|Bravo"))
    spots = sorted(b["vehicle_spots"] for b in data["boards"] if b["world"] != "Gym_Minimal")
    o = []
    w = o.append
    w("---")
    w('title: "Vehicle Spawns"')
    w('redirect_from: ["/Wardogs_VehicleSpawns_v1.html", "/Wardogs_VehicleSpawns_v1"]')
    w('parent: "Game Modes & Maps"')
    w('description: "Vehicle deployment points, vehicle yards and infantry spawn areas placed on each map: counts per team, the vehicles each yard allows, and the deploy timers the data gives"')
    w("---")
    w("")
    w("# Wardogs: Vehicle Spawns (deployment boards, vehicle yards and infantry spawn areas per map)")
    w("")
    w("*Source: the 61 world and World Partition cell packages that name the spawn volume class, plus the 5 further cells that hold a deployment board or spawn manager without a volume, the board Blueprint defaults, the experience configs under `data/Wardogs/Config/Experiences` and the VehicleUtility ini. Everything below is generated by [`_tools/vehicle_spawns.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/vehicle_spawns.py) into [`assets/data/vehicle-spawns.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-spawns.json); do not edit this page by hand. Evidence level: cooked data read, nothing run.*")
    w("")
    w("Round 42 found 110 spawn volumes in the world data ([evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md)). This page ties them to maps: each volume sits in a World Partition cell that belongs to a **spawn data layer** (for example `DL_GranadaSpawn`), and each King of the Hill entry in the experience configs enables one base layer plus **three spawn layers**, one per team slot ([Experiences](Wardogs_GameFeatures_Experiences_v2.md)). So a match uses three spawn sites per map, and each site is one layer.")
    w("")
    w("## 1. What a spawn layer holds")
    w("")
    w("Every spawn layer holds the same kit for one team slot (Alpha, Bravo or Charlie in the data):")
    w("")
    w("- **One deployment board** (`B_VehicleDeploymentBoard_<faction>_C`). It carries %d to %d vehicle spots (`VehicleSpawnLocations`, target points) and spawns the faction's APC (the [M113 APC SV](../_wiki/vehicles/m113-apc-sv.md) in the Lonestar, Valkyra or Manticore version, set by `SpawnVehicleTag`). Players deploy onto that vehicle. The board shows one reason at a time, the highest-priority one that applies (round 75, [evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round75-open-questions.md)): respawning, score required, no vehicle, radar destroyed, not in the control zone, vehicle moving (`Interactive.Deployment.Rejection.Driving`) and no free seat (`.NoSeat`); a player on cooldown or outside the zone sees those instead. The `.LowHP` tag exists but no rule uses it." % (spots[0], spots[-1]))
    w("- **Three to six spawn volumes** (`WDSpawnVolume`): normally an APC volume (the spots of the board), one to three ground-vehicle yards, one air yard and one light-vehicle (Bobcat) yard. A few layers lack one of these (section 3). Each lists the vehicle tags it allows and excludes. The `TargetPoints` of a volume are the vehicle spots; `MaxSpawnPoints` and the spacing fields are separate generation settings whose use was not traced (0 on many volumes).")
    w("- **One infantry spawn manager** (`B_SpawnManager_C`) with a `FactionTag` and a grid of %d to %d spawn transforms (200 cm spacing, the nine-by-nine grid trimmed to the terrain). This is the infantry spawn area of that team slot. The spawn query asset (`EQS_SpawnQuery_800_Bravo`, an 800 cm search) is set on %d of the %d managers." % (pts[0], pts[-1], q_n, len(maps_mgr)))
    w("")
    w("Totals per world are in section 6. The Kenya entry enables only its base layer (`DL_Kenya`) and has no world package under `Maps/Worlds` in the client (no Kenya or Africa map files at all); Sniper Showdown and the Tevza entry enable no spawn layer that holds a volume (Tevza names three spawn layers that no dumped cell contains; the three spawn managers without a layer are the PvE scenario spawn areas, round 75).")
    w("")
    w("## 2. King of the Hill entries")
    w("")
    w("Team slots: Alpha is paired with the Lonestar APC, Bravo with Valkyra and Charlie with Manticore (**inferred**: %d of %d APC volume tags and %d of %d linked board classes agree; the exceptions are listed in section 7)" % (len(apc_vols) - apc_bad, len(apc_vols), pair_ok, pair_n) + ".")
    w("")
    w("| Entry | Map | Alpha layer | Bravo layer | Charlie layer | Vehicle volumes | Vehicle spots | Boards | Infantry areas |")
    w("|---|---|---|---|---|---:|---:|---:|---:|")
    for k, e in E.items():
        if not e["teams"]:
            continue
        t = e["totals"]
        vv = str(t["volumes"]) + (" (+%d outside the layers)" % t["extra_volumes"] if t["extra_volumes"] else "")
        vs = str(t["vehicle_spots"]) + (" (+%d)" % t["extra_vehicle_spots"] if t["extra_vehicle_spots"] else "")
        w("| `%s` | %s | `%s` | `%s` | `%s` | %s | %s | %d | %d |" % (
            k, e["map"], e["teams"].get("Alpha", "-"), e["teams"].get("Bravo", "-"), e["teams"].get("Charlie", "-"),
            vv, vs, t["boards"], t["infantry_spawn_managers"]))
    w("")
    w("\"Vehicle volumes\" counts the ground, air, light and APC volumes of the three layers; the infantry volume that sits in a Strike and Disarm layer is not counted. \"Vehicle spots\" sums the target points of those volumes. Entries with no row here: `Kenya_KOTH_01` (base layer only), the three Sniper Showdown entries (data-layer set `EDL_SniperShowdown`, no spawn layer) and `Tevza_KOTH_01` (its spawn layers `DL_VostimiSpawn`, `DL_EdemiSpawn` and `DL_ShovliSpawn` hold no cell in the client).")
    w("")
    w("## 3. Spawn layers")
    w("")
    w("| Layer | World | Team | Board APC | APC volume | Ground yards | Air yards | Light yards | Vehicle spots | Infantry spawn grid |")
    w("|---|---|---|---|---:|---:|---:|---:|---:|---|")
    for k, l in L.items():
        if not l["layer"]:
            continue
        bk = l["by_kind"]
        brd = ", ".join(b["class"].replace("Valkrya", "Valkyra") for b in l["boards"]) or "none dumped"
        inf = ", ".join("%d pts" % m["points"] for m in l["infantry_spawn_managers"]) or "none dumped"
        w("| `%s` | %s | %s | %s | %d | %d | %d | %d | %d | %s |" % (
            l["layer"], l["world"], l["faction"], brd, bk.get("apc", 0), bk.get("ground", 0), bk.get("air", 0),
            bk.get("light", 0), l["vehicle_spots"], inf))
    w("")
    w("Layers also hold stray volumes of another team slot in one case: `DL_RostokinoSpawn` carries an extra Alpha air yard (9 spots). The Detroit map has one Alpha air yard in no data layer at all (7 spots, section 7).")
    w("")
    w("## 4. What each layer allows")
    w("")
    w("Tags are `Vehicle.Variant.*` gameplay tags; a parent tag stands for every vehicle under it. Names are from the [Vehicles](../_wiki/vehicles.md) pages (see section 5 for the pairing, which is inferred).")
    w("")
    w("| Layer | Team | APC tag in the volume | Allowed by the ground, air and light yards |")
    w("|---|---|---|---|")
    for k, l in L.items():
        if not l["layer"]:
            continue
        w("| `%s` | %s | %s | %s |" % (l["layer"], l["faction"], _names(l["apc_volume_tags"]).replace("Land.Tracked.SpawnVehicle.", "APC "),
                                     _names(sorted(l["volumes_offering_tag"]))))
    w("")
    w("Each yard also lists tags it **excludes**, which is how a generic tag such as the air tag is narrowed: air yards exclude `Land`; light yards exclude the other wheeled families, the tanks, the APCs and the air tags; APC volumes exclude every other APC tag. The full allowed and excluded lists are in the JSON (`volumes`).")
    w("")
    w("## 5. Tag to vehicle names")
    w("")
    w("| Tag | Vehicles (display names) | Basis |")
    w("|---|---|---|")
    for t, names in data["tag_display_names"].items():
        w("| `%s` | %s | inferred |" % (t, "; ".join(names)))
    w("")
    w("Basis: the internal-name rows of the [vehicle articles](../_wiki/vehicles.md) (TNK_01, TNK_04, WHL_02, WHL_05, WHL_07 and WHL_08 are the family codes) and the spotting and explosion tables for the helicopters. The data lists no vehicle by display name in the volumes, and the tags do not say which variant of a family (for example Humvee with or without a gun) a yard produces. The airplane is under the generic air tag; whether a yard ever places it was not traced. The test vehicle Azar has no wiki article.")
    w("")
    w("## 6. Per-world totals")
    w("")
    w("| World | Map | Volumes | Boards | Infantry spawn managers | Vehicle spots | Spawn layers |")
    w("|---|---|---:|---:|---:|---:|---|")
    for wn, x in data["worlds"].items():
        w("| %s | %s | %d | %d | %d | %d | %s |" % (wn, x["map"], x["volumes"], x["boards"], x["infantry_spawn_managers"],
                                                  x["vehicle_spots"], ", ".join("`%s`" % s for s in x["spawn_layers"])))
    w("")
    w("The totals include every layer a world has, not only those one entry enables (a world has %d to %d spawn layers and an entry uses 3). Gym_Minimal is a test area with its own three infantry volumes and three boards." % (nl[0], nl[-1]))
    w("")
    w("## 7. Limits, timers and data quirks")
    w("")
    bd = data["board_blueprint_defaults"].get("B_VehicleDeploymentBoard", {})
    w("- **Per-player vehicle limit.** `WDVehicleUtilityComponent.MaxVehiclesPerPlayer = 2` (`DefaultVehicleUtility.ini`); the plugin text says it caps vehicle ownership per player on the session game mode.")
    w("- **Deploy cooldown.** `PlayerDeployCooldown` is %s s in the board Blueprint default and no map board overrides it. It is written per player when a deployment seats the player on the board's APC (round 75) and shown as the cooldown reason. `RadarRestoreHealthThreshold` is %s: the radar is flagged destroyed when the APC's radar health reaches 0 and cleared when it is back at that share of its maximum." % (bd.get("PlayerDeployCooldown"), bd.get("RadarRestoreHealthThreshold")))
    w("- **Vehicle respawn timer: a native class default.** The board class has `VehicleRespawnTimer`, `LosingVehicleRespawnTimer`, `VehicleHealthThreshold` and `VehicleSpeedThreshold` (SDK `0x3F8..0x40C`). Neither the Blueprint default nor any of the 18 map boards sets them, so the live maps use the values the native constructor writes (round 53, [evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round53-spawn-board-defaults.md)): **respawn timer 300 s, losing-side respawn timer 60 s, health threshold 0.3, speed threshold 10**, plus a minimum score of 20 and a losing score threshold of 15. The Gym test boards override the respawn timer to 240 s. Round 75 ([evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round75-open-questions.md)) read the consumers: when the APC is lost the board takes the 60 s timer if the best other side leads the board's side by 15 score points or more, otherwise 300 s (scaled by a server value that defaults to 1); the timers time that APC only, not the yard vehicles. No APC is put out until one side has a score of 20 (the board shows the score-required text until then). The speed threshold is 10 km/h (the vehicle-moving reason). The health threshold 0.3 has no reader.")
    w("- **Native cooldown default.** The board constructor sets `PlayerDeployCooldown` to 120 s; the Blueprint raises it to 600 s, so 600 s is what the live maps use. The Gym boards set 120 s explicitly, which equals the native default. `RadarRestoreHealthThreshold` is 0.5 natively and 0.55 in the Blueprint. `MaxVehiclesPerPlayer` is 2 in the native constructor as well as in the ini.")
    w("- **No per-yard vehicle count or per-vehicle respawn timer.** A volume lists allowed tags and spots; how many of each vehicle exist and a per-yard or per-vehicle respawn time is not in the cooked data (the spawn logic is native; see the round 42 note on the open volume route). The board-level respawn timer is in the previous two bullets.")
    w("- **Boards and APC tags disagree in places.** Board classes against the team slot of their layer: Lonestar 5 of 6 on Alpha, Manticore 7 of 8 on Charlie, Valkyra 6 of 6 on Bravo (one Valkyra board has no APC volume to compare). The exceptions are in Russia, where the Kuzminki layer (Alpha) has a Manticore board and the Ramenki layer (Charlie) a Lonestar board. Volumes carry a different APC tag from their team slot in three places (all in Europe, all the Valkyra tag: `DL_StuttgartSpawn`, `DL_CalaisSpawn`, `DL_HanoverSpawn`). Which side of the pair wins at run time is not known.")
    w("- **One Detroit air yard belongs to no spawn layer.** An Alpha air yard with four explicit helicopter families (Havoc, Little Bird family, Huey, Z20 Lakota family) sits in a cell with no data layer, so it is part of the base world for every Detroit entry (inferred from the empty layer list of its cell).")
    w("- **Strike and Disarm.** One infantry volume (Charlie, 15 max points) and one spawn manager sit in the Strike and Disarm external layer on Kavkazi; they are not part of the King of the Hill spawns. Further spawn managers sit in the PvE scenario layers (ScenarioExample, VIP Escort, Strike and Disarm); they were not dumped.")
    w("")
    w("## 8. Reproduce")
    w("")
    w("```")
    w("WdExtract <Paks> <key> <usmap> <out> <Paks>\\oo2core_9_win64.dll findname Wardogs WDSpawnVolume      -> findname.txt (61 packages)")
    w("WdExtract ... <out>\\sv dump <those package paths>")
    w("WdExtract ... findname Wardogs B_SpawnManager_C   (and B_VehicleDeploymentBoard_Lonestar_C / _Manticore_C / _Valkrya_C)")
    w("WdExtract ... <out>\\sv_extra dump <the cells not already in sv>")
    w("WdExtract ... list B_VehicleDeploymentBoard, then dump it plus .../Gamemode/Objects/B_SpawnManager into <out>\\bd")
    w("python -I _tools/vehicle_spawns.py [--check] <round42 dir with sv> <dir bd>   (sv_extra is read next to bd)")
    w("```")
    w("")
    w("Extractor arguments are in [`tools/cue4parse_extractor/README.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/tools/cue4parse_extractor/README.md). The wiki articles for each map summarise this page.")
    w("")
    return "\n".join(o) + "\n"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    scratch = args[0] if args else "E:/Reverse_Engineer/wardogs_analysis/round42_modes"
    boards = args[1] if len(args) > 1 else "E:/Reverse_Engineer/wardogs_analysis/round51_spawns/bd"
    if not os.path.isdir(os.path.join(scratch, "sv")) or not os.path.isdir(boards):
        print("scratch input absent:", scratch, boards)
        return 0
    global EXTRA
    EXTRA = os.path.join(os.path.dirname(os.path.abspath(boards)), "sv_extra")
    data = build(scratch, boards)
    outs = [(OUT, json.dumps(data, indent=1) + "\n"), (PAGE, render_page(data))]
    if check:
        bad = 0
        for path, text in outs:
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
            print(os.path.basename(path), "same" if old == text else "DIFFERENT")
            bad += old != text
        return 1 if bad else 0
    for path, text in outs:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("wrote", path, len(text), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
