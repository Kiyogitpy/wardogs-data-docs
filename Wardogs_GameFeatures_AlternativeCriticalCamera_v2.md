---
title: "AlternativeCriticalCamera (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures: AlternativeCriticalCamera (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/AlternativeCriticalCamera/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera) — 8 JSON files.*

---

## 1. What This Folder Holds

The "critical" death-state camera: when a player is critically hurt, the view darkens, pans to the killer, and shows a killcam. A separate variant covers the vehicle seats. The camera is built from character-modifier states, camera modifiers, curves and a post-process registry.

| File | Type | Role |
|---|---|---|
| [`AlternativeCriticalCamera.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/AlternativeCriticalCamera.json) | GameFeatureData + actions | Adds the modifier states and the post-process registry |
| [`DA_CharacterModifierState_AlternateCritical.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DA_CharacterModifierState_AlternateCritical.json) | WDCharacterModifierStateDefinition | Infantry critical camera (5 exports) |
| [`DA_CharacterModifierState_AlternateVehicleCritical.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DA_CharacterModifierState_AlternateVehicleCritical.json) | WDCharacterModifierStateDefinition | Vehicle critical camera (4 exports) |
| [`DT_AlternativeCriticalCamera.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DT_AlternativeCriticalCamera.json) | DataTable | Post-process effect registry, no rows |
| [`CriticalFadeCurve.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CriticalFadeCurve.json) | CurveFloat | Fade curve for the critical effect (role inferred from name) |
| [`CRV_PanToKiller.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CRV_PanToKiller.json) | CurveFloat | Pan-to-killer location alpha |
| [`CRV_PanToKilled.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CRV_PanToKilled.json) | CurveFloat | Pan-to-killed interpolation speed |
| [`CRV_RotateToKiller.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CRV_RotateToKiller.json) | CurveFloat | Rotation alpha to the killer |

---

## 2. Feature Actions

| Action | Effect |
|---|---|
| `WDGameFeatureAction_AddCharacterModifierStates` | Adds the two state definitions with `bOverrideExistingState` true |
| `GameFeatureAction_DataRegistrySource` | Adds [`DT_AlternativeCriticalCamera`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DT_AlternativeCriticalCamera.json) to the `PostProcessEffectsData` registry (client and server) |

---

## 3. Infantry Critical State ([`DA_CharacterModifierState_AlternateCritical`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DA_CharacterModifierState_AlternateCritical.json))

| Field | Value |
|---|---|
| StateTag | `State.CharacterModifier.Critical` |
| Priority | 0 |
| Condition | `WDCharacterModifierCondition_StateTags`: requires `State.Player.Vitality.Critical`, and the vehicle roles `ActivePassenger`, `Driver`, `Gunner`, `PassivePassenger` (the condition queries cover vehicle seating too) |

Camera modifiers in this state:

| Modifier | Settings |
|---|---|
| `B_CameraModifier_DarkenView` | FadeTime 30.0, Priority 126 |
| `WDCameraModifier_Critical` | DefaultState: `RelativeWorldOffset`, bone `head`, world offset (0, −200, 0), relative offset (0, −300, 200). DraggedState: `RelativeOffset`. PitchLockAngle 40.0, Priority 20 |
| `WDCameraModifier_PanToKiller` | See 3a |

### 3a. Pan-to-killer sequence

| Step | Panning state | Time (s) |
|---|---|---|
| 1 | `EWDPanningState::FocusingKilled` | 0.5 |
| 2 | `EWDPanningState::PanningToKiller` | 2.0 |
| 3 | `EWDPanningState::FocusingKiller` | 2.5 |

| Setting | Value |
|---|---|
| RotationInterpSpeed | 100.0 |
| RelativeLocation | (0, 0, 235) |
| ToKillerPanLocationAlphaCurve | [`CRV_PanToKiller`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CRV_PanToKiller.json) |
| ToKilledPanInterpSpeedCurve | [`CRV_PanToKilled`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CRV_PanToKilled.json) |
| ToKillerPanRotationAlphaCurve | [`CRV_RotateToKiller`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CRV_RotateToKiller.json) |
| PostProcessEffects | `PostProcessEffect.DeathState.Killcam` |
| CauseQuery (what caused death) | `Id.Item.Claymore`, `ID.Item.ATMine`, `Id.Vehicle.WeaponExtension.TNK_01.Artillery` |

The cause query means the pan only runs when the killing cause is one of these. Other causes use the default camera. Note the tag `ID.Item.ATMine` uses `ID` where the other tags use `Id`. That is in the source and is kept as-is.

---

## 4. Vehicle Critical State ([`DA_CharacterModifierState_AlternateVehicleCritical`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DA_CharacterModifierState_AlternateVehicleCritical.json))

| Field | Value |
|---|---|
| StateTag | `State.CharacterModifier.Vehicle.Critical` |
| Priority | 0 |
| Condition | Same as infantry: `State.Player.Vitality.Critical` plus vehicle roles |
| Critical modifier | `WDCameraModifier_Critical`: YawLockAngle 30.0, PitchLockAngle 30.0 |
| Pan modifier | `WDCameraModifier_PanToKillerVehicle`: same panning states, curves, cause query and killcam as infantry |

The vehicle variant uses tighter locks (30 degrees on both yaw and pitch, against 40 pitch on foot). The intent is inferred from the values.

---

## 5. How Values Combine

- The critical state activates when `State.Player.Vitality.Critical` is set, and the pan modifier only fires for a matching cause.
- [`CriticalFadeCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CriticalFadeCurve.json) and the 30-second `FadeTime` on the darken modifier control how the screen darkens. Priority 126 on the darken modifier is the highest priority in this set. Higher priority is assumed to win; not verified.
- `bOverrideExistingState` is true, so this pack replaces any existing critical state of the same tag.

---

## 6. Still not pulled / limitations

- **Curve values.** The four CurveFloat assets are present, but their key values were not extracted in this pass.
- **Offset units.** The offsets are in the export's native units (Unreal cm is assumed, not confirmed).
- **Post-process effect.** The [`DT_AlternativeCriticalCamera`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DT_AlternativeCriticalCamera.json) registry has no rows in this export; the `PostProcessEffect.DeathState.Killcam` tag is resolved elsewhere.
- **Critical trigger.** What sets `State.Player.Vitality.Critical` is in the character systems, not this folder.
