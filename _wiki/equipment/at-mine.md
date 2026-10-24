---
title: AT Mine
parent: "Equipment"
group: "Explosives and throwables"
description: "The AT Mine: a placed anti-vehicle mine that fires when a moving vehicle drives over it, with 300 HP at its centre."
---

# AT Mine

| AT Mine | |
|---|---|
| **General** | |
| Type | Lethal, placed mine (anti-vehicle) |
| How it is used | Placed on the ground |
| Trigger | A vehicle moving over it above 0.1 km/h |
| Arming | 1 s after placement |
| Health | 1 HP |
| **Blast** | |
| Damage at centre | 300 HP |
| Full damage out to | 3.8 m |
| No damage beyond | 7.5 m |
| Minimum blast damage | 50 HP |
| **Availability** | |
| Price | 650 cash |
| Shop unlock level | 0 |
| Required items | None |
| Internal name | `ID.Item.ATMine` |
{: .wiki-infobox }

The AT Mine is a placed mine for stopping vehicles. It ignores people and is set off by a vehicle that drives over it. Its 300 HP centre blast ties with the Improvised Explosive Device for the largest of the placed explosives.

## Overview

The AT Mine is sold as a Lethal, Quick Slot item. It is placed, not thrown. It is triggered only by vehicles. Friendly vehicles set it off as well, so it can be a risk to a player's own team.

For the mine that goes off on people, see [Claymore](claymore.md).

## How it works

**Placing.** The mine is placed on the ground up to 4 m from the player, and the player moves at 40% speed while placing it.

**Arming.** The mine is armed 1 s after it is placed.

**Trigger.** The mine has a trigger box under it. It checks for vehicles every 0.1 s. A vehicle sets it off only when it is moving faster than 0.1 km/h. Players and infantry do not set it off.

**Friendly vehicles.** A vehicle on the player's own side sets the mine off too.

**Being shot.** Any damage sets the mine off except a thrown impact, so shooting an AT Mine detonates it.

## Damage

### To players

The mine does not trigger on players, but its blast does harm people near it when it goes off. The blast does its full 300 HP from the centre out to 3.8 m. Beyond 3.8 m the damage falls in a straight line to zero at 7.5 m. Examples from the data:

- At 2.5 m: 300 HP
- At 5 m: 250 HP
- At 7.5 m and beyond: nothing

Armor reduces this damage by body part. See [Body Armor](body-armor.md).

### To vehicles

The data gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Treat these as a guide, because blasts near several parts can count more than once.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| Little Bird family helicopter | 400 HP | 1 |
| Humvee | 500 HP | 1 |
| T-72B3 | 750 HP | 2 |
| 1000 HP vehicle | 1000 HP | 2 |

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

The Season 2 items data lists no change to the AT Mine, and no change to its price.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [Claymore](claymore.md), the mine that is triggered by people
- [Fire, Smoke and Flash](fire-smoke-and-flash.md), which covers mine triggers in more detail
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): placement, trigger, arming delay and shot rules
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): AT mine actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
