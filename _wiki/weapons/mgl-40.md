---
title: "MGL-40"
parent: "Weapons"
group: "Launchers"
description: "The MGL-40 launcher: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# MGL-40

| MGL-40 | |
|---|---|
| **General** |  |
| Class | Launcher |
| Caliber | None (explosive) |
| Fire modes | Semi-automatic |
| **Performance** |  |
| Fire rate | 75 rounds/min |
| Muzzle velocity | not yet known |
| Effective range | not yet known |
| Standard magazine | MMGL Internal Mag |
| **Availability** |  |
| Vendor price | 7500 |
| Unlock level | 1 |
| Internal name | MMGL |
{: .wiki-infobox }

The MGL-40 is a launcher that fires explosive rounds rather than bullets. Its fire rate is 75 rounds/min.

## Overview

Launchers fire explosive rounds rather than bullets.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 75 rounds/min |
| Muzzle velocity | not yet known |
| Effective range | not yet known |

Launcher stats beyond the fire rate are not in the data pages.

## Damage

The damage data pages do not compute body-part damage for launchers. The data treats the shot as an explosion; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).

## Recoil and spread

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 2.0° | 4.0° |
| Crouching, hip fire | 1.5° | 3.0° |
| Prone, hip fire | 1.0° | 2.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.6° | 0.6° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 3.5 m when still and 7.0 m at full speed; aimed, it is 1.0 m. Half of the shots land within half that radius.

Accuracy is 20 mrad, a full cone angle; the aimed row is half of it, in degrees.

- Shooting does not widen the spread. The data has no per-shot bloom and no recovery timer.
- Hip spread moves with speed, stance and being in the air, and eases to its new value in about 0.04 s.
- Fully aimed, hip spread drops to zero at once, so only the aimed row applies.
- The figures are before attachments, which can change spread (see [Attachments](attachments.md)).
- Between still and full speed, hip spread is a straight line.

**Recoil**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | none, each shot kicks at random |
| Random kick per shot | up 1.00° to 2.00°, sideways -1.00° to 1.00° |
| Climb after 10 shots | 15.0° up |
| Climb after 30 shots | 45.0° up |
| Average climb per shot over 30 shots | 1.50° up |
| Sideways drift after 30 shots | none |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 1.00× / 1.00× |
| Default-loadout recoil multiplier, vertical / horizontal | 1 / 1 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. This weapon has no authored pattern, so the climb figures use the middle of its random range.

Season 2 did not change the recoil pattern.

To see the whole pattern as a picture, open the [Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) and pick the MGL-40 in the viewer.

## Ammunition

Launchers do not use the bullet types on the [Ammunition](ammunition.md) page.

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Stock. See [Attachments](attachments.md) for what each part changes.

Default parts: sight (MMGL Sight), magazine (MMGL Internal Mag).

## Cost and unlocking

- Vendor price: 7500. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Muzzle velocity: 100 m/s to 75 m/s
- Vendor price: 6,000 to 7,500

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
