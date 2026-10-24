---
title: "Control Zone"
parent: "Game Modes & Maps"
group: "Game modes"
description: "The zone objective behind King of the Hill and Sniper Showdown: zone sizes, the moving Hot Zone, capture rules and placement."
---

# Control Zone

| Control Zone | |
|---|---|
| Type | Zone objective |
| Used by | King of the Hill, Sniper Showdown |
| Zone shape | Cylinder, with a Hot Zone inside |
| Hot Zone movement | Moves on a timer; speed set per map |
| Internal name | ControlZone (game feature) |
{: .wiki-infobox }

A Control Zone is a large cylinder laid over a map. Players capture it by standing in it with their side. Inside it sits a smaller Hot Zone that pays more and moves during the match. The zone is the objective of [King of the Hill](king-of-the-hill.md) and is also used in [Sniper Showdown](sniper-showdown.md).

## Overview

Each map has a Control Zone configuration that sets the size of the zone, the size of the Hot Zone, how the Hot Zone moves, and where the zone can appear. Maps with alternative placements pick one of them each match. The map list and zone sizes are on [Maps](maps.md).

## Rules and objectives

- **Capturing.** Only a living player adds to a capture. A critically wounded or dead player adds nothing.
- **Hot Zone.** The Hot Zone is a smaller cylinder in the centre of the Control Zone. It pays the higher rewards and is the place the Hot Zone Magnet works in. On the standard maps it is 85 m across.
- **Moving Hot Zone.** On the standard maps the Hot Zone moves every 25 seconds. The move speed starts at 1.0 and can change within a table from 0.75 to 2.0. On the Sniper Showdown maps the first move is at 0 seconds and the default speed is 1.5, with a table from 1.25 to 3.0.
- **Alternative placements.** Several maps have alternative spots for their zone. Each spot has a weight. The data suggests one spot is picked by weight at random, but this is not confirmed in the code. Some spots have weight 0, so by the weights alone they are never picked. See [Maps](maps.md).
- **Map regions.** Three of the main maps (Bakurani, Ozeti and Zestafona) also have named regions that the zone can sit in, with weights. The Ozeti and Zestafona links are made by name, so they are not fully confirmed. Bakurani has 60 regions, Ozeti 55 and Zestafona 56. Towers are weight 0 on every map. On Bakurani, a few regions (for example Sunflowers House, West Forest Pylon and Hillside Top) have weight 5, against weight 1 for most others. Which region is chosen, and how the weights are used, is not confirmed in the data.
- **Placement.** Players cannot place or deploy items outside a Control Zone. The game shows "location not in a Control Zone" and rejects the deployment.
- **Control state.** The on-screen status shows the zone as waiting to start, contested or controlled.

### Zone sizes

Sizes are the data values converted to metres. Height is the vertical extent.

| Map | Control Zone (m) | Hot Zone (m) | Placements |
|---|---|---|---|
| Bakurani | 500 × 500 × 170 | 85 × 85 × 170 | 3 |
| Ozeti | 550 × 550 × 150 | 85 × 85 × 150 | 4 |
| Zestafona | 500 × 500 × 500 | 85 × 85 × 850 | 4 |
| Saburtulo | 550 × 550 × 150 | 85 × 85 × 150 | 4 |
| Africa (see [Maps](maps.md)) | 550 × 550 × 150 | 85 × 85 × 150 | 4 |
| Bakurani Outskirts (Sniper Showdown) | 350 × 350 × 170 | 75 × 75 × 170 | None (fixed spot) |
| Sniper Showdown, North America and Russia zones | 350 × 350 × 170 | 75 × 75 × 170 | None (fixed spot) |

The Zestafona Hot Zone is 850 m tall against a 500 m tall Control Zone. The data does not say whether that is intended.

### Alternative placements

| Map | Placement | Weight |
|---|---|---|
| Bakurani | Default | 2.0 |
| Bakurani | Farmland | 1.0 |
| Bakurani | Lumberyard | 1.0 |
| Ozeti | Default, Church, River | 1.0 each |
| Ozeti | Farmland | 0.0 |
| Zestafona | Default, Water Treatment, Houses | 1.0 each |
| Zestafona | Small Factory | 0.0 |
| Africa | Default | 1.0 |
| Africa | North, East, West | 0.0 each |
| Saburtulo | Hospital | 1.0 |
| Saburtulo | Bazaar, River, Hillside | 0.0 each |

## Rewards

Cash for zone events, from the cash tables: a Control Zone event (contested, owned or not owned) pays 150, and entering the zone for the first time in a life pays 100. A Hot Zone event pays 600, and entering the Hot Zone pays 0. Owning or taking a Hot Zone Magnet pays 5,000 on activation. The complete table is on [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

## Season 2 changes

- Four Control Zone configurations were added: Sniper Showdown for North America and Russia, and Africa and Russia zones for the main modes.
- The Africa and Russia zones are 550 m across with 85 m Hot Zones and a 25-second move delay. Each has four alternatives.
- The two new Sniper Showdown zones are 350 m across with 75 m Hot Zones and no alternatives.

## See also

- [King of the Hill](king-of-the-hill.md)
- [Sniper Showdown](sniper-showdown.md)
- [Maps](maps.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)

## Sources

- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Zone rewards data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-rewards.json)
