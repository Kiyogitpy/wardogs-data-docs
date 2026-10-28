---
title: "Weapons Game Feature"
redirect_from: ["/Wardogs_GameFeatures_Weapons_v2.html", "/Wardogs_GameFeatures_Weapons_v2"]
parent: "Weapons & Ammo"
description: "The weapon package: roster, per-weapon ballistics, default attributes, shared handling data and bundle wiring."
---

# Wardogs — GameFeatures/Weapons Reference

*Source: `Wardogs/Plugins/GameFeatures/Weapons/` (1013 JSON files, 3905 exported objects, 0 parse errors). Parsed with a Python script that splits each file on its `--- export:` headers, since many files hold several objects. Values are cooked data as exported. Where a meaning is inferred from a property name, the text says so.*

> **Scope:** this folder holds the per-item GameFeature bundles: inventory definitions, weapon ballistics, vendor rows, attachment wiring, input bindings, audio and mutables. The `Content/Weapons` tree is covered by a separate doc.

## Season 02 update (2026-10-15)

- **Four new ranged weapons**, all with unlock level 1 and bundles under `Platforms/`: `WEPN_037` TCX-SPR (AR, shown price 3200), `WEPN_031` PP-19 Bizon (SMG, 1000), `WEPN_036` Evo-3 Ultra (LMG, 7250), and `WEPN_034` M14 (DMR, 7400). Ranged weapons go from 33 to 37.
- **Mosin moved.** Its item, stats and vendor data now sit under `Platforms/WEPN_017` (stats asset `DA_WEPN_017_Stats.json`). 11 files under `Sniper/Mosin` no longer exist at that path. Its values are unchanged except suppression x, which is now 1.5.
- **Shown prices, old → new:** AK74M 1600 → 800, TAR21 600 → 1200, WEPN_029 2200 → 2000, WEPN_030 6500 → 6000, RFB 6000 → 6250, LMG_02 4500 → 4100, CGM4 2600 → 2400, MMGL 6000 → 7500, RPG7 2000 → 1800, WEPN_027 900 → 750, WEPN_032 800 → 1000, MP9 900 → 1375, Vector 2600 → 5600, WEPN_028 1500 → 1800, SR_04 8800 → 14800, WEPN_035 1100 → 1200.
- **Suppression x, old → new:** LMG_02 0.45 → 0.9 and SVDM 0.4 → 0.8. New values where the old doc had `-`: AK74M 1.05, M4 0.95, M249 1.25, MK22 1.6, SR_04 2.0, SV98 1.5, Vector 0.8, WEPN_035 1.5, Mosin 1.5.
- **View kick x, old → new:** RFB 1.15 → none, SVDM 0.7 → none, WEPN_028 1.1 → 1.15. WEPN_037 is new at 0.9.
- **MMGL muzzle speed:** 10000 → 7500.
- **Attachments and components:** 99 → 119 attachment items (Muzzle 40 → 49, Sights 18 → 21, Magazines 28 → 34, Foregrips 13 → 15). Components 74 → 87.
- **New vehicle weapon bundles:** `VehicleWeaponry/` (MWSY_001 mounted heavy machine gun, MWSY_002). These are not in the ranged roster.
- **Input bindings:** `Reload.Discard` is now bound on 28 of 37 weapons (was 24). The 14 binding names are unchanged.
- **Totals:** 870 → 1013 JSON files and 3383 → 3905 exported objects.
- **Not tabulated here:** recoil patterns, aim sway and other curves changed on many weapons. Their values are not in this doc.

Full before/after list: [Season 2 Changes → Weapons & Ammo]({{ '/season-2-changes/weapons-ammo.html' | relative_url }}).

---

## 1. Folder layout

Each subfolder is one content bundle. A bundle has a `GameFeatureData` manifest, usually a `GameFeatureAction_DataRegistrySource` (which registers the vendor and entity-UI tables), and a `GameFeatureAction_AddWorldPartitionContent` (which adds an External Data Layer). Item definitions live in `Data/ID_*.json`.

| Group | Files | Item defs | Ranged-weapon exts | Weapon stats assets | GameFeatureData | DataTables |
|---|---|---|---|---|---|---|
| AR | 10 | 0 | 0 | 0 | 6 | 0 |
| SMG | 67 | 5 | 1 | 1 | 5 | 2 |
| LMG | 61 | 5 | 1 | 1 | 2 | 2 |
| DMR | 113 | 8 | 2 | 2 | 2 | 3 |
| Sniper | 130 | 12 | 2 | 2 | 4 | 4 |
| Shotgun | 54 | 5 | 1 | 1 | 2 | 1 |
| Pistols | 51 | 3 | 1 | 0 | 4 | 2 |
| Launchers | 88 | 3 | 2 | 2 | 4 | 2 |
| Platforms | 1134 | 35 | 27 | 26 | 27 | 42 |
| Attachments | 1609 | 119 | 0 | 0 | 141 | 225 |
| Components | 581 | 87 | 0 | 0 | 122 | 0 |
| VehicleWeaponry | 7 | 1 | 0 | 1 | 2 | 0 |

Notes on the layout:

- `AR/AR_01` to `AR_07` (six folders, 10 files) hold only GameFeature shells: 6 `GameFeatureData` and 4 world-partition actions. The AR-class item definitions are not in this folder.
- `Platforms/WEPN_0xx` (27 folders) holds the full bundles for the newer weapons. The older hand-named bundles sit in `DMR`, `Sniper`, `LMG`, `Shotgun`, `SMG`, `Pistols` and `Launchers` (`RFB`, `SVDM`, `MK22`, `Mosin`, `SR_04`, `MP43`, `SMG_03`, `LMG_02`, `Pistol_02`, `Launcher_04`, `RPG7`). The Mosin item and stats data now also sit under `Platforms/WEPN_017`.
- `Attachments/` holds 119 attachment items (Foregrips 15, Magazines 34, Muzzle 49, Sights 21), of which 113 have vendor rows. `Components/` holds 87 weapon-specific items (Barrels 25, Handguards 20, Pistol Grips 15, Stocks 21, Triggers 3, Dust Covers 3), none of which have vendor rows.

**Object types (3905 exported objects):**

| Type | Count | What it holds |
|---|---|---|
| WDItemInputBehavior_ActivateAction | 435 | Input action bindings (payload is empty in this export) |
| GameFeatureData | 321 | Bundle manifest; scans `BH.Item` assets under `/<Bundle>/Data` |
| GameFeatureAction_AddWorldPartitionContent | 303 | Adds an External Data Layer (`EDL_*`) |
| BHInventoryItemDefinition | 283 | Item root: `ItemId`, display name, `ItemContext` tags, `DataFragments` |
| DataTable | 283 | Vendor rows (`WDVendorData`) and entity UI rows (`BHEntityData_UI`) |
| WDInventoryFragment_Gunsmith | 271 | Gunsmith item type (Attachment, Weapon, etc.) |
| WDInventoryFragment_Attachment | 245 | Attachment type tag, applied GameplayEffects, removal flags |
| WDInventoryFragment_Audio | 221 | Pointer to a `WDAudioData` asset |
| BHInventoryFragment_CustomShape | 165 | Inventory shape fragment (no properties exported) |
| BHInventoryFragment_Droppable | 165 | Dropped-world mesh reference |
| BHInventoryFragment_UserInterface | 165 | UI fragment (no properties exported) |
| GameFeatureAction_DataRegistrySource | 160 | Registers DataTables into the `VendorData` / `EntityData_UI` registries |
| BHInventoryFragment_Weight | 162 | Item weight (units not stated) |
| BHInventoryFragment_SubSlotSupport | 119 | Sub-slot containers (what can be fitted or loaded) |
| WDItemInputBehavior_CompleteAction | 74 | Release-side input actions |
| BHAnimationSet | 45 | Animation set reference |
| B_DefaultWeaponInputData_C | 37 | Per-weapon input table (14 bindings) |
| BHItemExtensionData_AimAssistExtension | 37 | Aim-assist settings and filter assets |
| WDInventoryFragment_ItemActor | 37 | Container for the extension-data fragments |
| WDItemExtensionData_Animation | 37 | Animation set reference |
| WDItemExtensionData_AudioExtension | 37 | Audio asset reference |
| WDItemExtensionData_GameplayEffects | 37 | Default weapon attributes (`Attribute.Gameplay.Weapon.*`) |
| WDItemExtensionData_Holdable | 37 | Equip/holster montages, hip offset, FOV when ADS |
| WDItemExtensionData_Inventory | 37 | Ammo requirement for primary fire |
| WDItemExtensionData_Mutable | 37 | Customization parameters on `MUT_MasterWeapon` |
| WDItemExtensionData_RangedWeapon | 37 | Stats link, spread, stance effects, ADS transition, damage tag |
| WDAudioData | 38 | Sound list per weapon (and one for the vehicle machine gun) |
| WDItemsmithDataFragment_CameraData | 36 | Gunsmith camera framing |
| WDWeaponStatsData | 36 | Ballistics, recoil, aim sway, ADS curves (`DA_*_Stats`) |
| CurveFloat | 7 | Standalone float curves: five bipod camera-offset curves and two ADS curves, keys in [Ranged Weapon Item Fields](../content/Wardogs_RangedWeaponFields_v1.md) |
| WDInventoryFragment_TransferTime | 1 | Item fragment, present once (on `Launcher_04`): `TransferTime` 3.5 s ([Ranged Weapon Item Fields](../content/Wardogs_RangedWeaponFields_v1.md)) |

---

## 2. Weapon roster (37 ranged weapons)

Each weapon is found through its `WDItemExtensionData_RangedWeapon`, which names its `WDWeaponStatsData` asset. Price and unlock level come from the vendor variation with `bShowInVendor = true`. "Class" is the first segment of the damage tag (`Meta.Damage.Weapon.<Class>.*`). It is the most consistent family label in the data.

| ID | Display name | Class | Archetype tag | Shown price | Unlock lvl | Primary-fire ammo (type) | Stats asset |
|---|---|---|---|---|---|---|---|
| A91 | A-91 | AR | AR | 0 | 1 | 556mm (Magazine) | DA_A91_Stats.json |
| AK74M | AK74 | AR | AR | 800 | 1 | 545mm (Magazine) | DA_AK74M_Stats.json |
| KH2002 | KH-2002 | AR | AR | 0 | 1 | 556mm (Magazine) | DA_KH2002_Stats.json |
| M4 | M4 | AR | AR | 2800 | 1 | 556mm (Magazine) | DA_M4_Stats.json |
| TAR21 | T-21 | AR | AR | 1200 | 1 | 556mm (Magazine) | DA_TAR21_Stats.json |
| WEPN_029 | Galil | AR | AR | 2000 | 1 | 556mm (Magazine) | DA_WEPN_029_Stats.json |
| WEPN_030 | FAL | AR | AR | 6000 | 1 | 308Win (Magazine) | DA_WEPN_030_Stats.json |
| WEPN_033 | Bushmaster M17S | AR | AR | 0 | 1 | 556mm (Magazine) | DA_WEPN_033_Stats.json (copy, see 8.1) |
| WEPN_037 | TCX-SPR | AR | DMR | 3200 | 1 | 762mm (Magazine) | DA_WEPN_037_Stats.json |
| RFB | BMR-308 | DMR | DMR | 6250 | 1 | 308Win (Magazine) | DA_RFB_Stats.json |
| SKS | SKS | DMR | DMR | 2400 | 1 | 762mm (Ammo) | MISSING (no stats asset in folder) |
| SVDM | SVD | DMR | DMR | 4800 | 1 | 762x54mm (Magazine) | DA_SVDM_Stats.json |
| WEPN_034 | M14 | DMR | DMR | 7400 | 1 | 308Win (Magazine) | DA_WEPN_034_Stats.json |
| LMG_02 | PKM | LMG | LMG | 4100 | 1 | 762x54mm (Magazine) | DA_LMG_02_Stats.json |
| M249 | M249 SAW | LMG | LMG | 3200 | 1 | 556mm (Magazine) | DA_M249_Stats.json |
| WEPN_036 | Evo-3 Ultra | LMG | LMG | 7250 | 1 | 308Win (Magazine) | DA_WEPN_036_Stats.json |
| CGM4 | MAAWS | Launcher | Launcher | 2400 | 1 | 84mm (Ammo) | DA_CGM4_Stats.json |
| Launcher_04 | 9K333 Verba | Launcher | Launcher | 800 | 1 | 72mm (Ammo) | DA_Launcher_04_Stats.json |
| MMGL | MGL-40 | Launcher | Launcher | 7500 | 1 | 40mm (Ammo) | DA_MMGL_Stats.json |
| RPG7 | RPG-7 | Launcher | Launcher | 1800 | 1 | 93mm (Ammo) | DA_RPG7_Stats.json |
| Glock17 | GGX 17 | Pistol | Pistol | 200 | 1 | 9mm (Magazine) | DA_Glock17_Stats.json |
| Judge | Judge | Pistol | Pistol | 250 | 1 | 45Colt (Ammo) | MISSING (no stats asset in folder) |
| WEPN_026 | M1911 | Pistol | Pistol | 300 | 1 | 45ACP (Magazine) | DA_WEPN_026_Stats.json |
| WEPN_027 | Deagle | Pistol | Pistol | 750 | 1 | 50AE (Magazine) | DA_WEPN_027_Stats.json |
| WEPN_032 | GGX 18 | Pistol | Pistol | 1000 | 1 | 9mm (Magazine) | DA_WEPN_032_Stats.json |
| MP9 | AMP-9 | SMG | SMG | 1375 | 1 | 9mm (Magazine) | DA_MP9_Stats.json |
| SMG_03 | PP-19 Vityaz | SMG | SMG | 1200 | 1 | 9mm (Magazine) | DA_SMG_03_Stats.json |
| Vector | Super-45 | SMG | SMG | 5600 | 1 | 45ACP (Magazine) | DA_Vector_Stats.json |
| WEPN_028 | MP5 | SMG | SMG | 1800 | 1 | 9mm (Magazine) | DA_WEPN_028_Stats.json |
| WEPN_031 | PP-19 Bizon | SMG | SMG | 1000 | 1 | 9mm (Magazine) | DA_WEPN_031_Stats.json |
| M500 | M500 | Shotgun | Shotgun | 1200 | 1 | 12g (Ammo) | DA_M12G_Stats.json |
| MP43 | MP43 | Shotgun | Shotgun | 400 | 1 | 12g (Ammo) | DA_MP43_Stats.json |
| MK22 | MK22 | Sniper | Sniper | 6400 | 0 | 308Win (Magazine) | DA_MK22_Stats.json |
| Mosin | Mosin Nagant | Sniper | Sniper | 4500 | 1 | 762x54mm (Ammo) | DA_WEPN_017_Stats.json |
| SR_04 | AMR 50 | Sniper | Sniper | 14800 | 1 | 50Cal (Magazine) | DA_SR_04_Stats.json |
| SV98 | SV98 | Sniper | Sniper | 5200 | 1 | 762x54mm (Magazine) | DA_SV98_Stats.json |
| WEPN_035 | Scout Rifle TD | Sniper | Sniper | 1200 | 1 | 556mm (Ammo) | DA_WEPN_035_Stats.json |

A shown price of 0 is reported as-is for KH2002, A91 and WEPN_033 (see 8.3).

### Per-class summary

| Class | Weapons | IDs | RPM | Muzzle speed | Eff. range | Shown price (non-zero) |
|---|---|---|---|---|---|---|
| AR | 9 | AK74M, M4, KH2002, A91, TAR21, WEPN_029, WEPN_030, WEPN_033, WEPN_037 | 650-800 | 70000-95000 | 300-800 | 800-6000 |
| SMG | 5 | Vector, MP9, WEPN_028, SMG_03, WEPN_031 | 700-1200 | 37500-40000 | 50-200 | 1000-5600 |
| LMG | 3 | LMG_02, M249, WEPN_036 | 700-850 | 79000-91500 | 700-1000 | 3200-7250 |
| DMR | 4 | RFB, SVDM, SKS, WEPN_034 | 450-700 | 80000-88000 | 500-800 | 2400-7400 |
| Sniper | 5 | SV98, WEPN_035, MK22, Mosin, SR_04 | 41.5-46 | 83000-97500 | 300-2000 | 1200-14800 |
| Shotgun | 2 | M500, MP43 | 120-900 | 39100-48000 | 70 | 400-1200 |
| Pistol | 5 | Judge, Glock17, WEPN_026, WEPN_027, WEPN_032 | 267-1200 | 25300-47000 | 50 | 200-1000 |
| Launcher | 4 | Launcher_04, RPG7, MMGL, CGM4 | 75-100 | 2000-23000 | 300-1000 | 800-7500 |

Values are the raw numbers from the stats assets. No unit conversion has been applied.

## 3. Per-weapon ballistics (from the linked `WDWeaponStatsData`)

Column meanings are inferred from property names. `FocusEnergyReductionPerShot` and `RecoilReductionWhenFocussing` are read as a focus-energy cost and recoil relief. `WeaponAccuracy.AccuracyValue` is the full angle of the accuracy cone (milliradians by default, minutes of angle when `AccuracyType` says so; lower is tighter), confirmed against code on [Weapon Spread](../pipelines/Wardogs_WeaponSpread_v1.md). The other columns are still inferred from property names.

| ID | RPM | Muzzle spd | Eff. range | Accuracy | Deviation (deg) | Pitch recoil max | Focus / shot | Recoil relief | View kick x | ADS stab. (s) | Suppression x | Burst | Melee |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A91 | 700 | 71500 | 300 | 1.5 | 15 | 1* | 0* | 0* | 1* | 0.9 | 1.3 | 3* | 35 |
| AK74M | 650 | 88000 | 500 | 0.825 | 13 | 45 | 25 | 20 | 1.1 | 1.2 | 1.05 | 3* | 35 |
| KH2002 | 700 | 71500 | 300 | 1.5 | 15 | 45 | 40 | 30 | 1* | 1.1 | 1.3 | 3* | 35 |
| M4 | 800 | 91000 | 500 | 0.84 | 10 | 45 | 25 | 20 | 1.08 | 1 | 0.95 | 3* | 35 |
| TAR21 | 750 | 91000 | 550 | 0.87 | 15 | 45 | 40 | 30 | 1.1 | 1 | 1* | 3* | 35 |
| WEPN_029 | 650 | 95000 | 400 | 0.73 | 12 | 45 | 25 | 20 | 0.95 | 1.25 | 1* | 3* | 35 |
| WEPN_030 | 650 | 84000 | 800 | 0.58 | 16 | 45 | 25 | 20 | 1* | 1.35 | 0.25 | 3* | 35 |
| WEPN_033 | 700 | 71500 | 300 | 1.5 | 15 | 45 | 40 | 30 | 1* | 1.05 | 1.3 | 3* | 35 |
| WEPN_037 | 800 | 70000 | 400 | 0.58 | 14 | 45 | 50 | 30 | 0.9 | 1 | 0.4 | 1 | 35 |
| RFB | 450 | 88000 | 500 | 0.69 | 10 | 45 | 50 | 30 | 1* | 2 | 0.6 | 1 | 35 |
| SKS | 420 | 73500 | 400 | 0.73 | 5.5 | 45 | 50 | 30 | 1* | 2 | 1.1 | 3* | 35 |
| SVDM | 480 | 80000 | 800 | 0.45 | 10 | 45 | 50 | 30 | 1* | 1.75 | 0.8 | 3* | 35 |
| WEPN_034 | 700 | 85300 | 500 | 0.73 | 10 | 45 | 50 | 30 | 1* | 2 | 0.5 | 1 | 35 |
| LMG_02 | 600* | 82500 | 1000 | 2.5 | 20 | 45 | 10 | 50 | 1.25 | 3.5 | 0.9 | 3* | 40 |
| M249 | 850 | 91500 | 700 | 4.3 | 20 | 45 | 10 | 50 | 1.2 | 3 | 1.25 | 3* | 40 |
| WEPN_036 | 700 | 79000 | 1000 | 0.73 | 15 | 45 | 10 | 50 | 1* | 4 | 0.6 | 3* | 40 |
| CGM4 | 100 | 23000 | 400 | 2.5 | 5* | 1* | 0* | 0* | 1* | 1.75 | 1* | 3* | 40 |
| Launcher_04 | 100 | 2000 | 1000 | 1* | 5* | 1* | 0* | 0* | 1* | 2 | 1* | 3* | 40 |
| MMGL | 75 | 7500 | 400 | 20 | 5* | 45 | 0* | 0* | 1* | 1.5 | 1* | 3* | 40 |
| RPG7 | 100 | 10000 | 300 | 3 | 5* | 1* | 0* | 0* | 1* | 1.5 | 1* | 3* | 40 |
| Glock17 | 600* | 37500 | 50 | 3.49 | 10 | 1* | 40 | 10 | 1.5 | 0.6 | 1* | 3* | 20 |
| Judge | 200 | 33500 | 50 | 3.49 | 10 | 45 | 40 | 10 | 1* | 1.5 | 1* | 3* | 20 |
| WEPN_026 | 430 | 25300 | 50 | 2 | 10 | 45 | 40 | 10 | 1.85 | 0.75 | 1* | 3* | 20 |
| WEPN_027 | 267 | 47000 | 100* | 0.84 | 5* | 45 | 40 | 10 | 1* | 0.9 | 1* | 3* | 20 |
| WEPN_032 | 1200 | 37500 | 50 | 2 | 10 | 45 | 40 | 10 | 1* | 0.55 | 1* | 3* | 20 |
| MP9 | 900 | 40000 | 100* | 2.1 | 15 | 1* | 25 | 15 | 1.1 | 0.6 | 1* | 3* | 20 |
| SMG_03 | 800 | 38000 | 200 | 1.3 | 17 | 45 | 50 | 30 | 1* | 0.8 | 1* | 3* | 20 |
| Vector | 1200 | 37500 | 50 | 2 | 35 | 45 | 25 | 15 | 1* | 0.65 | 0.8 | 3* | 20 |
| WEPN_028 | 800 | 40000 | 200 | 1.16 | 20 | 45 | 25 | 15 | 1.15 | 0.7 | 1* | 3* | 20 |
| WEPN_031 | 700 | 38000 | 200 | 1.3 | 17 | 45 | 50 | 30 | 1* | 0.8 | 1* | 3* | 20 |
| M500 | 120 | 48000 | 70 | 1.5 | 24 | 45 | 0* | 0* | 1.6 | 1.1 | 1* | 3* | 35 |
| MP43 | 900 | 39100 | 100* | 3.08 | 28 | 45 | 0* | 0* | 1.15 | 1 | 1* | 3* | 35 |
| MK22 | 46 | 89400 | 1000 | 0.16 | 4 | 45 | 100 | 0* | 1.4 | 0.7 | 1.6 | 3* | 40 |
| Mosin | 46 | 86500 | 500 | 0.78 | 4 | 45 | 100 | 0* | 0.8 | 0.7 | 1.5 | 3* | 40 |
| SR_04 | 41.5 | 90000 | 2000 | 0.11 | 4 | 45 | 100 | 0* | 1.45 | 0.9 | 2.0 | 3* | 40 |
| SV98 | 46 | 83000 | 1000 | 0.56 | 4 | 45 | 100 | 0* | 1.3 | 0.8 | 1.5 | 3* | 40 |
| WEPN_035 | 46 | 97500 | 300 | 1.5 | 4 | 45 | 100 | 0* | 0.3 | 0.55 | 1.5 | 3* | 40 |

`*` marks a value the asset omits. An omitted property takes the class default, so these cells show the constructor value, not "no value" (**Data** for the omission, **Native** for the value; the `-` that remained are cells for properties this table does not read). SKS now shows its own values; the old row was all `-` although `DA_SKS_Stats` carries them.

**Native: class defaults of `WDWeaponStatsData`.** The export drops every property equal to the class default, so `DA_LMG_02_Stats` (PKM) has no `RoundsPerMinute` key and uses the default. `UWDWeaponStatsData` is 0x11D0 bytes with a `WDWeaponStats` struct (0xE48 bytes) at +0x38. The class constructor wrapper at RVA `0x6BBCDF0` sets the vtable (`0xB32BAB0`), copies a global tag (RVA `0xD2692F8`, not decoded) into `WeaponId` at +0x30, calls the struct constructor at RVA `0x699E6C0` for `WeaponStats`, then the `BackBlast` constructor at +0xE80. The struct constructor writes `RoundsPerMinute` (+0x138) = 600.0 (dword `0x44160000`) and these other defaults (struct offsets in brackets): `InitialBulletSpeed` 100000 [0xDA0], `EffectiveRange` 100 [0xDA4], `WeaponAccuracy.AccuracyValue` 1.0 [0x4], `RandomDeviationDegree` 5.0 [0xCE0], `RecoilPatternPitchMax` 1.0 [0xCB8], `FocusEnergyReductionPerShot` 0 [0x94], `RecoilReductionWhenFocussing` 0 [0x9C], `ViewKickMagnitudeMultiplier` 1.0 [0xB78], `AdsStabilizationData.AdsStabilizeTime` 0.5 [0xAC0], `SuppressionMultiplier` 1.0 [0xDA8], `RoundsPerBurst` 3 [0x150], `MeleeDamage` 25 [0xDAC], `Min/Max/ZeroingRange` 100 and `ZeroingStep` 100 [0x160-0x168]; `SupportedFireModes` is an empty array [0x140]. The exported default of the Blueprint copy of the struct (`B_Action_WeaponFire.Weapon Stats`, round-8 export, not published) independently shows `RoundsPerMinute` 600.0, `RoundsPerBurst` 3, `IronSightsAimTime` 0.2 and zeroing 100/100/100. Reproduce the cell fill with `python _tools/weapon_stats_defaults.py --check`.

**Rate of fire (consumer found).** **Native:** `UWDWeaponComponent` keeps its own copy of the 0xE48-byte stats struct at component `+0x140` (`0x1D2C340`: `lea rax, [rcx+0x140]`), so `RoundsPerMinute` is read at component `+0x278`. The one-line getter `0x5F7ED10` returns that float (`*(float*)(a1+0x138)`). The start-fire routine `0x6B980A0` (`UWDWeaponComponent` vtable slot 175) calls it with `component+0x140` and computes the shot interval as **`interval = 59.999996 / RoundsPerMinute` seconds** (constant `0x426FFFFF` at RVA `0xB2D3C08`, 60.0 minus one float step; the call is at `0x6B981C1`, the `divss` at `0x6B981D9`). It takes the world time (double at `+0x840` of the world object) minus the last-shot time (float at component `+0xFE8`) as the time since the last shot. If that is outside `(0, interval)` (or no shot yet) it fires at once through `0x6B94700` (the body of `Timer_FireWeapon`, exec thunk `0x6B99AB0`) and, in the fire modes held as 1 or 2 at `+0xF88`, starts a looping `FTimerManager::SetTimer` (`0x143AB8810`, handle at `+0x10F0`) with rate = interval; if the remaining wait is 0.1 s or less it sets a one-shot timer for the remainder and then the loop; if more than 0.1 s it does nothing yet. The timer delegate `0x6B98950` calls the same `0x6B94700`. **Derived:** the PKM at 600 RPM therefore fires every 0.1 s (0.099999994 s). Other readers of the getter: AI shoot task `0x887AD30` (`60.0 / RPM`), AI weapon-data field 6 `RoundsPerMinute` (`0x6A73020`, enum `EAIWeaponDataField`), `0x867A3A0`, `0x867A550`, `0x6F1C310` (Itemsmith stats query, display only; decoded in round 27 below), `0x6AB46A0` (classified in round 26 as audio). The Blueprint `B_Action_WeaponFire` plays no part in the cadence: it copies the struct into its `Weapon Stats` variable (`@4919`) but never reads `RoundsPerMinute`, and its `FireRateMs` variable (`+0x164`) has no reader in the listing. A second copy, `FWDWeaponStatsQueryData.RoundsPerMinute` (+0x28), feeds the Itemsmith `FireRateText` UI only. **Not found:** no `Attribute.Gameplay.Weapon.*` name concerns fire rate (the 14 names in `data/` and the attribute doc are AimTime, recoil, spread, accuracy, equip/holster speed, zoom, zeroing, length, detonator range, focus energy), no GameplayEffect in `data/` touches LMG_02, and the getter returns the raw float, so nothing was found that scales the 600. **Search done:** capstone scan of the whole `.text` for float loads from `[reg+0x138]`, `[reg+0x170]`, `[reg+0x270]`, `[reg+0x3D0]` within 160 bytes of a 60.0, 1/60, 60000 or 1000 constant (negative), then the weapon-component range `0x6B80000-0x6BC0000` for those constants (positive: `0x6B981C6`).

**Rate of fire: how the component's copy is filled, and whether anything rewrites it (round 18).** *Evidence: static-analysis image only, not devirtualized; decompilation and disassembly are not equivalence proof, and nothing was run.* **Native:** the data chain is item `ID_*` -> `WDItemExtensionData_RangedWeapon.WeaponStats` (data asset `+0x98`, the `WDWeaponStatsData` asset) -> `UWDWeaponComponent.InitWeapon(const UWDWeaponStatsData*)` -> the component's embedded stats struct at `+0x140` -> the start-fire routine. Details:
- `UWDWeaponComponent` has two stats-asset pointers: `DefaultWeaponStatsData` at `+0x128` (SDK, an editable class default) and `ActiveWeaponStatsData` at `+0x130`. `InitWeapon` is `UWDWeaponComponent` vtable slot 171 (vtable slot 175 is start-fire; the slot pointer `0xB3155E0` holds RVA `0x6B96720`). It stores the asset in `+0x130`, takes the asset's stats struct with the one-line getter `0x17E78D0` (`lea rax,[rcx+0x38]`), copy-assigns it over the component's struct at `+0x140` through `0x6B8F5A0` (the struct copy visits `RoundsPerMinute` at struct `+0x138`, so component `+0x278`), and copies the first `SupportedFireModes` entry into the fire-mode byte at `+0xF88`.
- Callers that pass a stats asset: the ranged-weapon item extension (`0x6C99700`-`0x6C9976E`: checks the loaded data's class, then calls `WeaponComponent(+0x128 of the extension)->vtable[0x558](data +0x98)`), the component's own default path (`0x6B902E0`-`0x6B90315`: passes `DefaultWeaponStatsData` +0x128), and the vehicle weapon extension (`0x7647B5D`-`0x7647B75`, extension data `+0x80`). The vtable-offset-0x558 call exists in about 60 places because other classes share the offset; only these three were matched to a stats asset. The remaining sites were not individually classified (open).
- A component that never receives an asset keeps the constructor value: the component constructor (`0x6B8E5A0`) calls the struct constructor `0x699E6C0` on `+0x140` (call at `0x6B8E65B`), so RPM is 600 until `InitWeapon` runs.
- **No rewrite found.** `RoundsPerMinute` is read only through the getter `0x5F7ED10` (direct `call rel32` sites found by byte scan: `0x6A73073`, `0x6AB4BAF`, `0x6B981C1`, `0x6F1C57B`, `0x6F1C616`, `0x867A44A`, `0x867A5F6`, `0x887B15D`; only `0x6B981C1` is in the weapon component; indirect calls are not covered). In the weapon-component code (`0x6B80000-0x6BC0000`) nothing stores to component `+0x278`; no instruction that writes the `+0x140` struct was found other than the struct copy routines (`0x6B8F5A0`, called by `InitWeapon`, and `0x6B8416D`, which round 20 found copies a different struct). The only component-level "modifier" field is `InitialBulletSpeedModifier` (`+0x114`, bullet speed, set by `SetInitialBulletSpeedModifier`). No attribute name or gameplay effect in the data concerns fire rate (see above), and fire-mode code was not seen touching the float (`CycleFireMode` was read in round 20: it stores only the fire-mode byte, see below). So item data, via the asset, is the only source of the interval, and the 600 default applies whenever the asset omits `RoundsPerMinute`.
- **Not verified (open):** (b) per-site classification of the other `vtable[0x558]` calls outside the weapon, item-extension and vehicle ranges (round 20 classified the ones inside them, below); (d) runtime confirmation, since the image was never executed. Items (a), (c) and the `CycleFireMode` question were worked in round 20 (next paragraph).
- **Virtualization check.** The protection layer's dispatch stubs (the `mov reg,[rip+x]; jmp [reg+disp]` pattern) were scanned with the project classifier over the bodies of start-fire (`0x6B980A0`-`0x6B983F7`), `InitWeapon` (`0x6B96717`-`0x6B96812`), the getter `0x5F7ED10`, the extension routine (`0x6C99700`-`0x6C9977F`), the component constructor (`0x6B8E5A0`-`0x6B8E8CD`) and the struct constructor (`0x699E6C0`-`0x699EA00`): **no stub inside any of them**, and every call in the start-fire body is a direct `rel32` call or a documented vtable call. The weapon-component range does contain 31 stubs elsewhere (for example the thunk at `0x6B99300`), so the result is "none in the functions read", not "none in the binary". Because the image is a static-analysis image and the layer's virtualized dispatch is not removed, a negative search outside these bodies stays inconclusive. This is why the "no modifier" result above is bounded to the scanned range and the call sites listed.

**Rate of fire: equip/spawn trigger, struct copies, CycleFireMode (round 20).** *Evidence: static-analysis image; virtualized dispatch not removed. Disassembly only, nothing was run. Pages that differ between the two images were read from the older reference image: the exec-thunk page `0x6B99000`, page `0x6BBB000` and page `0x675C000` (helpers `0x675CDB0`, `0x675CE10`, `0x675CEB0`). The thunk `0x6B99270` was compared byte for byte in both images. Every other function cited here sits on a page that is byte-identical in both images.*
- **(a) What triggers `0x6C99700`.** **Native:** `0x6C99700` is the body of `UWDItemExtension_RangedWeapon::OnRep_WeaponComponent`. The SDK declares `WeaponComponent` at extension `+0x128` as `Net, RepNotify, Transient`, and the class's native-function table pairs the name `OnRep_WeaponComponent` (`0xB389E80`) with the exec thunk `0x6CA1660` (slot at `0xB389E88`), whose tail `jmp` at `0x6CA1675` goes to `0x6C99700`. Two ways reach it. (1) The engine calls the OnRep on a client when the pointer replicates; the dispatch itself is engine code and was not read. (2) The extension's virtual slot 159 (`0x6C9AFB0`, vtable `0xB389548`, slot pointer `0xB389A40`) calls it directly at `0x6C9B59E`, with no role test around the call, after installing the weapon's default attributes. These are the only two references to `0x6C99700` in the image (byte scan for `call`/`jmp rel32` and for the absolute pointer). The server sets the pointer in the extension's `OnRegister` (slot 110, `0x6C99FA0`, slot pointer `0xB3898B8`): behind the owner role test `0x675CE10` (`[owner+0x170] == 3`, i.e. authority) it finds the weapon component, stores it at `+0x128` and calls `0x2480AB0(this, [this+0x38], 3)` (not decoded; read as a replication-dirty mark, **not verified**).
- **Who calls slot 159.** The item component's routine `0x6C561C0` walks the list of newly added extensions (`+0x378` bit 4 gates which) and calls vtable `+0x518` (slot 163) then vtable `+0x4F8` (slot 159) on each, at `0x6C56658` and `0x6C56664`. `0x6C561C0` is called from three virtual entries: `0x6C56730` (call at `0x6C5673B`, argument 0), `0x6C56C00` (call at `0x6C56C30`, argument 0; it also sets `+0x2CC` and flag bit 4) and `0x6C56E30` (jump at `0x6C56E51`, argument 1, only when `+0x378` bit 1 is set, a deferred retry). The bit-1 flag is cleared at `0x6C56390` and set at `0x6C5640D`. The class that owns these three entries, their slot numbers and the engine events that run them are **open**. **Derived:** InitWeapon therefore runs on whichever machine builds or receives the item's extension list, so the server and each client fill their own stats copy from the same item asset. The component's `ActiveWeaponStatsData` (`+0x130`) carries no `Net` flag in the SDK and the `+0x140` block is unreflected padding there, so the stats struct is not replicated as a property.
- **Is InitWeapon re-run on attachment or fire-mode change?** No static path found. The image has no `call rel32` to InitWeapon (`0x6B96720` is referenced only by the vtable slot `0xB3155E0`). Of the 62 `call [reg+0x558]` sites in the image, those inside the weapon, item-extension and vehicle ranges are: `0x6C9976E` (the OnRep above), `0x6B90315` (component default path), `0x7647B75` (vehicle extension), and `0x6B992E3`, which is the exec thunk `0x6B99270` of the Blueprint-callable `InitWeapon` itself (name at `0xB315820`, pointer `0xB315828`; it forwards the asset pointer from the script frame). No exported Blueprint listing in `data/` calls `InitWeapon`. The remaining sites in those ranges have other shapes and are not InitWeapon: `0x6B7A765` (takes a bool), `0x6CAB38B` and `0x6CABD17` (receiver at `+0x2F0`, result read back) and `0x763024A` (result read back from a stack buffer). The attachment paths (`OnRep_ReplicatedAttachmentMap`, thunk `0x6CA1680`; `SetPredictedAttachment`; `0x6C9D170`) are not among the `0x558` sites, so attachments do not go through InitWeapon; they act through the attribute route described in the Gameplay Effects pipeline.
- **(c) The struct copy constructor `0x6B8EFF0` is not the weapon stats struct.** It copies a different, smaller struct: the highest offset it copies is about `+0x12A`, and the array-copy loop that calls it at `0x76DB37E` strides `0x320` bytes, while the stats struct strides `0xE48` (loop at `0x6BBB7FE`). It does not touch `+0x138`, the RPM slot of the stats struct. Callers: `0x6B8C782` (function `0x6B8C720`: builds a stack copy at `rsp+0x390` from `rsp+0x50`, assigns it into the object at `[this->[0]+0xE0]` with `0x1418FCDB0`, then destroys it with `0x6B8ED40`), `0x76C1A08` (same shape: temp at `rbp+0x2B0` assigned to `[obj+0x30]`), `0x76D4CAB` and `0x76D4CDC` (function `0x76D4B40`: a copy of a looked-up element into a stack temp that is only tested with `0x1417FC060`) and `0x76DB37E` (array copy loop, stride `0x320`). None of them reads or writes the weapon component at `+0x140`, so none is a per-attachment copy of the stats struct. **Correction to the list above:** the "sibling at `0x6B8416D`" copies yet another struct (byte at `+0`, qword at `+4`, nested copy from `+0x10`, fields near `+0x90`); it does not access `+0x138` or `+0x278` in its first `0x290` bytes. The routines that copy the real 0xE48 stats struct (`0x6B8F5A0`) are: `InitWeapon` (`0x6B9676E`, destination is component `+0x140`), the exec thunk `0x6B99160` of `GetWeaponStats` (name at `0xB3157E0`; destination is the Blueprint return buffer and the source is component `+0x140`, so it only reads the copy), and the array element loop at `0x6BBB7FE` (function `0x6BBB7D0`, copies between arrays of stats structs, not into the component). `InitWeapon` remains the only writer of the component's copy that was found.
- **(3) `CycleFireMode` does not touch the RPM.** `UWDWeaponComponent::CycleFireMode(bool)` is native at `0x6B91330` (exec thunk `0x6B98EF0`, native-table slot `0xB315750`). `Server_CycleFireMode` has its thunk at `0x69E0C40`, which dispatches through vtable `+0x528` (slot 165, slot target `0x6B97810`), and that target is `CycleFireMode(this, true)`. The body reads `SupportedFireModes` through `0x1D2C340(component+0x140)`; because the accessor is `lea rax,[rcx+0x140]`, it returns the stats struct's `+0x140` TArray, so `0x1D2C340` is a struct-relative accessor and is not itself a witness for the component `+0x140` offset. It finds the current mode byte `+0xF88` in the array, takes the next entry with wraparound and stores it at `0x6B914B0` (`mov [rbx+0xF88], r8b`). That is the only store through the component pointer in the function (instruction scan of `0x6B91330-0x6B91700`). It then calls vtable `+0xF8` and `+0x60` on the owner object (`[component+0x20]`) and builds an event carrying the new mode byte. Start-fire reads `+0xF88` only to choose the timer form; the interval comes from the RPM alone, so a fire-mode change alters whether a looping timer is used (modes 1 and 2), not the RPM value. The indirect callees were not decoded, so a write to `+0x140` from them cannot be excluded (open).
- **Open after round 20.** (i) The class, slot numbers and engine events of the three entries that call `0x6C561C0`; (ii) the meaning of `0x2480AB0(this, [this+0x38], 3)` in `OnRegister`; (iii) the remaining `vtable[0x558]` sites outside the weapon, item-extension and vehicle ranges; (iv) indirect callees of `CycleFireMode`; (v) no runtime check was made. Virtualized dispatch is not removed in the analysis image, so every negative above is bounded to the functions and ranges named.

**Rate of fire: second-consumer search (round 26): no further consumer found.** *Evidence: static-analysis image only, virtualized dispatch not removed; disassembly and corpus call tables, nothing was run.* Question: does anything besides the start-fire routine `0x6B980A0` read the RPM or re-arm the shot timer, including burst, semi and stance logic?
- **Timer re-arm sites (confirmed for direct calls).** A byte scan of the whole `.text` for `call`/`jmp rel32` to `FTimerManager::SetTimer` (`0x3AB8810`) found 104 sites. Only four have a weapon-component timer handle (`+0x10F0`, `+0x10F8` or `+0x1100`) within the 0x300 bytes before the call: `0x6B9826C`, `0x6B982CA` and `0x6B9839B` (all inside start-fire, the loop timer and the one-shot remainder timer already described) and `0x6B94411` (inside `0x6B93610`, the post-shot routine called from the fire body `0x6B94700`). The fourth is **not** a cadence timer: its rate is `RecoilPatternResetTime` (stats struct `+0xCE4`, read by the one-line getter `0x6BBD5B0`, SDK `FWDWeaponStats`), its handle is `+0x1100`, and its delegate `0x6B97550` only stores -1 into component `+0xFF0` (the recoil pattern index reset). So the shot interval is armed in exactly one place.
- **Stop / re-arm.** Vtable slot 176 (`0x6B98560`, slot pointer `0xB315608`) is the stop-fire routine: it zeroes the burst counter (`+0xFEC`), clears the timer handles at `+0x10F0` and `+0x10F8`, and sends the stop event. It never writes a rate. The timer delegate `0x6B98950` only calls `0x6B94700`. (static-only: the decompiler output was read, not equivalence-proved.)
- **Burst logic (confirmed).** Burst is fire-mode byte `+0xF88` == 2. In `0x6B93610` (`0x6B93E74`-`0x6B93E9E`) each shot does `inc byte [comp+0xFEC]`; when it equals `RoundsPerBurst` (the getter `0x64D1800`: `movzx eax, byte [rcx+0x150]`, stats struct `+0x150`) the counter is reset and vtable `+0x580` (slot 176, stop-fire) is called. Burst therefore ends the loop by stopping it; the interval inside a burst is the same `59.999996 / RPM`. Semi (mode 1) and full-auto differ only in the timer form chosen in start-fire and in post-shot feedback (`0x6B96160`, which reads `+0xF88`/`+0xFEC` for sound and animation events). None of these touches `RoundsPerMinute`.
- **Second readers of the RPM field (confirmed negative in the scanned set).** (1) The only direct callers of the getter `0x5F7ED10` (`movss xmm0,[rcx+0x138]; ret`, so it is a plain struct read) remain the eight sites listed in round 18 (re-verified from the corpus call table plus a `call`/`jmp rel32` byte scan; no tail-jump callers). (2) A byte scan of the whole `.text` for scalar-float loads and compares (`movss`, `mulss`, `divss`, `cvtss2sd`, `comiss`, ...) with displacement `+0x138` (98 hits) or component-level `+0x278` (101 hits) was filtered for weapon-component fingerprints (displacements `+0xF88`, `+0xFE8`, `+0xFEC`, `+0x10F0` within 0x600 bytes): **no hit has one**, and none lies in the weapon-component range `0x6B80000-0x6BC0000` except the unrelated `0x6B82A27` (a vitality-component slot). A capstone pass over `0x6B80000-0x6BC0000` for memory operands at `+0x278`, `+0x10F0`, `+0x10F8`, `+0x1100`, `+0xFEC`, `+0xF88`, `+0xFE8` found no float access to `+0x278` (its nine `+0x278` hits are 8-byte or integer accesses in other classes' functions such as `0x6B8D830`, `0x6B8E100`, `0x6B8ED40`, `0x6B8EFF0`, `0x6B9C910`) and no store to the RPM slot outside the struct copy in `InitWeapon`.
- **The other getter callers, now classified (static-only).** `0x867A3A0` and `0x867A550` are in the automation orchestrator component (`UWDAutomationOrchestratorComponent`, caller `0x867A0B0`), a test-automation path, not live firing. `0x6AB46A0` (vtable slot 91 of `UWDAudioEventBehaviorKillingBlow`) reads the RPM at `0x6AB4BAF` and passes it to an audio-event call: an audio parameter, not a cadence. `0x6F1C310` (calls at `0x6F1C57B`, `0x6F1C616`) is the Itemsmith weapon-stats query builder: it fills an `FWDWeaponStatsQueryData` (`Damage` +0x08, `Range` +0x0C, `Accuracy` +0x10, `Recoil` +0x18, `Mobility` +0x1C, `Handling` +0x20, `MagazineSize` +0x24, `RoundsPerMinute` +0x28) from a stats struct embedded at `+0x30` of the query object (the debug strings `Weapon Recoil`, `Weapon Handling` and the others sit in the same function). The two uses are display only and are not part of the fire loop (**derived, confidence high**; the call at `0x6F1C616` stores the RPM unchanged into `RoundsPerMinute` +0x28, which feeds `FireRateText`). The call at `0x6F1C57B` feeds the **`Recoil` display stat**: `Recoil = RPM * mean_recoil * 0.5` (`mulss` at `0x6F1C5A4`, constant 0.5 at RVA `0x9AC3D40`, stored at `[rbp-0x58]` = query `+0x18`), where `mean_recoil` is the sum, over the first `MagazineSize` shots (query-object `+0xE80`, minimum 1), of the absolute values of both components of each `RecoilPattern` entry (stats struct `+0xCA0`), with every shot beyond the pattern's length counted as the width `|max - min|` of `PostPatternRandomYawRecoil` (`+0xCC0`) and of `PostPatternRandomPitchRecoil` (`+0xCD0`), divided by that shot count. **Inferred:** the number shown is a recoil-per-second index, not a per-shot angle. Which stat bar uses it was not traced (UI).
- **Attributes, effects, attachments, ADS and stance.** No code path found that carries one of these into the interval. The component-level modifier fields of the weapon component are bullet speed only (`InitialBulletSpeedModifier`, `+0x114`); the weapon attribute names and gameplay effects in `data/` contain nothing about fire rate (see above); attachments do not call `InitWeapon` (round 20). ADS and stance state were not seen in start-fire or the post-shot routine as inputs to the interval: start-fire reads only the RPM, world time, last-shot time (`+0xFE8`, written at `0x6B94597`) and the fire-mode byte. An attribute set could still reach the stats struct through a path that was not decoded, so this is **static-only, bounded to the ranges below**.
- **Ranges searched.** Whole `.text` (`0x1000`-`0x9A27000`) by byte pattern for `SetTimer` calls, getter calls and `+0x138`/`+0x278` float operands; capstone on `0x6B80000-0x6BC0000`; decompiled bodies of `0x6B93610` (post-shot, burst counter, recoil-reset timer), `0x6B94700` (fire body, read only for timer, burst and RPM use), `0x6B96160`, `0x6B98560` (stop-fire), `0x6B953E0` and `0x6B8FFE0`. A byte scan does not see indirect or virtualized dispatch (the protection layer's stubs are not removed in this image), and 27 of the +0x138/+0x278 hits are in code the corpus has no function record for, so those were ruled out only by the fingerprint window, not read. **Result: no second consumer of RPM and no second shot-interval timer found; item data through `InitWeapon` remains the only source. Runtime confirmation was not made.**

`IronSightsAimTime` is set on several launchers to 50000 (for example RPG-7 and 9K333). That is not a plausible value in seconds, so the column is left out of the table. `TypicalSpeed` is present on 24 stats assets. Its relation to `InitialBulletSpeed` is not stated in the data.

---

## 4. Default weapon attributes (`WDItemExtensionData_GameplayEffects`)

Each weapon stores a list of `Attribute.Gameplay.Weapon.*` defaults. Five multipliers are identical on all 37 weapons: `VerticalRecoilMultiplier` 1.0, `HorizontalRecoilMultiplier` 1.0, `AdsZoomMultiplier` 1.2, `SpreadMultiplier` 1.0, `AccuracyMultiplier` 1.0. `Length` is 80.0 on every weapon except `ID_Launcher_04`, which lists it twice (100, then 80); the first value, 100, is installed (see [Weapon Attributes §4](../content/Wardogs_WeaponAttributes_v1.md#4-flagged-cases)). The varying attributes are below.

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
| WEPN_037 | 0.48 | 1 | 0.95 | 100 | 200 |
| RFB | 0.52 | 0.92 | 1 | 100 | 300 |
| SKS | 0.53 | 1.15 | 1.1 | 100 | 1e+03 |
| SVDM | 0.53 | 0.97 | 1 | 100 | 1.1e+03 |
| WEPN_034 | 0.53 | 0.97 | 1 | 100 | 500 |
| LMG_02 | 0.73 | 0.95 | 1 | 100 | 1.5e+03 |
| M249 | 0.68 | 0.95 | 0.95 | 200 | 1.2e+03 |
| WEPN_036 | 0.64 | 1 | 1 | 100 | 500 |
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
| WEPN_031 | 0.285 | 0.94 | 1.15 | 50 | 200 |
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
| OutSettlePlayTime | 0.7-9 | 32 |
| OutSettleWeight | 0.1-0.7 | 33 |
| OutSettlePlayRate | 0.64 | 30 |
| TransitionVelocity | 0.14-1 | 33 |
| TransitionDamping | 0.5-0.7 | 33 |
| TransitionStrength | 0.8-1.8 | 26 |
| AttachmentOffsetAlphaLerpSpeed | 15-34 | 26 |
| AttachmentEndRange | 0.9-1 | 17 |
| CameraOffsetLerpSpeed | 30-999 | 31 |
| MinWallCollisionAlpha | 0.75-1 | 18 |
| MinBlockAdsWallCollisionAlpha | 0.01-0.3 | 17 |
| SpringLerpWeight | 0.1 | 5 |

### 5b. Spread, stance and holdable

- **Spread:** every weapon has three `SpreadValues` entries (`EBHPlayerStance::Stand`, `Crouch`, `Prone`). Each points at a row of `CT_Weapon_Spread` named `<Class>.<Stance>` (for example `AR.Stand` or `Sniper.Prone`). All stance multipliers are `1.0`, so the live spread numbers are in the curve table, not here. How the curve is evaluated (X is the planar speed over a per-stance reference speed, the result is a half-angle in degrees, smoothed at 25 per second, zero when fully aimed) is on [Weapon Spread §6](../pipelines/Wardogs_WeaponSpread_v1.md).
- **Stance recoil:** weapons with a `StanceGameplayEffects` list point at `GE_Weapon_StanceRecoil_<Class>_<Stance>` effects, with a separate set per class. Launcher_04 has no list.
- **Holdable:** `MeshFovAds` is 80.0 on 34 of the 37 weapons and 75.0 on the other 3. Hip offset (`ItemHipOffset`) varies per weapon. It is absent on `Launcher_04`, `RPG7` and `WEPN_033` through `WEPN_037`.
- **Trace radius (`WeaponTraceRadius`):** 6.0 on most rifles, 8.0 on Launcher_04, 4.0 on the Deagle, 3.0 on the Judge.

### 5c. Input bindings

Every weapon bundle carries a `B_DefaultWeaponInputData_C`. Across the bundles there are 14 distinct bindings. The first 13 appear on all 37 weapons: `Reload`, `SecondaryUse` (and `.Release`), `MeleeBash`, `Player.PrimaryUse` (and `.Release`), `CycleSights`, `CycleFireMode`, `IncreaseZeroing`, `DecreaseZeroing`, `Inspect`, `Bipod.ToggleFold`, `Bipod.Mount`. `Reload.Discard` appears on 28.

The `WDItemInputBehavior_ActivateAction` objects (435 in total) export with empty properties, so what each action does is not visible in this folder.

### 5d. Ammo model

Every weapon has one `Action.Item.PrimaryUse` requirement. It spends `ResourcesUsed = 1` of `RequiredResource` per shot, restricted to the weapon's own items (`bLimitSearchToItem = true`). The resource type is `Item.Resource.Magazine` (fed from a magazine) or `Item.Resource.Ammo` (loose). Section 2 gives both per weapon.

### 5e. Aim assist, audio and mutables

- **Aim assist:** 7 settings assets, one per class (`DA_AimAssistSettings_<Class>`), all sharing `DA_AimAssistFilter`. Weapon count per settings asset: AR 10, SR 9, Pistol 5, RPG 4, SMG 5, Shotgun 2, LMG 2.
- **Audio:** each weapon has one `WDAudioData` with between 31 and 51 sound cues (`SoundAssets`).
- **Mutable:** all 37 weapons point at `/Game/Items/Weapons/Mutable/MUT_MasterWeapon`. Each carries a `DefaultParameters` list of the slots it exposes: `Id.Item` (37), `Item.Attachment.Handguard` (35), `Sight` (34), `Barrel` (34), `Muzzle` (33), `Grip` (32), `Magazine` (32), `Mount{Left,Right,Top,Under}` (32 each), `Stock` (32), `Underbarrel` (32), `CantedSight` (31), `SightMount` (30), `DustCover` (2). The parameter values are not decoded.

---

## 6. Attachments and components

Grouped by folder. "Vendor-priced" counts items that have a `WDVendorData` row. The components have none.

| Folder | Items | Vendor-priced | Shown price | Unlock lvl | With GE effect | Attachment type tags |
|---|---|---|---|---|---|---|
| Muzzle | 49 | 46 | 350-1400 | 1 | 48 | Muzzle |
| Magazines | 34 | 33 | 10-280 | 0,1 | 33 | Magazine |
| Barrels | 25 | 0 | - | - | 0 | Barrel |
| Sights | 21 | 19 | 200-1800 | 1 | 21 | Sight |
| Stocks | 21 | 0 | - | - | 0 | Stock |
| Handguards | 20 | 0 | - | - | 0 | Handguard, Stock |
| Foregrips | 15 | 15 | 540-1480 | 1 | 15 | Bipod, Grip |
| Pistol Grips | 15 | 0 | - | - | 0 | Grip, None |
| Dust Covers | 3 | 0 | - | - | 0 | None |
| Triggers | 3 | 0 | - | - | 0 | Handguard, None |

Every vendor-priced attachment carries a `GE_*` gameplay effect in `AppliedEffects`. The numeric effects are inside those `GE_*` assets, which are not in this folder. Per-attachment stat deltas therefore cannot be given from this dump. Per-item price, unlock level, name, slot and fitting weapons are tabulated in [Weapon Shop and Parts](Wardogs_WeaponShop_v1.md).

**Magazine class tags** (on the item context, across all item definitions): Extended (12), Standard (10), Small (7), Drum (4), Belt (3), Internal (1). These are tags only. Round counts appear in item names, for example "AK74 30 RND Magazine".

**Shotgun choke override:** some muzzles set `bOverrideShotgunData`. For example, `MUZL_012` (`MZL_07`, AR Multi-Caliber Suppressor) sets `ChokeFactor 0.8`, `OuterConeHalfAngle 10`, `InnerConeHalfAngleMultiplier 0.5`, and `FireMuzzleFlashScaleMultiplier 0.2`.

**Attachment type tags are inconsistent:** two of three triggers (`TRGR_002`, `TRGR_003`) are tagged `Item.Attachment.Handguard`. Four stocks in `Handguards` are tagged `Item.Attachment.Stock`. Two pistol grips and one trigger have no attachment type. The effect of this on slot fitting is not verified.

**Multiple vendor variations:** magazine vendor rows hold 7 variations each. The first is shown (`bShowInVendor = true`) and the rest are hidden price points. For example, `MAGZ_002` shows 20 and hides 27, 27, 30, 30, 34, 34. The hidden variations are the per-ammunition-type prices, tabled in [Ranged Weapon Item Fields](../content/Wardogs_RangedWeaponFields_v1.md).

**Weight:** attachments range from 0.03 (sights) to 2.2 (magazines). Foregrips range 0.08 to 0.79.

---

## 7. Bundle wiring

- `GameFeatureData` (321): one per bundle. Each scans its own `/<Bundle>/Data` folder for `BH.Item` assets, marked `AlwaysCook`.
- `GameFeatureAction_DataRegistrySource` (160): registers `DT_VendorData_Ext_*` into the `VendorData` registry and `DT_EntityData_Ext_*` into `EntityData_UI`. Both are client and server sources.
- `GameFeatureAction_AddWorldPartitionContent` (303): adds an External Data Layer, for example `EDL_AR_01`.
- Entity-UI rows (`BHEntityData_UI`, 133 tables) hold display name (string-table key), description, category tag and icons. Vendor rows (`WDVendorData`, 150 tables) hold the variations described above.

---

## 8. Anomalies and data-quality notes

1. **WEPN_033 stats asset is a copy.** `DA_WEPN_033_Stats` has `WeaponId = Id.Item.TAR21` and values 700 RPM, 71,500 speed, 300 range, which match the A-91 family. `TAR21` already has its own stats asset (`DA_TAR21_Stats`, 750 RPM, 91,000 speed, 550 range). The `WEPN_033` item loads its own file, so its live values are the copied ones.
2. **Missing stats assets.** `Pistol_02` (Judge) references `DA_Judge_Stats` and `WEPN_007` (SKS) references `DA_SKS_Stats`. Neither exists in this folder, so their ballistics are unknown here.
3. **Zero shown prices.** `KH2002`, `A91` and `WEPN_033` are shown at price 0 with unlock level 1. The data does not say whether this means unreleased, free or unpriced.
4. **Launcher `IronSightsAimTime = 50000`.** Not a time value. Meaning unknown.
5. **Attachment type tags** are inconsistent (section 6).
6. **No vendor row for 93 of 206 parts.** That is all 87 `Components` items, plus 6 attachments (3 muzzles, 2 sights and 1 magazine). The 87 components are probably weapon-specific and unlocked by ownership, but the unlock path is not in this folder.
7. **Archetype tag differs from class.** `WEPN_037` (TCX-SPR) has damage class `AR` but archetype tag `Item.Archetype.DMR`. The table keeps both values as exported.

---

## 9. How the values combine

- **Price and unlock:** the shown vendor variation sets the price and `LevelToUnlock`. Hidden variations never appear in the shop.
- **Attachments:** a fitted attachment applies the `GE_*` effects in its `AppliedEffects`. Those effects are not in this folder, so the net stat change of a build cannot be computed here.
- **Ammo:** one unit of `RequiredResource` is spent per primary-fire shot, from the weapon's own magazine or ammo pool.
- **Spread and recoil:** base values sit in `WDWeaponStatsData` and the `CT_Weapon_Spread` curve table. Attribute multipliers (all 1.0 except `AdsZoomMultiplier` at 1.2) apply on top. The runtime combination is on [Weapon Spread](../pipelines/Wardogs_WeaponSpread_v1.md).

---

## 10. Still not pulled / limitations

- **`GE_*` gameplay effects** (attachment stat changes, stance recoil modifiers, default attribute effects) are referenced but not in this folder. Numeric attachment effects are the largest gap.
- **Curves:** ADS, recoil, view kick, sway and falloff curves are present as `EditorCurveData` keyframes inside `WDWeaponStatsData`, and as 7 `CurveFloat` objects. The keyframes are tabled, with every key, in [Weapon Spread and Recoil Data](../content/Wardogs_WeaponSpreadRecoilData_v1.md) (ADS, recoil, view kick and sway); the distance falloff curve is in [Weapons v2](../content/Wardogs_Weapons_v2.md); the 7 standalone `CurveFloat` objects are tabled in [Ranged Weapon Item Fields](../content/Wardogs_RangedWeaponFields_v1.md).
- **`WDItemInputBehavior_ActivateAction`** exports with empty payloads, so the action logic is not visible.
- **Mutable parameters** (`MUT_MasterWeapon`) are listed by key only. Option lists and default textures are not summarized.
- **Camera data** (`WDItemsmithDataFragment_CameraData`, 36) and **animation sets** (`BHAnimationSet`, 45) are counted but not decoded.
- **Missing stats:** Judge and SKS (section 8).
- **Units and meanings** of accuracy, deviation, focus energy, recoil relief, `TypicalSpeed`, `AimTime` and the zeroing values are inferred from property names.
- **Outside this folder:** the `Content/Weapons` tree and the `GameMechanics` damage and reward tables are not covered here.

## 11. Weapon plugin descriptors (round 73)

Each weapon plugin has a `GameFeatureData` descriptor. Four of them carry nothing, and two add a data layer:

| Descriptor | Contents |
|---|---|
| `AR_02` | One `AddWorldPartitionContent` action pointing at data layer `EDL_AR_02` |
| `AR_03` | The same kind of action (`EDL_AR_03`) plus a scan of `/AR_03/Data` for `BH.Item` definitions, cook rule AlwaysCook |
| `AR_04` | Empty: no actions, no scans |
| `AR_05` | Empty |
| `LMG_01` | Empty |
| `Shotgun_01` | Empty |

The empty ones are shells; the weapon data lives in the item folders of the same plugin or in `Weapons/Platforms`. The animation and audio sets of the DMR (`AnimSet_RFB`, `ID_SVDM_Audio`), LMG (`AnimSet_LMG_02`), shotgun (`AnimSet_MP43`), pistol (`ID_Judge_Audio`), SMG (`ID_SMG_03_Audio`) and sniper (`ID_MK22_Audio`, `ID_SR_04_Audio`) plugins are in [Animation](../content/Wardogs_Animation_v2.md) and [Audio](../content/Wardogs_Audio_v2.md).
