---
title: "ControlZoneRegions (feature)"
parent: "Game Features"
redirect_from: ["/Wardogs_GameFeatures_ControlZoneRegions_v2.html", "/Wardogs_GameFeatures_ControlZoneRegions_v2"]
---

# Wardogs — GameFeature: ControlZoneRegions Reference
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). Source: [`Wardogs/Plugins/GameFeatures/ControlZoneRegions/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions) (5 JSON files). Scripted pass over every file, then checked against the region arrays directly.*

> **Scope:** this folder holds the **region map data** for Control Zones: named polygons laid over each map, each with a selection weight. It is the layer the [`ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone.json) configs (sibling doc `Wardogs_GameFeatures_ControlZone_v2.md`) pick their zone placements from. The mapping between region weights and the zone placement is **not confirmed** by these files (section 5).

---

## 1. Package Contents

| File | Type | Role |
|---|---|---|
| [`ControlZoneRegions.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/ControlZoneRegions.json) | `GameFeatureData` | Root bundle. One action: a data-registry add for `DR_Editor_Trackers_ControlZoneRegions`, with `bPreloadInEditor` and `bPreloadInCommandlets` on. |
| [`DA_ControlZoneRegionsConfig_Kavkazi.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/Config/DA_ControlZoneRegionsConfig_Kavkazi.json) | `WDControlZoneRegionsConfigDataAsset` | 60 regions. |
| [`DA_ControlZoneRegionsConfig_Europe.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/Config/Europe/DA_ControlZoneRegionsConfig_Europe.json) | `WDControlZoneRegionsConfigDataAsset` | 55 regions. |
| [`DA_ControlZoneRegionsConfig_NorthAmerica.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/Config/NorthAmerica/DA_ControlZoneRegionsConfig_NorthAmerica.json) | `WDControlZoneRegionsConfigDataAsset` | 56 regions. |
| [`DT_Editor_TrackerData_ControlZoneRegions.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/DT_Editor_TrackerData_ControlZoneRegions.json) | `DataTable` (1 row) | Editor tracker for the regions, tag `Trackers.Type.ControlZone` (section 4). |

The bundle's data registry is marked **editor-only** (`DR_Editor_*`), and the tracker widget is also an editor widget (`W_Editor_Tracker_Regions`). The region data is therefore an authoring tool layer, not a runtime UI.

---

## 2. Region Record Format

Each region in an config's `ControlZoneRegionsData` array has five fields:

| Field | Type | Meaning |
|---|---|---|
| `ControlZoneRegionName` | string | Region label (for example `TOWER 1`, `Factory Large 1`). |
| `ControlZoneRegionDefaultWeight` | float | Base selection weight. **0 means the region is not chosen by default.** |
| `ControlZoneRegionAlternatorWeights` | float list | Per-alternator weights (see section 3). |
| `ControlZoneRegionPoints` | 2D point list (X, Y) | Polygon outline in world units. Between 4 and 44 points. |
| `ControlZoneRegionDebugColour` | RGBA + hex | Colour used to draw the region in the editor. |

---

## 3. Per-Config Statistics

| Config | Regions | Non-zero default weight | Sum of default weights | Weight range | Points per region |
|---|---|---|---|---|---|
| Kavkazi | 60 | 53 | **83.0** | 0.0 to 5.0 | 4 to 44 |
| Europe | 55 | 54 | **54.0** | 0.0 to 1.0 | 4 to 16 |
| NorthAmerica | 56 | 53 | **53.0** | 0.0 to 1.0 | 4 to 11 |

Interpretation of the weights:
- **Kavkazi** uses weights from 0 to 5. Most regions weigh 1.0 and some weigh 5.0, so those regions are much more likely to be picked.
- **Europe** and **NorthAmerica** use only 0 and 1, so every non-zero region is equally likely.

### 3a. Zero-weight regions (never chosen by default weight)

| Config | Zero-weight regions |
|---|---|
| Kavkazi (7) | `TOWER 1`, `TOWER 2`, `TOWER 3`, `TOWER 4`, `AbandonedTWR 2`, `TOWER 7`, `AbandonedTWR 3` |
| Europe (1) | `Tower 2` |
| NorthAmerica (3) | `Tower 1`, `Tower 2`, `Tower 3` |

The towers are the zero-weight regions in every config. They look like sites that are placed by hand or reserved for some other rule, but the data does not say which.

### 3b. Weight examples (Kavkazi, weight 5.0)

`SUNFLOWERS HOUSE`, `WEST FOREST PYLON`, `HILLSIDE TOP` (and other 5.0 regions). Most other non-zero Kavkazi regions weigh 1.0. Europe examples at weight 1.0: `Tower 1`, `Tower 3`, `Tower 4`, `POI Stadium`, `POI Pool`, `POI ChurchTop`, `POI Lumberyard`, `POI Apartments`.

---

## 4. Region Names by Config

Names are as stored. Spelling and case vary between configs.

**Kavkazi (60).** Towers (`TOWER 1`, `TOWER 2`, `TOWER 3`, `TOWER 4`, `TOWER 5 L`, `TOWER 7`, `AbandonedTWR 2`, `AbandonedTWR 3`), sunflower fields (`SUNFLOWERS SOUTH`, `SUNFLOWERS HOUSE`, `SUNFLOWERS CENTER`, `SUNFLOWER NORTH`, `SUNFLOWERS TOWER`, `SUNFLOWER CHURCH`), forest (`SOUTH TOWN FOREST WEST`, `SOUTH TOWN FOREST EAST`, `WEST FOREST PYLON`, `WEST FOREST NORTH`, `WEST FOREST CENTRAL`, `WEST FOREST HOUSE 2/3/4`, `RIVERSIDE FOREST`, `WEST HILL WOODS`), hills (`HILLSIDE HOUSES`, `HILLSIDE TOP`, `HILL TOWN`, `BRIDGE HILL`, `LUMBER HILLS 2`, `GREEN MOUNTAIN`), lumber and farmland (`LUMBERYARD HOUSE`, `LUMBERYARD NORTH`, `LUMBERYARD SOUTH`, `LUMBER FARMLANDS`, `SOUTH TOWN FARMLANDS`, `GREEN FARMLAND`), water (`WATER SILOS 2`, `WATER STORAGE OUTCROP`, `POND`, `MARKET SWAMP`, `NORTH RIVER`, `SOUTH WEST RIVER`), and urban (`APARTMENT HILLSIDE`, `APPARTMENTS`, `RESIDENTIAL`, `CONTAINERS AND FACTORY`, `SCRUBLAND WEST`, `SCRUBLAND EAST`).

**Europe (55).** Towers (`Tower 1` to `Tower 4`) and points of interest (`POI Stadium`, `POI Pool`, `POI ChurchTop`, `POI Lumberyard`, `POI Apartments`, and others).

**NorthAmerica (56).** Towers (`Tower 1` to `Tower 3`), industry (`Factory Large 1`, `Factory Large 2`, `Shipping Exports Large`, `Shipping Exports Long`, `Import Scrap`), and rail (`TrainTracks`, `TrainShed 1`, `TrainShed 2`).

The Kavkazi config is named for the map that the [`ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone.json) Bakurani config uses (`/Game/Maps/Worlds/Kavkazi/Kavkazi`), so the Kavkazi regions are most likely for that map. The Europe and NorthAmerica regions are matched by folder and name to their [`ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone.json) configs. That match is by name only.

---

## 5. Alternator Weights

Each region has a `ControlZoneRegionAlternatorWeights` list of floats. The lists are not all the same length, and they do not match the alternator count in the zone configs.

| Config | List lengths per region | Values |
|---|---|---|
| Kavkazi | 30 for 33 regions; 35 to 59 for the rest | Mostly 0.0, with fractional values (7 distinct values across 2,260 entries, including 0.2) |
| Europe | 0 to 54, varying by region | Mostly 1.0 (1,471 of 1,485 sampled entries) |
| NorthAmerica | 0 to 55, varying by region | Mostly 1.0 (1,537 of 1,540 sampled entries) |

Points to note:
- The **ControlZone** configs have **3 alternators** on Bakurani and **4** on Europe and NorthAmerica (see the sibling doc). The per-region lists have up to 59 entries. So the list index is not a direct index into the config's alternators.
- Non-zero entries sit at specific indices. For example, the Kavkazi `SUNFLOWERS SOUTH` region is non-zero at indices 0 to 4, and `TOWER 3` at indices 11 and 26.
- What an index refers to is **not confirmed** by these files. It could be an alternator index in a larger set, or a per-map placement ID.

---

## 6. Geometry

Each region has a closed polygon of 4 to 44 points in world units. Point counts are:

| Config | Min points | Max points |
|---|---|---|
| Kavkazi | 4 | 44 |
| Europe | 4 | 16 |
| NorthAmerica | 4 | 11 |

Example: the first Kavkazi region, `TOWER 1`, starts its outline at X = -824,856. The shape comes from its point list, so each region is a polygon, not a bounding box. Overlap and containment rules are not in the data.

---

## 7. Tracker

| Item | Value |
|---|---|
| Table | [`DT_Editor_TrackerData_ControlZoneRegions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/DT_Editor_TrackerData_ControlZoneRegions.json) (1 row) |
| Tag | `Trackers.Type.ControlZone` |
| Widget | `/ControlZoneRegions/Data/UI/W_Editor_Tracker_Regions` |
| View model | `WDUIRegionsTrackerViewModel` (ControlZoneRegionsRuntime) |
| Data asset | [`/Game/UI/Tools/WorldDisplay/Data/DA_Editor_Tracker_Location`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Tools/WorldDisplay/Data/DA_Editor_Tracker_Location.json) |
| Faction change recreate | No |
| Required tags | none |

This tracker displays the regions in the editor. It is not a player-facing HUD tracker. The player-facing Control Zone trackers are in the [`ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone.json) folder (sibling doc).

---

## 8. Limitations

- **Weight meaning is not confirmed.** The files say what the weights are (default and per-alternator) but not how the game uses them to pick zones. The statement that weight 5.0 is "more likely" is an inference from the usual meaning of a selection weight.
- **Alternator index meaning is not confirmed** (section 5). The list lengths do not match the zone config alternator counts.
- **The zero-weight towers** may be placed by a rule outside this folder, and that rule was not found.
- **Region-to-config matching** for Europe and NorthAmerica is by name and folder only. The map names for those folders were not resolved.
- **Debug colours** are editor-only and are not analysed here.
- The regions are **polygons**, and their containment and overlap rules are not stated in the data. Overlap was not checked.
