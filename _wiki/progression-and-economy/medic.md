---
title: "Medic"
parent: "Progression & Economy"
group: "Roles"
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

Medic is one of the six roles and has the fewest skills, four. Two skills tune medical items: the medic switches to them faster, and a medkit lasts more uses. The other two give a short sprint boost to the medic who has just revived a teammate and to the teammate who was revived. A bare-hands revive pays 1,500 cash, more than a revive with a defibrillator.

## Overview

The skills apply to medical items and to the revive itself. The medical item skills apply to items in the medical archetype or to a specific item, and the revive skills apply after a revive ends.

The skill curves give a value for each step. The unlock level and cost of each step are not in the sources, so they are not yet known (see [Skills](skills.md)).

## Skills

| Skill | What it does | Curve values | Notes |
|---|---|---|---|
| Medical item switch speed | Faster switching to medical items. | 1, 1.2, 1.4 | Medical items only |
| Medkit uses | The medkit lasts more uses before it runs out. | 1, 0.8, 0.7, 0.6 | Only when the medic uses it. See [Medical Items](../equipment/medical-items.md). |
| Sprint boost after a revive (medic) | After reviving a teammate, the medic sprints faster for a short time. | 1, 1.2, 1.4 | Sprint and tac-sprint. The data gives the boost a duration of 5.0 with no unit. |
| Sprint boost after a revive (teammate) | After the medic revives a teammate, the revived player sprints faster for a short time. | 1, 1.2, 1.4 | Sprint and tac-sprint. Same duration of 5.0 with no unit. |

Curve values are listed in key order, starting with the first key. Speed skills use three values and the medkit skill uses four. The data does not confirm which key is which rank, so the rank reading is inferred.

## Mastery and rewards

All six roles share one mastery XP curve. The milestones for Medic are:

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

- **Rewards per level.** Not yet known. The sources do not list a reward for each Medic mastery level, and the platform mastery reward data has no entries for roles.
- **Unlock tree.** Medic items unlock through the role tree at a minimum mastery level, with a cash cost. The Season 2 section lists the changes, which are large for this role.

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

The data lists a second Adrenaline Pen row worth 100. The data does not say which row applies in which case. Revives in a zone are multiplied by 1.2 to 2.0.

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
- [Battle-pass track and Platform Mastery rewards](../../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
