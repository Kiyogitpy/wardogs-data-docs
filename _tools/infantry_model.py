"""Collision model for the infantry hitbox viewer: assets/models/infantry/player.glb.

The player character (B_WDMoverPlayerCharacter) is hit on the bodies of its mesh component's physics asset.
CharacterMesh.SkeletalMesh is SK_DefaultCharacter, whose PhysicsAsset is PA_TPCharacter_Simplified; the
Mutable object that builds the runtime mesh (MUT_TP_Character) names the same physics asset on its reference
mesh SK_TP_Male_000. This script turns that physics asset into one GLB: one node, one mesh and one material
per body, all named exactly as the body's bone. Shapes become low-poly closed meshes: a sphyl a capsule, a
tapered capsule the hull of its two end spheres, a sphere a UV sphere, a box a box, a convex element its hull
triangles. There is no render geometry, texture or image: materials carry a baseColorFactor only.

Frame. The bodies are placed on the reference pose of SK_DefaultCharacter (component space), then turned by
the mesh component's RelativeRotation (Yaw -90) so the character faces the actor's forward. Axes are those of
the vehicle models: (x, y, z) = (-Y, Z, X)_UE / 100, metres, +Y up, the character facing +Z. The origin is the
mesh component's origin, at the feet; the actor (capsule centre) is 0.96 m above it (RelativeLocation Z -96).
In the uncompressed file each node's translation and rotation are its bone's frame and the mesh is in that
frame; meshopt's quantization then folds a scale and offset into each node, so read world positions, not
node transforms, from the published file. phys_material (asset.extras.bodies, node.extras) is the body's
PhysMaterialOverride, else its PhysMaterial.

UE conventions used: a sphyl's Length is its cylinder part and runs along the element's local Z; a tapered
capsule has Radius0 at +Z and Radius1 at -Z (in this asset that puts the thick end at the joint on all six
of them); box X, Y, Z are full extents. Rotations map as q -> (y, -z, -x, w) under the axis change.

    python -I _tools/infantry_model.py --physics <physics.json> [--raw <dir>]

--physics is the output of `WdExtract physics` run on PA_TPCharacter_Simplified and SK_DefaultCharacter
(tools/cue4parse_extractor/README.md); it may hold other assets too. --raw keeps the uncompressed GLB. Neither
is in the repository. The GLB is compressed with meshopt by a pinned glTF-Transform CLI (npx, Node.js needed);
viewers supply a meshopt decoder. The same input gives a byte-identical file.
"""
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "models", "infantry", "player.glb")
GLTF_TRANSFORM = "@gltf-transform/cli@4.5.1"
PHYSICS_ASSET = "/Game/Characters/Default_PlayerMesh/TP/PA_TPCharacter_Simplified"
SKELETAL_MESH = "/Game/Characters/Player/SK_DefaultCharacter"
# CharacterMesh.RelativeRotation Yaw -90 (UE quaternion (0, 0, -sin 45, cos 45)) in glTF axes: +90 degrees about +Y.
COMPONENT_ROTATION = (0.0, math.sqrt(0.5), 0.0, math.sqrt(0.5))
SEGMENTS = 12          # around a capsule or sphere axis
CAP_RINGS = 3          # latitude rings per capsule end, pole excluded
SPHERE_RINGS = 6       # latitude bands of a sphere
NOTES = [
    "Hit-trace bodies: PA_TPCharacter_Simplified is the PhysicsAsset of SK_DefaultCharacter (B_WDMoverPlayerCharacter"
    " CharacterMesh.SkeletalMesh) and of SK_TP_Male_000, the reference mesh of MUT_TP_Character that builds the"
    " runtime mesh. CharacterMesh.BodyInstance.CollisionEnabled is QueryOnly (profile Custom).",
    "Ragdoll uses a different asset: DA_WDRagdollMovement.PhysicsAsset is PA_TPCharacter_Simplified_Physics. It is"
    " not shown here.",
    "Reference pose of SK_DefaultCharacter; in game the bodies follow the animated bones.",
    "Origin at the feet (mesh component origin); the actor origin is 0.96 m higher. Facing +Z.",
    "Helmets: MUT_TP_Character also lists five helmet physics assets (PA_Helmet_*), each with one body on head."
    " Whether Mutable merges them into the runtime physics asset is not visible in the cooked data; they are not shown.",
]


# --- transforms (glTF axes) -----------------------------------------------------------------------

def quat_matrix(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def quat_mul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def unit(q):
    n = math.sqrt(sum(v * v for v in q))
    q = tuple(v / n for v in q)
    return q if q[3] >= 0 else tuple(-v for v in q)


# --- shapes (element frame, glTF axes: a capsule's axis is local +Y) ------------------------------

def capsule(r_top, r_bottom, length):
    """Hull of two spheres on the local Y axis: radius r_top at +length/2, r_bottom at -length/2."""
    h = length / 2
    # The tangent cone meets both spheres at the same latitude a (from the equator, towards +Y).
    a = math.asin(max(-1.0, min(1.0, (r_bottom - r_top) / length))) if length > 0 else 0.0
    rings = []  # (centre y, radius, latitude), bottom pole to top pole
    for k in range(CAP_RINGS):
        rings.append((-h, r_bottom, -math.pi / 2 + (a + math.pi / 2) * (k + 1) / CAP_RINGS))
    for k in range(CAP_RINGS):
        rings.append((h, r_top, a + (math.pi / 2 - a) * k / CAP_RINGS))
    return revolve([(-h, r_bottom)], rings, [(h, r_top)])


def sphere(r):
    rings = [(0.0, r, -math.pi / 2 + math.pi * k / SPHERE_RINGS) for k in range(1, SPHERE_RINGS)]
    return revolve([(0.0, r)], rings, [(0.0, r)])


def revolve(bottom, rings, top):
    """Rings of SEGMENTS vertices around +Y between two poles; faces wind counter-clockwise seen from outside."""
    (by, br), (ty, tr) = bottom[0], top[0]
    pos = [(0.0, by - br, 0.0)]
    for cy, r, lat in rings:
        for s in range(SEGMENTS):
            t = 2 * math.pi * s / SEGMENTS
            pos.append((r * math.cos(lat) * math.cos(t), cy + r * math.sin(lat), -r * math.cos(lat) * math.sin(t)))
    pos.append((0.0, ty + tr, 0.0))
    idx, top_i = [], len(pos) - 1
    ring = lambda k, s: 1 + k * SEGMENTS + s % SEGMENTS  # noqa: E731
    for s in range(SEGMENTS):
        idx += [0, ring(0, s + 1), ring(0, s)]
        idx += [top_i, ring(len(rings) - 1, s), ring(len(rings) - 1, s + 1)]
        for k in range(len(rings) - 1):
            a, b, c, d = ring(k, s), ring(k, s + 1), ring(k + 1, s), ring(k + 1, s + 1)
            idx += [a, b, d, a, d, c]
    return np.array(pos), np.array(idx)


def box(size):
    sx, sy, sz = (v / 2 for v in size)
    pos = np.array([(x, y, z) for x in (-sx, sx) for y in (-sy, sy) for z in (-sz, sz)])
    # vertex i = 4 * (x > 0) + 2 * (y > 0) + (z > 0); each face counter-clockwise seen from outside
    quads = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return pos, np.array([i for a, b, c, d in quads for i in (a, b, c, a, c, d)])


def convex(shape):
    pos = np.array(shape["vertices"], float)
    idx = np.array(shape["indices"], int)
    if len(idx) == 0:
        sys.exit(f"convex element {shape['name']}: no IndexData in the export")
    # The vertices were mapped by the det -1 axis change: reverse each triangle to keep it outward.
    return pos, idx.reshape(-1, 3)[:, ::-1].reshape(-1)


def shape_mesh(shape):
    kind = shape["type"]
    if kind == "sphyl":
        pos, idx = capsule(shape["radius"], shape["radius"], shape["length"])
    elif kind == "taperedCapsule":
        pos, idx = capsule(shape["radius0"], shape["radius1"], shape["length"])
    elif kind == "sphere":
        pos, idx = sphere(shape["radius"])
    elif kind == "box":
        pos, idx = box(shape["size"])
    elif kind == "convex":
        pos, idx = convex(shape)
    else:
        sys.exit(f"unsupported shape {kind}")
    loc = shape["local"]
    if any(abs(s - 1) > 1e-6 for s in loc["scale"]):
        pos = pos * np.array(loc["scale"])
    pos = pos @ quat_matrix(loc["rotation"]).T + np.array(loc["translation"])
    return pos, idx


def signed_volume(pos, idx):
    t = pos[idx.reshape(-1, 3)]
    return float(np.einsum("ij,ij->i", t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6)


def color(name):
    """Stable colour per bone name (FNV-1a hue, as the vehicle slots); the viewer recolours anyway."""
    h = 2166136261
    for ch in name:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    hue, s, v = (h % 360) / 360, 0.55, 0.85

    def f(k):
        x = (k + hue * 6) % 6
        return v - v * s * max(0, min(x, 4 - x, 1))
    return [round(f(5), 4), round(f(3), 4), round(f(1), 4), 1.0]


# --- GLB ------------------------------------------------------------------------------------------

def write_glb(path, nodes, asset_extras):
    """nodes: [(bone, translation, rotation, extras, [(positions, indices)])]; one mesh and material per node."""
    gltf = {"asset": {"version": "2.0", "generator": "_tools/infantry_model.py", "extras": asset_extras}, "scene": 0,
            "scenes": [{"name": "player", "nodes": [0]}], "nodes": [{"name": "player", "children": []}],
            "meshes": [], "materials": [], "accessors": [], "bufferViews": []}
    blob = bytearray()

    def view(arr, target):
        while len(blob) % 4:
            blob.append(0)
        gltf["bufferViews"].append({"buffer": 0, "byteOffset": len(blob), "byteLength": arr.nbytes, "target": target})
        blob.extend(arr.tobytes())
        return len(gltf["bufferViews"]) - 1

    for bone, t, q, extras, prims in nodes:
        gltf["materials"].append({"name": bone, "pbrMetallicRoughness": {
            "baseColorFactor": color(bone), "metallicFactor": 0.0, "roughnessFactor": 1.0}})
        mesh = {"name": bone, "primitives": []}
        for pos, idx in prims:
            pos = np.ascontiguousarray(np.round(pos, 5), np.float32)
            ind = np.ascontiguousarray(idx, np.uint16)
            gltf["accessors"].append({"bufferView": view(pos, 34962), "componentType": 5126, "count": len(pos), "type": "VEC3",
                                      "min": [float(v) for v in pos.min(0)], "max": [float(v) for v in pos.max(0)]})
            gltf["accessors"].append({"bufferView": view(ind, 34963), "componentType": 5123, "count": len(ind), "type": "SCALAR"})
            n = len(gltf["accessors"])
            mesh["primitives"].append({"attributes": {"POSITION": n - 2}, "indices": n - 1, "material": len(gltf["materials"]) - 1})
        gltf["meshes"].append(mesh)
        gltf["nodes"].append({"name": bone, "mesh": len(gltf["meshes"]) - 1, "translation": t, "rotation": q, "extras": extras})
        gltf["nodes"][0]["children"].append(len(gltf["nodes"]) - 1)
    while len(blob) % 4:
        blob.append(0)
    gltf["buffers"] = [{"byteLength": len(blob)}]
    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(blob)))
        f.write(struct.pack("<II", len(js), 0x4E4F534A) + js)
        f.write(struct.pack("<II", len(blob), 0x004E4942) + bytes(blob))


def glb_json(path):
    with open(path, "rb") as fh:
        fh.seek(12)
        size, _ = struct.unpack("<II", fh.read(8))
        return json.loads(fh.read(size))


def compress(raw, out):
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    subprocess.run([npx, "--yes", GLTF_TRANSFORM, "meshopt", raw, out], check=True, capture_output=True, text=True)


# --- build ----------------------------------------------------------------------------------------

def pick(items, package):
    for it in items:
        if it.get("package", "").replace("Wardogs/Content/", "/Game/").split(".")[0] == package:
            return it
    sys.exit(f"{package} is not in the physics export")


def build(physics):
    pa = pick(physics["physicsAssets"], PHYSICS_ASSET)
    sk = pick(physics["skeletalMeshes"], SKELETAL_MESH)
    if sk["physicsAsset"].split(".")[0] != PHYSICS_ASSET:
        sys.exit(f"{SKELETAL_MESH} names {sk['physicsAsset']}, not {PHYSICS_ASSET}")
    bones = {b["name"]: b for b in sk["bones"]}
    rot = quat_matrix(COMPONENT_ROTATION)
    nodes, bodies = [], []
    for body in pa["bodies"]:
        name = body["boneName"]
        if name not in bones:
            sys.exit(f"body {name}: bone not in {SKELETAL_MESH}")
        b = bones[name]
        t = [round(float(v), 6) for v in rot @ np.array(b["translation"])]
        q = [round(v, 7) for v in unit(quat_mul(COMPONENT_ROTATION, b["rotation"]))]
        prims = []
        for shape in body["shapes"]:
            pos, idx = shape_mesh(shape)
            vol = signed_volume(pos, idx)
            if vol <= 0:
                sys.exit(f"{name} {shape['type']} {shape['name']}: signed volume {vol}, faces not outward")
            prims.append((pos, idx))
        pm = body["physMaterialOverride"] or body["physMaterial"]
        pm = pm.split("/")[-1].split(".")[0] if pm else None
        enabled = sorted({s["collisionEnabled"].split("::")[-1] for s in body["shapes"]})
        extras = {"shapes": [s["type"] for s in body["shapes"]], "phys_material": pm, "collision_enabled": enabled,
                  "physics_type": body["physicsType"].split("::")[-1], "collision_response": body["collisionResponse"].split("::")[-1]}
        nodes.append((name, t, q, extras, prims))
        bodies.append({"bone": name, "shapes": [s["type"] for s in body["shapes"]], "phys_material": pm})
    bare = [b["bone"] for b in bodies if not b["phys_material"]]
    notes = NOTES + ([f"{', '.join(bare)}: no PhysMaterialOverride and no PhysMaterial (phys_material null), so the"
                      " engine's default physical material applies; every other body names its own."] if bare else [])
    extras = {"physics_asset": PHYSICS_ASSET, "skeletal_mesh": SKELETAL_MESH, "bodies": bodies, "notes": notes}
    return nodes, extras


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]

    def opt(flag):
        if flag in args:
            i = args.index(flag)
            value = args[i + 1]
            del args[i:i + 2]
            return value
        return None

    src = opt("--physics")
    raw_dir = opt("--raw") or tempfile.mkdtemp(prefix="infantry_model_")
    if not src or args:
        sys.exit(__doc__)
    with open(src, encoding="utf-8") as f:
        physics = json.load(f)
    nodes, extras = build(physics)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    raw = os.path.join(raw_dir, "player.glb")
    write_glb(raw, nodes, extras)
    compress(raw, OUT)
    if glb_json(OUT)["asset"].get("extras") != extras:
        sys.exit(f"{OUT}: asset.extras lost in compression")
    counts = {}
    for b in extras["bodies"]:
        for s in b["shapes"]:
            counts[s] = counts.get(s, 0) + 1
    tris = sum(len(i) // 3 for *_, prims in nodes for _, i in prims)
    print(f"player.glb: {len(nodes)} bodies, shapes {dict(sorted(counts.items()))}, {tris} triangles, "
          f"{os.path.getsize(OUT) / 1024:.1f} KiB (raw {os.path.getsize(raw) / 1024:.1f} KiB)")


if __name__ == "__main__":
    main()
