---
title: "Maps"
parent: "Game Modes & Maps"
group: "Maps"
description: "Every map the data names, the modes that use it, and its zone layout. Level layouts, spawns and buildings are not in the data."
---

# Maps

| Maps | |
|---|---|
| Maps named in the data | Bakurani, Ozeti, Zestafona, Saburtulo, Bakurani Outskirts - Jutari, plus one unnamed layout labelled Africa in the data |
| Map entries with no display name | Four King of the Hill entries, and the North America and Russia Sniper Showdown layouts |
| Training gyms | Two test areas, not playable modes |
{: .wiki-infobox }

Wardogs has four main King of the Hill maps, a Sniper Showdown map and one unnamed layout whose data is labelled Africa. The first five are named in the server browser by the name players see. The sources do not describe level layouts, spawn points or buildings, so the articles here cover only what the data records about each map.

## Individual maps

- [Bakurani](bakurani.md), King of the Hill
- [Ozeti](ozeti.md), King of the Hill
- [Zestafona](zestafona.md), King of the Hill
- [Saburtulo](saburtulo.md), King of the Hill
- [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md), Sniper Showdown
- [Unnamed Africa layout](unnamed-africa-layout.md), zone set with no server browser name

## Overview

| Map | Modes | Control Zone | Named zone regions | Notes |
|---|---|---|---|---|
| Bakurani | King of the Hill | 500 m, 3 placements | 60 | Two King of the Hill entries use this name. |
| Ozeti | King of the Hill | 550 m, 4 placements | 55 | |
| Zestafona | King of the Hill | 500 m, 4 placements | 56 | Its Hot Zone is 850 m tall. |
| Saburtulo | King of the Hill | 550 m, 4 placements | Not in the data | Its shader warm-up list was added in Season 2. |
| Bakurani Outskirts - Jutari | Sniper Showdown | 350 m, fixed spot | Not in the data | Sniper Showdown's own map entry. |
| [Unnamed Africa layout](unnamed-africa-layout.md) | Control Zone set | 550 m, 4 placements | Not in the data | Added in Season 2. Its display name is not in the data, and the Africa label is the data's, not a map name. |
| Four more entries | King of the Hill | Not in the data | Not in the data | The server browser lists them without display names. Their names are not yet known. |
| Sniper Showdown layouts (North America and Russia) | Sniper Showdown | 350 m, fixed spot | Not in the data | Not matched to a display name in the sources. |
| Deathmatch | Deathmatch | Not applicable | Not applicable | Listed in the server browser with no map name. |

Zone sizes and placement weights are on [Control Zone](control-zone.md).

## Map details

### Bakurani

The first King of the Hill map. The server browser lists it twice. Its Control Zone is 500 m across and 170 m tall, with an 85 m Hot Zone. Three placements exist: a default placement with weight 2, and Farmland and Lumberyard placements with weight 1 each. Its zone regions include a few that carry weight 5, such as Sunflowers House, West Forest Pylon and Hillside Top, so the zone is more likely to appear there.

### Ozeti

A King of the Hill map. Its Control Zone is 550 m across and 150 m tall, with four placements. The Farmland placement has weight 0, so it is never picked by weight alone. Its 55 zone regions all use weight 0 or 1.

### Zestafona

A King of the Hill map. Its Control Zone is 500 m across and 500 m tall. Its Hot Zone is 85 m across and 850 m tall, which is much taller than the zone around it. The data does not say whether that is intended. Its Small Factory placement has weight 0. Its 56 zone regions use weight 0 or 1.

### Saburtulo

A King of the Hill map. Its Control Zone is 550 m across and 150 m tall, with four placements. The Hospital placement is the only one with weight 1. Bazaar, River and Hillside have weight 0. The data does not include its zone region list.

### Bakurani Outskirts - Jutari

The Sniper Showdown map. Its zone is 350 m across and 170 m tall, with a 75 m Hot Zone and a fixed spot. See [Sniper Showdown](sniper-showdown.md).

### Unnamed Africa layout

A zone set (labelled Africa in the data) added in Season 2. Its Control Zone is 550 m across and 150 m tall. Four placements exist: a default with weight 1, and North, East and West with weight 0. The server browser table has no display name for this set, so it is listed here by its layout only.

### Other entries

The server browser table has four further King of the Hill entries with no display name, and one Sniper Showdown layout (for North America) and one for Russia that are not matched to a name. The sources do not say where those are, so they are not described further.

## Season 2 changes

- Season 2 added a shader warm-up list for the Saburtulo map. The Ozeti, Zestafona and Bakurani lists were updated. These lists are technical caches that prepare graphics before a match, not gameplay changes.
- Season 2 added sight-blocker map data for four main maps (matched by region: Ozeti, Zestafona, Saburtulo and Bakurani). The data does not say what sight-blockers do in play.
- Season 2 added the Africa and Russia zone sets and two Sniper Showdown zone layouts, described on [Control Zone](control-zone.md).

## Training gyms

The data includes two test areas that are not playable modes. A minimal test area holds a grid of zone cells, and a water test area has a fluid simulation and a height grid. They are used for testing, and the data does not describe any rules for them.

## Rules and objectives

Level layouts, spawn points, buildings and the places that count as zone cells are not in the data for any map. Anything a player sees on a map beyond the zone and region data is not yet known.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Sniper Showdown](sniper-showdown.md)
- [Deathmatch](deathmatch.md)

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
