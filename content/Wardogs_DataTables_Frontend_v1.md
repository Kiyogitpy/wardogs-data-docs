---
title: "Data Tables: Frontend, Server and Test Data"
redirect_from: ["/Wardogs_DataTables_Frontend_v1.html", "/Wardogs_DataTables_Frontend_v1"]
parent: "Data Tables"
grand_parent: "Data Tables & Tags"
description: "Frontend, server and test tables: loading-screen tips and menu data"
---

# Data Tables: Frontend, Server and Test Data
*Generic expansion of the data tables below, built by [`_tools/datatable_catalog.py`](../_tools/datatable_catalog.py) (`--write` is idempotent). Back to the [catalog index](Wardogs_DataTables_v1.md).*

> Columns are the flattened row fields: nested structs are dotted keys, gameplay tags show the tag name, object references show the asset name, arrays are joined with commas. Columns empty in every row are dropped. Long cells are cut with an ellipsis; open the table JSON for the full value.

## WDLoadingScreenTips

Tables: `DT_LoadingScreenTips`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDLoadingScreenTips -->
*1 table(s), 110 rows, 1 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `LoadingScreenText` |
|---|---|
| `Tip.Economy.Cash.TeamPlay` | Earning cash is easy if you're a team player. Playing the objective and helping your team rewards you with ca… |
| `Tip.Items.Weapons.FreeRifle` | Low on cash? Each faction provides a free rifle at the equipment vendor. |
| `Tip.ControlZone.FactionCount` | Every player in the Control Zone contributes 1 point to their team's Faction Count. The team with the highest… |
| `Tip.ControlZone.HotZone` | The Hot Zone (HZ) is a roaming sub-zone inside the Control Zone. Players in the Hot Zone count for twice the … |
| `Tip.Travel.Squads.FriendPings` | Create a squad with your friends to see each others pings and enable squad chat. |
| `Tip.Inventory.Ammo.Consolidate` | Use the ammo consolidation button in your inventory to combine rounds of the same caliber, maximizing the num… |
| `Tip.Combat.Weapons.FireModes` | Many weapons support multiple fire modes (e.g., semi-auto, burst, full-auto). Choose the mode that suits the … |
| `Tip.Combat.Weapons.Zeroing` | Zeroing makes the reticle accurate at a chosen range. While aiming down sight, adjust the zero up or down to … |
| `Tip.ControlZone.HotZone.Rewards` | The Hot Zone counts you as 2 players and rewards bonus cash for every teamplay action. |
| `Tip.Economy.Cash.SpendAtVendors` | Spend cash at Vendors to buy items and vehicles. Short on funds? Pick up the free weapon and go get some kill… |
| `Tip.Economy.Cash.Persistent` | The cash you earn in a match is persistent. Whatever you leave the match with, is what you have to spend in t… |
| `Tip.Movement.Mantle` | You can mantle over objects of different heights; the higher the obstacle, the longer the mantle takes. |
| `Tip.Interaction.WorldObjects` | You can interact with objects in the world, such as doors. When several actions are available, an options lis… |
| `Tip.Health.HealthBar` | Your current health is displayed in a bar at the bottom right of the screen. Keep an eye on this while in com… |
| `Tip.Health.CriticalState` | When your health reaches zero, you enter the critical state. If you aren't revived in time, you'll bleed out … |
| `Tip.Health.Revive` | If a friendly player is in a critical state, get within range, interact, and select Revive. Reviving with no … |
| `Tip.Inventory.Ammo.Combine` | Use the combine ammo button in your inventory to combine rounds of the same caliber, maximizing the number of… |
| `Tip.Economy.Loadout.Invest` | The most expensive loadout isn't always the most profitable. Tactically invest when you think you need too. |
| `Tip.Travel.Misc.RequestSupport` | Requesting ammo / healing / supplies / backup via the ping wheel lets your team know you need support at your… |
| `Tip.Health.ProximityHelp` | Need healing / ammo? Use proximity chat to ask for help from teammates, or loot an enemy corpse. |
| `Tip.Travel.Misc.RequestPickup` | Stuck in spawn with no cash? Request a pickup via the ping wheel to let your team know. |
| `Tip.Travel.Misc.AcknowledgeRequest` | You can acknowledge a distant players request for revive / health / pickup by pinging their request icon abov… |
| `Tip.Combat.UseCover` | Open space in the Control Zone is lethal, always try and keep cover nearby. |
| `Tip.SpawnVehicle.KeepSafe` | Spawn Vehicles are extremely advantageous for your team. Keep them hidden, keep them secret, keep them safe. |
| `Tip.Health.Resuscitator` | You can add one free resuscitator to your loadout per life - They help keep your team up and reward cash on r… |
| `Tip.Health.DragToSafety` | Dragging teammates to safety before reviving them is often a safer strategy than risking a revive out in the … |
| `Tip.Items.Gear.GhillieSuit` | Ghillie suits are extremely effective at hiding your location in forested areas. Not so useful in urban comba… |
| `Tip.Economy.Armour.WaitForRevive` | Your armor will likely outlive you. You might be throwing money away by respawning - consider waiting for a r… |
| `Tip.Combat.FriendlyFire` | Remember: friendly fire, isn't friendly. |
| `Tip.Travel.Map.MinimapZoom` | You can change the zoom level of the minimap on the fly - check your key bindings! |
| `Tip.Items.Gear.GhillieSuit.Infrared` | The ghillie suit makes you invisible to Infrared Binoculars. |
| `Tip.Economy.SupplyCrate.Trade` | You can buy and sell items to other players in the Control Zone for a profit by purchasing and filling a supp… |
| `Tip.Travel.Map.ChatCoordinates` | Clicking on coordinates shared by teammates in the chatbox will open that location on your tactical map. |
| `Tip.Vehicles.General.GiveLifts` | When you buy a vehicle, check if there are any teammates in your safe zone that need a lift before leaving. D… |
| `Tip.Vehicles.General.Unlock` | Purchased vehicles must be unlocked to allow teammates to enter. |
| `Tip.Vehicles.General.Parachutes` | You can see who does or doesn't have a parachute in the passenger list of your vehicle - especially useful fo… |
| `Tip.Vehicles.Rotary.FlyLow` | Flying low stops certain launchers being able to lock on to your vehicle. |
| `Tip.Combat.Vehicles.WeakPoints` | If you want to quickly dispose of an enemy vehicle, try focusing damage on its weak points (such as the engin… |
| `Tip.Vehicles.Refuel.SafeZone` | You can repair and refuel vehicles by returning to your factions safe zone - alternatively land in a FOB buil… |
| `Tip.Combat.Ammo.HollowPoint` | "Flesh Damage" Hollow Point (HP) ammo is particularly effective at damaging non-armored body parts. |
| `Tip.Combat.Ammo.ArmourPiercing` | Armor Piercing (AP) ammo is effective at penetrating armor. |
| `Tip.Combat.Ammo.FMJ` | "Standard" Full Metal Jacket (FMJ) ammo is a middle ground between flesh damage and penetration. |
| `Tip.Movement.Weight` | Weight effects your movement - to the point you can no longer tac-sprint if you carry too many items. |
| `Tip.ControlZone.DrillTowers` | Drill towers can be captured once inside them. Once captured - they reveal a part of a longer key code. Colle… |
| `Tip.ControlZone.DrillTowers.Loot` | Drill towers have randomized helpful equipment that spawn on their roofs - consider looting at the risk of be… |
| `Tip.Vehicles.Artillery.Angle` | The angle of your artillery tank effects the distance and direction of rounds. A level surface gives you the … |
| `Tip.Combat.Mines` | Claymores and AT mines are lethal to all players, not just enemies. Be careful where you place them. |
| `Tip.Buildables.Repair` | Damaged buildables can be repaired by hitting them with a hammer. |
| `Tip.Combat.Ricochet` | Bullets can ricochet off walls and penetrate surfaces. Remember this when retreating behind cover. |
| `Tip.ControlZone.WinCondition` | Winning WARDOGS is not just about kills. Every player in the Control Zone is helping their team gain a majori… |
| `Tip.Combat.Ammo.ShotgunSlugs` | Shotgun slugs can perform exceptionally well at range - providing more penetration capability than buckshot. |
| `Tip.ControlZone.DrillTowers.Duplicate` | Drill towers can be captured once inside them. Once captured - they reveal a part of a longer key code. Colle… |
| `Tip.Combat.Headshots` | Aim for the head. Not only does it kill targets without a helmet faster - you'll earn bonus cash and they'll … |
| `Tip.Combat.TargetLimbs` | Think before you pull the trigger - sometimes it makes sense to shoot unarmored limbs than try to penetrate h… |
| `Tip.Economy.Cash.LongRangeKills` | Snipers, artillery and mortars receive additional cash rewards the further away they are from their killed ta… |
| `Tip.Items.Looting.UseUnlocked` | Even if you haven't unlocked an item, you can still use it if you loot a body or purchase it from a supply cr… |
| `Tip.Combat.Weapons.QuickReload` | In close quarters, milliseconds matter. Double-tap reload to drop your current magazine and load the next one… |
| `Tip.Buildables.Strategy` | Build strategically - you can place FOBs and build outside the CZ if you think it'll give your team a tactica… |
| `Tip.Vehicles.Refuel.HIDZ` | High Impact Damage Zones (HIDZ) on vehicles can be repaired with repair tools. Consider buying one from the e… |
| `Tip.Travel.Routes` | Entering the Control Zone via the most direct route isn't always the safest option. Use alternative routes if… |
| `Tip.Travel.TrustDriver` | Make sure you trust your chosen pilot / driver to get you safely to the Control Zone - every trip to the CZ i… |
| `Tip.Economy.Cash.Dropoffs` | Taking players to the Control Zone in a vehicle can be very profitable. Consider returning to the Safe Zone a… |
| `Tip.Vehicles.Artillery.Fuel` | After parking up your artillery tank, remember to turn off the engine before switching to the gunner position… |
| `Tip.Vehicles.Aircraft.Altitude` | When in aircraft, ASL is your 'Altitude above Sea Level' and AGL is your 'Altitude above Ground Level'. |
| `Tip.Intro.LearnToPlay` | Remember to check the 'Learn to Play' section in the main menu for information on more advanced mechanics. |
| `Tip.Combat.HammerKill` | Hitting someone with a large hammer is an instant kill. |
| `Tip.Health.WaitForReviveReward` | If you wait for a revive from a teammate instead of giving up - you'll receive a cash reward for your patienc… |
| `Tip.Travel.LocalChat` | Both friendly and enemy players can hear you in local chat - use this knowledge to your advantage. |
| `Tip.Economy.EquipmentValue` | You can see your current equipment value when you open your inventory. Every bullet you fire is cash spent. |
| `Tip.Combat.Suppression` | Suppression can be effective at stopping players peeking angles - consider firing toward the enemy while your… |
| `Tip.Movement.SlowWalk` | You can bind 'slow walk' to a dedicated key to keep your footsteps quiet at the cost of speed. |
| `Tip.Combat.Spotting` | Spotting enemy player with binoculars makes them show up for your teammates on their mini and tactical maps. … |
| `Tip.Intro.Basics` | Complete role-specific actions to gain XP for that role (e.g., reviving grants Medic XP). |
| `Tip.Items.FreeWeapons` | Each faction offers one FREE weapon, so you'll never deploy without being combat-ready. |
| `Tip.Items.Gear.Armour` | Helmets and armor reduce damage from gunfire. Superior armor covers more of the body and offers better protec… |
| `Tip.Items.Gear.Backpacks` | Backpacks increase your carry capacity, allowing a bigger loadout. |
| `Tip.Items.Gear.Vests` | Vests provide Quick Access slots, used to swiftly switch between equipped items. |
| `Tip.Items.Utility.Traversal` | The Traversal slot is dedicated to movement gear, for example, parachutes. |
| `Tip.Items.Weapons.Purchasing` | Interact with the Equipment Vendor, open the weapons tab, and pick your weapon. Use filters to quickly find y… |
| `Tip.SpawnVehicle.Availability` | You can only spawn into your team’s Spawn Vehicle from the Spawn Board once its stationary inside the Control… |
| `Tip.SpawnVehicle.Cooldown` | If your team’s Spawn Vehicle takes enough damage, it will be destroyed. The Spawn Board then becomes inactive… |
| `Tip.SpawnVehicle.Unlocking` | Upon any team reaching 20 points from holding the Control Zone, each of the three teams will be granted a fre… |
| `Tip.Travel.Map.FactionRequests` | Downed allies and various faction requests will appear on the mini map. Check it frequently to see how you ca… |
| `Tip.Travel.Map.TacticalMap` | Use the tactical map to navigate; zoom in and out and pan around to spot key information that helps you plan … |
| `Tip.Travel.Map.Zones` | The mini map shows whether you are in the Control Zone, the Hot Zone, or No Man's Land. Take note of area tit… |
| `Tip.Travel.Misc.PingWheel` | The Ping Wheel is a powerful tool which you can use to make faction requests, to send squad commands, and to … |
| `Tip.Travel.Squads.CreateASquad` | You can create a new squad by accessing the Squad Menu and selecting the 'Create Squad' option. Whoever creat… |
| `Tip.Travel.Squads.JoinASquad` | To join an already existing squad, open the Squad Menu and select 'Join Squad' icon. It's also worth noting, … |
| `Tip.Travel.Squads.Pings` | The Squad Ping System allows you to easily mark a location or a threat for other squad members, without needi… |
| `Tip.Travel.Squads.SquadChat` | Squad Chat provides private text and voice channels for you and your squad. Allowing  focused and strategic d… |
| `Tip.Travel.Squads.SquadTracker` | All squadmates trackers are colored gold, making them easier to distinguish from the rest of your team. |
| `Tip.Travel.Squads.VehicleSquadLock` | After purchasing a vehicle from the Vendor, you can Squad Lock it. This results in the vehicle only being acc… |
| `Tip.Vehicles.General.Cameras` | Drivers and pilots can cycle between first- and third-person cameras. When in third person, you can also ente… |
| `Tip.Vehicles.General.Crews` | Vehicle crews share responsibilities. The driver or pilot navigates the battlefield, while gunners tracks tar… |
| `Tip.Vehicles.General.Entering` | To enter a vehicle, approach it and use the interaction prompt to initiate the Enter Vehicle action. |
| `Tip.Vehicles.General.Exiting` | Exit a vehicle by using the interaction menu. Press and Hold the Exit Vehicle option. |
| `Tip.Vehicles.General.GarageVendor` | Purchase ammo & supply crates for your vehicle. When sitting in a driver or pilot seat in the vehicle spawn, … |
| `Tip.Vehicles.General.Health` | Dashboard icons and smoke indicate your vehicle's status. Bail out or repair it before it's destroyed. |
| `Tip.Vehicles.General.Locking` | Vehicles are purchased in a locked state. Their owners can choose to unlock them for their squad, or everyone… |
| `Tip.Vehicles.General.Seats` | You can switch seats within a vehicle, but note, switching isn't instant and will take a moment. |
| `Tip.Vehicles.Refuel.FuelCan` | The Fuel Can is a purchasable item, used to provide emergency fuel during combat or travel. It can be stored … |
| `Tip.Vehicles.Refuel.GasStation` | Repair and refuel vehicles by returning to Headquarters or a FOB. This doesn't come free, you will be charged. |
| `Tip.Vehicles.Refuel.RepairTools` | Use the Vehicle Repair Tool to repair damaged vehicles. There are three types; pick the one that fits budget.… |
| `Tip.Vehicles.Rotary.Blades` | Be careful with the rotor blades, if they hit objects, they will break. |
| `Tip.Vehicles.Rotary.Flares` | Flares can be used to momentarily prevent heat-seeking projectiles from locking onto your helicopter. |
| `Tip.Vehicles.Rotary.Spooling` | Helicopter engines must spool up before takeoff, this can take a few moments and is done by the pilot. |
| `Tip.Vendor.CarryingItems` | You need a backpack to carry magazines and other essential equipment. Watch your carry weight, the more you t… |
| `Tip.Vendor.GarageVendor` | The Garage Vendor is accessible while seated in the driver’s or gunner’s seat. It sells vehicle supplies, suc… |
| `Tip.Vendor.Rebuy` | On respawn, you can repurchase the items you bought in your previous life. |
| `Tip.Vendor.VehicleVendor` | Vehicle vendors sell cars, tanks, helicopters and more. You can collect your vehicle near the main road to th… |
<!-- /datatable_catalog -->

## WDExperienceServerBrowserTagRow

Tables: `DT_ExperienceServerBrowserTags`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDExperienceServerBrowserTagRow -->
*1 table(s), 19 rows, 3 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `DescriptorTags` | `_aaabmndfbjeemaenllmhj` | `Tag` |
|---|---|---|---|
| `Experience.Rules.InfantryOnly` | Server.Descriptor.InfantryOnly |  | Experience.Rules.InfantryOnly |
| `Experience.Rules.Hardcore` | Server.Descriptor.Hardcore |  | Experience.Rules.Hardcore |
| `Experience.Rules.AutoAssignFactions` |  |  | Experience.Rules.AutoAssignFactions |
| `Experience.Rules.AutoAssignFirstFaction` |  |  | Experience.Rules.AutoAssignFirstFaction |
| `Experience.Rules.ChangeTeamDisabled` | Server.Descriptor.ChangeTeamDisabled |  | Experience.Rules.ChangeTeamDisabled |
| `Experience.Rules.ChatboxDisabled` |  |  | Experience.Rules.ChatboxDisabled |
| `Experience.Rules.ControlZoneRequiresTag` |  |  | Experience.Rules.ControlZoneRequiresTag |
| `Experience.Rules.EnablePresenceJoinOnExperienceLoad` |  |  | Experience.Rules.EnablePresenceJoinOnExperienceLoad |
| `Experience.Rules.FreeForAll` |  |  | Experience.Rules.FreeForAll |
| `Experience.Rules.GiveUpDisabled` | Server.Descriptor.GiveUpDisabled |  | Experience.Rules.GiveUpDisabled |
| `Experience.Rules.KillfeedSquadOnly` | Server.Descriptor.ReducedHUD.KillfeedSquadOnly |  | Experience.Rules.KillfeedSquadOnly |
| `Experience.Rules.NoCashFeed` | Server.Descriptor.ReducedHUD.CashFeed |  | Experience.Rules.NoCashFeed |
| `Experience.Rules.VaultEnabled` |  |  | Experience.Rules.VaultEnabled |
| `Experience.Rules.NoDynamicCrosshair` | Server.Descriptor.ReducedHUD.DynamicCrosshair |  | Experience.Rules.NoDynamicCrosshair |
| `Experience.Rules.NoHudAmmo` | Server.Descriptor.ReducedHUD.HudAmmo |  | Experience.Rules.NoHudAmmo |
| `Experience.Rules.NoMinimapHealth` | Server.Descriptor.ReducedHUD.MinimapHealth |  | Experience.Rules.NoMinimapHealth |
| `Experience.Rules.NoQuickSlots` | Server.Descriptor.ReducedHUD.QuickSlots |  | Experience.Rules.NoQuickSlots |
| `Experience.Rules.RebuyDisabled` | Server.Descriptor.RebuyDisabled |  | Experience.Rules.RebuyDisabled |
| `Experience.Rules.SkipPlayerDeathItemDrop` |  | Server.Descriptor.PlayerLootingDisabled | Experience.Rules.SkipPlayerDeathItemDrop |
<!-- /datatable_catalog -->

## WDServerBrowserRegionData

Tables: `DT_OnlineRegions`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDServerBrowserRegionData -->
*1 table(s), 14 rows, 3 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Endpoint` | `DisplayName` | `bIsFallback` |
|---|---|---|---|
| `eu-central` | dynamodb.eu-central-1.amazonaws.com | Europe (Central) | true |
| `eu-east` | dynamodb.eu-north-1.amazonaws.com | Europe (East) | false |
| `eu-west` | dynamodb.eu-west-2.amazonaws.com | Europe (West) | false |
| `eu-south` | dynamodb.eu-south-1.amazonaws.com | Europe (South) | false |
| `na-central` | dynamodb.us-east-2.amazonaws.com | North America (Central) | false |
| `na-north` | dynamodb.ca-central-1.amazonaws.com | North America (North) | false |
| `na-east` | dynamodb.us-east-1.amazonaws.com | North America (East) | false |
| `na-west` | dynamodb.us-west-2.amazonaws.com | North America (West) | false |
| `south-america` | dynamodb.sa-east-1.amazonaws.com | South America | false |
| `asia-east` | dynamodb.ap-northeast-2.amazonaws.com | Asia (East) | false |
| `asia-west` | dynamodb.ap-south-1.amazonaws.com | Asia (West) | false |
| `asia-se` | dynamodb.ap-southeast-1.amazonaws.com | Asia (South East) | false |
| `oceania` | dynamodb.ap-southeast-2.amazonaws.com | Oceania | false |
| `south-africa` | dynamodb.af-south-1.amazonaws.com | South Africa | false |
<!-- /datatable_catalog -->

## WDUIServerBrowserMapTextureTableRow

Tables: `DT_ServerBrowserMapTexture`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDUIServerBrowserMapTextureTableRow -->
*1 table(s), 12 rows, 3 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `DisplayName` | `DefaultMapTexture` | `GameMode` |
|---|---|---|---|
| `Bakurani_KOTH_01` | Bakurani | T_UI_LoadingScreen_Bakurani | KOTH |
| `Madrid_KOTH_01` | Ozeti | T_UI_LoadingScreen_Ozeti | KOTH |
| `Detroit_KOTH_01` | Zestafona | T_UI_LoadingScreen_Zestafona | KOTH |
| `Moscow_KOTH_01` | Saburtulo | T_UI_LoadingScreenMoscow | KOTH |
| `Bakurani_SniperShowdown_01` | Bakurani Outskirts - Jutari | T_UI_LoadingScreen_Bakurani | Sniper Showdown |
| `Tanktown` | Tank Town |  | Tank Town |
| `Mindori_KOTH_01` |  |  | KOTH |
| `Tevza_KOTH_01` |  |  | KOTH |
| `Berlin_KOTH_01` |  |  | KOTH |
| `Deathmatch` | Deathmatch |  | Deathmatch |
| `Paris_KOTH_01` |  |  | KOTH |
| `Bakurani_KOTH_02` | Bakurani | T_UI_LoadingScreen_Bakurani | KOTH |
<!-- /datatable_catalog -->

## WDUIUserSettingDisplayDataTableRow

Tables: `DT_Settings_DisplayData`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDUIUserSettingDisplayDataTableRow -->
*1 table(s), 15 rows, 5 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `SettingsDisplayWidgetParams.WidgetClass` | `SettingsDisplayWidgetParams.ViewModelParams.ViewModelClass` | `SettingsDisplayWidgetParams.ViewModelParams.Data` | `SettingsDisplayWidgetParams._aaabkejhohfkdpglkgkep` | `Tag` |
|---|---|---|---|---|---|
| `UserSettings.Controls.Gamepad.DeadZone.MoveStick.Preset` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.MoveStick.Preset |
| `UserSettings.Controls.Gamepad.DeadZone.MoveStick.Centre` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.MoveStick.Centre |
| `UserSettings.Controls.Gamepad.DeadZone.MoveStick.Axial` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.MoveStick.Axial |
| `UserSettings.Controls.Gamepad.DeadZone.MoveStick.MaxInput` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.MoveStick.MaxInput |
| `UserSettings.Controls.Gamepad.DeadZone.LookStick.Preset` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.LookStick.Preset |
| `UserSettings.Controls.Gamepad.DeadZone.LookStick.Centre` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.LookStick.Centre |
| `UserSettings.Controls.Gamepad.DeadZone.LookStick.Axial` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.LookStick.Axial |
| `UserSettings.Controls.Gamepad.DeadZone.LookStick.MaxInput` | W_DeadZone_Analogue.W_DeadZone_Analogue_C | WDGame.WDUIUserSettingDisplay_DeadZoneAnalogueViewModel | DA_DeadZoneAnalogue | false | UserSettings.Controls.Gamepad.DeadZone.LookStick.MaxInput |
| `UserSettings.Controls.Gamepad.DeadZone.Triggers.Preset` | W_DeadZone_Trigger.W_DeadZone_Trigger_C | WDGame.WDUIUserSettingDisplay_DeadZoneTriggerViewModel | DA_DeadZoneTrigger | false | UserSettings.Controls.Gamepad.DeadZone.Triggers.Preset |
| `UserSettings.Controls.Gamepad.DeadZone.LeftTrigger.Min` | W_DeadZone_Trigger.W_DeadZone_Trigger_C | WDGame.WDUIUserSettingDisplay_DeadZoneTriggerViewModel | DA_DeadZoneTrigger | false | UserSettings.Controls.Gamepad.DeadZone.LeftTrigger.Min |
| `UserSettings.Controls.Gamepad.DeadZone.LeftTrigger.Max` | W_DeadZone_Trigger.W_DeadZone_Trigger_C | WDGame.WDUIUserSettingDisplay_DeadZoneTriggerViewModel | DA_DeadZoneTrigger | false | UserSettings.Controls.Gamepad.DeadZone.LeftTrigger.Max |
| `UserSettings.Controls.Gamepad.DeadZone.RightTrigger.Min` | W_DeadZone_Trigger.W_DeadZone_Trigger_C | WDGame.WDUIUserSettingDisplay_DeadZoneTriggerViewModel | DA_DeadZoneTrigger | false | UserSettings.Controls.Gamepad.DeadZone.RightTrigger.Min |
| `UserSettings.Controls.Gamepad.DeadZone.RightTrigger.Max` | W_DeadZone_Trigger.W_DeadZone_Trigger_C | WDGame.WDUIUserSettingDisplay_DeadZoneTriggerViewModel | DA_DeadZoneTrigger | false | UserSettings.Controls.Gamepad.DeadZone.RightTrigger.Max |
| `UserSettings.Audio.MicrophoneTest.Enabled` | W_MicLevelMeter.W_MicLevelMeter_C | WDGame.WDUIUserSettingDisplay_MicLevelMeterViewModel | DA_MicLevelMeter | false | UserSettings.Audio.MicrophoneTest.Enabled |
| `UserSettings.Audio.Volume.Microphone` | W_MicLevelMeter.W_MicLevelMeter_C | WDGame.WDUIUserSettingDisplay_MicLevelMeterViewModel | DA_MicLevelMeter | false | UserSettings.Audio.Volume.Microphone |
<!-- /datatable_catalog -->

## WDUIScoreboardStatTableRow

Tables: `DT_ScoreboardStats_Default`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDUIScoreboardStatTableRow -->
*1 table(s), 5 rows, 7 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `WidgetClass` | `DisplayText` | `ValueFormat` | `FilterButtonClass` | `FilterButtonStyle` | `_aaaamdfdkodnjbklifhhh` | `Tag` |
|---|---|---|---|---|---|---|---|
| `Analytics.Player.Cash.Earned` | W_ScoreboardStat_Cash.W_ScoreboardStat_Cash_C | Cash Earned | Cash | W_ScoreboardFilterButton.W_ScoreboardFilterButton_C | B_Style_Button_ScoreboardFilter_CashEarned.B_Style_Button_ScoreboardFilter_CashEarned_C | 0.75 | Analytics.Player.Cash.Earned |
| `Analytics.Player.Kills` | W_ScoreboardStat.W_ScoreboardStat_C | Kills | Simple | W_ScoreboardFilterButton.W_ScoreboardFilterButton_C | B_Style_Button_ScoreboardFilter_Kills.B_Style_Button_ScoreboardFilter_Kills_C | 0.5 | Analytics.Player.Kills |
| `Analytics.Player.Assists` | W_ScoreboardStat.W_ScoreboardStat_C | Assists | Simple | W_ScoreboardFilterButton.W_ScoreboardFilterButton_C | B_Style_Button_ScoreboardFilter_Assists.B_Style_Button_ScoreboardFilter_Assists_C | 0.5 | Analytics.Player.Assists |
| `Analytics.Player.Revives` | W_ScoreboardStat.W_ScoreboardStat_C | Revives | Simple | W_ScoreboardFilterButton.W_ScoreboardFilterButton_C | B_Style_Button_ScoreboardFilter_Revives.B_Style_Button_ScoreboardFilter_Revives_C | 0.5 | Analytics.Player.Revives |
| `Analytics.Player.Deaths` | W_ScoreboardStat.W_ScoreboardStat_C | Deaths | Simple | W_ScoreboardFilterButton.W_ScoreboardFilterButton_C | B_Style_Button_ScoreboardFilter_Deaths.B_Style_Button_ScoreboardFilter_Deaths_C | 0.5 | Analytics.Player.Deaths |
<!-- /datatable_catalog -->

## WDUILevelTableRow

Tables: `DT_LevelIcons`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDUILevelTableRow -->
*1 table(s), 7 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `CareerLevelIcons` | `Tag` |
|---|---|---|
| `Meta.Role.Wardog` | {Key=0; Value=T_UI_Icon_CareerLevel_Unranked}, {Key=1; Value=T_UI_Icon_CareerLevel_1}, {Key=2; Value=T_UI_Ico… | Meta.Role.Wardog |
| `Meta.Role.Driver` | {Key=0; Value=T_UI_Icon_DriverLevel_Tier1}, {Key=50; Value=T_UI_Icon_DriverLevel_Tier2}, {Key=100; Value=T_UI… | Meta.Role.Driver |
| `Meta.Role.Infantry` | {Key=0; Value=T_UI_Icon_AssaultLevel_Tier1}, {Key=50; Value=T_UI_Icon_AssaultLevel_Tier2}, {Key=100; Value=T_… | Meta.Role.Infantry |
| `Meta.Role.Medic` | {Key=0; Value=T_UI_Icon_MedicLevel_Tier1}, {Key=50; Value=T_UI_Icon_MedicLevel_Tier2}, {Key=100; Value=T_UI_I… | Meta.Role.Medic |
| `Meta.Role.Pilot` | {Key=0; Value=T_UI_Icon_PilotLevel_Tier1}, {Key=50; Value=T_UI_Icon_PilotLevel_Tier2}, {Key=100; Value=T_UI_I… | Meta.Role.Pilot |
| `Meta.Role.Recon` | {Key=0; Value=T_UI_Icon_ReconLevel_Tier1}, {Key=50; Value=T_UI_Icon_ReconLevel_Tier2}, {Key=100; Value=T_UI_I… | Meta.Role.Recon |
| `Meta.Role.Support` | {Key=0; Value=T_UI_Icon_SupportLevel_Tier1}, {Key=50; Value=T_UI_Icon_SupportLevel_Tier2}, {Key=100; Value=T_… | Meta.Role.Support |
<!-- /datatable_catalog -->

## WDUISquadIntentTableRow

Tables: `DT_SquadIntents`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDUISquadIntentTableRow -->
*1 table(s), 12 rows, 4 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `DisplayName` | `Icon` | `SortOrder` | `Tag` |
|---|---|---|---|---|
| `Squad.Intent.Building` | Building | T_UI_SquadIntent_Building | 10 | Squad.Intent.Building |
| `Squad.Intent.Hotzone` | Hotzone | T_UI_SquadIntent_Hotzon | 20 | Squad.Intent.Hotzone |
| `Squad.Intent.AirCombat` | Air Combat | T_UI_SquadIntent_AirCombat | 50 | Squad.Intent.AirCombat |
| `Squad.Intent.GroundCombat` | Ground Combat | T_UI_SquadIntent_GroundCombat | 60 | Squad.Intent.GroundCombat |
| `Squad.Intent.AirTransport` | Air Transport | T_UI_SquadIntent_AirTransport | 70 | Squad.Intent.AirTransport |
| `Squad.Intent.GroundTransport` | Ground Transport | T_UI_SquadIntent_GroundTransport | 80 | Squad.Intent.GroundTransport |
| `Squad.Intent.FOBAssault` | FOB Assault | T_UI_SquadIntent_FobAssault | 90 | Squad.Intent.FOBAssault |
| `Squad.Intent.TalkingShit` | Talking shit | T_UI_SquadIntent_Talking | 100 | Squad.Intent.TalkingShit |
| `Squad.Intent.NoobFriendly` | Noob friendly | T_UI_SquadIntent_NoobFriendly | 110 | Squad.Intent.NoobFriendly |
| `Squad.Intent.Competitive` | Competitive | T_UI_SquadIntent_Competitive | 120 | Squad.Intent.Competitive |
| `Squad.Intent.CapturingTowers` | Capturing Towers | T_UI_SquadIntent_TowerCapture | 30 | Squad.Intent.CapturingTowers |
| `Squad.Intent.Recon` | Recon | T_UI_SquadIntent_Recon | 40 | Squad.Intent.Recon |
<!-- /datatable_catalog -->

## WDUIDeploymentBoardRejectionTableRow

Tables: `DT_DeploymentRejectionReasons`, `DT_DeploymentRejectionReasons_ControlZone`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDUIDeploymentBoardRejectionTableRow -->
*2 table(s), 12 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Table | Row | `RejectionText` | `Tag` |
|---|---|---|---|
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.Cooldown` | Deployment on cooldown - {Minutes}:{Seconds} | Interactive.Deployment.Rejection.Cooldown |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.Driving` | Spawn vehicle is moving | Interactive.Deployment.Rejection.Driving |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.LowHP` | Spawn vehicle has too low HP | Interactive.Deployment.Rejection.LowHP |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.NoSeat` | No available seat | Interactive.Deployment.Rejection.NoSeat |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.NoVehicle` | No Active Spawn Vehicle | Interactive.Deployment.Rejection.NoVehicle |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Available` | Deployment Available | Interactive.Deployment.Available |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.NotInControlZone` | Spawn vehicle is not in the control zone | Interactive.Deployment.Rejection.NotInControlZone |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.RadarDestroyed` | Spawn Vehicle Radar Destroyed : Awaiting Repairs | Interactive.Deployment.Rejection.RadarDestroyed |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.Respawning` | Spawn Vehicle will respawn in {Minutes}:{Seconds} | Interactive.Deployment.Rejection.Respawning |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.ScoreRequired` | Inactive Vehicle: Min Required Game Score: {Score} | Interactive.Deployment.Rejection.ScoreRequired |
| `DT_DeploymentRejectionReasons` | `Interactive.Deployment.Rejection.PlayerNotEnteredControlZone` | MAP OFFLINE... ENTER ZONE FOR DATA | Interactive.Deployment.Rejection.PlayerNotEnteredControlZone |
| `DT_DeploymentRejectionReasons_ControlZone` | `Interactive.Deployment.Rejection.NotInControlZone` |  | Interactive.Deployment.Rejection.NotInControlZone |
<!-- /datatable_catalog -->

## WDDevMenuMapsDataTableRow

Tables: `DT_DevMenuMaps`, `DT_Gunsmith_DevMenuMaps`, `DT_Vehiclesmith_DevMenuMaps`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDDevMenuMapsDataTableRow -->
*3 table(s), 4 rows, 4 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Table | Row | `MapName` | `MapToLoad` | `CustomLoadingScreenWidgetClass` | `Tag` |
|---|---|---|---|---|---|
| `DT_DevMenuMaps` | `DevMaps.ShootingRange` | Shooting Range | Shooting_Range_4 |  | DevMaps.ShootingRange |
| `DT_DevMenuMaps` | `DevMaps.ArtWorld` | Art World | ArtWorld |  | DevMaps.ArtWorld |
| `DT_Gunsmith_DevMenuMaps` | `DevMaps.Gunsmith` | Gunsmith | Gunsmith_Main_P | W_GunsmithLoadingScreen_C | DevMaps.Gunsmith |
| `DT_Vehiclesmith_DevMenuMaps` | `DevMaps.Vehiclesmith` | Vehiclesmith | Vehiclesmith_Main_P | W_VehiclesmithLoadingScreen_C | DevMaps.Vehiclesmith |
<!-- /datatable_catalog -->

## WDClientHotConfigTableRow

Tables: `DT_ClientHotConfigs`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDClientHotConfigTableRow -->
*1 table(s), 3 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `TargetIniFile` | `IniBlob` |
|---|---|---|
| `ServerBrowserSubsystem` | Game | [/Script/WDGame.WDServerBrowserSubsystem]  MaxSelectedRegions=3  ServerIDLength=6  bAllowGlobalSearch=False |
| `AuthSubsystem` | Game | [/Script/WDGame.WDOnlineAuthSubsystem]  bEnableFulfillOrders=True |
| `CommunicationSubsystem` | Game | [/Script/WDGame.WDCommunicationSubsystem]  MaxLoginRetries=2  LoginRetryDelaySeconds=30.0  LoginRetryJitterFr… |
<!-- /datatable_catalog -->

## WDAutomatedTestServerProfile

Tables: `DT_ServerTestingProfiles`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDAutomatedTestServerProfile -->
*1 table(s), 11 rows, 4 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `bClientsOptIn` | `TotalClients` | `TestOrchestrator` | `CustomPlayerControllerClass` |
|---|---|---|---|---|
| `Default` | true | 100 | B_Default.B_Default_C |  |
| `SoloTest` | true | 1 | B_SoloTest.B_SoloTest_C |  |
| `Default10Players` | true | 10 | B_Default10Players.B_Default10Players_C |  |
| `100Players` | true | 100 | B_100Players.B_100Players_C |  |
| `100GroundVehicles` | true | 100 | B_100GroundVehicles.B_100GroundVehicles_C |  |
| `100TrackedVehicles` | true | 100 | B_100TrackedVehicles.B_100TrackedVehicles_C |  |
| `100Helicopters` | true | 100 | B_100Helicopters.B_100Helicopters_C |  |
| `30BotOrchestra` | true | 30 | B_30BotOrchestra.B_30BotOrchestra_C |  |
| `MovementMedley` | true | 100 | B_MovementMedley.B_MovementMedley_C |  |
| `Macarena` | true | 100 | B_Macarena.B_Macarena_C |  |
| `InputTest` | true | 5 | B_InputTest.B_InputTest_C | PC_AutomatedPlayerController_C |
<!-- /datatable_catalog -->

## WDAutomatedTestClientProfile

Tables: `DT_ClientTestingProfiles`. Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDAutomatedTestClientProfile -->
*1 table(s), 4 rows, 6 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `PawnToControl` | `CustomTestFunction` | `AutomatedInputs` | `InputMethod` | `ConsoleCommands` | `bCustomSpawnMode` |
|---|---|---|---|---|---|---|
| `Character` | B_WDMoverPlayerCharacter.B_WDMoverPlayerCharacter_C |  | {Key.KeyName=None; InputAction=IA_Player_MoveDirectional; InputInterval.Min=2; InputInterval.Max=2; InputDura… | Asynchronous |  | false |
| `DownedCharacter` | B_WDMoverPlayerCharacter.B_WDMoverPlayerCharacter_C | B_AutoTestFunc_DownedPlayer.B_AutoTestFunc_DownedPlayer_C | {Key.KeyName=None; InputAction=IA_Player_MoveDirectional; InputInterval.Min=2; InputInterval.Max=2; InputDura… | Asynchronous |  | false |
| `TriggerHappyCharacter` | B_WDMoverPlayerCharacter.B_WDMoverPlayerCharacter_C | B_AutoTestFunc_TriggerHappyPlayer.B_AutoTestFunc_TriggerHappyPlayer_C | {Key.KeyName=None; InputAction=IA_Player_MoveDirectional; InputInterval.Min=0; InputInterval.Max=0; InputDura… | Asynchronous | WD.Player.SetInfiniteAmmo True, WD.Player.SetInvulnerable True | true |
| `MovementCharacter` | B_WDMoverPlayerCharacter.B_WDMoverPlayerCharacter_C | B_AutomatedTestFunc_CustomSpawner.B_AutomatedTestFunc_CustomSpawner_C | {Key.KeyName=None; InputInterval.Min=10; InputInterval.Max=10; InputDuration.Min=10; InputDuration.Max=10}, {… | Sequential |  | true |
<!-- /datatable_catalog -->
