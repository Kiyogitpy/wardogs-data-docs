---
title: "PvE (feature)"
redirect_from: ["/Wardogs_GameFeatures_PvE_v2.html", "/Wardogs_GameFeatures_PvE_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Scenario Packs, AI Character Configs, Voice-Over Assets"
---

# Wardogs — GameFeatures: PvE
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/PvE/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/PvE) — 37 JSON files. Each file is a sequence of `--- export:` blocks; the first is the asset, the rest are sub-objects. Values are raw export values.*

---

## 1. What This Folder Holds

PvE is the scenario framework: a shared base ([`PvECore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/PvECore/Content/PvECore.json), [`BaseScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/BaseScenario.json)) plus four mission scenarios and an example scenario. Each scenario is a GameFeatureData pack that sets a quest, a death rule set, a faction, and scenario-specific data.

| Metric | Value |
|---|---|
| Files | 37 |
| GameFeatureData packs | 6 ([`PvECore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/PvECore/Content/PvECore.json), [`BaseScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/BaseScenario.json), [`HunterKiller_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/HunterKiller_01/Content/HunterKiller_01.json), [`ScenarioExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/ScenarioExample/Content/ScenarioExample.json), [`StrikeDisarm_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/StrikeDisarm_01.json), [`VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/VIPEscort_01.json)) |
| AI character configs (`WDAICharacterConfigData`) | 5 |
| Voice-over assets (`WDScenarioVoiceOverData`) | 13 |
| DataTables | 6 |
| Other UI data assets | 5 (quest log, objective area, VIP map, distance text, scenario results) |

---

## 2. Scenario Packs

| Pack | Death rule set | Scenario quest | Player faction | Scenario value | Extra plumbing |
|---|---|---|---|---|---|
| [`BaseScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/BaseScenario.json) | — | — | — | — | Quest-log widget, scene data, minimap/tactical/spatial tracker tables |
| [`HunterKiller_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/HunterKiller_01/Content/HunterKiller_01.json) | `B_DeathRuleSet_NoRespawns` | `Q_HunterKiller_01` | not set | not set | Faction setup (3 teams) |
| [`ScenarioExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/ScenarioExample/Content/ScenarioExample.json) | `B_DeathRuleSet_NoRespawns` | `Q_ScenarioExample` | not set | not set | Example vendor (`B_ExampleScenarioVendorStock`) and free-vehicle spawner (`B_FreeVehicleSpawner`) |
| [`StrikeDisarm_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/StrikeDisarm_01.json) | `B_DeathRuleSet_NoRespawns` | `Q_StrikeDisarm_01` | `Meta.Alignment.Faction.Charlie` | 3000 (unnamed key) | Interaction contexts ([`DT_InteractionContextData_StrikeDisarm_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/DT_InteractionContextData_StrikeDisarm_01.json)) |
| [`VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/VIPEscort_01.json) | `B_DeathRuleSet_NoRespawns` | `Q_VIPEscort_01` | `Meta.Alignment.Faction.Bravo` | 2000 (unnamed key) | Lootable table ([`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json)) |

The "Scenario value" field is `ScenarioStartingCash` of `WDScenarioData` (SDK `BaseScenarioRuntime`, +0x0004): the cash players start the mission with. StrikeDisarm_01 = 3000, VIPEscort_01 = 2000; HunterKiller_01 and ScenarioExample set none. The key was unnamed in earlier exports only because the usmap name was hashed. Round 36 added the placed actors and quest graphs: see [`docs/evidence/round36-ai.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md) and `assets/data/pve-scenarios.json`.

Every scenario pack also adds `WDGameFeatureAction_AddScenarioState` with the `ScenarioData` shown above, and `GameFeatureAction_AddComponents` on `WDGameState` with `B_FactionSetup_CreateThreeTeams`.

### 2a. PvECore and BaseScenario plumbing

| Item | Value |
|---|---|
| Match states (PvECore) | `WDMatchState_PreMatch_Scenario`, `WDMatchState_Playing_Scenario`, `WDMatchState_PostMatch_Scenario` (BaseScenarioRuntime) |
| Components (PvECore/BaseScenario) | `WDScenarioDefaultPlayerSpawnManagerComponent` on `WDGameMode`; `SDQuestObjectiveDataProviderComponent` on `WDGameState`; `SDQuestObjectiveComponent` on `PC_WDPlayerController` |
| Scene registry | `UISceneData_Match` → [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) |
| Tracker registries | `TrackerData_TacticalMap` → [`DT_TrackerData_Map_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Map_Scenario.json); `TrackerData_Minimap` → [`DT_TrackerData_Minimap_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Minimap_Scenario.json); `TrackerData_Spatial` → [`DT_TrackerData_Spatial_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Spatial_Scenario.json) |
| HUD widgets | `UI.HUD.Element.GameFeature.Scenario.QuestLog` → `W_HUDScenarioQuestLog`; `UI.HUD.Element.InventorySpaceIndicator` → `W_HUDSubtitleWidget`; a persistent widget in the Normal layer |

---

## 3. AI Character Configs (`WDAICharacterConfigData`)

All five share the same controller, behaviour tree (`BT_WDAIPvECore_Base`), alert-threshold data, and influence data as the core preset in the AI folder.

| Config | Faction | Inventory (tag ×count) |
|---|---|---|
| [`AIC_Lonestar_Rifleman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar/AIC_Lonestar_Rifleman.json) | Alpha | `Id.Item.M4` ×1, `Id.Item.LightArmor` ×1, `Id.Item.LightHelmet` ×1, `Id.Item.M4Magazine` ×2 |
| [`AIC_Lonestar_Sniper`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar/AIC_Lonestar_Sniper.json) | Alpha | `Id.Item.MK22` ×1, `Id.Item.LightArmor`, `Id.Item.LightHelmet`, `Id.Item.SniperScope10x`, `Id.Item.MK22Mag` |
| [`AIC_Manticore_Rifleman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Rifleman.json) | Charlie | `Id.Item.AK74M`, `Id.Item.LightArmor`, `Id.Item.LightHelmet`, `Id.Item.AK74MMagazine`, `Id.Item.MZL_07` |
| [`AIC_Manticore_Machinegunner`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Machinegunner.json) | Charlie | `Id.Item.LMG_02`, `Id.Item.LightArmor`, `Id.Item.LightHelmet`, `Id.Item.LMG_02Magazine`, `Id.Item.MZL_04` |
| [`AIC_Manticore_Marksman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Marksman.json) | Charlie | `Id.Item.SVDM`, `Id.Item.LightArmor`, `Id.Item.LightHelmet`, `Id.Item.SVDMMagazine`, `Id.Item.6xScope`, `Id.Item.MZL_04` |

Round 36 read the full `AIInventory` of every config: each soldier carries `LightArmor` x1, `LightHelmet` x1 and **2 magazines** (`M4Magazine`, `MK22Mag`, `AK74MMagazine`, `LMG_02Magazine`, `SVDMMagazine`); the sniper has `SniperScope10x` x1, the marksman `6xScope` x1, and the Manticore soldiers one muzzle device (`MZL_07` rifleman, `MZL_04` machine gunner and marksman). Every config uses the player character `B_WDCore_MoverPlayerCharacter_C`, so health is the player's 100.

---

## 4. Voice-Over Assets (`WDScenarioVoiceOverData`)

13 assets. Each has a `VoiceOverAudioEventTag`, a localised `SubtitleText`, and (where present) a `SubtitleDurationInSecond`.

| Scenario | Assets |
|---|---|
| Example | [`DA_ExampleVoiceOverData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/ScenarioExample/Content/DA_ExampleVoiceOverData.json) |
| StrikeDisarm_01 | [`DA_VoiceOver_StrikeDisarm_Intro1`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/VoiceOvers/DA_VoiceOver_StrikeDisarm_Intro1.json), `_Intro2`, `_Intro3`, `_Intro4`, `_Laptop_Hack_Start`, `_Laptop_Hack_End`, `_Mission_Complete` |
| VIPEscort_01 | [`DA_VoiceOver_VIPEscort_Intro1`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/VoiceOvers/DA_VoiceOver_VIPEscort_Intro1.json), `_Intro2`, `_Intro3`, `_Success`, `_Fail` |

Samples checked (`StrikeDisarm_Intro1`, `VIPEscort_Intro3`, `VIPEscort_Success`, `ExampleVoiceOverData`) all use the audio event tag `Audio.Event.TestBubbleSpace` and a subtitle duration of 10.0. This looks like a placeholder, so treat it as unconfirmed for the rest of the set.

---

## 5. Scenario DataTables and UI

| Asset | Type | Content |
|---|---|---|
| [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) | DataTable (`WDSceneDataTableRow`) | Row `UI.Scene.Match.Scenario.Results`: InputMode UI, `bShouldBlockBack` true, `bIsFocusable` true, `bShouldPreload` false |
| [`DT_TrackerData_Map_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Map_Scenario.json) | DataTable (`WDUITrackerDataTableRow`) | 2 rows: `Trackers.Type.PVE.Objective` and `Trackers.Type.VIP` (persistent trackers) |
| [`DT_TrackerData_Minimap_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Minimap_Scenario.json) | DataTable | 2 rows: `Trackers.Type.PVE.Objective` and `Trackers.Type.VIP` |
| [`DT_TrackerData_Spatial_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Spatial_Scenario.json) | DataTable | Registered, rows not extracted |
| [`DA_QuestLog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/QuestLog/Data/DA_QuestLog.json) | `WDUIQuestLogData` | Quest entry view model (`WDUIHUDQuestLogEntryViewModel`); timeout tags `UI.HUD.Layout.Default`, `UI.HUD.Layout.Vehicle` |
| [`DA_ObjectiveArea`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/MapTracker/DA_ObjectiveArea.json) | `WDUIObjectiveAreaMapTrackerData` | Objective-area materials keyed by tag, e.g. `UI.Material.Tracker.PVE.Circle` → `MI_UI_Zone_Circle` |
| [`DA_VIPMapData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/MapTracker/DA_VIPMapData.json) | `WDUIVIPMapTrackerData` | VIP colour `#923BAD` (R146 G59 B173); vitality-state textures keyed by tag, e.g. `State.Player.Vitality.Critical` |
| `WDUIDistanceTextRules_2` | `WDUIDistanceTextRules` | Present, empty in export |
| [`DA_DefaultScenarioResultsSceneData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DA_DefaultScenarioResultsSceneData.json) | `WDUIScenarioResultsSceneData` | Present, empty in export |

---

## 6. Other Scenario Data

| Asset | Type | Content |
|---|---|---|
| [`Extraction_Helicopter_Speed_Curve_Entry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/ExtractionHelicopter/Extraction_Helicopter_Speed_Curve_Entry.json) | CurveFloat | Speed curve for the extraction helicopter entry; value 300.0 at t=0. Units not stated. |
| [`SOD_Hack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/Blueprints/SOD_Hack.json) (StrikeDisarm_01) | GameplayBehaviorSmartObjectBehaviorDefinition | Smart-object behaviour that wraps `WDGameplayBehaviorConfig_Action` (the hack interaction) |

---

## 7. How Values Combine

- A scenario's behaviour is the union of the PvECore base (match states, quest components, tracker registries) and the scenario pack's own GFD actions.
- The scenario `DeathRuleSetClass` for all four missions is `NoRespawns`, so death in a scenario is final unless the scenario's own rules override it.
- Faction tags on the AI configs and the scenario player faction determine hostility. Alpha and Charlie are used for the Lonestar and Manticore AI; the Bravo tag appears on the core AI preset and on the VIP escort player faction.

---

## 8. Still not pulled / limitations

- **Scenario quest contents.** The `Q_*`/`SQ_*` quest assets are not in this folder's export but are read in round 36 (see section 9). Hunter Killer's quest is an empty Entry to Exit.
- **Scenario values.** Resolved in round 36: 3000 and 2000 are the starting cash (section 2).
- **Full AI inventories.** Resolved in round 36 (section 3).
- **Tracker rows.** Some tracker-table rows were not expanded.
- **Voice-over durations.** Only the samples were checked. The 10.0 value is not confirmed across all 13 assets.
- **Units.** Curve times and values, and the helicopter speed, have no stated units.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Scenario logic.** How quest objectives and the `ScenarioData` values drive the mission flow is in BP and runtime code, not in this folder.
- **Remaining small assets.** Ten scenario voice-over entries, the VIP tracker distance rules and related framework settings are listed row by row in [PvE and Settings Assets](Wardogs_PveSettingsAssets_v1.md).

---

## 9. Round 36: placed AI, objectives and hack (from cooked scenario levels and quests)

Source: the World Partition cells of each scenario's external data layers and the `Q_*`/`SQ_*` quests, read with the extractor; method and every value in [`docs/evidence/round36-ai.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md). Machine-readable copy: [`assets/data/pve-scenarios.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/pve-scenarios.json).

| Mission | Map | AI spawners placed | Player faction | Start cash |
|---|---|---|---|---|
| HunterKiller_01 | Kavkazi | 0 (placeholder labels only; quest is empty) | not set | not set |
| StrikeDisarm_01 | Kavkazi | 53: `AIC_Lonestar_Rifleman` 49, `AIC_Lonestar_Sniper` 4. 27 start at once (6 on `Goal_Patrol`); 26 riflemen are a counter-attack wave started by quest event `Quest.Actor.Event.AISpawners.Trigger` when the hack begins | Charlie | 3000 |
| VIPEscort_01 | Kavkazi | 95: `AIC_Manticore_Rifleman` 86, `AIC_Manticore_Marksman` 5, `AIC_Manticore_Machinegunner` 4; 31 riflemen on `Goal_Patrol` | Bravo | 2000 |

- **Hack:** `B_StrikeDisarm_LaptopObjective_C.HackingDurationSeconds` is 60.0 on the Blueprint but 300.0 on the placed laptop. Aborting the hack fails the mission.
- **Strike and Disarm flow:** `SQ_LaptopHacking` (upload the virus, defend the laptop; during the hack `Goal_BesiegeTarget` and `Goal_StopHack` are added to the AI) then `SQ_Extraction_Helicopter` (board the helicopter), then the mission-complete line.
- **VIP Escort flow:** `SQ_RandomPlayerMarkedForDeath` makes one random player the VIP; the mission fails 10 s after that player goes Critical or disconnects; success is reaching `ExtractionProximity` and boarding the helicopter.
- **Time limit:** none in the quest data.
- **VIP loot:** `Lootable.VIPEscort01.AK` is `Id.Item.SV98` x1 + `Id.Item.SV98Magazine` x1 (respawn 10 s, 15 initial points); the name "AK" is misleading.
