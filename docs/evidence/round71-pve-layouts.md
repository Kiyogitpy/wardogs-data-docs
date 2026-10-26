# Round 71: PvE scenario layouts (R71-RE)

Static analysis only. Nothing was run. Evidence level: cooked data read (extractor `dump` of the 110 World Partition cell packages of the PvE external data layers in the Kavkazi world, every placed actor with its root component position; actors attached to another actor take the parent transform). No decompilation, nothing behind the protection layer was touched (PROTECTED items are listed where they apply). Method follows rounds 65 and 66 ([round66-map-actors.md](round66-map-actors.md)). Raw output and scripts are under `E:/Reverse_Engineer/wardogs_analysis/round71_re/` (outside the repository): `pve_cells.txt` (cell list), `dump/` (extractor output), `build.py` (actor extraction), `analyse.py` (distances, regions, clusters), `build_json.py` (writes the summary). The committed summary is [`assets/data/pve-layouts.json`](../../assets/data/pve-layouts.json); the data page section is [`content/Wardogs_Maps_v2.md`](../../content/Wardogs_Maps_v2.md) section 15.

Coordinates are metres in the world frame (cm / 100), the frame of `map-magnets-extents.json`. Distances are straight lines on the ground plane, not route lengths. Reference frame for the Bakurani map: zone area centre (-8301, -11201); play box x -9967..-6634, y -12925..-9477 (zone regions plus 500 m, round 67); named regions are the polygons of `DA_ControlZoneRegionsConfig_Kavkazi` (Riverside Forest, Lumber Farmlands, Green Farmland and others).

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Objective sites | FOUND | VIP Escort: one extraction trigger box (80 m marker radius) plus one helicopter entry path, one exit path, one helicopter spawn point and one scenario-end point at the same spot. Strike and Disarm: one laptop (hack 300 s placed), one objective point, one compound marker (200 m radius), one end marker (80 m radius) with the helicopter entry and exit paths. Hunter Killer: none (text labels only). |
| 1b | VIP start | ABSENT (placed) / FOUND (logic) | No VIP start point is placed. The VIP is one random player (quest logic, round 36), so the start is the player spawn area. |
| 1c | Player spawns | FOUND | One spawn manager per layer (VIP Escort, Strike and Disarm, example), each with one equipment vendor; Strike and Disarm adds one vehicle vendor and one spawn volume (faction Charlie, 15 spawn points). No `PlayerStart` actor in these layers. Hunter Killer none. |
| 1d | AI spawners | FOUND (count, config); NATIVE (output per spawner) | VIP Escort 95, Strike and Disarm 53 (26 of them held back for the counter-attack wave), others 0. One spawner has one `SpawnConfig` and no count field; one spawner is one soldier (inferred: the native `TriggerAISpawn` body was not read). |
| 1e | Loot markers | FOUND (shared tags); ABSENT (VIP Escort rows) | VIP Escort has 21 markers, all with shared tags (Bandage 12, Weapon 3, Defib.Cheap 3, Sniper 1, Armor 1, Helmet 1). None carries `Lootable.VIPEscort01.*`, so the SV98 and Fuel Canister rows have no marker in the PvE layers. The other layers have no marker. |
| 1f | Vehicles | FOUND | VIP Escort 6 vehicle spawners (Kodiak pickup 2, Kodiak 1, Bobcat 3); Strike and Disarm 5 (all Kodiak pickup: 1 at the player spawn, 4 tagged Alpha at the compound). No vehicle vendor in VIP Escort. |
| 1g | Triggers, volumes | FOUND | VIP Escort: 1 trigger box (extraction), 1 navmesh bounds volume, 4 navigation invoker actors. Strike and Disarm: tether volume 1, target-area volume 1, spawn volume 1, navmesh bounds 1, wave trigger (`B_MultiAISpawner`) 1, 1 ladder blockout mover. No tether volumes in VIP Escort. |
| 2 | Route distances | FOUND | Below. |
| 3 | Hunter Killer placed layer | FOUND (labels only) / ABSENT (gameplay actors) | 28 cells, 16 hidden text labels and 9 auto-instanced mesh actors. No spawn area, no AI spawner, no vendor, no vehicle spawner, no quest actor, no volume. |

## Layout per scenario

### VIP Escort (`VIPEscort_01`, 65 cells)

Placed (gameplay): AI spawners 95, patrol routes 16, vehicle spawners 6, loot markers 21, equipment vendor 1, spawn manager 1, trigger box 1, quest points 2 (helicopter spawn point and scenario end), helicopter paths 2 (entry 4 path points, exit 3), navmesh bounds 1, navigation invokers 4, pre-placed buildables 69 (62 H-barriers, 5 tank traps, 1 bunker, 1 forward operating base), 18 hidden developer text labels (Hay Bales 6, Road Block 1, Patrol 1, 10 blank).

| Point | Position (m) | Where |
|---|---|---|
| Player spawn area (spawn manager and equipment vendor, faction Bravo) | -7754, -7450 | 2,027 m north of the play box; 3,791 m from the zone area centre; in no named region (Lumber Farmlands edge 2,534 m) |
| Extraction trigger | -9417, -10365 | inside the play box; 1,394 m from the zone area centre; in no named region (Riverside Forest edge 235 m) |
| Helicopter spawn point (entry path start) | -9417, -10314 | 51 m from the trigger |
| Scenario end point | -9397, -10360 | 21 m from the trigger |

Distances: player spawn to extraction trigger 3,356 m (to the helicopter spawn point 3,312 m). VIP start to destination: same, 3,356 m, because the VIP is a random player starting at the spawn area. There is no separate objective between spawn and extraction (no hack site, bomb or disarm point): the route is the escort itself.

AI: 86 riflemen, 5 marksmen, 4 machine gunners; all start automatically; 31 riflemen follow patrol routes (16 route actors). By distance from the player spawn: 26 within 1,000 m, 34 at 1,000 to 2,000 m, 24 at 2,000 to 3,000 m, 11 beyond 3,000 m (nearest 370 m, farthest 3,283 m). Near the extraction point: 9 within 500 m, 18 within 1,000 m (nearest 203 m). 31 stand inside the play box, 6 inside a named region polygon (Riverside Forest 4, Lumber Farmlands 2), 89 in none. They form 17 groups of 250 m (largest: 15 at 643 m from the spawn, 14 at 1,653 m, 11 at 2,150 m, 10 at 1,543 m). No tether volume, so the soldiers are not tied to an area (placed data).

Loot markers (shared tags only, see 1e): Spawn area 1 (a Bandage, 50 m from the spawn), First House 4 (3 Bandage, 1 Armor; 384 to 393 m), Big Road Block 6 (2 Weapon, 2 Bandage, 1 Defib.Cheap, 1 Helmet; 623 to 664 m), Compound 8 (4 Bandage, 2 Defib.Cheap, 1 Sniper, 1 Weapon; around 1,800 m), Logging Camp 2 (2 Bandage; around 2,190 m). The group names are the actor names in the data. The road block group sits with the bunker, the forward base and the 5 tank traps (centre -8120, -7960, about 650 m from the spawn). The 62 H-barriers are spread over x -9412..-8096, y -10149..-7940 (centre -8664, -9394).

Vehicle spawners (distance from the player spawn): Bobcat 350 m, Bobcat 628 m, Kodiak 646 m, Bobcat 1,467 m, Kodiak pickup 1,827 m, Kodiak pickup 2,196 m. No faction tag is placed on them.

### Strike and Disarm (`StrikeDisarm_01`, 16 cells)

Placed (gameplay): AI spawners 53, wave trigger 1, patrol routes 4, vehicle spawners 5, laptop objective 1, quest points 2, compound and end marker actors 2, helicopter paths 2, tether volume 1, target-area volume 1, spawn volume 1, navmesh bounds 1, ladder blockout 1, equipment vendor 1, vehicle vendor 1, spawn manager 1, navigation invoker 1. No loot marker.

| Point | Position (m) | Where |
|---|---|---|
| Player spawn area (spawn manager, vendors, spawn volume) | -12410, -9736 | 2,443 m west of the play box; 4,363 m from the zone area centre; no named region within 3,211 m (Green Farmland) |
| Laptop | -10031, -10427 | 64 m west of the play box edge; 1,895 m from the zone area centre; 799 m from Green Farmland |
| Compound marker (200 m radius) | -10025, -10424 | around the laptop |
| Helicopter entry start | -9920, -10238 | inside the play box; 738 m from Riverside Forest |
| End marker and helicopter exit | -9920, -10288 | inside the play box |

Distances: player spawn to laptop 2,478 m; laptop to end marker 177 m (to the helicopter entry start 219 m); player spawn to end marker 2,551 m.

AI: 49 riflemen and 4 snipers. Start group 27 (23 riflemen, 4 snipers), wave 26 riflemen (held back, `DisableAutomaticSpawn`, started by the wave trigger 385 m from the laptop at -9847, -10765). Start group distance to the laptop: median 105 m, 13 within 100 m, farthest 406 m. Wave distance to the laptop: 232 to 541 m (median 491 m). Groups: 28 around the laptop (centre 37 m away), 16 about 420 m south-southeast, 8 about 495 m south-southwest, 1 at 406 m north. Nearest soldier to the player spawn 2,282 m; farthest 2,934 m. 48 are tied to the compound tether volume; 6 soldiers use the 4 patrol routes. 20 stand inside the play box, none inside a named region.

Vehicles: 1 Kodiak pickup at the player spawn (47 m), 4 Kodiak pickups tagged Alpha (the Lonestar side) 99 to 143 m from the laptop. The ladder blockout mover is 485 m west of the laptop.

### Hunter Killer (`HunterKiller_01`, 28 cells)

16 hidden text labels and 9 auto-instanced mesh actors; nothing else. Labels: Deploy Location 1 (-10709, -11254), HVT Location 1 (-10103, -10397), Lieutenant Location 2 (-10566, -10492 and -9761, -10783), Guards 4, Patrol 7, Exfil Location 1 (-9999, -10236). Deploy to HVT 1,050 m, HVT to exfil 192 m, deploy to exfil 1,242 m. The layout sits in the same compound as Strike and Disarm: the HVT label is 78 m from that laptop, the exfil label 79 m from that helicopter point, a Guards label 49 m from the laptop, a Lieutenant label 88 m from that wave trigger (inferred reuse of the blockout; not stated in the data). Status: placed layer FOUND (labels), gameplay actors ABSENT, AI ABSENT, player spawn ABSENT.

### Example scenario (`ScenarioExample`, 1 cell)

Spawn manager 1, equipment vendor 1, quest overlap area 1, quest progress test actor 1, quest position point 1, all within 17 m of each other at (-8890, -11355): 609 m from the zone area centre, inside the play box, 26 m from the West Hill Woods region edge. A test stub, no AI, no loot, no vehicle.

## Corrections to older claims

- VIP Escort "marker positions are not in the map files" (wiki, round 59): the 21 markers are in the files, but with shared tags; none is tagged for the two VIP Escort rows. Where the SV98 and Fuel Canister rows are placed is still not in these layers (ABSENT; likely a shared or other layer, not searched in the 40,000 base cells this round).
- "Hunter Killer has a map" (infobox): a layer exists but holds only labels.
- Round 66 listed Strike and Disarm as "54 AI spawners": 53 are soldiers, the 54th actor is the wave trigger.
- VIP Escort "appears at one of three entry points": the layer holds one entry path and one exit path (the same two shapes are in Strike and Disarm). The "three" is not visible in the layout (SERVER or quest data, not re-read this round).
- Round 36 said the Hunter Killer cells hold no spawners: confirmed, and now with positions.

## Not found

- Player start actors, bomb or disarm site other than the laptop, a VIP start point, tower or control zone in the PvE layers: ABSENT (searched all actor classes in the 110 cells).
- The native `TriggerAISpawn` body and any per-spawner soldier count above one: NATIVE (not read; the class has no count field).
- Route length over roads: not in the data (straight lines only).

## Wiki updates (done in this commit)

- `_wiki/game-modes-and-maps/vip-escort.md`, `strike-and-disarm.md`, `hunter-killer.md`, `pve-scenarios.md`, `ai-enemies.md`: new "Layout" section; VIP Escort loot-position sentence and the entry-point sentence corrected; Hunter Killer map claim qualified.
- `content/Wardogs_Maps_v2.md`: section 15; section 11 PvE bucket line corrected.
- `assets/data/pve-layouts.json`: summary data.
