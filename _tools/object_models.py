"""Collision models for the object viewer (pipelines/object-viewer.md): buildables, deployables and props.

Writes assets/models/objects/<id>.glb (one per object) and assets/data/object-collision.json. Everything is
collision geometry; no render mesh, texture or image is read or written. Three sources:

* Buildables (the WDBuildableDataAsset definitions, as _tools/buildable_tables.py reads them). Each stage of
  a definition's BuildingStagesDefinition lists static meshes and where they are placed (MeshToPlacements).
  Those meshes carry no collision mesh of their own: their UBodySetup holds simple collision primitives
  (AggGeom: boxes, spheres, sphyls, convex hulls), which `WdExtract collision` exports as cooked. Each
  primitive becomes a closed low-poly shape, placed by its stage placement. A mesh with an empty AggGeom
  (the FOB's stage meshes, the fuel canister, the C4 detonator) collides on its render triangles, which
  are not published; it is listed in the data file without geometry.
* Deployables (AT mine, Claymore, IED, C4, Molotov, smoke grenade): the item's static mesh body, the same way.
* Props with a physics asset (ammo crate, supply crates, the FWG_01 airplane, STN_05's skeletal mesh): the
  bodies of the PhysicsAsset on the skeletal mesh's reference pose, as the infantry model does.

Frame: UE centimetres (X forward, Y right, Z up, left-handed) to glTF metres, (x, y, z) = (-Y, Z, X) / 100,
+Y up, front +Z. Rotations (x, y, z, w) -> (y, -z, -x, w). Shapes are the infantry model's
(_tools/infantry_model.py: capsule, sphere, box, convex). A GLB has one node per placement, one mesh per
static mesh (shared by its placements) with one primitive per collision element, and one material per
(stage, mesh) named "S<n>|<mesh>" (props: "<body>"), baseColorFactor only. The file is compressed with
meshopt by the pinned glTF-Transform CLI (Node.js needed); viewers supply a meshopt decoder.

    python -I _tools/object_models.py --collision <collision.json> --physics <physics.json> [--raw <dir>]
    python -I _tools/object_models.py --plan <out-dir> --files <files.txt>   # writes collision_in.txt, phys_in.txt
    python -I _tools/object_models.py --check          # exit 1 when the written JSON is stale

--collision is `WdExtract collision` run on the buildable and item static meshes, --physics `WdExtract physics`
on the prop physics assets and their skeletal meshes (commands in docs/evidence/round86-models.md). Neither
is in the repository. --check regenerates the data file's buildable stage tables from data/ and compares them
with the written file (the geometry comes from the extraction and is checked by the GLB parse in
_tools/object_models_check.py).
"""
import json
import math
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import buildable_tables as bt  # noqa: E402
import infantry_model as im  # noqa: E402

ROOT = bt.ROOT
OUT_DIR = os.path.join(ROOT, "assets", "models", "objects")
OUT_JSON = os.path.join(ROOT, "assets", "data", "object-collision.json")
EVIDENCE = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round86-models.md"

# buildable definitions that are stationary vehicles: their vehicle model is in the vehicle viewer
VEHICLE_OF = {"DA_Buildable_MGNest": "stationary-mgnest", "DA_Buildable_MistralAA": "stationary-mistral",
              "DA_Buildable_STN_02": "stationary-phalanx", "DA_Buildable_STN_03": "stationary-mortar",
              "DA_Buildable_STN_04": "stationary-radiotower", "DA_Buildable_STN_05": "stationary-stn-05"}

# (id, name, static mesh, actor key in assets/data/explosive-actors.json, notes)
DEPLOYABLES = [
    ("at-mine", "AT Mine", "SM_AT_mine", "AT mine",
     ["Placed actor B_AT_Mine. A landmine placeable explodes when it takes 50 damage (AWDLandminePlaceable, round 17 native read)."]),
    ("claymore", "Claymore", "SM_Claymore", "Claymore",
     ["The mesh's collision uses CTF_UseSimpleAsComplex, so the box is also the trace collision."]),
    ("ied", "IED", "SM_IED_Planted", "IED", []),
    ("c4", "C4 charge", "SM_C4_Explosive", "C4",
     ["B_ThrowableC4: health 30, max detonation distance 100 (round 40 read); the detonator mesh has no simple collision."]),
    ("molotov", "Molotov", "SM_Molotov_01", "Molotov", []),
    ("smoke-grenade", "Smoke grenade", "SM_Smoke_Grenade", None, []),
]

# (id, name, physics asset, skeletal mesh or None, notes)
PROPS = [
    ("ammo-crate", "Ammo crate", "PA_AmmoCrate_01", None,
     ["A single sphyl on root_J. The crate's skeletal mesh is not exported, so the body sits at the origin."]),
    ("supply-crate-small", "Small supply crate", "SK_SupplyCrate_Small_Physics", "SK_SupplyCrate_Small", []),
    ("supply-crate-large", "Large supply crate", "SK_SupplyCrate_Large_Physics", "SK_SupplyCrate_Large", []),
    ("supply-crate-lonestar", "Free supply crate (Lonestar)", "SK_SupplyCrate_Free_Lonestar_Physics", "SK_SupplyCrate_Free_Lonestar", []),
    ("supply-crate-manticore", "Free supply crate (Manticore)", "SK_SupplyCrate_Free_Manticore_Physics", "SK_SupplyCrate_Free_Manticore", []),
    ("supply-crate-valkyra", "Free supply crate (Valkyra)", "SK_SupplyCrate_Free_Valkyra_Physics", "SK_SupplyCrate_Free_Valkyra", []),
    ("airplane-fwg-01", "FWG_01 airplane", "PA_FWG_01", "SK_FWG_01",
     ["Flyable airplane pawn with its own physics asset; it has no row in the vehicle damage tables and no collision meshes, "
      "so it is not in the vehicle viewer."]),
    ("stn-05-physics", "STN_05 skeletal mesh bodies", "PA_STN_05", "SK_STN_05",
     ["These are the bodies of SK_STN_05 (kinematic). The vehicle viewer's STN_05 model is the mortar base collision mesh that the "
      "vehicle platform attaches; this asset is the skeletal mesh's own physics asset."]),
]

PROFILE_KEYS = ("CollisionProfileName", "ObjectType")


# --- transforms ------------------------------------------------------------------------------------

def m_vec(v):
    return [-v["Y"] / 100, v["Z"] / 100, v["X"] / 100]


def m_quat(q):
    return [q["Y"], -q["Z"], -q["X"], q["W"]]


def rotator_quat(r):
    p, y, ro = (math.radians(r.get(k, 0.0)) / 2 for k in ("Pitch", "Yaw", "Roll"))
    sp, cp, sy, cy, sr, cr = math.sin(p), math.cos(p), math.sin(y), math.cos(y), math.sin(ro), math.cos(ro)
    return {"X": cr * sp * sy - sr * cp * cy, "Y": -cr * sp * cy - sr * cp * sy, "Z": cr * cp * sy - sr * sp * cy,
            "W": cr * cp * cy + sr * sp * sy}


def quat_matrix_ue(q):
    x, y, z, w = q["X"], q["Y"], q["Z"], q["W"]
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def local(center, quat_ue):
    return {"translation": m_vec(center), "rotation": m_quat(quat_ue), "scale": [1.0, 1.0, 1.0]}


IDENT = {"X": 0.0, "Y": 0.0, "Z": 0.0, "W": 1.0}


# --- AggGeom elements -> infantry-model shape dicts -------------------------------------------------

def shapes_of(agg):
    """UBodySetup AggGeom (asset-local cm, as cooked) -> shapes in the glTF frame (metres)."""
    out = []
    for i, e in enumerate(agg.get("BoxElems", [])):
        out.append({"type": "box", "name": f"box{i}", "size": [e["Y"] / 100, e["Z"] / 100, e["X"] / 100],
                    "local": local(e["Center"], rotator_quat(e.get("Rotation", {}))) })
    for i, e in enumerate(agg.get("SphereElems", [])):
        out.append({"type": "sphere", "name": f"sphere{i}", "radius": e["Radius"] / 100, "local": local(e["Center"], IDENT)})
    for i, e in enumerate(agg.get("SphylElems", [])):
        out.append({"type": "sphyl", "name": f"sphyl{i}", "radius": e["Radius"] / 100, "length": e["Length"] / 100,
                    "local": local(e["Center"], rotator_quat(e.get("Rotation", {})))})
    for i, e in enumerate(agg.get("TaperedCapsuleElems", [])):
        sys.exit(f"tapered capsule element in the export ({e}): not handled")
    for i, e in enumerate(agg.get("ConvexElems", [])):
        t = e["Transform"]
        s = np.array([t["Scale3D"][k] for k in "XYZ"])
        if (s <= 0).any():
            sys.exit(f"convex element {i}: non-positive scale {s}")
        rot = quat_matrix_ue(t["Rotation"])
        v = np.array([[p["X"], p["Y"], p["Z"]] for p in e["VertexData"]]) * s
        v = v @ rot.T + np.array([t["Translation"][k] for k in "XYZ"])
        g = np.stack([-v[:, 1], v[:, 2], v[:, 0]], axis=1) / 100
        out.append({"type": "convex", "name": f"convex{i}", "vertices": g.tolist(), "indices": e["IndexData"],
                    "local": {"translation": [0.0] * 3, "rotation": [0.0, 0.0, 0.0, 1.0], "scale": [1.0] * 3}})
    return out


def prim_meshes(shapes, what):
    out = []
    for s in shapes:
        pos, idx = im.shape_mesh(s)
        if len(pos) >= 65535:
            sys.exit(f"{what}: {s['name']} has too many vertices")
        if im.signed_volume(pos, idx) <= 0:
            sys.exit(f"{what}: {s['type']} {s['name']}: faces not outward")
        out.append((pos, idx))
    return out


def dims(s):
    r = lambda x: round(float(x), 3)  # noqa: E731
    if s["type"] == "box":
        return {"size_m": [r(v) for v in s["size"]]}
    if s["type"] in ("sphere", "sphyl"):
        d = {"radius_m": r(s["radius"])}
        if s["type"] == "sphyl":
            d["cylinder_length_m"] = r(s["length"])
        return d
    p = np.array(s["vertices"])
    return {"vertices": len(p), "triangles": len(s["indices"]) // 3,
            "extent_m": [r(v) for v in (p.max(0) - p.min(0))]}


# --- GLB --------------------------------------------------------------------------------------------

def write_glb(path, meshes, materials, nodes, extras):
    """meshes: {key: [(pos, idx)]}; materials: [name]; nodes: [(name, mesh key, material index, t, q, s, extras)]."""
    gltf = {"asset": {"version": "2.0", "generator": "_tools/object_models.py", "extras": extras}, "scene": 0,
            "scenes": [{"name": "object", "nodes": [0]}], "nodes": [{"name": "object", "children": []}],
            "meshes": [], "materials": [], "accessors": [], "bufferViews": []}
    blob = bytearray()

    def view(arr, target):
        while len(blob) % 4:
            blob.append(0)
        gltf["bufferViews"].append({"buffer": 0, "byteOffset": len(blob), "byteLength": arr.nbytes, "target": target})
        blob.extend(arr.tobytes())
        return len(gltf["bufferViews"]) - 1

    for name in materials:
        gltf["materials"].append({"name": name, "pbrMetallicRoughness": {
            "baseColorFactor": im.color(name.split("|")[-1]), "metallicFactor": 0.0, "roughnessFactor": 1.0}})
    # one glTF mesh per (static mesh, material): a mesh's primitives share the material of the node using it
    made = {}
    for name, key, mat, t, q, s, ex in nodes:
        if (key, mat) not in made:
            prims = []
            for pos, idx in meshes[key]:
                pos = np.ascontiguousarray(np.round(pos, 5), np.float32)
                ind = np.ascontiguousarray(idx, np.uint16)
                gltf["accessors"].append({"bufferView": view(pos, 34962), "componentType": 5126, "count": len(pos), "type": "VEC3",
                                          "min": [float(v) for v in pos.min(0)], "max": [float(v) for v in pos.max(0)]})
                gltf["accessors"].append({"bufferView": view(ind, 34963), "componentType": 5123, "count": len(ind), "type": "SCALAR"})
                n = len(gltf["accessors"])
                prims.append({"attributes": {"POSITION": n - 2}, "indices": n - 1, "material": mat})
            gltf["meshes"].append({"name": materials[mat], "primitives": prims})
            made[(key, mat)] = len(gltf["meshes"]) - 1
        node = {"name": name, "mesh": made[(key, mat)], "translation": [round(v, 6) for v in t],
                "rotation": [round(v, 7) for v in q], "extras": ex}
        if any(abs(v - 1) > 1e-6 for v in s):
            node["scale"] = [round(v, 6) for v in s]
        gltf["nodes"].append(node)
        gltf["nodes"][0]["children"].append(len(gltf["nodes"]) - 1)
    while len(blob) % 4:
        blob.append(0)
    gltf["buffers"] = [{"byteLength": len(blob)}]
    import struct
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(blob)))
        f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        f.write(struct.pack("<II", len(blob), 0x004E4942) + bytes(blob))


# --- collision export lookup ------------------------------------------------------------------------

def mesh_bodies(collision):
    """static mesh name -> {shapes, profile, trace_flag, package} from `WdExtract collision`."""
    bodies = {b["objectPath"]: b for b in collision["bodies"]}
    out = {}
    for sm in collision["staticMeshes"]:
        b = bodies[sm["bodySetupPath"]]
        props = b["properties"]
        agg = b.get("aggGeom") or {}
        inst = props.get("DefaultInstance", {})
        out[sm["objectPath"].split(".")[-1]] = {
            "shapes": shapes_of(agg),
            "profile": inst.get("CollisionProfileName"),
            "object_type": (inst.get("ObjectType") or "").split("::")[-1],
            "trace_flag": (props.get("CollisionTraceFlag") or "default").split("::")[-1].replace("CTF_", ""),
            "package": sm["assetPath"],
        }
    return out


# --- buildables -------------------------------------------------------------------------------------

def slug(asset):
    return asset.replace("DA_Buildable_", "").replace("DA_", "").lower().replace("_", "-")


def damage_summary(d, p):
    tag = p.get("DamageEntityData", {}).get("Tag", {}).get("TagName")
    row = d["damage"].get(tag) if tag else None
    return {"max_health": p.get("MaxHealth"), "damage_row": tag,
            "modifiers": {c: bt.single(row, t) for c, t in bt.DAMAGE_COLS} if row else None}


IDENTITY_T = {"Rotation": IDENT, "Translation": {"X": 0.0, "Y": 0.0, "Z": 0.0}, "Scale3D": {"X": 1.0, "Y": 1.0, "Z": 1.0}}
# The FOB definition has no stages asset: its foundation is DA_Buildable_FOB.FoundationStaticMesh and its faction
# meshes are named in the Blueprint (not in data/), so they are listed here from the package names. Placed at the
# actor origin; the relative placement is not in data/.
FOB_PIECES = [("Foundation", ["SM_Foundation_FOB"]),
              ("Complete (Lonestar)", ["SM_Buildable_FOB_Stages_Lonestar"]),
              ("Complete (Manticore)", ["SM_Buildable_FOB_Stages_Manticore"]),
              ("Complete (Valkyra)", ["SM_Buildable_FOB_Stages_Valkyra"]),
              ("Destroyed (Lonestar)", ["SM_FOB_Destroyed_Lonestar"]),
              ("Destroyed (Manticore)", ["SM_FOB_Destroyed_Manticore"]),
              ("Destroyed (Valkyra)", ["SM_FOB_Destroyed_Valkyra"])]


def buildable_stages(d, p, asset=None):
    """[{name, progress, meshes: [(mesh name, [placement transform], actor)]}] from the definition's stages."""
    if asset == "DA_Buildable_FOB":
        return [{"name": n, "progress": None, "meshes": [(m, [IDENTITY_T], None) for m in ms]} for n, ms in FOB_PIECES]
    out = []
    for st in bt.stage_list(d, p):
        meshes = []
        for item in st.get("MeshToPlacements", []):
            name = item["Key"].split(".")[-1]
            placements = [pl["RelativeTransform"] for pl in item["Value"].get("Placements", [])]
            meshes.append((name, placements, (item["Value"].get("ActorToSpawn") or {}).get("ObjectName")))
        out.append({"name": st.get("StageName"), "progress": st.get("RequiredBuildingProgress"), "meshes": meshes})
    return out


def node_trs(t):
    return (m_vec(t["Translation"]), m_quat(t["Rotation"]),
            [t["Scale3D"]["Y"], t["Scale3D"]["Z"], t["Scale3D"]["X"]])


def stage_table(d, p, asset=None):
    """The part of an object's record that comes from data/ alone (checked by --check)."""
    return [{"name": s["name"], "progress": s["progress"],
             "meshes": [{"mesh": m, "placements": len(pl), "spawns_actor": actor} for m, pl, actor in s["meshes"]]}
            for s in buildable_stages(d, p, asset)]


def build_buildable(d, rel, asset, typ, p, bodies, raw_dir, records):
    oid = slug(asset)
    stages = buildable_stages(d, p, asset)
    meshes, materials, nodes, stage_rec = {}, [], [], []
    for si, st in enumerate(stages, 1):
        pieces = []
        for mesh, placements, actor in st["meshes"]:
            b = bodies.get(mesh)
            piece = {"mesh": mesh, "placements": len(placements), "spawns_actor": actor}
            if b is None:
                piece["status"] = "mesh not in the collision export"
            elif not b["shapes"]:
                piece["status"] = "no simple collision primitives (any collision uses the render triangles, which are not published)"
                piece.update({"trace_flag": b["trace_flag"], "profile": b["profile"]})
            else:
                key = mesh
                if key not in meshes:
                    meshes[key] = prim_meshes(b["shapes"], mesh)
                mat_name = f"S{si}|{mesh}"
                materials.append(mat_name)
                for pi, t in enumerate(placements):
                    tr, q, sc = node_trs(t)
                    nodes.append((f"{mat_name}#{pi}", key, len(materials) - 1, tr, q, sc, {"stage": si, "mesh": mesh}))
                piece.update({"status": "ok", "material": mat_name, "profile": b["profile"], "object_type": b["object_type"],
                              "trace_flag": b["trace_flag"], "shapes": [{"type": s["type"], **dims(s)} for s in b["shapes"]]})
            pieces.append(piece)
        stage_rec.append({"name": st["name"], "progress": st["progress"], "pieces": pieces})
    rec = {"id": oid, "group": "buildables", "name": bt.display_name(d, p) or asset.replace("DA_Buildable_", ""),
           "asset": asset, "tag": bt.tag_of(p), "cost": p.get("Cost"), **damage_summary(d, p),
           "vehicle_viewer": VEHICLE_OF.get(asset), "stages": stage_rec, "glb": None, "notes": []}
    if not nodes:
        rec["notes"].append("No stage mesh of this definition has simple collision primitives to show.")
    else:
        finish(rec, oid, meshes, materials, nodes, {"object": oid, "source": asset}, raw_dir, records)
    return rec


def finish(rec, oid, meshes, materials, nodes, extras, raw_dir, records):
    raw = os.path.join(raw_dir, oid + ".glb")
    write_glb(raw, meshes, materials, nodes, extras)
    out = os.path.join(OUT_DIR, oid + ".glb")
    im.compress(raw, out)
    gj = im.glb_json(out)
    if gj.get("images") or gj.get("textures") or gj.get("samplers"):
        sys.exit(f"{out}: contains images or textures")
    rec["glb"] = f"assets/models/objects/{oid}.glb"
    rec["glb_bytes"] = os.path.getsize(out)
    records.append(oid)


# --- deployables ------------------------------------------------------------------------------------

def build_deployables(bodies, actors, raw_dir, records):
    out = []
    for oid, name, mesh, actor, notes in DEPLOYABLES:
        b = bodies.get(mesh)
        if b is None:
            sys.exit(f"{mesh} is not in the collision export")
        rec = {"id": oid, "group": "deployables", "name": name, "asset": mesh, "glb": None, "notes": list(notes),
               "blast": (actors.get(actor) or {}).get("damage_values") if actor else None,
               "blast_source": "assets/data/explosive-actors.json" if actor else None,
               "stages": [{"name": "Placed", "progress": None, "pieces": [{
                   "mesh": mesh, "placements": 1, "status": "ok" if b["shapes"] else "no simple collision primitives",
                   "profile": b["profile"], "object_type": b["object_type"], "trace_flag": b["trace_flag"],
                   "material": f"S1|{mesh}", "shapes": [{"type": s["type"], **dims(s)} for s in b["shapes"]]}]}]}
        if b["shapes"]:
            m = {mesh: prim_meshes(b["shapes"], mesh)}
            finish(rec, oid, m, [f"S1|{mesh}"], [(f"S1|{mesh}#0", mesh, 0, [0, 0, 0], [0, 0, 0, 1], [1, 1, 1],
                                                   {"stage": 1, "mesh": mesh})], {"object": oid, "source": mesh}, raw_dir, records)
        else:
            rec["notes"].append("The mesh has no simple collision primitives: any collision uses its render triangles, which are not published.")
        out.append(rec)
    return out


# --- props (physics assets) -------------------------------------------------------------------------

def pick_by_name(items, key, name):
    for it in items:
        if it.get(key, "").split("/")[-1].split(".")[0] == name:
            return it
    return None


def build_props(physics, raw_dir, records):
    out = []
    for oid, name, pa_name, sk_name, notes in PROPS:
        pa = pick_by_name(physics["physicsAssets"], "package", pa_name)
        if pa is None:
            sys.exit(f"{pa_name} is not in the physics export")
        sk = pick_by_name(physics["skeletalMeshes"], "skeletalMesh", sk_name) if sk_name else None
        bones = {b["name"]: b for b in sk["bones"]} if sk else {}
        mats, nodes, meshes, bodies_rec = [], [], {}, []
        for body in pa["bodies"]:
            bone = body["boneName"]
            b = bones.get(bone)
            t = [round(float(v), 6) for v in b["translation"]] if b else [0.0, 0.0, 0.0]
            q = list(im.unit(b["rotation"])) if b else [0.0, 0.0, 0.0, 1.0]
            if sk and not b:
                sys.exit(f"{oid}: bone {bone} not in {sk_name}")
            prims = prim_meshes(body["shapes"], f"{oid} {bone}")
            meshes[bone] = prims
            mats.append(bone)
            nodes.append((bone, bone, len(mats) - 1, t, q, [1, 1, 1], {"bone": bone}))
            pm = body["physMaterialOverride"] or body["physMaterial"]
            bodies_rec.append({"mesh": bone, "placements": 1, "status": "ok", "material": bone,
                               "physics_type": body["physicsType"].split("::")[-1].replace("PhysType_", ""),
                               "trace_flag": body["collisionTraceFlag"].split("::")[-1].replace("CTF_", "").replace(" (default)", ""),
                               "phys_material": pm.split("/")[-1].split(".")[0] if pm else None,
                               "shapes": [{"type": s["type"], **dims(s)} for s in body["shapes"]]})
        rec = {"id": oid, "group": "props", "name": name, "asset": pa_name, "glb": None, "notes": list(notes),
               "stages": [{"name": "Physics asset", "progress": None, "pieces": bodies_rec}]}
        finish(rec, oid, meshes, mats, nodes, {"object": oid, "source": pa_name}, raw_dir, records)
        out.append(rec)
    return out


# --- input lists for WdExtract ---------------------------------------------------------------------

ITEM_DIRS = ("AT_mine", "Claymore", "IED", "C4", "Molotov", "SmokeGrenade", "FuelCanister")
PHYS_PATTERNS = [
    r"Characters/(NPC|First_Playable)/.*/SK_[^/]*$", r"Characters/Player/SK_DefaultCharacter$",
    r"Characters/Default_PlayerMesh/TP/(PA_TPCharacter[^/]*|SK_TP_Male_000)$", r"Characters/Player/Parachute/SK[^/]*$",
    r"Weapons/Utilities/AmmoCrate/PA_[^/]*$", r"FWG_01/Meshes/(PA|SK)_[^/]*$",
    r"SupplyCrates.*/SK_SupplyCrate_[A-Za-z]*$", r"SupplyCrates.*_Physics$", r"SupplyCrate_Free_[A-Za-z]*$", r"STN_05/Content/Mesh/(SK|PA)_STN_05$"]
FOB_RE = r"/(SM_Buildable_FOB_Stages|SM_FOB_Destroyed|SM_Foundation_FOB)[^/]*$"


def plan(out_dir, files_txt):
    """Write collision_in.txt (WdExtract collision) and phys_in.txt (WdExtract physics) from data/ and the package list."""
    import re
    sys.path.insert(0, os.path.join(ROOT, "tools", "cue4parse_extractor"))
    import vehicle_meshes as vm
    pm = vm.package_map(files_txt)
    packages = open(files_txt, encoding="utf-8").read().split()
    d = bt.load()
    col, missing = set(), []
    for rel, asset, typ, p in d["assets"]:
        for st in bt.stage_list(d, p):
            for item in st.get("MeshToPlacements", []):
                key = item["Key"].split(".")[0].lower()
                if key in pm:
                    col.add(pm[key])
                else:
                    missing.append(item["Key"])
    item_re = re.compile(r"/Items/(%s)/.*/SM_[^/]*$" % "|".join(ITEM_DIRS))
    col |= {x for x in packages if item_re.search(x) or re.search(FOB_RE, x)}
    phys = {x for x in packages if any(re.search(pat, x) for pat in PHYS_PATTERNS)}
    # the Mutable preset skeletal meshes are read only for their PhysicsAsset: the first three, as in round 86
    phys |= set(sorted(x for x in packages if re.search(r"Characters/Player/_Presets/.*/SK_[^/]*$", x))[:3])
    os.makedirs(out_dir, exist_ok=True)
    for name, items in (("collision_in.txt", col), ("phys_in.txt", phys)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline=chr(10)) as f:
            f.write(chr(10).join(sorted(items)) + chr(10))
    print(f"collision_in.txt: {len(col)} packages, phys_in.txt: {len(phys)} packages"
          + (f"; {len(missing)} stage meshes not in the package list: {missing[:3]}" if missing else ""))


# --- main -------------------------------------------------------------------------------------------

GROUPS = [{"id": "buildables", "label": "Buildables and fortifications"},
          {"id": "deployables", "label": "Deployables and placed explosives"},
          {"id": "props", "label": "Crates, aircraft and other physics assets"}]


def data_tables(d):
    return {slug(a): stage_table(d, p, a) for rel, a, typ, p in d["assets"]}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]

    def opt(flag):
        if flag in args:
            i = args.index(flag)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return None

    plan_dir = opt("--plan")
    if plan_dir:
        files = opt("--files")
        if not files or args:
            sys.exit(__doc__)
        plan(plan_dir, files)
        return
    check = "--check" in args
    if check:
        args.remove("--check")
        written = json.load(open(OUT_JSON, encoding="utf-8"))
        d = bt.load()
        fresh = data_tables(d)
        have = {o["id"]: [{"name": s["name"], "progress": s["progress"],
                           "meshes": [{"mesh": p["mesh"], "placements": p["placements"], "spawns_actor": p.get("spawns_actor")}
                                      for p in s["pieces"]]} for s in o["stages"]]
                for o in written["objects"] if o["group"] == "buildables"}
        bad = [k for k in fresh if have.get(k) != fresh[k]] + [k for k in have if k not in fresh]
        if bad:
            print("stale or missing in assets/data/object-collision.json:", ", ".join(sorted(set(bad))))
            sys.exit(1)
        print(f"object-collision.json current: {len(have)} buildable stage tables match data/")
        return
    cpath, ppath = opt("--collision"), opt("--physics")
    raw_dir = opt("--raw") or tempfile.mkdtemp(prefix="object_models_")
    if not cpath or not ppath or args:
        sys.exit(__doc__)
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    collision = json.load(open(cpath, encoding="utf-8"))
    physics = json.load(open(ppath, encoding="utf-8"))
    actors = json.load(open(os.path.join(ROOT, "assets", "data", "explosive-actors.json"), encoding="utf-8"))["actors"]
    bodies = mesh_bodies(collision)
    d = bt.load()
    records, objects = [], []
    for rel, asset, typ, p in d["assets"]:
        objects.append(build_buildable(d, rel, asset, typ, p, bodies, raw_dir, records))
    objects += build_deployables(bodies, actors, raw_dir, records)
    objects += build_props(physics, raw_dir, records)
    for old in os.listdir(OUT_DIR):
        if old.endswith(".glb") and old[:-4] not in records:
            os.remove(os.path.join(OUT_DIR, old))
            print("removed stale", old)
    doc = {"meta": {"generator": "python -I _tools/object_models.py --collision <collision.json> --physics <physics.json>",
                    "build": "++Wardogs+Live-CL-516586",
                    "evidence": EVIDENCE,
                    "axes": "metres, +Y up, front +Z; (x, y, z) = (-Y, Z, X)_UE / 100",
                    "scope": "Collision geometry only: simple collision primitives (boxes, spheres, sphyls, convex hulls) of static meshes "
                             "and the bodies of physics assets. No render mesh, texture or image.",
                    "damage_source": "game-features/Wardogs_Buildables_v1.md (DT_GlobalDamage_BuildableData rows); blast values from "
                                     "assets/data/explosive-actors.json"},
           "groups": GROUPS, "objects": objects}
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
        f.write("\n")
    total = sum(o.get("glb_bytes", 0) for o in objects)
    print(f"{len(objects)} objects, {len(records)} GLBs, {total / 1024:.1f} KiB")
    for o in objects:
        if not o["glb"]:
            print("  no geometry:", o["id"])


if __name__ == "__main__":
    main()
