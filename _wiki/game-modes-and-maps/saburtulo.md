---
title: "Saburtulo"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Saburtulo King of the Hill map, added with its Season 2 zone and warm-up data: a 550 m zone with four placements."
---

# Saburtulo

| Saburtulo | |
|---|---|
| **General** | |
| Map area | About 16.3 km square (minimap bounds) |
| Play area | About 1.75 km by 1.65 km around the towers and the zone (stand-in, inferred) |
| Ground height in the play area | 132 m to 318 m on the game's height scale |
| Built-up area | About 5.0 km by 4.6 km (where buildings are placed) |
| Modes | King of the Hill |
| Vehicle spawns | 3 deployment boards and 11 vehicle yards (6 ground, 2 air, 3 light) and one extra air yard |
| **Zones** | |
| Control Zone | 550 m across, 150 m tall |
| Hot Zone | 85 m across, 150 m tall |
| Zone placements | 4 |
| Zone regions | None (the map's zone object has no region list) |
| Internal name | Server browser Moscow_KOTH_01; zone config Russia; minimap folder Russia |
{: .wiki-infobox }

Saburtulo is a King of the Hill map with a 550 m Control Zone and four possible zone placements. Its zone configuration, shader warm-up list and sight-blocker data were all added in Season 2. The data does not include a list of named zone regions for it, and it does not describe its streets or buildings. Its vehicle and infantry spawn areas are covered under Vehicle spawns.

## Overview

Saburtulo is played in [King of the Hill](king-of-the-hill.md) under one server browser entry. The data ties it to the Moscow entry by name and folder only (an inference from the names, not checked in game). Its zone configuration is stored under the Russia files. Some data entries spell the placement names with "Sabartulo", which refers to the same placement set.

## Modes played here

- [King of the Hill](king-of-the-hill.md).

## Zones and objectives

The Control Zone is 550 m across and 150 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The zone has four placements. Hospital has weight 1, so it is the only placement drawn at random. Bazaar, River and Hillside have weight 0, so they are used only when the server rotation names them.

| Placement | Weight |
|---|---|
| Hospital | 1 |
| Bazaar | 0 |
| River | 0 |
| Hillside | 0 |

- **Zone regions.** The data does not include a region list for this map. The zone object placed in the Saburtulo map files has an empty region slot, the Sniper Showdown zone placed there has none either, and the minimap data holds none, so where the zone can sit beyond these four placements is not known. Bakurani, Ozeti and Zestafona each have a list; this is the one King of the Hill map with a zone but no list.

## Vehicle spawns

The Moscow entry uses three spawn areas: Kuzminki (Lonestar side), Rostokino (Valkyra side) and Ramenki (Manticore side). In total the match has 11 vehicle yards in the spawn areas (6 ground, 2 air, 3 light), 3 deployment boards and 68 vehicle slots, plus one more air yard in the Rostokino area that is tagged for the Lonestar side.

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots |
|---|---|---|---:|---:|---:|---:|---:|
| Lonestar | Kuzminki | Manticore version | 2 | 0 | 1 | 17 | 81 |
| Valkyra | Rostokino | Valkyra version | 2 | 1 | 1 | 25 | 69 |
| Manticore | Ramenki | Lonestar version | 2 | 1 | 1 | 26 | 76 |

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). Two details look swapped in the data: the Kuzminki area (Lonestar side) holds a Manticore deployment board and the Ramenki area (Manticore side) holds a Lonestar board. Which team receives which spawn vehicle at run time is not known. The Rostokino area has no infantry spawn area in the dumped files.

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The data does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto a spawn vehicle, the deployment board's cooldown is 600 s (this value is stored; its start trigger was not traced). The deployment board's built-in respawn timers are 300 s, or 60 s for a losing side. They most likely time the side's spawn vehicle (inferred from their names). The data gives no return time for the other yard vehicles.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game files.

## Cover materials

Most cover on Saburtulo is made of the materials below. The counts are placed wall and building pieces taken from the map files, covering the whole map, because the data has no zone region list for it to narrow the count to the play area. A piece is one placed part such as a wall panel, floor, roof section, trim strip or fence section, so one building is many pieces. Each piece is counted under every material it uses, so a piece with brick walls and wood trim appears in both rows and the rows add up to more than the total. Pieces seen only as decals are left out. This was read from the game files, not checked in play, and broken-apart building pieces that appear when a building is destroyed are not included.

| Material | Pieces | Share of pieces | Mostly (from the material names) |
|---|---:|---:|---|
| Concrete | 60,809 | 32% | apartment walls, apartment floors, concrete trim |
| Wood | 49,790 | 26% | wood trim, wooden roofs |
| Brick | 49,470 | 26% | brick and mortar, house walls |
| Metal | 31,000 | 16% | girders, corrugated sheet, metal panels |
| Plaster | 11,151 | 6% | plaster walls, wall mouldings, skirting boards |
| Rubber | 10,035 | 5% | rubber trim, roofing, flooring |
| Ceramic | 5,715 | 3% | window frames, tiled facades, flooring |
| Glass | 3,061 | 2% | window glass |

Total: 189,545 pieces (184,855 building pieces and 4,690 wall, fence and barrier pieces) from 1,017 different shapes. How hard each material is to shoot through is on [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md), which lists a density for each one.

## Size and ground height

The ground of this map is one square of 16.32 km by 16.32 km. Across the whole square the ground runs from 83 m to 766 m on the game's height scale. Saburtulo has no list of zone regions, so the usual box (the regions plus 500 m) cannot be drawn. The play area above is a stand-in: the box around the five towers and the zone object, plus 500 m on each side. It is inferred and is not an edge the game enforces. Inside it the ground runs from 132 m to 318 m.

The heights are read from the game's ground pieces, which are 510 m wide, so the real spread inside the box can be a little smaller. The height scale is the game's own and starts below zero on some maps, so only the difference between two heights means something. The box is 1.75 km by 1.65 km and the ground piece count that touches it is 20. Nothing here was measured in play.

## Placed objects

These are the things the map file places for players to use or break. Saburtulo has no zone region list, so there is no "around the zones" area and only the whole file is counted. "Whole map file" counts everything in the file, and the Sniper Showdown layout for Russia uses the same file, so it is larger than this map alone. The counts were read from the game files, not checked in play.

| Object | Around the zones | Whole map file | What it is |
|---|---:|---:|---|
| Hot Zone Magnet towers | Not given | 5 | Numbered 1 to 5. These are the capture towers of the [tower system](hot-zone-magnet-towers.md) and the source of the [tower and magnet rewards](../progression-and-economy/hot-zone-magnet-challenges.md). Positions are under Where the towers stand. |
| Doors you can open | Not given | 536 | Houses, apartments, garages, offices, shops and a hospital. A garage door counts once. Doors can also be broken, see [Destruction](../game-mechanics/destruction.md). |
| Ladders | Not given | 40 | Climbable with the ladder controls on [Movement](../game-mechanics/movement.md). |
| Breakable windows | Not given | 2,687 | Single panes that smash when hit. |
| Destructible buildings | Not given | 378 | Single buildings that can be knocked down: houses, garages, warehouses and shops, plus a few larger ones. Doors and windows are counted on their own rows. |
| Pre-placed barbed wire | Not given | 52 | Slows and hurts players and damages vehicles, like the [Barbed Wire](../building/barbed-wire.md) you can build. |
| Water | Not given | None | No water actor was found in the file. |
| Supply buildings | Not given | 10 | A kind of building. Its data shows no supply or pickup function. |

### Where the towers stand

Saburtulo has no list of zone regions, so the towers cannot be placed in a named region. The table gives each tower's distance from the zone object the map places (the usual Hot Zone start). All five stand within about 0.5 km of it. How a tower is captured is on [Hot Zone Magnet Towers](hot-zone-magnet-towers.md).

| Tower | Distance from the zone object |
|---|---:|
| 1 | 113 m |
| 2 | 389 m |
| 3 | 416 m |
| 4 | 452 m |
| 5 | 333 m |

### In each team spawn area

The file places 3 team spawn areas for this map (the ones with a wager vendor; the other spawn areas in the file belong to other maps, inferred from that). Every area has a deployment board, an equipment vendor, a vehicle vendor, a garage vendor and a [wager vendor](../progression-and-economy/wagers.md), and also a small soccer pitch, 3 moving practice targets and a safe zone. The invisible safe zone boxes are about 480 m tall; each safe zone is 800 m by 800 m. They protect their own team from damage, and the play-area edge, the out-of-bounds countdown and the other safe zone rules are on [Boundaries and Safe Zones](boundaries-and-safe-zones.md). The map's play rectangle is 13.2 km by 13.2 km.

Saburtulo is the one map here whose spawn areas have no free fuel point.

Vehicle yards and spawn spots are on the Vehicle spawns section above.

### Not in the map files

The map file holds no capture points other than the Hot Zone Magnet towers, no pre-placed guns or emplacements, no ammo or supply pickups, no loot or crates and no zip lines. The free fuel point above is the only resupply object the file places.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#saburtulo).

## Season 2 changes

- The Russia zone configuration was added in Season 2. It is 550 m across with an 85 m Hot Zone, and it uses the standard 25-second move delay.
- A shader warm-up list for this map was added in Season 2. It lists 1,132 graphics pipeline states and 74 compute pipeline states. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The data does not say what sight blockers do in play.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Maps](maps.md)

## Sources

- [Boundaries and Safe Zones](boundaries-and-safe-zones.md)
- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): boards, yards and infantry spawn areas per map
- [Vehicle spawn data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-spawns.json)
- [Maps and gym data](../../content/Wardogs_Maps_v2.md): also the cover material counts per map
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Round 40 modes, AI and other evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md): Moscow name link (inference from names and folders)
- [Placed objects per map (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-gameplay-actors.json)
- [Tower positions and map extents (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-magnets-extents.json)
