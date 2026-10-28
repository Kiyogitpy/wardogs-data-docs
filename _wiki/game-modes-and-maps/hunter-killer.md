---
title: "Hunter Killer"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "A single-life PvE mission on the Bakurani world with no respawns. It is unfinished: no soldiers, objectives or player faction are set."
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
| Mission rewards | None set in the game files; see Rewards |
| Internal name | HunterKiller_01 |
{: .wiki-infobox }

Hunter Killer is a PvE mission played against AI squads instead of other players. A player who dies stays out for the rest of the mission. Like every PvE mission, it uses the shared setup with three teams. The mission is unfinished: it has a map layer that holds only labels, and no soldiers, objectives or player faction are set.

Hunter Killer is a plain-language name taken from the mission's internal name. The game gives no display name, so this is not confirmed as the in-game title.

## Overview

Hunter Killer is one of the three PvE missions, alongside [Strike and Disarm](strike-and-disarm.md) and [VIP Escort](vip-escort.md). It uses the shared PvE base described on the [PvE Scenarios](pve-scenarios.md) page: the no-respawn rule and the scenario quest log and trackers.

## Objective and rules

- **Respawns.** None. A player who dies stays out for the rest of the mission.
- **Teams.** Like the other PvE missions, it uses the shared three-team setup. The game sets no faction tag and no starting cash for the player on this mission, so there is no starting side to state.
- **Objectives.** None are set. The mission's quest has only a start and an end, with no steps between them.
- **Map.** The Bakurani world (the game's internal name for it is Kavkazi). No time limit is set.
- **Starting cash.** None is set for this mission.
- **Downed players.** The mission switches off the rule that skips the downed state, so a player can be downed here, as in King of the Hill.
- **Name.** The game has no name text for this mission at all, so the title above is a working name.
- **Completion cash.** No payout for finishing the mission appears in the game.

## Enemies

No AI soldiers are placed on the map, so the mission has no enemies. The map has placeholder labels such as Guards (4), Patrol (7) and Lieutenant Location (2), but no soldiers. The [AI enemies](ai-enemies.md) page describes the soldiers used in the other two PvE missions.

## Rewards

The game has no reward table and no cash payout for this mission, so any payout is decided by the server. Rewards follow the general rules; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). The session-event reward lookup has no rows for PvE missions.

## Layout

The mission has a placed layer in the Bakurani world, but it holds only developer labels and scenery, not game objects. There are 16 hidden text labels and 9 scenery actors. No spawn area, soldier spawner, vendor, vehicle spawner, objective or trigger is placed, and no loot marker.

The labels sketch a plan: one "Deploy Location" (the team's start), one "HVT Location" (the target), two "Lieutenant Location" labels, 4 "Guards" labels, 7 "Patrol" labels and one "Exfil Location". The distances between them are about 1,050 m from the deploy label to the target, 192 m from the target to the exfil label and 1,240 m from deploy to exfil. The plan sits at the western edge of the Bakurani zone area: the deploy label is 740 m outside it, the target label 136 m outside and the exfil label 32 m outside.

The target, exfil and one guard label lie 78 m, 79 m and 49 m from the laptop, helicopter point and compound of [Strike and Disarm](strike-and-disarm.md), and a lieutenant label 88 m from its wave trigger. This suggests (inferred) that Hunter Killer was sketched on the same compound and never built out.

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
- [Round 71 PvE layouts (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round71-pve-layouts.md): placed objects, positions and distances. Static analysis; positions are straight-line metres in the map frame.
