---
title: "WorldFeatures (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures: WorldFeatures
*Extracted from cooked game data (UE 5.7 export JSON). Source folder: [`Plugins/GameFeatures/WorldFeatures/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures) — 31 JSON files. Values are raw export values. StateTree internals were summarised, not decoded.*

---

## Season 02 update (2026-10-15)

- No files were added or removed, and the file count (31) and table counts are unchanged.
- HotZoneMagnet tower-capture cash reward, `HostileFactor` literal (`Resources[0]`): 3.0 → 6.0.
- HotZoneMagnet tower-capture XP reward, `HostileReward` literal (`Resources[1]`): 250.0 → 300.0.
- The three `ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_*` StateTrees and the [`DT_Challenges_SessionEvents_KOTH_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_HotZoneMagnet.json) table have structural changes only in fields this page does not cover. Their values are otherwise unchanged.
- [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) item entries changed across the tower rows, including `ItemsToSpawn` item tags, sub-item tags and sub-item amounts. Loot contents are not covered on this page, so only the notable changes are listed here:
  - Tower row `ItemsToSpawn[0]` item: `Id.Item.FOB` → `Id.Item.SV98`.
  - Tower row `ItemsToSpawn[2]` item: `Id.Item.M249` → `Id.Item.MedKit.Standard`.
  - Tower row `ItemsToSpawn[3]` sub-item amount: 1 → 30 (sub-item `Id.Item.12g.RifledSlug`).
  - Tower row `ItemsToSpawn[4]` item: `Id.Item.M500` → `ID.Item.RepairTool.Drill.Heavy`, with `ItemSpawnWeight` 1.0 → 0.5.

---

## 1. What This Folder Holds

WorldFeatures are the in-world objectives and props that the map places: the **HotZoneMagnet** (tower-capture hot zone) and the **Lootable** containers, plus a test pack for spawn zones. Each has a GFD that adds components and data layers.

| Metric | Value |
|---|---|
| Files | 31 |
| GameFeatureData packs | 3 ([`HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/HotZoneMagnet.json), [`Lootable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Lootable.json), [`SpawnZoneTest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/SpawnZoneTest/Content/SpawnZoneTest.json)) |
| DataTables | 10 |
| StateTrees | 3 (challenge event trees in HotZoneMagnet) |
| Interaction data assets | 3 (HotZoneMagnet) |
| Crosstalk audio events | 7 |
| Audio event blueprints | 2 |
| Map tracker data assets | 2 |

---

## 2. HotZoneMagnet

### 2a. Components and registries

| Host | Component | Module |
|---|---|---|
| `WDGameState` | `B_HotZoneMagnetGameStateComponent` | HotZoneMagnet/Data |
| `B_WDMoverPlayerCharacter` | `WDHotZoneMagnetWidgetInteractionComponent` | HotZoneMagnetRuntime |
| `WDPlayerController` | `WDHotZoneMagnetPlayerComponent` | HotZoneMagnetRuntime |

Data registries added by the GFD:

| Registry | Table |
|---|---|
| `RewardFeed` | [`DT_RewardFeedActions_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/RewardFeed/DT_RewardFeedActions_HotZoneMagnet.json) |
| `TrackerData_Minimap` | [`DT_TrackerData_Map_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DT_TrackerData_Map_HotZoneMagnet.json) |
| `TooltipData` | [`DT_TooltipData_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DT_TooltipData_HotZoneMagnet.json) |
| `UIInteractionContextV1` | [`DT_InteractionContexts_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DT_InteractionContexts_HotZoneMagnet.json) |
| `UIInteractionContextData` | [`DT_InteractionContextData_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DT_InteractionContextData_HotZoneMagnet.json) |
| `Challenges` | [`DT_Challenges_SessionEvents_KOTH_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_HotZoneMagnet.json) (0 rows) |
| `ChallengeRewards` | [`DT_ChallengeRewards_SessionEvents_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_HotZoneMagnet.json) |

### 2b. Interactions

Three interaction data assets. Each holds an `InteractionContext`, behaviour, and a duration.

| Asset | Context tag | Behaviour | Duration (s) |
|---|---|---|---|
| [`DA_HotzoneMagnet_Interactions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DA_HotzoneMagnet_Interactions.json) | `Interaction.Context.WorldFeatures.TowerControl` | Hold | 10.0 |
| [`DA_HotzoneMagnetHitInput_Interactions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DA_HotzoneMagnetHitInput_Interactions.json) | `Interaction.Context.WorldFeatures.HotZoneMagnet` | Tap | 0.3 |
| [`DA_HotzoneMagnetHitPoint_Interactions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DA_HotzoneMagnetHitPoint_Interactions.json) | `Interaction.Context.WorldFeatures.HotZoneHitPoint` | Hold | 0.5 |

The context type is `WDHotZoneMagnetInteractionContext`. Tower control is a 10-second hold. The hit-input and hit-point contexts are short tap and hold actions.

### 2c. Challenge rewards ([`DT_ChallengeRewards_SessionEvents_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_HotZoneMagnet.json))

Three rows, each with a `Resources` list of cash and XP.

| Row | Resource | Expression |
|---|---|---|
| `Challenges.Rewards.HotZoneMagnet.TowerCaptured` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * HostileModifier)` |
| `TowerCaptured` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetActivated` | Cash and XP.Role | `(BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetDeactivated` | Cash | `(BaseReward)` |

The tower-capture reward drops as more of the last victims were involved (`LastVictimCount`, clamped to `LastVictimCountMax`), by `LastVictimReductionModifier` per victim. The `HostileModifier` scales it for hostile captures. The activate and deactivate rewards are plain `BaseReward`.

The three `ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_*` StateTrees (`TowerCaptured`, `MagnetActivated`, `MagnetDeactivated`) drive these events. They are not decoded here.

### 2d. Map trackers and tooltips

| Asset | Type | Notes |
|---|---|---|
| [`DA_Tracker_Map_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DA_Tracker_Map_HotZoneMagnet.json) | `WDUIMapTrackerData` | Standard map tracker |
| [`DA_Tracker_Map_HotZoneMagnetTower`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DA_Tracker_Map_HotZoneMagnetTower.json) | `WDUIHotZoneMagnetMapTrackerData` | Has `Title` and `CooldownDescription` |

Tracker rows: `Trackers.Type.HotZoneMagnet` and `Trackers.Type.HotZoneMagnetTower`. Tooltip rows: `UI.Tooltip.Data.TacticalMap.HotZoneMagnet` and `…HotZoneMagnetTower`.

### 2e. Audio

| Asset | Type | Content |
|---|---|---|
| [`AE_Gamemode_HotZoneMagnet_Activate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Audio/Events/AE_Gamemode_HotZoneMagnet_Activate.json) | `AEB_PlayHotzoneMagnetActivate` | Plays the tower-magnet MetaSound on context `Audio.Context.Gamemode.HotZoneMagnet.Activate` |
| [`AE_Gamemode_HotZoneMagnet_Capture_Success`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Audio/Events/AE_Gamemode_HotZoneMagnet_Capture_Success.json) | `AEB_PlaySoundDelayed` | Plays `MSS_Gamemode_HotZoneMagnet_Code_Correct` after a 0.5 s delay, restart behaviour Always |

Seven crosstalk audio events cover the activate, deactivate, capture start and stop, and the code attempt states (`Clear`, `Incorrect`, `Input`, `Locked`).

---

## 3. Lootable

| Item | Value |
|---|---|
| Components | `B_LootableComponent` on `WDGameFrameworkComponentReceiver` |
| Interaction registries | [`DT_InteractionContexts_Lootable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_InteractionContexts_Lootable.json), [`DT_InteractionContextData_Lootable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_InteractionContextData_Lootable.json) |
| Contexts | `Interaction.Context.WorldFeatures.Lootable.Equip`, `…Lootable.Swap` |
| Loot table | [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) (12 rows) |
| Query | [`EQS_FindSubLootableLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/EQS_FindSubLootableLocation.json) |

### 3a. Loot rows

Each row has `bSpawnInsideControlZoneOnly`.

| Row | Inside control zone only |
|---|---|
| `Lootable.Test` | false |
| `Lootable.Tower` | **true** |
| `Lootable.AbandonedTower` | **true** |
| `Lootable.Bandage` | false |
| `Lootable.Weapon` | false |
| `Lootable.Helmet` | false |
| `Lootable.Armor` | false |
| `Lootable.Defib.Cheap` | false |
| `Lootable.Sniper` | false |
| `Lootable.SniperOnly.HighValue` | false |
| `Lootable.SniperOnly.MiddleValue` | false |
| `Lootable.SniperOnly.LowValue` | false |

Only the notable loot-content changes are listed in the Season 02 section. The full spawned item lists are not decoded here.

---

## 4. SpawnZoneTest

One GFD with no actions. It is a test pack and adds nothing.

---

## 5. How Values Combine

- HotZoneMagnet rewards are one table and four StateTree events. The tower-capture cash is the only expression that depends on victims.
- Tower and abandoned-tower loot is restricted to control zones, so it only spawns where a control zone is active.

---

## 6. Still not pulled / limitations

- **StateTree logic.** The three challenge StateTrees and the full set of state nodes are summarised, not decoded. Triggers and conditions are not confirmed.
- **Expression variables.** `LastVictimCount`, `LastVictimCountMax`, `LastVictimReductionModifier`, `HostileModifier` and `BaseReward` are named in the expression strings. Some of their literal values are in `DT_ChallengeRewards` in this folder. This page lists only the ones named in the Season 02 section.
- **Interaction ranges.** `InteractionRange` is set on the interaction assets but its value was not extracted.
- **Loot contents.** The full spawned item lists for each Lootable row are not decoded here.
- **Localisation keys.** Some `_aaa…` localisation keys are present; their text is not resolved here.
