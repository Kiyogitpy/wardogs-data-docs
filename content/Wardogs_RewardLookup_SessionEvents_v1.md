---
title: "Session-Event Reward Lookups"
parent: "Content"
redirect_from: ["/Wardogs_RewardLookup_SessionEvents_v1.html", "/Wardogs_RewardLookup_SessionEvents_v1"]
---

# Wardogs — Session-Event Reward Lookups Reference
*Exported from the game's own asset files. These are the lookup layer feeding the per-kill/per-event reward calculator whose formulas are in section 17 (`DT_ChallengeRewards_SessionEvents_*`).*

> **Scope:** **16 tables pulled**, covering KOTH challenge events ([`Challenges_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/Challenges_KOTH.json)), buildable destruction ([`Rewards/BuildableRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards)) and Spotting ([`Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Spotting.json)). Each table maps a row key (a vehicle variant, item or buildable ID) to a `Challenges.Rewards.*` reward tag. Reward amounts and the calculator that consumes these tags are outside this file.

> **Challenges and state trees:** which event each challenge waits for, what its state tree does and which of these lookup and formula rows it feeds are on [Challenges and Session Events](../game-features/Wardogs_Challenges_v1.md). That page also answers the "Event triggers" gap in section 19 from the tree data (event tags and payloads), though the in-game code that raises them is not traced.

## Season 02 update (2026-10-15)

- **Vehicle lookups (tables 2 to 6):** table 2 grows from 30 to 34 rows, and tables 3 to 6 from 24 to 28 rows. New keys: `Vehicle.Variant.Land.Wheeled.WHL_08.Default`, `WHL_08.MachineGun`, `Vehicle.Variant.Land.Tracked.TNK_04.Default` and `Vehicle.Variant.Stationary.MGNest`. Tables 3 to 6 also add `Vehicle.Variant.Land.Wheeled.Humvee.Minigun`.
- **Vehicle tags are per variant (table 2):** 23 of the 30 keys that were already in the table have a new tag, e.g. `VehicleDestroyed.Kodiak` → `VehicleDestroyed.Kodiak.Default`, and `Vehicle.Variant.Stationary.STN_05` → `VehicleDestroyed.STN_05` (was `VehicleDestroyed.Mortar`).
- **Supply crates (table 1):** `ID.Item.VehicleSupplyCrate.Container.Free` → `DestroySupplyCrate.Container.Free` (was `DestroySupplyCrate.Free`). The four `Pallet.*` keys were `DestroySupplyCrate.Pallet`; they are now `.Pallet.BuildSupply`, `.Pallet.FuelSupply`, `.Pallet.MunitionsSupply` and `.Pallet.SparePartsSupply`.
- **Buildables (table 14):** 34 → 36 rows, adding `Id.Buildable.WoodBase` and `Id.Buildable.SV_Shelter`. Sub-part keys (e.g. `Bunker.Floor`) move from `BuildableDestroyed.BarbedWire` to their own tags. `Id.Buildable.Gate.Ramp` `BremmerWall` → `Gate.Ramp`, `Id.Buildable.Door` `Gate` → `Door`, and `Id.Buildable.RefuelStation` `RepairStation` → `RefuelStation`.
- **Spotting (tables 15 and 16):** 47 → 51 rows each, adding the four vehicle keys `WHL_08.Default`, `WHL_08.MachineGun`, `TNK_04.Default` and `MGNest`. 37 of the 47 existing keys in each table have a new tag, e.g. `Spotting.Added.Huey` → `Spotting.Added.Huey.Default`.
- **Reward formulas, 17a ([`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json)):** 161 → 298 rows and 311 → 585 resource rows. 46 existing formulas changed, e.g. FOB-supplied assists are now divided by `NumberOfAssisters`, and `DeploySupplyCrate` gains a crate-streak term (`CrateStreak`).
- **Literal values, 17a:** `VehicleDestroyed.TNK_01.Heavy` 7000.0 → 5500.0; `VehicleDestroyed.Mortar` 300.0 → 650.0; `VehicleDestroyed.Phalanx` 3000.0 → 1200.0; `DestroySupplyCrate.Small.Armoured` 250.0 → 500.0; `DestroySupplyCrate.Large.Armoured` 500.0 → 800.0.
- **Reward formulas, 17b and 17c:** [`DT_ChallengeRewards_SessionEvents_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json) 29 → 47 rows and [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) 44 → 130 rows. 20 and 16 formulas changed respectively.
- **Reward formulas, 17d:** [`DT_ChallengeRewards_SessionEvents_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_HotZoneMagnet.json) is unchanged (3 rows, no formula changes).
- **Shared definitions:** [`DT_Challenges_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_Challenges_SessionEvents_Shared.json) goes from 0 to 10 rows (achievement definitions, see section 19).
- **Removed:** no files and no lookup rows were removed.

---

## 1. [`DT_RewardLookup_SessionEvent_DestroySupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroySupplyCrate.json)

Maps supply-crate item IDs to reward tags for the destroy-supply-crate event.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroySupplyCrate.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 10

| Row key | RewardTag | Tag |
|---|---|---|
| `ID.Item.VehicleSupplyCrate.Free` | Challenges.Rewards.DestroySupplyCrate.Free | ID.Item.VehicleSupplyCrate.Free |
| `ID.Item.VehicleSupplyCrate.Container.Free` | Challenges.Rewards.DestroySupplyCrate.Container.Free | ID.Item.VehicleSupplyCrate.Container.Free |
| `ID.Item.VehicleSupplyCrate.Small` | Challenges.Rewards.DestroySupplyCrate.Small | ID.Item.VehicleSupplyCrate.Small |
| `ID.Item.VehicleSupplyCrate.Small.Armoured` | Challenges.Rewards.DestroySupplyCrate.Small.Armoured | ID.Item.VehicleSupplyCrate.Small.Armoured |
| `ID.Item.VehicleSupplyCrate.Large` | Challenges.Rewards.DestroySupplyCrate.Large | ID.Item.VehicleSupplyCrate.Large |
| `ID.Item.VehicleSupplyCrate.Large.Armoured` | Challenges.Rewards.DestroySupplyCrate.Large.Armoured | ID.Item.VehicleSupplyCrate.Large.Armoured |
| `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet.BuildSupply | ID.Item.VehicleSupplyCrate.Pallet.BuildSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet.FuelSupply | ID.Item.VehicleSupplyCrate.Pallet.FuelSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet.MunitionsSupply | ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet.SparePartsSupply | ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply |

**Notes:**
- `ID.Item.VehicleSupplyCrate.Free` maps to `DestroySupplyCrate.Free`, and `.Container.Free` to `DestroySupplyCrate.Container.Free`. The four `Pallet.*` rows each have their own `DestroySupplyCrate.Pallet.*` tag.
- Armoured crates (`Small.Armoured`, `Large.Armoured`) have their own tags, separate from the unarmoured tiers.
- Keys use the `ID.Item.` prefix, as in the repair-tool table.

---

## 2. [`DT_RewardLookup_SessionEvent_DestroyVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicle.json)

Maps vehicle variant keys to `VehicleDestroyed` reward tags, grouped by vehicle family.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicle.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 34

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.VehicleDestroyed.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.VehicleDestroyed.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.VehicleDestroyed.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.VehicleDestroyed.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Stationary.Loudspeaker` | Challenges.Rewards.VehicleDestroyed.Loudspeaker | Vehicle.Variant.Stationary.Loudspeaker |
| `Vehicle.Variant.Stationary.MistralAA` | Challenges.Rewards.VehicleDestroyed.MistralAA | Vehicle.Variant.Stationary.MistralAA |
| `Vehicle.Variant.Stationary.Mortar` | Challenges.Rewards.VehicleDestroyed.Mortar | Vehicle.Variant.Stationary.Mortar |
| `Vehicle.Variant.Stationary.Phalanx` | Challenges.Rewards.VehicleDestroyed.Phalanx | Vehicle.Variant.Stationary.Phalanx |
| `Vehicle.Variant.Stationary.STN_05` | Challenges.Rewards.VehicleDestroyed.STN_05 | Vehicle.Variant.Stationary.STN_05 |
| `Vehicle.Variant.Stationary.MGNest` | Challenges.Rewards.VehicleDestroyed.MGNest | Vehicle.Variant.Stationary.MGNest |

**Notes:**
- Each row has its own tag, named after the vehicle family and variant (for example `Kodiak.Default`, `Kodiak.MachineGun` and `Kodiak.Pickup`). TNK_01's Heavy, AntiAir and Artillery variants each have a separate tag.
- `Vehicle.Variant.Stationary.STN_05` maps to `VehicleDestroyed.STN_05`, separate from `Stationary.Mortar`, which maps to `VehicleDestroyed.Mortar`.

---

## 3. [`DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist.json)

Vehicle keys from table 2, mapped to the FOB-supplied assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 28

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |

**Notes:**
- 28 rows. It omits the six `Vehicle.Variant.Stationary.*` keys, which table 2 (34 rows) includes.
- Tags use `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.<Family>.<Variant>`, with the same family grouping as table 2.

---

## 4. [`DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist.json)

Vehicle keys from table 2, mapped to the logistic-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 28

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |

**Notes:**
- Key set matches table 3 (28 keys). Only the tag prefix differs.

---

## 5. [`DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist.json)

Vehicle keys from table 2, mapped to the revive-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 28

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |

**Notes:**
- Key set matches tables 3 and 4 (28 keys). Only the tag prefix differs.

---

## 6. [`DT_RewardLookup_SessionEvent_DestroyVehicleSection`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleSection.json)

Vehicle keys from table 2, mapped to `DestroyVehicleSection` reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleSection.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 28

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.DestroyVehicleSection.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.DestroyVehicleSection.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.DestroyVehicleSection.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.DestroyVehicleSection.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.DestroyVehicleSection.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.DestroyVehicleSection.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.DestroyVehicleSection.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.DestroyVehicleSection.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.DestroyVehicleSection.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.DestroyVehicleSection.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.DestroyVehicleSection.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.DestroyVehicleSection.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.DestroyVehicleSection.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.DestroyVehicleSection.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.DestroyVehicleSection.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.DestroyVehicleSection.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.DestroyVehicleSection.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.DestroyVehicleSection.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.DestroyVehicleSection.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.DestroyVehicleSection.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.DestroyVehicleSection.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.DestroyVehicleSection.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.DestroyVehicleSection.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.DestroyVehicleSection.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.DestroyVehicleSection.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |

**Notes:**
- Key set matches tables 3 to 5 (28 keys). The tag prefix is `Challenges.Rewards.DestroyVehicleSection.`, not `VehicleDestroyed`.

---

## 7. [`DT_RewardLookup_SessionEvent_HealPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer.json)

Maps healing item IDs to the heal-player reward tag.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 6

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Item.Bandage` | Challenges.Rewards.HealPlayer.Bandage | Id.Item.Bandage |
| `Id.Item.SuperBandage` | Challenges.Rewards.HealPlayer.SuperBandage | Id.Item.SuperBandage |
| `Id.Item.MedKit.Standard` | Challenges.Rewards.HealPlayer.MedKit | Id.Item.MedKit.Standard |
| `Id.Item.StimPen` | Challenges.Rewards.HealPlayer.StimPen | Id.Item.StimPen |
| `Id.Item.AdrenalinePen` | Challenges.Rewards.HealPlayer.AdrenalinePen | Id.Item.AdrenalinePen |
| `Id.Item.Defibrillator.Standard` | Challenges.Rewards.HealPlayer.Defibrillator | Id.Item.Defibrillator.Standard |

**Notes:**
- Keys use the `Id.Item.` prefix. Some tags shorten the item name: `Id.Item.MedKit.Standard` maps to `HealPlayer.MedKit`, and `Id.Item.Defibrillator.Standard` to `HealPlayer.Defibrillator`.

---

## 8. [`DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist.json)

Same six healing item keys as table 7, mapped to the logistic-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 6

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Item.Bandage` | Challenges.Rewards.HealPlayer.LogisticAssist.Bandage | Id.Item.Bandage |
| `Id.Item.SuperBandage` | Challenges.Rewards.HealPlayer.LogisticAssist.SuperBandage | Id.Item.SuperBandage |
| `Id.Item.MedKit.Standard` | Challenges.Rewards.HealPlayer.LogisticAssist.MedKit | Id.Item.MedKit.Standard |
| `Id.Item.StimPen` | Challenges.Rewards.HealPlayer.LogisticAssist.StimPen | Id.Item.StimPen |
| `Id.Item.AdrenalinePen` | Challenges.Rewards.HealPlayer.LogisticAssist.AdrenalinePen | Id.Item.AdrenalinePen |
| `Id.Item.Defibrillator.Standard` | Challenges.Rewards.HealPlayer.LogisticAssist.Defibrillator | Id.Item.Defibrillator.Standard |

**Notes:**
- Same six keys as table 7. Only the tag prefix differs.

---

## 9. [`DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist.json)

Same six healing item keys as table 7, mapped to the revive-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 6

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Item.Bandage` | Challenges.Rewards.HealPlayer.ReviveAssist.Bandage | Id.Item.Bandage |
| `Id.Item.SuperBandage` | Challenges.Rewards.HealPlayer.ReviveAssist.SuperBandage | Id.Item.SuperBandage |
| `Id.Item.MedKit.Standard` | Challenges.Rewards.HealPlayer.ReviveAssist.MedKit | Id.Item.MedKit.Standard |
| `Id.Item.StimPen` | Challenges.Rewards.HealPlayer.ReviveAssist.StimPen | Id.Item.StimPen |
| `Id.Item.AdrenalinePen` | Challenges.Rewards.HealPlayer.ReviveAssist.AdrenalinePen | Id.Item.AdrenalinePen |
| `Id.Item.Defibrillator.Standard` | Challenges.Rewards.HealPlayer.ReviveAssist.Defibrillator | Id.Item.Defibrillator.Standard |

**Notes:**
- Same six keys as table 7. Only the tag prefix differs.

---

## 10. [`DT_RewardLookup_SessionEvent_RepairVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RepairVehicle.json)

Maps the three repair-tool IDs to repair-vehicle reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RepairVehicle.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 3

| Row key | RewardTag | Tag |
|---|---|---|
| `ID.Item.RepairTool.Wrench.Standard` | Challenges.Rewards.RepairVehicle.Wrench.Standard | ID.Item.RepairTool.Wrench.Standard |
| `ID.Item.RepairTool.Drill.Light` | Challenges.Rewards.RepairVehicle.Drill.Light | ID.Item.RepairTool.Drill.Light |
| `ID.Item.RepairTool.Drill.Heavy` | Challenges.Rewards.RepairVehicle.Drill.Heavy | ID.Item.RepairTool.Drill.Heavy |

**Notes:**
- Keys use the `ID.Item.` prefix. Tags name the tool and variant (`Wrench.Standard`, `Drill.Light`, `Drill.Heavy`).

---

## 11. [`DT_RewardLookup_SessionEvent_RevivePlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayer.json)

Maps revive-related item IDs to revive-player reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayer.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 6

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Item.Defibrillator.Standard` | Challenges.Rewards.RevivePlayer.Defibrillator | Id.Item.Defibrillator.Standard |
| `Id.Item.StimPen` | Challenges.Rewards.RevivePlayer.StimPen | Id.Item.StimPen |
| `Id.Item.AdrenalinePen` | Challenges.Rewards.RevivePlayer.AdrenalinePen | Id.Item.AdrenalinePen |
| `Id.Item.MedKit.Standard` | Challenges.Rewards.RevivePlayer.Medkit | Id.Item.MedKit.Standard |
| `Id.Item.Resuscitator.Cheap` | Challenges.Rewards.RevivePlayer.Resuscitator.Cheap | Id.Item.Resuscitator.Cheap |
| `Id.Item.Resuscitator.Standard` | Challenges.Rewards.RevivePlayer.Resuscitator.Standard | Id.Item.Resuscitator.Standard |

**Notes:**
- `Id.Item.MedKit.Standard` maps to `RevivePlayer.Medkit` (lowercase k in the tag), while the heal table uses [`MedKit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MedKit/Content/MedKit.json).
- `Resuscitator.Cheap` and `Resuscitator.Standard` each have their own tag.

---

## 12. [`DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist.json)

Same six item keys as table 11, mapped to the logistic-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 6

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Item.Defibrillator.Standard` | Challenges.Rewards.RevivePlayer.LogisticAssist.Defibrilator | Id.Item.Defibrillator.Standard |
| `Id.Item.StimPen` | Challenges.Rewards.RevivePlayer.LogisticAssist.StimPen | Id.Item.StimPen |
| `Id.Item.AdrenalinePen` | Challenges.Rewards.RevivePlayer.LogisticAssist.AdrenalinePen | Id.Item.AdrenalinePen |
| `Id.Item.MedKit.Standard` | Challenges.Rewards.RevivePlayer.LogisticAssist.Medkit | Id.Item.MedKit.Standard |
| `Id.Item.Resuscitator.Cheap` | Challenges.Rewards.RevivePlayer.LogisticAssist.Resuscitator | Id.Item.Resuscitator.Cheap |
| `Id.Item.Resuscitator.Standard` | Challenges.Rewards.RevivePlayer.LogisticAssist.Resuscitator | Id.Item.Resuscitator.Standard |

**Notes:**
- The tag spellings are kept as exported: `Defibrilator` (not [`Defibrillator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Defibrillator/Content/Defibrillator.json)) and `Medkit`. Both `Resuscitator` keys share the tag `RevivePlayer.LogisticAssist.Resuscitator`.

---

## 13. [`DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist.json)

Same six item keys as table 11, mapped to the revive-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 6

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Item.Defibrillator.Standard` | Challenges.Rewards.RevivePlayer.ReviveAssist.Defibrilator | Id.Item.Defibrillator.Standard |
| `Id.Item.StimPen` | Challenges.Rewards.RevivePlayer.ReviveAssist.StimPen | Id.Item.StimPen |
| `Id.Item.AdrenalinePen` | Challenges.Rewards.RevivePlayer.ReviveAssist.AdrenalinePen | Id.Item.AdrenalinePen |
| `Id.Item.MedKit.Standard` | Challenges.Rewards.RevivePlayer.ReviveAssist.Medkit | Id.Item.MedKit.Standard |
| `Id.Item.Resuscitator.Cheap` | Challenges.Rewards.RevivePlayer.ReviveAssist.Resuscitator | Id.Item.Resuscitator.Cheap |
| `Id.Item.Resuscitator.Standard` | Challenges.Rewards.RevivePlayer.ReviveAssist.Resuscitator | Id.Item.Resuscitator.Standard |

**Notes:**
- Same spellings and shared `Resuscitator` tag as table 12 (`Defibrilator`, `Medkit`).

---

## 14. [`DT_RewardLookup_SessionEvent_BuildableDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_BuildableDestroyed.json)

Maps buildable IDs, including some sub-parts, to buildable-destroyed reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_BuildableDestroyed.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 36

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Buildable.AirRaidShelter` | Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter | Id.Buildable.AirRaidShelter |
| `Id.Buildable.AirRaidShelter.Ceiling` | Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter.Ceiling | Id.Buildable.AirRaidShelter.Ceiling |
| `Id.Buildable.AirRaidShelter.Floor` | Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter.Floor | Id.Buildable.AirRaidShelter.Floor |
| `Id.Buildable.BarbedWire` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.BarbedWire |
| `Id.Buildable.BremmerWall` | Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall | Id.Buildable.BremmerWall |
| `Id.Buildable.Bunker` | Challenges.Rewards.Buildables.BuildableDestroyed.Bunker | Id.Buildable.Bunker |
| `Id.Buildable.Bunker.Floor` | Challenges.Rewards.Buildables.BuildableDestroyed.Bunker.Floor | Id.Buildable.Bunker.Floor |
| `Id.Buildable.Bunker.Roof` | Challenges.Rewards.Buildables.BuildableDestroyed.Bunker.Roof | Id.Buildable.Bunker.Roof |
| `Id.Buildable.CamoNetTent` | Challenges.Rewards.Buildables.BuildableDestroyed.CamoNetTent | Id.Buildable.CamoNetTent |
| `Id.Buildable.CrowsNest` | Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest | Id.Buildable.CrowsNest |
| `Id.Buildable.CrowsNest.BaseFloor` | Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.BaseFloor | Id.Buildable.CrowsNest.BaseFloor |
| `Id.Buildable.CrowsNest.FirstFloor` | Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.FirstFloor | Id.Buildable.CrowsNest.FirstFloor |
| `Id.Buildable.CrowsNest.Roof` | Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.Roof | Id.Buildable.CrowsNest.Roof |
| `Id.Buildable.Door` | Challenges.Rewards.Buildables.BuildableDestroyed.Door | Id.Buildable.Door |
| `Id.Buildable.Door.TopSegment` | Challenges.Rewards.Buildables.BuildableDestroyed.Door.TopSegment | Id.Buildable.Door.TopSegment |
| `Id.Buildable.FloorBoard` | Challenges.Rewards.Buildables.BuildableDestroyed.FloorBoard | Id.Buildable.FloorBoard |
| `Id.Buildable.FOB` | Challenges.Rewards.Buildables.BuildableDestroyed.FOB | Id.Buildable.FOB |
| `Id.Buildable.Gate` | Challenges.Rewards.Buildables.BuildableDestroyed.Gate | Id.Buildable.Gate |
| `Id.Buildable.Gate.Ramp` | Challenges.Rewards.Buildables.BuildableDestroyed.Gate.Ramp | Id.Buildable.Gate.Ramp |
| `Id.Buildable.HBlock` | Challenges.Rewards.Buildables.BuildableDestroyed.HBlock | Id.Buildable.HBlock |
| `Id.Buildable.HBlockQuadWall` | Challenges.Rewards.Buildables.BuildableDestroyed.HBlockQuadWall | Id.Buildable.HBlockQuadWall |
| `Id.Buildable.HotzoneMagnet` | Challenges.Rewards.Buildables.BuildableDestroyed.HotZoneMagnet | Id.Buildable.HotzoneMagnet |
| `Id.Buildable.Loudspeaker` | Challenges.Rewards.Buildables.BuildableDestroyed.Loudspeaker | Id.Buildable.Loudspeaker |
| `Id.Buildable.MistralAA` | Challenges.Rewards.Buildables.BuildableDestroyed.MistralAA | Id.Buildable.MistralAA |
| `Id.Buildable.Mortar` | Challenges.Rewards.Buildables.BuildableDestroyed.Mortar | Id.Buildable.Mortar |
| `Id.Buildable.Phalanx` | Challenges.Rewards.Buildables.BuildableDestroyed.Phalanx | Id.Buildable.Phalanx |
| `Id.Buildable.Radio` | Challenges.Rewards.Buildables.BuildableDestroyed.Radio | Id.Buildable.Radio |
| `Id.Buildable.Ramp` | Challenges.Rewards.Buildables.BuildableDestroyed.Ramp | Id.Buildable.Ramp |
| `Id.Buildable.RefuelStation` | Challenges.Rewards.Buildables.BuildableDestroyed.RefuelStation | Id.Buildable.RefuelStation |
| `Id.Buildable.RepairStation` | Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation | Id.Buildable.RepairStation |
| `Id.Buildable.SandbagWall` | Challenges.Rewards.Buildables.BuildableDestroyed.SandbagWall | Id.Buildable.SandbagWall |
| `Id.Buildable.TallHBlock` | Challenges.Rewards.Buildables.BuildableDestroyed.TallHBlock | Id.Buildable.TallHBlock |
| `Id.Buildable.TankTrap` | Challenges.Rewards.Buildables.BuildableDestroyed.TankTrap | Id.Buildable.TankTrap |
| `Id.Buildable.WindowBoard` | Challenges.Rewards.Buildables.BuildableDestroyed.WindowBoard | Id.Buildable.WindowBoard |
| `Id.Buildable.WoodBase` | Challenges.Rewards.Buildables.BuildableDestroyed.WoodBase | Id.Buildable.WoodBase |
| `Id.Buildable.SV_Shelter` | Challenges.Rewards.Buildables.BuildableDestroyed.SV_Shelter | Id.Buildable.SV_Shelter |

**Notes:**
- Each row has its own tag. Sub-part keys follow their key: for example `Id.Buildable.Bunker.Floor` maps to `BuildableDestroyed.Bunker.Floor`, and `Id.Buildable.Door.TopSegment` maps to `BuildableDestroyed.Door.TopSegment`.
- `Id.Buildable.Gate.Ramp` maps to `BuildableDestroyed.Gate.Ramp`, separate from `Id.Buildable.Gate`.
- `Id.Buildable.Door` maps to `BuildableDestroyed.Door`, and `Id.Buildable.Gate` to `BuildableDestroyed.Gate`.
- `Id.Buildable.RefuelStation` and `Id.Buildable.RepairStation` each have their own tag.
- This table sits in the BuildableRewards bundle, not in [`Challenges_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/Challenges_KOTH.json).

---

## 15. [`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json)

Maps spotted vehicles, stationary weapons, mines, supply crates and some buildables to `Spotting.Added` reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 51

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.Spotting.Added.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.Spotting.Added.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.Spotting.Added.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.Spotting.Added.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.Spotting.Added.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.Spotting.Added.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.Spotting.Added.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.Spotting.Added.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.Spotting.Added.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.Spotting.Added.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.Spotting.Added.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.Spotting.Added.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.Spotting.Added.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.Spotting.Added.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.Spotting.Added.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.Spotting.Added.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.Spotting.Added.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.Spotting.Added.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.Spotting.Added.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.Spotting.Added.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.Spotting.Added.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.Spotting.Added.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.Spotting.Added.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.Spotting.Added.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.Spotting.Added.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.Spotting.Added.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.Spotting.Added.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.Spotting.Added.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Id.Item.Claymore` | Challenges.Rewards.Spotting.Added.Claymore | Id.Item.Claymore |
| `ID.Item.ATMine` | Challenges.Rewards.Spotting.Added.ATMine | ID.Item.ATMine |
| `Id.Buildable.FOB` | Challenges.Rewards.Spotting.Added.FOB | Id.Buildable.FOB |
| `Id.Buildable.HotzoneMagnet` | Challenges.Rewards.Spotting.Added.BuildableHotZoneMagnet | Id.Buildable.HotzoneMagnet |
| `ID.Item.VehicleSupplyCrate.Free` | Challenges.Rewards.Spotting.Added.SupplyCrate.Free | ID.Item.VehicleSupplyCrate.Free |
| `ID.Item.VehicleSupplyCrate.Container.Free` | Challenges.Rewards.Spotting.Added.SupplyCrate.Container.Free | ID.Item.VehicleSupplyCrate.Container.Free |
| `ID.Item.VehicleSupplyCrate.Small` | Challenges.Rewards.Spotting.Added.SupplyCrate.Small | ID.Item.VehicleSupplyCrate.Small |
| `ID.Item.VehicleSupplyCrate.Small.Armoured` | Challenges.Rewards.Spotting.Added.SupplyCrate.Small.Armoured | ID.Item.VehicleSupplyCrate.Small.Armoured |
| `ID.Item.VehicleSupplyCrate.Large` | Challenges.Rewards.Spotting.Added.SupplyCrate.Large | ID.Item.VehicleSupplyCrate.Large |
| `ID.Item.VehicleSupplyCrate.Large.Armoured` | Challenges.Rewards.Spotting.Added.SupplyCrate.Large.Armoured | ID.Item.VehicleSupplyCrate.Large.Armoured |
| `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.BuildSupply | ID.Item.VehicleSupplyCrate.Pallet.BuildSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.FuelSupply | ID.Item.VehicleSupplyCrate.Pallet.FuelSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.MunitionsSupply | ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.SparePartsSupply | ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply |
| `Vehicle.Variant.Stationary.MistralAA` | Challenges.Rewards.Spotting.Added.MistralAA | Vehicle.Variant.Stationary.MistralAA |
| `Vehicle.Variant.Stationary.Mortar` | Challenges.Rewards.Spotting.Added.Mortar | Vehicle.Variant.Stationary.Mortar |
| `Vehicle.Variant.Stationary.Phalanx` | Challenges.Rewards.Spotting.Added.Phalanx | Vehicle.Variant.Stationary.Phalanx |
| `Vehicle.Variant.Stationary.Loudspeaker` | Challenges.Rewards.Spotting.Added.Loudspeaker | Vehicle.Variant.Stationary.Loudspeaker |
| `Id.Buildable.Radio` | Challenges.Rewards.Spotting.Added.BuildableRadio | Id.Buildable.Radio |
| `Id.Buildable.RepairStation` | Challenges.Rewards.Spotting.Added.BuildableRepairStation | Id.Buildable.RepairStation |
| `Id.Buildable.RefuelStation` | Challenges.Rewards.Spotting.Added.BuildableRefuelStation | Id.Buildable.RefuelStation |
| `Vehicle.Variant.Stationary.STN_05` | Challenges.Rewards.Spotting.Added.STN_05 | Vehicle.Variant.Stationary.STN_05 |
| `Vehicle.Variant.Stationary.MGNest` | Challenges.Rewards.Spotting.Added.MGNest | Vehicle.Variant.Stationary.MGNest |

**Notes:**
- 34 vehicle keys, the same set as table 2.
- Each row has its own tag. For example, `Vehicle.Variant.Stationary.Loudspeaker` maps to `Spotting.Added.Loudspeaker`, `Id.Buildable.Radio` to `Spotting.Added.BuildableRadio`, and `Vehicle.Variant.Stationary.STN_05` to `Spotting.Added.STN_05`.
- The `VehicleSupplyCrate` keys use `Spotting.Added.SupplyCrate.` tags. For example, `Pallet.BuildSupply` maps to `Spotting.Added.SupplyCrate.Pallet.BuildSupply`.
- Key prefixes are mixed (`Id.` and `ID.`) within this table, as exported.

---

## 16. [`DT_RewardLookup_SessionEvent_Spotting_Removed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Removed.json)

Same key set as table 15, mapped to `Spotting.Removed` reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Removed.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 51

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.Spotting.Removed.Kodiak.Default | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.Spotting.Removed.Kodiak.MachineGun | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.Spotting.Removed.Kodiak.Pickup | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Land.Wheeled.WHL_08.Default` | Challenges.Rewards.Spotting.Removed.WHL_08.Default | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` | Challenges.Rewards.Spotting.Removed.WHL_08.MachineGun | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.Spotting.Removed.LittleBird.Default | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.Spotting.Removed.Huey.Default | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.Spotting.Removed.Huey.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.Spotting.Removed.Blackhawk.Default | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.Spotting.Removed.Blackhawk.MountedMachineGuns | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.Spotting.Removed.LittleBird.MountedMachineGuns | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.Spotting.Removed.LittleBird.RocketPods | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.Spotting.Removed.Havoc.Default | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.Spotting.Removed.SpawnVehicle.Lonestar | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.Spotting.Removed.SpawnVehicle.Manticore | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.Spotting.Removed.SpawnVehicle.Valkyra | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.Spotting.Removed.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.Spotting.Removed.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.Spotting.Removed.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_04.Default` | Challenges.Rewards.Spotting.Removed.TNK_04.Default | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.Spotting.Removed.Bobcat.Default | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.Spotting.Removed.Humvee.Default | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.Spotting.Removed.Humvee.MachineGun | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.Spotting.Removed.Humvee.Minigun | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.Spotting.Removed.DuneBuggy.Default | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.Spotting.Removed.Ural.Battle | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.Spotting.Removed.Ural.Attack | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.Spotting.Removed.Ural.Default | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Id.Item.Claymore` | Challenges.Rewards.Spotting.Removed.Claymore | Id.Item.Claymore |
| `ID.Item.ATMine` | Challenges.Rewards.Spotting.Removed.ATMine | ID.Item.ATMine |
| `Id.Buildable.FOB` | Challenges.Rewards.Spotting.Removed.FOB | Id.Buildable.FOB |
| `Id.Buildable.HotzoneMagnet` | Challenges.Rewards.Spotting.Removed.BuildableHotZoneMagnet | Id.Buildable.HotzoneMagnet |
| `ID.Item.VehicleSupplyCrate.Free` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Free | ID.Item.VehicleSupplyCrate.Free |
| `ID.Item.VehicleSupplyCrate.Container.Free` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Container.Free | ID.Item.VehicleSupplyCrate.Container.Free |
| `ID.Item.VehicleSupplyCrate.Small` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Small | ID.Item.VehicleSupplyCrate.Small |
| `ID.Item.VehicleSupplyCrate.Small.Armoured` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Small.Armoured | ID.Item.VehicleSupplyCrate.Small.Armoured |
| `ID.Item.VehicleSupplyCrate.Large` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Large | ID.Item.VehicleSupplyCrate.Large |
| `ID.Item.VehicleSupplyCrate.Large.Armoured` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Large.Armoured | ID.Item.VehicleSupplyCrate.Large.Armoured |
| `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.BuildSupply | ID.Item.VehicleSupplyCrate.Pallet.BuildSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.FuelSupply | ID.Item.VehicleSupplyCrate.Pallet.FuelSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.MunitionsSupply | ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.SparePartsSupply | ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply |
| `Vehicle.Variant.Stationary.MistralAA` | Challenges.Rewards.Spotting.Removed.MistralAA | Vehicle.Variant.Stationary.MistralAA |
| `Vehicle.Variant.Stationary.Mortar` | Challenges.Rewards.Spotting.Removed.Mortar | Vehicle.Variant.Stationary.Mortar |
| `Vehicle.Variant.Stationary.Phalanx` | Challenges.Rewards.Spotting.Removed.Phalanx | Vehicle.Variant.Stationary.Phalanx |
| `Vehicle.Variant.Stationary.Loudspeaker` | Challenges.Rewards.Spotting.Removed.Loudspeaker | Vehicle.Variant.Stationary.Loudspeaker |
| `Id.Buildable.Radio` | Challenges.Rewards.Spotting.Removed.BuildableRadio | Id.Buildable.Radio |
| `Id.Buildable.RepairStation` | Challenges.Rewards.Spotting.Removed.BuildableRepairStation | Id.Buildable.RepairStation |
| `Id.Buildable.RefuelStation` | Challenges.Rewards.Spotting.Removed.BuildableRefuelStation | Id.Buildable.RefuelStation |
| `Vehicle.Variant.Stationary.STN_05` | Challenges.Rewards.Spotting.Removed.STN_05 | Vehicle.Variant.Stationary.STN_05 |
| `Vehicle.Variant.Stationary.MGNest` | Challenges.Rewards.Spotting.Removed.MGNest | Vehicle.Variant.Stationary.MGNest |

**Notes:**
- Same 47 keys and grouping as table 15. Only the prefix changes, from `Spotting.Added.` to `Spotting.Removed.`.

---

## 17. Reward formulas (`DT_ChallengeRewards_SessionEvents_*`)

Each row gives the currency tag and a formula for the reward. Most formula variables are literals inside the row itself (each resource's `Selectors` and `Variables`); the rest are runtime game values such as the event's base reward or kill streak. The **Value** column is each row evaluated as written, for the state picked with the **Zone multiplier** switch in the sidebar (you and the target both in a control zone, or both in a hot zone; `_tools/zone_rewards.py`). A value written as ×N is N times a runtime amount: hover it to see which.

### 17a. [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json) (298 rows)
- **Package:** `Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.uasset`

| Row | Resource | Formula |
|---|---|---|
| `Challenges.Rewards.PlayerKill` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * InstigatorZoneModifier * InstigatorWeight) + ((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * TargetZoneModifier * TargetWeight)) * DistanceToTarget * RevengeModifier * KillStreakStoppedModifier) * FriendlyModifier * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.PlayerKill` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.PlayerKill.CrewAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * CrewModifier` |
| `Challenges.Rewards.PlayerKill.CrewAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.PlayerKill.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.PlayerKill.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.FOBSuppliedAssist` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedModifier) / NumberOfAssisters` |
| `Challenges.Rewards.PlayerKill.FOBSuppliedAssist` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.PlayerKill.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.PlayerKill.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.Assist` | `Attribute.Meta.Currency.Cash` | `(TotalRewardSelector * AssistScalingModifierSelector * CurveValueSelector) + (TotalRewardSelector * AssistBaseModifierSelector)` |
| `Challenges.Rewards.PlayerKill.Assist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.Assist.CrewAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * CrewModifier` |
| `Challenges.Rewards.PlayerKill.Assist.CrewAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.Assist.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.PlayerKill.Assist.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.Assist.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.PlayerKill.Assist.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.Assist.FOBSuppliedAssist` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedModifier) / NumberOfAssisters` |
| `Challenges.Rewards.PlayerKill.Assist.FOBSuppliedAssist` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.PlayerKill.Assist.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.PlayerKill.Assist.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.WHL_08` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.WHL_08` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Huey` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Huey.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Huey.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Havoc` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Havoc.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * FactionScoreScalar * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * FactionScoreScalar * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * FactionScoreScalar * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * FactionScoreScalar * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + ((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Bobcat` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Humvee` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Humvee.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Ural` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Ural.Attack` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Ural.Battle` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Ural.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Ural.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Loudspeaker` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Loudspeaker` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.MistralAA` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.MistralAA` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.Mortar` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Mortar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.Phalanx` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Phalanx` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.MGNest` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.MGNest` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.CrewAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * CrewModifier` |
| `Challenges.Rewards.VehicleDestroyed.CrewAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Littlebird` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Littlebird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Attack` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Battle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Attack` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Battle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Attack` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Battle` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Default` | `Attribute.Meta.Currency.Cash` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural.Default` | `Attribute.Meta.XP.Role` | `(BaseReward) / NumberOfAssisters` |
| `Challenges.Rewards.VehicleDestroyed.STN_05` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.STN_05` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.VehicleDestroyed.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.WHL_08` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.WHL_08` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Huey` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Huey` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Huey.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Huey.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Havoc` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Havoc` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Havoc.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Bobcat` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Bobcat` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.DuneBuggy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Ural` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Ural` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Ural.Attack` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Ural.Battle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Ural.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Ural.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.CrewAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * CrewModifier` |
| `Challenges.Rewards.DestroyVehicleSection.CrewAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.DestroyVehicleSection.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.DestroyVehicleSection.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.DestroyVehicleSection.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.ZoneEntry` | `Attribute.Meta.Currency.Cash` | `RewardValue` |
| `Challenges.Rewards.ZoneEntry` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.ZonePresence` | `Attribute.Meta.Currency.Cash` | `RewardValue + (clamp(HotZoneStreak - 1, 0, HotZoneStreakMax) * HotZoneStreakValue)` |
| `Challenges.Rewards.HealPlayer` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight * ScaleFactor) + (BaseValue * TargetZoneModifier * TargetZoneWeight * ScaleFactor))` |
| `Challenges.Rewards.HealPlayer` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.Bandage` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight * ScaleFactor) + (BaseValue * TargetZoneModifier * TargetZoneWeight * ScaleFactor))` |
| `Challenges.Rewards.HealPlayer.Bandage` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.SuperBandage` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight * ScaleFactor) + (BaseValue * TargetZoneModifier * TargetZoneWeight * ScaleFactor))` |
| `Challenges.Rewards.HealPlayer.SuperBandage` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.MedKit` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight * ScaleFactor) + (BaseValue * TargetZoneModifier * TargetZoneWeight * ScaleFactor))` |
| `Challenges.Rewards.HealPlayer.MedKit` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.StimPen` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.HealPlayer.StimPen` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.AdrenalinePen` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.HealPlayer.AdrenalinePen` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.Defibrillator` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight * ScaleFactor) + (BaseValue * TargetZoneModifier * TargetZoneWeight * ScaleFactor))` |
| `Challenges.Rewards.HealPlayer.Defibrillator` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.Bandage` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.Bandage` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.SuperBandage` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.SuperBandage` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.MedKit` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.MedKit` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.StimPen` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.StimPen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.AdrenalinePen` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.AdrenalinePen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.Defibrillator` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.HealPlayer.LogisticAssist.Defibrillator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.Bandage` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.Bandage` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.SuperBandage` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.SuperBandage` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.MedKit` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.MedKit` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.StimPen` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.StimPen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.AdrenalinePen` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.AdrenalinePen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.Defibrillator` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.HealPlayer.ReviveAssist.Defibrillator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HealPlayer.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.HealPlayer.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroyThrowable` | `Attribute.Meta.Currency.Cash` | `(BaseReward * ZoneModifier) * AlignmentModifier ` |
| `Challenges.Rewards.DestroyThrowable` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight * AssistScalar) + (BaseValue * TargetZoneModifier * TargetZoneWeight * AssistScalar))` |
| `Challenges.Rewards.RevivePlayer` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AssistScalar)` |
| `Challenges.Rewards.RevivePlayer.Defibrillator` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.RevivePlayer.Defibrillator` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.RevivePlayer.StimPen` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.RevivePlayer.StimPen` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.RevivePlayer.AdrenalinePen` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.RevivePlayer.AdrenalinePen` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.RevivePlayer.Resuscitator.Cheap` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.RevivePlayer.Resuscitator.Cheap` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.RevivePlayer.Resuscitator.Standard` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.RevivePlayer.Resuscitator.Standard` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.RevivePlayer.Medkit` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight))` |
| `Challenges.Rewards.RevivePlayer.Medkit` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.Defibrilator` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.Defibrilator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.StimPen` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.StimPen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.AdrenalinePen` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.AdrenalinePen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.Medkit` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.Medkit` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.Resuscitator` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.RevivePlayer.LogisticAssist.Resuscitator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.Defibrilator` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.Defibrilator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.StimPen` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.StimPen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.AdrenalinePen` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.AdrenalinePen` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.Medkit` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.Medkit` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.Resuscitator` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.RevivePlayer.ReviveAssist.Resuscitator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.RevivePlayer.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.RevivePlayer.TargetInObjective` | `Attribute.Meta.Currency.Cash` | `(BaseValue * InstigatorZoneModifier * InstigatorZoneWeight) + (BaseValue * TargetZoneModifier * TargetZoneWeight)` |
| `Challenges.Rewards.RefuelVehicle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier)` |
| `Challenges.Rewards.RefuelVehicle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.DeployOnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward` |
| `Challenges.Rewards.DeploySupplyCrate` | `Attribute.Meta.Currency.Cash` | `(BaseReward + (clamp(CrateStreak - 1, 0, CrateStreakMax) * CrateStreakValue))  * TargetZoneModifier` |
| `Challenges.Rewards.DeploySupplyCrate` | `Attribute.Meta.XP.Role` | `((BaseReward + (clamp(CrateStreak - 1, 0, CrateStreakMax) * CrateStreakValue)) * TargetZoneModifier) * SupplyCrateValue` |
| `Challenges.Rewards.SupplyPalletDropped` | `Attribute.Meta.Currency.Cash` | `BaseReward * TargetZoneModifier` |
| `Challenges.Rewards.SupplyPalletDropped` | `Attribute.Meta.XP.Role` | `(BaseReward * TargetZoneModifier)` |
| `Challenges.Rewards.RepairVehicle.Wrench.Standard` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier * OwnerModifier)` |
| `Challenges.Rewards.RepairVehicle.Wrench.Standard` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Light` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier * OwnerModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Light` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Heavy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier * OwnerModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Heavy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.PurchaseFromSupplyCrate` | `Attribute.Meta.Currency.Cash` | `PurchaseValue * (MarkupMultiplier - (MarkupMultiplier - 1) * clamp(LastVictimCount, 0, LastVictimCountMax) / LastVictimCountMax)` |
| `Challenges.Rewards.PurchaseFromSupplyCrate` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * PurchaseValue` |
| `Challenges.Rewards.DestroySupplyCrate.Container.Free` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` |
| `Challenges.Rewards.DestroySupplyCrate.Container.Free` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Free` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` |
| `Challenges.Rewards.DestroySupplyCrate.Free` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Small` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` |
| `Challenges.Rewards.DestroySupplyCrate.Small` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Small.Armoured` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` |
| `Challenges.Rewards.DestroySupplyCrate.Small.Armoured` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Large` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` |
| `Challenges.Rewards.DestroySupplyCrate.Large` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Large.Armoured` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` |
| `Challenges.Rewards.DestroySupplyCrate.Large.Armoured` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.BuildSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.BuildSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.FuelSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.FuelSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.MunitionsSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.MunitionsSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.SparePartsSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet.SparePartsSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.SupplyCrateDestroyed` | `Attribute.Meta.Currency.Cash` | `BaseReward` |
| `Challenges.Rewards.PlayerDelivered` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(PlayerStreak - 1, 0, PlayerStreakMax) * PlayerStreakValue)) * ZoneModifier) * (PlayerCount)` |
| `Challenges.Rewards.PlayerDelivered` | `Attribute.Meta.XP.Role` | `(BaseReward + (clamp(PlayerStreak - 1, 0, PlayerStreakMax) * PlayerStreakValue))` |
| `Challenges.Rewards.PassengerSurvived` | `Attribute.Meta.Currency.Cash` | `BaseReward * ZoneModifier` |
| `Challenges.Rewards.PassengerSurvived` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.SafeZoneEntered` | `Attribute.Meta.Currency.Cash` | `(BaseReward + (clamp(ReturnStreak - 1, 0, ReturnStreakMax) * ReturnStreakValue)) * max(PlayersSurvivedMin, PlayersSurvivedCount)` |
| `Challenges.Rewards.SafeZoneEntered` | `Attribute.Meta.XP.Role` | `((BaseReward + (clamp(ReturnStreak - 1, 0, ReturnStreakMax) * ReturnStreakValue)) * max(PlayersSurvivedMin, PlayersSurvivedCount))` |
| `Challenges.Rewards.SendTip` | `Attribute.Meta.Currency.Cash` | `0 - BaseReward` |
| `Challenges.Rewards.SendPreTip` | `Attribute.Meta.Currency.Cash` | `(BaseReward) * PreTipValue` |
| `Challenges.Rewards.ReceiveTip` | `Attribute.Meta.Currency.Cash` | `BaseReward` |
| `Challenges.Rewards.ReceivePreTip` | `Attribute.Meta.Currency.Cash` | `(BaseReward) * PreTipValue` |
| `Challenges.Rewards.VehicleAirborne` | `Attribute.Meta.Currency.Cash` | `BaseReward * ElapsedAirTime` |
| `Challenges.Rewards.VehicleFlyThrough` | `Attribute.Meta.Currency.Cash` | `BaseReward * clamp(RepeatActionCount, 0, RepeatActionCountMax)` |
| `Challenges.Rewards.Test` | `Attribute.Meta.Currency.Cash` | `BaseRewardModifier` |

### 17b. [`DT_ChallengeRewards_SessionEvents_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json) (47 rows)
- **Package:** `Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.uasset`

| Row | Resource | Formula |
|---|---|---|
| `Challenges.Rewards.Buildables.BuildableDamaged` | `Attribute.Meta.Currency.Cash` | `BaseValue * AlignmentModifier` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FOB` | `Attribute.Meta.Currency.Cash` | `((BaseValue + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppliesMax) * FOBSuppliesBonus)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + ((BaseValue + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppliesMax) * FOBSuppliesBonus)) * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FOB` | `Attribute.Meta.XP.Role` | `(BaseReward + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppliesMax) * FOBSuppliesBonus))` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter.Ceiling` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter.Ceiling` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter.Floor` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter.Floor` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker.Floor` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker.Floor` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker.Roof` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker.Roof` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CamoNetTent` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CamoNetTent` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.BaseFloor` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.BaseFloor` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.FirstFloor` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.FirstFloor` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.Roof` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest.Roof` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Door` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Door` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Door.TopSegment` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Door.TopSegment` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FloorBoard` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FloorBoard` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Gate` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Gate` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Gate.Ramp` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Gate.Ramp` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlock` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlock` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlockQuadWall` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlockQuadWall` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HotZoneMagnet` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HotZoneMagnet` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Loudspeaker` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Loudspeaker` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.MistralAA` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.MistralAA` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Mortar` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Mortar` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Phalanx` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Phalanx` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Radio` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Radio` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Ramp` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Ramp` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.RefuelStation` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.RefuelStation` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TallHBlock` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TallHBlock` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.SandbagWall` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.SandbagWall` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.SV_Shelter` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.SV_Shelter` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TankTrap` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TankTrap` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.WindowBoard` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.WindowBoard` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.WoodBase` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.WoodBase` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Buildables.Building` | `Attribute.Meta.Currency.Cash` | `BuildAmount * BaseReward * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.Building` | `Attribute.Meta.XP.Role` | `BuildAmount * BaseReward` |
| `Challenges.Rewards.Buildables.BuildableFinished` | `Attribute.Meta.Currency.Cash` | `((BuildCost * BaseReward) * InstigatorZoneModifier) + SchematicOwnerModifier` |
| `Challenges.Rewards.Buildables.BuildableFinished` | `Attribute.Meta.XP.Role` | `BuildCost * BaseReward` |
| `Challenges.Rewards.Buildables.SchematicPlaced` | `Attribute.Meta.Currency.Cash` | `DefaultValue * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesDeposited.Owner` | `Attribute.Meta.Currency.Cash` | `DefaultValue * BuildSuppliesDeposited * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesDeposited.Owner` | `Attribute.Meta.XP.Role` | `BaseReward * BuildSuppliesDeposited  * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesDeposited.Interactor` | `Attribute.Meta.Currency.Cash` | `DefaultValue * BuildSuppliesDeposited * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesDeposited.Interactor` | `Attribute.Meta.XP.Role` | `BaseReward  * BuildSuppliesDeposited  * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesConsumed.Owner` | `Attribute.Meta.Currency.Cash` | `DefaultValue * BuildSuppliesDeposited  * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesConsumed.Owner` | `Attribute.Meta.XP.Role` | `BaseReward * BuildSuppliesDeposited * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesConsumed.Instigator` | `Attribute.Meta.Currency.Cash` | `DefaultValue  * InstigatorZoneModifier` |
| `Challenges.Rewards.Buildables.BuildSuppliesConsumed.Instigator` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.FOBOwnerPayed` | `Attribute.Meta.Currency.Cash` | `DefaultValue * CashSpent` |
| `Challenges.Rewards.Buildables.FOBHacked` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseValue * InstigatorZoneModifier)` |
| `Challenges.Rewards.Buildables.FOBHacked` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseValue)` |
| `Challenges.Rewards.Buildables.FOBDoorClosed` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseValue * InstigatorZoneModifier)` |

### 17c. [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) (130 rows)
- **Package:** `Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.uasset`

| Row | Resource | Formula |
|---|---|---|
| `Challenges.Rewards.Spotting.Added.Player` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Player` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Bobcat` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Bobcat` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Kodiak` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Kodiak` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.WHL_08` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.WHL_08` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.LittleBird` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.LittleBird` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Huey` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Huey` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Huey.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Huey.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Havoc` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Havoc` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Havoc.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_04` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_04` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Humvee` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Humvee` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Humvee.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.DuneBuggy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Ural` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Ural` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Ural.Attack` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Ural.Battle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Ural.Default` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Ural.Default` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Claymore` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Claymore` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.ATMine` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.ATMine` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.BuildableHotZoneMagnet` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableHotZoneMagnet` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableRadio` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableRadio` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableRefuelStation` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableRefuelStation` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableRepairStation` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.BuildableRepairStation` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.FOB` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.FOB` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Loudspeaker` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.Loudspeaker` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Container.Free` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Container.Free` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Free` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Free` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Large` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Large` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Large.Armoured` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Large.Armoured` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.BuildSupply` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.BuildSupply` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.FuelSupply` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.FuelSupply` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.MunitionsSupply` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.MunitionsSupply` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.SparePartsSupply` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Pallet.SparePartsSupply` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Small` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Small` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Small.Armoured` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate.Small.Armoured` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.MistralAA` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.MistralAA` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.Phalanx` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.Phalanx` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.Mortar` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.Mortar` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.MGNest` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.MGNest` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.STN_05` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| `Challenges.Rewards.Spotting.Added.STN_05` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| `Challenges.Rewards.Spotting.Removed.Player` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Player` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Bobcat.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Bobcat.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Kodiak.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Kodiak.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Kodiak.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Kodiak.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Kodiak.Pickup` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Kodiak.Pickup` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.WHL_08` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.WHL_08` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.WHL_08.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.WHL_08.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.WHL_08.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.WHL_08.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.LittleBird` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.LittleBird.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.LittleBird.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.LittleBird.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.LittleBird.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.LittleBird.RocketPods` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.LittleBird.RocketPods` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Huey.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Huey.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Huey.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Huey.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk.MountedMachineGuns` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk.MountedMachineGuns` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Havoc.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Havoc.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle.Lonestar` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle.Lonestar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle.Manticore` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle.Manticore` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle.Valkyra` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle.Valkyra` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_04` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_04` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_04.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_04.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Humvee.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Humvee.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Humvee.MachineGun` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Humvee.MachineGun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Humvee.Minigun` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Humvee.Minigun` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.DuneBuggy.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.DuneBuggy.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Ural.Attack` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Ural.Attack` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Ural.Battle` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Ural.Battle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Ural.Default` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Ural.Default` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Claymore` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Claymore` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.ATMine` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.ATMine` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.BuildableHotZoneMagnet` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableHotZoneMagnet` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableRadio` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableRadio` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableRefuelStation` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableRefuelStation` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableRepairStation` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.BuildableRepairStation` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.FOB` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.FOB` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Loudspeaker` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.Loudspeaker` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Container.Free` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Container.Free` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Free` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Free` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Large` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Large` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Large.Armoured` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Large.Armoured` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.BuildSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.BuildSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.FuelSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.FuelSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.MunitionsSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.MunitionsSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.SparePartsSupply` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Pallet.SparePartsSupply` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Small` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Small` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Small.Armoured` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate.Small.Armoured` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.MistralAA` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.MistralAA` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.Mortar` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.Mortar` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.Phalanx` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.Phalanx` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.MGNest` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.MGNest` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.STN_05` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| `Challenges.Rewards.Spotting.Removed.STN_05` | `Attribute.Meta.XP.Role` | `(BaseReward) * BuildProgress` |

### 17d. [`DT_ChallengeRewards_SessionEvents_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_HotZoneMagnet.json) (3 rows)
- **Package:** `Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_HotZoneMagnet.uasset`

| Row | Resource | Formula |
|---|---|---|
| `Challenges.Rewards.HotZoneMagnet.TowerCaptured` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * HostileModifier)` |
| `Challenges.Rewards.HotZoneMagnet.TowerCaptured` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetActivated` | `Attribute.Meta.Currency.Cash` | `(BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetActivated` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.HotZoneMagnet.MagnetDeactivated` | `Attribute.Meta.Currency.Cash` | `(BaseReward)` |

---

## 18. How the values combine

- **Lookup shape:** each table maps a row key to a `RewardTag` string. The `Tag` column repeats the key in all 16 tables, so it adds no information.
- **Event families:** destroy supply crate (table 1); destroy vehicle, with four parallel tables for FOB-supplied assist, logistic assist, revive assist and section (tables 2 to 6); heal player (tables 7 to 9); repair vehicle (table 10); revive player (tables 11 to 13); buildable destroyed (table 14); spotting added and removed (tables 15 and 16).
- **Parallel tables:** the assist and section tables reuse the vehicle keys from table 2 with a different tag prefix. The file does not say which in-game action selects which table.
- **Shared keys:** some keys appear in more than one family. Examples: `Id.Buildable.FOB` (tables 14 and 15), `ID.Item.VehicleSupplyCrate.*` (tables 1, 15 and 16) and `Id.Item.MedKit.Standard` (tables 7 to 9 and 11 to 13). The file does not say how a key with more than one tag is resolved.
- **Rewards:** tags are names only. Amounts, currency and the step from tag to value are not in this file. The header names [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json) as the calculator that consumes these lookups; that table is not included here, so the full combination is not verified.

---

## 19. Still not pulled / limitations

- **Formula variables:** literal values (`KillStreakValue`, `ControlZoneFactor`, `HotZoneFactor` and most others) are defined inside each row. Runtime game values (`LastVictimCount`, `KillStreak`, `CrewCount`, the event's base reward from the cash tables) and the `LiveCurves` scaling curves are not; the Value column takes a plain first kill with no repeat victim, a crew of one and a finished build, and shows rows that scale with a runtime amount as ×N.
- **Shared definitions table:** [`DT_Challenges_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_Challenges_SessionEvents_Shared.json) has 10 rows in this build.
- **Row fields:** the exported rows carry only the fields shown in each table (`Resources` and `Tag` for the reward tables; `RewardTag` and `Tag` for the lookup tables). No other fields exist in the export.
- **Event triggers:** the file does not say which in-game action selects the destroy-vehicle, section or assist tables, or which heal and revive table applies to a given use.
- **Spelling as exported:** `Defibrilator`, `Medkit` (vs [`MedKit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MedKit/Content/MedKit.json)), the `Id.` vs `ID.` prefixes, and `HotzoneMagnet` (key) vs [`HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/HotZoneMagnet.json) (tag) are kept as exported and not corrected.
- **Single extraction:** all tables come from one extraction. No comparison across builds has been made.
