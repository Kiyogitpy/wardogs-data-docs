---
title: "ShootingRangeTutorial (feature)"
redirect_from: ["/Wardogs_GameFeatures_ShootingRangeTutorial_v2.html", "/Wardogs_GameFeatures_ShootingRangeTutorial_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Match Flow and Components, Helicopter Fly-By, Quests and Text"
---

# Wardogs — GameFeatures: ShootingRangeTutorial
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/ShootingRangeTutorial/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial) — 7 JSON files.*

---

## Season 02 update (2026-10-15)

- Added a data registry source action to [`ShootingRangeTutorial.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/ShootingRangeTutorial.json) that adds `DT_SceneData_Match_ShootingRange` to the `UISceneData_Match` registry (client and server source, asset priority 0).

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

---

## 1. What This Folder Holds

The shooting-range tutorial: a scripted first-run mode with a helicopter fly-by, a seat with a locked camera, and a quest list. It is a short tutorial experience. The base shooting range is in the ShootingRange folder.

| File | Type | Role |
|---|---|---|
| [`ShootingRangeTutorial.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/ShootingRangeTutorial.json) | GameFeatureData + actions | Match state, components, quest-list widget, world layer |
| [`Actors/B_ShootingRangeTutorial_VerbaRocketSpline.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/B_ShootingRangeTutorial_VerbaRocketSpline.json) | AudioComponent | Audio component, not auto-activate |
| [`Actors/HelicopterFlyBy/CRV_ShootingRangeTutorial_FlyByCamera_Smooth.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/HelicopterFlyBy/CRV_ShootingRangeTutorial_FlyByCamera_Smooth.json) | CurveFloat | Smooth fly-by camera curve |
| [`Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_FlyByData.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_FlyByData.json) | WDShootingRangeTutorialFlyByData | Seat, rotor and effect settings |
| [`Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_CharacterModifierState_Vehicle.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_CharacterModifierState_Vehicle.json) | WDCharacterModifierStateDefinition | Vehicle-seat state with camera lock |
| [`UI/Data/DA_QuestEntry.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/UI/Data/DA_QuestEntry.json) | WDUIQuestEntryData | Quest-entry description format |
| [`UI/Data/DA_TutorialQuest.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/UI/Data/DA_TutorialQuest.json) | WDUITutorialQuestData | Tutorial quest view model |

---

## 2. Match Flow and Components

| Item | Value |
|---|---|
| Match state | `ShootingRangeTutorialRuntime.WDMatchState_Playing_ShootingRangeTutorial` |
| Component on `WDGameState` | `B_ShootingRangeTutorial_Component` |
| Component on `WDGameModeSession` | `WDShootingRangeTutorialPlayerSpawnManagerComponent` |
| World layer | `EDL_ShootingRangeTutorial` (external data layer) |
| Scene data registry | `UISceneData_Match` ← [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) |
| Character-modifier scan | `BH.CharacterModifierState` in `/ShootingRangeTutorial/Actors` |
| HUD | `UI.HUD.Element.Tutorial.QuestList` → `W_TutorialQuestList` |

---

## 3. Helicopter Fly-By

### 3a. Seat and effect ([`DA_ShootingRangeTutorial_FlyByData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_FlyByData.json))

| Setting | Value |
|---|---|
| EffectClass | `GE_ShootingRangeTutorial_FlyBy` |
| SeatPositionOffset | (−16.41, 87.35, 84.87) |
| SeatEyeHeight | 60.0 |
| SeatRotation | Pitch 0, Yaw 90, Roll 0 |
| EngineCooldownRotorInterpSpeed | 2.0 |
| Main rotor high-speed material | `M_Invisible_Inst` |
| Main rotor low-speed material | `MLI_LittleBird_Plastics` (ROT_03) |
| Rear rotor high-speed material | `M_RotorCircleBlur_Inst` |

The fly-by uses a Little Bird (ROT_03 materials). The rotor materials swap between a blur-disc (high speed) and plain plastics (low speed) as the engine spins up and down.

### 3b. Seat modifier and camera lock ([`DA_ShootingRangeTutorial_CharacterModifierState_Vehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_CharacterModifierState_Vehicle.json))

| Field | Value |
|---|---|
| StateTag | `State.CharacterModifier.Vehicle.ShootingRange` |
| Condition | `WDCharacterModifierCondition_Tags` requires `State.CharacterModifier.Vehicle.ShootingRange` |
| Modifier 1 | `WDCharacterModifier_Tutorial_Seat` pointing to [`DA_ShootingRangeTutorial_FlyByData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/Actors/HelicopterFlyBy/DA_ShootingRangeTutorial_FlyByData.json) |
| Modifier 2 | `WDCharacterModifier_CameraLock` |

Camera lock:

| Axis | Activation | Lock angle | Smoothing | Max turn speed |
|---|---|---|---|---|
| Pitch | `WorldZero` | 35.0 | 0.75 | 5.0 |
| Yaw | `WorldZero` | 75.0 | 0.75 | 5.0 |
| Roll | None | — | — | — |

Pitch and yaw are limited to 35 and 75 degrees with smoothing, which suggests the camera is held near the instructed view. The intent is inferred from the values.

---

## 4. Quests and Text

| Asset | Type | Content |
|---|---|---|
| [`DA_QuestEntry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/UI/Data/DA_QuestEntry.json) | `WDUIQuestEntryData` | Description format "{Description}" with a bullet prefix |
| [`DA_TutorialQuest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ShootingRangeTutorial/Content/UI/Data/DA_TutorialQuest.json) | `WDUITutorialQuestData` | Quest-entry view model `WDUIQuestEntryViewModel`; data asset reference |

The bullet prefix in the source is a non-ASCII character. It renders as "�" in the export and is kept as-is here.

---

## 5. How Values Combine

- The tutorial starts when the match enters `Playing_ShootingRangeTutorial`. The spawn manager and tutorial component run from there.
- The fly-by seat applies only while the vehicle-seat state tag is set. Its camera lock applies during that state.

---

## 6. Still not pulled / limitations

- **Quest steps.** The quest list is driven by the tutorial component in BP. Step contents are not in this folder.
- **Fly-by curve values.** The `CRV_..._Smooth` keys were not extracted.
- **Effect class.** `GE_ShootingRangeTutorial_FlyBy` is referenced but its behaviour is not in this folder.
- **Audio.** The audio component is not auto-activated. What triggers it is in BP.
- **Units.** Seat offsets are in native units (cm assumed).
