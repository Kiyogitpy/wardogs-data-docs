# Round 86: collision and hitbox model coverage

Build: ++Wardogs+Live-CL-516586. Scope: every gameplay object that can be hit or that blocks bullets or vehicles, and has a collision or physics asset in the paks. The pak listing (`WdExtract list ""`, 66,550 packages) was searched by path and name, then each candidate was checked against `data/` (what references it). GLBs carry collision geometry only; none has an image, texture or sampler (parsed from the GLB JSON chunk by `python -I _tools/object_models_check.py`).

## Coverage

| Group | Objects | Before | After | How |
|---|---|---|---|---|
| Vehicles (all `VV_*` variants, 23 ids) | tanks, wheeled, rotary, SPW, stationary | 22 ids, 36 GLBs; STN_05 had none | 23 ids, 37 GLBs | STN_05 added with `vehicle_meshes.py` and `vehicle_models.py`. Its platform attaches STN_03's `Mortar_Base_Proxy` (collision mesh `CC_Mortar_Base`, slot `CC_Fabric`); the damage map names `CC_Main`, so every hit takes the default section, which is the main Health |
| Wheel-destroyed states | Humvee WHL_05 (3 variants), WHL_08 (2) | covered | covered | existing |
| Stationary weapons | STN_01 to STN_06 | 5 of 6 | 6 of 6 | as above |
| Buildables and fortifications | 32 `WDBuildableDataAsset` definitions | none | 32 objects, 30 with geometry | new `_tools/object_models.py`, page `pipelines/object-viewer.md` |
| Placed explosives | AT mine, Claymore, IED, C4, Molotov, smoke grenade | none | 6 of 6 | same |
| Crates | ammo crate, small, large, three free supply crates | none | 6 of 6 | physics assets |
| Aircraft | FWG_01 airplane | none | 1 | `PA_FWG_01`; no damage row, no collision meshes |
| Characters | player, `SK_Western_Mid`, presets | player | player (see findings) | existing infantry model |

Totals: 46 objects in `assets/data/object-collision.json`, 44 GLBs (584 KiB meshopt-compressed, largest 41 KiB), plus the STN_05 vehicle GLB.

### Findings

- **AI and other characters.** `SK_Western_Mid`, the `SK_Preset_*` meshes (non-SuperHeavy) and `SK_TP_Male_000` all name `PA_TPCharacter_Simplified`, the player's asset, so the infantry model covers them. `SK_Lonestar_Vendor_03`, `SK_Manticore_Vendor_01` and `_04`, `SK_Pilot_01`, `SK_Rusalka`, `SK_Valkyra_Vendor_05_Face` and the `*_SuperHeavy_` presets name no physics asset (Mutable-built or non-combat NPCs). No separate AI character class was found in `data/` ([`WDAIPvEAICore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/WDAIPvEAICore.json) holds behaviour data only).
- **Buildable collision is simple shapes, not collision meshes.** Only `CC_Radio` (12 triangles) is a collision mesh in the buildables plugin. Every other stage mesh has a `UBodySetup` with `AggGeom` boxes, spheres, sphyls and convex hulls, which `WdExtract collision` already exports as cooked JSON. They are drawn as closed low-poly shapes placed by the stage's `MeshToPlacements`. Profiles are `BlockAll` or the default; only the Claymore sets `CTF_UseSimpleAsComplex`.
- **Meshes with no simple shapes** (any collision would use the render triangles; not published): `SM_Buildable_FOB_Stages_{Lonestar,Manticore,Valkyra}`, `SM_C4_Detonator`, `SM_Fuel_Canister`, the drills, `SM_Laptop`, and the cables, wires and loose paper in the Hotzone Magnet and Repair Station stages.
- **FOB.** The definition has no stages asset. Its foundation is `FoundationStaticMesh`; the faction meshes are named only in the Blueprint, which is not in `data/`. They are listed from the package names and placed at the origin (placement unknown).
- **Gate_Left and Gate_Right** have stages with no meshes (stage actors only): no geometry.
- **Vehicle destroyed bodies.** No destroyed-body collision mesh exists in the paks for any vehicle (a pak search for destroyed, wreck or husk names under `Vehicles/` finds only gameplay cues and a bus material). Destroyed wheel states are the only vehicle damage state with its own collision mesh, and they are covered.

### Not covered, with reason

| Item | Reason |
|---|---|
| `CC_Browning_Gun`, `CC_Browning_Mount` (MWSY_001) | The MG nest's gun proxy attaches to a `receiver_J` bone its skeleton lacks, so it is likely never attached (already noted on the vehicle viewer page). Collision meshes exist; placement does not. |
| Vehicle physics assets (`PA_TNK_*`, `PA_WHL_*`, `PA_ROT_*`, `SK_*_Physics`) | They drive vehicle physics, not hit tracing; hit slots come from the `CC_*` meshes the vehicle viewer shows. Not extracted. |
| `PA_STN_05` | Extracted and published as "STN_05 skeletal mesh bodies" (kinematic bodies of `SK_STN_05`), separate from the vehicle model. |
| Helmet physics assets (`PA_Helmet_*`) | Already listed on the infantry page as Mutable-selected. |
| Environment kits (walls, towers, props under [`Content/Environment`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Environment), `ExternalAssets`, landscape) | Level geometry, not gameplay objects with health; hundreds of meshes. Props used by buildable stages (planks, crates, sandbag pile) are included. |
| Hammers, repair-tool meshes, held-item physics assets (`PA_Claymore`, `PA_M67_Grenade`, ...) | First-person item meshes, not world objects. |
| `BP_Drone_Projectile` (STN_05) | The Blueprint is not in `data/`; the bp teammate owns Blueprint extraction. |

## Regenerate

`WdExtract.exe` at `E:/Reverse_Engineer/wardogs_analysis/round76_icons/bin/` already has the `mesh`, `physics` and `collision` modes. `X <out> <mode> ...` stands for `WdExtract <Paks> <aes.txt> normal-order.usmap <out> <Paks>/oo2core_9_win64.dll <mode> ...`. The input lists come from `object_models.py --plan` (buildable `MeshToPlacements` meshes mapped with `vehicle_meshes.package_map`, the item static meshes, the FOB meshes, and the crate, FWG_01, STN_05 and character `SK_`/`PA_` lists); the planned lists were diffed against the lists used in round 86 and are identical.

```
X all list ""                                                          # all/files.txt
python -I _tools/object_models.py --plan plan --files all/files.txt    # plan/collision_in.txt, plan/phys_in.txt
X col2 collision plan/collision_in.txt
X phys physics plan/phys_in.txt --names normal-order.usmap
python -I _tools/object_models.py --collision col2/collision.json --physics phys/physics.json
python -I _tools/object_models.py --check
python -I _tools/object_models_check.py
# vehicles (STN_05 shown; the same cycle as every vehicle)
python -I tools/cue4parse_extractor/vehicle_meshes.py plan . all/files.txt vv stationary-stn-05
X vv/stationary-stn-05 mesh vv/stationary-stn-05/_inputs.txt --names normal-order.usmap
python -I tools/cue4parse_extractor/vehicle_meshes.py finish . vv stationary-stn-05
python -I _tools/vehicle_models.py --meshes vv stationary-stn-05       # --meshes: the folder holding <id>/manifest.json
python -I _tools/damage_tables.py --json
```

The character `SK_` meshes in `phys_in.txt` are read only for their `PhysicsAsset`; only the props' skeletal meshes place bodies.

## Checks run

- `python -I _tools/object_models.py --check`: current (32 buildable stage tables match `data/`).
- `python -I _tools/object_models_check.py --browser` (Edge, `PW_CHANNEL=msedge`): 46 objects, 44 GLBs, no images, textures or samplers; materials match the data; the page loads in Chromium, every object lists its pieces, a hash selects an object, a piece click shows its detail.
- `python -I _tools/infantry_regen_check.py`: OK. The infantry model check inside `infantry_tables.py`: 20 bodies, 0 mismatches.
- `python _tools/vehicle_impact_browser_check.py --out <dir> --no-screenshots`: passed (23 vehicles, 154 routing slots).
- `python _tools/vehicle_hit_location_check.py` needs `--native <dump>` (the lead's native dump): not run.
- `python -I _tools/check_links.py`: 0 broken.

## Open items

- Placement of the FOB's faction meshes (Blueprint not in `data/`).
- Whether a mesh with no simple shapes collides at all: the render-triangle case was not decoded.
- Foundations of the other buildables (`FoundationStaticMesh`, spawned when a stage sets `bShouldSpawnFoundations`) are in the collision export (`SM_Foundation_*`) but not placed in the models, because their relative placement is not in the stage data.
- The viewer has no damage routing or per-caliber hits to destroy for buildables; it shows the damage-row modifiers only.
