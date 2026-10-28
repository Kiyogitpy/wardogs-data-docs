---
title: ".50 Cal"
parent: "Ammunition"
redirect_from: ["/wiki/weapons/caliber-50cal/"]
description: "The .50 Cal caliber: the weapons that fire it, its bullet types, how they do against armor and what the ammunition costs."
---

# .50 Cal

| .50 Cal | |
|---|---|
| ![.50 Cal]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox__50-AE_FMJ.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Bullet types | Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP) (each with a tracer version) |
| Weapons | 1 |
| Classes | Sniper rifle |
| **Ballistics** | |
| Muzzle velocity | 900 m/s |
| **Availability** | |
| Standard (FMJ) price | 250 cash (vendor lot of 5), not shown in the vendor list |
| Flesh Damage (HP) price | 375 cash (vendor lot of 5), not shown in the vendor list |
| Armor Piercing (AP) price | 500 cash (vendor lot of 5), not shown in the vendor list |
| Internal name | 50Cal |
{: .wiki-infobox }

The .50 Cal caliber is used by 1 weapon, across the Sniper rifle class. Its rounds are Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). The tables below show how each type does against armor.

## Weapons that use it

| Weapon | Class | Fire rate | Upper torso, no armor, point blank |
|---|---|---:|---:|
| [AMR 50](../weapons/amr-50.md) | Sniper rifle | 41.5 rounds/min | 207.9 |

Point-blank figures use standard rounds (buckshot for shotguns, per pellet), per hit, without falloff. See [Ammunition](../ammunition.md) for the bullet types.

## Ammunition types

Upper torso hits from the AMR 50 at point blank range, per hit, without falloff. Armor changes these numbers a lot, so every armor class is shown.

| Ammo | No armor | Light | Medium | Heavy | Super heavy |
|---|---|---|---|---|---|
| Standard (FMJ) | 207.9 | 145.5 | 124.7 | 93.6 | 72.8 |
| Flesh Damage (HP) | 415.8 | 61.7 | 44.9 | 25.3 | 9.8 |
| Armor Piercing (AP) | 166.3 | 116.4 | 99.8 | 74.8 | 58.2 |
| Standard (FMJ) with tracer | 207.9 | 145.5 | 124.7 | 93.6 | 72.8 |

Flesh Damage (HP) with tracer, Armor Piercing (AP) with tracer match their base type.

## Against armor

- Armor Piercing does less damage than standard rounds at every armor class.
- Flesh Damage does 2.0 times the standard damage with no armor and 0.1 times against super heavy armor. It is the strongest type against unarmored targets. It is the weakest type against super heavy armor.

The numbers come from the upper torso column of the table above. Head hits follow the same pattern at higher values; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).

## Season 2 changes

- Weapons in this caliber with Season 2 changes: [AMR 50](../weapons/amr-50.md). Each article lists its changes.

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
