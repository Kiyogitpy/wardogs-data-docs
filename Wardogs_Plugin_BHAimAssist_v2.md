---
title: "BHAimAssist"
parent: "Plugins"
---

# Wardogs — Plugin: BHAimAssist (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/BHAimAssist/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/BHAimAssist) — 30 JSON files, all `CurveFloat` assets under [`Content/AimAssist/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist). Curve keys were read directly; units are not stated in the export.*

---

## 1. What This Plugin Holds

The aim-assist tuning curves. Each curve is a `CurveFloat` that maps a value (usually distance) to a strength between 0 and 1. The plugin has no data assets, GameFeatures, or code-facing settings; the game code reads these curves by name.

Three curve families, plus one target-weight curve:

| Family | Count | Input | Output (strength) |
|---|---|---|---|
| **PullStrengthDistanceCurve** | 12 | Distance | How hard the reticle is pulled toward a target |
| **SlowStrengthDistanceCurve** | 12 | Distance | How much the aim is slowed near a target |
| **ReticleEdgeFalloff** | 6 | Normalised reticle position (0 at centre to 1 at edge) | Weight of the assist toward the reticle edge |
| **TargetWeightCurve** | 1 | Normalised input (0 to 1) | Weight of the target |

Pull and slow curves are split by weapon class and by aim state: **ADS** (aiming down sights) and **Hipfire**. Weapon classes are AR, LMG, Pistol, SMG, Shotgun, Sniper, and Melee (melee has hipfire only).

---

## 2. Pull Strength Curves

Keys are `Time:Value`. In the export, time is the distance.

| Curve | Key points (distance: strength) | Plateau | Falls to 0 at |
|---|---|---|---|
| `PullStrengthDistanceCurve_AR_ADS` | 0:0, 150:0, 400:1, 12000:1, 20000:0.6, 26000:0.25, 30000:0 | 400 to 12000 | 30000 |
| `PullStrengthDistanceCurve_AR_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 1900:1, 2100:0.75, 2300:0.5, 2500:0 | 600 to 1900 | 2500 |
| `PullStrengthDistanceCurve_LMG_ADS` | 0:0, 150:0, 400:1, 20000:1, 35000:0.6, 45000:0.25, 50000:0 | 400 to 20000 | 50000 |
| `PullStrengthDistanceCurve_LMG_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 1500:1, 1750:0.75, 2000:0.5, 2100:0 | 600 to 1500 | 2100 |
| `PullStrengthDistanceCurve_Melee_Hipfire` | 0:0, 150:0, 200:1, 500:1, 700:0.4, 800:0 | 200 to 500 | 800 |
| `PullStrengthDistanceCurve_Pistol_ADS` | 0:0, 150:0, 400:1, 5000:1, 7500:0.6, 9000:0.25, 10000:0 | 400 to 5000 | 10000 |
| `PullStrengthDistanceCurve_Pistol_Hipfire` | 0:0, 150:0, 400:1, 1000:1, 1500:0.75, 2000:0.5, 2100:0 | 400 to 1000 | 2100 |
| `PullStrengthDistanceCurve_SMG_ADS` | 0:0, 150:0, 400:1, 8000:1, 14000:0.6, 18000:0.25, 20000:0 | 400 to 8000 | 20000 |
| `PullStrengthDistanceCurve_SMG_Hipfire` | 0:0, 150:0, 400:1, 1000:1, 2000:0.75, 2500:0 | 400 to 1000 | 2500 |
| `PullStrengthDistanceCurve_Shotgun_ADS` | 0:0, 150:0, 400:1, 7000:1, 11000:0.6, 13500:0.25, 15000:0 | 400 to 7000 | 15000 |
| `PullStrengthDistanceCurve_Shotgun_Hipfire` | 0:0, 150:0, 400:1, 1000:1, 2000:0.75, 2500:0 | 400 to 1000 | 2500 |
| `PullStrengthDistanceCurve_Sniper` | 0:0, 150:0, 400:1, 5000:1, 8000:0.5, 10000:0 | 400 to 5000 | 10000 |

Pattern: every curve is 0 inside 150, ramps to full by 400, holds, then falls off. ADS curves hold to much longer distances than hipfire (AR ADS to 12000 against AR hipfire to 1900), and the sniper's fall-off is steepest in relative terms.

---

## 3. Slow Strength Curves

| Curve | Key points (distance: strength) | Plateau | Falls to 0 at |
|---|---|---|---|
| `SlowStrengthDistanceCurve_AR_ADS` | 0:0, 150:0, 1500:0.45, 3000:0.5, 9000:1, 20000:1, 25000:0.6, 30000:0 | 9000 to 20000 | 30000 |
| `SlowStrengthDistanceCurve_AR_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 2000:1, 2200:0.75, 2400:0.5, 2500:0 | 600 to 2000 | 2500 |
| `SlowStrengthDistanceCurve_LMG_ADS` | 0:0, 150:0, 300:0.5, 1200:1, 25000:1, 40000:0.6, 47000:0.3, 50000:0 | 1200 to 25000 | 50000 |
| `SlowStrengthDistanceCurve_LMG_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 2000:1, 2500:0.75, 3000:0.5, 3100:0 | 600 to 2000 | 3100 |
| `SlowStrengthDistanceCurvePistol_ADS` | 0:0, 150:0, 300:0.5, 1200:1, 6000:1, 8000:0.6, 9500:0.3, 10000:0 | 1200 to 6000 | 10000 |
| `SlowStrengthDistanceCurve_Pistol_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 2000:1, 2500:0.75, 3000:0.5, 3100:0 | 600 to 2000 | 3100 |
| `SlowStrengthDistanceCurve_SMG_ADS` | 0:0, 150:0, 300:0.5, 1200:1, 10000:1, 16000:0.6, 19000:0.3, 20000:0 | 1200 to 10000 | 20000 |
| `SlowStrengthDistanceCurve_SMG_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 2000:1, 2500:0.75, 3000:0.5, 3100:0 | 600 to 2000 | 3100 |
| `SlowStrengthDistanceCurveShotgun_ADS` | 0:0, 150:0, 300:0.5, 1200:1, 8000:1, 12000:0.6, 14000:0.3, 15000:0 | 1200 to 8000 | 15000 |
| `SlowStrengthDistanceCurve_Shotgun_Hipfire` | 0:0, 150:0, 400:0.8, 600:1, 2000:1, 2500:0.75, 3000:0.5, 3100:0 | 600 to 2000 | 3100 |
| `SlowStrengthDistanceCurve_Sniper` | 0:0, 150:0, 300:0.5, 1200:1, 6000:1, 8500:0.4, 10000:0 | 1200 to 6000 | 10000 |

Note the naming: the Pistol and Shotgun ADS slow curves use `SlowStrengthDistanceCurvePistol_ADS` and `SlowStrengthDistanceCurveShotgun_ADS` (no underscore before the weapon class). Keep the spelling when searching.

Slow curves differ from pull curves in the early range: they reach 0.5 at 300 (ADS) or 400 (hipfire), before reaching full at 1200 or 600. Their fall-off is also more gradual in the far range on most ADS curves.

---

## 4. Reticle Edge Falloff

Input is the normalised reticle position (0 at centre, 1 at edge). Output is the assist weight.

| Curve | 0.0 | 0.5 | 0.8 | 1.0 |
|---|---|---|---|---|
| `ReticleEdgeFalloff_Default` | 0.05 | 0.2 | 0.55 | 1 |
| `ReticleEdgeFalloff_AR` | 0.2 | 0.55 | 0.85 | 1 |
| `ReticleEdgeFalloff_LMG` | 0.14 | 0.44 | 0.75 | 1 |
| `ReticleEdgeFalloff_Pistol` | 0.05 | 0.2 | 0.55 | 1 |
| `ReticleEdgeFalloff_SMG` | 0.05 | 0.2 | 0.55 | 1 |
| `ReticleEdgeFalloff_Shotgun` | 0.05 | 0.2 | 0.55 | 1 |

Pistol, SMG and Shotgun share the Default values. AR gives the highest weight at every point (0.2 at input 0, 0.55 at 0.5). LMG sits between AR and Default.

---

## 5. Target Weight

| Curve | Key points (input: weight) |
|---|---|
| [`C_AimAssistTargetWeightCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistTargetWeightCurve.json) | 0:0, 0.05:0.5, 1:1 |

Target weight rises steeply from 0 to 0.5 within the first 5% of the input, then linearly to 1 at 1.0.

---

## 6. How Values Combine

These are general aim-assist semantics. The curves are read by name in game code, and the code's combination rule is not in this export.

- The **pull** curve gives the magnetic pull toward a target by distance. It is zero close in (under 150) and at long range, and full in between.
- The **slow** curve reduces aim speed near a target. It is weaker than the pull inside 400 units and falls off earlier on hipfire.
- The **reticle edge** falloff weights the assist as the target drifts toward the reticle edge.
- The **target weight** scales each target's contribution.
- The **ADS vs hipfire** split means the assist strength is selected by the weapon's aim state.

Related setting: the BHFramework `AimAssistSensitivityMultiplier` (max 1.5, default 1.0). It is presumed to scale aim-assist strength; the code path is not confirmed in this folder.

---

## 7. Still not pulled / limitations

- **Units.** The time axis is named "Time" in the curve, but it is used as distance (values 150 to 50000). The unit is assumed to be Unreal units (cm). Not confirmed by the export.
- **Code path.** Which code reads each curve, and how the reticle and target inputs are normalised, is not in this folder.
- **Weapon mapping.** How a weapon maps to a curve family (AR, LMG and so on) is in the weapon data, not here.
- **Curve tangents.** Only key time and value are summarised. Tangents and interpolation modes were not reported.
