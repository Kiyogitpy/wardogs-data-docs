---
title: "Ballistics"
parent: "Game Mechanics"
description: "How bullets travel, how gravity and drag bend their path, and how damage falls off with distance for each weapon."
---

# Ballistics

| Ballistics | |
|---|---|
| Gravity | 9.8 m/s² downward |
| Drag | Yes, modeled for every bullet |
| Muzzle speed range | 253 m/s (M1911) to 975 m/s (Scout Rifle TD) |
| Damage falloff | Set by each weapon's distance curve and by the bullet's slowing |
{: .wiki-infobox }

Bullets in Wardogs are not instant. Each one travels through the world at its own speed, drops under gravity and slows down in the air. Those three things decide where a shot lands and how hard it hits at range. This article covers the flight. [Health and Damage](health-and-damage.md) covers what happens on impact.

## Overview

A bullet leaves the muzzle at the weapon's muzzle speed. From then on, gravity pulls it down and drag slows it. A bullet that has slowed too much does less damage when it hits. Most weapons also lose damage with distance on a set curve, so a rifle that does full damage at close range can do much less at 1,000 m.

## How it works

- **Muzzle speed.** Every weapon fires its bullet at a fixed speed. Heavier sniper rounds and rifle rounds are fast; pistol and the Judge shotgun are slower.
- **Gravity.** Bullets fall at 9.8 m/s², the game's world gravity.
- **Lifetime.** A bullet is removed 10 s after it is fired. Artillery shells last longer, up to 40 s (see [Artillery](artillery.md)).
- **Flight steps.** The game moves a bullet in steps of 33 ms (about 30 a second) and checks its path at each step.
- **Drag.** Air slows bullets. How much depends on the bullet's shape, weight and size, so the same muzzle speed does not mean the same range for every round.
- **Damage falloff.** Each weapon has a distance curve. Damage stays at full up to a set distance and then drops; on many rifles the curve reaches 20% of full damage at 1,200 m. Separately, once a bullet has slowed below a reference speed, its damage is also scaled down (see Speed scale below). Both effects multiply together, which is why the table drops further than the curve alone.
- **Effective range.** Each weapon's data lists an effective range (see the table below). The game multiplies it by 100 when it sets up each shot, then scales it by 1.2 for armor-piercing ammo and 0.8 for hollow point. The only use found so far is as the distance over which the wind effect on the bullet's flight builds up, which is an inference from reading the code; it was not seen in play. It is not a damage cutoff: damage falloff comes from the weapon's own curve, not from the effective range.

## Numbers

Muzzle speed and listed effective range, from the weapon data:

| Weapon | Muzzle speed | Effective range |
|---|---:|---:|
| M4 | 910 m/s | 500 m |
| AK74 | 880 m/s | 500 m |
| FAL | 840 m/s | 800 m |
| SVD | 800 m/s | 800 m |
| MK22 | 894 m/s | 1,000 m |
| AMR 50 | 900 m/s | 2,000 m |
| MP5 | 400 m/s | 200 m |
| GGX 17 | 375 m/s | 50 m |
| Super-45 | 375 m/s | 50 m |
| Deagle | 470 m/s | 100 m (game default) |
| Judge | 335 m/s | 50 m |

Upper-torso damage per hit with full metal jacket ammo and no armor, at set distances. These include the distance curve and the slowing:

| Weapon | 0 m | 50 m | 100 m | 200 m | 400 m | 600 m | 800 m | 1,200 m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| M4 | 27.3 | 27.3 | 27.3 | 27.3 | 27.3 | 20.6 | 12.6 | 3.1 |
| AK74 | 25.3 | 25.3 | 25.3 | 25.3 | 25.3 | 21.3 | 13.6 | 3.1 |
| FAL | 32.9 | 32.9 | 32.9 | 32.9 | 32.9 | 32.9 | 31.5 | 4.5 |
| SVD | 41.4 | 41.4 | 41.4 | 41.4 | 41.4 | 41.4 | 41.4 | 7.5 |
| MK22 | 118.8 | 118.8 | 118.8 | 118.8 | 118.8 | 118.8 | 118.8 | 82.3 |
| AMR 50 | 207.9 | 207.9 | 207.9 | 207.9 | 207.9 | 207.9 | 207.9 | 207.9 |
| Deagle | 72.8 | 72.8 | 70.7 | 56.2 | 39.8 | 29.3 | 20.5 | 6.9 |
| Judge | 52.0 | 52.0 | 48.7 | 42.3 | 32.8 | 25.4 | 19.5 | 11.3 |
| GGX 17 | 25.4 | 25.4 | 23.3 | 18.5 | 12.0 | 7.6 | 4.6 | 1.3 |
| MP5 | 25.4 | 25.4 | 25.4 | 22.3 | 7.4 | 2.9 | 1.2 | 0.5 |
| Super-45 | 34.7 | 34.7 | 12.8 | 8.2 | 6.1 | 4.6 | 3.4 | 1.8 |

The AMR 50 and MK22 keep most of their damage at long range, while the MP5 and Super-45 lose most of theirs within a few hundred metres.

**Drop, estimated.** Ignoring drag, a bullet at 880 m/s falls about 6 cm at 100 m, about 25 cm at 200 m and about 1.6 m at 500 m. Drag makes the real drop larger than these figures. They are simple estimates from the gravity and muzzle speed in the data, not measured in-game values.

### Speed scale

Once a bullet is slower than the reference speed for its weapon, its damage is scaled by how much speed it has left. The scale is the bullet's speed divided by that reference, capped at 1, so full speed means no change. The figures below come from the game's drag model: the bullet is flown with the game's drag, and the speed is read at each distance. They are computed, not measured in game. Launchers, bows and vehicle guns are not in this model.

| Weapon | 100 m | 200 m | 400 m | 600 m |
|---|---:|---:|---:|---:|
| GGX 17 | 0.94 | 0.80 | 0.60 | 0.45 |
| AMP-9 | 1.00 | 0.88 | 0.66 | 0.50 |
| Super-45 | 0.92 | 0.80 | 0.64 | 0.52 |
| Judge | 0.94 | 0.81 | 0.63 | 0.49 |
| A-91 | 1.00 | 1.00 | 0.91 | 0.72 |
| AK74 | 1.00 | 1.00 | 1.00 | 0.95 |
| M4 | 1.00 | 1.00 | 1.00 | 0.85 |
| MK22 | 1.00 | 1.00 | 1.00 | 1.00 |

The M4 keeps full speed to 400 m. The GGX 17 is already at 0.80 by 200 m and 0.45 by 600 m, so pistols lose damage to speed as well as to distance.

## Tips that follow from the numbers

- **Range is different for every weapon.** The MP5 does 25.4 at 100 m and 7.4 at 400 m, so it is a close-range weapon. The FAL still does 32.9 at 600 m.
- **Sniper rifles hit hard at any distance.** The MK22 does 118.8 to the upper torso at 800 m. The AMR 50 does 207.9 at any distance in the table.
- **Drop grows quickly at long range.** Even without drag, a bullet from an M4-class rifle falls about 1.6 m by 500 m. The data does not say how sights are set for a given range, so the sight setting for long shots is not yet known.
- **Pistols lose damage quickly.** The GGX 17 falls from 25.4 at 50 m to 12.0 at 400 m.

## See also

- [Health and Damage](health-and-damage.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Spread and Recoil](spread-and-recoil.md)
- [Hit Registration](hit-registration.md)
- [Ammunition](../weapons/ammunition.md)
- [Weapons](../weapons.md)

## Sources

- [Projectile flight: drag and gravity](../../pipelines/Wardogs_ProjectileFlight_v1.md)
- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md) (damage over distance)
- [Weapon damage falloff (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md)
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): bullet lifetime, effective range use, flight step, and the hit record
- [Round 40 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-weapons.md): the 33 ms flight step re-check
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the speed scale after drag, computed by [weapon_speed_scale.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/weapon_speed_scale.py)
