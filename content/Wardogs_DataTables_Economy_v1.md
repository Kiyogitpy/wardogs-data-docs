---
title: "Data Tables: Economy and Rewards"
redirect_from: ["/Wardogs_DataTables_Economy_v1.html", "/Wardogs_DataTables_Economy_v1"]
parent: "Data Tables"
grand_parent: "Data Tables & Tags"
description: "Economy tables: rewards, spotting rewards, cash and currency values"
---

# Data Tables: Economy and Rewards
*Generic expansion of the data tables below, built by [`_tools/datatable_catalog.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/datatable_catalog.py) (`--write` is idempotent). Back to the [catalog index](Wardogs_DataTables_v1.md).*

> Columns are the flattened row fields: nested structs are dotted keys, gameplay tags show the tag name, object references show the asset name, arrays are joined with commas. Columns empty in every row are dropped. Long cells are cut with an ellipsis; open the table JSON for the full value.

## WDRewardTableRow

Tables: [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json), [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDRewardTableRow -->
*2 table(s), 81 rows, 7 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Table | Row | `ResourceTag` | `MaxDuration` | `ThresholdValue` | `bOneOffReward` | `ResourceValue` | `_aaaanepakckidoddhnopj` | `Tag` |
|---|---|---|---|---|---|---|---|---|
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.KillScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.KillScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneContested` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneContested |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneNotOwned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneNotOwned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneOwned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneOwned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneEntered` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneEntered |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneNotOwned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneNotOwned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneContested` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneContested |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneOwned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneOwned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneEntered` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneEntered |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneContested` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneContested |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneOwned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneOwned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneNotOwned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneNotOwned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.TowerCaptured` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.TowerCaptured |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.MagnetActivated` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.MagnetActivated |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.MagnetDestroyed` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.MagnetDestroyed |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.RevivedScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.RevivedScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DownedScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DownedScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.HealedScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.HealedScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.RepairingScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.RepairingScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.Builder` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 1 |  | Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.Builder |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.SchematicOwner` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.SchematicOwner |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicBuiltScore.FinalBuilder` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SchematicBuiltScore.FinalBuilder |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicBuiltScore.SchematicOwner` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SchematicBuiltScore.SchematicOwner |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicBuiltInFOBScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 |  | Meta.Progression.Resources.MatchScore.SchematicBuiltInFOBScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 |  | Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.BuildDamaged` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.BuildDamaged |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.VehicleKillScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.VehicleKillScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Faction.FirstPlace` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.Faction.FirstPlace |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Faction.SecondPlace` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.Faction.SecondPlace |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Faction.ThirdPlace` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.Faction.ThirdPlace |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneDeliveredPassengers` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 200 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneDeliveredPassengers |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneDeliveredPassengers` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 200 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneDeliveredPassengers |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZonePassengerSpawned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 50 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZonePassengerSpawned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzonePassengerSpawned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 50 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzonePassengerSpawned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.PassengerSpawned` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.PassengerSpawned |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.PurchaseSupplyCrateItemScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.PurchaseSupplyCrateItemScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SupplyCrateKillScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SupplyCrateKillScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 3000 |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DestoryedUtility` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DestoryedUtility |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Tip.Player.Revive` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 |  | Meta.Progression.Resources.MatchScore.Tip.Player.Revive |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffControlZone` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 10 |  | Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffControlZone |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffHotZone` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 15 |  | Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffHotZone |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Tip.Player.Heal` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 |  | Meta.Progression.Resources.MatchScore.Tip.Player.Heal |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DamageAssist.Player` | Attribute.Meta.Currency.Cash | 60 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DamageAssist.Player |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.TransportAssist.Kill` | Attribute.Meta.Currency.Cash | 600 | 0 | false | 100 |  | Meta.Progression.Resources.MatchScore.TransportAssist.Kill |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DamageAssist.Crew` | Attribute.Meta.Currency.Cash | 15 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DamageAssist.Crew |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DamageAssist.Buildable` | Attribute.Meta.Currency.Cash | 15 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DamageAssist.Buildable |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle` | Attribute.Meta.Currency.Cash | 45 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SuppressionAssist` | Attribute.Meta.Currency.Cash | 30 | 0 | false | 5 |  | Meta.Progression.Resources.MatchScore.SuppressionAssist |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SpawnTransportAssist` | Attribute.Meta.Currency.Cash | 600 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SpawnTransportAssist |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.RefuelingScore` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.RefuelingScore |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DeploySupplyCrate` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DeploySupplyCrate |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DestroyedDeployable` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DestroyedDeployable |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DestroyedDeployable.Friendly` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DestroyedDeployable.Friendly |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicPlaced` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SchematicPlaced |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.SchematicPlaced.FOB` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SchematicPlaced.FOB |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DropOffPassenger` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DropOffPassenger |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.VehicleKillScore.Assist` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.VehicleKillScore.Assist |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.TransportAssist.Revive` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.TransportAssist.Revive |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.TransportAssist.VehicleDestruction` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.TransportAssist.VehicleDestruction |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.PlayerKill` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.PlayerKill |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.VehicleKill` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.VehicleKill |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist.Kill` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ReviveAssist.Kill |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist.Revive` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ReviveAssist.Revive |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist.VehicleDestruction` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ReviveAssist.VehicleDestruction |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.DropOffPassengerSurvived` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.DropOffPassengerSurvived |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.BuildDamaged.Friendly` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.BuildDamaged.Friendly |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.TransportAssist` |  | 600 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.TransportAssist |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.Tip.Heal` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 | 5, 10, 15, 20 | Challenges.Rewards.Tip.Heal |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.Tip.Revive` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 10 | 10, 15, 20, 25 | Challenges.Rewards.Tip.Revive |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.Tip.PlayerDelivered` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 15 | 15, 20, 25, 30 | Challenges.Rewards.Tip.PlayerDelivered |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.Tip.Repair` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 | 5, 10, 15, 20 | Challenges.Rewards.Tip.Repair |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.Tip.Refuel` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 5 | 5, 10, 15, 20 | Challenges.Rewards.Tip.Refuel |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist` |  | 300 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.ReviveAssist |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.PreTip.IncrementAmount` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 50 |  | Challenges.Rewards.PreTip.IncrementAmount |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Challenges.Rewards.PreTip.MaxAmount` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 500 |  | Challenges.Rewards.PreTip.MaxAmount |
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | `Meta.Progression.Resources.MatchScore.MunitionsAssist` |  | 300 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.MunitionsAssist |
| [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json) | `Meta.Progression.Resources.MatchScore.SpottingOwner` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SpottingOwner |
| [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json) | `Meta.Progression.Resources.MatchScore.SpottingAssist` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SpottingAssist |
| [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json) | `Meta.Progression.Resources.MatchScore.SpottingDestroyed` | Attribute.Meta.Currency.Cash | 0 | 0 | false | 0 |  | Meta.Progression.Resources.MatchScore.SpottingDestroyed |
<!-- /datatable_catalog -->

## WDResourceRewardTableRow

Tables: [`DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDResourceRewardTableRow -->
*1 table(s), 49 rows, 5 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `bOneOffReward` | `RewardAmount` | `SimpleModifiers` | `ComplexModifiers` | `Tag` |
|---|---|---|---|---|---|
| `Meta.Progression.Resources.MatchScore.KillScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.KillScore |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneContested` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneContested |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneNotOwned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneNotOwned |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneOwned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneOwned |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneEntered` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneEntered |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneNotOwned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneNotOwned |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneContested` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneContested |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneOwned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneOwned |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneEntered` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneEntered |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneContested` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneContested |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneOwned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneOwned |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneNotOwned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneNotOwned |
| `Meta.Progression.Resources.MatchScore.TowerCaptured` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.TowerCaptured |
| `Meta.Progression.Resources.MatchScore.MagnetActivated` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.MagnetActivated |
| `Meta.Progression.Resources.MatchScore.MagnetDestroyed` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.MagnetDestroyed |
| `Meta.Progression.Resources.MatchScore.RevivedScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.RevivedScore |
| `Meta.Progression.Resources.MatchScore.DownedScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.DownedScore |
| `Meta.Progression.Resources.MatchScore.HealedScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.HealedScore |
| `Meta.Progression.Resources.MatchScore.RepairingScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.RepairingScore |
| `Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.Builder` | false | 0 |  | Meta.Rewards.Modifier.BuildScalar | Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.Builder |
| `Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.SchematicOwner` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.SchematicOwner |
| `Meta.Progression.Resources.MatchScore.SchematicBuiltScore.FinalBuilder` | false | 0 | {Key=Meta.Progression.Context.Instigator.InControlZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=… | Meta.Rewards.Modifier.BuildableBuilt | Meta.Progression.Resources.MatchScore.SchematicBuiltScore.FinalBuilder |
| `Meta.Progression.Resources.MatchScore.SchematicBuiltScore.SchematicOwner` | false | 0 | {Key=Meta.Progression.Context.Instigator.InControlZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=… | Meta.Rewards.Modifier.BuildableBuilt | Meta.Progression.Resources.MatchScore.SchematicBuiltScore.SchematicOwner |
| `Meta.Progression.Resources.MatchScore.SchematicBuiltInFOBScore` | false | 5 | {Key=Meta.Progression.Context.Instigator.InHotZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=5} |  | Meta.Progression.Resources.MatchScore.SchematicBuiltInFOBScore |
| `Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore` | false | 5 | {Key=Meta.Progression.Context.Instigator.InHotZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=5} |  | Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore |
| `Meta.Progression.Resources.MatchScore.BuildDamaged` | false | 0 | {Key=Meta.Progression.Context.Instigator.InControlZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=… |  | Meta.Progression.Resources.MatchScore.BuildDamaged |
| `Meta.Progression.Resources.MatchScore.VehicleKillScore` | false | 0 |  | Meta.Rewards.Modifier.DestroyedVehicleType | Meta.Progression.Resources.MatchScore.VehicleKillScore |
| `Meta.Progression.Resources.MatchScore.Faction.FirstPlace` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.Faction.FirstPlace |
| `Meta.Progression.Resources.MatchScore.Faction.SecondPlace` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.Faction.SecondPlace |
| `Meta.Progression.Resources.MatchScore.Faction.ThirdPlace` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.Faction.ThirdPlace |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneDeliveredPassengers` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneDeliveredPassengers |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneDeliveredPassengers` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneDeliveredPassengers |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZonePassengerSpawned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZonePassengerSpawned |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzonePassengerSpawned` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzonePassengerSpawned |
| `Meta.Progression.Resources.MatchScore.PurchaseSupplyCrateItemScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.PurchaseSupplyCrateItemScore |
| `Meta.Progression.Resources.MatchScore.SupplyCrateKillScore` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.SupplyCrateKillScore |
| `Meta.Progression.Resources.MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered |
| `Meta.Progression.Resources.MatchScore.DestoryedUtility` | false | 0 |  |  | Meta.Progression.Resources.MatchScore.DestoryedUtility |
| `Meta.Progression.Resources.MatchScore.Tip.Player.Revive` | false | 5 |  |  | Meta.Progression.Resources.MatchScore.Tip.Player.Revive |
| `Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffControlZone` | true | 10 |  |  | Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffControlZone |
| `Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffHotZone` | true | 15 |  |  | Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffHotZone |
| `Meta.Progression.Resources.MatchScore.Tip.Player.Heal` | false | 5 |  |  | Meta.Progression.Resources.MatchScore.Tip.Player.Heal |
| `Challenges.Rewards.Tip.Heal` | false | 5 |  |  | Challenges.Rewards.Tip.Heal |
| `Challenges.Rewards.Tip.Revive` | false | 10 |  |  | Challenges.Rewards.Tip.Revive |
| `Challenges.Rewards.Tip.PlayerDelivered` | false | 15 |  |  | Challenges.Rewards.Tip.PlayerDelivered |
| `Challenges.Rewards.Tip.Repair` | false | 5 |  |  | Challenges.Rewards.Tip.Repair |
| `Challenges.Rewards.Tip.Refuel` | false | 5 |  |  | Challenges.Rewards.Tip.Refuel |
| `Challenges.Rewards.PreTip.IncrementAmount` | false | 50 |  |  | Challenges.Rewards.PreTip.IncrementAmount |
| `Challenges.Rewards.PreTip.MaxAmount` | false | 500 |  |  | Challenges.Rewards.PreTip.MaxAmount |
<!-- /datatable_catalog -->

## WDAssistResourceRewardTableRow

Tables: [`DT_AssistCashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_AssistCashRewards.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDAssistResourceRewardTableRow -->
*1 table(s), 9 rows, 9 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 9:

| Row | `MaxDuration` | `bUsesThreshold` | `ThresholdValue` | `RewardAmount` | `bSeparateByAction` | `ActionRewards` | `SimpleModifiers` |
|---|---|---|---|---|---|---|---|
| `Meta.Progression.Resources.MatchScore.DamageAssist.Player` | 60 | false | 1 | 25 | false | {Value.RewardAmount=0} | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Additive; Value.ModifierValue=25}, {Ke… |
| `Meta.Progression.Resources.MatchScore.SpawnTransportAssist` | 300 | false | 30 | 0 | true | {Key=Meta.Progression.Resources.MatchScore.KillScore; Value.RewardAmount=10; Value.MessageTag=UI.Message.Rewa… | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Override; Value.ModifierValue=25}, {Ke… |
| `Meta.Progression.Resources.MatchScore.TransportAssist` | 600 | false | 30 | 0 | true | {Key=Meta.Progression.Resources.MatchScore.KillScore; Value.RewardAmount=10; Value.MessageTag=UI.Message.Rewa… | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Override; Value.ModifierValue=25}, {Ke… |
| `Meta.Progression.Resources.MatchScore.ReviveAssist` | 300 | false | 30 | 0 | true | {Key=Meta.Progression.Resources.MatchScore.KillScore; Value.RewardAmount=10; Value.MessageTag=UI.Message.Rewa… | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Override; Value.ModifierValue=25}, {Ke… |
| `Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle` | 45 | false | 1 | 0 | false |  | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=0}, … |
| `Meta.Progression.Resources.MatchScore.DamageAssist.Buildable` | 60 | false | 1 | 0 | false | {Value.RewardAmount=0} | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Additive; Value.ModifierValue=25}, {Ke… |
| `Meta.Progression.Resources.MatchScore.SuppressionAssist` | 30 | false | 1 | 5 | false |  | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=BaseAdditive; Value.ModifierValue=5}, … |
| `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist` | 0 | false | 1 | 10 | true | {Key=Meta.Progression.Resources.MatchScore.KillScore; Value.RewardAmount=10}, {Key=Meta.Progression.Resources… | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Override; Value.ModifierValue=25}, {Ke… |
| `Meta.Progression.Resources.MatchScore.MunitionsAssist` | 300 | false | 30 | 0 | true |  | {Key=Meta.Progression.Context.Target.InControlZone; Value.ModifierType=Override; Value.ModifierValue=25}, {Ke… |

Columns 8-9 of 9:

| Row | `ComplexModifiers` | `Tag` |
|---|---|---|
| `Meta.Progression.Resources.MatchScore.DamageAssist.Player` | Meta.Rewards.Modifier.DamageScalar | Meta.Progression.Resources.MatchScore.DamageAssist.Player |
| `Meta.Progression.Resources.MatchScore.SpawnTransportAssist` |  | Meta.Progression.Resources.MatchScore.SpawnTransportAssist |
| `Meta.Progression.Resources.MatchScore.TransportAssist` |  | Meta.Progression.Resources.MatchScore.TransportAssist |
| `Meta.Progression.Resources.MatchScore.ReviveAssist` |  | Meta.Progression.Resources.MatchScore.ReviveAssist |
| `Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle` | Meta.Rewards.Modifier.DamageScalar.Vehicle, Meta.Rewards.Modifier.DestroyedVehicleType | Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle |
| `Meta.Progression.Resources.MatchScore.DamageAssist.Buildable` |  | Meta.Progression.Resources.MatchScore.DamageAssist.Buildable |
| `Meta.Progression.Resources.MatchScore.SuppressionAssist` |  | Meta.Progression.Resources.MatchScore.SuppressionAssist |
| `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist` |  | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist |
| `Meta.Progression.Resources.MatchScore.MunitionsAssist` |  | Meta.Progression.Resources.MatchScore.MunitionsAssist |
<!-- /datatable_catalog -->

## WDResourceRewardModifierTableRow

Tables: [`DT_CashRewardModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewardModifiers.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDResourceRewardModifierTableRow -->
*1 table(s), 9 rows, 7 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `ModifierCategory` | `ModifierType` | `ModifierValue` | `ParentTag` | `ModifierValues` | `ScalarModifier` | `Tag` |
|---|---|---|---|---|---|---|---|
| `Meta.Rewards.Modifier.DamageScalar` | Scalar | PostMultiply | 1 |  |  | CF_Reward_Assist_DamagePlayer | Meta.Rewards.Modifier.DamageScalar |
| `Meta.Rewards.Modifier.TransportAssist.VehicleType` | Group | BaseAdditive | 1 | Vehicle.Variant | {Key=Vehicle.Variant.Air.Rotary.Littlebird; Value=0}, {Key=Vehicle.Variant.Land.Wheeled.Kodiak; Value=0} |  | Meta.Rewards.Modifier.TransportAssist.VehicleType |
| `Meta.Rewards.Modifier.DestroyedVehicleType` | Group | BaseAdditive | 1 | Vehicle.Variant | {Key=Vehicle.Variant.Air.Rotary.Littlebird; Value=300}, {Key=Vehicle.Variant.Land.Wheeled.Bobcat; Value=100},… |  | Meta.Rewards.Modifier.DestroyedVehicleType |
| `Meta.Rewards.Modifier.Transport.VehicleType` | Group | BaseAdditive | 1 | Vehicle.Variant | {Key=Vehicle.Variant.Air.Rotary; Value=25}, {Key=Vehicle.Variant.Land.Wheeled; Value=40}, {Key=Vehicle.Varian… |  | Meta.Rewards.Modifier.Transport.VehicleType |
| `Meta.Rewards.Modifier.DamageScalar.Vehicle` | Scalar | PostMultiply | 1 |  |  | CF_Reward_Assist_DamageVehicle | Meta.Rewards.Modifier.DamageScalar.Vehicle |
| `Meta.Rewards.Modifier.VehicleKill.VehicleType` | Group | BaseAdditive | 1 | Vehicle.Variant | {Key=Vehicle.Variant.Air.Rotary; Value=25}, {Key=Vehicle.Variant.Land.Wheeled; Value=50}, {Key=Vehicle.Varian… |  | Meta.Rewards.Modifier.VehicleKill.VehicleType |
| `Meta.Rewards.Modifier.PurchaseScalar.SupplyCrate` | Scalar | BaseAdditive | 1 |  |  | CF_Reward_SupplyCrateItemPurchase | Meta.Rewards.Modifier.PurchaseScalar.SupplyCrate |
| `Meta.Rewards.Modifier.BuildScalar` | Scalar | Additive | 1 |  |  | CF_Reward_Build | Meta.Rewards.Modifier.BuildScalar |
| `Meta.Rewards.Modifier.BuildableBuilt` | Group | Additive | 1 | Id.Buildable | {Key=Id.Buildable.HBlock; Value=20}, {Key=Id.Buildable.TallHBlock; Value=25}, {Key=Id.Buildable.SandbagWall; … |  | Meta.Rewards.Modifier.BuildableBuilt |
<!-- /datatable_catalog -->

## WDRewardFeedActionDataTableRow

Tables: [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json), [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json), [`DT_ChallengesFeedActions_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengesFeedActions_Crowbar.json), [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json), [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json), [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json), [`DT_RewardFeedActions_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/RewardFeed/DT_RewardFeedActions_HotZoneMagnet.json), [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json), [`DT_RewardFeedActions_TeamOffence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Data/UI/RewardFeed/DT_RewardFeedActions_TeamOffence.json), [`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDRewardFeedActionDataTableRow -->
*10 table(s), 159 rows, 5 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Table | Row | `ConditionalExpressions` | `DisplayText` | `bIsTip` | `AudioEventTag` | `Tag` |
|---|---|---|---|---|---|---|
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.RessedByEnemy; Condition.QueryTok… | Kill | false |  | Challenges.Rewards.PlayerKill |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.CrewAssist` |  | Kill Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.CrewAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.LogisticAssist` |  | Deployed Player Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.ReviveAssist` |  | Revived Player Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.FOBSuppliedAssist` |  | FOB Supplied Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.FOBSuppliedAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.SupplyCrateAssist` |  | Supplied Player Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.Assist` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.FriendlyKill; Condition.QueryToke… | Kill Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.Assist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.Assist.CrewAssist` |  | Kill Assist | false | Audio.Event.UX.Combat.KillAssist | Challenges.Rewards.PlayerKill.Assist.CrewAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.Assist.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.PlayerKill.Assist.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.Assist.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.PlayerKill.Assist.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.Assist.FOBSuppliedAssist` |  | FOB Supplied Assist | false |  | Challenges.Rewards.PlayerKill.Assist.FOBSuppliedAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerKill.Assist.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.PlayerKill.Assist.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RevivePlayer` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.LastKiller; Condition.QueryTokenS… | Revived Teammate | false | Audio.Event.UX.Cash.RevivedScore | Challenges.Rewards.RevivePlayer |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RevivePlayer.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.RevivePlayer.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RevivePlayer.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.RevivePlayer.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RevivePlayer.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.RevivePlayer.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RevivePlayer.TargetInObjective` |  | Waited to be revived | false |  | Challenges.Rewards.RevivePlayer.TargetInObjective |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RevivePlayer.Contributor` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.LastKiller; Condition.QueryTokenS… | Helped Revive Teammate | false | Audio.Event.UX.Cash.RevivedScore | Challenges.Rewards.RevivePlayer.Contributor |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.HealPlayer` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.Heal.BuffItem; Condition.QueryTok… | Healed Teammate | false | Audio.Event.UX.Cash.HealedScore | Challenges.Rewards.HealPlayer |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.HealPlayer.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.HealPlayer.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.HealPlayer.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.HealPlayer.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.HealPlayer.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.HealPlayer.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Rewards.VehicleDestroyed.SpawnVehicle, Ve… | Vehicle Destroyed | false | Audio.Event.UX.Cash.DestroyedVehicle | Challenges.Rewards.VehicleDestroyed |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.CrewAssist` |  | Vehicle Destroyed Assist | false | Audio.Event.UX.Cash.DestroyedVehicle | Challenges.Rewards.VehicleDestroyed.CrewAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.VehicleDestroyed.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.VehicleDestroyed.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist` |  | FOB Supplied Assist | false |  | Challenges.Rewards.VehicleDestroyed.FOBSuppliedAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.VehicleDestroyed.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.Assist` |  | Vehicle Destroyed Assist | false | Audio.Event.UX.Cash.Assist.Crew | Challenges.Rewards.VehicleDestroyed.Assist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.Assist.CrewAssist` |  | Vehicle Destroyed Assist | false | Audio.Event.UX.Cash.Assist.Crew | Challenges.Rewards.VehicleDestroyed.Assist.CrewAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.Assist.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.VehicleDestroyed.Assist.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.Assist.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.VehicleDestroyed.Assist.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.Assist.FOBSuppliedAssist` |  | FOB Supplied Assist | false |  | Challenges.Rewards.VehicleDestroyed.Assist.FOBSuppliedAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleDestroyed.Assist.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.VehicleDestroyed.Assist.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Attribute.Gameplay.Health.Engine; Condition.QueryTok… |  | false |  | Challenges.Rewards.DestroyVehicleSection |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.CrewAssist` |  | Vehicle Section Destroyed Assist | false |  | Challenges.Rewards.DestroyVehicleSection.CrewAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.DestroyVehicleSection.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.DestroyVehicleSection.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.DestroyVehicleSection.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.Assist` |  | Vehicle Section Destroyed Assist | false |  | Challenges.Rewards.DestroyVehicleSection.Assist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.Assist.CrewAssist` |  | Vehicle Section Destroyed Assist | false |  | Challenges.Rewards.DestroyVehicleSection.Assist.CrewAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.Assist.LogisticAssist` |  | Deployed Player Assist | false |  | Challenges.Rewards.DestroyVehicleSection.Assist.LogisticAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.Assist.ReviveAssist` |  | Revived Player Assist | false |  | Challenges.Rewards.DestroyVehicleSection.Assist.ReviveAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyVehicleSection.Assist.SupplyCrateAssist` |  | Supplied Player Assist | false |  | Challenges.Rewards.DestroyVehicleSection.Assist.SupplyCrateAssist |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.ZoneEntry` |  | Control Zone Entered | false |  | Challenges.Rewards.ZoneEntry |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.ZoneEntry.SpawnVehicle` |  | Spawn Vehicle Delivered | false | Audio.Event.UX.Cash.DeliveredSpawnVehicle | Challenges.Rewards.ZoneEntry.SpawnVehicle |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.ZonePresence` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.Instigator.InHotZone, Challenges.… | Control Zone Presence | false |  | Challenges.Rewards.ZonePresence |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroyThrowable` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Meta.Progression.Context.Player.Faction.Friendly; Co… | Equipment Destroyed | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.DestroyThrowable |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RefuelVehicle` |  | Refuelled Vehicle | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.RefuelVehicle |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DeployOnVehicle` |  | Spawn Vehicle Tactical Deployment | false |  | Challenges.Rewards.DeployOnVehicle |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DeploySupplyCrate` |  | Supplies Delivered | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.DeploySupplyCrate |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.RepairVehicle` |  | Repaired Vehicle | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.RepairVehicle |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PurchaseFromSupplyCrate` |  | Supply Crate Item Sold | false | Audio.Event.UX.Cash.PurchaseSupplies | Challenges.Rewards.PurchaseFromSupplyCrate |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.DestroySupplyCrate` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.Target.Friendly; Condition.QueryT… | Destroyed Supply Crate | false | Audio.Event.UX.Cash.DestroyedVehicle | Challenges.Rewards.DestroySupplyCrate |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.SupplyCrateDestroyed` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=ID.Item.VehicleSupplyCrate; Condition.QueryTokenStre… | Supplies Destroyed | false |  | Challenges.Rewards.SupplyCrateDestroyed |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PlayerDelivered` |  | Tactical Deployment | false | Audio.Event.UX.Cash.DeliveredPassenger | Challenges.Rewards.PlayerDelivered |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.PassengerSurvived` |  | Passenger Survived | false | Audio.Event.UX.Cash.PassengerSurvived | Challenges.Rewards.PassengerSurvived |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.SafeZoneEntered` |  | Round Trip | false | Audio.Event.UX.Cash.RevivedScore | Challenges.Rewards.SafeZoneEntered |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.SendTip` |  | Tip | true | Audio.Event.UX.Cash.Tip | Challenges.Rewards.SendTip |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.SendPreTip` |  | Bribe | false | Audio.Event.UX.Cash.Bribe | Challenges.Rewards.SendPreTip |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.ReceiveTip` |  | Tip | true | Audio.Event.UX.Cash.Tip | Challenges.Rewards.ReceiveTip |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.ReceivePreTip` |  | Bribe | false | Audio.Event.UX.Cash.Tip | Challenges.Rewards.ReceivePreTip |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.SupplyPalletDropped` |  | Supplies Delivered | false | Audio.Event.UX.Cash.DeliveredSpawnVehicle | Challenges.Rewards.SupplyPalletDropped |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleAirborne` |  | Air Time Bonus | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.VehicleAirborne |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleFlyThrough` |  | Fly Through Bonus | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.VehicleFlyThrough |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.Test` |  | TEST EVENT | false |  | Challenges.Rewards.Test |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleRepair` |  | Vehicle Repairing | false |  | Challenges.Rewards.VehicleRepair |
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | `Challenges.Rewards.VehicleRefuel` |  | Vehicle Refuelling | false |  | Challenges.Rewards.VehicleRefuel |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildableDamaged` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.Buildables.Friendly; Condition.Qu… | Buildable Damaged | false |  | Challenges.Rewards.Buildables.BuildableDamaged |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildableDestroyed` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Context.Buildables.Friendly; Condition.Qu… | Buildable Destroyed | false | Audio.Event.UX.Cash.RevivedScore | Challenges.Rewards.Buildables.BuildableDestroyed |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildableDestroyed.Assist` |  | Buildable Destroyed Assist | false | Audio.Event.UX.Cash.BuiltScore | Challenges.Rewards.Buildables.BuildableDestroyed.Assist |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.Building` |  | Building | false |  | Challenges.Rewards.Buildables.Building |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildableFinished` |  | Building Complete | false | Audio.Event.UX.Cash.HealedScore | Challenges.Rewards.Buildables.BuildableFinished |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.SchematicPlaced` |  | Build Schematic Placed | false |  | Challenges.Rewards.Buildables.SchematicPlaced |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildSuppliesDeposited` |  | Supplies Deposited | false | Audio.Event.UX.Cash.HotzoneReward | Challenges.Rewards.Buildables.BuildSuppliesDeposited |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildSuppliesConsumed.Owner` |  | Supplies Used  | false |  | Challenges.Rewards.Buildables.BuildSuppliesConsumed.Owner |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.BuildSuppliesConsumed.Instigator` |  | Supplies Consumed | false |  | Challenges.Rewards.Buildables.BuildSuppliesConsumed.Instigator |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.FOBOwnerPayed` |  | FOB Resources Used | false |  | Challenges.Rewards.Buildables.FOBOwnerPayed |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.FOBHacked` |  | FOB Hacked | false | Audio.Event.UX.Cash.RevivedScore | Challenges.Rewards.Buildables.FOBHacked |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | `Challenges.Rewards.Buildables.FOBDoorClosed` |  | FOB Door Closed | false | Audio.Event.UX.Cash.HealedScore | Challenges.Rewards.Buildables.FOBDoorClosed |
| [`DT_ChallengesFeedActions_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengesFeedActions_Crowbar.json) | `Challenges.Rewards.Crowbar.DoorForcedOpen` |  | Door Breached | false | Audio.Event.UX.Cash.HealedScore | Challenges.Rewards.Crowbar.DoorForcedOpen |
| [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json) | `Challenges.Rewards.Spotting.Added` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Challenges.Rewards.Spotting.Refreshed; Condition.Que… | Target Spotted | false |  | Challenges.Rewards.Spotting.Added |
| [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json) | `Challenges.Rewards.Spotting.Refreshed` |  | Target Spotted Refreshed | false |  | Challenges.Rewards.Spotting.Refreshed |
| [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json) | `Challenges.Rewards.Spotting.Removed` | {Condition.TokenStreamVersion=0; Condition.TagDictionary=Id.Item; Condition.QueryTokenStream=0, 1, 1, 1, 0; C… | Spotted Target Destroyed | false | Audio.Event.UX.Spotted.DestroyAssist.Player | Challenges.Rewards.Spotting.Removed |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneContested` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneEntered` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneOwned` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneNotOwned` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneContested` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneEntered` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneOwned` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneNotOwned` |  |  | false |  |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZoneDeliveredPassengers` |  |  | false | Audio.Event.UX.Cash.DeliveredPassenger |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzoneDeliveredPassengers` |  |  | false | Audio.Event.UX.Cash.DeliveredPassenger |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.ControlZonePassengerSpawned` |  |  | false | Audio.Event.UX.Cash.SpawnPassenger |  |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.HotzonePassengerSpawned` |  |  | false | Audio.Event.UX.Cash.SpawnPassenger |  |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DownedScore` |  | Enemy Player Downed | false |  | Meta.Progression.Resources.MatchScore.DownedScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.HealedScore` |  | Friendly Player Healed | false | Audio.Event.UX.Cash.HealedScore | Meta.Progression.Resources.MatchScore.HealedScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.KillScore` |  | Enemy Player Killed | false |  | Meta.Progression.Resources.MatchScore.KillScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.VehicleKillScore` |  | Enemy Vehicle Destroyed | false | Audio.Event.UX.Cash.DestroyedVehicle | Meta.Progression.Resources.MatchScore.VehicleKillScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.RevivedScore` |  | Friendly Player Revived | false | Audio.Event.UX.Cash.RevivedScore | Meta.Progression.Resources.MatchScore.RevivedScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DamageAssist.Player` |  | Enemy Kill Assist | false | Audio.Event.UX.Combat.KillAssist | Meta.Progression.Resources.MatchScore.DamageAssist.Player |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.DownedTeammate` |  | Teammate Downed | false |  | UI.Message.RewardFeed.DownedTeammate |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.KilledTeammate` |  | Teammate Killed | false | Audio.Event.UX.Cash.TeammateKill | UI.Message.RewardFeed.KilledTeammate |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.TransportAssist.Kill` |  | Transport Kill Assist | false |  | Meta.Progression.Resources.MatchScore.TransportAssist.Kill |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.DestroyedFriendlyVehicle` |  | Friendly Vehicle Destroyed | false |  | UI.Message.RewardFeed.DestroyedFriendlyVehicle |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.DestroyedNeutralVehicle` |  | Neutral Vehicle Destroyed | false |  | UI.Message.RewardFeed.DestroyedNeutralVehicle |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.DamageAssist.Friendly` |  | Teammate Kill Assist | false |  | UI.Message.RewardFeed.DamageAssist.Friendly |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle` |  | Enemy Vehicle Kill Assist | false |  | Meta.Progression.Resources.MatchScore.DamageAssist.Vehicle |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.DamageAssist.Vehicle.Friendly` |  | Friendly Vehicle Kill Assist | false |  | UI.Message.RewardFeed.DamageAssist.Vehicle.Friendly |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.RepairingScore` |  | Friendly Vehicle Repaired | false | Audio.Event.UX.Cash.RepairingScore | Meta.Progression.Resources.MatchScore.RepairingScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.PurchaseSupplyCrateItemScore` |  | Supply Crate Item Purchased | false |  | Meta.Progression.Resources.MatchScore.PurchaseSupplyCrateItemScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SupplyCrateKillScore` |  | Destroyed Enemy Supply Crate | false | Audio.Event.UX.Cash.DestroyedVehicle | Meta.Progression.Resources.MatchScore.SupplyCrateKillScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DeploySupplyCrate` |  | Deployed Supply Crate | false |  | Meta.Progression.Resources.MatchScore.DeploySupplyCrate |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `UI.Message.RewardFeed.DestroyedFriendlySupplyCrate` |  | Destroyed Friendly Supply Crate | false |  | UI.Message.RewardFeed.DestroyedFriendlySupplyCrate |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneNotOwned` |  | Magnet Presence | false |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneNotOwned |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneOwned` |  | Magnet Presence | false |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.MagnetZoneOwned |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.TowerCaptured` |  | Tower Captured | false | Audio.Event.UX.Cash.BuiltScore | Meta.Progression.Resources.MatchScore.TowerCaptured |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.MagnetActivated` |  | Magnet Activated | false | Audio.Event.UX.Cash.RevivedScore | Meta.Progression.Resources.MatchScore.MagnetActivated |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.MagnetDestroyed` |  | Magnet Destroyed | false | Audio.Event.UX.Cash.DestroyedVehicle | Meta.Progression.Resources.MatchScore.MagnetDestroyed |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.SchematicOwner` |  | Schematic Building! | false |  | Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.SchematicOwner |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.Builder` |  | Building | false |  | Meta.Progression.Resources.MatchScore.SchematicBuildStepScore.Builder |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicBuiltScore.FinalBuilder` |  | Finished Building | false | Audio.Event.UX.Cash.BuiltScore | Meta.Progression.Resources.MatchScore.SchematicBuiltScore.FinalBuilder |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicBuiltScore.SchematicOwner` |  | Buildable Complete | false |  | Meta.Progression.Resources.MatchScore.SchematicBuiltScore.SchematicOwner |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicBuiltInFOBScore` |  | Build Finished In FOB | false |  | Meta.Progression.Resources.MatchScore.SchematicBuiltInFOBScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore` |  | Schematic Placed In FOB | false |  | Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.BuildDamaged` |  | Enemy Buildable Damaged | false |  | Meta.Progression.Resources.MatchScore.BuildDamaged |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered` |  | Spawn Vehicle Delivered | false | Audio.Event.UX.Cash.DeliveredSpawnVehicle | Meta.Progression.Resources.MatchScore.ObjectiveScore.SpawnVehicle.ControlZoneEntered |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist` |  | Crew Assist | false |  | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DestoryedUtility` |  | Destroyed Utility | false | Audio.Event.UX.Cash.RepairingScore | Meta.Progression.Resources.MatchScore.DestoryedUtility |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ObjectiveScore.PassengerSpawned` |  | Passenger Spawned In Control Zone | false |  | Meta.Progression.Resources.MatchScore.ObjectiveScore.PassengerSpawned |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.RefuelingScore` |  | Refueling Vehicle | false | Audio.Event.UX.Cash.RepairingScore | Meta.Progression.Resources.MatchScore.RefuelingScore |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DropOffPassenger` |  | Passenger Delivered | false | Audio.Event.UX.Cash.DeliveredPassenger | Meta.Progression.Resources.MatchScore.DropOffPassenger |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist` |  | Friendly Player Revived Assist | false |  | Meta.Progression.Resources.MatchScore.ReviveAssist |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DestroyedDeployable` |  | Enemy Deployable Destroyed | false | Audio.Event.UX.Cash.RepairingScore | Meta.Progression.Resources.MatchScore.DestroyedDeployable |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DestroyedDeployable.Friendly` |  | Friendly Deployable Destroyed | false |  | Meta.Progression.Resources.MatchScore.DestroyedDeployable.Friendly |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicPlaced` |  | Schematic Placed | false |  | Meta.Progression.Resources.MatchScore.SchematicPlaced |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.SchematicPlaced.FOB` |  | FOB Placed | false | Audio.Event.UX.Cash.RevivedScore | Meta.Progression.Resources.MatchScore.SchematicPlaced.FOB |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.VehicleKillScore.Assist` |  | Enemy Vehicle Destroyed Assist | false |  | Meta.Progression.Resources.MatchScore.VehicleKillScore.Assist |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.TransportAssist.Revive` |  | Transport Revive Assist | false |  | Meta.Progression.Resources.MatchScore.TransportAssist.Revive |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.TransportAssist.VehicleDestruction` |  | Transport Vehicle Destroyed Assist | false |  | Meta.Progression.Resources.MatchScore.TransportAssist.VehicleDestruction |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.PlayerKill` |  | Crew Assist Player Kill | false | Audio.Event.UX.Combat.KillAssist | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.PlayerKill |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.VehicleKill` |  | Crew Assist Vehicle Destroyed | false |  | Meta.Progression.Resources.MatchScore.Vehicle.CrewAssist.VehicleKill |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist.Kill` |  | Revive Kill Assist | false |  | Meta.Progression.Resources.MatchScore.ReviveAssist.Kill |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist.Revive` |  | Revive Revive Assist | false |  | Meta.Progression.Resources.MatchScore.ReviveAssist.Revive |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.ReviveAssist.VehicleDestruction` |  | Revive Vehicle Destroyed Assist | false |  | Meta.Progression.Resources.MatchScore.ReviveAssist.VehicleDestruction |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.DropOffPassengerSurvived` |  | Passenger Survived | false | Audio.Event.UX.Cash.PassengerSurvived | Meta.Progression.Resources.MatchScore.DropOffPassengerSurvived |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | `Meta.Progression.Resources.MatchScore.BuildDamaged.Friendly` |  | Friendly Buildable Damaged | false |  | Meta.Progression.Resources.MatchScore.BuildDamaged.Friendly |
| [`DT_RewardFeedActions_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/RewardFeed/DT_RewardFeedActions_HotZoneMagnet.json) | `Challenges.Rewards.HotZoneMagnet.TowerCaptured` |  | Tower Captured | false | Audio.Event.UX.Cash.BuiltScore | Challenges.Rewards.HotZoneMagnet.TowerCaptured |
| [`DT_RewardFeedActions_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/RewardFeed/DT_RewardFeedActions_HotZoneMagnet.json) | `Challenges.Rewards.HotZoneMagnet.MagnetActivated` |  | Magnet Activated | false | Audio.Event.UX.Cash.RevivedScore | Challenges.Rewards.HotZoneMagnet.MagnetActivated |
| [`DT_RewardFeedActions_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/RewardFeed/DT_RewardFeedActions_HotZoneMagnet.json) | `Challenges.Rewards.HotZoneMagnet.MagnetDeactivated` |  | Magnet Deactivated | false | Audio.Event.UX.Cash.DestroyedVehicle | Challenges.Rewards.HotZoneMagnet.MagnetDeactivated |
| [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json) | `Meta.Progression.Resources.MatchScore.SpottingOwner` |  | Target Spotted | false |  | Meta.Progression.Resources.MatchScore.SpottingOwner |
| [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json) | `Meta.Progression.Resources.MatchScore.SpottingAssist` |  | Target Spotted Assist | false |  | Meta.Progression.Resources.MatchScore.SpottingAssist |
| [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json) | `Meta.Progression.Resources.MatchScore.SpottingDestroyed` |  | Spotted Target Destroyed | false | Audio.Event.UX.Spotted.DestroyAssist | Meta.Progression.Resources.MatchScore.SpottingDestroyed |
| [`DT_RewardFeedActions_TeamOffence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Data/UI/RewardFeed/DT_RewardFeedActions_TeamOffence.json) | `Challenges.Rewards.TeamOffence.Forgive` |  |  | false | Audio.Event.UX.Cash.RepairingScore | Challenges.Rewards.TeamOffence.Forgive |
| [`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json) | `Meta.Progression.Resources.MatchScore.Tip.Player.Revive` |  |  | false | Audio.Event.UX.Cash.Tip | Meta.Progression.Resources.MatchScore.Tip.Player.Revive |
| [`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json) | `Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffControlZone` |  |  | false | Audio.Event.UX.Cash.Tip | Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffControlZone |
| [`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json) | `Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffHotZone` |  |  | false | Audio.Event.UX.Cash.Tip | Meta.Progression.Resources.MatchScore.Tip.Vehicle.DropOffHotZone |
| [`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json) | `Meta.Progression.Resources.MatchScore.Tip.Player.Heal` |  |  | false | Audio.Event.UX.Cash.Tip | Meta.Progression.Resources.MatchScore.Tip.Player.Heal |
<!-- /datatable_catalog -->

## WDEventFeedActionDataTableRow

Tables: [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json), [`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDEventFeedActionDataTableRow -->
*2 table(s), 37 rows, 4 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Table | Row | `DisplayTextSelf` | `DisplayTextOther` | `MaxDistanceForTeamEvents` | `Tag` |
|---|---|---|---|---|---|
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Acknowledgement` | {RequestPlayerName} acknowledged <Highlight>{PlayerName}</>'s request | {RequestPlayerName} acknowledged your request | 0 | UI.HUD.Element.EventFeed.Type.Acknowledgement |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Safezone.Exit` | {RequestPlayerName} have left the Safe Zone |  | 0 | UI.HUD.Element.EventFeed.Type.Safezone.Exit |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Cancelled` | {RequestPlayerName} canceled your request | {RequestPlayerName} canceled their request | 0 | UI.HUD.Element.EventFeed.Type.Request.Cancelled |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Ammo` | {RequestPlayerName} requested <Highlight>{AmmoType} Ammo</> | {RequestPlayerName} is requesting <Highlight>{AmmoType} Ammo</> | 2500000000 | UI.HUD.Element.EventFeed.Type.Request.Ammo |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Healing` | {RequestPlayerName} requested <Highlight>Healing</> | {RequestPlayerName} is requesting <Highlight>Healing</> | 2500000000 | UI.HUD.Element.EventFeed.Type.Request.Healing |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Healing.Failed` | {RequestPlayerName} are already at full health |  | 0 | UI.HUD.Element.EventFeed.Type.Request.Healing.Failed |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Revive` | {RequestPlayerName} requested <Highlight>Revive</> | {RequestPlayerName} is requesting <Highlight>Revive</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Revive |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Refueling` | {RequestPlayerName} requested <Highlight>Fuel</> | {RequestPlayerName} is requesting <Highlight>Fuel</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Refueling |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Repair` | {RequestPlayerName} requested <Highlight>Vehicle Repairs</> | {RequestPlayerName} is requesting <Highlight>Vehicle Repairs</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Repair |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Pickup` | {RequestPlayerName} requested <Highlight>Pickup</> | {RequestPlayerName} is requesting <Highlight>Pickup</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Pickup |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Dropoff` | {RequestPlayerName} requested <Highlight>Dropoff</> | {RequestPlayerName} is requesting <Highlight>Dropoff</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Dropoff |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Squad.Request` | {RequestPlayerName} are looking for a squad | {RequestPlayerName} is looking for a squad | 0 | UI.HUD.Element.EventFeed.Type.Squad.Request |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Squad.Joined` | {RequestPlayerName} have joined <Highlight>{SquadName}</> |  | 0 | UI.HUD.Element.EventFeed.Type.Squad.Joined |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Squad.Added` | {RequestPlayerName} have been added to <Highlight>{SquadName}</> |  | 0 | UI.HUD.Element.EventFeed.Type.Squad.Added |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Squad.Kicked` | {RequestPlayerName} have been kicked from <Highlight>{SquadName}</> |  | 0 | UI.HUD.Element.EventFeed.Type.Squad.Kicked |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Item` | {RequestPlayerName} pinged <Highlight>{ItemName}</> | {RequestPlayerName} is pinging <Highlight>{ItemName}</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Item |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Weapon` | {RequestPlayerName} are looking for <Highlight>{AmmoType} ({CurrentAmmo})</> | {RequestPlayerName} is looking for <Highlight>{AmmoType} ({CurrentAmmo})</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Weapon |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Weapon.Attachment` | {RequestPlayerName} are looking for <Highlight>{AttachmentType}</> | {RequestPlayerName} is looking for <Highlight>{AttachmentType}</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Weapon.Attachment |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Weapon.Slot` | {RequestPlayerName} are looking for <Highlight>{WeaponType}</> | {RequestPlayerName} is looking for <Highlight>{WeaponType}</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Weapon.Slot |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Armor` | {RequestPlayerName} have <Highlight>Lvl {ArmorLevel} {ArmorType} ({ArmorDurability})</> | {RequestPlayerName} has <Highlight>Lvl {ArmorLevel} {ArmorType} ({ArmorDurability})</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Armor |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Armor.Slot` | {RequestPlayerName} are looking for <Highlight>{ArmorType}</> | {RequestPlayerName} is looking for <Highlight>{ArmorType}</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Armor.Slot |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Ping.Traversal.Slot` | {RequestPlayerName} are looking for <Highlight>{TraversalType}</> | {RequestPlayerName} is looking for <Highlight>{TraversalType}</> | 0 | UI.HUD.Element.EventFeed.Type.Ping.Traversal.Slot |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Ammo.Failed` | {RequestPlayerName} are already at full ammo |  | 0 | UI.HUD.Element.EventFeed.Type.Request.Ammo.Failed |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Disacknowledgement` | {RequestPlayerName} Disacknowledged <Highlight>{PlayerName}</>'s request | {RequestPlayerName} Disacknowledged your request | 0 | UI.HUD.Element.EventFeed.Type.Disacknowledgement |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Refueling.Failed` | Vehicle is already at full fuel. |  | 0 | UI.HUD.Element.EventFeed.Type.Request.Refueling.Failed |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Repair.Failed` | Vehicle is already at full health. |  | 0 | UI.HUD.Element.EventFeed.Type.Request.Repair.Failed |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.GetOut` | {RequestPlayerName} requested passengers to <Highlight>Get Out</> | {RequestPlayerName} is requesting you <Highlight>Get Out</> of their vehicle. | 0 | UI.HUD.Element.EventFeed.Type.Request.GetOut |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Backup` | {RequestPlayerName} requested <Highlight>Backup</> | {RequestPlayerName} is requesting <Highlight>Backup</> | 2500000000 | UI.HUD.Element.EventFeed.Type.Request.Backup |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.SquadInvite` | {RequestPlayerName} requested a <Highlight>Squad Invite</> | {RequestPlayerName} is requesting a <Highlight>Squad Invite</> | 0 | UI.HUD.Element.EventFeed.Type.Request.SquadInvite |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Acknowledgement.SquadInvite` | {RequestPlayerName} have been added to<Highlight>{Squad} Squad</> | {RequestPlayerName} has been added to<Highlight>{Squad} Squad</> | 0 | UI.HUD.Element.EventFeed.Type.Acknowledgement.SquadInvite |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.GetIn` | {RequestPlayerName} requested teammates to <Highlight>Get In</> | {RequestPlayerName} is requesting you to <Highlight>Get In</> their vehicle. | 0 | UI.HUD.Element.EventFeed.Type.Request.GetIn |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Dropoff.Exact` | {RequestPlayerName} requested <Highlight>Dropoff</> at <Highlight>[x: {X}] [y: {Y}]</> | {RequestPlayerName} is requesting <Highlight>Dropoff</> at <Highlight>[x: {X}] [y: {Y}]</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Dropoff.Exact |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Supplies` | {RequestPlayerName} requested <Highlight>Supplies</> | {RequestPlayerName} is requesting <Highlight>Supplies</> | 0 | UI.HUD.Element.EventFeed.Type.Request.Supplies |
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | `UI.HUD.Element.EventFeed.Type.Request.Ammo.NoWeapon` | {RequestPlayerName} have no weapon to resupply |  | 0 | UI.HUD.Element.EventFeed.Type.Request.Ammo.NoWeapon |
| [`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json) | `UI.HUD.Element.EventFeed.Type.SniperShowdown.StandingStill` | Keep moving or you will be revealed. |  | 0 | UI.HUD.Element.EventFeed.Type.SniperShowdown.StandingStill |
| [`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json) | `UI.HUD.Element.EventFeed.Type.SniperShowdown.Spotted` | You have been revealed. Run. |  | 0 | UI.HUD.Element.EventFeed.Type.SniperShowdown.Spotted |
| [`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json) | `UI.HUD.Element.EventFeed.Type.SniperShowdown.MovingClear` | You are now hidden. |  | 0 | UI.HUD.Element.EventFeed.Type.SniperShowdown.MovingClear |
<!-- /datatable_catalog -->

## WDRewardDefinition

Tables: [`DT_DemoRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/Demo/DT_DemoRewards.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDRewardDefinition -->
*1 table(s), 1 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Resources` | `Tag` |
|---|---|---|
| `Meta.Progression.Context.DefaultReward` | {Key=Attribute.Meta.Currency.Cash; Value.BaseValue=100; Value.Modifiers={ContextQuery.TokenStreamVersion=0; C… | Meta.Progression.Context.DefaultReward |
<!-- /datatable_catalog -->

## WDGoldMarketItemTableRow

Tables: [`DT_GoldMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Collection/DT_GoldMarket.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDGoldMarketItemTableRow -->
*1 table(s), 27 rows, 8 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 8:

| Row | `GoldBarCost` | `Category` | `EntityId` | `GridIndex` | `TileSize` | `ExpirationType` | `ExpirationTime.Ticks` |
|---|---|---|---|---|---|---|---|
| `Meta.Cosmetic.DigitalWood.GGX17` | 5 | Meta.Cosmetic.DigitalWood | Id.Item.Glock17 | 0 | LARGE_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.DigitalWood.SportsParachute` | 15 | Meta.Cosmetic.DigitalWood | Id.Item.Parachute.Sport | 1 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.DigitalWood.SV98` | 10 | Meta.Cosmetic.DigitalWood | Id.Item.SV98 | 2 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.DigitalWood.M4` | 10 | Meta.Cosmetic.DigitalWood | Id.Item.M4 | 3 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.Bobcat` | 5 | Meta.Cosmetic.TwoToneDesert | Vehicle.Variant.Land.Wheeled.Bobcat.Default | 0 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.DuneBuggy` | 10 | Meta.Cosmetic.TwoToneDesert | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default | 1 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.Humvee` | 10 | Meta.Cosmetic.TwoToneDesert | Vehicle.Variant.Land.Wheeled.Humvee.Default | 2 | LARGE_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.Littlebird` | 15 | Meta.Cosmetic.TwoToneDesert | Vehicle.Variant.Air.Rotary.Littlebird.Default | 3 | LARGE_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.A91` | 5 | Meta.Cosmetic.TwoToneDesert | Id.Item.A91 | 5 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.KH2002` | 5 | Meta.Cosmetic.TwoToneDesert | Id.Item.KH2002 | 6 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.Bushmaster` | 5 | Meta.Cosmetic.TwoToneDesert | Id.Item.WEPN_033 | 11 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.M4` | 10 | Meta.Cosmetic.TwoToneDesert | Id.Item.M4 | 8 | LARGE_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.M249` | 15 | Meta.Cosmetic.TwoToneDesert | Id.Item.M249 | 9 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.AX50` | 15 | Meta.Cosmetic.TwoToneDesert | Id.Item.SR_04 | 10 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.MP9` | 10 | Meta.Cosmetic.TwoToneDesert | Id.Item.MP9 | 7 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.M500` | 10 | Meta.Cosmetic.TwoToneDesert | Id.Item.M500 | 12 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.Emote.Middle_Finger` | 5 | Meta.Cosmetic.Emote | Id.Emote.Middle_Finger | 0 | LARGE_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.Emote.RockPaperScissors` | 5 | Meta.Cosmetic.Emote | Id.Emote.RockPaperScissors | 1 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.Emote.Shh` | 5 | Meta.Cosmetic.Emote | Id.Emote.Shh | 2 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.BlackAndGold.Littlebird` | 30 | Meta.Cosmetic.BlackAndGold | Vehicle.Variant.Air.Rotary.Littlebird.Default | 1 | HERO_TILE | EXPIRATION_NO_END_TIME | 639342720000000000 |
| `Meta.Cosmetic.TwoToneDesert.Mosin` | 10 | Meta.Cosmetic.TwoToneDesert | Id.Item.Mosin | 13 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.Galil` | 10 | Meta.Cosmetic.TwoToneDesert | Id.Item.WEPN_029 | 14 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.TwoToneDesert.Havoc` | 15 | Meta.Cosmetic.TwoToneDesert | Vehicle.Variant.Air.Rotary.Havoc.Default | 15 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.DigitalWood.M500` | 10 | Meta.Cosmetic.DigitalWood | Id.Item.M500 | 4 | SMALL_SQUARE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.ChocolateChip.M14` | 10 | Meta.Cosmetic.ChocolateChip | Id.Item.WEPN_034 | 2 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.ChocolateChip.Evolys` | 10 | Meta.Cosmetic.ChocolateChip | Id.Item.WEPN_036 | 1 | SMALL_RECTANGLE | NO_EXPIRATION | 0 |
| `Meta.Cosmetic.ChocolateChip.TCXSPR` | 10 | Meta.Cosmetic.ChocolateChip | Id.Item.WEPN_037 | 0 | LARGE_RECTANGLE | NO_EXPIRATION | 0 |

Columns 8-8 of 8:

| Row | `Tag` |
|---|---|
| `Meta.Cosmetic.DigitalWood.GGX17` | Meta.Cosmetic.DigitalWood.GGX17 |
| `Meta.Cosmetic.DigitalWood.SportsParachute` | Meta.Cosmetic.DigitalWood.SportsParachute |
| `Meta.Cosmetic.DigitalWood.SV98` | Meta.Cosmetic.DigitalWood.SV98 |
| `Meta.Cosmetic.DigitalWood.M4` | Meta.Cosmetic.DigitalWood.M4 |
| `Meta.Cosmetic.TwoToneDesert.Bobcat` | Meta.Cosmetic.TwoToneDesert.Bobcat |
| `Meta.Cosmetic.TwoToneDesert.DuneBuggy` | Meta.Cosmetic.TwoToneDesert.DuneBuggy |
| `Meta.Cosmetic.TwoToneDesert.Humvee` | Meta.Cosmetic.TwoToneDesert.Humvee |
| `Meta.Cosmetic.TwoToneDesert.Littlebird` | Meta.Cosmetic.TwoToneDesert.Littlebird |
| `Meta.Cosmetic.TwoToneDesert.A91` | Meta.Cosmetic.TwoToneDesert.A91 |
| `Meta.Cosmetic.TwoToneDesert.KH2002` | Meta.Cosmetic.TwoToneDesert.KH2002 |
| `Meta.Cosmetic.TwoToneDesert.Bushmaster` | Meta.Cosmetic.TwoToneDesert.Bushmaster |
| `Meta.Cosmetic.TwoToneDesert.M4` | Meta.Cosmetic.TwoToneDesert.M4 |
| `Meta.Cosmetic.TwoToneDesert.M249` | Meta.Cosmetic.TwoToneDesert.M249 |
| `Meta.Cosmetic.TwoToneDesert.AX50` | Meta.Cosmetic.TwoToneDesert.AX50 |
| `Meta.Cosmetic.TwoToneDesert.MP9` | Meta.Cosmetic.TwoToneDesert.MP9 |
| `Meta.Cosmetic.TwoToneDesert.M500` | Meta.Cosmetic.TwoToneDesert.M500 |
| `Meta.Cosmetic.Emote.Middle_Finger` | Meta.Cosmetic.Emote.Middle_Finger |
| `Meta.Cosmetic.Emote.RockPaperScissors` | Meta.Cosmetic.Emote.RockPaperScissors |
| `Meta.Cosmetic.Emote.Shh` | Meta.Cosmetic.Emote.Shh |
| `Meta.Cosmetic.BlackAndGold.Littlebird` | Meta.Cosmetic.BlackAndGold.Littlebird |
| `Meta.Cosmetic.TwoToneDesert.Mosin` | Meta.Cosmetic.TwoToneDesert.Mosin |
| `Meta.Cosmetic.TwoToneDesert.Galil` | Meta.Cosmetic.TwoToneDesert.Galil |
| `Meta.Cosmetic.TwoToneDesert.Havoc` | Meta.Cosmetic.TwoToneDesert.Havoc |
| `Meta.Cosmetic.DigitalWood.M500` | Meta.Cosmetic.DigitalWood.M500 |
| `Meta.Cosmetic.ChocolateChip.M14` | Meta.Cosmetic.ChocolateChip.M14 |
| `Meta.Cosmetic.ChocolateChip.Evolys` | Meta.Cosmetic.ChocolateChip.Evolys |
| `Meta.Cosmetic.ChocolateChip.TCXSPR` | Meta.Cosmetic.ChocolateChip.TCXSPR |
<!-- /datatable_catalog -->

## WDExchangeDefinitionTableRow

Tables: [`DT_ExchangeDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDExchangeDefinitionTableRow -->
*1 table(s), 1 rows, 1 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Tag` |
|---|---|
| `Attribute.Meta.Currency.GoldBars` | Attribute.Meta.Currency.GoldBars |
<!-- /datatable_catalog -->

## WDMockInvestmentItemTableRow

Tables: [`DT_MockInvestments`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/MockInvestments/DT_MockInvestments.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDMockInvestmentItemTableRow -->
*1 table(s), 1 rows, 3 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `ActiveInvestmentIds` | `Investments` | `Tag` |
|---|---|---|---|
| `Meta.MockInvestment.Definitions` | Meta.MockInvestment.Bandage | {Key=Meta.MockInvestment.AK74M; Value.ItemEntryId=Id.Item.AK74M; Value.ItemQuantity=1; Value.CashCostAmount=1… | Meta.MockInvestment.Definitions |
<!-- /datatable_catalog -->

## WDFactoryRecipe

Tables: [`DT_Factory01_Recipes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01/Content/Data/DT_Factory01_Recipes.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDFactoryRecipe -->
*1 table(s), 6 rows, 5 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `RecipeDuration` | `ProductionDiscount` | `bOverrideProductionCost` | `ProductionCost` | `Tag` |
|---|---|---|---|---|---|
| `Id.Item.AK74M` | 10 | 20 | false | 640 | Id.Item.AK74M |
| `Id.Item.M4` | 10 | 20 | false | 2240 | Id.Item.M4 |
| `Id.Item.MP9` | 10 | 20 | false | 1100 | Id.Item.MP9 |
| `Id.Item.Vector` | 10 | 20 | false | 4480 | Id.Item.Vector |
| `Id.Item.4xElcanSpectr` | 10 | 20 | false | 640 | Id.Item.4xElcanSpectr |
| `Id.Item.EotechHoloSight` | 10 | 20 | false | 496 | Id.Item.EotechHoloSight |
<!-- /datatable_catalog -->

## WDWagerConditionDefinition

Tables: [`DT_WagerConditions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerConditions.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDWagerConditionDefinition -->
*1 table(s), 50 rows, 21 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 21:

| Row | `_aaaakgfoodihlgbfboeka` | `DisplayName` | `_aaaakoinngipbcijjmfcn` | `Description` | `_aaaaiogbmobfimjejhddd` | `Icon` | `Category` |
|---|---|---|---|---|---|---|---|
| `Wager.Condition.Naked` | false | No Spend |  | Spend no cash while the wager is live. | Not available once you have spent cash this life. |  | Wager.ConditionCategory.Rules |
| `Wager.Condition.Deathwish` | false | Deathwish |  | Test row: multiplies the odds only. No in-game rule is enforced yet. |  |  | Wager.ConditionCategory.Rules |
| `Wager.Condition.TimeLimit` | false | Time Limit |  | Every action must be completed within 60 seconds of placing the wager. | The clock starts when the wager is placed. |  | Wager.ConditionCategory.Rules |
| `Wager.Condition.NoVehicles` | false | No Vehicles |  | Test row: multiplies the odds only. No in-game rule is enforced yet. |  |  | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.NoResupply` | false | No Resupply |  | Test row: multiplies the odds only. No in-game rule is enforced yet. | Only available on a kills wager. |  | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.Kills.WithAK74` | true | With {Entity} | Id.Item.AK74M |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Kills.WithJudge` | true | With {Entity} | Id.Item.Judge |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Kills.WithScout` | true | With {Entity} | Id.Item.WEPN_035 |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Kills.WithGrenade` | false | With {Entity} | Id.Item.M67Grenade | Counts a kill only when you make it with a frag grenade. |  |  | Wager.ConditionCategory.Means.Utility |
| `Wager.Condition.Kills.WithPunch` | true | With {Entity} | Id.Item.Fists |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Kills.WithLargeHammer` | true | With {Entity} | ID.Item.BuildTool.Hammer.Large |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Kills.UsingHPAmmo` | true | Using HP Ammo |  | Counts a kill only when you make it with hollow-point ammo, tracer rounds included. |  | T_UI_WagerVendor_Icon_HPAmmo | Wager.ConditionCategory.Means.Weapon.Ammo |
| `Wager.Condition.Kills.UsingAPAmmo` | false | Using AP Ammo |  | Counts a kill only when you make it with armor-piercing ammo, tracer rounds included. |  | T_UI_WagerVendor_Icon_APAmmo | Wager.ConditionCategory.Means.Weapon.Ammo |
| `Wager.Condition.Kills.WithHeadshot` | true | With Headshot |  |  |  | T_UI_Killfeed_Headshot | Wager.ConditionCategory.Manner |
| `Wager.Condition.VehiclesDestroyed.Tank` | false | Tank Destroyed |  | Counts a destroyed vehicle only when it is an L2A6 or T-72B3 tank. |  | T_UI_Icon_Killfeed_TNK_01_Heavy | Wager.ConditionCategory.Target.Vehicle |
| `Wager.Condition.VehiclesDestroyed.Havoc` | false | {Entity} Destroyed | Vehicle.Variant.Air.Rotary.Havoc.Default |  |  |  | Wager.ConditionCategory.Target.Vehicle |
| `Wager.Condition.VehiclesDestroyed.Blackhawk` | false | {Entity} Destroyed | Vehicle.Variant.Air.Rotary.ROT_04.Default |  |  |  | Wager.ConditionCategory.Target.Vehicle |
| `Wager.Condition.VehiclesDestroyed.Artillery` | false | {Entity} Destroyed | Vehicle.Variant.Land.Tracked.TNK_01.Artillery |  |  |  | Wager.ConditionCategory.Target.Vehicle |
| `Wager.Condition.VehiclesDestroyed.RocketLittleBird` | false | {Entity} Destroyed | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |  |  |  | Wager.ConditionCategory.Target.Vehicle |
| `Wager.Condition.Revives.WithResus` | false | With Resus |  |  |  |  | Wager.ConditionCategory.Means.Utility |
| `Wager.Condition.Revives.WithDefib` | true | With {Entity} | Id.Item.Defibrillator.Standard |  |  | T_UI_Icon_DefibKill | Wager.ConditionCategory.Means.Utility |
| `Wager.Condition.Revives.WithMedkit` | true | With {Entity} | ID.Item.MedKit.Standard |  |  | T_UI_Icon_Role_Medic | Wager.ConditionCategory.Means.Utility |
| `Wager.Condition.PlayerDelivery.ToControlZone` | false | To Control Zone |  | Counts a delivery only when the player you deliver is inside a control zone. |  | T_UI_WagerVendor_Icon_CZ | Wager.ConditionCategory.Place |
| `Wager.Condition.PlayerDelivery.ToHotzone` | true | To Hotzone |  | Counts a delivery only when the player you deliver is inside the hotzone. |  | T_UI_WagerVendor_Icon_HZ | Wager.ConditionCategory.Place |
| `Wager.Condition.PlayerDelivery.InAirVehicle` | false | In Air Vehicle |  |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InGroundVehicle` | false | In Ground Vehicle |  |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InLittleBird` | false | In {Entity} | Vehicle.Variant.Air.Rotary.Littlebird.Default |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InBlackhawk` | false | In {Entity} | Vehicle.Variant.Air.Rotary.ROT_04.Default |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InKodiak` | false | In {Entity} | Vehicle.Variant.Land.Wheeled.Kodiak.Default |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InDuneBuggy` | true | In {Entity} | Vehicle.Variant.Land.Wheeled.DuneBuggy.Default |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InBobcat` | true | In {Entity} | Vehicle.Variant.Land.Wheeled.Bobcat.Default |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.PlayerDelivery.InUral` | true | In {Entity} | Vehicle.Variant.Land.Wheeled.Ural.Default |  |  |  | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.Kills.WithVehicleImpact` | true | With Vehicle Impact |  | Counts a kill only when you make it by ramming someone with a vehicle. |  | T_UI_WagerVendor_Icon_VehicleImpact | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Kills.OnlyOneMag` | true | With Only 1 Mag |  | Counts a kill only while you carry no magazine besides the ones loaded in your weapons. |  | T_UI_WagerVendor_Icon_OneMag | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.VehiclesDestroyed.WithTank` | false | With Tank |  | Counts a destroyed vehicle only while you are seated in an L2A6 or T-72B3 tank. |  | T_UI_Icon_Killfeed_TNK_01_Heavy | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.VehiclesDestroyed.WithHavoc` | false | With {Entity} | Vehicle.Variant.Air.Rotary.Havoc.Default |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.VehiclesDestroyed.WithRocketLittleBird` | false | With {Entity} | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.VehiclesDestroyed.Above50Kph` | true | While Moving Above 50 kph |  | Counts a destroyed vehicle only while you are moving faster than 50 kph. |  | T_UI_WagerVendor_Icon_50kph | Wager.ConditionCategory.Manner |
| `Wager.Condition.Revives.FarFromTeammates` | true | 50 m From Teammates |  | Counts a revive only while your nearest living teammate, other than the player you revive, is at least 50 m a… |  | T_UI_WagerVendor_Icon_50m | Wager.ConditionCategory.Place.Proximity |
| `Wager.Condition.Revives.NoWeapons` | true | With No Weapons |  | Counts a revive only while you carry no weapons. |  | T_UI_WagerVendor_Icon_NoWeapons | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.PlayerDelivery.FiveTapes` | true | With 5 Tapes in the Vehicle |  | Counts a delivery only while the vehicle you are in holds at least five tapes. |  | T_UI_WagerVendor_Icon_Tapes | Wager.ConditionCategory.Means.Vehicle |
| `Wager.Condition.InControlZone` | false | In Control Zone |  | Counts only while you are inside a control zone. |  | T_UI_WagerVendor_Icon_CZ | Wager.ConditionCategory.Place |
| `Wager.Condition.InHotzone` | true | In Hotzone |  | Counts only while you are inside the hotzone. |  | T_UI_WagerVendor_Icon_HZ | Wager.ConditionCategory.Place |
| `Wager.Condition.NoArmor` | true | While Wearing No Armor |  | Counts only while you wear no helmet or body armor. |  | T_UI_WagerVendor_Icon_NoArmor | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.Loadout20k` | true | With a $20k Loadout |  | Counts only while your loadout is worth at least $20,000. |  | T_UI_WagerVendor_Icon_20KLoadout | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.NoBandages` | true | With No Bandages |  | Counts only while you carry no bandages. |  | T_UI_WagerVendor_Icon_NoBandages | Wager.ConditionCategory.Self.Loadout |
| `Wager.Condition.Under50HP` | true | While Under 50 HP |  | Counts only while you have under 50 health. |  | T_UI_WagerVendor_Icon_50Health | Wager.ConditionCategory.Self.Condition |
| `Wager.Condition.Kills.WithSmallHammer` | true | With {Entity} | ID.Item.BuildTool.Hammer.Small |  |  |  | Wager.ConditionCategory.Means.Weapon |
| `Wager.Condition.Revives.MagicHands` | true | With Magic Hands |  | Counts a revive only when you make it by hand, without a revive item. |  |  | Wager.ConditionCategory.Means.Utility |
| `Wager.Condition.Kills.WithLightDrill` | true | With {Entity} | ID.Item.RepairTool.Drill.Light |  |  |  | Wager.ConditionCategory.Means.Weapon |

Columns 8-14 of 21:

| Row | `Odds` | `TraitTags` | `IncompatibleTraitTags` | `RequiresAnyActionTags` | `_aaabbldhaebiklpgijlkp` | `_aaaalachhfgpfehmdofie.QueryDefinition.StaticStruct.SchemaClass` | `_aaaalachhfgpfehmdofie.QueryDefinition.SharedDefinition.Conditions.Structs` |
|---|---|---|---|---|---|---|---|
| `Wager.Condition.Naked` | 1.1 | Wager.ConditionTrait.Spend |  |  |  | WDMetaPrerequisiteSchema | {StatTag=Analytics.Player.Cash.Spent.CurrentLife; Comparison=Equal; Value=0; bInvert=false; Operator=Copy; Ne… |
| `Wager.Condition.Deathwish` | 10 | Wager.ConditionTrait.Public | Wager.ConditionTrait.Spend |  |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.TimeLimit` | 4 | Wager.ConditionTrait.Time |  |  |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.NoVehicles` | 3 |  |  |  |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.NoResupply` | 2 |  |  | Wager.Action.Kills |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithAK74` | 1.01 | Wager.ConditionTrait.Weapon | Wager.ConditionTrait.Weapon | Wager.Action.Kills | Id.Item.AK74M | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithJudge` | 1.3 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Mag | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Mag | Wager.Action.Kills | Id.Item.Judge | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithScout` | 1.05 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Mag | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Mag | Wager.Action.Kills | Id.Item.WEPN_035 | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithGrenade` | 1.45 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.Action.Kills | Id.Item.M67Grenade | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithPunch` | 1.4 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.Action.Kills | Id.Item.Fists | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithLargeHammer` | 1.3 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.Action.Kills | ID.Item.BuildTool.Hammer.Large | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.UsingHPAmmo` | 1.15 | Wager.ConditionTrait.Ammo | Wager.ConditionTrait.Ammo | Wager.Action.Kills | Meta.Damage.AmmoModifier.HollowPoint | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.UsingAPAmmo` | 1.1 | Wager.ConditionTrait.Ammo | Wager.ConditionTrait.Ammo | Wager.Action.Kills | Meta.Damage.AmmoModifier.ArmorPiercing | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithHeadshot` | 1.2 | Wager.ConditionTrait.Headshot | Wager.ConditionTrait.Headshot | Wager.Action.Kills | Challenges.Context.Headshot | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.Tank` | 1.6 | Wager.ConditionTrait.Target | Wager.ConditionTrait.Target | Wager.Action.VehiclesDestroyed | Vehicle.Variant.Land.Tracked.TNK_01.Heavy, Vehicle.Variant.Land.Tracked.TNK_04 | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.Havoc` | 1.7 | Wager.ConditionTrait.Target | Wager.ConditionTrait.Target | Wager.Action.VehiclesDestroyed | Vehicle.Variant.Air.Rotary.Havoc | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.Blackhawk` | 1.5 | Wager.ConditionTrait.Target | Wager.ConditionTrait.Target | Wager.Action.VehiclesDestroyed | Vehicle.Variant.Air.Rotary.ROT_04 | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.Artillery` | 1.4 | Wager.ConditionTrait.Target | Wager.ConditionTrait.Target | Wager.Action.VehiclesDestroyed | Vehicle.Variant.Land.Tracked.TNK_01.Artillery | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.RocketLittleBird` | 1.45 | Wager.ConditionTrait.Target | Wager.ConditionTrait.Target | Wager.Action.VehiclesDestroyed | Vehicle.Variant.Air.Rotary.Littlebird.RocketPods | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Revives.WithResus` | 1.1 | Wager.ConditionTrait.Item | Wager.ConditionTrait.Item | Wager.Action.Revives | Id.Item.Resuscitator | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Revives.WithDefib` | 1.025 | Wager.ConditionTrait.Item | Wager.ConditionTrait.Item | Wager.Action.Revives | Id.Item.Defibrillator | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Revives.WithMedkit` | 1.05 | Wager.ConditionTrait.Item | Wager.ConditionTrait.Item | Wager.Action.Revives | Id.Item.MedKit | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.ToControlZone` | 1.15 | Wager.ConditionTrait.Location | Wager.ConditionTrait.Location | Wager.Action.PlayerDelivery | Challenges.Context.Target.InControlZone | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.ToHotzone` | 1.25 | Wager.ConditionTrait.Location | Wager.ConditionTrait.Location | Wager.Action.PlayerDelivery | Challenges.Context.Target.InHotZone | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InAirVehicle` | 1.1 | Wager.ConditionTrait.Vehicle | Wager.ConditionTrait.Vehicle | Wager.Action.PlayerDelivery | Vehicle.Variant.Air | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InGroundVehicle` | 1.05 | Wager.ConditionTrait.Vehicle | Wager.ConditionTrait.Vehicle | Wager.Action.PlayerDelivery | Vehicle.Variant.Land | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InLittleBird` | 1.2 | Wager.ConditionTrait.Vehicle | Wager.ConditionTrait.Vehicle | Wager.Action.PlayerDelivery | Vehicle.Variant.Air.Rotary.Littlebird | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InBlackhawk` | 1.15 | Wager.ConditionTrait.Vehicle | Wager.ConditionTrait.Vehicle | Wager.Action.PlayerDelivery | Vehicle.Variant.Air.Rotary.ROT_04 | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InKodiak` | 1.15 | Wager.ConditionTrait.Vehicle | Wager.ConditionTrait.Vehicle | Wager.Action.PlayerDelivery | Vehicle.Variant.Land.Wheeled.Kodiak | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InDuneBuggy` | 1.025 | Wager.ConditionTrait.Vehicle, Wager.ConditionTrait.Tapes | Wager.ConditionTrait.Vehicle, Wager.ConditionTrait.Tapes | Wager.Action.PlayerDelivery | Vehicle.Variant.Land.Wheeled.DuneBuggy | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InBobcat` | 1.2 | Wager.ConditionTrait.Vehicle, Wager.ConditionTrait.Tapes | Wager.ConditionTrait.Vehicle, Wager.ConditionTrait.Tapes | Wager.Action.PlayerDelivery | Vehicle.Variant.Land.Wheeled.Bobcat | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.InUral` | 1.01 | Wager.ConditionTrait.Vehicle | Wager.ConditionTrait.Vehicle | Wager.Action.PlayerDelivery | Vehicle.Variant.Land.Wheeled.Ural | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithVehicleImpact` | 1.075 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.Action.Kills |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.OnlyOneMag` | 1.2 | Wager.ConditionTrait.Mag | Wager.ConditionTrait.Mag | Wager.Action.Kills |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.WithTank` | 1.1 | Wager.ConditionTrait.Weapon | Wager.ConditionTrait.Weapon | Wager.Action.VehiclesDestroyed |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.WithHavoc` | 1.15 | Wager.ConditionTrait.Weapon | Wager.ConditionTrait.Weapon | Wager.Action.VehiclesDestroyed |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.WithRocketLittleBird` | 1.15 | Wager.ConditionTrait.Weapon | Wager.ConditionTrait.Weapon | Wager.Action.VehiclesDestroyed |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.VehiclesDestroyed.Above50Kph` | 1.1 |  |  | Wager.Action.VehiclesDestroyed |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Revives.FarFromTeammates` | 1.1 |  |  | Wager.Action.Revives |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Revives.NoWeapons` | 1.15 | Wager.ConditionTrait.Loadout | Wager.ConditionTrait.Loadout | Wager.Action.Revives |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.PlayerDelivery.FiveTapes` | 1.005 | Wager.ConditionTrait.Tapes | Wager.ConditionTrait.Tapes | Wager.Action.PlayerDelivery |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.InControlZone` | 1.15 | Wager.ConditionTrait.Location | Wager.ConditionTrait.Location | Wager.Action.Kills, Wager.Action.Revives, Wager.Action.VehiclesDestroyed | Challenges.Context.Instigator.InControlZone | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.InHotzone` | 1.1 | Wager.ConditionTrait.Location | Wager.ConditionTrait.Location | Wager.Action.Kills, Wager.Action.Revives, Wager.Action.VehiclesDestroyed | Challenges.Context.Instigator.InHotZone | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.NoArmor` | 1.15 |  |  | Wager.Action.Kills, Wager.Action.Revives |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Loadout20k` | 1.05 | Wager.ConditionTrait.Loadout | Wager.ConditionTrait.Loadout | Wager.Action.Kills, Wager.Action.Revives, Wager.Action.VehiclesDestroyed |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.NoBandages` | 1.15 |  |  | Wager.Action.Kills, Wager.Action.Revives |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Under50HP` | 1.2 |  |  | Wager.Action.Kills, Wager.Action.Revives |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithSmallHammer` | 1.3 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.Action.Kills | ID.Item.BuildTool.Hammer.Small | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Revives.MagicHands` | 1.1 | Wager.ConditionTrait.Item | Wager.ConditionTrait.Item | Wager.Action.Revives |  | WDMetaPrerequisiteSchema |  |
| `Wager.Condition.Kills.WithLightDrill` | 1.3 | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag | Wager.ConditionTrait.Weapon, Wager.ConditionTrait.Ammo, Wager.ConditionTrait.Mag, Wager.ConditionTrait.Headsh… | Wager.Action.Kills | ID.Item.RepairTool.Drill.Light | WDMetaPrerequisiteSchema |  |

Columns 15-21 of 21:

| Row | `_aaaalachhfgpfehmdofie.QueryDefinition.SharedDefinition.SchemaClass` | `MinValue` | `MaxValue` | `ValueStep` | `CooldownSeconds` | `Behaviors` | `Tag` |
|---|---|---|---|---|---|---|---|
| `Wager.Condition.Naked` | WDMetaPrerequisiteSchema | 0 | 0 | 1 | 86400 | {ResourceTag=Attribute.Meta.Currency.Cash; _aaaapofmpjejiiekikojo=Meta.Progression.Resources.MatchScore.Purch… | Wager.Condition.Naked |
| `Wager.Condition.Deathwish` |  | 0 | 0 | 1 | 86400 | {} | Wager.Condition.Deathwish |
| `Wager.Condition.TimeLimit` |  | 0 | 0 | 1 | 86400 | {Seconds=60; _aaaaikkaafbipeiknogeo=Wager.Timer.FailAfterSeconds; FailReason=Wager.FailReason.TimedOut; _aaaa… | Wager.Condition.TimeLimit |
| `Wager.Condition.NoVehicles` |  | 0 | 0 | 1 | 86400 | {} | Wager.Condition.NoVehicles |
| `Wager.Condition.NoResupply` |  | 0 | 0 | 1 | 86400 | {} | Wager.Condition.NoResupply |
| `Wager.Condition.Kills.WithAK74` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithAK74 |
| `Wager.Condition.Kills.WithJudge` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithJudge |
| `Wager.Condition.Kills.WithScout` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithScout |
| `Wager.Condition.Kills.WithGrenade` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithGrenade |
| `Wager.Condition.Kills.WithPunch` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithPunch |
| `Wager.Condition.Kills.WithLargeHammer` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithLargeHammer |
| `Wager.Condition.Kills.UsingHPAmmo` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.UsingHPAmmo |
| `Wager.Condition.Kills.UsingAPAmmo` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.UsingAPAmmo |
| `Wager.Condition.Kills.WithHeadshot` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithHeadshot |
| `Wager.Condition.VehiclesDestroyed.Tank` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.VehiclesDestroyed.Tank |
| `Wager.Condition.VehiclesDestroyed.Havoc` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.VehiclesDestroyed.Havoc |
| `Wager.Condition.VehiclesDestroyed.Blackhawk` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.VehiclesDestroyed.Blackhawk |
| `Wager.Condition.VehiclesDestroyed.Artillery` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.VehiclesDestroyed.Artillery |
| `Wager.Condition.VehiclesDestroyed.RocketLittleBird` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.VehiclesDestroyed.RocketLittleBird |
| `Wager.Condition.Revives.WithResus` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Revives.WithResus |
| `Wager.Condition.Revives.WithDefib` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Revives.WithDefib |
| `Wager.Condition.Revives.WithMedkit` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Revives.WithMedkit |
| `Wager.Condition.PlayerDelivery.ToControlZone` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.ToControlZone |
| `Wager.Condition.PlayerDelivery.ToHotzone` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.ToHotzone |
| `Wager.Condition.PlayerDelivery.InAirVehicle` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InAirVehicle |
| `Wager.Condition.PlayerDelivery.InGroundVehicle` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InGroundVehicle |
| `Wager.Condition.PlayerDelivery.InLittleBird` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InLittleBird |
| `Wager.Condition.PlayerDelivery.InBlackhawk` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InBlackhawk |
| `Wager.Condition.PlayerDelivery.InKodiak` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InKodiak |
| `Wager.Condition.PlayerDelivery.InDuneBuggy` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InDuneBuggy |
| `Wager.Condition.PlayerDelivery.InBobcat` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InBobcat |
| `Wager.Condition.PlayerDelivery.InUral` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.PlayerDelivery.InUral |
| `Wager.Condition.Kills.WithVehicleImpact` |  | 0 | 0 | 1 | 86400 | {_aaaakfdimkkalchjcbedi=Meta.Damage.DamageType.Impact; _aaaalomlnknmafbflkiin=Meta.Damage.Kinetic.Impact.Thro… | Wager.Condition.Kills.WithVehicleImpact |
| `Wager.Condition.Kills.OnlyOneMag` |  | 0 | 0 | 1 | 86400 | {_aaaakajebecbokbemgoha.SupportFilter=AllowList; _aaaakajebecbokbemgoha.AllowedSubSlotContext=Item.Attachment… | Wager.Condition.Kills.OnlyOneMag |
| `Wager.Condition.VehiclesDestroyed.WithTank` |  | 0 | 0 | 1 | 86400 | {VehicleTags=Vehicle.Variant.Land.Tracked.TNK_01.Heavy, Vehicle.Variant.Land.Tracked.TNK_04; _aaaalndmlkdbdge… | Wager.Condition.VehiclesDestroyed.WithTank |
| `Wager.Condition.VehiclesDestroyed.WithHavoc` |  | 0 | 0 | 1 | 86400 | {VehicleTags=Vehicle.Variant.Air.Rotary.Havoc; _aaaalndmlkdbdgenbhaek=Wager.Behavior.RequireInVehicle} | Wager.Condition.VehiclesDestroyed.WithHavoc |
| `Wager.Condition.VehiclesDestroyed.WithRocketLittleBird` |  | 0 | 0 | 1 | 86400 | {VehicleTags=Vehicle.Variant.Air.Rotary.Littlebird.RocketPods; _aaaalndmlkdbdgenbhaek=Wager.Behavior.RequireI… | Wager.Condition.VehiclesDestroyed.WithRocketLittleBird |
| `Wager.Condition.VehiclesDestroyed.Above50Kph` |  | 0 | 0 | 1 | 86400 | {_aaaainbclocjcedlpfcmo=50; _aaaalndmlkdbdgenbhaek=Wager.Behavior.RequireOwnerSpeed} | Wager.Condition.VehiclesDestroyed.Above50Kph |
| `Wager.Condition.Revives.FarFromTeammates` |  | 0 | 0 | 1 | 86400 | {_aaaanhbbfgbimifphhckm=50; _aaaalndmlkdbdgenbhaek=Wager.Behavior.RequireTeammateDistance} | Wager.Condition.Revives.FarFromTeammates |
| `Wager.Condition.Revives.NoWeapons` |  | 0 | 0 | 1 | 86400 | {_aaaakajebecbokbemgoha.SupportFilter=AllowList; _aaaakajebecbokbemgoha.AllowedSubSlotContext=Item.Weapon; _a… | Wager.Condition.Revives.NoWeapons |
| `Wager.Condition.PlayerDelivery.FiveTapes` |  | 0 | 0 | 1 | 86400 | {_aaaakajebecbokbemgoha.SupportFilter=AllowList; _aaaakajebecbokbemgoha.AllowedSubSlotContext=Item.Context.Ve… | Wager.Condition.PlayerDelivery.FiveTapes |
| `Wager.Condition.InControlZone` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.InControlZone |
| `Wager.Condition.InHotzone` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.InHotzone |
| `Wager.Condition.NoArmor` |  | 0 | 0 | 1 | 86400 | {_aaaakajebecbokbemgoha.SupportFilter=AllowList; _aaaakajebecbokbemgoha.AllowedSubSlotContext=Inventory.Slot.… | Wager.Condition.NoArmor |
| `Wager.Condition.Loadout20k` |  | 0 | 0 | 1 | 86400 | {_aaaahnbbjmhmofgmjogdb=20000; _aaaalndmlkdbdgenbhaek=Wager.Behavior.RequireLoadoutCost} | Wager.Condition.Loadout20k |
| `Wager.Condition.NoBandages` |  | 0 | 0 | 1 | 86400 | {_aaaakajebecbokbemgoha.SupportFilter=AllowList; _aaaakajebecbokbemgoha.AllowedSubSlotItems=Id.Item.Bandage, … | Wager.Condition.NoBandages |
| `Wager.Condition.Under50HP` |  | 0 | 0 | 1 | 86400 | {_aaaalehghdhdnmhfiaehk=50; _aaaalndmlkdbdgenbhaek=Wager.Behavior.RequireOwnerHealth} | Wager.Condition.Under50HP |
| `Wager.Condition.Kills.WithSmallHammer` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithSmallHammer |
| `Wager.Condition.Revives.MagicHands` |  | 0 | 0 | 1 | 86400 | {_aaaakfdimkkalchjcbedi=Challenges.Context.Instigator; _aaaalomlnknmafbflkiin=Id.Item; _aaaalndmlkdbdgenbhaek… | Wager.Condition.Revives.MagicHands |
| `Wager.Condition.Kills.WithLightDrill` |  | 0 | 0 | 1 | 86400 |  | Wager.Condition.Kills.WithLightDrill |
<!-- /datatable_catalog -->

## WDWagerActionDefinition

Tables: [`DT_WagerActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerActions.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDWagerActionDefinition -->
*1 table(s), 4 rows, 16 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 16:

| Row | `_aaaakgfoodihlgbfboeka` | `DisplayName` | `ShortName` | `Description` | `Icon` | `Archetype` | `ChallengeId` |
|---|---|---|---|---|---|---|---|
| `Wager.Action.Kills` | true | Get {Count} Kills | Kills | Get this amount of kills. | T_UI_Killfeed_KillConfirmed | Wager.Archetype.Kills | Challenges.Challenge.Wager.Kills |
| `Wager.Action.PlayerDelivery` | true | Deliver {Count} people to the Control Zone | Players Delivered | Get this amount of players delivered to the Control Zone | t_ui_centrefeed_dropoff | Wager.Archetype.PlayersDelivered | Challenges.Challenge.Wager.PlayerDelivery |
| `Wager.Action.Revives` | true | Revive {Count} Teammates | Revives | Revive this many teammates. | T_UI_Killfeed_Revive | Wager.Archetype.Revives | Challenges.Challenge.Wager.Revives |
| `Wager.Action.VehiclesDestroyed` | true | Destroy {Count} Occupied Vehicles | Vehicles Destroyed | Destroy this many vehicles that have an enemy occupant. | T_UI_Icon_Killfeed_Explosion | Wager.Archetype.VehiclesDestroyed | Challenges.Challenge.Wager.VehiclesDestroyed |

Columns 8-14 of 16:

| Row | `_aaabcjojpnjmnbelecidg` | `MinCount` | `MaxCount` | `DefaultCount` | `Odds` | `Rules` | `PayoutResourceTag` |
|---|---|---|---|---|---|---|---|
| `Wager.Action.Kills` | NumPlayersToKill | 1 | 25 | 1 | 1.001, 1.001, 1.001, 1.0055, 1.01, 1.0179 (+19 more) | You must be inside the control zone, Enemy players only, Not a player an enemy revived, Repeats on the same p… | Attribute.Meta.Currency.Cash |
| `Wager.Action.PlayerDelivery` | NumPassengersToDeliver | 1 | 20 | 1 | 1.001, 1.001, 1.001, 1.001, 1.001, 1.0058 (+14 more) | Spawn vehicles don't count, Counts once your passenger survives the drop-off | Attribute.Meta.Currency.Cash |
| `Wager.Action.Revives` | NumPlayersToRevive | 1 | 50 | 5 | 1.001, 1.001, 1.001, 1.001, 1.001, 1.0058 (+44 more) | You must be inside the control zone, Teammates only, Not a player downed by a teammate or by themselves, Repe… | Attribute.Meta.Currency.Cash |
| `Wager.Action.VehiclesDestroyed` | NumVehiclesToDestroy | 1 | 20 | 1 | 1.001, 1.001, 1.001, 1.0055, 1.01, 1.0179 (+14 more) | An enemy must be driving it, An enemy must have bought it | Attribute.Meta.Currency.Cash |

Columns 15-16 of 16:

| Row | `CooldownSeconds` | `Tag` |
|---|---|---|
| `Wager.Action.Kills` | 86400 | Wager.Action.Kills |
| `Wager.Action.PlayerDelivery` | 86400 | Wager.Action.PlayerDelivery |
| `Wager.Action.Revives` | 86400 | Wager.Action.Revives |
| `Wager.Action.VehiclesDestroyed` | 86400 | Wager.Action.VehiclesDestroyed |
<!-- /datatable_catalog -->

## WDWagerObjectiveCatalogDefinition

Tables: [`DT_WagerObjectiveCatalog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerObjectiveCatalog.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDWagerObjectiveCatalogDefinition -->
*1 table(s), 1 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Objectives` | `Tag` |
|---|---|---|
| `Wager.ObjectiveCatalog` | {ID=Kills3; _aaaakgfoodihlgbfboeka=false; ActionId=Wager.Action.Kills; Count=3; Odds=1.001; CooldownSeconds=0… | Wager.ObjectiveCatalog |
<!-- /datatable_catalog -->

## WDWagerPricingDefinition

Tables: [`DT_WagerPricing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerPricing.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDWagerPricingDefinition -->
*1 table(s), 1 rows, 11 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 11:

| Row | `Pricing._aaaaneeiimhdoagdnepon` | `Pricing._aaaanhjhmeoeolaclenmp` | `Pricing.FoldBonusStep` | `Pricing.MaxPayout` | `Pricing.LivesOdds` | `MinStake` | `MaxStake` |
|---|---|---|---|---|---|---|---|
| `Wager.Pricing` | 1.001 | 100 | 0.25 | 5000000 | 1.009, 1.003, 1.002, 1.001 | 2500 | 100000 |

Columns 8-11 of 11:

| Row | `_aaabdmginceanljpngccf` | `_aaabappeahnblfboghmcb` | `_aaabdfkjenifhpkjaffkh` | `Tag` |
|---|---|---|---|---|
| `Wager.Pricing` | false | false | false | Wager.Pricing |
<!-- /datatable_catalog -->

## WDLootableDataTable

Tables: [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json), [`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDLootableDataTable -->
*2 table(s), 54 rows, 11 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 11:

| Table | Row | `LootableData.ItemsToSpawn` | `LootableData.SpawnChance` | `LootableData.bSpawnByDefault` | `LootableData.bSpawnByPoints` | `LootableData.InitialSpawnTime` | `LootableData.InitialSpawnPoints` | `LootableData.bCanRespawn` |
|---|---|---|---|---|---|---|---|---|
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Test` | {ItemTag=Id.Item.SV98; SubItemsSpawnData={SubItemTag=Id.Item.SniperScope10x; SubSpawnChance=100; SubItemAmoun… | 100 | true | true | 0 | 15 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Tower` | {ItemTag=Id.Item.SV98; SubItemsSpawnData={SubItemTag=Id.Item.SniperScope10x; SubSpawnChance=100; SubItemAmoun… | 50 | false | true | 0 | 10 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AbandonedTower` | {ItemTag=Id.Item.Bandage; SubItemsSpawnData={SubItemTag=Id.Item.M67Grenade; SubSpawnChance=100; SubItemAmount… | 50 | false | true | 0 | 10 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bandage` | {ItemTag=Id.Item.Bandage; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | true | 0 | 15 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Weapon` | {ItemTag=Id.Item.AK74M; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | true | 0 | 15 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Helmet` | {ItemTag=Id.Item.LightHelmet; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | true | 0 | 15 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Armor` | {ItemTag=Id.Item.LightArmor; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | true | 0 | 15 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Defib.Cheap` | {ItemTag=Id.Item.Defibrillator.Cheap; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | true | 0 | 15 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Sniper` | {ItemTag=Id.Item.Mosin; SubItemsSpawnData={SubItemTag=ID.Item.RangeFinder; SubSpawnChance=100; SubItemAmount=… | 100 | true | true | 0 | 15 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SniperOnly.HighValue` | {ItemTag=Id.Item.Mosin; SubItemsSpawnData={SubItemTag=Id.Item.4xElcanSpectr; SubSpawnChance=100; SubItemAmoun… | 25 | false | false | 30 | 15 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SniperOnly.MiddleValue` | {ItemTag=Id.Item.Mosin; SubItemsSpawnData={SubItemTag=Id.Item.4xElcanSpectr; SubSpawnChance=100; SubItemAmoun… | 25 | true | false | 10 | 15 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SniperOnly.LowValue` | {ItemTag=Id.Item.Mosin; SubItemsSpawnData={SubItemTag=Id.Item.4xElcanSpectr; SubSpawnChance=100; SubItemAmoun… | 20 | true | false | 10 | 15 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.PreLobby` | {ItemTag=Id.Item.Glock17; ItemAmount=1; ItemSpawnWeight=1}, {ItemTag=Id.Item.Judge; ItemAmount=1; ItemSpawnWe… | 100 | true | true | 0 | 15 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AK74` | {ItemTag=Id.Item.AK74M; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AR15` | {ItemTag=Id.Item.M4; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.KH2002` | {ItemTag=Id.Item.KH2002; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.A91` | {ItemTag=Id.Item.A91; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.TAR21` | {ItemTag=Id.Item.TAR21; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Vector` | {ItemTag=Id.Item.Vector; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SKS` | {ItemTag=Id.Item.SKS; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SV98` | {ItemTag=Id.Item.SV98; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M249` | {ItemTag=Id.Item.M249; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Glock17` | {ItemTag=Id.Item.Glock17; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M500` | {ItemTag=Id.Item.M500; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MMGL` | {ItemTag=Id.Item.MMGL; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.CGM4` | {ItemTag=Id.Item.CGM4; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MP9` | {ItemTag=Id.Item.MP9; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SVDM` | {ItemTag=Id.Item.SVDM; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.RFB` | {ItemTag=Id.Item.RFB; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Mosin` | {ItemTag=Id.Item.Mosin; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MK22` | {ItemTag=Id.Item.MK22; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.PKM` | {ItemTag=ID.Item.LMG_01_BRL_06; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Judge` | {ItemTag=Id.Item.Judge; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MP43` | {ItemTag=Id.Item.MP43; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.RPG` | {ItemTag=Id.Item.RPG7; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.PP19` | {ItemTag=Id.Item.WEPN_023; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AX50` | {ItemTag=Id.Item.SR_04; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Verba` | {ItemTag=Id.Item.Launcher_04; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M1911` | {ItemTag=Id.Item.WEPN_026; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Deagle` | {ItemTag=Id.Item.WEPN_027; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MP5` | {ItemTag=Id.Item.WEPN_028; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Galil` | {ItemTag=Id.Item.WEPN_029; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.FAL` | {ItemTag=Id.Item.WEPN_030; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Glock18` | {ItemTag=Id.Item.WEPN_032; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bushmaster` | {ItemTag=Id.Item.WEPN_033; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M14` | {ItemTag=Id.Item.WEPN_034; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Scout` | {ItemTag=Id.Item.WEPN_035; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Evolys` | {ItemTag=Id.Item.WEPN_036; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SigSpear` | {ItemTag=Id.Item.WEPN_037; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bow` | {ItemTag=Id.Item.CombatBow; SubItemsSpawnData={SubItemTag=Id.Item.Arrow; SubSpawnChance=100; SubItemAmount=10… | 100 | true | false | 0 | 0 | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M4` | {ItemTag=Id.Item.M4; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bag` | {ItemTag=Id.Item.BPAK_007; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | false |
| [`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json) | `Lootable.VIPEscort01.Fuelcan100` | {ItemTag=Id.Item.FuelCan; ItemAmount=1; ItemSpawnWeight=1} | 100 | true | false | 0 | 0 | false |
| [`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json) | `Lootable.VIPEscort01.AK` | {ItemTag=Id.Item.SV98; SubItemsSpawnData={SubItemTag=Id.Item.SV98Magazine; SubSpawnChance=100; SubItemAmount=… | 100 | true | true | 0 | 15 | true |

Columns 8-11 of 11:

| Table | Row | `LootableData.RespawnTime` | `LootableData.bNeverSelectPreviousItem` | `bSpawnInsideControlZoneOnly` | `_aaabeefoaikdjpkadlplk` |
|---|---|---|---|---|---|
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Test` | 1 | true | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Tower` | 300 | true | true | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AbandonedTower` | 300 | true | true | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bandage` | 10 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Weapon` | 10 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Helmet` | 10 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Armor` | 10 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Defib.Cheap` | 10 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Sniper` | 10 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SniperOnly.HighValue` | 60 | true | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SniperOnly.MiddleValue` | 20 | true | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SniperOnly.LowValue` | 20 | true | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.PreLobby` | 180 | true | false | true |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AK74` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AR15` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.KH2002` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.A91` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.TAR21` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Vector` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SKS` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SV98` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M249` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Glock17` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M500` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MMGL` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.CGM4` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MP9` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SVDM` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.RFB` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Mosin` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MK22` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.PKM` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Judge` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MP43` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.RPG` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.PP19` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.AX50` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Verba` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M1911` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Deagle` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.MP5` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Galil` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.FAL` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Glock18` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bushmaster` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M14` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Scout` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Evolys` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.SigSpear` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bow` | 1 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.M4` | 0 | false | false | false |
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | `Lootable.Bag` | 0 | false | false | false |
| [`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json) | `Lootable.VIPEscort01.Fuelcan100` | 0 | false | false | false |
| [`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json) | `Lootable.VIPEscort01.AK` | 10 | false | false | false |
<!-- /datatable_catalog -->

## WDControlZoneContributionModifierTableRow

Tables: [`DT_ControlZoneContributionModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Data/DT_ControlZoneContributionModifiers.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDControlZoneContributionModifierTableRow -->
*1 table(s), 3 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `ModifierTag` | `Multiplier` |
|---|---|---|
| `Alive` | State.Player.Vitality.Alive | 1 |
| `Critical` | State.Player.Vitality.Critical | 0 |
| `Dead` | State.Player.Vitality.Dead | 0 |
<!-- /datatable_catalog -->

## WDMissionDefinition

Tables: [`DT_PassiveMissions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissions.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDMissionDefinition -->
*1 table(s), 3 rows, 4 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `UnlockPrerequisite.QueryDefinition.StaticStruct.SchemaClass` | `Challenges` | `DifficultyWeight` | `Tag` |
|---|---|---|---|---|
| `Mission.Passive.EarnCash` | WDMetaPrerequisiteSchema | Challenges.Challenge.Mission.Passive.EarnCash.1, Challenges.Challenge.Mission.Passive.EarnCash.2, Challenges.… | 1 | Mission.Passive.EarnCash |
| `Mission.Passive.EarnAnyRoleXp` | WDMetaPrerequisiteSchema | Challenges.Challenge.Mission.Passive.EarnRoleXp.1, Challenges.Challenge.Mission.Passive.EarnRoleXp.2, Challen… | 1 | Mission.Passive.EarnAnyRoleXp |
| `Mission.Passive.TimePlayed` | WDMetaPrerequisiteSchema | Challenges.Challenge.Mission.Passive.TimePlayed.1, Challenges.Challenge.Mission.Passive.TimePlayed.2, Challen… | 1 | Mission.Passive.TimePlayed |
<!-- /datatable_catalog -->

## WDAchievementDefinition

Tables: [`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDAchievementDefinition -->
*1 table(s), 10 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `SteamAchievementID` | `DisplayName` |
|---|---|---|
| `Achievement.Tutorial.Completed` | ACH_TUTORIAL_COMPLETED | Complete The Tutorial |
| `Achievement.Tutorial.PunchKristopher` | ACH_TUTORIAL_PUNCH_KRISTOPHER | Punch Kristopher |
| `Achievement.Economy.TopCashEarner` | ACH_ECONOMY_TOP_CASH_EARNER | Top Cash Earner |
| `Achievement.Economy.SingleLifeProfit` | ACH_ECONOMY_SINGLE_LIFE_PROFIT | Single Life Profit |
| `Achievement.Economy.LoadoutSpend` | ACH_ECONOMY_LOADOUT_SPEND | Loadout Spender |
| `Achievement.Survival.ControlZoneSurvivor` | ACH_SURVIVAL_CONTROL_ZONE_SURVIVOR | Control Zone Survivor |
| `Achievement.Combat.LongShot` | ACH_COMBAT_LONG_SHOT | Long Shot |
| `Achievement.Match.CleanSweep` | ACH_MATCH_CLEAN_SWEEP | Clean Sweep |
| `Achievement.Combat.RicochetKill` | ACH_COMBAT_RICOCHET_KILL | Ricochet Kill |
| `Achievement.Combat.DefibrillatorKill` | ACH_COMBAT_DEFIBRILLATOR_KILL | Defibrillator Kill |
<!-- /datatable_catalog -->
