---
title: M67 Frag Grenade
parent: "Equipment"
group: "Explosives and throwables"
description: "The M67 Frag Grenade: a thrown blast grenade with a 4 second fuse, 100 HP at its centre and 10 m of reach."
---

# M67 Frag Grenade

| M67 Frag Grenade | |
|---|---|
| **General** | |
| Type | Lethal, thrown (quick slot) |
| How it is used | Thrown. Can be cooked (held before throwing) and thrown back |
| Fuse | 4 s after the throw |
| **Blast** | |
| Damage at centre | 100 HP |
| Full damage out to | 5 m |
| No damage beyond | 10 m |
| Minimum blast damage | 10 HP |
| Thrown contact | 10 HP |
| **Availability** | |
| Price | 200 cash |
| Shop unlock level | 1 |
| Required items | None |
| Internal name | `Id.Item.M67Grenade` |
{: .wiki-infobox }

The M67 Frag Grenade is the standard hand grenade. It is thrown, goes off 4 seconds later, and does up to 100 HP to everyone close to the blast. Its damage stops at 10 m. It can also be thrown back before it goes off.

## Overview

The M67 is the basic blast throwable in the item shop. It sits in the quick slot and is listed as a lethal item. The data also has a gold variant, but it has no shop listing, so it is not described here.

For the blast numbers of every other explosive, see [Grenades and Explosives](grenades-and-explosives.md).

## How it works

**Fuse.** The grenade goes off 4 s after it is thrown. Holding it before the throw (cooking) is allowed, so a player can shorten the time left before it lands. The data allows the grenade to be thrown back.

**Throw.** The data has three throws:

| Throw | Speed | Notes |
|---|---:|---|
| Overarm (primary) | 25 m/s (2,500 cm/s) | The longest throw |
| Underarm (secondary) | 14 m/s (1,400 cm/s) | Short range |
| Back throw | 18 m/s (1,800 cm/s) | Third throw action in the data; the data does not say when it is used |

**Contact.** A grenade that hits something before it goes off does 10 HP of thrown-contact damage.

## Damage

### To players

The blast does its full 100 HP from the centre out to 5 m. Beyond 5 m the damage falls in a straight line to zero at 10 m. Examples from the data:

- At 5 m: 100 HP
- At 7.5 m: 50 HP
- At 10 m and beyond: nothing

Body armor reduces this damage by body part. See [Body Armor](body-armor.md). The numbers here are before armor.

### To vehicles

The data gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Blasts near several parts of a vehicle can count more than once, so treat these as a guide.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 1 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 2 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 7 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 6 |

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

The Season 2 items data lists no change to the M67 Frag Grenade.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [C4 Charge](c4-charge.md), a remote-detonated charge with a larger blast
- [Improvised Explosive Device](improvised-explosive-device.md)
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff, fuse and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): throw speeds and throw actions
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price, unlock level and shop text
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): thrown actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
