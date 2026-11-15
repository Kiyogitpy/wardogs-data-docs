---
title: Ammunition
nav_order: 1.2
wiki_hub: true
has_children: true
has_toc: false
redirect_from: ["/wiki/weapons/ammunition/"]
description: "Bullet and shell types, what each does to armor and flesh, and which weapons use them."
---

# Ammunition

The bullet tables distinguish standard (FMJ), flesh damage (HP) and armor piercing (AP), with tracer variants. Shotguns list buckshot and rifled slugs. Damage figures below use S3 inputs with the historical damage formula; current native equivalence is unverified.

[Limited Mode excludes HP and AP ammunition](https://store.steampowered.com/news/app/1867240/view/688648135317127221); this is a full-roster model, not an allowlist for that mode.

| Type | What it does | Against no armor | Against armor |
|---|---|---|---|
| Standard (FMJ) | The baseline round. | Baseline. | Baseline. |
| Flesh Damage (HP) | Does more damage to unarmored targets. | About double the standard damage. | Much weaker than standard against every armor class. |
| Armor Piercing (AP) | Model applies an armor scalar. | About 0.8 times the standard damage. | Overtakes standard from Medium for rifle calibers and the Deagle, and from Heavy for 9mm, .45 ACP and .45 Colt. The .50 Cal AMR 50 is an exception: AP never beats FMJ in this model. |

Tracer variants have the same damage as their base type in the model. The historical loading rule checks the magazine and caliber rather than an ammo tag; current native loading behavior has not been verified.

## Torso damage by type: 5.56mm rifle example

A-91 chambered in 5.56mm, upper torso hits:

| Ammo | No armor | Light | Medium | Heavy | Super heavy |
|---|---|---|---|---|---|
| Standard (FMJ) | 30.8 | 21.6 | 18.5 | 15.4 | 12.3 |
| Flesh Damage (HP) | 61.6 | 9.1 | 6.7 | 4.2 | 1.7 |
| Armor Piercing (AP) | 24.6 | 20.2 | 18.7 | 17.2 | 15.8 |

Head hits follow the same pattern with higher numbers. Armor covers different body parts by type; see [Weapon Damage](../game-features/Wardogs_WeaponDamage_v1.md).

## Shotgun shells

- Buckshot: 24.8 upper torso damage, no armor, per pellet, 8 pellets per shot.
- Rifled slug: 104.0 upper torso damage, no armor, per hit.

## Which weapons use each caliber

| | Caliber | Weapons |
|---|---|---|
| ![.308 Win]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox__308_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [.308 Win](ammunition/308-win.md) | [FAL](weapons/fal.md), [BMR-308](weapons/bmr-308.md), [M14](weapons/m14.md), [Evo-3 Ultra](weapons/evo-3-ultra.md), [MK22](weapons/mk22.md) |
| ![.45 ACP]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_45-ACP_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [.45 ACP](ammunition/45-acp.md) | [M1911](weapons/m1911.md), [Super-45](weapons/super-45.md) |
| ![.45 Colt]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_45-COLT_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [.45 Colt](ammunition/45-colt.md) | [Judge](weapons/judge.md) |
| ![.50 AE]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox__50-AE_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [.50 AE](ammunition/50-ae.md) | [Deagle](weapons/deagle.md) |
| ![.50 Cal]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox__50-AE_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [.50 Cal](ammunition/50-cal.md) | [AMR 50](weapons/amr-50.md) |
| ![12 gauge]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_12g_slug_green.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [12 gauge](ammunition/12-gauge.md) | [M500](weapons/m500.md), [MP43](weapons/mp43.md) |
| ![5.45x39mm]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_5_45x39_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [5.45x39mm](ammunition/5-45x39mm.md) | [AK74](weapons/ak74.md) |
| ![5.56x45mm]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_5_56x45mm_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [5.56x45mm](ammunition/5-56x45mm.md) | [A-91](weapons/a-91.md), [Bushmaster M17S](weapons/bushmaster-m17s.md), [Galil](weapons/galil.md), [KH-2002](weapons/kh-2002.md), [M4](weapons/m4.md), [T-21](weapons/t-21.md), [M249 SAW](weapons/m249-saw.md), [Scout Rifle TD](weapons/scout-rifle-td.md) |
| ![7.62x39mm]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_7_62x39mm_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [7.62x39mm](ammunition/7-62x39mm.md) | [TCX-SPR](weapons/tcx-spr.md), [SKS](weapons/sks.md) |
| ![7.62x54mm]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_7_62x54R_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [7.62x54mm](ammunition/7-62x54mm.md) | [SVD](weapons/svd.md), [PKM](weapons/pkm.md), [Mosin Nagant](weapons/mosin-nagant.md), [SV98](weapons/sv98.md) |
| ![9x19mm]({{ '/assets/img/icons/equipment-ammoboxes/T_UI_Icon_ammobox_9x19mm_FMJ.png' | relative_url }}){: .wiki-icon .wiki-icon-wide } | [9x19mm](ammunition/9x19mm.md) | [GGX 17](weapons/ggx-17.md), [GGX 18](weapons/ggx-18.md), [AMP-9](weapons/amp-9.md), [MP5](weapons/mp5.md), [PP-19 Bizon](weapons/pp-19-bizon.md), [PP-19 Vityaz](weapons/pp-19-vityaz.md) |

## See also

- [Choosing Ammo](guides/choosing-ammo.md), which round to load against each armor level
- [Ammo Packing](ammunition/ammo-packing.md), how long loading and unloading magazines takes
- [Armor](game-mechanics/armor.md)
- [Penetration and Ricochet](game-mechanics/penetration-and-ricochet.md)
- [Ballistics](game-mechanics/ballistics.md)

## Sources

- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json)
- [ammo-availability.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ammo-availability.json)
- [Weapon Damage](../game-features/Wardogs_WeaponDamage_v1.md)
- [Ammo Game Feature](../game-features/Wardogs_GameFeatures_Ammo_v2.md)
- [Round 45 wiki evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-a.md): tracer loading rule
