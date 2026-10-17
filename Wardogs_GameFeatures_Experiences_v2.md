---
title: "Experiences (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures: Experiences
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/Experiences/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Experiences) — 11 JSON files. Two experiences: [`KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/KOTH/Content/KOTH.json) (1 file) and [`SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/SniperShowdown.json) (10 files).*

---

## 1. What This Folder Holds

Experiences are complete game modes. Each one is a GameFeature pack that sets match states, components, HUD widgets and data registries. Two are in this folder: **KOTH** (King of the Hill), and **SniperShowdown**, a sniper showdown mode with a stillness-detection mechanic.

| Experience | Files | Mode |
|---|---|---|
| KOTH | 1 | King of the Hill (control zone) |
| SniperShowdown | 10 | Sniper showdown |

---

## 2. KOTH ([`KOTH/Content/KOTH.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/KOTH/Content/KOTH.json))

### 2a. Match states

| Order | Match state |
|---|---|
| 1 | `WDMatchState_PreMatch_WaitingForWorldLoad` |
| 2 | `WDMatchState_PreMatch_WaitingForPlayerCount` |
| 3 | `ControlZoneRuntime.WDMatchState_Playing_KOTH` |
| 4 | `WDMatchState_PostMatch` |

### 2b. Components

| Host | Component |
|---|---|
| `WDGameStateSession` | `B_FactionSetup_CreateThreeTeams` (three factions) |
| `WDGameModeSession` | `WDKOTHPlayerSpawnManagerComponent` |
| `WDGameStateSession` | `WDItemRequirementsEvaluatorComponent` |

### 2c. Other

- World Partition: `EDL_KOTH` (external data layer).

---

## 3. SniperShowdown

### 3a. Match states

| Order | Match state |
|---|---|
| 1 | `WDMatchState_PreMatch_WaitingForWorldLoad` |
| 2 | `WDMatchState_PreMatch_WaitingForPlayerCount` |
| 3 | `SniperShowdownRuntime.WDMatchState_Playing_SniperShowdown` |
| 4 | `WDMatchState_PostMatch` |

### 3b. Components

| Host | Component | Role (inferred from name) |
|---|---|---|
| `WDGameStateSession` | `B_SniperShowdown_FactionAssignmentComponent` | Assigns factions |
| `WDGameStateSession` | `WDSniperShowdownLastKillTrackerComponent` | Tracks last kill |
| `WDGameStateSession` | `B_SniperShowdown_MusicController` | Music |
| `WDGameModeSession` | `B_SniperShowdown_PlayerSpawnManagerComponent` | Spawns players |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_ExplodeComponent` | Explode on defeat (inferred) |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_LoadoutComponent` | Loadout |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_OOBComponent` | Out-of-bounds handling |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_StillnessSpottingComponent` | Stillness-based spotting |
| `WDControlZone` | `WDSniperShowdownControlZoneSeekerComponent` | Control zone seeking |

### 3c. Player and widgets

| Item | Value |
|---|---|
| Pawn data | [`SniperShowdown_PlayerData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/Character/SniperShowdown_PlayerData.json) (`WDPawnData`): `B_SniperShowdown_MoverPlayerCharacter` |
| Scene registry | `UISceneData_Match` → [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) |
| Event feed | `UIEventFeedData` → [`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json) |
| Tracker registries | `TrackerData_Minimap` and `TrackerData_TacticalMap` → [`DT_TrackerData_Map_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_TrackerData_Map_SniperShowdown.json) |
| HUD: leaderboard | `UI.HUD.Element.GameModeLeaderboard` → `W_SniperShowdown_Leaderboard` |
| HUD: timer | `UI.HUD.Element.Timer` → `W_SniperShowdown_Timer` |
| HUD: status | `UI.HUD.Element.GameModeStatus` → `W_SniperShowdown_Empty` |
| Persistent: fade out | `W_SniperShowdown_FadeOut`, layer Upper |
| Persistent: revealed | `W_SniperShowdown_Revealed`, layer Lower |

### 3d. Event feed ([`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json))

| Row | Self text | Meaning |
|---|---|---|
| `UI.HUD.Element.EventFeed.Type.SniperShowdown.StandingStill` | "Keep moving or you will be revealed." | Warning: standing still is detected |
| `…Spotted` | "You have been revealed. Run." | You have been spotted |
| `…MovingClear` | "You are now hidden." | Cleared by moving |

These three rows confirm the stillness mechanic: standing still reveals you; moving clears it.

### 3e. Scene and UI assets

| Asset | Type | Content |
|---|---|---|
| [`DA_SniperShowdown_FadeOut`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DA_SniperShowdown_FadeOut.json) | `WDSniperShowdownFadeOutData` | Death text "Killed by {KillerName}"; blackout transition out 3.0 s; respawn text "Respawning in {Time}..." |
| [`DA_SniperShowdown_GameOverScene`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DA_SniperShowdown_GameOverScene.json) | `WDSniperShowdownGameOverSceneData` | "Next Round in {Minutes}:{Seconds}"; scoreboard view model `WDUIScoreboardViewModel` |
| [`DA_SniperShowdown_Leaderboard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DA_SniperShowdown_Leaderboard.json) | `WDSniperShowdownLeaderboardData` | Present, empty in export |
| [`DA_SniperShowdown_Timer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DA_SniperShowdown_Timer.json) | `WDSniperShowdownTimerData` | Format "{Minutes}:{Seconds}" |
| [`DA_Tracker_Map_SniperShowdownZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DA_Tracker_Map_SniperShowdownZone.json) | `WDUIMapTrackerData` | Text off, no map zoom scaling |
| [`DT_TrackerData_Map_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_TrackerData_Map_SniperShowdown.json) | DataTable | 3 rows: `Trackers.Type.SniperShowdownZoneActive`, `…ZonePassive`, `…ControlZone` |
| [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) | DataTable | 1 row: `UI.Scene.Match.EndgameMovie` |

---

## 4. How Values Combine

- Each experience is a self-contained mode. KOTH uses the control-zone runtime. SniperShowdown uses its own runtime and also a control zone with a seeker component.
- The stillness mechanic (SniperShowdown) is the only experience-level rule set in this folder. The event-feed rows make its three states explicit.

---

## 5. Still not pulled / limitations

- **Stillness thresholds.** The time or distance that defines "standing still" is in the `StillnessSpottingComponent`, which is in BP code and not in this folder.
- **Explode and OOB rules.** The rules inside `ExplodeComponent` and `OOBComponent` are not decoded here.
- **Music and timers.** Timer durations and music cues are not extracted.
- **Leaderboard data.** Empty in the export.
- **Unnamed keys.** Localised strings use `_aaa…` keys; their values are shown where the source string is present.
