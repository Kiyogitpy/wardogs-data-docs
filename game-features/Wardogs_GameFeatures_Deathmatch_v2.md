---
title: "Deathmatch (feature)"
parent: "Game Features"
redirect_from: ["/Wardogs_GameFeatures_Deathmatch_v2.html", "/Wardogs_GameFeatures_Deathmatch_v2"]
---

# Wardogs — GameFeatures: Deathmatch
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/Deathmatch/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Deathmatch) — 5 JSON files.*

---

## 1. What This Folder Holds

The Deathmatch experience: a team-deathmatch game mode with a weapon-select screen before spawn, health regeneration, and a loadout that generates ammo.

| File | Type | Role |
|---|---|---|
| [`Deathmatch.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Deathmatch.json) | GameFeatureData pack | Main pack: match states, components, registries, HUD widget |
| [`Data/DA_DeathmatchStatus.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DA_DeathmatchStatus.json) | `WDUIDeathmatchStatusData` | Status HUD entry view model |
| [`Data/DT_DeathmatchWeaponSelect.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DT_DeathmatchWeaponSelect.json) | DataTable | 20 weapon-select rows |
| [`UI/Scene/DA_WeaponSelectData.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DA_WeaponSelectData.json) | `WDUIWeaponSelectData` | Weapon-select item view model |
| [`UI/Scene/DT_DeathmatchSceneData_Match.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) | DataTable | 1 scene row |

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
| `WDGameMode` | `B_DeathmatchSpawner` | Spawns players |
| `WDMoverCharacter` | `WDHealthRegenComponent` | Health regeneration |
| `WDGameState` | `B_FactionSetup_CreateTwoTeams` | Two-team factions |
| `WDMoverPlayerCharacter` | `WDDeathmatchWeaponSelectionComponent` | Weapon selection |
| `WDMoverPlayerCharacter` | `WDLoadoutAmmoGenerationComponent` | Generates loadout ammo |

Two-team factions here, against three teams in KOTH and PvE scenarios.

---

## 4. Input, Registries and HUD

| Item | Value |
|---|---|
| Input | [`IMC_PlayerController`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IMC_PlayerController.json) added via `BHGameFeatureAction_AddInputContextMapping` |
| Minimap registry | `TrackerData_Minimap` → [`DT_TrackerData_Minimap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DT_TrackerData_Minimap.json) |
| Scene registry | `UISceneData_Match` → [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) |
| HUD element | `UI.HUD.Element.GameModeStatus` → `W_DeathmatchStatus` |

---

## 5. Weapon Select ([`DT_DeathmatchWeaponSelect`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DT_DeathmatchWeaponSelect.json))

20 rows, one per weapon tag. Each row has a `DeathmatchWeaponVariations` list with an overridable description and icon (`bOverwriteDescription`, `bOverwriteIcon`). In the export, all rows have overrides turned off, so the item's own name and icon are used.

| Rows (weapon tags) |
|---|
| `Id.Item.AK74M`, `M4`, `SKS`, `KH2002`, `A91`, `Glock17`, `M12G`, [`MP9`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/MP9/Content/MP9.json), `SV98`, [`SMG_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/SMG_03/Content/SMG_03.json), `Judge`, [`LMG_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/LMG_02.json), `M249`, [`MK22`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/MK22/Content/MK22.json), `MMGL`, [`RFB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/RFB/Content/RFB.json), [`SR_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/SR_04/Content/SR_04.json), [`SVDM`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/SVDM/Content/SVDM.json), `TAR21`, `Vector` |

The UI scene row is `UI.Scene.Deathmatch.WeaponSelect`.

---

## 6. Status HUD

[`DA_DeathmatchStatus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DA_DeathmatchStatus.json) binds `WDUIDeathmatchStatusEntryViewModel` (in `DeathmatchRuntime`) as the entry view model. The entry's data fields are not in the export.

---

## 7. How Values Combine

- Weapon select runs before spawn in `WaitingForReadyUp` → `Playing`. The chosen weapon comes from the 20-row list.
- Health regen is a component on the character, so it runs during the Playing state only if the component's own gating allows it. That gating is not in this folder.

---

## 8. Still not pulled / limitations

- **Regen rate.** `WDHealthRegenComponent` values are not in this folder.
- **Ammo amounts.** `WDLoadoutAmmoGenerationComponent` rules are not in this folder.
- **Spawn logic.** `B_DeathmatchSpawner` is a Blueprint and is not decoded.
- **Status entry fields.** The view-model's data fields are not in the export.
- **Weapon stats.** The weapons' own stats are in the Weapons folder, not here.
