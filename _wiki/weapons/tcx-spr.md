---
title: "TCX-SPR"
parent: "Weapons"
group: "Marksman rifles"
description: "The TCX-SPR marksman rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# TCX-SPR

| TCX-SPR | |
|---|---|
| **General** |  |
| Class | Marksman rifle |
| Caliber | [7.62x39mm](caliber-7-62x39mm.md) |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 700 m/s |
| Effective range | 400 m |
| Standard magazine | TCX-SPR 28 RND Magazine |
| **Availability** |  |
| Vendor price | 3200 |
| Unlock level | 1 |
| Internal name | WEPN_037 |
{: .wiki-infobox }

The TCX-SPR is a marksman rifle chambered in 7.62x39mm. It fires fully automatic and semi-automatic at 800 rounds/min. Its standard magazine is the TCX-SPR 28 RND Magazine.

## Overview

Marksman rifles are the DMR class in the weapon data. Most are semi-automatic rifles.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 700 m/s |
| Effective range | 400 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 70.3 |
| Neck | 52.7 |
| Upper torso | 29.1 |
| Middle torso | 29.0 |
| Upper arm | 16.2 |
| Thigh | 16.2 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 29.1 | 70.3 |
| Light | 20.4 | 49.2 |
| Medium | 17.5 | 42.2 |
| Heavy | 14.6 | 35.2 |
| Super heavy | 11.7 | 28.1 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 29.1 |
| 50 m | 29.1 |
| 100 m | 29.1 |
| 200 m | 29.1 |
| 300 m | 29.1 |
| 400 m | 29.1 |
| 600 m | 19.7 |
| 800 m | 13.2 |
| 1000 m | 7.9 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 29.1 |
| Flesh Damage (HP) | 58.3 |
| Armor Piercing (AP) | 23.3 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (SIG Spear Standard Mag), grip (Sig Spear Standard Pistol Grip), stock (Sig Spear Standard Stock), barrel (Sig Spear Standard Barrel).

## Cost and unlocking

- Vendor price: 3200. The data pages do not decode the currency, so the price is shown as a plain number.
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
