---
title: "Sniper Showdown"
parent: "Game Modes & Maps"
description: "A sniper mode where standing still gets you revealed, played on its own zone and a countdown between rounds."
---

# Sniper Showdown

| Sniper Showdown | |
|---|---|
| Type | Sniper mode with a stillness rule |
| Objective | Control zone, with players revealed when they stop moving |
| Maps | Bakurani Outskirts - Jutari, plus two zone layouts for North America and Russia (see [Maps](maps.md)) |
| Server browser label | Sniper Showdown |
| Internal name | SniperShowdown (experience) |
{: .wiki-infobox }

Sniper Showdown is a round-based sniper mode. Its defining rule is stillness: a player who stands still is spotted, and moving again clears it. It has its own zone, a leaderboard and a round timer, and it is one of the modes added to the game as its own experience.

## Overview

Sniper Showdown runs on its own map entry in the server browser, Bakurani Outskirts - Jutari. The data also has two more Sniper Showdown zone layouts, for North America and Russia, but they are not matched to a display name in the sources.

## Rules and objectives

- **Stillness.** Standing still reveals you. The on-screen message reads "Keep moving or you will be revealed." Once spotted, the message is "You have been revealed. Run." Moving clears it with "You are now hidden." The time or distance that counts as standing still is not in the data.
- **Zone.** The mode uses a Control Zone with a seeker that finds the zone. Its zones are 350 m across, with a 75 m Hot Zone and no alternative placements. The Hot Zone moves from the start (first move at 0 seconds), at a default speed of 1.5. See [Control Zone](control-zone.md).
- **Out of bounds.** A component handles players who leave the play area. The rules inside it are not in the data.
- **Deaths and respawns.** The death screen shows "Killed by" the attacker's name, then a blackout of 3.0 seconds, then "Respawning in" a countdown.
- **Round end.** At the end of a round a countdown shows "Next Round in" minutes and seconds, then a scoreboard.
- **Timer and leaderboard.** The timer shows minutes and seconds. A leaderboard is shown during play. The round length and the leaderboard's contents are not in the data.
- **Starting loadout.** Each player gets a Scout Backpack and a GGX 17 pistol at spawn.
- **Factions and team sizes.** Players are assigned factions by a component. How many factions, and team sizes, are not yet known.

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
