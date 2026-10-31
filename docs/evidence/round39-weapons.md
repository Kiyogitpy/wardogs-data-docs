# Round 39: weapons, ballistics and artillery backlog

GitHub-only page. Agent RE39-WEAP. Inputs: the cooked export in `data/`, the restored executable (static disassembly with capstone and the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__`), the SDK headers. Nothing was run. Statuses: FOUND, NATIVE, SERVER, ABSENT, as in the round 36 brief. Evidence levels: **cooked data read**, **static disassembly**, **static decompiler output (unreviewed)**, **derived**.

Reproduce the data tables with:

```
python -I _tools/weapon_capacity_tables.py --json   # assets/data/weapon-capacity.json (new)
python -I _tools/weapon_damage_tables.py --json     # assets/data/weapon-damage.json (rpm now falls back to 600)
python -I _tools/weapon_damage_tables.py --check
```

A note on "omitted equals default". The export drops every property that equals the class default (round 17). `bUseDistanceDamageFalloffCurve` shows as `true` on 31 of the 61 `WDWeaponStatsData` assets, so true is not the default. `RoundsPerMinute` is shown on 57 of the 61; the four that omit it are the build tool, the LMG_02, the Glock 17 and the mounted [`MWSY_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_001/Content/MWSY_001.json) machine gun, which hold the constructor value 600.

## Weapons and ballistics

### 1. Muzzle velocity of the launchers (9K333 Verba, MAAWS, RPG-7, MGL-40)
**FOUND.** Cooked data read, `WeaponStats.InitialBulletSpeed` (cm/s, confirmed native in item 6):

| Launcher | Item | Stats asset | InitialBulletSpeed | Launch speed | Round |
|---|---|---|---:|---:|---|
| 9K333 Verba | [`Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Launcher_04.json) | [`DA_Launcher_04_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/DA_Launcher_04_Stats.json) | 2000 | 20 m/s | `Id.Item.72mm` |
| MAAWS | `CGM4` | [`DA_CGM4_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_013/Content/Data/DA_CGM4_Stats.json) | 23000 | 230 m/s | `Id.Item.84mm` |
| RPG-7 | [`RPG7`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/RPG7/Content/RPG7.json) | [`DA_RPG7_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/RPG7/Content/Data/DA_RPG7_Stats.json) | 10000 | 100 m/s | `Id.Item.93mm` |
| MGL-40 | `MMGL` | [`DA_MMGL_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_012/Content/Data/DA_MMGL_Stats.json) | 7500 | 75 m/s | 40mm (6-round magazine) |

These are the speed at the muzzle. The rockets have `ThrustSpeed` and fuel (Projectile Flight section 6), so the cruise speed of the Verba is not 20 m/s. Not run. All four are in `assets/data/weapon-capacity.json`.

### 2. Effective range in play (MP43, Scout Rifle TD, AMP-9, Deagle, 9K333, MAAWS, MGL-40, RPG-7)
**Values FOUND; in-play meaning NATIVE (partial).** `EffectiveRange` (metres): Verba 1000, MAAWS 400, MGL-40 400, RPG-7 300, Scout Rifle TD ([`WEPN_035`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/WEPN_035.json)) 300. The MP43, AMP-9 ([`MP9`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/MP9/Content/MP9.json)) and Deagle ([`WEPN_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_027/Content/WEPN_027.json)) assets omit it, so they hold the struct constructor default **100 m** (`0x699E6C0`, stats `+0xDA4`, `0x42C80000`; `_tools/weapon_stats_defaults.py`).

What the game does with it (static disassembly and decompiler output, not run): the getter `0x6BBD420` returns `EffectiveRange x 100`. The weapon-component spawn routine `0x6B747F0` multiplies that by the ammo's `EffectiveRangeMultiplier` (projectile stats `+0x200`, read through `GetProjectileStats(projectile, ammoTag)` `0x6BBA900`) and stores it in the spawn request; the infantry fire path `0x6F1DDC0` stores the plain `x 100` value. The only consumer found for that request field is the wind ramp distance `X` (Projectile Flight section 6.4, inferred). No damage code reads `EffectiveRange` (round 25). The Itemsmith "Range" display stat was not traced to this field. So in play it is, as far as found, a wind and display value, not a damage cutoff. Section "Applier tag map" in item 7 gives the field map.

### 3. Standard magazine size (MP43, Scout Rifle TD, 9K333, MAAWS, RPG-7)
**FOUND.** Cooked data read, `MaxSlotAmountStackSize` of the loaded-round container (inferred meaning, Items v2 section 2a):
- MP43: no magazine container; the chamber container holds **2** (`Item.Caliber.12g`). The unused [`ID_MP43_Mag_Internal`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Shotgun/MP43/Content/Data/ID_MP43_Mag_Internal.json) (`Id.Item.MP43Magazine`) also holds 2.
- Scout Rifle TD ([`WEPN_035`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/WEPN_035.json)): no magazine container; chamber holds **1**, default `Id.Item.556mm.Tracer`.
- 9K333 Verba: chamber **1** (`Id.Item.72mm`, default loaded); [`ID_Launcher_04_Mag_Standard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/ID_Launcher_04_Mag_Standard.json) holds 1 but the weapon has no magazine container.
- MAAWS (`CGM4`): chamber **1** (`Id.Item.84mm`). RPG-7: chamber **1** (`Id.Item.93mm`). MGL-40 (`MMGL`): `Id.Item.MMGLMagazine` **6**.

### 4. Rate of fire for the PKM (LMG_02) and Glock 17 (GGX 17)
**FOUND (value native).** [`DA_LMG_02_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/Data/DA_LMG_02_Stats.json) and [`DA_Glock17_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_010/Content/Data/DA_Glock17_Stats.json) omit `RoundsPerMinute`; the constructor default is **600** (static disassembly `0x699E6C0`, dword `0x44160000`, struct `+0x138`; the Blueprint copy of the struct also exports 600). The shot interval is `59.999996 / RPM` s (start-fire `0x6B980A0`), 0.1 s for both. Nothing rewrites the value after `InitWeapon` (rounds 18, 20, 26 searches). Applied: `weapon_damage_tables.py` now uses 600 with `rpm_source = class_default_native` for both (`assets/data/weapon-damage.json`); `assets/data/weapon-capacity.json` carries it too. Not run. The vehicle weapons' rate belongs to another agent.

### 5. Rate of fire fill and rewrite path
**NATIVE.** No new evidence this round; rounds 18, 20 and 26 stand (`InitWeapon` slot 171 `0x6B96720` is the only writer of the component copy at `+0x140`; no scanned instruction rewrites `+0x278`). Dispatch stubs of the protection layer were not devirtualized.

### 6. Units of weapon speed, effective range, accuracy and deviation
**FOUND (native).** `InitialBulletSpeed` cm/s (launch velocity = unit direction x `0x6BBD500`, Projectile Flight section 2); `EffectiveRange` metres (`0x6BBD420` multiplies by 100.0); `WeaponAccuracy.AccuracyValue` in the unit of `AccuracyType` (0 MOA, 1 milliradian, default 1; getter `0x6BBD3D0`, Weapon Spread section 3); `RandomDeviationDegree` degrees (recoil field, Weapon Spread section 10). `IronSightsAimTime` read as seconds and the zeroing ranges as metres are still inferences. Data pages updated: `content/Wardogs_Weapons_v2.md`.

### 7. Native per-ammo speed modifiers for tracer, HP and AP
**FOUND: none exist.** The applier `0x6BBAB70` has a branch for `Projectile.Attributes.TypicalSpeed` (field `+0x1FC`), but the five `DA_AmmoModifier_*` assets carry only four keys: PenetrationEffectivenessMultiplier, EffectiveRangeMultiplier, TracerChance, PenetrationExitSpeedMultiplier. The infantry fire path `0x6F1DDC0` calls `GetProjectileStats` with the empty tag global `0xD2692F8` (never written; `0x6BBA900` returns the base stats for tag 0). So the base projectile asset is what flies. Static; not run.

Applier tag map (22 attributes; tag registration functions plus the applier body): BaseDamage `+0x30`, ExplosiveRadius `+0x34`, MinimumExplosiveDamage `+0x38`, EffectiveExplosiveRadius `+0x3C`, ExplosiveDamageFallOff `+0x40`, Length `+0x68`, Diameter `+0x6C`, Mass `+0x70`, DragModelValue `+0x78`, TypicalSpeed `+0x1FC`, EffectiveRangeMultiplier `+0x200`, PenetrationEffectivenessMultiplier `+0x208`, ThrustSpeed `+0x2B0`, Suppression BaseValue `+0xB8`, DistanceFalloff Min `+0xBC` and Max `+0xC0`, FriendlySafeRadius `+0x150`, FriendlyMultiplier `+0x154`, TravelDistanceWhizBy `+0x2D4`, DistanceToPlayerWhizBy `+0x2D8`, TracerChance `+0x1F4` (assigned), PenetrationExitSpeedMultiplier `+0x20C`.

### 8. Contents of the `AmmoModifiers` data assets
**FOUND.** Already tabulated (round 25 and Game Mechanics section 2e). ArmorPiercing: penetration 1.8, range 1.2, exit speed 0.0. ArmorPiercing.Tracer: 1.76, 1.2, 0.0, tracer 1.0. HollowPoint: 0.1, 0.8, 0.15. HollowPoint.Tracer: 0.1, 0.8, 0.15, tracer 1.0. Tracer: 1.0, 1.0, 0.075, tracer 1.0. [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) maps the five tags. `DefaultGameplayTags.ini` also registers `Meta.Damage.AmmoModifier.FMJ` ("Testing"), which has no asset. Cooked data read.

### 9. `ArmourPiercing` item tag (.338 Norma AP)
**FOUND.** The items are `Id.Item.338Nor.ArmourPiercing` and `...ArmourPiercing.Tracer` (British spelling, files `ID_338Nor_ArmorPiercing*.json`); the map key is `Meta.Damage.AmmoModifier.ArmorPiercing`. The last-name lookup cannot match, so they behave as FMJ. No weapon chambers .338 Norma (no `SupportedCaliber` of any exported stats asset contains it). Cooked data read; the lookup itself is the documented rule (Damage Pipeline 7.9).

### 10. `545mm.Tracer` has no `Item.Ammo` context
**FOUND by data; native check NATIVE not located.** `Id.Item.545mm.Tracer` has `Item.Caliber.545mm`, `Item.Ammo.Type.FMJ.Tracer`, `Item.Ammo.Type` and `Item.Context.ForceToStorage` but not `Item.Ammo`. All 69 magazine `Item.Ammo` containers use an allow list on `Item.Caliber.*` context only (none tests `Item.Ammo`), and the AK74M standard 30-round and extended 60-round magazines list `Id.Item.545mm.Tracer` as their default content. By the data it loads.

### 11. Do containers load an item without `Item.Ammo`; which spawns offer ammo
**FOUND (data) / NATIVE (load code not located).** See item 10. Spawn and vendor availability: `assets/data/ammo-availability.json` (round 24).

### 12. Which vehicle weapons load which caliber
**FOUND.** `SupportedCaliber` of each vehicle weapon stats asset. 7.62x51 mm (`308Win`): `DA_ROT_03_AttachedMachineGuns`, `DA_ROT_04_MountedMachineGun`, `DA_TNK_01_MachineGun_Weapon`, `DA_WHL_05_RingMinigun`. 20x102 mm: `DA_STN_02_Heavy_MainCannon`. 30 mm: `DA_ROT_02_Weapon_30mmCannon`. 35x228 mm: `DA_TNK_03_Weapon`. .338 Norma: none. 120x570: `DA_TankBarrelTest`, `DA_TNK_01_Heavy_Weapon`. 120x800: `DA_STN_03_Heavy_MainBarrel`. 125x570: `DA_TNK_04_Weapon`. 122 mm: `DA_ROT_02_Weapon_122mm`, `DA_ROT_03_Weapon_122mm`. 155 mm: `DA_TNK_01_Artillery_Weapon`, `DA_ArtilleryBarrelTest`. `DA_MWSY_001` 50Cal, `DA_STN_01` 72mm, `DA_STN_05` DroneProjectile, `DA_M2Browning` 762mm. Cooked data read.

### 13. Projectile step length
**FOUND.** `SimulationFrameRate` 30 (class default `0x6F2A600` and `DefaultGame.ini` line 303), so the step is `floor(1000/30)` = 33 ms (round 23, Projectile Flight section 3; re-checked). The 1 ms model step stays an approximation; WeaponDamage Limitations updated.

### 14. Hit limit past hit 33; exit deflection
**Hit limit FOUND (static disassembly).** `0x6F354DD`-`0x6F35516`: `movzx ecx, word [rdi+0x11A]` (ricochet) or `[rdi+0x11C]` (penetration), `movzx eax, word [rdi+0x118]` (hit counter), `bts ecx, eax`, `mov word [...], cx`; `inc word [rdi+0x118]` at `0x6F3551D`. `bts r32, r32` takes the bit offset modulo 32: hits 1-16 set bits 0-15; hits 17-32 set bits that the 16-bit store drops; hit 33 sets bit 0 again. The old "32-bit bitmap, hits 2 to 33" reading was wrong. No cap on hits was found. **Exit deflection: NATIVE**, not advanced (distribution parameters are in Hit Registration 4.4/4.6: angle 0 to 7.5 degrees, penetration range 5.0/0.5).

### 15. Ricochet reflection, deflection and ratio gate
**NATIVE.** Not advanced; still unreviewed pseudocode (round 25).

### 16. Exit-speed setting and the 0.8 / 1.2 range multipliers
**FOUND / NATIVE partial.** Exit-speed multiplier lands in projectile stats `+0x20C` and is read by the penetration step `0x6F36190` as `new velocity = old x (1 - thickness/capacity) x clamp(1 - 0.5(p + s), 0, 1)` (Hit Registration 4.4). The 0.8/1.2 multiply `EffectiveRange x 100` in the spawn request (item 2). Consumer of that request field beyond the wind ramp: not found.

### 17. Wall thickness unit, density, surface type of world meshes
**ABSENT** (unchanged). No physical-material assignment for world meshes in the export; unit not searched further.

### 18. Odd damage numbers (Scout Rifle TD 73.9 vs M4 27.3)
**FOUND (static).** Both start at base 28 and take entries 5, 138 and 140. Entry 5 is the bone-damage custom operation; [`DT_InfantryData_BoneDamageModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json) row `Weapon.Sniper` gives 2.64 on Torso.Upper, `Weapon.AR` 0.974 (28 x 2.64 = 73.9; 28 x 0.974 = 27.3). `weapon_damage_tables.py --check` passes. Whether the developers intend a sniper-class multiplier on a 5.56 mm rifle is not in the files.

### 19. Shotgun pellet pattern replaced by M500 chokes
**FOUND.** The replacement is in the attachment fragment (`WDInventoryFragment_Attachment.AttachmentData.ShotgunData`). [`ID_MUZL_044`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_044/Content/Data/ID_MUZL_044.json) Improved Cylinder Choke: ChokeFactor 0.65, OuterConeHalfAngle 1.36 deg, RandomConeHalfAngleRange 0 to 1.75, InnerConeHalfAngleMultiplier 0.55. [`ID_MUZL_045`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_045/Content/Data/ID_MUZL_045.json) Full Choke: 0.85, 0.95 deg, 0 to 1.55, 0.6. M500 base ([`DA_M12G_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_011/Content/Data/DA_M12G_Stats.json)): 0.5, 1.56, 0 to 2.0, inner 0.5. These are the only 2 of 56 attachments with the field that set `bOverrideShotgunData` true. The Full Choke narrows the outer cone from 1.56 to 0.95 degrees. Native selection `0x6B98980` is documented (Weapon Spread 11).

### 20. Shotgun curve enable flag (M500, MP43)
**FOUND (derived).** `bUseDistanceDamageFalloffCurve` is omitted on both; since 31 other assets show it true, the default is false, so the stored three-key curve is not applied. Matches the model.

### 21. Muzzle [`ID_MUZL_064`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_064/Content/Data/ID_MUZL_064.json)
**FOUND.** Display name "WEPN_033 (M14) standard muzzle". `AppliedEffects` is a list with one `null` entry, so no stat effect. It carries the suppressor cue (`Attachment.Cue.Suppressor`) and flash scale 0.2, identical to 20 suppressor entries. It changes sound context and flash only, by the tags.

### 22. Attachments whose data names no effect
**FOUND (counts) / NATIVE (code).** 149 of 298 attachment fragments list no effect: grips 21/32, handguards 25/25, magazines 23/69, muzzles 1/56 (this one), sights 1/29, stocks 37/37, barrels 41/41, bipods 0/9. Magazine capacity acts through data (the container stack, item 3), not an effect. Whether stocks, barrels and handguards act through code: not traced.

### 23. Obfuscated magazine floats (`+0x68`, `+0x6C`)
**NATIVE.** Not advanced this round; consumer found earlier (AttachmentsPlatforms "Obfuscated magazine fields").

### 24. Unused slot archetypes (`MountLeft`, `MountRight`, `MountTop`, `MountUnder`, `Underbarrel`)
**FOUND (data).** Scan of all `ID_*` items: no weapon container has a `Mount*` identifier and no attachment item carries a `Mount*` context. `Underbarrel` is used: 36 weapon containers, 19 foregrip items. Native use of the four unused ones not traced.

### 25. Pistol grip and M4 grip recoil value 0 versus in-game feel
Skipped: needs a live game.

### 26. Sight ADS zoom to on-screen magnification
**NATIVE** (not resolved). The value is `FWDSightData.AdsZoomMultiplier` (SDK `WDGame_structs.hpp`, struct offset `+0x370`, with `AdsTransitionData` at `+0x374`, `DefaultCycleSightTransitionData` and a per-sight tag map). The camera FOV consumer was not located in the time-box. Searched: SDK structs, attribute docs, weapon stats FOV fields (`FOVShiftingType` Curve or Constant, `FOVShiftDeltaAmount` -3.0 on some, `FOVShiftDuration` 0.15/0.45).

### 27. Sight multiplier path (`+0x3D0`) and the caller near `0x8633CD4`
**NATIVE.** Not advanced.

### 28. `IronSightsAimTime` 50,000 and `WeaponAccuracy` 70 MOA on the tank barrel
**FOUND (data), meaning inferred.** The asset is [`DA_TankBarrelTest_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/TankBarrelTest/Data/DA_TankBarrelTest_Stats.json) of [`ID_TankBarrelTest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Launcher/VehicleBarrelLaunchersTests/ID_TankBarrelTest.json) ([`Items/Weapons/Launcher/VehicleBarrelLaunchersTests`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Weapons/Launcher/VehicleBarrelLaunchersTests)); no other exported asset references the item or the stats asset. It has authored rate (100), speed (550 m/s) and range (3500 m) but aim time 50000 and 70 MOA: inert test values, not checked in code.

### 29. ADS, recoil, sway and falloff curve outputs; 7 `CurveFloat` objects
**FOUND (shapes), meaning partly inferred.** The seven `CF_*_ADS_Curve` (Assault Rifle, DMR, LMG, Launcher, Pistol, SMG, Shotgun) are identical three-key curves: (0, 0), (0.294, 0), (1, 1); [`CF_SniperRifles_ADS_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Curves/ADSCurves/CF_SniperRifles_ADS_Curve.json): (0, 0), (0.5, 0), (1, 1). Read as a 0 to 1 ADS progress remap with a dead zone of 29.4 percent (50 percent for snipers); the axis meaning is inferred. [`ADS_Blur_Curve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/ADS_Blur_Curve.json): (0, 0), (0.4, 0), (1, 1). The aim-sway curves per class (`AimSway_SpeedCurve_*`, `Horizontal/VerticalAimSway_MovementCurve_*`, `AdsStabilization_AimSwayScale/Speed_LMG` 1.2 to 0.8 and 1.12 to 1.0) have a 0 to 6 time axis; speed curves oscillate between 0.86 and 1.25, movement curves between -0.28 and 0.17. Output units not confirmed.

### 30. [`DA_GunsmithExpandedAccuracy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Shared/Stats/ExpandedStats/Data/DA_GunsmithExpandedAccuracy.json) large-MOA bands
**FOUND.** `LargeMOAValueBands` 5, 10, 15, 20, 25; `SmallMOAValueBands` 1 to 5; `MaxMOAValue` 25; `MOASmallValueLimit` 5. Gunsmith v2 section 9b updated.

### 31. Aim sway in the view rotation (`+0x840`), `bSpawnProjectileFromCameraWhenAds`
**NATIVE.** Not advanced.

### 32. `MaxPelletCount` and the inner-pellet probability `P`
**FOUND.** `MaxPelletCount` = **16** (`DefaultGame.ini` `ProjectileSystemSettings`, found in round 23, Hit Registration 4.6; the spread page said "not in the export"). `P = clamp(N/16) x AmmunitionFactor x ChokeFactor` with N = 8 and AmmunitionFactor 0.8 (7mm Buckshot): M500 **0.20**, MP43 **0.14**, M500 Improved Cylinder **0.26**, M500 Full Choke **0.34**. Weapon Spread 11 and 14 updated.

### 33. Airborne spread
**FOUND.** `InAirHipFireSpread` native default **10.0 degrees** (`0x41200000` at `0x6C9102D`, stats data `+0x1DC`); only [`GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) sets it (10.0); `SpreadMultiplier` is not applied on the airborne path (Weapon Spread 5 and 6, round 23). The weapon wiki pages already print 10.0.

### 34. `ZeroTable` (`+0xFF8`)
**NATIVE.** Not advanced.

### 35. Muzzle-speed scale `component+0x114`
**NATIVE.** Not advanced (applied to the pellet speed in the shotgun path, Weapon Spread 11).

### 36. Mounted and vehicle weapon spread (`+0x2BC`)
**NATIVE.** Not advanced.

### 37. `srand` seed and call site `0x46CF6E8`
**NATIVE (partial).** `0x46CF6E8` is `call [IAT]` with `ecx = ebx` in the engine start-up block; just before, two platform calls write a dword to `[rsp+0x38]` (at `0x46CF6BE` and `0x46CF6CD`), `ebx` gets the first and `edi` the second, and `edi` goes to the engine seeder `0x1415C48B0`. So the seed comes from a platform call and is not a constant in the image. The alternative branch at `0x46CF6D9` loads `r15d` into both (a fixed-seed switch is the likely reading; its value and trigger were not traced). Static disassembly; the platform call was not identified by name.

### 38. Frame `+0x270` echo; snapshot `0x6C9DB60`
**NATIVE.** Not advanced.

### 39. AI shooters
**FOUND / ABSENT.** `AEB_EnemyAccuracyScaling` is an audio-event behaviour (strings `EnemyAccuracyScaling_Vehicle` in the vehicle weapon fire events), not an accuracy value. `AIWeaponData` on 12 stats assets holds only `MinAIRange`, `MaxAIRange` (150 to 650) and `ShootCountOfBurst` (1 to 8); LMG 8, rifles 3, snipers and SVDM 1. No AI-specific spread exists (round 36 AI). The direction path for AI shots was not traced.

### 40. Per-shot bloom
**NATIVE** (negative, not exhaustive). Not advanced.

### 41-47. Hit registration O-1, O-2, O-4, O-5, O-6/O-7, O-8, O-10 and the `IgnoreInstigatorVehicleTime` length
**NATIVE.** Not advanced. Searched this round: the hit-history bitmap code only (item 14), which touches O-6 only in that the `inst+0x130` array is not the bitmap.

### 48. Bullet `MaxProjectileLifetime`
**FOUND.** The projectile stats constructor `0x699DEE0` stores 10.0 s at `+0x188` (`0x41200000`, `0x699E09B`). None of the bullet projectile assets sets the property (only the 70/72/120/125/155 mm shells, arrows and the drone do), so bullets live 10 s. The round 25 model caps flight at 12 s, so it runs 2 s past the game's limit (rows marked `not_reached_in_model` are beyond what the game flies, not just beyond the model). Projectile Flight section 2 updated.

### 49. Speed scale after drag in the damage tables
**NATIVE / model task**, not done. The drag model is documented; applying it in `weapon_damage_tables.py` was out of scope.

### 50. Pilot and tank helmets, two vests or helmets together
**FOUND (data).** Each helmet item carries its own `Meta.Damage.Helmet.<Class>` tag (Pilot, Tank, Light, Medium, Heavy, SuperHeavy, and the Ghillie ones) and all list the single slot context `Inventory.Slot.Helmet`; vests list `Inventory.Slot.Vest`, body armor `Inventory.Slot.Armor`. One item per slot is the data's structure. The armor rule matching through the parent tag is still not tested in a hit.

### 51. Explosive and radial hits ignore coverage
**NATIVE** (round 8). Not advanced.

### 52. Weapon-skin and paint rules
**FOUND (partial).** Which weapons a skin has an override for (`CPD_Overrides` keys of `WDSkinDataAsset`): [`Skin_ChocolateChip`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_ChocolateChip.json) 56 entries (35 of the 37 weapon items; not [`WEPN_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/WEPN_031.json), [`WEPN_035`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/WEPN_035.json)), [`Skin_DigitalWood`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_DigitalWood.json) 46 (29 weapons), [`Skin_TwoTone_Desert`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_TwoTone_Desert.json) 8 (7 weapons), [`Skin_BlackAndGold`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_BlackAndGold.json) 3 (2), and the three Supporter skins 1 each. Whether a weapon without an override can wear the skin (the `DefaultCPD` exists), mastery gating and cost are not in these assets; the cost belongs to the economy data.

### 53. Ammo packing: native consumer of the combine-loose map and default
**NATIVE.** Not advanced.

### 54. Ammo packing: tag parent search for `Id.Item.556mm.Tracer`
**NATIVE.** Not advanced. Data support from item 10: all magazine containers allow by caliber context; the tracer items are `Item.Caliber.556mm` members.

### 55. Ammo packing: extraction and load curves, output unit
**NATIVE.** Not advanced.

### 56. Aim assist target-data struct `FBHAimAssistTargetData`
**NATIVE.** Not advanced (Dumper-7 cannot resolve the fields).

### 57. Aim assist pull modes per asset
**NATIVE.** Not advanced.

## Artillery

### A1. Mil convention of the in-game dial and calculator
**NATIVE.** Not advanced (needs HUD code).

### A2. Hull pitch added to the commanded elevation
**NATIVE.** Not advanced.

### A3. Does the Standard 155 mm fly with `DragModel.Value` 80
**NATIVE.** Not advanced beyond Projectile Flight section 8.

### A4. Low arc needs 40 to 60 mil more than the high arc
**NATIVE** (model mismatch). Not advanced.

### A5. SPH-2 range-table mil value versus dial
**NATIVE.** Not advanced.

### A6. Zero of the sight's mil scale
**NATIVE.** Not advanced.

### A7. How `TypicalSpeed`, `ThrustSpeed`, `Mass`, `DragModel` and `MaxProjectileLifetime` enter the mover
**NATIVE (partial).** New: the applier field map and the `MaxProjectileLifetime` constructor default (items 7 and 48). `MaxProjectileLifetime` of the 155 mm shells is 40 s (data). The mover's use of the others: Projectile Flight sections 3 to 7.

### A8. Constructor defaults for artillery speed limits, drag and gravity scale
**NATIVE.** Not advanced.

### A9. `BP_155mm_Standard` and `BP_155mm_Expensive` mover mode and Blueprint
**NATIVE (partial).** Not advanced.

### A10. Gravity override volumes
**NATIVE.** Not advanced.

### A11. L81 mortar -300 mrad row travel time (20.0 s)
**FOUND (data).** The table is `ArtilleryRangeData` in [`WE_STN_03_Heavy_MainBarrel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/Weapons/WeaponExtensions/WE_STN_03_Heavy_MainBarrel.json). The -300 row is `ImpactDistance` 578, `TravelTime` 20.0; the rows around it are 17.86 (-350) and 19.02 (-250), and every row except -300 and +300 (22.0) has two decimals. A smooth value would be about 18.4. So the 20.0 (and the +300 row's 22.0, which also breaks the trend from 22.39) look like hand-entered round numbers. Cause of the entry still not stated by the files.

### A12. SPH-2 hull tilt and levelling
**NATIVE.** Not advanced.

## Counts

Weapons and ballistics (57 items) plus Artillery (12 items) = 69.

| Status | Items |
|---|---:|
| FOUND (including FOUND with a NATIVE part) | 31 |
| NATIVE (partial or not advanced) | 36 |
| ABSENT | 1 |
| SERVER | 0 |
| Skipped (needs a live game) | 1 |

FOUND: 1, 2 (values), 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14 (hit limit), 16 (partly), 18, 19, 20, 21, 22 (counts), 24, 28, 29, 30, 32, 33, 39, 48, 50, 52 (partial), A11 and A7 (partial). NATIVE: 5, 15, 23, 26, 27, 31, 34 to 38, 40 to 47, 49, 51, 53 to 57, A1 to A6, A8 to A10, A12, and the native halves above. ABSENT: 17. Skipped: 25.

## Files changed

`docs/evidence/round39-weapons.md` (this page); new `_tools/weapon_capacity_tables.py` and `assets/data/weapon-capacity.json`; `_tools/weapon_damage_tables.py` and `assets/data/weapon-damage.json` (rpm 600 fallback); `game-features/Wardogs_WeaponDamage_v1.md`, `Wardogs_AttachmentsPlatforms_v1.md`, `Wardogs_GameFeatures_Gunsmith_v2.md`; `pipelines/Wardogs_WeaponSpread_v1.md`, `Wardogs_ProjectileFlight_v1.md`, `Wardogs_HitRegistration_v1.md`; `content/Wardogs_Weapons_v2.md`.

## Wiki updates

- `_wiki/weapons/9k333-verba.md` -> Muzzle velocity: not yet known -> 20 m/s (launch speed, rocket thrust follows); Effective range: not yet known -> 1000 m; Standard magazine: not yet known -> 1 rocket (chamber, 72mm). Stats section sentence "Launcher stats beyond the fire rate are not in the data pages" -> remove.
- `_wiki/weapons/maaws.md` -> Muzzle velocity -> 230 m/s; Effective range -> 400 m; Standard magazine -> 1 round (84mm); same sentence removed.
- `_wiki/weapons/rpg-7.md` -> Muzzle velocity: not yet known -> 100 m/s; Effective range -> 300 m; Standard magazine -> 1 round (93mm); same sentence removed.
- `_wiki/weapons/mgl-40.md` -> Muzzle velocity -> 75 m/s; Effective range -> 400 m; add magazine 6 rounds.
- `_wiki/weapons/mp43.md` -> Effective range: not yet known -> 100 m (the data omits it, so this is the game default); Standard magazine: not yet known -> 2 shells (internal, no swappable magazine).
- `_wiki/weapons/scout-rifle-td.md` -> Standard magazine: not yet known -> 1 round (single-shot, chamber only, loaded with 5.56 tracer by default); Effective range stays 300 m.
- `_wiki/weapons/amp-9.md` and `_wiki/weapons/deagle.md` -> Effective range: not yet known -> 100 m (game default, the data omits it).
- `_wiki/weapons.md` -> launcher table: fill the three columns above; drop "launcher stats beyond the fire rate are not in the data pages".
- `_wiki/weapons/pkm.md`, `_wiki/weapons/ggx-17.md` -> Fire rate "600 rounds/min (class default)" -> "600 rounds/min (the game default; the weapon's data does not set it)". Fire interval 0.1 s. Note: `_tools/wiki_weapons.py` reads `rpm` from `weapon-damage.json`, which now holds 600 for both, so it would drop the "(class default)" suffix unless the writer keys on `rpm_source`.
- `_wiki/game-mechanics/ballistics.md` (line 29) -> "effective range ... in-play meaning not known" -> the game multiplies it by 100 for the spawn request, scales it by 1.2 (armor piercing) or 0.8 (hollow point), and the only consumer found is the wind ramp; it is not a damage cutoff (the damage falloff comes from the weapon's curve). Bullets expire after 10 s.
- `_wiki/game-mechanics/penetration-and-ricochet.md` (line 44) -> "how the game uses the 0.8 and 1.2 multipliers" -> they scale the effective range value in the shot's spawn request; they do not change speed. Armor piercing sets exit speed to 0 and hollow point to 0.15, tracer 0.075. "What is not yet known" list: drop the exit-speed and multiplier entries.
- `_wiki/game-mechanics/hit-registration.md` -> "Hits a single bullet's history can record: 33" -> the history keeps the first 16 hits; hits 17 to 32 are not recorded and hit 33 overwrites the first slot. No limit on the number of hits exists.
- `_wiki/weapons/attachments-muzzle-devices.md` (line 36) -> "replacement pattern values are not in the data" -> Improved Cylinder Choke: tighter cone (outer half-angle 1.36 degrees vs 1.56 base, more pellets in the inner cluster: 26 percent vs 20); Full Choke: 0.95 degrees, 34 percent. Also [`ID_MUZL_064`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_064/Content/Data/ID_MUZL_064.json): M14 stock muzzle with suppressed-sound cue, no stat effect.
- `_wiki/game-mechanics/spread-and-recoil.md` (line 29) -> "Air. ... size is not yet known" -> 10 degrees half-angle hip spread for every weapon (only the grenade launcher sets it, also 10), and the stance and speed multiplier does not apply while airborne. Shotguns line: add "Part of the 8 pellets cluster: probability 0.20 on the M500 and 0.14 on the MP43 (0.26 and 0.34 with the Improved Cylinder and Full Choke)."
- `_wiki/weapons/attachments-sights-and-optics.md` -> no change (zoom mapping still unknown).
- `_wiki/weapons/attachments-magazines.md` -> optional: "23 change nothing in the data" is correct; capacity comes from the magazine's container, not an effect.
- `_wiki/equipment/l81-mortar.md` (line 69) -> add: the -300 row's 20.0 s is a round number among two-decimal values (the +300 row is 22.0 too), so it is a hand-entered entry; a smooth value would be about 18.4 s.
- `_wiki/weapons/attachments-grips.md`, `_wiki/guides/aiming-the-sph-2.md`, `_wiki/game-mechanics/artillery.md` -> unchanged (items skipped or not advanced).
