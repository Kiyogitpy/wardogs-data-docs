---
title: Claymore
parent: "Equipment"
group: "Explosives and throwables"
description: "The Claymore: a placed anti-infantry mine that fires when a player or vehicle walks into the area in front of it."
---

# Claymore

| Claymore | |
|---|---|
| **General** | |
| Type | Lethal, placed mine (anti-infantry) |
| How it is used | Placed on the ground facing the area to cover |
| Trigger | A player or vehicle in the trigger area in front |
| Arming | 2 s after placement |
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

**Placing.** The Claymore is placed on the ground up to 4 m from the player. The placement angle limit is 30. The data does not state the unit, and it is assumed to be degrees. While the Claymore is being placed, the player moves at 40% speed.

**Arming.** The Claymore is armed 2 s after it is placed. Until then its trigger is off.

**Trigger.** The trigger is a box in front of the mine:

- A player is a target when a check on the player's gameplay tag passes. The tag that counts is not yet known.
- A vehicle is a target when it is moving faster than 0 km/h.
- A teammate on the same side also sets it off, because the data does not exempt them.
- Before it fires, the Claymore runs a line-of-sight check from the mine to the target.

**Being shot.** An explosion nearby sets the Claymore off. Other damage destroys it, because its health is 1 HP.

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

- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): placement, trigger box, arming delay and destruction rules
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): Claymore actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
