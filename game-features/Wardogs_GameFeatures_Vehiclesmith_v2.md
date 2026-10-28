---
title: "Vehiclesmith"
redirect_from: ["/Wardogs_GameFeatures_Vehiclesmith_v2.html", "/Wardogs_GameFeatures_Vehiclesmith_v2"]
parent: "Vehicles"
description: "The Vehiclesmith vehicle customisation screen: its scene, pages, data layers, dev menu map and persistent actions."
---

# Wardogs — Vehiclesmith Game Feature Reference
*Extracted from cooked game data (`Wardogs/Plugins/GameFeatures/Vehiclesmith`, 12 JSON files, all parsed). Build `++Wardogs+Live-CL-516586`, UE 5.7.*

> **What this is:** Vehiclesmith is the vehicle-customisation mode (the vehicle counterpart of Gunsmith), built on the shared **Itemsmith** UI framework. Almost everything here is UI configuration: scene layout, tabs, browser pages, camera modes, data layers and input bindings. There are no combat or balance numbers in this plugin.

---

## Season 02 update (2026-10-15)

- **No files added or removed.** The one changed file is the popup table below.
- **Popup options** (`DT_VehiclesmithPopupOptions`) went from 0 rows to 5, the same five popups as the Gunsmith popup table:
  - `UI.Popup.SaveBlueprint`: Info, Cancel / OK.
  - `UI.Popup.DeleteBlueprint`: Warning, "Do you wish to permanently delete this blueprint?" ("This cannot be undone"), Cancel / OK.
  - `UI.Popup.RenameItem`: Itemsmith rename type, RENAME / Cancel.
  - `UI.Popup.FullBlueprintItems`: Warning, OK.
  - `UI.Popup.ChangeComponent`: Warning, Apply / Cancel.

Full before/after list: [Season 2 Changes → Vehicles]({{ '/season-2-changes/vehicles.html' | relative_url }}).

## 1. Plugin Inventory

| Asset | Type | Role |
|---|---|---|
| `Vehiclesmith.json` (root) | `GameFeatureData` `Vehiclesmith` + `BHGameFeatureAction_AddInputContextMapping` + `GameFeatureAction_DataRegistrySource` | Registers input contexts and data registry sources |
| `Content/Data/DT_SceneData_Frontend_Vehiclesmith` | `DataTable` (`WDSceneDataTableRow`) | Frontend scene entry `UI.Scene.Frontend.Vehiclesmith` |
| `Content/Data/DT_Vehiclesmith_DevMenuMaps` | `DataTable` (`WDDevMenuMapsDataTableRow`) | Dev-menu map entry `DevMaps.Vehiclesmith` |
| `Content/UI/Scene/Data/DA_Vehiclesmith_Scene` | `WDUIVehiclesmithSceneData` | Scene root: tabs, pages, data layers, camera |
| `Content/UI/Scene/Data/DA_Vehiclesmith_PersistentActions` | `WDUIItemsmithCancelEditDecalPlacementAction` (13 exports) | Bottom-bar persistent actions (12 entries) |
| `Content/UI/Scene/Data/DT_VehiclesmithPopupOptions` | `DataTable` (`WDUIPopupOptionDataTableRow`) | Popup options; **5 rows** |
| `Content/UI/ItemSelect/Data/DA_Vehiclesmith_AirItemSelect` | `WDUIItemsmithItemSelectData` | Airframe browser (air archetypes) |
| `Content/UI/ItemSelect/Data/DA_Vehiclesmith_LandItemSelect` | `WDUIItemsmithItemSelectData` | Ground browser (land archetypes) |
| `Content/UI/ItemSelect/Data/DA_Vehiclesmith_BrowserList` | `WDUIItemsmithBrowserData` | Browser list layout |
| `Content/UI/ItemSelect/Data/DA_Vehiclesmith_BrowserEntry` | `WDUIItemsmithBrowserItemData` | Browser entry item |
| `Content/UI/VariantSelect/Data/DA_Vehiclesmith_VariantSelect` | `WDUIItemsmithItemSelectData` | Saved-variant (blueprint) picker |
| `Content/UI/BuildOverview/Data/DA_Vehiclesmith_BuildOverview` | `WDUIItemsmithBuildData` | Build page settings |

---

## 2. Root Game Feature

### 2a. Input context mappings
11 input mapping contexts are added, all at priority 0 (`bRegisterWithSettings` is set on the first entry; the others were not checked):

| Context | Purpose (from name) |
|---|---|
| `IMC_Itemsmith` | Scene base |
| `IMC_Itemsmith_PlayerController` | Player controller |
| `IMC_Itemsmith_ItemSelect` | Browser pages (priority 11 on the browser page data) |
| `IMC_Itemsmith_BlueprintSelect` | Variant picker (priority 1 on the variant page) |
| `IMC_Itemsmith_Dev` | Dev controls |
| `IMC_Itemsmith_BasicPaintSelect` | Basic paint |
| `IMC_Itemsmith_Flair`, `_FlairOverview`, `_FlairItemPaint`, `_FlairDecalOverview`, `_FlairDecalSelect` | Flair (paint and decal) sub-modes |

### 2b. Named action map
`InputActionTagsMap` maps **46** `Input.NamedActions.ItemSmith.*` tags to `IA_*` assets. Grouped:

| Group | Tags (examples) | Assets (examples) |
|---|---|---|
| Camera | `RotateView`, `ZoomIn`, `ZoomOut`, `PanCamera.Up/Down/Left/Right`, `FlipView`, `ResetCamera`, `EnableRotateView` | `IA_RotateView`, `IA_ZoomIn`, `IA_ZoomOut`, `IA_PanCameraUp`..., `IA_FlipView`, `IA_ResetCamera`, `IA_AllowRotateView` |
| Node navigation | `Node.Up/Down/Left/Right`, `MoveFocus.Up/Down/Left/Right/Forwards/Backwards`, `SelectNode`, `MovePreview.Up` | `IA_NodeUp`..., `IA_MoveFocusUp`..., `IA_SelectNode`, `IA_MovePreviewUp` |
| Pages and tabs | `Next`, `Previous` (and `.Alternative`), `Tab`, `HeroTitle`, `HideShowUI`, `ExpandStats` | `IA_Itemsmith_Next`, `IA_Itemsmith_Tab`, `IA_Itemsmith_HeroTitle`, `IA_Itemsmith_HideShowUI`, `IA_Itemsmith_ExpandStats` |
| Flair | `FlairOverview.EnterPaint`, `FlairOverview.EnterDecals`, `Flair.ApplyPaint`, `Flair.ClearDecalLayer`, `Flair.EditDecalPlacement`, `Flair.CancelEditDecalPlacement`, `Flair.ClearPaint` | `IA_Itemsmith_FlairOverview_EnterPaint`, `IA_Itemsmith_ApplyPaint`, ... |
| Blueprint | `RemoveBlueprint`, `SaveBlueprint`, `TestingGround` | `IA_Itemsmith_RemoveBlueprint`, `IA_Itemsmith_SaveBlueprint`, `IA_Itemsmith_TestingGround` |

Full list is 46 entries; the table is abbreviated.

### 2c. Data registry sources
One `GameFeatureAction_DataRegistrySource` adds two sources:

| Registry | Data table |
|---|---|
| `DevMenuMapsData` | `DT_Vehiclesmith_DevMenuMaps` (client source on, server source off) |
| `UISceneData_Frontend` | `DT_SceneData_Frontend_Vehiclesmith` |

---

## 3. Frontend Scene Entry (`DT_SceneData_Frontend_Vehiclesmith`)

| Field | Value |
|---|---|
| Row | `UI.Scene.Frontend.Vehiclesmith` |
| Input mode | `EWDInputMode::UI` |
| Reset focus on enter | true |
| Should block back | false |
| Should preload | false |
| Focusable | true |
| Layer / Z-order | `EWDWidgetLayer::Normal` / 1 |
| Widget class | `/Vehiclesmith/UI/Scene/W_VehiclesmithScene` |
| View model | `WDUIVehiclesmithSceneViewModel` on `DA_Vehiclesmith_Scene` |
| Show scene title / back button / seasonal countdown | all false |

---

## 4. Dev Menu Map (`DT_Vehiclesmith_DevMenuMaps`)

| Field | Value |
|---|---|
| Row | `DevMaps.Vehiclesmith` |
| Map name | "Vehiclesmith" |
| Map to load | `/Vehiclesmith/Maps/Vehiclesmith_Main_P` |
| Loading screen | `W_VehiclesmithLoadingScreen` |

---

## 5. Scene Root (`DA_Vehiclesmith_Scene`)

### 5a. Tabs and type

| Field | Value |
|---|---|
| Item system type | `EWDUIItemsmithType::Vehiclesmith` |
| Land tab text | set (`LandTabText`; its string key was not extracted) |
| Air tab text | `Vehiclesmith.Tab.Air` |
| Build tab text | `Itemsmith.Build.Title` |
| Flair tab text | `Itemsmith.Flair.Title` |
| Environment option -> family tag | Air -> `Vehicle.Variant.Air`; Land -> `Vehicle.Variant.Land` |
| Default item-family background | `Vehicle.Variant.Land` |

### 5b. Pages

| Page | Widget class | Scene widgets shown |
|---|---|---|
| `ItemSelect` | `W_Itemsmith_ItemSelectGrid` | (browser) |
| `Build` | `W_Itemsmith_Build` | `BuildFlair`, `Stats`, `BaseInfo`, `HeroTitle`, `NavigationBar` (5) |
| `Variants` | `W_Itemsmith_ItemSelectGrid` | `Stats`, `BaseInfo`, `HeroTitle`, `NavigationBar` (4) |

### 5c. Data layers per family

| Family | Background data layer | Test-drive data layer |
|---|---|---|
| `Vehicle.Variant.Land` | `DL_Vehiclesmith_Garage_Background` | `DL_Vehiclesmith_Land_TestDrive` |
| `Vehicle.Variant.Air` | `DL_Vehiclesmith_Hangar_Background` | `DL_Vehiclesmith_Air_TestDrive` |

### 5d. Camera, controls and misc

| Field | Value |
|---|---|
| Dpad controls angle | 55 |
| Scene mapping context | `IMC_Itemsmith` |
| Dev controls mapping context | `IMC_Itemsmith_Dev` |
| Persistent-action data | `DA_Vehiclesmith_PersistentActions` |
| Popup data table | `DT_VehiclesmithPopupOptions` (5 rows, see the Season 02 update) |

---

## 6. Persistent Actions (bottom bar, `DA_Vehiclesmith_PersistentActions`)

12 entries. Left-aligned (`EWDUIPersistentActionAlignment::Left`) and right-aligned (`Right`):

| Alignment | Action tag |
|---|---|
| Left | `Itemsmith.Actions.Persistent.Favourite` |
| Left | `Itemsmith.Actions.Persistent.DeleteVariant` |
| Left | `Itemsmith.Actions.Persistent.TestingGround` |
| Left | `Itemsmith.Actions.Persistent.HideUI` |
| Left | `Itemsmith.Actions.Persistent.RestoreUI` |
| Left | `Itemsmith.Actions.Persistent.SaveVariant` |
| Left | `Itemsmith.Actions.Persistent.FavouriteVariant` |
| Left | `Itemsmith.Actions.Persistent.FavouritePaint` |
| Right | `Itemsmith.Actions.Persistent.ClearDecalLayer` |
| Right | `Itemsmith.Actions.Persistent.EditDecalPlacement` |
| Right | `Itemsmith.Actions.Persistent.CancelEditDecalPlacement` |
| Right | `Itemsmith.Actions.Persistent.ClearPaint` |

Display strings come from `STRINGS_Itemsmith_PersistentActions` and `STRINGS_Vehiclesmith_PersistentActions` (the test-drive action uses the Vehiclesmith table, key `Vehiclesmith.Actions.TestDrive`).

---

## 7. Browser Pages

### 7a. Air browser (`DA_Vehiclesmith_AirItemSelect`)

| Field | Value |
|---|---|
| Default archetype | `Vehicle.Archetype.Air.Rotary` |
| Camera mode | `EItemsmithCameraMode::FixedSideOn` |
| Camera focus offset | (0, 0, 5.5) |
| Input mapping context | `IMC_Itemsmith_ItemSelect`, priority 11 |
| Browser filters | Favourited-archetype filter, plus archetype filter(s) |

### 7b. Land browser (`DA_Vehiclesmith_LandItemSelect`)

| Field | Value |
|---|---|
| Default archetype | `Vehicle.Archetype.Land.Wheeled` |
| Camera mode | `FixedSideOn` |
| Input mapping context | `IMC_Itemsmith_ItemSelect`, priority 11 |
| Browser filters | Archetype `Vehicle.Archetype.Land.Wheeled`, archetype `Vehicle.Archetype.Land.Tracked`, Favourited archetype `Vehicle.Archetype.Land` |

### 7c. Variant picker (`DA_Vehiclesmith_VariantSelect`)

| Field | Value |
|---|---|
| Page type | `EWDUIItemsmithPages::Variants` |
| Default archetype | `Vehicle.Archetype` |
| Camera mode | `FixedSideOn`, focus offset (0, 0, 5.5) |
| Input mapping context | `IMC_Itemsmith_BlueprintSelect`, priority 1 |
| Browser filters | Favourited variants (`Itemsmith.Variants.Tabs.Favourite`); Saved variants (`Itemsmith.Variants.Tabs.Saved`), with "create new" button tag `Itemsmith.Variants.CreateNewButton` |

### 7d. Browser list and entry

| Field | Value |
|---|---|
| Entry view model | `WDUIItemsmithBrowserEntryViewModel` on `DA_Vehiclesmith_BrowserEntry` |
| Entry width x height | **270 x 125** |
| Items per page | **6** |
| Entry widget | `W_ItemsmithBrowserEntry` |
| Entry icon type | `UI.Icon.Vendor` |
| Entry icon stretch | `ScaleToFitX` |
| Default persistent actions on entries | `Itemsmith.Actions.Persistent.Favourite` |

---

## 8. Build Overview (`DA_Vehiclesmith_BuildOverview`)

| Field | Value |
|---|---|
| Input mapping context priority | 11 |

Only one property is set in the export. The build page widgets come from the scene's `Build` page preference (section 5b).

---

## 9. How Values Combine

This plugin does not change vehicle stats. What it does:

- **Archetype filter** narrows the browser to one vehicle family (air rotary, land wheeled, land tracked). The default archetype is the first thing a player sees.
- **Environment option** picks the family (air or land), which then sets the background and test-drive data layer (section 5c).
- **Persistent actions** appear in the bottom bar, aligned left or right by the table in section 6.

---

## 10. Still Not Pulled / Limitations

- **Vehicle stats and part lists** are not here. They are defined in the vehicle category (see the Vehicles reference).
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **String and icon assets** (`STRINGS_Vehiclesmith_*`, `W_VehiclesmithScene`, `T_UI_*`) are referenced by key or path. The text itself is not in this export.
- **Lists of variant and filter ids** beyond the ones above (for example every `Vehicle.Archetype.*` tag) are not enumerated here.
- **The 46 named-action entries** are summarised by group in section 2b rather than listed one by one.
- **Input bindings** for the `IMC_Itemsmith_*` contexts are in their own assets, not in this plugin folder. Their key assignments are not covered here.
- **Data layer and map assets** (`DL_Vehiclesmith_*`, `Vehiclesmith_Main_P`) are referenced by path only.
