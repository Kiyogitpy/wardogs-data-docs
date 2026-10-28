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
| Map | The Bakurani world for all three missions (the data's name: Kavkazi) |
| Internal name | PvE (scenario framework) |
{: .wiki-infobox }

PvE Scenarios are missions played against AI squads instead of other players. Every mission ends a life for good, because all four mission rule sets turn respawns off. Each mission has its own objectives, voice-over and AI.

Mission names here are plain-language names taken from the missions' internal names. The game does not give display names for the missions, so these are not confirmed as the in-game titles. Two missions carry placeholder quest names, and the third has no name text at all.

## Overview

The framework has a shared base and a set of missions. Each mission adds its own quest, its own faction settings, and its own voice-over lines. The game shows three missions and one example for testing.

## Individual missions

- [Hunter Killer](hunter-killer.md): the mission with no respawns; it is unfinished, with no soldiers or objectives set.
- [Strike and Disarm](strike-and-disarm.md): the laptop hack mission, with an intro, a hack start and end, and a mission-complete line.
- [VIP Escort](vip-escort.md): the mission that tracks a VIP on the map and has its own loot table.
- [AI enemies](ai-enemies.md): the five PvE soldier types, their loadouts, and how their alert and cover behaviour is set up.

The example scenario used for testing has no article of its own.

## Rules and objectives

- **Respawns.** Every mission uses the no-respawn rule set. A player who dies stays out for the rest of the mission.
- **Hunter Killer.** Its quest has no objectives, and it places no soldiers; its map layer holds only labels.
- **Strike and Disarm.** The player faction is tagged Charlie, the same tag the Manticore AI uses. The mission includes a laptop hack with a start and an end, an intro in four voice-over lines, and a mission-complete line. The hack takes 5 minutes, and the AI soldiers are sent to the laptop to stop it.
- **VIP Escort.** The player faction is tagged Bravo, the Valkyra tag. The mission has an intro in three voice-over lines, a success line and a failure line. It uses its own loot table, but the 21 loot markers in its map layer carry common item names, not the table's two names. One random player is chosen as the VIP, and the team must escort them to the extraction helicopter.
- **AI squads.** The scenario AI comes in five types. The Lonestar squad has a rifleman and a sniper. The Manticore squad has a rifleman, a machine gunner and a marksman. The riflemen carry light armor, a light helmet, a rifle and spare magazines. The sniper and marksman carry scopes.
- **Starting cash.** Each player starts Strike and Disarm with 3,000 cash and VIP Escort with 2,000. Hunter Killer sets none.
- **Timers.** No mission has a time limit. The timers that do exist are the 5-minute laptop hack in Strike and Disarm and the 10-second wait between the VIP going down and VIP Escort failing. After a mission ends, the scenario waits 15 seconds before its post-match step, and the end screen is delayed by 0.5 seconds.
- **Downed players.** The three missions switch off the rule that skips the downed state, so a player can be downed in a mission, as in King of the Hill. The rules for downed players are on the [Downed and Revive](../game-mechanics/downed-and-revive.md) page.
- **Voice-over subtitles.** Every voice-over line in the missions has a subtitle that stays on screen for 10 s.
- **Team sizes.** The game sets no team size for these missions. The session size is a server setting.
- **Shared extraction.** Strike and Disarm and VIP Escort both end with the same extraction helicopter. The helicopter's mission has one start for each of the three team tags, and each mission uses exactly one of them (VIP Escort the Bravo version, Strike and Disarm the Charlie version, in both cases the tag the players have); it appears at the extraction vehicle point with its engine running. A non-player pilot flies it along an entry path at 3 m/s, it waits for players to board, and then it flies the exit path. The speed holds at 3 m/s for the first 70 percent of a path and eases to 1 m/s at the end; both paths use the same speed curve.
- **Soldier behaviour.** Patrol routes are used in Strike and Disarm and VIP Escort. The besiege behaviour is added while the laptop hack runs. Search is included with Strike and Disarm, but no soldier or quest uses it. Flee and the squad attack are example behaviours that no mission uses.

## Rewards

The scenarios have no cash or XP table of their own. The general rules apply; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). None of the four scenario definitions sets a cash reward for finishing a mission, so no completion payout appears in the game. Any payout would be decided elsewhere, and it is not known.

## Layout

All three missions and the example sit in the Bakurani world, in layers of their own, around and mostly outside the King of the Hill zone area of that map. In straight lines, from the game:

| | VIP Escort | Strike and Disarm | Hunter Killer | Example scenario |
|---|---|---|---|---|
| Team start | 1 area, far north | 1 area, far west | none placed (a label only) | 1 area, in the zone area |
| Objective | extraction point | laptop | none placed | one test area 17 m from the start |
| Start to objective | 3,356 m | 2,478 m | label to label 1,050 m | 17 m |
| Soldier spawners | 95 | 53 (26 held for the wave) | 0 | 0 |
| Patrol routes | 16 | 4 | 0 | 0 |
| Vehicle spawners | 6 | 5 | 0 | 0 |
| Loot markers | 21 (common items only) | 0 | 0 | 0 |

- The VIP Escort extraction and the Strike and Disarm helicopter point both lie inside the Bakurani zone area, about 1.4 km and 1.9 km from its centre, in none of the named zone regions. Both missions start outside the zone area (about 2.0 km north and 2.4 km west).
- The helicopter paths of the two missions have the same shape, copied: one arrival path and one departure path each.
- The example scenario is a test stub: a start area, an equipment vendor, one test area and two test objects, all within 17 m of each other and near the middle of the Bakurani zone area.

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
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md)
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 71 PvE layouts (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round71-pve-layouts.md): placed objects, positions and distances. Static analysis; positions are straight-line metres in the map frame.
