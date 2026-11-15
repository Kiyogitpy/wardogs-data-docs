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
| Win condition | ScoreLimit=100; stored hard-cap/inactivity values are 0 (runtime meaning unverified) |
| Saved browser listings | Bakurani, Ozeti, Zestafona, Saburtulo, and four more; active availability unverified (see [Maps](maps.md)) |
| Server browser label | KOTH |
| Internal name | KOTH (experience) |
{: .wiki-infobox }

King of the Hill (KOTH) is the main team mode. Three factions fight over a Control Zone on a map, and the zone's inner Hot Zone pays more than the outer zone. The mode runs on the [Control Zone](control-zone.md) rules, so the zone sizes, moving Hot Zones and capture rules are described there.

## Overview

King of the Hill is the mode most of the maps are built for. The saved server-browser table lists it on four main maps (Bakurani, Ozeti, Zestafona and Saburtulo) and on four further entries (Berlin, Paris, Mindori and Tevza) that have no zone data in the game. Tank Town, a separate server browser entry, uses these same rules. The experience configuration references the Control Zone feature and three factions; current server availability is not established by that configuration.

Players earn cash and XP from the zone and from fights around it. Challenges such as kills, revives and vehicle kills run during the match, and there are 62 KOTH-specific challenge rows; see [Challenges](../progression-and-economy/challenges.md).

## Rules and objectives

- **Factions.** Three teams are set up at the start of the match. The factions are named in the game as Lonestar, Valkyra and Manticore.
- **Match flow.** A match goes through four stages: waiting for the world to load, waiting for enough players, playing, then post-match. The current config stores 60 players / 10 seconds for PlayerCount and 9 players / 5 seconds for ReadyUpKOTH. The CL516586 native trace starts each countdown only after its readiness condition holds; it does not give the lobby ten seconds to fill and then fall back to nine players. S3 timer activation remains unverified. The current post-match setting stores 45 seconds. The wait before the match is the [Pre-lobby](pre-lobby.md), where points earned turn into starting Cash.
- **At the start of the match.** CL516586 round 70 identified removal of lobby activities and activation of match systems. Its selected-subscriber search found no teleport, health restore or inventory clear, but left callees untraced. S3 reset, persistence and pre-lobby Cash conversion remain unresolved; see [Pre-lobby](pre-lobby.md).
- **Scoring the zone.** A player counts toward capturing the zone only while alive. A critically wounded or dead player adds nothing. See [Control Zone](control-zone.md).
- **Hot Zone.** Each Control Zone has a Hot Zone in its centre. The Hot Zone moves during the match. Kills and captures inside it pay more than in the outer zone.
- **Hot Zone Magnet.** Players can build and activate a Hot Zone Magnet. While it is active, kills in the Hot Zone pay the highest multiplier in the game. Capturing hostile or neutral towers also counts. Each map also has numbered towers: a team captures towers to learn a secret code and types it on a tower keypad to pull the Hot Zone to that tower. See [Hot Zone Magnet Towers](hot-zone-magnet-towers.md).
- **Spawning.** KOTH has its own spawn manager. Your first spawn is in your faction's spawn area. The game picks a random start point in that area and, if it is taken, moves on to the next free point. There is no forward operating base step, and no enemy-distance rule like the one Deathmatch uses. Which spawn area a player gets on the maps other than Bakurani is not confirmed. The game does not describe a starting kit for KOTH players.
- **Win condition.** The first team to reach 100 points wins, which is the game's default score limit. A point is added every 22 seconds (the example server file uses 24 seconds). The current config stores MatchHardCapSeconds=0 and InactivityTimeoutSeconds=0; their S3 runtime interpretation has not been verified.
- **Team balance.** A team may be at most 2 players larger than the smallest team. The game's default leaves this lock off; the example server file turns it on.
- **Player cap.** The maximum number of players is a server setting, which can be set between 60 and 100.

## Rewards

King of the Hill challenge rewards use the shared challenge reward rows that every mode's challenges use. In that table a player kill pays 300 cash and 250 Role XP, a defibrillator revive 600 and 250, and a bandage heal 200 and 80 (base amounts, before the zone and assist terms). The cash tables on [Cash and Rewards](../progression-and-economy/cash-and-rewards.md) list different bases for the same actions (a default kill 250, a defibrillator revive 1,000, a Bandage heal 400), and the active registry and payout path have not been established, so the amounts here are stored bases rather than verified match payouts. The full list is on [King of the Hill Challenges](../progression-and-economy/king-of-the-hill-challenges.md).

Stored zone cash values from the separate match cash table; current activation and effective payment remain unresolved:

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

The placement table stores flat faction bonuses: 200 cash for first, 150 for second and 100 for third. Separately, Season 2 added a 10,000 cash entry for Lonestar and zero entries for the other two factions; this does not establish current payments. Earned cash and XP also get a percentage bonus by placement, described on [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

## See also

- [Control Zone](control-zone.md)
- [Maps](maps.md)
- [Challenges](../progression-and-economy/challenges.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Pre-lobby](pre-lobby.md), the wait before the match
- [Sniper Showdown](sniper-showdown.md), which uses the same zone rules
- [King of the Hill Guide](../guides/king-of-the-hill-guide.md), practical tips for the main maps

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
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
