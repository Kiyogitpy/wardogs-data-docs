---
title: "Audio"
redirect_from: ["/Wardogs_Audio_v2.html", "/Wardogs_Audio_v2"]
parent: "World, Visuals & Audio"
description: "Inventory, Event structure, Notable events, Player Damage, Movement and Item Audio"
---

# Wardogs — Audio Data Reference
*Extracted from cooked game data under `/Game/Audio/` (UE 5.7 export, 1002 JSON files in [`Wardogs/Content/Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio)). Every number below was counted by script over the whole folder. Behaviour meanings are inferred from property names unless marked as confirmed.*

> **Format note:** the files are not one-object-per-file. Each `.json` holds one primary export (the asset named after the file) followed by its sub-objects (`UObject` exports for behaviours, template-linked blueprint instances). Every export starts with its own `--- export: <Kind> / <Name> ---` line, so the parser splits on those lines and then `json.loads` each block. 956 primary exports + 1,626 sub-objects = 2,582 export blocks, 0 parse errors.

---

## Season 02 update (2026-10-15)

- **46 files added.** 42 are events, so the event count goes 633 → 675: 10 helmet-state events in a new [`Events/Gear/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Gear) folder, 9 vendor UI events, 8 vendor wager and greeting/result events, 5 soccer-ball events, 3 seeding reward reasons, 2 windscreen-wiper events, 2 looting movement events, 2 weapon foley events and 1 rocket travel event.
- **Four non-event assets added:** [`DT_RainSpots`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Environment/DT_RainSpots.json) (DataTable, `Environment/`), [`DA_Player_Looting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Movement/Looting/DA_Player_Looting.json), [`DA_Weapon_Projectile_125mm_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Projectile/125mm/DA_Weapon_Projectile_125mm_Audio.json) and [`DA_BulletCasings_Large`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Shared/BulletCasings/AudioDataAssets/DA_BulletCasings_Large.json) (all WDAudioData). The audio file total goes 956 → 1002.
- **Behaviour references** 1,626 → 1,704. Restart behaviour `Always` 137 → 154 and `PlayBoth` 63 → 65.
- **`Audio.Music.SpawnBoardWait`** priority 6 → 62.
- **Impulse resonance:** `DefaultResonanceRange` 7500 → 3500 on [`AE_Vehicle_Shared_Destroy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/AE_Vehicle_Shared_Destroy.json) and [`AE_Vehicle_ROT_Destroy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/ROT/AE_Vehicle_ROT_Destroy.json). Most `IdImpulseProperties` ranges of [`AE_Weapon_Projectile_Impact_Explosive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Weapon/Projectile/AE_Weapon_Projectile_Impact_Explosive.json) drop from 5000 or 7500 to 3500, and a `Item.Caliber.125x570mm` entry (3500) is added. [`AE_Vehicle_ROT_Destroyed_Crash`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/ROT/AE_Vehicle_ROT_Destroyed_Crash.json) gains an impulse behaviour with range 2500.
- **[`AE_Player_Death`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Player/Death/AE_Player_Death.json):** the death sound changes from `MSS_Player_Death_FromMelee_3p` to `MSS_Player_Death_FromBullet_1p`, and `Is Local Character` is set to true.
- **[`AE_UX_Cash_Bribe`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UX/Cash/AE_UX_Cash_Bribe.json):** restart behaviour `Always` → `PlayBoth`.
- **[`AE_UI_InGame_Vendor_Unlock`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/InGame/AE_UI_InGame_Vendor_Unlock.json):** vendor bark delay 2.0 → 1.5 s, context tag `Audio.Context.Default` → `Audio.Context.Dial.Equipment.Vendor`.
- **[`AE_Weapon_Fire_BulletCasing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Weapon/Firing/AE_Weapon_Fire_BulletCasing.json):** four size entries change from [`DA_BulletCasings_Medium`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Shared/BulletCasings/AudioDataAssets/DA_BulletCasings_Medium.json) to [`DA_BulletCasings_Large`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Shared/BulletCasings/AudioDataAssets/DA_BulletCasings_Large.json).
- **[`AE_Weapon_Projectile_Impact`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Weapon/Projectile/AE_Weapon_Projectile_Impact.json):** `DamageSize` 2 → 3, and the attenuation curve changes from [`CC_HDR_ATT_SharedImpacts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_ATT_SharedImpacts.json) to [`CC_HDR_ATT_SharedImpacts_30mm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_ATT_SharedImpacts_30mm.json).
- **Comms VOIP events** ([`AE_Comms_Played`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/AE_Comms_Played.json), [`AE_Comms_PlayerStartedSpeaking`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/VOIP/AE_Comms_PlayerStartedSpeaking.json), [`AE_Comms_PlayerStoppedSpeaking`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/VOIP/AE_Comms_PlayerStoppedSpeaking.json)) gain a `WDAudioEventBehaviorHelmetMuffle` behaviour.
- **Six impact DAs** (30mm, Large, Medium, Rocket_BluntImpact, Small) gain an `Audio.Asset.Surface.Vehicle` entry.

Full before/after list: [Season 2 Changes → World, Visuals & Audio]({{ '/season-2-changes/world-visuals-audio.html' | relative_url }}).

---

## 1. Inventory

### 1a. Primary asset types by folder

| Folder | Files | Primary Type (count) | What it holds |
|---|---|---|---|
| `Events/` | 675 | CrosstalkAudioEvent (675) | Named audio events, one per gameplay trigger. Each lists behaviours. |
| [`Vox/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox) | 151 | WDAudioData (148), WDVoxSettings (1), DataTable (1), WDVoxAudioProfile (1) | Voice barks, exertions, narrator, vox table, profile mapping |
| `Player/` | 62 | WDAudioData (62) | Footsteps, movement, parachute, ladder, stance, item sounds |
| `Vehicles/` | 16 | WDAudioData (11), PDA_CBM_Map_C (3), REVModelAsset (1), CurveFloat (1) | Vehicle surfaces, skids, CBM maps |
| `Weapon/` | 22 | WDAudioData (22) | Projectile impacts, bullet casings, attachments |
| [`Attenuations/HDR/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Attenuations/HDR) | 34 | CurveFloat (34) | HDR attenuation curves |
| [`Convo/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Convo) | 23 | WDConversationData (23) | Valkyra vehicle conversations |
| [`Destruction/DAs/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Destruction/DAs) | 6 | WDAudioData (6) | Building chunk tails and transients |
| `Curves/` | 7 | CurveFloat (7) | Gameplay curves (exertion decay, SMG external curve, UI ping, lock-on) |
| `Ambience/` | 2 | BHSignificanceSettingsAsset (1), BHSignificanceEvaluator_Sphere (1) | Significance settings for the Kavkazi river |
| `Environment/` | 2 | DataTable (2) | DT_ImpulseResonance, DT_RainSpots |
| `Music/` | 1 | DataTable (1) | DT_MusicSystem |
| `UI/` | 1 | WDMicLevelMeterData (1) | DA_MicLevelMeter (no exported properties) |
| **Total** | **1002** | | |

### 1b. Events folder breakdown (CrosstalkAudioEvent)

| Sub-folder | Events | Sub-folder | Events |
|---|---|---|---|
| [`Events/Player/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Player) | 126 | [`Events/Comms/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Comms) | 45 |
| [`Events/Vehicle/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Vehicle) | 125 | [`Events/UX/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/UX) | 34 |
| [`Events/Weapon/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Weapon) | 121 | [`Events/World/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/World) | 18 |
| [`Events/UI/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/UI) | 107 | [`Events/Gamemode/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Gamemode) | 15 |
| [`Events/Environment/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Environment) | 13 | [`Events/Doors/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Doors) | 10 |
| [`Events/Music/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Music) | 9 | [`Events/Prop/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Prop) | 14 |
| [`Events/Vendor/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Vendor) | 15 | [`Events/Destruction/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Destruction) | 5 |
| [`Events/Ambience/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Ambience) | 3 | `Events/` root (debug, stop, disconnect) | 5 |
| [`Events/Gear/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Events/Gear) | 10 | | |

Total: **675 events**. Each event has a `NameTag` (a gameplay tag, e.g. `Audio.Event.Weapon.ReloadEmpty.Stage3`). Tag prefixes by area: Vehicle 123, UI 111, Player 109, Weapon 105, Comms 41, UX 34, Item 33, World 18, Environment 15, Vendor 15, Prop 14, Gamemode 13, Projectile 12, Door 10, Music 9, Destruction 5, Ambience 3, Debug 2, OnDisconnect/StopSound/StopSoundFade 1 each.

---

## 2. Event structure (CrosstalkAudioEvent)

Every event has `NameTag` and `Behaviors` (an array of object references to sub-exports). Only one event carries `QueueLifetime` ([`AE_UI_FrontEnd_Enter_ConfirmationPopUp`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/FrontEnd/AE_UI_FrontEnd_Enter_ConfirmationPopUp.json) = 3.0 s).

Behaviour count per event (675 events, 1,704 behaviour references):

| Behaviours per event | Events | | Behaviours per event | Events |
|---|---|---|---|---|
| 0 | 7 | | 6 | 9 |
| 1 | 192 | | 7 | 3 |
| 2 | 226 | | 8 | 8 |
| 3 | 157 | | 9 | 10 |
| 4 | 36 | | 10 | 8 |
| 5 | 14 | | 11 / 12 / 15 / 16 | 2 / 1 / 0 / 2 |

Events with zero behaviours (silent or stub): [`AE_StartDistantWarfare`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Ambience/DistantWarfare/AE_StartDistantWarfare.json), [`AE_Music_InGame_Last10Points_FinalPoint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Music/InGame/AE_Music_InGame_Last10Points_FinalPoint.json), [`AE_Player_EnteredControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Player/AE_Player_EnteredControlZone.json), [`AE_Item_Dropped_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Player/Item/Drop/AE_Item_Dropped_Stop.json), [`AE_World_Blackmarket_Enter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/World/AE_World_Blackmarket_Enter.json), [`AE_World_GymTDM_Exit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/World/AE_World_GymTDM_Exit.json), [`AE_World_ShootingRange_Exit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/World/AE_World_ShootingRange_Exit.json).

### 2a. Payload routing (what an event actually plays)

Counted across all 675 events (an event can reference more than one kind):

| Payload route | Events | Notes |
|---|---|---|
| Direct `MetaSoundSource` (`MSS_*`) reference | 294 | Most common. 280 distinct MSS names referenced by events. |
| `WDAudioData` (`DA_*`) reference | 43 | Perspective and hostility variants (see 2c) |
| Direct `SoundWave` (`SFX_*`) reference | 2 | [`AE_Debug_23lufs`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/AE_Debug_23lufs.json) (`SFX_-23db`), [`AE_UI_FrontEnd_Enter_LogoScene`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/FrontEnd/AE_UI_FrontEnd_Enter_LogoScene.json) |
| Vox request (`AEB_RequestVox_C`, `AEB_RequestSquadVox_C`, `AEB_RequestDamagedVox_C`) | 46 | Resolves through [`DT_VoxData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/General/DT_VoxData.json) (section 6) |
| Only stop/end/parameter/CBM behaviours (no new sound) | 91 | e.g. `StopSound`, `EndBehavior`, `TriggerParam` |

### 2b. Behaviour classes (UObject sub-exports, all folders)

Count = number of sub-export instances in the dump. "Key properties" are the ones seen in the census.

| Behaviour class | Count | Key properties | Inferred role |
|---|---|---|---|
| `CrosstalkAudioEventBehaviorAttachSoundToActor` | 209 | `SocketName`, `AttachmentOffset` | Attaches the sound to a socket on the owning actor (offset in UE units) |
| `CrosstalkAudioEventBehaviorPlaySound` | 199 | `Sound`, `ContextTag`, `SoundRestartBehavior`, `FadeIn`, `bCancelFadeOut`, `CancelFadeOutDuration` | Plays a MetaSound or SoundWave |
| `AEB_AttachSoundToHeldItem_C` | 100 | `Socket Name`, `AttachmentRotationOffset`, `bStatic` | Attaches to held item (e.g. `handguard_Attach`, `S_Muzzle`) |
| `AEB_PlayHeldItemPerspectiveSound_C` | 87 | `FirstPersonSoundTag`, `ThirdPersonSoundTag`, `RestartBehaviour`, `ConcurrentInstanceLimit` | 1p/3p pair chosen by tag |
| `CrosstalkAudioEventBehaviorExecuteTriggerParameter` | 152 | `ParameterName` (`Trigger`, `Stop`, `HornOn`) | Fires a trigger or sets a named parameter on the running sound |
| `AEB_EndBehavior_C` | 62 | `BehaviorClass` | Ends a named behaviour (e.g. `AEB_Comms_StartPlayerVoice_C`) |
| `CrosstalkAudioEventBehaviorStopSound` | 59 | `FadeOut` | Stops the event's sound (optional fade, e.g. 0.3 s) |
| `AEB_DeactivateControlBusMix_C` | 62 | `Mix`, `Local Only`, `Delay` | Removes a control bus mix (`SoundControlBusMix`) |
| `AEB_ActivateControlBusMix_C` | 51 | `Mix`, `Local Only` | Activates a control bus mix |
| `WDAudioEventBehaviorPlayVehicleSound` | 41 | `SoundAssetTag`, `bPersistent`, `RestartBehavior` | Plays a vehicle sound by asset tag |
| `AEB_PlayPerspectiveSound_C` | 38 | `1pSound`, `3pSound`, `RestartBehaviour` | Explicit 1p and 3p MetaSound pair |
| `WDAudioEventBehaviourPlayPerspectiveSound_HostilityAware` | 38 | `FirstPersonSoundTag`, `AlliedThirdPersonSoundTag`, `HostileThirdPersonSoundTag`, `SoundAssetData`, `bStatic` | 1p / ally / enemy variant set from a `WDAudioData` |
| `AEB_VehiclePerspective_C` | 34 | `ContextTag` (horn) | Vehicle horn perspective; `ConcurrentInstanceLimit` = 0 here (meaning unclear) |
| `WDAudioEventBehaviorDisableMusicState` | 32 | `StateToDisable` | Disables a music state (e.g. `Audio.Music.SpawnBoardWait`) |
| `AEB_RequestVox_C` | 29 | `VoxRequest.LineID` | Requests a vox line by tag ([`DT_VoxData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/General/DT_VoxData.json)) |
| `AEB_SetBooleanParameter_C` | 27 | `In Name` (`VehicleReady`, `HornOn`, `Destroyed`), `In Bool`, `Delay` | Sets a bool on the sound |
| `AEB_StopSound_SpeedOfSoundDelay_C` | 17 | `Fade Out Duration` | Delayed stop for distant sources (by speed of sound) |
| `AEB_SetImpulseResonanceParameters_C` | 13 | (impulse params) | Feeds impulse resonance (section 8) |
| `AEB_PlayVehicleWeaponPerspectiveSound_C` | 15 | `FirstPersonSoundTag`, `ThirdPersonSoundTag`, `bUseManagedFireLoop` | Vehicle weapon 1p/3p |
| `AEB_RequestSquadVox_C` | 10 | `Line ID` | Squad order bark |
| `AEB_AttachSoundToVehicle_C` | 10 | `Socket Name` (`body_RadarSocket`, `gasPedal_J`), `Location Offset` | Vehicle socket attach |
| `AEB_SetHostilityParameter_C` | 10 | | Sets hostility (ally/enemy) parameter |
| `AEB_SetAudioParameters_C` | 10 | `Parameters` (list of `ParamName`, `FloatParam`, `BoolParam`, ...) | Writes several MetaSound inputs (e.g. `Gain` 0.6) |
| `AEB_SetBlendedFootstepSurfaceTrigger_C` | 9 | `AudioData`, `SurfacePropertiesMap` | Surface-driven footstep data (keyed by `EWDAudioSurface`) |
| `AEB_SetSoundWaveArrayParameterByHeldItem_C` | 9 | `HeldItemSoundSet`, `SoundParameterName` (`ItemFoley.Waves`) | Sprint/item foley wave arrays |
| `WDAudioEventBehaviorEnableMusicState` | 9 | `StateToEnable` | Enables a music state |
| `AEB_Doppler_C` | 9 | | Doppler on moving source |
| `AEB_SetVehicleHIDZAttribute_C` | 8 | `Attribute Tag` (e.g. `Attribute.Gameplay.Health.Engine`), `ParameterName` (`EngineHealth`), `ShouldNormaliseAttribute` | Drives HIDZ damage parameters from gameplay attributes |
| `WDAudioEventBehaviorApplyImpulseResonance` | 8 | `IdImpulseProperties`, `DefaultResonanceRange`, `CollisionChannel` | Impulse resonance on projectile hit (section 8) |
| `AEB_StoreFootstepData_C` | 7 | | Caches footstep data |
| `AEB_HandleProjectileSimulation_C` | 9 | | Projectile flight sound |
| `AEB_HandleRocketWhizby_C` | 8 | | Rocket flyby |
| `AEB_AttachSoundToDoorHandle_C` / `AEB_SelectDoorSound_C` | 6 / 6 | | Door sound routing |

Many other behaviour classes appear once to six times (e.g. `AEB_PlayVehicleCollisionSound_C`, `AEB_PlayItemPickup_C`, `AEB_Vaulting_C`, `AEB_XPProgression_PlayRoleLevelUp_C`). The full class list was produced by the census script; none were left uncounted.

### 2c. Perspective and hostility variants

Tags on sound assets carry a suffix that picks the variant. Distinct tag names in the dump (1,408 total) ending in:

| Suffix | Distinct tags | Meaning (inferred from usage) |
|---|---|---|
| `.1p` | 57 | First-person sound (player's own view) |
| `.3p` | 41 | Third-person sound (heard by others) |
| `.Ally` | 16 | Friendly-observer variant (from `HostilityAware` behaviours) |
| `.Enemy` | 18 | Hostile-observer variant |

Example. `WDAudioEventBehaviourPlayPerspectiveSound_HostilityAware` on the ragdoll, ladder and stance events points at WDAudioData such as [`DA_Stance_CrouchToStand_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Movement/Stance/DA/DA_Stance_CrouchToStand_Audio.json), with tags `Audio.Asset.Player.Stance.1p`, `.Ally` and `.Enemy`.

### 2d. Context tags and restart behaviour

- **200 distinct `ContextTag` values.** Most used: `Audio.Context.Default` (690 uses), `Audio.Context.Weapon.Fire` (85), `Audio.Context.Vehicle.Engine` (39), `Audio.Context.Projectile.Rocket` (22), `Audio.Context.Door` (20), `Audio.Context.Player.Footstep.Transition` (20), `Audio.Context.Player.Footstep` (19), `Audio.Context.Vehicle.Engine.RearRotor` (15).
- **Restart behaviour** (`ESoundRestartBehavior`; the property is spelled `SoundRestartBehavior`, `RestartBehaviour` or `RestartBehavior` depending on class): `Always` 154, `PlayBoth` 65, `PlayBothIfDifferentSound` 61, `IfDifferentSound` 41.

### 2e. Hashed unnamed property

Events and some behaviours carry a property whose name is an unresolved FName hash (`_aaabhgndclheajnnlnade`; `_aaabhonahgpdbjealfaaa_$ED076F31940B5000$_$23$` in exports before 2026-10-18). It is always a float (226 instances: 185 on events, 41 on behaviours). Values cluster by family:

| Family (events) | Value |
|---|---|
| Reload stages (`ReloadEmpty`, `ReloadTactical`, Drop and Drum variants) | 50.5 |
| Bipod fold/unfold | 50.5 |
| Vehicle reload | 65.0 (55.0 once) |
| HIDZ wheel pop / destroy | 150.0 |
| Comms social ([`AE_Comms_Social_Nice`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/Social/AE_Comms_Social_Nice.json), `_No`, `_Sorry`) | 80.0 |
| Most common overall | 50.5 (72 events) |

Its meaning is **not confirmed**. It looks like a per-event range or distance value, but the dump does not name it.

---

## 3. Notable events (real examples)

| Event asset | NameTag | Behaviours and payload |
|---|---|---|
| [`AE_Debug_23lufs`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/AE_Debug_23lufs.json) | `Audio.Event.Debug.23lufs` | PlaySound `SFX_-23db` (loudness calibration reference) |
| [`AE_Debug_AnimSync`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/AE_Debug_AnimSync.json) | `Audio.Event.Debug.AnimSync` | PlaySound `MSS_Debug_AnimSync` |
| [`AE_OnDisconnect_Reset`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/AE_OnDisconnect_Reset.json) | `Audio.Event.OnDisconnect.Reset` | DeactivateAllControlBusMix, Submix_DeactivateEffect on `SBMIX_CriticalGroup_Heavy`, `_Medium`, `_Light` |
| [`AE_StopEvent`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/AE_StopEvent.json) | `Audio.Event.StopSound` | StopSound, no fade |
| [`AE_StopEventFadeTrigger`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/AE_StopEventFadeTrigger.json) | `Audio.Event.StopSoundFade` | StopSound, FadeOut 0.3 |
| [`AE_Comms_Social_Nice`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/Social/AE_Comms_Social_Nice.json) | `Audio.Event.Comms.Social.Nice` | AttachToActor + RequestVox `Audio.Vox.Bark.Social.Nice`; hashed float 80.0 |
| [`AE_Comms_Request_Ammo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/AssistanceRequests/AE_Comms_Request_Ammo.json) | `Audio.Event.Comms.Request.Ammo` | RequestVox `Audio.Vox.Bark.Request.Ammo` + AttachToActor |
| [`AE_Comms_Order_Attack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/Orders/AE_Comms_Order_Attack.json) | `Audio.Event.Comms.Order.Attack` | RequestSquadVox `Audio.Vox.Bark.Order.Attack` |
| [`AE_Comms_Squad_Affirmative`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/Squad/AE_Comms_Squad_Affirmative.json) | `Audio.Event.Comms.Squad.Affirmative` | RequestSquadVox `Audio.Vox.Bark.Squad.Affirmative` |
| [`AE_Comms_LoggingIn_Connected`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Comms/VOIP/AE_Comms_LoggingIn_Connected.json) | `Audio.Event.Comms.LoggingIn.Connected` | PlaySound `MSS_Comms_LoggingIn_Connected_Preset` |
| [`AE_Player_Damaged_Melee`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Player/Damaged/AE_Player_Damaged_Melee.json) | `Audio.Event.Player.Damaged.Melee` | Perspective sound `MSS_Player_Damage_FromMelee_1p/_3p` + RequestDamagedVox (`TakingDamage.Light`/`Heavy`) |
| [`AE_Footstep_Stealth`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Player/Movement/Footstep/AE_Footstep_Stealth.json) | `Audio.Event.Player.Footstep.CrouchWalk` | AttachToHeldItem `handguard_Attach`, PlayItemMovementSound `MSS_Player_Movement_Footstep_Item_1p`, SetAudioParameters, SetBlendedFootstepSurfaceTrigger [`DA_Surface_Footstep_Stealth_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Movement/Footsteps/DA/DA_Surface_Footstep_Stealth_Audio.json) |
| [`AE_Weapon_Fire_Start_Auto_Suppressed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Weapon/Firing/AE_Weapon_Fire_Start_Auto_Suppressed.json) | `Audio.Event.Weapon.Fire.Start.Auto.Suppressed` | Held-item attach `S_Muzzle`, EnemyAccuracyScaling, SetHeldWeaponStartFireParameters, WeaponFire_PlaySound (looping fire tags) |
| [`AE_Vehicle_Weapon_Fire_Start_Semi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/Weapon/Fire/AE_Vehicle_Weapon_Fire_Start_Semi.json) | `Audio.Event.Vehicle.Shared.Weapon.Fire.Start.Semi` | PlayVehicleWeaponPerspectiveSound `Audio.Asset.Vehicle.Weapon.Fire.1p/3p` |
| [`AE_Vehicle_HIDZ_MainRotor_Damaged`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/Shared/HIDZ/AE_Vehicle_HIDZ_MainRotor_Damaged.json) | `Audio.Event.Vehicle.HIDZ.MainRotor.Damaged` | Doppler, SetVehicleHIDZAttribute `Attribute.Gameplay.Health.Rotor.Main` into `HIDZHealth`, horn perspective, attach `Collective_J` |
| [`AE_Vehicle_SpawnVehicle_RadarFold`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/AE_Vehicle_SpawnVehicle_RadarFold.json) | `Audio.Event.Vehicle.SpawnVehicle.RadarFold` | PlayAllegianceSound (`MSS_Vehicle_Land_SpawnVehicle_Radar_Lonestar`, `_Valkyra`, ...) + attach |
| [`AE_Engine_Running_ROT`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/ROT/AE_Engine_Running_ROT.json) | `Audio.Event.Vehicle.Engine.Running.ROT` | Doppler, 3 SetBool `Engine On`, SetVehicleHIDZAttribute `Rotor.Main` |
| [`AE_Vehicle_Stabilizing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/Weapon/Stabilizers/AE_Vehicle_Stabilizing.json) | `Audio.Event.Vehicle.Stabilizing` | TriggerStabilizingState, horn perspective, attach, PlaySound `MSS_Vehicle_TNK_Stabilizing` |
| [`AE_Countermeasures_SmokeScreen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/AE_Countermeasures_SmokeScreen.json) | `Audio.Event.Vehicle.Countermeasures.SmokeScreen` | SetSmokeScreenActiveTime, attach x2, PlaySound `MSS_Vehicle_Countermeasures_SmokeScreen_Detonation` |
| [`AE_Music_Deployed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Music/AE_Music_Deployed.json) | `Audio.Event.Music.Deployed` | DeactivateCBM `AM_CBM_UIScene_PopUpWindow`, DeactivateCBM `AM_CBM_UIScene_DeploymentScreen`, Music_Deployed |
| [`AE_Music_InGame_EndGame`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Music/InGame/AE_Music_InGame_EndGame.json) | `Audio.Event.Music.InGame.EndGame` | ActivateCBM `AM_CBM_Main`, ActivateCBM `AM_CBM_EndGame`, DeactivateCBM `AM_CBM_Critical`, StopSoundOnPlayerCharacter, Submix effects |
| [`AE_Gamemode_SpawnBoardFinished`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Gamemode/SpawnBoard/AE_Gamemode_SpawnBoardFinished.json) | `Audio.Event.Gamemode.SpawnBoard.Finished` | DeactivateCBM `AM_CBM_SpawnBoardWait`, DisableMusic `Audio.Music.SpawnBoardWait` |
| [`AE_UI_FrontEnd_Enter_Collection`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/FrontEnd/AE_UI_FrontEnd_Enter_Collection.json) | `Audio.Event.UI.FrontEnd.Open.Collection` | ActivateCBM `AM_CBM_UIScene`, DeactivateCBM `AM_CBM_FrontEnd_MainMenu`, PlaySound `MSS_UI_FrontEnd_Enter_Collection` |
| [`AE_UI_InGame_Vendor_Purchase`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UI/InGame/AE_UI_InGame_Vendor_Purchase.json) | `Audio.Event.UI.InGame.Vendor.Purchase` | PlayContextualPurchaseSound, PlaySound `MSS_UI_InGame_Vendor_PurchaseCart` |
| [`AE_UX_Combat_Kill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UX/Combat/AE_UX_Combat_Kill.json) | `Audio.Event.UX.Combat.Kill` | EnemyKilledParameters, PlaySound `MSS_UX_Combat_Notify_KillConfirmed` |
| [`AE_UX_Spotted_SpottedConfirmation`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/UX/Spotted/AE_UX_Spotted_SpottedConfirmation.json) | `Audio.Event.UX.Spotted.SpottedConfirmation` | PlaySound `MSS_UX_Spotting_SpottedConfirmation` |
| [`AE_Vehicle_Reversing_Start`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Vehicle/Shared/AE_Vehicle_Reversing_Start.json) | `Audio.Event.Vehicle.Shared.Reversing.Start` | Horn perspective, attach `gasPedal_J`, TriggerParam `Start`, PlayVehicleSound `Audio.Asset.Vehicle.Reversing` |

Event tags do not always match the asset name. About 40 events differ. Examples: [`AE_Door_Warehouse_Play`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Doors/AE_Door_Warehouse_Play.json) has tag `Audio.Event.Door.Warehouse`; [`AE_Gamemode_SpawnBoard_Loop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Gamemode/SpawnBoard/AE_Gamemode_SpawnBoard_Loop.json) has tag `Audio.Event.Gamemode.SpawnBoard`; [`AE_Footstep_Stealth`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Player/Movement/Footstep/AE_Footstep_Stealth.json) has tag `Audio.Event.Player.Footstep.CrouchWalk`. Runtime code presumably looks events up by tag, not by asset name, but that is inferred.

---

## 4. Player Damage, Movement and Item Audio (WDAudioData)

WDAudioData holds a `SoundAssets` map (tag → MetaSoundSource or SoundWave) and, in 186 of 249 files, a `SoundAssetSets` map (set tag → list of member tags). Sets look like random-variant pools (e.g. `Audio.Asset.Surface.Concrete` → `…Concrete.Wave01` to `Wave05`). This is inferred from the naming, not from engine code.

| Folder | DAs | SoundAssets entries | SoundAssetSets entries | Notes |
|---|---|---|---|---|
| [`Vox/Barks/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks) | 118 | 235 | 235 | Two status tags only: `Audio.Asset.Vox.Normal`, `Audio.Asset.Vox.LowHealth` |
| `Player/Movement/` | 52 | 843 | 116 | 224 distinct tags: ladders (mount, down, slide, dismount), drag, footsteps, parachute, stance, swim, ragdoll |
| [`Vox/Exertions/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Exertions) | 26 | 30 | 30 | Breath, focus, critical state, melee, throwing, vaulting, take-damage |
| `Player/Item/` | 10 | 60 | 0 | Item data ([`ID_Armor_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Armor_Audio.json), [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json), [`ID_Helmet_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Helmet_Audio.json), [`ID_Magazine_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Magazine_Audio.json), [`ID_LooseAmmoBox_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_LooseAmmoBox_Audio.json)) |
| `Weapon/Projectile/` | 10 | 260 | 50 | Per-calibre impact DAs (40mm, 72mm, 84mm, 93mm, 120mm, 122mm, 125mm, 155mm, Drone, Mortar) |
| [`Vehicles/Land/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vehicles/Land) | 8 | 80 | 10 | PZH2000 surface, skid and braking DAs |
| [`Weapon/Shared/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Weapon/Shared) | 8 | 229 | 18 | Bullet casings ([`DA_BulletCasings_Medium`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Shared/BulletCasings/AudioDataAssets/DA_BulletCasings_Medium.json), `_Shotgun`), impacts ([`DA_Impact_30mm_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Shared/Impacts/DA_Impact_30mm_Audio.json), [`DA_Impact_Large_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Shared/Impacts/DA_Impact_Large_Audio.json), ...) |
| [`Destruction/DAs/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Destruction/DAs) | 6 | 199 | 36 | Building chunk tails and transients, small/medium/large |
| [`Vox/Narrator/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Narrator) | 4 | 4 | 4 | Destroy-spotting barks (Buildable, Deployable, Player, Vehicle) |
| [`Weapon/Attachments/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Weapon/Attachments) | 4 | 36 | 0 | Attachment drag/drop and bipod fold ([`ID_Attachment_Bipod_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Attachments/Bipod/ID_Attachment_Bipod_Audio.json), [`ID_Attachment_Suppressor_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Weapon/Attachments/ID_Attachment_Suppressor_Audio.json), ...) |
| `Vehicles/Shared/` | 3 | 15 | 0 | [`DA_Vehicle_Helicopter_Shared_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Shared/Helicopter/DA/DA_Vehicle_Helicopter_Shared_Audio.json), [`DA_GarageVendor_Refuel_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Shared/Refuel/DA_GarageVendor_Refuel_Audio.json), [`DA_GarageVendor_Repair_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Shared/Repair/DA_GarageVendor_Repair_Audio.json) |

Footstep example. [`DA_Footstep_CrouchWalk_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Movement/Footsteps/DA/DA_Footstep_CrouchWalk_Audio.json) maps `Audio.Asset.Player.Footstep.1p` → `MSS_Player_Movement_LayeredFootstep_Stealth_1p`, `…Ally` → `MSS_Player_Movement_LayeredFootstep_Stealth_Ally`, and `…Enemy` → `MSS_Player_Movement_LayeredFootstep_Stealth_Enemy`. This is the 1p/Ally/Enemy triple pattern from section 2c.

Surface data. [`DA_Surface_Footstep_Stealth_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Movement/Footsteps/DA/DA_Surface_Footstep_Stealth_Audio.json) (and its siblings) hold a `SurfacePropertiesMap` keyed by `EWDAudioSurface` values (e.g. `EWDAudioSurface::Flesh`), each mapping to a surface tag set (e.g. `Audio.Asset.Surface.Concrete`). Surface families seen in the sets: Concrete, Dirt, Glass, Metal, Water, Wood, Grass, Gravel, Asphalt, Default.

---

## 5. Conversations (WDConversationData)

23 assets, all `Valkyra` vehicle conversations.

| Group | Assets | Duration range (s) | Lines per asset |
|---|---|---|---|
| Backstory | 1 ([`DA_Convo_Valkyra_Vehicle_Back_C1`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Convo/Valkyra/Vehicle/Backstory/DA_Convo_Valkyra_Vehicle_Back_C1.json)) | 14.2 | 4 |
| Generic | 6 (`Gen_C1` to `Gen_C6`) | 6.6 to 15.5 | 3 to 5 |
| Short | 16 (`Short_C01` to `Short_C19`, some numbers skipped) | 3.2 to 7.1 | 2 |

Each asset has `ConversationTag` (e.g. `Audio.Conversation.Valkyra.Vehicle.Dialogue.Generic.Var04`), `ConversationTime`, and `ConversationLines` (ordered list of `LineAudio` SoundWaves). Line names carry a speaker suffix `_Djinn` or `_Kaiser` (e.g. `SFX_Convo_Valkyra_Vehicle_Back_C1_L1_Djinn`, `..._L2_Kaiser`).

---

## 6. Vox System

### 6a. DT_VoxData (81 rows, [`Vox/General/DT_VoxData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/General/DT_VoxData.json))

Row struct `WDVoxBase`. Key = `LineID` tag (e.g. `Audio.Vox.Exertion.Breath.Inhale`).

| VoxGroup | Rows | Tag families |
|---|---|---|
| `EWDVoxGroup::Bark` | 62 | Spotting 35, Request 13, Order 5, Social 5, Squad 5, TakingDamage 4 |
| `EWDVoxGroup::Exertion` | 15 | Vaulting 3, Breath 2, MeleeSwing 2, ThrowingGrenade 2, Focus 2, Jump 1, CriticalState 1, ProneMovement 1 |
| `EWDVoxGroup::Narrator` | 4 | Narrator destroy-spotting lines |

Timing and interrupt fields:

| Field | Distribution |
|---|---|
| `InterruptibleBehavior` | `InterruptedByBothSameAndHigherPriorities` 70, `InterruptedOnlyByHigherPriority` 8, `NotInterruptible` 3 |
| `Lifetime` | 5.0 s (79 rows), 0.5 s (1), 1.0 s (1) |
| `CooldownTime` | 0.01 s (77), 1.0 s (2), 0.35 s (1), 5.0 s (1) |
| `PreDelayTime` | 0.01 s (72), 0.5 s (6), 0.15 s (2), 0.25 s (1) |
| `PostDelayTime` | 0.01 s (all 81) |

Two hidden fields (unnamed hashes) exist on every row: one bool (true on 3 rows) and one enum (`EWDVoxGroup::Exertion` on 3 rows, otherwise `NONE`). Their meaning is unknown.

### 6b. DA_VoxSettings ([`Vox/General/DA_VoxSettings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/General/DA_VoxSettings.json), class WDVoxSettings)

| Setting | Value |
|---|---|
| `VoxDataRegistry` | `DR_VoxData` (points at DT_VoxData) |
| `InterruptFadeOutDuration` | 0.1 s |
| `VoxGroupPriorities` | Narrator 1, Bark 2, Exertion 3, Dialogue 4 |
| `DefaultVoxPlayerStatus` | `Audio.Asset.Vox.Normal` |
| `VoxPlayerStatusAssetTags` | Normal → `Audio.Asset.Vox.Normal`; LowStamina → `…LowStamina`; LowHealth → `…LowHealth`; Critical → `…Critical` |
| `VoxPlayerStatusThresholdValues` | LowHealth 50.0; LowStamina 10.0 |

`Dialogue` (priority 4) has no rows in DT_VoxData. Conversations probably use it, but the dump does not say so.

### 6c. DA_Vox_Profile01 ([`Vox/Profiles/Profile01`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Profiles/Profile01), class WDVoxAudioProfile)

81 `VoxLineAudio` entries, one per DT_VoxData row. Each maps a `VoxLine` tag to a `VoxAudioData` WDAudioData, with optional `VoxAudioData1P` and `VoxAudioData3P` (null in the sampled entry) and `bSeparatePerspectives` (false in the sampled entry). Example: `Audio.Vox.Exertion.Breath.Inhale` → [`DA_Vox_Profile01_Exert_Norm_Breath_Inhale`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/Exertions/Breathing/DAs/DA_Vox_Profile01_Exert_Norm_Breath_Inhale.json).

### 6d. Bark asset counts (WDAudioData under [`Vox/Barks/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks), 118 total)

| Folder | DAs |
|---|---|
| [`AssistanceRequest/DAs`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks/AssistanceRequest/DAs) | 26 |
| [`Spotting/DA`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks/Spotting/DA) | 62 |
| [`Orders/DAs`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks/Orders/DAs) | 10 |
| [`Social/DAs`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks/Social/DAs) | 10 |
| [`Squad/DAs`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Vox/Barks/Squad/DAs) | 10 |

Naming pattern: `DA_Vox_Profile01_Bark_<Category>_<Line>_1p` and `_3p`. Each bark has one SoundAssets entry per status (`Normal`, `LowHealth`).

Exertion DAs (26): Breathing 2, Critical state 1, Focus 2, Going critical 2, Going low health 2, Jump 1, Melee 4, Prone movement 1, Take damage (melee 1, heavy 2, light 2, weapon 1), Throwing grenade 2, Vaulting fast 1 and slow 2.

---

## 7. Music (DT_MusicSystem, 12 rows)

Row struct `WDMusicState`. Key = music state tag. Each row has a MetaSoundSource track, a 4/4 quarter-note time signature at 90 BPM, a priority, and transition-in/out settings.

| State tag | Track | Priority | Transition in (fade, s) | Transition out (fade, s) | Disable when deactivated |
|---|---|---|---|---|---|
| `Audio.Music.FrontEnd.MainMenu` | `MSS_Music_FrontEnd_MainMenu` | 100 | Logarithmic, 1.0 | Logarithmic, 20.0 | False |
| `Audio.Music.Death` | `MSS_Music_Death` | 80 | Logarithmic, 0.2 | Logarithmic, 1.0 | True |
| `Audio.Music.FirstSpawn` | `MSS_Music_InGame_FirstSpawn` | 59 | Logarithmic, 0.2 | Logarithmic, 1.0 | True |
| `Audio.Music.FirstTimeLeaveSpawn` | `MSS_Music_InGame_FirstTimeLeaveSpawn` | 5 | Logarithmic, 1.0 | Logarithmic, 1.0 | True |
| `Audio.Music.FirstTimeInCZ` | `MSS_Music_InGame_FirstTimeInCZ` | 6 | Logarithmic, 1.0 | Logarithmic, 1.0 | True |
| `Audio.Music.EndGame` | `MSS_Music_InGame_EndGame` | 101 | Logarithmic, 0.0 | Logarithmic, 15.0 | True |
| `Audio.Music.SpawnBoardWait` | `MSS_Gamemode_SpawnBoardWait` | 62 | Linear, 0.1 | Linear, 4.0 | True |
| `Audio.Music.Last10Points` | `MSS_Music_InGame_Last10Points` | 60 | Linear, 1.0 | Linear, 1.0 | True |
| `Audio.Music.Last5Points` | `MSS_Music_InGame_Last5Points_Loop` | 61 | Linear, 1.0 | Linear, 1.0 | False |
| `Audio.Music.ShootingRangeTutorial.FlyOver` | `MSS_Music_InGame_ShootingRangeTutorial_FlyOver` | 60 | Linear, 1.0 | Linear, 0.5 | False |
| `Audio.Music.Revived` | `MSS_Music_Revived` | 81 | Linear, 0.0 | Linear, 10.0 | True |
| `Audio.Music.PreGameCount` | `MSS_Music_PreGameCount` | 60 | Linear, 0.0 | Linear, 1.0 | True |

Music is driven by the `WDAudioEventBehaviorEnableMusicState` and `WDAudioEventBehaviorDisableMusicState` behaviours (9 and 32 instances). Priority direction (higher wins) is inferred from the values, not confirmed.

---

## 8. Impulse Resonance (DT_ImpulseResonance, 116 rows)

Row struct `WDImpulseResonanceEntry`. Key = static mesh name. Each row has `StaticMesh` (AssetPathName), `AudioEvent` (tag), and `AudioLocation`.

| Field | Distribution |
|---|---|
| `AudioLocation` | `HitLocation` 109, `OwningActor` 7 |
| Distinct `AudioEvent` tags | 14 |
| Top events | `Environment.ImpulseResonance.MetalSmall` 43, `…ShippingContainer` 18, `…OilDrum` 12, `…CivilianVehicle.Alarm` 8, `…Fence.Chainlink` 7, `…MetalBarrier` 6, `…Locomotive.FreightCar` 4, `…CivilianVehicle.NoAlarm` 4, `…LargeMetal` 4, `…SmallMetalContainer` 4 |
| Mesh folders | `Environment/Props` 80, [`Environment/Architecture`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Environment/Architecture) 30, `Maps/WhiteBox_Assets` 3, `Megascans/3D_Assets` 3 |

Example row. `SM_Village_Fence_01` → `Audio.Event.Environment.ImpulseResonance.Fence` at `HitLocation`.

Projectile-side data. `WDAudioEventBehaviorApplyImpulseResonance` (8 instances) holds `IdImpulseProperties` keyed by item ID tags, e.g. `Id.Item.SR_04` → `ResonanceRange` 1000.0, `VolumeScaling` 0.3. Units for `ResonanceRange` are not stored (probably UE centimetres).

---

## 9. Control Bus Mixes (PDA_CBM_Map, 3 assets)

Each maps the `Audio.CBM.Interior` and `Audio.CBM.Exterior` tags to a `SoundControlBusMix`.

| Asset | Interior | Exterior |
|---|---|---|
| [`DA_Vehicle_Land_TankArtillery_Vehicle_CBM_Map`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Land/PZH2000/DA/DA_Vehicle_Land_TankArtillery_Vehicle_CBM_Map.json) (PZH2000) | `AM_CBM_Vehicle_Exterior` | `AM_CBM_Vehicle_Exterior` |
| [`DA_Vehicle_Land_SpawnVehicle_CBM_Map`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Land/Spawn_Vehicle/DA/DA_Vehicle_Land_SpawnVehicle_CBM_Map.json) | `AM_CBM_Vehicle_Interior` | `AM_CBM_Vehicle_Exterior` |
| [`DA_Vehicle_Air_Helicopter_CBM_Map`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Shared/Helicopter/DA/DA_Vehicle_Air_Helicopter_CBM_Map.json) | `AM_CBM_Helicopter_Interior` | `AM_CBM_Helicopter_Exterior` |

The tank entry maps both tags to the Exterior mix. This may be intentional, or it may be a data error. Check it before relying on it.

Event-level mixes: 28 distinct `AM_CBM_*` names are referenced by events, for example `AM_CBM_Main`, `AM_CBM_Critical`, `AM_CBM_Focus`, `AM_CBM_ADS`, `AM_CBM_SafeZone`, `AM_CBM_NarratorActive`, `AM_CBM_TutorialVideo`, `AM_CBM_UIScene`, `AM_CBM_UIScene_Vendor`, `AM_CBM_UIScene_Scoreboard`, `AM_CBM_Helicopter_Interior_Gunner`, `AM_CBM_TGMFlight1p`.

---

## 10. Ambience Significance

| Asset | Content |
|---|---|
| [`DA_Significance_KavkaziRiver`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Ambience/DA_Significance_KavkaziRiver.json) (BHSignificanceSettingsAsset) | One sphere evaluator. Two LevelSettings entries: TickRate 0.0 / SignificanceUpdateRate 0.03 / LocationUpdateRate 0.1, and TickRate 2.0 / SignificanceUpdateRate 2.0 / LocationUpdateRate 2.0 |
| [`DA_Significance_Kavkazi_Sphere_Evaluator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Ambience/DA_Significance_Kavkazi_Sphere_Evaluator.json) (BHSignificanceEvaluator_Sphere) | Settings with `Distance` 0.0 and 6000.0 |

The 6000.0 distance is probably UE centimetres (60 m). The meaning of the two LevelSettings entries is not stored. Ambience events: [`AE_AMB_3D_Water_Lake`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Ambience/3D/Water/AE_AMB_3D_Water_Lake.json) (MSS_AMB_3D_Water_Lake), [`AE_AMB_3D_Water_River`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Ambience/3D/Water/AE_AMB_3D_Water_River.json) (MSS_Amb_3D_RiverSpline), [`AE_StartDistantWarfare`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Events/Ambience/DistantWarfare/AE_StartDistantWarfare.json) (no behaviours).

---

## 11. Curves (42 CurveFloat)

| Folder | Count | Shape |
|---|---|---|
| [`Attenuations/HDR/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Attenuations/HDR) | 34 | Mostly 1.0 → 0.0 over normalised time 0 to 1 (3 to 10 keys). Two peak at 0.8: [`CC_HDR_ATT_Movement_Close_Enemy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_ATT_Movement_Close_Enemy.json), [`CC_HDR_ATT_Movement_Stance`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_ATT_Movement_Stance.json). Named by range or source, e.g. [`CC_HDR_800m`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_800m.json), [`CC_HDR_ATT_Weapon_Fire_Artillery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_ATT_Weapon_Fire_Artillery.json), [`CC_HDR_ATT_Vehicle_Engine`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_ATT_Vehicle_Engine.json), [`CC_HDR_Falloff_Resonance`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_Falloff_Resonance.json). |
| `Curves/` | 7 | [`AU_CRV_ExertionDecayRate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/AU_CRV_ExertionDecayRate.json) 0.03 → 0.06; [`AU_CRV_ExertionDecayRate_ADS`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/AU_CRV_ExertionDecayRate_ADS.json) 0.0 → 0.06; [`CC_Amb_DistantWarfare_Kavkazi_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/Amb/CC_Amb_DistantWarfare_Kavkazi_Audio.json) 0 → 1; [`CC_Vehicle_Destroy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/Explosions/CC_Vehicle_Destroy.json) 1 → 0; [`CC_Weapon_SMG_Fire_ExternalCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/Gunshots/CC_Weapon_SMG_Fire_ExternalCurve.json) 1 → 0.25; [`CC_UI_Ping`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/Ping/CC_UI_Ping.json) 1 → 0.035 over 1.001; [`CC_Targeting_LockOn`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Curves/Targeting%2B/CC_Targeting_LockOn.json) 1 → 0 |
| `Vehicles/Shared/` | 1 | [`AU_CRV_Reversing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Shared/AU_CRV_Reversing.json) 0 → 0.56 |

The `HDR` prefix is not explained in the dump. The time axis unit is not stored. The [`CC_HDR_800m`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Attenuations/HDR/CC_HDR_800m.json) name suggests an 800 m range, but that is inferred.

---

## 12. Small singletons

| Asset | Content |
|---|---|
| [`DA_MicLevelMeter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/UI/Data/DA_MicLevelMeter.json) (WDMicLevelMeterData) | No exported properties |
| `REVModelAsset` at [`Vehicles/Land/PZH2000/Wavs/EngineRevs_Ignition_TurnOff/SFX_Vehicles_Land_PZH2000_Engine_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vehicles/Land/PZH2000/Wavs/EngineRevs_Ignition_TurnOff/SFX_Vehicles_Land_PZH2000_Engine_02.json) | Properties are null in the export. The engine-revs model content is not in the dump. |

---

## 13. How values combine (what can be said from the data)

1. **Event fires behaviours.** An event lists its behaviours in stored order. Whether they run in sequence or in parallel is not in the dump.
2. **Tag resolves to asset.** A behaviour's tag (e.g. `Audio.Asset.Player.Footstep.1p`) is looked up in a WDAudioData's `SoundAssets`. Each entry is a MetaSoundSource or SoundWave. `SoundAssetSets` maps a set tag to member tags, so a set tag probably picks one member at random.
3. **Perspective and hostility choose the variant.** `1p` is for the player's own view, `3p` for others. `Ally` and `Enemy` come from the hostility-aware behaviour. These are inferred from tag names.
4. **Vox.** `RequestVox` (or the Squad/Damaged variants) carries a `LineID` that is a row key in DT_VoxData. Its group (Narrator, Bark, Exertion) sets priority through VoxGroupPriorities. The status (Normal, LowHealth, LowStamina, Critical) chooses which variant is used, based on the thresholds 50 HP and 10 stamina. Interrupt rules come from `InterruptibleBehavior`.
5. **Music.** A music state tag from DT_MusicSystem is enabled or disabled by behaviours. Priority decides which state wins (direction inferred).
6. **Mixes.** Activate and Deactivate CBM behaviours add or remove a `SoundControlBusMix`. Interior and exterior CBMs per vehicle come from the PDA_CBM_Map assets.

---

## Still not pulled / limitations

- **Sound content.** MetaSoundSource graphs (`.uasset` internals), SoundWave durations, loudness and sample data are not in the JSON. Event durations and loudness cannot be stated.
- **Behaviour logic.** The `AEB_*` and `WDAudioEventBehavior*` classes are Blueprint or C++ classes. Their code is not exported, so execution order, blending and what each behaviour does internally are inferred from property names.
  - **SDK (2026-10-16):** audio-event behaviour helpers are in [`BFL_AudioEventBehaviorHelpers_classes.hpp`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/BFL_AudioEventBehaviorHelpers_classes.hpp) (`UBFL_AudioEventBehaviorHelpers_C`, a `UBlueprintFunctionLibrary`). It exposes 14 static/member functions including:
    - `Evaluate_Restart_Behavior(AudioComp, Sound, ESoundRestartBehavior, ...)` — the restart-logic decision function (resolves "execution order" partially)
    - `HandlePlaySound(Context, Sound, RestartBehavior, Only_If_In_Range, CancelFadeOut, _aaabfkmmjhhnafhaehpbd (double), AttachParent, SocketName, Location, ...)` — the main sound-dispatch function; one parameter (`double`) remains unnamed and is a candidate for the "reload-stage value 50.5" the doc flagged
    - `GetSurfaceTypeCharacterIsStoodOn(Character, ..., Fluid_Depth, EWDAudioSurface, EPhysicalSurface, IsFromFoliage, Normal)` — resolves surface detection logic
    - `DetermineHostilityOfCharacter(Character, ..., Friendly)` and `DeterminePerspetiveOfCharacter(Character, ..., FirstPerson)` — hostility + perspective evaluators
    - `Handle_Helicopter_Audio_State_Change` — vehicle-specific audio state machine
  - Inner Blueprint logic of specific `AEB_*` classes still not exported (Dumper-7 captures signatures, not implementation bytecode).
- **Hashed property names.** The float on events (222 instances including behaviours), the bool and enum on DT_VoxData rows, and a list-valued hash on `WDAudioEventBehaviorApplyImpulseResonance` are unnamed. Their meaning is not confirmed. The reload-stage value 50.5 and comms value 80.0 are the most useful clues.
  - **SDK (2026-10-16, re-checked 2026-10-18):** the float is the native property `_aaabhgndclheajnnlnade` on `UCrosstalkAudioEvent` (`+0x4C`) and `UCrosstalkAudioEventBehavior` (`+0xBC`); its name is still hashed in this build. It is not the `HandlePlaySound` parameter `_aaabfkmmjhhnafhaehpbd`, a different (21-character) name. Without a resolved symbolic name from Dumper, static resolution hits its limit; next step is observational (what value is passed at specific event call-sites).
- **Priority direction.** It is not stored whether higher or lower numbers win for vox group priorities or music priorities.
- **Curve units.** Time and value units for the 42 curves are not stored. Distances in UE units are assumed to be centimetres but not verified.
- **Vox Dialogue group.** Priority 4 exists in settings but has no DT_VoxData rows.
- **Possible data issues.** The tank CBM map sends both interior and exterior to the exterior mix. `ConcurrentInstanceLimit` 0 appears on 34 `AEB_VehiclePerspective_C` instances. Both are flagged for review, not corrected.
- **Empty or null exports.** [`DA_MicLevelMeter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/UI/Data/DA_MicLevelMeter.json) has no properties. The `REVModelAsset` export has null properties.
- **Cross-references outside Audio.** Many references (`/Game/Maps/...`, `/Game/Environment/...` meshes, `SBMIX_*` submixes, weapon and vehicle BPs) point outside this folder and were not resolved.
- **Event tag to asset mismatch.** Around 40 events have a tag that does not match the asset name. Runtime lookup by tag is inferred, not verified.

---

## Appendix A. All 675 events

Generated from the census script (`events_summary.json`). Chain shows the first three behaviours as stored; `-> ...` means more follow. Rows 634 to 675 are the events added in the Season 02 update, listed in their own group at the end.

| # | Event asset | NameTag | Behaviours | Chain (first items, as stored) |
|---|---|---|---|---|
| | **(Events root)** | | | |
| 1 | AE_Debug_23lufs | `Audio.Event.Debug.23lufs` | 1 | PlaySound(SFX_-23db) |
| 2 | AE_Debug_AnimSync | `Audio.Event.Debug.AnimSync` | 1 | PlaySound(MSS_Debug_AnimSync) |
| 3 | AE_OnDisconnect_Reset | `Audio.Event.OnDisconnect.Reset` | 2 | DeactivateAllControlBusMix -> Submix_DeactivateEffect(SBMIX_CriticalGroup_Heavy, SBMIX_CriticalGroup_Medium, SBMIX_CriticalGroup_Light) |
| 4 | AE_StopEvent | `Audio.Event.StopSound` | 1 | StopSound |
| 5 | AE_StopEventFadeTrigger | `Audio.Event.StopSoundFade` | 1 | StopSound |
| | **Ambience/3D/Water** | | | |
| 6 | AE_AMB_3D_Water_Lake | `Audio.Event.Ambience.3D.Water.Lake` | 1 | PlaySound(MSS_AMB_3D_Water_Lake) |
| 7 | AE_AMB_3D_Water_River | `Audio.Event.Ambience.3D.Water.River` | 1 | PlaySound(MSS_Amb_3D_RiverSpline) |
| | **Ambience/DistantWarfare** | | | |
| 8 | AE_StartDistantWarfare | `Audio.Event.Ambience.3D.DistantWarfare` | 0 |  |
| | **Comms** | | | |
| 9 | AE_Comms_Played | `Audio.Event.Comms.Played` | 2 | Comms_VehiclePerspective_StartedSpeaking -> HelmetMuffle |
| | **Comms/AssistanceRequests** | | | |
| 10 | AE_Comms_Request_AcknowledgedRequest | `Audio.Event.Comms.Request.AcknowledgedRequest` | 1 | RequestVox(tag:Audio.Vox.Bark.Request.Acknowledge) |
| 11 | AE_Comms_Request_Ammo | `Audio.Event.Comms.Request.Ammo` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Ammo) -> AttachToActor |
| 12 | AE_Comms_Request_Backup | `Audio.Event.Comms.Request.Backup` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Backup) -> AttachToActor |
| 13 | AE_Comms_Request_Dropoff | `Audio.Event.Comms.Request.Dropoff` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.DropOff) -> AttachToActor |
| 14 | AE_Comms_Request_Fuel | `Audio.Event.Comms.Request.Fuel` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Fuel) -> AttachToActor |
| 15 | AE_Comms_Request_GetIn | `Audio.Event.Comms.Request.GetIn` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.GetIn) -> AttachToActor |
| 16 | AE_Comms_Request_GetOut | `Audio.Event.Comms.Request.GetOut` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.GetOut) -> AttachToActor |
| 17 | AE_Comms_Request_Healing | `Audio.Event.Comms.Request.Healing` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Healing) -> AttachToActor |
| 18 | AE_Comms_Request_Pickup | `Audio.Event.Comms.Request.Pickup` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Pickup) -> AttachToActor |
| 19 | AE_Comms_Request_Repair | `Audio.Event.Comms.Request.Repair` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Repair) -> AttachToActor |
| 20 | AE_Comms_Request_RequestAcknowledged | `Audio.Event.Comms.Request.RequestAcknowledged` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Acknowledge) -> AttachToActor |
| 21 | AE_Comms_Request_Revive | `Audio.Event.Comms.Request.Revive` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Revive) -> AttachToActor |
| 22 | AE_Comms_Request_SquadInvite | `Audio.Event.Comms.Request.SquadInvite` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.SquadInvite) -> AttachToActor |
| 23 | AE_Comms_Request_Supplies | `Audio.Event.Comms.Request.Supplies` | 2 | RequestVox(tag:Audio.Vox.Bark.Request.Supplies) -> AttachToActor |
| 24 | AE_Comms_Request_Supplies_Radio | `Audio.Event.Comms.Request.Supplies.Radio` | 1 | PlaySound(MSS_Vox_Bark_Norm_Request_Supplies_Radio_Preset) |
| | **Comms/Orders** | | | |
| 25 | AE_Comms_Order_Attack | `Audio.Event.Comms.Order.Attack` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Order.Attack) -> AttachToActor |
| 26 | AE_Comms_Order_Defend | `Audio.Event.Comms.Order.Defend` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Order.Defend) -> AttachToActor |
| 27 | AE_Comms_Order_FallBack | `Audio.Event.Comms.Order.FallBack` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Order.FallBack) -> AttachToActor |
| 28 | AE_Comms_Order_Fortify | `Audio.Event.Comms.Order.Fortify` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Order.Fortify) -> AttachToActor |
| 29 | AE_Comms_Order_Regroup | `Audio.Event.Comms.Order.Regroup` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Order.Regroup) -> AttachToActor |
| | **Comms/Social** | | | |
| 30 | AE_Comms_Social_Nice | `Audio.Event.Comms.Social.Nice` | 2 | RequestVox(tag:Audio.Vox.Bark.Social.Nice) -> AttachToActor |
| 31 | AE_Comms_Social_No | `Audio.Event.Comms.Social.No` | 2 | RequestVox(tag:Audio.Vox.Bark.Social.No) -> AttachToActor |
| 32 | AE_Comms_Social_Sorry | `Audio.Event.Comms.Social.Sorry` | 2 | RequestVox(tag:Audio.Vox.Bark.Social.Sorry) -> AttachToActor |
| 33 | AE_Comms_Social_Thanks | `Audio.Event.Comms.Social.Thanks` | 2 | RequestVox(tag:Audio.Vox.Bark.Social.Thanks) -> AttachToActor |
| 34 | AE_Comms_Social_Yes | `Audio.Event.Comms.Social.Yes` | 2 | RequestVox(tag:Audio.Vox.Bark.Social.Yes) -> AttachToActor |
| | **Comms/Squad** | | | |
| 35 | AE_Comms_Squad_Affirmative | `Audio.Event.Comms.Squad.Affirmative` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Squad.Affirmative) -> AttachToActor |
| 36 | AE_Comms_Squad_FollowMe | `Audio.Event.Comms.Squad.FollowMe` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Squad.FollowMe) -> AttachToActor |
| 37 | AE_Comms_Squad_Negative | `Audio.Event.Comms.Squad.Negative` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Squad.Negative) -> AttachToActor |
| 38 | AE_Comms_Squad_OnMyWay | `Audio.Event.Comms.Squad.OnMyWay` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Squad.OnMyWay) -> AttachToActor |
| 39 | AE_Comms_Squad_WatchHere | `Audio.Event.Comms.Squad.WatchHere` | 2 | RequestSquadVox(tag:Audio.Vox.Bark.Squad.WatchHere) -> AttachToActor |
| | **Comms/VOIP** | | | |
| 40 | AE_Comms_LoggingIn_Connected | `Audio.Event.Comms.LoggingIn.Connected` | 1 | PlaySound(MSS_Comms_LoggingIn_Connected_Preset) |
| 41 | AE_Comms_LoggingIn_Connecting | `Audio.Event.Comms.LoggingIn.Connecting` | 1 | PlaySound(MSS_Comms_LoggingIn_Connecting_Preset) |
| 42 | AE_Comms_LoggingIn_Disconnected | `Audio.Event.Comms.LoggingIn.Disconnected` | 1 | PlaySound(MSS_Comms_LoggingIn_Disconnected_Preset) |
| 43 | AE_Comms_LoggingIn_Disconnecting | `Audio.Event.Comms.LoggingIn.Disconnecting` | 1 | PlaySound(MSS_Comms_LoggingIn_Disconnecting_Preset) |
| 44 | AE_Comms_LoudspeakerStarted | `Audio.Event.Comms.LoudspeakerStarted` | 3 | Comms_RestartPlayerVoice -> TriggerParam(str:Trigger) -> PlaySound(MSS_Comms_SelfSpeaking_Loudspeaker) |
| 45 | AE_Comms_LoudspeakerStopped | `Audio.Event.Comms.LoudspeakerStopped` | 3 | Comms_RestartPlayerVoice -> TriggerParam(str:Stop) -> PlaySound(MSS_Comms_SelfSpeaking_Loudspeaker) |
| 46 | AE_Comms_MicTest_Started | `Audio.Event.Comms.MicTest.Started` | 1 | Comms_StartPlayerVoice |
| 47 | AE_Comms_MicTest_Stopped | `Audio.Event.Comms.MicTest.Stopped` | 2 | EndBehavior -> StopSound |
| 48 | AE_Comms_PlayerStartedSpeaking | `Audio.Event.Comms.PlayerStartedSpeaking` | 3 | Comms_StartPlayerVoice -> Comms_VehiclePerspective_StartedSpeaking -> HelmetMuffle |
| 49 | AE_Comms_PlayerStartedSpeaking_Self | `Audio.Event.UI.VOIP.TransmitPress` | 1 | Comms_SelfSpeaking(MSS_Comms_SelfSpeaking, MSS_Comms_SelfSpeaking_Fail) |
| 50 | AE_Comms_PlayerStartedSpeaking_Self_Fail | `Audio.Event.UI.VOIP.TransmitPress.Fail` | 1 | Comms_SelfSpeaking(MSS_Comms_SelfSpeaking_Fail) |
| 51 | AE_Comms_PlayerStoppedSpeaking | `Audio.Event.Comms.PlayerStoppedSpeaking` | 4 | EndBehavior -> EndBehavior -> StopSound -> ... |
| 52 | AE_Comms_PlayerStoppedSpeaking_Self | `Audio.Event.UI.VOIP.TransmitRelease` | 1 | Comms_SelfSpeaking(MSS_Comms_SelfSpeaking, MSS_Comms_SelfSpeaking_Fail) |
| 53 | AE_Comms_PlayerStoppedSpeaking_Self_Fail | `Audio.Event.UI.VOIP.TransmitRelease.Fail` | 1 | Comms_SelfSpeaking(MSS_Comms_SelfSpeaking_Fail) |
| | **Destruction** | | | |
| 54 | AE_Destruction_Building | `Audio.Event.Destruction.Building` | 2 | PlaySound(MSS_Destruction_Building_Prototype) -> WDMoveSoundToGameplayCueLocation |
| 55 | AE_Destruction_Chunk | `Audio.Event.Destruction.Chunk` | 1 | Destructionhunk_v2(DA_Destruction_Building_Chunk_Small_Transients, DA_Destruction_Building_Chunk_Small_Tails, DA_Destruction_Buil) |
| 56 | AE_Destruction_Decorator | `Audio.Event.Destruction.Decorator` | 1 | Destruction_Decorator |
| 57 | AE_Destruction_SmashableWindow | `Audio.Event.Destruction.SmashableWindow` | 2 | AttachToActor -> PlaySound(MSS_Dest_Glass_WindowSmash) |
| 58 | AE_Destruction_WindowDamage | `Audio.Event.Destruction.DamagedWindow` | 3 | WindowDamage -> AttachToActor -> PlaySound(MSS_Dest_Glass_WindowDamage) |
| | **Doors** | | | |
| 59 | AE_Door_Breach_Melee | `Audio.Event.Door.Breach.Melee` | 3 | AttachSoundToDoorHandle -> SelectDoorSound(MSS_Door_Metal_Breach, MSS_Door_Breach) -> TriggerParam(str:BreachMelee) |
| 60 | AE_Door_Breach_Sprint | `Audio.Event.Door.Breach.Sprint` | 3 | AttachSoundToDoorHandle -> SelectDoorSound(MSS_Door_Metal_Breach, MSS_Door_Breach) -> TriggerParam(str:BreachSprint) |
| 61 | AE_Door_Close | `Audio.Event.Door.Close` | 3 | AttachSoundToDoorHandle -> SelectDoorSound -> TriggerParam(str:Close) |
| 62 | AE_Door_Open | `Audio.Event.Door.Open` | 3 | AttachSoundToDoorHandle -> SelectDoorSound -> TriggerParam(str:Open) |
| 63 | AE_Door_Open_Foley | `Audio.Event.Door.Foley` | 2 | PerspSound(MSS_Door_Open_Foley_1p, MSS_Door_Open_Foley_3p) -> AttachToActor |
| 64 | AE_Door_PeekClose | `Audio.Event.Door.PeekClose` | 3 | AttachSoundToDoorHandle -> SelectDoorSound(MSS_Door_Metal_PeekOpenClose, MSS_Door_PeekOpenClose) -> TriggerParam(str:PeekClose) |
| 65 | AE_Door_PeekOpen | `Audio.Event.Door.PeekOpen` | 3 | AttachSoundToDoorHandle -> SelectDoorSound(MSS_Door_Metal_PeekOpenClose, MSS_Door_PeekOpenClose) -> TriggerParam(str:PeekOpen) |
| 66 | AE_Door_Unlock | `Audio.Event.Door.Unlock` | 2 | AttachToActor -> PlaySound(MSS_Door_Metal_Unlock) |
| 67 | AE_Door_Warehouse_Play | `Audio.Event.Door.Warehouse` | 3 | AttachToActor -> TriggerParam(str:Start) -> PlaySound(MSS_Door_Warehouse_OpenClose) |
| 68 | AE_Door_Warehouse_Stop | `Audio.Event.Door.Warehouse.Stop` | 1 | TriggerParam(str:Stop) |
| | **Environment/ImpulseResonance** | | | |
| 69 | AE_ImpulseResonance_BarbedWire | `Audio.Event.Environment.ImpulseResonance.Fence.BarbedWire` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_BarbedWire) |
| 70 | AE_ImpulseResonance_CivilianVehicle_Alarm | `Audio.Event.Environment.ImpulseResonance.CivilianVehicle.Alarm` | 3 | SetImpulseResonanceParameters -> AttachToActor -> WDPlaySoundCullNearbyDuplicates(MSS_Ambience_Resonance_CivilianVehicle_Alarm) |
| 71 | AE_ImpulseResonance_CivilianVehicle_NoAlarm | `Audio.Event.Environment.ImpulseResonance.CivilianVehicle.NoAlarm` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_CivilianVehicle_MetalResonance) |
| 72 | AE_ImpulseResonance_Fence | `Audio.Event.Environment.ImpulseResonance.Fence.Chainlink` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_Fence_Rattle) |
| 73 | AE_ImpulseResonance_FoundryCrane | `Audio.Event.Environment.ImpulseResonance.FoundryCrane` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_FoundryCrane) |
| 74 | AE_ImpulseResonance_LargeMetalGroans | `Audio.Event.Environment.ImpulseResonance.LargeMetal` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_LargeMetalGroan) |
| 75 | AE_ImpulseResonance_Locomotive_FreightCar | `Audio.Event.Environment.ImpulseResonance.Locomotive.FreightCar` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_Locomotive_FreightCar) |
| 76 | AE_ImpulseResonance_MetalBarrier | `Audio.Event.Environment.ImpulseResonance.MetalBarrier` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_MetalBarrier) |
| 77 | AE_ImpulseResonance_OilDrum | `Audio.Event.Environment.ImpulseResonance.OilDrum` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_OilDrum) |
| 78 | AE_ImpulseResonance_ShippingContainer | `Audio.Event.Environment.ImpulseResonance.ShippingContainer` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_Container) |
| 79 | AE_ImpulseResonance_SmallMetal | `Audio.Event.Environment.ImpulseResonance.MetalSmall` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_SmallMetal) |
| 80 | AE_ImpulseResonance_SmallRattlingContainer | `Audio.Event.Environment.ImpulseResonance.SmallMetalContainer` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_SmallMetalContainer) |
| 81 | AE_ImpulseResonance_TreeLarge | `Audio.Event.Environment.ImpulseResonance.Tree` | 2 | SetImpulseResonanceParameters -> PlaySound(MSS_Ambience_Resonance_TreeFoliage) |
| | **Gamemode** | | | |
| 82 | AE_AirRaidSiren_Radio | `Audio.Event.Environment.AirRaidSiren.Radio` | 1 | PlaySound(MSS_10PointSiren_Radio) |
| 83 | AE_AirRaidSiren_Tower | `Audio.Event.Environment.AirRaidSiren.Tower` | 1 | PlaySound(MSS_10PointSiren_Tower) |
| 84 | AE_Gamemode_DeployScreen_Enter | `Audio.Event.Gamemode.DeployScreen.Enter` | 1 | ActivateCBM(AM_CBM_UIScene_DeploymentScreen) |
| 85 | AE_Gamemode_DeployScreen_Exit | `Audio.Event.Gamemode.DeployScreen.Exit` | 2 | DeactivateCBM(AM_CBM_UIScene_DeploymentScreen) -> SetDeployScreenExit |
| 86 | AE_Gamemode_EndGame_ControlBusmanager | `Audio.Event.Gamemode.EndGame` | 7 | DeactivateCBM(AM_CBM_Helicopter_Interior) -> DeactivateCBM(AM_CBM_Helicopter_Interior_Gunner) -> DeactivateCBM(AM_CBM_Vehicle_DuneBuggy_Interior) -> ... |
| 87 | AE_Gamemode_FactionSelect_Enter | `Audio.Event.Gamemode.FactionSelect.Enter` | 1 | ActivateCBM(AM_CBM_UIScene_FactionSelect) |
| 88 | AE_Gamemode_FactionSelect_Exit | `Audio.Event.Gamemode.FactionSelect.Exit` | 1 | DeactivateCBM(AM_CBM_UIScene_FactionSelect) |
| 89 | AE_Gamemode_LoadingScreen_Enter | `Audio.Event.Gamemode.LoadingScreen.Enter` | 1 | LoadingScreen_Enter |
| 90 | AE_Gamemode_LoadingScreen_Exit | `Audio.Event.Gamemode.LoadingScreen.Exit` | 1 | LoadingScreen_Exit |
| | **Gamemode/SpawnBoard** | | | |
| 91 | AE_Gamemode_SpawnBoardFail | `Audio.Event.Gamemode.SpawnBoard.Fail` | 3 | TriggerParam(str:OnSpawnFailed) -> PlaySound(MSS_Gamemode_SpawnBoardWait) -> WDMoveSoundToGameplayCueLocation |
| 92 | AE_Gamemode_SpawnBoardFinished | `Audio.Event.Gamemode.SpawnBoard.Finished` | 2 | DeactivateCBM(AM_CBM_SpawnBoardWait) -> DisableMusic(tag:Audio.Music.SpawnBoardWait) |
| 93 | AE_Gamemode_SpawnBoardWait | `Audio.Event.Gamemode.SpawnBoard.Wait` | 3 | ActivateCBM(AM_CBM_SpawnBoardWait) -> PlaySound(MSS_UI_DeploymentBoard_StartWait) -> EnableMusic(tag:Audio.Music.SpawnBoardWait) |
| 94 | AE_Gamemode_SpawnBoard_Loop | `Audio.Event.Gamemode.SpawnBoard` | 2 | AttachToActor -> PlaySound(MSS_Gamemode_SpawnBoard) |
| 95 | AE_Gamemode_SpawnBoard_Radar_Start | `Audio.Event.Gamemode.SpawnBoard.Radar.Start` | 3 | MoveSoundToDeploymentRadarDish(str:radar_Pitch_J) -> PlayAllegianceSound(MSS_Gamemode_SpawnBoardRadar_Patriot, MSS_Gamemode_SpawnBoardRadar_Molotok, MSS_Gamemode_SpawnBoa |
| 96 | AE_Gamemode_SpawnBoard_Radar_Stop | `Audio.Event.Gamemode.SpawnBoard.Radar.Stop` | 2 | SetBool(str:VehicleReady) -> StopSound |
| | **Music** | | | |
| 97 | AE_Music_Deployed | `Audio.Event.Music.Deployed` | 3 | DeactivateCBM(AM_CBM_UIScene_PopUpWindow) -> DeactivateCBM(AM_CBM_UIScene_DeploymentScreen) -> Music_Deployed |
| 98 | AE_Music_MapLoad | `Audio.Event.Music.MapLoad` | 2 | ActivateCBM(AM_CBM_UIScene_DeploymentScreen) -> Music_MapLoad |
| | **Music/FrontEnd** | | | |
| 99 | AE_Music_FrontEnd_MainMenu | `Audio.Event.Music.FrontEnd.MainMenu` | 3 | DisableMusic(tag:Audio.Music.EndGame) -> DisableMusic(tag:Audio.Music.FirstSpawn) -> EnableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| | **Music/InGame** | | | |
| 100 | AE_Music_InGame_EndGame | `Audio.Event.Music.InGame.EndGame` | 10 | ActivateCBM(AM_CBM_Main) -> ActivateCBM(AM_CBM_EndGame) -> DeactivateCBM(AM_CBM_Critical) -> ... |
| 101 | AE_Music_InGame_FirstSpawn | `Audio.Event.Music.InGame.FirstSpawn` | 1 | EnableFirstSpawnMusicState |
| 102 | AE_Music_InGame_Last10Points | `Audio.Event.Music.InGame.Last10Points` | 1 | EnableMusic(tag:Audio.Music.Last10Points) |
| 103 | AE_Music_InGame_Last10Points_FinalPoint | `Audio.Event.Music.InGame.Last10Points.FinalPoint` | 0 |  |
| 104 | AE_Music_InGame_PreGameCount | `Audio.Event.Music.InGame.PreGameCount` | 1 | EnableMusic(tag:Audio.Music.PreGameCount) |
| 105 | AE_Music_InGame_TeamSelect | `Audio.Event.Music.InGame.TeamSelect` | 1 | PlaySound(MSS_Music_InGame_TeamSelect) |
| | **Player** | | | |
| 106 | AE_PingTeammates_Danger | `Audio.Event.Player.PingTeammates.Danger` | 3 | PlayPerspectiveSound_PlayerState(MSS_UI_InGame_Ping_1p, MSS_UI_InGame_Ping_3p) -> TriggerParam(str:TriggerDanger) -> WDMoveSoundToGameplayCueLocation |
| 107 | AE_PingTeammates_Default | `Audio.Event.Player.PingTeammates.Default` | 3 | PlayPerspectiveSound_PlayerState(MSS_UI_InGame_Ping_1p, MSS_UI_InGame_Ping_3p) -> TriggerParam(str:TriggerDefault) -> WDMoveSoundToGameplayCueLocation |
| 108 | AE_Player_EnteredControlZone | `Audio.Event.Player.EnteredControlZone` | 0 |  |
| 109 | AE_Player_Exertion | `Audio.Event.Player.Exertion` | 2 | RequestVox(tag:Audio.Vox.Exertion.MeleeSwing) -> AttachToActor |
| | **Player/Damaged** | | | |
| 110 | AE_Player_Damaged_Explosion | `Audio.Event.Player.Damaged.Explosive` | 6 | ActivateCBM(AM_CBM_DamageFromExplosion) -> DeactivateCBM(AM_CBM_DamageFromExplosion) -> PlayHitConfirmSound -> ... |
| 111 | AE_Player_Damaged_Fall | `Audio.Event.Player.Damaged.Fall` | 5 | ModifyCosmeticExertion -> PerspSound(MSS_Player_Damage_FromFall_1p, MSS_Player_Damage_FromFall_3p) -> RequestDamagedVox(tag:Audio.Vox.Exertion.TakingDamage.Light, Audio.V |
| 112 | AE_Player_Damaged_Impact | `Audio.Event.Player.Damaged.Impact` | 4 | PerspSound(MSS_Player_Damage_FromImpact_1p, MSS_Player_Damage_FromImpact_3p_Preset) -> RequestDamagedVox(tag:Audio.Vox.Exertion.TakingDamage.Light, Audio.Vox.Exertion.Tak |
| 113 | AE_Player_Damaged_Melee | `Audio.Event.Player.Damaged.Melee` | 4 | PerspSound(MSS_Player_Damage_FromMelee_1p, MSS_Player_Damage_FromMelee_3p) -> RequestDamagedVox(tag:Audio.Vox.Exertion.TakingDamage.Light, Audio.Vox.Exertion.TakingDamage |
| 114 | AE_Player_Damaged_Projectile | `Audio.Event.Player.Damaged.Projectile` | 5 | PerspSound(MSS_Player_Damage_FromBullet_3p) -> RequestDamagedVox(tag:Audio.Vox.Exertion.TakingDamage.Light, Audio.Vox.Exertion.TakingDamage.Heavy) -> AttachToActor -> ... |
| 115 | AE_Player_TakeHit | `Audio.Event.Player.TakeHit` | 4 | ModifyCosmeticExertion -> PlayHitConfirmSound(MSS_Player_Damage_Hurtmarker_Flesh, MSS_Player_Damage_Armor_Break_1p, MSS_Player_Damage_Helmet_Break_1p) -> AttachToActor -> |
| | **Player/Death** | | | |
| 116 | AE_Player_Death | `Audio.Event.Player.Death` | 8 | DeactivateControlBusMixes(AM_CBM_ADS, AM_CBM_Focus, AM_CBM_Helicopter_Exterior, AM_CBM_Helicopter_Interior, AM_CBM_Helicopter_Interior_G) -> PlayPerspectiveDeathSound(MSS |
| 117 | AE_Player_Death_BodyFall | `Audio.Event.Player.Death.BodyFall` | 2 | PlayBodyFall(MSS_Player_Death_BodyFall_Standing_1p, MSS_Player_Death_BodyFall_Standing_3p) -> AttachToActor |
| 118 | AE_Player_GiveUp | `Audio.Event.Player.GiveUp` | 2 | PerspSound(MSS_Player_Damage_Death_GiveUp_1p, MSS_Player_Damage_Death_GiveUp_3p) -> AttachToActor |
| 119 | AE_Player_GiveUp_Local | `Audio.Event.Player.GiveUp.Local` | 3 | ActivateCBM(AM_CBM_GiveUp) -> EndBehavior -> DisableMusic(tag:Audio.Music.Death) |
| | **Player/Emotes** | | | |
| 120 | AE_Player_Emotes_Assault | `Audio.Event.Player.Emote.Assault` | 2 | PerspSound(MSS_Player_Emotes_Assault_1p, MSS_Player_Emotes_Assault_3p) -> AttachToActor |
| 121 | AE_Player_Emotes_GenericEnd | `Audio.Event.Player.Emote.GenericEnd` | 2 | PerspSound(MSS_Player_Emotes_GenericEnd_1p, MSS_Player_Emote_GenericEnd_3p) -> AttachToActor |
| 122 | AE_Player_Emotes_Halt | `Audio.Event.Player.Emote.Halt` | 2 | PerspSound(MSS_Player_Emotes_Halt_1p, MSS_Player_Emote_Halt_3p) -> AttachToActor |
| 123 | AE_Player_Emotes_MiddleFinger | `Audio.Event.Player.Emote.MiddleFinger` | 2 | PerspSound(MSS_Player_Emotes_MiddleFinger_1p, MSS_Player_Emote_MiddleFinger_3p) -> AttachToActor |
| 124 | AE_Player_Emotes_MoveUp | `Audio.Event.Player.Emote.MoveUp` | 2 | PerspSound(MSS_Player_Emotes_MoveUp_1p, MSS_Player_Emote_MoveUp_3p) -> AttachToActor |
| 125 | AE_Player_Emotes_Point | `Audio.Event.Player.Emote.Point` | 2 | PerspSound(MSS_Player_Emotes_Point_1p, MSS_Player_Emote_Point_3p) -> AttachToActor |
| 126 | AE_Player_Emotes_Rps | `Audio.Event.Player.Emote.Rps` | 2 | PerspSound(MSS_Player_Emotes_Rps_1p, MSS_Player_Emote_Rps_3p) -> AttachToActor |
| 127 | AE_Player_Emotes_Shh | `Audio.Event.Player.Emote.Shh` | 2 | PerspSound(MSS_Player_Emotes_Shh_1p, MSS_Player_Emote_Shh_3p) -> AttachToActor |
| 128 | AE_Player_Emotes_Surrender | `Audio.Event.Player.Emote.Surrender` | 2 | PerspSound(MSS_Player_Emotes_Surrender_1p, MSS_Player_Emote_Surrender_3p) -> AttachToActor |
| 129 | AE_Player_Emotes_ThumbsDown | `Audio.Event.Player.Emote.ThumbsDown` | 2 | PerspSound(MSS_Player_Emotes_ThumbsDown_1p, MSS_Player_Emote_ThumbsDown_3p) -> AttachToActor |
| 130 | AE_Player_Emotes_ThumbsUp | `Audio.Event.Player.Emote.ThumbsUp` | 2 | PerspSound(MSS_Player_Emotes_ThumbsUp_1p, MSS_Player_Emote_ThumbsUp_3p) -> AttachToActor |
| | **Player/Fall** | | | |
| 131 | AE_Player_Fall_Parachute | `Audio.Event.Player.Fall.Parachute` | 2 | AttachToActor -> PerspSound(hostility)(DA_Item_Parachute_Fall; tag:Audio.Asset.Player.Parachute.Fall.1p, Audio.Asset.Player.Parachute.Fall.Ally, Audio.Asset.Player.Parach |
| 132 | AE_Player_Fall_SkyDive | `Audio.Event.Player.Fall.Skydive` | 2 | AttachToActor -> PerspSound(hostility)(DA_Item_Parachute_Skydive; tag:Audio.Asset.Player.Parachute.Skydive.1p, Audio.Asset.Player.Parachute.Skydive.Ally, Audio.Asset.Play |
| 133 | AE_Player_Fall_SkyDive_Enter | `Audio.Event.Player.Fall.Skydive.Enter` | 2 | AttachToActor -> PerspSound(hostility)(DA_Item_Parachute_SkydiveEnter; tag:Audio.Asset.Player.Parachute.SkydiveEnter.1p, Audio.Asset.Player.Parachute.SkydiveEnter.Ally, A |
| 134 | AE_Player_Fall_SkyDive_Stop | `Audio.Event.Player.Fall.Skydive.Stop` | 2 | TriggerParam(str:Stop) -> StopSound |
| | **Player/Item** | | | |
| 135 | AE_HealOther | `Audio.Event.Player.HealOther` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Player.HealOther.1p, Audio.Asset.Player.HealOther.3p) |
| 136 | AE_HealOther_Stop | `Audio.Event.Player.HealOther.Stop` | 1 | TriggerParam(str:Stop) |
| 137 | AE_HealSelf | `Audio.Event.Player.HealSelf` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Player.HealSelf.1p, Audio.Asset.Player.HealSelf.3p) |
| 138 | AE_Item_Deploy | `Audio.Event.Item.Deploy` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.Deploy.1p, Audio.Asset.Item.Deploy.3p) |
| 139 | AE_Item_Deploy_Stop | `Audio.Event.Item.UsePrimary.Stop.Deploy` | 1 | StopSound |
| 140 | AE_Item_Disarm_Complete | `Audio.Event.Item.Disarm.Complete` | 3 | AttachToActor -> PlaySound(MSS_Item_Disarm_Complete) -> XSetExecutionContextAbandonmentSettings |
| 141 | AE_Item_Disarm_Start | `Audio.Event.Item.Disarm.Start` | 2 | AttachToActor -> PlaySound(MSS_Item_Disarm_Start) |
| 142 | AE_Item_Disarm_Stop | `Audio.Event.Item.Disarm.Stop` | 1 | StopSound |
| 143 | AE_Item_UsePrimary | `Audio.Event.Item.UsePrimary` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.UsePrimary.1p, Audio.Asset.Item.UsePrimary.3p) |
| 144 | AE_Item_UsePrimary_Start | `Audio.Event.Item.UsePrimary.Start` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.UsePrimary.Start.1p, Audio.Asset.Item.UsePrimary.Start.3p) -> TriggerParam(str:Trigger) |
| 145 | AE_Item_UsePrimary_Stop | `Audio.Event.Item.UsePrimary.Stop` | 1 | TriggerParam(str:Stop) |
| 146 | AE_Player_Revived | `Audio.Event.Player.Revived` | 2 | PerspSound(MSS_Player_Damage_Death_Revived_1p, MSS_Player_Damage_Death_Revived_3p) -> AttachToActor |
| 147 | AE_Player_Revived_Local | `Audio.Event.Player.Revived.Local` | 2 | DisableMusic(tag:Audio.Music.Revived) -> EnableMusic(tag:Audio.Music.Revived) |
| 148 | AE_Reviving | `Audio.Event.Player.Reviving` | 2 | PerspSound(MSS_Player_Interact_Revive_1p, MSS_Player_Interact_Revive_3p_Preset) -> AttachToActor |
| 149 | AE_Reviving_Stop | `Audio.Event.Player.Reviving.Stop` | 1 | TriggerParam(str:Stop) |
| 150 | AE_Reviving_Success | `Audio.Event.Player.Reviving.Success` | 2 | PerspSound(MSS_Player_Interact_Revive_1p, MSS_Player_Interact_Revive_3p_Preset) -> TriggerParam(str:Success) |
| | **Player/Item/Adrenaline_Pen** | | | |
| 151 | AE_Player_Item_AdrenalinePen_Activate | `Audio.Event.Item.AdrenalinePen.Activate` | 1 | TriggerParam(str:Stop) |
| 152 | AE_Player_Item_AdrenalinePen_Use | `Audio.Event.Item.AdrenalinePen.Use` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Player.HealOther.1p, Audio.Asset.Player.HealOther.3p) |
| | **Player/Item/BuildTool** | | | |
| 153 | AE_BuildTool_Use | `Audio.Event.Player.BuildTool.Use` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Player.BuildTool.BuildToolUse.1p, Audio.Asset.Player.BuildTool.BuildToolUse.3p) |
| | **Player/Item/Drop** | | | |
| 154 | AE_Item_Drop | `Audio.Event.Item.Drop` | 2 | AttachToActor -> PlaySound(MSS_Player_Item_Drop) |
| 155 | AE_Item_Dropped_Bounce | `Audio.Event.Item.Dropped.Bounce` | 2 | PlayItemDrop -> AttachToActor |
| 156 | AE_Item_Dropped_Stop | `Audio.Event.Item.Dropped.Stop` | 0 |  |
| 157 | AE_Item_Pickup | `Audio.Event.Item.Pickup` | 4 | PlayItemPickup -> PerspSound -> AttachToActor -> ... |
| 158 | AE_Player_Item_Pickup | `Audio.Event.Player.Item.Pickup` | 2 | AttachToActor -> PlaySound(MSS_Player_Item_Pickup) |
| | **Player/Item/FuelCan** | | | |
| 159 | AE_Item_UsePrimary_Start_FuelCan | `Audio.Event.Item.UsePrimary.Start.FuelCan` | 3 | AttachToHeldItem -> FuelCannister -> HeldItemPerspSound(tag:Audio.Asset.Item.UsePrimary.1p, Audio.Asset.Item.UsePrimary.3p) |
| 160 | AE_Item_UsePrimary_Stop_FuelCan | `Audio.Event.Item.UsePrimary.Stop.FuelCan` | 1 | TriggerParam(str:Stop) |
| | **Player/Item/IFAK** | | | |
| 161 | AE_Player_Item_IFAK_Activate | `Audio.Event.Item.IFAK.Activation` | 2 | HeldItemPerspSound(tag:Audio.Asset.Player.StimActivation.1p, Audio.Asset.Player.StimActivation.3p) -> AttachToActor |
| | **Player/Item/RangeFinder** | | | |
| 162 | AE_Item_Rangefinder_ZoomDecrease | `Audio.Event.Item.RangeFinder.ZoomOut` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Zoom.Decrease) |
| 163 | AE_Item_Rangefinder_ZoomIncrease | `Audio.Event.Item.RangeFinder.ZoomIn` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Zoom.Increase) |
| | **Player/Item/StimPen** | | | |
| 164 | AE_Player_Item_StimShot_Activate | `Audio.Event.Item.StimShot.Activation` | 2 | HeldItemPerspSound(tag:Audio.Asset.Player.StimActivation.1p, Audio.Asset.Player.StimActivation.3p) -> AttachToActor |
| 165 | AE_Player_Item_StimShot_Stop | `Audio.Event.Item.StimShot.Stop` | 1 | TriggerParam(str:Stop) |
| 166 | AE_Player_Item_StimShot_Use | `Audio.Event.Item.StimShot.Use` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.UsePrimary.1p, Audio.Asset.Item.UsePrimary.3p) |
| | **Player/Item/UniversalTool** | | | |
| 167 | AE_Player_Item_Injection_Use | `Audio.Event.Item.Injection.Use` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Player.HealOther.1p, Audio.Asset.Player.HealOther.3p) -> TriggerParam(str:Start) |
| 168 | AE_Player_Item_Repair_Use | `Audio.Event.Item.Repair.Use` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Player.Repair.1p, Audio.Asset.Player.Repair.3p) -> TriggerParam(str:Start) |
| 169 | AE_Player_Item_UsePrimary_Stop | `Audio.Event.Item.Stop` | 1 | TriggerParam(str:Stop) |
| | **Player/Item/UsePrimary** | | | |
| 170 | AE_Item_UsePrimary_Parachute | `Audio.Event.Item.UsePrimary.Parachute` | 2 | AttachToActor -> PerspSound(hostility)(DA_Item_Parachute_Use; tag:Audio.Asset.Player.Parachute.Deploy.1p, Audio.Asset.Player.Parachute.Deploy.Ally, Audio.Asset.Player.Par |
| | **Player/Movement** | | | |
| 171 | AE_Player_Movement_Drag_Loop_Start | `Audio.Event.Player.Footstep.Drag.Loop` | 2 | AttachToActor -> PerspSound(hostility)(DA_PlayerMovement_Drag_Loop; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player.Footstep.Enem |
| 172 | AE_Player_Movement_Drag_Start | `Audio.Event.Player.Footstep.Drag.Start` | 2 | AttachToActor -> PerspSound(hostility)(DA_PlayerMovement_Drag_Start; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player.Footstep.Ene |
| 173 | AE_Player_Movement_Drag_Stop | `Audio.Event.Player.Footstep.Drag.Stop` | 3 | AttachToActor -> StopSound -> PerspSound(hostility)(DA_PlayerMovement_Drag_Stop; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player. |
| 174 | AE_Player_Movement_Ragdoll_Hard | `Audio.Event.Player.Ragdoll.Hard` | 2 | AttachToActor -> PerspSound(hostility)(DA_PlayerMovement_Ragdoll_Hard; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player.Footstep.E |
| 175 | AE_Player_Movement_Ragdoll_Medium | `Audio.Event.Player.Ragdoll.Medium` | 2 | AttachToActor -> PerspSound(hostility)(DA_PlayerMovement_Ragdoll_Medium; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player.Footstep |
| 176 | AE_Player_Movement_Ragdoll_Soft | `Audio.Event.Player.Ragdoll.Soft` | 2 | AttachToActor -> PerspSound(hostility)(DA_PlayerMovement_Ragdoll_Soft; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player.Footstep.E |
| 177 | AE_Player_Movement_Ragdoll_Start | `Audio.Event.Player.Ragdoll` | 2 | AttachToActor -> PerspSound(hostility)(DA_PlayerMovement_Ragdoll_Soft; tag:Audio.Asset.Player.Footstep.1p, Audio.Asset.Player.Footstep.Ally, Audio.Asset.Player.Footstep.E |
| 178 | AE_Player_Movement_Ragdoll_Stop | `Audio.Event.Player.Ragdoll.Stop` | 1 | StopSound |
| 179 | AE_Player_Vault | `Audio.Event.Player.Vault` | 3 | ModifyCosmeticExertion -> Vaulting(MSS_Player_Movement_Vault_1p, MSS_Player_Movement_Vault_3p_Ally_Preset, MSS_Player_Movement_Vault_3p_Enemy_Pre) -> AttachToActor |
| 180 | AE_Player_Vault_Hand_Impact_Fast | `Audio.Event.Player.Vault.HandImpact.Fast` | 2 | ExecuteTriggerOnPlayerCharacter -> RequestVox(tag:Audio.Vox.Exertion.Vaulting.Fast) |
| 181 | AE_Player_Vault_Hand_Impact_Slow | `Audio.Event.Player.Vault.HandImpact.Slow` | 2 | ExecuteTriggerOnPlayerCharacter -> RequestVox(tag:Audio.Vox.Exertion.Vaulting.Slow) |
| 182 | AE_Player_Vault_Stop | `Audio.Event.Player.Vault.Stop` | 2 | Vaulting_Stop -> TriggerParamOrStop(str:Stop) |
| | **Player/Movement/Foliage** | | | |
| 183 | AE_FoliageMovement | `Audio.Event.Player.Footstep.Foliage` | 3 | AttachToActor -> TriggerParam(str:Start) -> PlaySound(MSS_Player_Movement_Foliage_Sunflowers) |
| 184 | AE_FoliageMovement_Stop | `Audio.Event.Player.Footstep.Foliage.Stop` | 2 | XDetachSound -> TriggerParamOrStop(str:Stop) |
| | **Player/Movement/Footstep** | | | |
| 185 | AE_Footstep_Sprint | `Audio.Event.Player.Footstep.Sprint` | 10 | AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Footstep_Item_1p) -> SetAudioParameters -> ... |
| 186 | AE_Footstep_Stealth | `Audio.Event.Player.Footstep.CrouchWalk` | 10 | AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Footstep_Item_1p) -> SetAudioParameters -> ... |
| 187 | AE_Footstep_TacSprint | `Audio.Event.Player.Footstep.TacSprint` | 10 | AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Footstep_Item_1p) -> SetAudioParameters -> ... |
| 188 | AE_Footstep_Walk | `Audio.Event.Player.Footstep.Walk` | 11 | AttachToHeldItem(str:handguard_Attach) -> ModifyCosmeticExertion_Weight -> PlayItemMovementSound(MSS_Player_Movement_Footstep_Item_1p) -> ... |
| | **Player/Movement/Jump** | | | |
| 189 | AE_Player_Jump | `Audio.Event.Player.Jump.Start` | 5 | ModifyCosmeticExertion -> RequestVox(tag:Audio.Vox.Exertion.Jump) -> AttachToActor -> ... |
| 190 | AE_Player_Land | `Audio.Event.Player.Land` | 5 | PlayLandSound -> SetSoundWaveArrayParameterByHeldItem(tag:Audio.Asset.Item.Footstep.Sprint; str:Item) -> AttachToActor -> ... |
| | **Player/Movement/Ladders** | | | |
| 191 | AE_Ladder_Climbing | `Audio.Event.Player.Ladder.Climbing` | 3 | AttachToActor -> TriggerParam(str:Trigger) -> PerspSound(hostility)(DA_Player_Ladder_Climbing; tag:Audio.Asset.Player.Climb.Ladder.Climbing.1p, Audio.Asset.Player.Climb.L |
| 192 | AE_Ladder_Climbing_Slow | `Audio.Event.Player.Ladder.Climbing.Slow` | 3 | AttachToActor -> TriggerParam(str:Trigger) -> PerspSound(hostility)(DA_Player_Ladder_Climbing_Stealth; tag:Audio.Asset.Player.Climb.Ladder.Climbing.1p, Audio.Asset.Player |
| 193 | AE_Ladder_Dismount | `Audio.Event.Player.Ladder.Dismount` | 2 | AttachToActor -> PerspSound(hostility)(DA_Player_Ladder_Dismount; tag:Audio.Asset.Player.Climb.Ladder.Dismount.1p, Audio.Asset.Player.Climb.Ladder.Dismount.Ally, Audio.As |
| 194 | AE_Ladder_Down | `Audio.Event.Player.Ladder.Down` | 3 | AttachToActor -> TriggerParam(str:Trigger) -> PerspSound(hostility)(DA_Player_Ladder_Down; tag:Audio.Asset.Player.Climb.Ladder.Down.1p, Audio.Asset.Player.Climb.Ladder.Do |
| 195 | AE_Ladder_Mount | `Audio.Event.Player.Ladder.Mount` | 2 | AttachToActor -> PerspSound(hostility)(DA_Player_Ladder_Mount; tag:Audio.Asset.Player.Climb.Ladder.Mount.1p, Audio.Asset.Player.Climb.Ladder.Mount.Ally, Audio.Asset.Playe |
| 196 | AE_Ladder_Slide | `Audio.Event.Player.Ladder.Slide` | 3 | AttachToActor -> TriggerParam(str:Play) -> PerspSound(hostility)(DA_Player_Ladder_Slide; tag:Audio.Asset.Player.Climb.Ladder.Slide.1p, Audio.Asset.Player.Climb.Ladder.Sli |
| 197 | AE_Ladder_SlideStop | `Audio.Event.Player.Ladder.SlideStop` | 1 | TriggerParam(str:Stop) |
| | **Player/Movement/Lean** | | | |
| 198 | AE_Player_Lean | `Audio.Event.Player.Lean` | 2 | PerspSound(MSS_Player_Movement_Lean_1p, MSS_Player_Movement_Lean_3p_Preset) -> AttachToActor |
| 199 | AE_Player_Unlean | `Audio.Event.Player.Unlean` | 2 | PerspSound(MSS_Player_Movement_Unlean_1p, MSS_Player_Movement_Unlean_3p_Preset) -> AttachToActor |
| | **Player/Movement/Parachute** | | | |
| 200 | AE_Player_Cut_Parachute | `Audio.Event.Item.UsePrimary.Parachute.Cut` | 1 | StopSound |
| 201 | AE_Player_Land_Parachute | `Audio.Event.Player.Land.Parachute` | 2 | PerspSound(MSS_Player_Movement_Parachute_Land_1p, MSS_Player_Movement_Parachute_Land_3p_Enemy) -> StopSound |
| | **Player/Movement/Prone** | | | |
| 202 | AE_Prone | `Audio.Event.Player.Prone` | 6 | SetBlendedFootstepSurfaceTrigger(DA_Surface_Footstep_Prone_Audio) -> SetSourceTransformParameters -> StoreFootstepData -> ... |
| | **Player/Movement/Stance** | | | |
| 203 | AE_Player_CrouchToProne | `Audio.Event.Player.Stance.CrouchToProne` | 2 | AttachToActor -> PerspSound(hostility)(DA_Stance_CrouchToProne_Audio; tag:Audio.Asset.Player.Stance.1p, Audio.Asset.Player.Stance.Ally, Audio.Asset.Player.Stance.Enemy) |
| 204 | AE_Player_CrouchToStand | `Audio.Event.Player.Stance.CrouchToStand` | 2 | AttachToActor -> PerspSound(hostility)(DA_Stance_CrouchToStand_Audio; tag:Audio.Asset.Player.Stance.1p, Audio.Asset.Player.Stance.Ally, Audio.Asset.Player.Stance.Enemy) |
| 205 | AE_Player_ProneToCrouch | `Audio.Event.Player.Stance.ProneToCrouch` | 2 | AttachToActor -> PerspSound(hostility)(DA_Stance_ProneToCrouch_Audio; tag:Audio.Asset.Player.Stance.1p, Audio.Asset.Player.Stance.Ally, Audio.Asset.Player.Stance.Enemy) |
| 206 | AE_Player_ProneToStand | `Audio.Event.Player.Stance.ProneToStand` | 3 | AttachToActor -> TriggerParam(str:Stop) -> PerspSound(hostility)(DA_Stance_ProneToStand_Audio; tag:Audio.Asset.Player.Stance.1p, Audio.Asset.Player.Stance.Ally, Audio.Ass |
| 207 | AE_Player_StandToCrouch | `Audio.Event.Player.Stance.StandToCrouch` | 2 | AttachToActor -> PerspSound(hostility)(DA_Stance_StandToCrouch_Audio; tag:Audio.Asset.Player.Stance.1p, Audio.Asset.Player.Stance.Ally, Audio.Asset.Player.Stance.Enemy) |
| 208 | AE_Player_StandToProne | `Audio.Event.Player.Stance.StandToProne` | 3 | AttachToActor -> TriggerParam(str:Stop) -> PerspSound(hostility)(DA_Stance_StandToProne_Audio; tag:Audio.Asset.Player.Stance.1p, Audio.Asset.Player.Stance.Ally, Audio.Ass |
| | **Player/Movement/State** | | | |
| 209 | AE_Player_State_Sprint | `Audio.Event.Player.Sprint` | 10 | AddCosmeticExertionSource -> AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Item_Transition_1p) -> ... |
| 210 | AE_Player_State_SprintStop | `Audio.Event.Player.Sprint.Stop` | 9 | AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Item_Transition_1p) -> RemoveCosmeticExertionSource -> ... |
| 211 | AE_Player_State_TacSprint | `Audio.Event.Player.Sprint.Tactical` | 10 | AddCosmeticExertionSource -> AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Item_Transition_1p) -> ... |
| 212 | AE_Player_State_TacSprint_Stop | `Audio.Event.Player.Sprint.Tactical.Stop` | 9 | AttachToHeldItem(str:handguard_Attach) -> PlayItemMovementSound(MSS_Player_Movement_Item_Transition_1p) -> RemoveCosmeticExertionSource -> ... |
| | **Player/Movement/Swimming** | | | |
| 213 | AE_Swimming_LandHeavy | `Audio.Event.Player.Swimming.LandHeavy` | 2 | AttachToActor -> PerspSound(hostility)(DA_Player_Swim_LandHeavy; tag:Audio.Asset.Player.Swim.LandHeavy.1p, Audio.Asset.Player.Swim.LandHeavy.Ally, Audio.Asset.Player.Swim |
| 214 | AE_Swimming_LandLight | `Audio.Event.Player.Swimming.LandLight` | 2 | AttachToActor -> PerspSound(hostility)(DA_Player_Swim_LandLight; tag:Audio.Asset.Player.Swim.LandLight.1p, Audio.Asset.Player.Swim.LandLight.Ally, Audio.Asset.Player.Swim |
| 215 | AE_Swimming_Splash | `Audio.Event.Player.Swimming.Splash` | 1 | TriggerParam(str:Splash) |
| 216 | AE_Swimming_Start | `Audio.Event.Player.Swimming.Start` | 3 | SetSourceTransformParameters -> AttachToActor -> PerspSound(hostility)(DA_Player_Swim_SwimStart; tag:Audio.Asset.Player.Swim.SwimStart.1p, Audio.Asset.Player.Swim.SwimSta |
| 217 | AE_Swimming_Stop | `Audio.Event.Player.Swimming.Stop` | 4 | EndBehavior -> EndBehavior -> TriggerParam(str:Stop) -> ... |
| | **Player/State** | | | |
| 218 | AE_Player_State_Alive | `Audio.Event.Player.State.Alive` | 8 | ActivateCBM(AM_CBM_Main) -> DeactivateCBM(AM_CBM_EndGame) -> HandlePhysicalExertionVox -> ... |
| 219 | AE_Player_State_Alive_Local | `Audio.Event.Player.State.Alive.Local` | 1 | DeactivateCBM(AM_CBM_GiveUp) |
| 220 | AE_Player_State_BackBlast | `Audio.Event.Player.State.BackBlast` | 1 | SetTinnitusMix |
| 221 | AE_Player_State_BeingRevived | `Audio.Event.Player.State.BeingRevived` | 1 | SetReviveParametersToActiveMusicState |
| 222 | AE_Player_State_BeingRevived_Stop | `Audio.Event.Player.State.BeingRevived.Stop` | 1 | SendActiveMusicFloatParameter |
| 223 | AE_Player_State_Critical_Start | `Audio.Event.Player.State.Critical` | 10 | ActivateCBM(AM_CBM_Critical) -> ClearVoxQueue -> DeactivateCBM(AM_CBM_Main) -> ... |
| 224 | AE_Player_State_Critical_Stop | `Audio.Event.Player.State.Critical.Stop` | 8 | ActivateCBM(AM_CBM_Main) -> DeactivateCBM(AM_CBM_Critical) -> EndBehavior -> ... |
| 225 | AE_Player_State_LowHealth_Start | `Audio.Event.Player.State.LowHealth` | 2 | RequestVoxRepeat(tag:Audio.Vox.Exertion.TakingDamage.GoingLowHealth) -> AttachToActor |
| 226 | AE_Player_State_LowHealth_Stop | `Audio.Event.Player.State.LowHealth.Stop` | 1 | EndBehavior |
| 227 | AE_Player_State_SafeZone_Enter | `Audio.Event.Player.State.SafeZone.Enter` | 1 | ActivateCBM(AM_CBM_SafeZone) |
| 228 | AE_Player_State_SafeZone_Exit | `Audio.Event.Player.State.SafeZone.Exit` | 1 | DeactivateCBM(AM_CBM_SafeZone) |
| 229 | AE_Player_State_Tinnitus | `Audio.Event.Player.State.Tinnitus` | 1 | SetTinnitusMix |
| | **Prop** | | | |
| 230 | AE_Prop_MovingTarget_Impact | `Audio.Event.Prop.MovingTarget.Impact` | 2 | PlayTargetImpactSound -> AttachToActor |
| 231 | AE_Prop_MovingTarget_PopUp | `Audio.Event.Prop.MovingTarget.PopUp` | 2 | PlayTargetPopUpSound -> AttachToActor |
| | **Prop/PropDemolition** | | | |
| 232 | AE_PropDemolition_Bush | `Audio.Event.Prop.Demolition.Bush` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Bush_Preset) |
| 233 | AE_PropDemolition_Fence_Concrete | `Audio.Event.Prop.Demolition.FenceConcrete` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Fence_Concrete_Preset) |
| 234 | AE_PropDemolition_Fence_Metal_Chainlink | `Audio.Event.Prop.Demolition.FenceMetalChainlink` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Fence_Metal_Chainlink_Preset) |
| 235 | AE_PropDemolition_Fence_Metal_Sheet | `Audio.Event.Prop.Demolition.FenceMetalSheet` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Fence_Metal_Sheet_Preset) |
| 236 | AE_PropDemolition_Fence_Wood | `Audio.Event.Prop.Demolition.FenceWood` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Fence_Wood_Preset) |
| 237 | AE_PropDemolition_Sign | `Audio.Event.Prop.Demolition.Sign` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Sign_Preset) |
| 238 | AE_PropDemolition_Tree | `Audio.Event.Prop.Demolition.Tree` | 1 | HandlePropDemolitionSound(MSS_PropDemolition_Tree_Preset) |
| | **UI/EndGame** | | | |
| 239 | AE_UI_EndGame_CashNotify_CashEarned | `Audio.Event.UI.EndGame.CashNotify.CashEarned` | 1 | PlaySound(MSS_UI_EndGame_CashRecap_CashEarned_Preset) |
| 240 | AE_UI_EndGame_CashNotify_CashSpent | `Audio.Event.UI.EndGame.CashNotify.CashSpent` | 1 | PlaySound(MSS_UI_EndGame_CashRecap_CashSpent_Preset) |
| 241 | AE_UI_EndGame_CashNotify_FactionScored | `Audio.Event.UI.EndGame.CashNotify.FactionScored` | 1 | PlaySound(MSS_UI_EndGame_CashRecap_Bonus_Preset) |
| 242 | AE_UI_EndGame_CashNotify_PurchaseRefunded | `Audio.Event.UI.EndGame.CashNotify.PurchaseRefunded` | 1 | PlaySound(MSS_UI_EndGame_CashRecap_PurchaseRefund_Preset) |
| 243 | AE_UI_EndGame_CashNotify_TotalProfit | `Audio.Event.UI.EndGame.CashNotify.TotalProfit` | 1 | PlaySound(MSS_UI_EndGame_CashRecap_TotalProfit_Preset) |
| 244 | AE_UI_EndGame_FactionScore_End | `Audio.Event.UI.EndGame.FactionScore.Stop` | 1 | StopSound |
| 245 | AE_UI_EndGame_FactionScore_Start | `Audio.Event.UI.EndGame.FactionScore.Start` | 1 | PlaySound(MSS_UI_EndGame_Score_Bar_Loop) |
| 246 | AE_UI_EndGame_TeamWin | `Audio.Event.UI.EndGame.TeamWin` | 3 | ActivateCBM(AM_CBM_EndGame) -> Submix_DeactivateEffect(SBMIX_Vehicles, SBMIX_EnemyFootsteps, SBMIX_Player, SBMIX_Ambience, SBMIX_Weapons, SBMIX_VOIP, SBMIX_Dialogue_) ->  |
| | **UI/FrontEnd** | | | |
| 247 | AE_TutorialVideo | `Audio.Event.UI.FrontEnd.TutorialVideo` | 1 | PlayTutorialVideoSound |
| 248 | AE_UI_FrontEnd_BackgroundMovie_Start | `Audio.Event.UI.FrontEnd.BackgroundMovie.Start` | 1 | PlaySound(MSS_UI_FrontEnd_BackgroundMovie) |
| 249 | AE_UI_FrontEnd_BackgroundMovie_Stop | `Audio.Event.UI.FrontEnd.BackgroundMovie.Stop` | 1 | StopSound |
| 250 | AE_UI_FrontEnd_ChangeTab | `Audio.Event.UI.FrontEnd.ChangeTab` | 1 | PlaySound(MSS_UI_FrontEnd_ChangeTab) |
| 251 | AE_UI_FrontEnd_Enter_BlackMarket | `Audio.Event.UI.FrontEnd.Open.BlackMarket` | 1 | ActivateCBM(AM_CBM_UIScene) |
| 252 | AE_UI_FrontEnd_Enter_Collection | `Audio.Event.UI.FrontEnd.Open.Collection` | 3 | ActivateCBM(AM_CBM_UIScene) -> DeactivateCBM(AM_CBM_FrontEnd_MainMenu) -> PlaySound(MSS_UI_FrontEnd_Enter_Collection) |
| 253 | AE_UI_FrontEnd_Enter_ConfirmationPopUp | `Audio.Event.UI.FrontEnd.Open.ConfirmationPopUp` | 2 | ActivateCBM(AM_CBM_UIScene_PopUpWindow) -> PlaySound(MSS_UI_FrontEnd_OpenConfirmationPopUp) |
| 254 | AE_UI_FrontEnd_Enter_ContextDrawer | `Audio.Event.UI.FrontEnd.Open.ContextDrawer` | 2 | ActivateCBM(AM_CBM_UIScene_ContextDrawer) -> PlaySound(MSS_UI_FrontEnd_Enter_ContextDrawer) |
| 255 | AE_UI_FrontEnd_Enter_Customize | `Audio.Event.UI.FrontEnd.Open.Customize` | 1 | ActivateCBM(AM_CBM_UIScene) |
| 256 | AE_UI_FrontEnd_Enter_GoldMarket | `Audio.Event.UI.FrontEnd.Open.ServerBrowser` | 3 | ActivateCBM(AM_CBM_UIScene) -> DeactivateCBM(AM_CBM_FrontEnd_MainMenu) -> PlaySound(MSS_UI_FrontEnd_OpenServerBrowser) |
| 257 | AE_UI_FrontEnd_Enter_IntroScene | `Audio.Event.UI.FrontEnd.IntroScene.Enter` | 2 | PlaySound(UI_RevealTrailer_Audio) -> DisableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| 258 | AE_UI_FrontEnd_Enter_LearnToPlay | `Audio.Event.UI.FrontEnd.LearnToPlay.Enter` | 2 | ActivateCBM(AM_CBM_TutorialVideo) -> PlaySound(MSS_UI_FrontEnd_OpenSubMenu) |
| 259 | AE_UI_FrontEnd_Enter_LogoScene | `Audio.Event.UI.FrontEnd.LogoScene.Enter` | 1 | PlaySound(SFX_UI_FrontEnd_BootScreenVideo) |
| 260 | AE_UI_FrontEnd_Enter_MainMenu | `Audio.Event.UI.FrontEnd.Open.MainMenu` | 3 | ActivateCBM(AM_CBM_FrontEnd_MainMenu) -> DeactivateCBM(AM_CBM_TutorialVideo) -> DeactivateCBM(AM_CBM_UIScene) |
| 261 | AE_UI_FrontEnd_Enter_Photosensitivity | `Audio.Event.UI.FrontEnd.Photosensitivity.Enter` | 1 | DisableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| 262 | AE_UI_FrontEnd_Enter_ServerBrowser | `Audio.Event.UI.FrontEnd.Open.GoldMarket` | 3 | ActivateCBM(AM_CBM_UIScene) -> DeactivateCBM(AM_CBM_FrontEnd_MainMenu) -> PlaySound(MSS_UI_FrontEnd_Enter_GoldMarket) |
| 263 | AE_UI_FrontEnd_Enter_SubMenu | `Audio.Event.UI.FrontEnd.Open.SubMenu` | 2 | ActivateCBM(AM_CBM_UIScene) -> DeactivateCBM(AM_CBM_FrontEnd_MainMenu) |
| 264 | AE_UI_FrontEnd_Enter_Vault | `Audio.Event.UI.FrontEnd.Open.Vault` | 1 | ActivateCBM(AM_CBM_UIScene) |
| 265 | AE_UI_FrontEnd_Exit_ConfirmationPopUp | `Audio.Event.UI.FrontEnd.Close.ConfirmationPopUp` | 1 | DeactivateCBM(AM_CBM_UIScene_PopUpWindow) |
| 266 | AE_UI_FrontEnd_Exit_ContextDrawer | `Audio.Event.UI.FrontEnd.Close.ContextDrawer` | 2 | DeactivateCBM(AM_CBM_UIScene_ContextDrawer) -> PlaySound(MSS_UI_FrontEnd_Exit_ContextDrawer) |
| 267 | AE_UI_FrontEnd_Exit_IntroScene | `Audio.Event.UI.FrontEnd.IntroScene.Exit` | 2 | StopSound -> EnableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| 268 | AE_UI_FrontEnd_Exit_LearnToPlay | `Audio.Event.UI.FrontEnd.LearnToPlay.Exit` | 2 | DeactivateCBM(AM_CBM_TutorialVideo) -> PlaySound(MSS_UI_FrontEnd_General_Select) |
| 269 | AE_UI_FrontEnd_Exit_LogoScene | `Audio.Event.UI.FrontEnd.LogoScene.Exit` | 1 | StopSound |
| 270 | AE_UI_FrontEnd_Exit_MainMenu | `Audio.Event.UI.FrontEnd.Close.MainMenu` | 1 | DeactivateCBM(AM_CBM_FrontEnd_MainMenu) |
| 271 | AE_UI_FrontEnd_Exit_Photosensitivity | `Audio.Event.UI.FrontEnd.Photosensitivity.Exit` | 1 | EnableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| 272 | AE_UI_FrontEnd_Exit_ServerBrowser | `Audio.Event.UI.FrontEnd.Close.ServerBrowser` | 1 | DeactivateCBM(AM_CBM_UIScene) |
| 273 | AE_UI_FrontEnd_Exit_SubMenu | `Audio.Event.UI.FrontEnd.Close.SubMenu` | 2 | DeactivateCBM(AM_CBM_UIScene) -> PlaySound(MSS_UI_FrontEnd_General_Select) |
| 274 | AE_UI_FrontEnd_GoldExchange_Fail | `Audio.Event.UI.FrontEnd.GoldExchange.Fail` | 1 | PlaySound(MSS_UI_FrontEnd_InsufficientFunds) |
| 275 | AE_UI_FrontEnd_GoldExchange_Success | `Audio.Event.UI.FrontEnd.GoldExchange.Success` | 1 | PlaySound(MSS_UI_FrontEnd_PurchaseGoldBar) |
| 276 | AE_UI_FrontEnd_Hover | `Audio.Event.UI.FrontEnd.Hover` | 1 | PlaySound(MSS_UI_FrontEnd_General_Hover) |
| 277 | AE_UI_FrontEnd_JoinServer | `Audio.Event.UI.FrontEnd.JoinServer` | 2 | DeactivateCBM(AM_CBM_UIScene) -> PlaySound(MSS_UI_FrontEnd_JoinServer) |
| 278 | AE_UI_FrontEnd_MainMenuStart | `Audio.Event.UI.FrontEnd.MainMenuStart` | 1 | PlaySound(MSS_UI_FrontEnd_OpenMainMenu) |
| 279 | AE_UI_FrontEnd_Meta_Mock_Collect | `Audio.Event.UI.FrontEnd.Meta.Mock.Collect` | 1 | PlayInventoryItemUISound |
| 280 | AE_UI_FrontEnd_Meta_Mock_TimerStart | `Audio.Event.UI.FrontEnd.Meta.Mock.TimerStart` | 1 | PlaySound(MSS_UI_Meta_MockTimerStart) |
| 281 | AE_UI_FrontEnd_PurchaseCosmetic_Fail | `Audio.Event.UI.FrontEnd.PurchaseCosmetic.Fail` | 1 | PlaySound(MSS_UI_FrontEnd_InsufficientFunds) |
| 282 | AE_UI_FrontEnd_PurchaseCosmetic_Success | `Audio.Event.UI.FrontEnd.PurchaseCosmetic.Success` | 1 | PlaySound(MSS_UI_FrontEnd_PurchaseCosmetic) |
| 283 | AE_UI_FrontEnd_Select | `Audio.Event.UI.FrontEnd.Select` | 1 | PlaySound(MSS_UI_FrontEnd_General_Select) |
| 284 | AE_UI_FrontEnd_Slider | `Audio.Event.UI.FrontEnd.Slider` | 2 | TriggerParam(str:Play) -> PlaySound(MSS_UI_Slider) |
| 285 | AE_UI_FrontEnd_Vault_Sort | `Audio.Event.UI.FrontEnd.Vault.Sort` | 1 | PlaySound(MSS_UI_FrontEnd_Vault_Sort) |
| | **UI/InGame** | | | |
| 286 | AE_UI_InGame_DeploymentBoard_Close | `Audio.Event.UI.InGame.DeploymentBoard.Close` | 1 | PlaySound(MSS_UI_DeploymentBoard_Close) |
| 287 | AE_UI_InGame_DeploymentBoard_Open | `Audio.Event.UI.InGame.DeploymentBoard.Open` | 1 | PlaySound(MSS_UI_DeploymentBoard_Open) |
| 288 | AE_UI_InGame_LevelledUp | `Audio.Event.UI.InGame.LevelledUp` | 1 | PlaySound(MSS_UX_Meta_LevelUp) |
| 289 | AE_UI_InGame_Minimap_Close | `Audio.Event.UI.InGame.Minimap.Close` | 1 | PlaySound(MSS_UI_MiniMap_Close) |
| 290 | AE_UI_InGame_Minimap_Open | `Audio.Event.UI.InGame.Minimap.Open` | 1 | PlaySound(MSS_UI_Minimap_Open) |
| 291 | AE_UI_InGame_Purchasing_Close | `Audio.Event.UI.InGame.Purchasing.Close` | 2 | StopLocalPlayerSoundByContext -> PlaySound(MSS_UI_Vendor_Vehicle_Close) |
| 292 | AE_UI_InGame_Purchasing_Open | `Audio.Event.UI.InGame.Purchasing.Open` | 1 | PlaySound(MSS_UI_Vendor_Vehicle_Open) |
| 293 | AE_UI_InGame_Vendor_DeleteItem | `Audio.Event.UI.Vendor.DeleteItem` | 2 | StopLocalPlayerSoundByContext -> PlaySound(MSS_UI_Vendor_DeleteItem) |
| 294 | AE_UI_InGame_Vendor_Equipment_Close | `Audio.Event.UI.InGame.Vendor.Equipment.Close` | 2 | DeactivateCBM(AM_CBM_UIScene_Vendor) -> PlaySound(MSS_UI_Vendor_Equipment_Close) |
| 295 | AE_UI_InGame_Vendor_Equipment_Open | `Audio.Event.UI.InGame.Vendor.Equipment.Open` | 2 | ActivateCBM(AM_CBM_UIScene_Vendor) -> PlaySound(MSS_UI_Vendor_Equipment_Open) |
| 296 | AE_UI_InGame_Vendor_Garage_Close | `Audio.Event.UI.InGame.Vendor.Garage.Close` | 2 | DeactivateCBM(AM_CBM_UIScene_Vendor_Garage) -> PlaySound(MSS_UI_Vendor_Vehicle_Close) |
| 297 | AE_UI_InGame_Vendor_Garage_Open | `Audio.Event.UI.InGame.Vendor.Garage.Open` | 2 | ActivateCBM(AM_CBM_UIScene_Vendor_Garage) -> PlaySound(MSS_UI_Vendor_Vehicle_Open) |
| 298 | AE_UI_InGame_Vendor_InsufficientFunds | `Audio.Event.UI.Vendor.InsufficientFunds` | 1 | PlaySound(MSS_UI_InGame_Vendor_InsufficientFunds) |
| 299 | AE_UI_InGame_Vendor_Purchase | `Audio.Event.UI.InGame.Vendor.Purchase` | 2 | PlayContextualPurchaseSound -> PlaySound(MSS_UI_InGame_Vendor_PurchaseCart) |
| 300 | AE_UI_InGame_Vendor_PurchaseCart | `Audio.Event.UI.Vendor.PurchaseCart` | 1 | PlaySound(MSS_UI_InGame_Vendor_PurchaseCart) |
| 301 | AE_UI_InGame_Vendor_RemoveItemFromCart | `Audio.Event.UI.Vendor.RemoveItemFromCart` | 1 | PlaySound(MSS_UI_InGame_Vendor_RemoveItemFromCart) |
| 302 | AE_UI_InGame_Vendor_Unlock | `Audio.Event.UI.Vendor.Unlock` | 3 | PlayItemUnlockVendorBark -> AttachToActor -> PlaySound(MSS_UI_Meta_Unlock_Success) |
| 303 | AE_UI_InGame_Vendor_Unlock_Fail | `Audio.Event.UI.Vendor.Unlock.Fail` | 1 | PlaySound(MSS_UI_InGame_Vendor_InsufficientFunds) |
| 304 | AE_UI_InGame_Vendor_Vehicle_Close | `Audio.Event.UI.InGame.Vendor.Vehicle.Close` | 2 | DeactivateCBM(AM_CBM_UIScene_Vendor) -> PlaySound(MSS_UI_Vendor_Vehicle_Close) |
| 305 | AE_UI_InGame_Vendor_Vehicle_Open | `Audio.Event.UI.InGame.Vendor.Vehicle.Open` | 2 | ActivateCBM(AM_CBM_UIScene_Vendor) -> PlaySound(MSS_UI_Vendor_Vehicle_Open) |
| | **UI/InGame/TankReloadMinigame** | | | |
| 306 | AE_UI_InGame_TankReloadMiniGame_CompleteWithoutError | `Audio.Event.UI.InGame.ReloadingMinigame.CompleteWithoutError` | 2 | TriggerParam(str:CompleteWithoutError) -> PlaySound(MSS_UI_InGame_TankReloadMinigame) |
| 307 | AE_UI_InGame_TankReloadMiniGame_CorrectKeyPress | `Audio.Event.UI.InGame.ReloadingMinigame.CorrectKey` | 3 | SetReloadingMinigameSegment -> TriggerParam(str:Keypress) -> PlaySound(MSS_UI_InGame_TankReloadMinigame) |
| 308 | AE_UI_InGame_TankReloadMiniGame_FinalQuadrantSuccess | `Audio.Event.UI.InGame.ReloadingMinigame.FinalQuadrant` | 2 | TriggerParam(str:FinalQuadrantSuccess) -> PlaySound(MSS_UI_InGame_TankReloadMinigame) |
| 309 | AE_UI_InGame_TankReloadMiniGame_IncorrectKeyPress | `Audio.Event.UI.InGame.ReloadingMinigame.IncorrectKey` | 2 | TriggerParam(str:IncorrectKeyPress) -> PlaySound(MSS_UI_InGame_TankReloadMinigame) |
| 310 | AE_UI_InGame_TankReloadMiniGame_SuccessfulQuadrant | `Audio.Event.UI.InGame.ReloadingMinigame.SuccessfulQuadrant` | 3 | SetReloadingMinigameSegment -> TriggerParam(str:SuccessfulQuadrant) -> PlaySound(MSS_UI_InGame_TankReloadMinigame) |
| | **UI/Inventory** | | | |
| 311 | AE_UI_Inventory_Attach_Suppressor | `Audio.Event.UI.Inventory.Attach.Suppressor` | 1 | PlaySound(MSS_UI_InGame_Inventory_Attach_Suppressor) |
| 312 | AE_UI_Inventory_CombineMags | `Audio.Event.UI.Inventory.CombineMags` | 3 | MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_CombineMags) -> StopSound |
| 313 | AE_UI_Inventory_CombineMags_Start | `Audio.Event.UI.Inventory.CombineMags.Start` | 2 | MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_CombineMags_Start) |
| 314 | AE_UI_Inventory_CombineMags_Stop | `Audio.Event.UI.Inventory.CombineMags.Stop` | 1 | StopSound |
| 315 | AE_UI_Inventory_Detach_Suppressor | `Audio.Event.UI.Inventory.Detach.Suppressor` | 1 | PlaySound(MSS_UI_InGame_Inventory_Detach_Suppressor) |
| 316 | AE_UI_Inventory_ExtractAmmo | `Audio.Event.UI.Inventory.ExtractAmmo` | 3 | MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_ExtractAmmo) -> StopSound |
| 317 | AE_UI_Inventory_ExtractAmmo_Start | `Audio.Event.UI.Inventory.ExtractAmmo.Start` | 2 | MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_ExtractAmmo_Start) |
| 318 | AE_UI_Inventory_ExtractAmmo_Stop | `Audio.Event.UI.Inventory.ExtractAmmo.Stop` | 1 | StopSound |
| 319 | AE_UI_Inventory_Interaction | `Audio.Event.UI.Inventory.ItemInteraction` | 2 | MoveUISoundToCharacter -> PlayInventoryItemUISound(MSS_UI_InGame_Inventory_Hover) |
| 320 | AE_UI_Inventory_Rotate | `Audio.Event.UI.Inventory.Rotate` | 1 | PlaySound(MSS_UI_InGame_Inventory_Rotate) |
| 321 | AE_UI_Inventory_SceneEnter | `Audio.Event.UI.Inventory.SceneEnter` | 3 | ActivateCBM(AM_CBM_UIScene) -> MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_Open) |
| 322 | AE_UI_Inventory_SceneExit | `Audio.Event.UI.Inventory.SceneExit` | 3 | DeactivateCBM(AM_CBM_UIScene) -> MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_Close) |
| | **UI/Request** | | | |
| 323 | AE_UI_Request_Ammo | `Audio.Event.UI.Request.Ammo` | 1 | PerspSound(MSS_UI_InGame_Request_Ammo_1p) |
| 324 | AE_UI_Request_Healing | `Audio.Event.UI.Request.Healing` | 1 | PerspSound(MSS_UI_InGame_Request_Healing_1p) |
| 325 | AE_UI_Request_Pickup | `Audio.Event.UI.Request.Pickup` | 1 | PerspSound(MSS_UI_InGame_Request_Pickup_1p) |
| 326 | AE_UI_Request_SceneEnter | `Audio.Event.UI.Request.SceneEnter` | 1 | PlaySound(MSS_UI_InGame_Request_SceneEnter) |
| 327 | AE_UI_Request_SceneExit | `Audio.Event.UI.Request.SceneExit` | 1 | PlaySound(MSS_UI_InGame_Request_SceneExit) |
| | **UI/Scoreboard** | | | |
| 328 | AE_UI_Scoreboard_SceneEnter | `Audio.Event.UI.Scoreboard.Enter` | 3 | ActivateCBM(AM_CBM_UIScene_Scoreboard) -> MoveUISoundToCharacter -> PlaySound(MSS_UI_InGame_Inventory_Open) |
| 329 | AE_UI_Scoreboard_SceneExit | `Audio.Event.UI.Scoreboard.Exit` | 4 | DeactivateCBM(AM_CBM_UIScene_Scoreboard) -> DeactivateCBM(AM_CBM_UIScene) -> MoveUISoundToCharacter -> ... |
| | **UI/XPProgression** | | | |
| 330 | AE_UI_XPProgression_LevelledUp | `Audio.Event.UI.XPProgression.LevelledUp` | 1 | XPProgression_PlayRoleLevelUp(MSS_UI_EndGame_XP_LevelUp_Infantry_Preset, MSS_UI_EndGame_XP_LevelUp_Medic_Preset, MSS_UI_EndGame_XP_LevelUp_R) |
| 331 | AE_UI_XPProgression_RevealRoleProgression | `Audio.Event.UI.XPProgression.RevealRoleProgression` | 1 | PlaySound(MSS_UI_EndGame_XP_RoleCard) |
| 332 | AE_UI_XPProgression_SkipReveal | `Audio.Event.UI.XPProgression.SkipReveal` | 1 | StopSound |
| 333 | AE_UI_XPProgression_StartFillingProgress | `Audio.Event.UI.XPProgression.StartFillingProgress` | 2 | XPProgression_SetXPBarTime -> PlaySound(MSS_UI_EndGame_XP_Bar) |
| | **UX/Cash** | | | |
| 334 | AE_UX_Cash_Bribe | `Audio.Event.UX.Cash.Bribe` | 1 | PlaySound(MSS_UX_Cash_Bribe) |
| 335 | AE_UX_Cash_BuiltScore | `Audio.Event.UX.Cash.BuiltScore` | 1 | PlaySound(MSS_UX_Cash_Small_01) |
| 336 | AE_UX_Cash_DeliveredPassenger | `Audio.Event.UX.Cash.DeliveredPassenger` | 1 | PlaySound(MSS_UX_Cash_PassengerDelivered) |
| 337 | AE_UX_Cash_DeliveredSpawnVehicle | `Audio.Event.UX.Cash.DeliveredSpawnVehicle` | 1 | PlaySound(MSS_UX_Cash_Large_01) |
| 338 | AE_UX_Cash_DestroyedVehicle | `Audio.Event.UX.Cash.DestroyedVehicle` | 1 | PlaySound(MSS_UX_Cash_DestroyedVehicle) |
| 339 | AE_UX_Cash_HealedScore | `Audio.Event.UX.Cash.HealedScore` | 1 | PlaySound(MSS_UX_Cash_HealedScore) |
| 340 | AE_UX_Cash_Hotzone_Reward | `Audio.Event.UX.Cash.HotzoneReward` | 1 | PlaySound(MSS_UX_Cash_Hotzone_Reward) |
| 341 | AE_UX_Cash_Pallet_Deposit | `Audio.Event.UX.Cash.PalletDeposit` | 1 | PlaySound(MSS_UX_Cash_Hotzone_Reward) |
| 342 | AE_UX_Cash_PassengerSurvived | `Audio.Event.UX.Cash.PassengerSurvived` | 1 | PlaySound(MSS_UX_Cash_PassengerSurvived) |
| 343 | AE_UX_Cash_PurchaseSupplies | `Audio.Event.UX.Cash.PurchaseSupplies` | 1 | PlaySound(MSS_UX_Cash_PurchaseSupply) |
| 344 | AE_UX_Cash_RepairingScore | `Audio.Event.UX.Cash.RepairingScore` | 1 | PlaySound(MSS_UX_Cash_RepairingScore) |
| 345 | AE_UX_Cash_RevivedScore | `Audio.Event.UX.Cash.RevivedScore` | 1 | PlaySound(MSS_UX_Cash_RevivedScore) |
| 346 | AE_UX_Cash_SpawnPassenger | `Audio.Event.UX.Cash.SpawnPassenger` | 1 | PlaySound(MSS_UX_Cash_SpawnPassenger) |
| 347 | AE_UX_Cash_SupplyDestroyOnImpact | `Audio.Event.UX.Cash.SupplyDestroyOnImpact` | 1 | PlaySound(MSS_UX_Cash_SupplyDestroyOnImpact) |
| 348 | AE_UX_Cash_TeammateKill | `Audio.Event.UX.Cash.TeammateKill` | 1 | PlaySound(MSS_UX_Combat_Notify_TeammateKill) |
| 349 | AE_UX_Cash_Tip | `Audio.Event.UX.Cash.Tip` | 1 | PlaySound(MSS_UX_Cash_Tip) |
| | **UX/Cash/Assists** | | | |
| 350 | AE_UX_Cash_Assist_BuiltScore_Enemy | `Audio.Event.UX.Cash.Assist.BuiltScore.Enemy` | 1 | PlaySound(MSS_UX_Cash_Assist) |
| 351 | AE_UX_Cash_Assist_BuiltScore_Teammate | `Audio.Event.UX.Cash.Assist.BuiltScore.Teammate` | 1 | PlaySound(MSS_UX_Cash_Assist) |
| 352 | AE_UX_Cash_Assist_Crew | `Audio.Event.UX.Cash.Assist.Crew` | 1 | PlaySound(MSS_UX_Cash_Assist) |
| 353 | AE_UX_Cash_Assist_Spotting | `Audio.Event.UX.Cash.Assist.Spotting` | 1 | PlaySound |
| 354 | AE_UX_Cash_Assist_Transport | `Audio.Event.UX.Cash.Assist.Transport` | 1 | PlaySound(MSS_UX_Cash_Assist) |
| | **UX/Combat** | | | |
| 355 | AE_UX_Combat_HeadshotKill | `Audio.Event.UX.Combat.HeadshotKill` | 2 | SetEnemyKilledDistance -> PlaySound(MSS_UX_Combat_Notify_HeadshotKill) |
| 356 | AE_UX_Combat_HighValueKill | `Audio.Event.UX.Combat.HighValueKill` | 1 | SetBool(str:IsHighValue) |
| 357 | AE_UX_Combat_Hitmarker | `Audio.Event.UX.Combat.Hitmarker` | 2 | PlayHitConfirmSound(MSS_UX_Combat_Hitmarker_Flesh, MSS_UX_Combat_Hitmarker_Armor, MSS_UX_Combat_Hitmarker_Armor_Helmet, MSS_UX_Com) -> TriggerParam(str:Trigger) |
| 358 | AE_UX_Combat_Hitmarker_Vehicle | `Audio.Event.UX.Combat.Hitmarker.Vehicle` | 3 | PlayVehicleHitSound -> TriggerParam(str:Trigger) -> WDMoveSoundToGameplayCueLocation |
| 359 | AE_UX_Combat_Kill | `Audio.Event.UX.Combat.Kill` | 1 | EnemyKilledParameters(MSS_UX_Combat_Notify_KillConfirmed) |
| 360 | AE_UX_Combat_KillAssist | `Audio.Event.UX.Combat.KillAssist` | 1 | PlaySound(MSS_UX_Spotting_SpottedTargetDestroyAssist) |
| | **UX/Healing** | | | |
| 361 | AE_UX_Heal_Notify_End | `Audio.Event.UX.Healing.NotifyEnd` | 1 | PlayHealingSound(MSS_UX_Healing_Notify_End) |
| 362 | AE_UX_Heal_Notify_Start | `Audio.Event.UX.Healing.NotifyStart` | 1 | PlayHealingSound(MSS_UX_Healing_Notify_Start) |
| | **UX/Spotted** | | | |
| 363 | AE_UX_Spotted_SpottedConfirmation | `Audio.Event.UX.Spotted.SpottedConfirmation` | 1 | PlaySound(MSS_UX_Spotting_SpottedConfirmation) |
| 364 | AE_UX_Spotted_SpottedDestroy_BuildableDestroyed | `Audio.Event.UX.Spotted.DestroyAssist.Buildable` | 3 | ActivateCBM(AM_CBM_NarratorActive) -> DeactivateCBM(AM_CBM_NarratorActive) -> RequestLocalVox(tag:Audio.Vox.Bark.Spotting.Destroy.Buildable) |
| 365 | AE_UX_Spotted_SpottedDestroy_DeployableDestroyed | `Audio.Event.UX.Spotted.DestroyAssist.Deployable` | 3 | ActivateCBM(AM_CBM_NarratorActive) -> DeactivateCBM(AM_CBM_NarratorActive) -> RequestLocalVox(tag:Audio.Vox.Bark.Spotting.Destroy.Deployable) |
| 366 | AE_UX_Spotted_SpottedDestroy_EnemyKilled | `Audio.Event.UX.Spotted.DestroyAssist.Player` | 4 | ActivateCBM(AM_CBM_NarratorActive) -> DeactivateCBM(AM_CBM_NarratorActive) -> RequestLocalVox(tag:Audio.Vox.Bark.Spotting.Destroy.Player) -> ... |
| 367 | AE_UX_Spotted_SpottedDestroy_VehicleDestroyed | `Audio.Event.UX.Spotted.DestroyAssist.Vehicle` | 3 | ActivateCBM(AM_CBM_NarratorActive) -> DeactivateCBM(AM_CBM_NarratorActive) -> RequestLocalVox(tag:Audio.Vox.Bark.Spotting.Destroy.Vehicle) |
| | **Vehicle** | | | |
| 368 | AE_Countermeasures_SmokeScreen | `Audio.Event.Vehicle.Countermeasures.SmokeScreen` | 5 | SetSmokeScreenActiveTime -> AttachToActor -> AttachToActor -> ... |
| 369 | AE_Vehicle_Collision | `Audio.Event.Vehicle.Shared.Collision` | 2 | PlayVehicleCollisionSound(MSS_Vehicle_Truck_Collision_Preset) -> WDMoveSoundToGameplayCueLocation |
| 370 | AE_Vehicle_Horn | `Audio.Event.Vehicle.Shared.Horn` | 5 | Doppler -> PlayVehicleHorn -> SetBool(str:HornOn) -> ... |
| 371 | AE_Vehicle_Horn_Stop | `Audio.Event.Vehicle.Shared.Horn.Stop` | 2 | EndBehavior -> SetBool(str:HornOn) |
| 372 | AE_Vehicle_LockStateChange | `Audio.Event.Vehicle.Shared.LockStateChange` | 2 | PlayVehicleLockStateChangeSound -> AttachToActor(str:body_J) |
| 373 | AE_Vehicle_Perspective | `Audio.Event.Vehicle.Shared.Perspective` | 3 | Comms_VehiclePerspective_PerspectiveChanged -> SetVehicleHostility -> VehicleHorn/Persp |
| 374 | AE_Vehicle_PostDestroy_Stop | `Audio.Event.Vehicle.Shared.PostDestroy.Stop` | 1 | StopSound |
| 375 | AE_Vehicle_Shared_Damaged | `Audio.Event.Vehicle.Shared.Damaged` | 6 | Doppler -> SetVehicleHIDZAttribute(tag:Attribute.Gameplay.Health.Engine; str:EngineHealth) -> VehicleDamaged -> ... |
| 376 | AE_Vehicle_Shared_Damaged_Stop | `Audio.Event.Vehicle.Shared.Damaged.Stop` | 4 | EndBehavior -> EndBehavior -> EndBehavior -> ... |
| 377 | AE_Vehicle_Shared_DepositSupplies | `Audio.Event.Vehicle.Shared.DepositSupplies` | 2 | PlayVehicleDepositSound -> WDMoveSoundToGameplayCueLocation |
| 378 | AE_Vehicle_Shared_Destroy | `Audio.Event.Vehicle.Shared.Destroy` | 12 | AttachToGCObject -> StopSound_SpeedOfSoundDelay -> StopSound_SpeedOfSoundDelay -> ... |
| 379 | AE_Vehicle_Shared_PostDestroy | `Audio.Event.Vehicle.Shared.PostDestroy` | 2 | AttachToActor -> PlaySound(MSS_Vehicle_Shared_Destroy_PostDestroy) |
| 380 | AE_Vehicle_SpawnVehicle_RadarFold | `Audio.Event.Vehicle.SpawnVehicle.RadarFold` | 3 | PlayAllegianceSound(MSS_Vehicle_Land_SpawnVehicle_Radar_Lonestar, MSS_Vehicle_Land_SpawnVehicle_Radar_Valkyra, MSS_Vehicle_Land_Sp) -> AttachToActor(str:body_RadarSocket) |
| 381 | AE_Vehicle_SpawnVehicle_RadarUnfold | `Audio.Event.Vehicle.SpawnVehicle.RadarUnfold` | 3 | PlayAllegianceSound(MSS_Vehicle_Land_SpawnVehicle_Radar_Lonestar, MSS_Vehicle_Land_SpawnVehicle_Radar_Valkyra, MSS_Vehicle_Land_Sp) -> AttachToActor(str:body_RadarSocket) |
| 382 | AE_Vehicle_SpawnVehicle_Radar_Damaged_OnActive | `Audio.Event.Vehicle.SpawnVehicle.Radar.Damaged.OnActive` | 2 | AttachSoundToVehicle(str:body_RadarSocket) -> PlaySound(MSS_Vehicles_Land_SpawnVehicle_Patriot_RadarDish_Damage_OneShot) |
| 383 | AE_Vehicle_SpawnVehicle_Radar_Damaged_OnRemove | `Audio.Event.Vehicle.SpawnVehicle.Radar.Damaged.OnRemove` | 2 | EndBehavior -> TriggerParamOrStop(str:Stop) |
| 384 | AE_Vehicle_SpawnVehicle_Radar_Damaged_WhileActive | `Audio.Event.Vehicle.SpawnVehicle.Radar.Damaged.WhileActive` | 4 | AttachSoundToVehicle(str:body_RadarSocket) -> SetBool(str:Destroyed) -> SetVehicleHIDZAttribute(tag:Attribute.Gameplay.Health.Radar; str:RadarHealth) -> ... |
| 385 | AE_Vehicle_SpawnVehicle_Radar_Destroyed_OnActive | `Audio.Event.Vehicle.SpawnVehicle.Radar.Destroyed.OnActive` | 2 | AttachSoundToVehicle(str:body_RadarSocket) -> PlaySound(MSS_Vehicles_Land_SpawnVehicle_Patriot_RadarDish_Destroy_OneShot) |
| 386 | AE_Vehicle_SpawnVehicle_Radar_Destroyed_OnRemove | `Audio.Event.Vehicle.SpawnVehicle.Radar.Destroyed.OnRemove` | 1 | SetBool(str:Destroyed) |
| 387 | AE_Vehicle_SpawnVehicle_Radar_Destroyed_WhileActive | `Audio.Event.Vehicle.SpawnVehicle.Radar.Destroyed.WhileActive` | 1 | SetBool(str:Destroyed) |
| 388 | AE_Vehicle_SpawnVehicle_Radar_HeavyDamaged_OnActive | `Audio.Event.Vehicle.SpawnVehicle.Radar.HeavyDamage.OnActive` | 2 | AttachSoundToVehicle(str:body_RadarSocket) -> PlaySound(MSS_Vehicles_Land_SpawnVehicle_Patriot_RadarDish_Damage_OneShot) |
| 389 | AE_Vehicle_SpawnVehicle_Radar_HeavyDamaged_OnRemove | `Audio.Event.Vehicle.SpawnVehicle.Radar.HeavyDamage.OnRemove` | 2 | EndBehavior -> TriggerParamOrStop(str:Stop) |
| 390 | AE_Vehicle_SpawnVehicle_Radar_HeavyDamaged_WhileActive | `Audio.Event.Vehicle.SpawnVehicle.Radar.HeavyDamage.WhileActive` | 4 | AttachSoundToVehicle(str:body_RadarSocket) -> SetBool(str:Destroyed) -> SetVehicleHIDZAttribute(tag:Attribute.Gameplay.Health.Radar; str:RadarHealth) -> ... |
| 391 | AE_Vehicle_UnderAttackNotify | `Audio.Event.Vehicle.UnderAttack.Start` | 1 | PlayVehicleSound(tag:Audio.Asset.Vehicle.UnderAttack) |
| 392 | AE_Vehicle_UnderAttackNotify_Stop | `Audio.Event.Vehicle.UnderAttack.Stop` | 1 | StopSound |
| | **Vehicle/Land/PZH2000** | | | |
| 393 | AE_PZH2000_Destroy | `Audio.Event.Vehicle.PZH2000.Destroy` | 6 | AttachToGCObject -> XSetExecutionContextAbandonmentSettings -> StopSound -> ... |
| 394 | AE_PZH2000_Enter | `Audio.Event.Vehicle.PZH2000.Enter` | 4 | AttachToGCObject -> PerspSound(MSS_Vehicle_PZH_Enter_1p, MSS_Vehicle_PZH_Enter_3p) -> TriggerOnGCSourceObject -> ... |
| 395 | AE_PZH2000_Exit | `Audio.Event.Vehicle.PZH2000.Exit` | 3 | AttachToGCObject -> PerspSound(MSS_Vehicle_PZH_Exit_1p, MSS_Vehicle_PZH_Exit_3p) -> VehicleHorn/Persp |
| 396 | AE_PZH2000_PostDestroy | `Audio.Event.Vehicle.PZH2000.PostDestroy` | 2 | AttachToActor -> PlaySound(MSS_Vehicle_Shared_Destroy_PostDestroy) |
| | **Vehicle/Land/SPW_01** | | | |
| 397 | AE_Vehicle_Enter_SPW_01 | `Audio.Event.Vehicle.Enter.SPW_01` | 4 | AttachToGCObject -> PerspSound(MSS_Vehicle_Spawn_Vehicle_Enter_1p, MSS_Vehicle_Spawn_Vehicle_Enter_3p) -> TriggerOnGCSourceObject -> ... |
| 398 | AE_Vehicle_Exit_SPW_01 | `Audio.Event.Vehicle.Exit.SPW_01` | 3 | AttachSoundToVehicle -> VehicleHorn/Persp -> PlaySound(MSS_Vehicle_Spawn_Vehicle_Exit_3p) |
| | **Vehicle/Land/TNK_01** | | | |
| 399 | AE_Vehicle_Enter_TNK_01 | `Audio.Event.Vehicle.Enter.TNK_01` | 4 | AttachSoundToVehicle -> TriggerOnGCSourceObject -> VehicleHorn/Persp -> ... |
| 400 | AE_Vehicle_Exit_TNK_01 | `Audio.Event.Vehicle.Exit.TNK_01` | 3 | AttachSoundToVehicle -> VehicleHorn/Persp -> PlaySound(MSS_Vehicle_TNK_01_Exit_3p) |
| | **Vehicle/ROT** | | | |
| 401 | AE_Engine_Kill_ROT | `Audio.Event.Vehicle.Engine.Kill.ROT` | 9 | EndBehavior -> EndBehavior -> EndBehavior -> ... |
| 402 | AE_Engine_Running_ROT | `Audio.Event.Vehicle.Engine.Running.ROT` | 16 | Doppler -> SetBool(str:Engine On) -> SetBool(str:Engine On) -> ... |
| 403 | AE_Engine_Stop_ROT | `Audio.Event.Vehicle.Engine.Stop.ROT` | 9 | EndBehavior -> EndBehavior -> EndBehavior -> ... |
| 404 | AE_RearRotor_Kill | `Audio.Event.Vehicle.RearRotor.Kill` | 3 | EndBehavior -> EndBehavior -> StopSound |
| 405 | AE_Vehicle_Helicopter_DustKickup | `Audio.Event.Vehicle.Shared.DustKickup` | 3 | DustKickup -> VehicleHorn/Persp -> PlaySound(MSS_Vehicle_Helicopter_DustKickup) |
| 406 | AE_Vehicle_Helicopter_DustKickup_Stop | `Audio.Event.Vehicle.Shared.DustKickup.Stop` | 2 | EndBehavior -> TriggerParamOrStop(str:On Stop) |
| 407 | AE_Vehicle_ROT_Destroy | `Audio.Event.Vehicle.Destroy.ROT_03` | 16 | AttachToGCObject -> SetROTDestroyParams -> StopSound_SpeedOfSoundDelay -> ... |
| 408 | AE_Vehicle_ROT_Destroyed_Crash | `Audio.Event.Vehicle.Destroy.Crash.ROT_03` | 2 | PlayHelicopterDestroyCrashSound -> ApplyImpulseResonance |
| 409 | AE_Vehicle_RearRotor_Running | `Audio.Event.Vehicle.RearRotor.Running` | 6 | Doppler -> SetBool(str:Engine On) -> SetVehicleHIDZAttribute(tag:Attribute.Gameplay.Health.Rotor.Tail; str:TailRotorHealth) -> ... |
| 410 | AE_Vehicle_RearRotor_Stop | `Audio.Event.Vehicle.RearRotor.Stop` | 3 | EndBehavior -> EndBehavior -> SetBool(str:Engine On) |
| | **Vehicle/Shared** | | | |
| 411 | AE_Vehicle_BrakePedalDown | `Audio.Event.Vehicle.Shared.BrakePedalDown` | 4 | VehicleHorn/Persp -> AttachToActor(str:brakePedal_J) -> TriggerParam(str:Trigger) -> ... |
| 412 | AE_Vehicle_DefenceSystem_Flares | `Audio.Event.Vehicle.Shared.DefenceSystem.Flares` | 2 | AttachToActor -> PlaySound(MSS_Vehicle_DefenceSystem_Flares_Deploy) |
| 413 | AE_Vehicle_GarageVendor_Refuel_Start | `Audio.Event.Vehicle.Shared.GarageVendor.Refuel.Start` | 3 | AttachSoundToVehicle -> VehicleHorn/Persp -> PerspSound(hostility)(DA_GarageVendor_Refuel_Audio; tag:Audio.Asset.Item.UsePrimary.1p, Audio.Asset.Item.UsePrimary.3p) |
| 414 | AE_Vehicle_GarageVendor_Refuel_Stop | `Audio.Event.Vehicle.Shared.GarageVendor.Refuel.Stop` | 1 | TriggerParam(str:Stop) |
| 415 | AE_Vehicle_GarageVendor_Repair_Start | `Audio.Event.Vehicle.Shared.GarageVendor.Repair.Start` | 3 | AttachSoundToVehicle -> VehicleHorn/Persp -> PerspSound(hostility)(DA_GarageVendor_Repair_Audio; tag:Audio.Asset.Item.UsePrimary.1p, Audio.Asset.Item.UsePrimary.3p) |
| 416 | AE_Vehicle_GarageVendor_Repair_Stop | `Audio.Event.Vehicle.Shared.GarageVendor.Repair.Stop` | 1 | TriggerParam(str:Stop) |
| 417 | AE_Vehicle_GasPedalDown | `Audio.Event.Vehicle.Shared.GasPedalDown` | 4 | VehicleHorn/Persp -> AttachToActor(str:gasPedal_J) -> TriggerParam(str:Trigger) -> ... |
| 418 | AE_Vehicle_GearChange | `Audio.Event.Vehicle.Shared.GearChange` | 3 | VehicleHorn/Persp -> AttachToActor(str:gasPedal_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.GearChange) |
| 419 | AE_Vehicle_Reversing_Start | `Audio.Event.Vehicle.Shared.Reversing.Start` | 4 | VehicleHorn/Persp -> AttachToActor(str:gasPedal_J) -> TriggerParam(str:Start) -> ... |
| 420 | AE_Vehicle_Reversing_Stop | `Audio.Event.Vehicle.Shared.Reversing.Stop` | 1 | TriggerParamOrStop(str:Stop) |
| 421 | AE_Vehicle_Shared_CantEnter | `Audio.Event.Vehicle.Shared.CantEnter` | 3 | VehicleHorn/Persp -> PlaySound(MSS_Vehicle_Shared_CantEnter_3p_Preset) -> WDMoveSoundToGameplayCueLocation |
| 422 | AE_Vehicle_Shared_ChangeSeats | `Audio.Event.Vehicle.Shared.ChangedSeat` | 2 | PerspSound(MSS_Vehicle_Shared_ChangeSeats_Generic_1p, MSS_Vehicle_Shared_ChangeSeats_Generic_3p) -> VehicleHorn/Persp |
| 423 | AE_Vehicle_Shared_Hifi_Start | `Audio.Event.Vehicle.Hifi.Start` | 3 | VehicleHorn/Persp -> VehiclePlayTape(MSS_Vehicle_HiFi_Master) -> AttachToActor(str:radio_J) |
| 424 | AE_Vehicle_Shared_Hifi_Stop | `Audio.Event.Vehicle.Hifi.Stop` | 1 | TriggerParam(str:Stop) |
| 425 | AE_Vehicle_Shared_Spawn | `Audio.Event.Vehicle.Shared.Spawn` | 2 | PlayVehiclePurchaseHorn -> WDMoveSoundToGameplayCueLocation |
| | **Vehicle/Shared/HIDZ** | | | |
| 426 | AE_Haywire_Stop | `Audio.Event.Vehicle.HIDZ.Haywire.Stop` | 1 | TriggerParamOrStop(str:Stop) |
| 427 | AE_Vehicle_FuelTank_Leaking | `Audio.Event.Vehicle.FuelTank.Leaking` | 6 | VehicleHorn/Persp -> AttachToActor(str:fuelPoint_J) -> AttachToActor(str:fuelPoint_J) -> ... |
| 428 | AE_Vehicle_FuelTank_Leaking_Stop | `Audio.Event.Vehicle.FuelTank.Leaking.Stop` | 2 | EndBehavior -> TriggerParamOrStop(str:Stop) |
| 429 | AE_Vehicle_HIDZRearRotor_Destroy | `Audio.Event.Vehicle.HIDZ.TailRotor.Destroy` | 2 | AttachToActor(str:collective_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.TailRotor.Destroy) |
| 430 | AE_Vehicle_HIDZ_Haywire | `Audio.Event.Vehicle.HIDZ.Haywire` | 4 | SetBool(str:IsDestroyed) -> VehicleHorn/Persp -> AttachToActor(str:collectiveThrottleR_J) -> ... |
| 431 | AE_Vehicle_HIDZ_MainRotor_Damaged | `Audio.Event.Vehicle.HIDZ.MainRotor.Damaged` | 5 | Doppler -> SetVehicleHIDZAttribute(tag:Attribute.Gameplay.Health.Rotor.Main; str:HIDZHealth) -> VehicleHorn/Persp -> ... |
| 432 | AE_Vehicle_HIDZ_MainRotor_Damaged_Stop | `Audio.Event.Vehicle.HIDZ.MainRotor.Damaged.Stop` | 3 | EndBehavior -> EndBehavior -> TriggerParamOrStop(str:Stop) |
| 433 | AE_Vehicle_HIDZ_MainRotor_Destroy | `Audio.Event.Vehicle.HIDZ.MainRotor.Destroy` | 5 | SetROTDestroyParams -> StopSound_SpeedOfSoundDelay -> StopSound_SpeedOfSoundDelay -> ... |
| 434 | AE_Vehicle_HIDZ_RearRotor_Damaged | `Audio.Event.Vehicle.HIDZ.TailRotor.Damaged` | 5 | Doppler -> SetVehicleHIDZAttribute(tag:Attribute.Gameplay.Health.Rotor.Tail; str:HIDZHealth) -> VehicleHorn/Persp -> ... |
| 435 | AE_Vehicle_HIDZ_RearRotor_Damaged_Stop | `Audio.Event.Vehicle.HIDZ.TailRotor.Damaged.Stop` | 3 | EndBehavior -> EndBehavior -> TriggerParamOrStop(str:Stop) |
| | **Vehicle/Shared/HIDZ/Wheels** | | | |
| 436 | AE_Vehicle_HIDZ_WheelFlat_FrontLeft | `Audio.Event.Vehicle.HIDZ.Wheel.FlatLoop.FrontLeft` | 2 | AttachToActor(str:frontLWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.FlatLoop) |
| 437 | AE_Vehicle_HIDZ_WheelFlat_FrontRight | `Audio.Event.Vehicle.HIDZ.Wheel.FlatLoop.FrontRight` | 2 | AttachToActor(str:frontRWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.FlatLoop) |
| 438 | AE_Vehicle_HIDZ_WheelFlat_RearLeft | `Audio.Event.Vehicle.HIDZ.Wheel.FlatLoop.RearLeft` | 2 | AttachToActor(str:rearLWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.FlatLoop) |
| 439 | AE_Vehicle_HIDZ_WheelFlat_RearRight | `Audio.Event.Vehicle.HIDZ.Wheel.FlatLoop.RearRight` | 2 | AttachToActor(str:rearRWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.FlatLoop) |
| 440 | AE_Vehicle_HIDZ_WheelPop_FrontLeft | `Audio.Event.Vehicle.HIDZ.Wheel.Pop.FrontLeft` | 2 | AttachToActor(str:frontLWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Pop) |
| 441 | AE_Vehicle_HIDZ_WheelPop_FrontRight | `Audio.Event.Vehicle.HIDZ.Wheel.Pop.FrontRight` | 2 | AttachToActor(str:frontRWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Pop) |
| 442 | AE_Vehicle_HIDZ_WheelPop_RearLeft | `Audio.Event.Vehicle.HIDZ.Wheel.Pop.RearLeft` | 2 | AttachToActor(str:rearLWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Pop) |
| 443 | AE_Vehicle_HIDZ_WheelPop_RearRight | `Audio.Event.Vehicle.HIDZ.Wheel.Pop.RearRight` | 2 | AttachToActor(str:rearRWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Pop) |
| 444 | AE_Vehicle_HIDZ_Wheel_Destroy_FrontLeft | `Audio.Event.Vehicle.HIDZ.Wheel.Destroy.FrontLeft` | 2 | AttachToActor(str:frontLWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Destroy) |
| 445 | AE_Vehicle_HIDZ_Wheel_Destroy_FrontRight | `Audio.Event.Vehicle.HIDZ.Wheel.Destroy.FrontRight` | 2 | AttachToActor(str:frontRWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Destroy) |
| 446 | AE_Vehicle_HIDZ_Wheel_Destroy_RearLeft | `Audio.Event.Vehicle.HIDZ.Wheel.Destroy.RearLeft` | 2 | AttachToActor(str:rearLWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Destroy) |
| 447 | AE_Vehicle_HIDZ_Wheel_Destroy_RearRight | `Audio.Event.Vehicle.HIDZ.Wheel.Destroy.RearRight` | 2 | AttachToActor(str:rearRWheelSpin_J) -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.Destroy) |
| 448 | AE_Vehicle_HIDZ_Wheel_DestroyedLoop_FrontLeft | `Audio.Event.Vehicle.HIDZ.Wheel.DestroyedLoop.FrontLeft` | 3 | AttachToActor(str:frontLWheelSpin_J) -> StopSound -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.DestroyedLoop) |
| 449 | AE_Vehicle_HIDZ_Wheel_DestroyedLoop_FrontRight | `Audio.Event.Vehicle.HIDZ.Wheel.DestroyedLoop.FrontRight` | 3 | AttachToActor(str:frontRWheelSpin_J) -> StopSound -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.DestroyedLoop) |
| 450 | AE_Vehicle_HIDZ_Wheel_DestroyedLoop_RearLeft | `Audio.Event.Vehicle.HIDZ.Wheel.DestroyedLoop.RearLeft` | 3 | AttachToActor(str:rearLWheelSpin_J) -> StopSound -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.DestroyedLoop) |
| 451 | AE_Vehicle_HIDZ_Wheel_DestroyedLoop_RearRight | `Audio.Event.Vehicle.HIDZ.Wheel.DestroyedLoop.RearRight` | 3 | AttachToActor(str:rearRWheelSpin_J) -> StopSound -> PlayVehicleSound(tag:Audio.Asset.Vehicle.Shared.HIDZ.Wheel.DestroyedLoop) |
| | **Vehicle/TNK** | | | |
| 452 | AE_Vehicle_Engine_Running_TNK | `Audio.Event.Vehicle.Engine.Running.TNK` | 10 | Doppler -> SetBool(str:DisallowIgnition) -> SetBool(str:Engine On) -> ... |
| 453 | AE_Vehicle_Engine_Stop_TNK | `Audio.Event.Vehicle.Engine.Stop.TNK` | 4 | EndBehavior -> EndBehavior -> EndBehavior -> ... |
| 454 | AE_Vehicle_Moving_Stop_TNK | `Audio.Event.Vehicle.MovingStop.TNK` | 3 | EndBehavior -> StopSound -> StopSound |
| 455 | AE_Vehicle_Moving_TNK | `Audio.Event.Vehicle.Moving.TNK` | 7 | SetVehicleParameters_SpeedAndRotation -> SetVehicleParameters_Tracked -> VehicleHorn/Persp -> ... |
| | **Vehicle/Targeting** | | | |
| 456 | AE_Vehicle_Targeting_IsFullLockedOnTo | `Audio.Event.Vehicle.Shared.Targeting.IsFullLockedOnTo` | 4 | VehicleHorn/Persp -> AttachToActor -> TriggerParam(str:Full Locked Start) -> ... |
| 457 | AE_Vehicle_Targeting_IsFullLockedOnTo_Stop | `Audio.Event.Vehicle.Shared.Targeting.IsFullLockedOnTo.Stop` | 2 | TriggerParam(str:Full Locked Stop) -> StopSound |
| 458 | AE_Vehicle_Targeting_IsLockedOnTo | `Audio.Event.Vehicle.Shared.Targeting.IsLockedOnTo` | 4 | VehicleHorn/Persp -> AttachToActor -> TriggerParam(str:LockOn Start) -> ... |
| 459 | AE_Vehicle_Targeting_IsLockedOnTo_Stop | `Audio.Event.Vehicle.Shared.Targeting.IsLockedOnTo.Stop` | 2 | TriggerParam(str:Stop Sound) -> StopSound |
| | **Vehicle/WHL** | | | |
| 460 | AE_Vehicle_EngineRunning_WHL | `Audio.Event.Vehicle.Engine.Running.WHL` | 9 | Doppler -> SetBool(str:Engine On) -> SetVehicleHostility -> ... |
| 461 | AE_Vehicle_EngineStop_WHL | `Audio.Event.Vehicle.Engine.Stop.WHL` | 4 | EndBehavior -> EndBehavior -> EndBehavior -> ... |
| 462 | AE_Vehicle_Engine_Start | `Audio.Event.Vehicle.Engine.Start` | 2 | SetAudioParameters -> SetBool(str:AllowIgnition) |
| 463 | AE_Vehicle_MovingStop_WHL | `Audio.Event.Vehicle.MovingStop.WHL` | 4 | StopSoundByContext -> StopSound -> StopSound -> ... |
| 464 | AE_Vehicle_Moving_WHL | `Audio.Event.Vehicle.Moving.WHL` | 8 | HIDZ_Wheels -> SetVehicleParameters_SpeedAndRotation -> SetVehicleParameters_Wheeled -> ... |
| | **Vehicle/Weapon/Aim** | | | |
| 465 | AE_Vehicle_Weapon_Aim_ChangeDirection | `Audio.Event.Vehicle.Shared.Weapon.Aim.ChangeDirection` | 1 | TriggerParam(str:Change Direction) |
| 466 | AE_Vehicle_Weapon_Aim_Start | `Audio.Event.Vehicle.Shared.Weapon.Aim` | 3 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.Aim.1p, Audio.Asset.Vehicle.Weapon.Aim.3p) -> AttachToActor -> WDSetVehicleWeaponAim |
| 467 | AE_Vehicle_Weapon_Aim_Stop | `Audio.Event.Vehicle.Shared.Weapon.Aim.Stop` | 1 | EndBehavior |
| | **Vehicle/Weapon/Fire** | | | |
| 468 | AE_Vehicle_Weapon_Artillery_Fire | `Audio.Event.Weapon.Artillery.Fire` | 5 | ArtilleryFiringSound(MSS_Weapon_Vehicle_Artillery_Fire_1p, MSS_Weapon_Vehicle_Artillery_Fire_3p) -> SetHostilityParameter -> TriggerParam(str:Semi) -> ... |
| 469 | AE_Vehicle_Weapon_Artillery_Travel_1p | `Audio.Event.Weapon.Artillery.Travel.1p` | 2 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.Travel.1p) -> Vehicle_Artillery_Travel_1p |
| 470 | AE_Vehicle_Weapon_Artillery_Travel_1p_Stop | `Audio.Event.Weapon.Artillery.Travel.1p.Stop` | 3 | StopSound -> StopSound -> StopSound |
| 471 | AE_Vehicle_Weapon_Artillery_Travel_3p | `Audio.Event.Weapon.Artillery.Travel.3p` | 1 | PlayVehicleWeaponPerspectiveSound |
| 472 | AE_Vehicle_Weapon_Fire_DryFire | `Audio.Event.Vehicle.Shared.Weapon.Fire.DryFire` | 4 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Item.DryFire.1p, Audio.Asset.Item.DryFire.3p) -> SetHostilityParameter -> VehicleWeaponStartFireParameters -> ... |
| 473 | AE_Vehicle_Weapon_Fire_Start_Auto | `Audio.Event.Vehicle.Shared.Weapon.Fire.Start.Auto` | 5 | EnemyAccuracyScaling_Vehicle -> PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.Fire.1p, Audio.Asset.Vehicle.Weapon.Fire.3p) -> VehicleWeaponStartFirePar |
| 474 | AE_Vehicle_Weapon_Fire_Start_Burst | `Audio.Event.Vehicle.Shared.Weapon.Fire.Start.Burst` | 5 | EnemyAccuracyScaling_Vehicle -> PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.Fire.1p, Audio.Asset.Vehicle.Weapon.Fire.3p) -> SetHostilityParameter ->  |
| 475 | AE_Vehicle_Weapon_Fire_Start_Semi | `Audio.Event.Vehicle.Shared.Weapon.Fire.Start.Semi` | 6 | EnemyAccuracyScaling_Vehicle -> PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.Fire.1p, Audio.Asset.Vehicle.Weapon.Fire.3p) -> SetHostilityParameter ->  |
| 476 | AE_Vehicle_Weapon_Fire_Stop | `Audio.Event.Vehicle.Shared.Weapon.Fire.Stop` | 4 | EndBehavior -> EndBehavior -> SetBool(str:IsFiring) -> ... |
| 477 | AE_Vehicle_Weapon_Fire_StopSilent | `Audio.Event.Vehicle.Shared.Weapon.Fire.StopSilent` | 5 | EndBehavior -> EndBehavior -> EndBehavior -> ... |
| 478 | AE_Vehicle_Weapon_Fire_StopTail | `Audio.Event.Vehicle.Shared.Weapon.Fire.StopTail` | 1 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.Fire.Stop.3p) |
| 479 | AE_Vehicle_Weapon_PreFire_Start | `Audio.Event.Vehicle.Shared.Weapon.StartPreFire` | 3 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Vehicle.Weapon.PreFire.1P, Audio.Asset.Vehicle.Weapon.PreFire.3P) -> VehicleWeaponPreFireParameters -> TriggerParam(str: |
| 480 | AE_Vehicle_Weapon_PreFire_Stop | `Audio.Event.Vehicle.Shared.Weapon.StopPreFire` | 1 | TriggerParamOrStop(str:StopPreFire) |
| 481 | AE_Vehicle_Weapon_PreFire_StopSilent | `Audio.Event.Vehicle.Shared.Weapon.StopPreFire.Silent` | 1 | StopSound |
| | **Vehicle/Weapon/Reload** | | | |
| 482 | AE_Vehicle_Weapon_Reload_Cancelled | `Audio.Event.Vehicle.Shared.Weapon.Reload.Cancelled` | 1 | StopSound |
| 483 | AE_Vehicle_Weapon_Reload_Empty | `Audio.Event.Vehicle.Shared.Weapon.Reload.Empty` | 2 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> XMoveSoundToActor |
| 484 | AE_Vehicle_Weapon_Reload_LoadRound | `Audio.Event.Vehicle.Shared.Weapon.Reload.LoadRound` | 2 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> XMoveSoundToActor |
| 485 | AE_Vehicle_Weapon_Reload_LoadRounds | `Audio.Event.Vehicle.Shared.Weapon.Reload.LoadRounds` | 4 | GetLengthOfTankReload -> PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Reload) -> ... |
| 486 | AE_Vehicle_Weapon_Reload_Tactical | `Audio.Event.Vehicle.Shared.Weapon.Reload.Tactical` | 2 | PlayVehicleWeaponPerspectiveSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> XMoveSoundToActor |
| | **Vehicle/Weapon/Stabilizers** | | | |
| 487 | AE_Vehicle_Stabilizing | `Audio.Event.Vehicle.Stabilizing` | 4 | TriggerStabilizingState -> VehicleHorn/Persp -> AttachToActor -> ... |
| 488 | AE_Vehicle_Stabilizing_Complete | `Audio.Event.Vehicle.Stabilizing.Complete` | 4 | TriggerStabilizingState -> VehicleHorn/Persp -> AttachToActor -> ... |
| 489 | AE_Vehicle_Stabilizing_Fail | `Audio.Event.Vehicle.Stabilizing.Fail` | 4 | VehicleHorn/Persp -> AttachToActor -> TriggerParam(str:Trigger) -> ... |
| 490 | AE_Vehicle_Stabilizing_Stop | `Audio.Event.Vehicle.Stabilizing.Stop` | 1 | TriggerParam(str:Stop) |
| | **Vendor** | | | |
| 491 | AE_Vendor_Greeting_Bye_Base | `Audio.Event.Vendor.Greeting.Bye.Base` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Bye_Base_Preset) |
| 492 | AE_Vendor_Greeting_Bye_FTUE | `Audio.Event.Vendor.Greeting.Bye.FTUE` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Bye_FTUE_Preset) |
| 493 | AE_Vendor_Greeting_Bye_NoPurchase | `Audio.Event.Vendor.Greeting.Bye.NoPurchase` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Bye_NoPurchase_Preset) |
| 494 | AE_Vendor_Greeting_Bye_ShootingRange | `Audio.Event.Vendor.Greeting.Bye.ShootingRange` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Bye_ShootingRange_Preset) |
| 495 | AE_Vendor_Greeting_Hello_Base | `Audio.Event.Vendor.Greeting.Hello.Base` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Hello_Base_Preset) |
| 496 | AE_Vendor_Greeting_Hello_FTUE | `Audio.Event.Vendor.Greeting.Hello.FTUE` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Hello_FTUE_Preset) |
| 497 | AE_Vendor_Greeting_Hello_ShootingRange | `Audio.Event.Vendor.Greeting.Hello.ShootingRange` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Greeting_Hello_ShootingRange_Preset) |
| | **Weapon** | | | |
| 498 | AE_Weapon_Focus_End | `Audio.Event.Weapon.Focus.End` | 6 | DeactivateCBM(AM_CBM_Focus) -> FocusRemaining -> RemoveCosmeticExertionSource -> ... |
| 499 | AE_Weapon_Focus_Start | `Audio.Event.Weapon.Focus.Start` | 7 | ActivateCBM(AM_CBM_Focus) -> FocusFOVMultiplier -> FocusRemaining -> ... |
| | **Weapon/Attachment** | | | |
| 500 | AE_Weapon_Attachment_Bipod_Dismount | `Audio.Event.Weapon.Attachment.Bipod.Dismount` | 2 | AttachToHeldItem -> PerspSound(MSS_Weapon_Attachment_Bipod_Dismount_1p, MSS_Weapon_Attachment_Bipod_Dismount_3p) |
| 501 | AE_Weapon_Attachment_Bipod_Fold | `Audio.Event.Weapon.Attachment.Bipod.Fold` | 2 | AttachToHeldItem -> PlayWeaponAttachmentSound(tag:Audio.Asset.Weapon.Attachment.Bipod.Fold.1p, Audio.Asset.Weapon.Attachment.Bipod.Fold.3p) |
| 502 | AE_Weapon_Attachment_Bipod_Fold_BMR | `Audio.Event.Weapon.Attachment.Bipod.Fold.BMR` | 2 | AttachToHeldItem -> PerspSound(MSS_Weapon_Attachment_GripPod_Fold_1p, MSS_Weapon_Attachment_GripPod_Fold_3p_Preset) |
| 503 | AE_Weapon_Attachment_Bipod_Mount | `Audio.Event.Weapon.Attachment.Bipod.Mount` | 2 | AttachToHeldItem -> PerspSound(MSS_Weapon_Attachment_Bipod_Mount_1p, MSS_Weapon_Attachment_Bipod_Mount_3p) |
| 504 | AE_Weapon_Attachment_Bipod_Unfold | `Audio.Event.Weapon.Attachment.Bipod.Unfold` | 2 | AttachToHeldItem -> PlayWeaponAttachmentSound(tag:Audio.Asset.Weapon.Attachment.Bipod.Unfold.1p, Audio.Asset.Weapon.Attachment.Bipod.Unfold.3p) |
| 505 | AE_Weapon_Attachment_Bipod_Unfold_BMR | `Audio.Event.Weapon.Attachment.Bipod.Unfold.BMR` | 2 | AttachToHeldItem -> PerspSound(MSS_Weapon_Attachment_GripPod_Unfold_1p, MSS_Weapon_Attachment_GripPod_Unfold_3p_Preset) |
| | **Weapon/Firing** | | | |
| 506 | AE_Weapon_BackBlast | `Audio.Event.Weapon.BackBlast` | 2 | AttachSoundToWeaponComponent(str:S_backblast) -> PerspSound(MSS_Weapon_Shared_BackBlast) |
| 507 | AE_Weapon_CycleFireMode | `Audio.Event.Weapon.CycleFireMode` | 3 | AttachToHeldItem -> ExecuteFireModeTrigger -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Firemode.1p, Audio.Asset.Weapon.Firemode.3p) |
| 508 | AE_Weapon_DecreaseZeroing | `Audio.Event.Weapon.DecreaseZeroing` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Zeroing.1p, Audio.Asset.Weapon.Zeroing.3p) -> TriggerParam(str:DecreaseZeroing.Trigger) |
| 509 | AE_Weapon_Fire_BulletCasing | `Audio.Event.Weapon.Projectile.BulletCasing` | 1 | PlayBulletCasing(DA_BulletCasings_Medium, DA_BulletCasings_Shotgun) |
| 510 | AE_Weapon_Fire_DryFire | `Audio.Event.Weapon.Fire.DryFire` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.DryFire.1p, Audio.Asset.Item.DryFire.3p) -> TriggerParam(str:StopFire) |
| 511 | AE_Weapon_Fire_Start_Auto | `Audio.Event.Weapon.Fire.Start.Auto` | 8 | AttachToHeldItem(str:S_Muzzle) -> EnemyAccuracyScaling -> SetHeldWeaponStartFireParameters -> ... |
| 512 | AE_Weapon_Fire_Start_Auto_Suppressed | `Audio.Event.Weapon.Fire.Start.Auto.Suppressed` | 8 | AttachToHeldItem(str:S_Muzzle) -> EnemyAccuracyScaling -> SetHeldWeaponStartFireParameters -> ... |
| 513 | AE_Weapon_Fire_Start_Burst | `Audio.Event.Weapon.Fire.Start.Burst` | 8 | AttachToHeldItem(str:S_Muzzle) -> EnemyAccuracyScaling -> SetHeldWeaponStartFireParameters -> ... |
| 514 | AE_Weapon_Fire_Start_Burst_Suppressed | `Audio.Event.Weapon.Fire.Start.Burst.Suppressed` | 8 | AttachToHeldItem(str:S_Muzzle) -> EnemyAccuracyScaling -> SetHeldWeaponStartFireParameters -> ... |
| 515 | AE_Weapon_Fire_Start_Semi | `Audio.Event.Weapon.Fire.Start.Semi` | 11 | AttachToHeldItem(str:S_Muzzle) -> CombatBow_GetVelocity -> EnemyAccuracyScaling -> ... |
| 516 | AE_Weapon_Fire_Start_Semi_Suppressed | `Audio.Event.Weapon.Fire.Start.Semi.Suppressed` | 9 | AttachToHeldItem(str:S_Muzzle) -> EnemyAccuracyScaling -> SetHeldWeaponStartFireParameters -> ... |
| 517 | AE_Weapon_Fire_Stop | `Audio.Event.Weapon.Fire.Stop` | 4 | EndBehavior -> EndBehavior -> SetBool(str:IsFiring) -> ... |
| 518 | AE_Weapon_IncreaseZeroing | `Audio.Event.Weapon.IncreaseZeroing` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Zeroing.1p, Audio.Asset.Weapon.Zeroing.3p) -> TriggerParam(str:IncreaseZeroing.Trigger) |
| 519 | AE_Weapon_PreFire_Start | `Audio.Event.Weapon.PreFire.Start` | 2 | HeldItemPerspSound(tag:Audio.Asset.Weapon.PreFire.1p, Audio.Asset.Weapon.PreFire.3p) -> TriggerParam(str:StartPreFire) |
| 520 | AE_Weapon_PreFire_Stop | `Audio.Event.Weapon.PreFire.Stop` | 1 | TriggerParamOrStop(str:StopPreFire) |
| 521 | AE_Weapon_Rechamber | `Audio.Event.Weapon.Rechamber` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Rechamber.1p, Audio.Asset.Weapon.Rechamber.3p) |
| 522 | AE_Weapon_Rechamber_ExplosiveArrow | `Audio.Event.Weapon.Rechamber.Arrow.Explosive` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Rechamber.Arrow.Explosive.1p, Audio.Asset.Weapon.Rechamber.Arrow.Explosive.3p) |
| | **Weapon/Foley** | | | |
| 523 | AE_EquipFlair | `Audio.Event.Weapon.EquipFlair` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.EquipFlair.1p, Audio.Asset.Weapon.EquipFlair.3p) |
| 524 | AE_Item_Equip | `Audio.Event.Item.Equip` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.Equip.1p, Audio.Asset.Item.Equip.3p) |
| 525 | AE_Item_Equip_FuelCan | `Audio.Event.Item.Equip.FuelCan` | 3 | AttachToHeldItem -> FuelCannister -> HeldItemPerspSound(tag:Audio.Asset.Item.Equip.1p, Audio.Asset.Item.Equip.3p) |
| 526 | AE_Item_Holster | `Audio.Event.Item.Holster` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Item.Holster.1p, Audio.Asset.Item.Holster.3p) |
| 527 | AE_Item_Holster_FuelCan | `Audio.Event.Item.Holster.FuelCan` | 3 | AttachToHeldItem -> FuelCannister -> HeldItemPerspSound(tag:Audio.Asset.Item.Holster.1p, Audio.Asset.Item.Holster.3p) |
| 528 | AE_Item_Inspect_FuelCan | `Audio.Event.Item.Inspect.FuelCan` | 3 | AttachToHeldItem -> FuelCannister -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Inspect.1p, Audio.Asset.Weapon.Inspect.3p) |
| 529 | AE_Item_Inspect_Stop | `Audio.Event.Item.Inspect.Stop` | 1 | StopSound |
| 530 | AE_Weapon_ADSIn | `Audio.Event.Weapon.ADSIn` | 3 | ActivateCBM(AM_CBM_ADS) -> AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ADSIn.1p, Audio.Asset.Weapon.ADSIn.3p) |
| 531 | AE_Weapon_ADSOut | `Audio.Event.Weapon.ADSOut` | 4 | AttachToHeldItem -> DeactivateCBM(AM_CBM_ADS) -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ADSOut.1p, Audio.Asset.Weapon.ADSOut.3p) -> ... |
| 532 | AE_Weapon_Drop | `Audio.Event.Weapon.Drop` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Drop.1p, Audio.Asset.Weapon.Drop.3p) |
| 533 | AE_Weapon_Inspect | `Audio.Event.Weapon.Inspect` | 2 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Inspect.1p, Audio.Asset.Weapon.Inspect.3p) |
| 534 | AE_Weapon_MeleeSwing | `Audio.Event.Weapon.MeleeSwing` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Melee.1p, Audio.Asset.Weapon.Melee.3p) -> RequestVox(tag:Audio.Vox.Exertion.MeleeSwing) |
| 535 | AE_Weapon_MeleeSwing_Heavy | `Audio.Event.Weapon.MeleeSwing.Heavy` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.Melee.1p, Audio.Asset.Weapon.Melee.3p) -> RequestVox(tag:Audio.Vox.Exertion.MeleeSwing.Heavy) |
| 536 | AE_Weapon_Reload_Cancelled | `Audio.Event.Weapon.Reload.Cancelled` | 1 | CancelReloadSound |
| 537 | AE_Weapon_Zoom_In | `Audio.Event.Weapon.Zoom.In` | 1 | PlaySound(MSS_Weapon_Zooming_Master) |
| 538 | AE_Weapon_Zoom_Out | `Audio.Event.Weapon.Zoom.Out` | 1 | PlaySound(MSS_Weapon_Zooming_Master) |
| | **Weapon/Foley/ReloadEmpty** | | | |
| 539 | AE_ReloadEmpty_Stage1 | `Audio.Event.Weapon.ReloadEmpty.Stage1` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage1) |
| 540 | AE_ReloadEmpty_Stage2 | `Audio.Event.Weapon.ReloadEmpty.Stage2` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage2) |
| 541 | AE_ReloadEmpty_Stage3 | `Audio.Event.Weapon.ReloadEmpty.Stage3` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage3) |
| 542 | AE_ReloadEmpty_Stage4 | `Audio.Event.Weapon.ReloadEmpty.Stage4` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage4) |
| 543 | AE_ReloadEmpty_Stage5 | `Audio.Event.Weapon.ReloadEmpty.Stage5` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage5) |
| 544 | AE_ReloadEmpty_Stage6 | `Audio.Event.Weapon.ReloadEmpty.Stage6` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage6) |
| 545 | AE_ReloadEmpty_Stage7 | `Audio.Event.Weapon.ReloadEmpty.Stage7` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage7) |
| 546 | AE_ReloadEmpty_Stage8 | `Audio.Event.Weapon.ReloadEmpty.Stage8` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.1p, Audio.Asset.Weapon.ReloadEmpty.3p) -> TriggerParam(str:Stage8) |
| | **Weapon/Foley/ReloadEmpty_Drop** | | | |
| 547 | AE_MagRetention | `Audio.Event.Weapon.Reload.MagRetention` | 1 | PlaySound(MSS_Weapon_Shared_MagRetention) |
| 548 | AE_ReloadEmpty_Drop_Stage1 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage1` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage1) |
| 549 | AE_ReloadEmpty_Drop_Stage2 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage2` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage2) |
| 550 | AE_ReloadEmpty_Drop_Stage3 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage3` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage3) |
| 551 | AE_ReloadEmpty_Drop_Stage4 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage4` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage4) |
| 552 | AE_ReloadEmpty_Drop_Stage5 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage5` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage5) |
| 553 | AE_ReloadEmpty_Drop_Stage6 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage6` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage6) |
| 554 | AE_ReloadEmpty_Drop_Stage7 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage7` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage7) |
| 555 | AE_ReloadEmpty_Drop_Stage8 | `Audio.Event.Weapon.ReloadEmpty.Drop.Stage8` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drop.1p, Audio.Asset.Weapon.ReloadEmpty.Drop.3p) -> TriggerParam(str:Stage8) |
| | **Weapon/Foley/ReloadEmpty_Drum** | | | |
| 556 | AE_ReloadEmpty_Drum_Stage1 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage1` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage1) |
| 557 | AE_ReloadEmpty_Drum_Stage2 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage2` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage2) |
| 558 | AE_ReloadEmpty_Drum_Stage3 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage3` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage3) |
| 559 | AE_ReloadEmpty_Drum_Stage4 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage4` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage4) |
| 560 | AE_ReloadEmpty_Drum_Stage5 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage5` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage5) |
| 561 | AE_ReloadEmpty_Drum_Stage6 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage6` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage6) |
| 562 | AE_ReloadEmpty_Drum_Stage7 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage7` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage7) |
| 563 | AE_ReloadEmpty_Drum_Stage8 | `Audio.Event.Weapon.ReloadEmpty.Drum.Stage8` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadEmpty.Drum.1p, Audio.Asset.Weapon.ReloadEmpty.Drum.3p) -> TriggerParam(str:Stage8) |
| | **Weapon/Foley/ReloadTactical** | | | |
| 564 | AE_ReloadTactical_Stage1 | `Audio.Event.Weapon.ReloadTactical.Stage1` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage1) |
| 565 | AE_ReloadTactical_Stage2 | `Audio.Event.Weapon.ReloadTactical.Stage2` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage2) |
| 566 | AE_ReloadTactical_Stage3 | `Audio.Event.Weapon.ReloadTactical.Stage3` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage3) |
| 567 | AE_ReloadTactical_Stage4 | `Audio.Event.Weapon.ReloadTactical.Stage4` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage4) |
| 568 | AE_ReloadTactical_Stage5 | `Audio.Event.Weapon.ReloadTactical.Stage5` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage5) |
| 569 | AE_ReloadTactical_Stage6 | `Audio.Event.Weapon.ReloadTactical.Stage6` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage6) |
| 570 | AE_ReloadTactical_Stage7 | `Audio.Event.Weapon.ReloadTactical.Stage7` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage7) |
| 571 | AE_ReloadTactical_Stage8 | `Audio.Event.Weapon.ReloadTactical.Stage8` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.1p, Audio.Asset.Weapon.ReloadTactical.3p) -> TriggerParam(str:Stage8) |
| | **Weapon/Foley/ReloadTactical_Drop** | | | |
| 572 | AE_ReloadTactical_Drop_Stage1 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage1` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage1) |
| 573 | AE_ReloadTactical_Drop_Stage2 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage2` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage2) |
| 574 | AE_ReloadTactical_Drop_Stage3 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage3` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage3) |
| 575 | AE_ReloadTactical_Drop_Stage4 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage4` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage4) |
| 576 | AE_ReloadTactical_Drop_Stage5 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage5` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage5) |
| 577 | AE_ReloadTactical_Drop_Stage6 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage6` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage6) |
| 578 | AE_ReloadTactical_Drop_Stage7 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage7` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage7) |
| 579 | AE_ReloadTactical_Drop_Stage8 | `Audio.Event.Weapon.ReloadTactical.Drop.Stage8` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drop.1p, Audio.Asset.Weapon.ReloadTactical.Drop.3p) -> TriggerParam(str:Stage8) |
| | **Weapon/Foley/ReloadTactical_Drum** | | | |
| 580 | AE_ReloadTactical_Drum_Stage1 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage1` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage1) |
| 581 | AE_ReloadTactical_Drum_Stage2 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage2` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage2) |
| 582 | AE_ReloadTactical_Drum_Stage3 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage3` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage3) |
| 583 | AE_ReloadTactical_Drum_Stage4 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage4` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage4) |
| 584 | AE_ReloadTactical_Drum_Stage5 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage5` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage5) |
| 585 | AE_ReloadTactical_Drum_Stage6 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage6` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage6) |
| 586 | AE_ReloadTactical_Drum_Stage7 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage7` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage7) |
| 587 | AE_ReloadTactical_Drum_Stage8 | `Audio.Event.Weapon.ReloadTactical.Drum.Stage8` | 3 | AttachToHeldItem -> HeldItemPerspSound(tag:Audio.Asset.Weapon.ReloadTactical.Drum.1p, Audio.Asset.Weapon.ReloadTactical.Drum.3p) -> TriggerParam(str:Stage8) |
| | **Weapon/Projectile** | | | |
| 588 | AE_Weapon_Projectile_Impact | `Audio.Event.Weapon.Projectile.Impact` | 1 | PlayProjectileImpactSound(SBMIX_Reverb) |
| 589 | AE_Weapon_Projectile_Impact_Explosive | `Audio.Event.Weapon.Projectile.Impact.Explosive` | 6 | PlayProjectileExplosionImpactSound(DA_Impact_Drone_Explosion_Audio, DA_Weapon_Projectile_40mm_Audio, DA_Weapon_Projectile_72mm_Audio, DA_Weapon_P) -> PlayVehicleSound(tag |
| 590 | AE_Weapon_Projectile_PenetrationEnter | `Audio.Event.Weapon.Projectile.PenetrationEnter` | 1 | PlayProjectileImpactSound |
| 591 | AE_Weapon_Projectile_Ricochet | `Audio.Event.Weapon.Projectile.Ricochet` | 1 | PlayProjectileImpactSound |
| 592 | AE_Weapon_Projectile_WhizBy | `Audio.Event.Weapon.Projectile.WhizBy` | 1 | PlayProjectileWhizBy(MSS_Player_Whizby_Medium, MSS_Player_Whizby_Large, MSS_Player_Whizby_Shotgun, MSS_Player_Whizby_Arrow, MSS_Pla) |
| | **Weapon/Projectile/Projectile_Travel** | | | |
| 593 | AE_Weapon_Projectile_Rocket_Travel_120mm | `Audio.Event.Projectile.Rocket.Travel.120mm` | 3 | HandleProjectileSimulation -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_120mm_Preset) -> AttachToActor |
| 594 | AE_Weapon_Projectile_Rocket_Travel_122mm | `Audio.Event.Projectile.Rocket.Travel.122mm` | 3 | HandleProjectileSimulation -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_122mm_Preset) -> AttachToActor |
| 595 | AE_Weapon_Projectile_Rocket_Travel_155mm | `Audio.Event.Projectile.Rocket.Travel.155mm` | 4 | HandleProjectileSimulation -> HandleRocketIncoming(MSS_Weapon_Projectile_155mm_Incoming_Preset) -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_155mm) -> ... |
| 596 | AE_Weapon_Projectile_Rocket_Travel_40mm | `Audio.Event.Projectile.Rocket.Travel.40mm` | 3 | HandleProjectileSimulation -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_40mm_Preset) -> AttachToActor |
| 597 | AE_Weapon_Projectile_Rocket_Travel_72mm | `Audio.Event.Projectile.Rocket.Travel.72mm` | 4 | Doppler -> KillSoundOnProjectileImpact -> AttachToActor -> ... |
| 598 | AE_Weapon_Projectile_Rocket_Travel_84mm | `Audio.Event.Projectile.Rocket.Travel.84mm` | 3 | HandleProjectileSimulation -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_84mm_Preset) -> AttachToActor |
| 599 | AE_Weapon_Projectile_Rocket_Travel_93mm | `Audio.Event.Projectile.Rocket.Travel.93mm` | 3 | HandleProjectileSimulation -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_93mm_Preset) -> AttachToActor |
| 600 | AE_Weapon_Projectile_Rocket_Travel_Homing | `Audio.Event.Projectile.Rocket.Travel.Homing` | 2 | HandleProjectileSimulation -> HandleRocketWhizby(MSS_Weapon_Projectile_Flight_72mm_v2) |
| 601 | AE_Weapon_Projectile_Rocket_Travel_Mortar | `Audio.Event.Projectile.Rocket.Travel.Mortar` | 3 | HandleProjectileSimulation -> HandleRocketIncoming(MSS_Weapon_Projectile_Mortar_Incoming_Preset) -> AttachToActor |
| 602 | AE_Weapon_Projectile_Rocket_Travel_TGM_CBMActivate | `Audio.Event.Projectile.Rocket.Travel.TGM.CBMActivate` | 1 | HandleLocalCBM(AM_CBM_TGMFlight1p) |
| 603 | AE_Weapon_Projectile_Rocket_Travel_TGM_CBMDeactivate | `Audio.Event.Projectile.Rocket.Travel.TGM.CBMDeactivate` | 1 | HandleLocalCBM(AM_CBM_TGMFlight1p) |
| | **Weapon/Targeting** | | | |
| 604 | AE_Weapon_Targeting_IsFullLockedOnTo | `Audio.Event.Weapon.Targeting.IsFullLockedOnTo` | 2 | TriggerParam(str:Full Locked Start) -> PlaySound(MSS_Weapon_Targeting_LockOn_1p) |
| 605 | AE_Weapon_Targeting_IsLockedOnTo | `Audio.Event.Weapon.Targeting.IsLockedOnTo` | 3 | AttachToHeldItem -> TriggerParam(str:LockOn Start) -> PlaySound(MSS_Weapon_Targeting_LockOn_1p) |
| 606 | AE_Weapon_Targeting_IsLockedOnTo_Stop | `Audio.Event.Weapon.Targeting.IsLockedOnTo.Stop` | 2 | TriggerParam(str:Stop Sound) -> StopSound |
| | **Weapon/Throwable** | | | |
| 607 | AE_Throwable_Overhand | `Audio.Event.Weapon.Throwable.Overhand` | 3 | HeldItemPerspSound(tag:Audio.Asset.Item.Throw.OverHand.1p, Audio.Asset.Item.Throw.OverHand.3p) -> RequestVox(tag:Audio.Vox.Exertion.ThrowingGrenade.OverHand) -> AttachToA |
| 608 | AE_Throwable_Underhand | `Audio.Event.Weapon.Throwable.Underhand` | 2 | HeldItemPerspSound(tag:Audio.Asset.Item.Throw.UnderHand.1p, Audio.Asset.Item.Throw.UnderHand.3p) -> AttachToActor |
| | **Weapon/Throwable/Flashbang** | | | |
| 609 | AE_Weapon_Flashbang_Explosion | `Audio.Event.Weapon.Throwable.Flashbang.Explosion` | 4 | AttachToActor -> PlaySound -> XSetExecutionContextAbandonmentSettings -> ... |
| 610 | AE_Weapon_Flashbang_Impact | `Audio.Event.Weapon.Throwable.Flashbang.Impact` | 2 | AttachToActor -> PlaySound(MSS_Weapon_Throwable_Flashbang_Impact) |
| 611 | AE_Weapon_Flashbang_PinPull | `Audio.Event.Weapon.Throwable.Flashbang.PinPull` | 2 | HeldItemPerspSound(tag:Audio.Asset.Item.PinPull.1p, Audio.Asset.Item.PinPull.3p) -> AttachToActor |
| | **Weapon/Throwable/Grenade** | | | |
| 612 | AE_Weapon_Grenade_Explosion | `Audio.Event.Weapon.Throwable.Grenade.Explosion` | 4 | AttachToActor -> PlaySound(MSS_Weapon_Throwable_Grenade_Explosion_Preset) -> XSetExecutionContextAbandonmentSettings -> ... |
| 613 | AE_Weapon_Grenade_Impact | `Audio.Event.Weapon.Throwable.Grenade.Impact` | 2 | PlayThrowableImpactSound(MSS_Weapon_Throwable_Grenade_Impact) -> AttachToActor |
| 614 | AE_Weapon_Grenade_PinPull | `Audio.Event.Weapon.Throwable.Grenade.PinPull` | 2 | HeldItemPerspSound(tag:Audio.Asset.Item.PinPull.1p, Audio.Asset.Item.PinPull.3p) -> AttachToActor |
| 615 | AE_Weapon_Grenade_Primed | `Audio.Event.Weapon.Throwable.Grenade.Primed` | 2 | HeldItemPerspSound(tag:Audio.Asset.Item.Prime.1p, Audio.Asset.Item.Prime.3p) -> AttachToActor |
| | **World** | | | |
| 616 | AE_World_AudioGym_Enter | `Audio.Event.World.AudioGym.Enter` | 3 | ActivateCBM(AM_CBM_Main) -> CacheMetasoundOperators(/Game/Audio/Player/Movement/Footsteps/MSS/MSS_Footstep_MasterPreset.MSS_Footstep_MasterPreset, /Game/Audio/Wea) -> Dis |
| 617 | AE_World_AudioGym_Exit | `Audio.Event.World.AudioGym.Exit` | 5 | DiscardCachedMetasoundOperators(MSS_Footstep_MasterPreset, MSS_Weapon_Fire_3p_MasterPreset) -> EndBehavior -> DisableMusic(tag:Audio.Music.Death) -> ... |
| 618 | AE_World_Blackmarket_Enter | `Audio.Event.World.Blackmarket.Enter` | 0 |  |
| 619 | AE_World_Blackmarket_Exit | `Audio.Event.World.Blackmarket.Exit` | 3 | DeactivateCBM(AM_CBM_UIScene_PopUpWindow) -> DeactivateCBM(AM_CBM_UIScene_ContextDrawer) -> DeactivateCBM(AM_CBM_UIScene) |
| 620 | AE_World_Europe_Enter | `Audio.Event.World.Europe.Enter` | 3 | ActivateCBM(AM_CBM_Main) -> CacheMetasoundOperators(/Game/Audio/Player/Movement/Footsteps/MSS/MSS_Footstep_MasterPreset.MSS_Footstep_MasterPreset, /Game/Audio/Wea) -> Dea |
| 621 | AE_World_Europe_Exit | `Audio.Event.World.Europe.Exit` | 9 | DiscardCachedMetasoundOperators(MSS_Footstep_MasterPreset, MSS_Weapon_Fire_3p_MasterPreset) -> EndBehavior -> EndBehavior -> ... |
| 622 | AE_World_FrontEnd_Enter | `Audio.Event.World.FrontEnd.Enter` | 2 | ActivateCBM(AM_CBM_Main) -> DeactivateAllControlBusMix |
| 623 | AE_World_FrontEnd_Exit | `Audio.Event.World.FrontEnd.Exit` | 3 | DeactivateCBM(AM_CBM_UIScene_PopUpWindow) -> DeactivateCBM(AM_CBM_UIScene_ContextDrawer) -> DeactivateCBM(AM_CBM_UIScene) |
| 624 | AE_World_GymTDM_Enter | `Audio.Event.World.GymTDM.Enter` | 2 | ActivateCBM(AM_CBM_Main) -> DisableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| 625 | AE_World_GymTDM_Exit | `Audio.Event.World.GymTDM.Exit` | 0 |  |
| 626 | AE_World_Kavkazi_Enter | `Audio.Event.World.Kavkazi.Enter` | 3 | ActivateCBM(AM_CBM_Main) -> CacheMetasoundOperators(/Game/Audio/Player/Movement/Footsteps/MSS/MSS_Footstep_MasterPreset.MSS_Footstep_MasterPreset, /Game/Audio/Wea) -> Dea |
| 627 | AE_World_Kavkazi_Exit | `Audio.Event.World.Kavkazi.Exit` | 9 | DiscardCachedMetasoundOperators(MSS_Footstep_MasterPreset, MSS_Weapon_Fire_3p_MasterPreset, MSS_Player_Whizby_Master, MSS_Player_Movement_Foot) -> EndBehavior -> EndBehav |
| 628 | AE_World_NorthAmerica_Enter | `Audio.Event.World.NorthAmerica.Enter` | 3 | ActivateCBM(AM_CBM_Main) -> CacheMetasoundOperators(/Game/Audio/Player/Movement/Footsteps/MSS/MSS_Footstep_MasterPreset.MSS_Footstep_MasterPreset, /Game/Audio/Wea) -> Dea |
| 629 | AE_World_NorthAmerica_Exit | `Audio.Event.World.NorthAmerica.Exit` | 9 | DiscardCachedMetasoundOperators(MSS_Footstep_MasterPreset, MSS_Weapon_Fire_3p_MasterPreset, MSS_Player_Whizby_Master, MSS_Player_Movement_Foot) -> EndBehavior -> EndBehav |
| 630 | AE_World_Russia_Enter | `Audio.Event.World.Russia.Enter` | 3 | ActivateCBM(AM_CBM_Main) -> CacheMetasoundOperators(/Game/Audio/Player/Movement/Footsteps/MSS/MSS_Footstep_MasterPreset.MSS_Footstep_MasterPreset, /Game/Audio/Wea) -> Dea |
| 631 | AE_World_Russia_Exit | `Audio.Event.World.Russia.Exit` | 9 | DiscardCachedMetasoundOperators(MSS_Footstep_MasterPreset, MSS_Weapon_Fire_3p_MasterPreset, MSS_Player_Whizby_Master, MSS_Player_Movement_Foot) -> EndBehavior -> EndBehav |
| 632 | AE_World_ShootingRange_Enter | `Audio.Event.World.ShootingRange.Enter` | 3 | ActivateCBM(AM_CBM_Main) -> DeactivateCBM(AM_CBM_UIScene_PopUpWindow) -> DisableMusic(tag:Audio.Music.FrontEnd.MainMenu) |
| 633 | AE_World_ShootingRange_Exit | `Audio.Event.World.ShootingRange.Exit` | 0 |  |
| | **Added in Season 02 (2026-10-15)** | | | |
| 634 | AE_Helmet_Pilot_Active_Start | `Audio.Event.Player.State.Helmet.Pilot.Active.Start` | 1 | ActivateCBM(Am_CBM_Pilot_Helmet_Active) |
| 635 | AE_Helmet_Pilot_Active_Stop | `Audio.Event.Player.State.Helmet.Pilot.Active.Stop` | 1 | DeactivateCBM(Am_CBM_Pilot_Helmet_Active) |
| 636 | AE_Helmet_Pilot_Passive_Start | `Audio.Event.Player.State.Helmet.Pilot.Passive.Start` | 1 | ActivateCBM(Am_CBM_Pilot_Helmet_Passive) |
| 637 | AE_Helmet_Pilot_Passive_Stop | `Audio.Event.Player.State.Helmet.Pilot.Passive.Stop` | 1 | DeactivateCBM(Am_CBM_Pilot_Helmet_Passive) |
| 638 | AE_Helmet_SuperHeavy_Start | `Audio.Event.Player.State.Helmet.SuperHeavy.Start` | 1 | ActivateCBM(AM_CBM_Helmet_SuperHeavy) |
| 639 | AE_Helmet_SuperHeavy_Stop | `Audio.Event.Player.State.Helmet.SuperHeavy.Stop` | 1 | DeactivateCBM(AM_CBM_Helmet_SuperHeavy) |
| 640 | AE_Helmet_Tanker_Active_Start | `Audio.Event.Player.State.Helmet.Tank.Active.Start` | 1 | ActivateCBM(Am_CBM_Tanker_Helmet_Active) |
| 641 | AE_Helmet_Tanker_Active_Stop | `Audio.Event.Player.State.Helmet.Tank.Active.Stop` | 1 | ActivateCBM(Am_CBM_Tanker_Helmet_Active) |
| 642 | AE_Helmet_Tanker_Passive_Start | `Audio.Event.Player.State.Helmet.Tank.Passive.Start` | 1 | ActivateCBM(Am_CBM_Tanker_Helmet_Passive) |
| 643 | AE_Helmet_Tanker_Passive_Stop | `Audio.Event.Player.State.Helmet.Tank.Passive.Stop` | 1 | DeactivateCBM(Am_CBM_Tanker_Helmet_Passive) |
| 644 | AE_Player_Movement_Looting_Start | `Audio.Event.Player.Looting` | 3 | PlayPerspectiveSound_HostilityAware -> AttachToActor -> TriggerParam(str:Trigger) |
| 645 | AE_Player_Movement_Looting_Stop | `Audio.Event.Player.Looting.Stop` | 1 | TriggerParam(str:Stop) |
| 646 | AE_Prop_Soccer_Ball_Bounce_Hard | `Audio.Event.Prop.Ball.Bounce.Hard` | 3 | SendRawMagnitudeToMSS -> AttachToActor -> PlaySound(MSS_Soccer_Ball_Bounce_Hard) |
| 647 | AE_Prop_Soccer_Ball_Bounce_Soft | `Audio.Event.Prop.Ball.Bounce.Soft` | 3 | SendRawMagnitudeToMSS -> AttachToActor -> PlaySound(MSS_Soccer_Ball_Bounce_Soft) |
| 648 | AE_Prop_Soccer_Ball_Hit | `Audio.Event.Prop.Ball.Hit` | 3 | SendRawMagnitudeToMSS -> AttachToActor -> PlaySound(MSS_Soccer_Ball_Hit) |
| 649 | AE_Prop_Soccer_Ball_Reset | `Audio.Event.Prop.Ball.Reset` | 2 | AttachToActor -> PlaySound(MSS_Soccer_New_Match) |
| 650 | AE_Prop_Soccer_Goal | `Audio.Event.Prop.Ball.Goal` | 2 | PlaySound(MSS_Soccer_Goal) -> WDMoveSoundToGameplayCueLocation |
| 651 | AE_UI_InGame_Vendor_Rebuy | `Audio.Event.UI.Vendor.Rebuy` | 1 | PlaySound(MSS_UI_Vendor_Rebuy) |
| 652 | AE_UI_InGame_Vendor_Wager_Action | `Audio.Event.UI.InGame.Vendor.Wager.Action` | 1 | PlaySound(MSS_UI_InGame_Vendor_Wager_Action) |
| 653 | AE_UI_InGame_Vendor_Wager_Bet_Made | `Audio.Event.UI.InGame.Vendor.Wager.Bet.Made` | 1 | PlaySound(MSS_UI_InGame_Vendor_Wager_Bet_Made) |
| 654 | AE_UI_InGame_Vendor_Wager_Close | `Audio.Event.UI.InGame.Vendor.Wager.Close` | 2 | DeactivateCBM(AM_CBM_UIScene_Vendor) -> PlaySound(MSS_UI_Vendor_Vehicle_Close) |
| 655 | AE_UI_InGame_Vendor_Wager_Create_New | `Audio.Event.UI.InGame.Vendor.Wager.Create.New` | 1 | PlaySound(MSS_UI_InGame_Vendor_Wager_Create_New) |
| 656 | AE_UI_InGame_Vendor_Wager_Increment_Down | `Audio.Event.UI.InGame.Vendor.Wager.Increment.Down` | 1 | PlaySound(MSS_UI_InGame_Vendor_Wager_Increment_Down) |
| 657 | AE_UI_InGame_Vendor_Wager_Increment_Up | `Audio.Event.UI.InGame.Vendor.Wager.Increment.Up` | 1 | PlaySound(MSS_UI_InGame_Vendor_Wager_Increment_Up) |
| 658 | AE_UI_InGame_Vendor_Wager_Objective_Added | `Audio.Event.UI.InGame.Vendor.Wager.Objective.Added` | 1 | PlaySound(MSS_UI_InGame_Vendor_Wager_Objective_Added) |
| 659 | AE_UI_InGame_Vendor_Wager_Open | `Audio.Event.UI.InGame.Vendor.Wager.Open` | 2 | ActivateCBM(AM_CBM_UIScene_Vendor) -> PlaySound(MSS_UI_Vendor_Vehicle_Open) |
| 660 | AE_UI_InGame_Seeding_RewardReason_Potato | `Audio.Event.UI.InGame.ServerSeeding.RewardReason.Potato` | 1 | PlaySound(MSS_UI_InGame_Seeding_Reward) |
| 661 | AE_UI_InGame_Seeding_RewardReason_Shooting | `Audio.Event.UI.InGame.ServerSeeding.RewardReason.Shooting` | 1 | PlaySound(MSS_UI_InGame_Seeding_Reward_Shooting) |
| 662 | AE_UI_InGame_Seeding_RewardReason_Soccer | `Audio.Event.UI.InGame.ServerSeeding.RewardReason.Soccer` | 1 | PlaySound(MSS_UI_InGame_Seeding_Reward) |
| 663 | AE_Vehicle_Shared_Wiper_Stroke | `Audio.Event.Vehicle.Shared.Wiper.Stroke` | 3 | PlaySound(MSS_Vehicle_Shared_Wipers) -> AttachSoundToActor -> SetWiperParameters |
| 664 | AE_Vehicle_Shared_Windscreen_Wipers | `Audio.Event.Vehicle.Shared.Weapon` | 2 | SetAudioParameters -> AttachToActor |
| 665 | AE_Vendor_Wager_Greeting_Bye_BigBet | `Audio.Event.Vendor.Wager.Greeting.Bye.BigBet` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Wager_Greeting_Bye_BigBet_Preset) |
| 666 | AE_Vendor_Wager_Greeting_Bye_NoBet | `Audio.Event.Vendor.Wager.Greeting.Bye.NoBet` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Wager_Greeting_Bye_NoBet_Preset) |
| 667 | AE_Vendor_Wager_Greeting_Bye_SmallBet | `Audio.Event.Vendor.Wager.Greeting.Bye.SmallBet` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Wager_Greeting_Bye_SmallBet_Preset) |
| 668 | AE_Vendor_Wager_Greeting_Hello_Base | `Audio.Event.Vendor.Wager.Greeting.Hello.Base` | 2 | AttachToActor -> PlaySound(MSS_Vendor_Wager_Greeting_Hello_Base_Preset) |
| 669 | AE_Vendor_Wager_Result_Fail_Death | `Audio.Event.Vendor.Wager.Result.Fail.Death` | 2 | PlaySoundDelayed -> PlaySound(MSS_UI_InGame_Vendor_Wager_Failure) |
| 670 | AE_Vendor_Wager_Result_Fail_Time | `Audio.Event.Vendor.Wager.Result.Fail.Time` | 2 | PlaySoundDelayed -> PlaySound(MSS_UI_InGame_Vendor_Wager_Failure) |
| 671 | AE_Vendor_Wager_Result_Jackpot | `Audio.Event.Vendor.Wager.Result.Jackpot` | 2 | PlaySoundDelayed -> PlaySound(MSS_UI_InGame_Vendor_Wager_Jackpot) |
| 672 | AE_Vendor_Wager_Result_Win | `Audio.Event.Vendor.Wager.Result.Success` | 2 | PlaySoundDelayed -> PlaySound(MSS_UI_InGame_Vendor_Wager_Success) |
| 673 | AE_Weapon_Vehicle_ADSIn | `Audio.Event.Vehicle.Shared.Weapon.ADSIn` | 3 | ActivateCBM(AM_CBM_ADS) -> PlayVehicleWeaponPerspectiveSound -> AttachToActor |
| 674 | AE_Weapon_Vehicle_ADSOut | `Audio.Event.Vehicle.Shared.Weapon.ADSOut` | 4 | DeactivateCBM(AM_CBM_ADS) -> PlayVehicleWeaponPerspectiveSound -> AttachToActor -> ... |
| 675 | AE_Weapon_Projectile_Rocket_Travel_125mm | `Audio.Event.Projectile.Rocket.Travel.125mm` | 3 | HandleProjectileSimulation -> HandleRocketWhizby -> AttachToActor |

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | `data/` re-exported with the v2 usmap (names only; values unchanged): the unresolved float key is now `_aaabhgndclheajnnlnade`. |
| 2026-10-18 | Round-7 correction: the 222-instance float is the property `_aaabhgndclheajnnlnade`, not the `HandlePlaySound` parameter (different token length). |
