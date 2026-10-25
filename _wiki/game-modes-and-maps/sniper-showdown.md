---
title: "Sniper Showdown"
parent: "Game Modes & Maps"
group: "Game modes"
description: "A sniper mode where standing still gets you revealed, played on its own zone and a countdown between rounds."
---

# Sniper Showdown

| Sniper Showdown | |
|---|---|
| Type | Sniper mode with a stillness rule |
| Objective | Control zone, with players revealed when they stop moving |
| Win condition | 10 kills, or 30 minutes |
| Maps | Bakurani Outskirts - Jutari, plus two zone layouts for North America and Russia (see [Maps](maps.md)) |
| Server browser label | Sniper Showdown |
| Internal name | SniperShowdown (experience) |
{: .wiki-infobox }

Sniper Showdown is a round-based sniper mode. Its defining rule is stillness: a player who stands still is spotted, and moving again clears it. It has its own zone, a leaderboard and a round timer, and it is one of the modes added to the game as its own experience.

## Overview

Sniper Showdown runs on its own map entry in the server browser, Bakurani Outskirts - Jutari. The data also has two more Sniper Showdown zone layouts, for North America and Russia, but they are not matched to a display name in the sources.

## Rules and objectives

- **Stillness.** Stand within about 50 m of one spot for 90 seconds and you are revealed: a marker shows your position on the map for 200 seconds, and at most three markers show at once. A warning appears at 75 seconds. After a reveal, the check waits 15 seconds before it can count standing still again. The on-screen message reads "Keep moving or you will be revealed." Once spotted, the message is "You have been revealed. Run." Moving clears it with "You are now hidden." The 50 m figure assumes the data's distance unit is centimetres, and the 200 seconds comes from the same settings block. Neither is confirmed in play.
- **Zone.** The mode uses a Control Zone with a seeker that finds the zone. Its zones are 350 m across, with a 75 m Hot Zone and no alternative placements. The Hot Zone moves from the start (first move at 0 seconds), at a default speed of 1.5. See [Control Zone](control-zone.md).
- **Out of bounds.** Leaving both the Control Zone and the Hot Zone puts you in the hostile-zone state. The effect of that state is applied elsewhere in the game, and the data does not give its size.
- **Deaths and respawns.** The death screen shows "Killed by" the attacker's name, then a blackout of 3.0 seconds, then "Respawning in" a countdown.
- **Death explosion.** A player who dies explodes 1.5 seconds later. The blast is set to 250 damage, a radius of 500, an effective radius of 250, a minimum of 30 damage, a falloff of 0.5 and 100 blunt damage. Line of sight is checked. How these values combine into the final damage is not in the data.
- **Round end.** At the end of a round a countdown shows "Next Round in" minutes and seconds, then a scoreboard.
- **Timer and leaderboard.** The timer shows minutes and seconds. A leaderboard is shown during play. A round ends at 10 kills or after 30 minutes. The game files do not describe what the leaderboard shows.
- **Starting loadout.** Each player gets a Scout Backpack and a GGX 17 pistol at spawn.
- **Factions.** The mode is free-for-all. The game prepares a pool of 100 single-player factions and puts each joining player on the non-default faction with the fewest members. With 100 players or fewer, everyone is alone on a faction.
- **Loot points.** Each map has 150 sniper-only loot points, sorted into high-, middle- and low-value points. Kavkazi has 87 high, 21 middle and 42 low. North America has 69 high, 16 middle and 65 low. Russia has 79 high, 19 middle and 52 low.

## Rewards

The data does not list Sniper Showdown-specific cash or XP rewards. The general cash table applies to kills and other actions; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

## See also

- [Control Zone](control-zone.md)
- [King of the Hill](king-of-the-hill.md), which shares the zone rules
- [Maps](maps.md)
- [Challenges](../progression-and-economy/challenges.md)

## Sources

- [Experiences (KOTH and Sniper Showdown)](../../game-features/Wardogs_GameFeatures_Experiences_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Mode rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/mode-rules.json)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
