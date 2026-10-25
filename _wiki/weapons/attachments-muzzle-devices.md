---
title: "Muzzle Devices"
parent: "Weapons"
group: "Attachments"
description: "Muzzle devices (brakes, flash hiders, suppressors and chokes) and the recoil, spread and aim time changes each one makes."
---

# Muzzle Devices

| Muzzle Devices | |
|---|---|
| **General** | |
| Slot | Muzzle (end of the barrel) |
| Parts in data | 56 |
| Fits on | Barrel muzzle slot; the table lists the weapons whose barrel takes the device |
| **Performance** | |
| Stats changed | Vertical and horizontal recoil, spread, aim time |
| **Availability** | |
| Shop prices | 46 of 56 parts |
| Shop price range | 350 to 1,400 |
| Season 2 | 9 new, 23 price changes |
| Internal name | `Item.Attachment.Muzzle` |
{: .wiki-infobox }

Muzzle devices fit the end of a barrel: flash hiders, brakes, compensators, suppressors and shotgun chokes. The data lists 56 of them, and all of them fit a weapon. 55 change weapon numbers; the one that changes nothing is the M14 standard muzzle.

## What they change

- Vertical recoil: x0.74 to x1.02 (55 parts).
- Horizontal recoil: x0.78 to x1.05 (55 parts).
- Spread: x0.88 to x1 (55 parts).
- Aim time: x0.97 to x1.15 (55 parts).

Lower recoil and spread are better. Aim time is a time multiplier, so a value above 1 adds time to aim. A muzzle device changes no character-side stat in the data.

The two shotgun chokes on the M500 (Improved Cylinder Choke and Full Choke) replace the shotgun pellet pattern. Improved Cylinder Choke narrows the outer edge of the pellet cone from 1.56 to 1.36 degrees, and about 26 percent of pellets land in the tight inner cluster (20 percent without it). Full Choke narrows the outer edge to 0.95 degrees, and 34 percent of pellets land in the inner cluster (derived from the game's values).

The M14 standard muzzle carries the suppressor sound cue and a smaller flash, but no stat change.

Each device also stores a muzzle flash size and a sound cue. Only the stat changes are described here.

## Parts

Muzzle devices fit through a barrel, not straight onto the weapon. Fits lists the weapons whose barrel takes the device. Prices come from the Weapon Shop data.

| Part | Fits | Shop price | Main effect |
|---|---|---:|---|
| .30 Cal SS Phosphate Muzzle Brake | M14 | 950 | vertical recoil x0.85; horizontal recoil x1.05; spread x0.88; aim time x1.05 |
| .30 Cal Steel Black Flash Hider | M14 | 730 | aim time x0.97 |
| .45 ACP Pistol Compensator | M1911 | 990 | vertical recoil x0.86; horizontal recoil x0.98; spread x0.98; aim time x1.03 |
| .50 Cal Heavy Suppressor | AMR 50 | 1250 | vertical recoil x0.9; horizontal recoil x0.94; spread x0.9; aim time x1.12 |
| 12 Gauge Suppressor | M500 | Not in shop data | vertical recoil x0.88; horizontal recoil x0.95; spread x0.92; aim time x1.1 |
| 3 Prong Flash Hider | Galil, M249 SAW, M4, T-21 | 820 | spread x0.99; aim time x0.98 |
| 3-Chamber Brake | Galil, M249 SAW, M4, T-21 | 1000 | vertical recoil x0.8; horizontal recoil x0.98; spread x0.96; aim time x1.06 |
| AMP-9 9x19 Suppressor | AMP-9 | 1110 | vertical recoil x0.94; horizontal recoil x0.95; spread x0.92; aim time x1.08 |
| AMP-9 Tactical Flash Hider | AMP-9 | 550 | spread x0.99; aim time x0.98 |
| AMR 50 Cal Muzzle Brake | AMR 50 | 1380 | vertical recoil x0.8; horizontal recoil x0.92; spread x0.99; aim time x1.05 |
| AR Multi-Caliber Suppressor | FAL, Galil, M249 SAW, M4, T-21 | 1200 | vertical recoil x0.88; horizontal recoil x0.93; spread x0.9; aim time x1.1 |
| Ballista Brake | AK74, AMP-9, GGX 17, GGX 18, Galil, M4, MP5, PP-19 Bizon, PP-19 Vityaz, T-21 | 380 | vertical recoil x1.02; horizontal recoil x0.8; spread x0.95; aim time x1.04 |
| Birdcage Flash Hider | AK74 | 600 | spread x0.99; aim time x0.98 |
| BMR-308 Flash Hider | BMR-308 | 930 | spread x0.99; aim time x0.98 |
| BMR-308 Suppressor | BMR-308 | 1080 | vertical recoil x0.95; horizontal recoil x0.96; spread x0.92; aim time x1.08 |
| Clutch Lok Muzzle Brake | TCX-SPR | 1100 | vertical recoil x0.9; horizontal recoil x1.05; spread x0.9; aim time x1.02 |
| Constrictor Brake | BMR-308, Evo-3 Ultra, FAL, MK22, Mosin Nagant, PKM, SKS, SV98, TCX-SPR | 760 | vertical recoil x1.01; horizontal recoil x0.83; spread x0.97; aim time x1.03 |
| CQB 74 Brake | AK74 | Not in shop data | vertical recoil x0.8; horizontal recoil x0.97; spread x0.96; aim time x1.04 |
| Cross Rifle Muzzle Brake | TCX-SPR | 780 | vertical recoil x0.92; horizontal recoil x0.94; spread x0.9; aim time x1.08 |
| Deadeye Flash Hider | BMR-308, Evo-3 Ultra, FAL, MK22, Mosin Nagant, PKM, SKS, SV98, SVD, Scout Rifle TD, TCX-SPR | 400 | No stat change in data |
| DTK-1 Brake | SKS | 810 | vertical recoil x0.8; horizontal recoil x0.9; spread x0.95; aim time x1.06 |
| Dual Port Brake | AMP-9, GGX 17, GGX 18, MP5, PP-19 Bizon, PP-19 Vityaz | 720 | vertical recoil x0.82; horizontal recoil x0.96; spread x0.95; aim time x1.05 |
| Eclipse Flash Hider | AMP-9, GGX 17, GGX 18, MP5, PP-19 Bizon, PP-19 Vityaz | 580 | spread x0.99; aim time x0.98 |
| FAL Flash Hider | FAL | 1250 (hidden) | spread x0.97; aim time x0.98 |
| Flow-Through .308 Suppressor | MK22 | 1020 | vertical recoil x0.96; horizontal recoil x0.97; spread x0.9; aim time x1.05 |
| Full Choke | M500 | 1150 | aim time x1.02 |
| Ghost LITE Muzzle Brake | Super-45 | 970 | vertical recoil x0.78; horizontal recoil x0.88; spread x0.98; aim time x1.04 |
| GOL Multi-Caliber Suppressor | AMR 50, BMR-308, MK22, Mosin Nagant, SKS, SV98, SVD | Not in shop data | vertical recoil x0.84; horizontal recoil x0.9; spread x0.88; aim time x1.15 |
| Hexagon 762 Suppressor | Mosin Nagant, PKM, SKS, SV98, SVD | Not in shop data | vertical recoil x0.82; horizontal recoil x0.9; spread x0.89; aim time x1.12 |
| Hexagon Brake | Galil, M4, T-21 | 350 | vertical recoil x0.99; horizontal recoil x0.78; spread x0.96; aim time x1.05 |
| Improved Cylinder Choke | M500 | 540 | aim time x1.02 |
| M14 standard muzzle | M14 | No price in shop data | No stat change in data |
| M500 Sabre Brake | M500 | 740 | vertical recoil x0.8; horizontal recoil x1.02; spread x0.95; aim time x1.07 |
| MP5 Flash Hider | MP5 | 1150 (hidden) | spread x0.92; aim time x0.98 |
| Orpheus Max Brake | M249 SAW, PKM | 980 | vertical recoil x0.74; horizontal recoil x0.9; spread x0.98; aim time x1.07 |
| PBS-4 Suppressor | AK74 | Not in shop data | vertical recoil x0.86; horizontal recoil x0.92; spread x0.88; aim time x1.12 |
| PP-19 Vityaz Flash Hider | PP-19 Vityaz | 750 | spread x0.99; aim time x0.98 |
| PP-19-01 Vityaz 9x19 Suppressor | PP-19 Vityaz | 1290 | vertical recoil x0.97; horizontal recoil x0.97; spread x0.95; aim time x1.1 |
| QD-5 Suppressor | MP5 | 1130 | vertical recoil x0.94; horizontal recoil x0.95; spread x0.9; aim time x1.08 |
| QD-5 Suppressor | Evo-3 Ultra | No price in shop data | vertical recoil x0.94; horizontal recoil x0.95; spread x0.9; aim time x1.08 |
| RC-556 Suppressor | Galil, M249 SAW, M4, T-21 | 1310 | vertical recoil x0.88; horizontal recoil x0.92; spread x0.88; aim time x1.12 |
| SG Multi-Caliber Suppressor | AMP-9, GGX 17, GGX 18, M1911, MP5, PP-19 Bizon, PP-19 Vityaz, Super-45 | Not in shop data | vertical recoil x0.9; horizontal recoil x0.94; spread x0.91; aim time x1.08 |
| Sig Default | TCX-SPR | No price in shop data | vertical recoil x0.94; horizontal recoil x0.95; spread x0.9; aim time x1.08 |
| SL7i-BL Suppressor | Evo-3 Ultra | 1400 | vertical recoil x0.95; horizontal recoil x0.94; spread x0.9; aim time x1.1 |
| Slicktap Brake | SKS | 940 | vertical recoil x0.8; horizontal recoil x1.03; spread x0.96; aim time x1.08 |
| Slotted Flash Hider | PKM | 840 | spread x0.99; aim time x0.98 |
| SRD762TI-QD | TCX-SPR | 1350 | vertical recoil x0.93; horizontal recoil x0.94; spread x0.9; aim time x1.1 |
| SRVV Brake | Mosin Nagant, PKM, SV98, SVD | 1330 | vertical recoil x0.88; horizontal recoil x0.82; spread x0.95; aim time x1.05 |
| STRELIX Suppressor | Scout Rifle TD | 1000 | vertical recoil x0.96; horizontal recoil x0.96; spread x0.93; aim time x1.04 |
| Super-45 Flash Hider | Super-45 | 860 | spread x0.99; aim time x0.98 |
| Suppressor T8L1 Scout | FAL | 1000 (hidden) | vertical recoil x0.96; horizontal recoil x0.96; spread x0.93; aim time x1.07 |
| SVD 7.62x54R Brake | SVD | 650 | vertical recoil x0.82; horizontal recoil x0.98; spread x0.97; aim time x1.03 |
| TGP-A Suppressor 5.45 | AK74 | Not in shop data | vertical recoil x0.9; horizontal recoil x0.94; spread x0.91; aim time x1.1 |
| Three Port Brake | BMR-308, Evo-3 Ultra, FAL, MK22, TCX-SPR | 1040 | vertical recoil x0.78; horizontal recoil x0.96; spread x0.96; aim time x1.06 |
| TopComp Brake | Galil, M249 SAW, M4, T-21 | 770 | vertical recoil x0.82; horizontal recoil x0.98; spread x0.96; aim time x1.05 |
| Tread Brake | M249 SAW | 620 | vertical recoil x0.86; horizontal recoil x0.98; spread x0.97; aim time x1.03 |

## Season 2 changes

The Season 2 notes list no removed parts in this category.

New in Season 2: 9 parts: .30 Cal SS Phosphate Muzzle Brake, .30 Cal Steel Black Flash Hider, Clutch Lok Muzzle Brake, Cross Rifle Muzzle Brake, M14 standard muzzle, QD-5 Suppressor, SL7i-BL Suppressor, SRD762TI-QD, Sig Default.

Shop price changes (Season 1 to Season 2):

| Part | Season 1 | Season 2 | Change |
|---|---:|---:|---:|
| .45 ACP Pistol Compensator | 1,030 | 990 | -40 (-3.9%) |
| .50 Cal Heavy Suppressor | 1,420 | 1,250 | -170 (-12.0%) |
| 3 Prong Flash Hider | 1,000 | 820 | -180 (-18.0%) |
| 3-Chamber Brake | 1,080 | 1,000 | -80 (-7.4%) |
| AMP-9 9x19 Suppressor | 1,130 | 1,110 | -20 (-1.8%) |
| AMR 50 Cal Muzzle Brake | 1,600 | 1,380 | -220 (-13.8%) |
| AR Multi-Caliber Suppressor | 400 | 1,200 | +800 (+200.0%) |
| Birdcage Flash Hider | 900 | 600 | -300 (-33.3%) |
| BMR-308 Flash Hider | 1,280 | 930 | -350 (-27.3%) |
| BMR-308 Suppressor | 1,200 | 1,080 | -120 (-10.0%) |
| DTK-1 Brake | 820 | 810 | -10 (-1.2%) |
| Eclipse Flash Hider | 700 | 580 | -120 (-17.1%) |
| Flow-Through .308 Suppressor | 1,120 | 1,020 | -100 (-8.9%) |
| Full Choke | 1,400 | 1,150 | -250 (-17.9%) |
| Orpheus Max Brake | 1,020 | 980 | -40 (-3.9%) |
| PP-19 Vityaz Flash Hider | 800 | 750 | -50 (-6.2%) |
| PP-19-01 Vityaz 9x19 Suppressor | 1,450 | 1,290 | -160 (-11.0%) |
| QD-5 Suppressor | 1,170 | 1,130 | -40 (-3.4%) |
| RC-556 Suppressor | 1,550 | 1,310 | -240 (-15.5%) |
| Slotted Flash Hider | 960 | 840 | -120 (-12.5%) |
| SRVV Brake | 1,470 | 1,330 | -140 (-9.5%) |
| Super-45 Flash Hider | 1,050 | 860 | -190 (-18.1%) |
| Three Port Brake | 1,180 | 1,040 | -140 (-11.9%) |

## See also

- [Attachments](attachments.md), the list of attachment categories and what each slot does
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md), how the recoil and spread multipliers combine
- [Weapons](../weapons.md)
- [Barrels](attachments-barrels.md), the barrels that carry the muzzle slot

## Sources

- [Attachments and Platforms](../../game-features/Wardogs_AttachmentsPlatforms_v1.md): every attachment item, the weapons and slots that take it, and the modifiers it applies.
- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): display names, shop prices and component names.
- [Gameplay Effect Values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the modifier values behind each effect.
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): slot, part and effect data.
- [Season 2 changes: weapons and ammo](../../season-2-changes/weapons-ammo.md): Season 2 prices, new parts and sight values.
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): M500 choke replacement values, M14 muzzle
