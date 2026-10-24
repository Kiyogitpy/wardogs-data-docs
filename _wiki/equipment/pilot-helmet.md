---
title: Pilot Helmet
parent: "Equipment"
group: "Armor"
description: "Vehicle-use helmet: 30% head damage reduction, muffles vehicle audio, highlights target vehicles. Not sold in the shop."
---

# Pilot Helmet

| Pilot Helmet | |
|---|---|
| **General** | |
| Type | Helmet |
| Slot | Helmet |
| Weight | Not yet known |
| **Protection** | |
| Damage reduction | 30% |
| Body parts covered | Head |
| Durability | 180 |
| **Availability** | |
| Price | Not sold (hidden in the shop; the data lists 6,400 cash) |
| Unlock | Not applicable |
| **Reference** | |
| Internal name | `ID_PilotHelmet` (item `Id.Item.PilotHelmet`) |
{: .wiki-infobox }

The Pilot Helmet protects the head with a 30% reduction, the same as the [Level 1 Helmet](level-1-helmet.md). It also has two vehicle effects: it muffles vehicle audio and highlights target vehicles. The shop data marks it as hidden, so it is not sold in the shop.

## Overview

The Item Shop describes the Pilot Helmet as "Low Damage Reduction" and lists the two vehicle effects. The shop files it under "Vehicle Use" rather than "Armor". It is still an armor item in the item data, and it goes in the Helmet slot.

The item data gives no weight, so the weight is not yet known. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The Pilot Helmet reduces damage to the head by 30%. It covers the head only, not the neck. The item data gives it 180 durability.

With M4 full-metal-jacket rounds, a head hit does 65.8 HP with no helmet and 46.1 HP with the Pilot Helmet. That is the same as with the Level 1 Helmet.

| Helmet | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Helmet](level-1-helmet.md) | 30% | Head | 80 |
| [Level 2 Helmet](level-2-helmet.md) | 40% | Head | 100 |
| [Level 3 Helmet](level-3-helmet.md) | 50% | Head and neck | 180 |
| [Level 4 Helmet](level-4-helmet.md) | 60% | Head and neck | 200 |
| **Pilot Helmet** | 30% | Head | 180 |
| [Tank Helmet](tank-helmet.md) | 55% | Head and neck | 180 |

The data gives four durability stages, and all four list the same reduction. How durability is used up is not yet known.

The vehicle effects are not compared with a number in the data. How strong the audio muffling or the target highlight is, is not yet known.

## Season 2 changes

The Season 2 data does not change the Pilot Helmet.

## See also

- [Body Armor](body-armor.md)
- [Tank Helmet](tank-helmet.md), a vehicle-use helmet with more reduction
- [Level 1 Helmet](level-1-helmet.md), the helmet with the same reduction
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price (hidden), reduction, durability, covered body parts and effects
- [Items data](../../content/Wardogs_Items_v2.md): item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): M4 damage by body part with and without armor
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): covered body parts and reduction per armor item
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): category names
- [Body Armor](body-armor.md): the overview of all armor
