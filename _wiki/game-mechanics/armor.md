---
title: "Armor"
parent: "Game Mechanics"
description: "How vests and helmets reduce bullet damage, which body parts each one covers, and how ammo type changes the protection."
---

# Armor

| Armor | |
|---|---|
| Vests | Light 30%, Medium 40%, Heavy 50%, Super heavy 60% reduction |
| Helmets | Light 30%, Medium 40%, Pilot 30%, Heavy 50%, Super heavy 60%, Tank 55% reduction |
| Covers | Vests: torso. Helmets: head (and neck on the heavier helmets) |
| Ghillie suit | Protection and effective durability unresolved; historical set-effect values |
{: .wiki-infobox }

Armor is worn in two slots: a vest for the body and a helmet for the head. Each piece cuts the damage of a hit to the body parts it covers. The amount of protection depends on the armor class, and the ammo in the weapon changes how much of that protection applies. The full list of armor items is on [Body Armor](../../content/Wardogs_Items_v2.md).

## Overview

The armor classes are Light, Medium, Heavy and Super heavy for vests, and the same four plus Pilot and Tank for helmets. A higher class blocks more damage. Each piece has a durability. A hit takes durability from it, and the piece breaks at 0. The reduction does not fall as the piece wears, because all four durability stages give the same reduction.

## How it works

- A vest covers the upper, middle and lower torso. The Super heavy vest also covers the pelvis and the upper arm.
- A helmet covers the head. The Heavy, Super heavy and Tank helmets also cover the neck.
- A vest and a helmet never cover the same body part, so at any one place only one piece of armor applies.
- The lower arms, hands, thighs, calves and feet are not covered by any armor.
- Armor reduces bullet damage by its percentage. In the point-blank model, a Heavy vest (50%) turns a 30.8 HP upper-torso hit from an M4 into 15.4 HP.
- Ghillie item exports omit durability stages and covered locations but reference effects whose definitions are unavailable. The model assumes no armor; actual S3 protection remains unresolved. Earlier analysis describes a set bonus to aiming and movement (see [Ghillie Body Suit](../equipment/ghillie-body-suit.md)).

## Numbers

Modeled point-blank damage per hit to the upper torso and head, with M4 full-metal-jacket ammunition. These S3 inputs use the historical formula, assuming a hostile target outside a vehicle and no penetration or falloff; current native behavior remains unverified:

| Armor worn | Upper torso | Head |
|---|---:|---:|
| None | 30.8 | 65.8 |
| Light | 21.6 (vest) | 46.1 (helmet) |
| Medium | 18.5 (vest) | 39.5 (helmet) |
| Heavy | 15.4 (vest) | 32.9 (helmet) |
| Super heavy | 12.3 (vest) | 26.3 (helmet) |

Hits to kill with that same M4 at each armor level:

| Armor worn | Upper torso | Head |
|---|---:|---:|
| None | 4 | 2 |
| Light | 5 | 3 |
| Medium | 6 | 3 |
| Heavy | 7 | 4 |
| Super heavy | 9 | 4 |

**Ammo changes the armor effect.** The protection depends on which round is loaded:

- **Full metal jacket and tracer** get the full reduction.
- **Hollow point** does about twice the damage of full metal jacket on unarmored flesh, but armor counts for more against it, and it loses most of its advantage as soon as any armor is worn.
- **Armor-piercing** does 20% less damage against unarmored flesh, but the armor's reduction is weaker. How much weaker depends on the weapon's arm class: the reduction is kept at 70% for small arms, 60% for medium arms, 50% for high arms and 100% for special arms. Weapons with no arm class keep 30%.

Hollow point and armor-piercing numbers against the M4 (upper torso and head):

| Armor worn | Full metal jacket | Hollow point | Armor-piercing |
|---|---:|---:|---:|
| None (torso) | 30.8 | 61.6 | 24.6 |
| Light vest | 21.6 | 9.1 | 20.2 |
| Medium vest | 18.5 | 6.7 | 18.7 |
| Heavy vest | 15.4 | 4.2 | 17.2 |
| Super heavy vest | 12.3 | 1.7 | 15.8 |
| Heavy helmet (head) | 32.9 | 5.9 | 36.8 |
| Super heavy helmet (head) | 26.3 | 2.4 | 33.7 |

## Rounds with their own armor rules

A few rounds have extra rules on top of the armor's reduction. Each multiplies the damage that is left. Values are for Season 2.

| Round | Against | Extra factor |
|---|---|---:|
| 12 gauge rifled slug | Any vest | x0.70 |
| 12 gauge rifled slug | Any helmet | x0.95 |
| 12 gauge rifled slug | Super heavy helmet | x0.88 more, so x0.84 with the row above |
| Compound Bow arrow | Heavy vest, Heavy helmet | x0.90 |
| Compound Bow arrow | Super heavy vest, Super heavy helmet | x0.66 |
| .50 cal | Heavy vest, Heavy helmet | x0.90 |
| .50 cal | Super heavy vest | x0.875 |
| .50 cal | Super heavy helmet | x0.80 |
| Armor-piercing sniper rounds | Super heavy helmet | x0.80 |
| Molotov fire | Super heavy vest | x0.70 |

Season 2 changed the slug rule against vests from x0.87 to x0.70, added the arrow, .50 cal and Molotov rules, and removed the old x0.75 that every high-class round (7.62 family, .308, .338 Norma Magnum, .50 AE, 30 mm, arrows) took against a Super heavy helmet. See [Season 2 patch notes](../patch-notes/season-2.md).

## Tips that follow from the numbers

- **Against Light armor, full metal jacket is best.** Armor-piercing is slightly weaker, and hollow point is much weaker.
- **Against Medium or heavier armor, armor-piercing does more damage.** The model gives 18.7 HP with armor-piercing and 18.5 HP with full metal jacket against a Medium vest, and 15.8 HP against 12.3 HP against a Super heavy vest.
- **Hollow point is for unarmored targets.** Its damage against any armor is far lower than full metal jacket.
- **The same rule holds for pistols.** The GGX 17 does 13.2 with armor-piercing and 12.7 with full metal jacket against a Heavy vest.
- **Armor does not cover every hit.** A headshot into a vest does full head damage, and a hit to the lower arm is not reduced by any armor. The Super heavy vest covers the upper arm.

For a guide to choosing ammo for each armor class, see [Choosing Ammo](../guides/choosing-ammo.md).

## See also

- [Health and Damage](health-and-damage.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Body armor and helmets](../../content/Wardogs_Items_v2.md) (item data)
- [Body armor](../equipment/body-armor.md)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md) (armor on every hit location)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (armor reduction and ammo effects)
- [Game Mechanics Reference](../../content/Wardogs_GameMechanics_v2.md) (armor and helmet rules)
- [Weapon damage by location (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
