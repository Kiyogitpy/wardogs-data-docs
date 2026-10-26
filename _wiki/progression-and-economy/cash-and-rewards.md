---
title: "Cash and Rewards"
parent: "Progression & Economy"
group: "Economy"
description: "What each action pays in cash and role XP: kills, revives, heals, vehicles, zones, spotting, supply crates and the end-of-match bonus."
---

# Cash and Rewards

| Cash and Rewards | |
|---|---|
| Currencies | Cash (starts at 10,000; 3,000 in Strike and Disarm, 2,000 in VIP Escort), Gold Bars (see [Cosmetics](cosmetics.md)) |
| XP | One role XP per role: Assault, Medic, Support, Recon, Pilot and Driver |
| Mastery levels | 0 to 100 for each role, on one shared XP curve |
| Internal name | Reward cash tables and the per-kill calculator |
{: .wiki-infobox }

Every action in a match pays cash, and most also pay role XP. The base amount for an action depends on what was done: a kill with a default weapon pays 250, a kill from artillery in the open pays 5,000, and a Havoc attack helicopter destroyed pays 6,000. Zones and nearby kills are then multiplied, and the winning faction gets a bonus at the end.

## Overview

Cash pays for gear, weapons, vehicles and skills. Role XP raises a role's mastery level. Both are earned during the match, and the end-of-match bonus adds more on top. This article lists the base values; the per-kill formula is in [How it works](#how-it-works).

## How it works

- **Base value.** Each action has a base cash value from its reward table.
- **Zone multiplier.** A reward can be multiplied when it happens in a Control Zone or a Hot Zone. A kill in a Hot Zone counts with a weight of 10, a kill in a Control Zone with a weight of 5. A kill in the enemy's own Hot Zone counts with weight 4, and in the enemy's own Control Zone with weight 2.
- **Assists.** Assist credit is split between the player who did the damage and the assisters, by assist type: crew, logistics, revive, FOB-supplied, supply crate, and the general assist. A FOB-supplied assist is divided by the number of assisters.
- **Repeat victims.** Each repeat kill on the same player pays 24% less, up to four repeats. Spotting has its own, harsher rule: 50% less for each repeat, up to two (see [Spotting](../game-mechanics/spotting.md)).
- **Kill streaks.** Each streak kill adds 50 to the base, up to five. Ending an enemy's streak pays 1.5 times. Revenge kills pay 2.0 times.
- **Penalties.** A teamkill pays a negative amount. A kill on a player an enemy has just revived (for 60 s) is a "No Value Kill": cash is 0.01 times, and it pays no Role XP and no assist XP. Crew kills split the reward down by crew count (each extra crew member multiplies it by 0.8).
- **Pre-lobby points.** In King of the Hill, points earned while waiting for the match (up to 5,000) are paid as extra starting Cash at one Cash per point when the match starts. See [Pre-lobby](../game-modes-and-maps/pre-lobby.md).
- **Role XP.** For most events the role XP is the base value itself, without the zone and assist multipliers. Kill XP falls with repeat victims in the same way as kill cash.

## Numbers

### Kills

| Kill | Base cash |
|---|---|
| Default player kill | 250 |
| Killed from artillery while the attacker is in open ground | 5,000 |
| Artillery kill while the attacker is inside a zone | 100 |

The per-kill calculator uses a different base for each kill type: default 300, headshot 350, precision artillery strike 250, and air vehicle 300. The shared challenge reward rows used by the King of the Hill challenges also give 300 for a player kill (and 600 for a defibrillator revive, 200 for a Bandage heal), see [King of the Hill Challenges](king-of-the-hill-challenges.md).

### Revives and heals

| Revive (cash to the reviver) | Base cash |
|---|---|
| Bare hands | 1,500 |
| Defibrillator | 1,000 |
| Resuscitator | 1,000 |
| Medical Bag | 800 |
| Adrenaline Pen | 400 |
| Adrenaline Pen (a separate reward row with the same name) | 100 |

| Heal (cash to the healer) | Base cash |
|---|---|
| Heal with no item | 10 |
| Bandage | 400 |
| Individual First Aid Kit | 1,000 |
| Medical Bag | 100 |

When a heal is the one that brings a downed player back, it pays 1,500 with a defibrillator or resuscitator, and 1,200 with an Adrenaline Pen. Revives in a zone are multiplied by 1.2 to 2.0. Healing in your own team's spawn safe zone pays nothing (see [Boundaries and Safe Zones](../game-modes-and-maps/boundaries-and-safe-zones.md)); the same goes for repairing and refuelling there.

### Vehicles

| Vehicle destroyed | Base cash |
|---|---|
| Dune Buggy | 300 |
| Bobcat | 100 |
| Humvee | 500 |
| Kodiak | 500 |
| MH-6 (Little Bird) | 800 |
| [Huey](../vehicles/huey.md) (in the reward table, not sold in any shop) | 1,200 |
| Heavy tank | 5,000 |
| Artillery tank | 6,000 |
| Newer tank (Season 2) | 5,000 |
| Havoc attack helicopter | 6,000 |
| Spawn vehicle | 4,000 |

Repairs pay 20 cash with a wrench or light drill and 25 with a heavy drill. Refuelling pays 10. A passenger delivered pays 250, a passenger who is spawned onto a vehicle gives the driver 100, and any other transport pays 20.

### Zones and towers

| Event | Base cash |
|---|---|
| Control Zone contested, owned or not owned | 150 each |
| Entering a Control Zone (first time in a life) | 100 |
| Hot Zone contested, owned or not owned | 600 each |
| Entering a Hot Zone | 0 |
| Activating the Hot Zone Magnet | 5,000 |
| Deactivating the Hot Zone Magnet | 200 |
| Capturing a hostile tower | 1,000 |
| Capturing a neutral tower | 250 |
| Spawn vehicle reaching a Control Zone | 3,000 |

See [Control Zone](../game-modes-and-maps/control-zone.md) for the zone rules.

### Spotting, supply crates and buildables

| Event | Cash |
|---|---|
| Spotting a target | 15 to 275, scaled by the spot's contribution |
| Destroying a spotted target | 50 to 500, on the same scale |
| Deploying a supply crate | 25 (free container), 50 (small), 150 (large) |
| Destroying an enemy claymore, C4 or anti-tank mine | 100 each |
| Destroying an enemy supply crate | 100 to 200 |
| Placing a forward operating base (FOB) | 1,000 |
| Destroying an enemy FOB | 2,500, plus up to 7,500 by the FOB's supplies |
| Destroying a Hot Zone Magnet structure | 3,000 in the flat buildable cash table; the challenge reward row for the Drill Rig gives 2,750 and 700 Role XP (see [Buildable Challenges](buildable-challenges.md)) |

Destroying a Bunker, Recon Tower, Indirect Fire Shelter, Gate, Loudspeaker, Refuel Station or Repair Station pays 200 cash and 50 Role XP. A Vanguard CIWS pays 1,200 and 300, and an L81 Mortar or Talon 9K-SAM 650 and 175. Walls and other small buildables pay 5 to 85 cash. Placing a schematic pays 10 cash in a control zone and 20 in a hot zone, and nothing outside a zone. Building pays 5 cash per point of build progress inside a zone and 1 outside.

### End-of-match bonus

At the end of a match each faction is ranked and paid:

| Place | Cash bonus (share of match cash) | XP bonus (share of match XP, per role) | Flat cash |
|---|---|---|---|
| 1st | 0.30 times | 2.0 times | 200 |
| 2nd | 0.25 times | 1.75 times | 150 |
| 3rd | 0.20 times | 1.5 times | 100 |

The cash input is capped at 100,000 and the XP input at 2,500 before the multiplier applies. In Season 2 a separate bonus gives the Lonestar faction 10,000 cash at match end; the other two factions get nothing from that row.

## Role mastery XP

All six roles use the same XP curve. Milestones:

| Level | XP needed |
|---|---|
| 1 | 200 |
| 5 | 6,250 |
| 10 | 25,000 |
| 20 | 111,500 |
| 30 | 318,200 |
| 50 | 1,150,000 |
| 75 | 2,218,000 |
| 100 | 5,132,500 |

The data gives one XP value per level. Each value is the total Role XP needed to reach that level, not the step from the level before.

### Mastery rewards per level

Each role's mastery runs from level 0 to level 100 and gives no reward of its own: the level table has an empty reward list for every level. What a level opens is the role's unlock tree, where each item or vehicle needs a role level and a cash price. The table counts those unlocks for each tree. The Wardog tree is the overall level, and it runs to level 150. The game files hold no rule for how the six role levels add up to the overall level.

| Tree | Unlocks | Level range | Cash in the tree |
|---|---:|---:|---:|
| Assault | 40 | 2 to 50 | 1,270,000 |
| Recon | 58 | 2 to 50 | 2,445,000 |
| Support | 33 | 1 to 50 | 1,630,000 |
| Medic | 38 | 1 to 50 | 1,220,000 |
| Pilot | 11 | 2 to 35 | 1,218,250 |
| Driver | 21 | 3 to 35 | 2,308,250 |
| Wardog (overall level) | 63 | 1 to 150 | 2,645,000 |

The unlock rows for each role are on its page, under Unlocks.

## Tips that follow from the numbers

- Artillery kills in open ground pay 5,000, against 250 for a default kill. The per-kill calculator adds the zone and streak multipliers on top.
- A Hot Zone event pays 600, against 150 for a Control Zone event, so a Hot Zone is worth about four times as much per event.
- A bare-hands revive pays 1,500, more than a defibrillator revive (1,000). A defibrillator still pays 1,500 on the heal side when used on a downed player.
- Teamkills cost cash through a negative multiplier, so they are a loss rather than a gain.

## Season 2 changes

- Role mastery XP was lowered from level 10 upward. Level 10 went from 35,000 to 25,000, level 20 from 250,000 to 111,500, and level 100 from 6,000,000 to 5,132,500.
- The newer tank (Season 2) pays 5,000 when destroyed.
- The end-of-match bonus for the Lonestar faction (10,000) is new.
- Supply crate values were reduced: deploying a supply crate went from 250 to 125, and a free crate destroyed went from 250 to 150.
- Vehicle session rewards were lowered: the artillery vehicle's per-kill value went from 14,000 to 8,000, and the Phalanx from 3,000 to 1,200.

## See also

- [Challenges](challenges.md)
- [Skills](skills.md)
- [Shops](shops.md)
- [Control Zone](../game-modes-and-maps/control-zone.md)
- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md)
- [Pre-lobby](../game-modes-and-maps/pre-lobby.md), where waiting points turn into extra starting Cash

## Sources

- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Session-event reward lookups](../../content/Wardogs_RewardLookup_SessionEvents_v1.md)
- [Challenges](../../game-features/Wardogs_Challenges_v1.md)
- [Rewards (buildables)](../../game-features/Wardogs_GameFeatures_Rewards_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Zone rewards data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-rewards.json)
- [Economy data: role unlock tree and mastery](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
