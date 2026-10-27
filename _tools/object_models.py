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
* Blueprint-placed objects (round 91, assets/data/object-blueprints.json from _tools/object_blueprints.py): the FOB's faction
  Blueprints (component transforms resolved along the SCS parent chain), interactable doors and smashable windows (the mesh of the
  door's BHDestruction definition placed by its chunk transform; the window mesh by the Blueprint's relative transform) and the
  STN_05 drone projectile (its root box). Every definition's FoundationStaticMesh is a "Foundation" stage drawn at the origin.
* Props with a physics asset (ammo crate, supply crates, the FWG_01 airplane, STN_05's skeletal mesh): the
  bodies of the PhysicsAsset on the skeletal mesh's reference pose, as the infantry model does.

Frame: UE centimetres (X forward, Y right, Z up, left-handed) to glTF metres, (x, y, z) = (-Y, Z, X) / 100,
+Y up, front +Z. Rotations (x, y, z, w) -> (y, -z, -x, w). Shapes are the infantry model's
(_tools/infantry_model.py: capsule, sphere, box, convex). A GLB has one node per placement, one mesh per
static mesh (shared by its placements) with one primitive per collision element, and one material per
(stage, mesh) named "S<n>|<mesh>" (props: "<body>"), baseColorFactor only. The file is compressed with
meshopt by the pinned glTF-Transform CLI (Node.js needed); viewers supply a meshopt decoder.

    python -I _tools/object_models.py --collision <collision.json> --physics <physics.json> [--raw <dir>]
    python -I _tools/object_models.py --plan <out-dir> --files <files.txt>   # writes collision_in.txt, phys_in.txt, bp_in.txt
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
import re
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import buildable_tables as bt  # noqa: E402
import infantry_model as im  # noqa: E402
import object_blueprints as obp  # noqa: E402

ROOT = bt.ROOT
OUT_DIR = os.path.join(ROOT, "assets", "models", "objects")
OUT_JSON = os.path.join(ROOT, "assets", "data", "object-collision.json")
EVIDENCE = "https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round86-models.md"

# buildable definitions that are stationary vehicles: their vehicle model is in the vehicle viewer
VEHICLE_OF = {"DA_Buildable_MGNest": "stationary-mgnest", "DA_Buildable_MistralAA": "stationary-mistral",
              "DA_Buildable_STN_02": "stationary-phalanx", "DA_Buildable_STN_03": "stationary-mortar",
              "DA_Buildable_STN_04": "stationary-radiotower", "DA_Buildable_STN_05": "stationary-stn-05"}

# Buildables without a DisplayName and without an entity-table name: the parts of the Recon Tower (asset DA_Buildable_CrowsNest)
# are named after the tower, as the player sees it in the shop.
PIECE_NAMES = {"DA_Buildable_CrowsNest_BaseFloor": "Recon Tower base floor", "DA_Buildable_CrowsNest_FirstFloor": "Recon Tower first floor",
               "DA_Buildable_CrowsNest_Roof": "Recon Tower roof"}

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
FOUNDATION_NOTE = ("The foundation mesh is drawn at the buildable's origin: where the game spawns it relative to the buildable is native code "
                   "and not in the exported data.")
# Extra facts about a piece that come from a Blueprint component (FOB): (asset, stage index, mesh) -> {...}
PIECE_EXTRA = {}


def ft_dict(t):
    """A transform record of assets/data/object-blueprints.json -> the Rotation/Translation/Scale3D dict the stage tables use."""
    x, y, z = t["translation_cm"]
    qx, qy, qz, qw = t["rotation_xyzw"]
    sx, sy, sz = t["scale"]
    return {"Rotation": {"X": qx, "Y": qy, "Z": qz, "W": qw}, "Translation": {"X": x, "Y": y, "Z": z}, "Scale3D": {"X": sx, "Y": sy, "Z": sz}}


def foundation_name(p):
    f = p.get("FoundationStaticMesh")
    return f["AssetPathName"].rsplit(".", 1)[1] if f else None


def fob_stages(p):
    """The FOB definition has no stages asset. Each faction Blueprint (B_ForwardOperatingBase_<Faction>, dumped with WdExtract and
    read by _tools/object_blueprints.py) places its meshes with SCS component transforms: the finished base is the faction's stage mesh
    (render only), the invisible BlockAll collision proxies (prefab cubes, cylinders, ramps), the flag and the carried model; the
    destroyed base is the inherited DestroyedMesh component. The foundation is the definition's FoundationStaticMesh."""
    doc = obp.load()
    out = []
    for fac, rec in doc["fob"].items():
        for state, pick in (("Complete", lambda c: c["component"] != "DestroyedMesh"), ("Destroyed", lambda c: c["component"] == "DestroyedMesh")):
            meshes, order = {}, []
            for c in rec["components"]:
                if pick(c) and c["mesh"]:
                    if c["mesh"] not in meshes:
                        meshes[c["mesh"]] = []
                        order.append(c["mesh"])
                    meshes[c["mesh"]].append(c)
            idx = len(out) + 1  # the foundation stage comes first
            for m in order:
                PIECE_EXTRA[("DA_Buildable_FOB", idx, m)] = {
                    "visible": any(c["visible"] for c in meshes[m]), "component_profile": meshes[m][0]["profile"],
                    "components": len(meshes[m])}
            out.append({"name": f"{state} ({fac.replace('LoneStar', 'Lonestar')})", "progress": None,
                        "meshes": [(m, [ft_dict(c["world"]) for c in meshes[m]], None) for m in order]})
    return out


def buildable_stages(d, p, asset=None):
    """[{name, progress, meshes: [(mesh name, [placement transform], actor)]}] from the definition's stages."""
    if asset == "DA_Buildable_FOB":
        out = [{"name": "Foundation", "progress": None, "meshes": [(foundation_name(p), [IDENTITY_T], None)]}]
        return out + fob_stages(p)
    out = []
    for st in bt.stage_list(d, p):
        meshes = []
        for item in st.get("MeshToPlacements", []):
            name = item["Key"].split(".")[-1]
            placements = [pl["RelativeTransform"] for pl in item["Value"].get("Placements", [])]
            meshes.append((name, placements, (item["Value"].get("ActorToSpawn") or {}).get("ObjectName")))
        out.append({"name": st.get("StageName"), "progress": st.get("RequiredBuildingProgress"), "meshes": meshes})
    if foundation_name(p):
        out.append({"name": "Foundation", "progress": None, "meshes": [(foundation_name(p), [IDENTITY_T], None)]})
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
            piece.update(PIECE_EXTRA.get((asset, si - 1, mesh), {}))
            pieces.append(piece)
        stage_rec.append({"name": st["name"], "progress": st["progress"], "pieces": pieces})
    rec = {"id": oid, "group": "buildables", "name": bt.display_name(d, p) or PIECE_NAMES.get(asset) or asset.replace("DA_Buildable_", ""),
           "asset": asset, "tag": bt.tag_of(p), "cost": p.get("Cost"), **damage_summary(d, p),
           "vehicle_viewer": VEHICLE_OF.get(asset), "stages": stage_rec, "glb": None, "notes": []}
    if foundation_name(p):
        rec["notes"].append(FOUNDATION_NOTE)
    if asset == "DA_Buildable_FOB":
        rec["notes"].append("Placements are the Blueprint's component transforms (B_ForwardOperatingBase_<Faction>): the collision proxies are invisible "
                            "BlockAll meshes; the faction stage mesh is the visible base and has no simple collision primitives.")
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



# --- doors, windows, projectiles and loose meshes (round 91) -----------------------------------------

DOOR_NAMES = {
    "B_Door": "Door (base Blueprint)", "BP_InteractableDoor_Apartment": "Apartment door", "BP_InteractableDoor_ApartmentBalcony": "Apartment balcony door",
    "BP_InteractableDoor_ApartmentEntrance": "Apartment entrance door", "BP_InteractableDoor_Buisness": "Business door",
    "BP_InteractableDoor_Office": "Office door", "BP_InteractableDoor_WoodPVC": "Wood and PVC door",
    "BP_Interactable_Commercial_Door_01a_L": "Commercial door, left leaf", "BP_Interactable_Commercial_Door_01a_R": "Commercial door, right leaf",
    "BP_Interactable_Door_Wood_01a": "Wooden door", "BP_Interactable_GarageDoor_01a_Left": "Garage door, left leaf",
    "BP_Interactable_GarageDoor_01a_Right": "Garage door, right leaf", "BP_Interactable_HospitalDoor_01a_Left": "Hospital door, left leaf",
    "BP_Interactable_HospitalDoor_01a_Right": "Hospital door, right leaf"}
WINDOW_NAMES = {
    "B_SmashableWindowMaster": "Smashable window (master template)", "B_SmashableDoorWindow": "Smashable door window",
    "B_SmashableApartmentBalconyDoor": "Smashable apartment balcony door glass", "B_SmashableApartmentBalconyWindow": "Smashable apartment balcony window",
    "B_SmashableApartmentDoubleWindow": "Smashable apartment double window", "B_SmashableApartmentSingleWindow": "Smashable apartment window",
    "B_SmashableHospitalSingleWindow": "Smashable hospital window", "B_SmashableHospitalSingleWindow_03": "Smashable hospital window (variant 03)",
    "B_SmashableHospitalSingleWindow_04": "Smashable hospital window (variant 04)", "B_SmashableLargeWindow": "Smashable large window",
    "B_SmashableWindow_Tower_01a": "Smashable tower window (3 m)", "B_SmashableWindow_Tower_01b": "Smashable tower window (6 m)"}
# static meshes with simple collision that no data asset places (id, name, mesh, notes)
LOOSE_MESHES = [("hblock-mesh", "SM_HBlock (loose H-block mesh)", "SM_HBlock",
                 ["No data asset in the exports references this mesh (the H-block buildables use the SM_HESCO_* stage meshes). It is a "
                  "single convex hull of about 1.5 m on each side with the BlockAll profile."])]

DOOR_BREACH_DEFAULT = ("A door Blueprint that does not set a value keeps the native default of the AWDDoor class, which is not "
                       "in the exports.")


def mesh_piece(mesh, b, placements, mat, **extra):
    """The piece record for a mesh with a collision export entry (or without)."""
    piece = {"mesh": mesh, "placements": placements}
    if b is None:
        piece["status"] = "mesh not in the collision export"
    elif not b["shapes"]:
        piece["status"] = "no simple collision primitives (any collision uses the render triangles, which are not published)"
        piece.update({"trace_flag": b["trace_flag"], "profile": b["profile"]})
    else:
        piece.update({"status": "ok", "material": mat, "profile": b["profile"], "object_type": b["object_type"], "trace_flag": b["trace_flag"],
                      "shapes": [{"type": s["type"], **dims(s)} for s in b["shapes"]]})
    piece.update(extra)
    return piece


def trs_of(t):
    return node_trs(ft_dict(t))


def build_one_mesh_object(oid, group, name, asset, mesh, b, t, raw_dir, records, stage_name, facts, notes, **rec_extra):
    """An object that is one static mesh placed by one transform t (a blueprint transform record, or None for the origin)."""
    mat = f"S1|{mesh}"
    rec = {"id": oid, "group": group, "name": name, "asset": asset, "glb": None, "facts": facts, "notes": notes, **rec_extra,
           "stages": [{"name": stage_name, "progress": None, "pieces": [mesh_piece(mesh, b, 1, mat)]}]}
    if b is not None and b["shapes"]:
        tr, q, sc = trs_of(t) if t else ([0, 0, 0], [0, 0, 0, 1], [1, 1, 1])
        finish(rec, oid, {mesh: prim_meshes(b["shapes"], mesh)}, [mat], [(f"{mat}#0", mesh, 0, tr, q, sc, {"stage": 1, "mesh": mesh})],
               {"object": oid, "source": asset}, raw_dir, records)
    else:
        rec["notes"].append("The mesh has no simple collision primitives: any collision uses its render triangles, which are not published.")
    return rec


def cm(v):
    return f"{v:g} cm ({v / 100:g} m)"


def name_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_doors(doc, bodies, raw_dir, records):
    out = []
    for dr in doc["doors"]:
        bp, mesh = dr["blueprint"], dr["mesh"]
        b = bodies.get(mesh)
        facts = [["Blueprint", bp], ["Definition asset", dr["definition"]], ["Mesh", mesh], ["Frame height", cm(dr["frame_height_cm"])]]
        if dr["frame_thickness_cm"] is not None:
            facts.append(["Frame thickness", cm(dr["frame_thickness_cm"])])
        facts.append(["Leaves in the definition", f"{dr['chunks']} ({dr['chunk_configuration'] or 'native default'})"])
        facts.append(["Sound material", dr["audio_material"]])
        br = dr["max_breach_distances_cm"]
        facts.append(["Explosive breach, largest distance", cm(br["Explosive"]) if "Explosive" in br else "not set (native default)"])
        if dr["can_vehicles_breach"] is not None:
            facts.append(["Vehicles can breach", "yes" if dr["can_vehicles_breach"] else "no"])
        facts.append(["Sprint push", "speed %g, angle %g" % (dr["sprint_push"]["DoorPushSpeedMax"], dr["sprint_push"]["DoorPushSpeedMaxAngle"])
                      if dr["sprint_push"] else "not set (native default)"])
        notes = ["No health value and no damage-table row for this door is in the exported data. A door is a BHDestruction building "
                 "(class AWDDoor, one chunk) that opens and swings; players breach it by sprinting, melee, explosives or vehicles, and the Halligan "
                 "tool spends durability per breach (see the equipment data). " + DOOR_BREACH_DEFAULT,
                 "Closed position: the definition's chunk transform places the mesh (pivot at the hinge). The interaction trigger box "
                 "(not drawn) sits at Y %g, Z %g cm." % (dr["interaction_box"]["location_cm"][1], dr["interaction_box"]["location_cm"][2])]
        out.append(build_one_mesh_object(name_slug(DOOR_NAMES[bp]), "doors", DOOR_NAMES[bp], dr["definition"], mesh, b, dr["chunk"], raw_dir, records,
                                         "Closed", facts, notes))
    return out


def build_windows(doc, bodies, raw_dir, records):
    out = []
    for w in doc["windows"]:
        bp, mesh = w["blueprint"], w["mesh"]
        b = bodies.get(mesh)
        facts = [["Blueprint", bp], ["Glass mesh", mesh]]
        if w["airborne_break_threshold"] is not None:
            facts.append(["Break threshold, airborne", "%g" % w["airborne_break_threshold"]])
            facts.append(["Break threshold, grounded", "%g" % w["grounded_break_threshold"]])
        else:
            facts.append(["Break thresholds", "not set in this Blueprint (native defaults of AWDSmashableWindow, not in the exports)"])
        if w["glass_shard_amount"] is not None:
            facts.append(["Glass shards in the break effect", "%g" % w["glass_shard_amount"]])
        rem = len(w["broken_remains"])
        notes = ["A smashable window has no health value and no damage-table row in the exported data. The class has Normal, Damaged and "
                 "Smashed states and reacts to a hit on its mesh (an OnWindowMeshHit event with the impact impulse); the master Blueprint sets "
                 "movement break thresholds, the only numbers stored.",
                 "The glass mesh's collision profile %s. Broken-remains pieces%s are effects and are not drawn." % (
                     ("is " + b["profile"]) if b else "is unknown", (" (%d components)" % rem) if rem else "")]
        out.append(build_one_mesh_object(name_slug(WINDOW_NAMES[bp]), "doors", WINDOW_NAMES[bp], bp, mesh, b, w["relative"], raw_dir, records,
                                         "Intact", facts, notes))
    return out


def build_drone(doc, raw_dir, records):
    dr = doc["drone"]
    proj = strip_dump(os.path.join(ROOT, "data", "Wardogs", "Plugins", "GameFeatures", "Vehicles", "STN_05", "Content", "Data",
                                   "Projectile", "DA_Drone_ProjectileData.json"))
    ps = proj["Properties"]["ProjectileStats"]
    ex, ey, ez = dr["box_half_extent_cm"]
    shapes = shapes_of({"BoxElems": [{"Center": {"X": 0.0, "Y": 0.0, "Z": 0.0}, "X": 2 * ex, "Y": 2 * ey, "Z": 2 * ez}]})
    mesh = "Box Component"
    rec = {"id": "drone-projectile", "group": "projectiles", "name": "Drone projectile (STN_05)", "asset": dr["blueprint"], "glb": None,
           "max_health": dr["max_health"], "damage_row": None, "blast": ps["DamageValues"],
           "blast_source": "STN_05 DA_Drone_ProjectileData (damage tag %s)" % ps["DamageEntityData"]["Tag"]["TagName"],
           "facts": [["Blueprint", dr["blueprint"]], ["Collision", "root box component, %s x %s x %s cm" % tuple("%g" % (2 * v) for v in (ex, ey, ez))],
                     ["Projectile data", "DA_Drone_ProjectileData (arming delay %g s, lifetime %g s)" % (ps["ArmingDelay"], ps["MaxProjectileLifetime"])]],
           "notes": ["The health is the Blueprint's WDVitality component (base and max 50). The Blueprint has no damage-entity component, so no "
                     "per-caliber damage row applies to the drone itself. The explosion shown is its warhead (DA_Drone_ProjectileData).",
                     "Only the root box is a collision component with a size in the Blueprint. The skeletal mesh SK_Drone_01 (scale 0.7, under the "
                     "NetworkSmoothingComponent), the rotor, trail and first-person meshes are visual; the VFX meshes set the NoCollision profile."],
           "stages": [{"name": "In flight", "progress": None, "pieces": [{
               "mesh": mesh, "placements": 1, "status": "ok", "material": f"S1|{mesh}",
               "shapes": [{"type": s["type"], **dims(s)} for s in shapes]}]}]}
    finish(rec, rec["id"], {mesh: prim_meshes(shapes, mesh)}, [f"S1|{mesh}"],
           [(f"S1|{mesh}#0", mesh, 0, [0, 0, 0], [0, 0, 0, 1], [1, 1, 1], {"stage": 1, "mesh": mesh})],
           {"object": rec["id"], "source": dr["blueprint"]}, raw_dir, records)
    return [rec]


def strip_dump(path):
    """A data/ export (a header line, then JSON, one object or a list): the first object that has Properties."""
    text = open(path, encoding="utf-8").read()
    v = json.loads(text[min(i for i in (text.find("{"), text.find("[")) if i >= 0):])
    return v[0] if isinstance(v, list) else v


def build_loose(bodies, raw_dir, records):
    return [build_one_mesh_object(oid, "props", name, mesh, mesh, bodies.get(mesh), None, raw_dir, records, "Mesh", [], list(notes))
            for oid, name, mesh, notes in LOOSE_MESHES]


# --- input lists for WdExtract ---------------------------------------------------------------------

ITEM_DIRS = ("AT_mine", "Claymore", "IED", "C4", "Molotov", "SmokeGrenade", "FuelCanister")
PHYS_PATTERNS = [
    r"Characters/(NPC|First_Playable)/.*/SK_[^/]*$", r"Characters/Player/SK_DefaultCharacter$",
    r"Characters/Default_PlayerMesh/TP/(PA_TPCharacter[^/]*|SK_TP_Male_000)$", r"Characters/Player/Parachute/SK[^/]*$",
    r"Weapons/Utilities/AmmoCrate/PA_[^/]*$", r"FWG_01/Meshes/(PA|SK)_[^/]*$",
    r"SupplyCrates.*/SK_SupplyCrate_[A-Za-z]*$", r"SupplyCrates.*_Physics$", r"SupplyCrate_Free_[A-Za-z]*$", r"STN_05/Content/Mesh/(SK|PA)_STN_05$"]
FOB_RE = r"/(SM_Buildable_FOB_Stages|SM_FOB_Destroyed|SM_Foundation_FOB)[^/]*$"


def blueprint_mesh_packages(doc):
    """Every static mesh package the Blueprint records name (FOB components, door meshes, window meshes)."""
    out = set()
    for f in doc["fob"].values():
        out |= {c["mesh_package"] for c in f["components"] if c["mesh_package"]}
    out |= {d["mesh_package"] for d in doc["doors"]}
    for w in doc["windows"]:
        out.add(w["mesh_package"])
    return out


def plan(out_dir, files_txt):
    """Write collision_in.txt (WdExtract collision), phys_in.txt (WdExtract physics) and bp_in.txt (WdExtract dump) from data/ and the package list."""
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
    col |= {x for x in packages if item_re.search(x) or re.search(FOB_RE, x) or re.search(r"/SM_HBlock$", x)}
    # foundations: every definition's FoundationStaticMesh (round 91)
    for rel, asset, typ, p in d["assets"]:
        f = p.get("FoundationStaticMesh")
        if f:
            key = f["AssetPathName"].rsplit(".", 1)[0].lower()
            if key in pm:
                col.add(pm[key])
            else:
                missing.append(f["AssetPathName"])
    # Blueprint-placed meshes (FOB, doors, windows): the packages named in assets/data/object-blueprints.json, which
    # `object_blueprints.py <dump-dir>` writes from the dump of bp_in.txt. Absent on the first pass.
    bp_note = ""
    if os.path.exists(obp.OUT):
        for pkg in blueprint_mesh_packages(obp.load()):
            if pkg.lower() in pm:
                col.add(pm[pkg.lower()])
            else:
                missing.append(pkg)
    else:
        bp_note = "; object-blueprints.json not found: run the dump of bp_in.txt and object_blueprints.py, then plan again"
    bp = {x for x in packages if re.search(obp.BP_PACKAGE_RE, x)}
    unique = {}
    for x in bp:
        unique.setdefault(x.rsplit("/", 1)[1], []).append(x)
    dup = {k: v for k, v in unique.items() if len(v) > 1}
    if dup:
        sys.exit(f"Blueprint names in more than one package: {dup}")
    phys = {x for x in packages if any(re.search(pat, x) for pat in PHYS_PATTERNS)}
    # the Mutable preset skeletal meshes are read only for their PhysicsAsset: the first three, as in round 86
    phys |= set(sorted(x for x in packages if re.search(r"Characters/Player/_Presets/.*/SK_[^/]*$", x))[:3])
    os.makedirs(out_dir, exist_ok=True)
    for name, items in (("collision_in.txt", col), ("phys_in.txt", phys), ("bp_in.txt", bp)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline=chr(10)) as f:
            f.write(chr(10).join(sorted(items)) + chr(10))
    print(f"collision_in.txt: {len(col)} packages, phys_in.txt: {len(phys)} packages, bp_in.txt: {len(bp)} Blueprints"
          + (f"; {len(missing)} meshes not in the package list: {missing[:3]}" if missing else "") + bp_note)


# --- main -------------------------------------------------------------------------------------------

GROUPS = [{"id": "buildables", "label": "Buildables and fortifications"},
          {"id": "deployables", "label": "Deployables and placed explosives"},
          {"id": "props", "label": "Crates, aircraft and other physics assets"},
          {"id": "doors", "label": "Doors and windows"},
          {"id": "projectiles", "label": "Projectiles"}]


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
        names = {o["id"]: o["name"] for o in written["objects"] if o["group"] == "buildables"}
        want = {slug(a): bt.display_name(d, p) or PIECE_NAMES.get(a) or a.replace("DA_Buildable_", "") for rel, a, typ, p in d["assets"]}
        bad += [k + " (name)" for k in want if names.get(k) != want[k]]
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
    bpdoc = obp.load()
    objects += build_loose(bodies, raw_dir, records)
    objects += build_doors(bpdoc, bodies, raw_dir, records)
    objects += build_windows(bpdoc, bodies, raw_dir, records)
    objects += build_drone(bpdoc, raw_dir, records)
    ids = [o["id"] for o in objects]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate object ids: " + ", ".join(sorted({i for i in ids if ids.count(i) > 1})))
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
