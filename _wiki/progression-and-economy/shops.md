---
title: "Shops"
parent: "Progression & Economy"
group: "Economy"
description: "Where to buy gear, weapons, vehicles and supply crates, what each listing costs, how discounts apply, and how buy limits work."
---

# Shops

S3 changes the losing-faction comparison to the **first-place faction**, rather than the faction immediately ahead. Low-level catch-up discounts increase week by week per role; no fixed percentage is announced. These are announced gameplay rules, while the saved settings below and historical arithmetic remain separately scoped. See [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221).

| Shops | |
|---|---|
| Shop kinds | Gear and utility shop, weapon shop, vehicle and garage shop, Gold Market |
| Currency | Cash for most listings; Gold Bars for cosmetics |
| Gates | Wardog or role level, and required items. Stored vendor unlock levels are 0 or 1; effective gating remains unverified |
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

- **Price.** Each listing has one price. The vendor rows do not name a currency. The Season 2 unlock tree lists its costs in cash, so vendor prices are most likely cash, but the game does not state it outright.
- **Price modifiers.** The S3 settings store 90 for a tagged first purchase, 80 for a losing-faction modifier with a score difference of 40, and 0 for each faction's signature rifle. Under the earlier pricing model these correspond to 90%, 80% and 0% of the price. Current applicability and stacking still require a current pricing-consumer check.
- **Vendor discount.** The current entry stores no multiplier. It does not establish either a 50% discount for players at level 8 or below or a 100% fallback. A first-purchase price of 45% cannot be derived from this snapshot.

- **Refunds.** The settings store a refund modifier of 0.9 and an eligibility window of 20 score ticks. Ammunition and magazine contexts are blocked. The effective refund calculation and duration of a score tick need current consumer evidence.
- **Gating.** Shops gate listings by Wardog level or role level and by required items. The current vendor-variation output lists unlock levels of 0 or 1; those values alone do not prove that a listing has no gate.
- **Required items.** Some listings need other items first. The game records these; the sample listings below show none.
- **Buy limit.** Some listings have a lifetime buy limit. An omitted limit does not establish unlimited purchases; its effective default is unverified.
- **Amount.** Each purchase is one stack of the listing's amount. Most listings buy one item.
- **Hidden variations.** 344 of the 671 vendor variations are hidden from the shop panels, mostly ammunition and magazine variants. They are filtered out of the vendor lists, so the tables here show only the visible listings.

## Numbers

Prices changed in the [official S3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221): Basic parachute 500→1,250; Sport parachute 700→2,250; Wolf-110 [M2 Browning] 7,800→6,800; Kodiak [M249] 6,750→6,250; AH-6M [Miniguns] 12,000→10,480; Havoc 28,000→26,000 cash. These are announced purchase prices before applicable discounts, separate from role unlock costs.

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
| Basic parachute | 1,250 |
| Sport parachute | 2,250 |

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

Attachments, magazines and the rest of the weapon catalogue are on the weapon shop data page. The shop lists 0 for the three signature rifles. The economy settings pair their zero modifiers with factions: Bushmaster M17S for Lonestar, A-91 for Valkyra and KH-2002 for Manticore. The effective faction restriction and final price need current consumer evidence.

### Vehicles and supply crates

| Item | Price |
|---|---|
| MH-6 (helicopter) | 6,250 |
| AH-6M [Miniguns] | 10,480 |
| AH-6R [Rockets] | 18,800 |
| Z20 Lakota (transport helicopter) | 7,400 |
| Z20 Lakota, miniguns | 15,000 |
| Havoc (attack helicopter) | 26,000 |
| Wolf-110 [M2 Browning] | 6,800 |
| Kodiak [M249] | 6,250 |
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

The current economy output lists 411 unlock nodes across the seven trees. The examples above describe Season 2 changes; current requirements are in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

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
