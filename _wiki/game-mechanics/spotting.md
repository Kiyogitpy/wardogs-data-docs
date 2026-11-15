---
title: "Spotting"
parent: "Game Mechanics"
description: "How spotting marks enemies on the map, how much cash spotting and destroying a spotted target pay, and what the Recon skills change."
---

# Spotting

S3 reduces several spotted-target kill rewards, including Player XP from 150 to **125** and FOB XP from 250 to **200**. The full announced cash/XP table is on [Spotting Challenges](../progression-and-economy/spotting-challenges.md#announced-s3-spotted-target-rewards), sourced to the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). The older match-score ranges below are not the announced target-specific payouts.

| Spotting | |
|---|---|
| Spot a target | Shows it on the map and in the world |
| Stored match-score range | 15 to 275 cash for a spot; active payout path unresolved |
| Stored removal match-score range | 50 to 500 cash; distinct challenge bases below |
| Match-score spotter-share fields | 20% for a spot, 75% for a destroy; current application unresolved |
| Recon skills | Increased time to be spotted; increased spotted duration |
{: .wiki-infobox }

Spotting lets a player mark an enemy so that the whole team can see it on the map and in the world. The saved reward tables configure cash and Role XP for spotting and target removal, but disagree on their bases and do not establish the active payout path. This article separates those stored reward values from marking behavior. Base payouts for each kind of target are in the challenge tables, which are not summarised here.

## Overview

Spotting has two events. A **target spotted** event happens when an enemy is marked. A **spotted target destroyed** event happens when a marked enemy is removed, usually by being destroyed. Both have stored cash expressions with target-specific amounts for a player, a vehicle, a buildable, a supply crate or a stationary weapon. Assists, the teammates who helped, get a separate share of the pay.

## How it works

- **Marking.** A spotted target shows on the team map and as a marker in the world, so the team can see where it is.
- **How long a spot lasts.** On infantry a spot takes 0.5 s to register, fades over 30 s and is kept for up to 180 s. Rotary and wheeled vehicles take 0.75 s to spot and stay spotted 60 s (180 s kept); tracked vehicles take 1.25 s and stay 90 s. Bases and buildings stay spotted for up to 3,600 s.
- **Pay on spot.** The separate match-score table stores 15–275 cash and a 20% spotter-share field; current application is unresolved. Challenge rows instead store target-specific bases of 5–750.
- **Pay on destroy.** The separate match-score table stores 50–500 cash and a 75% spotter-share field; current application is unresolved. Challenge removal rows instead store bases of 10–5,000.
- **Role XP.** Challenge rows store bases of 5 to 100 Role XP for a spot (25 for a player). Removal rows store 5 to 400 (125 for a player). The removal expressions store a quarter-cash factor for destruction by the enemy; Role XP uses a target-specific value (75 instead of 125 for a player), not a universal half.
- **Assists.** Teammates who help with the spot or the destroy get their own share, set by a separate modifier.
- **Repeats.** Spotting has its own repeat rule, harsher than the one for kills. Each repeat of the same kind of target pays 50% less than the one before, counted up to two repeats. The pay is the base times (1 minus 0.5 for each repeat counted), so by the reward formula the second spot of the same kind of target pays half and the third and later spots pay nothing. The same cut applies to the Role XP, to spotting and to the destroy that follows. The game keeps a 180 s cooldown with the repeat counter, which most likely means a repeat count starts again after 180 s without a repeat (inferred from the setting's name). Kills use a different rule (24% less per repeat, up to four repeats).
- **Buildables.** In Season 2, buildable and stationary targets pay in proportion to how much they were built, so an unfinished buildable pays less.
- **Recon skills.** Two skills change spotting. One increases how long it takes for enemies to spot you. The other increases how long enemies stay spotted after you spot them. The spotted time is multiplied by 1.2 at skill level 2 and 1.4 at level 4.

## Numbers

Cash for spotting, from the match-score table:

| Event | Minimum | Maximum |
|---|---:|---:|
| Target spotted | 15 | 275 |
| Spotted target destroyed | 50 | 500 |

Share of the top amount for the spotter:

| Event | Spotter share |
|---|---:|
| Target spotted | 20% |
| Spotted target destroyed | 75% |

The challenge tables store target-specific bases before modifiers; these are not verified payouts. For a player the base is 100 cash and 25 Role XP for a spot (half of that, 50 cash and 12.5 Role XP, when the spot only refreshes an existing one), and 400 cash and 125 Role XP when the spotted player is destroyed. Other targets run from 5 to 750 cash and 5 to 100 Role XP on a spot, and from 10 to 5,000 cash and 5 to 400 Role XP on a destroy; the rest are not repeated here. These challenge values differ from the match-score table above, and the files do not show which of the two the payout uses. The Season 2 change to them is listed on the [Season 2 Game Modes and Maps page](../../season-2-changes/game-modes-maps.md).

## Tips that follow from the numbers

- **Reward comparison.** The separate match-score fields favor removal over spotting, but their activation is unresolved; they do not establish which sequence earns the most in S3.
- **Spot high-value targets for the team.** Because the team sees the marker, a spot helps everyone even when the spotter does not get the kill.
- **Pick the Recon skills that fit your role.** The increased time for enemies to spot you helps stay hidden, and the longer spotted time keeps targets on the map.
- **Repeat expression.** The stored 50% reduction gives half the base at count 1 and zero at count 2. Which events increment that count and when it resets remain unresolved.

## Not yet known

- How the spot times hold up in play. The values come from the game's spotting settings; the game was not run to time them.
- The base payout for every target type. It is in the challenge tables, not on this page.
- How the repeat counter is kept in play: which targets count as the same kind, and when it starts again. The reduction itself (50% a repeat, up to two) is known from the game.

## See also

- [Health and Damage](health-and-damage.md)
- [Movement](movement.md)
- [Season 2 Game Modes and Maps changes](../../season-2-changes/game-modes-maps.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)

## Sources

- [GameFeature: Spotting Reference](../../game-features/Wardogs_GameFeatures_Spotting_v2.md)
- [Game Modes & Maps changes (Season 2)](../../season-2-changes/game-modes-maps.md)
- [Player & Movement changes (Season 2)](../../season-2-changes/player-movement.md)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
