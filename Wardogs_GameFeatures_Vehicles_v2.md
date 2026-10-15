# Wardogs — GameFeatures / Vehicles Reference (v2)
*Extracted from cooked game data via CUE4Parse JSON export. Source: `Wardogs/Plugins/GameFeatures/Vehicles` — 868 files, 2,580 export objects, 0 parse errors. Values are shown exactly as stored unless noted.*

> **Scope note:** This doc covers the vehicle *plugin* data: GameFeature wrappers, vehicle market and stats tables, modular platform/variant/part assets, health pools, seats, weapons, buildables, supply crates, and physics configs. The `Content/Vehicles` folder is covered elsewhere and is not described here.
>
> **Units:** the export does not state units for most fields. Where a unit is named in the property (for example `_mps`, `_kmh`, `_deg`, `_m`), it is given. Everything else is "as stored".

---

## 1. Folder Layout and Family Map

Each top-level folder is one **family** (a vehicle, a vehicle variant group, a buildable, or a support feature). Every family has a `GameFeatureData` wrapper plus `GameFeatureAction_*` entries that register its data tables and content.

| Family folder | Role (class tag) | Files | Objects | What it is |
|---|---|---|---|---|
| `TNK_01` | Tracked | 85 | 255 | Heavy tank family: Heavy, Artillery, AntiAir variants |
| `WHL_01` | Wheeled (4W) | 51 | 117 | Bobcat light truck |
| `WHL_02` | Wheeled (4W) | 72 | 167 | Kodiak truck: Default, Pickup, base platform for ring turret |
| `WHL_02_RingTurret` | Wheeled | 15 | 40 | Kodiak "MachineGun" variant (ring turret) |
| `WHL_05` | Wheeled (4W) | 59 | 201 | Humvee (Default + shared platform) |
| `WHL_05_Minigun` | Wheeled | 17 | 40 | Humvee Minigun variant |
| `WHL_05_RingTurret` | Wheeled | 20 | 102 | Humvee MachineGun (ring turret) variant |
| `WHL_06` | Wheeled (4W) | 50 | 122 | Dune Buggy |
| `WHL_07` | Wheeled (4W) | 60 | 156 | Ural truck: Default and Battle variants |
| `WHL_07_ArmouredBattle` | Wheeled | 17 | 44 | Ural "Attack" (armoured battle) variant |
| `ROT_02` | Rotary | 48 | 213 | Havoc attack helicopter |
| `ROT_03` | Rotary | 40 | 209 | Littlebird helicopter (base) |
| `ROT_03_WeaponVariants` | Rotary | 31 | 66 | Littlebird Mounted MachineGuns and RocketPods variants |
| `ROT_04` | Rotary | 38 | 198 | ROT_04 helicopter (13 seats; unnamed in export) |
| `ROT_04_MachineGun` | Rotary | 18 | 39 | ROT_04 Mounted MachineGuns variant |
| `SPW_01` | Tracked | 36 | 117 | Spawn vehicle (Valkyra), 10 seats |
| `STN_01` | Stationary | 27 | 49 | Mistral AA (buildable emplacement) |
| `STN_02` | Stationary | 27 | 51 | Phalanx (buildable emplacement) |
| `STN_03` | Stationary | 27 | 49 | Mortar (buildable emplacement) |
| `STN_04` | Stationary | 18 | 31 | Loudspeaker (buildable) |
| `STN_05` | Stationary | 49 | 130 | Stingray (drone buildable, DroneProjectile) |
| `SupplyCrates` | n/a | 30 | 121 | Supply crates, supply pallets and the garage market for them |
| `BobbleHeads` | n/a | 20 | 36 | Bobblehead cosmetic parts (4 sub-features) |
| `Flares` | n/a | 4 | 9 | Flares countermeasure item and vendor entry |
| `Lockpicking` | n/a | 4 | 6 | Lockpicking interaction context and recon skill grant |
| `FreeVehicleSpawner` | n/a | 1 | 2 | Component add for a free vehicle spawner |
| `VehicleRewardZone` | n/a | 1 | 5 | Reward-zone widgets and components (values are not in this folder) |
| `VehicleUtility` | n/a | 1 | 2 | Component add (utility) |
| `VehicleLifetimeManager` | n/a | 1 | 1 | GameFeatureData only |
| `DebugCockpit` | n/a | 1 | 2 | Debug widget elements |

Object totals by type (top of the list): `WDGameplayCueEffect` 134, `MVF_StaticMesh` 133, `CurveFloat` 104, `DataTable` 95, `WDAttributeEffectsTrigger_VehicleHealth` 87, `ModularVehiclePart` 82, `WDWheeledVehicleEffect` 76, `ModularVehicleSlot` 61, `WDAudioData` 68, `ModularVehicleVariant` 28, `WDVehicleStatsDataAsset` 20, `WDVehicleWeaponDataAsset` 19, `WDVehicleWeaponExtensionDataAsset` 19, `WDWeaponStatsData` 14, `WDBuildableDataAsset` 5, `WDVehicleBuildSpawner` 5, `WDItemExtensionData_VehicleSupplyCrate` 9, `WDVendorData` (in DataTables) 17 tables.

GF action mix: `GameFeatureAction_DataRegistrySource` is in every content family. `GameFeatureAction_AddWorldPartitionContent` appears in the families that place world content (for example ROT_02, SPW_01, STN_01, STN_05, SupplyCrates, TNK_01, WHL_02, Flares, VehicleRewardZone). `BHGameFeatureAction_AddGameplayCuePath` appears in most vehicle families (not all).

---

## 2. Vehicle Chain: How the Assets Link

Most vehicle data follows one chain. Read it top-down to find any value.

1. **Market row** (`DT_VehicleMarket_*`) keyed by a `Vehicle.Variant.*` tag. Holds Price, LevelToUnlock, Amount and a `VehicleStatsDataAsset` reference.
2. **Variant** (`ModularVehicleVariant`, `VV_*`) with `VariantID` (same tag) and `AssemblyData.VehicleBase` pointing to a platform.
3. **Platform** (`ModularVehiclePlatform`, `VP_*`) with `ImplementationClass` (the actor class), `SpawnParams`, `Fragments` (Health, Seats, Config, Stats, Interactions, Destruction and so on) and `Slots`.
4. **Slots** (`ModularVehicleSlot`) hold parts. Parts are `ModularVehiclePart` (`VP_*`) or `MVF_StaticMesh` / `MVF_SkeletalMesh` fragments.
5. **Weapons**: slot part to `WDVehicleWeaponDataAsset` (`W_*`) to `WeaponExtensionsDataAssets` to `WDVehicleWeaponExtensionDataAsset` (ammo, reload, start inventory) to `WDWeaponStatsData` (RPM, speed, range).
6. **Config**: platform `Config` fragment to `MWheeledVehicleConfigDataAsset` / `BHRotaryVehicleConfigDataAsset` / `MTrackedVehicleConfigDataAsset` / `BHBaseVehicleConfigDataAsset`, which point to physics, camera, input, sensors and gameplay-system assets.

---

## 3. Vehicle Market (Purchase Prices)

Source: `DT_VehicleMarket_*` (one per family) and `DT_GarageMarket_SupplyCrates`. Each row is a `WDVendorData` with `VendorItemVariations`. Price is the stored purchase price; LevelToUnlock is the stored unlock level (its exact meaning is not confirmed, see section 15). All entries have Amount 1, LifeTimeBuyLimit 0 and bRequiresAccountEntitlement False.

| Variant tag | Price | LevelToUnlock | Vendor subcategory | Stats asset |
|---|---|---|---|---|
| Vehicle.Variant.Air.Rotary.Havoc.Default | 18,000 | 0 | Air.Combat | DA_ROT_02_Stats |
| Vehicle.Variant.Air.Rotary.Littlebird.Default | 6,250 | 1 | Air.Transport | DA_ROT_03_Stats |
| Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns | 7,000 | 1 | Air.Combat | DA_ROT_03_MachineGuns_Stats |
| Vehicle.Variant.Air.Rotary.Littlebird.RocketPods | 12,500 | 1 | Air.Combat | DA_ROT_03_RocketPods_Stats |
| Vehicle.Variant.Air.Rotary.ROT_04.Default | 7,400 | 0 | Air.Transport | DA_ROT_04_Stats |
| Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns | 8,000 | 0 | Air.Combat | DA_ROT_04_MachineGun_Stats |
| Vehicle.Variant.Land.Tracked.TNK_01.Heavy | 14,000 | 1 | Land.Tank | DA_TNK_01_Stats |
| Vehicle.Variant.Land.Tracked.TNK_01.AntiAir | 10,000 | 1 | Land.Tank | DA_TNK_03_Stats |
| Vehicle.Variant.Land.Tracked.TNK_01.Artillery | 8,000 | 1 | Land.Artillery | DA_TNK_02_Stats |
| Vehicle.Variant.Land.Wheeled.Bobcat.Default | 500 | 0 | Land.Transport | DA_WHL_01_Stats |
| Vehicle.Variant.Land.Wheeled.Kodiak.Default | 2,500 | 0 | Land.Transport | DA_WHL_02_Stats |
| Vehicle.Variant.Land.Wheeled.Kodiak.Pickup | 3,000 | 0 | Land.Transport | DA_WHL_02_Pickup_Stats |
| Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun | 3,750 | 0 | Land.Transport | DA_WHL_02_SUV_Stats |
| Vehicle.Variant.Land.Wheeled.Humvee.Default | 3,000 | 0 | Land.Transport | DA_WHL_05_Humvee_Stats |
| Vehicle.Variant.Land.Wheeled.Humvee.Minigun | 4,500 | 0 | Land.Transport | DA_WHL_05_Humvee_MinigunStats |
| Vehicle.Variant.Land.Wheeled.Humvee.MachineGun | 3,750 | 0 | Land.Transport | DA_WHL_05_Humvee_RingTurretStats |
| Vehicle.Variant.Land.Wheeled.DuneBuggy.Default | 1,500 | 0 | Land.Transport | DA_WHL_06_DuneBuggy_Stats |
| Vehicle.Variant.Land.Wheeled.Ural.Default | 5,000 | 0 | Land.Transport | DA_WHL_07_Stats |
| Vehicle.Variant.Land.Wheeled.Ural.Battle | 6,000 | 0 | Land.Transport | **DA_WHL_07_Stats** (see note) |
| Vehicle.Variant.Land.Wheeled.Ural.Attack | 6,750 | 0 | Land.Transport | DA_WHL_07_Battle_Stats |

> **Note:** `Ural.Battle` points at `DA_WHL_07_Stats`, while `Ural.Attack` (the ArmouredBattle asset) uses `DA_WHL_07_Battle_Stats`. Both have identical numbers in the stats table, so this has no visible effect in this export. It may be a leftover reference.

**Other market rows**

| Item | Price | LevelToUnlock | Category |
|---|---|---|---|
| Flares (`Id.Item.Flares`) | 750 | 1 | Vehicle.CounterMeasures.Flares |
| Supply crate Small (`ID.Item.VehicleSupplyCrate.Small`) | 150 | 0 | Vehicle.SupplyCrate |
| Supply crate Large | 300 | 0 | Vehicle.SupplyCrate |
| Supply crate Small Armoured | 500 | 0 | Vehicle.SupplyCrate |
| Supply crate Large Armoured | 800 | 0 | Vehicle.SupplyCrate |
| Pallet BuildSupply | 400 | 0 | Vehicle.Logistics.Pallet |
| Pallet MunitionsSupply | 400 | 0 | Vehicle.Logistics.Pallet |
| Pallet FuelSupply | 400 | 0 | Vehicle.Logistics.Pallet |
| Pallet SparePartsSupply | 400 | 0 | Vehicle.Logistics.Pallet |

Stationary buildables do not appear in these market tables. Their `Cost` is on the buildable asset (section 10).

---

## 4. Vehicle Stats (`WDVehicleStatsDataAsset`)

20 stats assets. Each lists the vehicle's spec sheet (MaxSpeed, MaxFuel, FuelEconomy, MaxSeats), a `Stats` array of vendor stat widgets (Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons), and display names for weapons and countermeasures. Stationary (STN) and drone families have no stats asset.

| Stats asset | Family | MaxSpeed | MaxFuel | FuelEconomy | MaxSeats |
|---|---|---|---|---|---|
| DA_ROT_02_Stats | ROT_02 (Havoc) | 400.0 | 130.0 | 4.4 | 2 |
| DA_ROT_03_Stats | ROT_03 (Littlebird) | 350.0 | 105.0 | 4.4 | 6 |
| DA_ROT_03_MachineGuns_Stats | ROT_03 MG variant | 350.0 | 105.0 | 4.4 | 2 |
| DA_ROT_03_RocketPods_Stats | ROT_03 Rocket variant | 350.0 | 105.0 | 4.4 | 2 |
| DA_ROT_04_Stats | ROT_04 | 445.0 | 120.0 | 4.4 | 13 |
| DA_ROT_04_MachineGun_Stats | ROT_04 MG variant | 445.0 | 120.0 | 4.4 | 13 |
| DA_SPW_Stats | SPW_01 (Valkyra) | 71.0 | 100.0 | 5.7 | 10 |
| DA_TNK_03_Stats | TNK_01 AntiAir | 65.0 | 110.0 | 10.0 | 2 |
| DA_TNK_02_Stats | TNK_01 Artillery | 65.0 | 105.0 | 8.0 | 3 |
| DA_TNK_01_Stats | TNK_01 Heavy | 65.0 | 110.0 | 8.0 | 3 |
| DA_WHL_01_Stats | WHL_01 (Bobcat) | 75.0 | 18.0 | 2.2 | 2 |
| DA_WHL_02_Stats | WHL_02 (Kodiak) | 154.0 | 50.0 | 2.9 | 4 |
| DA_WHL_02_Pickup_Stats | WHL_02 Pickup | 154.0 | 50.0 | 2.9 | 6 |
| DA_WHL_02_SUV_Stats | WHL_02 RingTurret | 154.0 | 50.0 | 2.9 | 5 |
| DA_WHL_05_Humvee_Stats | WHL_05 (Humvee) | 113.2291 | 65.0 | 3.3 | 4 |
| DA_WHL_05_Humvee_MinigunStats | WHL_05 Minigun | 113.2291 | 65.0 | 3.3 | 5 |
| DA_WHL_05_Humvee_RingTurretStats | WHL_05 RingTurret | 113.2291 | 65.0 | 3.3 | 5 |
| DA_WHL_06_DuneBuggy_Stats | WHL_06 | 130.0 | 68.0 | 5.0 | 3 |
| DA_WHL_07_Stats | WHL_07 (Ural) | 79.0 | 85.0 | 4.0 | 3 |
| DA_WHL_07_Battle_Stats | WHL_07 ArmouredBattle | 79.0 | 85.0 | 4.0 | 3 |

**Weapon names in stats** (example, DA_TNK_01_Stats): `VehicleWeaponryNames` = M249 Machine Gun, L55A1 Cannon, MG3A1 Coaxial Gun; `VehicleCounterMeasuresNames` = Smoke. These are localized through `STRINGS_VehicleVendor_Stats`.

**Things to check:**
- `MaxSeats` disagrees with the seat setups for TNK_01 Artillery and Heavy (3 stated, 2 seat setups). See section 7.
- MaxSpeed and FuelEconomy units are not given. Treat them as relative values until confirmed.

---

## 5. Health Pools (`MVF_HealthSections`)

Each platform lists its health pools as `HealthSections` (Attribute tag to MaxHealth). Sub-parts (wheels, tracks, radar) have their own pools in their part assets.

| Platform | Health (body) | Engine | FuelTank | Other pools |
|---|---|---|---|---|
| VP_ROT_02 (Havoc) | 800 | 200 | 200 | Rotor.Main 400, Rotor.Tail 300, Wheel.Left.Front 100, Wheel.Right.Front 100 |
| VP_ROT_03 (Littlebird) | 400 | 200 | 200 | Rotor.Main 400, Rotor.Tail 300 |
| VP_ROT_04 | 600 | 200 | 200 | Rotor.Main 400, Rotor.Tail 300 |
| VP_SPW (Valkyra) | 1,000 | n/a | 100 | Tracks.Left 125, Tracks.Right 125; Radar part 100 |
| VP_TNK_01_AntiAir | 800 | 150 | 150 | Tracks.Left 125, Tracks.Right 125 |
| VP_TNK_01_Artillery | 650 | 150 | 100 | Tracks.Left 125, Tracks.Right 125 |
| VP_TNK_01_Heavy | 800 | 150 | 150 | Tracks 125 each; Body.StrongArea 350 |
| VP_WHL_01 (Bobcat) | 200 | 200 | 100 | Wheels 75 each (VP_WHL_01_Wheels) |
| VP_WHL_02 (Kodiak) | 400 | 400 | 400 | Wheels 75 each |
| VP_WHL_05 (Humvee) | 500 | 400 | 400 | Wheels 75 each |
| VP_WHL_06_DuneBuggy | 400 | 400 | 300 | Wheels 75 each |
| VP_WHL_07 (Ural) | 700 | 400 | 400 | Wheels 75 each (6 wheels); Body.ModerateArea = 1 |
| VP_STN_01 (Mistral AA) | 3,000 | n/a | n/a | n/a |
| VP_STN_02 (Phalanx) | 5,000 | n/a | n/a | n/a |
| VP_STN_03 (Mortar) | 3,000 | n/a | n/a | n/a |
| VP_STN_04 (Loudspeaker) | 1,000 | n/a | n/a | n/a |
| VP_STN_05 (Stingray) | 3,000 | n/a | n/a | n/a |

Stationary body health matches the buildable `MaxHealth` (section 10).

---

## 6. Health Threshold Triggers (`WDAttributeEffectsTrigger_VehicleHealth`)

87 triggers. Each fires effects when an attribute crosses a threshold. Thresholds are percentages of max health unless marked otherwise.

| Pattern | Thresholds (percent) | Applies to |
|---|---|---|
| Body `Health` | 55, 25, 10 | ROT_02, ROT_03, ROT_04, SPW_01 (55, 10 only), TNK_01 (all three), WHL_01, WHL_02, WHL_05, WHL_06, WHL_07 |
| `Health.FuelTank` | 90 / 80, 55, 0 (or 10, 0 on ROT_03) | WHL_01, SPW_01, TNK_01, WHL_05_RingTurret, ROT_03 |
| `Health.Tracks.Left/Right` | 0 (dead), 55 (below) | SPW_01, TNK_01 (the "below 55%" trigger has 2 effects) |
| Wheel parts (`Health.Wheel.*`) | 55, 0 | WHL_01, WHL_02, WHL_05, WHL_05_RingTurret, WHL_07 (incl. Middle wheels) |
| `Health.Engine` | 20 (WHL_01), 55 (TNK_01, WHL_05_RingTurret), 0 | WHL_01, TNK_01, WHL_05_RingTurret |
| `Health.Rotor.Main` / `Tail` | 55 (above and below), 0 | ROT_02 |
| `Health.Radar` | 55, 25, 0 | SPW_01 |
| Stationary body | 1 | STN_02 |

Trigger effects are `WDVehicleEngineEffect`, `WDVehicleTurretEffect`, `WDFuelComponentEffect` and similar objects. Full effect semantics are not decoded here (see section 15).

---

## 7. Seats (`BHSeatSettingsDataAsset`)

Seat setups define a role per seat (Driver, Gunner, ActivePassenger, PassivePassenger) plus flags. Counts below are from the seat asset itself.

| Seat asset | Family | Setups | Roles | Gunner seats |
|---|---|---|---|---|
| DA_ROT_02_SeatSettings | ROT_02 | 2 | Driver, Gunner | 1 |
| DA_ROT_03_Attack_SeatSettings | ROT_03 Attack variant | 2 | Driver, ActivePassenger | 0 |
| DA_SeatSettings_SPW | SPW_01 | 10 | Driver + 9 PassivePassenger | 0 |
| DA_TNK_03_SeatSettings | TNK_01 AntiAir | 2 | Driver, Gunner | 1 |
| DA_TNK_01_Artillery_SeatSettings | TNK_01 Artillery | 2 | Driver, Gunner | 1 |
| DA_TNK_01_Heavy_SeatSettings | TNK_01 Heavy | 2 | Driver, Gunner | 1 |
| DA_SeatSettings_WHL_02 | WHL_02 Kodiak | 4 | Driver + 3 ActivePassenger | 0 |

Seat assets with 0 setups (no seats defined in this asset): WHL_01, STN_01, the MachineGun/MountedMachineGun variants (ROT_04_MachineGun, TNK_01 Artillery MG, TNK_01 Heavy MG), and several WHL variants (WHL_02_Pickup extra seats, WHL_02_RingTurret, WHL_05 variants, WHL_06, WHL_07_ArmouredBattle).

**Stats disagree with seat setups:**
- TNK_01 Artillery and Heavy: `MaxSeats` 3, but 2 seat setups.
- WHL_02 Pickup: `MaxSeats` 6, base seat asset has 4 and the extra-seats asset has 0 setups. Where the other 2 seats come from is not resolved here.
- ROT_03 and ROT_04: their base seat assets were not pulled in this pass, so no check is possible.

---

## 8. Weapons

### 8a. Weapon stats (`WDWeaponStatsData`)

| Stats asset | Family | RPM | Burst | Fire modes | Muzzle speed | Effective range | Accuracy | Caliber |
|---|---|---|---|---|---|---|---|---|
| DA_ROT_02_Weapon_122mm_Stats | ROT_02 rockets | 500 | 1 | Automatic | 45,000 | 1,000 | 6.0 | 122mm |
| DA_ROT_02_Weapon_30mmCannon_Stats | ROT_02 cannon | 250 | 1 | Automatic | 90,000 | 600 | 35.0 | 30mm |
| DA_ROT_03_AttachedMachineGuns_Stats | ROT_03 MGs | 1,500 | 1 | Automatic | 85,300 | 800 | 25.0 | 308Win |
| DA_ROT_03_Weapon_122mm_Stats | ROT_03 rocket pods | 350 | 1 | Automatic | 45,000 | 1,000 | 6.0 | 122mm |
| DA_ROT_04_MountedMachineGun_Stats | ROT_04 MG | 1,500 | 1 | Automatic | 85,300 | 1,500 | 10.0 | 308Win |
| DA_STN_01_Heavy_MountedMachineGun_Stats | STN_01 Mistral AA | 100 | 1 | SemiAutomatic | 2,000 | 1,000 | n/a | 72mm |
| DA_STN_02_Heavy_MainCannon_Stats | STN_02 Phalanx | 1,800 | 1 | Automatic | 85,000 | 1,000 | 25.0 | 20x102mm |
| DA_STN_03_Heavy_MainBarrel_Stats | STN_03 Mortar | 50 | 1 | SemiAutomatic | 80,000 | 1,000 | 50.0 | 120x800mm |
| DA_STN_05_Heavy_MainBarrel_Stats | STN_05 Stingray | 50 | 1 | SemiAutomatic | 11,000 | 10,000 | 50.0 | DroneProjectile |
| DA_TNK_03_Weapon_Stats | TNK_01 AntiAir | 1,100 | 1 | Automatic | 117,500 | 1,000 | n/a | 35x228mm |
| DA_TNK_01_Artillery_Weapon_Stats | TNK_01 Artillery | 50 | 1 | SemiAutomatic | 30,000 | 10,000 | 10.0 | 155mm |
| DA_TNK_01_Heavy_Weapon_Stats | TNK_01 Heavy | 50 | 1 | SemiAutomatic | 60,000 | 10,000 | 30.0 | 120x570mm |
| DA_TNK_01_MachineGun_Weapon_Stats | TNK_01 coax / MG | 650 | 1 | Automatic | 82,000 | 200 | 25.0 | 308Win |
| DA_WHL_05_RingMinigun_Stats | WHL_05 Minigun | 1,500 | 1 | Automatic | 85,300 | 800 | 25.0 | 308Win |

Muzzle speed is stored as a raw number with no unit in the export.

### 8b. Weapon extensions (`WDVehicleWeaponExtensionDataAsset`)

Each extension ties an item to its stats, ammo, reload timing and starting inventory. Reload fields are named `ReloadTime`, `StartDelayTime` and `LoopLoadRoundTime`. Their exact meaning is inferred from the names.

| Extension | Family | Ammo tag | Reload (s) | Start delay (s) | Loop round (s) | Start inventory | Restock needed |
|---|---|---|---|---|---|---|---|
| 122mm Rockets | ROT_02 | Id.Item.122mm | 6.0 | 1.0 | 0.75 | 0 | n/a |
| 30mm Cannon | ROT_02 | Id.Item.30mm | 8.0 | n/a | n/a | 0 | n/a |
| 308mm Machine Gun | ROT_03 MG | Id.Item.308Win | 4.25 | 1.0 | n/a | 300 (tracer) | n/a |
| MachineGun | ROT_04 MG | Id.Item.308Win | 5.0 | 1.0 | n/a | 150 (tracer) | n/a |
| Mounted Verba | STN_01 | Id.Item.72mm | 2.0 | 1.0 | n/a | 1 | 50 |
| Mounted Verba | STN_02 | Id.Item.20x102mm | 3.0 | 1.0 | n/a | 500 | 250 |
| Mortar | STN_03 | Id.Item.120x800mm | 4.5 | 1.0 | n/a | 3 | 75 |
| Stingray | STN_05 | Id.Item.DroneProjectile | 0.0 | 1.0 | n/a | 0 | 900 |
| 35mm Cannons | TNK_01 AntiAir | ID.Item.35x228mm | 4.0 | n/a | n/a | 0 | n/a |
| Artillery | TNK_01 Artillery | ID.Item.155mm | 25.0 | 1.0 | n/a | 10 (Expensive), 0 (Standard) | n/a |
| Heavy Turret | TNK_01 Heavy | ID.Item.120x570mm | 4.0 | 1.0 | n/a | 9 | n/a |
| Mounted M249 | TNK_01 | Id.Item.556mm | 4.25 | 1.0 | n/a | 0 (tracer) | n/a |
| Machine Gun | TNK_01 coax / MG | Id.Item.308Win | 4.25 | 1.0 | n/a | 300 (tracer) | n/a |
| Minigun | WHL_05 Minigun | Id.Item.308Win | 4.25 | 1.0 | n/a | 150 (tracer) | n/a |

Four extensions carry a restock count (the Restock column). The restock semantics and tag are not decoded.

### 8c. Weapon data (`WDVehicleWeaponDataAsset`)

19 assets, one per weapon mount (for example `W_TNK_01_Heavy`, `W_ROT_02_122mm`, `W_WHL_05_Humvee_RingMinigun`). Each gives the weapon tag (`Id.Vehicle.Weapon.*`), a skeletal mesh, muzzle sockets, the player attach socket and the aim sensitivities (for example Gamepad 35, Mouse 8, Key 45 for `W_TNK_01_Heavy`).

---

## 9. Projectile and Damage Model

### 9a. Drone projectile (`WDProjectileData`, Stingray)

| Field | Value |
|---|---|
| ProjectileId | Item.Caliber.DroneProjectile |
| Damage tag | Meta.Damage.Explosive.Drone |
| BaseDamage | 120 |
| ExplosiveRadius | 1,000 |
| EffectiveExplosiveRadius | 500 |
| MinimumExplosiveDamage | 15 |
| ExplosiveDamageFallOff | 0.45 |
| ExplosiveBluntDamage | 100 |
| Impulse scale | 2,500 (Z 3,500) |
| BaseSuppression | 0.8 |
| MaxProjectileLifetime | 500 |
| ArmingDelay | 0.1 |

### 9b. Global damage tables (`DT_GlobalDamage_VehicleData_*`)

A `WDDamageableEntityTableRow` lists damage modification entries per source, target and hit location.

| Table | Family | Rows | Entries | Operations used |
|---|---|---|---|---|
| DT_GlobalDamage_VehicleData_ROT_02 | ROT_02 | 1 | 34 | Percentage_Ongoing 30, None 4 |
| DT_GlobalDamage_VehicleData_SPW_01 | SPW_01 | 1 | 31 | Percentage_Ongoing 26, None 5 |
| DT_GlobalDamage_VehicleData_STN_01 | STN_01 | 1 | 24 | Percentage_Ongoing 19, None 4, Add 1 |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01 | 3 | 84 | Percentage_Ongoing 69, None 15 |
| DT_GlobalDamage_VehicleData_WHL_01 | WHL_01 | 1 | 19 | Percentage_Ongoing 18, None 1 |
| DT_GlobalDamage_VehicleData_WHL_05 (and Minigun, RingTurret) | WHL_05 family | 1 each | 30 each | Percentage_Ongoing 27, None 3 |
| DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy | WHL_06 | 1 | 29 | Percentage_Ongoing 26, None 3 |
| DT_GlobalDamage_VehicleData_WHL_07_Ural | WHL_07 | 1 | 29 | Percentage_Ongoing 26, None 3 |
| DT_GlobalDamage_SupplyCrate | SupplyCrates | 5 | 7 | Percentage_Ongoing 7 |

Each entry's `Amount` and per-entry requirements are not summarized here (section 15).

---

## 10. Stationary Buildables

Five buildable emplacements, each a `WDBuildableDataAsset` with a `WDVehicleBuildSpawner` that spawns the stationary vehicle.

| Buildable | Family | EntityTag | Cost | MaxHealth | MaxStack | Damage tag | Spawner variant |
|---|---|---|---|---|---|---|---|
| DA_Buildable_MistralAA | STN_01 | Id.Buildable.MistralAA | 1,000 | 3,000 | 6 | none | Vehicle.Variant.Stationary.MistralAA |
| DA_Buildable_STN_02 | STN_02 | Id.Buildable.Phalanx | 1,500 | 5,000 | 6 | none | Vehicle.Variant.Stationary.Phalanx |
| DA_Buildable_STN_03 | STN_03 | Id.Buildable.Mortar | 150 | 3,000 | 6 | Meta.Damage.Vehicle.Stationary.Mortar | Vehicle.Variant.Stationary.Mortar |
| DA_Buildable_STN_04 | STN_04 | Id.Buildable.Loudspeaker | 100 | 1,000 | not set | none | Vehicle.Variant.Stationary.Loudspeaker |
| DA_Buildable_STN_05 | STN_05 | Id.Buildable.STN_05 | 150 | 3,000 | 6 | Meta.Damage.Vehicle.Stationary.STN_05 | Vehicle.Variant.Stationary.STN_05 |

`Cost` is the stored build cost. Buildable prices are not on a vendor table in this folder.

---

## 11. Supply Crates and Pallets (`WDItemExtensionData_VehicleSupplyCrate`)

| Item | Slots | StartingHealth | MaxHealth | Notes |
|---|---|---|---|---|
| ID_FreeSupplyCrate | 6 | 150 | 250 | Free crate (no market row) |
| ID_SmallSupplyCrate | 6 | 150 | 300 | Market: Small, 150 |
| ID_SmallSupplyCrate_Armoured | 6 | 300 | not set | Market: Small Armoured, 500 |
| ID_LargeSupplyCrate | 16 | 250 | not set | Market: Large, 300 |
| ID_LargeSupplyCrate_Armoured | 16 | 400 | 500 | Market: Large Armoured, 800 |
| Pallet BuildSupplies | 12 | 800 | 800 | `bLockCrateOnPurchase` True; market 400 |
| Pallet FuelSupplies | 12 | 800 | 800 | Market 400 |
| Pallet MunitionsSupplies | 12 | 800 | 800 | Market 400 |
| Pallet SparePartsSupplies | 12 | 800 | 800 | Market 400 |

Crate and pallet bases are `BlueprintGeneratedClass` objects. Crates use the `WDItemExtension_VehicleSupplyCrate` component. Faction materials are keyed by `Meta.Alignment.Faction.*`. Lock-on-purchase was checked only on the BuildSupplies pallet (True).

---

## 12. Physics and Movement Configs

### 12a. Wheeled characteristics (`MWheeledVehicleCharacteristicsDataAsset`)

| Family | Mass | CoM Z offset | DrivetrainFriction | HandBrakePower | ABS | ASR | ReverseBrakeSpeed | DownForce |
|---|---|---|---|---|---|---|---|---|
| WHL_01 Bobcat | 250 | -0.45 | 25.0 | 8.0 | n/a | n/a | n/a | 0.1 |
| WHL_02 Kodiak | 2,750 | -0.3 | 100 | 50 | 30 (min speed 35) | 55 | 6.0 | 5.0 |
| WHL_05 Humvee | 7,250 | -0.4 | 100 | 80 | 50 | 45 | 15.0 | 5.0 |
| WHL_06 Dune Buggy | 550 | -0.65 (X 0.35) | 10.0 | 50 | 25 | 18 | n/a | 0.5 |
| WHL_07 Ural | 10,000 | -0.3 (X -1.4) | 100 | 50 | 15 (min 35) | 45 | 30.0 | 5.0 |

`n/a` means the field was not extracted, not that it is absent. Mass is as stored (Chaos units, probably kg). Several other wheeled fields are present but not tabled here (understeer and oversteer assists, friction, antiroll).

### 12b. Engine and transmission (`MWheeledVehicleEngineTransmissionDataAsset`)

| Family | Idle RPM | Limit RPM | Torque scale | Friction torque | Gear ratios | Final gear |
|---|---|---|---|---|---|---|
| WHL_01 | 1,200 | 7,000 | n/a | 15 | 4.2, 2.8, 1.9, 1.5, 1.3, 6.0 | 9.5 |
| WHL_02 | n/a | n/a | 0.6 | 75 | 6.0, 3.1, 2.45, 1.7, 1.3, 6.0 | 5.5 |
| WHL_05 | 700 | 4,000 | n/a | 75 | 3.6, 2.4, 1.7, 1.35, 1.12, 3.6 | 6.54 |
| WHL_06 | 800 | n/a | 0.35 | 75 | 4.8, 3.6, 2.7, 2.15, 1.98, 6.0 | 4.3 |
| WHL_07 | 650 | 2,600 (limiter 50) | 2.0 | n/a | 5.62, 2.89, 1.64, 1.25, 1.1, 3.25 | 7.32 |

Each has a torque curve (`CRV_Torque*`), a boost scale of 1.03 to 1.2, and a `ChangeTime` / `ClutchTime`.

### 12c. Rotary flight (`BHRotaryFlightDataAsset`)

| Family | MaxLiftCoeff | Rotor radius | Stall AoA (deg) | Translational lift % | Translational lift window (m/s) | Ground effect | Cyclic attenuation | Max angular velocity (deg/s) |
|---|---|---|---|---|---|---|---|---|
| ROT_02 Havoc | 1.8 | 600 | 40.0 | 20 | 24 to 34 | falloff 12 m | 0.45 | 83 |
| ROT_03 Littlebird | 1.25 | n/a | n/a | 16 | 20 to 28 | falloff 12 m | 0.6 | 83 |
| ROT_04 | 5.75 | 800 | n/a | 25 | 24 to 34 | strength 30%, falloff 12 m | 0.45 | 83 |

Rotor tuning on the engines: ROT_03 `EngineRPMDecreaseRatePerSecond` 850. ROT_04 `MainRotorCriticalLowRPM` 180 and `MainRotorOperatingRPM` 270. ROT_02 has an empty engine asset.

### 12d. Air drag (`BHAirVehicleDragDataAsset`)

| Asset | Family | Front area | Side area | Drag coefficient | Air density (sea level) |
|---|---|---|---|---|---|
| DA_ROT_02_Drag | ROT_02 | 4,000 | 7,000 | 0.0056 | 0.00125 |
| DA_ROT_03_DragDataAsset2000KGLight | ROT_03 | 1,000 | 5,000 | 0.0056 | 0.00125 |
| DA_ROT_03_RocketPods_DragDataAsset2000KGLight | ROT_03 RocketPods | 1,000 | 5,000 | 0.0056 | 0.00125 |
| DA_ROT_04_DragDataAsset | ROT_04 | 4,000 | 9,000 | 0.0056 | 0.00125 |

### 12e. Tracked configs (SPW_01, TNK_01)

Tracked vehicles use `MTrackedVehicleConfigDataAsset` with engine, suspension, wheel, dynamics and track data. The config carries `VehicleFlipCheckThreshold` (TNK_01 Artillery 150) and `EntryOffsetTolerance` (TNK_01 Artillery 1,000; SPW_01 400). Track wheel bone lists and tread meshes are set per family.

### 12f. Stationary configs

Stationary platforms use `BHBaseVehicleConfigDataAsset` (no physics). They carry gameplay system and camera assets, and `bAllowCameraViewToggle` is false on all four.

---

## 13. Other Features

| Feature | Contents | Notes |
|---|---|---|
| BobbleHeads (4 sub-features) | 8 `ModularVehiclePart` (bobblehead parts, `Vehicle.Bobblehead` tag), 8 `MVF_SkeletalMesh`, `WDCosmeticData` rows | Faction variants chosen by faction selectors: Lonestar, Valkyra, Manticore (Alpha, Bravo, Charlie); other sub-features: Warpup, HeavyHelmet, Grenade |
| Flares | `BHInventoryItemDefinition` (`Id.Item.Flares`), `BHEntityData_UI`, `WDVendorData` (750) | Anti-air countermeasure; "Deploys 3x bursts of flares" |
| Lockpicking | `WDUIInteractionContextDataTableRow` (action "LOCKPICK", context "Vehicle"), `WDMetaSkillEffectsTaggedTableRow` (grants `GE_GrantSkill_Lockpicking`), `WDGameFeatureActions_AddWorldInteractableContextToActor` | Role: Recon |
| VehicleRewardZone | `WDGameFeatureAction_AddWidgetElements` (plus `_Instance`), `GameFeatureAction_AddComponents`, world partition | Reward values are not in this folder |
| FreeVehicleSpawner | `GameFeatureAction_AddComponents` | Component add only |
| VehicleUtility | `GameFeatureAction_AddComponents` | Component add only |
| VehicleLifetimeManager | GameFeatureData only | No content |
| DebugCockpit | `WDGameFeatureAction_AddWidgetElements` | Debug widget |
| Vehicle interaction contexts | 12 `WDVehicleInteractionContextsData` assets and 24 `WDVehicleInteractionsDataAsset` | Ordering for Enter.Driver and other seats; interaction tracker points; per-context overrides |

---

## 14. How Values Combine

- **Buying a vehicle:** the market row (section 3) gives the Price and the LevelToUnlock gate. The row's stats asset (section 4) is the spec sheet shown to the player.
- **Health:** a vehicle's total effective durability is the body pool plus its sub-part pools (section 5). Threshold triggers (section 6) fire at percentages of each pool's max. Damage routing for hits is in the global damage tables (section 9b).
- **Seats:** the platform's Seats fragment points at the seat asset. `MaxSeats` in the stats is the displayed capacity, which can differ from the seat setup count (section 7).
- **Weapons:** a mount's weapon data (8c) gives its extensions. Each extension gives reload timing, starting ammo and restock (8b). The stats asset (8a) gives fire rate and range.
- **Buildables:** the buildable's MaxHealth matches its platform's body pool (sections 5 and 10). Cost is the build price.
- **Crates:** the item extension (section 11) sets slots and HP. The garage market price is separate (section 3).

---

## 15. Still not pulled / Limitations

- **Obfuscated property names.** Some fields have names like `_aaabgbmbdpbnepcapcckp_$1C13F1D4...$_$22$`. Their meanings are unknown and were skipped (for example, several flags on health triggers and vendor variations).
- **Units.** Speed, fuel, FuelEconomy, muzzle speed, drag area and mass are not labelled in the export. Treat them as relative values until a reference confirms them. Only fields with a unit suffix (`_mps`, `_kmh`, `_deg`, `_m`) have a known unit.
- **Semantics inferred from names.** `LevelToUnlock` (vendor), `StartDelayTime` / `LoopLoadRoundTime` (reload), `RestockSuppliesNeeded`, and the above/below effect split on health triggers are read from names only.
- **Health trigger effects.** Effect objects (`WDVehicleEngineEffect`, `WDFuelComponentEffect`, `WDVehicleTurretEffect`, `WDWheeledVehicleEffect` and so on, roughly 180 objects across the folder) are counted but their parameters are not decoded.
- **Damage entries.** Damage tables are counted by operation. Each entry's `Amount`, requirements and priority are not summarized.
- **Seat counts.** ROT_03 and ROT_04 base seat assets were not pulled. Pickup's extra 2 seats (6 stated vs 4 base) are unresolved.
- **Wheel and surface curves.** The 104 `CurveFloat` objects, the per-surface audio and skid assets (`DA_Vehicle_Surface_*`, `DA_Vehicle_Skidding_*`, `DA_Vehicle_BrakingSurface_*`), and the wheel-level `MWheeledVehicleWheelDataAsset` values (friction, suspension, brake torque, Values[0..2] meaning unconfirmed) are not tabled.
- **Control assist conditions.** The rotary control assist bodies and conditions (`BH*RotaryMovementControlAssist*` and related conditions, roughly 270 objects) are not decoded.
- **Audio and cues.** `WDGameplayCueEffect` (134), `WDAudioData` (68) and the Crosstalk audio event objects (about 130) are inventoried only.
- **Input and camera.** `MWheeledVehicleInputDataAsset`, `MLandInputControlsDataAsset`, and the spring arm and camera behaviour assets are not tabled.
- **Stationary stats.** STN_01 to STN_05 have no stats asset, so their MaxSpeed, fuel and seat values are not available.
- **Vendor stat widgets.** `W_VehicleVendor_Stat_*` widget objects (Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons) are referenced by each stats asset but their display logic is not decoded.
- **Ural asset mapping.** `Ural.Battle` points at `DA_WHL_07_Stats` rather than the ArmouredBattle asset (section 3). Numbers are identical, so this is only a reference oddity.
- **Localization.** Names come from string-table keys (`STRINGS_VehicleVendor_Stats`, `STRINGS_BuildTool`, `STRINGS_Bobblehead_Faction`). Only the source strings are shown, not localized text in other languages.
