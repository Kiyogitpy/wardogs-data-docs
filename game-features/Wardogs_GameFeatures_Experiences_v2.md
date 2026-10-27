---
title: "Experiences (feature)"
redirect_from: ["/Wardogs_GameFeatures_Experiences_v2.html", "/Wardogs_GameFeatures_Experiences_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, KOTH, SniperShowdown, How Values Combine"
---

# Wardogs — GameFeatures: Experiences
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/Experiences/` — 11 JSON files. Two experiences: `KOTH` (1 file) and `SniperShowdown` (10 files).*

---

## 1. What This Folder Holds

Experiences are complete game modes. Each one is a GameFeature pack that sets match states, components, HUD widgets and data registries. Two are in this folder: **KOTH** (King of the Hill), and **SniperShowdown**, a sniper showdown mode with a stillness-detection mechanic.

| Experience | Files | Mode |
|---|---|---|
| KOTH | 1 | King of the Hill (control zone) |
| SniperShowdown | 10 | Sniper showdown |

---

## 2. KOTH (`KOTH/Content/KOTH.json`)

### 2a. Match states

| Order | Match state |
|---|---|
| 1 | `WDMatchState_PreMatch_WaitingForWorldLoad` |
| 2 | `WDMatchState_PreMatch_WaitingForPlayerCount` |
| 3 | `ControlZoneRuntime.WDMatchState_Playing_KOTH` |
| 4 | `WDMatchState_PostMatch` |

### 2b. Components

| Host | Component |
|---|---|
| `WDGameStateSession` | `B_FactionSetup_CreateThreeTeams` (three factions) |
| `WDGameModeSession` | `WDKOTHPlayerSpawnManagerComponent` |
| `WDGameStateSession` | `WDItemRequirementsEvaluatorComponent` |

### 2c. Other

- World Partition: `EDL_KOTH` (external data layer).

---

## 3. SniperShowdown

### 3a. Match states

| Order | Match state |
|---|---|
| 1 | `WDMatchState_PreMatch_WaitingForWorldLoad` |
| 2 | `WDMatchState_PreMatch_WaitingForPlayerCount` |
| 3 | `SniperShowdownRuntime.WDMatchState_Playing_SniperShowdown` |
| 4 | `WDMatchState_PostMatch` |

### 3b. Components

| Host | Component | Role (inferred from name) |
|---|---|---|
| `WDGameStateSession` | `B_SniperShowdown_FactionAssignmentComponent` | Assigns factions |
| `WDGameStateSession` | `WDSniperShowdownLastKillTrackerComponent` | Tracks last kill |
| `WDGameStateSession` | `B_SniperShowdown_MusicController` | Music |
| `WDGameModeSession` | `B_SniperShowdown_PlayerSpawnManagerComponent` | Spawns players |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_ExplodeComponent` | Explodes the player's body 1.5 s after death (section 3c) |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_LoadoutComponent` | Loadout |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_OOBComponent` | Puts a player outside both zones into the hostile-zone state (section 3c) |
| `WDMoverPlayerCharacter` | `B_SniperShowdown_StillnessSpottingComponent` | Stillness-based spotting |
| `WDControlZone` | `WDSniperShowdownControlZoneSeekerComponent` | Control zone seeking |

### 3c. Player and widgets

| Item | Value |
|---|---|
| Pawn data | `SniperShowdown_PlayerData` (`WDPawnData`): `B_SniperShowdown_MoverPlayerCharacter` |
| Scene registry | `UISceneData_Match` → `DT_SceneData_Match_SniperShowdown` |
| Event feed | `UIEventFeedData` → `DT_EventFeedTypes_SniperShowdown` |
| Tracker registries | `TrackerData_Minimap` and `TrackerData_TacticalMap` → `DT_TrackerData_Map_SniperShowdown` |
| HUD: leaderboard | `UI.HUD.Element.GameModeLeaderboard` → `W_SniperShowdown_Leaderboard` |
| HUD: timer | `UI.HUD.Element.Timer` → `W_SniperShowdown_Timer` |
| HUD: status | `UI.HUD.Element.GameModeStatus` → `W_SniperShowdown_Empty` |
| Persistent: fade out | `W_SniperShowdown_FadeOut`, layer Upper |
| Persistent: revealed | `W_SniperShowdown_Revealed`, layer Lower |

### 3d. Event feed (`DT_EventFeedTypes_SniperShowdown`)

| Row | Self text | Meaning |
|---|---|---|
| `UI.HUD.Element.EventFeed.Type.SniperShowdown.StandingStill` | "Keep moving or you will be revealed." | Warning: standing still is detected |
| `…Spotted` | "You have been revealed. Run." | You have been spotted |
| `…MovingClear` | "You are now hidden." | Cleared by moving |

These three rows confirm the stillness mechanic: standing still reveals you; moving clears it.

### 3e. Scene and UI assets

| Asset | Type | Content |
|---|---|---|
| `DA_SniperShowdown_FadeOut` | `WDSniperShowdownFadeOutData` | Death text "Killed by {KillerName}"; blackout transition out 3.0 s; respawn text "Respawning in {Time}..." |
| `DA_SniperShowdown_GameOverScene` | `WDSniperShowdownGameOverSceneData` | "Next Round in {Minutes}:{Seconds}"; scoreboard view model `WDUIScoreboardViewModel` |
| `DA_SniperShowdown_Leaderboard` | `WDSniperShowdownLeaderboardData` | Present, empty in export |
| `DA_SniperShowdown_Timer` | `WDSniperShowdownTimerData` | Format "{Minutes}:{Seconds}" |
| `DA_Tracker_Map_SniperShowdownZone` | `WDUIMapTrackerData` | Text off, no map zoom scaling |
| `DT_TrackerData_Map_SniperShowdown` | DataTable | 3 rows: `Trackers.Type.SniperShowdownZoneActive`, `…ZonePassive`, `…ControlZone` |
| `DT_SceneData_Match_SniperShowdown` | DataTable | 1 row: `UI.Scene.Match.EndgameMovie` |

---

## 4. How Values Combine

- Each experience is a self-contained mode. KOTH uses the control-zone runtime. SniperShowdown uses its own runtime and also a control zone with a seeker component.
- The stillness mechanic (SniperShowdown) is the only experience-level rule set in this folder. The event-feed rows make its three states explicit.

---

### 3c. Explode and out-of-bounds components (decoded, round 86)

Both are Blueprint `ActorComponent` classes added to the player character. Their bytecode was exported with WdExtract and read with `kismet_listing.py` ([round 86 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round86-bp.md)).

**`B_SniperShowdown_OOBComponent`** (**Bytecode**). It owns no timer and no damage. On begin play it binds to the character's gameplay-tag change event (`OnTagsChangedDynamic`) and unbinds on end play. On every tag change:

| If the character | Then |
|---|---|
| has `State.Location.Objective.ControlZone` or `State.Location.Objective.Hotzone`, and has `State.Location.SafeZone.Hostile` | removes one count of `State.Location.SafeZone.Hostile` (`UpdateGameplayTag`, -1) |
| has neither zone tag, and does not have `State.Location.SafeZone.Hostile` | adds one count of `State.Location.SafeZone.Hostile` (+1) |
| any other combination | nothing |

So leaving both zones gives the character the hostile-zone tag, and re-entering either zone removes it. The 20 s return countdown and the death that follow are not in this component. They are in native code (static reading, round 88): the per-character out-of-bounds update at `0x6E78410` treats the character as out of bounds when it is outside the world's playable rectangle or carries `State.Location.SafeZone.Hostile`, adds `State.Location.OutOfBounds` while that holds, counts `CurrentOutOfBoundsTime` up by the frame time and, when the server-side copy of the character reaches `OutOfBoundsTimeLimit` (20 s on the player pawn), calls the death routine `0x6E71400`, which sets `State.Player.Vitality.Dead`. Outside the zone the time counts back down at the same speed. The whole update is skipped unless the world has the out-of-bounds switch (`bUseOutOfBounds`) on, so the tag only starts the countdown in a world that has it. There is no GameplayEffect and no data asset for this timer; the only data is the limit field on the pawn (see [boundaries and safe zones](../_wiki/game-modes-and-maps/boundaries-and-safe-zones.md)). The same tag also blocks building and mine placement, because the safe-zone placement conditions test for it (see [Buildables](Wardogs_Buildables_v1.md)). The component's class defaults also list `ItemsToStartWith` = `Id.Item.SmallBackpack`, `Id.Item.Glock17` (**Data**).

**`B_SniperShowdown_ExplodeComponent`** (**Bytecode** and **Data**). It binds to the character's vitality `OnKilled` event. When the character dies, after `KismetSystemLibrary::Delay` of 1.5 s (ubergraph offset 15) it calls `GetDamageData` and `WDDamageSubsystem::SimulateRadialDamage` at the body's location (instigator controller read from the dead pawn; the dead pawn is in the ignore list), then the multicast `PlayExplosiveVFX`, which runs the gameplay cue `GameplayCue.Claymore.Explode` on the character. The damage values are class defaults:

| Field | Value |
|---|---:|
| `BaseDamage` | 250 |
| `ExplosiveRadius` | 500 |
| `EffectiveExplosiveRadius` | 250 |
| `MinimumExplosiveDamage` | 30 |
| `ExplosiveDamageFallOff` | 0.5 |
| `ExplosiveBluntDamage` | 100 |
| `bCheckLOS`, `bPreferUpwardsTrace` | true, true |
| Impulse | off (`bApplyImpulse` false) |
| Damage tag (`DamageEntityData`) | `Meta.Damage.Explosive.Utility.Claymore` |

The damage type tag handed to the subsystem is `Meta.Damage.DamageType.Explosive`. The blast is a Claymore-tagged explosion, so Claymore damage-table rules apply to it. The component replicates (`bReplicates` true).

## 5. Still not pulled / limitations

- **Stillness thresholds.** The time or distance that defines "standing still" is in the `StillnessSpottingComponent`, which is in BP code and not in this folder.
- **Out-of-bounds countdown and death.** Found in native code in round 88 (section 3c: `0x6E78410`, death at `0x6E71400`, server side). The world setting is on: Sniper Showdown is a data layer inside the Kavkazi (Bakurani) world, not a world of its own, and that world's `WDWorldSettings` has `bUseOutOfBounds` true ([round 68 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round68-boundaries.md)). The world settings carry no time override; the only limit is the pawn's `OutOfBoundsTimeLimit` of 20 s.
- **Music and timers.** Timer durations and music cues are not extracted.
- **Leaderboard data.** Empty in the export.
- **Unnamed keys.** Localised strings use `_aaa…` keys; their values are shown where the source string is present.

---

## 6. Item grants at spawn, by mode

Static census in [Round-12 spawn provisioning](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round12-spawn-provisioning.md). No data asset lists a universal starting kit.

| Source | Where | Items | Label |
|---|---|---|---|
| Player inventory component defaults | Native constructor, 13 container setups | None (empty `DefaultContainerItems`) | Native |
| SniperShowdown `B_SniperShowdown_LoadoutComponent` | Added to `WDMoverPlayerCharacter`, server only; BeginPlay | `Id.Item.SmallBackpack`, `Id.Item.Glock17` (context Looted, amount 1) | Data |
| Deathmatch weapon selection and ammo components | Added to `WDMoverPlayerCharacter` | Chosen weapon plus magazines, selection-driven | Native + Data |
| KOTH, ShootingRange, Tutorial spawn managers | `WDGameModeSession` | No path into the item-add chain found | Native (bounded) |
| Normal gear (vendor purchase) | `Server_ApplyLoadout` continuation `0x6BD5860` | Purchased request rows | Native |
| Stash records | `WDStorageVaultComponent` import `0x6CFE100` | `ITEMS` and `VEHICLES` records | Native |
| Rejoin | `Server_RestoreInventory` | Rebuilt from the duplicated session | Native |

Order of these routes on a first spawn is not traced.
