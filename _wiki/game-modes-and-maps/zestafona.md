---
title: "Zestafona"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Zestafona King of the Hill map: a 500 m zone whose Hot Zone is 850 m tall, four placements, and 56 named zone regions."
---

# Zestafona

| Zestafona | |
|---|---|
| **General** | |
| Map area | About 16.4 km square (minimap bounds) |
| Play area | About 3.46 km by 3.25 km (zone regions plus 500 m on each side) |
| Ground height in the play area | 44 m to 251 m on the game's height scale |
| Built-up area | About 6.7 km by 5.9 km (where buildings are placed) |
| Modes | King of the Hill |
| Light and weather | Clear midday by default; no day and night cycle |
| Vehicle spawns | 3 deployment boards and 12 vehicle yards (7 ground, 2 air, 3 light) and one extra air yard |
| **Zones** | |
| Control Zone | 500 m across, 500 m tall |
| Hot Zone | 85 m across, 850 m tall |
| Zone placements | 4 |
| Zone regions | 56 |
| Internal name | Server browser Detroit_KOTH_01; zone config NorthAmerica; region config NorthAmerica |
{: .wiki-infobox }

Zestafona is a King of the Hill map whose Control Zone is 500 m across and 500 m tall. Its Hot Zone is 85 m across but 850 m tall, much taller than the zone around it. The zone has no cylinder shape in the data, so it is stored as a tall box (inferred from the missing field). It has four placements and 56 named zone regions, mostly industrial sites and rail sheds.

## Overview

Zestafona is played in [King of the Hill](king-of-the-hill.md) under one server browser entry, Detroit. Its zone and region files are stored under the North America folder, and the example server rotation pairs the Detroit entry with the Zestafona placements.

## Modes played here

- [King of the Hill](king-of-the-hill.md).

## Zones and objectives

The Control Zone is 500 m across and 500 m tall. The Hot Zone is 85 m across and 850 m tall. The data does not say whether that height is intended, and it was not checked in game. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The zone has four placements. Default, Water Treatment and Houses each have weight 1, and one of them is drawn at random when the server rotation does not name one. Small Factory has weight 0, so it is used only when the server rotation names it.

| Placement | Weight |
|---|---|
| Default | 1 |
| Water Treatment | 1 |
| Houses | 1 |
| Small Factory | 0 |

- **Zone regions.** The data lists 56 named regions. Of these, 53 have weight 1, and the three towers have weight 0. Named sites include large factories, shipping and export yards, a scrap import area, train tracks and two train sheds. Every non-zero region is equally likely under the data. A region just used gives away half its weight, so it is unlikely to come up again at once.

## Vehicle spawns

The Detroit entry uses three spawn areas: Boston (Lonestar side), Austin (Valkyra side) and Chicago (Manticore side). In total the match has 12 vehicle yards in the spawn areas (7 ground, 2 air, 3 light), 3 deployment boards and 61 vehicle slots, plus one more air yard that is not part of any spawn area.

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots | From zone area middle | From nearest tower |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Lonestar | Boston | Lonestar version | 2 | 0 | 1 | 15 | 68 | 3,730 m | 3,440 m (tower 3) |
| Valkyra | Austin | Valkyra version | 2 | 1 | 1 | 22 | 60 | 3,930 m | 3,670 m (tower 1) |
| Manticore | Chicago | Manticore version | 3 | 1 | 1 | 24 | 81 | 3,650 m | 3,400 m (tower 2) |

Distances are straight-line metres from the middle of each side's infantry spawn points to the middle of the zone area and to the nearest Hot Zone Magnet tower (see Where the towers stand below). The Hot Zone itself moves, so these are distances to the area it can reach, not to the zone at a given moment. The deployment board stands within about 60 m of the spawn point.

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). The Boston area has no air yard of its own. The Lonestar side instead uses one extra air yard placed in the base map (7 slots), which is the only yard in the game data that lists helicopters by family: the Havoc, the Little Bird family, the Huey and the Z20 Lakota family. That it belongs to the base map is inferred, because it sits outside every spawn area.

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The data does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto the side's spawn vehicle (the APC), that player cannot deploy from the same board again for 600 s. If the APC is destroyed, the board counts down 300 s before it returns, or 60 s when the side is losing, which means the best other side is ahead by 15 score points or more at that moment. The countdown times the APC only, and the board does not put the APC out at all until one side has a score of 20. The data gives no return time for the other yard vehicles.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game files.

## Light and weather

Clear midday light by default: the sun stands about 44 degrees up, so shadows are short. Nothing changes during a match, because there is no day and night cycle and no changing weather. The server owner picks the lighting for each map entry from the presets on [Maps](maps.md#lighting-presets), so a server can run Zestafona in a foggy morning or an overcast afternoon instead. The map's own haze starts about 20 m from the viewer and is light (inferred; the chosen preset sets the final fog thickness).

## Cover materials

Most cover on Zestafona is made of the materials below. The counts are placed wall and building pieces taken from the map files, covering the part of the map around its zone regions (the area the Hot Zone can reach, plus 500 m on every side), which holds 98,745 of the 129,411 wall and building pieces placed on the whole map. A piece is one placed part such as a wall panel, floor, roof section, trim strip or fence section, so one building is many pieces. Each piece is counted under every material it uses, so a piece with brick walls and wood trim appears in both rows and the rows add up to more than the total. Pieces seen only as decals are left out. This was read from the game files, not checked in play, and broken-apart building pieces that appear when a building is destroyed are not included.

| Material | Pieces | Share of pieces | Mostly (from the material names) |
|---|---:|---:|---|
| Metal | 39,303 | 40% | girders, metal panels, painted metal |
| Concrete | 28,672 | 29% | apartment walls, concrete trim, apartment floors |
| Wood | 17,185 | 17% | wood trim, wooden roofs |
| Brick | 12,525 | 13% | brick and mortar, house walls |
| Plaster | 3,716 | 4% | plaster walls, wall mouldings, skirting boards |
| Dirt | 2,520 | 3% | trash piles, rubble |
| Rubber | 1,997 | 2% | rubber trim, roofing, flooring |
| Ceramic | 1,788 | 2% | window frames, tiled facades, flooring |

Total: 98,745 pieces (97,329 building pieces and 1,416 wall, fence and barrier pieces) from 986 different shapes. How hard each material is to shoot through is on [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md), which lists a density for each one.

## Size and ground height

The ground of this map is one square of 16.32 km by 16.32 km. Across the whole square the ground runs from 25 m to 707 m on the game's height scale. The play area is the box around every named zone region, plus 500 m on each side. It is the same box the cover and object counts on this page use. Inside it the ground runs from 44 m to 251 m.

The heights are read from the game's ground pieces, which are 510 m wide, so the real spread inside the box can be a little smaller. The height scale is the game's own and starts below zero on some maps, so only the difference between two heights means something. The box is 3.46 km by 3.25 km and the ground piece count that touches it is 64. Nothing here was measured in play.

## Placed objects

These are the things the map file places for players to use or break. "Around the zones" counts the objects inside the area the Hot Zone can reach plus 500 m on every side, the same area as the cover counts above. "Whole map file" counts everything in the file, and no other King of the Hill entry uses the same file (the Sniper Showdown layout for North America does), so it is larger than this map alone. The counts were read from the game files, not checked in play.

| Object | Around the zones | Whole map file | What it is |
|---|---:|---:|---|
| Hot Zone Magnet towers | 3 | 3 | Numbered 1 to 3. These are the capture towers of the [tower system](hot-zone-magnet-towers.md) and the source of the [tower and magnet rewards](../progression-and-economy/hot-zone-magnet-challenges.md). Positions are under Where the towers stand. |
| Doors you can open | 259 | 425 | Houses, apartments, garages, offices. A garage door counts once. Doors can also be broken, see [Destruction](../game-mechanics/destruction.md). |
| Ladders | 88 | 98 | Climbable with the ladder controls on [Movement](../game-mechanics/movement.md). |
| Breakable windows | 1,219 | 1,699 | Single panes that smash when hit. |
| Destructible buildings | 161 | 224 | Single buildings that can be knocked down: houses, garages, warehouses and shops, plus a few larger ones. Doors and windows are counted on their own rows. |
| Pre-placed barbed wire | 41 | 73 | Slows and hurts players and damages vehicles, like the [Barbed Wire](../building/barbed-wire.md) you can build. |
| Water | 3 river sections | 14 river sections | Water you can swim in. |
| Supply buildings | 1 | 3 | A kind of building. Its data shows no supply or pickup function. |

### Where the towers stand

The map names its zone regions, and each tower stands inside one of them. "The middle of the zone area" is the middle of the box around all regions. Distances are straight-line metres on the map, read from the game files. All three tower regions have weight 0, so the Hot Zone never lands on them by the random draw. How a tower is captured is on [Hot Zone Magnet Towers](hot-zone-magnet-towers.md).

| Tower | Region it stands in | From that region's middle | From the middle of the zone area |
|---|---|---:|---:|
| 1 | Tower 1 | 13 m | 260 m |
| 2 | Tower 2 | 17 m | 288 m |
| 3 | Tower 3 | 12 m | 289 m |

### In each team spawn area

The file places 3 team spawn areas for this map (the ones with a wager vendor; the other spawn areas in the file belong to other maps, inferred from that). Every area has a deployment board, an equipment vendor, a vehicle vendor, a garage vendor and a [wager vendor](../progression-and-economy/wagers.md), and also a free fuel point, a small soccer pitch, 3 moving practice targets and a safe zone. None of these areas lies inside the zone area. The invisible safe zone boxes are about 480 m tall; each safe zone is 480 m by 480 m. They protect their own team from damage, and the play-area edge, the out-of-bounds countdown and the other safe zone rules are on [Boundaries and Safe Zones](boundaries-and-safe-zones.md). The map's play rectangle is 10.5 km by 9.2 km.

The fuel point refuels vehicles without cost and does not run out (the data marks its fuel as unlimited and free in spawn). See [Fuel and refueling](../vehicles/fuel-and-refueling.md). Vehicle yards and spawn spots are on the Vehicle spawns section above.

### Not in the map files

The map file holds no capture points other than the Hot Zone Magnet towers, no pre-placed guns or emplacements, no ammo or supply pickups, no loot or crates and no zip lines. The free fuel point above is the only resupply object the file places.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#zestafona).

## Season 2 changes

- The shader warm-up list for this map was updated. Graphics pipeline states went from 1,870 to 1,000, and compute pipeline states from 76 to 79. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The data does not say what sight blockers do in play.
- The Season 2 notes list no change to this map's Control Zone.

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
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Placed objects per map (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-gameplay-actors.json)
- [Tower positions and map extents (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-magnets-extents.json)
