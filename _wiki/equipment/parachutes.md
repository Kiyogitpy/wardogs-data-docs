---
title: Parachutes
parent: "Equipment"
group: "Utility"
description: "The Basic and Sport parachutes: when they can be opened, what the Sport adds over the Basic, and their Season 2 prices and fall rules."
---

# Parachutes

| Parachutes | |
|---|---|
| **General** | |
| Type | Traversal, single use |
| Deploy | By hand only |
| Weight | Basic 2.5, Sport 9 (unit not stated) |
| **Use** | |
| Steering | Basic: no. Sport: yes |
| Opening time | 2 s (Season 2 data) |
| Opens after a fall of | 400 (unit not stated) |
| Clearance above ground to open | 1,000 (unit not stated) |
| **Availability** | |
| Price | Basic 500 cash, Sport 700 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `Id.Item.Parachute.Basic`, `Id.Item.Parachute.Sport` |
{: .wiki-infobox }

The parachute comes in two versions, the Basic Parachute and the Sport Parachute. Both are single-use items that the player deploys by hand after a long fall. The Sport version can be steered, can glide and can pull up, while the Basic version cannot.

## Overview

Both parachutes sit in the Traversal slot of the shop and are listed under the Utility category. Each one is used once, and neither needs an unlock. The shop text says the Basic Parachute "Cannot be Controlled" and the Sport Parachute "Can be Controlled". The Sport version is heavier and has more movement values in the data.

## How it works

### Opening

- A parachute can only be deployed after a fall of at least 400, which is most likely 4 m (derived from the speed scale).
- The player needs at least 1,000 clearance above the ground to open it, most likely 10 m (derived).
- Opening takes 2.0. The data does not give the unit.
- To open a parachute you need the parachute item, the parachute must not already be open, you must be falling, and there must be enough clear space below you. You can cut the parachute only while it is open.
- The game text says both versions reduce fall damage when deployed. The landing damage curve for a parachute runs from 0 at input 695 to 100 at 1,700, in a straight line (input unit not stated).

### Movement values

| Value | Basic | Sport |
|---|---:|---:|
| Horizontal acceleration | 300 | 250 |
| Horizontal drag | 1.0 | 1.1 |
| Turn acceleration | 60 | 40 |
| Pitch speed | 1.0 | 1.6 |
| Glide acceleration | 0 | 1,000 |
| Pull-up drag | 0 | 400 |
| Pull-up stamina used per second | 0 | 50 |
| Pull-up stamina regained per second | 0 | 30 |
| Horizontal speed cap | 2,000 (class default) | 2,200 |
| Vertical speed cap | 5,000 (class default) | 3,000 |
| Roll speed | 1 | 2 (class default) |
| Pull-up stamina pool | 0 | 100 (class default) |

The data does not state units for any of these. The Basic version sets no speed caps, so the class defaults apply to it (2,000 horizontal and 5,000 vertical). The Sport version sets no roll speed or pull-up pool, so the class defaults (2 and 100) apply to it. The Basic Parachute has no glide, no pull-up and no stamina bar, which matches its shop text. The Sport Parachute's pull-up uses its stamina bar, which drains at 50 per second and refills at 30 per second.

## Season 2 changes

| Value | Season 1 | Season 2 |
|---|---:|---:|
| Basic price (cash) | 100 | 500 |
| Sport price (cash) | 1,000 | 700 |
| Fall needed before opening, both | 100 | 400 |
| Sport pull-up drag | 825 | 400 |

Both parachutes also gained three values in Season 2: a vertical drag coefficient of 1.75, an open time of 2.0 and a clearance above the ground to open of 1,000. They have no Season 1 value to compare against.

## See also

- [Backpacks](backpacks.md), for the storage gear
- [Utility Items](utility-items.md), for the rest of the group

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the opening and cutting rules (static reading of the parachute checks)
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock level, shop text, weights
- [Parachutes](../../game-features/Wardogs_GameFeatures_Parachutes_v2.md): movement values, vendor rows and the Season 02 update
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Traversal slot name
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
