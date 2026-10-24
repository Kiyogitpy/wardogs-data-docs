---
title: Fire, Smoke and Flash
parent: "Equipment"
group: "Explosives and throwables"
description: "Molotov fire, smoke and signal grenades, mine and Claymore triggers, and throwing. Flash and stun grenades are not in this build."
---

# Fire, Smoke and Flash

| Fire, smoke and flash | |
|---|---|
| Fire | Molotov (burning area for 45 s) |
| Smoke | White and Black smoke; eight coloured signal grenades; vehicle smoke |
| Triggered | AT Mine, Claymore, C4 and IED (detail below) |
| Flash and stun | not in this build |
{: .wiki-infobox }

This article covers the throwables and placed gear that do something other than a direct blast: the Molotov's burning area, the smoke and signal grenades, the triggers of the mines and Claymore, and how throwables are thrown. Blast damage and radius for every explosive are on [Grenades and Explosives](grenades-and-explosives.md).

## Overview

Flash and stun grenades are not in the data for this build. There is no flashbang item, no shop listing and no effect. The only remnants are three sound effects and a Medic skill that reduces the effect of flash and stun, which has no number attached in the data.

## Effects

### Molotov

The Molotov bursts on detonation, dealing 40 HP at its centre out to 2.5 m and nothing beyond 5 m. It then leaves a burning area.

- **Burning area.** The fire lasts up to 45 s. It damages players and vehicles inside it every 0.4 s.
- **Players.** Each tick deals 15 HP, which is 37.5 HP per second while standing in the fire. Players without the Alive state take no damage.
- **Vehicles.** Each tick deals 2 health, which is 5 per second.
- **Burning status.** A player in the fire gets a "burning" status, shown with a screen effect that darkens and blurs the view. The status ends when the player leaves the fire. The data points to this without a timer, but this is not fully confirmed.

Not yet known: whether armor reduces fire damage, whether the Molotov bursts on impact or when its fuse runs out, and whether a teammate's Molotov fire damages you.

### Smoke grenades

Smoke grenades make a cloud of smoke. The data gives the length of each cloud, but no effect on play. No item applies a game effect through smoke, so smoke does not hurt, heal or slow anyone in the data. What the cloud blocks, such as sight or enemy targeting, is not yet known.

| Item | Cloud length | Cost (cash) |
|---|---:|---:|
| M18 Smoke Grenade: White | 120 s | 100 |
| M18 Smoke Grenade: Black | 120 s | 100 |
| Vehicle smoke (countermeasure) | 6 s | 750 |

Vehicle smoke is a countermeasure that trails smoke around a vehicle and then settles into a larger screen that gives infantry cover, according to the shop text.

### Signal grenades

Signal grenades release a column of coloured smoke and place a marker on the map. The data gives 180 s of cloud length for most colours and 64 s for the blue one. Each costs 50 cash.

| Colour | Shop name | Map marker | Type |
|---|---|---|---|
| Yellow | Alert | Alert | Tactical |
| Red | Hostile | Hostile | Tactical |
| Blue | Friendly | Friendly | Tactical |
| Orange | Damaged Vehicle | Damaged vehicle | Tactical |
| Green | Supply Request | Supply Request | Logistics |
| Purple | Landing Zone | Landing Zone | Logistics |

How the marker is created is not yet known.

### Mines and placed explosives

The AT Mine, Claymore and IED are placed on the ground, and each has its own trigger. Placing them takes time, and the player moves at 40% speed while placing. A placed mine has 1 HP.

| | AT Mine | Claymore | C4 Charge | IED |
|---|---|---|---|---|
| Triggered by | Vehicles | Players and vehicles | Remote Detonator | IED trigger |
| Speed rule | Vehicle moving above 0.1 km/h | Vehicle moving above 0 km/h | none | none |
| Arming delay | 1 s after placement | 2 s after placement | none | none |
| Delay after trigger | none | none | none (charge 0.2 s) | 3 s |
| Team rule | Triggers on friendly vehicles | Triggers on teammates | none | none |
| Line of sight | not used | yes, to the target | none | none |
| Range | placed up to 4 m away | placed up to 4 m away | 200 m (remote) | no limit |
| Shot | any damage except thrown impacts sets it off | an explosion sets it off; other damage destroys it | a C4 or IED blast sets it off; it has 30 HP | same as C4 |

Notes from the data:

- The AT Mine checks for vehicles every 0.1 s, and ignores everything else.
- The Claymore's trigger area is in front of it. Players must have a matching tag to count as a target.
- The C4 charge and IED charge stick to the surface they hit. A charge whose owner is no longer valid is removed after a 5 s check, without a blast.
- Placement distance for the mines and Claymore is 400 units, which is about 4 m. The placement angle limit is 30, which the data reads as degrees; this is assumed.

### Throwing

The Molotov and smoke grenades use the same throw speeds:

| Throw | Speed (cm/s) | Speed (m/s) |
|---|---:|---:|
| Overarm (primary) | 2,000 | 20 |
| Underarm (secondary) | 1,200 | 12 |

Each throw also has a speed curve in the data. How the curve combines with the flat speed is not yet known.

## Use and timing

| Item | Fuse | Notes |
|---|---|---|
| Molotov | 5 s | Cannot be cooked (held before throwing) |
| Smoke grenades | 3 s | The cloud lasts for the length given above |
| C4 Charge | 0.2 s after the trigger | Set off by the Remote Detonator |
| IED | 3 s after the trigger | |

## Cost

| Item | Price (cash) |
|---|---:|
| Molotov | 340 |
| M18 Smoke Grenade: White or Black | 100 |
| Signal grenades (each colour) | 50 |
| Vehicle smoke | 750 |
| AT Mine | 650 |
| Claymore | 900 |
| IED trigger | 300 |

## Season 2 changes

The Season 2 items data lists no change to the Molotov, smoke grenades, mines or Claymore.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), for blast damage and fuses of the frag grenade, C4 and launcher rounds
- [Buildables](buildables.md), for the structures that the Molotov fire damages

## Sources

- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): Molotov burst and fire, smoke assets, throws and mine triggers
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, shop text and signal grenade names
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): the Molotov fire field and mine values
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): Molotov blast damage and fuses
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
