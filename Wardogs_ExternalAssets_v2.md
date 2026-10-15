---
title: "ExternalAssets"
parent: "Content"
---

# Wardogs — External Assets Reference (v2)
*Extracted from cooked game data ([`Content/ExternalAssets`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets), 100 JSON exports, UE 5.7 build `++Wardogs+Live-CL-509546`). Every number below was parsed from the export files by script. Where a field's meaning is inferred from its name rather than confirmed, the doc says so.*

> **Scope note:** This folder is almost entirely **building destruction data** (`Flix/Blueprints/**`), plus two damage-tag whitelists and one VFX mapping. It holds no weapons, economy or progression data. All 100 files parsed without error.

---

## 1. File Inventory

| Type | Files | Role (as read) |
|---|---|---|
| `BHDestructionBuildingDefinitionDataAsset` | 48 | Destructible building: chunk layout, junctions, required meshes, Niagara refs |
| `BHDestructionBuildingDecoratorDefinitionDataAsset` | 49 | Decorator layer for a building: spawned actors, cosmetic props, authoritative props, preload lists |
| `BHDestructionDecoratorMeshDamageTagsDataAsset` | 2 | Per-mesh damage-tag whitelists (ballistic and explosive) |
| `BHDestructionBuildingVFXDataAsset` | 1 | [`D_BuildingVFX`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/VFX/Environmental/Destruction/SharedEmitterSystem/DataChannels/D_BuildingVFX.json): chunk classification to Niagara data channel and Houdini point caches |

Folders: [`Flix/Blueprints/Bakurani`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani) (23 buildings), [`Flix/Blueprints/Madrid`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid) (10), [`Flix/Blueprints/Industrial`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial) (14), [`Flix/Blueprints/Commercial/Office`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Commercial/Office) (1), [`Flix/DataAssets`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets/Flix/DataAssets), and `Flix/VFX/.../DataChannels`.

---

## 2. Building Definitions (`BHDestructionBuildingDefinitionDataAsset`, 48 assets)

**Totals across all 48:** 13,087 chunks, 2,364 required-mesh entries, 6,875 junctions, 330 chunks with a prefab reference.

### 2a. Top-level fields

| Property | Shape | Meaning (confidence) |
|---|---|---|
| `SaveID` | GUID string | Building identifier. Madrid copies get a different SaveID from their Bakurani source (checked on apartment and house pairs). Purpose not confirmed. |
| `RequiredMeshes` | list of `{StaticMesh, MaterialOverrideArray, PhysicalMaterialOverride, MeshCenter, RefCount, StringISMOverrides}` | Static meshes the building needs. `RefCount` is how many chunks use it. `MeshCenter` is the pivot offset (high confidence, from field names). |
| `ChunkData` | list of chunk records | One record per destructible piece. Fields in 2b. |
| `ChunkIDLookupMap` | list of `{Key: ChunkId, Value: index}` | Same length as `ChunkData`. Maps chunk GUID to array index (confirmed by inspection on [`DA_Warehouse_Small_Hut_02a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial/Warehouse_Small_Hut_02a/DA_Warehouse_Small_Hut_02a.json)). |
| `JunctionData` | list of `{JunctionLocation, JunctionEdgeData[]}` | Points where several chunk edges meet. Each edge has `ChunkIndex` and `EdgePieceData.EdgeOffset`. Absent on every industrial building and on the Factory Awnings. |
| `RequiredNiagaraAssets` | list of `{NiagaraAsset}` | Niagara systems referenced by index, e.g. `NS_FullWallBreak_1`, `NS_BalconyBreak`. 0 to 2 per building. |

### 2b. Chunk record fields

| Field | Meaning (confidence) |
|---|---|
| `ChunkId` | GUID string. The key used by `ChunkIDLookupMap` and by decorator `OwningChunkIDs`. |
| `Transform` | Rotation, Translation, Scale3D. Units are not stated in the dump (probably cm, the UE default). |
| `AssetRefIndex` | Index into `RequiredMeshes`, -1 when none (inferred from name). |
| `NiagaraAssetRefIndex` | Index into `RequiredNiagaraAssets`, -1 when none (inferred from name). |
| `StructuralSupports.VitalConnections` / `ProportionalConnections` | Chunk-to-chunk support links as index lists. "Vital" probably means the chunk falls if the link breaks; "proportional" probably means load is shared. Both inferred from names, not confirmed. |
| `EdgePieces` | Edge geometry used when the chunk breaks. Counted per building in section 2c. |
| `NiagaraBespokeEffectFormat` | Enum: `NoBespokeFormat`, `Wall2m`, `Wall4m`, `Wall6m`. Picks a bespoke debris effect by wall length. On [`DA_ApartmentBuilding_01_a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_01_a.json), `Wall4m` (481) is the most common non-default format. |
| `NiagaraDataChannelParameters` | Debris tags: `DebrisMeshType` (Wall, Ceiling, Roof, Balcony, Generic), `DebrisShape` (e.g. `Wall_4m`, `Corner_J_2m_x_2m`, `Roof_Slope_4m_x_4m`, or `None`), `DebrisMaterial` (Concrete, Wood, Metal). |
| `ChunkTraits` | Present on every chunk, empty on every sampled chunk. |
| `ChunkCustomPrimitiveData` | Four floats (e.g. `0.4, 0.12, 0.085, 1.0`). Meaning not stated, probably shader parameters. Not decoded. |
| `Prefab` / `PrefabHash` | Optional prefab class reference (e.g. `CP_ModKit04_Roof_Panel_Short_2m_A`). Mostly on apartments (47, 23, 36 chunks in the three Bakurani apartment blocks), Office (15), and houses and bungalows (2 to 17 each). |
| `AudioPhysMaterialArray` | Audio physical materials. Empty on sampled chunks. |
| `Properties` | Integer flag field. Non-zero on 882 of 1,550 chunks in [`DA_ApartmentBuilding_01_a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_01_a.json). Meaning not confirmed. |

### 2c. Per-building table

Columns: mesh entries (`RequiredMeshes` count), unique `StaticMesh` names, chunks, junctions, Niagara refs, chunks with a prefab, total edge pieces, vital and proportional connections (summed over chunks), and `RefCount` summed over all required meshes.

| Building DA | Folder | Mesh entries | Unique meshes | Chunks | Junctions | Niagara refs | Prefab chunks | Edge pieces | Vital conn. | Proportional conn. | Sum RefCount |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DA_ApartmentBuilding_01_a | Bakurani/Apartments | 108 | 92 | 1550 | 837 | 2 | 47 | 1463 | 683 | 474 | 3013 |
| DA_ApartmentBuilding_01_b | Bakurani/Apartments | 112 | 94 | 1979 | 1115 | 2 | 23 | 1962 | 869 | 620 | 3941 |
| DA_ApartmentBuilding_01c | Bakurani/Apartments | 106 | 93 | 1079 | 606 | 2 | 36 | 1034 | 586 | 368 | 2113 |
| DA_MarketBuilding_02 | Bakurani/Commercial/MarketBuilding_02 | 22 | 22 | 188 | 102 | 1 | 0 | 129 | 0 | 2 | 317 |
| D_MarketBuilding_04a_chunk | Bakurani/Commercial/MarketBuilding_04 | 16 | 16 | 62 | 40 | 1 | 0 | 50 | 0 | 8 | 112 |
| D_MarketBuilding_05a_chunk | Bakurani/Commercial/MarketBuilding_05 | 16 | 16 | 52 | 38 | 1 | 0 | 47 | 0 | 2 | 99 |
| D_MarketBuilding_06 | Bakurani/Commercial/MarketBuilding_06 | 27 | 26 | 129 | 56 | 1 | 0 | 81 | 0 | 26 | 210 |
| D_Market_Building_01a | Bakurani/Commercial/Market_Building_01 | 73 | 40 | 654 | 425 | 1 | 0 | 656 | 36 | 249 | 1310 |
| D_MarketBuilding_03a | Bakurani/Commercial/Market_Building_03 | 59 | 37 | 414 | 296 | 1 | 0 | 470 | 38 | 243 | 884 |
| D_Shop_01 | Bakurani/Commercial/Shop_01 | 30 | 30 | 58 | 53 | 0 | 0 | 69 | 11 | 15 | 127 |
| D_Shop_02 | Bakurani/Commercial/Shop_02 | 24 | 24 | 37 | 28 | 0 | 0 | 32 | 0 | 8 | 69 |
| D_Shop_03 | Bakurani/Commercial/Shop_03 | 30 | 29 | 93 | 71 | 0 | 0 | 86 | 14 | 11 | 179 |
| D_Residential_Bungalow_01 | Bakurani/Residential | 70 | 61 | 78 | 53 | 1 | 8 | 80 | 49 | 49 | 158 |
| D_Residential_Bungalow_02 | Bakurani/Residential | 65 | 62 | 106 | 66 | 1 | 17 | 100 | 28 | 77 | 206 |
| D_Residential_Bungalow_03 | Bakurani/Residential | 48 | 42 | 70 | 38 | 1 | 9 | 56 | 21 | 66 | 126 |
| D_Residential_House_01 | Bakurani/Residential | 94 | 79 | 159 | 87 | 1 | 13 | 143 | 89 | 136 | 302 |
| D_Residential_House_03 | Bakurani/Residential | 76 | 73 | 159 | 98 | 1 | 6 | 158 | 69 | 85 | 317 |
| D_Residential_House_04 | Bakurani/Residential | 89 | 80 | 153 | 85 | 1 | 17 | 136 | 72 | 100 | 289 |
| D_Residential_House_05 | Bakurani/Residential | 94 | 82 | 163 | 96 | 1 | 2 | 162 | 135 | 95 | 325 |
| D_Residential_House_Abandoned_01 | Bakurani/Residential | 86 | 69 | 130 | 107 | 2 | 0 | 195 | 84 | 49 | 325 |
| D_SupplyBuilding_01 | Bakurani/Residential | 19 | 18 | 58 | 42 | 0 | 0 | 50 | 0 | 24 | 108 |
| D_SupplyBuilding_02 | Bakurani/Residential | 20 | 19 | 34 | 55 | 0 | 0 | 67 | 0 | 20 | 101 |
| D_SwimPoolBuilding_01 | Bakurani/Residential/SwimmingPool | 39 | 35 | 251 | 182 | 0 | 0 | 271 | 3 | 107 | 522 |
| DA_Office_01a | Commercial/Office | 98 | 74 | 487 | 356 | 1 | 15 | 649 | 267 | 147 | 1136 |
| DA_Factory_Awning_01a | Industrial/Factory_Awning_01a | 5 | 5 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| DA_Factory_Awning_02a | Industrial/Factory_Awning_02a | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| DA_Warehouse_02a | Industrial/Warehouse_02a | 13 | 13 | 84 | 0 | 0 | 0 | 0 | 16 | 64 | 84 |
| DA_Warehouse_03a | Industrial/Warehouse_03a | 22 | 22 | 237 | 0 | 0 | 0 | 0 | 46 | 278 | 237 |
| DA_Warehouse_03b | Industrial/Warehouse_03a | 21 | 21 | 235 | 0 | 0 | 0 | 0 | 46 | 278 | 235 |
| DA_Warehouse_04a | Industrial/Warehouse_04a | 15 | 15 | 168 | 0 | 0 | 0 | 0 | 0 | 167 | 168 |
| DA_Warehouse_Garage_01a | Industrial/Warehouse_Garage_01a | 5 | 5 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| DA_Warehouse_Scrapyard_01a | Industrial/Warehouse_Scrapyard_01a | 6 | 6 | 48 | 0 | 0 | 0 | 0 | 0 | 32 | 48 |
| DA_Warehouse_Small_01a | Industrial/Warehouse_Small_01a | 12 | 12 | 68 | 0 | 0 | 0 | 0 | 0 | 36 | 68 |
| DA_Warehouse_Small_02a | Industrial/Warehouse_Small_02a | 14 | 14 | 30 | 0 | 0 | 0 | 0 | 0 | 18 | 30 |
| DA_Warehouse_Small_03a | Industrial/Warehouse_Small_03a | 8 | 8 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| DA_Warehouse_Small_03b | Industrial/Warehouse_Small_03b | 7 | 7 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| DA_Warehouse_Small_Hut_01a | Industrial/Warehouse_Small_Hut_01a | 10 | 10 | 18 | 0 | 0 | 0 | 0 | 0 | 6 | 18 |
| DA_Warehouse_Small_Hut_02a | Industrial/Warehouse_Small_Hut_02a | 7 | 7 | 11 | 0 | 0 | 0 | 0 | 0 | 2 | 11 |
| DA_Ozeti_ApartmentBuilding_01_a | Madrid/Apartments | 108 | 92 | 1550 | 837 | 2 | 47 | 1463 | 683 | 474 | 3013 |
| DA_Ozeti_ApartmentBuilding_01c | Madrid/Apartments | 106 | 93 | 1079 | 606 | 2 | 36 | 1034 | 586 | 367 | 2113 |
| D_FootballStadium_Building_01a | Madrid/Commercial/FootballStadium | 57 | 48 | 463 | 0 | 0 | 0 | 0 | 0 | 0 | 463 |
| D_Residential_Bungalow_Madrid_01 | Madrid/Residential | 70 | 61 | 78 | 53 | 1 | 2 | 80 | 49 | 49 | 158 |
| D_Residential_Bungalow_Madrid_02 | Madrid/Residential | 65 | 62 | 106 | 66 | 1 | 17 | 100 | 28 | 77 | 206 |
| D_Residential_Bungalow_Madrid_03 | Madrid/Residential | 48 | 42 | 70 | 38 | 1 | 9 | 56 | 18 | 67 | 126 |
| D_Residential_House_Madrid_01 | Madrid/Residential | 95 | 81 | 158 | 90 | 1 | 13 | 148 | 128 | 139 | 306 |
| D_Residential_House_Madrid_03 | Madrid/Residential | 68 | 62 | 149 | 70 | 1 | 1 | 107 | 67 | 76 | 256 |
| D_Residential_House_Madrid_04 | Madrid/Residential | 90 | 81 | 153 | 85 | 1 | 10 | 137 | 97 | 102 | 290 |
| D_Residential_House_Madrid_05 | Madrid/Residential | 90 | 83 | 163 | 98 | 1 | 2 | 168 | 172 | 74 | 331 |

**Reading the table:**
- [`DA_ApartmentBuilding_01_b`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_01_b.json) is the largest building: 1,979 chunks, 1,115 junctions.
- Industrial buildings have no junctions and no edge pieces, but many chunks. They break into flat pieces with no junction layer.
- The Madrid apartment and bungalow definitions match their Bakurani sources chunk for chunk (section 7).

---

## 3. Decorator Definitions (`BHDestructionBuildingDecoratorDefinitionDataAsset`, 49 assets)

**Totals across all 49:** 25,927 cosmetic decorator entries, 5,902 authoritative decorator entries, 1,427 actor decorator entries, 209 actor-class references.

### 3a. Field meanings

| Property | Shape | Meaning (confidence) |
|---|---|---|
| `SaveID` | GUID string | One per decorator asset. |
| `RequiredActorClasses` | list of `{SoftActorClass: {AssetPathName}, RefCount}` | Soft references to actor classes the decorator spawns, to be preloaded. |
| `ActorDecoratorData` | list | Spawned actor placements. Fields: `Transform`, `ActorClassRefIndex` (index into `RequiredActorClasses`), `OwningChunkIDs`, `StringTemplateOverrides`, `Prefab`. Likely doors, windows and decals (inferred from the classes in 3c). |
| `CosmeticDecoratorData` | list | Visual-only pieces. Fields: `OwningChunkIDs` (building chunks it attaches to), `Transform`, `AssetRefIndex`, `ActorClassRefIndex`, `NiagaraAssetRefIndex`, `SoundEmitterAssetRefIndex`, `DecoratorNiagaraDataChannelParameters`, plus an unnamed GUID-keyed list. The largest collection in the set. |
| `AuthoritativeDecoratorData` | list | Same shape as cosmetic data. The name suggests server-authoritative pieces (doors, smashable windows). Not confirmed by code. |
| `RequiredCosmeticMeshes` / `RequiredAuthoritativeMeshes` | list of `{StaticMesh, ...}` | Preload lists, same shape as building `RequiredMeshes`. |
| `RequiredNiagaraAssets` | list | Niagara systems, on only a few decorators. |

Decorator-to-building linkage is by **name pattern** (`DA_X` pairs with `DA_Decorator_X` or `D_Decorator_X`) and by the `OwningChunkIDs` GUIDs. The dump has no explicit building reference on the decorator.

### 3b. Per-decorator table

Columns: actor-class references, `ActorDecoratorData` count, `CosmeticDecoratorData` count, `AuthoritativeDecoratorData` count, preload-list lengths for cosmetic and authoritative meshes, and Niagara refs.

| Decorator DA | Folder | Actor class refs | ActorDecoratorData | CosmeticDecoratorData | AuthoritativeDecoratorData | Req. cosmetic meshes | Req. auth. meshes | Req. Niagara |
|---|---|---|---|---|---|---|---|---|
| DA_ApartmentBuilding_Decorator_01a | Bakurani/Apartments | 10 | 117 | 3573 | 880 | 166 | 86 | 0 |
| DA_ApartmentBuilding_Decorator_01b | Bakurani/Apartments | 12 | 135 | 4350 | 1084 | 165 | 84 | 0 |
| DA_ApartmentBuilding_Decorator_01c | Bakurani/Apartments | 11 | 103 | 2975 | 600 | 167 | 69 | 0 |
| DA_Decorator_MarketBuilding_02 | Bakurani/Commercial/MarketBuilding_02 | 1 | 17 | 12 | 96 | 5 | 36 | 0 |
| D_MarketBuilding_04a_deco | Bakurani/Commercial/MarketBuilding_04 | 1 | 4 | 2 | 32 | 2 | 17 | 0 |
| D_MarketBuilding_05a_deco | Bakurani/Commercial/MarketBuilding_05 | 1 | 8 | 9 | 19 | 6 | 11 | 0 |
| D_Decorator_MarketBuilding_06 | Bakurani/Commercial/MarketBuilding_06 | 1 | 6 | 25 | 39 | 10 | 16 | 0 |
| D_Market_Building_Deco_01a | Bakurani/Commercial/Market_Building_01 | 2 | 32 | 54 | 115 | 19 | 39 | 0 |
| D_Decorator_MarketBuilding_03a | Bakurani/Commercial/Market_Building_03 | 2 | 23 | 65 | 74 | 20 | 17 | 0 |
| D_Decorator_Shop_01 | Bakurani/Commercial/Shop_01 | 3 | 16 | 144 | 104 | 43 | 41 | 0 |
| D_Decorator_Shop_02 | Bakurani/Commercial/Shop_02 | 4 | 8 | 92 | 25 | 30 | 11 | 0 |
| D_Decorator_Shop_03 | Bakurani/Commercial/Shop_03 | 4 | 15 | 98 | 50 | 26 | 20 | 0 |
| D_Decorator_D_Residential_House_01 | Bakurani/Residential | 6 | 32 | 448 | 63 | 98 | 38 | 0 |
| D_Decorator_D_Residential_House_03 | Bakurani/Residential | 11 | 51 | 470 | 75 | 106 | 39 | 0 |
| D_Decorator_D_Residential_House_04 | Bakurani/Residential | 10 | 48 | 438 | 57 | 95 | 34 | 0 |
| D_Decorator_D_Residential_House_05 | Bakurani/Residential | 7 | 33 | 435 | 88 | 99 | 39 | 0 |
| D_Decorator_Res_Abandoned_01 | Bakurani/Residential | 5 | 23 | 450 | 47 | 104 | 29 | 0 |
| D_Decorator_Residential_Bungalow_01 | Bakurani/Residential | 5 | 19 | 210 | 42 | 95 | 31 | 3 |
| D_Decorator_Residential_Bungalow_02 | Bakurani/Residential | 4 | 22 | 288 | 45 | 85 | 31 | 0 |
| D_Decorator_Residential_Bungalow_03 | Bakurani/Residential | 7 | 18 | 202 | 31 | 70 | 25 | 0 |
| D_Decorator_SupplyBuilding_01 | Bakurani/Residential | 1 | 1 | 62 | 0 | 13 | 0 | 0 |
| D_Decorator_SupplyBuilding_01b | Bakurani/Residential | 2 | 4 | 83 | 31 | 24 | 7 | 0 |
| D_Decorator_SupplyBuilding_02 | Bakurani/Residential | 2 | 4 | 42 | 0 | 10 | 0 | 0 |
| D_Decorator_SupplyBuilding_02b | Bakurani/Residential | 2 | 4 | 57 | 19 | 20 | 8 | 0 |
| D_Decorator_SwimPoolBuilding_01 | Bakurani/Residential/SwimmingPool | 4 | 58 | 155 | 47 | 17 | 14 | 0 |
| DA_Office_Decorator_01a | Commercial/Office | 8 | 87 | 1571 | 362 | 131 | 45 | 0 |
| FA_Factory_Awning_01a_Decorator | Industrial/Factory_Awning_01a | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DA_Factory_Awning_02a_Decorator | Industrial/Factory_Awning_02a | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_02a_Decorator | Industrial/Warehouse_02a | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_03a_Decorator | Industrial/Warehouse_03a | 1 | 8 | 74 | 0 | 6 | 0 | 0 |
| DA_Warehouse_04a_Decorator | Industrial/Warehouse_04a | 3 | 29 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Garage_01a_Decorator | Industrial/Warehouse_Garage_01a | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Scrapyard_01a_Decorator | Industrial/Warehouse_Scrapyard_01a | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Small_01a_Decorator | Industrial/Warehouse_Small_01a | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Small_02a_Decorator | Industrial/Warehouse_Small_02a | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Small_03a_Decorator | Industrial/Warehouse_Small_03a | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Small_03b_Decorator | Industrial/Warehouse_Small_03b | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| DAWarehouse_Small_Hut_01a_Decorator | Industrial/Warehouse_Small_Hut_01a | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| DA_Warehouse_Small_Hut_02a_Decorator | Industrial/Warehouse_Small_Hut_02a | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| DA_Ozeti_ApartmentBuilding_Decorator_01a | Madrid/Apartments | 10 | 117 | 3617 | 869 | 175 | 87 | 0 |
| DA_Ozeti_ApartmentBuilding_Decorator_01c | Madrid/Apartments | 11 | 103 | 2995 | 606 | 176 | 69 | 0 |
| D_FootballStadium_Building_Decorator_01a | Madrid/Commercial/FootballStadium | 3 | 46 | 338 | 14 | 15 | 4 | 0 |
| D_Decorator_D_Residential_House_Madrid_01 | Madrid/Residential | 6 | 28 | 468 | 64 | 110 | 39 | 0 |
| D_Decorator_D_Residential_House_Madrid_03 | Madrid/Residential | 9 | 42 | 480 | 69 | 117 | 36 | 0 |
| D_Decorator_D_Residential_House_Madrid_04 | Madrid/Residential | 10 | 47 | 460 | 56 | 109 | 34 | 0 |
| D_Decorator_D_Residential_House_Madrid_05 | Madrid/Residential | 7 | 34 | 453 | 88 | 110 | 40 | 0 |
| D_Decorator_Residential_Bungalow_Madrid_01 | Madrid/Residential | 5 | 20 | 214 | 43 | 101 | 32 | 3 |
| D_Decorator_Residential_Bungalow_Madrid_02 | Madrid/Residential | 4 | 23 | 307 | 38 | 93 | 31 | 0 |
| D_Decorator_Residential_Bungalow_Madrid_03 | Madrid/Residential | 7 | 18 | 211 | 30 | 78 | 24 | 0 |

**Notes:**
- Four decorators hold a single property and no decoration data: [`FA_Factory_Awning_01a_Decorator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial/Factory_Awning_01a/FA_Factory_Awning_01a_Decorator.json), [`DA_Factory_Awning_02a_Decorator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial/Factory_Awning_02a/DA_Factory_Awning_02a_Decorator.json), [`DA_Warehouse_Garage_01a_Decorator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial/Warehouse_Garage_01a/DA_Warehouse_Garage_01a_Decorator.json), [`DA_Warehouse_Scrapyard_01a_Decorator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial/Warehouse_Scrapyard_01a/DA_Warehouse_Scrapyard_01a_Decorator.json). Those buildings get no decoration.
- [`DA_Warehouse_04a_Decorator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Industrial/Warehouse_04a/DA_Warehouse_04a_Decorator.json) has 29 actor decorators and no cosmetic or authoritative data.
- The Madrid apartment decorators carry about the same counts as the Bakurani ones but are not identical (cosmetic 3,617 for [`DA_Ozeti_ApartmentBuilding_Decorator_01a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Apartments/DA_Ozeti_ApartmentBuilding_Decorator_01a.json) vs 3,573 for [`DA_ApartmentBuilding_Decorator_01a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_Decorator_01a.json)).

### 3c. Actor classes used by decorators (top 25 by reference count)

| Actor class (leaf name) | Occurrences across decorators |
|---|---|
| WDGame | 43 |
| B_SmashableApartmentSingleWindow | 25 |
| B_SmashableApartmentDoubleWindow | 18 |
| B_Door | 18 |
| MI_Apartment_EdgeDirt_01b | 15 |
| BP_InteractableDoor_Apartment | 11 |
| BP_InteractableDoor_ApartmentBalcony | 11 |
| B_SmashableApartmentBalconyWindow | 9 |
| MI_Apartment_EdgeDirt_01d | 9 |
| MI_Apartment_EdgeDirt_01c | 9 |
| BP_InteractableDoor_ApartmentEntrance | 8 |
| MI_Apartment_EdgeDirt_01f | 7 |
| BP_Apartment_EdgeDirt_01a | 5 |
| BP_Apartment_StairStripeDecal_01a | 3 |
| BP_Apartment_StairStripeDecal_01b | 3 |
| BP_Debris_Decal_01a | 3 |
| BP_Apartment_StairStripeDecal_Orange_01a | 2 |
| BP_Apartment_StairStripeDecal_Orange_01b | 2 |
| MI_Apartment_EdgeDirt_01e | 2 |
| BP_Apartment_StairStripeDecal_Blue_01a | 1 |
| BP_Apartment_StairStripeDecal_Blue_01b | 1 |
| BP_WaterStain_Decal_01a | 1 |
| B_SmashableApartmentBalconyDoor | 1 |
| BP_InteractableDoor_Office | 1 |
| BP_InteractableDoor_WoodPVC | 1 |

These are soft references (`AssetPathName`). Most are doors (`BP_InteractableDoor_*`, `B_Door`), smashable window and balcony blueprints (`B_Smashable*Window`, `B_SmashableApartmentBalconyDoor`), and decals (`MI_Apartment_EdgeDirt_*`, `BP_Apartment_StairStripeDecal_*`, `BP_WaterStain_Decal_01a`). One script class, `/Script/WDGame.WDDestructionAmbienceVolume`, is used 43 times.

---

## 4. Damage-Tag Whitelists (`BHDestructionDecoratorMeshDamageTagsDataAsset`)

| Asset | Entries | Content |
|---|---|---|
| [`DA_DestructionDecoratorBallisticsTagWhitelist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/DataAssets/DA_DestructionDecoratorBallisticsTagWhitelist.json) | 68 | Each entry is `Key` (a `/Game/...` static mesh path: decorative room props such as `SM_DecorativePlate01`, and Megascans assets) and `Value` (a list of damage-tag strings). 67 entries carry 13 tags. One entry (`S_Wooden_Floor_Lamp_vi5hbjgga_high_Var2`) carries 12. |
| [`DA_DestructionDecoratorExplosiveTagWhitelist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/DataAssets/DA_DestructionDecoratorExplosiveTagWhitelist.json) | 0 | Header only, no `Properties`. Empty. |

**The 13 distinct ballistic tags** (all `Meta.Damage.Bullet.*`): `9mm`, `12g`, `30mm`, `308Win`, `338Nor`, `45ACP`, `45Colt`, `50Cal`, `545mm`, `556mm`, `762mm`, `762x51mm`, `762x54mm`. 67 of the 68 meshes carry all 13.

Meaning, inferred from the name: a mesh gets bullet decoration only if the incoming damage tag is on its list. The explosive whitelist is empty, so no mesh in this export is whitelisted for explosive damage tags.

---

## 5. Chunk-Classification VFX ([`D_BuildingVFX`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/VFX/Environmental/Destruction/SharedEmitterSystem/DataChannels/D_BuildingVFX.json), `BHDestructionBuildingVFXDataAsset`)

| Entry | Niagara data channel | Houdini point caches |
|---|---|---|
| 1 | `NDC_WallDebris` | 8 (e.g. `SM_Wall_2m_points`) |
| 2 | `NDC_RoofDebris` | 6 (e.g. `SM_Roof_Bottom_A_points`) |
| 3 | `NDC_CeilingDebris` | 0 |
| 4 | `NDC_BalconyDebris` | 2 (e.g. `Balcony_B_points`) |
| 5 | `NDC_GenericDestruction` | 0 |

`ChunkClassificationEffects` maps a chunk class to a Niagara data channel and to pre-baked Houdini point caches. The dump does not show how a chunk gets its class. The `DebrisMeshType` tag in section 2b is the likely selector, but that is not confirmed.

---

## 6. How the Pieces Combine

1. A **building definition** describes the chunks, their connections (vital and proportional), junctions and the meshes they use.
2. A **decorator definition** with the same name family attaches props to those chunks. Each cosmetic or authoritative entry lists its `OwningChunkIDs`, so it breaks with the chunks it sits on.
3. Debris look is chosen per chunk from `NiagaraDataChannelParameters` (mesh type, shape, material), and from `NiagaraBespokeEffectFormat` for wall lengths.
4. Bullet decoration on a mesh is gated by its **damage-tag whitelist**. The ballistic list covers 68 meshes. The explosive list is empty.

---

## 7. Madrid Reskins

The [`Flix/Blueprints/Madrid`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid) folder re-uses Bakurani geometry under new SaveIDs. Chunk-ID lists were compared pairwise:

| Madrid asset | Bakurani source | Same chunk IDs |
|---|---|---|
| [`DA_Ozeti_ApartmentBuilding_01_a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Apartments/DA_Ozeti_ApartmentBuilding_01_a.json) | [`DA_ApartmentBuilding_01_a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_01_a.json) | yes |
| [`DA_Ozeti_ApartmentBuilding_01c`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Apartments/DA_Ozeti_ApartmentBuilding_01c.json) | [`DA_ApartmentBuilding_01c`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_01c.json) | yes |
| [`D_Residential_Bungalow_Madrid_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_Bungalow_Madrid_01.json) | [`D_Residential_Bungalow_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_Bungalow_01.json) | yes |
| [`D_Residential_Bungalow_Madrid_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_Bungalow_Madrid_02.json) | [`D_Residential_Bungalow_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_Bungalow_02.json) | yes |
| [`D_Residential_Bungalow_Madrid_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_Bungalow_Madrid_03.json) | [`D_Residential_Bungalow_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_Bungalow_03.json) | yes |
| [`D_Residential_House_Madrid_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_House_Madrid_01.json) | [`D_Residential_House_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_House_01.json) | no (148 vs 143 edge pieces) |
| [`D_Residential_House_Madrid_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_House_Madrid_03.json) | [`D_Residential_House_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_House_03.json) | no |
| [`D_Residential_House_Madrid_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_House_Madrid_04.json) | [`D_Residential_House_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_House_04.json) | yes |
| [`D_Residential_House_Madrid_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Residential/D_Residential_House_Madrid_05.json) | [`D_Residential_House_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Residential/D_Residential_House_05.json) | yes |

So 7 of 9 pairs share chunk IDs. [`D_FootballStadium_Building_01a`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Madrid/Commercial/FootballStadium/D_FootballStadium_Building_01a.json) (Madrid, 463 chunks, no junctions) has no Bakurani source in this folder.

---

## 8. Still not pulled / Limitations

- **Unresolved property names.** Some properties appear only as GUID-style keys. On every `RequiredMeshes` entry the value is `EBHDestructionCPDInputStyle::Building`. Cosmetic decorator entries carry an unnamed list. Their meaning is not known from this export.
- **Bit and enum meanings not decoded.** The chunk `Properties` flag, `ChunkCustomPrimitiveData` (four floats) and `ChunkTraits` (empty in every sample) are reported as found, not interpreted.
- **Connection semantics inferred.** "Vital" and "proportional" support links are read from property names. Runtime behaviour is not confirmed.
- **Decorator-to-building link is by name.** Only the `OwningChunkIDs` GUIDs give a hard link, and they were spot-checked, not checked for every decorator.
- **Explosive whitelist is empty.** Whether that is intended or a cook artifact is not known.
- **One ballistic entry with 12 tags.** The mesh `S_Wooden_Floor_Lamp_vi5hbjgga_high_Var2` is missing one of the 13 tags. Which one was not checked.
- **Units.** `Transform` values are reported raw. The dump does not state units.
- **Houdini point caches not expanded.** Section 5 gives names and counts only.
- **Large files summarised, not read entry by entry.** The largest file ([`DA_ApartmentBuilding_01_b`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/ExternalAssets/Flix/Blueprints/Bakurani/Apartments/DA_ApartmentBuilding_01_b.json), about 7.5 MB) was parsed in full by script, and its chunk arrays were summarised rather than inspected individually.
