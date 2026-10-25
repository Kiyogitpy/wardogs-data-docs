---
title: "Currencies"
parent: "Progression & Economy"
group: "Economy"
description: "The money in Wardogs: Cash, Gold Bars (bought with cash at the Gold Exchange) and Intel (earned from passive missions, with no use in the data), their starting balances, and the Gold Market."
---

# Currencies

| Currencies | |
|---|---|
| Cash | Starts at 10,000. Earned in matches and spent at vendors and on unlocks |
| Gold Bars | Start at 0. Exchanged for cash at the Gold Exchange, then spent on cosmetics |
| Intel | Earned from passive missions. The data gives it no use |
| Skill points | Reserved. Six per-role tags exist, and nothing grants or spends them |
| Gold Exchange | Unlocks at Wardog level 35 for 150,000 cash |
| Internal name | Currency definitions and exchange table (`DT_CurrenciesDefinitions`, `DT_ExchangeDefinitions`) |
{: .wiki-infobox }

The game has three currencies a player sees: Cash, Gold Bars and Intel. Cash is the money of a match. Gold Bars come from exchanging cash and buy cosmetics. Intel is paid for passive missions, and the data gives it no use.

## Overview

| Currency | Starting balance | How it is earned | How it is spent | Carries between matches |
|---|---|---|---|---|
| Cash | 10,000 | Kills, revives, heals, vehicle work, zones, spotting, supply crates, and the end-of-match bonus | Vendors, role unlocks, factory investments | Yes, according to the in-game tip |
| Gold Bars | 0 | Exchanged from cash at the Gold Exchange, and leftover cash at a season reset | Gold Market skins and emotes | Not in the data |
| Intel | None (no entry in the currency table) | Passive missions, 100 to 500 per tier | None found in the game files | None found in the game files |

## Cash

Cash is the main currency. It starts every player at 10,000, and players earn more during the match. The client's currency table sets this starting balance.

- **Earned.** Every action in a match pays cash, such as a kill, a revive or a heal. The amounts are in [Cash and Rewards](cash-and-rewards.md). The end-of-match bonus adds more on top, for the faction placed first, second or third.
- **Spent.** Cash buys gear, weapons, vehicles and supply crates from vendors, as listed on [Shops](shops.md). Vendor prices are changed by discounts there, and a refund returns 90% of the eligible amount. It also buys role unlocks in the unlock tree, and it can be exchanged for Gold Bars. In Season 2 the Humvee unlock for the Driver role rose from 25,000 to 75,000 cash. The first factory investment costs 200 cash (see [Factory Investment](factory-investment.md)).
- **Carries over.** The loading-screen tip says the cash a player earns in a match is persistent, and whatever they leave with is what they spend in the next match. A server setting, Persistent Progression, switches persistent cash and XP on or off. The data does not say what an off setting does beyond losing the carry-over.

## Gold Bars

Gold Bars are the premium currency. They pay for cosmetics only.

- **Starting balance.** 0.
- **Earning.** Gold Bars are earned by exchanging cash at the Gold Exchange. The exchange unlocks at Wardog level 35, and unlocking it costs 150,000 cash. The exchange text calls Gold Bars the WARDOGS endgame currency, says that the rate varies, and says that a gold exchange cannot be resold or refunded.
- **Rate.** The server sets the rate, and it changes over time. The client holds no rate, so the cash price of a Gold Bar is not known from the data.
- **Season resets.** At the end of a major update cycle, level progression and cash are reset. Any cash left over is exchanged for Gold Bars automatically. The season reset reports the leftover cash and the Gold Bars given, and the conversion happens on the server.
- **Other sources.** No match event, challenge, mission or achievement pays Gold Bars directly. The data has no Gold Bar pack, so whether Gold Bars are sold for money is not in the client data.
- **Spending.** Gold Market cosmetics. See the Gold Market section below.
- **Carry-over.** Decided by the server; the game files do not describe it.

## Intel

In the data, Intel is paid only by passive missions.

- **Earned.** The passive mission Earn Cash pays 100, 200, 300, 400 and 500 Intel at its five tiers. The Earn Role XP mission and the Time Played mission pay the same five amounts. See [Challenges](challenges.md).
- **Spent.** Nothing in the data uses Intel. It has no balance entry, no shop price, no unlock cost and no exchange, so the client has no spending route for it.
- **Starting balance.** None. The client's currency table has no Intel entry, so Intel starts at nothing.

## Skill points

The data has a skill point tag for each role. Each role XP gain also sets a skill point value. Nothing in the data grants or spends skill points: the currency table defines only Cash and Gold Bars, and no reward, unlock or cost uses them. They are reserved. See [Skills](skills.md).

## Gold Market

The Gold Market sells cosmetics for Gold Bars. Its table has 27 entries worth 275 Gold Bars in total.

| Category | Entries | Gold Bars in total |
|---|---|---|
| Weapon skins | 17 | 160 |
| Vehicle skins | 6 | 85 |
| Parachute skin | 1 | 15 |
| Emotes | 3 | 15 |
| Total | 27 | 275 |

- Prices run from 5 to 30 Gold Bars per entry. The most expensive is the Black and Gold MH-6 at 30.
- Most entries have no expiry.
- The Black and Gold MH-6 has an expiry date of 31 December 2026 in the data, and its tile shows a countdown. The expiry field has three settings in the data: no expiry, expiry with no end time, and expiry with an end time. This entry has the no-end-time setting. Whether the entry leaves the market on that date is decided by the server; the game files only store the date.
- Cosmetics that are not on the Gold Market, such as the faction logos, the taxi skin and the bobbleheads, have no price in the data. Their route is not known. See [Cosmetics](cosmetics.md).

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
- [Loading screen tips](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Data/DT_LoadingScreenTips.json), the persistent cash tip
- [Economy data: currencies, exchange and Gold Market](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Currency definitions (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): expiry (P18), carry-over (P15) and Intel spend path (P13)
