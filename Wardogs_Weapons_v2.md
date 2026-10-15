---
title: "Weapons"
parent: "Content"
---

# Wardogs — Weapons Reference (v2)
*Extracted from cooked game data (JSON export, `Wardogs/Content/Weapons/`, 92 source files). Parsed with a Python script; 15 Input files contain several `--- export:` blocks each and were split on those headers. Numbers are the raw exported values.*

> **Scope note:** this folder holds only **8 weapon stat assets** (`WDWeaponStatsData`). The main rifle, SMG, LMG, shotgun and pistol stat tables are not in this folder. Their aim-sway curves are here, so the stat tables are presumably elsewhere in the dump.

---

## 1. Weapon Stat Assets (`WDWeaponStatsData`)

| Asset | WeaponId tag | Caliber | RPM | Fire modes | Init. bullet speed | Effective range | Max zeroing | Melee dmg |
|---|---|---|---|---|---|---|---|---|
| `DA_SKS_Stats` | `Id.Item.SKS` | `Item.Caliber.762mm` | 420 | SemiAutomatic | 73,500 | 400 | 1,000 | 35 |
| `DA_Judge_Stats` | `Id.Item.Judge` | `Item.Caliber.45Colt` | 200 | SemiAutomatic | 33,500 | 50 | 25 (min 25, step 25) | 20 |
| `DA_AT4_Stats` | `Id.Item.AT4` | `Item.Caliber.84mm` | 100 | SemiAutomatic | 29,000 | 300 | none | none |
| `DA_ArtilleryBarrelTest_Stats` | `Id.Item.ArtilleryBarrelTest` | `Item.Caliber.155mm` | 150 | SemiAutomatic (RoundsPerBurst 1) | 46,400 | 10,000 | 1,000 | 0 |
| `DA_TankBarrelTest_Stats` | `Id.Item.LeapordBarrel` | `Item.Caliber.120x570mm` | 100 | SemiAutomatic | 55,000 | 3,500 | 1,000 | none |
| `DA_M2Browning_Stats` | `Id.Item.BrowningMG` | `Item.Caliber.762mm` | 500 | Automatic | 71,500 | none | 1,000 | none |
| `DA_Fists_Stats` | `Id.Item.Fists` | none | 300 | SemiAutomatic | none | none | none | none |
| `DA_BuildTool_Stats` | `ID.Item.BuildTool` | none | none | none | none | none | none | none |

Notes:
- `DA_BuildTool_Stats` contains only `WeaponId`. Its tag uses `ID.Item.` where every other asset uses `Id.Item.`.
- `DA_TankBarrelTest_Stats` uses the tag `Id.Item.LeapordBarrel` (misspelling of "Leopard" is in the source).
- Units are not stated in the export. Inferred, not confirmed: `InitialBulletSpeed` is in Unreal cm/s (SKS 73,500 cm/s = 735 m/s; AT4 29,000 = 290 m/s), and `EffectiveRange` is in metres (SKS 400 m, Artillery 10 km).

### 1a. Per-weapon details beyond the table

**DA_SKS_Stats** (the most fully specified asset)
| Field | Value |
|---|---|
| WeaponAccuracy | 0.73, `AccuracyType = MinutesOfAngle` |
| FocusEnergyReductionPerShot | 50.0 |
| RecoilReductionWhenFocussing | 30.0 |
| ViewKickCurve | 3 keys: 0→0, 0.15→1, 0.4→0.75 |
| ViewKickMagnitudeMultiplier | 1.1 |
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
| AdsCameraCurve | `CF_DMR_ADS_Curve` |
| AimSway | Persistent=False, CrouchOffsetMultiplier 0.55, ProneOffsetMultiplier 0.35, TotalPatternDuration 6.0, NoFocusEnergySpeedMultiplier 2.5, PlayerCameraOffsetMultiplier 0.75 |
| AimSway stabilisation | AdsStabilizeTime 2.0, CooldownRate 9.0, CooldownRateMovingMultiplier 2.0, MovementProgressPenalty 0.75, ExitGracePeriod 9.0 |
| Animation sway | ADSPitch/Yaw multiplier curves both `CRV_WeaponAnimSwayMultiplier_DMR_Harsh` |

The distance falloff times line up with `EffectiveRange = 400` if the times are in cm (40,000 cm = 400 m). This is consistent with the unit inference above but not proven.

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
| AdsCameraCurve | `CF_Pistol_ADS_Curve` |
| AimSway stabilisation | AdsStabilizeTime 1.5, CooldownRate 4.0, ExitGracePeriod 4.0 |
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
- The LMG has two extra ADS-stabilisation scalars: `AdsStabilization_AimSwayScale_LMG` (1.2 → 0.8) and `AdsStabilization_AimSwaySpeed_LMG` (1.12 → 1.0).

**Shared root curves** (in `Weapons/`): `AimSway_SpeedCurve` (0.5–1.0), `HorizontalAimSway_MovementCurve` (−0.015 – +0.02), `VerticalAimSway_MovementCurve` (−0.2 – +0.15). `ADS_Blur_Curve` goes 0 → 1 over 0–1.

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

## 3. ADS Curves (`Curves/ADSCurves/`)

Eight `CurveFloat` assets, one per class. Each has 3 keys over t = 0–1. They rise from about 0 to 1.0 (the sniper curve starts at exactly 0).

| Asset | Used by (confirmed) |
|---|---|
| `CF_AssaultRifle_ADS_Curve` | no `DA_*_Stats` in this folder reference it |
| `CF_DMR_ADS_Curve` | `DA_SKS_Stats` (`AdsCameraCurve`) |
| `CF_LMG_ADS_Curve` | not referenced here |
| `CF_Launcher_ADS_Curve` | not referenced here |
| `CF_Pistol_ADS_Curve` | `DA_Judge_Stats` (`AdsCameraCurve`) |
| `CF_SMG_ADS_Curve` | not referenced here |
| `CF_Shotgun_ADS_Curve` | not referenced here |
| `CF_SniperRifles_ADS_Curve` | not referenced here |

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

The 25-entry `IMC_BaseWeapon` also binds the `IA_Player_*` actions for Inspect, Holdable Secondary Use and Holdable Primary Use Release.

---

## 5. How Values Combine

The export lists the inputs to each system but not the formulas that combine them. The points below are the likely roles, not confirmed behaviour.

- **Aim sway (likely):** the class speed curve, the horizontal and vertical movement curves, and the `AimSwayData` multipliers (crouch, prone, camera offset, no-focus speed) appear to feed one sway offset. The combination method is unknown.
- **Recoil (likely):** `RecoilPattern` gives per-shot X/Y offsets, `RandomDeviationDegree` adds random deviation, and the post-pattern yaw and pitch ranges add random kick afterwards. `RecoilPatternResetTime` probably controls when the pattern restarts.
- **Distance falloff (SKS):** `DistanceDamageFalloffCurve` is a multiplier indexed by distance. The falloff times are presumably in the same units as `InitialBulletSpeed`.
- **Focus energy (SKS, Judge):** `FocusEnergyReductionPerShot` and `RecoilReductionWhenFocussing` are per-shot values. `NoFocusEnergySpeedMultiplier` is probably a sway-speed scalar used when focus is empty. Neither is confirmed.

---

## 6. Still Not Pulled / Limitations

- The main AR, SMG, LMG, shotgun and pistol **stat tables** are not in this folder. Only their aim-sway and stabilisation curves are here.
- **Units are not stated** in the export. Speeds are assumed to be cm/s and ranges to be metres, based on the falloff-curve and EffectiveRange check. That is an inference.
- `IronSightsAimTime = 50,000` on the tank barrel and `WeaponAccuracy = 70 MOA` look like placeholders or unused tuning. The export gives no way to check.
- Two properties on the SKS and Judge are obfuscated names (`_aaabijhbknckndgboaemo_…` and `_aaacamgpphfkeldlcaboo_…`), so their meaning is unknown. Values: SKS 1.0 and 2.5, Judge 2.0.
- `CF_*_ADS_Curve` and `ADS_Blur_Curve` have no stated output meaning.
- Curve tangents and interpolation modes are not summarised. Only key times and values are reported.
- The M2 recoil pattern has 29 points; the full list is not reproduced.
- Input mapping contexts are shown only for their first key per action. Secondary keys and gamepad alternates are summarised, not listed in full.
