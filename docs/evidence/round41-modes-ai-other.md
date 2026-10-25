---
title: Round 41 modes, AI and other gaps
nav_exclude: true
---

# Round 41: AI detection, EQS, PvE, spawns and the UI/Other list (RE41-MODES)

Continues [round 40](round40-modes-ai-other.md). Static CL516586 review; nothing was run. Native RVAs are for `WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10...0cc37`), read from the decompiled corpus (`corpus.sqlite`) and, where the decompiler hid an argument, from the disassembly of the same bytes. No devirtualization. Scratch output: `E:/Reverse_Engineer/wardogs_analysis/round41_modes/` (`o1` factions, `o2` smoke/moving target/profiles, `o3` localisation copies; the locres files are not committed, only counts).

Statuses: FOUND, NATIVE (open, with the exact next step), SERVER, ABSENT (where searched), PROTECTED (none this round). Evidence: *data* (cooked asset read), *static* (decompiled or disassembled code read, not run), *config*, *SDK* (Dumper-7 headers).

Machine-readable results (idempotent, `python -I`; `--check` compares with the committed file):

- `_tools/ai_detection.py` -> `assets/data/ai-detection.json` (parameters, formulas, per-second tables).
- `_tools/ai_eqs.py` -> `assets/data/ai-eqs.json` (22 EQS queries resolved option by option, 5 contexts).
- `_tools/r41_misc_data.py` -> `assets/data/r41-misc.json` (faction setup, smoke VFX defaults, moving target, load-test profiles, translation counts).

## Rows

| # | Status | Item | Result |
|---|---|---|---|
| 1 | FOUND (static) | First-spawn route order (King of the Hill) | See R1. Faction spawn volume, random start index, circular walk to the first free point. No FOB step. Positions of the volumes: NATIVE (row 1b). |
| 1b | NATIVE | Where the KOTH spawn volumes are | They are `WDSpawnVolume` actors placed in the World Partition cells (not extracted). Next step: dump the cells of one world and filter `WDSpawnVolume` (fields `FactionTag`, `MaxSpawnPoints`, `HorizontalSpacing`, `VerticalSpacing`, `SpawnPointHalfExtent`). |
| 2 | FOUND (static) | AI detection combine | See R2. |
| 3 | FOUND (static) | AI sight and hearing in play | See R3. `VisionRangeMultiplier` is an exponent, `HearingRangeMultiplier` a linear factor; neither shrinks the radii. |
| 4 | FOUND (data) | AI EQS fields | See R4 and `ai-eqs.json`. |
| 5a | ABSENT | PvE team sizes | No player-count or team-size field in the four scenario feature plugins, the four `Config/Experiences/LegacyAIScenarios/*.json` files, or `DefaultGame.ini` (searched: `MaxPlayers`, `TeamSize`, `SquadSize`, scenario names). The scenarios create three factions (R5). Session size is the server-wide 60 to 100 of round 40. |
| 5b | ABSENT | Hunter Killer "side" | `HunterKiller_01` sets no `PlayerFactionTag`, no starting cash, no spawners; its quest is Entry then Exit. VIP Escort players are Bravo (Valkyra) against Manticore AI; Strike and Disarm players are Charlie (Manticore) against Lonestar AI. |
| 5c | ABSENT | PvE mission rewards | `ScenarioCompletedRewardCash` is set in none of the four scenarios (round 36). Any payout is not in the client scenario data; treat as SERVER. |
| 5d | FOUND (data) | PvE mission names | Quest names are placeholders: `[PH] Strike and Swipe`, `[PH] VIP Escort`; Hunter Killer has no string table. Experience aliases `ED_HunterKiller_01`, `ED_VIPEscort_01`, `ED_StrikeDisarm_01`, `ED_ScenarioExample`. |
| 5e | FOUND (data) | PvE voice-over lengths | All 10 `WDScenarioVoiceOverData` entries have `SubtitleDurationInSecond` 10 (already on `Wardogs_PveSettingsAssets_v1.md`). Audio length not read (audio is out of scope). |
| 5f | FOUND (config) | PvE experience flags | The three missions enable `DestructionPlayground`, `Lootable`, `WDAICover` (+ `Behaviour_Patrol` for VIP Escort and Strike and Disarm) and **disallow `Experience.Rules.SkipPlayerDowned`**, so players can be downed (KOTH does the same). |
| 6.1 | ABSENT | `BHUserSettingEnumDiscreteValues` | `rawfiles` search for "DiscreteValues" over all paks: 0 packages. There is no asset of that name in this build. |
| 6.2 | NATIVE | Hashed property names (2,645) | Not worked this round (no new evidence). Next step: the hash is a per-build obfuscation; compare the name table inside serialized owner descriptors against Dumper-7 `FArrayPropertyParams`, as in round 12 section 5. |
| 6.3 | NATIVE | Water height grid doubles `+0x58`, `+0x60` | Partial. Class `UWDWaterHeightGridAsset` ctor `0x6A59C50` (size `0x98`); loader `0x6F77240` registers a grid only if `Heights.Num == GridWidth x GridHeight` (reads `GridWidth` `+0x50`, `GridHeight` `+0x54` and the `Heights` count at `+0x90`), so the 16-bit samples are a plain row-major grid. The sampler that reads the two doubles was not located. Next step: callers of the grid list built at `0x6F77240` (`a1+72`). |
| 6.4 | NATIVE | Fluid Flux `Iteration`, shader, channels | No native class named FluidFlux in the corpus (third-party plugin, only cooked assets). Not resolvable without the plugin's shader; stays open. |
| 6.5 | FOUND (SDK) | MicroBiome `AttenuationDistance` | The SDK field with that name (`+0x330`, with `Proximity` `+0x32C`) is on a `SweejAmbience` component (ambient sound). It is an audio ambience distance, out of scope. Link from MicroBiome assets to that component is an inference. |
| 6.6 | FOUND (data) | Smoke VFX Blueprint `PDA_SmokeGrenade` | Now dumped. Class defaults: `Diameter` 15.0, `Total Duration` 180.0, `Fade In Time` 20.0, `Fade Out Time` 10.0, `SpriteMaxSize` 800.0, colour white alpha 0.75. `DA_SmokeGrenade_White` overrides the duration to 120.0; the vehicle `DA_SmokeScreen` uses Diameter 0.1, duration 6.0, fades 2.0/2.0, sprite 1500. So diameter is a scale-like parameter (15.0 vs 0.1), not centimetres. The Niagara system is not read. |
| 6.7 | FOUND (config) | Gameplay tags | `DefaultGameplayTags.ini`: `ImportTagsFromConfig=True`, `NumBitsForContainerSize=6`, `NetIndexFirstBitSegment=16`. No `GameplayTagRedirects` anywhere in the config (searched `*.ini`, `Tags/*.ini`; the only redirects are 3 class, 5 property, 2 struct core redirects for UI and resource-requirement renames). Tag matching is stock engine behaviour (not in files). |
| 6.8 | NATIVE | Mechanics units (arm-class, seat-reduction arrays) | Not worked. Next step: match the array element structs against `WDGame_structs.hpp`. |
| 6.9 | FOUND (static) | Effect aggregation (basis of `Percentage_Ongoing`) | `sub_14522E5C0` evaluates an attribute from six modifier lists: if an active override exists it wins; otherwise `((base + sum(add)) x (1 + sum(mul - 1)) / (1 + sum(div - 1)) x product(compound)) + sum(final add)` (division term replaced by 1 if its magnitude is under 1e-8). This is the stock engine aggregator layout. The **damage** `Percentage_Ongoing` operation is a separate function and stays NATIVE (open): next step, the damage-operation switch in the damage pipeline. |
| 6.10 | ABSENT | `EToolFonts` | No `EToolFonts` in the SDK headers (`sdk/raw`, grep); editor-only enum. |
| 6.11 | NATIVE | Significance level selection | SDK: `BHSignificanceEvaluator_FOV` (fields `LowestConeCosAngle`, `HighestConeCosAngle`, `FurthestDistanceSquared`) and `_Sphere` (`LowestNonZeroSignificanceDistance`) are the two evaluators; settings values are in round 40. Order and hysteresis not decoded; next step: `UBHSignificanceEvaluator_VFT` slots (`0xAA3D230`). |
| 6.12 | NATIVE | Units across the export (weight, mass, speed) | Not worked; no new evidence. |
| 6.13 | NATIVE | Explosion timing viewer mapping | Not worked. |
| 6.14 | NATIVE | Characters (streaming budget, Kawaii constraints) | Not worked this round. |
| 6.15 | NATIVE | Achievements thresholds | Not worked (round 36 econ appendix stands). |
| 6.16 | FOUND (data) | Automation | `DT_ServerTestingProfiles` (row struct `WDAutomatedTestServerProfile`) has 11 rows of load tests, so `WDAutomation` is **test scripting**, not scripted scenarios: `Default` 100 clients, `SoloTest` 1, `Default10Players` 10, `100Players`, `100GroundVehicles`, `100TrackedVehicles`, `100Helicopters`, `30BotOrchestra` (30), `MovementMedley` 100, `Macarena` 100, `InputTest` 5 (custom controller `PC_AutomatedPlayerController`). Each names an orchestrator Blueprint under `/Game/Tests/LoadTests/Orchestrators/`. `DT_ClientTestingProfiles` is not a package in the paks. |
| 6.17 | FOUND (data) | Moving target (Gym range) | `B_MovingTarget`: `Health` 1.0, `DamageIncrease` 3.5, `TimeToReachTargetRange` min 15.0 max 25.0 (seconds assumed; random per run), targets slide between two points 150 either side of centre (relative Y +/-150), a 0.5 s fall timeline (`FallRate` curve 0 to 1 over 0.5 s). Graph nodes not exported. |
| 6.18 | FOUND (data) | Localisation | The paks hold `Game.locres` (UE LocRes v3) for **15 cultures**: en, de, es-ES, fr-FR, it-IT, ja-JP, ko, pl-PL, pt, pt-BR, ru, tr-TR, uk-UA, zh-Hans, zh-Hant. Each has 5,948 entries in 169 namespaces (largest: `STRINGS_Settings` 779, empty namespace 707, `STRINGS_Ingame` 584, `STRINGS_Frontend` 293, `STRINGS_Popups` 258, `BHUserSettings` 179). Entries identical to English: 443 (ru) to 640 (de). `Engine` and `LearnToPlay` locres also exist. The earlier note "non-English text is not in the data" is wrong: it is in `.locres`, not in the cooked JSON. Text was not exported (counts only). |
| 6.19 | skipped | Shooting range tutorial values | Scope rule: tutorial text and layout are not gameplay numbers. |
| 6.20 | skipped | Skins (textures, `CPD` fields) | Scope rule: pure visuals. |

Row 6 covers the UI/Other list: 6.1 to 6.20 (20 sub-items; the 21st, hashed `_aaa` names, is merged into 6.2 and 6.3).

## R1. First-spawn route order (King of the Hill)

Status FOUND (static). Evidence: `UWDKOTHPlayerSpawnManagerComponent_VFT` (`0xBAE6878`), compared slot by slot with the Deathmatch component (`0xBA28D28`) and the base. KOTH overrides slots **0** (destructor), **159** (`0x8636420`, choose a start) and **160** (`0x86363A0`, not read). It does **not** override slot 128, which in Deathmatch gathers every `PlayerStart`; so KOTH does not use `PlayerStart` actors.

Route (slot 159, called with the game-mode session as owner):

1. The owner's spawn-volume holder (object at owner `+424`, array at `+0x560`, count at `+0x568`) is searched linearly (`0x6D956D0`, reads each volume's faction through `0x6D76F90` and compares with the player's faction reference at player `+1440`; the compare target is read from the register, so the "faction" reading is by call shape). The match is the player's **faction spawn volume** (`WDSpawnVolume`, fields `FactionTag`, `Faction`, `MaxSpawnPoints`, `HorizontalSpacing`, `VerticalSpacing`, `SpawnPointHalfExtent`, `SpawnPointOffsetZ`, `bSpawnRightToLeft`).
2. `WDSpawnVolume` point pick (`0x6D77470`): `index = (int)(rand() / 32768 x count)`, clamped to `count - 1`.
3. With no pawn supplied, that random point is returned. With a pawn, the volume walks the list from that index and, for `(index + k) mod count`, adds a height offset read from the pawn through a virtual call (slot 278; its meaning is not decoded) to Z and tests the spot with a placement check (`0x4404E5F0`); the first point that passes is used. If none passes, the spawn fails.

So: faction area -> random start point -> next points in list order until one is free. The FOB is not part of this route (it is a separate re-deploy path; see round 38 section 14). Round 40 found the Deathmatch route (furthest start from all enemies); KOTH has no enemy-distance rule.

## R2. How detection is built

Status FOUND (static). Evidence: `sub_148876C80` (`0x8876C80`, perception update, dispatches each stimulus by sense class: sight `+560`, hearing `+568`, damage `+576`), `sub_148877A80` (sight strength), `sub_148876A40` (hearing strength), `sub_148870350` (hearing detectability of the target), `sub_148872190` (sight detectability), `sub_148877450` (accumulate), `sub_14887D1D0` (tick). `GetMappedRangeValueClamped` is `0x53197B0` (arguments confirmed in the disassembly: input range (0, radius), output range (0, 1)); the power function is the import stub `0x98F80DA`.

Per target, per tick (delta time `dt`, world time `t`):

- `sight = angle x (x^(-2 x VisionRangeMultiplier) - 1) x concealment x detectSight`, `x = clamp(distance / SightRadius, 0, 1)` (the term is set to 3.4e38 at distance 0 and is exactly 0 at and beyond the radius). `angle = dot(facing, direction to target)^VisionAngleMultiplier`, 0 when the dot is not positive. `concealment = (visible points / total points)^VisionPlayerConcealmentMultiplier` from the target's `WDAISightTargetComponent`. Native defaults for angle and concealment multipliers are 1.0 (ctor `0x8863540`, round 36).
- `detectSight = StanceDetectability[stance] x StanceDetectabilityMultiplier + clamp(speed / maxSpeed, 0, 1) x MovementSpeedMultiplier`. Stance map: Stand 1.0, Crouch 0.4, Prone 0.3, multiplier 0.5 -> **0.5, 0.2, 0.15 standing still**; `MovementSpeedMultiplier` is unset in the Blueprint (native 1.0), so running at full speed adds 1.0. `maxSpeed` is a value cached when the component starts (`0x88698A0` stores `+352` as the owner movement component's speed of mode 2 times its scale at `+308`; mode 2 not named).
- `hearing = detectHear x (1 / x^2 - 1) x HearingRangeMultiplier`, `x = clamp(distance / HearingRange, 0, 1)`; zero at or beyond the range. `detectHear` is **1.0 if the character is operating a vehicle** (a `BHVehicleOperatorComponent` with a valid controlled vehicle, class getter `0x5314B20`), else `max(WeaponFiring x WeaponFiringMultiplier when firing, clamp(speed / maxSpeed, 0, 1)^2 x HearingMovementSpeedMultiplier)`. Values: WeaponFiring 5.0 x 1.0 = **5.0**, HearingMovementSpeedMultiplier **0.0015**. Standing still and silent gives 0.
- Damage: the stimulus adds a fixed **1.0**.
- `detectionLevel = clamp(level + dt x (sum of the sense strengths), 0, MaxDetectionLevel)` (`0x8877450`; `MaxDetectionLevel` native 1.0; the entry is flagged when the cap is reached). Decay (round 40): `dt x 0.25` once 5 s have passed since the last update (`0x887D1D0`); the entry is removed at level 0 or below. The strength of one sense (the sense whose id equals one looked up from the perception settings, by call shape probably sight) is also stored separately in the entry; its use is not decoded.

Not decoded: the exact test behind "is firing" (a component of the target's controller, `0x6B96BF0`), how the alert thresholds (0.8 Alert, 1.0 Combat) read the level (inferred from the 0..1 range), which events make the engine create hearing stimuli (noise reports), and the mode-2 speed. Per-second tables: `assets/data/ai-detection.json`.

## R3. Sight and hearing "in play"

Status FOUND (static). Combining R2 with the radii (`SightRadius` 200000, `HearingRange` 100000 in the Blueprint; assumed centimetres, so 2,000 m and 1,000 m):

- **The multipliers do not shrink the radii.** The earlier guess (40 m sight, 50 m hearing) is wrong. `VisionRangeMultiplier` 0.02 is the exponent in `x^(-2 x 0.02) - 1 = x^-0.04 - 1`, a very flat falloff; `HearingRangeMultiplier` 0.05 is a linear factor on the inverse-square term.
- Sight gain per second for a standing, still target in the open, seen head-on (detectability 0.5): 10 m **0.118**, 25 m 0.096, 100 m **0.064**, 500 m 0.029, 1,000 m 0.014, 1,500 m 0.006, 2,000 m 0. Full level 1.0 takes about 8 s at 10 m, 16 s at 100 m, 35 s at 500 m, 70 s at 1,000 m. Crouching is 0.4x that, prone 0.3x. Running at full speed (0.5 + 1.0) is 3x the standing rate.
- Hearing gain per second: gunfire (detectability 5.0) at 10 m 2,500, 100 m **24.75**, 500 m about 100, 900 m 0.059, 1,000 m 0 -- gunshots inside about 450 m give at least 1.0 per second (full detection within one second). A vehicle occupant (1.0) is 1/5 of that (100 m: 4.95). Running at full speed on foot (0.0015) gives only 0.75 at 10 m and 0.0074 at 100 m: footsteps hardly matter. Standing still is silent.
- Practical reading: AI notice a firing player at hundreds of metres almost at once; a silent player is noticed slowly by sight, 3x faster when sprinting, and crouching or prone slows it. Whether the AI also needs line of sight for Combat is the alert-state rule of round 40; the line-of-sight trace itself is the engine sight sense, not decoded.

## R4. AI EQS fields

Status FOUND (data). 22 queries in `WDAIPvEAICore` / AI plugin `EQS_*` (round 36 dump), resolved in `ai-eqs.json`. Highlights:

- `EQS_FindTarget` (service every 1.5 s): three options, each a `WDEnvQueryGenerator_ThreatActors` (default sense, `AISense_Hearing`, `AISense_Damage`) with one test, actor has tag `State.Player.Vitality.Alive`. So targets come from remembered sight, hearing and damage threats, alive only.
- Cover generators (`SDEnvQueryGenerator_Covers`): `FindCoverNearby` radius from the character config `RadiusToSearchForCovers` (default 3000), reserved-by-me included, free covers only; `FindClosestCoverToQuerier` radius 2000; besiege queries use the target volume size.
- Common tests: keep at least **200** from living teammates; dot (cover direction vs enemy) minimum 0.7 (`FindCoverCloserToEnemy`), 0.4 (`FindCoverTowardsEnemy`), 0.8 to 1.0 (`FindClosestCoverToQuerier`, toward the goal target); distance to the enemy limited by weapon data (`EAIWeaponDataField::MinAIRange` (8 providers) and `MaxAIRange` (1)); cover trace to the enemy (`WDEnvQueryTest_CoverTrace`); pathfinding cost or batch filters; influence map `InfluenceMap.TeamMap` value (max 0.4 for besiege cover).
- `EQS_FindCombatPositionCloserToTarget`: donut generator inner 200, outer from `RadiusToSearchForCovers`, projected on navigation.
- `EQS_FindPointAroundBesiegeTarget`: donut around the goal target, spacing 500, inner 200, filtered by `WDTargetAreaVolume` and path distance. `EQS_PatrolPoint`: projected spline points 1,000/1,500/2,000 ahead. `EQS_PatrolPoint_Follower`: spiral donut 1 to 600, spacing 200. `EQS_FindFleePointFromGoalTarget`: 180 degree arc away from the target. `EQS_FindSearchLocation`: influence-map locations (`BP_InfluenceEvaluator_AlertLocationGenerator`).
- Exact test orders and scoring equations per query are in the JSON.

## R5. PvE group

Status see rows 5a to 5f. Extra fact (FOUND, data): `B_FactionSetup_CreateThreeTeams` (used by all PvE missions and by King of the Hill) creates the default faction plus Alpha, Bravo, Charlie; `CreateTwoTeams` creates Alpha and Bravo. So PvE missions have three team slots but the missions fix the players' faction (VIP Escort Bravo, Strike and Disarm Charlie).

## Counts

Tally of the rows above (row 1 counted as FOUND, 1b separately):

- FOUND: R1 (1), 2, 3, 4, 5d, 5e, 5f, 6.5, 6.6, 6.7, 6.9, 6.16, 6.17, 6.18 = **14**
- NATIVE (open, next step given): 1b, 6.2, 6.3, 6.4, 6.8, 6.11, 6.12, 6.13, 6.14, 6.15 = **10**
- ABSENT: 5a, 5b, 5c, 6.1, 6.10 = **5**
- SERVER: 0 (5c is treated as ABSENT with a SERVER reading)
- PROTECTED: 0
- skipped by scope: 6.19, 6.20 = 2

## Reproduce

- Detection: `corpus.sqlite` functions at the RVAs above; arguments hidden by the decompiler read with `capstone` from `WardogsClient-Win64-Shipping.restored.exe` (`0x53197B0`, `0x8870350`, `0x8877BE6`). Constants: `-2.0` at `0x8877C0B`'s source operand, `3.4e38` guard, `(0, 1)` output range at `0x9AADBC0`.
- Data: `WdExtract ... dump <list>` for `Wardogs/Content/VFX/Shared/PDA_SmokeGrenade`, `Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget`, `Wardogs/Content/Tests/LoadTests/Data/DT_ServerTestingProfiles`, `Wardogs/Content/GameMechanics/Gamemode/B_FactionSetup_Create*Teams`; `rawfiles Content/Localization/Game --copy`. Then `python -I _tools/ai_detection.py`, `_tools/ai_eqs.py`, `_tools/r41_misc_data.py` (each with `--check`).

## Wiki updates

- `_wiki/game-modes-and-maps/ai-enemies.md`, Senses: replace "effective 40 m sight and 50 m hearing is not verified" with "the two multipliers do not shorten the ranges: sight and hearing still reach 2,000 m and 1,000 m (configured), but the build-up rate is tiny at range (see below)". Add a "How detection builds up" section: each soldier adds up sight, hearing and damage every tick into a detection level from 0 to 1 per target; standing still in the open at 100 m takes about 16 s to reach full detection, at 10 m about 8 s; crouched about 2.5x slower, prone about 3.3x slower, sprinting 3x faster; gunfire is detected almost instantly within a few hundred metres; a vehicle driver is heard at one fifth of gunfire; footsteps barely register; a silent standing player is not heard at all; a damage hit adds 1.0 per second. Level fades by 0.25 per second after 5 s unseen.
- `_wiki/game-modes-and-maps/ai-enemies.md`, Targeting: "targets are chosen among alive players the soldier has seen, heard or been damaged by (checked every 1.5 s)"; cover search: "covers within 3,000 (config) of the soldier, at least 200 from teammates, preferring covers that face the enemy and are within weapon range".
- `_wiki/game-modes-and-maps/king-of-the-hill.md` (and `zone-layouts.md` if it has a spawn section): add "You spawn at your faction's spawn area: the game picks a random spawn point in that area and moves to the next free one; there is no PlayerStart or enemy-distance rule (unlike Deathmatch)".
- `_wiki/game-modes-and-maps/hunter-killer.md`, `vip-escort.md`, `strike-and-disarm.md`, `pve-scenarios.md`: players can be downed in PvE missions (the skip-downed rule is disallowed); no team-size field exists in the client data (server decides); placeholder names "[PH] Strike and Swipe", "[PH] VIP Escort", Hunter Killer has no name text; mission voice-over subtitles show for 10 s each; no mission reward cash is set in the data.
- `_wiki/equipment/m18-smoke-grenade.md` / `fire-smoke-and-flash.md`: smoke effect data: default total duration 180 s with 20 s fade in and 10 s fade out; the white grenade variant lasts 120 s; vehicle smoke screen 6 s with 2 s fades (Niagara units of "diameter" unknown).
- Maps page (Gym range): moving target has 1 health, damage multiplier 3.5, takes 15 to 25 s to reach its far point, moves 1.5 m either side (relative 150, unit assumed cm), falls in 0.5 s.
- Settings / languages page: the game ships text in 15 languages (en, de, es, fr, it, ja, ko, pl, pt, pt-BR, ru, tr, uk, zh-Hans, zh-Hant), each with 5,948 text entries.
- `docs`/automation notes (GitHub only): WDAutomation is load-test scripting (11 server profiles, 1 to 100 clients).
