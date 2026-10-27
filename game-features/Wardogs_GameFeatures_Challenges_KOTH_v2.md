---
title: "Challenges KOTH (feature)"
redirect_from: ["/Wardogs_GameFeatures_Challenges_KOTH_v2.html", "/Wardogs_GameFeatures_Challenges_KOTH_v2"]
parent: "Rewards & Unlocks"
description: "What the Package Contains, How the Pieces Connect, State Tree Inventory, Reward Lookup Tables"
---

# Wardogs — GameFeature: Challenges_KOTH Reference
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). Source: `Wardogs/Plugins/GameFeatures/Challenges_KOTH/` (75 JSON files). Scripted pass over every file, then spot-checked against representative files.*

> **Scope note:** this folder holds the **wiring** for the KOTH challenge set: which state tree runs for which session event, which reward tag it grants, and which lookup table turns a vehicle/item variant into a reward tag. The **reward values** (cash, XP) live in the shared challenge tables outside this folder. See `Wardogs_Rewards_and_Progression_v2.md` (sections 10, 13, 15) and the sibling doc `Wardogs_GameFeatures_Rewards_v2.md`.

## Season 02 update (2026-10-15)

- **Challenge definitions are now present.** `DT_Challenges_SessionEvents_KOTH` went from 0 rows to **60 rows**. Every row has an empty `Rewards` and `Objectives` list. `Challenges.SessionEvents.SupplyPalletDropped` is the only row with auto-activate off.
- **Lookup tables grew:** `DestroyVehicle` 30 → **34** rows; `DestroyVehicleSection`, `DestroyVehicleFOBSuppliedAssist`, `DestroyVehicleLogisticAssist` and `DestroyVehicleReviveAssist` 24 → **28** rows each. `RevivePlayerLogisticAssist` and `RevivePlayerReviveAssist` did not change (6 rows each in both seasons).
- **Distinct reward tags referenced by the lookups:** 112 → **193**.
- **Vehicle variants now have their own reward tags.** `VehicleDestroyed.Kodiak` is now `VehicleDestroyed.Kodiak.Default`, `.Kodiak.MachineGun` and `.Kodiak.Pickup`. The same split applies to other families (for example `VehicleDestroyed.LittleBird` → `.LittleBird.Default`, `.LittleBird.MountedMachineGuns`, `.LittleBird.RocketPods`).
- **Supply crate tags were renamed:** `DestroySupplyCrate.Free` → `DestroySupplyCrate.Container.Free` (lookup), and `DestroySupplyCrate.Pallet` → `DestroySupplyCrate.Pallet.BuildSupply`, `.FuelSupply`, `.MunitionsSupply`, `.SparePartsSupply`.
- **Destroy-vehicle-section trees now grant reward tags** (previously none). Examples: `DestroyVehicleSection.CrewAssist` and `VehicleDestroyed.SupplyCrateAssist`.
- **State tree step counts changed:** `SafeZoneEntered` 24 → **36** states, `PlayerKill` 29 → **31**, `PlayerDelivered` 21 → **25**, `RevivePlayer` 35 → **36**, `RepairVehicle` 27 → **28**, `PurchaseFromSupplyCrate` 10 → **11**, `Player_DeploySupplyCrate` 15 → **18**. The overall range is now **10 to 36** states.
- **New reward tags on state trees:** `PassengerSurvived` (survival tree), `ReceiveTip` and `SendTip` (tip trees), `DeployOnVehicle`, `DeploySupplyCrate`, `DestroyThrowable`, `SupplyPalletDropped`, and `ZoneEntry.SpawnVehicle`.
- **Outside this folder, 6 files were added** under `Content/Meta/Challenges/`: curve assets `CRV_Challenges_Curves_DeploySupplyCrate_XP` and `CRV_Challenges_Curves_DestroySupplyCrate_Cash`, and four challenge state trees: `ST_Challenges_Challenge_PassengersDelivered`, `ST_Challenges_Challenge_RewardedKills`, `ST_Challenges_Challenge_RewardedRevives` and `ST_Challenges_Challenge_RewardedVehiclesDestroyed`.
- **No files were removed** from this folder. The folder still holds 75 JSON files.

Full before/after list: [Season 2 Changes → Rewards & Unlocks]({{ '/season-2-changes/rewards-unlocks.html' | relative_url }}).

---

## 1. What the Package Contains

| Export type | Count | Role |
|---|---|---|
| `GameFeatureData` (`Challenges_KOTH`) | 1 | Root bundle. Two actions. |
| `GameFeatureAction_DataRegistrySource` | 1 | Adds `DT_Challenges_SessionEvents_KOTH` as a source to the `Challenges` registry (client and server). |
| `GameFeatureAction_DataRegistry` | 1 | Adds 13 lookup registries (`DR_SessionEvent_*`). |
| `StateTree` | 60 | One state tree per session event or assist variant (section 3). |
| `WDChallengeStateTreeSchema` | 60 | One schema object per state tree. All are empty (no properties). |
| `DataTable` | 14 | 1 challenge-definition table (**60 rows**) plus 13 reward lookup tables (section 4). |

The `DT_Challenges_SessionEvents_KOTH` table has `RowStruct = WDChallengeDefinition` and **60 rows**, one per session event or assist variant. Every row has empty `Rewards` and `Objectives` lists. The reward amounts for these challenges are not in this folder (section 5).

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

### 3a. Sampled tree: `ST_Challenges_SessionEvents_KOTH_PlayerKill_Assist_CrewAssist` (13 states)

`Root` → `Wait For Player Kill Assist Crew Assist Event` → `On Player Kill Assist Crew Assist Event` → `Populate Context` → `Populate Reward XP Tags` → `Add Role XP Tag To Context` → `Transfer Context from Event` → `Add Crew Assist To Context Tags` → `IncrementMatchStat` → `Calculate Reward` → `Update Reward XP Tags` → `Grant Reward` → `Complete When Done`

Tags present: `Event.StateTree.KillAssist.CrewAssist`, `Analytics.Player.Assists`, `State.Player.Vitality.Critical`.

---

## 4. Reward Lookup Tables (13 tables, 183 rows)

Each row maps a **variant tag** (the specific vehicle, item or buildable variant) to a **reward tag**. Row names and the `Tag` column are the variant. The `RewardTag` column is what the state tree grants.

| Lookup table | Rows | Maps to (reward tag family) | Examples |
|---|---|---|---|
| `DT_RewardLookup_SessionEvent_DestroyVehicle` | 34 | `Challenges.Rewards.VehicleDestroyed.<Vehicle>.<Variant>` | Kodiak (3 variants), LittleBird (3), Huey (2), Blackhawk (2), SpawnVehicle (3), TNK_01 (3), TNK_04, WHL_08 (2), Bobcat, Humvee (3), DuneBuggy, Ural (3), Havoc, Loudspeaker, MistralAA, Mortar, Phalanx, STN_05, MGNest |
| `DT_RewardLookup_SessionEvent_DestroyVehicleSection` | 28 | `Challenges.Rewards.DestroyVehicleSection.<Vehicle>.<Variant>` | Same vehicle families as above, section-based |
| `DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist` | 28 | `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.<Vehicle>.<Variant>` | Blackhawk, TNK_01.Artillery, Humvee, and others |
| `DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist` | 28 | `Challenges.Rewards.VehicleDestroyed.LogisticAssist.<Vehicle>.<Variant>` | Havoc, TNK_01.AntiAir, Humvee, and others |
| `DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist` | 28 | `Challenges.Rewards.VehicleDestroyed.ReviveAssist.<Vehicle>.<Variant>` | Same family pattern as above |
| `DT_RewardLookup_SessionEvent_DestroySupplyCrate` | 10 | `Challenges.Rewards.DestroySupplyCrate.<Size>` | Free (2 variants: `Free` and `Container.Free`), Small, Small.Armoured, Large, Large.Armoured, Pallet (4 pallet types: BuildSupply, FuelSupply, MunitionsSupply, SparePartsSupply) |
| `DT_RewardLookup_SessionEvent_HealPlayer` | 6 | `Challenges.Rewards.HealPlayer.<Item>` | Bandage, SuperBandage, MedKit, StimPen, AdrenalinePen, Defibrillator |
| `DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist` | 6 | `Challenges.Rewards.HealPlayer.LogisticAssist.<Item>` | Same six items |
| `DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist` | 6 | `Challenges.Rewards.HealPlayer.ReviveAssist.<Item>` | Same six items |
| `DT_RewardLookup_SessionEvent_RevivePlayer` | 6 | `Challenges.Rewards.RevivePlayer.<Item>` | AdrenalinePen, Defibrillator, MedKit, Resuscitator (2 variants), StimPen |
| `DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist` | 5 | `Challenges.Rewards.RevivePlayer.LogisticAssist.<Item>` | AdrenalinePen, Defibrillator, MedKit, Resuscitator, StimPen |
| `DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist` | 5 | `Challenges.Rewards.RevivePlayer.ReviveAssist.<Item>` | AdrenalinePen, Defibrillator, MedKit, Resuscitator, StimPen |
| `DT_RewardLookup_SessionEvent_RepairVehicle` | 3 | `Challenges.Rewards.RepairVehicle.<Tool>` | Wrench.Standard, Drill.Light, Drill.Heavy |

Observations:
- Heal and revive lookups map a **consumable item** to a reward tag. The item tags are `Id.Item.*` (for example `Id.Item.MedKit.Standard`, `Id.Item.Defibrillator.Standard`).
- Repair lookups map a **tool** to a reward tag. Tool tags are `ID.Item.RepairTool.*`.
- Each vehicle variant now has its own reward tag. For example, Kodiak Default, MachineGun and Pickup grant `VehicleDestroyed.Kodiak.Default`, `VehicleDestroyed.Kodiak.MachineGun` and `VehicleDestroyed.Kodiak.Pickup`. Reward values for these tags are still resolved outside this folder.
- Row names and `Tag` columns are not always spelled identically. The revive lookups use `Defibrilator` in some row keys and `Medkit` in some row keys, while the `Tag` column is `Id.Item.Defibrillator.Standard` and `Id.Item.MedKit.Standard`. The `Tag` column is what the game uses to match. This was verified on the RevivePlayerLogisticAssist table.
- Across all 13 tables there are **193 distinct `Challenges.Rewards.*` reward tags** referenced by the lookups.

---

## 5. Reward Values

**Not in this folder.** The KOTH state trees grant reward tags, but the cash and XP amounts for those tags are defined in the shared challenge reward table (`DT_ChallengeRewards_SessionEvents_Shared`, under `Content/Meta/Challenges/`), which the existing v2 doc covers in section 15. Use that section for the per-kill and per-event calculator, and section 10 for end-of-match rewards.

---

## 5.1 State tree logic (decoded, round 86)

A compiled `StateTree` asset is not bytecode. It keeps its states, transitions, task and condition nodes (editor name and instance values) and its property bindings in flat arrays. [`_tools/statetree_outline.py`](../_tools/statetree_outline.py) resolves all 83 `ST_Challenges_*` trees (the 60 here plus the Hot Zone Magnet, Buildable, Spotting and Team Offence trees) into [`challenge-statetrees.json`](../assets/data/challenge-statetrees.json): per state its enter conditions, tasks and transitions, and every binding as `target <- source`. Native task and condition classes keep their code in the executable; what is read here is the wiring and the values.

**Shape of every reward tree** (**Data**). A tree waits in `Wait For ... Event` for its `Event.StateTree.*` tag, then enters `Populate Context`. The gate there is a list of conditions (killer is not the victim, victim is a pawn, and so on). If it passes, a chain of small states each add one `Challenges.Context.*` tag to the challenge's context when their condition holds (the table below), then `Track Target Repeat Count` (task `Resolve Repeat Action Count`), `Calculate Reward` (task `Calculate Reward`, which succeeds or fails and ends the run on failure), `Update Reward XP Tags` and `Grant Reward`. Some trees then broadcast an assist event (crew, logistic, revive, FOB-supplied, supply crate) for the helpers. Every tree ends in `Complete When Done`, which returns to `Root` on the next tick.

**Repeat-reward window** (**Data**). The evaluator `Get Repeat Actions Cooldown` holds `RepeatActionsCooldown` = 180 s in all 25 trees that use it (44 evaluator nodes), and `Resolve Repeat Action Count` receives it as its cooldown. The count it produces is the `RepeatCount` parameter, which `Calculate Reward` receives under the name `LastVictimCount` in 29 trees. That is the consumer of the repeated-target value on the reward-input side: the value is the number of recent rewards for the same target, with a 180 s window. The reward formula turns it into a smaller payout: in `Challenges.Rewards.PlayerKill` the term is `1 - clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier`, read from the reward row (data; the native task only evaluates it, see [Rewards and Progression](../Wardogs_Rewards_and_Progression_v2.md) section 15). A tree that never sets the count pays with 0 for it.

**What feeds `Calculate Reward`** (**Data**, generated). The input names are the variables the reward formula can read; the right column is the tree parameter or evaluator bound to them. Inputs with no binding are set by a state task.

<!-- statetree_tables inputs -->
| Inputs to `Calculate Reward` | Bound from | Trees | Examples |
|---|---|---:|---|
| BaseRewardValue | Get Reward Resource Value | 16 | `KOTH_DestroyVehicleSection_Assist_LogisticAssist`, `KOTH_DestroyVehicleSection_Assist_ReviveAssist`, `KOTH_DestroyVehicleSection_LogisticAssist` |
| CalculatedReward | CalculatedReward | 14 | `KOTH_DestroyVehicleSection_Assist_CrewAssist`, `KOTH_DestroyVehicleSection_Assist_SupplyCrateAssist`, `KOTH_DestroyVehicleSection_CrewAssist` |
| LastVictimCount | RepeatCount | 8 | `Buildable_FOBDoorClosed`, `Buildable_FOBHacked`, `Crowbar_ForceOpenDoor` |
| LastVictimCount, DistanceToTarget, KillStreak | RepeatCount | 6 | `KOTH_PlayerKill_Assist_FOBSuppliedAssist`, `KOTH_PlayerKill_Assist_LogisticAssist`, `KOTH_PlayerKill_Assist_ReviveAssist` |
| BaseRewardValue, NumberOfAssisters | Get Reward Resource Value, NumberOfAssisters | 4 | `KOTH_DestroyVehicle_Assist_FOBSuppliedAssist`, `KOTH_DestroyVehicle_FOBSuppliedAssist`, `KOTH_PlayerKill_Assist_FOBSuppliedAssist` |
| DamageDealthModifier, KillReward | Divide.Result, Get Reward Resource Value | 4 | `KOTH_PlayerKill_Assist`, `KOTH_PlayerKill_Assist_FOBSuppliedAssist`, `KOTH_PlayerKill_Assist_LogisticAssist` |
| DamageFraction, FactionScoreDifference, KillStreak | Calculate Vehicle Damage Fraction.DamageFraction | 3 | `KOTH_DestroyVehicle_Assist_FOBSuppliedAssist`, `KOTH_DestroyVehicle_Assist_LogisticAssist`, `KOTH_DestroyVehicle_Assist_ReviveAssist` |
| FactionScoreDifference, KillStreak | (set by a state task, not a parameter) | 3 | `KOTH_DestroyVehicle_FOBSuppliedAssist`, `KOTH_DestroyVehicle_LogisticAssist`, `KOTH_DestroyVehicle_ReviveAssist` |
| HealFactor, LastVictimCount | HealFraction, RepeatCount | 3 | `KOTH_HealPlayer`, `KOTH_HealPlayer_LogisticAssist`, `KOTH_HealPlayer_ReviveAssist` |
| LastVictimCount | (set by a state task, not a parameter) | 3 | `KOTH_DestroyVehicleSection_LogisticAssist`, `KOTH_DestroyVehicleSection_ReviveAssist`, `KOTH_RevivePlayer` |
| BuildSuppliesConsumed | BuildSuppliesConsumed | 2 | `Buildable_BuildSuppliesConsumed` |
| BuildSuppliesDeposited | BuildSuppliesDeposited | 2 | `Buildable_BuildSuppliesDeposited` |
| LastVictimCount, DamageFraction | Calculate Vehicle Damage Fraction.DamageFraction | 2 | `KOTH_DestroyVehicleSection_Assist_LogisticAssist`, `KOTH_DestroyVehicleSection_Assist_ReviveAssist` |
| PreTipValue | PreTipValue | 2 | `KOTH_PreTip` |
| SupplyCrateValue | SupplyCrateValue | 2 | `KOTH_DestroySupplyCrate` |
| TipAmount | Enter Event.Payload.CurrentStepAmount | 2 | `KOTH_Tip` |
| BuildAmount | BuildAmount | 1 | `Buildable_Building` |
| BuildCost | BuildCost | 1 | `Buildable_BuildingFinished` |
| BuildProgress, TotalFOBSupplies | BuildingProgress, TotalFOBSupplies | 1 | `Buildable_BuildableDestroyed` |
| CashSpent | MoneySpent | 1 | `Buildable_FOBOwnerPayed` |
| DamageFraction, BuildProgress, TotalFOBSupplies | DamageFraction, BuildingProgress, TotalFOBSupplies | 1 | `Buildable_BuildableDestroyed_Assist` |
| DamageFraction, FactionScoreDifference, KillStreak, CrewCount | Calculate Vehicle Damage Fraction.DamageFraction, Get Faction Score Difference.Difference, Get Players Match Stat.Value, Get Crew Members For Player Count.CrewCount | 1 | `KOTH_DestroyVehicle_Assist` |
| DamageFraction, LastVictimCount, CrewCount | Calculate Vehicle Damage Fraction.DamageFraction, RepeatCount, Get Crew Members For Player Count.CrewCount | 1 | `KOTH_DestroyVehicleSection_Assist` |
| ElapsedAirTime | ElapsedAirTime | 1 | `VehicleAirTime` |
| FactionScoreDifference, KillStreak, CrewCount | Get Faction Score Difference.Difference, Get Players Match Stat.Value, Get Crew Members For Player Count.CrewCount | 1 | `KOTH_DestroyVehicle` |
| LastVictimCount, CrewCount | TargetCount, Get Crew Members For Player Count.CrewCount | 1 | `KOTH_DestroyVehicleSection` |
| LastVictimCount, DistanceToTarget, KillStreak, CrewCount | RepeatCount, Get Distance Between Actors.OutDistance, Get Players Match Stat.Value, Get Crew Members For Player Count.CrewCount | 1 | `KOTH_PlayerKill_Assist` |
| LastVictimCount, DistanceToTarget, KillStreak, CrewCount | VictimCount, Get Distance Between Actors.OutDistance, Get Players Match Stat.Value, Get Crew Members For Player Count.CrewCount | 1 | `KOTH_PlayerKill` |
| LastVictimCount, InteractionProgress | RepeatCount, InteractionProgress | 1 | `KOTH_RevivePlayerContributor` |
| LastVictimCount, ScalarValue | RepeatCount, ScalarValue | 1 | `KOTH_Spotting_Added` |
| MarkupMultiplier, PurchaseValue, LastVictimCount | MarkupMultiplier, PurchaseValue, VictimCount | 1 | `KOTH_PurchaseFromSupplyCrate` |
| PlayerCount, PlayerStreak | Get Control Zone Player Count.PlayerCount, PlayerStreak | 1 | `KOTH_PlayerDelivered` |
| PlayersSurvivedCount, ReturnStreak | PlayersSurvivedCount, ReturnStreak | 1 | `KOTH_SafeZoneEntered` |
| RefuelAmount, CurrentFuel, MaxFuel, LastVictimCount | RefuelAmount, CurrentAmount, MaxAmount, RepeatCount | 1 | `KOTH_RefuelVehicle` |
| RepeatActionCount | RepeatActionCount | 1 | `VehicleFlyThrough` |
| ScalarValue | ScalarValue | 1 | `KOTH_Spotting_Removed` |
| SupplyCrateValue, CrateStreak | SupplyCrateValue, CrateStreak | 1 | `Player_DeploySupplyCrate` |
<!-- /statetree_tables -->

**Context tags and their conditions** (**Data**, generated). A tag is added when the condition in the right column holds. Zone conditions are native condition classes (`Actor In Control Zone`, `Actor In Hot Zone`, `Hot Zone Magnet Active`); the tree supplies the actor and the wanted answer. `Float Compare` and `Integer Compare` rows show the operator, the constants and what is bound to the left side. Distances are Unreal units (centimetres).

<!-- statetree_tables rules -->
| Context tag | Added when | Trees |
|---|---|---:|
| `Challenges.Context.AirVehicleKill` | Actor Occupies Vehicle Condition(AcceptedVehicles Vehicle.Variant.Air.Rotary.Havoc.Default, Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns, Vehicle.Variant.Air.Rotary.Littlebird.RocketPods, Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns) and Tag Equal Condition(TagB State.Player.Vehicle.Role.Gunner) or Tag Equal Condition(TagB State.Player.Vehicle.Role.Driver) or Tag Equal Condition(TagB Attribute.Meta.XP.Role.Pilot) | 1 |
| `Challenges.Context.AssaultKill` | Tag Equal Condition(TagB Attribute.Meta.XP.Role.Infantry) | 1 |
| `Challenges.Context.Assist.TrackingVehicle` | Has Tag(Tag Meta.Progression.Resources.MatchScore.TrackingDestroyVehicle) | 1 |
| `Challenges.Context.Buildables.BuildableOwner` | Object Equals | 2 |
| `Challenges.Context.Buildables.BuildableOwner` | Bool Compare(bLeft False; bRight True) | 1 |
| `Challenges.Context.Buildables.Dismantle` | Tag Equal Condition(TagB ID.Item.BuildTool.Hammer.Large) or Tag Equal Condition(TagB ID.Item.BuildTool.Hammer.Medium) or Tag Equal Condition(TagB ID.Item.BuildTool.Hammer.Small) or Has Tag(Tag Meta.Damage.DamageType.Dismantle) | 3 |
| `Challenges.Context.Buildables.Dismantle` | Tag Equal Condition(TagB ID.Item.BuildTool.Hammer.Large) or Tag Equal Condition(TagB ID.Item.BuildTool.Hammer.Medium) or Tag Equal Condition(TagB ID.Item.BuildTool.Hammer.Small) or Has Tag(Tag Meta.Damage.DamageType.Dismantle) or Has Tag(Tag Challenges.Context.VehicleDismantled) | 2 |
| `Challenges.Context.Buildables.Friendly` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Friendly) | 3 |
| `Challenges.Context.Buildables.Friendly` | Object Is Valid | 1 |
| `Challenges.Context.Buildables.InFOB` | Has Tag(Tag Buildable.BuildFinished.Context.InFOB) | 2 |
| `Challenges.Context.Buildables.SchematicOwner` | Object Equals | 2 |
| `Challenges.Context.CrewAssistPenalty` | Integer Compare(Greater; Left 0; Right 1; Left from Get Crew Members For Player Count.CrewCount) | 6 |
| `Challenges.Context.ExplosiveKill` | Has Tag(TagContainer ID.Item.ATMine, Id.Item.C4Explosive, Id.Item.Claymore, Id.Item.IED.Explosive, Id.Item.Launcher_04, Id.Item.72mm, … (8 in all)) | 2 |
| `Challenges.Context.ExplosiveKill` | Has Tag(TagContainer ID.Item.ATMine, Id.Item.C4Explosive, Id.Item.Claymore, Id.Item.IED.Explosive) | 1 |
| `Challenges.Context.FreeVehicle` | Actor Has Matching GameplayTag(TagToMatch State.Vehicle.FreeVehicle) and Object Equals | 1 |
| `Challenges.Context.FreeVehicle` | Actor Has Matching GameplayTag(TagToMatch State.Vehicle.FreeVehicle) and Object Equals or Object Equals | 1 |
| `Challenges.Context.FriendlyKill` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Friendly) | 8 |
| `Challenges.Context.Headshot` | Name Compare(Left None; Right Head) | 1 |
| `Challenges.Context.Heal.BuffItem` | Has Tags(OtherContainer Id.Item.StimPen) | 3 |
| `Challenges.Context.Heal.ReviveItem` | Has Tags(OtherContainer Id.Item.AdrenalinePen, Id.Item.Defibrillator) | 3 |
| `Challenges.Context.HotZoneMagnet.Hostile` | not Tag Equal Condition | 1 |
| `Challenges.Context.HotZoneMagnet.Instigator` | Object Equals | 3 |
| `Challenges.Context.HotZoneMagnetActive` | Hot Zone Magnet Active(bMagnetEnabled True) | 47 |
| `Challenges.Context.Instigator.InControlZone` | Actor In Control Zone(bInsideTheZone True) | 45 |
| `Challenges.Context.Instigator.InHotZone` | Actor In Hot Zone(bInsideTheZone True) | 45 |
| `Challenges.Context.Instigator.InSpawnVehicle` | Bool Compare(bLeft False; bRight True) and Float Compare(Less; Left 0.0; Right 0.0; Left from SpawnVehicleOwnerSetWorldTime; Right from Get Server World Time.ServerWorldTimeSeconds) | 2 |
| `Challenges.Context.Instigator.InSpawnVehicle` | Bool Compare(bLeft False; bRight True) | 1 |
| `Challenges.Context.Instigator.InSpawnVehicle` | Bool Compare(bLeft False; bRight True) and Tag Equal Condition(TagB Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar) or Tag Equal Condition(TagB Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore) or Tag Equal Condition(TagB Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra) and Tag Equal Condition(TagB State.Player.Vehicle.Role.Driver) | 1 |
| `Challenges.Context.Instigator.InSpawnVehicle` | Has Tags(OtherContainer Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar, Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra, Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore) | 1 |
| `Challenges.Context.Instigator.NotInVehicle` | not Actor Occupies Vehicle Condition | 9 |
| `Challenges.Context.KillStreakStopped` | Integer Compare(Greater; Left 0; Right 6; Left from Get Players Match Stat.Value) | 1 |
| `Challenges.Context.KilledByEnemy` | Bool Compare(bLeft False; bRight False) | 1 |
| `Challenges.Context.KilledByFriendly` | Last Killer Hostility Condition(AcceptedValues ETeamAttitude::Friendly) | 1 |
| `Challenges.Context.LastKiller` | Is Last Killer Condition | 2 |
| `Challenges.Context.PrecisionArtilleryStrikeKill` | Actor In Control Zone(bInsideTheZone True) and Actor In Control Zone(bInsideTheZone False) and Actor Occupies Vehicle Condition(AcceptedVehicles Vehicle.Variant.Land.Tracked.TNK_01.Artillery) | 7 |
| `Challenges.Context.PrecisionArtilleryStrikeKill` | Actor In Control Zone(bInsideTheZone True) and Actor In Control Zone(bInsideTheZone False) and Actor Occupies Vehicle Condition(AcceptedVehicles Vehicle.Variant.Land.Tracked.TNK_01.Artillery) or Actor Occupies Vehicle Condition(AcceptedVehicles Vehicle.Variant.Stationary.Mortar) | 1 |
| `Challenges.Context.RessedByEnemy` | Actor Has Matching GameplayTag(TagToMatch State.Player.RessedByEnemy) | 2 |
| `Challenges.Context.RevengeKill` | Is Last Killer Condition | 1 |
| `Challenges.Context.SniperKill` | Has Tag(TagContainer Id.Item.MK22, Id.Item.Mosin, Id.Item.SR_04, Id.Item.SV98, Id.Item.RFB, Id.Item.SVDM, … (7 in all)) and Float Compare(GreaterOrEqual; Left 0.0; Right 30000.0; Left from Get Distance Between Actors.OutDistance) | 1 |
| `Challenges.Context.SpawnVehicle` | Actor Has Matching GameplayTag(TagToMatch Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar) or Actor Has Matching GameplayTag(TagToMatch Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore) or Actor Has Matching GameplayTag(TagToMatch Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra) | 2 |
| `Challenges.Context.SupplyCrateEmpty` | Bool Compare(bLeft False; bRight True) | 1 |
| `Challenges.Context.TankKill` | Actor Occupies Vehicle Condition(AcceptedVehicles Vehicle.Variant.Land.Tracked.TNK_01.Artillery, Vehicle.Variant.Land.Tracked.TNK_01.Heavy) or Tag Equal Condition(TagB Id.Vehicle.WeaponExtension.TNK_01.Artillery) or Tag Equal Condition(TagB Id.Vehicle.WeaponExtension.TNK_01.Heavy) or Tag Equal Condition(TagB Id.Vehicle.Weapon.TNK_01.Turret.AntiAir) or Tag Equal Condition(TagB Id.Vehicle.Weapon.TNK_01.Turret.Artillery) or Tag Equal Condition(TagB Id.Vehicle.Weapon.TNK_01.Turret.Heavy) or Tag Equal Condition(TagB Id.Vehicle.Weapon.TNK_01.MountedMachineGun) or Tag Equal Condition(TagB Id.Vehicle.WeaponExtension.TNK_01.MountedMachineGun) or Tag Equal Condition(TagB Id.Vehicle.WeaponExtension.TNK_01.MachineGun) or Tag Equal Condition(TagB Id.Vehicle.WeaponExtension.TNK_01.Light) or Tag Equal Condition(TagB Id.Vehicle.WeaponExtension.TNK_01.AntiAir) | 1 |
| `Challenges.Context.Target.FreeSpawn` | not Object Is Valid | 4 |
| `Challenges.Context.Target.Friendly` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Friendly) | 6 |
| `Challenges.Context.Target.Hostile` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Hostile) | 4 |
| `Challenges.Context.Target.InControlZone` | Actor In Control Zone(bInsideTheZone True) | 41 |
| `Challenges.Context.Target.InHotZone` | Actor In Hot Zone(bInsideTheZone True) | 41 |
| `Challenges.Context.Target.InSafeZone` | Actor Has Matching GameplayTag(TagToMatch State.Location.SafeZone.Alpha) or Actor Has Matching GameplayTag(TagToMatch State.Location.SafeZone.Bravo) or Actor Has Matching GameplayTag(TagToMatch State.Location.SafeZone.Charlie) | 3 |
| `Challenges.Context.Target.Neutral` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Neutral) | 4 |
| `Challenges.Context.Target.Neutral` | Actor In Control Zone(bInsideTheZone False) and Float Compare(Greater; Left 0.0; Right 10000.0; Left from Get Actor Distance From Control Zone.Distance) | 1 |
| `Challenges.Context.Target.Neutral` | Bool Compare(bLeft False; bRight True) | 1 |
| `Challenges.Context.Target.Neutral` | Tag Equal Condition or not Tag Equal Condition(TagB Attribute.Meta.XP.Role.Driver) | 1 |
| `Challenges.Context.Target.PlayerOwned` | Object Equals | 6 |
| `Challenges.Context.Target.PlayerOwned` | Is Owner | 1 |
| `Challenges.Rewards.Spotting.Refreshed` | Bool Compare(bLeft False; bRight True) | 1 |
| `Meta.Progression.Context.Target.InControlZone` | Actor In Control Zone(bInsideTheZone True) | 1 |
| `Meta.Progression.Context.Target.InHotZone` | Actor In Hot Zone(bInsideTheZone True) | 1 |
| `Meta.Progression.Context.Target.InNoMansLand` | Actor In Control Zone(bInsideTheZone False) | 1 |
| `Meta.Progression.Context.Vehicle.Buyer` | Object Equals and not Has Tag(TagContainer Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar, Vehicle.Variant.Land.Tracked.SpawnVehicle.Manticore, Vehicle.Variant.Land.Tracked.SpawnVehicle.Valkyra) | 1 |
| `Meta.Progression.Context.Vehicle.Faction.Friendly` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Friendly) | 2 |
| `Meta.Progression.Context.Vehicle.Faction.Hostile` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Hostile) | 2 |
| `Meta.Progression.Context.Vehicle.Faction.Neutral` | Actor Hostility Condition(AcceptedValues ETeamAttitude::Neutral) | 2 |
<!-- /statetree_tables -->

Numbers worth reading out of that table (**Data**): a sniper kill needs a kill made with one of the seven listed rifles (`MK22`, `Mosin`, `SR_04`, `SV98`, `RFB`, `SVDM`, `SKS`) at a distance of 30,000 or more (300 m); the kill-streak-stopped tag fires when a player's current-life kill count (`Analytics.Player.Kills.CurrentLife`) is greater than 6 (which player's state the tree reads is not resolved from the bindings); the crew-assist penalty tag fires when the crew count is greater than 1; the precision artillery strike needs the victim inside the Control Zone, the killer outside it and the killer in a `TNK_01.Artillery` tank or a stationary mortar. Control Zone and Hot Zone presence are tested twice in each family, once for the acting player (`Instigator.*`) and once for the target (`Target.*`), so the reward lookup can price the same kill differently inside and outside the objective.

### Hot Zone Magnet trees

The three trees under `WorldFeatures/HotZoneMagnet` are per-player trees that run on each player's challenge component when the magnet fires an event. They are the same shape as the other trees with a different gate (**Data**, generated table below).

<!-- statetree_tables magnet -->
| Tree | Event it waits for | Context tags it can add | Reward formula inputs |
|---|---|---|---|
| `KOTH_HotZoneMagnet_MagnetActivated` | `Event.StateTree.HotZoneMagnet.MagnetActivated` | `Challenges.Context.HotZoneMagnet.Instigator` | none |
| `KOTH_HotZoneMagnet_MagnetDeactivated` | `Event.StateTree.HotZoneMagnet.MagnetDeactivated` | `Challenges.Context.HotZoneMagnet.Instigator` | none |
| `KOTH_HotZoneMagnet_TowerCaptured` | `Event.StateTree.HotZoneMagnet.TowerCaptured` | `Challenges.Context.HotZoneMagnet.Instigator`, `Challenges.Context.HotZoneMagnet.Hostile` | LastVictimCount |
<!-- /statetree_tables -->

The `Populate Context` gate is four conditions joined by `And`: the player's pawn is inside the tower range of the magnet that fired (`Actor In Tower Range`, `bInsideTowerRange` true); the player's faction tag equals the faction tag of the event's `Interactor` (so only teammates of the capturing or activating player pass); the player is not `State.Player.Vitality.Critical`; and not `State.Player.Vitality.Dead`. Players who pass receive the role XP tag, and the interactor itself also gets `Challenges.Context.HotZoneMagnet.Instigator` (the tree compares its own player state with the interactor's). In the capture tree, `Challenges.Context.HotZoneMagnet.Hostile` is added when the tower had a previous owner (`PreviousFaction` is not `None`), so taking a tower from an enemy can pay differently from claiming a neutral one. The capture tree also passes the repeat count (`LastVictimCount`) for the magnet as the target, with the same 180 s window; the activation and deactivation trees have no formula inputs. The reward amounts for the three reward tags are in the shared reward tables, not in the trees.

---

## 6. Limitations
- Values for each `Challenges.Rewards.*` tag are not in this folder; they are the formula rows described in the next item.
- The structure, conditions and bindings of every state tree are decoded in section 5.1. The reward formulas are not in the trees, but they are in data: each `Challenges.Rewards.*` row in the `DT_ChallengeRewards_*` tables carries its formula, selectors and variables, and the native `Calculate Reward` task only runs it (static reading, round 88; see [Rewards and Progression](../Wardogs_Rewards_and_Progression_v2.md) section 15). `LastVictimCount`, `DistanceToTarget` and `KillStreak` are the three inputs the task always supplies (0 when no tree sets them); the other inputs listed in section 5.1 are read by name from the same table. The task that produces the repeat count (`Resolve Repeat Action Count`) was not located in code.
- A reward tag with no row in any `DT_ChallengeRewards_*` table pays nothing and raises no error. 17 of the 54 tags in the trees have none: `Assist.VehicleDestroyed`, `Assist.VehicleDestroyed.DamageAssist`, `Buildables.BuildSuppliesDeposited`, `DestroySupplyCrate`, `RepairVehicle`, `Spotting.Refreshed`, `Tip.Heal`, `Tip.PlayerDelivered`, `Tip.Refuel`, `Tip.Repair`, `Tip.Revive`, `VehicleDestroyed`, `VehicleDestroyed.Assist.CrewAssist`, `.FOBSuppliedAssist`, `.LogisticAssist`, `.ReviveAssist` and `ZoneEntry.SpawnVehicle`. Some are base tags whose variants have rows.
- `DT_Challenges_SessionEvents_KOTH` has 60 rows, but their `Rewards` and `Objectives` lists are empty. The reward amounts for each challenge are not visible from this folder.
- The `DataRegistry` action lists 13 lookup registries, but not every state tree maps to a lookup. Some trees (the families in section 3 with no `Challenges.Rewards.*` tag, or only event tags) grant no reward through a lookup, and their reward path was not traced.
- The `WDChallengeStateTreeSchema` objects carry no properties, so schema-level settings are not available.
- The conditions that add each `Challenges.Context.*` tag are decoded in section 5.1. How the reward lookup uses a tag when pricing a reward is outside the trees.
