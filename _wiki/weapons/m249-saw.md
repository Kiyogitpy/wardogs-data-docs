---
title: "M249 SAW"
parent: "Weapons"
group: "Light machine guns"
description: "The M249 SAW light machine gun: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# M249 SAW

| M249 SAW | |
|---|---|
| **General** |  |
| Class | Light machine gun |
| Caliber | [5.56x45mm](caliber-5-56x45mm.md) |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 850 rounds/min |
| Muzzle velocity | 915 m/s |
| Effective range | 700 m |
| Standard magazine | M249 200 RND Box |
| **Availability** |  |
| Vendor price | 3200 |
| Unlock level | 1 |
| Internal name | M249 |
{: .wiki-infobox }

The M249 SAW is a light machine gun chambered in 5.56x45mm. It fires fully automatic and semi-automatic at 850 rounds/min. Its standard magazine is the M249 200 RND Box.

## Overview

Light machine guns are the LMG class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 850 rounds/min |
| Muzzle velocity | 915 m/s |
| Effective range | 700 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 65.8 |
| Neck | 49.4 |
| Upper torso | 27.3 |
| Middle torso | 27.2 |
| Upper arm | 15.1 |
| Thigh | 15.1 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 27.3 | 65.8 |
| Light | 19.1 | 46.1 |
| Medium | 16.4 | 39.5 |
| Heavy | 13.6 | 32.9 |
| Super heavy | 10.9 | 26.3 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 27.3 |
| 50 m | 27.3 |
| 100 m | 27.3 |
| 200 m | 27.3 |
| 300 m | 27.3 |
| 400 m | 27.3 |
| 600 m | 27.3 |
| 800 m | 21.7 |
| 1000 m | 12.0 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 27.3 |
| Flesh Damage (HP) | 54.5 |
| Armor Piercing (AP) | 21.8 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Recoil and spread

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 3.0° | 6.0° |
| Crouching, hip fire | 2.0° | 4.0° |
| Prone, hip fire | 1.0° | 2.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.1° | 0.1° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 5.2 m when still and 10.5 m at full speed; aimed, it is 0.22 m. Half of the shots land within half that radius.

Accuracy is 4.3 mrad, a full cone angle; the aimed row is half of it, in degrees.

- Shooting does not widen the spread. The data has no per-shot bloom and no recovery timer.
- Hip spread moves with speed, stance and being in the air, and eases to its new value in about 0.04 s.
- Fully aimed, hip spread drops to zero at once, so only the aimed row applies.
- The figures are before attachments, which can change spread (see [Attachments](attachments.md)).
- Between still and full speed, hip spread is a straight line.

**Recoil**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | 7 |
| Kick on the first shot | 2.41° up |
| Climb after 10 shots | 16.1° up |
| Climb after 30 shots | 36.1° up |
| Average climb per shot over 30 shots | 1.20° up |
| Sideways drift after 30 shots | 1.5° left |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 0.60× / 0.35× |
| Default-loadout recoil multiplier, vertical / horizontal | 1.17 / 1.17 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. The game turns each authored kick by up to 20° per shot, so the real sideways drift varies from burst to burst. After shot 7 each kick is random inside the post-pattern range.

Season 2 did not change the recoil pattern.

To see the whole pattern as a picture, open the [Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) and pick the M249 SAW in the viewer.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (M249 200 RND Box).

## Cost and unlocking

- Vendor price: 3200. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 1.25

## See also

- [Weapons](../weapons.md)
- [Ammunition](ammunition.md)
- [Attachments](attachments.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Ballistics](../game-mechanics/ballistics.md)
- [Health and Damage](../game-mechanics/health-and-damage.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)

## Sources

- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): price, unlock level, default magazine
- [Infantry Weapon Stats](../../content/Wardogs_InfantryWeapons_Stats_v1.md): fire rate and fire modes
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part, armor and falloff numbers
- [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md): spread and recoil inputs
- [Weapon Spread pipeline](../../pipelines/Wardogs_WeaponSpread_v1.md): how the aim cone and hip spread are computed
- [Spray Patterns Gallery](../../game-features/Wardogs_SprayPatterns_v1.md): recoil patterns, Season 1 and Season 2
- [weapon-spread-recoil.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-spread-recoil.json): accuracy and hip spread curves
- [spray-patterns.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/spray-patterns.json): recoil pattern points, Season 1 and Season 2
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): names, slots and effects
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): body-part and armor damage
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): speed, effective range and falloff
