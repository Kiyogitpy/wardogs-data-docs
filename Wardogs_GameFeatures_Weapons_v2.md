---
title: "Weapons (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures/Weapons Reference (v2)

*Source: `Wardogs/Plugins/GameFeatures/Weapons/` (870 JSON files, 3383 exported objects, 0 parse errors). Parsed with a Python script that splits each file on its `--- export:` headers, since many files hold several objects. Values are cooked data as exported. Where a meaning is inferred from a property name, the text says so.*

> **Scope:** this folder holds the per-item GameFeature bundles: inventory definitions, weapon ballistics, vendor rows, attachment wiring, input bindings, audio and mutables. The `Content/Weapons` tree is covered by a separate doc.

---

## 1. Folder layout

Each subfolder is one content bundle. A bundle has a `GameFeatureData` manifest, usually a `GameFeatureAction_DataRegistrySource` (which registers the vendor and entity-UI tables), and a `GameFeatureAction_AddWorldPartitionContent` (which adds an External Data Layer). Item definitions live in `Data/ID_*.json`.

| Group | Files | Item defs | Ranged-weapon exts | Weapon stats assets | GameFeatureData | DataTables |
|---|---|---|---|---|---|---|
| AR | 10 | 0 | 0 | 0 | 6 | 0 |
| SMG | 67 | 5 | 1 | 1 | 5 | 2 |
| LMG | 61 | 5 | 1 | 1 | 2 | 2 |
| DMR | 113 | 8 | 2 | 2 | 2 | 3 |
| Sniper | 189 | 19 | 3 | 3 | 4 | 5 |
| Shotgun | 54 | 5 | 1 | 1 | 2 | 1 |
| Pistols | 51 | 3 | 1 | 0 | 4 | 2 |
| Launchers | 87 | 3 | 2 | 2 | 4 | 2 |
| Platforms | 907 | 24 | 22 | 21 | 23 | 31 |
| Attachments | 1349 | 99 | 0 | 0 | 120 | 191 |
| Components | 495 | 74 | 0 | 0 | 104 | 0 |

Notes on the layout:

- `AR/AR_01` to `AR_07` (six folders, 10 files) hold only GameFeature shells: 6 `GameFeatureData` and 4 world-partition actions. The AR-class item definitions are not in this folder.
- `Platforms/WEPN_0xx` (23 folders) holds the full bundles for the newer weapons. The older hand-named bundles sit in `DMR`, `Sniper`, `LMG`, `Shotgun`, `SMG`, `Pistols` and `Launchers` (`RFB`, `SVDM`, `MK22`, `Mosin`, `SR_04`, `MP43`, `SMG_03`, `LMG_02`, `Pistol_02`, `Launcher_04`, `RPG7`).
- `Attachments/` holds 99 attachment items (Foregrips 13, Magazines 28, Muzzle 40, Sights 18), of which 96 have vendor rows. `Components/` holds 74 weapon-specific items (Barrels 21, Handguards 17, Pistol Grips 12, Stocks 18, Triggers 3, Dust Covers 3), none of which have vendor rows.

**Object types (3383 exported objects):**

| Type | Count | What it holds |
|---|---|---|
| WDItemInputBehavior_ActivateAction | 387 | Input action bindings (payload is empty in this export) |
| GameFeatureData | 276 | Bundle manifest; scans `BH.Item` assets under `/<Bundle>/Data` |
| GameFeatureAction_AddWorldPartitionContent | 259 | Adds an External Data Layer (`EDL_*`) |
| BHInventoryItemDefinition | 245 | Item root: `ItemId`, display name, `ItemContext` tags, `DataFragments` |
| DataTable | 239 | Vendor rows (`WDVendorData`) and entity UI rows (`BHEntityData_UI`) |
| WDInventoryFragment_Gunsmith | 234 | Gunsmith item type (Attachment, Weapon, etc.) |
| WDInventoryFragment_Attachment | 212 | Attachment type tag, applied GameplayEffects, removal flags |
| WDInventoryFragment_Audio | 190 | Pointer to a `WDAudioData` asset |
| BHInventoryFragment_CustomShape | 141 | Inventory shape fragment (no properties exported) |
| BHInventoryFragment_Droppable | 141 | Dropped-world mesh reference |
| BHInventoryFragment_UserInterface | 141 | UI fragment (no properties exported) |
| GameFeatureAction_DataRegistrySource | 138 | Registers DataTables into the `VendorData` / `EntityData_UI` registries |
| BHInventoryFragment_Weight | 138 | Item weight (units not stated) |
| BHInventoryFragment_SubSlotSupport | 104 | Sub-slot containers (what can be fitted or loaded) |
| WDItemInputBehavior_CompleteAction | 66 | Release-side input actions |
| BHAnimationSet | 39 | Animation set reference |
| B_DefaultWeaponInputData_C | 33 | Per-weapon input table (14 bindings) |
| BHItemExtensionData_AimAssistExtension | 33 | Aim-assist settings and filter assets |
| WDInventoryFragment_ItemActor | 33 | Container for the extension-data fragments |
| WDItemExtensionData_Animation | 33 | Animation set reference |
| WDItemExtensionData_AudioExtension | 33 | Audio asset reference |
| WDItemExtensionData_GameplayEffects | 33 | Default weapon attributes (`Attribute.Gameplay.Weapon.*`) |
| WDItemExtensionData_Holdable | 33 | Equip/holster montages, hip offset, FOV when ADS |
| WDItemExtensionData_Inventory | 33 | Ammo requirement for primary fire |
| WDItemExtensionData_Mutable | 33 | Customization parameters on `MUT_MasterWeapon` |
| WDItemExtensionData_RangedWeapon | 33 | Stats link, spread, stance effects, ADS transition, damage tag |
| WDAudioData | 33 | Sound list per weapon |
| WDItemsmithDataFragment_CameraData | 32 | Gunsmith camera framing |
| WDWeaponStatsData | 31 | Ballistics, recoil, aim sway, ADS curves (`DA_*_Stats`) |
| CurveFloat | 7 | Standalone float curves (not decoded here) |

---

## 2. Weapon roster (33 ranged weapons)

Each weapon is found through its `WDItemExtensionData_RangedWeapon`, which names its `WDWeaponStatsData` asset. Price and unlock level come from the vendor variation with `bShowInVendor = true`. "Class" is the first segment of the damage tag (`Meta.Damage.Weapon.<Class>.*`). It is the most consistent family label in the data.

| ID | Display name | Class | Archetype tag | Shown price | Unlock lvl | Primary-fire ammo (type) | Stats asset |
|---|---|---|---|---|---|---|---|
| A91 | A-91 | AR | AR | 0 | 1 | 556mm (Magazine) | DA_A91_Stats.json |
| AK74M | AK74 | AR | AR | 1600 | 1 | 545mm (Magazine) | DA_AK74M_Stats.json |
| KH2002 | KH-2002 | AR | AR | 0 | 1 | 556mm (Magazine) | DA_KH2002_Stats.json |
| M4 | M4 | AR | AR | 2800 | 1 | 556mm (Magazine) | DA_M4_Stats.json |
| TAR21 | T-21 | AR | AR | 600 | 1 | 556mm (Magazine) | DA_TAR21_Stats.json |
| WEPN_029 | Galil | AR | AR | 2200 | 1 | 556mm (Magazine) | DA_WEPN_029_Stats.json |
| WEPN_030 | FAL | AR | AR | 6500 | 1 | 308Win (Magazine) | DA_WEPN_030_Stats.json |
| WEPN_033 | Bushmaster M17S | AR | AR | 0 | 1 | 556mm (Magazine) | DA_WEPN_033_Stats.json (copy, see 8.1) |
| RFB | BMR-308 | DMR | DMR | 6000 | 1 | 308Win (Magazine) | DA_RFB_Stats.json |
| SKS | SKS | DMR | DMR | 2400 | 1 | 762mm (Ammo) | MISSING (no stats asset in folder) |
| SVDM | SVD | DMR | DMR | 4800 | 1 | 762x54mm (Magazine) | DA_SVDM_Stats.json |
| LMG_02 | PKM | LMG | LMG | 4500 | 1 | 762x54mm (Magazine) | DA_LMG_02_Stats.json |
| M249 | M249 SAW | LMG | LMG | 3200 | 1 | 556mm (Magazine) | DA_M249_Stats.json |
| CGM4 | MAAWS | Launcher | Launcher | 2600 | 1 | 84mm (Ammo) | DA_CGM4_Stats.json |
| Launcher_04 | 9K333 Verba | Launcher | Launcher | 800 | 1 | 72mm (Ammo) | DA_Launcher_04_Stats.json |
| MMGL | MGL-40 | Launcher | Launcher | 6000 | 1 | 40mm (Ammo) | DA_MMGL_Stats.json |
| RPG7 | RPG-7 | Launcher | Launcher | 2000 | 1 | 93mm (Ammo) | DA_RPG7_Stats.json |
| Glock17 | GGX 17 | Pistol | Pistol | 200 | 1 | 9mm (Magazine) | DA_Glock17_Stats.json |
| Judge | Judge | Pistol | Pistol | 250 | 1 | 45Colt (Ammo) | MISSING (no stats asset in folder) |
| WEPN_026 | M1911 | Pistol | Pistol | 300 | 1 | 45ACP (Magazine) | DA_WEPN_026_Stats.json |
| WEPN_027 | Deagle | Pistol | Pistol | 900 | 1 | 50AE (Magazine) | DA_WEPN_027_Stats.json |
| WEPN_032 | GGX 18 | Pistol | Pistol | 800 | 1 | 9mm (Magazine) | DA_WEPN_032_Stats.json |
| MP9 | AMP-9 | SMG | SMG | 900 | 1 | 9mm (Magazine) | DA_MP9_Stats.json |
| SMG_03 | PP-19 Vityaz | SMG | SMG | 1200 | 1 | 9mm (Magazine) | DA_SMG_03_Stats.json |
| Vector | Super-45 | SMG | SMG | 2600 | 1 | 45ACP (Magazine) | DA_Vector_Stats.json |
| WEPN_028 | MP5 | SMG | SMG | 1500 | 1 | 9mm (Magazine) | DA_WEPN_028_Stats.json |
| M500 | M500 | Shotgun | Shotgun | 1200 | 1 | 12g (Ammo) | DA_M12G_Stats.json |
| MP43 | MP43 | Shotgun | Shotgun | 400 | 1 | 12g (Ammo) | DA_MP43_Stats.json |
| MK22 | MK22 | Sniper | Sniper | 6400 | 0 | 308Win (Magazine) | DA_MK22_Stats.json |
| Mosin | Mosin Nagant | Sniper | Sniper | 4500 | 1 | 762x54mm (Ammo) | DA_Mosin_Stats.json |
| SR_04 | AMR 50 | Sniper | Sniper | 8800 | 1 | 50Cal (Magazine) | DA_SR_04_Stats.json |
| SV98 | SV98 | Sniper | Sniper | 5200 | 1 | 762x54mm (Magazine) | DA_SV98_Stats.json |
| WEPN_035 | Scout Rifle TD | Sniper | Sniper | 1100 | 1 | 556mm (Ammo) | DA_WEPN_035_Stats.json |

A shown price of 0 is reported as-is for KH2002, A91 and WEPN_033 (see 8.3).

### Per-class summary

| Class | Weapons | IDs | RPM | Muzzle speed | Eff. range | Shown price (non-zero) |
|---|---|---|---|---|---|---|
| AR | 8 | AK74M, M4, KH2002, A91, TAR21, WEPN_029, WEPN_030, WEPN_033 | 650-800 | 71500-95000 | 300-800 | 600-6500 |
| SMG | 4 | Vector, MP9, WEPN_028, SMG_03 | 800-1200 | 37500-40000 | 50-200 | 900-2600 |
| LMG | 2 | LMG_02, M249 | 850 | 82500-91500 | 700-1000 | 3200-4500 |
| DMR | 3 | RFB, SVDM, SKS | 450-480 | 80000-88000 | 500-800 | 2400-6000 |
| Sniper | 5 | SV98, WEPN_035, MK22, Mosin, SR_04 | 41.5-46 | 83000-97500 | 300-2000 | 1100-8800 |
| Shotgun | 2 | M500, MP43 | 120-900 | 39100-48000 | 70 | 400-1200 |
| Pistol | 5 | Judge, Glock17, WEPN_026, WEPN_027, WEPN_032 | 267-1200 | 25300-47000 | 50 | 200-900 |
| Launcher | 4 | Launcher_04, RPG7, MMGL, CGM4 | 75-100 | 2000-23000 | 300-1000 | 800-6000 |

Values are the raw numbers from the stats assets. No unit conversion has been applied.

## 3. Per-weapon ballistics (from the linked `WDWeaponStatsData`)

Column meanings are inferred from property names. `FocusEnergyReductionPerShot` and `RecoilReductionWhenFocussing` are read as a focus-energy cost and recoil relief. `WeaponAccuracy.AccuracyValue` is read as spread, where lower is tighter. None of these are confirmed against code.

| ID | RPM | Muzzle spd | Eff. range | Accuracy | Deviation (deg) | Pitch recoil max | Focus / shot | Recoil relief | View kick x | ADS stab. (s) | Suppression x | Burst | Melee |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A91 | 700 | 71500 | 300 | 1.5 | 15 | - | - | - | - | 0.9 | 1.3 | - | 35 |
| AK74M | 650 | 88000 | 500 | 0.825 | 13 | 45 | 25 | 20 | 1.1 | 1.2 | - | - | 35 |
| KH2002 | 700 | 71500 | 300 | 1.5 | 15 | 45 | 40 | 30 | - | 1.1 | 1.3 | - | 35 |
| M4 | 800 | 91000 | 500 | 0.84 | 10 | 45 | 25 | 20 | 1.08 | 1 | - | - | 35 |
| TAR21 | 750 | 91000 | 550 | 0.87 | 15 | 45 | 40 | 30 | 1.1 | 1 | - | - | 35 |
| WEPN_029 | 650 | 95000 | 400 | 0.73 | 12 | 45 | 25 | 20 | 0.95 | 1.25 | - | - | 35 |
| WEPN_030 | 650 | 84000 | 800 | 0.58 | 16 | 45 | 25 | 20 | - | 1.35 | 0.25 | - | 35 |
| WEPN_033 | 700 | 71500 | 300 | 1.5 | 15 | 45 | 40 | 30 | - | 1.05 | 1.3 | - | 35 |
| RFB | 450 | 88000 | 500 | 0.69 | 10 | 45 | 50 | 30 | 1.15 | 2 | 0.6 | 1 | 35 |
| SKS | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SVDM | 480 | 80000 | 800 | 0.45 | 10 | 45 | 50 | 30 | 0.7 | 1.75 | 0.4 | - | 35 |
| LMG_02 | - | 82500 | 1000 | 2.5 | 20 | 45 | 10 | 50 | 1.25 | 3.5 | 0.45 | - | 40 |
| M249 | 850 | 91500 | 700 | 4.3 | 20 | 45 | 10 | 50 | 1.2 | 3 | - | - | 40 |
| CGM4 | 100 | 23000 | 400 | 2.5 | - | - | - | - | - | 1.75 | - | - | 40 |
| Launcher_04 | 100 | 2000 | 1000 | - | - | - | - | - | - | 2 | - | - | 40 |
| MMGL | 75 | 10000 | 400 | 20 | - | 45 | - | - | - | 1.5 | - | - | 40 |
| RPG7 | 100 | 10000 | 300 | 3 | - | - | - | - | - | 1.5 | - | - | 40 |
| Glock17 | - | 37500 | 50 | 3.49 | 10 | - | 40 | 10 | 1.5 | 0.6 | - | - | 20 |
| Judge | - | - | - | - | - | - | - | - | - | - | - | - | - |
| WEPN_026 | 430 | 25300 | 50 | 2 | 10 | 45 | 40 | 10 | 1.85 | 0.75 | - | - | 20 |
| WEPN_027 | 267 | 47000 | - | 0.84 | - | 45 | 40 | 10 | - | 0.9 | - | - | 20 |
| WEPN_032 | 1200 | 37500 | 50 | 2 | 10 | 45 | 40 | 10 | - | 0.55 | - | - | 20 |
| MP9 | 900 | 40000 | - | 2.1 | 15 | - | 25 | 15 | 1.1 | 0.6 | - | - | 20 |
| SMG_03 | 800 | 38000 | 200 | 1.3 | 17 | 45 | 50 | 30 | - | 0.8 | - | - | 20 |
| Vector | 1200 | 37500 | 50 | 2 | 35 | 45 | 25 | 15 | - | 0.65 | - | - | 20 |
| WEPN_028 | 800 | 40000 | 200 | 1.16 | 20 | 45 | 25 | 15 | 1.1 | 0.7 | - | - | 20 |
| M500 | 120 | 48000 | 70 | 1.5 | 24 | 45 | - | - | 1.6 | 1.1 | - | - | 35 |
| MP43 | 900 | 39100 | - | 3.08 | 28 | 45 | - | - | 1.15 | 1 | - | - | 35 |
| MK22 | 46 | 89400 | 1000 | 0.16 | 4 | 45 | 100 | - | 1.4 | 0.7 | - | - | 40 |
| Mosin | 46 | 86500 | 500 | 0.78 | 4 | 45 | 100 | - | 0.8 | 0.7 | - | - | 40 |
| SR_04 | 41.5 | 90000 | 2000 | 0.11 | 4 | 45 | 100 | - | 1.45 | 0.9 | - | - | 40 |
| SV98 | 46 | 83000 | 1000 | 0.56 | 4 | 45 | 100 | - | 1.3 | 0.8 | - | - | 40 |
| WEPN_035 | 46 | 97500 | 300 | 1.5 | 4 | 45 | 100 | - | 0.3 | 0.55 | - | - | 40 |

`IronSightsAimTime` is set on several launchers to 50000 (for example RPG-7 and 9K333). That is not a plausible value in seconds, so the column is left out of the table. `TypicalSpeed` is present on 20 stats assets. Its relation to `InitialBulletSpeed` is not stated in the data.

---

## 4. Default weapon attributes (`WDItemExtensionData_GameplayEffects`)

Each weapon stores a list of `Attribute.Gameplay.Weapon.*` defaults. Five multipliers are identical on all 33 weapons: `VerticalRecoilMultiplier` 1.0, `HorizontalRecoilMultiplier` 1.0, `AdsZoomMultiplier` 1.2, `SpreadMultiplier` 1.0, `AccuracyMultiplier` 1.0. `Length` is 80.0 on all 33. The varying attributes are below.

| ID | AimTime | EquipSpeedMult | HolsterSpeedMult | MinZeroingRange | MaxZeroingRange |
|---|---|---|---|---|---|
| A91 | 0.525 | 0.92 | 1 | 100 | 100 |
| AK74M | 0.45 | 1 | 1.05 | 100 | 1e+03 |
| KH2002 | 0.525 | 0.95 | 1 | 100 | 100 |
| M4 | 0.49 | 0.95 | 1.1 | 100 | 500 |
| TAR21 | 0.525 | 0.95 | 1 | 100 | 300 |
| WEPN_029 | 0.49 | 0.95 | 1 | 100 | 400 |
| WEPN_030 | 0.5 | 0.95 | 1 | 100 | 600 |
| WEPN_033 | 0.525 | 0.95 | 1 | 100 | 100 |
| RFB | 0.52 | 0.92 | 1 | 100 | 300 |
| SKS | 0.53 | 1.15 | 1.1 | 100 | 1e+03 |
| SVDM | 0.53 | 0.97 | 1 | 100 | 1.1e+03 |
| LMG_02 | 0.73 | 0.95 | 1 | 100 | 1.5e+03 |
| M249 | 0.68 | 0.95 | 0.95 | 200 | 1.2e+03 |
| CGM4 | 0.5 | 0.95 | 1 | 100 | 100 |
| Launcher_04 | 0.5 | absent | 1.15 | 100 | 1e+03 |
| MMGL | 0.4 | 0.95 | 1 | 50 | 400 |
| RPG7 | 0.5 | 0.95 | 1 | 100 | 500 |
| Glock17 | 0.2 | 1.2 | 1.1 | 50 | 50 |
| Judge | 0.35 | 0.95 | 1.15 | 25 | 25 |
| WEPN_026 | 0.2 | 0.92 | 1 | 25 | 25 |
| WEPN_027 | 0.25 | 0.9 | 0.85 | 50 | 50 |
| WEPN_032 | 0.2 | 1.2 | 1.15 | 50 | 50 |
| MP9 | 0.25 | 1.12 | 1.2 | 50 | 100 |
| SMG_03 | 0.285 | 0.94 | 1.15 | 50 | 200 |
| Vector | 0.25 | 1 | 1 | 50 | 100 |
| WEPN_028 | 0.285 | 1.05 | 0.9 | 25 | 100 |
| M500 | 0.365 | 0.95 | 1 | 100 | 100 |
| MP43 | 0.35 | 1.25 | 0.95 | 70 | 70 |
| MK22 | 0.675 | 1.05 | 1.17 | 100 | 300 |
| Mosin | 0.65 | 0.94 | 1 | 200 | 800 |
| SR_04 | 0.68 | 0.9 | 1.15 | 100 | 300 |
| SV98 | 0.6 | 0.95 | 1 | 100 | 100 |
| WEPN_035 | 0.5 | 1 | 1 | 100 | 100 |

"absent" means the key is not in that weapon's list. The engine fallback is not in this folder. `AimTime` is read as the ADS raise time, and the zeroing values are read in the same units as `EffectiveRange`. Both readings are inferred.

---

## 5. Shared handling data

### 5a. ADS transition ranges (all weapons)

| Field | Range across weapons | Weapons with field |
|---|---|---|
| OutSettlePlayTime | 0.7-9 | 28 |
| OutSettleWeight | 0.1-0.7 | 29 |
| OutSettlePlayRate | 0.64 | 26 |
| TransitionVelocity | 0.14-1 | 29 |
| TransitionDamping | 0.5-0.7 | 29 |
| TransitionStrength | 0.8-1.8 | 23 |
| AttachmentOffsetAlphaLerpSpeed | 15-34 | 23 |
| AttachmentEndRange | 0.9-1 | 13 |
| CameraOffsetLerpSpeed | 30-999 | 27 |
| MinWallCollisionAlpha | 0.75-1 | 16 |
| MinBlockAdsWallCollisionAlpha | 0.01-0.3 | 15 |
| SpringLerpWeight | 0.1 | 5 |

### 5b. Spread, stance and holdable

- **Spread:** every weapon has three `SpreadValues` entries (`EBHPlayerStance::Stand`, `Crouch`, `Prone`). Each points at a row of `CT_Weapon_Spread` named `<Class>.<Stance>` (for example `AR.Stand` or `Sniper.Prone`). All stance multipliers are `1.0`, so the live spread numbers are in the curve table, not here.
- **Stance recoil:** weapons with a `StanceGameplayEffects` list point at `GE_Weapon_StanceRecoil_<Class>_<Stance>` effects, with a separate set per class. Launcher_04 has no list.
- **Holdable:** `MeshFovAds` is 80.0 on all 33. Hip offset (`ItemHipOffset`) varies per weapon. It is absent on the launchers.
- **Trace radius (`WeaponTraceRadius`):** 6.0 on most rifles, 8.0 on Launcher_04, 4.0 on the Deagle, 3.0 on the Judge.

### 5c. Input bindings

Every weapon bundle carries a `B_DefaultWeaponInputData_C`. Across the bundles there are 14 distinct bindings. The first 13 appear on all 33 weapons: `Reload`, `SecondaryUse` (and `.Release`), `MeleeBash`, `Player.PrimaryUse` (and `.Release`), `CycleSights`, `CycleFireMode`, `IncreaseZeroing`, `DecreaseZeroing`, `Inspect`, `Bipod.ToggleFold`, `Bipod.Mount`. `Reload.Discard` appears on 24.

The `WDItemInputBehavior_ActivateAction` objects (387 in total) export with empty properties, so what each action does is not visible in this folder.

### 5d. Ammo model

Every weapon has one `Action.Item.PrimaryUse` requirement. It spends `ResourcesUsed = 1` of `RequiredResource` per shot, restricted to the weapon's own items (`bLimitSearchToItem = true`). The resource type is `Item.Resource.Magazine` (fed from a magazine) or `Item.Resource.Ammo` (loose). Section 2 gives both per weapon.

### 5e. Aim assist, audio and mutables

- **Aim assist:** 7 settings assets, one per class (`DA_AimAssistSettings_<Class>`), all sharing `DA_AimAssistFilter`. Weapon count per settings asset: AR 9, SR 8, Pistol 5, RPG 4, SMG 4, Shotgun 2, LMG 1.
- **Audio:** each weapon has one `WDAudioData` with between 31 and 51 sound cues (`SoundAssets`).
- **Mutable:** all 33 weapons point at `/Game/Items/Weapons/Mutable/MUT_MasterWeapon`. Each carries a `DefaultParameters` list of the slots it exposes: `Id.Item` (33), `Item.Attachment.Handguard` (31), `Sight` (30), `Barrel` (30), `Muzzle` (29), `Grip` (28), `Magazine` (28), `Mount{Left,Right,Top,Under}` (28 each), `Stock` (28), `Underbarrel` (28), `CantedSight` (27), `SightMount` (26), `DustCover` (2). The parameter values are not decoded.

---

## 6. Attachments and components

Grouped by folder. "Vendor-priced" counts items that have a `WDVendorData` row. The components have none.

| Folder | Items | Vendor-priced | Shown price | Unlock lvl | With GE effect | Attachment type tags |
|---|---|---|---|---|---|---|
| Muzzle | 40 | 40 | 350-1600 | 1 | 40 | Muzzle |
| Magazines | 28 | 27 | 10-280 | 0,1 | 27 | Magazine |
| Barrels | 21 | 0 | - | - | 0 | Barrel |
| Sights | 18 | 16 | 200-1800 | 1 | 18 | Sight |
| Stocks | 18 | 0 | - | - | 0 | Stock |
| Handguards | 17 | 0 | - | - | 0 | Handguard, Stock |
| Foregrips | 13 | 13 | 540-1400 | 1 | 13 | Bipod, Grip |
| Pistol Grips | 12 | 0 | - | - | 0 | Grip, None |
| Dust Covers | 3 | 0 | - | - | 0 | None |
| Triggers | 3 | 0 | - | - | 0 | Handguard, None |

Every vendor-priced attachment carries a `GE_*` gameplay effect in `AppliedEffects`. The numeric effects are inside those `GE_*` assets, which are not in this folder. Per-attachment stat deltas therefore cannot be given from this dump.

**Magazine class tags** (on the item context): Extended (11), Standard (9), Small (7), Drum (4), Belt (2), Internal (1). These are tags only. Round counts appear in item names, for example "AK74 30 RND Magazine".

**Shotgun choke override:** some muzzles set `bOverrideShotgunData`. For example, `MUZL_012` (`MZL_07`, AR Multi-Caliber Suppressor) sets `ChokeFactor 0.8`, `OuterConeHalfAngle 10`, `InnerConeHalfAngleMultiplier 0.5`, and `FireMuzzleFlashScaleMultiplier 0.2`.

**Attachment type tags are inconsistent:** two of three triggers (`TRGR_002`, `TRGR_003`) are tagged `Item.Attachment.Handguard`. One stock in `Handguards` is tagged `Item.Attachment.Stock`. Two pistol grips and one trigger have no attachment type. The effect of this on slot fitting is not verified.

**Multiple vendor variations:** magazine vendor rows hold 7 variations each. The first is shown (`bShowInVendor = true`) and the rest are hidden price points. For example, `MAGZ_002` shows 20 and hides 27, 27, 30, 30, 34, 34. The hidden variations are not decoded.

**Weight:** attachments range from 0.03 (sights) to 2.2 (magazines). Foregrips range 0.08 to 0.7.

---

## 7. Bundle wiring

- `GameFeatureData` (276): one per bundle. Each scans its own `/<Bundle>/Data` folder for `BH.Item` assets, marked `AlwaysCook`.
- `GameFeatureAction_DataRegistrySource` (138): registers `DT_VendorData_Ext_*` into the `VendorData` registry and `DT_EntityData_Ext_*` into `EntityData_UI`. Both are client and server sources.
- `GameFeatureAction_AddWorldPartitionContent` (259): adds an External Data Layer, for example `EDL_AR_01`.
- Entity-UI rows (`BHEntityData_UI`, 111 tables) hold display name (string-table key), description, category tag and icons. Vendor rows (`WDVendorData`, 128 tables) hold the variations described above.

---

## 8. Anomalies and data-quality notes

1. **WEPN_033 stats asset is a copy.** `DA_WEPN_033_Stats` has `WeaponId = Id.Item.TAR21` and values 700 RPM, 71,500 speed, 300 range, which match the A-91 family. `TAR21` already has its own stats asset (`DA_TAR21_Stats`, 750 RPM, 91,000 speed, 550 range). The `WEPN_033` item loads its own file, so its live values are the copied ones.
2. **Missing stats assets.** `Pistol_02` (Judge) references `DA_Judge_Stats` and `WEPN_007` (SKS) references `DA_SKS_Stats`. Neither exists in this folder, so their ballistics are unknown here.
3. **Zero shown prices.** `KH2002`, `A91` and `WEPN_033` are shown at price 0 with unlock level 1. The data does not say whether this means unreleased, free or unpriced.
4. **Launcher `IronSightsAimTime = 50000`.** Not a time value. Meaning unknown.
5. **Attachment type tags** are inconsistent (section 6).
6. **No vendor row for 77 of 173 parts.** That is all 74 `Components` items, plus 3 attachments (2 sights and 1 magazine). The 74 components are probably weapon-specific and unlocked by ownership, but the unlock path is not in this folder.

---

## 9. How the values combine

- **Price and unlock:** the shown vendor variation sets the price and `LevelToUnlock`. Hidden variations never appear in the shop.
- **Attachments:** a fitted attachment applies the `GE_*` effects in its `AppliedEffects`. Those effects are not in this folder, so the net stat change of a build cannot be computed here.
- **Ammo:** one unit of `RequiredResource` is spent per primary-fire shot, from the weapon's own magazine or ammo pool.
- **Spread and recoil:** base values sit in `WDWeaponStatsData` and the `CT_Weapon_Spread` curve table. Attribute multipliers (all 1.0 except `AdsZoomMultiplier` at 1.2) apply on top. How the runtime combines them is not in this folder.

---

## 10. Still not pulled / limitations

- **`GE_*` gameplay effects** (attachment stat changes, stance recoil modifiers, default attribute effects) are referenced but not in this folder. Numeric attachment effects are the largest gap.
- **Curves:** ADS, recoil, view kick, sway and falloff curves are present as `EditorCurveData` keyframes inside `WDWeaponStatsData`, and as 7 `CurveFloat` objects. They are not decoded.
- **`WDItemInputBehavior_ActivateAction`** exports with empty payloads, so the action logic is not visible.
- **Mutable parameters** (`MUT_MasterWeapon`) are listed by key only. Option lists and default textures are not summarized.
- **Camera data** (`WDItemsmithDataFragment_CameraData`, 32) and **animation sets** (`BHAnimationSet`, 39) are counted but not decoded.
- **Missing stats:** Judge and SKS (section 8).
- **Units and meanings** of accuracy, deviation, focus energy, recoil relief, `TypicalSpeed`, `AimTime` and the zeroing values are inferred from property names.
- **Outside this folder:** the `Content/Weapons` tree and the `GameMechanics` damage and reward tables are not covered here.

