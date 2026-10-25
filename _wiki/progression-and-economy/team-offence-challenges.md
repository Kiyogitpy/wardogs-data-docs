---
title: "Team Offence Challenges"
parent: "Progression & Economy"
group: "Unlocks"
description: "The two Team Offence challenges, for punishing a kill and for voting on a teamkill. A voter forgive pays 500 cash; a punished kill pays points, not cash."
---

# Team Offence Challenges

| Team Offence Challenges | |
|---|---|
| **General** | |
| Kind | Event reward |
| Challenges | 2 |
| Auto-activate | Yes |
| Reward | Forgive pays 500 cash; a punished kill pays points, not cash |
| Internal name | DT_Challenges_SessionEvents_TeamOffence |
{: .wiki-infobox }

Team Offence challenges belong to the [Team Offence](../game-modes-and-maps/team-offence.md) mode. They cover punishing a kill and voting on a teamkill. The voter's forgive decision pays 500 cash. A punished kill is scored in points rather than cash.

## Challenges

| Challenge | What earns it | Cash | Role XP |
|---|---|---|---|
| Team Offence Punish | Punishing a kill in Team Offence. Pays points, not cash: 1 to 5 points per kill (see below). | None (points instead) | No row |
| Teamkill Voter | Voting on a teamkill. A forgive decision pays 500 cash. | 500 | No row |

### Punish points

The punish value is the damage contribution plus 5, multiplied by a cause multiplier, then kept between 1 and 5 points. The cause multipliers are 0.1 for a Claymore kill and an environment kill (so they reach the minimum of 1 point), 0.8 for an explosive kill (4 points), and 1.0 for a headshot, sniper or precision-artillery kill and for any other cause (5 points). When the kill was flagged as a teamkill, the value is then divided by 2.5, so a flagged kill is worth 2 points at most and a flagged Claymore or environment kill is worth 0.4. These points are derived from the reward expression, not checked in play. Derived from the round 43 reward expression (https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md).

The forgive reward is cash only. The voter's decision decides whether it is paid: a forgive decision grants 500 cash, and a reject does not.

## Season 2 changes

- The Season 02 update added the punish challenge and the teamkill voter challenge.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Team Offence](../game-modes-and-maps/team-offence.md)

## Sources

- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the forgive cash, and the punish points on the reward expression.
- [Round 43 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md): the minimum of 1 point in the punish expression, applied before the flagged division.
- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), sections 3 and 6
- [Team Offence challenge table](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/DT_Challenges_SessionEvents_TeamOffence.json) (JSON)
