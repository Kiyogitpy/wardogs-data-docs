---
title: "Hot Potato"
parent: "Game Modes & Maps"
group: "Game modes"
description: "A Season 2 pre-lobby mini-game: players pass the Gold Potato while they wait for a match, and the points it earns become starting cash."
---

# Hot Potato

| Hot Potato | |
|---|---|
| Type | Pre-lobby mini-game (Season 2) |
| Added | Season 2 |
| Items | Three Gold Potato items, labelled Alpha, Bravo and Charlie in the data |
| Points | 10 times the pass multiplier for each pass |
| Teams, match length and win condition | None: it is not a match mode |
| Internal name | HotPotato (game feature) |
{: .wiki-infobox }

Hot Potato is a mini-game played in the pre-lobby, the waiting area before a match starts. Players pass the Gold Potato to each other, and each pass earns points. Those points are paid out as starting Cash when the match begins. It is not a match mode, so it has no teams, match length or win condition.

## Overview

Hot Potato came in with Season 2 alongside [Team Offence](team-offence.md). The pre-lobby has other mini-games as well: the game's pre-lobby reward reasons name a shooting game and a soccer game. These are the moving practice targets (a hit pays points equal to its damage) and the soccer pitch (a goal pays 50, an assist 25) that stand in each team spawn area. See [Boundaries and Safe Zones](boundaries-and-safe-zones.md).

## Rules and objectives

- **Passing.** Each pass of the Gold Potato pays 10 times the pass multiplier, in pre-lobby points. The multiplier is a whole number. A new potato starts at 1, and each pass adds 1: when a thrown potato reaches another player, the potato that player ends up with has the thrown potato's multiplier plus 1. So passes pay 10, 20, 30 and so on. No upper limit was found.
- **Items.** There are three Gold Potato items. They share one name in the game's text, with the description "Don't hold it for too long..." and the flavour line "Hot. Hot. Hot." The game labels them Alpha, Bravo and Charlie, and they differ only in their tag. The potato is thrown like a grenade, overarm or underarm.
- **Fuse.** Each potato runs a hidden timer that picks a random time between 8 and 15 seconds, then shortens it by a factor of 0.85 for every point of the multiplier, so a potato that has been passed many times goes off sooner. At multiplier 1 the time is about 6.8 to 12.8 seconds, and at multiplier 5 about 3.5 to 6.7 seconds (worked out from the game code, not timed in play). When the timer ends while a player is holding the potato, it goes off in their hands: the game plays the grenade explosion effect on that player, announces that the potato was destroyed, and removes it from their inventory. The game shows no other penalty: the potato's explosion damage and impact damage are both 0, and nothing takes points away. The only cost is losing the potato, which ends the chain of pass rewards (read from the game code and item stats, not seen in play).
- **Damage.** The potato does no damage according to the item stats, whether it is thrown or goes off in the holder's hands.
- **Map tracker.** The mode has its own map tracker.
- **Teams, match length and win condition.** None. The game runs while players wait for the match to start.

## Rewards

The points from Hot Potato go into the same pre-lobby award as the other pre-lobby mini-games. The game's defaults give a first award of 150 points and a periodic award of 250 points every 60 seconds, with a cap of 5,000 points on the amount waiting for the match. When the match starts, the waiting points are paid as starting Cash at one Cash per point, and the player gets a first-purchase discount (see [Shops](../progression-and-economy/shops.md)). Points are only paid to players who have been in the lobby for at least 15 seconds. The full rules are in [Pre-lobby](pre-lobby.md). The game does not show what the points buy beyond that.

## See also

- [Pre-lobby](pre-lobby.md), how the points turn into Cash
- [Team Offence](team-offence.md), the other Season 2 addition
- [Factions](factions.md), each of which has its own Hot Potato item
- [Maps](maps.md)

## Sources

- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Challenges](../../game-features/Wardogs_Challenges_v1.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
