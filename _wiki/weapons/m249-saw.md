---
title: "M249 SAW"
parent: "Weapons"
description: "The M249 SAW light machine gun: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# M249 SAW

| M249 SAW | |
|---|---|
| Class | Light machine gun |
| Caliber | 5.56x45mm |
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 850 rounds/min |
| Muzzle velocity | 915 m/s |
| Effective range | 700 m |
| Standard magazine | M249 200 RND Box |
| Vendor price | 3200 |
| Unlock level | 1 |
| Internal name | M249 |
{: .wiki-infobox }

The M249 SAW is a light machine gun chambered in 5.56x45mm. It fires fully automatic and semi-automatic at 850 rounds/min. Its standard magazine is the M249 200 RND Box.

## Overview

Light machine guns are the LMG class in the weapon data.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 850 rounds/min |
| Muzzle velocity | 915 m/s |
| Effective range | 700 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 65.8 |
| Neck | 49.4 |
| Upper torso | 27.3 |
| Middle torso | 27.2 |
| Upper arm | 15.1 |
| Thigh | 15.1 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 27.3 | 65.8 |
| Light | 19.1 | 46.1 |
| Medium | 16.4 | 39.5 |
| Heavy | 13.6 | 32.9 |
| Super heavy | 10.9 | 26.3 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 27.3 |
| 50 m | 27.3 |
| 100 m | 27.3 |
| 200 m | 27.3 |
| 300 m | 27.3 |
| 400 m | 27.3 |
| 600 m | 27.3 |
| 800 m | 21.7 |
| 1000 m | 12.0 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 27.3 |
| Flesh Damage (HP) | 54.5 |
| Armor Piercing (AP) | 21.8 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (M249 200 RND Box).

## Cost and unlocking

- Vendor price: 3200. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Suppression effect multiplier: none to 1.25

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
