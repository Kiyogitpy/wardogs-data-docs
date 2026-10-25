---
title: "Recon"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Recon role: 17 skills for sniper and marksman rifles, longer enemy spotting, lower visibility to infrared, lockpicking, its mastery curve and how it earns cash and XP."
---

# Recon

| Recon | |
|---|---|
| **General** | |
| Skills | 17 |
| Focus | Sniper rifles, marksman rifles and spotting |
| **Mastery** | |
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Recon, DT_ReconSkills |
{: .wiki-infobox }

Recon is one of the six roles. Its 17 skills mostly tune long-range play: how fast a player aims and recovers with sniper rifles and marksman rifles, how much these rifles kick, and how fast they switch. Recon also has spotting skills: enemies take longer to spot a Recon player, and enemies a Recon player spots stay marked for longer. Lockpicking is the role's other ability, granted by the data rather than tuned by a number.

## Overview

Most Recon skills apply to one weapon archetype. A skill for marksman rifles helps only marksman rifles, and a skill for sniper rifles helps only sniper rifles. The spotting skills apply to the player and to spotted targets, not to a weapon.

Each skill's value comes from its curve at the skill's level. The unlock cost of each skill level is not in the game data, so it is not yet known (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
|---|---|---|---|
| Aim down sights time (marksman rifles) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Marksman rifles only |
| Aim down sights time (sniper rifles) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Sniper rifles only |
| Aim move speed (marksman rifles) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Marksman rifles only |
| Aim move speed (sniper rifles) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Sniper rifles only |
| Infrared visibility | Reduces how visible the player is to enemies' infrared sights. | Set to 2.0, no curve (default 1) | One-time unlock. The data describes a heavy reduction, not invisibility. |
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

Curve values are listed in order for skill levels 0, 2, 3 and 4. Level 0 is always 1, which means no effect. Curves with three values store levels 0, 2 and 4 only, and levels in between are blended from the stored values.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Recon are the total XP needed to reach each level, not the step from the level before:

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
- **Unlock tree.** 58 items and vehicles, from level 2 to level 50, with 2,445,000 cash in total. Each one needs a role level and a cash price (see Unlocks below).

## Unlocks

Each row is one item, vehicle or attachment in the Recon unlock tree, with the role level it needs and its cash cost. The data gives no other cost for any unlock. Rows at 0 cash are magazines, ammunition and explosives. Where the data has no display name for an item, the row describes it in plain words.

| Role level | Item | Cash |
|---|---:|---:|
| 2 | Monocular | 7,500 |
| 3 | STRELIX Suppressor | 5,000 |
| 5 | SKS | 25,000 |
| 6 | Deadeye Flash Hider | 12,500 |
| 7 | SKS Bipod | 10,000 |
| 8 | Range finder | 25,000 |
| 9 | DTK-1 Brake | 7,500 |
| 10 | PU 91/30 Scope | 12,500 |
| 10 | Mosin Nagant | 50,000 |
| 11 | 1x-6x LPVO Short Dot | 15,000 |
| 12 | SVD 5 RND Magazine | 0 |
| 12 | SVD | 50,000 |
| 13 | SVD 7.62x54R Brake | 10,000 |
| 14 | SVD Bipod | 10,000 |
| 15 | Hexagon 762 Suppressor | 15,000 |
| 16 | Arrow | 0 |
| 16 | Compound Bow | 150,000 |
| 17 | SVD magazine | 25,000 |
| 18 | SV98 magazine | 0 |
| 18 | SV98 | 100,000 |
| 19 | 6-10x Scope MOA | 45,000 |
| 20 | FAL 10 RND Magazine | 0 |
| 20 | BMR-308 | 125,000 |
| 21 | SV98 Bipod | 17,500 |
| 22 | SRVV Brake | 17,500 |
| 23 | Claymore | 90,000 |
| 24 | BMR-308 Flash Hider | 50,000 |
| 25 | M14 10 RND Magazine | 0 |
| 25 | M14 | 100,000 |
| 26 | Ghillie Headwear | 60,000 |
| 26 | Ghillie Suit | 80,000 |
| 27 | Leatherwood ART II | 35,000 |
| 28 | 6-10x Scope MRAD | 40,000 |
| 29 | M14 Bipod | 25,000 |
| 30 | MK22 5 RND Magazine | 0 |
| 30 | MK22 | 150,000 |
| 31 | M14 20 RND Magazine | 27,500 |
| 32 | Infrared range finder | 50,000 |
| 33 | BMR-308 Suppressor | 25,000 |
| 34 | Constrictor Brake | 20,000 |
| 35 | AMR 50 magazine | 0 |
| 35 | AMR 50 | 200,000 |
| 36 | M14 30 RND Magazine | 50,000 |
| 37 | .30 Cal SS Phosphate Muzzle Brake | 22,500 |
| 38 | AMR 50 Cal Muzzle Brake | 35,000 |
| 39 | MK22 magazine | 35,000 |
| 40 | Flow-Through .308 Suppressor | 30,000 |
| 41 | Ghillie headwear (dead variant) | 80,000 |
| 41 | Ghillie suit (dead variant) | 100,000 |
| 42 | .30 Cal Steel Black Flash Hider | 27,500 |
| 43 | 6x Marksman Scope + Reflex | 75,000 |
| 44 | Slicktap Brake | 22,500 |
| 45 | GOL Multi-Caliber Suppressor | 32,500 |
| 46 | Pro Tilt Bipod | 50,000 |
| 47 | Frontier 2.5x-10x Precision Scope | 95,000 |
| 48 | .50 Cal Heavy Suppressor | 27,500 |
| 49 | Three Port Brake | 25,000 |
| 50 | AMR 50 10 RND Magazine | 50,000 |

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
