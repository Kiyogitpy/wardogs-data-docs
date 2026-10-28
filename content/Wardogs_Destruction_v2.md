---
title: "Destruction"
redirect_from: ["/Wardogs_Destruction_v2.html", "/Wardogs_Destruction_v2"]
parent: "World, Visuals & Audio"
description: "Destruction lookups for normal and anonymous buildings, plus the score curves."
---

# Wardogs — Destruction Reference
*Extracted from cooked game data (JSON export, `Wardogs/Content/Destruction/`, 4 source files: 2 mesh-to-prefab lookup assets, 2 curves). Parsed with a Python script. Values are the raw exported values.*

> **Scope note:** this folder is small. It holds the mesh-to-prefab lookup tables that tell the engine which building mesh swaps to which destruction prefab, and two score curves. It has no damage thresholds, debris counts or collapse timings.

---

## Season 02 update (2026-10-15)

- **No files added or removed,** and no values in this folder's four files changed.
- **Garage assets** (`Environment/Architecture/Residential/Garages`, 14 files) changed only in an internal save identifier. This doc does not cover them, so no values are listed here.

## 1. Assets at a Glance

| Asset | Type | Entries / keys | What it does |
|---|---|---|---|
| `DA_NormalBuilding_MeshToPrefabLookup` | `BHDestructionMeshToPrefabLookupDataAsset` | 63 | Maps building meshes to destruction prefab classes (all 63 mapped) |
| `DA_AnonymousBuilding_MeshToPrefabLookup` | `BHDestructionMeshToPrefabLookupDataAsset` | 23 | Lists street and prop meshes. **No prefab is mapped** for any of the 23 |
| `CF_DestructionBuildingAngleScore` | `CurveFloat` | 3 keys | Score as a function of an angle-like input (time axis 0–100) |
| `CF_DestructionBuildingDistanceScore` | `CurveFloat` | 3 keys | Score as a function of distance (time axis 2,000–75,000) |

Full before/after list: [Season 2 Changes → World, Visuals & Audio]({{ '/season-2-changes/world-visuals-audio.html' | relative_url }}).

---

## 2. Normal Building Lookup (63 entries, all mapped)

Each `LookUp` entry is `Key` (the source static mesh) → `Value` (a prefab class, `CP_<name>_C`, that replaces it on destruction). `SubPathString` is empty for all entries.

**Mesh families by source folder** (the folder above the mesh in its `Walls/`, `Roof/`… path, counted by the prefab's folder):

| Family | Entries | Examples (prefab name, `CP_` prefix removed) |
|---|---|---|
| Walls | 14 | ModKit04_Wall_4m, ModKit04_Wall_2m, ModKit04_Wall_1m, ModKit04_Wall_Door_4m, ModKit04_Wall_Window_Single_4m_A |
| Roof | 13 | ModKit04_Roof_Bottom_A, ModKit04_Roof_Top_A, ModKit04_Roof_Corner_Top_A, ModKit04_Roof_Top_Middle_A |
| Balcony | 10 | ModKit04_Balcony_A, ModKit04_Balcony_B, ModKit04_Balcony_Roof_A, ModKit04_Balcony_Enclosed_A |
| Floor | 6 | ModKit04_Floor_4m_A, ModKit04_Floor_2m, ModKit04_Floor_1m, ModKit04_Floor_2x4m |
| ClothesLine | 5 | ModKit04_Clothes_Hanging_B–E, ModKit04_Clothes_Line_A |
| Apartment | 3 | Apartment_FirstFloor_MiddleEnd, Apartment_CorridorEnd, Apartment_StairCorridorEnd |
| Wall_Concrete_Residential_01 | 3 | (concrete residential wall set) |
| Stairs | 3 | ModKitHouse_Stairs_Interior_A, ModKitHouse_Stairs_L_Interior_B, ModKit04_Stairs_Metal_Full_A |
| Extension | 2 | ModKit04_Extension_Wall_01_A, _02_A |
| ModularKit_02_Pieces | 2 | ModularKit_02_Wall_Top_02, ModularKit_02_Corner_Top_02 |
| ApartmentEntrance | 1 | ModKit04_Entrance_A |
| CompressorUnit | 1 | CompressorUnit_01a |

Source meshes come from `Environment/Architecture/Residential/` (59 entries), `Environment/Props/Walls_and_Fences/` (3, the low-wall set) and one `Industrial` entry.

Naming irregularity to check:
- `SM_ModKit04_Roof_Panel_Short_4m_A` maps to `CP_ModKit04_Roof_Panel_Corner_Short_2m1` (a 4 m panel mapped to a 2 m corner prefab with a `1` suffix). It may be a copy-paste error in the lookup, or an intentional fallback. The export does not say.

---

## 3. Anonymous Building Lookup (23 entries, none mapped)

Every `Value` is an empty `AssetPathName`. The table lists the meshes that appear in the lookup but have no destruction prefab.

| Source folder | Entries | Meshes |
|---|---|---|
| Transport_Infrastructure / Road_Signs | 13 | SM_Road_Sign_01a … SM_Road_Sign_12a, plus SM_Road_Sign_013a |
| Transport_Infrastructure / Telephone_Poles | 4 | SM_TelephonePole_01a, 01b, 02a, 02b |
| Transport_Infrastructure / Street_Lights | 1 | SM_LampPost_01a |
| Props / Residential, Commercial | 3 | SM_ParkBench_01a, SM_Bench_01a, SM_CommercialBin_01a |
| Megascans traffic cone | 1 | S_Traffic_Cone_uhcgdgufa_high_Var1 |
| Maps / WhiteBox | 1 | SM_Cover_WheelyBin |

These are street objects (signs, poles, benches, bins, a cone). Their absence from the normal-building table suggests a different handling path. The Demolition folder has its own poles and signs (see the Demolition doc), but the export does not link the two folders, and it does not show which system reads the anonymous table.

---

## 4. Score Curves

Both are `CurveFloat` assets with cubic interpolation. Keys are listed as time → value.

### 4a. `CF_DestructionBuildingAngleScore`

| Time | Value |
|---|---|
| 0 | 0.70 |
| 90 | 0.20 |
| 100 | 0.00 |

The score drops from 0.7 to 0.2 across 0–90 and reaches 0 at 100. The time unit is not stated. The 0–100 range suggests degrees, but the export does not confirm it.

### 4b. `CF_DestructionBuildingDistanceScore`

| Time | Value |
|---|---|
| 2,000 | 1.00 |
| 50,000 | 0.50 |
| 75,000 | 0.10 |

Full score (1.0) inside 2,000 units, falling to 0.5 at 50,000 and 0.1 at 75,000. If the units are Unreal cm, that is 20 m, 500 m and 750 m. This is an inference from the export's usual units, not confirmed.

Neither curve states what it scores. Both are plausibly multipliers on a building-destruction value (for example, how strongly a hit or event affects a building), but the export does not say so.

---

## 5. How Values Combine

- A mesh that appears in the normal lookup has a prefab class to spawn when the building is destroyed. A mesh that appears only in the anonymous lookup has no prefab. How the anonymous meshes are destroyed is not in this folder.
- The two curves are independent, one-input functions. Combining them with each other or with other systems is not shown in the export.

---

## 6. Still Not Pulled / Limitations

- **The consumer of each lookup is not in this folder.** The export does not show which system reads the lookup tables, or when.
- **Prefab classes are referenced by name only.** The `CP_*_C` blueprint classes are not exported here, so their contents (debris, collision, damage thresholds) are unknown.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Curve input and output meanings are not stated.** The angle unit and the distance unit are inferred, not confirmed.
- **No damage or collapse numbers** appear in this folder, so none are reported.
- The **anonymous lookup has no prefab entries at all.** Whether it is unfinished or deliberately empty cannot be determined from the export.
