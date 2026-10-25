---
title: "Support"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Support role: 12 skills for LMGs and shotguns, a longer C4 detonator range, its mastery curve, and how it earns cash and XP from supply crates, buildables and forward bases."
---

# Support

| Support | |
|---|---|
| **General** | |
| Skills | 12 |
| Focus | LMGs, shotguns and building |
| **Mastery** | |
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Support, DT_SupportSkills |
{: .wiki-infobox }

Support is one of the six roles. Its 12 skills tune the heavy weapons: light machine guns (LMGs) and shotguns get faster aiming, less recoil and quicker switching. The role's one non-weapon skill extends the range of the C4 detonator. Support's earning events are mostly resupply and building work: supply crates, forward operating bases (FOBs) and buildables all pay cash and XP.

## Overview

Most Support skills apply to one weapon archetype. A skill for LMGs helps only LMGs, and a skill for shotguns helps only shotguns. The switching skill covers both archetypes at once.

Each skill's value comes from its curve at the skill's level. The unlock cost of each skill level is not in the game data, so it is not yet known (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
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

Curve values are listed in order for skill levels 0, 2, 3 and 4. Level 0 is always 1, which means no effect. Curves with three values store levels 0, 2 and 4 only, and levels in between are blended from the stored values.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Support are the total XP needed to reach each level, not the step from the level before:

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
- **Unlock tree.** 33 items and vehicles, from level 1 to level 50, with 1,630,000 cash in total. Each one needs a role level and a cash price (see Unlocks below).

## Unlocks

Each row is one item, vehicle or attachment in the Support unlock tree, with the role level it needs and its cash cost. The data gives no other cost for any unlock. Rows at 0 cash are magazines, ammunition and explosives. Where the data has no display name for an item, the row describes it in plain words.

| Role level | Item | Cash |
|---|---:|---:|
| 1 | Light repair drill | 10,000 |
| 3 | Medium hammer | 25,000 |
| 6 | 93mm | 0 |
| 6 | RPG-7 | 30,000 |
| 8 | Large hammer | 75,000 |
| 10 | M500 | 50,000 |
| 11 | M500 Sabre Brake | 17,500 |
| 12 | PGO-7 | 10,000 |
| 13 | Improved Cylinder Choke | 7,500 |
| 14 | 9K333 Verba | 50,000 |
| 15 | PKM magazine | 0 |
| 15 | PKM | 100,000 |
| 16 | Full Choke | 30,000 |
| 17 | PKM Bipod | 25,000 |
| 18 | MAAWS | 100,000 |
| 19 | Slotted Flash Hider | 20,000 |
| 20 | M249 100 RND Fabric Magazine | 0 |
| 20 | M249 SAW | 150,000 |
| 21 | 4x Combat Prism Scope with Reflex | 35,000 |
| 24 | M249 Bipod | 50,000 |
| 25 | Anti-tank mine | 75,000 |
| 26 | M249 200 RND Box | 35,000 |
| 27 | Tread Brake | 10,000 |
| 28 | Heavy repair drill | 50,000 |
| 30 | Evo-3 Ultra 50 RND Box | 0 |
| 30 | Evo-3 Ultra | 200,000 |
| 32 | 12 Gauge Suppressor | 25,000 |
| 33 | Evo-3 Ultra Bipod | 75,000 |
| 35 | 40mm | 0 |
| 35 | MGL-40 | 250,000 |
| 40 | SL7i-BL Suppressor | 35,000 |
| 45 | Orpheus Max Brake | 40,000 |
| 50 | Hybrid Grip Pod | 50,000 |

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
