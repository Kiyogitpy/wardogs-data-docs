---
title: "VIP Escort"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "A single-life PvE mission on the Kavkazi map in which one random player is the VIP to escort to an extraction helicopter, against 95 Manticore soldiers."
---

# VIP Escort

| VIP Escort | |
|---|---|
| **General** | |
| Mode | PvE mission against AI squads |
| Map or layout | Kavkazi (the data's name; the in-game name is not confirmed) |
| Lives | One: no respawns |
| **Objective** | |
| Objective | Keep the marked VIP alive, reach the extraction area and board the extraction helicopter |
| **Rewards** | |
| Mission rewards | Own loot table: an SV98 sniper rifle and a Fuel Canister |
| Internal name | VIPEscort_01 |
{: .wiki-infobox }

VIP Escort is a PvE mission played against AI squads instead of other players. The mission follows a VIP, who has a tracker on the map and minimap. A player who dies stays out for the rest of the mission.

VIP Escort is a plain-language name taken from the data's internal mission name. The data gives no display name, so this is not confirmed as the in-game title.

## Overview

VIP Escort is one of the three PvE missions in the data, alongside [Hunter Killer](hunter-killer.md) and [Strike and Disarm](strike-and-disarm.md). It is the only mission in the data with its own loot table. The shared PvE rules are described on the [PvE Scenarios](pve-scenarios.md) page.

## Objective and rules

- **Respawns.** None. A player who dies stays out for the rest of the mission.
- **Player faction.** Set to the Valkyra faction.
- **VIP tracker.** The VIP has a persistent tracker on the tactical map and the minimap. The map marker is purple, and the VIP's health state is shown with its own icon for each vitality state.
- **The VIP.** One random player is chosen as the VIP. The VIP is a player, not a soldier.
- **Failure.** The mission fails 10 seconds after the VIP is critically wounded or disconnects.
- **Success.** The team must reach the extraction area with the VIP alive, then board the extraction helicopter. The helicopter is a Little Bird. It appears for the team at one of three entry points and flies a set route.
- **Voice-over.** An intro of three lines, a success line and a failure line.
- **Starting cash.** Each player starts the mission with 2,000 cash. The mission data sets no time limit.
- **Map.** The Kavkazi map, which all three PvE missions share.

## Enemies

The mission has 95 Manticore soldiers: 86 riflemen, 5 marksmen and 4 machine gunners. All of them are on the map from the start, and 31 of the riflemen follow patrol routes. The [AI enemies](ai-enemies.md) page describes their loadouts.

## Rewards

The mission has a loot table of its own with two entries, each with a 100% chance: a [Fuel Canister](../equipment/fuel-canister.md), which does not respawn, and an [SV98](../weapons/sv98.md) sniper rifle with one magazine, which respawns after 10 seconds. The data names the rifle entry "AK", but the item is the SV98, not an AK. The data does not say where this loot is placed or how often it appears.

Other rewards follow the general rules; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). The session-event reward lookup has no rows for PvE missions.

## See also

- [PvE Scenarios](pve-scenarios.md)
- [Hunter Killer](hunter-killer.md)
- [Strike and Disarm](strike-and-disarm.md)
- [AI enemies](ai-enemies.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)

## Sources

- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)

- [Round 36 AI and PvE evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md)
- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md) (the VIP loot table is new in Season 2)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
