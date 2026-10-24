---
title: "Pilot"
parent: "Progression & Economy"
group: "Roles"
description: "The Pilot role: 6 skills for air vehicles, covering mounted machine gun aiming and recoil, fuel use, impact damage and supply crate durability, plus its mastery curve and earnings."
---

# Pilot

| Pilot | |
|---|---|
| **General** | |
| Skills | 6 |
| Focus | Air vehicles and their mounted machine guns |
| **Mastery** | |
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Pilot, DT_PilotSkills |
{: .wiki-infobox }

Pilot is one of the six roles. Its six skills apply to air vehicles: the mounted machine gun on an air vehicle is faster to aim and kicks less, the vehicle uses less fuel and takes less damage from impacts. The role also makes a dropped supply crate tougher. The Pilot skills mirror the [Driver](driver.md) skills, with the air vehicle in place of the ground vehicle.

## Overview

The vehicle skills apply to the air vehicle the player is flying. The gun skills apply only to the mounted machine gun named in the data, not to every gun on an air vehicle. The supply crate skill applies to a crate the pilot drops.

The skill curves give a value for each step. The unlock level and cost of each step are not in the sources, so they are not yet known (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
|---|---|---|---|
| Aim down sights time (mounted machine gun) | Less time to raise the sights on the mounted machine gun. | 1, 0.8, 0.7, 0.6 | Mounted machine gun on air vehicles |
| Fuel use | Less fuel used in air vehicles, for a longer fuel time. | 1, 0.8, 0.7, 0.6 | Air vehicles. The data overrides the fuel usage multiplier with this value. |
| Horizontal recoil (mounted machine gun) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Mounted machine gun on air vehicles |
| Impact damage | Less damage when the air vehicle hits objects or the ground. | 1, 0.8, 0.7, 0.6 | Air vehicles. The data overrides the impact reduction multiplier with this value. |
| Supply crate durability | A supply crate the pilot drops takes more damage before it breaks. | 1, 1.2, 1.4 | Crates the pilot drops |
| Vertical recoil (mounted machine gun) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Mounted machine gun on air vehicles |

Curve values are listed in key order, starting with the first key. Speed and durability skills use three values and the others use four. The data does not confirm which key is which rank, so the rank reading is inferred.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Pilot are:

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
- **Unlock tree.** 11 items and vehicles, from level 2 to level 35, with 1,218,250 cash in total. Each one needs a role level and a cash price (see Unlocks below).

## Unlocks

Each row is one item, vehicle or attachment in the Pilot unlock tree, with the role level it needs and its cash cost. The data gives no other cost for any unlock. Rows at 0 cash are magazines, ammunition and explosives. Where the data has no display name for an item, the row describes it in plain words.

| Role level | Item | Cash |
|---|---:|---:|
| 2 | Armored small supply crate | 10,000 |
| 5 | Music tape 08 | 750 |
| 8 | AH-6M [Miniguns] | 125,000 |
| 10 | Z20 Lakota | 35,000 |
| 13 | Music tape 01 | 2,500 |
| 15 | Armored large supply crate | 25,000 |
| 20 | AH-6R [Rockets] | 250,000 |
| 23 | Music tape 09 | 10,000 |
| 25 | Z20 Lakota [Miniguns] | 85,000 |
| 30 | Music tape 04 | 25,000 |
| 35 | Havoc | 650,000 |

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Pilot's work in air vehicles. Role XP for most events equals the base value of the event.

- **Air vehicles destroyed.** The [MH-6](../vehicles/mh-6.md) pays 800 and the [Havoc](../vehicles/havoc.md) attack helicopter pays 6,000 when destroyed.
- **Vehicle kills and assists.** Kill and assist XP follows the same rules as cash. An assist credit is split by assist type, as described in [Cash and Rewards](cash-and-rewards.md#how-it-works).
- **Vehicle upkeep.** Repairs pay 20 cash with a wrench or light drill and 25 with a heavy drill. Refuelling pays 10. The sources do not say which roles these events credit.
- **Supply crates.** Deploying a supply crate pays 25 for the free container, 50 for a small crate and 150 for a large one.

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Havoc.** The Havoc default variant's cash cost in the Pilot unlock tree went from 500,000 to 650,000.
- **MH-6 guns.** The MH-6's mounted machine guns went from 50,000 to 125,000 in cash cost, and their level gate from 4 to 8.
- **Unlock tree.** The Pilot tree gained 2 nodes and lost 2. Several Pilot level gates changed.
- **Skills.** The sources list no Season 2 change to the six Pilot skill values. The supply crate change in Season 2 applies to crates in general and is listed in the [Support](support.md) article.

## See also

- [Skills](skills.md)
- [Driver](driver.md)
- [Cash and Rewards](cash-and-rewards.md)
- [MH-6](../vehicles/mh-6.md)
- [Havoc](../vehicles/havoc.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)
- [Vehicle weapons](../vehicles/vehicle-weapons.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Pilot skill table
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Economy data: role unlock tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
