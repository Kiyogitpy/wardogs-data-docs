---
title: Round 42 modes, AI and other gaps
nav_exclude: true
---

# Round 42: AI alert/firing/hearing, spawn volumes and the open "Other" rows (RE42-MODES)

Continues [round 41](round41-modes-ai-other.md). Static CL516586 review plus cooked-data reads; nothing was run. Native RVAs are for `WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10...0cc37`), read from the decompiled corpus (`corpus.sqlite`) and, where the decompiler hid an operand, from the disassembly of the same bytes. No devirtualization. Scratch output: `E:/Reverse_Engineer/wardogs_analysis/round42_modes/` (`sv` spawn-volume packages, 1.0 GB; `ex` explosion cues; `k` animation blueprints; `n*` name-map searches).

Statuses: FOUND, NATIVE (open, with the exact next step), SERVER, ABSENT (where searched), PROTECTED (none this round). Evidence: *data* (cooked asset read), *static* (decompiled code read, not run), *config*, *SDK* (Dumper-7 headers).

Machine-readable result (idempotent, `python -I`; `--check` compares with the committed file): `_tools/r42_modes_data.py` -> `assets/data/r42-modes.json` (alert rule, firing flag, vehicle noise defaults, significance rules, 110 spawn volumes with positions, explosion-sequence map, Kawaii settings, 40 water grids against their flux states, arm class per projectile, streaming pools).

## Rows

Each open round-41 row got its own time budget, in player-value order.

| # | Status | Item | Result |
|---|---|---|---|
| 1 | FOUND (static + data) | How AI alert thresholds read the detection level | See R1. |
| 2 | FOUND (static) | The "is firing" test | See R2. |
| 3a | FOUND (static + data) | Vehicle noise ranges for AI hearing | `UBHBaseVehicleConfigDataAsset` constructor `0x5300B10` sets `AIEngineLoudnessMaxRange` 10,000, `AIHornLoudnessMaxRange` 50,000 and `AIVehicleDestroyedLoudnessMaxRange` 80,000 (cm: 100 m, 500 m, 800 m). No cooked asset overrides them (the string `LoudnessMaxRange` appears in no exported data file and in no package name map). |
| 3b | NATIVE | Which events create hearing stimuli | See R3. The emitters were not located. |
| 4a | FOUND (data) | Where the spawn volumes are | See R4: 110 `WDSpawnVolume` actors in 5 worlds. Positions in `r42-modes.json`. |
| 4b | NATIVE | Which volume the King of the Hill first spawn actually picks | See R4. Only 4 volumes carry no vehicle list. |
| 5 | FOUND (data) | Explosion timing mapping (which sequence fires for what) | See R5. |
| 6a | FOUND (data) | Kawaii physics settings (characters) | See R6. The round-41 note "stiffness and damping are not in these assets" is wrong: they are in the animation blueprints. |
| 6b | FOUND (config) | Streaming budget | See R6. |
| 7 | FOUND (data) | Achievement thresholds | Already done in [round 36 economy](round36-econ.md) section 2 (4 thresholds, criteria for all 10); the round-41 row "not worked" was a cross-reference miss. No new work. |
| 8 | NATIVE | Hashed `_aaa` property names (2,645) | See R8. |
| 9 | NATIVE | Water-grid sampler (`0x6F77240` loader) | See R9: sampler not located; the two doubles are almost certainly a Z range. |
| 10a | FOUND (data, inferred) | Flux state `Iteration` | See R10. |
| 10b | NATIVE | Flux shader and channel packing | See R10. |
| 11 | FOUND (static) | Significance rule order | See R11. |
| 12 | FOUND (data + static) | Units (weight, mass, speed) | Weight: the HUD formats it as `{Weight}kg` (string table keys `Text.Weight.Kilograms`, `TooltipItem.Header.Weight.Formatting`), so the item `Weight` values (0.08 to 42.0) are kilograms. Speed in cm/s and mass in kg: [Projectile Flight section 9](../../pipelines/Wardogs_ProjectileFlight_v1.md#9-units) (unchanged). The vehicle `Mass override` 10,000 is a physics mass and is in kg by the engine's convention (not separately checked). |
| 13 | FOUND (data) | Arm class (`Meta.Damage.Arms.*`) | See R13. |
| 14 | FOUND (cross-ref) | `Percentage_Ongoing` in the damage pipeline (round-41 row 6.9 open part) | Decoded in [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md) (non-custom operation: `(Amount x 0.01) x C`). Nothing open. |

## R1. How AI alert thresholds read the detection level

Status FOUND. `UWDAIAlertStateComponent` virtual slot 131 (`0x887C140`, tick) recomputes the alert state; the setter is `0x887C000` (writes the byte at `+256`, bumps a version counter, then notifies listeners: the alert-state decorator of the behaviour tree).

Per tick:

1. `level` = the larger of (a) the highest detection level (the float at `+4` of each 48-byte entry) among the AI's own perceived targets, and (b) the value returned by `0x8870590`, which is the highest such level among the allied AIs it iterates (a set at `+752` of the other component, skipping the AI that owns the query). So an AI becomes alert from its own detection **or from the detection of its group**.
2. Walk `AlertStatesWithThreashold` (asset [`AlertStateThreashold_DataConfig`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DataAssets/AlertStateThreashold_DataConfig.json): Relaxed 0.0, Alert 0.8, Combat 1.0) in file order. An entry passes when `level >= LowerThreshold` and, if its sight flag applies, the **sight strength of the current target** (the per-entry float at `+12`, absolute value) is above **0.0001**. The sight flag is `bRequireSightToTransitionFromHigher` when the current state is at or above the candidate, `bRequireSightToTransitionFromLower` otherwise.
3. The walk stops at the first entry that fails; the state is the last passing entry (Relaxed when none passes). The state is applied every tick, so there is no timer and no hysteresis other than the sight flag.

With the shipped asset: Alert is reached at level 0.8 with no sight needed (hearing or a squad-mate's detection is enough); Combat needs level 1.0 **and** current sight on the target when rising; once in Combat it stays while the level holds 1.0 (no sight needed when falling, flag false). The level itself falls by 0.25 per second after 5 s without update (round 41), so a Combat AI leaves Combat as soon as the level drops below 1.0, then Alert below 0.8. Constants and rule text are in `r42-modes.json` (`static.alert_state_update`).

## R2. The "is firing" test

Status FOUND. The test reads one byte of the **target's `UWDWeaponComponent`** at `+0xFE1` (`0x6B96BF0`; the same byte is returned by the Blueprint getter `IsCurrentlyFiring`, `0x6B99300`, and by the automation function `IsWeaponFiring`, `0x6AEA4E0`). AI hearing (`0x8870350`) fetches the target character's weapon component through the character's component getter (vtable offset 1848) and applies `WeaponFiring x WeaponFiringMultiplier` (5.0) while the byte is set. A second variant (`0x6B96C00`, `0x6B99320`) also requires the byte at `+0xFEC` to be above 0 (not used by the AI). The byte is set (word `0x0101` at `+0xFE1`) by slot 175 (`0x6B980A0`, start of a firing sequence) and cleared by slot 176 (`0x6B98560`) and the failure path of `0x6B980A0`. So "firing" is the weapon component's active firing-sequence flag, not ammo or trigger state alone.

## R3. Which events create hearing stimuli

Status NATIVE (open); sub-result 3a FOUND above.

Searched:

- Cooked packages: `findname` over every package (`Wardogs` and [`Wardogs/Plugins`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins)) for `ReportNoiseEvent`, `MakeNoise`, `PawnNoiseEmitter`, `AINoiseEvent`, `AISense_Hearing`, `LoudnessMaxRange`, `AIHornLoudness`: **0 packages**. No Blueprint, gameplay cue or data asset reports noise by name; the only hit class is `BP_CoreAIController`, which holds the sense *configs* (`AISenseConfig_Hearing`, `_Sight`, `_Damage`).
- Native: the static `UAISense_Hearing::ReportNoiseEvent` body is `0x4889724` (queues a 64-byte event); its only caller is its own Blueprint thunk (`0x4895130`). `UAISense_Damage::ReportDamageEvent` is `0x48894E0`, called from `0x6B17760` (the damage path), which is the 1.0 damage stimulus of round 41. No other function in the game range contains the event-queue code (constant `2112` with the queue growth helper `0x1565910` and `0x14181BFC0`).
- Config fields: the vehicle config assets carry the three AI loudness ranges of row 3a, so engine, horn and vehicle-destroyed noises exist as concepts, but the code reading `+0x2A0..+0x2A8` of the vehicle config was not found (a text search over the decompiled corpus matches far too many `+672` offsets).

Next step: break on writes to the AI noise queue by looking up engine-internal paths (`AActor::MakeNoise` -> `UPawnNoiseEmitterComponent`, vtable `0xA3F5B20`) and find the vehicle component that reads the three ranges, using xrefs to the vehicle config class getter. Note that the hearing strength formula of round 41 (R2 above) reads the target's firing flag and movement directly, so whether a gunshot also creates a separate noise event is not known.

## R4. Spawn volumes

Status 4a FOUND (data); 4b NATIVE.

Method: `WdExtract findname Wardogs WDSpawnVolume` lists the 61 packages whose name map holds the class (the 5 world packages plus 56 World Partition `_Generated_` cells); `dump` of those 61 packages (1.0 GB). There are **110** `WDSpawnVolume` actors, no duplicates between the world package and its cells. Other classes with "SpawnVolume" in the name: `B_ShootingRangeSpawnVolume` (a Blueprint, tutorial) and the `ScenarioExample` scenario; no Blueprint creates a `WDSpawnVolume` at run time (no other package names it).

| World | Alpha | Bravo | Charlie | With no vehicle list (player-type) |
|---|---|---|---|---|
| Europe | 10 | 15 | 16 | 0 |
| Kavkazi | 11 | 8 | 15 + 1 | **1** (Charlie) |
| NorthAmerica | 5 | 5 | 6 | 0 |
| Russia | 5 | 5 | 5 | 0 |
| Gym_Minimal | 1 | 1 | 1 | 3 |

Almost all volumes have `AllowedObjectsToSpawn` set to vehicle variant tags (for example `Vehicle.Variant.Land.Tracked.SpawnVehicle.Lonestar`, `Vehicle.Variant.Air`): they belong to **vehicle deployment boards** (each cell holds a `B_VehicleDeploymentBoard_*_C`, a `B_SpawnManager_C` and `TargetPoint` actors; `HorizontalSpacing` 1200 or 2500, `MaxSpawnPoints` 0 or 15). Only four volumes have no vehicle list:

| Where | Faction | Location (X, Y, Z) | Max points | Spacing H / V |
|---|---|---|---|---|
| Kavkazi (cell `6R0UAIQ0ULMW77RFELQNR28PU`) | Charlie | -1,241,132 / -973,957 / -93,696 | 15 | 2500 / 2500 |
| Gym_Minimal | Alpha | -1,555 / -1,878 / 320 | 15 | 1200 / 1200 (`SpawnPointOffsetZ` set) |
| Gym_Minimal | Bravo | -1,543 / 1,789 / 320 | 15 | 1200 / 1200 |
| Gym_Minimal | Charlie | 2,112 / -10 / 320 | 15 | 1200 / 1200 |

Coordinates are the actor root component's relative location in cm (World Partition cells are not offset, so these are world coordinates). All 110 positions, the point lists and the allowed vehicle tags are in `r42-modes.json` (`spawn_volumes`).

4b: the first-spawn route of round 41 (R1) searches the holder array for the first volume whose `FactionTag` (`+0x2F0`, an FName compare, `0x6D76F90`) equals the player's faction and does **not** test the vehicle list. In the Europe, North America and Russia worlds no player-type volume exists, so the volume that matched can only be one of the vehicle-board volumes (or the holder is filled by something not in the cooked level). This is not decided. Next step: find the writers of owner `+0x560` (the volume array) and the code that fills it (look for `GetAllActorsOfClass` of the volume class near `0x6D956D0` callers), and check whether KOTH uses the 'player-type' volume only in Kavkazi.

## R5. Explosion sequence mapping

Status FOUND (data). Sources: `GC_Vehicle_Destroyed` (`TagsToExplosionSequence`), `BP_Explosions` (`TagToExplosionSequence`), `GC_IED_Explode`, `GC_FOB_DamageStateChanged` (name maps).

| Trigger | Sequence |
|---|---|
| Vehicle destroyed `ROT_01`, [`ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/ROT_04.json) | [`DA_HelicopterExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_HelicopterExplosionSequence.json) |
| [`ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/ROT_02.json) | [`DA_HavocExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_HavocExplosionSequence.json) |
| [`ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/ROT_03.json) | [`DA_LittlebirdExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_LittlebirdExplosionSequence.json) |
| `PZH2000`, `FWG_01` | [`DA_TankExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_TankExplosionSequence.json) |
| [`WHL_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/WHL_02.json), [`WHL_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/WHL_05.json), [`WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/WHL_08.json) | [`DA_KodiakExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_KodiakExplosionSequence.json) |
| [`WHL_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/WHL_06.json) | [`DA_DuneBuggyExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_DuneBuggyExplosionSequence.json) |
| [`WHL_07`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/WHL_07.json) | [`DA_UralExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_UralExplosionSequence.json) |
| [`STN_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/STN_01.json), [`STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/STN_02.json), [`STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/STN_03.json), [`STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/STN_04.json) | `DA_STN01_Misteral_`, `DA_STN02_Phalanx_`, `DA_STN03_Mortar_`, [`DA_STN04_Loudspeaker_ExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_STN04_Loudspeaker_ExplosionSequence.json) |
| 155 mm shell, Standard and Expensive | [`DA_155mmExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_155mmExplosionSequence.json) |
| IED (`GameplayCue.IED.Explode`) | [`DA_IEDExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_IEDExplosionSequence.json) |
| FOB destroyed (`GameplayCue.FOB.DamageStateChanged`) | [`DA_FOBDestroyed_ExplosionSequence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Explosions/Blueprints/Sequence/DA_FOBDestroyed_ExplosionSequence.json) |

All 14 sequences are used. Vehicles with no tag here (for example [`WHL_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/WHL_01.json), `TNK_*`, `STN_05/06`) get a single recipe from `BP_Explosions.ExplosionSettings` (or none: [`WHL_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/WHL_02.json), [`ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/ROT_03.json) and `PZH2000` have a null recipe there because they use a sequence). The sequence entries (recipe, time, offset) are in the [VFX page](../../content/Wardogs_VFX_v2.md) section 3.

## R6. Characters

Status FOUND.

- **Kawaii physics** (animation blueprint nodes, dump `k/`): the two ghillie post-process blueprints use `Damping` 0.25, `Stiffness` 0.1, `WorldDampingLocation` 1.0, `WorldDampingRotation` 1.0, `LimitAngle` 40, `BoneForwardAxis` X+, component space, 60 Hz target; armour `Radius` 7.0 with 21 extra root chains (22 in total, root `ghille_dyn_back_l_A1`), head `Radius` 5.0 with 11 extra chains (root `ghille_dyn_head_r_A1`). Teleport reset beyond 300 cm or 10 degrees. The six bobblehead blueprints (`ABP_Bobblehead_000_Lonestar`, `_001_VK`, `_003`, `_004`, `_005`, `_MT_002`) use `Damping` 0, `Stiffness` 0.1, `Radius` 1, base-bone space, `LimitAngle` 20 (60 on `_004`), `WorldDampingLocation` 1.0 (2.0 on the `_005` base chain, 0.1 on the `_003` eye chain), `WorldDampingRotation` 0.2 (0.8 on the `_003` eye chain, 0.1 on the `_005` base chain). Curves are empty. Full table: `r42-modes.json` (`kawaii_physics`, 11 nodes).
- **Streaming budget**: no per-asset budget exists in the LOD asset (confirmed). The budget is global config: texture streaming pool by `TextureQuality` scalability level 0/1/2/3 = 1,280 / 2,048 / 3,072 / 6,144 MB (Cine 310 MB), `r.MeshStreaming=True`, Nanite streaming pool 256 MB (`DefaultEngine.ini`; 512 MB on the console device profiles).

## R8. Hashed property names

Status NATIVE (open). Round 12 section 5 stands: the hash is not FNV-1/1a, djb2, sdbm, MurmurHash64A or XXH64 and only real names from the build's own data can name a token. Not newly resolved this round. Exact next steps, in value order: (1) read serialized `UserDefinedStruct` / `UserDefinedEnum` exports (cooked row structs keep real field names, unlike the usmap) and match by owner, slot and kind as round 12 did for Blueprint classes; (2) test the 31,815 known token/name pairs against CityHash64, SipHash, xxHash3, wyhash, CRC64 and Murmur3-128 (round 12 tried six functions only); (3) native `FArrayPropertyParams` name tables by class offset.

## R9. Water height grid sampler

Status NATIVE (open); structure FOUND.

- The grid list is owned by `UWDWaterHeightSubsystem` (SDK `0x48` array; vtable `0xB29DFB0`). Its vtable overrides only the destructor and slot 91 (`0x6F77240`, the loader that fills `+72`); every other slot is the base. The sampler is therefore a non-virtual member and is not Blueprint-exposed (no function of the class in the SDK), so it was not reached from the vtable.
- The two doubles (`+0x58`, `+0x60`) are very likely a **Z range**: in all 40 grids the second is above the first by 855 to 4,475 cm, both sit below the linked flux state's `AreaLocation.Z`, the second is always below it, and both are of the same order as the state's `CaptureOffset` (for example [`PDA_Europe_0000`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Water/FluidFlux/Europe/PDA_Europe_0000.json): -97,173.6 and -94,622.6; state `AreaLocation.Z` -94,178.6, `CaptureOffset` -96,428.6). The samples are 16-bit; 65,535 is the most common value in every grid (56,018 of 65,536 in `Europe_0000`), consistent with "no water" or the upper end of the range. Mapping `height = lo + sample/65535 x (hi - lo)` is a hypothesis, not read from code.
- Grid geometry (data): `worldmin` = state `AreaLocation` minus half of `AreaSize` in X and Y for **40 of 40** grids; `WorldSize` equals the state's X and Y area size; cell size is 200 cm (512 x 128 grid over 102,400 x 25,600 cm).

Next step: find the callers of the subsystem (its class getter) and the accessor that indexes `a1+72` with `worldmin`, `WorldSize` and the grid width/height (`0x50`/`0x54`), then read the use of `+0x58`/`+0x60`.

## R10. Fluid Flux

- 10a FOUND (data, inferred). Every flux state also stores `IterationDeltaTime`: **0.18 s in all 40 states that have a grid** (field already in the cooked states). `Iteration` (23,813 to 1,261,732) is therefore a count of simulation steps at the capture, by its pairing with the step time; it is not a version or frame counter. Simulated time is `Iteration x 0.18` s (about 4,300 s for the smallest, 227,000 s for the largest). The plugin code is not in the client, so the inference rests on the field pair. `Resolution` is 2048 x 512 for the 102,400 x 25,600 cm area (the height grid is one quarter per axis).
- 10b NATIVE. Channels: `GroundMap`, `VelocityDepthFoamMap` (velocity, depth and foam packed in one map; velocity encoded against `EncodeVelocityMax` 5.0), `HeightWetMap` (height against `EncodeHeightMax` 256, plus wetness). That is by field name only. The packing and the shader are in the plugin's compiled shaders (cooked shader library), not read. Next step: dump the material or compute-shader assets referenced by `PDA_FluxSurfacePreset_C` and [`CP_River_Kavkazi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Water/FluidFlux/Surface/CP_River_Kavkazi.json) and read their parameter names.

## R11. Significance rule order

Status FOUND (static). `UBHSignificanceEvaluator_Sphere` (`0x50D30B0`, setup `0x50D32E0`) and `_FOV` (`0x50D2CE0`, setup `0x50D2FC0`) both only ever **lower** an object's stored level (`min`), so the final level is the minimum over all evaluators and viewers; the set of evaluators in the settings asset therefore has no meaningful order. Level 0 is the nearest or most central band.

- Sphere: for each object take the squared distance `d2` to the nearest viewer; level = the highest settings index whose squared distance is at or below `d2`; 0 when `d2 <=` `LowestNonZeroSignificanceDistance` squared (or none matches).
- FOV: for each viewer and object take the unit direction and `dot` with the viewer facing; level 0 when `dot >= HighestConeCosAngle` and `d2 <= FurthestDistanceSquared`; otherwise, when `dot > LowestConeCosAngle` and `d2 <= FurthestDistanceSquared`, the first settings index from 1 upward with `cone cosine <= dot` and `distance squared >= d2`. The cosines and squared distances are cached by the setup functions.

No hysteresis is in these functions; any hysteresis would sit in the subsystem update (not read). Rules in `r42-modes.json` (`static.significance_rules`).

## R13. Arm class

Status FOUND (data). `Meta.Damage.Arms.*` is a property of the **projectile (caliber)**, not of armour: each `DA_*_ProjectileData` carries one tag. Small: 9mm, .45 ACP, .45 Colt, 7mm buckshot, 12g rifled slug. Medium: 5.45 mm, 5.56 mm. High: 7.62x39, 7.62x51, 7.62x54R, .308, .338 Norma Magnum, .50 AE, 30 mm and the combat/explosive arrows. Special: .50 Cal. (17 assets, listed in `r42-modes.json` `arm_class_by_projectile`.) So "Bullet from Sniper vs High arm class +28% (Armor)" means sniper-fired High-class rounds, and the penetration table of [`DT_InfantryData_AmmoTypeEffectivenessPen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json) scales armour-piercing effectiveness by this bullet class (0.7 / 0.6 / 0.5 / 1.0 for Small / Medium / High / Special).

## Counts

Rows: 1, 2, 3a, 3b, 4a, 4b, 5, 6a, 6b, 7, 8, 9, 10a, 10b, 11, 12, 13, 14 (18).

- FOUND: 1, 2, 3a, 4a, 5, 6a, 6b, 7, 10a, 11, 12, 13, 14 = **13**
- NATIVE (open, next step given): 3b, 4b, 8, 9, 10b = **5**
- ABSENT: 0 as a row status (row 3b records an ABSENT-by-name result: 0 cooked packages name any noise function)
- SERVER: 0. PROTECTED: 0.

## Reproduce

- Spawn volumes: `WdExtract ... findname Wardogs WDSpawnVolume`, then `dump` of the listed packages; `python -I _tools/r42_modes_data.py`.
- Explosion mapping: `dump` of `Wardogs/Content/VFX/Explosions/Blueprints/BP_Explosions`, `Wardogs/Content/GameplayCues/Vehicles/Destroyed/GC_Vehicle_Destroyed`; Kawaii: `findname Wardogs KawaiiPhysics` then `dump`.
- Native: `corpus.sqlite` functions at the RVAs above; `0x6B96BF0`, `0x5300B10` operands from the disassembly (`capstone`).

## Wiki updates

- `_wiki/game-modes-and-maps/ai-enemies.md`, alert levels: "A soldier is Alert at detection 0.8 and in Combat at 1.0. The detection that counts is the highest of its own and its squad-mates' (an enemy that sees you alerts the others). To go into Combat it must also currently see you; once in Combat it stays while the level is held at 1.0 (hidden for a few seconds and the level fades 0.25 per second, so it drops back to Alert and then Relaxed)."
- `_wiki/game-modes-and-maps/ai-enemies.md`, hearing: "Gunfire is loud because the soldier checks whether your weapon is in a firing sequence; vehicles are heard from up to 100 m (engine), 500 m (horn) and 800 m (when destroyed) by the AI (configured ranges, same for every vehicle)."
- `_wiki/game-modes-and-maps/king-of-the-hill.md` / `zone-layouts.md`: replace any "spawn positions unknown" with: "Vehicle deployment boards place vehicles at spawn areas defined per faction in each map; the tutorial gym has one player spawn area per faction (15 points, 12 m apart)." Do not state KOTH player start positions (not decided).
- Vehicle wiki pages and `fire-smoke-and-flash.md`: wrecks play one of 14 explosion sequences: helicopters (ROT_01 and ROT_04) the helicopter one, ROT_02 Havoc, ROT_03 Littlebird, tanks and the heavy FWG_01 the tank one, wheeled vehicles Kodiak/Ural/Dune Buggy their own, the four stationary guns (STN_01 to STN_04) their own, plus 155 mm shells, IEDs and a destroyed FOB.
- `_wiki/` cosmetics/ghillie: "the ghillie suit's strips sway with a soft spring (damping 0.25, stiffness 0.1)"; bobbleheads wobble with stiffness 0.1 and no damping.
- Settings / graphics: texture streaming budget by Texture Quality: 1.25 GB, 2 GB, 3 GB, 6 GB (levels 0 to 3).
- Weight pages: item weight values are kilograms (the HUD prints `{Weight}kg`).
- Ammo / damage pages: "arm class" is the bullet's class (Small: pistol and shotgun rounds; Medium: 5.45, 5.56; High: 7.62 family, .308, .338, .50 AE, 30 mm, arrows; Special: .50 Cal), not an armour class.
- `docs`/Environment page section 13 (GitHub only): `IterationDeltaTime` 0.18 s in all states, `Iteration` is a step count; the water grid doubles are a Z range (hypothesis); grid cell 200 cm; `worldmin` = area centre minus half size for all 40 grids.
