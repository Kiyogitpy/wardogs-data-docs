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
| Ghillie suit | Effect not yet known |
{: .wiki-infobox }

Armor is worn in two slots: a vest for the body and a helmet for the head. Each piece cuts the damage of a hit to the body parts it covers. The amount of protection depends on the armor class, and the ammo in the weapon changes how much of that protection applies. The full list of armor items is on [Body Armor](../../content/Wardogs_Items_v2.md).

## Overview

The armor classes are Light, Medium, Heavy and Super heavy for vests, and the same four plus Pilot and Tank for helmets. A higher class blocks more damage. Each piece lasts for a set amount of durability, and the reduction does not fall as durability falls in the current data.

## How it works

- A vest covers the upper, middle and lower torso. The Super heavy vest also covers the pelvis and the upper arm.
- A helmet covers the head. The Heavy, Super heavy and Tank helmets also cover the neck.
- A vest and a helmet never cover the same body part, so at any one place only one piece of armor applies.
- The lower arms, hands, thighs, calves and feet are not covered by any armor.
- Armor reduces bullet damage by its percentage. A Heavy vest (50%) turns a 27.3 upper-torso hit from an M4 into 13.6.
- Ghillie suits and helmets do not have a reduction in the data, so their effect is not yet known.

## Numbers

Damage per hit to the upper torso and to the head, with the M4 (full metal jacket ammo):

| Armor worn | Upper torso | Head |
|---|---:|---:|
| None | 27.3 | 65.8 |
| Light | 19.1 (vest) | 46.1 (helmet) |
| Medium | 16.4 (vest) | 39.5 (helmet) |
| Heavy | 13.6 (vest) | 32.9 (helmet) |
| Super heavy | 10.9 (vest) | 26.3 (helmet) |

Hits to kill with that same M4 at each armor level:

| Armor worn | Upper torso | Head |
|---|---:|---:|
| None | 4 | 2 |
| Light | 6 | 3 |
| Medium | 7 | 3 |
| Heavy | 8 | 4 |
| Super heavy | 10 | 4 |

**Ammo changes the armor effect.** The protection depends on which round is loaded:

- **Full metal jacket and tracer** get the full reduction.
- **Hollow point** does about twice the damage of full metal jacket on unarmored flesh, but armor counts for more against it, and it loses most of its advantage as soon as any armor is worn.
- **Armor-piercing** does 20% less damage against unarmored flesh, but the armor's reduction is weaker. How much weaker depends on the weapon's arm class: the reduction is kept at 70% for small arms, 60% for medium arms, 50% for high arms and 100% for special arms. Weapons with no arm class keep 30%.

Hollow point and armor-piercing numbers against the M4 (upper torso and head):

| Armor worn | Full metal jacket | Hollow point | Armor-piercing |
|---|---:|---:|---:|
| None (torso) | 27.3 | 54.5 | 21.8 |
| Light vest | 19.1 | 8.1 | 17.9 |
| Medium vest | 16.4 | 5.9 | 16.6 |
| Heavy vest | 13.6 | 3.7 | 15.3 |
| Super heavy vest | 10.9 | 1.5 | 14.0 |
| Heavy helmet (head) | 32.9 | 5.9 | 36.8 |
| Super heavy helmet (head) | 26.3 | 2.4 | 33.7 |

## Tips that follow from the numbers

- **Against Light armor, full metal jacket is best.** Armor-piercing is slightly weaker, and hollow point is much weaker.
- **Against Medium or heavier armor, armor-piercing does more damage.** The M4 does 16.6 with armor-piercing and 16.4 with full metal jacket against a Medium vest, and 14.0 against 10.9 against a Super heavy vest.
- **Hollow point is for unarmored targets.** Its damage against any armor is far lower than full metal jacket.
- **The same rule holds for pistols.** The GGX 17 does 13.2 with armor-piercing and 12.7 with full metal jacket against a Heavy vest.
- **Armor does not cover every hit.** A headshot into a vest does full head damage, and a hit to the arm is not reduced by any armor.

For a guide to choosing ammo for each armor class, see [Choosing Ammo](../guides/choosing-ammo.md).

## See also

- [Health and Damage](health-and-damage.md)
- [Penetration and Ricochet](penetration-and-ricochet.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Body armor and helmets](../../content/Wardogs_Items_v2.md) (item data)

## Sources

- [Damage by Weapon and Ammo](../../game-features/Wardogs_WeaponDamage_v1.md) (armor on every hit location)
- [Damage rules](../../pipelines/Wardogs_DamagePipeline_v2.md) (armor reduction and ammo effects)
- [Game Mechanics Reference](../../content/Wardogs_GameMechanics_v2.md) (armor and helmet rules)
- [Weapon damage by location (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json)
