---
title: "Achievements"
parent: "Progression & Economy"
group: "Challenges"
description: "The ten one-time achievements, the thresholds they use (100,000 cash, one hour in a control zone, 950 m) and what each one asks for. Each is a Steam achievement, and the data lists no other reward."
---

# Achievements

| Achievements | |
|---|---|
| **General** | |
| Kind | One-time goals |
| Number | 10 |
| Rewards | None in the data. The Steam achievement is the reward |
| Steam | Each achievement is also a Steam achievement |
| **Thresholds** | |
| Cash | 100,000 (Loadout Spender and Single Life Profit) |
| Time | 3,600 seconds, or 1 hour (Control Zone Survivor) |
| Distance | 950 m (Long Shot) |
| Internal name | DT_Challenges_SessionEvents_Shared |
{: .wiki-infobox }

Achievements are one-time goals. A player can earn each one once, and each is also a Steam achievement. The data gives a name and a goal for all ten. Four of them have a number to reach: 100,000 cash twice, one hour in a control zone, and a 950 m kill. The data lists no cash, XP or item reward for any of them, so the Steam achievement is the only reward.

## Overview

There are ten achievements. They are active from the start, and each one stops counting once it is done.

## How it works

- **Always active.** The data sets all ten achievements to start automatically.
- **Earned once.** Each achievement stops counting after it is earned.
- **Steam.** Each achievement is linked to a Steam achievement with its own ID in the data.
- **Thresholds.** Loadout Spender and Single Life Profit need 100,000 cash. Control Zone Survivor needs 3,600 seconds (one hour) alive in a control zone. Long Shot needs a kill from 950 m. The data stores that distance as 95,000 Unreal units, the same unit the kill-distance rewards use, so 950 m is a derived figure.

## Achievements

| Achievement | Goal | Threshold | Reward |
|---|---|---|---|
| Loadout Spender | Make one loadout purchase of at least 100,000 cash. The check is on a single purchase event. | 100,000 cash | Steam achievement |
| Complete The Tutorial | Finish the tutorial. | None | Steam achievement |
| Punch Kristopher | Hit the tutorial character Kristopher with a melee attack. | None | Steam achievement |
| Top Cash Earner | Finish first for cash earned in a match, with more than 0 cash earned. It is checked from the match stats, not from an event. | None | Steam achievement |
| Control Zone Survivor | Stay alive in a control zone for 3,600 seconds. Entering the zone starts the timer, and a death resets it. | 3,600 s (1 hour) | Steam achievement |
| Single Life Profit | Reach a profit of 100,000 cash. The check runs on each profit change. | 100,000 cash | Steam achievement |
| Long Shot | Kill a hostile target from at least 950 m. | 950 m | Steam achievement |
| Ricochet Kill | Kill a hostile target with a ricochet. | None | Steam achievement |
| Defibrillator Kill | Kill a hostile target with the defibrillator. | None | Steam achievement |
| Clean Sweep | At the end of the match, your faction has a score above 0 and the other faction has 0. It is checked from the final scores. | None | Steam achievement |

Kill achievements count hostile targets only. Long Shot, Ricochet Kill and Defibrillator Kill all need the target to be an enemy.

## Rewards

The data lists no cash, role XP or item for any achievement. The reward is the Steam achievement that matches each one.

## Season 2 changes

- The achievement table went from no rows to 10 rows in the Season 02 update.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Passive Missions](passive-missions.md)
- [Wagers](wagers.md)
- [Cash and Rewards](cash-and-rewards.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- Achievement table (JSON)
- Shared session-event challenges (JSON)
- [Economy data: achievements](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
