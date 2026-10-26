---
title: "12 gauge"
parent: "Ammunition"
redirect_from: ["/wiki/weapons/caliber-12g/"]
description: "The 12 gauge caliber: the weapons that fire it, its bullet types, how they do against armor and what the ammunition costs."
---

# 12 gauge

| 12 gauge | |
|---|---|
| ![12 gauge]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_12g_slug_green.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Bullet types | Buckshot, Rifled slug |
| Weapons | 2 |
| Classes | Shotgun |
| **Ballistics** | |
| Muzzle velocity | 391 to 480 m/s |
| **Availability** | |
| Buckshot price | 60 cash (vendor lot of 6) |
| Rifled slug price | 200 cash (vendor lot of 6) |
| Internal name | 12g |
{: .wiki-infobox }

The 12 gauge caliber is used by 2 weapons in the weapon data, across the Shotgun class. Its shells are Buckshot, Rifled slug. The tables below show how each type does against armor.

## Weapons that use it

| Weapon | Class | Fire rate | Upper torso, no armor, point blank |
|---|---|---:|---:|
| [M500](../weapons/m500.md) | Shotgun | 120 rounds/min | 24.8 per pellet (8 pellets) |
| [MP43](../weapons/mp43.md) | Shotgun | 900 rounds/min | 24.8 per pellet (8 pellets) |

Point-blank figures use standard rounds (buckshot for shotguns, per pellet), per hit, without falloff. See [Ammunition](../ammunition.md) for the bullet types.

## Ammunition types

Upper torso hits from the M500 at point blank range, per hit, without falloff. Armor changes these numbers a lot, so every armor class is shown.

| Ammo | No armor | Light | Medium | Heavy | Super heavy |
|---|---|---|---|---|---|
| Buckshot (per pellet) | 24.8 | 10.4 | 8.9 | 7.4 | 3.6 |
| Rifled slug | 104.0 | 50.9 | 43.7 | 36.4 | 29.1 |

A buckshot shot has 8 pellets, so multiply the per-pellet figure by 8 for a full hit.

## Against armor

- A rifled slug does less damage than a full buckshot shot up to heavy armor and more damage from super heavy armor up if all 8 pellets hit.

The numbers come from the upper torso column of the table above. Head hits follow the same pattern at higher values; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).

## Season 2 changes

The Season 2 changes page lists no changes to this caliber or to the weapons that use it.

## See also

- [Ammunition](../ammunition.md), the bullet types and which weapons use each caliber
- [Choosing Ammo](../guides/choosing-ammo.md), which round to load against each armor level
- [Armor](../game-mechanics/armor.md)
- [Ballistics](../game-mechanics/ballistics.md)
- [Weapons](../weapons.md)

## Sources

- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part and armor numbers
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber names
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): ammo types and damage by armor class
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): muzzle velocity
- [ammo-availability.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ammo-availability.json): ammo prices
