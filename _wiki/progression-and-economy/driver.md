---
title: "Driver"
parent: "Progression & Economy"
group: "Roles"
description: "The Driver role: 6 skills for ground vehicles, covering mounted machine gun aiming and recoil, fuel use, impact damage and supply crate durability, plus its mastery curve and earnings."
---

# Driver

| Driver | |
|---|---|
| **General** | |
| Skills | 6 |
| Focus | Ground vehicles and their mounted machine guns |
| **Mastery** | |
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Driver, DT_DriverSkills |
{: .wiki-infobox }

Driver is one of the six roles. Its six skills apply to ground vehicles: the mounted machine gun on a ground vehicle is faster to aim and kicks less, the vehicle uses less fuel and takes less damage from impacts. The role also makes a dropped supply crate tougher. The Driver skills mirror the [Pilot](pilot.md) skills, with the ground vehicle in place of the air vehicle.

## Overview

The vehicle skills apply to the ground vehicle the player is driving. The gun skills apply only to the mounted machine gun named in the data, which is the heavy tank's mounted machine gun, not every gun on a ground vehicle. The supply crate skill applies to a crate the driver drops. It sets the crate's own health, not the vehicle's.

The skill curves give a value for each step. The unlock level and cost of each step are not in the sources, so they are not yet known (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
|---|---|---|---|
| Aim down sights time (mounted machine gun) | Less time to raise the sights on the mounted machine gun. | 1, 0.8, 0.7, 0.6 | Heavy tank's mounted machine gun |
| Fuel use | Less fuel used in ground vehicles, for a longer fuel time. | 1, 0.8, 0.7, 0.6 | Ground vehicles. The data overrides the fuel usage multiplier with this value. |
| Horizontal recoil (mounted machine gun) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Heavy tank's mounted machine gun |
| Impact damage | Less damage when the ground vehicle hits objects or the landscape. | 1, 0.8, 0.7, 0.6 | Ground vehicles. The data overrides the impact reduction multiplier with this value. |
| Supply crate durability | A supply crate the driver drops has 1.0, 1.2 or 1.4 times its normal health at skill levels 0, 2 and 4. It is set when the crate is created, and it is not a vehicle-health bonus. | 1, 1.2, 1.4 | Crates the driver drops |
| Vertical recoil (mounted machine gun) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Heavy tank's mounted machine gun |

Curve values are listed in key order, starting with the first key. The durability skill uses three values and the others use four. The data does not confirm which key is which rank, so the rank reading is inferred, except for supply crate durability, whose levels (0, 2 and 4) the data gives.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Driver are the total XP needed to reach each level, not the step from the level before:

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
- **Unlock tree.** 21 items and vehicles, from level 3 to level 35, with 2,308,250 cash in total. Each one needs a role level and a cash price (see Unlocks below).

## Unlocks

Each row is one item, vehicle or attachment in the Driver unlock tree, with the role level it needs and its cash cost. The data gives no other cost for any unlock. Rows at 0 cash are magazines, ammunition and explosives. Where the data has no display name for an item, the row describes it in plain words.

| Role level | Item | Cash |
|---|---:|---:|
| 3 | Ural | 35,000 |
| 5 | Music tape 06 | 750 |
| 6 | Kodiak [M249] | 50,000 |
| 8 | Wolf-110 | 50,000 |
| 9 | Dune Buggy | 25,000 |
| 10 | Kodiak [Pickup] | 35,000 |
| 13 | Music tape 07 | 2,500 |
| 14 | Humvee | 75,000 |
| 15 | Ural Defender | 75,000 |
| 16 | Wolf-110 [M2 Browning] | 125,000 |
| 17 | Large supply crate | 20,000 |
| 20 | T-72B3 | 250,000 |
| 22 | Ural Defender [M249] | 100,000 |
| 23 | Music tape 02 | 5,000 |
| 24 | Humvee [M249] | 125,000 |
| 25 | Flakpanzer Gepard | 300,000 |
| 28 | Music tape 03 | 10,000 |
| 30 | Humvee [Minigun] | 150,000 |
| 31 | SPH-2 | 350,000 |
| 33 | Music tape 05 | 25,000 |
| 35 | L2A6 | 500,000 |

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Driver's work in ground vehicles. Role XP for most events equals the base value of the event.

- **Ground vehicles destroyed.** The base cash is 100 for a Bobcat, 300 for a Dune Buggy, and 500 each for a Humvee and a Kodiak. A heavy tank pays 5,000, an artillery tank 6,000, and the newer tank added in Season 2 pays 5,000.
- **Passengers.** A passenger delivered pays 250. A passenger spawned onto a vehicle gives the driver 100. Any other transport pays 20.
- **Vehicle upkeep.** Repairs pay 20 cash with a wrench or light drill and 25 with a heavy drill. Refuelling pays 10. The sources do not say which roles these events credit.
- **Supply crates.** Deploying a supply crate pays 25 for the free container, 50 for a small crate and 150 for a large one.

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Humvee.** The Humvee's cash cost in the Driver unlock tree went from 25,000 to 75,000.
- **Newer tank.** The newer tank pays 5,000 when destroyed. It is new in Season 2.
- **Artillery tank.** The artillery tank's per-kill session value went from 14,000 to 8,000.
- **Unlock tree.** The Driver tree gained 8 nodes and lost 2, including new ground vehicle variants. Several Driver level gates changed.
- **Skills.** The sources list no Season 2 change to the six Driver skill values.

## See also

- [Skills](skills.md)
- [Pilot](pilot.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Humvee](../vehicles/humvee.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)
- [Vehicle weapons](../vehicles/vehicle-weapons.md)
- [Vehicles](../vehicles.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Driver skill table
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Economy data: role unlock tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the supply crate durability skill and how it is applied to dropped crates
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
