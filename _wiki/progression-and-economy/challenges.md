---
title: "Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The challenges that pay out during and across matches: in-match actions, achievements, passive missions, retained wager data and tips."
---

# Challenges

| Challenges | |
|---|---|
| Kinds | In-match challenges, achievements, passive missions, retained wager configuration, tips |
| In-match action challenges | 62 for King of the Hill, plus buildable, spotting, Hot Zone Magnet, crowbar and Team Offence challenges |
| Achievements | 13 in the shared challenge table, plus the shooting-range horn challenge |
| Passive missions | 15 (earn cash, earn role XP, time played) |
| Wagers | Removed vendor in S3; 11 goals retained in data, categories unresolved |
| Internal name | Challenges (game feature) |
{: .wiki-infobox }

A challenge is a small rule that waits for one thing to happen in a match, then pays out or counts progress toward a goal. Most challenges run during a match and pay cash and role XP for the action itself. Others, such as passive missions and achievements, track longer goals across play.

## Overview

The sources list 122 challenge definitions in ten tables. Each table is one category, and each category has its own article, listed under Categories below. The auto-activate flags are stored per row; they do not by themselves establish which challenges run in a live match.

## How it works

- **Action challenges.** Each one waits for an event, such as a player kill, a revive, or a vehicle destroyed. The reward is then calculated from the action, with the multipliers described on [Cash and Rewards](cash-and-rewards.md).
- **Assist versions.** Most action challenges have assist versions. A player who helped with a kill, a revive or a vehicle kill gets credit under the assist version, with its own split.
- **Tips.** A tip is a reward for passing help to a teammate, such as sending or receiving a tip for healing or delivering a player. Pre-tips are a separate challenge.
- **Passive missions.** These track a total over time. They do not depend on one event.
- **Wagers.** The vendor was removed in S3 ([official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221)). Its retained goals are documented on the Wagers article, not offered as current earning advice.

## Categories

- [Achievements](achievements.md): 13 shared definitions; Shooting Range adds a separate Sound the Horn definition
- [Passive Missions](passive-missions.md): 15 tiered totals (cash earned, role XP earned, time played)
- [Wagers](wagers.md): 11 stored goals, including drill towers, FOB hacking, three freefall goals, spawn radars and supply pallets
- [King of the Hill Challenges](king-of-the-hill-challenges.md): 62 event rewards, including assist versions
- [Buildable Challenges](buildable-challenges.md): 12 rewards for buildables and FOBs
- [Crowbar Challenges](crowbar-challenges.md): 1 reward for forcing a door open
- [Spotting Challenges](spotting-challenges.md): 2 rewards for spotting and for destroying a spotted target
- [Team Offence Challenges](team-offence-challenges.md): 2 rewards for punishing a kill and voting on a teamkill
- [Hot Zone Magnet Challenges](hot-zone-magnet-challenges.md): 3 rewards for magnet and tower events

## Tips

Tips are a reward for teamwork. The game lists tip tiers for five actions, and a pre-tip bonus:

| Tip for | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Heal | 5 | 10 | 15 | 20 |
| Revive | 10 | 15 | 20 | 25 |
| Player delivered | 15 | 20 | 25 | 30 |
| Repair | 5 | 10 | 15 | 20 |
| Refuel | 5 | 10 | 15 | 20 |

A pre-tip pays 50 cash for each tip, capped at 500. The unit for the tier values is not stated, apart from the pre-tip bonus, which is cash.

## Numbers

Base values for in-match actions are on [Cash and Rewards](cash-and-rewards.md). The King of the Hill action list covers, among others:

- Player kill, with crew, logistics, revive, FOB-supplied and supply-crate assist versions.
- Revive player and heal player, each with assist versions.
- Destroy vehicle, destroy vehicle section, and their assist versions.
- Zone entry, safe zone entered after a logistics run, and survived trip.
- Deploy on vehicle, deploy a supply crate, supply pallet dropped, repair vehicle, refuel vehicle, purchase from a supply crate, and destroy a supply crate.
- Target spotted and spotted target destroyed.
- Hot Zone Magnet events: magnet activated, magnet deactivated, and tower captured.

## Season 2 changes

- The King of the Hill challenge table went from no rows to 60.
- Vehicle destroyed rewards split by variant, for example Kodiak now has Default, Machine Gun and Pickup versions.
- Four challenges were added for wagers: passengers delivered, rewarded kills, rewarded revives and rewarded vehicles destroyed.
- Team Offence adds a punish challenge and a teamkill voter challenge. See [Team Offence](../game-modes-and-maps/team-offence.md).

## See also

- [Cash and Rewards](cash-and-rewards.md)
- [Weapon Mastery](weapon-mastery.md)
- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md)
- [Team Offence](../game-modes-and-maps/team-offence.md)

## Sources

- [Challenges](../../game-features/Wardogs_Challenges_v1.md)
- [KOTH challenges](../../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
