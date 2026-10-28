---
title: "Bakurani"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Bakurani King of the Hill map: zone sizes, the three zone placements, and the 60 named zone regions listed for it."
---

# Bakurani

| Bakurani | |
|---|---|
| **General** | |
| Map area | About 16.3 km square (minimap bounds) |
| Play area | About 3.33 km by 3.45 km (zone regions plus 500 m on each side) |
| Ground height in the play area | -991 m to -278 m on the game's height scale |
| Built-up area | About 7.8 km by 7.7 km (where buildings are placed) |
| Modes | King of the Hill, two server browser entries |
| Light and weather | Clear midday by default; no day and night cycle |
| Vehicle spawns | 3 deployment boards per entry; 13 vehicle yards in the first entry and 12 in the second |
| **Zones** | |
| Control Zone | 500 m across, 170 m tall |
| Hot Zone | 85 m across, 170 m tall |
| Zone placements | 3 |
| Zone regions | 60 |
| Internal name | Server browser Bakurani_KOTH_01 and Bakurani_KOTH_02; zone config Bakurani; region config and minimap folder Kavkazi |
{: .wiki-infobox }

Bakurani is the first King of the Hill map in the server browser, and it is the one with the most zone information. It has three alternative zone placements and 60 named zone regions, so the zone can appear in several parts of the map. The game does not describe its streets or buildings. Its vehicle and infantry spawn areas are covered under Vehicle spawns.

![Bakurani map]({{ '/assets/img/maps/bakurani.jpg' | relative_url }})

*Bakurani minimap, orientation as in the game's minimap (the map has no north). Source: the game's world minimap texture, 16,384 px at 100 units per pixel, shown at about 2.8 m per pixel. The crop is the play box (zone regions plus 500 m) with a 500 m margin, about 4.3 km by 4.4 km, scale bar in the corner. The white outlines are the 60 named zone regions, with the five Hot Zone Magnet tower regions drawn heavier; magenta circles are the towers, numbered as in the table below. Arrows point toward the three spawn areas of the first server browser entry (Baghi, Khevuli, Chuta), which lie 3.8 to 4.1 km from the middle of the crop. Tower 5 has no region of its own, and TOWER 7 is not placed. Marks drawn from placed-object positions; the overview below shows the whole map.*

## Overview

Bakurani is played in [King of the Hill](king-of-the-hill.md). The server browser lists it as two entries, both called Bakurani. They share the same map and rules and differ only in their spawn areas: the first uses the Khevuli, Chuta and Baghi areas, the second the Rachuri, Tavarshi and Sanavi areas. Both use the Bakurani name and loading screen art, and the Bakurani zone configuration.

## Modes played here

- [King of the Hill](king-of-the-hill.md), in both server browser entries.
- Not used for Sniper Showdown. The Sniper Showdown map with a Bakurani name is a separate entry, [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md).

## Zones and objectives

The Control Zone is 500 m across and 170 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds. Its default speed is 1.0, and the speed table runs from 0.75 to 2.0.
- **Placements.** The zone has three placements. The server rotation can name one for a match. Without a name, one is drawn at random by weight, so the default (weight 2) is twice as likely as Farmland or Lumberyard (weight 1 each). The example server rotation names a Bakurani River entry, which has no placement in the game, so that match falls back to the random draw: Default 50%, Farmland 25%, Lumberyard 25%.

| Placement | Weight |
|---|---|
| Default | 2 |
| Farmland | 1 |
| Lumberyard | 1 |

- **Zone regions.** The game lists 60 named regions. Seven are towers with weight 0, which are never drawn at random. Most other regions have weight 1, and a few have weight 5, including SUNFLOWERS HOUSE, WEST FOREST PYLON and HILLSIDE TOP, which makes them much more likely. The Hot Zone moves to a region drawn at random by weight, and the region just used gives away half its weight, so it is unlikely to come up again at once. Regions overlap in 33 pairs, which does not affect the draw.

## Vehicle spawns

Bakurani has two server browser entries with different spawn areas, so its vehicle spawns differ between them. The first entry uses Baghi (Lonestar side), Khevuli (Valkyra side) and Chuta (Manticore side) and has 13 vehicle yards (7 ground, 3 air, 3 light) with 67 vehicle slots. The second uses Sanavi (Lonestar side), Rachuri (Valkyra side) and Tavarshi (Manticore side) and has 12 vehicle yards (6 ground, 3 air, 3 light) with 72 vehicle slots. Both entries have 3 deployment boards.

**First entry (Baghi, Khevuli, Chuta)**

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots | From zone area middle | From nearest tower |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Lonestar | Baghi | Lonestar version | 3 | 1 | 1 | 25 | 69 | 3,940 m | 3,610 m (tower 5) |
| Valkyra | Khevuli | Valkyra version | 1 | 1 | 1 | 21 | 46 | 3,810 m | 3,500 m (tower 4) |
| Manticore | Chuta | Manticore version | 3 | 1 | 1 | 21 | 81 | 4,130 m | 3,780 m (tower 3) |

**Second entry (Sanavi, Rachuri, Tavarshi)**

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots | From zone area middle | From nearest tower |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| Lonestar | Sanavi | Lonestar version | 2 | 1 | 1 | 23 | 81 | 3,900 m | 3,650 m (tower 2) |
| Valkyra | Rachuri | Valkyra version | 2 | 1 | 1 | 25 | 69 | 3,850 m | 3,520 m (tower 4) |
| Manticore | Tavarshi | Manticore version | 2 | 1 | 1 | 24 | 69 | 3,820 m | 3,460 m (tower 3) |

Distances are straight-line metres from the middle of each side's infantry spawn points to the middle of the zone area and to the nearest Hot Zone Magnet tower (see Where the towers stand below). The Hot Zone itself moves, so these are distances to the area it can reach, not to the zone at a given moment. The deployment board stands within about 60 m of the spawn point.

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). In the first entry the Khevuli area has no APC volume of its own and only one ground yard; the Baghi and Chuta areas have three ground yards. One Baghi yard also allows the Azar test vehicle, which has no wiki article. The Chuta infantry spawn area is the largest in the first entry. 

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The game does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto the side's spawn vehicle (the APC), that player cannot deploy from the same board again for 600 s. If the APC is destroyed, the board counts down 300 s before it returns, or 60 s when the side is losing, which means the best other side is ahead by 15 score points or more at that moment. The countdown times the APC only, and the board does not put the APC out at all until one side has a score of 20. The game gives no return time for the other yard vehicles.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game.

## Light and weather

Clear midday light by default: the sun stands about 44 degrees up, so shadows are short. Nothing changes during a match, because there is no day and night cycle and no changing weather. The server owner picks the lighting for each map entry from the presets on [Maps](maps.md#lighting-presets), so a server can run Bakurani in a foggy morning or an overcast afternoon instead. The map's own haze starts about 20 m from the viewer and is light (inferred; the chosen preset sets the final fog thickness).

## Cover materials

Most cover on Bakurani is made of the materials below. The counts are placed wall and building pieces taken from the map files, covering the part of the map around its zone regions (the area the Hot Zone can reach, plus 500 m on every side), which holds 109,586 of the 202,748 wall and building pieces placed on the whole map. A piece is one placed part such as a wall panel, floor, roof section, trim strip or fence section, so one building is many pieces. Each piece is counted under every material it uses, so a piece with brick walls and wood trim appears in both rows and the rows add up to more than the total. Pieces seen only as decals are left out. This was read from the game, not checked in play, and broken-apart building pieces that appear when a building is destroyed are not included.

| Material | Pieces | Share of pieces | Mostly (from the material names) |
|---|---:|---:|---|
| Wood | 30,535 | 28% | wood trim, wooden roofs |
| Concrete | 25,274 | 23% | apartment floors, apartment walls, concrete trim |
| Brick | 24,195 | 22% | house walls, brick and mortar |
| Metal | 23,380 | 21% | girders, corrugated sheet, painted metal |
| Plaster | 7,960 | 7% | plaster walls, wall mouldings, skirting boards |
| Rubber | 5,413 | 5% | rubber trim, roofing, flooring |
| Ceramic | 3,743 | 3% | window frames, tiled facades, flooring |
| Rock | 1,587 | 1% | house foundations, church stonework |
| Dirt | 1,367 | 1% | trash piles, rubble |

Total: 109,586 pieces (106,793 building pieces and 2,793 wall, fence and barrier pieces) from 845 different shapes. How hard each material is to shoot through is on [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md), which lists a density for each one.

## Size and ground height

![Bakurani overview map]({{ '/assets/img/maps/bakurani-overview.jpg' | relative_url }})

*Whole minimap (16.3 km square, orientation as in the game's minimap). The white box is the play box shown above; coloured dots are the three spawn areas (infantry spawn point middles).*

The ground of this map is one square of 16.32 km by 16.32 km. Across the whole square the ground runs from -1,008 m to 178 m on the game's height scale. The play area is the box around every named zone region, plus 500 m on each side. It is the same box the cover and object counts on this page use. Inside it the ground runs from -991 m to -278 m.

The heights are read from the game's ground pieces, which are 1020 m wide, so the real spread inside the box can be a little smaller. The height scale is the game's own and starts below zero on some maps, so only the difference between two heights means something. The box is 3.33 km by 3.45 km and the ground piece count that touches it is 16. Nothing here was measured in play.

## Water height

![Bakurani water surface height]({{ '/assets/img/maps/bakurani-water-height.png' | relative_url }})

*Height of the water surface in the 23 river and lake sections of the map. Dry ground is dark. The white box is the play box. The map is drawn the same way as the minimap, with +Y running down.*

The game stores the water of this map as 23 height grids that each cover a square or rectangle of ground. The grids together span about 15.9 km by 9.4 km and run from -1,016 m to -806 m on the game's height scale (the same scale as the ground heights above). Each grid cell is 2 m wide, except one grid at 4 m.

The numbers are read straight from the game. The water is flat on lakes and falls steadily along each river toward the low end, and neighbouring grids agree where they overlap, to within a few tens of centimetres. Per-grid figures are in the [water height table](../../content/Wardogs_Environment_v2.md#13b-height-grids).

## Placed objects

These are the things the map file places for players to use or break. "Around the zones" counts the objects inside the area the Hot Zone can reach plus 500 m on every side, the same area as the cover counts above. "Whole map file" counts everything in the file, and Mindori and Tevza (and Bakurani Outskirts - Jutari) use the same file, so it is larger than this map alone. The counts were read from the game, not checked in play.

| Object | Around the zones | Whole map file | What it is |
|---|---:|---:|---|
| Hot Zone Magnet towers | 5 | 5 | Numbered 1 to 5. These are the capture towers of the [tower system](hot-zone-magnet-towers.md) and the source of the [tower and magnet rewards](../progression-and-economy/hot-zone-magnet-challenges.md). Positions are under Where the towers stand. |
| Doors you can open | 283 | 585 | Houses, apartments, garages. A garage door counts once. Doors can also be broken, see [Destruction](../game-mechanics/destruction.md). |
| Ladders | 54 | 100 | Climbable with the ladder controls on [Movement](../game-mechanics/movement.md). |
| Breakable windows | 1,916 | 3,779 | Single panes that smash when hit. |
| Destructible buildings | 264 | 446 | Single buildings that can be knocked down: houses, garages, warehouses and shops, plus a few larger ones. Doors and windows are counted on their own rows. |
| Pre-placed barbed wire | 33 | 161 | Slows and hurts players and damages vehicles, like the [Barbed Wire](../building/barbed-wire.md) you can build. |
| Water | 3 lakes, 6 river sections | 3 lakes, 23 river sections | Water you can swim in. |

### Where the towers stand

The map names its zone regions, and each tower stands inside one of them. "The middle of the zone area" is the middle of the box around all regions. Distances are straight-line metres on the map, read from the game. Towers 1 to 4 stand in the regions named Tower 1 to Tower 4, which have weight 0 so the Hot Zone never lands there by the random draw. Tower 5 stands in Lumberyard North, 78 m from a small region named Tower 5 L. A region named Tower 7 exists in the list, but the map places no tower there. How a tower is captured is on [Hot Zone Magnet Towers](hot-zone-magnet-towers.md).

| Tower | Region it stands in | From that region's middle | From the middle of the zone area |
|---|---|---:|---:|
| 1 | Tower 1 | 2 m | 160 m |
| 2 | Tower 2 | 19 m | 360 m |
| 3 | Tower 3 | 18 m | 382 m |
| 4 | Tower 4 | 17 m | 337 m |
| 5 | Lumberyard North | 39 m | 354 m |

### In each team spawn area

The file places 6 team spawn areas for this map (the ones with a wager vendor; the other spawn areas in the file belong to other maps, inferred from that). Every area has a deployment board, an equipment vendor, a vehicle vendor, a garage vendor and a [wager vendor](../progression-and-economy/wagers.md), and also a free fuel point, a small soccer pitch, 3 moving practice targets and a safe zone (all 6 areas; one lies 166 m from its spawn point, just beyond the 150 m radius used here). None of these areas lies inside the zone area. The invisible safe zone boxes are about 480 m tall; three safe zones are 640 m by 640 m and three are 480 m by 480 m. They protect their own team from damage, and the play-area edge, the out-of-bounds countdown and the other safe zone rules are on [Boundaries and Safe Zones](boundaries-and-safe-zones.md). The map's play rectangle is 11.0 km by 11.0 km.

The fuel point refuels vehicles without cost and does not run out (the game marks its fuel as unlimited and free in spawn). See [Fuel and refueling](../vehicles/fuel-and-refueling.md). Vehicle yards and spawn spots are on the Vehicle spawns section above.

### Not in the map files

The map file holds no capture points other than the Hot Zone Magnet towers, no pre-placed guns or emplacements, no ammo or supply pickups, no loot or crates and no zip lines. The free fuel point above is the only resupply object the file places.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#bakurani).

## Season 2 changes

- The shader warm-up list for this map was updated. Its old count was withdrawn because the old file was cut short. The new file lists 867 graphics pipeline states and 117 compute pipeline states. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The game does not say what sight blockers do in play.
- The Season 2 notes list no change to this map's Control Zone or regions.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Maps](maps.md)
- [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md)

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
