"""Write assets/data/shell-actors.json: Blueprint projectile actors named by DA_*_ProjectileData (round 21).

The data assets set bActorHandlesProjectileMovement / bUseProjectileActor and name a Blueprint actor class
(ProjectileActor). That actor carries a Mover component (BHMoverComponent) whose movement mode is a native
class. This tool joins, for each actor:

  da          the DA_*_ProjectileData fields that choose and feed the actor (read from data/)
  actor       Blueprint class defaults: native parent class, CDO values the Blueprint sets, component values
  mover       Mover component: mode tag, mode class, mode settings the Blueprint sets
  bytecode    functions found in the Blueprint bytecode and the calls/variables each uses
  world       world gravity sources (ini and WorldSettings), read from --world (a JSON list of entries)

Dumps come from tools/cue4parse_extractor (`dump` mode; `rawfiles` mode for the packed .ini files),
written outside this repository. Idempotent:

    python _tools/shell_actors.py --dump DIR [--world DIR]   # rewrite assets/data/shell-actors.json

Entry schema follows assets/data/bp-defaults.json (topic, asset, class, property, value, unit,
resolved_from, from_asset, package, note).
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "data", "shell-actors.json")
CAL = os.path.join(ROOT, "data", "Wardogs")
PA = "Wardogs/Content/Vehicles/Weapons/WeaponExtensions/ProjectileActors/"
CAL_ = "Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/"
PKG = {
    "BP_155mm_Standard": PA + "BP_155mm_Standard",
    "BP_155mm_Expensive": PA + "BP_155mm_Expensive",
    "BP_120x570mm": PA + "BP_120x570mm",
    "BP_120x800mm": PA + "BP_120x800mm",
    "BP_125x570mm": PA + "BP_125x570mm",
    "BP_122mm": CAL_ + "122mm/BP_122mm",
    "BP_40mm": CAL_ + "40mm/BP_40mm",
    "BP_72mm": CAL_ + "72mm/BP_72mm",
    "BP_84mm": CAL_ + "84mm/BP_84mm",
    "BP_93mm": CAL_ + "93mm/BP_93mm",
    "BP_Drone_Projectile": "Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Blueprints/BP_Drone_Projectile",
    "BP_MoverProjectile": "Wardogs/Content/Developers/ryangoldsmith/Movement/Mover/BP_MoverProjectile",
}
SKIP_CDO = {"UberGraphFrame", "BoxComponent", "MoverComponent", "ProjectileMesh", "NetworkSmoothingComponent",
            "RootComponent", "CameraComponent", "CameraSpringArmComponent", "FirstPersonMesh"}
DA_FIELDS = ["bUseProjectileActor", "bActorHandlesProjectileMovement", "TypicalSpeed", "ThrustSpeed",
             "MaxProjectileLifetime", "bShouldPreSimulate", "bClientPredictive", "PerceivedImpactRange"]
E = []


def add(topic, asset, cls, prop, value, resolved, frm, pkg, note="", unit=""):
    e = {"topic": topic, "asset": asset, "class": cls, "property": prop, "value": value, "unit": unit,
         "resolved_from": resolved, "from_asset": frm, "package": pkg}
    if note:
        e["note"] = note
    E.append(e)


def load_json_text(p):
    t = open(p, encoding="utf-8").read()
    parts = re.split(r"^--- export:.*$", t, flags=re.M)
    return [json.loads(x) for x in parts if x.strip()]


def da_links():
    """actor name -> list of (da asset, da package, ProjectileStats dict)."""
    out = {}
    for p in glob.glob(CAL + "/**/*.json", recursive=True):
        b = os.path.basename(p)
        if "ProjectileData" not in b and "Missile" not in b:
            continue
        try:
            docs = load_json_text(p)
        except Exception:
            continue
        for d in docs:
            ps = (d.get("Properties") or {}).get("ProjectileStats") or {}
            pa = ps.get("ProjectileActor")
            if not pa:
                continue
            m = re.search(r"/([^/.]+)\.[^/]+$", pa.get("AssetPathName", ""))
            if m:
                out.setdefault(m.group(1), []).append((d["Name"], d.get("Package", "").lstrip("/"), ps))
    return out


def scalar(v):
    return isinstance(v, (int, float, str, bool)) or (isinstance(v, dict) and v and all(isinstance(x, (int, float)) for x in v.values()))


def clsname(s):
    return s.replace("Class'", "").rstrip("'")


def walk(x, calls, ivars):
    if isinstance(x, dict):
        f = x.get("Function")
        if isinstance(f, dict) and "ObjectName" in f:
            calls.add(clsname(f["ObjectName"]))
        if x.get("Token") == "EX_InstanceVariable":
            n = (x.get("Variable", {}).get("Property") or {}).get("Name")
            if n:
                ivars.add(n)
        for v in x.values():
            walk(v, calls, ivars)
    elif isinstance(x, list):
        for v in x:
            walk(v, calls, ivars)


def actor(name, dump):
    pkg = PKG[name]
    ex = json.load(open(os.path.join(dump, name + ".json"), encoding="utf-8"))
    cdo = next(e for e in ex if e["Name"] == "Default__" + name + "_C")
    gen = next(e for e in ex if e["Type"] == "BlueprintGeneratedClass")
    A = name
    add("actor", A, "BlueprintGeneratedClass", "ParentNativeClass", clsname(gen["SuperStruct"]["ObjectName"]), "export", A, pkg)
    for k, v in cdo["Properties"].items():
        if k in SKIP_CDO:
            continue
        if k == "PrimaryActorTick":
            k, v = "PrimaryActorTick.bCanEverTick", v.get("bCanEverTick")
        if scalar(v) or (isinstance(v, dict) and "TagName" in v):
            add("actor", A, name + "_C", k, v, "export", A, pkg)
        elif isinstance(v, dict) and ("ObjectName" in v or "AssetPathName" in v):
            add("actor", A, name + "_C", k, v.get("ObjectName") or v.get("AssetPathName"), "export", A, pkg, note="reference")
        else:
            add("actor", A, name + "_C", k, v, "export", A, pkg, note="struct value")
    add("actor", A, "BlueprintGeneratedClass", "DeclaredVariables", [c["Name"] for c in gen.get("ChildProperties", [])],
        "export", A, pkg, note="Blueprint-declared variables (ChildProperties); one the CDO does not set has its type default")
    for e in ex:
        p = e.get("Properties") or {}
        if e["Type"] == "BoxComponent":
            add("actor", A, "BoxComponent", "BoxExtent", p.get("BoxExtent", "not set"), "export", A, pkg, unit="cm")
        if e["Type"] == "BHMoverComponent":
            for mm in p.get("MovementModes", []):
                add("mover", A, "BHMoverComponent", "MovementMode.Tag", mm["Key"]["TagName"], "export", A, pkg)
                add("mover", A, "BHMoverComponent", "MovementMode.Class", mm["Value"]["ObjectName"].split("'")[0], "export", A, pkg,
                    note="native class; its constructor values are not in this file")
            add("mover", A, "BHMoverComponent", "StartingMovementMode", p["StartingMovementMode"]["TagName"], "export", A, pkg)
            add("mover", A, "BHMoverComponent", "PersistentSyncStateDataTypes",
                [clsname(s["RequiredType"]["ObjectName"]) for s in p.get("PersistentSyncStateDataTypes", [])], "export", A, pkg)
        if re.match(r"WD.*Move$", e["Type"]):
            if not p:
                add("mover", A, e["Type"], "ModeProperties", "none set", "native-pending", A, pkg,
                    note="the Blueprint stores no override; native constructor values apply")
            for k, v in p.items():
                if isinstance(v, dict) and "ObjectName" in v:
                    add("mover", A, e["Type"], k, v["ObjectName"], "export", A, pkg, note="reference to a settings asset")
                else:
                    add("mover", A, e["Type"], k, v, "export", A, pkg)
        if e["Type"] == "BHCommonMovementSettings":
            add("mover", A, "BHCommonMovementSettings", "SharedSettings", p or "none set", "native-pending", A, pkg,
                note="shared mover settings object; no values stored in the Blueprint")
    for e in ex:
        if e["Type"] == "Function" and e.get("ScriptBytecode"):
            calls, iv = set(), set()
            walk(e["ScriptBytecode"], calls, iv)
            add("bytecode", A, "Function", e["Name"],
                {"statements": len(e["ScriptBytecode"]), "calls": sorted(calls), "instance_variables_read": sorted(iv)},
                "export", A, pkg)


def main():
    a = sys.argv[1:]
    dump = a[a.index("--dump") + 1]
    world = a[a.index("--world") + 1] if "--world" in a else None
    links = da_links()
    for name in PKG:
        for da, dpkg, ps in sorted(links.get(name, [])):
            add("da", da, "WDProjectileData", "ProjectileStats.ProjectileActor", name, "export", da, dpkg)
            for f in DA_FIELDS:
                if f in ps:
                    add("da", da, "WDProjectileData", "ProjectileStats." + f, ps[f], "export", da, dpkg, note="selects actor " + name)
            pd = ps.get("ProjectileDimensions") or {}
            if pd:
                add("da", da, "WDProjectileData", "ProjectileStats.ProjectileDimensions.Mass", pd.get("Mass"), "export", da, dpkg)
                add("da", da, "WDProjectileData", "ProjectileStats.ProjectileDimensions.DragModel.Value",
                    (pd.get("DragModel") or {}).get("Value"), "export", da, dpkg)
        actor(name, dump)
    if world:
        E.extend(json.load(open(os.path.join(world, "world.json"), encoding="utf-8")))
    meta = {"source": "Blueprint projectile actors named by DA_*_ProjectileData, exported with tools/cue4parse_extractor (dump mode; rawfiles mode for the packed .ini), written by _tools/shell_actors.py (round 21)",
            "resolved_from": {"export": "set on the named export",
                              "native-pending": "not set by any Blueprint; the native constructor value applies and is not in this file",
                              "ini": "a Config .ini packed in the game paks",
                              "default": "no override found: the engine default applies"},
            "count": len(E)}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"meta": meta, "entries": E}, f, indent=1)
        f.write("\n")
    print(len(E), "entries")
    return 0


sys.exit(main())
