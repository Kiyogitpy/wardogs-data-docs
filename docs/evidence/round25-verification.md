---
title: Round 25 independent verification
nav_exclude: true
---

# Round 25 independent verification (teammate J)

Verifier: `python _tools/verify_round25.py [falloff|locations|penetration]`. It prints PASS or FAIL per check and exits 1 on any FAIL. It reads only `data/Wardogs`, the three JSON files and the three evidence docs, and imports none of `damage_tables.py`, `weapon_damage_tables.py`, `weapon_damage_falloff.py`, `weapon_damage_locations.py` or `weapon_penetration.py`. The rule walk for track G follows the approach of `_tools/verify_weapon_damage.py` but is a separate copy. The ricochet and exit-speed tables of track H live in the offline round 8 config extraction (`E:/Reverse_Engineer/wardogs_analysis/round8_config_20261018/extracted/Wardogs/Config`), which is not part of `data/`; the script reads it when present and prints UNDETERMINED for those checks when it is absent.

The script currently exits 1 because four checks FAIL. Each FAIL is a claim in a doc that the data does not support (listed under "Discrepancies"); none is a data mismatch.

Verdict words: CONFIRMED (reproduced from raw data), REFUTED (raw data disagrees with the claim as written), UNDETERMINED (rests on native code or game behavior that I did not re-read or observe).

## Summary of maximum differences

| Track | Compared | Max difference |
|---|---|---|
| F curve multiplier | 33 weapons, all ammo rows, 14 distances each, own Hermite and linear evaluation from raw keys and tangents | 4.8e-6 absolute (JSON rounds to 5 decimals) |
| F curve keys | key times, values, interp modes, arrive and leave tangents of 32 stored curves against raw | 0 mismatches |
| F speed scale bite distance | 35 FMJ, Buckshot and Slug rows, own RK4 integration at 0.5 ms | 1 m (10 rows differ by exactly 1 m, 25 agree) |
| F speed at the 14 distances | same rows | 0.16 percent relative (M500 buckshot at 1000 m: 3794 against 3788 cm/s) |
| G damage cells | 6650 cells (33 weapons, all ammo rows, 12 locations, every covering class) | 1.1e-13 |
| G coverage table | 14 items against the JSON `armor_items` and `armor_effect` | 0 mismatches |
| H capacity coefficient K | 190 weapon x ammo rows | 3.0e-6 relative (JSON rounds to six digits) |
| H reference block | 1050 surface factors and next-impact fractions | 5.0e-7 |
| H surface tables | 63 entries x (exit speed, ricochet, restitution, name) | 0 mismatches |

## Track F: damage over distance

### Curves (all 33 weapons)

Weapons with a stored curve: 32. Judge has none. Applied (flag true): 30. M500 and MP43 store a three-key curve without the flag. All 32 stored curves match the JSON keys, interp modes and tangents. I evaluated Unreal's `FRichCurve::Eval` myself: constant extrapolation outside the keys, the segment taking the interp mode of its first key, linear as a lerp, cubic as the Hermite form with tangents `LeaveTangent * dt` of the first key and `ArriveTangent * dt` of the second. Cubic keys exist in exactly WEPN_028, MP9, SMG_03 and WEPN_031.

| Weapon (group) | Curve end (m) | Max abs diff vs JSON over 14 distances |
|---|---:|---:|
| A91, TAR21, WEPN_033, KH2002 (all linear) | 1200 | 4.4e-6 |
| M4, AK74M, RFB, WEPN_034 (all linear) | 1200 | 4.3e-6 |
| Glock17, WEPN_032, WEPN_026 (linear) | 1200 | 4.8e-6 |
| Vector (six linear keys) | 1200 | 4.8e-6 |
| WEPN_028 (cubic) | 1200 | 4.6e-6 |
| MP9 (cubic) | 1200 | 3.9e-6 |
| SMG_03, WEPN_031 (cubic) | 1200 | 4.8e-6 |
| Judge (no curve) | none | 0 (multiplier 1 everywhere) |
| M500, MP43 (curve stored, flag absent) | 1200 | 0 (curve not applied, multiplier 1) |
| LMG_02, WEPN_036, SV98 (1500 m LMG and sniper curves) | 1500 | 1e-16 |
| MK22 | 1600 | 0 |
| SR_04 | 2500 | 0 |

The script checks all 33 weapons, not only these. Verdicts for the structural claims: last key at 1200 m for 25 weapons that apply a curve (27 store one; M500 and MP43 account for the difference) CONFIRMED; LMG_02, WEPN_036 and SV98 end at 1500 m, MK22 at 1600, SR_04 at 2500 CONFIRMED; 30 of 33 weapons apply a curve CONFIRMED; Vector has six keys, all linear CONFIRMED; Judge has no curve CONFIRMED; M500 and MP43 store a curve with the flag absent CONFIRMED; key modes of the four SMGs (MP9 linear at 0 m then cubic at 100, 200 and 1200 m; the other three linear at 0, cubic at 200 and 300, linear at 1200) CONFIRMED.

Whether the engine applies the stored M500 and MP43 curve when the flag is absent is UNDETERMINED (the flag's native default was not read by anyone).

### Linear approximation versus exact curve

| Weapon | 400 m exact | 400 m linear | Overstatement | 600 m | 800 m exact | 800 m linear | Overstatement at 800 m | 1000 m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| WEPN_028 | 0.4424 | 0.5444 | 23.1% | 85.7% | 0.1329 | 0.3222 | 142.4% | 107.7% |
| MP9 | 0.3327 | 0.5000 | 50.3% | 120.0% | 0.1145 | 0.3000 | 161.9% | 103.7% |
| SMG_03 | 0.4620 | 0.5444 | 17.8% | 62.6% | 0.1575 | 0.3222 | 104.6% | 91.5% |
| WEPN_031 | 0.4620 | 0.5444 | 17.8% | 62.6% | 0.1575 | 0.3222 | 104.6% | 91.5% |

The overstatement is linear divided by exact minus one. Scanning 400 to 1000 m at 1 m steps, the smallest value is 17.8 percent at 400 m for SMG_03 and WEPN_031, 23.1 percent for WEPN_028, 50.3 percent for MP9.

- Claim "overstates the four SMGs by 18 percent or more between 400 m and 1000 m": REFUTED by 0.2 points. The minimum is 17.8 percent, not 18. The doc itself names SMG_03 at 400 m as the smallest case. The claim holds from 401 m for SMG_03; every other SMG and distance is above 18 percent.
- Claim "more than 100 percent at 800 m for all four": CONFIRMED. The minimum is 104.6 percent (SMG_03 and WEPN_031).
- Quoted multipliers at 400 m and 800 m (0.442, 0.333, 0.462 exact; 0.544, 0.500, 0.544 linear; 0.133, 0.115, 0.158 and 0.322, 0.300, 0.322 at 800 m): CONFIRMED to three decimals.
- Largest linear versus exact multiplier gap: MP9 0.218 at 608.8 m, WEPN_028 0.207 at 673 m, SMG_03 and WEPN_031 0.175 at 691.6 m: CONFIRMED.
- MP9 spline falls below its final value 0.1: CONFIRMED. It is 0.0982 at 1000 m and reaches a minimum of 0.0981 at 1022.2 m.

### Drag model and speed scale

I integrated the documented model (`a = -100 * 0.5 * 1.2 * Cd * (pi/4) * (D/100)^2 * (v/100)^2 / m`, `Cd = DragModel.Value * Curve[row](v in m/s)`, drag rows linear with constant extrapolation, `m` floored at 0.001) with RK4 at 0.5 ms along the line of sight, no gravity, and read the continuous crossing of the reference speed. The reference is the weapon `TypicalSpeed` when `bOverrideTypicalSpeed` is true and the value is above 0, else the projectile asset `TypicalSpeed`. The JSON reference speed and reference source agree with this rule for every row, and the muzzle speed is above the reference for every row.

| Weapon | Muzzle cm/s | Reference cm/s | JSON bite (m) | My crossing (m) | My first whole metre | Difference |
|---|---:|---:|---:|---:|---:|---:|
| M4 | 91000 | 40400 (projectile) | 513 | 512.80 | 513 | 0 |
| Glock17 | 37500 | 30000 (override) | 73 | 72.60 | 73 | 0 |
| SV98 | 83000 | 41500 (override) | 905 | 905.18 | 906 | +1 |
| MP9 | 40000 | 28000 (override) | 122 | 121.52 | 122 | 0 |
| A91 | 71500 | 40400 (projectile) | 353 | 352.63 | 353 | 0 |
| SMG_03 | 38000 | 20200 (override) | 321 | 320.63 | 321 | 0 |
| M500 buckshot | 48000 | 29200 (projectile) | 92 | 91.68 | 92 | 0 |
| LMG_02 | 82500 | 33600 (override) | 1141 | 1141.31 | 1142 | +1 |
| SR_04 | 90000 | 31300 (override) | 2016 | 2015.69 | 2016 | 0 |

Verdict: bite distances CONFIRMED to within 1 m for all 35 rows. The 1 m differences are step discretization: the JSON integrates with 1 ms trapezoid steps, I use RK4, and the crossing sits within 0.4 m of the JSON value in every case. The model itself is the one in the docs, so this confirms the integration and the wiring of data (projectile dimensions, drag row, reference rule), not that the game matches the model. The 12 s flight cap figures (Glock17 1285 m, WEPN_026 1318 m, M500 buckshot 1065 m) are CONFIRMED to the metre. The 33-row speed table in the evidence doc matches the JSON and the raw stats for muzzle speed, reference, source, bite distance and curve end (33 of 33 rows). The doc's A91 values 0.78, 0.64 and 0.51 at 500, 800 and 1200 m are the speed scale factor alone (damage ratios 0.645, 0.355, 0.103 include the curve); the sentence says "of its curve value", which is correct.

Of the 33 weapons, 23 set `bOverrideTypicalSpeed`; across all 82 weapon stats assets in the export, 24 do. The doc's "24 overrides that Damage Pipeline section 7.8 counts" is the global count, consistent.

### Step size

The doc says the game steps by `floor(1000 / Rate)` ms with Rate unread, and bounds the effect with a 16 ms comparison (at most 2.2 percent). The track H JSON `config.simulation_frame_rate` is 30, read from the raw `ProjectileSystemSettings` (`SimulationFrameRate=30`, confirmed). If that is the Rate in the formula, the step is 33 ms. With a plain explicit Euler step (not the game's scheme, which nobody has read) the bite distance moves by 2.5 percent at 16 ms (MP9, 122 m to 119 m) and by 9.8 percent at 33 ms (M500 buckshot, 92 m to 83 m). So the doc's 2.2 percent bound does not cover the step the other track's data implies. Whether SimulationFrameRate is the Rate in question is UNDETERMINED. The F JSON `assumptions` still says Rate is unread.

## Track G: armor coverage by hit location

### Coverage table rebuilt from raw

There are 14 `WDInventoryFragment_Armor` fragments in `data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data` (the 10 armored items and four Ghillie variants), and no other armor fragment anywhere in `data/`. The rebuilt table matches the JSON `armor_items` and `armor_effect` (context tag, covered locations as a set, R, FMJ multiplier).

| Item | Tag | R | Head | Neck | Torso.Upper | Torso.Middle | Torso.Lower | Pelvis | Arm.Upper |
|---|---|---:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ID_LightArmor | Armor.Light | 30 | | | x | x | x | | |
| ID_MediumArmor | Armor.Medium | 40 | | | x | x | x | | |
| ID_HeavyArmor | Armor.Heavy | 50 | | | x | x | x | | |
| ID_SuperHeavyArmor | Armor.SuperHeavy | 60 | | | x | x | x | x | x |
| ID_LightHelmet | Helmet.Light | 30 | x | | | | | | |
| ID_MediumHelmet | Helmet.Medium | 40 | x | | | | | | |
| ID_PilotHelmet | Helmet.Pilot | 30 | x | | | | | | |
| ID_HeavyHelmet | Helmet.Heavy | 50 | x | x | | | | | |
| ID_SuperHeavyHelmet | Helmet.SuperHeavy | 60 | x | x | | | | | |
| ID_TankHelmet | Helmet.Tank | 55 | x | x | | | | | |

Arm.Lower, Arm.Hand, Leg.Thigh, Leg.Calf and Leg.Foot are covered by no item. Every armored item has four durability stages with one R each. `assets/data/infantry-hitboxes.json` `covered_by` matches the rebuilt coverage for all 12 locations. CONFIRMED.

Verdicts: no location is covered by two items of different kinds (a vest and a helmet): CONFIRMED. Several items of the same kind do share a location (for example six helmets at Head); that is one slot, not a conflict, and slot exclusivity is UNDETERMINED (the doc says so). Ghillie items have no stages and no coverage: CONFIRMED.

### Damage cells

Full sweep: 6650 cells, maximum absolute difference 1.1e-13 against `damage_raw`; the class set per location equals {None} plus my covering classes in every case; no armored cell exceeds its unarmored cell; rounded values agree. The round 24 Torso.Upper and Head columns and the four unarmored location columns in the locations JSON equal `weapon-damage.json` for all rows. All 20 numbers quoted in the armor doc (M4 FMJ and AP, SR_04 HP at the Neck, Pelvis, Arm.Upper, Torso.Middle) reproduce. The claim that the largest absolute drop is the SR_04 hollow point at the Neck is CONFIRMED (479.15, tied with HollowPoint.Tracer, which has the same values).

Named sample (35 cells; weapon, ammo, location, class: my value / `damage_raw`):

| Cell | Mine | JSON |
|---|---:|---:|
| M4 FMJ Neck Heavy | 24.6750 | 24.6750 |
| M4 FMJ Neck Tank | 22.2075 | 22.2075 |
| M4 FMJ Neck SuperHeavy | 19.7400 | 19.7400 |
| M4 FMJ Torso.Middle Heavy | 13.5800 | 13.5800 |
| M4 FMJ Torso.Middle Light | 19.0120 | 19.0120 |
| M4 FMJ Torso.Lower Medium | 15.4812 | 15.4812 |
| M4 FMJ Torso.Lower SuperHeavy | 10.3208 | 10.3208 |
| M4 FMJ Pelvis SuperHeavy | 10.0800 | 10.0800 |
| M4 FMJ Arm.Upper SuperHeavy | 6.0480 | 6.0480 |
| M4 AP Neck Heavy | 27.6360 | 27.6360 |
| M4 AP Neck SuperHeavy | 25.2672 | 25.2672 |
| M4 HP Torso.Middle SuperHeavy | 1.4666 | 1.4666 |
| SR_04 HP Neck SuperHeavy | 7.0005 | 7.0005 |
| SR_04 HP Neck Tank | 15.3137 | 15.3137 |
| SR_04 HP Neck Heavy | 19.6890 | 19.6890 |
| SR_04 AP Pelvis SuperHeavy | 39.3112 | 39.3112 |
| Glock17 FMJ Head Pilot | 32.3400 | 32.3400 |
| Glock17 FMJ Head Tank | 20.7900 | 20.7900 |
| Glock17 AP Torso.Lower Heavy | 11.4114 | 11.4114 |
| WEPN_026 HP Head Pilot | 16.2162 | 16.2162 |
| WEPN_026 FMJ Head Tank | 36.8550 | 36.8550 |
| AK74M Tracer Arm.Upper SuperHeavy | 5.6160 | 5.6160 |
| SVDM AP Torso.Middle Heavy | 24.9216 | 24.9216 |
| M500 Buckshot Neck Tank | 8.8594 | 8.8594 |
| M500 Slug Pelvis SuperHeavy | 23.8140 | 23.8140 |
| WEPN_035 FMJ Torso.Lower Light | 35.9980 | 35.9980 |
| MK22 HP Neck Heavy | 12.9601 | 12.9601 |
| Judge FMJ Arm.Upper SuperHeavy | 14.0400 | 14.0400 |
| SKS HP.Tracer Neck SuperHeavy | 2.2491 | 2.2491 |
| M4 FMJ Arm.Hand, Leg.Calf, Leg.Foot, Arm.Lower (unarmored) | 7.56, 12.60, 7.56, 12.60 | same |
| WEPN_017 AP Leg.Calf (unarmored) | 26.4000 | 26.4000 |
| Glock17 FMJ Arm.Hand (unarmored) | 8.5800 | 8.5800 |

All 35 CONFIRMED, including Pilot and Tank helmets and the SuperHeavy vest at Pelvis, Arm.Upper, Neck and Torso.Middle and Lower. The rule engine and its inputs are the rule table logic the doc names; I did not re-derive the rule table itself beyond reusing the approach of the round 24 verifier.

### Ghillie

The claim "Ghillie items have no effect in the data" needs two qualifications.

1. In the infantry damage table (`DT_GlobalDamage_InfantryData`) no entry mentions Ghillie, and passing the Ghillie tag as the covering piece returns the unarmored value (27.2580 against 27.2580). CONFIRMED for the player damage rule the JSON models.
2. `DT_GlobalDamage_ArmorData` has two entries that require a Ghillie target tag: `Meta.Damage.Armor` entry 7 (Percentage_Ongoing -10000) and `Meta.Damage.Helmet` entry 6 (-1000), plus Ghillie-specific rows (`Meta.Damage.Armor.Ghillie`, `Meta.Damage.Helmet.Ghillie`) with -100 percent entries against explosive, cannon, impact and melee sources. By table position these are the armor item's own damage channel, not the wearer's, but the evidence doc lists "Whether Ghillie context tags matter for any rule entry" as not covered, and the answer is that they do appear in one rule table. The Ghillie fragments also carry `AppliedEffects` (`GE_Player_Ghilli_Armor`, `GE_Player_Ghilli_Helmet`, `GE_Player_GhilliEffects`); those gameplay effect assets are not in `data/` (0 files match `GE_Player_Ghilli*`), so any effect they have on damage taken is UNDETERMINED. The doc's parenthetical "they have R = 0 in the item data" is also inexact: the Ghillie fragments have no R field at all.

## Track H: ricochet and penetration

### (a) Surface table

Raw: `ProjectileSystemSettings` on line 303 of the extracted `DefaultGame.ini`, names from `DefaultEngine.ini` `[PhysicalSurfaces]`. The JSON `config.surfaces` equals it for all 63 entries (exit speed, ricochet probability, restitution including the empty entry at SurfaceType19, names). Types 39 to 62 have exit speed 0, ricochet 0.5, restitution 0.4 to 0.6: CONFIRMED.

| Claim | Raw result | Verdict |
|---|---|---|
| 63 entries in the surface table | 63 ricochet, 63 exit-speed, 62 restitution | CONFIRMED |
| Ricochet probability nonzero for 57 of 63 | 57 | CONFIRMED |
| Ricochet zero only for SurfaceType3 and 17 | zero at 3 Body, 13 Fur, 17 Head, 19 Lava, 20 Leaf, 34 Water (6 types) | REFUTED |
| Exit-speed modifier nonzero for 36 of 63 | 36 | CONFIRMED |
| Those 36 are "every named type except Body and Head" | named types are 0 to 38 (39 of them); zero exit speed at 0 Default, 3 Body, 17 Head, so 36 of the 39 | REFUTED as worded (Default is also zero) |
| Largest exit-speed modifier 1.0 at BulletProofGlass (38) | 1.0 | CONFIRMED |

The two REFUTED rows sit in the doc's opening list of corrections, and the first contradicts the same sentence's "57 of the 63" (57 nonzero means 6 zeros). The Damage Pipeline wording "Packed SurfaceType3/17 exit-speed modifiers and ricochet chances are zero" is correct as written.

### (b) Ammo modifiers (five assets, raw)

| Asset | PenetrationEffectiveness | ExitSpeed | EffectiveRange | TracerChance | Verdict |
|---|---:|---:|---:|---:|---|
| AmmoModifier_ArmorPiercing | 1.8 | 0.0 | 1.2 | none | CONFIRMED |
| AmmoModifier_ArmorPiercing_Tracer | 1.76 | 0.0 | 1.2 | 1.0 | CONFIRMED |
| AmmoModifier_HollowPoint | 0.1 | 0.15 | 0.8 | none | CONFIRMED |
| AmmoModifier_HollowPoint_Tracer | 0.1 | 0.15 | 0.8 | 1.0 | CONFIRMED |
| AmmoModifier_Tracer | 1.0 | 0.075 | 1.0 | 1.0 | CONFIRMED |

The JSON `ammo_modifiers` equals these. Note that AP Tracer stores 1.76, not 1.8 times 1.0; the doc table shows 1.76 and so is right, but a reader multiplying the two rows would expect 1.8.

### (c) A91 FMJ capacity coefficient

`K = v * 0.01 * m * E / (0.099999994 * d^2)` with v 71500, m 0.0041, E 1, d 0.57 gives 90.2278: CONFIRMED (stated 90.2278). AP gives 162.4100 (stated 162.41), AP Tracer 158.8009 (stated 158.801). K and the exit-speed multiplier recomputed for all 190 weapon x ammo rows differ from the JSON by at most 3.0e-6 relative. The formula, constants and the pass condition themselves are native claims (below).

Doc worked examples (X = 45 and 70, Concrete): FMJ speed after 25447 cm/s, AP 41351, next-impact fractions 0.630 and 1.000: CONFIRMED. Struggling FMJ round at X = 70: I get 11381 cm/s and fraction 0.282 where the doc has 11366 and 0.281 (the doc rounds f to 0.776 before multiplying; 0.13 percent). Ricochet chance 0.104 CONFIRMED (0.1045). The `reference` block (1050 values for A91, AK74M, SV98, SR_04, Glock17) reproduces to 5e-7.

### (d) Angle table and minimum ricochet angle

The angle table is nine 10 degree bins with 0.08, 0.18, 0.30, 0.42, 0.55, 0.67, 0.78, 0.87, 0.92 and equals the JSON: CONFIRMED. `PenetrationEffectivenessRicochetProbabilities` is (2, 1): CONFIRMED. `MaxConsecutiveFullRefundedSubsteps` 10, `MaxPelletCount` 16, `SimulationFrameRate` 30, `MaxRicochetAngleVariance` 40, deflection ranges and `PlanarSurfaceThicknessScale` 10: CONFIRMED.

`MinImpactAngleForRicochet` is set on projectile assets as follows. 91 on the four 155 mm assets (CONFIRMED) and also on 120x570, 120x800, 122, 122 HAVOC, 125x570, 20x102 and others; 100 on 70 mm; 85 on the TV guided missile and the 30 mm round; 30 on the combat arrow. So the doc's "91 on the 155 mm assets (never)" is correct for those assets but understates the spread, and "never" does not apply to the 85 and 30 values. The 10 degree default for assets that omit the field comes from the native constructor and is not in data: UNDETERMINED here.

### Other data claims in the penetration doc

| Claim | Result |
|---|---|
| 156 data files carry `PhysicalMaterialOverride`; 9,076 null; 125 named (Metal 90, Concrete 24, Plaster 9, Brick 1, Glass 1) | CONFIRMED exactly |
| 0 of 146 infantry damage entries key on `Kinetic.Impact.Ricochet` or `.Penetration` | CONFIRMED |
| No `WDPhysicalMaterial` or `PM_*` assets in the export | CONFIRMED (no `PM_*.json` files) |
| Arrow exit speed 0.55 so `p + s` reaches 1.55 and the factor floor is 0.225; arrow E 0.5 | CONFIRMED |
| `bForcePenetrateThinSurfaces` on 122, HAVOC, 40, 72, 84, 93 mm and arrows | CONFIRMED (same six assets plus arrows) |
| `bShouldPenetrate` false on 70, 72, 84, 93, 120, 122, 125, 155 mm | CONFIRMED, but incomplete: also false on 40 mm and the TV guided missile |
| Base p and E per caliber (5.56 0.18, .308 0.13, 9 mm 0.35, .45 ACP 0.32, .50 Cal 0.05 and E 3.5, 20x102 E 1.8) | CONFIRMED for the values I read; the doc's E list omits the 122 mm and 30 mm assets, which also set 2.0 |
| JSON `projectiles` (32 assets) diameter, mass, flags | CONFIRMED against raw |

## Discrepancies, ranked by how much they would mislead

1. Penetration doc, opening correction: "ricochet chances are zero is true only for SurfaceType3 and 17" while 57 of 63 are nonzero. Six types are zero (Body, Fur, Head, Lava, Leaf, Water). The sentence also says the 36 nonzero exit-speed types are every named type but Body and Head, but Default is zero too. A reader will conclude the wrong set of surfaces never ricochets. This is the headline correction of the doc, and its own count contradicts it.
2. Falloff step size. `weapon-damage-falloff.json` and its doc say the game's step length is unread and bound the error at 2.2 percent using 16 ms. The penetration JSON carries `SimulationFrameRate` 30 from the raw config, which would give 33 ms if it is the Rate in `floor(1000 / Rate)`. With a plain Euler step the speed scale bite distance moves up to 9.8 percent at 33 ms. Every speed-scaled cell in the falloff JSON inherits this uncertainty, and the two docs should be reconciled.
3. Locations: "Ghillie items have no effect at any location" is stated as an assumption in the JSON `meta` and the doc lists the question as not covered. The data does hold Ghillie-specific rows in `DT_GlobalDamage_ArmorData` and gameplay effects on the fragments that are not in the export. The player damage numbers are right for the data given, but the sentence is stronger than the evidence, and "R = 0 in the item data" is inexact (no R field).
4. Falloff doc: "overstates by 18 percent or more between 400 m and 1000 m". The true minimum is 17.8 percent (SMG_03 and WEPN_031 at 400 m). Small, and the doc points at the case itself.
5. Penetration doc: the minimum ricochet angle "91 on the 155 mm assets (never)" suggests an exceptional setting for heavy shells. The raw data sets it on at least 18 projectile assets, with values 91, 100, 85 and (arrow) 30, so some of them do ricochet. Also `bShouldPenetrate` false is listed without 40 mm and the TV missile.
6. Locations JSON `meta.assumptions` still carries a sentence about `rpm` copied from the round 24 JSON, but this file has no rpm field. Stale text, no data effect.
7. Penetration doc: struggling-round example 11366 cm/s and 0.281 are 0.13 percent off the unrounded 11381 and 0.282. No effect on any conclusion.
8. Penetration JSON `meta.surface_note` says "the names above", but no names appear above it in `meta`; they are in `config.surfaces`.

Not discrepancies, noted so nobody spends time on them: bite distances differ from my RK4 by 1 m in 10 of 35 rows (integration step); 23 of the 33 weapons set the speed override against the 24 global overrides the doc quotes; the AP Tracer value 1.76 is the stored number.

## What I could not verify

Verified from data: everything in the tables above, i.e. curve keys, tangents and interp modes; reference-speed sources; drag inputs (diameter, mass, drag value and row) and the drag curve rows; coverage, R and tags of all 14 armor items; per-cell damage under the documented rule engine; the 63-entry surface tables, the angle table and projectile-system constants from the config extraction; the five ammo modifier assets; projectile flags and dimensions; the physical-material override counts; the K arithmetic.

Rests on native code or game behavior that I did not re-read or observe:

- Unreal's `FRichCurve::Eval` semantics (I implemented the standard engine behavior; I did not read it in this binary). Whether a missing extrapolation mode means constant.
- The drag formula itself, the `rho = 1.2` and level-in-m/s details (Projectile Flight section 5, `0x6F2E240`), and the claim that the game integrates this way; my integration confirms the arithmetic and the data wiring only.
- The speed scale rule at `0x6C255B0` and the order and form of the speed and distance scales at `0x6B725B0`; that point-blank damage scales linearly through the rule chain (both `damage_tables.py` and the falloff doc assume it).
- The first-covering-piece hook (`0x6F01BB0`) behind the claim that a non-covering piece has no effect.
- The penetration pass condition, the capacity formula, constants `0.01` and `0.099999994`, the exit-speed formula, the ricochet decision at `0x6F36600` (the doc itself marks it New and unreviewed), the native default of `MinImpactAngleForRicochet` 10, and `bShouldPenetrate` defaults.
- Whether `SimulationFrameRate` is the Rate in the step formula, the actual step scheme, gravity sensitivity (I did not rerun the 22 percent figure), and the maximum projectile lifetime.
- The `GE_Player_Ghilli*` gameplay effects, slot exclusivity for vests and helmets, the mapping of world props to surface types and densities, and anything observed in a live game.
- The ricochet and exit-speed tables are not in `data/`; they were verified from the offline extraction at the path above, which a plain clone cannot repeat.

Corrections applied by the lead after this verification: the four REFUTED claims (17.8 percent instead of 18, six zero-ricochet surface types, Default as a zero exit-speed type, the spread of minimum ricochet angles) were rewritten in the falloff and ricochet evidence docs, the damage page and the Damage Pipeline note, and the step-length uncertainty and the Ghillie assumption were added to the page and the evidence docs. `_tools/verify_round25.py` still tests the original wording of those four claims, so it keeps reporting them as FAIL by design.
