---
title: "Ozeti"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Ozeti King of the Hill map: a 550 m zone with four placements, and 55 named zone regions in the data."
---

# Ozeti

| Ozeti | |
|---|---|
| **General** | |
| Map area | About 16.3 km square (minimap bounds) |
| Modes | King of the Hill |
| Vehicle spawns | 3 deployment boards and 13 vehicle yards (7 ground, 3 air, 3 light) |
| **Zones** | |
| Control Zone | 550 m across, 150 m tall |
| Hot Zone | 85 m across, 150 m tall |
| Zone placements | 4 |
| Zone regions | 55 |
| Internal name | Server browser Madrid_KOTH_01; zone config Europe; region config Europe |
{: .wiki-infobox }

Ozeti is a King of the Hill map with a 550 m Control Zone and four possible zone placements. It has 55 named zone regions, almost all with weight 1. The data does not describe its streets or buildings. Its vehicle and infantry spawn areas are covered under Vehicle spawns.

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

- **Zone regions.** The data lists 55 named regions. Of these, 54 have weight 1 and one, Tower 2, has weight 0. Regions are named for towers and points of interest such as the stadium, pool, church top, lumberyard and apartments. Every non-zero region is equally likely under the data, because no other weight values appear. A region just used gives away half its weight, so it is unlikely to come up again at once.

## Vehicle spawns

The Madrid entry gives each side its own spawn area with a vehicle deployment board, a set of vehicle yards and an infantry spawn area. The areas are called Granada (Lonestar side), Barcelona (Valkyra side) and Malaga (Manticore side) in the files. In total the match has 13 vehicle yards (7 ground, 3 air, 3 light), 3 deployment boards and 74 vehicle slots.

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots |
|---|---|---|---:|---:|---:|---:|---:|
| Lonestar | Granada | Lonestar version | 2 | 1 | 1 | 22 | 81 |
| Valkyra | Barcelona | Valkyra version | 2 | 1 | 1 | 25 | 61 |
| Manticore | Malaga | Manticore version | 3 | 1 | 1 | 27 | 72 |

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). The Malaga area has a third ground yard, which is why the totals are not equal across sides.

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The data does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto a spawn vehicle, the deployment board's cooldown is 600 s (this value is stored; its start trigger was not traced). How long a destroyed vehicle takes to return is not in the data.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game files.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#ozeti).

## Season 2 changes

- The shader warm-up list for this map was updated. Graphics pipeline states went from 1,639 to 1,053, and compute pipeline states from 6 to 83. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The data does not say what sight blockers do in play.
- The Season 2 notes list no change to this map's Control Zone.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Maps](maps.md)

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
