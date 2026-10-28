---
title: "Ozeti"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Ozeti King of the Hill map: a 550 m zone with four placements, and 55 named zone regions."
---

# Ozeti

| Ozeti | |
|---|---|
| **General** | |
| Map area | About 16.3 km square (minimap bounds) |
| Play area | About 3.8 km by 2.95 km (zone regions plus 500 m on each side) |
| Ground height in the play area | -988 m to -759 m on the game's height scale |
| Built-up area | About 6.6 km by 4.3 km (where buildings are placed) |
| Modes | King of the Hill |
| Light and weather | Clear late afternoon by default; no day and night cycle |
| Vehicle spawns | 3 deployment boards and 13 vehicle yards (7 ground, 3 air, 3 light) |
| **Zones** | |
| Control Zone | 550 m across, 150 m tall |
| Hot Zone | 85 m across, 150 m tall |
| Zone placements | 4 |
| Zone regions | 55 |
| Internal name | Server browser Madrid_KOTH_01; zone config Europe; region config Europe |
{: .wiki-infobox }

Ozeti is a King of the Hill map with a 550 m Control Zone and four possible zone placements. It has 55 named zone regions, almost all with weight 1. The game does not describe its streets or buildings. Its vehicle and infantry spawn areas are covered under Vehicle spawns.

![Ozeti map]({{ '/assets/img/maps/ozeti.jpg' | relative_url }})

*Ozeti minimap, orientation as in the game's minimap (the map has no north). Source: the game's world minimap texture, 16,384 px at 100 units per pixel, shown at about 3 m per pixel. The crop is the play box (zone regions plus 500 m) with a 500 m margin, about 4.8 km by 3.9 km, scale bar in the corner. The white outlines are the 55 named zone regions; magenta circles are the four Hot Zone Magnet towers, numbered as in the table below. Arrows point toward the three Madrid spawn areas (Granada, Barcelona, Malaga); Malaga lies off the top-left corner. Marks drawn from placed-object positions; the overview below shows the whole map.*

## Overview

Ozeti is played in [King of the Hill](king-of-the-hill.md) under one server browser entry, Madrid. Its zone configuration and regions are stored under the Europe files, and the example server rotation pairs the Madrid entry with the Ozeti placements.

## Modes played here

- [King of the Hill](king-of-the-hill.md).

## Zones and objectives

The Control Zone is 550 m across and 150 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The zone has four placements. Default, Church and River each have weight 1, and one of them is drawn at random when the server rotation does not name one. Farmland has weight 0, so it is used only when the server rotation names it.

| Placement | Weight |
|---|---|
| Default | 1 |
| Church | 1 |
| River | 1 |
| Farmland | 0 |

- **Zone regions.** The game lists 55 named regions. Of these, 54 have weight 1 and one, Tower 2, has weight 0. Regions are named for towers and points of interest such as the stadium, pool, church top, lumberyard and apartments. Every non-zero region is equally likely, because no other weight values appear. A region just used gives away half its weight, so it is unlikely to come up again at once.

## Vehicle spawns

The Madrid entry gives each side its own spawn area with a vehicle deployment board, a set of vehicle yards and an infantry spawn area. The areas are called Granada (Lonestar side), Barcelona (Valkyra side) and Malaga (Manticore side) in the files. In total the match has 13 vehicle yards (7 ground, 3 air, 3 light), 3 deployment boards and 74 vehicle slots.

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots | From zone area middle | From nearest tower |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Lonestar | Granada | Lonestar version | 2 | 1 | 1 | 22 | 81 | 3,520 m | 3,290 m (tower 2) |
| Valkyra | Barcelona | Valkyra version | 2 | 1 | 1 | 25 | 61 | 4,010 m | 3,380 m (tower 3) |
| Manticore | Malaga | Manticore version | 3 | 1 | 1 | 27 | 72 | 3,890 m | 3,720 m (tower 1) |

Distances are straight-line metres from the middle of each side's infantry spawn points to the middle of the zone area and to the nearest Hot Zone Magnet tower (see Where the towers stand below). The Hot Zone itself moves, so these are distances to the area it can reach, not to the zone at a given moment. The deployment board stands within about 60 m of the spawn point.

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). The Malaga area has a third ground yard, which is why the totals are not equal across sides.

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The game does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto the side's spawn vehicle (the APC), that player cannot deploy from the same board again for 600 s. If the APC is destroyed, the board counts down 300 s before it returns, or 60 s when the side is losing, which means the best other side is ahead by 15 score points or more at that moment. The countdown times the APC only, and the board does not put the APC out at all until one side has a score of 20. The game gives no return time for the other yard vehicles.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game.

## Light and weather

Clear late afternoon light by default: the sun stands only about 20 degrees up, so shadows are long and the low sun comes from one fixed direction. Nothing changes during a match, because there is no day and night cycle and no changing weather. The server owner picks the lighting for each map entry from the presets on [Maps](maps.md#lighting-presets), so a server can run Ozeti in midday light or an overcast or foggy setting instead. The map's own haze starts about 100 m from the viewer and is light (inferred; the chosen preset sets the final fog thickness).

## Cover materials

Most cover on Ozeti is made of the materials below. The counts are placed wall and building pieces taken from the map files, covering the part of the map around its zone regions (the area the Hot Zone can reach, plus 500 m on every side), which holds 69,833 of the 114,190 wall and building pieces placed on the whole map. A piece is one placed part such as a wall panel, floor, roof section, trim strip or fence section, so one building is many pieces. Each piece is counted under every material it uses, so a piece with brick walls and wood trim appears in both rows and the rows add up to more than the total. Pieces seen only as decals are left out. This was read from the game, not checked in play, and broken-apart building pieces that appear when a building is destroyed are not included.

| Material | Pieces | Share of pieces | Mostly (from the material names) |
|---|---:|---:|---|
| Wood | 21,921 | 31% | wood trim, wooden roofs |
| Brick | 16,523 | 24% | house walls, brick and mortar |
| Concrete | 14,051 | 20% | apartment floors, apartment walls, concrete trim |
| Metal | 12,286 | 18% | corrugated sheet, girders, painted metal |
| Plaster | 5,370 | 8% | plaster walls, wall mouldings, skirting boards |
| Rubber | 4,265 | 6% | rubber trim, roofing, flooring |
| Ceramic | 2,269 | 3% | window frames, tiled facades, flooring |
| Rock | 1,083 | 2% | house foundations, church stonework |
| Dirt | 745 | 1% | trash piles, rubble |

Total: 69,833 pieces (66,641 building pieces and 3,192 wall, fence and barrier pieces) from 828 different shapes. How hard each material is to shoot through is on [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md), which lists a density for each one.

## Size and ground height

![Ozeti overview map]({{ '/assets/img/maps/ozeti-overview.jpg' | relative_url }})

*Whole minimap (16.3 km square, orientation as in the game's minimap). The white box is the play box shown above; coloured dots are the three spawn areas (infantry spawn point middles).*

The ground of this map is one square of 16.32 km by 16.32 km. Across the whole square the ground runs from -1,037 m to -275 m on the game's height scale. The play area is the box around every named zone region, plus 500 m on each side. It is the same box the cover and object counts on this page use. Inside it the ground runs from -988 m to -759 m.

The heights are read from the game's ground pieces, which are 510 m wide, so the real spread inside the box can be a little smaller. The height scale is the game's own and starts below zero on some maps, so only the difference between two heights means something. The box is 3.8 km by 2.95 km and the ground piece count that touches it is 54. Nothing here was measured in play.

## Water height

![Ozeti water surface height]({{ '/assets/img/maps/ozeti-water-height.png' | relative_url }})

*Height of the water surface in the 17 river and lake sections of the map. Dry ground is dark. The white box is the play box. The map is drawn the same way as the minimap, with +Y running down.*

The game stores the water of this map as 17 height grids that each cover a square or rectangle of ground. The grids together span about 15.8 km by 13.0 km and run from -1,063 m to -883 m on the game's height scale (the same scale as the ground heights above). Each grid cell is 2 m to 12 m wide; most are 2 m.

The numbers are read straight from the game. The water is flat on lakes and falls steadily along each river toward the low end, and neighbouring grids agree where they overlap, to within a few tens of centimetres. Per-grid figures are in the [water height table](../../content/Wardogs_Environment_v2.md#13b-height-grids).

## Placed objects

These are the things the map file places for players to use or break. "Around the zones" counts the objects inside the area the Hot Zone can reach plus 500 m on every side, the same area as the cover counts above. "Whole map file" counts everything in the file, and Berlin and Paris use the same file, so it is larger than this map alone. The counts were read from the game, not checked in play.

| Object | Around the zones | Whole map file | What it is |
|---|---:|---:|---|
| Hot Zone Magnet towers | 4 | 4 | Numbered 1 to 4. These are the capture towers of the [tower system](hot-zone-magnet-towers.md) and the source of the [tower and magnet rewards](../progression-and-economy/hot-zone-magnet-challenges.md). Positions are under Where the towers stand. |
| Doors you can open | 188 | 349 | Houses, apartments, garages. A garage door counts once. Doors can also be broken, see [Destruction](../game-mechanics/destruction.md). |
| Ladders | 22 | 34 | Climbable with the ladder controls on [Movement](../game-mechanics/movement.md). |
| Breakable windows | 1,425 | 2,358 | Single panes that smash when hit. |
| Destructible buildings | 247 | 354 | Single buildings that can be knocked down: houses, garages, warehouses and shops, plus a few larger ones. Doors and windows are counted on their own rows. |
| Pre-placed barbed wire | 32 | 32 | Slows and hurts players and damages vehicles, like the [Barbed Wire](../building/barbed-wire.md) you can build. |
| Water | 4 river sections, a swimming pool | 17 river sections, a swimming pool | Water you can swim in. |
| Supply buildings | 1 | 1 | A kind of building. It has no supply or pickup function. |

### Where the towers stand

The map names its zone regions, and each tower stands inside one of them. "The middle of the zone area" is the middle of the box around all regions. Distances are straight-line metres on the map, read from the game. The region named Tower 2 has weight 0; the regions named Tower 1, 3 and 4 have weight 1, so the Hot Zone can land on them by the random draw. How a tower is captured is on [Hot Zone Magnet Towers](hot-zone-magnet-towers.md).

| Tower | Region it stands in | From that region's middle | From the middle of the zone area |
|---|---|---:|---:|
| 1 | Tower 1 | 15 m | 238 m |
| 2 | Tower 2 | 6 m | 426 m |
| 3 | Tower 3 | 2 m | 632 m |
| 4 | Tower 4 | 11 m | 526 m |

### In each team spawn area

The file places 3 team spawn areas for this map (the ones with a wager vendor; the other spawn areas in the file belong to other maps, inferred from that). Every area has a deployment board, an equipment vendor, a vehicle vendor, a garage vendor and a [wager vendor](../progression-and-economy/wagers.md), and also a free fuel point, a small soccer pitch (2 of 3 areas), 3 moving practice targets and a safe zone (all 3 areas; one lies 155 m from its spawn point, just beyond the 150 m radius used here). None of these areas lies inside the zone area. The invisible safe zone boxes are about 480 m tall; each safe zone is 480 m by 480 m. They protect their own team from damage, and the play-area edge, the out-of-bounds countdown and the other safe zone rules are on [Boundaries and Safe Zones](boundaries-and-safe-zones.md). The map's play rectangle is 8.5 km by 7.8 km.

The fuel point refuels vehicles without cost and does not run out (the game marks its fuel as unlimited and free in spawn). See [Fuel and refueling](../vehicles/fuel-and-refueling.md). Vehicle yards and spawn spots are on the Vehicle spawns section above.

### Not in the map files

The map file holds no capture points other than the Hot Zone Magnet towers, no pre-placed guns or emplacements, no ammo or supply pickups, no loot or crates and no zip lines. The free fuel point above is the only resupply object the file places.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#ozeti).

## Season 2 changes

- The shader warm-up list for this map was updated. Graphics pipeline states went from 1,639 to 1,053, and compute pipeline states from 6 to 83. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The game does not say what sight blockers do in play.
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
- [Environment data: water height grids](../../content/Wardogs_Environment_v2.md#13b-height-grids)
- [Water height grids (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-height-grids.json)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Placed objects per map (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-gameplay-actors.json)
- [Tower positions and map extents (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-magnets-extents.json)
