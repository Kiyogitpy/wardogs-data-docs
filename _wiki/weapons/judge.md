---
title: "Judge"
parent: "Weapons"
group: "Pistols"
description: "The Judge pistol: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Judge

| Judge | |
|---|---|
| **General** |  |
| Class | Pistol |
| Caliber | [.45 Colt](caliber-45-colt.md) |
| Fire modes | Semi-automatic |
| **Performance** |  |
| Fire rate | 200 rounds/min |
| Muzzle velocity | 335 m/s |
| Effective range | 50 m |
| Standard magazine | Judge Bullet Cylinder |
| **Availability** |  |
| Vendor price | 250 |
| Unlock level | 1 |
| Internal name | Judge |
{: .wiki-infobox }

The Judge is a pistol chambered in .45 Colt. It fires semi-automatic at 200 rounds/min. Its standard magazine is the Judge Bullet Cylinder.

## Overview

Pistols are the sidearm class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 200 rounds/min |
| Muzzle velocity | 335 m/s |
| Effective range | 50 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 94.5 |
| Neck | 70.9 |
| Upper torso | 52.0 |
| Middle torso | 47.2 |
| Upper arm | 35.1 |
| Thigh | 35.1 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 52.0 | 94.5 |
| Light | 36.4 | 66.2 |
| Medium | 31.2 | 56.7 |
| Heavy | 26.0 | 47.2 |
| Super heavy | 20.8 | 37.8 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 52.0 |
| 50 m | 52.0 |
| 100 m | 48.7 |
| 200 m | 42.3 |
| 300 m | 37.1 |
| 400 m | 32.8 |
| 600 m | 25.4 |
| 800 m | 19.5 |
| 1000 m | 14.9 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 52.0 |
| Flesh Damage (HP) | 104.0 |
| Armor Piercing (AP) | 41.6 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Magazine. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (Judge Bullet Cylinder).

## Cost and unlocking

- Vendor price: 250. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

The Season 2 changes page lists no changes for this weapon.

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
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): names, slots and effects
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): body-part and armor damage
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): speed, effective range and falloff
