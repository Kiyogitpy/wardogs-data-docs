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
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto a spawn vehicle, the deployment board's cooldown is 600 s (this value is stored; its start trigger was not traced). How long a destroyed vehicle takes to return is not in the data.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game files.

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
- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
