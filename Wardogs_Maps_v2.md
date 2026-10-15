---
title: "Maps"
parent: "Content"
---

# Wardogs — Maps & Gym Data Reference (v2)
*Extracted from the cooked JSON export under `Content/Maps` (7 files, 41 export blocks). Values are raw asset properties. Anything inferred from a name rather than from the export is marked as inferred. The `.umap` level files are not in this category, so this doc covers the data assets that sit beside the maps.*

> **Scope note:** this is the supporting data for the test gyms (`Gyms/`) and the per-map shader warmup manifests (`PSOWarming/`). The actual level layouts, actor placement, and gameplay rules are not in this dump.

---

## 1. Inventory

| File | Export type | What it is |
|---|---|---|
| `Gyms/Minimal/DT_Gym_Minimal_GridTest` | `WDAutomationWorldGridData` | Grid of capture cells over the minimal test gym |
| `Gyms/Range/Assets/B_MovingTarget` | `BlueprintGeneratedClass` (`B_MovingTarget_C`) | Moving shooting-range target actor |
| `Gyms/Water/PDA_Flux_Gym_Water` | `PDA_FluxSimulationState_C` | Fluid simulation settings and texture references for the water gym |
| `Gyms/Water/WHG_PDA_Flux_Gym_Water` | `WDWaterHeightGridAsset` | Water height grid (512 x 512 samples) for the water gym |
| `PSOWarming/Europe_Madrid_KOTH_01` | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Madrid KOTH map |
| `PSOWarming/NorthAmerica_Detroit_KOTH_01` | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Detroit KOTH map |
| `PSOWarming/Kavkazi_Bakurani_KOTH_01` | `WDPSOWarmupDataAsset` | Shader/PSO warmup manifest for the Bakurani KOTH map (**truncated in the dump**, see section 6) |

---

## 2. Minimal Grid Test (`DT_Gym_Minimal_GridTest`)

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

## 3. Shooting-Range Moving Target (`B_MovingTarget`)

The moving target is a blueprint actor. The export includes its class defaults, its components, its one timeline, and the names of its functions. The function bodies (graph logic) are not in the export, so only the data is documented here.

### 3a. Class defaults

| Property | Value | Notes |
|---|---|---|
| Health | 1.0 | Units not stated |
| DamageIncrease | 3.5 | Units and meaning not stated |
| TimeToReachTargetRange | Min 15, Max 25 | Likely seconds (inferred from name). The range is consumed by `GetTimeToReachTarget` |
| StartingLocation | (0, 0, 0) | |
| bReplicates | True | |
| RemoteRole | `ROLE_SimulatedProxy` | |

### 3b. Components

| Component | Class | Mesh | Notes |
|---|---|---|---|
| Root_GEN_VARIABLE | StaticMeshComponent | `Cube` | Scale X -10. Child of DummyRoot in the component hierarchy |
| Cube2_GEN_VARIABLE | StaticMeshComponent | `SM_Target_Base` | Scale X 0.28, Z -5.47. Base of the target stand (inferred from name) |
| Cube3_GEN_VARIABLE | StaticMeshComponent | `SM_Target_Rail` | Rail piece (inferred from name) |
| RotatePoint_GEN_VARIABLE | StaticMeshComponent | `SM_Target_01a` | Target face. Its pivot role is inferred from the variable name |
| DefaultSceneRoot_GEN_VARIABLE | SceneComponent | - | Scene root of the actor (`SCS_Node_0`) |
| DummyRoot_GEN_VARIABLE | SceneComponent | - | Parent of the Root mesh node |
| MovePoint_GEN_VARIABLE | SceneComponent | - | Movement pivot |
| LeftMoveLocation / RightMoveLocation_GEN_VARIABLE | SceneComponent | - | The two end points of the horizontal move. LeftMoveLocation relative location X -0.41, Z 12.23 |

### 3c. Timeline and curve

| Item | Value |
|---|---|
| Timeline name | `TargetFall` (template `TargetFall_Template`) |
| TimelineLength | 0.5 |
| Track | `FallRate` on `CurveFloat_0` |
| Curve keys | (t 0.0, value 0.0) to (t 0.5, value 1.0), cubic interpolation, auto tangents |
| Bound functions | `TargetFall__UpdateFunc`, `TargetFall__FinishedFunc` |

The fall plays out over half a second. The rate curve goes from 0 to 1 over the length of the timeline.

### 3d. Function list

`SetMovingTarget`, `GetTimeToReachTarget`, `OnMovingTargetUpdated`, `TakeDamage`, `ReceiveDamage`, `Knockdown`, `Popup`, `ReceiveBeginPlay`, `ExecuteUbergraph_B_MovingTarget`, `TargetFall__UpdateFunc`, `TargetFall__FinishedFunc`.

Function names only. The export has no graph nodes, so the actual formula for time-to-target or the damage math is not in this dump.

---

## 4. Water Gym (`PDA_Flux_Gym_Water` and `WHG_PDA_Flux_Gym_Water`)

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
| Linked asset | `PDA_Flux_Gym_Water` (the sim state in 4a) |

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
- Two unnamed float values are stored under obfuscated keys: -2216.76 and 2046.39. They are probably the minimum and maximum of the height range, but that is not verified. The export's `CaptureOffset` in 4a is -621.76, and the two values do not obviously relate to it.

---

## 5. Shader/PSO Warmup Manifests (`WDPSOWarmupDataAsset`)

Three per-map manifests list the materials and vertex factories that the map uses, and the compute shaders it needs. The asset type and the `PSOWarming` folder suggest they are used to pre-compile pipeline state objects before a match starts. That purpose is inferred from the names.

Each manifest has the same structure:

- `WorldData`: the world asset (`/Game/Maps/Worlds/...`) and the experience name.
- `GraphicsPSOs`: one entry per material, with its `MatObjectPath` and the `VertexFactories` it is drawn with.
- `ComputePSOs`: a list of compute shader names.

### 5a. Summary

| Manifest | Experience name | World | Graphics PSOs | Compute PSOs | Status |
|---|---|---|---|---|---|
| `Europe_Madrid_KOTH_01` | Madrid_KOTH_01 | `/Game/Maps/Worlds/Europe/Europe` | 1,639 | 6 | Complete |
| `NorthAmerica_Detroit_KOTH_01` | Detroit_KOTH_01 | `/Game/Maps/Worlds/NorthAmerica/NorthAmerica` | 1,870 | 76 | Complete |
| `Kavkazi_Bakurani_KOTH_01` | Bakurani_KOTH_01 | `/Game/Maps/Worlds/Kavkazi/Kavkazi` | 2,528 | at least 2 (file truncated) | **Truncated**, see section 6 |

The experience name for the Kavkazi file is `Bakurani_KOTH_01`, which differs from the file name. The file name and the experience name are both kept as they appear in the export.

### 5b. Vertex factory usage (per GraphicsPSO entry)

A PSO can list more than one vertex factory, so these counts add up to more than the PSO totals.

| Vertex factory | Madrid | Detroit | Kavkazi |
|---|---|---|---|
| `FNaniteVertexFactory` | 1,152 | 1,300 | 1,016 |
| `FLocalVertexFactory` | 318 | 150 | 1,274 |
| `TGPUSkinVertexFactoryDefault` | 128 | 399 | 191 |
| `FInstancedStaticMeshVertexFactory` | 49 | 49 | 49 |
| `FSplineMeshVertexFactory` | 18 | 11 | 23 |
| `FNiagaraSpriteVertexFactory` | 16 | 16 | 21 |
| `FNiagaraMeshVertexFactory` | 3 | 1 | 2 |

Nanite dominates Madrid and Detroit. Kavkazi relies much more on the local vertex factory (1,274), which suggests a different mix of non-Nanite static geometry.

### 5c. Material folders (top six by top-level folder under `/Game`)

| Folder | Madrid | Detroit | Kavkazi |
|---|---|---|---|
| Environment | 813 | 835 | 855 |
| Maps | 484 | 663 | 629 |
| Characters | 111 | 172 | 169 |
| Megascans | 28 | 32 | 36 |
| VFX | 23 | - | 25 |
| Materials | - | 37 | 13 |
| Items | - | 26 | - |
| Assets | 8 | - | - |

Only the top six folders are shown, so "-" means "not in that manifest's top six", not zero. Detroit has the most Maps and Characters materials of the three. Madrid has the smallest total (1,639 graphics PSOs).

### 5d. Compute PSO names (sample)

| Manifest | Examples in the list |
|---|---|
| Madrid (all 6) | `TBasePassCSFNoLightMapPolicy`, `FRDGMemcpyCS`, `FMicropolyRasterizeCS`, `FShader_VirtualTextureCompress_CS< ERuntimeVirtualTextureMaterialType::Mask4 >`, `FNiagaraShader`, `FRDGMemsetBufferCS` |
| Detroit (sample of 76) | `FScatterUpdates_CS`, `FStochasticLightingTileClassificationMarkCS`, `FScreenProbeTemporalReprojectionCS`, `FMicropolyRasterizeCS`, `TBasePassCSFNoLightMapPolicy`, `FLumenReflectionDenoiserTemporalCS`, `FClearReplacementCS_Texture3D_Uint4_Bounds`, `FHZBBuildCS` |
| Kavkazi (surviving entries) | `TBasePassCSFNoLightMapPolicy`, `FCopyDistanceFieldAtlasCS` |

The Detroit list is heavier on Lumen, screen-probe, and HZB shaders (engine rendering features). That matches a larger graphics configuration for that map.

---

## 6. Truncated File: `Kavkazi_Bakurani_KOTH_01`

The file is 629,760 bytes, but the JSON stops partway through the `ComputePSOs` array (around character 614,457). As a result it does not parse as a whole.

What was recovered:

- **Header and WorldData:** complete. Experience name `Bakurani_KOTH_01`, world `/Game/Maps/Worlds/Kavkazi/Kavkazi`.
- **GraphicsPSOs:** complete. The array is closed before `ComputePSOs` begins, so it was isolated and parsed on its own, giving **2,528 entries**.
- **ComputePSOs:** partial. Only the first two entries survived (`TBasePassCSFNoLightMapPolicy`, `FCopyDistanceFieldAtlasCS`). The total count is unknown.

The GraphicsPSO figures in section 5 come from that isolated, complete array, so they are reliable. The compute count is not.

---

## 7. How Values Combine

- **Water gym:** the fluid sim (4a) runs over a 102400-unit area at 2048 by 2048. The height grid (4b) covers the same 102400-unit world size at 512 by 512, which is a coarser sampling of the same area (one height sample per 200 units, versus one sim texel per 50 units). How the grid is used at runtime is not in the export.
- **Moving target:** the timeline (3c) runs its fall over 0.5 seconds. The move range is 15 to 25 (3a), and the actual choice of time within that range happens in the blueprint graph, which is not exported.
- **PSO manifests:** a map's effective warmup is the union of its graphics and compute entries. The vertex-factory counts in 5b show which rendering paths the map needs.

---

## 8. Still Not Pulled / Limitations

- **Level (`.umap`) data.** Actor placement, spawn points, and gameplay rules are not in `Content/Maps`. Only the supporting assets are.
- **Blueprint logic.** `B_MovingTarget` exports its function names, variables, and components, but not the graph nodes. The time-to-target formula and the damage response are not in this dump.
- **Units and meaning.** Health (1.0), DamageIncrease (3.5), the grid bounds, and the simulation values have no units in the export. The `Iteration` counter and the sample meaning of 65535 in the height grid are not verified.
- **Obfuscated keys.** Several properties in the height grid and the warmup manifests use hashed keys (for example `_aaaaidjmhamkdihpinkjd_$39C70CA387F8DA93$_$8$`). Their values were read and reported, but their names are not known. Those values are cited by position and value only.
- **Kavkazi compute list.** The file is truncated. Its full compute PSO count and names are not recoverable from this dump.
- **Water height decoding.** The mapping from the 16-bit samples to world heights is not in the export. The sentinel reading of 65535 is an inference from the distribution.
- **Vertex factory and material paths.** The manifests reference materials and vertex factories by path and class name. The materials themselves are in other categories.
