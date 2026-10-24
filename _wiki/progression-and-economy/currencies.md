---
title: "Currencies"
parent: "Progression & Economy"
group: "Economy"
description: "The money in Wardogs: Cash, Gold Bars and Intel, their starting balances, how each is earned and spent, and the Gold Market."
---

# Currencies

| Currencies | |
|---|---|
| Cash | Starts at 10,000. Earned in matches and spent at vendors and on unlocks |
| Gold Bars | Start at 0. Spent on skins and emotes on the Gold Market. No way to earn them is in the data |
| Intel | Paid by passive missions. Its use is not yet known |
| Skill points | One per role in the data. Not yet known how they are shown or spent |
| Internal name | Currency definitions and exchange table (`DT_CurrenciesDefinitions`, `DT_ExchangeDefinitions`) |
{: .wiki-infobox }

The game has three currencies a player sees: Cash, Gold Bars and Intel. Cash is the money of a match. Gold Bars buy cosmetics. Intel is paid for passive missions and has no shop use in the data yet.

## Overview

| Currency | Starting balance | How it is earned | How it is spent | Carries between matches |
|---|---|---|---|---|
| Cash | 10,000 | Kills, revives, heals, vehicle work, zones, spotting, supply crates, and the end-of-match bonus | Vendors, role unlocks, factory investments | Yes, according to the in-game tip |
| Gold Bars | 0 | Not yet known. No reward row pays them | Gold Market skins and emotes | Not yet known |
| Intel | Not yet known | Passive missions, 100 to 500 per tier | Not yet known | Not yet known |

## Cash

Cash is the main currency. It starts every player at 10,000, and players earn more during the match.

- **Earned.** Every action in a match pays cash, such as a kill, a revive or a heal. The amounts are in [Cash and Rewards](cash-and-rewards.md). The end-of-match bonus adds more on top, for the faction placed first, second or third.
- **Spent.** Cash buys gear, weapons, vehicles and supply crates from vendors, as listed on [Shops](shops.md). It also buys role unlocks in the unlock tree. In Season 2 the Humvee unlock for the Driver role rose from 25,000 to 75,000 cash. The first factory investment costs 200 cash (see [Factory Investment](factory-investment.md)).
- **Carries over.** The loading-screen tip says the cash a player earns in a match is persistent, and whatever they leave with is what they spend in the next match. A server setting, Persistent Progression, switches persistent cash and XP on or off. The data does not say what an off setting does beyond losing the carry-over.

## Gold Bars

Gold Bars are the premium currency. They pay for cosmetics only.

- **Starting balance.** 0.
- **Earning.** The data gives Gold Bars no reward. No match event, challenge or mission pays them, and the exchange table has no cash-to-Gold-Bar rate. The UI data has Gold Exchange text and a purchase sound, but no rate, so how a player gets Gold Bars is not yet known.
- **Spending.** Gold Market cosmetics. See the Gold Market section below.
- **Carry-over.** Not yet known.

## Intel

In the data, Intel is paid only by passive missions.

- **Earned.** The passive mission Earn Cash pays 100, 200, 300, 400 and 500 Intel at its five tiers. The Earn Role XP mission and the Time Played mission pay the same five amounts. See [Challenges](challenges.md).
- **Spent.** The data gives Intel no display text beyond its name and no shop use, so its use is not yet known.
- **Starting balance.** Not stated in the data.

## Skill points

The data has a skill point tag for each role. The resource-change effect sets a skill point value alongside each role XP value. The data gives skill points no display name, starting balance or spending rule, so how they work is not yet known. See [Skills](skills.md).

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
- Most entries never expire.
- One entry, the Black and Gold MH-6, carries an expiry timestamp of 31 December 2026 in the data. Its expiration type is "no end time", so whether it leaves the market at that date is not yet known.
- Cosmetics that are not on the Gold Market, such as the faction logos, the taxi skin and the bobbleheads, have no price in the data. See [Cosmetics](cosmetics.md).

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
