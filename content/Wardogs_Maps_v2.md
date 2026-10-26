---
title: "Maps"
redirect_from: ["/Wardogs_Maps_v2.html", "/Wardogs_Maps_v2"]
parent: "Game Modes & Maps"
description: "Inventory, Minimal Grid Test, Shooting-Range Moving Target, Water Gym"
---

# Wardogs — Maps & Gym Data Reference
*Extracted from the cooked JSON export under [`Content/Maps`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps) (12 files, 48 export blocks). Values are raw asset properties. Anything inferred from a name rather than from the export is marked as inferred. The `.umap` level files are not in this category, so this doc covers the data assets that sit beside the maps.*

> **Scope note:** this is the supporting data for the test gyms ([`Gyms/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps/Gyms)) and the per-map shader warmup manifests ([`PSOWarming/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps/PSOWarming)). The actual level layouts, actor placement, and gameplay rules are not in the export.

---

## Season 02 update (2026-10-15)

- **New sight blocker assets:** four `DA_SightBlockers_*` files for Europe, North America, Russia and Kavkazi. See [section 7](#7-sight-blockers-wdsightblockerbakedataasset).
- **New warmup manifest:** [`Russia_Moscow_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Russia_Moscow_KOTH_01.json) (1,132 graphics PSOs, 74 compute PSOs).
- **Kavkazi manifest is complete:** 867 graphics PSOs and 117 compute PSOs. The previous file stopped partway through the compute list, so the old 2,528 graphics count is withdrawn. See [section 6](#6-kavkazi_bakurani_koth_01-manifest).
- **Graphics PSO counts:** Madrid 1,639 to 1,053. Detroit 1,870 to 1,000. Kavkazi 2,528 to 867.
- **Compute PSO counts:** Madrid 6 to 83. Detroit 76 to 79.
- **Nanite vertex factory entries:** Madrid 1,152 to 824. Detroit 1,300 to 771. Kavkazi 1,016 to 624.
- **Local vertex factory entries:** Madrid 318 to 76. Detroit 150 to 82. Kavkazi 1,274 to 91.
- **Environment material entries:** Madrid 813 to 639. Detroit 835 to 603. Kavkazi 855 to 620.
- **Moving target:** two functions added, `Play pop up audio` and `Play Knock Down Audio`. See [section 3d](#3d-function-list).
- **Moving target offsets:** the root and base components' values are now exported as relative location (root X -10; base X 0.28, Z -5.47). Values are unchanged.
- **File count:** 7 files and 41 export blocks become 12 files and 48 export blocks.

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

---

## 1. Inventory

| File | Export type | What it is |
|---|---|---|
| [`Gyms/Minimal/DT_Gym_Minimal_GridTest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Minimal/DT_Gym_Minimal_GridTest.json) | `WDAutomationWorldGridData` | Grid of capture cells over the minimal test gym |
| [`Gyms/Range/Assets/B_MovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json) | `BlueprintGeneratedClass` ([`B_MovingTarget_C`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json)) | Moving shooting-range target actor |
| [`Gyms/Water/PDA_Flux_Gym_Water`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Water/PDA_Flux_Gym_Water.json) | `PDA_FluxSimulationState_C` | Fluid simulation settings and texture references for the water gym |
| [`Gyms/Water/WHG_PDA_Flux_Gym_Water`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Water/WHG_PDA_Flux_Gym_Water.json) | `WDWaterHeightGridAsset` | Water height grid (512 x 512 samples) for the water gym |
| [`PSOWarming/Europe_Madrid_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Europe_Madrid_KOTH_01.json) | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Madrid KOTH map |
| [`PSOWarming/NorthAmerica_Detroit_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/NorthAmerica_Detroit_KOTH_01.json) | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Detroit KOTH map |
| [`PSOWarming/Kavkazi_Bakurani_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Kavkazi_Bakurani_KOTH_01.json) | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Bakurani KOTH map (see section 6) |
| [`PSOWarming/Russia_Moscow_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Russia_Moscow_KOTH_01.json) | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Moscow KOTH map |
| [`SightBlockers/Europe/DA_SightBlockers_Europe`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/Europe/DA_SightBlockers_Europe.json) | `WDSightBlockerBakedDataAsset` | Sight blocker data for the Europe map (section 7) |
| [`SightBlockers/NorthAmerica/DA_SightBlockers_NorthAmerica`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/NorthAmerica/DA_SightBlockers_NorthAmerica.json) | `WDSightBlockerBakedDataAsset` | Sight blocker data for the North America map (section 7) |
| [`SightBlockers/Russia/DA_SightBlockers_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/Russia/DA_SightBlockers_Russia.json) | `WDSightBlockerBakedDataAsset` | Sight blocker data for the Russia map (section 7) |
| [`SightBlockers/kavkazi/DA_SightBlockers_Kavkazi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/kavkazi/DA_SightBlockers_Kavkazi.json) | `WDSightBlockerBakedDataAsset` | Sight blocker data for the Kavkazi map (section 7) |

---

## 2. Minimal Grid Test ([`DT_Gym_Minimal_GridTest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Minimal/DT_Gym_Minimal_GridTest.json))

| Field | Value |
|---|---|
| GridBoundsMin | X -12000, Y -12000, Z 0 |
| GridBoundsMax | X 14000, Y 14000, Z 8000 |
| GridCellsX / GridCellsY | 2 / 2 |
| LocationZOffset | 4500 |
| Rotator (Pitch / Yaw / Roll) | -90 / 0 / 0 |

**How to read it**

- The footprint is 26000 by 26000 units, split into a 2 by 2 grid. Each cell is therefore about 13000 by 13000 if the cells divide the bounds evenly. That split is inferred, not stated.
- The pitch of -90 points the view straight down. Combined with `LocationZOffset` 4500 and a Z range of 0 to 8000, this reads as a top-down capture rig that hovers 4500 units above the grid. The name `WDAutomationWorldGridData` and the "GridTest" name suggest it is a tool for automated capture of the gym, but that purpose is inferred from the name.
- Units are not stated. They are presumed to be Unreal centimetres, which is the engine default.

---

## 3. Shooting-Range Moving Target ([`B_MovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json))

The moving target is a blueprint actor. The export includes its class defaults, its components, its one timeline, and the names of its functions. The function bodies (graph logic) are not in the export, so only the data is documented here.

### 3a. Class defaults

| Property | Value | Notes |
|---|---|---|
| Health | 1.0 | Units not stated |
| DamageIncrease | 3.5 | Units and meaning not stated |
| TimeToReachTargetRange | Min 15, Max 25 | Likely seconds (inferred from name). The range is consumed by [`GetTimeToReachTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json) |
| StartingLocation | (0, 0, 0) | |
| bReplicates | True | |
| RemoteRole | `ROLE_SimulatedProxy` | |

### 3b. Components

| Component | Class | Mesh | Notes |
|---|---|---|---|
| Root_GEN_VARIABLE | StaticMeshComponent | `Cube` | Relative location X -10. Child of DummyRoot in the component hierarchy |
| Cube2_GEN_VARIABLE | StaticMeshComponent | `SM_Target_Base` | Relative location X 0.28, Z -5.47. Base of the target stand (inferred from name) |
| Cube3_GEN_VARIABLE | StaticMeshComponent | `SM_Target_Rail` | Rail piece (inferred from name) |
| RotatePoint_GEN_VARIABLE | StaticMeshComponent | `SM_Target_01a` | Target face. Its pivot role is inferred from the variable name |
| DefaultSceneRoot_GEN_VARIABLE | SceneComponent | - | Scene root of the actor (`SCS_Node_0`) |
| DummyRoot_GEN_VARIABLE | SceneComponent | - | Parent of the Root mesh node |
| MovePoint_GEN_VARIABLE | SceneComponent | - | Movement pivot |
| LeftMoveLocation / RightMoveLocation_GEN_VARIABLE | SceneComponent | - | The two end points of the horizontal move. LeftMoveLocation relative location X -0.41, Z 12.23 |

### 3c. Timeline and curve

| Item | Value |
|---|---|
| Timeline name | `TargetFall` (template [`TargetFall_Template`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json)) |
| TimelineLength | 0.5 |
| Track | `FallRate` on `CurveFloat_0` |
| Curve keys | (t 0.0, value 0.0) to (t 0.5, value 1.0), cubic interpolation, auto tangents |
| Bound functions | [`TargetFall__UpdateFunc`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`TargetFall__FinishedFunc`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json) |

The fall plays out over half a second. The rate curve goes from 0 to 1 over the length of the timeline.

### 3d. Function list

[`SetMovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`GetTimeToReachTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`OnMovingTargetUpdated`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`TakeDamage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`ReceiveDamage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`Knockdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`Popup`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`Play pop up audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`Play Knock Down Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), `ReceiveBeginPlay`, [`ExecuteUbergraph_B_MovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`TargetFall__UpdateFunc`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json), [`TargetFall__FinishedFunc`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json).

Function names only. The export has no graph nodes, so the actual formula for time-to-target or the damage math is not in the export.

---

## 4. Water Gym ([`PDA_Flux_Gym_Water`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Water/PDA_Flux_Gym_Water.json) and [`WHG_PDA_Flux_Gym_Water`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Water/WHG_PDA_Flux_Gym_Water.json))

Two assets make up the water gym. The first is the fluid simulation state. The second is a precomputed height grid.

### 4a. Fluid simulation state (`PDA_FluxSimulationState_C`)

| Property | Value |
|---|---|
| Static | True |
| Resolution | 2048 x 2048 |
| AreaLocation | (0, 0.0000198, 4178.24) |
| AreaSize | 102400 x 102400 x 6400 |
| EncodeVelocityMax | 5.0 |
| EncodeHeightMax | 256.0 |
| IterationDeltaTime | 0.18 |
| CaptureOffset | -621.76 |
| Compression | True |
| Iteration | 101594 (meaning not stated) |
| GroundMap texture | `PDA_Flux_Gym_Water_Ground` |
| VelocityDepthFoamMap texture | `PDA_Flux_Gym_Water_Velocity` |
| HeightWetMap texture | `PDA_Flux_Gym_Water_Height` |

**Notes**

- The simulated area is 102400 units square (1024 m if the unit is centimetres), at a 2048 by 2048 resolution. That is 50 units per texel.
- `EncodeHeightMax` 256 and `EncodeVelocityMax` 5 look like the range that the height and velocity textures are encoded over. How the values are decoded is not in the export, so that mapping is inferred.
- `Iteration` 101594 is a large count whose meaning is not stated. It could be a simulation step counter or a precomputed iteration budget. It is not interpreted here.

### 4b. Height grid (`WDWaterHeightGridAsset`)

| Property | Value |
|---|---|
| WorldSize | 102400 x 102400 |
| GridWidth | 512 |
| Origin | (-51200, -51200), half the world size, so the grid is centred on the origin |
| Sample array | 262,144 values (512 x 512), stored as unsigned 16-bit |
| Linked asset | [`PDA_Flux_Gym_Water`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Water/PDA_Flux_Gym_Water.json) (the sim state in 4a) |

**Sample distribution (from the array)**

| Value | Count | Share |
|---|---|---|
| 65535 | 249,869 | 95.3% |
| 65501 | 255 | 0.1% |
| 63687 | 143 | 0.05% |
| 65132 | 73 | 0.03% |

There are 5,413 distinct values in total, and the minimum is 0.

**Notes**

- 95.3% of the grid is exactly 65535, which is the maximum unsigned 16-bit value. That is most likely a "no water here" sentinel or the dry-ground value, with the remaining samples holding the actual water surface. This is inferred from the distribution. The export does not say what 65535 means, and it has not been decoded to world heights.
- Two unnamed float values are stored under unnamed fields: -2216.76 and 2046.39. They are probably the minimum and maximum of the height range, but that is not verified. The export's `CaptureOffset` in 4a is -621.76, and the two values do not obviously relate to it.

---

## 5. Shader/PSO Warmup Manifests (`WDPSOWarmupDataAsset`)

Four per-map manifests list the materials and vertex factories that the map uses, and the compute shaders it needs. The asset type and the `PSOWarming` folder suggest they are used to pre-compile pipeline state objects before a match starts. That purpose is inferred from the names.

Each manifest has the same structure:

- `WorldData`: the world asset (`/Game/Maps/Worlds/...`) and the experience name.
- `GraphicsPSOs`: one entry per material, with its `MatObjectPath` and the `VertexFactories` it is drawn with.
- `ComputePSOs`: a list of compute shader names.

### 5a. Summary

| Manifest | Experience name | World | Graphics PSOs | Compute PSOs | Status |
|---|---|---|---|---|---|
| [`Europe_Madrid_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Europe_Madrid_KOTH_01.json) | Madrid_KOTH_01 | `/Game/Maps/Worlds/Europe/Europe` | 1,053 | 83 | Complete |
| [`NorthAmerica_Detroit_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/NorthAmerica_Detroit_KOTH_01.json) | Detroit_KOTH_01 | `/Game/Maps/Worlds/NorthAmerica/NorthAmerica` | 1,000 | 79 | Complete |
| [`Kavkazi_Bakurani_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Kavkazi_Bakurani_KOTH_01.json) | Bakurani_KOTH_01 | `/Game/Maps/Worlds/Kavkazi/Kavkazi` | 867 | 117 | Complete, see section 6 |
| [`Russia_Moscow_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Russia_Moscow_KOTH_01.json) | Moscow_KOTH_01 | `/Game/Maps/Worlds/Russia/Russia` | 1,132 | 74 | Complete |

The experience name for the Kavkazi file is `Bakurani_KOTH_01`, which differs from the file name. The Russia file's experience name is `Moscow_KOTH_01`. The file name and the experience name are both kept as they appear in the export.

### 5b. Vertex factory usage (per GraphicsPSO entry)

A PSO can list more than one vertex factory, so these counts add up to more than the PSO totals.

| Vertex factory | Madrid | Detroit | Kavkazi | Russia |
|---|---|---|---|---|
| `FNaniteVertexFactory` | 824 | 771 | 624 | 887 |
| `FLocalVertexFactory` | 76 | 82 | 91 | 103 |
| `TGPUSkinVertexFactoryDefault` | 116 | 120 | 118 | 114 |
| `FInstancedStaticMeshVertexFactory` | 41 | 33 | 39 | 46 |
| `FSplineMeshVertexFactory` | 19 | 14 | 22 | 19 |
| `FNiagaraSpriteVertexFactory` | 13 | 12 | 14 | 13 |
| `FNiagaraMeshVertexFactory` | 1 | 1 | 2 | 1 |

Nanite is the most common vertex factory in all four manifests. The local vertex factory is most common in Russia (103).

### 5c. Material folders (top eight by top-level folder under `/Game`)

| Folder | Madrid | Detroit | Kavkazi | Russia |
|---|---|---|---|---|
| Environment | 639 | 603 | 620 | 700 |
| Maps | 230 | 217 | 59 | 251 |
| Characters | 111 | 116 | 114 | 113 |
| Megascans | 23 | 21 | 26 | 30 |
| VFX | 19 | 13 | 15 | 14 |
| FluidFlux | 6 | 6 | 6 | 0 |
| Materials | 4 | 6 | 4 | 6 |
| WorldBuilding | 5 | 5 | 7 | 4 |

These are the eight folders with the largest counts across the four manifests. Russia has the most Environment (700) and Maps (251) materials. Detroit has the most Characters (116). Kavkazi has the fewest Maps (59) and the most WorldBuilding (7). Kavkazi has the smallest total (867 graphics PSOs).

### 5d. Compute PSO names (sample)

| Manifest | Examples in the list |
|---|---|
| Madrid (sample of 83) | `FAllocatePagesCS`, `FBuildGridTilesCS`, `FLumenCardCS`, `FScreenProbeTemporalReprojectionCS`, `FVolumetricFogLightScatteringCS`, `FNiagaraShader`, `TBasePassCSFNoLightMapPolicyVoxel` |
| Detroit (sample of 79) | `FAllocatePagesCS`, `FBuildHeightfieldComposeTilesCS`, `FBuildIndirectDispatchArgsBufferCS`, `FLumenCardCS`, `FHZBBuildCS`, `FNiagaraShader`, `TBasePassCSFNoLightMapPolicyVoxel` |
| Kavkazi (sample of 117) | `FBuildFeedbackHashTableCS`, `FLumenCardBatchDirectLightingCS`, `FScreenProbeComputeLightingProbabilityDensityFunctionCS`, `FHZBBuildCS`, `TBasePassCSFNoLightMapPolicyVoxel` |
| Russia (sample of 74) | `FAllocatePagesCS`, `FClearProbeFreeList`, `FClearReplacementCS_Texture2D_Float4_Bounds`, `FLumenReflectionDenoiserTemporalCS`, `FHZBBuildCS`, `FNiagaraShader`, `TBasePassCSFNoLightMapPolicyVoxel` |

Lumen-named compute entries: Madrid 4, Detroit 3, Kavkazi 13, Russia 4. Kavkazi has the most compute entries of the four manifests (117).

---

## 6. Kavkazi_Bakurani_KOTH_01 manifest

The file is 216,911 bytes and parses as complete JSON.

- **Header and WorldData:** experience name `Bakurani_KOTH_01`, world `/Game/Maps/Worlds/Kavkazi/Kavkazi`.
- **GraphicsPSOs:** **867 entries**. Each entry has a `MatObjectPath` and a `VertexFactories` list.
- **ComputePSOs:** **117 entries**.

The counts in section 5 come from this file.

---

## 7. Sight Blockers (`WDSightBlockerBakedDataAsset`)

Four baked data assets, one per map. Each has the same shape: a world reference, a bounds box (`Min` and `Max`), an `IsValid` flag, and several numeric fields with no readable names. The export does not say what the sight blockers are used for.

| File | World | Bounds Min (X, Y, Z) | Bounds Max (X, Y, Z) | Unnamed field 1 | Unnamed field 2 |
|---|---|---|---|---|---|
| [`SightBlockers/Europe/DA_SightBlockers_Europe`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/Europe/DA_SightBlockers_Europe.json) | `/Game/Maps/Worlds/Europe/Europe` | -729935.1, -673922.44, -110735.72 | -546697.2, -548435.56, -71294.94 | 3125 | 384 |
| [`SightBlockers/NorthAmerica/DA_SightBlockers_NorthAmerica`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/NorthAmerica/DA_SightBlockers_NorthAmerica.json) | `/Game/Maps/Worlds/NorthAmerica/NorthAmerica` | -181848.62, -287751.4, -48359.086 | -55560.918, -131958.1, 55640.914 | 2880 | 185 |
| [`SightBlockers/Russia/DA_SightBlockers_Russia`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/Russia/DA_SightBlockers_Russia.json) | `/Game/Maps/Worlds/Russia/Russia` | -90184.53, -84857.62, -38785.887 | 59737.117, 55525.145, 72420.54 | 4833 | 708 |
| [`SightBlockers/kavkazi/DA_SightBlockers_Kavkazi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/kavkazi/DA_SightBlockers_Kavkazi.json) | `/Game/Maps/Worlds/Kavkazi/Kavkazi` | -888067.25, -1175312.1, -114160.0 | -758231.7, -1046870.4, -76160.0 | 4546 | 813 |

**Notes**

- `IsValid` is 1 in all four assets.
- Each asset also holds a block of seven unnamed fields. Their values are not decoded here.
- The bounds use the same units as the other map data (presumed Unreal centimetres, as in section 2). The export does not state units.

## 8. How Values Combine

- **Water gym:** the fluid sim (4a) runs over a 102400-unit area at 2048 by 2048. The height grid (4b) covers the same 102400-unit world size at 512 by 512, which is a coarser sampling of the same area (one height sample per 200 units, versus one sim texel per 50 units). How the grid is used at runtime is not in the export.
- **Moving target:** the timeline (3c) runs its fall over 0.5 seconds. The move range is 15 to 25 (3a), and the actual choice of time within that range happens in the blueprint graph, which is not exported.
- **PSO manifests:** a map's effective warmup is the union of its graphics and compute entries. The vertex-factory counts in 5b show which rendering paths the map needs.

---

## 10. Placed wall and building materials (round 65)

Read from the cooked World Partition cell packages of the four worlds (`Content/Maps/Worlds/<World>/<World>/_Generated_/*.umap`, about 40,000 cells; static-mesh instances in `InstancedStaticMeshComponent`, `HierarchicalInstancedStaticMeshComponent`, `StaticMeshComponent` and spline-mesh exports). Each mesh's `StaticMaterials` slots (with any component `OverrideMaterials` applied) were followed through the material `Parent` chain to the first `PhysMaterial`. Full data: [`assets/data/map-cover-materials.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-cover-materials.json); method and caveats: [`docs/evidence/round65-open-questions.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round65-open-questions.md).

A piece is one placed instance. Wall and building pieces are meshes under `Environment/Architecture`, `ExternalAssets`, `Props/Walls_and_Fences` and `Transport_Infrastructure/Road_Barriers`; HLOD proxies, foliage, landscape, roads, other props and the `WDTraversal` collision helper blocks are not counted. A piece is counted under every physical material its mesh uses (the rows add up to more than the total). `play` scope is the zone-region bounding box plus 500 m; Saburtulo has no region list, so only `world` scope exists for it.

| Map (world) | Scope | Wall and building pieces | Built-up area (km) | Pieces with this physical material (top five) |
|---|---|---:|---|---|
| Bakurani (Kavkazi) | play | 109,586 | 7.8 x 7.7 | Wood 30,535, Concrete 25,274, Brick 24,195, Metal 23,380, Plaster 7,960 |
| Ozeti (Europe) | play | 69,833 | 6.6 x 4.3 | Wood 21,921, Brick 16,523, Concrete 14,051, Metal 12,286, Plaster 5,370 |
| Zestafona (NorthAmerica) | play | 98,745 | 6.7 x 5.9 | Metal 39,303, Concrete 28,672, Wood 17,185, Brick 12,525, Plaster 3,716 |
| Saburtulo (Russia) | world | 189,545 | 5.0 x 4.6 | Concrete 60,809, Wood 49,790, Brick 49,470, Metal 31,000, Plaster 11,151 |

The `none` entry (mesh decals with no physical material anywhere in their parent chain) is left out of the table. Component centres, not single instances, decide the `play` scope (an approximation). Buildings that break apart are produced by the demolition system at run time (`BHDemolitionCellProxyActor` cells are markers only), so their pieces are not in these counts.


---

## 11. Placed gameplay actors (round 66)

Read from the same cooked World Partition cells as section 10 (`Content/Maps/Worlds/<World>/<World>/_Generated_/*.umap`, plus the GameFeatures external data layer cells of the same world, which hold the zone object, the Hot Zone Magnets and the PvE, range and Sniper Showdown content). Every export that is a placed actor (its outer is the persistent level) was recorded with its class and the root component `RelativeLocation`; child actors (single doors, windows) take the position of the parent building. Raw output is kept outside the repository. Full data: [`assets/data/map-gameplay-actors.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-gameplay-actors.json); method, statuses and caveats: [`docs/evidence/round66-map-actors.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round66-map-actors.md). Spawn volumes, boards and infantry spawn spots per area are in [`assets/data/vehicle-spawns.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-spawns.json) (round 51) and are not repeated; the board and spawn-area rows below are counts only.

Cells are `play / world`: `play` is the zone-region bounding box plus 500 m (the section 10 scope), `world` is the whole world package (shared with other maps: Mindori, Tevza and Bakurani Outskirts - Jutari use the Kavkazi world, Berlin and Paris the Europe world). Saburtulo has no region list, so only `world` is given (`-` for play).

| Class | Blueprint | Bakurani | Ozeti | Zestafona | Saburtulo |
|---|---|---:|---:|---:|---:|
| Hot Zone Magnet tower | `B_HotZoneMagnet_C` (`HotZoneTowerNumber` 1..N, external data layer cells of the HotZoneMagnet game feature) | 5 / 5 | 4 / 4 | 3 / 3 | - / 5 |
| Zone object | `B_ControlZone_C` (ControlZone layer; the Europe world has two; the Sniper Showdown ones are in other buckets) | 1 / 1 | 1 / 2 | 1 / 1 | - / 1 |
| Single door (child of a building) | `B_Door_C` | 180 / 376 | 150 / 250 | 76 / 144 | - / 303 |
| Apartment door | `BP_InteractableDoor_Apartment_C` | 64 / 64 | 25 / 25 | 25 / 27 | - / 63 |
| Balcony door | `BP_InteractableDoor_ApartmentBalcony_C` | 0 / 80 | 0 / 39 | 0 / 22 | - / 73 |
| Apartment entrance door | `BP_InteractableDoor_ApartmentEntrance_C` | 4 / 22 | 2 / 12 | 2 / 76 | - / 8 |
| Office door | `BP_InteractableDoor_Office_C` | 0 | 0 | 153 / 153 | - / 17 |
| Shop door | `BP_InteractableDoor_Buisness_C`, `BP_Interactable_Commercial_Door_01a_L/R_C` | 0 | 0 | 0 | - / 10 |
| Hospital door (leaf) | `BP_Interactable_HospitalDoor_01a_Left/Right_C` | 0 | 0 | 0 | - / 38 |
| Wooden door | `BP_Interactable_Door_Wood_01a_C` | 0 | 0 | 0 | - / 2 |
| Garage door leaf | `BP_Interactable_GarageDoor_01a_Left/Right_C` | 70 / 86 | 22 / 46 | 6 / 6 | - / 44 |
| Ladder | `BP_Ladder_C`, `B_Mover_Ladder_BlockOut_C` | 54 / 100 | 22 / 34 | 88 / 98 | - / 40 |
| Breakable window | `B_Smashable*_C` | 1,916 / 3,779 | 1,425 / 2,358 | 1,219 / 1,699 | - / 2,687 |
| Destructible building | any actor carrying `BHDestructionBuildingEditorComponent`, doors excluded | 264 / 446 | 247 / 354 | 161 / 224 | - / 378 |
| Demolition cell marker | `BHDemolitionCellProxyActor` | 152 / 373 | 118 / 249 | 144 / 343 | - / 251 |
| Pre-placed barbed wire | `B_BarbedWire_Damage_Volume_C` | 33 / 161 | 32 / 32 | 41 / 73 | - / 52 |
| Lake | `BP_WaterLake_C` | 3 / 3 | 0 | 0 | 0 |
| River section | `BP_FluxSurface_River_C` | 6 / 23 | 4 / 17 | 3 / 14 | 0 |
| Swimming pool building | `B_SwimPool_Building_01_C` | 0 | 1 / 1 | 0 | 0 |
| Supply building | `B_SupplyBuilding_01/02(b)_C` | 0 | 1 / 1 | 1 / 3 | - / 10 |
| Infantry spawn area | `B_SpawnManager_C` (all areas in the world file) | 0 / 7 | 1 / 8 | 0 / 3 | - / 3 |
| Spawn safe zone | `B_SafeZone_C` | 0 / 7 | 1 / 8 | 0 / 3 | - / 3 |
| Deployment board | `B_VehicleDeploymentBoard_*_C` | 0 / 7 | 1 / 8 | 0 / 3 | - / 3 |
| Equipment vendor | `B_EquipmentVendor_C` | 0 / 7 | 1 / 8 | 0 / 3 | - / 3 |
| Vehicle vendor | `B_VehicleVendor_C` | 0 / 7 | 1 / 8 | 0 / 3 | - / 3 |
| Garage vendor | `B_GarageVendor_C`, `B_GarageVendor_01_C` | 0 / 7 | 1 / 8 | 0 / 3 | - / 3 |
| Wager vendor | `B_WagerVendor_C` | 0 / 6 | 0 / 3 | 0 / 3 | - / 3 |
| Free fuel point | `B_SpawnFuelItemRefill_C` | 0 / 6 | 0 / 3 | 0 / 3 | 0 |
| Soccer pitch | `B_WDSoccerField_C` | 0 / 6 | 0 / 3 | 0 / 3 | - / 3 |
| Moving practice target | `B_MovingTarget_C` | 0 / 18 | 0 / 9 | 0 / 9 | - / 9 |
| Conversation point | `B_Conversation_Kaiser_Djinn_C` | 0 | 1 / 4 | 0 | 0 |
| Mini digger prop | `BP_MiniDigger_01_C` | 0 | 0 | 2 / 2 | 0 |
| Decorative vehicle prop (art) | `PropVehicle_C`, `BP_BasicVehicleProp_C` | 458 / 718 | 381 / 543 | 510 / 589 | - / 803 |
| Fly-through trigger (art) | `B_FlyThroughTrigger_C` | 5 / 9 | 7 / 16 | 11 / 17 | 0 |

**Main-map spawn areas.** Spawn areas that hold a wager vendor within 150 m (an inferred rule: only the named map's areas have one; the rest of the world file serves the other maps): Bakurani 6, Ozeti 3, Zestafona 3, Saburtulo 3. Each such area holds one board, one equipment vendor, one vehicle vendor, one garage vendor and one wager vendor, and, with exceptions, one safe zone, one soccer pitch, three moving targets and one fuel point. Totals over those areas: Bakurani: deployment board 6, equipment vendor 6, fuel point 6, garage vendor 6, moving target 18, safe zone 5, soccer pitch 6, vehicle vendor 6, wager vendor 6; Ozeti: deployment board 3, equipment vendor 3, fuel point 3, garage vendor 3, moving target 9, safe zone 2, soccer pitch 2, vehicle vendor 3, wager vendor 3; Zestafona: deployment board 3, equipment vendor 3, fuel point 3, garage vendor 3, moving target 9, safe zone 3, soccer pitch 3, vehicle vendor 3, wager vendor 3; Saburtulo: deployment board 3, equipment vendor 3, garage vendor 3, moving target 9, safe zone 3, soccer pitch 3, vehicle vendor 3, wager vendor 3. No main-map spawn area lies inside the `play` box (Ozeti has one non-main area inside it).

**Other buckets (not in the totals).** Bakurani (Kavkazi) world cells also hold PvE scenario layers: VIPEscort_01 (95 PvE AI spawners, 69 pre-placed buildables, 6 vehicle spawners, 2 quest points, an equipment vendor and a spawn area), StrikeDisarm_01 (53 AI spawners plus one wave trigger, 5 vehicle spawners, a laptop objective, 2 quest points, a ladder, vendors) and ScenarioExample (a quest area and a quest point). The Sniper Showdown layers add one zone object per world (Kavkazi, NorthAmerica, Russia). The shooting range and tutorial layers hold the `B_ShootingRange*` and `B_ShootingRangeTutorial*` actors and are not counted.

**Absent on all four maps.** Capture towers other than the Hot Zone Magnet, pre-placed static weapons or emplacements, ammo or supply pickup points, loot or crate actors, zip lines. The only free resupply object is the fuel point (`B_Item_RefuelComponent_C`: infinite fuel, free in spawn, `RefuelPerUpdate` 2, `PricePerLiter` 2), absent on Saburtulo. Barbed wire is a pre-placed `B_BarbedWire_Damage_Volume_C` trigger (flat player damage 8, vehicle damage 10 percent with a 15 percent floor, a slow effect).

**Limits.** (a) Positions are actor roots; a child actor with no own location uses its parent building. (b) The `play` box is a rectangle, not the real zone shape. (c) Which cells belong to which of the maps sharing a world is not in the cells; the spawn-area attribution is inferred. (d) Water: only `BP_WaterLake_C` and `BP_FluxSurface_River_C` actors were counted; water drawn by the landscape or a material would not show (Saburtulo has none of either). (e) PvE and range cells are listed separately and are not part of a King of the Hill map.

---

## 12. Hot Zone Magnet towers, map extents and server-browser-only entries (round 67)

Static read of the same cooked cells as sections 10 and 11, the landscape components of the four worlds, the Hot Zone Magnet Blueprints and the native `HotZoneMagnetRuntime` module. Evidence and method: [`docs/evidence/round67-maps.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round67-maps.md). Data: [`assets/data/map-magnets-extents.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-magnets-extents.json). Positions are world metres (x, y, z) as stored, with no stated north.

Round 66 inferred that the placed `B_HotZoneMagnet_C` actors are the capture towers behind the tower rewards; this section settles it from the Blueprint and the native class (`AWDHotZoneMagnet`).

### 12a. Tower system values

| Value | Setting | Source |
|---|---|---|
| Capture | Hold, 10.0 s, range 250 cm, one interactor at a time | `DA_HotzoneMagnet_Interactions` (`Interaction.Context.WorldFeatures.TowerControl`) |
| Keypad key | Tap, 0.3 s, range 250 cm; keys 0 to 9, CLEAR, ENTER | `DA_HotzoneMagnetHitInput_Interactions`, `W_HotZoneMagnet_Keyboard` |
| Code | One digit 0 to 9 per tower, drawn on the server at match start and again when the recharge timer ends | native `0x856D9A0` (static disassembly) |
| Partial code | Digits shown for owned towers if the map has at least 4 towers, otherwise only when all towers are owned | static dword at RVA `0xCF377C8` = 4 in the restored image; `0x8573500` |
| Wrong codes before a lock | 3 (`HotZoneMagnetCodeMaxAttempts`, constructor `0x8565CF0`) | native default |
| Lock time | 30.0 s (Blueprint `HotZoneMagnetCodeAttemptsTimePenalty`; native default 5.0) | `B_HotZoneMagnet` |
| Reward range | 8000 cm (`HotZoneTowerRewardRange`, constructor `0x8565CF0`) | native default |
| Magnet active | 180 s (`ActivatedHotZoneMagnetDuration`) | `B_HotZoneMagnetGameStateComponent` |
| Recharge | 900 s (`TowerControlRechargeDuration`), started when the magnet deactivates (`0x8570080`) | `B_HotZoneMagnetGameStateComponent` |
| Hot Zone speed and size | 3.0 m/s, (0.6, 0.6, 1.0) | round 45 and 46 |
| Switch-off by players | `bCanDeactivateMagnet` false (constructor) | native default |
| Reward repeat cooldown | 180 s (`RepeatActionsCooldown` in `ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_TowerCaptured`) | cooked data |

### 12b. Tower positions

| Map | Tower | x (m) | y (m) | z (m) | Region it stands in | From region centre (m) | From zone area centre (m) |
|---|---:|---:|---:|---:|---|---:|---:|
| Bakurani | 1 | -8297 | -11041 | -917 | TOWER 1 | 2 | 160 |
| Bakurani | 2 | -8627 | -11050 | -928 | TOWER 2 | 19 | 360 |
| Bakurani | 3 | -8628 | -11398 | -927 | TOWER 3 | 18 | 382 |
| Bakurani | 4 | -7990 | -11333 | -917 | TOWER 4 | 17 | 337 |
| Bakurani | 5 | -8127 | -10892 | -926 | LUMBERYARD NORTH | 39 | 354 |
| Ozeti | 1 | -6614 | -6102 | -911 | Tower 1 | 15 | 238 |
| Ozeti | 2 | -6163 | -5742 | -925 | Tower 2 | 6 | 426 |
| Ozeti | 3 | -5749 | -6183 | -903 | Tower 3 | 2 | 632 |
| Ozeti | 4 | -6131 | -6577 | -887 | Tower 4 | 11 | 526 |
| Zestafona | 1 | -1332 | -2223 | 109 | Tower 1 | 13 | 260 |
| Zestafona | 2 | -903 | -2315 | 97 | Tower 2 | 17 | 288 |
| Zestafona | 3 | -1175 | -1825 | 95 | Tower 3 | 12 | 289 |
| Saburtulo | 1 | -108 | -145 | 176 | none (no region list) | - | 113 (from zone object) |
| Saburtulo | 2 | 187 | 65 | 166 | none (no region list) | - | 389 (from zone object) |
| Saburtulo | 3 | -362 | 316 | 155 | none (no region list) | - | 416 (from zone object) |
| Saburtulo | 4 | -560 | -307 | 211 | none (no region list) | - | 452 (from zone object) |
| Saburtulo | 5 | 8 | -333 | 164 | none (no region list) | - | 333 (from zone object) |

Bakurani tower 5 stands in LUMBERYARD NORTH, 78 m from the centre of the small region TOWER 5 L; the region list also holds TOWER 7, where no tower is placed. The zone area centre is the centre of the bounding box of all region points: Bakurani (-8301, -11201), Ozeti (-6376, -6111), Zestafona (-1100, -2105).

### 12c. Map extents

| Map (world) | Landscape | Landscape pieces | Play box | Play box size (km) | Ground z in play box (m) | Ground z, whole landscape (m) |
|---|---|---:|---|---|---|---|
| Bakurani (Kavkazi) | 16.32 x 16.32 km | 256 of 1020 m | zone regions plus 500 m | 3.33 x 3.45 | -991 to -278 | -1008 to 178 |
| Ozeti (Europe) | 16.32 x 16.32 km | 1024 of 510 m | zone regions plus 500 m | 3.8 x 2.95 | -988 to -759 | -1037 to -275 |
| Zestafona (NorthAmerica) | 16.32 x 16.32 km | 1024 of 510 m | zone regions plus 500 m | 3.46 x 3.25 | 44 to 251 | 25 to 707 |
| Saburtulo (Russia) | 16.32 x 16.32 km | 1024 of 510 m | five magnets and the zone object plus 500 m (stand-in, no region list) | 1.75 x 1.65 | 132 to 318 | 83 to 766 |

Heights are `LandscapeComponent.CachedLocalBox` min and max z, scaled by the landscape actor scale and offset by its location (z = location z + scale z x local z). The check is that every placed tower lies inside the height range of the piece under it (Bakurani, Ozeti) or within about 16 m above it (Zestafona). Pieces are 1020 m wide on Bakurani and 510 m elsewhere, so a range is an outer bound for the box. Saburtulo has no region list; its box is the five towers and the zone object plus 500 m (a stand-in).

### 12d. Server-browser-only entries

| Entry | World | Spawn layers named in the experience | Distance of each placed spawn point from the zone area centre (m) |
|---|---|---|---|
| Mindori | Kavkazi | DL_KhevuliSpawn, DL_LiknisiSpawn, DL_BaghiSpawn | DL_KhevuliSpawn 3807, DL_LiknisiSpawn 2798, DL_BaghiSpawn 3939 |
| Tevza | Kavkazi | DL_VostimiSpawn, DL_EdemiSpawn, DL_ShovliSpawn | DL_VostimiSpawn not placed, DL_EdemiSpawn not placed, DL_ShovliSpawn not placed |
| Berlin | Europe | DL_StuttgartSpawn, DL_HanoverSpawn, DL_BremenSpawn | DL_StuttgartSpawn 1573, DL_HanoverSpawn 2358, DL_BremenSpawn 4378 |
| Paris | Europe | DL_RennesSpawn, DL_CalaisSpawn, DL_GranadaSpawn | DL_RennesSpawn 4027, DL_CalaisSpawn 5278, DL_GranadaSpawn 3522 |

No experience in this group names a zone configuration. Each world file holds one zone object (Bakurani config and Kavkazi region list; Europe config and region list), so the zone area is the main map's (inferred). The Bakurani region list holds MindoriVillage, MindoriHillside1 and MindorHillside2, about 0.9 km from the zone area centre; no region carries the name Tevza, Berlin or Paris.

## 13. Play-area boundary and spawn safe zones (round 68)

Static analysis only; nothing was run. Raw output is outside the repository. Summary data: [map-boundaries.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-boundaries.json). Evidence: [round68-boundaries.md](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round68-boundaries.md).

**Boundary rectangle.** Each world's `WDWorldSettings` holds `bUseOutOfBounds` (true in all four worlds) and `PlayableBoundsExtent`, a 2D box (X and Y only, no height). Units are cm in the export; metres below.

| Map (world) | X from / to (m) | Y from / to (m) | Size (km) | Round 67 play box inside it, gap W / E / S / N (m) | Kill Z (m) |
|---|---|---|---|---|---|
| Bakurani (Kavkazi) | -14,000 / -3,000 | -17,000 / -6,000 | 11.0 x 11.0 | 4,033 / 3,634 / 4,075 / 3,477 | -1,500 |
| Ozeti (Europe) | -10,423 / -1,905 | -9,758 / -2,010 | 8.52 x 7.75 | 2,146 / 2,571 / 2,174 / 2,628 | -1,500 |
| Zestafona (NorthAmerica) | -6,200 / 4,300 | -6,000 / 3,200 | 10.5 x 9.2 | 3,370 / 3,670 / 2,272 / 3,682 | -1,500 |
| Saburtulo (Russia) | -6,600 / 6,600 | -6,600 / 6,600 | 13.2 x 13.2 | 5,540 / 5,913 / 5,767 / 5,784 (stand-in play box) | not set (engine default) |

**Timers.** A character that is outside the rectangle, or that carries the hostile safe zone tag, runs a timer up at 1 s per second. The limit is 20 s (`B_WDMoverPlayerCharacter` value; native default 10 s). Back inside, the timer counts down at 1 s per second. At the limit the server kills the character. A vehicle uses the same test with a native default limit of 22 s (Blueprint overrides not read); at the limit the server calls a destroy-like call on its health component. The HUD shows "Return to the Combat Area" (message display length 5 s) and a countdown.

**Safe zone actor.** `B_SafeZone_C` (parent `WDSafeZoneVolume`): faction tag, tag applied to the faction's players (`State.Location.SafeZone.<Faction>`), tag applied to other factions (`State.Location.SafeZone.Hostile`), no effects. The box is the default 32 cm half extent times the placed scale (inferred; the extent is not stored).

| Map | Safe zones near the main spawn areas | Size (m wide x deep x tall) |
|---|---|---|
| Bakurani | 6 | 3 x 640 x 640 x 480, 3 x 480 x 480 x 480 |
| Ozeti | 3 | 3 x 480 x 480 x 480 |
| Zestafona | 3 | 3 x 480 x 480 x 480 |
| Saburtulo | 3 | 3 x 800 x 800 x 480 |

**Spawn-area extras.** Soccer pitch `B_WDSoccerField_C`: bounds box 40 x 30 x 10 m, two goal boxes (1 x 8 x 3 m) at 15.5 m from the centre, ball reset 3.0 s after the ball leaves the bounds box, goal award 50 (scorer) and 25 (assist) pre-lobby points. Moving target `B_MovingTarget_C`: health 1, crossing time 15 to 25 s, fall 0.5 s, award equal to the truncated damage of the hit as pre-lobby points (reason Shooting), none for melee or fists. 15 pitches and 45 targets in the four worlds.

## 14. Spawn distances, light and weather, match start (round 70)

Static analysis only. Evidence: [`round70-maps-matchstart.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round70-maps-matchstart.md). Data: [`map-spawn-distances.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-spawn-distances.json), [`map-light-weather.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-light-weather.json), [`match-start.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/match-start.json).

### 14a. Distance from each spawn area to the zone area and the nearest Hot Zone Magnet tower

Straight-line metres on the map plane. Spawn position is the infantry spawn manager of the side's data layer (the middle of the spawn grid, inferred); the deployment board is within about 60 m of it. The zone area middle is the middle of the box around all zone regions (Saburtulo: the placed zone object, inferred).

| Server browser entry | Spawn area | Team slot | To zone area middle (m) | To nearest tower (m) | Nearest tower |
|---|---|---|---:|---:|---:|
| Bakurani_KOTH_01 | Khevuli | Bravo | 3807 | 3501 | 4 |
| Bakurani_KOTH_01 | Chuta | Charlie | 4131 | 3781 | 3 |
| Bakurani_KOTH_01 | Baghi | Alpha | 3939 | 3607 | 5 |
| Bakurani_KOTH_02 | Rachuri | Bravo | 3851 | 3525 | 4 |
| Bakurani_KOTH_02 | Tavarshi | Charlie | 3822 | 3458 | 3 |
| Bakurani_KOTH_02 | Sanavi | Alpha | 3895 | 3646 | 2 |
| Madrid_KOTH_01 | Barcelona | Bravo | 4006 | 3375 | 3 |
| Madrid_KOTH_01 | Malaga | Charlie | 3891 | 3717 | 1 |
| Madrid_KOTH_01 | Granada | Alpha | 3522 | 3291 | 2 |
| ED_Detroit_KOTH_01 | Austin | Bravo | 3927 | 3669 | 1 |
| ED_Detroit_KOTH_01 | Boston | Alpha | 3729 | 3445 | 3 |
| ED_Detroit_KOTH_01 | Chicago | Charlie | 3649 | 3396 | 2 |
| Moscow_KOTH_01 | Rostokino | Bravo | 3867 | 3540 | 5 |
| Moscow_KOTH_01 | Kuzminki | Alpha | 3932 | 3623 | 2 |
| Moscow_KOTH_01 | Ramenki | Charlie | 3996 | 3653 | 4 |

All fifteen spawn areas lie between 3.5 and 4.1 km from the middle of their zone area and between 3.3 and 3.8 km from the nearest tower. The three spawn areas of one entry differ from each other by at most 0.5 km.

### 14b. Light and weather

Each world holds one sky actor (`BP_SkyActor_C`) with a stored lighting preset (`DA_LightSettings_*`). Its tick is off, no day-cycle sky (`WDDynamicSky`), time-of-day or weather actor is placed in any content package, and rain exists only as one preset (`DayLateRain`). The lighting of a match is therefore a fixed preset, chosen by the server rotation (`Lighting` field of a rotation entry, SERVER). Stored defaults:

| Map | Stored preset | Server name | Sun height (deg) | Fog density | Fog start (actor, m) |
|---|---|---|---:|---:|---:|
| Bakurani | DA_LightSettings_Midday_01 | DayClear | 43.8 | 0.009 | 20 |
| Zestafona | DA_LightSettings_Midday_01 | DayClear | 43.8 | 0.009 | 20 |
| Ozeti | DA_LightSettings_Afternoon_01 | DayLateClear | 20.2 | 0.007 | 100 |
| Saburtulo | DA_LightSettings_Afternoon_01 | DayLateClear | 20.2 | 0.007 | 100 |

Presets by fog density (thinnest first):

| Server name | Plain name | Sun height (deg) | Sun intensity | Fog density | Rain |
|---|---|---:|---:|---:|---|
| DayEndClear | Sunset, clear | 12.8 | 12000 | 0.0009 | - |
| DayEarlyClear | Morning, clear | 10.1 | 6000 | 0.002 | - |
| DayLateClear | Late afternoon, clear | 20.2 | 60000 | 0.004 | - |
| DayStartClear | Sunrise, clear | 5.1 | 18000 | 0.007 | - |
| DayClear | Midday, clear | 43.8 | 120000 | 0.009 | - |
| DayLateGray | Late afternoon, overcast | 32.9 | 100 | 0.015 | - |
| DayLateGrayFog | Late afternoon, overcast and foggy | 32.9 | 100 | 0.015 | - |
| DayEarlyFog | Morning, foggy | 10.1 | 6000 | 0.06 | - |
| DayLateRain | Late afternoon, heavy rain | 32.9 | 100 | 0.3 | yes |

### 14c. Match start (what the `MatchState.Playing` subscribers do)

See [`match-start.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/match-start.json). No subscriber teleports a player, resets health, clears inventory or sets the starting balance. The pre-lobby payout is the only Cash write. Base starting Cash is 10,000 (`DT_CurrenciesDefinitions`, session override -1); PvE scenarios set 3,000 (Strike and Disarm) and 2,000 (VIP Escort).

---


## 15. PvE scenario layouts (round 71)

Read from the 110 cells of the PvE external data layers in the Kavkazi (Bakurani) world (VIPEscort_01 65 cells, StrikeDisarm_01 16, HunterKiller_01 28, ScenarioExample 1). Every placed actor was read with its root position (an attached actor takes the parent transform). Data: [`assets/data/pve-layouts.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/pve-layouts.json); method and statuses: [`docs/evidence/round71-pve-layouts.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round71-pve-layouts.md). Positions are metres in the world frame; distances are straight lines. Bakurani reference: zone area centre (-8301, -11201), play box x -9967..-6634, y -12925..-9477.

| Item | VIP Escort | Strike and Disarm | Hunter Killer | Example |
|---|---|---|---|---|
| Player spawn area | 1 at (-7754, -7450) | 1 at (-12410, -9736), plus 15-point spawn volume | none | 1 at (-8890, -11355) |
| Spawn area from play box | 2,027 m north | 2,443 m west | - | inside |
| Objective | extraction trigger (-9417, -10365), 80 m marker | laptop (-10031, -10427), 200 m compound marker | none (labels only) | 1 overlap area, 17 m from spawn |
| Helicopter paths | 1 entry, 1 exit | 1 entry, 1 exit (end marker (-9920, -10288)) | none | none |
| Spawn to objective | 3,356 m | 2,478 m | - | 17 m |
| Objective to end point | 51 m (trigger to helicopter point) | 177 m (laptop to end marker) | HVT label to exfil label 192 m | - |
| AI spawners (one soldier each, inferred) | 95 (86 rifle, 5 marksman, 4 machine gun) | 53 (49 rifle, 4 sniper); 26 held for the wave | 0 | 0 |
| Patrol routes | 16 (31 soldiers) | 4 (6 soldiers) | 0 | 0 |
| Vehicle spawners | 6 | 5 | 0 | 0 |
| Loot markers | 21 (shared tags, none for the VIP rows) | 0 | 0 | 0 |
| Volumes | 1 navmesh volume, 1 trigger box | tether 1, target area 1, spawn 1, navmesh 1 | none | none |
| Vendors | equipment 1 | equipment 1, vehicle 1 | none | equipment 1 |

Notes. (a) The VIP of VIP Escort is a random player, so no VIP start is placed; the start is the spawn area. (b) The extraction point of VIP Escort and the end area of Strike and Disarm both lie inside the play box, 1.4 and 1.9 km from the zone area centre, in no named region polygon (nearest: Riverside Forest, 235 m and 736 m). The laptop is 64 m outside the play box, 799 m from Green Farmland. (c) Hunter Killer holds 16 hidden text labels (Deploy 1, HVT 1, Lieutenant 2, Guards 4, Patrol 7, Exfil 1) and 9 mesh actors; its HVT and exfil labels sit 78 and 79 m from the Strike and Disarm laptop and helicopter point (inferred reuse of one compound). (d) Soldiers per distance from the VIP Escort spawn: 26 within 1 km, 34 at 1 to 2 km, 24 at 2 to 3 km, 11 beyond 3 km. Strike and Disarm start group: 13 of 27 within 100 m of the laptop; the wave stands 232 to 541 m away. (e) The native body that creates the soldier (`TriggerAISpawn`) was not read (NATIVE).

## 9. Still Not Pulled / Limitations

- **Level (`.umap`) data.** Round 65 read the placed static meshes of the four world maps (section 10) and round 66 the placed gameplay actors (section 11). Gameplay rules and the Blueprint graphs are not in [`Content/Maps`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps). Only the supporting assets are.
- **Blueprint logic.** [`B_MovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json) exports its function names, variables, and components, but not the graph nodes. The time-to-target formula and the damage response are not in the export.
- **Units and meaning.** Health (1.0), DamageIncrease (3.5), the grid bounds, and the simulation values have no units in the export. The `Iteration` counter and the sample meaning of 65535 in the height grid are not verified.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Unnamed fields.** Several properties in the height grid, the warmup manifests, and the sight blocker assets are unnamed fields. Their values were read and reported, but their names are not known. Those values are cited by position and value only.
- **Water height decoding.** The mapping from the 16-bit samples to world heights is not in the export. The sentinel reading of 65535 is an inference from the distribution.
- **Vertex factory and material paths.** The manifests reference materials and vertex factories by path and class name. The materials themselves are in other categories.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
