# Round 66: placed gameplay actors per map (R66-MAPS)

Static analysis only. Nothing was run. Evidence level: cooked data read (extractor `dump` of the World Partition cell packages, Blueprint defaults read from `dump` of the actor Blueprints), no decompilation. Method follows round 65 ([round65-open-questions.md](round65-open-questions.md), section 1). Scripts and raw output are under `E:/Reverse_Engineer/wardogs_analysis/round66_maps/` (outside the repository): `scan_actors.py` and `scan_act2.py` (actor scanners; `act2_*.jsonl` is the final output), `scan_dbe.py` (destruction component owners, `dbe_*.jsonl`, plus a sample of actor properties in `props_*.jsonl`), `summarize.py`, `build_json.py`, `apply_wiki.py`, `apply_maps_v2.py`, `magnets.py` (magnet numbering and positions, `magnets.json`). The round 65 cell lists (`cells_<World>.txt`, 40,616 packages, which already include the GameFeatures external data layer cells of each world) were reused unchanged.

## Method

1. Each cell is dumped (`WdExtract dump`, 300 cells per batch) and every export whose outer is the persistent level (an actor) is recorded, except a noise set (static mesh actors, terrain tiles, PCG partition actors, HLOD actors, decal actors, road sub-actors, micro-biome PCG actors). A record holds the cell id, the export type, the generated-class path and the world `RelativeLocation` of the actor's root component (the root component export is matched by name and owner actor).
2. Child actors have no root of their own in the level (single doors `B_Door_C`, smashable windows): they carry a `ParentComponent` that names the parent building actor, and the parent's location is used (up to four hops). After this pass every recorded actor of interest has a position.
3. Destructible buildings are the owners of `BHDestructionBuildingEditorComponent` (same pass structure, `scan_dbe.py`). The component is on every destructible actor, doors and windows included, so doors are excluded from the building count (class name contains `Door`) and counted as doors.
4. Each cell is mapped to a bucket from its package path: `world` (`Content/Maps/Worlds`), `zone_plugin` (ControlZone, HotZoneMagnet, FlyByManager game feature cells), `sniper_showdown` (Experiences/SniperShowdown), `pve_range` (PvE scenarios, shooting range, tutorial). `world` and `zone_plugin` make the map totals; the others are listed apart.
5. Scope: `play` is the bounding box of the region polygons of `DA_ControlZoneRegionsConfig_*` plus 500 m (round 65). Saburtulo has no region list, so only `world`. `jutari_zone_area` is a 850 m box around the Sniper Showdown zone object in the Kavkazi world (centre x -672,688, y -1,117,098 cm, extents 35,000 cm plus 50,000 cm margin).
6. The spawn-area profile counts, around each `B_SpawnManager_C` within 150 m, the board, vendors, safe zone, soccer pitch, moving targets and fuel point.
7. Blueprint defaults of `B_BarbedWire_Damage_Volume`, `B_WDSoccerField`, `B_SafeZone`, `B_SpawnFuelItemRefill` and its `B_Item_RefuelComponent_C` were read from their packages to say what each actor is.

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | Capture towers | FOUND (one kind) | The only tower is the Hot Zone Magnet: 5 (Bakurani), 4 (Ozeti), 3 (Zestafona), 5 (Saburtulo), each with a `HotZoneTowerNumber` 1..N. The tower reward table ([`DT_Reward_Cash_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet/DT_Reward_Cash_HotZoneMagnet.json): hostile tower 1,000, neutral tower 250) belongs to the same game feature, which makes these the capturable towers (inferred from the shared plugin and name; the capture logic was not read). |
| 2 | Pre-placed emplacements or static weapons | ABSENT | No turret, emplacement, mortar, SAM, weapon-station or buildable-item actor class in the 40,616 cells of the four worlds. The PvE cells hold 69 pre-placed buildables (`B_BuildablePrefab_HBlock_C` 62, `B_PlacementBuildable_TankTrap_C` 5, a bunker and a forward operating base), PvE-only and Bakurani world only. |
| 3 | Supply, ammo or refuel points | FOUND (fuel); ABSENT (ammo, supply) | Free fuel point (`B_SpawnFuelItemRefill_C`): Bakurani world 6, Ozeti world 3, Zestafona world 3, Saburtulo none. Its source container has `bHasInfiniteFuel` true, `bFreeInSpawn` true, `MaxFuel` 40, `RefuelPerUpdate` 2, `PricePerLiter` 2. No ammo, supply-crate, pickup, loot or container actor class. The `B_SupplyBuilding_*` classes are destructible building models (live chunk data); no interaction component. |
| 4 | Ladders, ziplines, doors | FOUND (ladders, doors); ABSENT (ziplines) | Ladders, doors and garage doors below; no zip line, rope or cable-ride actor (the cable spline tool is scenery). |
| 5 | Destructible buildings | FOUND | 264 / 247 / 161 / - in the play scope, 446 / 354 / 224 / 378 in the whole world. Plus 10,523 breakable window actors in the four worlds and 249 to 373 demolition cell markers per world (markers, no mesh). |
| 6 | Water volumes | FOUND | Bakurani: 3 lakes and 23 river sections (world); Ozeti: 17 river sections and a swimming pool building; Zestafona: 14 river sections; Saburtulo: none. |
| 7 | Other gameplay-named classes | FOUND | Spawn safe zones, vendors (equipment, vehicle, garage, wager), deployment boards, soccer pitches, moving practice targets, pre-placed barbed wire, a conversation point (Ozeti), a mini digger prop (Zestafona), PvE scenario content (Bakurani world only). Details below. |

## Counts

`play / world`. Doors: the sum of all door rows, a garage door counted once (two leaves). Full per-class rows are in [Wardogs_Maps_v2.md](../../content/Wardogs_Maps_v2.md) section 11 and [map-gameplay-actors.json](../../assets/data/map-gameplay-actors.json).

| Object | Bakurani | Ozeti | Zestafona | Saburtulo (world only) |
|---|---:|---:|---:|---:|
| Hot Zone Magnet towers | 5 / 5 | 4 / 4 | 3 / 3 | 5 |
| Doors | 283 / 585 | 188 / 349 | 259 / 425 | 536 |
| Ladders | 54 / 100 | 22 / 34 | 88 / 98 | 40 |
| Breakable windows | 1,916 / 3,779 | 1,425 / 2,358 | 1,219 / 1,699 | 2,687 |
| Destructible buildings | 264 / 446 | 247 / 354 | 161 / 224 | 378 |
| Pre-placed barbed wire | 33 / 161 | 32 / 32 | 41 / 73 | 52 |
| Lakes | 3 / 3 | 0 | 0 | 0 |
| River sections | 6 / 23 | 4 / 17 | 3 / 14 | 0 |
| Swimming pool building | 0 | 1 / 1 | 0 | 0 |
| Supply buildings | 0 | 1 / 1 | 1 / 3 | 10 |
| Main-map spawn areas (inferred) | 6 | 3 | 3 | 3 |
| Free fuel points (main areas) | 6 | 3 | 3 | 0 |

Jutari: in the 850 m box around its zone spot, the Kavkazi world holds 31 doors (a garage door counted once), 9 ladders, 270 breakable windows, 37 destructible buildings and 16 pre-placed barbed wire volumes, and no magnets, vendors or boards.

Spawn-area facilities are all outside the play box (the one exception is a non-main Ozeti area, not counted for the map). Each main-map spawn area holds one deployment board, one equipment vendor, one vehicle vendor, one garage vendor and one wager vendor, plus (with the exceptions in the JSON: one Bakurani area without a safe zone, one Ozeti area without a safe zone or soccer pitch) a safe zone, a soccer pitch, three moving targets and a fuel point. The attribution of areas to maps is inferred: the area has a wager vendor, and the number of such areas equals the number of deployment boards the map articles give (6, 3, 3, 3: two entries of three for Bakurani).

## Caveats

- **Position of child actors.** Single doors, interactable doors and windows are children of buildings and take the building's position, not their own. A door on the edge of the box is counted by its building.
- **Shared worlds.** The `world` column includes other maps that use the same file (Mindori, Tevza and Jutari in the Kavkazi world, Berlin and Paris in the Europe world). The `play` box removes most of them except where they overlap.
- **Rectangle scope.** The `play` box is the bounding rectangle of the region polygons plus 500 m, not the actual zone shape.
- **Water.** Only lake and river actors are counted. Water authored in the landscape or a material would not appear; Saburtulo has no lake or river actor, which does not prove it has no water.
- **Magnet equals tower (inferred).** The data pairs [`DT_Reward_Cash_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet/DT_Reward_Cash_HotZoneMagnet.json) (tower and magnet rows) with the HotZoneMagnet game feature; the placed actor class has a tower number. The capture handling itself was not read in this round.
- **Supply building.** Named by its Blueprint; the cooked data has destruction chunk data and no interaction component, so a supply function is not found. It is reported as a kind of building.
- **Absent means not found in the cells.** Items created at run time (supply drops, player-built emplacements, AI-held positions) would not be in the cells. Searching: every actor class name in the four worlds' cells (`act2_*.jsonl`, 46,304 actor records) against interaction, pickup, loot, crate, station, turret, emplacement, mortar, weapon, ammo, supply, capture, flag, tower, zip, rope, container and objective words.
- **PvE and range content.** The Bakurani world cells carry PvE scenarios (VIPEscort_01, StrikeDisarm_01, ScenarioExample, HunterKiller_01) and the shooting range and tutorial. These are not King of the Hill content and are not in the totals.
- **Not run.** Nothing was observed in play.

## Wiki updates (done in this commit)

- `_wiki/game-modes-and-maps/bakurani.md`, `ozeti.md`, `zestafona.md`, `saburtulo.md`: new "Placed objects" section (table, spawn-area facilities, what is not placed), and a Sources line.
- `_wiki/game-modes-and-maps/bakurani-outskirts-jutari.md`: new "Placed objects" section (the area around the Jutari zone).
- `content/Wardogs_Maps_v2.md`: section 11 added after section 10, section 9's first limitation updated.
- `assets/data/map-gameplay-actors.json`: the summary data.
