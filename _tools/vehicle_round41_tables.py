"""Round 41 vehicle and explosive tables: wheeled input tuning, vehicle smoke screen, drone projectile, explosives against vehicles, weapon spread curves.

Writes five files under assets/data/ and one page (idempotent; rerun gives byte-identical output):

    vehicle-input-controls.json   every MWheeledVehicleInputDataAsset (DA_Input_*, DA_WHL_01_Input): scalar tuning and the curve assets it names,
                                  each curve resolved to its keys (time, value).
    explosive-vs-vehicles.json    for each vehicle row of DT_GlobalDamage_VehicleData*: the damage-table entries whose source tag is a utility
                                  explosive (AT mine, C4, Claymore, IED), grenade, 40 mm grenade or the drone, with operation and amount.
    weapon-spread-curves.json     CT_Weapon_Spread rows (key list) and how many item assets name each row.
    grenade-throwback-gate.json   (round 42) per grenade: fuse, throw-back flag, minimum fuse left and whether the native gate can pass.
    air-vehicle-mass-override.json (round 42) MassOverride of the airplane and helicopter body data assets.
    game-features/Wardogs_VehicleInputsAndExplosiveEffects_v1.md   the page built from those files, the smoke block of vehicle-flares.json and
                                  the STN_05 drone projectile asset.

    python _tools/vehicle_round41_tables.py --write     # (re)write the JSON files and the page
    python _tools/vehicle_round41_tables.py --check     # exit 1 when a file is stale
    python _tools/vehicle_round41_tables.py             # print counts

Inputs: data/Wardogs/**. Evidence: docs/evidence/round41-vehicles-explosives.md, round42-vehicles-explosives.md. Standard library only; run with python -I.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
VEH = os.path.join(DATA, "Wardogs", "Plugins", "GameFeatures", "Vehicles")
OUT = os.path.join(ROOT, "assets", "data")
PAGE = os.path.join(ROOT, "game-features", "Wardogs_VehicleInputsAndExplosiveEffects_v1.md")
REPO = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/"


def load(path):
    """Read a dumped package: one JSON value or several concatenated ones, optionally after a '--- export:' line."""
    text = open(path, encoding="utf8").read()
    dec, i, out = json.JSONDecoder(), 0, []
    while i < len(text):
        while i < len(text) and text[i] in " \r\n\t,[]":
            i += 1
        if i >= len(text):
            break
        if text.startswith("---", i):
            i = text.index("\n", i) + 1
            continue
        obj, i = dec.raw_decode(text, i)
        out.append(obj)
    return out


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def g(v):
    return ("%g" % v) if isinstance(v, float) else str(v)


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def curve_keys(name, object_path=""):
    """Keys of a CurveFloat package: resolved from its object path (/PLUGIN/sub/Name.0), else the first file of that name under the vehicle plugins."""
    hits = []
    m = re.match(r"/([^/]+)/(.+)\.\d+$", object_path or "")
    if m:
        cand = os.path.join(VEH, m.group(1), "Content", m.group(2) + ".json")
        if os.path.exists(cand):
            hits = [cand]
    if not hits:
        hits = sorted(glob.glob(os.path.join(VEH, "**", name + ".json"), recursive=True))
    if not hits:
        return None
    for o in load(hits[0]):
        if o.get("Type") == "CurveFloat":
            keys = o.get("Properties", {}).get("FloatCurve", {}).get("Keys", [])
            return [[round(k["Time"], 3), round(k["Value"], 3)] for k in keys]
    return None


def inputs():
    rows = []
    paths = sorted(glob.glob(os.path.join(VEH, "*", "Content", "**", "*.json"), recursive=True))
    for path in paths:
        base = os.path.basename(path)
        if not (base.startswith("DA_Input_") or base.endswith("_Input.json")):
            continue
        for o in load(path):
            if o.get("Type") != "MWheeledVehicleInputDataAsset":
                continue
            scalars, curves = {}, {}
            for k, v in o.get("Properties", {}).items():
                if isinstance(v, dict) and "ObjectName" in v:
                    cname = re.search(r"'([^']+)'", v["ObjectName"]).group(1)
                    curves[k] = {"asset": cname, "keys": curve_keys(cname, v.get("ObjectPath", ""))}
                elif not isinstance(v, (dict, list)):
                    scalars[k] = v
            rows.append({"asset": o["Name"], "vehicle": rel(path).split("/Vehicles/")[1].split("/")[0], "scalars": scalars, "curves": curves})
    return rows


SOURCES = [("Explosive.Utility.ATMine", "AT mine"), ("Explosive.Utility.C4", "C4"), ("Explosive.Utility.Claymore", "Claymore"),
           ("Explosive.Utility.IED", "IED"), ("Explosive.Grenade", "Frag grenade"), ("Explosive.Grenade.40mm", "40 mm grenade"),
           ("Explosive.Drone", "Drone")]


def vs_vehicles():
    rows = {}
    for path in sorted(glob.glob(os.path.join(DATA, "**", "DT_GlobalDamage_VehicleData*.json"), recursive=True)):
        for o in load(path):
            for rn, row in (o.get("Rows") or {}).items():
                key = rn.replace("Meta.Damage.Vehicle.", "")
                for e in row.get("DamageModificationEntries", []):
                    src = [s.replace("Meta.Damage.", "") for s in e["SourceRequirements"]]
                    for tag, label in SOURCES:
                        if tag in src and not (tag == "Explosive.Grenade" and "Explosive.Grenade.40mm" in src):
                            om = e["OutModification"]
                            op = om["Operation"].split("::")[-1]
                            ent = {"source": label, "also": [s for s in src if s != tag], "operation": op, "amount": om["Amount"]}
                            rows.setdefault(key, []).append(ent)
    return [{"row": k, "entries": v} for k, v in sorted(rows.items())]


def spread():
    path = os.path.join(DATA, "Wardogs", "Content", "Items", "Weapons", "Curves", "CT_Weapon_Spread.json")
    tbl = next(o for o in load(path) if o.get("Type") == "CurveTable")
    uses = {}
    for p in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
        if p.endswith("CT_Weapon_Spread.json"):
            continue
        t = open(p, encoding="utf8", errors="ignore").read()
        if "CT_Weapon_Spread" not in t:
            continue
        for m in re.finditer(r'CT_Weapon_Spread[^}]{0,300}?"RowName": "([^"]+)"', t, re.S):
            uses[m.group(1)] = uses.get(m.group(1), 0) + 1
    rows = []
    for name, c in tbl["Rows"].items():
        rows.append({"row": name, "keys": [[round(k["Time"], 3), round(k["Value"], 3)] for k in c["Keys"]], "assetsNamingRow": uses.get(name, 0)})
    rows.sort(key=lambda r: r["row"])
    return rows


def smoke_and_drone():
    fl = json.load(open(os.path.join(OUT, "vehicle-flares.json"), encoding="utf8"))
    smoke = fl["smokeSettings"]
    drone = None
    p = os.path.join(VEH, "STN_05", "Content", "Data", "Projectile", "DA_Drone_ProjectileData.json")
    for o in load(p):
        if o.get("Type") == "WDProjectileData":
            drone = o["Properties"]
    return smoke, drone


def throwback():
    """Grenade throw-back gate (native check 0x6CAE290): rows built from the exported Blueprint defaults (bp-defaults.json)."""
    ents = json.load(open(os.path.join(OUT, "bp-defaults.json"), encoding="utf8"))["entries"]

    def val(asset, prop, default):
        for e in ents:
            if e["asset"] == asset and e["property"] == prop:
                v = e["value"]
                return v["MinimumRemainingFuseTime"] if prop == "GrenadeInteractionData" else v
        return default

    rows = []
    for asset, src in (("B_FragGrenade", "M67"), ("B_GoldFragGrenade", "Gold M67 (inherits the M67 Blueprint)"), ("B_Molotov", "Molotov"), ("B_SmokeGrenade_Red", "Smoke grenades")):
        base = "B_FragGrenade" if asset == "B_GoldFragGrenade" else asset
        fuse = val(asset, "BaseFuseTime", 5.0)
        back = val(base, "bCanThrowBack", False)
        need = val(base, "GrenadeInteractionData", 0.0)
        rows.append({"grenade": src, "asset": asset, "baseFuseTime": fuse, "canThrowBack": back, "minimumRemainingFuseTime": need,
                     "canPassGate": bool(back and fuse > need)})
    return rows


def air_mass():
    """MassOverride of the airplane/helicopter body data assets (read by 0x531D520)."""
    rows = []
    for p in sorted(glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True)):
        if "Vehicles" not in p or "Body" not in os.path.basename(p):
            continue
        try:
            objs = load(p)
        except ValueError:
            continue
        for o in objs:
            pr = o.get("Properties") if isinstance(o, dict) else None
            if pr and "bEnableMassOverride" in pr:
                rows.append({"asset": os.path.basename(p)[:-5], "enabled": pr["bEnableMassOverride"], "massOverride": pr.get("MassOverride")})
    return rows


def build():
    return {"vehicle-input-controls.json": inputs(), "explosive-vs-vehicles.json": vs_vehicles(), "weapon-spread-curves.json": spread(), "grenade-throwback-gate.json": throwback(), "air-vehicle-mass-override.json": air_mass()}


def dumps(o):
    return json.dumps(o, indent=1, ensure_ascii=False) + "\n"


def keytext(keys):
    return "; ".join("%s: %s" % (g(t), g(v)) for t, v in keys) if keys else "-"


# Values read from the BP_Drone_Projectile Blueprint dump (WdExtract, round 41): not in data/, so recorded here.
DRONE_BP = {"collisionBoxHalfExtents": (46.64308, 46.0, 18.7716), "cameraFov": 50.0, "meshScale": 0.7}


def render_page(inp, vs, sp, smoke, drone, tb, mass):
    L = []
    L.append('---\ntitle: "Vehicle Inputs and Explosive Effects"\n'
             'redirect_from: ["/Wardogs_VehicleInputsAndExplosiveEffects_v1.html", "/Wardogs_VehicleInputsAndExplosiveEffects_v1"]\n'
             'parent: "Vehicles"\n'
             'description: "Wheeled steering and pedal tuning, the vehicle smoke screen, the Stingray drone projectile, explosives against each vehicle row, the weapon spread curve table, the grenade throw-back gate and the air vehicle mass override"\n---\n')
    L.append("# Wardogs: Vehicle Inputs and Explosive Effects\n")
    L.append("*Generated by [`_tools/vehicle_round41_tables.py`](" + REPO + "_tools/vehicle_round41_tables.py) (`--write` refreshes this page and "
             "`assets/data/vehicle-input-controls.json`, `explosive-vs-vehicles.json`, `weapon-spread-curves.json`, `grenade-throwback-gate.json`, `air-vehicle-mass-override.json`). Values are shown as stored in the cooked data; "
             "`-` means the asset does not set the field. Evidence: [round 41](" + REPO + "docs/evidence/round41-vehicles-explosives.md).*\n")
    L.append("## 1. Wheeled input tuning (`DA_Input_*`)\n")
    L.append("Each wheeled vehicle names one `MWheeledVehicleInputDataAsset`. The names are the engine's own: sensitivity scales the raw stick or key input, "
             "input gravity is the return-to-centre rate, the deadzone is the stick range ignored, steering assist is an extra correction; the speed and limit curves "
             "shape steering against vehicle speed, and the engagement curves shape throttle, brake and clutch against pedal travel. Units are not labelled by the game.\n")
    cols = ["SteerSensivity", "SteerInputGravity", "SteerDeadzone", "SteeringAssist", "ThrottleSensivity", "BrakingSensivity"]
    rows = [["`%s`" % x["asset"]] + [g(x["scalars"][c]) if c in x["scalars"] else "-" for c in cols] for x in inp]
    L.append(md_table(["Asset", "Steer sensitivity", "Steer input gravity", "Steer deadzone", "Steering assist", "Throttle sensitivity", "Braking sensitivity"], rows) + "\n")
    L.append("The curves each asset names, as (input: output) keys:\n")
    rows = []
    for x in inp:
        for k, c in x["curves"].items():
            rows.append(["`%s`" % x["asset"], k, "`%s`" % c["asset"], keytext(c["keys"])])
    L.append(md_table(["Asset", "Slot", "Curve", "Keys"], rows) + "\n")
    L.append("## 2. Vehicle smoke screen (tanks and the M113)\n")
    L.append("Four vehicle assets carry the smoke block (`TNK_01` Heavy, `TNK_03` Gepard, `TNK_04` T-72B3, `SPW` M113). In the native handler (`0x766F240`) the first "
             "float starts a timer that clears the \"smoke active\" flag and the second float starts a timer that marks the smoke ready again, so they read as a "
             "**16 s active window** and a **90 s cooldown**. The byte is the starting number of smoke charges (`SPW` 255, the tanks 1), by analogy with the flare struct's "
             "starting amount (the load path was not traced). The vector (0, 400, 200) is stored with the effect and is read as a spawn offset (not traced).\n")
    rows = []
    for s in smoke:
        f = s["fields"]
        v = f["+0x28 vector"]
        rows.append(["`%s`" % s["asset"], f["+0x08 byte"], g(f["+0x0C float"]), g(f["+0x10 float"]), "%s, %s, %s" % (g(v["X"]), g(v["Y"]), g(v["Z"]))])
    L.append(md_table(["Gameplay systems asset", "Starting charges", "Active window (s)", "Cooldown (s)", "Offset (X, Y, Z)"], rows) + "\n")
    L.append("## 3. Stingray drone (`STN_05`) projectile\n")
    d = drone["ProjectileStats"]
    dv = d["DamageValues"]
    dm = d["ProjectileDimensions"]
    L.append("The drone is a projectile actor (`BP_Drone_Projectile`). Projectile asset `DA_Drone_ProjectileData`: base damage %s, explosive radius %s, effective radius %s, "
             "minimum explosive damage %s, falloff %s, blunt damage %s, impulse %s / Z %s, length %s, diameter %s, mass %s, arming delay %s s, maximum lifetime %s, typical speed %s, "
             "thrust speed %s, damage tag `%s`. The Blueprint holds a box collision of half extents %s x %s x %s (cm), a camera of field of view %s and a skeletal mesh at scale %s.\n"
             % (g(dv["BaseDamage"]), g(dv["ExplosiveRadius"]), g(dv["EffectiveExplosiveRadius"]), g(dv["MinimumExplosiveDamage"]), g(dv["ExplosiveDamageFallOff"]),
                g(dv["ExplosiveBluntDamage"]), g(dv["ImpulseValues"]["ImpulseScale"]), g(dv["ImpulseValues"]["ImpulseZScale"]), g(dm["Length"]), g(dm["Diameter"]), g(dm["Mass"]),
                g(d["ArmingDelay"]), g(d["MaxProjectileLifetime"]), g(d["TypicalSpeed"]), g(d["ThrustSpeed"]), d["DamageEntityData"]["Tag"]["TagName"],
                g(DRONE_BP["collisionBoxHalfExtents"][0]), g(DRONE_BP["collisionBoxHalfExtents"][1]), g(DRONE_BP["collisionBoxHalfExtents"][2]), g(DRONE_BP["cameraFov"]), g(DRONE_BP["meshScale"])))
    L.append("## 4. Explosives against each vehicle row\n")
    L.append("Every entry in `DT_GlobalDamage_VehicleData*` whose source tag is the listed explosive. The amount is the table's own number: `Percentage_Ongoing` multiplies the running "
             "damage by 1 + amount/100 (so -25 keeps 75 %, +200 triples it), `Add` adds a flat amount. Other entries on the same row (the generic Explosive rows, rocket rows, hit "
             "locations) apply in addition and are in the [damage pipeline](../pipelines/Wardogs_VehicleDamagePipeline_v1.md). A vehicle row missing from a column has no entry for that source. "
             "The Frag grenade column lists the plain grenade source; where the entry also requires the inner radius that is marked.\n")
    labels = [l for _, l in SOURCES]
    rows = []
    for r in vs:
        cell = {l: [] for l in labels}
        for e in r["entries"]:
            tx = ("%+g" % e["amount"]) if e["operation"] == "Percentage_Ongoing" else "%s %+g" % (e["operation"], e["amount"])
            if e["also"]:
                tx += " (+" + ", ".join(a.replace("Explosive.Radius.", "") for a in e["also"]) + ")"
            cell[e["source"]].append(tx)
        rows.append(["`%s`" % r["row"]] + [" / ".join(cell[l]) or "-" for l in labels])
    L.append(md_table(["Vehicle row"] + labels, rows) + "\n")
    L.append("## 5. Weapon spread curves (`CT_Weapon_Spread`)\n")
    L.append("One curve table, %d rows named `<class>.<stance>` (or a mounted-gun name). Each row is a two-key linear curve from input 0 to input 1; the output values are spread "
             "numbers whose unit and the meaning of the 0 to 1 input (read as the share of the weapon's maximum spread buildup) are native and not traced. The last column counts the "
             "item and weapon-extension assets that name the row.\n" % len(sp))
    rows = [["`%s`" % s["row"], keytext(s["keys"]), s["assetsNamingRow"]] for s in sp]
    L.append(md_table(["Row", "Keys (input: output)", "Assets naming it"], rows) + "\n")
    L.append("## 6. Grenade throw-back gate\n")
    L.append("A thrown grenade can be picked up and thrown back only while a native check (`0x6CAE290`) passes: the grenade is older than 0.5 s, moves at no more than 250 cm/s, "
             "and its fuse timer has **more than `MinimumRemainingFuseTime`** seconds left. The fuse timer starts when the grenade is launched, with a length of `BaseFuseTime` minus the "
             "cooked time, so the time left can never exceed `BaseFuseTime`. The M67 Blueprint sets `bCanThrowBack` true and `MinimumRemainingFuseTime` 5.0 against a 4.0 s fuse, "
             "so by this reading **the gate cannot pass for the M67 as shipped**. Other throwables keep the native default (`bCanThrowBack` false). Evidence: [round 42](" + REPO + "docs/evidence/round42-vehicles-explosives.md).\n")
    rows = [[r["grenade"], "`%s`" % r["asset"], g(r["baseFuseTime"]), "yes" if r["canThrowBack"] else "no", g(r["minimumRemainingFuseTime"]), "yes" if r["canPassGate"] else "no"] for r in tb]
    L.append(md_table(["Grenade", "Blueprint", "Fuse (s)", "Throw-back enabled", "Minimum fuse left (s)", "Gate can pass"], rows) + "\n")
    L.append("## 7. Air vehicle mass override\n")
    L.append("The airplane and helicopter body data assets (`UBHAirplaneBodyDataAsset`) can override the physics body mass. The body initialiser (`0x531D520`) reads the enable flag (`+0x52`) and the "
             "double at `+0x58`, converts it to a float and hands it unchanged to the physics mass setter (no scaling), so the number is in the engine's own mass unit, kilograms. "
             "The wheeled `Characteristics.Mass` values use a different path that was not read.\n")
    rows = [["`%s`" % r["asset"], "yes" if r["enabled"] else "no", g(r["massOverride"])] for r in mass]
    L.append(md_table(["Body asset", "Override enabled", "Mass (kg)"], rows) + "\n")
    return "\n".join(L)


def main():
    b = build()
    smoke, drone = smoke_and_drone()
    page = render_page(b["vehicle-input-controls.json"], b["explosive-vs-vehicles.json"], b["weapon-spread-curves.json"], smoke, drone, b["grenade-throwback-gate.json"], b["air-vehicle-mass-override.json"])
    if "--write" in sys.argv:
        for name, obj in b.items():
            with open(os.path.join(OUT, name), "w", encoding="utf8", newline="\n") as fh:
                fh.write(dumps(obj))
        with open(PAGE, "w", encoding="utf8", newline="\n") as fh:
            fh.write(page)
        print("wrote", ", ".join(b), "and", rel(PAGE))
        return 0
    if "--check" in sys.argv:
        bad = [n for n, o in b.items() if not os.path.exists(os.path.join(OUT, n))
               or open(os.path.join(OUT, n), encoding="utf8", newline="").read() != dumps(o)]
        if not os.path.exists(PAGE) or open(PAGE, encoding="utf8", newline="").read() != page:
            bad.append(rel(PAGE))
        print("stale:", bad or "none")
        return 1 if bad else 0
    for n, o in b.items():
        print(n, len(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
