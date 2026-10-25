---
title: "Penetration and Ricochet"
parent: "Game Mechanics"
description: "When a bullet bounces off a surface or passes through it, how ammo type and surface material change the chance, and what is still unknown."
---

# Penetration and Ricochet

| Penetration and ricochet | |
|---|---|
| Ricochet chance | 0% to 80%, set by the surface material |
| Flesh | Bodies and heads never ricochet |
| Best penetrating ammo | Armor-piercing (penetration 1.8) |
| Worst penetrating ammo | Hollow point (penetration 0.1) |
{: .wiki-infobox }

A bullet that hits a surface that is not flesh can do one of three things: stop, bounce off (ricochet) or pass through and keep going. Which one happens depends on the surface material, the angle of the hit, and the ammo in the weapon. This article explains the rules. It does not give a result for any particular wall, because the data does not list the materials of the world's walls and props.

## Overview

Most bullets stop at the first solid surface, and that surface absorbs the bullet. Some surfaces send a bullet back out at a new angle. A few materials are thin or weak enough for a bullet to pass through, and then the bullet keeps going with less speed. A bullet that passes through does less damage at its next hit, because it has slowed down.

## How it works

- **Ricochet.** When a bullet hits a surface, the game rolls a chance to bounce. The chance depends on the surface material (see the table below) and on the angle of the hit. Measured from the surface's normal (the line straight out of it), a head-on hit's chance is multiplied by 0.08, and a hit at 80 to 90 degrees, almost flat along the surface, by 0.92. A bullet that has slowed below a tenth of its launch speed cannot bounce. The data indicates that ricochet is checked first, so a bullet that bounces does not also pass through (not fully verified).
- **Penetration.** A bullet can pass through a surface only if it has enough energy left for that thickness. A steeper angle makes the surface look thicker, which makes passing harder. Armor-piercing rounds have the most penetration, and hollow points have very little.
- **Speed after passing.** A bullet that passes through leaves slower. How much slower depends on the surface and the ammo.
- **Damage at the next hit.** A bullet that has slowed does less damage when it hits something next, in proportion to the speed it has left.
- **Flesh.** Body and head surfaces have no ricochet, so a bullet that hits a person does not bounce off them.

## How a ricochet leaves

A bounce is not a mirror reflection. The game picks the new direction at random, and for nearly every bounce the bullet leaves steeper than a mirror would send it, so it rises away from the surface more sharply (derived from the game's code).

- **Random cone.** The new direction is picked at random within a cone of up to 40 degrees around the surface normal. Two bullets that hit the same spot can leave at different angles.
- **Steeper than a mirror.** The sideways part of the bullet's speed is kept. The part that was driving it into the surface is turned around and multiplied by one plus a random factor. That factor is drawn between 0.2 and 10, with an average of about 5, for almost every bounce. A factor above 1 leaves steeper than a mirror, so most bounces do. About 1 bounce in 12 draws a factor under 1 and leaves lower than a mirror (derived, assuming the draws are spread evenly across the range).
- **Speed after the bounce.** The bullet's speed is set back to what it was before the hit, then multiplied by a random factor that depends on the surface. Each material has its own range for this. The ranges are in the data pipeline and are not listed here.

## Numbers

Ammo penetration, from the ammo data:

| Ammo | Penetration | Exit-speed setting |
|---|---:|---:|
| Full metal jacket | 1.0 | Normal |
| Tracer | 1.0 | Low |
| Hollow point | 0.1 | 0.15 |
| Hollow point tracer | 0.1 | 0.15 |
| Armor-piercing | 1.8 | 0 |
| Armor-piercing tracer | 1.76 | 0 |

The exit-speed setting controls how much speed a bullet keeps when it comes out the far side. Only penetration uses it. The effective-range multiplier for each ammo type (hollow point 0.8, armor-piercing 1.2) only moves the distance at which wind starts to act on the bullet. It does not change the bullet's speed or its penetration. See [Ballistics](ballistics.md).

Ricochet chance by surface material (named surfaces in the data; unnamed surface types are left out):

| Surface | Ricochet chance |
|---|---:|
| Ice | 80% |
| Marble | 65% |
| Limestone | 60% |
| Ceramic | 55% |
| Rock | 50% |
| Metal | 45% |
| Gravel | 45% |
| Debris | 40% |
| Rubber | 40% |
| Plastic | 40% |
| Concrete | 35% |
| Default (unspecified surface) | 30% |
| Wood | 30% |
| Brick | 25% |
| Plaster | 20% |
| Soil | 12% |
| Mirror | 15% |
| Glass | 10% |
| Bulletproof glass | 10% |
| Grass | 10% |
| Snow | 3% |
| Sand, fabric, paper | 2% |
| Body, head, water, lava, leaves | 0% |

## Tips that follow from the numbers

- **Armor-piercing is the choice for passing through cover.** At 1.8 penetration it passes through surfaces that stop full metal jacket. Hollow point almost never passes through anything at 0.1.
- **Ice is the most bouncy surface.** An 80% chance means a bullet hitting ice usually bounces, so shooting at ice is unreliable.
- **Glass rarely bounces bullets.** A 10% ricochet chance means most bullets do not bounce off glass.
- **Angle matters.** A bullet that strikes a surface at a shallow angle has to pass through more material, so it is less likely to get through.

## What is not yet known

- The materials and thicknesses of world walls, doors and props. The data has no material assigned to most world meshes, so no result can be given for a specific wall.
- The unit of surface thickness.
- The speed ranges kept after a bounce for each material, which are in the data pipeline but not listed here.
- Whether a bullet with penetration 2 or more can ever ricochet. The data suggests not, but this has not been checked.

## See also

- [Ballistics](ballistics.md)
- [Health and Damage](health-and-damage.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Hit Registration](hit-registration.md)
- [Ammunition](../weapons/ammunition.md)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md) (ricochet and penetration)
- [Weapon penetration (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-penetration.json)
- [Hit Registration](../../pipelines/Wardogs_HitRegistration_v1.md)
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): the exit-speed setting and the effective-range multiplier
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the direction of a ricochet, the angle factor and the speed kept after a bounce
- [Round 45 wiki evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-a.md): the range multipliers (wind start only) and the exit-speed multiplier (penetration only)
