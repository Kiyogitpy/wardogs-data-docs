---
title: "Wagers"
parent: "Progression & Economy"
group: "Unlocks"
description: "The four wager challenges (get kills, drop off people, revive teammates, destroy occupied vehicles) and the stake limits in the data."
---

# Wagers

| Wagers | |
|---|---|
| **General** | |
| Kind | Goals taken on with a stake |
| Challenges | 4 |
| Stake | 2,500 to 100,000 cash |
| Reward | Not in the data |
| Internal name | DT_WagerChallenges |
{: .wiki-infobox }

Wagers are goals that a player can take on with a stake. The data has four wager challenges and a pricing table that sets the stake limits. The goal numbers and the payouts for each wager are not in the data.

## Overview

| Wager | Goal | Target number |
|---|---|---|
| Get Kills | Get a set number of player kills | Not in the data |
| Dropoff People | Deliver a set number of passengers | Not in the data |
| Revive Teammates | Revive a set number of teammates. Some action types do not count. | Not in the data |
| Destroy Occupied Vehicles | Destroy a set number of vehicles that have someone in them | Not in the data |

## How it works

- **Not automatic.** The data marks wager challenges as not auto-activated.
- **Set numbers.** Each wager has a number that its state tree uses (kills, passengers, revives or vehicles). The data does not set those numbers.
- **Eligible actions.** The revive and vehicle wagers have lists of eligible and excluded action types. The sources do not list them.

## Stakes

The pricing table sets a stake of at least 2,500 cash and at most 100,000 cash, and caps the payout at 5,000,000 cash. The table also has odds and bonus values whose use is not yet known.

## Objective catalogue

The wager system also has an objective catalogue with count-based objectives, for example one that needs 3 kills. The data does not say which catalogue objective each of the four wager challenges uses.

## Rewards

The data lists no cash, XP or item for the four wager challenges.

## Season 2 changes

- The wager system was added in the Season 02 update, with seven files under the wager data folder: pricing, actions, challenges, conditions, an objective catalogue and two UI tables.
- Four wager challenges were added: passengers delivered, rewarded kills, rewarded revives and rewarded vehicles destroyed.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Passive Missions](passive-missions.md)
- [Achievements](achievements.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Wager challenge table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerChallenges.json) (JSON)
- [Wager pricing table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerPricing.json) (JSON)
