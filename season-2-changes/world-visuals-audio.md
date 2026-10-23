---
title: "World, Visuals & Audio changes"
parent: "Season 2 Changes"
nav_order: 9
description: "World, Visuals & Audio: 163 assets added, 153 modified with real changes, 245 noise-only. Destructible buildings and water changed. Audio and UI are counts only."
---

# World, Visuals & Audio changes

Season 1 to Season 2 changes for this area, from the area diff file. Audio and UI widget assets are counted only. Every change in this area is in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=world-visuals-audio), where each asset and property can be filtered.

| Measure | Count |
|---|---:|
| Assets added | 163 |
| Assets removed | 0 |
| Assets modified with real changes | 153 |
| Assets moved | 0 |
| Noise-only modified assets (skipped, no real change) | 245 |
| Property changes | 2,554 (changed 1,782, added 603, removed 168, resequenced 1) |

## Gameplay-relevant changes

- Destructible buildings: 26 building definitions and 21 decorator definitions added. 55 building definitions and 56 decorator definitions modified with real changes (decorator transforms, chunk IDs and prefab hashes).
- Water height grids and hot zone magnet data: 40 and 3 assets modified. All of them are noise-only, so no value changed.
- Environment generation: 18 spline PCG, 12 cluster PCG, 7 ground detail and 4 micro-biome assets added.

Other added assets are listed by folder below. Audio and UI are counted in the next table.

## Audio and UI (counts only)

| Class | Added | Modified with real changes | Noise-only | Removed | Browse |
|---|---:|---:|---:|---:|---|
| Audio | 46 | 25 | 196 | 0 | [audio changes]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=world-visuals-audio&q=CrosstalkAudioEvent) |
| UI widgets | 1 | 4 | 6 | 0 | [ui widgets changes]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=world-visuals-audio&q=UI) |

## Added in Season 2 (gameplay and visual assets)

| Folder | Type | Added assets |
|---|---|---|
| `Content/Environment/Blueprints/VehiclePropTooling` | PDA_VehicleProp_C (1) | `DA_VehicleProp_Ambulance_01a` |
| `Content/Environment/Foliage/Biomes/Farm/Layers` | PDA_MBLayer_C (2) | `MBL_Farm_FIeld_Grass_Tall_Transition`, `MBL_Farm_Field_Brambles_Transition` |
| `Content/Environment/Foliage/Biomes/Farm/MicroBiomes` | PDA_MicroBiome_C (1) | `MB_Farm_Field_Edge` |
| `Content/Environment/Foliage/Biomes/Woodland/MicroBiomes` | PDA_MicroBiome_C (2) | `MB_Woodland_TreeLine_Bushes`, `MB_Woodland_TreeLine_Saplings` |
| `Content/Environment/Foliage/Bushes/Bramble/DataAssets/Clusters` | PDA_MBCluster_C (1) | `MBC_Bush_Bramble_Patch_3m_01a` |
| `Content/Environment/Foliage/Bushes/Bramble/DataAssets/Scatters` | PDA_MBScatter_C (1) | `MBS_Bush_Bramble_Strands` |
| `Content/Environment/Foliage/Grass/Field/DataAssets/Clusters` | PDA_MBCluster_C (1) | `MBC_Grass_Field_Tall_Transition` |
| `Content/Environment/Foliage/Trees/Ash/DataAssets/Clusters` | PDA_MBCluster_C (1) | `MBC_Tree_Ash_Sapling_01a` |
| `Content/Environment/Foliage/Trees/Oak/DataAssets/Clusters` | PDA_MBCluster_C (1) | `MBC_Tree_Oak_Field_02a` |
| `Content/Environment/Foliage/Trees/Pine/DataAssets/Clusters` | PDA_MBCluster_C (1) | `MBC_Pine_04m` |
| `Content/Environment/Lighting/DataAssets/Presets/Weather` | WDRainAppearance (1) | `WD_HeavyRain` |
| `Content/Environment/PCG/GroundDetail` | DA_GroundProxies_C (1) | `AdditionalGroundMeshes` |
| `Content/Environment/PCG/GroundDetail/GroundDetailData` | DA_GroundDetail_C (7) | `GD_AsphaltPatches`, `GD_Ivy`, `GD_Leaves`, `GD_NettlesEdge`, `GD_Paper`, `GD_PotHoles`, `GD_RubbleEdges` |
| `Content/Environment/PCG/Kavkazi/DataAssets/Clusters` | PDA_ClusterPCG_C (2) | `DA_Cluster_Weeds_02`, `DA_Cluster_Weeds_Spline` |
| `Content/Environment/PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` | PDA_ClusterPCG_C (10) | `DA_FencePost_GasPipe_400_01`, `DA_FencePost_StoneRetainingWall_01`, `DA_Fence_Chainlink_Post_01`, `DA_Fence_Metal_Residential_Pillar_03`, `DA_Fence_Metal_Residential_Pillar_04`, `DA_Fence_Metal_Residential_Pillar_05`, `DA_Fence_Tarp_01`, `DA_Pillar_ChurchExt_01b`, `DA_Pillar_ChurchExt_02`, `DA_Wall_Plaster_Residential_Pillar_01` |
| `Content/Environment/PCG/Kavkazi/DataAssets/Splines/Wall` | PDA_SplinePCG_C (18) | `DA_ConcreteBarrier_01`, `DA_Ditch_01`, `DA_Fence_ChainLink_02`, `DA_Fence_Concrete_Large_02`, `DA_Fence_CorrugatedMetal_01`, `DA_Fence_HescoSmall_01`, `DA_Fence_HescoTall_01`, `DA_Fence_Large_BoxHedge_02`, `DA_Fence_Low_Concrete_02`, `DA_Fence_Med_BoxHedge_01`, `DA_Fence_Metal_02`, `DA_Fence_Metal_Residential_03`, `DA_Fence_Metal_Residential_04`, `DA_Fence_Metal_Residential_05`, `DA_Fence_StoneRetainingWall_01`, `DA_Fence_TallWoodWall_Damaged_02`, `DA_Wall_ChurchExt_02`, `DA_Wall_Plaster_Residential_01` |
| `Content/Environment/PCG/MicroBiomes/Pine` | PDA_MicroBiome_C (1) | `MB_Pine_Spline_Dense_02` |
| `Content/Environment/PCG/MicroBiomes/Pine/Clusters` | PDA_MBCluster_C (1) | `MBC_Pine_06mFiller` |
| `Content/Environment/PCG/MicroBiomes/Pine/Layers` | PDA_MBLayer_C (1) | `MBL_Pine_04m_Edge` |
| `Content/Environment/PCG/RVTD/DataAssets` | PDA_RVTD_C (1) | `DA_RVTD_Forest_001` |
| `Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential` | BHDestructionBuildingDefinitionDataAsset (6), BHDestructionBuildingDecoratorDefinitionDataAsset (2) | `D_Decorator_D_Residential_House_05b`, `D_Decorator_Residential_House_06`, `D_Residential_House_05b`, `D_Residential_House_06`, `D_Residential_House_Var_01`, `D_Residential_House_Var_03`, `D_Residential_House_Var_04`, `D_Residential_House_Var_05` |
| `Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/SwimmingPool` | BHDestructionBuildingDecoratorDefinitionDataAsset (1), BHDestructionBuildingDefinitionDataAsset (1) | `D_Decorator_SwimPool_Building_02`, `D_SwimPool_Building_02` |
| `Content/ExternalAssets/Flix/Blueprints/Commercial/Highstreet` | BHDestructionBuildingDefinitionDataAsset (14), BHDestructionBuildingDecoratorDefinitionDataAsset (13) | `D_Comm_Highstreet_Base_01a`, `D_Comm_Highstreet_Base_02a`, `D_Comm_Highstreet_Base_02b`, `D_Comm_Highstreet_Base_02c`, `D_Comm_Highstreet_Base_02d`, `D_Comm_Highstreet_Top_01a`, `D_Comm_Highstreet_Top_02a`, `D_Comm_Highstreet_Top_02b`, `D_Comm_Highstreet_Top_02e`, `D_Comm_Highstreet_Top_03a`, `D_Comm_Highstreet_Top_04a`, `D_Comm_Highstreet_Top_Var_01a`, `D_Comm_Highstreet_Top_Var_02c`, `D_Comm_Highstreet_Top_Var_02d`, `D_Decorator_Comm_Highstreet_Base_01a`, `D_Decorator_Comm_Highstreet_Base_02a`, `D_Decorator_Comm_Highstreet_Base_02b`, `D_Decorator_Comm_Highstreet_Base_02c`, `D_Decorator_Comm_Highstreet_Base_02d`, `D_Decorator_Comm_Highstreet_Top_01a`, `D_Decorator_Comm_Highstreet_Top_02a`, `D_Decorator_Comm_Highstreet_Top_02b`, `D_Decorator_Comm_Highstreet_Top_02c`, `D_Decorator_Comm_Highstreet_Top_02d`, `D_Decorator_Comm_Highstreet_Top_02e`, `D_Decorator_Comm_Highstreet_Top_03a`, `D_Decorator_Comm_Highstreet_Top_04a` |
| `Content/ExternalAssets/Flix/Blueprints/Commercial/Hospital` | BHDestructionBuildingDefinitionDataAsset (4), BHDestructionBuildingDecoratorDefinitionDataAsset (4) | `DA_HospitalBuilding_01a`, `DA_HospitalBuilding_01a_Decorator`, `DA_HospitalBuilding_01b`, `DA_HospitalBuilding_01b_Decorator`, `DA_HospitalBuilding_01c`, `DA_HospitalBuilding_01c_Decorator`, `DA_HospitalBuilding_01d`, `DA_HospitalBuilding_01d_Decorator` |
| `Content/ExternalAssets/Flix/Blueprints/Commercial/WorkShop` | BHDestructionBuildingDecoratorDefinitionDataAsset (1), BHDestructionBuildingDefinitionDataAsset (1) | `D_Decorator_WorkShopBuilding_01`, `D_WorkShopBuilding_01` |
| `Content/VFX/Explosions` | PDA_Explosion_C (1) | `DA_Explosion_125x570mm` |
| `Content/VFX/Vehicles/Exhaust/DataAssets` | BHExhaustDataAsset_C (2) | `DA_TNK_04_Exhaust`, `DA_WHL_08_Exhaust` |
| `Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData` | PDA_MuzzleFlashAttachement_C (3) | `DA_MF_MUZL_069`, `DA_MF_MUZL_070`, `DA_MF_MUZL_072` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/AssualtRifles` | PDA_MuzzleFlash_C (1) | `DA_MuzzleFlash_SigMcx` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/DMR` | PDA_MuzzleFlash_C (1) | `DA_MuzzleFlash_M14` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/LMG` | PDA_MuzzleFlash_C (1) | `DA_MuzzleFlash_Evloys` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/SMG` | PDA_MuzzleFlash_C (1) | `DA_MuzzleFlash_WEPN_031` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/STN_06` | PDA_MuzzleFlash_C (1) | `DA_MuzzleFlash_STN_06_MountedMachineGun` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/TNK_04` | PDA_MuzzleFlash_C (2) | `DA_MuzzleFlash_TNK_04`, `DA_MuzzleFlash_TNK_04_MountedMachineGun` |
| `Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/WHL_08` | PDA_MuzzleFlash_C (1) | `DA_MuzzleFlash_WHL_08_MountedMachineGun` |

Total in this table: 116 assets. Audio and UI added assets are counted above and are not listed.

## Removed in Season 2

No assets were removed in this area.

## See also

- [Environment]({{ '/content/Wardogs_Environment_v2.html' | relative_url }}#season-02-update)
- [Destruction]({{ '/content/Wardogs_Destruction_v2.html' | relative_url }}#season-02-update)
- [Demolition]({{ '/content/Wardogs_Demolition_v2.html' | relative_url }}#season-02-update)
- [VFX]({{ '/content/Wardogs_VFX_v2.html' | relative_url }}#season-02-update)
- [Audio]({{ '/content/Wardogs_Audio_v2.html' | relative_url }}#season-02-update)

