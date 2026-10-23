---
title: "Weapons & Ammo changes"
parent: "Season 2 Changes"
nav_order: 1
description: "Weapon stats, vendor prices, attachments and aim assist: 162 assets added, 16 removed, 192 modified, 11 moved, 1,469 property changes."
---

# Weapons & Ammo changes

Weapons, ammo, attachments and aim assist: what changed between Season 1 and Season 2.

- **Added:** 162 assets
- **Removed:** 16 assets (all aim assist curves)
- **Modified with real changes:** 192 assets (233 more are noise-only and not listed: only renamed keys or shifted references)
- **Moved:** 11 assets (the Mosin folder moved to `WEPN_017`)
- **Property changes:** 1,469 (includes 989 removed values)

Vector rows show the signed change on each axis, for example `X −0.4, Y −0.4`.

## Headline changes

### Weapon stats (`DA_*_Stats`)

#### Random firing animation offset (42 rows, 21 weapons)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_AK74M_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.0, 0.05) | (-0.15, -0.05) | X −0.15, Y −0.1 |
| DA_AK74M_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.15, -0.05) | (0.0, 0.05) | X +0.15, Y +0.1 |
| DA_KH2002_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.2, 0.2) | (-0.2, -0.2) | X −0.4, Y −0.4 |
| DA_KH2002_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.2, -0.2) | (0.2, 0.2) | X +0.4, Y +0.4 |
| DA_M12G_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.35) | (-0.35, -0.35) | X −0.7, Y −0.7 |
| DA_M12G_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.35) | (0.35, 0.35) | X +0.7, Y +0.7 |
| DA_M249_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.5, 0.5) | (-0.5, -0.5) | X −1.0, Y −1.0 |
| DA_M249_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.5, -0.5) | (0.5, 0.5) | X +1.0, Y +1.0 |
| DA_M4_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.1) | (-0.35, -0.1) | X −0.7, Y −0.2 |
| DA_M4_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.1) | (0.35, 0.1) | X +0.7, Y +0.2 |
| DA_MP43_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.35) | (-0.35, -0.35) | X −0.7, Y −0.7 |
| DA_MP43_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.35) | (0.35, 0.35) | X +0.7, Y +0.7 |
| DA_MP9_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.3, 0.3) | (-0.3, -0.3) | X −0.6, Y −0.6 |
| DA_MP9_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.3, -0.3) | (0.3, 0.3) | X +0.6, Y +0.6 |
| DA_RFB_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.1) | (-0.35, -0.1) | X −0.7, Y −0.2 |
| DA_RFB_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.1) | (0.35, 0.1) | X +0.7, Y +0.2 |
| DA_SKS_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.2, 0.2) | (-0.2, -0.2) | X −0.4, Y −0.4 |
| DA_SKS_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.2, -0.2) | (0.2, 0.2) | X +0.4, Y +0.4 |
| DA_SMG_03_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.3, 0.3) | (1.0, -1.0) | X +0.7, Y −1.3 |
| DA_SMG_03_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (1.0, -1.0) | (0.3, 0.3) | X −0.7, Y +1.3 |
| DA_SV98_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.2, 0.2) | — | removed |
| DA_SV98_Stats | MaximumRandomFiringAnimationOffset (X, Y) | — | (0.2, 0.2) | added |
| DA_SVDM_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.5, 0.5) | (0.2, 0.2) | X −0.3, Y −0.3 |
| DA_SVDM_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (0.2, 0.2) | (0.5, 0.5) | X +0.3, Y +0.3 |
| DA_TAR21_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.2, 0.2) | (-0.2, -0.2) | X −0.4, Y −0.4 |
| DA_TAR21_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.2, -0.2) | (0.2, 0.2) | X +0.4, Y +0.4 |
| DA_Vector_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.3, 0.3) | (-0.3, -0.3) | X −0.6, Y −0.6 |
| DA_Vector_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.3, -0.3) | (0.3, 0.3) | X +0.6, Y +0.6 |
| DA_WEPN_026_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.3, 0.3) | (-0.3, -0.3) | X −0.6, Y −0.6 |
| DA_WEPN_026_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.3, -0.3) | (0.3, 0.3) | X +0.6, Y +0.6 |
| DA_WEPN_027_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.1) | (-0.35, -0.1) | X −0.7, Y −0.2 |
| DA_WEPN_027_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.1) | (0.35, 0.1) | X +0.7, Y +0.2 |
| DA_WEPN_028_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.3, 0.3) | (-0.3, -0.3) | X −0.6, Y −0.6 |
| DA_WEPN_028_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.3, -0.3) | (0.3, 0.3) | X +0.6, Y +0.6 |
| DA_WEPN_029_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.0, 0.05) | (-0.15, -0.05) | X −0.15, Y −0.1 |
| DA_WEPN_029_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.15, -0.05) | (0.0, 0.05) | X +0.15, Y +0.1 |
| DA_WEPN_030_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.1) | (-0.35, -0.1) | X −0.7, Y −0.2 |
| DA_WEPN_030_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.1) | (0.35, 0.1) | X +0.7, Y +0.2 |
| DA_WEPN_033_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.2, 0.2) | (-0.2, -0.2) | X −0.4, Y −0.4 |
| DA_WEPN_033_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.2, -0.2) | (0.2, 0.2) | X +0.4, Y +0.4 |
| DA_WEPN_035_Stats | MinimumRandomFiringAnimationOffset (X, Y) | (0.35, 0.1) | (-0.35, -0.1) | X −0.7, Y −0.2 |
| DA_WEPN_035_Stats | MaximumRandomFiringAnimationOffset (X, Y) | (-0.35, -0.1) | (0.35, 0.1) | X +0.7, Y +0.2 |

[All 232 FiringAnimationOffset changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=weapons-ammo&q=FiringAnimationOffset)

### Recoil pattern (79 points, 4 weapons)

Shown: the 24 points with the largest change. The other 55 points are in the browser.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_SKS_Stats | RecoilPattern[6] (X, Y) | (0.03, 1.4) | (-2.398731, 3.5) | X −2.428731, Y +2.1 |
| DA_SVDM_Stats | RecoilPattern[6] (X, Y) | (-1.259, 1.309) | (0.944, 2.374) | X +2.203, Y +1.065 |
| DA_SKS_Stats | RecoilPattern[3] (X, Y) | (0.136, 1.45) | (-1.287133, 3.625) | X −1.423133, Y +2.175 |
| DA_SKS_Stats | RecoilPattern[4] (X, Y) | (0.122, 1.44) | (-0.377998, 3.6) | X −0.499998, Y +2.16 |
| DA_SKS_Stats | RecoilPattern[2] (X, Y) | (0.118, 1.42) | (-0.437593, 3.55) | X −0.555593, Y +2.13 |
| DA_SKS_Stats | RecoilPattern[5] (X, Y) | (0.078, 1.42) | (-1.197064, 3.55) | X −1.275064, Y +2.13 |
| DA_SKS_Stats | RecoilPattern[7] (X, Y) | (-0.003, 1.38) | (-1.426486, 3.45) | X −1.423486, Y +2.07 |
| DA_SKS_Stats | RecoilPattern[8] (X, Y) | (-0.017, 1.36) | (0.613115, 3.4) | X +0.630115, Y +2.04 |
| DA_SKS_Stats | RecoilPattern[9] (X, Y) | (0.0, 1.345) | (-0.809759, 3.3625) | X −0.809759, Y +2.0175 |
| DA_SKS_Stats | RecoilPattern[10] (X, Y) | (0.032, 1.33) | (-1.497126, 3.325) | X −1.529126, Y +1.995 |
| DA_SKS_Stats | RecoilPattern[11] (X, Y) | (0.078, 1.32) | (-0.918821, 3.3) | X −0.996821, Y +1.98 |
| DA_SKS_Stats | RecoilPattern[12] (X, Y) | (0.1, 1.32) | (-0.407489, 3.3) | X −0.507489, Y +1.98 |
| DA_SKS_Stats | RecoilPattern[13] (X, Y) | (0.091, 1.3) | (-0.689072, 3.25) | X −0.780072, Y +1.95 |
| DA_SKS_Stats | RecoilPattern[1] (X, Y) | (0.103, 1.28) | (-0.034409, 3.2) | X −0.137409, Y +1.92 |
| DA_SKS_Stats | RecoilPattern[14] (X, Y) | (0.063, 1.28) | (-0.382609, 3.2) | X −0.445609, Y +1.92 |
| DA_SKS_Stats | RecoilPattern[15] (X, Y) | (0.015, 1.26) | (-0.786865, 3.15) | X −0.801865, Y +1.89 |
| DA_SKS_Stats | RecoilPattern[16] (X, Y) | (-0.029, 1.24) | (-0.203181, 3.1) | X −0.174181, Y +1.86 |
| DA_RFB_Stats | RecoilPattern[2] (X, Y) | (0.158, 1.245) | (0.55, 3.06) | X +0.392, Y +1.815 |
| DA_SKS_Stats | RecoilPattern[17] (X, Y) | (-0.047, 1.2) | (0.010702, 3.0) | X +0.057702, Y +1.8 |
| DA_SVDM_Stats | RecoilPattern[7] (X, Y) | (0.856, 1.787) | (-0.913, 2.005) | X −1.769, Y +0.218 |
| DA_SKS_Stats | RecoilPattern[18] (X, Y) | (-0.031, 1.16) | (-0.564315, 2.9) | X −0.533315, Y +1.74 |
| DA_SVDM_Stats | RecoilPattern[3] (X, Y) | (0.227, 1.888) | (-1.385, 3.601) | X −1.612, Y +1.713 |
| DA_RFB_Stats | RecoilPattern[4] (X, Y) | (0.235, 1.375) | (0.4, 3.06) | X +0.165, Y +1.685 |
| DA_RFB_Stats | RecoilPattern[3] (X, Y) | (0.216, 1.47) | (0.7, 3.105) | X +0.484, Y +1.635 |

[All 150 recoil pattern changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=weapons-ammo&q=RecoilPattern)

### Other weapon stats

On `DA_SKS_Stats`, `ViewKickMagnitudeMultiplier` was removed and `SuppressionMultiplier` was added. These are two separate properties, not a rename.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_MMGL_Stats | InitialBulletSpeed | 10000.0 | 7500.0 | −2500.0 (−25.0%) |
| DA_WEPN_017_Stats | Name | DA_Mosin_Stats | DA_WEPN_017_Stats | changed |
| DA_WEPN_017_Stats | Package | /Mosin/Data/DA_Mosin_Stats | /WEPN_017/Data/DA_WEPN_017_Stats | changed |
| DA_AK74M_Stats | SuppressionMultiplier | — | 1.05 | added |
| DA_LMG_02_Stats | SuppressionMultiplier | 0.45 | 0.9 | +0.45 (+100.0%) |
| DA_M249_Stats | SuppressionMultiplier | — | 1.25 | added |
| DA_M2Browning_Stats | SuppressionMultiplier | — | 0.8 | added |
| DA_M4_Stats | SuppressionMultiplier | — | 0.95 | added |
| DA_MK22_Stats | SuppressionMultiplier | — | 1.6 | added |
| DA_SKS_Stats | SuppressionMultiplier | — | 1.1 | added |
| DA_SR_04_Stats | SuppressionMultiplier | — | 2.0 | added |
| DA_SV98_Stats | SuppressionMultiplier | — | 1.5 | added |
| DA_SVDM_Stats | SuppressionMultiplier | 0.4 | 0.8 | +0.4 (+100.0%) |
| DA_Vector_Stats | SuppressionMultiplier | — | 0.8 | added |
| DA_WEPN_017_Stats | SuppressionMultiplier | — | 1.5 | added |
| DA_WEPN_035_Stats | SuppressionMultiplier | — | 1.5 | added |
| DA_RFB_Stats | ViewKickMagnitudeMultiplier | 1.15 | — | removed |
| DA_SKS_Stats | ViewKickMagnitudeMultiplier | 1.1 | — | removed |
| DA_SVDM_Stats | ViewKickMagnitudeMultiplier | 0.7 | — | removed |
| DA_WEPN_028_Stats | ViewKickMagnitudeMultiplier | 1.1 | 1.15 | +0.05 (+4.5%) |

### Vector distance falloff curve

Season 2 adds two keys, `Keys[3]` at Time 10000.0 (Value 0.4) and `Keys[4]` at Time 15000.0 (Value 0.3). Keys 1 and 2 also change interpolation and tangents. The Season 1 key at Time 120000.0 (Value 0.2) is unchanged.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[1].ArriveTangent | -8.594104e-05 | 0.0 | +8.6e-05 (+100.0%) |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[1].InterpMode | RCIM_Cubic | RCIM_Linear | changed |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[1].LeaveTangent | -8.4807776e-05 | 0.0 | +8.5e-05 (+100.0%) |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[1].TangentMode | RCTM_User | RCTM_Auto | changed |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[2].ArriveTangent | -1.18046255e-05 | 0.0 | +1.2e-05 (+100.0%) |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[2].InterpMode | RCIM_Cubic | RCIM_Linear | changed |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[2].LeaveTangent | -1.1804622e-05 | 0.0 | +1.2e-05 (+100.0%) |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[2].TangentMode | RCTM_User | RCTM_Auto | changed |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[3] (added key: Time 10000.0, Value 0.4) | — | added | added |
| DA_Vector_Stats | DistanceDamageFalloffCurve Keys[4] (added key: Time 15000.0, Value 0.3) | — | added | added |

### Vendor prices (46 rows)

Each row is one vendor price in a `DT_*` data table. Sorted from largest decrease to largest increase.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_WeaponVendor_Ext_AR_01 | Price (AK74M) | 1600.0 | 800.0 | −800.0 (−50.0%) |
| DT_VendorData_Ext_MUZL_039 | Price (MUZL_039) | 900.0 | 600.0 | −300.0 (−33.3%) |
| DT_VendorData_Ext_MUZL_055 | Price (MUZL_055) | 1280.0 | 930.0 | −350.0 (−27.3%) |
| DT_VendorData_Ext_FGRP_007 | Price (FGRP_007) | 1150.0 | 840.0 | −310.0 (−27.0%) |
| DT_VendorData_Ext_MUZL_046 | Price (MUZL_046) | 1050.0 | 860.0 | −190.0 (−18.1%) |
| DT_VendorData_Ext_MUZL_013 | Price (MUZL_013) | 1000.0 | 820.0 | −180.0 (−18.0%) |
| DT_VendorData_Ext_MUZL_045 | Price (MUZL_045) | 1400.0 | 1150.0 | −250.0 (−17.9%) |
| DT_VendorData_Ext_MUZL_037 | Price (MUZL_037) | 700.0 | 580.0 | −120.0 (−17.1%) |
| DT_VendorData_Ext_WEPN_027 | Price (WEPN_027) | 900.0 | 750.0 | −150.0 (−16.7%) |
| DT_VendorData_Ext_MUZL_032 | Price (MUZL_032) | 1550.0 | 1310.0 | −240.0 (−15.5%) |
| DT_VendorData_Ext_MUZL_048 | Price (MUZL_048) | 1600.0 | 1380.0 | −220.0 (−13.8%) |
| DT_VendorData_Ext_FGRP_014 | Price (FGRP_014) | 1100.0 | 950.0 | −150.0 (−13.6%) |
| DT_VendorData_Ext_MUZL_038 | Price (MUZL_038) | 960.0 | 840.0 | −120.0 (−12.5%) |
| DT_VendorData_Ext_MUZL_049 | Price (MUZL_049) | 1420.0 | 1250.0 | −170.0 (−12.0%) |
| DT_VendorData_Ext_MUZL_030 | Price (MUZL_030) | 1180.0 | 1040.0 | −140.0 (−11.9%) |
| DT_VendorData_Ext_MUZL_053 | Price (MUZL_053) | 1450.0 | 1290.0 | −160.0 (−11.0%) |
| DT_VendorData_Ext_MUZL_056 | Price (MUZL_056) | 1200.0 | 1080.0 | −120.0 (−10.0%) |
| DT_VendorData_Weapon_RPG7 | Price (RPG7) | 2000.0 | 1800.0 | −200.0 (−10.0%) |
| DT_VendorData_Ext_MUZL_041 | Price (MUZL_041) | 1470.0 | 1330.0 | −140.0 (−9.5%) |
| DT_VendorData_Ext_WEPN_029 | Price (WEPN_029) | 2200.0 | 2000.0 | −200.0 (−9.1%) |
| DT_VendorData_Ext_MUZL_057 | Price (MUZL_057) | 1120.0 | 1020.0 | −100.0 (−8.9%) |
| DT_VendorData_Weapon_LMG_02 | Price (LMG_02) | 4500.0 | 4100.0 | −400.0 (−8.9%) |
| DT_VendorData_Ext_WEPN_030 | Price (WEPN_030) | 6500.0 | 6000.0 | −500.0 (−7.7%) |
| DT_WeaponVendor_EXT_Launcher_02 | Price (CGM4) | 2600.0 | 2400.0 | −200.0 (−7.7%) |
| DT_VendorData_Ext_MUZL_027 | Price (MUZL_027) | 1080.0 | 1000.0 | −80.0 (−7.4%) |
| DT_VendorData_Ext_FGRP_006 | Price (FGRP_006) | 770.0 | 720.0 | −50.0 (−6.5%) |
| DT_VendorData_Ext_MUZL_054 | Price (MUZL_054) | 800.0 | 750.0 | −50.0 (−6.2%) |
| DT_VendorData_Ext_FGRP_016 | Price (FGRP_016) | 680.0 | 640.0 | −40.0 (−5.9%) |
| DT_VendorData_Ext_FGRP_018 | Price (FGRP_018) | 720.0 | 680.0 | −40.0 (−5.6%) |
| DT_VendorData_Ext_MUZL_029 | Price (MUZL_029) | 1020.0 | 980.0 | −40.0 (−3.9%) |
| DT_VendorData_Ext_MUZL_050 | Price (MUZL_050) | 1030.0 | 990.0 | −40.0 (−3.9%) |
| DT_VendorData_Ext_MUZL_058 | Price (MUZL_058) | 1170.0 | 1130.0 | −40.0 (−3.4%) |
| DT_VendorData_Ext_MUZL_051 | Price (MUZL_051) | 1130.0 | 1110.0 | −20.0 (−1.8%) |
| DT_VendorData_Ext_MUZL_028 | Price (MUZL_028) | 820.0 | 810.0 | −10.0 (−1.2%) |
| DT_VendorData_Ext_FGRP_010 | Price (FGRP_010) | 800.0 | 810.0 | +10.0 (+1.2%) |
| DT_VendorData_Weapon_RFB | Price (RFB) | 6000.0 | 6250.0 | +250.0 (+4.2%) |
| DT_VendorData_Ext_WEPN_035 | Price (WEPN_035) | 1100.0 | 1200.0 | +100.0 (+9.1%) |
| DT_VendorData_Ext_C4 | Price (C4Trigger) | 550.0 | 650.0 | +100.0 (+18.2%) |
| DT_VendorData_Ext_WEPN_028 | Price (WEPN_028) | 1500.0 | 1800.0 | +300.0 (+20.0%) |
| DT_WeaponsVendor_EXT_WEPN_032 | Price (WEPN_032) | 800.0 | 1000.0 | +200.0 (+25.0%) |
| DT_WeaponVendor_EXT_Launcher_01 | Price (MMGL) | 6000.0 | 7500.0 | +1500.0 (+25.0%) |
| DT_VendorData_Weapon_MP9 | Price (MP9) | 900.0 | 1375.0 | +475.0 (+52.8%) |
| DT_VendorData_Weapon_SR_04 | Price (SR_04) | 8800.0 | 14800.0 | +6000.0 (+68.2%) |
| DT_WeaponsVendor_EXT_TAR21 | Price (TAR21) | 600.0 | 1200.0 | +600.0 (+100.0%) |
| DT_WeaponVendor_EXT_SMG_01 | Price (Vector) | 2600.0 | 5600.0 | +3000.0 (+115.4%) |
| DT_WeaponVendor_MUZL_012 | Price (MZL_07) | 400.0 | 1200.0 | +800.0 (+200.0%) |

### Bipod and stance values (7 items, 2 groups)

Items: `ID_FGP_04`, `ID_FGRP_009`, `ID_FGRP_010`, `ID_FGRP_011`, `ID_FGRP_013`. The table shows the first item; the others have identical values. 21 values each.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| ID_FGP_04 | Stand · BipodMountLocationVerticalDistance | 75.0 | 40.0 | −35.0 (−46.7%) |
| ID_FGP_04 | Stand · MaxBipodToPlayerHorizontalDistance | 37.5 | 75.0 | +37.5 (+100.0%) |
| ID_FGP_04 | Stand · MaxLedgeAngle | -15.0 | 15.0 | +30.0 (+200.0%) |
| ID_FGP_04 | Stand · MaxTransitionDuration | 0.2 | 0.5 | +0.3 (+150.0%) |
| ID_FGP_04 | Stand · MinBipodToPlayerHorizontalDistance | 40.0 | 37.5 | −2.5 (−6.2%) |
| ID_FGP_04 | Stand · MinLedgeAngle | 15.0 | -15.0 | −30.0 (−200.0%) |
| ID_FGP_04 | Stand · MinTransitionDuration | 0.5 | 0.2 | −0.3 (−60.0%) |
| ID_FGP_04 | Crouch · BipodMountLocationVerticalDistance | 75.0 | 40.0 | −35.0 (−46.7%) |
| ID_FGP_04 | Crouch · MaxBipodToPlayerHorizontalDistance | 37.5 | 75.0 | +37.5 (+100.0%) |
| ID_FGP_04 | Crouch · MaxLedgeAngle | -15.0 | 15.0 | +30.0 (+200.0%) |
| ID_FGP_04 | Crouch · MaxTransitionDuration | 0.2 | 0.5 | +0.3 (+150.0%) |
| ID_FGP_04 | Crouch · MinBipodToPlayerHorizontalDistance | 40.0 | 37.5 | −2.5 (−6.2%) |
| ID_FGP_04 | Crouch · MinLedgeAngle | 15.0 | -15.0 | −30.0 (−200.0%) |
| ID_FGP_04 | Crouch · MinTransitionDuration | 0.5 | 0.2 | −0.3 (−60.0%) |
| ID_FGP_04 | Prone · BipodMountLocationVerticalDistance | 75.0 | 60.0 | −15.0 (−20.0%) |
| ID_FGP_04 | Prone · MaxBipodToPlayerHorizontalDistance | 37.5 | 75.0 | +37.5 (+100.0%) |
| ID_FGP_04 | Prone · MaxLedgeAngle | -15.0 | 15.0 | +30.0 (+200.0%) |
| ID_FGP_04 | Prone · MaxTransitionDuration | 0.5 | 1.0 | +0.5 (+100.0%) |
| ID_FGP_04 | Prone · MinBipodToPlayerHorizontalDistance | 60.0 | 37.5 | −22.5 (−37.5%) |
| ID_FGP_04 | Prone · MinLedgeAngle | 15.0 | -15.0 | −30.0 (−200.0%) |
| ID_FGP_04 | Prone · MinTransitionDuration | 1.0 | 0.5 | −0.5 (−50.0%) |

Items: `ID_FGRP_008`, `ID_FGRP_012`. The same 21 values change as in the table above, except these 4, which differ:

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| ID_FGRP_008 | Stand · MaxTransitionDuration | 0.35 | 0.7 | +0.35 (+100.0%) |
| ID_FGRP_008 | Stand · MinTransitionDuration | 0.7 | 0.35 | −0.35 (−50.0%) |
| ID_FGRP_008 | Crouch · MaxTransitionDuration | 0.35 | 0.7 | +0.35 (+100.0%) |
| ID_FGRP_008 | Crouch · MinTransitionDuration | 0.7 | 0.35 | −0.35 (−50.0%) |

Other numeric item values:

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| ID_4xElcanSpectr | AttachmentData.SightsData[Key=S_Aim02].Value.SightCameraOffsetOverridePerWeapon[0] | -30.0 | -1.6 | +28.4 (+94.7%) |
| ID_EotechHoloSight | AttachmentData.SightsData[Key=S_Aim01].Value.SightCameraOffsetOverridePerWeapon[0] | -8.0 | -7.0 | +1.0 (+12.5%) |
| ID_OPT_08 | AttachmentData.SightsData[Key=S_Aim01].Value.SightCameraOffsetOverridePerWeapon[0] | -20.548815 | -3.9 | +16.648815 (+81.0%) |
| ID_SGHT_011 | AttachmentData.SightsData[Key=S_Aim01].Value.ScopeMaskScale.X | 0.015 | 0.02 | +0.005 (+33.3%) |
| ID_SGHT_011 | AttachmentData.SightsData[Key=S_Aim01].Value.ScopeMaskScale.Y | 0.015 | 0.02 | +0.005 (+33.3%) |
| ID_SGHT_011 | AttachmentData.SightsData[Key=S_Aim01].Value.ScopeMaskScale.Z | 0.015 | 0.02 | +0.005 (+33.3%) |
| ID_SGHT_016 | AttachmentData.SightsData[Key=S_Aim01].Value.SightCameraOffsetOverridePerWeapon[0] | 10.0 | -5.0 | −15.0 (−150.0%) |
| ID_SGHT_023 | AttachmentData.SightsData[Key=S_Aim01].Value.SightCameraOffsetOverridePerWeapon[0] | -8.0 | -2.0 | +6.0 (+75.0%) |
| ID_SR_04 | TimeAfterFireToRechamber | 0.24 | 0.2 | −0.04 (−16.7%) |
| ID_SV98 | TimeAfterFireToRechamber | 0.3 | 0.08 | −0.22 (−73.3%) |

### Animation sets (10 rows)

15 boolean flags (`bOverrideLength`) also changed and are in the browser.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| AnimSet_AK74M | Animations[Animation.Asset.Weapon.Fire].Value.ItemBlendOutTime | 0.1 | 0.0 | −0.1 (−100.0%) |
| AnimSet_Glock17 | Animations[Inspect].Value.OverrideLength | 1.0 | 13.35 | +12.35 (+1235.0%) |
| AnimSet_SVDM | Animations[Inspect].Value.OverrideLength | 1.0 | 8.9 | +7.9 (+790.0%) |
| AnimSet_WEPN_026 | Animations[Inspect].Value.OverrideLength | 1.0 | 13.35 | +12.35 (+1235.0%) |
| AnimSet_WEPN_027 | Animations[Inspect].Value.OverrideLength | 1.0 | 13.35 | +12.35 (+1235.0%) |
| AnimSet_WEPN_028 | Animations[Inspect].Value.OverrideLength | 1.0 | 10.8 | +9.8 (+980.0%) |
| AnimSet_WEPN_030 | Animations[Inspect].Value.OverrideLength | 1.0 | 13.8 | +12.8 (+1280.0%) |
| AnimSet_WEPN_032 | Animations[Inspect].Value.OverrideLength | 1.0 | 13.35 | +12.35 (+1235.0%) |
| AnimSet_WEPN_035 | Animations[Animation.Asset.Weapon.Reload.Empty].Value.OverrideLength | 5.0 | 3.0 | −2.0 (−40.0%) |
| AnimSet_WEPN_035 | Animations[Animation.Asset.Weapon.Reload.Tactical].Value.OverrideLength | 1.25 | 3.0 | +1.75 (+140.0%) |

### Aim assist settings (141 numeric rows across 7 assets)

Shown: the 30 largest changes by percentage (values that start at 0 are listed first). The other 111 rows are in the browser.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_AimAssistSettings_Melee | PullInnerStrengthHip | 0.0 | 1.0 | +1.0 (n/a) |
| DA_AimAssistSettings_Melee | SlowInnerStrengthHip | 0.0 | 0.36 | +0.36 (n/a) |
| DA_AimAssistSettings_SR | PullInnerStrengthAds | 0.0 | 2.0 | +2.0 (n/a) |
| DA_AimAssistSettings_SR | SlowInnerStrengthAds | 0.0 | 0.4 | +0.4 (n/a) |
| DA_AimAssistSettings_AR | unnamed property (`_aaabkejidmenonabgon`) | 0.5 | 2.5 | +2.0 (+400.0%) |
| DA_AimAssistSettings_LMG | unnamed property (`_aaabkejidmenonabgon`) | 0.5 | 2.5 | +2.0 (+400.0%) |
| DA_AimAssistSettings_Pistol | unnamed property (`_aaabkejidmenonabgon`) | 0.5 | 2.5 | +2.0 (+400.0%) |
| DA_AimAssistSettings_Shotgun | unnamed property (`_aaabkejidmenonabgon`) | 0.5 | 2.5 | +2.0 (+400.0%) |
| DA_AimAssistSettings_SR | unnamed property (`_aaabkejidmenonabgon`) | 0.5 | 2.5 | +2.0 (+400.0%) |
| DA_AimAssistSettings_AR | SlowInnerStrengthAds | 0.19 | 0.6 | +0.41 (+215.8%) |
| DA_AimAssistSettings_LMG | SlowInnerStrengthAds | 0.19 | 0.6 | +0.41 (+215.8%) |
| DA_AimAssistSettings_SR | AssistInnerReticleWidth | 400.0 | 1200.0 | +800.0 (+200.0%) |
| DA_AimAssistSettings_AR | PullInnerStrengthAds | 0.7 | 2.0 | +1.3 (+185.7%) |
| DA_AimAssistSettings_SR | AssistInnerReticleHeight | 340.0 | 960.0 | +620.0 (+182.4%) |
| DA_AimAssistSettings_LMG | PullInnerStrengthHip | 0.36 | 1.0 | +0.64 (+177.8%) |
| DA_AimAssistSettings_Pistol | PullInnerStrengthHip | 0.36 | 1.0 | +0.64 (+177.8%) |
| DA_AimAssistSettings_Shotgun | PullInnerStrengthHip | 0.36 | 1.0 | +0.64 (+177.8%) |
| DA_AimAssistSettings_LMG | PullInnerStrengthAds | 0.8 | 2.0 | +1.2 (+150.0%) |
| DA_AimAssistSettings_SMG | PullInnerStrengthHip | 0.44 | 1.0 | +0.56 (+127.3%) |
| DA_AimAssistSettings_LMG | SlowLerpInRate | 5.0 | 10.0 | +5.0 (+100.0%) |
| DA_AimAssistSettings_Melee | PullInnerStrengthAds | 1.5 | 0.0 | −1.5 (−100.0%) |
| DA_AimAssistSettings_Melee | SlowInnerStrengthAds | 0.19 | 0.0 | −0.19 (−100.0%) |
| DA_AimAssistSettings_Pistol | SlowLerpInRate | 5.0 | 10.0 | +5.0 (+100.0%) |
| DA_AimAssistSettings_Shotgun | SlowLerpInRate | 5.0 | 10.0 | +5.0 (+100.0%) |
| DA_AimAssistSettings_SMG | SlowLerpInRate | 5.0 | 10.0 | +5.0 (+100.0%) |
| DA_AimAssistSettings_SR | PullInnerStrengthHip | 0.28 | 0.0 | −0.28 (−100.0%) |
| DA_AimAssistSettings_SR | SlowInnerStrengthHip | 2.0 | 0.0 | −2.0 (−100.0%) |
| DA_AimAssistSettings_SR | SlowLerpInRate | 5.0 | 10.0 | +5.0 (+100.0%) |
| DA_AimAssistSettings_SR | ReticleDepth | 20000.0 | 40000.0 | +20000.0 (+100.0%) |
| DA_AimAssistSettings_SR | AssistOuterReticleWidth | 1860.0 | 3600.0 | +1740.0 (+93.5%) |

[All 214 aim assist settings changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=weapons-ammo&q=AimAssistSettings)

### Aim assist curves (69 time and value rows across 14 curves)

Shown: the 30 largest changes by percentage (values that start at 0 are listed first). The other 39 rows, tangent values, and the removed and added keys are in the browser.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| C_AimAssistPullStrengthDistanceCurve_AR_ADS | Keys[1].Value | 0.0 | 1.0 | +1.0 (n/a) |
| C_AimAssistPullStrengthDistanceCurve_LMG_ADS | Keys[1].Value | 0.0 | 1.0 | +1.0 (n/a) |
| C_AimAssistPullStrengthDistanceCurve_Pistol_ADS | Keys[1].Value | 0.0 | 1.0 | +1.0 (n/a) |
| C_AimAssistPullStrengthDistanceCurve_Shotgun_ADS | Keys[1].Value | 0.0 | 1.0 | +1.0 (n/a) |
| C_AimAssistPullStrengthDistanceCurve_SMG_ADS | Keys[1].Value | 0.0 | 1.0 | +1.0 (n/a) |
| C_AimAssistSlowStrengthDistanceCurve_AR_ADS | Keys[1].Value | 0.0 | 0.8 | +0.8 (n/a) |
| C_AimAssistSlowStrengthDistanceCurve_LMG_ADS | Keys[1].Value | 0.0 | 0.8 | +0.8 (n/a) |
| C_AimAssistSlowStrengthDistanceCurve_SMG_ADS | Keys[1].Value | 0.0 | 0.8 | +0.8 (n/a) |
| C_AimAssistSlowStrengthDistanceCurve_Sniper | Keys[1].Value | 0.0 | 1.0 | +1.0 (n/a) |
| C_AimAssistSlowStrengthDistanceCurvePistol_ADS | Keys[1].Value | 0.0 | 0.8 | +0.8 (n/a) |
| C_AimAssistSlowStrengthDistanceCurveShotgun_ADS | Keys[1].Value | 0.0 | 0.8 | +0.8 (n/a) |
| C_AimAssistSlowStrengthDistanceCurve_Sniper | Keys[2].Time | 300.0 | 27500.0 | +27200.0 (+9066.7%) |
| C_AimAssistPullStrengthDistanceCurve_AR_ADS | Keys[2].Time | 400.0 | 22500.0 | +22100.0 (+5525.0%) |
| C_AimAssistPullStrengthDistanceCurve_Shotgun_ADS | Keys[2].Time | 400.0 | 17500.0 | +17100.0 (+4275.0%) |
| C_AimAssistPullStrengthDistanceCurve_SMG_ADS | Keys[2].Time | 400.0 | 12500.0 | +12100.0 (+3025.0%) |
| C_AimAssistPullStrengthDistanceCurve_Pistol_ADS | Keys[2].Time | 400.0 | 10000.0 | +9600.0 (+2400.0%) |
| C_AimAssistSlowStrengthDistanceCurve_Sniper | Keys[3].Time | 1200.0 | 30000.0 | +28800.0 (+2400.0%) |
| C_AimAssistSlowStrengthDistanceCurve_LMG_ADS | Keys[3].Time | 1200.0 | 20000.0 | +18800.0 (+1566.7%) |
| C_AimAssistSlowStrengthDistanceCurveShotgun_ADS | Keys[3].Time | 1200.0 | 17500.0 | +16300.0 (+1358.3%) |
| C_AimAssistSlowStrengthDistanceCurve_AR_ADS | Keys[1].Time | 150.0 | 2000.0 | +1850.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurve_LMG_ADS | Keys[1].Time | 150.0 | 2000.0 | +1850.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurve_LMG_ADS | Keys[2].Time | 300.0 | 4000.0 | +3700.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurve_SMG_ADS | Keys[1].Time | 150.0 | 2000.0 | +1850.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurve_SMG_ADS | Keys[2].Time | 300.0 | 4000.0 | +3700.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurve_Sniper | Keys[1].Time | 150.0 | 2000.0 | +1850.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurvePistol_ADS | Keys[1].Time | 150.0 | 2000.0 | +1850.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurvePistol_ADS | Keys[2].Time | 300.0 | 4000.0 | +3700.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurveShotgun_ADS | Keys[1].Time | 150.0 | 2000.0 | +1850.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurveShotgun_ADS | Keys[2].Time | 300.0 | 4000.0 | +3700.0 (+1233.3%) |
| C_AimAssistSlowStrengthDistanceCurve_SMG_ADS | Keys[3].Time | 1200.0 | 15000.0 | +13800.0 (+1150.0%) |

Added `DefaultValue` on 3 curves: `C_AimAssistSlowStrengthDistanceCurve_LMG_ADS` (0.0), `C_AimAssistSlowStrengthDistanceCurvePistol_ADS` (0.0), `C_AimAssistSlowStrengthDistanceCurveShotgun_ADS` (0.0).

Removed key entries: 36 (across 13 curves). Added key entries: 0.

[All 0 aim assist curve changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=weapons-ammo&q=AimAssistCurve)

### New in Season 2 (162 assets)

| Asset | Type | Identification |
|---|---|---|
| [AnimSet_FGRP_019](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/Data/AnimSet_FGRP_019.json) | BHAnimationSet | — |
| [AnimSet_FGRP_020](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/Data/AnimSet_FGRP_020.json) | BHAnimationSet | — |
| [AnimSet_Molotov](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/AnimSet_Molotov.json) | BHAnimationSet | — |
| [AnimSet_WEPN_031](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/AnimSet_WEPN_031.json) | BHAnimationSet | — |
| [AnimSet_WEPN_034](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/AnimSet_WEPN_034.json) | BHAnimationSet | — |
| [AnimSet_WEPN_036](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/AnimSet_WEPN_036.json) | BHAnimationSet | — |
| [AnimSet_WEPN_037](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/AnimSet_WEPN_037.json) | BHAnimationSet | — |
| [ID_BARL_046](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_046/Content/Data/ID_BARL_046.json) | BHInventoryItemDefinition | Id.Item.BARL_046 |
| [ID_BARL_047](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_047/Content/Data/ID_BARL_047.json) | BHInventoryItemDefinition | Id.Item.BARL_047 |
| [ID_BARL_048](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_048/Content/Data/ID_BARL_048.json) | BHInventoryItemDefinition | Id.Item.BARL_048 |
| [ID_BARL_049](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_049/Content/Data/ID_BARL_049.json) | BHInventoryItemDefinition | Id.Item.BARL_049 |
| [ID_FGRP_019](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/Data/ID_FGRP_019.json) | BHInventoryItemDefinition | Id.Item.FGRP_019 |
| [ID_FGRP_020](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/Data/ID_FGRP_020.json) | BHInventoryItemDefinition | Id.Item.FGRP_020 |
| [ID_HNDG_053](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Handguards/HNDG_053/Content/Data/ID_HNDG_053.json) | BHInventoryItemDefinition | Id.Item.HNDG_053 |
| [ID_HNDG_054](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Handguards/HNDG_054/Content/Data/ID_HNDG_054.json) | BHInventoryItemDefinition | Id.Item.HNDG_054 |
| [ID_HNDG_055](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Handguards/HNDG_055/Content/Data/ID_HNDG_055.json) | BHInventoryItemDefinition | Id.Item.HNDG_055 |
| [ID_MAGZ_051](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_051/Content/Data/ID_MAGZ_051.json) | BHInventoryItemDefinition | Id.Item.9mm.Tracer |
| [ID_MAGZ_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_067/Content/Data/ID_MAGZ_067.json) | BHInventoryItemDefinition | Id.Item.308Win.Tracer |
| [ID_MAGZ_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_068/Content/Data/ID_MAGZ_068.json) | BHInventoryItemDefinition | Id.Item.308Win.Tracer |
| [ID_MAGZ_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_069/Content/Data/ID_MAGZ_069.json) | BHInventoryItemDefinition | Id.Item.762mm.Tracer |
| [ID_MAGZ_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_070/Content/Data/ID_MAGZ_070.json) | BHInventoryItemDefinition | Id.Item.308Win.Tracer |
| [ID_MAGZ_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_071/Content/Data/ID_MAGZ_071.json) | BHInventoryItemDefinition | Id.Item.308Win.Tracer |
| [ID_MUZL_064](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_064/Content/Data/ID_MUZL_064.json) | BHInventoryItemDefinition | Id.Item.MUZL_064 |
| [ID_MUZL_065](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_065/Content/Data/ID_MUZL_065.json) | BHInventoryItemDefinition | Id.Item.MUZL_065 |
| [ID_MUZL_066](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_066/Content/Data/ID_MUZL_066.json) | BHInventoryItemDefinition | Id.Item.MUZL_066 |
| [ID_MUZL_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_067/Content/Data/ID_MUZL_067.json) | BHInventoryItemDefinition | Id.Item.MUZL_067 |
| [ID_MUZL_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_068/Content/Data/ID_MUZL_068.json) | BHInventoryItemDefinition | Id.Item.MUZL_068 |
| [ID_MUZL_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_069/Content/Data/ID_MUZL_069.json) | BHInventoryItemDefinition | Id.Item.MUZL_069 |
| [ID_MUZL_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_070/Content/Data/ID_MUZL_070.json) | BHInventoryItemDefinition | Id.Item.MUZL_070 |
| [ID_MUZL_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_071/Content/Data/ID_MUZL_071.json) | BHInventoryItemDefinition | Id.Item.MUZL_071 |
| [ID_MUZL_072](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_072/Content/Data/ID_MUZL_072.json) | BHInventoryItemDefinition | Id.Item.MUZL_072 |
| [ID_Molotov](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/ID_Molotov.json) | BHInventoryItemDefinition | Id.Item.Molotov |
| [ID_PGRP_042](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_042/Content/Data/ID_PGRP_042.json) | BHInventoryItemDefinition | Id.Item.PGRP_042 |
| [ID_PGRP_043](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_043/Content/Data/ID_PGRP_043.json) | BHInventoryItemDefinition | Id.Item.PGRP_043 |
| [ID_PGRP_044](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_044/Content/Data/ID_PGRP_044.json) | BHInventoryItemDefinition | Id.Item.PGRP_044 |
| [ID_SGHT_038](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_038/Content/Data/ID_SGHT_038.json) | BHInventoryItemDefinition | Id.Item.SGHT_038 |
| [ID_SGHT_039](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_039/Content/Data/ID_SGHT_039.json) | BHInventoryItemDefinition | Id.Item.SGHT_039 |
| [ID_SGHT_040](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_040/Content/Data/ID_SGHT_040.json) | BHInventoryItemDefinition | Id.Item.SGHT_040 |
| [ID_STOK_058](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Stocks/STOK_058/Content/Data/ID_STOK_058.json) | BHInventoryItemDefinition | Id.Item.STOK_058 |
| [ID_STOK_059](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Stocks/STOK_059/Content/Data/ID_STOK_059.json) | BHInventoryItemDefinition | Id.Item.STOK_059 |
| [ID_STOK_060](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Stocks/STOK_060/Content/Data/ID_STOK_060.json) | BHInventoryItemDefinition | Id.Item.STOK_060 |
| [ID_WEPN_031](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/ID_WEPN_031.json) | BHInventoryItemDefinition | Id.Item.HNDG_055 |
| [ID_WEPN_034](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/ID_WEPN_034.json) | BHInventoryItemDefinition | Id.Item.MAGZ_068 |
| [ID_WEPN_036](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/ID_WEPN_036.json) | BHInventoryItemDefinition | Id.Item.MAGZ_067 |
| [ID_WEPN_037](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/ID_WEPN_037.json) | BHInventoryItemDefinition | Id.Item.MAGZ_069 |
| [AE_Player_Damage_Environment_Burn](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Player_Damage_Environment_Burn.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Burn](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Burn.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Burn_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Burn_Stop.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Explode](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Explode.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Explode_Water](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Explode_Water.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Flight](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Flight.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Flight_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Flight_Stop.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Inspect](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Inspect.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Light](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Light.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Light_Overarm](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Light_Overarm.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Light_Overarm_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Light_Overarm_Stop.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Light_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Light_Stop.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Light_Underarm](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Light_Underarm.json) | CrosstalkAudioEvent | — |
| [AE_Weapon_Throwable_Molotov_Light_Underarm_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Audio/Events/AE_Weapon_Throwable_Molotov_Light_Underarm_Stop.json) | CrosstalkAudioEvent | — |
| [C_AimAssistPullStrengthDistanceCurve_Default](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Default.json) | CurveFloat | — |
| [C_AimAssistSlowStrengthDistanceCurve_Default](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_Default.json) | CurveFloat | — |
| [DT_EntityData_Ext_FGRP_019](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/Data/DT_EntityData_Ext_FGRP_019.json) | DataTable | Id.Item.FGRP_019 |
| [DT_EntityData_Ext_FGRP_020](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/Data/DT_EntityData_Ext_FGRP_020.json) | DataTable | Id.Item.FGRP_020 |
| [DT_EntityData_Ext_MAGZ_051](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_051/Content/Data/DT_EntityData_Ext_MAGZ_051.json) | DataTable | Id.Item.MAGZ_051 |
| [DT_EntityData_Ext_MAGZ_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_067/Content/Data/DT_EntityData_Ext_MAGZ_067.json) | DataTable | Id.Item.MAGZ_067 |
| [DT_EntityData_Ext_MAGZ_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_068/Content/Data/DT_EntityData_Ext_MAGZ_068.json) | DataTable | Id.Item.MAGZ_068 |
| [DT_EntityData_Ext_MAGZ_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_069/Content/Data/DT_EntityData_Ext_MAGZ_069.json) | DataTable | Id.Item.MAGZ_069 |
| [DT_EntityData_Ext_MAGZ_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_070/Content/Data/DT_EntityData_Ext_MAGZ_070.json) | DataTable | Id.Item.MAGZ_070 |
| [DT_EntityData_Ext_MAGZ_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_071/Content/Data/DT_EntityData_Ext_MAGZ_071.json) | DataTable | Id.Item.MAGZ_071 |
| [DT_EntityData_Ext_MUZL_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_067/Content/Data/DT_EntityData_Ext_MUZL_067.json) | DataTable | Id.Item.MUZL_067 |
| [DT_EntityData_Ext_MUZL_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_068/Content/Data/DT_EntityData_Ext_MUZL_068.json) | DataTable | Id.Item.MUZL_068 |
| [DT_EntityData_Ext_MUZL_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_069/Content/Data/DT_EntityData_Ext_MUZL_069.json) | DataTable | Id.Item.MUZL_069 |
| [DT_EntityData_Ext_MUZL_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_070/Content/Data/DT_EntityData_Ext_MUZL_070.json) | DataTable | Id.Item.MUZL_070 |
| [DT_EntityData_Ext_MUZL_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_071/Content/Data/DT_EntityData_Ext_MUZL_071.json) | DataTable | Id.Item.MUZL_071 |
| [DT_EntityData_Ext_MUZL_072](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_072/Content/Data/DT_EntityData_Ext_MUZL_072.json) | DataTable | Id.Item.MUZL_072 |
| [DT_EntityData_Ext_SGHT_038](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_038/Content/Data/DT_EntityData_Ext_SGHT_038.json) | DataTable | Id.Item.SGHT_038 |
| [DT_EntityData_Ext_SGHT_039](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_039/Content/Data/DT_EntityData_Ext_SGHT_039.json) | DataTable | Id.Item.SGHT_039 |
| [DT_EntityData_Ext_SGHT_040](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_040/Content/Data/DT_EntityData_Ext_SGHT_040.json) | DataTable | Id.Item.SGHT_040 |
| [DT_EntityData_Ext_WEPN_017](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_EntityData_Ext_WEPN_017.json) | DataTable | Id.Item.WEPN_017 |
| [DT_EntityData_Ext_WEPN_031](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/DT_EntityData_Ext_WEPN_031.json) | DataTable | Id.Item.WEPN_031 |
| [DT_EntityData_Ext_WEPN_034](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/DT_EntityData_Ext_WEPN_034.json) | DataTable | Id.Item.WEPN_034 |
| [DT_EntityData_Ext_WEPN_036](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/DT_EntityData_Ext_WEPN_036.json) | DataTable | Id.Item.WEPN_036 |
| [DT_EntityData_Ext_WEPN_037](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DT_EntityData_Ext_WEPN_037.json) | DataTable | Id.Item.WEPN_037 |
| [DT_EntityData_UI_Ext_Molotov](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DT_EntityData_UI_Ext_Molotov.json) | DataTable | Id.Item.Molotov |
| [DT_PostProcessEffects_Molotov](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DT_PostProcessEffects_Molotov.json) | DataTable | — |
| [DT_VendorData_Ext_FGRP_019](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/Data/DT_VendorData_Ext_FGRP_019.json) | DataTable | Id.Item.FGRP_019 |
| [DT_VendorData_Ext_FGRP_020](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/Data/DT_VendorData_Ext_FGRP_020.json) | DataTable | Id.Item.FGRP_020 |
| [DT_VendorData_Ext_MAGZ_051](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_051/Content/Data/DT_VendorData_Ext_MAGZ_051.json) | DataTable | Id.Item.MAGZ_051 |
| [DT_VendorData_Ext_MAGZ_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_067/Content/Data/DT_VendorData_Ext_MAGZ_067.json) | DataTable | Id.Item.MAGZ_067 |
| [DT_VendorData_Ext_MAGZ_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_068/Content/Data/DT_VendorData_Ext_MAGZ_068.json) | DataTable | Id.Item.MAGZ_068 |
| [DT_VendorData_Ext_MAGZ_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_069/Content/Data/DT_VendorData_Ext_MAGZ_069.json) | DataTable | Id.Item.MAGZ_069 |
| [DT_VendorData_Ext_MAGZ_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_070/Content/Data/DT_VendorData_Ext_MAGZ_070.json) | DataTable | Id.Item.MAGZ_070 |
| [DT_VendorData_Ext_MAGZ_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_071/Content/Data/DT_VendorData_Ext_MAGZ_071.json) | DataTable | Id.Item.MAGZ_071 |
| [DT_VendorData_Ext_MUZL_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_067/Content/Data/DT_VendorData_Ext_MUZL_067.json) | DataTable | Id.Item.MUZL_067 |
| [DT_VendorData_Ext_MUZL_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_068/Content/Data/DT_VendorData_Ext_MUZL_068.json) | DataTable | Id.Item.MUZL_068 |
| [DT_VendorData_Ext_MUZL_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_069/Content/Data/DT_VendorData_Ext_MUZL_069.json) | DataTable | Id.Item.MUZL_069 |
| [DT_VendorData_Ext_MUZL_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_070/Content/Data/DT_VendorData_Ext_MUZL_070.json) | DataTable | Id.Item.MUZL_070 |
| [DT_VendorData_Ext_MUZL_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_071/Content/Data/DT_VendorData_Ext_MUZL_071.json) | DataTable | Id.Item.MUZL_071 |
| [DT_VendorData_Ext_MUZL_072](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_072/Content/Data/DT_VendorData_Ext_MUZL_072.json) | DataTable | Id.Item.MUZL_072 |
| [DT_VendorData_Ext_Molotov](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DT_VendorData_Ext_Molotov.json) | DataTable | Id.Item.Molotov |
| [DT_VendorData_Ext_WEPN_017](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_VendorData_Ext_WEPN_017.json) | DataTable | Id.Item.WEPN_017 |
| [DT_VendorData_Ext_WEPN_036](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/DT_VendorData_Ext_WEPN_036.json) | DataTable | Id.Item.WEPN_036 |
| [DT_VendorData_Weapon_WEPN_031](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/DT_VendorData_Weapon_WEPN_031.json) | DataTable | Id.Item.WEPN_031 |
| [DT_VendorData_Weapon_WEPN_034](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/DT_VendorData_Weapon_WEPN_034.json) | DataTable | Id.Item.WEPN_034 |
| [DT_VendorData_Weapon_WEPN_037](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DT_VendorData_Weapon_WEPN_037.json) | DataTable | Id.Item.WEPN_037 |
| [DT_WeaponVendor_SGHT_038](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_038/Content/Data/DT_WeaponVendor_SGHT_038.json) | DataTable | Id.Item.SGHT_038 |
| [DT_WeaponVendor_SGHT_039](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_039/Content/Data/DT_WeaponVendor_SGHT_039.json) | DataTable | Id.Item.SGHT_039 |
| [DT_WeaponVendor_SGHT_040](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_040/Content/Data/DT_WeaponVendor_SGHT_040.json) | DataTable | Id.Item.SGHT_040 |
| [BARL_046](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_046/Content/BARL_046.json) | GameFeatureData | — |
| [BARL_047](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_047/Content/BARL_047.json) | GameFeatureData | — |
| [BARL_048](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_048/Content/BARL_048.json) | GameFeatureData | — |
| [BARL_049](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Barrels/BARL_049/Content/BARL_049.json) | GameFeatureData | — |
| [FGRP_019](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/FGRP_019.json) | GameFeatureData | — |
| [FGRP_020](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/FGRP_020.json) | GameFeatureData | — |
| [HNDG_053](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Handguards/HNDG_053/Content/HNDG_053.json) | GameFeatureData | — |
| [HNDG_054](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Handguards/HNDG_054/Content/HNDG_054.json) | GameFeatureData | — |
| [HNDG_055](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Handguards/HNDG_055/Content/HNDG_055.json) | GameFeatureData | — |
| [IRNS_009](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Default Sights/IRNS_009/Content/IRNS_009.json) | GameFeatureData | — |
| [IRNS_010](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Default Sights/IRNS_010/Content/IRNS_010.json) | GameFeatureData | — |
| [IRNS_011](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Default Sights/IRNS_011/Content/IRNS_011.json) | GameFeatureData | — |
| [MAGZ_051](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_051/Content/MAGZ_051.json) | GameFeatureData | — |
| [MAGZ_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_067/Content/MAGZ_067.json) | GameFeatureData | — |
| [MAGZ_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_068/Content/MAGZ_068.json) | GameFeatureData | — |
| [MAGZ_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_069/Content/MAGZ_069.json) | GameFeatureData | — |
| [MAGZ_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_070/Content/MAGZ_070.json) | GameFeatureData | — |
| [MAGZ_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_071/Content/MAGZ_071.json) | GameFeatureData | — |
| [MUZL_064](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_064/Content/MUZL_064.json) | GameFeatureData | — |
| [MUZL_065](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_065/Content/MUZL_065.json) | GameFeatureData | — |
| [MUZL_066](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_066/Content/MUZL_066.json) | GameFeatureData | — |
| [MUZL_067](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_067/Content/MUZL_067.json) | GameFeatureData | — |
| [MUZL_068](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_068/Content/MUZL_068.json) | GameFeatureData | — |
| [MUZL_069](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_069/Content/MUZL_069.json) | GameFeatureData | — |
| [MUZL_070](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_070/Content/MUZL_070.json) | GameFeatureData | — |
| [MUZL_071](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_071/Content/MUZL_071.json) | GameFeatureData | — |
| [MUZL_072](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_072/Content/MUZL_072.json) | GameFeatureData | — |
| [Molotov](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Molotov.json) | GameFeatureData | — |
| [PGRP_042](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_042/Content/PGRP_042.json) | GameFeatureData | — |
| [PGRP_043](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_043/Content/PGRP_043.json) | GameFeatureData | — |
| [PGRP_044](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Pistol Grips/PGRP_044/Content/PGRP_044.json) | GameFeatureData | — |
| [RAIL_010](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Rails/RAIL_010/Content/RAIL_010.json) | GameFeatureData | — |
| [RAIL_011](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Rails/RAIL_011/Content/RAIL_011.json) | GameFeatureData | — |
| [SGHT_038](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_038/Content/SGHT_038.json) | GameFeatureData | — |
| [SGHT_039](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_039/Content/SGHT_039.json) | GameFeatureData | — |
| [SGHT_040](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_040/Content/SGHT_040.json) | GameFeatureData | — |
| [SGHT_041](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_041/Content/SGHT_041.json) | GameFeatureData | — |
| [STOK_058](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Stocks/STOK_058/Content/STOK_058.json) | GameFeatureData | — |
| [STOK_059](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Stocks/STOK_059/Content/STOK_059.json) | GameFeatureData | — |
| [STOK_060](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Components/Stocks/STOK_060/Content/STOK_060.json) | GameFeatureData | — |
| [WEPN_017](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/WEPN_017.json) | GameFeatureData | — |
| [WEPN_031](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/WEPN_031.json) | GameFeatureData | — |
| [WEPN_034](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/WEPN_034.json) | GameFeatureData | — |
| [WEPN_037](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/WEPN_037.json) | GameFeatureData | — |
| [ID_Molotov_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/ID_Molotov_Audio.json) | WDAudioData | — |
| [ID_WEPN_031_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/ID_WEPN_031_Audio.json) | WDAudioData | — |
| [ID_WEPN_034_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/ID_WEPN_034_Audio.json) | WDAudioData | — |
| [ID_WEPN_036_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/ID_WEPN_036_Audio.json) | WDAudioData | — |
| [ID_WEPN_037_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/ID_WEPN_037_Audio.json) | WDAudioData | — |
| [DA_CharacterModifierState_MolotovBurning](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DA_CharacterModifierState_MolotovBurning.json) | WDCharacterModifierStateDefinition | — |
| [DA_WEPN_031_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/DA_WEPN_031_Stats.json) | WDWeaponStatsData | Id.Item.WEPN_031 |
| [DA_WEPN_034_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/DA_WEPN_034_Stats.json) | WDWeaponStatsData | Id.Item.WEPN_034 |
| [DA_WEPN_036_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/DA_WEPN_036_Stats.json) | WDWeaponStatsData | Id.Item.WEPN_036 |
| [DA_WEPN_037_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DA_WEPN_037_Stats.json) | WDWeaponStatsData | Id.Item.WEPN_037 |

### Removed in Season 2 (16 assets)

These assets are not on GitHub, so there are no links.

| Asset | Type | Season 1 path |
|---|---|---|
| C_AimAssistPullStrengthDistanceCurve_AR_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_AR_Hipfire.json |
| C_AimAssistPullStrengthDistanceCurve_LMG_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_LMG_Hipfire.json |
| C_AimAssistPullStrengthDistanceCurve_Melee_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Melee_Hipfire.json |
| C_AimAssistPullStrengthDistanceCurve_Pistol_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Pistol_Hipfire.json |
| C_AimAssistPullStrengthDistanceCurve_Shotgun_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Shotgun_Hipfire.json |
| C_AimAssistPullStrengthDistanceCurve_SMG_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_SMG_Hipfire.json |
| C_AimAssistReticleEdgeFalloff_AR | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_AR.json |
| C_AimAssistReticleEdgeFalloff_LMG | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_LMG.json |
| C_AimAssistReticleEdgeFalloff_Pistol | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_Pistol.json |
| C_AimAssistReticleEdgeFalloff_Shotgun | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_Shotgun.json |
| C_AimAssistReticleEdgeFalloff_SMG | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_SMG.json |
| C_AimAssistSlowStrengthDistanceCurve_AR_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_AR_Hipfire.json |
| C_AimAssistSlowStrengthDistanceCurve_LMG_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_LMG_Hipfire.json |
| C_AimAssistSlowStrengthDistanceCurve_Pistol_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_Pistol_Hipfire.json |
| C_AimAssistSlowStrengthDistanceCurve_Shotgun_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_Shotgun_Hipfire.json |
| C_AimAssistSlowStrengthDistanceCurve_SMG_Hipfire | CurveFloat | Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_SMG_Hipfire.json |

### Moved in Season 2 (11 assets)

The Mosin was moved, not removed. `DA_Mosin_Stats` became `DA_WEPN_017_Stats`, with WeaponId `Id.Item.Mosin`. It gains `SuppressionMultiplier` 1.5. The `ID_Mosin` item became `ID_WEPN_017`. Most of its 142 changes are path and reference updates.

| Asset | Type | Season 1 path → Season 2 path |
|---|---|---|
| AnimSet_Mosin | BHAnimationSet | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/AnimSet_Mosin.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/AnimSet_Mosin.json` |
| DA_WEPN_017_Stats | WDWeaponStatsData | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/DA_Mosin_Stats.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DA_WEPN_017_Stats.json` |
| DT_VendorData_Weapon_Mosin | DataTable | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/DT_VendorData_Weapon_Mosin.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_VendorData_Weapon_Mosin.json` |
| ID_Mosin_MagInternal | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/ID_Mosin_MagInternal.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_Mosin_MagInternal.json` |
| ID_MosinBarrel | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Components/ID_MosinBarrel.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Components/ID_MosinBarrel.json` |
| ID_MosinStock | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Components/ID_MosinStock.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Components/ID_MosinStock.json` |
| ID_SR_02_BRL_04 | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Attachments/ID_SR_02_BRL_04.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Attachments/ID_SR_02_BRL_04.json` |
| ID_SR_02_GRP_02 | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Attachments/ID_SR_02_GRP_02.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Attachments/ID_SR_02_GRP_02.json` |
| ID_SR_02_STK_01 | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/Attachments/ID_SR_02_STK_01.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/Attachments/ID_SR_02_STK_01.json` |
| ID_WEPN_017 | BHInventoryItemDefinition | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/ID_Mosin.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_WEPN_017.json` |
| ID_WEPN_017_Audio | WDAudioData | `Wardogs/Plugins/GameFeatures/Weapons/Sniper/Mosin/Content/Data/ID_Mosin_Audio.json` → `Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/ID_WEPN_017_Audio.json` |

## See also

- [Infantry weapon stats, Season 02 update]({{ '/content/Wardogs_InfantryWeapons_Stats_v1.html' | relative_url }}#season-02-update-2026-10-15)
- [Weapons (items, vendor data), Season 02 update]({{ '/content/Wardogs_Weapons_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Weapons game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Weapons_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Ammo game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Ammo_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Gunsmith game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Gunsmith_v2.html' | relative_url }}#season-02-update-2026-10-15)
