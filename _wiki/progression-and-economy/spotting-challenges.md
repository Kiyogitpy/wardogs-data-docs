---
title: "Spotting Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The two spotting challenges, with stored cash and Role XP expressions for spotting and removing targets."
---

# Spotting Challenges

## Announced S3 spotted-target rewards

The [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) give these rewards for a spotted target being killed/destroyed, not for initially marking it. Vehicle variants are preserved exactly; the unspecified spawn-vehicle class is not expanded into guessed variants.

| Target | Resource | Earlier | S3 |
|---|---|---:|---:|
| AH-6M Littlebird [Miniguns] / AH-6R Littlebird [Rockets] | cash | 1,000 | 850 |
| Z20 Lakota [Miniguns] | cash | 1,400 | 1,200 |
| L2A6 | cash | 3,300 | 3,000 |
| T-72B3 | cash | 2,400 | 2,000 |
| Hot Zone Magnet | cash | 1,650 | 1,500 |
| Player | XP | 150 | 125 |
| FOB | XP | 250 | 200 |
| Hot Zone Magnet | XP | 225 | 200 |
| Spawn vehicles | XP | 500 | 400 |

These announced gameplay amounts take precedence over older payout advice. Retained match-score values are separate resources, not evidence that these rewards are unavailable. Exact event routing and modifiers still need current consumer evidence.

| Spotting Challenges | |
|---|---|
| **General** | |
| Kind | Event reward |
| Challenges | 2 |
| Cash | Stored challenge bases: 5 to 750 (spotted); 10 to 5,000 (removed), before modifiers |
| Role XP | 5 to 100 per spot; 5 to 400 per destroyed target (25 and 125 for a player) |
| Internal name | DT_Challenges_SessionEvents_KOTH_Spotting |
{: .wiki-infobox }

The two stored spotting definitions describe rewards for marking and removing a target. Their cash and Role XP expressions are configured reward rules; current activation and actual payments remain unresolved.

## Challenges

| Challenge | What earns it | Cash | Role XP |
|---|---|---|---|
| Target Spotted | A player successfully spots a target | Stored base 5 to 750, before modifiers | 5 to 100 (25 for a player) |
| Spotted Target Destroyed | A spotted target is destroyed. Pays the players who spotted it. | Stored base 10 to 5,000, before modifiers | 5 to 400 (125 for a player) |

The 15–275 and 50–500 cash figures belong to the separate match-score tables, not to the per-target challenge bases. Current challenge rows store 5–750 cash for spotting and 10–5,000 for removal, before their alignment, zone, repeat and build-progress factors. Which reward path is active in a match remains unresolved. The Role XP per target type is set by the target: an armoured vehicle or aircraft pays more than a supply crate or mine. The removal expressions store a 0.25 cash factor for destruction by the enemy. Role XP uses a target-specific selector, not a universal half: the player row stores 125 normally and 75 for KilledByEnemyReward. These are saved expression inputs, not verified payouts.

## Season 2 changes

The sources list no Season 2 changes for these challenges.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [King of the Hill Challenges](king-of-the-hill-challenges.md)

## Sources

- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), section 3
- Spotting cash rewards (JSON)
- Spotting challenge table (JSON)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
