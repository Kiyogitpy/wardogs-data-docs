# cue4parse_extractor (WdExtract)

Offline static export of cooked Wardogs assets with
[CUE4Parse](https://github.com/FabianFG/CUE4Parse). It reads the game's own
`.pak`/`.utoc` files; it never runs the game or contacts a service. This is
the tool behind [`assets/data/ge-values.json`](../../assets/data/ge-values.json)
(the [Gameplay Effect Values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md) page)
and the Blueprint bytecode in
[DamagePipeline §7](../../pipelines/Wardogs_DamagePipeline_v2.md#7-custom-operations).

## You need

- .NET SDK 10
- A CUE4Parse checkout. FabianFG/CUE4Parse at commit `0415fe2` (2026-10-14) is
  known to work with this build. By default the project expects it at
  `../../../CUE4Parse` (next to this repository's folder); otherwise pass
  `-p:CUE4ParseProject=<path to CUE4Parse.csproj>`. The `mesh` mode also uses
  `CUE4Parse-Conversion` from the same checkout (found next to `CUE4Parse/`;
  override with `-p:CUE4ParseConversionProject=<path>`).
- Your own installed copy of the game: the `Paks` folder and its
  `oo2core_9_win64.dll`.
- The build's usmap (`5.7.4-516586+++Wardogs+Live-Wardogs.usmap`) and the pak AES
  key in a one-line text file. Neither is in this repository; `.gitignore` keeps
  `aes.*` and `*.usmap` out if you store them in the checkout.

## Build

```
dotnet build -c Release -p:CUE4ParseProject=<path>\CUE4Parse\CUE4Parse.csproj
```

## Run

```
WdExtract <Paks> <keyfile> <usmap> <out> <Paks>\oo2core_9_win64.dll <mode> [args] [--names <usmap>]
```

| Mode | Writes |
|---|---|
| `list GE_` | `<out>/files.txt`: every package whose name starts with the prefix |
| `schema BHGameplay` | `<out>/usmap_schema.json`: usmap layouts whose name contains the text |
| `recover-bp-types <new.usmap>` | New map with unknown array element types recovered from cooked Blueprint `ChildProperties`; refuses an existing output map. Audit log in `<out>/_blueprint_types_log.txt`. |
| `recover-rigvm-types <new.usmap>` | New map with unknown array element types recovered from exact RigVM property-bag descriptor hashes; refuses an existing output map. Audit log in `<out>/_rigvm_types_log.txt`. |
| `dump <files.txt or package paths>` | `<out>/<name>.json` per package: all exports, Blueprint bytecode included; failures in `_failures.txt` |
| `deobfuscate <out.usmap> --names <donor.usmap> [--sdk <sdk/raw>] [--types <usmap>] [--fill-names <usmap>]` | A deobfuscated copy of `<usmap>`: names and element types restored from the donor, then (with `--sdk`) from this build's SDK headers, then the hand patches; read back through CUE4Parse to check it. `--types` / `--fill-names` then make the export usmap (see below). No paks or key are read (pass `-` for those arguments). Log in `<out>/_deobfuscate_log.txt` |
| `findname <path prefix> <text>` | `<out>/findname.txt`: packages under the prefix whose name map contains the text (IoStore imports are hashed, so this finds names an asset uses, not who references it) |
| `mesh <files.txt or package paths>` | `<out>/<collision mesh>.glb` per vehicle collision mesh, plus `manifest.json`; failures in `_failures.txt` (see [Collision meshes](#collision-meshes-mesh)) |
| `physics <files.txt or package paths>` | `<out>/physics.json`: each physics asset's bodies (collision primitives) and each skeletal mesh's reference skeleton; failures in `_failures.txt` (see [Physics assets](#physics-assets-physics)) |
| `collision <files.txt or package paths>` | `<out>/collision.json`: BodySetup properties, primitive metadata, static-mesh bounds and SHA-256-indexed cooked collision payload files. Collision formats remain undecoded. Refuses existing metadata or payload files; failures return exit code 2. |

`recover-bp-types` reads serialized Blueprint `UStruct.ChildProperties`,
including the embedded `FArrayProperty.Inner` field. It requires a unique
matching package and generated-class export, matching static-array dimensions
and complete inner-type metadata. A property-name miss can match only a unique
ASCII-case-equivalent cooked name after the complete ordered owner property
names, static dimensions and cumulative schema slots align. This fallback
preserves the usmap spelling; folded-name equality alone is insufficient.
Generated property bags are outside this pass.

`recover-rigvm-types` restores generated property-bag array types only after
reconstructing an exact descriptor hash for an existing owner and matching its
ordered names, slot count, static dimensions and already-known types. Both
modes fill only unknown array element types. Each takes a pre-deobfuscated
input map and a new output path; `--names` is refused and the original input
map is preserved. Existing output paths are refused, but an I/O failure may
leave a partial newly-created output file. On CL516586, Blueprint recovery
fills **83** slots and RigVM recovery fills **79**. Applied in sequence to the
v2 export, the resulting `wardogs.recovered.usmap` is **3,046,707** bytes,
SHA-256 `277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380`;
it retains **2,690** hashed names and leaves **53** unknown types across
**36** other generated property-bag owners. See the [Blueprint mapping audit](../../docs/evidence/round8-mapping-gaps.md)
and [property-bag recovery evidence](../../docs/evidence/round8-propertybag-types.md).

**`--names <usmap>`** (except `recover-bp-types` and `recover-rigvm-types`) borrows property names and array element
types from an unobfuscated usmap, by the same rules as `deobfuscate` (see
[`mappings/README.md`](../../mappings/README.md#how-deobfuscated-it-is)).
Simpler: generate the deobfuscated usmap once and pass it as `<usmap>`:

```
WdExtract - - mappings\5.7.4-516586+++Wardogs+Live-Wardogs.usmap out - deobfuscate ^
  mappings\5.7.4-516586+++Wardogs+Live-Wardogs.deobfuscated.v2.usmap ^
  --names mappings\old-deobfuscated-507-ClosedBeta.usmap --sdk sdk\raw
```

**`--sdk <dir>`** (`deobfuscate` only) aligns each usmap struct with its declaration in the
Dumper-style SDK headers of this build (`sdk/raw/*_classes.hpp`, `*_structs.hpp`). The pass pairs
properties only between anchors where both sides agree on count, type, static-array size and token
length. It corrects closed-beta names where fields were reordered between builds, and withdraws a
donor name when the SDK gives that name to another token. The log lines start with `sdk`; the
method and counts are in [`mappings/README.md`](../../mappings/README.md#how-deobfuscated-it-is).
Without `--sdk` the output is the v1 file, byte for byte.

**`--types <usmap>` / `--fill-names <usmap>`** (`deobfuscate` only) turn the result into the usmap
`data/` is exported with. Both compare each struct only with the same-named struct of the other usmap
when the two have the same number of property entries, key by key, and need the same property type
(and static-array size, and struct type). `--types` gives a property whose type still contains
`Unknown` the other side's fully known type; without it CUE4Parse stops reading a struct at its first
`Unknown` array. `--fill-names` gives a property whose name is still a plain token the other side's
name, only if the name has the length the token encodes, is readable nowhere in this build's own
usmap, is not given to another token, is not already in the struct, and token and name are one to
one across all structs. A name already present is never replaced. The log lines start with
`export`. The exact commands are in [`mappings/README.md`](../../mappings/README.md#data-and-the-v2-usmap).

The donor is the closed-beta usmap (`mappings/old-deobfuscated-507-ClosedBeta.usmap`,
an older build, not obfuscated). With the result, skeletal meshes, physics assets
and data tables decode too. Keep both usmaps in `mappings/`; they are gitignored
and never committed. Checked: all 341 GE assets re-dumped with the deobfuscated
usmap are byte-identical to the published export.

`dump` and `mesh` first restore usmap property names that are hashed in this build and
array types the usmap leaves as `Unknown`, by property index against the SDK
headers in `sdk/raw/` and UE's declaration order: `BHGameplayEffect.Modifiers`,
`GameplayTagQuery.TagDictionary` / `QueryTokenStream`, and for static meshes
`StaticMaterials`, `Sockets`, `AssetUserData`, `ComplexCollisionMesh` and
`StaticMaterial.MaterialSlotName` (without these a static mesh's render data
fails to load). What it changed is
written to `_usmap_patches.txt`.

## Collision meshes (`mesh`)

Exports the low-poly collision meshes that carry a vehicle's hitbox slots
(`CC_FuelTank`, `CC_Main`, …; [VehicleDamagePipeline §3.1](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md#31-hitboxes)),
never a render mesh:

- a static mesh with `ComplexCollisionMesh` set: that collision mesh is written,
  and the input is recorded as its render mesh. A mesh whose
  `ComplexCollisionMesh` is itself (the render mesh doubling as collision, e.g.
  `SM_WHL_07_Transport_Armored_Glass`) is skipped as render geometry;
- a static mesh under `…/ComplexCollision(s)/` or named `CC_*` (stationary
  vehicles' `ComplexProxy` fragments): written as is;
- any other static mesh: skipped (listed under `skipped`);
- a skeletal mesh: no geometry; its reference-pose bones and sockets (the
  mesh's and its skeleton's, placed on their bone) go to the manifest's `bones`
  (needs `--names`). Skeletal meshes carry no collision mesh of their own.

Every input static mesh's sockets (mesh-local) go to `staticMeshSockets`,
whether or not it has a collision mesh.

Geometry is decoded by CUE4Parse-Conversion's `StaticMeshDto` (LOD0) and
written with SharpGLTF directly, not with Conversion's glTF writer: that writer
names materials after the material instance (`MI_VehicleCC_FuelTank`) rather
than the slot, and adds normals, tangents and UVs. Each GLB has one node and
one mesh named after the collision mesh, and one primitive and material per
slot, named exactly as `FStaticMaterial.MaterialSlotName`. Materials carry only
a `baseColorFactor` (a stable colour per slot name); there are no textures,
images, samplers, normals or UVs, only `POSITION` and indices.

**Coordinates.** Unreal stores centimetres, X forward, Y right, Z up
(left-handed). The GLBs are metres, +Y up, right-handed, with the vehicle's
front along +Z (glTF's convention):

```
[x]           [ 0 -1  0] [X]                     x = -Y/100   (UE right -> glTF -X)
[y] = 1/100 * [ 0  0  1] [Y]    (column vectors)  y =  Z/100   (UE up    -> glTF +Y)
[z]           [ 1  0  0] [Z]                      z =  X/100   (UE fwd   -> glTF +Z)
```

`det M = -1`: the map is a reflection, which is what turns left-handed into
right-handed. Triangle index order is kept: read as plain numbers, UE's cooked
triangles have negative signed volume (clockwise seen from outside), and the
reflection makes them counter-clockwise from outside as glTF requires. The
mode logs both signed volumes per mesh and the manifest keeps the glTF one
(`signedVolumeM3`, positive). For comparison, Conversion's own writer maps
`(X, Z, Y)/100`, front along +X. Rotations map as `R' = M R Mᵀ`; for a
quaternion `(x, y, z, w)` that is `(y, -z, -x, w)`.

`manifest.json` lists per collision mesh: `name`, `collisionMesh` (package
path), `file`, `renderMeshes`, `lod` (0), `triangles`, `slots` (name,
collision material and its path, `materialIndices` into `StaticMaterials`,
triangles, vertices), `boundsMin` / `boundsMax` (metres,
glTF axes) and `signedVolumeM3`. `bones` holds, per skeletal mesh, every
bone's component-space reference pose in the same frame: `translation`,
`rotation` (glTF quaternion), `scale` and a glTF column-major `matrix`.

## Physics assets (`physics`)

Exports the bodies of a `UPhysicsAsset`, which are collision primitives only, and the reference
skeleton that places them. This is the source of the infantry hitbox model
(`_tools/infantry_model.py`). Run it with `--names`, since skeletal meshes and physics assets do not
decode without it.

- A physics asset goes to `physicsAssets`: `name`, `package`, `bodyCount`, `shapeCounts`,
  `boundsBodies`, the number of `constraints`, and `bodies` in `SkeletalBodySetups` order. Each body
  has its `index`, `bodySetup` (export name) and `boneName`, and the collision settings as cooked:
  `physicsType`, `collisionResponse` (UE's `CollisionReponse`), `collisionTraceFlag`,
  `physMaterial`, `physMaterialOverride` and the raw `defaultInstance`. A value the asset leaves
  out is the class default and is written with `(default)` after it.
- Each body's `shapes` come from `AggGeom`. `type` is `sphyl`, `sphere`, `box`, `taperedCapsule`
  or `convex`; any other non-empty element array (level sets, skinned meshes) fails the asset. Each
  shape also has `name`, `collisionEnabled` and `local`, its frame relative to the bone in the
  glTF axes of `mesh` (metres, `translation`, `rotation`, `scale`). Sizes are in metres too:
  `radius` and `length` (the cylinder part of a sphyl, along the element's UE Z, which is glTF
  local +Y), `radius0` / `radius1` (a tapered capsule's +Z and -Z ends), and a box's `size` as
  full extents in glTF local x, y, z (UE Y, Z, X). A convex element has `vertices` (glTF, element
  frame) and `indices` (UE order). `ue` keeps the element's cooked values: centimetres, FRotator
  degrees, bone-local.
- A skeletal mesh goes to `skeletalMeshes` with its `physicsAsset`, `shadowPhysicsAsset`,
  `skeleton`, and `bones` in component space. Bones are written as in `mesh`'s manifest
  (translation, glTF rotation, scale, column-major matrix and parent). To place a shape, compose the
  bone's frame with the shape's `local`.

Checked on 2026-10-18: `PA_TPCharacter_Simplified` gives 20 bodies (9 box, 1 sphere, 6 sphyl,
6 tapered capsule), `PA_TPCharacter` 20 (19 convex, 2 sphyl), `PA_TPCharacter_Simplified_Physics`
21 (6 box, 15 sphyl). `SK_DefaultCharacter` and `SK_TP_Male_000` have the same 177 bones and the
same reference pose on every bone that has a body.

```
WdExtract <Paks> <keyfile> <usmap> out\physics <Paks>\oo2core_9_win64.dll physics ^
  Wardogs/Content/Characters/Default_PlayerMesh/TP/PA_TPCharacter_Simplified ^
  Wardogs/Content/Characters/Player/SK_DefaultCharacter --names <closed-beta usmap>
python -I _tools/infantry_model.py --physics out\physics\physics.json
```

## Post-processing

- `python -I ge_summary.py <out> <out>/files.txt <summary dir>` turns GE dumps
  into `ge_summary.json` (copy it to `assets/data/ge-values.json`) and a
  markdown overview. Then run `python _tools/ge_values.py` from the repository
  root.
- `python -I kismet_listing.py <dump>.json <listing>.txt` prints a Blueprint's
  bytecode one statement per line with byte offsets.

## Reproduce the GE export

```
WdExtract <Paks> <keyfile> <usmap> out <Paks>\oo2core_9_win64.dll list GE_
WdExtract <Paks> <keyfile> <usmap> out\ge_raw <Paks>\oo2core_9_win64.dll dump out\files.txt
python -I ge_summary.py out\ge_raw out\files.txt out
```

Checked on 2026-10-17: 341 packages, and a re-dump matched the published
export byte for byte.

## Export every vehicle's collision meshes

`vehicle_meshes.py` drives `mesh` per entry of
[`assets/data/vehicle-hitboxes.json`](../../assets/data/vehicle-hitboxes.json):

```
WdExtract <Paks> <keyfile> <usmap> out <Paks>\oo2core_9_win64.dll list ""
python -I vehicle_meshes.py plan <repo> out\files.txt <meshes>
WdExtract <Paks> <keyfile> <usmap> <meshes>\<id> <Paks>\oo2core_9_win64.dll mesh <meshes>\<id>\_inputs.txt --names <closed-beta usmap>
python -I vehicle_meshes.py finish <repo> <meshes>
```

`plan` assembles each vehicle's first variant with `damage_tables.assemble()`
(platform plus slot parts) from `data/`, applies the variant's
`CustomFragmentData` mesh overrides (for example a different `:Chassis`
skeletal mesh), and lists the meshes of `MVF_StaticMesh`,
`MVF_DestructibleMeshes` (unless `bRegisterComplexSurface` is false),
`MVF_InstancedWheels` and `MVF_SkeletalMesh` fragments. `finish` adds to the
manifest every mesh fragment (module, enabled, attach query, relative
transform in UE and glTF frames, surface group and type,
`bRegisterComplexSurface`, `IndexedSlotNames`, collision profile, the collision
mesh it maps to or why none), the wheel setup from the vehicle config's axles
(index, side, bone, tyre health tag), the slot map, and `slotCheck`: the slots
on the meshes against the map. Indexed wheel slots are assumed to expand to
`<name>_<wheel index>`, which matches the maps' `CC_Wheel_N` / `CC_Tyre_N`.
It checks every GLB and writes `_DONE.txt`; a negative signed volume is a
warning (open or inward-facing in the source data).

Checked on 2026-10-17: all 21 vehicles export with no failures, 84 GLBs and
74,101 triangles, and every GLB passes
`npx --yes @gltf-transform/cli@4.4.2 validate` with no messages. The Havoc
gives the 9 collision meshes of `SM_ROT_02_*` (the missile pods, the reticle
and the destroyed body have none).
