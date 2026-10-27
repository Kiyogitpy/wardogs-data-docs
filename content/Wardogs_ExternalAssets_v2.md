---
title: "ExternalAssets"
redirect_from: ["/Wardogs_ExternalAssets_v2.html", "/Wardogs_ExternalAssets_v2"]
parent: "World, Visuals & Audio"
description: "File Inventory, Building Definitions, Decorator Definitions, Damage-Tag Whitelists"
---

# Wardogs — External Assets Reference
*Extracted from cooked game data (`Content/ExternalAssets`, 147 JSON exports, UE 5.7 build `++Wardogs+Live-CL-516586`). Every number below was parsed from the export files by script. Where a field's meaning is inferred from its name rather than confirmed, the doc says so.*

> **Scope note:** This folder is almost entirely **building destruction data** (`Flix/Blueprints/**`), plus two damage-tag whitelists and one VFX mapping. It holds no weapons, economy or progression data. All 147 files parsed without error.

---

## Season 02 update (2026-10-15)

- **Added: 47 files** (26 building definitions and 21 decorator definitions). New in Bakurani: six residential houses and one swimming-pool building, with their decorators. New in Commercial: 14 Highstreet buildings with 13 decorators, 4 Hospital buildings with 4 decorators, and one WorkShop building with one decorator.
- **Removed: none.**
- **Building definitions: 48 → 74.** Chunks 13,087 → 22,137; required-mesh entries 2,364 → 3,943; junctions 6,875 → 13,953; chunks with a prefab reference 330 → 343.
- **Decorator definitions: 49 → 70.** Cosmetic entries 25,927 → 29,890; authoritative entries 5,902 → 8,068; actor decorator entries 1,427 → 1,989; actor-class references 209 → 279.
- **DA_Warehouse_Small_02a:** 30 → 29 chunks (required-mesh RefCount sum 30 → 29).
- **D_Residential_House_03:** chunks with a prefab 6 → 2. **D_Residential_House_04:** 17 → 12.
- **House decorators, cosmetic entries:** D_Decorator_D_Residential_House_01 448 → 470, _03 470 → 492, _04 438 → 459, _05 435 → 455. Required cosmetic meshes: _01 98 → 101, _03 106 → 107, _04 95 → 97, _05 99 → 100.
- **Actor decorator entries:** DA_ApartmentBuilding_Decorator_01c 103 → 104, D_Decorator_Shop_01 16 → 17, D_Decorator_Residential_Bungalow_02 22 → 23.
- **Madrid reskins:** the same 7 of 9 pairs share chunk IDs. The two House pairs (Madrid 01 and 03) still differ from Bakurani.
- **SaveIDs** changed on 97 existing files. Per-chunk prefab hashes and primitive-data values also changed; those fields are not decoded here, so no table records them.

Full before/after list: [Season 2 Changes → World, Visuals & Audio]({{ '/season-2-changes/world-visuals-audio.html' | relative_url }}).

---

## 1. File Inventory

| Type | Files | Role (as read) |
|---|---|---|
| `BHDestructionBuildingDefinitionDataAsset` | 74 | Destructible building: chunk layout, junctions, required meshes, Niagara refs |
| `BHDestructionBuildingDecoratorDefinitionDataAsset` | 70 | Decorator layer for a building: spawned actors, cosmetic props, authoritative props, preload lists |
| `BHDestructionDecoratorMeshDamageTagsDataAsset` | 2 | Per-mesh damage-tag whitelists (ballistic and explosive) |
| `BHDestructionBuildingVFXDataAsset` | 1 | `D_BuildingVFX`: chunk classification to Niagara data channel and Houdini point caches |

Folders: `Flix/Blueprints/Bakurani` (30 buildings), `Flix/Blueprints/Madrid` (10), `Flix/Blueprints/Industrial` (14), `Flix/Blueprints/Commercial/Office` (1), `Flix/Blueprints/Commercial/Highstreet` (14), `Flix/Blueprints/Commercial/Hospital` (4), `Flix/Blueprints/Commercial/WorkShop` (1), `Flix/DataAssets`, and `Flix/VFX/.../DataChannels`.

---

## 2. Building Definitions (`BHDestructionBuildingDefinitionDataAsset`, 74 assets)

**Totals across all 74:** 22,137 chunks, 3,943 required-mesh entries, 13,953 junctions, 343 chunks with a prefab reference.

### 2a. Top-level fields

| Property | Shape | Meaning (confidence) |
|---|---|---|
| `SaveID` | GUID string | Building identifier. Madrid copies get a different SaveID from their Bakurani source (checked on apartment and house pairs). Purpose not confirmed. |
| `RequiredMeshes` | list of `{StaticMesh, MaterialOverrideArray, PhysicalMaterialOverride, MeshCenter, RefCount, StringISMOverrides}` | Static meshes the building needs. `RefCount` is how many chunks use it. `MeshCenter` is the pivot offset (high confidence, from field names). |
| `ChunkData` | list of chunk records | One record per destructible piece. Fields in 2b. |
| `ChunkIDLookupMap` | list of `{Key: ChunkId, Value: index}` | Same length as `ChunkData`. Maps chunk GUID to array index (confirmed by inspection on `DA_Warehouse_Small_Hut_02a`). |
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
| `NiagaraBespokeEffectFormat` | Enum: `NoBespokeFormat`, `Wall2m`, `Wall4m`, `Wall6m`. Picks a bespoke debris effect by wall length. On `DA_ApartmentBuilding_01_a`, `Wall4m` (481) is the most common non-default format. |
| `NiagaraDataChannelParameters` | Debris tags: `DebrisMeshType` (Wall, Ceiling, Roof, Balcony, Generic), `DebrisShape` (e.g. `Wall_4m`, `Corner_J_2m_x_2m`, `Roof_Slope_4m_x_4m`, or `None`), `DebrisMaterial` (Concrete, Wood, Metal). |
| `ChunkTraits` | Present on every chunk, empty on every sampled chunk. |
| `ChunkCustomPrimitiveData` | Four floats (e.g. `0.4, 0.12, 0.085, 1.0`). Meaning not stated, probably shader parameters. Not decoded. |
| `Prefab` / `PrefabHash` | Optional prefab class reference (e.g. `CP_ModKit04_Roof_Panel_Short_2m_A`). Mostly on apartments (47, 23, 36 chunks in the three Bakurani apartment blocks), Office (15), houses and bungalows (0 to 17 each), Highstreet buildings (0 to 3 each) and hospitals (1 each). |
| `AudioPhysMaterialArray` | Audio physical materials. Empty on sampled chunks. |
| `Properties` | Integer flag field. Non-zero on 882 of 1,550 chunks in `DA_ApartmentBuilding_01_a`. Meaning not confirmed. |

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
| D_Residential_House_03 | Bakurani/Residential | 76 | 73 | 159 | 98 | 1 | 2 | 158 | 69 | 85 | 317 |
| D_Residential_House_04 | Bakurani/Residential | 89 | 80 | 153 | 85 | 1 | 12 | 136 | 72 | 100 | 289 |
| D_Residential_House_05 | Bakurani/Residential | 94 | 82 | 163 | 96 | 1 | 2 | 162 | 135 | 95 | 325 |
| D_Residential_House_Abandoned_01 | Bakurani/Residential | 86 | 69 | 130 | 107 | 2 | 0 | 195 | 84 | 49 | 325 |
| D_Residential_House_05b | Bakurani/Residential | 97 | 82 | 163 | 96 | 1 | 11 | 163 | 135 | 80 | 326 |
| D_Residential_House_06 | Bakurani/Residential | 70 | 59 | 219 | 168 | 0 | 0 | 320 | 175 | 54 | 539 |
| D_Residential_House_Var_01 | Bakurani/Residential | 94 | 79 | 159 | 87 | 1 | 3 | 143 | 89 | 136 | 302 |
| D_Residential_House_Var_03 | Bakurani/Residential | 79 | 76 | 159 | 98 | 1 | 2 | 158 | 69 | 85 | 317 |
| D_Residential_House_Var_04 | Bakurani/Residential | 89 | 80 | 153 | 85 | 1 | 2 | 136 | 72 | 100 | 289 |
| D_Residential_House_Var_05 | Bakurani/Residential | 93 | 81 | 163 | 96 | 1 | 1 | 162 | 135 | 95 | 325 |
| D_SupplyBuilding_01 | Bakurani/Residential | 19 | 18 | 58 | 42 | 0 | 0 | 50 | 0 | 24 | 108 |
| D_SupplyBuilding_02 | Bakurani/Residential | 20 | 19 | 34 | 55 | 0 | 0 | 67 | 0 | 20 | 101 |
| D_SwimPoolBuilding_01 | Bakurani/Residential/SwimmingPool | 39 | 35 | 251 | 182 | 0 | 0 | 271 | 3 | 107 | 522 |
| D_SwimPool_Building_02 | Bakurani/Residential/SwimmingPool | 33 | 32 | 326 | 350 | 0 | 0 | 520 | 97 | 85 | 846 |
| DA_Office_01a | Commercial/Office | 98 | 74 | 487 | 356 | 1 | 15 | 649 | 267 | 147 | 1136 |
| D_Comm_Highstreet_Base_01a | Commercial/Highstreet | 53 | 39 | 181 | 136 | 0 | 0 | 155 | 73 | 13 | 336 |
| D_Comm_Highstreet_Base_02a | Commercial/Highstreet | 61 | 42 | 170 | 122 | 1 | 0 | 140 | 94 | 1 | 310 |
| D_Comm_Highstreet_Base_02b | Commercial/Highstreet | 35 | 31 | 197 | 108 | 0 | 0 | 120 | 59 | 0 | 317 |
| D_Comm_Highstreet_Base_02c | Commercial/Highstreet | 39 | 29 | 185 | 128 | 1 | 0 | 144 | 71 | 0 | 329 |
| D_Comm_Highstreet_Base_02d | Commercial/Highstreet | 34 | 26 | 222 | 113 | 1 | 0 | 123 | 53 | 14 | 345 |
| D_Comm_Highstreet_Top_01a | Commercial/Highstreet | 66 | 54 | 353 | 243 | 2 | 3 | 402 | 231 | 186 | 755 |
| D_Comm_Highstreet_Top_02a | Commercial/Highstreet | 58 | 45 | 499 | 357 | 2 | 0 | 576 | 184 | 404 | 1075 |
| D_Comm_Highstreet_Top_02b | Commercial/Highstreet | 58 | 45 | 500 | 358 | 2 | 0 | 577 | 185 | 404 | 1077 |
| D_Comm_Highstreet_Top_02e | Commercial/Highstreet | 56 | 45 | 255 | 163 | 2 | 0 | 257 | 93 | 204 | 512 |
| D_Comm_Highstreet_Top_03a | Commercial/Highstreet | 62 | 47 | 848 | 522 | 2 | 0 | 906 | 452 | 421 | 1754 |
| D_Comm_Highstreet_Top_04a | Commercial/Highstreet | 61 | 47 | 733 | 420 | 2 | 0 | 695 | 391 | 359 | 1428 |
| D_Comm_Highstreet_Top_Var_01a | Commercial/Highstreet | 65 | 53 | 353 | 242 | 2 | 0 | 401 | 231 | 186 | 754 |
| D_Comm_Highstreet_Top_Var_02c | Commercial/Highstreet | 61 | 48 | 454 | 346 | 2 | 0 | 597 | 207 | 256 | 1051 |
| D_Comm_Highstreet_Top_Var_02d | Commercial/Highstreet | 62 | 49 | 503 | 346 | 2 | 0 | 597 | 286 | 257 | 1100 |
| DA_HospitalBuilding_01a | Commercial/Hospital | 65 | 47 | 495 | 563 | 1 | 0 | 866 | 48 | 171 | 1361 |
| DA_HospitalBuilding_01b | Commercial/Hospital | 58 | 50 | 813 | 948 | 1 | 0 | 1635 | 175 | 605 | 2448 |
| DA_HospitalBuilding_01c | Commercial/Hospital | 64 | 46 | 649 | 698 | 1 | 0 | 1120 | 90 | 190 | 1769 |
| DA_HospitalBuilding_01d | Commercial/Hospital | 46 | 39 | 211 | 252 | 1 | 0 | 389 | 95 | 134 | 600 |
| D_WorkShopBuilding_01 | Commercial/WorkShop | 20 | 20 | 88 | 33 | 1 | 0 | 41 | 4 | 18 | 129 |
| DA_Factory_Awning_01a | Industrial/Factory_Awning_01a | 5 | 5 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| DA_Factory_Awning_02a | Industrial/Factory_Awning_02a | 1 | 1 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| DA_Warehouse_02a | Industrial/Warehouse_02a | 13 | 13 | 84 | 0 | 0 | 0 | 0 | 16 | 64 | 84 |
| DA_Warehouse_03a | Industrial/Warehouse_03a | 22 | 22 | 237 | 0 | 0 | 0 | 0 | 46 | 278 | 237 |
| DA_Warehouse_03b | Industrial/Warehouse_03a | 21 | 21 | 235 | 0 | 0 | 0 | 0 | 46 | 278 | 235 |
| DA_Warehouse_04a | Industrial/Warehouse_04a | 15 | 15 | 168 | 0 | 0 | 0 | 0 | 0 | 167 | 168 |
| DA_Warehouse_Garage_01a | Industrial/Warehouse_Garage_01a | 5 | 5 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| DA_Warehouse_Scrapyard_01a | Industrial/Warehouse_Scrapyard_01a | 6 | 6 | 48 | 0 | 0 | 0 | 0 | 0 | 32 | 48 |
| DA_Warehouse_Small_01a | Industrial/Warehouse_Small_01a | 12 | 12 | 68 | 0 | 0 | 0 | 0 | 0 | 36 | 68 |
| DA_Warehouse_Small_02a | Industrial/Warehouse_Small_02a | 14 | 14 | 29 | 0 | 0 | 0 | 0 | 0 | 18 | 29 |
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
- `DA_ApartmentBuilding_01_b` is the largest building: 1,979 chunks, 1,115 junctions.
- Industrial buildings have no junctions and no edge pieces, but many chunks. They break into flat pieces with no junction layer.
- The Madrid apartment and bungalow definitions match their Bakurani sources chunk for chunk (section 7).

---

## 3. Decorator Definitions (`BHDestructionBuildingDecoratorDefinitionDataAsset`, 70 assets)

**Totals across all 70:** 29,890 cosmetic decorator entries, 8,068 authoritative decorator entries, 1,989 actor decorator entries, 279 actor-class references.

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
| DA_ApartmentBuilding_Decorator_01c | Bakurani/Apartments | 11 | 104 | 2975 | 600 | 167 | 69 | 0 |
| DA_Decorator_MarketBuilding_02 | Bakurani/Commercial/MarketBuilding_02 | 1 | 17 | 12 | 96 | 5 | 36 | 0 |
| D_MarketBuilding_04a_deco | Bakurani/Commercial/MarketBuilding_04 | 1 | 4 | 2 | 32 | 2 | 17 | 0 |
| D_MarketBuilding_05a_deco | Bakurani/Commercial/MarketBuilding_05 | 1 | 8 | 9 | 19 | 6 | 11 | 0 |
| D_Decorator_MarketBuilding_06 | Bakurani/Commercial/MarketBuilding_06 | 1 | 6 | 25 | 39 | 10 | 16 | 0 |
| D_Market_Building_Deco_01a | Bakurani/Commercial/Market_Building_01 | 2 | 32 | 54 | 115 | 19 | 39 | 0 |
| D_Decorator_MarketBuilding_03a | Bakurani/Commercial/Market_Building_03 | 2 | 23 | 65 | 74 | 20 | 17 | 0 |
| D_Decorator_Shop_01 | Bakurani/Commercial/Shop_01 | 3 | 17 | 144 | 104 | 43 | 41 | 0 |
| D_Decorator_Shop_02 | Bakurani/Commercial/Shop_02 | 4 | 8 | 92 | 25 | 30 | 11 | 0 |
| D_Decorator_Shop_03 | Bakurani/Commercial/Shop_03 | 4 | 15 | 98 | 50 | 26 | 20 | 0 |
| D_Decorator_D_Residential_House_01 | Bakurani/Residential | 6 | 32 | 470 | 63 | 101 | 38 | 0 |
| D_Decorator_D_Residential_House_03 | Bakurani/Residential | 11 | 51 | 492 | 75 | 107 | 39 | 0 |
| D_Decorator_D_Residential_House_04 | Bakurani/Residential | 10 | 48 | 459 | 57 | 97 | 34 | 0 |
| D_Decorator_D_Residential_House_05 | Bakurani/Residential | 7 | 33 | 455 | 88 | 100 | 39 | 0 |
| D_Decorator_D_Residential_House_05b | Bakurani/Residential | 7 | 24 | 428 | 80 | 98 | 40 | 0 |
| D_Decorator_Residential_House_06 | Bakurani/Residential | 7 | 37 | 188 | 199 | 31 | 106 | 0 |
| D_Decorator_Res_Abandoned_01 | Bakurani/Residential | 5 | 23 | 450 | 47 | 104 | 29 | 0 |
| D_Decorator_Residential_Bungalow_01 | Bakurani/Residential | 5 | 19 | 210 | 42 | 95 | 31 | 3 |
| D_Decorator_Residential_Bungalow_02 | Bakurani/Residential | 4 | 23 | 288 | 45 | 85 | 31 | 0 |
| D_Decorator_Residential_Bungalow_03 | Bakurani/Residential | 7 | 18 | 202 | 31 | 70 | 25 | 0 |
| D_Decorator_SupplyBuilding_01 | Bakurani/Residential | 1 | 1 | 62 | 0 | 13 | 0 | 0 |
| D_Decorator_SupplyBuilding_01b | Bakurani/Residential | 2 | 4 | 83 | 31 | 24 | 7 | 0 |
| D_Decorator_SupplyBuilding_02 | Bakurani/Residential | 2 | 4 | 42 | 0 | 10 | 0 | 0 |
| D_Decorator_SupplyBuilding_02b | Bakurani/Residential | 2 | 4 | 57 | 19 | 20 | 8 | 0 |
| D_Decorator_SwimPoolBuilding_01 | Bakurani/Residential/SwimmingPool | 4 | 58 | 155 | 47 | 17 | 14 | 0 |
| D_Decorator_SwimPool_Building_02 | Bakurani/Residential/SwimmingPool | 2 | 24 | 9 | 62 | 4 | 16 | 0 |
| DA_Office_Decorator_01a | Commercial/Office | 8 | 87 | 1571 | 362 | 131 | 45 | 0 |
| D_Decorator_Comm_Highstreet_Base_01a | Commercial/Highstreet | 3 | 12 | 114 | 58 | 36 | 24 | 0 |
| D_Decorator_Comm_Highstreet_Base_02a | Commercial/Highstreet | 4 | 12 | 108 | 9 | 48 | 6 | 0 |
| D_Decorator_Comm_Highstreet_Base_02b | Commercial/Highstreet | 1 | 1 | 84 | 30 | 29 | 15 | 0 |
| D_Decorator_Comm_Highstreet_Base_02c | Commercial/Highstreet | 0 | 0 | 120 | 36 | 42 | 16 | 0 |
| D_Decorator_Comm_Highstreet_Base_02d | Commercial/Highstreet | 0 | 0 | 118 | 54 | 41 | 13 | 0 |
| D_Decorator_Comm_Highstreet_Top_01a | Commercial/Highstreet | 3 | 24 | 276 | 66 | 50 | 8 | 0 |
| D_Decorator_Comm_Highstreet_Top_02a | Commercial/Highstreet | 3 | 30 | 226 | 102 | 44 | 12 | 0 |
| D_Decorator_Comm_Highstreet_Top_02b | Commercial/Highstreet | 3 | 28 | 221 | 103 | 44 | 12 | 0 |
| D_Decorator_Comm_Highstreet_Top_02c | Commercial/Highstreet | 3 | 30 | 289 | 102 | 54 | 12 | 0 |
| D_Decorator_Comm_Highstreet_Top_02d | Commercial/Highstreet | 3 | 30 | 287 | 103 | 53 | 12 | 0 |
| D_Decorator_Comm_Highstreet_Top_02e | Commercial/Highstreet | 3 | 22 | 166 | 58 | 43 | 11 | 0 |
| D_Decorator_Comm_Highstreet_Top_03a | Commercial/Highstreet | 3 | 20 | 263 | 139 | 45 | 13 | 0 |
| D_Decorator_Comm_Highstreet_Top_04a | Commercial/Highstreet | 3 | 20 | 245 | 111 | 43 | 13 | 0 |
| DA_HospitalBuilding_01a_Decorator | Commercial/Hospital | 7 | 61 | 102 | 107 | 13 | 16 | 0 |
| DA_HospitalBuilding_01b_Decorator | Commercial/Hospital | 5 | 108 | 267 | 472 | 53 | 42 | 0 |
| DA_HospitalBuilding_01c_Decorator | Commercial/Hospital | 3 | 40 | 202 | 211 | 51 | 34 | 0 |
| DA_HospitalBuilding_01d_Decorator | Commercial/Hospital | 5 | 27 | 63 | 51 | 28 | 15 | 0 |
| D_Decorator_WorkShopBuilding_01 | Commercial/WorkShop | 2 | 9 | 102 | 13 | 27 | 9 | 0 |
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
- Four decorators hold a single property and no decoration data: `FA_Factory_Awning_01a_Decorator`, `DA_Factory_Awning_02a_Decorator`, `DA_Warehouse_Garage_01a_Decorator`, `DA_Warehouse_Scrapyard_01a_Decorator`. Those buildings get no decoration.
- `DA_Warehouse_04a_Decorator` has 29 actor decorators and no cosmetic or authoritative data.
- The Madrid apartment decorators carry about the same counts as the Bakurani ones but are not identical (cosmetic 3,617 for `DA_Ozeti_ApartmentBuilding_Decorator_01a` vs 3,573 for `DA_ApartmentBuilding_Decorator_01a`).

### 3c. Actor classes used by decorators (top 25 by reference count)

| Actor class (leaf name) | Occurrences across decorators |
|---|---|
| WDDestructionAmbienceVolume | 61 |
| B_SmashableApartmentSingleWindow | 31 |
| B_SmashableApartmentDoubleWindow | 21 |
| B_Door | 20 |
| MI_Apartment_EdgeDirt_01b | 16 |
| BP_InteractableDoor_ApartmentBalcony | 14 |
| BP_InteractableDoor_Apartment | 13 |
| BP_Debris_Decal_01a | 11 |
| B_SmashableApartmentBalconyWindow | 10 |
| MI_Apartment_EdgeDirt_01d | 10 |
| MI_Apartment_EdgeDirt_01c | 9 |
| BP_WaterStain_Decal_01a | 9 |
| BP_InteractableDoor_ApartmentEntrance | 8 |
| MI_Apartment_EdgeDirt_01f | 7 |
| BP_Apartment_EdgeDirt_01a | 6 |
| B_SmashableHospitalSingleWindow_03 | 4 |
| BP_Apartment_StairStripeDecal_01a | 3 |
| BP_Apartment_StairStripeDecal_01b | 3 |
| BP_Interactable_HospitalDoor_01a_Left | 3 |
| BP_Interactable_HospitalDoor_01a_Right | 3 |
| BP_Apartment_StairStripeDecal_Orange_01a | 2 |
| BP_Apartment_StairStripeDecal_Orange_01b | 2 |
| MI_Apartment_EdgeDirt_01e | 2 |
| BP_InteractableDoor_Buisness | 2 |
| BP_Apartment_StairStripeDecal_Blue_01a | 1 |

These are soft references (`AssetPathName`). Most are doors (`BP_InteractableDoor_*`, `B_Door`, `BP_Interactable_HospitalDoor_*`), smashable window and balcony blueprints (`B_Smashable*Window`, `B_SmashableApartmentBalconyDoor`), and decals (`MI_Apartment_EdgeDirt_*`, `BP_Apartment_StairStripeDecal_*`, `BP_WaterStain_Decal_01a`, `BP_Debris_Decal_01a`). One script class, `/Script/WDGame.WDDestructionAmbienceVolume`, is used 61 times.

---

## 4. Damage-Tag Whitelists (`BHDestructionDecoratorMeshDamageTagsDataAsset`)

| Asset | Entries | Content |
|---|---|---|
| `DA_DestructionDecoratorBallisticsTagWhitelist` | 68 | Each entry is `Key` (a `/Game/...` static mesh path: decorative room props such as `SM_DecorativePlate01`, and Megascans assets) and `Value` (a list of damage-tag strings). 67 entries carry 13 tags. One entry (`S_Wooden_Floor_Lamp_vi5hbjgga_high_Var2`) carries 12. |
| `DA_DestructionDecoratorExplosiveTagWhitelist` | 0 | Header only, no `Properties`. Empty. |

**The 13 distinct ballistic tags** (all `Meta.Damage.Bullet.*`): `9mm`, `12g`, `30mm`, `308Win`, `338Nor`, `45ACP`, `45Colt`, `50Cal`, `545mm`, `556mm`, `762mm`, `762x51mm`, `762x54mm`. 67 of the 68 meshes carry all 13.

Meaning, inferred from the name: a mesh gets bullet decoration only if the incoming damage tag is on its list. The explosive whitelist is empty, so no mesh in this export is whitelisted for explosive damage tags.

---

## 5. Chunk-Classification VFX (`D_BuildingVFX`, `BHDestructionBuildingVFXDataAsset`)

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

The `Flix/Blueprints/Madrid` folder re-uses Bakurani geometry under new SaveIDs. Chunk-ID lists were compared pairwise:

| Madrid asset | Bakurani source | Same chunk IDs |
|---|---|---|
| `DA_Ozeti_ApartmentBuilding_01_a` | `DA_ApartmentBuilding_01_a` | yes |
| `DA_Ozeti_ApartmentBuilding_01c` | `DA_ApartmentBuilding_01c` | yes |
| `D_Residential_Bungalow_Madrid_01` | `D_Residential_Bungalow_01` | yes |
| `D_Residential_Bungalow_Madrid_02` | `D_Residential_Bungalow_02` | yes |
| `D_Residential_Bungalow_Madrid_03` | `D_Residential_Bungalow_03` | yes |
| `D_Residential_House_Madrid_01` | `D_Residential_House_01` | no (148 vs 143 edge pieces) |
| `D_Residential_House_Madrid_03` | `D_Residential_House_03` | no |
| `D_Residential_House_Madrid_04` | `D_Residential_House_04` | yes |
| `D_Residential_House_Madrid_05` | `D_Residential_House_05` | yes |

So 7 of 9 pairs share chunk IDs. `D_FootballStadium_Building_01a` (Madrid, 463 chunks, no junctions) has no Bakurani source in this folder.

---

## 8. Still not pulled / Limitations

- **Unresolved property names.** Some properties appear only as GUID-style keys. On every `RequiredMeshes` entry the value is `EBHDestructionCPDInputStyle::Building`. Cosmetic decorator entries carry an unnamed list. Their meaning is not known from this export.
  - **SDK (2026-10-16):** `EBHDestructionCPDInputStyle` is a 3-value enum: `Building = 0`, `TrimSheet = 1`, `None = 2`. The doc's observation that every `RequiredMeshes` entry carries `Building` is consistent with the enum's design — building meshes get the `Building` style, trimsheet meshes get `TrimSheet`. The GUID-style keys on cosmetic decorator entries remain unresolved via SDK (Dumper-7 could not label them).
- **Bit and enum meanings not decoded.** The chunk `Properties` flag, `ChunkCustomPrimitiveData` (four floats) and `ChunkTraits` (empty in every sample) are reported as found, not interpreted.
- **Connection semantics inferred.** "Vital" and "proportional" support links are read from property names. Runtime behaviour is not confirmed.
- **Decorator-to-building link is by name.** Only the `OwningChunkIDs` GUIDs give a hard link, and they were spot-checked, not checked for every decorator.
- **Explosive whitelist is empty.** Whether that is intended or a cook artifact is not known.
- **One ballistic entry with 12 tags.** The mesh `S_Wooden_Floor_Lamp_vi5hbjgga_high_Var2` is missing one of the 13 tags. Which one was not checked.
- **Units.** `Transform` values are reported raw. The dump does not state units.
- **Houdini point caches not expanded.** Section 5 gives names and counts only.
- **Large files summarised, not read entry by entry.** The largest file (`DA_ApartmentBuilding_01_b`, about 7.5 MB) was parsed in full by script, and its chunk arrays were summarised rather than inspected individually.
