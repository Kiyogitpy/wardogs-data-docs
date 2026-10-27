---
title: "Aim Assist Curves and Target Score"
redirect_from: ["/Wardogs_AimAssistCurves_v1.html", "/Wardogs_AimAssistCurves_v1"]
parent: "Weapons & Ammo"
description: "Every aim-assist distance curve with its keys, which curve each weapon class uses, the target-score fields and formula, and the seven unnamed settings floats"
---

# Wardogs - Aim Assist Curves and Target Score

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) - [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

The curves and the fields of `BHAimAssistSettingsData` that [Items, section 9](Wardogs_Items_v2.md) does not tabulate. The stored strengths, reticle sizes, rates and pull modes are on that page; the player-facing summary is [Aim Assist](../_wiki/game-mechanics/aim-assist.md). Nothing here was measured in the game. Labels: **Data** for what the export says, **Native** for what the traced code does, **Default** for a constructor value the asset leaves out, **Inferred** for a reading not confirmed in code. Regenerate the tables with `python -I _tools/aim_assist_tables.py --write`.

## Distance curves (Data)

Pull and slow strength are multiplied by these curves. The key is the distance to the target in centimetres (inferred: the target range is stored in the same units), the value is a 0 to 1 factor. Hip fire uses short curves (full strength from 6 m to 20 m, gone at 25 m), aiming down sights uses long ones that fade out between 125 m and 300 m depending on the class. The sniper has a dead zone below 1.5 m on its pull curve.

<!-- aim_assist curves -->
| Curve | Keys (distance in cm, strength 0 to 1) |
|---|---|
| `C_AimAssistPullStrengthDistanceCurve_AR_ADS` | (0, 0), (200, 1), (22500, 1), (25000, 0) |
| `C_AimAssistPullStrengthDistanceCurve_Default` | (0, 0), (600, 1), (2000, 1), (2500, 0) |
| `C_AimAssistPullStrengthDistanceCurve_LMG_ADS` | (0, 0), (200, 1), (20000, 1), (22500, 0) |
| `C_AimAssistPullStrengthDistanceCurve_Pistol_ADS` | (0, 0), (200, 1), (10000, 1), (12500, 0) |
| `C_AimAssistPullStrengthDistanceCurve_SMG_ADS` | (0, 0), (200, 1), (12500, 1), (15000, 0) |
| `C_AimAssistPullStrengthDistanceCurve_Shotgun_ADS` | (0, 0), (200, 1), (17500, 1), (20000, 0) |
| `C_AimAssistPullStrengthDistanceCurve_Sniper` | (0, 0), (150, 0), (200, 1), (15000, 1), (20000, 0) |
| `C_AimAssistReticleEdgeFalloff_Default` | (0, 0.2), (1, 1) (key is the position inside the reticle, 0 at the centre and 1 at the edge, not a distance) |
| `C_AimAssistSlowStrengthDistanceCurvePistol_ADS` | (0, 0), (2000, 0.8), (4000, 1), (10000, 1), (12500, 0) |
| `C_AimAssistSlowStrengthDistanceCurveShotgun_ADS` | (0, 0), (2000, 0.8), (4000, 1), (17500, 1), (20000, 0) |
| `C_AimAssistSlowStrengthDistanceCurve_AR_ADS` | (0, 0), (2000, 0.8), (4000, 1), (20000, 1), (22500, 0) |
| `C_AimAssistSlowStrengthDistanceCurve_Default` | (0, 0), (600, 1), (2000, 1), (2500, 0) |
| `C_AimAssistSlowStrengthDistanceCurve_LMG_ADS` | (0, 0), (2000, 0.8), (4000, 1), (20000, 1), (30000, 0) |
| `C_AimAssistSlowStrengthDistanceCurve_SMG_ADS` | (0, 0), (2000, 0.8), (4000, 1), (15000, 1), (20000, 0) |
| `C_AimAssistSlowStrengthDistanceCurve_Sniper` | (0, 0), (2000, 1), (27500, 1), (30000, 0) |
| `C_AimAssistTargetWeightCurve` | (0, 0), (0.01, 1), (1, 1) (key unit not named in the export) |
<!-- /aim_assist -->

## Which curve each class uses (Data)

A dash means the asset omits the field. The RPG asset (shared by the RPG-7, 9K333 Verba, MGL-40 and MAAWS) zeroes its strengths and sets no curves except the target weight. The sniper omits the hip curves because its hip pull and slow strengths are 0. Melee has no ADS curve because its ADS strengths are 0.

<!-- aim_assist classes -->
| Field | AR | LMG | SMG | Shotgun | SR | Pistol | Melee | RPG |
|---|---|---|---|---|---|---|---|---|
| Hip pull curve | `PullStrengthDistanceCurve_Default` | `PullStrengthDistanceCurve_Default` | `PullStrengthDistanceCurve_Default` | `PullStrengthDistanceCurve_Default` | - | `PullStrengthDistanceCurve_Default` | `PullStrengthDistanceCurve_Default` | - |
| ADS pull curve | `PullStrengthDistanceCurve_AR_ADS` | `PullStrengthDistanceCurve_LMG_ADS` | `PullStrengthDistanceCurve_SMG_ADS` | `PullStrengthDistanceCurve_Shotgun_ADS` | `PullStrengthDistanceCurve_Sniper` | `PullStrengthDistanceCurve_Pistol_ADS` | - | - |
| Hip slow curve | `SlowStrengthDistanceCurve_Default` | `SlowStrengthDistanceCurve_Default` | `SlowStrengthDistanceCurve_Default` | `SlowStrengthDistanceCurve_Default` | - | `SlowStrengthDistanceCurve_Default` | `SlowStrengthDistanceCurve_Default` | - |
| ADS slow curve | `SlowStrengthDistanceCurve_AR_ADS` | `SlowStrengthDistanceCurve_LMG_ADS` | `SlowStrengthDistanceCurve_SMG_ADS` | `SlowStrengthDistanceCurveShotgun_ADS` | `SlowStrengthDistanceCurve_Sniper` | `SlowStrengthDistanceCurvePistol_ADS` | - | - |
| Reticle edge falloff | `ReticleEdgeFalloff_Default` | `ReticleEdgeFalloff_Default` | `ReticleEdgeFalloff_Default` | `ReticleEdgeFalloff_Default` | `ReticleEdgeFalloff_Default` | `ReticleEdgeFalloff_Default` | `ReticleEdgeFalloff_Default` | - |
| Target weight curve | `TargetWeightCurve` | `TargetWeightCurve` | `TargetWeightCurve` | `TargetWeightCurve` | `TargetWeightCurve` | `TargetWeightCurve` | `TargetWeightCurve` | `TargetWeightCurve` |
| `SensitivityScale` (hip) | - | - | - | - | 0 | - | - | 0 |
| `SensitivityScaleADS` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| `StrengthScale` | - | - | - | - | - | - | - | 0 |
| `TargetScore_AssistWeight` | - | - | - | - | - | - | - | 0 |
| `TargetScore_ViewDot` | - | - | - | - | - | - | - | 0 |
| `TargetScore_ViewDotOffset` | - | - | - | - | - | - | - | 0 |
| `TargetScore_ViewDistance` | 1 | - | 1 | - | - | - | - | 0 |
| `TargetScore_RenderedRecently` | - | - | - | - | - | - | - | - |
| `bFOVReticleScaling` | no | no | no | no | no | no | no | - |
| `bApplySlowing` | - | - | - | - | - | - | - | no |
| `bUseDynamicSlow` | - | - | - | - | - | - | - | no |
| `bApplyStrafePullScale` | - | - | - | - | - | - | - | no |
<!-- /aim_assist -->

## Target score (Native)

For each candidate in front of the camera the target-collection routine (`0x6763510`) computes one score and trims the list to `MaxNumberOfTargets` (8 in every asset; the constructor default is 6). A target behind the camera (view dot not above 0) is dropped before scoring, as is one that fails the routine's visibility test (a virtual call at `+0x510`; smoke blocks here, see [Aim Assist](../_wiki/game-mechanics/aim-assist.md)).

```
score = lastWeight * TargetScore_AssistWeight
      + (viewDot * TargetScore_ViewDot - TargetScore_ViewDotOffset)
      + (1 - distance / range) * TargetScore_ViewDistance
      + (target rendered recently ? TargetScore_RenderedRecently : 0)
```

- `lastWeight` is the weight the same target had on the previous update (element `+108` of the 160-byte target record), or the default weight for a new target.
- `viewDot` is the dot product of the camera's forward vector with the unit vector to the target (1 straight ahead). `distance` is camera to target, `range` is `TargetRange`, divided by the FOV scale when `bFOVReticleScaling` is on (it is off in every asset).
- The constructor defaults (**Default**, from `0x6760E9E`) are: AssistWeight 10, ViewDot 50, ViewDotOffset 40, ViewDistance 0.25, RenderedRecently 1000. Assault rifle and SMG assets set `TargetScore_ViewDistance` to 1; every other class keeps 0.25. The RPG asset sets all five to 0.
- The check before the last term is a native call (`0x43AAA8D0`) on the target's component. Its body is not in the decompiled corpus; the field name and the call shape fit a "was this component rendered recently" test (**Inferred**).
- With these defaults a recently rendered target gets +1000, far above the other terms (the weight term is at most 10, the view terms at most 10 and 1), so a target on screen always outranks one that is not.

After scoring, each target's weight is recomputed in `0x6766850`: it is `TargetWeightCurve` evaluated by the collecting component (clamped to 0 to 1), the weights are divided by their sum, and each is then floored at `MinAssistWeight` (0.125 in every asset; the constructor default is 0.25). The curve is the same asset for every class: 0 at key 0, 1 at key 0.01, then flat at 1. The argument the curve is evaluated at is not visible in the decompiled code (**not traced**).

`StrengthScale` multiplies the final pull (`0x6765BF0`); only the RPG asset sets it (0).

## Unnamed settings floats (Data, partly Native)

Seven floats in the settings asset have hashed names in the export. Their offsets are from the SDK. Melee omits `0x3B8` to `0x3C8`, so it keeps the constructor values (0.25, 0.25, 0.6, 1.0, 0.25). The two at `0x3B8` and `0x3BC` are the look and move input thresholds that gate the pull ([Items](Wardogs_Items_v2.md), section 9). `0x3B4` is read by the pull routine (`0x6765BF0`) in a ratio that is clamped to at most 10; the other four were not matched to a use (**not traced**).

<!-- aim_assist hashed -->
| Unnamed field | Settings offset | AR | LMG | SMG | Shotgun | SR | Pistol | Melee | RPG |
|---|---|---|---|---|---|---|---|---|---|
| `_aaablbcidfbimhkninjgh` | `0x3B0` | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | - |
| `_aaabohfjefmdjckeghchd` | `0x3B4` | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 | - |
| `_aaabifkkogdgdilllniki` | `0x3B8` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | - | - |
| `_aaabiopcjcdaaocfaifcm` | `0x3BC` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | - | - |
| `_aaabgnegmcifdipjmhfdb` | `0x3C0` | 0.75 | 0.75 | 0.75 | 0.75 | 0.75 | 0.75 | - | - |
| `_aaabkejidmenonabgonll` | `0x3C4` | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | 2.5 | - | - |
| `_aaabfibckgemadeemoaha` | `0x3C8` | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | - | - |
<!-- /aim_assist -->
