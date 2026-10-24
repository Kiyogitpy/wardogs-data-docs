---
title: "Infantry"
parent: "Progression & Economy"
group: "Roles"
description: "The Infantry role: 17 skills for assault rifles and SMGs, faster aiming and recoil control, longer tac-sprints, its mastery curve and how it earns cash and XP."
---

# Infantry

| Infantry | |
|---|---|
| **General** | |
| Skills | 17 |
| Game label | ASSAULT |
| Focus | Assault rifles, SMGs and movement |
| **Mastery** | |
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Infantry, DT_InfantrySkills |
{: .wiki-infobox }

Infantry is one of the six roles. Each role has its own skill set and its own mastery level. The 17 Infantry skills mostly tune assault rifles and submachine guns: how fast they come up to the sights, how much they kick, and how fast they switch. The role also has movement skills for crouching, proning and tac-sprinting, and one ability, breaching doors by sprinting into them. The game's XP and role labels show this role as ASSAULT.

## Overview

Most Infantry skills apply to one weapon archetype. A skill for assault rifles helps only assault rifles, and a skill for SMGs helps only SMGs. The movement and handling skills apply to the player or to the held weapon in general.

The skill curves give a value for each step of the skill. The data does not state the unlock level or cost of each step, so those are not yet known (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
|---|---|---|---|
| Aim down sights time (assault rifles) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Assault rifles only |
| Aim down sights time (SMGs) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | SMGs only |
| Aim move speed (assault rifles) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Assault rifles only |
| Aim move speed (SMGs) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | SMGs only |
| Crouch and prone speed | Faster movement while crouched or prone. | 1, 1.2, 1.4 | Any weapon |
| Crouch and prone tac-sprint recovery | Tac-sprint stamina refills faster while crouched or prone. | 1, 1.2, 1.4 | Any weapon |
| Horizontal recoil (assault rifles) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Assault rifles only |
| Horizontal recoil (SMGs) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | SMGs only |
| Return to fire (assault rifles) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | Assault rifles only. The data calls this a ready-to-fire speed. |
| Return to fire (SMGs) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | SMGs only. Same data name as above. |
| Sprint breach | Lets the player bash through doors by sprinting into them. | Not a number | Grants an ability |
| Tac-sprint length | Lower tac-sprint stamina use, so the sprint lasts longer. | 1, 0.8, 0.7, 0.6 | Stamina use multiplier |
| Tac-sprint recovery | Tac-sprint stamina refills faster. | 1, 1.2, 1.4 | Any weapon |
| Unarmed sprint speed | Faster sprint with the fists out, for both sprint and tac-sprint. | 1, 1.2, 1.4 | Fists only |
| Vertical recoil (assault rifles) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Assault rifles only |
| Vertical recoil (SMGs) | Less upward kick. | 1, 0.8, 0.7, 0.6 | SMGs only |
| Weapon switch speed | Faster switching to assault rifles and SMGs. | 1, 1.2, 1.4 | Assault rifles and SMGs |

Curve values are listed in key order, starting with the first key. Speed skills use three values and handling skills use four. The data does not confirm which key is which rank, so the rank reading is inferred. For the multiplier skills, a lower value gives a faster or less disruptive result, and the data's skill descriptions say so for aiming and recoil.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Infantry are:

| Level | XP needed |
|---|---|
| 1 | 200 |
| 5 | 6,250 |
| 10 | 25,000 |
| 20 | 111,500 |
| 50 | 1,150,000 |
| 75 | 2,218,000 |
| 100 | 5,132,500 |

The full curve is in [Cash and Rewards](cash-and-rewards.md#role-mastery-xp). Whether each value is a running total or a step from the level before is not stated.

- **Rewards per level.** Not yet known. The sources do not list a reward for each Infantry mastery level, and the platform mastery reward data has no entries for roles.
- **Unlock tree.** Items and vehicles that unlock through the role's tree have a minimum mastery level (a level gate) and a cash cost. The tree entries are not listed here, so see the Season 2 section for the changes.

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Infantry's work of fighting on foot. Role XP for most events equals the base value of the event, so a kill that pays 250 cash also adds 250 XP to the role.

- **Player kills.** A kill with a default weapon pays 250. Each repeat kill on the same player pays 24% less, up to four repeats. Each kill in a streak adds 50 to the base, up to five.
- **Streak and revenge bonuses.** Ending an enemy's streak pays 1.5 times. A revenge kill pays 2.0 times.
- **Zone kills.** A kill in a Hot Zone counts with a weight of 10 and a kill in a Control Zone with a weight of 5. In the enemy's own zones the weights are 4 (Hot Zone) and 2 (Control Zone).
- **Artillery kills.** A kill from artillery while the attacker is in the open pays 5,000. The same kill from inside a zone pays 100.
- **Mines and explosives.** Destroying an enemy claymore, C4 or anti-tank mine pays 100 each.
- **Zones and towers.** Capturing a hostile tower pays 1,000 and a neutral tower 250. A Control Zone event pays 150 and the first entry into a Control Zone pays 100 in a life.
- **Penalties.** A kill on a player an enemy medic has just revived pays 0.01 times. A teamkill pays a negative amount.

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Unlock tree.** The Infantry tree gained 14 nodes and lost 7. The STANAG magazine's cash cost went from 10,000 to 0. Level gates changed for several Infantry nodes.
- **Skills.** The sources list no Season 2 change to the 17 Infantry skill values.

## See also

- [Skills](skills.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Shops](shops.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)
- [Movement](../game-mechanics/movement.md)
- [Weapons](../weapons.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Infantry skill table
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Battle-pass track and Platform Mastery rewards](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md), for the ASSAULT label
