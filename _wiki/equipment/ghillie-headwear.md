---
title: Ghillie Headwear
parent: "Equipment"
group: "Armor"
description: "Camouflage headwear for 2,500 cash, worn with the Ghillie Body Suit. It has no durability and gives no protection."
---

# Ghillie Headwear

| Ghillie Headwear | |
|---|---|
| **General** | |
| Type | Camouflage headwear |
| Slot | Helmet |
| Weight | 1 kg |
| **Protection** | |
| Damage reduction | None |
| Body parts covered | None |
| Durability | None (no durability fragment) |
| **Availability** | |
| Price | 2,500 cash |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_GhillieHelmet` (item `Id.Item.GhillieHelmet`) |
{: .wiki-infobox }

Ghillie Headwear is camouflage for the head. It must be worn with the [Ghillie Body Suit](ghillie-body-suit.md). Like the suit, it removes the death cam after the wearer kills an enemy, and it hides the wearer from infrared range finders. It gives no protection and has no durability.

## Overview

The shop groups the Ghillie Headwear under "Camouflage" and lists it as armor. It goes in the Helmet slot.

The Item Shop also lists a "Ghillie Headwear (Dead)" at 2,800 cash. The data does not say how it differs from this item. The item data omits the weight, so the game's default of 1 applies. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The headwear has no durability, covers no body parts and gives no protection. The game's armor damage table sets the armor damage of this piece to zero, so it never reduces a hit and takes no armor damage (read from the game data; the game was not run to confirm it). The Weapon Damage page therefore treats it as no armor.

| Piece | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| **Ghillie Headwear** | None | None | None |
| [Level 1 Helmet](level-1-helmet.md) | 30% | Head | 80 |

## Effects when worn together

The suit and the headwear work as a pair. The effects below apply only when both pieces are worn:

| Effect | Change |
|---|---|
| Aim down sights time | 20% faster (multiplier 0.8) |
| Aim sway | 15% more (multiplier 1.15) |
| Lean and unlean time | 15% slower (multiplier 1.15) |
| Move speed | 5% slower (multiplier 0.95) |
| Jump velocity | 5% lower (multiplier 0.95) |

The armor damage table has rows for the suit and headwear tags that take their armor damage to zero, so the set takes no armor damage and gives no reduction.

## Season 2 changes

The Season 2 data does not list a change for the Ghillie Headwear.

## See also

- [Body Armor](body-armor.md)
- [Ghillie Body Suit](ghillie-body-suit.md), the body piece worn with this item
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock and effects
- [Items data](../../content/Wardogs_Items_v2.md): item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): how the damage tables treat the Ghillie items
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): no reduction and no covered body parts in the item data
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): the combined effect of the Ghillie headwear and suit.
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): the armor damage rows and the set bonus values.
