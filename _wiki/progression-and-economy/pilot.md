---
title: "Pilot"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Pilot role: 6 skills for air vehicles, covering mounted machine gun aiming and recoil, fuel use, impact damage and supply crate durability, plus its mastery curve and earnings."
---

# Pilot

| Pilot | |
|---|---|
| **General** | |
| Skills | 6 |
| Focus | Air vehicles and their mounted machine guns |
| **Mastery** | |
| Stored XP at level 10 | 36,750 |
| Stored XP at level 50 | 1,950,000 |
| Stored XP at level 100 | 6,600,000 |
| Internal name | Meta.Role.Pilot, DT_PilotSkills |
{: .wiki-infobox }

Pilot has six saved skill-effect rows for the named mounted gun, vehicle fuel and impact attributes, and a supply-crate effect. The gun rows require Id.Item.ROT_01.MountedMachineGun. These mappings do not prove current activation or application to every air vehicle.

## Overview

The skill table below summarizes the configured effect targets and intended changes. Application requirements are saved filters, not evidence that the S3 consumer applies an effect. Historical application details are identified separately.

The reviewed skill-effect and curve exports do not supply per-level unlock costs. Earning, spending and upgrade consumers remain unresolved; this is not proof that costs or skill points are absent from the game (see [Skills](skills.md)).

## Skills

| Skill | Configured effect / historical interpretation | Stored curve values | Notes |
|---|---|---|---|
| Aim down sights time (mounted machine gun) | Less time to raise the sights on the mounted machine gun. | 1, 0.8, 0.7, 0.6 | Mounted machine gun on air vehicles |
| Fuel use | Less fuel used in air vehicles, for a longer fuel time. | 1, 0.8, 0.7, 0.6 | Air vehicles. The saved row names the fuel-usage multiplier effect; current override arithmetic is unverified. |
| Horizontal recoil (mounted machine gun) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Mounted machine gun on air vehicles |
| Impact damage | Less damage when the air vehicle hits objects or the ground. | 1, 0.8, 0.7, 0.6 | Air vehicles. The saved row names the impact-reduction multiplier effect; current override arithmetic is unverified. |
| Supply crate durability | The Meta.Skill.SupplyCrate row references GE_Vehicle_Health and a 1.0 / 1.2 / 1.4 curve. The CL516586 round 42 trace associated it with dropped-crate creation; S3 recipient and spawn-time application remain unverified. | 1, 1.2, 1.4 | Crates the pilot drops |
| Vertical recoil (mounted machine gun) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Mounted machine gun on air vehicles |

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
- **Current unlock tree.** 34 saved nodes, with level requirements from 2 to 50 and 2,723,250 cash in listed costs. These are stored requirements, not a test of server unlock behavior. The full current list is in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Current S3 unlock list

These 34 rows reproduce the CL533731 saved role tree: level prerequisites and cash **unlock costs**, not vendor purchase prices. Shared items can be unlocked through multiple roles in S3, as announced in the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). Mode restrictions and removed vendors still govern availability; a retained node alone is not an active shop offer.

| Role level | Item | Unlock cash |
|---:|---|---:|
| 2 | Small Armored Crate | 10,000 |
| 4 | Field Backpack | 20,000 |
| 5 | HORA - Irina Rimes & Jerry Heil | 750 |
| 7 | Level 1 Helmet | 7,500 |
| 7 | Level 1 Armor | 10,000 |
| 8 | AH-6M [Miniguns] | 125,000 |
| 10 | Z20 Lakota | 35,000 |
| 11 | Mechanical Supply Pallet | 10,000 |
| 12 | Operator Backpack | 25,000 |
| 13 | H4ZARD - Gigilow | 2,500 |
| 14 | Ammo Supply Pallet | 25,000 |
| 14 | Medium Tac Vest | 10,000 |
| 15 | Sport Parachute | 25,000 |
| 18 | Large Crate | 20,000 |
| 19 | Fuel Supply Pallet | 50,000 |
| 20 | AH-6R [Rockets] | 250,000 |
| 21 | Level 2 Helmet | 37,500 |
| 21 | Level 2 Armor | 50,000 |
| 22 | Large Tac Vest | 25,000 |
| 22 | Assault Backpack | 50,000 |
| 23 | Helikopter - Fazlija | 10,000 |
| 25 | Z20 Lakota [Miniguns] | 85,000 |
| 26 | Ruck Backpack | 100,000 |
| 26 | .308 Win Flesh Damage (HP) | 15,000 |
| 30 | Large Armored Crate | 50,000 |
| 33 | Ride of the Valkyries - Richard Wagner | 25,000 |
| 34 | Gunner Backpack + Sling | 125,000 |
| 35 | Havoc | 750,000 |
| 36 | .308 Win Armor Piercing (AP) | 75,000 |
| 41 | Level 3 Helmet | 75,000 |
| 41 | Level 3 Armor | 100,000 |
| 46 | Arsenal Backpack + 2 Slings | 175,000 |
| 50 | Level 4 Helmet | 150,000 |
| 50 | Level 4 Armor | 200,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Pilot`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json). The [pinned earlier role article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/d3cf6f2bf54541b8389b9327aab933e1e8488b9b/_wiki/progression-and-economy/pilot.md) retains the earlier table for historical comparison.

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

- [Choosing a Role](../guides/choosing-a-role.md)
- [Helicopter Guide](../guides/helicopter-guide.md)
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
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the supply crate durability skill and how it is applied to dropped crates
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
