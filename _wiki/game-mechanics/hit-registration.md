---
title: "Hit Registration"
parent: "Game Mechanics"
description: "The plain-language rules for when a bullet counts as a hit, which body part it hits, and how friendly fire is handled."
---

# Hit Registration

| Hit registration | |
|---|---|
| Bullet type | Travelling projectile for most ammunition; some shots are hit-scan |
| Stops at | The first surface or player in its path, unless it passes through or bounces |
| Friendly fire | Half damage to players of your own faction and to yourself |
| Shotgun | 8 pellets per shell, each a separate hit |
{: .wiki-infobox }

This article explains, in plain terms, when a bullet counts as a hit and what the game does with it. For the numbers, see [Health and Damage](health-and-damage.md). For how bullets travel, see [Ballistics](ballistics.md).

## Overview

In Wardogs, most bullets are moving objects, not instant lines from the gun to the target. Each bullet travels, and at every step the game checks what lies on its path. The first thing that stops it, or that it passes through, decides what happens. That is how a bullet can hit a wall, bounce, pass through a thin surface or hit a player.

## How it works

- **Path.** A bullet is checked along its path at each step of its flight. If something solid is in the way, the bullet hits it.
- **Hit-scan shots.** A shot counts as hit-scan, meaning it is not a travelling bullet, when its ammunition is not a self-moving projectile. The condition comes from a stats flag that the projectile code reads. Which ammunition has that flag off is not listed here (a static reading of the game code, not checked in play).
- **Surfaces.** A hit on a surface can stop the bullet, bounce it off (ricochet) or let it pass through. The surface material decides the chance. See [Penetration and Ricochet](penetration-and-ricochet.md).
- **Players.** A bullet that reaches a player is checked against every body part its path passes through. A character has 20 collision bodies, and one bullet can cross several of them. The game works out the damage for each part crossed, and the highest result counts. Which part that is decides the damage (see [Health and Damage](health-and-damage.md)).
- **Limbs.** Calves, forearms and thighs are checked as plain capsules: a straight shape whose radius is the average of its two ends, not a tapered shape (a static reading of the game code, not checked in play).
- **One hit per target.** A bullet does not hit the same target twice. It keeps a list of the actors it has already hit and skips them. The game shows no way to turn this off (a static reading of the game code, not checked in play).
- **Your own vehicle.** A shot fired from a vehicle seat can be set to ignore that vehicle, so the bullet passes it. This is a plain on or off setting for the projectile, not a timer. There is no time limit for it. The setting belongs to the ammunition type, not to the weapon: 20 of the 36 projectile types have it on (vehicle cannons and autocannons, rockets, shells, the Stingray drone, the explosive arrow and the TV-guided missile) and the rest have it off, including the ordinary rifle, pistol, shotgun and .50 caliber rounds.
- **Friendly fire.** Bullets that hit a player of your own faction still count as hits, but they do half the damage. Nothing in the game stops the bullet from hitting that player. Two players are of the same faction when they carry the same faction tag. Two players with no faction at all also match (derived from the code, not seen in play).
- **Impact effects.** Each hit shows an impact effect on the surface it struck. These do not change the damage.
- **Artillery shells.** The 155 mm shells are checked against a box 61.2 cm long and 11 cm across, not a point (derived from the shell's box size).
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

- How the game settles a hit when the shooter and target see it differently, such as with slow connections. That is decided on the game servers, which are not part of the game, so it cannot be read from the game itself.
- Whether a vehicle-mounted machine gun that fires an ordinary rifle or .50 caliber round passes through its own vehicle. Those rounds have the setting off, so it most likely does not (inferred; the game was not run).

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
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): limb shapes, the one-hit list and the hit-scan flag
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the hit-scan setting and the fire and hit paths
