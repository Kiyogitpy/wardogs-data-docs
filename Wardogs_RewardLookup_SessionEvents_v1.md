---
title: "Session-Event Reward Lookups"
parent: "Content"
---

# Wardogs — Session-Event Reward Lookups Reference (v1)
*Extracted live via CUE4Parse (.NET) directly from the game's encrypted Paks, from the game's own asset files. These are the lookup layer feeding the per-kill/per-event reward calculator whose formulas are in section 17 (`DT_ChallengeRewards_SessionEvents_*`).*

> **Scope:** **16 tables pulled**, covering KOTH challenge events ([`Challenges_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/Challenges_KOTH.json)), buildable destruction ([`Rewards/BuildableRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards)) and Spotting ([`Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Spotting.json)). Each table maps a row key (a vehicle variant, item or buildable ID) to a `Challenges.Rewards.*` reward tag. Reward amounts and the calculator that consumes these tags are outside this file.

---

## 1. [`DT_RewardLookup_SessionEvent_DestroySupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroySupplyCrate.json)

Maps supply-crate item IDs to reward tags for the destroy-supply-crate event.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroySupplyCrate.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 10

| Row key | RewardTag | Tag |
|---|---|---|
| `ID.Item.VehicleSupplyCrate.Free` | Challenges.Rewards.DestroySupplyCrate.Free | ID.Item.VehicleSupplyCrate.Free |
| `ID.Item.VehicleSupplyCrate.Container.Free` | Challenges.Rewards.DestroySupplyCrate.Free | ID.Item.VehicleSupplyCrate.Container.Free |
| `ID.Item.VehicleSupplyCrate.Small` | Challenges.Rewards.DestroySupplyCrate.Small | ID.Item.VehicleSupplyCrate.Small |
| `ID.Item.VehicleSupplyCrate.Small.Armoured` | Challenges.Rewards.DestroySupplyCrate.Small.Armoured | ID.Item.VehicleSupplyCrate.Small.Armoured |
| `ID.Item.VehicleSupplyCrate.Large` | Challenges.Rewards.DestroySupplyCrate.Large | ID.Item.VehicleSupplyCrate.Large |
| `ID.Item.VehicleSupplyCrate.Large.Armoured` | Challenges.Rewards.DestroySupplyCrate.Large.Armoured | ID.Item.VehicleSupplyCrate.Large.Armoured |
| `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet | ID.Item.VehicleSupplyCrate.Pallet.BuildSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet | ID.Item.VehicleSupplyCrate.Pallet.FuelSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet | ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` | Challenges.Rewards.DestroySupplyCrate.Pallet | ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply |

**Notes:**
- Two rows share `DestroySupplyCrate.Free` (`ID.Item.VehicleSupplyCrate.Free` and `.Container.Free`). The four `Pallet.*` rows share `DestroySupplyCrate.Pallet`.
- Armoured crates (`Small.Armoured`, `Large.Armoured`) have their own tags, separate from the unarmoured tiers.
- Keys use the `ID.Item.` prefix, as in the repair-tool table.

---

## 2. [`DT_RewardLookup_SessionEvent_DestroyVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicle.json)

Maps vehicle variant keys to `VehicleDestroyed` reward tags, grouped by vehicle family.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicle.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 30

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.VehicleDestroyed.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Stationary.Loudspeaker` | Challenges.Rewards.VehicleDestroyed.Loudspeaker | Vehicle.Variant.Stationary.Loudspeaker |
| `Vehicle.Variant.Stationary.MistralAA` | Challenges.Rewards.VehicleDestroyed.MistralAA | Vehicle.Variant.Stationary.MistralAA |
| `Vehicle.Variant.Stationary.Mortar` | Challenges.Rewards.VehicleDestroyed.Mortar | Vehicle.Variant.Stationary.Mortar |
| `Vehicle.Variant.Stationary.Phalanx` | Challenges.Rewards.VehicleDestroyed.Phalanx | Vehicle.Variant.Stationary.Phalanx |
| `Vehicle.Variant.Stationary.STN_05` | Challenges.Rewards.VehicleDestroyed.Mortar | Vehicle.Variant.Stationary.STN_05 |

**Notes:**
- Variants of one vehicle share a tag. For example, the three Kodiak rows all map to `VehicleDestroyed.Kodiak`. TNK_01 is the exception: its Heavy, AntiAir and Artillery variants each have a separate tag.
- `Vehicle.Variant.Stationary.STN_05` maps to `VehicleDestroyed.Mortar`, the same tag as `Stationary.Mortar`.

---

## 3. [`DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist.json)

Vehicle keys from table 2, mapped to the FOB-supplied assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 24

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |

**Notes:**
- 24 rows. It omits the five `Vehicle.Variant.Stationary.*` keys and `Vehicle.Variant.Land.Wheeled.Humvee.Minigun`, which table 2 (30 rows) includes.
- Tags use `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.<Family>`, with the same family grouping as table 2.

---

## 4. [`DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist.json)

Vehicle keys from table 2, mapped to the logistic-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 24

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |

**Notes:**
- Key set matches table 3 (24 keys). Only the tag prefix differs.

---

## 5. [`DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist.json)

Vehicle keys from table 2, mapped to the revive-assist tag prefix.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 24

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |

**Notes:**
- Key set matches tables 3 and 4 (24 keys). Only the tag prefix differs.

---

## 6. [`DT_RewardLookup_SessionEvent_DestroyVehicleSection`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleSection.json)

Vehicle keys from table 2, mapped to `DestroyVehicleSection` reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleSection.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 24

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.DestroyVehicleSection.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.DestroyVehicleSection.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.DestroyVehicleSection.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.DestroyVehicleSection.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.DestroyVehicleSection.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.DestroyVehicleSection.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.DestroyVehicleSection.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.DestroyVehicleSection.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.DestroyVehicleSection.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.DestroyVehicleSection.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.DestroyVehicleSection.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.DestroyVehicleSection.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.DestroyVehicleSection.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.DestroyVehicleSection.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.DestroyVehicleSection.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.DestroyVehicleSection.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.DestroyVehicleSection.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.DestroyVehicleSection.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.DestroyVehicleSection.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.DestroyVehicleSection.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.DestroyVehicleSection.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.DestroyVehicleSection.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.DestroyVehicleSection.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.DestroyVehicleSection.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |

**Notes:**
- Key set matches tables 3 to 5 (24 keys). The tag prefix is `Challenges.Rewards.DestroyVehicleSection.`, not `VehicleDestroyed`.

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
- **Row count:** 34

| Row key | RewardTag | Tag |
|---|---|---|
| `Id.Buildable.AirRaidShelter` | Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter | Id.Buildable.AirRaidShelter |
| `Id.Buildable.AirRaidShelter.Ceiling` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.AirRaidShelter.Ceiling |
| `Id.Buildable.AirRaidShelter.Floor` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.AirRaidShelter.Floor |
| `Id.Buildable.BarbedWire` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.BarbedWire |
| `Id.Buildable.BremmerWall` | Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall | Id.Buildable.BremmerWall |
| `Id.Buildable.Bunker` | Challenges.Rewards.Buildables.BuildableDestroyed.Bunker | Id.Buildable.Bunker |
| `Id.Buildable.Bunker.Floor` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.Bunker.Floor |
| `Id.Buildable.Bunker.Roof` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.Bunker.Roof |
| `Id.Buildable.CamoNetTent` | Challenges.Rewards.Buildables.BuildableDestroyed.CamoNetTent | Id.Buildable.CamoNetTent |
| `Id.Buildable.CrowsNest` | Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest | Id.Buildable.CrowsNest |
| `Id.Buildable.CrowsNest.BaseFloor` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.CrowsNest.BaseFloor |
| `Id.Buildable.CrowsNest.FirstFloor` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.CrowsNest.FirstFloor |
| `Id.Buildable.CrowsNest.Roof` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.CrowsNest.Roof |
| `Id.Buildable.Door` | Challenges.Rewards.Buildables.BuildableDestroyed.Gate | Id.Buildable.Door |
| `Id.Buildable.Door.TopSegment` | Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire | Id.Buildable.Door.TopSegment |
| `Id.Buildable.FloorBoard` | Challenges.Rewards.Buildables.BuildableDestroyed.FloorBoard | Id.Buildable.FloorBoard |
| `Id.Buildable.FOB` | Challenges.Rewards.Buildables.BuildableDestroyed.FOB | Id.Buildable.FOB |
| `Id.Buildable.Gate` | Challenges.Rewards.Buildables.BuildableDestroyed.Gate | Id.Buildable.Gate |
| `Id.Buildable.Gate.Ramp` | Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall | Id.Buildable.Gate.Ramp |
| `Id.Buildable.HBlock` | Challenges.Rewards.Buildables.BuildableDestroyed.HBlock | Id.Buildable.HBlock |
| `Id.Buildable.HBlockQuadWall` | Challenges.Rewards.Buildables.BuildableDestroyed.HBlockQuadWall | Id.Buildable.HBlockQuadWall |
| `Id.Buildable.HotzoneMagnet` | Challenges.Rewards.Buildables.BuildableDestroyed.HotZoneMagnet | Id.Buildable.HotzoneMagnet |
| `Id.Buildable.Loudspeaker` | Challenges.Rewards.Buildables.BuildableDestroyed.Loudspeaker | Id.Buildable.Loudspeaker |
| `Id.Buildable.MistralAA` | Challenges.Rewards.Buildables.BuildableDestroyed.MistralAA | Id.Buildable.MistralAA |
| `Id.Buildable.Mortar` | Challenges.Rewards.Buildables.BuildableDestroyed.Mortar | Id.Buildable.Mortar |
| `Id.Buildable.Phalanx` | Challenges.Rewards.Buildables.BuildableDestroyed.Phalanx | Id.Buildable.Phalanx |
| `Id.Buildable.Radio` | Challenges.Rewards.Buildables.BuildableDestroyed.Radio | Id.Buildable.Radio |
| `Id.Buildable.Ramp` | Challenges.Rewards.Buildables.BuildableDestroyed.Ramp | Id.Buildable.Ramp |
| `Id.Buildable.RefuelStation` | Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation | Id.Buildable.RefuelStation |
| `Id.Buildable.RepairStation` | Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation | Id.Buildable.RepairStation |
| `Id.Buildable.SandbagWall` | Challenges.Rewards.Buildables.BuildableDestroyed.SandbagWall | Id.Buildable.SandbagWall |
| `Id.Buildable.TallHBlock` | Challenges.Rewards.Buildables.BuildableDestroyed.TallHBlock | Id.Buildable.TallHBlock |
| `Id.Buildable.TankTrap` | Challenges.Rewards.Buildables.BuildableDestroyed.TankTrap | Id.Buildable.TankTrap |
| `Id.Buildable.WindowBoard` | Challenges.Rewards.Buildables.BuildableDestroyed.WindowBoard | Id.Buildable.WindowBoard |

**Notes:**
- Eight sub-part keys map to `BuildableDestroyed.BarbedWire`: `AirRaidShelter.Ceiling`, `AirRaidShelter.Floor`, `Bunker.Floor`, `Bunker.Roof`, `CrowsNest.BaseFloor`, `CrowsNest.FirstFloor`, `CrowsNest.Roof` and `Door.TopSegment`. The base `Id.Buildable.BarbedWire` key uses the same tag.
- `Id.Buildable.Gate.Ramp` maps to `BremmerWall`.
- `Id.Buildable.Door` and `Id.Buildable.Gate` both map to `Gate`.
- `RefuelStation` and `RepairStation` share `BuildableDestroyed.RepairStation`.
- This table sits in the BuildableRewards bundle, not in [`Challenges_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/Challenges_KOTH.json).

---

## 15. [`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json)

Maps spotted vehicles, stationary weapons, mines, supply crates and some buildables to `Spotting.Added` reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 47

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.Spotting.Added.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.Spotting.Added.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.Spotting.Added.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.Spotting.Added.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.Spotting.Added.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.Spotting.Added.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.Spotting.Added.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.Spotting.Added.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.Spotting.Added.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.Spotting.Added.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.Spotting.Added.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.Spotting.Added.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.Spotting.Added.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.Spotting.Added.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.Spotting.Added.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.Spotting.Added.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.Spotting.Added.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.Spotting.Added.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.Spotting.Added.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.Spotting.Added.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.Spotting.Added.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.Spotting.Added.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.Spotting.Added.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.Spotting.Added.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.Spotting.Added.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Id.Item.Claymore` | Challenges.Rewards.Spotting.Added.Claymore | Id.Item.Claymore |
| `ID.Item.ATMine` | Challenges.Rewards.Spotting.Added.ATMine | ID.Item.ATMine |
| `Id.Buildable.FOB` | Challenges.Rewards.Spotting.Added.FOB | Id.Buildable.FOB |
| `Id.Buildable.HotzoneMagnet` | Challenges.Rewards.Spotting.Added.BuildableHotZoneMagnet | Id.Buildable.HotzoneMagnet |
| `ID.Item.VehicleSupplyCrate.Free` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Free |
| `ID.Item.VehicleSupplyCrate.Container.Free` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Container.Free |
| `ID.Item.VehicleSupplyCrate.Small` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Small |
| `ID.Item.VehicleSupplyCrate.Small.Armoured` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Small.Armoured |
| `ID.Item.VehicleSupplyCrate.Large` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Large |
| `ID.Item.VehicleSupplyCrate.Large.Armoured` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Large.Armoured |
| `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.BuildSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.FuelSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` | Challenges.Rewards.Spotting.Added.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply |
| `Vehicle.Variant.Stationary.MistralAA` | Challenges.Rewards.Spotting.Added.MistralAA | Vehicle.Variant.Stationary.MistralAA |
| `Vehicle.Variant.Stationary.Mortar` | Challenges.Rewards.Spotting.Added.Mortar | Vehicle.Variant.Stationary.Mortar |
| `Vehicle.Variant.Stationary.Phalanx` | Challenges.Rewards.Spotting.Added.Phalanx | Vehicle.Variant.Stationary.Phalanx |
| `Vehicle.Variant.Stationary.Loudspeaker` | Challenges.Rewards.Spotting.Added.MistralAA | Vehicle.Variant.Stationary.Loudspeaker |
| `Id.Buildable.Radio` | Challenges.Rewards.Spotting.Added.MistralAA | Id.Buildable.Radio |
| `Id.Buildable.RepairStation` | Challenges.Rewards.Spotting.Added.MistralAA | Id.Buildable.RepairStation |
| `Id.Buildable.RefuelStation` | Challenges.Rewards.Spotting.Added.MistralAA | Id.Buildable.RefuelStation |
| `Vehicle.Variant.Stationary.STN_05` | Challenges.Rewards.Spotting.Added.Mortar | Vehicle.Variant.Stationary.STN_05 |

**Notes:**
- 30 vehicle keys: the 25 non-stationary keys of table 2, plus the five stationary keys.
- `Stationary.Loudspeaker`, `Id.Buildable.Radio`, `Id.Buildable.RepairStation` and `Id.Buildable.RefuelStation` map to `Spotting.Added.MistralAA`, not their own tags. `Stationary.STN_05` maps to `Spotting.Added.Mortar`.
- All ten `VehicleSupplyCrate` keys map to `Spotting.Added.SupplyCrate`.
- Key prefixes are mixed (`Id.` and `ID.`) within this table, as exported.

---

## 16. [`DT_RewardLookup_SessionEvent_Spotting_Removed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Removed.json)

Same key set as table 15, mapped to `Spotting.Removed` reward tags.

- **Package:** `Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Removed.uasset`
- **Row struct:** `Class'WDVariantRewardLookupRow'`
- **Row count:** 47

| Row key | RewardTag | Tag |
|---|---|---|
| `Vehicle.Variant.Land.Wheeled.Kodiak.Default` | Challenges.Rewards.Spotting.Removed.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Default |
| `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` | Challenges.Rewards.Spotting.Removed.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` | Challenges.Rewards.Spotting.Removed.Kodiak | Vehicle.Variant.Land.Wheeled.Kodiak.Pickup |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | Challenges.Rewards.Spotting.Removed.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | Challenges.Rewards.Spotting.Removed.Huey | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | Challenges.Rewards.Spotting.Removed.Huey | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | Challenges.Rewards.Spotting.Removed.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | Challenges.Rewards.Spotting.Removed.Blackhawk | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | Challenges.Rewards.Spotting.Removed.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | Challenges.Rewards.Spotting.Removed.LittleBird | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | Challenges.Rewards.Spotting.Removed.Havoc | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` | Challenges.Rewards.Spotting.Removed.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` | Challenges.Rewards.Spotting.Removed.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore |
| `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` | Challenges.Rewards.Spotting.Removed.SpawnVehicle | Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra |
| `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` | Challenges.Rewards.Spotting.Removed.TNK_01.Heavy | Vehicle.Variant.Land.Tracked.TNK_01.Heavy |
| `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` | Challenges.Rewards.Spotting.Removed.TNK_01.Artillery | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |
| `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` | Challenges.Rewards.Spotting.Removed.TNK_01.AntiAir | Vehicle.Variant.Land.Tracked.TNK_01.AntiAir |
| `Vehicle.Variant.Land.Wheeled.Bobcat.Default` | Challenges.Rewards.Spotting.Removed.Bobcat | Vehicle.Variant.Land.Wheeled.Bobcat.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | Challenges.Rewards.Spotting.Removed.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | Challenges.Rewards.Spotting.Removed.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | Challenges.Rewards.Spotting.Removed.Humvee | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` | Challenges.Rewards.Spotting.Removed.DuneBuggy | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |
| `Vehicle.Variant.Land.Wheeled.Ural.Battle` | Challenges.Rewards.Spotting.Removed.Ural | Vehicle.Variant.Land.Wheeled.Ural.Battle |
| `Vehicle.Variant.Land.Wheeled.Ural.Attack` | Challenges.Rewards.Spotting.Removed.Ural | Vehicle.Variant.Land.Wheeled.Ural.Attack |
| `Vehicle.Variant.Land.Wheeled.Ural.Default` | Challenges.Rewards.Spotting.Removed.Ural | Vehicle.Variant.Land.Wheeled.Ural.Default |
| `Id.Item.Claymore` | Challenges.Rewards.Spotting.Removed.Claymore | Id.Item.Claymore |
| `ID.Item.ATMine` | Challenges.Rewards.Spotting.Removed.ATMine | ID.Item.ATMine |
| `Id.Buildable.FOB` | Challenges.Rewards.Spotting.Removed.FOB | Id.Buildable.FOB |
| `Id.Buildable.HotzoneMagnet` | Challenges.Rewards.Spotting.Removed.BuildableHotZoneMagnet | Id.Buildable.HotzoneMagnet |
| `ID.Item.VehicleSupplyCrate.Free` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Free |
| `ID.Item.VehicleSupplyCrate.Container.Free` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Container.Free |
| `ID.Item.VehicleSupplyCrate.Small` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Small |
| `ID.Item.VehicleSupplyCrate.Small.Armoured` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Small.Armoured |
| `ID.Item.VehicleSupplyCrate.Large` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Large |
| `ID.Item.VehicleSupplyCrate.Large.Armoured` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Large.Armoured |
| `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.BuildSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.FuelSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply |
| `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` | Challenges.Rewards.Spotting.Removed.SupplyCrate | ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply |
| `Vehicle.Variant.Stationary.MistralAA` | Challenges.Rewards.Spotting.Removed.MistralAA | Vehicle.Variant.Stationary.MistralAA |
| `Vehicle.Variant.Stationary.Mortar` | Challenges.Rewards.Spotting.Removed.Mortar | Vehicle.Variant.Stationary.Mortar |
| `Vehicle.Variant.Stationary.Phalanx` | Challenges.Rewards.Spotting.Removed.Phalanx | Vehicle.Variant.Stationary.Phalanx |
| `Vehicle.Variant.Stationary.Loudspeaker` | Challenges.Rewards.Spotting.Removed.MistralAA | Vehicle.Variant.Stationary.Loudspeaker |
| `Id.Buildable.Radio` | Challenges.Rewards.Spotting.Removed.MistralAA | Id.Buildable.Radio |
| `Id.Buildable.RepairStation` | Challenges.Rewards.Spotting.Removed.MistralAA | Id.Buildable.RepairStation |
| `Id.Buildable.RefuelStation` | Challenges.Rewards.Spotting.Removed.MistralAA | Id.Buildable.RefuelStation |
| `Vehicle.Variant.Stationary.STN_05` | Challenges.Rewards.Spotting.Removed.Mortar | Vehicle.Variant.Stationary.STN_05 |

**Notes:**
- Same 47 keys and grouping as table 15. Only the prefix changes, from `Spotting.Added.` to `Spotting.Removed.`.

---

## 17. Reward formulas (`DT_ChallengeRewards_SessionEvents_*`)

Each row gives the currency tag and a formula for the reward. Most formula variables are literals inside the row itself (each resource's `Selectors` and `Variables`); the rest are runtime game values such as the event's base reward or kill streak. The **Value** column is each row evaluated as written, for the state picked with the **Zone multiplier** switch in the sidebar (you and the target both in a control zone, or both in a hot zone; `_tools/zone_rewards.py`). A value written as ×N is N times a runtime amount: hover it to see which.

### 17a. [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json) (161 rows)
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
| `Challenges.Rewards.PlayerKill.FOBSuppliedAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedModifier` |
| `Challenges.Rewards.PlayerKill.FOBSuppliedAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
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
| `Challenges.Rewards.PlayerKill.Assist.FOBSuppliedAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedModifier` |
| `Challenges.Rewards.PlayerKill.Assist.FOBSuppliedAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PlayerKill.Assist.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.PlayerKill.Assist.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Huey` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Havoc` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * FactionScoreScalar * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + ((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `((BaseReward + (clamp(KillStreak - 1, 0, KillStreakMax) * KillStreakValue)) * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Bobcat` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Humvee` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Ural` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward) * AlignmentModifier` |
| `Challenges.Rewards.VehicleDestroyed.Loudspeaker` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Loudspeaker` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.MistralAA` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.MistralAA` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.Mortar` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Mortar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.Phalanx` | `Attribute.Meta.Currency.Cash` | `(BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar * CrewScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar * CrewScalar) * pow(CrewPenaltyModifier, clamp(CrewCount - 1, 0, CrewCountMax))` |
| `Challenges.Rewards.VehicleDestroyed.Phalanx` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.CrewAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * CrewModifier` |
| `Challenges.Rewards.VehicleDestroyed.CrewAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Littlebird` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Littlebird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * LogisticAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.LogisticAssist.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * ReviveAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.ReviveAssist.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * FOBSuppliedAssistModifier` |
| `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.VehicleDestroyed.SupplyCrateAssist` | `Attribute.Meta.Currency.Cash` | `BaseReward * SupplyCrateModifier` |
| `Challenges.Rewards.VehicleDestroyed.SupplyCrateAssist` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Kodiak` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.LittleBird` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Huey` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Huey` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Blackhawk` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Havoc` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Havoc` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Bobcat` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Bobcat` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.DuneBuggy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Humvee` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
| `Challenges.Rewards.DestroyVehicleSection.Ural` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * AssistCurve * AssistScalar) + (BaseReward * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * AssistCurve * AssistScalar))` |
| `Challenges.Rewards.DestroyVehicleSection.Ural` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * AlignmentModifier)` |
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
| `Challenges.Rewards.DeploySupplyCrate` | `Attribute.Meta.Currency.Cash` | `BaseReward * TargetZoneModifier` |
| `Challenges.Rewards.DeploySupplyCrate` | `Attribute.Meta.XP.Role` | `(BaseReward * TargetZoneModifier)` |
| `Challenges.Rewards.SupplyPalletDropped` | `Attribute.Meta.Currency.Cash` | `BaseReward * TargetZoneModifier` |
| `Challenges.Rewards.SupplyPalletDropped` | `Attribute.Meta.XP.Role` | `(BaseReward * TargetZoneModifier)` |
| `Challenges.Rewards.RepairVehicle.Wrench.Standard` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier * OwnerModifier)` |
| `Challenges.Rewards.RepairVehicle.Wrench.Standard` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Light` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier * OwnerModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Light` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Heavy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseRewardValue * ZoneModifier * HostilityModifier * OwnerModifier)` |
| `Challenges.Rewards.RepairVehicle.Drill.Heavy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * ((BaseReward) * HostilityModifier)` |
| `Challenges.Rewards.PurchaseFromSupplyCrate` | `Attribute.Meta.Currency.Cash` | `PurchaseValue * MarkupMultiplier` |
| `Challenges.Rewards.PurchaseFromSupplyCrate` | `Attribute.Meta.XP.Role` | `PurchaseValue` |
| `Challenges.Rewards.DestroySupplyCrate.Free` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Free` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Small` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Small` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Small.Armoured` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Small.Armoured` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Large` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Large` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Large.Armoured` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Large.Armoured` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier ` |
| `Challenges.Rewards.DestroySupplyCrate.Pallet` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.SupplyCrateDestroyed` | `Attribute.Meta.Currency.Cash` | `BaseReward` |
| `Challenges.Rewards.PlayerDelivered` | `Attribute.Meta.Currency.Cash` | `(BaseReward * ZoneModifier) * (PlayerCount)` |
| `Challenges.Rewards.PlayerDelivered` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.PassengerSurvived` | `Attribute.Meta.Currency.Cash` | `BaseReward * ZoneModifier` |
| `Challenges.Rewards.PassengerSurvived` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.SafeZoneEntered` | `Attribute.Meta.Currency.Cash` | `BaseReward * max(PlayersSurvivedMin, PlayersSurvivedCount)` |
| `Challenges.Rewards.SafeZoneEntered` | `Attribute.Meta.XP.Role` | `(BaseReward * max(PlayersSurvivedMin, PlayersSurvivedCount))` |
| `Challenges.Rewards.SendTip` | `Attribute.Meta.Currency.Cash` | `0 - BaseReward` |
| `Challenges.Rewards.SendPreTip` | `Attribute.Meta.Currency.Cash` | `(BaseReward) * PreTipValue` |
| `Challenges.Rewards.ReceiveTip` | `Attribute.Meta.Currency.Cash` | `BaseReward` |
| `Challenges.Rewards.ReceivePreTip` | `Attribute.Meta.Currency.Cash` | `(BaseReward) * PreTipValue` |
| `Challenges.Rewards.VehicleAirborne` | `Attribute.Meta.Currency.Cash` | `BaseReward * ElapsedAirTime` |
| `Challenges.Rewards.VehicleFlyThrough` | `Attribute.Meta.Currency.Cash` | `BaseReward * RepeatActionCount` |
| `Challenges.Rewards.Test` | `Attribute.Meta.Currency.Cash` | `BaseRewardModifier` |

### 17b. [`DT_ChallengeRewards_SessionEvents_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json) (29 rows)
- **Package:** `Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.uasset`

| Row | Resource | Formula |
|---|---|---|
| `Challenges.Rewards.Buildables.BuildableDamaged` | `Attribute.Meta.Currency.Cash` | `BaseValue * AlignmentModifier` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FOB` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FOB` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.AirRaidShelter` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BarbedWire` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.BremmerWall` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Bunker` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CamoNetTent` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CamoNetTent` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.CrowsNest` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FloorBoard` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.FloorBoard` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Gate` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Gate` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlock` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlock` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlockQuadWall` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HBlockQuadWall` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HotZoneMagnet` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.HotZoneMagnet` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Radio` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Radio` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Ramp` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.Ramp` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.RepairStation` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TallHBlock` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TallHBlock` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.SandbagWall` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.SandbagWall` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TankTrap` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.TankTrap` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.WindowBoard` | `Attribute.Meta.Currency.Cash` | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)` |
| `Challenges.Rewards.Buildables.BuildableDestroyed.WindowBoard` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
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

### 17c. [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) (44 rows)
- **Package:** `Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.uasset`

| Row | Resource | Formula |
|---|---|---|
| `Challenges.Rewards.Spotting.Added.Player` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Player` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Bobcat` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Bobcat` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Kodiak` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Kodiak` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.LittleBird` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.LittleBird` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Huey` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Huey` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Blackhawk` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Havoc` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Havoc` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Humvee` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Humvee` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.DuneBuggy` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Ural` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Ural` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Claymore` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Claymore` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.ATMine` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.ATMine` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.BuildableHotZoneMagnet` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.BuildableHotZoneMagnet` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.FOB` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.FOB` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.SupplyCrate` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.MistralAA` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.MistralAA` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Phalanx` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Phalanx` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Added.Mortar` | `Attribute.Meta.Currency.Cash` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| `Challenges.Rewards.Spotting.Added.Mortar` | `Attribute.Meta.XP.Role` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Player` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Player` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Bobcat` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Bobcat` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Kodiak` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Kodiak` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.LittleBird` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.LittleBird` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Huey` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Huey` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Blackhawk` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Havoc` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Havoc` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SpawnVehicle` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Heavy` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Heavy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Artillery` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.Artillery` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.AntiAir` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.TNK_01.AntiAir` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Humvee` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Humvee` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.DuneBuggy` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.DuneBuggy` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Ural` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Ural` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Claymore` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Claymore` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.ATMine` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.ATMine` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.BuildableHotZoneMagnet` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.BuildableHotZoneMagnet` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.FOB` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.FOB` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.SupplyCrate` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.MistralAA` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.MistralAA` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Mortar` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Mortar` | `Attribute.Meta.XP.Role` | `(BaseReward)` |
| `Challenges.Rewards.Spotting.Removed.Phalanx` | `Attribute.Meta.Currency.Cash` | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| `Challenges.Rewards.Spotting.Removed.Phalanx` | `Attribute.Meta.XP.Role` | `(BaseReward)` |

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
- **Shared definitions table:** [`DT_Challenges_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_Challenges_SessionEvents_Shared.json) has 0 rows in this build.
- **Row fields:** the exported rows carry only the fields shown in each table (`Resources` and `Tag` for the reward tables; `RewardTag` and `Tag` for the lookup tables). No other fields exist in the export.
- **Event triggers:** the file does not say which in-game action selects the destroy-vehicle, section or assist tables, or which heal and revive table applies to a given use.
- **Spelling as exported:** `Defibrilator`, `Medkit` (vs [`MedKit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MedKit/Content/MedKit.json)), the `Id.` vs `ID.` prefixes, and `HotzoneMagnet` (key) vs [`HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/HotZoneMagnet.json) (tag) are kept as exported and not corrected.
- **Single extraction:** all tables come from one extraction. No comparison across builds has been made.
