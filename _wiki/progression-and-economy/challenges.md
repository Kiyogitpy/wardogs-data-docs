---
title: "Challenges"
parent: "Progression & Economy"
description: "The challenges that pay out during and across matches: in-match actions, achievements, passive missions, wagers and tips."
---

# Challenges

| Challenges | |
|---|---|
| Kinds | In-match action challenges, achievements, passive missions, wagers, tips |
| In-match action challenges | 60 for King of the Hill, plus buildable, spotting and Team Offence challenges |
| Achievements | 10 |
| Passive missions | 15 (earn cash, earn role XP, time played) |
| Wagers | 4 (get kills, drop off people, revive teammates, destroy occupied vehicles) |
| Internal name | Challenges (game feature) |
{: .wiki-infobox }

A challenge is a small rule that waits for one thing to happen in a match, then pays out or counts progress toward a goal. Most challenges run during a match and pay cash and role XP for the action itself. Others, such as passive missions and achievements, track longer goals across play.

## Overview

The sources list 108 challenge definitions in nine tables. Most are in-match action challenges that run automatically as the match goes on. The rest are achievements, passive missions, wagers and Team Offence challenges.

## How it works

- **Action challenges.** Each one waits for an event, such as a player kill, a revive, or a vehicle destroyed. The reward is then calculated from the action, with the multipliers described on [Cash and Rewards](cash-and-rewards.md).
- **Assist versions.** Most action challenges have assist versions. A player who helped with a kill, a revive or a vehicle kill gets credit under the assist version, with its own split.
- **Tips.** A tip is a reward for passing help to a teammate, such as sending or receiving a tip for healing or delivering a player. Pre-tips are a separate challenge.
- **Passive missions.** These track a total over time. They do not depend on one event.
- **Wagers.** A wager is a short goal inside a match, such as a number of kills. The number needed is a setting the data does not record.

## Achievements

Achievements are one-time goals. They are: Loadout Spender, Complete The Tutorial, Punch Kristopher, Top Cash Earner, Control Zone Survivor, Single Life Profit, Long Shot, Ricochet Kill, Defibrillator Kill and Clean Sweep.

Some achievements have a number attached. Loadout Spender and Single Life Profit use a cash threshold, Control Zone Survivor uses a required time in the zone, and Long Shot uses a distance threshold. The data does not give those numbers in the rows.

## Passive missions

| Mission | Target | Reward per tier |
|---|---|---|
| Earn Cash | 5,000, 12,000, 30,000, 80,000, 200,000 cash (five tiers) | 100, 200, 300, 400, 500 Intel |
| Earn Role XP | 500 role XP in each of five tiers | 100, 200, 300, 400, 500 Intel |
| Time Played | 1,800 seconds (30 minutes) in each of five tiers | 100, 200, 300, 400, 500 Intel |

Intel is the currency these missions pay. The data gives it no display name and no shop use, so its use is not yet known.

## Wagers

| Wager | Goal |
|---|---|
| Get Kills | A set number of player kills |
| Dropoff People | A set number of passengers delivered |
| Revive Teammates | A set number of revives (some action types excluded) |
| Destroy Occupied Vehicles | A set number of vehicles destroyed while occupied |

The wager goals are set by the match. The numbers are not in the data.

## Tips

Tips are a reward for teamwork. The data lists tip tiers for five actions, and a pre-tip bonus:

| Tip for | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Heal | 5 | 10 | 15 | 20 |
| Revive | 10 | 15 | 20 | 25 |
| Player delivered | 15 | 20 | 25 | 30 |
| Repair | 5 | 10 | 15 | 20 |
| Refuel | 5 | 10 | 15 | 20 |

A pre-tip pays 50 cash for each tip, capped at 500. The unit for the tier values is not stated in the data, apart from the pre-tip bonus, which is cash.

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
- Four challenge state trees were added for wagers: passengers delivered, rewarded kills, rewarded revives and rewarded vehicles destroyed.
- Team Offence adds a punish challenge and a teamkill voter challenge. See [Team Offence](../game-modes-and-maps/team-offence.md).

## See also

- [Cash and Rewards](cash-and-rewards.md)
- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md)
- [Team Offence](../game-modes-and-maps/team-offence.md)

## Sources

- [Challenges](../../game-features/Wardogs_Challenges_v1.md)
- [KOTH challenges](../../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
