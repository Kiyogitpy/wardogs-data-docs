---
title: "Environment"
redirect_from: ["/Wardogs_Environment_v2.html", "/Wardogs_Environment_v2"]
parent: "World, Visuals & Audio"
description: "Environment and PCG data: the folder inventory, how vegetation and PCG data combine, micro-biomes and layers."
---

# Wardogs — Environment & PCG Reference
*Extracted from cooked game data (`Wardogs/Content/Environment/`, 419 JSON exports, UE 5.7). Values are the raw asset values. Positions and distances are Unreal units (cm) unless noted. Parsed with a Python script that strips the export header, normalises GUID-suffixed property names, and groups by folder and type.*

> **Scope note:** this covers only `Content/Environment`. Every `.json` in the folder was parsed (0 errors). Items marked *inferred* are guesses from names and value ranges. The export does not say what they mean.

---

## Season 02 update (2026-10-15)

- **Inventory:** 363 → 419 JSON exports. 46 MicroBiome, layer, cluster, scatter, spline and prop assets are new (section 15a). Headings count them, but the catalogue rows above list only the earlier assets.
- **New families:** `DA_GroundDetail_C` (7), `DA_GroundProxies_C` (1), `PDA_RVTD_C` (1) and `WDRainAppearance` (1), listed in section 15b.
- **`DA_LightSettings_AfternoonOvercast` and `_AfternoonOvercastFog`:** sun intensity 20000 → 100 (overkill too). AfternoonOvercast sun temperature 7600 → 7000.
- **`DA_LightSettings_Morning`:** sun intensity 9000 → 6000, fog density 0.004 → 0.002, lower hemisphere 500 → 300 (overkill 250 → 700), auto-exposure brightness 8.5 / 9.5 → 9 / 9.4.
- **`DA_LightSettings_MorningFoggy`:** sun intensity 35000 → 6000, fog density 0.01 → 0.06 (overkill same), lower hemisphere 500 → 300 (overkill 100 → 400), auto-exposure brightness 9 / 10 → 9.2 / 9.5, second fog density no longer set.
- **`DA_LightSettings_AfternoonOvercast` and `_AfternoonOvercastFog`:** sky light 0.7 no longer set (shown as `-`). AfternoonOvercast base colour contrast 1.2 no longer set.
- **`DA_FencePost_Wood_Tall_01`:** position Y min/max -2 → 0.
- **`DA_Fence_TallWoodWall_02`:** distance 202 no longer set (shown as `-`). **`DA_Pillar_Church_01`:** collision no longer set (shown as `-`).

Full before/after list: [Season 2 Changes → World, Visuals & Audio]({{ '/season-2-changes/world-visuals-audio.html' | relative_url }}).

---

## 1. Inventory and folder map

| Asset type (`Type`) | Files | Folders |
|---|---|---|
| `PDA_MBCluster_C` | 60 | `PCG/MicroBiomes/*/Clusters`, `Foliage/*/DataAssets/Clusters` |
| `PDA_FluxSimulationState_C` | 54 | `Water/FluidFlux/{Europe, Kavkazi, NorthAmerica}` |
| `PDA_MicroBiome_C` | 45 | `PCG/MicroBiomes/*`, `Foliage/Biomes/*/MicroBiomes` |
| `PDA_MBLayer_C` | 43 | `PCG/MicroBiomes/*/Layers`, `Foliage/Biomes/*/Layers` |
| `WDWaterHeightGridAsset` | 40 | `Water/FluidFlux/{Europe, Kavkazi}` |
| `PDA_SplinePCG_C` | 57 | `PCG/Kavkazi/DataAssets/Splines/*` |
| `PDA_VehicleProp_C` | 34 | `Blueprints/VehiclePropTooling` |
| `PDA_ClusterPCG_C` | 34 | `PCG/Kavkazi/DataAssets/Clusters`, `Foliage/*/DataAssets/Clusters` |
| `PDA_MBScatter_C` | 13 | `Foliage/*`, `PCG/MicroBiomes/Scatter` |
| `PDA_LightSettings_C` | 9 | `Lighting/DataAssets/Presets` |
| `BHDestructionBuildingDefinitionDataAsset` | 7 | `Architecture/Residential/Garages/BPs` |
| `BHDestructionBuildingDecoratorDefinitionDataAsset` | 7 | `Architecture/Residential/Garages/BPs` |
| `CurveLinearColor` | 2 | `Landscape/Materials/Kavkazi` |
| `DataTable` | 2 | `Blueprints/VehiclePropTooling`, `PCG/Runtime` |
| `CurveLinearColorAtlas` | 1 | `Landscape/Materials/Kavkazi` |
| `PDA_FluxSurfacePreset_C` | 1 | `Water/FluidFlux/Surface` |
| `DA_GroundDetail_C` | 7 | `PCG/GroundDetail/GroundDetailData` |
| `DA_GroundProxies_C` | 1 | `PCG/GroundDetail` |
| `PDA_RVTD_C` | 1 | `PCG/RVTD/DataAssets` |
| `WDRainAppearance` | 1 | `Lighting/DataAssets/Presets/Weather` |
| **Total** | **419** | |

Top-level folder file counts: `Water/FluidFlux` 95, `PCG/MicroBiomes` 87, `PCG/Kavkazi` 91, `Blueprints/VehiclePropTooling` 35, `Foliage` 71, `Architecture` 14, `Lighting` 10, `Geology` 3, `Landscape` 3, `PCG/GroundDetail` 8, `PCG/RVTD` 1, `PCG/Runtime` 1.

Size note: `WHG_*` height grids are the largest files (up to about 3.7 MB each, 40 files). Everything else is under 15 KB.

---

## 2. How the vegetation and PCG data combines

There are three parallel placement systems. They reference each other only where noted.

1. **MicroBiome chain (biome-driven vegetation).** `PDA_MicroBiome_C` → `Layers` (each a `PDA_MBLayer_C`) → `Clusters` (each a `PDA_MBCluster_C`) → `Scatterers` (each a `PDA_MBScatter_C`) and `Modules` (mesh bundles inside the cluster). The biome sets the mix. The layer sets how points are sampled. The cluster picks a mesh and sets scale, rotation, and offset. The scatter adds dense ground detail.
2. **Standalone cluster PCG (`PDA_ClusterPCG_C`).** Self-contained scatter definitions with their own mesh list, grid, and seed. Used for crops, weeds, fence posts, and hedges. Does not go through a MicroBiome.
3. **Spline PCG (`PDA_SplinePCG_C`).** Places pieces along a spline (fences, walls, curbs, guardrails, tree lines, embankments). Spacing is `Distance` (cm).

Weights (`Weight` on layer clusters, cluster meshes, and PCG mesh lists) are relative pick weights. They are not normalised in the data, so absolute values only matter relative to each other within one list.

For a MicroBiome layer entry, the placement gates apply in this order (inferred from field names):
- `Enabled` must be true.
- `AreaDensityThreshold`, `AreaDensityOffset`, and `AreaDensityInvert` gate the entry on the biome's `AreaDensity` value.
- `Density` sets how many points the layer produces.
- `AreaOfInfluence` sets the radius over which the entry applies (cm assumed).


---

## 3. MicroBiomes (`PDA_MicroBiome_C`, 45 assets)

Top-level biome containers. Each is a list of layer entries plus a few shared settings. Folders follow the on-disk layout. `Layers` lists the referenced layer assets in order. `Priority / MaxWeight` shows the shared values (40 of 41 set; `-` where absent). `Area density` is the `AreaDensity` value (`-` means unset). `Foliage-tagged` is `FoliageTagged`, set on only 2 assets.

### 3a. Catalogue

| Folder | Asset | Layers | Layer assets | Icon | Area density | Priority / MaxWeight | AttenuationDist | SplinePadding | Foliage-tagged |
|---|---|---|---|---|---|---|---|---|---|
| Foliage/Biomes/Farm/MicroBiomes | MB_Farm_Field_Crop_Maize | 1 | MBL_Farm_Crop_Maize | Icon_Crop_BC | - | - / - | - | - | yes |
| Foliage/Biomes/Farm/MicroBiomes | MB_Farm_Field_Crop_Sunflower | 1 | MBL_Farm_Crop_Sunflower | Icon_Sunflower_BC | - | 3 / 1 | 1000 | 1 | yes |
| Foliage/Biomes/Forest/MicroBiomes | MB_Forest_Interior_Sparse | 6 | MBL_Pine_10m, MBL_Forest_Trees_06m_Canopy, MBL_Forest_Bushes_Transition, MBL_Forest_Trees_Stumps, MBL_Forest_Trees_Saplings, MBL_Forest_Undergrowth | Icon_Missing_BC | 0.49 | 3 / 1 | 1000 | 10 | no |
| Foliage/Biomes/Forest/MicroBiomes | MB_Forest_TreeLine | 4 | MBL_Forest_Trees_TreeLine, MBL_Forest_Trees_Saplings, MBL_Forest_Bushes, MBL_Forest_Undergrowth | Icon_Missing_BC | - | 3 / 1 | 1000 | - | no |
| Foliage/Biomes/Forest/MicroBiomes | MB_Forest_TreeLine_Saplings_02 | 3 | MBL_Forest_Trees_Saplings, MBL_Forest_Bushes, MBL_Forest_Undergrowth | Icon_Missing_BC | - | 3 / 1 | 1000 | - | no |
| Foliage/Biomes/Woodland/MicroBiomes | MB_Woodland_TreeLine | 4 | MBL_Woodland_Trees_TreeLine, MBL_Deciduous_Saplings, MBL_Woodland_Bushes, MBL_Woodland_Undergrowth | - | - | 3 / 1 | 1000 | 50 | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Interior_Dense | 6 | MBL_Ash_Canopy_10m, MBL_Oak_Canopy, MBL_Beech_Canopy_10m, MBL_Ash_Canopy_10m, MBL_Beech_Canopy_6m, MBL_Bushes_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Interior_DensePlayspace | 11 | MBL_Rock_Huge, MBL_Rocks_Medium, MBL_Ash_Canopy_10m, MBL_Oak_Canopy, MBL_Beech_Canopy_10m, MBL_Ash_Canopy_10m, MBL_Logs, MBL_Beech_Canopy_6m, MBL_Deciduous_Saplings, MBL_Bushes_NoCol, MBL_Woodland_Trees_Ferns_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | 0 | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Interior_Sparse | 6 | MBL_Ash_Canopy_10m, MBL_Oak_Canopy, MBL_Beech_Canopy_10m, MBL_Ash_Canopy_10m, MBL_Beech_Canopy_6m, MBL_Bushes_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | 0 | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Interior_Sparse_Playspace | 9 | MBL_Rocks_Medium, MBL_Ash_Canopy_10m, MBL_Oak_Canopy, MBL_Beech_Canopy_10m, MBL_Ash_Canopy_10m, MBL_Logs, MBL_Beech_Canopy_6m, MBL_Deciduous_Saplings, MBL_Bushes | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | 50 | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Saplings_Spline | 2 | MBL_Deciduous_Saplings, MBL_BushesCloseEdge_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Spline_Dense | 4 | MBL_Deciduous_08mTrees, MBL_BushesEdge_NoCol, MBL_Deciduous_Saplings, MBL_Rocks_Medium | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Spline_Sparse | 2 | MBL_Deciduous_08mTrees, MBL_BushesCloseEdge_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Treeline_Dense | 2 | MBL_Deciduous_08mTreesClose, MBL_BushesCloseEdge_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Treeline_Sparse | 2 | MBL_Deciduous_08mTreesClose, MBL_BushesCloseEdge_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Deciduous | MB_Deciduous_Treeline_Sparse_02 | 2 | MBL_Deciduous_08mTreesClose, MBL_BushesCloseEdge_NoCol | Icon_Dec_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Interior_Dense | 2 | MBL_Pine_10m, MBL_Bushes_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | 150 | no |
| PCG/MicroBiomes/Pine | MB_Pine_Interior_Dense_Deforested | 1 | MBL_Forest_Trees_Stumps | Icon_Tree_BC | - | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/Pine | MB_Pine_Interior_Dense_Playspace | 10 | MBL_Rock_Huge, MBL_Pine_10m, MBL_Rocks_Medium, MBL_Pine_Saplings, MBL_Bushes_NoCol, MBL_Sticks, MBL_Logs, MBL_Pine_06m, MBL_Forest_Embankments, MBL_Bushes | Icon_Tree_BC | - | 3 / 1 | 1000 | 0 | no |
| PCG/MicroBiomes/Pine | MB_Pine_Interior_Sparse | 4 | MBL_Pine_10m, MBL_Pine_06m, MBL_Pine_Saplings, MBL_Bushes_NoCol | Icon_Tree_BC | 0.8 | 3 / 1 | 1000 | 0 | no |
| PCG/MicroBiomes/Pine | MB_Pine_Interior_Sparse_Playspace | 9 | MBL_Rock_Huge, MBL_Pine_10m, MBL_Rocks_Medium, MBL_Pine_Saplings, MBL_Bushes_NoCol, MBL_Sticks, MBL_Logs, MBL_Pine_06m, MBL_Forest_Embankments | Icon_Tree_BC | 0.8 | 3 / 1 | 1000 | 0 | no |
| PCG/MicroBiomes/Pine | MB_Pine_Saplings_Spline | 1 | MBL_Pine_Saplings | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Spline_Dense | 2 | MBL_Pine_06m_Edge, MBL_BushesEdge_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Spline_DensePlayspace | 3 | MBL_Pine_06m_Edge, MBL_BushesEdge_NoCol, MBL_Pine_SaplingsEdge | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Spline_Sparse | 3 | MBL_Pine_06m, MBL_Pine_Saplings, MBL_Bushes_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Spline_Sparse_02 | 3 | MBL_Pine_06m, MBL_Pine_Saplings, MBL_Bushes_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Treeline | 4 | MBL_Pine_06mClose, MBL_Pine_SaplingsClose, MBL_BushesCloseEdge, MBL_BushesCloseEdge_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Treeline_Dense | 4 | MBL_Pine_06mClose, MBL_Pine_SaplingsClose, MBL_BushesCloseEdge, MBL_BushesCloseEdge_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Treeline_Sparce | 4 | MBL_Pine_06mClose, MBL_Pine_SaplingsClose, MBL_BushesCloseEdge, MBL_BushesCloseEdge_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Pine | MB_Pine_Treeline_Sparce_02 | 4 | MBL_Pine_06mClose, MBL_Pine_SaplingsClose, MBL_BushesCloseEdge, MBL_BushesCloseEdge_NoCol | Icon_Tree_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Plants | MB_BushesRock_Dense | 3 | MBL_BushesEdge_NoCol, MBL_Bushes, MBL_Rocks_Medium | Icon_BushRock_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Plants | MB_BushesRock_Sparse | 3 | MBL_BushesEdge_NoCol, MBL_Bushes, MBL_Rocks_Medium | Icon_BushRock_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Plants | MB_Bushes_Dense | 2 | MBL_Bushes_NoCol, MBL_Bushes | Icon_Bush_BC | - | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/Plants | MB_Bushes_Sparse | 2 | MBL_BushesEdge_NoCol, MBL_Bushes | Icon_Bush_BC | - | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/Plants | MB_Rock_Dense | 1 | MBL_Rocks_Medium | Icon_Rock_BC | - | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/Plants | MB_Spline_Bushes | 2 | MBL_BushesCloseEdge, MBL_BushesCloseEdge_NoCol | Icon_Bush_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Plants | MB_Spline_BushesNoCol | 4 | MBL_Deciduous_08mTrees, MBL_BushesEdge_NoCol, MBL_Deciduous_Saplings, MBL_Rocks_Medium | Icon_Bush_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/Plants | MB_Spline_Bushes_Sparse | 2 | MBL_BushesEdge_NoCol, MBL_Bushes | Icon_Bush_BC | - | 3 / 1 | 1000 | - | no |
| PCG/MicroBiomes/River | MB_River_Playspace | 3 | MBL_Rocks_River_CoverLarge, MBL_Rocks_Riverbed, MBL_Rocks_River_CoverMedium | Icon_River_BC | - | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/River | MB_River_Sparse | 2 | MBL_Rocks_Riverbed, MBL_Rocks_River_CoverMedium | Icon_River_BC | 0.8 | 3 / 1 | 1000 | 1 | no |
| PCG/MicroBiomes/River | MB_River_Sparse_Europe | 2 | MBL_Rocks_Riverbed, MBL_Rocks_River_CoverMedium | Icon_River_BC | 0.8 | 3 / 1 | 1000 | 1 | no |

### 3b. Layer-entry parameters (145 entries across all 41 biomes)

Each entry in `Layers` is a struct with the fields below. Counts are over all 145 entries.

| Field | What the data shows | Notes |
|---|---|---|
| `Enabled` | 136 on, 9 off | Disabled entries: `MB_Forest_Interior_Sparse` (MBL_Forest_Undergrowth), `MB_Woodland_TreeLine` (MBL_Woodland_Undergrowth), `MB_Deciduous_Interior_DensePlayspace` (MBL_Woodland_Trees_Ferns_NoCol), `MB_Deciduous_Spline_Dense` (MBL_Rocks_Medium), `MB_Pine_Interior_Dense_Playspace` and `MB_Pine_Interior_Sparse_Playspace` (MBL_Pine_06m), `MB_Spline_BushesNoCol` (3 entries: MBL_Deciduous_08mTrees, MBL_Deciduous_Saplings, MBL_Rocks_Medium). |
| `AreaOfInfluence` | Most common: 100 (20 entries), 300 (17), 400 (12), 200 (12), 1000 (11), 600 (8), 150 (8), 500 (8) | Unit assumed cm (Unreal default). Not confirmed. |
| `Density` | Most common: 1.0 (44), 0.5 (28), 0.6 (14), 0.3 (11), 0.01 (10), 0.8 (9), 0.04 (7), 0.4 (5) | Relative placement density for that layer within the biome. Inferred from name and range. |
| `AreaDensityThreshold` | 0.0 (105), 0.1 (30), -1.0 (6), 0.2 (3), -0.3 (1) | Gate on the biome's area-density value. Inferred. |
| `AreaDensityOffset` | 0.0 (88), then scattered values such as -0.3, 1.0, -0.7552 | Offset applied to the area-density value. Inferred. |
| `AreaDensityInvert` | false (104), true (41) | Inverts the threshold test. |
| `IgnoreLandscapeLayers` | true on 6 entries | Ignores landscape-layer filtering for that entry. |
| `UseTransitionMeshes` | true on 2 entries | |
| `IgnoreTransformOffsets` | true on 1 entry | |
| `RVTDataAsset` | never set (0 of 145) | Runtime virtual texture hook is unused in this dump. |

Worked example, `MB_Pine_Treeline` (4 entries, all enabled): `MBL_Pine_06mClose` (AreaOfInfluence 1800, Density 0.5, threshold -1.0, invert on), `MBL_Pine_SaplingsClose` (100, 0.5, threshold 0.0, invert on), `MBL_BushesCloseEdge` (100, 0.3, threshold 0.0, invert off), `MBL_BushesCloseEdge_NoCol` (100, 0.6, threshold 0.0, invert off). The first entry has a very large influence radius and the other three are small.

---

## 4. Layers (`PDA_MBLayer_C`, 43 assets)

A layer picks clusters by weight and decides where they go. `Clusters` is a weighted list; each entry carries `Weight` and `OffsetMin`/`OffsetMax` (2D). Layer-level fields: `SamplingMode` (set on 14 layers), `UsePointGrid` (19 layers), `PointGridColMultiplier` (rare), `AngleRangeMin` (0.9 on 7 layers, 0.85 on 5, 0.95 on 2, 0.0 on 2), `FilterByAngle` (7 layers, all false), `MustBeOnGround` (4 layers), `ExcludeSplines` and `InvertFilter` (rare). `AngleRangeMin` values of 0.85 to 0.95 look like a cosine threshold on surface normal (about 18 to 32 degrees). That reading is inferred, not confirmed.

### 4a. Catalogue

| Layer asset | Folder | Clusters | Cluster assets (weight) | Sampling | Point grid | Angle min | Ground | Extra |
|---|---|---|---|---|---|---|---|---|
| MBL_Farm_Crop_Maize | Foliage/Biomes/Farm/Layers | 1 | MBC_Crop_Maize (1) | NewEnumerator2 | yes | - | no | gridColMult 0.3 |
| MBL_Farm_Crop_Sunflower | Foliage/Biomes/Farm/Layers | 1 | MBC_Crop_Sunflower (1) | NewEnumerator2 | yes | - | no | gridColMult 0.05 |
| MBL_Forest_Bushes | Foliage/Biomes/Forest/Layers | 2 | MBC_Tree_Beech_Bush_01a (1), MBC_Bush_01a (1) | - | no | - | no | - |
| MBL_Forest_Bushes_Transition | Foliage/Biomes/Forest/Layers | 2 | None (1), None (1) | - | no | - | no | - |
| MBL_Forest_Embankments | Foliage/Biomes/Forest/Layers | 1 | MBC_Embankment_01a (1) | - | no | 0.9 | no | - |
| MBL_Forest_Trees_06m_Canopy | Foliage/Biomes/Forest/Layers | 1 | MBC_Tree_Pine_Forest_06mCanopy_01a (1) | - | yes | - | no | gridColMult 2 |
| MBL_Forest_Trees_Saplings | Foliage/Biomes/Forest/Layers | 2 | MBC_Pine_Sapling_Large_01a (1), MBC_Pine_Sapling_Small_01a (1) | - | no | - | no | - |
| MBL_Forest_Trees_Stumps | Foliage/Biomes/Forest/Layers | 1 | MBC_Pine_Stump_01a (1) | - | no | - | no | - |
| MBL_Forest_Trees_TreeLine | Foliage/Biomes/Forest/Layers | 1 | MBC_Tree_Pine_ForestEdge_10mCanopy_01a (1) | - | no | - | no | - |
| MBL_Forest_Undergrowth | Foliage/Biomes/Forest/Layers | 6 | MBC_Rock_Forest_2m_Low_01a (0.5), MBC_Tree_Pine_Branch_Large_01a (0.5), MBC_Tree_Pine_Twigs_01a (1), MBC_Plant_Fern_01a (1), MBC_Weed_Nettle (0.5), MBC_Rock_Forest_Stones_01a (1) | - | no | - | no | - |
| MBL_Woodland_Bushes | Foliage/Biomes/Woodland/Layers | 2 | MBC_Tree_Beech_Bush_01a (1), MBC_Bush_01a (1) | - | no | - | no | - |
| MBL_Woodland_Trees_Ferns_NoCol | Foliage/Biomes/Woodland/Layers | 2 | MBC_Fern01 (1), MBC_Fern02 (1) | - | no | - | no | - |
| MBL_Woodland_Trees_TreeLine | Foliage/Biomes/Woodland/Layers | 2 | MBC_Tree_Beech_ForestEdge_08mCanopy_01a (1), MBC_Tree_Beech_ForestEdge_06mCanopy_01a (1) | - | yes | 0.9 | no | - |
| MBL_Woodland_Undergrowth | Foliage/Biomes/Woodland/Layers | 8 | MBC_Tree_Beech_Seedling_01a (1), MBC_Tree_Beech_Seedling_02a (1), MBC_Tree_Beech_Branch_Large_01a (1), MBC_Tree_Beech_Debris_01a (1), MBC_Weed_Nettle (1), MBC_Vines_Ivy_Debris (1), MBC_Vines_Ivy_Debris_Small (1), MBC_Rock_Forest_Stones_01a (1) | - | no | - | no | - |
| MBL_Ash_Canopy_10m | PCG/MicroBiomes/Deciduous/Layers | 1 | MBC_Tree_Ash_Forest_10mCanopy_01a (1) | - | yes | 0.85 | no | - |
| MBL_Beech_Canopy_10m | PCG/MicroBiomes/Deciduous/Layers | 1 | MBC_Tree_Beech_Forest_10mCanopy_01a (0.5) | - | yes | 0.85 | no | - |
| MBL_Beech_Canopy_6m | PCG/MicroBiomes/Deciduous/Layers | 1 | MBC_Tree_Beech_Forest_08mCanopy_01a (0.5) | - | yes | 0.85 | no | - |
| MBL_Deciduous_08mTrees | PCG/MicroBiomes/Deciduous/Layers | 3 | MBC_Tree_Beech_ForestEdge_08mCanopy_01a (1), MBC_Tree_Birch_ForestEdge_08mCanopy_01a (1), MBC_Tree_Ash_ForestEdge_8mCanopy_01a (1) | - | no | - | no | - |
| MBL_Deciduous_08mTreesClose | PCG/MicroBiomes/Deciduous/Layers | 3 | MBC_Tree_Beech_ForestEdge_08mCanopy_01a (1), MBC_Tree_Birch_ForestEdge_08mCanopy_01a (1), MBC_Tree_Ash_ForestEdge_8mCanopy_01a (1) | - | no | - | no | - |
| MBL_Deciduous_Saplings | PCG/MicroBiomes/Deciduous/Layers | 4 | MBC_Tree_Beech_Sapling_01a (0.8), MBC_Tree_Beech_Sapling_02a (0.8), MBC_Tree_Birch_Sapling_01a (0.2), MBC_Tree_Birch_Sapling_02a (0.2) | - | no | - | no | - |
| MBL_Oak_Canopy | PCG/MicroBiomes/Deciduous/Layers | 1 | MBC_Tree_Oak_Field_01a (0.5) | - | yes | 0.85 | no | - |
| MBL_Pine_06m | PCG/MicroBiomes/Pine/Layers | 1 | MBC_Pine_06m (1) | NewEnumerator2 | yes | 0.9 | no | - |
| MBL_Pine_06mClose | PCG/MicroBiomes/Pine/Layers | 1 | MBC_Pine_06m (1) | NewEnumerator2 | yes | 0.9 | no | - |
| MBL_Pine_06m_Edge | PCG/MicroBiomes/Pine/Layers | 1 | MBC_Pine_06mEdge (1) | NewEnumerator2 | yes | 0.85 | no | - |
| MBL_Pine_10m | PCG/MicroBiomes/Pine/Layers | 1 | MBC_Pine_10m (1) | - | yes | 0.9 | no | - |
| MBL_Pine_Saplings | PCG/MicroBiomes/Pine/Layers | 2 | MBC_Pine_Sapling_Large_01a (0.05), MBC_Pine_Sapling_Small_01a (1) | NewEnumerator2 | yes | - | no | - |
| MBL_Pine_SaplingsClose | PCG/MicroBiomes/Pine/Layers | 2 | MBC_Pine_Sapling_Large_01a (0.05), MBC_Pine_Sapling_Small_01a (1) | NewEnumerator2 | yes | - | no | - |
| MBL_Pine_SaplingsEdge | PCG/MicroBiomes/Pine/Layers | 2 | MBC_Pine_Sapling_Large_01a (0.1), MBC_Pine_Sapling_Small_01a (0.7) | NewEnumerator2 | yes | - | no | - |
| MBL_Bushes | PCG/MicroBiomes/Plants/Layers | 2 | MBC_Tree_Beech_Bush_01a (1), MBC_Bush_01a (0) | NewEnumerator2 | no | - | no | - |
| MBL_BushesCloseEdge | PCG/MicroBiomes/Plants/Layers | 2 | MBC_Tree_Beech_Bush_01a (1), MBC_Bush_01a (0) | NewEnumerator2 | no | - | no | - |
| MBL_BushesCloseEdge_NoCol | PCG/MicroBiomes/Plants/Layers | 1 | MBC_Bush_NoCol (1) | NewEnumerator2 | no | - | no | - |
| MBL_BushesEdge_NoCol | PCG/MicroBiomes/Plants/Layers | 1 | MBC_Bush_NoCol (1) | NewEnumerator2 | no | - | no | - |
| MBL_Bushes_NoCol | PCG/MicroBiomes/Plants/Layers | 1 | MBC_Bush_NoCol (1) | NewEnumerator2 | no | - | no | - |
| MBL_Logs | PCG/MicroBiomes/Plants/Layers | 4 | MBC_Log_Pile01 (0.15), MBC_Log_Pile02 (0.2), MBC_Log_Short (0.1), MBC_Log_Long (0.5) | - | yes | 0.95 | yes | - |
| MBL_Sticks | PCG/MicroBiomes/Plants/Layers | 1 | MBC_Scatter_Sticks (1) | NewEnumerator2 | no | - | no | - |
| MBL_Rocks_River_CoverLarge | PCG/MicroBiomes/River/Layers | 1 | MBC_Rock_River_Cover_Large_01 (1) | - | yes | 0 | yes | - |
| MBL_Rocks_River_CoverMedium | PCG/MicroBiomes/River/Layers | 2 | MBC_Rock_River_Cover_Medium_01 (1), MBC_Rock_River_Cover_Medium_02 (0.5) | - | yes | 0 | yes | - |
| MBL_Rocks_Riverbed | PCG/MicroBiomes/River/Layers | 2 | MBC_Rock_Riverbed_02 (0.7), MBC_Rock_Riverbed_01 (0.85) | - | yes | 0.95 | yes | - |
| MBL_Rock_Huge | PCG/MicroBiomes/Rocks/Layers | 1 | MBC_Rock_Huge (0.5) | - | no | 0.9 | no | InvertFilter |
| MBL_Rocks_Medium | PCG/MicroBiomes/Rocks/Layers | 2 | MBC_Rock_Forest_2m_Med_01a (0.5), MBC_Rock_Forest_2m_Low_01a (0.5) | - | no | 0.9 | no | - |

---

## 5. Clusters (`PDA_MBCluster_C`, 60 assets)

A cluster is one placeable tree, plant, rock, or log. `CoreMesh` is the main mesh. `Scatterers` reference `PDA_MBScatter` assets (12 clusters), each with `Radius`, `ExtentsMultiply`, and `ExcludeFromSplines`. `Modules` are mesh bundles with `Weight`, `SpawnChance`, cull distances, and HLOD flags (12 clusters). `ScaleMin`/`ScaleMax`, `RotationMin`/`RotationMax`, `AlignToWorldUpAxis` (0 to 1, how far the instance follows the ground normal), `OffsetMinZ`/`OffsetMaxZ`, and `BoundsModifierMin`/`Max` shape each placement. `DecalMaterial` is set on 19 clusters and `DecalMinMaxScale` on 25. `DebugColor` is an editor tint. In the scale column, `?` means `ScaleMin` is not set in the asset, so the engine default applies (not in the export).

### 5a. Catalogue

| Asset | Core mesh | Scale min-max | Align up | Z offset min/max | Bounds mod min/max | Decal mat | Decal scale | Scatterers | Modules | Debug |
|---|---|---|---|---|---|---|---|---|---|---|
| MBC_Crop_Maize | SM_Crop_Maize_05a | ? to 1.5 | 0.8 | -20 / -10 | (72.5, 72.5, 0) / (-72.5, -72.5, -150) | - | (4, 5) | MBS_Crop_Maize | - | 9C11FF |
| MBC_Crop_Sunflower | SM_Crop_Sunflower_10a | 0.85 to 1.15 | 0.8 | - / - | (100, 100, 0) / (-100, -100, -100) | - | (3, 5) | - | - | 9C11FF |
| MBC_Plant_Fern_01a | - | ? to 1.15 | 0 | - / - | - / - | - | - | MBS_Plant_Fern, MBS_Weed_Nettle | - | D91FFF |
| MBC_Tree_Ash_ForestEdge_8mCanopy_01a | SM_Tree_Ash_ForestEdge_8mCanopy_01a_Core | 0.85 to 1.15 | 0.8 | -100 / -40 | (350, 350, 0) / (-350, -350, 0) | MI_RVT_Leaves_Fallen_Dying_01a_WS | (15, 20) | - | 4 | FF00FF |
| MBC_Fern01 | SM_CF_PlantFernA1 | ? to 3 | 0.8 | - / - | (50, 50, 0) / (-50, -50, 0) | - | - | - | - | 890089 |
| MBC_Fern02 | SM_CF_PlantFernA2 | 0.8 to 2 | 0.8 | - / - | (50, 50, 0) / (-50, -50, 0) | - | - | - | - | 890089 |
| MBC_Tree_Beech_Branch_Large_01a | SM_Tree_Beech_Debris_BranchLarge_01a | 0.85 to 1.15 | 0 | - / - | - / - | - | - | - | - | 9C11FF |
| MBC_Tree_Beech_Bush_01a | SM_Tree_Beech_Bush_01a | 0.8 to 1.2 | 0.8 | -40 / -20 | (150, 150, 0) / (-150, -150, 0) | MI_RVT_PineTrees_001_WS | (7, 12) | - | - | 890089 |
| MBC_Tree_Beech_Bush_01a_Transition | SM_Tree_Beech_Bush_01a | 0.85 to 1.15 | 0.8 | - / - | - / - | - | - | - | - | 890089 |
| MBC_Tree_Beech_Bush_02a_Transition | SM_Tree_Beech_Bush_02a | 0.85 to 1.15 | 0.8 | - / - | - / - | - | - | - | - | 890089 |
| MBC_Tree_Beech_Debris_01a | - | 0.85 to 1.15 | 0 | - / - | - / - | - | - | - | - | A89A4B |
| MBC_Tree_Beech_ForestEdge_06mCanopy_01a | SM_Tree_Beech_ForestEdge_06mCanopy_01a_Core | 0.85 to 1.15 | - | - / - | - / - | - | - | - | 3 | 890089 |
| MBC_Tree_Beech_ForestEdge_08mCanopy_01a | SM_Tree_Beech_ForestEdge_08mCanopy_01a_Core | 0.85 to 1.15 | - | -400 / -100 | (350, 350, 0) / (-350, -350, 0) | MI_RVT_Leaves_Fallen_Dying_01a_WS | (10, 20) | - | 4 | 890089 |
| MBC_Tree_Beech_Forest_08mCanopy_01a | SM_Tree_Beech_Forest_08mCanopy_01a_Core | 0.8 to 1.3 | 0.8 | -400 / -40 | (250, 250, 0) / (-250, -250, 0) | MI_RVT_PineTrees_001_WS | (25, 40) | - | 4 | FFFF00 |
| MBC_Tree_Beech_Forest_10mCanopy_01a | SM_Tree_Beech_Forest_10mCanopy_01a_Core | 0.8 to 1.3 | 0.9 | -50 / -40 | (325, 325, 0) / (-325, -325, 0) | MI_RVT_PineTrees_001_WS | (25, 40) | - | 4 | FFBC00 |
| MBC_Tree_Beech_Sapling_01a | SM_Tree_Beech_Sapling_01a | 0.8 to 1.3 | 0.8 | -100 / -20 | - / - | - | - | - | - | 890089 |
| MBC_Tree_Beech_Sapling_02a | SM_Tree_Beech_Sapling_02a | 0.8 to 1.3 | 0.8 | -100 / -40 | - / - | - | - | - | - | 890089 |
| MBC_Tree_Beech_Seedling_01a | SM_Tree_Beech_Seedling_01a | 0.85 to 1.15 | 0 | - / - | - / - | - | - | - | - | 890089 |
| MBC_Tree_Beech_Seedling_02a | SM_Tree_Beech_Seedling_02a | 0.85 to 1.15 | 0 | - / - | - / - | - | - | - | - | 890089 |
| MBC_Tree_Birch_ForestEdge_08mCanopy_01a | SM_Tree_Birch_ForestEdge_08mCanopy_01a_Core | 0.85 to 1.15 | - | -100 / -40 | (350, 350, 0) / (-350, -350, 0) | MI_RVT_Leaves_Fallen_Dying_01a_WS | (15, 20) | - | 4 | 890089 |
| MBC_Tree_Birch_Sapling_01a | SM_Tree_Birch_Sapling_01a | 0.85 to 1.15 | 1 | - / - | - / - | - | - | - | - | 890089 |
| MBC_Tree_Birch_Sapling_02a | SM_Tree_Birch_Sapling_02a | 0.85 to 1.15 | 1 | - / - | - / - | - | - | - | - | 890089 |
| MBC_Tree_Oak_Field_01a | SM_Tree_Oak_Field_01a_Core | 1.5 to 2.5 | 0.8 | -60 / -40 | (350, 300, 0) / (-300, -300, 0) | MI_RVT_PineTrees_001_WS | (25, 40) | - | 4 | FFBC00 |
| MBC_Tree_Pine_Branch_Large_01a | SM_Tree_Pine_Branch_Large_01a | 0.85 to 1.15 | 0 | - / - | - / - | - | - | - | - | 9C11FF |
| MBC_Tree_Pine_ForestEdge_10mCanopy_01a | SM_Tree_Pine_ForestEdge_10mCanopy_01a_Core | 0.85 to 1.15 | 0.9 | - / - | - / - | - | - | - | 1 | FFB006 |
| MBC_Tree_Pine_Forest_06mCanopy_01a | SM_Tree_Pine_Forest_06mCanopy_01a_Core | ? to 1.2 | 0.9 | -600 / -40 | - / - | - | - | - | - | FFFF11 |
| MBC_Tree_Pine_Twigs_01a | - | 0.85 to 1.15 | 0 | - / - | - / - | - | - | - | - | A89A4B |
| MBC_Vines_Ivy_Debris | - | ? to ? | - | - / - | - / - | - | - | MBS_Vines_Ivy_Debris | - | - |
| MBC_Vines_Ivy_Debris_Small | - | ? to ? | - | - / - | - / - | - | - | MBS_Vines_Ivy_Debris_Small | - | - |
| MBC_Weed_Nettle | - | ? to ? | 1 | - / - | - / - | - | - | MBS_Weed_Nettle | - | FF00B6 |
| MBC_Embankment_01a | SM_Embankment_High_Outer_01a | 1.2 to 1.4 | 0 | -300 / -300 | (1000, 1000, 0) / (-1000, -1000, 0) | - | - | MBS_Rock_Forest_Stones, MBS_Weed_Nettle, MBS_Grass_Field_Clump | - | 1CFF24 |
| MBC_Rock_Forest_Stones_01a | - | 0.85 to 1.15 | 0 | - / - | - / - | - | - | MBS_Rock_Forest_Stones, MBS_Weed_Nettle, MBS_Grass_Field_Clump | - | 1CFF24 |
| MBC_Tree_Ash_Forest_10mCanopy_01a | SM_Tree_Ash_Forest_10mCanopy_01a_Core | 0.8 to 1.3 | 0.8 | -100 / -40 | (300, 300, 0) / (-300, -300, 0) | MI_RVT_PineTrees_001_WS | (25, 40) | - | 4 | 896300 |
| MBC_Pine_06m | SM_Tree_Pine_ForestEdge_10mCanopy_01a_Core | ? to 1.5 | 0.9 | -200 / -100 | (350, 350, 0) / (-390, -350, 0) | MI_RVT_PineTrees_001_WS | (10, 25) | - | 1 | FFB006 |
| MBC_Pine_06mEdge | SM_Tree_Pine_ForestEdge_6mCanopy_01a_Core | ? to 1.75 | 0.8 | -50 / -20 | (350, 350, 0) / (-350, -350, 0) | MI_RVT_PineTrees_001_WS | (15, 25) | - | 1 | FF192F |
| MBC_Pine_10m | SM_Tree_Pine_Forest_10mCanopy_01a_Core | ? to 1.5 | 0.8 | -800 / -40 | (350, 350, 0) / (-350, -340, 0) | MI_RVT_PineTrees_001_WS | (30, 40) | MBS_Tree_Twigs | 1 | FF192F |
| MBC_Pine_Sapling_Large_01a | SM_Tree_Pine_Sapling_Large_01a | 0.9 to 1.3 | 0.8 | -100 / -5 | (150, 150, 0) / (-150, -150, 0) | MI_RVT_PineTrees_001_WS | (1.5, 2.5) | - | - | 0000FF |
| MBC_Pine_Sapling_Small_01a | SM_Tree_Pine_Sapling_Small_01a | 0.3 to 0.85 | 0.8 | -30 / -10 | (125, 125, 0) / (-125, -125, 0) | - | - | - | - | A89A4B |
| MBC_Pine_Stump_01a | SM_Tree_Pine_Stump_01a | 0.85 to 1.15 | 0.8 | - / - | - / - | MI_RVT_PineTrees_001_WS | (30, 40) | - | - | 1CFF24 |
| MBC_Bush_01a | SM_Tree_Beech_Bush_02a | 0.85 to 1.15 | 0.8 | - / - | - / - | MI_RVT_PineTrees_001_WS | (1, 3) | - | - | 890089 |
| MBC_Bush_NoCol | SM_Tree_Beech_Bush_01a_NoCol | 0.8 to 1.2 | 0.8 | -200 / -100 | (150, 150, 0) / (-150, -150, 0) | MI_RVT_PineTrees_001_WS | (4, 4) | - | - | 890089 |
| MBC_Log_Long | S_Large_Fallen_Tree_wd1mbcvbw_high_Var1 | 0.9 to 1.2 | 0 | -10 / - | (50, 50, 0) / (-50, -50, 0) | - | - | - | - | 1CFF24 |
| MBC_Log_Pile01 | SM_LogPile_Small_02 | ? to ? | 0 | -10 / - | - / - | - | - | MBS_Grass_Flowers, MBS_Grass_Field_Clump, MBS_Stumps, MBS_Branches | - | 1CFF24 |
| MBC_Log_Pile02 | SM_LogPile_Medium_02 | 0.8 to 1.2 | 0 | -10 / - | - / - | - | - | MBS_Grass_Flowers, MBS_Grass_Field_Clump, MBS_Stumps, MBS_Branches | - | 1CFF24 |
| MBC_Log_Short | S_Mossy_Birch_Log_tjsicjffa_high | 6 to 9 | 0 | -10 / - | (20, 10, 0) / (-20, -5, 0) | - | - | MBS_Grass_Flowers, MBS_Grass_Field_Clump | - | 1CFF24 |
| MBC_Scatter_Sticks | SM_TwigGroundScatter | 0.8 to 1.2 | 0.8 | -200 / -100 | (250, 250, 0) / (-250, -250, 0) | - | - | - | - | 890089 |
| MBC_Rock_River_Cover_Large_01 | S_Nordic_Forest_Cluster_Rock_Medium_xf3odif_lod3 | 4 to 6 | 0 | -20 / -20 | (50, 50, 0) / (-50, -50, 0) | - | (25, 40) | - | - | 896300 |
| MBC_Rock_River_Cover_Medium_01 | S_Nordic_Forest_Cluster_Rock_Medium_xf3odif_lod3 | 2 to 3 | 0 | -20 / -20 | - / - | - | (10, 20) | - | - | 896300 |
| MBC_Rock_River_Cover_Medium_02 | S_Nordic_Forest_Cluster_Rock_Medium_xf3odif_lod3 | 3 to 4 | 0 | -20 / -20 | (50, 50, 0) / (-50, -50, 0) | - | (10, 20) | - | - | 896300 |
| MBC_Rock_Riverbed_01 | S_Tundra_Rocky_Ground_vizsbgudw_high_Var1 | ? to 3 | 0 | - / -40 | (100, 100, 0) / (-100, -100, 0) | MI_RVT_Mud_01c | (15, 25) | - | - | 896300 |
| MBC_Rock_Riverbed_02 | S_Nordic_Beach_Rocky_Ground_ve3qdhmqx_high_Var1 | 3 to 6 | 0 | -25 / -25 | (150, 150, 0) / (-150, -150, 0) | - | (25, 40) | - | - | 896300 |
| MBC_Rock_Forest_2m_Low_01a | SM_Boulder_05a | 0.7 to ? | 0 | - / - | (50, 50, 50) / (-50, -50, -50) | MI_RVT_Rocks_001_WS | (5, 7.5) | - | - | 1CFF24 |
| MBC_Rock_Forest_2m_Med_01a | SM_Boulder_06a | 0.8 to 1.1 | 0 | - / - | (75, 75, 75) / (-75, -75, -75) | MI_RVT_Rocks_001_WS | (5, 7.5) | - | - | 1CFF24 |
| MBC_Rock_Huge | SM_Forest_Boulder_01a | 1.5 to 2 | 0 | -70 / -70 | (40, 40, 0) / (-50, -50, 0) | MI_RVT_Rocks_001_WS | (22, 22) | MBS_Bush_NoCol, MBS_Grass_Flowers, MBS_Grass_Field_Clump | - | 1CFF24 |

---

## 6. Scatters (`PDA_MBScatter_C`, 13 assets)

Low-density ground-detail passes used by clusters through `Scatterers`. All 12 `Data` references from clusters resolve to files in this dump. Fields: `Meshes`, `AreaOfInfluence`, `Density`, `ScaleMin`/`ScaleMax`, `OffsetMin`/`OffsetMax`, `StartCullDistance`/`EndCullDistance` (cm), and render flags (`ForceNoCollision`, `CastShadow`, `CastDynamicShadow`, `IncludeInHLOD`, `AllowOverlap`, Nanite pixel-programmable distances). Cull distances of 102400 mean effectively no culling.

### 6a. Catalogue

| Asset | Meshes | Area of influence | Density | Scale min-max | Offset min / max | Cull start-end | Extra |
|---|---|---|---|---|---|---|---|
| MBS_Branches | SM_Tree_Hawthorn_Debris_Branch_01a, SM_Tree_Hawthorn_Debris_Branch_02a | 20 | - | 0.8 to ? | (-200, -200, 0) / (200, 200, 0) | 2000 to 3000 | nocol=yes, castShadow=no, HLOD=no |
| MBS_Bush_NoCol | SM_Tree_Beech_Bush_01a_NoCol | 100 | 2 | 0.75 to ? | (0, 0, -100) / (0, 0, -50) | 102400 to 102400 | dynShadow=yes |
| MBS_Crop_Maize | SM_Crop_Maize_05a | 20 | - | ? to 1.5 | - / - | 10000 to 20000 | nocol=yes |
| MBS_Grass_Field_Clump | SM_Grass_Field_Tall_05a | 0 | - | 0.75 to 1.25 | - / - | 4000 to 5000 | HLOD=no |
| MBS_Grass_Flowers | SM_Grass_Field_Flowers_01a | 20 | 0.5 | ? to 2 | (-50, -50, 0) / (50, 50, 0) | 7000 to 8000 | castShadow=no, HLOD=no |
| MBS_Plant_Fern | SM_Plant_Fern_Large_01a | 80 | 0.5 | ? to 2 | (-100, -100, -5) / (100, 100, -5) | 7000 to 8000 | dynShadow=yes, HLOD=no |
| MBS_Rock_Forest_Stones |  | 20 | - | 0.4 to 0.7 | (-100, -100, -2) / (100, 100, -2) | 9000 to 10000 | dynShadow=yes, HLOD=no |
| MBS_Stumps | SM_Tree_Beech_Stump_02a, SM_Tree_Beech_Stump_02a_Collision, SM_Tree_Beech_Stump_03a, SM_Tree_Beech_Stump_03a_Collision, SM_Dead_Branch_06_a | 300 | 0.01 | 0.8 to 1.5 | (-50, -50, -10) / (50, 50, -10) | 7000 to 8000 | nocol=yes, castShadow=no, HLOD=no |
| MBS_Tree_Twigs | SM_TwigGroundScatter | 20 | 2 | 2 to 3 | - / - | 3200 to 6400 | nocol=yes, castShadow=no, overlap=yes, HLOD=no |
| MBS_Vines_Ivy_Debris | SM_Vine_Ivy_GroundPlant_01a, SM_Vine_Ivy_GroundPlant_02a, SM_Vine_Ivy_GroundPlant_03a, SM_Vine_Ivy_Roots_01a, SM_Vine_Ivy_Roots_02a, SM_Vine_Ivy_Roots_03a | 100 | 0.3 | ? to ? | - / - | ? to ? |  |
| MBS_Vines_Ivy_Debris_Small | SM_Vine_Ivy_GroundPlant_01a, SM_Vine_Ivy_GroundPlant_02a, SM_Vine_Ivy_GroundPlant_03a | - | - | ? to ? | - / - | ? to ? |  |
| MBS_Weed_Nettle | SM_Weed_Nettle_01a, SM_Weed_Nettle_02a, SM_Weed_Nettle_03a, SM_Weed_Nettle_04a, SM_Weed_Nettle_05a | 10 | 0.25 | ? to 1.5 | (-50, -50, -2) / (50, 50, -2) | 2000 to 3000 |  |

---

## 7. Standalone cluster PCG (`PDA_ClusterPCG_C`, 34 assets)

Self-contained scatter definitions that bypass the MicroBiome chain. Most sit in `PCG/Kavkazi/DataAssets/Clusters` (fence posts, crop-field weeds, hedges). `StaticMeshes` is a weighted list; each entry can be `isModular` and carries optional `Twigs`, `Leaves`, and `Ivy` sub-meshes. `ScatterGridSize` and `ScatterGridCellsSize` are the point-grid dimensions (cm). `MaxNumOfScatterPts` caps points per cell. `Seed` is a fixed random seed. 18 of 22 assets share the seed `1301486335`, which looks like a copy-pasted default (inferred, not verified). Their random placement will therefore be correlated.

### 7a. Catalogue

| Asset | Folder | Meshes (weight) | Density | Max pts | Grid size / cell | Position min-max | Scale min-max | Cull start-end | Collision | Seed |
|---|---|---|---|---|---|---|---|---|---|---|
| DA_ClusterCrops_Maize | PCG/Kavkazi/DataAssets/Clusters | SM_Weed_Nettle_01a (1), SM_Weed_Nettle_02a (1), SM_Weed_Nettle_03a (1), SM_Weed_Nettle_04a (1), SM_Weed_Nettle_05a (1), SM_Bush_Bramble_Patch_1m_01a (1), SM_Bush_Bramble_Patch_3m_01a (1), SM_Bush_Bramble_Strand_01a (1), SM_Bush_Bramble_Strand_02a (1), SM_Bush_Bramble_Strand_Small_01a (1), SM_Bush_Bramble_Strand_Small_02a (1) | 0.2 | 50 | 200 / 50 | (-75, -75, 0) / (75, 75, 0) | 0.5 to ? | 12800 to 25600 | no | 21474 |
| DA_ClusterFields_BramblePatches | PCG/Kavkazi/DataAssets/Clusters | SM_Bush_Bramble_Patch_1m_01a (1), SM_Bush_Bramble_Strand_01a (1), SM_Bush_Bramble_Strand_02a (1), SM_Bush_Bramble_Strand_Small_01a (1), SM_Bush_Bramble_Strand_Small_02a (1), SM_Weed_Nettle_01a (1), SM_Weed_Nettle_02a (1), SM_Weed_Nettle_03a (1), SM_Weed_Nettle_04a (1) | 0.5 | 200 | - / 10 | (-500, -500, 0) / (500, 500, 0) | ? to 1.5 | 30000 to 50000 | no | 57395 |
| DA_ClusterHedge_Hawthorn | PCG/Kavkazi/DataAssets/Clusters | SM_Tree_Hawthorn_Sapling_01a (1), SM_Tree_Hawthorn_Sapling_02a (1), SM_Tree_Hawthorn_Seedling_01a (1), SM_Tree_Hawthorn_Seedling_02a (1), SM_Bush_Bramble_Patch_3m_01a (1), SM_Bush_Bramble_Patch_1m_01a (1), SM_Bush_Bramble_Strand_01a (1), SM_Bush_Bramble_Strand_02a (1), SM_Bush_Bramble_Strand_Small_01a (1), SM_Bush_Bramble_Strand_Small_02a (1), SM_Weed_Nettle_01a (1), SM_Weed_Nettle_02a (1), SM_Weed_Nettle_03a (1), SM_Weed_Nettle_04a (1), SM_Weed_Nettle_05a (1) | 0.2 | 20 | 300 / 10 | (-75, -75, 0) / (75, 75, 0) | 0.5 to ? | 30000 to 50000 | no | 54265 |
| DA_ClusterRhododendronSparse | PCG/Kavkazi/DataAssets/Clusters | SM_Weed_Nettle_03a (1), SM_Weed_Nettle_04a (1), SM_Weed_Nettle_05a (1), SM_Tree_Beech_Debris_BranchSmall_01a (1), SM_Tree_Beech_Debris_LeafPatch_01a (1) | - | 15 | 20 / 4 | (-100, -100, 0) / (100, 100, 0) | 0.5 to ? | 7000 to 10000 | no | 1301486335 |
| DA_Cluster_Weeds_01 | PCG/Kavkazi/DataAssets/Clusters | SM_Tree_Hawthorn_Seedling_01a (0.04), SM_Tree_Hawthorn_Seedling_02a (0.04), SM_Bush_Bramble_Patch_3m_01a (0.7), SM_Bush_Bramble_Patch_1m_01a (1), SM_Weed_Nettle_01a (1), SM_Weed_Nettle_02a (1), SM_Weed_Nettle_03a (1), SM_Weed_Nettle_05a (1) | - | 10 | 200 / 13 | (-75, -75, -10) / (75, 75, -2) | 0.5 to ? | 30000 to 50000 | no | 43509 |
| DA_FencePost_Concrete_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Fence_Concrete_Generic_01_Pillar_01b (0.3), SM_Fence_Concrete_Generic_01_Pillar_01a (1) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | no | 1301486335 |
| DA_FencePost_Concrete_Wall_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Concrete_Industrial_01_Pillar_01a (1), SM_Wall_Concrete_Industrial_01_Pillar_01b (0.25) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | no | 1301486335 |
| DA_FencePost_GasPipe_300_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_GasPipe_Support_300_01a (1) | - | - | 10 / 50 | (0, 0, 300) / (0, 0, 300) | ? to ? | ? to ? | no | 1301486335 |
| DA_FencePost_WoodBeams_Low_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Fence_Wood_02a_Support (1) | - | - | 10 / 50 | (0, 0, -5) / (0, 0, -5) | ? to ? | ? to ? | no | 1301486335 |
| DA_FencePost_Wood_Low_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Fence_Wood_Generic_02_Pillar_01a (1) | - | - | 10 / 50 | (0, 0, 5) / - | ? to ? | ? to ? | no | 1301486335 |
| DA_FencePost_Wood_Tall_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Fence_Wood_Generic_01_Pillar_01a (1) | - | - | 10 / 50 | (0, 0, 5) / (0, 0, 15) | ? to ? | ? to ? | no | 1301486335 |
| DA_Fence_Base_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Low_Wall_Left_01 (1) | - | - | 10 / 50 | (-20, 0, -110) / (-20, 0, -110) | ? to ? | ? to ? | no | 1301486335 |
| DA_Fence_Base_ChainLink_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Fence_Base_01a (1), SM_Fence_Base_01b (0.1) | - | - | 10 / 50 | (0, -10, -110) / (0, -10, -110) | 1.1 to 1.1 | ? to ? | no | 1301486335 |
| DA_Fence_Industrial_Metal_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Heap_Divider_Pillar_01a (1) | - | 1 | 10 / 50 | (0, 10, -40) / (0, 10, -40) | ? to ? | ? to ? | no | 1301486335 |
| DA_Fence_MetalBars_Pillar_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Fence_MetalBars_01_Pillar_01a (1) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | no | 1301486335 |
| DA_Fence_Tall_Stone_Pillar_02 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Stone_Generic_01_Pillar_01a (1) | - | - | 10 / 50 | (0, -2, -5) / (0, -2, -5) | ? to ? | ? to ? | no | 1301486335 |
| DA_Pillar_Brick_Industrial_01_Var_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Brick_Industrial_01_Pillar_01a (1) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | no | 1301486335 |
| DA_Pillar_ChurchExt_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Church_Ext_Pillar_Stone_01a (1) | - | - | 10 / 50 | (0, 0, -360) / (0, 0, -360) | ? to ? | ? to ? | no | 1301486335 |
| DA_Pillar_Church_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Stone_Generic_01_Pillar_01a (1) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | - | 1301486335 |
| DA_Wall_Concrete_Brickwall_01_Pillars | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Brick_Industrial_01_Pillar_01a (1) | - | - | 10 / 50 | - / - | 0.52 to 0.52 | ? to ? | no | 1301486335 |
| DA_Wall_Concrete_Industrial_01_Pillars_Straight | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Concrete_Industrial_01_Pillar_01b (0.5), SM_Wall_Concrete_Industrial_01_Pillar_01a (0.5) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | no | 1301486335 |
| DA_Wall_Concrete_Industrial_01_Pillars_Var_01 | PCG/Kavkazi/DataAssets/Clusters/Fence_Posts | SM_Wall_Concrete_Industrial_01_Pillar_01b (0.5), SM_Wall_Concrete_Industrial_01_Pillar_01a (0.5) | - | - | 10 / 50 | - / - | ? to ? | ? to ? | no | 1301486335 |

---

## 8. Spline PCG (`PDA_SplinePCG_C`, 57 assets)

Spline-driven placement for fences, walls, curbs, guardrails, tree lines, and embankments. `StaticMeshes` is the body mesh set. `EdgesStaticMeshes` (25 assets) are end caps and pillars placed at spline ends. `Distance` (33 assets) is the spacing along the spline in cm. `ProjectLocationOnGround` (26 of 39) snaps placed pieces to the ground. `ScaleToFitDistance` (35 of 39) stretches pieces to fit the spline length. Vegetation overlays are rare: `Twigs` on 3 assets, `Leaves` on 2, `Ivy` on 1.

### 8a. Catalogue

| Asset | Folder | Meshes | Edge meshes | Distance | Ground proj | Scale min-max | Twigs/Leaves/Ivy | Cull WPO |
|---|---|---|---|---|---|---|---|---|
| DA_SplineTreeDefault | PCG/Kavkazi/DataAssets/Splines/Biome | SM_Tree_Beech_ForestEdge_06mCanopy_01a_Core, SM_Tree_Beech_ForestEdge_08mCanopy_01a_Core, SM_Tree_Ash_ForestEdge_6mCanopy_01a_Core, SM_Tree_Ash_ForestEdge_8mCanopy_01a_Core | - | 350 | yes | ? to ? | - | - |
| DA_Spline_Curbs_Single_01a | PCG/Kavkazi/DataAssets/Splines/Biome | SM_Sidewalk_Curb_Single_100cm_01a, SM_Sidewalk_Curb_Single_100cm_01b, SM_Sidewalk_Curb_Single_100cm_01c, SM_Sidewalk_Curb_Single_100cm_01d, SM_Sidewalk_Curb_Single_100cm_01f, SM_Sidewalk_Curb_Single_100cm_01g | - | 98 | yes | ? to ? | - | - |
| DA_Embankment_Large_01 | PCG/Kavkazi/DataAssets/Splines/Embankments | SM_Embankment_High_Outer_01a | - | 760 | no | ? to ? | - | 2500 |
| DA_Curb_01a | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Sidewalk_Curb_Single_100cm_01a, SM_Sidewalk_Curb_Single_100cm_01b, SM_Sidewalk_Curb_Single_100cm_01c, SM_Sidewalk_Curb_Single_100cm_01d, SM_Sidewalk_Curb_Single_100cm_01f | - | 101 | no | ? to ? | - | - |
| DA_Curb_02a | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Sidewalk_Curb_Single_100cm_01a, SM_Sidewalk_Curb_Single_100cm_01b, SM_Sidewalk_Curb_Single_100cm_01c, SM_Sidewalk_Curb_Single_100cm_01d, SM_Sidewalk_Curb_Single_100cm_01f | - | 101 | yes | ? to ? | - | - |
| DA_Fence_BreezeBlock_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Brick_Residential_01a, SM_Wall_Brick_Residential_01b, SM_Wall_Brick_Residential_01c, SM_Wall_Brick_Residential_01d, SM_Wall_Brick_Residential_01e | SM_Fence_Base_01c | - | yes | ? to ? | - | - |
| DA_Fence_BrickWall_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_WoodTopped_Residential_01a, SM_Wall_WoodTopped_Residential_01b, SM_Wall_WoodTopped_Residential_01c | SM_Wall_WoodTopped_Residential_01_EndCap_L_01a | - | yes | ? to ? | - | - |
| DA_Fence_BrickWall_Hills_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_WoodTopped_Residential_01a, SM_Wall_WoodTopped_Residential_01b, SM_Wall_WoodTopped_Residential_01c | SM_Fence_Base_01c | - | yes | ? to ? | - | - |
| DA_Fence_ChainLink_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_ChainLinkFence_2m | SM_ChainLinkFence_1m_Damaged_01a | 220 | yes | ? to ? | Twigs | 1 |
| DA_Fence_ChainLink_04 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_ChainLinkFence_BarbedWire_2m, SM_ChainLinkFence_1m_Damaged_01a, SM_ChainLinkFence_2m | SM_ChainLinkFence_1m_Damaged_01a | 210 | yes | ? to ? | Twigs/Leaves | 1 |
| DA_Fence_ChainLink_Residential_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_ChainLink_Residential_01a | - | 201 | yes | ? to ? | - | 1 |
| DA_Fence_Concrete_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Concrete_Generic_01a, SM_Fence_Concrete_Generic_01c, SM_Fence_Concrete_Generic_01b | SM_Fence_Base_01c | 191 | yes | ? to ? | - | - |
| DA_Fence_Concrete_Large_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_MID_Wall_01a | - | 246 | no | ? to ? | - | - |
| DA_Fence_GasPipe_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_GasPipe_300_01a | - | 300 | no | ? to ? | - | 1 |
| DA_Fence_Industrial_Metal_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Heap_Divider_01a | SM_Fence_Base_01c | 298 | yes | ? to ? | - | - |
| DA_Fence_LowWoodWall_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_02a | SM_Fence_Wood_Generic_02_EndCap_L_01a, SM_Fence_Wood_Generic_02_EndCap_R_01a | - | yes | ? to ? | - | 1 |
| DA_Fence_LowWoodWall_01_Straight | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_02a | SM_Fence_Wood_Generic_02_EndCap_L_01a, SM_Fence_Wood_Generic_02_EndCap_R_01a | - | no | ? to ? | - | 1 |
| DA_Fence_Low_Concrete_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_FlowerBed_Concrete_WallSection_01a | SM_Fence_Wood_Generic_02_EndCap_L_01a, SM_Fence_Wood_Generic_02_EndCap_R_01a | 300 | no | ? to ? | - | 1 |
| DA_Fence_Low_Metal_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Decorative_Residential_2m_Straight_01a, SM_Fence_Decorative_Residential_2m_Straight_01b, SM_Fence_Decorative_Residential_2m_Straight_01c | SM_Fence_Decorative_Residential_2m_EndCap_L_01a | - | yes | ? to ? | - | 10 |
| DA_Fence_Low_WoodBeams_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_02a, SM_Fence_Wood_02b, SM_Fence_Wood_02c, None | SM_Fence_Wood_02a_Support | 400 | yes | ? to ? | - | 1 |
| DA_Fence_MetalBars_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_MetalBars_01a, SM_Fence_MetalBars_01b, SM_Fence_MetalBars_01c | SM_Fence_MetalBars_01_Pillar_01a | 400 | yes | ? to ? | - | 2500 |
| DA_Fence_Metal_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Metal_Residential_01a, SM_Fence_Metal_Residential_01b, SM_Fence_Metal_Residential_01c, SM_Fence_Metal_Residential_01d | SM_Fence_Base_01c | 191 | yes | ? to ? | - | - |
| DA_Fence_Ornate_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_OrnamentalFence_A_Gate_01a | - | 170 | no | ? to ? | - | - |
| DA_Fence_TallWoodWall_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01a | SM_Fence_Wood_Generic_01_EndCap_L_01a, SM_Fence_Wood_Generic_01_EndCap_R_01a | 201 | yes | ? to ? | - | 2500 |
| DA_Fence_TallWoodWall_02 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01d, SM_Fence_Wood_Generic_01e, SM_Fence_Wood_Generic_01f | SM_Fence_Wood_Generic_01_Pillar_01a, SM_Fence_Wood_Generic_01_Pillar_01a | - | yes | 0.95 to 1.05 | - | 2500 |
| DA_Fence_TallWoodWall_02_Straight | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01d, SM_Fence_Wood_Generic_01e, SM_Fence_Wood_Generic_01f | SM_Fence_Wood_Generic_01_Pillar_01a, SM_Fence_Wood_Generic_01_Pillar_01a | 201 | no | ? to ? | - | 2500 |
| DA_Fence_TallWoodWall_Damaged_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01d, SM_Fence_Wood_Generic_01e, SM_Fence_Wood_Generic_01f | SM_Fence_Wood_Generic_01_Pillar_01a, SM_Fence_Wood_Generic_01_Pillar_01a | 201 | yes | ? to ? | - | 2500 |
| DA_Fence_TallWoodWall_Damaged_01_Straight | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01a, SM_Fence_Wood_Generic_01d, SM_Fence_Wood_Generic_01e, SM_Fence_Wood_Generic_01f | SM_Fence_Wood_Generic_01_Pillar_01a, SM_Fence_Wood_Generic_01_Pillar_01a | 201 | no | ? to ? | - | 2500 |
| DA_Fence_Tall_Stone_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Stone_Generic_01a | SM_Wall_Stone_Generic_01_Pillar_01a | 400 | yes | ? to ? | Twigs/Leaves/Ivy | - |
| DA_Fence_Tall_Stone_Straight_02 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Stone_Generic_01a | SM_Fence_Base_01c | 400 | no | ? to ? | - | - |
| DA_Fence_Tall_Stone_Straight_03 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Stone_Generic_01a | SM_Wall_Stone_Generic_01_Pillar_01a | 400 | yes | ? to ? | - | 1 |
| DA_Fence_Tall_WoodMetalMix_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Fence_Wood_Generic_01a, SM_Fence_Metal_Residential_01c, SM_Fence_Wood_Generic_01d, SM_Fence_Wood_Generic_01e, SM_Fence_Metal_Residential_01d, SM_Fence_Metal_Residential_01a | SM_Fence_Wood_Generic_01_Pillar_01a, SM_Fence_Wood_Generic_01_Pillar_01a | 201 | yes | ? to ? | - | 2500 |
| DA_GuardRail_01a | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Road_Highway_Guardrail_02a | SM_Road_Highway_Guardrail_EndCap_01a | 445 | yes | ? to ? | - | - |
| DA_Wall_Brick_Industrial_01_Var_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Brick_Industrial_01a | - | 400 | no | 0 to ? | - | - |
| DA_Wall_Brick_Industrial_01_Var_02 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Brick_Industrial_01a | - | 400 | yes | ? to ? | - | - |
| DA_Wall_ChurchExt_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Church_Ext_Wall_Stone_01a, SM_Church_Ext_Wall_Stone_01b | - | 415 | no | ? to ? | - | 2500 |
| DA_Wall_Church_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Church | SM_Fence_Base_01c | 521 | yes | ? to ? | - | - |
| DA_Wall_Concrete_Industrial_01_Straight | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Concrete_Industrial_01a | - | 319 | no | ? to ? | - | - |
| DA_Wall_Concrete_Industrial_01_Var_01 | PCG/Kavkazi/DataAssets/Splines/Wall | SM_Wall_Concrete_Industrial_01a | - | 320 | yes | ? to ? | - | 2500 |

---

## 9. Grass settings (`DT_GrassSettings`)

A DataTable with row struct `GrassLayerInfo`. Five rows, one per grass layer. Each row has a `ScatterMaskChannel` (which RGBA channel of a mask texture it reads; the texture is not named in the export), a threshold and softness, the grass mesh, density, random and spatial noise, and scale ranges. All five rows share `LayerSeed = 42`.

### 9a. Rows

| Property | ShortGrass | Field | Forest | Farmland | River |
|---|---|---|---|---|---|
| ScatterMaskChannel | FF0000 | 00FF00 | 0000FF | FFFF00 | 00FFFF |
| ScatterMaskThreshold | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 |
| ScatterMaskSoftness | 0.2 | 0.2 | 0.2 | 0.2 | 0.1 |
| Mesh | SM_Grass_Field_Patch_Short_02a | SM_Grass_Tall_05a | SM_TwigGroundScatter | SM_Grass_Tall_05a | SM_Rock_Meadow_Stone_01a |
| Density | 1 | 0.8 | 0.1 | 0.8 | 0.9 |
| RandomNoiseScale | 100 | 100 | 20 | 100 | 100 |
| RandomPositionOffset | 100 | 100 | 100 | 100 | 100 |
| RandomScaleMinMax | (2, 2.2) | (1, 1.2) | (1.5, 2.5) | (1, 1.2) | (0.5, 1.5) |
| SpatialNoiseScale | 125 | 125 | 125 | 125 | 125 |
| SpatialNoiseStrength | 0.45 | 0.2 | 0.45 | 0.2 | 0.45 |
| ScaleByDensityMinMax | (1, 1.5) | (0.8, 1.2) | (0.8, 1) | (0.8, 1.1) | (0.8, 1.2) |
| LayerSeed | 42 | 42 | 42 | 42 | 42 |

---

## 10. Vehicle props (`PDA_VehicleProp_C`, 34 assets, plus `DT_VehiclePropList`)

Wrecks and parked vehicles built from modular meshes. `BaseMesh` is the chassis. `BaseGlassMesh`, `WheelMeshPrimary`, and `LoadMesh`/`CabinMesh`/`RoofMesh` add parts. `BaseColor`, `CabinColor`, `LoadColor`, and `WheelColor` are colour palettes (hex). `Wheel Uniform Scale` is set on 25 assets (0.67 to 1.025). The `DT_VehiclePropList` DataTable maps 29 row names to assets through an enum value.

Coverage check: 4 vehicle assets are **not** in `DT_VehiclePropList`: `DA_VehicleProp_Destroyed_Car_02a`, `DA_VehicleProp_Destroyed_CivilianCar02_01a`, `DA_VehicleProp_Ozeti_Van`, and `DA_VehicleProp_Truck_GasTank`. All 29 list references resolve to a file that exists. Enum values are cooked as `NewEnumeratorN`, so the list shows the index as exported.

### 10a. Catalogue

| Asset | Base mesh | Glass | Wheel mesh | Wheel scale | Load/Cabin/Roof mesh | Base colour(s) | Base scale | Override |
|---|---|---|---|---|---|---|---|---|
| DA_Abandoned_Tractor_01a | SM_Tractor_Abandoned_01a | - | SM_Bulldozer_Tyre_01a | 0.75 | - | A64840, D09F52, 5E778E, 6C9F7C | - | - |
| DA_Locomotive_01a | SM_Locomotive_01a | - | - | - | - | A5504D, D3B650, 507C56, 717171 | - | - |
| DA_Mini_Digger_01a | SM_MiniDigger_01 | - | - | - | - | 999696, D09F52, 5E778E, 6C9F7C | - | - |
| DA_SolarPanelUnit_01a | SM_Solar_Panel_Unit | - | SM_Wheel_03a | 0.85 | - | 999696, D09F52, 5E778E, 6C9F7C | - | - |
| DA_VehicleProp_Bulldozer_01a | SM_Bulldozer_01 | SM_Bulldozer_Glass_01 | SM_Bulldozer_Tyre_01a | - | load: SM_Bulldozer_Attachment_01, SM_Bulldozer_Attachment_02a, SM_Bulldozer_Attachment_03a | ACA8A8, D09F52, 9D7258, 6C7F95 | - | - |
| DA_VehicleProp_Bus | SM_Base_bus_01a | SM_Base_bus_Glass_01a | SM_Bus_Tyre | - | - | 9B9C9B | - | - |
| DA_VehicleProp_CivillianCar_01a | SM_CivilianCar01 | SM_Car01_VarB_Glass | SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.8 | - | A3A3A3, DDDDDD, 636D8A, 8A6364, C2A999 | - | - |
| DA_VehicleProp_CivillianCar_02a | SM_Civilian_Car_02a | SM_Civilian_Car_Glass_02a | SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.67 | - | 5B5B5B, 8C8989, D7D7D7, CFA771, 546982, 8A6364, 3E5141 | - | - |
| DA_VehicleProp_Destroyed_Car_01a | SM_DestroyedCar01 | - | - | 0.8 | - | 636D8A, BE6F75, CECBC3, 78765C, C2A999 | - | - |
| DA_VehicleProp_Destroyed_Car_02a | SM_DestroyedCar_02 | - | - | 0.8 | - | 636D8A, AB614F, CECBC3, 78765C, 75706C | - | - |
| DA_VehicleProp_Destroyed_CivilianCar02_01a | SM_CivilianCar02_Destroyed_01a | - | - | - | - | - | - | - |
| DA_VehicleProp_Exclavator_Tracks_01a | SM_Excavator_Body_01a | SM_Excavator_glass | - | - | load: SM_Excavator_tracks; cabin: SM_Excavator_arm_01a | BEBAB8 | - | - |
| DA_VehicleProp_Exclavator_Wheels_01a | SM_Excavator_Body_01a | SM_Excavator_glass | SM_Excavator_Wheels_Legs_01a | - | load: SM_Excavator_Wheels_01a; cabin: SM_Excavator_arm_01a; roof: SM_Excavator_Wheels_Legs_01a | C2BFBF | - | - |
| DA_VehicleProp_Faction_Generator_01 | SM_Lonestar_Faction_Generator | SM_Lonestar_Faction_Generator_Glass_01a | SM_Wheel_02c, SM_Wheel_03b, SM_Wheel_02b | 0.76 | - | - | - | - |
| DA_VehicleProp_Faction_Generator_02 | SM_FactionGenerator_02a | - | SM_Wheel_02c, SM_Wheel_03b, SM_Wheel_02b | 0.92 | cabin: SM_FactionGenerator02_TarpOpen_01a, SM_FactionGenerator02_TarpClosed_01a | - | - | - |
| DA_VehicleProp_Faction_Generator_02b | SM_FactionGenerator_02b | - | SM_Wheel_02c, SM_Wheel_03b, SM_Wheel_02b | 0.92 | - | - | - | - |
| DA_VehicleProp_Faction_Generator_03 | SM_FactionGenerator_03a | - | SM_Wheel_02c, SM_Wheel_03b, SM_Wheel_02b | 0.81 | - | - | - | - |
| DA_VehicleProp_FireTruck | SM_Chassis_01a | SM_CivilianTruck_Cab_Glass | SM_Bus_Tyre | 1.02 | load: SM_Fire_Truck_Boxbody_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_GasRepair | SM_Chassis_01a | SM_GassRepair_Glass_01a | SM_Bus_Tyre | 1.02 | load: SM_GasRepair_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_Lorry_40ft_01a | SM_Chassis_01a | SM_TruckRigidBodyGlass_01a | SM_Bus_Tyre | 0.93 | load: SM_Truck_Cab_Extension_01a; cabin: SM_TruckRigidBody_01a | - | BaseMesh 1.1, Cabin 1.1, Load 1.1, BaseGlassMesh 1.1 | - |
| DA_VehicleProp_Lorry_40ft_Trailer_01a | SM_Truck_Trailer_01a | - | SM_Bus_Tyre | 0.85 | - | 82A386, C84C4C, 75A5CC, AE904B | - | - |
| DA_VehicleProp_Lorry_Standard_01a | SM_Chassis_01a | SM_TruckRigidBodyGlass_01a | SM_Bus_Tyre | 0.85 | load: SM_TruckRigidBodyTrailer_01b, SM_TruckRigidBodyTrailer_01a; cabin: SM_TruckRigidBody_01a | - | - | - |
| DA_VehicleProp_Military_FuelTruck_01a | SM_Chassis_01a | SM_CivilianTruck_Cab_Glass | SM_Bus_Tyre | 1.02 | load: SM_CivilianTruck01_Tanker_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_Ozeti_Van | SM_Ozeti_Van_01a | SM_Ozeti_Van_Glass_01a | SM_Flat_Wheel_01a | - | cabin: SM_Ozeti_Van_Decal | B2B2B2 | - | - |
| DA_VehicleProp_Pickup_Truck_02 | SM_PickupTruck02_Chassis_01a | SM_PickupTruck02_Glass_01a | SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.8 | load: SM_PickupTruck02_BackBars_01a, SM_PickupTruck02_BoxBody_01a, 1x1x1_Box_Pivot_-XYZ; roof: SM_Standard_Rim | 634940, 66786B, 2E5063, CFA771, C3C0BB, C3BDB2, BEBAA6, 8C8989 | - | - |
| DA_VehicleProp_PoliceSedan | SM_Sedan_01a, SM_Sedan_01b | SM_Sedan_Glass_01a, SM_Sedan_Glass_02a | SM_Wheel_01a, SM_Wheel_01b, SM_Wheel_02a, SM_Wheel_02b, SM_Wheel_02c, SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.8 | roof: SM_Police_Light_01b | C2C1C2, CECBC3, D5D5D5 | - | MI_Sedan_PolicePaint |
| DA_VehicleProp_Sedan | SM_Sedan_01a, SM_Sedan_01b | SM_Sedan_Glass_01a, SM_Sedan_Glass_02a | SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.8 | - | DAD7D0, C86764, B3AB85, 7B97C0 | - | - |
| DA_VehicleProp_TaxiSedan | SM_Sedan_01b, SM_Sedan_01a | SM_Sedan_Glass_01a, SM_Sedan_Glass_02a | SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.8 | roof: SM_Taxi_Topper_01a | D3CFC7 | - | - |
| DA_VehicleProp_Truck | SM_Chassis_01a | SM_CivilianTruck_Cab_Glass | SM_Bus_Tyre | 1.02 | load: SM_WoodenDumpTruck_Flatbed_01a, SM_WoodenDumpTruck_01b, SM_WoodenDumpTruck_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_Truck_01d_Garbage | SM_Chassis_01a | SM_Truck_GarbageTruckVariant_Glass_01a | SM_Bus_Tyre | 1.02 | load: SM_Truck_GarbageTruckVariant_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_Truck_GasTank | SM_Chassis_01a | SM_CivilianTruck_Cab_Glass | SM_Bus_Tyre | 1.02 | load: SM_CivilianTruck01_Tanker_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_Truck_MobileCrane_01a | SM_Chassis_01a | SM_Truck_Mobile_Crane_Varient_Glass_01a | SM_Bus_Tyre | 1.02 | load: SM_Truck_Mobile_Crane_Variant_01a; cabin: SM_CivilianTruck_Cab_01a | - | - | - |
| DA_VehicleProp_Van | SM_Van_02a | SM_Van_02_Glass | SM_Flat_Wheel_01a, SM_Flat_Wheel_01b, SM_Flat_Wheel_02a, SM_Flat_Wheel_02b, SM_Flat_Wheel_02c | 0.9 | - | C46A68, EDEBE5, 839BB3 | - | - |

### 10b. DataTable rows (DT_VehiclePropList)

| Row name | Enum value | DataAsset |
|---|---|---|
| Abandoned_Tractor_01a | NewEnumerator21 | DA_Abandoned_Tractor_01a |
| Bulldozer_01 | NewEnumerator18 | DA_VehicleProp_Bulldozer_01a |
| Bus_01a | NewEnumerator5 | DA_VehicleProp_Bus |
| Civilian_Car_01a | NewEnumerator4 | DA_VehicleProp_CivillianCar_01a |
| Civilian_Car_02a | NewEnumerator24 | DA_VehicleProp_CivillianCar_02a |
| Destroyed_Cars_01a | NewEnumerator15 | DA_VehicleProp_Destroyed_Car_01a |
| Exclavator_Tracks | NewEnumerator14 | DA_VehicleProp_Exclavator_Tracks_01a |
| Exclavator_Wheels | NewEnumerator13 | DA_VehicleProp_Exclavator_Wheels_01a |
| Faction_Generator_01 | NewEnumerator28 | DA_VehicleProp_Faction_Generator_01 |
| Faction_Generator_02 | NewEnumerator29 | DA_VehicleProp_Faction_Generator_02 |
| Faction_Generator_02b | NewEnumerator31 | DA_VehicleProp_Faction_Generator_02b |
| Faction_Generator_03 | NewEnumerator30 | DA_VehicleProp_Faction_Generator_03 |
| Locomotive_01a | NewEnumerator22 | DA_Locomotive_01a |
| Lorry_40ft | NewEnumerator11 | DA_VehicleProp_Lorry_40ft_01a |
| Lorry_Standard | NewEnumerator10 | DA_VehicleProp_Lorry_Standard_01a |
| Lorry_Trailer_40ft | NewEnumerator12 | DA_VehicleProp_Lorry_40ft_Trailer_01a |
| Military_FuelTruck_01a | NewEnumerator32 | DA_VehicleProp_Military_FuelTruck_01a |
| Mini_Digger_01a | NewEnumerator20 | DA_Mini_Digger_01a |
| Pickup_Truck_02a | NewEnumerator23 | DA_VehicleProp_Pickup_Truck_02 |
| Sedan_01a | NewEnumerator1 | DA_VehicleProp_Sedan |
| Sedan_01b_Taxi | NewEnumerator8 | DA_VehicleProp_TaxiSedan |
| Sedan_01c_PoliceCar | NewEnumerator0 | DA_VehicleProp_PoliceSedan |
| SolarPanelUnit_01a | NewEnumerator33 | DA_SolarPanelUnit_01a |
| Truck_01a | NewEnumerator2 | DA_VehicleProp_Truck |
| Truck_01b_FireTruck | NewEnumerator9 | DA_VehicleProp_FireTruck |
| Truck_01c_GasRepair | NewEnumerator25 | DA_VehicleProp_GasRepair |
| Truck_01d_Garbage | NewEnumerator26 | DA_VehicleProp_Truck_01d_Garbage |
| Truck_MobileCrane_01a | NewEnumerator27 | DA_VehicleProp_Truck_MobileCrane_01a |
| Van_02a | NewEnumerator3 | DA_VehicleProp_Van |

---

## 11. Lighting presets (`PDA_LightSettings_C`, 9 assets)

Time-of-day and weather presets. Each has `UserTitle` (display name), `SkyMaterial` (HDRI), `DirectionalLightSettings` (sun), `SkyLightSettings`, `ExponentialHeightFogSettings`, `SkyAtmopshereSettings` (sic, the export's spelling), and `PostProcessSettings`. Sun `Intensity` runs from 9,000 (Morning) to 120,000 (Midday_01), and is probably lux (unit not stated). `Temperature` is in kelvin. Sky `LowerHemisphereIntensity` runs from 200 (Sunset) to 5,000 (Midday_01).

Each preset also has an `_Overkill` twin for every block, with its own sun intensity, sky lower-hemisphere intensity, and fog density. The export does not say what the `_Overkill` set is for (a higher-quality tier is a guess).

### 11a. Presets

| Asset | Title | Sky material | Sun pitch/yaw | Sun intensity (lux) | Sun temp (K) | Sky light | Lower hemi | Fog density | Fog 2nd density | Sky lum. tint |
|---|---|---|---|---|---|---|---|---|---|---|
| DA_LightSettings_AfternoonOvercast | DayLateGray | MI_HDRI_Overcast_001 | P-32.88 Y-149.82 R0 | 100 | 7000 | - | 500 | 0.015 | 0.002 | FFFFFF |
| DA_LightSettings_AfternoonOvercastFog | DayLateGrayFog | MI_HDRI_Overcast_001 | P-32.88 Y-149.82 R0 | 100 | 7000 | - | 700 | 0.015 | 0.02 | - |
| DA_LightSettings_Afternoon_01 | DayLateClear | MI_HDRI_Cloudy_001 | P-20.17 Y-170 R0 | 60000 | 5500 | 0.7 | 2000 | 0.004 | 0.002 | FFFFFF |
| DA_LightSettings_Midday_01 | DayClear | MI_HDRI_ClearSkies_001 | P-43.75 Y-88.8 R120 | 120000 | 8000 | 0.7 | 5000 | 0.009 | 0.002 | - |
| DA_LightSettings_Morning | DayEarlyClear | MI_HDRI_Morning | P-10.06 Y15.93 R0 | 6000 | 5500 | 0.7 | 300 | 0.002 | 0.0001 | - |
| DA_LightSettings_MorningFoggy | DayEarlyFog | MI_HDRI_Morning | P-10.06 Y15.93 R0 | 6000 | 5500 | 0.7 | 300 | 0.06 | - | - |
| DA_LightSettings_Sunrise | DayStartClear | MI_HDRI_Sunrise | P-5.06 Y16.22 R0 | 18000 | - | 0.7 | 400 | 0.007 | 0.003 | - |
| DA_LightSettings_Sunset | DayEndClear | MI_HDRI_Sunset | P-12.84 Y191 R1056.03 | 12000 | 5000 | 0.7 | 200 | 0.0009 | 0.0002 | - |

Overkill variants (sun / sky light / fog density):

| Asset | Overkill sun intensity | Overkill sun pitch/yaw | Overkill lower hemi | Overkill fog density |
|---|---|---|---|---|
| DA_LightSettings_AfternoonOvercast | 100 | P-32.88 Y-149.82 R0 | 1000 | 0.013 |
| DA_LightSettings_AfternoonOvercastFog | 100 | P-32.88 Y-149.82 R0 | 700 | 0.015 |
| DA_LightSettings_Afternoon_01 | 100000 | P-20.17 Y-157 R0 | 1000 | 0.007 |
| DA_LightSettings_Midday_01 | 200000 | P-43.75 Y-88.8 R120 | 1000 | 0.009 |
| DA_LightSettings_Morning | 6000 | P-10.06 Y15.93 R0 | 700 | 0.002 |
| DA_LightSettings_MorningFoggy | 6000 | P-10.06 Y15.93 R0 | 400 | 0.06 |
| DA_LightSettings_Sunrise | 18000 | P-5.06 Y16.22 R0 | 500 | 0.007 |
| DA_LightSettings_Sunset | 16000 | P-12.84 Y191 R1056.03 | 100 | 0.0009 |

| Asset | AutoExposureBias | AE min/max brightness | WhiteTemp | ColorContrast | VignetteIntensity | AO intensity |
|---|---|---|---|---|---|---|
| DA_LightSettings_AfternoonOvercast | - | 11 / 12 | 6000 | - | 0.3 | 0.85 |
| DA_LightSettings_AfternoonOvercastFog | - | 10.8 / 12.2 | 6000 | 1.2 | 0.3 | 0.85 |
| DA_LightSettings_Afternoon_01 | 1 | 11.3 / 12.3 | 6000 | 1.15 | 0.2 | 0.85 |
| DA_LightSettings_Midday_01 | 1 | 12.7 / 13.7 | 6000 | 1.15 | 0.3 | 0.7 |
| DA_LightSettings_Morning | 1 | 9 / 9.4 | 6000 | 1.15 | 0.3 | 0.85 |
| DA_LightSettings_MorningFoggy | 1 | 9.2 / 9.5 | 6000 | 1.15 | 0.3 | 0.85 |
| DA_LightSettings_Sunrise | 1 | 10 / 11 | - | 1.2 | 0.2 | 0.85 |
| DA_LightSettings_Sunset | 1 | 8.3 / 9 | 6000 | 1.1 | 0.3 | 0.85 |

---

## 12. Landscape colour curves

Two `CurveLinearColor` assets and one atlas that packs them. `CA_Landscape` (`CurveLinearColorAtlas`) lists `VC_Stratus` and `VC_GrassTint` and has `ImportedSize` 256 x 2. Each curve stores one float curve per channel. `VC_Stratus` uses R, G, and B (11 keys each), with A empty. `VC_GrassTint` uses all four channels (3 keys each). The export does not say which landscape material samples them; that is inferred from the names.

### 12a. Curves

| Curve | Channel | Keys | Time range | Value range |
|---|---|---|---|---|
| VC_Stratus | R | 11 | 0 to 1 | 0.5 to 0.625 |
| VC_Stratus | G | 11 | 0 to 1 | 0.45 to 0.6 |
| VC_Stratus | B | 11 | 0 to 1 | 0.4 to 0.55 |
| VC_Stratus | A | 0 | - | - |
| VC_GrassTint | R | 3 | 0.04 to 1 | 0.552 to 0.7 |
| VC_GrassTint | G | 3 | 0.04 to 1 | 0.6 to 0.7 |
| VC_GrassTint | B | 3 | 0.04 to 1 | 0.233 to 0.36 |
| VC_GrassTint | A | 3 | 0 to 1 | 0 to 0.125 |

---

## 13. Fluid Flux water (`PDA_FluxSimulationState_C` x54, `WDWaterHeightGridAsset` x40, `PDA_FluxSurfacePreset_C` x1)

Water is driven by one simulation state per area (`PDA_FluxSimulationState_C`). Each state covers a box: `AreaLocation` is the origin and `AreaSize` is the extent, both in cm. It points at three baked textures: `GroundMap`, `VelocityDepthFoamMap`, and `HeightWetMap`. `EncodeHeightMax` is 256 on all 54 states. `EncodeVelocityMax` is 5.0 on 40 states and missing on the 14 North America states. Every state has `Static = true` and `Compression = true`.

`Iteration` is a large integer (23,813 to 1,261,732) with no label in the export. `CaptureOffset` is a Z offset: Europe and Kavkazi states sit around -85,000 to -105,000 cm, and North America states are positive (+1,958 to +15,583 cm).

`WDWaterHeightGridAsset` holds the height grid. `GridWidth` is 512 (most), 256, or 128, `GridHeight` is 128 to 512, and `WorldSize` is in cm. Each grid links to one state through an unnamed field. The `Heights` array is decoded in section 13b (round 89). `CP_River_Kavkazi` is the only surface preset (clarity 0.66; scattering, absorption, and overlay colours).

Notes: 54 states exist, but only 40 have a height grid. The 14 `DA_Flux_NorthAmerica_*` states have no grid in this dump, and their velocity-encode field is missing too. They look incomplete or stored elsewhere.

### 13a. Simulation states

| Asset | Folder | Area location (X, Y, Z) | Area size (X x Y x Z) | Iteration | Capture offset | Ground / Velocity / Height maps | Encode max | Compression |
|---|---|---|---|---|---|---|---|---|
| PDA_Europe_0000 | Water/FluidFlux/Europe | (-590444, -584778, -94179) | 102400 x 25600 x 3000 | 110793 | -96429 | PDA_Europe_0000_Ground / PDA_Europe_0000_Velocity / PDA_Europe_0000_Height | H 256, V 5 | yes |
| PDA_Europe_0001 | Water/FluidFlux/Europe | (-685623, -581786, -94761) | 102400 x 25600 x 3000 | 127947 | -97011 | PDA_Europe_0001_Ground / PDA_Europe_0001_Velocity / PDA_Europe_0001_Height | H 256, V 5 | yes |
| PDA_Europe_0002 | Water/FluidFlux/Europe | (-784823, -588186, -97235) | 102400 x 25600 x 3000 | 132926 | -99485 | PDA_Europe_0002_Ground / PDA_Europe_0002_Velocity / PDA_Europe_0002_Height | H 256, V 5 | yes |
| PDA_Europe_0003 | Water/FluidFlux/Europe | (-880823, -600102, -97235) | 102400 x 25600 x 3000 | 102758 | -99485 | PDA_Europe_0003_Ground / PDA_Europe_0003_Velocity / PDA_Europe_0003_Height | H 256, V 5 | yes |
| PDA_Europe_0004 | Water/FluidFlux/Europe | (-494804, -572064, -93456) | 102400 x 51200 x 3000 | 55395 | -95706 | PDA_Europe_0004_Ground / PDA_Europe_0004_Velocity / PDA_Europe_0004_Height | H 256, V 5 | yes |
| PDA_Europe_0005 | Water/FluidFlux/Europe | (-414589, -528537, -92209) | 102400 x 51200 x 3000 | 64864 | -94459 | PDA_Europe_0005_Ground / PDA_Europe_0005_Velocity / PDA_Europe_0005_Height | H 256, V 5 | yes |
| PDA_Europe_0006 | Water/FluidFlux/Europe | (-317923, -528537, -91260) | 102400 x 51200 x 3000 | 46357 | -93510 | PDA_Europe_0006_Ground / PDA_Europe_0006_Velocity / PDA_Europe_0006_Height | H 256, V 5 | yes |
| PDA_Europe_0009 | Water/FluidFlux/Europe | (-707092, -1023996, -91931) | 204800 x 409600 x 6400 | 277444 | -96731 | PDA_Europe_0009_Ground / PDA_Europe_0009_Velocity / PDA_Europe_0009_Height | H 256, V 5 | yes |
| PDA_Europe_0010 | Water/FluidFlux/Europe | (-849081, -818788, -93924) | 102400 x 102400 x 3000 | 97729 | -96174 | PDA_Europe_0010_Ground / PDA_Europe_0010_Velocity / PDA_Europe_0010_Height | H 256, V 5 | yes |
| PDA_Europe_0011 | Water/FluidFlux/Europe | (-873965, -722145, -95052) | 51200 x 102400 x 3000 | 64723 | -97302 | PDA_Europe_0011_Ground / PDA_Europe_0011_Velocity / PDA_Europe_0011_Height | H 256, V 5 | yes |
| PDA_Europe_0012 | Water/FluidFlux/Europe | (-933711, -625397, -96852) | 102400 x 102400 x 3000 | 47507 | -99102 | PDA_Europe_0012_Ground / PDA_Europe_0012_Velocity / PDA_Europe_0012_Height | H 256, V 5 | yes |
| PDA_Europe_0014 | Water/FluidFlux/Europe | (-1174175, -509230, -98224) | 409600 x 204800 x 5000 | 207756 | -101974 | PDA_Europe_0014_Ground / PDA_Europe_0014_Velocity / PDA_Europe_0014_Height | H 256, V 5 | yes |
| PDA_Europe_007 | Water/FluidFlux/Europe | (-267609, -570821, -90752) | 51200 x 51200 x 3000 | 26321 | -93002 | PDA_Europe_007_Ground / PDA_Europe_007_Velocity / PDA_Europe_007_Height | H 256, V 5 | yes |
| PDA_Europe_008 | Water/FluidFlux/Europe | (-211647, -612833, -89578) | 102400 x 51200 x 3000 | 105211 | -91828 | PDA_Europe_008_Ground / PDA_Europe_008_Velocity / PDA_Europe_008_Height | H 256, V 5 | yes |
| PDA_Europe_013 | Water/FluidFlux/Europe | (-90047, -657633, -87889) | 204800 x 102400 x 5000 | 76306 | -91639 | PDA_Europe_013_Ground / PDA_Europe_013_Velocity / PDA_Europe_013_Height | H 256, V 5 | yes |
| PDA_Europe_015 | Water/FluidFlux/Europe | (-1361173, -317322, -101351) | 409600 x 204800 x 5000 | 127401 | -105101 | PDA_Europe_015_Ground / PDA_Europe_015_Velocity / PDA_Europe_015_Height | H 256, V 5 | yes |
| PDA_Europe_016 | Water/FluidFlux/Europe | (-793244, -1365284, -91047) | 307200 x 307200 x 5000 | 180576 | -94797 | PDA_Europe_016_Ground / PDA_Europe_016_Velocity / PDA_Europe_016_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_001 | Water/FluidFlux/Kavkazi | (-633700, -1660200, -79976) | 102400 x 102400 x 8000 | 63648 | -85976 | PDA_Flux_Bakurani_River_001_Ground / PDA_Flux_Bakurani_River_001_Velocity / PDA_Flux_Bakurani_River_001_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_000 | Water/FluidFlux/Kavkazi | (-53000, -932500, -88500) | 102400 x 102400 x 3000 | 76695 | -90750 | PDA_Flux_Bakurani_River_East_000_Ground / PDA_Flux_Bakurani_River_East_000_Velocity / PDA_Flux_Bakurani_River_East_000_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_001 | Water/FluidFlux/Kavkazi | (-151800, -908200, -89800) | 102400 x 102400 x 3000 | 190097 | -92050 | PDA_Flux_Bakurani_River_East_001_Ground / PDA_Flux_Bakurani_River_East_001_Velocity / PDA_Flux_Bakurani_River_East_001_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_002 | Water/FluidFlux/Kavkazi | (-251900, -907600, -90000) | 102400 x 102400 x 5000 | 155865 | -93750 | PDA_Flux_Bakurani_River_East_002_Ground / PDA_Flux_Bakurani_River_East_002_Velocity / PDA_Flux_Bakurani_River_East_002_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_003 | Water/FluidFlux/Kavkazi | (-348000, -927400, -91400) | 102400 x 102400 x 5000 | 137487 | -95150 | PDA_Flux_Bakurani_River_East_003_Ground / PDA_Flux_Bakurani_River_East_003_Velocity / PDA_Flux_Bakurani_River_East_003_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_004 | Water/FluidFlux/Kavkazi | (-443900, -940900, -91900) | 102400 x 102400 x 5000 | 222034 | -95650 | PDA_Flux_Bakurani_River_East_004_Ground / PDA_Flux_Bakurani_River_East_004_Velocity / PDA_Flux_Bakurani_River_East_004_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_005 | Water/FluidFlux/Kavkazi | (-539000, -994600, -91600) | 102400 x 102400 x 5000 | 138858 | -95350 | PDA_Flux_Bakurani_River_East_005_Ground / PDA_Flux_Bakurani_River_East_005_Velocity / PDA_Flux_Bakurani_River_East_005_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_006 | Water/FluidFlux/Kavkazi | (-634900, -994600, -92400) | 102400 x 102400 x 5000 | 77591 | -96150 | PDA_Flux_Bakurani_River_East_006_Ground / PDA_Flux_Bakurani_River_East_006_Velocity / PDA_Flux_Bakurani_River_East_006_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_007 | Water/FluidFlux/Kavkazi | (-732800, -994600, -93600) | 102400 x 102400 x 5000 | 178073 | -97350 | PDA_Flux_Bakurani_River_East_007_Ground / PDA_Flux_Bakurani_River_East_007_Velocity / PDA_Flux_Bakurani_River_East_007_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_East_008 | Water/FluidFlux/Kavkazi | (-832090, -994600, -96473) | 102400 x 102400 x 5000 | 66764 | -100223 | PDA_Flux_Bakurani_River_East_008_Ground / PDA_Flux_Bakurani_River_East_008_Velocity / PDA_Flux_Bakurani_River_East_008_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_RedSpawn_000 | Water/FluidFlux/Kavkazi | (-633700, -1566600, -84600) | 51200 x 102400 x 4000 | 160886 | -87600 | PDA_Flux_Bakurani_River_RedSpawn_000_Ground / PDA_Flux_Bakurani_River_RedSpawn_000_Velocity / PDA_Flux_Bakurani_River_RedSpawn_000_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_West_000 | Water/FluidFlux/Kavkazi | (-980800, -1008000, -98200) | 102400 x 102400 x 2000 | 483046 | -99700 | PDA_Flux_Bakurani_River_West_000_Ground / PDA_Flux_Bakurani_River_West_000_Velocity / PDA_Flux_Bakurani_River_West_000_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_West_001 | Water/FluidFlux/Kavkazi | (-1079800, -951400, -98200) | 102400 x 102400 x 2000 | 65161 | -99700 | PDA_Flux_Bakurani_River_West_001_Ground / PDA_Flux_Bakurani_River_West_001_Velocity / PDA_Flux_Bakurani_River_West_001_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_West_002 | Water/FluidFlux/Kavkazi | (-1177200, -928300, -98200) | 102400 x 102400 x 2000 | 63070 | -99700 | PDA_Flux_Bakurani_River_West_002_Ground / PDA_Flux_Bakurani_River_West_002_Velocity / PDA_Flux_Bakurani_River_West_002_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_West_003 | Water/FluidFlux/Kavkazi | (-1327933, -884437, -99000) | 204800 x 102400 x 2000 | 284089 | -100500 | PDA_Flux_Bakurani_River_West_003_Ground / PDA_Flux_Bakurani_River_West_003_Velocity / PDA_Flux_Bakurani_River_West_003_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_West_005 | Water/FluidFlux/Kavkazi | (-1469100, -831200, -100300) | 102400 x 102400 x 2000 | 23813 | -101800 | PDA_Flux_Bakurani_River_West_005_Ground / PDA_Flux_Bakurani_River_West_005_Velocity / PDA_Flux_Bakurani_River_West_005_Height | H 256, V 5 | yes |
| PDA_Flux_Bakurani_River_West_006 | Water/FluidFlux/Kavkazi | (-1539700, -823500, -100900) | 102400 x 102400 x 2000 | 248599 | -102400 | PDA_Flux_Bakurani_River_West_006_Ground / PDA_Flux_Bakurani_River_West_006_Velocity / PDA_Flux_Bakurani_River_West_006_Height | H 256, V 5 | yes |
| PDA_Flux_RedSpawn_001 | Water/FluidFlux/Kavkazi | (-704629, -1472756, -80065) | 102400 x 102400 x 12800 | 77615 | -89665 | PDA_Flux_RedSpawn_001_Ground / PDA_Flux_RedSpawn_001_Velocity / PDA_Flux_RedSpawn_001_Height | H 256, V 5 | yes |
| PDA_Flux_RedSpawn_002 | Water/FluidFlux/Kavkazi | (-768864, -1395100, -88900) | 51200 x 102400 x 5000 | 298983 | -92650 | PDA_Flux_RedSpawn_002_Ground / PDA_Flux_RedSpawn_002_Velocity / PDA_Flux_RedSpawn_002_Height | H 256, V 5 | yes |
| PDA_Flux_RedSpawn_003 | Water/FluidFlux/Kavkazi | (-813600, -1301700, -90945) | 102400 x 102400 x 5000 | 43496 | -94695 | PDA_Flux_RedSpawn_003_Ground / PDA_Flux_RedSpawn_003_Velocity / PDA_Flux_RedSpawn_003_Height | H 256, V 5 | yes |
| PDA_Flux_River_CZ_000 | Water/FluidFlux/Kavkazi | (-843960, -1207964, -92300) | 25600 x 102400 x 4000 | 58874 | -95300 | PDA_Flux_River_CZ_000_Ground / PDA_Flux_River_CZ_000_Velocity / PDA_Flux_River_CZ_000_Height | H 256, V 5 | yes |
| PDA_Flux_River_CZ_001 | Water/FluidFlux/Kavkazi | (-872362, -1135700, -94540) | 51200 x 102400 x 5000 | 244633 | -98290 | PDA_Flux_River_CZ_001_Ground / PDA_Flux_River_CZ_001_Velocity / PDA_Flux_River_CZ_001_Height | H 256, V 5 | yes |
| PDA_Flux_River_CZ_002 | Water/FluidFlux/Kavkazi | (-894250, -1046250, -94700) | 102400 x 102400 x 5000 | 125237 | -98450 | PDA_Flux_River_CZ_002_Ground / PDA_Flux_River_CZ_002_Velocity / PDA_Flux_River_CZ_002_Height | H 256, V 5 | yes |
| DA_Flux_NorthAmerica_000 | Water/FluidFlux/NorthAmerica | (-525815, -711871, 8649) | 409600 x 204800 x 4000 | 1261732 | 5649 | DA_Flux_NorthAmerica_000_Ground / DA_Flux_NorthAmerica_000_Velocity / DA_Flux_NorthAmerica_000_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_001 | Water/FluidFlux/NorthAmerica | (-281724, -527866, 6095) | 102400 x 204800 x 4000 | 584192 | 3095 | DA_Flux_NorthAmerica_001_Ground / DA_Flux_NorthAmerica_001_Velocity / DA_Flux_NorthAmerica_001_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_002 | Water/FluidFlux/NorthAmerica | (-173155, -348646, 9343) | 204800 x 204800 x 5000 | 404349 | 5593 | DA_Flux_NorthAmerica_002_Ground / DA_Flux_NorthAmerica_002_Velocity / DA_Flux_NorthAmerica_002_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_003 | Water/FluidFlux/NorthAmerica | (-264941, -197762, 5716) | 102400 x 102400 x 5000 | 204926 | 1966 | DA_Flux_NorthAmerica_003_Ground / DA_Flux_NorthAmerica_003_Velocity / DA_Flux_NorthAmerica_003_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_004 | Water/FluidFlux/NorthAmerica | (-339196, -119492, 5260) | 51200 x 102400 x 2500 | 741557 | 3385 | DA_Flux_NorthAmerica_004_Ground / DA_Flux_NorthAmerica_004_Velocity / DA_Flux_NorthAmerica_004_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_005 | Water/FluidFlux/NorthAmerica | (-301449, 24769, 5223) | 102400 x 204800 x 2500 | 416636 | 3348 | DA_Flux_NorthAmerica_005_Ground / DA_Flux_NorthAmerica_005_Velocity / DA_Flux_NorthAmerica_005_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_006 | Water/FluidFlux/NorthAmerica | (-209565, 136373, 4767) | 102400 x 51200 x 2500 | 195672 | 2892 | DA_Flux_NorthAmerica_006_Ground / DA_Flux_NorthAmerica_006_Velocity / DA_Flux_NorthAmerica_006_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_007 | Water/FluidFlux/NorthAmerica | (-147013, 255413, 4613) | 204800 x 204800 x 2500 | 115499 | 2738 | DA_Flux_NorthAmerica_007_Ground / DA_Flux_NorthAmerica_007_Velocity / DA_Flux_NorthAmerica_007_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_008 | Water/FluidFlux/NorthAmerica | (-91978, 455751, 4055) | 102400 x 204800 x 2500 | 209259 | 2180 | DA_Flux_NorthAmerica_008_Ground / DA_Flux_NorthAmerica_008_Velocity / DA_Flux_NorthAmerica_008_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_009 | Water/FluidFlux/NorthAmerica | (-159953, 655874, 3833) | 102400 x 204800 x 2500 | 95685 | 1958 | DA_Flux_NorthAmerica_009_Ground / DA_Flux_NorthAmerica_009_Velocity / DA_Flux_NorthAmerica_009_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_010 | Water/FluidFlux/NorthAmerica | (19193, -360707, 12242) | 204800 x 102400 x 5000 | 56340 | 8492 | DA_Flux_NorthAmerica_010_Ground / DA_Flux_NorthAmerica_010_Velocity / DA_Flux_NorthAmerica_010_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_011 | Water/FluidFlux/NorthAmerica | (220240, -395712, 14281) | 204800 x 25600 x 5000 | 62401 | 10531 | DA_Flux_NorthAmerica_011_Ground / DA_Flux_NorthAmerica_011_Velocity / DA_Flux_NorthAmerica_011_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_012 | Water/FluidFlux/NorthAmerica | (415187, -442738, 17411) | 204800 x 102400 x 5000 | 59986 | 13661 | DA_Flux_NorthAmerica_012_Ground / DA_Flux_NorthAmerica_012_Velocity / DA_Flux_NorthAmerica_012_Height | H 256, V - | yes |
| DA_Flux_NorthAmerica_013 | Water/FluidFlux/NorthAmerica | (588131, -539367, 19333) | 204800 x 102400 x 5000 | 63728 | 15583 | DA_Flux_NorthAmerica_013_Ground / DA_Flux_NorthAmerica_013_Velocity / DA_Flux_NorthAmerica_013_Height | H 256, V - | yes |

### 13b. Height grids

**Decode (round 89, [evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round89-map.md)).** Each `WDWaterHeightGridAsset` stores a water surface height map, not ground height.

- **Layout.** `Heights` holds `GridWidth` x `GridHeight` unsigned 16-bit values, row-major: row 0 is at world Y = `worldmin.Y`, and the row index runs toward +Y. The column index runs toward +X from `worldmin.X`. `worldmin` is the minimum corner (cm); `WorldSize` is the extent (cm). Cell size is `WorldSize.X / GridWidth` by `WorldSize.Y / GridHeight`: 200 cm in 34 of the 40 grids, 400 cm in 2, 800 cm in 3 and 1200 cm in 1. `worldmin` plus half of `WorldSize` equals the linked simulation state's `AreaLocation` X and Y in all 40.
- **Sentinel.** 65535 means no water in the cell (dry). It is 84% to 98% of the cells, depending on the grid.
- **Height.** Every other value `v` (0 to 65534) is `z = z0 + v / 65534 x (z1 - z0)` in cm, where `z0` and `z1` are the two unnamed doubles (`_aaaajahedjfgkemenmnfj`, `_aaaajbpajedfcbkcoihjn`): the lowest and the highest water surface in that grid. The smallest wet value is 0 and the largest 65534 in all 41 grids (40 here and the gym grid), which is why the range is normalised per grid. Both doubles lie inside the vertical extent of the linked state's box (`AreaLocation.Z - AreaSize.Z` to `AreaLocation.Z`) in all 41. Heights are on the game's own height scale (below zero on Europe and Kavkazi).
- **Third unnamed field.** `_aaabflcohlopnaadhglfk` is the soft reference to the linked `PDA_FluxSimulationState_C` in all 40 (and in the gym grid).
- **Result.** Bakurani (Kavkazi) has 23 grids, -1,015.95 m to -805.93 m. Ozeti (Europe) has 17 grids, -1,063.46 m to -883.03 m. North America (Zestafona) and Russia (Saburtulo) have no grids. Images and the full table: [Bakurani](../_wiki/game-modes-and-maps/bakurani.md#water-height), [Ozeti](../_wiki/game-modes-and-maps/ozeti.md#water-height), and `assets/data/map-height-grids.json`. Generated by `_tools/map_height_grids.py`.

![Bakurani water surface height]({{ '/assets/img/maps/bakurani-water-height.png' | relative_url }})

![Ozeti water surface height]({{ '/assets/img/maps/ozeti-water-height.png' | relative_url }})

<!-- height-grids:begin -->
| Grid asset | Map | Grid (W x H) | Cell (m) | Origin X, Y (m) | Size X x Y (m) | Water surface min to max (m) | Wet cells |
|---|---|---|---|---|---|---|---|
| WHG_PDA_Flux_Bakurani_River_001 | Bakurani | 512 x 512 | 2 | -6,849, -17,114 | 1,024 x 1,024 | -879.7 to -811.4 | 5,488 (2.1%) |
| WHG_PDA_Flux_Bakurani_River_East_000 | Bakurani | 512 x 512 | 2 | -1,042, -9,837 | 1,024 x 1,024 | -914.9 to -895.0 | 4,277 (1.6%) |
| WHG_PDA_Flux_Bakurani_River_East_001 | Bakurani | 512 x 512 | 2 | -2,030, -9,594 | 1,024 x 1,024 | -919.0 to -912.2 | 4,972 (1.9%) |
| WHG_PDA_Flux_Bakurani_River_East_002 | Bakurani | 512 x 512 | 2 | -3,031, -9,588 | 1,024 x 1,024 | -931.0 to -918.7 | 4,394 (1.7%) |
| WHG_PDA_Flux_Bakurani_River_East_003 | Bakurani | 512 x 512 | 2 | -3,992, -9,786 | 1,024 x 1,024 | -939.5 to -930.3 | 5,397 (2.1%) |
| WHG_PDA_Flux_Bakurani_River_East_004 | Bakurani | 512 x 512 | 2 | -4,951, -9,921 | 1,024 x 1,024 | -948.1 to -938.5 | 7,842 (3.0%) |
| WHG_PDA_Flux_Bakurani_River_East_005 | Bakurani | 512 x 512 | 2 | -5,902, -10,458 | 1,024 x 1,024 | -956.9 to -947.6 | 5,483 (2.1%) |
| WHG_PDA_Flux_Bakurani_River_East_006 | Bakurani | 512 x 512 | 2 | -6,861, -10,458 | 1,024 x 1,024 | -965.5 to -956.1 | 5,514 (2.1%) |
| WHG_PDA_Flux_Bakurani_River_East_007 | Bakurani | 512 x 512 | 2 | -7,840, -10,458 | 1,024 x 1,024 | -971.7 to -964.4 | 7,267 (2.8%) |
| WHG_PDA_Flux_Bakurani_River_East_008 | Bakurani | 512 x 512 | 2 | -8,833, -10,458 | 1,024 x 1,024 | -976.2 to -971.1 | 5,126 (2.0%) |
| WHG_PDA_Flux_Bakurani_River_RedSpawn_000 | Bakurani | 256 x 512 | 2 | -6,593, -16,178 | 512 x 1,024 | -886.0 to -864.5 | 7,806 (6.0%) |
| WHG_PDA_Flux_Bakurani_River_West_000 | Bakurani | 512 x 512 | 2 | -10,320, -10,592 | 1,024 x 1,024 | -992.1 to -983.5 | 6,894 (2.6%) |
| WHG_PDA_Flux_Bakurani_River_West_001 | Bakurani | 512 x 512 | 2 | -11,310, -10,026 | 1,024 x 1,024 | -993.3 to -990.3 | 9,086 (3.5%) |
| WHG_PDA_Flux_Bakurani_River_West_002 | Bakurani | 512 x 512 | 2 | -12,284, -9,795 | 1,024 x 1,024 | -998.5 to -987.2 | 9,385 (3.6%) |
| WHG_PDA_Flux_Bakurani_River_West_003 | Bakurani | 512 x 256 | 4 | -14,303, -9,356 | 2,048 x 1,024 | -1,009.9 to -999.7 | 5,155 (3.9%) |
| WHG_PDA_Flux_Bakurani_River_West_005 | Bakurani | 512 x 512 | 2 | -15,203, -8,824 | 1,024 x 1,024 | -1,015.7 to -1,004.5 | 5,693 (2.2%) |
| WHG_PDA_Flux_Bakurani_River_West_006 | Bakurani | 512 x 512 | 2 | -15,909, -8,747 | 1,024 x 1,024 | -1,016.0 to -1,010.3 | 18,277 (7.0%) |
| WHG_PDA_Flux_RedSpawn_001 | Bakurani | 512 x 512 | 2 | -7,558, -15,240 | 1,024 x 1,024 | -923.0 to -805.9 | 12,832 (4.9%) |
| WHG_PDA_Flux_RedSpawn_002 | Bakurani | 256 x 512 | 2 | -7,945, -14,463 | 512 x 1,024 | -934.7 to -895.1 | 5,852 (4.5%) |
| WHG_PDA_Flux_RedSpawn_003 | Bakurani | 512 x 512 | 2 | -8,648, -13,529 | 1,024 x 1,024 | -959.4 to -914.6 | 8,200 (3.1%) |
| WHG_PDA_Flux_River_CZ_000 | Bakurani | 128 x 512 | 2 | -8,568, -12,592 | 256 x 1,024 | -962.1 to -938.0 | 8,900 (13.6%) |
| WHG_PDA_Flux_River_CZ_001 | Bakurani | 256 x 512 | 2 | -8,980, -11,869 | 512 x 1,024 | -990.4 to -949.5 | 9,971 (7.6%) |
| WHG_PDA_Flux_River_CZ_002 | Bakurani | 512 x 512 | 2 | -9,454, -10,974 | 1,024 x 1,024 | -994.0 to -954.2 | 6,633 (2.5%) |
| WHG_PDA_Europe_0000 | Ozeti | 512 x 128 | 2 | -6,416, -5,976 | 1,024 x 256 | -971.7 to -946.2 | 9,518 (14.5%) |
| WHG_PDA_Europe_0001 | Ozeti | 512 x 128 | 2 | -7,368, -5,946 | 1,024 x 256 | -977.6 to -954.0 | 5,893 (9.0%) |
| WHG_PDA_Europe_0002 | Ozeti | 512 x 128 | 2 | -8,360, -6,010 | 1,024 x 256 | -1,002.3 to -975.9 | 10,236 (15.6%) |
| WHG_PDA_Europe_0003 | Ozeti | 512 x 128 | 2 | -9,320, -6,129 | 1,024 x 256 | -1,002.3 to -985.2 | 6,140 (9.4%) |
| WHG_PDA_Europe_0004 | Ozeti | 512 x 256 | 2 | -5,460, -5,977 | 1,024 x 512 | -964.5 to -935.5 | 13,383 (10.2%) |
| WHG_PDA_Europe_0005 | Ozeti | 512 x 256 | 2 | -4,658, -5,541 | 1,024 x 512 | -952.0 to -927.1 | 12,875 (9.8%) |
| WHG_PDA_Europe_0006 | Ozeti | 512 x 256 | 2 | -3,691, -5,541 | 1,024 x 512 | -942.5 to -916.9 | 13,017 (9.9%) |
| WHG_PDA_Europe_0009 | Ozeti | 256 x 512 | 8 | -8,095, -12,288 | 2,048 x 4,096 | -983.3 to -927.9 | 5,848 (4.5%) |
| WHG_PDA_Europe_0010 | Ozeti | 512 x 512 | 2 | -9,003, -8,700 | 1,024 x 1,024 | -969.2 to -945.3 | 13,105 (5.0%) |
| WHG_PDA_Europe_0011 | Ozeti | 256 x 512 | 2 | -8,996, -7,733 | 512 x 1,024 | -980.5 to -961.0 | 13,577 (10.4%) |
| WHG_PDA_Europe_0012 | Ozeti | 512 x 512 | 2 | -9,849, -6,766 | 1,024 x 1,024 | -998.5 to -972.0 | 20,123 (7.7%) |
| WHG_PDA_Europe_0014 | Ozeti | 512 x 256 | 8 | -13,790, -6,116 | 4,096 x 2,048 | -1,032.2 to -993.6 | 6,349 (4.8%) |
| WHG_PDA_Europe_007 | Ozeti | 256 x 256 | 2 | -2,932, -5,964 | 512 x 512 | -937.5 to -911.9 | 8,551 (13.1%) |
| WHG_PDA_Europe_008 | Ozeti | 512 x 256 | 2 | -2,628, -6,384 | 1,024 x 512 | -925.7 to -899.3 | 11,905 (9.1%) |
| WHG_PDA_Europe_013 | Ozeti | 512 x 256 | 4 | -1,924, -7,088 | 2,048 x 1,024 | -928.8 to -883.0 | 5,747 (4.4%) |
| WHG_PDA_Europe_015 | Ozeti | 512 x 256 | 8 | -15,660, -4,197 | 4,096 x 2,048 | -1,063.5 to -1,017.8 | 6,843 (5.2%) |
| WHG_PDA_Europe_016 | Ozeti | 256 x 256 | 12 | -9,468, -15,189 | 3,072 x 3,072 | -960.4 to -919.9 | 5,054 (7.7%) |
<!-- height-grids:end -->

### 13c. Surface preset

| Asset | Clarity | Scattering | Absorption | Overlay |
|---|---|---|---|---|
| CP_River_Kavkazi | 0.66 | BCECFF | FFFFFF | 68BCBCBC |

---

## 14. Destruction buildings (`BHDestructionBuildingDefinitionDataAsset` x7, `BHDestructionBuildingDecoratorDefinitionDataAsset` x7)

Garages only in this folder. Each building definition lists `RequiredMeshes` (with material and physical-material overrides), `ChunkData` (transform per destruction chunk), and `ChunkIDLookupMap` (chunk ID to index). Each definition has a `_Decorator` companion. Closed garages carry no decorator actors. Openable garages carry two door actors, `BP_Interactable_GarageDoor_01a_Left_C` and `_Right_C`, bound to chunks through `OwningChunkIDs`.

### 14a. Building definitions

| Asset | Required meshes | Chunks | Decorator |
|---|---|---|---|
| DA_Garage_Closed_01a | SM_Garage_Intact_FullMesh_01a, SM_Garage_Door_Locked_01a | 2 | DA_Garage_Closed_01a_Decorator |
| DA_Garage_Closed_02a | SM_Garage_Intact_FullMesh_02a, SM_Garage_Door_Locked_01a | 2 | DA_Garage_Closed_02a_Decorator |
| DA_Garage_Closed_03a | SM_Garage_Intact_FullMesh_03a, SM_Garage_Door_Locked_01a | 2 | DA_Garage_Closed_03a_Decorator |
| DA_Garage_Closed_03b | SM_Garage_Intact_FullMesh_03a, SM_Garage_Door_Locked_01b | 2 | DA_Garage_Closed_03b_Decorator |
| DA_Garage_Openable_01a | SM_Garage_Intact_FullMesh_01a | 1 | DA_Garage_Openable_01a_Decorator |
| DA_Garage_Openable_02a | SM_Garage_Intact_FullMesh_02a | 1 | DA_Garage_Openable_02a_Decorator |
| DA_Garage_Openable_03a | SM_Garage_Intact_FullMesh_03a | 1 | DA_Garage_Openable_03a_Decorator |

### 14b. Decorators

| Asset | Required actor classes | Decorator entries |
|---|---|---|
| DA_Garage_Closed_01a_Decorator | - | 0 |
| DA_Garage_Closed_02a_Decorator | - | 0 |
| DA_Garage_Closed_03a_Decorator | - | 0 |
| DA_Garage_Closed_03b_Decorator | - | 0 |
| DA_Garage_Openable_01a_Decorator | BP_Interactable_GarageDoor_01a_Left_C, BP_Interactable_GarageDoor_01a_Right_C | 2 |
| DA_Garage_Openable_02a_Decorator | BP_Interactable_GarageDoor_01a_Left_C, BP_Interactable_GarageDoor_01a_Right_C | 2 |
| DA_Garage_Openable_03a_Decorator | BP_Interactable_GarageDoor_01a_Left_C, BP_Interactable_GarageDoor_01a_Right_C | 2 |

---

## 15. Season 02 additions

Files added in the 2026-10-15 update. The catalogue tables in sections 3 to 11 still list only the assets from the earlier export; the catalogue columns for the assets below are not filled in yet.

### 15a. Added MicroBiome, layer, cluster, scatter, spline and prop assets (46)

| Asset | Type | Folder |
|---|---|---|
| `DA_VehicleProp_Ambulance_01a` | `PDA_VehicleProp_C` | `Blueprints/VehiclePropTooling` |
| `MBL_Farm_FIeld_Grass_Tall_Transition` | `PDA_MBLayer_C` | `Foliage/Biomes/Farm/Layers` |
| `MBL_Farm_Field_Brambles_Transition` | `PDA_MBLayer_C` | `Foliage/Biomes/Farm/Layers` |
| `MB_Farm_Field_Edge` | `PDA_MicroBiome_C` | `Foliage/Biomes/Farm/MicroBiomes` |
| `MB_Woodland_TreeLine_Bushes` | `PDA_MicroBiome_C` | `Foliage/Biomes/Woodland/MicroBiomes` |
| `MB_Woodland_TreeLine_Saplings` | `PDA_MicroBiome_C` | `Foliage/Biomes/Woodland/MicroBiomes` |
| `MBC_Bush_Bramble_Patch_3m_01a` | `PDA_MBCluster_C` | `Foliage/Bushes/Bramble/DataAssets/Clusters` |
| `MBS_Bush_Bramble_Strands` | `PDA_MBScatter_C` | `Foliage/Bushes/Bramble/DataAssets/Scatters` |
| `MBC_Grass_Field_Tall_Transition` | `PDA_MBCluster_C` | `Foliage/Grass/Field/DataAssets/Clusters` |
| `MBC_Tree_Ash_Sapling_01a` | `PDA_MBCluster_C` | `Foliage/Trees/Ash/DataAssets/Clusters` |
| `MBC_Tree_Oak_Field_02a` | `PDA_MBCluster_C` | `Foliage/Trees/Oak/DataAssets/Clusters` |
| `MBC_Pine_04m` | `PDA_MBCluster_C` | `Foliage/Trees/Pine/DataAssets/Clusters` |
| `DA_LightSettings_AfternoonOvercastRain` | `PDA_LightSettings_C` | `Lighting/DataAssets/Presets` |
| `DA_Cluster_Weeds_02` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters` |
| `DA_Cluster_Weeds_Spline` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters` |
| `DA_FencePost_GasPipe_400_01` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_FencePost_StoneRetainingWall_01` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Fence_Chainlink_Post_01` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Fence_Metal_Residential_Pillar_03` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Fence_Metal_Residential_Pillar_04` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Fence_Metal_Residential_Pillar_05` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Fence_Tarp_01` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Pillar_ChurchExt_01b` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Pillar_ChurchExt_02` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_Wall_Plaster_Residential_Pillar_01` | `PDA_ClusterPCG_C` | `PCG/Kavkazi/DataAssets/Clusters/Fence_Posts` |
| `DA_ConcreteBarrier_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Ditch_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_ChainLink_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Concrete_Large_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_CorrugatedMetal_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_HescoSmall_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_HescoTall_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Large_BoxHedge_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Low_Concrete_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Med_BoxHedge_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Metal_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Metal_Residential_03` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Metal_Residential_04` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_Metal_Residential_05` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_StoneRetainingWall_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Fence_TallWoodWall_Damaged_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Wall_ChurchExt_02` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `DA_Wall_Plaster_Residential_01` | `PDA_SplinePCG_C` | `PCG/Kavkazi/DataAssets/Splines/Wall` |
| `MBC_Pine_06mFiller` | `PDA_MBCluster_C` | `PCG/MicroBiomes/Pine/Clusters` |
| `MBL_Pine_04m_Edge` | `PDA_MBLayer_C` | `PCG/MicroBiomes/Pine/Layers` |
| `MB_Pine_Spline_Dense_02` | `PDA_MicroBiome_C` | `PCG/MicroBiomes/Pine` |

### 15b. Added families (10)

These four types are new to this doc. Their fields are not decoded here yet.

| Asset | Type | Folder |
|---|---|---|
| `WD_HeavyRain` | `WDRainAppearance` | `Lighting/DataAssets/Presets/Weather` |
| `AdditionalGroundMeshes` | `DA_GroundProxies_C` | `PCG/GroundDetail` |
| `GD_AsphaltPatches` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `GD_Ivy` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `GD_Leaves` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `GD_NettlesEdge` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `GD_Paper` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `GD_PotHoles` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `GD_RubbleEdges` | `DA_GroundDetail_C` | `PCG/GroundDetail/GroundDetailData` |
| `DA_RVTD_Forest_001` | `PDA_RVTD_C` | `PCG/RVTD/DataAssets` |

---

## 16. Still not pulled / limitations

- **Fluid Flux `Iteration`** (23,813 to 1,261,732 across states) has no label in the export. Its meaning (bake frame, simulation step, or version counter) is unknown.
- **`AttenuationDistance`** (1000 on all 40 MicroBiomes that set it) and the other distance-like fields on MicroBiomes are not confirmed as cm cull or fade distances.
- **Height grid arrays** (`WDWaterHeightGridAsset`) are decoded in section 13b (round 89): the unnamed fields are the lowest and highest water surface and the linked state. Still open: which runtime code reads the grids (the decode was done from the data, not from native code), and what the 65535 sentinel is called in the engine.
  - **SDK (2026-10-16):** `UWDWaterHeightGridAsset` is a `UDataAsset` with 8 fields:
    - `worldmin` (`FVector2D`, 0x30) — origin
    - `WorldSize` (`FVector2D`, 0x40) — world size (cm, confirmed)
    - `GridWidth` (`int32`, 0x50) — grid X dim
    - `GridHeight` (`int32`, 0x54) — grid Y dim
    - `_aaaajahedjfgkemenmnfj` (`double`, 0x58) — unresolved (Dumper-7)
    - `_aaaajbpajedfcbkcoihjn` (`double`, 0x60) — unresolved
    - `_aaabflcohlopnaadhglfk` (`FSoftObjectPath`, 0x68) — unresolved; **this is likely the "linked state" field** the doc references (points to a `PDA_FluxSimulationState_C`)
    - `Heights` (`TArray<FNone_>`, 0x88) — the binary height data
  - The two unresolved `double` fields are candidates for min/max height clip, scale factor, or sea-level offset; symbolic names remain unresolved via SDK, could be inferred by reading values across all 40 asset instances.
- **North America fluid states** (`DA_Flux_NorthAmerica_000` to `_013`, 14 assets) have no matching height grid in this dump and no `EncodeVelocityMax`. Their runtime role is unclear.
- **Missing scale defaults.** Where a cluster, scatter, or PCG asset has no `ScaleMin` (shown as `?`), the engine default applies. That default is not in the export.
- **Enum names** in `DT_VehiclePropList` are cooked as `NewEnumeratorN`. Only the index is shown.
- **Four vehicle assets are unlisted** (see section 10). Whether they are spawned another way is not in this folder.
- **Usage links are not in the export.** It does not say which landscape material samples `VC_Stratus`, `VC_GrassTint`, or the atlas, nor which mask texture the grass `ScatterMaskChannel` reads.
- **Unit assumptions.** Distances are assumed to be Unreal cm. Sun `Intensity` is assumed to be lux. Neither is stated in the export.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **`_Overkill` light presets.** Their purpose is not confirmed.
- **Sampling of raw files.** Most values come from the script's normalised output. Raw JSON was spot-checked for `MB_Pine_Treeline` and `CP_River_Kavkazi`, and the headers of several other assets.
- **Not in this folder.** The landscape material, the PCG graphs that consume these data assets, the mesh-material overrides, and the `BP_Interactable_GarageDoor_*` blueprints live elsewhere in the dump and are not covered here.

---

*Source folder: `Wardogs/Content/Environment/` (read-only). Generated by parsing all 419 JSON exports.*

## 17. Engine default assets (round 73)

Engine-side assets exported with the game. They are stock or near-stock and carry little gameplay meaning.

| Asset | What it is |
|---|---|
| `C_Sky_Cloud_Color` | `CurveLinearColor`, 6 keys per RGB channel from time -0.79 to 0.81: R 0.054 to 0.929, G 0.059 to 0.947, B 0.065 to 1.0. Cloud tint |
| `C_Sky_Horizon_Color` | `CurveLinearColor`, 6 keys per channel from -0.99 to 0.45: R 0.048 to 0.92, G 0.052 to 1.322, B 0.075 to 2.0 (values above 1 are HDR). Horizon tint |
| `C_Sky_Zenith_Color` | `CurveLinearColor`, 7 keys per channel from -0.95 to 0.47: R 0 to 0.023, G 0 to 0.049, B 0 to 0.12. Zenith tint |
| `FloatCurve_WaterBodyIsland` | Water plugin default `CurveFloat`: (0.05, 0), (0.1, 0.9), (1.0, 1.0). Island falloff shape |
| `DefaultPaperTerrainMaterial` | Paper2D default terrain material: one rule, body sprite `DummySprite`, angle 0 to 360, collision on. Unused by a 3D game |

The alpha channel of the sky curves has no keys. The engine animation-compression defaults are in [Animation](Wardogs_Animation_v2.md) section 8b.
