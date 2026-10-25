---
title: "Deagle"
parent: "Weapons"
group: "Pistols"
description: "The Deagle pistol: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Deagle

| Deagle | |
|---|---|
| **General** |  |
| Class | Pistol |
| Caliber | [50AE](caliber-50ae.md) |
| Fire modes | Semi-automatic |
| **Performance** |  |
| Fire rate | 267 rounds/min |
| Muzzle velocity | 470 m/s |
| Effective range | 100 m (game default) |
| Standard magazine | Deagle 7 RND Magazine |
| **Availability** |  |
| Vendor price | 750 |
| Unlock level | 1 |
| Internal name | WEPN_027 |
{: .wiki-infobox }

The Deagle is a pistol chambered in 50AE. It fires semi-automatic at 267 rounds/min. Its standard magazine is the Deagle 7 RND Magazine.

## Overview

Pistols are the sidearm class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 267 rounds/min |
| Muzzle velocity | 470 m/s |
| Effective range | 100 m (game default) |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 132.3 |
| Neck | 99.2 |
| Upper torso | 72.8 |
| Middle torso | 66.2 |
| Upper arm | 49.1 |
| Thigh | 49.1 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 72.8 | 132.3 |
| Light | 50.9 | 92.6 |
| Medium | 43.7 | 79.4 |
| Heavy | 36.4 | 66.2 |
| Super heavy | 29.1 | 52.9 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 72.8 |
| 50 m | 72.8 |
| 100 m | 70.7 |
| 200 m | 56.2 |
| 300 m | 46.3 |
| 400 m | 39.8 |
| 600 m | 29.3 |
| 800 m | 20.5 |
| 1000 m | 13.1 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 72.8 |
| Flesh Damage (HP) | 145.5 |
| Armor Piercing (AP) | 58.2 |

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
| Aimed down sights | 0.0070° | 0.0070° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 5.2 m when still and 10.5 m at full speed; aimed, it is 0.01 m. Half of the shots land within half that radius.

Accuracy is 0.84 MOA, a full cone angle; the aimed row is half of it, in degrees.

- The data has no per-shot bloom and no recovery timer: nothing found in the spread data makes firing widen the spread, and spread changes only with speed, stance, being in the air and aiming. This comes from reading the game files, not from testing in game.
- Hip spread eases toward its new value with a time constant of about 0.04 s (a native default found by static reading).
- The 10° in-air figure is a native default found by static reading; only the grenade launcher's data sets it, to the same 10°.
- At full aim (aim blend exactly 1.0) hip spread is set to zero, so only the aimed row applies. A partly aimed weapon counts as hip fire.
- "Full speed" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; between still and that speed the hip spread is a straight line.
- The figures are before attachments, which can change spread (see [Attachments](attachments.md)).

**Recoil**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | 15 |
| Kick on the first shot | 1.17° up |
| Climb after 10 shots | 13.0° up |
| Climb after 30 shots | 28.9° up |
| Average climb per shot over 30 shots | 0.96° up |
| Sideways drift after 30 shots | 9.2° right |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 0.85× / 0.70× |
| Default-loadout recoil multiplier, vertical / horizontal | 1 / 1 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. The game turns each authored kick by up to 5° per shot, so the real sideways drift varies from burst to burst. After shot 15 each kick is random inside the post-pattern range.

Season 2 did not change the recoil pattern.

To see the whole pattern as a picture, open the [Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) and pick the Deagle in the viewer.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Magazine, Sight. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (Deagle 7 RND Magazine), barrel (Deagle Barrel).

## Cost and unlocking

- Vendor price: 750. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Vendor price: 900 to 750

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
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): falloff curves
- [weapon-capacity.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-capacity.json): muzzle speed, effective range, chamber and magazine
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate
