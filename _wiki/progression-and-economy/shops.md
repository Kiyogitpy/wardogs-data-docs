---
title: "Shops"
parent: "Progression & Economy"
group: "Economy"
description: "Where to buy gear, weapons, vehicles and supply crates, what each listing costs, how discounts apply, and how buy limits work."
---

# Shops

| Shops | |
|---|---|
| Shop kinds | Gear and utility shop, weapon shop, vehicle and garage shop, Gold Market |
| Currency | Cash for most listings; Gold Bars for cosmetics |
| Gates | Wardog or role level, and required items. Shop unlock levels are 0 or 1 and gate nothing |
| Internal name | Vendor data tables (one per shop) |
{: .wiki-infobox }

Players buy gear, weapons, vehicles and supply crates from vendors inside a match or from the frontend. Each listing has a price, optional required items, and an optional buy limit. Cosmetics are sold separately on the Gold Market, priced in Gold Bars.

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
- **Price modifiers.** Each price is multiplied by every discount that applies. A discount is a percentage: 50% halves the price and 90% takes 10% off. The discounts in the game's economy settings are:
  - Wardog level 8 or below: 50%.
  - The losing faction, when it trails by 40 points: 80%. The condition is read from the setting's field names.
  - A first purchase: 90%.
  - The signature rifle of a faction is free (0%) for that faction. See [Factions](../game-modes-and-maps/factions.md).

  Derived example: an AK74 (800 cash) bought as a first purchase by a Wardog level 8 player costs 360 (800 x 0.5 x 0.9), before any other discount.
- **Refunds.** A refund pays 90% of the smaller of what was spent on the refunded items and the eligible purchase amount. It must be claimed within 20 score ticks, a window set in the economy settings.
- **Gating.** Shops gate listings by Wardog level or role level and by required items. The unlock level field in the vendor data is 0 or 1 on every listing and gates nothing.
- **Required items.** Some listings need other items first. The data records these; the sample listings below show none.
- **Buy limit.** Some listings have a lifetime buy limit. Where the data shows none, the listing has no limit.
- **Amount.** Each purchase is one stack of the listing's amount. Most listings buy one item.
- **Hidden variations.** 343 of the 670 vendor variations in the data are hidden from the shop panels, mostly ammunition and magazine variants. They are filtered out of the vendor lists, so the tables here show only the visible listings.

## Numbers

### Gear

| Item | Price |
|---|---|
| Small Tac Vest | 100 |
| Medium Tac Vest | 250 |
| Large Tac Vest | 400 |
| Pouch | 0 |
| Scout Backpack | 350 |
| Field Backpack | 650 |
| Operator Backpack | 800 |
| Ruck Backpack | 1,600 |
| Sport parachute | 700 |

### Utility and medical

| Item | Price |
|---|---|
| Bandage | 200 |
| Individual First Aid Kit | 800 |
| Defibrillator | 1,600 |
| Medical Bag | 1,800 |
| Battery | 150 |

### Weapons

| Weapon | Price |
|---|---|
| GGX 17 (pistol) | 200 |
| Judge | 250 |
| T-21 | 1,200 |
| AK74 | 800 |
| Galil | 2,000 |
| M4 | 2,800 |
| FAL | 6,000 |
| A-91, KH-2002 and Bushmaster M17S | 0 |

Attachments, magazines and the rest of the weapon catalogue are on the weapon shop data page. The shop lists 0 for the three signature rifles. Each one is free for its own faction: Bushmaster M17S for Lonestar, A-91 for Valkyra and KH-2002 for Manticore.

### Vehicles and supply crates

| Item | Price |
|---|---|
| MH-6 (helicopter) | 6,250 |
| AH-6M [Miniguns] | 12,000 |
| AH-6R [Rockets] | 18,800 |
| Z20 Lakota (transport helicopter) | 7,400 |
| Z20 Lakota, miniguns | 15,000 |
| Havoc (attack helicopter) | 28,000 |
| Small crate | 150 |
| Large crate | 300 |
| Small armored crate | 500 |
| Large armored crate | 800 |
| Supply pallets (build, ammunition, fuel, mechanical) | 400 each |

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
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Price modifiers (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/price-modifiers.json)
- [Vendor variation flags (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vendor-flags.json)
- [Round 43 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md)
- [Round 44 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round44-econ-buildables.md)
