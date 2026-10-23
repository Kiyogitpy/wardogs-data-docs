---
title: "BHAimAssist"
redirect_from: ["/Wardogs_Plugin_BHAimAssist_v2.html", "/Wardogs_Plugin_BHAimAssist_v2"]
parent: "Player & Movement"
description: "What This Plugin Holds, Pull Strength Curves, Slow Strength Curves, Reticle Edge Falloff"
---

# Wardogs — Plugin: BHAimAssist
*Extracted from cooked game data (UE 5.7 export JSON). Source folder: [`Plugins/BHAimAssist/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/BHAimAssist) — 16 JSON files, all `CurveFloat` assets under [`Content/AimAssist/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist). Curve keys were read directly; units are not stated in the export.*

---

## Season 02 update (2026-10-15)

- **Hipfire curves removed.** All 11 hipfire pull and slow curves are gone (AR, LMG, Melee, Pistol, SMG and Shotgun for pull; AR, LMG, Pistol, SMG and Shotgun for slow). Only the ADS curves remain, plus the new Default curves.
- **New Default curves.** `PullStrengthDistanceCurve_Default` (0:0, 600:1, 2000:1, 2500:0) and `SlowStrengthDistanceCurve_Default` (0:0, 600:1, 2000:1, 2500:0) were added.
- **Reticle edge falloff reduced to one curve.** The AR, LMG, Pistol, SMG and Shotgun falloff curves were removed. `ReticleEdgeFalloff_Default` now has two keys (0:0.2, 1:1), was 0:0.05, 0.5:0.2, 0.8:0.55, 1:1.
- **Target weight.** [`C_AimAssistTargetWeightCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistTargetWeightCurve.json) now reaches 1 at input 0.01 (was 0.5 at 0.05, 1 at 1.0).
- **Pull ramp.** ADS pull curves now reach full strength at 200 (was 400). The sniper pull is still 0 at 150 and reaches full at 200.
- **Pull plateau ends and fall-off, ADS (old → new):**
  - AR: plateau end 12000 → 22500, falls to 0 at 30000 → 25000
  - LMG: plateau end 20000 → 20000 (same), falls to 0 at 50000 → 22500
  - Pistol: falls to 0 at 10000 → 12500
  - SMG: falls to 0 at 20000 → 15000
  - Shotgun: falls to 0 at 15000 → 20000
  - Sniper: plateau end 5000 → 15000, falls to 0 at 10000 → 20000
- **Slow ramp, ADS.** Slow ADS curves now reach 0.8 at 2000 and full at 4000 (was 0.5 at 300 and full at 1200). The sniper slow curve reaches full at 2000 (was 1200).
- **Slow fall-off, ADS.** LMG slow falls to 0 at 50000 → 30000. AR slow falls to 0 at 30000 → 22500. The other ADS slow curves now end between 12500 and 30000.
- The official patch notes list an aim assist strength slider in Settings and changes to Aim Acceleration. This page covers the curve data only.

---

## 1. What This Plugin Holds

The aim-assist tuning curves. Each curve is a `CurveFloat` that maps a value (usually distance) to a strength between 0 and 1. The plugin has no data assets, GameFeatures, or code-facing settings; the game code reads these curves by name.

Three curve families, plus one target-weight curve:

| Family | Count | Input | Output (strength) |
|---|---|---|---|
| **PullStrengthDistanceCurve** | 7 | Distance | How hard the reticle is pulled toward a target |
| **SlowStrengthDistanceCurve** | 7 | Distance | How much the aim is slowed near a target |
| **ReticleEdgeFalloff** | 1 | Normalised reticle position (0 at centre to 1 at edge) | Weight of the assist toward the reticle edge |
| **TargetWeightCurve** | 1 | Normalised input (0 to 1) | Weight of the target |

Pull and slow curves are split by weapon class and by aim state: **ADS** (aiming down sights) and **Default**. Weapon classes with ADS curves are AR, LMG, Pistol, SMG, Shotgun, and Sniper (the sniper curves have no `_ADS` suffix). The Default curves are not tied to a weapon class.

---

## 2. Pull Strength Curves

Keys are `Time:Value`. In the export, time is the distance.

| Curve | Key points (distance: strength) | Plateau | Falls to 0 at |
|---|---|---|---|
| `PullStrengthDistanceCurve_AR_ADS` | 0:0, 200:1, 22500:1, 25000:0 | 200 to 22500 | 25000 |
| `PullStrengthDistanceCurve_Default` | 0:0, 600:1, 2000:1, 2500:0 | 600 to 2000 | 2500 |
| `PullStrengthDistanceCurve_LMG_ADS` | 0:0, 200:1, 20000:1, 22500:0 | 200 to 20000 | 22500 |
| `PullStrengthDistanceCurve_Pistol_ADS` | 0:0, 200:1, 10000:1, 12500:0 | 200 to 10000 | 12500 |
| `PullStrengthDistanceCurve_SMG_ADS` | 0:0, 200:1, 12500:1, 15000:0 | 200 to 12500 | 15000 |
| `PullStrengthDistanceCurve_Shotgun_ADS` | 0:0, 200:1, 17500:1, 20000:0 | 200 to 17500 | 20000 |
| `PullStrengthDistanceCurve_Sniper` | 0:0, 150:0, 200:1, 15000:1, 20000:0 | 200 to 15000 | 20000 |

Pattern: every ADS curve is 0 at the origin, reaches full by 200, holds, then falls off. The sniper stays at 0 until 150. The Default curve ramps to full at 600 and falls off by 2500, so it holds to much shorter distances than the ADS curves.

---

## 3. Slow Strength Curves

| Curve | Key points (distance: strength) | Plateau | Falls to 0 at |
|---|---|---|---|
| `SlowStrengthDistanceCurve_AR_ADS` | 0:0, 2000:0.8, 4000:1, 20000:1, 22500:0 | 4000 to 20000 | 22500 |
| `SlowStrengthDistanceCurve_Default` | 0:0, 600:1, 2000:1, 2500:0 | 600 to 2000 | 2500 |
| `SlowStrengthDistanceCurve_LMG_ADS` | 0:0, 2000:0.8, 4000:1, 20000:1, 30000:0 | 4000 to 20000 | 30000 |
| `SlowStrengthDistanceCurvePistol_ADS` | 0:0, 2000:0.8, 4000:1, 10000:1, 12500:0 | 4000 to 10000 | 12500 |
| `SlowStrengthDistanceCurve_SMG_ADS` | 0:0, 2000:0.8, 4000:1, 15000:1, 20000:0 | 4000 to 15000 | 20000 |
| `SlowStrengthDistanceCurveShotgun_ADS` | 0:0, 2000:0.8, 4000:1, 17500:1, 20000:0 | 4000 to 17500 | 20000 |
| `SlowStrengthDistanceCurve_Sniper` | 0:0, 2000:1, 27500:1, 30000:0 | 2000 to 27500 | 30000 |

Note the naming: the Pistol and Shotgun ADS slow curves use `SlowStrengthDistanceCurvePistol_ADS` and `SlowStrengthDistanceCurveShotgun_ADS` (no underscore before the weapon class). Keep the spelling when searching.

Slow curves ramp more gently than pull curves. The ADS slow curves reach 0.8 at 2000 and full at 4000, and the sniper reaches full at 2000. The Default curve reaches full at 600.

---

## 4. Reticle Edge Falloff

Input is the normalised reticle position (0 at centre, 1 at edge). Output is the assist weight.

| Curve | Key points (input: weight) |
|---|---|
| `ReticleEdgeFalloff_Default` | 0:0.2, 1:1 |

This is the only reticle edge falloff curve in the current data. The AR, LMG, Pistol, SMG and Shotgun curves are no longer present.

---

## 5. Target Weight

| Curve | Key points (input: weight) |
|---|---|
| [`C_AimAssistTargetWeightCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistTargetWeightCurve.json) | 0:0, 0.01:1, 1:1 |

Target weight reaches 1 at input 0.01 and holds at 1 through 1.0.

---

## 6. How Values Combine

These are general aim-assist semantics. The curves are read by name in game code, and the code's combination rule is not in this export.

- The **pull** curve gives the magnetic pull toward a target by distance. It is zero at close range, reaches full within 200 on ADS curves (600 on Default), and falls off at long range.
- The **slow** curve reduces aim speed near a target. It reaches full later than the pull curve on ADS (4000 against 200).
- The **reticle edge** falloff weights the assist as the target drifts toward the reticle edge.
- The **target weight** scales each target's contribution.
- The **ADS vs Default** split means the assist strength is selected by the curve set the game code uses. The selection rule is not in this export.

Related setting: the BHFramework `AimAssistSensitivityMultiplier` (max 1.5, default 1.0). It is presumed to scale aim-assist strength; the code path is not confirmed in this folder.

---

## 7. Still not pulled / limitations

- **Units.** The time axis is named "Time" in the curve, but it is used as distance (key values 150 to 30000). The unit is assumed to be Unreal units (cm). Not confirmed by the export.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Code path.** Which code reads each curve, and how the reticle and target inputs are normalised, is not in this folder.
- **Weapon mapping.** How a weapon maps to a curve family (AR, LMG and so on) is in the weapon data, not here.
- **Curve tangents.** Only key time and value are summarised. Tangents and interpolation modes were not reported.
