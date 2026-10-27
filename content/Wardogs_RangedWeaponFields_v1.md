---
title: "Ranged Weapon Item Fields"
redirect_from: ["/Wardogs_RangedWeaponFields_v1.html", "/Wardogs_RangedWeaponFields_v1"]
parent: "Weapons & Ammo"
description: "Per-weapon rechamber flags and delays, iron-sight and sight offsets, fire-animation blend values, trace radius, and the crosshair override on holdable tools"
---

# Wardogs - Ranged Weapon Item Fields

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) - [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

The item-level settings that sit next to a weapon's stats asset: the `WDItemExtensionData_RangedWeapon` block of each weapon item and the crosshair override of the `WDItemExtensionData_Holdable` block. Nothing here was measured in the game. Labels: **Data** for what the export says, **Not traced** where no reader of the field was found.

A dash means the item does not set the field (an exported asset leaves out every property that equals the class default). Spread, recoil and sway values are on [Weapon Spread and Recoil Data](Wardogs_WeaponSpreadRecoilData_v1.md); attachment effects are on [Weapon Attributes](Wardogs_WeaponAttributes_v1.md). Regenerate the tables with `python -I _tools/weapon_ranged_fields.py --write`.

## Ranged weapons

<!-- ranged_fields counts -->
38 ranged-weapon items and 24 items with a crosshair override
<!-- /ranged_fields -->

<!-- ranged_fields weapons -->
| Weapon | Item | Rechamber after each shot | Rechamber delay (s) | Unchamber on reload | Iron-sight camera offset (X, Y, Z) | Sight position offset (X, Y, Z) | Fire blend targets | Buffered fire blend (s) | Trace radius |
|---|---|---|---|---|---|---|---|---|---|
| 9K333 Verba | `ID_Launcher_04` | yes | - | - | - | - | - | - | 8 |
| A-91 | `ID_A91` | - | - | - | (0, 0, -0.13) | - | - | - | 7 |
| AK74 | `ID_AK74M` | - | - | - | - | (0, 3, 0) | 5 | - | 6 |
| AMP-9 | `ID_MP9` | - | - | - | (0, 0, -0.08) | (0, -5, 0) | - | - | 6 |
| AMR 50 | `ID_SR_04` | yes | 0.2 | - | - | - | 10 | - | 6 |
| BMR-308 | `ID_RFB` | - | - | - | (0, 0, -0.1) | (0, 0.5, 0) | - | - | 6 |
| Bushmaster M17S | `ID_WEPN_033` | - | - | - | (0, 0, -0.1) | - | - | - | 7 |
| Compound Bow | `ID_CombatBow` | - | - | - | - | - | 10 | 0.05 | 6 |
| Deagle | `ID_WEPN_027` | - | - | - | - | (0, -3.5, 0) | - | - | 4 |
| Evo-3 Ultra | `ID_WEPN_036` | - | 0.25 | - | - | (0, 3.7, 0) | - | 0 | 6 |
| FAL | `ID_WEPN_030` | - | - | - | - | - | - | - | 6 |
| Galil | `ID_WEPN_029` | - | - | - | (0, 0, 0.1) | - | 5 | - | 6 |
| GGX 17 | `ID_Glock17` | - | - | - | - | - | - | - | 3 |
| GGX 18 | `ID_WEPN_032` | - | - | - | (0, 2, 0) | - | - | - | 3 |
| Judge | `ID_Judge` | - | 0.3 | yes | (-0.07, 0, -0.1) | - | - | - | 3 |
| KH-2002 | `ID_KH2002` | - | - | - | - | - | - | - | 7 |
| M14 | `ID_WEPN_034` | - | 0.25 | - | (0.03, -0.5, 0) | (0, 10.5, 2.2) | - | 0 | 6 |
| M1911 | `ID_WEPN_026` | - | - | - | (0, 0, -0.05) | - | - | - | 3 |
| M249 SAW | `ID_M249` | - | - | - | - | (0, 2, 0) | - | - | 6 |
| M4 | `ID_M4` | - | - | - | (0, 0, -0.05) | - | - | - | 6 |
| M500 | `ID_M500` | yes | - | - | - | - | - | 0 | - |
| MAAWS | `ID_CGM4` | - | - | - | - | - | - | - | 7 |
| MGL-40 | `ID_MMGL` | - | - | yes | - | - | - | - | 6 |
| MK22 | `ID_MK22` | yes | 0.4 | - | (0, 0, -0.1) | - | 10 | - | 6 |
| Mosin Nagant | `ID_WEPN_017` | yes | 0.25 | - | - | - | 10 | - | 6 |
| MP43 | `ID_MP43` | - | 0.2 | - | (0, 0, -0.15) | (0, 0, 0.5) | - | - | 6 |
| MP5 | `ID_WEPN_028` | - | - | - | (0, 0, -0.05) | - | - | - | 6 |
| PKM | `ID_LMG_02` | - | 0.25 | - | - | (0, -10, 0) | - | - | 6 |
| PP-19 Bizon | `ID_WEPN_031` | - | - | - | - | (0, 3, 0) | - | - | 6 |
| PP-19 Vityaz | `ID_SMG_03` | - | - | - | (0, 0, -0.05) | (0, 3, 0) | - | - | 6 |
| RPG-7 | `ID_RPG7` | yes | - | - | (0, -10, 0) | - | - | - | 7 |
| Scout Rifle TD | `ID_WEPN_035` | - | - | - | - | (0, 3, 0) | - | - | 6 |
| SKS | `ID_SKS` | - | - | - | - | - | - | - | 6 |
| Super-45 | `ID_Vector` | - | - | - | (0, 0, 0.2) | - | - | - | 6 |
| SV98 | `ID_SV98` | yes | 0.08 | - | (0, 0, -0.05) | (0, -10, 0) | 10 | 0 | 6 |
| SVD | `ID_SVDM` | - | 0.25 | - | (0, 2.8, -0.18) | (0, 2, 0) | - | - | 6 |
| T-21 | `ID_TAR21` | - | - | - | - | - | - | - | 7 |
| TCX-SPR | `ID_WEPN_037` | - | 0.25 | - | (0.03, 0, 0) | (0, 4.4, 0) | - | 0 | 6 |
<!-- /ranged_fields -->

What each column holds (**Data**):

- **Rechamber after each shot** is `bRequiresRechamberAfterFire`. Seven items set it: the 9K333 Verba, AMR 50, M500, MK22, Mosin Nagant, RPG-7 and SV98. The set is the bolt-action rifles, the M500 and the single-shot launchers; no semi-auto or full-auto weapon sets it.
- **Rechamber delay** is `TimeAfterFireToRechamber` in seconds. It is set on eleven items, including weapons that do not require a rechamber (SVD, PKM, MP43, M14, TCX-SPR, Evo-3 Ultra, Judge), so the delay is not limited to bolt guns. **Not traced:** which code starts the rechamber animation after the delay.
- **Unchamber on reload** is `bShouldUnchamberDuringReload`; only the Judge and the MGL-40 set it.
- **Iron-sight camera offset** and **sight position offset** are vectors in the weapon's local axes, units not stated by the export (the values run from 0.03 to 10.5, so the two fields use different scales). They are per weapon and not per sight. How the camera applies them is **Not traced**.
- **Fire blend targets** (`FireAnimBlendTargets`) is 5 on the AK74 and Galil and 10 on the AMR 50, Compound Bow, MK22, Mosin Nagant and SV98. **Buffered fire blend** (`BufferedFireAnimBlendTime`) is 0 on five items and 0.05 s on the Compound Bow. Both are animation settings; the consumer is **Not traced**.
- **Trace radius** is `WeaponTraceRadius`, 3 on pistols and the Judge, 4 on the Deagle, 6 to 7 on rifles, 8 on the Verba. The M500 sets none.
- The two vehicle barrel test items are left out.

## Crosshair overrides on holdable items

Every holdable can replace the default crosshair. Twenty-four items do (**Data**): throwables use the `Throwable` crosshair type, the three hammers and the Halligan Bar use `BuildTool` with a buildable check radius of 275 cm (350 cm for the Large Hammer), and the repair tools and fuel canister use a plain cross with hair length 7.5, gap 5 and opacity 0.6. The remote detonator draws a dot only. No weapon in the table above overrides its crosshair; the weapons use the default crosshair, which the spread settings drive.

<!-- ranged_fields crosshair -->
| Item | Name | Override default crosshair | Shows crosshair | Type | Dot | Hair length | Gap | Opacity | Spread multiplier | Buildable check radius (cm) |
|---|---|---|---|---|---|---|---|---|---|---|
| `ID_C4_Trigger` | Remote Detonator | yes | yes | - | yes | 0 | 0 | - | 0 | - |
| `ID_Crowbar` | Halligan Bar | yes | - | BuildTool | yes | - | - | - | - | 275 |
| `ID_FuelCan_40L` | 40L Fuel Canister | yes | yes | - | - | 7.5 | 5 | 0.6 | 0 | - |
| `ID_HeavyDrill_RepairTool` | Heavy Drill | yes | yes | - | - | 7.5 | 5 | 0.6 | 0 | - |
| `ID_HotPotato_Alpha` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_HotPotato_Bravo` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_HotPotato_Charlie` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_IED_Trigger` | Improvised Explosive Device | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_LargeHammer` | Large Hammer | yes | yes | BuildTool | yes | - | - | - | - | 350 |
| `ID_LightDrill_RepairTool` | Light Drill | yes | yes | - | - | 7.5 | 5 | 0.6 | 0 | - |
| `ID_M67Grenade` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_M67Grenade_Gold` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_MediumHammer` | Medium Hammer | yes | yes | BuildTool | yes | - | - | - | - | 275 |
| `ID_Molotov` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmallHammer` | Small Hammer | yes | yes | BuildTool | yes | - | - | - | - | 275 |
| `ID_SmokeGrenade_Black` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_Blue` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_Green` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_Orange` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_Purple` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_Red` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_White` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_SmokeGrenade_Yellow` | - | yes | yes | Throwable | - | - | - | - | - | - |
| `ID_Wrench_RepairTool` | Wrench | yes | yes | - | - | 7.5 | 5 | 0.6 | 0 | - |
<!-- /ranged_fields -->

## Standalone weapon curves

Seven `CurveFloat` assets sit in the weapon plugins (**Data**). Five belong to bipods and give a camera location offset by field of view (the key runs from 40 to 120, apparently a field of view in degrees; the unit of the value is not stated). Two are ADS-in progress curves for the Galil and the FAL: the FAL one is a straight line, the Galil one stays at 0 until 29% of the ADS time and then rises linearly to 1. Which camera code reads the bipod curves is **Not traced**.

<!-- ranged_fields curves -->
| Curve | Used by | Keys (time or FOV in, value out) |
|---|---|---|
| `CRV_FGRP_009_CameraLocationFOVOffset` | SV98 Bipod | (40, -45), (60, -10), (70, 0), (80, 20), (90, 50), (100, 65), (110, 80), (120, 90) |
| `CRV_FGRP_010_CameraLocationFOVOffset` | SKS Bipod | (40, -50), (60, -50), (70, -30), (80, -10), (90, 10), (100, 25), (110, 35), (120, 60) |
| `CRV_FGRP_011_CameraLocationFOVOffset` | SVD Bipod | (40, -90), (60, -90), (70, -40), (80, 5), (90, 25), (100, 45), (110, 60), (120, 80) |
| `CRV_FGRP_012_CameraLocationFOVOffset` | M249 Bipod | (40, -45), (60, 20), (70, 40), (80, 70), (90, 85), (100, 100), (120, 115) |
| `CRV_FGRP_013_CameraLocationFOVOffset` | Pro Tilt Bipod | (40, 60), (60, 60), (70, 80), (80, 95), (90, 110), (100, 120), (110, 130), (120, 140) |
| `CF_WEPN_029_ADS_Curve` | Galil | (0, 0), (0.294325, 0), (1, 1) |
| `CF_WEPN_030_ADS_Curve` | FAL | (0, 0), (1, 1) |
<!-- /ranged_fields -->

## Magazine price points by ammunition type

Each magazine's vendor row holds seven variations (30 of 33 magazines), one per ammunition type: the shown "standard" price, then FMJ, hollow point and armor piercing, each with a tracer twin. Only the first has `bShowInVendor` set, so the vendor list shows the standard price; the rest are the prices for loading that ammunition type (**Data**; how the vendor UI applies them is not traced). Three magazines have fewer: one lacks the tracer variants and two list only the tracer types. Every variation unlocks at level 1.

<!-- ranged_fields magazines -->
| Magazine | Item | Standard | FMJ | FMJ tracer | Hollow point | Hollow point tracer | Armor piercing | Armor piercing tracer |
|---|---|---|---|---|---|---|---|---|
| M1911 7 RND Magazine | `ID_MAGZ_002` | 20 | 27 | 27 | 30 | 30 | 34 | 34 |
| Deagle 7 RND Magazine | `ID_MAGZ_003` | 50 | 78 | 78 | 99 | 99 | 176 | 176 |
| MP5 30 RND Magazine | `ID_MAGZ_004` | 100 | 130 | 130 | 145 | 145 | 160 | 160 |
| Galil 35 RND Magazine | `ID_MAGZ_005` | 60 | 113 | 113 | 148 | 148 | 200 | 200 |
| FAL 20 RND Magazine | `ID_MAGZ_006` | 150 | 230 | 230 | 290 | 290 | 510 | 510 |
| GGX 50 RND Drum Magazine | `ID_MAGZ_011` | 110 | 160 | 160 | 185 | 185 | 210 | 210 |
| GGX 33 RND Magazine | `ID_MAGZ_012` | 70 | 103 | 103 | 119 | 119 | 136 | 136 |
| FAL 30 RND Magazine | `ID_MAGZ_024` | 250 | 370 | 370 | 460 | 460 | 790 | 790 |
| AMR 50 10 RND Magazine | `ID_MAGZ_026` | 30 | 530 | 530 | 390 | - | 515 | - |
| MK22 5 RND Magazine | `ID_MAGZ_034` | 30 | 50 | 50 | 65 | 65 | 120 | 120 |
| PP-19 50 RND Vityaz Drum Magazine | `ID_MAGZ_046` | 200 | 250 | 250 | 275 | 275 | 300 | 300 |
| PP-19 Bizon 53 RND Magazine | `ID_MAGZ_051` | 200 | 253 | 253 | 280 | 280 | 306 | 306 |
| AMP-9 20 RND Magazine | `ID_MAGZ_052` | 70 | 90 | 90 | 100 | 100 | 110 | 110 |
| Super-45 40 RND Drum Magazine | `ID_MAGZ_055` | 280 | 340 | 340 | 370 | 370 | 400 | 400 |
| MP5 50 RND Drum Magazine | `ID_MAGZ_056` | 230 | 280 | 280 | 305 | 305 | 330 | 330 |
| Super-45 13 RND Magazine | `ID_MAGZ_057` | 30 | 43 | 43 | 49 | 49 | 56 | 56 |
| PP-19 Vityaz 10 RND Magazine | `ID_MAGZ_059` | 25 | 35 | 35 | 40 | 40 | 45 | 45 |
| Galil 50 RND Magazine | `ID_MAGZ_060` | 110 | 185 | 185 | 235 | 235 | 310 | 310 |
| AMP-9 15 RND Magazine | `ID_MAGZ_061` | 30 | 45 | 45 | 52 | 52 | 60 | 60 |
| M249 100 RND Fabric Magazine | `ID_MAGZ_062` | 200 | 350 | 350 | 450 | 450 | 600 | 600 |
| M1911 10 RND Magazine | `ID_MAGZ_063` | 35 | 45 | 45 | 50 | 50 | 55 | 55 |
| MP5 20 RND Magazine | `ID_MAGZ_064` | 70 | 90 | 90 | 100 | 100 | 110 | 110 |
| SVD 5 RND Magazine | `ID_MAGZ_065` | 20 | 50 | 50 | 75 | 75 | 110 | 160 |
| AMP-9 50 RND Drum Magazine | `ID_MAGZ_066` | 180 | 230 | 230 | 255 | 255 | 280 | 280 |
| Evo-3 Ultra 50 RND Box | `ID_MAGZ_067` | 110 | 310 | 310 | 460 | 460 | 1,010 | 1,010 |
| M14 10 RND Magazine | `ID_MAGZ_068` | 60 | 100 | 100 | 130 | 130 | 240 | 240 |
| TCX-SPR 28 RND Magazine | `ID_MAGZ_069` | 50 | 162 | 162 | 302 | 302 | 470 | 470 |
| M14 30 RND Magazine | `ID_MAGZ_070` | 180 | 300 | 300 | 390 | 390 | 720 | 720 |
| M14 20 RND Magazine | `ID_MAGZ_071` | 110 | 190 | 100 | 130 | 130 | 240 | 240 |
| - | `ID_MP9Magazine` | 100 | 130 | 130 | 145 | 145 | 160 | 160 |
| - | `ID_STANAGExtendedMagazine` | 180 | - | 270 | - | 330 | - | 420 |
| - | `ID_STANAGMagazine20rd` | 10 | - | 40 | - | 60 | - | 90 |
| - | `ID_VectorMagazine` | 80 | 110 | 110 | 125 | 125 | 140 | 140 |
<!-- /ranged_fields -->

## Transfer time on the 9K333 Verba

The 9K333 Verba (`ID_Launcher_04`) is the only item with a `WDInventoryFragment_TransferTime` fragment: `TransferTime` = **3.5 s**. The inventory transfer rule has a default transfer time of 0.5 s ([Game Mechanics](Wardogs_GameMechanics_v2.md)). That the fragment replaces the rule default for this item is **Inferred** from the names; the reader of the fragment was not traced.
