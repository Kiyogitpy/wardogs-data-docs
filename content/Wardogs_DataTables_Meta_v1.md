---
title: "Data Tables: Meta Progression and Cosmetics"
redirect_from: ["/Wardogs_DataTables_Meta_v1.html", "/Wardogs_DataTables_Meta_v1"]
parent: "Data Tables"
grand_parent: "Data Tables & Tags"
description: "Meta-progression and cosmetic tables: skill nodes, unlock trees and skins"
---

# Data Tables: Meta Progression and Cosmetics
*Generic expansion of the data tables below, built by [`_tools/datatable_catalog.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/datatable_catalog.py) (`--write` is idempotent). Back to the [catalog index](Wardogs_DataTables_v1.md).*

> Columns are the flattened row fields: nested structs are dotted keys, gameplay tags show the tag name, object references show the asset name, arrays are joined with commas. Columns empty in every row are dropped. Long cells are cut with an ellipsis; open the table JSON for the full value.

## WDMetaTreeNodeData_UI

Tables: [`DT_CharacterSkillNodes_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_CharacterSkillNodes_Data.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDMetaTreeNodeData_UI -->
*1 table(s), 131 rows, 4 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `FriendlyName` | `Description` | `NodeIcon` | `Tag` |
|---|---|---|---|---|
| `Meta.Role.Driver.AimDownSightSpeed.MountedGun` | Time-to-ADS speed improvement (Mounted MG - Ground Vehicles) | Reduces the amount of time it takes to enter ADS whilst using any mounted MG's on ground vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.AimDownSightSpeed.MountedGun |
| `Meta.Role.Driver.AutoRepair` | Can autorepair at petrol stations (Ground Vehicles) | Unlocks the ability to auto repair ground vehicles at a petrol station. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.AutoRepair |
| `Meta.Role.Driver.FuelUsageReduction` | Fuel usage rate reduction (Ground Vehicles) | Reduces the usage of fuel when driving ground vehicles, providing a longer fuel time. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.FuelUsageReduction |
| `Meta.Role.Driver.HorizontalRecoil.MountedGun` | Horizontal recoil reduction (Mounted MG - Ground Vehicles) | Reduces horizontal recoil experienced when firing a mounted MG on a ground vehicle. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.HorizontalRecoil.MountedGun |
| `Meta.Role.Driver.ImpactDamageReduction` | Impact damage reduction (Ground Vehicles) | Reduces the amount of damage your ground vehicle receives from impacting with objects & landscape in the worl… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.ImpactDamageReduction |
| `Meta.Role.Driver.IncreasedHealth.SupplyCrate` | Increased supply crate durability (Ground Vehicles) | Increases the amount of damage a supply crate can take before it is destroyed (when the supply crate is dropp… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.IncreasedHealth.SupplyCrate |
| `Meta.Role.Driver.QuickerEngineStart` | Engine turn on speed improvement | Reduces the time it takes to turn the engine on in ground vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.QuickerEngineStart |
| `Meta.Role.Driver.RefuelSpeed.PetrolStation` | Petrol station refueling speed improvement (Ground Vehicles) | Reduces the amount of time it takes to refuel a ground vehicle at a petrol station. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.RefuelSpeed.PetrolStation |
| `Meta.Role.Driver.RefuelSpeed.Spawn` | Spawnzone refueling speed improvement (Ground Vehicles) | Reduces the amount of time it takes to refuel a ground vehicle in the spawnzone. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.RefuelSpeed.Spawn |
| `Meta.Role.Driver.ReloadSpeed.MountedGun` | Reload speed improvement (Mounted MG - Ground Vehicles) | Reduces the amount of time it takes to reload the mounted MG's on ground vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.ReloadSpeed.MountedGun |
| `Meta.Role.Driver.RepairSpeed.Spawn` | Spawnzone Repairing speed improvement (Ground Vehicles) | Reduces the amount of time it takes to repair a ground vehicle in the spawnzone. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.RepairSpeed.Spawn |
| `Meta.Role.Driver.VerticalRecoil.MountedGun` | Vertical recoil reduction (Mounted MG - Ground Vehicles) | Reduces vertical recoil experienced when firing a mounted MG on a ground vehicle. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Driver.VerticalRecoil.MountedGun |
| `Meta.Role.Medic.BuffApplicationTime` | Buff application speed improvement | Reduces the amount of time it takes to apply buffs to self AND teammates. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.BuffApplicationTime |
| `Meta.Role.Medic.BuffDuration.Self` | Increased self buff duration | Increases the amount of time a buff is active after you have self-buffed. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.BuffDuration.Self |
| `Meta.Role.Medic.BuffDuration.Teammate` | Increased teammate buff duration | Increases the amount of time a buff is active on a teammate you have buffed. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.BuffDuration.Teammate |
| `Meta.Role.Medic.ChargeTime.Defibrillator` | Defib charge speed improvement | Reduces the amount of time it takes to charge up your defib. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ChargeTime.Defibrillator |
| `Meta.Role.Medic.DragSpeed` | Drag speed improvement | Increases the speed that you can move when you are dragging another player. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.DragSpeed |
| `Meta.Role.Medic.HealthierRevive` | Increased health after base reviving someone | Increases the amount of health a teammate revives with after you have revived them using the base-revive (no … | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.HealthierRevive |
| `Meta.Role.Medic.HealTime.Self` | Self-healing speed improvement | Reduces the amount of time it takes to heal yourself with all medical items. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.HealTime.Self |
| `Meta.Role.Medic.HealTime.Teammate` | Teammate healing speed improvement | Reduces the amount of time it takes to heal teammates with all medical items. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.HealTime.Teammate |
| `Meta.Role.Medic.HealTimeWhileSuppressed` | Faster healing whilst suppressed | Reduces the amount of time it takes to heal a teammate whilst you are experiencing the suppressed effect from… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.HealTimeWhileSuppressed |
| `Meta.Role.Medic.IncreaseBleedTime` | Increased bleedout timer | Increases the amount of time you have before you bleed out when you are in a downed state. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.IncreaseBleedTime |
| `Meta.Role.Medic.LessSuppression` | Reduced suppression effect | Reduces the severity of the suppression effect experienced when enemies are firing at you. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.LessSuppression |
| `Meta.Role.Medic.MedicalItemSwapSpeed` | Item-switch speed improvement (Medical Archetype) | Reduces the amount of time it takes to switch TO any items / equipment within the 'medical' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.MedicalItemSwapSpeed |
| `Meta.Role.Medic.MedicalItemWeightReduction` | Reduced weight-penalty for medical items | Reduces the amount of weight-penalty that is given from carrying medical items specifically. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.MedicalItemWeightReduction |
| `Meta.Role.Medic.MedicBag` | Medic bag (additional slots for medical items) | Unlocks the ability to purchase a medic bag, which provides additional slots specifically for medical items. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.MedicBag |
| `Meta.Role.Medic.MedkitUsage` | Medkits have more uses | Increases the amount of 'uses' a medkit has before it is depleted (only when you are using it). | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.MedkitUsage |
| `Meta.Role.Medic.ReducedFalldamage` | Reduced fall damage | Reduces the amount of fall damage you take. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReducedFalldamage |
| `Meta.Role.Medic.ReduceUsage.Defibrillator` | Increased charges per battery | Increases the amount of charges per battery when you are using a defib. (One time unlock). | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReduceUsage.Defibrillator |
| `Meta.Role.Medic.ReduceUsage.Medkit` | Medkits have more uses | Increases the amount of 'uses' a medkit has before it is depleted (only when you are using it). | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReduceUsage.Medkit |
| `Meta.Role.Medic.ReviveDamageReduction` | Take less damage whilst reviving teammate | Reduces the amount of incoming damage whilst you are reviving a teammate. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReviveDamageReduction |
| `Meta.Role.Medic.ReviveSpeed.Standard` | Base revive speed improvement | Reduces the time it takes to 'base-revive' a teammate. (no equipment, just bare hands). | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReviveSpeed.Standard |
| `Meta.Role.Medic.ReviveSpeedBoost.Self` | Increased sprint speed after reviving teammates | After you have revived a teammate, YOU will receive a temporary increase in your sprint speed. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReviveSpeedBoost.Self |
| `Meta.Role.Medic.ReviveSpeedBoost.Teammate` | Teammates faster after you've revived them | After you have revived a teammate, THEY will receive a temporary increase in their sprint speed. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.ReviveSpeedBoost.Teammate |
| `Meta.Role.Medic.StunResistance` | Reduced flash/stun effect duration | Reduces the duration of the effects received from flash & stun grenades. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Medic.StunResistance |
| `Meta.Role.Pilot.AimDownSightSpeed.MountedGun` | Time-to-ADS speed improvement (Mounted MG - Air Vehicles) | Reduces the amount of time it takes to enter ADS whilst using any mounted MG's on air vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.AimDownSightSpeed.MountedGun |
| `Meta.Role.Pilot.AutoRepair` | Can autorepair at petrol stations (Air Vehicles) | Unlocks the ability to auto repair air vehicles at a petrol station. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.AutoRepair |
| `Meta.Role.Pilot.FuelUsageReduction` | Fuel usage rate reduction (Air Vehicles) | Reduces the usage of fuel when piloting air vehicles, providing a longer fuel time. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.FuelUsageReduction |
| `Meta.Role.Pilot.HorizontalRecoil.MountedGun` | Horizontal recoil reduction (Mounted MG - Air Vehicles) | Reduces horizontal recoil experienced when firing a mounted MG on an air vehicle. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.HorizontalRecoil.MountedGun |
| `Meta.Role.Pilot.ImpactDamageReduction` | Impact damage reduction (Air Vehicles) | Reduces the amount of damage your air vehicle receives from impacting with objects & landscape in the world (… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.ImpactDamageReduction |
| `Meta.Role.Pilot.IncreasedHealth.SupplyCrate` | Increased supply crate durability (Air Vehicles) | Increases the amount of damage a supply crate can take before it is destroyed (when the supply crate is dropp… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.IncreasedHealth.SupplyCrate |
| `Meta.Role.Pilot.QuickerEngineStart` | Engine turn on speed improvement (Air Vehicles) | Reduces the time it takes to turn the engine on in air vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.QuickerEngineStart |
| `Meta.Role.Pilot.RefuelSpeed.PetrolStation` | Petrol station refueling speed improvement (Air Vehicles) | Reduces the amount of time it takes to refuel an air vehicle at a petrol station. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.RefuelSpeed.PetrolStation |
| `Meta.Role.Pilot.RefuelSpeed.Spawn` | Spawnzone refueling speed improvement (Air Vehicles) | Reduces the amount of time it takes to refuel an air vehicle in the spawnzone. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.RefuelSpeed.Spawn |
| `Meta.Role.Pilot.ReloadSpeed.MountedGun` | Reload speed improvement (Mounted MG - Air Vehicles) | Reduces the amount of time it takes to reload the mounted MG's on air vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.ReloadSpeed.MountedGun |
| `Meta.Role.Pilot.RepairSpeed.Spawn` | Spawnzone Repairing speed improvement (Air Vehicles) | Reduces the amount of time it takes to repair an air vehicle in the spawnzone. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.RepairSpeed.Spawn |
| `Meta.Role.Pilot.VerticalRecoil.MountedGun` | Vertical recoil reduction (Mounted MG - Air Vehicles) | Reduces vertical recoil experienced when firing a mounted MG on an air vehicle. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Pilot.VerticalRecoil.MountedGun |
| `Meta.Role.Recon.AimDownSightSpeed.Marksman` | Time-to-ADS speed improvement (Marksman Archetype) | Reduces the time it takes to enter ADS, specifically with weapons within the 'marksman' archetypes. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.AimDownSightSpeed.Marksman |
| `Meta.Role.Recon.AimDownSightSpeed.Sniper` | Time-to-ADS speed improvement (Sniper Rifle Archetype) | Reduces the time it takes to enter ADS, specifically with weapons within the 'sniper rifle' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.AimDownSightSpeed.Sniper |
| `Meta.Role.Recon.AimMoveSpeed.Marksman` | ADS movement speed improvement (Marksman Archetype) | Increases the speed a player can move whilst aiming down sights, specifically with weapons within the 'marksm… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.AimMoveSpeed.Marksman |
| `Meta.Role.Recon.AimMoveSpeed.Sniper` | ADS movement speed improvement (Sniper Rifle Archetype) | Increases the speed a player can move whilst aiming down sights, specifically with weapons within the 'sniper… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.AimMoveSpeed.Sniper |
| `Meta.Role.Recon.BoltActionRechamberSpeed` | Bolt action rechambering speed improvement | Reduces the time it takes to rechamber a bullet when using bolt action rifles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.BoltActionRechamberSpeed |
| `Meta.Role.Recon.ColdBlooded` | Infrared visibility reduction | Reduces how visible you are on enemies infrared sights when people are looking at you. (not completely invisi… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.ColdBlooded |
| `Meta.Role.Recon.FocusSteadyAimSpeed` | Focus-time steady aim speed improvement | Reduces the time it takes for the 'steady aim' effect to complete when you hold your breath with a weapon. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.FocusSteadyAimSpeed |
| `Meta.Role.Recon.HearNearbySquadChat` | Hear nearby squad chat | Unlocks the ability to eavesdrop nearby enemy squad chats. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.HearNearbySquadChat |
| `Meta.Role.Recon.HorizontalRecoil.Marksman` | Horizontal recoil reduction (Marksman Archetype) | Reduces the amount of horizontal recoil a player experiences when firing weapons within the 'marksman' archet… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.HorizontalRecoil.Marksman |
| `Meta.Role.Recon.HorizontalRecoil.Sniper` | Horizontal recoil reduction (Sniper Rifle Archetype) | Reduces the amount of horizontal recoil a player experiences when firing weapons within the 'sniper rifle' ar… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.HorizontalRecoil.Sniper |
| `Meta.Role.Recon.IncreasedSpottingDuration` | Increased 'enemy spotted' duration | Increases the duration that enemies remain spotted when you have personally spotted them. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.IncreasedSpottingDuration |
| `Meta.Role.Recon.IncreasedSpottedTime` | Increased time to be spotted | Increases the time it takes for you to be successfully spotted by an enemy player. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.IncreasedSpottedTime |
| `Meta.Role.Recon.IncreaseFocusDuration` | Increased focus-time duration | Increases the amount of time you are able to "hold breath" with a weapon before it runs out. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.IncreaseFocusDuration |
| `Meta.Role.Recon.Lockpicking` | Lockpicking | Unlock the ability to 'lockpick' enemy locked vehicles, buildables and fortifications. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.Lockpicking |
| `Meta.Role.Recon.MagnificationSpeed` | Magnification speed improvement | Reduces the time it takes to 'zoom in' on scopes that have magnification. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.MagnificationSpeed |
| `Meta.Role.Recon.QuieterInteractions` | Quieter interactions | Unlocks the ability to perform all interactions that make noise quieter. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.QuieterInteractions |
| `Meta.Role.Recon.ReadyToFireSpeed.Marksman` | Ready-to-fire speed improvement (Marksman Archetype) | Reduces the time it takes for your gun to come up after certain actions, specifically with weapons that fall … | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.ReadyToFireSpeed.Marksman |
| `Meta.Role.Recon.ReadyToFireSpeed.Sniper` | Ready-to-fire speed improvement (Sniper Rifle Archetype) | Reduces the time it takes for your weapon to come up after certain actions, specifically with weapons that fa… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.ReadyToFireSpeed.Sniper |
| `Meta.Role.Recon.ReduceFocus` | Reduced shooting penalty on focus-time (Sniper Rifle & Marksman Archetypes) | Reduces the amount of focus-time penalty the player experiences when they shoot their weapon whilst holding t… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.ReduceFocus |
| `Meta.Role.Recon.ReloadSpeed.Marksman` | Reload speed improvement (Marksman Archetype) | Reduces the time it takes to reload. Specifically with weapons within the 'marksman' archetypes. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.ReloadSpeed.Marksman |
| `Meta.Role.Recon.ReloadSpeed.Sniper` | Reload speed improvement (Sniper Rifle Archetype) | Reduces the time it takes to reload. Specifically with weapons within the 'sniper rifle' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.ReloadSpeed.Sniper |
| `Meta.Role.Recon.SniperKillFocusReset` | Sniper Rifle kill replenishes focus | Downing an enemy player with any weapon in the 'sniper rifle' platform with replenish your focus. (one time u… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.SniperKillFocusReset |
| `Meta.Role.Recon.SpotDeployables` | Spot enemy buildables & deployables | Unlock the ability to spot enemy buildables, fortifications and deployables. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.SpotDeployables |
| `Meta.Role.Recon.StealthMeleeDamage` | Increased melee damage from behind | Increases the amount of damage you do with melee attacks, specifically when you hit an enemy from behind. Thi… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.StealthMeleeDamage |
| `Meta.Role.Recon.VerticalRecoil.Marksman` | Vertical recoil reduction (Marksman Archetype) | Reduces the amount of vertical recoil a player experiences when firing weapons within the 'marksman' archetyp… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.VerticalRecoil.Marksman |
| `Meta.Role.Recon.VerticalRecoil.Sniper` | Vertical recoil reduction (Sniper Rifle Archetype) | Reduces the amount of vertical recoil a player experiences when firing weapons within the 'sniper rifle' arch… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.VerticalRecoil.Sniper |
| `Meta.Role.Recon.WeaponSwitchSpeed.Pistol` | Weapon-switch speed improvement (Sidearms Archetype). | Reduces the amount of time it takes to switch TO any weapons within the sidearm archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.WeaponSwitchSpeed.Pistol |
| `Meta.Role.Recon.WeaponSwitchSpeed.ReconWeaponry` | Weapon-switch speed improvement (Sniper Rifle & Marksman Archetypes) | Reduces the amount of time it takes to switch TO any weapons within the Sniper Rifle & Marksman archetypes. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Recon.WeaponSwitchSpeed.ReconWeaponry |
| `Meta.Role.Support.AimDownSightSpeed.LMG` | Time-to-ADS speed improvement (LMG Archetype) | Reduces the time it takes to enter ADS, specifically with weapons within the 'LMG' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.AimDownSightSpeed.LMG |
| `Meta.Role.Support.AimdownSightspeed.Shotgun` | Time-to-ADS speed improvement (Shotgun Archetype) | Reduces the time it takes to enter ADS, specifically with weapons within the 'shotgun' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.AimdownSightspeed.Shotgun |
| `Meta.Role.Support.AimMoveSpeed.LMG` | ADS movement speed improvement (LMG Archetype) | Increases the speed a player can move whilst aiming down sights, specifically with weapons within the 'LMG' a… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.AimMoveSpeed.LMG |
| `Meta.Role.Support.AimMoveSpeed.Shotgun` | ADS movement speed improvement (Shotgun Archetype) | Increases the speed a player can move whilst aiming down sights, specifically with weapons within the 'shotgu… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.AimMoveSpeed.Shotgun |
| `Meta.Role.Support.CombineMagSpeed` | Combining mags' speed improvement | Reduces the amount of time it takes to combine mags in your inventory. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.CombineMagSpeed |
| `Meta.Role.Support.DeploySpeed` | Equipment deployment speed improvement | Reduces the amount of time it takes to deploy deployable equipment. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.DeploySpeed |
| `Meta.Role.Support.GrenadeThrowback` | Throw back grenades | Unlocks the ability to pick up and throw back enemy grenades that have been thrown at you and have landed on … | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.GrenadeThrowback |
| `Meta.Role.Support.HorizontalRecoil.LMG` | Horizontal recoil reduction (LMG Archetype) | Reduces the amount of horizontal recoil a player experiences when firing weapons within the 'LMG' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.HorizontalRecoil.LMG |
| `Meta.Role.Support.HorizontalRecoil.Shotgun` | Horizontal recoil reduction (Shotgun Archetype) | Reduces the amount of horizontal recoil a player experiences when firing weapons within the 'shotgun' archety… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.HorizontalRecoil.Shotgun |
| `Meta.Role.Support.IncreadedDetonatorRange` | Increased detonator range | Unlocks Increased effective range of the C4's detonator. (Can detonate C4s from further away). This is a one … | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.IncreadedDetonatorRange |
| `Meta.Role.Support.IncreasedDurability.Buildables` | Increased buildables durability | Increases the amount of damage it takes to destroy buildables that YOU have built. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.IncreasedDurability.Buildables |
| `Meta.Role.Support.IncreasedDurability.RepairTool` | Increased repair tool durability | Increases the amount of durability your repair tools have when you are using them. This should affect all rep… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.IncreasedDurability.RepairTool |
| `Meta.Role.Support.MediumHammerUpgrade` | Build anything with medium hammers | Unlocks the ability to build things with the medium hammer that you would normally need the heavy hammer to b… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.MediumHammerUpgrade |
| `Meta.Role.Support.ReadyToFireSpeed.LMG` | Ready-to-fire speed improvement (LMG Archetype) | Reduces the time it takes for your weapon to come up after certain actions, specifically with weapons that fa… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReadyToFireSpeed.LMG |
| `Meta.Role.Support.ReadyToFireSpeed.Shotgun` | Ready-to-fire speed improvement (Shotgun Archetype) | Reduces the time it takes for your weapon to come up after certain actions, specifically with weapons that fa… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReadyToFireSpeed.Shotgun |
| `Meta.Role.Support.ReduceExplosiveDamage.Teammate` | Explosives do less damage to teammates | Reduces the amount of damage that your explosives do to teammates. This includes explosives from launchers, g… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReduceExplosiveDamage.Teammate |
| `Meta.Role.Support.ReduceFocus` | Reduced shooting penalty on focus-time (LMG & Shotgun Archetypes) | Reduces the amount of focus-time penalty the player experiences when they shoot their weapon whilst holding t… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReduceFocus |
| `Meta.Role.Support.ReduceResourceUsage` | Less resource use per hit | Reduces the amount of resources that are used per hit of building. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReduceResourceUsage |
| `Meta.Role.Support.RefuelSpeed` | Refueling speed improvement | Reduces the time it takes to refuel vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.RefuelSpeed |
| `Meta.Role.Support.ReloadSpeed.Launcher` | Reload speed improvement (Launchers Archetype) | Reduces the amount of time it takes to reload weapons within the 'launcher' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReloadSpeed.Launcher |
| `Meta.Role.Support.ReloadSpeed.LMG` | Reload speed improvement ('LMG' Archetype) | Reduces the amount of time it takes to reload weapons within the 'LMG' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReloadSpeed.LMG |
| `Meta.Role.Support.ReloadSpeed.Shotgun` | Reload speed improvement (Shotgun Archetype) | Reduces the time it takes to reload. Specifically with weapons within the 'shotgun' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.ReloadSpeed.Shotgun |
| `Meta.Role.Support.RepairSpeed` | Repair speed improvement | Reduces the time it takes to repair damaged vehicles. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.RepairSpeed |
| `Meta.Role.Support.SmallHammerUpgrade` | Build anything with small hammers | Unlocks the ability to build things with the small hammer that you would normally need the medium or heavy ha… | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.SmallHammerUpgrade |
| `Meta.Role.Support.VerticalRecoil.LMG` | Vertical recoil reduction (LMG Archetype) | Reduces the amount of vertical recoil a player experiences when firing weapons within the 'LMG' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.VerticalRecoil.LMG |
| `Meta.Role.Support.VerticalRecoil.Shotgun` | Vertical recoil reduction (Shotgun Archetype) | Reduces the amount of vertical recoil a player experiences when firing weapons within the 'shotgun' archetype. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.VerticalRecoil.Shotgun |
| `Meta.Role.Support.WeaponSwitchSpeed` | Weapon-switch speed improvement (LMG & Shotgun Archetypes) | Reduces the amount of time it takes to switch TO any weapons within the LMG and shotgun archetypes. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Support.WeaponSwitchSpeed |
| `Meta.Role.Infantry.StrongArm` | Increased grenade throw strength | Increase throw strength when throwing grenades, allowing for a higher potential maximum distance. | T_UI_Icon_Grenade | Meta.Role.Infantry.StrongArm |
| `Meta.Role.Infantry.WeightPenalty` | Reduced weight-related movement penalty | Reduces the amount that movement is negatively affected by inventory weight. | T_UI_Icon_GameMode_PlayerCount_White_256 | Meta.Role.Infantry.WeightPenalty |
| `Meta.Role.Infantry.MeleeDamage` | Melee damage increase | Increase the damage dealt by the player's melee attacks. This includes fists, melee weapons and weapon 'bashi… | T_UI_Icon_Killfeed_MeleeFist | Meta.Role.Infantry.MeleeDamage |
| `Meta.Role.Infantry.MeleeSpeed` | Melee speed improvement | Reduce the time it takes for players to complete a melee attack. This includes fists, melee weapons and weapo… | T_UI_Icon_Killfeed_MeleeFist | Meta.Role.Infantry.MeleeSpeed |
| `Meta.Role.Infantry.SprintBreach` | Sprint-breach through doors | Unlocks the ability to bash through doors by sprinting into them. | T_UI_Frontend_WDLogo_Icon | Meta.Role.Infantry.SprintBreach |
| `Meta.Role.Infantry.ReducedFocus` | Reduced effect of received damage on focus-reduction | Reduces the effect that receiving damage has on your focus-time. | T_KillfeedIcon | Meta.Role.Infantry.ReducedFocus |
| `Meta.Role.Infantry.FlakJacket` | Reduced suppresion effect | Reduces the severity of the suppresion effect experienced when under fire / near an explosion. | T_Placeholder_Icon_Vest1 | Meta.Role.Infantry.FlakJacket |
| `Meta.Role.Infantry.ReturnToFireSpeed.AssaultRifle` | Ready-to-fire speed improvement (Assault Archetype) | Reduces the time it takes for your gun to come up after certain actions, specifically with weapons that fall … | T_Placeholder_Icon_Weapon_AK | Meta.Role.Infantry.ReturnToFireSpeed.AssaultRifle |
| `Meta.Role.Infantry.AimMoveSpeed.AssaultRifle` | ADS movement speed improvement (Assault Archetype) | Increases the speed a player can move whilst aiming down sights, specifically with weapons within the 'assaul… | T_Placeholder_Icon_Weapon_AK | Meta.Role.Infantry.AimMoveSpeed.AssaultRifle |
| `Meta.Role.Infantry.HorizontalRecoil.AssaultRifle` | Horizontal recoil reduction (Assault Archetype) | Reduces the amount of horizontal recoil a player experiences when firing weapons within the 'assault' archety… | T_Placeholder_Icon_Weapon_AK | Meta.Role.Infantry.HorizontalRecoil.AssaultRifle |
| `Meta.Role.Infantry.VerticalRecoil.AssaultRifle` | Vertical recoil reduction (Assault Archetype) | Reduces the amount of vertical recoil a player experiences when firing weapons under the 'assault' archetype. | T_Placeholder_Icon_Weapon_AK | Meta.Role.Infantry.VerticalRecoil.AssaultRifle |
| `Meta.Role.Infantry.AimDownSightSpeed.AssaultRifle` | Time-to-ADS speed improvement (Assault Archetype) | Reduces the time it takes to enter ADS, specifically with weapons within the 'assault' archetype. | T_Placeholder_Icon_Weapon_AK | Meta.Role.Infantry.AimDownSightSpeed.AssaultRifle |
| `Meta.Role.Infantry.ReloadSpeed.AssaultRifle` | Reload Speed Improvement (Assault Archetype) | Reduces the time it takes to reload. Specifically with weapons within the 'assault' archetype. | T_Placeholder_Icon_Weapon_AK | Meta.Role.Infantry.ReloadSpeed.AssaultRifle |
| `Meta.Role.Infantry.BreathHoldImpact` | Reduced shooting penalty on focus-time (Assault & SMG Archetypes) | Reduces the amount of focus-time penalty the player experiences when they shoot their weapon whilst holding t… | T_KillfeedIcon | Meta.Role.Infantry.BreathHoldImpact |
| `Meta.Role.Infantry.WeaponSwitchSpeed` | Weapon-switch speed improvement (Assault & SMG Archetypes) | Reduces the amount of time it takes to switch TO any weapon in the assault & SMG archetypes. | T_UI_Icon_GunsmithLogo | Meta.Role.Infantry.WeaponSwitchSpeed |
| `Meta.Role.Infantry.HorizontalRecoil.SMG` | Horizontal recoil reduction (SMG Archetype) | Reduces the amount of horizontal recoil a player experiences when firing weapons within the 'SMG' archetypes. | T_Placeholder_Icon_Weapon_MP7 | Meta.Role.Infantry.HorizontalRecoil.SMG |
| `Meta.Role.Infantry.VerticalRecoil.SMG` | Vertical recoil reduction (SMG Archetype) | Reduces the amount of vertical recoil a player experiences when firing weapons under the 'SMG' archetypes. | T_Placeholder_Icon_Weapon_MP7 | Meta.Role.Infantry.VerticalRecoil.SMG |
| `Meta.Role.Infantry.AimDownSightSpeed.SMG` | Time-to-ADS speed improvement (SMG Archetype) | Reduces the time it takes to enter ADS, specifically with weapons within the 'SMG' archetypes. | T_Placeholder_Icon_Weapon_MP7 | Meta.Role.Infantry.AimDownSightSpeed.SMG |
| `Meta.Role.Infantry.ReloadSpeed.SMG` | Reload Speed Improvement (SMG Archetype) | Reduces the time it takes to reload. Specifically with weapons within the 'SMG' archetypes. | T_Placeholder_Icon_Weapon_MP7 | Meta.Role.Infantry.ReloadSpeed.SMG |
| `Meta.Role.Infantry.ReturnToFireSpeed.SMG` | Ready-to-fire speed improvement (SMG Archetype) | Reduces the time it takes for your gun to come up after certain actions, specifically with weapons that fall … | T_Placeholder_Icon_Weapon_MP7 | Meta.Role.Infantry.ReturnToFireSpeed.SMG |
| `Meta.Role.Infantry.AimMoveSpeed.SMG` | ADS movement speed improvement (SMG Archetype) | Increases the speed a player can move whilst aiming down sights, specifically with weapons within the 'SMG' a… | T_Placeholder_Icon_Weapon_MP7 | Meta.Role.Infantry.AimMoveSpeed.SMG |
| `Meta.Role.Infantry.SlideDownLadders` | Fast-descend down ladders | Unlocks the ability to quickly descend ladders by sliding down them. | T_UI_Frontend_WDLogo_Icon | Meta.Role.Infantry.SlideDownLadders |
| `Meta.Role.Infantry.UnarmedSprintSpeed` | Unarmed sprint speed improvement | Increases the speed a player sprints when they have their fists out. | T_UI_Icon_Weapon_FIST_Textured_512x512 | Meta.Role.Infantry.UnarmedSprintSpeed |
| `Meta.Role.Infantry.TacticalSprintRecovery` | Tac-sprint recovery time improvement | Reduces the time it takes to recover tac-sprint stamina. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Infantry.TacticalSprintRecovery |
| `Meta.Role.Infantry.FasterVault` | Faster vault speed | Reduces the time it takes to perform vaults at all heights. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Infantry.FasterVault |
| `Meta.Role.Infantry.CovertStaminaRegen` | Faster Tac-sprint stamina regen whilst crouched/proned | Tac-sprint stamina recovery is faster when player is crouched or proned. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Infantry.CovertStaminaRegen |
| `Meta.Role.Infantry.TacticalSprintDuration` | Tac-sprint duration | Increased duration of tac-sprint before it runs out. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Infantry.TacticalSprintDuration |
| `Meta.Role.Infantry.TacticalSwimDuration` | Tac-swim duration | Increased duration of tac-swimming before it runs out. | T_UI_Icon_Killfeed_Roadkill | Meta.Role.Infantry.TacticalSwimDuration |
| `Meta.Role.Infantry.CovertMovementSpeed` | Crouch/prone movement speed improvements | Increases the base speed a player moves when they are in crouch & prone. | T_UI_Icon_Placeholder_Supplier | Meta.Role.Infantry.CovertMovementSpeed |
<!-- /datatable_catalog -->

## WDMetaTreeTableRow

Tables: [`DT_MetaTree_Roles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDMetaTreeTableRow -->
*1 table(s), 7 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Nodes` | `Tag` |
|---|---|---|
| `Meta.Role.Driver` | {ID=Vehicle.Variant.Land.Wheeled.Ural.Default; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaC… | Meta.Role.Driver |
| `Meta.Role.Infantry` | {ID=Id.Item.MUZL_039; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaClass=WDMetaPrerequisiteSc… | Meta.Role.Infantry |
| `Meta.Role.Medic` | {ID=Id.Item.MUZL_037; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaClass=WDMetaPrerequisiteSc… | Meta.Role.Medic |
| `Meta.Role.Pilot` | {ID=ID.Item.VehicleSupplyCrate.Small.Armoured; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaC… | Meta.Role.Pilot |
| `Meta.Role.Recon` | {ID=ID.Item.Monocular; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaClass=WDMetaPrerequisiteS… | Meta.Role.Recon |
| `Meta.Role.Support` | {ID=ID.Item.RepairTool.Drill.Light; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaClass=WDMeta… | Meta.Role.Support |
| `Meta.Role.Wardog` | {ID=Id.Item.Judge; LevelsData={Prerequisites.QueryDefinition.StaticStruct.SchemaClass=WDMetaPrerequisiteSchem… | Meta.Role.Wardog |
<!-- /datatable_catalog -->

## WDMetaMasteryDefinitionTableRow

Tables: [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDMetaMasteryDefinitionTableRow -->
*1 table(s), 6 rows, 3 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `ResourceTag` | `LevelDefinitions` | `Tag` |
|---|---|---|---|
| `Meta.Role.Driver` | Attribute.Meta.XP.Role.Driver | {Level=0; XP=0}, {Level=1; XP=200}, {Level=2; XP=750}, {Level=3; XP=1250}, {Level=4; XP=3000}, {Level=5; XP=6… | Meta.Role.Driver |
| `Meta.Role.Infantry` | Attribute.Meta.XP.Role.Infantry | {Level=0; XP=0}, {Level=1; XP=200}, {Level=2; XP=750}, {Level=3; XP=1250}, {Level=4; XP=3000}, {Level=5; XP=6… | Meta.Role.Infantry |
| `Meta.Role.Medic` | Attribute.Meta.XP.Role.Medic | {Level=0; XP=0}, {Level=1; XP=200}, {Level=2; XP=750}, {Level=3; XP=1250}, {Level=4; XP=3000}, {Level=5; XP=6… | Meta.Role.Medic |
| `Meta.Role.Pilot` | Attribute.Meta.XP.Role.Pilot | {Level=0; XP=0}, {Level=1; XP=200}, {Level=2; XP=750}, {Level=3; XP=1250}, {Level=4; XP=3000}, {Level=5; XP=6… | Meta.Role.Pilot |
| `Meta.Role.Recon` | Attribute.Meta.XP.Role.Recon | {Level=0; XP=0}, {Level=1; XP=200}, {Level=2; XP=750}, {Level=3; XP=1250}, {Level=4; XP=3000}, {Level=5; XP=6… | Meta.Role.Recon |
| `Meta.Role.Support` | Attribute.Meta.XP.Role.Support | {Level=0; XP=0}, {Level=1; XP=200}, {Level=2; XP=750}, {Level=3; XP=1250}, {Level=4; XP=3000}, {Level=5; XP=6… | Meta.Role.Support |
<!-- /datatable_catalog -->

## WDMetaSeasonDefinitionTableRow

Tables: [`DT_SeasonDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/DT_SeasonDefinitions.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDMetaSeasonDefinitionTableRow -->
*1 table(s), 1 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `CurrentSeasonNumber` | `Tag` |
|---|---|---|
| `Meta.Season.Definitions` | 1 | Meta.Season.Definitions |
<!-- /datatable_catalog -->

## WDCosmeticSetData

Tables: [`DT_CosmeticSets_Debug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Cosmetics/DT_CosmeticSets_Debug.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDCosmeticSetData -->
*1 table(s), 12 rows, 5 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `Name` | `UITextures.FallbackIcon` | `bHideInCollection` | `SortIndex` | `Tag` |
|---|---|---|---|---|---|
| `Meta.Cosmetic.Featured` | Featured | T_UI_Generic_BG | false | 0 | Meta.Cosmetic.Featured |
| `Meta.Cosmetic.BlackAndGold` | Black & Gold | T_UI_BlackAndGold_BG | false | 1 | Meta.Cosmetic.BlackAndGold |
| `Meta.Cosmetic.Frogman` | Frogman | T_UI_Generic_BG | false | 2 | Meta.Cosmetic.Frogman |
| `Meta.Cosmetic.DigitalWood` | Digital Wood | T_UI_DigitalWood_BG | false | 3 | Meta.Cosmetic.DigitalWood |
| `Meta.Cosmetic.TripleDesert` | Triple Desert | T_UI_Quality | false | 4 | Meta.Cosmetic.TripleDesert |
| `Meta.Cosmetic.DigitalFlora` | Digital Flora | T_UI_Generic_BG | false | 5 | Meta.Cosmetic.DigitalFlora |
| `Meta.Cosmetic.TwoToneDesert` | Two Tone Desert | T_UI_TwoToneDesert_BG | false | 6 | Meta.Cosmetic.TwoToneDesert |
| `Meta.Cosmetic.Emote` | Emotes | T_UI_Generic_BG | true | 8 | Meta.Cosmetic.Emote |
| `Meta.Cosmetic.Bobblehead` | Bobbleheads | T_UI_Generic_BG | false | 9 | Meta.Cosmetic.Bobblehead |
| `Meta.Cosmetic.Taxi` | Taxi | T_UI_Generic_BG | false | 10 | Meta.Cosmetic.Taxi |
| `Meta.Cosmetic.FactionLogo` | Faction Logo | T_UI_Generic_BG | false | 11 | Meta.Cosmetic.FactionLogo |
| `Meta.Cosmetic.ChocolateChip` | Chocolate Chip | T_UI_Generic_BG | false | 7 | Meta.Cosmetic.ChocolateChip |
<!-- /datatable_catalog -->

## WDEmoteData

Tables: [`DT_EmoteData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Character/DT_EmoteData.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDEmoteData -->
*1 table(s), 27 rows, 8 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 8:

| Row | `_aaaakmaiagceginhpgeoe` | `_aaaamcjgaokphjebecjic` | `PlayRate` | `bHolsterWeapon` | `_aaabgjmmjbmjfbncaafch` | `_aaabjdgjapjmbgmpamikg` | `_aaabelpijohgmmanaeoif` |
|---|---|---|---|---|---|---|---|
| `Action.Player.Emote.Bowman` | false | false | 1.15 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Come_Here` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Assault` | false | false | 1.1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Chefs_Kiss` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Move_Up` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Point` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.RPS` | false | false | 1.1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Surrender_Drop` | true | false | 1 | false | false | false |  |
| `Action.Player.Emote.ThumbsUp` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Wave` | false | false | 1.2 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Face_Palm` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Finger_Gun` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Follow_Me` | false | false | 0.95 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Halt` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Middle_Finger` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.OK` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Paper` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Rock` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Salute` | true | true | 1 | true | true | false |  |
| `Action.Player.Emote.Scissors` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Shh` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Sit_Down` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Sitting` | true | true | 1 | true | true | false |  |
| `Action.Player.Emote.Slow_Down` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Stop` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.Throat_Slit` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |
| `Action.Player.Emote.ThumbsDown` | false | false | 1 | false | false | true | Id.Item.Fists, Id.Item.TAR21, Id.Item.M4, Id.Item.WEPN_033, Id.Item.KH2002, Id.Item.WEPN_030 (+56 more) |

Columns 8-8 of 8:

| Row | `Tag` |
|---|---|
| `Action.Player.Emote.Bowman` | Action.Player.Emote.Bowman |
| `Action.Player.Emote.Come_Here` | Action.Player.Emote.Come_Here |
| `Action.Player.Emote.Assault` | Action.Player.Emote.Assault |
| `Action.Player.Emote.Chefs_Kiss` | Action.Player.Emote.Chefs_Kiss |
| `Action.Player.Emote.Move_Up` | Action.Player.Emote.Move_Up |
| `Action.Player.Emote.Point` | Action.Player.Emote.Point |
| `Action.Player.Emote.RPS` | Action.Player.Emote.RPS |
| `Action.Player.Emote.Surrender_Drop` | Action.Player.Emote.Surrender_Drop |
| `Action.Player.Emote.ThumbsUp` | Action.Player.Emote.ThumbsUp |
| `Action.Player.Emote.Wave` | Action.Player.Emote.Wave |
| `Action.Player.Emote.Face_Palm` | Action.Player.Emote.Face_Palm |
| `Action.Player.Emote.Finger_Gun` | Action.Player.Emote.Finger_Gun |
| `Action.Player.Emote.Follow_Me` | Action.Player.Emote.Follow_Me |
| `Action.Player.Emote.Halt` | Action.Player.Emote.Halt |
| `Action.Player.Emote.Middle_Finger` | Action.Player.Emote.Middle_Finger |
| `Action.Player.Emote.OK` | Action.Player.Emote.OK |
| `Action.Player.Emote.Paper` | Action.Player.Emote.Paper |
| `Action.Player.Emote.Rock` | Action.Player.Emote.Rock |
| `Action.Player.Emote.Salute` | Action.Player.Emote.Salute |
| `Action.Player.Emote.Scissors` | Action.Player.Emote.Scissors |
| `Action.Player.Emote.Shh` | Action.Player.Emote.Shh |
| `Action.Player.Emote.Sit_Down` | Action.Player.Emote.Sit_Down |
| `Action.Player.Emote.Sitting` | Action.Player.Emote.Sitting |
| `Action.Player.Emote.Slow_Down` | Action.Player.Emote.Slow_Down |
| `Action.Player.Emote.Stop` | Action.Player.Emote.Stop |
| `Action.Player.Emote.Throat_Slit` | Action.Player.Emote.Throat_Slit |
| `Action.Player.Emote.ThumbsDown` | Action.Player.Emote.ThumbsDown |
<!-- /datatable_catalog -->

## WDPlayerIdentityRow

Tables: [`DT_PlayerIdentities`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_PlayerIdentities.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDPlayerIdentityRow -->
*1 table(s), 5 rows, 9 non-empty columns. Source: the `Rows` of each table export (**Data**).*

Columns 1-7 of 9:

| Row | `DisplayName` | `Priority` | `_aaaancbloodmkealjoiop` | `_aaaamkihpmjajnpfjbpfh` | `_aaaaoddiblkfcomabbebl` | `_aaaapjfdfpekdnohlpcal` | `TaggedIcons.FallbackIcon` |
|---|---|---|---|---|---|---|---|
| `Player.Identity.CommunityDev` | Community Developer | 0 | true | Dev Impersonator | None |  | T_UI_BHlogo_128 |
| `Player.Identity.VIP` | VIP | 1 | true | VIP Impersonator | None |  | T_UI_ServerBrowser_Checkmark |
| `Player.Identity.ETP` | ETP | 2 | false |  | None |  | T_UI_EPTIcon |
| `Player.Identity.EASupporter` | Early Access Supporter | 3 | false |  | Entitlement | Player.Identity.EASupporter | T_UI_Icon_SupporterBadge |
| `Player.Identity.EarlyAdopter` | Early Adopter | 4 | false |  | Entitlement | Player.Identity.EarlyAdopter | T_UI_Icon_TwitchBadgeViewer |

Columns 8-9 of 9:

| Row | `TaggedIcons.TaggedIcons` | `Tag` |
|---|---|---|
| `Player.Identity.CommunityDev` | {Key=/Game/UI/Features/Scoreboard/Textures/T_UI_BHlogo_128.T_UI_BHlogo_128; Value=UI.Icon.Scoreboard} | Player.Identity.CommunityDev |
| `Player.Identity.VIP` | {Key=/Game/UI/Shared/Icons/Frontend/T_UI_ServerBrowser_Checkmark.T_UI_ServerBrowser_Checkmark; Value=UI.Icon.… | Player.Identity.VIP |
| `Player.Identity.ETP` | {Key=/Game/UI/Features/Scoreboard/Textures/T_UI_EPTIcon.T_UI_EPTIcon; Value=UI.Icon.Scoreboard} | Player.Identity.ETP |
| `Player.Identity.EASupporter` | {Key=/Game/UI/Shared/Icons/Frontend/T_UI_Icon_SupporterBadge.T_UI_Icon_SupporterBadge; Value=UI.Icon.Scoreboa… | Player.Identity.EASupporter |
| `Player.Identity.EarlyAdopter` | {Key=/Game/UI/Features/Scoreboard/Textures/T_UI_Icon_TwitchBadgeViewer.T_UI_Icon_TwitchBadgeViewer; Value=UI.… | Player.Identity.EarlyAdopter |
<!-- /datatable_catalog -->

## WDFactionDataTableRow

Tables: [`DT_FactionData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_FactionData.json). Each name is linked in the [index](Wardogs_DataTables_v1.md).

<!-- datatable_catalog struct WDFactionDataTableRow -->
*1 table(s), 4 rows, 2 non-empty columns. Source: the `Rows` of each table export (**Data**).*

| Row | `FactionData` | `Tag` |
|---|---|---|
| `Meta.Alignment.Faction.Default` | Meta_Alignment_Faction_Default | Meta.Alignment.Faction.Default |
| `Meta.Alignment.Faction.Alpha` | Meta_Alignment_Faction_Alpha | Meta.Alignment.Faction.Alpha |
| `Meta.Alignment.Faction.Bravo` | Meta_Alignment_Faction_Bravo | Meta.Alignment.Faction.Bravo |
| `Meta.Alignment.Faction.Charlie` | Meta_Alignment_Faction_Charlie | Meta.Alignment.Faction.Charlie |
<!-- /datatable_catalog -->
