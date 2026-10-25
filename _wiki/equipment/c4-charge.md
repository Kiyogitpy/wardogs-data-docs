---
title: C4 Charge
parent: "Equipment"
group: "Explosives and throwables"
description: "The C4 Charge and its Remote Detonator: a charge that sticks to a surface and goes off on command, with a 200 m remote range."
---

# C4 Charge

| C4 Charge | |
|---|---|
| **General** | |
| Type | Lethal, remote-detonated charge |
| How it is used | Thrown at a surface, where it sticks. Set off with the Remote Detonator |
| Fuse | 0.2 s after the Remote Detonator is pressed |
| Charge health | 30 HP |
| **Blast** | |
| Damage at centre | 250 HP |
| Full damage out to | 2.5 m |
| No damage beyond | 6 m |
| Minimum blast damage | 20 HP |
| Thrown contact | 10 HP |
| Remote range | 200 m |
| **Availability** | |
| Price, C4 Charge | 250 cash |
| Price, Remote Detonator | 650 cash |
| Shop unlock level | 0 |
| Internal name | `Id.Item.C4Explosive` (charge), `Id.Item.C4Trigger` (Remote Detonator) |
{: .wiki-infobox }

The C4 Charge is a strong blast that a player places and sets off from a distance. The charge sticks to whatever it hits, and the Remote Detonator sets it off. Because the player chooses when it goes off, the charge can be placed first and set off later.

## Overview

The C4 Charge is sold as a Lethal, Resource item. It does nothing on its own. The Remote Detonator is a separate Equipment item in the quick slot, and it is needed to set the charge off. Both are in the item shop.

## How it works

**Throwing.** The charge is thrown with the Remote Detonator's throw action, a short underarm throw at 9 m/s (900 cm/s). Each throw uses one C4 Charge from the inventory.

**Sticking.** The charge sticks to the surface it hits, and it is attached to that object.

**Detonating.** Pressing the Remote Detonator sets off every charge in range after a 0.2 s delay. The Remote Detonator's range is 200 m. A Support skill raises it to 240 m and then to 280 m.

**Expiry.** If the player who placed a charge is no longer valid, the charge is removed after a check every 5 s. It is removed without a blast.

**Chain reactions.** A blast from another C4 or from an IED sets off a charge. Other damage must wear down its 30 HP, and the charge is destroyed when that runs out.

## Damage

### To players

The blast does its full 250 HP from the centre out to 2.5 m. Beyond 2.5 m the damage falls in a straight line to zero at 6 m. Examples from the data:

- At 5 m: about 71 HP
- At 6 m and beyond: nothing

Armor reduces this damage by body part. See [Body Armor](body-armor.md).

### To vehicles

The data gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Treat these as a guide, because blasts near several parts can count more than once.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 2 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 3 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 5 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 4 |

Against armour the C4 is weak on the tanks and the Humvee family, and very strong on stationary weapons. Its table entry is -25 % on the tanks and -15 to -52.5 % on the Humvee family and the Havoc. On stationary weapons it is +1,500 % on the Mistral, +700 % on the Phalanx and +300 % on the Mortar and the Stingray. Other entries on the same row also apply.

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

The Season 2 items data lists no change to the C4 Charge or the Remote Detonator, and no change to their prices.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [M67 Frag Grenade](m67-frag-grenade.md)
- [Improvised Explosive Device](improvised-explosive-device.md), which is also set off by a remote trigger
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the C4 armour readings against vehicles and stationary weapons
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): charge health, detonator range, throw speed and expiry check
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): names, prices and unlock levels
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): charge actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
