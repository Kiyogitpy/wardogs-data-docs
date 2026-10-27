---
title: "Deathmatch (feature)"
redirect_from: ["/Wardogs_GameFeatures_Deathmatch_v2.html", "/Wardogs_GameFeatures_Deathmatch_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Match Flow, Components, Input, Registries and HUD"
---

# Wardogs — GameFeatures: Deathmatch
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/Deathmatch/` — 5 JSON files.*

---

## 1. What This Folder Holds

The Deathmatch experience: a team-deathmatch game mode with a weapon-select screen before spawn, health regeneration, and a loadout that generates ammo.

| File | Type | Role |
|---|---|---|
| `Deathmatch.json` | GameFeatureData pack | Main pack: match states, components, registries, HUD widget |
| `Data/DA_DeathmatchStatus.json` | `WDUIDeathmatchStatusData` | Status HUD entry view model |
| `Data/DT_DeathmatchWeaponSelect.json` | DataTable | 20 weapon-select rows |
| `UI/Scene/DA_WeaponSelectData.json` | `WDUIWeaponSelectData` | Weapon-select item view model |
| `UI/Scene/DT_DeathmatchSceneData_Match.json` | DataTable | 1 scene row |

---

## 2. Match Flow

| Order | Match state |
|---|---|
| 1 | `WDMatchState_PreMatch_WaitingForWorldLoad` |
| 2 | `WDMatchState_PreMatch_WaitingForReadyUp` |
| 3 | `DeathmatchRuntime.WDMatchState_Playing_Deathmatch` |
| 4 | `BHModularGameplay.BHMatchState_PostMatch` |

The match waits in `WaitingForReadyUp` (not `WaitingForPlayerCount`) before it starts. The name suggests a ready-up gate; the exact trigger is not in this folder.

---

## 3. Components

| Host | Component | Role (from name) |
|---|---|---|
| `WDGameMode` | `B_DeathmatchSpawner` | Spawns players (empty subclass of the native `WDDeathmatchPlayerSpawnManagerComponent`) |
| `WDMoverCharacter` | `WDHealthRegenComponent` | Health regeneration |
| `WDGameState` | `B_FactionSetup_CreateTwoTeams` | Two-team factions |
| `WDMoverPlayerCharacter` | `WDDeathmatchWeaponSelectionComponent` | Weapon selection |
| `WDMoverPlayerCharacter` | `WDLoadoutAmmoGenerationComponent` | Generates loadout ammo |

Two-team factions here, against three teams in KOTH and PvE scenarios.

---

## 4. Input, Registries and HUD

| Item | Value |
|---|---|
| Input | `IMC_PlayerController` added via `BHGameFeatureAction_AddInputContextMapping` |
| Minimap registry | `TrackerData_Minimap` → `DT_TrackerData_Minimap` |
| Scene registry | `UISceneData_Match` → `DT_DeathmatchSceneData_Match` |
| HUD element | `UI.HUD.Element.GameModeStatus` → `W_DeathmatchStatus` |

---

## 5. Weapon Select (`DT_DeathmatchWeaponSelect`)

20 rows, one per weapon tag. Each row has a `DeathmatchWeaponVariations` list with an overridable description and icon (`bOverwriteDescription`, `bOverwriteIcon`). In the export, all rows have overrides turned off, so the item's own name and icon are used.

| Rows (weapon tags) |
|---|
| `Id.Item.AK74M`, `M4`, `SKS`, `KH2002`, `A91`, `Glock17`, `M12G`, `MP9`, `SV98`, `SMG_03`, `Judge`, `LMG_02`, `M249`, `MK22`, `MMGL`, `RFB`, `SR_04`, `SVDM`, `TAR21`, `Vector` |

The UI scene row is `UI.Scene.Deathmatch.WeaponSelect`.

---

## 6. Status HUD

`DA_DeathmatchStatus` binds `WDUIDeathmatchStatusEntryViewModel` (in `DeathmatchRuntime`) as the entry view model. The entry's data fields are not in the export.

---

## 7. How Values Combine

- Weapon select runs before spawn in `WaitingForReadyUp` → `Playing`. The chosen weapon comes from the 20-row list.
- Health regen is a component on the character, so it runs during the Playing state only if the component's own gating allows it. That gating is not in this folder.

---

## 8. Still not pulled / limitations

- **Regen rate.** `WDHealthRegenComponent` values are not in this folder.
- **Ammo amounts.** `WDLoadoutAmmoGenerationComponent` rules are not in this folder.
- **Spawn logic.** `B_DeathmatchSpawner` was exported in round 86. It is an empty Blueprint subclass of the native `WDDeathmatchPlayerSpawnManagerComponent` (`/Script/DeathmatchRuntime`): no variables, no overrides, no class defaults, no bytecode. The spawn selection rules therefore run entirely in native code. Read statically in round 88 (restored executable; `WDDeathmatchPlayerSpawnManagerComponent` overrides two virtual functions):
  - **Candidate points.** At start-up the component collects every `PlayerStart` actor in the level into its list (`0x8490260`).
  - **Selection** (`0x8493480`, called with the spawning player). The game collects the pawns of all other players that are not spectators; when the match has two or more teams only pawns of other teams count, in a single-team match everyone counts. A point is skipped when it is already claimed by another spawning player or when the spawning pawn would not fit there (an overlap test, `0x6D73880`). Each remaining point is scored by the distance (3D, straight line) to the nearest counted enemy pawn, and the point with the **largest** score wins. A tie goes to the point that comes first in the list.
  - **No randomness and no sight test.** The routine uses no random number and no line-of-sight or visibility check. Which point is chosen therefore depends only on where the enemies stand.
  - **Claim.** The chosen point is marked as claimed by the spawning player (`0x6D73BA0`) and a repeating timer on the point (`AWDPlayerStart.ExpirationCheckInterval`, default 5 s) releases it once the claiming pawn has left or is gone. If no point passes the tests, the routine reports failure and the spawn falls back to whatever the caller does next (not traced).
  All of this is a static reading and was not confirmed in play.
- **Status entry fields.** The view-model's data fields are not in the export.
- **Weapon stats.** The weapons' own stats are in the Weapons folder, not here.
