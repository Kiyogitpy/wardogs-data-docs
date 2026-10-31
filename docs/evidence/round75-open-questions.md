# Round 75: open questions on the deployment board, keycards, the VIP Escort helicopter, starting Cash and Tevza (R75-RE)

Static analysis only. Nothing was run, the protection layer was not touched (every function below is outside it; nothing is PROTECTED). Evidence levels: static disassembly of `WardogsClient-Win64-Shipping.restored.exe` with capstone (`rdis.py`, `rxref.py` of `E:/Reverse_Engineer/wardogs_analysis/round40_veh/`), the decompiled corpus (`corpus.sqlite`, helper `dec.py` printing a function by RVA), cooked data read with `WdExtract` (`dump`, `findname`, `schema`), the SDK headers and the exported JSON of rounds 36, 45, 53, 67, 69, 70 and 71. Raw output and scripts are under `E:/Reverse_Engineer/wardogs_analysis/round75_re/` (outside the repository): `rej.c`, `respawn.c`, `tick.c`, `ctor.c`, `deploycheck.c` (decompiled functions), `bd/` (board Blueprints re-dumped), `sch/`, `sch2/` (usmap layouts), `fn_*/` (name-map searches), `vip_pins.txt`. RVAs are relative to the image base `0x140000000`.

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Reader of the board rejection reasons | FOUND | `0x770C7B0` walks the `RejectionRules` array (seven 16-byte rules, written by the board constructor, not by any asset): priority, tag, rule type. The highest priority rule that fires names the reason. |
| 1b | `MinRequiredScore` 20 | FOUND | Gates the `ScoreRequired` reason and the APC (re)spawn: the board puts out its APC only once some side's score is 20 or more (`0x770EF10` calling `0x770ABA0`). |
| 1c | `LosingScoreThreshold` 15 and "losing" | FOUND | At the moment the APC is lost, the side is losing when the best other side's score minus its own is 15 or more (`0x770E900`). |
| 1d | 300 s and 60 s timers | FOUND | Chosen in `0x770E900` (the board's spawn-vehicle-destroyed handler); they time the deployment APC only. Scaled by a server value that defaults to 1.0. |
| 1e | `VehicleSpeedThreshold` 10 | FOUND | `Driving` reason when the APC's speed is 10 km/h or more (the speed getter multiplies cm/s by 0.036). |
| 1f | `RadarRestoreHealthThreshold` 0.55 | FOUND | Radar-destroyed flag: set when the radar health attribute reaches 0, cleared when it is 55 percent of its maximum or more (`0x770DF00`). |
| 1g | `VehicleHealthThreshold` 0.3 | ABSENT (no consumer) | No function reads it. The `LowHP` tag and text exist but no rule uses them. |
| 1h | `PlayerDeployCooldown` 600 | FOUND | Written per player when a deployment seats the player (`0x6E6C500` calls `0x770EC80`); shown as the `Cooldown` reason. |
| 2 | Keycards: anything that accepts them | ABSENT (placed use) / NATIVE (reader class) | The code has a keycard reader class with a door link and a scan action; no map, mission, Blueprint or quest names the reader or a card. |
| 3 | VIP Escort helicopter "entry points" | FOUND | Three entry nodes (Alpha, Bravo, Charlie) in the helicopter sub-quest are three factions, not three places. VIP Escort wires the Bravo pin only; Strike and Disarm wires the Charlie pin only. |
| 4 | Where `InitialBalance` is applied | FOUND (function), NATIVE (condition), SERVER (live balance) | `0x6D61030`, at join (player data initialisation), only when the game mode does not keep Cash between matches. The `OverrideStartingCash` setting does not exist in this build. |
| 5 | Tevza spawn points | ABSENT | None of the three unlayered spawn managers is Tevza's: all three are the PvE scenario spawn areas (exact coordinates). Tevza's four layers have no actor in any cell. |

## 1. The deployment board

### Method

Board class `AWDVehicleDeploymentBoard`, vtable `0xB690390`, constructor `0x7708A00` ([round 53](round53-spawn-board-defaults.md)). Round 53 scanned the 0x76F0000..0x7730000 range for loads of the threshold offsets and stopped at 0x770C7B0, 0x770EF10 and others without tracing them. This round decompiled every board function that touches the relevant offsets (`rej.c`, `respawn.c`, `tick.c`, `ctor.c`) and followed the callers.

Field offsets used below: `+0x3F8` VehicleHealthThreshold, `+0x3FC` RadarRestoreHealthThreshold, `+0x400` VehicleSpeedThreshold, `+0x404` MinRequiredScore, `+0x408` VehicleRespawnTimer, `+0x40C` LosingVehicleRespawnTimer, `+0x410` LosingScoreThreshold, `+0x418` PlayerDeployCooldown, `+0x428` RejectionRules, `+0x438` tag container, `+0x458` RejectionReasonTag (decimal 1112 in the decompile), `+0x460` CurrentSpawnVehicle, `+0x468` DeploymentCooldowns, `+0x478` game state, `+0x54C` respawn time left, `+0x550` respawn running flag, `+0x554` respawn finish time, `+0x568` radar-destroyed flag. `AWDFaction` (`Score` at `+0x2B8`) is the object the score reads use; the array they walk is `GameState.Factions` (`+0x448`, accessor `0x6DA29C0`; `0x1BFF8F0` returns `Faction.Score`).

### 1a. The rule table (constructor, `ctor.c` lines 520 to 600)

`RejectionRules` is empty in the Blueprint (the cooked `B_VehicleDeploymentBoard` holds only the three-tag container at `+0x438` and the two overrides; its name map has no `NoVehicle`, `ScoreRequired`, `Respawning`, `RadarDestroyed` or `Cooldown` tag, checked with `findname`). The constructor adds seven rules `{Priority, Tag, RuleType}` (struct `WDDeploymentRejectionRule`, enum `EWDDeployRule`). Tag names come from the registration functions `0x1297610..0x1297C50` (tag globals `0x14D36BC30..BC80`).

| Priority | Rule type | Tag | Text in [`DT_DeploymentRejectionReasons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/DeploymentBoard/Data/DT_DeploymentRejectionReasons.json) |
|---:|---|---|---|
| 100 | Respawning | `Interactive.Deployment.Rejection.Respawning` | Spawn Vehicle will respawn in {Minutes}:{Seconds} |
| 90 | ScoreRequired | `...Rejection.ScoreRequired` | Inactive Vehicle: Min Required Game Score: {Score} |
| 80 | NoVehicle | `...Rejection.NoVehicle` | No Active Spawn Vehicle |
| 70 | RadarDestroyed | `...Rejection.RadarDestroyed` | Spawn Vehicle Radar Destroyed : Awaiting Repairs |
| 60 | ExternalProviders | `...Rejection.NotInControlZone` | Spawn vehicle is not in the control zone |
| 50 | Driving | `...Rejection.Driving` | Spawn vehicle is moving |
| 40 | NoSeat | `...Rejection.NoSeat` | No available seat |

`0x770C7B0` evaluates each rule by type and keeps the tag of the highest priority rule whose test fires; with none it returns the empty tag, which the tick turns into `Interactive.Deployment.Available` ("Deployment Available"). Tests:

- Respawning: flag `+0x550` set and `+0x54C` > 0.
- ScoreRequired: fires when there is no live APC (none, destroyed or in water) and no faction has `Score >= MinRequiredScore`. A live APC (present, not destroyed, not in water) clears it.
- NoVehicle: `CurrentSpawnVehicle` missing.
- RadarDestroyed: flag `+0x568`.
- Driving: `abs(vehicle speed) >= VehicleSpeedThreshold` (vehicle vtable slot 313, `0x53CAE30`: velocity length in cm/s times 0.036, so km/h).
- NoSeat: the seat component reports no free seat (`0x532D3C0` counts empty seats).
- ExternalProviders: asks registered providers (`0x770E590`; the Control Zone feature provides `NotInControlZone`).

`LowHP` (`...Rejection.LowHP`, "Spawn vehicle has too low HP") has a registered tag (`0x14D36BC38`), a text row and a place in the container, but no rule in the table and no read of it in any function of the corpus (searched for all references to the tag global).

The per-player layer is `0x770D1F0` (the reflected `GetEffectiveRejectionReasonForPlayer` body is `0x7710520`): when the board reason is empty or Available, a player who has not entered the control zone gets `PlayerNotEnteredControlZone` ("MAP OFFLINE... ENTER ZONE FOR DATA"), a player with an active cooldown gets `Cooldown` ("Deployment on cooldown - {Minutes}:{Seconds}"), otherwise Available. When the board reason is something else, an active cooldown replaces it only if the reason is in the three-tag container (`Driving`, `LowHP`, `NoSeat`); the other reasons show as they are. The deploy request function `0x6E699E0` lets the player through when the reason is Available **or Driving** (it compares against both globals before calling the seating function `0x6E6C500`), so the "moving" message reads as a warning that does not block (decompiled; the third argument of the call is not shown by the decompiler, and nothing was seen in play).

### 1b. MinRequiredScore (20)

Two readers. (1) the ScoreRequired rule (above). (2) the board tick `0x770EF10` (server only): when the board has no live APC (none, destroyed or in water), a faction has `Score >= 20` and the respawn countdown flag is clear, it calls `0x770ABA0`, the asynchronous APC spawn (loads the vehicle class for `SpawnVehicleTag` at `+0x41C` and spawns it). No other function calls `0x770ABA0`. So the board does not put out its APC until the first side reaches 20 points; before that the board shows the ScoreRequired text. Faction scores only rise during a match (inferred), so the gate opens once.

### 1c to 1d. Losing and the two timers (`respawn.c`, `0x770E900`)

`0x770E900` runs when the spawn vehicle is lost (called from `0x7711300`; it clears `CurrentSpawnVehicle`, raises the destroyed event and starts the countdown). It reads the board's own faction object (virtual call at `+696`), takes its `Score`, finds the highest `Score` among the other entries of `GameState.Factions` (the running maximum starts at its own score), and sets `losing = (best other - own) >= LosingScoreThreshold (15)`. It then picks `*(float*)(board + 0x408 + 4 * losing)`: 300 s when not losing, 60 s when losing. The result is multiplied by a float from the reward subsystem (`0x6CB9970`, session value of the tag `Challenges.Rewards.MatchScoreScalar`, default constant 1.0 when absent; the live value is not in the client, SERVER). The product goes to `+0x54C` (time left) and, plus the server time, to `+0x554` (finish time); `+0x550` is set. The tick subtracts the frame time from `+0x54C` and clears the flag at 0, which lets the spawn gate in 1b fire again.

The handler belongs to the board and handles `CurrentSpawnVehicle` only, so the 300 s and 60 s timers govern the deployment APC and nothing else. No function reads `+0x408` or `+0x40C` anywhere else.

### 1e to 1f. Speed and radar

Speed threshold: see the Driving rule (10 km/h; round 53 left the unit open). Radar: `0x770DF00` is the attribute-change handler of the spawn vehicle's `Attribute.Gameplay.Health.Radar` (tag global `0x14D2E7A30`, registration `0x11FF1F0`). When the radar value reaches 0 it sets the `+0x568` flag; when the value is at least `RadarRestoreHealthThreshold` (0.55) times the radar's maximum it clears the flag; in between it keeps the previous state. The flag feeds the RadarDestroyed rule (priority 70).

### 1g to 1h. Health threshold and cooldown

`VehicleHealthThreshold` (`+0x3F8`) is read by no function of the board class, the deploy functions or anything else with the board tags (full-corpus search for the offset in functions that also read `CurrentSpawnVehicle`, plus the board range read line by line). ABSENT as a consumer; the LowHP reason can never be produced by the shipped rule table.

`PlayerDeployCooldown` (`+0x418`, 600 s on the live Blueprint): `0x770EC80` appends a `WDDeploymentCooldown` entry `{player net id, server time + cooldown}`; its only caller is the seating function `0x6E6C500`, after a seat was found for the deploying player. A second field pair (`+0x558` byte, `+0x55C` float 5.0 set by the constructor) would replace the 600 s with 5 s when the byte is set; nothing writes the byte, so it is unused in the shipped code.

## 2. Keycards

- Cooked data: `findname` over every package under [`Wardogs/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs) (149,124 files mounted) for [`Keycard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Keycard/Content/Keycard.json) and `KeyCard` returns 30 packages, all in the Keycard feature plus the two input assets ([`IA_KeyCard_Use`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IA_KeyCard_Use.json), [`IMC_Action_KeyCard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IMC_Action_KeyCard.json)). No world cell, quest, Blueprint, data table or scenario names a card tag (`Id.Item.KeyCard.*`). `findname` for `KeycardReader` and `KeycardRuntime` returns 0 packages. The Keycard plugin holds no map content (34 files: items, anim sets, one mesh, one material, one texture, the `EDL_Keycard` layer asset and the plugin descriptor).
- Native code: a module `KeycardRuntime` exists (SDK `KeycardRuntime_classes.hpp`). `AWDKeycardReader` is an actor with a skeletal mesh, a collision box, a `KeycardValidationComponent`, a `KeyCardReaderDoor` actor reference and a `KeyCardReaderDependencies` array. `UWDKeycardValidationComponent` has `KeycardAlignment` (faction tag), `KeycardNumber` and the server call `Server_TryValidateKeycard`, with result states None, Success, IncorrectAlignment, IncorrectNumber. The use action (`UWDItemExtension_Keycard::TryActivateKeycardScanner`, `0x88A77F0` into `0x88A7400`) traces 100 cm (1 m) from the player's view; if the hit actor has a validation component it submits the card. So the code can open a door from a reader that compares the side and the number, but the shipped data places no reader and subclasses none (no Blueprint derives from the reader; the class is not an asset).
- Status: ABSENT for any placed reader, door, quest or Blueprint use; NATIVE for the unused reader class. What a success does to the door is not read.

## 3. VIP Escort helicopter entry options

`SQ_Extraction_Helicopter` (round 36 graph, round 45 section 14) has three `SDQuestNodeFlowControl_Entry` nodes named Alpha (node 0), Bravo (14) and Charlie (15). Each leads to a `SpawnVehicle` node for `Vehicle.Variant.Air.Rotary.Littlebird.Default` with `VehicleFactionTag` Alpha, Bravo or Charlie; all three spawn at the same point tag (`QuestObjective.BaseScenario.Extraction.Vehicle`), join in one OR node and continue on the same entry path. So the three "entry points" of the old wiki are three **factions**, not three places; the map layer holds one entry path, as round 71 found.

How one is chosen: the parent mission's `PlayQuest` node has one input pin per entry node, named Alpha, Bravo, Charlie, each pin carrying the entry node's `NodeId` GUID (`vip_pins.txt`: pin GUIDs equal the entry node GUIDs, for example Bravo `85C06AEF-40F1F52F-AF1F52AB-1BCCBF42`). The starter `0x86FDE50` matches the sub-quest node whose GUID equals the wired pin's GUID and sets it as the entry (`0x86FB200`); there is no random choice and no runtime test. In `Q_VIPEscort_01` node 10 only the **Bravo** pin (`SDQuestNodePin_13`) is connected (from the extraction-proximity wait). In `Q_StrikeDisarm_01` node 9 only the **Charlie** pin (`SDQuestNodePin_18`) is connected. This matches the player faction tags of the two missions (Bravo in VIP Escort, Charlie in Strike and Disarm; round 71 and the spawn data). Result: VIP Escort always gets the Bravo-tagged Little Bird, Strike and Disarm the Charlie-tagged one.

## 4. Starting Cash

- `FWDCurrencyDefinition.InitialBalance` (`+0x20`) is read by exactly one function, `0x6D61030` (the only caller of the struct's StaticStruct getter `0x69B7A60`). It reads the data registry item for the Cash tag (`DR_CurrenciesDefinitions` -> [`DT_CurrenciesDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json), Cash row 10,000), builds one attribute entry `{Cash tag, minimum = InitialBalance, maximum = InitialBalance}` and applies it through the player state's virtual at `+2120`, then sets the "player data ready" flag (`+1100`). Its caller `0x6D5B4E0` is an asynchronous continuation of the player-data request (`0x6D682A0`, which asks the `WardogsOnlineServerPlayerDataInterface` for the player's saved data). Object: `AWDPlayerState` (the attribute component at `+0x3D0` is its `GameplayEffectComponent`).
- When: at join, when the player's data is initialised. Not at match start (round 70 found no Playing subscriber that sets it) and not in the pre-lobby.
- Condition: the grant happens only when the authority game mode's keep-Cash flag is false. `AWDGameMode` slot 300 (`0x6D39640`) returns `bPersistCash` (`+0x358`), whose constructor default is **true** (`0x69C6FA0` writes 1); `AWDGameModeSession`'s override (`0x6D9B4F0`) returns it only when the net mode is not standalone. No Blueprint derives from `WDGameModeSession`, `DefaultGame.ini` has no `bPersistCash` line, so on a networked server the flag is true and the function takes the other branch (the saved player data from the online service, `0x6D682A0`). The grant therefore applies in standalone or editor runs (and to any mode that clears the flag); on a live server the balance comes from the saved data. This agrees with the in-game tip that Cash carries between matches ([currencies](../../_wiki/progression-and-economy/currencies.md)). What the saved balance is for a new account is SERVER; the same table is the source of the backend's `Pragma_Content_CurrencySpec` (`InitialAmount`) per round 36 (inferred link).
- `OverrideStartingCash=-1` in `DefaultGame.ini` ([round 40](round40-modes-ai-other.md)) has no matching property in this build: it is absent from the `WDGameModeSession` layout of the usmap (`sch2/usmap_schema.json`) and from `GObjects-Dump-WithProperties.txt` (which lists `ScenarioStartingCash` only). The line is a stale config entry; the session cannot override the starting balance with it. ABSENT.
- Scenario cash (`ScenarioStartingCash` 3,000 and 2,000) is a separate field of the scenario data; its consumer was not traced here.

## 5. Tevza

- Experience [`Tevza_KOTH_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Config/Experiences/Kavkazi/Tevza_KOTH_01.json) enables `DL_Tevza`, `DL_VostimiSpawn`, `DL_EdemiSpawn`, `DL_ShovliSpawn` ([round 67](round67-maps.md)). The Kavkazi world package holds the four data layer instances (`WorldDataLayers`), and that is the only place the names occur: re-read from the persistent-level export (43,117 exports), no actor references the Tevza layer instances; in the cell index (9,621 cells, `round67_re/cells_dl_Kavkazi.json`) the layers in use are `STAGE_Blockout`, `DL_Baghi`, `DL_Chuta`, `DL_Khevuli`, `DL_Rachuri`, `DL_Liknisi`, `DL_Sanavi`, `DL_Tavarshi` and `DL_Destruction`; none is a Tevza layer.
- The three spawn managers without a layer (round 67): (-7,754, -7,450), (-12,410, -9,736), (-8,890, -11,355) m. Round 71 placed exactly these as the player spawn areas of the PvE scenarios: VIP Escort (-7,754, -7,450), Strike and Disarm (-12,410, -9,736) and the example scenario (-8,890, -11,355). They sit in the scenarios' external data layers, so none is Tevza's.
- Result: Tevza has no placed spawn point of its own. ABSENT (settled by exact coordinate match).

## Reproduce

```
python dec.py 770C7B0     # rejection reasons;   770E900 respawn handler;  770EF10 tick;  770DF00 radar
python dec.py 7708A00     # board constructor: rule table near the end
python rdis.py 53CAE30 80 # speed getter (x0.036 constant at RVA 0xAB73570)
python dec.py 6E699E0     # deploy request;  6E6C500 seating;  770EC80 cooldown
python dec.py 6D61030     # InitialBalance reader;  6D39640 / 6D9B4F0 keep-Cash flag
wx.sh fn_x findname Wardogs/ KeycardReader      # 0 packages
wx.sh fn_x findname Wardogs/ KeycardRuntime     # 0 packages
```

## Wiki updates

- `_wiki/game-modes-and-maps/maps.md`, the four map articles ("Limits and timers"), `_wiki/vehicles/m113-apc-sv.md`, `_wiki/guides/king-of-the-hill-guide.md`, `_wiki/guides/vehicle-guide.md`: the "inferred" timers become read: 300 s or 60 s when the side trails by 15 points, timing only the deployment APC; 600 s cooldown starts when you deploy; the APC is not out until a side has 20 points; board messages and their triggers.
- `game-features/Wardogs_VehicleSpawns_v1.md` through `_tools/vehicle_spawns.py`: the refusal sentence and the timer bullets.
- `_wiki/equipment/keycards.md`: reader class exists in the code, none placed.
- `_wiki/game-modes-and-maps/vip-escort.md`, `strike-and-disarm.md`, `pve-scenarios.md`: the helicopter's team is fixed by the mission.
- `_wiki/game-modes-and-maps/pre-lobby.md`, `_wiki/progression-and-economy/currencies.md`: the starting Cash is applied at join and only when Cash is not kept; the server setting does not exist.
- `_wiki/game-modes-and-maps/zone-layouts.md`, `maps.md`: Tevza's three unlayered spawn points are the PvE ones.
