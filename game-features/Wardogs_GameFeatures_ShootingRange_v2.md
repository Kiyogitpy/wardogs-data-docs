---
title: "ShootingRange (feature)"
redirect_from: ["/Wardogs_GameFeatures_ShootingRange_v2.html", "/Wardogs_GameFeatures_ShootingRange_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Match Flow and Components, How It Is Used"
---

# Wardogs — GameFeatures: ShootingRange
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/ShootingRange/` — 1 JSON file (`Content/ShootingRange.json`, 6 exports).*

---

## Season 02 update (2026-10-15)

- Added a data registry source action that adds `DT_SceneData_Match_ShootingRange` to the `UISceneData_Match` registry (client and server source, asset priority 0).
- Export count in this file: 5 → 6.

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

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
| Minimap registry | `TrackerData_Minimap` → `DT_TrackerData_Minimap` |
| Scene data registry | `UISceneData_Match` ← `DT_SceneData_Match_ShootingRange` |

---

## 3. How It Is Used

- The range runs in the single `Playing_ShootingRange` state. There is no pre-match or post-match state in this pack.
- Three-team faction setup is shared with KOTH and the PvE scenarios.

---

## 4. Still not pulled / limitations

- **Range rules.** `WDShootingRangeComponent` and the spawn manager are C++ classes with no values in this export.
- **Layer contents.** The `EDL_ShootingRange` layer's content is not in this folder.
- **Tracker rows.** Not expanded here; see the Deathmatch and PvE docs for the shared minimap table layout.
