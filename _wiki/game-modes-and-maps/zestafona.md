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
| Modes | King of the Hill |
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

| Side | Spawn area | Deployment board | Ground yards | Air yards | Light yards | Vehicle slots | Infantry spawn spots |
|---|---|---|---:|---:|---:|---:|---:|
| Lonestar | Boston | Lonestar version | 2 | 0 | 1 | 15 | 68 |
| Valkyra | Austin | Valkyra version | 2 | 1 | 1 | 22 | 60 |
| Manticore | Chicago | Manticore version | 3 | 1 | 1 | 24 | 81 |

The side names follow the spawn vehicle that each area's yards list (Lonestar, Valkyra or Manticore version; the pairing with the three team slots is inferred, see the [Vehicle Spawns data page](../../game-features/Wardogs_VehicleSpawns_v1.md)). Vehicle slots are the places where each side's yards park vehicles (inferred from the yard's target points). The Boston area has no air yard of its own. The Lonestar side instead uses one extra air yard placed in the base map (7 slots), which is the only yard in the game data that lists helicopters by family: the Havoc, the Little Bird family, the Huey and the Z20 Lakota family. That it belongs to the base map is inferred, because it sits outside every spawn area.

- **Vehicles offered (inferred).** The yards do not name vehicles one by one; they allow vehicle families by tag. The ground yards allow the Humvee, Kodiak, Ural, Dune Buggy and Wolf 110 families (each family covers its gun variants), the tank family of the L2A6, Flakpanzer Gepard and SPH-2, and the T-72B3. The light yards allow only the Bobcat. The air yards allow any helicopter (the fixed-wing airplane is under the same tag; whether a yard ever places it was not checked). The data does not say how many of each vehicle a yard holds or in what order they appear.
- **Limits and timers.** A player may own at most 2 spawned vehicles at a time. After a player deploys onto a spawn vehicle, the deployment board's cooldown is 600 s (this value is stored; its start trigger was not traced). The deployment board's built-in respawn timers are 300 s, or 60 s for a losing side. They most likely time the side's spawn vehicle (inferred from their names). The data gives no return time for the other yard vehicles.
- **What is not known.** Which vehicle each slot gives, how many vehicles of one kind can exist, and whether every King of the Hill match uses these yards are not in the game files.

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
