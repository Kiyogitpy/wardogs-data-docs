---
title: "SKS"
parent: "Weapons"
description: "The SKS marksman rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# SKS

| SKS | |
|---|---|
| Class | Marksman rifle |
| Caliber | 7.62x39mm |
| Fire modes | Semi-automatic |
| Fire rate | 420 rounds/min |
| Muzzle velocity | 735 m/s |
| Effective range | 400 m |
| Standard magazine | SKS Internal Mag |
| Vendor price | 2400 |
| Unlock level | 1 |
| Internal name | SKS |
{: .wiki-infobox }

The SKS is a marksman rifle chambered in 7.62x39mm. It fires semi-automatic at 420 rounds/min. Its standard magazine is the SKS Internal Mag.

## Overview

Marksman rifles are the DMR class in the weapon data. Most are semi-automatic rifles.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 420 rounds/min |
| Muzzle velocity | 735 m/s |
| Effective range | 400 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 83.3 |
| Neck | 62.5 |
| Upper torso | 40.0 |
| Middle torso | 40.1 |
| Upper arm | 25.5 |
| Thigh | 25.5 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 40.0 | 83.3 |
| Light | 28.0 | 58.3 |
| Medium | 24.0 | 50.0 |
| Heavy | 20.0 | 41.7 |
| Super heavy | 16.0 | 33.3 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 40.0 |
| 50 m | 40.0 |
| 100 m | 40.0 |
| 200 m | 40.0 |
| 300 m | 40.0 |
| 400 m | 40.0 |
| 600 m | 25.1 |
| 800 m | 16.7 |
| 1000 m | 10.0 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 40.0 |
| Flesh Damage (HP) | 80.0 |
| Armor Piercing (AP) | 32.0 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (SKS Internal Mag).

## Cost and unlocking

- Vendor price: 2400. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 1.1
- View kick multiplier removed
- Recoil pattern reworked

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
