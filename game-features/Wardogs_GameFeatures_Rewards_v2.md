---
title: "Buildable Rewards"
redirect_from: ["/Wardogs_GameFeatures_Rewards_v2.html", "/Wardogs_GameFeatures_Rewards_v2"]
parent: "Rewards & Unlocks"
description: "Buildable challenge rewards: calculator rows, feed strings, destroyed-variant lookups and the assist damage curve."
---

# Wardogs — GameFeature: Rewards (Buildables) Reference
*Extracted from cooked game data (build `++Wardogs+Live-CL-516586`, UE 5.7.4). Source: `Wardogs/Plugins/GameFeatures/Rewards/` (18 JSON files). Scripted pass over every file, then spot-checked against representative rows.*

> **Overlap with the main doc:** the flat per-structure cash values (Built / Placed / Destroyed) are in `Wardogs_Rewards_and_Progression_v2.md`, section 7. This doc covers what that doc does not: the **formula structure** of the buildable reward calculator, the **variable and modifier selectors** it uses, the **feed/UI strings** that announce each reward, the **variant-to-reward lookup** for destroyed buildables, and the **assist damage curve**.

---

## Season 02 update (2026-10-15)

- Calculator rows (`DT_ChallengeRewards_SessionEvents_Buildables`): 29 → 47. Added 18 rows: 17 destroyed-variant rows and `FOBDoorClosed`.
- New destroyed-variant rows: AirRaidShelter.Ceiling, AirRaidShelter.Floor, Bunker.Floor, Bunker.Roof, CrowsNest.BaseFloor, CrowsNest.FirstFloor, CrowsNest.Roof, Door, Door.TopSegment, Gate.Ramp, Loudspeaker, MistralAA, Mortar, Phalanx, RefuelStation, SV_Shelter, WoodBase.
- New `FOBDoorClosed` row: cash only (no XP), feed text "FOB Door Closed", new state tree `ST_Challenges_SessionEvents_Buildable_FOBDoorClosed`. State trees 10 → 11. Feed strings 11 → 12.
- Destroyed-variant lookup (`DT_RewardLookup_SessionEvent_BuildableDestroyed`): 34 → 36 rows. Door, Gate.Ramp, and the floor and roof variants now have their own reward tags instead of sharing BarbedWire, Gate or BremmerWall. WoodBase and SV_Shelter are added.
- Destroyed XP: `BaseReward` → `(BaseReward) * BuildProgress` on the 18 existing destroyed rows. The 17 new destroyed-variant rows use the new form from the start, so all 35 destroyed rows now have it.
- FOB destroyed row: adds a supplies term, with `FOBSuppliesBonus` 7500 (cash) and 250 (XP), `FOBSuppliesMax` 25000.
- `BaseValue` (cash) changes: Gate 500 → 200, RepairStation 400 → 200, HotZoneMagnet 4500 → 2750, HBlockQuadWall 150 → 75, HBlock 30 → 15, SandbagWall 30 → 15, TallHBlock 44 → 20, TankTrap 44 → 20, BarbedWire 14 → 5, CamoNetTent 14 → 5, FloorBoard 10 → 5, Radio 40 → 20, Ramp 40 → 20.
- `FOBHacked` `BaseValue`: 2500 → 1000. New `HackerValue` option (2500) on `BaseValue` for buildables owned by the player.
- New selectors: `TotalFOBSupplies`, `FOBSuppliesMax`, `FOBSuppliesBonus` (used by the FOB row).

Full before/after list: [Season 2 Changes → Rewards & Unlocks]({{ '/season-2-changes/rewards-unlocks.html' | relative_url }}).

---

## 1. Package Contents

| Export type | Count | Role |
|---|---|---|
| `GameFeatureData` (`BuildableRewards`) | 1 | Root bundle. Adds a data-registry source and a registry. |
| `StateTree` | 11 | One per buildable session event (section 3). |
| `WDChallengeStateTreeSchema` | 11 | Empty schema objects, one per state tree. |
| `DataTable` | 5 | Reward calculator (`DT_ChallengeRewards_SessionEvents_Buildables`), feed strings (`DT_ChallengesFeedActions_Building`), challenge definitions (`DT_Challenges_SessionEvents_Buildables`, **0 rows**), assist curve table, and the destroyed-variant lookup. |
| `CurveFloat` | 1 | `CRV_Challenges_Curves_BuildableDestroyedAssist_DamageFraction` (section 6). |

Files in the folder, with row counts:

| File | Rows | Row struct |
|---|---|---|
| `DT_ChallengeRewards_SessionEvents_Buildables` | 47 | `WDChallengeRewardDefinition` (calculator) |
| `DT_RewardLookup_SessionEvent_BuildableDestroyed` | 36 | `WDVariantRewardLookupRow` |
| `DT_ChallengesFeedActions_Building` | 12 | `WDRewardFeedActionDataTableRow` |
| `DT_Challenges_Curves_BuildableDestroyedAssist` | 1 | `WDLiveCurveTableRow` |
| `DT_Challenges_SessionEvents_Buildables` | 0 | `WDChallengeDefinition` |

---

## 2. How the Calculator Works

Each row of `DT_ChallengeRewards_SessionEvents_Buildables` has one or two **resources**, each a `DefaultExpression`:

- **`Attribute.Meta.Currency.Cash`**: present on all 47 rows.
- **`Attribute.Meta.XP.Role`**: present on 43 rows.

Each resource has:
- An **`ExpressionString`**: the formula, written in named variables (for example `BaseValue * AlignmentModifier`).
- **`Selectors`**: one per variable. Each selector has a `DefaultOption` and a list of `Options`. Each option has a **condition** (a tag query such as `ALL( Challenges.Context.Instigator.InHotZone )`) and a **variable name** it resolves to. The first matching option wins; otherwise the default applies.

So a formula variable is not a number in the table. It is a choice of named factor, picked at runtime from the event's context tags.

### 2a. Selector dictionary (distinct selectors across the 47 rows)

| Formula variable | Default | Options (condition → variable) | Meaning (inferred from names) |
|---|---|---|---|
| `BaseValue` | `BaseValue` | `ALL(Buildables.Dismantle, Buildables.Friendly)` → `DismantleValue`; `ALL(Context.TankKill)` → `TankValue`; `ALL(Buildables.BuildableOwner)` → `HackerValue` | Base payout. Dismantling a friendly buildable and killing a tank each use their own base. |
| `AlignmentModifier` | `DefaultModifier` | `ALL(Buildables.Friendly)` → `FriendlyModifier` | Penalty or reduction when the buildable is friendly. |
| `InstigatorZoneModifier` | `DefaultFactor` or `DefaultModifier` (varies by row) | `ALL(Instigator.InHotZone, HotZoneMagnetActive)` → `HotZoneMagnetFactor`; `ALL(Instigator.InHotZone)` → `HotZoneFactor`; `ALL(Instigator.InControlZone)` → `ControlZoneFactor` | Multiplier when the **instigator** is in a zone. Magnet is the strongest case. |
| `TargetZoneModifier` | `DefaultModifier` | `ALL(Target.InHotZone, HotZoneMagnetActive)` → `HotZoneMagnetFactor`; `ALL(Target.InHotZone)` → `HotZoneFactor`; `ALL(Target.InControlZone)` → `ControlZoneFactor` | Multiplier when the **target buildable** is in a zone. |
| `InstigatorZoneWeight` | `InstigatorFactor` | none | Weight on the instigator-side term. |
| `TargetZoneWeight` | `TargetFactor` | none | Weight on the target-side term. |
| `AssistCurve` | `DefaultModifier` | `ALL(Assist.BuildableDamage)` → `DamageAssistCurve` | Assist share, read from the damage-fraction curve (section 6). |
| `AssistScalar` | `DefaultModifier` | `ALL(Assist.BuildableDamage)` → `DamageAssistScalar` | Scalar applied to assist credit. |
| `TankReward` / `TankAssistReward` | n/a | `ALL(TankKill)`, `ALL(TankKill, Assist.BuildableDamage)` | Used by the tank-kill variants. |
| `FriendlyReward` / `DriverValue` / `FriendlyValue` | n/a | `ANY/ALL(Buildables.Friendly)` | Friendly-side payouts. |
| `HotZoneReward` / `ControlZoneReward` | n/a | `ALL(Instigator.InHotZone)` / `ALL(Instigator.InControlZone)` | Zone-specific payouts on the supply and schematic rows. |
| `SchematicOwnerValue` / `OwnerAssistReward` / `BaseReward` | n/a | `ALL(Buildables.SchematicOwner)`, `ALL(SchematicOwner, BuildableOwner)` | Owner-only payouts for the schematic path. |
| `TotalFOBSupplies`, `FOBSuppliesMax`, `FOBSuppliesBonus` | none | none | FOB supply term used by the FOB destroyed row (section 3a). |
| `DefaultValue`, `BuildProgress`, `BuildCost`, `BuildAmount`, `BaseReward`, `CashSpent`, `BuildSuppliesDeposited`, `LastVictimCount`, `LastVictimCountMax`, `LastVictimReductionModifier` | none | none | Numeric inputs. They are supplied at runtime from the event payload, not defined in these tables. |

Every condition is written as a tag query over `Challenges.Context.*` tags. Those tags are set by the state tree from the event (section 3).

**Numbers are not in these tables.** The option variables (`DismantleValue`, `HotZoneMagnetFactor`, and the rest) carry no values here. Their values are defined in the shared challenge tables, which are covered by `Wardogs_Rewards_and_Progression_v2.md`, section 15 (`DT_ChallengeRewards_SessionEvents_Shared`). This doc does not guess them.

---

## 3. Calculator Rows (47)

Each row is one challenge event. "Cash" and "XP" are the expressions in plain form.

### 3a. Destroyed buildables (`Challenges.Rewards.Buildables.BuildableDestroyed.<Structure>`, 36 rows)

All 36 rows use the **same cash expression**, except the FOB row (below). The XP expression is the same on 35 rows; the FOB row differs:

- **Cash:** `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZoneWeight * BuildProgress * AssistCurve * AssistScalar) + (BaseValue * AlignmentModifier * TargetZoneModifier * TargetZoneWeight * BuildProgress * AssistCurve * AssistScalar)`
- **XP:** `(BaseReward) * BuildProgress`

**FOB** (`BuildableDestroyed.FOB`) adds a supplies term. Its cash expression replaces `BaseValue` with `(BaseValue + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppliesMax) * FOBSuppliesBonus))` in both terms. Its XP is `(BaseReward + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppliesMax) * FOBSuppliesBonus))`.

So the destroyed payout is two terms added together: one for the **instigator's** zone position and one for the **target's** zone position, each scaled by build progress and by the assist curve. The per-structure base values are in section 2 of the main doc (section 7 there).

Structures (36 rows): FOB, AirRaidShelter, AirRaidShelter.Ceiling, AirRaidShelter.Floor, BarbedWire, BremmerWall, Bunker, Bunker.Floor, Bunker.Roof, CamoNetTent, CrowsNest, CrowsNest.BaseFloor, CrowsNest.FirstFloor, CrowsNest.Roof, Door, Door.TopSegment, FloorBoard, Gate, Gate.Ramp, HBlock, HBlockQuadWall, HotZoneMagnet, Loudspeaker, MistralAA, Mortar, Phalanx, Radio, Ramp, RefuelStation, RepairStation, SandbagWall, SV_Shelter, TallHBlock, TankTrap, WindowBoard, WoodBase.

### 3b. Other calculator rows (11)

| Row | Cash expression | XP expression |
|---|---|---|
| `BuildableDamaged` | `BaseValue * AlignmentModifier` | none |
| `Building` | `BuildAmount * BaseReward * InstigatorZoneModifier` | `BuildAmount * BaseReward` |
| `BuildableFinished` | `((BuildCost * BaseReward) * InstigatorZoneModifier) + SchematicOwnerModifier` | `BuildCost * BaseReward` |
| `SchematicPlaced` | `DefaultValue * InstigatorZoneModifier` | none |
| `BuildSuppliesDeposited.Owner` | `DefaultValue * BuildSuppliesDeposited * InstigatorZoneModifier` | `BaseReward * BuildSuppliesDeposited * InstigatorZoneModifier` |
| `BuildSuppliesDeposited.Interactor` | `DefaultValue * BuildSuppliesDeposited * InstigatorZoneModifier` | `BaseReward * BuildSuppliesDeposited * InstigatorZoneModifier` |
| `BuildSuppliesConsumed.Owner` | `DefaultValue * BuildSuppliesDeposited * InstigatorZoneModifier` | `BaseReward * BuildSuppliesDeposited * InstigatorZoneModifier` |
| `BuildSuppliesConsumed.Instigator` | `DefaultValue * InstigatorZoneModifier` | `(BaseReward)` |
| `FOBOwnerPayed` | `DefaultValue * CashSpent` | none |
| `FOBHacked` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseValue * InstigatorZoneModifier)` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseValue)` |
| `FOBDoorClosed` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseValue * InstigatorZoneModifier)` | none |

Notes:
- `FOBHacked` uses the **last victim** reduction, so repeated hacks of the same owner pay less. The reduction is `clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier`, subtracted from 1.
- `BuildableFinished` adds `SchematicOwnerModifier` as a flat term, so the schematic owner gets a flat bonus on completion.
- `BuildSuppliesConsumed.Owner` and `.Instigator` differ. The owner row scales cash and XP by `BuildSuppliesDeposited`, the instigator row does not.
- `BuildableDamaged`, `SchematicPlaced`, `FOBOwnerPayed` and `FOBDoorClosed` have **no XP resource**. That accounts for 4 of the 47 rows, leaving the 43 rows with XP.

### 3c. Assist entry without a calculator row

The feed table has a `Challenges.Rewards.Buildables.BuildableDestroyed.Assist` entry ("Buildable Destroyed Assist", section 4). **There is no matching calculator row** in `DT_ChallengeRewards_SessionEvents_Buildables`. The assist credit appears to come through the `AssistCurve` and `AssistScalar` selectors inside the destroyed rows instead. This is an inference from the table layout, not a verified path.

---

## 4. Feed Strings (`DT_ChallengesFeedActions_Building`, 12 rows)

These are the messages shown in the reward feed, and the audio event each one plays. Strings come from `/Game/UI/StringTables/STRINGS_ChallengesRewardFeed`.

| Feed tag | Display string | Audio event |
|---|---|---|
| `BuildableDamaged` | Buildable Damaged | none |
| `BuildableDestroyed` | Buildable Destroyed | `Audio.Event.UX.Cash.RevivedScore` |
| `BuildableDestroyed.Assist` | Buildable Destroyed Assist | `Audio.Event.UX.Cash.BuiltScore` |
| `Building` | Building | none |
| `BuildableFinished` | Building Complete | `Audio.Event.UX.Cash.HealedScore` |
| `SchematicPlaced` | Build Schematic Placed | none |
| `BuildSuppliesDeposited` | Supplies Deposited | `Audio.Event.UX.Cash.HotzoneReward` |
| `BuildSuppliesConsumed.Owner` | Supplies Used | none |
| `BuildSuppliesConsumed.Instigator` | Supplies Consumed | none |
| `FOBOwnerPayed` | FOB Resources Used | none |
| `FOBHacked` | FOB Hacked | `Audio.Event.UX.Cash.RevivedScore` |
| `FOBDoorClosed` | FOB Door Closed | `Audio.Event.UX.Cash.HealedScore` |

Two of these rows have a `ConditionalExpressions` entry: `BuildableDamaged` and `BuildableDestroyed` show different text when the buildable is friendly (`ANY(Challenges.Context.Buildables.Friendly)`).

Note: `BuildSuppliesConsumed.Instigator` has a localisation key that reads `...BuildSuppliesConsumed.Repair` while its feed tag is `...BuildSuppliesConsumed.Instigator`. The text is correct, but the key name does not match the tag.

---

## 5. Destroyed-Variant Lookup (`DT_RewardLookup_SessionEvent_BuildableDestroyed`, 36 rows)

Maps each **placed buildable variant** to the **reward tag** that the destroyed calculator (section 3a) uses. Every variant has its own reward tag.

| Reward tag | Variants | Notes |
|---|---|---|
| `BuildableDestroyed.FOB` | 1 | `Id.Buildable.FOB` |
| `BuildableDestroyed.AirRaidShelter` | 1 | `Id.Buildable.AirRaidShelter` |
| `BuildableDestroyed.AirRaidShelter.Ceiling` | 1 | `Id.Buildable.AirRaidShelter.Ceiling` |
| `BuildableDestroyed.AirRaidShelter.Floor` | 1 | `Id.Buildable.AirRaidShelter.Floor` |
| `BuildableDestroyed.BarbedWire` | 1 | `Id.Buildable.BarbedWire` |
| `BuildableDestroyed.BremmerWall` | 1 | `Id.Buildable.BremmerWall` |
| `BuildableDestroyed.Bunker` | 1 | `Id.Buildable.Bunker` |
| `BuildableDestroyed.Bunker.Floor` | 1 | `Id.Buildable.Bunker.Floor` |
| `BuildableDestroyed.Bunker.Roof` | 1 | `Id.Buildable.Bunker.Roof` |
| `BuildableDestroyed.CamoNetTent` | 1 | `Id.Buildable.CamoNetTent` |
| `BuildableDestroyed.CrowsNest` | 1 | `Id.Buildable.CrowsNest` |
| `BuildableDestroyed.CrowsNest.BaseFloor` | 1 | `Id.Buildable.CrowsNest.BaseFloor` |
| `BuildableDestroyed.CrowsNest.FirstFloor` | 1 | `Id.Buildable.CrowsNest.FirstFloor` |
| `BuildableDestroyed.CrowsNest.Roof` | 1 | `Id.Buildable.CrowsNest.Roof` |
| `BuildableDestroyed.Door` | 1 | `Id.Buildable.Door` |
| `BuildableDestroyed.Door.TopSegment` | 1 | `Id.Buildable.Door.TopSegment` |
| `BuildableDestroyed.FloorBoard` | 1 | `Id.Buildable.FloorBoard` |
| `BuildableDestroyed.Gate` | 1 | `Id.Buildable.Gate` |
| `BuildableDestroyed.Gate.Ramp` | 1 | `Id.Buildable.Gate.Ramp` |
| `BuildableDestroyed.HBlock` | 1 | `Id.Buildable.HBlock` |
| `BuildableDestroyed.HBlockQuadWall` | 1 | `Id.Buildable.HBlockQuadWall` |
| `BuildableDestroyed.HotZoneMagnet` | 1 | `Id.Buildable.HotzoneMagnet` |
| `BuildableDestroyed.Loudspeaker` | 1 | `Id.Buildable.Loudspeaker` |
| `BuildableDestroyed.MistralAA` | 1 | `Id.Buildable.MistralAA` |
| `BuildableDestroyed.Mortar` | 1 | `Id.Buildable.Mortar` |
| `BuildableDestroyed.Phalanx` | 1 | `Id.Buildable.Phalanx` |
| `BuildableDestroyed.Radio` | 1 | `Id.Buildable.Radio` |
| `BuildableDestroyed.Ramp` | 1 | `Id.Buildable.Ramp` |
| `BuildableDestroyed.RefuelStation` | 1 | `Id.Buildable.RefuelStation` |
| `BuildableDestroyed.RepairStation` | 1 | `Id.Buildable.RepairStation` |
| `BuildableDestroyed.SandbagWall` | 1 | `Id.Buildable.SandbagWall` |
| `BuildableDestroyed.SV_Shelter` | 1 | `Id.Buildable.SV_Shelter` |
| `BuildableDestroyed.TallHBlock` | 1 | `Id.Buildable.TallHBlock` |
| `BuildableDestroyed.TankTrap` | 1 | `Id.Buildable.TankTrap` |
| `BuildableDestroyed.WindowBoard` | 1 | `Id.Buildable.WindowBoard` |
| `BuildableDestroyed.WoodBase` | 1 | `Id.Buildable.WoodBase` |

Three things to note:
- The Door (`Id.Buildable.Door`) and the gate ramp (`Id.Buildable.Gate.Ramp`) each have their own reward tag and their own calculator row. They no longer share the Gate or BremmerWall payout.
- The table has 36 rows and 36 reward tags. Each tag maps to one calculator row in section 3a, so each variant has its own payout.
- `Id.Buildable.Door.TopSegment` and the AirRaidShelter, Bunker and CrowsNest floor and roof pieces each have their own tag, separate from BarbedWire.

---

## 6. Assist Damage Curve

| Item | Value |
|---|---|
| Table | `DT_Challenges_Curves_BuildableDestroyedAssist` (1 row) |
| Live curve tag | `LiveCurves.Challenges.SessionEvents.BuildableDestroyedAssist.DamageFraction` |
| Curve asset | `CRV_Challenges_Curves_BuildableDestroyedAssist_DamageFraction` |
| Interpolation | Linear |
| Keys | (time 0.0, value 0.0) and (time 1.0, value 1.0) |
| Default value | 0.0 |

So the curve is a straight line from 0 to 1 over the input range. The input is not named in these files. The most likely reading is that the input is the fraction of a buildable's health the assisting player damaged, so an assist that removes a bigger share of the buildable's health earns a bigger share of the reward. That reading is not confirmed by the data.

The curve is wired to `AssistCurve` through the `DamageAssistCurve` option (section 2a).

---

## 7. Limitations

- **No numeric reward values in this folder.** The calculator uses option variables (`DismantleValue`, `HotZoneMagnetFactor`, `ControlZoneFactor`, `BaseReward`, `DefaultValue`, and so on). Their values are defined outside this folder, in the shared challenge tables covered by the main doc. This doc names them but does not give values.
- **Input sources and ranges need tracing.** The producers and ranges of `BuildProgress`, `BuildCost`, `BuildAmount`, `CashSpent`, `BuildSuppliesDeposited` and `LastVictimCount` are not established here. `LastVictimCountMax` is a configured literal of 2.0 in all three variable definitions in `DT_ChallengeRewards_SessionEvents_Buildables`, rather than an unknown event input in those definitions. See [runtime triage RT-015](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/gap_resolution/RUNTIME.md).
- **The assist path is inferred.** No `BuildableDestroyed.Assist` calculator row exists (section 3c). The assist credit is assumed to flow through `AssistCurve` and `AssistScalar`.
- **The `Repair` key mismatch** in section 4 is a localisation quirk, not a gameplay issue. It was not checked in-game.
- **The buildable challenge definitions table** `DT_Challenges_SessionEvents_Buildables` has zero rows. The active buildable challenge list is not visible from this folder.
- **The 11 state trees** (`ST_Challenges_SessionEvents_Buildable_*`) are compiled StateTree bytecode. This doc names them (BuildableDamaged, BuildableDestroyed, BuildableDestroyed_Assist, Building, BuildingFinished, BuildSuppliesConsumed, BuildSuppliesDeposited, FOBDoorClosed, FOBHacked, FOBOwnerPayed, SchematicPlaced) but does not decode their states.
- For the per-structure **cash base values**, see `Wardogs_Rewards_and_Progression_v2.md`, section 7. Modifier values for the zone factors are in section 15 of the same doc.
