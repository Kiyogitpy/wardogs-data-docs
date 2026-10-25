---
title: "AI Enemies"
parent: "Game Modes & Maps"
group: "PvE missions"
description: "The computer-controlled soldiers of the PvE missions: five types in the Lonestar and Manticore squads, their loadouts, and how their alert, cover and squad behaviour is set up."
---

# AI Enemies

| AI Enemies | |
|---|---|
| **General** | |
| Type | Computer-controlled infantry in PvE missions |
| Squads | Lonestar (rifleman, sniper) and Manticore (rifleman, machine gunner, marksman) |
| **Combat** | |
| Health | 100, the same as a player |
| Accuracy | No AI-specific value; they shoot with their weapon's own spread and recoil |
| Sight and hearing | Configured radius 2,000 m sight and 1,000 m hearing; the range in play is not confirmed |
| Reaction time | No reaction-time value; a soldier waits 2 s after noticing a threat before it moves to cover |
| Internal name | AIC_Lonestar_Rifleman, AIC_Lonestar_Sniper, AIC_Manticore_Rifleman, AIC_Manticore_Machinegunner, AIC_Manticore_Marksman |
{: .wiki-infobox }

The AI enemies are the computer-controlled soldiers that fill the PvE missions. The data defines five soldier types in two squads, each with its own weapon, armor, helmet and magazines. It gives their health, senses, firing, loadouts, and how their alert, cover and squad behaviour is set up. The data has no AI-specific accuracy value, and their reaction timing is only partly known.

## Overview

All five PvE soldiers share the same controller, behaviour tree and alert and influence settings. They differ in their loadouts. [Strike and Disarm](strike-and-disarm.md) uses the Lonestar squad, [VIP Escort](vip-escort.md) uses the Manticore squad, and [Hunter Killer](hunter-killer.md) places no soldiers. Counts for each mission are under Where the soldiers appear.

## Squad types and loadouts

| Squad | Role | Weapon | Attachments | Magazine |
|---|---|---|---|---|
| Lonestar | Rifleman | [M4](../weapons/m4.md) | None listed | M4 Standard Mag |
| Lonestar | Sniper | [MK22](../weapons/mk22.md) | 6-10x Scope MRAD | MK22 Standard Mag |
| Manticore | Rifleman | [AK74](../weapons/ak74.md) | AR Multi-Caliber Suppressor | AK74 30 RND Magazine |
| Manticore | Machine gunner | [PKM](../weapons/pkm.md) | GOL Multi-Caliber Suppressor | PKM 100 RND Box |
| Manticore | Marksman | [SVD](../weapons/svd.md) | 3-6x Scope, GOL Multi-Caliber Suppressor | SVDM Standard Magazine |

Every soldier also carries [Level 1 Armor](../equipment/level-1-armor.md) and a [Level 1 Helmet](../equipment/level-1-helmet.md). Each soldier carries one of its weapon and two spare magazines for it.

The weapon, attachment and magazine names are the display names from the game data. For attachments, see [Sights and Optics](../weapons/attachments-sights-and-optics.md) and [Muzzle Devices](../weapons/attachments-muzzle-devices.md).

## Health and armor

- **Health.** An AI soldier has 100 health, the same as a player. The soldiers are built on the player character, and the data sets no separate health value for them.
- **Armor and helmet.** Every soldier wears Level 1 Armor and a Level 1 Helmet, so hits to the body and the head are handled the same way as for players. See [Armor](../game-mechanics/armor.md).
- **Damage.** The data has no damage multiplier that applies only to AI soldiers. The normal damage rules are the only ones found for them.

## Senses and detection

| Setting | Value |
|---|---|
| Sight range | 2,000 m |
| Distance at which a soldier loses sight of a player | 2,100 m |
| Hearing range | 1,000 m |
| How long a soldier remembers what it saw or heard | 30 s |
| How long a soldier remembers a hit | 10 s |

These are the configured radii, not confirmed distances in play. The perception setup also carries two range multipliers, 0.02 for sight and 0.05 for hearing, and how the game combines them with the radii is not known. A soldier may therefore notice a player at far less than 2 km, but the real sight and hearing distance has not been measured or decoded, so do not rely on either figure.

- **Threat build-up.** A soldier builds up a detection level for a player and loses it again over time. The fade starts 5 s after the last detection and runs at 0.25 per second, so a full level is gone in about 4 seconds.
- **How visible a player is.** The data sets a value of 1.0 for a standing player, 0.4 for a crouching player and 0.3 for a prone player. Firing a weapon is set at 5.0, far above standing still, and movement speed also feeds into hearing. How these values combine into a chance of being spotted is not confirmed.

## Firing and aim

- When a soldier uses burst fire, it fires three shots per burst, with a 1 s pause between bursts.
- It aims at the target's head and refreshes its aim every 0.1 s.
- The data has no AI-specific spread or accuracy value. Soldiers shoot with their weapon's own spread and recoil; see [Spread and recoil](../game-mechanics/spread-and-recoil.md).

## Where the soldiers appear

- **Strike and Disarm:** 53 Lonestar soldiers, 49 riflemen and 4 snipers. 27 are on the map from the start, six of them on patrol routes. When the laptop hack begins, 26 more riflemen spawn as one counter-attack wave.
- **VIP Escort:** 95 Manticore soldiers, 86 riflemen, 5 marksmen and 4 machine gunners. All start on the map, and 31 of the riflemen follow patrol routes.
- **Hunter Killer:** no soldiers. The mission places none in the data.

## Numbers

- **Alert levels.** Relaxed starts at 0.0, Alert at 0.8 and Combat at 1.0. Moving up to Combat requires the soldier to see the player. Moving back down does not require sight.
- **Pressure.** The alert levels are compared with a continuous value. The data has a value named Pressure that is most likely the input, but the data does not say so outright.
- **Influence maps.** The team map has a radius of 1000 and the enemy map a radius of 500. The alert map has a radius of 1000 and is fed by hearing. Units are not yet confirmed.
- **Fire mode priority.** The base preset that the PvE soldiers follow prefers Burst, then Automatic, then Semi-automatic.
- **Health and senses.** See Health and armor and Senses and detection above.

## How the AI behaves

- **Alert build-up.** A soldier moves from Relaxed to Alert and then to Combat as pressure builds. Hearing feeds the alert map, and the data does not say how much a sound adds. It needs to see the player to enter Combat.
- **Finding targets.** A soldier picks a target from the threats it knows about.
- **Taking cover.** Soldiers look for nearby cover, cover closer to the enemy and cover that faces the enemy. They also look for peek points off their current cover, peek points toward a sighting, combat positions near the target, and shooting spots in the open.
- **Team awareness.** Soldiers share a team map and an enemy map. Both fade over time, and the enemy map is refreshed every 2 seconds.
- **Computers.** In Strike and Disarm, soldiers are sent to the laptop to stop the hack. The data shows no other mission using this.
- **Behaviours in the missions.** Patrol sends soldiers along set routes in VIP Escort and Strike and Disarm. The besiege behaviour is added to the soldiers while the laptop hack runs. Search is included with Strike and Disarm, but no soldier or quest in the data uses it. Flee and the squad attack are example behaviours that no mission uses. A squad example includes a query that handles movement tokens, probably so squad members take turns moving.
- **Action order.** Each soldier runs its behaviour in this order. First, if it is on Alert, it stops its current task, looks toward the stimulus and waits 2 s before it finds cover or peeks. Otherwise it takes a job when it has none, runs the goal of that job, and falls back to idling. It attacks only in Combat with line of sight to the player: it shoots from cover first, then moves along cover, and shoots in the open only when neither works. A burst is three rounds, and it reloads when its magazine is empty. Its target is refreshed every 1.5 seconds.

## See also

- [PvE Scenarios](pve-scenarios.md)
- [Hunter Killer](hunter-killer.md)
- [Strike and Disarm](strike-and-disarm.md)
- [VIP Escort](vip-escort.md)

## Sources

- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)
- [Weapon and attachment loadout data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json) (display names)

- [Round 36 AI and PvE evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
