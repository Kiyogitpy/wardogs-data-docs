---
title: Round 40 modes, AI and other gaps
nav_exclude: true
---

# Round 40: modes, zones, AI and other gaps (RE40-MODES)

Continues [round 39](round39-modes-ai-other.md). Static CL516586 review; nothing was run. Native RVAs are for `WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10...0cc37`), read from the decompiled corpus (`corpus.sqlite`, no devirtualization). Extractor output: `E:/Reverse_Engineer/wardogs_analysis/round40_modes/` (`umap/rawfiles.txt`); round 39's full config copy `round39_modes/cfgc/raw/Wardogs/Config/` was read this round.

Statuses as in the round 36 brief (FOUND, NATIVE, SERVER, ABSENT) plus **OPEN** (not resolved; the line says what was searched). Evidence levels: *config* (file text read), *data* (cooked asset read), *static* (decompiled code read, not run), *inference* (stated).

Machine-readable results (idempotent, `python -I`):

- `_tools/default_game_ini.py` -> `assets/data/default-game-ini.json` (source excerpt `data/Wardogs/Config/DefaultGame.excerpt.ini`).
- `_tools/zone_selection.py` -> `assets/data/zone-selection.json` (selection rules, per-layout fallback probabilities, Hot Zone movement per config, all region weights).
- `_tools/mode_rules.py` (round 39) now carries an `overriddenBy` note.

## New source: `Wardogs/Config/DefaultGame.ini` (and the rest of the staged Config folder)

Round 39 copied the whole staged `Config` folder but only read the Experiences, server example and plugin inis. `DefaultGame.ini` (about 1,170 lines, 106 sections), `DefaultInput.ini`, `DefaultSignificance.ini` and `DefaultFeatureFlags.ini` are the real project defaults. The full `DefaultGame.ini` also holds backend URLs and a bearer token, so only a whitelisted excerpt is committed (the tool says which sections). **Do not copy the full file into the repository.**

### Corrections to round 39 (important)

Round 39 reported native constructor defaults. `DefaultGame.ini` overrides them:

| Field | Round 39 (native default) | Actual project default (config) |
|---|---|---|
| `MatchState.Playing.KOTH` `ScoreLimit` | 10 | **100** |
| `MatchState.Playing.KOTH` `ScorePeriod` | 0 (example server: 24) | **22.0** s (inside the 18..30 clamp; the example server file sets 24) |
| `MatchState.Playing.Deathmatch` | `ScoreLimit` 75, no time limit | `ScoreLimit` 75, **`MaxTime` 1800** (30 min, unit assumed seconds like the other `MaxTime` entries) |
| `MatchState.Playing.SniperShowdown` | `KillLimit` 10, no time found | `KillLimit` 10, **`MaxTime` 1800** |
| `MatchState.PreMatch...PlayerCount` | `MinimumRequiredPlayers` class default 0 (example server 20) | **60**, `MaxTime` 10.0 s |
| `MatchState.PreMatch...ReadyUpKOTH` | not read | `MinimumRequiredPlayers` **9**, `MaxTime` 5.0 s |
| `MatchState.PostMatch` | not read | `MaxTime` **45.0** s (the legacy `DefaultMatchState.ini` said 35) |
| KOTH `InactivityTimeoutSeconds`, `MatchHardCapSeconds` | 0 | 0 (so King of the Hill has no time limit) |

Other values in the same file: `WDGameSession` `LowestAllowedMaxPlayers` 60, `HighestAllowedMaxPlayers` 100, `ServerNameMaxLength` 64; `WDGameModeSession` `bAutoAssignFactions` False, `OverrideStartingCash` -1 (use the currency default), `bSkipDownedState` True; `WDGameStateSession` `OverpopulatedTeamThresholdConfig` 2, lock False (the example server turns the lock on). Level of evidence: config. Whether a server-side override applies on top is the server owner's business (the example server file shows how).

## The asked-for items

### R1. Which zone layout is used when the rotation names none

Status **FOUND** (static). Evidence: `sub_1477646F0` (called from `AWDControlZone` BeginPlay `0x77698A0` and from `0x7766520`), `sub_14776C740` (pick by tag, weighted), `sub_14776E780` (apply layout), `sub_146BFE220` (the counter).

Order of precedence, run on the server only and only when the config's `bActivateAlternator` is true:

1. Launch option `DisableZoneAlternator`: no alternator, the config's base `ZoneData` is used (index -1).
2. **The tag set for the match** (the rotation entry's `ZoneAlternator`, held on an object reached through the world's game-state side, `0x6F497F0`, at `+0x100`): if the config has an alternator with exactly that tag it is used (if several entries share the tag, one is drawn by weight; a single weight-0 entry is still used).
3. Otherwise, if the server ini list `ControlZoneQueue` (Config array of strings; BeginPlay turns each `X` into the tag `<prefix>.X`, prefix = the `ZoneAlternator` tag root, keeping only tags that exist) is not empty: **entry number (counter mod queue length)**. The counter `dword_14CEBA820` is incremented once per call of the function `0x6BFE220`, which copies an FURL-shaped structure (protocol, host, port, map, options) and then calls the browse routine, so it counts map loads (inference from the call shape). `DefaultControlZone.ini` and the example server file set no queue, so the queue is empty by default.
4. Otherwise a **weighted random draw** over `AlternatorSelectionWeight`: sum all weights, `r = rand() / 32767 * sum`, walk the entries adding weights, first entry whose running total reaches `r`; entries with weight 0 (absolute value below 1e-8) are skipped. Fall-through leaves -1 (base data). So **weight-0 layouts are never drawn by weight; they are reachable only by naming them (step 2) or through the queue (step 3).**

Fallback probabilities from the data (when nothing names a layout): Ozeti (Europe) Default, Church, River each 1/3 (Farmland 0); Zestafona (NorthAmerica) Default, WaterTreatment, Houses each 1/3 (SmallFactory 0); Bakurani Default 1/2, Farmland 1/4, Lumberyard 1/4; Kenya (Africa) Default 100% (North, East, West 0); Sabartulo (Russia) Hospital 100% (Bazaar, River, Hillside 0). Machine-readable in `zone-selection.json`.

### R2. What `Bakurani.River` does

Status **FOUND** (static, plus data). The example rotation names `ZoneAlternator.Bakurani.River.Circle` six times. The Bakurani zone config has three alternators (Default, Farmland, Lumberyard) and **no River entry**, so step 2 above finds no match and the server falls through to step 3/4: with an empty queue the layout is a **random weighted draw: Default 50%, Farmland 25%, Lumberyard 25%**. The tag is therefore effectively "random layout" (probably left over from an earlier River layout). No crash path is visible; the apply function handles index -1.

### R3. Region selection (where the Hot Zone goes)

Status **FOUND** (static). Evidence: `sub_148458DA0` (selection), `sub_1484599B0` (weight redistribution), `sub_148458790` (point in region), component `WDControlZoneRegionsComponent` fields `LastSelectedIndex +0x118`, `ControlZoneRegionsDynamicWeights +0x120`, `NextSelectedIndex +0x130`; data `DA_ControlZoneRegionsConfig_{Kavkazi,Europe,NorthAmerica}` (60, 55 and 56 regions).

- A region is a candidate if it is not the previous choice, has a dynamic weight slot, **has no polygon vertex within `MinHotZoneMoveDistance`** of the Hot Zone's current position, and at least one vertex passes a placement test (`0x1477651E0`). `MinHotZoneMoveDistance` is unset (0) in all King of the Hill configs and 750 in the Gym config (so in play the distance filter is inactive except in the Gym).
- Weight used: `ControlZoneRegionAlternatorWeights[AlternatorIndex]` if that index exists (30 slots stored per region), else `ControlZoneRegionDefaultWeight`. Example (Kavkazi): SUNFLOWERS HOUSE has default 5.0, 1.0 for layout 0 (Default) and 5.0 for the others; SUNFLOWERS SOUTH 1.0 everywhere.
- Draw: one `rand()`, `r = rand() / 32767 * sum` of the candidates' **dynamic** weights, first candidate whose running total reaches `r` wins. If `NextSelectedIndex` is not -1 (server command `Auth_SetNextSelectedIndex`) that index is used once instead and then cleared.
- After a region is chosen (`0x1484599B0`) it gives away **half of its dynamic weight**; the other regions share that half in proportion to their configured weight (`base_j / (sum of base weights - base_chosen)`), so total weight stays constant: a just-used region becomes less likely and recovers as others are drawn. The caller's total of base weights reaches this function in a register (reading inferred from the call shape, not an argument in the decompiled prototype).
- **Zero-weight regions are never drawn by this rule**: the Kavkazi towers (TOWER 1, 2, 4, 7, AbandonedTWR 2 and 3, all slots 0; TOWER 3 has 0.2 only at layout slots 11 and 26, which no config reaches), Europe `Tower 2`, NorthAmerica `Tower 1..3`. They can be reached only through `Auth_SetNextSelectedIndex` (server command). Redistribution gives them nothing (their base weight is 0).
- Overlap: nothing in the selection tests overlap between regions. Computed from the stored polygons (vertex inside the other polygon, or crossing edges): **33 overlapping pairs in Kavkazi, 9 in Europe, 7 in NorthAmerica** (examples: Kavkazi TOWER 3 / WEST HILL WOODS, TOWER 4 / SUNFLOWERS TOWER; Europe Tower 1 / POI Apartment Garages; NorthAmerica Shipping Exports Large / Long / TrainTracks). Overlaps are harmless to the code: each region is drawn independently and the point inside the chosen polygon is generated afterwards.
- Region configs exist for **Kavkazi, Europe, NorthAmerica only**. Russia and Africa have none (so those maps cannot use the regions component).

### R4. What the pre-lobby award buys

Status **FOUND** (static plus config). `WDServerSeedingPreLobbyComponent::0x8640D40` (runs when the match starts, pending amount `+0x118` greater than 0): it sends the pending amount as a currency award tagged **`Attribute.Meta.Currency.Cash`** (tag registered at `0x128B090`, used as `qword_14D36B340`), and adds the Blueprint's tag list (`Vendor.Discount.FirstPurchase`) to the player (`0x145239140`, count 1). So the pre-lobby points become **starting Cash** (first award 150, periodic 250 per 60 s, cap 5000, from round 39; a Hot Potato pass is 10 x pass multiplier), plus a **first-purchase discount** tag.

The discount rule is in `DefaultGame.ini` `[/Script/WDGame.WDEconomyConfig]`: `WDEntityPriceModifier_FirstPurchase(RequiredTag=Vendor.Discount.FirstPurchase, EntityTarget=Global, Multiplier=90.0)`. The same list: `Level` (Wardog level at or below 8, global) 50.0; `LosingFaction` (score difference 40, global) 80.0; and three `Faction` rows with Multiplier 0.0 for one item each (Alpha `Id.Item.WEPN_033`, Bravo `Id.Item.A91`, Charlie `Id.Item.KH2002`). `RefundModifier` 0.9. **Reading of `Multiplier`:** the values (0, 50, 80, 90) fit "percent of the normal price" (0 = free signature rifle, 50 = half price for new players, 80 and 90 = 20% and 10% off), but the native code that applies them was not traced; treat the unit as an inference. The wiki can say "a first purchase gets a discount (the file's multiplier is 90)" and "pre-lobby points are added to starting cash".

### R5. Sniper Showdown standing-still time

Status **FOUND** (static). `WDSniperShowdownStillnessSpottingComponent` (`B_...` Blueprint overrides nothing). BeginPlay `0x8646E50` arms a looping timer (`0x864B140`) with period `UpdateInterval` (1.0 s) whose callback is `0x864DFA0`:

- It compares the squared distance from the player to a stored anchor against `DistanceThreshold` squared (5000.0; unit assumed Unreal cm = 50 m, not verified). While the player stays inside, a counter `+0x134` grows by `UpdateInterval` each tick; leaving resets/re-anchors (`0x864B360`).
- At `+0xF0` = **90.0 s** of standing still the player is spotted: `0x8647140` stores a marker at that position that lasts `+0xFC` = **200.0** (added to the game-state time, seconds assumed) and keeps at most `+0xF8` = **3** markers (older ones are dropped).
- At 90 - `+0xEC` (15.0) = **75 s** a one-time warning feed message is shown (`Client_ShowEventFeedMessage`, tag `qword_14D3E8108`).
- After a spot the check resets (`0x86478A0`) with a **`GracePeriod` of 15.0 s** before standing still can count again.
- `+0xE4` = 5.0 is read nowhere in this path (unresolved).

Wiki wording: "Stand within about 50 m (assumed) for 90 s and you are revealed on the map for 200 s (at most three reveals shown); a warning appears at 75 s; after a reveal you get 15 s before the check restarts." The units of distance (cm) and of the 200 are assumptions.

### R6. Deathmatch spawn selection and ammunition

Status **FOUND** (static; ammunition amount partly inferred).

- Spawn: `WDDeathmatchPlayerSpawnManagerComponent` overrides virtual slots 128 (`0x8490260`: collects every `PlayerStart` actor of the world into `PlayerStarts`) and 159 (`0x8493480`: choose a start). The choice: take the positions of living players on **other factions** (when the game has two or more factions; all players otherwise), keep starts that pass two checks (`0x6D73B80` false, `0x6D73880` true for this player), and pick the start whose **minimum distance to any enemy is largest**. With no enemies the first valid start is used. In words: respawns go to the start furthest from all enemies. Starts used are marked (`0x6D73BA0`).
- Ammunition: `WDLoadoutAmmoGenerationComponent::Server_SetupLoadoutByTag` (vslot 159, `0x8495620`) grants the chosen weapon (quantity argument 1) and then grants the weapon's first child item matching **`Item.Attachment.Magazine`** (tag registered at `0x129E190`) with quantity argument **4**. So a Deathmatch weapon pick gives the weapon plus four magazine items; the loaded magazine versus spares split is not decoded and the argument meaning (count) is read from the call shape.

## Backlog items (round 39 OPEN list)

| Status | Item | Value, source, evidence |
|---|---|---|
| FOUND | Factions: what each is | Data `Meta_Alignment_Faction_{Alpha,Bravo,Charlie}`: Alpha **Lonestar** (short `L*`, colour #4CB1EF blue), Bravo **Valkyra** (`Vlk`, #FA503E red), Charlie **Manticore** (`Mtc`, #1DD65C green); squad colour #EDA314 for all; each has a logo texture and safe-zone tags. Backstory text: ABSENT (no description strings in the faction assets). data |
| FOUND | Factions: weapons and gear differences | Each faction has one signature 5.56 mm rifle priced at multiplier 0: Alpha `WEPN_033`, Bravo `A91`, Charlie `KH2002` (`DefaultGame.ini` economy). Other faction differences (vehicle versions, cosmetics) as before. config |
| OPEN | Experiences: first-spawn route order | Searched: spawn manager vtables for KOTH not opened (only Deathmatch). Not resolved. |
| FOUND | Moscow = Sabartulo name link | Experience `Russia/Moscow_KOTH_01` and the Russia zone config (alternators `ZoneAlternator.Sabartulo.*`) belong to the same `Russia` map; the server rotation's `Map` key for it would be `Russia` (examples use Kavkazi, Europe, NorthAmerica). inference from names and folders |
| FOUND | Zone region choice | R3. static |
| FOUND | Zero-weight towers / alternators | R1 (alternators) and R3 (towers): never drawn by weight; reachable only by naming or a forced next index. static |
| FOUND | Hot Zone movement in play | State machine `0x776DB20`: first move after `FirstMoveDelay` (absent = 0 in the KOTH configs, so the Hot Zone is placed at once), then each `MoveDelay` (25 s in all KOTH configs, 0 in the Sniper Showdown configs) times a scale read from the game-state side (`0x6CB9970`, 1.0 when none is found). The scale's source was not identified, so 25 s is the data value and "about 25 s" the safe wording. `bUseOverrideHotZoneMovementData` lets the server replace the whole block. HotzoneSpeeds 0.75 to 2.0 (KOTH) / 1.25 to 3.0 (Sniper Showdown), DefaultSpeed 1.0 / 1.5 are per-stage speeds. static + data |
| FOUND | NorthAmerica Hot Zone height 85,000 | The NorthAmerica config stores no `ZoneShape` (all other configs store Cylinder); the enum default 0 is **Box**; its control zone Z extent is 50,000 and Hot Zone Z 85,000 (others 15,000 to 17,000). So the zone is stored as a tall box covering the city's height range; why 85,000 exactly is not stated. Box default is an inference from cooked-JSON omission. data |
| FOUND | Region containment/overlap | R3 (33 / 9 / 7 overlapping pairs; no overlap test in the selection). static + data |
| FOUND | Gym Hot Zone sizing | `DA_ControlZoneConfig_Gym_Minimal`: control zone cylinder extents 5000 x 5000 x 2500; **no Hot Zone extents are stored** (shape only); `MinHotZoneMoveDistance` 750, `MoveDelay` 25, inner radius 1.0, alternator off. data |
| FOUND | Map layouts beyond zone data (.umap) | Exist in the paks: `Frontend`, `Gyms/Minimal/Gym_Minimal`, `Worlds/{Europe,Kavkazi,NorthAmerica,Russia}`, `PocketWorldLevel`, `DiscoveryMap`, plus **39,442** World Partition streaming cells under each world's `_Generated_` folder (Russia 10,730, Europe 10,134, NorthAmerica 9,961, Kavkazi 9,617) and per-scenario/experience data-layer copies (`EDL`). List: `round40_modes/umap/rawfiles.txt` (40,631 files). Spawn points and building placements would be in these cells; **not extracted** (large; next step is `dump` of selected cells and a class filter for `PlayerStart`). |
| FOUND | Map areas (Saburtulo, Bakurani Outskirts, Africa) | Region polygon configs exist only for Kavkazi, Europe, NorthAmerica (R3), so Russia (Saburtulo) and Africa have **no regions data**; their zone configs have a single full-size cylinder (Africa 55,000, Russia 55,000 radius). Bakurani Outskirts has its zone config only for the Sniper Showdown variant (35,000). data |
| OPEN | AI detection combine | Searched: perception component callers, `WDAIThreatDetectionMonitorComponent` tick (`0x887D1D0`) shows only the fade (below); the code that raises detection from stance, movement and firing multipliers was not reached in the timebox. |
| OPEN | AI sight and hearing in play | Not reached (needs the stimulus handler that feeds the threat list `0x8877450`/`0x8878F70`). |
| FOUND | AI threat fade | `WDAIThreatDetectionMonitorComponent` tick `0x887D1D0`: for each tracked target, if `now > lastUpdate + TimeBeforeStartDecay` then `level -= DeltaTime x DetectionDecayRate`; an entry is removed when the target is gone or the level is 0 or less. So the rate is **per second**: the Blueprint's 0.25 empties a full level of 1.0 in 4 s after a 5 s wait; native defaults 0.01 per second after 10 s. static |
| FOUND | AI action order | Behaviour tree summary below. data |
| FOUND | AI alert thresholds | Thresholds (Relaxed 0.0, Alert 0.8, Combat 1.0, Combat needs line of sight to go up) are consumed by the alert-state decorator: `BT_WDAIPvECore_Base` root selector, first branch `AlertState == Alert` (re-evaluated on change, aborts both ways) with `AlertInterruptible` set: end job, then run `AlertedReaction`; `DefaultBehavior` picks attack only when `TargetActor` is set and the state is Combat with `HasLineOfSight`. data |
| OPEN | AI EQS fields | Not reached. |
| FOUND | AI blackboard key use (core set) | In the core trees: `TargetActor` is written by the `EQS_FindTarget` service every 1.5 s (no deviation) in `DefaultBehavior`; `LastAlertState`, `AlertInterruptible`, `HasLineOfSight` are read by decorators; `Cover` is written by `ReserveCover` and read by `HasValidCover`/`CoverChangeBodyStance`. Other trees (patrol, besiege, interact) not walked. data |
| OPEN | PvE team sizes, Hunter Killer side, mission rewards, mission names, VO durations, scenario units and logic | Not reached this round. |
| FOUND | ADS FOV option text | `DT_Settings_General` `UserSettings.General.FieldOfView.AimingMode`, "Aim Down Sight (FOV)": "Affected: ADS FOV is based on the user's FOV setting at low magnification levels (below 3.25x). Independent: ADS FOV is always based on a base FOV constant." data |
| FOUND | Key rebinding | `BHUserSettingsConfig`: `RebindExistingKeyMode = OneActionPerKeyPerCategory` (a key can serve one action per category), binding sources EnhancedInput and CommonUI; voice push-to-talk (proximity, squad) are "never ignored" input actions. config |
| FOUND | `IMC_*` input contexts | 27 mapping contexts registered with settings (player controller, mover player, aiming, base weapon, build tool, fists, inventory, interaction, UI keybinds, ladder, body drag, downed, falling, no-clip, parachuting, swimming, tipping, spectator, land / rotary / tracked / airplane vehicle drivers, mounted gunner, default vehicle inputs, vehicle active reload, projectile camera, drone projectile). List in `default-game-ini.json` `input.mappingContexts`. config |
| FOUND | Shooting range damage rule | `[MatchState.Playing.ShootingRange]` ignores the disable-damage flag for four classes: plain buildable, spawned buildable, buildable door, base vehicle pawn (`ActorClassPathsToIgnoreDisableDamage`). config |
| FOUND | Automation | `WDGameSettings` points to load-test profile tables `/Game/Tests/LoadTests/Data/DT_ServerTestingProfiles` and `.../DT_ClientTestingProfiles`; the config sets `NumInitialBots = 0` and 12 bot names (Adam, Betty, Colin, Doris, Edward, Frankie, George, Hillary, Ian, Jane, Kirk, Laura). Table contents not read. config |
| FOUND | Significance | `DefaultSignificance.ini`: animation budget on (`bAutoEnableAnimationBudget`), `BudgetInMs` 1.25, `MaxTickRate` 10, interpolation max rate 6, 16 interpolated components, look-at max angle 90, recently-rendered threshold 5.0; per-object significance comes from `DA_SignificanceSettings_*` assets (not read). config |
| FOUND | Other game-wide limits (not in the backlog) | `WDGameSettings`: proximity chat max distance 1500, team-local chat 10000, chat history 250, global interaction tap time 0.15 s, max shooter distance offset 200, player hit-detection bounds padding (2.5, 2.5, 1.0) standing, (3, 3, 1) prone and downed, `MaxSquadMembers`/`SquadLimit` 0 (data-driven elsewhere), squad name length 10. Units not stated. config |
| OPEN | Not reached (no search made): `BHUserSettingEnumDiscreteValues`, hashed names, `_aaa` fields, water grid, FluidFlux, MicroBiome, smoke VFX, gameplay-tag lists, mechanics units, `Percentage_Ongoing`, `EToolFonts`, units, explosion timing, characters, achievements, moving target, localisation, skins | The timebox went to modes, zones, the economy file and the AI trees. |

## AI behaviour tree order (`BT_WDAIPvECore_*`, read from `round36_ai/dump`)

`Base` (selector, blackboard `BB_PVEAI`): 1. if alert state is Alert (and `AlertInterruptible` is set) -> end the current job, run `AlertedReaction` (round 39: look at the stimulus, wait 2.0 s, find cover or peek). 2. Apply for a job (when the job state is not assigned). 3. When a job is assigned -> run the injected goal behaviour (`AI.Behavior.BTInjection_Goal`). 4. When no job is assigned -> `DefaultBehavior`.
`DefaultBehavior` (selector; service `EQS_FindTarget` -> `TargetActor` every 1.5 s): if `TargetActor` is set and state is Combat with line of sight -> `DefaultAttackTarget`; otherwise `Idle` (runs `Action.Player.Idle`).
`DefaultAttackTarget` (selector): `BT_CoverShooting`, then `BT_CoverSurfing`, then `BT_NonCoverShooting` (first that can run).
`BaseTakeCover`: release cover if asked; else reserve a cover, then (if valid) move to it with an enemy-avoiding nav filter while a parallel injected behaviour (`AI.Behavior.ActionParallelCoverMove`, default `BaseShooting`) shoots, then run the in-cover behaviour (`AI.Behavior.ActionInCover`, default `BT_Default_InCoverShooting`).
`BaseShooting`: reload if out of ammunition (`BaseReload`), then `ShootAtTarget` with 3 rounds of bursts. `BaseReloadInCover`: change body stance in cover, then `BaseReload`.

## Counts

Backlog table rows: FOUND 22, OPEN 6 (first-spawn route order, AI detection combine, AI sight and hearing, AI EQS fields, the PvE group, and the unreached UI/Other list of about 21 sub-items). Native-code results are reported as FOUND with evidence level static; separate NATIVE rows 0, SERVER 0, ABSENT 1 (faction backstory, noted inside the Factions row). The six asked-for items R1 to R6 are all FOUND, so 28 FOUND in total.

## Reproduce

- Zone layout and region code: `corpus.sqlite` -> `functions` by RVA (`0x77646F0`, `0x776C740`, `0x776E780`, `0x77698A0`, `0x8458DA0`, `0x84599B0`, `0x776DB20`); tag strings via `search`.
- Deathmatch spawn `0x8490260`, `0x8493480`; ammo `0x8495620`, tag init `0x129E190`; stillness `0x8646E50`, `0x864B140`, `0x864DFA0`, `0x8647140`, `0x86478A0`; pre-lobby `0x8640D40`, tag init `0x128B090`, `0x1271930`; threat fade `0x887D1D0`. vtable differences: compare the component's `_VFT::slot_N` aliases with its base class.
- Data: `python -I _tools/default_game_ini.py --check`, `python -I _tools/zone_selection.py --check`, `python -I _tools/mode_rules.py --check`.
- Config: `WdExtract ... rawfiles Wardogs/Config --copy` (round 39); maps list: `WdExtract ... rawfiles .umap` (list only).

## Wiki updates (round 40)

- `_wiki/game-modes-and-maps/king-of-the-hill.md` -> win condition: "default 10 points" -> "the match ends when a team reaches **100 points** (server default); points are added every 22 s (24 s in the example server file); there is no time limit".
- `_wiki/game-modes-and-maps/king-of-the-hill.md` -> lobby: add "a match starts when 60 players have joined (waits up to 10 s), or 9 players after the ready-up step (5 s)"; server player cap between 60 and 100 (server setting).
- `_wiki/game-modes-and-maps/deathmatch.md` -> "No time limit in the data" -> "30 minutes (1800 s) time limit as well as the 75 kill score limit"; spawning "native code (no data)" -> "you respawn at the spawn point furthest from all enemies"; ammunition "not in the data" -> "choosing a weapon gives the weapon and four magazines (spare/loaded split not decoded)".
- `_wiki/game-modes-and-maps/sniper-showdown.md` -> round length "not in the data" -> "30 minutes or 10 kills"; stillness: "Standing within about 50 m (distance unit assumed) of one spot for 90 s reveals you on the map for 200 s (at most three reveals shown); you get a warning at 75 s and a 15 s grace before the check restarts."
- `_wiki/game-modes-and-maps/zone-layouts.md`, `control-zone.md`, `bakurani.md` -> layout choice: add the order (named by the server rotation; else an optional server queue by map count; else random weighted by layout weight; weight-0 layouts are never drawn at random); `Bakurani.River` in the example rotation has no layout in the game files, so it picks a random Bakurani layout (50% Default, 25% Farmland, 25% Lumberyard).
- `_wiki/game-modes-and-maps/zone-layouts.md`, `bakurani.md` -> regions: "how a region is picked" -> "the Hot Zone moves to a randomly chosen region weighted by region weight; the region just used gives away half its weight to the others so it is unlikely to repeat; towers have weight 0 and are never picked at random"; region overlap exists (33 pairs on Bakurani, 9 on Europe, 7 on North America) and is harmless; Russia and Africa have no region data.
- `_wiki/game-modes-and-maps/zone-layouts.md` -> Hot Zone movement: "about every 25 s in King of the Hill (data value; a runtime scale not identified)"; the Hot Zone is placed immediately at the start.
- `_wiki/game-modes-and-maps/zone-layouts.md` / North America page -> the 85,000 height: "North America's zone is stored as a tall box (no cylinder shape), 85,000 high for the Hot Zone".
- `_wiki/game-modes-and-maps/hot-potato.md` and the Server Seeding / pre-lobby text -> "what the award buys is not decoded" -> "At match start the pre-lobby points are paid out as starting Cash and give a first-purchase discount (the economy file lists a 90 multiplier for it)".
- `_wiki/game-modes-and-maps/factions.md` -> add "Lonestar (blue), Valkyra (red), Manticore (green)"; "whether factions differ in weapons" -> "each faction's signature 5.56 rifle is free for that faction (Lonestar WEPN_033, Valkyra A91, Manticore KH2002)".
- `_wiki/game-modes-and-maps/ai-enemies.md` -> threat fade: "rate 0.25 per second after 5 s; a full detection level fades in 4 s"; action order: add the tree order above (alert reaction, job, goal, default behaviour; attack only in Combat with line of sight; cover shooting then cover surfing then open shooting; bursts of 3; reload when empty).
- `_wiki/progression-and-economy/` (vendor / prices page) -> add the price modifiers: new Wardogs (level 8 or lower) multiplier 50, losing team by 40 points 80, first purchase 90, faction signature rifles 0, refunds 0.9 (multiplier reading as percent of price is an inference).
- Settings page -> ADS FOV option text as in the table; key rebinding rule (one action per key per category); chat distances (proximity 1500, team 10000).
- Maps page -> "level layouts not in the export" -> "level files exist (four worlds, Frontend, Gym); the actor data is in 39,442 streaming cells not yet extracted".
