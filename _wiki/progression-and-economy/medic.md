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
| XP to level 10 | 25,000 |
| XP to level 50 | 1,150,000 |
| XP to level 100 | 5,132,500 |
| Internal name | Meta.Role.Medic, DT_MedicSkills |
{: .wiki-infobox }

Medic is one of the six roles and has the fewest skills with numbers, four. Its tree has 23 nodes. The other 19 have no number in the game and no game code reads them, so their effect is not known. Two skills tune medical items: the medic switches to them faster, and a medkit lasts more uses. The other two give a short sprint boost to the medic who has just revived a teammate and to the teammate who was revived. A bare-hands revive pays 1,500 cash, more than a revive with a defibrillator.

## Overview

The skills apply to medical items and to the revive itself. The medical item skills apply to items in the medical archetype or to a specific item, and the revive skills apply after a revive ends.

Each skill's value comes from its curve at the skill's level. The game has no unlock cost or skill points for the skill levels (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
|---|---|---|---|
| Medical item switch speed | Faster switching to medical items. | 1, 1.2, 1.4 | Medical items only |
| Medkit uses | The medkit lasts more uses before it runs out. | 1, 0.8, 0.7, 0.6 | Only when the medic uses it. See [Medical Items](../equipment/medical-items.md). |
| Sprint boost after a revive (medic) | After reviving a teammate, the medic sprints faster for a short time. | 1, 1.2, 1.4 | Sprint and tac-sprint. The game gives the boost a duration of 5.0 with no unit. |
| Sprint boost after a revive (teammate) | After the medic revives a teammate, the revived player sprints faster for a short time. | 1, 1.2, 1.4 | Sprint and tac-sprint. Same duration of 5.0 with no unit. |

Curve values are listed in order for skill levels 0, 2, 3 and 4. Level 0 is always 1, which means no effect. Curves with three values store levels 0, 2 and 4 only, and levels in between are blended from the stored values.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Medic are the total XP needed to reach each level, not the step from the level before:

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

- **Rewards per level.** None. The level table has an empty reward list for every level, so a level gives no reward of its own. What a level gives is access to the unlock tree (see Unlocks below).
- **Unlock tree.** 38 items and vehicles, from level 1 to level 50, with 1,220,000 cash in total. Each one needs a role level and a cash price (see Unlocks below).

## Unlocks

Each row is one item, vehicle or attachment in the Medic unlock tree, with the role level it needs and its cash cost. The game gives no other cost for any unlock. Rows at 0 cash are magazines, ammunition and explosives. Where the game gives no display name for an item, the row describes it in plain words.

| Role level | Item | Cash |
|---|---:|---:|
| 1 | Eclipse Flash Hider | 7,500 |
| 2 | Resuscitator | 10,000 |
| 4 | MP5 20 RND Magazine | 0 |
| 4 | MP5 | 25,000 |
| 5 | White smoke grenade | 7,500 |
| 6 | Holographic Sight | 20,000 |
| 8 | MP5 30 RND Magazine | 10,000 |
| 10 | Individual First Aid Kit | 25,000 |
| 11 | AFG Angled Foregrip | 10,000 |
| 12 | Ballista Brake | 15,000 |
| 13 | QD-5 Suppressor | 12,500 |
| 14 | Medkit | 50,000 |
| 15 | PP-19 Vityaz magazine | 0 |
| 15 | PP-19 Vityaz | 50,000 |
| 16 | Stim Pen | 25,000 |
| 17 | PP-19 Vityaz 10 RND Magazine | 10,000 |
| 18 | PP-19 Vityaz Flash Hider | 17,500 |
| 19 | Vektor Frenix-X Micro Reflex Sight | 15,000 |
| 20 | AMP-9 15 RND Magazine | 0 |
| 20 | AMP-9 | 75,000 |
| 21 | PP-19 50 RND Vityaz Drum Magazine | 15,000 |
| 22 | Defibrillator | 110,000 |
| 23 | Black smoke grenade | 15,000 |
| 24 | PP-19-01 Vityaz 9x19 Suppressor | 20,000 |
| 25 | AMP-9 20 RND Magazine | 12,500 |
| 26 | AMP-9 Tactical Flash Hider | 45,000 |
| 27 | AMP-9 9x19 Suppressor | 25,000 |
| 28 | Dual Port Brake | 22,500 |
| 29 | MP5 50 RND Drum Magazine | 50,000 |
| 30 | AMP-9 magazine | 50,000 |
| 35 | Super-45 13 RND Magazine | 0 |
| 35 | Super-45 | 200,000 |
| 36 | Super-45 Flash Hider | 40,000 |
| 40 | Ghost LITE Muzzle Brake | 30,000 |
| 43 | Super-45 30 RND Magazine | 25,000 |
| 45 | AMP-9 50 RND Drum Magazine | 75,000 |
| 48 | SG Multi-Caliber Suppressor | 50,000 |
| 50 | Super-45 40 RND Drum Magazine | 50,000 |

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
