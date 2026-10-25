---
title: "Spotting Challenges"
parent: "Progression & Economy"
group: "Unlocks"
description: "The two spotting challenges, which pay cash when a player spots a target and when a spotted target is destroyed."
---

# Spotting Challenges

| Spotting Challenges | |
|---|---|
| **General** | |
| Kind | Event reward |
| Challenges | 2 |
| Cash | 15 to 275 (target spotted); 50 to 500 (spotted target destroyed) |
| Role XP | 5 to 100 per spot; 5 to 500 per destroyed target (25 and 150 for a player) |
| Internal name | DT_Challenges_SessionEvents_KOTH_Spotting |
{: .wiki-infobox }

Spotting challenges pay players who spot a target. One pays when a target is spotted, and the other pays when a spotted target is destroyed.

## Challenges

| Challenge | What earns it | Cash | Role XP |
|---|---|---|---|
| Target Spotted | A player successfully spots a target | 15 to 275 | 5 to 100 (25 for a player) |
| Spotted Target Destroyed | A spotted target is destroyed. Pays the players who spotted it. | 50 to 500 | 5 to 500 (150 for a player) |

The amount for each is scaled between its minimum and maximum by an assist curve. The scale depends on how much the spot contributed to the kill. The Role XP per target type is set by the target: an armoured vehicle or aircraft pays more than a supply crate or mine. A target destroyed by the enemy (not by the spotter's side) pays a quarter of its cash and half its Role XP.

## Season 2 changes

The sources list no Season 2 changes for these challenges.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [King of the Hill Challenges](king-of-the-hill-challenges.md)

## Sources

- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), section 3
- [Spotting cash rewards](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json) (JSON)
- [Spotting challenge table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_Spotting.json) (JSON)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
