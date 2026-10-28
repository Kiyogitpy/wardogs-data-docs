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

A bullet that hits a surface that is not flesh can do one of three things: stop, bounce off (ricochet) or pass through and keep going. Which one happens depends on the surface material, the angle of the hit, and the ammo in the weapon. This article explains the rules. It does not give a result for any particular wall, because the materials of the world's walls and props are not known.

## Overview

Most bullets stop at the first solid surface, and that surface absorbs the bullet. Some surfaces send a bullet back out at a new angle. A few materials are thin or weak enough for a bullet to pass through, and then the bullet keeps going with less speed. A bullet that passes through does less damage at its next hit, because it has slowed down.

## How it works

- **Ricochet.** When a bullet hits a surface, the game rolls a chance to bounce. The chance depends on the surface material (see the table below) and on the angle of the hit. Measured from the surface's normal (the line straight out of it), a head-on hit's chance is multiplied by 0.08, and a hit at 80 to 90 degrees, almost flat along the surface, by 0.92. A bullet that has slowed below a tenth of its launch speed cannot bounce. A bullet that can get through the surface easily also bounces less. The chance is cut by how much the bullet's ability to pass the surface exceeds the surface thickness: equal or less keeps the full chance, twice the thickness or more never bounces, and in between the chance is scaled down (derived from the game's code; the game was not run). So a round strong enough to pass through a thin surface by a margin of two will not ricochet off it. The game indicates that ricochet is checked first, so a bullet that bounces does not also pass through (not fully verified).
- **Penetration.** A bullet can pass through a surface only if it has enough energy left for that thickness. A steeper angle makes the surface look thicker, which makes passing harder. Armor-piercing rounds have the most penetration, and hollow points have very little.
- **Thickness.** Thickness is measured in the game's world units, which are centimetres (inferred from the engine). When a bullet hits a solid object, the game fires a short check straight on through it to find where the bullet would come out, and the distance in between is the thickness. If it finds no exit within about 2 m, the bullet cannot pass. Thin sheet surfaces such as glass use a stored thickness instead, multiplied by 10.
- **Wall materials.** The material comes from the surface paint (the material applied to the wall mesh), not from the mesh itself. About 1,800 of the 3,150 material sets in the game name one of the physical materials in the table below, and the rest take it from a parent material. Of the 63 wall material sets, 40 are concrete, 10 brick, 4 metal, 1 wood and 1 plaster, and 7 inherit theirs. Across the 256 building material sets, 71 are concrete, 53 metal, 18 brick, 16 wood and 11 plaster.
- **Density.** Each physical material has a density number, and the denser of the two sides a bullet crosses counts. A higher density makes the surface harder to pass.
- **Speed after passing.** A bullet that passes through leaves slower. How much slower depends on the surface and the ammo.
- **Damage at the next hit.** A bullet that has slowed does less damage when it hits something next, in proportion to the speed it has left.
- **Flesh.** Body and head surfaces have no ricochet, so a bullet that hits a person does not bounce off them.

## How a ricochet leaves

A bounce is not a mirror reflection. The game picks the new direction at random, and for nearly every bounce the bullet leaves steeper than a mirror would send it, so it rises away from the surface more sharply (derived from the game's code).

- **Random cone.** The new direction is picked at random within a cone of up to 40 degrees around the surface normal. Two bullets that hit the same spot can leave at different angles.
- **Steeper than a mirror.** The sideways part of the bullet's speed is kept. The part that was driving it into the surface is turned around and multiplied by one plus a random factor. That factor is drawn between 0.2 and 10, with an average of about 5, for almost every bounce. A factor above 1 leaves steeper than a mirror, so most bounces do. About 1 bounce in 12 draws a factor under 1 and leaves lower than a mirror (derived, assuming the draws are spread evenly across the range).
- **Speed after the bounce.** The bullet's speed is set back to what it was before the hit, then multiplied by a random factor that depends on the surface. Each material has its own range for this, listed in the last column of the table below. A bounce off ice keeps 50% to 85% of the speed; a bounce off most soft ground keeps 15% or less.

## Numbers

Ammo penetration, by ammo type:

| Ammo | Penetration | Exit-speed setting |
|---|---:|---:|
| Full metal jacket | 1.0 | Normal |
| Tracer | 1.0 | Low |
| Hollow point | 0.1 | 0.15 |
| Hollow point tracer | 0.1 | 0.15 |
| Armor-piercing | 1.8 | 0 |
| Armor-piercing tracer | 1.76 | 0 |

The exit-speed setting controls how much speed a bullet keeps when it comes out the far side. Only penetration uses it. The effective-range multiplier for each ammo type (hollow point 0.8, armor-piercing 1.2) only moves the distance at which wind starts to act on the bullet. It does not change the bullet's speed or its penetration. See [Ballistics](ballistics.md).

Ricochet chance by surface material (only named surfaces are listed; unnamed surface types are left out):

| Surface | Ricochet chance | Speed kept after a bounce |
|---|---:|---:|
| Ice | 80% | 50% to 85% |
| Marble | 65% | 35% to 60% |
| Limestone | 60% | 25% to 50% |
| Ceramic | 55% | 20% to 40% |
| Rock | 50% | 35% to 55% |
| Metal | 45% | 35% to 65% |
| Gravel | 45% | 15% to 35% |
| Debris | 40% | 15% to 50% |
| Rubber | 40% | 10% to 25% |
| Plastic | 40% | 20% to 45% |
| Concrete | 35% | 25% to 50% |
| Default (unspecified surface) | 30% | 25% to 45% |
| Wood | 30% | 15% to 35% |
| Brick | 25% | 15% to 35% |
| Plaster | 20% | 15% to 35% |
| Soil | 12% | 8% to 20% |
| Mirror | 15% | 10% to 25% |
| Glass | 10% | 15% to 40% |
| Bulletproof glass | 10% | 15% to 40% |
| Grass | 10% | 5% to 15% |
| Snow | 3% | 3% to 10% |
| Sand, fabric, paper | 2% | 3% to 10% (sand), 10% to 15% (fabric), 10% to 15% (paper) |
| Body, head, water, lava, leaves | 0% | Not applicable |

Density by physical material (higher is harder to pass; a surface with no density set uses 1.0, inferred):

| Material | Density |
|---|---:|
| Concrete | 8.5 |
| Metal (plain, solid) | 7.0 |
| Metal sheet | 7.85 |
| Corrugated metal | 6.0 |
| Brick | 5.2 |
| Ceramic | 4.5 |
| Plaster | 3.0 |
| Rock | 3.0 |
| Wood | 2.56 |
| Fabric | 1.5 |
| Plastic | 1.3 |
| Weak metal | 2.0 |
| Rubber | 0.7 |
| Paper | 0.85 |

## Tips that follow from the numbers

- **Armor-piercing is the choice for passing through cover.** At 1.8 penetration it passes through surfaces that stop full metal jacket. Hollow point almost never passes through anything at 0.1.
- **Ice is the most bouncy surface.** An 80% chance means a bullet hitting ice usually bounces, so shooting at ice is unreliable.
- **Glass rarely bounces bullets.** A 10% ricochet chance means most bullets do not bounce off glass.
- **Angle matters.** A bullet that strikes a surface at a shallow angle has to pass through more material, so it is less likely to get through.

## What is not yet known

- The thickness and material of one particular wall, door or prop on a map. Thickness is measured live from the shape of the object when you shoot it, so no result can be given for a specific wall. The map files were read for which materials the placed walls and buildings use, and the totals for each map are in its article: [Bakurani](../game-modes-and-maps/bakurani.md#cover-materials), [Ozeti](../game-modes-and-maps/ozeti.md#cover-materials), [Zestafona](../game-modes-and-maps/zestafona.md#cover-materials) and [Saburtulo](../game-modes-and-maps/saburtulo.md#cover-materials).

## See also

- [Ballistics](ballistics.md)
- [Health and Damage](health-and-damage.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Hit Registration](hit-registration.md)
- [Ammunition](../ammunition.md)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md) (ricochet and penetration)
- [Weapon penetration (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-penetration.json)
- [Hit Registration](../../pipelines/Wardogs_HitRegistration_v1.md)
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): the exit-speed setting and the effective-range multiplier
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the direction of a ricochet, the angle factor and the speed kept after a bounce
- [Round 45 wiki evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-a.md): the range multipliers (wind start only) and the exit-speed multiplier (penetration only)
