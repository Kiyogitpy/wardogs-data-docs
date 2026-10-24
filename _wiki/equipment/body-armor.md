---
title: Body Armor
parent: "Equipment"
group: "Armor"
description: "Vests and helmets: four tiers, the body parts each one covers, their damage reduction, durability, weight and price."
---

# Body Armor

| Body armor | |
|---|---|
| Kinds | Vest (torso), helmet (head) |
| Tiers | 4 levels, plus Pilot and Tank helmets |
| Vest reduction | 30% to 60% |
| Helmet reduction | 30% to 60%; Tank helmet 55% |
| Not covered by any armor | Lower arms, hands, legs |
{: .wiki-infobox }

Body armor is worn in two separate slots. A vest protects the torso, and on the top tier also the pelvis and upper arms. A helmet protects the head, and on the higher tiers also the neck. Each piece cuts incoming damage at the body parts it covers by a fixed percentage. A vest and a helmet never cover the same body part, so only one piece of armor applies to a hit.

## Overview

The armor levels are named by tier in the game. The vests are the "Level 1" to "Level 4" armors, and the helmets are the "Level 1" to "Level 4" helmets, with the Pilot and Tank helmets as separate pieces. The Ghillie suit and Ghillie headwear are camouflage. The data gives them no damage reduction.

Tactical vests are a different item. They add quick slots and do not protect against damage. See [Utility Items](utility-items.md).

## Individual items

Each vest and helmet has its own article.

- Vests: [Level 1 Armor](level-1-armor.md), [Level 2 Armor](level-2-armor.md), [Level 3 Armor](level-3-armor.md), [Level 4 Armor](level-4-armor.md)
- Helmets: [Level 1 Helmet](level-1-helmet.md), [Level 2 Helmet](level-2-helmet.md), [Level 3 Helmet](level-3-helmet.md), [Level 4 Helmet](level-4-helmet.md), [Pilot Helmet](pilot-helmet.md), [Tank Helmet](tank-helmet.md)
- Camouflage: [Ghillie Body Suit](ghillie-body-suit.md), [Ghillie Headwear](ghillie-headwear.md)

## Effects

### Vests

| Item | Reduction | Covers | Durability | Weight | Price (cash) |
|---|---:|---|---:|---:|---:|
| Level 1 Armor | 30% | Torso (lower, middle, upper) | 200 | 3 | 400 |
| Level 2 Armor | 40% | Torso (lower, middle, upper) | 220 | 4.5 | 1,000 |
| Level 3 Armor | 50% | Torso (lower, middle, upper) | 250 | 10.5 | 2,500 |
| Level 4 Armor | 60% | Torso, pelvis, upper arms | 300 | 18 | 5,000 |

### Helmets

| Item | Reduction | Covers | Durability | Weight | Price (cash) | Notes |
|---|---:|---|---:|---:|---:|---|
| Level 1 Helmet | 30% | Head | 80 | - | 200 | |
| Level 2 Helmet | 40% | Head | 100 | 1.6 | 500 | |
| Level 3 Helmet | 50% | Head and neck | 180 | 3 | 2,000 | Low suppression reduction |
| Level 4 Helmet | 60% | Head and neck | 200 | 4.5 | 4,500 | High suppression reduction; strongly muffles nearby sound |
| Pilot Helmet | 30% | Head | 180 | - | not sold (data value 6,400) | Muffles vehicle audio; highlights target vehicles |
| Tank Helmet | 55% | Head and neck | 180 | - | not sold (data value 5,000) | Muffles vehicle and infantry audio; removes suppression and tinnitus |

The Pilot and Tank helmets are marked as hidden in the shop data, so they do not appear in the shop listing. The data values are shown for reference.

### What the reduction does

The reduction is applied to each hit at a covered body part. Taking the M4 with full-metal-jacket rounds as an example, the table below shows the damage per hit in HP at each location. Each cell is the damage with no armor, then with the armor level that covers that location. "No cover" means no armor of that level covers the location.

| Body part | No armor | Level 1 | Level 2 | Level 3 | Level 4 |
|---|---:|---:|---:|---:|---:|
| Head | 65.8 | 46.1 (helmet) | 39.5 (helmet) | 32.9 (helmet) | 26.3 (helmet) |
| Neck | 49.4 | no cover | no cover | 24.7 (helmet) | 19.7 (helmet) |
| Torso, upper | 27.3 | 19.1 (vest) | 16.4 (vest) | 13.6 (vest) | 10.9 (vest) |
| Torso, middle | 27.2 | 19.0 (vest) | 16.3 (vest) | 13.6 (vest) | 10.9 (vest) |
| Torso, lower | 25.8 | 18.1 (vest) | 15.5 (vest) | 12.9 (vest) | 10.3 (vest) |
| Pelvis | 25.2 | no cover | no cover | no cover | 10.1 (vest) |
| Upper arm | 15.1 | no cover | no cover | no cover | 6.0 (vest) |
| Lower arm | 12.6 | no cover | no cover | no cover | no cover |
| Hand | 7.6 | no cover | no cover | no cover | no cover |
| Thigh | 15.1 | no cover | no cover | no cover | no cover |
| Calf | 12.6 | no cover | no cover | no cover | no cover |
| Foot | 7.6 | no cover | no cover | no cover | no cover |

Read the table as: a Level 3 vest turns a 27.3 HP upper-torso hit into 13.6 HP. Each weapon and ammunition type has its own numbers, so the M4 values are an example, not a rule. The full per-weapon tables are on the [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) data page.

**Lower arms, hands and legs have no armor.** No vest or helmet covers them in the data. A hit there takes the full damage listed in the no-armor column.

### Durability

Each armor piece has a durability value, and the data gives each one four durability stages. All four stages list the same reduction, so the data does not show protection dropping as the armor takes hits. How durability is used up is not yet known.

## Use and timing

Armor fills the vest and helmet slots. The data has one armor slot and one helmet slot, so two vests or two helmets are not worn together. The data gives no time to put armor on or take it off, so that is not yet known.

## Cost

Prices are in the tables above. The Level 1 and Level 2 pieces cost 200 to 1,000 cash. The Level 4 vest costs 5,000 cash, and the Level 4 helmet 4,500 cash. The Ghillie Body Suit costs 3,000 cash, and the data gives no damage reduction for it or for the Ghillie headwear.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---|---|
| Level 3 Armor reduction | 55% | 50% |
| Level 4 Armor reduction | 65% | 60% |
| Level 3 Helmet reduction | 55% | 50% |
| Level 4 Helmet reduction | 65% | 60% |
| Level 3 Armor price | 2,000 | 2,500 |
| Level 4 Armor price | 4,000 | 5,000 |
| Level 3 Helmet price | 1,500 | 2,000 |
| Level 4 Helmet price | 3,000 | 4,500 |

The Level 1 and Level 2 armor and helmets, and the Pilot and Tank helmets, did not change in the Season 2 data.

## See also

- [Medical Items](medical-items.md)
- [Utility Items](utility-items.md), including the Tactical Vests, which are not armor
- [Grenades and Explosives](grenades-and-explosives.md)
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Health and Damage](../game-mechanics/health-and-damage.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, armor stages, weights and covered body parts
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): armor coverage by body part and the M4 damage table
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): armor reduction and price changes
