---
title: Gepard cooked Chaos payload decoding
nav_exclude: true
---

# Gepard cooked Chaos payload decoding

The targeted Gepard export contains 13 BodySetup records, 11 cooked payloads and seven distinct payload hashes. The offline decoder consumes every byte of all 11 payloads. All five collision-mesh triangle sets match their corresponding raw CC GLB triangles as **unoriented surfaces**, including material slot names, within an explicit coordinate tolerance. A separate ordered check finds opposite winding on all 2,682 triangles after mapping into the same glTF frame. This establishes the decoded geometry and remaps for these frozen artifacts, not oriented collision parity. It does not establish which shapes or query filters the target activates, their placed pose, or explosion gameplay parity.

No cooked payload, decoded vertex array, or other raw geometry is stored in this repository. All paths below refer to local evidence outside the checkout.

## Evidence and restart

The evidence root is `E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019`:

| Artifact | Relative path |
|---|---|
| Exported BodySetup metadata and binary payloads | `cooked-v2/collision.json`, alongside its referenced `.bin` files |
| Original parsed package exports | `dump/` |
| Standalone decoder | `chaos-decode-v1/decode_chaos.py` |
| Final decode and comparison report | `chaos-decode-v1/decoded-verified/report.json` |
| Decoded resources | `chaos-decode-v1/decoded-verified/<payload-sha256>.decoded.json` |
| Negative validation results | `chaos-decode-v1/validation.json` |
| Separate winding audit and per-face correspondences | `chaos-decode-v1/audit_winding.py`, `chaos-decode-v1/winding-v1.json` |

The raw collision GLBs used for comparison are in `E:/Reverse_Engineer/wardogs_analysis/vv_mesh_out/land-tracked-tnk-01-antiair/CC_TNK_03_*.glb`. These are the raw component exports, rather than the assembled viewer models.

The following command records the successful decode configuration. **Choose a new output directory for each rerun**: the decoder refuses an existing directory rather than overwriting evidence. The final report also records the input manifest hash, decoder hash, raw GLB hashes and individual schema-source hashes.

```powershell
python -I E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/chaos-decode-v1/decode_chaos.py `
  --manifest E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/cooked-v2/collision.json `
  --out E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/chaos-decode-v1/decoded-verified `
  --raw-glb-dir E:/Reverse_Engineer/wardogs_analysis/vv_mesh_out/land-tracked-tnk-01-antiair `
  --raw-dump-dir E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/dump `
  --ue-source E:/UE_5.7 `
  --cue-source E:/WardogsConversion/CUE4Parse/CUE4Parse
```

| Artifact | SHA-256 |
|---|---|
| `decode_chaos.py` | `d14c54d801f2b699b6d4dc1dcba2c82700e7f663e425b442e19e38cc6e8ccf7d` |
| `cooked-v2/collision.json` | `11215210b1cab96a61cc9977f04dbfbd56951bf939c5a9b31a3a9f14b7e106e5` |
| `decoded-verified/report.json` | `f3afbcdfc3be2a1424ee19cc29b4448b679c85f60fb2e9ad7849b9c5a4f90914` |
| `validation.json` | `b7875e3cd3fbffe64223cc1e07591aae7093a031500a39b9247b8eab15b7110c` |
| `audit_winding.py` | `279b7070d3837c96d6a2064fd364e931b81ab412e24896b0f60a7f53e1ef1f0d` |
| `winding-v1.json` | `9ddcb6d2e9b132598df15c17e5e1908508df2e6e9c96d36c9ad3af1a73cebd84` |

## Target and schema provenance

The target exports are from Wardogs `++Wardogs+Live-CL-516586`. The local source at `E:/UE_5.7` identifies itself as UE 5.7.4, CL 51494982, compatible CL 47537391, branch `++UE5+Release-5.7`. These are different build identities. Local UE source supplies serialization hypotheses; full byte consumption, structural validation and independent GLB comparisons support the observed layout in the target payloads. This is not general Chaos version negotiation or future-build support.

The consulted CUE4Parse checkout is `E:/WardogsConversion/CUE4Parse`, HEAD `0415fe26eeba66ac0d814c2547b098219682066f`. Individual file hashes in the report are the reproducible identities if that checkout has local modifications. Its convex/archive serializers helped establish pointer and topology layouts; its triangle-mesh factory branch does not supply the complete decoder used here.

The main local UE schema anchors, relative to `E:/UE_5.7`, are:

| Source | Relevant serialization |
|---|---|
| `Engine/Source/Runtime/Engine/Private/PhysicsEngine/Experimental/ChaosDerivedData.cpp`, lines 104–118; `ChaosDerivedDataReader.cpp` in the same directory | Precision, simple resources, complex resources, UV information and final face-remap order |
| `Engine/Source/Runtime/Experimental/Chaos/Public/Chaos/ChaosArchive.h` | Pointer existence flag, object tag and implicit type |
| `Engine/Source/Runtime/Experimental/Chaos/Private/Chaos/ImplicitObject.cpp`, lines 337–360 | Convex flag, collision flag and collision type |
| `Engine/Source/Runtime/Experimental/Chaos/Public/Chaos/TriangleMeshImplicitObject.h`, approximately lines 275, 380 and 618–724 | BVH, index buffer and triangle-mesh field order |
| `Engine/Source/Runtime/Experimental/Chaos/Public/Chaos/Convex.h`, approximately lines 911–1015; adjacent `ConvexStructureData.h` and `ConvexHalfEdgeStructureData.h` | Convex planes, vertices, topology and mass properties |
| `Engine/Source/Runtime/Engine/Classes/PhysicsEngine/BodySetup.h`, lines 44–64 | UV indices, double-precision positions and UV channels |

For example, the reader source hashes to `e578466f1a1d99e3a6248f5d29279a64c82acb4b762d0878506745fbff8ea85d`, `TriangleMeshImplicitObject.h` to `528fa3404fada90754aa2924986ff67ed833d9ccf44986be39ba1d267d132171`, and `Convex.h` to `88a5648349e8c00228c611fb864b8ed3e62ea4081f98726b19290fd90cdd53b7`. The report contains the complete source list and hashes.

## Observed binary layout

All offsets are decimal byte offsets, zero based; ranges end exclusively. Array offsets in the tables include the signed 32-bit element count. The data is little endian. Geometry coordinates remain Unreal asset/body-local centimetres; no component or bone placement has been applied.

The payload begins with signed 32-bit precision `4`, then a counted simple-implicit array and a counted complex-implicit array. Precision `4` is a scalar width, not an engine version. No embedded custom-version table was observed in these blobs. The supported layout is the observed modern branch, with convex implicit type `8` and triangle-mesh type `11`; other types and unsupported layouts fail.

For a pure complex payload, the initial fields are:

| Offset | Field | Observed value |
|---|---|---|
| 0 | Precision, int32 | 4 |
| 4 | Simple resource count, int32 | 0 |
| 8 | Complex resource count, int32 | 1 |
| 12 | Pointer exists, bool stored as int32 | 1 |
| 16 | Object tag, int32 | 0 |
| 20 | Implicit type, uint8 | 11 |
| 21 | Is convex, bool32 | 0 |
| 25 | Do collide, bool32 | 0 |
| 29 | Collision type, uint8 | 11 |
| 30 | Particles serialized, bool32 | 1 |
| 34 | Vertex count, int32 | Varies |
| 38 | Vertex data | XYZ float32 |

After vertices come a bool32 large-index flag (`0` in every observed mesh), a triangle count and uint16 index triplets. Subsequent fields are six float32 AABB values; a counted fast-BVH node array; per-face bounds; uint16 material indices; int32 external face and vertex maps; UV data; and the final BodySetup face-remap array. A BVH node has two 32-byte children, each containing six float32 bounds values, an int32 child/face index and an int32 face count. Per-face bounds use six float32 values.

| Count field / range | Body | Spin | CC Pitch | Either barrel |
|---|---|---|---|---|
| Vertices | 34–11138, 925 | 34–5234, 433 | 34–2198, 180 | 34–230, 16 |
| Triangles | 11142–20662, 1586 | 5238–9586, 724 | 2202–4174, 328 | 234–370, 22 |
| AABB, no count | 20662–20686 | 9586–9610 | 4174–4198 | 370–394 |
| BVH nodes | 20686–27282, 103 | 9610–12622, 47 | 4198–5418, 19 | 394–462, 1 |
| Face bounds | 27282–65350, 1586 | 12622–30002, 724 | 5418–13294, 328 | 462–994, 22 |
| Materials | 65350–68526, 1586 | 30002–31454, 724 | 13294–13954, 328 | 994–1042, 22 |
| External face map | 68526–74874, 1586 | 31454–34354, 724 | 13954–15270, 328 | 1042–1134, 22 |
| External vertex map | 74874–81646, 1692 | 34354–37070, 678 | 15270–16594, 330 | 1134–1242, 26 |
| UV int32 indices | 81646–100682, 4758 | 37070–45762, 2172 | 16594–20534, 984 | 1242–1510, 66 |
| UV XYZ float64 positions | 100682–141294, 1692 | 45762–62038, 678 | 20534–28458, 330 | 1510–2138, 26 |
| UV channel count | 141294, 1 | 62038, 1 | 28458, 1 | 2138, 1 |
| UV channel 0, XY float64 | 141298–168374, 1692 | 62042–72894, 678 | 28462–33746, 330 | 2142–2562, 26 |
| Final face-remap count | 168374, 0 | 72894, 0 | 33746, 0 | 2562, 0 |
| End of payload | 168378 | 72898 | 33750 | 2566 |

### Convex resources

The SM Pitch payload has two simple resources followed by its complex triangle mesh. Convex planes are six float32 values (point and normal); vertices are three float32 values. Bounds use six float32 values, volume one, centre of mass three and margin one. Topology index type `1` selects uint8 indices: each plane has two indices, each half-edge three, each vertex one incident half-edge, and each unique edge one half-edge. Inertia is three float32 values; mass rotation is four float64 values.

| Field | SM Pitch first resource | PA base first resource |
|---|---|---|
| Whole implicit object | 8–1359 | 8–702 |
| Planes | 26–462, 18 | 26–246, 9 |
| Vertices | 462–850, 32 | 246–418, 14 |
| Bounds | 850–874 | 418–442 |
| Volume / centre / margin | 874–894 | 442–462 |
| Topology index type | 894, value 1 | 462, value 1 |
| Plane topology | 895–935, 18 | 463–485, 9 |
| Half-edges | 935–1227, 96 | 485–615, 42 |
| Vertex incident edges | 1227–1263, 32 | 615–633, 14 |
| Unique edges | 1263–1315, 48 | 633–658, 21 |
| Inertia / mass rotation | 1315–1359 | 658–702 |
| Second resource | 1359–2710 | 702–1396 |

The paired resources have identical decoded geometry and topology, with separate object tags. SM Pitch's complex count is at 2710; its triangle object spans 2714–19296. Every remaining CC Pitch field offset is shifted by 2702, ending at 36452. The PA base complex count at 1396 is zero; empty UV indices, UV positions, channel count and final face-remap count occupy 1400–1416. The two `PA_TNK_03_Turret` BodySetups have no cooked payload; their authored box primitives are represented in exported AggGeom metadata instead.

Do not interpret the two serialized convex resources as two active hulls. Local `BodySetup.cpp` around lines 241–283 prepares nonmirrored and X-mirrored inputs, while `ChaosCooking.cpp` around lines 160–203 mirrors X again for its mirrored cook. This is a plausible source-level explanation for the identical pair, rather than proof of the target's loading semantics. Local `FinishCreatingPhysicsMeshes_Chaos` around `BodySetup.cpp` lines 599–641 consumes resources according to authored `AggGeom.ConvexElems.Num()` and resets extras. The target branch and active shape selection still require independent verification.

## Counts, hashes and material mapping checks

SM and CC versions of Body, Spin and both barrels have byte-identical payloads. SM Pitch has the additional convex prefix, while its decoded complex triangle mesh agrees with CC Pitch. The PA base is the seventh distinct payload.

| Resource | Bytes | Cooked vertices / triangles | SHA-256 |
|---|---:|---|---|
| Body | 168378 | 925 / 1586 | `54fbcfaab11f0949781b2c5b518428d390341b6a3798b6ac1509ecb50a554e86` |
| Spin | 72898 | 433 / 724 | `405681ca128c73bdd1e73136735419621e05357843597ac6a949e622b4bba89c` |
| CC Pitch | 33750 | 180 / 328 | `6f3af8c05b4ca4f0f6d7cdf3b8f7dd48b4ff87e4c81173535fc498b2f8c5949e` |
| SM Pitch | 36452 | 180 / 328, plus two convex resources | `121577f3b24688e92346811d234cba2009fd15e0fcaea72c0ff7daa9929ff112` |
| Barrel L | 2566 | 16 / 22 | `4af3e8d93cfbeca8930b5f7f67b3a89abbeb6dd1efe45af4475c0960bd11561c` |
| Barrel R | 2566 | 16 / 22 | `5c91cc5c93acc908a71de022c7ed880f6c7551853d07f204c298c9cfc2b3d326` |
| PA base | 1416 | Two 14-vertex, 9-plane convex resources | `f05d97c1fd42aea07228e423020f7a73f7f65b49ca98353ada4656013b2c4269` |

The final comparator matches triangles one to one by material slot name and coordinates, allowing arbitrary corner permutation. It requires maximum absolute per-coordinate error at most `1e-6` metres. All five comparisons have zero missing and zero extra triangles. This does not claim winding equivalence. An earlier decimal-rounding comparison in the separate `decoded/` directory produced rounding-boundary mismatches; `decoded-verified/` is the final tolerance-based result.

| CC mesh | Matched triangles | Maximum coordinate error, metres |
|---|---:|---:|
| `CC_TNK_03_Body` | 1586 | 1.1444091807533141e-7 |
| `CC_TNK_03_Turret_Spin` | 724 | 1.1444091807533141e-7 |
| `CC_TNK_03_Turret_Pitch` | 328 | 5.7220459037665705e-8 |
| `CC_TNK_03_Turret_Barrel_L` | 22 | 6.675720198856538e-8 |
| `CC_TNK_03_Turret_Barrel_R` | 22 | 8.583068833445395e-8 |

Material IDs are joined against the original CC UStaticMesh `Properties.StaticMaterials` array, retaining slot indices rather than assuming GLB primitive order. Body IDs 0 and 1 are left and right tracks (629 and 648 faces); IDs 2 and 4 both resolve to `CC_MainBody` (203 and 28 faces); ID 3 is engine (48), ID 5 glass (6), and ID 6 fuel tank (24). Spin has strong metal slot 0 (420) and moderate metal slot 1 (304). Pitch and both barrels use `CC_MainBody` slot 0.

Every external face map is a permutation of `0..triangleCount-1`. Applying the external face and vertex maps reconstructs the original UV triangle indices, treating triangle corner order as unordered. Every final BodySetup face-remap array is empty. These maps preserve cooked-face material attribution; they do not identify a gameplay health section by themselves.

### Ordered winding check

The separate audit preserves the cooked index order while converting each UE centimetre position `(X,Y,Z)` to glTF metres `(-Y,Z,X)/100`. This coordinate transform has negative determinant, so it reverses handedness. Matches use the same material and `1e-6` metre tolerance as above; even corner permutations preserve winding, odd permutations reverse it. Each raw triangle has exactly one available cooked-face match, and no matched triangle admits both parities within tolerance.

| CC mesh | Same winding | Opposite winding | Ambiguous parity |
|---|---:|---:|---:|
| Body | 0 | 1586 | 0 |
| Spin | 0 | 724 | 0 |
| Pitch | 0 | 328 | 0 |
| Barrel L | 0 | 22 | 0 |
| Barrel R | 0 | 22 | 0 |
| Total | 0 | 2682 | 0 |

The JSON audit stores `rawFace`, `cookedFace` and `orientation` for every pair, plus the SM/CC dump hashes and property-presence flags. It contains no vertex geometry. Run it with `python -I E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/chaos-decode-v1/audit_winding.py`; it reads the fixed verified decode and refuses an existing `winding-v1.json`. Preserve or select a fresh output filename before a rerun.

Local UE source explains why cooked indices and a renderer's winding cannot be interchanged without care. `Engine/Source/Runtime/Engine/Private/StaticMesh.cpp:9184` sets collision input `bFlipNormals=true`. `Experimental/ChaosCooking.cpp:220–226` then swaps the first two triangle indices when that flag is set. The local cooking comment specifies the physics convention as clockwise in left-handed coordinates, equivalently counterclockwise in right-handed coordinates. This is schema guidance from the different local UE build, not a recovered target call or flag value.

The local Chaos ray visitor computes `cross(B-A,C-A)` and skips a face when `dot(rayDirection, normal)>0` **if** `bCullsBackFaceRaycast` is enabled (`Engine/Source/Runtime/Experimental/Chaos/Private/Chaos/TriangleMeshImplicitObject.cpp:149–166`). With the orthogonal handedness conversion `P(X,Y,Z)=(-Y,Z,X)`, `dot(cross(P(edge1),P(edge2)),P(direction))` is the negative of the UE-frame dot product. Consequently, this UE backface rejection corresponds to a **negative** dot product in the converted cooked frame, rather than the positive-dot rejection used for conventional glTF counterclockwise faces. Positive unit scaling does not change that sign. Opposite cooked/render winding after this reflection does not itself mean the target's orientation is wrong.

`BodySetup.cpp:710` passes `bDoubleSidedGeometry` into shape-creation parameters, and `Experimental/ChaosInterfaceUtils.cpp:323` sets mesh culling to its inverse. Thus the cooked triangle order, coordinate reflection, active shape construction and culling setting all matter. The two newly consulted source hashes are `4434c0d2df0f4e7dfb9f9ad280d516a4e0b34c4e1f889804ea1dad4c0369d978` for `TriangleMeshImplicitObject.cpp` and `d77b83e28c3e34bfcd4fbbb65e86d418732ef492282a1420142cb560695d0880` for `ChaosInterfaceUtils.cpp`.

All five original CC BodySetup JSON dumps explicitly contain `bDoubleSidedGeometry: true`; all five corresponding SM dumps omit this property. Omission is reported as absence, with a null value in the audit, rather than an independently recovered target class default. SM Body and CC Body have identical cooked bytes despite this metadata difference. Binary geometry equality therefore does not establish equal query participation or culling. A double-sided offline ray fixture remains conditional; conventional glTF counterclockwise culling cannot be applied to the converted cooked indices as proof of native behavior.

## Validation and semantic limits

The parser verifies payload size and SHA-256 against the manifest, finite numeric fields, bounded counts, booleans restricted to 0/1, triangle indices, topology references and reciprocal half-edge twins, mass-rotation normalization, and exact end-of-file consumption. Serialized bounds must agree with vertices within `1e-3` Unreal centimetres. External vertex mappings must agree with original UV positions within the same tolerance. UV sizes and remapped triangle indices are checked. Counts are capped at 1,000,000 and constrained by remaining input bytes.

The saved negative validation rejects all five mutations:

| Mutation | Rejection |
|---|---|
| Remove final byte | `truncated i at 2562` |
| Append one byte | `unconsumed bytes: 1 at 2566` |
| Change precision to 8 | `unsupported physics precision 8` |
| Set simple-array count to -1 | `invalid simple implicits count -1 at 4` |
| Set a triangle vertex to 65535 | `triangle vertex index out of bounds` |

All observed triangle objects serialize `DoCollide=false`; simple convex resources serialize `true`. Local `TriangleMeshImplicitObject.h` constructs triangle meshes with `DisableCollisions`. Consequently, the stored flag alone does not prove that scene raycasts exclude triangle meshes. Query participation also depends on active shape construction, collision trace mode, filter data and query flags. No query or simulation behavior was executed here.

Decoded body-local triangles are suitable inputs for a separate placement and query experiment. They do not resolve native component selection, skeletal transforms, trace complexity, mirror/scale handling, first-contact order, material-to-section routing or the explosion candidate-point algorithm. Those remain separate evidence questions; replacing a display proxy with these resources must preserve that distinction.

## Programmatic loading and decoder provenance

The report's `bodies` entries identify `bodySetupPath` and a `payloads` array. Each payload points to a deduplicated decoded file by `decodedFile`. For example:

```python
import json
from pathlib import Path

base = Path("E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/chaos-decode-v1/decoded-verified")
report = json.loads((base / "report.json").read_text(encoding="utf-8"))
body = next(b for b in report["bodies"]
            if "/CC/CC_TNK_03_Body." in b["bodySetupPath"])
decoded = json.loads((base / body["payloads"][0]["decodedFile"])
                     .read_text(encoding="utf-8"))
mesh = decoded["complexImplicits"][0]
vertices_cm = mesh["vertices"]
triangles = mesh["triangles"]
material_ids = mesh["materialIndices"]
original_face_ids = mesh["externalFaceIndexMap"]
```

`materialIndices[internal_face]` is the original static material slot index. `externalFaceIndexMap[internal_face]` gives the original face index; `externalVertexIndexMap[original_vertex]` gives the cooked vertex index or `-1`. `decoded["uvInfo"]` contains `indexBuffer`, `vertexPositions` and `channels`; `simpleImplicits` contains decoded convex resources including planes, vertices, topology and mass properties. Material names must be joined from the corresponding CC package dump. Preserve centimetres and the body-local frame until explicitly applying the actual component transform.

The external decoder is independently authored diagnostic Python using only the standard library. It is not a bundled UE or CUE4Parse source implementation and currently has no separately packaged license notice. The repository's code policy is MIT, documentation is CC-BY-SA-4.0, CUE4Parse carries Apache-2.0, and local Epic source remains under its own license. This evidence note references local schema paths and hashes; it does not redistribute those sources or the game's raw geometry.
