---
title: "King of the Hill"
parent: "Game Modes & Maps"
group: "Game modes"
description: "The main three-team zone-capture mode: hold the Control Zone and its Hot Zone against two other factions."
---

# King of the Hill

| King of the Hill | |
|---|---|
| Type | Three-team zone capture |
| Teams | Three factions: Lonestar, Valkyra and Manticore |
| Objective | Hold the Control Zone and the Hot Zone inside it |
| Win condition | First team to 100 points; no time limit |
| Maps | Bakurani, Ozeti, Zestafona, Saburtulo, and four more (see [Maps](maps.md)) |
| Server browser label | KOTH |
| Internal name | KOTH (experience) |
{: .wiki-infobox }

King of the Hill (KOTH) is the main team mode. Three factions fight over a Control Zone on a map, and the zone's inner Hot Zone pays more than the outer zone. The mode runs on the [Control Zone](control-zone.md) rules, so the zone sizes, moving Hot Zones and capture rules are described there.

## Overview

King of the Hill is the mode most of the maps are built for. The server browser lists it on four main maps (Bakurani, Ozeti, Zestafona and Saburtulo) and on four further entries (Berlin, Paris, Mindori and Tevza) that have no zone data in the game files. Tank Town, a separate server browser entry, uses these same rules. Every KOTH match uses the Control Zone runtime and three factions.

Players earn cash and XP from the zone and from fights around it. Challenges such as kills, revives and vehicle kills run during the match, and there are 60 KOTH-specific challenge rows; see [Challenges](../progression-and-economy/challenges.md).

## Rules and objectives

- **Factions.** Three teams are set up at the start of the match. The factions are named in the data as Lonestar, Valkyra and Manticore.
- **Match flow.** A match goes through four stages: waiting for the world to load, waiting for enough players, playing, then post-match. The lobby needs 60 players and waits up to 10 seconds for them. If that does not fill, a 5 second ready-up step needs at least 9 players. The post-match screen lasts 45 seconds.
- **Scoring the zone.** A player counts toward capturing the zone only while alive. A critically wounded or dead player adds nothing. See [Control Zone](control-zone.md).
- **Hot Zone.** Each Control Zone has a Hot Zone in its centre. The Hot Zone moves during the match. Kills and captures inside it pay more than in the outer zone.
- **Hot Zone Magnet.** Players can build and activate a Hot Zone Magnet. While it is active, kills in the Hot Zone pay the highest multiplier in the game. Capturing hostile or neutral towers also counts.
- **Spawning.** KOTH has its own spawn manager. Your first spawn is in your faction's spawn area. The game picks a random start point in that area and, if it is taken, moves on to the next free point. There is no forward operating base step, and no enemy-distance rule like the one Deathmatch uses. Which spawn area a player gets on the maps other than Bakurani is not confirmed. The data does not describe a starting kit for KOTH players.
- **Win condition.** The first team to reach 100 points wins, which is the game's default score limit. A point is added every 22 seconds (the example server file uses 24 seconds). There is no time limit.
- **Team balance.** A team may be at most 2 players larger than the smallest team. The game's default leaves this lock off; the example server file turns it on.
- **Player cap.** The maximum number of players is a server setting, which can be set between 60 and 100.

## Rewards

Cash for the zone, from the cash tables:

| Event | Base cash |
|---|---|
| Control Zone contested, owned or not owned | 150 each |
| Entering the Control Zone (first time in a life) | 100 |
| Hot Zone contested, owned or not owned | 600 each |
| Entering the Hot Zone | 0 |
| Activating the Hot Zone Magnet | 5,000 |
| Capturing a hostile tower | 1,000 |
| Capturing a neutral tower | 250 |
| Spawn vehicle reaching the Control Zone | 3,000 |

Kills in the zones are multiplied. A kill inside a Hot Zone counts with a weight of 10, a kill in a Control Zone with a weight of 5, and a kill in the enemy's own Hot Zone with a weight of 4. The full kill formula is on [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

At the end of the match, factions are ranked and paid a flat placement bonus: 200 cash for first, 150 for second and 100 for third. Separately, Season 2 added a 10,000 cash bonus for the Lonestar faction only; the other two factions get none. Earned cash and XP also get a percentage bonus by placement, described on [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

## See also

- [Control Zone](control-zone.md)
- [Maps](maps.md)
- [Challenges](../progression-and-economy/challenges.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Sniper Showdown](sniper-showdown.md), which uses the same zone rules

## Sources

- [Experiences (KOTH and Sniper Showdown)](../../game-features/Wardogs_GameFeatures_Experiences_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [ControlZone regions](../../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md)
- [KOTH challenges](../../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Maps and gym data](../../content/Wardogs_Maps_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md)
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md)
- [Mode rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/mode-rules.json)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
