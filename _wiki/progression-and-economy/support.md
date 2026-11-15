---
title: "Support"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Support role: 12 skills for LMGs and shotguns, a longer C4 detonator range, its mastery curve, and how it earns cash and XP from supply crates, buildables and forward bases."
---

# Support

S3 announcement: Large Hammer moves from level 8 to 14, and Verba from 14 to 8. See the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221); the current saved table below gives individual costs and prerequisites.

| Support | |
|---|---|
| **General** | |
| Skills | 12 |
| Focus | LMGs, shotguns and building |
| **Mastery** | |
| Stored XP at level 10 | 36,750 |
| Stored XP at level 50 | 1,950,000 |
| Stored XP at level 100 | 6,600,000 |
| Internal name | Meta.Role.Support, DT_SupportSkills |
{: .wiki-infobox }

Support has 12 saved skill-effect rows: 11 in the role table and the C4 detonator-range row in its plugin table. They configure LMG and shotgun handling plus detonator range; current activation and effective arithmetic remain unverified.

## Overview

The skill table below summarizes the configured effect targets and intended changes. Application requirements are saved filters, not evidence that the S3 consumer applies an effect. Historical application details are identified separately.

The reviewed skill-effect and curve exports do not supply per-level unlock costs. Earning, spending and upgrade consumers remain unresolved; this is not proof that costs or skill points are absent from the game (see [Skills](skills.md)).

## Skills

| Skill | Configured effect / historical interpretation | Stored curve values | Notes |
|---|---|---|---|
| Aim down sights time (LMGs) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | LMGs only |
| Aim down sights time (shotguns) | Less time to raise the sights. | 1, 0.8, 0.7, 0.6 | Shotguns only |
| Aim move speed (LMGs) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | LMGs only |
| Aim move speed (shotguns) | Faster walking while aimed down sights. | 1, 1.2, 1.4 | Shotguns only |
| Horizontal recoil (LMGs) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | LMGs only |
| Horizontal recoil (shotguns) | Less sideways kick. | 1, 0.8, 0.7, 0.6 | Shotguns only |
| C4 detonator range | The detonator works from further away. | 1, 1.2, 1.4 | One-time unlock |
| Ready to fire (LMGs) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | LMGs only |
| Ready to fire (shotguns) | The weapon comes up faster after sprinting, using a ladder or exiting a vault. | 1, 0.8, 0.7, 0.6 | Shotguns only |
| Vertical recoil (LMGs) | Less upward kick. | 1, 0.8, 0.7, 0.6 | LMGs only |
| Vertical recoil (shotguns) | Less upward kick. | 1, 0.8, 0.7, 0.6 | Shotguns only |
| Weapon switch speed | Faster switching to LMGs and shotguns. | 1, 1.2, 1.4 | LMGs and shotguns |

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
- **Current unlock tree.** 56 saved nodes, with level requirements from 1 to 50 and 3,100,000 cash in listed costs. These are stored requirements, not a test of server unlock behavior. The full current list is in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Current S3 unlock list

These 56 rows reproduce the CL533731 saved role tree: level prerequisites and cash **unlock costs**, not vendor purchase prices. Shared items can be unlocked through multiple roles in S3, as announced in the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). Mode restrictions and removed vendors still govern availability; a retained node alone is not an active shop offer.

| Role level | Item | Unlock cash |
|---:|---|---:|
| 1 | Light Drill | 10,000 |
| 2 | Field Backpack | 20,000 |
| 3 | Medium Hammer | 25,000 |
| 5 | RPG-7 | 30,000 |
| 6 | Level 1 Helmet | 7,500 |
| 6 | Level 1 Armor | 10,000 |
| 7 | Operator Backpack | 25,000 |
| 8 | 9K333 Verba | 50,000 |
| 9 | Medium Tac Vest | 10,000 |
| 10 | M500 | 50,000 |
| 11 | M500 Sabre Brake | 17,500 |
| 12 | PGO-7 | 10,000 |
| 12 | Assault Backpack | 50,000 |
| 13 | Improved Cylinder Choke | 7,500 |
| 13 | 12g Rifled Slug | 15,000 |
| 14 | Large Hammer | 75,000 |
| 15 | PKM | 100,000 |
| 15 | PKM 100 RND Box | 0 |
| 16 | Level 2 Helmet | 37,500 |
| 16 | Level 2 Armor | 50,000 |
| 17 | Full Choke | 30,000 |
| 17 | PKM Bipod | 25,000 |
| 18 | MAAWS | 100,000 |
| 18 | Sport Parachute | 25,000 |
| 19 | Slotted Flash Hider | 20,000 |
| 19 | 7.62x54mm Flesh Damage (HP) | 15,000 |
| 20 | M249 SAW | 150,000 |
| 20 | M249 100 RND Fabric Magazine | 0 |
| 21 | Large Tac Vest | 25,000 |
| 21 | Ruck Backpack | 100,000 |
| 22 | 4x Combat Prism Scope with Reflex | 35,000 |
| 23 | M249 Bipod | 50,000 |
| 24 | 5.56mm Flesh Damage (HP) | 15,000 |
| 25 | AT Mine | 75,000 |
| 25 | Gunner Backpack + Sling | 125,000 |
| 26 | M249 200 RND Box | 35,000 |
| 27 | Tread Brake | 10,000 |
| 28 | Heavy Drill | 50,000 |
| 29 | 5.56mm Armor Piercing (AP) | 75,000 |
| 30 | Evo-3 Ultra | 200,000 |
| 30 | Evo-3 Ultra 50 RND Box | 0 |
| 31 | .308 Win Flesh Damage (HP) | 15,000 |
| 32 | 12 Gauge Suppressor | 25,000 |
| 33 | Evo-3 Ultra Bipod | 75,000 |
| 35 | MGL-40 | 250,000 |
| 35 | 40mm | 0 |
| 36 | Level 3 Helmet | 75,000 |
| 36 | Level 3 Armor | 100,000 |
| 37 | 7.62x54mm Armor Piercing (AP) | 75,000 |
| 40 | Arsenal Backpack + 2 Slings | 175,000 |
| 41 | .308 Win Armor Piercing (AP) | 75,000 |
| 43 | SL7i-BL Suppressor | 35,000 |
| 45 | Level 4 Helmet | 150,000 |
| 45 | Level 4 Armor | 200,000 |
| 46 | Orpheus Max Brake | 40,000 |
| 50 | Hybrid Grip Pod | 50,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Support`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json). The [pinned earlier role article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/d3cf6f2bf54541b8389b9327aab933e1e8488b9b/_wiki/progression-and-economy/support.md) retains the earlier table for historical comparison.

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Support's work of resupply and building. Role XP for most events equals the base value of the event.

- **Deploying a supply crate.** The base cash is 25 for the free container, 50 for a small crate and 150 for a large one.
- **Destroying a supply crate.** An enemy supply crate pays 100 to 200.
- **Forward operating bases.** Hacking an enemy FOB pays 1,000. Destroying an enemy FOB pays 2,500, plus up to 7,500 by the supplies it holds. The FOB-supplied assist is divided by the number of assisters.
- **Buildables.** Destroying a Bunker or an Indirect Fire Shelter pays 200 cash and 50 Role XP. Destroying an enemy claymore, C4 or anti-tank mine pays 100 each. Other buildables mostly pay 10 to 500. Destroying a Drill Rig (the Hot Zone Magnet) pays 2,750 cash and 700 Role XP.
- **Supply crate assists.** Assist credit for a supply crate kill is split by assist type, as described in [Cash and Rewards](cash-and-rewards.md#how-it-works).

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Supply crates.** Deploying a supply crate went from 250 to 125 in the session-event calculator. A free crate destroyed went from 250 to 150.
- **Buildables.** The base cash for a gate went from 500 to 200, and for a repair station from 400 to 200.
- **Unlock tree.** The Support tree gained 5 nodes and lost 3. The heavy drill's cash cost went from 25,000 to 50,000.
- **Skills.** The sources list no Season 2 change to the 12 Support skill values.

## See also

- [Choosing a Role](../guides/choosing-a-role.md)
- [Skills](skills.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Building](../building.md)
- [C4 Charge](../equipment/c4-charge.md)
- [Weapons](../weapons.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Support skill table
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Rewards (buildables)](../../game-features/Wardogs_GameFeatures_Rewards_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Economy data: role unlock tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
