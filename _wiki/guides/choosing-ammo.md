---
title: "Choosing Ammo"
parent: "Guides"
description: "When armor-piercing ammo beats full metal jacket, when hollow point is worth it, and which round to load against each armor class."
---

# Choosing Ammo

This guide works out which ammo does the most damage against each kind of armor. The comparisons use the current saved-input damage model (historical formula, hostile point-blank hits outside vehicles, no penetration or ricochet); S3 native equivalence is unverified. Its inputs come from the damage tables for the M4 rifle and the GGX 17 pistol, which cover the three main rounds: full metal jacket (FMJ), hollow point (HP) and armor-piercing (AP). Tracer rounds do the same damage as the plain round of the same type.

## The short answer

- **No armor:** hollow point does the most damage, about twice the full metal jacket.
- **Light armor:** full metal jacket is best. Hollow point drops to a fraction of its damage.
- **Medium armor and up:** armor-piercing does more modeled damage than full metal jacket on the listed rifles, except the AMR 50.
- **Helmets:** armor-piercing is the better choice against a Heavy or Super heavy helmet.

## M4 damage by armor

Damage per hit to the upper torso and head in the current saved-input model: hostile, point-blank hits, outside vehicles, without penetration or ricochet. The model uses the historical damage formula; S3 native equivalence has not been established.

| Armor | Full metal jacket | Hollow point | Armor-piercing | Best round |
|---|---:|---:|---:|---|
| No armor, torso | 30.8 | 61.6 | 24.6 | Hollow point |
| No armor, head | 65.8 | 131.6 | 52.6 | Hollow point |
| Light vest | 21.6 | 9.1 | 20.2 | Full metal jacket |
| Medium vest | 18.5 | 6.7 | 18.7 | Armor-piercing (only slightly) |
| Heavy vest | 15.4 | 4.2 | 17.2 | Armor-piercing |
| Super heavy vest | 12.3 | 1.7 | 15.8 | Armor-piercing |
| Light helmet | 46.1 | 13.0 | 43.2 | Full metal jacket |
| Medium helmet | 39.5 | 9.5 | 40.0 | Armor-piercing (only slightly) |
| Heavy helmet | 32.9 | 5.9 | 36.8 | Armor-piercing |
| Super heavy helmet | 26.3 | 2.4 | 33.7 | Armor-piercing |

Against no armor, a single hollow-point headshot from the M4 deals 131.6, which exceeds 100 HP in this model. Downing versus immediate death depends on mode behavior; this calculation does not establish a guaranteed kill.

## GGX 17 damage by armor

The GGX 17 pistol shows the same pattern, at lower damage:

| Armor | Full metal jacket | Hollow point | Armor-piercing | Best round |
|---|---:|---:|---:|---|
| No armor, torso | 25.4 | 50.8 | 20.3 | Hollow point |
| Light vest | 17.8 | 7.5 | 16.1 | Full metal jacket |
| Medium vest | 15.2 | 5.5 | 14.6 | Full metal jacket |
| Heavy vest | 12.7 | 3.4 | 13.2 | Armor-piercing |
| Super heavy vest | 10.2 | 1.4 | 11.8 | Armor-piercing |

## Which calibers switch at which armor

- **Rifle calibers** (5.56 mm, 5.45 mm, 7.62 mm, .308 Win) pass full metal jacket at Medium armor. The FAL does 23.8 with armor-piercing and 22.3 with full metal jacket against a Medium vest.
- **Pistol calibers** (9 mm, .45 ACP, .45 Colt) do not pass full metal jacket at Medium armor. They pass it at Heavy armor. The GGX 17 does 13.2 with armor-piercing and 12.7 with full metal jacket against a Heavy vest.
- **The Deagle** (.50 AE) passes full metal jacket at Medium armor: 46.6 against 43.7.
- **The Judge** does not pass full metal jacket at Medium armor (29.9 against 31.2), but does at Heavy armor (27.0 against 26.0).
- **The .50 cal AMR 50** is the exception. Its arm class gives armor-piercing the same armor effect as full metal jacket, so armor-piercing never beats it. With no armor its hollow point round (listed as Flesh Damage) does 415.8 to the upper torso, the most of the rounds checked, against 207.9 for full metal jacket and 166.3 for armor-piercing.

## Rules to remember

- **Hollow point is for unarmored targets.** Its damage against any armor is far lower than full metal jacket.
- **Armor-piercing loses 20% against bare flesh.** That is why it is weaker than full metal jacket on unarmored targets.
- **Shotguns have no armor-piercing or hollow point rounds.** They fire buckshot and slugs only.
- **Tracers do the same damage as the plain round** of the same type. A tracer is not a damage upgrade.

## Practical picks

| Opponent | Load |
|---|---|
| Unarmored | Hollow point |
| Light armor | Full metal jacket |
| Medium armor | Armor-piercing (listed rifles except AMR 50, and the Deagle); full metal jacket (AMR 50 and other listed pistols) |
| Heavy or Super heavy armor | Armor-piercing, except the AMR 50 (see above) |

For how armor works, see [Armor](../game-mechanics/armor.md). For how far a bullet's damage falls with distance, see [Ballistics](../game-mechanics/ballistics.md).

## See also

- [Armor](../game-mechanics/armor.md)
- [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md)
- [Beginner's Guide](beginners-guide.md)
- [Ammunition](../ammunition.md)
- [Body armor](../equipment/body-armor.md)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md) (ammo comparison and armor tables)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (ammo and armor rules)
- [Weapon damage by location (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json)
