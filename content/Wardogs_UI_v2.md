---
title: "UI"
redirect_from: ["/Wardogs_UI_v2.html", "/Wardogs_UI_v2"]
parent: "World, Visuals & Audio"
description: "Inventory of the Category, Minimap and World Textures, Map and Minimap Trackers, Ping Wheel"
---

# Wardogs — UI Data Reference
*Extracted from cooked game data ([`Wardogs/Content/UI`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI), 605 JSON files holding 793 export blocks: 501 UDataAsset, 188 UObject, 92 UDataTable, 11 curve assets, 1 common input table). Values are as exported; nothing here was checked in-game. Multi-export files were split on their `--- export:` headers before parsing.*

> **Scope note:** this is the UI-layer data: HUD trackers and feeds, map and minimap setup, ping and radial wheels, vendor and inventory grids, tooltips, settings display, frontend scenes, localisation-tag tables, and UI audio. Gameplay numbers (cash, XP, weapon stats) live in other categories. Where a UI asset refers to a gameplay tag or entity, the tag is named but its gameplay value is not included here.

---

## Season 02 update (2026-10-15)

- **Size:** the UI export now has 605 JSON files and 793 export blocks (was 586 and 774), including 92 DataTables (was 88).
- **New wager family:** a wager vendor entry, a create-wager panel, an objective selector, a match status scene, a receipt, an in-match HUD and result toasts. See section 8d.
- **New squad tools:** [`DT_SquadIntents`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/ContextDrawer/Tabs/Party/Data/DT_SquadIntents.json) (12 rows, `Squad.Intent.*` tags) and a create-squad popup ([`DA_CreateSquadData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/ContextDrawer/Tabs/Party/Widgets/SquadCreationPopup/Data/DA_CreateSquadData.json)) on the party tab of the context drawer.
- **New shooting-range context drawer:** [`DA_ShootingRange_ContextDrawer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/ContextDrawer/Data/DA_ShootingRange_ContextDrawer.json) and the match scene row `UI.Scene.Match.ContextDrawer` ([`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json)).
- **New frontend assets:** deployment select scene ([`DA_DeploymentSelectScene`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/DeploymentSelect/Data/DA_DeploymentSelectScene.json)), advanced filters and lookup session popups ([`DA_Popup_AdvancedFilter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/FindMatch/Widgets/AdvancedFiltersPopup/Data/DA_Popup_AdvancedFilter.json), [`DA_Popup_LookupSession`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/FindMatch/Widgets/LookupSessionPopup/Data/DA_Popup_LookupSession.json)), and a Gold Exchange entity row ([`DT_EntityData_UI_GoldExchange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/GoldExchange/Data/DT_EntityData_UI_GoldExchange.json)).
- **New chat and vehicle assets:** clan-tag blocklist [`DA_ClanTagProfanityFilter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DA_ClanTagProfanityFilter.json) (17 entries) and vehicle countermeasure asset [`DA_VehicleCountermeasure`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Vehicles/NEWHUD/Countermeasures/Data/DA_VehicleCountermeasure.json).
- **New settings widgets:** [`DA_SettingValue_RetryCommunication`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Widgets/SettingValue/Data/DA_SettingValue_RetryCommunication.json), [`DA_SettingValue_Status`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Widgets/SettingValue/Data/DA_SettingValue_Status.json) and [`DA_Setting_Value_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Widgets/SettingValue/Data/DA_Setting_Value_Default.json). [`DT_SettingTypeUIData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Widgets/SettingValue/Data/DT_SettingTypeUIData.json) goes from 12 to 13 rows (adds `SwitchConfirmed`).
- **Removed:** `DA_VehicleFlares`, `DA_SettingValue_Button` and the two inventory prompt-bar assets (`DA_ItemCard_PromptBarData_Inventory` and `_Gear`). `WDUIButtonPromptsBarData` goes from 12 to 10.
- **Tables that were empty now have rows:** [`DT_PlayerIdentities`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_PlayerIdentities.json) 0 → 5, [`DT_ExperienceServerBrowserTags`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/ServerBrowser/DT_ExperienceServerBrowserTags.json) 0 → 19, [`DT_OnlineRegions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/FindMatch/Data/DT_OnlineRegions.json) 0 → 14, [`DT_ServerBrowserMapTexture`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/FindMatch/Data/DT_ServerBrowserMapTexture.json) 0 → 12, [`DT_PopupButtons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Widgets/Data/DT_PopupButtons.json) 0 → 2.
- **Row count changes:** [`DT_ScopeReticleTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/ScopeReticle/Data/DT_ScopeReticleTypes.json) 15 → 17, [`DT_VendorTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Data/DT_VendorTypes.json) 3 → 4 (adds `Vendor.Type.Wager`), [`DT_PopupTypes_Features`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Data/DT_PopupTypes_Features.json) 13 → 14, [`DT_TooltipData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Tooltips/Data/DT_TooltipData.json) 33 → 34, [`DT_Calibers_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_Calibers_TaggedIcons.json) 33 → 34, [`DT_EntityData_UI_Items`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Items.json) 295 → 296, [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) 24 → 25.
- **Tracker fields:** `Duration` is no longer exported on [`DA_Tracker_Map_HitMarker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Widgets/Trackers/Data/DA_Tracker_Map_HitMarker.json) (was 150) or [`DA_Tracker_Spatial_AssistanceRequest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_AssistanceRequest.json) (was 20). The `RemovalTime` of 10 on [`DA_MaterialTrackerData_AssistanceRequest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Map_Optimisation/Data/DA_MaterialTrackerData_AssistanceRequest.json) is gone. [`DA_SpatialTrackers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Data/DA_SpatialTrackers.json) keeps its 0.6 value, now under an unnamed field.
- **Ping requests:** `ChannelType` is set on [`DA_PingAction_Request_Dropoff`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Requests/DA_PingAction_Request_Dropoff.json) (`Vehicle`) and on the Fuel and Supplies request assets (`Team`).
- **Spelling in strings:** some UI strings moved to US spelling, for example "Optimised" → "Optimized" in [`DT_EntityData_UI_Items`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Items.json) and "cancelled" → "canceled" in [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json).

Full before/after list: [Season 2 Changes → World, Visuals & Audio]({{ '/season-2-changes/world-visuals-audio.html' | relative_url }}).

---

## 1. Inventory of the Category

| Top folder | Export blocks | Notes |
|---|---|---|
| [`Features/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Features) | 737 | All screens and HUD elements; see section 1b for the breakdown |
| `Data/` | 39 | Shared tables: entities, tagged icons, audio, scenes, interaction, tag-to-text |
| `Tools/` | 9 | Minimap texture definitions ([`Tools/WorldCapture`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Tools/WorldCapture)) and editor-only tracker data |
| `Shared/` | 4 | Rich-text image tables |
| [`Cursors/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Cursors), `Input/`, [`Prototype/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Prototype) | 4 | Software cursor, common input actions, one prototype |

### 1a. Most common asset types

| Type | Count | What it is |
|---|---|---|
| `DataTable` | 92 | Row tables (see section 13) |
| `WDPingActionAsset` | 35 | One per ping-wheel entry |
| `WDUITutorialsContentData` | 26 | LearnToPlay tab content (all under [`Frontend/LearnToPlay`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Features/Frontend/LearnToPlay)) |
| `WDUIContainerGridData` | 16 | Grid size and label per container view |
| `WDUIRadialWheelSlotTypeDataAsset` | 16 | Radial wheel slot definitions |
| `WDUIMaterialTrackerDataAsset` | 15 | Map material-tracker settings (`Map_Optimisation`) |
| `WDPingAction_SendTextMessage` / `WDPingAction_VoxRequest` | 15 / 15 | Ping action behaviours |
| `WDUIButtonPromptsBarData` | 10 | Button prompt bars |
| `WDUIMapTrackerData` | 12 | Basic map tracker settings |
| `WDUITooltipContainerData` | 10 | Container tooltip layouts |
| `WDUILineOfSightRules` / `WDUIWorldDistanceOpacityRules` | 11 / 10 | Shared rule assets used by trackers and markers |
| `WDMinimapTextureData` | 7 | One per world minimap texture |

### 1b. Export blocks by feature folder

| Folder under [`Features/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Features) | Blocks | Folder under [`Features/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Features) | Blocks |
|---|---|---|---|
| `HUD` | 191 | `Popups` | 11 |
| `Frontend` | 133 | `Scoreboard` | 8 |
| `PingWheel` | 109 | `ContextDrawer`, `DeathRecap` | 9 and 6 |
| `Vendor` | 89 | `DeploymentBoard` | 5 |
| `Tooltips` | 41 | `GameOver` | 4 |
| `Map` | 36 | `PocketWorldRender`, `QuickRestock` | 3 each |
| `Inventory_2_0` | 28 | `AccountBar`, `AdminPanel`, `FactionSelect`, `TVGuided` | 1–2 each |
| `RadialWheel` | 28 | | |
| `Settings` | 23 | `Wagers` | 5 |

---

## 2. Minimap and World Textures

Each `DA_UI_<Map>` asset (`WDMinimapTextureData`) binds a virtual texture to world coordinates. Map files: `Tools/WorldCapture/Textures/<Map>/`.

| Map | Texture | SizeX (px) | WorldUnitsPerPixel | Bounds X (min → max) | Bounds Y (min → max) | UV max |
|---|---|---|---|---|---|---|
| Europe | `T_UI_Europe_VT` | 32,768 | not set | −1,616,000 → 16,000 | −1,616,000 → 16,000 | 1.0 |
| NorthAmerica | `T_UI_NorthAmerica_VT` | 32,768 | not set | −819,200 → 819,200 | −819,200 → 819,200 | 1.0 |
| Russia | `T_UI_Russia_VT` | 32,768 | not set | −1,632,000 → 0 | −2,040,000 → −408,000 | 1.0 |
| Kavkazi | `T_UI_Kavkazi_VT` | 16,384 | 100 | −1,632,000 → 0 | −2,040,000 → −408,000 | 1.0 |
| Gym_Minimal | `T_UI_Gym_Minimal_VT` | 9,803 | 51 | −250,001.7 → 249,998.5 | −245,100.0 → 254,900.0 | 0.598 |
| PCGBuildAutomationTestLevel | `T_UI_PCGBuildAutomationTestLevel_VT` | 4,032 | not set | −100,800 → 100,800 | −100,800 → 100,800 | 0.984 |
| Shooting_Range_4 | `T_UI_Shooting_Range_4_VT` | not set | not set | −100,000 → 100,000 | −100,000 → 100,000 | 0.977 |

Z bounds are present on every map (for example Europe ±164,285.9; Shooting_Range_4 −30,000 → 30,000).

**Derived, not stored:** where `SizeX` and the XY bounds are both present, bounds width ÷ SizeX gives the implied world units per pixel. Europe and Russia give about 49.8, Kavkazi about 99.6 (matching its stored 100), NorthAmerica and PCGBuildAutomationTestLevel exactly 50.0, and Gym_Minimal 51.0 (matching its stored 51). Europe and Russia have no stored `WorldUnitsPerPixel`, so the derived figure is the only one available.

---

## 3. Map and Minimap Trackers

Trackers are registered in [`DT_TrackerData_Minimap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DT_TrackerData_Minimap.json) (17 rows), `DT_TrackerData_Map` (17 rows, tactical map) and [`DT_TrackerData_Spatial`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DT_TrackerData_Spatial.json) (13 rows, world-space markers). Each row binds a `Trackers.Type.*` tag to a tracker class and a widget (`W_Tracker_Map_*` or `W_Tracker_Spatial_*`).

### 3a. Tracker types on the minimap and tactical map

| Tracker tag | Tracker class | Widget family | Recreate on faction change |
|---|---|---|---|
| `Trackers.Type.Character` | `WDUIPersistentDataTracker` | Player | Yes |
| `Trackers.Type.Vehicle` | `WDUIPersistentDataTracker` | Vehicle | Yes |
| `Trackers.Type.StationaryVehicle` | not captured | StationaryVehicle | Yes |
| `Trackers.Type.Spawn` | `WDUIPersistentDataTracker` | Spawn | Yes |
| `Trackers.Type.SafeZone` | `WDUIPersistentDataTracker` | SafeZone | Yes |
| `Trackers.Type.Vendor` | `WDUIPersistentDataTracker` | Vendor | Yes |
| `Trackers.Type.DeploymentBoard` | `WDUIPersistentDataTracker` | DeploymentBoard | Yes |
| `Trackers.Type.RefuelStation` | `WDUIPersistentDataTracker` | FuelStation | **No** |
| `Trackers.Type.Corpse` | `WDUIStaticTransformTracker` | Corpse | Yes |
| `Trackers.Type.Deployable` | `WDUIPersistentDataTracker` | Deployable (requires `Id.Item`) | Yes |
| `Trackers.Type.SupplyCrate` / `SupplyPallet` | `WDUIPersistentDataTracker` | SupplyCrate / SupplyPallet | Yes |
| `Trackers.Type.AssistanceRequest` | `WDUIPersistentDataTracker` | AssistanceRequest | Yes |
| `Trackers.Type.Ping` | `WDUIPingTracker` | Ping | Yes |
| `Trackers.Type.Ping.Contextual` | `WDUIPingTracker` | Contextual | Yes |
| `Trackers.Type.Ping.Contextual.MarkCoordinates` | `WDUIPingTracker` | Marker | Yes |
| `Trackers.Type.HitMarker` | `WDUIPersistentDataTracker` | HitMarker | Yes |

On the minimap table, four trackers require gameplay tags: `Character`, `Vehicle` and `StationaryVehicle` need their `*.Data` and `*.Transforms` tags (`Vehicle` and `StationaryVehicle` also need `Vehicle`), and `Deployable` needs `Id.Item` and `Trackers.Type.Deployable`. All other rows have no required tags.

### 3b. Per-tracker display settings (map variants)

| Asset | Type | ZOrder | Other notable values |
|---|---|---|---|
| [`DA_Tracker_Minimap_Spawn`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_Spawn.json) | WDUIMapTrackerData | 1 | — |
| [`DA_Tracker_Minimap_Corpse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_Corpse.json) | WDUITimedMapTrackerData | 10 | — |
| [`DA_Tracker_Minimap_DeploymentBoard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_DeploymentBoard.json) | WDUIMapTrackerData | 20 | Default tracker icon set |
| [`DA_Tracker_Minimap_Vendor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_Vendor.json) | WDUIVendorMapTrackerData | 20 | `VendorTextures` ×2 |
| [`DA_Tracker_Minimap_Vehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_Vehicle.json) | WDUIVehicleMapTrackerData | 25 | `OccupantsTextFormat`, 4 assistance-request textures |
| [`DA_Tracker_Minimap_Ping`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_Ping.json) | WDUIPingMapTrackerData | 40 | 2 ping colours |
| [`DA_Tracker_Minimap_AssistanceRequestPing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_AssistanceRequestPing.json) | WDUIAssistanceRequestMapTrackerData | 40 | 1 texture, 1 ping colour, 1 tracker exception |
| [`DA_Tracker_Minimap_ContextualPing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_ContextualPing.json) | WDUIContextualMapTrackerData | 40 | 6 textures and colours |
| [`DA_Tracker_Minimap_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DA_Tracker_Minimap_Player.json) | WDUIPlayerMapTrackerData | 80 | `DefaultTexture` = `T_UI_FriendlyMarker_Map_Icon`, `SelfOrSquadTexture` = `T_UI_PlayerMarker_Map_Icon`; 9 assistance-request and 10 acknowledged textures |
| [`DA_Tracker_Map_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Widgets/Trackers/Data/DA_Tracker_Map_Player.json) (tactical) | WDUIPlayerMapTrackerData | — | `DefaultIconScale` 0.75, `LowHealthColor`, `OverHealHealthColor` |
| [`DA_Tracker_Map_HitMarker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Widgets/Trackers/Data/DA_Tracker_Map_HitMarker.json) | WDUITimedMapTrackerData | 40 | — |

**Material-tracker removal times** ([`Features/Map/Map_Optimisation`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Features/Map/Map_Optimisation), 15 assets): `RemovalTime` = **10** on Corpse, Ping and ContextualPing. The AssistanceRequest asset no longer exports a removal time, and the others have none. Every one carries a `ZoomScaleCurve`.

### 3c. Spatial (world-space) trackers

| Asset | Type | Key values |
|---|---|---|
| [`DA_SpatialTrackers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Data/DA_SpatialTrackers.json) | WDUISpatialTrackersData | an unnamed field (0.6); 6 `WorldDistanceScoreMultipliers` |
| [`DA_Tracker_Spatial_AssistanceRequest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_AssistanceRequest.json) | WDUIAssistanceRequestSpatialTrackerData | `StalkMaxYSize` 300, `StalkSizeChangeRate` 1500, `PingScaleMaxDistance` 10, `ZOrder` 3 |
| [`DA_Tracker_Spatial_ContextualPing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_ContextualPing.json) | WDUIContextualPingSpatialTrackerData | `StalkMaxYSize` 300, `StalkSizeChangeRate` 1500, `PingScaleMaxDistance` 10 |
| [`DA_Tracker_Spatial_Ping`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_Ping.json) | WDUIPingSpatialTrackerData | `StalkMinYSize` 0, `StalkMaxYSize` 0, `StalkSizeChangeRate` 1500, `PingScaleMaxDistance` 10 |
| [`DA_Tracker_Spatial_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_Player.json) | WDUIPlayerSpatialTrackerData | `bUseOcclusionFade` True, `OcclusionFadeDuration` 0.5 |
| [`DA_Tracker_Spatial_Vehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_Vehicle.json) | WDUIVehicleSpatialTrackerData | `bHideIfDrivenByLocalPlayer` True, `bUseOcclusionFade` True, fade 0.5 |
| `DA_Tracker_Spatial_Vehicle_LockOn` | WDUISpatialTrackerData | `bUseOcclusionFade` True, fade 0.5 |
| [`DA_Tracker_Spatial_ActiveZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DA_Tracker_Spatial_ActiveZone.json) | WDUIActiveZoneData | `ValueSmoothingSpeed` 0.5 |
| `DA_Tracker_Spatial_Interactable_*` (2) | WDUIInteractableActorData | Second variant is screen-clamped |

Spatial `RuleSets` and `DistanceRulesets` reference shared rule assets (section 9). The meaning of the `Stalk*` fields is inferred from their names and was not confirmed.

---

## 4. Ping Wheel

The ping wheel has 35 entries in five categories. Each entry is one `DT_PingActions_*` row that points to one `WDPingActionAsset`.

| Category table | Rows | Category tag | Preferred page |
|---|---|---|---|
| `DT_PingActions_Emote` | 10 | not captured | not captured |
| [`DT_PingActions_Orders`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Orders/DT_PingActions_Orders.json) | 5 | `UI.Features.PingWheel.Category.Squad` | 2 |
| [`DT_PingActions_Request`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Requests/DT_PingActions_Request.json) | 10 | `UI.Features.PingWheel.Category.Requests` | 1 |
| [`DT_PingActions_Social`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Social/DT_PingActions_Social.json) | 5 | not captured | not captured |
| [`DT_PingActions_Squad`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Squad/DT_PingActions_Squad.json) | 5 | not captured | not captured |

### 4a. Orders (Squad category, page 2)

| Action | Slot | Icon |
|---|---|---|
| Fortify | 1 | `T_UI_Icon_PingWheel_fortify` |
| Defend | 2 | `T_UI_Icon_PingWheel_Defend_64x64` |
| Attack | 3 | `T_UI_Icon_PingWheel_Attack_64x64` |
| FallBack | 4 | `T_UI_Icon_PingWheel_FallBack_64x64` |
| Regroup | 5 | `T_UI_Icon_PingWheel_Regroup_64x64` |

### 4b. Requests (page 1) and their gating

| Action | Required player-state tag | Blocked player-state tag |
|---|---|---|
| Backup | — | Driver |
| Ammo | — | Driver |
| Healing | — | Driver |
| Supplies | — | — |
| Pickup | — | ActivePassenger, and others |
| Dropoff | ActivePassenger, Gunner, and others | not captured |
| Repair | Driver | — |
| Refueling | Driver | — |
| GetIn | Driver | — |
| GetOut | Driver | — |

`bRequestPlayerMapCoordinates` is True on Backup, Fuel, Healing, Pickup, Repair and Supplies. It is not set on Dropoff, GetIn, GetOut or Ammo, as far as the digest shows.

### 4c. Action asset behaviours

| Asset class | Count | Fields that vary |
|---|---|---|
| `WDPingActionAsset` | 35 | `Text`, `Icon`, `Actions` (values 1–4), `NonTriggerableDescriptions` (1–2 items), `LockedDescription` (21 of 35), `bIsWorkInProgress`, `bRequestPlayerMapCoordinates` |
| `WDPingAction_SendTextMessage` | 15 | `ChannelType`, `PingActionChatLocText` |
| `WDPingAction_VoxRequest` | 15 | `GameplayCueTag` |
| `WDPingAction_Emote` | 10 | Emote reference |
| `WDPingAction_CheckSquadStatus` | 10 | `bCheckIsSquadLeader` True on 5 |
| `WDPingAction_ShowSpatialMarker` | 6 | `SpatialMarkerTag` |
| `WDPingAction_AssistanceRequest_*` | 10 | One per request type (Ammo, Backup, Dropoff, Refueling, GetIn, GetOut, Healing, Pickup, Repair, Supplies). `ChannelType` is `Vehicle` on Dropoff and `Team` on Refueling and Supplies |

Emote icons include Assault, Move_Up, Point, Surrender_Drop, Halt, Middle_Finger, Paper, Rock, Scissors and Shh. Social icons are the Nice, No, Sorry, Thanks and Yes set.

---

## 5. Radial Wheels

| Wheel tag | Display name / title | Close action | Slot table |
|---|---|---|---|
| `UI.RadialWheel.Equipment` | "TAC-VEST" | `UI.Action.Feature.RadialWheel.Equipment.ToggleScene` | [`DT_RadialWheelSlotType_EquipmentData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/EquipmentWheel/DT_RadialWheelSlotType_EquipmentData.json) (7 rows) |
| `UI.RadialWheel.VoiceChat` | "SELECT VOICE CHANNEL" (description: "Current - {TalkingChannel}") | `UI.Action.Feature.RadialWheel.VoiceChat.ToggleScene` | [`DT_RadialWheelSlotType_VoiceChatData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/VoiceChat/DT_RadialWheelSlotType_VoiceChatData.json) (2 rows) |

[`DT_RadialWheelSlotType_Vehicles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/Vehicles/DT_RadialWheelSlotType_Vehicles.json) has 9 rows. Slot-type assets cover empty and locked states: `EmptySlotTitleText`, `EmptySlotDescriptionText`, `LockedSlotTitleText`, `LockedSlotDescriptionText`, `EmptyTextureScale`, `LockedTextureScale`, and `QuantityTextAngleOverride`. Voice-channel slot assets also hold `ChannelType`, `Action`, `Icon` and `IconScale`.

---

## 6. Feeds and Notifications

### 6a. Reward feed ([`DA_RewardFeed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DA_RewardFeed.json), [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json), 52 rows)

| Setting | Value |
|---|---|
| `InitialExpiryTime` (feed) | 6 |
| `XPTextFormat` (entry) | `{XPValue}XP` |
| Action table | 52 rows, each with `DisplayText`, `bIsTip` and an optional `AudioEventTag` |

Sample rows (tag → text):

| Tag (short) | Feed text | Audio tag |
|---|---|---|
| `MatchScore.KillScore` | Enemy Player Killed | — |
| `MatchScore.DownedScore` | Enemy Player Downed | — |
| `MatchScore.HealedScore` | Friendly Player Healed | `Audio.Event.UX.Cash.HealedScore` |
| `MatchScore.RevivedScore` | Friendly Player Revived | `Audio.Event.UX.Cash.RevivedScore` |
| `MatchScore.VehicleKillScore` | Enemy Vehicle Destroyed | `Audio.Event.UX.Cash.DestroyedVehicle` |
| `MatchScore.DamageAssist.Player` | Enemy Kill Assist | `Audio.Event.UX.Combat.KillAssist` |
| `MatchScore.SupplyCrateKillScore` | Destroyed Enemy Supply Crate | `Audio.Event.UX.Cash.DestroyedVehicle` |
| `MatchScore.TowerCaptured` | Tower Captured | `Audio.Event.UX.Cash.BuiltScore` |
| `MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered` | Spawn Vehicle Delivered | `Audio.Event.UX.Cash.DeliveredSpawnVehicle` |
| `MatchScore.DropOffPassengerSurvived` | Passenger Survived | `Audio.Event.UX.Cash.PassengerSurvived` |
| `MatchScore.SchematicBuiltScore.FinalBuilder` | Finished Building | `Audio.Event.UX.Cash.BuiltScore` |

The remaining rows cover friendly-fire and destroyed-friendly variants, schematic and FOB build steps, magnet zone states, deployables, supply crates and transport assists.

### 6b. Challenges feed ([`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json), 68 rows)

Rows are keyed `Challenges.Rewards.*`. Some carry `ConditionalExpressions` on context tags. For example, `Challenges.Rewards.PlayerKill` shows **"No Value Kill"** when the context is `Challenges.Context.RessedByEnemy`, which is the feed-side counterpart of the ressed-by-enemy penalty. `Challenges.Rewards.PlayerKill.CrewAssist` shows "Kill Assist" and `.LogisticAssist` shows "Deployed Player Assist".

### 6c. Tipping

[`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json) (4 rows, reward-feed row type). [`DA_TippingData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DA_TippingData.json) `TipPromptDuration` = 8.

### 6d. Killfeed ([`DA_Killfeed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Killfeed/Data/DA_Killfeed.json), [`DA_KillfeedEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Killfeed/Widgets/KillfeedEntry/Data/DA_KillfeedEntry.json))

| Setting | Value |
|---|---|
| `MaximumEntries` | 5 |
| `EntryDuration` | 10 (unit not stated; likely seconds) |
| Preloaded kill-context icons | 8: Headshot, Falling, Default, RoadKill, Penetration, Ricochet, WeaponMelee, RangedWeaponMelee |
| `DistanceTextFormat` | `[{Distance} {Unit}]` |
| `DisconnectedPlayerText` | "Disconnected Player" |

### 6e. Event feed ([`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json), 34 rows; [`DA_EventFeedEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Widgets/EventFeedEntry/Data/DA_EventFeedEntry.json))

| Setting | Value |
|---|---|
| Entry `EntryDuration` | 5 |
| Each type has | `DisplayTextSelf`, `DisplayTextOther`, `MaxDistanceForTeamEvents` |
| Acknowledge icon | `T_UI_Icon_PingWheel_Affirmative_64x64` |

Examples: `Type.Acknowledgement` ("{RequestPlayerName} acknowledged <Highlight>{PlayerName}</>'s request"), `Type.Safezone.Exit` ("{RequestPlayerName} have left the Safe Zone"), `Type.Request.Cancelled`.

### 6f. Feedback and chat

| Asset | Key values |
|---|---|
| [`DA_HUDFeedback`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/HUDFeedback/Data/DA_HUDFeedback.json) | `EntryDuration` 4.5 |
| [`DA_Chatbox`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DA_Chatbox.json) | `MaximumCachedMessages` 50, `DisplayDuration` 10, `MaxCharactersPerMessage` 64, mention prefix `@`, profanity filter [`DA_ProfanityFilter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DA_ProfanityFilter.json) |
| [`DA_ClanTagProfanityFilter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DA_ClanTagProfanityFilter.json) | Clan-tag blocklist (`WDUIProfanityFilter`, 17 entries) |
| Chat channel tags | Player name, mention-me and mention-other links, coordinate link |

---

## 7. HUD Core Elements

| Asset | Type | Key values |
|---|---|---|
| [`DA_Crosshair`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Crosshair/Data/DA_Crosshair.json) | WDUICrosshairData | `Opacity` 0.6, `HairLength` 7.5, `Gap` 0, `SpreadMultiplier` 600, `BuildableCheckRadius` 310, `bShowDot` True, `RevealGraceTime` 0.4, `RevealAnimPlayRate` 1.2, `FallbackCrosshairProjectionDistance` 1000. Hidden during 14 action tags (Sprint, TacSprint, Ladder, Climbing, Mantling, Vaulting, Revive, MeleeBash, Reload, ChamberRound, Swimming, Parachuting, Inspect, Prone.Crawl) and 3 gameplay tags (Vitality.Critical, Vitality.Dead, Vehicle.Role.ActivePassenger) |
| [`DA_Compass`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Compass/Data/DA_Compass.json) | WDUICompassData | 8 cardinal/intercardinal labels at 45° steps (N = 0, E = 90, S = 180, W = 270); `IconSize` 18×18; `FadeStart` 0.4; `bCullPingsAtEdgeOfCompass` True |
| [`DA_FadeOut`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/FadeOut/Data/DA_FadeOut.json) | WDUIFadeOutData | `BlackoutTransitionDurationOut` 3; "Respawning in {Time}..." |
| [`DA_HUDQuickSlots`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/QuickSlots/Data/DA_HUDQuickSlots.json) | WDUIHUDQuickSlotsData | `TimeUntilFadeStarts` 4 |
| [`DA_HUDPrompts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Prompts/Data/DA_HUDPrompts.json) | WDUIHUDPromptsData | `ProneBlockedDisplayTime` 1.2; `bEnableTraversalPrompt` False |
| [`DA_HUDFalling`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Falling/Data/DA_HUDFalling.json) | WDUIHUDFallingData | `MinimumGaugeActivationHeight` 5; `bShowGaugeWhileFallingWithoutParachute` False |
| [`DA_DeathState`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/DeathState/Data/DA_DeathState.json) | WDUIDeathStateData | `TimeBetweenDistanceChecks` 1; `MaxBlackoutOpacity` 1; `MaximumDistanceToConsiderAsNearby` 100 |
| [`DA_EquippedItem`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EquippedItem/Data/DA_EquippedItem.json) | WDUIEquippedItemData | Default magazine, bullet and chamber textures; `EquippedItemNameTextFormat` `{ItemDisplayName} // {ResourceDisplayName} // SN ...` |
| [`DA_ScopeReticle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/ScopeReticle/Data/DA_ScopeReticle.json) | WDUIScopeReticleData | `DeadZoneSize` 0, `DampenZoneSize` 0 (17 reticle types in [`DT_ScopeReticleTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/ScopeReticle/Data/DT_ScopeReticleTypes.json)) |
| [`DA_WeightDisplay`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Shared/Widgets/WeightDisplay/Data/DA_WeightDisplay.json) | WDUIWeightDisplayData | `HeaviestWeightBuffer` 15 |
| `DA_VehicleFuelHealth` | WDUIVehicleFuelHealthData | `LowFuelThreshold` 0.2 |
| [`DA_Passengers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Passengers/Data/DA_Passengers.json) | WDUIPassengersData | "PASSENGERS [{Occupants}/{Capacity}]"; `PassengerCollapseThreshold` 13 |
| [`DA_KillfeedEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Killfeed/Widgets/KillfeedEntry/Data/DA_KillfeedEntry.json) | WDUIKillfeedEntryData | See 6d |

Vehicle HUD assets (`WDUIVehicleStateData` ×2, `WDUIVehicleWeaponAmmoData` ×2, `WDUIVehicleReloadingMinigameData`, `WDUIVehicleCountermeasureData`, `WDUIVehicleThreatIndicatorData`, and others) hold icon sets, colour thresholds and a reloading minigame that uses quadrant-based inputs. Their numeric detail was not extracted (section 14).

---

## 8. Vendor, Inventory and Container Grids

### 8a. Container grid sizes (`WDUIContainerGridData`, 16 assets)

| Asset | Min W×H | Max W×H | Notes |
|---|---|---|---|
| [`DA_ContainerGrid_Inventory_Slot`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Inventory_2_0/Widgets/ContainerGrid/Data/DA_ContainerGrid_Inventory_Slot.json) | 1×1 | 1×1 | Single-slot equipment |
| [`DA_ContainerGrid_Inventory_Slot_Weapon`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Inventory_2_0/Widgets/ContainerGrid/Data/DA_ContainerGrid_Inventory_Slot_Weapon.json) | 1×1 | 1×1 | |
| [`DA_ContainerGrid_Inventory_Slot_Vest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Inventory_2_0/Widgets/ContainerGrid/Data/DA_ContainerGrid_Inventory_Slot_Vest.json) | 1×1 | 1×1 | |
| [`DA_ContainerGrid_Inventory_Slot_Attachment`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Inventory_2_0/Widgets/ContainerGrid/Data/DA_ContainerGrid_Inventory_Slot_Attachment.json) | 1×1 | 1×1 | |
| [`DA_ContainerGrid_Vendor_Backpack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/ContainerGrid/Data/DA_ContainerGrid_Vendor_Backpack.json) | 9×2 | 9×2 | Label "Backpack"; fixed-size grid |
| [`DA_ContainerGrid_Vendor_Slot`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/ContainerGrid/Data/DA_ContainerGrid_Vendor_Slot.json) | 1×1 | 1×2 | Label "Backpack" |
| [`DA_ContainerGrid_Vendor_Slot_Weapon`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/ContainerGrid/Data/DA_ContainerGrid_Vendor_Slot_Weapon.json) | 1×1 | 1×2 | Label "Backpack" |
| [`DA_ContainerGrid_Vendor_Slot_Attachment`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/ContainerGrid/Data/DA_ContainerGrid_Vendor_Slot_Attachment.json) | 1×1 | 1×1 | |

Subslot grids (Backpack, Storage, Vest, Vault) and the vehicle-inventory grid carry labels and `bUseItemAsSlotName` settings but no size bounds.

### 8b. Vendor panels and types

[`DT_VendorTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Data/DT_VendorTypes.json) has 4 rows:

| Vendor type | Default panel | Swap to default on close | Panel buttons |
|---|---|---|---|
| `Vendor.Type.Equipment` | `Vendor.Panel.Overview` | True | Overview, and others |
| `Vendor.Type.Vehicle` | — | False | Land (50×50 minimum size), and others |
| `Vendor.Type.Garage` | `Vendor.Panel.Garage.Overview` | True | Overview, and others |
| `Vendor.Type.Wager` | `Vendor.Category.Wagers` | False | CREATE (120×50 minimum size) |

Panel data assets: `WDUIVendorPanelData_Utility` (2), `_Gear`, `_Weapons`, `_Garage`, `_GarageOverview`, `_GarageSupplyCrate`, `_Overview`, `_Vehicles`. The wager create panel is `WDUIVendorPanelData_Wagers` ([`DA_VendorPanel_Wagers_Create`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/VendorPanel/Data/DA_VendorPanel_Wagers_Create.json)). Utility panels set `bTryPurchaseEvenIfDesiredSlotIsUnavailable` True and `bCheckForSubslotSupportWhenFilteringPurchases` True, and show "CAP. {Amount}/{Capacity}".

### 8c. Purchasable item cards

Purchasable card assets (`WDUIPurchasableItemCardData_Vendor`, 5) share these texts:

| Text key | Value |
|---|---|
| `MultipleItemsPriceTooltipFormat` | `{Value} per Item` |
| `UnlockLevelTextFormat` | `{Role} Lvl {Level}` (vehicles and some gear); "No storage space available" (the generic purchasable card) |
| `InsufficientFundsWarning` | "Not Enough Cash" |
| `ItemAmountType` | `EWDUIItemAmountType::InInventory` |

Vehicle vendor ([`DA_VehicleVendor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Data/DA_VehicleVendor.json)): `VehicleTypeFormat` `{Subcategory} Vehicle`, `bFlushInputOnEnter` True.

### 8d. Wagers (new in Season 02)

Wagers are placed at a vendor, tracked on a match status scene, and reported by a HUD element and toasts.

| Asset | Type | Key values |
|---|---|---|
| [`DA_WagerVendor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Data/DA_WagerVendor.json) | WDUIVendorData_Rework | Opens from the `Action.Player.AccessWagerVendor` action; equipment vendor open and close audio |
| [`DA_VendorPanel_Wagers_Create`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/VendorPanel/Data/DA_VendorPanel_Wagers_Create.json) | WDUIVendorPanelData_Wagers | Create-wager panel (`Vendor.Category.Wagers`): "Create new wager", "Unlock wagers", "Requires Wardog level {Level}", "Minimum stake is {Amount}", "Not enough cash - you have {Amount}" |
| [`DA_Wagers_ObjectiveSelector`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Widgets/Wagers/WagerObjectiveSelector/Data/DA_Wagers_ObjectiveSelector.json) | WDUIWagerObjectiveSelectorData | Four objective archetypes: Kills, Revives, Drop Offs (`Wager.Archetype.PlayersDelivered`), Destroy Vehicles (`Wager.Archetype.VehiclesDestroyed`) |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) (1 row) | WDSceneDataTableRow | Scene `UI.Scene.Match.WagerStatus`: UI input mode, session scene group |
| [`DA_WagerStatusScene`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Wagers/Status/DA_WagerStatusScene.json) | WDUIWagerStatusSceneData | Hosts the status and receipt view models; close action `UI.Action.Feature.CloseScene` |
| [`DA_WagerStatus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Wagers/Status/DA_WagerStatus.json) | WDUIWagerStatusData | Title "Wager #{Handle}"; states Active, Completed, Failed |
| [`DA_WagerReceipt`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Wagers/Receipt/DA_WagerReceipt.json) | WDUIWagerReceiptData | "Potential return", "Paid", "Stake lost", "No active wager. Visit the wager vendor in spawn." |
| [`DA_WagerHUD`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Wagers/HUD/DA_WagerHUD.json) | WDUIWagerHUDData | In-match wager HUD |
| [`DA_WagerToast`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Wagers/Toast/DA_WagerToast.json) | WDUIWagerToastData | "WAGER COMPLETE", "WAGER FAILED" and "JACKPOT WINNER" toasts; result sounds under `Audio.Event.Vendor.Wager.Result.*` |

---

## 9. Shared Rule Assets

Rule assets are reused across trackers, markers and HUD elements. Counts are the number of assets.

| Rule type | Count | Typical fields |
|---|---|---|
| `WDUILineOfSightRules` | 11 | `SquaredRange` (11), `TraceChannel` (4), `Range` (3), `bUseAdditionalCharacterTraces`, `BlockedOpacity`, `bRequireRenderedComponent` |
| `WDUIWorldDistanceOpacityRules` | 10 | `MaximumVisibleDistance`, `MinimumVisibleDistance`, `FalloffRangeMinimum`/`Maximum`, `MaxOpacity`, `Targets` |
| `WDUIScreenClampingRules` | 9 | `ClampingAsPixels` (5), `ClampingAsPercentage` (4), `bClampByScreenPercentage` |
| `WDUIWorldDistanceScaleRules` | 7 | `DistanceForScalingEnd`, `StartScale`, `EndScale` |
| `WDUIScreenDistanceOpacityRules` | 6 | `MaximumVisibleDistance`, `FalloffRangeMaximum`, `OpacityRange`, `bInvertOpacity` |
| `WDUILocationOffsetRules` | 4 | `Offset`, `bDynamicOffset`, `DynamicOffsetDistanceCurve`, `AttachBone` |
| `WDUIScreenLocationOffsetRules` | 4 | `bOffsetAfterScreenClamping`, `bOffsetByScreenPercentage`, `OffsetAsPercentage` |
| `WDUIContextTextRules` / `WDUINameTextRules` / `WDUIDistanceTextRules` | 4 each (contexts 4, names 4, distance 4) | Text state and rules |
| `WDUIOpacityMultiplierRule` / `WDUIScaleMultiplierRule` | 2 / 1 | `Multiplier`, `Targets` |
| `WDUIFocusFadeInOpacityRules` | 3 | `Targets` |

Trackers reference these by `RuleSets` and `DistanceRulesets` (arrays of 1–7 entries). The exact evaluation order between rules is not known from the data.

---

## 10. Settings, Input and Cursor

| Asset | Key values |
|---|---|
| [`DA_SoftwareCursor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Cursors/Data/DA_SoftwareCursor.json) (`WDUISoftwareCursorData`) | `FallbackCursorSize` 18×21.33; `DeadZoneRadius` 0.15; `AnalogStickResponseCurve` = [`C_CursorAnalogStickResponseCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Cursors/C_CursorAnalogStickResponseCurve.json); `CursorInfoMap` |
| [`DA_DeadZoneAnalogue`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Data/DA_DeadZoneAnalogue.json) | Test readout text "X: {XValue}%, Y: {YValue}%" for both sticks |
| [`DA_DeadZoneTrigger`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Data/DA_DeadZoneTrigger.json) | "Trigger: {Percentage}%" for left and right triggers |
| [`DT_Settings_DisplayData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Data/DT_Settings_DisplayData.json) (15 rows) | Includes gamepad move-stick dead-zone presets: `Preset`, `Centre`, `Axial`, `MaxInput` |
| [`DT_SettingTypeUIData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Widgets/SettingValue/Data/DT_SettingTypeUIData.json) (13 rows) | Display widget types: Numeric, Keybind, InputField, Rotator, Switch, SwitchConfirmed, Dropdown, Hyperlink, Button, JoystickAxis, JoystickAction, Status, RetryCommunication |
| `WDUISettingValueData` (4) | `bCanBeNudged` (2), `bCanBeContinuouslyNudged` (4), `NudgeCurve` (4) |
| `WDUISettingsPanelData` (6), `WDUISettingsData` (1), `WDUIInitialSettingsData` (1) | Settings panel pages, categories and first-run settings |

Common UI input actions are in `UCommonGenericInputActionDataTable` (1 table) and [`DT_UIInputActionData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_UIInputActionData.json) (1 row).

---

## 11. Frontend Scenes, Mastery and Tutorials

### 11a. Scene tables

| Table | Rows | Example scenes |
|---|---|---|
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | 28 | `Logo`, `Photosensitivity`, `Start`, `InitialSettings`, `Home`, `Career`, `Customize` |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | 25 | In-match scenes |
| [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | 1 | Shooting-range context drawer scene (`UI.Scene.Match.ContextDrawer`) |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | 1 | Wager status scene (`UI.Scene.Match.WagerStatus`) |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | 4 | Shared scenes |

Scene fields: `InputMode` (`EWDInputMode::UI`), `bResetFocusOnEnter` (True on the sampled rows), `bShouldBlockBack` (True on `Logo`, `Photosensitivity`, `Start`, `InitialSettings`; False on `Home`, `Career`, `Customize`), `bIsFocusable`.

### 11b. Role skill tree ([`DT_CharacterSkillNodes_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_CharacterSkillNodes_Data.json), 131 rows)

| Role | Nodes |
|---|---|
| Infantry | 29 |
| Recon | 28 |
| Support | 27 |
| Medic | 23 |
| Driver | 12 |
| Pilot | 12 |

Each node has a `FriendlyName` (for example "Medkits have more uses"), a `Description` and a `NodeIcon`. Sample Medic nodes: `BuffApplicationTime`, `BuffDuration.Self`, `ChargeTime.Defibrillator`, `HealthierRevive`, `HealTime.Self`, `IncreaseBleedTime`, `MedicBag`, `ReviveSpeed.Standard`. Driver and Pilot nodes split by vehicle class (Ground Vehicles, Air Vehicles, Mounted MG). Scene titles use `{ROLENAME} MASTERY` and `{PLATFORMNAME} PLATFORM`.

### 11c. LearnToPlay tutorials

All 26 `WDUITutorialsContentData` assets sit under [`Frontend/LearnToPlay/Data/ContentSceneData/TabData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Features/Frontend/LearnToPlay/Data/ContentSceneData/TabData). Tab folders include `Introduction`, `UsingEquipment`, `Vehicles` and `TravelToObjective`. Each carries `MediaPlayer` and `ContentTabData` references.

### 11d. Loading screen tips

[`DT_LoadingScreenTips`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Data/DT_LoadingScreenTips.json) has **110 rows**. Tag prefixes: `Tip.Economy.*`, `Tip.Items.*` (including weapon examples), `Tip.ControlZone.*`.

---

## 12. Entities, Icons and Localisation Tags

| Table | Rows | Role |
|---|---|---|
| [`DT_EntityData_UI_Items`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Items.json) | 296 | UI entity data per `Id.Item.*` (e.g. `Id.Item.Fists`, `Id.Item.Bandage`, `Id.Item.SuperBandage`) |
| [`DT_EntityData_UI_Garage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Garage.json) | 2 | Garage entities |
| [`DT_EntityData_UI_VehicleAmmo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_VehicleAmmo.json) | 5 | Vehicle ammo entities |
| [`DT_EntityData_UI_Misc`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Misc.json) | 1 | Misc entity |
| [`DT_EntityData_UI_GoldExchange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/GoldExchange/Data/DT_EntityData_UI_GoldExchange.json) | 1 | Gold Exchange unlock entity (`Meta.Unlocks.GoldExchange`) |
| [`DT_InteractionContextData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Interaction/DT_InteractionContextData.json) | 86 | Interaction prompt text and condition rules, e.g. `Interaction.Context.Container.Loot` → "Container" |
| [`DT_InteractionContexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_InteractionContexts.json) | 70 | Second interaction table (`BHEntityData_UI` row type) |
| [`DT_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_TaggedIcons.json) | 63 | Inventory slot and general tag icons |
| [`DT_Calibers_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_Calibers_TaggedIcons.json) | 34 | Calibre icons |
| [`DT_CaliberModifiers_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_CaliberModifiers_TaggedIcons.json) | 6 | Calibre modifier icons |
| [`DT_DamageTypes_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_DamageTypes_TaggedIcons.json) | 3 | Fall, Impact, Explosive |
| [`DT_LevelIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_LevelIcons.json) | 7 | Role level icons: Wardog, Driver, Infantry, and others |
| [`DT_TooltipData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Tooltips/Data/DT_TooltipData.json) | 34 | Tooltip widget and view-model mapping |

**Gameplay-tag-to-text tables** ([`Data/GameplayTagsToText`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Data/GameplayTagsToText), 15 tables, 331 rows total): Categories 112, InventorySlots 37, SceneNames 38, Calibers 31, Archetypes 16, Ammunition 14, Roles 13, ServerTags 24, Damage 9, Tooltips 10, Components 7, EventLog 6, Tutorials 5, PlayerStates 5, Prompts 4.

---

## 13. Data Tables (all 92)

Grouped by row type. Row counts from the export.

| Row type (RowStruct) | Tables | Total rows | Covered in |
|---|---|---|---|
| `BHEntityData_UI` | 6 | 375 | Section 12 |
| `WDUIGameplayTagToTextTableRow` | 15 | 331 | Section 12 |
| `WDMetaTreeNodeData_UI` | 1 | 131 | Section 11b |
| `WDRewardFeedActionDataTableRow` | 3 | 124 | Section 6 |
| `WDLoadingScreenTips` | 1 | 110 | Section 11d |
| `WDUITaggedIconRow` | 5 | 108 | Section 12 |
| `WDUIInteractionContextDataTableRow` | 1 | 86 | Section 12 |
| `WDSceneDataTableRow` | 5 | 59 | Section 11a |
| `WDUITrackerDataTableRow` | 4 | 51 | Section 3 |
| `RichImageRow` | 5 | 35 | Not detailed |
| `WDUIPingAction` | 5 | 35 | Section 4 |
| `WDEventFeedActionDataTableRow` | 1 | 34 | Section 6e |
| `WDUITooltipDataTableRow` | 1 | 34 | Section 12 |
| `WDUIActionSoundTableRow` | 1 | 20 | Section 13 notes |
| `WDUIRadialWheelSlotTypeTableRow` | 3 | 18 | Section 5 |
| `WDUITaggedWidgetParamsRow` | 2 | 17 | Not detailed |
| `WDUIPopupTypeDataTableRow` | 2 | 17 | Not detailed |
| `WDUIMaterialTrackerDataTableRow` | 1 | 15 | Section 13 notes |
| `RichTextStyleRow` | 10 | 15 | Not detailed |
| `WDUIScopeReticleType` | 1 | 17 | Section 7 |
| `WDUIUserSettingDisplayDataTableRow` | 1 | 15 | Section 10 |
| `WDUIDeploymentBoardRejectionTableRow` | 1 | 11 | Not detailed |
| `WDUILevelTableRow` | 1 | 7 | Section 12 |
| `WDUIScoreboardStatTableRow` | 1 | 5 | Section 13 notes |
| `WDUIInteractionContextStateDataTableRow` | 1 | 4 | Not detailed |
| `WDPlacementUiTextRecord` | 1 | 3 | Not detailed |
| `WDUIVendorType` | 1 | 4 | Section 8b |
| `WDUIInteractableComponentStateDataTableRow` | 1 | 2 | Not detailed |
| `WDDevMenuMapsDataTableRow` | 1 | 2 | Not detailed |
| `WDUIIndicatorTableRow` | 1 | 2 | Not detailed |
| `WDUIRadialWheelTableRow` | 1 | 2 | Section 5 |
| `WDUIInputActionDataTableRow` | 1 | 1 | Section 10 |
| `SDUINotificationDataRow` | 1 | 1 | Not detailed |
| `WDExperienceServerBrowserTagRow` | 1 | 19 | Not detailed |
| `WDUISquadIntentTableRow` | 1 | 12 | Not detailed |
| `WDServerBrowserRegionData` | 1 | 14 | Not detailed |
| `WDUIServerBrowserMapTextureTableRow` | 1 | 12 | Not detailed |
| `WDPlayerIdentityRow` | 1 | 5 | Not detailed |
| `WDUIPopupButtonDataTableRow` | 1 | 2 | Not detailed |

Counts come from a grouping of all 92 `DataTable` exports by RowStruct. Row types that appear in more than one table are listed once with the combined count.

Notable non-trivial tables:

- [`DT_UIAudioData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Audio/DT_UIAudioData.json) (20 rows, `WDUIActionSoundTableRow`): maps UI tags to MSS sound assets. Several rows have an **empty** `AssetPathName`, so the sound is unset: `UI.Audio.Vendor.Open`, `UI.Audio.Vendor.Close`, `UI.Audio.RewardFeed.CashComboAdd`, `UI.Audio.RewardFeed.CashComboBank`.
- [`DT_MaterialTrackerSettingsData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Trackers/DT_MaterialTrackerSettingsData.json) (15 rows): material-tracker settings, paired with section 3b.
- [`DT_PopupTypes_Features`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Data/DT_PopupTypes_Features.json) (14) and [`DT_PopupTypes_Generic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Data/DT_PopupTypes_Generic.json) (3): popup type definitions.
- [`DT_ScoreboardStats_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Scoreboard/Widgets/Scoreboard/Data/DT_ScoreboardStats_Default.json) (5): default scoreboard columns.
- [`DT_LootedComponentTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Inventory_2_0/Widgets/InventoryComponent/Data/DT_LootedComponentTypes.json) (4): loot-container component widget params.

---

## 14. Curves and Textures

| Asset | Type | Use (from name) |
|---|---|---|
| [`C_CursorAnalogStickResponseCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Cursors/C_CursorAnalogStickResponseCurve.json) | CurveFloat | Cursor analogue-stick response; keys run from (0, ~0) to (1, 1), cubic auto tangents |
| [`C_DynamicLocationOffsetPlayerTracker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/C_DynamicLocationOffsetPlayerTracker.json) / [`C_DynamicLocationOffsetVehicleTracker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/C_DynamicLocationOffsetVehicleTracker.json) | CurveFloat | Dynamic location offset for tracker markers |
| [`CC_SpatialPingTimeline`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Materials/CC_SpatialPingTimeline.json) / [`CC_SpatialPingDangerTimeline`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Materials/CC_SpatialPingDangerTimeline.json) | CurveLinearColor | Spatial ping colour timeline (normal and danger) |
| [`CC_AlphaTime`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Textures/CC_AlphaTime.json) / [`CC_LinesTimeline`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Textures/CC_LinesTimeline.json) / [`CC_PulseTimeline`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Textures/CC_PulseTimeline.json) | CurveLinearColor | HUD animation timelines |
| [`CA_SpatialPingTimeline`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Materials/CA_SpatialPingTimeline.json) / [`CA_SpatialPingDangerTimeline`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Materials/CA_SpatialPingDangerTimeline.json) / [`CA_ThrobberTime`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Textures/CA_ThrobberTime.json) | CurveLinearColorAtlas | Gradient atlases for the same timelines |

Curve key values were not extracted, so the shapes are not documented here.

---

## 15. How the Pieces Connect

- A **tracker** is defined by a row in one of the three tracker tables (section 3). It picks a widget and a data asset. The data asset chooses textures, colours and `ZOrder`, and points to **rule assets** (section 9) that decide opacity, scale, clamping and visibility by distance.
- A **ping** starts from a ping-wheel row (section 4), which gates it by player state. The action asset then decides what is sent: text to a channel, a voice request, a spatial marker or a squad-status check. Pings that place a map coordinate set `bRequestPlayerMapCoordinates`.
- **Feeds** (section 6) match an event tag to display text and an audio tag. Reward-feed rows are keyed by the same `Meta.Progression.Resources.*` tags that the cash and XP tables use.
- **Vendor and inventory** grids (section 8) combine a container-grid size, a layout, an item card and a panel type from [`DT_VendorTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Data/DT_VendorTypes.json).

---

## 16. Still not pulled / limitations

- **Curve keyframes** (section 14) and **`WDUIMaterialTrackerDataAsset` ZoomScaleCurve** values were not extracted. Only the names are listed.
- **Field meanings not confirmed:** `ZOrder` direction (higher drawn on top is inferred from values), `RemovalTime` and `Duration` units (seconds assumed for the 10 values, but not stated), `EntryDuration` units, the `Stalk*` spatial fields, defaults where `bIsWorkInProgress` is omitted, and the `RuleSets` evaluation order. `Actions=[N]` counts entries in an array of action-object references; the full per-ping list and execution semantics remain outside this pass.
- **Partially extracted:** the tactical map's `SmallestViewSize` and `LerpZoomPresetTolerance`; the full list of `Actions` for each ping action; the `Challenges.Rewards.*` condition tags; the vehicle-HUD assets in section 7.
- **Not covered in detail:** `DT_RichText_Style_*` and `DT_RichImg_*` styling rows (only counted); [`DT_CustomEmojis`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DT_CustomEmojis.json) and tooltip emojis (only counted); `DA_Settings*` category contents; `WDUIMockInvestmentCardData` and other mock or prototype assets; loading-screen tip text.
- **Multi-export files:** 60 files contain more than one export block. They are parsed correctly by splitting on the `--- export:` header, but sub-objects such as `WDUIViewModelExtension_HideReasons_0` appear in the same file and were counted separately.
- Localised strings are taken from `SourceString` (the English source text). Localised builds may differ.
- Nothing in this document was verified against live gameplay or the running UI.

---

*Source directory: [`Wardogs/Content/UI`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI).*
