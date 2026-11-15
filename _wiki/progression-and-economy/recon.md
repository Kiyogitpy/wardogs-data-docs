---
title: "Recon"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Recon role: 17 skills for sniper and marksman rifles, longer enemy spotting, lower visibility to infrared, lockpicking, its mastery curve and how it earns cash and XP."
---

# Recon

S3 announcement: AMR 50 moves from level 35 to 41. The Infrared Range Finder was removed from vendors pending redesign; the saved Range Finder node below does not establish an available offering. See the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221); the current saved table below gives individual costs and prerequisites.

| Recon | |
|---|---|
| **General** | |
| Skills | 17 |
| Focus | Sniper rifles, marksman rifles and spotting |
| **Mastery** | |
| Stored XP at level 10 | 36,750 |
| Stored XP at level 50 | 1,950,000 |
| Stored XP at level 100 | 6,600,000 |
| Internal name | Meta.Role.Recon, DT_ReconSkills |
{: .wiki-infobox }

Recon has 17 saved skill-effect rows across the role and plugin tables: rifle handling, spotting, infrared visibility and ability-grant effects. These are configured effects and target tags; current activation and effective arithmetic remain unverified.

## Overview

The skill table below summarizes the configured effect targets and intended changes. Application requirements are saved filters, not evidence that the S3 consumer applies an effect. Historical application details are identified separately.

The reviewed skill-effect and curve exports do not supply per-level unlock costs. Earning, spending and upgrade consumers remain unresolved; this is not proof that costs or skill points are absent from the game (see [Skills](skills.md)).

## Skills

| Skill | Configured effect / historical interpretation | Stored curve values | Notes |
|---|---|---|---|
| Aim down sights time (marksman rifles) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Marksman rifles only |
| Aim down sights time (sniper rifles) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Sniper rifles only |
| Aim move speed (marksman rifles) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Marksman rifles only |
| Aim move speed (sniper rifles) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Sniper rifles only |
| Infrared visibility | Reduces how visible the player is to enemies' infrared sights. | Set to 2.0, no curve (default 1) | One-time unlock. The game describes a heavy reduction, not invisibility. |
| Horizontal recoil (marksman rifles) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Marksman rifles only |
| Horizontal recoil (sniper rifles) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Sniper rifles only |
| Time to be spotted | Enemies take longer to spot the player. | 1, 1.2, 1.4 | Any weapon |
| Enemy spotted duration | Enemies the player spots stay spotted longer. | 1, 1.2, 1.4 | Any weapon |
| Lockpicking | Lets the player lockpick enemy locked vehicles, buildables and fortifications. | Grants an ability | Not a number |
| Ready to fire (marksman rifles) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | Marksman rifles only |
| Ready to fire (sniper rifles) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | Sniper rifles only |
| Focus refill on sniper kill | A kill with a sniper rifle refills focus. | Grants an ability | One-time unlock |
| Vertical recoil (marksman rifles) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Marksman rifles only |
| Vertical recoil (sniper rifles) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Sniper rifles only |
| Pistol switch speed | Faster switching to sidearms. | 1, 1.2, 1.4 | Sidearms only |
| Sniper and marksman switch speed | Faster switching to sniper and marksman rifles. | 1, 1.2, 1.4 | Sniper and marksman rifles |

The stored curve keys are at Time 0, 2, 3 and 4, or 0, 2 and 4 for three-value curves; their interpolation mode is Linear and the Time-0 value is 1. The CL516586 round 45 trace used the node upgrade level as Time. Applying that interpretation and interpolation to S3 remains conditional: the current activation, input level and native arithmetic have not been established.

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
- **Current unlock tree.** 81 saved nodes, with level requirements from 2 to 50 and 3,940,000 cash in listed costs. These are stored requirements, not a test of server unlock behavior. The full current list is in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Current S3 unlock list

These 81 rows reproduce the CL533731 saved role tree: level prerequisites and cash **unlock costs**, not vendor purchase prices. Shared items can be unlocked through multiple roles in S3, as announced in the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). Mode restrictions and removed vendors still govern availability; a retained node alone is not an active shop offer.

| Role level | Item | Unlock cash |
|---:|---|---:|
| 2 | Monocular | 7,500 |
| 3 | STRELIX Suppressor | 5,000 |
| 4 | Field Backpack | 20,000 |
| 5 | SKS | 25,000 |
| 6 | Level 1 Helmet | 7,500 |
| 6 | Level 1 Armor | 10,000 |
| 7 | SKS Bipod | 10,000 |
| 7 | 5.56mm Flesh Damage (HP) | 15,000 |
| 8 | Deadeye Flash Hider | 12,500 |
| 8 | Range Finder | 25,000 |
| 9 | DTK-1 Brake | 7,500 |
| 9 | Medium Tac Vest | 10,000 |
| 10 | Mosin Nagant | 50,000 |
| 10 | PU 91/30 Scope | 12,500 |
| 11 | 3x-6x LPVO Short Dot | 15,000 |
| 11 | Operator Backpack | 25,000 |
| 12 | SVD | 50,000 |
| 12 | SVD 5 RND Magazine | 0 |
| 13 | SVD 7.62x54R Brake | 10,000 |
| 13 | 7.62mm Flesh Damage (HP) | 15,000 |
| 14 | Hexagon 762 Suppressor | 15,000 |
| 14 | SVD Bipod | 10,000 |
| 15 | Compound Bow | 150,000 |
| 15 | Assault Backpack | 50,000 |
| 16 | Level 2 Helmet | 37,500 |
| 16 | Level 2 Armor | 50,000 |
| 17 | SVD 10 RND Magazine | 25,000 |
| 17 | 7.62x54mm Flesh Damage (HP) | 15,000 |
| 18 | SV98 | 100,000 |
| 18 | SV98 10 RND Magazine | 0 |
| 19 | 6-10x Scope MOA | 45,000 |
| 19 | Large Tac Vest | 25,000 |
| 20 | BMR-308 | 125,000 |
| 20 | FAL 10 RND Magazine | 0 |
| 21 | SV98 Bipod | 17,500 |
| 22 | SRVV Brake | 17,500 |
| 22 | Sport Parachute | 25,000 |
| 23 | Claymore | 90,000 |
| 23 | Ruck Backpack | 100,000 |
| 24 | BMR-308 Flash Hider | 50,000 |
| 25 | M14 | 100,000 |
| 25 | M14 10 RND Magazine | 0 |
| 26 | Ghillie Headwear | 60,000 |
| 26 | Ghillie Body Suit | 80,000 |
| 27 | Leatherwood ART II | 35,000 |
| 27 | 5.56mm Armor Piercing (AP) | 75,000 |
| 28 | 6-10x Scope MRAD | 40,000 |
| 28 | 7.62mm Armor Piercing (AP) | 75,000 |
| 29 | M14 Bipod | 25,000 |
| 30 | MK22 | 150,000 |
| 30 | MK22 5 RND Magazine | 0 |
| 31 | M14 20 RND Magazine | 27,500 |
| 31 | .308 Win Flesh Damage (HP) | 15,000 |
| 32 | M14 30 RND Magazine | 50,000 |
| 33 | BMR-308 Suppressor | 25,000 |
| 33 | Constrictor Brake | 20,000 |
| 34 | Gunner Backpack + Sling | 125,000 |
| 34 | 7.62x54mm Armor Piercing (AP) | 75,000 |
| 35 | .308 Win Armor Piercing (AP) | 75,000 |
| 36 | Level 3 Helmet | 75,000 |
| 36 | Level 3 Armor | 100,000 |
| 37 | .30 Cal SS Phosphate Muzzle Brake | 22,500 |
| 39 | MK22 10 RND Magazine | 35,000 |
| 40 | Flow-Through .308 Suppressor | 30,000 |
| 41 | AMR 50 | 200,000 |
| 41 | AMR 50 5 RND Magazine | 0 |
| 42 | .30 Cal Steel Black Flash Hider | 27,500 |
| 42 | AMR 50 Cal Muzzle Brake | 35,000 |
| 43 | 6x Marksman Scope + Reflex | 75,000 |
| 43 | Slicktap Brake | 22,500 |
| 44 | GOL Multi-Caliber Suppressor | 32,500 |
| 45 | Level 4 Helmet | 150,000 |
| 45 | Level 4 Armor | 200,000 |
| 46 | Pro Tilt Bipod | 50,000 |
| 47 | Frontier 2.5x-10x Precision Scope | 95,000 |
| 48 | .50 Cal Heavy Suppressor | 27,500 |
| 48 | Arsenal Backpack + 2 Slings | 175,000 |
| 49 | Three Port Brake | 25,000 |
| 49 | AMR 50 10 RND Magazine | 50,000 |
| 50 | Ghillie Headwear (Dead) | 80,000 |
| 50 | Ghillie Body Suit (Dead) | 100,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Recon`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json). The [pinned earlier role article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/d3cf6f2bf54541b8389b9327aab933e1e8488b9b/_wiki/progression-and-economy/recon.md) retains the earlier table for historical comparison.

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Recon's job of spotting and long-range kills. Role XP for most events equals the base value of the event.

- **Spotting.** Spotting a target pays 15 to 275, scaled by the spot's contribution. Destroying a target the player spotted pays 50 to 500 on the same scale.
- **Long-range kills.** Recon kills follow the same kill rules as any role. A default kill pays 250, each repeat kill on the same player pays 24% less (up to four repeats), and each streak kill adds 50 to the base (up to five).
- **Streak and revenge bonuses.** Ending an enemy's streak pays 1.5 times. A revenge kill pays 2.0 times.
- **Artillery and zones.** A kill from artillery in the open pays 5,000. A Hot Zone kill counts with a weight of 10 and a Control Zone kill with a weight of 5.
- **Penalties.** A kill on a player an enemy medic has just revived pays 0.01 times. A teamkill pays a negative amount.

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Unlock tree.** The Recon tree gained 9 nodes and lost none. The Claymore's cash cost went from 50,000 to 90,000. Several Recon level gates changed. The Season 2 page lists them.
- **Skills.** The sources list no Season 2 change to the 17 Recon skill values.

## See also

- [Choosing a Role](../guides/choosing-a-role.md)
- [Skills](skills.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Spotting](../game-mechanics/spotting.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)
- [Claymore](../equipment/claymore.md)
- [Weapons](../weapons.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Recon skill table
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Economy data: role unlock tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
