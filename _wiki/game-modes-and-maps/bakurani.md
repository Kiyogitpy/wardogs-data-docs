---
title: "Bakurani"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Bakurani King of the Hill map: zone sizes, the three zone placements, and the 60 named zone regions the data lists for it."
---

# Bakurani

| Bakurani | |
|---|---|
| **General** | |
| Map area | About 16.3 km square (minimap bounds) |
| Built-up area | About 7.8 km by 7.7 km (where buildings are placed) |
| Modes | King of the Hill, two server browser entries |
| Vehicle spawns | 3 deployment boards per entry; 13 vehicle yards in the first entry and 12 in the second |
| **Zones** | |
| Control Zone | 500 m across, 170 m tall |
| Hot Zone | 85 m across, 170 m tall |
| Zone placements | 3 |
| Zone regions | 60 |
| Internal name | Server browser Bakurani_KOTH_01 and Bakurani_KOTH_02; zone config Bakurani; region config and minimap folder Kavkazi |
{: .wiki-infobox }

Bakurani is the first King of the Hill map in the server browser, and it is the one with the most zone data. It has three alternative zone placements and 60 named zone regions, so the zone can appear in several parts of the map. The data does not describe its streets or buildings. Its vehicle and infantry spawn areas are covered under Vehicle spawns.

## Overview

Bakurani is played in [King of the Hill](king-of-the-hill.md). The server browser lists it as two entries, both called Bakurani. They share the same map and rules and differ only in their spawn areas: the first uses the Khevuli, Chuta and Baghi areas, the second the Rachuri, Tavarshi and Sanavi areas. Both use the Bakurani name and loading screen art, and the Bakurani zone configuration.

## Modes played here

- [King of the Hill](king-of-the-hill.md), in both server browser entries.
- Not used for Sniper Showdown. The Sniper Showdown map with a Bakurani name is a separate entry, [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md).

## Zones and objectives

The Control Zone is 500 m across and 170 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds. Its default speed is 1.0, and the speed table runs from 0.75 to 2.0.
- **Placements.** The zone has three placements. The server rotation can name one for a match. Without a name, one is drawn at random by weight, so the default (weight 2) is twice as likely as Farmland or Lumberyard (weight 1 each). The example server rotation names a Bakurani River entry, which has no placement in the game files, so that match falls back to the random draw: Default 50%, Farmland 25%, Lumberyard 25%.

| Placement | Weight |
|---|---|
| Default | 2 |
| Farmland | 1 |
| Lumberyard | 1 |

- **Zone regions.** The data lists 60 named regions. Seven are towers with weight 0, which are never drawn at random. Most other regions have weight 1, and a few have weight 5, including SUNFLOWERS HOUSE, WEST FOREST PYLON and HILLSIDE TOP, which makes them much more likely. The Hot Zone moves to a region drawn at random by weight, and the region just used gives away half its weight, so it is unlikely to come up again at once. Regions overlap in 33 pairs, which does not affect the draw.

## Vehicle spawns

Bakurani has two server browser entries with different spawn areas, so its vehicle spawns differ between them. The first entry uses Baghi (Lonestar side), Khevuli (Valkyra side) and Chuta (Manticore side) and has 13 vehicle yards (7 ground, 3 air, 3 light) with 67 vehicle slots. The second uses Sanavi (Lonestar side), Rachuri (Valkyra side) and Tavarshi (Manticore side) and has 12 vehicle yards (6 ground, 3 air, 3 light) with 72 vehicle slots. Both entries have 3 deployment boards.

**First entry (Baghi, Khevuli, Chuta)**

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots |
|---|---|---|---:|---:|---:|---:|---:|
| Lonestar | Baghi | Lonestar version | 3 | 1 | 1 | 25 | 69 |
| Valkyra | Khevuli | Valkyra version | 1 | 1 | 1 | 21 | 46 |
| Manticore | Chuta | Manticore version | 3 | 1 | 1 | 21 | 81 |

**Second entry (Sanavi, Rachuri, Tavarshi)**

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots |
|---|---|---|---:|---:|---:|---:|---:|
| Lonestar | Sanavi | Lonestar version | 2 | 1 | 1 | 23 | 81 |
| Valkyra | Rachuri | Valkyra version | 2 | 1 | 1 | 25 | 69 |
| Manticore | Tavarshi | Manticore version | 2 | 1 | 1 | 24 | 69 |

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). In the first entry the Khevuli area has no APC volume of its own and only one ground yard; the Baghi and Chuta areas have three ground yards. One Baghi yard also allows the Azar test vehicle, which has no wiki article. The Chuta infantry spawn area is the largest in the first entry. 

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The data does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto a spawn vehicle, the deployment board's cooldown is 600 s (this value is stored; its start trigger was not traced). The deployment board's built-in respawn timers are 300 s, or 60 s for a losing side. They most likely time the side's spawn vehicle (inferred from their names). The data gives no return time for the other yard vehicles.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game files.

## Cover materials

Most cover on Bakurani is made of the materials below. The counts are placed wall and building pieces taken from the map files, covering the part of the map around its zone regions (the area the Hot Zone can reach, plus 500 m on every side), which holds 109,586 of the 202,748 wall and building pieces placed on the whole map. A piece is one placed part such as a wall panel, floor, roof section, trim strip or fence section, so one building is many pieces. Each piece is counted under every material it uses, so a piece with brick walls and wood trim appears in both rows and the rows add up to more than the total. Pieces seen only as decals are left out. This was read from the game files, not checked in play, and broken-apart building pieces that appear when a building is destroyed are not included.

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

## Placed objects

These are the things the map file places for players to use or break. "Around the zones" counts the objects inside the area the Hot Zone can reach plus 500 m on every side, the same area as the cover counts above. "Whole map file" counts everything in the file, and Mindori and Tevza (and Bakurani Outskirts - Jutari) use the same file, so it is larger than this map alone. The counts were read from the game files, not checked in play.

| Object | Around the zones | Whole map file | What it is |
|---|---:|---:|---|
| Hot Zone Magnet towers | 5 | 5 | Numbered 1 to 5. The King of the Hill [tower and magnet rewards](../progression-and-economy/hot-zone-magnet-challenges.md) belong to these (inferred from the shared name). |
| Doors you can open | 283 | 585 | Houses, apartments, garages. A garage door counts once. Doors can also be broken, see [Destruction](../game-mechanics/destruction.md). |
| Ladders | 54 | 100 | Climbable with the ladder controls on [Movement](../game-mechanics/movement.md). |
| Breakable windows | 1,916 | 3,779 | Single panes that smash when hit. |
| Destructible buildings | 264 | 446 | Single buildings that can be knocked down: houses, garages, warehouses and shops, plus a few larger ones. Doors and windows are counted on their own rows. |
| Pre-placed barbed wire | 33 | 161 | Slows and hurts players and damages vehicles, like the [Barbed Wire](../building/barbed-wire.md) you can build. |
| Water | 3 lakes, 6 river sections | 3 lakes, 23 river sections | Water you can swim in. |

### In each team spawn area

The file places 6 team spawn areas for this map (the ones with a wager vendor; the other spawn areas in the file belong to other maps, inferred from that). Every area has a deployment board, an equipment vendor, a vehicle vendor, a garage vendor and a [wager vendor](../progression-and-economy/wagers.md), and also a free fuel point, a small soccer pitch, 3 moving practice targets and a safe zone (5 of 6 areas). None of these areas lies inside the zone area.

The fuel point refuels vehicles without cost and does not run out (the data marks its fuel as unlimited and free in spawn). See [Fuel and refueling](../vehicles/fuel-and-refueling.md). Vehicle yards and spawn spots are on the Vehicle spawns section above.

### Not in the map files

The map file holds no capture towers other than the Hot Zone Magnet towers, no pre-placed guns or emplacements, no ammo or supply pickups, no loot or crates and no zip lines. The free fuel point above is the only resupply object the file places.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#bakurani).

## Season 2 changes

- The shader warm-up list for this map was updated. Its old count was withdrawn because the old file was cut short. The new file lists 867 graphics pipeline states and 117 compute pipeline states. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The data does not say what sight blockers do in play.
- The Season 2 notes list no change to this map's Control Zone or regions.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Maps](maps.md)
- [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md)

## Sources

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
