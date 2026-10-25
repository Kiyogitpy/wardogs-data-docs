#!/usr/bin/env python3
"""Round 38 buildables: build assets/data/buildable-semantics.json from the exported data.

Reads only files under data/ and assets/data/native-defaults.json. Idempotent: the output is
rewritten with sorted, stable content.

  python -I _tools/buildable_semantics.py            write assets/data/buildable-semantics.json
  python -I _tools/buildable_semantics.py --check    assert the key values (exit 1 on mismatch)

Per buildable data asset: whether the final stage is overridden, the spawner class, the placement
flags and stack limit (explicit value or native default), the weak-spot flag and counts per stage,
the sub-actors the final stage spawns, and the placement conditions. Also the hammer weak-spot
settings, the two placement conditions that were Blueprint-only before and the Drill Rig settings.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GF = os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures")
OUT = os.path.join(ROOT, "assets", "data", "buildable-semantics.json")

# EWDPlacementFlags (sdk/raw/BuildablesRuntime_structs.hpp)
FLAG_BITS = [(1, "AllowRotation"), (2, "CanBeBuiltOn"), (4, "CanPlaceVertically"), (8, "CanPlaceOnBuildables")]


def load(path):
    """Load one exported asset (several JSON objects, possibly behind '--- export' header lines)."""
    text = open(path, encoding="utf-8").read()
    dec = json.JSONDecoder()
    out, i = [], 0
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


def first(path, typ):
    for o in load(path):
        if isinstance(o, dict) and o.get("Type") == typ:
            return o.get("Properties", {})
    return None


def cls(ref):
    """Short class name from an object reference."""
    if isinstance(ref, dict):
        ref = ref.get("ObjectName", "")
    ref = ref or ""
    return ref.split("'")[1] if "'" in ref else ref


def native_defaults():
    d = json.load(open(os.path.join(ROOT, "assets", "data", "native-defaults.json"), encoding="utf-8"))
    return {e["property"]: e["value"] for e in d["entries"] if e["class"] == "UWDBuildableDataAsset"}


def flag_names(v):
    return [n for b, n in FLAG_BITS if v & b]


def stage_def(da_props):
    ref = da_props.get("BuildingStagesDefinition")
    if not ref:
        return None
    name = cls(ref)
    hits = glob.glob(os.path.join(GF, "**", name + ".json"), recursive=True)
    return first(hits[0], "BuildingStagesDefinition") if hits else None


def buildables(nd):
    rows = []
    for f in sorted(glob.glob(os.path.join(GF, "**", "DA_Buildable*.json"), recursive=True)):
        if f.endswith("_Stages.json"):
            continue
        objs = load(f)
        da = next((o for o in objs if o.get("Type") in ("WDBuildableDataAsset", "WDBuildableHotZoneMagnetDataAsset")), None)
        if not da:
            continue
        p = da["Properties"]
        spawn = next((o for o in objs if "Spawner" in o.get("Type", "")), None)
        sp = (spawn or {}).get("Properties", {})
        sd = stage_def(p)
        stages = sd["Stages"] if sd else []
        last = stages[-1] if stages else None
        final_actors = []
        if last:
            for m in last["MeshToPlacements"]:
                v = m["Value"]
                if v.get("ActorToSpawn"):
                    final_actors.append(cls(v["ActorToSpawn"]))
        flags = p.get("PlacementFlags", nd["PlacementFlags"])
        conds = [cls(c) for c in p.get("PlacementConditions", [])]
        rows.append({
            "asset": os.path.basename(f)[:-5],
            "id": (p.get("EntityTag") or {}).get("TagName"),
            "name": (p.get("DisplayName") or {}).get("SourceString"),
            "overridesFinalStage": bool(p.get("bOverridesFinalStage", False)),
            "spawnerBaseClass": cls(sp.get("BaseBuildableClass")) if sp else None,
            "instantFinish": bool(p.get("bInstantFinish", False)),
            "placementFlags": flags,
            "placementFlagsExplicit": "PlacementFlags" in p,
            "placementFlagNames": flag_names(flags),
            "maxStack": p.get("MaxStack", nd["MaxStack"]),
            "maxStackExplicit": "MaxStack" in p,
            "stackCheckOffset": p.get("StackCheckOffset", nd["StackCheckOffset"]),
            "usesCriticalHitSpots": bool(p.get("bUsesCriticalHitSpots", nd["bUsesCriticalHitSpots"])),
            "criticalSpotsPerStage": [len(s["CriticalHitSpots"]) for s in stages],
            "stageCount": len(stages),
            "finalStageSpawnedActors": final_actors,
            "registersWithFob": bool(p.get("bRegisterWithFOB", nd["bRegisterWithFOB"])),
            "placementConditions": conds,
            "hasSafeZoneCondition": "B_SafeZonePlacementCondition_C" in conds,
            "hasLadderCondition": "B_WithinLadderBoundsPlacementCondition_C" in conds,
        })
    return rows


def hammers():
    out = {}
    for h in ("Small", "Medium", "Large"):
        f = os.path.join(GF, "Items", "Buildables", "Content", "Data", h + "Hammer", "ID_" + h + "Hammer.json")
        bt = first(f, "WDItemExtensionData_BuildTool")
        cs = first(f, "WDItemExtensionData_CriticalHitSpotManager")
        out[h] = {
            "buildAmountPerHit": bt["BuildAmount"],
            "weakSpotBuildAmountOnHit": cs["BuildAmountWhenTargetIsHit"],
            "weakSpotMaxDistanceFromView": cs["CriticalHitSpotMaxDistanceAwayFromPlayerView"],
            "weakSpotMaxDegreesAwayFromCameraAtSpawn": cs["CriticalHitSpotMaxDegreesFacingAwayFromCameraAtSpawn"],
            "constructTraceDistance": bt["MaxConstructTraceDistance"],
        }
    return out


def drill():
    f = os.path.join(GF, "Items", "Buildables", "Content", "Data", "Buildables", "Hotzone_Magnet", "DA_Buildable_HotzoneMagnet.json")
    p = first(f, "WDBuildableHotZoneMagnetDataAsset")
    return {k: p[k] for k in ("InitialDelayDuration", "HotZoneMagnetRechargeDuration", "HotZoneMagnetMinimumFuel",
                              "HotZoneMagnetDurationPerFuel", "MaxFuel", "Cost", "MaxHealth")}


def build():
    nd = native_defaults()
    bl = buildables(nd)
    return {
        "_about": "Generated by _tools/buildable_semantics.py (round 38). Do not edit by hand.",
        "placementFlagBits": {str(b): n for b, n in FLAG_BITS},
        "nativeDefaults": {k: nd[k] for k in ("PlacementFlags", "MaxStack", "StackCheckOffset", "bUsesCriticalHitSpots",
                                              "bRegisterWithFOB")},
        "placementConditions": {
            "B_SafeZonePlacementCondition_C": {"MinDistanceToSafezone": 300.0, "unit": "Unreal units (cm)"},
            "B_WithinLadderBoundsPlacementCondition_C": {"BlockRadius": 100.0, "unit": "Unreal units (cm)"},
        },
        "hammerWeakSpots": hammers(),
        "drillRig": drill(),
        "buildables": sorted(bl, key=lambda r: r["asset"]),
    }


def main():
    data = build()
    if "--check" in sys.argv:
        b = {r["asset"]: r for r in data["buildables"]}
        ov = sorted(r["name"] for r in data["buildables"] if r["overridesFinalStage"])
        assert len(ov) == 6, ov
        assert b["DA_Buildable_FOB"]["placementFlags"] == 1 and b["DA_Buildable_FOB"]["placementFlagNames"] == ["AllowRotation"]
        assert b["DA_Buildable_Radio"]["placementFlags"] == 9
        assert b["DA_Buildable_HBlock"]["placementFlags"] == 11 and not b["DA_Buildable_HBlock"]["placementFlagsExplicit"]
        assert b["DA_Buildable_Door"]["maxStack"] == 2
        assert data["hammerWeakSpots"]["Large"]["weakSpotBuildAmountOnHit"] == 8.0
        assert data["drillRig"]["HotZoneMagnetDurationPerFuel"] == 0.03
        print("ok")
        return 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", os.path.relpath(OUT, ROOT), len(data["buildables"]), "buildables")
    return 0


if __name__ == "__main__":
    sys.exit(main())
