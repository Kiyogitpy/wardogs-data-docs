---
title: "Significance"
redirect_from: ["/Wardogs_Significance_v2.html", "/Wardogs_Significance_v2"]
parent: "World, Visuals & Audio"
description: "Significance settings (update rates per level) and the sphere and field-of-view evaluators."
---

# Wardogs — Significance Reference
*Extracted from cooked game data (JSON export, `Wardogs/Content/Significance/`, 15 source files: 8 significance settings, 2 FOV evaluators, 5 sphere evaluators). Parsed with a Python script. Values are the raw exported values.*

> **What this is:** the significance system decides how often each object type updates, based on distance and (for some types) whether it is in view. Each **settings** asset is one object category. It lists which **evaluators** to use and gives a timing row per significance level. The evaluators hold the distance and cone thresholds that place an object in a level.

---

## 1. Asset Families

| Family | Count | Type | Role |
|---|---|---|---|
| Settings | 8 | `BHSignificanceSettingsAsset` | One per object category; picks evaluators and timing per level |
| Sphere evaluators | 5 | `BHSignificanceEvaluator_Sphere` | Distance thresholds (one per level) |
| FOV evaluators | 2 | `BHSignificanceEvaluator_FOV` | Distance and cone-angle thresholds (one per level) |

---

## 2. Settings Assets (8)

Each row is one settings asset. Each cell gives the timing for that significance level as `TickRate / SignificanceUpdateRate / LocationUpdateRate`. Level 0 is the highest significance (presumably closest or most relevant). Blank cells mean the asset has no entry for that level.

| Settings asset | Evaluators | L0 | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|---|---|
| `DA_SignificanceSettings_Default` | Sphere_Default | 0 / 0.03 / 0.03 | 0.03 / 0.1 / 0.1 | 0.06 / 0.3 / 1.0 | 0.1 / 1.0 / 2.0 | | |
| `DA_SignificanceSettings_PrimaryMovable` | Sphere_Default, FOV_Primary | 0 / 0.03 / 0.03 | 0.03 / 0.1 / 0.1 | 0.06 / 0.3 / 1.0 | 0.1 / 1.0 / 2.0 | | |
| `DA_SignificanceSettings_RotaryVehicle` | Sphere_Default, FOV_Primary | 0 / 0.03 / 0.03 | 0.03 / 0.1 / 0.1 | 0.06 / 0.3 / 1.0 | 0.1 / 1.0 / 2.0 | | |
| `DA_SignificanceSettings_HoldableWeapon` | Sphere_HoldableWeapon | 0 / 0.15 / 0.03 | 0.1 / 0.25 / 0.1 | 0.33 / 0.5 / 1.0 | 0.75 / 1.0 / 2.0 | | |
| `DA_SignificanceSettings_NPP` | Sphere_NPP, FOV_NPP | −1 / 0.03 / 0.03 | −1 / 0.03 / 0.03 | −1 / 0.06 / 0.06 | −1 / 0.09 / 0.09 | −1 / 0.12 / 0.12 | −1 / 0.12 / 0.12 |
| `DA_SignificanceSettings_WorldInteractionComponent` | Sphere_Default | 0 / 0.03 / 0.03 | 0.03 / 0.1 / 0.1 | 0.3 / 0.3 / 0.3 | −1 / 1.0 / 1.0 | | |
| `DA_SignificanceSettings_WorldMovementEffectsComponent` | Sphere_MovementEffectsComponent | 0 / 0.3 / 0.5 | −1 / 1.0 / 1.0 | | | | |
| `DA_SignificanceSettings_BudgetedCharacterMesh` | Sphere_BudgetedCharacterMesh | 0 / 0.03 / 0.03 | 0 / 0.1 / 0.1 | 0 / 0.1 / 0.1 | | | |

Column notes:
- `TickRate` of **−1** appears on every NPP level, on the last level of WorldInteractionComponent, and on the last level of WorldMovementEffectsComponent. It is probably a "do not tick" sentinel, but the export does not say.
- The number of levels for each asset equals the number of entries in its sphere evaluator's `Settings` list (see section 3). This suggests each level maps one-to-one to a distance threshold.
- The timing values appear to be in seconds (0.03 is roughly 33 ms, one frame at 30 Hz). Not confirmed.

Timing patterns:
- Default, PrimaryMovable and RotaryVehicle all use the same four-level ramp (0.03 → 0.1 → 0.3 → 1.0 in significance). Their timings are identical, but their evaluators differ (see section 4).
- HoldableWeapon re-evaluates significance more slowly than Default at the closest levels (significance update 0.15 / 0.25 / 0.5 against Default's 0.03 / 0.1 / 0.3). Its tick rates are also coarser (0 / 0.1 / 0.33 / 0.75 against 0 / 0.03 / 0.06 / 0.1). Its location timings match Default.
- NPP has the most levels (6), and its last two levels share the same timing (0.12 / 0.12).

---

## 3. Sphere Evaluators (5)

`Settings` lists `Distance` thresholds. Entries are in ascending distance order.

| Evaluator | Distance thresholds (`Settings[i].Distance`) | Levels |
|---|---|---|
| `DA_Significance_Evaluator_Sphere_BudgetedCharacterMesh` | 0, 500, 1,000 | 3 |
| `DA_Significance_Evaluator_Sphere_Default` | 0, 1,000, 2,500, 5,000 | 4 |
| `DA_Significance_Evaluator_Sphere_HoldableWeapon` | 0, 1,000, 3,000, 8,000 | 4 |
| `DA_Significance_Evaluator_Sphere_MovementEffectsComponent` | 0, 7,500 | 2 |
| `DA_Significance_Evaluator_Sphere_NPP` | 0, 1,000, 2,500, 5,000, 10,000, 25,000 | 6 |

Distances are in the export's engine units. If they are Unreal cm, the Default thresholds are 0, 10, 25 and 50 m.

---

## 4. FOV Evaluators (2)

`FOVLevelSettings` lists `(Distance, ConeAngle)` pairs. Entries are in descending distance order, which is the reverse of the sphere lists.

| Evaluator | (Distance, ConeAngle°) pairs | Levels |
|---|---|---|
| `DA_Significance_Evaluator_FOV_Primary` | (50,000, 15), (35,000, 25), (20,000, 35), (10,000, 40) | 4 |
| `DA_Significance_Evaluator_FOV_NPP` | (100,001, 15), (50,000, 20), (25,000, 30), (10,000, 50), (5,000, 60), (2,500, 90) | 6 |

The cone angle widens as distance falls: the narrowest cone (15°) applies at the longest range, and the widest (90° for NPP) at the shortest. This reads as "far objects count only if nearly in front of the camera, close objects count from almost any angle". That is an inference from the values, not confirmed.

---

## 5. Evaluator Wiring

| Evaluator | Used by |
|---|---|
| Sphere_Default | Default, PrimaryMovable, RotaryVehicle, WorldInteractionComponent |
| FOV_Primary | PrimaryMovable, RotaryVehicle |
| Sphere_NPP and FOV_NPP | NPP (the only settings asset that uses an NPP-specific FOV evaluator) |
| Sphere_HoldableWeapon | HoldableWeapon |
| Sphere_MovementEffectsComponent | WorldMovementEffectsComponent |
| Sphere_BudgetedCharacterMesh | BudgetedCharacterMesh |

Every one of the seven evaluators is referenced by at least one settings asset.

---

## 6. How Values Combine

- **Level choice** (inferred): an object's distance selects the highest level whose sphere threshold it has passed. FOV evaluators, where present, add a second check on the cone angle.
- **Timing** comes from the settings row for the chosen level: `TickRate` (how often it ticks), `SignificanceUpdateRate` (how often significance is re-evaluated) and `LocationUpdateRate` (how often its location is refreshed). The combination is not stated in the export.
- **Sharing:** Default, PrimaryMovable and RotaryVehicle have the same timing rows but different evaluator sets, so PrimaryMovable and RotaryVehicle get the FOV check that plain Default does not.

---

## 7. Still Not Pulled / Limitations

- **Units are not stated.** Distances are assumed to be cm and timings seconds. Both are inferences.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **The level-selection rule** (distance threshold or FOV check first, and whether it is hysteresis-based) is not in the export.
- **The `TickRate = −1` meaning** is unconfirmed.
- **Which systems consume each category** (for example, which actors use the NPP settings) is not in this folder. Only the category names are given.
- **Engine defaults** for fields not set in the export are not included.
