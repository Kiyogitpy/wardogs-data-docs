---
title: "Data Tables: Combat, Vehicles and Scene Data"
redirect_from: ["/Wardogs_DataTables_Combat_v1.html", "/Wardogs_DataTables_Combat_v1"]
parent: "Data Tables"
grand_parent: "Data Tables & Tags"
description: "Combat, vehicle and scene tables: damage reduction, seat modifiers, deathmatch scenes and more"
---

# Data Tables: Combat, Vehicles and Scene Data
*Generic expansion of the data tables below, built by [`_tools/datatable_catalog.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/datatable_catalog.py) (`--write` is idempotent). Back to the [catalog index](Wardogs_DataTables_v1.md).*

> Columns are the flattened row fields: nested structs are dotted keys, gameplay tags show the tag name, object references show the asset name, arrays are joined with commas. Columns empty in every row are dropped. Long cells are cut with an ellipsis; open the table JSON for the full value.

## WDVehicleSeatDamageReductionData

Tables: [`DT_InfantryData_VehicleSeatDamageReduction`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDVehicleSeatDamageReductionData -->
*1 table(s), 11 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `_aaabcpelbmpimhadngldm` | `Tag` |
|---|---|---|
| `Vehicle.Variant.Air.Rotary.ROT_01.Default` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.ROT_01.Default |
| `Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.ROT_01.MountedMachineGuns |
| `Vehicle.Variant.Air.Rotary.Havoc.Default` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.Havoc.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.Default` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.Littlebird.Default |
| `Vehicle.Variant.Air.Rotary.Littlebird.RocketPods` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |
| `Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.Littlebird.MountedMachineGuns |
| `Vehicle.Variant.Land.Wheeled.Humvee.Default` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Land.Wheeled.Humvee.Default |
| `Vehicle.Variant.Land.Wheeled.Humvee.MachineGun` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Land.Wheeled.Humvee.MachineGun |
| `Vehicle.Variant.Land.Wheeled.Humvee.Minigun` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Land.Wheeled.Humvee.Minigun |
| `Vehicle.Variant.Air.Rotary.ROT_04.Default` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| `Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns` | {DamageSources=Meta.Damage.Arms.Small, Meta.Damage.Arms.Medium; VehicleSeats={Key=State.Player.Vehicle.SeatDa… | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
<!-- /datatable_catalog -->

## FVehiclePropEntry

Tables: [`DT_VehiclePropList`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Blueprints/VehiclePropTooling/DT_VehiclePropList.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct FVehiclePropEntry -->
*1 table(s), 29 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Enum_6_6B2D6CBF43B68DD624E114A3BE847D53` | `DataAsset_8_B5411959416D66C7F66AF08E024E7911` |
|---|---|---|
| `Civilian_Car_01a` | NewEnumerator4 | DA_VehicleProp_CivillianCar_01a |
| `Civilian_Car_02a` | NewEnumerator24 | DA_VehicleProp_CivillianCar_02a |
| `Sedan_01a` | NewEnumerator1 | DA_VehicleProp_Sedan |
| `Sedan_01b_Taxi` | NewEnumerator8 | DA_VehicleProp_TaxiSedan |
| `Sedan_01c_PoliceCar` | NewEnumerator0 | DA_VehicleProp_PoliceSedan |
| `Destroyed_Cars_01a` | NewEnumerator15 | DA_VehicleProp_Destroyed_Car_01a |
| `Truck_01a` | NewEnumerator2 | DA_VehicleProp_Truck |
| `Truck_01b_FireTruck` | NewEnumerator9 | DA_VehicleProp_FireTruck |
| `Truck_01c_GasRepair` | NewEnumerator25 | DA_VehicleProp_GasRepair |
| `Truck_01d_Garbage` | NewEnumerator26 | DA_VehicleProp_Truck_01d_Garbage |
| `Pickup_Truck_02a` | NewEnumerator23 | DA_VehicleProp_Pickup_Truck_02 |
| `Van_02a` | NewEnumerator3 | DA_VehicleProp_Van |
| `Bus_01a` | NewEnumerator5 | DA_VehicleProp_Bus |
| `Lorry_Standard` | NewEnumerator10 | DA_VehicleProp_Lorry_Standard_01a |
| `Lorry_40ft` | NewEnumerator11 | DA_VehicleProp_Lorry_40ft_01a |
| `Lorry_Trailer_40ft` | NewEnumerator12 | DA_VehicleProp_Lorry_40ft_Trailer_01a |
| `Exclavator_Wheels` | NewEnumerator13 | DA_VehicleProp_Exclavator_Wheels_01a |
| `Exclavator_Tracks` | NewEnumerator14 | DA_VehicleProp_Exclavator_Tracks_01a |
| `Bulldozer_01` | NewEnumerator18 | DA_VehicleProp_Bulldozer_01a |
| `Mini_Digger_01a` | NewEnumerator20 | DA_Mini_Digger_01a |
| `Abandoned_Tractor_01a` | NewEnumerator21 | DA_Abandoned_Tractor_01a |
| `Locomotive_01a` | NewEnumerator22 | DA_Locomotive_01a |
| `Truck_MobileCrane_01a` | NewEnumerator27 | DA_VehicleProp_Truck_MobileCrane_01a |
| `Faction_Generator_01` | NewEnumerator28 | DA_VehicleProp_Faction_Generator_01 |
| `Faction_Generator_02` | NewEnumerator29 | DA_VehicleProp_Faction_Generator_02 |
| `Faction_Generator_03` | NewEnumerator30 | DA_VehicleProp_Faction_Generator_03 |
| `Faction_Generator_02b` | NewEnumerator31 | DA_VehicleProp_Faction_Generator_02b |
| `Military_FuelTruck_01a` | NewEnumerator32 | DA_VehicleProp_Military_FuelTruck_01a |
| `SolarPanelUnit_01a` | NewEnumerator33 | DA_SolarPanelUnit_01a |
<!-- /datatable_catalog -->

## WDAmmoModifierTableRow

Tables: [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDAmmoModifierTableRow -->
*1 table(s), 5 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `AmmoModifierDataAsset` | `Tag` |
|---|---|---|
| `Meta.Damage.AmmoModifier.HollowPoint` | DA_AmmoModifier_HollowPoint | Meta.Damage.AmmoModifier.HollowPoint |
| `Meta.Damage.AmmoModifier.ArmorPiercing` | DA_AmmoModifier_ArmorPiercing | Meta.Damage.AmmoModifier.ArmorPiercing |
| `Meta.Damage.AmmoModifier.Tracer` | DA_AmmoModifier_Tracer | Meta.Damage.AmmoModifier.Tracer |
| `Meta.Damage.AmmoModifier.HollowPoint.Tracer` | DA_AmmoModifier_HollowPoint_Tracer | Meta.Damage.AmmoModifier.HollowPoint.Tracer |
| `Meta.Damage.AmmoModifier.ArmorPiercing.Tracer` | DA_AmmoModifier_ArmorPiercing_Tracer | Meta.Damage.AmmoModifier.ArmorPiercing.Tracer |
<!-- /datatable_catalog -->

## WDDeathmatchWeaponData

Tables: [`DT_DeathmatchWeaponSelect`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DT_DeathmatchWeaponSelect.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDDeathmatchWeaponData -->
*1 table(s), 20 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `DeathmatchWeaponVariations` | `Tag` |
|---|---|---|
| `Id.Item.AK74M` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.AK74M |
| `Id.Item.M4` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.M4 |
| `Id.Item.SKS` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.SKS |
| `Id.Item.KH2002` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.KH2002 |
| `Id.Item.A91` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.A91 |
| `Id.Item.Glock17` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.Glock17 |
| `Id.Item.M12G` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.M12G |
| `Id.Item.MP9` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.MP9 |
| `Id.Item.SV98` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.SV98 |
| `Id.Item.SMG_03` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.SMG_03 |
| `Id.Item.Judge` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.Judge |
| `Id.Item.LMG_02` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.LMG_02 |
| `Id.Item.M249` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.M249 |
| `Id.Item.MK22` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.MK22 |
| `Id.Item.MMGL` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.MMGL |
| `Id.Item.RFB` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.RFB |
| `Id.Item.SR_04` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.SR_04 |
| `Id.Item.SVDM` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.SVDM |
| `Id.Item.TAR21` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.TAR21 |
| `Id.Item.Vector` | {bOverwriteDescription=false; bOverwriteIcon=false} | Id.Item.Vector |
<!-- /datatable_catalog -->

## WDSceneDataTableRow

Tables: [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json), [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json), [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json), [`DT_SceneData_Frontend_Gunsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith.json), [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json), [`DT_SceneData_Frontend_Vehiclesmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_SceneData_Frontend_Vehiclesmith.json), [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json), [`DT_SceneData_Match_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/FobRefuelRepair/DT_SceneData_Match_Buildables.json), [`DT_SceneData_Match_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/UI/DT_SceneData_Match_STN_05.json), [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json), [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json), [`DT_SceneData_Match_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/UI/Data/DT_SceneData_Match_SupplyCrates.json) (+2 more). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDSceneDataTableRow -->
*14 table(s), 68 rows, 22 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 22:

| Table | Row | `InputMode` | `bResetFocusOnEnter` | `bShouldBlockBack` | `bIsFocusable` | `bShouldPreload` | `Group` | `SceneRules` |
|---|---|---|---|---|---|---|---|---|
| [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) | `UI.Scene.Deathmatch.WeaponSelect` | UI | true | false | true | false |  |  |
| [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) | `UI.Scene.Match.Scenario.Results` | UI | true | true | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Logo` | UI | true | true | true | true |  | {FallbackSceneTag=UI.Scene.Frontend.Photosensitivity} |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Photosensitivity` | UI | true | true | true | true |  | {FallbackSceneTag=UI.Scene.Frontend.Start} |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Start` | UI | true | true | true | true |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.InitialSettings` | UI | true | true | true | false |  | {FallbackSceneTag=UI.Scene.Frontend.Home} |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Home` | UI | true | false | true | true | UI.SceneGroup.Frontend.TopBar |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Career` | UI | true | false | true | false | UI.SceneGroup.Frontend.TopBar |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Customize` | UI | true | false | true | false | UI.SceneGroup.Frontend.TopBar |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Collection` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.GoldMarket` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Orientation` | UI | true | true | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.FindMatch` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DevMenu` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket` | UI | true | false | true | false | UI.SceneGroup.Frontend.TopBar |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Missions` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Unlocks` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Investments` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Customize` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Vault` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Platforms` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.PlatformProgress` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Roles` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.RoleSkillTree` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.LearnToPlay` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Tutorials` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.ContextDrawer` | UI | true | false | true | true |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Mailbox` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DeploymentSelect` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend_Gunsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith.json) | `UI.Scene.Frontend.Gunsmith` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json) | `UI.Scene.Itemsmith.TestingGround.Pause` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Frontend_Vehiclesmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_SceneData_Frontend_Vehiclesmith.json) | `UI.Scene.Frontend.Vehiclesmith` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Map` | GameAndUI | true | false | true | true |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Inventory` | UI | true | false | true | true | UI.SceneGroup.Session | {_aaabogpkidlhgbejcobka=OnlyShowWhenGameIsNotOver} |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Scoreboard` | UI | true | false | true | false | UI.SceneGroup.Session |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.FactionSelect` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver` | UI | true | false | true | false | UI.SceneGroup.GameOver |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.XPProgression` | UI | true | false | true | false | UI.SceneGroup.GameOver |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock.Garage` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Vehicles` | UI | true | false | true | true |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Garage` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeploymentBoard` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.WaitingToDeploy` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Looting` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.EndgameMovie` | UI | true | true | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.PingWheel` | GameAndUI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.RadialWheel` | GameAndUI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Missile` | Game | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Weapon` | Game | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.Internal.AdminPanel` | Game | false | false | false | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeathRecap` | GameAndUI | true | false | true | true |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.AdminPanel` | GameAndUI | true | false | true | false |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.ContextDrawer` | UI | true | false | true | true |  |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Frontend.Progression` | UI | true | false | true | false | UI.SceneGroup.Session |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.Scoreboard` | UI | true | false | true | false | UI.SceneGroup.GameOver |  |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Wagers` | UI | true | false | true | true |  |  |
| [`DT_SceneData_Match_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/FobRefuelRepair/DT_SceneData_Match_Buildables.json) | `UI.Scene.Match.FobRefuelRepair` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/UI/DT_SceneData_Match_STN_05.json) | `UI.Scene.Match.DroneReload` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | `UI.Scene.Match.ContextDrawer` | UI | true | false | true | true |  |  |
| [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) | `UI.Scene.Match.EndgameMovie` | UI | true | true | true | false |  |  |
| [`DT_SceneData_Match_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/UI/Data/DT_SceneData_Match_SupplyCrates.json) | `UI.Scene.Match.VehicleSupplyCrate` | UI | true | false | true | true |  |  |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | `UI.Scene.Match.WagerStatus` | UI | true | false | true | false | UI.SceneGroup.Session | {_aaabogpkidlhgbejcobka=OnlyShowWhenGameIsNotOver} |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Popups` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Settings` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Frontend.Loadouts` | UI | true | false | true | false |  |  |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Match.Vendor.Equipment` | UI | true | false | true | true |  |  |

Columns 8-14 of 22:

| Table | Row | `OpenSceneActions` | `CloseSceneActions` | `Params.Layer` | `Params.ZOrder` | `Params.WidgetClass` | `Params.ViewModelParams.ViewModelClass` | `Params.ViewModelParams.Data` |
|---|---|---|---|---|---|---|---|---|
| [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) | `UI.Scene.Deathmatch.WeaponSelect` |  |  | Normal | 0 | W_DeathmatchWeaponSelectScene.W_DeathmatchWeaponSelectScene_C | DeathmatchRuntime.WDUIDeathmatchWeaponSelectViewModel | DA_WeaponSelectData |
| [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) | `UI.Scene.Match.Scenario.Results` |  |  | Normal | 0 | W_ScenarioResultsScene.W_ScenarioResultsScene_C | BaseScenarioRuntime.WDUIScenarioResultsSceneViewModel | DA_DefaultScenarioResultsSceneData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Logo` |  |  | Upper | 0 | W_LogoScene.W_LogoScene_C | WDGame.WDUILogoMovieViewModel | DA_LogoScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Photosensitivity` |  |  | Upper | 0 | W_PhotosensitivityScene.W_PhotosensitivityScene_C | WDGame.WDUIPhotosensitivityViewModel | DA_PhotosensitivityScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Start` |  |  | Upper | 1 | W_StartScene.W_StartScene_C | WDGame.WDUIStartViewModel | DA_StartScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.InitialSettings` | {WidgetClass=W_AccountBar_C} | {WidgetClass=W_AccountBar_C} | Normal | 0 | W_InitialSettingsScene.W_InitialSettingsScene_C | WDGame.WDUIInitialSettingsViewModel | DA_InitialSettingsScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Home` |  |  | Normal | 0 | W_HomeScene.W_HomeScene_C | WDGame.WDUIHomeViewModel | DA_HomeScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Career` |  |  | Normal | 0 | W_Progression_Scene.W_Progression_Scene_C | WDGame.WDUIProgressionSceneViewModel | DA_Progression_Scene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Customize` |  |  | Normal | 0 | W_CustomiseScene.W_CustomiseScene_C | WDGame.WDUISceneViewModel | DA_CustomizeScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Collection` |  |  | Normal | 0 | W_CollectionScene.W_CollectionScene_C | WDGame.WDUICollectionViewModel | DA_CollectionScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.GoldMarket` |  |  | Normal | 0 | W_GoldMarketScene.W_GoldMarketScene_C | WDGame.WDUIGoldMarketViewModel | DA_GoldMarketScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Orientation` |  |  | Normal | 0 | W_OrientationScene.W_OrientationScene_C | WDGame.WDUIOrientationViewModel | DA_OrientationScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.FindMatch` |  |  | Normal | 0 | W_FindMatchScene.W_FindMatchScene_C | WDGame.WDUIFindMatchViewModel | DA_FindMatchScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DevMenu` |  |  | Normal | 0 | W_DevMenuScene.W_DevMenuScene_C | WDGame.WDUIDevMenuViewModel | DA_DevMenuScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog` |  |  | Normal | 0 | W_WardogScene.W_WardogScene_C | WDGame.WDUIWardogViewModel | DA_WardogScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket` |  |  | Normal | 0 | W_BlackMarketScene.W_BlackMarketScene_C | WDGame.WDUIBlackMarketViewModel | DA_BlackMarketScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Missions` |  |  | Normal | 0 | W_MissionsScene.W_MissionsScene_C | WDGame.WDUISceneViewModel | DA_MissionsScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Unlocks` |  |  | Normal | 0 | W_UnlocksScene.W_UnlocksScene_C | WDGame.WDUIUnlocksSceneViewModel | DA_UnlocksScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Investments` |  |  | Normal | 0 | W_InvestmentsScene.W_InvestmentsScene_C | WDGame.WDUIInvestmentsViewModel | DA_InvestmentsScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Customize` |  |  | Normal | 0 | W_CustomizeScene.W_CustomizeScene_C | WDGame.WDUICustomizeViewModel | DA_CustomizeScene |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Vault` |  |  | Normal | 0 | W_VaultScene.W_VaultScene_C | WDGame.WDUIVaultViewModel | DA_VaultSceneData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Platforms` |  |  | Normal | 0 | W_PlatformMastery_Scene.W_PlatformMastery_Scene_C | WDGame.WDUIPlatformMasterySceneViewModel | DA_UI_PlatformMastery_SceneData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.PlatformProgress` |  |  | Normal | 0 | W_PlatformMastery_ProgressScene.W_PlatformMastery_ProgressScene_C | WDGame.WDUIPlatformMasteryProgressSceneViewModel | DA_UI_PlatformMastery_ProgressSceneData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Roles` |  |  | Normal | 0 | W_RoleMastery_Scene.W_RoleMastery_Scene_C | WDGame.WDUISceneViewModel | DA_UI_RoleMastery_SceneData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.RoleSkillTree` |  |  | Normal | 0 | W_RoleSkillTree_Scene.W_RoleSkillTree_Scene_C | WDGame.WDUIRoleSkillTreeSceneViewModel | DA_UI_RoleSkillTree_SceneData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.LearnToPlay` |  |  | Normal | 0 | W_LearnToPlayScene.W_LearnToPlayScene_C | WDGame.WDUILearnToPlayViewModel | DA_LearnToPlay |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Tutorials` |  |  | Normal | 0 | W_TutorialsScene.W_TutorialsScene_C | WDGame.WDUITutorialsViewModel | DA_TutorialsContent |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.ContextDrawer` |  |  | Upper | 3 | W_ContextDrawer.W_ContextDrawer_C | WDGame.WDUIContextDrawerViewModel | DA_Frontend_ContextDrawer |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Mailbox` |  |  | Normal | 0 | W_MailboxScene.W_MailboxScene_C | WDGame.WDUISceneViewModel | DA_MailboxData |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DeploymentSelect` |  |  | Normal | 0 | W_DeploymentSelectScene.W_DeploymentSelectScene_C | WDGame.WDUIDeploymentSelectViewModel | DA_DeploymentSelectScene |
| [`DT_SceneData_Frontend_Gunsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith.json) | `UI.Scene.Frontend.Gunsmith` |  |  | Normal | 1 | W_GunsmithScene.W_GunsmithScene_C | GunsmithRuntime.WDUIGunsmithSceneViewModel | DA_GunsmithScene |
| [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json) | `UI.Scene.Itemsmith.TestingGround.Pause` |  |  | Normal | 1 | W_TestingGroundPauseScene.W_TestingGroundPauseScene_C | ItemsmithRuntime.WDUIItemsmithTestingGroundPauseViewModel | DA_TestingGroundSceneData |
| [`DT_SceneData_Frontend_Vehiclesmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_SceneData_Frontend_Vehiclesmith.json) | `UI.Scene.Frontend.Vehiclesmith` |  |  | Normal | 1 | W_VehiclesmithScene.W_VehiclesmithScene_C | VehiclesmithRuntime.WDUIVehiclesmithSceneViewModel | DA_Vehiclesmith_Scene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Map` |  |  | Normal | 0 | W_MapScene.W_MapScene_C | WDGame.WDUIMapViewModel | DA_MapScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Inventory` | {WidgetClass=W_Chatbox_C}, {_aaaapgcbaljpbdjjghoii=Audio.Event.UI.Inventory.SceneEnter} | {WidgetClass=W_Chatbox_C} | Normal | 1 | W_InventoryScene_2_0.W_InventoryScene_2_0_C | WDGame.WDUIInventoryViewModel | DA_InventoryScene_2_0 |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Scoreboard` | {WidgetClass=W_Chatbox_C}, {_aaaapgcbaljpbdjjghoii=Audio.Event.UI.Scoreboard.Enter} | {WidgetClass=W_Chatbox_C} | Normal | 1 | W_ScoreboardScene.W_ScoreboardScene_C | WDGame.WDUIScoreboardSceneViewModel | DA_ScoreboardScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.FactionSelect` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Upper | 0 | W_FactionSelectScene.W_FactionSelectScene_C | WDGame.WDUIFactionSelectViewModel | DA_FactionSelectScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver` | {bEnableNavigationRibbon=true} |  | Normal | 0 | W_GameOverScene.W_GameOverScene_C | WDGame.WDUIGameOverViewModel | DA_GameOverScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.XPProgression` |  |  | Normal | 0 | W_XPProgressionScene.W_XPProgressionScene_C | WDGame.WDUIXPProgressionViewModel | DA_XPProgressionScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock` |  |  | Normal | 0 | W_QuickRestockScene.W_QuickRestockScene_C | WDGame.WDUIQuickRestockViewModel | DA_QuickRestockScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock.Garage` |  |  | Normal | 0 | W_QuickRestockScene.W_QuickRestockScene_C | WDGame.WDUIGarageQuickRestockViewModel | DA_GarageQuickRestockScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Vehicles` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 0 | W_VehicleVendorScene_Rework.W_VehicleVendorScene_Rework_C | WDGame.WDUIVehicleVendorViewModel | DA_VehicleVendor |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Garage` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 0 | W_VendorScene_Garage_Rework.W_VendorScene_Garage_Rework_C | WDGame.WDUIGarageVendorViewModel_Rework | DA_GarageVendorRework |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeploymentBoard` |  |  | Normal | 0 | W_DeploymentBoardScene.W_DeploymentBoardScene_C | WDGame.WDUIDeploymentBoardViewModel | DA_DeploymentBoardScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.WaitingToDeploy` | {WidgetClass=W_AccountBar_C} | {WidgetClass=W_AccountBar_C} | Normal | 0 | W_WaitingToDeployScene.W_WaitingToDeployScene_C | WDGame.WDUIWaitingToDeployViewModel | DA_WaitingToDeployScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Looting` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 0 | W_LootingScene_2_0.W_LootingScene_2_0_C | WDGame.WDUILootingViewModel | DA_LootingScene_2_0 |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.EndgameMovie` | {bEnableNavigationRibbon=false} |  | Normal | 0 | W_EndgameMovieScene.W_EndgameMovieScene_C | WDGame.WDUIEndgameMovieViewModel | DA_EndgameMovie |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.PingWheel` |  |  | Normal | 0 | W_PingWheelScene.W_PingWheelScene_C | WDGame.WDUIPingWheelViewModel | DA_PingWheelScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.RadialWheel` |  |  | Normal | 0 | W_RadialWheelScene.W_RadialWheelScene_C | WDGame.WDUIRadialWheelSceneViewModel | DA_RadialWheelScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Missile` |  |  | Normal | 0 | W_TVGuidedScene_Missile.W_TVGuidedScene_Missile_C | WDGame.WDUITVGuidedMissileViewModel | DA_TVGuidedScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Weapon` |  |  | Normal | 0 | W_TVGuidedScene_Weapon.W_TVGuidedScene_Weapon_C | WDGame.WDUITVGuidedWeaponViewModel | DA_TVGuidedScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.Internal.AdminPanel` |  |  | Normal | 0 | W_WardogsInteractionAdminScene.W_WardogsInteractionAdminScene_C | WDGame.WDUIVehicleInteractionAdminViewModel | DA_VehicleInteractionAdminData |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeathRecap` |  |  | Normal | 0 | W_DeathRecapScene.W_DeathRecapScene_C | WDGame.WDUIDeathRecapViewModel | DA_DeathRecapScene |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.AdminPanel` |  |  | Normal | 0 | W_AdminPanelScene.W_AdminPanelScene_C | WDGame.WDUIAdminPanelSceneViewModel | DA_AdminPanel |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.ContextDrawer` |  |  | Upper | 3 | W_ContextDrawer.W_ContextDrawer_C | WDGame.WDUIContextDrawerViewModel | DA_Match_ContextDrawer |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Frontend.Progression` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 0 | W_Progression_Scene.W_Progression_Scene_C | WDGame.WDUIProgressionSceneViewModel | DA_Progression_Scene_Match |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.Scoreboard` |  |  | Normal | 0 | W_ScoreboardScene.W_ScoreboardScene_C | WDGame.WDUIScoreboardSceneViewModel | DA_ScoreboardScene_GameOver |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Wagers` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 0 | W_WagerVendorScene.W_WagerVendorScene_C | WDGame.WDUIWagerVendorViewModel | DA_WagerVendor |
| [`DT_SceneData_Match_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/FobRefuelRepair/DT_SceneData_Match_Buildables.json) | `UI.Scene.Match.FobRefuelRepair` |  |  | Normal | 0 | W_FobRefuelAndRepair.W_FobRefuelAndRepair_C | BuildablesRuntime.WDUIFobRefuelRepairViewModel | DA_Scene_FobRefuelRepair |
| [`DT_SceneData_Match_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/UI/DT_SceneData_Match_STN_05.json) | `UI.Scene.Match.DroneReload` |  |  | Normal | 0 | W_DroneReloadScene.W_DroneReloadScene_C | BuildablesRuntime.WDUIDroneReloadSceneViewModel | DA_Scene_DroneReload |
| [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | `UI.Scene.Match.ContextDrawer` |  |  | Upper | 3 | W_ContextDrawer.W_ContextDrawer_C | WDGame.WDUIContextDrawerViewModel | DA_ShootingRange_ContextDrawer |
| [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) | `UI.Scene.Match.EndgameMovie` | {bEnableNavigationRibbon=false} |  | Normal | 0 | W_SniperShowdown_GameOverScene.W_SniperShowdown_GameOverScene_C | SniperShowdownRuntime.WDSniperShowdownGameOverSceneViewModel | DA_SniperShowdown_GameOverScene |
| [`DT_SceneData_Match_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/UI/Data/DT_SceneData_Match_SupplyCrates.json) | `UI.Scene.Match.VehicleSupplyCrate` |  |  | Normal | 0 | W_SupplyCrateScene_2_0.W_SupplyCrateScene_2_0_C | WDGame.WDUIVehicleSupplyCrateViewModel | DA_SupplyCrateScene |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | `UI.Scene.Match.WagerStatus` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 1 | W_WagerStatusScene.W_WagerStatusScene_C | WDGame.WDUIWagerStatusSceneViewModel | DA_WagerStatusScene |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Popups` |  |  | Popup | 0 | W_PopupsScene.W_PopupsScene_C | WDGame.WDUIPopupsViewModel | DA_PopupsScene |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Settings` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 1 | W_SettingsScene.W_SettingsScene_C | WDGame.WDUISettingsViewModel | DA_SettingsScene |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Frontend.Loadouts` |  |  | Normal | 0 | W_LoadoutsScene.W_LoadoutsScene_C | WDGame.WDUILoadoutsViewModel | DA_LoadoutsScene |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Match.Vendor.Equipment` | {WidgetClass=W_Chatbox_C} | {WidgetClass=W_Chatbox_C} | Normal | 0 | W_VendorScene_New.W_VendorScene_New_C | WDGame.WDUIVendorViewModel_Rework | DA_VendorScene_New |

Columns 15-21 of 22:

| Table | Row | `Params._aaabkejhohfkdpglkgkep` | `bBlockTopBarUpdates` | `bShowSceneTitle` | `bShowBackButton` | `bShowSeasonalCountdown` | `bOpenOnTop` | `_aaabfeppjajiiglgbhgoo` |
|---|---|---|---|---|---|---|---|---|
| [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) | `UI.Scene.Deathmatch.WeaponSelect` | false | false | false | false | false | false | false |
| [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) | `UI.Scene.Match.Scenario.Results` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Logo` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Photosensitivity` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Start` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.InitialSettings` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Home` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Career` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Customize` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Collection` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.GoldMarket` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Orientation` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.FindMatch` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DevMenu` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket` | false | false | false | false | true | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Missions` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Unlocks` | false | false | false | true | true | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Investments` | false | false | false | true | true | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Customize` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Vault` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Platforms` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.PlatformProgress` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Roles` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.RoleSkillTree` | false | false | false | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.LearnToPlay` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Tutorials` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.ContextDrawer` | false | true | false | false | false | true | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Mailbox` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DeploymentSelect` | false | false | true | true | false | false | false |
| [`DT_SceneData_Frontend_Gunsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith.json) | `UI.Scene.Frontend.Gunsmith` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json) | `UI.Scene.Itemsmith.TestingGround.Pause` | false | false | false | false | false | false | false |
| [`DT_SceneData_Frontend_Vehiclesmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_SceneData_Frontend_Vehiclesmith.json) | `UI.Scene.Frontend.Vehiclesmith` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Map` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Inventory` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Scoreboard` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.FactionSelect` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.XPProgression` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock.Garage` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Vehicles` | false | false | true | true | false | false | true |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Garage` | false | false | true | true | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeploymentBoard` | false | false | false | false | false | false | true |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.WaitingToDeploy` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Looting` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.EndgameMovie` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.PingWheel` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.RadialWheel` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Missile` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Weapon` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.Internal.AdminPanel` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeathRecap` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.AdminPanel` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.ContextDrawer` | false | false | false | false | false | true | true |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Frontend.Progression` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.Scoreboard` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Wagers` | false | false | true | true | false | false | true |
| [`DT_SceneData_Match_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/FobRefuelRepair/DT_SceneData_Match_Buildables.json) | `UI.Scene.Match.FobRefuelRepair` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/UI/DT_SceneData_Match_STN_05.json) | `UI.Scene.Match.DroneReload` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | `UI.Scene.Match.ContextDrawer` | false | false | false | false | false | true | true |
| [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) | `UI.Scene.Match.EndgameMovie` | false | false | false | false | false | false | false |
| [`DT_SceneData_Match_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/UI/Data/DT_SceneData_Match_SupplyCrates.json) | `UI.Scene.Match.VehicleSupplyCrate` | false | false | true | true | false | false | false |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | `UI.Scene.Match.WagerStatus` | false | false | false | false | false | false | false |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Popups` | false | true | false | false | false | false | false |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Settings` | false | false | true | true | false | false | false |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Frontend.Loadouts` | false | false | false | true | false | false | false |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Match.Vendor.Equipment` | false | false | true | true | false | false | true |

Columns 22-22 of 22:

| Table | Row | `Tag` |
|---|---|---|
| [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) | `UI.Scene.Deathmatch.WeaponSelect` | UI.Scene.Deathmatch.WeaponSelect |
| [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) | `UI.Scene.Match.Scenario.Results` | UI.Scene.Match.Scenario.Results |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Logo` | UI.Scene.Frontend.Logo |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Photosensitivity` | UI.Scene.Frontend.Photosensitivity |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Start` | UI.Scene.Frontend.Start |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.InitialSettings` | UI.Scene.Frontend.InitialSettings |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Home` | UI.Scene.Frontend.Home |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Career` | UI.Scene.Frontend.Career |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Customize` | UI.Scene.Frontend.Customize |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Collection` | UI.Scene.Frontend.Collection |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.GoldMarket` | UI.Scene.Frontend.GoldMarket |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Orientation` | UI.Scene.Frontend.Orientation |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.FindMatch` | UI.Scene.Frontend.FindMatch |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DevMenu` | UI.Scene.Frontend.DevMenu |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog` | UI.Scene.Frontend.Wardog |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket` | UI.Scene.Frontend.Blackmarket |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Missions` | UI.Scene.Frontend.Blackmarket.Missions |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Unlocks` | UI.Scene.Frontend.Blackmarket.Unlocks |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Blackmarket.Investments` | UI.Scene.Frontend.Blackmarket.Investments |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Customize` | UI.Scene.Frontend.Wardog.Customize |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Vault` | UI.Scene.Frontend.Vault |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Platforms` | UI.Scene.Frontend.Wardog.Mastery.Platforms |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.PlatformProgress` | UI.Scene.Frontend.Wardog.Mastery.PlatformProgress |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.Roles` | UI.Scene.Frontend.Wardog.Mastery.Roles |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Wardog.Mastery.RoleSkillTree` | UI.Scene.Frontend.Wardog.Mastery.RoleSkillTree |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.LearnToPlay` | UI.Scene.Frontend.LearnToPlay |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Tutorials` | UI.Scene.Frontend.Tutorials |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.ContextDrawer` | UI.Scene.Frontend.ContextDrawer |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.Mailbox` | UI.Scene.Frontend.Mailbox |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | `UI.Scene.Frontend.DeploymentSelect` | UI.Scene.Frontend.DeploymentSelect |
| [`DT_SceneData_Frontend_Gunsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith.json) | `UI.Scene.Frontend.Gunsmith` | UI.Scene.Frontend.Gunsmith |
| [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json) | `UI.Scene.Itemsmith.TestingGround.Pause` | UI.Scene.Itemsmith.TestingGround.Pause |
| [`DT_SceneData_Frontend_Vehiclesmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_SceneData_Frontend_Vehiclesmith.json) | `UI.Scene.Frontend.Vehiclesmith` | UI.Scene.Frontend.Vehiclesmith |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Map` | UI.Scene.Match.Map |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Inventory` | UI.Scene.Match.Inventory |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Scoreboard` | UI.Scene.Match.Scoreboard |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.FactionSelect` | UI.Scene.Match.FactionSelect |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver` | UI.Scene.Match.GameOver |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.XPProgression` | UI.Scene.Match.GameOver.XPProgression |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock` | UI.Scene.Match.QuickRestock |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.QuickRestock.Garage` | UI.Scene.Match.QuickRestock.Garage |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Vehicles` | UI.Scene.Match.Vendor.Vehicles |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Garage` | UI.Scene.Match.Vendor.Garage |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeploymentBoard` | UI.Scene.Match.DeploymentBoard |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.WaitingToDeploy` | UI.Scene.Match.WaitingToDeploy |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Looting` | UI.Scene.Match.Looting |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.EndgameMovie` | UI.Scene.Match.EndgameMovie |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.PingWheel` | UI.Scene.Match.PingWheel |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.RadialWheel` | UI.Scene.Match.RadialWheel |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Missile` | UI.Scene.Match.Vehicle.TVGuided.Missile |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.TVGuided.Weapon` | UI.Scene.Match.Vehicle.TVGuided.Weapon |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vehicle.Internal.AdminPanel` | UI.Scene.Match.Vehicle.Internal.AdminPanel |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.DeathRecap` | UI.Scene.Match.DeathRecap |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.AdminPanel` | UI.Scene.Match.AdminPanel |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.ContextDrawer` | UI.Scene.Match.ContextDrawer |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Frontend.Progression` | UI.Scene.Frontend.Progression |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.GameOver.Scoreboard` | UI.Scene.Match.GameOver.Scoreboard |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | `UI.Scene.Match.Vendor.Wagers` | UI.Scene.Match.Vendor.Wagers |
| [`DT_SceneData_Match_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/FobRefuelRepair/DT_SceneData_Match_Buildables.json) | `UI.Scene.Match.FobRefuelRepair` | UI.Scene.Match.FobRefuelRepair |
| [`DT_SceneData_Match_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/UI/DT_SceneData_Match_STN_05.json) | `UI.Scene.Match.DroneReload` | UI.Scene.Match.DroneReload |
| [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | `UI.Scene.Match.ContextDrawer` | UI.Scene.Match.ContextDrawer |
| [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) | `UI.Scene.Match.EndgameMovie` | UI.Scene.Match.EndgameMovie |
| [`DT_SceneData_Match_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/UI/Data/DT_SceneData_Match_SupplyCrates.json) | `UI.Scene.Match.VehicleSupplyCrate` | UI.Scene.Match.VehicleSupplyCrate |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | `UI.Scene.Match.WagerStatus` | UI.Scene.Match.WagerStatus |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Popups` | UI.Scene.Shared.Popups |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Shared.Settings` | UI.Scene.Shared.Settings |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Frontend.Loadouts` | UI.Scene.Frontend.Loadouts |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | `UI.Scene.Match.Vendor.Equipment` | UI.Scene.Match.Vendor.Equipment |
<!-- /datatable_catalog -->

## BHGameplayEffectTaggedTableRow

Tables: [`DT_Meta_ResourceEffects`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Resources/Effects/DT_Meta_ResourceEffects.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct BHGameplayEffectTaggedTableRow -->
*1 table(s), 1 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `GameplayEffect` | `Tag` |
|---|---|---|
| `Meta.Effect.Resource` | GE_Meta_ResourceChange.GE_Meta_ResourceChange_C | Meta.Effect.Resource |
<!-- /datatable_catalog -->

## WDAssistanceRequestData

Tables: [`DT_AssistanceRequests`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/AssistanceRequests/DT_AssistanceRequests.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDAssistanceRequestData -->
*1 table(s), 12 rows, 20 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 20:

| Row | `RequestClass` | `EventFeedTag` | `bOnlyShowEventFeedToInvolvedPlayers` | `CancelWhenEnteringVitalityStates` | `Duration` | `GameplayCueDuration` | `MaxDistanceForTeamEvent` |
|---|---|---|---|---|---|---|---|
| `Communication.AssistanceRequest.Ammo` | WDGame.WDAssistanceRequest_Ammo | UI.HUD.Element.EventFeed.Type.Request.Ammo | false | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 0 | 0 | 50 |
| `Communication.AssistanceRequest.Backup` | WDGame.WDAssistanceRequest_Backup | UI.HUD.Element.EventFeed.Type.Request.Backup | false | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 10 | 0 | 50 |
| `Communication.AssistanceRequest.Refueling` | WDGame.WDAssistanceRequest_Refueling | UI.HUD.Element.EventFeed.Type.Request.Refueling | true | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 0 | 0 | 200 |
| `Communication.AssistanceRequest.Healing` | WDGame.WDAssistanceRequest_Healing | UI.HUD.Element.EventFeed.Type.Request.Healing | false | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 0 | 0 | 50 |
| `Communication.AssistanceRequest.Repair` | WDGame.WDAssistanceRequest_Repair | UI.HUD.Element.EventFeed.Type.Request.Repair | true | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 0 | 0 | 200 |
| `Communication.AssistanceRequest.Revive` | WDGame.WDAssistanceRequest_Revive | UI.HUD.Element.EventFeed.Type.Request.Revive | true | State.Player.Vitality.Alive, State.Player.Vitality.Dead | 0 | 0 | 30 |
| `Communication.AssistanceRequest.Pickup` | WDGame.WDAssistanceRequest_Pickup | UI.HUD.Element.EventFeed.Type.Request.Pickup | false | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 0 | 0 | 200 |
| `Communication.AssistanceRequest.Dropoff` | WDGame.WDAssistanceRequest_Dropoff | UI.HUD.Element.EventFeed.Type.Request.Dropoff | true | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 20 | 0 | 1000 |
| `Communication.AssistanceRequest.Getout` | WDGame.WDAssistanceRequest_GetOut | UI.HUD.Element.EventFeed.Type.Request.Getout | false | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 15 | 0 | 30 |
| `Communication.AssistanceRequest.SquadInvite` | WDGame.WDAssistanceRequest_SquadInvite | UI.HUD.Element.EventFeed.Type.Request.SquadInvite | true | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 60 | 0 | 30 |
| `Communication.AssistanceRequest.GetIn` | WDGame.WDAssistanceRequest_GetIn | UI.HUD.Element.EventFeed.Type.Request.GetIn | true | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 20 | 0 | 30 |
| `Communication.AssistanceRequest.Supplies` | WDGame.WDAssistanceRequest_Supplies | UI.HUD.Element.EventFeed.Type.Request.Supplies | false | State.Player.Vitality.Critical, State.Player.Vitality.Dead | 0 | 0 | 50 |

Columns 8-14 of 20:

| Row | `MaxDistanceForVisibleSpatialIcon` | `TagsToBlockRequest` | `RequiredTagsToAcceptRequest` | `bShowToOnlyInVehicle` | `_aaabiallblepnacgldlho` | `_aaabhfplnboaifloconni` | `bCancelRequestOnVehicleEntry` |
|---|---|---|---|---|---|---|---|
| `Communication.AssistanceRequest.Ammo` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Backup` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Refueling` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Healing` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Repair` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Revive` | 500 |  | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Pickup` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vehicle.Role.Driver, State.Player.Vitality.Alive | true | true | true | true |
| `Communication.AssistanceRequest.Dropoff` | 1500 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive, State.Player.Vehicle.Role.Driver | true | true | true | false |
| `Communication.AssistanceRequest.Getout` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive, State.Player.Vehicle.Role | true | false | false | false |
| `Communication.AssistanceRequest.SquadInvite` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Squad.InSquad, State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.GetIn` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | false | false |
| `Communication.AssistanceRequest.Supplies` | 100 | State.Player.Vitality.Critical, State.Player.Vitality.Dead | State.Player.Vitality.Alive | false | false | true | false |

Columns 15-20 of 20:

| Row | `bAutoplayCue` | `AssistanceRequestSpatialContext` | `GameplayCueTag` | `CustomAcknowledgementMessage` | `_aaabdjgllgkciaeipccgg` | `Tag` |
|---|---|---|---|---|---|---|
| `Communication.AssistanceRequest.Ammo` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.Ammo |  |  | Communication.AssistanceRequest.Ammo |
| `Communication.AssistanceRequest.Backup` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.Backup |  |  | Communication.AssistanceRequest.Backup |
| `Communication.AssistanceRequest.Refueling` | true | Communication.AssistanceRequest.Context.Vehicle | GameplayCue.AssistanceRequest.Refueling |  |  | Communication.AssistanceRequest.Refueling |
| `Communication.AssistanceRequest.Healing` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.Healing |  |  | Communication.AssistanceRequest.Healing |
| `Communication.AssistanceRequest.Repair` | true | Communication.AssistanceRequest.Context.Vehicle | GameplayCue.AssistanceRequest.Repair |  |  | Communication.AssistanceRequest.Repair |
| `Communication.AssistanceRequest.Revive` | false | Communication.AssistanceRequest.Context.Player |  |  |  | Communication.AssistanceRequest.Revive |
| `Communication.AssistanceRequest.Pickup` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.Pickup |  |  | Communication.AssistanceRequest.Pickup |
| `Communication.AssistanceRequest.Dropoff` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.Dropoff |  |  | Communication.AssistanceRequest.Dropoff |
| `Communication.AssistanceRequest.Getout` | true | Communication.AssistanceRequest.Context.Vehicle | GameplayCue.AssistanceRequest.Getout |  |  | Communication.AssistanceRequest.Getout |
| `Communication.AssistanceRequest.SquadInvite` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.SquadInvite | UI.HUD.Element.EventFeed.Type.Acknowledgement.SquadInvite |  | Communication.AssistanceRequest.SquadInvite |
| `Communication.AssistanceRequest.GetIn` | true | Communication.AssistanceRequest.Context.Vehicle | GameplayCue.AssistanceRequest.GetIn |  |  | Communication.AssistanceRequest.GetIn |
| `Communication.AssistanceRequest.Supplies` | true | Communication.AssistanceRequest.Context.Player | GameplayCue.AssistanceRequest.Supplies |  | GameplayCue.AssistanceRequest.Supplies.Radio | Communication.AssistanceRequest.Supplies |
<!-- /datatable_catalog -->

## WDPingTypeData

Tables: [`DT_PingTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/Pings/DT_PingTypes.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDPingTypeData -->
*1 table(s), 4 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `_aaaappkbjmlhlgjieakgj` | `Tag` |
|---|---|---|
| `Communication.Ping` | 10 | Communication.Ping |
| `Communication.Ping.Type.Context.Map.MarkCoordinates` | 20 | Communication.Ping.Type.Context.Map.MarkCoordinates |
| `Communication.AssistanceRequest` | 60 | Communication.AssistanceRequest |
| `Trackers.Type.HitMarker` | 150 | Trackers.Type.HitMarker |
<!-- /datatable_catalog -->

## WDVoxBase

Tables: [`DT_VoxData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/General/DT_VoxData.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDVoxBase -->
*1 table(s), 81 rows, 9 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 9:

| Row | `LineID` | `VoxGroup` | `_aaaboohabieiclmklfndp` | `_aaabdahbdpknhigmfnpnd` | `InterruptibleBehavior` | `CooldownTime` | `PreDelayTime` |
|---|---|---|---|---|---|---|---|
| `Audio.Vox.Exertion.Breath.Inhale` | Audio.Vox.Exertion.Breath.Inhale | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.Breath.Exhale` | Audio.Vox.Exertion.Breath.Exhale | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.MeleeSwing` | Audio.Vox.Exertion.MeleeSwing | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.Jump` | Audio.Vox.Exertion.Jump | Exertion | false | NONE | InterruptedOnlyByHigherPriority | 0.35 | 0.01 |
| `Audio.Vox.Exertion.TakingDamage.Light` | Audio.Vox.Exertion.TakingDamage.Light | Bark | true | Exertion | InterruptedOnlyByHigherPriority | 0.01 | 0.15 |
| `Audio.Vox.Exertion.TakingDamage.Heavy` | Audio.Vox.Exertion.TakingDamage.Heavy | Bark | true | Exertion | InterruptedOnlyByHigherPriority | 0.01 | 0.15 |
| `Audio.Vox.Exertion.Vaulting.Fast` | Audio.Vox.Exertion.Vaulting.Fast | Exertion | false | NONE | InterruptedOnlyByHigherPriority | 0.01 | 0.01 |
| `Audio.Vox.Exertion.Vaulting.Slow` | Audio.Vox.Exertion.Vaulting.Slow | Exertion | false | NONE | InterruptedOnlyByHigherPriority | 0.01 | 0.01 |
| `Audio.Vox.Exertion.Vaulting.Slow.Stop` | Audio.Vox.Exertion.Vaulting.Slow.Stop | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.CriticalState` | Audio.Vox.Exertion.CriticalState | Exertion | false | NONE | NotInterruptible | 0.01 | 0.01 |
| `Audio.Vox.Exertion.ThrowingGrenade.OverHand` | Audio.Vox.Exertion.ThrowingGrenade.OverHand | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.ThrowingGrenade.UnderHand` | Audio.Vox.Exertion.ThrowingGrenade.UnderHand | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.ProneMovement` | Audio.Vox.Exertion.ProneMovement | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 5 | 0.01 |
| `Audio.Vox.Exertion.TakingDamage.GoingCritical` | Audio.Vox.Exertion.TakingDamage.GoingCritical | Bark | true | Exertion | NotInterruptible | 0.01 | 0.25 |
| `Audio.Vox.Exertion.Focus.In` | Audio.Vox.Exertion.Focus.In | Exertion | false | NONE | InterruptedOnlyByHigherPriority | 1 | 0.01 |
| `Audio.Vox.Exertion.Focus.Out` | Audio.Vox.Exertion.Focus.Out | Exertion | false | NONE | InterruptedOnlyByHigherPriority | 1 | 0.01 |
| `Audio.Vox.Exertion.TakingDamage.GoingLowHealth` | Audio.Vox.Exertion.TakingDamage.GoingLowHealth | Exertion | false | NONE | NotInterruptible | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Ammo` | Audio.Vox.Bark.Request.Ammo | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Healing` | Audio.Vox.Bark.Request.Healing | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Backup` | Audio.Vox.Bark.Request.Backup | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.GetOut` | Audio.Vox.Bark.Request.GetOut | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Order.Attack` | Audio.Vox.Bark.Order.Attack | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.5 |
| `Audio.Vox.Bark.Order.Defend` | Audio.Vox.Bark.Order.Defend | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.5 |
| `Audio.Vox.Bark.Order.FallBack` | Audio.Vox.Bark.Order.FallBack | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.5 |
| `Audio.Vox.Bark.Order.Fortify` | Audio.Vox.Bark.Order.Fortify | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.5 |
| `Audio.Vox.Bark.Order.Regroup` | Audio.Vox.Bark.Order.Regroup | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.5 |
| `Audio.Vox.Bark.Social.Nice` | Audio.Vox.Bark.Social.Nice | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Social.No` | Audio.Vox.Bark.Social.No | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Social.Sorry` | Audio.Vox.Bark.Social.Sorry | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Social.Thanks` | Audio.Vox.Bark.Social.Thanks | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Social.Yes` | Audio.Vox.Bark.Social.Yes | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Squad.FollowMe` | Audio.Vox.Bark.Squad.FollowMe | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Squad.OnMyWay` | Audio.Vox.Bark.Squad.OnMyWay | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Revive` | Audio.Vox.Bark.Request.Revive | Bark | false | NONE | InterruptedOnlyByHigherPriority | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.AATank` | Audio.Vox.Bark.Spotting.AATank | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Artillery` | Audio.Vox.Bark.Spotting.Artillery | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Bobcat` | Audio.Vox.Bark.Spotting.Bobcat | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Enemy` | Audio.Vox.Bark.Spotting.Enemy | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Havoc` | Audio.Vox.Bark.Spotting.Havoc | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Kodiak` | Audio.Vox.Bark.Spotting.Kodiak | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Littlebird` | Audio.Vox.Bark.Spotting.Littlebird | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.SpawnVehicle` | Audio.Vox.Bark.Spotting.SpawnVehicle | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Tank` | Audio.Vox.Bark.Spotting.Tank | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Target` | Audio.Vox.Bark.Spotting.Target | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Vehicle` | Audio.Vox.Bark.Spotting.Vehicle | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Vehicle.Empty` | Audio.Vox.Bark.Spotting.Vehicle.Empty | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.ATMine` | Audio.Vox.Bark.Spotting.ATMine | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Buildable` | Audio.Vox.Bark.Spotting.Buildable | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.BuildableMagnet` | Audio.Vox.Bark.Spotting.BuildableMagnet | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Claymore` | Audio.Vox.Bark.Spotting.Claymore | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Deployable` | Audio.Vox.Bark.Spotting.Deployable | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.DuneBuggy` | Audio.Vox.Bark.Spotting.DuneBuggy | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.FOB` | Audio.Vox.Bark.Spotting.FOB | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Humvee` | Audio.Vox.Bark.Spotting.Humvee | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Acknowledge` | Audio.Vox.Bark.Request.Acknowledge | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.DropOff` | Audio.Vox.Bark.Request.DropOff | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Fuel` | Audio.Vox.Bark.Request.Fuel | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.GetIn` | Audio.Vox.Bark.Request.GetIn | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Pickup` | Audio.Vox.Bark.Request.Pickup | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.SquadInvite` | Audio.Vox.Bark.Request.SquadInvite | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Repair` | Audio.Vox.Bark.Request.Repair | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Squad.Affirmative` | Audio.Vox.Bark.Squad.Affirmative | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Squad.Negative` | Audio.Vox.Bark.Squad.Negative | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Squad.WatchHere` | Audio.Vox.Bark.Squad.WatchHere | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.5 |
| `Audio.Vox.Bark.Spotting.AntiAir` | Audio.Vox.Bark.Spotting.AntiAir | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.AssaultHumvee` | Audio.Vox.Bark.Spotting.AssaultHumvee | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.AssaultKodiak` | Audio.Vox.Bark.Spotting.AssaultKodiak | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.AssaultUral` | Audio.Vox.Bark.Spotting.AssaultUral | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.AttackLittlebird` | Audio.Vox.Bark.Spotting.AttackLittlebird | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.ForwardOperatingBase` | Audio.Vox.Bark.Spotting.ForwardOperatingBase | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Mortar` | Audio.Vox.Bark.Spotting.Mortar | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.SupplyPoint` | Audio.Vox.Bark.Spotting.SupplyPoint | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Ural` | Audio.Vox.Bark.Spotting.Ural | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Exertion.MeleeSwing.Heavy` | Audio.Vox.Exertion.MeleeSwing.Heavy | Exertion | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Destroy.Player` | Audio.Vox.Bark.Spotting.Destroy.Player | Narrator | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Destroy.Vehicle` | Audio.Vox.Bark.Spotting.Destroy.Vehicle | Narrator | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Destroy.Deployable` | Audio.Vox.Bark.Spotting.Destroy.Deployable | Narrator | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.Destroy.Buildable` | Audio.Vox.Bark.Spotting.Destroy.Buildable | Narrator | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Request.Supplies` | Audio.Vox.Bark.Request.Supplies | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.BlackHawk` | Audio.Vox.Bark.Spotting.BlackHawk | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |
| `Audio.Vox.Bark.Spotting.AttackBlackHawk` | Audio.Vox.Bark.Spotting.AttackBlackHawk | Bark | false | NONE | InterruptedByBothSameAndHigherPriorities | 0.01 | 0.01 |

Columns 8-9 of 9:

| Row | `PostDelayTime` | `Lifetime` |
|---|---|---|
| `Audio.Vox.Exertion.Breath.Inhale` | 0.01 | 5 |
| `Audio.Vox.Exertion.Breath.Exhale` | 0.01 | 5 |
| `Audio.Vox.Exertion.MeleeSwing` | 0.01 | 5 |
| `Audio.Vox.Exertion.Jump` | 0.01 | 0.5 |
| `Audio.Vox.Exertion.TakingDamage.Light` | 0.01 | 5 |
| `Audio.Vox.Exertion.TakingDamage.Heavy` | 0.01 | 5 |
| `Audio.Vox.Exertion.Vaulting.Fast` | 0.01 | 5 |
| `Audio.Vox.Exertion.Vaulting.Slow` | 0.01 | 5 |
| `Audio.Vox.Exertion.Vaulting.Slow.Stop` | 0.01 | 5 |
| `Audio.Vox.Exertion.CriticalState` | 0.01 | 5 |
| `Audio.Vox.Exertion.ThrowingGrenade.OverHand` | 0.01 | 5 |
| `Audio.Vox.Exertion.ThrowingGrenade.UnderHand` | 0.01 | 5 |
| `Audio.Vox.Exertion.ProneMovement` | 0.01 | 1 |
| `Audio.Vox.Exertion.TakingDamage.GoingCritical` | 0.01 | 5 |
| `Audio.Vox.Exertion.Focus.In` | 0.01 | 5 |
| `Audio.Vox.Exertion.Focus.Out` | 0.01 | 5 |
| `Audio.Vox.Exertion.TakingDamage.GoingLowHealth` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Ammo` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Healing` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Backup` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.GetOut` | 0.01 | 5 |
| `Audio.Vox.Bark.Order.Attack` | 0.01 | 5 |
| `Audio.Vox.Bark.Order.Defend` | 0.01 | 5 |
| `Audio.Vox.Bark.Order.FallBack` | 0.01 | 5 |
| `Audio.Vox.Bark.Order.Fortify` | 0.01 | 5 |
| `Audio.Vox.Bark.Order.Regroup` | 0.01 | 5 |
| `Audio.Vox.Bark.Social.Nice` | 0.01 | 5 |
| `Audio.Vox.Bark.Social.No` | 0.01 | 5 |
| `Audio.Vox.Bark.Social.Sorry` | 0.01 | 5 |
| `Audio.Vox.Bark.Social.Thanks` | 0.01 | 5 |
| `Audio.Vox.Bark.Social.Yes` | 0.01 | 5 |
| `Audio.Vox.Bark.Squad.FollowMe` | 0.01 | 5 |
| `Audio.Vox.Bark.Squad.OnMyWay` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Revive` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AATank` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Artillery` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Bobcat` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Enemy` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Havoc` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Kodiak` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Littlebird` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.SpawnVehicle` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Tank` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Target` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Vehicle` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Vehicle.Empty` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.ATMine` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Buildable` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.BuildableMagnet` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Claymore` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Deployable` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.DuneBuggy` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.FOB` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Humvee` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Acknowledge` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.DropOff` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Fuel` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.GetIn` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Pickup` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.SquadInvite` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Repair` | 0.01 | 5 |
| `Audio.Vox.Bark.Squad.Affirmative` | 0.01 | 5 |
| `Audio.Vox.Bark.Squad.Negative` | 0.01 | 5 |
| `Audio.Vox.Bark.Squad.WatchHere` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AntiAir` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AssaultHumvee` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AssaultKodiak` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AssaultUral` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AttackLittlebird` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.ForwardOperatingBase` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Mortar` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.SupplyPoint` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Ural` | 0.01 | 5 |
| `Audio.Vox.Exertion.MeleeSwing.Heavy` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Destroy.Player` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Destroy.Vehicle` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Destroy.Deployable` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.Destroy.Buildable` | 0.01 | 5 |
| `Audio.Vox.Bark.Request.Supplies` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.BlackHawk` | 0.01 | 5 |
| `Audio.Vox.Bark.Spotting.AttackBlackHawk` | 0.01 | 5 |
<!-- /datatable_catalog -->
