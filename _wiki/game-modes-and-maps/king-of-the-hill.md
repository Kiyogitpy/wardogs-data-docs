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
| Maps | Bakurani, Ozeti, Zestafona, Saburtulo, and four more (see [Maps](maps.md)) |
| Server browser label | KOTH |
| Internal name | KOTH (experience) |
{: .wiki-infobox }

King of the Hill (KOTH) is the main team mode. Three factions fight over a Control Zone on a map, and the zone's inner Hot Zone pays more than the outer zone. The mode runs on the [Control Zone](control-zone.md) rules, so the zone sizes, moving Hot Zones and capture rules are described there.

## Overview

King of the Hill is the mode most of the maps are built for. The server browser lists it on four main maps (Bakurani, Ozeti, Zestafona and Saburtulo) and on four further maps that have no display name in the data. Every KOTH match uses the Control Zone runtime and three factions.

Players earn cash and XP from the zone and from fights around it. Challenges such as kills, revives and vehicle kills run during the match, and there are 60 KOTH-specific challenge rows; see [Challenges](../progression-and-economy/challenges.md).

## Rules and objectives

- **Factions.** Three teams are set up at the start of the match. The factions are named in the data as Lonestar, Valkyra and Manticore.
- **Match flow.** A match goes through four stages: waiting for the world to load, waiting for enough players, playing, then post-match.
- **Scoring the zone.** A player counts toward capturing the zone only while alive. A critically wounded or dead player adds nothing. See [Control Zone](control-zone.md).
- **Hot Zone.** Each Control Zone has a Hot Zone in its centre. The Hot Zone moves during the match. Kills and captures inside it pay more than in the outer zone.
- **Hot Zone Magnet.** Players can build and activate a Hot Zone Magnet. While it is active, kills in the Hot Zone pay the highest multiplier in the game. Capturing hostile or neutral towers also counts.
- **Spawning.** KOTH has its own spawn manager. The data does not describe a starting kit for KOTH players.
- **Team sizes, match length and win condition.** Not yet known.

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
