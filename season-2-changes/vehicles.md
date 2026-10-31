---
title: "Vehicles changes"
parent: "Season 2 Changes"
nav_order: 4
description: "Vehicle changes from Season 1 to Season 2: 151 assets added, 1 removed, 261 modified with real changes, 3,926 property changes."
---

# Vehicles changes

{{ page.description }}

Counts come from `assets/data/season-diff/index.json` and `vehicles.json`. Values are copied as stored. Signed deltas and percentages are calculated from the stored values. Noise-only assets are skipped: renamed keys, swapped key names or shifted references from the different Season 1 export.

| Measure | Count |
|---|---|
| Assets added | 151 |
| Assets removed | 1 |
| Assets modified with real changes | 261 |
| Assets modified, noise only (skipped) | 201 |
| Assets moved | 0 |
| Property changes (index.json) | 3,926 |

The change list for these assets holds 3,944 records. The index figure equals that total minus `removed_values` (18).

## Headline changes

### Vehicle damage tables (`DT_GlobalDamage_VehicleData_*`)

Changed `OutModification.Amount` values in existing entries:

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_GlobalDamage_VehicleData_ROT_02 | Rotary.Havoc entry 12 Amount | 87.5 | -46.0 | −133.5 (−152.6%) |
| DT_GlobalDamage_VehicleData_ROT_03 | Rotary.LittleBird entry 15 Amount | -40.0 | -69.5 | −29.5 (−73.8%) |
| DT_GlobalDamage_VehicleData_ROT_04 | Rotary.ROT_04 entry 12 Amount | -40.0 | -57.25 | −17.25 (−43.1%) |
| DT_GlobalDamage_VehicleData_SPW_01 | Leopard.Spawn entry 25 Amount | -60.0 | -84.0 | −24.0 (−40.0%) |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01.AntiAir entry 22 Amount | -75.0 | -85.0 | −10.0 (−13.3%) |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01.Artillery entry 22 Amount | -75.0 | -85.0 | −10.0 (−13.3%) |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01.Heavy entry 22 Amount | -75.0 | -85.0 | −10.0 (−13.3%) |
| DT_GlobalDamage_VehicleData_WHL_05_Humvee | Humvee.Default entry 13 Amount | -67.0 | -85.0 | −18.0 (−26.9%) |
| DT_GlobalDamage_VehicleData_WHL_05_Minigun | Humvee.Minigun entry 13 Amount | -71.0 | -88.0 | −17.0 (−23.9%) |
| DT_GlobalDamage_VehicleData_WHL_05_Minigun | Humvee.Minigun entry 27 Amount | -90.0 | -88.0 | +2.0 (+2.2%) |
| DT_GlobalDamage_VehicleData_WHL_05_RingTurret | Humvee.MachineGun entry 13 Amount | -69.0 | -86.5 | −17.5 (−25.4%) |
| DT_GlobalDamage_VehicleData_WHL_05_RingTurret | Humvee.MachineGun entry 27 Amount | -87.5 | -86.5 | +1.0 (+1.1%) |
| DT_GlobalDamage_VehicleData_WHL_07_Ural | Wheeled.Ural entry 13 Amount | -65.0 | -87.5 | −22.5 (−34.6%) |

New damage entries. 24 entries were added across 17 tables. Each row is one new entry, shown with its source tag and amount:

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_GlobalDamage_VehicleData_ROT_02 | Rotary.Havoc entry 34 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 150.0 | added |
| DT_GlobalDamage_VehicleData_ROT_03 | Rotary.LittleBird entry 32 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 100.0 | added |
| DT_GlobalDamage_VehicleData_ROT_04 | Rotary.ROT_04 entry 32 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 150.0 | added |
| DT_GlobalDamage_VehicleData_SPW_01 | Leopard.Spawn entry 31 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | -10.0 | added |
| DT_GlobalDamage_VehicleData_STN_01 | Stationary.Mistral entry 25 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 50.0 | added |
| DT_GlobalDamage_VehicleData_STN_01 | Stationary.Mistral entry 6 · Meta.Damage.Cannon.20x102mm · Amount | — | -70.0 | added |
| DT_GlobalDamage_VehicleData_STN_02 | Stationary.Phalanx entry 25 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | -20.0 | added |
| DT_GlobalDamage_VehicleData_STN_02 | Stationary.Phalanx entry 6 · Meta.Damage.Cannon.20x102mm · Amount | — | -70.0 | added |
| DT_GlobalDamage_VehicleData_STN_03 | Stationary.Mortar entry 23 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | -50.0 | added |
| DT_GlobalDamage_VehicleData_STN_03 | Stationary.Mortar entry 6 · Meta.Damage.Cannon.20x102mm · Amount | — | -70.0 | added |
| DT_GlobalDamage_VehicleData_STN_04 | Stationary.RadioTower entry 24 · Meta.Damage.Cannon.20x102mm · Amount | — | -70.0 | added |
| DT_GlobalDamage_VehicleData_STN_04 | Stationary.RadioTower entry 26 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_STN_05 | Stationary.STN_05 entry 23 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | -50.0 | added |
| DT_GlobalDamage_VehicleData_STN_05 | Stationary.STN_05 entry 6 · Meta.Damage.Cannon.20x102mm · Amount | — | -70.0 | added |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01.AntiAir entry 28 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 40.0 | added |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01.Artillery entry 28 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 15.0 | added |
| DT_GlobalDamage_VehicleData_TNK_01 | TNK_01.Heavy entry 28 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 31.5 | added |
| DT_GlobalDamage_VehicleData_WHL_01 | Wheeled.Bobcat entry 19 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_WHL_02 | Patriot.Kodiak entry 28 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_WHL_05_Humvee | Humvee.Default entry 30 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_WHL_05_Minigun | Humvee.Minigun entry 30 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_WHL_05_RingTurret | Humvee.MachineGun entry 30 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy | Wheeled.DuneBuggy entry 29 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 250.0 | added |
| DT_GlobalDamage_VehicleData_WHL_07_Ural | Wheeled.Ural entry 29 · Meta.Damage.Explosive.Rocket.125mm · Amount | — | 75.0 | added |

Of these, 19 are `Meta.Damage.Explosive.Rocket.125mm` entries in 17 tables. 5 are `Meta.Damage.Cannon.20x102mm` entries in the five stationary tables.

Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=DT_GlobalDamage_VehicleData

### Phalanx and Mistral stage tables

[`DA_Phalanx_Stages`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/BuildableData/DA_Phalanx_Stages.json) has 1,894 change records and [`DA_Mistral_AA_Stages`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/BuildableData/DA_Mistral_AA_Stages.json) has 559. Most are `CriticalHitSpots` array entries compared by index. That is array churn, not a balance change, so these rows are not tabulated. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=DA_Phalanx_Stages

### Countermeasures

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_VehicleFlares → DA_VehicleCountermeasure | Type | WDUIVehicleFlaresData | WDUIVehicleCountermeasureData | changed |

The asset was renamed and its type changed. The record is in `engine-tooling-data.json`, not in this area.

### Wheels, axles and suspension

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_FrontAxle_WHL_02 | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_02 | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_02_Pickup | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_02_Pickup | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_05_Humvee | TorqueShare | 0.7 | 0.4 | −0.3 (−42.9%) |
| DA_FrontAxle_WHL_05_Humvee | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_05_Humvee | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_06_DuneBuggy | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_06_DuneBuggy | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_07 | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontAxle_WHL_07 | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_FrontWheels_WHL_05_Humvee | CompressionDamper.Values | 6000.0 | 7000.0 | +1000.0 (+16.7%) |
| DA_FrontWheels_WHL_05_Humvee | RelaxationDamper.Values | 7000.0 | 5250.0 | −1750.0 (−25.0%) |
| DA_MidAxle_WHL_07 | WheelSetup[rearL_frontWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_MidAxle_WHL_07 | WheelSetup[rearR_frontWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_02 | WheelSetup[rearLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_02 | WheelSetup[rearRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_02_Pickup | WheelSetup[rearLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_02_Pickup | WheelSetup[rearRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_05_Humvee | TorqueShare | 0.3 | 0.6 | +0.3 (+100.0%) |
| DA_RearAxle_WHL_05_Humvee | WheelSetup[rearLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_05_Humvee | WheelSetup[rearRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_06_DuneBuggy | WheelSetup[rearLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_06_DuneBuggy | WheelSetup[rearRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_07 | WheelSetup[rearL_rearWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearAxle_WHL_07 | WheelSetup[rearR_rearWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_RearWheels_WHL_05_Humvee | CompressionDamper.Values | 9000.0 | 8250.0 | −750.0 (−8.3%) |
| DA_RearWheels_WHL_05_Humvee | RelaxationDamper.Values | 12000.0 | 6250.0 | −5750.0 (−47.9%) |
| DA_RearWheels_WHL_06_DuneBuggy | BrakeTorque.Values | 16000.0 | 13000.0 | −3000.0 (−18.8%) |
| DA_RearWheels_WHL_06_DuneBuggy | BrakeTorque.Values[1] | 12000.0 | 9000.0 | −3000.0 (−25.0%) |
| DA_SPW_01_WheelData | DampingRebound | 12000.0 | 17000.0 | +5000.0 (+41.7%) |
| DA_TNK_01_WheelData | DampingRebound | 12000.0 | 17000.0 | +5000.0 (+41.7%) |
| DA_WHL_01_FrontAxle | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_WHL_01_FrontAxle | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_WHL_01_RearAxle | WheelSetup[rearLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_WHL_01_RearAxle | WheelSetup[rearRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |

Showing all 36 numeric changes in wheel, axle and suspension assets. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=Wheel

### Vehicle market prices and buildable costs

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_VehicleMarket_ROT_02 | Price (Havoc.Default) | 18000.0 | 28000.0 | +10000.0 (+55.6%) |
| DT_VehicleMarket_ROT_03_WeaponVariants | Price (Littlebird.MountedMachineGuns) | 7000.0 | 12000.0 | +5000.0 (+71.4%) |
| DT_VehicleMarket_ROT_03_WeaponVariants | Price (Littlebird.RocketPods) | 12500.0 | 18800.0 | +6300.0 (+50.4%) |
| DT_VehicleMarket_ROT_04_MachineGun | Price (ROT_04.MountedMachineGuns) | 8000.0 | 15000.0 | +7000.0 (+87.5%) |
| DT_VehicleMarket_TNK_01 | Price (TNK_01.AntiAir) | 10000.0 | 14000.0 | +4000.0 (+40.0%) |
| DT_VehicleMarket_TNK_01 | Price (TNK_01.Heavy) | 14000.0 | 22000.0 | +8000.0 (+57.1%) |
| DT_VehicleMarket_WHL_02_RingTurret | Price (Kodiak.MachineGun) | 3750.0 | 6750.0 | +3000.0 (+80.0%) |
| DT_VehicleMarket_WHL_05_Minigun | Price (Humvee.Minigun) | 4500.0 | 10000.0 | +5500.0 (+122.2%) |
| DT_VehicleMarket_WHL_05_RingTurret | Price (Humvee.MachineGun) | 3750.0 | 8500.0 | +4750.0 (+126.7%) |
| DT_VehicleMarket_WHL_07_ArmouredBattle | Price (Ural.Attack) | 6750.0 | 9500.0 | +2750.0 (+40.7%) |
| DT_VehicleMarket_WHL_07_Ural | Price (Ural.Battle) | 6000.0 | 7200.0 | +1200.0 (+20.0%) |
| DA_Buildable_MistralAA | Cost | 1000 | 650 | −350 (−35.0%) |
| DA_Buildable_STN_02 | Cost | 1500 | 1200 | −300 (−20.0%) |
| DA_Buildable_STN_03 | Cost | 150 | 600 | +450 (+300.0%) |
| DA_Buildable_STN_04 | Cost | 100 | 200 | +100 (+100.0%) |
| DA_Buildable_STN_05 | Cost | 150 | 650 | +500 (+333.3%) |

Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=DT_VehicleMarket

### Torque curve

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| CRV_Torque | FloatCurve.Keys[0].Value | 850.0 | 1200.0 | +350.0 (+41.2%) |
| CRV_Torque | FloatCurve.Keys[1].ArriveTangent | 0.4375 | 0.0 | −0.4375 (−100.0%) |
| CRV_Torque | FloatCurve.Keys[1].LeaveTangent | 0.4375 | 0.0 | −0.4375 (−100.0%) |
| CRV_Torque | FloatCurve.Keys[1].Value | 1000.0 | 1200.0 | +200.0 (+20.0%) |
| CRV_Torque | FloatCurve.Keys[2].ArriveTangent | 0.4375 | 0.1875 | −0.25 (−57.1%) |
| CRV_Torque | FloatCurve.Keys[2].LeaveTangent | 0.4375 | 0.1875 | −0.25 (−57.1%) |
| CRV_Torque | FloatCurve.Keys[4].ArriveTangent | 0.15 | -0.13095558 | −0.28095558 (−187.3%) |
| CRV_Torque | FloatCurve.Keys[4].LeaveTangent | 0.15 | -0.13095558 | −0.28095558 (−187.3%) |
| CRV_Torque | FloatCurve.Keys[6].Time | 4000.0 | 3750.0 | −250.0 (−6.2%) |
| CRV_Torque | FloatCurve.Keys[6].Value | 650.0 | 399.99997 | −250.00003 (−38.5%) |

### Other numeric changes

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DA_GameplaySystems_TNK_01_Heavy | ActiveZonesSettings.ActiveZones[1].WidgetLocation.Y | -40.0 | -85.0 | −45.0 (−112.5%) |
| DA_GameplaySystems_TNK_01_Heavy | ActiveZonesSettings.ActiveZones[4].WidgetLocation.Y | 40.0 | 85.0 | +45.0 (+112.5%) |
| DA_GameplaySystems_TNK_03 | ActiveZonesSettings.ActiveZones[1].WidgetLocation.Y | -40.0 | -85.0 | −45.0 (−112.5%) |
| DA_GameplaySystems_TNK_03 | ActiveZonesSettings.ActiveZones[4].WidgetLocation.Y | 40.0 | 85.0 | +45.0 (+112.5%) |
| DA_STN_02_Heavy_MainCannon_Stats | WeaponStats.InitialBulletSpeed | 85000.0 | 110000.0 | +25000.0 (+29.4%) |
| DA_STN_03_Heavy_MainBarrel_Stats | WeaponStats.WindupTime | 0.85 | 2.5 | +1.65 (+194.1%) |
| DA_VehicleInteractions_TNK_01_Heavy | InteractionTrackerPoints[6].Location.Y | -40.0 | -85.0 | −45.0 (−112.5%) |
| DA_VehicleInteractions_TNK_01_Heavy | InteractionTrackerPoints[8].Location.Y | 40.0 | 85.0 | +45.0 (+112.5%) |
| DA_VehicleInteractions_TNK_03 | InteractionTrackerPoints[5].Location.Y | -40.0 | -85.0 | −45.0 (−112.5%) |
| DA_VehicleInteractions_TNK_03 | InteractionTrackerPoints[6].Location.Y | 40.0 | 85.0 | +45.0 (+112.5%) |
| ID_ROT_02_Default | Dimensions.X | 4 | 5 | +1 (+25.0%) |
| ID_ROT_04_Default | Dimensions.X | 4 | 5 | +1 (+25.0%) |
| ID_ROT_04_MountedMachineGuns | Dimensions.X | 4 | 5 | +1 (+25.0%) |
| ID_TNK_01_AntiAir | Dimensions.X | 4 | 6 | +2 (+50.0%) |
| ID_TNK_01_Artillery | Dimensions.X | 4 | 6 | +2 (+50.0%) |
| ID_TNK_01_Heavy | Dimensions.X | 4 | 6 | +2 (+50.0%) |
| ID_WHL_01_Default | Dimensions.X | 4 | 3 | −1 (−25.0%) |
| ID_WHL_01_Default | Dimensions.Y | 4 | 2 | −2 (−50.0%) |
| ID_WHL_02_Default | Dimensions.Y | 4 | 3 | −1 (−25.0%) |
| ID_WHL_02_MachineGun | Dimensions.Y | 4 | 3 | −1 (−25.0%) |
| ID_WHL_02_Pickup | Dimensions.Y | 4 | 3 | −1 (−25.0%) |
| ID_WHL_05_Default | Dimensions.Y | 4 | 3 | −1 (−25.0%) |
| ID_WHL_05_MachineGun | Dimensions.Y | 4 | 3 | −1 (−25.0%) |
| ID_WHL_05_Minigun | Dimensions.Y | 4 | 3 | −1 (−25.0%) |
| Skin_BlackAndGold | Skin.DefaultCPD.AccentPrimaryUVInfo.Y | 1.35187 | 0.1 | −1.25187 (−92.6%) |
| WE_STN_01_Heavy_MountedMachineGun | ReloadSetupData.ReloadTime | 2.0 | 5.0 | +3.0 (+150.0%) |
| WE_STN_01_Heavy_MountedMachineGun | RestockSuppliesNeeded | 50 | 200 | +150 (+300.0%) |
| WE_STN_03_Heavy_MainBarrel | RestockSuppliesNeeded | 75 | 150 | +75 (+100.0%) |
| W_STN_01_MountedMachineGun | GamepadRotationSensitivity | 30.0 | 100.0 | +70.0 (+233.3%) |
| W_STN_01_MountedMachineGun | HUDScopeBlurAlpha | 2.4254257e-38 | 1.0 | +1.0 |
| W_STN_01_MountedMachineGun | InitialWeaponPossessFovLerpTime | 1.83671e-40 | 0.22 | +0.22 |
| W_STN_02_MainCannon | GamepadRotationSensitivity | 50.0 | 90.0 | +40.0 (+80.0%) |
| W_STN_03_MainBarrel | GamepadRotationSensitivity | 15.0 | 50.0 | +35.0 (+233.3%) |
| W_STN_05_MainBarrel | GamepadRotationSensitivity | 15.0 | 50.0 | +35.0 (+233.3%) |
| W_SUV_RingTurret | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_TNK_01_Heavy_MountedMachineGun | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_WHL_05_Humvee_RingMinigun | GamepadRotationSensitivity | 75.0 | 100.0 | +25.0 (+33.3%) |
| W_WHL_05_Humvee_RingTurret | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_WHL_07_Ural_RingTurret_L | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_WHL_07_Ural_RingTurret_R | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |

Showing 40 of 45 rows. The 2 rows with Season 1 values near 1e-38 or below have no percentage: [`W_STN_01_MountedMachineGun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/Weapon/W_STN_01_MountedMachineGun.json). Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=Properties

The audio event [`AE_Vehicle_Exit_ROT_Littlebird`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/Audio/Events/AE_Vehicle_Exit_ROT_Littlebird.json) also has one unnamed value that goes from 0.505 to 50.5. That looks like a rescale from a 0–1 range to 0–100, so it is not in the table.

### Skin values

[`Skin_DigitalWood`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_DigitalWood.json) has 59 numeric changes (UV and pattern values). They are not tabulated here. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=Skin_DigitalWood

### Non-numeric changes

366 changed values are not numeric. The most common properties:

| Property | Changes | Example asset | Season 1 | Season 2 |
|---|---|---|---|---|
| bCheckIfAboveThreshold | 205 | DA_FWG_01_GameplaySystems | true | false |
| ObjectPath | 78 | DA_Vehicle_BrakingSurface_WHL_06 | /WHL_06/Audio/Wavs/Skidding_WheelSpin_Braking/Dirt/SFX_Vehicles_Land_WHL01_DirtWheelBraki… | /Game/Audio/Vehicles/Shared/Surface/SFX_Vehicles_Land_WHL01_DirtWheelBraking_01.0 |
| ObjectName | 33 | DA_Vehicle_Skidding_Fast_WHL_01 | SoundWave'SFX_Vehicles_Land_WHL_02_Skidding_Asphalt' | SoundWave'SFX_Vehicles_Land_WHL_02_Skidding_Asphalt1' |
| TagName | 11 | DT_EntityData_UI_TNK01 | Attribute.Meta.XP.Role.Support | Attribute.Meta.XP.Role.Driver |
| SettingBehavior | 8 | IMC_LandVehicles_Driver | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings |
| Name | 6 | IMC_RotaryVehicles_Driver | Input.NamedActions.Vehicle.FireFlares | Input.NamedActions.Vehicle.FireCountermeasures |
| KeyName | 5 | IMC_MountedGunnerInput | Gamepad_LeftTriggerAxis | Gamepad_LeftTrigger |
| Key | 4 | DT_EntityData_UI_Vehicles_ROT_04 | Vehicle.Name.Rotary.Blackhawk | Vehicle.Name.Rotary.Z20 |
| SourceString | 4 | DT_EntityData_UI_Vehicles_WHL_02_RingTurret | - 1 Driver + 4 Passengers  / - Optional Logistics Crates | - 2 Crew + 3 Passengers  / - Optional Logistics Crates |
| LocalizedString | 4 | DT_EntityData_UI_Vehicles_WHL_02_RingTurret | - 1 Driver + 4 Passengers  / - Optional Logistics Crates | - 2 Crew + 3 Passengers  / - Optional Logistics Crates |
| GroupRules | 3 | VP_SPW_Radar | — | {"_aaabbmnjfiefjaocbjbnl":{"TagName":"Vehicle.DestructibleMesh.Radar.Deployed"},"_aaaaomn… |
| TangentMode | 2 | CRV_Torque | RCTM_Auto | RCTM_User |

## New in Season 2

151 assets were added. Identification is the type, the vehicle folder in the path, and the export count.

| Asset | Type | Vehicle folder | Exports |
|---|---|---|---|
| AE_Vehicle_SupplyCrate_Deploy_Fail | CrosstalkAudioEvent | SupplyCrates | 2 |
| CRV_BrakeEngagement_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_ClutchEngagement_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_CollisionDamage_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_ForeignVehicleCollisionDamage_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_FreeLookPitchRange_STN_06 | CurveFloat | STN_06 | 1 |
| CRV_FreeLookPitchRange_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_SteerLimitVariant_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_SteerSpeedVariant_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_ThrottleEngagement_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_Torque_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_VehicleCollisionDamage_WHL_08 | CurveFloat | WHL_08 | 1 |
| CRV_WHL_08_SpeedCurveFOV | CurveFloat | WHL_08 | 1 |
| DA_ArcadeControls_WHL_08 | MWheeledVehicleArcadeDataAsset | WHL_08 | 1 |
| DA_Buildable_MGNest | WDBuildableDataAsset | STN_06 | 2 |
| DA_CameraBehaviour_STN_06 | MLandVehicleSpringArmDataAsset | STN_06 | 1 |
| DA_Characteristics_WHL_08 | MWheeledVehicleCharacteristicsDataAsset | WHL_08 | 1 |
| DA_Config_STN_06 | BHBaseVehicleConfigDataAsset | STN_06 | 1 |
| DA_Config_TNK_04 | MTrackedVehicleConfigDataAsset | TNK_04 | 1 |
| DA_Config_WHL_08 | MWheeledVehicleConfigDataAsset | WHL_08 | 1 |
| DA_EngineTransmission_WHL_08 | MWheeledVehicleEngineTransmissionDataAsset | WHL_08 | 1 |
| DA_FP_CameraBehaviour_WHL_08 | MLandVehicleSpringArmDataAsset | WHL_08 | 1 |
| DA_FrontAxle_WHL_08 | MWheeledVehicleAxlesDataAsset | WHL_08 | 1 |
| DA_FrontWheels_WHL_08 | MWheeledVehicleWheelDataAsset | WHL_08 | 1 |
| DA_GameplaySystems_STN_06 | WDVehicleGameplayComponentsDataAsset | STN_06 | 3 |
| DA_GameplaySystems_TNK_04 | WDVehicleGameplayComponentsDataAsset | TNK_04 | 28 |
| DA_GameplaySystems_WHL_08 | WDVehicleGameplayComponentsDataAsset | WHL_08 | 61 |
| DA_InputControls_TNK_04 | MTrackedInputControlsDataAsset | TNK_04 | 1 |
| DA_Input_WHL_08 | MWheeledVehicleInputDataAsset | WHL_08 | 1 |
| DA_MGNest_Stages | BuildingStagesDefinition | STN_06 | 1 |
| DA_MWSY_001_Heavy_MountedMachineGun_Stats | WDWeaponStatsData | — | 1 |
| DA_MWSY_001_MountedMachineGun_Audio | WDAudioData | — | 1 |
| DA_PredictionSettings_TNK_04 | MVehiclePredictionSettings_Tracked | TNK_04 | 1 |
| DA_PredictionSettings_WHL_08 | MVehiclePredictionSettings_Wheeled | WHL_08 | 1 |
| DA_RadialWheelSlotType_MGNest | WDUIRadialWheelSlotTypeDataAsset | STN_06 | 1 |
| DA_RearAxle_WHL_08 | MWheeledVehicleAxlesDataAsset | WHL_08 | 1 |
| DA_RearWheels_WHL_08 | MWheeledVehicleWheelDataAsset | WHL_08 | 1 |
| DA_STN_06_CameraBehaviour_FP | MLandVehicleSpringArmDataAsset | STN_06 | 1 |
| DA_SeatSettings_STN_06 | BHSeatSettingsDataAsset | STN_06 | 1 |
| DA_SeatSettings_WHL_08 | BHSeatSettingsDataAsset | WHL_08 | 1 |
| DA_SeatSettings_WHL_08_RingTurret | BHSeatSettingsDataAsset | WHL_08_RingTurret | 1 |
| DA_SimpleTireModel_WHL_08 | MWheeledVehicleTireModelSimpleDataAsset | WHL_08 | 1 |
| DA_TNK_04_Audio | WDAudioData | TNK_04 | 1 |
| DA_TNK_04_Camera_FP | MVehicleSpringArmDataAsset | TNK_04 | 1 |
| DA_TNK_04_Camera_TP | MVehicleSpringArmDataAsset | TNK_04 | 1 |
| DA_TNK_04_DynamicsData | MTrackedVehicleDynamicsData | TNK_04 | 1 |
| DA_TNK_04_EngineData | MTrackedVehicleEngineData | TNK_04 | 1 |
| DA_TNK_04_MachineGun_Weapon_Audio | WDAudioData | TNK_04 | 1 |
| DA_TNK_04_MountedMachineGun_SeatSettings | BHSeatSettingsDataAsset | TNK_04 | 1 |
| DA_TNK_04_SeatSettings | BHSeatSettingsDataAsset | TNK_04 | 1 |
| DA_TNK_04_Stats | WDVehicleStatsDataAsset | TNK_04 | 7 |
| DA_TNK_04_SuspensionData | MTrackedVehicleSuspensionData | TNK_04 | 1 |
| DA_TNK_04_Weapon_Audio | WDAudioData | TNK_04 | 1 |
| DA_TNK_04_Weapon_Stats | WDWeaponStatsData | TNK_04 | 1 |
| DA_TNK_04_WheelData | MTrackedVehicleWheelData | TNK_04 | 1 |
| DA_TP_CameraBehaviour_WHL_08 | MLandVehicleSpringArmDataAsset | WHL_08 | 1 |
| DA_VehicleInteractionContext_TNK_04 | WDVehicleInteractionContextsData | TNK_04 | 1 |
| DA_VehicleInteractionContext_WHL_08 | WDVehicleInteractionContextsData | WHL_08 | 1 |
| DA_VehicleInteractionContext_WHL_08_RingTurret | WDVehicleInteractionContextsData | WHL_08_RingTurret | 1 |
| DA_VehicleInteractions_STN_06 | WDVehicleInteractionsDataAsset | STN_06 | 1 |
| DA_VehicleInteractions_TNK_04 | WDVehicleInteractionsDataAsset | TNK_04 | 1 |
| DA_VehicleInteractions_WHL_08 | WDVehicleInteractionsDataAsset | WHL_08 | 1 |
| DA_VehicleInteractions_WHL_08_RingTurret | WDVehicleInteractionsDataAsset | WHL_08_RingTurret | 1 |
| DA_VehicleSensor_TNK_04 | MVehicleSensorsDataAsset | TNK_04 | 1 |
| DA_VehicleSensors_WHL_08 | MVehicleSensorsDataAsset | WHL_08 | 1 |
| DA_Vehicle_BrakingSurface_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_Skidding_Fast_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_Skidding_Medium_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_Skidding_Slow_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_Surface_Fast_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_Surface_Medium_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_Surface_Slow_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicle_WheelSpinSurface_WHL_08 | WDAudioData | WHL_08 | 1 |
| DA_Vehicles_TNK_04_BrakingSurface | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_Skidding_Fast | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_Skidding_Medium | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_Skidding_Slow | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_Surface_Fast | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_Surface_Medium | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_Surface_Slow | WDAudioData | TNK_04 | 1 |
| DA_Vehicles_TNK_04_WheelSpinSurface | WDAudioData | TNK_04 | 1 |
| DA_WHL_08_Audio | WDAudioData | WHL_08 | 1 |
| DA_WHL_08_InputControls | MLandInputControlsDataAsset | WHL_08 | 1 |
| DA_WHL_08_RingTurretStats | WDVehicleStatsDataAsset | WHL_08_RingTurret | 7 |
| DA_WHL_08_Stats | WDVehicleStatsDataAsset | WHL_08 | 7 |
| DT_Buildables_STN_06 | DataTable | STN_06 | 1 |
| DT_Cosmetics_Season02_Skins | DataTable | — | 1 |
| DT_EntityData_Ext_VehicleSmoke | DataTable | VehicleSmoke | 1 |
| DT_EntityData_UI_TNK04 | DataTable | TNK_04 | 1 |
| DT_EntityData_UI_Vehicles_STN_06 | DataTable | STN_06 | 1 |
| DT_EntityData_UI_Vehicles_WHL_08 | DataTable | WHL_08 | 1 |
| DT_EntityData_UI_Vehicles_WHL_08_RingTurret | DataTable | WHL_08_RingTurret | 1 |
| DT_GlobalDamage_VehicleData_STN_06 | DataTable | STN_06 | 1 |
| DT_GlobalDamage_VehicleData_TNK_04 | DataTable | TNK_04 | 1 |
| DT_GlobalDamage_VehicleData_WHL_08 | DataTable | WHL_08 | 1 |
| DT_GlobalDamage_VehicleData_WHL_08_RingTurret | DataTable | WHL_08_RingTurret | 1 |
| DT_RadialWheelSlotType_BuildToolData | DataTable | STN_06 | 1 |
| DT_VehicleCrosshair_STN06 | DataTable | STN_06 | 1 |
| DT_VehicleCrosshair_TNK04 | DataTable | TNK_04 | 1 |
| DT_VehicleMarket_TNK_04 | DataTable | TNK_04 | 1 |
| DT_VehicleMarket_WHL_08 | DataTable | WHL_08 | 1 |
| DT_VehicleMarket_WHL_08_RingTurret | DataTable | WHL_08_RingTurret | 1 |
| DT_VehicleSeatOverrides_STN_06 | DataTable | STN_06 | 1 |
| DT_VendorData_Ext_VehicleSmoke | DataTable | VehicleSmoke | 1 |
| IA_Vehicle_FireCountermeasures | BHInputAction | Inputs | 1 |
| ID_MWSY_001_MountedMachineGun | BHInventoryItemDefinition | — | 2 |
| ID_MountedMachineGun_TNK_04 | BHInventoryItemDefinition | Weapons | 2 |
| ID_TNK_04 | BHInventoryItemDefinition | TNK_04 | 3 |
| ID_VehicleSmoke | BHInventoryItemDefinition | VehicleSmoke | 4 |
| ID_VehicleTurretMachineGun_TNK_04 | BHInventoryItemDefinition | Weapons | 2 |
| ID_VehicleTurret_TNK_04 | BHInventoryItemDefinition | Weapons | 2 |
| ID_WHL_08_Default | BHInventoryItemDefinition | WHL_08 | 3 |
| ID_WHL_08_MachineGun | BHInventoryItemDefinition | WHL_08_RingTurret | 3 |
| ID_WHL_08_RingTurret | BHInventoryItemDefinition | Weapons | 2 |
| MWSY_001 | GameFeatureData | — | 2 |
| MWSY_002 | GameFeatureData | — | 1 |
| STN_06 | GameFeatureData | STN_06 | 3 |
| Season02_SkinsData | GameFeatureData | — | 2 |
| Skin_ChocolateChip | WDSkinDataAsset | — | 1 |
| TNK_04 | GameFeatureData | TNK_04 | 4 |
| VP_STN_06 | ModularVehiclePlatform | STN_06 | 9 |
| VP_STN_06_Body | ModularVehiclePart | STN_06 | 2 |
| VP_STN_06_Seats | ModularVehiclePart | STN_06 | 2 |
| VP_STN_06_Turret | ModularVehiclePart | STN_06 | 7 |
| VP_TNK_04 | ModularVehiclePlatform | TNK_04 | 11 |
| VP_TNK_04_MountedMachineGun | ModularVehiclePart | TNK_04 | 7 |
| VP_TNK_04_Turret | ModularVehiclePart | TNK_04 | 8 |
| VP_WHL_08 | ModularVehiclePlatform | WHL_08 | 10 |
| VP_WHL_08_MainBody_Default | ModularVehiclePart | WHL_08 | 6 |
| VP_WHL_08_MainBody_MachineGun | ModularVehiclePart | WHL_08_RingTurret | 7 |
| VP_WHL_08_RingTurret | ModularVehiclePart | WHL_08_RingTurret | 5 |
| VP_WHL_08_Seats | ModularVehiclePart | WHL_08 | 2 |
| VP_WHL_08_Turret_Seats | ModularVehiclePart | WHL_08_RingTurret | 2 |
| VP_WHL_08_Wheels | ModularVehiclePart | WHL_08 | 3 |
| VV_STN_06 | ModularVehicleVariant | STN_06 | 1 |
| VV_TNK_04 | ModularVehicleVariant | TNK_04 | 1 |
| VV_WHL_08_Default | ModularVehicleVariant | WHL_08 | 1 |
| VV_WHL_08_RingTurret | ModularVehicleVariant | WHL_08_RingTurret | 1 |
| VehicleSmoke | GameFeatureData | VehicleSmoke | 3 |
| Vehicle_WHL_08_REV | REVModelAsset | WHL_08 | 1 |
| WE_STN_06_MountedMachineGun | WDVehicleWeaponExtensionDataAsset | STN_06 | 1 |
| WE_TNK_04 | WDVehicleWeaponExtensionDataAsset | TNK_04 | 1 |
| WE_TNK_04_MachineGun | WDVehicleWeaponExtensionDataAsset | TNK_04 | 1 |
| WE_TNK_04_MountedMachineGun | WDVehicleWeaponExtensionDataAsset | TNK_04 | 1 |
| WE_WHL_08_RingTurret | WDVehicleWeaponExtensionDataAsset | WHL_08_RingTurret | 1 |
| WHL_08 | GameFeatureData | WHL_08 | 4 |
| WHL_08_RingTurret | GameFeatureData | WHL_08_RingTurret | 2 |
| W_STN_06_MountedMachineGun | WDVehicleWeaponDataAsset | STN_06 | 1 |
| W_TNK_04 | WDVehicleWeaponDataAsset | TNK_04 | 1 |
| W_TNK_04_MountedMachineGun | WDVehicleWeaponDataAsset | TNK_04 | 1 |
| W_WHL_08_RingTurret | WDVehicleWeaponDataAsset | WHL_08_RingTurret | 1 |

## Removed in Season 2

| Asset | Type | Path |
|---|---|---|
| IA_Vehicle_FireFlares | BHInputAction | Wardogs/Content/Vehicles/Inputs/IA_Vehicle_FireFlares.json |

Removed assets are not on GitHub, so there are no links.

## Moved

None.

## See also

- [Vehicle stats and damage tables]({{ '/content/Wardogs_AllVehicles_Stats_Damage_v1.html' | relative_url }}#season-02-update-2026-10-15), Season 02 update
- [Vehicles]({{ '/content/Wardogs_Vehicles_v2.html' | relative_url }}#season-02-update-2026-10-15), Season 02 update
- [Vehicles game feature]({{ '/game-features/Wardogs_GameFeatures_Vehicles_v2.html' | relative_url }}#season-02-update-2026-10-15), Season 02 update
- [Vehiclesmith game feature]({{ '/game-features/Wardogs_GameFeatures_Vehiclesmith_v2.html' | relative_url }}#season-02-update-2026-10-15), Season 02 update

Full change browser for this area: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=

