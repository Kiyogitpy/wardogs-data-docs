---
title: "Game Modes & Maps changes"
parent: "Season 2 Changes"
nav_order: 8
description: "Game Modes & Maps: 30 assets added (TeamOffence and HotPotato modes), 2 removed, 8 modified with real changes, 5,331 property changes. Map warm-up data is most of the churn."
---

# Game Modes & Maps changes

Season 1 to Season 2 changes for the Game Modes & Maps area, from the area diff file. Every number below is copied from `assets/data/season-diff/game-modes-maps.json`.

| Measure | Count |
|---|---:|
| Assets added | 30 |
| Assets removed | 2 |
| Assets modified with real changes | 8 |
| Assets modified, not compared (Season 1 source truncated) | 1 |
| Noise-only modified assets (skipped, no real change) | 26 |
| Assets moved | 0 |
| Property changes | 5,331 (changed 967, added 1,511, removed 2,852, resequenced 1); 40 further entries are on the removed assets |

Full filterable list: [Game Modes & Maps in the change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps).

## Headline changes

### Map shader warm-up data (PSOWarming)

| Asset | Property changes | Added | Changed | Removed | Lists and paths touched |
|---|---:|---:|---:|---:|---|
| NorthAmerica_Detroit_KOTH_01 | 2,828 | 710 | 546 | 1,572 | GraphicsPSOs 2,692, ComputePSOs 136 |
| Europe_Madrid_KOTH_01 | 2,454 | 763 | 419 | 1,272 | GraphicsPSOs 2,370, ComputePSOs 84 |

These two map files list shader and pipeline warm-up entries (graphics and compute pipeline states, vertex factories) and material paths. They are compiled data and are not tabulated. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps&q=PSOWarmup).

`Kavkazi_Bakurani_KOTH_01` is listed as modified, but it was not compared. The Season 1 copy is truncated in the source, so it could not be read and compared with Season 2. The asset carries a note in the data to that effect.

### Shooting range and gym

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| B_MovingTarget (range target) | Subsystem class on the knock-down path | Class'CrosstalkAudioEventSubsystem' | Class'GameplayMessageSubsystem' | changed |
| B_MovingTarget (range target) | Child function and property entries | — | 30 added, 7 removed | changed |
| ShootingRange | GameFeatureAction_DataRegistrySource_1 | — | added | added |
| ShootingRangeTutorial | GameFeatureAction_DataRegistrySource_1 | — | added | added |

B_MovingTarget has 30 entries added, 7 removed, 2 changed and 1 resequenced. Most of the added entries are audio event functions, which are not described here.

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
| [AnimSet_HotPotato](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/AnimSet_HotPotato.json) | BHAnimationSet | Hot Potato animation set |
| [DA_ControlZone_Config_Africa](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Africa.json) | WDControlZoneConfigDataAsset | Control zone config, Africa |
| [DA_ControlZone_Config_Russia](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Russia.json) | WDControlZoneConfigDataAsset | Control zone config, Russia |
| [DA_ControlZoneConfig_SniperShowdown_NorthAmerica](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_NorthAmerica.json) | WDControlZoneConfigDataAsset | Control zone config, Sniper Showdown, North America |
| [DA_ControlZoneConfig_SniperShowdown_Russia](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_SniperShowdown_Russia.json) | WDControlZoneConfigDataAsset | Control zone config, Sniper Showdown, Russia |
| [DA_SightBlockers_Europe](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/Europe/DA_SightBlockers_Europe.json) | WDSightBlockerBakedDataAsset | Sight blocker map data, Europe |
| [DA_SightBlockers_Kavkazi](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/kavkazi/DA_SightBlockers_Kavkazi.json) | WDSightBlockerBakedDataAsset | Sight blocker map data, Kavkazi |
| [DA_SightBlockers_NorthAmerica](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/NorthAmerica/DA_SightBlockers_NorthAmerica.json) | WDSightBlockerBakedDataAsset | Sight blocker map data, North America |
| [DA_SightBlockers_Russia](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/SightBlockers/Russia/DA_SightBlockers_Russia.json) | WDSightBlockerBakedDataAsset | Sight blocker map data, Russia |
| [DT_ChallengeRewards_TeamOffence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/DT_ChallengeRewards_TeamOffence.json) | DataTable | Team offence challenge rewards |
| [DT_Challenges_SessionEvents_TeamOffence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/DT_Challenges_SessionEvents_TeamOffence.json) | DataTable | Team offence session event challenges |
| [HotPotato](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/HotPotato.json) | GameFeatureData | Hot Potato game mode (game feature data) |
| [ID_HotPotato_Alpha](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/Items/ID_HotPotato_Alpha.json) | BHInventoryItemDefinition | Hot Potato item (Alpha) |
| [ID_HotPotato_Bravo](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/Items/ID_HotPotato_Bravo.json) | BHInventoryItemDefinition | Hot Potato item (Bravo) |
| [ID_HotPotato_Charlie](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/Items/ID_HotPotato_Charlie.json) | BHInventoryItemDefinition | Hot Potato item (Charlie) |
| [Russia_Moscow_KOTH_01](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Russia_Moscow_KOTH_01.json) | WDPSOWarmupDataAsset | Map shader warm-up data, Moscow KOTH |
| [ServerSeeding](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ServerSeeding/Content/ServerSeeding.json) | GameFeatureData | Server seeding feature (game feature data) |
| [ST_Challenges_SessionEvents_TeamOffencePunish](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/ST_Challenges_SessionEvents_TeamOffencePunish.json) | StateTree | Team offence punish challenge state tree |
| [ST_Challenges_SessionEvents_TeamOffenceVoter](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/ST_Challenges_SessionEvents_TeamOffenceVoter.json) | StateTree | Team offence voter challenge state tree |
| [TeamOffence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/TeamOffence.json) | GameFeatureData | Team offence game mode (game feature data) |

UI data (count only): 9 added assets, including the Team Offence prompt and Hot Potato tracker data. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps&q=TeamOffence).

Audio (count only): 1 added asset. Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=game-modes-maps&q=Audio).

Team Offence and Hot Potato are new game-mode plugins. Team Offence adds challenge tables and a punish state tree and a voter state tree. Hot Potato adds game feature data and items.

## Removed in Season 2

| Type | Path |
|---|---|
| GameFeatureData | Wardogs/Plugins/GameFeatures/MonkeyScore/Content/MonkeyScore.json |
| GameFeatureData | Wardogs/Plugins/GameFeatures/TeamkillTracking/Content/TeamkillTracking.json |

## See also

- [Maps: map and mode details]({{ '/content/Wardogs_Maps_v2.html' | relative_url }}#season-02-update)
- [Game mechanics: modes and scoring]({{ '/content/Wardogs_GameMechanics_v2.html' | relative_url }}#season-02-update)
- [Control zone game feature]({{ '/game-features/Wardogs_GameFeatures_ControlZone_v2.html' | relative_url }}#season-02-update)
- [Shooting range game feature]({{ '/game-features/Wardogs_GameFeatures_ShootingRange_v2.html' | relative_url }}#season-02-update)
- [Shooting range tutorial game feature]({{ '/game-features/Wardogs_GameFeatures_ShootingRangeTutorial_v2.html' | relative_url }}#season-02-update)
- [Teamkill tracking game feature]({{ '/game-features/Wardogs_GameFeatures_TeamkillTracking_v2.html' | relative_url }}#season-02-update)

