---
title: "All-Vehicle Stat & Damage Sheets"
parent: "Content"
---

# Wardogs — Every Vehicle's Stat/Damage Sheet Reference (excl. TNK_01)
*Extracted from cooked game data.*

> **Scope:** TNK_01 Artillery was already fully documented separately; this covers the rest of the roster: ROT_02 (Havoc), ROT_03 (Littlebird), ROT_04, SPW_01, STN_01-05, WHL_01, WHL_02, WHL_05 (Humvee + variants), WHL_06 (DuneBuggy), WHL_07 (Ural/SpawnVehicle).

**15 `WDVehicleStatsDataAsset` assets, 17 `DT_GlobalDamage_VehicleData*` tables pulled.**

## Season 02 update (2026-10-15)

- No vehicle stat assets (section 1) or weapon-stat rows (section 2) changed. No files were added or removed.
- Damage entries went from 451 to 472 across the 17 tables. A new `Meta.Damage.Explosive.Rocket.125mm` entry was added to each of these 12 tables: Havoc (150.0), Little Bird (100.0), ROT_04 (150.0), Leopard (-10.0), Bobcat (250.0), Kodiak (250.0), Humvee Default, Minigun and MachineGun (250.0 each), Dune Buggy (250.0), Ural (75.0) and STN_05 (-50.0). Mistral, Phalanx, Mortar and Radio Tower each gained two entries.
- Humvee Default entry 13 `Amount`: -67.0 → -85.0.
- Humvee Minigun entry 13 `Amount`: -71.0 → -88.0. Entry 27: -90.0 → -88.0.
- Humvee MachineGun entry 13 `Amount`: -69.0 → -86.5. Entry 27: -87.5 → -86.5.
- Ural Defender entry 13 `Amount`: -65.0 → -87.5.
- Little Bird AH-6M entry 15 `Amount`: -40.0 → -69.5.
- ROT_04 entry 12 `Amount`: -40.0 → -57.25.
- Havoc entry 12 `Amount`: 87.5 → -46.0.
- Leopard entry 25 `Amount`: -60.0 → -84.0.
- Phalanx entry 12 `Amount`: 80.0 → -65.0.
- Mistral, Phalanx, Mortar, Radio Tower and STN_05 entries were re-sequenced. Several changed their source tag, operation or priority category. The changes are in the tables below.
- Patch notes describe calibre reductions that apply to vehicle miniguns such as the Little Bird AH-6M Minigun and the Humvee Minigun.

---

## 1. Vehicle Stat Assets (`WDVehicleStatsDataAsset`)

| Asset | Package | MaxSpeed | MaxFuel | FuelEconomy | MaxSeats | Weaponry | Countermeasures |
|---|---|---|---|---|---|---|---|
| [`DA_ROT_02_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Data/DA_ROT_02_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Data/DA_ROT_02_Stats.uasset` | 400.0 | 130.0 | 4.4 | 2 | 2A42 Autocannon, B-13 Rocket Pods | Flares |
| [`DA_ROT_03_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Data/DA_ROT_03_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Data/DA_ROT_03_Stats.uasset` | 350.0 | 105.0 | 4.4 | 6 | — | Flares |
| [`DA_ROT_03_MachineGuns_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_MachineGuns_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_MachineGuns_Stats.uasset` | 350.0 | 105.0 | 4.4 | 2 | Two M134D Miniguns | Flares |
| [`DA_ROT_03_RocketPods_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_RocketPods_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_RocketPods_Stats.uasset` | 350.0 | 105.0 | 4.4 | 2 | B-13 Rocket Pods | Flares |
| [`DA_ROT_04_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Data/DA_ROT_04_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Data/DA_ROT_04_Stats.uasset` | 445.0 | 120.0 | 4.4 | 13 | — | Flares |
| [`DA_ROT_04_MachineGun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/Data/MachineGun/DA_ROT_04_MachineGun_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/Data/MachineGun/DA_ROT_04_MachineGun_Stats.uasset` | 445.0 | 120.0 | 4.4 | 13 | Two M134D Miniguns | Flares |
| [`DA_SPW_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/Data/DA_SPW_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/Data/DA_SPW_Stats.uasset` | 71.0 | 100.0 | 5.7 | 10 | — | — |
| [`DA_WHL_01_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/Data/DA_WHL_01_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/Data/DA_WHL_01_Stats.uasset` | 75.0 | 18.0 | 2.2 | 2 | — | — |
| [`DA_WHL_02_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/Data/DA_WHL_02_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/Data/DA_WHL_02_Stats.uasset` | 154.0 | 50.0 | 2.9 | 4 | — | — |
| [`DA_WHL_02_Pickup_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/Data/WHL_02_Pickup/DA_WHL_02_Pickup_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/Data/WHL_02_Pickup/DA_WHL_02_Pickup_Stats.uasset` | 154.0 | 50.0 | 2.9 | 6 | — | — |
| [`DA_WHL_02_SUV_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02_RingTurret/Content/Data/WHL_02_SUV_RingTurret/DA_WHL_02_SUV_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_02_RingTurret/Content/Data/WHL_02_SUV_RingTurret/DA_WHL_02_SUV_Stats.uasset` | 154.0 | 50.0 | 2.9 | 5 | M249 Machine Gun | — |
| [`DA_WHL_05_Humvee_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/Data/DA_WHL_05_Humvee_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/Data/DA_WHL_05_Humvee_Stats.uasset` | 113.2291 | 65.0 | 3.3 | 4 | — | — |
| [`DA_WHL_06_DuneBuggy_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/Data/DA_WHL_06_DuneBuggy_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/Data/DA_WHL_06_DuneBuggy_Stats.uasset` | 130.0 | 68.0 | 5.0 | 3 | — | — |
| [`DA_WHL_07_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Data/DA_WHL_07_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Data/DA_WHL_07_Stats.uasset` | 79.0 | 85.0 | 4.0 | 3 | — | — |
| [`DA_WHL_07_Battle_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07_ArmouredBattle/Content/Data/ArmouredBattleUral/DA_WHL_07_Battle_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_07_ArmouredBattle/Content/Data/ArmouredBattleUral/DA_WHL_07_Battle_Stats.uasset` | 79.0 | 85.0 | 4.0 | 3 | — | — |

Notes:
- A dash (`—`) in the Weaponry or Countermeasures column is how the export shows an empty cell. The file does not say whether that means none or unset.
- The three ROT_03 rows share MaxSpeed, MaxFuel and FuelEconomy. They differ in MaxSeats (6 for the base asset, 2 for the variants) and in Weaponry.
- [`DA_WHL_05_Humvee_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/Data/DA_WHL_05_Humvee_Stats.json) MaxSpeed is exported as 113.2291, the only value in the column with more than one decimal place.

---

## 2. Vehicle-Mounted Weapon Stats Found Alongside (`WDWeaponStatsData`)

| Asset | Package | WeaponId | RPM | Fire modes |
|---|---|---|---|---|
| [`DA_ROT_02_Weapon_122mm_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Weapons/122mm/DA_ROT_02_Weapon_122mm_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Weapons/122mm/DA_ROT_02_Weapon_122mm_Stats.uasset` | ID.Item.VehicleHelicopterRockets | 500.0 | Automatic |
| [`DA_ROT_02_Weapon_30mmCannon_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Weapons/Cannon/DA_ROT_02_Weapon_30mmCannon_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Weapons/Cannon/DA_ROT_02_Weapon_30mmCannon_Stats.uasset` | ID.Item.VehicleHelicopterCannon | 250.0 | Automatic |
| [`DA_ROT_03_AttachedMachineGuns_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Weapons/DA_ROT_03_AttachedMachineGuns_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Weapons/DA_ROT_03_AttachedMachineGuns_Stats.uasset` | Id.Item.ROT_03.MountedMachineGun | 1500.0 | Automatic |
| [`DA_ROT_03_Weapon_122mm_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Weapons/DA_ROT_03_Weapon_122mm_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Weapons/DA_ROT_03_Weapon_122mm_Stats.uasset` | ID.Item.VehicleHelicopterRockets_ROT_03 | 350.0 | Automatic |
| [`DA_ROT_04_MountedMachineGun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/Weapons/DA_ROT_04_MountedMachineGun_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/Weapons/DA_ROT_04_MountedMachineGun_Stats.uasset` | Id.Item.ROT_04.MountedMachineGun | 1500.0 | Automatic |
| [`DA_STN_01_Heavy_MountedMachineGun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/Weapon/DA_STN_01_Heavy_MountedMachineGun_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/Weapon/DA_STN_01_Heavy_MountedMachineGun_Stats.uasset` | Id.Item.MistralAA | 100.0 | SemiAutomatic |
| [`DA_STN_02_Heavy_MainCannon_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/Weapons/DA_STN_02_Heavy_MainCannon_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/Weapons/DA_STN_02_Heavy_MainCannon_Stats.uasset` | Id.Item.STN_02.MainCannon | 1800.0 | Automatic |
| [`DA_STN_03_Heavy_MainBarrel_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/Weapons/DA_STN_03_Heavy_MainBarrel_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/Weapons/DA_STN_03_Heavy_MainBarrel_Stats.uasset` | Id.Item.STN_03.MainBarrel | 50.0 | SemiAutomatic |
| [`DA_STN_05_Heavy_MainBarrel_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Weapons/DA_STN_05_Heavy_MainBarrel_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Weapons/DA_STN_05_Heavy_MainBarrel_Stats.uasset` | Id.Item.STN_03.MainBarrel | 50.0 | SemiAutomatic |
| [`DA_WHL_05_RingMinigun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/Weapons/WeaponExtensions/DA_WHL_05_RingMinigun_Stats.json) | `Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/Weapons/WeaponExtensions/DA_WHL_05_RingMinigun_Stats.uasset` | Id.Item.HumveeVehicleRingMinigun | 1500.0 | Automatic |

Notes:
- [`DA_STN_03_Heavy_MainBarrel_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/Weapons/DA_STN_03_Heavy_MainBarrel_Stats.json) and [`DA_STN_05_Heavy_MainBarrel_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Weapons/DA_STN_05_Heavy_MainBarrel_Stats.json) both use WeaponId `Id.Item.STN_03.MainBarrel` (50.0 RPM, SemiAutomatic).
- [`DA_STN_01_Heavy_MountedMachineGun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/Weapon/DA_STN_01_Heavy_MountedMachineGun_Stats.json) uses WeaponId `Id.Item.MistralAA`, not an STN_01 prefix.
- WeaponId prefixes are shown as exported: `ID.Item.` on the ROT_02 and ROT_03 rocket and cannon rows, `Id.Item.` elsewhere.

---

## 3. Global Vehicle Damage Tables (`DT_GlobalDamage_VehicleData*`)

Each table holds one row, named by its gameplay tag, with a list of damage entries. The tables below list the entries in file order, numbered from 0 as the Season notes above cite them.

- **Category** is the entry's `PriorityCategory` (`Meta.Damage.Category.*`).
- **Source** lists the damage tags in `SourceRequirements`, without the `Meta.Damage.` prefix. Several tags are joined with +.
- **Hit location** lists `PossibleHitLocations`, without the `Meta.Damage.HitLocation.` prefix. Several locations are joined with /.
- **Change** is the `Amount`. For `Percentage_Ongoing` entries it reads as a percentage change, as on the [GameMechanics page](Wardogs_GameMechanics_v2.html#2f-infantry-damage-modification-rules-dt_globaldamage_infantrydata-row-metadamageinfantry); `Add` entries are marked flat. Section 6 covers what the file leaves open.
- The fields that are empty or default on every entry (instigator and target requirements, alignment, custom operation, priority index) are left out. Section 5 lists them.

### 3a. [`DT_GlobalDamage_VehicleData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json)
- **Package:** `Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.uasset`
- **Row:** `Meta.Damage.Vehicle`, 10 entries. The 6 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 4 | AmmoModifier | Bullet | — | none |
| 5 | AmmoModifier | AmmoModifier.HollowPoint | — | −40% |
| 6 | AmmoModifier | AmmoModifier.HollowPoint | — | +40% |
| 7 | Ricochet | Kinetic.Impact.Ricochet | — | 0% |


### 3b. [`DT_GlobalDamage_VehicleData_ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_02.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_02.uasset`
- **Row:** `Meta.Damage.Vehicle.Air.Rotary.Havoc`, 35 entries. The 4 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 1 | Armor | Bullet | — | −95% |
| 2 | Armor | Cannon | — | −70% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | 0% |
| 4 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +400% |
| 5 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | −20% |
| 6 | Armor | Bullet.308Win | — | −70% |
| 7 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 8 | Armor | Explosive.Utility.C4 | — | −15% |
| 9 | Armor | Explosive.Utility.IED | — | +45% |
| 10 | Armor | Explosive.Utility.Claymore | — | −75% |
| 11 | Calibre | Cannon.30mm | — | −35% |
| 12 | Calibre | Cannon.35x228mm | — | −46% |
| 13 | Calibre | Explosive.Rocket.72mm | — | −60% |
| 14 | Calibre | Explosive.Rocket.93mm | — | −30% |
| 15 | Calibre | Explosive.Rocket.93mm | Vehicle.MainRotor / Vehicle.TailRotor / Vehicle.Tail | −45% |
| 16 | Calibre | Explosive.Rocket.120x800mm | — | −10% |
| 17 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 18 | Calibre | Explosive.Rocket.84mm | Vehicle.MainRotor / Vehicle.TailRotor / Vehicle.Tail | −5% |
| 19 | Calibre | Explosive.Rocket.120mm | — | +150% |
| 20 | Calibre | Cannon.20x102mm | — | −75.5% |
| 21 | Calibre | Explosive.Rocket.122mm | — | −85% |
| 22 | Calibre | Explosive.Grenade.40mm | — | −30% |
| 23 | Calibre | Explosive.Rocket.155mm | — | 0% |
| 26 | Calibre | Explosive.Rocket | Vehicle.TailRotor | +50% |
| 27 | Calibre | Explosive.Rocket | Vehicle.MainRotor | 0% |
| 28 | Calibre | Explosive.Rocket | Vehicle.Tail | 0% |
| 29 | Calibre | Explosive.Rocket | Vehicle.Engine | 0% |
| 31 | Bone | Bullet | Vehicle.FuelTank | +300% |
| 32 | Bone | Bullet | Attribute.Gameplay.Health / Attribute.Gameplay.Health.Skids / Attribute.Gameplay.Health.Tail / Vehicle.MainBody / Vehicle.MainRotor / Vehicle.Skids / Vehicle.Tail / Vehicle.TailRotor | −50% |
| 33 | Calibre | Explosive.Drone | — | +450% |
| 34 | Calibre | Explosive.Rocket.125mm | — | +150% |


### 3c. [`DT_GlobalDamage_VehicleData_ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_03.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_03.uasset`
- **Row:** `Meta.Damage.Vehicle.Air.Rotary.LittleBird`, 33 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 1 | Armor | Bullet | — | −92.5% |
| 2 | Armor | Cannon | — | −30% |
| 3 | Armor | Cannon.20x102mm | — | −85% |
| 4 | Armor | Bullet | Attribute.Gameplay.Health / Attribute.Gameplay.Health.Tail / Attribute.Gameplay.Health.Skids | −80% |
| 5 | Bone | Bullet | Attribute.Gameplay.Health.FuelTank | +200% |
| 6 | Ricochet | Kinetic.Impact.Ricochet | — | −95% |
| 7 | Armor | Bullet.308Win | — | −55% |
| 8 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +400% |
| 9 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | +50% |
| 10 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 11 | Armor | Explosive.Utility.C4 | — | 0% |
| 12 | Armor | Explosive.Utility.IED | — | +25% |
| 13 | Armor | Explosive.Utility.Claymore | — | −50% |
| 14 | Calibre | Cannon.30mm | — | −15% |
| 15 | Calibre | Cannon.35x228mm | — | −69.5% |
| 16 | Calibre | Explosive.Grenade.40mm | — | −40% |
| 17 | Calibre | Explosive.Rocket.72mm | — | 0% |
| 18 | Calibre | Explosive.Rocket.120x800mm | — | +25% |
| 19 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 20 | Calibre | Explosive.Rocket.93mm | — | −7.5% |
| 21 | Calibre | Explosive.Rocket.120mm | — | +100% |
| 22 | Calibre | Explosive.Rocket.122mm | — | −80% |
| 23 | Calibre | Cannon.20x102mm | — | −10% |
| 24 | Calibre | Explosive.Rocket.155mm | — | 0% |
| 27 | Calibre | Explosive.Rocket | Vehicle.Tail / Vehicle.TailRotor | +200% |
| 28 | Calibre | Explosive.Rocket | Attribute.Gameplay.Health.Rotor.Main / Vehicle.MainRotor | 0% |
| 29 | Calibre | Explosive.Rocket | Vehicle.Tail / Vehicle.TailRotor | 0% |
| 30 | Calibre | Explosive.Rocket | Vehicle.Engine | 0% |
| 31 | Calibre | Explosive.Drone | — | +500% |
| 32 | Calibre | Explosive.Rocket.125mm | — | +100% |


### 3d. [`DT_GlobalDamage_VehicleData_ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_04.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_04.uasset`
- **Row:** `Meta.Damage.Vehicle.Air.Rotary.ROT_04`, 33 entries. The 4 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 1 | Armor | Bullet | — | −95% |
| 2 | Armor | Cannon | — | −70% |
| 3 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 4 | Calibre | Explosive.Radius.Inner + Explosive.Grenade | — | 0% |
| 5 | Armor | Bullet.308Win | — | −60% |
| 6 | Ricochet | Kinetic.Impact.Ricochet | — | 0% |
| 7 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 8 | Armor | Explosive.Utility.C4 | — | −35% |
| 9 | Armor | Explosive.Utility.IED | — | +30% |
| 10 | Armor | Explosive.Utility.Claymore | — | −75% |
| 11 | Calibre | Cannon.30mm | — | −15% |
| 12 | Calibre | Cannon.35x228mm | — | −57.25% |
| 13 | Calibre | Explosive.Rocket.72mm | — | −32.5% |
| 14 | Calibre | Explosive.Rocket.120x800mm | — | −55% |
| 15 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 16 | Calibre | Explosive.Rocket.93mm | — | −10% |
| 17 | Calibre | Explosive.Rocket.120mm | — | +150% |
| 18 | Calibre | Explosive.Grenade.40mm | — | −20% |
| 19 | Calibre | Explosive.Rocket.122mm | — | −80% |
| 20 | Calibre | Explosive.Rocket.155mm | — | 0% |
| 21 | Calibre | Cannon.20x102mm | — | −80% |
| 24 | Calibre | Explosive.Rocket | Vehicle.TailRotor | +50% |
| 25 | Calibre | Explosive.Rocket | Vehicle.MainRotor | 0% |
| 26 | Calibre | Explosive.Rocket | Vehicle.Tail | 0% |
| 27 | Calibre | Explosive.Rocket | Vehicle.Engine | 0% |
| 29 | Bone | Bullet | Vehicle.FuelTank | +350% |
| 30 | Bone | Bullet | Vehicle.MainBody / Vehicle.Skids | −50% |
| 31 | Calibre | Explosive.Drone | — | +450% |
| 32 | Calibre | Explosive.Rocket.125mm | — | +150% |


### 3e. [`DT_GlobalDamage_VehicleData_SPW_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/DataTables/DT_GlobalDamage_VehicleData_SPW_01.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/DataTables/DT_GlobalDamage_VehicleData_SPW_01.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Tracked.Leopard.Spawn`, 32 entries. The 5 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 1 | Armor | Bullet | Vehicle.MainBody / Vehicle.Tracks.Left / Vehicle.Tracks.Right / Vehicle.FuelTank | −100% |
| 2 | Armor | Bullet | Vehicle.Radar | −95% |
| 3 | Armor | Cannon | — | −70% |
| 4 | Ricochet | Kinetic.Impact.Ricochet | — | −95% |
| 5 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +100% |
| 6 | Calibre | Explosive.Rocket.155mm | — | 0% |
| 7 | Calibre | Explosive.Radius.Inner + Explosive.Grenade | — | −80% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +100% |
| 9 | Armor | Explosive.Utility.C4 | — | +15% |
| 10 | Armor | Explosive.Utility.IED | — | +150% |
| 11 | Armor | Explosive.Utility.Claymore | — | −95% |
| 14 | Calibre | Explosive.Rocket | Vehicle | 0% |
| 16 | Bone | Bullet | Attribute.Gameplay.Health.FuelTank | +200% |
| 17 | Bone | Bullet | Vehicle.FuelTank.Destroyed | −90% |
| 19 | Calibre | Explosive.Rocket.72mm | — | −30% |
| 20 | Calibre | Cannon.35x228mm | — | −84% |
| 21 | Calibre | Explosive.Grenade.40mm | — | +20% |
| 22 | Calibre | Explosive.Rocket.120x800mm | — | +20% |
| 23 | Calibre | Explosive.Rocket.84mm | — | +90% |
| 24 | Calibre | Cannon.30mm | — | −30% |
| 25 | Calibre | Cannon.20x102mm | — | −84% |
| 26 | Calibre | Explosive.Rocket.93mm | — | 0% |
| 27 | Calibre | Explosive.Rocket.120mm | — | −10% |
| 28 | Calibre | Explosive.Rocket.122mm | — | −55% |
| 29 | Calibre | Explosive.Rocket.155mm | — | +10% |
| 30 | Calibre | Explosive.Drone | — | +500% |
| 31 | Calibre | Explosive.Rocket.125mm | — | −10% |


### 3f. [`DT_GlobalDamage_VehicleData_STN_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/DataTables/DT_GlobalDamage_VehicleData_STN_01.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/DataTables/DT_GlobalDamage_VehicleData_STN_01.uasset`
- **Row:** `Meta.Damage.Vehicle.Stationary.Mistral`, 26 entries. The 4 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | — | DamageType.Melee | — | −80% |
| 1 | Melee | Kinetic.Impact.Throwable | — | −100% |
| 2 | Melee | Kinetic.Impact.ExplosiveBlunt | — | −50% |
| 4 | CaliberEffectiveness | Explosive.Rocket | — | +650% |
| 5 | Calibre | Cannon.35x228mm | — | −70% |
| 6 | Calibre | Cannon.20x102mm | — | −70% |
| 7 | CaliberEffectiveness | Cannon.30mm | — | −50% |
| 8 | CaliberEffectiveness | Explosive.Rocket.120mm | — | +50% |
| 9 | AmmoModifier | Explosive.Rocket.155mm | — | −9% |
| 10 | CaliberEffectiveness | Explosive.Rocket.84mm | — | 0% |
| 11 | CaliberEffectiveness | Explosive.Rocket.93mm | — | 0% |
| 12 | Calibre | Explosive.Rocket.122mm | — | −70% |
| 13 | Calibre | Explosive.Rocket.120x800mm | — | +80% |
| 15 | CaliberEffectiveness | Explosive.Utility | — | 0% |
| 16 | CaliberEffectiveness | Explosive.Utility.C4 | — | +1500% |
| 17 | CaliberEffectiveness | Explosive.Utility.IED | — | +150% |
| 18 | CaliberEffectiveness | Explosive.Grenade | — | 0% |
| 20 | Calibre | Bullet | — | −85% |
| 21 | AmmoModifier | AmmoModifier.ArmorPiercing + Bullet | — | +100% |
| 22 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −50% |
| 24 | Bone | Vehicle.Land.Tracked | — | +1000 flat |
| 25 | CaliberEffectiveness | Explosive.Rocket.125mm | — | +50% |


### 3g. [`DT_GlobalDamage_VehicleData_STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/DataTables/DT_GlobalDamage_VehicleData_STN_02.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/DataTables/DT_GlobalDamage_VehicleData_STN_02.uasset`
- **Row:** `Meta.Damage.Vehicle.Stationary.Phalanx`, 26 entries. The 4 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | — | DamageType.Melee | — | −80% |
| 1 | Melee | Kinetic.Impact.Throwable | — | −100% |
| 2 | Melee | Kinetic.Impact.ExplosiveBlunt | — | −50% |
| 4 | CaliberEffectiveness | Explosive.Rocket | — | +650% |
| 5 | Calibre | Cannon.35x228mm | — | −70% |
| 6 | Calibre | Cannon.20x102mm | — | −70% |
| 7 | CaliberEffectiveness | Cannon.30mm | — | −50% |
| 8 | CaliberEffectiveness | Explosive.Rocket.120mm | — | −20% |
| 9 | AmmoModifier | Explosive.Rocket.155mm | — | −9% |
| 10 | CaliberEffectiveness | Explosive.Rocket.84mm | — | 0% |
| 11 | CaliberEffectiveness | Explosive.Rocket.93mm | — | 0% |
| 12 | Calibre | Explosive.Rocket.122mm | — | −65% |
| 13 | Calibre | Explosive.Rocket.120x800mm | — | +80% |
| 15 | CaliberEffectiveness | Explosive.Utility | — | 0% |
| 16 | CaliberEffectiveness | Explosive.Utility.C4 | — | +700% |
| 17 | CaliberEffectiveness | Explosive.Utility.IED | — | +2000% |
| 18 | CaliberEffectiveness | Explosive.Grenade | — | 0% |
| 20 | Calibre | Bullet | — | −85% |
| 21 | AmmoModifier | AmmoModifier.ArmorPiercing + Bullet | — | +100% |
| 22 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −50% |
| 24 | Bone | Vehicle.Land.Tracked | — | +1000 flat |
| 25 | CaliberEffectiveness | Explosive.Rocket.125mm | — | −20% |


### 3h. [`DT_GlobalDamage_VehicleData_STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/DataTable/DT_GlobalDamage_VehicleData_STN_03.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/DataTable/DT_GlobalDamage_VehicleData_STN_03.uasset`
- **Row:** `Meta.Damage.Vehicle.Stationary.Mortar`, 24 entries. The 4 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | — | DamageType.Melee | — | −80% |
| 1 | Melee | Kinetic.Impact.Throwable | — | −100% |
| 2 | Melee | Kinetic.Impact.ExplosiveBlunt | — | −50% |
| 4 | CaliberEffectiveness | Explosive.Rocket | — | +650% |
| 5 | Calibre | Cannon.35x228mm | — | −70% |
| 6 | Calibre | Cannon.20x102mm | — | −70% |
| 7 | CaliberEffectiveness | Cannon.30mm | — | −50% |
| 8 | CaliberEffectiveness | Explosive.Rocket.120mm | — | −50% |
| 9 | AmmoModifier | Explosive.Rocket.155mm | — | −80% |
| 10 | Calibre | Explosive.Rocket.120x800mm | — | +80% |
| 11 | Calibre | Explosive.Rocket.122mm | — | −65% |
| 13 | CaliberEffectiveness | Explosive.Utility | — | 0% |
| 14 | CaliberEffectiveness | Explosive.Utility.C4 | — | +300% |
| 15 | CaliberEffectiveness | Explosive.Utility.IED | — | +400% |
| 16 | CaliberEffectiveness | Explosive.Grenade | — | 0% |
| 18 | Calibre | Bullet | — | −85% |
| 19 | AmmoModifier | AmmoModifier.ArmorPiercing + Bullet | — | +100% |
| 20 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −50% |
| 22 | Bone | Vehicle.Land.Tracked | — | +1000 flat |
| 23 | CaliberEffectiveness | Explosive.Rocket.125mm | — | −50% |


### 3i. [`DT_GlobalDamage_VehicleData_STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/DataTables/DT_GlobalDamage_VehicleData_STN_04.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/DataTables/DT_GlobalDamage_VehicleData_STN_04.uasset`
- **Row:** `Meta.Damage.Vehicle.Stationary.RadioTower`, 27 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −95% |
| 1 | Armor | Bullet + AmmoModifier.ArmorPiercing | — | +17.5% |
| 2 | Armor | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −85% |
| 4 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 5 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | +100% |
| 6 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 7 | Armor | Explosive.Utility.C4 | — | 0% |
| 8 | Armor | Explosive.Utility.IED | — | +150% |
| 9 | Armor | Explosive.Utility.Claymore | — | −50% |
| 10 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 13 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Right.Front | +27.5% |
| 14 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Rear | +45% |
| 16 | Bone | Bullet | Attribute.Gameplay.Health.FuelTank | +200% |
| 17 | Bone | Bullet | Vehicle.Wheel | −50% |
| 18 | Bone | Bullet | Attribute.Gameplay.Health | −50% |
| 19 | Calibre | Cannon.35x228mm | — | −70% |
| 20 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 21 | Calibre | Explosive.Rocket.93mm | — | −30% |
| 22 | Calibre | Explosive.Rocket.120x800mm | — | −30% |
| 23 | Calibre | Cannon.30mm | — | −15% |
| 24 | Calibre | Cannon.20x102mm | — | −70% |
| 25 | Calibre | Explosive.Rocket.122mm | — | −40% |
| 26 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3j. [`DT_GlobalDamage_VehicleData_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/DataTable/DT_GlobalDamage_VehicleData_STN_05.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/DataTable/DT_GlobalDamage_VehicleData_STN_05.uasset`
- **Row:** `Meta.Damage.Vehicle.Stationary.STN_05`, 24 entries. The 4 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | — | DamageType.Melee | — | −80% |
| 1 | Melee | Kinetic.Impact.Throwable | — | −100% |
| 2 | Melee | Kinetic.Impact.ExplosiveBlunt | — | −50% |
| 4 | CaliberEffectiveness | Explosive.Rocket | — | +650% |
| 5 | Calibre | Cannon.35x228mm | — | −70% |
| 6 | Calibre | Cannon.20x102mm | — | −70% |
| 7 | CaliberEffectiveness | Cannon.30mm | — | −50% |
| 8 | CaliberEffectiveness | Explosive.Rocket.120mm | — | −50% |
| 9 | AmmoModifier | Explosive.Rocket.155mm | — | −80% |
| 10 | Calibre | Explosive.Rocket.120x800mm | — | +80% |
| 11 | Calibre | Explosive.Rocket.122mm | — | −65% |
| 13 | CaliberEffectiveness | Explosive.Utility | — | 0% |
| 14 | CaliberEffectiveness | Explosive.Utility.C4 | — | +300% |
| 15 | CaliberEffectiveness | Explosive.Utility.IED | — | +400% |
| 16 | CaliberEffectiveness | Explosive.Grenade | — | 0% |
| 18 | Calibre | Bullet | — | −85% |
| 19 | AmmoModifier | AmmoModifier.ArmorPiercing + Bullet | — | +100% |
| 20 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −50% |
| 22 | Bone | Vehicle.Land.Tracked | — | +1000 flat |
| 23 | CaliberEffectiveness | Explosive.Rocket.125mm | — | −50% |


### 3k. [`DT_GlobalDamage_VehicleData_WHL_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_01.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_01.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.Bobcat`, 20 entries. The 1 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −92.5% |
| 1 | AmmoModifier | Bullet + AmmoModifier.ArmorPiercing | — | +20% |
| 2 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Armor | Bullet.308Win | — | −65% |
| 4 | Ricochet | Kinetic.Impact.Ricochet | — | −95% |
| 5 | AmmoModifier | Explosive.Grenade.40mm + Explosive.Rocket | — | +250% |
| 6 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | 0% |
| 7 | Armor | Explosive.Utility.IED | — | +150% |
| 8 | AmmoModifier | Explosive | — | +100% |
| 9 | Armor | Explosive.Utility.Claymore | — | −50% |
| 10 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 11 | Calibre | Cannon.30mm | — | 0% |
| 12 | Calibre | Cannon.35x228mm | — | −40% |
| 13 | Calibre | Cannon.20x102mm | — | −75% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 16 | Bone | Bullet | Vehicle.FuelTank | 0% |
| 17 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | +500% |
| 18 | Calibre | Explosive.Drone | — | +500% |
| 19 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3l. [`DT_GlobalDamage_VehicleData_WHL_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_02.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_02.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.Patriot.Kodiak`, 29 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −95% |
| 1 | AmmoModifier | Bullet + AmmoModifier.ArmorPiercing | — | +20% |
| 2 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −85% |
| 4 | Armor | Bullet.308Win | — | −50% |
| 6 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +400% |
| 7 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | −17.5% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 9 | Armor | Explosive.Utility.C4 | — | 0% |
| 10 | Armor | Explosive.Utility.IED | — | +150% |
| 11 | Armor | Explosive.Utility.Claymore | — | −50% |
| 12 | Calibre | Cannon.30mm | — | −50% |
| 13 | Calibre | Cannon.35x228mm | — | −70% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 15 | Calibre | Explosive.Rocket.155mm | — | +250% |
| 17 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | 0% |
| 19 | Bone | Bullet | Vehicle.FuelTank | +200% |
| 20 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | +700% |
| 21 | Bone | Bullet | Vehicle.MainBody | −50% |
| 22 | Calibre | Explosive.Grenade.40mm | Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear / Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear | +300% |
| 23 | Calibre | Explosive.Rocket.93mm | — | 0% |
| 24 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 25 | Calibre | Explosive.Rocket.120x800mm | — | +30% |
| 26 | Calibre | Cannon.20x102mm | — | −82.5% |
| 27 | Calibre | Explosive.Drone | — | +500% |
| 28 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3m. [`DT_GlobalDamage_VehicleData_WHL_05_Humvee`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_Humvee.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_Humvee.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.Humvee.Default`, 31 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −95% |
| 1 | Armor | Bullet + AmmoModifier.ArmorPiercing | — | +17.5% |
| 2 | Armor | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −85% |
| 4 | Armor | Bullet.308Win | — | −50% |
| 6 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 7 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | −35% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 9 | Armor | Explosive.Utility.C4 | — | −20% |
| 10 | Armor | Explosive.Utility.IED | — | +150% |
| 11 | Armor | Explosive.Utility.Claymore | — | −75% |
| 12 | Calibre | Cannon.30mm | — | −70% |
| 13 | Calibre | Cannon.35x228mm | — | −85% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 15 | Calibre | Explosive.Rocket.155mm | — | +250% |
| 17 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Right.Front | +27.5% |
| 18 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Rear | +45% |
| 20 | Bone | Bullet | Vehicle.FuelTank | +400% |
| 21 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | +500% |
| 22 | Bone | Bullet | Vehicle.MainBody | −50% |
| 23 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 24 | Calibre | Explosive.Rocket.93mm | — | −70% |
| 25 | Calibre | Explosive.Grenade.40mm | Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear / Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear | +75% |
| 26 | Calibre | Explosive.Rocket.120x800mm | — | −35% |
| 27 | Calibre | Cannon.20x102mm | — | −85% |
| 28 | Calibre | Explosive.Rocket.122mm | — | −55% |
| 29 | Calibre | Explosive.Drone | — | +350% |
| 30 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3n. [`DT_GlobalDamage_VehicleData_WHL_05_Minigun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_Minigun.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_Minigun.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.Humvee.Minigun`, 31 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −97.5% |
| 1 | Armor | Bullet + AmmoModifier.ArmorPiercing | — | +17.5% |
| 2 | Armor | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −85% |
| 4 | Armor | Bullet.308Win | — | −50% |
| 6 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 7 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | −45% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 9 | Armor | Explosive.Utility.C4 | — | −52.5% |
| 10 | Armor | Explosive.Utility.IED | — | +150% |
| 11 | Armor | Explosive.Utility.Claymore | — | −75% |
| 12 | Calibre | Cannon.30mm | — | −75% |
| 13 | Calibre | Cannon.35x228mm | — | −88% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 15 | Calibre | Explosive.Rocket.155mm | — | +250% |
| 17 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Right.Front | +27.5% |
| 18 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Rear | +45% |
| 20 | Bone | Bullet | Vehicle.FuelTank | +400% |
| 21 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | +800% |
| 22 | Bone | Bullet | Vehicle.MainBody | −50% |
| 23 | Calibre | Explosive.Rocket.84mm | — | +15% |
| 24 | Calibre | Explosive.Rocket.93mm | — | −77.5% |
| 25 | Calibre | Explosive.Grenade.40mm | Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear / Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear | +75% |
| 26 | Calibre | Explosive.Rocket.120x800mm | — | −35% |
| 27 | Calibre | Cannon.20x102mm | — | −88% |
| 28 | Calibre | Explosive.Rocket.122mm | — | −65% |
| 29 | Calibre | Explosive.Drone | — | +350% |
| 30 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3o. [`DT_GlobalDamage_VehicleData_WHL_05_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_RingTurret/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_RingTurret.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_RingTurret/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_RingTurret.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.Humvee.MachineGun`, 31 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −96% |
| 1 | Armor | Bullet + AmmoModifier.ArmorPiercing | — | +17.5% |
| 2 | Armor | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −85% |
| 4 | Armor | Bullet.308Win | — | −50% |
| 6 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 7 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | −40% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 9 | Armor | Explosive.Utility.C4 | — | −35% |
| 10 | Armor | Explosive.Utility.IED | — | +150% |
| 11 | Armor | Explosive.Utility.Claymore | — | −75% |
| 12 | Calibre | Cannon.30mm | — | −77.5% |
| 13 | Calibre | Cannon.35x228mm | — | −86.5% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 15 | Calibre | Explosive.Rocket.155mm | — | +250% |
| 17 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Right.Front | +27.5% |
| 18 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Rear | +45% |
| 20 | Bone | Bullet | Vehicle.FuelTank | +400% |
| 21 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | +650% |
| 22 | Bone | Bullet | Vehicle.MainBody | −50% |
| 23 | Calibre | Explosive.Rocket.84mm | — | +20% |
| 24 | Calibre | Explosive.Rocket.93mm | — | −75% |
| 25 | Calibre | Explosive.Grenade.40mm | Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear / Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear | +75% |
| 26 | Calibre | Explosive.Rocket.120x800mm | — | −35% |
| 27 | Calibre | Cannon.20x102mm | — | −86.5% |
| 28 | Calibre | Explosive.Rocket.122mm | — | −60% |
| 29 | Calibre | Explosive.Drone | — | +350% |
| 30 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3p. [`DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.DuneBuggy`, 30 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −90% |
| 1 | AmmoModifier | Bullet + AmmoModifier.ArmorPiercing | — | +20% |
| 2 | AmmoModifier | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −95% |
| 4 | Armor | Bullet.308Win | — | −45% |
| 6 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 7 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | +5% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +200% |
| 9 | Armor | Explosive.Utility.C4 | — | 0% |
| 10 | Armor | Explosive.Utility.IED | — | +150% |
| 11 | Armor | Explosive.Utility.Claymore | — | −50% |
| 12 | Calibre | Cannon.30mm | — | −60% |
| 13 | Calibre | Cannon.35x228mm | — | −65% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +250% |
| 15 | Calibre | Explosive.Rocket.155mm | — | +250% |
| 17 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Right.Front | +27.5% |
| 18 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Rear | +45% |
| 20 | Bone | Bullet | Vehicle.FuelTank | +200% |
| 21 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear | +275% |
| 22 | Bone | Bullet | Vehicle.MainBody | −50% |
| 23 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 24 | Calibre | Explosive.Rocket.93mm | — | −45% |
| 25 | Calibre | Explosive.Grenade.40mm | Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Rear / Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Rear | +300% |
| 26 | Calibre | Explosive.Rocket.120x800mm | — | +30% |
| 27 | Calibre | Cannon.20x102mm | — | −75% |
| 28 | Calibre | Explosive.Drone | — | +500% |
| 29 | Calibre | Explosive.Rocket.125mm | — | +250% |


### 3q. [`DT_GlobalDamage_VehicleData_WHL_07_Ural`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_07_Ural.json)
- **Package:** `Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_07_Ural.uasset`
- **Row:** `Meta.Damage.Vehicle.Land.Wheeled.Ural`, 30 entries. The 3 empty ones, with no source and no change, are not listed.

| # | Category | Source | Hit location | Change |
|---|---|---|---|---|
| 0 | Armor | Bullet | — | −95% |
| 1 | Armor | Bullet + AmmoModifier.ArmorPiercing | — | +17.5% |
| 2 | Armor | Bullet + AmmoModifier.HollowPoint | — | −20% |
| 3 | Ricochet | Kinetic.Impact.Ricochet | — | −85% |
| 4 | Armor | Bullet.308Win | — | −65% |
| 6 | Calibre | Explosive.Rocket + Explosive.Radius.Inner | — | +200% |
| 7 | Calibre | Explosive.Grenade + Explosive.Radius.Inner | — | −15% |
| 8 | Calibre | Explosive.Utility.ATMine | — | +250% |
| 9 | Armor | Explosive.Utility.C4 | — | −55% |
| 10 | Armor | Explosive.Utility.IED | — | +50% |
| 11 | Armor | Explosive.Utility.Claymore | — | −65% |
| 12 | Calibre | Cannon.30mm | — | −40% |
| 13 | Calibre | Cannon.35x228mm | — | −87.5% |
| 14 | Calibre | Explosive.Rocket.120mm | — | +75% |
| 16 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Right.Front | +27.5% |
| 17 | Calibre | Explosive.Rocket | Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Rear | +45% |
| 19 | Bone | Bullet | Vehicle.FuelTank | +350% |
| 20 | Bone | Bullet | Vehicle.Wheel.Left.Front / Vehicle.Wheel.Left.Middle / Vehicle.Wheel.Left.Rear / Vehicle.Wheel.Right.Front / Vehicle.Wheel.Right.Middle / Vehicle.Wheel.Right.Rear | +350% |
| 21 | Bone | Bullet | Vehicle.MainBody | −50% |
| 22 | Calibre | Explosive.Rocket.84mm | — | +30% |
| 23 | Calibre | Explosive.Rocket.93mm | — | −30% |
| 24 | Calibre | Explosive.Rocket.120x800mm | — | −30% |
| 25 | Calibre | Explosive.Grenade.40mm + Explosive.Radius.Inner | — | −30% |
| 26 | Calibre | Cannon.20x102mm | — | −87.5% |
| 27 | Calibre | Explosive.Rocket.122mm | — | −55% |
| 28 | Calibre | Explosive.Drone | — | +500% |
| 29 | Calibre | Explosive.Rocket.125mm | — | +75% |

---

## 4. Full property export (`WDVehicleStatsDataAsset`)

What each of the 15 vehicle stat assets holds beyond the six values in section 1: the vendor stat rows it shows, in its own order, and the string-table keys behind its Weaponry and Countermeasures names (`STRINGS_VehicleVendor_Stats`, without the `VehicleStats.Equipment.` prefix). The stat rows are `W_VehicleVendor_Stat_*` widgets with no values of their own. Asset names link to the full export.

| Asset | Vendor stat rows, in order | Weaponry keys | Countermeasure keys |
|---|---|---|---|
| [`DA_ROT_02_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Data/DA_ROT_02_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | `30mmCannon`, `122mmRockets` | `Flares` |
| [`DA_ROT_03_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Data/DA_ROT_03_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | `Flares` |
| [`DA_ROT_03_MachineGuns_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_MachineGuns_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | `DuelMiniguns` | `Flares` |
| [`DA_ROT_03_RocketPods_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/Data/WeaponVariants/DA_ROT_03_RocketPods_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | `122mmRockets` | `Flares` |
| [`DA_ROT_04_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/Data/DA_ROT_04_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | `Flares` |
| [`DA_ROT_04_MachineGun_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/Data/MachineGun/DA_ROT_04_MachineGun_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | `DuelMiniguns` | `Flares` |
| [`DA_SPW_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/Data/DA_SPW_Stats.json) | — | — | — |
| [`DA_WHL_01_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/Data/DA_WHL_01_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |
| [`DA_WHL_02_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/Data/DA_WHL_02_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |
| [`DA_WHL_02_Pickup_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/Data/WHL_02_Pickup/DA_WHL_02_Pickup_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |
| [`DA_WHL_02_SUV_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02_RingTurret/Content/Data/WHL_02_SUV_RingTurret/DA_WHL_02_SUV_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | `MountedM249` | — |
| [`DA_WHL_05_Humvee_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/Data/DA_WHL_05_Humvee_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |
| [`DA_WHL_06_DuneBuggy_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/Data/DA_WHL_06_DuneBuggy_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |
| [`DA_WHL_07_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/Data/DA_WHL_07_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |
| [`DA_WHL_07_Battle_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07_ArmouredBattle/Content/Data/ArmouredBattleUral/DA_WHL_07_Battle_Stats.json) | Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons | — | — |

---

## 5. How the values combine

- **Structure:** section 1 is the per-asset export of six columns. Section 2 lists weapon-stat rows keyed by `WeaponId`. Section 3 lists each table's one row, named by its `Tag`, entry by entry from its `DamageModificationEntries` list. Section 4 lists what the stat assets hold beyond section 1.
- **Entry fields:** each damage entry has `InstigatorRequirements`, `TargetRequirements` and `SourceRequirements` lists, an `AlignmentRequired` value, `PossibleHitLocations`, and an `OutModification` block with `Operation`, `Amount`, `PriorityCategory` and `PriorityIndex`.
- **Operations:** `Percentage_Ongoing` on 407 entries, `None` on 61 and `Add` on 4 (472 entries in total).
- **Requirements:** the Instigator and Target lists are empty on every entry. Source lists hold one or more gameplay tags, such as `Meta.Damage.Bullet` with `Meta.Damage.AmmoModifier.ArmorPiercing`, or `Meta.Damage.Explosive.Rocket` with `Meta.Damage.Explosive.Radius.Inner`. Some Source lists are empty.
- **Hit locations:** `PossibleHitLocations` is populated on 66 entries, using `Meta.Damage.HitLocation.Vehicle.*` tags (wheels, fuel tank, main body).
- **Priority:** `PriorityIndex` is -1 on all 472 entries. `PriorityCategory` carries a tag on 408 entries (Calibre 220, Armor 74, Bone 34, CaliberEffectiveness 36, AmmoModifier 23, Ricochet 13, Melee 8) and `None` on 64.
- **Alignment and custom operations:** `AlignmentRequired` is `EWDDamageAlignment::None` and `bUseCustomOperation` is False on every entry. `CustomOperationClass` is None on every entry.

---

## 6. Still not pulled / limitations

- **Operation meaning:** the file does not define `Percentage_Ongoing`, `Add` or `None`. The unit, sign and stacking of `Amount` cannot be read from here. Amounts across all entries are exported as signed numbers from -100.0 to 2000.0.
- **Priority order:** with every `PriorityIndex` at -1, the order applied when several entries match is not shown.
- **Tag definitions:** the tag names and their hierarchy are in the config files; see [Wardogs_GameplayTags_v1.md](Wardogs_GameplayTags_v1.md). How a requirement tag matches its child tags is engine logic and is not in those files.
- **Weaponry link:** `VehicleWeaponryNames` gives each vehicle's weapons as display-name string keys (`STRINGS_VehicleVendor_Stats`), not as the `WeaponId` tags used in section 2. The export does not map one to the other.
- **Hit locations:** the `PossibleHitLocations` tags are listed per entry. How they map to the vehicle model is not in the export.
- **Dashes:** the meaning of `—` cells is unconfirmed.
- **Scope:** TNK_01 is excluded here and documented separately.
