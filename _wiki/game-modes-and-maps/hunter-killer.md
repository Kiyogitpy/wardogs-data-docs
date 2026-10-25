---
title: "Hunter Killer"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "A single-life PvE mission on the Bakurani world with no respawns. Its data is unfinished: no soldiers, objectives or player faction are set."
---

# Hunter Killer

| Hunter Killer | |
|---|---|
| **General** | |
| Mode | PvE mission against AI squads |
| Map or layout | The Bakurani world (the data's name: Kavkazi) |
| Lives | One: no respawns |
| **Objective** | |
| Objective | None set: the mission data is unfinished |
| **Rewards** | |
| Mission rewards | Not in the data; see Rewards |
| Internal name | HunterKiller_01 |
{: .wiki-infobox }

Hunter Killer is a PvE mission played against AI squads instead of other players. A player who dies stays out for the rest of the mission. Like every PvE mission, it uses the shared setup with three teams. The mission data is unfinished: it has a map, but no soldiers, objectives or player faction are set.

Hunter Killer is a plain-language name taken from the data's internal mission name. The data gives no display name, so this is not confirmed as the in-game title.

## Overview

Hunter Killer is one of the three PvE missions in the data, alongside [Strike and Disarm](strike-and-disarm.md) and [VIP Escort](vip-escort.md). It uses the shared PvE base described on the [PvE Scenarios](pve-scenarios.md) page: the no-respawn rule and the scenario quest log and trackers.

## Objective and rules

- **Respawns.** None. A player who dies stays out for the rest of the mission.
- **Teams.** Like the other PvE missions, it uses the shared three-team setup. The game files set no faction for the player on this mission, so which side the player starts on is not in the data.
- **Objectives.** None are set. The mission's quest has only a start and an end, with no steps between them.
- **Map.** The Bakurani world (the data's name for it is Kavkazi). No time limit is set in the data.
- **Starting cash.** None is set for this mission.
- **Downed players.** The mission switches off the rule that skips the downed state, so a player can be downed here, as in King of the Hill.
- **Name.** The data has no name text for this mission at all, so the title above is a working name.
- **Completion cash.** No payout for finishing the mission appears in the game files.

## Enemies

No AI soldiers are placed on the map, so the mission has no enemies in the data. The map has placeholder labels such as Guards and Patrol, but no soldiers. The [AI enemies](ai-enemies.md) page describes the soldiers used in the other two PvE missions.

## Rewards

The data has no reward table and no cash payout for this mission, so any payout is decided by the server. Rewards follow the general rules; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). The session-event reward lookup has no rows for PvE missions.

## See also

- [PvE Scenarios](pve-scenarios.md)
- [Strike and Disarm](strike-and-disarm.md)
- [VIP Escort](vip-escort.md)
- [AI enemies](ai-enemies.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)

## Sources

- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)
- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)

- [Round 36 AI and PvE evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md)
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md)
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
