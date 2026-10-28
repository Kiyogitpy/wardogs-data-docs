---
title: Level 4 Helmet
parent: "Equipment"
group: "Armor"
description: "Top helmet tier: 60% reduction for the head and neck, 200 durability, 4,500 cash in Season 2, strongly muffles nearby sound."
---

# Level 4 Helmet

| Level 4 Helmet | |
|---|---|
| ![Level 4 Helmet]({{ '/assets/img/icons/vendor-gear/T_UI_Vendor_Helmet_004a.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Helmet |
| Slot | Helmet |
| Weight | 4.5 kg |
| **Protection** | |
| Damage reduction | 60% (65% in Season 1) |
| Body parts covered | Head and neck |
| Durability | 200 |
| **Availability** | |
| Price | 4,500 cash (3,000 in Season 1) |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_SuperHeavyHelmet` (item `Id.Item.SuperHeavyHelmet`) |
{: .wiki-infobox }

Level 4 Helmet is the top helmet tier. It protects the head and neck and cuts damage there by 60%. It also strongly muffles the sounds around the wearer. It costs 4,500 cash in Season 2 and needs no unlock.

## Overview

The Item Shop describes the Level 4 Helmet as "Very High Damage Reduction", with "High Suppression Reduction" and a strong muffling of nearby sound. The listed areas are the head and neck.

It goes in the Helmet slot and weighs 4.5. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

Level 4 Helmet reduces damage to the head and neck by 60%. It does nothing for the body. It has 200 durability, the highest of the helmets.

With M4 full-metal-jacket rounds:

- Head: 65.8 HP with no helmet, 26.3 HP with Level 4 Helmet.
- Neck: 49.4 HP with no helmet, 19.7 HP with Level 4 Helmet.

| Helmet | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Helmet](level-1-helmet.md) | 30% | Head | 80 |
| [Level 2 Helmet](level-2-helmet.md) | 40% | Head | 100 |
| [Level 3 Helmet](level-3-helmet.md) | 50% | Head and neck | 180 |
| **Level 4 Helmet** | 60% | Head and neck | 200 |
| [Pilot Helmet](pilot-helmet.md) | 30% | Head | 180 |
| [Tank Helmet](tank-helmet.md) | 55% | Head and neck | 180 |

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

## Season 2 changes

| Property | Season 1 | Season 2 |
|---|---|---|
| Damage reduction | 65% | 60% |
| Price | 3,000 cash | 4,500 cash |

Only these two changes are listed for this helmet in Season 2.

## See also

- [Body Armor](body-armor.md)
- [Level 1 Helmet](level-1-helmet.md), [Level 2 Helmet](level-2-helmet.md), [Level 3 Helmet](level-3-helmet.md)
- [Pilot Helmet](pilot-helmet.md), [Tank Helmet](tank-helmet.md)
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock, durability, reduction and covered body parts
- [Items data](../../content/Wardogs_Items_v2.md): weight and item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): M4 damage by body part with and without armor
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): covered body parts and reduction per armor item
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): reduction and price changes
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): slot and category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): durability per piece, the armour damage rule and the helmet weights
