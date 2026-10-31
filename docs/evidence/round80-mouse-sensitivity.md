# Round 80: the mouse sensitivity formula (degrees per mouse count)

Static analysis only (disassembly with capstone over the restored executable, the decompiled corpus, cooked JSON, and config files read out of the paks with `WdExtract rawfiles`). Nothing was run and no game session was observed. RVAs are image-base-relative. Nothing here is behind the protection layer (no PROTECTED items). The status of each link is FOUND (read from data or code), NATIVE (read from native code, value static) or ABSENT (searched, not found); "inferred" marks a link that rests on engine behaviour or an offset argument rather than on a line read here.

Answer in one line: hip fire turns the view by `0.07 x S` degrees per mouse count, where `S` is the stored sensitivity (default 0.4), so 0.028 degrees per count at the default and 0.07 at stored 1.0; aiming multiplies that by the ADS multiplier setting (default 1) and by a field of view ratio `R` (0.2 for a 4x scope on a 90 degree base, 16:9, default settings).

## 0. Result

```
S      = stored MouseSensitivity            (default 0.4; slider shown value d, S = 0.1 + (d - 0.1) * 0.9 / 1.9)
hip    : degrees per count (yaw and pitch) = 0.07 * S
ADS    : degrees per count                 = 0.07 * S * MouseADSMultiplier * R
R      = 1 + (R_full - 1) * w               (w = ADS blend, see section 5)
Relative: R_full = atan(k * tan(Fa/2)) / atan(k * tan(F0/2))      k = max(coef/100, 0.001) * (aspect / (16/9))
Legacy  : R_full = tan(Fa/2) / tan(F0/2)
F0 = Field of view setting (horizontal degrees, default 90)
Fa = aimed field of view = base / magnification, base = 72 if (Independent, or sight test input >= 3.25) else F0
```

Worked values (800 DPI, 16:9, defaults otherwise):

| Case | Degrees per count | Counts per 360 | cm per 360 |
|---|---|---|---|
| Stored S 0.4 (the data default; slider shows 0.733) | 0.0280 | 12,857 | 40.8 |
| Stored S 1.0 (slider maximum 2.0) | 0.0700 | 5,143 | 16.3 |
| Slider 1.0 (S 0.526) | 0.0368 | 9,771 | 31.0 |
| Slider 0.4 (S 0.242) | 0.0169 | 21,242 | 67.4 |
| Slider 0.1 (S 0.1) | 0.0070 | 51,429 | 163.3 |
| 4x scope, S 0.4, base 90, ADS multiplier 1 | 0.0056 | 64,286 | 204.1 |

cm per 360 = 360 / (degrees per count) / DPI x 2.54.

Important correction to the premise: the slider is a masked value. The data default 0.4 is the stored value; the slider shows `0.1 + (0.4 - 0.1) * 1.9 / 0.9 = 0.733`, not 0.4 (section 3).

## 1. The BH axis modifier (FOUND, NATIVE)

[`DA_Player_InputAxisConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Controls/DA_Player_InputAxisConfig.json) (`BHAxisConfigDataAsset`) holds the wiring only. The code that applies it is the Enhanced Input modifier `UWDApplyAxisConfig`, whose vtable is `0xB338C68`. Its `ModifyRaw` (vtable slot 86) is `0x6BF2B70`. It:

- accepts only a valid player-controlled input (checks around `0x6BF2B70` to `0x6BF2C00`);
- builds two lists of `FBHAxisSettingModifier` entries (12 bytes each: axis byte, bGamepad byte, ModifierType byte, then the property FName), the `DefaultAxisConfig` list first (`0x144D06260`) and the matching `StateAxisConfigs` after it (`0x144D06290`, entries whose gameplay tag requirements match the pawn);
- walks each list in order and skips entries whose bGamepad differs from the modifier's own flag (`WDApplyAxisConfig_0` is the mouse instance, `WDApplyAxisConfig_1` has `bIsGamepad` true);
- for axis X or Y calls `0x6BF0090`, for axis XY calls `0x6BF0260`.

Both apply functions look the named property up on the user settings object (`0x146EAD470` class, `0x1418AA860` find property by FName, `0x146EB0FE0` get the settings object) and read the float or bool at the property offset. By ModifierType (`EBHAxisModifierType`: Exponent 0, Sensitivity 1, Invert 2; the Sensitivity value 1 is also in `sdk/raw/BHEnhancedInput_structs.hpp`):

| Type | What it does to the value v | Code |
|---|---|---|
| Sensitivity (1) | `v = v * property` (a plain multiply; property missing reads 1.0). No curve, no power, no divide by a reference, no hidden constant. | `0x6BF0090` `else if result==0` branch: `v14 = 1.0; ... *a3 = v14 * *a3` |
| Invert (2) | negates v if the bool property is true; an axis already negated by an earlier entry in the same call is recorded in a small list so a later entry can undo it (a state config overrides the default). | `0x6BF0090` / `0x6BF0260` |
| Exponent (0) | `e = property + 1.0`; if `e != 1.0` then `v = sign(v) * pow(|v|, e)`, else unchanged. The call at `0x6BF022A` is `pow` (resolved through the import thunk `0x98F81A6` to `api-ms-win-crt-math-l1-1-0.dll!pow`). | `0x6BF01FF` to `0x6BF022A` |

So the whole axis step for the mouse is: `v -> sign(v)*|v|^(1+MouseAcceleration)`, then `* MouseSensitivity`, then (Y only) optional negate, then, when the pawn carries the aiming tag (`State.Player.Movement.Aiming`), `* MouseADSSensitivityMultiplier`. The `DefaultAxisConfig` also lists an X Exponent with property None (reads 0, so `e == 1`, no effect).

`MouseVerticalAxisSensitivityMultiplier` is not in the axis config. It is a real property (`BHUserSettings +0x444`, getter at `0x4E39210`, no direct caller; the only references are the property registration stubs near `0x4E2F764`). No reader of it was found (ABSENT as a mouse-look factor). The wiki setting "Vertical axis multiplier" (default 1, 0.01 to 5) therefore has no static effect link here; this round treats it as 1. It is the one open item that could change the pitch factor.

Mouse acceleration: [`DA_Setting_Controls_MouseAcceleration`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHFramework/Content/Settings/Controls/DA_Setting_Controls_MouseAcceleration.json) has Maximum 0.05, DisplayMaximum 5.0, bMaskValue, no Default (so 0). The stored value is 0 to 0.05, shown 0 to 5; the exponent is `1 + stored`, so the default is exponent 1.0 (off) and the largest is 1.05. FOUND (data) plus the Exponent branch above. The power is applied to the value after the engine axis step (section 4), before the sensitivity multiply.

## 2. The input chain from mouse counts to the view (per link)

| # | Link | Status | Where |
|---|---|---|---|
| 1 | Raw `Mouse2D` counts per frame (dx, dy) | engine, inferred | UE input |
| 2 | Project axis config for `Mouse2D`: DeadZone 0, Exponent 1, Sensitivity 0.07 | FOUND (config), applied by the engine: inferred | `Engine/Config/BaseInput.ini` lines 27 to 29 (`MouseX`, `MouseY`, `Mouse2D` all 0.07); `Wardogs/Config/DefaultInput.ini` re-adds only the four gamepad stick entries (neutralised to 1/0/1), so the mouse entries stay at 0.07 |
| 3 | IMC mapping: [`IMC_PlayerController`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IMC_PlayerController.json) entry `Mouse2D -> IA_Look`, modifiers: `WDApplyAxisConfig_0` only (no Scalar, no Negate, no swizzle, no ScaleByDeltaTime) | FOUND | `data/.../PlayerController/IMC_PlayerController.json` lines 530 to 545 |
| 4 | [`IA_Look`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Look.json) is Axis2D with one action modifier `WDAimAssistInputModifier` | FOUND; its effect on mouse input not traced | [`IA_Look.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Look.json) |
| 5 | Axis modifier (section 1) | FOUND, NATIVE | `0x6BF2B70`, `0x6BF0090`, `0x6BF0260` |
| 6 | Look handler: scales the 2D value by the field of view factor and calls AddYawInput (x) and AddPitchInput (y) | NATIVE | `0x6D4F700` (the call `0x6D4DEB0` at `0x6D4FC2F`, virtual slot 425 at `+0xD48` for yaw, slot 424 at `+0xD40` for pitch; the engine's own `AddYawInput` thunk `0x42E5140` calls the same slot). Bound through an action callback thunk at `0x6D591F8` (binding of the thunk to IA_Look not traced: inferred) |
| 7 | `AddYawInput` / `AddPitchInput` (slots 425 and 424 are the unmodified engine `0x42B43E0` and `0x42B3F40`) | NATIVE | `RotationInput.Yaw += Val * scale` where `scale = (UInputSettings.bEnableLegacyInputScales ? controller.InputYawScale : 1.0)`; the false branch constant is 1.0 for both (`0x57F95E3`, `0x57F9A83`) |
| 8 | `bEnableLegacyInputScales` | FOUND | `Wardogs/Config/DefaultInput.ini`: `bEnableLegacyInputScales=False`, `bEnableFOVScaling=False`. So the legacy 2.5 / -2.5 controller scales are not used: scale is 1.0 |
| 9 | `RotationInput` added to the view rotation in degrees, no delta time on the mouse binding | engine, inferred | UE `UpdateRotation` |

Config files came from the pak: `WdExtract rawfiles "Config/Default" --copy` and `... "Config/Base" --copy` (output under `E:/Reverse_Engineer/wardogs_analysis/round80_sens/raw`). `DefaultInput.ini` is 37 KB; the lines that matter are `bEnableFOVScaling=False`, `bEnableLegacyInputScales=False`, `DefaultPlayerInputClass=/Script/BHEnhancedInput.BHEnhancedPlayerInput` and the four gamepad `AxisConfig` re-adds (lines 5 to 12). The controller class defaults of `InputYawScale` / `InputPitchScale` were not needed (legacy scales off) and were not read.

Why link 2 is "inferred": that Enhanced Input applies the project `AxisConfig` properties (including `Sensitivity=0.07`) to `Mouse2D` is engine behaviour, not read in this executable. Two things support it: (a) the project re-adds the gamepad axis entries with DeadZone 0 / Sensitivity 1, which only makes sense if the legacy axis properties are applied to Enhanced Input values (the stick dead zone is handled by `WDDeadZoneInputModifier` instead); (b) without the 0.07, the default would be 0.4 degrees per count, 2.9 cm per 360 at 800 DPI, which is not a usable default, while with it the default is 40.8 cm and the slider range is 16 to 163 cm. If link 2 were absent, every degrees-per-count and cm/360 figure would be 14.29 times faster and the formula would read `S` degrees per count.

## 3. The slider-to-stored mapping (FOUND data, mask rule derived)

[`DA_Setting_Controls_Sensitivity`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHFramework/Content/Settings/Controls/DA_Setting_Controls_Sensitivity.json) (BHFramework): Minimum 0.1, Default 0.4, bMaskValue true, DisplayMinimum 0.1, DisplayMaximum 2.0, Increment 0.01; no Maximum, so the struct default applies. `bMaskValue` maps the stored range [Minimum, Maximum] linearly onto [DisplayMinimum, DisplayMaximum]. The struct default Maximum is 1.0 and Minimum 0, shown by:

- [`DA_Setting_Audio_Volumes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHFramework/Content/Settings/Audio/DA_Setting_Audio_Volumes.json): only Default 1.0 and DisplayMaximum 100 are stored; the volume default displays as 100 only if Maximum is 1.0;
- the weapon view model scale: stored default 0.3333 (setting `FirstPersonMeshFieldOfViewScale`), display 1 to 10 with Increment 1; in an installed config the stored value 0.666667 maps to exactly 7.0 under `1 + stored * 9`, a whole number on the Increment 1 grid;
- the mouse sensitivity stored in the same config, 0.407895, maps to exactly 0.75 under `0.1 + (S - 0.1) * 1.9 / 0.9`, a value on the 0.01 grid (for other maxima it does not land on the grid).

Both are consistent with Maximum 1.0, so the mapping is `d = 0.1 + (S - 0.1) * 1.9 / 0.9` and `S = 0.1 + (d - 0.1) * 0.9 / 1.9`. The default is stored (the gamepad rows behave the same: Default 4 in a stored range 1 to 7). The default S 0.4 therefore shows as 0.733 on the slider. The native mask code itself was not located (a scan of the exe for the Parameters field reads found no match), so the mask rule is derived from these data patterns, not from a line of code: inferred. The "shown range 0.1 to 2" in the wiki is the display range; the stored range is 0.1 to 1.0.

## 4. Mouse acceleration (FOUND, NATIVE)

See section 1: exponent `1 + MouseAcceleration`, default stored 0, so off by default; the setting is stored 0 to 0.05 (shown 0 to 5). With acceleration `a`, a frame's value `v = 0.07 * counts` becomes `sign(v) * |v|^(1+a) `, so small per-frame movements are reduced relative to large ones and the effect depends on the frame rate (it acts on per-frame counts).

## 5. The look handler's field of view factor (NATIVE)

`0x6D4DEB0` (called from the look handler `0x6D4F700` at `0x6D4FC2F`) returns the factor. Inputs: the settings object `this` (the player controller, which caches the settings in `+0x968` AimingFovMode, `+0x969` Sensitivity scaling mode, `+0x96A` transition, `+0x96C` Monitor matching distance; the cache is filled by `0x6D51CE0` from the getters `0x6EB1220`, `0x6EB1240`, `0x6EB1260`, `0x6EB1BE0`, and the coefficient getter reads stored 0 to 100); the ADS state object (`0x6B86300`: `+0x04` aiming alpha, `+0x14` the 3.25 test input of round 79, `+0x18` the eased zoom multiplier, or 1.0 when it is below 1e-8); `DefaultFOV` of the camera manager (`+0x2D0`, the Field of view setting, per round 79); the viewport size (`0x42CA040`; width / height, 16/9 when the height is 0).

1. `F0 = DefaultFOV`. `Fa = 0x6C29420(mode, test, zoom, F0)`: if `|zoom| > 1e-8` then `base = 72` when `mode == Independent` or `test >= 3.25`, else `base = F0`; `Fa = base / zoom`. Otherwise `Fa = F0`. (The 72.0 constant is at `0x6C29441`'s load, the 3.25 at `0x6C29438`'s compare. This is the same rule the camera modifier and round 79 use.)
2. With `a` = aspect ratio: `tb = tan(F0 * pi/360)` then `* (1/a)` then `atan` then `tan` (the `* 0.99999994` between is a float guard), i.e. `tb = tan(F0/2) / a`; likewise `ta = tan(Fa/2) / a`. (`tanf` is the thunk `0x98F81AC`, `atanf` is `0x98F81D6`; both resolved through the import table.)
3. Legacy (mode byte 1): `R_full = ta / tb = tan(Fa/2) / tan(F0/2)`.
4. Relative (mode byte 0): `X = max(coef * 0.01, 0.001) * a * (a * 0.5625)`; `R_full = atan(ta * X) / atan(tb * X)`. Since `ta * X = max(coef/100, 0.001) * (a / (16/9)) * tan(Fa/2)`, this is `atan(k tan(Fa/2)) / atan(k tan(F0/2))` with `k = max(coef/100, 0.001) * a / (16/9)`. At the default coefficient (100) on a 16:9 screen `k = 1`, so `R_full = Fa / F0`, the plain ratio of the angles. As the coefficient falls toward 0 it tends to the Legacy tangent ratio.
5. The blend weight `w` by transition type (`AimingFovSensitivityTransitionType`): StartAiming 0 gives 1 whenever the alpha is above 1e-8 (UI: While Transitioning); AimingAlpha 1 gives the alpha itself (UI: ADS Transition, the default); EndAiming 2 gives 1 only when the alpha is within 1e-8 of 1 (UI: Transition Finished); IsAiming 3 gives 1 while the aiming state is on (UI: Instant). The result is `R = 1 + (R_full - 1) * w`.

The caller multiplies the 2D look value by `R` (and by a gamepad-only look acceleration factor that is 1 for the mouse: it is gated by the gamepad-input check `0x6C04740` and the gamepad look acceleration setting) before `AddYawInput` / `AddPitchInput`. So the FOV factor does not touch hip fire (alpha 0 gives `w = 0` for the default type, and the other types also give 0 outside aiming).

Default constants: `AimingFovMode` Affected (0), `AimingFovSensitivityMode` Relative (0), `AimingSensitivityRelativeCoefficient` 100 (the settings constructor `0x6EAE210` stores 0 at `+0x654` and the float `0x42C80000` = 100.0 at `+0x65C`); the transition default is the DA default index 1 = AimingAlpha. The `MouseADSSensitivityMultiplier` (aiming tag state config) has no data row in this dump (BHFramework setting [`DA_Setting_Controls_SensitivityMultiplier`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHFramework/Content/Settings/Controls/DA_Setting_Controls_SensitivityMultiplier.json): 0.01 to 5, default 1.0 is the matching template); treated as default 1.0.

How the ADS multiplier combines: it multiplies inside the axis step (section 1); `R` multiplies after it, in the look handler. They are independent factors: `ADS = hip * MouseADSMultiplier * R`.

### The 4x scope example (defaults, 800 DPI, 16:9)

`F0 = 90`; a 4x sight is at or above 3.25 so `base = 72`, `Fa = 72/4 = 18`, `R_full = 18/90 = 0.2` (Relative, coefficient 100), `w = 1` at full aim. Degrees per count = `0.028 * 1.0 * 0.2 = 0.0056`; counts per 360 = 64,286; 204.1 cm per 360. More cases (R_full):

| Sight and mode | Fa | Relative 16:9 | Relative 21:9 | Relative 16:10 | Legacy |
|---|---|---|---|---|---|
| 4x (Affected or Independent) | 18 | 0.2000 | 0.2229 | 0.1932 | 0.1584 |
| 2x, Affected | 45 | 0.5000 | 0.5414 | 0.4869 | 0.4142 |
| 3x, Affected | 30 | 0.3333 | 0.3677 | 0.3229 | 0.2679 |
| 6x, Affected | 12 | 0.1333 | 0.1490 | 0.1287 | 0.1051 |
| 10x, Affected | 7.2 | 0.0800 | 0.0896 | 0.0772 | 0.0629 |
| 1.2x reflex, Affected | 75 | 0.8333 | 0.8578 | 0.8247 | 0.7673 |
| 1.2x reflex, Independent | 60 | 0.6667 | 0.7051 | 0.6539 | 0.5774 |

## 6. Gaps and caveats

- Link 2 (Sensitivity 0.07 on `Mouse2D`) is inferred from engine behaviour and the project's gamepad re-adds; if wrong, every figure here is 14.29 times slower than the true value.
- The mask rule in section 3 is derived from data patterns, not from the mask code. If the true Maximum were not 1.0 the slider labels would shift but the stored-value formulas would not.
- `MouseVerticalAxisSensitivityMultiplier` has no found reader; treated as 1.
- `WDAimAssistInputModifier` on [`IA_Look`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Look.json) was not traced; it is an aim assist (target pull and slowdown) and is assumed to be a gamepad feature.
- Mouse smoothing (`bEnableMouseSmoothing=true` in the engine base config) belongs to the legacy axis path; whether it touches Enhanced Input mouse values was not traced. It would change timing, not the total rotation per count.
- The first-person camera's own `FOV` and view model FOV do not feed this formula; only the camera manager's `DefaultFOV` does.
- Vehicle and helicopter mouse sensitivities use other multipliers (`LandVehicleSensitivityMultiplier`, `AirVehicleSensitivityMultiplier`, the rotary mouse settings) and are not covered here.

## Wiki updates

- `_wiki/game-mechanics/controls-and-settings.md`: add the "Mouse sensitivity formula" subsection under "Aim and sensitivity" (formula, worked values, cm/360 table, ADS factor); change the Sensitivity row and the header row to say the default 0.4 is the stored value and the slider shows about 0.73.
