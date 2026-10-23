---
title: "Deagle"
parent: "Weapons"
description: "The Deagle pistol: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Deagle

| Deagle | |
|---|---|
| Class | Pistol |
| Caliber | 50AE |
| Fire modes | Semi-automatic |
| Fire rate | 267 rounds/min |
| Muzzle velocity | 470 m/s |
| Effective range | not yet known |
| Standard magazine | Deagle 7 RND Magazine |
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
| Effective range | not yet known |

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
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): names, slots and effects
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): body-part and armor damage
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): speed, effective range and falloff
