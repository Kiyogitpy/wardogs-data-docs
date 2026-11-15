---
title: "Crowbar Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The one crowbar challenge, Door Forced Open, and its stored cash expression."
---

# Crowbar Challenges

| Crowbar Challenges | |
|---|---|
| **General** | |
| Kind | Event reward |
| Challenges | 1 |
| Auto-activate | Stored flag: true; live activation unverified |
| Internal name | DT_Challenges_SessionEvents_Crowbar |
{: .wiki-infobox }

The crowbar challenge definition associates forcing a door open with a stored cash expression; current payout eligibility is unverified. The crowbar is the [Halligan Bar](../equipment/halligan-bar.md).

## Challenges

| Challenge | What earns it | Cash (base) | Role XP (base) |
|---|---|---|---|
| Door Forced Open | Breaching a door | 100 × zone factor × repeat factor | No Role XP resource in this row |

The current cash row stores `(1 - clamp(LastVictimCount, 0, 1)) * (100 * InstigatorZoneModifier)`. The zone selector stores 2 in a Hot Zone, 1 in a Control Zone and 0 otherwise: with a repeat count of zero, the expression gives 200, 100 or 0 cash respectively. A repeat count of one or more makes it zero. This is a calculation from the saved expression, not a measured payout; the current native evaluator, repeat-counter lifetime and live activation remain unverified. There is no owner-assist multiplier or Role XP resource in this row.

## Season 2 changes

The sources list no Season 2 changes for this challenge.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Halligan Bar](../equipment/halligan-bar.md)
- [Buildable Challenges](buildable-challenges.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), sections 3 and 6
- [Crowbar challenge definition](../../data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_Challenges_SessionEvents_Crowbar.json) and [current reward expression](../../data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengeRewards_SessionEvents_Crowbar.json)
