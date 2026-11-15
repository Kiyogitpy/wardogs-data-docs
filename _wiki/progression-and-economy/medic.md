---
title: "Medic"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The Medic role: 4 skills for medical items, medkit uses and sprint boosts after a revive, its mastery curve, and how it earns cash and XP from heals and revives."
---

# Medic

| Medic | |
|---|---|
| **General** | |
| Skills | 4 |
| Focus | Medical items and reviving teammates |
| **Mastery** | |
| Stored XP at level 10 | 36,750 |
| Stored XP at level 50 | 1,950,000 |
| Stored XP at level 100 | 6,600,000 |
| Internal name | Meta.Role.Medic, DT_MedicSkills |
{: .wiki-infobox }

Medic has four saved skill-effect rows for medical-item switching, medkit usage and revive speed boosts. The earlier skill-tree inventory lists 23 nodes; lack of an effect mapping for the other 19 in the reviewed exports does not exclude other current consumers. Both Self and Teammate speed-boost rows use Meta.Skill.Revive.Target, so their names alone do not prove which player receives the boost.

## Overview

The skill table below summarizes the configured effect targets and intended changes. Application requirements are saved filters, not evidence that the S3 consumer applies an effect. Historical application details are identified separately.

The reviewed skill-effect and curve exports do not supply per-level unlock costs. Earning, spending and upgrade consumers remain unresolved; this is not proof that costs or skill points are absent from the game (see [Skills](skills.md)).

## Skills

| Skill | Configured effect / historical interpretation | Stored curve values | Notes |
|---|---|---|---|
| Medical item switch speed | Faster switching to medical items. | 1, 1.2, 1.4 | Medical items only |
| Medkit uses | The medkit lasts more uses before it runs out. | 1, 0.8, 0.7, 0.6 | Only when the medic uses it. See [Medical Items](../equipment/medical-items.md). |
| Sprint boost after a revive (medic) | Self-named sprint/tac-sprint curve; saved slot is Meta.Skill.Revive.Target, so recipient remains unresolved. | 1, 1.2, 1.4 | Sprint and tac-sprint. The game gives the boost a duration of 5.0 with no unit. |
| Sprint boost after a revive (teammate) | Teammate-named sprint/tac-sprint curve; saved slot is Meta.Skill.Revive.Target, current application unverified. | 1, 1.2, 1.4 | Sprint and tac-sprint. Same duration of 5.0 with no unit. |

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
- **Current unlock tree.** 59 saved nodes, with level requirements from 1 to 50 and 2,585,000 cash in listed costs. These are stored requirements, not a test of server unlock behavior. The full current list is in the [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

## Current S3 unlock list

These 59 rows reproduce the CL533731 saved role tree: level prerequisites and cash **unlock costs**, not vendor purchase prices. Shared items can be unlocked through multiple roles in S3, as announced in the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). Mode restrictions and removed vendors still govern availability; a retained node alone is not an active shop offer.

| Role level | Item | Unlock cash |
|---:|---|---:|
| 1 | Eclipse Flash Hider | 7,500 |
| 2 | Field Resuscitator | 10,000 |
| 3 | Field Backpack | 20,000 |
| 4 | MP5 | 25,000 |
| 4 | MP5 20 RND Magazine | 0 |
| 5 | M18 Smoke Grenade: White | 7,500 |
| 5 | Medium Tac Vest | 10,000 |
| 6 | Level 1 Helmet | 7,500 |
| 6 | Level 1 Armor | 10,000 |
| 7 | Holographic Sight | 20,000 |
| 8 | MP5 30 RND Magazine | 10,000 |
| 8 | 9mm Flesh Damage (HP) | 15,000 |
| 10 | Individual First Aid Kit | 25,000 |
| 11 | AFG Angled Foregrip | 10,000 |
| 11 | Operator Backpack | 25,000 |
| 12 | Ballista Brake | 15,000 |
| 12 | Large Tac Vest | 25,000 |
| 13 | QD-5 Suppressor | 12,500 |
| 14 | Medical Bag | 50,000 |
| 14 | Assault Backpack | 50,000 |
| 15 | PP-19 Vityaz | 50,000 |
| 15 | PP-19 Vityaz 30 RND Magazine | 0 |
| 16 | Level 2 Helmet | 37,500 |
| 16 | Level 2 Armor | 50,000 |
| 17 | PP-19 Vityaz 10 RND Magazine | 10,000 |
| 17 | Adrenaline Pen | 25,000 |
| 18 | PP-19 Vityaz Flash Hider | 17,500 |
| 18 | Sport Parachute | 25,000 |
| 19 | Vektor Frenix-X Micro Reflex Sight | 15,000 |
| 20 | AMP-9 | 75,000 |
| 20 | AMP-9 15 RND Magazine | 0 |
| 21 | PP-19 50 RND Vityaz Drum Magazine | 15,000 |
| 22 | Defibrillator | 110,000 |
| 23 | M18 Smoke Grenade: Black | 15,000 |
| 23 | Ruck Backpack | 100,000 |
| 24 | PP-19-01 Vityaz 9x19 Suppressor | 20,000 |
| 25 | AMP-9 20 RND Magazine | 12,500 |
| 26 | AMP-9 Tactical Flash Hider | 45,000 |
| 27 | AMP-9 9x19 Suppressor | 25,000 |
| 28 | Dual Port Brake | 22,500 |
| 29 | MP5 50 RND Drum Magazine | 50,000 |
| 29 | Gunner Backpack + Sling | 125,000 |
| 30 | AMP-9 30 RND Magazine | 50,000 |
| 33 | 9mm Armor Piercing (AP) | 75,000 |
| 35 | Super-45 | 200,000 |
| 35 | Super-45 13 RND Magazine | 0 |
| 36 | Level 3 Helmet | 75,000 |
| 36 | Level 3 Armor | 100,000 |
| 37 | Super-45 Flash Hider | 40,000 |
| 37 | .45 ACP Flesh Damage (HP) | 15,000 |
| 40 | Ghost LITE Muzzle Brake | 30,000 |
| 41 | .45 ACP Armor Piercing (AP) | 75,000 |
| 42 | Super-45 30 RND Magazine | 25,000 |
| 44 | AMP-9 50 RND Drum Magazine | 75,000 |
| 45 | Level 4 Helmet | 150,000 |
| 45 | Level 4 Armor | 200,000 |
| 46 | SG Multi-Caliber Suppressor | 50,000 |
| 48 | Arsenal Backpack + 2 Slings | 175,000 |
| 50 | Super-45 40 RND Drum Magazine | 50,000 |

Source: [current role tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json), `Meta.Role.Medic`; [economy output](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json). The [pinned earlier role article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/d3cf6f2bf54541b8389b9327aab933e1e8488b9b/_wiki/progression-and-economy/medic.md) retains the earlier table for historical comparison.

## How the role earns cash and XP

The reward tables list events, not roles. The events below are the ones that fit Medic's work of healing and reviving. Role XP for most events equals the base value of the event.

Revive cash goes to the player who revives:

| Revive item | Cash to the reviver |
|---|---|
| Bare hands | 1,500 |
| Defibrillator | 1,000 |
| Resuscitator | 1,000 |
| Medical Bag | 800 |
| Adrenaline Pen | 400 |

The game lists a second Adrenaline Pen entry worth 100. The game does not say which entry applies in which case. Revives in a zone are multiplied by 1.2 to 2.0.

Heal cash goes to the player who heals:

| Heal item | Cash to the healer |
|---|---|
| No item | 10 |
| [Bandage](../equipment/bandage.md) | 400 |
| [Individual First Aid Kit](../equipment/individual-first-aid-kit.md) | 1,000 |
| [Medical Bag](../equipment/medical-bag.md) | 100 |

When a heal brings a downed player back, it pays 1,500 with a defibrillator or resuscitator, and 1,200 with an Adrenaline Pen.

## Season 2 changes

- **Mastery curve.** Role mastery XP was lowered from level 10 upward for all roles. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, level 50 from 1,500,000 to 1,150,000, and level 100 from 6,000,000 to 5,132,500.
- **Unlock tree.** The Medic tree gained 4 nodes and lost 2. The [Defibrillator](../equipment/defibrillator.md) cash cost went from 50,000 to 110,000, and its level gate went from 11 to 22. Several other Medic unlocks changed cost or level gate. The Season 2 page lists them.
- **Skills.** The sources list no Season 2 change to the four Medic skill values.

## See also

- [Choosing a Role](../guides/choosing-a-role.md)
- [Skills](skills.md)
- [Cash and Rewards](cash-and-rewards.md)
- [Medical Items](../equipment/medical-items.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)
- [Defibrillator](../equipment/defibrillator.md)
- [Medical Bag](../equipment/medical-bag.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Medic skill table
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Reward track and platform mastery data](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Economy data: role unlock tree](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
