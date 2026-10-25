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
| **Zones** | |
| Control Zone | 500 m across, 500 m tall |
| Hot Zone | 85 m across, 850 m tall |
| Zone placements | 4 |
| Zone regions | 56 |
| Internal name | Server browser Detroit_KOTH_01; zone config NorthAmerica; region config NorthAmerica |
{: .wiki-infobox }

Zestafona is a King of the Hill map whose Control Zone is 500 m across and 500 m tall. Its Hot Zone is 85 m across but 850 m tall, much taller than the zone around it. It has four placements and 56 named zone regions, mostly industrial sites and rail sheds.

## Overview

Zestafona is played in [King of the Hill](king-of-the-hill.md) under one server browser entry. The data ties it to the Detroit entry by name, and its zone and region files are stored under the North America folder. The name link is not confirmed in game.

## Modes played here

- [King of the Hill](king-of-the-hill.md).

## Zones and objectives

The Control Zone is 500 m across and 500 m tall. The Hot Zone is 85 m across and 850 m tall. The data does not say whether that height is intended, and it was not checked in game. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone moves every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The zone has four placements. Default, Water Treatment and Houses each have weight 1. Small Factory has weight 0, so by weight alone it is never picked.

| Placement | Weight |
|---|---|
| Default | 1 |
| Water Treatment | 1 |
| Houses | 1 |
| Small Factory | 0 |

- **Zone regions.** The data lists 56 named regions. Of these, 53 have weight 1, and the three towers have weight 0. Named sites include large factories, shipping and export yards, a scrap import area, train tracks and two train sheds. Every non-zero region is equally likely under the data.

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

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
