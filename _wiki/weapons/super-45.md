---
title: "Super-45"
parent: "Weapons"
group: "Submachine guns"
description: "The Super-45 submachine gun: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Super-45

| Super-45 | |
|---|---|
| **General** |  |
| Class | Submachine gun |
| Caliber | .45 ACP |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 1,200 rounds/min |
| Muzzle velocity | 375 m/s |
| Effective range | 50 m |
| Standard magazine | Super-45 30 RND Magazine |
| **Availability** |  |
| Vendor price | 5600 |
| Unlock level | 1 |
| Internal name | Vector |
{: .wiki-infobox }

The Super-45 is a submachine gun chambered in .45 ACP. It fires fully automatic and semi-automatic at 1,200 rounds/min. Its standard magazine is the Super-45 30 RND Magazine.

## Overview

Submachine guns are the SMG class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 1,200 rounds/min |
| Muzzle velocity | 375 m/s |
| Effective range | 50 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 63.0 |
| Neck | 47.3 |
| Upper torso | 34.7 |
| Middle torso | 31.5 |
| Upper arm | 23.4 |
| Thigh | 23.4 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 34.7 | 63.0 |
| Light | 24.3 | 44.1 |
| Medium | 20.8 | 37.8 |
| Heavy | 17.3 | 31.5 |
| Super heavy | 13.9 | 25.2 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 34.7 |
| 50 m | 34.7 |
| 100 m | 12.8 |
| 200 m | 8.2 |
| 300 m | 7.1 |
| 400 m | 6.1 |
| 600 m | 4.6 |
| 800 m | 3.4 |
| 1000 m | 2.5 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 34.7 |
| Flesh Damage (HP) | 69.3 |
| Armor Piercing (AP) | 27.7 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (Super-45 30 RND Magazine).

## Cost and unlocking

- Vendor price: 5600. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 0.8
- Vendor price: 2,600 to 5,600
- Damage falloff curve reshaped

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
