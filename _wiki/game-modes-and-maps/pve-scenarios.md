---
title: "PvE Scenarios"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "Single-life PvE missions against AI squads: Hunter Killer, Strike and Disarm, and VIP Escort, with their objectives and AI factions."
---

# PvE Scenarios

| PvE Scenarios | |
|---|---|
| Type | Player-versus-AI missions |
| Missions | Hunter Killer, Strike and Disarm, VIP Escort (plus an example scenario for testing) |
| Respawns | None: death in a scenario is final |
| Factions | Three: Lonestar, Valkyra and Manticore |
| Map | Kavkazi for all three missions (the data's name; the in-game name is not confirmed) |
| Internal name | PvE (scenario framework) |
{: .wiki-infobox }

PvE Scenarios are missions played against AI squads instead of other players. Every mission in the data ends a life for good, because all four mission rule sets turn respawns off. Each mission has its own objectives, voice-over and AI.

Mission names here are plain-language names taken from the data's internal mission names. The data does not give display names for the missions, so these are not confirmed as the in-game titles.

## Overview

The framework has a shared base and a set of missions. Each mission adds its own quest, its own faction settings, and its own voice-over lines. The data shows three missions and one example for testing.

## Individual missions

- [Hunter Killer](hunter-killer.md): the mission with no respawns; its data is unfinished, with no soldiers or objectives set.
- [Strike and Disarm](strike-and-disarm.md): the laptop hack mission, with an intro, a hack start and end, and a mission-complete line.
- [VIP Escort](vip-escort.md): the mission that tracks a VIP on the map and has its own loot table.
- [AI enemies](ai-enemies.md): the five PvE soldier types, their loadouts, and how their alert and cover behaviour is set up.

The example scenario used for testing has no article of its own.

## Rules and objectives

- **Respawns.** Every mission uses the no-respawn rule set. A player who dies stays out for the rest of the mission.
- **Hunter Killer.** Its quest has no objectives in the data, and it places no soldiers.
- **Strike and Disarm.** The player faction is tagged Charlie, the same tag the Manticore AI uses. The mission includes a laptop hack with a start and an end, an intro in four voice-over lines, and a mission-complete line. The hack takes 5 minutes, and the AI soldiers are sent to the laptop to stop it.
- **VIP Escort.** The player faction is tagged Bravo, the Valkyra tag. The mission has an intro in three voice-over lines, a success line and a failure line. It uses its own loot table. One random player is chosen as the VIP, and the team must escort them to the extraction helicopter.
- **AI squads.** The scenario AI comes in five types. The Lonestar squad has a rifleman and a sniper. The Manticore squad has a rifleman, a machine gunner and a marksman. The riflemen carry light armor, a light helmet, a rifle and spare magazines. The sniper and marksman carry scopes.
- **Starting cash.** Each player starts Strike and Disarm with 3,000 cash and VIP Escort with 2,000. Hunter Killer sets none.
- **Timers.** No mission has a time limit in its data. The timers that do exist are the 5-minute laptop hack in Strike and Disarm and the 10-second wait between the VIP going down and VIP Escort failing.
- **Team sizes.** Not yet known.
- **Shared extraction.** Strike and Disarm and VIP Escort both end with the same extraction helicopter. It appears for the player's team at one of three entry points and flies a set route.
- **Soldier behaviour.** Patrol routes are used in Strike and Disarm and VIP Escort. The besiege behaviour is added while the laptop hack runs. Search is included with Strike and Disarm, but no soldier or quest in the data uses it. Flee and the squad attack are example behaviours that no mission uses.

## Rewards

The scenario data has no cash or XP table of its own. The general rules apply; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

## See also

- [Challenges](../progression-and-economy/challenges.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Shooting Range](shooting-range.md)

## Sources

- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)
- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)

- [Round 36 AI and PvE evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md)
