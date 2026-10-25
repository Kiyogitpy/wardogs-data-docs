---
title: "Zone Layouts"
parent: "Game Modes & Maps"
group: "Maps"
description: "Every Control Zone layout in the data: the named maps, the unnamed Africa, Sniper Showdown and server browser layouts, and the test area. Zone sizes, placements and Hot Zone movement for each."
---

# Zone Layouts

| Zone Layouts | |
|---|---|
| **General** | |
| Zone configurations in the data | 9 |
| Linked to a named map | 5 (by name only) |
| Unnamed layouts | 3 (Africa and two Sniper Showdown layouts) |
| Test area | 1 |
| **Zones** | |
| Control Zone | 350 to 550 m across |
| Hot Zone | 75 to 85 m across |
| Shape | Cylinder. Two Africa and Russia alternatives are ellipses. |
{: .wiki-infobox }

A zone layout is one Control Zone configuration: the size of the zone and its Hot Zone, how the Hot Zone moves, and which alternative spots the zone can appear in. King of the Hill and Sniper Showdown both play on these layouts. Five layouts are linked by name to a map in the server browser. Three have no display name, and the data does not say which server browser entry, if any, uses them. Those links are by name only and are not confirmed in game.

## Overview

| Layout | Mode | Control Zone | Hot Zone | Placements | Hot Zone timing |
|---|---|---|---|---|---|
| [Bakurani](bakurani.md) | King of the Hill | 500 m across, 170 m tall | 85 m across, 170 m tall | 3 | Moves every 25 s |
| [Ozeti](ozeti.md) | King of the Hill | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Moves every 25 s |
| [Zestafona](zestafona.md) | King of the Hill | 500 m across, 500 m tall | 85 m across, 850 m tall | 4 | Moves every 25 s |
| [Saburtulo](saburtulo.md) | King of the Hill | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Moves every 25 s |
| [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md) | Sniper Showdown | 350 m across, 170 m tall | 75 m across, 170 m tall | None (one spot) | 0 s before the first move and between moves |
| [Unnamed layout (data name: Africa)](#unnamed-layout-data-name-africa) | Not yet known | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Moves every 25 s |
| [Unnamed layout (data name: Sniper Showdown North America)](#unnamed-layout-data-name-sniper-showdown-north-america) | Sniper Showdown | 350 m across, 170 m tall | 75 m across, 170 m tall | None (one spot) | 0 s before the first move and between moves |
| [Unnamed layout (data name: Sniper Showdown Russia)](#unnamed-layout-data-name-sniper-showdown-russia) | Sniper Showdown | 350 m across, 170 m tall | 75 m across, 170 m tall | None (one spot) | 0 s before the first move and between moves |
| [Four unnamed King of the Hill entries](#unnamed-king-of-the-hill-entries-with-no-zone-data) | King of the Hill | No zone data | No zone data | No zone data | No zone data |
| [Tank Town](#tank-town-server-browser-entry) | Tank Town | No zone data | No zone data | No zone data | No zone data |
| [Minimal test area](#minimal-test-area-data-name-gym_minimal) | Test area, not a mode | 50 m across, 25 m tall | None (shape only) | None | Moves every 25 s, minimum 7.5 m |

## Rules and objectives

- **Placements.** A layout with alternatives has a selection weight on each placement. The data suggests one placement is picked by weight at random for each match, but the code path is not confirmed. A placement with weight 0 is never picked by weight alone. On Bakurani, the default placement has weight 2 and the other two have weight 1, so the default is twice as likely if weights decide.
- **Region sets.** Three layouts also have a list of named zone regions: Bakurani (60), Ozeti (55) and Zestafona (56). Each region has a default weight, and a weight of 0 means it is not picked by default. How the region list relates to the placements is not confirmed. Saburtulo, Africa and the Sniper Showdown layouts have no region list in the data.
- **Hot Zone movement.** On the King of the Hill layouts the Hot Zone moves every 25 seconds. The default speed is 1.0 and the speed table runs from 0.75 to 2.0. On the Sniper Showdown layouts the first move and the delay between moves are both 0 seconds, the default speed is 1.5, and the speed table runs from 1.25 to 3.0. How often the Sniper Showdown zone moves in play is not confirmed.
- **Hot Zone size.** The effective inner size of the Hot Zone is 95 percent of its listed extent on every layout except the test area. This is inferred from the field name.

## Named layouts

### Bakurani

- **Mode:** King of the Hill, in both server browser entries for Bakurani.
- **Control Zone:** 500 m across, 170 m tall. **Hot Zone:** 85 m across, 170 m tall.
- **Placements:** Default (weight 2), Farmland (weight 1), Lumberyard (weight 1). The alternatives match the base size.
- **Region set:** 60 named regions. Seven are towers with weight 0. Most other regions have weight 1, and a few have weight 5, including Sunflowers House, West Forest Pylon and Hillside Top. The region labels are sites such as sunflower fields, forest, hills, farmland, water and urban areas. The data does not confirm that players see these labels.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Internal name:** zone config Bakurani, the layout for the Bakurani King of the Hill entries (Bakurani_KOTH_01 and Bakurani_KOTH_02). The region set and the world are stored under the Kavkazi name.

### Ozeti

- **Mode:** King of the Hill.
- **Control Zone:** 550 m across, 150 m tall. **Hot Zone:** 85 m across, 150 m tall.
- **Placements:** Default (weight 1), Church (weight 1), River (weight 1), Farmland (weight 0).
- **Region set:** 55 named regions, 54 with weight 1 and one tower with weight 0. Labels include the stadium, pool, church top, lumberyard, apartments, residential blocks, farms, forest blocks and hillside churches.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Internal name:** zone config Europe, server browser Madrid_KOTH_01, world Europe. The name link to Ozeti is not confirmed in game.

### Zestafona

- **Mode:** King of the Hill.
- **Control Zone:** 500 m across, 500 m tall. **Hot Zone:** 85 m across, 850 m tall. The Hot Zone is much taller than the zone around it. The data does not say whether that is intended.
- **Placements:** Default (weight 1), Water Treatment (weight 1), Houses (weight 1), Small Factory (weight 0).
- **Region set:** 56 named regions, 53 with weight 1 and three towers with weight 0. Labels include large factories, shipping and export yards, a scrap import area, train tracks and two train sheds.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Internal name:** zone config NorthAmerica, server browser Detroit_KOTH_01, world NorthAmerica. The name link to Zestafona is not confirmed in game.

### Saburtulo

- **Mode:** King of the Hill.
- **Control Zone:** 550 m across, 150 m tall. **Hot Zone:** 85 m across, 150 m tall.
- **Placements:** Hospital (weight 1), Bazaar, River and Hillside (weight 0 each). The data spells the placement names with "Sabartulo".
- **Region set:** none in the data.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Internal name:** zone config Russia, server browser Moscow_KOTH_01, world Russia. Added in Season 2. The name link to Saburtulo is not confirmed in game.

### Bakurani Outskirts - Jutari

- **Mode:** Sniper Showdown.
- **Control Zone:** 350 m across, 170 m tall. **Hot Zone:** 75 m across, 170 m tall.
- **Placements:** none. The zone is always in one spot.
- **Region set:** none in the data.
- **Hot Zone movement:** first move and move delay both 0 s, default speed 1.5, speed table 1.25 to 3.0.
- **Internal name:** Sniper Showdown zone config Bakurani, server browser Bakurani_SniperShowdown_01. The name link is not confirmed in game.

## Unnamed layouts

These layouts have no display name in the data. The title gives the data name, which is a label in the data and not a name players see.

### Unnamed layout (data name: Africa)

- **Mode:** not yet known. The layout uses the Control Zone rules, which King of the Hill and Sniper Showdown both use, but the data does not say which entry uses it.
- **Control Zone:** 550 m across, 150 m tall. **Hot Zone:** 85 m across, 150 m tall.
- **Placements:** Default (weight 1). North, East and West (weight 0 each).
- **Alternatives:** each alternative is a 500 m ellipse, 500 m tall, with an 85 m Hot Zone that is 500 m tall. That does not match the base layout.
- **Region set:** none in the data.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Season 2:** added.
- **Internal name:** zone config Africa, with placements named after a region called Kenya.

### Unnamed layout (data name: Sniper Showdown North America)

- **Mode:** Sniper Showdown, from the config name. No server browser entry uses it in the data.
- **Control Zone:** 350 m across, 170 m tall. **Hot Zone:** 75 m across, 170 m tall.
- **Placements:** none. **Region set:** none.
- **Hot Zone movement:** first move and move delay both 0 s, default speed 1.5, speed table 1.25 to 3.0.
- **Season 2:** added. Its map is not named in the data.
- **Internal name:** Sniper Showdown zone config NorthAmerica.

### Unnamed layout (data name: Sniper Showdown Russia)

- **Mode:** Sniper Showdown, from the config name. No server browser entry uses it in the data.
- **Control Zone:** 350 m across, 170 m tall. **Hot Zone:** 75 m across, 170 m tall.
- **Placements:** none. **Region set:** none.
- **Hot Zone movement:** the same as the North America Sniper Showdown layout.
- **Season 2:** added. Its map is not named in the data.
- **Internal name:** Sniper Showdown zone config Russia.

## Server browser entries with no zone data

The server browser lists four King of the Hill entries and one Tank Town entry with no display name or zone configuration that the data can tie them to. The data does not say which zone layout, if any, they use.

### Unnamed King of the Hill entries with no zone data

These four entries are listed as King of the Hill with no display name:

- **Mindori** (data name: Mindori_KOTH_01)
- **Tevza** (data name: Tevza_KOTH_01)
- **Berlin** (data name: Berlin_KOTH_01)
- **Paris** (data name: Paris_KOTH_01)

The zone data contains no configuration with these names. Two region labels in the Bakurani region set begin with "Mindori", but that does not show that the Mindori entry uses the Bakurani layout. Their zone sizes, placements and region sets are not known.

### Tank Town (server browser entry)

The server browser lists Tank Town as a mode with the display name Tank Town and no map image. The zone data has no layout for it, and the data does not say whether this mode uses a Control Zone.

## Test area

### Minimal test area (data name: Gym_Minimal)

- **Use:** a test area, not a playable mode. See [Maps](maps.md) for the test areas.
- **Control Zone:** 50 m across, 25 m tall. No Hot Zone size is given in the zone data.
- **Hot Zone movement:** every 25 s, default speed 1.0, with a minimum move distance of 7.5 m. The inner radius is the full extent (100 percent) rather than 95 percent.
- **Placements:** none. **Region set:** none.

## Season 2 changes

- Four zone configurations were added: Africa, Russia, Sniper Showdown North America and Sniper Showdown Russia. The zone configurations went from 5 to 9.
- The Africa and Russia layouts use the 550 m Control Zone and 85 m Hot Zone sizes described above, with four alternatives each.
- The two new Sniper Showdown layouts are 350 m across, with 75 m Hot Zones, and use the same speed table as the Sniper Showdown Bakurani layout.
- No Season 2 change is recorded for the existing Bakurani, Ozeti or Zestafona layouts. Saburtulo's zone layout was added in Season 2.

## See also

- [Maps](maps.md)
- [Control Zone](control-zone.md)
- [King of the Hill](king-of-the-hill.md)
- [Sniper Showdown](sniper-showdown.md)

## Sources

- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
