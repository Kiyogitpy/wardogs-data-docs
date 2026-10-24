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
| Health | Not yet known |
| Accuracy | Not yet known |
| Perception and reaction time | Not yet known |
| Internal name | AIC_Lonestar_Rifleman, AIC_Lonestar_Sniper, AIC_Manticore_Rifleman, AIC_Manticore_Machinegunner, AIC_Manticore_Marksman |
{: .wiki-infobox }

The AI enemies are the computer-controlled soldiers that fill the PvE missions. The data defines five soldier types in two squads, each with its own weapon, armor, helmet and magazines. It gives their loadouts and how their alert, cover and squad behaviour is set up, but not their health, accuracy or reaction times.

## Overview

All five PvE soldiers share the same controller, behaviour tree and alert and influence settings. They differ in their loadouts. The data does not say which mission uses which squad; see the Enemies section of each mission, such as [Strike and Disarm](strike-and-disarm.md).

## Squad types and loadouts

| Squad | Role | Weapon | Attachments | Magazine |
|---|---|---|---|---|
| Lonestar | Rifleman | [M4](../weapons/m4.md) | None listed | M4 Standard Mag |
| Lonestar | Sniper | [MK22](../weapons/mk22.md) | 6-10x Scope MRAD | MK22 Standard Mag |
| Manticore | Rifleman | [AK74](../weapons/ak74.md) | AR Multi-Caliber Suppressor | AK74 30 RND Magazine |
| Manticore | Machine gunner | [PKM](../weapons/pkm.md) | GOL Multi-Caliber Suppressor | PKM 100 RND Box |
| Manticore | Marksman | [SVD](../weapons/svd.md) | 3-6x Scope, GOL Multi-Caliber Suppressor | SVDM Standard Magazine |

Every soldier also carries [Level 1 Armor](../equipment/level-1-armor.md) and a [Level 1 Helmet](../equipment/level-1-helmet.md). The data gives a count only for some items: one M4 and two M4 magazines for the Lonestar rifleman, and one MK22 for the Lonestar sniper. All other counts are not yet known.

The weapon, attachment and magazine names are the display names from the game data. For attachments, see [Sights and Optics](../weapons/attachments-sights-and-optics.md) and [Muzzle Devices](../weapons/attachments-muzzle-devices.md).

## Numbers

- **Alert levels.** Relaxed starts at 0.0, Alert at 0.8 and Combat at 1.0. Moving up to Combat requires the soldier to see the player. Moving back down does not require sight.
- **Pressure.** The alert levels are compared with a continuous value. The data has a value named Pressure that is most likely the input, but the data does not say so outright.
- **Influence maps.** The team map has a radius of 1000 and the enemy map a radius of 500. The alert map has a radius of 1000 and is fed by hearing. Units are not yet confirmed.
- **Fire mode priority.** The base preset that the PvE soldiers follow prefers Burst, then Automatic, then Semi-automatic.
- **Health, accuracy, perception range and reaction time.** Not yet known.

## How the AI behaves

- **Alert build-up.** A soldier moves from Relaxed to Alert and then to Combat as pressure builds. Hearing feeds the alert map, and the data does not say how much a sound adds. It needs to see the player to enter Combat.
- **Finding targets.** A soldier picks a target from the threats it knows about.
- **Taking cover.** Soldiers look for nearby cover, cover closer to the enemy and cover that faces the enemy. They also look for peek points off their current cover, peek points toward a sighting, combat positions near the target, and shooting spots in the open.
- **Team awareness.** Soldiers share a team map and an enemy map. Both fade over time, and the enemy map is refreshed every 2 seconds.
- **Computers.** The AI can use a computer as a smart object. The data does not say which missions use this.
- **Example behaviours.** The AI data also has patrol, search, flee and squad attack examples. A squad example includes a query that handles movement tokens, probably so squad members take turns moving. These are example packs, and the data does not confirm that they are used in the live game.
- **Exact action order.** The behaviour tree that sequences these actions is not in the data, so the exact order is not yet known.

## See also

- [PvE Scenarios](pve-scenarios.md)
- [Hunter Killer](hunter-killer.md)
- [Strike and Disarm](strike-and-disarm.md)
- [VIP Escort](vip-escort.md)

## Sources

- [AI game feature](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [PvE game feature](../../game-features/Wardogs_GameFeatures_PvE_v2.md)
- [Weapon and attachment loadout data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json) (display names)
