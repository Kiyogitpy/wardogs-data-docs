---
title: Level 2 Armor
parent: "Equipment"
group: "Armor"
description: "Second vest tier: 40% damage reduction on the torso, 220 durability, 1,000 cash."
---

# Level 2 Armor

| Level 2 Armor | |
|---|---|
| **General** | |
| Type | Vest |
| Slot | Armor |
| Weight | 4.5 |
| **Protection** | |
| Damage reduction | 40% |
| Body parts covered | Torso: upper, middle and lower |
| Durability | 220 |
| **Availability** | |
| Price | 1,000 cash |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_MediumArmor` (item `Id.Item.MediumArmor`) |
{: .wiki-infobox }

Level 2 Armor is the second of the four vests. It protects the upper, middle and lower torso and cuts damage there by 40%. It costs 1,000 cash and needs no unlock.

## Overview

Level 2 Armor sits between [Level 1 Armor](level-1-armor.md) and [Level 3 Armor](level-3-armor.md). The Item Shop describes it as "Medium Damage Reduction" and says it protects the upper and lower torso. The item data lists the upper, middle and lower torso.

It goes in the Armor slot and covers nothing below the torso. Its weight of 4.5 is heavier than Level 1 Armor (3) and lighter than Level 3 Armor (10.5). For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

Level 2 Armor reduces damage at the upper, middle and lower torso by 40%. It does nothing for other body parts. The item data gives it 220 durability.

With M4 full-metal-jacket rounds, an upper torso hit does 27.3 HP with no armor and 16.4 HP with Level 2 Armor.

| Vest | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Armor](level-1-armor.md) | 30% | Torso (upper, middle, lower) | 200 |
| **Level 2 Armor** | 40% | Torso (upper, middle, lower) | 220 |
| [Level 3 Armor](level-3-armor.md) | 50% | Torso (upper, middle, lower) | 250 |
| [Level 4 Armor](level-4-armor.md) | 60% | Torso, pelvis, upper arms | 300 |

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

## Season 2 changes

The Season 2 data does not change Level 2 Armor.

## See also

- [Body Armor](body-armor.md)
- [Level 1 Armor](level-1-armor.md), [Level 3 Armor](level-3-armor.md), [Level 4 Armor](level-4-armor.md)
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock, durability, reduction and covered body parts
- [Items data](../../content/Wardogs_Items_v2.md): weight and item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): M4 damage by body part with and without armor
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): covered body parts and reduction per armor item
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): slot and category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): durability per piece, the armour damage rule and the helmet weights
