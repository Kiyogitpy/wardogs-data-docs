---
title: "ShootingRange (feature)"
parent: "Game Features"
redirect_from: ["/Wardogs_GameFeatures_ShootingRange_v2.html", "/Wardogs_GameFeatures_ShootingRange_v2"]
---

# Wardogs — GameFeatures: ShootingRange
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/ShootingRange/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/ShootingRange) — 1 JSON file ([`Content/ShootingRange.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRange/Content/ShootingRange.json), 6 exports).*

---

## Season 02 update (2026-10-15)

- Added a data registry source action that adds [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRange/Content/ShootingRange.json) to the `UISceneData_Match` registry (client and server source, asset priority 0).
- Export count in this file: 5 → 6.

---

## 1. What This Folder Holds

The base shooting-range experience: a match state, a three-team faction setup, a spawn manager, a shooting-range component, a world layer and a minimap tracker. It is the one-file pack for the range itself. The tutorial that runs on top of it is in ShootingRangeTutorial.

---

## 2. Match Flow and Components

| Item | Value |
|---|---|
| Match state | `ShootingRangeRuntime.WDMatchState_Playing_ShootingRange` |
| Component on `WDGameState` | `B_FactionSetup_CreateThreeTeams` (three factions) |
| Component on `WDGameState` | `WDShootingRangeComponent` (ShootingRangeRuntime) |
| Component on `WDGameModeSession` | `WDShootingRangePlayerSpawnManagerComponent` |
| World layer | `EDL_ShootingRange` (external data layer) |
| Minimap registry | `TrackerData_Minimap` → [`DT_TrackerData_Minimap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DT_TrackerData_Minimap.json) |
| Scene data registry | `UISceneData_Match` ← [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) |

---

## 3. How It Is Used

- The range runs in the single `Playing_ShootingRange` state. There is no pre-match or post-match state in this pack.
- Three-team faction setup is shared with KOTH and the PvE scenarios.

---

## 4. Still not pulled / limitations

- **Range rules.** `WDShootingRangeComponent` and the spawn manager are C++ classes with no values in this export.
- **Layer contents.** The `EDL_ShootingRange` layer's content is not in this folder.
- **Tracker rows.** Not expanded here; see the Deathmatch and PvE docs for the shared minimap table layout.
