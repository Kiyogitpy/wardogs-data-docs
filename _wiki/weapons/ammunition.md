---
title: "Ammunition"
parent: "Weapons"
description: "Bullet and shell types, what each does to armor and flesh, and which weapons use them."
---

# Ammunition

Bullet weapons use one of four bullet types, and each has a tracer version that does the same damage with a visible trail. The shotgun fires two shell types. The type changes how much damage a hit does, most of all against armor.

| Type | What it does | Against no armor | Against armor |
|---|---|---|---|
| Standard (FMJ) | The baseline round. | Baseline. | Baseline. |
| Flesh Damage (HP) | Does more damage to unarmored targets. | About double the standard damage. | Much weaker than standard against every armor class. |
| Armor Piercing (AP) | Built to get through armor. | About 0.8 times the standard damage. | Overtakes standard from Medium armor for rifle calibers, and from Heavy armor for pistol and SMG calibers. |

Tracer versions of each type do the same damage as their base type.

## Torso damage by type: 5.56mm rifle example

A-91 chambered in 5.56mm, upper torso hits:

| Ammo | No armor | Light | Medium | Heavy | Super heavy |
|---|---|---|---|---|---|
| Standard (FMJ) | 27.3 | 19.1 | 16.4 | 13.6 | 10.9 |
| Flesh Damage (HP) | 54.5 | 8.1 | 5.9 | 3.7 | 1.5 |
| Armor Piercing (AP) | 21.8 | 17.9 | 16.6 | 15.3 | 14.0 |

Head hits follow the same pattern with higher numbers. Armor covers different body parts by type; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).

## Shotgun shells

- Buckshot: 24.8 upper torso damage, no armor, per pellet, 8 pellets per shot.
- Rifled slug: 104.0 upper torso damage, no armor, per hit.

## Which weapons use each caliber

| Caliber | Weapons |
|---|---|
| .308 Win | [FAL](fal.md), [BMR-308](bmr-308.md), [M14](m14.md), [Evo-3 Ultra](evo-3-ultra.md), [MK22](mk22.md) |
| .45 ACP | [M1911](m1911.md), [Super-45](super-45.md) |
| .45 Colt | [Judge](judge.md) |
| .50Cal | [AMR 50](amr-50.md) |
| 12g | [M500](m500.md), [MP43](mp43.md) |
| 5.45x39mm | [AK74](ak74.md) |
| 5.56x45mm | [A-91](a-91.md), [Bushmaster M17S](bushmaster-m17s.md), [Galil](galil.md), [KH-2002](kh-2002.md), [M4](m4.md), [T-21](t-21.md), [M249 SAW](m249-saw.md), [Scout Rifle TD](scout-rifle-td.md) |
| 50AE | [Deagle](deagle.md) |
| 7.62x39mm | [SKS](sks.md), [TCX-SPR](tcx-spr.md) |
| 7.62x54mm | [SVD](svd.md), [PKM](pkm.md), [Mosin Nagant](mosin-nagant.md), [SV98](sv98.md) |
| 9x19mm | [GGX 17](ggx-17.md), [GGX 18](ggx-18.md), [AMP-9](amp-9.md), [MP5](mp5.md), [PP-19 Bizon](pp-19-bizon.md), [PP-19 Vityaz](pp-19-vityaz.md) |

## See also

- [Choosing Ammo](../guides/choosing-ammo.md), which round to load against each armor level
- [Armor](../game-mechanics/armor.md)
- [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md)
- [Ballistics](../game-mechanics/ballistics.md)

## Sources

- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json)
- [ammo-availability.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ammo-availability.json)
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md)
- [Ammo (feature)](../../game-features/Wardogs_GameFeatures_Ammo_v2.md)
