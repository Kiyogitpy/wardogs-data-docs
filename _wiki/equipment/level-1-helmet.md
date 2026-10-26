---
title: Level 1 Helmet
parent: "Equipment"
group: "Armor"
description: "Entry helmet: 30% head damage reduction, 80 durability, 200 cash, no neck cover."
---

# Level 1 Helmet

| Level 1 Helmet | |
|---|---|
| ![Level 1 Helmet]({{ '/assets/img/icons/vendor-gear/T_UI_Vendor_Helmet_001a.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Helmet |
| Slot | Helmet |
| Weight | 1 kg |
| **Protection** | |
| Damage reduction | 30% |
| Body parts covered | Head |
| Durability | 80 |
| **Availability** | |
| Price | 200 cash |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_LightHelmet` (item `Id.Item.LightHelmet`) |
{: .wiki-infobox }

Level 1 Helmet is the first of the four helmet tiers. It protects the head and cuts head damage by 30%. It is the cheapest helmet, at 200 cash, and needs no unlock.

## Overview

Level 1 Helmet is the first helmet tier. The Item Shop describes it as "Low Damage Reduction" and says it protects the head. Unlike the higher tiers, it does not cover the neck.

It goes in the Helmet slot. The item data omits the weight, so the game's default of 1 applies. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

Level 1 Helmet reduces damage to the head by 30%. It does nothing for the neck or the body. The item data gives it 80 durability, the lowest of the helmets.

With M4 full-metal-jacket rounds, a head hit does 65.8 HP with no helmet and 46.1 HP with Level 1 Helmet.

| Helmet | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| **Level 1 Helmet** | 30% | Head | 80 |
| [Level 2 Helmet](level-2-helmet.md) | 40% | Head | 100 |
| [Level 3 Helmet](level-3-helmet.md) | 50% | Head and neck | 180 |
| [Level 4 Helmet](level-4-helmet.md) | 60% | Head and neck | 200 |
| [Pilot Helmet](pilot-helmet.md) | 30% | Head | 180 |
| [Tank Helmet](tank-helmet.md) | 55% | Head and neck | 180 |

The [Pilot Helmet](pilot-helmet.md) has the same 30% reduction and covers the same body part, but its durability is 180.

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

## Season 2 changes

The Season 2 data does not change Level 1 Helmet.

## See also

- [Body Armor](body-armor.md)
- [Level 2 Helmet](level-2-helmet.md), [Level 3 Helmet](level-3-helmet.md), [Level 4 Helmet](level-4-helmet.md)
- [Pilot Helmet](pilot-helmet.md), [Tank Helmet](tank-helmet.md)
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock, durability, reduction and covered body parts
- [Items data](../../content/Wardogs_Items_v2.md): item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): M4 damage by body part with and without armor
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): covered body parts and reduction per armor item
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): slot and category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): durability per piece, the armour damage rule and the helmet weights
