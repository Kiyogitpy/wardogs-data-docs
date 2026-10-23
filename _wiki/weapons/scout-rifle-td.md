---
title: "Scout Rifle TD"
parent: "Weapons"
description: "The Scout Rifle TD sniper rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# Scout Rifle TD

| Scout Rifle TD | |
|---|---|
| Class | Sniper rifle |
| Caliber | 5.56x45mm |
| Fire modes | Semi-automatic |
| Fire rate | 46 rounds/min |
| Muzzle velocity | 975 m/s |
| Effective range | 300 m |
| Standard magazine | not yet known |
| Vendor price | 1200 |
| Unlock level | 1 |
| Internal name | WEPN_035 |
{: .wiki-infobox }

The Scout Rifle TD is a sniper rifle chambered in 5.56x45mm. It fires semi-automatic at 46 rounds/min.

## Overview

Sniper rifles are the sniper class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 46 rounds/min |
| Muzzle velocity | 975 m/s |
| Effective range | 300 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 119.5 |
| Neck | 89.6 |
| Upper torso | 73.9 |
| Middle torso | 54.1 |
| Upper arm | 25.2 |
| Thigh | 25.2 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 73.9 | 119.5 |
| Light | 51.7 | 83.6 |
| Medium | 44.4 | 71.7 |
| Heavy | 37.0 | 59.7 |
| Super heavy | 29.6 | 47.8 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 73.9 |
| 50 m | 73.9 |
| 100 m | 73.9 |
| 200 m | 73.9 |
| 300 m | 73.9 |
| 400 m | 62.6 |
| 600 m | 35.5 |
| 800 m | 21.1 |
| 1000 m | 12.7 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 73.9 |
| Flesh Damage (HP) | 147.8 |
| Armor Piercing (AP) | 59.1 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: stock (Scout Rifle Stock), barrel (Scout Rifle Standard Barrel).

## Cost and unlocking

- Vendor price: 1200. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 1.5
- Vendor price: 1,100 to 1,200

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
