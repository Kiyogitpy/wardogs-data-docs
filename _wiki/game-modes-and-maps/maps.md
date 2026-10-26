---
title: "Maps"
parent: "Game Modes & Maps"
group: "Maps"
description: "Every map the data names, the modes that use it, and its zone layout. Vehicle spawns are summarised; buildings are not described."
---

# Maps

| Maps | |
|---|---|
| Maps named in the data | Bakurani, Ozeti, Zestafona, Saburtulo, Bakurani Outskirts - Jutari, and Kenya (its zone layout is labelled Africa in the data) |
| Entries with no zone data | Four King of the Hill entries (Berlin, Paris, Mindori and Tevza) and Tank Town |
| Training gyms | Two test areas, not playable modes |
{: .wiki-infobox }

Wardogs has four main King of the Hill maps, a fifth King of the Hill map (Kenya, whose zone layout is labelled Africa in the data) and a Sniper Showdown map. The first five are named in the server browser by the name players see. The sources do not describe level layouts or buildings, so the articles here cover only what the data records about each map: zones, regions and, for the four main maps, vehicle and infantry spawn areas.

## Layouts

Every zone layout in the data, including the unnamed Africa, Sniper Showdown and server browser layouts, is described on [Zone Layouts](zone-layouts.md).

## Individual maps

- [Bakurani](bakurani.md), King of the Hill
- [Ozeti](ozeti.md), King of the Hill
- [Zestafona](zestafona.md), King of the Hill
- [Saburtulo](saburtulo.md), King of the Hill
- [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md), Sniper Showdown
- [Kenya (Africa layout)](unnamed-africa-layout.md), King of the Hill map

## Overview

| Map | Modes | Control Zone | Named zone regions | Notes |
|---|---|---|---|---|
| Bakurani | King of the Hill | 500 m, 3 placements | 60 | Two King of the Hill entries use this name. |
| Ozeti | King of the Hill | 550 m, 4 placements | 55 | |
| Zestafona | King of the Hill | 500 m, 4 placements | 56 | Its Hot Zone is 850 m tall. |
| Saburtulo | King of the Hill | 550 m, 4 placements | Not in the data | Its shader warm-up list was added in Season 2. |
| Bakurani Outskirts - Jutari | Sniper Showdown | 350 m, fixed spot | Not in the data | Sniper Showdown's own map entry. |
| [Kenya (Africa layout)](unnamed-africa-layout.md) | King of the Hill | 550 m, 4 placements | Not in the data | Added in Season 2. The zone set is labelled Africa in the data. |
| Berlin, Paris, Mindori and Tevza | King of the Hill | Not in the data | Not in the data | Listed in the server browser. The game files hold no zone data for them, so their layouts cannot be stated. |
| Detroit and Moscow Sniper Showdown layouts | Sniper Showdown | 350 m, fixed spot | Not in the data | Match the Detroit and Moscow Sniper Showdown entries by name only (not confirmed in game). |
| Deathmatch | Deathmatch | Not applicable | Not applicable | Listed in the server browser with no map name. |
| Tank Town | Tank Town | Not applicable | Not applicable | Uses the King of the Hill rules, with no map or zone data of its own. |

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

### Kenya (Africa layout)

The Kenya map, added in Season 2. Its zone set is labelled Africa in the data. Its Control Zone is 550 m across and 150 m tall. Four placements exist: a default with weight 1, and North, East and West with weight 0. It is covered in full on [Kenya (Africa layout)](unnamed-africa-layout.md).

### Vehicle spawns on the main maps

Each King of the Hill match uses three spawn areas, one per side, and each area has a vehicle deployment board, several vehicle yards and an infantry spawn area. The counts below are per server browser entry; the data does not say how many vehicles of each kind a yard holds.

| Map (entry) | Deployment boards | Vehicle yards (ground / air / light) | Vehicle slots |
|---|---:|---|---:|
| Bakurani (first entry) | 3 | 13 (7 / 3 / 3) | 67 |
| Bakurani (second entry) | 3 | 12 (6 / 3 / 3) | 72 |
| Ozeti | 3 | 13 (7 / 3 / 3) | 74 |
| Zestafona | 3 | 12 (7 / 2 / 3), plus one extra air yard | 61, plus 7 |
| Saburtulo | 3 | 11 (6 / 2 / 3), plus one extra air yard | 68, plus 9 |
| Kenya | Not in the data | Not in the data | Not in the data |

Each deployment board looks after one vehicle, the side's M113 APC SV that players deploy onto. The APC is not on the map from the start: the board puts it out only once one side has reached a score of 20, and until then the board reads "Inactive Vehicle: Min Required Game Score: 20". When the APC is destroyed the board counts down before it returns: 300 s normally, or 60 s if the board's side is losing, meaning the best other side is ahead of it by 15 score points or more at the moment the APC is lost. The board shows the time left while it counts, and the countdown applies to this APC only; the data gives no respawn time for the vehicles in the yards. Once a player has deployed onto the APC, that player cannot deploy from the same board again for 600 s. The board's reasons for refusing, shown one at a time with the first on this list that applies, are: respawning, score required, no vehicle, radar destroyed, not in the control zone, vehicle moving and no free seat. The "vehicle moving" message looks like a warning only: the deploy check still lets the player through (read from the game's code, not seen in play). The vehicle counts as moving at 10 km/h or more. The radar is flagged destroyed when its health reaches zero and is back once it is repaired to 55 percent of its maximum. These values are the game's built-in defaults and the board Blueprint, not map file settings.

The Berlin, Paris and Mindori entries also have spawn areas of the same kind; the Tevza entry names three spawn areas that hold no vehicle or infantry spawn data in the game files, and the three spawn points in the map file that carry no layer belong to the co-operative missions, not to Tevza. The details are on the [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md) data page.

### Other entries

The server browser table has four further King of the Hill entries with no display name, and one Sniper Showdown layout (for North America) and one for Russia that are not matched to a name. The sources do not say where those are, so they are not described further.

## Lighting presets

The light on every map is a fixed setting. There is no day and night cycle and no weather that changes during a match, and nothing in the game files places a moving sun, a moon or storms on the main maps. Each map has a stored default, and a server owner can name a different preset for each map entry in the server rotation, so the same map can be played in different light. The example server file rotates six of the nine presets (all except sunrise, sunset and rain). Rain exists only in the heavy rain preset, which also removes direct sunlight; the example server file does not use it.

| Name servers use | What it looks like | Sun height | Fog thickness (clear morning = 1) |
|---|---|---:|---:|
| DayEndClear | Sunset, clear, low orange sun | 12.8 degrees | 0.45 |
| DayEarlyClear | Morning, clear, low sun | 10.1 degrees | 1 |
| DayLateClear | Late afternoon, clear, low sun | 20.2 degrees | 2 |
| DayStartClear | Sunrise, clear, sun near the horizon | 5.1 degrees | 3.5 |
| DayClear | Midday, clear, high sun | 43.8 degrees | 4.5 |
| DayLateGray | Late afternoon, overcast, no direct sun | 32.9 degrees | 7.5 |
| DayLateGrayFog | Late afternoon, overcast, with a low fog layer | 32.9 degrees | 7.5 |
| DayEarlyFog | Morning, foggy | 10.1 degrees | 30 |
| DayLateRain | Late afternoon, heavy rain, no direct sun | 32.9 degrees | 1.5e+02 |

The last column compares the fog density in each preset with the clear morning preset. The ratio is what matters; how far you can see in each is not stated in the files. The foggy morning is the thickest of the six in the example rotation. A low sun is hard to look into and throws long shadows, but the files do not say which way is north, so compass directions are not given here. Which preset a server runs is the server owner's choice.

## Season 2 changes

- Season 2 added a shader warm-up list for the Saburtulo map. The Ozeti, Zestafona and Bakurani lists were updated. These lists are technical caches that prepare graphics before a match, not gameplay changes.
- Season 2 added sight-blocker map data for four main maps (matched by region: Ozeti, Zestafona, Saburtulo and Bakurani). The data does not say what sight-blockers do in play.
- Season 2 added the Africa and Russia zone sets and two Sniper Showdown zone layouts, described on [Control Zone](control-zone.md).

## Training gyms

The data includes two test areas that are not playable modes. A minimal test area holds a grid of zone cells, and a water test area has a fluid simulation and a height grid. They are used for testing, and the data does not describe any rules for them.

## Rules and objectives

The game's level files exist for the four main worlds and the test gym. The data lists the spawn areas for vehicles and infantry (see the Vehicle spawns section of each map article, and [Zone Layouts](zone-layouts.md)), but the buildings inside the maps are not described here. The level cells that were checked hold only art and ambience, with no player starts, spawn volumes, zones or bases. Those come from the separate game mode data, so the zone, region and spawn data above is all the game files hold on map layout.

The playable areas are about 8.5 by 7.8 km on the Europe world, 11 by 11 km on Kavkazi, 10.5 by 9.2 km on North America and 13.2 by 13.2 km on Russia. The map data measures in centimetres (one world unit is 1 cm). On Europe, Kavkazi and North America the kill height is 1,500 m below the map's zero level; the data gives no kill height for Russia.

The gym range has a moving target, which slides on a set path and takes 15 to 25 seconds to cross. See [Shooting Range](shooting-range.md).

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Sniper Showdown](sniper-showdown.md)
- [Deathmatch](deathmatch.md)
- [Boundaries and Safe Zones](boundaries-and-safe-zones.md), the play area edge and the spawn safe zones

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [Light and weather data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-light-weather.json)
- [Round 70 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round70-maps-matchstart.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
