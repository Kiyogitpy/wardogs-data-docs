---
title: "Shops"
parent: "Progression & Economy"
group: "Economy"
description: "Where to buy gear, weapons, vehicles and supply crates, what each listing costs, and how unlock levels and buy limits work."
---

# Shops

| Shops | |
|---|---|
| Shop kinds | Gear and utility shop, weapon shop, vehicle and garage shop, Gold Market |
| Currency | Cash for most listings; Gold Bars for cosmetics |
| Unlock levels | Most listings are level 1; some are level 0 |
| Internal name | Vendor data tables (one per shop) |
{: .wiki-infobox }

Players buy gear, weapons, vehicles and supply crates from vendors inside a match or from the frontend. Each listing has a price, an unlock level, optional required items, and an optional buy limit. Cosmetics are sold separately on the Gold Market, priced in Gold Bars.

## Overview

| Shop | What it sells | Examples |
|---|---|---|
| Gear | Armor, vests, backpacks and parachutes | Scout Backpack, Ruck Backpack |
| Utility | Medical items, batteries, tools, throwables, mines and explosives | Bandage, Defibrillator, Battery |
| Weapon | Weapons, attachments, magazines and ammunition | AK74, M4, T-21, Galil |
| Vehicle and garage | Vehicles, vehicle supply crates and pallets | Havoc, MH-6, Z20 Lakota, supply crates |
| Gold Market | Cosmetics: skins, emotes and similar | Skins and emotes, priced in Gold Bars |

The weapon listings are on the weapon shop data page. Gear, medical items and vehicles are on the item shop data page.

## How it works

- **Price.** Each listing has one price. The vendor rows do not name a currency. The Season 2 unlock tree lists its costs in cash, so vendor prices are most likely cash, but the data does not state it outright.
- **Unlock level.** Each listing has an unlock level. Most listings are level 1 and some are level 0. The data does not say which level counts (for example the role level or the account level).
- **Required items.** Some listings need other items first. The data records these; the sample listings below show none.
- **Buy limit.** Some listings have a lifetime buy limit. Where the data shows none, the listing has no limit.
- **Amount.** Each purchase is one stack of the listing's amount. Most listings buy one item.
- **Hidden prices.** Some listings have hidden price points that the vendor does not show. The data marks these "(hidden)".

## Numbers

### Gear

| Item | Price | Unlock level |
|---|---|---|
| Small Tac Vest | 100 | 1 |
| Medium Tac Vest | 250 | 1 |
| Large Tac Vest | 400 | 1 |
| Pouch | 0 | 1 |
| Scout Backpack | 350 | 1 |
| Field Backpack | 650 | 1 |
| Operator Backpack | 800 | 1 |
| Ruck Backpack | 1,600 | 1 |
| Sport parachute | 700 | 0 |

### Utility and medical

| Item | Price | Unlock level |
|---|---|---|
| Bandage | 200 | 1 |
| Individual First Aid Kit | 800 | 1 |
| Defibrillator | 1,600 | 0 |
| Medical Bag | 1,800 | 0 |
| Battery | 150 | 1 |

### Weapons

| Weapon | Price | Unlock level |
|---|---|---|
| GGX 17 (pistol) | 200 | 1 |
| Judge | 250 | 1 |
| T-21 | 1,200 | 1 |
| AK74 | 800 | 1 |
| Galil | 2,000 | 1 |
| M4 | 2,800 | 1 |
| FAL | 6,000 | 1 |
| A-91, KH-2002 and Bushmaster M17S | 0 | 1 |

Attachments, magazines and the rest of the weapon catalogue are on the weapon shop data page.

### Vehicles and supply crates

| Item | Price | Unlock level |
|---|---|---|
| MH-6 (helicopter) | 6,250 | 1 |
| AH-6M [Miniguns] | 12,000 | 1 |
| AH-6R [Rockets] | 18,800 | 1 |
| Z20 Lakota (transport helicopter) | 7,400 | 0 |
| Z20 Lakota, miniguns | 15,000 | 0 |
| Havoc (attack helicopter) | 28,000 | 0 |
| Small crate | 150 | 0 |
| Large crate | 300 | 0 |
| Small armored crate | 500 | 0 |
| Large armored crate | 800 | 0 |
| Supply pallets (build, ammunition, fuel, mechanical) | 400 each | 0 |

The vehicle market table has no rows of its own; vehicle listings sit in per-vehicle tables.

### Unlocks through role trees

Some items are unlocked through a role's unlock tree rather than bought from a vendor. In Season 2 the tree's cash costs changed for many items. Examples from the Season 2 changes:

- A GGX 17 pistol in the Wardog tree went from 5,000 to 15,000 cash.
- A Humvee in the Driver tree went from 25,000 to 75,000 cash.
- Some Medic items went up: a Medic magazine from 10,000 to 50,000 cash, and a Defibrillator from 50,000 to 110,000 cash.
- Some items went down: a Medic magazine went from 50,000 to 15,000 cash, and a Medic weapon from 75,000 to 25,000 cash.

The full tree is not in the sources, so this page does not list every unlock.

## Tips that follow from the numbers

- Gear is cheap next to weapons. A Ruck Backpack (1,600) costs less than a Galil (2,000) or an M4 (2,800).
- A Bandage costs 200, and a heal with one pays the healer 400 in cash. A Defibrillator costs 1,600, and a revive with one pays the reviver 1,000 in cash.
- Armored supply crates cost 500 and 800, against 150 and 300 for plain crates. Both are on the same vendor list.

## Season 2 changes

- Many unlock-tree cash costs changed, with level gates changed for more than a hundred nodes. The examples above are from that list. See the Season 2 Rewards & Unlocks page for the full set.

## See also

- [Cash and Rewards](cash-and-rewards.md)
- [Factory Investment](factory-investment.md), which produces some weapons
- [Cosmetics](cosmetics.md), which are sold for Gold Bars
- [Skills](skills.md)
- [Weapons](../weapons.md)
- [Body armor](../equipment/body-armor.md)
- [Medical Items](../equipment/medical-items.md)
- [Vehicles](../vehicles.md)

## Sources

- [Item shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Weapon shop](../../game-features/Wardogs_WeaponShop_v1.md)
- [Progression tables](../../game-features/Wardogs_Progression_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
