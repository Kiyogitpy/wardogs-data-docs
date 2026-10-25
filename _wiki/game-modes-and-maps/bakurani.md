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
| **Zones** | |
| Control Zone | 500 m across, 170 m tall |
| Hot Zone | 85 m across, 170 m tall |
| Zone placements | 3 |
| Zone regions | 60 |
| Internal name | Server browser Bakurani_KOTH_01 and Bakurani_KOTH_02; zone config Bakurani; region config and minimap folder Kavkazi |
{: .wiki-infobox }

Bakurani is the first King of the Hill map in the server browser, and it is the one with the most zone data. It has three alternative zone placements and 60 named zone regions, so the zone can appear in several parts of the map. The data does not describe its streets, buildings or spawn points.

## Overview

Bakurani is played in [King of the Hill](king-of-the-hill.md). The server browser lists it twice, as Bakurani_KOTH_01 and Bakurani_KOTH_02, and both use the Bakurani name and loading screen art. The data does not say how the two entries differ. The Bakurani zone configuration is tied to these entries by name only, which is not confirmed in game.

## Modes played here

- [King of the Hill](king-of-the-hill.md), in both server browser entries.
- Not used for Sniper Showdown. The Sniper Showdown map with a Bakurani name is a separate entry, [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md).

## Zones and objectives

The Control Zone is 500 m across and 170 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone moves every 25 seconds. Its default speed is 1.0, and the speed table runs from 0.75 to 2.0.
- **Placements.** The zone has three placements. The default has weight 2, and Farmland and Lumberyard each have weight 1. If the weights decide the pick, the default is twice as likely as either alternative. The data suggests this, but the code path is not confirmed.

| Placement | Weight |
|---|---|
| Default | 2 |
| Farmland | 1 |
| Lumberyard | 1 |

- **Zone regions.** The data lists 60 named regions. Seven are towers with weight 0, so they are never picked by default weight. Most other regions have weight 1. A few have weight 5, including SUNFLOWERS HOUSE, WEST FOREST PYLON and HILLSIDE TOP, which makes them much more likely. How a region is chosen is not confirmed in the data.

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

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
