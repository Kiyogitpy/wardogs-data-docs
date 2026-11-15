---
title: "Hot Zone Magnet Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The three Hot Zone Magnet and tower challenges, and their stored cash and Role XP bases."
---

# Hot Zone Magnet Challenges

| Hot Zone Magnet Challenges | |
|---|---|
| **General** | |
| Kind | Event reward |
| Challenges | 3 |
| Cash | 2,500 base (magnet activated) |
| Stored Role XP base | 500 (Magnet Activated), 100 neutral / 300 hostile (Tower Captured) |
| Internal name | DT_Challenges_SessionEvents_KOTH_HotZoneMagnet |
{: .wiki-infobox }

These challenge definitions describe rewards for activating or deactivating a Hot Zone Magnet and capturing towers. The stored expressions do not establish which reward registry currently pays in a match. The mode they belong to is [King of the Hill](../game-modes-and-maps/king-of-the-hill.md). How a tower is captured and how the code works is on [Hot Zone Magnet Towers](../game-modes-and-maps/hot-zone-magnet-towers.md).

## Challenges

| Challenge | What earns it | Cash (base) | Role XP |
|---|---|---|---|
| Magnet Activated | Players in range of an activated magnet | 2,500 | 500 |
| Magnet Deactivated | Players in range of a deactivated magnet | 2,500 | None (cash only) |
| Tower Captured | Players in range of a captured tower | 250 for a neutral tower, 1,500 for a hostile tower (six times the neutral amount) | 100 (300 for a hostile tower) |

The CL516586 round 67 trace selected players on the capturing team within 80 m who were neither dead nor critically wounded; that native recipient path has not been re-established for S3. A neutral tower belongs to no team. A tower is hostile when any team owned it at the moment it was taken: the historical round 92 trace passed the previous owner to the reward, and the reward adds the hostile modifier whenever that owner is not "no team". The tower row pays a neutral and a hostile tower at different amounts: a hostile tower pays six times the neutral cash and 300 Role XP instead of 100. The stored expression reduces the base by 25% per counted repeat, capped at four repeats. Round 92 associated the counter with a 180 s window in CL516586; current counter lifetime and event binding remain unverified. The Magnet Deactivated row pays cash only. The cash table also has a magnet destroyed row worth 150 cash, which the game marks as unused.

This challenge table and the match cash table give different tower amounts: the cash table stores 1,000 for a hostile tower and 250 for a neutral one (see [Cash and Rewards](cash-and-rewards.md#zones-and-towers)). Both are stored in the snapshot; the active registry and current payout path have not been established, as for the other [King of the Hill rewards](king-of-the-hill-challenges.md).

## Season 2 changes

The sources list no Season 2 changes for these challenges.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md)
- [Hot Zone Magnet Towers](../game-modes-and-maps/hot-zone-magnet-towers.md)
- [King of the Hill Challenges](king-of-the-hill-challenges.md)
- [Cash and Rewards](cash-and-rewards.md)

## Sources

- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md), section 6b for the magnet and tower cash
- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), sections 3 and 6
- Hot Zone Magnet challenge table (JSON)
- [Round 67 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round67-maps.md): the capture rule and the 80 m reward range.
- [Round 92 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round92-modes-economy.md): the hostile test and the repeat payout.
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
