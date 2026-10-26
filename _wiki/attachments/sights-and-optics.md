---
title: "Sights and Optics"
redirect_from: ["/wiki/weapons/attachments-sights-and-optics/"]
parent: "Attachments"
description: "Red dots, holographic sights, scopes and iron sights for the top of the weapon, with their zoom, aim time and zeroing range values."
---

# Sights and Optics

| Sights and Optics | |
|---|---|
| **General** | |
| Slot | Sight (top of the weapon) |
| Parts in data | 29 |
| Fits on | Sight slot of the weapons listed in the table |
| **Performance** | |
| Stats changed | ADS zoom, aim time, zeroing range, sway (character) |
| **Availability** | |
| Shop prices | 19 of 29 parts |
| Shop price range | 200 to 1,800 |
| Season 2 | 3 new, 0 price changes |
| Internal name | `Item.Attachment.Sight` |
{: .wiki-infobox }

Sights sit on the top slot of a weapon. The data lists 29 of them and 28 fit a weapon. Every sight sets the weapon's ADS zoom, and most also change aim time and zeroing range. No sight changes recoil or spread in the data.

## What they change

- ADS zoom: set to a fixed value on 29 sights, from 1.2 (red dots and holographic sights) to 6 (the 6-10x scope). The number is a magnification factor: 2.5 means the view is magnified 2.5 times (derived from the game's code, not checked on screen). The sight's sway is divided by it, so higher magnification steadies the view more.
- Aim time: x0.85 to x1.2 (26 parts). This multiplies the time the weapon takes to come up to aim down the sights.
- Minimum zeroing range: set to 10 to 100 on 18 sights. The data gives no unit; the game code treats the number as metres (derived).
- Maximum zeroing range: set to 10 to 1000 on 18 sights. On 7 sights it follows the minimum zeroing range instead of a fixed value. The data gives no unit; the game code treats the number as metres (derived).
- Character side: weapon sway stabilisation time is multiplied by 1 to 1.5 on 5 sights and set to 1.6 on 8 others.

Zeroing range is the distance the sight is set for, bounded by the minimum and maximum. A weapon starts at the minimum, and the reset control returns it there (derived from the game's code; the game was not run).

### What the zoom does to the view

The ADS zoom narrows the camera's view by the sight's magnification. At full aim the on-screen field of view is your base field of view divided by the magnification, so a 2.5x sight on a 90 degree base gives 36 degrees. This is a plain division of the angle. The base is your Field of view setting in the default Affected aiming mode, or 72 degrees in Independent mode (see [Controls and settings](../game-mechanics/controls-and-settings.md)). The Affected mode follows your setting only at low magnification: the setting's own description says "below 3.25x". A sight of 3.25x or more uses 72 degrees as its base in both modes, so a 4x sight gives 18 degrees whatever your Field of view setting is. The 3.25 value is the larger of two numbers: the weapon's aiming magnification, and the highest magnification the sight can reach. They differ only for variable-zoom scopes. The Leatherwood ART II, for example, is listed at 3x but zooms up to 9x, so it counts as 9x for this test and uses 72 degrees even when it is turned down to 3x. The Frontier 2.5x-10x Precision Scope counts as 10x. A sight that cannot zoom just uses its own fixed magnification: the minimum and maximum zoom some of these sights still carry in their data (Spitfire 3X, Tricon, CQ-2x, 3x Tactical Prism, 4x Combat Prism, PGO-7, the 6x scopes and the PU 91/30) are ignored for the test (read from the game's code, not tested on screen). Iron sights count as a magnification of 1.2 plus the focus bonus.

The view narrows along the weapon's aiming curve and eases toward its target at the weapon's FOV interpolation speed, which is 20 per second unless the weapon sets its own. For weapons with that option set, the aimed view is never wider than the view you had before aiming; the data does not show which weapons set it. These rules come from reading the camera code and were not checked on screen.

### Effective magnification

The magnification number in the table above is not what you see on screen. The game narrows the view by dividing the viewing angle, not the size of the picture, so a sight's real picture magnification against the normal view is the tangent of half the normal angle divided by the tangent of half the aimed angle. The aimed angle is the starting angle divided by the sight's magnification, and the starting angle is your Field of view setting for low magnification sights but a fixed 72 degrees for sights of 3.25x and up. A 4x scope therefore aims at 72 / 4 = 18 degrees, which against a 90 degree normal view is about 6.3 times the size, not 4.

The 3x-6x LPVO Short Dot is named "1x-6x" in its item data, but its zoom runs from 3 to 6.

The table below uses the default settings: Field of view 90 and the Affected aiming mode. Variable zoom scopes are listed at both ends of their range. The combo sights are listed in both modes. A combo sight keeps the 72 degree start in its 1.2x reflex mode, so its reflex view is 60 degrees rather than 75. A scope that can zoom starts from 72 degrees across its whole range, even at its lowest zoom. The Leatherwood ART II at 3x is an example. These figures are derived from the camera code, not measured on screen. They hold at full aim, with no focus bonus, and the Independent aiming mode would put every sight on 72 degrees.

| Sight | Magnification used | Starting angle (degrees) | Aimed view (degrees) | Effective magnification |
|---|---:|---:|---:|---:|
| 3x-6x LPVO Short Dot (highest zoom) | 6 | 72 | 12 | 9.51 |
| 3x-6x LPVO Short Dot (lowest zoom) | 3 | 72 | 24 | 4.7 |
| 2.5x Combat Optic | 2.5 | 90 | 36 | 3.08 |
| 3-6x Scope (highest zoom) | 6 | 72 | 12 | 9.51 |
| 3-6x Scope (lowest zoom) | 3 | 72 | 24 | 4.7 |
| 3x Tactical Prism Scope | 3 | 90 | 30 | 3.73 |
| 4x Combat Prism Scope with Reflex (reflex mode) | 1.2 | 72 | 60 | 1.73 |
| 4x Combat Prism Scope with Reflex (scope mode) | 4 | 72 | 18 | 6.31 |
| 4x Elcan Spectr (reflex mode) | 1.2 | 72 | 60 | 1.73 |
| 4x Elcan Spectr (scope mode) | 4 | 72 | 18 | 6.31 |
| 4x Hybrid | 4 | 72 | 18 | 6.31 |
| 6-10x Scope MOA (highest zoom) | 10 | 72 | 7.2 | 15.89 |
| 6-10x Scope MOA (lowest zoom) | 6 | 72 | 12 | 9.51 |
| 6-10x Scope MRAD (highest zoom) | 10 | 72 | 7.2 | 15.89 |
| 6-10x Scope MRAD (lowest zoom) | 6 | 72 | 12 | 9.51 |
| 6x Marksman Scope + Reflex (reflex mode) | 1.2 | 72 | 60 | 1.73 |
| 6x Marksman Scope + Reflex (scope mode) | 6 | 72 | 12 | 9.51 |
| 6x Precision Rifle Scope | 6 | 72 | 12 | 9.51 |
| CantedIrons | 2 | 90 | 45 | 2.41 |
| CGM4 Scope | 1.2 | 90 | 75 | 1.3 |
| Compact P-1 Red Dot | 1.2 | 90 | 75 | 1.3 |
| Compact T-2 Red Dot | 1.2 | 90 | 75 | 1.3 |
| CQ-2x Prism Combat Scope | 2 | 90 | 45 | 2.41 |
| Four Reticle Reflex | 1.2 | 90 | 75 | 1.3 |
| Frontier 2.5x-10x Precision Scope (highest zoom) | 10 | 72 | 7.2 | 15.89 |
| Frontier 2.5x-10x Precision Scope (lowest zoom) | 2.5 | 72 | 28.8 | 3.89 |
| Holographic Sight | 1.2 | 90 | 75 | 1.3 |
| Kobra Reflex | 1.2 | 90 | 75 | 1.3 |
| Leatherwood ART II (highest zoom) | 9 | 72 | 8 | 14.3 |
| Leatherwood ART II (lowest zoom) | 3 | 72 | 24 | 4.7 |
| Mini Reflex Sight | 1.2 | 90 | 75 | 1.3 |
| MMGL Sight | 1.2 | 90 | 75 | 1.3 |
| OKP 7 Reflex | 1.2 | 90 | 75 | 1.3 |
| PGO-7 | 2.8 | 90 | 32.1 | 3.47 |
| PU 91/30 Scope | 3.5 | 72 | 20.6 | 5.51 |
| Spitfire 3X | 3 | 90 | 30 | 3.73 |
| Tricon 1.5x Compact Prism Scope | 1.5 | 90 | 60 | 1.73 |
| Vektor Frenix-X Micro Reflex Sight | 1.2 | 90 | 75 | 1.3 |

## Parts

Prices come from the Weapon Shop data. The sight with no weapon is listed in the table with No weapon; see the notes below.

| | Part | Fits | Shop price | Main effect |
|---|---|---|---:|---|
| ![2.5x Combat Optic]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_008.png' | relative_url }}){: .wiki-icon } | 2.5x Combat Optic | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | Not in shop data | aim time x1.05; ADS zoom set to 2.5; min zeroing range set to 100; max zeroing range set to 300 |
|  | 3-6x Scope | AMR 50, BMR-308, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | Not in shop data | ADS zoom set to 3; aim time +0.2; max zeroing range set to 500; min zeroing range set to 100; ADS zoom set to 3 |
| ![3x Tactical Prism Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_029.png' | relative_url }}){: .wiki-icon } | 3x Tactical Prism Scope | AK74, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, PKM, SKS, SV98, SVD, Scout Rifle TD, T-21, TCX-SPR | 740 | ADS zoom set to 3; min zeroing range set to 100; max zeroing range set to 300; aim time x1.1 |
| ![3x-6x LPVO Short Dot]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_011.png' | relative_url }}){: .wiki-icon } | 3x-6x LPVO Short Dot | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | 860 | ADS zoom set to 3; aim time x1.12; max zeroing range set to 600; min zeroing range set to 100; ADS zoom set to 3; sway stabilise time set to 1.6 |
| ![4x Combat Prism Scope with Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_030.png' | relative_url }}){: .wiki-icon } | 4x Combat Prism Scope with Reflex | AK74, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, PKM, SKS, SV98, SVD, Scout Rifle TD, T-21, TCX-SPR | 880 | max zeroing range set to 400; min zeroing range set to 100; aim time x1.1; ADS zoom set to 4; aim time x1.05; ADS zoom set to 1.2; sway stabilise time x1.5 |
|  | 4x Elcan Spectr | AK74, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, PKM, SKS, SV98, SVD, Scout Rifle TD, T-21, TCX-SPR | Not in shop data | max zeroing range set to 400; min zeroing range set to 100; aim time x1.1; ADS zoom set to 4; aim time x1.05; ADS zoom set to 1.2; sway stabilise time x1.5 |
| ![4x Hybrid]({{ '/assets/img/icons/other-sights-reticles/T_Reticle_4X_Hybrid_Greyscale.png' | relative_url }}){: .wiki-icon } | 4x Hybrid | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | Not in shop data | ADS zoom set to 4; aim time +0.35 |
| ![6-10x Scope MOA]({{ '/assets/img/icons/attachments-3d/T_UI_Icon_Attachment_10x_Optic_Textured_512x512.png' | relative_url }}){: .wiki-icon } | 6-10x Scope MOA | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | Not in shop data | aim time x1.15; ADS zoom set to 6; max zeroing range set to 1000; min zeroing range set to 100; sway stabilise time set to 1.6; sway rotation stabilise x1.8; sway translation stabilise x1.4 |
| ![6-10x Scope MRAD]({{ '/assets/img/icons/attachments-3d/T_UI_Icon_Attachment_10x_Optic_Textured_512x512.png' | relative_url }}){: .wiki-icon } | 6-10x Scope MRAD | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | Not in shop data | aim time x1.15; ADS zoom set to 6; max zeroing range set to 1000; min zeroing range set to 100; sway stabilise time set to 1.6; sway rotation stabilise x1.8; sway translation stabilise x1.4 |
| ![6x Marksman Scope + Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_036.png' | relative_url }}){: .wiki-icon } | 6x Marksman Scope + Reflex | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | 1650 | ADS zoom set to 6; aim time x1.12; max zeroing range set to 600; min zeroing range set to 100; aim time x1.05; ADS zoom set to 1.2; sway stabilise time set to 1.6 |
| ![6x Precision Rifle Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_031.png' | relative_url }}){: .wiki-icon } | 6x Precision Rifle Scope | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | 680 | ADS zoom set to 6; aim time x1.15; max zeroing range set to 600; min zeroing range set to 100; ADS zoom set to 6; sway stabilise time set to 1.6; sway rotation stabilise x1.8; sway translation stabilise x1.4 |
|  | CantedIrons | No weapon | Not in shop data | aim time set to 0.1; ADS zoom set to 2 |
| ![CGM4 Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_033.png' | relative_url }}){: .wiki-icon } | CGM4 Scope | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MAAWS, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | No price in shop data | ADS zoom set to 1.2 |
| ![Compact P-1 Red Dot]({{ '/assets/img/icons/vendor-optics/T_UI_Weapons_SGHT_038.png' | relative_url }}){: .wiki-icon } | Compact P-1 Red Dot | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 480 | ADS zoom set to 1.2; max zeroing range follows min zeroing range |
| ![Compact T-2 Red Dot]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_013.png' | relative_url }}){: .wiki-icon } | Compact T-2 Red Dot | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 340 | ADS zoom set to 1.2; aim time x0.9; max zeroing range follows min zeroing range |
| ![CQ-2x Prism Combat Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_028.png' | relative_url }}){: .wiki-icon } | CQ-2x Prism Combat Scope | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 640 | aim time x1.05; ADS zoom set to 2; min zeroing range set to 100; max zeroing range set to 300 |
| ![Four Reticle Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_016.png' | relative_url }}){: .wiki-icon } | Four Reticle Reflex | AK74, AMP-9, AMR 50, BMR-308, Deagle, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 580 | ADS zoom set to 1.2; aim time x0.85; max zeroing range follows min zeroing range |
| ![Frontier 2.5x-10x Precision Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_032.png' | relative_url }}){: .wiki-icon } | Frontier 2.5x-10x Precision Scope | AMR 50, M14, MK22, SKS, SV98, SVD, Scout Rifle TD | 1800 | aim time x1.2; ADS zoom set to 2.5; max zeroing range set to 1000; min zeroing range set to 100; sway stabilise time set to 1.6; sway rotation stabilise x1.8; sway translation stabilise x1.4 |
| ![Holographic Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_005.png' | relative_url }}){: .wiki-icon } | Holographic Sight | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | Not in shop data | ADS zoom set to 1.2; aim time x0.9; min zeroing range set to 100; max zeroing range set to 100 |
| ![Kobra Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_009.png' | relative_url }}){: .wiki-icon } | Kobra Reflex | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 520 | ADS zoom set to 1.2; aim time x0.85; max zeroing range follows min zeroing range |
| ![Leatherwood ART II]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_039.png' | relative_url }}){: .wiki-icon } | Leatherwood ART II | M14 | 950 | ADS zoom set to 3; aim time x1.15; max zeroing range set to 800; min zeroing range set to 100; sway stabilise time set to 1.6; sway rotation stabilise x1.8; sway translation stabilise x1.4 |
| ![Mini Reflex Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_025.png' | relative_url }}){: .wiki-icon } | Mini Reflex Sight | GGX 18 | 200 | ADS zoom set to 1.2; aim time x1.02; max zeroing range follows min zeroing range |
| ![MMGL Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_037.png' | relative_url }}){: .wiki-icon } | MMGL Sight | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MGL-40, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | No price in shop data | ADS zoom set to 1.2 |
| ![OKP 7 Reflex]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_023.png' | relative_url }}){: .wiki-icon } | OKP 7 Reflex | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 840 | ADS zoom set to 1.2; aim time x0.85; max zeroing range follows min zeroing range |
| ![PGO-7]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_034.png' | relative_url }}){: .wiki-icon } | PGO-7 | RPG-7 | 850 | ADS zoom set to 2.8; aim time x1.15; min zeroing range set to 10; max zeroing range set to 10 |
| ![PU 91/30 Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_040.png' | relative_url }}){: .wiki-icon } | PU 91/30 Scope | Mosin Nagant | 780 | ADS zoom set to 3.5; aim time x1.15; max zeroing range set to 800; min zeroing range set to 100; sway stabilise time set to 1.6; sway rotation stabilise x1.8; sway translation stabilise x1.4 |
| ![Spitfire 3X]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_024.png' | relative_url }}){: .wiki-icon } | Spitfire 3X | AK74, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, PKM, SKS, SV98, SVD, Scout Rifle TD, T-21, TCX-SPR | 790 | ADS zoom set to 3; min zeroing range set to 100; max zeroing range set to 300; aim time x1.1; sway stabilise time x1.35 |
| ![Tricon 1.5x Compact Prism Scope]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_026.png' | relative_url }}){: .wiki-icon } | Tricon 1.5x Compact Prism Scope | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M249 SAW, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 650 | aim time x0.97; ADS zoom set to 1.5; min zeroing range set to 100; max zeroing range set to 200 |
| ![Vektor Frenix-X Micro Reflex Sight]({{ '/assets/img/icons/vendor-optics/T_UI_Vendor_SGHT_027.png' | relative_url }}){: .wiki-icon } | Vektor Frenix-X Micro Reflex Sight | AK74, AMP-9, AMR 50, BMR-308, Evo-3 Ultra, FAL, Galil, M14, M4, M500, MK22, MP5, PKM, PP-19 Bizon, PP-19 Vityaz, SKS, SV98, SVD, Scout Rifle TD, Super-45, T-21, TCX-SPR | 820 | ADS zoom set to 1.2; aim time x0.87; max zeroing range follows min zeroing range |

## Parts that fit no weapon

1 part in the data can't be fitted: no weapon's slot accepts them, so their modifiers never apply in game. They are still listed in the table above with "No weapon" in the Fits column.

CantedIrons.

## Season 2 changes

The Season 2 notes list no removed parts in this category.

New in Season 2: 3 parts: Compact P-1 Red Dot, Leatherwood ART II, PU 91/30 Scope.

No shop price changes for this category are listed in the Season 2 notes.

Three existing sights changed values in Season 2 (the stat names suggest what these values control; the data does not describe them):

- Holographic Sight: sight camera offset on one weapon changed from -8 to -7.

- 3x-6x LPVO Short Dot: scope mask scale changed from 0.015 to 0.02 on each of its three axes.

- OKP 7 Reflex: sight camera offset on one weapon changed from -8 to -2.

The Season 2 notes also list a fourth sight folder that has no part data in this export.

## See also

- [Attachments](../attachments.md), the list of attachment categories and what each slot does
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md), how the recoil and spread multipliers combine
- [Weapons](../weapons.md)
- [Muzzle Devices](muzzle-devices.md)

## Sources

- [Attachments and Platforms](../../game-features/Wardogs_AttachmentsPlatforms_v1.md): every attachment item, the weapons and slots that take it, and the modifiers it applies.
- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): display names, shop prices and component names.
- [Gameplay Effect Values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md): the modifier values behind each effect.
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): slot, part and effect data.
- [Season 2 changes: weapons and ammo](../../season-2-changes/weapons-ammo.md): Season 2 prices, new parts and sight values.
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the ADS zoom as a magnification factor and the sight's ADS time
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
