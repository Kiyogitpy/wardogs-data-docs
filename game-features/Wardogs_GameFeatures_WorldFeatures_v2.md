---
title: "WorldFeatures (feature)"
redirect_from: ["/Wardogs_GameFeatures_WorldFeatures_v2.html", "/Wardogs_GameFeatures_WorldFeatures_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, HotZoneMagnet, Lootable, SpawnZoneTest"
---

# Wardogs — GameFeatures: WorldFeatures
*Extracted from cooked game data (UE 5.7 export JSON). Source folder: `Plugins/GameFeatures/WorldFeatures/` — 31 JSON files. Values are raw export values. StateTree internals of the challenge trees are in [Challenges](Wardogs_Challenges_v1.md).*

---

## Season 02 update (2026-10-15)

- No files were added or removed, and the file count (31) is unchanged. Row counts: `DT_LootableDataTable` 12 to 52 (below); the other tables are unchanged.
- HotZoneMagnet tower-capture cash reward, `HostileFactor` literal (`Resources[0]`): 3.0 → 6.0.
- HotZoneMagnet tower-capture XP reward, `HostileReward` literal (`Resources[1]`): 250.0 → 300.0.
- The three `ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_*` StateTrees and the `DT_Challenges_SessionEvents_KOTH_HotZoneMagnet` table have structural changes only in fields this page does not cover. Their values are otherwise unchanged.
- `DT_LootableDataTable` grew from 12 rows to 52. 40 rows are new: `Lootable.PreLobby` and 39 rows named for a weapon or item (for example `Lootable.AK74`, `Lootable.M4`, `Lootable.Mosin`, `Lootable.SV98`). The 12 existing rows are otherwise unchanged except for the `Lootable.Tower` row, which lost its `Id.Item.FOB` entry (weight 0.5, no sub-items) from `ItemsToSpawn`, so that list goes from 6 entries to 5. Every other `Lootable.Tower` entry is identical in both seasons (`Id.Item.SV98`, `Id.Item.M249`, `Id.Item.MedKit.Standard`, `Id.Item.M500` with its 30-round `Id.Item.12g.RifledSlug` sub-item, `ID.Item.RepairTool.Drill.Heavy`); they only sit one position earlier. Season 2 also adds a new boolean field, exported with an unresolved name (`_aaabeefoaikdjpkadlplk`), to every row, including the original 12. It is false on 51 rows and true on `Lootable.PreLobby`.

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

---

## 1. What This Folder Holds

WorldFeatures are the in-world objectives and props that the map places: the **HotZoneMagnet** (tower-capture hot zone) and the **Lootable** containers, plus a test pack for spawn zones. Each has a GFD that adds components and data layers.

| Metric | Value |
|---|---|
| Files | 31 |
| GameFeatureData packs | 3 (`HotZoneMagnet`, `Lootable`, `SpawnZoneTest`) |
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
| `RewardFeed` | `DT_RewardFeedActions_HotZoneMagnet` |
| `TrackerData_Minimap` | `DT_TrackerData_Map_HotZoneMagnet` |
| `TooltipData` | `DT_TooltipData_HotZoneMagnet` |
| `UIInteractionContextV1` | `DT_InteractionContexts_HotZoneMagnet` |
| `UIInteractionContextData` | `DT_InteractionContextData_HotZoneMagnet` |
| `Challenges` | `DT_Challenges_SessionEvents_KOTH_HotZoneMagnet` (0 rows) |
| `ChallengeRewards` | `DT_ChallengeRewards_SessionEvents_HotZoneMagnet` |

### 2b. Interactions

Three interaction data assets. Each holds an `InteractionContext`, behaviour, and a duration.

| Asset | Context tag | Behaviour | Duration (s) |
|---|---|---|---|
| `DA_HotzoneMagnet_Interactions` | `Interaction.Context.WorldFeatures.TowerControl` | Hold | 10.0 |
| `DA_HotzoneMagnetHitInput_Interactions` | `Interaction.Context.WorldFeatures.HotZoneMagnet` | Tap | 0.3 |
| `DA_HotzoneMagnetHitPoint_Interactions` | `Interaction.Context.WorldFeatures.HotZoneHitPoint` | Hold | 0.5 |

The context type is `WDHotZoneMagnetInteractionContext`. Tower control is a 10-second hold. The hit-input and hit-point contexts are short tap and hold actions.

### 2c. Challenge rewards (`DT_ChallengeRewards_SessionEvents_HotZoneMagnet`)

Three rows, each with a `Resources` list of cash and XP.

| Row | Resource | Expression |
|---|---|---|
| `Challenges.Rewards.HotZoneMagnet.TowerCaptured` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * HostileModifier)` |
| `TowerCaptured` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetActivated` | Cash and XP.Role | `(BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetDeactivated` | Cash | `(BaseReward)` |

The tower-capture reward drops as more of the last victims were involved (`LastVictimCount`, clamped to `LastVictimCountMax`), by `LastVictimReductionModifier` per victim. The `HostileModifier` scales it for hostile captures. The activate and deactivate rewards are plain `BaseReward`.

The three `ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_*` StateTrees (`TowerCaptured`, `MagnetActivated`, `MagnetDeactivated`) drive these events. Their events and conditions are tabled in [Challenges](Wardogs_Challenges_v1.md).

### 2d. Map trackers and tooltips

| Asset | Type | Notes |
|---|---|---|
| `DA_Tracker_Map_HotZoneMagnet` | `WDUIMapTrackerData` | Standard map tracker |
| `DA_Tracker_Map_HotZoneMagnetTower` | `WDUIHotZoneMagnetMapTrackerData` | Has `Title` and `CooldownDescription` |

Tracker rows: `Trackers.Type.HotZoneMagnet` and `Trackers.Type.HotZoneMagnetTower`. Tooltip rows: `UI.Tooltip.Data.TacticalMap.HotZoneMagnet` and `…HotZoneMagnetTower`.

### 2e. Audio

| Asset | Type | Content |
|---|---|---|
| `AE_Gamemode_HotZoneMagnet_Activate` | `AEB_PlayHotzoneMagnetActivate` | Plays the tower-magnet MetaSound on context `Audio.Context.Gamemode.HotZoneMagnet.Activate` |
| `AE_Gamemode_HotZoneMagnet_Capture_Success` | `AEB_PlaySoundDelayed` | Plays `MSS_Gamemode_HotZoneMagnet_Code_Correct` after a 0.5 s delay, restart behaviour Always |

Seven crosstalk audio events cover the activate, deactivate, capture start and stop, and the code attempt states (`Clear`, `Incorrect`, `Input`, `Locked`).

---

## 3. Lootable

| Item | Value |
|---|---|
| Components | `B_LootableComponent` on `WDGameFrameworkComponentReceiver` |
| Interaction registries | `DT_InteractionContexts_Lootable`, `DT_InteractionContextData_Lootable` |
| Contexts | `Interaction.Context.WorldFeatures.Lootable.Equip`, `…Lootable.Swap` |
| Loot table | `DT_LootableDataTable` (52 rows in Season 2, 12 in Season 1; the tables below list the 12 Season 1 rows) |
| Query | `EQS_FindSubLootableLocation` |

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

- **StateTree logic.** The triggers and conditions of the three challenge StateTrees are tabled in [Challenges](Wardogs_Challenges_v1.md).
- **Expression variables.** `LastVictimCount`, `LastVictimCountMax`, `LastVictimReductionModifier`, `HostileModifier` and `BaseReward` are named in the expression strings. Some of their literal values are in `DT_ChallengeRewards` in this folder. This page lists only the ones named in the Season 02 section.
- **Interaction ranges.** `InteractionRange` is set on the interaction assets but its value was not extracted.
- **Loot contents.** Decoded on [Loot Containers](Wardogs_LootContainers_v1.md): every Lootable row with its items, weights, chances and sub-items.
- **Localisation keys.** Some `_aaa…` localisation keys are present; their text is not resolved here.
