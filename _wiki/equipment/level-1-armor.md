---
title: Level 1 Armor
parent: "Equipment"
group: "Armor"
description: "The lightest vest in the Armor group: 30% damage reduction on the torso, 200 durability, 400 cash."
---

# Level 1 Armor

| Level 1 Armor | |
|---|---|
| ![Level 1 Armor]({{ '/assets/img/icons/vendor-gear/T_UI_Vendor_Armor_001a.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Vest |
| Slot | Armor |
| Weight | 3 kg |
| **Protection** | |
| Damage reduction | 30% |
| Body parts covered | Torso: upper, middle and lower |
| Durability | 200 |
| **Availability** | |
| Price | 400 cash |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | [`ID_LightArmor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_LightArmor.json) (item `Id.Item.LightArmor`) |
{: .wiki-infobox }

Level 1 Armor is the lightest of the four vests and the cheapest of them. It protects the upper, middle and lower torso and cuts damage there by 30%. It needs no unlock, so it can be bought from the start.

## Overview

Level 1 Armor is the first vest tier. The Item Shop describes it as "Low Damage Reduction" and says it protects the upper and lower torso. Three torso areas are listed, upper, middle and lower, so the middle torso is covered as well.

The vest goes in the Armor slot, and it does not cover the pelvis, arms or legs. Tactical vests are a different item. They are in the Tac-Vest slot, add quick slots and give no protection. For how armor is applied to a hit, see [Armor](../game-mechanics/armor.md). For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

Level 1 Armor reduces damage taken at the upper, middle and lower torso by 30%. It does nothing for the head, neck, pelvis, arms or legs. It has 200 durability.

In the point-blank damage model, M4 full-metal-jacket rounds deal 30.8 HP to an unarmored upper torso and 21.6 HP with Level 1 Armor. This assumes a hostile target outside a vehicle, no penetration and the historical damage formula applied to S3 inputs.

| Vest | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| **Level 1 Armor** | 30% | Torso (upper, middle, lower) | 200 |
| [Level 2 Armor](level-2-armor.md) | 40% | Torso (upper, middle, lower) | 220 |
| [Level 3 Armor](level-3-armor.md) | 50% | Torso (upper, middle, lower) | 250 |
| [Level 4 Armor](level-4-armor.md) | 60% | Torso, pelvis, upper arms | 300 |

The S3 item lists the same reduction at all four durability stages. Earlier CL516586 code removed 0.4 times incoming bullet damage from durability and broke the piece at zero. That wear and break behavior has not been traced in the current S3 build; equal stored stages alone do not establish protection until breakage.

## Season 2 changes

Level 1 Armor did not change in Season 2.

## See also

- [Body Armor](body-armor.md)
- [Level 2 Armor](level-2-armor.md), [Level 3 Armor](level-3-armor.md), [Level 4 Armor](level-4-armor.md)
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
