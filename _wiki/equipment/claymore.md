---
title: Claymore
parent: "Equipment"
group: "Explosives and throwables"
description: "The Claymore: a placed anti-infantry mine that fires when a player or vehicle walks into the area in front of it."
---

# Claymore

| Claymore | |
|---|---|
| ![Claymore]({{ '/assets/img/icons/utility-3d/t_ui_icon_claymore_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Lethal, placed mine (anti-infantry) |
| How it is used | Placed on the ground facing the area to cover |
| Trigger | A moving living player or vehicle in the trigger area in front, with a clear line of sight |
| Arming | 2 s after placement |
| Placement | Not allowed in a safe zone |
| Health | 1 HP |
| **Blast** | |
| Damage at centre | 150 HP |
| Full damage out to | 1.5 m |
| No damage beyond | 3 m |
| Minimum blast damage | 30 HP |
| **Availability** | |
| Price | 900 cash |
| Shop unlock level | 0 |
| Required items | None |
| Internal name | `Id.Item.Claymore` |
{: .wiki-infobox }

The Claymore is a placed mine built to hit infantry. It has a short blast, a narrow trigger area in front of it, and a fixed direction. It is a poor answer to vehicles, which take a large number of hits to break.

## Overview

The Claymore is sold as a Lethal, Quick Slot item. It is placed, not thrown. Its trigger is a box in front of the mine, and it is set off by a player or vehicle that enters that box.

For the mine that is aimed at vehicles, see [AT Mine](at-mine.md). Both are described on [Grenades and Explosives](grenades-and-explosives.md).

## How it works

**Placing.** The Claymore is placed on the ground up to 4 m from the player. It cannot be placed in a safe zone (Alpha, Bravo, Charlie or the hostile safe zone). The data stores a placement angle of 30. A static reading of the game's placement code shows it compares the slope of the surface you aim at (the angle between the surface normal and straight up, in degrees) with that number, so a surface steeper than 30 degrees from level is refused. The reach is the same 4 m line from your view, plus a small allowance for the Claymore's own size. While the Claymore is being placed, the player moves at 40% speed.

**Arming.** The Claymore is armed 2 s after it is placed. Until then its trigger is off.

**Trigger.** The trigger is a box in front of the mine:

- A target must be alive and moving: a living player whose speed is above 0 sets it off, and so does a vehicle driver or passenger in a moving vehicle. A motionless target does not trigger it.
- The check compares the placer's faction with the target's, so the data points to enemies as the targets. The data does not show how a teammate is handled.
- The blast must reach the target. The Claymore runs a line-of-sight check to the target's damage points before it fires.

**Being shot.** An explosion nearby sets the Claymore off. Other damage destroys it, because its health is 1 HP.

**Detonation.** The mine goes off once it has taken 50 damage. That is the default for placed explosives, and neither the Claymore nor the AT mine overrides it (static reading). Once it has gone off it is removed. Whether the 50 counts each hit or the running total was not checked in play.

**Friendly fire.** The damage tables reduce friendly fire only for infantry bullets (-50 %) and large hammers (-70 %). Explosives and fire have no friendly-fire reduction in the tables. Any limit on hitting teammates with this item would have to come from the item itself or from native code, which the data does not show.

## Damage

### To players

The blast does its full 150 HP from the centre out to 1.5 m. Beyond 1.5 m the damage falls in a straight line to zero at 3 m. Examples from the data:

- At 2.5 m: 100 HP
- At 3 m and beyond: nothing

Armor reduces this damage by body part. See [Body Armor](body-armor.md).

### To vehicles

The data gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. The Claymore is weak against vehicles, so these numbers are high.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 6 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 14 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 106 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 141 |

Against armour the Claymore is weak. Its table entry is -95 % on the tanks, -75 % on the Humvee family and the Havoc, -65 % on the Ural, -62.5 % on the Wolf-110 and -50 % on the Little Bird, Dune Buggy, Bobcat and Kodiak. Each figure is the table's amount for the Claymore's source, and other entries on the same row also apply.

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

The Season 2 items data lists no change to the Claymore, and no change to its price.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [AT Mine](at-mine.md), the vehicle-triggered mine
- [Fire, Smoke and Flash](fire-smoke-and-flash.md), which covers mine and Claymore triggers in more detail
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the 50 damage detonation rule and the armour readings for the Claymore
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): placement, trigger box, arming delay and destruction rules
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): Claymore actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Claymore target, line-of-sight and placement rules.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
