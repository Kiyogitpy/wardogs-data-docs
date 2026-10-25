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

Each map has a Control Zone configuration that sets the size of the zone, the size of the Hot Zone, how the Hot Zone moves, and where the zone can appear. Maps with alternative placements use one of them each match. The server's map rotation can name it, and otherwise it is drawn at random by weight (see [Zone Layouts](zone-layouts.md)). The map list and zone sizes are on [Maps](maps.md).

## Rules and objectives

- **Capturing.** Only a living player adds to a capture. A critically wounded or dead player adds nothing.
- **Hot Zone.** The Hot Zone is a smaller cylinder in the centre of the Control Zone. It pays the higher rewards and is the place the Hot Zone Magnet works in. An activated [Drill Rig](../building/drill-rig.md) moves the Hot Zone toward it at a speed in metres per second, and the travel time adds to how long the rig stays active. On the standard maps it is 85 m across.
- **Moving Hot Zone.** On the standard maps the Hot Zone is placed at the start and then moves about every 25 seconds. The move speed starts at 1.0 and can change within a table from 0.75 to 2.0. On the Sniper Showdown maps the first move is at 0 seconds and the default speed is 1.5, with a table from 1.25 to 3.0.
- **Alternative placements.** Several maps have alternative spots for their zone. The server's map rotation can name the spot for each map entry, and a named spot is used even if its weight is 0. Without a name, one spot is drawn at random by weight, and a spot with weight 0 is never drawn that way. See [Zone Layouts](zone-layouts.md) and [Maps](maps.md).
- **Map regions.** Three of the main maps (Bakurani, Ozeti and Zestafona) also have named regions that the zone can sit in. The Hot Zone moves to a region drawn at random by weight, and a region with weight 0 (the towers) is never drawn that way. The region just used gives away half its weight, so it is unlikely to come up again at once. Bakurani has 60 regions, Ozeti 55 and Zestafona 56. On Bakurani, a few regions (for example Sunflowers House, West Forest Pylon and Hillside Top) have weight 5, against weight 1 for most others.
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
| Kenya (Africa layout) (see [Maps](maps.md)) | 550 × 550 × 150 | 85 × 85 × 150 | 4 |
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
| Kenya (Africa layout) | Default | 1.0 |
| Kenya (Africa layout) | North, East, West | 0.0 each |
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
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
