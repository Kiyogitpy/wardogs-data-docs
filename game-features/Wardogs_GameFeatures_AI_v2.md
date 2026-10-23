---
title: "AI (feature)"
redirect_from: ["/Wardogs_GameFeatures_AI_v2.html", "/Wardogs_GameFeatures_AI_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Core AI Preset, Alert State Thresholds, Influence Maps"
---

# Wardogs — GameFeatures: AI
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/AI/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/AI) — 39 JSON files. Each file was parsed as a sequence of `--- export:` blocks; the first block is the asset, later blocks are sub-objects (EQS options, tests, generators, data providers, goals). Values below are raw export values.*

---

## 1. What This Folder Holds

The AI folder is the PvE AI stack plus several example/test feature packs. It is organised as ten feature folders and contains three kinds of data:

1. **Core config** in `WDAIPvEAICore/` — the character AI preset, alert-state thresholds, influence-map settings, the blackboard, and the smart-object/action definitions that the rest of the game references.
2. **Behaviour content** — goal classes (`BHGameFeatureAction_AddGoal`) and Environment Queries (EQS) used by the behaviours.
3. **Example packs** (`*Example`, `Behavior_*`, [`BesiegeExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/BesiegeExample/Content/BesiegeExample.json), [`CoverExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/CoverExample/Content/CoverExample.json), [`SmartObjectExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SmartObjectExample/Content/SmartObjectExample.json), [`AINavigation_Example`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/AINavigation_Example/Content/AINavigation_Example.json)) — these are GameFeature packs with EQS and goals. The dump does not say whether they ship in the live build; treat them as example/test content unless a live reference is found.

| Metric | Value |
|---|---|
| Files | 39 |
| GameFeatureData assets (across all files, including sub-exports) | 10 |
| EQS query assets (`EQS_*.json` with an EnvQuery or equivalent root) | 22 |
| Blackboard assets | 1 ([`BB_PVEAI`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BB_PVEAI.json)) |
| Behaviour goals | 4 |
| Smart-object / action definitions | 2 |

### 1a. Subfolder breakdown

| Subfolder | Files | Contents |
|---|---|---|
| `WDAIPvEAICore/` | 16 | Core AI: [`DefaultAIPreset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DefaultAIPreset.json), [`BB_PVEAI`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BB_PVEAI.json), alert thresholds, influence data, influence-map config, [`EQS_FindTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/EQS/EQS_FindTarget.json), 8 cover/position EQS, 2 action defs, the core GFD |
| `Behavior_Besiege/` | 7 | GFD + 6 besiege EQS (cover and point search around a besiege target) |
| `SquadExample/` | 4 | GFD + goal `Goal_Example_AttackPlayer` + 3 squad EQS (closest cover, cover toward goal, leap-frog token handling) |
| `Behavior_Patrol/` | 3 | GFD + goal `Goal_Patrol` + 2 patrol-point EQS |
| `Behavior_Search/` | 2 | GFD + goal `Goal_Search` + 1 EQS [`EQS_FindSearchLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/EQS/EQS_FindSearchLocation.json) |
| `Behaviour_Example/` | 2 | GFD + goal `Goal_Example_Flee` + 1 EQS flee point |
| `CoverExample/` | 2 | GFD + [`EQS_FindRandomPeekPoint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/CoverExample/Content/EQS_FindRandomPeekPoint.json) |
| `AINavigation_Example/` | 1 | GFD with `BH.AISpawn` scan rule (`WDAICharacterConfigData`) |
| `BesiegeExample/` | 1 | GFD only (no actions) |
| `SmartObjectExample/` | 1 | GFD only (no actions) |

---

## 2. Core AI Preset ([`WDAIPvEAICore/Content/DefaultAIPreset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DefaultAIPreset.json))

This is the `WDAICharacterConfigData` that the PvE configs in the PvE folder follow. Its fields define the AI character baseline.

| Field | Value |
|---|---|
| AICharacterClass | `B_WDCore_MoverPlayerCharacter_C` (WDCore) |
| AIControllerClass | `BP_CoreAIController_C` |
| FireModePriority | Burst > Automatic > SemiAutomatic |
| FactionTag | `Meta.Alignment.Faction.Bravo` |
| AIInventory | `Id.Item.AK74M` ×1 |
| BehaviorTree | `BT_WDAIPvECore_Base` |
| AlertStatesWithThreashold | [`AlertStateThreashold_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AlertStateThreashold_DataConfig.json) |
| AIInfluenceDataAsset | [`AIInfluence_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AIInfluence_DataConfig.json) |

(The asset name spells "Threashold" as in the source; keep the spelling when searching.)

---

## 3. Alert State Thresholds ([`AlertStateThreashold_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AlertStateThreashold_DataConfig.json))

| Alert state | LowerThreshold | Require sight to go up from lower | Require sight to go down from higher |
|---|---|---|---|
| `EWDAIAlertState::Relaxed` | 0.0 | false | false |
| `EWDAIAlertState::Alert` | 0.8 | false | false |
| `EWDAIAlertState::Combat` | 1.0 | **true** | false |

**Meaning:** The threshold is compared against a continuous value. The blackboard has a `Pressure` key, which is the likely input, but the export does not say so explicitly. This is an inference.

---

## 4. Influence Maps

### 4a. Influence data ([`AIInfluence_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AIInfluence_DataConfig.json), type `WDAIInfluenceData`)

| Influence tag | Radius | Strength |
|---|---|---|
| `InfluenceMap.TeamMap` | 1000.0 | 1.0 |
| `InfluenceMap.EnemyMap` | 500.0 | 1.0 |
| `InfluenceMap.AlertMap` | 1000.0 | 1.0 |

`SensesToUseForAlertMap`: `AISense_Hearing` — hearing feeds the alert map.

### 4b. Influence-map config ([`WDInfluenceConfigData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/InfluenceMap/WDInfluenceConfigData.json), type `SDInfluenceMapConfigDataAsset`)

| Map | DecayPercentagePerSecond | UpdateFrequency (s) | PropagateInfluence | EvaluationType | CreateArea | CheckPathExistToAreaID | RemoveEvaluation |
|---|---|---|---|---|---|---|---|
| `TeamMap` | 10.0 | 5.0 | true | NavRaycast | false | false | None |
| `EnemyMap` | 10.0 | 2.0 | true | None | false | false | None |
| `AlertMap` | 1.0 | 0.5 | false | None | **true** | **true** | NavRaycast |

`AIPawnClass`: `B_WDCore_MoverPlayerCharacter_C`. Debug is off on all three maps.

---

## 5. Blackboard ([`BB_PVEAI`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BB_PVEAI.json))

13 keys. The types come from the sub-exports (Bool, Enum `EWDAIAlertState`, Object/Actor, Vector).

| # | Key | Notes |
|---|---|---|
| 1 | HasLineOfSight | Bool, default `true` |
| 2 | MoveGoal | Vector |
| 3 | SelfActor | Object |
| 4 | TargetActor | Object |
| 5 | Pressure | Float-like driver of alert state (inferred) |
| 6 | HasTeleportedToAO | Bool |
| 7 | Cover | Object, with EQS context `EQS_Context_TargetEnemy` in some sub-exports |
| 8 | PeekPoint | Vector |
| 9 | SOClaimHande | Smart-object claim handle. The spelling is in the source. |
| 10 | GoalActor | Object |
| 11 | LastAlertState | Enum `EWDAIAlertState` |
| 12 | TargetAreaId | Int-like area id |
| 13 | AlertInterruptible | Bool |

---

## 6. Goals (`BHGameFeatureAction_AddGoal`)

Goal purposes are inferred from class names and folder EQS; the goal logic is not in this folder.

| Goal class | Source file | Notes |
|---|---|---|
| `Goal_Patrol_C` | [`Behavior_Patrol/Content/Behavior_Patrol.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Patrol/Content/Behavior_Patrol.json) | Patrol (inferred from name; folder EQS [`EQS_PatrolPoint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Patrol/Content/EQS/EQS_PatrolPoint.json)) |
| `Goal_Search_C` | [`Behavior_Search/Content/Behavior_Search.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/Behavior_Search.json) | Search (inferred from name; folder EQS [`EQS_FindSearchLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/EQS/EQS_FindSearchLocation.json)) |
| `Goal_Example_Flee_C` | [`Behaviour_Example/Content/Behaviour_Example.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behaviour_Example/Content/Behaviour_Example.json) | Flee (inferred from name; folder EQS [`EQS_FindFleePointFromGoalTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behaviour_Example/Content/EQS/EQS_FindFleePointFromGoalTarget.json)) |
| `Goal_Example_AttackPlayer_C` | [`SquadExample/Content/SquadExample.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SquadExample/Content/SquadExample.json) | Attack-player example (inferred from name) |

---

## 7. Actions and Smart Objects

| Asset | Type | Tag / context | Action class |
|---|---|---|---|
| [`DA_Action_AIIdle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Actions/DA_Action_AIIdle.json) | BHActionDefinition | `Action.Player.Idle`; contexts TwoHanded, Holdable | `B_Action_AIIdle_C` |
| [`DA_Action_UseComputer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/SmartObject/UseComputer/DA_Action_UseComputer.json) | BHActionDefinition | `Action.SmartObject.UseComputer`; contexts Interaction, TwoHanded, Holdable; activation context `WDSmartObjectActionContext` | `B_Action_UseComputer_C` |

The [`WDAIPvEAICore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/WDAIPvEAICore.json) GFD scans `BH.Action` in [`/SmartObject/UseComputer`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/SmartObject/UseComputer) and `/WDAIPvEAICore/Actions`.

---

## 8. Components Added by the Core GFD ([`WDAIPvEAICore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/WDAIPvEAICore.json))

Feature actions in [`WDAIPvEAICore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/WDAIPvEAICore.json) (from `GameFeatureAction_AddComponents`):

| Host actor | Component added | Module |
|---|---|---|
| `WDGameState` | `WDAIPvEGameStateComponent` | WDAIPvEAICoreRuntime |
| `WDGameMode` | `SDAIRuleManagerComponent` | SDAIRules |
| Player character (`B_WDCore_MoverPlayerCharacter`) | `SDAISmartObjectActorComponent` | SDUESmartObject |
| Player character | `BP_PlayerCharacterDetectabilityComponent` | WDAIPvEAICore |
| Player character | `WDAISightTargetComponent` | WDAIPvEAICoreRuntime |
| `BP_CoreAIController` | `WDAITetherComponent` | WDAIPvEAICoreRuntime |
| `BHBaseVehiclePawn` | `WDVehicleDetectabilityComponent` | WDAIPvEAICoreRuntime |

It also activates `SDGameFeatureAction_ActivateSubsystem`.

---

## 9. EQS Catalogue

22 query assets. Purpose is inferred from the file name and the tests. The "Tests" column lists the test or generator classes with counts across the query's options.

| Query | Folder | Generator | Main tests | Purpose (inferred) |
|---|---|---|---|---|
| [`EQS_FindTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/EQS/EQS_FindTarget.json) | WDAIPvEAICore | WDEnvQueryGenerator_ThreatActors ×3 | GameplayTags ×3 | Pick a target from threats |
| [`EQS_FindCoverNearby`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindCoverNearby.json) | WDAIPvEAICore/Cover | SDEnvQueryGenerator_Covers | Distance ×2, Dot, AIConfigData provider | Nearby cover |
| [`EQS_FindCoverCloserToEnemy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindCoverCloserToEnemy.json) | WDAIPvEAICore/Cover | SDEnvQueryGenerator_Covers, Composite provider | WeaponData ×4, Distance ×3, Dot, PathfindingBatch, WDEnvQueryTest_CoverTrace | Cover that closes on the enemy |
| [`EQS_FindCoverTowardsEnemy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindCoverTowardsEnemy.json) | WDAIPvEAICore/Cover | SDEnvQueryGenerator_Covers | Distance ×3, Dot, Pathfinding, Distance provider | Cover facing the enemy |
| [`EQS_FindBestPeekPointOfCurrentCover`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindBestPeekPointOfCurrentCover.json) | WDAIPvEAICore/Cover | SDEnvQueryGenerator_PeekPoints | WDEnvQueryTest_CoverTrace | Peek point off current cover |
| [`EQS_FindPeekPointToStimulus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindPeekPointToStimulus.json) | WDAIPvEAICore/Cover | SDEnvQueryGenerator_PeekPoints | — | Peek toward a stimulus |
| [`EQS_FindCombatPositionCloserToTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindCombatPositionCloserToTarget.json) | WDAIPvEAICore/Cover | Donut | Distance ×2, Pathfinding, WeaponData ×2, Composite, Distance provider | Combat position |
| [`EQS_FindShootPositionInTheOpen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/Cover/EQS/EQS_FindShootPositionInTheOpen.json) | WDAIPvEAICore/Cover | Donut | WeaponData ×3, Distance ×2, Pathfinding, Trace, AgentHeight provider | Open-ground shot position |
| [`EQS_BesiegeTakeOverMovementTokenHandling`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/EQS/EQS_BesiegeTakeOverMovementTokenHandling.json) | Behavior_Besiege | SDEnvQueryGenerator_TokenRequests | WDEnvQueryTest_InfluenceMapValue | Movement tokens during besiege takeover |
| [`EQS_FindCoverInBesiegeArea`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/EQS/EQS_FindCoverInBesiegeArea.json) | Behavior_Besiege | SDEnvQueryGenerator_Covers | Distance, Dot, PathfindingBatch, Volume, InfluenceMapValue, VolumeSize provider | Cover inside besiege volume |
| [`EQS_FindCoverInBesiegeAreaClosest`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/EQS/EQS_FindCoverInBesiegeAreaClosest.json) | Behavior_Besiege | SDEnvQueryGenerator_Covers | Distance ×2, PathfindingBatch, Volume, VolumeSize provider | Nearest cover inside besiege volume |
| [`EQS_FindCoverTowardBesiegeTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/EQS/EQS_FindCoverTowardBesiegeTarget.json) | Behavior_Besiege | SDEnvQueryGenerator_Covers | Distance ×2, Dot, PathfindingBatch, Volume, SDAIGoalDataProvider_Target | Cover toward besiege target |
| [`EQS_FindPointAroundBesiegeTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/EQS/EQS_FindPointAroundBesiegeTarget.json) | Behavior_Besiege | Donut | Distance ×2, PathfindingBatch, Volume | Ring points around besiege target |
| [`EQS_FindPointCloseToBesiegeTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/EQS/EQS_FindPointCloseToBesiegeTarget.json) | Behavior_Besiege | Donut | Distance ×2, PathfindingBatch | Points close to besiege target |
| [`EQS_PatrolPoint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Patrol/Content/EQS/EQS_PatrolPoint.json) | Behavior_Patrol | ProjectedLocation | Distance ×2, PathfindingBatch | Patrol point |
| [`EQS_PatrolPoint_Follower`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Patrol/Content/EQS/EQS_PatrolPoint_Follower.json) | Behavior_Patrol | Donut | Distance, PathfindingBatch | Patrol point for a follower |
| [`EQS_FindFleePointFromGoalTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behaviour_Example/Content/EQS/EQS_FindFleePointFromGoalTarget.json) | Behaviour_Example | Donut | Distance | Flee point |
| [`EQS_FindSearchLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/EQS/EQS_FindSearchLocation.json) | Behavior_Search | BP_InfluenceEvaluator_AlertLocationGenerator | Dot, Pathfinding, Covers | Search location from alert data |
| [`EQS_FindRandomPeekPoint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/CoverExample/Content/EQS_FindRandomPeekPoint.json) | CoverExample | SDEnvQueryGenerator_PeekPoints | — | Random peek point (example) |
| [`EQS_FindClosestCoverToQuerier`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SquadExample/Content/EQS/EQS_FindClosestCoverToQuerier.json) | SquadExample | SDEnvQueryGenerator_Covers | Distance, Dot, Pathfinding | Closest cover (squad example) |
| [`EQS_FindCoverTowardGoalTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SquadExample/Content/EQS/EQS_FindCoverTowardGoalTarget.json) | SquadExample | SDEnvQueryGenerator_Covers | Distance ×2, Dot, Pathfinding, Target provider | Cover toward goal (squad example) |
| [`EQS_LeapFrogTokenHandling`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SquadExample/Content/EQS/EQS_LeapFrogTokenHandling.json) | SquadExample | SDEnvQueryGenerator_TokenRequests | Distance | Leap-frog token handling |

Note: [`EQS_FindSearchLocation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/EQS/EQS_FindSearchLocation.json) has `BP_InfluenceEvaluator_AlertLocationGenerator_C` as its first export, not an EnvQuery. The count of 22 includes it.

---

## 10. How Values Combine

These are general UE EQS semantics. The dump gives the test settings, but this pass did not verify scoring behaviour in the runtime.

- Each test has a `TestPurpose` (`Filter`, `Score`, or both) and a `TestOrder`. Filters run first; scoring tests then combine.
- `FilterType` (`Minimum`/`Maximum`) with `FloatValueMin`/`FloatValueMax` defines the pass range. Values seen include minimum distances of 100 to 400 and dot thresholds of 0.4 to 0.8 (Dot2D).
- `ScoringFactor` (typically 0.5 to 10) and `ScoringEquation` (for example `InverseLinear`) weight a test's contribution.
- `MultipleContextScoreOp` is `MinScore` on most distance tests, so an item must satisfy the nearest context.
- `WDAIDataProvider_*` nodes feed AI config values (cover radius, weapon min/max range, agent height) into the test's `DataBinding`.

---

## 11. Still not pulled / limitations

- **Unit system.** Distances are in the export's native units. The export does not name them. Treat them as Unreal units (cm) only after checking against a known value.
- **Enum meanings.** `EWDAIAlertState` values are given by name, but the numeric thresholds are not linked to a documented meaning. The Pressure key is inferred to drive them.
- **Example packs.** Whether `*Example` and [`BesiegeExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/BesiegeExample/Content/BesiegeExample.json)/[`CoverExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/CoverExample/Content/CoverExample.json)/[`SmartObjectExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SmartObjectExample/Content/SmartObjectExample.json) ship in the live build is not established here.
- **Blackboard key use.** Which AI task reads or writes each key is in behaviour trees and BP graphs, not in this folder. This doc does not map key use.
- **Behaviour trees.** `BT_WDAIPvECore_Base` is referenced but not in this folder.
- **Sub-exports not expanded.** EQS sub-exports (individual test settings) are summarised by count and type, not every field.
- **Unnamed localisation keys.** Some properties appear as `_aaa…` hashes; those were not resolved.
