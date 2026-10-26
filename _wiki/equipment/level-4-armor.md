---
title: Level 4 Armor
parent: "Equipment"
group: "Armor"
description: "Top vest tier: 60% damage reduction on the torso, pelvis and upper arms, 300 durability, 5,000 cash."
---

# Level 4 Armor

| Level 4 Armor | |
|---|---|
| ![Level 4 Armor]({{ '/assets/img/icons/vendor-gear/T_UI_Vendor_Armor_004a.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Vest |
| Slot | Armor |
| Weight | 18 kg |
| **Protection** | |
| Damage reduction | 60% (65% in Season 1) |
| Body parts covered | Torso (upper, middle, lower), pelvis and upper arms |
| Durability | 300 |
| **Availability** | |
| Price | 5,000 cash (4,000 in Season 1) |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_SuperHeavyArmor` (item `Id.Item.SuperHeavyArmor`) |
{: .wiki-infobox }

Level 4 Armor is the top vest tier. It covers the same torso as the lower tiers, and also the pelvis and upper arms. It cuts damage at those parts by 60%. It is the heaviest vest and costs 5,000 cash.

## Overview

Level 4 Armor is the only vest that protects outside the torso. The Item Shop describes it as "Very High Damage Reduction" and says it protects the upper and lower torso, the upper arms and the pelvis. The item data lists the same areas.

It goes in the Armor slot. The lower arms, hands and legs are not covered. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

Level 4 Armor reduces damage by 60% at the upper, middle and lower torso, the pelvis and the upper arms. The item data gives it 300 durability.

With M4 full-metal-jacket rounds, these hits are reduced as follows:

- Upper torso: 27.3 HP with no armor, 10.9 HP with Level 4 Armor.
- Pelvis: 25.2 HP with no armor, 10.1 HP with Level 4 Armor.
- Upper arm: 15.1 HP with no armor, 6.0 HP with Level 4 Armor.

| Vest | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Armor](level-1-armor.md) | 30% | Torso (upper, middle, lower) | 200 |
| [Level 2 Armor](level-2-armor.md) | 40% | Torso (upper, middle, lower) | 220 |
| [Level 3 Armor](level-3-armor.md) | 50% | Torso (upper, middle, lower) | 250 |
| **Level 4 Armor** | 60% | Torso, pelvis, upper arms | 300 |

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

## Season 2 changes

| Property | Season 1 | Season 2 |
|---|---|---|
| Damage reduction | 65% | 60% |
| Price | 4,000 cash | 5,000 cash |

The Season 2 data lists only these two changes for this vest.

## See also

- [Body Armor](body-armor.md)
- [Level 1 Armor](level-1-armor.md), [Level 2 Armor](level-2-armor.md), [Level 3 Armor](level-3-armor.md)
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
