---
title: "Game Modes & Maps changes"
parent: "Season 2 Changes"
nav_order: 8
description: "Game Modes & Maps: 30 assets added (TeamOffence and HotPotato modes), 2 removed, 8 modified with real changes, 2,285 property changes. Map warm-up data is most of the churn."
---

# Game Modes & Maps changes

Season 1 to Season 2 changes for the Game Modes & Maps area, from the area diff file. Every number below is copied from `assets/data/season-diff/game-modes-maps.json`.

| Measure | Count |
|---|---:|
| Assets added | 30 |
| Assets removed | 2 |
| Assets modified with real changes | 8 |
| Assets modified, not compared (Season 1 source truncated) | 1 |
| Noise-only modified assets (skipped: renamed keys, swapped key names or shifted references from the different Season 1 export) | 26 |
| Assets moved | 0 |
| Property changes | 2,285 (changed 59, added 439, removed 1,785, resequenced 2); 40 further entries are on the removed assets |

Full filterable list: [Game Modes & Maps in the change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps).

## Headline changes

### Map shader warm-up data (PSOWarming)

| Asset | Property changes | Added | Changed | Removed | Lists and paths touched |
|---|---:|---:|---:|---:|---|
| NorthAmerica_Detroit_KOTH_01 | 1,500 | 312 | 9 | 1,179 | GraphicsPSOs 1,364, ComputePSOs 136 |
| Europe_Madrid_KOTH_01 | 740 | 91 | 48 | 600 | GraphicsPSOs 656, ComputePSOs 84 |

These two map files list shader and pipeline warm-up entries (graphics and compute pipeline states, vertex factories) and material paths. They are compiled data and are not tabulated. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps&q=PSOWarmup).

`Kavkazi_Bakurani_KOTH_01` is listed as modified, but it was not compared. The Season 1 copy is truncated in the source, so it could not be read and compared with Season 2. The asset carries a note in the data to that effect.

### Shooting range and gym

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| B_MovingTarget (range target) | Subsystem class on the knock-down path | Class'CrosstalkAudioEventSubsystem' | Class'GameplayMessageSubsystem' | changed |
| B_MovingTarget (range target) | Child function and property entries | — | 28 added, 5 removed | changed |
| ShootingRange | GameFeatureAction_DataRegistrySource_1 | — | added | added |
| ShootingRangeTutorial | GameFeatureAction_DataRegistrySource_1 | — | added | added |

B_MovingTarget has 28 entries added, 5 removed, 2 changed and 1 resequenced. Most of the added entries are audio event functions, which are not described here.

### Loot and rewards

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · base | — | 5000.0 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · FriendlyModifier | — | -0.75 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · NeutralModifier | — | 0.25 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · OwnerModifier | — | 0.0 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · ModifierCZ | — | 1.5 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · ModifierHZ | — | 2.0 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · ModifierHZM | — | 2.0 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · InstigatorLocationRatioModifier | — | 0.5 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · TargetLocationRatioModifier | — | 0.5 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · AssistBaseModifier | — | 0.01 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · AssistScalingModifier | — | 0.99 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · CrewAssistModifier | — | 1.0 | added |
| DT_Reward_Cash_VehicleDestroyed | Rows.Vehicle.Variant.Land.Tracked.TNK_04.Default · LogisticAssistModifier | — | 0.25 | added |
| DT_LootableDataTable_VIPEscort_01 | VIPEscort01 · Fuelcan100 · unnamed property (`_aaabeefoaikdjpkadlp`) | — | False | added |
| DT_LootableDataTable_VIPEscort_01 | VIPEscort01 · AK · unnamed property (`_aaabeefoaikdjpkadlp`) | — | False | added |

### Removed game feature data

`MonkeyScore` and `TeamkillTracking` (both GameFeatureData) were removed. Their property entries are listed in the browser; the counts are 20 for MonkeyScore and 20 for TeamkillTracking.

## New in Season 2

| Asset | Type | What it is |
|---|---|---|
| AnimSet_HotPotato | BHAnimationSet | Hot Potato animation set |
| DA_ControlZone_Config_Africa | WDControlZoneConfigDataAsset | Control zone config, Africa |
| DA_ControlZone_Config_Russia | WDControlZoneConfigDataAsset | Control zone config, Russia |
| DA_ControlZoneConfig_SniperShowdown_NorthAmerica | WDControlZoneConfigDataAsset | Control zone config, Sniper Showdown, North America |
| DA_ControlZoneConfig_SniperShowdown_Russia | WDControlZoneConfigDataAsset | Control zone config, Sniper Showdown, Russia |
| DA_SightBlockers_Europe | WDSightBlockerBakedDataAsset | Sight blocker map data, Europe |
| DA_SightBlockers_Kavkazi | WDSightBlockerBakedDataAsset | Sight blocker map data, Kavkazi |
| DA_SightBlockers_NorthAmerica | WDSightBlockerBakedDataAsset | Sight blocker map data, North America |
| DA_SightBlockers_Russia | WDSightBlockerBakedDataAsset | Sight blocker map data, Russia |
| DT_ChallengeRewards_TeamOffence | DataTable | Team offence challenge rewards |
| DT_Challenges_SessionEvents_TeamOffence | DataTable | Team offence session event challenges |
| HotPotato | GameFeatureData | Hot Potato game mode (game feature data) |
| ID_HotPotato_Alpha | BHInventoryItemDefinition | Hot Potato item (Alpha) |
| ID_HotPotato_Bravo | BHInventoryItemDefinition | Hot Potato item (Bravo) |
| ID_HotPotato_Charlie | BHInventoryItemDefinition | Hot Potato item (Charlie) |
| Russia_Moscow_KOTH_01 | WDPSOWarmupDataAsset | Map shader warm-up data, Moscow KOTH |
| ServerSeeding | GameFeatureData | Server seeding feature (game feature data) |
| ST_Challenges_SessionEvents_TeamOffencePunish | StateTree | Team offence punish challenge state tree |
| ST_Challenges_SessionEvents_TeamOffenceVoter | StateTree | Team offence voter challenge state tree |
| TeamOffence | GameFeatureData | Team offence game mode (game feature data) |

UI data (count only): 9 added assets, including the Team Offence prompt and Hot Potato tracker data. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps&q=TeamOffence).

Audio (count only): 1 added asset. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps&q=Audio).

Team Offence and Hot Potato are new game-mode plugins. Team Offence adds challenge tables and a punish state tree and a voter state tree. Hot Potato adds game feature data and items.

## Removed in Season 2

| Type | Path |
|---|---|
| GameFeatureData | Wardogs/Plugins/GameFeatures/MonkeyScore/Content/MonkeyScore.json |
| GameFeatureData | Wardogs/Plugins/GameFeatures/TeamkillTracking/Content/TeamkillTracking.json |

## See also

- [Maps: map and mode details]({{ '/content/Wardogs_Maps_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Game mechanics: modes and scoring]({{ '/content/Wardogs_GameMechanics_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Control zone game feature]({{ '/game-features/Wardogs_GameFeatures_ControlZone_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Shooting range game feature]({{ '/game-features/Wardogs_GameFeatures_ShootingRange_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Shooting range tutorial game feature]({{ '/game-features/Wardogs_GameFeatures_ShootingRangeTutorial_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Teamkill tracking game feature]({{ '/game-features/Wardogs_GameFeatures_TeamkillTracking_v2.html' | relative_url }}#season-02-update-2026-10-15)

