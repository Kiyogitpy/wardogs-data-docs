---
title: "Items & Equipment changes"
parent: "Season 2 Changes"
nav_order: 5
description: "Item and equipment changes from Season 1 to Season 2: 37 assets added, 4 removed, 211 modified with real changes, 1,883 property changes."
---

# Items & Equipment changes

{{ page.description }}

Counts come from `assets/data/season-diff/index.json` and `items-equipment.json`. Values are copied as stored. Signed deltas and percentages are calculated from the stored values. Noise-only assets are skipped.

| Measure | Count |
|---|---|
| Assets added | 37 |
| Assets removed | 4 |
| Assets modified with real changes | 211 |
| Assets modified, noise only (skipped) | 100 |
| Assets moved | 0 |
| Property changes (index.json) | 1,883 |

The change list holds 2,067 records. The index figure equals that total minus `removed_values` (184).

## Headline changes

Numeric changes are grouped by asset family. 818 numeric records in stage assets (`DA_Buildable_*_Stages`) are not tabulated. They are mostly `CriticalHitSpots` and `SnapTransforms` transform values compared by index, which is array churn.

### Ammo and projectiles

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_120x570mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Max | 3.0 | 5.0 | +2.0 (+66.7%) |
| DA_120x570mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 1.0 | 2.0 | +1.0 (+100.0%) |
| DA_122mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.6 | 0.9 | +0.3 (+50.0%) |
| DA_12g_RifledSlug_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.1 | 1.0 | +0.9 (+900.0%) |
| DA_308Winchester_ProjectileData | ProjectileStats.DamageValues.BaseDamage | 60.0 | 45.0 | −15.0 (−25.0%) |
| DA_308Winchester_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.9 | 0.65 | −0.25 (−27.8%) |
| DA_308Winchester_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.5 | 1.25 | +0.75 (+150.0%) |
| DA_30mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.55 | 0.75 | +0.2 (+36.4%) |
| DA_35x228mm_ProjectileData | ProjectileStats.ProjectileDimensions.DragModel.Value | 2.5 | 0.5 | −2.0 (−80.0%) |
| DA_35x228mm_ProjectileData | ProjectileStats.ProjectileDimensions.Mass | 0.15 | 0.375 | +0.225 (+150.0%) |
| DA_35x228mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.55 | 0.8 | +0.25 (+45.5%) |
| DA_45ACP_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.075 | 0.15 | +0.075 (+100.0%) |
| DA_45Colt_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.3 | 0.8 | +0.5 (+166.7%) |
| DA_50AE_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.5 | 0.32 | −0.18 (−36.0%) |
| DA_50AE_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.75 | 0.9 | +0.15 (+20.0%) |
| DA_50Cal_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 1.0 | 0.75 | −0.25 (−25.0%) |
| DA_545mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.15 | 0.3 | +0.15 (+100.0%) |
| DA_545mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.35 | 1.0 | +0.65 (+185.7%) |
| DA_556mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.12 | 0.3 | +0.18 (+150.0%) |
| DA_556mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.35 | 1.0 | +0.65 (+185.7%) |
| DA_762mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.5 | 1.0 | +0.5 (+100.0%) |
| DA_762x54mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.9 | 0.65 | −0.25 (−27.8%) |
| DA_762x54mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.35 | 1.5 | +1.15 (+328.6%) |
| DA_7mmBuckshot_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.13 | 0.2 | +0.07 (+53.8%) |
| DA_7mmBuckshot_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.1 | 0.4 | +0.3 (+300.0%) |
| DA_9mm_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.1 | 0.2 | +0.1 (+100.0%) |
| DA_9mm_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.1 | 0.8 | +0.7 (+700.0%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.MaxProjectileLifetime | 30.0 | 14.0 | −16.0 (−53.3%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.PenetrationEffectivenessMultiplier | 0.03 | 0.5 | +0.47 (+1566.7%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.ProjectileDimensions.Diameter | 0.4 | 0.65 | +0.25 (+62.5%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.ProjectileDimensions.DragModel.Value | 1.8 | 2.5 | +0.7 (+38.9%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.SuppressionData.BaseSuppression | 0.6 | 0.2 | −0.4 (−66.7%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Max | 1.2 | 1.5 | +0.3 (+25.0%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.SuppressionData.DistanceFalloffRange.Min | 0.1 | 0.2 | +0.1 (+100.0%) |
| DA_Arrow_Combat_ProjectileData | ProjectileStats.TypicalSpeed | 64200.0 | 15200.0 | −49000.0 (−76.3%) |
| DA_CombatBow_Stats | …EditorCurveData.Keys[1].ArriveTangent | -2.413006e-05 | -1.070042e-05 | +1.34296e-05 (+55.7%) |
| DA_CombatBow_Stats | …EditorCurveData.Keys[1].LeaveTangent | -2.4311637e-05 | -1.0786811e-05 | +1.35248e-05 (+55.6%) |
| DA_CombatBow_Stats | WeaponStats.DistanceDamageFalloffCurve.EditorCurveData.Keys[2].Time | 120000.0 | 50000.0 | −70000.0 (−58.3%) |
| DA_CombatBow_Stats | WeaponStats.DistanceDamageFalloffCurve.EditorCurveData.Keys[2].Value | 0.2 | 0.0 | −0.2 (−100.0%) |
| DA_CombatBow_Stats | WeaponStats.InitialBulletSpeed | 65000.0 | 16000.0 | −49000.0 (−75.4%) |

Showing 40 of 55 rows, sorted by significance. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=ProjectileData

### Armour, helmets and melee

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| ID_30mm | MaxStackSize | 200 | 50 | −150 (−75.0%) |
| ID_Crowbar | ReplicatedData.Durability | 5000.0 | 7000.0 | +2000.0 (+40.0%) |
| ID_HeavyArmor | DurabilityStagesSetupData[0].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyArmor | DurabilityStagesSetupData[1].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyArmor | DurabilityStagesSetupData[2].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyArmor | DurabilityStagesSetupData[3].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyHelmet | DurabilityStagesSetupData[0].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyHelmet | DurabilityStagesSetupData[1].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyHelmet | DurabilityStagesSetupData[2].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_HeavyHelmet | DurabilityStagesSetupData[3].DamagePercentageReduction | 55.0 | 50.0 | −5.0 (−9.1%) |
| ID_LargeHammer | BuildAmountWhenTargetIsHit | 10.0 | 8.0 | −2.0 (−20.0%) |
| ID_LargeHammer | DefaultDecalColor.A | 0 | 255 | +255 |
| ID_LargeHammer | DefaultDecalColor.B | 1 | 2 | +1 (+100.0%) |
| ID_LargeHammer | DefaultDecalColor.G | 0 | 207 | +207 |
| ID_LargeHammer | DefaultDecalColor.R | 0 | 255 | +255 |
| ID_LargeHammer | unnamed property (`_aaabelcphphddcjabdj`) | 1056964608 | 0.5 | −1056964607.5 (−100.0%) |
| ID_MediumHammer | BuildAmountWhenTargetIsHit | 6.0 | 5.0 | −1.0 (−16.7%) |
| ID_MediumHammer | DefaultDecalColor.A | 0 | 255 | +255 |
| ID_MediumHammer | DefaultDecalColor.B | 1 | 2 | +1 (+100.0%) |
| ID_MediumHammer | DefaultDecalColor.G | 0 | 207 | +207 |
| ID_MediumHammer | DefaultDecalColor.R | 0 | 255 | +255 |
| ID_MediumHammer | unnamed property (`_aaabelcphphddcjabdj`) | 1056964608 | 0.5 | −1056964607.5 (−100.0%) |
| ID_SmallHammer | DefaultDecalColor.A | 0 | 255 | +255 |
| ID_SmallHammer | DefaultDecalColor.B | 1 | 2 | +1 (+100.0%) |
| ID_SmallHammer | DefaultDecalColor.G | 0 | 207 | +207 |
| ID_SmallHammer | DefaultDecalColor.R | 0 | 255 | +255 |
| ID_SmallHammer | unnamed property (`_aaabelcphphddcjabdj`) | 1056964608 | 0.5 | −1056964607.5 (−100.0%) |
| ID_SuperHeavyArmor | DurabilityStagesSetupData[0].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyArmor | DurabilityStagesSetupData[1].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyArmor | DurabilityStagesSetupData[2].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyArmor | DurabilityStagesSetupData[3].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyHelmet | DurabilityStagesSetupData[0].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyHelmet | DurabilityStagesSetupData[1].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyHelmet | DurabilityStagesSetupData[2].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |
| ID_SuperHeavyHelmet | DurabilityStagesSetupData[3].DamagePercentageReduction | 65.0 | 60.0 | −5.0 (−7.7%) |

Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=ID_

### Vendor tables

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_VendorData_Ext_Armor | Rows.Id.Item.HeavyArmor.VendorItemVariations[Id.Item.HeavyArmor].Price | 2000.0 | 2500.0 | +500.0 (+25.0%) |
| DT_VendorData_Ext_Armor | …HeavyHelmet.VendorItemVariations[Id.Item.HeavyHelmet].Price | 1500.0 | 2000.0 | +500.0 (+33.3%) |
| DT_VendorData_Ext_Armor | …SuperHeavyArmor.VendorItemVariations[Id.Item.SuperHeavyArmor].Price | 4000.0 | 5000.0 | +1000.0 (+25.0%) |
| DT_VendorData_Ext_Armor | …SuperHeavyHelmet.VendorItemVariations[Id.Item.SuperHeavyHelmet].Price | 3000.0 | 4500.0 | +1500.0 (+50.0%) |
| DT_VendorData_Ext_Binoculars | Rows.ID.Item.Binoculars.VendorItemVariations[ID.Item.Binoculars].Price | 75.0 | 180.0 | +105.0 (+140.0%) |
| DT_VendorData_Ext_CombatBow | Rows.Id.Item.CombatBow.VendorItemVariations[Id.Item.CombatBow].Price | 800.0 | 1350.0 | +550.0 (+68.8%) |
| DT_VendorData_Ext_Crowbar | Rows.Id.Item.Crowbar.VendorItemVariations[Id.Item.Crowbar].Price | 1100.0 | 885.0 | −215.0 (−19.5%) |
| DT_VendorData_Ext_Enox | …Standard.VendorItemVariations[Id.Item.Resuscitator.Standard].Price | 500.0 | 425.0 | −75.0 (−15.0%) |
| DT_VendorData_Ext_MedKit | …Standard.VendorItemVariations[ID.Item.MedKit.Standard].Price | 2000.0 | 1800.0 | −200.0 (−10.0%) |
| DT_VendorData_Ext_RangeFinder | …InfraredRangeFinder.VendorItemVariations[ID.Item.InfraredRangeFinder].Price | 1200.0 | 3200.0 | +2000.0 (+166.7%) |
| DT_VendorData_Ext_RangeFinder | Rows.ID.Item.Monocular.VendorItemVariations[ID.Item.Monocular].Price | 150.0 | 350.0 | +200.0 (+133.3%) |
| DT_VendorData_Ext_RangeFinder | …RangeFinder.VendorItemVariations[ID.Item.RangeFinder].Price | 400.0 | 1450.0 | +1050.0 (+262.5%) |
| DT_VendorData_Ext_VehicleRepairTool | …Standard.VendorItemVariations[ID.Item.RepairTool.Wrench.Standard].Price | 150.0 | 180.0 | +30.0 (+20.0%) |

Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=DT_VendorData_Ext

### Buildables

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_Buildable_AirRaidShelter | Cost | 100 | 200 | +100 (+100.0%) |
| DA_Buildable_AirRaidShelter_Ceiling | BuildingStages[0].MeshLocalBoundingBox.Max.X | 356.9321 | 355.86703 | −1.06507 (−0.3%) |
| DA_Buildable_AirRaidShelter_Ceiling | BuildingStages[0].MeshLocalBoundingBox.Max.Z | 17.571127 | 9.19816 | −8.372967 (−47.7%) |
| DA_Buildable_AirRaidShelter_Ceiling | BuildingStages[0].MeshLocalBoundingBox.Min.X | -354.43753 | -352.2929 | +2.14463 (+0.6%) |
| DA_Buildable_AirRaidShelter_Ceiling | FinalStageBoundingBox.Max.X | 356.9321 | 355.86703 | −1.06507 (−0.3%) |
| DA_Buildable_AirRaidShelter_Ceiling | FinalStageBoundingBox.Max.Z | 17.571127 | 9.19816 | −8.372967 (−47.7%) |
| DA_Buildable_AirRaidShelter_Ceiling | FinalStageBoundingBox.Min.X | -354.43753 | -352.2929 | +2.14463 (+0.6%) |
| DA_Buildable_BremmerWall | Cost | 15 | 32 | +17 (+113.3%) |
| DA_Buildable_Bunker | Cost | 100 | 200 | +100 (+100.0%) |
| DA_Buildable_Bunker_Roof | BuildingStages[0].MeshLocalBoundingBox.Max.X | 367.36096 | 716.6255 | +349.26454 (+95.1%) |
| DA_Buildable_Bunker_Roof | BuildingStages[0].MeshLocalBoundingBox.Max.Y | 367.73395 | 382.2424 | +14.50845 (+3.9%) |
| DA_Buildable_Bunker_Roof | BuildingStages[0].MeshLocalBoundingBox.Max.Z | 110.41064 | 110.70189 | +0.29125 (+0.3%) |
| DA_Buildable_Bunker_Roof | BuildingStages[0].MeshLocalBoundingBox.Min.X | -382.31192 | -441.62207 | −59.31015 (−15.5%) |
| DA_Buildable_Bunker_Roof | BuildingStages[0].MeshLocalBoundingBox.Min.Y | -366.1128 | -367.41464 | −1.30184 (−0.4%) |
| DA_Buildable_Bunker_Roof | BuildingStages[0].MeshLocalBoundingBox.Min.Z | -215.54507 | -224.36818 | −8.82311 (−4.1%) |
| DA_Buildable_Bunker_Roof | FinalStageBoundingBox.Max.X | 367.36096 | 716.6255 | +349.26454 (+95.1%) |
| DA_Buildable_Bunker_Roof | FinalStageBoundingBox.Max.Y | 367.73395 | 382.2424 | +14.50845 (+3.9%) |
| DA_Buildable_Bunker_Roof | FinalStageBoundingBox.Max.Z | 110.41064 | 110.70189 | +0.29125 (+0.3%) |
| DA_Buildable_Bunker_Roof | FinalStageBoundingBox.Min.X | -382.31192 | -441.62207 | −59.31015 (−15.5%) |
| DA_Buildable_Bunker_Roof | FinalStageBoundingBox.Min.Y | -366.1128 | -367.41464 | −1.30184 (−0.4%) |
| DA_Buildable_Bunker_Roof | FinalStageBoundingBox.Min.Z | -215.54507 | -224.36818 | −8.82311 (−4.1%) |
| DA_Buildable_CrowsNest | Cost | 100 | 200 | +100 (+100.0%) |
| DA_Buildable_Door | Cost | 22 | 80 | +58 (+263.6%) |
| DA_Buildable_Gate | Cost | 85 | 200 | +115 (+135.3%) |
| DA_Buildable_HotzoneMagnet | Cost | 2250 | 2750 | +500 (+22.2%) |
| DA_Buildable_HotzoneMagnet | HotZoneMagnetDurationPerFuel | 0.05 | 0.03 | −0.02 (−40.0%) |
| DA_Buildable_HotzoneMagnet | HotZoneMagnetMinimumFuel | 1500.0 | 2000.0 | +500.0 (+33.3%) |
| DA_Buildable_HotzoneMagnet | MaxFuel | 7500.0 | 10000.0 | +2500.0 (+33.3%) |
| DT_GlobalDamage_BuildableData | …DamageModificationEntries[11].OutModification.Amount | -70.0 | -80.0 | −10.0 (−14.3%) |
| DT_GlobalDamage_BuildableData | …DamageModificationEntries[9].OutModification.Amount | -80.0 | -92.0 | −12.0 (−15.0%) |
| DT_GlobalDamage_BuildableData | …DamageModificationEntries[8].OutModification.Amount | -40.0 | -50.0 | −10.0 (−25.0%) |
| DT_GlobalDamage_BuildableData | …DamageModificationEntries[11].OutModification.Amount | -85.0 | -92.0 | −7.0 (−8.2%) |
| DT_GlobalDamage_BuildableData | …DamageModificationEntries[9].OutModification.Amount | -75.0 | -80.0 | −5.0 (−6.7%) |
| DT_GlobalDamage_BuildableData | …DamageModificationEntries[11].OutModification.Amount | -75.0 | -92.0 | −17.0 (−22.7%) |

Showing 34 of 34 rows. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=DA_Buildable

### Other numeric changes

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| AE_Player_Item_Defibrillator_DryFire | unnamed property (`_aaabhgndclheajnnlna`) | 0.505 | 50.5 | +49.995 (+9900.0%) |

Showing 1 of 1 rows. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=DA_

### Non-numeric changes

126 changed values are not numeric. The most common properties:

| Property | Changes | Example asset | Season 1 | Season 2 |
|---|---|---|---|---|
| bShouldSpawnFoundations | 27 | DA_Buildable_AirRaidShelter_Stages | false | true |
| Key | 22 | DA_Buildable_Bunker_Floor | 87DFBA84480B10D57E5455B5567D31A2 | Buildable.Bunker |
| SourceString | 21 | DA_Buildable_CrowsNest_BaseFloor | CrowsNest | — |
| LocalizedString | 21 | DA_Buildable_CrowsNest_BaseFloor | CrowsNest |  |
| TagName | 10 | DT_Ext_VendorData_MusicTape_01 | None | Audio.Event.UI.InGame.Vendor.Purchase |
| AssetPathName | 5 | Crowbar | /Script/WDGame.WDDoor | /Buildables/Data/Buildables/HBlock_Gate_6x2/B_Door_Gate_Right.B_Door_Gate_Right_C |
| SaveID | 5 | D_BuildableDoor | 4A3D41E9-44BC5FE1-C5584BAE-88E50EC5 | 6A939B1C-48AB3604-C363B598-B3484C13 |
| ObjectName | 3 | DA_545mm_ProjectileData | CurveFloat'AR_SuppressionCurve' | CurveFloat'CR_SuppressionCurve_Medium' |
| ObjectPath | 3 | DA_545mm_ProjectileData | /Game/GameMechanics/Inventory/AR_SuppressionCurve.0 | /Game/GameMechanics/Inventory/CR_SuppressionCurve_Medium.0 |
| Hex | 3 | ID_LargeHammer | 000001 | FFCF02 |
| ThirdPersonPlayerAnimation | 1 | AnimSet_CombatBow | — | {'ObjectName': "AnimMontage'AM_TP_Bow_Door_Interact'", 'ObjectPath': '/Game/Animation/Cha… |
| bShouldPenetrate | 1 | DA_Arrow_Explosive_ProjectileData | true | false |

`DT_EmoteData` has 120 change records. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=DT_EmoteData

## New in Season 2

37 assets were added. Identification is the type, the item or buildable folder from the path, and the export count.

| Asset | Type | Folder | Exports |
|---|---|---|---|
| [AE_InfraredRangeFinder_Active](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Audio/Infrared/Events/AE_InfraredRangeFinder_Active.json) | CrosstalkAudioEvent | Events | 4 |
| [AE_InfraredRangeFinder_Active_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Audio/Infrared/Events/AE_InfraredRangeFinder_Active_Stop.json) | CrosstalkAudioEvent | Events | 2 |
| [AE_InfraredRangeFinder_LowBattery](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Audio/Infrared/Events/AE_InfraredRangeFinder_LowBattery.json) | CrosstalkAudioEvent | Events | 3 |
| [AE_InfraredRangeFinder_LowBattery_Stop](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Audio/Infrared/Events/AE_InfraredRangeFinder_LowBattery_Stop.json) | CrosstalkAudioEvent | Events | 2 |
| [AE_InfraredRangeFinder_Toggle](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Audio/Infrared/Events/AE_InfraredRangeFinder_Toggle.json) | CrosstalkAudioEvent | Events | 2 |
| [AE_InfraredRangeFinder_Toggle_Off](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Audio/Infrared/Events/AE_InfraredRangeFinder_Toggle_Off.json) | CrosstalkAudioEvent | Events | 2 |
| [CF_FogProgressToDeltaTime](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/UI/CF_FogProgressToDeltaTime.json) | CurveFloat | UI | 1 |
| [CF_FogProgressToRemovalTime](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/UI/CF_FogProgressToRemovalTime.json) | CurveFloat | UI | 1 |
| [CR_SuppressionCurve_GrenadeLauncher](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_GrenadeLauncher.json) | CurveFloat | Inventory | 1 |
| [CR_SuppressionCurve_Large](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Large.json) | CurveFloat | Inventory | 1 |
| [CR_SuppressionCurve_Medium](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Medium.json) | CurveFloat | Inventory | 1 |
| [CR_SuppressionCurve_Rocket](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Rocket.json) | CurveFloat | Inventory | 1 |
| [CR_SuppressionCurve_Small](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Small.json) | CurveFloat | Inventory | 1 |
| [CR_SuppressionCurve_Special](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/CR_SuppressionCurve_Special.json) | CurveFloat | Inventory | 1 |
| [DA_125x570mm_ProjectileData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/125x570mm/DA_125x570mm_ProjectileData.json) | WDProjectileData | 125x570mm | 1 |
| [DA_Action_AccessLooting](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/UI/DA_Action_AccessLooting.json) | BHActionDefinition | UI | 1 |
| [DA_Action_AccessWagerVendor](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/UI/DA_Action_AccessWagerVendor.json) | BHActionDefinition | UI | 1 |
| [DA_Action_RangeFinder_Reload](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/Actions/DA_Action_RangeFinder_Reload.json) | WDActionDefinition | Actions | 1 |
| [DA_ArmorOverlay](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/UI/DA_ArmorOverlay.json) | WDUIArmorOverlayData | UI | 1 |
| [DA_Buildable_Shelter](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/SV_Shelter/DA_Buildable_Shelter.json) | WDBuildableDataAsset | SV_Shelter | 2 |
| [DA_Buildable_Shelter_Stages](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/SV_Shelter/DA_Buildable_Shelter_Stages.json) | BuildingStagesDefinition | SV_Shelter | 1 |
| [DA_Buildable_WoodBase](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/WoodBase/DA_Buildable_WoodBase.json) | WDBuildableDataAsset | WoodBase | 2 |
| [DA_RadialWheelSlotType_Shelter](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/SV_Shelter/DA_RadialWheelSlotType_Shelter.json) | WDUIRadialWheelSlotTypeDataAsset | SV_Shelter | 1 |
| [DA_RadialWheelSlotType_WoodBase](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/WoodBase/DA_RadialWheelSlotType_WoodBase.json) | WDUIRadialWheelSlotTypeDataAsset | WoodBase | 1 |
| [DA_Vehicle_MusicTape_11](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/Data/DA_Vehicle_MusicTape_11.json) | WDAudioData | Data | 1 |
| [DA_WoodBase_Stages](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/WoodBase/DA_WoodBase_Stages.json) | BuildingStagesDefinition | WoodBase | 1 |
| [DT_ChallengeRewards_SessionEvents_Crowbar](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengeRewards_SessionEvents_Crowbar.json) | DataTable | Rewards | 1 |
| [DT_ChallengesFeedActions_Crowbar](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengesFeedActions_Crowbar.json) | DataTable | Rewards | 1 |
| [DT_Challenges_SessionEvents_Crowbar](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_Challenges_SessionEvents_Crowbar.json) | DataTable | Rewards | 1 |
| [DT_Ext_Entity_UI_MusicTape_11](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/Data/DT_Ext_Entity_UI_MusicTape_11.json) | DataTable | Data | 1 |
| [DT_Ext_VendorData_MusicTape_11](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/Data/DT_Ext_VendorData_MusicTape_11.json) | DataTable | Data | 1 |
| [ID_125x570mm](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/125x570mm/ID_125x570mm.json) | BHInventoryItemDefinition | 125x570mm | 8 |
| [ID_MusicTape_11](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/Data/ID_MusicTape_11.json) | BHInventoryItemDefinition | Data | 5 |
| [ID_PilotHelmet](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_PilotHelmet.json) | BHInventoryItemDefinition | Data | 7 |
| [ID_TankHelmet](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/ID_TankHelmet.json) | BHInventoryItemDefinition | Data | 7 |
| [MusicTape_11](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/MusicTape_11.json) | GameFeatureData | Content | 4 |
| [ST_Challenges_SessionEvents_Crowbar_ForceOpenDoor](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/ST_Challenges_SessionEvents_Crowbar_ForceOpenDoor.json) | StateTree | Rewards | 2 |

## Removed in Season 2

| Asset | Type | Path |
|---|---|---|
| AR_SuppressionCurve | CurveFloat | Wardogs/Content/GameMechanics/Inventory/AR_SuppressionCurve.json |
| DA_Significance_Buildable | BHSignificanceSettingsAsset | Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/DA_Significance_Bui… |
| DA_Significance_Evaluator_Buildable | BHSignificanceEvaluator_Sphere | Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/DA_Significance_Eva… |
| DA_UI_BuildablePlacementData | WDUIBuildablePlacementData | Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/DA_UI_BuildablePlac… |

Removed assets are not on GitHub, so there are no links.

## Moved

None.

## See also

- [Items]({{ '/game-features/Wardogs_GameFeatures_Items_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Itemsmith]({{ '/game-features/Wardogs_GameFeatures_Itemsmith_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Ammo]({{ '/game-features/Wardogs_GameFeatures_Ammo_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Weapons]({{ '/content/Wardogs_Weapons_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Items]({{ '/content/Wardogs_Items_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Destruction]({{ '/content/Wardogs_Destruction_v2.html' | relative_url }}#season-02-update), Season 02 update

Full change browser for this area: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=items-equipment&q=

