---
title: "Assault"
redirect_from: ["/wiki/progression-and-economy/infantry/"]
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Assault role: 17 skills for assault rifles and SMGs, faster aiming and recoil control, longer tac-sprints, its mastery curve and how it earns cash and XP."
---

# Assault

S3 announcement: C4 moves from level 4 to 5; Molotov from 13 to 8. Molotov unlock cash falls from 25,000 to 12,500. See the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221); the current saved table below gives individual costs and prerequisites.

| Assault | |
|---|---|
| **General** | |
| Skills | 17 |
| Focus | Assault rifles, SMGs and movement |
| **Mastery** | |
| Stored XP at level 10 | 36,750 |
| Stored XP at level 50 | 1,950,000 |
| Stored XP at level 100 | 6,600,000 |
| Internal name | Meta.Role.Infantry, DT_InfantrySkills |
{: .wiki-infobox }

Assault has 17 saved skill-effect rows for assault rifles, SMGs, movement and sprint breaching. The rows identify effects, application tags and curves; they do not establish that the current game activates those effects. The internal role tag is Meta.Role.Infantry.

## Overview

The skill table below summarizes the configured effect targets and intended changes. Application requirements are saved filters, not evidence that the S3 consumer applies an effect. Historical application details are identified separately.

The reviewed skill-effect and curve exports do not supply per-level unlock costs. Earning, spending and upgrade consumers remain unresolved; this is not proof that costs or skill points are absent from the game (see [Skills](skills.md)).

## Skills

| Skill | Configured effect / historical interpretation | Stored curve values | Notes |
|---|---|---|---|
| Aim down sights time (assault rifles) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Assault rifles only |
| Aim down sights time (SMGs) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | SMGs only |
| Aim move speed (assault rifles) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Assault rifles only |
| Aim move speed (SMGs) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | SMGs only |
| Crouch and prone speed | Faster movement while crouched or prone. | 1, 1.2, 1.4 | Any weapon |
| Crouch and prone tac-sprint recovery | Tac-sprint stamina refills faster while crouched or prone. | 1, 1.2, 1.4 | Any weapon |
| Horizontal recoil (assault rifles) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Assault rifles only |
| Horizontal recoil (SMGs) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | SMGs only |
| Return to fire (assault rifles) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | Assault rifles only. The game calls this a ready-to-fire speed. |
| Return to fire (SMGs) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | SMGs only. Same name as above. |
| Sprint breach | Lets the player bash through doors by sprinting into them. | Not a number | Grants an ability |
| Tac-sprint length | Lower tac-sprint stamina use, so the sprint lasts longer. | 1, 0.8, 0.7, 0.6 | Stamina use multiplier |
| Tac-sprint recovery | Tac-sprint stamina refills faster. | 1, 1.2, 1.4 | Any weapon |
| Unarmed sprint speed | Faster sprint with the fists out, for both sprint and tac-sprint. | 1, 1.2, 1.4 | Fists only |
| Vertical recoil (assault rifles) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Assault rifles only |
| Vertical recoil (SMGs) | Less upward kick. | 1, 0.8, 0.7, 0.6 | SMGs only |
| Weapon switch speed | Faster switching to assault rifles and SMGs. | 1, 1.2, 1.4 | Assault rifles and SMGs |

The stored curve keys are at Time 0, 2, 3 and 4, or 0, 2 and 4 for three-value curves; their interpolation mode is Linear and the Time-0 value is 1. The CL516586 round 45 trace used the node upgrade level as Time. Applying that interpretation and interpolation to S3 remains conditional: the current activation, input level and native arithmetic have not been established. For the multiplier skills, a lower value gives a faster or less disruptive result, and the game's skill descriptions say so for aiming and recoil.

## Mastery and rewards

The six current role definitions store the same XP values. These are the S3 values at selected levels; interpreting them as cumulative thresholds requires the level consumer:

| Level | XP needed |
|---|---|
| 1 | 200 |
| 5 | 6,250 |
| 10 | 36,750 |
| 20 | 275,000 |
| 50 | 1,950,000 |
| 75 | 3,320,500 |
| 100 | 6,600,000 |

The full curve is in [Cash and Rewards](cash-and-rewards.md#role-mastery-xp). Whether each value is a running total or a step from the level before is not stated.

- **Rewards per level.** The current level definitions have empty reward lists. This does not rule out server grants; the separate unlock tree stores level prerequisites and cash costs.
- **Current unlock tree.** 65 saved nodes, with level requirements from 2 to 50 and 2,802,500 cash in listed costs. These are stored requirements, not a test of server unlock behavior. The full current list is in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Current S3 unlock list

These 65 rows reproduce the CL533731 saved role tree: level prerequisites and cash **unlock costs**, not vendor purchase prices. Shared items can be unlocked through multiple roles in S3, as announced in the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). Mode restrictions and removed vendors still govern availability; a retained node alone is not an active shop offer.

| Role level | Item | Unlock cash |
|---:|---|---:|
| 2 | Birdcage Flash Hider | 5,000 |
| 3 | T-21 | 10,000 |
| 3 | STANAG 30 RND Magazine | 0 |
| 4 | Level 1 Helmet | 7,500 |
| 4 | Level 1 Armor | 10,000 |
| 5 | Remote Detonator | 15,000 |
| 5 | C4 Charge | 0 |
| 6 | Field Backpack | 20,000 |
| 6 | 5.45mm Flesh Damage (HP) | 15,000 |
| 7 | Hexagon Brake | 12,500 |
| 7 | 3 Prong Flash Hider | 7,500 |
| 8 | Molotov | 12,500 |
| 8 | Medium Tac Vest | 10,000 |
| 9 | 5.56mm Flesh Damage (HP) | 15,000 |
| 10 | Galil | 35,000 |
| 10 | Galil 35 RND Magazine | 0 |
| 11 | Operator Backpack | 25,000 |
| 12 | CQ-2x Prism Combat Scope | 15,000 |
| 12 | Rubberized Ergonomic Foregrip | 7,500 |
| 13 | CQR Tactical Front Rail Grip | 10,000 |
| 14 | Level 2 Helmet | 37,500 |
| 14 | Level 2 Armor | 50,000 |
| 15 | Sport Parachute | 25,000 |
| 16 | Galil 50 RND Magazine | 25,000 |
| 17 | 2.5x Combat Optic | 10,000 |
| 17 | CQB 74 Brake | 15,000 |
| 18 | Large Tac Vest | 25,000 |
| 18 | Assault Backpack | 50,000 |
| 19 | PBS-4 Suppressor | 25,000 |
| 20 | TCX-SPR | 100,000 |
| 20 | TCX-SPR 28 RND Magazine | 0 |
| 21 | TopComp Brake | 20,000 |
| 21 | 7.62mm Flesh Damage (HP) | 15,000 |
| 22 | Four Reticle Reflex | 10,000 |
| 22 | Clutch Lok Muzzle Brake | 37,500 |
| 23 | Ruck Backpack | 100,000 |
| 24 | RC-556 Suppressor | 30,000 |
| 25 | AK74 60 RND Magazine | 30,000 |
| 26 | OKP 7 Reflex | 30,000 |
| 27 | TGP-A Suppressor 5.45 | 17,500 |
| 27 | 5.45mm Armor Piercing (AP) | 75,000 |
| 28 | M4 | 150,000 |
| 29 | AR Multi-Caliber Suppressor | 22,500 |
| 29 | Gunner Backpack + Sling | 125,000 |
| 30 | STANAG 60 RND Magazine | 25,000 |
| 31 | Cross Rifle Muzzle Brake | 35,000 |
| 31 | 5.56mm Armor Piercing (AP) | 75,000 |
| 32 | Level 3 Helmet | 75,000 |
| 32 | Level 3 Armor | 100,000 |
| 33 | 3x Tactical Prism Scope | 15,000 |
| 35 | FAL | 250,000 |
| 35 | FAL 20 RND Magazine | 0 |
| 36 | AK74 75 RND Drum Magazine | 75,000 |
| 37 | .308 Win Flesh Damage (HP) | 15,000 |
| 38 | RVG Vertical Foregrip | 25,000 |
| 39 | 7.62mm Armor Piercing (AP) | 75,000 |
| 40 | Level 4 Helmet | 150,000 |
| 40 | Level 4 Armor | 200,000 |
| 41 | .308 Win Armor Piercing (AP) | 75,000 |
| 42 | SRD762TI-QD | 40,000 |
| 43 | Spectr 4x | 15,000 |
| 45 | 3-Chamber Brake | 45,000 |
| 46 | Shift Foregrip | 30,000 |
| 48 | Arsenal Backpack + 2 Slings | 175,000 |
| 50 | FAL 30 RND Magazine | 50,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Infantry`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json). The [pinned earlier role article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/d3cf6f2bf54541b8389b9327aab933e1e8488b9b/_wiki/progression-and-economy/assault.md) retains the earlier table for historical comparison.

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

- [Choosing a Role](../guides/choosing-a-role.md)
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
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
