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
| Sight and hearing | Sight reaches 2,000 m but builds up slowly with distance; gunfire is heard almost at once out to about 450 m |
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

The weapon, attachment and magazine names are the display names from the game data. For attachments, see [Sights and Optics](../attachments/sights-and-optics.md) and [Muzzle Devices](../attachments/muzzle-devices.md).

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

The two range multipliers in the data (0.02 for sight and 0.05 for hearing) do not shorten these ranges. They set how fast detection builds up with distance instead. The figures below are worked out from the game's detection formulas and the data's values. They were not timed in play.

### How detection builds up

Each soldier keeps a detection level from 0 to 1 for each player it knows about. The level rises with what the soldier sees and hears of that player, and it fades when nothing new comes in.

- **Sight.** A player who is standing still in the open, seen from the front, takes about 8 s to reach full detection at 10 m, about 16 s at 100 m and about 35 s at 500 m. Sight keeps building out to 2,000 m, but very slowly, and adds nothing beyond that. A crouching player is seen about 2.5 times more slowly and a prone player about 3.3 times more slowly. Sprinting is about 3 times faster than standing still. A soldier that is not facing the player builds up more slowly, and not at all from directly behind. A player whose body is mostly hidden by cover is also seen more slowly.
- **Gunfire.** A shot is heard almost at once. Inside about 450 m, one shot fills a full level within a second. A player driving a vehicle is heard at about a fifth of the gunfire rate. A player who stands still makes no sound.
- **Footsteps.** Footsteps barely register. Running adds about 0.75 per second at 10 m and under 0.01 per second at 100 m.
- **Hits.** A hit on a soldier adds a fixed amount (1.0 in the data) to its detection. The detection level is capped at 1.0, so one hit takes a soldier to full detection in one step (derived from the perception code, not tested in play).
- **Fading.** A soldier that loses sight keeps its level for 5 s. After that the level falls by 0.25 per second, so a full level is gone about 4 seconds later.
- **Vehicle noise.** Vehicles have three configured noise ranges: engine 100 m, horn 500 m and a destroyed vehicle 800 m. Which game events make these noises count for the AI is not confirmed.
- **Other hearing.** Which other events create hearing signals is not confirmed. Hearing is zero beyond 1,000 m.

## Firing and aim

- When a soldier uses burst fire, it fires three shots per burst, with a 1 s pause between bursts.
- It aims at the target's head and refreshes its aim every 0.1 s.
- The data has no AI-specific spread or accuracy value. Soldiers shoot with their weapon's own spread and recoil; see [Spread and recoil](../game-mechanics/spread-and-recoil.md).

## Where the soldiers appear

- **Strike and Disarm:** 53 Lonestar soldiers, 49 riflemen and 4 snipers. 27 are on the map from the start, six of them on patrol routes. When the laptop hack begins, 26 more riflemen spawn as one counter-attack wave.
- **VIP Escort:** 95 Manticore soldiers, 86 riflemen, 5 marksmen and 4 machine gunners. All start on the map, and 31 of the riflemen follow patrol routes.
- **Hunter Killer:** no soldiers. The mission places none in the data.

## Numbers

- **Alert levels.** Relaxed is 0.0, Alert 0.8 and Combat 1.0. A soldier uses the highest detection level of its own and of its squad-mates, so one soldier that sees you alerts the rest of the squad. Alert needs no sight of the player. To move up to Combat, the soldier must also see the player at that moment. Once in Combat it stays there while the level is held at 1.0, and it does not need sight to stay.
- **Dropping back.** When the player is out of sight, the level fades as described under Senses and detection. The soldier leaves Combat as soon as the level drops below 1.0, then Alert below 0.8, so a few seconds out of sight is enough to calm it down.
- **Pressure.** The alert levels are compared with the detection level described above. A value named Pressure also appears in the data, but its role was not confirmed.
- **Influence maps.** The team map has a radius of 1000 and the enemy map a radius of 500. The alert map has a radius of 1000 and is fed by hearing. Every map has a strength of 1.0. The alert map fades by 1% per second and refreshes every 0.5 s, while the team map fades by 10% per second and refreshes every 5 s, and the enemy map by 10% per second and every 2 s. The alert map is the one soldiers use to pick a place to search. Units are not yet confirmed.
- **Fire mode priority.** The base preset that the PvE soldiers follow prefers Burst, then Automatic, then Semi-automatic.
- **Health and senses.** See Health and armor and Senses and detection above.

## How the AI behaves

- **Alert build-up.** A soldier moves from Relaxed to Alert and then to Combat as its detection level rises. Its squad's detections count too, and the team and enemy maps carry that awareness between soldiers. Hearing feeds the alert map, and how much a sound adds to a soldier's detection is set by the hearing rules above: a nearby shot adds a full level within a second, a vehicle a fifth of that, footsteps almost nothing. The data has no separate fixed "alert amount" per sound.
- **Finding targets.** A soldier picks its target among the living players it has seen, heard or been damaged by, and it checks again every 1.5 s. A downed player is not chosen, because the check looks for the Alive state.
- **Taking cover.** Each search for a place to move to is a scored query. The game gathers candidate spots, throws out the ones that fail its tests, and picks the best of the rest. For cover, it looks within a configured search radius of 3,000 units (the data gives no unit) and keeps at least 200 units from living teammates. It prefers cover that faces the enemy, cover from which a line trace reaches the enemy, and cover within the weapon's range. It also looks for peek points off its current cover, peek points toward a sighting, combat positions near the target and shooting spots in the open. The weighting of each test is in the data's query files and is not summarised here.
- **Team awareness.** Soldiers share a team map and an enemy map. Both fade over time, and the enemy map is refreshed every 2 seconds.
- **Computers.** In Strike and Disarm, soldiers are sent to the laptop to stop the hack. The data shows no other mission using this.
- **Behaviours in the missions.** Patrol sends soldiers along set routes in VIP Escort and Strike and Disarm. The besiege behaviour is added to the soldiers while the laptop hack runs. Search is included with Strike and Disarm, but no soldier or quest in the data uses it. Flee and the squad attack are example behaviours that no mission uses. A squad example includes a query that handles movement tokens, probably so squad members take turns moving.
- **Action order.** Each soldier runs its behaviour in this order. First, if it is on Alert, it stops its current task, looks toward the stimulus and waits 2 s before it finds cover or peeks. Otherwise it takes a job when it has none, runs the goal of that job, and falls back to idling. It attacks only in Combat with line of sight to the player: it shoots from cover first, then moves along cover, and shoots in the open only when neither works. A burst is three rounds, and it reloads when its magazine is empty. Its target is refreshed every 1.5 seconds.

## Layout

The map layers of the missions place the soldiers one spawner each (inferred). In straight lines from the team's start:

- **VIP Escort.** 95 spawners spread along the whole route: 26 within 1,000 m of the start, 34 at 1,000 to 2,000 m, 24 at 2,000 to 3,000 m and 11 beyond 3,000 m. 9 stand within 500 m of the extraction point. 16 patrol routes carry 31 riflemen. Nothing ties them to an area.
- **Strike and Disarm.** 53 spawners, all 2,300 to 2,900 m from the start and clustered at the laptop: 13 of the 27 start soldiers stand within 100 m of it and the 26 wave soldiers 232 to 541 m away. 48 are tied to one compound area and 6 use the 4 patrol routes.
- **Hunter Killer.** None; only labels. See the [Hunter Killer](hunter-killer.md) article.

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
- [Round 41 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-modes-ai-other.md)
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md)
- [AI detection model (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ai-detection.json)
- [AI EQS queries (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ai-eqs.json)
- [Round 71 PvE layouts (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round71-pve-layouts.md): placed objects, positions and distances. Static analysis; positions are straight-line metres in the map frame.
