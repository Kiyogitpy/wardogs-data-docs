# Wardogs — GameFeature: Challenges_KOTH Reference (v2)
*Extracted from cooked game data via CUE4Parse (build `++Wardogs+Live-CL-509546`, UE 5.7.4). Source: `Wardogs/Plugins/GameFeatures/Challenges_KOTH/` (75 JSON files). Scripted pass over every file, then spot-checked against representative files.*

> **Scope note:** this folder holds the **wiring** for the KOTH challenge set: which state tree runs for which session event, which reward tag it grants, and which lookup table turns a vehicle/item variant into a reward tag. The **reward values** (cash, XP) live in the shared challenge tables outside this folder. See `Wardogs_Rewards_and_Progression_v2.md` (sections 10, 13, 15) and the sibling doc `Wardogs_GameFeatures_Rewards_v2.md`.

---

## 1. What the Package Contains

| Export type | Count | Role |
|---|---|---|
| `GameFeatureData` (`Challenges_KOTH`) | 1 | Root bundle. Two actions. |
| `GameFeatureAction_DataRegistrySource` | 1 | Adds `DT_Challenges_SessionEvents_KOTH` as a source to the `Challenges` registry (client and server). |
| `GameFeatureAction_DataRegistry` | 1 | Adds 13 lookup registries (`DR_SessionEvent_*`). |
| `StateTree` | 60 | One state tree per session event or assist variant (section 3). |
| `WDChallengeStateTreeSchema` | 60 | One schema object per state tree. All are empty (no properties). |
| `DataTable` | 14 | 1 challenge-definition table (**0 rows**) plus 13 reward lookup tables (section 4). |

The `DT_Challenges_SessionEvents_KOTH` table has `RowStruct = WDChallengeDefinition` and **no rows**. The challenge definitions for this set are not stored in this folder.

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

Families by event. State counts are the number of states in each tree (range **10 to 35**).

| Family | Trees | Event tag root | Reward tags referenced by the tree |
|---|---|---|---|
| Player kill (direct) | 6 | `Event.StateTree.PlayerKill[.CrewAssist / .FOBSuppliedAssist / .LogisticAssist / .ReviveAssist / .SupplyCrateAssist]` | Analytics tags only (kill counters). Values resolved elsewhere. |
| Player kill (assist) | 6 | `Event.StateTree.KillAssist[.<assist type>]` | `Analytics.Player.Assists` |
| Destroy vehicle | 12 | `Event.StateTree.DestroyVehicle[.Assist[.<type>] / .<assist type>]` | `Challenges.Rewards.VehicleDestroyed` and the `.FOBSuppliedAssist`, `.LogisticAssist`, `.ReviveAssist` variants |
| Destroy vehicle section | 10 | `Event.StateTree.DestroyVehicleSection[.Assist][.<assist type>]` | Event tags only in the list pass |
| Destroy supply crate | 1 | `Event.StateTree.DestroySupplyCrate` | `Challenges.Rewards.DestroySupplyCrate.Free` |
| Heal player | 4 | `Event.StateTree.HealPlayer[.LogisticAssist / .ReviveAssist / .SupplyCrateAssist]` | `Challenges.Rewards.HealPlayer`, `.Tip.Heal` (base tree), plus `.LogisticAssist` and `.ReviveAssist` variants |
| Revive player | 5 | `Event.StateTree.RevivePlayer[.Contributor / .LogisticAssist / .ReviveAssist / .SupplyCrateAssist]` | `Challenges.Rewards.RevivePlayer`, `.Tip.Revive` (base tree), plus variants |
| Repair / refuel vehicle | 2 | `Event.StateTree.RepairVehicle`, `Event.StateTree.RefuelVehicle` | `Challenges.Rewards.Tip.Repair`, `Challenges.Rewards.Tip.Refuel` |
| Player delivered / passenger | 2 | `Event.StateTree.PlayerDelivered`, `Event.StateTree.PassengerSurvived` | `Challenges.Rewards.Tip.PlayerDelivered` (delivery tree only) |
| Supply crate purchase / deploy | 3 | `Event.StateTree.PurchaseFromSupplyCrate`, `Event.StateTree.DeployOnVehicle`, `Event.StateTree.DeploySupplyCrate` | Event tags only |
| Throwables, pallets, air time | 4 | `Event.StateTree.DestroyThrowable`, `.SupplyPalletDropped`, `.VehicleAirborne`, `.VehicleFlyThrough` | Event tags only |
| Zone and tips | 4 | `Event.StateTree.SafeZoneEntered`, `.ZoneEntry`, `.PreTip`, `.Tip` | Event tags only |
| Test | 1 | `Event.StateTree.Test` | None |

Notes:
- The "Event tags only" entries reference no `Challenges.Rewards.*` tag in the aggregated pass. Their reward path is either absent or resolved through a shared table. This was not traced per state.
- The `Event.StateTree.*` tags are how the game routes an event to its tree. The mapping from in-game action to event tag is not in this folder.

### 3a. Sampled tree: `ST_Challenges_SessionEvents_KOTH_PlayerKill_Assist_CrewAssist` (13 states)

`Root` → `Wait For Player Kill Assist Crew Assist Event` → `On Player Kill Assist Crew Assist Event` → `Populate Context` → `Populate Reward XP Tags` → `Add Role XP Tag To Context` → `Transfer Context from Event` → `Add Crew Assist To Context Tags` → `IncrementMatchStat` → `Calculate Reward` → `Update Reward XP Tags` → `Grant Reward` → `Complete When Done`

Tags present: `Event.StateTree.KillAssist.CrewAssist`, `Analytics.Player.Assists`, `State.Player.Vitality.Critical`.

---

## 4. Reward Lookup Tables (13 tables, 175 rows)

Each row maps a **variant tag** (the specific vehicle, item or buildable variant) to a **reward tag**. Row names and the `Tag` column are the variant. The `RewardTag` column is what the state tree grants.

| Lookup table | Rows | Maps to (reward tag family) | Examples |
|---|---|---|---|
| `DT_RewardLookup_SessionEvent_DestroyVehicle` | 30 | `Challenges.Rewards.VehicleDestroyed.<Vehicle>` | Kodiak (3 variants), LittleBird (3), Huey (2), Blackhawk (2), SpawnVehicle (3), TNK_01.Heavy, Bobcat, Humvee (3), DuneBuggy, Ural (3), Loudspeaker, MistralAA, Mortar (2), Phalanx |
| `DT_RewardLookup_SessionEvent_DestroyVehicleSection` | 24 | `Challenges.Rewards.DestroyVehicleSection.<Vehicle>` | Same vehicle families as above, section-based |
| `DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist` | 24 | `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist.<Vehicle>` | Blackhawk, TNK_01.Artillery, Humvee, and others |
| `DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist` | 24 | `Challenges.Rewards.VehicleDestroyed.LogisticAssist.<Vehicle>` | Havoc, TNK_01.AntiAir, Humvee, and others |
| `DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist` | 24 | `Challenges.Rewards.VehicleDestroyed.ReviveAssist.<Vehicle>` | Same family pattern as above |
| `DT_RewardLookup_SessionEvent_DestroySupplyCrate` | 10 | `Challenges.Rewards.DestroySupplyCrate.<Size>` | Free (2 variants), Small, Small.Armoured, Large, Large.Armoured, Pallet (4 pallet types: BuildSupply, FuelSupply, MunitionsSupply, SparePartsSupply) |
| `DT_RewardLookup_SessionEvent_HealPlayer` | 6 | `Challenges.Rewards.HealPlayer.<Item>` | Bandage, SuperBandage, MedKit, StimPen, AdrenalinePen, Defibrillator |
| `DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist` | 6 | `Challenges.Rewards.HealPlayer.LogisticAssist.<Item>` | Same six items |
| `DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist` | 6 | `Challenges.Rewards.HealPlayer.ReviveAssist.<Item>` | Same six items |
| `DT_RewardLookup_SessionEvent_RevivePlayer` | 6 | `Challenges.Rewards.RevivePlayer.<Item>` | Defibrillator, StimPen, AdrenalinePen and others |
| `DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist` | 6 | `Challenges.Rewards.RevivePlayer.LogisticAssist.<Item>` | Defibrillator, StimPen, AdrenalinePen, MedKit |
| `DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist` | 6 | `Challenges.Rewards.RevivePlayer.ReviveAssist.<Item>` | StimPen, AdrenalinePen, MedKit, Resuscitator (2 variants) |
| `DT_RewardLookup_SessionEvent_RepairVehicle` | 3 | `Challenges.Rewards.RepairVehicle.<Tool>` | Wrench.Standard, Drill.Light, Drill.Heavy |

Observations:
- Heal and revive lookups map a **consumable item** to a reward tag. The item tags are `Id.Item.*` (for example `Id.Item.MedKit.Standard`, `Id.Item.Defibrillator.Standard`).
- Repair lookups map a **tool** to a reward tag. Tool tags are `ID.Item.RepairTool.*`.
- Several vehicle families map **multiple variants to one reward tag** (for example Kodiak Default, MachineGun and Pickup all grant `VehicleDestroyed.Kodiak`). The payout is per vehicle type, not per variant.
- Row names and `Tag` columns are not always spelled identically. The revive lookups use `Defibrilator` in some row keys and `Medkit` in some row keys, while the `Tag` column is `Id.Item.Defibrillator.Standard` and `Id.Item.MedKit.Standard`. The `Tag` column is what the game uses to match. This was verified on the RevivePlayerLogisticAssist table.
- Across all 13 tables there are **112 distinct `Challenges.Rewards.*` reward tags** referenced by the lookups.

---

## 5. Reward Values

**Not in this folder.** The KOTH state trees grant reward tags, but the cash and XP amounts for those tags are defined in the shared challenge reward table (`DT_ChallengeRewards_SessionEvents_Shared`, under `Content/Meta/Challenges/`), which the existing v2 doc covers in section 15. Use that section for the per-kill and per-event calculator, and section 10 for end-of-match rewards.

---

## 6. Limitations
- Values for each `Challenges.Rewards.*` tag are not resolved in this doc. They live outside the folder.
- Per-state logic (the actual calculation in `Calculate Reward`) is compiled StateTree bytecode. This doc names states and tags but does not decode the expressions.
- `DT_Challenges_SessionEvents_KOTH` (challenge definitions) has zero rows here, so the list of active challenges for KOTH mode is not visible from this folder.
- The `DataRegistry` action lists 13 lookup registries, but not every state tree maps to a lookup. Some (the "Event tags only" trees in section 3) grant no reward through a lookup, and their reward path was not traced.
- The `WDChallengeStateTreeSchema` objects carry no properties, so schema-level settings are not available.
- The meaning of `Challenges.Context.*` tags is inferred from their names. Their runtime values were not checked.
