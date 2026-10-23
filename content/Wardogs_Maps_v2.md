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

## 9. Still Not Pulled / Limitations

- **Level (`.umap`) data.** Actor placement, spawn points, and gameplay rules are not in [`Content/Maps`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Maps). Only the supporting assets are.
- **Blueprint logic.** [`B_MovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json) exports its function names, variables, and components, but not the graph nodes. The time-to-target formula and the damage response are not in the export.
- **Units and meaning.** Health (1.0), DamageIncrease (3.5), the grid bounds, and the simulation values have no units in the export. The `Iteration` counter and the sample meaning of 65535 in the height grid are not verified.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Unnamed fields.** Several properties in the height grid, the warmup manifests, and the sight blocker assets are unnamed fields. Their values were read and reported, but their names are not known. Those values are cited by position and value only.
- **Water height decoding.** The mapping from the 16-bit samples to world heights is not in the export. The sentinel reading of 65535 is an inference from the distribution.
- **Vertex factory and material paths.** The manifests reference materials and vertex factories by path and class name. The materials themselves are in other categories.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
