---
title: "Spotting (feature)"
redirect_from: ["/Wardogs_GameFeatures_Spotting_v2.html", "/Wardogs_GameFeatures_Spotting_v2"]
parent: "Game Modes & Maps"
description: "What 'Spotting' Covers, Package Contents, Challenge Calculator, Match-Score Payouts"
---

# Wardogs — GameFeature: Spotting Reference
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). Source: [`Wardogs/Plugins/GameFeatures/Spotting/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Spotting) (28 JSON files).*

> **Overlap with the main doc:** the flat Spotting cash min and max values (15 / 275 and 50 / 500) are in `Wardogs_Rewards_and_Progression_v2.md`, section 9. This doc adds the **per-target challenge formulas**, the **modifier table** behind those min and max values, the **variant lookups**, **skills**, **feed strings**, **trackers**, **input bindings** and **audio** for spotting.

---

## Season 02 update (2026-10-15)

- **Challenge calculator:** 44 rows become 130 (22 Added and 22 Removed become 65 and 65). The new rows are variant-level entries, the new vehicles [`TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/TNK_04.json) and [`WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/WHL_08.json), and the stationary and buildable entries `Loudspeaker`, `MGNest`, [`STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/STN_05.json), `BuildableRadio`, `BuildableRepairStation` and `BuildableRefuelStation`.
- **New `BuildProgress` factor:** `BuildProgress` is a new factor in 10 buildable and stationary rows of each of the Added and Removed sets (20 rows). Four of those (`BuildableHotZoneMagnet`, `MistralAA`, `Mortar`, `Phalanx`) are existing rows that gained it, and six are new rows (section 3a). No other formula changed.
- **Lookup tables:** 47 rows become 51 in both lookups. Every reward tag is now specific to one variant, and `MistralAA`, `Mortar` and [`STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/STN_05.json) no longer share a tag (section 5).
- **Values, old -> new (Added):** TNK_01.Heavy XP 75 -> 60. TNK_01.Artillery cash 1500 -> 400 and XP 75 -> 60. MistralAA cash 200 -> 75 and XP 50 -> 20. Mortar cash 100 -> 75 and XP 50 -> 20.
- **Values, old -> new (Removed):** TNK_01.Heavy cash 5000 -> 3300 and XP 375 -> 200. TNK_01.Artillery cash 8000 -> 1200. Phalanx cash 1500 -> 725 and XP 125 -> 100.
- **KOTH challenge definitions:** [`DT_Challenges_SessionEvents_KOTH_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_Spotting.json) goes from 0 rows to 2 (`Challenges.SessionEvents.Spotting.Added` and `.Removed`).
- **Trackers:** the map and spatial trackers gain per-vehicle overrides for [`WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/WHL_08.json) (reward tag `VehicleDestroyed.WHL_08`) and [`TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/TNK_04.json) (reward tag `VehicleDestroyed.TNK_04.Default`). The material tracker gains icon entries for both.
- **Input:** [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json) adds reload bindings on `R` and gamepad face button left ([`IA_Weapon_Reload`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IA_Weapon_Reload.json)).
- **Unchanged:** state tree states (22 and 21), skills, feed strings, audio, and the match-score cash min and max values.

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

---

## 1. What "Spotting" Covers

Spotting lets a player mark an enemy target so that it shows on the map and in the world. Each spot is a **challenge event**. Two events exist:

| Event | Feed text | Meaning (inferred from names) |
|---|---|---|
| **Added** (`Challenges.Rewards.Spotting.Added.*`) | "Target Spotted" | A target becomes spotted. |
| **Removed** (`Challenges.Rewards.Spotting.Removed.*`) | "Spotted Target Destroyed" | A spotted target is removed from the spotted list, usually because it was destroyed. |

Both events pay out, and both are split by target type (player, vehicle, buildable, supply crate, stationary weapon). Assist and owner credit come from separate match-score tags (section 4).

---

## 2. Package Contents

| Group | Files | Contents |
|---|---|---|
| Root bundle | 1 | [`Spotting.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Spotting.json) (`GameFeatureData`): data registry and sources, a gameplay cue path, components, and a widget element. |
| Challenge rewards | 2 | [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) (130 rows, the calculator). [`DT_Challenges_SessionEvents_KOTH_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_Spotting.json) (2 rows, challenge definitions). |
| Variant lookups | 2 | [`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json) (51 rows), `..._Removed` (51 rows). |
| State trees | 2 | [`ST_Challenges_SessionEvents_KOTH_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/ST_Challenges_SessionEvents_KOTH_Spotting_Added.json) (22 states), `..._Removed` (21 states). Each has a `WDChallengeStateTreeSchema`. |
| Match-score rewards | 2 | [`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json) (4 rows, live min and max values). [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json) (3 rows, all zero). |
| Skills | 1 | [`DT_Skills_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Skills/DT_Skills_Spotting.json) (2 rows, Recon skills). |
| Feed | 2 | [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json) (3), [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json) (3). |
| Trackers and HUD | 8 | Map and spatial trackers (`DA_` and `DT_`), material tracker, overlay, and the dynamic offset curve. |
| Input | 2 | [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json), [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json). |
| Audio | 6 | [`AE_Comms_Spotted`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted.json), [`AE_Comms_Spotted_VehicleEmpty`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted_VehicleEmpty.json), [`AE_UX_Spotted_Target`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotted_Target.json), [`AE_UX_Spotting_Start`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Start.json), `_Stop`, `_Complete`. |

---

## 3. Challenge Calculator ([`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json), 130 rows)

There are **65 Added rows and 65 Removed rows**. The original 22 target types keep one row per event. The rest are variant-level rows (for example `Bobcat.Default` and `Kodiak.MachineGun`), the new vehicles [`TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/TNK_04.json) and [`WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/WHL_08.json), and the stationary and buildable entries listed below. Each row has a cash resource and an XP resource.

Target types (the original 22 names, on both events): `Player`, `Bobcat`, `Kodiak`, `LittleBird`, `Huey`, `Blackhawk`, `Havoc`, `SpawnVehicle`, `TNK_01.Heavy`, `TNK_01.Artillery`, `TNK_01.AntiAir`, `Humvee`, `DuneBuggy`, `Ural`, [`Claymore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Claymore/Content/Claymore.json), `ATMine`, `BuildableHotZoneMagnet`, `FOB`, `SupplyCrate`, `MistralAA`, `Phalanx`, `Mortar`. New row names in this update: `TNK_04`, `WHL_08`, `Loudspeaker`, `MGNest`, `STN_05`, `BuildableRadio`, `BuildableRepairStation`, `BuildableRefuelStation`, plus variant rows for the vehicles, spawn vehicles and supply crates.

### 3a. Formulas

| Event | Resource | Expression |
|---|---|---|
| Added (55 rows) | Cash | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| Added (10 rows, see note) | Cash | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier * BuildProgress)` |
| Added (55 rows) | XP | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| Added (10 rows, see note) | XP | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * BuildProgress)` |
| Removed (55 rows) | Cash | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| Removed (10 rows, see note) | Cash | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier * BuildProgress` |
| Removed (55 rows) | XP | `(BaseReward)` |
| Removed (10 rows, see note) | XP | `(BaseReward) * BuildProgress` |

Note the difference. **Added** pays down by how many times the target was already spotted (the "last victim" count). **Removed** has no victim reduction, but adds `DestroyedByTeamModifier`.

The 10 rows marked "see note" are the buildable and stationary entries: `BuildableHotZoneMagnet`, `BuildableRadio`, `BuildableRefuelStation`, `BuildableRepairStation`, `Loudspeaker`, `MistralAA`, `Mortar`, `Phalanx`, `MGNest` and [`STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/STN_05.json). They multiply by `BuildProgress`, a variable whose source is not in this folder.

### 3b. Selectors

| Variable | Default | Options (condition → variable) | Rows |
|---|---|---|---|
| `BaseReward` | `DefaultReward` | `ALL(Challenges.Rewards.Spotting.Refreshed)` → `RefreshedReward` | all 130 |
| `BaseReward` | `DefaultReward` | `ALL(Challenges.Context.KilledByEnemy)` → `KilledByEnemyReward` | 65 Removed rows |
| `AlignmentModifier` | `DefaultFactor` | `ANY(Vehicle.Faction.Friendly, FriendlyKill)` → `FriendlyFactor`; `ANY(Vehicle.Faction.Neutral)` → `NeutralFactor`; `ANY(Vehicle.Faction.Hostile)` → `HostileFactor` | all 130 |
| `TargetZoneModifier` | `DefaultFactor` | `ALL(HotZoneMagnetActive, Target.InHotZone)` → `HotZoneMagnetFactor`; `ALL(Target.InHotZone)` → `HotZoneFactor`; `ALL(Target.InControlZone)` → `ControlZoneFactor` | all 130 |
| `DestroyedByTeamModifier` | `DefaultFactor` | `ALL(Challenges.Context.KilledByEnemy)` → `KilledByEnemyFactor` | 65 Removed rows |

Points to note:
- `AlignmentModifier` picks a factor by **faction of the target vehicle** (friendly, neutral, hostile). A friendly target also matches `FriendlyKill`.
- `DestroyedByTeamModifier` is keyed on `KilledByEnemy`, which reads oddly. The name suggests the factor applies when the spotted target was killed by an enemy. The option's name fits the Removed event, so this doc uses it as written.
- The `Player` row is in the calculator but **has no variant lookup row** (section 5).

The numeric values behind `BaseReward`, the faction factors and the zone factors are **not in this table**. The `DefaultReward`, `RefreshedReward` and `KilledByEnemyReward` names point to values held in the shared challenge tables (`Wardogs_Rewards_and_Progression_v2.md`, section 15).

---

## 4. Match-Score Payouts

### 4a. Live min and max ([`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json), 4 rows)

These are the values the v2 doc's section 9 quotes. The modifier columns are the part that doesn't appear there.

| Row | Base | Owner modifier | Assist base | Assist scaling |
|---|---|---|---|---|
| `Meta.Progression.Context.MatchScore.SpottedMin` | **15** | 1.0 | 0.5 | 0.2 |
| `Meta.Progression.Context.MatchScore.SpottedMax` | **275** | 0.2 | 0.1 | 0.2 |
| `Meta.Progression.Context.MatchScore.SpottedDestroyedMin` | **50** | 1.0 | 0.5 | 1.0 |
| `Meta.Progression.Context.MatchScore.SpottedDestroyedMax` | **500** | 0.75 | 0.5 | 0.75 |

All four rows also carry these modifiers at 1.0: `FriendlyModifier`, `NeutralModifier`, `ModifierCZ`, `ModifierHZ`, `ModifierHZM`, `InstigatorLocationRatioModifier`, `TargetLocationRatioModifier`, `CrewAssistModifier`, `LogisticAssistModifier`.

So the **owner** (the player who spotted) gets a reduced share of the max value (20% for a spot, 75% for a destroy). The **assist** share is driven by `AssistBaseModifier` and `AssistScalingModifier`. The spread between min and max is set by the assist-scaling curve (in the v2 doc's terms).

### 4b. Placeholder rows ([`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json), 3 rows, all zero)

`Meta.Progression.Resources.MatchScore.SpottingOwner`, `...SpottingAssist` and `...SpottingDestroyed`. Each has `ResourceValue = 0.0`, `ResourceTag = Attribute.Meta.Currency.Cash`. These are the same stale layer the v1 Rewards doc found: the live numbers are in [`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json) above.

---

## 5. Variant Lookups ([`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json) and `_Removed`)

Each lookup has 51 rows and maps the spotted variant to its reward tag. Each row now has its own reward tag, so the table below lists each one (Added shown; Removed uses the same variants with the `.Removed.` prefix). The Added and Removed tables are identical in layout. Only the reward tag prefix differs (`.Added.` or `.Removed.`).

| Reward tag | Variant tag |
|---|---|
| `Spotting.*.Kodiak.Default` | `Vehicle.Variant.Land.Wheeled.Kodiak.Default` |
| `Spotting.*.Kodiak.MachineGun` | `Vehicle.Variant.Land.Wheeled.Kodiak.MachineGun` |
| `Spotting.*.Kodiak.Pickup` | `Vehicle.Variant.Land.Wheeled.Kodiak.Pickup` |
| `Spotting.*.WHL_08.Default` | `Vehicle.Variant.Land.Wheeled.WHL_08.Default` |
| `Spotting.*.WHL_08.MachineGun` | `Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun` |
| `Spotting.*.LittleBird.Default` | `Vehicle.Variant.Air.Rotary.Littlebird.Default` |
| `Spotting.*.LittleBird.MountedMachineGuns` | `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` |
| `Spotting.*.LittleBird.RocketPods` | `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` |
| `Spotting.*.Huey.Default` | `Vehicle.Variant.Air.Rotary.ROT_01.Default` |
| `Spotting.*.Huey.MountedMachineGuns` | `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` |
| `Spotting.*.Blackhawk.Default` | `Vehicle.Variant.Air.Rotary.ROT_04.Default` |
| `Spotting.*.Blackhawk.MountedMachineGuns` | `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` |
| `Spotting.*.Havoc.Default` | `Vehicle.Variant.Air.Rotary.Havoc.Default` |
| `Spotting.*.SpawnVehicle.Lonestar` | `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar` |
| `Spotting.*.SpawnVehicle.Manticore` | `Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore` |
| `Spotting.*.SpawnVehicle.Valkyra` | `Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra` |
| `Spotting.*.TNK_01.Heavy` | `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` |
| `Spotting.*.TNK_01.Artillery` | `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` |
| `Spotting.*.TNK_01.AntiAir` | `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` |
| `Spotting.*.TNK_04.Default` | `Vehicle.Variant.Land.Tracked.TNK_04.Default` |
| `Spotting.*.Bobcat.Default` | `Vehicle.Variant.Land.Wheeled.Bobcat.Default` |
| `Spotting.*.Humvee.Default` | `Vehicle.Variant.Land.Wheeled.Humvee.Default` |
| `Spotting.*.Humvee.MachineGun` | `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` |
| `Spotting.*.Humvee.Minigun` | `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` |
| `Spotting.*.DuneBuggy.Default` | `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` |
| `Spotting.*.Ural.Battle` | `Vehicle.Variant.Land.Wheeled.Ural.Battle` |
| `Spotting.*.Ural.Attack` | `Vehicle.Variant.Land.Wheeled.Ural.Attack` |
| `Spotting.*.Ural.Default` | `Vehicle.Variant.Land.Wheeled.Ural.Default` |
| `Spotting.*.Claymore` | `Id.Item.Claymore` |
| `Spotting.*.ATMine` | `ID.Item.ATMine` |
| `Spotting.*.FOB` | `Id.Buildable.FOB` |
| `Spotting.*.BuildableHotZoneMagnet` | `Id.Buildable.HotzoneMagnet` |
| `Spotting.*.SupplyCrate.Free` | `ID.Item.VehicleSupplyCrate.Free` |
| `Spotting.*.SupplyCrate.Container.Free` | `ID.Item.VehicleSupplyCrate.Container.Free` |
| `Spotting.*.SupplyCrate.Small` | `ID.Item.VehicleSupplyCrate.Small` |
| `Spotting.*.SupplyCrate.Small.Armoured` | `ID.Item.VehicleSupplyCrate.Small.Armoured` |
| `Spotting.*.SupplyCrate.Large` | `ID.Item.VehicleSupplyCrate.Large` |
| `Spotting.*.SupplyCrate.Large.Armoured` | `ID.Item.VehicleSupplyCrate.Large.Armoured` |
| `Spotting.*.SupplyCrate.Pallet.BuildSupply` | `ID.Item.VehicleSupplyCrate.Pallet.BuildSupply` |
| `Spotting.*.SupplyCrate.Pallet.FuelSupply` | `ID.Item.VehicleSupplyCrate.Pallet.FuelSupply` |
| `Spotting.*.SupplyCrate.Pallet.MunitionsSupply` | `ID.Item.VehicleSupplyCrate.Pallet.MunitionsSupply` |
| `Spotting.*.SupplyCrate.Pallet.SparePartsSupply` | `ID.Item.VehicleSupplyCrate.Pallet.SparePartsSupply` |
| `Spotting.*.MistralAA` | `Vehicle.Variant.Stationary.MistralAA` |
| `Spotting.*.Mortar` | `Vehicle.Variant.Stationary.Mortar` |
| `Spotting.*.Phalanx` | `Vehicle.Variant.Stationary.Phalanx` |
| `Spotting.*.Loudspeaker` | `Vehicle.Variant.Stationary.Loudspeaker` |
| `Spotting.*.BuildableRadio` | `Id.Buildable.Radio` |
| `Spotting.*.BuildableRepairStation` | `Id.Buildable.RepairStation` |
| `Spotting.*.BuildableRefuelStation` | `Id.Buildable.RefuelStation` |
| `Spotting.*.STN_05` | `Vehicle.Variant.Stationary.STN_05` |
| `Spotting.*.MGNest` | `Vehicle.Variant.Stationary.MGNest` |

Observations:
- **51 reward tags**, one per lookup row, appear in each lookup. The `Player` target is not in either lookup. The player row must be selected by a different path, which was not traced.
- Each reward tag now maps to a single variant tag. `MistralAA`, `Mortar` and [`STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/STN_05.json) have separate tags, and the Loudspeaker, Radio, RepairStation and RefuelStation buildables each have their own.

---

## 6. State Trees

Both trees are the KOTH-prefixed challenge runners for spotting. They follow the same challenge pipeline as the KOTH state trees (`Wardogs_GameFeatures_Challenges_KOTH_v2.md`, section 3a).

| Tree | States | Tags |
|---|---|---|
| `ST_..._Spotting_Added` | 22 | `Event.StateTree.Spotting.Added`, `Challenges.Rewards.Spotting.Added.Player` |
| `ST_..._Spotting_Removed` | 21 | `Event.StateTree.Spotting.Removed`, `Challenges.Rewards.Spotting.Removed.Player`, `Analytics.Player.Assists` |

The `Removed` tree is the only one that carries the `Analytics.Player.Assists` tag, which fits its "destroyed" meaning. The `Added` tree carries no analytics tag.

---

## 7. Skills ([`DT_Skills_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Skills/DT_Skills_Spotting.json), 2 rows)

Both skills are **Recon** role skills.

| Skill tag | Skill key | Gameplay effect | Attribute | Magnitude source |
|---|---|---|---|---|
| `Meta.Role.Recon.IncreasedSpottedTime` | `Meta.Skill.Character` | `GE_Spotting_IncreasedSpottedTime` | `Attribute.Gameplay.Spotting.SpottedTimeMultiplier` | Base 1.0, scaled by curve [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), row `IncreasedSpottedTime` |
| `Meta.Role.Recon.IncreasedSpottingDuration` | `Meta.Skill.Item` | `GE_Spotting_IncreasedSpottingDuration` | `Attribute.Gameplay.Spotting.SpottingDurationMultiplier` | Base 1.0, scaled by curve [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), row `IncreasedSpottingDuration` |

The skill attribute is a multiplier on how long a spot lasts (`SpottedTimeMultiplier` on the target side, `SpottingDurationMultiplier` on the spotter side). The actual per-rank values are in [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), which is outside this folder.

---

## 8. Feed Strings

### 8a. Challenge feed ([`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json), 3 rows)

| Feed tag | Default text | Conditional text (tag → text, audio) |
|---|---|---|
| `Challenges.Rewards.Spotting.Added` | Target Spotted | `ANY(Challenges.Rewards.Spotting.Refreshed)` → "Target Spotted Refreshed" (no audio override) |
| `Challenges.Rewards.Spotting.Refreshed` | Target Spotted Refreshed | none |
| `Challenges.Rewards.Spotting.Removed` | Spotted Target Destroyed | `Id.Item` → "Spotted Item Destroyed" (`Audio.Event.UX.Spotted.DestroyAssist.Deployable`); `Id.Buildable` → "Spotted Buildable Destroyed" (`...DestroyAssist.Buildable`); `Vehicle.Variant` → "Spotted Vehicle Destroyed" (`...DestroyAssist.Vehicle`) |

The default audio for the Removed row is `Audio.Event.UX.Spotted.DestroyAssist.Player`.

### 8b. Match-score feed ([`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json), 3 rows)

| Match-score tag | Text | Audio |
|---|---|---|
| `Meta.Progression.Resources.MatchScore.SpottingOwner` | Target Spotted | none |
| `Meta.Progression.Resources.MatchScore.SpottingAssist` | Target Spotted Assist | none |
| `Meta.Progression.Resources.MatchScore.SpottingDestroyed` | Spotted Target Destroyed | `Audio.Event.UX.Spotted.DestroyAssist` |

### 8c. Overlay ([`DA_SpottingOverlay`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/DA_SpottingOverlay.json))

| Setting | Value |
|---|---|
| Time until fade after action | 1.0 s |
| Distance text format | `{Distance} M` |
| Distance when empty | `___._` |

---

## 9. Trackers

Spotting has three tracker assets. The map and spatial trackers share the tag `Trackers.Type.SpottingTarget`.

### 9a. Map tracker ([`DT_TrackerData_Map_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Map/Data/DT_TrackerData_Map_Spotting.json) → [`DA_Tracker_Map_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Map/Data/DA_Tracker_Map_Spotting.json))

| Setting | Value |
|---|---|
| Widget | `W_Tracker_Map_SpottingTarget` |
| View model | `WDUISpottingTargetMapTrackerViewModel` |
| Required tags | `Meta.Alignment.Faction`, `Trackers.Type.SpottingTarget` |
| Recreate on faction change | Yes |

### 9b. Spatial tracker ([`DT_TrackerData_Spatial_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/DT_TrackerData_Spatial_Spotting.json) → [`DA_Tracker_Spatial_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/DA_Tracker_Spatial_Spotting.json))

| Element | Setting |
|---|---|
| Widget | `W_Tracker_Spatial_SpottingTarget` |
| View model | `WDUISpottingTargetSpatialTrackerViewModel` |
| Marker material | `M_UI_SpottingMarker` (default), `M_UI_SpottingTracker` (override) |
| Default marker texture | `T_UI_Map_Spotted`, scale 0.8, fade-out 3.0 s, starting opacity 0.75 |
| Reward tag on the default texture | `Challenges.Rewards.PlayerKill` |
| Distance text | Forced to metres |
| Line-of-sight rules | 3 rules, trace channel `ECC_GameTraceChannel4`. One rule has squared range 100,000,000 (about 10,000 units). Rendered-component check on. |
| Location offset | Base offset Z = 300. Second rule uses dynamic offset curve [`C_DynamicLocationOffsetSpottingTracker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/C_DynamicLocationOffsetSpottingTracker.json) (range about 252) and attaches to the `Head` bone. |
| Screen clamping | 250 × 250 px |
| World distance scale | 2 rules |

The spatial tracker has per-vehicle texture overrides, so the marker changes by target. The Littlebird override uses `T_UI_Map_Spotted_Heli` with rotation 90°, and each vehicle override carries its own `RewardTag` (for example `Challenges.Rewards.VehicleDestroyed.LittleBird`, `...Huey`, `...Havoc`, `...Blackhawk`).

### 9c. Material tracker ([`DT_MaterialTrackerSettingsData_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Optimization/Data/DT_MaterialTrackerSettingsData_Spotting.json) → [`DA_MaterialTrackerData_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Optimization/Data/DA_MaterialTrackerData_Spotting.json))

This tracker is for **stationary and artillery gunner positions**. It is shown only when the local player is a gunner.

| Setting | Value |
|---|---|
| Tracker type | `WDUIMaterialTracker_Spotting` |
| Requires state | `State.Player.Vehicle.Role.Gunner` |
| Allowed vehicles | `Vehicle.Variant.Land.Tracked.TNK_01.Artillery`, `Vehicle.Variant.Stationary.Mortar`, `Vehicle.Variant.Stationary.STN_05` |
| Override for current vehicle | Yes |
| Show cash text | No |
| Force metres | Yes |

It also keys a reward tag by target class (player → `Challenges.Rewards.PlayerKill`, rotary → per-variant `VehicleDestroyed` tags, tracked vehicle → `VehicleDestroyed.TNK_01.Heavy`, and so on).

---

## 10. Input

| Context | Binding | Action | Notes |
|---|---|---|---|
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Left mouse button | [`IA_Player_PrimaryUse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_PrimaryUse.json) | |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Gamepad right trigger (axis) | [`IA_Player_PrimaryUse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_PrimaryUse.json) | Has a `WDDeadZoneInputModifier` |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Mouse wheel up / down | [`IA_Player_IncreaseScopeZoom`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_IncreaseScopeZoom.json) / `DecreaseScopeZoom` | |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Left Shift | [`IA_Player_Focus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_Focus.json) | Gamepad left stick click also maps to Focus |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Gamepad left / right shoulder | [`IA_Player_Lean_Left`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_Lean_Left.json) / `Lean_Right` | |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | (unbound) | [`IA_Player_ToggleScopeZoom`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_ToggleScopeZoom.json) | Inherits settings from the action |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Gamepad D-pad right / left | `IncreaseScopeZoom` / `DecreaseScopeZoom` | `InputTriggerPulse` with interval 0.2 s |
| [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json) | (2 mappable key settings, 2 dead-zone modifiers) | | Not individually decoded |

The dead-zone modifiers mean stick and trigger input is filtered in both contexts.

---

## 11. Audio

| Event asset | Behaviours | Use (inferred) |
|---|---|---|
| [`AE_Comms_Spotted`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted.json) | Request spotted vox, play perspective sound, crosstalk | Radio call when a target is spotted |
| [`AE_Comms_Spotted_VehicleEmpty`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted_VehicleEmpty.json) | Same types as above | Variant for an empty spotted vehicle |
| [`AE_UX_Spotted_Target`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotted_Target.json) | Play spotted-target sound, crosstalk | UX cue on spot |
| [`AE_UX_Spotting_Start`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Start.json) | Set spotting parameters, execute trigger, play sound, crosstalk | Spotting mode opens |
| [`AE_UX_Spotting_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Stop.json) | Execute trigger, crosstalk | Spotting mode closes |
| [`AE_UX_Spotting_Complete`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Complete.json) | Execute trigger, crosstalk | Spot completed |

### 7b. Spot timing per target (round 39)

Read from the `BH_SpottingExtensionData` of each spotter item (**Data**; `Binoculars_Standard`, `Monocular`, `RangeFinder_Standard`, `RangeFinder_Expensive`). For every target class the spotter item lists four times: the time the crosshair must stay on the target (`SpotTime`), the time to refresh an existing spot (`SpotRefreshTime`), how long the spot fades (`DecayTime`) and how long a persistent spot is kept (`PersistentSpotTime`). Infantry (`WDMoverCharacter`): 0.5 s to spot, 30 s decay, 180 s persistent. The two Recon skills multiply spot time by the `CT_ReconSkills` rows `IncreasedSpottedTime` and `IncreasedSpottingDuration` (**Data**: skill level 0: 1.0, level 2: 1.2, level 4: 1.4). The units are not exported; seconds are presumed from the values (30, 90, 180, 900, 3600). Generated by `_tools/round39_medical_tables.py` into [`medical-status-r39.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/medical-status-r39.json).

<!-- r39_med spot_times -->
| Target class | Spot time (s) | Refresh time (s) | Decay time (s) | Persistent spot time (s) | Spotter items |
|---|---|---|---|---|---|
| `WDMoverCharacter` | 0.5 | 1.0 | 30 | 180 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDTargetDummy` | 0.5 | 1.0 | 30 | 180 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDAirplaneVehicle` | 0.75 | 1.25 | 60 | 180 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDRotaryVehicle` | 0.75 | 1.25 | 60 | 180 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDWheeledVehiclePawn` | 0.75 | 1.25 | 60 | 180 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDTrackedVehicle` | 1.25 | 1.5 | 90 | 180 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_BuildableRefuelStation` | 2.5 | 5.0 | 900 | 900 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_BuildableRepairStation` | 2.5 | 5.0 | 900 | 900 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_Buildable_HotzoneMagnet` | 2.5 | 5.0 | 900 | 900 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDStationaryVehicle` | 2.5 | 5.0 | 900 | 900 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_Buildable_ForwardOperatingBase_Lonestar` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_Buildable_ForwardOperatingBase_Manticore` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_Buildable_ForwardOperatingBase_Valkyra` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_ForwardOperatingBase_LoneStar` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_ForwardOperatingBase_Manticore` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `B_ForwardOperatingBase_Valkyra` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDLandminePlaceable` | 1.5 | 2.5 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDVehicleSupplyCrate` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
| `WDVehicleSupplyPallet` | 2.5 | 5.0 | 3600 | 3600 | Binoculars_Standard, Monocular, RangeFinder_Expensive, RangeFinder_Standard |
<!-- /r39_med -->

---

## 12. Limitations

- **Base values for each target** are not in this folder. The `BaseReward` options name `DefaultReward`, `RefreshedReward` and `KilledByEnemyReward`, and their numbers are in the shared challenge tables covered by the v2 doc (section 15). Only the min and max match-score values (section 4a) are in this folder.
- **The `Player` target** has a calculator row but no lookup row. The path that pays a spotted player was not traced.
- **Meaning of `DestroyedByTeamModifier`** is taken from its option name `KilledByEnemyFactor`. Its direction (boost or penalty) was not checked.
- **Zone and faction factor values** are not in this folder.
- **The [`Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Spotting.json) root bundle's widget element** and the gameplay cue path were not decoded in this pass.
- **The [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json) input context** was listed but not decoded to individual bindings.
- **The spatial tracker's second line-of-sight and world-scale rules** were counted but not individually checked for values.
- **The Recon skill magnitudes** come from [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), which is outside this folder.
- **[`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json)** is zero-valued (placeholder). Do not use it for live numbers.
