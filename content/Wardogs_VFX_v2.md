---
title: "VFX"
redirect_from: ["/Wardogs_VFX_v2.html", "/Wardogs_VFX_v2"]
parent: "World, Visuals & Audio"
description: "Inventory, Explosions, Explosion Sequences, Muzzle Flashes"
---

# Wardogs — VFX Reference
*Extracted from the cooked JSON export under [`Content/VFX`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX) (205 files, all parsed; 205 export blocks). Values are the raw asset properties. Where a property's meaning is inferred from its name, that is said explicitly. A "-" in a table means the property is absent from the export, so the engine default applies and that default is not in the dump.*

> **Scope note:** this doc covers only [`Content/VFX`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX). Balance numbers for weapons and vehicles live in other categories. Asset names in the tables match the export `Name` field, so they can be searched directly in the dump.

---

## Season 02 update (2026-10-15)

- 14 assets added: one explosion recipe ([`DA_Explosion_125x570mm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/DA_Explosion_125x570mm.json)), two vehicle exhausts ([`DA_TNK_04_Exhaust`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Vehicles/Exhaust/DataAssets/DA_TNK_04_Exhaust.json), [`DA_WHL_08_Exhaust`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Vehicles/Exhaust/DataAssets/DA_WHL_08_Exhaust.json)), three muzzle attachments ([`DA_MF_MUZL_069`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_MUZL_069.json), [`DA_MF_MUZL_070`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_MUZL_070.json), [`DA_MF_MUZL_072`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_MUZL_072.json)) and eight weapon flash recipes ([`DA_MuzzleFlash_SigMcx`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/AssualtRifles/DA_MuzzleFlash_SigMcx.json), `_M14`, `_Evloys`, `_WEPN_031`, `_STN_06_MountedMachineGun`, `_TNK_04`, `_TNK_04_MountedMachineGun`, `_WHL_08_MountedMachineGun`).
- Asset counts: 191 files → 205. Explosions 34 → 35, vehicle exhaust data assets 11 → 13, muzzle attachments 44 → 47, weapon flash recipes 40 → 48.

---

## 1. Inventory

| Family (subfolder) | Files | Asset type | What it controls |
|---|---|---|---|
| `Explosions/` | 35 | `PDA_Explosion_C` | Single explosion recipes (fireball, core, streaks, embers, shockwave, camera shake) |
| [`Explosions/Blueprints/Sequence/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence) | 14 | `PDA_ExplosionTimingData_C` | Multi-explosion sequences (which recipe fires, when, and where) |
| [`Weapons/MuzzleFlashes/AmmoMuzzleFlashData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AmmoMuzzleFlashData) | 12 | `PDA_MuzzleFlashAmmuniton_C` | Per-ammo-type flash color and spark overrides |
| [`Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData) | 47 | `PDA_MuzzleFlashAttachement_C` | Per-muzzle-device flash size, pattern, gas and light multipliers |
| [`Weapons/MuzzleFlashes/MuzzleFlashData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData) (+ subfolders) | 48 | `PDA_MuzzleFlash_C` | Per-weapon flash: 1P/3P size, lifetime, distant flash, gas, light, default muzzle |
| [`Weapons/Impacts/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Weapons/Impacts) | 9 | `PDA_PhysicalMaterialResponse_C` | Bullet and explosion response per physical material |
| [`VFXManager/WeaponImpacts/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/VFXManager/WeaponImpacts) | 1 | `CurveFloat` | [`C_KineticRemap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/VFXManager/WeaponImpacts/C_KineticRemap.json) float curve |
| [`VFXManager/LandscapeResponse/CurveAtlas/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/VFXManager/LandscapeResponse/CurveAtlas) | 6 | `CurveLinearColor` x5 + `CurveLinearColorAtlas` | Landscape-response color gradients |
| `Shared/` + [`Shared/SmokeGrenadeVFX_Variants/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Shared/SmokeGrenadeVFX_Variants) | 8 | `PDA_SmokeGrenade_C` | Smoke grenade colors and duration |
| [`Vehicles/Exhaust/DataAssets/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Vehicles/Exhaust/DataAssets) | 13 | `BHExhaustDataAsset_C` | Vehicle exhaust Niagara setup per vehicle |
| [`Vehicles/Exhaust/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Vehicles/Exhaust) | 4 | `CurveLinearColor` x3 + `CurveLinearColorAtlas` | Exhaust scale-by-velocity curves |
| [`Environmental/Ambient/FallingLeaves/Materials/Gradients/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Environmental/Ambient/FallingLeaves/Materials/Gradients) | 7 | `CurveLinearColor` x6 + `CurveLinearColorAtlas` | Falling-leaf color gradients per tree type |
| [`Postprocess/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Postprocess) | 1 | `DataTable` (11 rows) | Post-process effects keyed by damage/state tag |

Totals: 35 + 14 + 12 + 47 + 48 + 9 + 1 + 6 + 8 + 13 + 4 + 7 + 1 = **205**.

---

## 2. Explosions (`PDA_Explosion_C`, 35 assets)

Each row is one explosion recipe. Used directly, or as a timing entry inside a sequence (section 3).

| Asset | Fireball | FireballSize | Lifetime (s) | CoreSize | CoreAmt | SizeMult | Heat | Shockwave | ShockSize | Streaks | Embers | Sparks | Debris | HangSmoke | CamShakeRange |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DA_BluntImpact | - | - | - | 0 | 0 | 1.2 | 1800 | - | 4 | - | - | 70 | 155 | - | 0 |
| DA_ComponentBurst_Small | - | 0.288 | 1.909 | 5 | 0 | 1 | 0 | True | 0.628 | - | - | 0 | 10 | - | 250 |
| DA_DebrisExplosion_LowTemp | True | 74.84 | 2.806 | 21.48 | 2 | 2.358 | 1000 | True | 5 | 5 | 16 | 1500 | 200 | 2 | 5000 |
| DA_Explosion_30mm | True | 75 | 1.596 | 20 | 1 | 0.01 | 1750 | - | 1 | 4 | - | 300 | 5 | 1 | 0 |
| DA_Explosion_40mm | - | 108.2 | 2 | 17.48 | 1 | 2.234 | - | True | 3 | 12 | - | 500 | 25 | 8 | 1500 |
| DA_Explosion_72mm | - | - | - | 0 | 0 | - | - | True | - | 5 | 8 | 300 | 50 | - | - |
| DA_Explosion_84mm | - | - | - | 15.26 | 1 | - | - | True | 3 | 10 | 8 | 400 | 5 | - | 2000 |
| DA_Explosion_93mm | - | - | - | 15.26 | 1 | - | - | True | 3 | 10 | 8 | 400 | 5 | - | 2000 |
| DA_Explosion_115mm | True | 69.32 | - | 14.76 | - | - | - | True | 2.815 | 14 | - | - | 500 | 3 | 2000 |
| DA_Explosion_120x570mm | - | 160.2 | 2.617 | 29.18 | 2 | 4 | 5000 | True | 6.5 | 14 | 8 | 300 | 15 | 2 | 2200 |
| DA_Explosion_120x800mm | - | 160.2 | 2.617 | 29.18 | 2 | 4 | 5000 | True | 6.5 | 14 | 8 | 300 | 15 | 2 | 2200 |
| DA_Explosion_125x570mm | - | 160.2 | 2.617 | 29.18 | 2 | 4 | 5000 | True | 6.5 | 14 | 8 | 300 | 15 | 2 | 2200 |
| DA_Explosion_155mm | True | 344.5 | 6.048 | 44 | - | 1.922 | 4400 | True | 15 | 15 | 25 | 0 | 0 | - | 3750 |
| DA_Explosion_ATMine | True | 88.39 | 2.54 | 20.5 | 2 | 2.902 | 3750 | True | 5 | 8 | 4 | 1500 | 20 | - | 2000 |
| DA_Explosion_Claymore | - | 60 | - | 30 | 2 | 2.65 | 3500 | True | 5 | 6 | 3 | 75 | 55 | - | 1500 |
| DA_Explosion_Default | - | - | - | 0 | 0 | - | - | True | - | 5 | 8 | 300 | 50 | - | - |
| DA_Explosion_ExplosiveArrow | - | 61.51 | - | 12.77 | 1 | 2.46 | 3000 | True | - | - | - | 35 | 5 | - | - |
| DA_Explosion_Grenade | - | 60 | - | 30 | 2 | 2.65 | 3500 | True | 3 | 6 | 3 | 75 | 55 | - | 1500 |
| DA_Explosion_Helicopter | True | 90.75 | 2.806 | 21.48 | 2 | 3 | - | True | 7 | 10 | 16 | 1500 | 155 | 4 | 5000 |
| DA_Explosion_Large | True | 175 | - | 16 | 1 | - | 3000 | - | - | 5 | - | 300 | 15 | - | - |
| DA_Explosion_LargeHelicopter | True | 157.8 | 3.059 | 31.59 | 2 | 3 | - | True | 9 | 15 | 30 | 1100 | 300 | 2 | 5000 |
| DA_Explosion_LargeVehicle | True | 90.75 | 2.806 | 21.48 | 2 | 3 | - | - | 7 | 10 | 16 | 1500 | 155 | 4 | 5000 |
| DA_Explosion_Medium | - | - | - | 0 | 0 | - | - | - | - | 5 | 8 | 300 | 50 | - | - |
| DA_Explosion_MediumWheeledVehicle | True | 90.75 | 2.806 | 21.48 | 2 | 3 | - | True | 5 | 25 | 16 | 1500 | 155 | 2 | 5000 |
| DA_Explosion_Medium_DebrisHeavyFireball | True | 90.75 | 2.806 | 21.48 | 2 | 3 | - | - | 5 | 25 | 16 | 1500 | 155 | 4 | 5000 |
| DA_Explosion_Medium_NoEmbers | - | - | - | 0 | 0 | - | - | - | - | 5 | - | 300 | 0 | - | - |
| DA_Explosion_NoHangingSmoke | True | 90.75 | 2.806 | 21.48 | 2 | 3.249 | 3874 | True | 5 | 25 | 10 | 1500 | 165 | 1 | 5000 |
| DA_Explosion_Small | - | - | - | 0 | 0 | 1 | 2000 | - | - | 3 | - | 300 | 25 | - | - |
| DA_Explosion_SmallWheeledVehicle | True | 41.82 | - | 16.09 | 4 | - | - | - | - | 8 | - | 2000 | - | 8 | - |
| DA_Explosion_Tank | True | 137.5 | 4.206 | 29.36 | 2 | - | - | True | 4.818 | 25 | 24 | 1000 | 300 | 3 | 4000 |
| DA_Explosion_VeryLarge | True | 252.4 | 5.79 | 28.85 | 2 | 6 | 3200 | - | - | 12 | - | 0 | 35 | 1 | - |
| DA_HeavyDebrisBurst_NoTemp | - | 74.84 | 2.806 | 23 | 2 | 2.358 | 0 | - | 5 | 5 | 2 | 1500 | 200 | 2 | 5000 |
| DA_SmokeBurst_Small | - | 0 | 0 | 5 | 1 | 0.05 | 0 | - | 0 | - | - | 0 | 0 | 2 | 0 |

**Reading the table**

- **Size tiers are visible in the numbers.** Small and medium recipes (30mm through 115mm-class, and the infantry and vehicle-scale bursts) sit around CoreSize 14 to 21 and FireballSize 60 to 90. Artillery and large vehicles go up to FireballSize 157 to 344 (155mm = 344.5, lifetime 6.05 s). [`DA_Explosion_VeryLarge`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/DA_Explosion_VeryLarge.json) is FireballSize 252.4 with a 5.79 s lifetime.
- **Camera shake range** is 5000 on the heavy recipes (DA_Explosion_Helicopter, LargeVehicle, LargeHelicopter, DebrisExplosion_LowTemp, HeavyDebrisBurst_NoTemp, Medium_DebrisHeavyFireball). The smallest non-zero is 250 (DA_ComponentBurst_Small). Each recipe also references a camera shake blueprint by name (for example `B_CameraShake_Artillery_C` on DA_Explosion_155mm); those names are not in this table.
- **Heat intensity (`HeatIntensity`)** is set on 19 assets, from 0 to 5000. The highest are DA_Explosion_120x570mm, DA_Explosion_120x800mm and DA_Explosion_125x570mm at 5000, followed by DA_Explosion_155mm at 4400.
- **Fireball and Shockwave are independent booleans.** Neither implies the other. For example DA_Explosion_30mm has a fireball and no shockwave, and DA_Explosion_LargeVehicle has a fireball and no shockwave.
- **Units** are not stated in the export. The values look like Unreal centimetres for sizes and seconds for lifetimes, but that is an inference from magnitude, not confirmed.

---

## 3. Explosion Sequences (`PDA_ExplosionTimingData_C`, 14 assets)

A sequence is a list of `TimingInfo` entries. Each entry names an explosion recipe (section 2), a start time, and a root offset from the sequence origin. Format below: `recipe @ time s (offsetX, offsetY, offsetZ)`.

| Sequence asset | Entries | Timing entries |
|---|---|---|
| DA_155mmExplosionSequence | 13 | 155mm @ 0.0 (0,0,0); VeryLarge @ 0.0 at (650,0,0), (-650,0,0), (0,650,0), (0,-652,0); Large @ 0.0 at (400,-400,0), (-400,400,0), (400,400,0), (-400,-400,0); Medium_NoEmbers @ 0.0 at (800,50,0), (-800,50,0), (-50,800,0), (25,-800,0) |
| DA_DuneBuggyExplosionSequence | 3 | Small @ 0.10 (125,0,100); Medium @ 0.09 (-150,0,150); SmallWheeledVehicle @ 0.088 (0,0,125) |
| DA_FOBDestroyed_ExplosionSequence | 4 | Small @ 0.01 (170,50,60); Medium @ 0.10 (185,0,160); Medium @ 0.09 (-250,0,150); NoHangingSmoke @ 0.125 (0,0,200) |
| DA_HavocExplosionSequence | 6 | Medium @ 0.0 (-350,0,250); Medium @ 0.10 (0,125,200); Medium @ 0.15 (0,-125,200); Medium @ 0.35 (200,0,250); LargeVehicle @ 0.15 (100,0,400); LargeHelicopter @ 0.30 (-50,0,425) |
| DA_HelicopterExplosionSequence | 4 | Medium @ 0.0 (-400,0,200); Medium @ 0.45 (650,0,250); LargeVehicle @ 0.30 (250,0,450); LargeHelicopter @ 0.30 (-50,0,475) |
| DA_IEDExplosionSequence | 5 | MediumWheeledVehicle @ 0.01 (0,50,5); NoHangingSmoke @ 0.114 (250,0,5); SmallWheeledVehicle @ 0.04 (-250,0,1); Small @ 0.05 (-225,125,-5); Small @ 0.05 (0,225,5) |
| DA_KodiakExplosionSequence | 3 | Medium @ 0.10 (185,0,160); Medium @ 0.09 (-250,0,150); MediumWheeledVehicle @ 0.088 (0,0,200) |
| DA_LittlebirdExplosionSequence | 3 | Medium @ 0.15 (-270,0,55); Medium_DebrisHeavyFireball @ 0.30 (25,0,150); Helicopter @ 0.40 (0,0,250) |
| DA_STN01_Misteral_ExplosionSequence | 3 | Medium @ 0.10 (125,0,100); Medium @ 0.09 (-125,0,100); DebrisExplosion_LowTemp @ 0.088 (0,0,200) |
| DA_STN02_Phalanx_ExplosionSequence | 3 | Medium @ 0.10 (185,0,60); Medium @ 0.09 (-200,0,60); MediumWheeledVehicle @ 0.088 (0,0,170) |
| DA_STN03_Mortar_ExplosionSequence | 4 | Medium @ 0.10 (125,0,100); Medium @ 0.10 (-125,0,95); Medium @ 0.09 (-125,0,100); DebrisExplosion_LowTemp @ 0.088 (0,0,200) |
| DA_STN04_Loudspeaker_ExplosionSequence | 3 | HeavyDebrisBurst_NoTemp @ 0.088 (0,0,726); HeavyDebrisBurst_NoTemp @ 0.05 (0,0,400); HeavyDebrisBurst_NoTemp @ 0.02 (0,0,25) |
| DA_TankExplosionSequence | 5 | Medium @ 0.0 (-250,0,200); Medium @ 0.10 (-100,50,200); Default @ 0.20 (175,0,200); MediumWheeledVehicle @ 0.25 (0,0,180); Tank @ 0.34 (50,0,280) |
| DA_UralExplosionSequence | 3 | Medium @ 0.10 (300,0,220); Medium @ 0.09 (-220,0,220); MediumWheeledVehicle @ 0.09 (100,0,250) |

**Notes**

- The 155mm sequence has 13 entries, and it fires 4 VeryLarge, 4 Large, and 4 Medium_NoEmbers recipes around a central 155mm burst. It is the widest sequence in the set.
- Timings run from 0.0 to 0.45 s. The vehicle sequences (Kodiak, Ural, IED) stagger a Medium recipe with a wheeled-vehicle recipe at about 0.09 s.
- Offsets are in the same units as the sequence's root (presumed centimetres). Z values from 0 to 726 are used to lift the fireball above the ground.
- Every `TimingInfo` entry's recipe reference resolves to a recipe in section 2. The cross-reference check in this pass found 0 missing targets (78 references checked across explosions and muzzle flashes).

---

## 4. Muzzle Flashes

Three layers, combined in this order: the **weapon** asset (section 4c) names a **default muzzle** attachment (section 4b). The **ammo** asset (section 4a) can override flash color and sparks. The attachment's multipliers scale the weapon's values. The exact multiplication rule is an inference (see section 10).

### 4a. Ammo overrides (`PDA_MuzzleFlashAmmuniton_C`, 12 assets)

| Asset | OverrideFlash | Flash RGB (R,G,B) | OverrideSparks | Spark amount (X,Y) | Spark RGB |
|---|---|---|---|---|---|
| DA_MF_45ACP | True | 175, 72.2, 14.58 | - | - | - |
| DA_MF_45Colt | - | (default) | - | - | - |
| DA_MF_50AE | - | (default) | - | - | - |
| DA_MF_545mm | - | (default) | - | - | - |
| DA_MF_556mm | - | (default) | - | - | - |
| DA_MF_762mm | - | (default) | - | - | - |
| DA_MF_762x54mm | - | (default) | True | 2, 3 | 50, 1.446, 0 |
| DA_MF_7mmBuck | - | (default) | - | - | - |
| DA_MF_93mm | - | (default) | - | - | - |
| DA_MF_9mm | True | 175, 72.2, 14.58 | - | - | - |
| DA_MF_AmmoType | - | (default) | - | - | - |
| DA_MF_VehicleFallback | - | (default) | - | - | - |

Only DA_MF_45ACP and DA_MF_9mm set `Override Flash`. The `(default)` entries carry the same stored RGB, but without the override flag they are not expected to change the flash color. Only DA_MF_762x54mm overrides sparks. Its spark color is (50, 1.446, 0), a warm yellow-orange.

### 4b. Muzzle device attachments (`PDA_MuzzleFlashAttachement_C`, 47 assets)

Grouped by the mesh each one is paired with. Ranges are min..max across the group. Columns that are constant across a group are shown as one value.

| Group (mesh) | Count | SizeMult 1P | LightMult | Pattern | PatternSize 1P | GasSideScale | DistantMult | HeadOnMult | Members |
|---|---|---|---|---|---|---|---|---|---|
| `SK_MZL_04` | 31 | 0.30 to 0.70 | 0.05 | True (on shown rows) | 5 to 10 | 20 to 40 | 0.75 to 0.85 | - | MUZL_013, 032, 037, 038, 039, 040, 041, 042, 046, 049, 051 to 062, MUZL_069, MUZL_070, MUZL_072, MZL_04, MZL_06, MZL_07, MZL_08, MZL_09, MZL_10 |
| `SK_MZL_05` | 1 | 0.40 | 0.05 | True | 5 | 40 | 0.80 | - | MZL_05 |
| `SK_PWSCQB74_Muzzle` | 1 | - | 0.10 | True | 6 | 50 | 0.80 | 0.40 | PWSCQB74 |
| (no mesh) | 14 | 1.5 (where set) | 0.10 (where set) | mostly True | 4 to 10 | 0 to 50 | - | 0.75 to 0.80 | A91_DefaultMuzzle, AK74-M_Default, Attachment, KH2002_DefaultMuzzle, M249_DefaultMuzzle, M4_DefaultMuzzle, M500_DefaultMuzzle, NoAttachment, RFB_DefaultMuzzle, SKS_DefaultMuzzle, SVDM_DefaultMuzzle, TAR91_DefaultMuzzle, WEPN_029_DefaultMuzzle, WEPN_030_DefaultMuzzle |

**Notes**

- The 14 no-mesh entries are the **default muzzles** referenced by weapons in section 4c (for example [`DA_MF_A91_DefaultMuzzle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_A91_DefaultMuzzle.json), [`DA_MF_M4_DefaultMuzzle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_M4_DefaultMuzzle.json)). They are the built-in flash for a weapon with no attachment.
- [`DA_MF_Attachment`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_Attachment.json) and [`DA_MF_NoAttachment`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_NoAttachment.json) do not set a size multiplier. They act as the placeholder entries.
- Across the 47 attachments, `Override Spark Amount` is set on 32, `Override Material` on 36, `Override Flash Frequency` on 16, and `Override Distant Flash` on 1. These are flags that say whether the attachment replaces the weapon's value for that field.

### 4c. Weapon flash recipes (`PDA_MuzzleFlash_C`, 48 assets)

Folder shown as the subfolder under [`MuzzleFlashData/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData). Size1P / Size3P are the first-person and third-person flash sizes. "DistSize / DistMax" is the distant-flash size and its cap. Gas columns are the gas puff amount, size, and spread. Every row has the same flash RGB (175, 74.5, 18.2).

| Folder | Asset | Size 1P | Size 3P | Life (s) | DistSize | DistMax | Prob | Freq | Gas amt / size / spread | DefaultMuzzle | DistantFX |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AssualtRifles | DA_MuzzleFlash_A91 | 15 | 30 | 0.05 | 90 | 200 | - | - | - | DA_MF_A91_DefaultMuzzle | - |
| AssualtRifles | DA_MuzzleFlash_AK74-M | 15 | 35 | 0.05 | 90 | 200 | - | - | - / 120 / - | DA_MF_AK74-M_Default | - |
| AssualtRifles | DA_MuzzleFlash_Fal | 18 | 57 | 0.05 | 100 | 250 | - | - | - | DA_MF_WEPN_030_DefaultMuzzle | - |
| AssualtRifles | DA_MuzzleFlash_Galil | 15 | 52.5 | 0.05 | 90 | 200 | - | - | - | DA_MF_WEPN_029_DefaultMuzzle | - |
| AssualtRifles | DA_MuzzleFlash_KH2002 | 15 | 30 | - | 90 | 200 | - | - | - | DA_MF_KH2002_DefaultMuzzle | - |
| AssualtRifles | DA_MuzzleFlash_M4 | 10 | 35 | 0.05 | 90 | 200 | - | - | - | DA_MF_M4_DefaultMuzzle | - |
| AssualtRifles | DA_MuzzleFlash_TAR21 | 15 | 30 | 0.05 | 80 | 350 | - | - | - | DA_MF_TAR91_DefaultMuzzle | - |
| AssualtRifles | DA_MuzzleFlash_SigMcx | 18 | 57 | 0.05 | 100 | 250 | - | - | - | DA_MF_WEPN_030_DefaultMuzzle | - |
| (root) | DA_MuzzleFlash_Default | - | - | - | - | - | 0.9 | 0.9 | - | - | - |
| DMR | DA_MuzzleFlash_RFB | - | 35 | 0.05 | 95 | 300 | - | - | - | DA_MF_RFB_DefaultMuzzle | - |
| DMR | DA_MuzzleFlash_SKS | - | 35 | 0.05 | 95 | 300 | - | - | - | DA_MF_SKS_DefaultMuzzle | - |
| DMR | DA_MuzzleFlash_SVDM | - | 35 | 0.05 | 95 | 300 | - | - | - | DA_MF_SVDM_DefaultMuzzle | - |
| DMR | DA_MuzzleFlash_M14 | - | 35 | 0.05 | 95 | 300 | - | - | - | DA_MF_RFB_DefaultMuzzle | - |
| LMG | DA_MuzzleFlash_M249 | - | 35 | 0.05 | 90 | 300 | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |
| LMG | DA_MuzzleFlash_PKM | - | 38 | 0.05 | 95 | 300 | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |
| LMG | DA_MuzzleFlash_Evloys | - | 38 | 0.05 | 95 | 300 | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |
| ROT_01 | DA_MuzzleFlash_ROT_01_MountedMachineGun | 30 | 50 | - | 80 | 350 | - | - | 3 / 120 / 40 | - | - |
| ROT_02 | DA_MuzzleFlash_Cannon30mm | 0.8 | 90 | - | 150 | 150 | - | - | 3 / 120 / 40 | - | - |
| ROT_02 | DA_MuzzleFlash_ROT_02_Rocket | 10 | - | - | - | - | 0.8 | 0.8 | - | - | NS_MF_Tank |
| ROT_03 | DA_MuzzleFlash_ROT_03_MountedMachineGun | 30 | 50 | 0.1 | 80 | 350 | - | - | 3 / 120 / 40 | - | - |
| ROT_03 | DA_MuzzleFlash_ROT_03_RocketPods | 50 | 7.5 | - | - | 250 | 0.8 | 0.8 | - / 400 / - | - | NS_MF_RocketPod |
| ROT_04 | DA_MuzzleFlash_ROT_04_MountedMachineGun | 30 | 50 | - | 80 | 350 | - | - | 3 / 120 / 40 | - | - |
| SMG | DA_MuzzleFlash_MP5 | 15 | 25 | 0.05 | 80 | 200 | 0.5 | - | - | - | - |
| SMG | DA_MuzzleFlash_MP9 | 15 | 25 | 0.05 | 80 | 200 | 0.5 | - | - | - | - |
| SMG | DA_MuzzleFlash_SMG_03 | 15 | 25 | 0.05 | 80 | 200 | - | - | - | - | - |
| SMG | DA_MuzzleFlash_Vector | 15 | 25 | 0.05 | 80 | 350 | 0.5 | 0.7 | - | - | - |
| SMG | DA_MuzzleFlash_WEPN_031 | 15 | 25 | 0.05 | 80 | 200 | - | - | - | - | - |
| STN03_Mortar | DA_MuzzleFlash_STN_03_MortarLaunch | 50 | 7.5 | - | - | 250 | 0.8 | 0.8 | - / 400 / - | - | NS_MF_Mortar |
| STN_06 | DA_MuzzleFlash_STN_06_MountedMachineGun | - | 30 | - | 50 | - | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |
| Shotgun | DA_MuzzleFlash_M12G | 30 | 50 | 0.05 | 100 | 150 | - | - | 5 / 130 / 60 | DA_MF_M500_DefaultMuzzle | - |
| Shotgun | DA_MuzzleFlash_MP43 | 30 | 50 | 0.05 | 150 | 150 | - | - | 5 / 130 / 60 | - | - |
| Sidearms | DA_MuzzleFlash_Deagle | 25 | 35 | 0.05 | 130 | 150 | - | - | 6 / 100 / 40 | - | - |
| Sidearms | DA_MuzzleFlash_Glock17 | 10 | 20 | 0.05 | 80 | 150 | - | - | - | - | - |
| Sidearms | DA_MuzzleFlash_Judge | 25 | 35 | 0.05 | 130 | 150 | - | - | 6 / 100 / 40 | - | - |
| Sidearms | DA_MuzzleFlash_M1911 | 10 | 20 | 0.05 | 80 | 150 | - | - | - | - | - |
| SniperRifles | DA_MuzzleFlash_MK22 | 25 | 40 | 0.06 | 100 | 300 | - | - | 3 / 120 / 40 | - | - |
| SniperRifles | DA_MuzzleFlash_Mosin | 25 | 40 | 0.06 | 100 | 300 | - | - | 3 / 120 / 40 | - | - |
| SniperRifles | DA_MuzzleFlash_SR_04 | 30 | 40 | 0.06 | 100 | 350 | - | - | 3 / 120 / 40 | - | - |
| SniperRifles | DA_MuzzleFlash_SV98 | 25 | 37 | 0.06 | 100 | 300 | - | - | 3 / 120 / 40 | - | - |
| SniperRifles | DA_MuzzleFlash_WEPN_035 | 25 | 40 | 0.06 | 100 | 300 | - | - | 3 / 120 / 40 | - | - |
| TNK_01/Artillery | DA_MuzzleFlash_Artillery | 10 | - | - | - | - | 0.8 | 0.8 | - | DA_MF_M4_DefaultMuzzle | NS_MF_Artillery |
| TNK_01/Heavy | DA_MuzzleFlash_Heavy | 10 | - | - | - | - | 0.8 | 0.8 | - | DA_MF_M4_DefaultMuzzle | NS_MF_Tank |
| TNK_01/Heavy | DA_MuzzleFlash_TankCoaxialGun | 5 | - | - | 50 | - | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |
| TNK_04 | DA_MuzzleFlash_TNK_04 | 10 | - | - | - | - | 0.8 | 0.8 | - | DA_MF_M4_DefaultMuzzle | NS_MF_Tank |
| TNK_04 | DA_MuzzleFlash_TNK_04_MountedMachineGun | - | 30 | - | 50 | - | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |
| TNK_03_Gepard | DA_MuzzleFlash_Cannon35x228mm | 0.8 | 90 | - | 150 | 150 | - | - | 3 / 120 / 40 | - | - |
| WHL_05 | DA_MuzzleFlash_WHL_05_Minigun | 30 | 50 | 0.1 | 80 | 350 | - | - | 3 / 120 / 40 | - | - |
| WHL_08 | DA_MuzzleFlash_WHL_08_MountedMachineGun | - | 30 | - | 50 | - | - | - | - / 120 / 40 | DA_MF_M249_DefaultMuzzle | - |

Additional fields on single rows: [`DA_MuzzleFlash_ROT_03_RocketPods`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/ROT_03/DA_MuzzleFlash_ROT_03_RocketPods.json) and [`DA_MuzzleFlash_STN_03_MortarLaunch`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/STN03_Mortar/DA_MuzzleFlash_STN_03_MortarLaunch.json) carry a light radius of 250 with intensity unset. [`DA_MuzzleFlash_TankCoaxialGun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/TNK_01/Heavy/DA_MuzzleFlash_TankCoaxialGun.json) uses socket `S_CoaxialMuzzle`. [`DA_MuzzleFlash_Deagle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/Sidearms/DA_MuzzleFlash_Deagle.json) and [`DA_MuzzleFlash_Judge`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/Sidearms/DA_MuzzleFlash_Judge.json) override the material to `MI_MuzzleFlash_02`. [`DA_MuzzleFlash_AK74-M`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/AssualtRifles/DA_MuzzleFlash_AK74-M.json) sets light intensity 100.

**Notes**

- Size 1P is much smaller than Size 3P on almost every rifle (for example A91: 15 vs 30). The first-person flash is the close-up view and is scaled down.
- Cannon-class entries (`Cannon30mm`, `Cannon35x228mm`) have a Size 1P of 0.8 next to a Size 3P of 90, which is a very large ratio. This is probably intentional (a huge third-person blast with a tiny first-person one), but it is unverified.
- `Gas` values appear on machine guns and shotguns (gas amount 3 to 6, gas size 100 to 130). Pistols mostly have none.

---

## 5. Impacts (`PDA_PhysicalMaterialResponse_C`, 9 assets)

Each physical material maps to a bullet impact effect, a bullet decal, an explosion effect, an explosion decal, and caliber-based sizes.

| Asset | Bullet impact FX | Bullet decal | Explosion FX | Explosion decal | Decal size | Small / Medium / Large caliber size | Size random (min, max) |
|---|---|---|---|---|---|---|---|
| DA_ImpactBody | NS_VFX_BloodImpact01_body | - | - | - | 200 | - | - |
| DA_ImpactConcrete | - | - | - | - | 200 | 6 / 6 / 6 | - |
| DA_ImpactDefault | - | - | - | - | 200 | - | - |
| DA_ImpactDirt | NS_VFX_ImpactDirt | MI_Decal_DirtBulletImpact | NS_VFX_Explosion01_Dirt | - | 200 | 4 / 4 / 4 | 0.8, 1.2 |
| DA_ImpactGlass | NS_VFX_ImpactGlass | MM_GlassCrack | NS_VFX_Explosion01_Glass | MM_GlassCrack | 1 | 0.2 / 0.25 / 0.4 | 0.9, 1.1 |
| DA_ImpactHead | NS_VFX_BloodImpact01_head | - | - | - | 200 | - | - |
| DA_ImpactMetal | NS_VFX_ImpactMetal | MI_VFX_BulletDecal_Metal | NS_VFX_Explosion01_Metal | - | 200 | 2 / 2 / 2 | 0.95, 1.05 |
| DA_ImpactWater | NS_VFX_ImpactWater | - | NS_VFX_Explosion01_Water_above | - | - | - | - |
| DA_ImpactWood | NS_VFX_ImpactWood | MI_VFX_BulletDecal_Wood | NS_VFX_Explosion01_Wood | - | 200 | 6 / 6 / 7 | 0.9, 1.1 |

**Notes**

- Body and head have blood impacts (`NS_VFX_BloodImpact01_body` / `_head`) and no decal. Decals are for surfaces.
- Glass is the only material with a decal size of 1 and tiny caliber sizes (0.2 to 0.4). Its explosion decal is also a glass crack (`MM_GlassCrack`), which is a material, not a Niagara system.
- Caliber sizes are the scale of the impact effect per bullet class (small, medium, large). Their exact effect on the visual is not defined in the asset (see section 11).

---

## 6. Smoke Grenades (`PDA_SmokeGrenade_C`, 8 assets)

| Asset | Folder | SmokeType | SmokeColor RGBA | Hex | Sprite max size | Total duration (s) |
|---|---|---|---|---|---|---|
| DA_SmokeGrenade_White | Shared | - | - | - | - | 120 |
| DA_SmokeGrenade_Black | SmokeGrenadeVFX_Variants | - | 0.10, 0.10, 0.10, 0.90 | E6595959 | - | 120 |
| DA_SmokeGrenade_Blue | SmokeGrenadeVFX_Variants | NewEnumerator1 | 0.156, 0.247, 0.807, 0.75 | BF6E88E8 | 300 | 64 |
| DA_SmokeGrenade_Green | SmokeGrenadeVFX_Variants | NewEnumerator1 | 0.135, 0.396, 0.105, 0.75 | BF66A95B | 300 | - |
| DA_SmokeGrenade_Orange | SmokeGrenadeVFX_Variants | NewEnumerator1 | 0.594, 0.187, 0.034, 0.75 | BFCB7833 | 300 | - |
| DA_SmokeGrenade_Purple | SmokeGrenadeVFX_Variants | NewEnumerator1 | 0.210, 0.070, 0.479, 0.75 | BF7E4BB8 | 300 | - |
| DA_SmokeGrenade_Red | SmokeGrenadeVFX_Variants | NewEnumerator1 | 0.531, 0.058, 0.058, 0.75 | BFC14444 | 300 | - |
| DA_SmokeGrenade_Yellow | SmokeGrenadeVFX_Variants | NewEnumerator1 | 0.833, 0.628, 0.056, 0.75 | BFECD043 | 300 | - |

**Notes**

- The colored variants all use alpha 0.75. Black is the outlier at alpha 0.90.
- Only three assets (White, Black, Blue) set `Total Duration`. The other five use the default duration, which is not in the dump. Blue is the only one with a non-120 duration (64 s).
- `SmokeType` is `NewEnumerator1` on six entries. That is an unnamed enum value, so the actual smoke behavior it selects is unclear.

---

## 7. Vehicle Exhaust (`BHExhaustDataAsset_C`, 13 assets, plus 4 curve assets)

| Asset | Niagara system | CurveIndex | Lifetime (s) | InitialVelocity | SpriteSize (X x Y) | AlphaSmoke | DualExhaust | DualOffset (X, Y, Z) |
|---|---|---|---|---|---|---|---|---|
| DA_AntiAirExhaust | NS_TankExhaust | - | 0.8 to 1.0 | 200 | 120 x 140 | 0.20 | True | -280, 0, 0 |
| DA_ArtilleryExhaust | NS_TankExhaust | - | 0.8 to 1.0 | 200 | 120 x 140 | 0.20 | - | - |
| DA_BobcatExhaust | - | - | 0.8 to 1.0 | 350 | 50 x 70 | 0.35 | - | - |
| DA_BuggySpawn_Exhaust | - | - | 1.0 to 1.2 | 250 | 60 x 80 | 0.35 | - | - |
| DA_HavocExhaust | NS_HeliRadiator | - | 1.2 to 1.4 | 200 | 140 x 160 | 0.02 | True | 0, 344, 0 |
| DA_HeavyTankExhaust | NS_TankExhaust | - | 0.8 to 1.0 | 200 | 120 x 140 | 0.35 | True | - |
| DA_HumveeExhaust | - | 1 | 0.8 to 1.0 | 350 | 80 x 100 | 0.35 | - | - |
| DA_KodiakExhaust | - | 2 | 0.8 to 1.0 | 350 | 60 x 80 | 0.35 | - | - |
| DA_LittleBirdExhaust | NS_HeliRadiator | - | 0.8 to 1.0 | 200 | 40 x 60 | 0.05 | - | - |
| DA_ROT_04_Exhaust | NS_HeliRadiator | - | 1.0 to 1.2 | 200 | 80 x 100 | 0.05 | True | 0, -213, 0 |
| DA_TNK_04_Exhaust | NS_TankExhaust | - | 0.8 to 1.0 | 200 | 120 x 140 | 0.35 | - | - |
| DA_UralExhaust | - | 1 | 0.8 to 1.0 | 250 | 80 x 100 | 0.35 | - | - |
| DA_WHL_08_Exhaust | - | 1 | 0.8 to 1.0 | 350 | 80 x 100 | 0.35 | - | - |

**Exhaust scale curves** (`CurveLinearColor` on the vehicle exhaust, packed in [`Exhaust_ScaleVel_Atlas`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Vehicles/Exhaust/Exhaust_ScaleVel_Atlas.json)):

| Curve | Keys | Start value | End value |
|---|---|---|---|
| Buggy_ExhaustCurve | 2 (t 0 to 1) | 1 | 1 |
| Humvee_ExhaustCurve | 2 (t 0 to 1) | 1 | 0.5 |
| Kodiak_ExhaustCurve | 2 (t 0 to 1) | 0 | -5 |

**Notes**

- `CurveIndex` picks a row in the atlas. Humvee uses index 1 and Kodiak index 2, which matches the order in the atlas. The Ural's index is also 1.
- The Kodiak curve drops to -5, which is outside the 0 to 1 range of the others. Whether a negative scale is clamped by the consumer is not visible in the export.
- `DualExhaust` splits one exhaust into two offset emitters. Only some vehicles use it.

---

## 8. Post-Process Effects ([`DT_PostProcessEffects`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Postprocess/DT_PostProcessEffects.json), DataTable with 11 rows)

Each row is a `WDPostProcessEffect` keyed by a gameplay tag. The material is `MI_PP_Damage` in 10 of 11 rows; `DeathState.CloseEyes` uses `MI_Postprocess_Death_Eyes`. The row shows its duration, its progress curves, the values applied at the start of the effect, and the values restored when it ends.

| Row (tag suffix) | Progress parameters (curve keys as (time, value)) | Applied on start | Restored on end |
|---|---|---|---|
| DamageType.Fall | - | - | - |
| DamageType.Explosive | DirtProgress (0,0) (0.2,1) (4,1) (5,0); BlurProgress (0,0) (0.015,1) (0.6,1) (1,0); DamageVignetteProgress (0,0) (0.15,1) (0.8,1) (1,0); HealthProgress (0,1) | - | - |
| Injured.Static | - | - | - |
| Injured.Delta | BlurProgress (0,0) (0.01,1) (0.25,1) (1,0); DamageVignetteProgress (0,0) (0.01,1) (0.5,1) (1,0) | - | - |
| Suppression.Default | - | - | - |
| Suppression.Concussive | DarkenProgress (0,1); BlurProgress (0,1); DesaturationProgress (0,1) | - | - |
| DirectionalIndicator | - | - | - |
| DeathState.Critical | - | BlurProgress = 1 | BlurProgress = 0, DarkenProgress = 0 |
| DeathState.CloseEyes | - | - | - |
| VehicleProjectileCamera | - | BlurProgress = 0.05, DarkenProgress = 1 | BlurProgress = 0, DarkenProgress = 0 |
| Backblast | DirtProgress (0,0) (0.2,1) (4,1) (5,0); BlurProgress (0,0) (0.015,1) (0.6,1) (1,0); DamageVignetteProgress (0,0) (0.15,1) (0.8,1) (1,0); HealthProgress (0,1); DarkenProgress (0,0) (0.015,1) (0.6,1) (1,0) | DarkenMaxIntensity = 15, BlurIntensityMax = 2, DarkenSmoothStepMin = -1, DarkenSmoothStepMax = 10 | - |

**Duration and blend by row** (from the same DataTable):

| Row | Duration (s) | BlendWeight | IgnoreMaterialRemoval | RemoveOnPawnPossessed |
|---|---|---|---|---|
| DamageType.Fall | 0.1 | 1.0 | True | True |
| DamageType.Explosive | 5.0 | 1.0 | True | True |
| Injured.Static | 0.0 | 1.0 | True | True |
| Injured.Delta | 1.0 | 1.0 | True | True |
| Suppression.Default | 0.0 | 1.0 | True | True |
| Suppression.Concussive | 2.0 | 1.0 | False | True |
| DirectionalIndicator | 0.0 | 1.0 | True | True |
| DeathState.Critical | 0.0 | 1.0 | True | True |
| DeathState.CloseEyes | 0.0 | 1.0 | False | True |
| VehicleProjectileCamera | 0.0 | 1.0 | True | True |
| Backblast | 5.0 | 1.0 | True | True |

**Notes**

- A progress parameter is a curve over the effect's duration. Explosive, for example, ramps `DirtProgress` up to 1 by 0.2 s, holds it until 4 s, and ramps it back to 0 by 5 s.
- `Duration = 0.0` rows are instant or state-driven effects. They are kept on until something else removes them (for example `DeathState.Critical`, which applies `BlurProgress` = 1 and restores it on removal).
- `HealthProgress` (0 to 1) on Explosive and Backblast is driven by health. Its exact mapping is not in the row.
- `DefaultValue` on Suppression.Concussive is 3.4028235e+38 (float max) for one curve. That is the engine's "unset" sentinel, so it is not a real value.

---

## 9. Curves and Gradients

| Group | Asset | Type | Keys | Start to end | Use |
|---|---|---|---|---|---|
| Falling leaves | AshLeaf_Gradient | CurveLinearColor | 4 | value 0.017 at t~0 to 0.641 at t=1 | Leaf color ramp for ash trees |
| Falling leaves | BeechLeaf_Gradient | CurveLinearColor | 4 | value 0.021 at t~0 to 0.766 at t=1 | Leaf color ramp for beech |
| Falling leaves | BirchLeaf_Gradient, ChestnutLeaf_Gradient, HawthorneLeaf_Gradient, OakLeaf_Gradient | CurveLinearColor | - | - | Leaf color ramps per tree (not decoded in this pass) |
| Falling leaves | Leaves_Gradients | CurveLinearColorAtlas | - | - | Atlas that packs the six leaf gradients |
| Landscape response | LR_Dirt | CurveLinearColor | 2 | 0.2 to 1 over t 0 to 0.8 | Dirt landscape response |
| Landscape response | LR_Grass | CurveLinearColor | 2 | 0.2 to 1 over t 0 to 0.2 | Grass landscape response |
| Landscape response | LR_Leaf | CurveLinearColor | 1 | 1 | Leaf landscape response (constant) |
| Landscape response | LR_Water | CurveLinearColor | 2 | 0.2 to 1 over t 0 to 0.7 | Water landscape response |
| Landscape response | LandscapeResponse_Default | CurveLinearColor | 2 | 0 to 1 over t 0 to 0.1 | Fallback response |
| Landscape response | CA_LandscapeResponse | CurveLinearColorAtlas | - | - | Atlas packing the five responses |
| Weapon impacts | C_KineticRemap | CurveFloat | 2 | 20 at t=0 to 350 at t=2000 | Remaps an input to a 20 to 350 range (input name not stated) |
| Vehicle exhaust | Buggy / Humvee / Kodiak_ExhaustCurve | CurveLinearColor | 2 each | 1 to 1; 1 to 0.5; 0 to -5 | Exhaust scale by velocity (see section 7) |
| Vehicle exhaust | Exhaust_ScaleVel_Atlas | CurveLinearColorAtlas | - | - | Atlas for the three exhaust curves |

**Notes**

- Every landscape-response curve ends at 1. Apart from [`LR_Leaf`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/VFXManager/LandscapeResponse/CurveAtlas/LR_Leaf.json) (a constant 1), each starts at 0.2 ([`LandscapeResponse_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/VFXManager/LandscapeResponse/CurveAtlas/LandscapeResponse_Default.json) starts at 0), so each ramps up to full strength over a short time window.
- Time ranges are small (0.0 to 0.8). The time axis is probably a normalized input, not seconds.
- [`C_KineticRemap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/VFXManager/WeaponImpacts/C_KineticRemap.json) time axis runs to 2000, so its input is most likely a raw speed or energy value. The unit is not in the export.

---

## 10. How Values Combine

- **Muzzle flash, per shot:** weapon flash recipe (section 4c) provides the base size, lifetime, and gas. Its default muzzle attachment (section 4b) applies the device multipliers (`Flash Size Multiplyer 1P`, `Gas Side Scale`, and so on). The ammo override (section 4a) can then replace color and sparks. The exact order and whether multipliers stack multiplicatively are not stated in the export, so the stacking rule is an inference, not confirmed.
- **Explosion sequence:** a sequence (section 3) fires each entry's recipe at its `Timing` (seconds) with its `RootOffset` added to the sequence origin. The entries are not sorted by time in the file (the 155mm sequence lists every entry at t = 0.0), so each entry's `Timing` value, not its list position, sets when it fires.
- **Post-process:** each row's progress curves drive their parameters over the row's `Duration`. `ParameterValuesOnEffectApplication` is set when the effect starts and `OnRemoveParameterValues` is set when it ends. A row with `Duration = 0` does not time out and must be removed by the gameplay side.
- **Impacts:** the physical material is chosen by the surface the bullet hits. The caliber bucket (small/medium/large) then scales the impact size within the random range.

---

## 11. Still Not Pulled / Limitations

- **Object references only.** Recipe rows reference `B_CameraShake_*` blueprints and `NS_*` Niagara systems by path or class name. Only those references were pulled. The shake behavior and the Niagara internals are not in [`Content/VFX`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/VFX) and are not in this doc.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Unit and meaning uncertainty.** Sizes, lifetimes, and offsets have no units in the export. Multiplier names (for example `Flash Size Multiplyer 1P`) are read literally, and how they stack at runtime is not verified.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Unnamed enum.** `SmokeType = NewEnumerator1` on six smoke grenades does not say which behavior it selects.
  - **SDK (2026-10-16):** enum type is [`ESmokeTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/ESmokeTypes_structs.hpp) (3 values: `NewEnumerator0`, `NewEnumerator1`, `ESmokeTypes_MAX`). Dumper-7 did not resolve the symbolic value names either — the UserDefinedEnum ships without string labels. Behaviour mapping remains unresolved via static means; would need runtime observation to confirm which value triggers which smoke behavior.
- **Unnamed property names.** Some keys in the timing sequences are suffixed with hash tokens (for example `ExplosionData_9_FB01A97E496F...`). They were trimmed to their readable part. The mapping is one-to-one, so the meaning is unchanged, but the raw keys are not reproduced here.
  - **SDK (2026-10-16):** struct is [`FFExplosionTimingInfo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/FExplosionTimingInfo_structs.hpp) with three fields: `ExplosionData` (`UPDA_Explosion_C*`, 0x00), `Timing` (`double`, 0x08), `RootOffset` (`FVector`, 0x10). The hash suffixes (`_9_FB01A97E...`, `_2_4D3BBAEA...`, `_6_F64F6510...`) are Blueprint internal versioning GUIDs; the readable prefix is the actual symbolic field name. Doc's one-to-one assertion confirmed.
- **Default values not exported.** Any property shown as `-` is absent from the export. The engine default applies, and it is not in the dump.
- **Material and decal assets not opened.** `MI_*`, `MM_*`, and `MI_Decal_*` paths are listed but their parameters are not in this category.
- **Landscape-response and leaf gradients partially decoded.** The gradient key lists for the leaf types other than Ash and Beech, and the Landscape response in the CA atlas beyond the five curves, were not reproduced key by key.
- **Post-process UI tags.** The row tags (for example `PostProcessEffect.DamageType.Fall`) are shown in the table, but how the gameplay side selects a row by damage type is not in this category.
