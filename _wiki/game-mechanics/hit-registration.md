---
title: "Hit Registration"
parent: "Game Mechanics"
description: "The plain-language rules for when a bullet counts as a hit, which body part it hits, and how friendly fire is handled."
---

# Hit Registration

| Hit registration | |
|---|---|
| Bullet type | Travelling projectile, not an instant hit |
| Stops at | The first surface or player in its path, unless it passes through or bounces |
| Friendly fire | Half damage to players of your own faction and to yourself |
| Shotgun | 8 pellets per shell, each a separate hit |
{: .wiki-infobox }

This article explains, in plain terms, when a bullet counts as a hit and what the game does with it. For the numbers, see [Health and Damage](health-and-damage.md). For how bullets travel, see [Ballistics](ballistics.md).

## Overview

In Wardogs, a bullet is a moving object, not an instant line from the gun to the target. Each bullet travels, and at every step the game checks what lies on its path. The first thing that stops it, or that it passes through, decides what happens. That is how a bullet can hit a wall, bounce, pass through a thin surface or hit a player.

## How it works

- **Path.** A bullet is checked along its path at each step of its flight. If something solid is in the way, the bullet hits it.
- **Surfaces.** A hit on a surface can stop the bullet, bounce it off (ricochet) or let it pass through. The surface material decides the chance. See [Penetration and Ricochet](penetration-and-ricochet.md).
- **Players.** A bullet that reaches a player is checked against every body part its path passes through. A character has 20 collision bodies, and one bullet can cross several of them. The game works out the damage for each part crossed, and the highest result counts. Which part that is decides the damage (see [Health and Damage](health-and-damage.md)).
- **Your own vehicle.** A shot fired from a vehicle seat can be set to ignore that vehicle, so the bullet passes it. This is a plain on or off setting for the projectile, not a timer. The data has no time limit for it.
- **Friendly fire.** Bullets that hit a player of your own faction still count as hits, but they do half the damage. Nothing in the game stops the bullet from hitting that player. Two players are of the same faction when they carry the same faction tag. Two players with no faction at all also match (derived from the code, not seen in play).
- **Impact effects.** Each hit shows an impact effect on the surface it struck. These do not change the damage.
- **Artillery shells.** The 155 mm shells are checked against a box 61.2 cm long and 11 cm across, not a point (derived from the box size in the shell data).
- **Shotgun pellets.** Each pellet is a separate hit. A pellet that misses does no damage, and each one that hits does its own damage.

## Numbers

Bullet and hit values that matter in play:

| Value | Figure |
|---|---|
| Bullets that bounce off flesh | 0% (bodies and heads never ricochet) |
| Friendly-fire damage | 50% of normal |
| Shotgun pellets per buckshot shell | 8 |
| Hits a bullet's record holds | The first 16. Hits 17 to 32 are not recorded, and the record starts again at hit 33 |
| 155 mm artillery shell hit box | 61.2 cm long, 11 cm across (derived) |
| Cap on the number of hits a bullet can make | None found |

## Tips that follow from the rules

- **Watch the path, not just the target.** A bullet hits the first thing in its path, so cover between you and the target blocks the shot even when the target is visible.
- **Shotguns need to hit with several pellets.** Each pellet is a separate hit, so a close shot with most pellets landing does far more damage than one that catches a few.
- **Teammates still get hurt.** Friendly fire halves the damage, but it does not disappear, so careless shots still cost health.

## What is not yet known

- How the game settles a hit when the shooter and target see it differently, such as with slow connections. The data does not show this.
- Whether the own-vehicle setting applies to every projectile fired from a vehicle. It was not checked weapon by weapon.

## See also

- [Ballistics](ballistics.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Health and Damage](health-and-damage.md)
- [Spread and Recoil](spread-and-recoil.md)

## Sources

- [Hit Registration](../../pipelines/Wardogs_HitRegistration_v1.md)
- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (friendly fire)
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): hit record of 16 slots and the hit limit
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): body parts crossed, the faction rule, the own-vehicle setting and the artillery shell box
