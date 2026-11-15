---
title: "Driver"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Driver role: 6 skills for ground vehicles, covering mounted machine gun aiming and recoil, fuel use, impact damage and supply crate durability, plus its mastery curve and earnings."
---

# Driver

S3 announcement: The announcement summarizes tank unlocks as moving from Driver levels 20–35 to 35–50, and returning to the Wardog track at level 200 instead of 145. The saved individual gates differ: see the [Wardog table](currencies.md#current-s3-wardog-unlocks), where L2A6 is 200 but T-72B3 is 155, SPH-2 is 145 and Vanguard AA is 165. See the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221); the current saved table below gives individual costs and prerequisites.

| Driver | |
|---|---|
| **General** | |
| Skills | 6 |
| Focus | Ground vehicles and their mounted machine guns |
| **Mastery** | |
| Stored XP at level 10 | 36,750 |
| Stored XP at level 50 | 1,950,000 |
| Stored XP at level 100 | 6,600,000 |
| Internal name | Meta.Role.Driver, DT_DriverSkills |
{: .wiki-infobox }

Driver has six saved skill-effect rows for the named mounted gun, vehicle fuel and impact attributes, and a supply-crate effect. The gun rows require ID.Item.HeavyTankMountedMachineGun. These mappings do not prove current activation or application to every ground vehicle.

## Overview

The skill table below summarizes the configured effect targets and intended changes. Application requirements are saved filters, not evidence that the S3 consumer applies an effect. Historical application details are identified separately.

The reviewed skill-effect and curve exports do not supply per-level unlock costs. Earning, spending and upgrade consumers remain unresolved; this is not proof that costs or skill points are absent from the game (see [Skills](skills.md)).

## Skills

| Skill | Configured effect / historical interpretation | Stored curve values | Notes |
|---|---|---|---|
| Aim down sights time (mounted machine gun) | Less time to raise the sights on the mounted machine gun. | 1, 0.8, 0.7, 0.6 | Heavy tank's mounted machine gun |
| Fuel use | Less fuel used in ground vehicles, for a longer fuel time. | 1, 0.8, 0.7, 0.6 | Ground vehicles. The saved row names the fuel-usage multiplier effect; current override arithmetic is unverified. |
| Horizontal recoil (mounted machine gun) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Heavy tank's mounted machine gun |
| Impact damage | Less damage when the ground vehicle hits objects or the landscape. | 1, 0.8, 0.7, 0.6 | Ground vehicles. The saved row names the impact-reduction multiplier effect; current override arithmetic is unverified. |
| Supply crate durability | The Meta.Skill.SupplyCrate row references GE_Vehicle_Health and a 1.0 / 1.2 / 1.4 curve. The CL516586 round 42 trace associated it with dropped-crate creation; S3 recipient and spawn-time application remain unverified. | 1, 1.2, 1.4 | Crates the driver drops |
| Vertical recoil (mounted machine gun) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Heavy tank's mounted machine gun |

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
- **Current unlock tree.** 49 saved nodes, with level requirements from 2 to 50 and 4,363,250 cash in listed costs. These are stored requirements, not a test of server unlock behavior. The full current list is in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Current S3 unlock list

These 49 rows reproduce the CL533731 saved role tree: level prerequisites and cash **unlock costs**, not vendor purchase prices. Shared items can be unlocked through multiple roles in S3, as announced in the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). Mode restrictions and removed vendors still govern availability; a retained node alone is not an active shop offer.

| Role level | Item | Unlock cash |
|---:|---|---:|
| 2 | Small Armored Crate | 10,000 |
| 3 | Ural | 35,000 |
| 4 | Mechanical Supply Pallet | 10,000 |
| 4 | Field Backpack | 20,000 |
| 5 | Tianqi Xu - Vodka Bomb | 750 |
| 6 | Kodiak [M249] | 50,000 |
| 7 | Level 1 Helmet | 7,500 |
| 7 | Level 1 Armor | 10,000 |
| 8 | Wolf-110 | 50,000 |
| 9 | 5.56mm Flesh Damage (HP) | 15,000 |
| 10 | Kodiak [Pickup] | 35,000 |
| 11 | Ammo Supply Pallet | 25,000 |
| 12 | Dune Buggy | 25,000 |
| 12 | Operator Backpack | 25,000 |
| 13 | Liuli-Liuli - Masha Kondratenko | 2,500 |
| 14 | Medium Tac Vest | 10,000 |
| 15 | Humvee | 75,000 |
| 16 | Ural Defender | 75,000 |
| 17 | Wolf-110 [M2 Browning] | 125,000 |
| 18 | Large Crate | 20,000 |
| 18 | Sport Parachute | 25,000 |
| 19 | Fuel Supply Pallet | 50,000 |
| 20 | Ural Defender [M249] | 100,000 |
| 21 | Level 2 Helmet | 37,500 |
| 21 | Level 2 Armor | 50,000 |
| 22 | Large Tac Vest | 25,000 |
| 22 | Assault Backpack | 50,000 |
| 23 | You Are Not Invited - MokuMoku | 10,000 |
| 24 | Large Armored Crate | 50,000 |
| 25 | Humvee [M249] | 125,000 |
| 26 | Ruck Backpack | 100,000 |
| 28 | Giants (Remix) - The Qemists | 10,000 |
| 29 | 5.56mm Armor Piercing (AP) | 75,000 |
| 30 | Humvee [Minigun] | 150,000 |
| 31 | .308 Win Flesh Damage (HP) | 15,000 |
| 33 | Dyshat' - Baryber | 25,000 |
| 34 | Gunner Backpack + Sling | 125,000 |
| 35 | T-72B3 | 250,000 |
| 36 | 7.62x54mm Flesh Damage (HP) | 15,000 |
| 38 | 7.62x54mm Armor Piercing (AP) | 75,000 |
| 40 | SPH-2 | 350,000 |
| 41 | Level 3 Helmet | 75,000 |
| 41 | Level 3 Armor | 100,000 |
| 43 | .308 Win Armor Piercing (AP) | 75,000 |
| 45 | Flakpanzer Gepard | 500,000 |
| 46 | Arsenal Backpack + 2 Slings | 175,000 |
| 48 | Level 4 Helmet | 150,000 |
| 48 | Level 4 Armor | 200,000 |
| 50 | L2A6 | 750,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Driver`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json). The [pinned earlier role article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/d3cf6f2bf54541b8389b9327aab933e1e8488b9b/_wiki/progression-and-economy/driver.md) retains the earlier table for historical comparison.

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

- [Choosing a Role](../guides/choosing-a-role.md)
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
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
