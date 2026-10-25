---
title: "Team Offence"
parent: "Game Modes & Maps"
group: "Match rules"
description: "Season 2: teamkill offences are handled by player ballots that can punish, kick or forgive the offender."
---

# Team Offence

| Team Offence | |
|---|---|
| Type | Game-mode plugin for teamkill offences |
| Added | Season 2 |
| How it works | Player ballots on an offence: punish, kick, or forgive |
| Teams | Not applicable to a fixed mode; the plugin runs alongside other modes |
| Internal name | TeamOffence (game feature) |
{: .wiki-infobox }

Team Offence is a Season 2 game-mode plugin that deals with teamkilling. When a player is accused of an offence, a ballot opens and players vote on what happens. Season 2 also removed the older teamkill tracking feature.

## Overview

Team Offence adds its own challenges, a punish challenge, a voter challenge and its own reward feed. Its values are tied to the punish and voter challenges and the ballot.

## Rules and objectives

- **Ballots.** When an offence is recorded, a ballot opens or joins a ballot that is already open. Players vote on the offender. Pending ballots queue up one after another.
- **Vote outcomes.** The notices in the data are: offender punished, offender kicked, voter punish, voter kick, voter forgive, voter safe-zone forgive, and voter expired. A voter who leaves the safe zone before deciding records a "forgive by leave" vote, and a voter whose time runs out is recorded as having given up (voter expired).
- **Vehicle crashes.** A vehicle crash can count as a team offence in the challenge data.
- **Challenges.** The "Teamkill Voter" challenge tracks voting, and the "Team Offence Punish" challenge tracks the punish outcome.
- **Numbers.** A vote on an offence is open for 180 seconds. When the offence is recorded, the game sets the vote's deadline to 180 seconds after the offence, and sends that deadline to the voters' prompts, which close when it passes (inferred from the game code, not seen in play). A voter who has not decided by then is recorded as expired. Once an offender reaches 15 points, a kick vote follows. A vote has a 60-second self-defence window. Punishment bans step up through 10 minutes, 25 minutes, 1 hour and 1 day. Forgiveness lasts 7 days. A 15-minute cooldown follows a rejected reward. A voter who leaves the safe zone before deciding is recorded as Forgive. These are the plugin's built-in defaults; the exported game config has no section for them.
- **Team sizes and timers.** Not applicable: the plugin runs alongside other modes.

## Rewards

A forgive decision pays the voter 500 cash and no XP. A punished kill pays points rather than cash: 1 to 5 points, or 2 at most (0.4 for a Claymore or environment kill) when the kill was flagged as a teamkill (see [Team Offence challenges](../progression-and-economy/team-offence-challenges.md#punish-points)). Points are not cash, so they do not add to the cash total.

## See also

- [Challenges](../progression-and-economy/challenges.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Hot Potato](hot-potato.md), the other Season 2 mode

## Sources

- [Challenges](../../game-features/Wardogs_Challenges_v1.md)
- [KOTH challenges](../../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
