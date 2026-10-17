"""Collision models for the hitbox viewer: GLBs for the vehicles in assets/data/vehicle-hitboxes.json.

Every variant of a vehicle is assembled; variants whose assemblies are identical (node names, transforms,
material names, vertices) share a file. The file holding the vehicle's first variant is <id>.glb, the
others <id>--<first variant in the file, lowercased, non-alphanumerics as '-'>.glb, and each file lists
its variants in asset.extras.variants (the VV_ names without the prefix) and, when MESH_NOTES has one
for a mesh it places, a note for the viewer in asset.extras.notes.

A variant is assembled the way its modules place their meshes (Wardogs_VehicleDamagePipeline_v1.md §3.1).
damage_tables.assemble() gives the variant's platform and parts. Every enabled
MVF_StaticMesh fragment, and every MVF_DestructibleMeshes entry with bRegisterComplexSurface, places a
render mesh at AttachQuery.SocketName on the component whose tag is AttachQuery.SourceId (usually the
Chassis skeletal mesh). Destructible entries add their RelativeTransform; static-mesh fragments have
none. The render mesh's collision mesh (UStaticMesh.ComplexCollisionMesh) shares the render mesh's local
frame, so the GLB from `WdExtract mesh` for that collision mesh goes at the same transform. The rotor hubs
and blades are destructible entries on the platform, attached to the Chassis bones mainRotorSpin_J and
rearRotorSpin_J.

Transforms. Unreal uses centimetres, +Z up, left-handed (X forward, Y right). The mesh GLBs use
(x, y, z) = (-Y, Z, X) / 100: metres, +Y up, front +Z (manifest.json "axes"). With P that axis map, a UE
transform (R, t) becomes (P R P^T, P t / 100). P is a reflection, so P R P^T is a proper rotation and
stays a quaternion: (x, y, z, w) -> (y, -z, -x, w). Bones are the skeletal mesh's reference pose in
component space. A skeletal-mesh socket adds its RelativeLocation and RelativeRotation (FRotator in
degrees) on its bone. The Chassis component is the actor root, at identity.

Materials: one per collision slot, named as the slot, or "<slot>|<Group>" when the mesh registers
outside ComplexSurface.Group.Default. Untextured: baseColorFactor only. Node names are the
collision-mesh names. node.extras records the render mesh, module, attach point and surface group. The
merged GLB is compressed with meshopt by a pinned glTF-Transform CLI (npx, Node.js needed). Viewers must
supply a meshopt decoder.

    python -I _tools/vehicle_models.py --meshes <vv_mesh_out> [--meshes <more>...] [--skeletons <dir>] [--raw <dir>] [vehicle ids...]

--meshes is the `WdExtract mesh` output: one folder per vehicle with the collision GLBs and a
manifest.json, whose "bones" give the skeletal meshes' bones. --skeletons is optional. It holds
`WdExtract dump` JSON of skeletal meshes, needed only for attach points that are mesh sockets rather than
bones, and <mesh>.refskel.json reference skeletons for meshes the manifest has no bones for. --raw keeps
the uncompressed GLBs. None of these is in the repository.
"""
import glob
import hashlib
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import damage_tables as dt  # noqa: E402

ROOT = dt.ROOT
OUT = os.path.join(ROOT, *dt.MODELS.split("/"))
GLTF_TRANSFORM = "@gltf-transform/cli@4.5.1"
DEFAULT_GROUP = "ComplexSurface.Group.Default"
# UE (X, Y, Z) -> glTF (-Y, Z, X), as in the mesh GLBs.
P = np.array([[0.0, -1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])


# --- transforms (UE space, centimetres, column vectors) -------------------------------------------

def quat_matrix(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def rotator_quat(r):
    """FRotator::Quaternion (degrees: Pitch about Y, Yaw about Z, Roll about X)."""
    sp, cp = math.sin(math.radians(r.get("Pitch", 0)) / 2), math.cos(math.radians(r.get("Pitch", 0)) / 2)
    sy, cy = math.sin(math.radians(r.get("Yaw", 0)) / 2), math.cos(math.radians(r.get("Yaw", 0)) / 2)
    sr, cr = math.sin(math.radians(r.get("Roll", 0)) / 2), math.cos(math.radians(r.get("Roll", 0)) / 2)
    return (cr * sp * sy - sr * cp * cy, -cr * sp * cy - sr * cp * sy, cr * cp * sy - sr * sp * cy, cr * cp * cy + sr * sp * sy)


def trs(q=(0, 0, 0, 1), t=(0, 0, 0), s=(1, 1, 1)):
    m = np.eye(4)
    m[:3, :3] = quat_matrix(q) @ np.diag(s)
    m[:3, 3] = t
    return m


def ftransform(t):
    """FTransform JSON (Rotation XYZW, Translation, Scale3D) -> 4x4."""
    if not t:
        return np.eye(4)
    return trs(tuple(t["Rotation"][k] for k in "XYZW"), tuple(t["Translation"][k] for k in "XYZ"),
               tuple(t.get("Scale3D", {}).get(k, 1.0) for k in "XYZ"))


def to_gltf(m):
    """UE 4x4 (cm) -> glTF translation, rotation quaternion, scale (metres, mesh-GLB axes)."""
    a = m[:3, :3]
    scale = np.linalg.norm(a, axis=0)
    r = P @ (a / scale) @ P.T
    t = P @ m[:3, 3] / 100
    s = np.abs(P) @ scale
    # rotation matrix -> quaternion (Shepperd)
    tr = np.trace(r)
    if tr > 0:
        k = math.sqrt(tr + 1) * 2
        q = ((r[2, 1] - r[1, 2]) / k, (r[0, 2] - r[2, 0]) / k, (r[1, 0] - r[0, 1]) / k, k / 4)
    else:
        i = int(np.argmax(np.diag(r)))
        j, n = (i + 1) % 3, (i + 2) % 3
        k = math.sqrt(1 + r[i, i] - r[j, j] - r[n, n]) * 2
        q = [0.0] * 4
        q[i], q[j], q[n], q[3] = k / 4, (r[j, i] + r[i, j]) / k, (r[n, i] + r[i, n]) / k, (r[n, j] - r[j, n]) / k
    q = np.array(q) / np.linalg.norm(q)
    return [round(float(v), 6) for v in t], [round(float(v), 7) for v in q], [round(float(v), 6) for v in s]


# --- skeletons ------------------------------------------------------------------------------------

def manifest_bones(entry):
    """manifest.json "bones" entry (component space, glTF frame, column-major matrices) -> name -> UE 4x4 (cm)."""
    out = {}
    for b in entry.get("bones", []):
        g = np.array(b["matrix"], float).reshape(4, 4).T
        m = np.eye(4)
        m[:3, :3] = P.T @ g[:3, :3] @ P
        m[:3, 3] = P.T @ g[:3, 3] * 100
        out[b["name"]] = m
    return out


def load_skeleton(skel_dir, mesh_path, bones=None):
    """Bone/socket name -> component-space 4x4 (UE cm) for a skeletal mesh. Bones come from the mesh
    manifest (`bones`) or else <skeletons>/<mesh>.refskel.json (reference pose composed through the
    parents); sockets from the mesh's dump <skeletons>/<mesh>.json (RelativeLocation/Rotation on BoneName)."""
    name = mesh_path.rsplit("/", 1)[-1].split(".")[0]
    out = dict((bones or {}).get(name, {}))
    ref = os.path.join(skel_dir, name + ".refskel.json") if skel_dir else None
    if not out and ref and os.path.exists(ref):
        rs = json.load(open(ref, encoding="utf-8"))
        world = []
        for info, pose in zip(rs["FinalRefBoneInfo"], rs["FinalRefBonePose"]):
            local = ftransform(pose)
            world.append(local if info["ParentIndex"] < 0 else world[info["ParentIndex"]] @ local)
            out[info["Name"]] = world[-1]
    if not out:
        return None
    def sockets(path):
        """Socket exports of a dump: the skeleton's first (USkeleton sockets), then the mesh's own."""
        if not path or not os.path.exists(path):
            return []
        objs = json.load(open(path, encoding="utf-8"))
        mesh = next((o for o in objs if o.get("Type") == "SkeletalMesh"), None)
        skel = (mesh or {}).get("Properties", {}).get("Skeleton", {}).get("ObjectName", "").split("'")[1:2]
        first = sockets(os.path.join(skel_dir, skel[0] + ".json")) if skel else []
        return first + [o for o in objs if o.get("Type") == "SkeletalMeshSocket"]

    for o in sockets(os.path.join(skel_dir, name + ".json") if skel_dir else None):
        p = o.get("Properties", {})
        if p.get("BoneName") in out:
            rel = trs(rotator_quat(p.get("RelativeRotation", {})),
                      tuple(p.get("RelativeLocation", {}).get(k, 0.0) for k in "XYZ"),
                      tuple(p.get("RelativeScale", {}).get(k, 1.0) for k in "XYZ"))
            out[p["SocketName"]] = out[p["BoneName"]] @ rel
    return out


# --- components -----------------------------------------------------------------------------------

def components(module_files):
    """Mesh components the modules create: dicts with tags, mesh, attach (source, socket), rel, group, register."""
    comps = []
    for f in module_files:
        objs = {o.get("Name"): o for o in dt.exports(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for fr in (owner or {}).get("Properties", {}).get("Fragments", []):
            if not fr["Value"].get("bEnabled", True):
                continue
            obj = objs.get(fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'"), {})
            p, kind = obj.get("Properties", {}), obj.get("Type")
            cs = p.get("ComponentSettings", {})
            aq = cs.get("AttachQuery", {})
            base = {"module": os.path.basename(f)[:-5], "fragment": fr["Key"], "tags": set(cs.get("Tags", [])),
                    "source": aq.get("SourceId"), "socket": aq.get("SocketName"), "rel": np.eye(4)}
            if kind == "MVF_SkeletalMesh":
                comps.append(dict(base, kind="skeletal", mesh=p.get("SkeletalMesh", {}).get("AssetPathName"),
                                  register=False, group=None))
            elif kind == "MVF_StaticMesh":
                comps.append(dict(base, kind="static", mesh=p.get("StaticMesh", {}).get("AssetPathName"),
                                  register=p.get("bRegisterComplexSurface", True),
                                  group=dt.tag(p.get("SurfaceGroup")) or DEFAULT_GROUP))
            elif kind == "MVF_DestructibleMeshes":
                gcs = p.get("DestructibleMeshesComponentSettings", {})
                for g in p.get("DestructibleMeshesData", []):
                    for s in g.get("DestructibleMeshesSettings", []):
                        scs = s.get("ComponentSettings", {})
                        saq = scs.get("AttachQuery") or gcs.get("AttachQuery", {})
                        mtype = s.get("MeshType", "").split("::")[-1]
                        comps.append({"module": base["module"], "fragment": f"{fr['Key']}/{dt.tag(s.get('MeshTag'))}",
                                      "tags": set(scs.get("Tags", [])), "kind": "skeletal" if mtype == "SkeletalMesh" else "static",
                                      "source": saq.get("SourceId"), "socket": saq.get("SocketName"),
                                      "rel": ftransform(s.get("RelativeTransform")),
                                      "mesh": (s.get("Mesh") or {}).get("AssetPathName"),
                                      "register": s.get("bRegisterComplexSurface", False),
                                      "group": dt.tag(s.get("SurfaceGroup")) if dt.tag(s.get("SurfaceGroup")) not in (None, "None") else None})
    return comps


WHEEL_GROUP = "ComplexSurface.Group.Wheel"
# Notes for the viewer, by render mesh: a file that places the mesh lists the note in asset.extras.notes.
MESH_NOTES = {
    "SM_WHL_08_TurretHousing": "The turret housing's collision mesh (CC_WHL_08_TurretHousing) is authored in vehicle "
                               "space, but the data attaches it at the turret socket like a socket-local mesh, so its "
                               "hitbox sits about 2 m above the roof. Shown where the data places it; whether the game "
                               "corrects this is not traced.",
    "Browning_Mount_Proxy": "Only the gun mount is shown. The gun's own proxy (CC_Browning_Gun) attaches to a receiver_J "
                            "bone that SK_Browning_Mounted doesn't have, so where the game puts it is not traced.",
}


def wheel_components(module_files):
    """One component per wheel of an MVF_InstancedWheels fragment. The wheels are the WheelSetup entries of
    the vehicle config's AxleDataAssets, in axle order then WheelSetup order. That order is taken as the
    wheel's DataIndex, which the game appends to its IndexedSlotNames (CC_Wheel -> CC_Wheel_0, ...) through
    the instance remap. With every wheel active the remap is the identity; the TyreHealthAttribute check at the
    end of assemble_variant() flags any index that disagrees with the slot map. Each wheel sits at its
    BoneName on the Chassis skeleton. The single WheelMesh is authored for the right side; left wheels are
    mirrored across the bone's XZ plane (bMirrorLeftHanded: class default, not in the export)."""
    configs, frags = [], []
    for f in module_files:
        objs = {o.get("Name"): o for o in dt.exports(f)}
        owner = next((o for o in objs.values() if o.get("Type") in ("ModularVehiclePlatform", "ModularVehiclePart")), None)
        for fr in (owner or {}).get("Properties", {}).get("Fragments", []):
            obj = objs.get(fr["Value"]["Fragment"]["ObjectName"].split(":")[-1].rstrip("'"), {})
            if not fr["Value"].get("bEnabled", True):
                continue
            if obj.get("Type") == "MVF_VehicleConfig":
                configs.append(obj["Properties"]["VehicleConfig"]["AssetPathName"])
            elif obj.get("Type") == "MVF_InstancedWheels":
                frags.append((os.path.basename(f)[:-5], fr["Key"], obj["Properties"]))
    if not frags:
        return [], []
    notes = [f"vehicle configs {configs}: the last one is used"] if len(set(configs)) > 1 else []
    setup = []
    cfg = dt.asset_file(configs[-1]) if configs else None
    for o in dt.exports(cfg) if cfg else []:
        for a in next(dt.walk(o, "AxleDataAssets"), []):
            axle = dt.asset_file(a["ObjectName"].split("'")[-2])
            setup += next((w for x in dt.exports(axle) for w in dt.walk(x, "WheelSetup")), []) if axle else []
    comps = []
    for module, key, p in frags:
        explicit = dt.tag(p.get("SurfaceGroup"))
        per_wheel = p.get("PerWheelSurfaceGroups") or []
        if per_wheel:
            notes.append(f"{key}: PerWheelSurfaceGroups {per_wheel} not applied")
        for i, w in enumerate(setup):
            comps.append({"module": module, "fragment": f"{key}[{i}]", "tags": set(), "kind": "static",
                          "source": None, "root_socket": True, "socket": w["BoneName"], "rel": np.eye(4),
                          "mesh": p["WheelMesh"]["AssetPathName"], "register": p.get("bRegisterComplexSurface", True),
                          "group": explicit if explicit not in (None, "None") else WHEEL_GROUP,
                          "indexed": (set(p.get("IndexedSlotNames", [])), i), "mirror": w["Side"].endswith("Left"),
                          "wheel": {"index": i, "side": w["Side"].split("::")[-1], "bone": w["BoneName"],
                                    "health": dt.tag(w.get("TyreHealthAttribute"))}})
    return comps, notes


def place(comps, skel_dir, bones=None):
    """World (actor-space, UE cm) 4x4 per component; components that cannot be resolved get None and a note.
    AttachQuery.SourceId names the parent by component tag or fragment key; "Mesh" (SourceMode Explicit) is
    the pawn's own mesh, the root Chassis skeletal mesh. Socket names match bones/sockets ignoring case, as
    FNames do."""
    skeletons = {}
    notes = []
    root = next((c for c in comps if c["kind"] == "skeletal" and not c["source"]), None)

    def lookup(sk, name):
        if name in sk:
            return sk[name]
        return {k.lower(): v for k, v in sk.items()}.get(name.lower())

    def frame(c, depth=0):
        if "world" in c:
            return c["world"]
        c["world"] = None
        if not c["source"] and not c.get("root_socket"):
            c["world"] = c["rel"]  # actor root (the Chassis skeletal mesh)
            return c["world"]
        if c.get("root_socket"):
            parent = root
        else:
            cands = [p for p in comps if p is not c and (c["source"] in p["tags"] or p["fragment"] == c["source"])]
            parent = cands[0] if cands else (root if c["source"] == "Mesh" else None)
        if parent is None or depth > 8:
            notes.append(f"{c['fragment']}: no component for source {c['source']}")
            return None
        pw = frame(parent, depth + 1)
        if pw is None:
            return None
        sock = np.eye(4)
        if c["socket"] and c["socket"] != "None":
            if parent["kind"] == "skeletal":
                if parent["mesh"] not in skeletons:
                    skeletons[parent["mesh"]] = load_skeleton(skel_dir, parent["mesh"], bones)
                sk = skeletons[parent["mesh"]]
                if sk is None:
                    notes.append(f"{c['fragment']}: no reference skeleton for {parent['mesh']}")
                    return None
                sock = lookup(sk, c["socket"])
                if sock is None:
                    notes.append(f"{c['fragment']}: {c['socket']} not a bone or socket of {parent['mesh']}")
                    return None
            else:
                notes.append(f"{c['fragment']}: static-mesh socket {c['socket']} on {parent['mesh']} not resolved "
                             "(placed at that mesh's origin)")
        c["world"] = pw @ sock @ c["rel"]
        return c["world"]

    for c in comps:
        frame(c)
    return notes


# --- GLB io ---------------------------------------------------------------------------------------

COMPONENTS = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
WIDTH = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def read_glb(path):
    """[(material name, baseColorFactor, positions (n,3) float32, indices (m,) uint32)] of a mesh GLB's first mesh."""
    with open(path, "rb") as f:
        data = f.read()
    off, gltf, binary = 12, None, b""
    while off < len(data):
        size, kind = struct.unpack_from("<II", data, off)
        chunk = data[off + 8: off + 8 + size]
        if kind == 0x4E4F534A:
            gltf = json.loads(chunk)
        elif kind == 0x004E4942:
            binary = chunk
        off += 8 + size

    def accessor(i):
        a = gltf["accessors"][i]
        v = gltf["bufferViews"][a["bufferView"]]
        dtype, width = COMPONENTS[a["componentType"]], WIDTH[a["type"]]
        start = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        stride = v.get("byteStride")
        item = np.dtype(dtype).itemsize * width
        if stride and stride != item:
            raw = np.frombuffer(binary, np.uint8, count=stride * (a["count"] - 1) + item, offset=start)
            rows = np.lib.stride_tricks.as_strided(raw, (a["count"], item), (stride, 1))
            return np.ascontiguousarray(rows).view(dtype).reshape(a["count"], width)
        return np.frombuffer(binary, dtype, count=a["count"] * width, offset=start).reshape(a["count"], width)

    out = []
    for prim in gltf["meshes"][0]["primitives"]:
        mat = gltf["materials"][prim["material"]] if "material" in prim else {}
        pos = accessor(prim["attributes"]["POSITION"]).astype(np.float32)
        idx = accessor(prim["indices"]).reshape(-1).astype(np.uint32) if "indices" in prim else np.arange(len(pos), dtype=np.uint32)
        out.append((mat.get("name", ""), mat.get("pbrMetallicRoughness", {}).get("baseColorFactor", [0.8, 0.8, 0.8, 1]), pos, idx))
    return out


def write_glb(path, root_name, nodes, asset_extras=None):
    """nodes: [(name, (t, q, s), extras, [(material name, color, positions, indices)])]. Positions stay local."""
    gltf = {"asset": {"version": "2.0", "generator": "_tools/vehicle_models.py"}, "scene": 0,
            "scenes": [{"name": root_name, "nodes": [0]}], "nodes": [{"name": root_name, "children": []}],
            "meshes": [], "materials": [], "accessors": [], "bufferViews": []}
    blob = bytearray()
    materials = {}

    def view(arr, target):
        while len(blob) % 4:
            blob.append(0)
        gltf["bufferViews"].append({"buffer": 0, "byteOffset": len(blob), "byteLength": arr.nbytes, "target": target})
        blob.extend(arr.tobytes())
        return len(gltf["bufferViews"]) - 1

    for name, (t, q, s), extras, prims in nodes:
        mesh = {"name": name, "primitives": []}
        for mname, color, pos, idx in prims:
            if mname not in materials:
                materials[mname] = len(gltf["materials"])
                gltf["materials"].append({"name": mname, "pbrMetallicRoughness": {
                    "baseColorFactor": [round(float(c), 4) for c in color], "metallicFactor": 0.0, "roughnessFactor": 1.0}})
            pos = np.ascontiguousarray(pos, np.float32)
            small = len(pos) < 65536
            ind = np.ascontiguousarray(idx, np.uint16 if small else np.uint32)
            gltf["accessors"].append({"bufferView": view(pos, 34962), "componentType": 5126, "count": len(pos), "type": "VEC3",
                                      "min": [float(v) for v in pos.min(0)], "max": [float(v) for v in pos.max(0)]})
            gltf["accessors"].append({"bufferView": view(ind, 34963), "componentType": 5123 if small else 5125,
                                      "count": len(ind), "type": "SCALAR"})
            n = len(gltf["accessors"])
            mesh["primitives"].append({"attributes": {"POSITION": n - 2}, "indices": n - 1, "material": materials[mname]})
        gltf["meshes"].append(mesh)
        node = {"name": name, "mesh": len(gltf["meshes"]) - 1, "translation": t, "rotation": q}
        if any(abs(v - 1) > 1e-6 for v in s):
            node["scale"] = s
        if extras:
            node["extras"] = extras
        gltf["nodes"].append(node)
        gltf["nodes"][0]["children"].append(len(gltf["nodes"]) - 1)
    while len(blob) % 4:
        blob.append(0)
    if asset_extras:
        gltf["asset"]["extras"] = asset_extras
    gltf["buffers"] = [{"byteLength": len(blob)}]
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(blob)))
        f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        f.write(struct.pack("<II", len(blob), 0x004E4942) + bytes(blob))


# --- assembly -------------------------------------------------------------------------------------

def collision_index(mesh_roots):
    """Over all manifests (earlier roots first): render-mesh name -> (collision mesh name, GLB path),
    render-mesh name -> skip reason, and skeletal-mesh name -> bone matrices (UE space)."""
    found, skipped, bones = {}, {}, {}
    for man in [m for r in mesh_roots for m in sorted(glob.glob(os.path.join(r, "*", "manifest.json")))]:
        m = json.load(open(man, encoding="utf-8"))
        for c in m.get("collisionMeshes", []):
            for r in c.get("renderMeshes", []):
                found.setdefault(r.rsplit("/", 1)[-1], (c["name"], os.path.join(os.path.dirname(man), c["file"])))
        for s in m.get("skipped", []):
            path, _, why = s.partition("	")
            skipped.setdefault(path.rsplit("/", 1)[-1], why)
        for path, entry in m.get("bones", {}).items():
            bones.setdefault(path.rsplit("/", 1)[-1], manifest_bones(entry))
    return found, skipped, bones


def variant_file(name):
    return next(v for v in dt.variants() if os.path.basename(v) == f"VV_{name}.json")


def assemble_variant(vehicle, variant, index, skel_dir):
    """One variant's placed collision meshes: ([(name, (t, q, s), extras, prims)], notes)."""
    found, skipped, bones = index
    modules, missing, _ = dt.assemble(variant_file(variant))
    comps = components(modules)
    wheels, wnotes = wheel_components(modules)
    comps += wheels
    notes = wnotes + place(comps, skel_dir, bones) + [f"module not in data/: {m}" for m in missing]
    nodes, used = [], {}
    # Slot names are FNames, which compare ignoring case (CC_Mainbody hits the CC_MainBody mapping): one
    # spelling per slot, the map's when it has one, else the first seen.
    spelling = {s["slot"].lower(): s["slot"] for s in vehicle["slots"]}
    for c in comps:
        if c["kind"] != "static" or not c["mesh"]:
            continue
        render = c["mesh"].rsplit("/", 1)[-1].split(".")[0]
        if not c["register"]:
            notes.append(f"{render}: bRegisterComplexSurface off, not a hitbox")
            continue
        if render not in found:
            notes.append(f"{render}: {skipped.get(render, 'no collision GLB exported')}")
            continue
        if c.get("world") is None:
            notes.append(f"{render}: placement unresolved, left out")
            continue
        cc, glb = found[render]
        group = c["group"] or DEFAULT_GROUP
        suffix = "" if group == DEFAULT_GROUP else "|" + group.rsplit(".", 1)[-1]
        names, index_ = c.get("indexed", (set(), None))
        prims = []
        for slot, color, pos, idx in read_glb(glb):
            if c.get("mirror"):  # mirror UE Y (glTF x) and keep the faces outward
                pos = pos * np.array([-1, 1, 1], np.float32)
                idx = idx.reshape(-1, 3)[:, ::-1].reshape(-1)
            base = f"{slot}_{index_}" if slot.lower() in {n.lower() for n in names} else slot
            canon = spelling.setdefault(base.lower(), base)
            if canon != base:
                notes.append(f"{cc}: slot {base} named {canon} (same FName)")
            prims.append((canon + suffix, color, pos, idx))
        used[cc] = used.get(cc, 0) + 1
        name = f"{cc}_{index_}" if index_ is not None else (cc if used[cc] == 1 else f"{cc}_{used[cc]}")
        extras = {"render_mesh": render, "module": c["module"],
                  "attach": f"{c['source'] or 'Chassis'}:{c['socket']}" if c["source"] or c.get("root_socket") else None,
                  "surface_group": group}
        if c.get("wheel"):
            extras["wheel"] = dict(c["wheel"], mirrored=c["mirror"])
        nodes.append((name, to_gltf(c["world"]), extras, prims))
    # The wheel index must give the slot the section the axle data names for that wheel (TyreHealthAttribute).
    section = {s["slot"]: s["section"] for s in vehicle["slots"]}
    for c in wheels:
        for slot in sorted(c["indexed"][0]):
            name = f"{slot}_{c['wheel']['index']}"
            if name in section and section[name] != c["wheel"]["health"]:
                notes.append(f"wheel {c['wheel']['index']} ({c['wheel']['bone']}): {name} maps to {section[name]}, "
                             f"the axle data says {c['wheel']['health']}")
    return nodes, notes


def signature(nodes):
    """Content of an assembly: node names, transforms, material names, vertices and indices (not extras)."""
    h = hashlib.sha256()
    for name, trs_, _, prims in nodes:
        h.update(json.dumps([name, trs_, [p[0] for p in prims]]).encode())
        for _, _, pos, idx in prims:
            h.update(np.ascontiguousarray(pos, np.float32).tobytes())
            h.update(np.ascontiguousarray(idx, np.uint32).tobytes())
    return h.hexdigest()


def file_stem(vehicle, variant):
    """<id> for the file holding the vehicle's first variant, else <id>--<variant, lowercased, non-alnum as '-'>."""
    if variant == vehicle["variants"][0]:
        return vehicle["id"]
    return vehicle["id"] + "--" + re.sub(r"[^a-z0-9]+", "-", variant.lower()).strip("-")


def build(vehicle, index, skel_dir, raw_dir):
    """Every variant of one vehicle-hitboxes.json entry, variants with identical assemblies sharing a file.
    Returns [(stem, raw path, variants, report)] in variant order of each file's first variant."""
    files = {}
    for variant in vehicle["variants"]:
        nodes, notes = assemble_variant(vehicle, variant, index, skel_dir)
        entry = files.setdefault(signature(nodes), {"nodes": nodes, "notes": notes, "variants": []})
        entry["variants"].append(variant)
    expected = {s["slot"] + ("" if s["group"] == DEFAULT_GROUP else "|" + s["group"].rsplit(".", 1)[-1])
                for s in vehicle["slots"] if s["slot"] != "(default)"}
    out = []
    for f in files.values():
        stem = file_stem(vehicle, f["variants"][0])
        raw = os.path.join(raw_dir, stem + ".raw.glb")
        asset_extras = {"variants": f["variants"]}
        notes = list(dict.fromkeys(MESH_NOTES[n[2]["render_mesh"]] for n in f["nodes"] if n[2]["render_mesh"] in MESH_NOTES))
        if notes:
            asset_extras["notes"] = notes
        write_glb(raw, vehicle["id"], f["nodes"], asset_extras)
        materials = {p[0] for n in f["nodes"] for p in n[3]}
        out.append((stem, raw, f["variants"], {"nodes": [n[0] for n in f["nodes"]], "notes": f["notes"],
                                               "missing_slots": sorted(expected - materials),
                                               "extra_slots": sorted(materials - expected)}))
    return out


def glb_json(path):
    with open(path, "rb") as fh:
        fh.seek(12)
        size, _ = struct.unpack("<II", fh.read(8))
        return json.loads(fh.read(size))


def compress(raw, out):
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    subprocess.run([npx, "--yes", GLTF_TRANSFORM, "meshopt", raw, out], check=True, capture_output=True, text=True)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]

    def opt(flag, default=None):
        if flag in args:
            i = args.index(flag)
            value = args[i + 1]
            del args[i:i + 2]
            return value
        return default

    mesh_roots = []
    while "--meshes" in args:
        mesh_roots.append(opt("--meshes"))
    skel_dir = opt("--skeletons")
    raw_dir = opt("--raw") or tempfile.mkdtemp(prefix="vehicle_models_")
    if not mesh_roots:
        sys.exit(__doc__)
    vehicles = json.load(open(dt.JSON_OUT, encoding="utf-8"))["vehicles"]
    wanted = set(args)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(raw_dir, exist_ok=True)
    index = collision_index(mesh_roots)
    total = 0
    for v in vehicles:
        if wanted and v["id"] not in wanted:
            continue
        written = set()
        for stem, raw, variants, rep in build(v, index, skel_dir, raw_dir):
            if not rep["nodes"]:
                print(f"{stem}: skipped, no collision meshes placed ({', '.join(variants)})")
                for n in rep["notes"]:
                    print("   ", n)
                continue
            out = os.path.join(OUT, stem + ".glb")
            compress(raw, out)
            if glb_json(out)["asset"].get("extras") != glb_json(raw)["asset"].get("extras"):
                sys.exit(f"{out}: asset.extras lost in compression")
            written.add(stem + ".glb")
            size = os.path.getsize(out)
            total += size
            print(f"{stem}: {', '.join(variants)}: {len(rep['nodes'])} meshes, {size / 1024:.1f} KiB"
                  + ("  OVER THE 1.5 MB BUDGET" if size > 1.5e6 else ""))
            print(f"    slots in the map without geometry: {', '.join(rep['missing_slots']) or 'none'}")
            print(f"    geometry slots not in the map (take the default section): {', '.join(rep['extra_slots']) or 'none'}")
            for n in dict.fromkeys(rep["notes"]):
                print("   ", n)
        for old in glob.glob(os.path.join(OUT, v["id"] + "--*.glb")):  # files of a previous grouping
            if os.path.basename(old) not in written:
                os.remove(old)
                print(f"    removed stale {os.path.basename(old)}")
    print(f"total {total / 1024:.1f} KiB (this run)")


if __name__ == "__main__":
    main()
