---
title: Ghillie Body Suit
parent: "Equipment"
group: "Armor"
description: "Camouflage suit for 3,000 cash, worn with Ghillie Headwear. It has no durability and gives no protection."
---

# Ghillie Body Suit

| Ghillie Body Suit | |
|---|---|
| **General** | |
| Type | Camouflage suit |
| Slot | Armor |
| Weight | 1.5 kg |
| **Protection** | |
| Damage reduction | None |
| Body parts covered | None |
| Durability | None (no durability fragment) |
| **Availability** | |
| Price | 3,000 cash |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | `ID_GhillieArmor` (item `Id.Item.GhillieArmor`) |
{: .wiki-infobox }

The Ghillie Body Suit is camouflage that goes in the Armor slot. It must be worn with [Ghillie Headwear](ghillie-headwear.md). It removes the death cam after the wearer kills an enemy, and it hides the wearer from infrared range finders. It gives no protection and has no durability. The suit's strips sway on a soft spring (damping 0.25, stiffness 0.1), so they trail behind movement and settle slowly. This comes from the animation setup and has not been checked in play.

## Overview

The shop groups the Ghillie Body Suit under "Camouflage". Its two listed effects are the removal of the death cam after a kill and protection from infrared range finders.

The Item Shop also lists a "Ghillie Body Suit (Dead)" at 3,500 cash. It is a separate item with the same effects and no durability. It differs in its look: its material is a dead-plant (dry) camouflage, and it costs more. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The suit has no durability, covers no body parts and gives no protection. The game's armor damage table sets the armor damage of this piece to zero, so it never reduces a hit and takes no armor damage (read from the game data; the game was not run to confirm it). The Weapon Damage page therefore treats it as no armor.

| Piece | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| **Ghillie Body Suit** | None | None | None |
| [Level 1 Armor](level-1-armor.md) | 30% | Torso (upper, middle, lower) | 200 |

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

The Season 2 data does not list a change for the Ghillie Body Suit.

## See also

- [Body Armor](body-armor.md)
- [Ghillie Headwear](ghillie-headwear.md), the head piece worn with this suit
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock and effects
- [Items data](../../content/Wardogs_Items_v2.md): weight and item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): how the damage tables treat the Ghillie items
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): no reduction and no covered body parts in the item data
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): the combined effect of the Ghillie suit and headwear.
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): the armor damage rows and the set bonus values.
