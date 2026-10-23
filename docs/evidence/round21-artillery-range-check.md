---
title: Round 21 artillery range check
nav_exclude: true
---

# Round 21 artillery range check

An outside reviewer said the artillery calculator's range tables (the "mil dial") are measurements and not derived from game data, that the dial looks offset by about 200 mil, and that a longest range of 2629 m implies a no-drag launch speed of about 161 m/s against the 300 m/s the data gives. This page tests the documented flight model against both the calculator's table and a log of the artillery's own impacts, **without fitting any parameter**, and reports where it holds and where it does not.

Nothing here changes a game fact. The model is the one on [Projectile Flight](../../pipelines/Wardogs_ProjectileFlight_v1.md) (sections 1, 4, 5, 8) with the shell data from [Artillery shell flight data](../../game-features/Wardogs_ArtilleryShellFlight_v1.md). Evidence level: static reading of the executable plus cooked data; the impact log is a third-party-style observation set, summarised here as aggregates only (no per-shot rows, positions or timestamps are in the repository).

Labels: **Derived** is arithmetic on documented data; **Measured** is a number taken from the impact log or the calculator table; **Assumed** is a convention or step choice the data does not settle.

## 1. Method

**Simulator.** [`_tools/shell_sim.py`](../../_tools/shell_sim.py) integrates the planar flight of one shell (no wind) from the documented equations only:

| Term | Value | Label |
|---|---|---|
| Muzzle speed | 30000 cm/s (`InitialBulletSpeed` of `DA_TNK_01_Artillery_Weapon_Stats`) | Derived (data) |
| Gravity | -980 cm/s^2 (`BaseEngine.ini`) | Derived (data) |
| Drag | `-(100/m) * 0.5 * 1.2 * Cd * (pi/4) * (D/100)^2 * (v/100)^2`, `Cd = DragModel.Value * Curve(v in m/s)` | Derived (native) |
| Curve | `GC (Cylinder)` row of `CT_Projectile_DragCoefficients`, linear, clamped beyond 600 m/s | Derived (data) |
| Standard shell | `Value` 80, mass 70 kg, diameter 8.4 cm | Derived (data) |
| Expensive shell | `Value` 2.5, mass 19 kg, diameter 10.5 cm | Derived (data) |
| Thrust, wind | none (`bShouldThrust` never set on 155 mm; wind taken as zero) | Derived / Assumed |
| Step | `a` from the velocity at the start of the step, `v1 = v + a*dt`, `dx = (v+v1)/2*dt` | Derived (native) |
| Lifetime | flight ends after 40 s (`MaxProjectileLifetime`) | Derived (data) |

**Step length (assumed).** The native step is `floor(1000/Rate)` ms and `Rate` was never located when this was written (open item 3 on the flight page). Round 23 found it: `SimulationFrameRate` is 30, a 33 ms step, which is inside the tested range. Results are given at 4 ms for the exploration and tested from 1 ms to 33 ms (Rate 30 to 1000). The step does not move any conclusion (section 4, last block).

**Mil to elevation (assumed).** The calculator's dial range runs 20 to 1390 mil; the artillery's pitch limits are 2 to 80 degrees (`MinWeaponPitchAngle`, `MaxWeaponPitchAngle` of `W_TNK_01_Artillery`). Three conventions are tested, none fitted: NATO (6400 per turn), Warsaw (6000 per turn) and the true milliradian (2000*pi per turn, 1 mil = 0.0573 degrees). The elevation is the barrel elevation above horizontal.

**Impact log.** 170 logged impacts of the self-propelled gun. 89 record a dial value and a fired arc; two of those show an exactly zero error (impact equal to plan) and are dropped as likely logger artefacts, leaving N = 87 usable shots (79 distinct plan/dial combinations; 18 with no recorded height difference, treated as 0). The residual is `predicted impact distance - measured impact distance` in metres, with the target height above the gun taken as the logged height difference (positive = target higher, **assumed**; the opposite sign is tested). The muzzle sits 0 to 3 m above the gun's ground in the tests; muzzle height is not in the exported data.

**Calculator table.** The third-party calculator lists, for the SPG, a low and a high arc as `[range m, mil]` pairs from 20 mil (1181 m) through the peak (2629 m at 600 to 620 mil) to 1400 mil (735 m). It is used only as a comparison curve.

Reproduce: `python -I _tools/artillery_range_check.py --shots <shots.csv> --calc <calculator.json>` (private inputs; flags `--only D` for the table comparison, `--only E` for the replicate scatter) and `python -I _tools/shell_sim.py` for the flat-ground table in section 2.

## 2. Flat-ground curve (independent of the log)

**Derived.** Range on level ground, muzzle speed 300 m/s, 1 ms step:

| Elevation (deg) | Standard (m) | Expensive (m) | No drag (m) |
|---:|---:|---:|---:|
| 5 | 494 | 1023 | 1595 |
| 10 | 648 | 1593 | 3141 |
| 20 | 781 | 2240 | 5903 |
| 30 | 815 | 2529 | 7953 |
| 34 | 810 | 2572 | 8515 |
| 40 | 787 | 2572 | 9044 |
| 45 | 754 | 2514 | no landing within 40 s |
| 60 | 590 | 2051 | no landing within 40 s |
| 80 | 231 | 820 | no landing within 40 s |

| Quantity | Standard | Expensive |
|---|---:|---:|
| Maximum flat range | 814.5 m | 2581.8 m |
| Elevation of the maximum | 29.94 deg (532 mil NATO, 523 mrad) | 36.96 deg (657 mil NATO, 645 mrad) |
| Flight time at the maximum | 13.0 s | 24.0 s |
| Impact speed at the maximum | 53 m/s | 113 m/s |
| Apex at the maximum | 221 m | 728 m |

The calculator's longest range is 2629 m at about 605 mil. The Expensive shell's derived maximum is 2582 m, 1.8 percent below the table. The Standard shell (`DragModel.Value` 80) cannot reach 815 m at any elevation, so the table (and the logged impacts, section 3) cannot belong to a Standard shell flown by these equations. The step length moves the Expensive maximum from 2582 m (1 ms) to 2574 m (33 ms).

### The 161 m/s figure

The reviewer's number is `sqrt(R * g) = sqrt(2629 * 9.8) = 160.5 m/s`: the speed at which a drag-free shell fired at 45 degrees would land at 2629 m. It is a back-calculation, not a muzzle speed. With the documented 300 m/s and no drag the same gun would throw 9184 m at 45 degrees (and the flight would exceed the 40 s lifetime). With the Expensive drag the shell leaves at 300 m/s, lands at 113 m/s after 24 s and reaches 2582 m: the "missing" energy is the drag, as the equations say. There is no contradiction once drag is included. Units were checked: the drag curve axis is m/s, mass is kg, diameter is cm, gravity is cm/s^2, and a mil is an angle, not a length (the unit-sensitive step, the diameter-to-area conversion, is the `10^-4` factor on the flight page, section 5). The one real tension is the other direction: the same equations make the **Standard** shell (`Value` 80) a short-range round, which matches no observation here (open item 3).

## 3. Residuals against the logged impacts (no fitting)

**A. Shell variant and mil convention** (target above gun, muzzle height 0, 4 ms; the row for each case uses the same N = 87 shots, fewer where the shell never lands):

| Hypothesis | N | Median (pred - meas) m | IQR m | Median abs m | Max abs m |
|---|---:|---:|---|---:|---:|
| Expensive, true milliradian | 87 | +7.7 | -29.4 to +73.9 | 58.9 | 492 |
| Expensive, NATO 6400 | 87 | +63.4 | +6.3 to +156.4 | 83.2 | 553 |
| Expensive, Warsaw 6000 | 87 | -154.3 | -208.2 to -21.5 | 171.5 | 613 |
| Standard, any convention | 85 to 86 | about -1200 | -1560 to -950 | about 1200 to 1240 | 1782 |

The Standard variant misses by more than a kilometre on every shot (two or three shots never land within 40 s). The Expensive variant with the milliradian reading is the only hypothesis with a median error near zero.

**B. Robustness of the best case** (Expensive, true milliradian):

| Variation | N | Median m | IQR m | Median abs m | Max abs m |
|---|---:|---:|---|---:|---:|
| Baseline (above) | 87 | +7.7 | -29.4 to +73.9 | 58.9 | 492 |
| Height difference sign reversed | 86 | -2.1 | -70.5 to +71.1 | 71.3 | 1027 |
| Muzzle 3 m above ground | 87 | +8.2 | -28.7 to +74.3 | 59.3 | 493 |
| Dial plus the logged vehicle pitch | 87 | +11.9 | -27.8 to +39.9 | 34.4 | 346 |
| Step 1 ms (Rate 1000) | 87 | +8.1 | -28.8 to +74.2 | 59.3 | 493 |
| Step 8 ms (Rate 125) | 87 | +7.2 | -30.1 to +73.4 | 58.5 | 492 |
| Step 16 ms (Rate 62) | 87 | +6.1 | -31.6 to +72.6 | 57.6 | 490 |
| Step 33 ms (Rate 30) | 87 | +3.0 | -34.8 to +70.7 | 58.0 | 488 |
| Low arc only | 25 | +4.3 | -65.9 to +84.7 | 79.1 | 150 |
| High arc only | 62 | +10.5 | -29.0 to +73.2 | 52.4 | 492 |
| Height difference logged | 69 | -10.1 | -40.5 to +42.9 | 41.5 | 420 |
| Height difference blank (as 0) | 18 | +72.6 | +65.9 to +82.5 | 72.6 | 492 |

The step length, the muzzle height and the arc do not matter. Adding the logged vehicle pitch to the dial narrows the middle half and halves the median absolute error, which is consistent with the dial being relative to a tilted hull, but whether the game adds the pitch is not established (**assumed**). The 18 shots with no height difference carry a systematic +66 to +83 m overshoot; their true height difference is unknown.

**C. Replicate scatter of the log.** Ten repeat shots at one plan/dial scatter by a median of 4.4 m (max 12.1 m) about their mean. The log is therefore far more repeatable than the model error (about 59 m median absolute), so the remaining residual is a model or convention difference, not shot-to-shot noise. Only one replicate group of three or more exists.

**D. One measured offset (the only free parameter).** The dial offset that minimises the median absolute residual, with a 100-sample bootstrap interval (grid of 10 mil). **This offset is measured from the log, not derived:**

| Convention | Best offset (mil) | Bootstrap 2.5 to 97.5 percent | Median abs at offset (m) | IQR at offset (m) |
|---|---:|---|---:|---|
| True milliradian | +10 | -10 to +20 | 52.9 | -56.7 to +41.6 |
| NATO 6400 | +30 | +10 to +50 | 53.6 | -50.3 to +61.5 |
| Warsaw 6000 | -50 | -50 to -40 | 47.0 | -51.4 to +44.9 |

A fitted offset removes the bias but leaves a median absolute error of about 50 m for every convention: the residual shape is not an offset.

## 4. Residuals against the calculator table

Elevation that the simulator (Expensive) needs to reach each table range, expressed in each convention, minus the table's dial value. This is the offset that would reconcile the table; it is a **measured difference**, not a derived constant.

| Convention | Arc | Points | Median offset (mil) | IQR (mil) | Min to max (mil) |
|---|---|---:|---:|---|---|
| True milliradian | high | 67 | +10 | +2 to +14 | -55 to +15 |
| True milliradian | low | 48 | +68 | +63 to +76 | +62 to +128 |
| NATO 6400 | high | 67 | +30 | +19 to +37 | -42 to +42 |
| NATO 6400 | low | 48 | +73 | +69 to +82 | +68 to +140 |
| Warsaw 6000 | high | 67 | -42 | -46 to -39 | -86 to -38 |
| Warsaw 6000 | low | 48 | +53 | +48 to +64 | +46 to +100 |

The needed offset is **not the same on both arcs** in any convention: the high arc is consistent (a few tens of mil, narrow IQR) and the low arc needs 40 to 60 mil more. No single constant reconciles the table. The peak of the table sits near 605 mil while the simulator's peak is at 645 mrad (657 mil NATO), a gap of 40 to 52 mil. The reviewer's "about 200 mil" is not supported: it would be the gap between a drag-free 45-degree peak (800 mil NATO) and the table's 605, but drag moves the peak down to about 37 degrees, which accounts for most of that gap by itself. The residual offset after drag is tens of mil, not hundreds, and is convention dependent.

The table's 20 mil row (1181 m) is the sharpest disagreement for a drag-limited shell: the simulator needs about 6.2 degrees there (110 mil NATO, 108 mrad) to throw the shell 1181 m, which is the +68 to +90 mil low-arc offset above. Either the low part of the table was measured at a different effective launch height or elevation reference, or the in-game dial differs from barrel elevation at low angles; the log has only 25 low-arc shots, all with median error within +4 m but scatter of +/-80 m, so it cannot separate these.

## 5. Verdict

1. **The derived model reproduces the logged impacts to within about 60 m (median absolute) without any fitted parameter**, but only for the Expensive-shell drag (`DragModel.Value` 2.5, 19 kg, 10.5 cm) and only if the dial is read as a true milliradian. That is 3 percent of range at 2 km. With the NATO reading the median overshoot is 63 m; with the Warsaw reading the model undershoots by 154 m.
2. **It does not reach the measurement precision.** The log repeats to a few metres; the model is off by tens of metres with a spread of -29 to +74 m and a worst case near 490 m. The model is a good first-order description, not an exact one. Bias is within the spread, so a constant offset is not required, and a fitted one (+10 mil) is within its own uncertainty of zero.
3. **The Standard 155 mm round is excluded** as the shell that was fired: the documented equations give it at most 815 m, against logged impacts beyond 2 km. Either the log is of the Expensive shell, or the Standard asset's `DragModel.Value` of 80 is not applied the way the page reads it. This stays open and is already item 10 on the flight page.
4. **The calculator's table is consistent with the same physics, not independent of it.** Its longest range (2629 m) is 1.8 percent above the Expensive maximum (2582 m); its high arc matches the simulator with an offset of +10 mil (milliradian) to +30 mil (NATO); its low arc needs 40 to 60 mil more. The "about 200 mil offset" is a misreading of the peak position (drag, not offset); the real offset is not constant across arcs.
5. **What this does not show.** The log's shell variant, dz sign and mil convention are assumptions (sections 1 and 3); the artillery mover's rotation step (`WDArtilleryProjectileMove`) is untraced; wind and gravity-override volumes are not modelled; muzzle height is not in the data.

## 6. Open items

1. Which mil convention the in-game dial and the calculator use (the log fits a milliradian best; NATO is +63 m, Warsaw -154 m). The game's data stores no mil value.
2. Whether the game adds hull pitch to the commanded elevation (adding the logged pitch halves the median error).
3. Whether the Standard 155 mm asset flies with `DragModel.Value` 80 (excluded here) or the artillery mover changes drag.
4. The calculator's low arc, which needs 40 to 60 mil more than its high arc under this model.
5. `Rate` (step) and the artillery-mover rotation step (flight page, items 3 and 8); neither moves the result here.
