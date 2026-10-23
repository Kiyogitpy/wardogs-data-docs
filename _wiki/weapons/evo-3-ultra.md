---
title: "Evo-3 Ultra"
parent: "Weapons"
group: "Light machine guns"
description: "The Evo-3 Ultra light machine gun: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Evo-3 Ultra

| Evo-3 Ultra | |
|---|---|
| **General** |  |
| Class | Light machine gun |
| Caliber | .308 Win |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 700 rounds/min |
| Muzzle velocity | 790 m/s |
| Effective range | 1000 m |
| Standard magazine | Evo-3 Ultra 50 RND Box |
| **Availability** |  |
| Vendor price | 7250 |
| Unlock level | 1 |
| Internal name | WEPN_036 |
{: .wiki-infobox }

The Evo-3 Ultra is a light machine gun chambered in .308 Win. It fires fully automatic and semi-automatic at 700 rounds/min. Its standard magazine is the Evo-3 Ultra 50 RND Box.

## Overview

Light machine guns are the LMG class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 700 rounds/min |
| Muzzle velocity | 790 m/s |
| Effective range | 1000 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 79.3 |
| Neck | 59.5 |
| Upper torso | 32.9 |
| Middle torso | 32.7 |
| Upper arm | 18.2 |
| Thigh | 18.2 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 32.9 | 79.3 |
| Light | 23.0 | 55.5 |
| Medium | 19.7 | 47.6 |
| Heavy | 16.4 | 39.7 |
| Super heavy | 13.1 | 31.7 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 32.9 |
| 50 m | 32.9 |
| 100 m | 32.9 |
| 200 m | 32.9 |
| 300 m | 32.9 |
| 400 m | 32.9 |
| 600 m | 32.9 |
| 800 m | 32.9 |
| 1000 m | 32.6 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 32.9 |
| Flesh Damage (HP) | 65.7 |
| Armor Piercing (AP) | 26.3 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (Evo-3 Ultra 50 RND Box), grip (Evoly Grip), stock (Evoly stock), barrel (Evoly Standard Barrel).

## Cost and unlocking

- Vendor price: 7250. The data pages do not decode the currency, so the price is shown as a plain number.
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
