---
title: "Recon"
parent: "Progression & Economy"
group: "Roles"
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

The skill curves give a value for each step. The unlock level and cost of each step are not in the sources, so they are not yet known (see [Skills](skills.md)).

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

Curve values are listed in key order, starting with the first key. Speed skills use three values and handling skills use four. The data does not confirm which key is which rank, so the rank reading is inferred.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Recon are:

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

- **Rewards per level.** Not yet known. The sources do not list a reward for each Recon mastery level, and the platform mastery reward data has no entries for roles.
- **Unlock tree.** Recon items and vehicles unlock through the role tree at a minimum mastery level, with a cash cost. The Season 2 section lists the changes.

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
- [Battle-pass track and Platform Mastery rewards](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
