---
title: "Saburtulo"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Saburtulo King of the Hill map, added with its Season 2 zone and warm-up data: a 550 m zone with four placements."
---

# Saburtulo

| Saburtulo | |
|---|---|
| **General** | |
| Map area | About 16.3 km square (minimap bounds) |
| Modes | King of the Hill |
| **Zones** | |
| Control Zone | 550 m across, 150 m tall |
| Hot Zone | 85 m across, 150 m tall |
| Zone placements | 4 |
| Zone regions | Not in the data |
| Internal name | Server browser Moscow_KOTH_01; zone config Russia; minimap folder Russia |
{: .wiki-infobox }

Saburtulo is a King of the Hill map with a 550 m Control Zone and four possible zone placements. Its zone configuration, shader warm-up list and sight-blocker data were all added in Season 2. The data does not include a list of named zone regions for it, and it does not describe its streets, buildings or spawn points.

## Overview

Saburtulo is played in [King of the Hill](king-of-the-hill.md) under one server browser entry. The data ties it to the Moscow entry by name and folder only (an inference from the names, not checked in game). Its zone configuration is stored under the Russia files. Some data entries spell the placement names with "Sabartulo", which refers to the same placement set.

## Modes played here

- [King of the Hill](king-of-the-hill.md).

## Zones and objectives

The Control Zone is 550 m across and 150 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The zone has four placements. Hospital has weight 1, so it is the only placement drawn at random. Bazaar, River and Hillside have weight 0, so they are used only when the server rotation names them.

| Placement | Weight |
|---|---|
| Hospital | 1 |
| Bazaar | 0 |
| River | 0 |
| Hillside | 0 |

- **Zone regions.** The data does not include a region list for this map, so where the zone can sit beyond these four placements is not known.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#saburtulo).

## Season 2 changes

- The Russia zone configuration was added in Season 2. It is 550 m across with an 85 m Hot Zone, and it uses the standard 25-second move delay.
- A shader warm-up list for this map was added in Season 2. It lists 1,132 graphics pipeline states and 74 compute pipeline states. These lists are technical caches and do not change play.
- Sight-blocker map data was added for this map. The data does not say what sight blockers do in play.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Maps](maps.md)

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [UI data (minimap bounds)](../../content/Wardogs_UI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Round 40 modes, AI and other evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md): Moscow name link (inference from names and folders)
