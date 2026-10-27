---
title: "Sights and Optics"
parent: "Weapons & Ammo"
description: "Every sight attachment with its magnification, ADS field of view, ADS time effect, zeroing range, sight entries, shop price, unlock level, the weapons that accept it and its reticle images."
---

# Sights and Optics

One row per sight attachment (29 in the data), generated from the item data and gameplay effects by [`_tools/sight_tables.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/sight_tables.py) into [`sights.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/sights.json). Pick sights for a weapon in the [Loadout Builder](loadout-builder.md); the attribute rules are on [Weapon attributes](Wardogs_WeaponAttributes_v1.md) and the slot structure on [Attachments and platforms](../game-features/Wardogs_AttachmentsPlatforms_v1.md); the per-weapon values are on [Weapons](Wardogs_Weapons_v2.md).

## How to read

Aiming narrows the camera angle: the aimed field of view (ADS FOV) is the base field of view divided by the magnification, a plain division of the angle. The base is your Field of view setting (default 90 degrees), except that a sight whose zoom test value is 3.25 or more uses 72 degrees whatever the setting is (for a variable-zoom scope the test value is its highest zoom). The figure in brackets is the apparent zoom against the normal 90 degree view, the tangent of half the normal angle over the tangent of half the aimed angle. This is derived from the camera code, not measured on screen; the evidence is in [round 46](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md) and [round 79](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round79-sight-zoom.md). "ADS time" is what the sight does to the weapon's aim time (a multiplier, an addition in seconds, or a fixed value). Zeroing range is in metres by the game code's reading (the data gives no unit); "weapon's own" means the sight does not set it. Shop price is the Weapon Shop price in cash; unlock levels and costs come from the class trees, where "Wardog level" is the career level and the others are class levels.

## Sights

<!-- sight_tables main -->
| | Sight | Magnification | ADS FOV (apparent zoom) | ADS time | Zeroing range (m) | Sight entries | Shop price | Unlock | Unlock cost | Id |
|---|---|---:|---|---|---|---|---:|---|---:|---|
| ![CGM4 Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_033.png' | relative_url }}){: width="48" } | CGM4 Scope | 1.2x | 75° (1.3x) | no change | weapon's own | Main sight | not in shop | no class gate |  | `ID_SGHT_033` |
| ![Compact P-1 Red Dot]({{ '/assets/img/icons/vendor-optics/T_UI_Weapons_SGHT_038.png' | relative_url }}){: width="48" } | Compact P-1 Red Dot | 1.2x | 75° (1.3x) | no change | min weapon's own, max same as min | Main sight | $480 | Wardog level 21 | $12,500 | `ID_SGHT_038` |
| ![Compact T-2 Red Dot]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_013.png' | relative_url }}){: width="48" } | Compact T-2 Red Dot | 1.2x | 75° (1.3x) | x0.9 | min weapon's own, max same as min | Main sight | $340 | Wardog level 17 | $5,000 | `ID_RedDot` |
| ![Four Reticle Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_016.png' | relative_url }}){: width="48" } | Four Reticle Reflex | 1.2x | 75° (1.3x) | x0.85 | min weapon's own, max same as min | Main sight | $580 | Infantry level 22 | $10,000 | `ID_SGHT_016` |
| ![Holographic Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_005.png' | relative_url }}){: width="48" } | Holographic Sight | 1.2x | 75° (1.3x) | x0.9 | min 100, max 100 | Main sight | not in shop | Medic level 6 | $20,000 | `ID_EotechHoloSight` |
| ![Kobra Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_009.png' | relative_url }}){: width="48" } | Kobra Reflex | 1.2x | 75° (1.3x) | x0.85 | min weapon's own, max same as min | Main sight | $520 | Wardog level 4 | $7,500 | `ID_SGHT_009` |
| ![Mini Reflex Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_025.png' | relative_url }}){: width="48" } | Mini Reflex Sight | 1.2x | 75° (1.3x) | x1.02 | min weapon's own, max same as min | Main sight | $200 | no class gate |  | `ID_SGHT_025` |
| ![MMGL Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_037.png' | relative_url }}){: width="48" } | MMGL Sight | 1.2x | 75° (1.3x) | no change | weapon's own | Main sight | not in shop | no class gate |  | `ID_SGHT_037` |
| ![OKP 7 Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_023.png' | relative_url }}){: width="48" } | OKP 7 Reflex | 1.2x | 75° (1.3x) | x0.85 | min weapon's own, max same as min | Main sight | $840 | Infantry level 26 | $30,000 | `ID_SGHT_023` |
| ![Vektor Frenix-X Micro Reflex Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_027.png' | relative_url }}){: width="48" } | Vektor Frenix-X Micro Reflex Sight | 1.2x | 75° (1.3x) | x0.87 | min weapon's own, max same as min | Main sight | $820 | Medic level 19 | $15,000 | `ID_SGHT_027` |
| ![Tricon 1.5x Compact Prism Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_026.png' | relative_url }}){: width="48" } | Tricon 1.5x Compact Prism Scope | 1.5x | 60° (1.73x) | x0.97 | min 100, max 200 | Main sight | $650 | Wardog level 26 | $10,000 | `ID_SGHT_026` |
| ![CantedIrons]({{ '/assets/img/icons/attachments-3d/T_UI_Icon_Attachment_RedDot_Textured_512x512.png' | relative_url }}){: width="48" } | CantedIrons | 2x | 45° (2.41x) | set to 0.1 s | weapon's own | Canted sight | not in shop | no class gate |  | `ID_CantedIrons` |
| ![CQ-2x Prism Combat Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_028.png' | relative_url }}){: width="48" } | CQ-2x Prism Combat Scope | 2x | 45° (2.41x) | x1.05 | min 100, max 300 | Main sight | $640 | Infantry level 12 | $15,000 | `ID_SGHT_028` |
| ![2.5x Combat Optic]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_008.png' | relative_url }}){: width="48" } | 2.5x Combat Optic | 2.5x | 36° (3.08x) | x1.05 | min 100, max 300 | Main sight | not in shop | Infantry level 17 | $10,000 | `ID_OPT_08` |
| ![Frontier 2.5x-10x Precision Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_032.png' | relative_url }}){: width="48" } | Frontier 2.5x-10x Precision Scope | 2.5x to 10x | 28.8° to 7.2° (3.89x to 15.89x) | x1.2 | min 100, max 1,000 | Main sight | $1,800 | Recon level 47 | $95,000 | `ID_SGHT_032` |
| ![PGO-7]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_034.png' | relative_url }}){: width="48" } | PGO-7 | 2.8x | 32.14° (3.47x) | x1.15 | min 10, max 10 | Main sight | $850 | Support level 12 | $10,000 | `ID_SGHT_034` |
|  | 3-6x Scope | 3x to 6x | 24° to 12° (4.7x to 9.51x) | +0.2 s | min 100, max 500 | Main sight | not in shop | no class gate |  | `ID_6xScope` |
| ![3x Tactical Prism Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_029.png' | relative_url }}){: width="48" } | 3x Tactical Prism Scope | 3x | 30° (3.73x) | x1.1 | min 100, max 300 | Main sight | $740 | Infantry level 33 | $15,000 | `ID_SGHT_029` |
| ![3x-6x LPVO Short Dot]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_011.png' | relative_url }}){: width="48" } | 3x-6x LPVO Short Dot | 3x to 6x | 24° to 12° (4.7x to 9.51x) | x1.12 | min 100, max 600 | Main sight | $860 | Recon level 11 | $15,000 | `ID_SGHT_011` |
| ![Leatherwood ART II]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_039.png' | relative_url }}){: width="48" } | Leatherwood ART II | 3x to 9x | 24° to 8° (4.7x to 14.3x) | x1.15 | min 100, max 800 | Main sight | $950 | Recon level 27 | $35,000 | `ID_SGHT_039` |
| ![Spitfire 3X]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_024.png' | relative_url }}){: width="48" } | Spitfire 3X | 3x | 30° (3.73x) | x1.1 | min 100, max 300 | Main sight | $790 | Wardog level 31 | $25,000 | `ID_3xScope` |
| ![PU 91/30 Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_040.png' | relative_url }}){: width="48" } | PU 91/30 Scope | 3.5x | 20.57° (5.51x) | x1.15 | min 100, max 800 | Main sight | $780 | Recon level 10 | $12,500 | `ID_SGHT_040` |
| ![4x Combat Prism Scope with Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_030.png' | relative_url }}){: width="48" } | 4x Combat Prism Scope with Reflex | 4x | 18° (6.31x) | x1.1 | min 100, max 400 | Main sight; Second sight (1.2x, ADS FOV 60° (1.73x), ADS time x1.05) | $880 | Support level 21 | $35,000 | `ID_SGHT_030` |
| ![4x Elcan Spectr]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_001.png' | relative_url }}){: width="48" } | 4x Elcan Spectr | 4x | 18° (6.31x) | x1.1 | min 100, max 400 | Main sight; Second sight (1.2x, ADS FOV 60° (1.73x), ADS time x1.05) | not in shop | Infantry level 43 | $15,000 | `ID_4xElcanSpectr` |
| ![4x Hybrid]({{ '/assets/img/icons/attachments-3d/T_UI_Icon_Attachment_4x_Optic_Textured_512x512.png' | relative_url }}){: width="48" } | 4x Hybrid | 4x | 18° (6.31x) | +0.35 s | weapon's own | Main sight | not in shop | no class gate |  | `ID_4xHybrid` |
| ![6-10x Scope MOA]({{ '/assets/img/icons/attachments-3d/T_UI_Icon_Attachment_10x_Optic_Textured_512x512.png' | relative_url }}){: width="48" } | 6-10x Scope MOA | 6x to 10x | 12° to 7.2° (9.51x to 15.89x) | x1.15 | min 100, max 1,000 | Main sight | not in shop | Recon level 19 | $45,000 | `ID_10xScopeMoa` |
| ![6-10x Scope MRAD]({{ '/assets/img/icons/attachments-3d/T_UI_Icon_Attachment_10x_Optic_Textured_512x512.png' | relative_url }}){: width="48" } | 6-10x Scope MRAD | 6x to 10x | 12° to 7.2° (9.51x to 15.89x) | x1.15 | min 100, max 1,000 | Main sight | not in shop | Recon level 28 | $40,000 | `ID_10xScope` |
| ![6x Marksman Scope + Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_036.png' | relative_url }}){: width="48" } | 6x Marksman Scope + Reflex | 6x | 12° (9.51x) | x1.12 | min 100, max 600 | Main sight; Second sight (1.2x, ADS FOV 60° (1.73x), ADS time x1.05) | $1,650 | Recon level 43 | $75,000 | `ID_SGHT_036` |
| ![6x Precision Rifle Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_031.png' | relative_url }}){: width="48" } | 6x Precision Rifle Scope | 6x | 12° (9.51x) | x1.15 | min 100, max 600 | Main sight | $680 | no class gate |  | `ID_SGHT_031` |
<!-- /sight_tables -->

A sight can carry several sight entries: the main sight, a second sight (the combo scopes switch to a short-range reflex sight) and a canted sight. The row's magnification, ADS FOV and ADS time are for the main entry; the other entries are listed in the "Sight entries" column.

## Which weapons accept which sight

Fit follows the sub-slot filters of each weapon's sight slot and its mounts. Launchers and a few rifles accept few or no sights.

<!-- sight_tables fits -->
| Weapon | Sights | Sights that fit |
|---|---:|---|
| 9K333 Verba | 0 | none |
| A-91 | 0 | none |
| AK74 | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| AMP-9 | 12 | 2.5x Combat Optic, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| AMR 50 | 24 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| BMR-308 | 17 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| Bushmaster M17S | 0 | none |
| Compound Bow | 0 | none |
| Deagle | 1 | Four Reticle Reflex |
| Evo-3 Ultra | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| FAL | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| Galil | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| GGX 17 | 0 | none |
| GGX 18 | 1 | Mini Reflex Sight |
| Judge | 0 | none |
| KH-2002 | 0 | none |
| M14 | 25 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, Leatherwood ART II, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| M1911 | 0 | none |
| M249 SAW | 13 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, Spitfire 3X, Tricon 1.5x Compact Prism Scope |
| M4 | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| M500 | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| MAAWS | 1 | CGM4 Scope |
| MGL-40 | 1 | MMGL Sight |
| MK22 | 24 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| Mosin Nagant | 1 | PU 91/30 Scope |
| MP43 | 0 | none |
| MP5 | 12 | 2.5x Combat Optic, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| PKM | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| PP-19 Bizon | 12 | 2.5x Combat Optic, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| PP-19 Vityaz | 12 | 2.5x Combat Optic, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| RPG-7 | 1 | PGO-7 |
| Scout Rifle TD | 24 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| SKS | 24 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| Super-45 | 12 | 2.5x Combat Optic, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| SV98 | 24 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| SVD | 24 | 2.5x Combat Optic, 3-6x Scope, 3x Tactical Prism Scope, 3x-6x LPVO Short Dot, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, 4x Hybrid, 6-10x Scope MOA, 6-10x Scope MRAD, 6x Marksman Scope + Reflex, 6x Precision Rifle Scope, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Frontier 2.5x-10x Precision Scope, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| T-21 | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |
| TCX-SPR | 16 | 2.5x Combat Optic, 3x Tactical Prism Scope, 4x Combat Prism Scope with Reflex, 4x Elcan Spectr, CGM4 Scope, Compact P-1 Red Dot, Compact T-2 Red Dot, CQ-2x Prism Combat Scope, Four Reticle Reflex, Holographic Sight, Kobra Reflex, MMGL Sight, OKP 7 Reflex, Spitfire 3X, Tricon 1.5x Compact Prism Scope, Vektor Frenix-X Micro Reflex Sight |

Fit no weapon: CantedIrons.
<!-- /sight_tables -->

## Reticles

Reticle images exist for the sights below; the list grows as more are extracted. A scope view marked approximate is drawn from the scope's material parameters, not a game texture.

<!-- sight_tables reticles -->
| Sight | Reticle | Image |
|---|---|---|
| CGM4 Scope | Scope view overlay (approximate, drawn from material parameters) | ![CGM4 Scope scope view]({{ '/assets/img/icons/scope-reticles/MI_Optics_SGHT_033_Lens.png' | relative_url }}){: width="96" } |
| Compact P-1 Red Dot | Scope view overlay (approximate, drawn from material parameters) | ![Compact P-1 Red Dot scope view]({{ '/assets/img/icons/scope-reticles/MI_Optics_SGHT_038_Lens.png' | relative_url }}){: width="96" } |
| Compact T-2 Red Dot | Main sight (HUD reticle) | ![Compact T-2 Red Dot reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_KobraSight_Greyscale.png' | relative_url }}){: width="96" } |
| Holographic Sight | Main sight (HUD reticle) | ![Holographic Sight reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_Holographic_Greyscale.png' | relative_url }}){: width="96" } |
| Kobra Reflex | Scope view overlay (approximate, drawn from material parameters) | ![Kobra Reflex scope view]({{ '/assets/img/icons/scope-reticles/MI_SGHT_009_Reticle.png' | relative_url }}){: width="96" } |
| Mini Reflex Sight | Scope view overlay (approximate, drawn from material parameters) | ![Mini Reflex Sight scope view]({{ '/assets/img/icons/scope-reticles/MI_SGHT_025_Reticle.png' | relative_url }}){: width="96" } |
| Vektor Frenix-X Micro Reflex Sight | Scope view overlay (approximate, drawn from material parameters) | ![Vektor Frenix-X Micro Reflex Sight scope view]({{ '/assets/img/icons/scope-reticles/MI_SGHT_027_Lens.png' | relative_url }}){: width="96" } |
| 2.5x Combat Optic | Main sight (HUD reticle) | ![2.5x Combat Optic reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_KobraSight_Greyscale.png' | relative_url }}){: width="96" } |
| 2.5x Combat Optic | Scope view overlay | ![2.5x Combat Optic scope view]({{ '/assets/img/icons/scope-reticles/T_UI_2_5x_Scope_SDF.png' | relative_url }}){: width="96" } |
| 3-6x Scope | Scope view overlay | ![3-6x Scope scope view]({{ '/assets/img/icons/scope-reticles/T_UI_1-6x_Scope_SDF.png' | relative_url }}){: width="96" } |
| 3x-6x LPVO Short Dot | Scope view overlay | ![3x-6x LPVO Short Dot scope view]({{ '/assets/img/icons/scope-reticles/T_UI_1-6x_Scope_SDF.png' | relative_url }}){: width="96" } |
| Spitfire 3X | Scope view overlay | ![Spitfire 3X scope view]({{ '/assets/img/icons/scope-reticles/T_UI_3x_Scope_SDF.png' | relative_url }}){: width="96" } |
| 4x Elcan Spectr | Main sight (HUD reticle) | ![4x Elcan Spectr reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_4X_Hybrid_Greyscale.png' | relative_url }}){: width="96" } |
| 4x Elcan Spectr | Second sight (HUD reticle) | ![4x Elcan Spectr reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_KobraSight_Greyscale.png' | relative_url }}){: width="96" } |
| 4x Elcan Spectr | Scope view overlay | ![4x Elcan Spectr scope view]({{ '/assets/img/icons/scope-reticles/T_UI_4x_Scope_SDF.png' | relative_url }}){: width="96" } |
| 4x Hybrid | Main sight (HUD reticle) | ![4x Hybrid reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_4X_Hybrid_Greyscale.png' | relative_url }}){: width="96" } |
| 6-10x Scope MRAD | Main sight (HUD reticle) | ![6-10x Scope MRAD reticle]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_10X_Greyscale.png' | relative_url }}){: width="96" } |
| 6x Marksman Scope + Reflex | Scope view overlay (approximate, drawn from material parameters) | ![6x Marksman Scope + Reflex scope view]({{ '/assets/img/icons/scope-reticles/MI_SGHT_036_Reticle.png' | relative_url }}){: width="96" } |
| 6x Precision Rifle Scope | Scope view overlay (approximate, drawn from material parameters) | ![6x Precision Rifle Scope scope view]({{ '/assets/img/icons/scope-reticles/MI_SGHT_031_Reticle.png' | relative_url }}){: width="96" } |
<!-- /sight_tables -->
