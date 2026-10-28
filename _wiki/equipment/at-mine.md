---
title: AT Mine
parent: "Equipment"
group: "Explosives and throwables"
description: "The AT Mine: a placed anti-vehicle mine that fires when a moving vehicle drives over it, with 300 HP at its centre."
---

# AT Mine

| AT Mine | |
|---|---|
| ![AT Mine]({{ '/assets/img/icons/utility-3d/T_UI_Item_Mine_BC.png' | relative_url }}){: .wiki-infobox-img } | |
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

**Placing.** The mine is placed on the ground up to 4 m from the player, and the player moves at 40% speed while placing it. It cannot be placed in a safe zone (Alpha, Bravo, Charlie or the hostile safe zone).

**Arming.** The mine is armed 1 s after it is placed.

**Trigger.** The mine has a trigger box under it. It checks for vehicles every 0.1 s. A vehicle sets it off only when it is moving faster than 0.1 km/h. Players and infantry do not set it off.

**Friendly vehicles.** A vehicle on the player's own side sets the mine off too.

**Being shot.** Any damage sets the mine off except a thrown impact, so shooting an AT Mine detonates it.

**Detonation.** The mine goes off once it has taken 50 damage. That is the default for placed explosives, and neither the Claymore nor the AT mine overrides it (static reading). Once it has gone off it is removed. Whether the 50 counts each hit or the running total was not checked in play.

**Friendly fire.** The damage tables reduce friendly fire only for infantry bullets (-50 %) and large hammers (-70 %). Explosives and fire have no friendly-fire reduction in the tables. Any limit on hitting teammates with this item would have to come from the item itself or from native code, which the game files do not show.

## Damage

### To players

The mine does not trigger on players, but its blast does harm people near it when it goes off. The blast does its full 300 HP from the centre out to 3.8 m. Beyond 3.8 m the damage falls in a straight line to zero at 7.5 m. Examples:

- At 2.5 m: 300 HP
- At 5 m: 250 HP
- At 7.5 m and beyond: nothing

Armor reduces this damage by body part. See [Body Armor](body-armor.md).

### To vehicles

The table gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Treat these as a guide, because blasts near several parts can count more than once.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 1 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 1 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 2 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 2 |

Against armour the AT mine is strong. Its table entry is +200 % on most vehicles (the Humvee, Kodiak, Dune Buggy, Bobcat, Havoc and Wolf-110), +145 % on the tanks and +250 % on the Ural. Each figure is the table's amount for the mine's source. The same vehicle row has other explosive and hit-location entries that also apply, so the total is not that figure alone.

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

No Season 2 change to the AT Mine, or to its price, is listed.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [Claymore](claymore.md), the mine that is triggered by people
- [Fire, Smoke and Flash](fire-smoke-and-flash.md), which covers mine triggers in more detail
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the 50 damage detonation rule and the armour readings for the AT mine
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): placement, trigger, arming delay and shot rules
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): AT mine actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
