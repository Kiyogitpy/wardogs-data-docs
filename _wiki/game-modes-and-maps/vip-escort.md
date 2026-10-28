---
title: "VIP Escort"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "A single-life PvE mission on the Bakurani world in which one random player is the VIP to escort to an extraction helicopter, against 95 Manticore soldiers."
---

# VIP Escort

| VIP Escort | |
|---|---|
| **General** | |
| Mode | PvE mission against AI squads |
| Map or layout | The Bakurani world (the data's name: Kavkazi) |
| Lives | One: no respawns |
| **Objective** | |
| Objective | Keep the marked VIP alive, reach the extraction area and board the extraction helicopter |
| **Rewards** | |
| Mission rewards | Own loot table: an SV98 sniper rifle and a Fuel Canister |
| Internal name | VIPEscort_01 |
{: .wiki-infobox }

VIP Escort is a PvE mission played against AI squads instead of other players. The mission follows a VIP, who has a tracker on the map and minimap. A player who dies stays out for the rest of the mission.

VIP Escort is a plain-language name taken from the mission's internal name. The game gives no display name, so this is not confirmed as the in-game title. The quest's own name is a placeholder, "[PH] VIP Escort".

## Overview

VIP Escort is one of the three PvE missions, alongside [Hunter Killer](hunter-killer.md) and [Strike and Disarm](strike-and-disarm.md). It is the only mission with its own loot table. The shared PvE rules are described on the [PvE Scenarios](pve-scenarios.md) page.

## Objective and rules

- **Respawns.** None. A player who dies stays out for the rest of the mission.
- **Player faction.** Set to the Valkyra faction.
- **Downed players.** The mission switches off the rule that skips the downed state, so a player can be downed here, as in King of the Hill.
- **VIP tracker.** The VIP has a persistent tracker on the tactical map and the minimap. The map marker is purple, and the VIP's health state is shown with its own icon for each vitality state.
- **The VIP.** One random player is chosen as the VIP. The VIP is a player, not a soldier.
- **Failure.** The mission fails 10 seconds after the VIP goes down (reaches the critical state). The countdown starts the moment the VIP drops and nothing stops it: a revive inside those 10 seconds does not cancel it, and the normal bleed-out time (see [Downed and Revive](../game-mechanics/downed-and-revive.md)) does not matter here. The VIP needs to stay on their feet.
- **VIP disconnects.** This does not fail the mission. If the VIP leaves, the game picks another random player as the new VIP.
- **Success.** The team must reach the extraction area with the VIP alive, then board the extraction helicopter. The helicopter is a Little Bird. It appears at the extraction point and flies a set route; the map layer holds one arrival path and one departure path, so there is only one place it can come from. The mission always starts the Valkyra-tagged (Bravo) version of the helicopter, the same tag the players have; nothing chooses at random.
- **Voice-over.** An intro of three lines, a success line and a failure line.
- **Starting cash.** Each player starts the mission with 2,000 cash. The mission sets no time limit.
- **Map.** The Bakurani world (the game's internal name: Kavkazi), which all three PvE missions share.
- **Vehicle spawners.** This mission has 6 vehicle spawners.

## Enemies

The mission has 95 Manticore soldiers: 86 riflemen, 5 marksmen and 4 machine gunners. All of them are on the map from the start, and 31 of the riflemen follow patrol routes. The [AI enemies](ai-enemies.md) page describes their loadouts.

## Rewards

The mission has a loot table of its own with two entries, each with a 100% chance: a [Fuel Canister](../equipment/fuel-canister.md), which does not respawn, and an [SV98](../weapons/sv98.md) sniper rifle with one magazine, which respawns after 10 seconds. The game names the rifle entry "AK", but the item is the SV98, not an AK. Loot appears at marker points placed in the map, and each marker is named after one of the loot entries. When the match starts, the game creates the loot at every marker whose name matches an entry; neither VIP Escort entry is limited to a control zone, so both appear straight away. The chance is rolled once per marker (100% for both, so always), and when an entry lists several items the game picks one by weight. The mission's map layer does hold 21 loot markers, but they are named for common items (bandages, weapons, defibs, armor, a helmet), not for these two entries; no marker for the SV98 or the Fuel Canister is in the mission's own layer, so where they lie is not known (see Layout).

Other rewards follow the general rules; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). The session-event reward lookup has no rows for PvE missions.

## Layout

The mission is placed in the Bakurani world, in its own map layer. Distances below are straight lines, not road lengths, and come from the game, not from play.

- **Start.** One spawn area with one equipment vendor, in the far north of the world, about 2,000 m north of the King of the Hill zone area on Bakurani and about 3,800 m from the centre of that zone area. There is no vehicle vendor and no deployment board there. No separate start point for the VIP is placed: the VIP is a random player, so the VIP starts with the team.
- **Extraction.** One extraction trigger, marked on the map as a circle about 80 m in radius, with the helicopter's arrival point 51 m from it. It lies inside the Bakurani zone area, about 1,400 m from its centre, and in none of the named zone regions (the nearest is Riverside Forest, 235 m away).
- **Distance.** From the spawn area to the extraction point is about 3,350 m in a straight line. There is no other objective on the way: no bomb, laptop or disarm site is placed.
- **Soldiers.** 95 soldier spawners (86 riflemen, 5 marksmen, 4 machine gunners), one soldier each (inferred). 26 stand within 1,000 m of the spawn area, 34 between 1,000 and 2,000 m, 24 between 2,000 and 3,000 m and 11 beyond 3,000 m. The nearest is 370 m from the spawn; 9 stand within 500 m of the extraction point. 16 patrol routes are placed, used by 31 riflemen. No area is set that ties the soldiers to one place.
- **Vehicles.** 6 vehicle spawners: 3 Bobcats, 1 Kodiak and 2 Kodiak pickups. The nearest is 350 m from the spawn area and the farthest 2,196 m.
- **Loot.** 21 loot markers are placed, all on the shared loot names: 12 Bandage, 3 Weapon, 3 Defib (cheap), 1 Sniper, 1 Armor and 1 Helmet. None carries the name of the mission's own two entries (the SV98 and the Fuel Canister), so no marker for those two is in this layer. The markers sit in five spots: the spawn area (1, 50 m away), a house (4, about 390 m), a road block (6, 620 to 660 m), a compound (8, about 1,800 m) and a logging camp (2, about 2,190 m).
- **Built objects.** 69 pre-placed buildables: 62 concrete barriers, 5 tank traps, 1 bunker and 1 forward base. The bunker, base and tank traps form the road block about 650 m from the spawn area; the barriers are spread along the route.
- **Triggers.** One trigger box (the extraction area) and one navigation volume. The helicopter has one arrival path (four path points, about 50 m long) and one departure path.

## See also

- [PvE Scenarios](pve-scenarios.md)
- [Hunter Killer](hunter-killer.md)
- [Strike and Disarm](strike-and-disarm.md)
- [AI enemies](ai-enemies.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)

## Sources

- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)

- [Round 36 AI and PvE evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md)
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md)
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md)
- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md) (the VIP loot table is new in Season 2)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 59 open questions evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round59-open-questions.md): the revive clock, the VIP re-pick and loot placement.
- [Round 71 PvE layouts (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round71-pve-layouts.md): placed objects, positions and distances. Static analysis; positions are straight-line metres in the map frame.
