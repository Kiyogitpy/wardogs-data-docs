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
| **Zones** | |
| Control Zone | 550 m across, 150 m tall |
| Hot Zone | 85 m across, 150 m tall |
| Zone placements | 4 |
| Zone regions | 55 |
| Internal name | Server browser Madrid_KOTH_01; zone config Europe; region config Europe |
{: .wiki-infobox }

Ozeti is a King of the Hill map with a 550 m Control Zone and four possible zone placements. It has 55 named zone regions, almost all with weight 1. The data does not describe its streets, buildings or spawn points.

## Overview

Ozeti is played in [King of the Hill](king-of-the-hill.md) under one server browser entry. The data ties it to the Madrid entry by name, and its zone configuration and regions are stored under the Europe files. The name link is not confirmed in game.

## Modes played here

- [King of the Hill](king-of-the-hill.md).

## Zones and objectives

The Control Zone is 550 m across and 150 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone moves every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The zone has four placements. Default, Church and River each have weight 1. Farmland has weight 0, so by weight alone it is never picked.

| Placement | Weight |
|---|---|
| Default | 1 |
| Church | 1 |
| River | 1 |
| Farmland | 0 |

- **Zone regions.** The data lists 55 named regions. Of these, 54 have weight 1 and one, Tower 2, has weight 0. Regions are named for towers and points of interest such as the stadium, pool, church top, lumberyard and apartments. Every non-zero region is equally likely under the data, because no other weight values appear.

## Season 2 changes

- The shader warm-up list for this map was updated. Graphics pipeline states went from 1,639 to 1,053, and compute pipeline states from 6 to 83. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The data does not say what sight blockers do in play.
- The Season 2 notes list no change to this map's Control Zone.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Maps](maps.md)

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
