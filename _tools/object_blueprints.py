"""Blueprint-defined placements for the object viewer (round 91): FOB faction meshes, interactable doors,
smashable windows and the STN_05 drone projectile.

The Blueprints are not in data/. They are dumped with `WdExtract dump` (the package list is written by
`object_models.py --plan`), and this script reads the dump folder and writes assets/data/object-blueprints.json,
which _tools/object_models.py then reads. The JSON is committed; the dumps are not.

    python -I _tools/object_blueprints.py [<dump-dir>]        # default round91_models/dump1; writes assets/data/object-blueprints.json
    python -I _tools/object_blueprints.py --check             # exit 1 when the JSON disagrees with data/

What is read:
* FOB (B_ForwardOperatingBase_{LoneStar,Manticore,Valkyra}): every StaticMeshComponent of the SimpleConstructionScript with its
  relative transform, resolved through the parent chain to the actor root with Unreal's FTransform composition
  (scale multiplies, a child's translation is scaled by the parent's scale, then rotated). DestroyedMesh is inherited from
  B_ForwardOperatingBase; the faction Blueprint's override record supplies its mesh.
* Doors (BP_Interactable*, BP_InteractableDoor_*, B_Door): the door's Blueprint defaults (a property absent from the dump keeps
  the native default of AWDDoor, which is not in the dump) and its BHDestruction definition asset in data/ (the door mesh,
  its pivot and the chunk transform that places it).
* Windows (B_Smashable*): WindowMesh and its relative transform, the movement break thresholds of the parent class.
* Drone (BP_Drone_Projectile): the root BoxComponent extent, the vitality, the skeletal mesh transform.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "data", "object-blueprints.json")
# the permanent copy of the extraction output (not in the repository)
EXTRACT = "E:/Reverse_Engineer/wardogs_analysis/round91_models"
DEFAULT_DUMP = EXTRACT + "/dump1"
DOORS_DIR = os.path.join(ROOT, "data", "Wardogs", "Content", "GameMechanics", "WorldInteractable", "Objects",
                         "EnvironmentalObjects", "Doors")

FACTIONS = ["LoneStar", "Manticore", "Valkyra"]
FOB_BASE = "B_ForwardOperatingBase"
DOOR_BPS = ["B_Door", "BP_InteractableDoor_Apartment", "BP_InteractableDoor_ApartmentBalcony", "BP_InteractableDoor_ApartmentEntrance",
            "BP_InteractableDoor_Buisness", "BP_InteractableDoor_Office", "BP_InteractableDoor_WoodPVC",
            "BP_Interactable_Commercial_Door_01a_L", "BP_Interactable_Commercial_Door_01a_R", "BP_Interactable_Door_Wood_01a",
            "BP_Interactable_GarageDoor_01a_Left", "BP_Interactable_GarageDoor_01a_Right",
            "BP_Interactable_HospitalDoor_01a_Left", "BP_Interactable_HospitalDoor_01a_Right"]
WINDOW_BPS = ["B_SmashableWindowMaster", "B_SmashableDoorWindow", "B_SmashableApartmentBalconyDoor", "B_SmashableApartmentBalconyWindow",
              "B_SmashableApartmentDoubleWindow", "B_SmashableApartmentSingleWindow", "B_SmashableHospitalSingleWindow",
              "B_SmashableHospitalSingleWindow_03", "B_SmashableHospitalSingleWindow_04", "B_SmashableLargeWindow",
              "B_SmashableWindow_Tower_01a", "B_SmashableWindow_Tower_01b"]
DRONE_BP = "BP_Drone_Projectile"
# Blueprint packages `object_models.py --plan` writes to bp_in.txt (matched on the end of the package path)
BP_PACKAGE_RE = (r"/(%s)$" % "|".join([FOB_BASE] + [f"{FOB_BASE}_{f}" for f in FACTIONS] + DOOR_BPS + WINDOW_BPS + [DRONE_BP]))
# the Blueprint's mesh parts that are not collision proxies: flag, in-hand model and decals
IDENT_T = {"Rotation": {"X": 0.0, "Y": 0.0, "Z": 0.0, "W": 1.0}, "Translation": {"X": 0.0, "Y": 0.0, "Z": 0.0},
           "Scale3D": {"X": 1.0, "Y": 1.0, "Z": 1.0}}


def dump(dir_, name):
    with open(os.path.join(dir_, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def by_name(exports):
    return {e["Name"]: e for e in exports}


def cdo(exports):
    c = [e for e in exports if e["Name"].startswith("Default__")]
    if len(c) != 1:
        sys.exit("expected one class default object")
    return c[0].get("Properties", {})


def mpath(obj):
    """ObjectPath "/Game/X/SM_A.1" -> /Game/X/SM_A (the package, for the pak listing)."""
    return obj["ObjectPath"].rsplit(".", 1)[0] if obj else None


def short(obj):
    """ObjectName "StaticMesh'SM_X'" -> SM_X."""
    return obj["ObjectName"].split("'")[1].split(":")[-1] if obj else None


# --- FTransform --------------------------------------------------------------------------------------

def rot_quat(r):
    """Unreal FRotator (degrees) -> quaternion, as FRotator::Quaternion."""
    p, y, ro = (math.radians(r.get(k, 0.0)) / 2 for k in ("Pitch", "Yaw", "Roll"))
    sp, cp, sy, cy, sr, cr = math.sin(p), math.cos(p), math.sin(y), math.cos(y), math.sin(ro), math.cos(ro)
    return (cr * sp * sy - sr * cp * cy, -cr * sp * cy - sr * cp * sy, cr * cp * sy - sr * sp * cy, cr * cp * cy + sr * sp * sy)


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def qrot(q, v):
    x, y, z, w = q
    # v' = v + 2w(q x v) + 2 q x (q x v)
    tx, ty, tz = 2 * (y * v[2] - z * v[1]), 2 * (z * v[0] - x * v[2]), 2 * (x * v[1] - y * v[0])
    return (v[0] + w * tx + (y * tz - z * ty), v[1] + w * ty + (z * tx - x * tz), v[2] + w * tz + (x * ty - y * tx))


def vec(v, default):
    return (v["X"], v["Y"], v["Z"]) if v else default


def local_t(props):
    """(translation, quaternion, scale) of a component's relative transform; absent properties keep the identity."""
    return (vec(props.get("RelativeLocation"), (0.0, 0.0, 0.0)), rot_quat(props.get("RelativeRotation") or {}),
            vec(props.get("RelativeScale3D"), (1.0, 1.0, 1.0)))


def compose(child, parent):
    """FTransform child * parent (apply child, then parent): scale multiplies, translation is scaled by the parent then rotated."""
    (ct, cq, cs), (pt, pq, ps) = child, parent
    scaled = tuple(a * b for a, b in zip(ct, ps))
    r = qrot(pq, scaled)
    return (tuple(r[i] + pt[i] for i in range(3)), qmul(pq, cq), tuple(a * b for a, b in zip(cs, ps)))


def rd(v, n=5):
    return [round(x, n) + 0.0 for x in v]


def t_json(t):
    return {"translation_cm": rd(t[0], 3), "rotation_xyzw": rd(t[1], 6), "scale": rd(t[2], 5)}


# --- FOB -----------------------------------------------------------------------------------------------

def scs_nodes(exports):
    """{InternalVariableName: {component props, parent (name or None), template name}} for a Blueprint's SCS."""
    names = by_name(exports)
    nodes, parent_of = {}, {}
    for e in exports:
        if e["Type"] != "SCS_Node":
            continue
        p = e["Properties"]
        var = p["InternalVariableName"]
        tmpl = p["ComponentTemplate"]["ObjectName"].split(":")[-1].rstrip("'")
        nodes[var] = {"node": e["Name"], "template": tmpl, "props": names.get(tmpl, {}).get("Properties", {}),
                      "class": p["ComponentClass"]["ObjectName"].split("'")[1], "parent_name": p.get("ParentComponentOrVariableName"),
                      "children": [c["ObjectName"].split(".")[-1].rstrip("'") for c in p.get("ChildNodes", [])]}
    node_var = {n["node"]: v for v, n in nodes.items()}
    for v, n in nodes.items():
        for c in n["children"]:
            parent_of[node_var[c]] = v
    for v, n in nodes.items():
        n["parent"] = parent_of.get(v) or n["parent_name"]
    return nodes


def fob_faction(dir_, faction):
    base_name = FOB_BASE
    bp = f"{FOB_BASE}_{faction}"
    ex, bex = dump(dir_, bp), dump(dir_, base_name)
    nodes, bnodes = scs_nodes(ex), scs_nodes(bex)
    # inherited components: the faction Blueprint's override record (a *_GEN_VARIABLE component named in the dump) over the base's
    inherited = {}
    for v, n in bnodes.items():
        tmpl = by_name(ex).get(v + "_GEN_VARIABLE")
        inherited[v] = {"props": {**n["props"], **(tmpl or {}).get("Properties", {})}, "class": n["class"], "parent": n["parent"]}
    if "DestroyedMesh" not in inherited:
        sys.exit("DestroyedMesh not found in the base Blueprint")

    def comp(v):
        return nodes[v] if v in nodes else inherited[v]

    def parent(v):
        p = comp(v)["parent"]
        return None if p in (None, "DefaultSceneRoot") else p

    def world(v):
        t = local_t(comp(v)["props"])
        p = parent(v)
        return compose(t, world(p)) if p else t

    out = []
    for v in list(nodes) + ["DestroyedMesh"]:
        c = comp(v)
        if c["class"] != "StaticMeshComponent":
            continue
        pr = c["props"]
        body = pr.get("BodyInstance") or {}
        chain, p = [], parent(v)
        while p:
            chain.append(p)
            p = parent(p)
        out.append({"component": v, "mesh": short(pr.get("StaticMesh")), "mesh_package": mpath(pr.get("StaticMesh")), "parent": chain[0] if chain else None,
                    "relative": t_json(local_t(pr)), "world": t_json(world(v)), "visible": pr.get("bVisible", True),
                    "profile": body.get("CollisionProfileName"), "scs": v in nodes})
    return {"blueprint": bp, "components": sorted(out, key=lambda c: (c["mesh"] or "", c["component"]))}


# --- doors -----------------------------------------------------------------------------------------------

def strip_header(text):
    return json.loads(text[text.index("{"):])


def door_definition(def_name):
    with open(os.path.join(DOORS_DIR, def_name + ".json"), encoding="utf-8") as f:
        p = strip_header(f.read())["Properties"]
    if len(p["RequiredMeshes"]) != 1 or len(p["ChunkData"]) != 1:
        sys.exit(f"{def_name}: expected one mesh and one chunk")
    m, c = p["RequiredMeshes"][0], p["ChunkData"][0]
    tr = c["Transform"]
    t = ((tr["Translation"]["X"], tr["Translation"]["Y"], tr["Translation"]["Z"]),
         (tr["Rotation"]["X"], tr["Rotation"]["Y"], tr["Rotation"]["Z"], tr["Rotation"]["W"]),
         (tr["Scale3D"]["X"], tr["Scale3D"]["Y"], tr["Scale3D"]["Z"]))
    return {"mesh": short(m["StaticMesh"]), "mesh_package": mpath(m["StaticMesh"]), "mesh_center_cm": rd(vec(m["MeshCenter"], (0, 0, 0)), 3), "chunk": t_json(t),
            "chunks": len(p["ChunkData"])}


def tagname(v):
    return v.get("TagName") if isinstance(v, dict) else v


def door(dir_, bp):
    ex = dump(dir_, bp)
    p = cdo(ex)
    names = by_name(ex)
    box = [e for e in ex if e["Type"] == "BoxComponent" and e["Name"] == "Box"][0].get("Properties", {})
    d_name = short(p["BuildingDefinitionAsset"])
    rec = {"blueprint": bp, "definition": d_name, "decorator": short(p["BuildingDecoratorDefinitionAsset"]),
           "frame_height_cm": p.get("FrameHeight"), "frame_thickness_cm": p.get("FrameThickness"), "frame_width_cm": p.get("FrameWidth"),
           "chunk_configuration": (p.get("DoorChunkConfiguration") or "").split("::")[-1] or None,
           "audio_material": tagname(p.get("DoorTypeContextTag")),
           "max_breach_distances_cm": {k["Key"].split("::")[-1]: k["Value"] for k in p.get("MaxBreachDistances", [])},
           "can_vehicles_breach": p.get("bCanVehiclesBreach"), "push_radius_buffer_cm": p.get("PushRadiusBuffer"),
           "sprint_push": p.get("SprintPushParams"),
           "interaction_box": {"location_cm": rd(vec(box.get("RelativeLocation"), (0, 0, 0)), 2), "scale": rd(vec(box.get("RelativeScale3D"), (1, 1, 1)), 3)}}
    rec.update(door_definition(d_name))
    return rec


# --- windows ---------------------------------------------------------------------------------------------

def window(dir_, bp):
    ex = dump(dir_, bp)
    names = by_name(ex)
    wm = names["WindowMesh"]["Properties"]
    p = cdo(ex)
    remains = []
    for e in ex:
        if e["Type"] == "StaticMeshComponent" and e["Name"].startswith("BrokenRemains"):
            pr = e.get("Properties", {})
            if pr.get("StaticMesh"):
                remains.append({"mesh": short(pr["StaticMesh"]), "mesh_package": mpath(pr["StaticMesh"]),
                                "profile": (pr.get("BodyInstance") or {}).get("CollisionProfileName")})
    return {"blueprint": bp, "mesh": short(wm["StaticMesh"]), "mesh_package": mpath(wm["StaticMesh"]),
            "relative": t_json(local_t(wm)), "y_forward_mesh": p.get("YForwardMesh"),
            "airborne_break_threshold": p.get("AirborneMovementBreakThreshold"),
            "grounded_break_threshold": p.get("GroundedMovementBreakThreshold"), "smashed_lifespan": p.get("SmashedLifespan"),
            "glass_shard_amount": p.get("GlassShard_Amount"), "broken_remains": remains}


# --- drone ----------------------------------------------------------------------------------------------

def drone(dir_):
    ex = dump(dir_, DRONE_BP)
    names = by_name(ex)
    box = names["Box Component"]["Properties"]["BoxExtent"]
    vit = names["WDVitality_GEN_VARIABLE"]["Properties"]
    sk = names["SK_Drone_01_GEN_VARIABLE"]["Properties"]
    p = cdo(ex)
    return {"blueprint": DRONE_BP, "box_half_extent_cm": [box["X"], box["Y"], box["Z"]], "box_is_root": short(p["RootComponent"]) == "Box Component",
            "base_health": vit.get("BaseHealth"), "max_health": vit.get("MaxHealth"),
            "skeletal_mesh": short(sk["SkeletalMesh"]), "skeletal_mesh_relative": t_json(local_t(sk)),
            "mesh_parent": "NetworkSmoothingComponent (a SceneComponent attached to the box)",
            "projectile_data": "STN_05/Content/Data/Projectile/DA_Drone_ProjectileData"}


def build(dir_):
    return {"meta": {"generator": "python -I _tools/object_blueprints.py <dump-dir>", "build": "++Wardogs+Live-CL-516586",
                     "frame": "Unreal centimetres (X forward, Y right, Z up); rotation quaternions (x, y, z, w) in Unreal's frame",
                     "note": "Transforms are Unreal FTransform compositions of the Blueprint's relative transforms along the SCS parent chain."},
            "fob": {f: fob_faction(dir_, f) for f in FACTIONS},
            "doors": [door(dir_, b) for b in DOOR_BPS], "windows": [window(dir_, b) for b in WINDOW_BPS], "drone": drone(dir_)}


def load():
    with open(OUT, encoding="utf-8") as f:
        return json.load(f)


def check():
    """The committed JSON against data/: each door's definition asset (mesh, pivot, chunk transform)."""
    doc = load()
    bad = []
    for d in doc["doors"]:
        fresh = door_definition(d["definition"])
        for k in ("mesh", "mesh_package", "mesh_center_cm", "chunk", "chunks"):
            if fresh[k] != d[k]:
                bad.append(f"{d['blueprint']}.{k}")
    if bad:
        print("stale in assets/data/object-blueprints.json:", ", ".join(bad))
        sys.exit(1)
    print(f"object-blueprints.json current: {len(doc['doors'])} door definitions match data/")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if args == ["--check"]:
        check()
        return
    if len(args) > 1:
        sys.exit(__doc__)
    doc = build(args[0] if args else DEFAULT_DUMP)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote", OUT, f"({sum(len(v['components']) for v in doc['fob'].values())} FOB components, {len(doc['doors'])} doors, {len(doc['windows'])} windows)")


if __name__ == "__main__":
    main()
