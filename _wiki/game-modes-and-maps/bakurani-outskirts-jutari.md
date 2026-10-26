---
title: "Bakurani Outskirts - Jutari"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Sniper Showdown map named Bakurani Outskirts - Jutari: a 350 m zone with a fixed spot, a 75 m Hot Zone and a faster Hot Zone speed."
---

# Bakurani Outskirts - Jutari

| Bakurani Outskirts - Jutari | |
|---|---|
| **General** | |
| Map area | Shares the Bakurani world: about 16.3 km square (minimap bounds), with buildings over about 7.8 km by 7.7 km |
| Modes | Sniper Showdown |
| **Zones** | |
| Control Zone | 350 m across, 170 m tall |
| Hot Zone | 75 m across, 170 m tall |
| Zone placements | None, one fixed spot |
| Zone regions | Not in the data |
| Internal name | Server browser Bakurani_SniperShowdown_01; Sniper Showdown zone config Bakurani |
{: .wiki-infobox }

Bakurani Outskirts - Jutari is the Sniper Showdown map with a Bakurani name. Its Control Zone is 350 m across, smaller than the King of the Hill zones, and it has a single fixed spot rather than alternative placements. Its Hot Zone moves faster than the King of the Hill Hot Zones, with a default speed of 1.5.

## Overview

The server browser lists this map as a Sniper Showdown entry, with the Bakurani loading screen art. The data links it to the Sniper Showdown zone configuration named Bakurani by name. The data does not describe its terrain, buildings or sniper positions.

## Modes played here

- [Sniper Showdown](sniper-showdown.md).

## Zones and objectives

The Control Zone is 350 m across and 170 m tall, with a 75 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md) and [Sniper Showdown](sniper-showdown.md).

- **Hot Zone movement.** The data sets the first move and the delay between moves to 0 seconds. The data gives no delay between moves, so no timer holds the zone back; how often it moves in play was not measured.
- **Speed.** The default move speed is 1.5. The speed table runs from 1.25 to 3.0, which is faster than the 0.75 to 2.0 table on the King of the Hill maps.
- **Placements.** There are no alternative placements. The zone is always in the same spot.
- **Zone regions.** The data has no region list for this zone. The Sniper Showdown zone placed in the Bakurani world has an empty region slot, and the Bakurani region list belongs to the King of the Hill zone only.
- **Where it sits.** The fixed spot is inside the same world as [Bakurani](bakurani.md), about 400 m east of the edge of the area that Bakurani's zone regions cover (read from the placed zone object; the data gives the map no separate size).

## Placed objects

This entry has no objects of its own. Its zone sits in the Bakurani map file, so the objects around it are Bakurani's. Taking an area of 850 m across, centred on the fixed zone spot (the zone's 350 m width plus 500 m on every side, the same margin the other map articles use), the file places the following. The counts were read from the game files, not checked in play.

| Object | Count in that area |
|---|---:|
| Doors you can open (a garage door counts once) | 31 |
| Ladders | 9 |
| Breakable windows | 270 |
| Destructible buildings | 37 |
| Pre-placed barbed wire | 16 |

The area holds no Hot Zone Magnet towers, no vendors, no deployment boards and no water. For what the objects are, see [Bakurani](bakurani.md#placed-objects).

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#bakurani-outskirts---jutari).

## Season 2 changes

- Two more Sniper Showdown layouts were added in Season 2, for North America and Russia. They have no display name in the data, so they are not described on their own page. See [Maps](maps.md).
- The Season 2 notes list no change to this map's zone.

## See also

- [Sniper Showdown](sniper-showdown.md)
- [Control Zone](control-zone.md)
- [Bakurani](bakurani.md)
- [Maps](maps.md)

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 40 modes, AI and other evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md): Hot Zone movement state machine (Sniper Showdown configs)
