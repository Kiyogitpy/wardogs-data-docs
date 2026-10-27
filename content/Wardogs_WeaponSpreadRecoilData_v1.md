---
title: "Weapon Spread and Recoil Data"
redirect_from: ["/Wardogs_WeaponSpreadRecoilData_v1.html", "/Wardogs_WeaponSpreadRecoilData_v1"]
parent: "Weapons & Ammo"
description: "Every weapon's spread, recoil, camera-kick, sway and movement-accuracy values, row by row, with curve keys and native defaults"
---

# Wardogs — Weapon Spread and Recoil Data

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

One row per weapon for every spread, recoil, camera-kick, sway and movement-accuracy field in the cooked data. Nothing here was measured in the
game. Labels: **Data** for what the export says, **Native** for a value read from the constructor when the asset omits the field.

How the numbers are used: [Weapon Spread pipeline](../pipelines/Wardogs_WeaponSpread_v1.md) (the code that turns these fields into a cone) and
[Hit Registration](../pipelines/Wardogs_HitRegistration_v1.md). Field meanings and the recoil formula: [Weapons](Wardogs_Weapons_v2.md) (§5a, §5b).
Attachment effects on the multipliers: [Weapon Attributes](Wardogs_WeaponAttributes_v1.md). Full raw property export: [Infantry Weapon Stats](Wardogs_InfantryWeapons_Stats_v1.md).

**Machine-readable:** [`weapon-spread-recoil.json`](../assets/data/weapon-spread-recoil.json) holds the same rows with every curve key (time, value, interpolation,
tangents), the resolved native defaults and the source file of each weapon. Regenerate both with `python -I _tools/spread_recoil_tables.py --write`.

**Native defaults.** An exported asset leaves out every property that still equals the class default. The script disassembles the `FWDWeaponStats`
constructor (RVA `0x699E6C0` in the reference image, 0xE48 bytes), applies every store to a byte map, follows its memset and curve-constructor calls, and
reads each omitted field at its offset (field names and offsets from the SDK dump). This is the same method as `_tools/native_defaults_check.py`.

<!-- spread_recoil_tables -->
61 `WDWeaponStatsData` assets (40 infantry, 21 vehicle, stationary or test weapons), 40 of them with a ranged-weapon item. `†` marks a value the asset omits, taken from the `FWDWeaponStats` constructor. `—` means the object has no such field (items) or no item.

### Native defaults used

| Field | Group | Offset in `FWDWeaponStats` | Type | Native default |
|---|---|---|---|---|
| `WeaponAccuracy.AccuracyType` | Spread and accuracy | `0x0` | EWDWeaponAccuracyType | `Milliradians` |
| `WeaponAccuracy.AccuracyValue` | Spread and accuracy | `0x4` | f32 | `1` |
| `bSpawnProjectileFromCameraWhenAds` | Spread and accuracy | `0x16c` | bool | `yes` |
| `RandomDeviationDegree` | Spread and accuracy | `0xce0` | f32 | `5` |
| `ShotgunData.ChokeFactor` | Spread and accuracy | `0xd40` | f32 | `0.8` |
| `ShotgunData.bSeparateOuterConeHalfAngles` | Spread and accuracy | `0xd44` | bool | `no` |
| `ShotgunData.OuterConeHalfAngle` | Spread and accuracy | `0xd48` | f32 | `10` |
| `ShotgunData.OuterConeHorizontalHalfAngle` | Spread and accuracy | `0xd4c` | f32 | `10` |
| `ShotgunData.OuterConeVerticalHalfAngle` | Spread and accuracy | `0xd50` | f32 | `10` |
| `ShotgunData.OuterPreviewDistance` | Spread and accuracy | `0xd54` | f32 | `0` |
| `ShotgunData.OuterSpreadDistance` | Spread and accuracy | `0xd58` | f32 | `0` |
| `ShotgunData.OuterHorizontalSpreadDistance` | Spread and accuracy | `0xd5c` | f32 | `0` |
| `ShotgunData.OuterVerticalSpreadDistance` | Spread and accuracy | `0xd60` | f32 | `0` |
| `ShotgunData.bSeparateRandomConeHalfAnglesRanges` | Spread and accuracy | `0xd64` | bool | `no` |
| `ShotgunData.RandomConeHalfAngleRange` | Spread and accuracy | `0xd68` | vec2 | `0 … 0` |
| `ShotgunData.RandomConeHorizontalHalfAngleRange` | Spread and accuracy | `0xd78` | vec2 | `0 … 0` |
| `ShotgunData.RandomConeVerticalHalfAngleRange` | Spread and accuracy | `0xd88` | vec2 | `0 … 0` |
| `ShotgunData.InnerConeHalfAngleMultiplier` | Spread and accuracy | `0xd98` | f32 | `0.5` |
| `FocusEnergyReductionPerShot` | Recoil | `0x94` | f32 | `0` |
| `_aaabimbpohdlmnphjbidm` | Recoil | `0x98` | f32 | `0.5` |
| `RecoilReductionWhenFocussing` | Recoil | `0x9c` | f32 | `0` |
| `FocusData.FocusEnergyUsageMultiplier` | Recoil | `0xae0` | f32 | `1` |
| `FocusData.FocusEnergyRecoveryMultiplier` | Recoil | `0xae4` | f32 | `1` |
| `FocusData.AdditionalFocusZoom` | Recoil | `0xae8` | f32 | `20` |
| `RecoilPattern` | Recoil | `0xca0` | array | `none` |
| `RecoilPatternYawMinMax` | Recoil | `0xcb0` | interval | `-1 … 1` |
| `RecoilPatternPitchMax` | Recoil | `0xcb8` | f32 | `1` |
| `PostPatternRandomYawRecoil` | Recoil | `0xcc0` | vec2 | `-1 … 1` |
| `PostPatternRandomPitchRecoil` | Recoil | `0xcd0` | vec2 | `1 … 2` |
| `RecoilPatternResetTime` | Recoil | `0xce4` | f32 | `0.5` |
| `FiringAnimationOffsetType` | Recoil | `0xce8` | EWDFiringAnimationOffsetType | `None` |
| `MinimumRandomFiringAnimationOffset` | Recoil | `0xcf0` | vec2 | `0 … 0` |
| `MaximumRandomFiringAnimationOffset` | Recoil | `0xd00` | vec2 | `0 … 0` |
| `FiringAnimationOffsetPatternMultiplier` | Recoil | `0xd10` | vec2 | `1 … 1` |
| `AdsCameraCurve` | Camera kick | `0x8` | curve | `empty curve (no keys)` |
| `FovInterpSpeed` | Camera kick | `0x90` | f32 | `20` |
| `IronSightsAimTime` | Camera kick | `0x154` | f32 | `0.2` |
| `IronSightsFovMultiplier` | Camera kick | `0x158` | f32 | `1.2` |
| `ViewKickCurve` | Camera kick | `0xaf0` | curve | `empty curve (no keys)` |
| `ViewKickMagnitudeMultiplier` | Camera kick | `0xb78` | f32 | `1` |
| `RecoveryKickCurve` | Camera kick | `0xb80` | curve | `empty curve (no keys)` |
| `FOVShiftingType` | Camera kick | `0xc08` | EWDWeaponFOVShiftingType | `None` |
| `FOVShiftDeltaAmount` | Camera kick | `0xc0c` | f32 | `-2.5` |
| `FOVShiftingCurve` | Camera kick | `0xc10` | curve | `empty curve (no keys)` |
| `FOVShiftDuration` | Camera kick | `0xc98` | f32 | `0.25` |
| `AimSwayData.CurveData.HorizontalAimSwayMovementCurve` | Movement accuracy | `0x458` | curve | `empty curve (no keys)` |
| `AimSwayData.CurveData.VerticalAimSwayMovementCurve` | Movement accuracy | `0x4e0` | curve | `empty curve (no keys)` |
| `AimSwayData.PlayerSpeedStabilizationMultiplierCurve` | Movement accuracy | `0x918` | curve | `empty curve (no keys)` |
| `AimSwayData.ADSStabilizationMovementSpeedRateUp` | Movement accuracy | `0x9a0` | f32 | `6` |
| `AimSwayData.ADSStabilizationMovementSpeedRateDown` | Movement accuracy | `0x9a4` | f32 | `1.5` |
| `AimSwayData.AdsStabilizationData.AdsStabilizeCooldownRateMovingMultiplier` | Movement accuracy | `0xacc` | f32 | `3` |
| `AimSwayData.AdsStabilizationData.AdsStabilizeMovementProgressPenalty` | Movement accuracy | `0xad0` | f32 | `1` |
| `bAnimationSwayEnabled` | Sway | `0x16d` | bool | `yes` |
| `AnimationSwayData.StandSwayMultiplier` | Sway | `0x170` | f32 | `1` |
| `AnimationSwayData.CrouchSwayMultiplier` | Sway | `0x174` | f32 | `0.75` |
| `AnimationSwayData.ProneSwayMultiplier` | Sway | `0x178` | f32 | `0.5` |
| `AnimationSwayData.bPersistentHipValues` | Sway | `0x17c` | bool | `yes` |
| `AnimationSwayData.HipPitchSwayMultiplier` | Sway | `0x180` | f32 | `-0.25` |
| `AnimationSwayData.HipPitchSwayMultiplierCurve` | Sway | `0x188` | curve | `empty curve (no keys)` |
| `AnimationSwayData.HipYawSwayMultiplier` | Sway | `0x210` | f32 | `0.25` |
| `AnimationSwayData.HipYawSwayMultiplierCurve` | Sway | `0x218` | curve | `empty curve (no keys)` |
| `AnimationSwayData.bPersistentADSValues` | Sway | `0x2a0` | bool | `yes` |
| `AnimationSwayData.ADSPitchSwayMultiplier` | Sway | `0x2a4` | f32 | `1` |
| `AnimationSwayData.ADSPitchSwayMultiplierCurve` | Sway | `0x2a8` | curve | `empty curve (no keys)` |
| `AnimationSwayData.ADSYawSwayMultiplier` | Sway | `0x330` | f32 | `1` |
| `AnimationSwayData.ADSYawSwayMultiplierCurve` | Sway | `0x338` | curve | `empty curve (no keys)` |
| `AimSwayData.bPersistentValues` | Sway | `0x3c0` | bool | `yes` |
| `AimSwayData.PersistentData.AimSwaySpeed` | Sway | `0x3c4` | f32 | `0.1` |
| `AimSwayData.PersistentData.HorizontalAimSwayMagnitude` | Sway | `0x3c8` | f32 | `1` |
| `AimSwayData.PersistentData.VerticalAimSwayMagnitude` | Sway | `0x3cc` | f32 | `1` |
| `AimSwayData.CurveData.AimSwaySpeedCurve` | Sway | `0x3d0` | curve | `empty curve (no keys)` |
| `AimSwayData.CurveData.HorizontalDeviationRange` | Sway | `0x568` | interval | `1 … 1` |
| `AimSwayData.CurveData.VerticalDeviationRange` | Sway | `0x570` | interval | `1 … 1` |
| `AimSwayData.TotalPatternDuration` | Sway | `0x578` | f32 | `0` |
| `AimSwayData.StandOffsetMultiplier` | Sway | `0x57c` | f32 | `1` |
| `AimSwayData.CrouchOffsetMultiplier` | Sway | `0x580` | f32 | `0.75` |
| `AimSwayData.ProneOffsetMultiplier` | Sway | `0x584` | f32 | `0.5` |
| `AimSwayData.FocusOffsetMultiplier` | Sway | `0x588` | f32 | `0.25` |
| `AimSwayData.NoFocusEnergySpeedMultiplier` | Sway | `0x58c` | f32 | `1` |
| `AimSwayData.CorrectionOffsetTime` | Sway | `0x590` | f32 | `2.5` |
| `AimSwayData.PlayerCameraOffsetMultiplier` | Sway | `0x594` | f32 | `0.25` |
| `AimSwayData.SwayScaleDecreaseCorrectionSpeed` | Sway | `0x598` | f32 | `2` |
| `AimSwayData.SwayScaleIncreaseCorrectionSpeed` | Sway | `0x59c` | f32 | `2` |
| `AimSwayData.SwaySpeedDecreaseCorrectionSpeed` | Sway | `0x5a0` | f32 | `2` |
| `AimSwayData.SwaySpeedIncreaseCorrectionSpeed` | Sway | `0x5a4` | f32 | `2` |
| `AimSwayData.WeaponRotationIdleSwayMultiplier` | Sway | `0x5a8` | f32 | `0` |
| `AimSwayData.WeaponTranslationIdleSwayMultiplier` | Sway | `0x5ac` | f32 | `0` |
| `AimSwayData.WeaponTranslationStabilizationSway` | Sway | `0x5b0` | vcurve | `empty curve (no keys)` |
| `AimSwayData.WeaponTranslationStabilizationSwayCurveStanceMultiplier.StandMultiplier` | Sway | `0x738` | f32 | `1` |
| `AimSwayData.WeaponTranslationStabilizationSwayCurveStanceMultiplier.CrouchMultiplier` | Sway | `0x73c` | f32 | `0.5` |
| `AimSwayData.WeaponTranslationStabilizationSwayCurveStanceMultiplier.ProneMultiplier` | Sway | `0x740` | f32 | `0.25` |
| `AimSwayData.WeaponRotationStabilizationSway` | Sway | `0x748` | vcurve | `empty curve (no keys)` |
| `AimSwayData.WeaponRotationStabilizationSwayCurveStanceMultiplier.StandMultiplier` | Sway | `0x8d0` | f32 | `1` |
| `AimSwayData.WeaponRotationStabilizationSwayCurveStanceMultiplier.CrouchMultiplier` | Sway | `0x8d4` | f32 | `0.5` |
| `AimSwayData.WeaponRotationStabilizationSwayCurveStanceMultiplier.ProneMultiplier` | Sway | `0x8d8` | f32 | `0.25` |
| `AimSwayData.WeaponRotationStabilizationSwayMultiplier` | Sway | `0x8dc` | f32 | `0` |
| `AimSwayData.WeaponTranslationStabilizationSwayMultiplier` | Sway | `0x8e0` | f32 | `0` |
| `AimSwayData.bUseTranslationStabilizationJitter` | Sway | `0x8e4` | bool | `no` |
| `AimSwayData.TranslationStabilizationJitter.StabilizationNoiseResultOffset` | Sway | `0x8e8` | f32 | `0` |
| `AimSwayData.TranslationStabilizationJitter.StabilizationNoiseJitter` | Sway | `0x8ec` | f32 | `2` |
| `AimSwayData.TranslationStabilizationJitter.StabilizationInitialOffset` | Sway | `0x8f0` | f32 | `2` |
| `AimSwayData.TranslationStabilizationJitter.GeneralPathJitter` | Sway | `0x8f4` | f32 | `0.2` |
| `AimSwayData.TranslationStabilizationJitter.SecondaryJitter` | Sway | `0x8f8` | f32 | `0.2` |
| `AimSwayData.bUseRotationStabilizationJitter` | Sway | `0x8fc` | bool | `no` |
| `AimSwayData.RotationStabilizationJitter.StabilizationNoiseResultOffset` | Sway | `0x900` | f32 | `0` |
| `AimSwayData.RotationStabilizationJitter.StabilizationNoiseJitter` | Sway | `0x904` | f32 | `2` |
| `AimSwayData.RotationStabilizationJitter.StabilizationInitialOffset` | Sway | `0x908` | f32 | `2` |
| `AimSwayData.RotationStabilizationJitter.GeneralPathJitter` | Sway | `0x90c` | f32 | `0.2` |
| `AimSwayData.RotationStabilizationJitter.SecondaryJitter` | Sway | `0x910` | f32 | `0.2` |
| `AimSwayData.SightSwayDefaultDistanceOffset` | Sway | `0x914` | f32 | `0` |
| `AimSwayData.StabilizationHoldTime` | Sway | `0x9a8` | f32 | `0.3` |
| `AimSwayData.AdsStabilizationData.AdsAimSwayScaleCurve` | Sway | `0x9b0` | curve | `empty curve (no keys)` |
| `AimSwayData.AdsStabilizationData.AdsAimSwaySpeedCurve` | Sway | `0xa38` | curve | `empty curve (no keys)` |
| `AimSwayData.AdsStabilizationData.AdsStabilizeTime` | Sway | `0xac0` | f32 | `0.5` |
| `AimSwayData.AdsStabilizationData.AdsStabilizeCooldownRate` | Sway | `0xac4` | f32 | `2` |
| `AimSwayData.AdsStabilizationData.AdsStabilizeExitGracePeriod` | Sway | `0xac8` | f32 | `0.15` |
| `AimSwayData.AdsStabilizationData._aaacalknjllchnkieahdj` | Sway | `0xad4` | f32 | `3` |
| `AimSwayData.AdsStabilizationData._aaablccoleojpkdkeghnk` | Sway | `0xad8` | f32 | `0` |
| `AimSwayData.AdsStabilizationData._aaabiaflojcopmfgdolfd` | Sway | `0xadc` | f32 | `0` |

## 1. Spread and accuracy

The aim cone itself is `WeaponAccuracy` (minutes of angle or milliradians) times the stance spread rows below times the `SpreadMultiplier` and `AccuracyMultiplier` attributes; how the code combines them is in the [weapon spread pipeline](../pipelines/Wardogs_WeaponSpread_v1.md). `RandomDeviationDegree` is the per-shot random cone used with the recoil pattern (see section 2). There is no field named bloom in the cooked weapon data; the in-game bloom is the spread rows.

### 1a. Stats-asset fields

| Weapon | Class | Accuracy type | Accuracy value | Random deviation (deg) | Projectile from camera in ADS | Choke | Separate outer cone | Outer cone half angle | Separate random cone | Random cone range | Inner cone × |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | Infantry | Milliradians† | 1.5 | 15 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `AK74M` | Infantry | Milliradians† | 0.825 | 13 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `AT4` | Infantry | Milliradians† | 1† | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `ArtilleryBarrelTest` | Other | Milliradians† | 1† | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `BuildTool` | Other | Milliradians† | 1† | 5† | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `CGM4` | Infantry | Milliradians† | 2.5 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `CombatBow` | Infantry | Milliradians† | 0 | 4 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `Fists` | Other | Milliradians† | 1† | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `Glock17` | Infantry | Milliradians† | 3.49 | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `GrenadeLauncher` | Infantry | Milliradians† | 1† | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `Judge` | Infantry | Milliradians† | 3.49 | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `KH2002` | Infantry | Milliradians† | 1.5 | 15 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `LMG_02` | Infantry | Milliradians† | 2.5 | 20 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `Launcher_04` | Infantry | Milliradians† | 1† | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `M12G` | Infantry | Milliradians† | 1.5 | 24 | no | 0.5 | no† | 1.56 | no† | 0 … 2 | 0.5† |
| `M249` | Infantry | Milliradians† | 4.3 | 20 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `M2Browning` | Stationary | Milliradians† | 1† | 5† | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `M4` | Infantry | Milliradians† | 0.84 | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `MK22` | Infantry | Milliradians† | 0.16 | 4 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `MMGL` | Infantry | Milliradians† | 20 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `MP43` | Infantry | Milliradians† | 3.08 | 28 | yes† | 0.35 | no† | 1.85 | no† | 0 … 3 | 0.6 |
| `MP9` | Infantry | Milliradians† | 2.1 | 15 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `MWSY_001_Heavy_MountedMachineGun` | Vehicle | Milliradians† | 16 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `RFB` | Infantry | Milliradians† | 0.69 | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `ROT_02_Weapon_122mm` | Vehicle | Milliradians† | 6 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `ROT_02_Weapon_30mmCannon` | Vehicle | Milliradians† | 35 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `ROT_03_AttachedMachineGuns` | Vehicle | Milliradians† | 25 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `ROT_03_Weapon_122mm` | Vehicle | Milliradians† | 6 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `ROT_04_MountedMachineGun` | Vehicle | Milliradians† | 10 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `RPG7` | Infantry | Milliradians† | 3 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `SKS` | Infantry | MinutesOfAngle | 0.73 | 5.5 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `SMG_03` | Infantry | Milliradians† | 1.3 | 17 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `SR_04` | Infantry | Milliradians† | 0.11 | 4 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `STN_01_Heavy_MountedMachineGun` | Vehicle | MinutesOfAngle | 1† | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `STN_02_Heavy_MainCannon` | Vehicle | MinutesOfAngle | 25 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `STN_03_Heavy_MainBarrel` | Vehicle | MinutesOfAngle | 50 | 360 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `STN_05_Heavy_MainBarrel` | Vehicle | MinutesOfAngle | 50 | 360 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `SV98` | Infantry | Milliradians† | 0.56 | 4 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `SVDM` | Infantry | Milliradians† | 0.45 | 10 | yes† | 0 | no† | 0 | no† | 0 … 0† | 0 |
| `TAR21` | Infantry | Milliradians† | 0.87 | 15 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `TNK_01_Artillery_Weapon` | Vehicle | Milliradians† | 10 | 90 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `TNK_01_Heavy_Weapon` | Vehicle | MinutesOfAngle | 30 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `TNK_01_MachineGun_Weapon` | Vehicle | Milliradians† | 25 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `TNK_03_Weapon` | Vehicle | Milliradians† | 1† | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `TNK_04_Weapon` | Vehicle | MinutesOfAngle | 30 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `TankBarrelTest` | Other | MinutesOfAngle | 70 | 5† | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `Vector` | Infantry | Milliradians† | 2 | 35 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_017` | Infantry | Milliradians† | 0.78 | 4 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_026` | Infantry | Milliradians† | 2 | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_027` | Infantry | MinutesOfAngle | 0.84 | 5† | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_028` | Infantry | Milliradians† | 1.16 | 20 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_029` | Infantry | Milliradians† | 0.73 | 12 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_030` | Infantry | Milliradians† | 0.58 | 16 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_031` | Infantry | Milliradians† | 1.3 | 17 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_032` | Infantry | Milliradians† | 2 | 10 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_033` | Infantry | Milliradians† | 1.5 | 15 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_034` | Infantry | Milliradians† | 0.73 | 10 | yes† | 0 | no† | 0 | no† | 0 … 0† | 0 |
| `WEPN_035` | Infantry | Milliradians† | 1.5 | 4 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_036` | Infantry | Milliradians† | 0.73 | 15 | yes† | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |
| `WEPN_037` | Infantry | Milliradians† | 0.58 | 14 | yes† | 0 | no† | 0 | no† | 0 … 0† | 0 |
| `WHL_05_RingMinigun` | Vehicle | Milliradians† | 25 | 0 | no | 0.8† | no† | 10† | no† | 0 … 0† | 0.5† |

### 1b. Stance spread (item `SpreadValues`)

Each stance names a `CT_Weapon_Spread` row and a scalar. Item attributes are the item's `DefaultAttributes` before attachments ([final values with default attachments](Wardogs_WeaponAttributes_v1.md)).

| Weapon | Item | Stand | Crouch | Prone | Spread × | Accuracy × | Trace radius |
|---|---|---|---|---|---|---|---|
| `A91` | `ID_A91` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 7 |
| `AK74M` | `ID_AK74M` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |
| `ArtilleryBarrelTest` | `ID_ArtilleryBarrelTest` | `Launcher.Stand` ×1 | `Launcher.Crouch` ×1 | `Launcher.Prone` ×1 | 1 | 1 | — |
| `CGM4` | `ID_CGM4` | `Launcher.Stand` ×1 | `Launcher.Crouch` ×1 | `Launcher.Prone` ×1 | 1 | 1 | 7 |
| `CombatBow` | `ID_CombatBow` | `Bow.Stand` ×1 | `Bow.Crouch` ×1 | `Bow.Prone` ×1 | 1 | 1 | 6 |
| `Glock17` | `ID_Glock17` | `Pistol.Stand` ×1 | `Pistol.Crouch` ×1 | `Pistol.Prone` ×1 | 1 | 1 | 3 |
| `Judge` | `ID_Judge` | `Pistol.Stand` ×1 | `Pistol.Crouch` ×1 | `Pistol.Prone` ×1 | 1 | 1 | 3 |
| `KH2002` | `ID_KH2002` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 7 |
| `LMG_02` | `ID_LMG_02` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `Launcher_04` | `ID_Launcher_04` | `Launcher.Stand` ×1 | `Launcher.Crouch` ×1 | `Launcher.Prone` ×1 | 1 | 1 | 8 |
| `M12G` | `ID_M500` | `Shotgun.Stand` ×1 | `Shotgun.Crouch` ×1 | `Shotgun.Prone` ×1 | 1 | 1 | — |
| `M249` | `ID_M249` | `LMG.Stand` ×1 | `LMG.Crouch` ×1 | `LMG.Prone` ×1 | 1 | 1 | 6 |
| `M4` | `ID_M4` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |
| `MK22` | `ID_MK22` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `MMGL` | `ID_MMGL` | `Launcher.Stand` ×1 | `Launcher.Crouch` ×1 | `Launcher.Prone` ×1 | 1 | 1 | 6 |
| `MP43` | `ID_MP43` | `Shotgun.Stand` ×1 | `Shotgun.Crouch` ×1 | `Shotgun.Prone` ×1 | 1 | 1 | 6 |
| `MP9` | `ID_MP9` | `SMG.Stand` ×1 | `SMG.Crouch` ×1 | `SMG.Prone` ×1 | 1 | 1 | 6 |
| `RFB` | `ID_RFB` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |
| `RPG7` | `ID_RPG7` | `Launcher.Stand` ×1 | `Launcher.Crouch` ×1 | `Launcher.Prone` ×1 | 1 | 1 | 7 |
| `SKS` | `ID_SKS` | `DMR.Stand` ×1 | `DMR.Crouch` ×1 | `DMR.Prone` ×1 | 1 | 1 | 6 |
| `SMG_03` | `ID_SMG_03` | `SMG.Stand` ×1 | `SMG.Crouch` ×1 | `SMG.Prone` ×1 | 1 | 1 | 6 |
| `SR_04` | `ID_SR_04` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `SV98` | `ID_SV98` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `SVDM` | `ID_SVDM` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `TAR21` | `ID_TAR21` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 7 |
| `TankBarrelTest` | `ID_TankBarrelTest` | `Launcher.Stand` ×1 | `Launcher.Crouch` ×1 | `Launcher.Prone` ×1 | 1 | 1 | — |
| `Vector` | `ID_Vector` | `SMG.Stand` ×1 | `SMG.Crouch` ×1 | `SMG.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_017` | `ID_WEPN_017` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_026` | `ID_WEPN_026` | `Pistol.Stand` ×1 | `Pistol.Crouch` ×1 | `Pistol.Prone` ×1 | 1 | 1 | 3 |
| `WEPN_027` | `ID_WEPN_027` | `Pistol.Stand` ×1 | `Pistol.Crouch` ×1 | `Pistol.Prone` ×1 | 1 | 1 | 4 |
| `WEPN_028` | `ID_WEPN_028` | `SMG.Stand` ×1 | `SMG.Crouch` ×1 | `SMG.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_029` | `ID_WEPN_029` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_030` | `ID_WEPN_030` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_031` | `ID_WEPN_031` | `SMG.Stand` ×1 | `SMG.Crouch` ×1 | `SMG.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_032` | `ID_WEPN_032` | `Pistol.Stand` ×1 | `Pistol.Crouch` ×1 | `Pistol.Prone` ×1 | 1 | 1 | 3 |
| `WEPN_033` | `ID_WEPN_033` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 7 |
| `WEPN_034` | `ID_WEPN_034` | `DMR.Stand` ×1 | `DMR.Crouch` ×1 | `DMR.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_035` | `ID_WEPN_035` | `Sniper.Stand` ×1 | `Sniper.Crouch` ×1 | `Sniper.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_036` | `ID_WEPN_036` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |
| `WEPN_037` | `ID_WEPN_037` | `AR.Stand` ×1 | `AR.Crouch` ×1 | `AR.Prone` ×1 | 1 | 1 | 6 |

### 1c. `CT_Weapon_Spread` rows

| Row | Keys (time:value) |
|---|---|
| `AR.Crouch` | 0:2 1:4 |
| `AR.Prone` | 0:1.5 1:3 |
| `AR.Stand` | 0:3 1:6 |
| `Bow.Crouch` | 0:0.5 1:1 |
| `Bow.Prone` | 0:0.5 1:0.5 |
| `Bow.Stand` | 0:1 1:2 |
| `DMR.Crouch` | 0:2 1:4 |
| `DMR.Prone` | 0:1 1:2 |
| `DMR.Stand` | 0:3 1:6 |
| `LMG.Crouch` | 0:2 1:4 |
| `LMG.Prone` | 0:1 1:2 |
| `LMG.Stand` | 0:3 1:6 |
| `Launcher.Crouch` | 0:1.5 1:3 |
| `Launcher.Prone` | 0:1 1:2 |
| `Launcher.Stand` | 0:2 1:4 |
| `MountedMachineGun` | 0:1 1:2 |
| `Pistol.Crouch` | 0:2 1:4 |
| `Pistol.Prone` | 0:1 1:2 |
| `Pistol.Stand` | 0:3 1:6 |
| `SMG.Crouch` | 0:1.5 1:3 |
| `SMG.Prone` | 0:1 1:2 |
| `SMG.Stand` | 0:2 1:4 |
| `Shotgun.Crouch` | 0:2 1:4 |
| `Shotgun.Prone` | 0:1 1:2 |
| `Shotgun.Stand` | 0:3 1:6 |
| `Sniper.Crouch` | 0:3 1:6 |
| `Sniper.Prone` | 0:2 1:4 |
| `Sniper.Stand` | 0:4 1:7 |
| `StableMountedMachineGun` | 0:0.5 1:1 |

## 2. Recoil

The recoil pattern is the per-shot (yaw, pitch) kick list; after its last shot the random yaw and pitch ranges apply. How shots become view kick is in [Weapons §5a](Wardogs_Weapons_v2.md). The `_aaabimbpohdlmnphjbidm` column is the unnamed focus drain window (+0x98).

### 2a. Scalars

| Weapon | Pitch max | Yaw min … max | After pattern: yaw | After pattern: pitch | Reset (s) | Anim offset type | Anim offset min | Anim offset max | Anim offset pattern × | Focus recoil cut % | Focus energy % / shot | Focus window (s) | Focus usage × | Focus recovery × | Focus extra zoom |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | 1† | -1 … 1† | -0.25 … 0.25 | 0.5 … 0.72 | 0.78 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `AK74M` | 45 | -22.5 … 22.5 | -0.28 … 0.28 | 0.45 … 0.75 | 0.65 | None† | -0.15 … -0.05 | 0 … 0.05 | 1 … 1† | 20 | 25 | 0.5† | 1† | 1† | 20† |
| `AT4` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `ArtilleryBarrelTest` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `BuildTool` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `CGM4` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `CombatBow` | 45 | -22.5 … 22.5 | -1 … 1† | 2 … 3 | 0.2 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 80 | 100 | 0.5† | 1† | 1† | 20† |
| `Fists` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `Glock17` | 1† | -1 … 1† | -0.5 … 0.5 | 0.5 … 1 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 10 | 40 | 0.5† | 1† | 1† | 20† |
| `GrenadeLauncher` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `Judge` | 45 | -22.5 … 22.5 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 10 | 40 | 0.5† | 1† | 1† | 20† |
| `KH2002` | 45 | -22.5 … 22.5 | -0.25 … 0.25 | 0.5 … 0.72 | 0.78 | None† | -0.2 … -0.2 | 0.2 … 0.2 | 1 … 1† | 30 | 40 | 0.5† | 1† | 1† | 20† |
| `LMG_02` | 45 | -22.5 … 22.5 | -0.62 … 0.72 | 1.1 … 1.95 | 0.9 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 50 | 10 | 0.5† | 1† | 1† | 20† |
| `Launcher_04` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `M12G` | 45 | -22.5 … 22.5 | -0.5 … 0.5 | 0.9 … 1.6 | 1 | None† | -0.35 … -0.35 | 0.35 … 0.35 | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `M249` | 45 | -22.5 … 22.5 | -0.5 … 0.5 | 0.5 … 1.5 | 0.5† | None† | -0.5 … -0.5 | 0.5 … 0.5 | 1 … 1† | 50 | 10 | 0.5† | 1† | 1† | 20† |
| `M2Browning` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `M4` | 45 | -22.5 … 22.5 | -0.26 … 0.26 | 0.4 … 0.65 | 0.55 | None† | -0.35 … -0.1 | 0.35 … 0.1 | 1 … 1† | 20 | 25 | 0.5† | 1† | 1† | 20† |
| `MK22` | 45 | -22.5 … 22.5 | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 100 | 1 | 1† | 1† | 20† |
| `MMGL` | 45 | -22.5 … 22.5 | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `MP43` | 45 | -22.5 … 22.5 | -0.45 … 0.45 | 0.8 … 1.4 | 1.2 | None† | -0.35 … -0.35 | 0.35 … 0.35 | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `MP9` | 1† | -1 … 1† | -0.3 … 0.3 | 0.3 … 0.55 | 0.55 | None† | -0.3 … -0.3 | 0.3 … 0.3 | 1 … 1† | 15 | 25 | 0.5† | 1† | 1† | 20† |
| `MWSY_001_Heavy_MountedMachineGun` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `RFB` | 45 | -22.5 … 22.5 | -0.28 … 0.34 | 0.74 … 0.98 | 1 | None† | -0.35 … -0.1 | 0.35 … 0.1 | 1 … 1† | 30 | 50 | 1 | 1† | 1† | 20† |
| `ROT_02_Weapon_122mm` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `ROT_02_Weapon_30mmCannon` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 0 | 1† | 110 |
| `ROT_03_AttachedMachineGuns` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `ROT_03_Weapon_122mm` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `ROT_04_MountedMachineGun` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 100 | 0† | 0.5† | 1† | 1† | 100 |
| `RPG7` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `SKS` | 45 | -22.5 … 22.5 | -0.28 … 0.38 | 0.55 … 0.85 | 0.95 | None† | -0.2 … -0.2 | 0.2 … 0.2 | 1 … 1† | 30 | 50 | 1 | 1† | 1† | 20† |
| `SMG_03` | 45 | -22.5 … 22.5 | -0.2 … 0.2 | 0.4 … 0.62 | 0.55 | Procedural | 1 … -1 | 0.3 … 0.3 | 1 … 1† | 30 | 50 | 0.5† | 1† | 1† | 20† |
| `SR_04` | 45 | -22.5 … 22.5 | -1 … 1† | 1 … 2.5 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 100 | 1 | 1† | 1† | 20† |
| `STN_01_Heavy_MountedMachineGun` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `STN_02_Heavy_MainCannon` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `STN_03_Heavy_MainBarrel` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `STN_05_Heavy_MainBarrel` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `SV98` | 45 | -22.5 … 22.5 | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0.2 … 0.2 | 1 … 1† | 0† | 100 | 1 | 1† | 1† | 20† |
| `SVDM` | 45 | -22.5 … 22.5 | 0.05 … 0.32 | 0.65 … 1.1 | 1.1 | Procedural | 0.2 … 0.2 | 0.5 … 0.5 | 1 … 1† | 30 | 50 | 1 | 1† | 1† | 20† |
| `TAR21` | 45 | -22.5 … 22.5 | -0.22 … 0.22 | 0.55 … 0.8 | 0.8 | None† | -0.2 … -0.2 | 0.2 … 0.2 | 1 … 1† | 30 | 40 | 0.5† | 1† | 1† | 20† |
| `TNK_01_Artillery_Weapon` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 0 | 1† | 100 |
| `TNK_01_Heavy_Weapon` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 0 | 1† | 100 |
| `TNK_01_MachineGun_Weapon` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `TNK_03_Weapon` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `TNK_04_Weapon` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 0 | 1† | 100 |
| `TankBarrelTest` | 1† | -1 … 1† | -1 … 1† | 1 … 2† | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 20† |
| `Vector` | 45 | -22.5 … 22.5 | -0.05 … 0.05 | -0.08 … 0.12 | 0.48 | None† | -0.3 … -0.3 | 0.3 … 0.3 | 1 … 1† | 15 | 25 | 0.5† | 1† | 1† | 20† |
| `WEPN_017` | 45 | -22.5 … 22.5 | -1 … 1† | 2 … 3 | 0.2 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 100 | 1 | 1† | 1† | 20† |
| `WEPN_026` | 45 | -22.5 … 22.5 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | None† | -0.3 … -0.3 | 0.3 … 0.3 | 1 … 1† | 10 | 40 | 0.5† | 1† | 1† | 20† |
| `WEPN_027` | 45 | -22.5 … 22.5 | 0.25 … 1 | 0.25 … 1 | 0.5† | None† | -0.35 … -0.1 | 0.35 … 0.1 | 1 … 1† | 10 | 40 | 0.5† | 1† | 1† | 20† |
| `WEPN_028` | 45 | -22.5 … 22.5 | -0.32 … 0.32 | 0.35 … 0.58 | 0.5† | None† | -0.3 … -0.3 | 0.3 … 0.3 | 1 … 1† | 15 | 25 | 0.5† | 1† | 1† | 20† |
| `WEPN_029` | 45 | -22.5 … 22.5 | -0.3 … 0.3 | 0.5 … 0.78 | 0.8 | None† | -0.15 … -0.05 | 0 … 0.05 | 1 … 1† | 20 | 25 | 0.5† | 1† | 1† | 20† |
| `WEPN_030` | 45 | -22.5 … 22.5 | -0.35 … 0.35 | 0.7 … 1.1 | 0.7 | None† | -0.35 … -0.1 | 0.35 … 0.1 | 1 … 1† | 20 | 25 | 0.5† | 1† | 1† | 20† |
| `WEPN_031` | 45 | -22.5 … 22.5 | -0.2 … 0.2 | 0.4 … 0.62 | 0.6 | Procedural | 1 … -1 | 0.3 … 0.3 | 1 … 1† | 30 | 50 | 0.5† | 1† | 1† | 20† |
| `WEPN_032` | 45 | -22.5 … 22.5 | -0.5 … 0.5 | 0.5 … 1 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 10 | 40 | 0.5† | 1† | 1† | 20† |
| `WEPN_033` | 45 | -22.5 … 22.5 | -0.25 … 0.25 | 0.5 … 0.72 | 0.78 | None† | -0.2 … -0.2 | 0.2 … 0.2 | 1 … 1† | 30 | 40 | 0.5† | 1† | 1† | 20† |
| `WEPN_034` | 45 | -22.5 … 22.5 | 0.05 … 0.32 | 0.65 … 1.1 | 1.1 | None† | 0.2 … 0.2 | 0.5 … 0.5 | 1 … 1† | 30 | 50 | 1 | 1† | 1† | 20† |
| `WEPN_035` | 45 | -22.5 … 22.5 | -1 … 1† | 1 … 2† | 0.5† | None† | -0.35 … -0.1 | 0.35 … 0.1 | 1 … 1† | 0† | 100 | 0.001 | 1† | 1† | 20† |
| `WEPN_036` | 45 | -22.5 … 22.5 | -0.22 … 0.22 | 1.35 … 1.7 | 0.75 | None† | 0 … 0† | 0 … 0† | 1 … 1† | 50 | 10 | 0.5† | 1† | 1† | 20† |
| `WEPN_037` | 45 | -22.5 … 22.5 | -0.34 … 0.34 | 0.62 … 0.95 | 0.5† | None† | 0.2 … 0.2 | 0.5 … 0.5 | 1 … 1† | 30 | 50 | 1 | 1† | 1† | 20† |
| `WHL_05_RingMinigun` | 1† | -1 … 1† | 0 … 0 | 0 … 0 | 0.5† | None† | 0 … 0† | 0 … 0† | 1 … 1† | 0† | 0† | 0.5† | 1† | 1† | 100 |

### 2b. Item recoil attributes and stance effects

| Weapon | Vertical recoil × | Horizontal recoil × | Stand effect | Crouch effect | Prone effect |
|---|---|---|---|---|---|
| `A91` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Prone` | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Standing` |
| `AK74M` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `ArtilleryBarrelTest` | 1 | 1 | — | — | — |
| `CGM4` | 1 | 1 | — | — | — |
| `CombatBow` | 1 | 1 | `GE_Weapon_StanceRecoil_SR_Standing` | `GE_Weapon_StanceRecoil_SR_Crouch` | `GE_Weapon_StanceRecoil_SR_Prone` |
| `Glock17` | 1 | 1 | `GE_Weapon_StanceRecoil_Pistol_Standing` | `GE_Weapon_StanceRecoil_Pistol_Crouch` | `GE_Weapon_StanceRecoil_Pistol_Prone` |
| `Judge` | 1 | 1 | — | — | — |
| `KH2002` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `LMG_02` | 1 | 1 | `GE_Weapon_StanceRecoil_LMG_Standing` | `GE_Weapon_StanceRecoil_LMG_Crouch` | `GE_Weapon_StanceRecoil_LMG_Prone` |
| `Launcher_04` | 1 | 1 | — | — | — |
| `M12G` | 1 | 1 | `GE_Weapon_StanceRecoil_Shotgun_Standing` | `GE_Weapon_StanceRecoil_Shotgun_Crouch` | `GE_Weapon_StanceRecoil_Shotgun_Prone` |
| `M249` | 1 | 1 | `GE_Weapon_StanceRecoil_LMG_Standing` | `GE_Weapon_StanceRecoil_LMG_Crouch` | `GE_Weapon_StanceRecoil_LMG_Prone` |
| `M4` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `MK22` | 1 | 1 | `GE_Weapon_StanceRecoil_SR_Standing` | `GE_Weapon_StanceRecoil_SR_Crouch` | `GE_Weapon_StanceRecoil_SR_Prone` |
| `MMGL` | 1 | 1 | — | — | — |
| `MP43` | 1 | 1 | `GE_Weapon_StanceRecoil_Shotgun_Standing` | `GE_Weapon_StanceRecoil_Shotgun_Crouch` | `GE_Weapon_StanceRecoil_Shotgun_Prone` |
| `MP9` | 1 | 1 | `GE_Weapon_StanceRecoil_SMG_Standing` | `GE_Weapon_StanceRecoil_SMG_Crouch` | `GE_Weapon_StanceRecoil_SMG_Prone` |
| `RFB` | 1 | 1 | `GE_Weapon_StanceRecoil_DMR_Standing` | `GE_Weapon_StanceRecoil_DMR_Crouch` | `GE_Weapon_StanceRecoil_DMR_Prone` |
| `RPG7` | 1 | 1 | — | — | — |
| `SKS` | 1 | 1 | `GE_Weapon_StanceRecoil_DMR_Standing` | `GE_Weapon_StanceRecoil_DMR_Crouch` | `GE_Weapon_StanceRecoil_DMR_Prone` |
| `SMG_03` | 1 | 1 | `GE_Weapon_StanceRecoil_SMG_Standing` | `GE_Weapon_StanceRecoil_SMG_Crouch` | `GE_Weapon_StanceRecoil_SMG_Prone` |
| `SR_04` | 1 | 1 | `GE_Weapon_StanceRecoil_SR_Standing` | `GE_Weapon_StanceRecoil_SR_Crouch` | `GE_Weapon_StanceRecoil_SR_Prone` |
| `SV98` | 1 | 1 | `GE_Weapon_StanceRecoil_SR_Standing` | `GE_Weapon_StanceRecoil_SR_Crouch` | `GE_Weapon_StanceRecoil_SR_Prone` |
| `SVDM` | 1 | 1 | `GE_Weapon_StanceRecoil_DMR_Standing` | `GE_Weapon_StanceRecoil_DMR_Crouch` | `GE_Weapon_StanceRecoil_DMR_Prone` |
| `TAR21` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `TankBarrelTest` | 1 | 1 | — | — | — |
| `Vector` | 1 | 1 | `GE_Weapon_StanceRecoil_SMG_Standing` | `GE_Weapon_StanceRecoil_SMG_Crouch` | `GE_Weapon_StanceRecoil_SMG_Prone` |
| `WEPN_017` | 1 | 1 | `GE_Weapon_StanceRecoil_SR_Standing` | `GE_Weapon_StanceRecoil_SR_Crouch` | `GE_Weapon_StanceRecoil_SR_Prone` |
| `WEPN_026` | 1 | 1 | `GE_Weapon_StanceRecoil_Pistol_Standing` | `GE_Weapon_StanceRecoil_Pistol_Crouch` | `GE_Weapon_StanceRecoil_Pistol_Prone` |
| `WEPN_027` | 1 | 1 | `GE_Weapon_StanceRecoil_Pistol_Standing` | `GE_Weapon_StanceRecoil_Pistol_Crouch` | `GE_Weapon_StanceRecoil_Pistol_Prone` |
| `WEPN_028` | 1 | 1 | `GE_Weapon_StanceRecoil_SMG_Standing` | `GE_Weapon_StanceRecoil_SMG_Crouch` | `GE_Weapon_StanceRecoil_SMG_Prone` |
| `WEPN_029` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `WEPN_030` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `WEPN_031` | 1 | 1 | `GE_Weapon_StanceRecoil_SMG_Standing` | `GE_Weapon_StanceRecoil_SMG_Crouch` | `GE_Weapon_StanceRecoil_SMG_Prone` |
| `WEPN_032` | 1 | 1 | `GE_Weapon_StanceRecoil_Pistol_Standing` | `GE_Weapon_StanceRecoil_Pistol_Crouch` | `GE_Weapon_StanceRecoil_Pistol_Prone` |
| `WEPN_033` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `WEPN_034` | 1 | 1 | `GE_Weapon_StanceRecoil_DMR_Standing` | `GE_Weapon_StanceRecoil_DMR_Crouch` | `GE_Weapon_StanceRecoil_DMR_Prone` |
| `WEPN_035` | 1 | 1 | `GE_Weapon_StanceRecoil_SR_Standing` | `GE_Weapon_StanceRecoil_SR_Crouch` | `GE_Weapon_StanceRecoil_SR_Prone` |
| `WEPN_036` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Prone` |
| `WEPN_037` | 1 | 1 | `GE_Weapon_StanceRecoil_AR_Standing` | `GE_Weapon_StanceRecoil_AR_Crouch` | `GE_Weapon_StanceRecoil_AR_Standing` |

The stance effects multiply both recoil attributes (compound): Standing 1.0 for every archetype; Crouch 0.85 (AR, DMR, SMG, SR, Pistol, Shotgun) or 0.6 (LMG); Prone 0.7 (AR, DMR, SMG, SR, Pistol, Shotgun) or 0.35 vertical and 0.25 horizontal (LMG). Values are from [`weapon-loadouts.json`](../assets/data/weapon-loadouts.json).

### 2c. Recoil patterns, every shot

Each cell is `yaw,pitch` of that shot. Weapons without a pattern use only the after-pattern ranges.

| Weapon | Shots | Pattern (yaw,pitch per shot) |
|---|---|---|
| `A91` | 30 | 0,0.85; 0.03,1.02; 0.055,1.15; 0.075,1.24; 0.09,1.28; 0.095,1.3; 0.092,1.3; 0.085,1.285; 0.075,1.265; 0.065,1.245; 0.055,1.23; 0.045,1.215; 0.035,1.2; 0.025,1.19; -0.015,1.18; -0.04,1.17; -0.058,1.16; -0.065,1.155; -0.06,1.15; -0.048,1.145; -0.03,1.14; -0.012,1.13; 0.018,1.12; 0.038,1.115; 0.052,1.11; 0.058,1.105; 0.052,1.1; 0.04,1.05; 0.025,1.02; 0.01,1 |
| `AK74M` | 30 | 0.01,0.717554; -0.02,0.936807; 0.025,1.07633; 0.045,1.14609; 0.07,1.21585; 0.085,1.24575; 0.08,1.22582; 0.07,1.19592; 0.06,1.17599; 0.055,1.15606; 0.045,1.14609; 0.04,1.13613; 0.03,1.12616; 0.025,1.1162; -0.03,1.09626; -0.055,1.09626; -0.065,1.0863; -0.06,1.07633; -0.05,1.0863; -0.04,1.07633; -0.03,1.06637; -0.02,1.06637; 0.015,1.0564; 0.035,1.0564; 0.055,1.04643; 0.065,1.03647; 0.06,1.0265; 0.05,1.01653; 0.04,1.00657; 0.03,0.946772 |
| `Judge` | 1 | 0.09,2.24775 |
| `KH2002` | 30 | 0,0.85; 0.03,1.02; 0.055,1.15; 0.075,1.24; 0.09,1.28; 0.095,1.3; 0.092,1.3; 0.085,1.285; 0.075,1.265; 0.065,1.245; 0.055,1.23; 0.045,1.215; 0.035,1.2; 0.025,1.19; -0.015,1.18; -0.04,1.17; -0.058,1.16; -0.065,1.155; -0.06,1.15; -0.048,1.145; -0.03,1.14; -0.012,1.13; 0.018,1.12; 0.038,1.115; 0.052,1.11; 0.058,1.105; 0.052,1.1; 0.04,1.05; 0.025,1.02; 0.01,1 |
| `LMG_02` | 30 | 0.13,1.68; 0.21,2.072; 0.285,2.352; 0.342,2.52; 0.374,2.576; 0.39,2.59; 0.387,2.59; 0.37,2.576; 0.342,2.548; 0.305,2.52; 0.263,2.492; 0.219,2.464; 0.17,2.436; 0.117,2.408; 0.062,2.38; -0.089,2.352; -0.179,2.324; -0.241,2.296; -0.268,2.268; -0.257,2.24; -0.219,2.212; -0.159,2.184; -0.078,2.156; 0.159,2.114; 0.3,2.072; 0.403,2.03; 0.463,1.988; 0.479,1.946; 0.451,1.904; 0.393,1.82 |
| `M12G` | 7 | 0.11,1.8; 0.18,2; -0.28,2.2; -0.38,2.1; -0.32,2; 0.15,1.9; 0.26,1.8 |
| `M249` | 7 | 1.10714,2.40603; -0.308035,1.66072; -0.987682,0.876429; -0.547855,1.83821; 0.504108,1.50071; -0.204642,2.85286; -1.09301,2.0028 |
| `M2Browning` | 29 | 0,0.918003; -0.0333333,0.8; 0.0333333,0.8; 0.0666667,0.88; 0.2,0.72; 0.233333,1.12; 0.1,1.2; -0.2,0.88; -0.5,0.64; -0.3,0.48; -0.266667,0.64; 0.166667,0.4; -0.133333,0.56; -0.2,0.64; -0.0666667,1.36; 0,0.88; 0.233333,0.16; 0.0666667,0.72; -0.0666667,0.72; 0.266667,0.64; 0.2,1.2; 0.233333,0.88; 0.233333,0.88; 0.0666667,0.8; -0.0333333,1.04; -0.2,0.56; 0.0333333,0.72; 0,1.2; -0.0333333,0.96 |
| `M4` | 30 | 0.037,0.693; -0.007,0.891; -0.079,1.0395; -0.122,1.089; -0.137,1.1385; -0.107,1.1682; -0.065,1.1385; -0.007,1.1088; 0.023,1.089; 0.022,1.0692; 0.007,1.0494; -0.035,1.0296; -0.108,1.0494; -0.122,1.0395; -0.122,1.0197; -0.093,0.9999; -0.065,1.0098; -0.021,0.99; 0.008,0.9702; 0.022,0.9504; 0.008,0.9405; -0.007,0.9504; -0.065,0.9603; -0.107,0.9504; -0.122,0.9405; -0.108,0.9306; -0.093,0.9207; -0.065,0.9108; -0.007,0.9009; 0.008,0.891 |
| `MP43` | 2 | 0.840004,1.71; 0.45,1.93 |
| `MP9` | 30 | 0.01815,0.6292; 0.03025,0.8712; 0.0363,0.8349; 0.03388,0.8591; 0.02662,0.8712; 0.01815,0.8712; 0.00968,0.86515; -0.00605,0.847; -0.11495,0.8228; -0.1694,0.79255; -0.1936,0.76835; -0.18755,0.7502; -0.16335,0.74415; -0.12705,0.74778; -0.07865,0.75262; 0.06655,0.76835; 0.1331,0.78045; 0.17545,0.78408; 0.18755,0.78045; 0.17908,0.77198; 0.1573,0.7623; 0.12705,0.75262; 0.11495,0.74778; 0.12705,0.74052; 0.14278,0.73205; 0.14762,0.71995; 0.14278,0.70422; 0.13068,0.68728; 0.11132,0.67155; 0.0847,0.5808 |
| `RFB` | 20 | 0.15,2.34; 0.35,2.79; 0.55,3.06; 0.7,3.105; 0.4,3.06; -0.45,2.61; -0.6,2.52; 0.3,2.835; 0.65,2.79; 0.8,2.745; 0.55,2.7; 0.2,2.655; -0.5,2.34; -0.35,2.43; 0.25,2.565; 0.6,2.52; 0.7,2.475; 0.45,2.43; 0.1,2.385; -0.2,2.25 |
| `ROT_03_AttachedMachineGuns` | 7 | 1.10714,2.40603; -0.308035,1.66071; -0.987682,0.876429; -0.547855,1.83821; 0.504108,1.50071; -0.204642,2.85286; -1.09301,2.0028 |
| `ROT_04_MountedMachineGun` | 7 | 1.107,2.4; -0.3,1.66; -0.98,0.87; -0.547,1.83; 0.5,1.5; -0.2,2.85; -1.09,2 |
| `SKS` | 20 | -0.025538,2.375; -0.034409,3.2; -0.437593,3.55; -1.28713,3.625; -0.377998,3.6; -1.19706,3.55; -2.39873,3.5; -1.42649,3.45; 0.613115,3.4; -0.809759,3.3625; -1.49713,3.325; -0.918821,3.3; -0.407489,3.3; -0.689072,3.25; -0.382609,3.2; -0.786865,3.15; -0.203181,3.1; 0.010702,3; -0.564315,2.9; -0.495283,2.625 |
| `SMG_03` | 30 | 0.033,1.08994; 0.077,1.18903; 0.099,1.24848; 0.1155,1.28811; 0.11,1.27821; 0.0935,1.2683; 0.066,1.25344; 0.033,1.23857; -0.0605,1.22866; -0.121,1.2138; -0.165,1.19894; -0.1815,1.18407; -0.1705,1.16921; -0.1375,1.15435; -0.0935,1.13949; -0.033,1.12463; 0.0638,1.10976; 0.121,1.0949; 0.154,1.08004; 0.1595,1.06517; 0.1452,1.05031; 0.11,1.03544; 0.0638,1.02058; 0.0165,1.00572; -0.0462,0.988876; -0.0858,0.971042; -0.0968,0.949242; -0.0682,0.926452; -0.0275,0.896727; 0.033,0.86261 |
| `SVDM` | 9 | -0.283,3.683; 0.63,3.643; 0.126,2.538; -1.385,3.601; -0.378,2.864; -1.259,1.76; 0.944,2.374; -0.913,2.005; -0.976,2.168 |
| `TAR21` | 30 | 0,0.7; 0.06,0.93; -0.075,1.08; -0.16,1.035; -0.225,1.17; -0.255,1.22; -0.23,1.255; -0.16,1.205; 0.01,1.29; 0.13,1.33; 0.185,1.285; 0.195,1.365; 0.16,1.405; 0.075,1.435; -0.075,1.39; -0.165,1.47; -0.215,1.505; -0.23,1.46; -0.195,1.54; -0.115,1.575; 0.02,1.605; 0.115,1.56; 0.17,1.635; 0.18,1.67; 0.145,1.625; 0.06,1.7; -0.07,1.73; -0.15,1.69; -0.19,1.755; -0.175,1.785 |
| `Vector` | 55 | 0.09,0.267748; 0.18,0.27; 0,0.36; 0,0; -0.18,-0.27; 0,0.18; -0.27,0.09; 0,0; -0.18,-0.09; 0.18,-0.36; -0.18,0.09; 0,0.27; -0.27,0.36; 0,-0.18; 0,0; 0,0; 0.18,0; 0,0; 0.09,0.09; 0,0; 0.09,0; 0.09,0; 0.09,0; 0,0; 0,0; 0.09,0; 0,0; 0,0; 0,0; 0,0; 0,0; 0,0.18; 0,0; -0.09,0; -0.18,0; 0,0; 0,0; 0,-0.09; 0,0; 0,0; 0,0; 0.18,0; 0.09,0; 0,0; 0,0; 0,0.09; 0,0; 0.27,0; 0,0; -0.09,0.09; 0,0; -0.18,0; -0.09,0; -0.09,0; -0.09,0.18 |
| `WEPN_027` | 15 | 0,1.16775; -0.09,1.17; -0.09,1.35; 0.36,0.99; -0.18,1.35; -0.18,1.53; 0,1.44; 0.18,1.08; 0.09,1.8; -0.27,1.17; -0.18,1.62; 0.36,1.17; 0.09,1.26; -0.09,1.44; -0.18,0.99 |
| `WEPN_028` | 30 | -0.088829,0.7161; -0.205342,0.8778; -0.283395,0.924; 0.156968,0.924; 0.049187,0.92169; -0.596899,0.91476; -0.612739,0.89859; -0.331502,0.88011; -0.079796,0.860475; -0.531679,0.84084; 0.419242,0.825825; -0.386867,0.814275; -0.040806,0.80388; 0.096261,0.79464; 0.295631,0.78771; 0.289858,0.78309; -0.327794,0.77616; -0.285228,0.77154; -0.650047,0.768075; 0.322267,0.76461; -0.564585,0.7623; -0.395291,0.75999; -0.682746,0.75768; 0.203505,0.75537; 0.290153,0.74844; 0.015301,0.73689; -0.171771,0.721875; -0.263335,0.70686; -0.151014,0.69069; -0.064259,0.6699 |
| `WEPN_029` | 30 | -0.01,0.3969; -0.035,0.5859; -0.06,0.7749; -0.075,0.9639; -0.07,1.1151; -0.055,1.2285; -0.03,1.2663; 0,1.27575; 0.03,1.25685; 0.05,1.20015; 0.06,1.1718; 0.06,1.16235; 0.05,1.15762; 0.035,1.1529; 0.015,1.14817; -0.01,1.134; -0.03,1.1151; -0.045,1.0962; -0.05,1.0773; -0.04,1.0584; -0.025,1.0395; -0.005,1.0206; 0.02,1.01115; 0.04,1.0017; 0.055,0.99225; 0.065,0.97335; 0.07,0.95445; 0.07,0.945; 0.07,0.91665; 0.072,0.89775 |
| `WEPN_030` | 20 | 0.055,1.09725; 0.095,1.3794; 0.13,1.5884; 0.155,1.6929; 0.165,1.72425; 0.16,1.7138; 0.148,1.6929; 0.132,1.672; 0.115,1.6511; 0.095,1.6302; -0.04,1.59885; -0.085,1.57795; -0.11,1.55705; -0.105,1.53615; -0.085,1.5257; -0.055,1.51525; 0.07,1.4839; 0.105,1.4421; 0.095,1.41075; 0.07,1.3585 |
| `WEPN_031` | 30 | 0.0345,1.13949; 0.0805,1.24307; 0.1035,1.30523; 0.12075,1.34667; 0.115,1.33631; 0.09775,1.32595; 0.069,1.31041; 0.0345,1.29487; -0.06325,1.28451; -0.1265,1.26897; -0.1725,1.25344; -0.18975,1.2379; -0.17825,1.22236; -0.14375,1.20682; -0.09775,1.19128; -0.0345,1.17575; 0.0667,1.1602; 0.1265,1.14467; 0.161,1.12913; 0.16675,1.11359; 0.1518,1.09805; 0.115,1.08251; 0.0667,1.06697; 0.01725,1.05144; -0.0483,1.03382; -0.0897,1.01518; -0.1012,0.992389; -0.0713,0.968563; -0.02875,0.937487; 0.0345,0.90182 |
| `WEPN_032` | 50 | 0.0360022,1.53; -0.00699829,1.628; -0.169003,1.831; 0.0679999,2.139; 0.365999,1.65; -0.123003,1.264; 0.00399902,1.43; 0.117999,1.787; 0.167003,1.075; 0.0650006,1.542; -0.0630011,1.21; 0.154001,1.786; 0.170002,1.92; -0.269,1.793; -0.197001,1.763; 0.09,2.19; 0.326997,0.912997; 0.396002,1.531; 0.558001,1.524; 0.373997,1.432; 0.0719989,1.344; -0.205999,1.26; -0.375002,1.18; -0.322998,1.103; -0.0549976,1.028; 0.260002,0.954998; 0.491001,0.885004; 0.519,0.815999; 0.355001,0.749004; 0.0440002,0.682998; -0.236997,0.619003; -0.407999,0.555996; -0.358,0.495; -0.0830017,0.436003; 0.235997,0.379001; -0.0909998,0.323998; -0.230999,0.27; -0.0959985,0.217002; 0.240002,0.167003; 0.583001,0.117999; 0.728998,0.0709991; 0.589999,0.0259991; 0.243001,-0.0180011; -0.111,-0.0599963; -0.261002,-0.0999976; -0.114999,-0.138999; 0.245001,-0.176001; 0.609999,-0.212003; 0.764,-0.247; 0.850001,-0.290001 |
| `WEPN_033` | 30 | 0,0.85; 0.03,1.02; 0.055,1.15; 0.075,1.24; 0.09,1.28; 0.095,1.3; 0.092,1.3; 0.085,1.285; 0.075,1.265; 0.065,1.245; 0.055,1.23; 0.045,1.215; 0.035,1.2; 0.025,1.19; -0.015,1.18; -0.04,1.17; -0.058,1.16; -0.065,1.155; -0.06,1.15; -0.048,1.145; -0.03,1.14; -0.012,1.13; 0.018,1.12; 0.038,1.115; 0.052,1.11; 0.058,1.105; 0.052,1.1; 0.04,1.05; 0.025,1.02; 0.01,1 |
| `WEPN_034` | 32 | 0,3.06; 0.18,3.06; 0.27,3.06; 0.36,3.06; 0.45,3.06; 0.36,3.06; 0.54,3.24; 0.45,3.24; 0.27,3.24; 0.09,3.24; -0.09,3.24; -0.18,3.24; 0,3.42; -0.27,3.42; -0.36,3.42; -0.45,3.42; -0.36,3.42; -0.54,3.42; -0.63,3.6; -0.45,3.6; -0.54,3.6; -0.36,3.6; -0.18,3.6; 0.09,3.6; 0.27,3.78; 0.36,3.78; 0.45,3.78; 0.27,3.78; 0.36,3.78; 0.18,3.96; 0.27,3.96; 0.09,3.96 |
| `WEPN_036` | 40 | 0,2.5306; 0.098389,2.93994; 0.224784,3.1784; 0.235984,3.59678; 0.146393,3.52415; 0.013606,3.52999; -0.075985,2.74674; -0.064782,2.78259; 0.061612,2.72472; 0.259999,3.43004; 0.458389,3.34806; 0.584783,3.35481; 0.493652,2.61465; 0.301727,2.64605; 0.066606,2.59361; -0.125318,3.28617; -0.21645,3.20453; -0.192389,3.21148; -0.096333,2.48196; -0.000278,2.51648; 0.023783,2.46081; -0.067348,3.13825; -0.259273,3.05935; -0.494394,3.07025; -0.545885,2.35213; -0.496583,2.39048; -0.332089,2.33633; -0.0956,3.00039; 0.140889,2.92247; 0.305383,2.92893; 0.354685,2.22971; 0.303194,2.26333; 0.208506,2.21015; 0.157015,2.86436; 0.082384,2.78426; 0.122944,2.79547; 0.2355,2.11071; 0.348056,2.13956; 0.388616,2.06892; 0.313985,2.66662 |
| `WEPN_037` | 30 | 0.0154,1.07484; -0.0231,1.40287; 0.0308,1.60652; 0.0616,1.71965; 0.08855,1.75353; 0.1078,1.73103; 0.1232,1.69703; 0.11935,1.66315; 0.11165,1.64052; 0.1001,1.61789; 0.08085,1.59514; 0.0539,1.58389; 0.01925,1.56126; -0.0231,1.55001; -0.0616,1.53864; -0.0924,1.52738; -0.11935,1.51601; -0.13475,1.50476; -0.1463,1.49338; -0.14245,1.48201; -0.12705,1.48201; -0.1001,1.47076; -0.06545,1.47076; -0.0231,1.4595; 0.0154,1.4595; 0.0462,1.44813; 0.0693,1.43675; 0.077,1.43675; 0.06545,1.4255; 0.0462,1.41425 |
| `WHL_05_RingMinigun` | 7 | 1.10714,2.40603; -0.308035,1.66071; -0.987682,0.876429; -0.547855,1.83821; 0.504108,1.50071; -0.204642,2.85286; -1.09301,2.0028 |

## 3. Camera kick

### 3a. Scalars

| Weapon | View kick × | FOV shift type | FOV shift delta | FOV shift duration (s) | FOV interp speed | Iron-sights aim time (s) | Iron-sights FOV × |
|---|---|---|---|---|---|---|---|
| `A91` | 1† | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `AK74M` | 1.1 | Curve | -2.5† | 0.25† | 20† | 0.8 | 1.2† |
| `AT4` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `ArtilleryBarrelTest` | 1† | None† | -2.5† | 0.25† | 20† | 12 | 1.2† |
| `BuildTool` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `CGM4` | 1† | Constant | -3 | 0.4 | 20† | 50000 | 1.2† |
| `CombatBow` | 0 | Curve | -2.5† | 0.35 | 20† | 0.2† | 1.2† |
| `Fists` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `Glock17` | 1.5 | Curve | -2.5† | 0.15 | 20† | 0.08 | 1.2† |
| `GrenadeLauncher` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `Judge` | 1† | Curve | -2.5† | 0.15 | 20† | 0.2† | 1.2† |
| `KH2002` | 1† | Curve | -1.5 | 0.25† | 20† | 0.2† | 1.2† |
| `LMG_02` | 1.25 | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `Launcher_04` | 1† | None† | -2.5† | 0.25† | 20† | 50000 | 1.2† |
| `M12G` | 1.6 | Curve | -2.5† | 0.35 | 20† | 0.2† | 1.2† |
| `M249` | 1.2 | Curve | -2.5† | 0.25† | 20† | 5 | 1.2† |
| `M2Browning` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `M4` | 1.08 | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `MK22` | 1.4 | Curve | -2.5† | 0.5 | 20† | 0.2† | 1.2† |
| `MMGL` | 1† | Constant | -3 | 0.35 | 20† | 0.2† | 1.2† |
| `MP43` | 1.15 | Curve | -2.5† | 0.35 | 20† | 0.2† | 1 |
| `MP9` | 1.1 | Curve | -2.5† | 0.2 | 20† | 0.2† | 1.2† |
| `MWSY_001_Heavy_MountedMachineGun` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `RFB` | 1† | Curve | -2.5† | 0.3 | 20† | 0.2† | 1.2† |
| `ROT_02_Weapon_122mm` | 1† | None† | -2.5† | 0.25† | 20† | 0.45 | 1.2† |
| `ROT_02_Weapon_30mmCannon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `ROT_03_AttachedMachineGuns` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `ROT_03_Weapon_122mm` | 1† | None† | -2.5† | 0.25† | 20† | 0.45 | 1.2† |
| `ROT_04_MountedMachineGun` | 1† | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `RPG7` | 1† | Constant | -3 | 0.4 | 20† | 50000 | 1.2† |
| `SKS` | 1† | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `SMG_03` | 1† | Curve | -2.5† | 0.2 | 20† | 0.2† | 1.2† |
| `SR_04` | 1.45 | Curve | -2.5† | 0.45 | 20† | 0.2† | 1.2† |
| `STN_01_Heavy_MountedMachineGun` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `STN_02_Heavy_MainCannon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `STN_03_Heavy_MainBarrel` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `STN_05_Heavy_MainBarrel` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `SV98` | 1.3 | Curve | -2.5† | 0.5 | 20† | 0.2† | 1.2† |
| `SVDM` | 1† | Curve | -2.5† | 0.35 | 20† | 0.2† | 1.2† |
| `TAR21` | 1.1 | Curve | -1.5 | 0.25† | 20† | 0.2† | 1.2† |
| `TNK_01_Artillery_Weapon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `TNK_01_Heavy_Weapon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `TNK_01_MachineGun_Weapon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `TNK_03_Weapon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `TNK_04_Weapon` | 1† | None† | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `TankBarrelTest` | 1† | None† | -2.5† | 0.25† | 20† | 50000 | 1.2† |
| `Vector` | 1† | Curve | -2.5† | 0.2 | 20† | 0.2† | 1.2† |
| `WEPN_017` | 0.8 | Curve | -2.5† | 0.35 | 20† | 0.2† | 1.2† |
| `WEPN_026` | 1.85 | Curve | -2.5† | 0.2 | 20† | 0.2† | 1.2† |
| `WEPN_027` | 1† | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `WEPN_028` | 1.15 | Curve | -2.5† | 0.2 | 20† | 0.2† | 1.2† |
| `WEPN_029` | 0.95 | Curve | -2.5† | 0.25† | 20† | 0.8 | 1.2† |
| `WEPN_030` | 1† | Curve | -2.5† | 0.3 | 20† | 0.2† | 1.2† |
| `WEPN_031` | 1† | Curve | -2.5† | 0.2 | 20† | 0.2† | 1.2† |
| `WEPN_032` | 1† | Curve | -2.5† | 0.15 | 20† | 0.08 | 1.2† |
| `WEPN_033` | 1† | Curve | -1.5 | 0.25† | 20† | 0.2† | 1.2† |
| `WEPN_034` | 1† | Curve | -2.5† | 0.35 | 20† | 0.2† | 1.2† |
| `WEPN_035` | 0.3 | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `WEPN_036` | 1† | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |
| `WEPN_037` | 0.9 | Curve | -2.5† | 0.3 | 20† | 0.2† | 1.2† |
| `WHL_05_RingMinigun` | 1† | Curve | -2.5† | 0.25† | 20† | 0.2† | 1.2† |

### 3b. Curves per weapon

| Weapon | `AdsCameraCurve` | `ViewKickCurve` | `RecoveryKickCurve` | `FOVShiftingCurve` |
|---|---|---|---|---|
| `A91` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#1` |
| `AK74M` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#2` | `RecoveryKickCurve#1` | `FOVShiftingCurve#1` |
| `AT4` | none† | none† | none† | none† |
| `ArtilleryBarrelTest` | none† | none† | none† | none† |
| `BuildTool` | none† | none† | none† | none† |
| `CGM4` | `CF_Launcher_ADS_Curve` | none† | none† | none† |
| `CombatBow` | `CF_SniperRifles_ADS_Curve` | `ViewKickCurve#3` | `RecoveryKickCurve#1` | `FOVShiftingCurve#2` |
| `Fists` | none† | `ViewKickCurve#1` | `RecoveryKickCurve#2` | none† |
| `Glock17` | `CF_Pistol_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#3` |
| `GrenadeLauncher` | none† | `ViewKickCurve#4` | `RecoveryKickCurve#3` | none† |
| `Judge` | `CF_Pistol_ADS_Curve (variant 4)` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#4` |
| `KH2002` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#1` |
| `LMG_02` | `CF_LMG_ADS_Curve` | `ViewKickCurve#5` | `RecoveryKickCurve#1` | `FOVShiftingCurve#5` |
| `Launcher_04` | `CF_Launcher_ADS_Curve` | `ViewKickCurve#6` | `RecoveryKickCurve#4` | none† |
| `M12G` | `CF_Shotgun_ADS_Curve` | `ViewKickCurve#7` | `RecoveryKickCurve#5` | `FOVShiftingCurve#6` |
| `M249` | `CF_LMG_ADS_Curve` | `ViewKickCurve#5` | `RecoveryKickCurve#1` | `FOVShiftingCurve#5` |
| `M2Browning` | none† | `ViewKickCurve#1` | `RecoveryKickCurve#6` | none† |
| `M4` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#7` |
| `MK22` | `CF_SniperRifles_ADS_Curve (variant 7)` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#8` |
| `MMGL` | `CF_Launcher_ADS_Curve` | `ViewKickCurve#4` | `RecoveryKickCurve#1` | none† |
| `MP43` | `CF_Shotgun_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#7` | `FOVShiftingCurve#6` |
| `MP9` | `CF_SMG_ADS_Curve` | `ViewKickCurve#8` | `RecoveryKickCurve#1` | `FOVShiftingCurve#9` |
| `MWSY_001_Heavy_MountedMachineGun` | `AdsCameraCurve#1` | none† | none† | none† |
| `RFB` | `CF_DMR_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#10` |
| `ROT_02_Weapon_122mm` | none† | none† | none† | none† |
| `ROT_02_Weapon_30mmCannon` | none† | none† | none† | none† |
| `ROT_03_AttachedMachineGuns` | none† | none† | none† | none† |
| `ROT_03_Weapon_122mm` | none† | none† | none† | none† |
| `ROT_04_MountedMachineGun` | none† | none† | none† | `FOVShiftingCurve#5` |
| `RPG7` | `CF_Launcher_ADS_Curve` | `ViewKickCurve#6` | `RecoveryKickCurve#4` | none† |
| `SKS` | `CF_DMR_ADS_Curve (variant 11)` | `ViewKickCurve#9` | `RecoveryKickCurve#1` | `FOVShiftingCurve#11` |
| `SMG_03` | `CF_SMG_ADS_Curve` | `ViewKickCurve#8` | `RecoveryKickCurve#1` | `FOVShiftingCurve#9` |
| `SR_04` | `CF_SniperRifles_ADS_Curve (variant 7)` | `ViewKickCurve#10` | `RecoveryKickCurve#1` | `FOVShiftingCurve#8` |
| `STN_01_Heavy_MountedMachineGun` | none† | none† | none† | none† |
| `STN_02_Heavy_MainCannon` | none† | none† | none† | none† |
| `STN_03_Heavy_MainBarrel` | none† | none† | none† | none† |
| `STN_05_Heavy_MainBarrel` | none† | none† | none† | none† |
| `SV98` | `CF_SniperRifles_ADS_Curve (variant 7)` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#12` |
| `SVDM` | `CF_DMR_ADS_Curve` | `ViewKickCurve#9` | `RecoveryKickCurve#1` | `FOVShiftingCurve#13` |
| `TAR21` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#1` |
| `TNK_01_Artillery_Weapon` | none† | none† | none† | none† |
| `TNK_01_Heavy_Weapon` | none† | none† | none† | none† |
| `TNK_01_MachineGun_Weapon` | none† | none† | none† | none† |
| `TNK_03_Weapon` | none† | none† | none† | none† |
| `TNK_04_Weapon` | none† | none† | none† | none† |
| `TankBarrelTest` | none† | none† | none† | none† |
| `Vector` | `CF_SMG_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#9` |
| `WEPN_017` | `CF_SniperRifles_ADS_Curve (variant 7)` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `CF_AimSway_Stabilization_PlayerSpeed_SR` |
| `WEPN_026` | `CF_SMG_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#3` |
| `WEPN_027` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#7` |
| `WEPN_028` | `CF_SMG_ADS_Curve` | `ViewKickCurve#8` | `RecoveryKickCurve#1` | `FOVShiftingCurve#9` |
| `WEPN_029` | `CF_WEPN_029_ADS_Curve` | `ViewKickCurve#2` | `RecoveryKickCurve#1` | `FOVShiftingCurve#1` |
| `WEPN_030` | `CF_WEPN_030_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#10` |
| `WEPN_031` | `CF_SMG_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#9` |
| `WEPN_032` | `CF_Pistol_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#3` |
| `WEPN_033` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#1` |
| `WEPN_034` | `CF_DMR_ADS_Curve` | `ViewKickCurve#11` | `RecoveryKickCurve#1` | `FOVShiftingCurve#13` |
| `WEPN_035` | `CF_SMG_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#12` |
| `WEPN_036` | `CF_LMG_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#5` |
| `WEPN_037` | `CF_AssaultRifle_ADS_Curve` | `ViewKickCurve#1` | `RecoveryKickCurve#1` | `FOVShiftingCurve#7` |
| `WHL_05_RingMinigun` | none† | none† | none† | `FOVShiftingCurve#5` |

### 3c. Curve keys

**`AdsCameraCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `CF_AssaultRifle_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 8 | A91, AK74M, KH2002, M4, TAR21, WEPN_027, … |
| `CF_Launcher_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `CF_SniperRifles_ADS_Curve` | no keys | 1 | CombatBow |
| `CF_Pistol_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 2 | Glock17, WEPN_032 |
| `CF_Pistol_ADS_Curve (variant 4)` | no keys | 1 | Judge |
| `CF_LMG_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 3 | LMG_02, M249, WEPN_036 |
| `CF_Shotgun_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 2 | M12G, MP43 |
| `CF_SniperRifles_ADS_Curve (variant 7)` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 4 | MK22, SR_04, SV98, WEPN_017 |
| `CF_SMG_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 7 | MP9, SMG_03, Vector, WEPN_026, WEPN_028, WEPN_031, … |
| `AdsCameraCurve#1` | 0:0C 1:1C | 1 | MWSY_001_Heavy_MountedMachineGun |
| `CF_DMR_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 3 | RFB, SVDM, WEPN_034 |
| `CF_DMR_ADS_Curve (variant 11)` | no keys | 1 | SKS |
| `CF_WEPN_029_ADS_Curve` | 0:-7.02603e-08L 0.294325:-3.19272e-09C 1:1C | 1 | WEPN_029 |
| `CF_WEPN_030_ADS_Curve` | 0:0C 1:1C | 1 | WEPN_030 |

**`ViewKickCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `ViewKickCurve#1` | 0:0C 0.15:1C | 23 | A91, Fists, Glock17, Judge, KH2002, M2Browning, … |
| `ViewKickCurve#2` | 0:0C 0.18:1C | 2 | AK74M, WEPN_029 |
| `ViewKickCurve#3` | 0:0C 0.15:1C 0.4:0.5L | 1 | CombatBow |
| `ViewKickCurve#4` | 0:0C 1:1C | 2 | GrenadeLauncher, MMGL |
| `ViewKickCurve#5` | 0:0C 0.3:1C | 2 | LMG_02, M249 |
| `ViewKickCurve#6` | 0:0C 0.2:8K | 2 | Launcher_04, RPG7 |
| `ViewKickCurve#7` | 0:0C 0.5:1C | 1 | M12G |
| `ViewKickCurve#8` | 0:0C 0.1:1C | 3 | MP9, SMG_03, WEPN_028 |
| `ViewKickCurve#9` | 0:0C 0.15:1C 0.4:0.75L | 2 | SKS, SVDM |
| `ViewKickCurve#10` | 0:0C 0.124178:1C | 1 | SR_04 |
| `ViewKickCurve#11` | 0:0C 0.0578813:0.806773C 0.15:1C | 1 | WEPN_034 |

**`RecoveryKickCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `RecoveryKickCurve#1` | 0:0C | 33 | A91, AK74M, CombatBow, Glock17, Judge, KH2002, … |
| `RecoveryKickCurve#2` | 0:0C 0.3:1C | 1 | Fists |
| `RecoveryKickCurve#3` | 0:0C 1:1C | 1 | GrenadeLauncher |
| `RecoveryKickCurve#4` | 0:0C 0.35:1C | 2 | Launcher_04, RPG7 |
| `RecoveryKickCurve#5` | -0.000432327:0C | 1 | M12G |
| `RecoveryKickCurve#6` | 0:0C 0.3:0.2C | 1 | M2Browning |
| `RecoveryKickCurve#7` | -0.000432:0C | 1 | MP43 |

**`FOVShiftingCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `FOVShiftingCurve#1` | 0:0L 1:-0.1L 5:-0.1L 10:-0.75L 40:-0.75L 50:-1.25L | 6 | A91, AK74M, KH2002, TAR21, WEPN_029, WEPN_033 |
| `FOVShiftingCurve#2` | 0:0L 1:0L 5:-3L | 1 | CombatBow |
| `FOVShiftingCurve#3` | 0:0L 1:-0.5L 5:-0.5L 10:-1L | 3 | Glock17, WEPN_026, WEPN_032 |
| `FOVShiftingCurve#4` | 0:0L 1:-1.5L 3:-2L 5:-3L | 1 | Judge |
| `FOVShiftingCurve#5` | 0:0L 1:-0.5L 5:-0.5L 10:-1L 40:-1L 50:-1.5L | 5 | LMG_02, M249, ROT_04_MountedMachineGun, WEPN_036, WHL_05_RingMinigun |
| `FOVShiftingCurve#6` | 0:0L 1:-0.4L 3:-0.8L 10:-1L | 2 | M12G, MP43 |
| `FOVShiftingCurve#7` | 0:0L 1:-0.1L 5:-0.1L 10:-0.75L 20:-0.75L 30:-0.75L 40:-0.75L 50:-1.25L | 3 | M4, WEPN_027, WEPN_037 |
| `FOVShiftingCurve#8` | 0:0L 1:-3L 5:-5L | 2 | MK22, SR_04 |
| `FOVShiftingCurve#9` | 0:0L 1:-0.1L 5:-0.5L 10:-0.75L 20:-0.75L 30:-0.75L 40:-0.75L 50:-1.25L | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |
| `FOVShiftingCurve#10` | 0:0L 1.59059:-0.491866L 8.43103:-0.995803L 13.431:-0.995803L 30.2644:-1.47322L | 2 | RFB, WEPN_030 |
| `FOVShiftingCurve#11` | 0:0L 1.5:-0.5L 8.43103:-1L 13.431:-1L 30.2644:-1.5L | 1 | SKS |
| `FOVShiftingCurve#12` | 0:0L 1:-2L 5:-3L | 2 | SV98, WEPN_035 |
| `FOVShiftingCurve#13` | 0:0L 1:-0.5L 5:-1L 10:-1L 30:-1.25L | 2 | SVDM, WEPN_034 |
| `CF_AimSway_Stabilization_PlayerSpeed_SR` | 0:0L 1:-2L 5:-3L | 1 | WEPN_017 |

### 3d. Item camera and animation fields

| Weapon | `AdsTransitionData` | `FireAnimBlendTimeCurve` | Blend targets | Buffered blend time | Sight position offset | Iron-sight camera offset |
|---|---|---|---|---|---|---|
| `A91` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.7, SpringLerpWeight 0.1, AttachmentOffsetAlphaLerpSpeed 34, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.8, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.0251131:0.09C 0.21:-0.01C 1:0C | — | — | — | 0 … 0 … -0.13 |
| `AK74M` | OutSettleWeight 0.1, TransitionVelocity 1, TransitionDamping 0.5, TransitionStrength 0.8, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 30 | 0:0C 0.0982661:0.1C 0.348298:-0.00297387C 0.723272:0.00384496L 1:0C | 5 | — | 0 … 3 … 0 | — |
| `ArtilleryBarrelTest` | — | — | — | — | — | — |
| `CGM4` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | — | — | — | — | — |
| `CombatBow` | TransitionDamping 1, TransitionStrength 1.5, SpringLerpWeight 1, AttachmentEndRange 1 | — | 10 | 0.05 | — | — |
| `Glock17` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | 0:-0.374081L 0.08:0.07L 0.3:-0.15L 0.6:0L | — | — | — | — |
| `Judge` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | — | — | — | — | -0.065 … 0 … -0.1 |
| `KH2002` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.7, SpringLerpWeight 0.1, AttachmentOffsetAlphaLerpSpeed 34, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.8, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.0266773:0.09C 0.210987:-0.00946281C 0.74805:0C | — | — | — | — |
| `LMG_02` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentEndRange 1, CameraOffsetLerpSpeed 999 | 4.65242e-05:-0.235639C 0.0474942:0.0177329C 0.117094:0.0549392C 0.430577:-0.0604416C 0.8:0C | — | — | 0 … -10 … 0 | — |
| `Launcher_04` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | — | — | — | — | — |
| `M12G` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentEndRange 1, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.2 | — | — | 0 | — | — |
| `M249` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentEndRange 0.9, CameraOffsetLerpSpeed 999 | 0:-0.243402L 0.0509249:-0.0206125C 0.113704:0.0441712C 0.290662:-0.0477396C 0.6:0L | — | — | 0 … 2 … 0 | — |
| `M4` | OutSettlePlayTime 9, OutSettleWeight 0.1, TransitionVelocity 1, TransitionDamping 0.5, TransitionStrength 1.2, AttachmentOffsetAlphaLerpSpeed 20, CameraOffsetLerpSpeed 80, MinWallCollisionAlpha 1, MinBlockAdsWallCollisionAlpha 0.3 | 0:-0.028757C 0.059852:0.080121C 0.325306:-0.006201C 1:0C | — | — | — | 0 … 0 … -0.05 |
| `MK22` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | — | 10 | — | — | 0 … 0 … -0.1 |
| `MMGL` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | — | — | — | — | — |
| `MP43` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75 | — | — | — | 0 … 0 … 0.5 | 0 … 0 … -0.154472 |
| `MP9` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, AttachmentEndRange 1 | 0:-0.250063C 0.0550966:0.0147646C 0.117774:0.00208326C 0.4:-0.03C 0.7:0C | — | — | 0 … -5 … 0 | 0 … 0 … -0.08 |
| `RFB` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, AttachmentEndRange 0.9, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.8, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.042125:1C 0.0759435:0.209886C 0.096176:-0.0465181C 1:0C | — | — | 0 … 0.5 … 0 | 0 … 0 … -0.1 |
| `RPG7` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | — | — | — | — | 0 … -10 … 0 |
| `SKS` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.7, SpringLerpWeight 0.1, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.8, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.035835:0.8C 0.230363:-0.218573C 1:0C | — | — | — | — |
| `SMG_03` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.6, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 999 | 0:-0.0589125C 0.0619211:0.0608459C 0.247531:-0.00513959C 0.4:-0.00443341C 0.7:0C | — | — | 0 … 3 … 0 | 0 … 0 … -0.05 |
| `SR_04` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | — | 10 | — | — | — |
| `SV98` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentEndRange 1, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | — | 10 | 0 | 0 … -10 … 0 | 0 … 0 … -0.05 |
| `SVDM` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.0457412:0.766627C 0.164721:-0.201256C 1:0C | — | — | 0 … 2 … 0 | 0 … 2.8 … -0.18 |
| `TAR21` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.7, SpringLerpWeight 0.1, AttachmentOffsetAlphaLerpSpeed 34, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.8, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.03:0.009C 0.21:-0.01C 1:0C | — | — | — | — |
| `TankBarrelTest` | — | — | — | — | — | — |
| `Vector` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, MinWallCollisionAlpha 0.8 | 0:-0.24679C 0.05:0.0123967C 0.15:0.002C 0.4:-0.03C 0.822937:0C | — | — | — | 0 … 0 … 0.2 |
| `WEPN_017` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 15, AttachmentEndRange 0.9, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | — | 10 | — | — | — |
| `WEPN_026` | — | 0:-0.24679C 0.05:0.0123967C 0.15:0.002C 0.4:-0.03C 0.822937:0C | — | — | — | 0 … 0 … -0.05 |
| `WEPN_027` | — | 0:-0.028757C 0.059852:0.080121C 0.325306:-0.006201C 1:0C | — | — | 0 … -3.5 … 0 | — |
| `WEPN_028` | AttachmentEndRange 1 | 0:-0.250063C 0.0550966:0.0147646C 0.117774:0.00208326C 0.4:-0.03C 0.7:0C | — | — | — | 0 … 0 … -0.05 |
| `WEPN_029` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999, MinBlockAdsWallCollisionAlpha 0.3 | 0:0C 0.0982661:0.1C 0.348298:-0.00297387C 0.723272:0.00384496L 1:0C | 5 | — | — | 0 … 0 … 0.1 |
| `WEPN_030` | AttachmentEndRange 1 | 0:0C 0.042125:1C 0.0759435:0.209886C 0.096176:-0.0465181C 1:0C | — | — | — | — |
| `WEPN_031` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.6, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 999 | 0:-0.028757C 0.059852:0.080121C 0.325306:-0.006201C 1:0C | — | — | 0 … 3 … 0 | — |
| `WEPN_032` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.14, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 22, CameraOffsetLerpSpeed 999 | 0:-0.374081L 0.08:0.07L 0.3:-0.15L 0.6:0L | — | — | — | 0 … 2 … 0 |
| `WEPN_033` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.7, SpringLerpWeight 0.1, AttachmentOffsetAlphaLerpSpeed 34, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.8, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.03:0.009C 0.21:-0.01C 1:0C | — | — | — | 0 … 0 … -0.1 |
| `WEPN_034` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.16:0.1C 0.3:0C 1:0C | — | 0 | 0 … 10.5 … 2.2 | 0.0275 … -0.5 … 0 |
| `WEPN_035` | OutSettlePlayTime 9, OutSettleWeight 0.1, TransitionVelocity 1, TransitionDamping 0.5, TransitionStrength 1.2, AttachmentOffsetAlphaLerpSpeed 20, CameraOffsetLerpSpeed 80, MinWallCollisionAlpha 1, MinBlockAdsWallCollisionAlpha 0.3 | — | — | — | 0 … 3 … 0 | — |
| `WEPN_036` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentEndRange 1, CameraOffsetLerpSpeed 999 | 4.65242e-05:0C 0.0572643:0.0468795C 0.225949:0.00652454C 0.50119:-0.000310004L | — | 0 | 0 … 3.7 … 0 | — |
| `WEPN_037` | OutSettlePlayTime 0.7, OutSettleWeight 0.7, OutSettlePlayRate 0.64, TransitionVelocity 0.2, TransitionDamping 0.52, TransitionStrength 1.8, AttachmentOffsetAlphaLerpSpeed 30, AttachmentEndRange 1, CameraOffsetLerpSpeed 999, MinWallCollisionAlpha 0.75, MinBlockAdsWallCollisionAlpha 0.01 | 0:0C 0.16:0.1C 0.3:0C 1:0C | — | 0 | 0 … 4.4 … 0 | 0.03 … 0 … 0 |

## 4. Sway

### 4a. Aim sway scalars

| Weapon | Persistent | Pattern duration (s) | Stand × | Crouch × | Prone × | Focus × | No-focus speed × | Correction offset time | Camera offset × | Scale down speed | Scale up speed | Speed down speed | Speed up speed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | no | 6 | 1.8 | 1.55 | 1.15 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `AK74M` | no | 6 | 1.1 | 0.85 | 0.45 | 0.25† | 2.5 | 2.5† | 1 | 2.9 | 4.1 | 3.2 | 4.4 |
| `AT4` | no | 6 | 1† | 0.75† | 0.5† | 0.25† | 2.5 | 2.5† | 0.75 | 2† | 2† | 2† | 2† |
| `ArtilleryBarrelTest` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `BuildTool` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `CGM4` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 5 | 0.75 | 1.4 | 2.6 | 1.6 | 2.9 |
| `CombatBow` | no | 6 | 0.8 | 0.5 | 0.25 | 0.25† | 2.5 | 2.5† | 0.75 | 2† | 2† | 2† | 2† |
| `Fists` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `Glock17` | no | 6 | 1† | 0.75† | 0.25 | 0.25† | 2.5 | 1 | 0.75 | 2.9 | 4 | 3.2 | 4.3 |
| `GrenadeLauncher` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `Judge` | no | 6 | 1† | 0.75† | 0.25 | 0.25† | 2.5 | 1 | 0.75 | 2.8 | 3.9 | 3.1 | 4.2 |
| `KH2002` | no | 6 | 1.8 | 1.55 | 1.15 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `LMG_02` | no | 6 | 1.15 | 0.55 | 0.35 | 0.25† | 2.5 | 5 | 0.75 | 1.5 | 2.6 | 1.7 | 2.9 |
| `Launcher_04` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 2.5† | 0.75 | 2† | 2† | 2† | 2† |
| `M12G` | no | 6 | 1† | 0.75† | 0.5† | 0.25† | 2.5 | 5 | 0.75 | 2.1 | 2.8 | 2.3 | 3 |
| `M249` | no | 6 | 1† | 0.55 | 0.35 | 0.25† | 2.5 | 5 | 0.75 | 1.6 | 2.7 | 1.8 | 3 |
| `M2Browning` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `M4` | no | 6 | 1† | 0.75† | 0.45 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2† | 3 |
| `MK22` | no | 6 | 0.7 | 0.4 | 0.2 | 0.25† | 2.5 | 5 | 0.75 | 1.4 | 2.6 | 1.7 | 2.9 |
| `MMGL` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 5 | 0.75 | 1.4 | 2.6 | 1.6 | 2.9 |
| `MP43` | no | 6 | 1.3 | 0.75† | 0.4 | 0.25† | 2.5 | 2.5† | 0.75 | 2.1 | 2.8 | 2.3 | 3 |
| `MP9` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 1 | 0.75 | 2.9 | 4.1 | 3.2 | 4.4 |
| `MWSY_001_Heavy_MountedMachineGun` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `RFB` | no | 6 | 1.2 | 0.55 | 0.35 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `ROT_02_Weapon_122mm` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `ROT_02_Weapon_30mmCannon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `ROT_03_AttachedMachineGuns` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `ROT_03_Weapon_122mm` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `ROT_04_MountedMachineGun` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `RPG7` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 5 | 0.75 | 1.3 | 2.6 | 1.6 | 2.8 |
| `SKS` | no | 6 | 1† | 0.55 | 0.35 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.9 | 2.4 | 3.1 |
| `SMG_03` | no | 6 | 0.9 | 0.65 | 0.25 | 0.25† | 2.5 | 1 | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `SR_04` | no | 6 | 0.75 | 0.4 | 0.2 | 0.25† | 2.5 | 5 | 0.75 | 1.5 | 2.8 | 1.8 | 3.1 |
| `STN_01_Heavy_MountedMachineGun` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `STN_02_Heavy_MainCannon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `STN_03_Heavy_MainBarrel` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `STN_05_Heavy_MainBarrel` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `SV98` | no | 6 | 0.7 | 0.4 | 0.25 | 0.25† | 2.5 | 5 | 0.75 | 1.5 | 2.7 | 1.7 | 3 |
| `SVDM` | no | 6 | 1.15 | 0.55 | 0.35 | 0.25† | 2.5 | 2.5† | 0.75 | 2.1 | 2.8 | 2.3 | 3 |
| `TAR21` | no | 6 | 1.8 | 1.55 | 1.15 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `TNK_01_Artillery_Weapon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `TNK_01_Heavy_Weapon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `TNK_01_MachineGun_Weapon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `TNK_03_Weapon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `TNK_04_Weapon` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `TankBarrelTest` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |
| `Vector` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 1 | 0.75 | 2.8 | 4 | 3.1 | 4.3 |
| `WEPN_017` | no | 6 | 0.75 | 0.4 | 0.25 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.9 | 2.5 | 3.1 |
| `WEPN_026` | no | 6 | 1† | 0.75† | 0.25 | 0.25† | 2.5 | 1 | 0.75 | 2.7 | 3.8 | 3 | 4.1 |
| `WEPN_027` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 1 | 0.75 | 2.9 | 4 | 3.2 | 4.3 |
| `WEPN_028` | no | 6 | 1† | 0.75† | 0.35 | 0.25† | 2.5 | 1 | 0.75 | 2.8 | 4 | 3.1 | 4.2 |
| `WEPN_029` | no | 6 | 1.2 | 0.95 | 0.55 | 0.25† | 2.5 | 2.5† | 0.75 | 2.1 | 2.7 | 2.3 | 2.9 |
| `WEPN_030` | no | 6 | 1.3 | 1.05 | 0.65 | 0.25† | 2.5 | 2.5† | 0.75 | 2.1 | 2.7 | 2.3 | 2.9 |
| `WEPN_031` | no | 6 | 0.9 | 0.65 | 0.25 | 0.25† | 2.5 | 1 | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `WEPN_032` | no | 6 | 1† | 0.75† | 0.25 | 0.25† | 2.5 | 1 | 0.75 | 2.9 | 4 | 3.2 | 4.3 |
| `WEPN_033` | no | 6 | 1.8 | 1.55 | 1.15 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2.4 | 3 |
| `WEPN_034` | no | 6 | 1† | 0.55 | 0.35 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.9 | 2.4 | 3.1 |
| `WEPN_035` | no | 6 | 0.7 | 0.4 | 0.25 | 0.25† | 2.5 | 5 | 0.75 | 1.5 | 2.7 | 1.7 | 3 |
| `WEPN_036` | no | 6 | 1.5 | 0.75† | 0.45 | 0.25† | 2.5 | 5 | 0.75 | 1.5 | 2.6 | 1.7 | 2.9 |
| `WEPN_037` | no | 6 | 1† | 0.75† | 0.45 | 0.25† | 2.5 | 2.5† | 0.75 | 2.2 | 2.8 | 2† | 3 |
| `WHL_05_RingMinigun` | yes† | 0† | 1† | 0.75† | 0.5† | 0.25† | 1† | 2.5† | 0.25† | 2† | 2† | 2† | 2† |

### 4b. Aim sway deviation, idle sway, stabilisation sway

| Weapon | Horizontal deviation min … max | Vertical deviation min … max | Rotation idle × | Translation idle × | Translation stab. stance × | Rotation stab. stance × | Rotation stab. × | Translation stab. × | Translation jitter | Rotation jitter | Sight sway distance | Stabilisation hold (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | 0.9 … 1.5 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | -7 | 0.3† |
| `AK74M` | 0.9 … 1.5 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 0.8 / 0.5† / 0.25† | 0† | 0† | no† | yes | 25 | 0.4 |
| `AT4` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `ArtilleryBarrelTest` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `BuildTool` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `CGM4` | 0.94 … 1.08 | 0.94 … 1.08 | 0.02 | 0.01 | 0.8 / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 0† | 0.8 |
| `CombatBow` | 0.95 … 1.1 | 0.9 … 1.15 | 0.02 | 0.01 | 0.7 / 0.5† / 0.25† | 0.8 / 0.5† / 0.25† | 0† | 0† | yes | yes | 13 | 0.3† |
| `Fists` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `Glock17` | 0.88 … 1.2 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 0.5 / 0.35 / 0.25† | 0† | 0† | no† | yes | 5 | 0.2 |
| `GrenadeLauncher` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `Judge` | 0.88 … 1.2 | 0.9 … 1.15 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1.2 / 0.5† / 0.25† | 0† | 0† | no† | yes | 5 | 0.5 |
| `KH2002` | 0.9 … 1.5 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | -7 | 0.35 |
| `LMG_02` | 0.92 … 1.25 | 0.9 … 2 | 0.4 | 0.25 | 0.25 / 0.25 / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 15 | 1.5 |
| `Launcher_04` | 0.94 … 1.08 | 1 … 1† | 0.02 | 0.01 | 0.8 / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | -7 | 1 |
| `M12G` | 0.9 … 1.15 | 0.9 … 1.12 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 0.5 / 0.35 / 0.25† | 0† | 0† | no† | yes | 10 | 0.4 |
| `M249` | 0.92 … 1.2 | 0.9 … 2 | 0.08 | 0.04 | 0.25 / 0.25 / 0.25† | 1† / 0.5† / 0.35 | 0† | 0† | yes | yes | -3 | 1.5 |
| `M2Browning` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `M4` | 0.85 … 1.4 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 0† | 0.3† |
| `MK22` | 0.9 … 1.15 | 0.92 … 1.2 | 0.15 | 0.1 | 1† / 0.5† / 0.35 | 0.4 / 0.3 / 0.2 | 0† | 0† | yes | yes | 25 | 1.5 |
| `MMGL` | 0.94 … 1.15 | 0.9 … 1.12 | 0.02 | 0.01 | 0.8 / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 16 | 0.7 |
| `MP43` | 0.9 … 1.15 | 0.9 … 1.12 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 0.5 / 0.35 / 0.25† | 0† | 0† | no† | yes | 10 | 0.35 |
| `MP9` | 0.88 … 1.3 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 0.8 / 0.5† / 0.25† | 0† | 0† | no† | yes | 15 | 0.15 |
| `MWSY_001_Heavy_MountedMachineGun` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `RFB` | 0.92 … 1.08 | 0.94 … 1.08 | 0.03 | 0.02 | 0.25 / 0.25 / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | yes | yes | 3 | 1 |
| `ROT_02_Weapon_122mm` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `ROT_02_Weapon_30mmCannon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `ROT_03_AttachedMachineGuns` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `ROT_03_Weapon_122mm` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `ROT_04_MountedMachineGun` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `RPG7` | 0.94 … 1.08 | 0.94 … 1.08 | 0.02 | 0.01 | 0.8 / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | -15 | 0.7 |
| `SKS` | 0.92 … 1.08 | 0.94 … 1.08 | 0.05 | 0.02 | 0.25 / 0.25 / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | yes | yes | 25 | 0.5 |
| `SMG_03` | 0.88 … 1.25 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 0.8 / 0.5† / 0.25† | 0† | 0† | no† | yes | 40 | 0.25 |
| `SR_04` | 0.9 … 1.15 | 0.92 … 1.2 | 0.1 | 0.06 | 1† / 0.5† / 0.35 | 0.5 / 0.3 / 0.25† | 0† | 0† | yes | yes | 12 | 2 |
| `STN_01_Heavy_MountedMachineGun` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `STN_02_Heavy_MainCannon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `STN_03_Heavy_MainBarrel` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `STN_05_Heavy_MainBarrel` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `SV98` | 0.9 … 1.15 | 0.92 … 1.2 | 0.09 | 0.05 | 1† / 0.5† / 0.35 | 0.4 / 0.3 / 0.2 | 0† | 0† | yes | yes | 30 | 1.25 |
| `SVDM` | 0.92 … 1.08 | 0.94 … 1.08 | 0.05 | 0.02 | 0.25 / 0.25 / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | yes | yes | 30 | 0.8 |
| `TAR21` | 0.9 … 1.5 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | -3 | 0.3† |
| `TNK_01_Artillery_Weapon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `TNK_01_Heavy_Weapon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `TNK_01_MachineGun_Weapon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `TNK_03_Weapon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `TNK_04_Weapon` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `TankBarrelTest` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |
| `Vector` | 0.88 … 1.25 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 25 | 0.15 |
| `WEPN_017` | 0.9 … 1.15 | 0.92 … 1.2 | 0.09 | 0.06 | 1† / 0.5† / 0.35 | 0.4 / 0.3 / 0.2 | 0† | 0† | yes | yes | 45 | 1.25 |
| `WEPN_026` | 0.88 … 1.2 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 5 | 0.2 |
| `WEPN_027` | 0.88 … 1.2 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 0† | 0.3† |
| `WEPN_028` | 0.88 … 1.2 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 0.8 / 0.5† / 0.25† | 0† | 0† | no† | yes | 2 | 0.2 |
| `WEPN_029` | 0.9 … 1.5 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 0† | 0.4 |
| `WEPN_030` | 0.95 … 1.55 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | yes | yes | -5 | 0.45 |
| `WEPN_031` | 0.88 … 1.25 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 0.8 / 0.5† / 0.25† | 0† | 0† | no† | yes | 40 | 0.25 |
| `WEPN_032` | 0.88 … 1.2 | 0.9 … 1.15 | 0.04 | 0.02 | 1† / 0.5† / 0.25† | 0.5 / 0.35 / 0.25† | 0† | 0† | no† | yes | 5 | 0.15 |
| `WEPN_033` | 0.9 … 1.5 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | -3 | 0.3† |
| `WEPN_034` | 0.92 … 1.08 | 0.94 … 1.08 | 0.05 | 0.02 | 0.25 / 0.25 / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | yes | yes | 25 | 0.5 |
| `WEPN_035` | 0.9 … 1.15 | 0.92 … 1.2 | 0.09 | 0.05 | 0.5 / 0.4 / 0.35 | 0.4 / 0.3 / 0.2 | 0† | 0† | yes | yes | 30 | 1.25 |
| `WEPN_036` | 0.92 … 1.25 | 0.9 … 2 | 0.4 | 0.25 | 0.8 / 0.65 / 0.4 | 0.8 / 0.5† / 0.25† | 0† | 0† | no† | yes | 0.5 | 1 |
| `WEPN_037` | 0.85 … 1.4 | 0.92 … 1.1 | 0.02 | 0.01 | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | yes | 0† | 0.3† |
| `WHL_05_RingMinigun` | 1 … 1† | 1 … 1† | 0† | 0† | 1† / 0.5† / 0.25† | 1† / 0.5† / 0.25† | 0† | 0† | no† | no† | 0† | 0.3† |

Stance multipliers read `stand / crouch / prone`; each member has its own `†`.

### 4c. Jitter

| Weapon | Transl. Result offset | Transl. Noise jitter | Transl. Initial offset | Transl. Path jitter | Transl. Secondary | Rot. Result offset | Rot. Noise jitter | Rot. Initial offset | Rot. Path jitter | Rot. Secondary |
|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 1 |
| `AK74M` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 0.75 |
| `AT4` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `ArtilleryBarrelTest` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `BuildTool` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `CGM4` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.5 |
| `CombatBow` | 0.1 | 2† | 2† | 1 | 2 | 0.1 | 2† | 0 | 2 | 1 |
| `Fists` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `Glock17` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.5 | 0.5 |
| `GrenadeLauncher` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `Judge` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.7 |
| `KH2002` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 1 |
| `LMG_02` | 0.01 | 1 | 0 | 0.15 | 0.05 | 0.1 | 1 | 1 | 1 | 2 |
| `Launcher_04` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.5 |
| `M12G` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.7 |
| `M249` | 0.01 | 1 | 0 | 0.02 | 0.01 | 0.1 | 1 | 1 | 1 | 1.5 |
| `M2Browning` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `M4` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 0.7 |
| `MK22` | 0.1 | 1 | 1 | 0.05 | 0.03 | 0.1 | 0.75 | 1 | 1 | 0.75 |
| `MMGL` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 1 | 0.5 |
| `MP43` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.7 |
| `MP9` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.2† |
| `MWSY_001_Heavy_MountedMachineGun` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `RFB` | 0.01 | 2† | 0 | 0.01 | 0.05 | 0.1 | 1 | 0 | 1 | 0.7 |
| `ROT_02_Weapon_122mm` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `ROT_02_Weapon_30mmCannon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `ROT_03_AttachedMachineGuns` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `ROT_03_Weapon_122mm` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `ROT_04_MountedMachineGun` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `RPG7` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 1 | 0.5 |
| `SKS` | 0.01 | 1 | 0 | 0.02 | 0.01 | 0.1 | 1 | 0 | 0.7 | 1 |
| `SMG_03` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.2† |
| `SR_04` | 0.1 | 1 | 1 | 0.05 | 0.03 | 0.1 | 0.8 | 1 | 1.1 | 0.7 |
| `STN_01_Heavy_MountedMachineGun` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `STN_02_Heavy_MainCannon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `STN_03_Heavy_MainBarrel` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `STN_05_Heavy_MainBarrel` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `SV98` | 0.1 | 1 | 1 | 0.05 | 0.03 | 0.1 | 0.75 | 1 | 1 | 0.7 |
| `SVDM` | 0.01 | 1 | 0 | 0.01 | 0.05 | 0.1 | 1 | 0 | 1 | 0.7 |
| `TAR21` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 1 |
| `TNK_01_Artillery_Weapon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `TNK_01_Heavy_Weapon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `TNK_01_MachineGun_Weapon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `TNK_03_Weapon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `TNK_04_Weapon` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `TankBarrelTest` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |
| `Vector` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.2† |
| `WEPN_017` | 0.1 | 1 | 1 | 0.05 | 0.03 | 0.1 | 0.75 | 1 | 1 | 0.7 |
| `WEPN_026` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.5 | 0.5 |
| `WEPN_027` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.7 |
| `WEPN_028` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.2† |
| `WEPN_029` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1 | 0 | 1 | 0.4 |
| `WEPN_030` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1 | 0 | 0.5 | 1 |
| `WEPN_031` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.7 | 0.2† |
| `WEPN_032` | 0† | 2† | 2† | 0.2† | 0.2† | 0.1 | 1 | 0 | 0.5 | 0.5 |
| `WEPN_033` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 1 |
| `WEPN_034` | 0.01 | 1 | 0 | 0.02 | 0.01 | 0.1 | 1 | 0 | 0.7 | 1 |
| `WEPN_035` | 0.1 | 1 | 1 | 0.05 | 0.03 | 0.1 | 0.75 | 1 | 1 | 0.7 |
| `WEPN_036` | 0.01 | 1 | 0 | 0.15 | 0.05 | 0.1 | 1 | 1 | 0.5 | 1 |
| `WEPN_037` | 0.1 | 1 | 0 | 0.02 | 0.01 | 0.01 | 1.25 | 0 | 0.5 | 0.7 |
| `WHL_05_RingMinigun` | 0† | 2† | 2† | 0.2† | 0.2† | 0† | 2† | 2† | 0.2† | 0.2† |

### 4d. Persistent (non-curve) sway values

| Weapon | Sway speed | Horizontal magnitude | Vertical magnitude |
|---|---|---|---|
| `ArtilleryBarrelTest` | 0.1† | 1† | 1† |
| `BuildTool` | 0.1† | 1† | 1† |
| `Fists` | 0.1† | 1† | 1† |
| `GrenadeLauncher` | 0.1† | 1† | 1† |
| `M2Browning` | 0.1† | 1† | 1† |
| `MWSY_001_Heavy_MountedMachineGun` | 0.1† | 1† | 1† |
| `ROT_02_Weapon_122mm` | 0.1† | 1† | 1† |
| `ROT_02_Weapon_30mmCannon` | 0.1† | 1† | 1† |
| `ROT_03_AttachedMachineGuns` | 0.1† | 1† | 1† |
| `ROT_03_Weapon_122mm` | 0.1† | 1† | 1† |
| `ROT_04_MountedMachineGun` | 0.1† | 1† | 1† |
| `STN_01_Heavy_MountedMachineGun` | 0.1† | 1† | 1† |
| `STN_02_Heavy_MainCannon` | 0.1† | 1† | 1† |
| `STN_03_Heavy_MainBarrel` | 0.1† | 1† | 1† |
| `STN_05_Heavy_MainBarrel` | 0.1† | 1† | 1† |
| `TNK_01_Artillery_Weapon` | 0.1† | 1† | 1† |
| `TNK_01_Heavy_Weapon` | 0.1† | 1† | 1† |
| `TNK_01_MachineGun_Weapon` | 0.1† | 1† | 1† |
| `TNK_03_Weapon` | 0.1† | 1† | 1† |
| `TNK_04_Weapon` | 0.1† | 1† | 1† |
| `TankBarrelTest` | 0.1† | 1† | 1† |
| `WHL_05_RingMinigun` | 0.1† | 1† | 1† |

### 4e. Animation sway

| Weapon | Enabled | Stand × | Crouch × | Prone × | Hip persistent | Hip pitch × | Hip yaw × | ADS persistent | ADS pitch × | ADS yaw × |
|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `AK74M` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `AT4` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `ArtilleryBarrelTest` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `BuildTool` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `CGM4` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `CombatBow` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `Fists` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `Glock17` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `GrenadeLauncher` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `Judge` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `KH2002` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `LMG_02` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `Launcher_04` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `M12G` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `M249` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `M2Browning` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `M4` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `MK22` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `MMGL` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `MP43` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `MP9` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `MWSY_001_Heavy_MountedMachineGun` | no | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `RFB` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `ROT_02_Weapon_122mm` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `ROT_02_Weapon_30mmCannon` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `ROT_03_AttachedMachineGuns` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `ROT_03_Weapon_122mm` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `ROT_04_MountedMachineGun` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `RPG7` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `SKS` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `SMG_03` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `SR_04` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `STN_01_Heavy_MountedMachineGun` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `STN_02_Heavy_MainCannon` | no | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `STN_03_Heavy_MainBarrel` | no | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `STN_05_Heavy_MainBarrel` | no | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `SV98` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `SVDM` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `TAR21` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `TNK_01_Artillery_Weapon` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `TNK_01_Heavy_Weapon` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `TNK_01_MachineGun_Weapon` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `TNK_03_Weapon` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `TNK_04_Weapon` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `TankBarrelTest` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |
| `Vector` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_017` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_026` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_027` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_028` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_029` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_030` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_031` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_032` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_033` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_034` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_035` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_036` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WEPN_037` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | no | 1† | 1† |
| `WHL_05_RingMinigun` | yes† | 1† | 0.75† | 0.5† | yes† | -0.25† | 0.25† | yes† | 1† | 1† |

### 4f. Sway curves per weapon

| Weapon | `Anim.HipPitchSwayMultiplierCurve` | `Anim.HipYawSwayMultiplierCurve` | `Anim.ADSPitchSwayMultiplierCurve` | `Anim.ADSYawSwayMultiplierCurve` | `CurveData.AimSwaySpeedCurve` | `WeaponTranslationStabilizationSway` | `WeaponRotationStabilizationSway` | `AdsStabilizationData.AdsAimSwayScaleCurve` | `AdsStabilizationData.AdsAimSwaySpeedCurve` | `CurveData.HorizontalAimSwayMovementCurve` | `CurveData.VerticalAimSwayMovementCurve` | `PlayerSpeedStabilizationMultiplierCurve` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `AK74M` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Harsh` | `CRV_WeaponAnimSwayMultiplier_AR_Harsh` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `AT4` | none† | none† | none† | none† | `AimSway_SpeedCurve` | none† | none† | none† | none† | `HorizontalAimSway_MovementCurve` | `VerticalAimSway_MovementCurve` | none† |
| `ArtilleryBarrelTest` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `BuildTool` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `CGM4` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Launcher` | `CRV_WeaponAnimSwayMultiplier_Launcher` | `AimSway_SpeedCurve_Launchers` | `AdsStabilizationTranslation_Launcher` | `AdsStabilizationRotation_Launcher` | none† | none† | `HorizontalAimSway_MovementCurve_Launchers` | `VerticalAimSway_MovementCurve_Launchers` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `CombatBow` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Bow` | `CRV_WeaponAnimSwayMultiplier_Bow` | `AimSway_SpeedCurve` | `AdsStabilizationTranslation_DMR` | `AdsStabilizationRotation_DMR` | none† | none† | `HorizontalAimSway_MovementCurve` | `VerticalAimSway_MovementCurve` | `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` |
| `Fists` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `Glock17` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `AimSway_SpeedCurve_Pistol` | `AdsStabilizationTranslation_Pistol` | `AdsStabilizationRotation_Pistol` | none† | none† | `HorizontalAimSway_MovementCurve_Pistol` | `VerticalAimSway_MovementCurve_Pistol` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `GrenadeLauncher` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `Judge` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Sidearms (variant 5)` | `CRV_WeaponAnimSwayMultiplier_Sidearms (variant 5)` | `AimSway_SpeedCurve_Pistol (variant 4)` | `AdsStabilizationTranslation_Pistol` | `AdsStabilizationRotation_Pistol` | none† | none† | `HorizontalAimSway_MovementCurve_Pistol (variant 4)` | `VerticalAimSway_MovementCurve_Pistol (variant 4)` | `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` |
| `KH2002` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `LMG_02` | none† | none† | `CRV_WeaponAnimSwayMultiplier_LMG_Moderate` | `CRV_WeaponAnimSwayMultiplier_LMG_Moderate` | `AimSway_SpeedCurve_LMG` | `AdsStabilizationTranslation_LMG` | `AdsStabilizationRotation_LMG` | `AdsStabilization_AimSwayScale_LMG` | `AdsStabilization_AimSwaySpeed_LMG` | `HorizontalAimSway_MovementCurve_LMG` | `VerticalAimSway_MovementCurve_LMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `Launcher_04` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Launcher` | `CRV_WeaponAnimSwayMultiplier_Launcher` | `AimSway_SpeedCurve_Launchers` | `AdsStabilizationTranslation_Launcher` | `AdsStabilizationRotation_Launcher` | none† | none† | `HorizontalAimSway_MovementCurve_Launchers` | `VerticalAimSway_MovementCurve_Launchers` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `M12G` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Shotgun` | `CRV_WeaponAnimSwayMultiplier_Shotgun` | `AimSway_SpeedCurve_Shotgun` | `AdsStabilizationTranslation_Shotgun` | `AdsStabilizationRotation_Shotgun` | none† | none† | `HorizontalAimSway_MovementCurve_Shotgun` | `VerticalAimSway_MovementCurve_Shotgun` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `M249` | none† | none† | `CRV_WeaponAnimSwayMultiplier_LMG_Harsh` | `CRV_WeaponAnimSwayMultiplier_LMG_Harsh` | `AimSway_SpeedCurve_LMG` | `AdsStabilizationTranslation_LMG` | `AdsStabilizationRotation_LMG` | none† | none† | `HorizontalAimSway_MovementCurve_LMG` | `VerticalAimSway_MovementCurve_LMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `M2Browning` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `M4` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `MK22` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `AimSway_SpeedCurve_SR` | `AdsStabilizationTranslation_SR` | `AdsStabilizationRotation_SR` | none† | none† | `HorizontalAimSway_MovementCurve_SR` | `VerticalAimSway_MovementCurve_SR` | `CF_AimSway_Stabilization_PlayerSpeed_SR` |
| `MMGL` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Launcher` | `CRV_WeaponAnimSwayMultiplier_Launcher` | `AimSway_SpeedCurve_Launchers` | `AdsStabilizationTranslation_Launcher` | `AdsStabilizationRotation_Launcher` | none† | none† | `HorizontalAimSway_MovementCurve_Launchers` | `VerticalAimSway_MovementCurve_Launchers` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `MP43` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Shotgun` | `CRV_WeaponAnimSwayMultiplier_Shotgun` | `AimSway_SpeedCurve_Shotgun` | `AdsStabilizationTranslation_Shotgun` | `AdsStabilizationRotation_Shotgun` | none† | none† | `HorizontalAimSway_MovementCurve_Shotgun` | `VerticalAimSway_MovementCurve_Shotgun` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `MP9` | none† | none† | `CRV_WeaponAnimSwayMultiplier_SMG` | `CRV_WeaponAnimSwayMultiplier_SMG` | `AimSway_SpeedCurve_SMG` | `AdsStabilizationTranslation_SMG` | `AdsStabilizationRotation_SMG` | none† | none† | `HorizontalAimSway_MovementCurve_SMG` | `VerticalAimSway_MovementCurve_SMG` | `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` |
| `MWSY_001_Heavy_MountedMachineGun` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `RFB` | none† | none† | `CRV_WeaponAnimSwayMultiplier_DMR_Moderate` | `CRV_WeaponAnimSwayMultiplier_DMR_Moderate` | `AimSway_SpeedCurve_DMR` | `AdsStabilizationTranslation_DMR` | `AdsStabilizationRotation_DMR` | none† | none† | `HorizontalAimSway_MovementCurve_DMR` | `VerticalAimSway_MovementCurve_DMR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `ROT_02_Weapon_122mm` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `ROT_02_Weapon_30mmCannon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `ROT_03_AttachedMachineGuns` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `ROT_03_Weapon_122mm` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `ROT_04_MountedMachineGun` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `RPG7` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Launcher` | `CRV_WeaponAnimSwayMultiplier_Launcher` | `AimSway_SpeedCurve_Launchers` | `AdsStabilizationTranslation_Launcher` | `AdsStabilizationRotation_Launcher` | none† | none† | `HorizontalAimSway_MovementCurve_Launchers` | `VerticalAimSway_MovementCurve_Launchers` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `SKS` | none† | none† | `CRV_WeaponAnimSwayMultiplier_DMR_Harsh` | `CRV_WeaponAnimSwayMultiplier_DMR_Harsh` | `AimSway_SpeedCurve_DMR (variant 10)` | `AdsStabilizationTranslation_DMR` | `AdsStabilizationRotation_DMR` | none† | none† | `HorizontalAimSway_MovementCurve_DMR (variant 10)` | `VerticalAimSway_MovementCurve_DMR (variant 10)` | `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` |
| `SMG_03` | none† | none† | `CRV_WeaponAnimSwayMultiplier_SMG` | `CRV_WeaponAnimSwayMultiplier_SMG` | `AimSway_SpeedCurve_SMG` | `AdsStabilizationTranslation_SMG` | `AdsStabilizationRotation_SMG` | none† | none† | `HorizontalAimSway_MovementCurve_SMG` | `VerticalAimSway_MovementCurve_SMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `SR_04` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `AimSway_SpeedCurve_SR` | `AdsStabilizationTranslation_SR` | `AdsStabilizationRotation_SR` | none† | none† | `HorizontalAimSway_MovementCurve_SR` | `VerticalAimSway_MovementCurve_SR` | `CF_AimSway_Stabilization_PlayerSpeed_SR` |
| `STN_01_Heavy_MountedMachineGun` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `STN_02_Heavy_MainCannon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `STN_03_Heavy_MainBarrel` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `STN_05_Heavy_MainBarrel` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `SV98` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `AimSway_SpeedCurve_SR` | `AdsStabilizationTranslation_SR` | `AdsStabilizationRotation_SR` | none† | none† | `HorizontalAimSway_MovementCurve_SR` | `VerticalAimSway_MovementCurve_SR` | `CF_AimSway_Stabilization_PlayerSpeed_SR` |
| `SVDM` | none† | none† | `CRV_WeaponAnimSwayMultiplier_DMR_Harsh (variant 13)` | `CRV_WeaponAnimSwayMultiplier_DMR_Harsh (variant 13)` | `AimSway_SpeedCurve_DMR` | `AdsStabilizationTranslation_DMR` | `AdsStabilizationRotation_DMR` | none† | none† | `HorizontalAimSway_MovementCurve_DMR` | `VerticalAimSway_MovementCurve_DMR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `TAR21` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `TNK_01_Artillery_Weapon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `TNK_01_Heavy_Weapon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `TNK_01_MachineGun_Weapon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `TNK_03_Weapon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `TNK_04_Weapon` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `TankBarrelTest` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |
| `Vector` | none† | none† | `CRV_WeaponAnimSwayMultiplier_SMG` | `CRV_WeaponAnimSwayMultiplier_SMG` | `AimSway_SpeedCurve_SMG` | `AdsStabilizationTranslation_SMG` | `AdsStabilizationRotation_SMG` | none† | none† | `HorizontalAimSway_MovementCurve_SMG` | `VerticalAimSway_MovementCurve_SMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_017` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Snipers_Moderate` | `CRV_WeaponAnimSwayMultiplier_Snipers_Moderate` | `AimSway_SpeedCurve_SR` | `AdsStabilizationTranslation_SR` | `AdsStabilizationRotation_SR` | none† | none† | `HorizontalAimSway_MovementCurve_SR` | `VerticalAimSway_MovementCurve_SR` | `CF_AimSway_Stabilization_PlayerSpeed_SR (variant 3)` |
| `WEPN_026` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `AimSway_SpeedCurve_Pistol` | `AdsStabilizationTranslation_Pistol` | `AdsStabilizationRotation_Pistol` | none† | none† | `HorizontalAimSway_MovementCurve_Pistol` | `VerticalAimSway_MovementCurve_Pistol` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_027` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `AimSway_SpeedCurve_Pistol` | `AdsStabilizationTranslation_Pistol` | `AdsStabilizationRotation_Pistol` | none† | none† | `HorizontalAimSway_MovementCurve_Pistol` | `VerticalAimSway_MovementCurve_Pistol` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_028` | none† | none† | `CRV_WeaponAnimSwayMultiplier_SMG` | `CRV_WeaponAnimSwayMultiplier_SMG` | `AimSway_SpeedCurve_SMG` | `AdsStabilizationTranslation_SMG` | `AdsStabilizationRotation_SMG` | none† | none† | `HorizontalAimSway_MovementCurve_SMG` | `VerticalAimSway_MovementCurve_SMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_029` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` |
| `WEPN_030` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_SR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_031` | none† | none† | `CRV_WeaponAnimSwayMultiplier_SMG` | `CRV_WeaponAnimSwayMultiplier_SMG` | `AimSway_SpeedCurve_SMG` | `AdsStabilizationTranslation_SMG` | `AdsStabilizationRotation_SMG` | none† | none† | `HorizontalAimSway_MovementCurve_SMG` | `VerticalAimSway_MovementCurve_SMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_032` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `CRV_WeaponAnimSwayMultiplier_Sidearms` | `AimSway_SpeedCurve_Pistol` | `AdsStabilizationTranslation_Pistol` | `AdsStabilizationRotation_Pistol` | none† | none† | `HorizontalAimSway_MovementCurve_Pistol` | `VerticalAimSway_MovementCurve_Pistol` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_033` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR` | `VerticalAimSway_MovementCurve_AR` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_034` | none† | none† | `CRV_WeaponAnimSwayMultiplier_DMR_Harsh (variant 13)` | `CRV_WeaponAnimSwayMultiplier_DMR_Harsh (variant 13)` | `AimSway_SpeedCurve_DMR (variant 10)` | `AdsStabilizationTranslation_DMR` | `AdsStabilizationRotation_DMR` | none† | none† | `HorizontalAimSway_MovementCurve_DMR (variant 10)` | `VerticalAimSway_MovementCurve_DMR (variant 10)` | `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` |
| `WEPN_035` | none† | none† | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | `AimSway_SpeedCurve_SR` | `AdsStabilizationTranslation_DMR` | `AdsStabilizationRotation_DMR` | none† | none† | `HorizontalAimSway_MovementCurve_SR` | `VerticalAimSway_MovementCurve_SR` | `CF_AimSway_Stabilization_PlayerSpeed_SR` |
| `WEPN_036` | none† | none† | `CRV_WeaponAnimSwayMultiplier_LMG_Moderate` | `CRV_WeaponAnimSwayMultiplier_LMG_Moderate` | `AimSway_SpeedCurve_LMG` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | `AdsStabilization_AimSwayScale_LMG` | `AdsStabilization_AimSwaySpeed_LMG` | `HorizontalAimSway_MovementCurve_LMG` | `VerticalAimSway_MovementCurve_LMG` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WEPN_037` | none† | none† | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | `AimSway_SpeedCurve_AR` | `AdsStabilizationTranslation_AR` | `AdsStabilizationRotation_AR` | none† | none† | `HorizontalAimSway_MovementCurve_AR (variant 11)` | `VerticalAimSway_MovementCurve_AR (variant 11)` | `CF_AimSway_Stabilization_PlayerSpeed` |
| `WHL_05_RingMinigun` | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† | none† |

### 4g. Sway curve keys

**`AnimationSwayData.HipPitchSwayMultiplierCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|

**`AnimationSwayData.HipYawSwayMultiplierCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|

**`AnimationSwayData.ADSPitchSwayMultiplierCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 8 | A91, KH2002, M4, TAR21, WEPN_029, WEPN_030, … |
| `CRV_WeaponAnimSwayMultiplier_AR_Harsh` | 0:-6.41202e-08C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 1 | AK74M |
| `CRV_WeaponAnimSwayMultiplier_Launcher` | 0:0C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `CRV_WeaponAnimSwayMultiplier_Bow` | no keys | 1 | CombatBow |
| `CRV_WeaponAnimSwayMultiplier_Sidearms` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 4 | Glock17, WEPN_026, WEPN_027, WEPN_032 |
| `CRV_WeaponAnimSwayMultiplier_Sidearms (variant 5)` | no keys | 1 | Judge |
| `CRV_WeaponAnimSwayMultiplier_LMG_Moderate` | 0:0C 0.005:0.5C 0.01:0.7C 0.02:1.1C 0.025:1.5C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 2 | LMG_02, WEPN_036 |
| `CRV_WeaponAnimSwayMultiplier_Shotgun` | 0:0C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 2 | M12G, MP43 |
| `CRV_WeaponAnimSwayMultiplier_LMG_Harsh` | 0:0C 0.005:1.2C 0.01:1.4C 0.02:1.8C 0.025:2.2C 0.1:2.4K 0.25:2.4K 0.5:2.4K | 1 | M249 |
| `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | 0:0C 0.05:1.2C 0.1:4.5C 0.2:4C 0.4:3.3C 0.7:2.7C 1.2:2.2C 2:1.7C 3:1.5K | 4 | MK22, SR_04, SV98, WEPN_035 |
| `CRV_WeaponAnimSwayMultiplier_SMG` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |
| `CRV_WeaponAnimSwayMultiplier_DMR_Moderate` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 1 | RFB |
| `CRV_WeaponAnimSwayMultiplier_DMR_Harsh` | no keys | 1 | SKS |
| `CRV_WeaponAnimSwayMultiplier_DMR_Harsh (variant 13)` | 0:0C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 2 | SVDM, WEPN_034 |
| `CRV_WeaponAnimSwayMultiplier_Snipers_Moderate` | 0:0C 0.05:1C 0.1:4C 0.2:3.6C 0.4:3C 0.7:2.5C 1.2:2C 2:1.6C 3:1.4K | 1 | WEPN_017 |

**`AnimationSwayData.ADSYawSwayMultiplierCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `CRV_WeaponAnimSwayMultiplier_AR_Moderate` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 8 | A91, KH2002, M4, TAR21, WEPN_029, WEPN_030, … |
| `CRV_WeaponAnimSwayMultiplier_AR_Harsh` | 0:-6.41202e-08C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 1 | AK74M |
| `CRV_WeaponAnimSwayMultiplier_Launcher` | 0:0C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `CRV_WeaponAnimSwayMultiplier_Bow` | no keys | 1 | CombatBow |
| `CRV_WeaponAnimSwayMultiplier_Sidearms` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 4 | Glock17, WEPN_026, WEPN_027, WEPN_032 |
| `CRV_WeaponAnimSwayMultiplier_Sidearms (variant 5)` | no keys | 1 | Judge |
| `CRV_WeaponAnimSwayMultiplier_LMG_Moderate` | 0:0C 0.005:0.5C 0.01:0.7C 0.02:1.1C 0.025:1.5C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 2 | LMG_02, WEPN_036 |
| `CRV_WeaponAnimSwayMultiplier_Shotgun` | 0:0C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 2 | M12G, MP43 |
| `CRV_WeaponAnimSwayMultiplier_LMG_Harsh` | 0:0C 0.005:1.2C 0.01:1.4C 0.02:1.8C 0.025:2.2C 0.1:2.4K 0.25:2.4K 0.5:2.4K | 1 | M249 |
| `CRV_WeaponAnimSwayMultiplier_Snipers_Harsh` | 0:0C 0.05:1.2C 0.1:4.5C 0.2:4C 0.4:3.3C 0.7:2.7C 1.2:2.2C 2:1.7C 3:1.5K | 4 | MK22, SR_04, SV98, WEPN_035 |
| `CRV_WeaponAnimSwayMultiplier_SMG` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |
| `CRV_WeaponAnimSwayMultiplier_DMR_Moderate` | 0:0C 0.005:0.3C 0.01:0.5C 0.02:0.9C 0.025:1.3C 0.1:2.1K 0.25:2.1K 0.5:2.1K | 1 | RFB |
| `CRV_WeaponAnimSwayMultiplier_DMR_Harsh` | no keys | 1 | SKS |
| `CRV_WeaponAnimSwayMultiplier_DMR_Harsh (variant 13)` | 0:0C 0.005:0.4C 0.01:0.6C 0.02:1C 0.025:1.4C 0.1:2.2K 0.25:2.2K 0.5:2.2K | 2 | SVDM, WEPN_034 |
| `CRV_WeaponAnimSwayMultiplier_Snipers_Moderate` | 0:0C 0.05:1C 0.1:4C 0.2:3.6C 0.4:3C 0.7:2.5C 1.2:2C 2:1.6C 3:1.4K | 1 | WEPN_017 |

**`AimSwayData.CurveData.AimSwaySpeedCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `AimSway_SpeedCurve_AR` | 0:1C 1:0.92C 1.5:0.9C 3:1.08C 4.5:0.99C 5:0.92C 6:1C | 9 | A91, AK74M, KH2002, M4, TAR21, WEPN_029, … |
| `AimSway_SpeedCurve` | no keys | 2 | AT4, CombatBow |
| `AimSway_SpeedCurve_Launchers` | 0:0.92C 1.4985:0.96C 2.997:1.02C 4.4955:1C 6:0.92C | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `AimSway_SpeedCurve_Pistol` | 0:1C 1.5:1.1C 3:1.2C 4.5:1.1C 6:1C | 4 | Glock17, WEPN_026, WEPN_027, WEPN_032 |
| `AimSway_SpeedCurve_Pistol (variant 4)` | no keys | 1 | Judge |
| `AimSway_SpeedCurve_LMG` | 0:0.95C 1.2:0.88C 1.6:0.86C 3:1.02C 3.6:1.1C 4.2:1.18C 4.6:1.12C 4.9:0.92C 5.2:0.88C 6:0.95C | 3 | LMG_02, M249, WEPN_036 |
| `AimSway_SpeedCurve_Shotgun` | 0:0.92C 1:1.25C 2:1.15C 3:1.13C 4:1.15C 5:1.25C 6:0.92C | 2 | M12G, MP43 |
| `AimSway_SpeedCurve_SR` | 0:0.97C 1:1.08C 2:0.94C 3:1.06C 4:0.93C 5:1.09C 6:0.97C | 5 | MK22, SR_04, SV98, WEPN_017, WEPN_035 |
| `AimSway_SpeedCurve_SMG` | 0:1.1C 1:1.25C 2:1.15C 3:1.13C 4:1.15C 5:1.25C 6:1.1C | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |
| `AimSway_SpeedCurve_DMR` | 0:0.95C 1.5:1.02C 3:0.98C 4.5:1.08C 8:0.95C | 2 | RFB, SVDM |
| `AimSway_SpeedCurve_DMR (variant 10)` | no keys | 2 | SKS, WEPN_034 |

**`AimSwayData.WeaponTranslationStabilizationSway`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `AdsStabilizationTranslation_AR` | X: 0:0C 0.25:-0.002C 0.5:-0.006C 0.75:-0.012C 1:-0.02C | 9 | A91, AK74M, KH2002, M4, TAR21, WEPN_029, … |
| `AdsStabilizationTranslation_Launcher` | X: 0:0C 0.1:0.0125C 0.25:0.075C 0.5:-0.05C 0.75:-0.275C 1:-0.35C | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `AdsStabilizationTranslation_DMR` | X: 0:0C 0.1:-0.005C 0.25:-0.03C 0.5:0.05C 0.75:-0.025C 1:-0.08C | 6 | CombatBow, RFB, SKS, SVDM, WEPN_034, WEPN_035 |
| `AdsStabilizationTranslation_Pistol` | X: 0:0C 0.2:-0.001C 0.4:0.002C 0.6:0.005C 0.8:0.009C 1:0.012C | 5 | Glock17, Judge, WEPN_026, WEPN_027, WEPN_032 |
| `AdsStabilizationTranslation_LMG` | X: 0:0C 0.1:0.05C 0.25:0.3C 0.5:-0.2C 0.75:-1.1C 1:-1.4C | 2 | LMG_02, M249 |
| `AdsStabilizationTranslation_Shotgun` | X: 0:0C 0.2:-0.001C 0.4:0.002C 0.6:0.005C 0.8:0.009C 1:0.012C | 2 | M12G, MP43 |
| `AdsStabilizationTranslation_SR` | X: 0:0C 0.3:0C 0.65:0C 0.7:0.015C 0.75:0.06C 0.8:-0.07C 0.85:-0.28C 0.9:-0.5C 0.95:-0.7C 1:-0.5C | 5 | MK22, SR_04, SV98, WEPN_017, WEPN_030 |
| `AdsStabilizationTranslation_SMG` | X: 0:0C 0.2:-0.001C 0.4:0.002C 0.6:0.005C 0.8:0.009C 1:0.012C | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |

**`AimSwayData.WeaponRotationStabilizationSway`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `AdsStabilizationRotation_AR` | X: 0:-3.31833e-09C 0.15:0.024C 0.35:-0.08C 0.6:-0.24C 0.8:-0.52C 1:-0.72C | 10 | A91, AK74M, KH2002, M4, TAR21, WEPN_029, … |
| `AdsStabilizationRotation_Launcher` | X: 0:0C 0.1:0.0125C 0.3:0.1C 0.6:-0.15C 1:-0.4C | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `AdsStabilizationRotation_DMR` | X: 0:-3.31833e-09C 0.1:-0.04C 0.2:-0.16C 0.4:0.1C 0.8:-0.4C 1:-0.5C | 6 | CombatBow, RFB, SKS, SVDM, WEPN_034, WEPN_035 |
| `AdsStabilizationRotation_Pistol` | X: 0:-3.31833e-09C 0.2:0.02C 0.4:0.08C 0.6:0.16C 0.8:0.25C 1:0.35C | 5 | Glock17, Judge, WEPN_026, WEPN_027, WEPN_032 |
| `AdsStabilizationRotation_LMG` | X: 0:0C 0.1:0.0125C 0.3:0.1C 0.6:-0.35C 1:-0.6C | 2 | LMG_02, M249 |
| `AdsStabilizationRotation_Shotgun` | X: 0:-3.31833e-09C 0.2:0.02C 0.4:0.08C 0.6:0.16C 0.8:0.25C 1:0.35C | 2 | M12G, MP43 |
| `AdsStabilizationRotation_SR` | X: 0:0C 0.3:0C 0.65:0C 0.7:0.15C 0.75:0.4C 0.8:-0.35C 0.85:-1.4C 0.9:-2.7C 0.95:-3.5C 1:-3C | 4 | MK22, SR_04, SV98, WEPN_017 |
| `AdsStabilizationRotation_SMG` | X: 0:-3.31833e-09C 0.2:0.02C 0.4:0.08C 0.6:0.16C 0.8:0.25C 1:0.35C | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |

**`AimSwayData.AdsStabilizationData.AdsAimSwayScaleCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `AdsStabilization_AimSwayScale_LMG` | 0:1.2C 1:0.8C | 2 | LMG_02, WEPN_036 |

**`AimSwayData.AdsStabilizationData.AdsAimSwaySpeedCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `AdsStabilization_AimSwaySpeed_LMG` | 0:1.12C 1:1C | 2 | LMG_02, WEPN_036 |

**`AimSwayData.CurveData.HorizontalAimSwayMovementCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `HorizontalAimSway_MovementCurve_AR` | 0:1.1664e-08C 1:0.02C 1.5:0.035C 3:0C 3.8:-0.0182C 4.3:-0.024C 4.8:-0.035C 5.4:-0.015C 6:1.1664e-08C | 8 | A91, AK74M, KH2002, M4, TAR21, WEPN_029, … |
| `HorizontalAimSway_MovementCurve` | no keys | 2 | AT4, CombatBow |
| `HorizontalAimSway_MovementCurve_Launchers` | 0:-1.94393e-08C 0.999:0.0525C 1.998:-0.02625C 2.997:-0.13125C 3.996:-0.21C 4.662:-0.2625C 5.328:-0.18375C 6:-1.94393e-08C | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `HorizontalAimSway_MovementCurve_Pistol` | 0:-4.6194e-09C 1:-0.035C 2:-0.14C 3:-0.21C 4:-0.28C 5:-0.21C 6:-4.6194e-09C | 4 | Glock17, WEPN_026, WEPN_027, WEPN_032 |
| `HorizontalAimSway_MovementCurve_Pistol (variant 4)` | no keys | 1 | Judge |
| `HorizontalAimSway_MovementCurve_LMG` | 0:4.2458e-08C 1:0.028C 1.5:0.04C 2.2:0.018C 3:0C 3.55:-0.02C 4.05:-0.055C 4.65:-0.075C 5.05:-0.045C 5.45:-0.02C 6:0C | 3 | LMG_02, M249, WEPN_036 |
| `HorizontalAimSway_MovementCurve_Shotgun` | 0:0C 1:0.03C 1.5:0.045C 2.2:0.02C 3:0C 3.8:-0.025C 4.3:-0.045C 4.9:-0.018C 6:0C | 2 | M12G, MP43 |
| `HorizontalAimSway_MovementCurve_SR` | 0:0C 1:0.032C 2:0.006C 3:-0.034C 4:-0.01C 5:0.028C 6:0C | 5 | MK22, SR_04, SV98, WEPN_017, WEPN_035 |
| `HorizontalAimSway_MovementCurve_SMG` | 0:0C 1:0.03C 1.5:0.045C 2.2:0.02C 3:0C 3.8:-0.025C 4.3:-0.045C 4.9:-0.018C 6:-1.33478e-09C | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |
| `HorizontalAimSway_MovementCurve_DMR` | 0:0C 1:0.032C 2:0.006C 3:-0.034C 4:-0.01C 5:0.028C 6:0C | 2 | RFB, SVDM |
| `HorizontalAimSway_MovementCurve_DMR (variant 10)` | no keys | 2 | SKS, WEPN_034 |
| `HorizontalAimSway_MovementCurve_AR (variant 11)` | 0:0C 1:0.02C 1.5:0.035C 3:0C 3.8:-0.0182C 4.3:-0.024C 4.8:-0.035C 5.4:-0.015C 6:0C | 1 | WEPN_037 |

**`AimSwayData.CurveData.VerticalAimSwayMovementCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `VerticalAimSway_MovementCurve_AR` | 0:0C 0.75:0.06C 0.75:0.06C 1.5:0.1C 3:3.35253e-09C 4.5:-0.1C 5.25:-0.06C 6:0C | 8 | A91, AK74M, KH2002, M4, TAR21, WEPN_029, … |
| `VerticalAimSway_MovementCurve` | no keys | 2 | AT4, CombatBow |
| `VerticalAimSway_MovementCurve_Launchers` | 0:0C 0.999:0.06C 0.999:0.06C 1.998:0.09C 2.997:0.015C 3.996:-0.075C 4.662:-0.105C 5.328:-0.045C 6:0C | 4 | CGM4, Launcher_04, MMGL, RPG7 |
| `VerticalAimSway_MovementCurve_Pistol` | 0:-1.79681e-09C 1:0.04375C 1:0.04375C 2:-1.79681e-09C 3:-0.04375C 4:-1.79681e-09C 5:0.04375C 6:-1.79681e-09C | 4 | Glock17, WEPN_026, WEPN_027, WEPN_032 |
| `VerticalAimSway_MovementCurve_Pistol (variant 4)` | no keys | 1 | Judge |
| `VerticalAimSway_MovementCurve_LMG` | 0:0C 0.9:0.05C 0.9:0.05C 1.5:0.085C 2.1:0.08C 3:0C 3.9:-0.05C 4.5:-0.085C 5.1:-0.08C 6:0C | 3 | LMG_02, M249, WEPN_036 |
| `VerticalAimSway_MovementCurve_Shotgun` | 0:0C 0.8:0.045C 1.2:0.06C 1.6:0.052C 3:0C 3.8:-0.045C 4.2:-0.06C 4.6:-0.052C 6:0C | 2 | M12G, MP43 |
| `VerticalAimSway_MovementCurve_SR` | 0:0C 1:0.17C 1:0.17C 2:0.08C 3:0C 4:-0.12C 5:-0.18C 6:0C | 5 | MK22, SR_04, SV98, WEPN_017, WEPN_035 |
| `VerticalAimSway_MovementCurve_SMG` | 0:0C 0.8:0.045C 0.8:0.045C 1.2:0.06C 1.6:0.052C 3:0C 3.8:-0.045C 4.2:-0.06C 4.6:-0.052C 6:0C | 5 | MP9, SMG_03, Vector, WEPN_028, WEPN_031 |
| `VerticalAimSway_MovementCurve_DMR` | 0:0C 1:0.17C 2:0.08C 3:0C 4:-0.12C 5:-0.18C 6:0C | 2 | RFB, SVDM |
| `VerticalAimSway_MovementCurve_DMR (variant 10)` | no keys | 2 | SKS, WEPN_034 |
| `VerticalAimSway_MovementCurve_AR (variant 11)` | 0:0C 0.75:0.06C 0.75:0.06C 1.5:0.1C 3:0C 4.5:-0.1C 5.25:-0.06C 6:0C | 1 | WEPN_037 |

**`AimSwayData.PlayerSpeedStabilizationMultiplierCurve`**

| Curve | Keys (time:value, L linear, C cubic, K constant) | Weapons | Used by |
|---|---|---|---|
| `CF_AimSway_Stabilization_PlayerSpeed` | 0:0.5K 350:1K | 27 | A91, AK74M, CGM4, Glock17, KH2002, LMG_02, … |
| `CF_AimSway_Stabilization_PlayerSpeed (variant 1)` | no keys | 6 | CombatBow, Judge, MP9, SKS, WEPN_029, WEPN_034 |
| `CF_AimSway_Stabilization_PlayerSpeed_SR` | 0:0.5K 350:1K | 4 | MK22, SR_04, SV98, WEPN_035 |
| `CF_AimSway_Stabilization_PlayerSpeed_SR (variant 3)` | no keys | 1 | WEPN_017 |

## 5. Movement accuracy

Movement changes accuracy through the sway system: the horizontal and vertical movement curves scale the sway magnitude with player speed, the player-speed stabilisation curve scales how fast the ADS stabilisation builds while moving, and the ADS stabilisation scalars below set the build and cooldown rates. The curves are listed with the sway curves in 4f and 4g.

| Weapon | Stab. speed rate up | Stab. speed rate down | ADS stabilise time (s) | Cooldown rate | Exit grace period (s) | Cooldown ×, moving | Movement progress penalty | Unnamed +0x124 | Unnamed +0x128 | Unnamed +0x12C |
|---|---|---|---|---|---|---|---|---|---|---|
| `A91` | 6† | 2 | 0.9 | 0.45 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `AK74M` | 6† | 2 | 1.2 | 0.5 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `AT4` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `ArtilleryBarrelTest` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `BuildTool` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `CGM4` | 6† | 2 | 1.75 | 0.7 | 0.15† | 2 | 0.5 | 2.5 | 7 | 7 |
| `CombatBow` | 6† | 1.5† | 1.25 | 5 | 0.15† | 3† | 0.35 | 3† | 0† | 0† |
| `Fists` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `Glock17` | 6† | 2.5 | 0.6 | 0.35 | 0.25 | 1.5 | 0.2 | 2 | 4 | 4 |
| `GrenadeLauncher` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `Judge` | 6† | 1.5† | 1.5 | 0.1 | 0.15† | 3† | 1† | 2 | 4 | 4 |
| `KH2002` | 6† | 2 | 1.1 | 0.5 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `LMG_02` | 8 | 1 | 3.5 | 1 | 0.05 | 4 | 1† | 3.5 | 8 | 8 |
| `Launcher_04` | 8 | 2 | 2 | 0.8 | 0.15† | 2 | 0.5 | 2.5 | 7 | 7 |
| `M12G` | 6† | 2 | 1.1 | 0.55 | 0.2 | 2 | 0.4 | 3† | 0† | 0† |
| `M249` | 8 | 1 | 3 | 1 | 0.05 | 4 | 1† | 3.5 | 8 | 8 |
| `M2Browning` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `M4` | 6† | 2 | 1 | 0.5 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `MK22` | 2 | 0.7 | 0.7 | 2.5 | 0.1 | 6 | 0.8 | 1.15 | 10 | 14 |
| `MMGL` | 6† | 2 | 1.5 | 0.5 | 0.15† | 2 | 0.5 | 2.5 | 7 | 7 |
| `MP43` | 6† | 2 | 1 | 0.6 | 0.2 | 2 | 0.4 | 3† | 0† | 0† |
| `MP9` | 6† | 2 | 0.6 | 0.35 | 0.2 | 1.5 | 0.3 | 2.5 | 5 | 5 |
| `MWSY_001_Heavy_MountedMachineGun` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `RFB` | 6† | 1 | 2 | 0.7 | 0.1 | 3† | 0.8 | 2.5 | 9 | 9 |
| `ROT_02_Weapon_122mm` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `ROT_02_Weapon_30mmCannon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `ROT_03_AttachedMachineGuns` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `ROT_03_Weapon_122mm` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `ROT_04_MountedMachineGun` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `RPG7` | 6† | 2 | 1.5 | 0.6 | 0.15† | 2 | 0.5 | 2.5 | 7 | 7 |
| `SKS` | 6† | 1.5† | 2 | 0.2 | 0.15† | 2 | 0.75 | 2.5 | 9 | 9 |
| `SMG_03` | 6† | 2 | 0.8 | 0.3 | 0.2 | 1.5 | 0.3 | 2.5 | 5 | 5 |
| `SR_04` | 3 | 0.5 | 0.9 | 3 | 0.1 | 6 | 0.8 | 1.1 | 10 | 14 |
| `STN_01_Heavy_MountedMachineGun` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `STN_02_Heavy_MainCannon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `STN_03_Heavy_MainBarrel` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `STN_05_Heavy_MainBarrel` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `SV98` | 1 | 0.6 | 0.8 | 2.5 | 0.1 | 6 | 0.75 | 1.15 | 10 | 14 |
| `SVDM` | 6† | 1 | 1.75 | 0.65 | 0.1 | 3† | 0.8 | 2.5 | 9 | 9 |
| `TAR21` | 6† | 2 | 1 | 0.45 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `TNK_01_Artillery_Weapon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `TNK_01_Heavy_Weapon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `TNK_01_MachineGun_Weapon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `TNK_03_Weapon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `TNK_04_Weapon` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `TankBarrelTest` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |
| `Vector` | 6† | 2 | 0.65 | 0.3 | 0.2 | 1.5 | 0.3 | 2.5 | 5 | 5 |
| `WEPN_017` | 1.5 | 0.6 | 0.7 | 2.5 | 0.1 | 6 | 0.8 | 1.15 | 10 | 14 |
| `WEPN_026` | 6† | 2.5 | 0.75 | 0.4 | 0.25 | 1.5 | 0.2 | 2 | 5 | 5 |
| `WEPN_027` | 6† | 2.5 | 0.9 | 0.5 | 0.25 | 1.5 | 0.2 | 2 | 4 | 4 |
| `WEPN_028` | 6† | 2 | 0.7 | 0.35 | 0.2 | 1.5 | 0.3 | 2.5 | 5 | 5 |
| `WEPN_029` | 6† | 2 | 1.25 | 0.55 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `WEPN_030` | 6† | 2 | 1.35 | 0.55 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `WEPN_031` | 6† | 2 | 0.8 | 0.3 | 0.2 | 1.5 | 0.3 | 2.5 | 5 | 5 |
| `WEPN_032` | 6† | 2.5 | 0.55 | 0.3 | 0.25 | 1.5 | 0.2 | 2 | 4 | 4 |
| `WEPN_033` | 6† | 2 | 1.05 | 0.5 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `WEPN_034` | 6† | 1.5† | 2 | 0.2 | 0.15† | 2 | 0.75 | 2.5 | 9 | 9 |
| `WEPN_035` | 1 | 0.6 | 0.55 | 2.5 | 0.1 | 6 | 0.75 | 1.15 | 10 | 14 |
| `WEPN_036` | 6† | 2 | 4 | 0.05 | 0.1 | 4 | 0.6 | 2 | 6 | 6 |
| `WEPN_037` | 6† | 2 | 1 | 0.5 | 0.15† | 2 | 0.6 | 3† | 6 | 6 |
| `WHL_05_RingMinigun` | 6† | 1.5† | 0.5† | 2† | 0.15† | 3† | 1† | 3† | 0† | 0† |

The three unnamed values sit at `AdsStabilizationData` +0x124, +0x128 and +0x12C; Weapons §5b places +0x128 and +0x12C at the sight-sway translation and rotation length limits.

### 5a. ADS stabilisation curves

`AimSwayData.AdsStabilizationData.AdsAimSwayScaleCurve`: set by 2 assets: LMG_02, WEPN_036.

`AimSwayData.AdsStabilizationData.AdsAimSwaySpeedCurve`: set by 2 assets: LMG_02, WEPN_036.

### 5b. Sight attachments

Sights shift the sway distance and the stabilisation curve multipliers per weapon archetype, and move the camera. An omitted override flag means the weapon's own value applies. Only sights that set at least one override are listed.

| Sight item | Sight | Sway distance offset | Stabilisation multipliers by archetype | Camera offset |
|---|---|---|---|---|
| `ID_10xScope` | `S_Aim01` | 0 (per weapon: Mosin 25, SV98 4.35, MK22 4.35, SR_04 0, SKS -5, SVDM -1.5) | Sniper: translation 1.7, rotation 1.6 | -2 |
| `ID_10xScopeMoa` | `S_Aim01` | 0 (per weapon: Mosin 25, SV98 4.35, MK22 4.35, SR_04 0, SKS -5, SVDM -1.5) | Sniper: translation 1.7, rotation 1.6 | -2 |
| `ID_OPT_08` | `S_Aim01` | — | — | 0 (per weapon: WEPN_036 -3.9) |
| `ID_4xElcanSpectr` | `S_Aim01` | 0 (per weapon: Mosin 27, SV98 8, MK22 6, SR_04 2, SKS -2, SVDM 2, RFB -6, M249 -1.6, LMG_02 0) | Sniper: translation 1.3, rotation 1.3 | 0 (per weapon: WEPN_036 -1.6) |
| `ID_4xElcanSpectr` | `S_Aim02` | — | — | 0 (per weapon: WEPN_036 -1.6) |
| `ID_4xHybrid` | `S_Aim01` | — | — | -5 (per weapon: AK74M 2, SV98 -14.2002, SKS -2.5, M4 -14.2) |
| `ID_6xScope` | `S_Aim01` | — | — | 0 |
| `ID_CantedIrons` | `S_AimCanted1` | — | — | -20 |
| `ID_EotechHoloSight` | `S_Aim01` | — | — | 0 (per weapon: WEPN_036 -7) |
| `ID_SGHT_009` | `S_Aim01` | — | — | 0 (per weapon: SR_04 5, Mosin 5, LMG_02 5) |
| `ID_SGHT_011` | `S_Aim01` | 0 (per weapon: Mosin 25, SV98 4.35, MK22 4.35, SR_04 0, SKS -5, SVDM -1.5) | Sniper: translation 1.4, rotation 1.3 | — |
| `ID_RedDot` | `S_Aim01` | — | — | 0 (per weapon: CGM4 10, MMGL 10, M249 -5, WEPN_036 -2) |
| `ID_SGHT_016` | `S_Aim01` | — | — | 0 (per weapon: WEPN_036 -5) |
| `ID_SGHT_023` | `S_Aim01` | — | — | 0 (per weapon: WEPN_036 -2) |
| `ID_3xScope` | `S_Aim01` | 0 (per weapon: Mosin 31, SV98 11, MK22 10.3, SR_04 6, SKS 1.6, SVDM 6, RFB -3, M249 2.5, LMG_02 4.3, M4 0.7, AK74M 2, WEPN_029 -3, WEPN_030 0) | Sniper: translation 1.2, rotation 1.2 | — (per weapon: M249 -1.85217) |
| `ID_SGHT_026` | `S_Aim01` | 0 (per weapon: Mosin 31, SV98 11, MK22 10.3, SR_04 6, SKS 1.6, SVDM 6, RFB -3, M249 2.5, LMG_02 4.3, M4 0.7, AK74M 2, WEPN_029 -3, WEPN_030 0) | — | 0 (per weapon: M249 0.05) |
| `ID_SGHT_027` | `S_Aim01` | — | — | 0 (per weapon: WEPN_036 -5) |
| `ID_SGHT_028` | `S_Aim01` | 0 (per weapon: Mosin 31, SV98 11, MK22 10.3, SR_04 6, SKS 1.6, SVDM 6, RFB -3, M249 2.5, LMG_02 4.3, M4 0.7, AK74M 2, WEPN_029 -3, WEPN_030 0) | Sniper: translation 1.2, rotation 1.2 | 0.63 (per weapon: M249 0.05, WEPN_036 -0.74) |
| `ID_SGHT_029` | `S_Aim01` | 0 (per weapon: Mosin 31, SV98 11, MK22 10.3, SR_04 6, SKS 1.6, SVDM 6, RFB -3, M249 2.5, LMG_02 4.3, M4 0.7, AK74M 2, WEPN_029 -3, WEPN_030 0) | Sniper: translation 1.2, rotation 1.2 | 1.96878 |
| `ID_SGHT_030` | `S_Aim01` | 0 (per weapon: Mosin 27, SV98 8, MK22 6, SR_04 2, SKS -2, SVDM 2, RFB -6, M249 -1.6, LMG_02 0) | Sniper: translation 1.3, rotation 1.3 | 0 (per weapon: M249 -0.62797, LMG_02 -0.62797, WEPN_036 -1.5) |
| `ID_SGHT_030` | `S_Aim02` | — | — | 0 (per weapon: M249 -0.62797, LMG_02 -0.62797, WEPN_036 -1.5) |
| `ID_SGHT_031` | `S_Aim01` | 0 (per weapon: Mosin 4.35, SV98 4.35, MK22 4.35, SR_04 0, SKS -5, SVDM -1.5) | Sniper: translation 1.4, rotation 1.5 | 3.8 (per weapon: Mosin 3.8) |
| `ID_SGHT_032` | `S_Aim01` | 0 (per weapon: Mosin 25, SV98 4.35, MK22 4.35, SR_04 0, SKS -5, SVDM -1.5) | Sniper: translation 1.7, rotation 1.6 | 2.9 |
| `ID_SGHT_034` | `S_Aim01` | 0 (per weapon: Mosin 31, SV98 11, MK22 10.3, SR_04 6, SKS 1.6, SVDM 6, RFB -3, M249 2.5, LMG_02 4.3, M4 0.7, AK74M 2, WEPN_029 -3, WEPN_030 0) | Sniper: translation 1.2, rotation 1.2 | -1.89162 (per weapon: LMG_02 -27.6722, M249 -27.974) |
| `ID_SGHT_036` | `S_Aim01` | 0 (per weapon: Mosin 25, SV98 4.35, MK22 4.35, SR_04 0, SKS -5, SVDM -1.5) | Sniper: translation 1, rotation 1.2 | 3.8 |
| `ID_SGHT_036` | `S_Aim02` | — | — | 3.8 |
| `ID_SGHT_038` | `S_Aim01` | — | — | -0.8 |
| `ID_SGHT_039` | `S_Aim01` | 0 | Sniper: translation 1.4, rotation 1.5 | 8.5 |
| `ID_SGHT_040` | `S_Aim01` | 0 | Sniper: translation 1.4, rotation 1.5 | 8.5 |

<!-- /spread_recoil_tables -->
