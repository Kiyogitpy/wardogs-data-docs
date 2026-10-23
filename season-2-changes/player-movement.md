---
title: "Player & Movement changes"
parent: "Season 2 Changes"
nav_order: 3
description: "Parachutes, spotting challenge rewards and input mappings: 2 assets added, 25 modified with real changes, 706 property changes."
---

# Player & Movement changes

Movement, parachutes, spotting challenge rewards and input mappings: what changed between Season 1 and Season 2.

- **Added:** 2 assets
- **Removed:** 0 assets
- **Modified with real changes:** 25 assets (13 more are noise-only and not listed: only renamed keys or shifted references)
- **Moved:** 0 assets
- **Property changes:** 706

Movement effect and cue changes and compiled binding indexes are counted, not listed.

## Headline changes

### Parachutes (13 rows)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| CRV_ParachutePunishment_Damage | Keys[1].Time | 1111.0 | 1700.0 | +589.0 (+53.0%) |
| CRV_ParachutePunishment_Damage | Keys[1].LeaveTangent | 0.0 | 0.05540166 | +0.055402 (n/a) |
| DA_ParachuteMovement_Basic | VerticalDragCoefficient | — | 1.75 | added |
| DA_ParachuteMovement_Basic | OpenDuration | — | 2.0 | added |
| DA_ParachuteMovement_Basic | MinFallHeightBeforeAbleToParachute | 100.0 | 400.0 | +300.0 (+300.0%) |
| DA_ParachuteMovement_Basic | MinHeightOpenParachuteFromGround | — | 1000.0 | added |
| DA_ParachuteMovement_Sport | VerticalDragCoefficient | — | 1.75 | added |
| DA_ParachuteMovement_Sport | PullUpDragAcceleration | 825.0 | 400.0 | −425.0 (−51.5%) |
| DA_ParachuteMovement_Sport | OpenDuration | — | 2.0 | added |
| DA_ParachuteMovement_Sport | MinFallHeightBeforeAbleToParachute | 100.0 | 400.0 | +300.0 (+300.0%) |
| DA_ParachuteMovement_Sport | MinHeightOpenParachuteFromGround | — | 1000.0 | added |
| DT_VendorData_Ext_Parachutes | Price (Parachute.Sport) | 1000.0 | 700.0 | −300.0 (−30.0%) |
| DT_VendorData_Ext_Parachutes | Price (Parachute.Basic) | 100.0 | 500.0 | +400.0 (+400.0%) |

[All 55 parachute changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=player-movement&q=Parachute)

### Spotting challenge rewards (70 values changed)

Each row is one reward value: event (Added or Removed), challenge row, resource, and variable. Shown: the 30 largest changes by percentage (values that start at 0 are listed first). The other 40 values are in the browser.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_ChallengeRewards_SessionEvents_Spotting | Added · Claymore · XP.Role · RefreshedReward | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · ATMine · XP.Role · RefreshedReward | 2.5 | 5.0 | +2.5 (+100.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · TNK_01.Artillery · Currency.Cash · DefaultReward | 8000.0 | 1200.0 | −6800.0 (−85.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · TNK_01.Artillery · Currency.Cash · DefaultReward | 1500.0 | 400.0 | −1100.0 (−73.3%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · TNK_01.Artillery · Currency.Cash · RefreshedReward | 750.0 | 200.0 | −550.0 (−73.3%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · MistralAA · Currency.Cash · DefaultReward | 200.0 | 75.0 | −125.0 (−62.5%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · MistralAA · Currency.Cash · RefreshedReward | 100.0 | 40.0 | −60.0 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · MistralAA · XP.Role · DefaultReward | 50.0 | 20.0 | −30.0 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · MistralAA · XP.Role · RefreshedReward | 25.0 | 10.0 | −15.0 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · Mortar · XP.Role · DefaultReward | 50.0 | 20.0 | −30.0 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Added · Mortar · XP.Role · RefreshedReward | 25.0 | 10.0 | −15.0 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · MistralAA · Currency.Cash · DefaultReward | 1000.0 | 400.0 | −600.0 (−60.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · TNK_01.AntiAir · Currency.Cash · DefaultReward | 5000.0 | 2100.0 | −2900.0 (−58.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · MistralAA · XP.Role · DefaultReward | 125.0 | 60.0 | −65.0 (−52.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · MistralAA · XP.Role · KilledByEnemyReward | 62.5 | 30.0 | −32.5 (−52.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Mortar · XP.Role · DefaultReward | 125.0 | 60.0 | −65.0 (−52.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Mortar · XP.Role · KilledByEnemyReward | 62.5 | 30.0 | −32.5 (−52.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Phalanx · Currency.Cash · DefaultReward | 1500.0 | 725.0 | −775.0 (−51.7%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Player · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Bobcat · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Kodiak · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · LittleBird · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Huey · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Blackhawk · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Havoc · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · SpawnVehicle · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · TNK_01.Heavy · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · TNK_01.Artillery · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · TNK_01.AntiAir · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |
| DT_ChallengeRewards_SessionEvents_Spotting | Removed · Humvee · Currency.Cash · KilledByEnemyFactor | 0.5 | 0.25 | −0.25 (−50.0%) |

214 reward rows were added to this table across 23 challenge groups. They are listed in the browser.

[All 308 spotting challenge changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=player-movement&q=SessionEvents_Spotting)

### Input mappings (24 rows)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| IMC_Action_ThrowExplosive | DefaultKeyMappings.Mappings[4].Key.KeyName | Gamepad_LeftShoulder | Gamepad_FaceButton_Left | changed |
| IMC_LadderClimbing | DefaultKeyMappings.Mappings[0].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_LadderClimbing | DefaultKeyMappings.Mappings[1].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_LadderClimbing | DefaultKeyMappings.Mappings[2].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_LadderClimbing | DefaultKeyMappings.Mappings[3].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_MoverPlayer | DefaultKeyMappings.Mappings[16].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_MoverPlayer | DefaultKeyMappings.Mappings[17].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_Player_BodyDrag | DefaultKeyMappings.Mappings[0].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_Player_BodyDrag | DefaultKeyMappings.Mappings[1].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_Player_Downed | DefaultKeyMappings.Mappings[6].Key.KeyName | Gamepad_Special_Right | Gamepad_FaceButton_Left | changed |
| IMC_Player_Swimming | DefaultKeyMappings.Mappings[0].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_Player_Swimming | DefaultKeyMappings.Mappings[1].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_PlayerController | DefaultKeyMappings.Mappings[7].Key.KeyName | Gamepad_Special_Left | Gamepad_Special_Right | changed |
| IMC_PlayerController | DefaultKeyMappings.Mappings[9].Key.KeyName | None | L | changed |
| IMC_PlayerController | DefaultKeyMappings.Mappings[14].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_PlayerController | DefaultKeyMappings.Mappings[15].SettingBehavior | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings | changed |
| IMC_PlayerController | DefaultKeyMappings.Mappings[32] | — | {"Triggers": [], "Modifiers": [], "Action": {"ObjectName": "BHInputAction'IA_UI_Map_ToggleZoomPreset'", "ObjectPath": "/Game/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_UI_Map_ToggleZoomPreset.0"}, "Key": {"KeyName": "Gamepad_Special_Left"}, "SettingBehavior": "EPlayerMappableKeySettingBehaviors::InheritSettingsFromAction", "PlayerMappableKeySettings": null} | added |
| IMC_Spotting | DefaultKeyMappings.Mappings[3] | — | {"Triggers": [], "Modifiers": [{"ObjectName": "WDDeadZoneInputModifier'IMC_Spotting:WDDeadZoneInputModifier_0'", "ObjectPath": "/Spotting/Data/Input/IMC_Spotting.3"}], "Action": {"ObjectName": "BHInputAction'IA_Player_Holdable_SecondaryUse_Release'", "ObjectPath": "/Game/GameMechanics/Player/PlayerCharacter/Inputs/TaggedActions/IA_Player_Holdable_SecondaryUse_Release.0"}, "Key": {"KeyName": "Gamepad_LeftTriggerAxis"}, "SettingBehavior": "EPlayerMappableKeySettingBehaviors::InheritSettingsFromAction", "PlayerMappableKeySettings": null} | added |
| IMC_Spotting | DefaultKeyMappings.Mappings[5].Modifiers[ObjectName=WDDeadZoneInputModifier'IMC_Spotting:WDDeadZoneInputModifier_0'] | {"ObjectName": "WDDeadZoneInputModifier'IMC_Spotting:WDDeadZoneInputModifier_0'", "ObjectPath": "/Spotting/Data/Input/IMC_Spotting.3"} | — | removed |
| IMC_Spotting | DefaultKeyMappings.Mappings[5].Action.ObjectName | BHInputAction'IA_Player_Holdable_SecondaryUse_Release' | BHInputAction'IA_Weapon_Reload' | changed |
| IMC_Spotting | DefaultKeyMappings.Mappings[5].Action.ObjectPath | /Game/GameMechanics/Player/PlayerCharacter/Inputs/TaggedActions/IA_Player_Holdable_SecondaryUse_Release.0 | /Game/Weapons/Input/IA_Weapon_Reload.0 | changed |
| IMC_Spotting | DefaultKeyMappings.Mappings[5].Key.KeyName | Gamepad_LeftTriggerAxis | R | changed |
| IMC_Spotting | DefaultKeyMappings.Mappings[6] | — | {"Triggers": [], "Modifiers": [], "Action": {"ObjectName": "BHInputAction'IA_Weapon_Reload'", "ObjectPath": "/Game/Weapons/Input/IA_Weapon_Reload.0"}, "Key": {"KeyName": "Gamepad_FaceButton_Left"}, "SettingBehavior": "EPlayerMappableKeySettingBehaviors::InheritSettingsFromAction", "PlayerMappableKeySettings": null} | added |
| IMC_Tipping | DefaultKeyMappings.Mappings[3] | — | {"Triggers": [], "Modifiers": [], "Action": {"ObjectName": "BHInputAction'IA_Tip_Reject'", "ObjectPath": "/Game/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Tip_Reject.0"}, "Key": {"KeyName": "Gamepad_Special_Left"}, "SettingBehavior": "EPlayerMappableKeySettingBehaviors::InheritSettingsFromAction", "PlayerMappableKeySettings": null} | added |

[All 24 input mapping changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=player-movement&q=IMC_)

### Player character components (12 rows)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_PlayerCharacterComponents | SkeletalMeshComponent_0 · RelativeLocation | — | {"X": 0.0, "Y": 0.0, "Z": -96.0} | added |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_0 · RelativeRotation | — | {"Pitch": 0.0, "Yaw": -90.0, "Roll": 0.0} | added |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_0 · RelativeScale3D | {"X": 0.0, "Y": 0.0, "Z": -96.0} | — | removed |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_0 · ComponentVelocity | {"X": 0.0, "Y": -90.0, "Z": 0.0} | — | removed |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_1 · RelativeLocation | — | {"X": 15.628124, "Y": 0.0, "Z": -96.0} | added |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_1 · RelativeScale3D | {"X": 15.628124, "Y": 0.0, "Z": -96.0} | — | removed |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_2 · RelativeLocation | — | {"X": -8.464119, "Y": 0.0, "Z": -95.50413} | added |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_2 · RelativeScale3D | {"X": -8.464119, "Y": 0.0, "Z": -95.50413} | — | removed |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_3 · RelativeLocation | — | {"X": 0.0, "Y": 0.0, "Z": -171.5} | added |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_3 · RelativeRotation | — | {"Pitch": 0.0, "Yaw": -90.0, "Roll": 0.0} | added |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_3 · RelativeScale3D | {"X": 0.0, "Y": 0.0, "Z": -171.5} | — | removed |
| DA_PlayerCharacterComponents | SkeletalMeshComponent_3 · ComponentVelocity | {"X": 0.0, "Y": -90.0, "Z": 0.0} | — | removed |

## Other changes

- `DA_DefaultPlayerMovementAudioConfiguration` (WDCharacterMovementEffectsComponentConfigurationDataAsset): 42 changed.
- `DA_MaterialTrackerData_Spotting` (WDUISpottingMaterialTrackerDataAsset): 3 added.
- `DA_Tracker_Map_Spotting` (WDUISpottingTargetMapTrackerData): 2 added.
- `DA_Tracker_Spatial_Spotting` (WDUISpottingSpatialTrackerData): 8 added, 1 changed, 31 removed.
- `DT_Challenges_SessionEvents_KOTH_Spotting` (DataTable): 2 added.
- `DT_Cosmetics_Season01_Emotes` (DataTable): 3 added, 3 removed.
- `DT_RewardLookup_SessionEvent_Spotting_Added` (DataTable): 4 added, 37 changed.
- `DT_RewardLookup_SessionEvent_Spotting_Removed` (DataTable): 4 added, 37 changed.
- `ST_Challenges_SessionEvents_KOTH_Spotting_Added` (StateTree): 6 added, 79 changed, 1 removed.
- `ST_Challenges_SessionEvents_KOTH_Spotting_Removed` (StateTree): 6 added, 79 changed, 1 removed.

The two `ST_Challenges_SessionEvents_KOTH_Spotting_*` state trees have 132 numeric values that change. They are compiled property-binding indexes and hashes, not balance changes. They are in the browser.

The `DA_DefaultPlayerMovementAudioConfiguration` asset has 42 changes to effect and gameplay cue tags and effect flags. They are not listed here; they are in the browser.

[All 615 spotting changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=player-movement&q=Spotting)

The UI tracker assets (DA_Tracker_* and DA_MaterialTrackerData_Spotting) have 45 changes, and DA_DefaultPlayerMovementAudioConfiguration has 42. Both are left out of the tables and are in the browser.

[All 45 UI tracker changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=player-movement&q=Tracker) · [All 42 audio configuration changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=player-movement&q=AudioConfiguration)

## New in Season 2 (2 assets)

| Asset | Type | Identification |
|---|---|---|
| [CRV_DamageIndicator_IntensityResponse](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_DamageIndicator_IntensityResponse.json) | CurveFloat | 1 exports |
| [DT_PingTypes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/Pings/DT_PingTypes.json) | DataTable | 1 exports |

## Removed in Season 2 (0 assets)

None.

## Moved in Season 2 (0 assets)

None.

## See also

- [Parachutes game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Parachutes_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Spotting game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Spotting_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [KOTH challenges game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Reward lookup session events, Season 02 update]({{ '/content/Wardogs_RewardLookup_SessionEvents_v1.html' | relative_url }}#season-02-update-2026-10-15)
