---
title: Improvised Explosive Device
parent: "Equipment"
group: "Explosives and throwables"
description: "The Improvised Explosive Device: a placed charge that a player sets off from anywhere with its trigger, 3 s after the trigger is pressed."
---

# Improvised Explosive Device

| Improvised Explosive Device | |
|---|---|
| ![Improvised Explosive Device]({{ '/assets/img/icons/utility-3d/T_UI_Vendor_IED2.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Lethal, placed explosive with a remote trigger |
| How it is used | Placed on the ground, then set off with its trigger |
| Fuse | 3 s after the trigger is pressed |
| **Blast** | |
| Damage at centre | 300 HP |
| Full damage out to | 4 m |
| No damage beyond | 8 m |
| Minimum blast damage | 60 HP |
| Thrown contact | 10 HP |
| Remote range | No limit |
| **Availability** | |
| Price | 300 cash |
| Shop unlock level | 0 |
| Required items | None |
| Internal name | `Id.Item.IED.Trigger` (trigger), `Id.Item.IED.Explosive` (charge) |
{: .wiki-infobox }

The Improvised Explosive Device is a placed charge with a long-range trigger. The player places it, then presses the trigger once the target is close enough to be caught by the blast. It has no range limit, and it does 300 HP at its centre, the same as the AT Mine.

## Overview

The Improvised Explosive Device is sold as a Lethal, Quick Slot item. The shop text says it can only be used once. The trigger allows one placed IED at a time.

The IED uses a C4-style detonation, so a blast from another C4 or IED sets it off. See [C4 Charge](c4-charge.md).

## How it works

**Placing.** The IED is placed on the ground. It cannot be placed in a safe zone (Alpha, Bravo, Charlie or the hostile safe zone), and it has no set placement distance in the data.

**Trigger.** Pressing the IED trigger starts a 3 s delay. After the delay the IED goes off. Nothing in the data limits the distance from the player to the trigger.

**Chain reactions.** Another C4 or IED blast sets it off.

## Default controls

Held, the IED uses the left mouse button (right trigger on a gamepad) for its main use, the right mouse button (left trigger) for its secondary use, and I to inspect. These are defaults and can be rebound in the control settings.

## Damage

### To players

The blast does its full 300 HP from the centre out to 4 m. Beyond 4 m the damage falls in a straight line to zero at 8 m. Examples from the data:

- At 5 m: 225 HP
- At 7.5 m: 60 HP
- At 8 m and beyond: nothing

Armor reduces this damage by body part. See [Body Armor](body-armor.md).

### To vehicles

The data gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Treat these as a guide, because blasts near several parts can count more than once.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 2 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 1 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 3 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 2 |

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

The Season 2 items data lists no change to the Improvised Explosive Device, and no change to its price.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [C4 Charge](c4-charge.md), the charge the IED's detonation is based on
- [AT Mine](at-mine.md)
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): trigger delay, placement and detonation rules
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price, description and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): IED actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Misc Gameplay Assets: item inputs](../../content/Wardogs_MiscGameplayAssets_v1.md): section 7a, the default keys
