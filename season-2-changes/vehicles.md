---
title: "Vehicles changes"
parent: "Season 2 Changes"
nav_order: 4
description: "Vehicle changes from Season 1 to Season 2: 151 assets added, 1 removed, 331 modified with real changes, 3,886 property changes."
---

# Vehicles changes

{{ page.description }}

Counts come from `assets/data/season-diff/index.json` and `vehicles.json`. Values are copied as stored. Signed deltas and percentages are calculated from the stored values. Noise-only assets are skipped: renamed keys, swapped key names or shifted references from the different Season 1 export.

| Measure | Count |
|---|---|
| Assets added | 151 |
| Assets removed | 1 |
| Assets modified with real changes | 331 |
| Assets modified, noise only (skipped) | 131 |
| Assets moved | 0 |
| Property changes (index.json) | 3,886 |

The change list for these assets holds 3,904 records. The index figure equals that total minus `removed_values` (18).

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

`DA_Phalanx_Stages` has 1,252 change records and `DA_Mistral_AA_Stages` has 592. Most are `CriticalHitSpots` array entries compared by index. That is array churn, not a balance change, so these rows are not tabulated. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=DA_Phalanx_Stages

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
| DA_RearWheels_WHL_05_Humvee | RelaxationDamper.Values | 12000.0 | 6250.0 | −5750.0 (−47.9%) |
| DA_RearWheels_WHL_06_DuneBuggy | BrakeTorque.Values | 16000.0 | 13000.0 | −3000.0 (−18.8%) |
| DA_RearWheels_WHL_06_DuneBuggy | BrakeTorque.Values[1] | 12000.0 | 9000.0 | −3000.0 (−25.0%) |
| DA_SPW_01_WheelData | DampingRebound | 12000.0 | 17000.0 | +5000.0 (+41.7%) |
| DA_TNK_01_WheelData | DampingRebound | 12000.0 | 17000.0 | +5000.0 (+41.7%) |
| DA_WHL_01_FrontAxle | WheelSetup[frontLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_WHL_01_FrontAxle | WheelSetup[frontRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_WHL_01_RearAxle | WheelSetup[rearLWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |
| DA_WHL_01_RearAxle | WheelSetup[rearRWheelSpin_J].DeflateThreshold | 0.5 | 0.55 | +0.05 (+10.0%) |

Showing all 34 numeric changes in wheel, axle and suspension assets. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=Wheel

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
| CRV_Torque | FloatCurve.Keys[5].ArriveTangent | 0.036315992 | -0.84 | −0.876315992 (−2413.0%) |
| CRV_Torque | FloatCurve.Keys[5].LeaveTangent | 0.036315992 | -0.84 | −0.876315992 (−2413.0%) |
| CRV_Torque | FloatCurve.Keys[5].Time | 3000.0 | 3100.0 | +100.0 (+3.3%) |
| CRV_Torque | FloatCurve.Keys[5].Value | 1500.0 | 1000.0 | −500.0 (−33.3%) |
| CRV_Torque | FloatCurve.Keys[6].ArriveTangent | -0.779376 | 0.0 | +0.779376 (+100.0%) |
| CRV_Torque | FloatCurve.Keys[6].LeaveTangent | -0.779376 | 0.0 | +0.779376 (+100.0%) |
| CRV_Torque | FloatCurve.Keys[6].Time | 3550.0 | 3750.0 | +200.0 (+5.6%) |
| CRV_Torque | FloatCurve.Keys[6].Value | 1335.0 | 399.99997 | −935.00003 (−70.0%) |

### Other numeric changes

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| AE_Vehicle_Exit_ROT_Littlebird | unnamed property (`_aaabhgndclheajnnlna`) | 0.505 | 50.5 | +49.995 (+9900.0%) |
| DA_GameplaySystems_SPW | …CountermeasureSettings.unnamed property (`_aaaanaajodikgainmio`).unnamed property (`_aaa… | 10.0 | 16.0 | +6.0 (+60.0%) |
| DA_GameplaySystems_TNK_01_Heavy | ActiveZonesSettings.ActiveZones[1].WidgetLocation.Y | -40.0 | -85.0 | −45.0 (−112.5%) |
| DA_GameplaySystems_TNK_01_Heavy | ActiveZonesSettings.ActiveZones[4].WidgetLocation.Y | 40.0 | 85.0 | +45.0 (+112.5%) |
| DA_GameplaySystems_TNK_01_Heavy | …CountermeasureSettings.unnamed property (`_aaaanaajodikgainmio`).unnamed property (`_aaa… | 10.0 | 16.0 | +6.0 (+60.0%) |
| DA_GameplaySystems_TNK_03 | ActiveZonesSettings.ActiveZones[1].WidgetLocation.Y | -40.0 | -85.0 | −45.0 (−112.5%) |
| DA_GameplaySystems_TNK_03 | ActiveZonesSettings.ActiveZones[4].WidgetLocation.Y | 40.0 | 85.0 | +45.0 (+112.5%) |
| DA_GameplaySystems_TNK_03 | …CountermeasureSettings.unnamed property (`_aaaanaajodikgainmio`).unnamed property (`_aaa… | 10.0 | 16.0 | +6.0 (+60.0%) |
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
| Skin_BlackAndGold | Skin.DefaultCPD.AccentPrimaryUVInfo.Y | 1.35187 | 0.1 | −1.25187 (−92.6%) |
| WE_STN_01_Heavy_MountedMachineGun | ReloadSetupData.ReloadTime | 2.0 | 5.0 | +3.0 (+150.0%) |
| WE_STN_01_Heavy_MountedMachineGun | RestockSuppliesNeeded | 50 | 200 | +150 (+300.0%) |
| WE_STN_03_Heavy_MainBarrel | RestockSuppliesNeeded | 75 | 150 | +75 (+100.0%) |
| W_STN_01_MountedMachineGun | GamepadRotationSensitivity | 30.0 | 100.0 | +70.0 (+233.3%) |
| W_STN_01_MountedMachineGun | HUDScopeBlurAlpha | 2.4254257e-38 | 1.0 | +1.0 (+4122987564615976242944986667581790224384.0%) |
| W_STN_01_MountedMachineGun | InitialWeaponPossessFovLerpTime | 1.83671e-40 | 0.22 | +0.22 (+119779388145107283385640262840580418043904.0%) |
| W_STN_02_MainCannon | GamepadRotationSensitivity | 50.0 | 90.0 | +40.0 (+80.0%) |
| W_STN_03_MainBarrel | GamepadRotationSensitivity | 15.0 | 50.0 | +35.0 (+233.3%) |
| W_STN_05_MainBarrel | GamepadRotationSensitivity | 15.0 | 50.0 | +35.0 (+233.3%) |
| W_SUV_RingTurret | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_TNK_01_Heavy_MountedMachineGun | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_WHL_05_Humvee_RingMinigun | GamepadRotationSensitivity | 75.0 | 100.0 | +25.0 (+33.3%) |
| W_WHL_05_Humvee_RingTurret | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_WHL_07_Ural_RingTurret_L | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |
| W_WHL_07_Ural_RingTurret_R | GamepadRotationSensitivity | 35.0 | 80.0 | +45.0 (+128.6%) |

Showing 40 of 49 rows. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=Properties

### Skin values

`Skin_DigitalWood` has 59 numeric changes (UV and pattern values). They are not tabulated here. Browser link: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=Skin_DigitalWood

### Non-numeric changes

378 changed values are not numeric. The most common properties:

| Property | Changes | Example asset | Season 1 | Season 2 |
|---|---|---|---|---|
| bCheckIfAboveThreshold | 205 | DA_FWG_01_GameplaySystems | true | false |
| ObjectPath | 78 | DA_Vehicle_BrakingSurface_WHL_06 | /WHL_06/Audio/Wavs/Skidding_WheelSpin_Braking/Dirt/SFX_Vehicles_Land_WHL01_DirtWheelBraki… | /Game/Audio/Vehicles/Shared/Surface/SFX_Vehicles_Land_WHL01_DirtWheelBraking_01.0 |
| ObjectName | 33 | DA_Vehicle_Skidding_Fast_WHL_01 | SoundWave'SFX_Vehicles_Land_WHL_02_Skidding_Asphalt' | SoundWave'SFX_Vehicles_Land_WHL_02_Skidding_Asphalt1' |
| TagName | 14 | DA_GameplaySystems_SPW | Id.Item.Flares | Id.Item.VehicleSmoke |
| SettingBehavior | 8 | IMC_LandVehicles_Driver | EPlayerMappableKeySettingBehaviors::OverrideSettings | EPlayerMappableKeySettingBehaviors::IgnoreSettings |
| YawJointSocket | 7 | W_ROT_04_MountedMachineGun_L | TurretSkeleton_L | turretYaw_J |
| Name | 6 | IMC_RotaryVehicles_Driver | Input.NamedActions.Vehicle.FireFlares | Input.NamedActions.Vehicle.FireCountermeasures |
| KeyName | 5 | IMC_MountedGunnerInput | Gamepad_LeftTriggerAxis | Gamepad_LeftTrigger |
| Key | 4 | DT_EntityData_UI_Vehicles_ROT_04 | Vehicle.Name.Rotary.Blackhawk | Vehicle.Name.Rotary.Z20 |
| SourceString | 4 | DT_EntityData_UI_Vehicles_WHL_02_RingTurret | - 1 Driver + 4 Passengers  / - Optional Logistics Crates | - 2 Crew + 3 Passengers  / - Optional Logistics Crates |
| LocalizedString | 4 | DT_EntityData_UI_Vehicles_WHL_02_RingTurret | - 1 Driver + 4 Passengers  / - Optional Logistics Crates | - 2 Crew + 3 Passengers  / - Optional Logistics Crates |
| TangentMode | 3 | CRV_Torque | RCTM_Auto | RCTM_User |

## New in Season 2

151 assets were added. Identification is the type, the vehicle folder in the path, and the export count.

| Asset | Type | Vehicle folder | Exports |
|---|---|---|---|
| [AE_Vehicle_SupplyCrate_Deploy_Fail](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/Audio/Events/AE_Vehicle_SupplyCrate_Deploy_Fail.json) | CrosstalkAudioEvent | SupplyCrates | 2 |
| [CRV_BrakeEngagement_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_BrakeEngagement_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_ClutchEngagement_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_ClutchEngagement_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_CollisionDamage_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_CollisionDamage_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_ForeignVehicleCollisionDamage_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_ForeignVehicleCollisionDamage_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_FreeLookPitchRange_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Curves/CRV_FreeLookPitchRange_STN_06.json) | CurveFloat | STN_06 | 1 |
| [CRV_FreeLookPitchRange_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_FreeLookPitchRange_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_SteerLimitVariant_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_SteerLimitVariant_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_SteerSpeedVariant_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_SteerSpeedVariant_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_ThrottleEngagement_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_ThrottleEngagement_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_Torque_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_Torque_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_VehicleCollisionDamage_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_VehicleCollisionDamage_WHL_08.json) | CurveFloat | WHL_08 | 1 |
| [CRV_WHL_08_SpeedCurveFOV](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Curves/CRV_WHL_08_SpeedCurveFOV.json) | CurveFloat | WHL_08 | 1 |
| [DA_ArcadeControls_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_ArcadeControls_WHL_08.json) | MWheeledVehicleArcadeDataAsset | WHL_08 | 1 |
| [DA_Buildable_MGNest](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DA_Buildable_MGNest.json) | WDBuildableDataAsset | STN_06 | 2 |
| [DA_CameraBehaviour_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Data/DA_CameraBehaviour_STN_06.json) | MLandVehicleSpringArmDataAsset | STN_06 | 1 |
| [DA_Characteristics_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_Characteristics_WHL_08.json) | MWheeledVehicleCharacteristicsDataAsset | WHL_08 | 1 |
| [DA_Config_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Data/DA_Config_STN_06.json) | BHBaseVehicleConfigDataAsset | STN_06 | 1 |
| [DA_Config_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_Config_TNK_04.json) | MTrackedVehicleConfigDataAsset | TNK_04 | 1 |
| [DA_Config_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_Config_WHL_08.json) | MWheeledVehicleConfigDataAsset | WHL_08 | 1 |
| [DA_EngineTransmission_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_EngineTransmission_WHL_08.json) | MWheeledVehicleEngineTransmissionDataAsset | WHL_08 | 1 |
| [DA_FP_CameraBehaviour_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_FP_CameraBehaviour_WHL_08.json) | MLandVehicleSpringArmDataAsset | WHL_08 | 1 |
| [DA_FrontAxle_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/AxleData/DA_FrontAxle_WHL_08.json) | MWheeledVehicleAxlesDataAsset | WHL_08 | 1 |
| [DA_FrontWheels_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/AxleData/DA_FrontWheels_WHL_08.json) | MWheeledVehicleWheelDataAsset | WHL_08 | 1 |
| [DA_GameplaySystems_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Data/DA_GameplaySystems_STN_06.json) | WDVehicleGameplayComponentsDataAsset | STN_06 | 3 |
| [DA_GameplaySystems_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_GameplaySystems_TNK_04.json) | WDVehicleGameplayComponentsDataAsset | TNK_04 | 28 |
| [DA_GameplaySystems_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_GameplaySystems_WHL_08.json) | WDVehicleGameplayComponentsDataAsset | WHL_08 | 61 |
| [DA_InputControls_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_InputControls_TNK_04.json) | MTrackedInputControlsDataAsset | TNK_04 | 1 |
| [DA_Input_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_Input_WHL_08.json) | MWheeledVehicleInputDataAsset | WHL_08 | 1 |
| [DA_MGNest_Stages](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DA_MGNest_Stages.json) | BuildingStagesDefinition | STN_06 | 1 |
| [DA_MWSY_001_Heavy_MountedMachineGun_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_001/Content/Weapons/DA_MWSY_001_Heavy_MountedMachineGun_Stats.json) | WDWeaponStatsData | — | 1 |
| [DA_MWSY_001_MountedMachineGun_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_001/Content/Data/DA_MWSY_001_MountedMachineGun_Audio.json) | WDAudioData | — | 1 |
| [DA_PredictionSettings_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_PredictionSettings_TNK_04.json) | MVehiclePredictionSettings_Tracked | TNK_04 | 1 |
| [DA_PredictionSettings_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_PredictionSettings_WHL_08.json) | MVehiclePredictionSettings_Wheeled | WHL_08 | 1 |
| [DA_RadialWheelSlotType_MGNest](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DA_RadialWheelSlotType_MGNest.json) | WDUIRadialWheelSlotTypeDataAsset | STN_06 | 1 |
| [DA_RearAxle_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/AxleData/DA_RearAxle_WHL_08.json) | MWheeledVehicleAxlesDataAsset | WHL_08 | 1 |
| [DA_RearWheels_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/AxleData/DA_RearWheels_WHL_08.json) | MWheeledVehicleWheelDataAsset | WHL_08 | 1 |
| [DA_STN_06_CameraBehaviour_FP](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Data/DA_STN_06_CameraBehaviour_FP.json) | MLandVehicleSpringArmDataAsset | STN_06 | 1 |
| [DA_SeatSettings_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Data/DA_SeatSettings_STN_06.json) | BHSeatSettingsDataAsset | STN_06 | 1 |
| [DA_SeatSettings_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_SeatSettings_WHL_08.json) | BHSeatSettingsDataAsset | WHL_08 | 1 |
| [DA_SeatSettings_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Data/RingTurretDefender/DA_SeatSettings_WHL_08_RingTurret.json) | BHSeatSettingsDataAsset | WHL_08_RingTurret | 1 |
| [DA_SimpleTireModel_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/AxleData/DA_SimpleTireModel_WHL_08.json) | MWheeledVehicleTireModelSimpleDataAsset | WHL_08 | 1 |
| [DA_TNK_04_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_TNK_04_Audio.json) | WDAudioData | TNK_04 | 1 |
| [DA_TNK_04_Camera_FP](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_Camera_FP.json) | MVehicleSpringArmDataAsset | TNK_04 | 1 |
| [DA_TNK_04_Camera_TP](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_Camera_TP.json) | MVehicleSpringArmDataAsset | TNK_04 | 1 |
| [DA_TNK_04_DynamicsData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_DynamicsData.json) | MTrackedVehicleDynamicsData | TNK_04 | 1 |
| [DA_TNK_04_EngineData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_EngineData.json) | MTrackedVehicleEngineData | TNK_04 | 1 |
| [DA_TNK_04_MachineGun_Weapon_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/WeaponExtensions/MachineGun/DA_TNK_04_MachineGun_Weapon_Audio.json) | WDAudioData | TNK_04 | 1 |
| [DA_TNK_04_MountedMachineGun_SeatSettings](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/MountedMachineGun/DA_TNK_04_MountedMachineGun_SeatSettings.json) | BHSeatSettingsDataAsset | TNK_04 | 1 |
| [DA_TNK_04_SeatSettings](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_SeatSettings.json) | BHSeatSettingsDataAsset | TNK_04 | 1 |
| [DA_TNK_04_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_Stats.json) | WDVehicleStatsDataAsset | TNK_04 | 7 |
| [DA_TNK_04_SuspensionData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_SuspensionData.json) | MTrackedVehicleSuspensionData | TNK_04 | 1 |
| [DA_TNK_04_Weapon_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/WeaponExtensions/DA_TNK_04_Weapon_Audio.json) | WDAudioData | TNK_04 | 1 |
| [DA_TNK_04_Weapon_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/WeaponExtensions/DA_TNK_04_Weapon_Stats.json) | WDWeaponStatsData | TNK_04 | 1 |
| [DA_TNK_04_WheelData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_TNK_04_WheelData.json) | MTrackedVehicleWheelData | TNK_04 | 1 |
| [DA_TP_CameraBehaviour_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_TP_CameraBehaviour_WHL_08.json) | MLandVehicleSpringArmDataAsset | WHL_08 | 1 |
| [DA_VehicleInteractionContext_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_VehicleInteractionContext_TNK_04.json) | WDVehicleInteractionContextsData | TNK_04 | 1 |
| [DA_VehicleInteractionContext_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_VehicleInteractionContext_WHL_08.json) | WDVehicleInteractionContextsData | WHL_08 | 1 |
| [DA_VehicleInteractionContext_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Data/RingTurretDefender/DA_VehicleInteractionContext_WHL_08_RingTurret.json) | WDVehicleInteractionContextsData | WHL_08_RingTurret | 1 |
| [DA_VehicleInteractions_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Data/DA_VehicleInteractions_STN_06.json) | WDVehicleInteractionsDataAsset | STN_06 | 1 |
| [DA_VehicleInteractions_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_VehicleInteractions_TNK_04.json) | WDVehicleInteractionsDataAsset | TNK_04 | 1 |
| [DA_VehicleInteractions_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_VehicleInteractions_WHL_08.json) | WDVehicleInteractionsDataAsset | WHL_08 | 1 |
| [DA_VehicleInteractions_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Data/RingTurretDefender/DA_VehicleInteractions_WHL_08_RingTurret.json) | WDVehicleInteractionsDataAsset | WHL_08_RingTurret | 1 |
| [DA_VehicleSensor_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Data/DA_VehicleSensor_TNK_04.json) | MVehicleSensorsDataAsset | TNK_04 | 1 |
| [DA_VehicleSensors_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_VehicleSensors_WHL_08.json) | MVehicleSensorsDataAsset | WHL_08 | 1 |
| [DA_Vehicle_BrakingSurface_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_BrakingSurface_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_Skidding_Fast_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_Skidding_Fast_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_Skidding_Medium_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_Skidding_Medium_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_Skidding_Slow_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_Skidding_Slow_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_Surface_Fast_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_Surface_Fast_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_Surface_Medium_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_Surface_Medium_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_Surface_Slow_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_Surface_Slow_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicle_WheelSpinSurface_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/DA/DA_Vehicle_WheelSpinSurface_WHL_08.json) | WDAudioData | WHL_08 | 1 |
| [DA_Vehicles_TNK_04_BrakingSurface](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_BrakingSurface.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_Skidding_Fast](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_Skidding_Fast.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_Skidding_Medium](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_Skidding_Medium.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_Skidding_Slow](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_Skidding_Slow.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_Surface_Fast](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_Surface_Fast.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_Surface_Medium](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_Surface_Medium.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_Surface_Slow](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_Surface_Slow.json) | WDAudioData | TNK_04 | 1 |
| [DA_Vehicles_TNK_04_WheelSpinSurface](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Audio/DA/DA_Vehicles_TNK_04_WheelSpinSurface.json) | WDAudioData | TNK_04 | 1 |
| [DA_WHL_08_Audio](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_WHL_08_Audio.json) | WDAudioData | WHL_08 | 1 |
| [DA_WHL_08_InputControls](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_WHL_08_InputControls.json) | MLandInputControlsDataAsset | WHL_08 | 1 |
| [DA_WHL_08_RingTurretStats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Data/RingTurretDefender/DA_WHL_08_RingTurretStats.json) | WDVehicleStatsDataAsset | WHL_08_RingTurret | 7 |
| [DA_WHL_08_Stats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Data/DA_WHL_08_Stats.json) | WDVehicleStatsDataAsset | WHL_08 | 7 |
| [DT_Buildables_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DT_Buildables_STN_06.json) | DataTable | STN_06 | 1 |
| [DT_Cosmetics_Season02_Skins](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Data/DT_Cosmetics_Season02_Skins.json) | DataTable | — | 1 |
| [DT_EntityData_Ext_VehicleSmoke](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleSmoke/Content/Data/DT_EntityData_Ext_VehicleSmoke.json) | DataTable | VehicleSmoke | 1 |
| [DT_EntityData_UI_TNK04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_EntityData_UI_TNK04.json) | DataTable | TNK_04 | 1 |
| [DT_EntityData_UI_Vehicles_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_EntityData_UI_Vehicles_STN_06.json) | DataTable | STN_06 | 1 |
| [DT_EntityData_UI_Vehicles_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_08.json) | DataTable | WHL_08 | 1 |
| [DT_EntityData_UI_Vehicles_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_08_RingTurret.json) | DataTable | WHL_08_RingTurret | 1 |
| [DT_GlobalDamage_VehicleData_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_GlobalDamage_VehicleData_STN_06.json) | DataTable | STN_06 | 1 |
| [DT_GlobalDamage_VehicleData_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_GlobalDamage_VehicleData_TNK_04.json) | DataTable | TNK_04 | 1 |
| [DT_GlobalDamage_VehicleData_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_08.json) | DataTable | WHL_08 | 1 |
| [DT_GlobalDamage_VehicleData_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_08_RingTurret.json) | DataTable | WHL_08_RingTurret | 1 |
| [DT_RadialWheelSlotType_BuildToolData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DT_RadialWheelSlotType_BuildToolData.json) | DataTable | STN_06 | 1 |
| [DT_VehicleCrosshair_STN06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_VehicleCrosshair_STN06.json) | DataTable | STN_06 | 1 |
| [DT_VehicleCrosshair_TNK04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_VehicleCrosshair_TNK04.json) | DataTable | TNK_04 | 1 |
| [DT_VehicleMarket_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_VehicleMarket_TNK_04.json) | DataTable | TNK_04 | 1 |
| [DT_VehicleMarket_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/DataTables/DT_VehicleMarket_WHL_08.json) | DataTable | WHL_08 | 1 |
| [DT_VehicleMarket_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/DataTables/DT_VehicleMarket_WHL_08_RingTurret.json) | DataTable | WHL_08_RingTurret | 1 |
| [DT_VehicleSeatOverrides_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_VehicleSeatOverrides_STN_06.json) | DataTable | STN_06 | 1 |
| [DT_VendorData_Ext_VehicleSmoke](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleSmoke/Content/Data/DT_VendorData_Ext_VehicleSmoke.json) | DataTable | VehicleSmoke | 1 |
| [IA_Vehicle_FireCountermeasures](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Vehicles/Inputs/IA_Vehicle_FireCountermeasures.json) | BHInputAction | Inputs | 1 |
| [ID_MWSY_001_MountedMachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_001/Content/Weapons/ID_MWSY_001_MountedMachineGun.json) | BHInventoryItemDefinition | — | 2 |
| [ID_MountedMachineGun_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_04/ID_MountedMachineGun_TNK_04.json) | BHInventoryItemDefinition | Weapons | 2 |
| [ID_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Variants/ID_TNK_04.json) | BHInventoryItemDefinition | TNK_04 | 3 |
| [ID_VehicleSmoke](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleSmoke/Content/Data/ID_VehicleSmoke.json) | BHInventoryItemDefinition | VehicleSmoke | 4 |
| [ID_VehicleTurretMachineGun_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_04/ID_VehicleTurretMachineGun_TNK_04.json) | BHInventoryItemDefinition | Weapons | 2 |
| [ID_VehicleTurret_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_04/ID_VehicleTurret_TNK_04.json) | BHInventoryItemDefinition | Weapons | 2 |
| [ID_WHL_08_Default](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Variants/ID_WHL_08_Default.json) | BHInventoryItemDefinition | WHL_08 | 3 |
| [ID_WHL_08_MachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Variants/ID_WHL_08_MachineGun.json) | BHInventoryItemDefinition | WHL_08_RingTurret | 3 |
| [ID_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/WHL_08/ID_WHL_08_RingTurret.json) | BHInventoryItemDefinition | Weapons | 2 |
| [MWSY_001](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_001/Content/MWSY_001.json) | GameFeatureData | — | 2 |
| [MWSY_002](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/VehicleWeaponry/MWSY_002/Content/MWSY_002.json) | GameFeatureData | — | 1 |
| [STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/STN_06.json) | GameFeatureData | STN_06 | 3 |
| [Season02_SkinsData](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Season02_SkinsData.json) | GameFeatureData | — | 2 |
| [Skin_ChocolateChip](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/Skin_ChocolateChip.json) | WDSkinDataAsset | — | 1 |
| [TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/TNK_04.json) | GameFeatureData | TNK_04 | 4 |
| [VP_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Platforms/VP_STN_06.json) | ModularVehiclePlatform | STN_06 | 9 |
| [VP_STN_06_Body](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Parts/VP_STN_06_Body.json) | ModularVehiclePart | STN_06 | 2 |
| [VP_STN_06_Seats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Parts/VP_STN_06_Seats.json) | ModularVehiclePart | STN_06 | 2 |
| [VP_STN_06_Turret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Parts/VP_STN_06_Turret.json) | ModularVehiclePart | STN_06 | 7 |
| [VP_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Platforms/VP_TNK_04.json) | ModularVehiclePlatform | TNK_04 | 11 |
| [VP_TNK_04_MountedMachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Parts/VP_TNK_04_MountedMachineGun.json) | ModularVehiclePart | TNK_04 | 7 |
| [VP_TNK_04_Turret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Parts/VP_TNK_04_Turret.json) | ModularVehiclePart | TNK_04 | 8 |
| [VP_WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Platforms/VP_WHL_08.json) | ModularVehiclePlatform | WHL_08 | 10 |
| [VP_WHL_08_MainBody_Default](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Parts/VP_WHL_08_MainBody_Default.json) | ModularVehiclePart | WHL_08 | 6 |
| [VP_WHL_08_MainBody_MachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Parts/VP_WHL_08_MainBody_MachineGun.json) | ModularVehiclePart | WHL_08_RingTurret | 7 |
| [VP_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Parts/VP_WHL_08_RingTurret.json) | ModularVehiclePart | WHL_08_RingTurret | 5 |
| [VP_WHL_08_Seats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Parts/VP_WHL_08_Seats.json) | ModularVehiclePart | WHL_08 | 2 |
| [VP_WHL_08_Turret_Seats](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Parts/VP_WHL_08_Turret_Seats.json) | ModularVehiclePart | WHL_08_RingTurret | 2 |
| [VP_WHL_08_Wheels](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Parts/VP_WHL_08_Wheels.json) | ModularVehiclePart | WHL_08 | 3 |
| [VV_STN_06](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Variants/VV_STN_06.json) | ModularVehicleVariant | STN_06 | 1 |
| [VV_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Variants/VV_TNK_04.json) | ModularVehicleVariant | TNK_04 | 1 |
| [VV_WHL_08_Default](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Variants/VV_WHL_08_Default.json) | ModularVehicleVariant | WHL_08 | 1 |
| [VV_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Variants/VV_WHL_08_RingTurret.json) | ModularVehicleVariant | WHL_08_RingTurret | 1 |
| [VehicleSmoke](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleSmoke/Content/VehicleSmoke.json) | GameFeatureData | VehicleSmoke | 3 |
| [Vehicle_WHL_08_REV](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/Audio/Vehicle_WHL_08_REV.json) | REVModelAsset | WHL_08 | 1 |
| [WE_STN_06_MountedMachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Weapons/WeaponExtensions/WE_STN_06_MountedMachineGun.json) | WDVehicleWeaponExtensionDataAsset | STN_06 | 1 |
| [WE_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/WeaponExtensions/WE_TNK_04.json) | WDVehicleWeaponExtensionDataAsset | TNK_04 | 1 |
| [WE_TNK_04_MachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/WeaponExtensions/MachineGun/WE_TNK_04_MachineGun.json) | WDVehicleWeaponExtensionDataAsset | TNK_04 | 1 |
| [WE_TNK_04_MountedMachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/WeaponExtensions/MountedMachineGun/WE_TNK_04_MountedMachineGun.json) | WDVehicleWeaponExtensionDataAsset | TNK_04 | 1 |
| [WE_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Weapons/WeaponExtensions/WE_WHL_08_RingTurret.json) | WDVehicleWeaponExtensionDataAsset | WHL_08_RingTurret | 1 |
| [WHL_08](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/WHL_08.json) | GameFeatureData | WHL_08 | 4 |
| [WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/WHL_08_RingTurret.json) | GameFeatureData | WHL_08_RingTurret | 2 |
| [W_STN_06_MountedMachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Weapons/W_STN_06_MountedMachineGun.json) | WDVehicleWeaponDataAsset | STN_06 | 1 |
| [W_TNK_04](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/W_TNK_04.json) | WDVehicleWeaponDataAsset | TNK_04 | 1 |
| [W_TNK_04_MountedMachineGun](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/Weapons/W_TNK_04_MountedMachineGun.json) | WDVehicleWeaponDataAsset | TNK_04 | 1 |
| [W_WHL_08_RingTurret](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/Weapons/WeaponExtensions/W_WHL_08_RingTurret.json) | WDVehicleWeaponDataAsset | WHL_08_RingTurret | 1 |

## Removed in Season 2

| Asset | Type | Path |
|---|---|---|
| IA_Vehicle_FireFlares | BHInputAction | Wardogs/Content/Vehicles/Inputs/IA_Vehicle_FireFlares.json |

Removed assets are not on GitHub, so there are no links.

## Moved

None.

## See also

- [Vehicle stats and damage tables]({{ '/content/Wardogs_AllVehicles_Stats_Damage_v1.html' | relative_url }}#season-02-update), Season 02 update
- [Vehicles]({{ '/content/Wardogs_Vehicles_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Vehicles game feature]({{ '/game-features/Wardogs_GameFeatures_Vehicles_v2.html' | relative_url }}#season-02-update), Season 02 update
- [Vehiclesmith game feature]({{ '/game-features/Wardogs_GameFeatures_Vehiclesmith_v2.html' | relative_url }}#season-02-update), Season 02 update

Full change browser for this area: {{ '/season-2-changes/all-changes.html' | relative_url }}#area=vehicles&q=

