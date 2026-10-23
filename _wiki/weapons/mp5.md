---
title: "MP5"
parent: "Weapons"
description: "The MP5 submachine gun: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# MP5

| MP5 | |
|---|---|
| Class | Submachine gun |
| Caliber | 9x19mm |
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 400 m/s |
| Effective range | 200 m |
| Standard magazine | MP5 30 RND Magazine |
| Vendor price | 1800 |
| Unlock level | 1 |
| Internal name | WEPN_028 |
{: .wiki-infobox }

The MP5 is a submachine gun chambered in 9x19mm. It fires fully automatic and semi-automatic at 800 rounds/min. Its standard magazine is the MP5 30 RND Magazine.

## Overview

Submachine guns are the SMG class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 400 m/s |
| Effective range | 200 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 46.2 |
| Neck | 34.7 |
| Upper torso | 25.4 |
| Middle torso | 23.1 |
| Upper arm | 17.2 |
| Thigh | 17.2 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 25.4 | 46.2 |
| Light | 17.8 | 32.3 |
| Medium | 15.2 | 27.7 |
| Heavy | 12.7 | 23.1 |
| Super heavy | 10.2 | 18.5 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 25.4 |
| 50 m | 25.4 |
| 100 m | 25.4 |
| 200 m | 22.3 |
| 300 m | 11.5 |
| 400 m | 7.4 |
| 600 m | 2.9 |
| 800 m | 1.2 |
| 1000 m | 0.7 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 25.4 |
| Flesh Damage (HP) | 50.8 |
| Armor Piercing (AP) | 20.3 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (MP5 30 RND Magazine), stock (MP5 Stock), barrel (MP5 Barrel).

## Cost and unlocking

- Vendor price: 1800. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- View kick multiplier: 1.1 to 1.15
- Vendor price: 1,500 to 1,800

## See also

- [Weapons](../weapons.md)
- [Ammunition](ammunition.md)
- [Attachments](attachments.md)

## Sources

- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): price, unlock level, default magazine
- [Infantry Weapon Stats](../../content/Wardogs_InfantryWeapons_Stats_v1.md): fire rate and fire modes
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part, armor and falloff numbers
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): names, slots and effects
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): body-part and armor damage
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): speed, effective range and falloff
