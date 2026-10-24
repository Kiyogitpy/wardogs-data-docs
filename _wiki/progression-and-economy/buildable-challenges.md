---
title: "Buildable Challenges"
parent: "Progression & Economy"
group: "Unlocks"
description: "The eleven challenges for building, supplying, damaging and hacking buildables and forward operating bases, with the base amounts in the data."
---

# Buildable Challenges

| Buildable Challenges | |
|---|---|
| **General** | |
| Kind | Event rewards for buildables and FOBs |
| Challenges | 11 |
| Auto-activate | 9 of 11 |
| Internal name | DT_Challenges_SessionEvents_Buildables |
{: .wiki-infobox }

Buildable challenges pay for work on buildables, the structures players place, including forward operating bases (FOBs). The eleven rows cover building, finishing, destroying, supplying, hacking and closing doors. Most pay cash and role XP from a base amount and a share for the owner or helpers.

## Overview

Rows are grouped by the kind of work: building and finishing, destroying and damaging, schematics and build supplies, and FOB events. The cash and XP columns show the base amounts from the data. Where a row says "match score", the sources list that as the reward and give no cash or XP for it.

## How it works

- **Calculated.** Most rows are worked out from one input. Finishing a buildable uses the build cost, building uses the build amount, FOB resources used uses the cash spent, and hacks and door closures use the victim count.
- **Formula not given.** The sources list the base numbers and the owner or helper shares, but not the formula that combines them with the input. The numbers are shown as the data lists them.
- **Not automatic.** Buildable Damaged and Schematic Placed are not auto-activated.

## Challenges

| Challenge | What earns it | Cash (base) | Role XP (base) |
|---|---|---|---|
| Buildable Damaged | Damaging a buildable | Match score only | Not in the data |
| Buildable Destroyed | Destroying a buildable | Match score only | Not in the data |
| Buildable Destroyed Assist | Helping to destroy a buildable | Match score only | Not in the data |
| Buildable Finished | Finishing construction of a buildable | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| Buildable Building | Contributing to a buildable under construction | Base 5, owner assist 1 | Base 1, owner assist 0.4 |
| Schematic Placed | Placing a building schematic | Default 10 | Not in the data |
| Build Supplies Deposited | Placing build supplies in the FOB | Base 0.5, owner assist 0.25, default 0.4 | Base 0.25, owner assist 0.1, default 0.1 |
| Build Supplies Consumed | Using build supplies in the FOB | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| FOB Resources Used | Another player uses supplies from your FOB | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| FOB Hacked | Hacking an enemy FOB | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |
| Door Closed | Successfully closing a friendly door | Base 0.5, owner assist 0.25 | Base 0.25, owner assist 0.1 |

## Season 2 changes

The sources list no Season 2 changes for these rows.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Buildables](../equipment/buildables.md)
- [Forward Operating Base](../equipment/forward-operating-base.md)
- [Crowbar Challenges](crowbar-challenges.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), sections 3 and 6
- [Buildable challenge table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_Challenges_SessionEvents_Buildables.json) (JSON)
- [Buildable reward formulas](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json) (JSON)
