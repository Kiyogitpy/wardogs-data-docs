"""Round 39 vehicle tables: weapon rate/range, seat roles, health-trigger effects and flare settings, rebuilt from data/.

Writes four files under assets/data/ (idempotent; rerun gives byte-identical output):

    vehicle-weapons.json         every WDVehicleWeaponExtensionDataAsset (WE_*) with the rate, range, calibre, muzzle speed and reload of
                                 the WDWeaponStatsData it points at. Where the stats asset omits RoundsPerMinute the native constructor
                                 default of FWDWeaponStats (600, +0x138; see _tools/spray_patterns.py) is applied and flagged.
    vehicle-seats.json           every BHSeatSettingsDataAsset seat: role tag, gunner/crew/exterior/standing flags, priority and tags.
    vehicle-health-effects.json  every WDAttributeEffectsTrigger_VehicleHealth in the vehicle GameplaySystems assets: attribute, threshold,
                                 and the effect objects (engine, fuel leak, wheeled, drag, friction, turret, cue) with their values.
    vehicle-flares.json          FWDFlaresSettings per vehicle (starting flares, active time, range band) plus the native defaults.

    python _tools/vehicle_round39_tables.py --write     # (re)write the four JSON files
    python _tools/vehicle_round39_tables.py --check      # exit 1 when a file is stale
    python _tools/vehicle_round39_tables.py              # print counts

Inputs: data/Wardogs/Plugins/GameFeatures/Vehicles/**, data/Wardogs/Plugins/GameFeatures/Weapons/**, data/Wardogs/Content/Vehicles/**.
Evidence: docs/evidence/round39-vehicles-explosives.md. Standard library only; run with python -I.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "Wardogs")
OUT = os.path.join(ROOT, "assets", "data")
DEFAULT_RPM = 600.0  # FWDWeaponStats ctor: RoundsPerMinute (+0x138), constructor default; assets that omit the field use it
# Native defaults of FWDFlaresSettings, read from the targeting-settings constructor sub_14766AEA0 (RVA 0x766AEA0) at struct offset +0x60:
FLARE_NATIVE_DEFAULTS = {
    "StartingFlaresAmount": 0, "FlaresEffectiveRangeMin": 25.0, "FlaresEffectiveRangeMax": 100.0,
    "FlaresActiveTime": 5.0, "FlaresCooldownTime": 5.0,
}


def exports(path):
    """Yield (header, object) for each '--- export:' block of a dumped package file."""
    text = open(path, encoding="utf8").read()
    for part in re.split(r"--- export: ", text)[1:]:
        head, _, body = part.partition("\n")
        try:
            yield head.strip(), json.loads(body[body.find("{"):body.rfind("}") + 1])
        except ValueError:
            continue


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def name_of(ref):
    m = re.search(r"'([^']+)'", ref or "")
    return m.group(1) if m else None


def tag(v):
    return v.get("TagName") if isinstance(v, dict) else v


def vehicle_of(path):
    path = path.replace("\\", "/")
    m = re.search(r"/Pawns/Air/Airplane/(FWG_\d+)/", path)
    if m:
        return m.group(1)
    m = re.search(r"/(Vehicles|VehicleWeaponry)/([^/]+)/", path)
    return m.group(2) if m else "?"


def weapons():
    idx = {}
    for f in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
        idx.setdefault(os.path.basename(f)[:-5], f)
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA, "Plugins", "GameFeatures", "Vehicles", "**", "WE_*.json"), recursive=True)):
        for _, d in exports(f):
            if d.get("Type") != "WDVehicleWeaponExtensionDataAsset":
                continue
            p = d["Properties"]
            sname = name_of((p.get("WeaponStatsData") or {}).get("ObjectName"))
            ws = {}
            if sname in idx:
                for _, sd in exports(idx[sname]):
                    if "WeaponStats" in (sd.get("Properties") or {}):
                        ws = sd["Properties"]["WeaponStats"]
            rpm = ws.get("RoundsPerMinute")
            rows.append({
                "asset": os.path.basename(f)[:-5], "plugin": vehicle_of(rel(f)), "name": p.get("WeaponExtensionName"),
                "statsAsset": sname, "roundsPerMinute": rpm if rpm is not None else DEFAULT_RPM,
                "rpmSource": "stats asset" if rpm is not None else "native default 600 (stats asset omits RoundsPerMinute)",
                "effectiveRange_m": ws.get("EffectiveRange"), "caliber": (ws.get("SupportedCaliber") or [None])[0],
                "initialBulletSpeed": ws.get("InitialBulletSpeed"),
                "fireModes": ws.get("SupportedFireModes"), "accuracyValue": (ws.get("WeaponAccuracy") or {}).get("AccuracyValue"),
                "reloadTime_s": (p.get("ReloadSetupData") or {}).get("ReloadTime"),
                "startingAmmo": {tag(i["Key"]): i["Value"] for i in p.get("WeaponStartingInventoryItems", [])},
                "weaponItemId": tag(p.get("WeaponItemId")),
            })
    return rows


def seats():
    rows = []
    for f in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        if not re.search(r"Seat(Settings|s)|ExtraSeats", os.path.basename(f)):
            continue
        for _, d in exports(f):
            if d.get("Type") != "BHSeatSettingsDataAsset":
                continue
            for i, s in enumerate((d.get("Properties") or {}).get("SeatSetups", []) or []):
                rows.append({
                    "asset": os.path.basename(f)[:-5], "plugin": vehicle_of(rel(f)), "index": i,
                    "role": (tag(s.get("SeatRoleTag")) or "").replace("State.Player.Vehicle.Role.", "") or None,
                    "priority": s.get("SeatPriority"), "isGunner": s.get("bIsGunner"), "isCrewSeat": s.get("bIsCrewSeat"),
                    "isExteriorSeat": s.get("bIsExteriorSeat"), "isStandingSeat": s.get("bIsStandingSeat"),
                    "autoEnterGunner": s.get("bShouldAutoEnterGunner"), "tags": [tag(t) for t in s.get("SeatTags", [])],
                })
    return rows


def effect_value(o):
    p = dict((o or {}).get("Properties") or {})
    out = {}
    for k, v in p.items():
        if k.startswith("_aaa"):
            continue
        if k in ("GameplayCuesToApply", "GameplayCuesToRemove"):
            out[k] = [tag(c.get("GameplayCue")) if isinstance(c, dict) and "GameplayCue" in c else tag(c) for c in v]
        elif isinstance(v, dict) and "ObjectName" in v:
            out[k] = name_of(v["ObjectName"])
        else:
            out[k] = v
    return out


def health_effects():
    rows = []
    files = glob.glob(os.path.join(DATA, "Plugins", "GameFeatures", "Vehicles", "**", "*GameplaySystems*.json"), recursive=True)
    files += glob.glob(os.path.join(DATA, "Content", "Vehicles", "**", "*GameplaySystems*.json"), recursive=True)
    for f in sorted(set(files)):
        objs = {}
        trigs = []
        for _, d in exports(f):
            outer = name_of((d.get("Outer") or {}).get("ObjectName")) or ""
            outer = outer.split(":")[-1].split(".")[0]
            objs[(outer, d.get("Name"))] = d
            if d.get("Type") == "WDAttributeEffectsTrigger_VehicleHealth":
                trigs.append(d)
        for t in trigs:
            p = t["Properties"]
            for th in p.get("ThresholdTriggers", []):
                eff = []
                for key in ("BelowThresholdEffects", "AboveThresholdEffects"):
                    for ref in th.get(key, []) or []:
                        if not ref:
                            continue
                        full = name_of(ref["ObjectName"]) or ""
                        nm = full.split(".")[-1]
                        o = objs.get((t["Name"], nm)) or objs.get((t["Name"], nm.split(":")[-1]))
                        eff.append({"side": "below" if key.startswith("Below") else "above", "type": (o or {}).get("Type", full),
                                    "values": effect_value(o)})
                rows.append({
                    "asset": os.path.basename(f)[:-5], "plugin": vehicle_of(rel(f)), "attribute": tag(p.get("AttributeTag")),
                    "threshold": th.get("AttributeThreshold"), "asPercentage": th.get("bCheckAsPercentage"),
                    "triggersWhenBelow": th.get("bCheckIfBelowThreshold"), "removedInReverse": th.get("bRemoveEffectInReverse"),
                    "effects": eff,
                })
    return rows


SMOKE_FIELDS = {  # FWDSmokeSettings member (obfuscated in the usmap) -> struct offset; roles are not named by the game
    "_aaaakbeoelbjacoaefbcd": "+0x00 item tag", "_aaabddcccjnffofpllkon": "+0x08 byte", "_aaaaphngenogpojekmnlk": "+0x0C float",
    "_aaabbhmhgpiflkhboefec": "+0x10 float", "_aaabdkadoonhgnkciiklf": "+0x14 cue tag", "_aaabdnaapmpnhnelpjlic": "+0x28 vector",
}


def smoke_settings():
    rows = []
    files = glob.glob(os.path.join(DATA, "Plugins", "GameFeatures", "Vehicles", "**", "*GameplaySystems*.json"), recursive=True)
    files += glob.glob(os.path.join(DATA, "Content", "Vehicles", "**", "*GameplaySystems*.json"), recursive=True)
    for f in sorted(set(files)):
        for _, d in exports(f):
            cm = ((d.get("Properties") or {}).get("TargetingSettings") or {}).get("CountermeasureSettings") or {}
            for k, v in cm.items():
                if k == "FlaresSettings" or not isinstance(v, dict):
                    continue
                rows.append({"asset": os.path.basename(f)[:-5], "plugin": vehicle_of(rel(f)),
                             "fields": {SMOKE_FIELDS.get(a, a): (tag(b) if isinstance(b, dict) and "TagName" in b else b) for a, b in v.items()}})
    return rows


def flares():
    rows = []
    files = glob.glob(os.path.join(DATA, "Plugins", "GameFeatures", "Vehicles", "**", "*GameplaySystems*.json"), recursive=True)
    files += glob.glob(os.path.join(DATA, "Content", "Vehicles", "**", "*GameplaySystems*.json"), recursive=True)
    for f in sorted(set(files)):
        for _, d in exports(f):
            ts = ((d.get("Properties") or {}).get("TargetingSettings") or {}).get("CountermeasureSettings") or {}
            fs = ts.get("FlaresSettings")
            if fs:
                rows.append({
                    "asset": os.path.basename(f)[:-5], "plugin": vehicle_of(rel(f)),
                    "set": {k: v for k, v in fs.items() if k in FLARE_NATIVE_DEFAULTS},
                    "effective": {k: fs.get(k, FLARE_NATIVE_DEFAULTS[k]) for k in FLARE_NATIVE_DEFAULTS},
                    "cooldownFromNativeDefault": "FlaresCooldownTime" not in fs,
                })
    return {"nativeDefaults": FLARE_NATIVE_DEFAULTS, "vehicles": rows, "smokeSettings": smoke_settings()}


def repair_tools():
    rows = []
    base = os.path.join(DATA, "Plugins", "GameFeatures", "Items", "VehicleRepairTool", "Content", "Data")
    for f in sorted(glob.glob(os.path.join(base, "ID_*_RepairTool.json"))):
        row = {"asset": os.path.basename(f)[:-5]}
        for _, d in exports(f):
            p = d.get("Properties") or {}
            if d.get("Type") == "WDInventoryFragment_Durability":
                row["durability"] = (p.get("ReplicatedData") or {}).get("Durability")
            if d.get("Type") == "WDItemExtensionData_Appliable":
                row["healthPerApplication"] = p.get("AttributeValue")
                row["attribute"] = tag(p.get("Attribute"))
            for k in ("UpdateTime", "UpdateAmount"):
                if k in (p.get("ContainerData") or {}):
                    row[k] = p["ContainerData"][k]
        rows.append(row)
    return rows



PAGE = os.path.join(ROOT, "game-features", "Wardogs_VehicleWeaponsEffects_v1.md")
REPO = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"
ROLE_CODE = {"Driver": "D", "Gunner": "G", "ActivePassenger": "A", "PassivePassenger": "P"}


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def render_page(b):
    w, se, he = b["vehicle-weapons.json"], b["vehicle-seats.json"], b["vehicle-health-effects.json"]
    fl, rt = b["vehicle-flares.json"], b["vehicle-repair-tools.json"]
    L = []
    L.append('---\ntitle: "Vehicle weapon rates, seats and damage effects"\n'
             'redirect_from: ["/Wardogs_VehicleWeaponsEffects_v1.html", "/Wardogs_VehicleWeaponsEffects_v1"]\n'
             'parent: "Vehicles"\n'
             'description: "Rate and range of every vehicle weapon, flare and smoke settings, seat roles, health-trigger effects and hand repair tool numbers"\n---\n')
    L.append("# Wardogs: Vehicle Weapon Rates, Seats and Damage Effects\n")
    L.append("*Generated by [`_tools/vehicle_round39_tables.py`](" + REPO + "_tools/vehicle_round39_tables.py) (`--write` refreshes this page and the "
             "`assets/data/vehicle-*.json` files). Values are shown as stored in the cooked data unless a cell says otherwise. Reading notes and evidence levels are in the "
             "[round 39 evidence](" + REPO + "docs/evidence/round39-vehicles-explosives.md).*\n")
    L.append("## 1. Vehicle weapons: rate and range\n")
    L.append("Each row is a `WDVehicleWeaponExtensionDataAsset` with the `WDWeaponStatsData` it names. `Rounds/min` marked `*` is the native constructor default of "
             "`FWDWeaponStats` (600, offset `+0x138`): the stats asset omits the field. The T-72B3 coaxial PKTM reuses the infantry `DA_LMG_02_Stats` asset, four vehicles "
             "reuse the infantry `DA_M249_Stats`, and three share one M2 Browning stats asset. Range is `EffectiveRange` (metres, as the other weapon pages read it).\n")
    rows = []
    for r in w:
        rpm = ("%g" % r["roundsPerMinute"]) + ("" if r["rpmSource"] == "stats asset" else "*")
        rows.append(("`%s`" % r["asset"], r["name"], "`%s`" % r["statsAsset"], rpm, "%g" % r["effectiveRange_m"], r["caliber"],
                     "%g" % r["initialBulletSpeed"], r["reloadTime_s"]))
    L.append(md_table(["Extension asset", "Name", "Stats asset", "Rounds/min", "Range (m)", "Caliber", "Muzzle speed", "Reload (s)"], rows) + "\n")
    L.append("## 2. Flares and smoke countermeasures\n")
    L.append("`FWDFlaresSettings` per vehicle. A field the vehicle asset does not set takes the native constructor default (read from `sub_14766AEA0`, RVA `0x766AEA0`): "
             "starting flares 0, range 25 to 100, active time 5.0, **cooldown 5.0 s**. No shipped asset sets `FlaresCooldownTime`, so every flare vehicle uses the 5.0 s default.\n")
    rows = []
    for r in fl["vehicles"]:
        e = r["effective"]
        cd = ("%g (native default)" % e["FlaresCooldownTime"]) if r["cooldownFromNativeDefault"] else "%g" % e["FlaresCooldownTime"]
        rows.append((r["plugin"], e["StartingFlaresAmount"], e["FlaresActiveTime"], cd, "%g to %g" % (e["FlaresEffectiveRangeMin"], e["FlaresEffectiveRangeMax"])))
    L.append(md_table(["Vehicle", "Starting flares", "Active (s)", "Cooldown (s)", "Effective range (m)"], rows) + "\n")
    L.append("Four more vehicle assets carry a smoke countermeasure block (item `Id.Item.VehicleSmoke`, cue `GameplayCue.Vehicle.Countermeasures.Smoke`). "
             "The member names are obfuscated in the game files; the byte at `+0x08` sits in the slot where the flare struct keeps its starting amount.\n")
    rows = [(r["asset"].replace("DA_GameplaySystems_", ""), r["plugin"], r["fields"].get("+0x08 byte"), r["fields"].get("+0x0C float"),
             r["fields"].get("+0x10 float")) for r in fl["smokeSettings"]]
    L.append(md_table(["Gameplay systems asset", "Plugin", "Byte at +0x08", "Float at +0x0C", "Float at +0x10"], rows) + "\n")
    L.append("## 3. Seats\n")
    L.append("One row per seat asset: the roles of its seats in order (`D` driver, `G` gunner, `A` active passenger, `P` passive passenger; `x` marks an exterior seat, `-` a seat with no role tag).\n")
    by = {}
    for r in se:
        by.setdefault((r["plugin"], r["asset"]), []).append(r)
    rows = []
    for (plug, asset), v in by.items():
        code = " ".join(ROLE_CODE.get(x["role"], "-") + ("x" if x["isExteriorSeat"] else "") for x in v)
        rows.append((plug, "`%s`" % asset, len(v), code))
    L.append(md_table(["Plugin", "Seat asset", "Seats", "Roles"], rows) + "\n")
    L.append("## 4. Health-trigger effects\n")
    L.append("Every vehicle `GameplaySystems` asset holds `WDAttributeEffectsTrigger_VehicleHealth` objects: when a health attribute falls below a threshold (percent of that component) its "
             "effect objects apply. The export holds %d thresholds. An effect shown with `{}` serialises no property, so it runs on class defaults that were not read. "
             "Cue-only effects are left out.\n" % len(he))
    agg = {}
    for r in he:
        for e in r["effects"]:
            if e["type"] in ("WDGameplayCueEffect", "WDVehicleWheelGameplayCueEffect"):
                continue
            key = (r["attribute"].replace("Attribute.Gameplay.", ""), e["type"], r["threshold"], json.dumps(e["values"], sort_keys=True))
            agg.setdefault(key, set()).add(r["plugin"])
    rows = [(k[0], k[1], "%g%%" % k[2], "`%s`" % k[3], ", ".join(sorted(v)))
            for k, v in sorted(agg.items(), key=lambda kv: (kv[0][1], kv[0][0], kv[0][2], kv[0][3]))]
    L.append(md_table(["Attribute", "Effect type", "Below", "Values", "Vehicles"], rows) + "\n")
    L.append("## 5. Hand repair tools\n")
    L.append("`HandleApplication` in `B_Action_VehicleRepairTool` sets `RepairAmount` from the item's `ContainerData.UpdateAmount`, passes it to `TryRepairVehicleHealthZone`, and takes the same "
             "amount off the item's durability. The `AttributeValue` 5.0 on the same items is not read by that function.\n")
    rows = []
    for r in rt:
        ua, ut = r.get("UpdateAmount"), r.get("UpdateTime")
        dur = r.get("durability")
        rows.append(("`%s`" % r["asset"], ua, ut, "%.2f" % (ua / ut), dur if dur else "none", ("%.1f s" % (dur / ua * ut)) if dur else "-", r.get("healthPerApplication")))
    L.append(md_table(["Item", "Health per application", "Seconds per application", "Health per second", "Durability", "Time to empty", "`AttributeValue` (not read)"], rows) + "\n")
    return "\n".join(L)


def build():
    return {
        "vehicle-repair-tools.json": repair_tools(),
        "vehicle-weapons.json": weapons(), "vehicle-seats.json": seats(),
        "vehicle-health-effects.json": health_effects(), "vehicle-flares.json": flares(),
    }


def dumps(o):
    return json.dumps(o, indent=1, sort_keys=False, ensure_ascii=False) + "\n"


def main():
    built = build()
    if "--write" in sys.argv:
        for name, obj in built.items():
            with open(os.path.join(OUT, name), "w", encoding="utf8", newline="\n") as fh:
                fh.write(dumps(obj))
        with open(PAGE, "w", encoding="utf8", newline="\n") as fh:
            fh.write(render_page(built))
        print("wrote", ", ".join(built), "and", rel(PAGE))
        return 0
    if "--check" in sys.argv:
        bad = [n for n, o in built.items() if not os.path.exists(os.path.join(OUT, n))
               or open(os.path.join(OUT, n), encoding="utf8", newline="").read() != dumps(o)]
        if not os.path.exists(PAGE) or open(PAGE, encoding="utf8", newline="").read() != render_page(built):
            bad.append(rel(PAGE))
        print("stale:", bad or "none")
        return 1 if bad else 0
    for n, o in built.items():
        print(n, len(o) if isinstance(o, list) else len(o["vehicles"]))
    print(rel(PAGE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
