---
title: Ghillie Headwear
parent: "Equipment"
group: "Armor"
description: "Camouflage headwear for 2,500 cash, worn with the Ghillie Body Suit. Its protection and effective durability are not established for S3."
---

# Ghillie Headwear

| Ghillie Headwear | |
|---|---|
| ![Ghillie Headwear]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Ghillie_Helmet_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Camouflage headwear |
| Slot | Helmet |
| Weight | Not serialized; current default unverified |
| **Protection** | |
| Damage reduction | Not established for S3 |
| Body parts covered | Not serialized |
| Durability | No durability fragment exported; effective behavior unknown |
| **Availability** | |
| Price | 2,500 cash |
| Unlock | None (unlock level 0) |
| **Reference** | |
| Internal name | [`ID_GhillieHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_GhillieHelmet.json) (item `Id.Item.GhillieHelmet`) |
{: .wiki-infobox }

Ghillie Headwear is camouflage for the head. It must be worn with the [Ghillie Body Suit](ghillie-body-suit.md). Like the suit, it removes the death cam after the wearer kills an enemy, and it hides the wearer from infrared range finders. Its exported definition does not establish protection or effective durability.

## Overview

The shop groups the Ghillie Headwear under "Camouflage" and lists it as armor. It goes in the Helmet slot.

The Item Shop also lists a "Ghillie Headwear (Dead)" at 2,800 cash. It is a separate item with the same effects. It differs in its look: its material is a dead-plant (dry) camouflage, and it costs more. The game files omit the weight; the earlier default of 1 has not been verified for S3. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The S3 item omits armor stages and covered locations but references armor and set effects whose definitions are not available in the exported data. Missing fields do not prove zero protection or zero durability. The damage model treats this piece as no armor as an explicit assumption; its actual S3 protection remains unresolved.

| Piece | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| **Ghillie Headwear** | Unknown | Not serialized | Unknown |
| [Level 1 Helmet](level-1-helmet.md) | 30% | Head | 80 |

## Effects when worn together

The suit and the headwear work as a pair. Earlier CL516586 analysis attributed the following effects to wearing both pieces. Their application in S3 remains unverified:

| Effect | Change |
|---|---|
| Aim down sights time | 20% faster (multiplier 0.8) |
| Aim sway | 15% more (multiplier 1.15) |
| Lean and unlean time | 15% slower (multiplier 1.15) |
| Move speed | 5% slower (multiplier 0.95) |
| Jump velocity | 5% lower (multiplier 0.95) |

Armor-damage rules for the camouflage tags do not by themselves establish player-health damage reduction. Resolving protection requires the referenced effects and the current armor application path.

## Season 2 changes

No Season 2 change to the Ghillie Headwear is listed.

## See also

- [Body Armor](body-armor.md)
- [Ghillie Body Suit](ghillie-body-suit.md), the body piece worn with this item
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock and effects
- [Items data](../../content/Wardogs_Items_v2.md): item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): how the damage tables treat the Ghillie items
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): model treatment of omitted coverage, with unresolved protection
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): the combined effect of the Ghillie headwear and suit.
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): the armor damage rows and the set bonus values.
