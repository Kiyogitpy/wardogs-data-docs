---
title: "Kenya (Africa layout)"
parent: "Game Modes & Maps"
group: "Maps"
description: "The Kenya King of the Hill map, added in Season 2: a 550 m Control Zone with four placements, whose zone set is labelled Africa."
---

# Kenya (Africa layout)

| Kenya | |
|---|---|
| **General** | |
| Map | Kenya |
| Map area | Not in the data (no Africa map, minimap or map layer in the game files) |
| Modes | King of the Hill |
| **Zones** | |
| Control Zone | 550 m across, 150 m tall |
| Hot Zone | 85 m across, 150 m tall |
| Zone placements | 4 |
| Zone regions | Not in the data |
| Internal name | Zone config Africa; King of the Hill entry Kenya_KOTH_01 |
{: .wiki-infobox }

The Kenya map is a King of the Hill map added in Season 2. Its zone set is labelled "Africa", and its placements are named after a region called Kenya, so this article uses the map name.

## Overview

The game has one zone set labelled Africa, added in Season 2. It belongs to the Kenya King of the Hill entry, so the zone set and the map share the name Kenya. The game gives the layout and the map name, and nothing about the streets, buildings or spawn points. The Kenya entry turns on a single map layer called Kenya, but the game holds no map layer, world map or minimap named Kenya or Africa (checked across all map layers, world folders and minimap assets), so the size of the Kenya map and any list of zone regions cannot be stated. No vehicle deployment board, yard or infantry spawn area was found for it in the game.

## Modes played here

- King of the Hill. The Kenya entry uses the King of the Hill rules: three teams, the score limit of the mode and the Control Zone.

## Zones and objectives

The Control Zone is 550 m across and 150 m tall, with an 85 m Hot Zone in its centre. For how capture works, see [Control Zone](control-zone.md).

- **Hot Zone movement.** The Hot Zone is placed at the start and then moves about every 25 seconds, with a default speed of 1.0 and a speed table from 0.75 to 2.0.
- **Placements.** The default placement has weight 1. North, East and West have weight 0, so they are never drawn at random. The server rotation can name one of them for a match.

| Placement | Weight |
|---|---|
| Default | 1 |
| North | 0 |
| East | 0 |
| West | 0 |

- **Zone regions.** The game has no region list for this zone set.

## Layouts

The zone layout for this map is described in full on [Zone Layouts](zone-layouts.md#kenya-africa-layout).

## Season 2 changes

- The zone set labelled Africa was added in Season 2. Its Control Zone and Hot Zone sizes match the Russia zone set used by [Saburtulo](saburtulo.md).

## See also

- [Maps](maps.md)
- [Zone Layouts](zone-layouts.md)
- [Control Zone](control-zone.md)
- [King of the Hill](king-of-the-hill.md)

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
