---
title: "Rewards & Unlocks changes"
parent: "Season 2 Changes"
nav_order: 7
description: "Rewards & Unlocks: 14 assets added, 105 modified with real changes, 4 noise-only, 10,299 property changes. Role XP, unlock-tree costs and challenge rewards changed."
---

# Rewards & Unlocks changes

Season 1 to Season 2 changes for the Rewards & Unlocks area, from the area diff file. Every number below is copied from `assets/data/season-diff/rewards-unlocks.json`.

| Measure | Count |
|---|---:|
| Assets added | 14 |
| Assets removed | 0 |
| Assets modified with real changes | 105 |
| Assets moved | 0 |
| Noise-only modified assets (skipped, no real change) | 4 |
| Property changes | 10,299 (changed 7,954, added 2,062, removed 283) |

Full filterable list: [Rewards & Unlocks in the change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=rewards-unlocks).

## Headline changes

### Role mastery XP

`DT_RoleMasteryDefinitions` has 546 changed XP values: 6 roles (Driver, Infantry, Medic, Pilot, Recon, Support) with 91 levels each, levels 10 to 100. The values are the same for every role.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---:|---:|---:|
| DT_RoleMasteryDefinitions | Driver · level 10 · XP | 35000 | 25000 | −10000 (−28.6%) |
| DT_RoleMasteryDefinitions | Driver · level 11 · XP | 46250 | 28750 | −17500 (−37.8%) |
| DT_RoleMasteryDefinitions | Driver · level 20 · XP | 250000 | 111500 | −138500 (−55.4%) |
| DT_RoleMasteryDefinitions | Driver · level 30 · XP | 500000 | 318200 | −181800 (−36.4%) |
| DT_RoleMasteryDefinitions | Driver · level 50 · XP | 1500000 | 1150000 | −350000 (−23.3%) |
| DT_RoleMasteryDefinitions | Driver · level 75 · XP | 2826750 | 2218000 | −608750 (−21.5%) |
| DT_RoleMasteryDefinitions | Driver · level 100 · XP | 6000000 | 5132500 | −867500 (−14.5%) |

### Unlock tree costs and level gates (`DT_MetaTree_Roles`)

194 node cash costs and 194 node level gates (`MinLevel`) changed, 211 node IDs changed, and 31 nodes were added. Nodes are listed by their position in the table. 211 node IDs changed, so the same position can name a different unlock in each season.

Largest cash cost changes (top 20 of 194 by percent):

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---:|---:|---:|
| DT_MetaTree_Roles | Pilot · node 2 · cash cost | 750 | 125000 | +124250 (+16566.7%) |
| DT_MetaTree_Roles | Pilot · node 6 · cash cost | 2500 | 250000 | +247500 (+9900.0%) |
| DT_MetaTree_Roles | Driver · node 5 · cash cost | 1500 | 35000 | +33500 (+2233.3%) |
| DT_MetaTree_Roles | Driver · node 12 · cash cost | 5000 | 100000 | +95000 (+1900.0%) |
| DT_MetaTree_Roles | Support · node 10 · cash cost | 7500 | 100000 | +92500 (+1233.3%) |
| DT_MetaTree_Roles | Support · node 14 · cash cost | 10000 | 100000 | +90000 (+900.0%) |
| DT_MetaTree_Roles | Support · node 28 · cash cost | 25000 | 250000 | +225000 (+900.0%) |
| DT_MetaTree_Roles | Wardog · node 50 · cash cost | 5000 | 50000 | +45000 (+900.0%) |
| DT_MetaTree_Roles | Driver · node 10 · cash cost | 2500 | 20000 | +17500 (+700.0%) |
| DT_MetaTree_Roles | Medic · node 30 · cash cost | 25000 | 200000 | +175000 (+700.0%) |
| DT_MetaTree_Roles | Recon · node 40 · cash cost | 25000 | 200000 | +175000 (+700.0%) |
| DT_MetaTree_Roles | Recon · node 34 · cash cost | 25000 | 150000 | +125000 (+500.0%) |
| DT_MetaTree_Roles | Infantry · node 30 · cash cost | 45000 | 250000 | +205000 (+455.6%) |
| DT_MetaTree_Roles | Infantry · node 17 · cash cost | 20000 | 100000 | +80000 (+400.0%) |
| DT_MetaTree_Roles | Medic · node 11 · cash cost | 10000 | 50000 | +40000 (+400.0%) |
| DT_MetaTree_Roles | Medic · node 18 · cash cost | 15000 | 75000 | +60000 (+400.0%) |
| DT_MetaTree_Roles | Support · node 9 · cash cost | 10000 | 50000 | +40000 (+400.0%) |
| DT_MetaTree_Roles | Support · node 16 · cash cost | 30000 | 150000 | +120000 (+400.0%) |
| DT_MetaTree_Roles | Wardog · node 6 · cash cost | 5000 | 25000 | +20000 (+400.0%) |
| DT_MetaTree_Roles | Recon · node 21 · cash cost | 30000 | 125000 | +95000 (+316.7%) |

Largest level gate changes (top 10 of 194 by size):

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---:|---:|---:|
| DT_MetaTree_Roles | Wardog · node 57 · min level | 150 | 100 | −50 (−33.3%) |
| DT_MetaTree_Roles | Wardog · node 56 · min level | 140 | 100 | −40 (−28.6%) |
| DT_MetaTree_Roles | Wardog · node 55 · min level | 130 | 95 | −35 (−26.9%) |
| DT_MetaTree_Roles | Wardog · node 54 · min level | 120 | 90 | −30 (−25.0%) |
| DT_MetaTree_Roles | Wardog · node 53 · min level | 110 | 85 | −25 (−22.7%) |
| DT_MetaTree_Roles | Wardog · node 45 · min level | 83 | 65 | −18 (−21.7%) |
| DT_MetaTree_Roles | Wardog · node 49 · min level | 93 | 75 | −18 (−19.4%) |
| DT_MetaTree_Roles | Wardog · node 51 · min level | 100 | 82 | −18 (−18.0%) |
| DT_MetaTree_Roles | Wardog · node 43 · min level | 80 | 63 | −17 (−21.2%) |
| DT_MetaTree_Roles | Wardog · node 44 · min level | 82 | 65 | −17 (−20.7%) |

The other 174 cost changes and 184 level gate changes are in the [browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=rewards-unlocks&q=MetaTree).

### Challenge rewards (`DT_ChallengeRewards_SessionEvents_Shared`)

50 numeric literal values changed and 47 non-numeric values changed. 736 values were added across 164 rows in 9 event groups, and 1 entry was removed.

Compiled expression instructions in this table changed 18 times (compiled data, not tabulated).

Largest literal value changes (top 30 of 50 by percent):

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---:|---:|---:|
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · Mortar · XP · AssistReward | 37.5 | 90.0 | +52.5 (+140.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · Mortar · XP · DefaultReward | 75.0 | 175.0 | +100 (+133.3%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · Mortar · Cash · BaseReward | 300.0 | 650.0 | +350 (+116.7%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroySupplyCrate · Small · Armoured · Cash · BaseReward | 250.0 | 500.0 | +250 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroyVehicleSection · TNK_01 · AntiAir · Cash · TracksReward | 1250.0 | 350.0 | −900 (−72.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroyVehicleSection · TNK_01 · Heavy · Cash · TracksReward | 1750.0 | 550.0 | −1200 (−68.6%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · MistralAA · Cash · BaseReward | 2000.0 | 650.0 | −1350 (−67.5%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroyVehicleSection · TNK_01 · AntiAir · Cash · EngineReward | 2500.0 | 875.0 | −1625 (−65.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · MistralAA · XP · DefaultReward | 500.0 | 175.0 | −325 (−65.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · TNK_01 · AntiAir · Cash · BaseReward | 10000.0 | 3500.0 | −6500 (−65.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · MistralAA · XP · AssistReward | 250.0 | 90.0 | −160 (−64.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroyVehicleSection · TNK_01 · Heavy · Cash · EngineReward | 3500.0 | 1375.0 | −2125 (−60.7%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroySupplyCrate · Large · Armoured · Cash · BaseReward | 500.0 | 800.0 | +300 (+60.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · Phalanx · Cash · BaseReward | 3000.0 | 1200.0 | −1800 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · Phalanx · XP · DefaultReward | 750.0 | 300.0 | −450 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · Phalanx · XP · AssistReward | 375.0 | 150.0 | −225 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DeploySupplyCrate · Cash · SmallCrateReward | 250.0 | 125.0 | −125 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DeploySupplyCrate · Cash · PalletReward | 1250.0 | 625.0 | −625 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DeploySupplyCrate · Cash · LargeCrateReward | 500.0 | 250.0 | −250 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DeploySupplyCrate · Cash · ArmouredSmallCrateReward | 250.0 | 125.0 | −125 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DeploySupplyCrate · Cash · ArmouredLargeCrateReward | 500.0 | 250.0 | −250 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | PlayerDelivered · XP · DefaultReward | 25.0 | 12.5 | −12.5 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | PlayerDelivered · XP · HotZoneMagnetReward | 50.0 | 25.0 | −25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | PlayerDelivered · XP · ControlZoneReward | 50.0 | 25.0 | −25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | PlayerDelivered · XP · HotZoneReward | 50.0 | 25.0 | −25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | SafeZoneEntered · XP · DefaultReward | 100.0 | 50.0 | −50 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | VehicleDestroyed · TNK_01 · Artillery · Cash · BaseReward | 14000.0 | 8000.0 | −6000 (−42.9%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroySupplyCrate · Free · Cash · BaseReward | 250.0 | 150.0 | −100 (−40.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroySupplyCrate · Large · Cash · BaseReward | 500.0 | 300.0 | −200 (−40.0%) |
| DT_ChallengeRewards_SessionEvents_Shared | DestroySupplyCrate · Small · Cash · BaseReward | 250.0 | 150.0 | −100 (−40.0%) |

The other 20 literal value changes are in the [browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=rewards-unlocks&q=SessionEvents_Shared).

Non-numeric changes (expressions and text values, grouped by the before and after pair):

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_ChallengeRewards_SessionEvents_Shared | XP · expression (16 rows) | `(BaseReward)` | `(BaseReward) / NumberOfAssisters` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (14 rows) | `BaseReward * FOBSuppliedAssistModifier` | `(BaseReward * FOBSuppliedAssistModifier) / NumberOfAssisters` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (5 rows) | `BaseReward * AlignmentModifier * TargetZoneModifier ` | `BaseReward * AlignmentModifier * TargetZoneModifier * SupplyCrateValue` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (2 rows) | `BaseReward * FOBSuppliedModifier` | `(BaseReward * FOBSuppliedModifier) / NumberOfAssisters` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | XP · Variables[Key=FriendlyReward].Value.Game (1 row) | `None` | `NumberOfAssisters` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (1 row) | `BaseReward * TargetZoneModifier` | `(BaseReward + (clamp(CrateStreak - 1, 0, CrateStreakMax) * CrateStrea…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | XP · expression (1 row) | `(BaseReward * TargetZoneModifier)` | `((BaseReward + (clamp(CrateStreak - 1, 0, CrateStreakMax) * CrateStre…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (1 row) | `PurchaseValue * MarkupMultiplier` | `PurchaseValue * (MarkupMultiplier - (MarkupMultiplier - 1) * clamp(La…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | XP · expression (1 row) | `PurchaseValue` | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReduc…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (1 row) | `(BaseReward * ZoneModifier) * (PlayerCount)` | `((BaseReward + (clamp(PlayerStreak - 1, 0, PlayerStreakMax) * PlayerS…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | XP · expression (1 row) | `(BaseReward)` | `(BaseReward + (clamp(PlayerStreak - 1, 0, PlayerStreakMax) * PlayerSt…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (1 row) | `BaseReward * max(PlayersSurvivedMin, PlayersSurvivedCount)` | `(BaseReward + (clamp(ReturnStreak - 1, 0, ReturnStreakMax) * ReturnSt…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | XP · expression (1 row) | `(BaseReward * max(PlayersSurvivedMin, PlayersSurvivedCount))` | `((BaseReward + (clamp(ReturnStreak - 1, 0, ReturnStreakMax) * ReturnS…` | changed |
| DT_ChallengeRewards_SessionEvents_Shared | Cash · expression (1 row) | `BaseReward * RepeatActionCount` | `BaseReward * clamp(RepeatActionCount, 0, RepeatActionCountMax)` | changed |

Rows added, by event group:

| Event group | Rows with added values |
|---|---:|
| VehicleDestroyed | 120 |
| DestroyVehicleSection | 26 |
| DestroySupplyCrate | 10 |
| PlayerKill | 3 |
| DeploySupplyCrate | 1 |
| PurchaseFromSupplyCrate | 1 |
| PlayerDelivered | 1 |
| SafeZoneEntered | 1 |
| VehicleFlyThrough | 1 |

### Buildable challenge rewards (`DT_ChallengeRewards_SessionEvents_Buildables`)

87 numeric literal values changed and 20 non-numeric values changed. 260 values were added across 38 rows, and 15 entries were removed.

Compiled expression instructions in this table changed 20 times (compiled data, not tabulated).

Largest literal value changes (top 30 of 87 by percent):

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---:|---:|---:|
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · FloorBoard · XP · TankAssistReward | 0.625 | 5.0 | +4.375 (+700.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · WindowBoard · XP · TankAssistReward | 0.625 | 5.0 | +4.375 (+700.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · BarbedWire · XP · TankAssistReward | 0.875 | 5.0 | +4.125 (+471.4%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · CamoNetTent · XP · TankAssistReward | 0.875 | 5.0 | +4.125 (+471.4%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · FloorBoard · XP · AssistReward | 1.25 | 5.0 | +3.75 (+300.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · FloorBoard · XP · TankReward | 1.25 | 5.0 | +3.75 (+300.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · WindowBoard · XP · AssistReward | 1.25 | 5.0 | +3.75 (+300.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · WindowBoard · XP · TankReward | 1.25 | 5.0 | +3.75 (+300.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · BarbedWire · XP · AssistReward | 1.75 | 5.0 | +3.25 (+185.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · BarbedWire · XP · TankReward | 1.75 | 5.0 | +3.25 (+185.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · CamoNetTent · XP · AssistReward | 1.75 | 5.0 | +3.25 (+185.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · CamoNetTent · XP · TankReward | 1.75 | 5.0 | +3.25 (+185.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · BremmerWall · XP · TankAssistReward | 1.875 | 5.0 | +3.125 (+166.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · HBlock · XP · TankAssistReward | 1.875 | 5.0 | +3.125 (+166.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · SandbagWall · XP · TankAssistReward | 1.875 | 5.0 | +3.125 (+166.7%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · FloorBoard · Cash · TankValue | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · FloorBoard · XP · DefaultReward | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · Radio · XP · TankAssistReward | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · Ramp · XP · TankAssistReward | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · WindowBoard · Cash · TankValue | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · WindowBoard · XP · DefaultReward | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · TallHBlock · XP · TankAssistReward | 2.75 | 5.0 | +2.25 (+81.8%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · BarbedWire · Cash · BaseValue | 14.0 | 5.0 | −9 (−64.3%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · CamoNetTent · Cash · BaseValue | 14.0 | 5.0 | −9 (−64.3%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · Gate · Cash · BaseValue | 500.0 | 200.0 | −300 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · Gate · XP · DefaultReward | 125.0 | 50.0 | −75 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · Gate · XP · AssistReward | 62.5 | 25.0 | −37.5 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · Gate · XP · TankReward | 62.5 | 25.0 | −37.5 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · FOBHacked · Cash · BaseValue | 2500.0 | 1000.0 | −1500 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Buildables | Buildables · BuildableDestroyed · TallHBlock · Cash · BaseValue | 44.0 | 20.0 | −24 (−54.5%) |

The other 57 literal value changes are in the [browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=rewards-unlocks&q=Buildables).

Non-numeric changes:

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_ChallengeRewards_SessionEvents_Buildables | XP · expression (18 rows) | `(BaseReward)` | `(BaseReward) * BuildProgress` | changed |
| DT_ChallengeRewards_SessionEvents_Buildables | Cash · expression (1 row) | `(BaseValue * AlignmentModifier * InstigatorZoneModifier * InstigatorZ…` | `((BaseValue + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppl…` | changed |
| DT_ChallengeRewards_SessionEvents_Buildables | XP · expression (1 row) | `(BaseReward)` | `(BaseReward + ((clamp(TotalFOBSupplies, 0, FOBSuppliesMax) / FOBSuppl…` | changed |

Rows added, by group:

| Group | Rows with added values |
|---|---:|
| Buildables.BuildableDestroyed | 36 |
| Buildables.FOBHacked | 1 |
| Buildables.FOBDoorClosed | 1 |

### Other numeric tables

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---:|---:|---:|
| DT_Factory01_Recipes | AK74M · production cost | 1280 | 640 | −640 (−50.0%) |
| DT_Factory01_Recipes | MP9 · production cost | 720 | 1100 | +380 (+52.8%) |
| DT_Factory01_Recipes | Vector · production cost | 2080 | 4480 | +2400 (+115.4%) |
| CRV_Challenges_Curves_PurchaseFromSupplyCrate_XP | Curve key 2 · time | 75.0 | 10.0 | −65 (−86.7%) |

Cosmetic sort indexes in `DT_CosmeticSets_Debug` also changed (4 rows, each +1), and one cosmetic set was added (`ChocolateChip`).

### Other tables with row-level changes

| Asset | Change |
|---|---|
| DT_GoldMarket | 27 rows added, 20 rows removed |
| DT_Achievements | 10 rows added |
| DT_PassiveMissionChallenges | 15 rows added |
| DT_Challenges_SessionEvents_Shared | 10 rows added |
| DT_Challenges_Curves_PurchaseFromSupplyCrate | 2 rows added |
| DT_ClientHotConfigs, DT_MockInvestments, DT_PassiveMissions, MoneyMan | noise-only (no real change) |

### State trees

| Group | State trees | Property changes |
|---|---:|---:|
| KOTH session-event state trees | 52 | 6,232 |
| Buildable session-event state trees | 10 | 860 |
| Other state trees | 20 | 466 |

Most of these changes are compiled-graph data: task and node indexes, offsets, bindings, and `LastCompiledEditorDataHash`. They are not tabulated here. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=rewards-unlocks&q=KOTH).

Non-zero input values in state tree instance data. Other scalar changes in these files are compiled indexes, offsets, hashes, or default zeros, and are not tabulated.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| ST_Challenges_SessionEvents_KOTH_DestroyVehicle_Assist_FOBSuppliedAssist | Inputs[0] · input value | (absent) | 0.04 | added |
| ST_Challenges_SessionEvents_KOTH_DestroyVehicle_Assist_LogisticAssist | Inputs[0] · input value | (absent) | 0.04 | added |
| ST_Challenges_SessionEvents_KOTH_DestroyVehicle_Assist_ReviveAssist | Inputs[0] · input value | (absent) | 0.04 | added |
| ST_Challenges_SessionEvents_KOTH_RevivePlayerContributor | Inputs[1] · input value | (absent) | 1.0 | added |
| ST_Challenges_SessionEvents_KOTH_SafeZoneEntered | Inputs[0] · input value | (absent) | 5.0 | added |

## New in Season 2

| Asset | Type | What it is |
|---|---|---|
| [CRV_Challenges_Curves_DeploySupplyCrate_XP](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DeploySupplyCrate_XP.json) | CurveFloat | Supply crate deploy XP curve |
| [CRV_Challenges_Curves_DestroySupplyCrate_Cash](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/CRV_Challenges_Curves_DestroySupplyCrate_Cash.json) | CurveFloat | Supply crate destroy cash curve |
| [DT_WagerActions](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerActions.json) | DataTable | Wager action table |
| [DT_WagerChallenges](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerChallenges.json) | DataTable | Wager objective challenge table |
| [DT_WagerConditions](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerConditions.json) | DataTable | Wager condition table |
| [DT_WagerObjectiveCatalog](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerObjectiveCatalog.json) | DataTable | Wager objective catalogue |
| [DT_WagerPricing](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerPricing.json) | DataTable | Wager stake pricing table |
| [ST_Challenges_Challenge_PassengersDelivered](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_PassengersDelivered.json) | StateTree | Passengers delivered challenge state tree |
| [ST_Challenges_Challenge_RewardedKills](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedKills.json) | StateTree | Rewarded kills challenge state tree |
| [ST_Challenges_Challenge_RewardedRevives](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedRevives.json) | StateTree | Rewarded revives challenge state tree |
| [ST_Challenges_Challenge_RewardedVehiclesDestroyed](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/StateTrees/ST_Challenges_Challenge_RewardedVehiclesDestroyed.json) | StateTree | Rewarded vehicles destroyed challenge state tree |
| [ST_Challenges_SessionEvents_Buildable_FOBDoorClosed](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/ST_Challenges_SessionEvents_Buildable_FOBDoorClosed.json) | StateTree | FOB door closed session event state tree |

UI data (count only): 2 added assets are Wager UI tables. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=rewards-unlocks&q=Wagers).

The Wagers system adds seven files under `Meta/Wagers`. Five are gameplay tables (pricing, actions, challenges, conditions, objective catalogue) and two are UI data.

## Removed in Season 2

No assets were removed in this area. Row-level removals are listed under each table above.

## See also

- [Meta: unlock trees, achievements and rewards]({{ '/content/Wardogs_Meta_v2.html' | relative_url }}#season-02-update)
- [Rewards: game-feature reward tables]({{ '/game-features/Wardogs_GameFeatures_Rewards_v2.html' | relative_url }}#season-02-update)
- [Challenges KOTH: session-event state trees]({{ '/game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.html' | relative_url }}#season-02-update)
- [Reward lookup: session events]({{ '/content/Wardogs_RewardLookup_SessionEvents_v1.html' | relative_url }}#season-02-update)
- [Tree reward track and platform mastery]({{ '/content/Wardogs_TreeRewardTrack_PlatformMastery_v1.html' | relative_url }}#season-02-update)

