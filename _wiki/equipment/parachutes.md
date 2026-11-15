---
title: Parachutes
parent: "Equipment"
group: "Utility"
description: "The Basic and Sport parachutes: when they can be opened, what the Sport adds over the Basic, and their S3 saved prices and movement settings."
---

# Parachutes

| Parachutes | |
|---|---|
| ![Parachutes]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Parachute_Basic.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Traversal, single use |
| Deploy | By hand only |
| Weight | Basic 2.5, Sport 9 kg |
| **Use** | |
| Steering | Basic: no. Sport: yes |
| Stored opening duration | Basic 3.5; Sport 2.0 (seconds in the historical model) |
| Stored minimum fall height | Basic 800; Sport 400 (8 m / 4 m assuming cm) |
| Stored minimum ground clearance | Basic 2,000; Sport 1,000 (20 m / 10 m assuming cm) |
| **Availability** | |
| Price | Basic 1,250 cash, Sport 2,250 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `Id.Item.Parachute.Basic`, `Id.Item.Parachute.Sport` |
{: .wiki-infobox }

The parachute comes in two versions, the Basic Parachute and the Sport Parachute. Both are single-use items that the player deploys by hand after a long fall. The Sport version can be steered, can glide and can pull up, while the Basic version cannot.

## Overview

Both parachutes sit in the Traversal slot of the shop and are listed under the Utility category. Each one is used once. Season 3 makes parachutes unlockable through every role track; the saved shop level 0 is not a claim of unrestricted availability. The shop text says the Basic Parachute "Cannot be Controlled" and the Sport Parachute "Can be Controlled". The Sport version is heavier and has more movement values.

## How it works

### Opening

- The S3 `MinFallHeightBeforeAbleToParachute` value is 800 for Basic and 400 for Sport: 8 m and 4 m if the height unit is cm. The current native threshold consumer has not been reverified.
- The stored minimum ground clearance is 2,000 for Basic and 1,000 for Sport: 20 m and 10 m if the height unit is cm.
- `OpenDuration` is 3.5 for Basic and 2.0 for Sport; interpreting these as seconds follows the historical model, not an S3 timing measurement.
- To open a parachute you need the parachute item, the parachute must not already be open, you must be falling, and there must be enough clear space below you. You can cut the parachute only while it is open.
- The game text says both versions reduce fall damage when deployed. The two S3 movement profiles reference different piecewise-linear landing curves. Basic stores input/output pairs 700/0, 900/20 and 1,200/100; Sport stores 800/0, 1,000/25 and 1,900/100. If the historical speed-in-cm/s interpretation applies, these are 7/9/12 m/s for Basic and 8/10/19 m/s for Sport. Current damage application is unverified.

### Movement values

| Value | Basic | Sport |
|---|---:|---:|
| Horizontal acceleration | 150 | 550 |
| Horizontal drag | 1.0 | 1.0 |
| Vertical drag | 1.6 | 1.5 |
| Turn acceleration | 30 | 110 |
| Pitch speed | 1.0 | 4.0 |
| Glide acceleration | 0 | 1,300 |
| Pull-up drag | 0 | 550 |
| Pull-up stamina used per second | 0 | 50 |
| Pull-up stamina regained per second | 0 | 47.5 |
| Horizontal speed cap | Not serialized; historical default 2,000 | 2,200 |
| Vertical speed cap | Not serialized; historical default 5,000 | 3,000 |
| Roll speed | 1 | 4 |
| Pull-up stamina pool | 0 | 150 |

These are saved field values; units and current consumers are not independently established here. Basic omits its speed caps: the historical 2,000/5,000 defaults are assumptions, not verified S3 defaults. Sport now explicitly stores roll speed 4 and a pull-up pool of 150. The Basic Parachute has no glide, no pull-up and no stamina bar, which matches its shop text. The Sport Parachute's pull-up uses its stamina bar, which drains at 50 per second and has a stored refill rate of 47.5 per second.

## Season 3 announcement

Basic is intended for emergency helicopter exits: effective above about 100 m, with survival possible above 60 m given a fast reaction. Opening is slower, and pulling within about 20 m of the ground is blocked. Its price rose from $500 to $1,250. Sport is intended for BASE jumping: effective above about 60 m, with survival possible above 40 m given a fast reaction; its price rose from $700 to $2,250. Sport turns, glides and dives faster, with a stronger, longer flare and somewhat faster descent. These approximate jump heights are practical guidance, not the stored minimum-fall thresholds. Both parachutes are now unlockable through every role track.

Source: [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). These are developer-announced changes; saved fields and historical models below do not independently verify the current binary consumer.

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

- [S3 Basic movement data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DA_ParachuteMovement_Basic.json) and [Sport movement data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DA_ParachuteMovement_Sport.json): current stored values and separate landing-curve references.
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the opening and cutting rules (static reading of the parachute checks)
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock level, shop text, weights
- [Parachutes](../../game-features/Wardogs_GameFeatures_Parachutes_v2.md): movement values, vendor rows and the Season 02 update
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Traversal slot name
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
