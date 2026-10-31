# Round 67: Hot Zone Magnet towers, magnet positions, map extents, server-browser-only entries (R67-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (extractor `dump` of Blueprints, data assets, World Partition cells and landscape components), decompiled-corpus reading (`E:/Reverse_Engineer/wardogs_analysis/decompiled_cl516586_20261017_mmvpuc__`, RVAs, image base 0x140000000) and a read of the restored image's `.data` for one static. No protected (virtualized) code was devirtualized, and nothing below needed it: no row is PROTECTED. Method follows rounds 65 and 66 ([round65-open-questions.md](round65-open-questions.md), [round66-map-actors.md](round66-map-actors.md)). Raw output and scripts are under `E:/Reverse_Engineer/wardogs_analysis/round67_re/` (outside the repository): `pp.py` (Blueprint bytecode printer), `fx.py` and `show.py` (corpus function reader), `rd.py` (restored-image reader), `reg.py` (region polygons), `land.py` and `land2.py` (landscape components), `dlmap.py` (cell to data layer map), `extents.py`, `build.py` (summary), `apply_wiki.py`. The committed summary is [map-magnets-extents.json](../../assets/data/map-magnets-extents.json).

## Statuses

| # | Question | Status | One line |
|---|---|---|---|
| 1a | How a magnet (tower) is captured | FOUND (data) and NATIVE (rule) | Hold 10 s within 2.5 m, one player at a time; refused if the tower is already your team's, is cooling down, or a magnet is running. |
| 1b | Who can capture | NATIVE | Any player whose team differs from the tower's owner; the reward goes to alive, non-critical players of the capturing team within 80 m. |
| 1c | How long | FOUND | 10.0 s hold (capture); 0.3 s per keypad tap. |
| 1d | Hostile and neutral | NATIVE (inferred) | Neutral = no previous owner; hostile = another team owned it. The event carries the previous owner; the reward comparison bindings were not traced. |
| 1e | What a magnet does to the Hot Zone | FOUND and NATIVE | A correct code activates that tower; all towers take the activator's team; the Hot Zone is pulled to it at 3 m/s at 0.6 of its size for 180 s; the "Magnet activation 5,000" cash row is the flat table row for this event. |
| 1f | Cooldown | FOUND | 900 s recharge from deactivation; 30 s keypad lock after 3 wrong codes; 180 s reward repeat cooldown. |
| 2 | Magnet positions vs regions | FOUND | Every tower sits in a named region (Bakurani 1 to 4, Ozeti 1 to 4 and Zestafona 1 to 3 in regions "Tower N"; Bakurani 5 in Lumberyard North). Saburtulo: no region list, ABSENT. |
| 3 | Play box and terrain height range | FOUND (component resolution) | Landscape 16.32 km square on all four maps; play box and ground ranges below. Saburtulo play box is a stand-in. |
| 4 | Server-browser-only entries | FOUND (structure), inferred (use) | No zone config of their own; they share their world's single zone object, so their zone area is the main map's (distance 0). Own spawn areas listed. Tevza has none placed. |

## 1. Hot Zone Magnet towers

### 1.1 What the placed object is

Round 66 inferred that the 5, 4, 3 and 5 placed `B_HotZoneMagnet_C` actors are the towers behind the "hostile tower 1,000 / neutral tower 250" rewards. That is now settled by the Blueprint and the native class: the actor is `AWDHotZoneMagnet` (`HotZoneMagnetRuntime`) with `HotZoneTowerNumber`, a faction component, a world interactable (capture), and a spawned `B_HotZoneMagnetInput` actor that carries a keypad widget. The player-facing names are "Tower N" and "Drill N active" (strings in `W_HotZoneMagnet_Display`, [`DA_Tracker_Map_HotZoneMagnetTower`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DA_Tracker_Map_HotZoneMagnetTower.json)). The buildable Drill Rig (`BuildablesRuntime.WDBuildableHotZoneMagnetActor`) is a different class that feeds the same `WDHotZoneMagnetGameStateComponent`.

### 1.2 Capture. FOUND and NATIVE

- **Data.** [`DA_HotzoneMagnet_Interactions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DA_HotzoneMagnet_Interactions.json) (`Interaction.Context.WorldFeatures.TowerControl`): `InteractionBehavior` Hold, `InteractionDuration` 10.0, `InteractionRange` 250.0 (cm), `bAllowMultipleInteractors` false, `bSendFailureRPC` true. Context class `WDHotZoneMagnetInteractionContext`.
- **Success handler.** Vtable slot 91 of `UWDHotZoneMagnetInteractionContext_VFT` is `0x8570B60` (authority only: `*(a+368)==3`). It posts a `WDHotZoneMagnetInteractionEvent {PreviousFaction, InteractingFaction, HotZoneMagnet, Interactor}`, sets the tower's faction component to the interactor's faction (`0x146B38880`), and calls `0x8570020`, which posts the tower-captured message with the tower number and location to the game state component.
- **Access check.** Slot 100 is `0x8567F70`. It lets the interaction through only if: the tower's faction tag differs from the player's, the tower's faction tag differs from the cooldown tag `qword_14D3E5248` (the tag `0x856A060` writes to every tower when a magnet ends), and the game state's `ActiveHotZoneMagnetTowerNumber` (+0x110) is 255 (no magnet running). Reading of the control flow; the JUMPOUT target `0x147743E90` is the shared "allowed" tail (inferred from the structure, not traced).
- **Cooldown tag.** `0x856A060` sets every tower's faction to `qword_14D3E5248` and the contested faction (+784) to None, and replicates the change. `W_HotZoneMagnet_Display` shows "COOLING DOWN" for it. Faction colour dispatch at `workers/05/code/085.c:12596` treats three cases: `qword_14D3E5248`, None and a real faction.
- **Contested faction.** `FactionCurrentlyCapturingTower` (+0x310) is replicated and used for the map tracker's contested colour while a hold is in progress.

### 1.3 Reward on capture. FOUND

[`ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_TowerCaptured`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_TowerCaptured.json) listens for the interaction event. Its enter conditions: the rewardee is inside the tower range (`WDStateTreeActorInTowerRange`, using `GetHotZoneTowerRewardRange`), not `State.Player.Vitality.Critical` and not `State.Player.Vitality.Dead`, plus tag and object comparisons whose property bindings were not traced (rewardee faction against the interactor's, and the previous-owner test). A task adds `Challenges.Context.HotZoneMagnet.Hostile` ("Add Hostile Tower To Context") and `...Instigator`; `RepeatActionsCooldown` is 180.0. `HotZoneTowerRewardRange` is 8000 cm (80 m), the constructor default in `0x8565CF0` (`*(a+764)=0x45FA0000`); the placed actors carry only `HotZoneTowerNumber`. Reward values (cash 250 base, hostile x6 in the challenge table; flat table 1,000 hostile and 250 neutral) were found in rounds 38 and 42.

Hostile and neutral: the event struct carries `PreviousFaction`. Neutral is the case with no previous owner, hostile the case where another team held the tower. The comparison itself sits in unbound state-tree property bindings, so the exact test is inferred.

### 1.4 The code. FOUND and NATIVE

- **Generation.** `0x856D9A0` (server): for each registered tower it appends one random byte `0..9` (`(rand() & 0x7FFF) * 0.000305185`, clamped to 9) to `GameStateComponent+296`, then spawns one `WDHotZoneMagnetDataCoordinator` per faction whose replicated `Code` starts as all `0xFF` bytes, then calls `0x8573500`. It runs at match start and, via the timer callback `0x8570430`, when the recharge ends. So the code has one digit per tower: 5, 4, 3 and 5 digits.
- **Visible digits.** `0x8573500` rebuilds each faction's `Code`: tower i's digit is copied if that tower's faction tag equals the faction, else `0xFF`. If the tower count is at least `dword_14CF377C8` (4 in the restored image's `.data`, read statically; the only reader is `GetNumTowersToShowPartialCode` and this function), the array with blanks is written; if it is lower, the array is written only when every tower is owned. The tower screen string "ALL TOWERS REQUIRED FOR CODE" in `W_HotZoneMagnet_Display` fits this. Zestafona (3 towers) falls below the threshold.
- **Keypad.** [`DA_HotzoneMagnetHitInput_Interactions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DA_HotzoneMagnetHitInput_Interactions.json): Tap, 0.3 s, range 250 cm, `bSendSuccessRPC` true. The keyboard widget has keys 0 to 9, CLEAR and ENTER. `Server_HotZoneMagnetKeyPressed` (slot 159, `0x8572A20`): a multi-character key string submits the buffer (`0x8568060`), an empty string clears it, a single digit is appended while the buffer is shorter than the code. Reading of the string-length tests; the key strings themselves live in the widget.
- **Submit.** `0x8568060` compares the typed string with the server code string (`0x856C920`). Equal: `ActivateHotZoneMagnetTower` (`0x85674A0`). Not equal: the buffer clears and `+808` (attempts) increments; at `>= HotZoneMagnetCodeMaxAttempts` (+772, constructor default 3) it marks that tower locked in the game state array (`0x8571050`) and starts a timer of `HotZoneMagnetCodeAttemptsTimePenalty` seconds (+768) whose callback `0x8572CC0` unlocks it and resets attempts. Blueprint `B_HotZoneMagnet` sets the penalty to 30.0 (constructor default 5.0); `HotZoneMagnetCodeMaxAttempts` is not overridden, so 3.
- **Access check for the keypad.** Slot 100 of `UWDHotZoneMagnetCodeInteractionContext_VFT` is `0x8567DE0`: the tower must not be locked (`0x856D000`), its faction tag must not be the cooldown tag, and no magnet may be running. It does not compare the typed-in team with the tower's owner (reading of the control flow, inferred).

### 1.5 Activation and the Hot Zone. FOUND and NATIVE

`0x85674A0` (authority): posts `WDHotZoneMagnetActivatedEvent {tower, instigator}`; for every tower unlocks it (`0x8572CC0`), clears it (`0x856A060`) and sets its faction to the activating pawn's faction; then calls `0x856FE50` with the tower number and location (the Hot Zone move, round 45 and 46: extents x `(0.6, 0.6, 1.0)`, speed 3.0 m/s, travel time added to the active time). `ActivatedHotZoneMagnetDuration` is 180 s. Deactivation `0x8570080` sets `ActiveHotZoneMagnetTowerNumber` to 255, posts `WDHotZoneMagnetDeactivatedEvent`, clears towers and starts the recharge timer of `TowerControlRechargeDuration` (900 s) times the world time dilation; the callback `0x8570430` runs the code generation `0x856D9A0` again (new code, tower reset message). `bCanDeactivateMagnet` (+0x2F8) is false in the constructor for these towers.

The "Magnet activation 5,000" cash is [`DT_Reward_Cash_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet/DT_Reward_Cash_HotZoneMagnet.json) MagnetActivated; the challenge row pays 2,500 cash and 500 Role XP to players in range (round 42). Which player the flat 5,000 goes to is not stated in the data. Whether towers return to neutral when the recharge ends was not traced (the reset message at the end of `0x856D9A0` is sent to each tower; its handler was not read).

### 1.6 Open items

- ABSENT: the property bindings of the state tree's hostile and faction comparisons (state-tree binding tables are not decoded).
- The 4-tower threshold is a static in `.data`; whether a console variable changes it at run time was not checked.
- No PROTECTED code was met in this module.

## 2. Magnet positions. FOUND

Positions are world metres from the cell data; the zone area centre is the centre of the bounding box of all region points. Full numbers (x, y, z, offsets) are in the JSON.

| Map | Tower | Position (x, y) m | Region it stands in | From region centre | From zone area centre |
|---|---:|---|---|---:|---:|
| Bakurani | 1 | (-8297, -11041) | TOWER 1 | 2 m | 160 m |
| Bakurani | 2 | (-8627, -11050) | TOWER 2 | 19 m | 360 m |
| Bakurani | 3 | (-8628, -11398) | TOWER 3 | 18 m | 382 m |
| Bakurani | 4 | (-7990, -11333) | TOWER 4 | 17 m | 337 m |
| Bakurani | 5 | (-8127, -10892) | LUMBERYARD NORTH (78 m from TOWER 5 L) | 39 m | 354 m |
| Ozeti | 1 | (-6614, -6102) | Tower 1 | 15 m | 238 m |
| Ozeti | 2 | (-6163, -5742) | Tower 2 | 6 m | 426 m |
| Ozeti | 3 | (-5749, -6183) | Tower 3 | 2 m | 632 m |
| Ozeti | 4 | (-6131, -6577) | Tower 4 | 11 m | 526 m |
| Zestafona | 1 | (-1332, -2223) | Tower 1 | 13 m | 260 m |
| Zestafona | 2 | (-903, -2315) | Tower 2 | 17 m | 288 m |
| Zestafona | 3 | (-1175, -1825) | Tower 3 | 12 m | 289 m |

Saburtulo (Russia world): towers at (x, y, z) m (-108, -145, 176), (187, 65, 166), (-362, 316, 155), (-560, -307, 211) and (8, -333, 164) for towers 1 to 5. There is no region list, so only the distance from the placed zone object at (-181, -59) m is given: 113, 389, 416, 452 and 333 m. Status ABSENT for named regions (round 65, 2a).

Notes: Bakurani's region list holds TOWER 1 to 4 (weight 0), TOWER 5 L (weight 1) and TOWER 7 (weight 0, no tower placed there). Ozeti's Tower 1, 3 and 4 regions have weight 1, Tower 2 weight 0. Zestafona's three have weight 0. Each tower's z lies inside the ground range of the landscape piece under it on Bakurani, Ozeti and Saburtulo, and 4 to 16 m above the piece's top on Zestafona.

## 3. Map extents. FOUND (component resolution)

Source: `LandscapeComponent` exports in the cells (256 packages per world found by `findname LandscapeComponent`): `SectionBaseX/Y`, `ComponentSizeQuads`, `CachedLocalBox`, and the owning `LandscapeStreamingProxy` root (`RelativeLocation`, `RelativeScale3D` 200 x 200 x 900, Zestafona z 585, Saburtulo z 683.6; proxy `SectionBase`). World x/y of a piece = proxy location minus proxy section base times scale, plus the piece's section base times scale; world z = proxy location z + scale z x local z. Check: every placed tower lies inside or just above the height range of the piece under it.

| Map | Landscape | Pieces | Play box (basis) | Play box (km) | Ground z in play box (m) | Whole landscape z (m) |
|---|---|---|---|---|---|---|
| Bakurani | 16.32 x 16.32 km | 256 of 1020 m | regions plus 500 m | 3.33 x 3.45 | -991 to -278 | -1008 to 178 |
| Ozeti | 16.32 x 16.32 km | 1024 of 510 m | regions plus 500 m | 3.80 x 2.95 | -988 to -759 | -1037 to -275 |
| Zestafona | 16.32 x 16.32 km | 1024 of 510 m | regions plus 500 m | 3.46 x 3.25 | 44 to 251 | 25 to 707 |
| Saburtulo | 16.32 x 16.32 km | 1024 of 510 m | towers and zone object plus 500 m (stand-in, no region list) | 1.75 x 1.65 | 132 to 318 | 83 to 766 |

Limits: the height range is the min and max over the pieces that overlap the box, so it is an outer bound (pieces are 1020 m wide on Bakurani and 510 m elsewhere; exact heights would need the heightmap textures). The height scale is the game's own (Bakurani and Ozeti sit near z = -900 m). The Saburtulo box is not the region box and is inferred.

## 4. Server-browser-only entries. FOUND (structure), inferred (use)

Experience files (`Config/Experiences/...`) list only `EnabledDataLayers`: Mindori `DL_Mindori` + `DL_KhevuliSpawn`, `DL_LiknisiSpawn`, `DL_BaghiSpawn`; Tevza `DL_Tevza` + `DL_VostimiSpawn`, `DL_EdemiSpawn`, `DL_ShovliSpawn`; Berlin `DL_Berlin` + `DL_StuttgartSpawn`, `DL_HanoverSpawn`, `DL_BremenSpawn`; Paris `DL_Paris` + `DL_RennesSpawn`, `DL_CalaisSpawn`, `DL_GranadaSpawn`. None names a zone config. Each world holds one `B_ControlZone_C` (round 65, 2a): Kavkazi uses [`DA_ControlZoneConfig_Bakurani`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZoneConfig_Bakurani.json) and the Kavkazi region list, Europe uses [`DA_ControlZone_Config_Europe`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Config/DA_ControlZone_Config_Europe.json) and the Europe region list. The data layers `DL_Bakurani`, `DL_Mindori`, `DL_Tevza`, `DL_Berlin`, `DL_Paris` have no cells in the world's runtime hash (cells carry only spawn layers, destruction and blockout layers), and the zone object is in a game feature external data layer, so no layer ties the zone object to one entry. The entries therefore use the world's zone object (inferred).

Cell to layer map: `WorldPartitionRuntimeLevelStreamingCell.DataLayers` -> `DataLayerInstanceWithAsset` in each world's `.umap` (`dlmap.py`). Spawn manager positions come from round 66's `act2_*.jsonl`.

| Entry | World | Zone area | Distance from main zone area | Placed spawn points, distance from zone area centre |
|---|---|---|---|---|
| Mindori | Kavkazi | Bakurani's | 0 | Khevuli 3807 m, Liknisi 2798 m, Baghi 3939 m |
| Tevza | Kavkazi | Bakurani's | 0 | none placed (Vostimi, Edemi, Shovli have no spawn manager with that layer) |
| Berlin | Europe | Ozeti's | 0 | Stuttgart 1573 m, Hanover 2358 m, Bremen 4378 m |
| Paris | Europe | Ozeti's | 0 | Rennes 4027 m, Calais 5278 m, Granada 3522 m |

For comparison: Bakurani entry one 3807 to 4131 m, entry two 3823 to 3895 m, Ozeti (Madrid) 3522 to 4006 m. Khevuli and Baghi are shared by Mindori and the first Bakurani entry; Granada by Paris and Ozeti. The Bakurani region list holds MindoriVillage (-7404, -11057), MindoriHillside1 (-7461, -10858) and MindorHillside2 (-7527, -10669), 0.9 km from the zone area centre (-8301, -11201); no region carries the name Tevza, Berlin or Paris. Three Kavkazi spawn managers carry no layer (positions (-7754, -7450), (-12410, -9736), (-8890, -11355)); whether any belongs to Tevza is not known.

## Wiki updates (done in this commit)

- `_wiki/game-modes-and-maps/hot-zone-magnet-towers.md`: new article (capture, code, keypad, magnet, cooldowns).
- `_wiki/progression-and-economy/hot-zone-magnet-challenges.md`: link to the new article, who is paid and the 80 m range.
- `_wiki/game-modes-and-maps/king-of-the-hill.md`, `_wiki/building/drill-rig.md`: links.
- `_wiki/game-modes-and-maps/bakurani.md`, `ozeti.md`, `zestafona.md`, `saburtulo.md`: infobox rows (play area, ground height), "Size and ground height" section, "Where the towers stand" table, tower row text.
- `_wiki/game-modes-and-maps/zone-layouts.md`: Mindori, Tevza, Berlin and Paris section and overview row.
- `content/Wardogs_Maps_v2.md`: section 12.
- `assets/data/map-magnets-extents.json`: new summary data.
