---
title: "Passive Missions"
parent: "Progression & Economy"
group: "Unlocks"
description: "The three passive missions with five tiers each: cash earned, role XP earned and time played, and the Intel each tier pays."
---

# Passive Missions

| Passive Missions | |
|---|---|
| **General** | |
| Kind | Tiered totals tracked over time |
| Missions | 3, with 5 tiers each (15 in total) |
| Reward | Intel per tier |
| Auto-activate | No |
| Internal name | DT_PassiveMissionChallenges |
{: .wiki-infobox }

Passive missions track a total that builds up over play, not a single event. There are three missions, and each has five tiers. Each tier pays Intel when its goal is reached.

## Overview

- **Earn Cash** counts the cash a player earns. Tiers: 5,000, 12,000, 30,000, 80,000 and 200,000 cash.
- **Earn Role XP** counts role XP earned. Every tier has the same goal in the data: 500 role XP.
- **Time Played** counts time played. Every tier has the same goal in the data: 1,800 seconds (30 minutes).

## How it works

- **Not automatic.** The data marks passive missions as not auto-activated.
- **Tiers.** Each tier is a separate challenge with its own reward. The Earn Role XP and Time Played tiers differ only in their reward.
- **Time Played** is checked on a set interval. The length of that interval is not in the data.

## Missions

| Mission | Tier | Goal | Reward |
|---|---|---|---|
| Earn Cash | 1 | 5,000 cash earned | 100 Intel |
| Earn Cash | 2 | 12,000 cash earned | 200 Intel |
| Earn Cash | 3 | 30,000 cash earned | 300 Intel |
| Earn Cash | 4 | 80,000 cash earned | 400 Intel |
| Earn Cash | 5 | 200,000 cash earned | 500 Intel |
| Earn Role XP | 1 | 500 role XP earned | 100 Intel |
| Earn Role XP | 2 | 500 role XP earned | 200 Intel |
| Earn Role XP | 3 | 500 role XP earned | 300 Intel |
| Earn Role XP | 4 | 500 role XP earned | 400 Intel |
| Earn Role XP | 5 | 500 role XP earned | 500 Intel |
| Time Played | 1 | 1,800 seconds played | 100 Intel |
| Time Played | 2 | 1,800 seconds played | 200 Intel |
| Time Played | 3 | 1,800 seconds played | 300 Intel |
| Time Played | 4 | 1,800 seconds played | 400 Intel |
| Time Played | 5 | 1,800 seconds played | 500 Intel |

## Intel

Intel is the currency these missions pay. The data gives it no display name, and the game files show no way to spend it.

## Season 2 changes

- The passive mission table went from no rows to 15 rows in the Season 02 update.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Achievements](achievements.md)
- [Wagers](wagers.md)
- [Cash and Rewards](cash-and-rewards.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Passive mission table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissionChallenges.json) (JSON)
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): no spend path for Intel (P13)
