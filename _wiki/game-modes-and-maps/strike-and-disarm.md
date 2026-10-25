---
title: "Strike and Disarm"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "A single-life PvE mission on the Bakurani world: the team hacks a laptop while Lonestar soldiers try to stop it, then boards an extraction helicopter."
---

# Strike and Disarm

| Strike and Disarm | |
|---|---|
| **General** | |
| Mode | PvE mission against AI squads |
| Map or layout | The Bakurani world (the data's name: Kavkazi) |
| Lives | One: no respawns |
| **Objective** | |
| Objective | Keep Lonestar soldiers away from the laptop until the virus is uploaded, then board the extraction helicopter |
| **Rewards** | |
| Mission rewards | Not in the data; see Rewards |
| Internal name | StrikeDisarm_01 |
{: .wiki-infobox }

Strike and Disarm is a PvE mission played against AI squads instead of other players. It includes a laptop hack and opens with a four-line voice-over intro. A player who dies stays out for the rest of the mission.

Strike and Disarm is a plain-language name taken from the data's internal mission name. The data gives no display name, so this is not confirmed as the in-game title. The quest's own name in the data is a placeholder, "[PH] Strike and Swipe".

## Overview

Strike and Disarm is one of the three PvE missions in the data, alongside [Hunter Killer](hunter-killer.md) and [VIP Escort](vip-escort.md). It is the mission with the laptop hack. The shared PvE rules are described on the [PvE Scenarios](pve-scenarios.md) page.

## Objective and rules

- **Respawns.** None. A player who dies stays out for the rest of the mission.
- **Downed players.** The mission switches off the rule that skips the downed state, so a player can be downed here, as in King of the Hill.
- **Player faction.** Set to the Manticore faction, the same faction the Manticore AI uses.
- **Laptop hack.** The hack takes 5 minutes (300 seconds) once it starts. It has a start line and an end line of voice-over. Aborting the hack fails the mission.
- **Intro and completion.** Four intro voice-over lines and a mission-complete line.
- **Starting cash.** Each player starts the mission with 3,000 cash. The mission data sets no time limit.
- **Map.** The Bakurani world (the data's name: Kavkazi), which all three PvE missions share.
- **Objectives.** Upload the virus while keeping Lonestar soldiers away from the laptop, then board the extraction helicopter to leave the area.
- **Vehicle spawners.** This mission has 5 vehicle spawners.

## Enemies

The mission has 53 Lonestar soldiers: 49 riflemen and 4 snipers. 27 are on the map when the mission starts, six of them on patrol routes. When the laptop hack begins, 26 more riflemen spawn as a counter-attack, a single wave, and the soldiers are sent to the laptop to stop the hack. The [AI enemies](ai-enemies.md) page describes their loadouts.

## Rewards

The mission has no reward table of its own. No payout for completing the mission is set in the game files, so any payout is decided by the server. Rewards follow the general rules; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). The session-event reward lookup has no rows for PvE missions.

## See also

- [PvE Scenarios](pve-scenarios.md)
- [Hunter Killer](hunter-killer.md)
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
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
