---
title: "BHFramework"
parent: "Plugins"
---

# Wardogs — Plugin: BHFramework (v2)
*Extracted from cooked game data (UE 5.7 export JSON). Source folder: [`Plugins/BHFramework/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/BHFramework) — 47 JSON files, all under [`Content/Settings/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/BHFramework/Content/Settings). These are user-setting definitions (`BHUserSetting*`). Values are the export's defaults and ranges.*

---

## Season 02 update (2026-10-15)

- **New setting:** `AllowOverkillPreset` (Video). An On/Off choice; turning it on opens a confirmation popup ("Are You Sure?") that says these settings will affect PC performance.
- **Gamepad horizontal sensitivity:** default 3.0 → 4.0, min 0.5 → 1.0, max 10.0 → 7.0.
- **Gamepad vertical sensitivity:** default 2.0 → 3.0, min 0.5 → 1.0, max 10.0 → 7.0.
- **AimAssistSensitivityMultiplier:** the maximum of 1.5 (and display maximum) is no longer in the export. Default 1.0 is unchanged.
- **FrameRateLimit:** now exports a maximum of 360 (display maximum 360) and a step of 1 with 0 decimals. Previously it had no parameters.
- **File and type counts:** 46 → 47 JSON files; Video settings 11 → 12; BoolDiscrete value sets 5 → 6.

## 1. What This Plugin Holds

The game's user-setting definitions: each asset defines one option the player can change in the settings menu, with its default, range, and display rules. The plugin has no gameplay logic; the settings UI and the code that reads these values are elsewhere.

| Setting type | Count | Meaning |
|---|---|---|
| `BHUserSettingNumericData` | 21 | A slider or number: min, max, default, step |
| `BHUserSettingDiscreteData` | 20 | A choice from a list of values, with a default index or dynamic default |
| `BHUserSettingBoolDiscreteValues` | 6 | On/off choice with labelled values (Yes/No, On/Off) |

Setting counts by folder:

| Folder | Files | Settings |
|---|---|---|
| `Audio/` | 6 | Devices and volumes |
| `Controls/` | 17 | Sensitivity, aim assist, gamepad, action behaviour |
| `General/` | 6 | Field of view, vehicle camera, transmission |
| `Shared/` | 6 | Quality presets and toggles |
| `Video/` | 12 | Display, resolution, upscaling, frame rate |

(Some files are the same class with different defaults. The totals above are the count of files, not of distinct settings.)

---

## 2. Audio (6)

| Setting | Type | Default | Range / display |
|---|---|---|---|
| `Audio_InputDevice` | Discrete | Dynamic default | — |
| `Audio_OutputDevice` | Discrete | Dynamic default | — |
| `Audio_Volumes` | Numeric | 1.0 | Displays 0 to 100, step 1 |
| `Audio_Volumes_LicensedMusic` | Numeric | 0.5 | Displays 0 to 100, step 1 |
| `Audio_Volumes_Microphone` | Numeric | 1.0 | Displays 0 to 100, step 1 |
| `Audio_Volumes_VOIP` | Numeric | 0.5 | Displays 0 to 100, step 1 |

---

## 3. Controls (17)

| Setting | Type | Default | Range |
|---|---|---|---|
| `ActionBehavior_Default_Hold` | Discrete | — | 2 values (raw indices 0, 1) |
| `ActionBehavior_Default_Toggle` | Discrete | index 1 | 2 values (raw 0, 1) |
| `ActionBehavior_Default_ToggleOnly` | Discrete | — | 1 value (raw 1) |
| `ActionBehaviour_RotaryMouse` | BoolDiscrete | — | On/Off |
| `AimAssistSensitivityMultiplier` | Numeric | 1.0 | No min or max in the export; 1 decimal |
| `Gamepad_ADSSensitivityMultiplier` | Numeric | 0.5 | Min 0.01, max 5.0, step 0.01 |
| `Gamepad_AxisConfig` | Discrete | `Input.Gamepad.Config.Axis.Default` | — |
| `Gamepad_ButtonConfig_GroundVehicle` | Discrete | `Input.Gamepad.Config.Button.Vehicle.Ground.Default` | — |
| `Gamepad_ButtonConfig_Helicopter` | Discrete | `Input.Gamepad.Config.Button.Vehicle.Air.Helicopter.Default` | — |
| `Gamepad_ButtonConfig_Infantry` | Discrete | `Input.Gamepad.Config.Button.Infantry.Default` | — |
| `Gamepad_HorizontalSensitivity` | Numeric | 4.0 | Min 1.0, max 7.0; display 1 to 10 |
| `Gamepad_VerticalSensitivity` | Numeric | 3.0 | Min 1.0, max 7.0; display 1 to 10 |
| `MouseAcceleration` | Numeric | — | Max 0.05; display max 5.0, step 0.01 |
| `Sensitivity` | Numeric | 0.4 | Min 0.1; display 0.1 to 2.0, step 0.01 |
| `SensitivityMultiplier` | Numeric | 1.0 | Min 0.01, max 5.0, step 0.01 |
| `SensitivityMultiplier_Vehicle_Weapons` | Numeric | 1.0 | Min 0.01, step 0.01 |
| `SensitivityMultiplier_Vehicles` | Numeric | 0.5 | Min 0.01, max 2.0, step 0.01 |

---

## 4. General (6)

| Setting | Type | Default | Range |
|---|---|---|---|
| `Controller_FreeCursorSensitivity` | Numeric | 1.0 | Min 0.1, max 2.0; display 0.1 to 2.0 |
| `FieldOfView` | Numeric | 90 | Min 60, max 120, step 1 |
| `FieldOfView_Vehicle` | Numeric | 85 | Min 60, max 110, step 1 |
| `AdvancedVehicle_FirstPersonFreeCamSensitivity` | Numeric | 1.0 | Max 1.5; display max 150 |
| `AdvancedVehicle_ThirdPersonFreeCamSensitivity` | Numeric | 1.0 | Max 1.5; display max 150 |
| `AdvancedVehicle_TransmissionType` | Discrete | — | 2 values (raw 0, 1) |

---

## 5. Shared (6)

| Setting | Type | Default | Notes |
|---|---|---|---|
| `PresetQuality_Default_High_Restricted` | Discrete | index 3, dynamic | Values −1 to 4 |
| `Quality_Default_High_Restricted` | Discrete | index 1 | Values 4, 0, 1, 2, 3 |
| `Toggle_Default_No` | BoolDiscrete | — | Yes/No labels |
| `Toggle_Default_Off` | BoolDiscrete | — | On/Off labels |
| `Toggle_Default_On` | BoolDiscrete | — | On/Off labels |
| `Toggle_Default_Yes` | BoolDiscrete | — | Yes/No labels |

---

## 6. Video (12)

| Setting | Type | Default | Range / values |
|---|---|---|---|
| `AllowOverkillPreset` | BoolDiscrete | — | On/Off (raw `True`, `False`) |
| `Brightness` | Numeric | 2.2 | Min 1.7, max 2.7; display 50 to 150, step 1 |
| `DisplayMode` | Discrete | index 1 | 3 values (raw 0, 1, 2) |
| `DisplayResolution` | Discrete | dynamic | Resolution list |
| `FSR3` | Discrete | index 3 | Values 0 to 4 |
| `FrameRateLimit` | Numeric | — | Max 360, display max 360, step 1, 0 decimals |
| `NVIDIA_DLSS` | Discrete | — | Raw values 1 to 7 |
| `NVIDIA_DLSSG` | Discrete | — | Raw values 0, 251, 241, 17, 23, 31, 37, 41 |
| `NVIDIA_Reflex` | Discrete | — | Raw values 0, 1, 3 |
| `ResolutionScale` | Numeric | 0.87 | Shown as a percent, 0 to 100, step 0.01 |
| `Upscaling` | Discrete | dynamic | Values 0 to 6 |
| `XeSS` | Discrete | — | Raw values 1 to 7 |

---

## 7. How Values Combine

- Each setting's effective value is the player's saved choice, or the default if none is saved. Discrete settings with a dynamic default pick their default from the hardware or platform at runtime.
- Some settings are multipliers of others. `AimAssistSensitivityMultiplier` scales aim-assist strength (see the BHAimAssist doc), and the `SensitivityMultiplier_*` settings scale mouse sensitivity by control context (general, vehicles, vehicle weapons).
- Upscaling settings (FSR3, DLSS, DLSSG, XeSS) are alternatives. Only the one matching the player's hardware is used; the others are not active.

---

## 8. Still not pulled / limitations

- **Enum labels.** Discrete settings store raw values (for example `0`, `1`, `251`). The labels (what each value means) come from the `BHUserSettingEnumDiscreteValues` sub-exports keyed by localised strings. The labels were not resolved in this pass, so the raw values above are shown as-is.
- **Localised labels.** Yes/No, On/Off and the setting names are localised strings. Only the keys are in the export.
- **Dynamic defaults.** How the dynamic default is picked for display, resolution, device and upscaling is in the runtime code.
- **Gamepad button and axis mappings.** The tag values are defaults. The full mapping tables are in the gamepad config sub-exports and were not expanded.
- **FrameRateLimit.** The export gives a maximum (360) and a step (1) but no minimum or default. Its off label is a localised string.
- **Setting consumers.** Which code reads each setting is not in this folder.
