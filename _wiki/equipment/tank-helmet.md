---
title: Tank Helmet
parent: "Equipment"
group: "Armor"
description: "Vehicle-use helmet: 55% reduction for the head and neck, removes suppression and tinnitus. Not sold in the shop."
---

# Tank Helmet

| Tank Helmet | |
|---|---|
| ![Tank Helmet]({{ '/assets/img/icons/vendor-gear/T_UI_Gear_TankHelmet.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Helmet |
| Slot | Helmet |
| Weight | 1 kg |
| **Protection** | |
| Damage reduction | 55% |
| Body parts covered | Head and neck |
| Durability | 180 |
| **Availability** | |
| Price | Not sold (hidden in the shop; a price of 5,000 cash is listed) |
| Unlock | Not applicable |
| **Reference** | |
| Internal name | [`ID_TankHelmet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_TankHelmet.json) (item `Id.Item.TankHelmet`) |
{: .wiki-infobox }

The Tank Helmet has a 55% reduction for the head and neck, which is between the [Level 3 Helmet](level-3-helmet.md) (50%) and the [Level 4 Helmet](level-4-helmet.md) (60%). It also muffles vehicle and infantry audio, and removes suppression and tinnitus. The shop data marks it as hidden, so it is not sold in the shop.

## Overview

The Item Shop describes the Tank Helmet as "High Damage Reduction", and lists the audio and suppression effects. The shop files it under "Vehicle Use" rather than "Armor". It goes in the Helmet slot.

The weight is not listed, so the game's default of 1 applies. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The Tank Helmet reduces damage to the head and neck by 55%. It does nothing for the body. It has 180 durability.

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

Suppression on the wearer is set per bullet class (0.2 for small pistol rounds to 0.9 for 120 mm and larger), and the shop text says the Tank Helmet removes it. The audio muffling is set in the game's audio mixes. In the driver or gunner seat of a tracked vehicle, vehicle sound is turned down to a volume setting of 0.63 (about 4 dB quieter) with a low-pass filter setting of 0.6, other players' footsteps get a filter setting of 0.6, other players' gunfire 0.7, and the ringing in the ears (tinnitus) sound is set to 0.50 (about 6 dB quieter). Anywhere else the helmet muffles everything a little, with a low-pass setting of 0.45 on most sounds and 0.5 on your own weapon, the same as the [Pilot Helmet](pilot-helmet.md) does. The filter settings run from 0 (most muffled) to 1 (not muffled) as far as the control names show, and the frequency they work out to is not in the files (inferred).

## Season 2 changes

The Tank Helmet did not change in Season 2.

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
