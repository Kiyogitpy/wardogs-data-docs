---
title: "Spotting (feature)"
parent: "Game Features"
---

# Wardogs — GameFeature: Spotting Reference (v2)
*Extracted from cooked game data via CUE4Parse (build `++Wardogs+Live-CL-509546`, UE 5.7.4). Source: [`Wardogs/Plugins/GameFeatures/Spotting/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Spotting) (28 JSON files). Scripted pass over every file, then spot-checked against the reward and tracker tables.*

> **Overlap with the main doc:** the flat Spotting cash min and max values (15 / 275 and 50 / 500) are in `Wardogs_Rewards_and_Progression_v2.md`, section 9. This doc adds the **per-target challenge formulas**, the **modifier table** behind those min and max values, the **variant lookups**, **skills**, **feed strings**, **trackers**, **input bindings** and **audio** for spotting.

---

## 1. What "Spotting" Covers

Spotting lets a player mark an enemy target so that it shows on the map and in the world. Each spot is a **challenge event**. Two events exist:

| Event | Feed text | Meaning (inferred from names) |
|---|---|---|
| **Added** (`Challenges.Rewards.Spotting.Added.*`) | "Target Spotted" | A target becomes spotted. |
| **Removed** (`Challenges.Rewards.Spotting.Removed.*`) | "Spotted Target Destroyed" | A spotted target is removed from the spotted list, usually because it was destroyed. |

Both events pay out, and both are split by target type (player, vehicle, buildable, supply crate, stationary weapon). Assist and owner credit come from separate match-score tags (section 4).

---

## 2. Package Contents

| Group | Files | Contents |
|---|---|---|
| Root bundle | 1 | [`Spotting.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Spotting.json) (`GameFeatureData`): data registry and sources, a gameplay cue path, components, and a widget element. |
| Challenge rewards | 2 | [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) (44 rows, the calculator). [`DT_Challenges_SessionEvents_KOTH_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_Spotting.json) (0 rows, challenge definitions). |
| Variant lookups | 2 | [`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json) (47 rows), `..._Removed` (47 rows). |
| State trees | 2 | [`ST_Challenges_SessionEvents_KOTH_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/ST_Challenges_SessionEvents_KOTH_Spotting_Added.json) (22 states), `..._Removed` (21 states). Each has a `WDChallengeStateTreeSchema`. |
| Match-score rewards | 2 | [`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json) (4 rows, live min and max values). [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json) (3 rows, all zero). |
| Skills | 1 | [`DT_Skills_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Skills/DT_Skills_Spotting.json) (2 rows, Recon skills). |
| Feed | 2 | [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json) (3), [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json) (3). |
| Trackers and HUD | 8 | Map and spatial trackers (`DA_` and `DT_`), material tracker, overlay, and the dynamic offset curve. |
| Input | 2 | [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json), [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json). |
| Audio | 6 | [`AE_Comms_Spotted`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted.json), [`AE_Comms_Spotted_VehicleEmpty`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted_VehicleEmpty.json), [`AE_UX_Spotted_Target`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotted_Target.json), [`AE_UX_Spotting_Start`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Start.json), `_Stop`, `_Complete`. |

---

## 3. Challenge Calculator ([`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json), 44 rows)

There are **22 Added rows and 22 Removed rows**, one per target type. Each row has a cash resource and an XP resource.

Target types (same 22 names on both events): `Player`, `Bobcat`, `Kodiak`, `LittleBird`, `Huey`, `Blackhawk`, `Havoc`, `SpawnVehicle`, `TNK_01.Heavy`, `TNK_01.Artillery`, `TNK_01.AntiAir`, `Humvee`, `DuneBuggy`, `Ural`, [`Claymore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Claymore/Content/Claymore.json), `ATMine`, `BuildableHotZoneMagnet`, `FOB`, `SupplyCrate`, `MistralAA`, `Phalanx`, `Mortar`.

### 3a. Formulas

| Event | Resource | Expression |
|---|---|---|
| Added (all 22) | Cash | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward * AlignmentModifier * TargetZoneModifier)` |
| Added (all 22) | XP | `(1 - (clamp(LastVictimCount, 0, LastVictimCountMax) * LastVictimReductionModifier)) * (BaseReward)` |
| Removed (all 22) | Cash | `BaseReward * AlignmentModifier * TargetZoneModifier * DestroyedByTeamModifier` |
| Removed (all 22) | XP | `(BaseReward)` |

Note the difference. **Added** pays down by how many times the target was already spotted (the "last victim" count). **Removed** has no victim reduction, but adds `DestroyedByTeamModifier`.

### 3b. Selectors

| Variable | Default | Options (condition → variable) | Rows |
|---|---|---|---|
| `BaseReward` | `DefaultReward` | `ALL(Challenges.Rewards.Spotting.Refreshed)` → `RefreshedReward` | all 44 |
| `BaseReward` | `DefaultReward` | `ALL(Challenges.Context.KilledByEnemy)` → `KilledByEnemyReward` | 22 Removed rows |
| `AlignmentModifier` | `DefaultFactor` | `ANY(Vehicle.Faction.Friendly, FriendlyKill)` → `FriendlyFactor`; `ANY(Vehicle.Faction.Neutral)` → `NeutralFactor`; `ANY(Vehicle.Faction.Hostile)` → `HostileFactor` | all 44 |
| `TargetZoneModifier` | `DefaultFactor` | `ALL(HotZoneMagnetActive, Target.InHotZone)` → `HotZoneMagnetFactor`; `ALL(Target.InHotZone)` → `HotZoneFactor`; `ALL(Target.InControlZone)` → `ControlZoneFactor` | all 44 |
| `DestroyedByTeamModifier` | `DefaultFactor` | `ALL(Challenges.Context.KilledByEnemy)` → `KilledByEnemyFactor` | 22 Removed rows |

Points to note:
- `AlignmentModifier` picks a factor by **faction of the target vehicle** (friendly, neutral, hostile). A friendly target also matches `FriendlyKill`.
- `DestroyedByTeamModifier` is keyed on `KilledByEnemy`, which reads oddly. The name suggests the factor applies when the spotted target was killed by an enemy. The option's name fits the Removed event, so this doc uses it as written.
- The `Player` row is in the calculator but **has no variant lookup row** (section 5).

The numeric values behind `BaseReward`, the faction factors and the zone factors are **not in this table**. The `DefaultReward`, `RefreshedReward` and `KilledByEnemyReward` names point to values held in the shared challenge tables (`Wardogs_Rewards_and_Progression_v2.md`, section 15).

---

## 4. Match-Score Payouts

### 4a. Live min and max ([`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json), 4 rows)

These are the values the v2 doc's section 9 quotes. The modifier columns are the part that doesn't appear there.

| Row | Base | Owner modifier | Assist base | Assist scaling |
|---|---|---|---|---|
| `Meta.Progression.Context.MatchScore.SpottedMin` | **15** | 1.0 | 0.5 | 0.2 |
| `Meta.Progression.Context.MatchScore.SpottedMax` | **275** | 0.2 | 0.1 | 0.2 |
| `Meta.Progression.Context.MatchScore.SpottedDestroyedMin` | **50** | 1.0 | 0.5 | 1.0 |
| `Meta.Progression.Context.MatchScore.SpottedDestroyedMax` | **500** | 0.75 | 0.5 | 0.75 |

All four rows also carry these modifiers at 1.0: `FriendlyModifier`, `NeutralModifier`, `ModifierCZ`, `ModifierHZ`, `ModifierHZM`, `InstigatorLocationRatioModifier`, `TargetLocationRatioModifier`, `CrewAssistModifier`, `LogisticAssistModifier`.

So the **owner** (the player who spotted) gets a reduced share of the max value (20% for a spot, 75% for a destroy). The **assist** share is driven by `AssistBaseModifier` and `AssistScalingModifier`. The spread between min and max is set by the assist-scaling curve (in the v2 doc's terms).

### 4b. Placeholder rows ([`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json), 3 rows, all zero)

`Meta.Progression.Resources.MatchScore.SpottingOwner`, `...SpottingAssist` and `...SpottingDestroyed`. Each has `ResourceValue = 0.0`, `ResourceTag = Attribute.Meta.Currency.Cash`. These are the same stale layer the v1 Rewards doc found: the live numbers are in [`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json) above.

---

## 5. Variant Lookups ([`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json) and `_Removed`)

Each lookup has 47 rows and maps the spotted variant to its reward tag. The Added and Removed tables are identical in layout. Only the reward tag prefix differs (`.Added.` or `.Removed.`).

| Reward tag | Variants | Variant tags |
|---|---|---|
| `Spotting.*.Kodiak` | 3 | `Vehicle.Variant.Land.Wheeled.Kodiak.Default / .MachineGun / .Pickup` |
| `Spotting.*.LittleBird` | 3 | `Vehicle.Variant.Air.Rotary.Littlebird.Default / .MountedMachineGuns / .RocketPods` |
| `Spotting.*.Huey` | 2 | `Vehicle.Variant.Air.Rotary.ROT_01.Default / .MountedMachineGuns` |
| `Spotting.*.Blackhawk` | 2 | `Vehicle.Variant.Air.Rotary.ROT_04.Default / .MountedMachineGuns` |
| `Spotting.*.Havoc` | 1 | `Vehicle.Variant.Air.Rotary.Havoc.Default` |
| `Spotting.*.SpawnVehicle` | 3 | `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar / .Manticore / .Valkyra` |
| `Spotting.*.TNK_01.Heavy` | 1 | `Vehicle.Variant.Land.Tracked.TNK_01.Heavy` |
| `Spotting.*.TNK_01.Artillery` | 1 | `Vehicle.Variant.Land.Tracked.TNK_01.Artillery` |
| `Spotting.*.TNK_01.AntiAir` | 1 | `Vehicle.Variant.Land.Tracked.TNK_01.AntiAir` |
| `Spotting.*.Bobcat` | 1 | `Vehicle.Variant.Land.Wheeled.Bobcat.Default` |
| `Spotting.*.Humvee` | 3 | `Vehicle.Variant.Land.Wheeled.Humvee.Default / .MachineGun / .Minigun` |
| `Spotting.*.DuneBuggy` | 1 | `Vehicle.Variant.Land.Wheeled.DuneBuggy.Default` |
| `Spotting.*.Ural` | 3 | `Vehicle.Variant.Land.Wheeled.Ural.Battle / .Attack / .Default` |
| `Spotting.*.Claymore` | 1 | `Id.Item.Claymore` |
| `Spotting.*.ATMine` | 1 | `ID.Item.ATMine` |
| `Spotting.*.FOB` | 1 | `Id.Buildable.FOB` |
| `Spotting.*.BuildableHotZoneMagnet` | 1 | `Id.Buildable.HotzoneMagnet` |
| `Spotting.*.SupplyCrate` | 10 | All `ID.Item.VehicleSupplyCrate.*` variants (Free, Container.Free, Small, Small.Armoured, Large, Large.Armoured, Pallet types) |
| `Spotting.*.MistralAA` | 5 | `Vehicle.Variant.Stationary.MistralAA`, `Vehicle.Variant.Stationary.Loudspeaker`, `Id.Buildable.Radio`, `Id.Buildable.RepairStation`, `Id.Buildable.RefuelStation` |
| `Spotting.*.Mortar` | 2 | `Vehicle.Variant.Stationary.Mortar`, `Vehicle.Variant.Stationary.STN_05` |
| `Spotting.*.Phalanx` | 1 | `Vehicle.Variant.Stationary.Phalanx` |

Observations:
- **21 target reward tags** appear in each lookup. The `Player` target is not in either lookup. The player row must be selected by a different path, which was not traced.
- The `MistralAA` reward tag covers two stationary vehicles and three buildables (Radio, RepairStation, RefuelStation). They all pay the same.
- **Mortar and STN_05** share one reward tag (`Spotting.*.Mortar`).

---

## 6. State Trees

Both trees are the KOTH-prefixed challenge runners for spotting. They follow the same challenge pipeline as the KOTH state trees (`Wardogs_GameFeatures_Challenges_KOTH_v2.md`, section 3a).

| Tree | States | Tags |
|---|---|---|
| `ST_..._Spotting_Added` | 22 | `Event.StateTree.Spotting.Added`, `Challenges.Rewards.Spotting.Added.Player` |
| `ST_..._Spotting_Removed` | 21 | `Event.StateTree.Spotting.Removed`, `Challenges.Rewards.Spotting.Removed.Player`, `Analytics.Player.Assists` |

The `Removed` tree is the only one that carries the `Analytics.Player.Assists` tag, which fits its "destroyed" meaning. The `Added` tree carries no analytics tag.

---

## 7. Skills ([`DT_Skills_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Skills/DT_Skills_Spotting.json), 2 rows)

Both skills are **Recon** role skills.

| Skill tag | Skill key | Gameplay effect | Attribute | Magnitude source |
|---|---|---|---|---|
| `Meta.Role.Recon.IncreasedSpottedTime` | `Meta.Skill.Character` | `GE_Spotting_IncreasedSpottedTime` | `Attribute.Gameplay.Spotting.SpottedTimeMultiplier` | Base 1.0, scaled by curve [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), row `IncreasedSpottedTime` |
| `Meta.Role.Recon.IncreasedSpottingDuration` | `Meta.Skill.Item` | `GE_Spotting_IncreasedSpottingDuration` | `Attribute.Gameplay.Spotting.SpottingDurationMultiplier` | Base 1.0, scaled by curve [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), row `IncreasedSpottingDuration` |

The skill attribute is a multiplier on how long a spot lasts (`SpottedTimeMultiplier` on the target side, `SpottingDurationMultiplier` on the spotter side). The actual per-rank values are in [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), which is outside this folder.

---

## 8. Feed Strings

### 8a. Challenge feed ([`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json), 3 rows)

| Feed tag | Default text | Conditional text (tag → text, audio) |
|---|---|---|
| `Challenges.Rewards.Spotting.Added` | Target Spotted | `ANY(Challenges.Rewards.Spotting.Refreshed)` → "Target Spotted Refreshed" (no audio override) |
| `Challenges.Rewards.Spotting.Refreshed` | Target Spotted Refreshed | none |
| `Challenges.Rewards.Spotting.Removed` | Spotted Target Destroyed | `Id.Item` → "Spotted Item Destroyed" (`Audio.Event.UX.Spotted.DestroyAssist.Deployable`); `Id.Buildable` → "Spotted Buildable Destroyed" (`...DestroyAssist.Buildable`); `Vehicle.Variant` → "Spotted Vehicle Destroyed" (`...DestroyAssist.Vehicle`) |

The default audio for the Removed row is `Audio.Event.UX.Spotted.DestroyAssist.Player`.

### 8b. Match-score feed ([`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json), 3 rows)

| Match-score tag | Text | Audio |
|---|---|---|
| `Meta.Progression.Resources.MatchScore.SpottingOwner` | Target Spotted | none |
| `Meta.Progression.Resources.MatchScore.SpottingAssist` | Target Spotted Assist | none |
| `Meta.Progression.Resources.MatchScore.SpottingDestroyed` | Spotted Target Destroyed | `Audio.Event.UX.Spotted.DestroyAssist` |

### 8c. Overlay ([`DA_SpottingOverlay`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/DA_SpottingOverlay.json))

| Setting | Value |
|---|---|
| Time until fade after action | 1.0 s |
| Distance text format | `{Distance} M` |
| Distance when empty | `___._` |

---

## 9. Trackers

Spotting has three tracker assets. The map and spatial trackers share the tag `Trackers.Type.SpottingTarget`.

### 9a. Map tracker ([`DT_TrackerData_Map_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Map/Data/DT_TrackerData_Map_Spotting.json) → [`DA_Tracker_Map_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Map/Data/DA_Tracker_Map_Spotting.json))

| Setting | Value |
|---|---|
| Widget | `W_Tracker_Map_SpottingTarget` |
| View model | `WDUISpottingTargetMapTrackerViewModel` |
| Required tags | `Meta.Alignment.Faction`, `Trackers.Type.SpottingTarget` |
| Recreate on faction change | Yes |

### 9b. Spatial tracker ([`DT_TrackerData_Spatial_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/DT_TrackerData_Spatial_Spotting.json) → [`DA_Tracker_Spatial_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/DA_Tracker_Spatial_Spotting.json))

| Element | Setting |
|---|---|
| Widget | `W_Tracker_Spatial_SpottingTarget` |
| View model | `WDUISpottingTargetSpatialTrackerViewModel` |
| Marker material | `M_UI_SpottingMarker` (default), `M_UI_SpottingTracker` (override) |
| Default marker texture | `T_UI_Map_Spotted`, scale 0.8, fade-out 3.0 s, starting opacity 0.75 |
| Reward tag on the default texture | `Challenges.Rewards.PlayerKill` |
| Distance text | Forced to metres |
| Line-of-sight rules | 3 rules, trace channel `ECC_GameTraceChannel4`. One rule has squared range 100,000,000 (about 10,000 units). Rendered-component check on. |
| Location offset | Base offset Z = 300. Second rule uses dynamic offset curve [`C_DynamicLocationOffsetSpottingTracker`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/C_DynamicLocationOffsetSpottingTracker.json) (range about 252) and attaches to the `Head` bone. |
| Screen clamping | 250 × 250 px |
| World distance scale | 2 rules |

The spatial tracker has per-vehicle texture overrides, so the marker changes by target. The Littlebird override uses `T_UI_Map_Spotted_Heli` with rotation 90°, and each vehicle override carries its own `RewardTag` (for example `Challenges.Rewards.VehicleDestroyed.LittleBird`, `...Huey`, `...Havoc`, `...Blackhawk`).

### 9c. Material tracker ([`DT_MaterialTrackerSettingsData_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Optimization/Data/DT_MaterialTrackerSettingsData_Spotting.json) → [`DA_MaterialTrackerData_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Optimization/Data/DA_MaterialTrackerData_Spotting.json))

This tracker is for **stationary and artillery gunner positions**. It is shown only when the local player is a gunner.

| Setting | Value |
|---|---|
| Tracker type | `WDUIMaterialTracker_Spotting` |
| Requires state | `State.Player.Vehicle.Role.Gunner` |
| Allowed vehicles | `Vehicle.Variant.Land.Tracked.TNK_01.Artillery`, `Vehicle.Variant.Stationary.Mortar`, `Vehicle.Variant.Stationary.STN_05` |
| Override for current vehicle | Yes |
| Show cash text | No |
| Force metres | Yes |

It also keys a reward tag by target class (player → `Challenges.Rewards.PlayerKill`, rotary → per-variant `VehicleDestroyed` tags, tracked vehicle → `VehicleDestroyed.TNK_01.Heavy`, and so on).

---

## 10. Input

| Context | Binding | Action | Notes |
|---|---|---|---|
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Left mouse button | [`IA_Player_PrimaryUse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_PrimaryUse.json) | |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Gamepad right trigger (axis) | [`IA_Player_PrimaryUse`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_PrimaryUse.json) | Has a `WDDeadZoneInputModifier` |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Mouse wheel up / down | [`IA_Player_IncreaseScopeZoom`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_IncreaseScopeZoom.json) / `DecreaseScopeZoom` | |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Left Shift | [`IA_Player_Focus`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_Focus.json) | Gamepad left stick click also maps to Focus |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Gamepad left / right shoulder | [`IA_Player_Lean_Left`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_Lean_Left.json) / `Lean_Right` | |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | (unbound) | [`IA_Player_ToggleScopeZoom`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IA_Player_ToggleScopeZoom.json) | Inherits settings from the action |
| [`IMC_SpottingAds`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_SpottingAds.json) | Gamepad D-pad right / left | `IncreaseScopeZoom` / `DecreaseScopeZoom` | `InputTriggerPulse` with interval 0.2 s |
| [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json) | (2 mappable key settings, 2 dead-zone modifiers) | | Not individually decoded |

The dead-zone modifiers mean stick and trigger input is filtered in both contexts.

---

## 11. Audio

| Event asset | Behaviours | Use (inferred) |
|---|---|---|
| [`AE_Comms_Spotted`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted.json) | Request spotted vox, play perspective sound, crosstalk | Radio call when a target is spotted |
| [`AE_Comms_Spotted_VehicleEmpty`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_Comms_Spotted_VehicleEmpty.json) | Same types as above | Variant for an empty spotted vehicle |
| [`AE_UX_Spotted_Target`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotted_Target.json) | Play spotted-target sound, crosstalk | UX cue on spot |
| [`AE_UX_Spotting_Start`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Start.json) | Set spotting parameters, execute trigger, play sound, crosstalk | Spotting mode opens |
| [`AE_UX_Spotting_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Stop.json) | Execute trigger, crosstalk | Spotting mode closes |
| [`AE_UX_Spotting_Complete`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Audio/Events/AE_UX_Spotting_Complete.json) | Execute trigger, crosstalk | Spot completed |

---

## 12. Limitations

- **Base values for each target** are not in this folder. The `BaseReward` options name `DefaultReward`, `RefreshedReward` and `KilledByEnemyReward`, and their numbers are in the shared challenge tables covered by the v2 doc (section 15). Only the min and max match-score values (section 4a) are in this folder.
- **The `Player` target** has a calculator row but no lookup row. The path that pays a spotted player was not traced.
- **Meaning of `DestroyedByTeamModifier`** is taken from its option name `KilledByEnemyFactor`. Its direction (boost or penalty) was not checked.
- **Zone and faction factor values** are not in this folder.
- **The [`Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Spotting.json) root bundle's widget element** and the gameplay cue path were not decoded in this pass.
- **The [`IMC_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Input/IMC_Spotting.json) input context** was listed but not decoded to individual bindings.
- **The spatial tracker's second line-of-sight and world-scale rules** were counted but not individually checked for values.
- **The Recon skill magnitudes** come from [`CT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/CT_ReconSkills.json), which is outside this folder.
- **[`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json)** is zero-valued (placeholder). Do not use it for live numbers.
