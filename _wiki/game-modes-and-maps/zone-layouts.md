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
| Linked to a named map | 6 |
| Unnamed layouts | 2 (two Sniper Showdown layouts) |
| Test area | 1 |
| **Zones** | |
| Control Zone | 350 to 550 m across |
| Hot Zone | 75 to 85 m across |
| Shape | Cylinder. Two Africa and Russia alternatives are ellipses. |
{: .wiki-infobox }

A zone layout is one Control Zone configuration: the size of the zone and its Hot Zone, how the Hot Zone moves, and which alternative spots the zone can appear in. King of the Hill and Sniper Showdown both play on these layouts. Six layouts are linked to a map in the server browser. The Africa layout is the Kenya King of the Hill map. The Sniper Showdown layouts for North America and Russia match the Detroit and Moscow Sniper Showdown entries by name only, and the link from Saburtulo to Moscow is by name and folder only, so neither is confirmed in game.

## Overview

| Layout | Mode | Control Zone | Hot Zone | Placements | Hot Zone timing |
|---|---|---|---|---|---|
| [Bakurani](bakurani.md) | King of the Hill | 500 m across, 170 m tall | 85 m across, 170 m tall | 3 | Moves about every 25 s |
| [Ozeti](ozeti.md) | King of the Hill | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Moves about every 25 s |
| [Zestafona](zestafona.md) | King of the Hill | 500 m across, 500 m tall | 85 m across, 850 m tall | 4 | Moves about every 25 s |
| [Saburtulo](saburtulo.md) | King of the Hill | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Moves about every 25 s |
| [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md) | Sniper Showdown | 350 m across, 170 m tall | 75 m across, 170 m tall | None (one spot) | 0 s before the first move and between moves |
| [Kenya (Africa layout)](#kenya-africa-layout) | King of the Hill | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Moves about every 25 s |
| [Unnamed layout (data name: Sniper Showdown North America)](#unnamed-layout-data-name-sniper-showdown-north-america) | Sniper Showdown | 350 m across, 170 m tall | 75 m across, 170 m tall | None (one spot) | 0 s before the first move and between moves |
| [Unnamed layout (data name: Sniper Showdown Russia)](#unnamed-layout-data-name-sniper-showdown-russia) | Sniper Showdown | 350 m across, 170 m tall | 75 m across, 170 m tall | None (one spot) | 0 s before the first move and between moves |
| [Four unnamed King of the Hill entries](#unnamed-king-of-the-hill-entries-with-no-zone-data) | King of the Hill | No zone data | No zone data | No zone data | No zone data |
| [Tank Town](#tank-town-server-browser-entry) | Tank Town | No zone data | No zone data | No zone data | No zone data |
| [Minimal test area](#minimal-test-area-data-name-gym_minimal) | Test area, not a mode | 50 m across, 25 m tall | None (shape only) | None | Moves about every 25 s, minimum 7.5 m |

## Rules and objectives

- **Placements.** A layout with alternatives has a selection weight on each placement. The layout a match uses is chosen in this order. First, the server's map rotation can name the placement for that map, and a named placement is used even if its weight is 0. Second, if nothing is named, a server queue of placements can be used, one per map load. Third, a placement is drawn at random by weight, and a placement with weight 0 is never drawn this way. On Bakurani the default has weight 2 and the other two have weight 1, so with the random draw the default is twice as likely. The example server rotation lists every placement the same number of times, including the weight 0 ones.
- **Region sets.** Three layouts also have a list of named zone regions: Bakurani (60), Ozeti (55) and Zestafona (56). Each region has a weight, and the Hot Zone moves to a region drawn at random by weight. A region with weight 0 (the towers) is never drawn that way. The region just used gives away half its weight, so it is unlikely to come up again at once. Regions overlap in places, which does not affect the draw. Saburtulo, Africa and the Sniper Showdown layouts have no region list in the data.
- **Hot Zone movement.** On the King of the Hill layouts the Hot Zone is placed at once at the start and then moves about every 25 seconds (the data value; the timing in play is not confirmed). The default speed is 1.0 and the speed table runs from 0.75 to 2.0. On the Sniper Showdown layouts the first move and the delay between moves are both 0 seconds, the default speed is 1.5, and the speed table runs from 1.25 to 3.0. How often the Sniper Showdown zone moves in play is not confirmed.
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
- **Internal name:** zone config Europe, server browser Madrid_KOTH_01, world Europe. The example server rotation pairs Madrid with these placements.

### Zestafona

- **Mode:** King of the Hill.
- **Control Zone:** 500 m across, 500 m tall. **Hot Zone:** 85 m across, 850 m tall. The Hot Zone is much taller than the zone around it. The data does not say whether that is intended.
- **Placements:** Default (weight 1), Water Treatment (weight 1), Houses (weight 1), Small Factory (weight 0).
- **Region set:** 56 named regions, 53 with weight 1 and three towers with weight 0. Labels include large factories, shipping and export yards, a scrap import area, train tracks and two train sheds.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Internal name:** zone config NorthAmerica, server browser Detroit_KOTH_01, world NorthAmerica. The example server rotation pairs Detroit with these placements.

### Saburtulo

- **Mode:** King of the Hill.
- **Control Zone:** 550 m across, 150 m tall. **Hot Zone:** 85 m across, 150 m tall.
- **Placements:** Hospital (weight 1), Bazaar, River and Hillside (weight 0 each). The data spells the placement names with "Sabartulo".
- **Region set:** none in the data.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Internal name:** zone config Russia, server browser Moscow_KOTH_01, world Russia. Added in Season 2. The link to Moscow is by name and folder only, so it is not confirmed in game.

### Bakurani Outskirts - Jutari

- **Mode:** Sniper Showdown.
- **Control Zone:** 350 m across, 170 m tall. **Hot Zone:** 75 m across, 170 m tall.
- **Placements:** none. The zone is always in one spot.
- **Region set:** none in the data.
- **Hot Zone movement:** first move and move delay both 0 s, default speed 1.5, speed table 1.25 to 3.0.
- **Internal name:** Sniper Showdown zone config Bakurani, server browser Bakurani_SniperShowdown_01.

## Unnamed layouts

The two Sniper Showdown layouts have no display name in the data. The title gives the data name, which is a label in the data and not a name players see.

### Kenya (Africa layout)

- **Map and mode:** the Kenya map in King of the Hill. The zone set is labelled Africa in the data, and its placements are named after Kenya.
- **Control Zone:** 550 m across, 150 m tall. **Hot Zone:** 85 m across, 150 m tall.
- **Placements:** Default (weight 1). North, East and West (weight 0 each).
- **Alternatives:** each alternative is a 500 m ellipse, 500 m tall, with an 85 m Hot Zone that is 500 m tall. That does not match the base layout.
- **Region set:** none in the data.
- **Hot Zone movement:** every 25 s, default speed 1.0.
- **Season 2:** added.
- **Internal name:** zone config Africa, with placements named after a region called Kenya.

### Unnamed layout (data name: Sniper Showdown North America)

- **Mode:** Sniper Showdown, from the config name. A Sniper Showdown entry named for Detroit matches it by name only (not confirmed in game).
- **Control Zone:** 350 m across, 170 m tall. **Hot Zone:** 75 m across, 170 m tall.
- **Placements:** none. **Region set:** none.
- **Hot Zone movement:** first move and move delay both 0 s, default speed 1.5, speed table 1.25 to 3.0.
- **Season 2:** added. Its map is not named in the data.
- **Internal name:** Sniper Showdown zone config NorthAmerica.

### Unnamed layout (data name: Sniper Showdown Russia)

- **Mode:** Sniper Showdown, from the config name. A Sniper Showdown entry named for Moscow matches it by name only (not confirmed in game).
- **Control Zone:** 350 m across, 170 m tall. **Hot Zone:** 75 m across, 170 m tall.
- **Placements:** none. **Region set:** none.
- **Hot Zone movement:** the same as the North America Sniper Showdown layout.
- **Season 2:** added. Its map is not named in the data.
- **Internal name:** Sniper Showdown zone config Russia.

## Server browser entries with no zone data

The server browser lists four King of the Hill entries that the game files name but give no zone configuration. The data does not say which zone layout, if any, they use.

### Unnamed King of the Hill entries with no zone data

These four entries are listed as King of the Hill:

- **Mindori** (data name: Mindori_KOTH_01)
- **Tevza** (data name: Tevza_KOTH_01)
- **Berlin** (data name: Berlin_KOTH_01)
- **Paris** (data name: Paris_KOTH_01)

The zone data contains no configuration with these names. Two region labels in the Bakurani region set begin with "Mindori", but that does not show that the Mindori entry uses the Bakurani layout. Their zone sizes, placements and region sets are not known.

### Tank Town (server browser entry)

The server browser lists Tank Town as a mode with the display name Tank Town and no map image. Tank Town uses the King of the Hill experience unchanged, with the same three teams, 100 point score limit and Control Zone rules. It has no map or zone data of its own.

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
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
