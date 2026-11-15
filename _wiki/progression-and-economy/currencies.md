---
title: "Currencies"
parent: "Progression & Economy"
group: "Economy"
description: "The money in Wardogs: Cash, Gold Bars and Movember, plus Intel referenced by passive missions, their starting balances, and the Gold Market."
---

# Currencies

| Currencies | |
|---|---|
| Cash | Stored starting balance 10,000; live persistence depends on server behavior |
| Gold Bars | Start at 0. Exchanged for cash at the Gold Exchange, then spent on cosmetics |
| Movember | Stored starting balance 0; earning and spending routes not established here |
| Intel | Referenced by passive missions; no currency-definition entry |
| Skill points | Per-role tags; current earning and spending consumers remain unverified |
| Gold Exchange | Stored unlock requirement: Wardog level 35 and 100,000 cash |
| Internal name | Currency definitions and exchange table ([`DT_CurrenciesDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json), [`DT_ExchangeDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json)) |
{: .wiki-infobox }

The current currency definitions contain Cash, Gold Bars and Movember. Passive missions separately reference Intel. Cash is the money of a match. Gold Bars come from exchanging cash and buy cosmetics. Passive missions name Intel amounts, but their invalid reward-type setting leaves payment unverified.

## Overview

| Currency | Starting balance | How it is earned | How it is spent | Carries between matches |
|---|---|---|---|---|
| Cash | 10,000 | Kills, revives, heals, vehicle work, zones, spotting, supply crates, and the end-of-match bonus | Vendors, role unlocks, factory investments | Yes, according to the in-game tip |
| Gold Bars | 0 | Exchanged from cash at the Gold Exchange, and leftover cash at a season reset | Gold Market skins and emotes | Set by the server, so not in the game |
| Movember | 0 | Not established here | Not established here | Not established here |
| Intel | Unknown (no entry in the currency table) | Stored passive-mission amounts 100 to 500; invalid reward type, payment unresolved | No route in reviewed currency/exchange rows | Unresolved |

## Cash

The current currency table stores an initial Cash balance of 10,000. Earlier CL516586 analysis described mode overrides of 3,000 in Strike and Disarm and 2,000 in VIP Escort, persistent account cash, and King of the Hill pre-lobby conversion at one Cash per point up to 5,000 (see [Pre-lobby](../game-modes-and-maps/pre-lobby.md)). Those historical consumers have not been independently matched to S3; the table value alone does not establish a first-login balance or live carry-over.

- **Earned.** Reward tables cover selected events such as kills, revives and heals. The amounts are in [Cash and Rewards](cash-and-rewards.md). The end-of-match bonus adds more on top, for the faction placed first, second or third.
- **Spent.** Cash buys gear, weapons, vehicles and supply crates from vendors, as listed on [Shops](shops.md). Vendor prices are changed by discounts there, and the current refund setting stores 0.9; the effective calculation remains unverified. It also buys role unlocks in the unlock tree, and it can be exchanged for Gold Bars. In Season 2 the Humvee unlock for the Driver role rose from 25,000 to 75,000 cash. The first factory investment costs 200 cash (see [Factory Investment](factory-investment.md)).
- **Carries over.** The loading-screen tip says the cash a player earns in a match is persistent, and whatever they leave with is what they spend in the next match. A server setting, Persistent Progression, switches persistent cash and XP on or off. The game does not say what an off setting does beyond losing the carry-over.

## Current S3 Wardog unlocks

The saved CL533731 Wardog track contains 67 nodes. Cash below is the **unlock cost**, not the vendor purchase price. These are exact saved prerequisites; mode restrictions and removed offerings still apply.

The [official S3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) summarize tanks as moving from Wardog level 145 to 200. The saved tree is more specific: **L2A6 is at 200**, while **SPH-2 is 145, T-72B3 is 155 and Vanguard AA is 165**. Do not apply the broad announcement as a universal level-200 gate for every tracked vehicle. This distinction requires current gameplay confirmation if the announcement intended a wider change.

| Wardog level | Item | Unlock cash |
|---:|---|---:|
| 1 | Judge | 5,000 |
| 4 | Kobra Reflex | 7,500 |
| 8 | Level 1 Helmet | 7,500 |
| 8 | Level 1 Armor | 10,000 |
| 10 | Field Backpack | 20,000 |
| 11 | 5.45mm Flesh Damage (HP) | 15,000 |
| 12 | 5.56mm Flesh Damage (HP) | 15,000 |
| 13 | 9mm Flesh Damage (HP) | 15,000 |
| 14 | 7.62mm Flesh Damage (HP) | 15,000 |
| 15 | Medium Tac Vest | 10,000 |
| 16 | Mechanical Supply Pallet | 10,000 |
| 17 | RK6 Tactical Foregrip | 7,500 |
| 18 | Compact T-2 Red Dot | 5,000 |
| 19 | .45 Colt Flesh Damage (HP) | 15,000 |
| 20 | GGX 17 | 15,000 |
| 20 | GGX 17 RND Magazine | 0 |
| 21 | Compact P-1 Red Dot | 12,500 |
| 22 | GGX 33 RND Magazine | 10,000 |
| 24 | Ammo Supply Pallet | 25,000 |
| 25 | Operator Backpack | 25,000 |
| 26 | Tricon 1.5x Compact Prism Scope | 10,000 |
| 28 | Blue (Da Ba Dee) - Eiffel 65 | 25,000 |
| 30 | Fuel Supply Pallet | 50,000 |
| 31 | Spitfire 3X | 25,000 |
| 32 | 12g Rifled Slug | 15,000 |
| 34 | 45° Angled Foregrip | 15,000 |
| 35 | Gold Exchange | 100,000 |
| 36 | Mini Angled Foregrip | 12,500 |
| 37 | Assault Backpack | 50,000 |
| 39 | 7.62x54mm Flesh Damage (HP) | 15,000 |
| 40 | M1911 | 25,000 |
| 40 | M1911 7 RND Magazine | 0 |
| 43 | .45 ACP Pistol Compensator | 15,000 |
| 45 | Sport Parachute | 25,000 |
| 46 | High Capacity Battery | 50,000 |
| 47 | Large Tac Vest | 25,000 |
| 49 | .45 ACP Flesh Damage (HP) | 15,000 |
| 50 | Level 2 Helmet | 37,500 |
| 50 | Level 2 Armor | 50,000 |
| 53 | M1911 10 RND Magazine | 10,000 |
| 55 | Ruck Backpack | 100,000 |
| 60 | TDG Vertical Foregrip | 25,000 |
| 65 | Deagle | 75,000 |
| 65 | Deagle 7 RND Magazine | 0 |
| 68 | 50AE Flesh Damage (HP) | 15,000 |
| 70 | Gunner Backpack + Sling | 125,000 |
| 75 | .308 Win Flesh Damage (HP) | 15,000 |
| 76 | 5.45mm Armor Piercing (AP) | 75,000 |
| 80 | 5.56mm Armor Piercing (AP) | 75,000 |
| 85 | GGX 50 RND Drum Magazine | 50,000 |
| 90 | 9mm Armor Piercing (AP) | 75,000 |
| 100 | 7.62mm Armor Piercing (AP) | 75,000 |
| 110 | GGX 18 | 125,000 |
| 120 | .45 Colt Armor Piercing (AP) | 75,000 |
| 130 | 7.62x54mm Armor Piercing (AP) | 75,000 |
| 140 | .45 ACP Armor Piercing (AP) | 75,000 |
| 145 | SPH-2 | 350,000 |
| 150 | Level 3 Helmet | 75,000 |
| 150 | Level 3 Armor | 100,000 |
| 155 | T-72B3 | 250,000 |
| 160 | 50AE Armor Piercing (AP) | 75,000 |
| 165 | Flakpanzer Gepard | 500,000 |
| 170 | .308 Win Armor Piercing (AP) | 75,000 |
| 180 | Level 4 Helmet | 150,000 |
| 180 | Level 4 Armor | 200,000 |
| 190 | Arsenal Backpack + 2 Slings | 175,000 |
| 200 | L2A6 | 750,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Wardog`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Gold Bars

Gold Bars are the premium currency. They pay for cosmetics only.

- **Starting balance.** The current definition stores 0; backend initialization is unverified.
- **Earning.** Gold Bars are earned by exchanging cash at the Gold Exchange. The exchange unlocks at Wardog level 35, and its current unlock node lists a cost of 100,000 cash. The exchange text calls Gold Bars the WARDOGS endgame currency, says that the rate varies, and says that a gold exchange cannot be resold or refunded.
- **Rate.** The exchange text describes a variable rate. The current exchange table contains a Gold Bars row with an empty rate list. It gives no usable conversion rate; the active rate and its producer require server evidence.
- **Season resets.** At the end of a major update cycle, level progression and cash are reset. Any cash left over is exchanged for Gold Bars automatically. The season reset reports the leftover cash and the Gold Bars given, and the conversion happens on the server.
- **Other sources.** The reviewed currency and exchange definitions do not establish other earning or purchase routes. A complete reward/backend audit would be needed to exclude direct grants or real-money packs.
- **Spending.** Gold Market cosmetics. See the Gold Market section below.
- **Carry-over.** Decided by the server; the game does not describe it.

## Intel

The selected passive-mission rows reference Intel rewards. They do not establish that missions are its only source.

- **Earned.** The Earn Cash, Earn Role XP and Time Played missions each list 100, 200, 300, 400 and 500 Intel at five tiers. All 15 entries have an invalid reward-type setting, so these are configured amounts, not verified payments. See [Challenges](challenges.md).
- **Spent.** The reviewed currency definitions and exchange row supply no Intel spending route. A complete current consumer or backend audit is still needed to exclude other uses.
- **Starting balance.** Unknown. The current currency table has no Intel entry; that absence does not establish a zero balance or backend initialization.

## Skill points

Per-role skill-point tags were identified in the earlier progression analysis. Its XP-to-skill-point association has not been matched to the current consumer. The reviewed currency definitions list Cash, Gold Bars and Movember, without a skill-point entry; that table does not exclude skill-point grants or spending through other systems. Current earning, spending and upgrade behavior remain unresolved. See [Skills](skills.md).

## Gold Market

The Gold Market sells cosmetics for Gold Bars. The S3 table has 32 entries worth 345 Gold Bars in total. These are saved listings, not confirmation of current server availability.

| Category | Entries | Gold Bars in total |
|---|---|---|
| Weapon skins | 21 | 200 |
| Vehicle skins | 6 | 85 |
| Parachute skin | 1 | 15 |
| Emotes | 3 | 15 |
| Medical-item skin | 1 | 30 |
| Total | 32 | 345 |

- Prices run from 5 to 30 Gold Bars per entry. The Black and Gold MH-6 and Black and Gold Defibrillator each cost 30 in the table.
- Most entries have no expiry.
- The [official S3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) announce a **2-week carryover** for Littlebird Black & Gold from S2. This governs the announced availability; the retained date field below is not an independently verified expiry.
- The Black and Gold MH-6 has an expiry date of 31 December 2026, and its tile shows a countdown. The expiry field has three settings: no expiry, expiry with no end time, and expiry with an end time. This entry has the no-end-time setting. Whether the entry leaves the market on that date is decided by the server; the game only stores the date.
- Cosmetics absent from the reviewed Gold Market table, such as the faction logos, the taxi skin and the bobbleheads, have no price in that table. Their route is not known. See [Cosmetics](cosmetics.md).

The full list of skins and emotes is in [Weapon Skins](weapon-skins.md), [Vehicle Skins](vehicle-skins.md), [Emotes](emotes.md) and [Season 1 Cosmetics](season-01-cosmetics.md).

## Season 2 changes

- Season 2 changed 54 cash costs in the role unlock tree. The Humvee for the Driver role rose from 25,000 to 75,000 cash. The Havoc for the Pilot role rose from 500,000 to 650,000 cash. See [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md).
- The end-of-match bonus gained a Lonestar faction payment of 10,000 cash. See [Cash and Rewards](cash-and-rewards.md).
- Season 2 added Gold Market entries: the Chocolate Chip set, the Little Bird in Black and Gold, and several weapons.

## See also

- [Cash and Rewards](cash-and-rewards.md)
- [Shops](shops.md)
- [Cosmetics](cosmetics.md)
- [Challenges](challenges.md)
- [Skills](skills.md)
- [Factory Investment](factory-investment.md)
- [Progression & Economy](../progression-and-economy.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), the currency definitions and the Gold Market prices
- [Meta: currency, exchange and Gold Market](../../content/Wardogs_Meta_v2.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Data tables: Economy and Rewards](../../content/Wardogs_DataTables_Economy_v1.md), including the Gold Market and exchange tables
- [Data tables: Frontend](../../content/Wardogs_DataTables_Frontend_v1.md), the economy tips
- [Challenges](../../game-features/Wardogs_Challenges_v1.md), for the Intel rewards
- [Factory investment](../../game-features/Wardogs_GameFeatures_FactoryInvestment_01_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- Loading screen tips, the persistent cash tip
- [Economy data: currencies, exchange and Gold Market](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- Currency definitions (JSON)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): expiry (P18), carry-over (P15) and Intel spend path (P13)
