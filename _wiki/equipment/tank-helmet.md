---
title: Tank Helmet
parent: "Equipment"
group: "Armor"
description: "Vehicle-use helmet: 55% reduction for the head and neck, removes suppression and tinnitus. Not sold in the shop."
---

# Tank Helmet

| Tank Helmet | |
|---|---|
| **General** | |
| Type | Helmet |
| Slot | Helmet |
| Weight | 1 kg |
| **Protection** | |
| Damage reduction | 55% |
| Body parts covered | Head and neck |
| Durability | 180 |
| **Availability** | |
| Price | Not sold (hidden in the shop; the data lists 5,000 cash) |
| Unlock | Not applicable |
| **Reference** | |
| Internal name | `ID_TankHelmet` (item `Id.Item.TankHelmet`) |
{: .wiki-infobox }

The Tank Helmet has a 55% reduction for the head and neck, which is between the [Level 3 Helmet](level-3-helmet.md) (50%) and the [Level 4 Helmet](level-4-helmet.md) (60%). It also muffles vehicle and infantry audio, and removes suppression and tinnitus. The shop data marks it as hidden, so it is not sold in the shop.

## Overview

The Item Shop describes the Tank Helmet as "High Damage Reduction", and lists the audio and suppression effects. The shop files it under "Vehicle Use" rather than "Armor". It goes in the Helmet slot.

The item data omits the weight, so the game's default of 1 applies. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The Tank Helmet reduces damage to the head and neck by 55%. It does nothing for the body. The item data gives it 180 durability.

With M4 full-metal-jacket rounds:

- Head: 65.8 HP with no helmet, 29.6 HP with the Tank Helmet.
- Neck: 49.4 HP with no helmet, 22.2 HP with the Tank Helmet.

| Helmet | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Helmet](level-1-helmet.md) | 30% | Head | 80 |
| [Level 2 Helmet](level-2-helmet.md) | 40% | Head | 100 |
| [Level 3 Helmet](level-3-helmet.md) | 50% | Head and neck | 180 |
| [Level 4 Helmet](level-4-helmet.md) | 60% | Head and neck | 200 |
| [Pilot Helmet](pilot-helmet.md) | 30% | Head | 180 |
| **Tank Helmet** | 55% | Head and neck | 180 |

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

Suppression on the wearer is set per bullet class (0.2 for small pistol rounds to 0.9 for 120 mm and larger), and the shop text says the Tank Helmet removes it. How much the audio muffling reduces sound is not measured in the data.

## Season 2 changes

The Season 2 data does not change the Tank Helmet.

## See also

- [Body Armor](body-armor.md)
- [Pilot Helmet](pilot-helmet.md), the other vehicle-use helmet
- [Level 3 Helmet](level-3-helmet.md) and [Level 4 Helmet](level-4-helmet.md), the armor helmets with the nearest reduction
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price (hidden), reduction, durability, covered body parts and effects
- [Items data](../../content/Wardogs_Items_v2.md): item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): M4 damage by body part with and without armor, including the Tank column
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): covered body parts and reduction per armor item
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): durability per piece, the armour damage rule and the helmet weights
