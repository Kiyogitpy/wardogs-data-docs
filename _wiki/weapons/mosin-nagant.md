---
title: "Mosin Nagant"
parent: "Weapons"
description: "The Mosin Nagant sniper rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Mosin Nagant

| Mosin Nagant | |
|---|---|
| Class | Sniper rifle |
| Caliber | 7.62x54mm |
| Fire modes | Semi-automatic |
| Fire rate | 46 rounds/min |
| Muzzle velocity | 865 m/s |
| Effective range | 500 m |
| Standard magazine | Mosin Standard Mag |
| Vendor price | 4500 |
| Unlock level | 1 |
| Internal name | WEPN_017 |
{: .wiki-infobox }

The Mosin Nagant is a sniper rifle chambered in 7.62x54mm. It fires semi-automatic at 46 rounds/min. Its standard magazine is the Mosin Standard Mag.

## Overview

Sniper rifles are the sniper class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 46 rounds/min |
| Muzzle velocity | 865 m/s |
| Effective range | 500 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 187.7 |
| Neck | 140.8 |
| Upper torso | 116.2 |
| Middle torso | 85.1 |
| Upper arm | 39.6 |
| Thigh | 39.6 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 116.2 | 187.7 |
| Light | 81.3 | 131.4 |
| Medium | 69.7 | 112.6 |
| Heavy | 58.1 | 93.9 |
| Super heavy | 46.5 | 75.1 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 116.2 |
| 50 m | 116.2 |
| 100 m | 116.2 |
| 200 m | 116.2 |
| 300 m | 116.2 |
| 400 m | 116.2 |
| 600 m | 106.2 |
| 800 m | 86.3 |
| 1000 m | 66.4 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 116.2 |
| Flesh Damage (HP) | 232.3 |
| Armor Piercing (AP) | 92.9 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (Mosin Standard Mag).

## Cost and unlocking

- Vendor price: 4500. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 1.5

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
