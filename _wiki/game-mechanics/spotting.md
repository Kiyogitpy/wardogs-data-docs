---
title: "Spotting"
parent: "Game Mechanics"
description: "How spotting marks enemies on the map, how much cash spotting and destroying a spotted target pay, and what the Recon skills change."
---

# Spotting

| Spotting | |
|---|---|
| Spot a target | Shows it on the map and in the world |
| Spotting pays | 15 to 275 cash for a spot |
| Destroying a spotted target pays | 50 to 500 cash |
| Spotter's share of the top amount | 20% for a spot, 75% for a destroy |
| Recon skills | Increased time to be spotted; increased spotted duration |
{: .wiki-infobox }

Spotting lets a player mark an enemy so that the whole team can see it on the map and in the world. A spotted target is also worth cash, and destroying a spotted target pays more. This article covers how the marking works and what it pays. Base payouts for each kind of target are in the challenge tables, which are not summarised here.

## Overview

Spotting has two events. A **target spotted** event happens when an enemy is marked. A **spotted target destroyed** event happens when a marked enemy is removed, usually by being destroyed. Both events pay cash, and both pay different amounts for each kind of target: a player, a vehicle, a buildable, a supply crate or a stationary weapon. Assists, the teammates who helped, get a separate share of the pay.

## How it works

- **Marking.** A spotted target shows on the team map and as a marker in the world, so the team can see where it is.
- **How long a spot lasts.** On infantry a spot takes 0.5 s to register, fades over 30 s and is kept for up to 180 s. Rotary and wheeled vehicles take 0.75 s to spot and stay spotted 60 s (180 s kept); tracked vehicles take 1.25 s and stay 90 s. Bases and buildings stay spotted for up to 3,600 s.
- **Pay on spot.** Spotting pays between 15 and 275 cash. The spotter gets a share of the top amount, which is 20% of the 275 maximum.
- **Pay on destroy.** Destroying a spotted target pays between 50 and 500 cash. The spotter gets 75% of the 500 maximum for the destroy.
- **Role XP.** A spot pays 5 to 100 Role XP (25 for a player). Destroying a spotted target pays 5 to 500 (150 for a player). A target destroyed by the enemy pays a quarter of its cash and half its Role XP.
- **Assists.** Teammates who help with the spot or the destroy get their own share, set by a separate modifier.
- **Repeats.** The data lowers the pay for a target type after repeated kills of that same type. The exact reduction per repeat is not yet known.
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

Base payouts for each kind of target (vehicle, buildable, player and so on) are on the challenge tables, and are not repeated here. The Season 2 change to them is listed on the [Season 2 Game Modes and Maps page](../../season-2-changes/game-modes-maps.md).

## Tips that follow from the numbers

- **Spot first, then destroy.** The destroy event pays far more than the spot (a 75% share against 20%), so spotting a target and then destroying it earns the most.
- **Spot high-value targets for the team.** Because the team sees the marker, a spot helps everyone even when the spotter does not get the kill.
- **Pick the Recon skills that fit your role.** The increased time for enemies to spot you helps stay hidden, and the longer spotted time keeps targets on the map.
- **Expect smaller pay for repeats.** Repeated spots of the same kind of target earn less each time.

## Not yet known

- How the spot times hold up in play. The values come from the spotting data; the game was not run to time them.
- The base payout for every target type. It is in the challenge tables, not on this page.
- The payout for spotting a player. The data has a calculator row but no lookup for it.
- The exact reduction for repeat targets.

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
