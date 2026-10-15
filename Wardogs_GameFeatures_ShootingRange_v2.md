---
title: "ShootingRange (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures: ShootingRange (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/ShootingRange/` — 1 JSON file (`Content/ShootingRange.json`, 5 exports).*

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

---

## 3. How It Is Used

- The range runs in the single `Playing_ShootingRange` state. There is no pre-match or post-match state in this pack.
- Three-team faction setup is shared with KOTH and the PvE scenarios.

---

## 4. Still not pulled / limitations

- **Range rules.** `WDShootingRangeComponent` and the spawn manager are C++ classes with no values in this export.
- **Layer contents.** The `EDL_ShootingRange` layer's content is not in this folder.
- **Tracker rows.** Not expanded here; see the Deathmatch and PvE docs for the shared minimap table layout.
