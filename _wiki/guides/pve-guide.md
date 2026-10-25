---
title: "PvE Guide"
parent: "Guides"
description: "What each PvE mission asks of the team, how the AI soldiers fight, and what each mission starts with and drops, with every number taken from the PvE articles."
---

# PvE Guide

This guide covers the three PvE missions, which are played against AI squads on the Bakurani world. Every mission ends a life for good, because respawns are off in all of them. Every figure comes from the linked mission and AI articles, so check there for the full rules. Hunter Killer is not finished in the data, so it has its own short section.

## The missions at a glance

| Mission | Objective | Enemies | Starting cash | Loot | Timer |
|---|---|---|---:|---|---|
| [Strike and Disarm](../game-modes-and-maps/strike-and-disarm.md) | Upload the virus at the laptop, then board the extraction helicopter | 53 Lonestar soldiers: 27 at the start, 26 more as a counter-attack | 3,000 | None of its own; see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md) | 5-minute laptop hack |
| [VIP Escort](../game-modes-and-maps/vip-escort.md) | Keep the VIP alive, reach the extraction area and board the extraction helicopter | 95 Manticore soldiers, all on the map from the start | 2,000 | A Fuel Canister and an SV98 | Fails 10 s after the VIP goes critical or disconnects |
| [Hunter Killer](../game-modes-and-maps/hunter-killer.md) | None set | None placed | None set | None set | None set |

Every mission uses the no-respawn rule, so a player who dies stays out for the rest of the mission. The shared rules are on the [PvE Scenarios](../game-modes-and-maps/pve-scenarios.md) page.

## Strike and Disarm

The team has to keep Lonestar soldiers away from the laptop until the virus is uploaded. The data sets 53 Lonestar soldiers: 49 riflemen and 4 snipers. 27 are on the map when the mission starts, six of them on patrol routes. When the laptop hack begins, 26 more riflemen spawn as a single counter-attack wave, and the soldiers are sent to the laptop to stop it.

Tips that follow from the numbers:

- **Because the hack takes 300 seconds once it starts, the team has to hold the laptop for the full five minutes.** The hack has a start and an end line of voice-over, and the data gives no time limit on the mission itself. See [Strike and Disarm](../game-modes-and-maps/strike-and-disarm.md).
- **Because aborting the hack fails the mission, do not stop it to reposition.** The article lists the abort as a fail condition.
- **Because the 26 counter-attack riflemen come as one wave at the start of the hack, the data gives no later waves to plan for.** The team faces that wave, then the rest of the soldiers already on the map.
- **Because a dead player stays out for the rest of the mission, every early death shrinks the team that must hold the laptop for 300 seconds.** See [PvE Scenarios](../game-modes-and-maps/pve-scenarios.md).

## VIP Escort

One random player is chosen as the VIP. The VIP is a player, not a soldier, and has a persistent tracker on the tactical map and the minimap. The team must get the VIP to the extraction area alive, then board the extraction helicopter, which is a Little Bird.

The data sets 95 Manticore soldiers: 86 riflemen, 5 marksmen and 4 machine gunners. All of them are on the map from the start, and 31 of the riflemen follow patrol routes.

Tips that follow from the numbers:

- **Because the VIP is marked on the minimap for the whole mission, the rest of the team can always see where the VIP is.** The marker is purple.
- **Because the mission fails 10 seconds after the VIP is critically wounded or disconnects, a critical VIP leaves a 10-second clock.** The data does not say whether a revive stops that clock, so do not plan on it.
- **Because the SV98 loot entry respawns after 10 seconds and the Fuel Canister entry does not, the rifle is the loot that comes back.** The data does not say where either item is placed. See [VIP Escort](../game-modes-and-maps/vip-escort.md).

## Hunter Killer

Hunter Killer has a map, but its data is unfinished. It sets no soldiers, no objectives, no player faction and no starting cash. The mission has a quest with a start and an end and nothing between them.

Because the data gives nothing to plan for, this mission has no tips in this guide. The [Hunter Killer](../game-modes-and-maps/hunter-killer.md) article lists what is missing.

## The enemy

The AI soldiers use the same behaviour across the missions. Their squads, weapons and loadouts are in the [AI enemies](../game-modes-and-maps/ai-enemies.md) article.

| Squad | Role | Weapon |
|---|---|---|
| Lonestar | Rifleman | [M4](../weapons/m4.md) |
| Lonestar | Sniper | [MK22](../weapons/mk22.md) with a 6-10x scope |
| Manticore | Rifleman | [AK74](../weapons/ak74.md) |
| Manticore | Machine gunner | [PKM](../weapons/pkm.md) |
| Manticore | Marksman | [SVD](../weapons/svd.md) with a 3-6x scope |

Every soldier has 100 HP, the same as a player, and wears [Level 1 Armor](../equipment/level-1-armor.md) and a [Level 1 Helmet](../equipment/level-1-helmet.md). The armor cuts torso damage by 30% and head damage by 30%.

Tips that follow from the numbers:

- **Because a Level 1 Helmet cuts head damage by 30%, the M4 needs three headshots on a soldier where it needs two on an unarmored player.** The M4 does 65.8 to the head with no armor and 46.1 with a Level 1 Helmet, both with full metal jacket. Two hits on the helmeted head give 92.2 (derived), which is under 100 HP. See [Armor](../game-mechanics/armor.md).
- **Because soldiers aim at the head, the helmet is the armor piece that meets their aim.** The data says each soldier aims at the target's head and refreshes its aim every 0.1 s.
- **Because the PvE soldiers' base preset prefers burst fire, and a burst is three shots followed by a 1 s pause, a soldier stops between bursts.** The data gives the burst size and the pause, not the time between shots inside a burst.
- **Because a soldier moves to Combat only once it sees the player, a soldier that has not seen you is at most on Alert.** The levels are Relaxed at 0.0, Alert at 0.8 and Combat at 1.0. Hearing raises the alert level, but the data does not say by how much.
- **Because a standing player is rated 1.0 for visibility, a crouched player 0.4 and a prone player 0.3, staying low lowers the rating a soldier works from.** Firing is rated 5.0, far above standing still, so a shot reveals a player more than stance does. The data does not confirm how these values combine into a chance of being spotted.
- **Because the configured sight range is 2,000 m and the hearing range is 1,000 m, do not plan for those distances.** The data sets two range multipliers, 0.02 for sight and 0.05 for hearing; they do not shorten those ranges but set how fast detection builds up with distance ([AI Enemies](../game-modes-and-maps/ai-enemies.md#how-detection-builds-up)). Worked out from the perception code (not tested in play), a standing, still target in the open reaches full detection by sight in about 16 s at 100 m, and gunfire within about 450 m gives full hearing detection within a second.

## Starting cash and loot

- **Strike and Disarm** starts each player with 3,000 cash.
- **VIP Escort** starts each player with 2,000 cash.
- **Hunter Killer** sets no starting cash.

The VIP Escort loot table has two entries, each with a 100% chance: a [Fuel Canister](../equipment/fuel-canister.md), which does not respawn, and an [SV98](../weapons/sv98.md) with one magazine, which respawns after 10 seconds. The scenario data has no cash or XP table of its own, so other rewards follow the general rules. See [Cash and Rewards](../progression-and-economy/cash-and-rewards.md). The game files set no team size for any mission, so the server decides it.

## Sources

- [PvE Scenarios](../game-modes-and-maps/pve-scenarios.md), [Strike and Disarm](../game-modes-and-maps/strike-and-disarm.md), [VIP Escort](../game-modes-and-maps/vip-escort.md), [Hunter Killer](../game-modes-and-maps/hunter-killer.md) and [AI enemies](../game-modes-and-maps/ai-enemies.md)
- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)
- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Round 41 modes, AI and other evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md): sight and hearing in play (R3)
