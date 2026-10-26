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
| Mission rewards | None set in the game files; see Rewards |
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

## Layout

The mission is placed in the Bakurani world, in its own map layer. Distances below are straight lines, not road lengths, and come from the game files, not from play.

- **Start.** One spawn area in the far west of the world, about 2,400 m west of the Bakurani zone area of King of the Hill. It has an equipment vendor, a vehicle vendor, one vehicle spawner (a Kodiak pickup) and an area for the team to appear in with room for 15 spawn points.
- **Laptop.** One laptop, the only objective site, 2,478 m from the spawn area in a straight line. It stands just outside the western edge of the Bakurani zone area (64 m) and 799 m from the nearest named zone region (Green Farmland). A map circle of about 200 m radius marks the compound around it, and a smaller target area sits 30 m from the laptop for the counter-attack.
- **Extraction.** The mission always starts the Manticore-tagged (Charlie) version of the helicopter, the same tag the players have. The helicopter arrives 219 m from the laptop and the end marker is 177 m from it, both inside the Bakurani zone area (738 m from Riverside Forest). The spawn area to the end marker is 2,551 m.
- **Soldiers.** 53 soldier spawners (49 riflemen, 4 snipers), one soldier each (inferred). The 27 at the start stand mostly around the laptop: 13 within 100 m, and the farthest 406 m away. The 26 for the counter-attack wave stand 232 to 541 m from it (about 490 m typical) and are released by one trigger 385 m from the laptop. All wave soldiers and 22 of the start soldiers are tied to one compound area. 6 soldiers use the 4 patrol routes. The nearest soldier is 2,282 m from the spawn area, so the team meets none of them near the start.
- **Vehicles.** 5 vehicle spawners: the one at the spawn area and 4 Kodiak pickups for the Lonestar side, 99 to 143 m from the laptop.
- **Other placed objects.** One ladder blockout 485 m west of the laptop. No loot markers are placed.
- **Triggers and volumes.** One compound area for the soldiers, one target area for the wave, one spawn area for the team, one navigation volume and one wave trigger.

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
- [Round 71 PvE layouts (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round71-pve-layouts.md): placed objects, positions and distances. Static analysis; positions are straight-line metres in the map frame.
