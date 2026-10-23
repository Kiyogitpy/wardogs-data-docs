---
title: "Taxi SkinsData (feature)"
redirect_from: ["/Wardogs_GameFeatures_Taxi_SkinsData_v2.html", "/Wardogs_GameFeatures_Taxi_SkinsData_v2"]
parent: "Vehicles"
description: "What This Folder Holds, Registry and Scan, Cosmetic Row, Skin"
---

# Wardogs — GameFeatures: Taxi_SkinsData
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/Taxi_SkinsData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData) — 3 JSON files.*

---

## 1. What This Folder Holds

The cosmetic data for the taxi (a Little Bird helicopter). One cosmetic entry, one skin asset, and a pack that registers both into the cosmetic and skin registries.

| File | Type | Role |
|---|---|---|
| [`Content/Taxi_SkinsData.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Taxi_SkinsData.json) | GameFeatureData + registry action | Registers the cosmetic table and scans skin assets |
| [`Content/Data/DT_Cosmetics_Taxi.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/DT_Cosmetics_Taxi.json) | DataTable (`WDCosmeticData`) | One cosmetic row |
| [`Content/Data/Skin_Taxi.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/Skin_Taxi.json) | `WDSkinDataAsset` | Skin with a material-swap mode |

---

## 2. Registry and Scan

| Item | Value |
|---|---|
| Registry | `CosmeticData` → [`DT_Cosmetics_Taxi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/DT_Cosmetics_Taxi.json) (client and server source) |
| Primary asset scan | `WDSkinDataAsset` (base `WDSkinDataAsset`, WDGame) |

---

## 3. Cosmetic Row ([`DT_Cosmetics_Taxi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/DT_Cosmetics_Taxi.json))

| Row | Field | Value |
|---|---|---|
| `Meta.Cosmetic.Taxi.Littlebird` | EntityId | `Vehicle.Variant.Air.Rotary.Littlebird.Default` |
| | Category | `Meta.Cosmetic.Taxi` |
| | Archetype | `Vehicle.Archetype.Air.Rotary` |
| | UITextures | `FallbackIcon` set (path in export) |

The only taxi cosmetic is for the Little Bird, and it binds to the variant `Vehicle.Variant.Air.Rotary.Littlebird.Default`.

---

## 4. Skin ([`Skin_Taxi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/Skin_Taxi.json))

| Field | Value |
|---|---|
| Application mode | `EWDSkinApplicationMode::MaterialSwap` |
| MaterialOverrides | A list of key–value overrides (contents not expanded here) |

A material-swap skin replaces the listed materials on the vehicle rather than changing the mesh.

---

## 5. Still not pulled / limitations

- **Material overrides.** The list of material swaps is in the export but was not expanded.
- **Icon path.** The `FallbackIcon` path is in the export; the texture itself is in the UI assets.
- **Other taxi variants.** Only one taxi cosmetic exists in this folder. Other vehicle skins are in the Skins and Vehicles docs.

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | `data/` re-exported with the v2 usmap (names only; values unchanged): the row key is spelled `EntityId`. |
