---
title: "AMR 50"
parent: "Weapons"
group: "Sniper rifles"
description: "The AMR 50 sniper rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# AMR 50

| AMR 50 | |
|---|---|
| **General** |  |
| Class | Sniper rifle |
| Caliber | [.50Cal](caliber-50cal.md) |
| Fire modes | Semi-automatic |
| **Performance** |  |
| Fire rate | 41.5 rounds/min |
| Muzzle velocity | 900 m/s |
| Effective range | 2000 m |
| Standard magazine | AMR 50 5 RND Magazine |
| **Availability** |  |
| Vendor price | 14800 |
| Unlock level | 1 |
| Internal name | SR_04 |
{: .wiki-infobox }

The AMR 50 is a sniper rifle chambered in .50Cal. It fires semi-automatic at 41.5 rounds/min. Its standard magazine is the AMR 50 5 RND Magazine.

## Overview

Sniper rifles are the sniper class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 41.5 rounds/min |
| Muzzle velocity | 900 m/s |
| Effective range | 2000 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 324.1 |
| Neck | 243.1 |
| Upper torso | 207.9 |
| Middle torso | 151.0 |
| Upper arm | 81.0 |
| Thigh | 81.0 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 207.9 | 324.1 |
| Light | 145.5 | 226.9 |
| Medium | 124.7 | 194.5 |
| Heavy | 93.6 | 145.8 |
| Super heavy | 72.8 | 103.7 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 207.9 |
| 50 m | 207.9 |
| 100 m | 207.9 |
| 200 m | 207.9 |
| 300 m | 207.9 |
| 400 m | 207.9 |
| 600 m | 207.9 |
| 800 m | 207.9 |
| 1000 m | 207.9 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 207.9 |
| Flesh Damage (HP) | 415.8 |
| Armor Piercing (AP) | 166.3 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Handguard, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (AMR 50 5 RND Magazine).

## Cost and unlocking

- Vendor price: 14800. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 2.0
- Vendor price: 8,800 to 14,800

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
