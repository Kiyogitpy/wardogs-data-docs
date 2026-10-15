---
title: "FlyByManager (feature)"
parent: "Game Features"
---

# Wardogs — FlyByManager Game Feature Reference (v2)
*Extracted from cooked game data ([`Wardogs/Plugins/GameFeatures/FlyByManager`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/FlyByManager), 6 JSON files, all parsed). Build `++Wardogs+Live-CL-509546`, UE 5.7.*

> **What this is:** the jet fly-by audio plugin. It has **no numeric gameplay data**. It registers gameplay cue and world-partition content, and defines six Crosstalk audio events for two jet types (Jet_01, Jet_02): a moving loop with a Doppler behaviour, a weapon-fire one-shot, and stop events.

---

## 1. Plugin Inventory

| Asset | Type | Role |
|---|---|---|
| [`Content/FlyByManager`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/FlyByManager.json) | `GameFeatureData` + 2 actions | Plugin root |
| [`Content/Audio/Jet_01/Events/AE_Jet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_01/Events/AE_Jet.json) | `CrosstalkAudioEvent` (+ `AEB_Doppler_C` behaviour) | Jet_01 moving loop |
| [`Content/Audio/Jet_01/Events/AE_Jet_Fire`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_01/Events/AE_Jet_Fire.json) | `CrosstalkAudioEvent` | Jet_01 weapon fire |
| [`Content/Audio/Jet_01/Events/AE_Jet_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_01/Events/AE_Jet_Stop.json) | `CrosstalkAudioEvent` | Jet_01 moving stop |
| [`Content/Audio/Jet_02/Events/AE_Jet02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_02/Events/AE_Jet02.json) | `CrosstalkAudioEvent` | Jet_02 moving loop |
| [`Content/Audio/Jet_02/Events/AE_Jet02_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_02/Events/AE_Jet02_Stop.json) | `CrosstalkAudioEvent` | Jet_02 moving stop |

---

## 2. Plugin Root ([`FlyByManager`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/FlyByManager.json))

| Action | Setting |
|---|---|
| `BHGameFeatureAction_AddGameplayCuePath` | Adds gameplay cue directory `/FlyByManager/GameplayCues` |
| `GameFeatureAction_AddWorldPartitionContent` | External data layer `EDL_FlyBy` (`/FlyByManager/DataLayers/EDL_FlyBy`) |

The root's `PrimaryAssetTypesToScan` was not extracted.

---

## 3. Audio Events

Each `CrosstalkAudioEvent` is a list of behaviours. The name tag is the event the game triggers by name.

### 3a. Jet_01

| Event | Name tag | Behaviours (in order) | Sound | Restart | Context tag |
|---|---|---|---|---|---|
| [`AE_Jet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_01/Events/AE_Jet.json) | none | `AEB_Doppler_C` (Doppler behaviour, `/Game/Audio/Behaviours/AEB_Doppler`); `AttachSoundToActor`; `PlaySound` | `MSS_Vehicles_Jet` (`/FlyByManager/Audio/Jet_01/MSS_Vehicles_Jet`) | `ESoundRestartBehavior::Always` | `Audio.Context.Vehicle.Moving` |
| [`AE_Jet_Fire`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_01/Events/AE_Jet_Fire.json) | `Audio.Event.Vehicle.Jet.Fire` | `AttachSoundToActor`; `PlaySound` | `MSS_Vehicles_Jet_Firing` | none set | `Audio.Context.Vehicle.Weapon.Fire` |
| [`AE_Jet_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_01/Events/AE_Jet_Stop.json) | `Audio.Event.Vehicle.Jet.Moving.Stop` | `StopSound` | (stops the moving loop) | n/a | `Audio.Context.Vehicle.Moving` |

### 3b. Jet_02

| Event | Name tag | Behaviours (in order) | Sound | Restart | Context tag |
|---|---|---|---|---|---|
| [`AE_Jet02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_02/Events/AE_Jet02.json) | `Audio.Event.Vehicle.Jet02.Moving` | `AttachSoundToActor`; `PlaySound` | `MSS_Vehicles_Jet_02` (`/FlyByManager/Audio/Jet_02/MSS_Vehicles_Jet_02`) | `ESoundRestartBehavior::Always` | `Audio.Context.Vehicle.Moving` |
| [`AE_Jet02_Stop`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FlyByManager/Content/Audio/Jet_02/Events/AE_Jet02_Stop.json) | `Audio.Event.Vehicle.Jet02.Moving.Stop` | `StopSound` | (stops the moving loop) | n/a | `Audio.Context.Vehicle.Moving` |

Note the asymmetry: Jet_01 has a dedicated fire event and a Doppler behaviour. Jet_02 has neither in this export.

---

## 4. How They Work Together

- **Moving:** the moving event attaches a `MetaSoundSource` to the jet actor and plays it under the `Audio.Context.Vehicle.Moving` context. The stop event carries the same context, which suggests it halts that loop (inferred from the shared tag, not from an explicit sound reference). The Jet_01 version also runs the Doppler behaviour; its effect is not in this export.
- **Firing:** Jet_01 plays its fire MetaSound under the weapon-fire context, separate from the moving loop.
- The event name tags are how the game code requests a sound; the context tags group sounds so the stop events can find the right loop.

---

## 5. Still Not Pulled / Limitations

- **No numeric data.** This plugin holds no speeds, altitudes, volumes or timings.
- **Doppler parameters** live in the `AEB_Doppler` blueprint (`/Game/Audio/Behaviours/AEB_Doppler`), which is outside this plugin. Its settings were not extracted.
- **MetaSound contents** (`MSS_Vehicles_Jet`, `MSS_Vehicles_Jet_Firing`, `MSS_Vehicles_Jet_02`) are referenced by path. Their internal parameters are not in the dump.
- **Trigger call sites** (which game code fires `Audio.Event.Vehicle.Jet.Fire` and the Jet02 events, and when) are not in this plugin.
- **Stop-sound targets** are inferred from the context tag, not from an explicit sound reference, since the stop behaviour has no sound field.
