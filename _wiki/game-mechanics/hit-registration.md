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
| Friendly fire | Half damage to teammates and to yourself |
| Shotgun | 8 pellets per shell, each a separate hit |
{: .wiki-infobox }

This article explains, in plain terms, when a bullet counts as a hit and what the game does with it. For the numbers, see [Health and Damage](health-and-damage.md). For how bullets travel, see [Ballistics](ballistics.md).

## Overview

In Wardogs, a bullet is a moving object, not an instant line from the gun to the target. Each bullet travels, and at every step the game checks what lies on its path. The first thing that stops it, or that it passes through, decides what happens. That is how a bullet can hit a wall, bounce, pass through a thin surface or hit a player.

## How it works

- **Path.** A bullet is checked along its path at each step of its flight. If something solid is in the way, the bullet hits it.
- **Surfaces.** A hit on a surface can stop the bullet, bounce it off (ricochet) or let it pass through. The surface material decides the chance. See [Penetration and Ricochet](penetration-and-ricochet.md).
- **Players.** A bullet that reaches a player counts as a hit on the body part it struck. Which part that is decides the damage (see [Health and Damage](health-and-damage.md)).
- **Your own vehicle.** A shot fired from a vehicle is not stopped by that vehicle for a short time after you fire. The length of that time is not yet known.
- **Friendly fire.** Bullets that hit a teammate, or the shooter, still count as hits, but they do half the damage. Nothing in the game stops the bullet from hitting a teammate.
- **Impact effects.** Each hit shows an impact effect on the surface it struck. These do not change the damage.
- **Shotgun pellets.** Each pellet is a separate hit. A pellet that misses does no damage, and each one that hits does its own damage.

## Numbers

Bullet and hit values that matter in play:

| Value | Figure |
|---|---|
| Bullets that bounce off flesh | 0% (bodies and heads never ricochet) |
| Friendly-fire damage | 50% of normal |
| Shotgun pellets per buckshot shell | 8 |
| Hits a single bullet's history can record | 33 (what happens after that is not yet known) |

## Tips that follow from the rules

- **Watch the path, not just the target.** A bullet hits the first thing in its path, so cover between you and the target blocks the shot even when the target is visible.
- **Shotguns need to hit with several pellets.** Each pellet is a separate hit, so a close shot with most pellets landing does far more damage than one that catches a few.
- **Teammates still get hurt.** Friendly fire halves the damage, but it does not disappear, so careless shots still cost health.

## What is not yet known

- How the game settles a hit when the shooter and target see it differently, such as with slow connections. The data does not show this.
- The length of time a vehicle's own shots are ignored by that vehicle.
- What happens to a bullet after its 33rd recorded hit.

## See also

- [Ballistics](ballistics.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Health and Damage](health-and-damage.md)
- [Spread and Recoil](spread-and-recoil.md)

## Sources

- [Hit Registration](../../pipelines/Wardogs_HitRegistration_v1.md)
- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (friendly fire)
