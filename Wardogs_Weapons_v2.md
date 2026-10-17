---
title: "Weapons"
parent: "Content"
---

# Wardogs — Weapons Reference
*Extracted from cooked game data (JSON export, [`Wardogs/Content/Weapons/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Weapons), 92 source files). Parsed with a Python script; 15 Input files contain several `--- export:` blocks each and were split on those headers. Numbers are the raw exported values.*

> **Scope note:** this folder holds only **8 weapon stat assets** (`WDWeaponStatsData`). The main rifle, SMG, LMG, shotgun and pistol stat tables are not in this folder. Their aim-sway curves are here; the stat tables themselves live under [`Plugins/GameFeatures/Weapons`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Weapons), all 45 listed in [Infantry Weapon Stats](Wardogs_InfantryWeapons_Stats_v1.html).

---

## Season 02 update (2026-10-15)

- **Removed:** the Mosin sniper package under [`Plugins/GameFeatures/Weapons/Sniper/Mosin`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin) (11 files, including `DA_Mosin_Stats`). Nothing in the tables below changes because the Mosin was never in this folder.
- **Added:** 154 files under [`Plugins/GameFeatures/Weapons`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Weapons), mostly attachments: foregrips FGRP_019 and FGRP_020, magazines MAGZ_051 and MAGZ_067 to MAGZ_071, and muzzles MUZL_064 to MUZL_067. Six new weapon stat assets: [`DA_WEPN_017_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DA_WEPN_017_Stats.json), [`DA_WEPN_031_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/DA_WEPN_031_Stats.json), [`DA_WEPN_034_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/DA_WEPN_034_Stats.json), [`DA_WEPN_036_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/DA_WEPN_036_Stats.json), [`DA_WEPN_037_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DA_WEPN_037_Stats.json) and [`DA_MWSY_001_Heavy_MountedMachineGun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_001/Content/Weapons/DA_MWSY_001_Heavy_MountedMachineGun_Stats.json).
- **SKS recoil pattern ([`DA_SKS_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/DMR/SKS/Data/DA_SKS_Stats.json)):** all 20 vertical (Y) values are 2.5x the old values (first point 0.95 → 2.375, last point 1.05 → 2.625). Horizontal (X) values now range from −2.399 to +0.613, where they previously ranged from −0.055 to +0.136. This fits the patch note "new recoil pass across all DMRs".
- **SKS fields:** `ViewKickMagnitudeMultiplier` 1.1 is gone, and `SuppressionMultiplier` 1.1 is new. This fits the suppression rebuild in the patch notes.
- **SKS and Judge stabilisation:** the CooldownRate and ExitGracePeriod entries are now unnamed fields. Values are unchanged (SKS 9.0, Judge 4.0).
- **M2 Browning ([`DA_M2Browning_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Stationary/M2Browning/Data/DA_M2Browning_Stats.json)):** `SuppressionMultiplier` 0.8 is new.
- **Vendor prices (weapons):** AK74M 1600 → 800, Vector 2600 → 5600, MMGL 6000 → 7500, LMG_02 4500 → 4100, RPG7 2000 → 1800, TAR21 600 → 1200.
- **Vendor prices (attachments):** FGRP_007 1150 → 840, FGRP_014 1100 → 950, MUZL_013 1000 → 820, MUZL_012 400 → 1200. Attachment prices are not in this doc's tables.
- **SR_04 ([`ID_SR_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/SR_04/Content/Data/ID_SR_04.json)):** `TimeAfterFireToRechamber` 0.24 → 0.2.
- The folder still holds 92 files and 8 stat assets. No files were added or removed here.

---

## 1. Weapon Stat Assets (`WDWeaponStatsData`)

| Asset | WeaponId tag | Caliber | RPM | Fire modes | Init. bullet speed | Effective range | Max zeroing | Melee dmg |
|---|---|---|---|---|---|---|---|---|
| [`DA_SKS_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/DMR/SKS/Data/DA_SKS_Stats.json) | `Id.Item.SKS` | `Item.Caliber.762mm` | 420 | SemiAutomatic | 73,500 | 400 | 1,000 | 35 |
| [`DA_Judge_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Pistol/Judge/Data/DA_Judge_Stats.json) | `Id.Item.Judge` | `Item.Caliber.45Colt` | 200 | SemiAutomatic | 33,500 | 50 | 25 (min 25, step 25) | 20 |
| [`DA_AT4_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/AT4/Data/DA_AT4_Stats.json) | `Id.Item.AT4` | `Item.Caliber.84mm` | 100 | SemiAutomatic | 29,000 | 300 | none | none |
| [`DA_ArtilleryBarrelTest_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/ArtilleryBarrelTest/Data/DA_ArtilleryBarrelTest_Stats.json) | `Id.Item.ArtilleryBarrelTest` | `Item.Caliber.155mm` | 150 | SemiAutomatic (RoundsPerBurst 1) | 46,400 | 10,000 | 1,000 | 0 |
| [`DA_TankBarrelTest_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/TankBarrelTest/Data/DA_TankBarrelTest_Stats.json) | `Id.Item.LeapordBarrel` | `Item.Caliber.120x570mm` | 100 | SemiAutomatic | 55,000 | 3,500 | 1,000 | none |
| [`DA_M2Browning_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Stationary/M2Browning/Data/DA_M2Browning_Stats.json) | `Id.Item.BrowningMG` | `Item.Caliber.762mm` | 500 | Automatic | 71,500 | none | 1,000 | none |
| [`DA_Fists_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Fists/Data/DA_Fists_Stats.json) | `Id.Item.Fists` | none | 300 | SemiAutomatic | none | none | none | none |
| [`DA_BuildTool_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/BuildTool/Data/DA_BuildTool_Stats.json) | `ID.Item.BuildTool` | none | none | none | none | none | none | none |

Notes:
- [`DA_BuildTool_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/BuildTool/Data/DA_BuildTool_Stats.json) contains only `WeaponId`. Its tag uses `ID.Item.` where every other asset uses `Id.Item.`.
- [`DA_TankBarrelTest_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/TankBarrelTest/Data/DA_TankBarrelTest_Stats.json) uses the tag `Id.Item.LeapordBarrel` (misspelling of "Leopard" is in the source).
- Units are not stated in the export. Inferred, not confirmed: `InitialBulletSpeed` is in Unreal cm/s (SKS 73,500 cm/s = 735 m/s; AT4 29,000 = 290 m/s), and `EffectiveRange` is in metres (SKS 400 m, Artillery 10 km).

### 1a. Per-weapon details beyond the table

**DA_SKS_Stats** (the most fully specified asset)

| Field | Value |
|---|---|
| WeaponAccuracy | 0.73, `AccuracyType = MinutesOfAngle` |
| FocusEnergyReductionPerShot | 50.0 |
| RecoilReductionWhenFocussing | 30.0 |
| ViewKickCurve | 3 keys: 0→0, 0.15→1, 0.4→0.75 |
| SuppressionMultiplier | 1.1 |
| RecoveryKickCurve | 1 key (0→0) |
| FOVShiftingType / Curve | `Curve`: 0→0, 1.5→−0.5, 8.43→−1, 13.43→−1, 30.26→−1.5 |
| RecoilPattern | 20 points |
| RecoilPatternYawMinMax | −22.5 … +22.5 |
| RecoilPatternPitchMax | 45.0 |
| RandomDeviationDegree | 5.5 |
| RecoilPatternResetTime | 0.95 |
| PostPatternRandomYawRecoil (X,Y) | −0.28, 0.38 |
| PostPatternRandomPitchRecoil (X,Y) | 0.55, 0.85 |
| MaxZeroingRange | 1,000 |
| MeleeHitBoxSize | 55 × 35 × 25 |
| Distance damage falloff | `bUseDistanceDamageFalloffCurve = True`; curve 0→1, 40,000→1, 120,000→0.2 |
| AdsCameraCurve | [`CF_DMR_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_DMR_ADS_Curve.json) |
| AimSway | Persistent=False, CrouchOffsetMultiplier 0.55, ProneOffsetMultiplier 0.35, TotalPatternDuration 6.0, NoFocusEnergySpeedMultiplier 2.5, PlayerCameraOffsetMultiplier 0.75 |
| AimSway stabilisation | AdsStabilizeTime 2.0, two unnamed fields (both 9.0), CooldownRateMovingMultiplier 2.0, MovementProgressPenalty 0.75 |
| Animation sway | ADSPitch/Yaw multiplier curves both [`CRV_WeaponAnimSwayMultiplier_DMR_Harsh`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/AimSway/DMR/CRV_WeaponAnimSwayMultiplier_DMR_Harsh.json) |

The distance falloff times are in cm: the native projectile path evaluates the curve with the shot-origin-to-hit distance in engine units ([DamagePipeline §7.6](Wardogs_DamagePipeline_v2.md#76-the-bullet-event)). 40,000 cm = 400 m, matching `EffectiveRange = 400`.

**DA_Judge_Stats** (pistol)

| Field | Value |
|---|---|
| WeaponAccuracy | 3.49 (no AccuracyType set, so the default applies) |
| FocusEnergyReductionPerShot | 40.0 |
| RecoilReductionWhenFocussing | 10.0 |
| Zeroing | Min 25, Max 25, Step 25 |
| ViewKickCurve | 2 keys: 0→0, 0.15→1 |
| FOVShiftingCurve | 0→0, 1→−1.5, 3→−2, 5→−3; FOVShiftDuration 0.15 |
| RecoilPattern | 1 point |
| RecoilPatternYawMinMax | −22.5 … +22.5; Pitch max 45.0 |
| RandomDeviationDegree | 10.0 |
| PostPatternRandomYaw / Pitch | Yaw (−0.5, 0.5); Pitch (0.5, 1.0) |
| AdsCameraCurve | [`CF_Pistol_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_Pistol_ADS_Curve.json) |
| AimSway stabilisation | AdsStabilizeTime 1.5, two unnamed fields (both 4.0) |
| MeleeDamage | 20 |

**DA_AT4_Stats** (rocket launcher)

| Field | Value |
|---|---|
| Aim sway | Speed/Horizontal/Vertical curves plus `TotalPatternDuration` 6.0, `NoFocusEnergySpeedMultiplier` 2.5, `PlayerCameraOffsetMultiplier` 0.75 |
| bFirstFocalPlane / bSpawnProjectileFromCameraWhenAds | both False |
| No recoil pattern, no ADS camera curve, no melee block | |

**DA_ArtilleryBarrelTest_Stats** (155 mm, 10 km range): `IronSightsAimTime` 12.0; `bSpawnProjectileFromCameraWhenAds` False; melee hitbox 0×0×0 and melee damage 0.

**DA_TankBarrelTest_Stats** (120×570 mm, 3.5 km range)
- `WeaponAccuracy` 70.0 with `AccuracyType = MinutesOfAngle`. That is a very loose spread compared with the SKS's 0.73.
- `IronSightsAimTime` 50,000.0. This looks wrong or unused, but the export gives no reason.

**DA_M2Browning_Stats** (stationary machine gun)
- `ViewKickCurve` 0→0, 0.15→1; `RecoveryKickCurve` 0→0, 0.3→0.2.
- `RecoilPattern` has **29** points (the largest pattern in this folder), with no aim-sway block.
- No `EffectiveRange` field.
- `SuppressionMultiplier` 0.8.

**DA_Fists_Stats**: `RandomDeviationDegree` 10.0; view kick 0→0, 0.15→1; recovery kick 0→0, 0.3→1.

---

## 2. Aim Sway Curve Families (`AimSway/<Class>/`)

Each weaponry class has a set of aim-sway curves. The `DA_*_Stats` assets reference them by name.

**Per-class curves** (`CurveFloat` unless noted. Min/max are over the whole curve; the time base is 0–6 s, the sway pattern duration.)

| Class | AimSway speed curve (min–max) | Horizontal sway (min–max) | Vertical sway (min–max) |
|---|---|---|---|
| AssaultRifle | 0.90 – 1.08 (v0 = 1.0) | −0.035 – +0.035 | −0.10 – +0.10 |
| DMR | 0.95 – 1.08 | −0.034 – +0.032 | −0.18 – +0.17 |
| LMG | 0.86 – 1.18 | −0.075 – +0.040 | −0.085 – +0.085 |
| Launchers | 0.92 – 1.02 | −0.2625 – +0.0525 | −0.105 – +0.090 |
| Pistol | 1.00 – 1.20 | −0.28 – 0 | −0.04375 – +0.04375 |
| SMG | 1.10 – 1.25 | −0.045 – +0.045 | −0.06 – +0.06 |
| Shotgun | 0.92 – 1.25 | −0.045 – +0.045 | −0.06 – +0.06 |
| SniperRifles | 0.93 – 1.09 | −0.034 – +0.032 | −0.18 – +0.17 |

Observations:
- DMR and SniperRifles have identical horizontal and vertical ranges (to the printed precision). They may share a template.
- The LMG has two extra ADS-stabilisation scalars: [`AdsStabilization_AimSwayScale_LMG`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/AimSway/LMG/AdsStabilization_AimSwayScale_LMG.json) (1.2 → 0.8) and [`AdsStabilization_AimSwaySpeed_LMG`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/AimSway/LMG/AdsStabilization_AimSwaySpeed_LMG.json) (1.12 → 1.0).

**Shared root curves** (in `Weapons/`): [`AimSway_SpeedCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/AimSway_SpeedCurve.json) (0.5–1.0), [`HorizontalAimSway_MovementCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/HorizontalAimSway_MovementCurve.json) (−0.015 – +0.02), [`VerticalAimSway_MovementCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/VerticalAimSway_MovementCurve.json) (−0.2 – +0.15). [`ADS_Blur_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/ADS_Blur_Curve.json) goes 0 → 1 over 0–1.

### 2a. ADS stabilisation (`CurveVector`)

Each class has two `CurveVector` assets, `AdsStabilizationRotation_<cls>` and `AdsStabilizationTranslation_<cls>`. Each has three channels, `FloatCurves[0..2]`, which per Unreal convention are X, Y and Z. The rotation and translation channels are shaped over t = 0–1.

| Class | Rotation X (min→max key) | Rotation Y | Translation X | Translation Y |
|---|---|---|---|---|
| AssaultRifle | 0 → −0.72 (6 keys) | 0 → 0 (flat) | 0 → −0.02 | 0 → −0.01 |
| DMR | 0 → −0.5 (6 keys, dips to −0.4 at 0.8) | 0 → −0.048 | 0 → −0.08 | 0 → −0.05 |
| LMG | 0 → −0.6 | 0 → 0.6 peak at 0.5 | 0 → −1.4 | 0 → −0.8 |
| Launchers | 0 → −0.4 | 0 → 0.18 at 0.7 | 0 → −0.35 | 0 → −0.2 |
| Pistol | 0 → 0.35 | 0 → 0.25 | 0 → 0.012 | 0 → 0.018 |
| SMG | 0 → 0.35 | 0 → 0.25 | 0 → 0.012 | 0 → 0.018 |
| Shotgun | 0 → 0.35 | 0 → 0.25 | 0 → 0.012 | 0 → 0.018 |
| SniperRifles | 0 → −3 (10 keys, peaks −3.5 at 0.95) | 0 → −1 (9 keys, peaks −1.8) | 0 → −0.5 | 0 → 0.85 |

The third channel (`FloatCurves[2]`) is near zero for every class except that the translation channel carries a `DefaultValue` of about 8.5e-08. The sign and meaning of the axes are not confirmed.

---

## 3. ADS Curves ([`Curves/ADSCurves/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Weapons/Curves/ADSCurves))

Eight `CurveFloat` assets, one per class. Each has 3 keys over t = 0–1. They rise from about 0 to 1.0 (the sniper curve starts at exactly 0).

| Asset | Used by (confirmed) |
|---|---|
| [`CF_AssaultRifle_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_AssaultRifle_ADS_Curve.json) | no `DA_*_Stats` in this folder reference it |
| [`CF_DMR_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_DMR_ADS_Curve.json) | [`DA_SKS_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/DMR/SKS/Data/DA_SKS_Stats.json) (`AdsCameraCurve`) |
| [`CF_LMG_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_LMG_ADS_Curve.json) | not referenced here |
| [`CF_Launcher_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_Launcher_ADS_Curve.json) | not referenced here |
| [`CF_Pistol_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_Pistol_ADS_Curve.json) | [`DA_Judge_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Pistol/Judge/Data/DA_Judge_Stats.json) (`AdsCameraCurve`) |
| [`CF_SMG_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_SMG_ADS_Curve.json) | not referenced here |
| [`CF_Shotgun_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_Shotgun_ADS_Curve.json) | not referenced here |
| [`CF_SniperRifles_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_SniperRifles_ADS_Curve.json) | not referenced here |

The meaning of the curve value (for example, FOV or blend fraction) is not stated in the export. The shape is the same for all classes.

---

## 4. Input Actions and Mapping Contexts (`Input/`)

### 4a. Input Actions (`BHInputAction`)

| Action | Tag | Trigger | Notes |
|---|---|---|---|
| IA_Weapon_Reload | `…HoldableItem.Weapon.Reload` | Tap | consume=false |
| IA_Weapon_ReloadDiscard | `…Weapon.Reload.Discard` | Hold | |
| IA_Weapon_CycleFireMode | `…Weapon.CycleFireMode` | none listed | |
| IA_Weapon_CycleSights / _Keyboard | `…Weapon.CycleSights` / `…CycleSightsKeyboard` | none | keyboard variant has consume=false |
| IA_Weapon_IncreaseZeroing | `…Weapon.IncreaseZeroing` | Tap | |
| IA_Weapon_DecreaseZeroing | `…Weapon.DecreaseZeroing` | Pressed | |
| IA_Weapon_ResetZeroing | `…Weapon.ResetZeroing` | Hold | |
| IA_Weapon_MeleeBash | `…Weapon.MeleeBash` | Pressed | |
| IA_Weapon_MountBipod | `…Weapon.Bipod.Mount` | Tap | |
| IA_Weapon_ToggleBipodFold | `…Weapon.Bipod.ToggleFold` | Hold | |
| IA_Weapon_ToggleAncillaryFire | `…Weapon.ToggleAncillaryFire` | Pressed | |
| IA_BuildTool_Rotate | `…HoldableItem.BuildTool.Rotate` | Pressed | |
| IA_BuildTool_ToggleSnapping | `…BuildTool.ToggleSnapping` | Pressed | |
| IA_BuildTool_Dismantle / _Release | `…BuildTool.Dismantle` / `.Release` | Pressed / Released | |
| IA_KeyCard_Use | `…HoldableItem.Keycard.PrimaryUse` | Pressed | has a PlayerMappableKeySettings block |
| IA_Projectile_Eject | `Input.NamedActions.Projectile.Eject` | Pressed | |
| IA_Drone_Projectile_Steer | `…Drone.Projectile.Steer` | none | `ValueType = Axis2D` |
| IA_Drone_Projectile_Boost / _Brake | `…Drone.Projectile.Boost` / `.Brake` | none | hold actions |

### 4b. Default key bindings (`IMC_*`, first-listed key per action)

| Context | Bindings (action = key; `[trigger]` where set) |
|---|---|
| IMC_BaseWeapon (25) | Reload = R (Gamepad Face Left); ReloadDiscard = R; CycleFireMode = B [Pressed] / DPad Up [Hold]; IncreaseZeroing = PageUp / DPad Up [Tap]; DecreaseZeroing = PageDown; ResetZeroing = **None**; MeleeBash = V / RB; PrimaryUse = LMB / RT; SecondaryUse = RMB / LT; Inspect = I; ToggleAncillaryFire = H; ToggleBipodFold = G / DPad Left; MountBipod = G / DPad Left |
| IMC_BuildTool (12) | Rotate = R / LB; ToggleSnapping = B / RB; PrimaryUse = LMB / RT; SecondaryUse = RMB / LT; Dismantle = V / R-stick press; Reload = R; Inspect = I |
| IMC_C4Weapon (5) | PrimaryUse = LMB / RT; TriggerUse = RMB / LT; Inspect = I |
| IMC_DeployableItem (9) | PrimaryUse = LMB / RT; SecondaryUse = RMB / LT; Rotate = R / LB; Holdable PrimaryUse Release = LMB / RT; Inspect = I |
| IMC_Fists (7) | PrimaryUse = LMB / RT [Hold, Released]; SecondaryUse = RMB / LT [Hold, Released]; Inspect = I; MeleeBash = V / RB |
| IMC_GrenadeWeapon (5) | PrimaryUse = LMB / RT; PrimaryAltUse = RMB / LT; Inspect = I |
| IMC_Action_KeyCard (2) | KeyCard_Use = LMB / LT |
| IMC_Drone_Projectile (20) | Eject = C / LB; Vehicle Reload = R / Face Left; ToggleFreeLook = LAlt / DPad Left; HoldFreeLook = LAlt / RB; Steer = W, A, S, D and Mouse2D; Boost = LShift / left stick press; Brake = LCtrl / LT; FreeLook = Mouse2D / right stick |
| IMC_ProjectileCamera (10) | Eject = C / LB; Reload = R / Face Left; FreeLook = Mouse2D / right stick; ToggleFreeLook = LAlt / DPad Left; HoldFreeLook = LAlt / DPad Left |

The 25-entry [`IMC_BaseWeapon`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IMC_BaseWeapon.json) also binds the `IA_Player_*` actions for Inspect, Holdable Secondary Use and Holdable Primary Use Release.

---

## 5. How Values Combine

The export lists the inputs to each system but not the formulas that combine them. Recoil (§5a), aim sway and focus energy (§5b) are traced in code.

- **Recoil:** §5a.
- **Aim sway and focus energy:** §5b.
- **Evidence:** [`docs/evidence/weapons.md`](docs/evidence/weapons.md): a verification status for every native address §5a and §5b cite.
- **Distance falloff (SKS):** `DistanceDamageFalloffCurve` is a multiplier indexed by distance. The falloff times are centimetres of distance, confirmed in code; per-weapon damage by distance is in [DamagePipeline §7.8](Wardogs_DamagePipeline_v2.md#78-damage-over-distance).

### 5a. Recoil

**Native.** Recoil is a kick to the player's view (the control rotation), in degrees: X is yaw (positive turns right) and Y is pitch (positive looks up).

1. **Which pattern point.** The fire routine (`0x6B93610`) computes a kick per shot, but only when the weapon owner's controller is a local `WDPlayerController` (`0x6B96C20`, which ends in `APlayerController::IsLocalController`, `0x42CD0B0`). The weapon component keeps a shot counter (`+0xFF0`) that starts at −1 (constructor `0x6B8E5A0`). Shot `n` = counter + 1 uses pattern point `n`, then the counter moves on. Every shot restarts a timer of `RecoilPatternResetTime` seconds, and when the timer runs out the counter goes back to −1 (`0x6B97550`). So the pattern starts over after any pause longer than the reset time.
2. **The kick** (`0x6B95C50`):
   - Inside the pattern: `RecoilPattern[n]`, turned by a random angle between −`RandomDeviationDegree` and +`RandomDeviationDegree` degrees. The turn changes the kick's direction, not its size.
   - Past the end of the pattern, and on every shot of a weapon without one: yaw uniform between the two values of `PostPatternRandomYawRecoil`, pitch uniform between the two values of `PostPatternRandomPitchRecoil`.
   - Then yaw × the weapon's `HorizontalRecoilMultiplier` and pitch × its `VerticalRecoilMultiplier`. These are the current values of the `Attribute.Gameplay.Weapon.*RecoilMultiplier` attributes on the weapon item, or 1 if it has none (`0x6C979A0`, `0x6C989A0`, the item extension's `IWDWeaponOwner` at `+0xF0`). Both start at 1.0 on every weapon ([GameFeatures Weapons §4](Wardogs_GameFeatures_Weapons_v2.md#4-default-weapon-attributes-wditemextensiondata_gameplayeffects)); attachment and stance effects change them by the [effect formula](Wardogs_GameplayEffectsPipeline_v1.md#44-current-value).
   - The random numbers come from the C runtime's `rand()`. `RecoilPatternYawMinMax` and `RecoilPatternPitchMax` are not read here.
3. **Focus and size** (weapon behavior component, `0x6B85D30`):
   - While focusing (the focus blend is above `MinFocusInterpRequiredForRecoilReduction` / 100; that field is 80 by default and no asset changes it), the kick shrinks by `RecoilReductionWhenFocussing` percent.
   - While focusing, and for a short window after it (an unnamed stats field at `+0x98`: default 0.5 s, set by no weapon), each shot drains `FocusEnergyReductionPerShot` percent of `MaxFocusEnergy` (10), down to 0.
   - The kick is then multiplied by `ViewKickMagnitudeMultiplier` and queued.
4. **Applying it** (`TickComponent` `0x6B891F0` → `0x6B89A20` → `0x6B89BB0`), for a pawn with a player controller. Each queued kick follows `ViewKickCurve`, read as a value between 0 and 1. Every frame, pitch and yaw move by (curve value now − curve value last frame) × kick. A curve that rises from 0 to 1 therefore applies the whole kick over the curve's length. A curve that falls back hands part of the kick back: the SKS curve reaches 1 at 0.15 s and 0.75 at 0.4 s, so a quarter of each kick returns. Pitch is kept within the camera's pitch limits, and any part cut off there is remembered.
5. **Recovery.** When a kick's curve ends, the kick (less any pitch that was cut off) is added to a recovery amount, and the view moves back along `RecoveryKickCurve` the same way. A kick that ends during a recovery restarts it with the rest of the old amount plus the new kick. Every firearm's `RecoveryKickCurve` is a single key at 0, so no firearm recovers by itself: the player pulls the view back. Three launchers (the grenade launcher, `Launcher_04`, `RPG7`) return the whole kick, over 1 s or 0.35 s; the MMGL does not. Outside the table, the M2 Browning returns 20% of each kick over 0.3 s and the fists all of it over 0.3 s.

**Example.** An AK-74M without attachments, standing, not focusing. Both multipliers are 1: the AR stance effect is ×1 standing, ×0.85 crouched and ×0.7 prone. Shot 1 is `RecoilPattern[0]` = (0.01, 0.718) × 1.1: a kick of about 0.79°, pointing up to 13° either side of the pattern's direction (almost straight up), applied over 0.18 s. Shots 31 and on kick yaw −0.31 … 0.31° and pitch 0.50 … 0.83° (the post-pattern ranges × 1.1). Pausing longer than 0.65 s restarts the pattern.

The table gives each weapon's inputs. Yaw and pitch are in degrees. A dagger (†) marks the native default from the `FWDWeaponStats` constructor (`0x699E6C0`), which the asset does not store. Attachment and stance multipliers are not applied. Curve values outside 0 … 1 count as 0 or 1: the `Launcher_04` and `RPG7` kick curves rise to 8, so their whole kick lands before 0.2 s.

<!-- recoil_table -->
| Weapon | Pattern shots | Shot 1 (yaw, pitch) | Deviation (°) | After pattern: yaw | After pattern: pitch | Reset (s) | Kick × | Kick curve | Recovery | Focus: recoil cut % / energy % per shot |
|---|---:|---|---:|---|---|---:|---:|---|---|---|
| `SKS` | 20 | -0.025538, 2.375 | ±5.5 | -0.28 … 0.38 | 0.55 … 0.85 | 0.95 | ×1† | 1 at 0.15 s, 0.75 at 0.4 s | none | 30 / 50 |
| `Judge` | 1 | 0.09, 2.24775 | ±10 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | ×1† | 1 at 0.15 s | none | 10 / 40 |
| `AT4` | 0 | — | ±5† | -1 … 1† | 1 … 2† | 0.5† | ×1† | none (no curve) | none | 0† / 0† |
| `CombatBow` | 0 | — | ±4 | -1 … 1† | 2 … 3 | 0.2 | ×0 | 1 at 0.15 s, 0.5 at 0.4 s | none | 80 / 100 |
| `GrenadeLauncher` | 0 | — | ±5† | -1 … 1† | 1 … 2† | 0.5† | ×1† | 1 at 1 s | 100% over 1 s | 0† / 0† |
| `RFB` | 20 | 0.15, 2.34 | ±10 | -0.28 … 0.34 | 0.74 … 0.98 | 1 | ×1† | 1 at 0.15 s | none | 30 / 50 |
| `SVDM` | 9 | -0.283, 3.683 | ±10 | 0.05 … 0.32 | 0.65 … 1.1 | 1.1 | ×1† | 1 at 0.15 s, 0.75 at 0.4 s | none | 30 / 50 |
| `LMG_02` | 30 | 0.13, 1.68 | ±20 | -0.62 … 0.72 | 1.1 … 1.95 | 0.9 | ×1.25 | 1 at 0.3 s | none | 50 / 10 |
| `Launcher_04` | 0 | — | ±5† | -1 … 1† | 1 … 2† | 0.5† | ×1† | 8 at 0.2 s | 100% over 0.35 s | 0† / 0† |
| `RPG7` | 0 | — | ±5† | -1 … 1† | 1 … 2† | 0.5† | ×1† | 8 at 0.2 s | 100% over 0.35 s | 0† / 0† |
| `AK74M` | 30 | 0.01, 0.717554 | ±13 | -0.28 … 0.28 | 0.45 … 0.75 | 0.65 | ×1.1 | 1 at 0.18 s | none | 20 / 25 |
| `M4` | 30 | 0.037, 0.693 | ±10 | -0.26 … 0.26 | 0.4 … 0.65 | 0.55 | ×1.08 | 1 at 0.15 s | none | 20 / 25 |
| `KH2002` | 30 | 0, 0.85 | ±15 | -0.25 … 0.25 | 0.5 … 0.72 | 0.78 | ×1† | 1 at 0.15 s | none | 30 / 40 |
| `A91` | 30 | 0, 0.85 | ±15 | -0.25 … 0.25 | 0.5 … 0.72 | 0.78 | ×1† | 1 at 0.15 s | none | 0† / 0† |
| `TAR21` | 30 | 0, 0.7 | ±15 | -0.22 … 0.22 | 0.55 … 0.8 | 0.8 | ×1.1 | 1 at 0.15 s | none | 30 / 40 |
| `Vector` | 55 | 0.09, 0.267748 | ±35 | -0.05 … 0.05 | -0.08 … 0.12 | 0.48 | ×1† | 1 at 0.15 s | none | 15 / 25 |
| `SV98` | 0 | — | ±4 | -1 … 1† | 1 … 2† | 0.5† | ×1.3 | 1 at 0.15 s | none | 0† / 100 |
| `M249` | 7 | 1.10714, 2.40603 | ±20 | -0.5 … 0.5 | 0.5 … 1.5 | 0.5† | ×1.2 | 1 at 0.3 s | none | 50 / 10 |
| `Glock17` | 0 | — | ±10 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | ×1.5 | 1 at 0.15 s | none | 10 / 40 |
| `M12G (M500)` | 7 | 0.11, 1.8 | ±24 | -0.5 … 0.5 | 0.9 … 1.6 | 1 | ×1.6 | 1 at 0.5 s | none | 0† / 0† |
| `MMGL` | 0 | — | ±5† | -1 … 1† | 1 … 2† | 0.5† | ×1† | 1 at 1 s | none | 0† / 0† |
| `CGM4` | 0 | — | ±5† | -1 … 1† | 1 … 2† | 0.5† | ×1† | none (no curve) | none | 0† / 0† |
| `MP9` | 30 | 0.01815, 0.6292 | ±15 | -0.3 … 0.3 | 0.3 … 0.55 | 0.55 | ×1.1 | 1 at 0.1 s | none | 15 / 25 |
| `WEPN_017 (Mosin)` | 0 | — | ±4 | -1 … 1† | 2 … 3 | 0.2 | ×0.8 | 1 at 0.15 s | none | 0† / 100 |
| `WEPN_026` | 0 | — | ±10 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | ×1.85 | 1 at 0.15 s | none | 10 / 40 |
| `WEPN_027` | 15 | 0, 1.16775 | ±5† | 0.25 … 1 | 0.25 … 1 | 0.5† | ×1† | 1 at 0.15 s | none | 10 / 40 |
| `WEPN_028` | 30 | -0.088829, 0.7161 | ±20 | -0.32 … 0.32 | 0.35 … 0.58 | 0.5† | ×1.15 | 1 at 0.1 s | none | 15 / 25 |
| `WEPN_029` | 30 | -0.01, 0.3969 | ±12 | -0.3 … 0.3 | 0.5 … 0.78 | 0.8 | ×0.95 | 1 at 0.18 s | none | 20 / 25 |
| `WEPN_030` | 20 | 0.055, 1.09725 | ±16 | -0.35 … 0.35 | 0.7 … 1.1 | 0.7 | ×1† | 1 at 0.15 s | none | 20 / 25 |
| `WEPN_031` | 30 | 0.0345, 1.13949 | ±17 | -0.2 … 0.2 | 0.4 … 0.62 | 0.6 | ×1† | 1 at 0.15 s | none | 30 / 50 |
| `WEPN_032` | 50 | 0.0360022, 1.53 | ±10 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | ×1† | 1 at 0.15 s | none | 10 / 40 |
| `WEPN_033 (TAR21)` | 30 | 0, 0.85 | ±15 | -0.25 … 0.25 | 0.5 … 0.72 | 0.78 | ×1† | 1 at 0.15 s | none | 30 / 40 |
| `WEPN_034` | 32 | 0, 3.06 | ±10 | 0.05 … 0.32 | 0.65 … 1.1 | 1.1 | ×1† | 0.806773 at 0.0578813 s, 1 at 0.15 s | none | 30 / 50 |
| `WEPN_035` | 0 | — | ±4 | -1 … 1† | 1 … 2† | 0.5† | ×0.3 | 1 at 0.15 s | none | 0† / 100 |
| `WEPN_036` | 40 | 0, 2.5306 | ±15 | -0.22 … 0.22 | 1.35 … 1.7 | 0.75 | ×1† | 1 at 0.15 s | none | 50 / 10 |
| `WEPN_037` | 30 | 0.0154, 1.07484 | ±14 | -0.34 … 0.34 | 0.62 … 0.95 | 0.5† | ×0.9 | 1 at 0.15 s | none | 30 / 50 |
| `SMG_03` | 30 | 0.033, 1.08994 | ±17 | -0.2 … 0.2 | 0.4 … 0.62 | 0.55 | ×1† | 1 at 0.1 s | none | 30 / 50 |
| `MP43` | 2 | 0.840004, 1.71 | ±28 | -0.45 … 0.45 | 0.8 … 1.4 | 1.2 | ×1.15 | 1 at 0.15 s | none | 0† / 0† |
| `MK22` | 0 | — | ±4 | -1 … 1† | 1 … 2† | 0.5† | ×1.4 | 1 at 0.15 s | none | 0† / 100 |
| `SR_04` | 0 | — | ±4 | -1 … 1† | 1 … 2.5 | 0.5† | ×1.45 | 1 at 0.124178 s | none | 0† / 100 |
<!-- /recoil_table -->

### 5b. Aim sway and focus energy

**Native** (weapon behavior component, `0x6B884D0`, run from `TickComponent` every frame). While aiming down sights (`IsAiming`, component `+0x3E0`), the view drifts along a looping pattern. The component's `AimSwayMode` is `Camera` (constructor `0x6B84E80`; no asset changes it), so the drift moves the control rotation. Every attribute below is a character or weapon attribute that counts as 1 when absent.

1. **Focus energy.** While focusing and aiming, focus energy drains at the weapon's `Attribute.Gameplay.Weapon.FocusEnergyUsageMultiplier` per second. Otherwise it refills at 1 per second up to `MaxFocusEnergy`, which is 10 (component defaults). At the default rate a full bar lasts 10 s, and shots drain it too (§5a). When it reaches 0, focus stops (`0x6B88310`) and the pawn's action system is called with `Action.Player.Focus`.
2. **Sway size.** A scale eases toward its target with `FInterpTo`, at `SwayScaleIncreaseCorrectionSpeed` when growing and `SwayScaleDecreaseCorrectionSpeed` when shrinking. The target is the product of:
   - the character's `AimSwayScaleMultiplier`;
   - the stance's `StandOffsetMultiplier`, `CrouchOffsetMultiplier` or `ProneOffsetMultiplier`;
   - `AdsAimSwayScaleCurve` at the stabilization progress;
   - `FocusOffsetMultiplier`, while focusing.
3. **Sway speed.** A speed eases the same way, at `SwaySpeedIncreaseCorrectionSpeed` / `SwaySpeedDecreaseCorrectionSpeed`. Its target is the product of:
   - `AimSwaySpeedCurve` at the pattern time;
   - `AdsAimSwaySpeedCurve` at the stabilization progress;
   - the character's `AimSwaySpeedMultiplier`;
   - when not focusing, a factor that runs linearly from `NoFocusEnergySpeedMultiplier` with an empty focus bar to 1 with a full one.
4. **Pattern.** Pattern time advances by speed × frame time and wraps at `TotalPatternDuration`. At each wrap (`0x6B87260`), two deviation curves are rebuilt. Each gets one random key per key of its movement curve, at the same time, with a value uniform in `HorizontalDeviationRange` or `VerticalDeviationRange`. Every loop follows the same timing with new random amplitudes.
5. **Offset.** Yaw = `HorizontalAimSwayMovementCurve` × the horizontal deviation curve × the character's `AimSwayHorizontalMovementMultiplier` × scale, with both curves read at the pattern time. Pitch works the same way with the vertical curves and `AimSwayVerticalMovementMultiplier`. Each frame, the change in this offset × `PlayerCameraOffsetMultiplier` is added to the control rotation.

The stabilization progress is the component's stabilization timer (`+0x408`) divided by `AdsStabilizeTime`, kept between 0 and 1. The two `AdsAimSway…Curve`s count as 1 when they have no keys. How the timer itself runs (`AdsStabilizeCooldownRate` and the other stabilization fields) is not traced. Neither are the weapon-model sway (the `WeaponSway.*` attributes, idle and stabilization sway, jitter) or the `Weapon` mode. `bPersistentValues` and `PersistentData` are not read by this code.

---

## 6. Still Not Pulled / Limitations

- The main AR, SMG, LMG, shotgun and pistol **stat tables** are not in this folder. Only their aim-sway and stabilisation curves are here. The stat tables are in [Infantry Weapon Stats](Wardogs_InfantryWeapons_Stats_v1.html).
- **Units are not stated** in the export. Speeds are assumed to be cm/s and ranges to be metres, based on the falloff-curve and EffectiveRange check. That is an inference. Recoil values are degrees of view rotation, confirmed in code (§5a).
- `IronSightsAimTime = 50,000` on the tank barrel and `WeaponAccuracy = 70 MOA` look like placeholders or unused tuning. The export gives no way to check.
- Two unnamed fields on the SKS and Judge have no known meaning. Values: SKS 1.0 and 2.5, Judge 2.0.
- `CF_*_ADS_Curve` and [`ADS_Blur_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/ADS_Blur_Curve.json) have no stated output meaning.
- Curve tangents and interpolation modes are not summarised. Only key times and values are reported.
- The M2 recoil pattern has 29 points; the full list is not reproduced.
- Input mapping contexts are shown only for their first key per action. Secondary keys and gamepad alternates are summarised, not listed in full.
