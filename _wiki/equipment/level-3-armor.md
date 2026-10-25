---
title: Level 3 Armor
parent: "Equipment"
group: "Armor"
description: "Third vest tier: 50% damage reduction on the torso, 250 durability, 2,500 cash in Season 2."
---

# Level 3 Armor

| Level 3 Armor | |
|---|---|
| **General** | |
| Type | Vest |
| Slot | Armor |
| Weight | 10.5 kg |
| **Protection** | |
| Damage reduction | 50% (55% in Season 1) |
| Body parts covered | Torso: upper, middle and lower |
| Durability | 250 |
| **Availability** | |
| Price | 2,500 cash (2,000 in Season 1) |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_HeavyArmor` (item `Id.Item.HeavyArmor`) |
{: .wiki-infobox }

Level 3 Armor is the third of the four vests. It protects the upper, middle and lower torso and cuts damage there by 50%. In Season 2 its reduction went down and its price went up. It needs no unlock.

## Overview

Level 3 Armor is one step below [Level 4 Armor](level-4-armor.md). The Item Shop describes it as "High Damage Reduction" and says it protects the upper and lower torso. The item data lists the upper, middle and lower torso.

It goes in the Armor slot and covers nothing below the torso. With a weight of 10.5, it is much heavier than the two lower tiers. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

Level 3 Armor reduces damage at the upper, middle and lower torso by 50%. It does nothing for other body parts. The item data gives it 250 durability.

With M4 full-metal-jacket rounds, an upper torso hit does 27.3 HP with no armor and 13.6 HP with Level 3 Armor.

| Vest | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Armor](level-1-armor.md) | 30% | Torso (upper, middle, lower) | 200 |
| [Level 2 Armor](level-2-armor.md) | 40% | Torso (upper, middle, lower) | 220 |
| **Level 3 Armor** | 50% | Torso (upper, middle, lower) | 250 |
| [Level 4 Armor](level-4-armor.md) | 60% | Torso, pelvis, upper arms | 300 |

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

## Season 2 changes

| Property | Season 1 | Season 2 |
|---|---|---|
| Damage reduction | 55% | 50% |
| Price | 2,000 cash | 2,500 cash |

The Season 2 data lists only these two changes for this vest.

## See also

- [Body Armor](body-armor.md)
- [Level 1 Armor](level-1-armor.md), [Level 2 Armor](level-2-armor.md), [Level 4 Armor](level-4-armor.md)
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
