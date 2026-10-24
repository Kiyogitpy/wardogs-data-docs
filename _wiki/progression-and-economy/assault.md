---
title: "Assault"
redirect_from: ["/wiki/progression-and-economy/infantry/"]
parent: "Progression & Economy"
group: "Roles"
description: "The Assault role: 17 skills for assault rifles and SMGs, faster aiming and recoil control, longer tac-sprints, its mastery curve and how it earns cash and XP."
---

# Assault

| Assault | |
|---|---|
| **General** | |
| Skills | 17 |
| Focus | Assault rifles, SMGs and movement |
| **Mastery** | |
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Infantry, DT_InfantrySkills |
{: .wiki-infobox }

Assault is one of the six roles. Each role has its own skill set and its own mastery level. The 17 Assault skills mostly tune assault rifles and submachine guns: how fast they come up to the sights, how much they kick, and how fast they switch. The role also has movement skills for crouching, proning and tac-sprinting, and one ability, breaching doors by sprinting into them. The game files call it the Assault role internally.

## Overview

Most Assault skills apply to one weapon archetype. A skill for assault rifles helps only assault rifles, and a skill for SMGs helps only SMGs. The movement and handling skills apply to the player or to the held weapon in general.

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

All six roles share one mastery XP curve. The milestones for Assault are:

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

- **Rewards per level.** None in the data. The level table has an empty reward list for every level, so a level gives no reward of its own. What a level gives is access to the unlock tree (see Unlocks below).
- **Unlock tree.** 40 items and vehicles, from level 2 to level 50, with 1,270,000 cash in total. Each one needs a role level and a cash price (see Unlocks below).

## Unlocks

Each row is one item, vehicle or attachment in the Assault unlock tree, with the role level it needs and its cash cost. The data gives no other cost for any unlock. Rows at 0 cash are magazines, ammunition and explosives. Where the data has no display name for an item, the row describes it in plain words.

| Role level | Item | Cash |
|---|---:|---:|
| 2 | Birdcage Flash Hider | 5,000 |
| 3 | STANAG 30 RND Magazine | 0 |
| 3 | T-21 | 10,000 |
| 4 | C4 explosive | 0 |
| 4 | C4 detonator | 15,000 |
| 5 | Hexagon Brake | 12,500 |
| 8 | 3 Prong Flash Hider | 7,500 |
| 10 | Galil 35 RND Magazine | 0 |
| 10 | Galil | 35,000 |
| 11 | Rubberized Ergonomic Foregrip | 7,500 |
| 12 | CQ-2x Prism Combat Scope | 15,000 |
| 13 | Molotov | 25,000 |
| 14 | CQR Tactical Front Rail Grip | 10,000 |
| 15 | Galil 50 RND Magazine | 25,000 |
| 16 | CQB 74 Brake | 15,000 |
| 17 | 2.5x Combat Optic | 10,000 |
| 19 | PBS-4 Suppressor | 25,000 |
| 20 | SIG Spear Standard Mag | 0 |
| 20 | TCX-SPR | 100,000 |
| 21 | TopComp Brake | 20,000 |
| 22 | Four Reticle Reflex | 10,000 |
| 24 | RC-556 Suppressor | 30,000 |
| 25 | AK74 60 RND Magazine | 30,000 |
| 26 | OKP 7 Reflex | 30,000 |
| 27 | TGP-A Suppressor 5.45 | 17,500 |
| 28 | M4 | 150,000 |
| 29 | AR Multi-Caliber Suppressor | 22,500 |
| 30 | STANAG extended magazine | 25,000 |
| 32 | Cross Rifle Muzzle Brake | 35,000 |
| 33 | 3x Tactical Prism Scope | 15,000 |
| 35 | FAL 20 RND Magazine | 0 |
| 35 | FAL | 250,000 |
| 36 | AK74 75 RND Drum Magazine | 75,000 |
| 37 | Clutch Lok Muzzle Brake | 37,500 |
| 38 | RVG Vertical Foregrip | 25,000 |
| 40 | SRD762TI-QD | 40,000 |
| 43 | Spectr 4x | 15,000 |
| 45 | 3-Chamber Brake | 45,000 |
| 48 | Shift Foregrip | 30,000 |
| 50 | FAL 30 RND Magazine | 50,000 |

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Assault's work of fighting on foot. Role XP for most events equals the base value of the event, so a kill that pays 250 cash also adds 250 XP to the role.

- **Player kills.** A kill with a default weapon pays 250. Each repeat kill on the same player pays 24% less, up to four repeats. Each kill in a streak adds 50 to the base, up to five.
- **Streak and revenge bonuses.** Ending an enemy's streak pays 1.5 times. A revenge kill pays 2.0 times.
- **Zone kills.** A kill in a Hot Zone counts with a weight of 10 and a kill in a Control Zone with a weight of 5. In the enemy's own zones the weights are 4 (Hot Zone) and 2 (Control Zone).
- **Artillery kills.** A kill from artillery while the attacker is in the open pays 5,000. The same kill from inside a zone pays 100.
- **Mines and explosives.** Destroying an enemy claymore, C4 or anti-tank mine pays 100 each.
- **Zones and towers.** Capturing a hostile tower pays 1,000 and a neutral tower 250. A Control Zone event pays 150 and the first entry into a Control Zone pays 100 in a life.
- **Penalties.** A kill on a player an enemy medic has just revived pays 0.01 times. A teamkill pays a negative amount.

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Unlock tree.** The Assault tree gained 14 nodes and lost 7. The STANAG magazine's cash cost went from 10,000 to 0. Level gates changed for several Assault nodes.
- **Skills.** The sources list no Season 2 change to the 17 Assault skill values.

## See also

- [Skills](skills.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Shops](shops.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)
- [Movement](../game-mechanics/movement.md)
- [Weapons](../weapons.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the role's skill table (listed there as Assault)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md), for the ASSAULT label
- [Economy data: role unlock tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
