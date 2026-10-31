# Round 36: AI soldiers and PvE missions

Closes the "not yet known" gaps of the wiki pages `ai-enemies`, `hunter-killer`, `strike-and-disarm`, `vip-escort`, `pve-scenarios`.
GitHub-only page (docs/ is not part of the site), so asset names and RVAs are used freely.

## Method and evidence level

- Cooked data read with `WdExtract` (round-36 build of `tools/cue4parse_extractor`, built to `E:/Reverse_Engineer/wardogs_analysis/round36_ai/bin`; the checked-in `bin/` copy predates the `rawfiles` mode). Inputs: the `AI` and `PvE` game feature plugins (145 packages through `dump`), plus the 110 World Partition cell levels (`.umap`) of the five scenario data layers, found with `rawfiles <scenario>/Content/EDL` and dumped by package path. The cells hold the placed actors (AI spawners, vendors, loot markers, the laptop). The earlier `data/` export did not contain them.
- Plugin descriptors (`.uplugin`, `rawfiles .uplugin --copy`) for the feature dependency graph.
- Native defaults: static reading of the decompiled corpus (`decompiled_cl516586_20261017_mmvpuc__`, constructors located through the `*_VFT` aliases). Evidence level for those: **static disassembly / decompiler output, not run**. Nothing was devirtualized.
- Reproduce: `list ""` once, `dump` the `Wardogs/Plugins/GameFeatures/{PvE,AI}/` packages (minus `/UI/` and `VoiceOvers/`), `rawfiles "<Scenario>/Content/EDL"` per scenario, `dump` the listed `.umap` package paths. `_tools/pve_scenario_data.py` rebuilds `assets/data/pve-scenarios.json` from those dumps.

## Summary

| Gap | Status | Result |
|---|---|---|
| 1 AI health, damage multipliers | FOUND (indirect) / NATIVE | AI uses the player character Blueprint `B_WDCore_MoverPlayerCharacter_C`: 100 max health, same as players. No AI-specific health or damage multiplier exists in cooked data. |
| 2 Perception, alert, aim | FOUND + NATIVE | Sight 2000 m, lose-sight 2100 m, hearing 1000 m, plus multipliers and detectability numbers below. No AI-specific accuracy or aim-error value exists; aim point is the target's head bone. |
| 3 Squads per mission, counts, waves | FOUND | Strike and Disarm 53 Lonestar spawners (27 at start, 26 counter-attack wave on hack start); VIP Escort 95 Manticore spawners; Hunter Killer none (unfinished blockout). |
| 4 Objectives, time limit, map, 3000/2000, hack duration | FOUND | 3000/2000 are `ScenarioStartingCash`. All missions are on the Kavkazi world. Hack takes 300 s (placed value; the Blueprint default is 60). No time limit in the quest data. |
| 5 VIP loot "AK" | FOUND | Row name says AK, item is `Id.Item.SV98` x1 with 1 `Id.Item.SV98Magazine` (100%), respawn 10 s, 15 initial spawn points. |
| 6 Patrol / search / flee in the shipped game | FOUND | Patrol (VIP Escort), Search and Besiege (Strike and Disarm) are dependencies of shipped scenarios and used. Flee and AttackPlayer are example packs with no dependent. |

## 1. AI health and damage taken

Status: FOUND (indirect). Evidence: cooked data read plus existing native-defaults.

- Every `WDAICharacterConfigData` ([`DefaultAIPreset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DefaultAIPreset.json), [`AIC_Lonestar_Rifleman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar/AIC_Lonestar_Rifleman.json), [`AIC_Lonestar_Sniper`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar/AIC_Lonestar_Sniper.json), [`AIC_Manticore_Rifleman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Rifleman.json), [`AIC_Manticore_Machinegunner`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Machinegunner.json), [`AIC_Manticore_Marksman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Marksman.json)) has `AICharacterClass = /WDCore/Character/B_WDCore_MoverPlayerCharacter.B_WDCore_MoverPlayerCharacter_C`. That is the player character. There is no separate AI character Blueprint (searched: `B_AI*`, `BP_AI*`, `*NPC*`, `AIC_*`; the only `Characters/NPC` assets are meshes and vendor props).
- The controller (`BP_CoreAIController`) and the config set no health, attribute set or GameplayEffect. Health is therefore the player character's: `UWDVitalityComponent` ctor `0x6B81720` writes `BaseHealth` = `MaxHealth` = 100.0 (see [Medical](../../game-features/Wardogs_Medical_v1.md); `assets/data/bp-defaults.json` carries `MaxHealth` 100 for this Blueprint).
- All five soldiers carry `Id.Item.LightArmor` and `Id.Item.LightHelmet`, the same items players can wear, so the normal [damage pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md) applies, including armor and head multipliers.
- The only AI-keyed setting near damage is the perception side: `AISenseConfig_Damage` (MaxAge 10 s) lets a hit alert the soldier.
- Not found: any AI-specific damage taken multiplier, in data or in the damage-pipeline functions already reviewed. This is "not found in data and the reviewed natives", not a proof of absence in all native code. Status for the multiplier: ABSENT in cooked data (searched: GameplayEffects, AttributeSets, config components, controller, spawner), NATIVE not checked beyond the reviewed damage path.

## 2. Perception, alert thresholds, firing, aim

Status: FOUND for Blueprint values, NATIVE for constructor defaults and for how multipliers combine.

### 2a. Senses (`BP_CoreAIController`, `AIPerception` = `WDAIPerceptionComponent`)

| Property | Value | Source |
|---|---|---|
| `AISenseConfig_Sight.SightRadius` | 200000 | BP CDO (cm, = 2000 m) |
| `AISenseConfig_Sight.LoseSightRadius` | 210000 | BP CDO (= 2100 m) |
| `AISenseConfig_Sight.MaxAge` | 30.0 s | BP CDO |
| `AISenseConfig_Hearing.HearingRange` | 100000 | BP CDO (= 1000 m) |
| `AISenseConfig_Hearing.MaxAge` | 30.0 s | BP CDO |
| `AISenseConfig_Damage.MaxAge` | 10.0 s | BP CDO |
| `DominantSense` | `AISense_Sight` | BP CDO |
| `WDAIPerceptionComponent.VisionRangeMultiplier` | 0.02 | BP CDO |
| `WDAIPerceptionComponent.HearingRangeMultiplier` | 0.05 | BP CDO |
| `VisionAngleMultiplier`, `VisionPlayerConcealmentMultiplier` | 1.0, 1.0 | NATIVE, ctor `0x8863540` (offsets +0x224, +0x228) |

Sight angle: the `AISenseConfig_Sight` export sets only radii and age, so `PeripheralVisionAngleDegrees` and the other fields are engine defaults (not exported).

How `VisionRangeMultiplier` / `HearingRangeMultiplier` combine with the radii is native logic (`UWDAIPerceptionComponent`, no function names resolved in the corpus). If they scale the radii, the effective values would be 40 m sight and 50 m hearing; that is **not verified** and should not be published as fact.

### 2b. Detection build-up and alert (`WDAIThreatDetectionMonitorComponent`, `WDAIAlertStateComponent`)

| Property | Blueprint value | Native default (ctor `0x8863AB0`) |
|---|---|---|
| `DetectionDecayRate` | 0.25 | 0.01 (0x3C23D70A) |
| `TimeBeforeStartDecay` | 5.0 s | 10.0 |
| `MaxDetectionLevel` | not set | 1.0 |

Alert thresholds ([`AlertStateThreashold_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AlertStateThreashold_DataConfig.json), already on the AI page): Relaxed 0.0, Alert 0.8, Combat 1.0 (combat needs line of sight to go up). With `MaxDetectionLevel` 1.0 native this fits a 0..1 detection level, but that the threshold input is this level is still an inference.

`WDAICharacterConfigData` fields not set in any AI asset take the native defaults of ctor `0x8863090`: `POILookAtSwitchTime` 2.5 s (+0x158), `AlertWaitTime` 2.0 s (+0x15C), `RadiusToSearchForCovers` 3000.0 (+0x160). `BT_WDAIPvECore_AlertedReaction` reads `AlertWaitTime` through `WDAIDataProvider_AIConfigData` as its wait time (the task default value in the BT is 10.0 and is overridden by the binding).

### 2c. How visible a player is (`BP_PlayerCharacterDetectabilityComponent`, added to the player character by the [`WDAIPvEAICore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/WDAIPvEAICore.json) plugin)

| Property | Value | Native default (ctor `0x8864400`) |
|---|---|---|
| `StanceDetectability` | Stand 1.0, Crouch 0.4, Prone 0.3 | empty map |
| `StanceDetectabilityMultiplier` | 0.5 | 1.0 |
| `HearingMovementSpeedMultiplier` | 0.0015 | 1.0 |
| `WeaponFiring` | 5.0 | 1.0 |
| `WeaponFiringMultiplier`, `MovementSpeedMultiplier` | not set | 1.0, 1.0 |

The formula that combines these is native (not decoded). Only the inputs are known.

### 2d. Reaction, aiming, firing

| Item | Value | Source |
|---|---|---|
| Aim point | target's `Head` bone (`BTS_AimAtTarget.GetFocalPoint`, `GetBoneTransform("Head")`, then `K2_SetFocalPoint`) | BP bytecode |
| Aim update interval | 0.1 s, no deviation (`BT_Default_InCoverShooting`) | BT data |
| Burst (`BTS_FireWeapon`) | `BurstShotCount` 3, `BurstDuration` 0.2, `BurstInterval` 1.0, `ShotInterval` 0.2, `TriggerPullDuration` 0.05 | BP CDO |
| Shoot task | `WDBTTask_ShootAtTarget.RoundOfBursts` 3 | BT data |
| Fire modes | Burst, then Automatic, then SemiAutomatic (`ShootingConfigData.FireModePriority`) | config |
| Cover waits | `BT_TakeOverCoverPeek` 2 s +/-1 and 4 s +/-2; `BT_CoverSurfing` 1 s +/-0.5; `BT_AttackPlayer` waits 1 s and 3 s | BT data |

Accuracy: no spread, inaccuracy or hit-chance value exists in any AI asset. The soldiers fire through the same weapon component as players (`WDWeaponComponent`, `GetActiveFireMode`), so weapon spread and recoil are the weapon's own. Status for AI accuracy: ABSENT as an AI-specific value (searched: config data, controller, all `BT_*`, `BTS_*`, `BTT_*`); NATIVE for how the focal point turns into aim.

## 3. Squads, counts and waves per mission

Status: FOUND. Evidence: cooked cell levels of each scenario's external data layers (`Kavkazi/_Generated_/*.umap`). Counts are placed `BP_WDPvEAISpawner_C` actors; each has one `SpawnConfig`. That one spawner produces exactly one soldier is the spawner's native logic and is not verified.

| Mission | Spawners | Config | Notes |
|---|---|---|---|
| Strike and Disarm | 53 | [`AIC_Lonestar_Rifleman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar/AIC_Lonestar_Rifleman.json) 49, [`AIC_Lonestar_Sniper`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar/AIC_Lonestar_Sniper.json) 4 | 27 start automatically (23 riflemen, 4 snipers); 26 riflemen have `SpawnTriggerType = DisableAutomaticSpawn` and form the counter-attack wave. 6 of the 27 use `ForcedGoal = Goal_Patrol`; 22 of the 27 and all 26 wave spawners are tied to a `WDAITetherVolume` (48 tethered). The 26 wave spawners point `ForcedGoalTarget` at a `WDTargetAreaVolume`. |
| VIP Escort | 95 | [`AIC_Manticore_Rifleman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Rifleman.json) 86, [`AIC_Manticore_Marksman`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Marksman.json) 5, [`AIC_Manticore_Machinegunner`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore/AIC_Manticore_Machinegunner.json) 4 | All start automatically. 31 riflemen use `Goal_Patrol` with a `BP_PatrolRouteActor` (16 routes placed). No tether volumes. |
| Hunter Killer | 0 | none | 28 cells contain only text labels ("Guards", "Deploy Location", "HVT Location", "Lieutenant Location", "Exfil Location", "Patrol"), no spawners, no quest nodes (`Q_HunterKiller_01` is just Entry then Exit), no player faction, no cash. The mission is an unfinished blockout. |

Wave mechanism: `SQ_LaptopHacking` sends the quest event `Quest.Actor.Event.AISpawners.Trigger` to `QuestObjective.StrikeDisarm_01.CounterAttackSpawn` when the laptop enters `HackingInProgress`. `B_MultiAISpawner_C` (one placed) receives it and calls `WDPveAISpawnerCollectionComponent.TriggerAISpawners` on its list of exactly 26 spawners. There is one wave; no timed or repeating waves were found. Native enum `EWDPveAISpawnType`: 0 EnableAutomaticSpawn, 1 DisableAutomaticSpawn.

Factions match the story strings: Strike and Disarm player faction Charlie (Manticore), enemies Lonestar (Alpha). VIP Escort player faction Bravo (Valkyra), enemies Manticore (Charlie).

Other placed actors: 3 to 6 `b_VehicleSpawner_C` per mission (Kodiak and Bobcat variants), equipment and vehicle vendors, and one `WDSpawnVolume` (faction Charlie, `MaxSpawnPoints` 15, spacing 2500/2500) in Strike and Disarm.

## 4. Objectives, time limits, map, 3000/2000, hack duration

Status: FOUND. Evidence: `Q_*`/`SQ_*` quest graphs (node behaviours and links read from the dump), string tables, GFDs, placed laptop actor.

- **3000 and 2000** are `FWDScenarioData.ScenarioStartingCash` (SDK `BaseScenarioRuntime_structs.hpp`, offset 0x0004): the cash players start the mission with (Strike and Disarm 3000, VIP Escort 2000). They are not time limits or score targets. Hunter Killer and the example scenario set no cash. `ScenarioCompletedRewardCash` is not set in any scenario.
- **Map:** all three missions use the Kavkazi world (`/Game/Maps/Worlds/Kavkazi/Kavkazi`) through external data layers `EDL_Blockout_*` and `EDL_Gameplay_*` (plugin content streamed into the base world). Layout names inside the data are not available beyond that.
- **Strike and Disarm flow:** four intro voice lines (parallel), then `SQ_LaptopHacking`: laptop set to Idle; wait for `HackingInProgress`; on start play the hack-start line, add `Goal_BesiegeTarget` and `Goal_StopHack` (source tag `Interaction.Context.Laptop`) to the AI, trigger the counter-attack wave; wait for `Hacked` (objective text "Prevent Lonestar from reaching the laptop until the virus is uploaded"); on completion play the hack-end line and remove both goals; if the state becomes `AbortedHack` the scenario completes as failed ("LaptopObjectiveFailed"). Then `SQ_Extraction_Helicopter` (objective "Board the extraction helicopter to leave the area"), then the mission-complete line. The AI goal `Goal_StopHack` makes soldiers walk to the laptop with `BT_Interact` (assignment range `MaxDistanceForAssignment` 3000, priority 500 to 1000).
- **Hack duration:** `B_StrikeDisarm_LaptopObjective_C.HackingDurationSeconds` is 60.0 in the Blueprint class default and **300.0 on the placed laptop instance**, so the effective hack takes 300 s (5 minutes). The [`SOD_Hack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/Blueprints/SOD_Hack.json) smart-object behaviour is `IsTimeLimited` true with action `Action.SmartObject.UseComputer`. Countdown text on the laptop is a placeholder ("Hacking 25:15").
- **VIP Escort flow:** three intro voice lines, `SQ_RandomPlayerMarkedForDeath` picks one random player and gives it `WDMarkedForDeathComponent` (tracker tag `QuestObjective.BaseScenario.MarkedForDeath`; the VIP is a player, not an AI). It ends when that player reaches the `State.Player.Vitality.Critical` state or disconnects: then the fail line plays, a 10.0 s wait, and the scenario completes as failed ("The targeted player died."). In parallel the team must reach the overlap area `QuestObjective.VIPEscort_01.ExtractionProximity` (objective "Safely escort the targeted player to the extraction point"), then board the extraction helicopter (`SQ_Extraction_Helicopter`, `Vehicle.Variant.Air.Rotary.Littlebird.Default`, spawned for the player's faction at one of three entry points, flies a spline with [`Extraction_Helicopter_Speed_Curve_Entry`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/ExtractionHelicopter/Extraction_Helicopter_Speed_Curve_Entry.json)); the success line plays and the scenario completes as succeeded ("The team escaped successfully.").
- **Time limit:** none found. The only timers in the quest graphs are the 10 s delay after the VIP dies and the 300 s hack. `ScenarioPostMatchTimeoutDuration` (a `Config` property of a native `BaseScenarioRuntime` class, SDK offset 0x01B8; it limits the post-match screen, not play time) exists but is an ini value, not read here. Status for a mission time limit: ABSENT in cooked scenario data (searched all `Q_*`, `SQ_*`, GFDs, string tables).
- Quest display names are placeholders in the data ("[PH] Strike and Swipe", "[PH] VIP Escort"); the string table calls the Strike and Disarm laptop mission "Strike and Swipe" internally.

## 5. VIP Escort loot ([`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json))

Status: FOUND. Evidence: cooked DataTable (rows already on the Economy data-tables page).

| Row | Item | Amount | Chance | By points | Initial points | Respawn |
|---|---|---|---|---|---|---|
| `Lootable.VIPEscort01.Fuelcan100` | `Id.Item.FuelCan` | 1 | 100 | no | 0 | no |
| `Lootable.VIPEscort01.AK` | `Id.Item.SV98` (sub-item `Id.Item.SV98Magazine` x1, 100%) | 1 | 100 | yes | 15 | yes, 10.0 s |

The row is named "AK" but the item is the SV98 sniper rifle plus one magazine, not an AK. Both rows: `bSpawnByDefault` true, `bSpawnInsideControlZoneOnly` false. Placement: no actor tagged `Lootable.VIPEscort01.*` exists in the 65 VIP Escort cells (the placed loot markers there use the shared tags `Lootable.Bandage` x12, `Weapon` x3, `Defib.Cheap` x3, `Sniper`, [`Armor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Armor.json), `Helmet`), so where these two rows are placed is not in this data (likely the base world layer); how often or where the SV98 and the fuel can appear is NOT known.

## 6. Patrol, search, flee in the shipped game

Status: FOUND. Evidence: `.uplugin` dependency lists plus placed actors and quest nodes.

- `Goal_Patrol` (plugin [`Behavior_Patrol`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Patrol/Content/Behavior_Patrol.json)): required by [`VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/VIPEscort_01.json); set as `ForcedGoal` on 31 VIP Escort and 6 Strike and Disarm spawners with `BP_PatrolRouteActor` targets. Behaviour tree `BT_Patrol`: speed modifier 0.5 while patrolling (`BTDecorator_ModifyMovementSpeed`), `AdjustMovementSpeedByDistance` run distance 500, modifier 0.4 to 1.0.
- `Goal_BesiegeTarget` (plugin [`Behavior_Besiege`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Besiege/Content/Behavior_Besiege.json)): required by [`StrikeDisarm_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/StrikeDisarm_01.json); added to the AI by `SQ_LaptopHacking` while the hack runs.
- `Goal_Search` (plugin [`Behavior_Search`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behavior_Search/Content/Behavior_Search.json)): required by [`StrikeDisarm_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/StrikeDisarm_01.json). No quest or spawner names it directly, so how it is used is native or `BT` logic; the plugin is a declared dependency of a shipped mission.
- `Goal_Example_Flee` (plugin [`Behaviour_Example`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/Behaviour_Example/Content/Behaviour_Example.json)) and `Goal_Example_AttackPlayer` (plugin [`SquadExample`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/SquadExample/Content/SquadExample.json)): no scenario or plugin depends on them. They are example packs; nothing in the data activates them. All AI/PvE plugins are `ExplicitlyLoaded`, `EnabledByDefault` false, initial state `Registered`, so activation is driven from outside the plugin files (scenario or native code); whether the backend ever activates the examples is unknown.

## Corrections to existing pages

- PvE page said AI inventory counts were not extracted: now complete (see below). Magazines are x2 for every soldier.
- AI/PvE pages did not link the 5 AI configs to scenarios: now done.

Full AI inventories (`AIInventory`): Lonestar Rifleman M4 x1, LightArmor x1, LightHelmet x1, M4Magazine x2. Lonestar Sniper MK22 x1, LightArmor x1, LightHelmet x1, SniperScope10x x1, MK22Mag x2. Manticore Rifleman AK74M x1, LightArmor x1, LightHelmet x1, AK74MMagazine x2, MZL_07 x1. Manticore Machinegunner LMG_02 x1, LightArmor x1, LightHelmet x1, LMG_02Magazine x2, MZL_04 x1. Manticore Marksman SVDM x1, LightArmor x1, LightHelmet x1, SVDMMagazine x2, 6xScope x1, MZL_04 x1.

## Wiki updates

- `_wiki/game-modes-and-maps/ai-enemies.md` infobox: Health "Not yet known" -> "100, the same as a player (the soldiers use the player character)"; Accuracy "Not yet known" -> "No AI-specific accuracy value; they fire their weapons like players and aim at the head"; Perception -> "Sees up to 2,000 m, hears up to 1,000 m (configured ranges, scaled by internal multipliers); alert wait 2 s". Add sections: Health and armor (100 HP, light armor and light helmet on all five, no AI damage multiplier found), Senses (table 2a, 2b), How players are detected (stance 1.0 / crouch 0.4 / prone 0.3; firing noise factor 5), Firing (3-round bursts every 1 s, aim updated every 0.1 s), Magazines (2 each, full inventories), squad usage per mission.
- `ai-enemies.md` "The data does not say which mission uses which squad" -> Strike and Disarm uses Lonestar riflemen and snipers, VIP Escort uses Manticore riflemen, marksmen and machine gunners; Hunter Killer has no soldiers.
- `_wiki/game-modes-and-maps/strike-and-disarm.md`: "Scenario value 3000, meaning not confirmed" -> starting cash 3,000; "hack length not yet known" -> 5 minutes (300 s; the base game object says 60 s but the placed laptop overrides it); Enemies section -> 53 Lonestar soldiers (49 riflemen, 4 snipers), 27 at the start (a few on patrol) plus a 26-rifleman counter-attack wave that spawns when the hack starts; while it runs the soldiers are sent to the laptop to stop it; objectives (upload virus, defend until done, board extraction helicopter); failure if the hack is aborted; map -> Kavkazi; time limit -> none found; infobox "Objective" and "Map or layout".
- `_wiki/game-modes-and-maps/vip-escort.md`: "Scenario value 2000" -> starting cash 2,000; objectives: one random player is the VIP (marked for death), keep them alive, reach the extraction area, board the helicopter; fail 10 s after the VIP goes down (reaches Critical) or disconnects; Enemies -> 95 Manticore (86 riflemen, 5 marksmen, 4 machine gunners), 31 of the riflemen on patrol routes; map -> Kavkazi; loot: "a rifle that the data names only as AK" -> SV98 sniper rifle with one magazine (the row is named AK), respawning 10 s after pickup, plus one Fuel Canister (no respawn); where they are placed is not in the data.
- `_wiki/game-modes-and-maps/hunter-killer.md`: Map -> Kavkazi; Objective/Enemies "not yet known" -> the mission is an unfinished blockout: no AI soldiers, no objectives, no starting cash and no player faction are set; the map only holds placeholder labels (Guards, Lieutenant, HVT, Deploy, Exfil, Patrol), which hint at a planned kill/capture mission.
- `_wiki/game-modes-and-maps/pve-scenarios.md`: replace "unnamed values 3000 / 2000" -> starting cash; add that all missions are on Kavkazi; add the shared extraction (helicopter from one of three entry points) and the marked-for-death VIP mechanic; patrol, search and besiege behaviours ship and are used by Strike and Disarm and VIP Escort, while flee and attack-player are example packs only.
- Also update the glossary/"not yet known" tiles anywhere that lists "AI health", "hack duration", "VIP loot AK" as unknown.
