# Round 91: FOB placement, foundations, doors, smashable windows, drone projectile

Items V5-06 and V5-07 of census v5 (`docs/evidence/round90-census-v5.md`). Build ++Wardogs+Live-CL-516586. Method and tools: `docs/evidence/round86-models.md`.

## Coverage

| | Before | After |
|---|---|---|
| Objects in `assets/data/object-collision.json` | 46 (44 GLBs, 584 KiB) | 74 (74 GLBs, 685 KiB, largest 78 KiB) |
| Groups | buildables, deployables, props | + "Doors and windows" (26 objects), "Projectiles" (1) |
| FOB | 7 pieces at the origin, finished-stage meshes without geometry | 3 factions placed from the Blueprints: foundation, finished base (collision proxies, flag, carried model), destroyed base |
| Foundations (`FoundationStaticMesh`) | FOB only (at origin) | 24 buildables have a "Foundation" stage (23 new) |
| Interactable doors | none | 14 Blueprints (13 `BP_Interactable*`/`BP_InteractableDoor_*`, `B_Door`) |
| Smashable windows | none | 12 Blueprints (`B_Smashable*`) |
| `BP_Drone_Projectile` | none | 1 object |
| `SM_HBlock` | none | 1 object (loose mesh) |

## Status per item

### V5-06 FOB faction meshes, foundations, drone: FOUND

- **FOB placement.** The three faction Blueprints (`B_ForwardOperatingBase_LoneStar`, `_Manticore`, `_Valkyra`, under `Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/ForwardOperatingBase/`) were dumped with `WdExtract dump`. Each places its static meshes with SimpleConstructionScript component transforms. A faction's finished base is its `SM_Buildable_FOB_Stages_<Faction>` (render only, no simple collision primitives; `RelativeLocation` about 0, 0, 11 for Lonestar), a flag, the carried model `SM_FOB_InHand_01a` and its decals, and 10 to 15 invisible (`bVisible` false) `BlockAll` collision proxies: `SM_PrefabCollision_Cube_1x1m_01a`, `_Cylinder_8Sides_01a`, `_DirectionalRamp_01a` (Lonestar), `_Trapezium_1x1m_01a` (Manticore, Valkyra). These proxies are the FOB's real collision: a 4 m ground slab, boxes, cylinders and a tall mast. The destroyed base is the inherited `DestroyedMesh` component (`SM_FOB_Destroyed_<Faction>`, convex hulls, `visible` false in the default). Proxies that Lonestar and Manticore hang under the slab inherit its scale (parent scale multiplies; the child's offset is scaled by it); the composition is Unreal's FTransform rule (`_tools/object_blueprints.py`).
- **Check on the placement.** The "1x1m" prefab meshes are 2 m cubes (box extent 100). With the parent-scale rule every proxy of all three bases lies inside the bounds of the faction's stage mesh (Lonestar 15 of 15, Manticore 13 of 13, Valkyra 10 of 10, tolerance 30 cm); without it, the mast (offset z 2280) would be 22 m up, well above the stage mesh's 14 m top. The mast's top (about 11.7 m of box above the slab) also matches the flag at z 1174.
- **Foundations.** `FoundationStaticMesh` is set on 24 definitions; the meshes (`SM_Foundation_*`, `SM_SV_Shelter_FoundationPlaceholder`) are in the collision export. Each is a "Foundation" stage drawn at the buildable's origin. ABSENT: the spawn transform (native code, `bShouldSpawnFoundations` spawns it; not in the exports). Supporting check: for 21 of the 23 non-FOB buildables the foundation's bounding box at the origin overlaps the bounds of the finished stage meshes, with the box centre about 1 m below the origin (z -87 to -128 cm). The two gate leaves have no stage meshes to compare. This is a plausibility check, not a decoded transform.
- **`BP_Drone_Projectile`** (`STN_05/Content/Blueprints`). Root component is `Box Component`, half extent 46.64 x 46 x 18.77 cm (93.3 x 92 x 37.5 cm), no collision profile set in the Blueprint (the default of a box component). Attached through `NetworkSmoothingComponent`: `SK_Drone_01` (relative 15.14, 0, -11.18 cm, yaw -90, scale 0.7, no collision primitives read here), the rotor mesh (hidden), trail and first-person meshes (VFX, `NoCollision` profile). Vitality: `WDVitalityComponent` base and max health 50. No `WDDamageEntityComponent`, so no per-caliber damage row for the drone as a target. Its warhead is `DA_Drone_ProjectileData`: tag `Meta.Damage.Explosive.Drone`, base damage 120, radius 1000 (full damage inside 500), minimum 15, falloff 0.45, blunt 100, arming delay 0.1 s, lifetime 500 s. Movement: `WDGlideProjectileMove` (max altitude 25000, max turn rate 60 deg/s).
- **`SM_HBlock`**: one convex hull about 1.5 m per side, `BlockAll`; no data asset in `data/` references it. Added as a loose mesh in "props".

### V5-07 doors and smashable windows: FOUND (collision, Blueprint data); health ABSENT

- **Doors.** `D_Interactable*` and `D_InteractableDoor_*`/`D_Door` are `BHDestructionBuildingDefinitionDataAsset`s with one mesh and one chunk. The 14 door Blueprints (`GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/Doors`, parent `AWDDoor`, which derives from `AWDDestructionBuilding`) name them. The definition's `MeshCenter` equals the mesh's local bounds centre, so the chunk transform places the mesh as it is (yaw 90, a few cm offset): the pivot is the hinge and the leaf extends 80 cm to the side, the same place as the Blueprint's interaction box (Y -80, Z 140 to 150). Door meshes with simple collision: 1 box each, 3 boxes for `SM_ModKit04_Apartment_BalconyDoor_01a`, convex hulls for the hospital leaves; profile `BlockAll`; trace flag `UseSimpleAsComplex` on the apartment, entrance, `SM_ModKit04_Door`, `DoorSolid_01a`, garage and `SM_Door_01a_R` meshes, default on the rest.
- **Blueprint values stored** (only values the Blueprints override are in a dump; every other `AWDDoor` field keeps its native default, which is not in the exports): `FrameHeight` 268 (all), `FrameThickness` 12 (8 doors), `FrameWidth` (2), `DoorChunkConfiguration` Single (13), `DoorTypeContextTag` `Audio.Asset.Door.Metal` (11) or `.Wooden` (3: `B_Door`, Balcony, WoodPVC), `MaxBreachDistances` Explosive 250 cm (9 doors; the commercial right leaf, both garage leaves and both hospital leaves set none), `PushRadiusBuffer` 60 and `SprintPushParams` (speed 26, angle 15; 9 doors), `bCanVehiclesBreach` false (`B_Door` only), breach and swing curves `Curve_DoorBreach_Float`, `Curve_DoorSwing_Float`. `EWDDoorBreachMethod` is Sprint, Melee, Explosive, Vehicle (SDK). Breaching with the Halligan costs 1000 of 7000 durability (`docs/evidence/round40-medical-movement.md`, M23).
- **Health and damage rows: ABSENT.** No door Blueprint sets a health value or a damage-entity tag, and no damage table has a row for an environment door (the only `Meta.Damage.Buildable.Door` rows belong to the buildable barrier door). The SDK class lists `BaseBreachDamage`, `MeleeBreach` distances and vehicle breach speeds as native fields with native defaults, which cannot be read without the CDO. NOT RESOLVABLE with the exports.
- **Smashable windows.** 12 `B_Smashable*` Blueprints (native parent `AWDSmashableWindow`: states Normal, Damaged, Smashed; `OnWindowMeshHit`). They set only the glass mesh (`WindowMesh`, yaw 90, `YForwardMesh` true), the broken-remains meshes (4 components) and effects. `B_SmashableWindowMaster` alone sets `AirborneMovementBreakThreshold` 0.8, `GroundedMovementBreakThreshold` 6, `GlassShard_Amount` 250 and `SmashedLifespan` 0. Glass meshes have one box each, profile `BlockAll` except `SM_ModKit04_Double_WindowGlass_01a` (`NoCollision`). Health and damage rows: ABSENT (as for doors); the break is a hit event on the mesh with a movement threshold, not a health pool. Whether a bullet breaks a pane is native code, not traced.
- Not drawn: the 4 `BrokenRemains` components per window (`SM_VFX_WindowPiece*`, effect meshes; the master's use `NoCollision`), door swing and breach curves (the viewer shows the closed leaf).

## Scripted inputs

`python -I _tools/object_models.py --plan <dir> --files <files.txt>` now also writes `bp_in.txt` (31 Blueprint packages) and extends `collision_in.txt` with the Blueprint meshes, every `FoundationStaticMesh` and `SM_HBlock` (183 packages; the Blueprint meshes come from `assets/data/object-blueprints.json` once it exists).

## Regenerate

`X <out> <mode> ...` stands for `WdExtract <Paks> <aes.txt> normal-order.usmap <out> <Paks>/oo2core_9_win64.dll <mode> ...` as in round 86.

```
X all list ""                                                         # all/files.txt
python -I _tools/object_models.py --plan plan --files all/files.txt   # bp_in.txt (collision_in.txt is partial on the first pass)
X bp dump plan/bp_in.txt                                              # Blueprint dumps
python -I _tools/object_blueprints.py bp                              # assets/data/object-blueprints.json
python -I _tools/object_models.py --plan plan --files all/files.txt   # collision_in.txt complete
X col collision plan/collision_in.txt
X phys physics plan/phys_in.txt --names normal-order.usmap
python -I _tools/object_models.py --collision col/collision.json --physics phys/physics.json
python -I _tools/object_models.py --check
python -I _tools/object_blueprints.py --check
python -I _tools/object_models_check.py
```

New scripts: `_tools/object_blueprints.py` (Blueprint dump to `assets/data/object-blueprints.json`; `--check` compares the door definitions with `data/`). There is no `_tools/pipeline_registry.json` on this branch.

## Open items

- Spawn transform of foundations (native).
- Door health, breach damage and window break rules (native defaults and code; no data row).
- Smashed-window state collision (`BP_UpdateWindowVisualsAndCollision` runs in the Blueprint's ubergraph; not decoded).
- Meshes with no simple collision primitives (FOB stage meshes, the flag, in-hand decals) still collide on render triangles, not published.
