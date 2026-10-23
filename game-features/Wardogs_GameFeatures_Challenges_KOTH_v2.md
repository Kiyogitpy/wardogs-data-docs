---
title: "Challenges KOTH (feature)"
redirect_from: ["/Wardogs_GameFeatures_Challenges_KOTH_v2.html", "/Wardogs_GameFeatures_Challenges_KOTH_v2"]
parent: "Rewards & Unlocks"
description: "What the Package Contains, How the Pieces Connect, State Tree Inventory, Reward Lookup Tables"
---

# Wardogs — GameFeature: Challenges_KOTH Reference
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). Source: [`Wardogs/Plugins/GameFeatures/Challenges_KOTH/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH) (75 JSON files). Scripted pass over every file, then spot-checked against representative files.*

> **Scope note:** this folder holds the **wiring** for the KOTH challenge set: which state tree runs for which session event, which reward tag it grants, and which lookup table turns a vehicle/item variant into a reward tag. The **reward values** (cash, XP) live in the shared challenge tables outside this folder. See `Wardogs_Rewards_and_Progression_v2.md` (sections 10, 13, 15) and the sibling doc `Wardogs_GameFeatures_Rewards_v2.md`.

## Season 02 update (2026-10-15)

- **Challenge definitions are now present.** [`DT_Challenges_SessionEvents_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/DT_Challenges_SessionEvents_KOTH.json) went from 0 rows to **60 rows**. Every row has an empty `Rewards` and `Objectives` list. `Challenges.SessionEvents.SupplyPalletDropped` is the only row with auto-activate off.
- **Lookup tables grew:** `DestroyVehicle` 30 → **34** rows; `DestroyVehicleSection`, `DestroyVehicleFOBSuppliedAssist`, `DestroyVehicleLogisticAssist` and `DestroyVehicleReviveAssist` 24 → **28** rows each; `RevivePlayerLogisticAssist` and `RevivePlayerReviveAssist` 6 → **5** rows each.
- **Distinct reward tags referenced by the lookups:** 112 → **193**.
- **Vehicle variants now have their own reward tags.** `VehicleDestroyed.Kodiak` is now `VehicleDestroyed.Kodiak.Default`, `.Kodiak.MachineGun` and `.Kodiak.Pickup`. The same split applies to other families (for example `VehicleDestroyed.LittleBird` → `.LittleBird.Default`, `.LittleBird.MountedMachineGuns`, `.LittleBird.RocketPods`).
- **Supply crate tags were renamed:** `DestroySupplyCrate.Free` → `DestroySupplyCrate.Container.Free` (lookup), and `DestroySupplyCrate.Pallet` → `DestroySupplyCrate.Pallet.BuildSupply`, `.FuelSupply`, `.MunitionsSupply`, `.SparePartsSupply`.
- **Destroy-vehicle-section trees now grant reward tags** (previously none). Examples: `DestroyVehicleSection.CrewAssist` and `VehicleDestroyed.SupplyCrateAssist`.
- **State tree step counts changed:** `SafeZoneEntered` 24 → **36** states, `PlayerKill` 29 → **31**, `PlayerDelivered` 21 → **25**, `RevivePlayer` 35 → **36**, `RepairVehicle` 27 → **28**, `PurchaseFromSupplyCrate` 10 → **11**, `Player_DeploySupplyCrate` 15 → **18**. The overall range is now **10 to 36** states.
- **New reward tags on state trees:** `PassengerSurvived` (survival tree), `ReceiveTip` and `SendTip` (tip trees), `DeployOnVehicle`, `DeploySupplyCrate`, `DestroyThrowable`, `SupplyPalletDropped`, and `ZoneEntry.SpawnVehicle`.
- **Outside this folder, 6 files were added** under [`Content/Meta/Challenges/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Challenges): curve assets [`CRV_Challenges_Curves_DeploySupplyCrate_XP`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json) and [`CRV_Challenges_Curves_DestroySupplyCrate_Cash`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DestroySupplyCrate_Cash.json), and four challenge state trees: [`ST_Challenges_Challenge_PassengersDelivered`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_PassengersDelivered.json), [`ST_Challenges_Challenge_RewardedKills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedKills.json), [`ST_Challenges_Challenge_RewardedRevives`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedRevives.json) and [`ST_Challenges_Challenge_RewardedVehiclesDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedVehiclesDestroyed.json).
- **No files were removed** from this folder. The folder still holds 75 JSON files.

---

## 1. What the Package Contains

| Export type | Count | Role |
|---|---|---|
| `GameFeatureData` ([`Challenges_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/Challenges_KOTH.json)) | 1 | Root bundle. Two actions. |
| `GameFeatureAction_DataRegistrySource` | 1 | Adds [`DT_Challenges_SessionEvents_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/DT_Challenges_SessionEvents_KOTH.json) as a source to the `Challenges` registry (client and server). |
| `GameFeatureAction_DataRegistry` | 1 | Adds 13 lookup registries (`DR_SessionEvent_*`). |
| `StateTree` | 60 | One state tree per session event or assist variant (section 3). |
| `WDChallengeStateTreeSchema` | 60 | One schema object per state tree. All are empty (no properties). |
| `DataTable` | 14 | 1 challenge-definition table (**60 rows**) plus 13 reward lookup tables (section 4). |

The [`DT_Challenges_SessionEvents_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/DT_Challenges_SessionEvents_KOTH.json) table has `RowStruct = WDChallengeDefinition` and **60 rows**, one per session event or assist variant. Every row has empty `Rewards` and `Objectives` lists. The reward amounts for these challenges are not in this folder (section 5).

---

## 2. How the Pieces Connect

1. A gameplay event fires (for example `Event.StateTree.DestroyVehicle.Assist.CrewAssist`).
2. The matching state tree runs. Its states are, in order, roughly: wait for the event → populate context tags → populate reward XP tags → add role XP tag to context → transfer context from event → add crew/assist tags → increment match stat → **calculate reward** → update reward XP tags → **grant reward** → complete.
3. The state tree grants a **reward tag** (`Challenges.Rewards.*`).
4. Where the reward depends on *what* was involved (vehicle variant, item, supply crate), the registry lookup maps the variant tag to that reward tag (section 4).
5. The reward tag's cash and XP values are resolved from the shared challenge tables (not in this folder).

The state trees carry context tags such as `Challenges.Context.FriendlyKill`, `Challenges.Context.Target.Friendly`, `Challenges.Context.VehicleDismantled`, `Challenges.Context.Instigator.InSpawnVehicle`, `Challenges.Context.LastKiller` and `Challenges.Context.RessedByEnemy`. These are the inputs the shared calculator uses to pick modifiers.

---

## 3. State Tree Inventory (60 trees)

Families by event. State counts are the number of states in each tree (range **10 to 36**).

| Family | Trees | Event tag root | Reward tags referenced by the tree |
|---|---|---|---|
| Player kill (direct) | 6 | `Event.StateTree.PlayerKill[.CrewAssist / .FOBSuppliedAssist / .LogisticAssist / .ReviveAssist / .SupplyCrateAssist]` | `Challenges.Rewards.PlayerKill` and `.PlayerKill.LogisticAssist` (base and FOB, logistic and revive variants). None on the crew and supply crate variants. |
| Player kill (assist) | 6 | `Event.StateTree.KillAssist[.<assist type>]` | `Analytics.Player.Assists`, plus `Challenges.Rewards.PlayerKill`, `.PlayerKill.Assist` and `.PlayerKill.Assist.LogisticAssist` on the base and variants. None on the crew and supply crate variants. |
| Destroy vehicle | 12 | `Event.StateTree.DestroyVehicle[.Assist[.<type>] / .<assist type>]` | `Challenges.Rewards.VehicleDestroyed`, plus `.Assist.*`, `.CrewAssist`, `.FOBSuppliedAssist`, `.LogisticAssist`, `.ReviveAssist` and `.SupplyCrateAssist` variants. The FOB, logistic and revive variants also grant `Challenges.Rewards.RevivePlayer`. |
| Destroy vehicle section | 10 | `Event.StateTree.DestroyVehicleSection[.Assist][.<assist type>]` | `Challenges.Rewards.VehicleDestroyed` and `.DestroyVehicleSection.<type>` (CrewAssist, LogisticAssist, ReviveAssist). Logistic and revive variants also grant `RevivePlayer`. Assist base grants `Assist.VehicleDestroyed` and `.DamageAssist`. |
| Destroy supply crate | 1 | `Event.StateTree.DestroySupplyCrate` | `Challenges.Rewards.DestroySupplyCrate`, `Challenges.Rewards.DestroySupplyCrate.Free` and `Challenges.Rewards.ReceiveTip` |
| Heal player | 4 | `Event.StateTree.HealPlayer[.LogisticAssist / .ReviveAssist / .SupplyCrateAssist]` | `Challenges.Rewards.HealPlayer`, `.Tip.Heal` (base tree), plus `.LogisticAssist` and `.ReviveAssist` variants |
| Revive player | 5 | `Event.StateTree.RevivePlayer[.Contributor / .LogisticAssist / .ReviveAssist / .SupplyCrateAssist]` | `Challenges.Rewards.RevivePlayer`, `.Tip.Revive` (base tree), plus variants |
| Repair / refuel vehicle | 2 | `Event.StateTree.RepairVehicle`, `Event.StateTree.RefuelVehicle` | `Challenges.Rewards.RepairVehicle` and `.Tip.Repair` (repair tree), `Challenges.Rewards.Tip.Refuel` (refuel tree) |
| Player delivered / passenger | 2 | `Event.StateTree.PlayerDelivered`, `Event.StateTree.PassengerSurvived` | `Challenges.Rewards.Tip.PlayerDelivered` (delivery tree), `Challenges.Rewards.PassengerSurvived` (passenger tree) |
| Supply crate purchase / deploy | 3 | `Event.StateTree.PurchaseFromSupplyCrate`, `Event.StateTree.DeployOnVehicle`, `Event.StateTree.DeploySupplyCrate` | `Challenges.Rewards.PurchaseFromSupplyCrate`, `.DeployOnVehicle`, `.DeploySupplyCrate` |
| Throwables, pallets, air time | 4 | `Event.StateTree.DestroyThrowable`, `.SupplyPalletDropped`, `.VehicleAirborne`, `.VehicleFlyThrough` | `Challenges.Rewards.DestroyThrowable` and `.SupplyPalletDropped`. Air time and fly through trees reference none. |
| Zone and tips | 4 | `Event.StateTree.SafeZoneEntered`, `.ZoneEntry`, `.PreTip`, `.Tip` | `Challenges.Rewards.PassengerSurvived` (safe zone), `.ZoneEntry.SpawnVehicle` (zone entry), `.ReceiveTip` and `.SendTip` (pre-tip and tip) |
| Test | 1 | `Event.StateTree.Test` | None |

Notes:
- Reward tags in this table come from each tree's state data. Where a family lists none, the tree grants no reward tag through its state data.
- The `Event.StateTree.*` tags are how the game routes an event to its tree. The link from in-game action to event tag is not in this folder.

### 3a. Sampled tree: [`ST_Challenges_SessionEvents_KOTH_PlayerKill_Assist_CrewAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/ST_Challenges_SessionEvents_KOTH_PlayerKill_Assist_CrewAssist.json) (13 states)

`Root` → `Wait For Player Kill Assist Crew Assist Event` → `On Player Kill Assist Crew Assist Event` → `Populate Context` → `Populate Reward XP Tags` → `Add Role XP Tag To Context` → `Transfer Context from Event` → `Add Crew Assist To Context Tags` → `IncrementMatchStat` → `Calculate Reward` → `Update Reward XP Tags` → `Grant Reward` → `Complete When Done`

Tags present: `Event.StateTree.KillAssist.CrewAssist`, `Analytics.Player.Assists`, `State.Player.Vitality.Critical`.

---

## 4. Reward Lookup Tables (13 tables, 183 rows)

Each row maps a **variant tag** (the specific vehicle, item or buildable variant) to a **reward tag**. Row names and the `Tag` column are the variant. The `RewardTag` column is what the state tree grants.

| Lookup table | Rows | Maps to (reward tag family) | Examples |
|---|---|---|---|
| [`DT_RewardLookup_SessionEvent_DestroyVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicle.json) | 34 | `Challenges.Rewards.VehicleDestroyed.<Vehicle>.<Variant>` | Kodiak (3 variants), LittleBird (3), Huey (2), Blackhawk (2), SpawnVehicle (3), TNK_01 (3), TNK_04, WHL_08 (2), Bobcat, Humvee (3), DuneBuggy, Ural (3), Havoc, Loudspeaker, MistralAA, Mortar, Phalanx, STN_05, MGNest |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleSection`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleSection.json) | 28 | `Challenges.Rewards.DestroyVehicleSection.<Vehicle>.<Variant>` | Same vehicle families as above, section-based |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist.json) | 28 | `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.<Vehicle>.<Variant>` | Blackhawk, TNK_01.Artillery, Humvee, and others |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist.json) | 28 | `Challenges.Rewards.VehicleDestroyed.LogisticAssist.<Vehicle>.<Variant>` | Havoc, TNK_01.AntiAir, Humvee, and others |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist.json) | 28 | `Challenges.Rewards.VehicleDestroyed.ReviveAssist.<Vehicle>.<Variant>` | Same family pattern as above |
| [`DT_RewardLookup_SessionEvent_DestroySupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroySupplyCrate.json) | 10 | `Challenges.Rewards.DestroySupplyCrate.<Size>` | Free (2 variants: `Free` and `Container.Free`), Small, Small.Armoured, Large, Large.Armoured, Pallet (4 pallet types: BuildSupply, FuelSupply, MunitionsSupply, SparePartsSupply) |
| [`DT_RewardLookup_SessionEvent_HealPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer.json) | 6 | `Challenges.Rewards.HealPlayer.<Item>` | Bandage, SuperBandage, MedKit, StimPen, AdrenalinePen, Defibrillator |
| [`DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist.json) | 6 | `Challenges.Rewards.HealPlayer.LogisticAssist.<Item>` | Same six items |
| [`DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist.json) | 6 | `Challenges.Rewards.HealPlayer.ReviveAssist.<Item>` | Same six items |
| [`DT_RewardLookup_SessionEvent_RevivePlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayer.json) | 6 | `Challenges.Rewards.RevivePlayer.<Item>` | AdrenalinePen, Defibrillator, MedKit, Resuscitator (2 variants), StimPen |
| [`DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist.json) | 5 | `Challenges.Rewards.RevivePlayer.LogisticAssist.<Item>` | AdrenalinePen, Defibrillator, MedKit, Resuscitator, StimPen |
| [`DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist.json) | 5 | `Challenges.Rewards.RevivePlayer.ReviveAssist.<Item>` | AdrenalinePen, Defibrillator, MedKit, Resuscitator, StimPen |
| [`DT_RewardLookup_SessionEvent_RepairVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RepairVehicle.json) | 3 | `Challenges.Rewards.RepairVehicle.<Tool>` | Wrench.Standard, Drill.Light, Drill.Heavy |

Observations:
- Heal and revive lookups map a **consumable item** to a reward tag. The item tags are `Id.Item.*` (for example `Id.Item.MedKit.Standard`, `Id.Item.Defibrillator.Standard`).
- Repair lookups map a **tool** to a reward tag. Tool tags are `ID.Item.RepairTool.*`.
- Each vehicle variant now has its own reward tag. For example, Kodiak Default, MachineGun and Pickup grant `VehicleDestroyed.Kodiak.Default`, `VehicleDestroyed.Kodiak.MachineGun` and `VehicleDestroyed.Kodiak.Pickup`. Reward values for these tags are still resolved outside this folder.
- Row names and `Tag` columns are not always spelled identically. The revive lookups use `Defibrilator` in some row keys and `Medkit` in some row keys, while the `Tag` column is `Id.Item.Defibrillator.Standard` and `Id.Item.MedKit.Standard`. The `Tag` column is what the game uses to match. This was verified on the RevivePlayerLogisticAssist table.
- Across all 13 tables there are **193 distinct `Challenges.Rewards.*` reward tags** referenced by the lookups.

---

## 5. Reward Values

**Not in this folder.** The KOTH state trees grant reward tags, but the cash and XP amounts for those tags are defined in the shared challenge reward table ([`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json), under [`Content/Meta/Challenges/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Meta/Challenges)), which the existing v2 doc covers in section 15. Use that section for the per-kill and per-event calculator, and section 10 for end-of-match rewards.

---

## 6. Limitations
- Values for each `Challenges.Rewards.*` tag are not resolved in this doc. They live outside the folder.
- Per-state logic (the actual calculation in `Calculate Reward`) is compiled StateTree bytecode. This doc names states and tags but does not decode the expressions.
- [`DT_Challenges_SessionEvents_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/DT_Challenges_SessionEvents_KOTH.json) has 60 rows, but their `Rewards` and `Objectives` lists are empty. The reward amounts for each challenge are not visible from this folder.
- The `DataRegistry` action lists 13 lookup registries, but not every state tree maps to a lookup. Some trees (the families in section 3 with no `Challenges.Rewards.*` tag, or only event tags) grant no reward through a lookup, and their reward path was not traced.
- The `WDChallengeStateTreeSchema` objects carry no properties, so schema-level settings are not available.
- The meaning of `Challenges.Context.*` tags is inferred from their names. Their runtime values were not checked.
