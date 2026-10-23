---
title: "Downed and Revive"
parent: "Game Mechanics"
description: "What happens when health reaches zero, how long a downed player has before bleeding out, how teammates revive them, and how healing items work."
---

# Downed and Revive

| Downed and revive | |
|---|---|
| Downed at | 0 HP |
| Bleed-out timer | 360 s, draining at half speed (about 12 minutes) |
| Timer after a revive | At least 30 s |
| Revive by hand | 20 s hold |
| Defibrillator revive | Restores 35 HP |
| Medical Bag revive | Restores 50 HP |
| Natural regeneration | None found in the data |
{: .wiki-infobox }

When a player's health reaches zero, they are not dead yet. They are downed, and they have a limited time before bleeding out. In that time a teammate can revive them, or they can give up. This article explains the downed state and the items that heal and revive. [Health and Damage](health-and-damage.md) explains how the health was lost in the first place.

## Overview

A downed player is on the ground and cannot fight. Health does not drop any further while they bleed out, so the bleed-out timer is the only clock. If nobody revives them before the timer runs out, they bleed out and respawn at Headquarters. The tutorial text describes this as the critical state.

## How it works

- **Going down.** At 0 HP the player enters the critical state.
- **Bleed-out timer.** The timer starts at 360 seconds. In the normal downed state it drains at half speed, so a player lasts about 720 seconds (12 minutes) unless helped.
- **Giving up.** A downed player can choose to give up. The timer then drains at 240 per second instead of 0.5, so giving up ends the wait in 1.5 s.
- **Being dragged.** A teammate can drag a downed player. Drag speed can be raised with a Medic skill.
- **Reviving by hand.** A teammate holds the revive for 20 seconds with no equipment. The health the revived player comes back with is not yet known.
- **Reviving with a defibrillator.** A defibrillator revives the player instantly to 35 HP. It needs a battery and a 4 s charge. The user cannot use it while downed.
- **Reviving with a Medical Bag.** A teammate can revive a player with a Medical Bag, restoring 50 HP and costing 10 durability.
- **Reviving with a resuscitator.** Resuscitators revive faster than bare hands. Each one is a single use. The health they restore is not yet known.
- **Revived again.** A player who is revived and then goes down again gets a bleed-out timer of at least 30 s. At half drain speed that is about 60 seconds.
- **Revive boost.** After a Medic reviews a teammate, both can get a short sprint speed boost for 5 seconds (see the skills table below).

Health comes back from items, not on its own. The data shows no natural regeneration over time for infantry.

## Numbers

Healing items:

| Item | Effect | Time | Notes |
|---|---|---|---|
| Bandage | +35 HP | 5.2 s on yourself, 4.8 s on a teammate | Stack of 5 |
| Individual First Aid Kit | +100 HP | 5.2 s (heal lands at 4.7 s) | Single item |
| Medical Bag, yourself | 35 HP over 5 s | 7 HP per second | Costs 25 durability per use from 150 |
| Medical Bag, teammate | 15 HP over 1.5 s | 10 HP per second | Costs 2 durability per use |
| Enox | +40 HP as decaying health | 2.2 s | Pool of 40; the decay rate is not confirmed |
| Adrenaline Pen | No healing; unlimited tactical sprint for 60 s | 2 s on yourself, 1.3 s on a teammate | Stack of 3 |

Using any of the healing items also halves your movement speed while you use it.

Medic skills that change these numbers, where the data gives a value:

| Skill | Effect |
|---|---|
| Medical item switch speed | Switching to medical items gets faster: speed rises to 1.2 times at level 2 and 1.4 times at level 4 |
| Medkits have more uses | Medkit usage cost falls: 0.8 at level 2, 0.7 at level 3, 0.6 at level 4 |
| Sprint boost after reviving (you) | Sprint and tactical sprint speed rise to 1.2 or 1.4 times for 5 s |
| Sprint boost after reviving (teammate) | The revived teammate gets the same boost for 5 s |

The other Medic skills have names and descriptions in the data, but the size of their effect is not yet known.

## Tips that follow from the numbers

- **Heal in a safe spot.** A bandage takes about 5 seconds, and the Medical Bag's healing stops if you move away.
- **Bring a Medical Bag for teammates.** It heals a teammate at 10 HP per second, which is faster than it heals you (7 HP per second).
- **Use the First Aid Kit for a big heal.** It restores 100 HP in one use, so it is the fastest way to get a badly hurt player back to full.
- **A downed player has time.** With 12 minutes on the normal timer, there is usually time for a revive if teammates act quickly. Giving up is only worth choosing when no help is coming.
- **Plan for a second downing.** A player revived once gets a shorter timer if they go down again: at least 30 s, which is about 60 seconds of real time.

## Not yet known

- The health a bare-hands revive restores.
- The health a resuscitator restores, and how long a resuscitator revive takes.
- Whether natural regeneration exists for infantry. The data shows a 10-second delay before regeneration would start, but no healing over time.
- The exact decay rate of Enox's extra health.
- What the Medic skills for bleed-out time and heal speed change in play.

## See also

- [Health and Damage](health-and-damage.md)
- [Movement](movement.md)
- [Beginner's Guide](../guides/beginners-guide.md)
- [Medical Items](../equipment/medical-items.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md)
- [Character health rules](../../pipelines/Wardogs_DamagePipeline_v2.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md) (item names and costs)
