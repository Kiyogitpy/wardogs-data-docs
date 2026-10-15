# Wardogs: GameFeatures Items Reference (v2)
*Source: exported JSON under `Wardogs/Plugins/GameFeatures/Items` (495 files, 24 item folders). Numbers are read from the export; anything not confirmed is marked as unclear.*

> **Scope note:** this covers the Items plugin only. Firearms, vehicles and the global reward/economy tables live in other plugins or Content folders and are not in this doc.

---

## 1. Layout and File Counts

Export `Type` counts across all 495 files:

| Export Type | Files | What it holds |
|---|---|---|
| DataTable | 84 | Row tables: entity UI, vendor, buildable, damage, tracker, skill, UI |
| WDAudioData | 46 | Audio event bundles (not decoded) |
| CrosstalkAudioEvent | 42 | Crosstalk/voice events (not decoded) |
| BHInventoryFragment_CustomShape | 39 | Inventory grid footprint (section 7) |
| BHActionDefinition | 32 | Use/input actions (section 5) |
| WDActorBuildSpawner | 30 | Buildable spawn class (section 6.2) |
| BHAnimationSet | 29 | Animation sets (not decoded) |
| BuildingStagesDefinition | 29 | Per-stage build geometry (section 6.2) |
| GameFeatureAction_AddWorldPartitionContent | 22 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIRadialWheelSlotTypeDataAsset | 20 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHInventoryFragment_Droppable | 16 | World-item mesh for dropped items |
| AEB_AttachSoundToHeldItem_C | 8 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHPlayerMappableKeySettings | 6 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_PlayHeldItemPerspectiveSound_C | 5 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| CurveFloat | 5 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_PrototypeMaskedScopes_ExtensionData_C | 4 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDActionDefinition | 4 | Movement, interaction and vehicle actions (section 5) |
| AEB_Play_Buildable_Sound_C | 4 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| GameFeatureAction_DataRegistrySource | 3 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDProjectileData | 3 | Projectile stats (section 4) |
| BHDestructionBuildingDefinitionDataAsset | 3 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIMaterialTrackerDataAsset | 3 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| GameFeatureAction_AddComponents | 3 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_VehicleRepairToolExtensionData_C | 3 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHGameFeatureAction_AddGameplayCuePath | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHDestructionBuildingDecoratorDefinitionDataAsset | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_AttachSoundToVehicle_C | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIContainerGridData | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIItemCardData_Inventory | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIMapTrackerData | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_C4_Data_C | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_FuelCan_ExtensionData_C | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| GameFeatureData | 2 | GFD shells with no properties exported (Injector, Landmine) |
| WDUIDeployableMapTrackerData | 2 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_AT_MineExtensionData_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHInventoryFragment_Stackable | 1 | Stack size (section 7) |
| WDBuildablePlacementDataAsset | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHSignificanceSettingsAsset | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHSignificanceEvaluator_Sphere | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIBuildablePlacementData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_SetBuildableDamageValue_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDFobInteractionDataAsset | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDFOBRulesetData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_SetFOBStateParameters_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIBuildToolRadialWheelData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIBuildToolData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIContainerGridSlotData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIInventoryComponentData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIFobSupplyTooltipEntryData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIFobTooltipData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIFobMapTrackerData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIBuildableSpatialTrackerData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIFobRefuelRepairData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_ClaymoreExtensionData_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDWeaponStatsData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| B_DefaultWeaponInputData_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| B_CharacterModifier_IgnoreLookInput_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_Defibrillator_WattsExtensionData_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| InputMappingContext | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BH_ExtensionData_MedicalPrompts_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_PlayPerspectiveSound_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_SetSmokeGrenadeDuration_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDUIDeployableSpatialTrackerData | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| WDCameraModifier_StimulantEffects | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| BHGameFeatureAction_AddInputContextMapping | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |
| AEB_SetVehicleRepairParameters_C | 1 | Other: UI, audio, input, curves, Blueprint actions or world-partition hooks (section 11) |

Files per item folder:

| Folder | Files | Folder | Files |
|---|---|---|---|
| AT_mine | 9 | IED | 15 |
| Armor | 15 | Injector | 1 |
| Battery | 8 | Keycard | 15 |
| Binoculars | 7 | Landmine | 1 |
| Buildables | 203 | MedKit | 9 |
| C4 | 16 | MusicTapes | 46 |
| Claymore | 8 | PrototypeMaskedScopes | 2 |
| CombatBow | 27 | RangeFinder | 11 |
| Crowbar | 17 | SmokeGrenade | 20 |
| Defibrillator | 14 | SpotterScope | 1 |
| Enox | 11 | StimPen | 10 |
| FuelCanister | 10 | VehicleRepairTool | 19 |

---

## 2. Item Roster (Display Names and Tags)

From the 104 rows of the `BHEntityData_UI` tables. These rows give the player-facing name for each tag. A category of `None` (as exported) marks buildables, interaction contexts or UI-only entries.

| Folder | Row tag | Display name | Category |
|---|---|---|---|
| Armor | Id.Item.LightArmor | Level 1 Armor | Item.Category.Armor |
| Armor | Id.Item.MediumArmor | Level 2 Armor | Item.Category.Armor |
| Armor | Id.Item.HeavyArmor | Level 3 Armor | Item.Category.Armor |
| Armor | Id.Item.SuperHeavyArmor | Level 4 Armor | Item.Category.Armor |
| Armor | Id.Item.LightHelmet | Level 1 Helmet | Item.Category.Armor |
| Armor | Id.Item.MediumHelmet | Level 2 Helmet | Item.Category.Armor |
| Armor | Id.Item.HeavyHelmet | Level 3 Helmet | Item.Category.Armor |
| Armor | Id.Item.SuperHeavyHelmet | Level 4 Helmet | Item.Category.Armor |
| Armor | Id.Item.ARMR_005 | Flak Jacket | Item.Category.Armor |
| Armor | Id.Item.HELM_005 | Level 4 Helmet | Item.Category.Armor |
| Armor | Id.Item.GhillieArmor | Ghillie Body Suit | Item.Category.Armor |
| Armor | Id.Item.GhillieHelmet | Ghillie Headwear | Item.Category.Armor |
| Armor | Id.Item.GhillieArmor.Dead | Ghillie Body Suit (Dead) | Item.Category.Armor |
| Armor | Id.Item.GhillieHelmet.Dead | Ghillie Headwear (Dead) | Item.Category.Armor |
| AT_mine | ID.Item.ATMine | AT Mine | Item.Category.Deployable |
| Battery | Id.Item.LargeBattery | High Capacity Battery | Item.Category.Ammunition |
| Battery | Id.Item.Battery | Battery | Item.Category.Ammunition |
| Binoculars | ID.Item.Binoculars | Binoculars | None |
| Buildables | ID.Item.BuildTool.Hammer.Large | Large Hammer | Item.Category.Deployable |
| Buildables | ID.Item.BuildTool.Hammer.Medium | Medium Hammer | Item.Category.Deployable |
| Buildables | ID.Item.BuildTool.Hammer.Small | Small Hammer | Item.Category.Deployable |
| Buildables | Id.Item.MunitionsSupplies | Ammo Supplies | Item.Category.Ammunition |
| Buildables | Id.Item.FOB | Forward Operating Base | Item.Category.Deployable |
| Buildables | Id.Item.BuildToolSupply | Build Supplies | Item.Category.Ammunition |
| Buildables | Id.Item.FuelSupplies | Fuel Supplies | Item.Category.Ammunition |
| Buildables | Id.Item.SparePartsSupplies | Mechanical Supplies | Item.Category.Ammunition |
| Buildables | Id.Buildable.RefuelStation | Refuel Station | None |
| Buildables | Id.Buildable.RepairStation | Repair Station | None |
| Buildables | ID.Item.DPLY_001 | Drill Rig | None |
| Buildables | ID.Item.DPLY_002 | Mortars | None |
| Buildables | ID.Item.DPLY_003 | Repair Station | None |
| Buildables | Id.Buildable.BarbedWire | Barbed Wire | None |
| Buildables | Id.Buildable.BremmerWall | Bremer Wall | None |
| Buildables | Id.Buildable.CamoNetTent | Recon Tent | None |
| Buildables | Id.Buildable.Door | Door | None |
| Buildables | Id.Buildable.FOB | Forward Operating Base | None |
| Buildables | Id.Buildable.Gate | Gate | None |
| Buildables | Id.Buildable.HBlock | HBlock | None |
| Buildables | Id.Buildable.TallHBlock | HBlock | None |
| Buildables | Id.Buildable.HBlockQuadWall | HBlock | None |
| Buildables | Id.Buildable.LoudSpeaker | Loudspeaker | None |
| Buildables | Id.Buildable.MistralAA | Talon 9K-SAM | None |
| Buildables | Id.Buildable.Mortar | L81 Mortar | None |
| Buildables | Id.Buildable.Phalanx | Vanguard CIWS | None |
| Buildables | Id.Buildable.Radio | Builder's Radio | None |
| Buildables | Id.Buildable.SandbagWall | Sandbag Wall | None |
| Buildables | Id.Buildable.TankTrap | Hedgehog | None |
| Buildables | Id.Buildable.Bunker.Floor | Bunker | None |
| Buildables | Id.Buildable.Bunker.Roof | Bunker | None |
| Buildables | Id.Buildable.Bunker | Bunker | None |
| Buildables | Id.Buildable.CrowsNest | Recon Tower | None |
| Buildables | Id.Buildable.AirRaidShelter.Ceiling | Indirect Fire Shelter | None |
| Buildables | Id.Buildable.AirRaidShelter.Floor | Indirect Fire Shelter | None |
| Buildables | Id.Buildable.AirRaidShelter | Indirect Fire Shelter | None |
| C4 | Id.Item.C4Trigger | Remote Detonator | Item.Category.Throwable |
| C4 | Id.Item.C4Explosive | C4 Charge | Item.Category.Throwable |
| Claymore | Id.Item.Claymore | Claymore | Item.Category.Deployable |
| CombatBow | Id.Item.CombatBow | Compound Bow | Item.Category.Weapon.Ranged |
| CombatBow | Id.Item.Arrow | Broadhead Arrow | Item.Category.Ammunition |
| CombatBow | Id.Item.Arrow.Explosive | Rambo Explosive Arrow | Item.Category.Ammunition |
| Crowbar | Id.Item.Crowbar | Halligan Bar | Item.Category.Deployable |
| Defibrillator | Id.Item.Defibrillator.Standard | Defibrillator | Item.Category.Weapon |
| Enox | ID.Item.Enox.Standard | Enox | Item.Category.Health |
| Enox | Id.Item.Resuscitator.Cheap | Emergency Resuscitator | Item.Category.Health |
| Enox | Id.Item.Resuscitator.Standard | Field Resuscitator | Item.Category.Health |
| FuelCanister | Id.Item.FuelCan | 40L Fuel Canister | Item.Category.Deployable |
| IED | Id.Item.IED.Trigger | Improvised Explosive Device | Item.Category.Throwable |
| IED | Id.Item.IED.Explosive | Improvised Explosive Device | Item.Category.Throwable |
| Keycard | Id.Item.KeyCard.Alpha.1 | Alpha Card | Item.Keycard |
| Keycard | Id.Item.KeyCard.Alpha.2 | Alpha Card | Item.Keycard |
| Keycard | Id.Item.KeyCard.Bravo.1 | Bravo Card | Item.Keycard |
| Keycard | Id.Item.KeyCard.Bravo.2 | Bravo Card | Item.Keycard |
| Keycard | Id.Item.KeyCard.Charlie.1 | Charlie Card | Item.Keycard |
| Keycard | Id.Item.KeyCard.Charlie.2 | Charlie Card | Item.Keycard |
| MedKit | ID.Item.MedKit.Standard | Medical Bag | Item.Category.Health |
| RangeFinder | ID.Item.Monocular | Monocular | None |
| RangeFinder | ID.Item.RangeFinder | Range Finder | None |
| RangeFinder | ID.Item.InfraredRangeFinder | Infrared Range Finder | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Yellow | M18  Signal Grenade: Alert | None |
| SmokeGrenade | ID.Item.SmokeGrenade.White | M18 Smoke Grenade: White | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Red | M18  Signal Grenade: Hostile | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Blue | M18  Signal Grenade: Friendly | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Green | M18  Signal Grenade: Supply Request | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Black | M18 Smoke Grenade: Black | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Purple | M18  Signal Grenade: Landing Zone | None |
| SmokeGrenade | ID.Item.SmokeGrenade.Orange | M18  Signal Grenade: Damaged Vehicle | None |
| StimPen | Id.Item.StimPen | Adrenaline Pen | Item.Category.Health |
| VehicleRepairTool | ID.Item.RepairTool.Wrench.Standard | Wrench | None |
| VehicleRepairTool | ID.Item.RepairTool.Drill.Light | Light Drill | Item.Category.Weapon |
| VehicleRepairTool | ID.Item.RepairTool.Drill.Heavy | Heavy Drill | Item.Category.Weapon |

---

## 3. Vendor Prices

From `WDVendorData` rows (`DT_VendorData_Ext_*`). Every row has exactly one `VendorItemVariations` entry, so the price below is the only price for that item. `Qty` is the amount granted per purchase. `Level` is `LevelToUnlock` on the variation; its meaning is not confirmed (values are only 0 or 1). `Life limit` is `LifeTimeBuyLimit` (0 means no cap in the export).

| Row tag | Name | Price | Qty | Subcategory | Level | Life limit | Unlock items | Folder |
|---|---|---|---|---|---|---|---|---|
| Id.Item.LightArmor | Level 1 Armor | 400 | 1 | Gear.Armor | 0 | 0 | - | Armor |
| Id.Item.MediumArmor | Level 2 Armor | 1000 | 1 | Gear.Armor | 0 | 0 | - | Armor |
| Id.Item.HeavyArmor | Level 3 Armor | 2000 | 1 | Gear.Armor | 0 | 0 | - | Armor |
| Id.Item.SuperHeavyArmor | Level 4 Armor | 4000 | 1 | Gear.Armor | 0 | 0 | - | Armor |
| Id.Item.LightHelmet | Level 1 Helmet | 200 | 1 | Gear.Helmet | 0 | 0 | - | Armor |
| Id.Item.MediumHelmet | Level 2 Helmet | 500 | 1 | Gear.Helmet | 0 | 0 | - | Armor |
| Id.Item.HeavyHelmet | Level 3 Helmet | 1500 | 1 | Gear.Helmet | 0 | 0 | - | Armor |
| Id.Item.SuperHeavyHelmet | Level 4 Helmet | 3000 | 1 | Gear.Helmet | 0 | 0 | - | Armor |
| Id.Item.GhillieArmor | Ghillie Body Suit | 3000 | 1 | Gear.Camouflage | 0 | 0 | - | Armor |
| Id.Item.GhillieHelmet | Ghillie Headwear | 2500 | 1 | Gear.Camouflage | 0 | 0 | - | Armor |
| Id.Item.GhillieArmor.Dead | Ghillie Body Suit (Dead) | 3500 | 1 | Gear.Camouflage | 0 | 0 | - | Armor |
| Id.Item.GhillieHelmet.Dead | Ghillie Headwear (Dead) | 2800 | 1 | Gear.Camouflage | 0 | 0 | - | Armor |
| ID.Item.ATMine | AT Mine | 650 | 1 | Utility.Type.Offensive | 0 | 0 | - | AT_mine |
| Id.Item.Battery | Battery | 150 | 1 | Utility.Type.Misc | 1 | 0 | - | Battery |
| Id.Item.LargeBattery | High Capacity Battery | 300 | 1 | Utility.Type.Misc | 1 | 0 | - | Battery |
| ID.Item.Binoculars | Binoculars | 75 | 1 | Utility.Type.Recon | 0 | 0 | - | Binoculars |
| Id.Item.MunitionsSupplies | Ammo Supplies | 10 | 50 | Utility.Type.Building | 1 | 0 | - | Buildables |
| Id.Item.FOB | Forward Operating Base | 7500 | 1 | Utility.Type.Building | 0 | 0 | - | Buildables |
| ID.Item.BuildTool.Hammer.Large | Large Hammer | 2400 | 1 | Utility.Type.Building | 0 | 0 | - | Buildables |
| ID.Item.BuildTool.Hammer.Medium | Medium Hammer | 800 | 1 | Utility.Type.Building | 0 | 0 | - | Buildables |
| ID.Item.BuildTool.Hammer.Small | Small Hammer | 100 | 1 | Utility.Type.Building | 0 | 0 | - | Buildables |
| Id.Item.BuildToolSupply | Build Supplies | 10 | 50 | Utility.Type.Building | 1 | 0 | - | Buildables |
| Id.Item.FuelSupplies | Fuel Supplies | 10 | 50 | Utility.Type.Building | 1 | 0 | - | Buildables |
| Id.Item.SparePartsSupplies | Mechanical Supplies | 10 | 50 | Utility.Type.Building | 1 | 0 | - | Buildables |
| Id.Item.C4Explosive | C4 Charge | 250 | 1 | Utility.Type.Offensive | 0 | 0 | - | C4 |
| Id.Item.C4Trigger | Remote Detonator | 550 | 1 | Utility.Type.Offensive | 0 | 0 | - | C4 |
| Id.Item.Claymore | Claymore | 900 | 1 | Utility.Type.Offensive | 0 | 0 | - | Claymore |
| Id.Item.CombatBow | Compound Bow | 800 | 1 | Weapon.Type.Bow | 0 | 0 | - | CombatBow |
| Id.Item.Arrow | Broadhead Arrow | 75 | 5 | Utility.Type.Misc | 0 | 0 | - | CombatBow |
| Id.Item.Arrow.Explosive | Rambo Explosive Arrow | 150 | 1 | Utility.Type.Misc | 0 | 0 | - | CombatBow |
| Id.Item.Crowbar | Halligan Bar | 1100 | 1 | Utility.Type.Offensive | 0 | 0 | - | Crowbar |
| Id.Item.Defibrillator.Standard | Defibrillator | 1600 | 1 | Utility.Type.Medical | 0 | 0 | - | Defibrillator |
| ID.Item.Enox.Standard | Enox | 450 | 1 | Utility.Type.Medical | 0 | 0 | - | Enox |
| Id.Item.Resuscitator.Cheap | Emergency Resuscitator | 0 | 1 | Utility.Type.Medical | 0 | 1 | - | Enox |
| Id.Item.Resuscitator.Standard | Field Resuscitator | 500 | 1 | Utility.Type.Medical | 0 | 0 | - | Enox |
| Id.Item.FuelCan | 40L Fuel Canister | 150 | 1 | Utility.Type.Vehicle | 0 | 0 | - | FuelCanister |
| Id.Item.IED.Trigger | Improvised Explosive Device | 300 | 1 | Utility.Type.Offensive | 0 | 0 | - | IED |
| ID.Item.MedKit.Standard | Medical Bag | 2000 | 1 | Utility.Type.Medical | 0 | 0 | - | MedKit |
| Id.Item.MusicTape.01 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.02 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.03 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.04 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.05 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.06 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.07 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.08 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| Id.Item.MusicTape.09 | - | 100 | 1 | Vehicle.Music | 0 | 0 | - | MusicTapes |
| ID.Item.Monocular | Monocular | 150 | 1 | Utility.Type.Recon | 0 | 0 | - | RangeFinder |
| ID.Item.RangeFinder | Range Finder | 400 | 1 | Utility.Type.Recon | 0 | 0 | - | RangeFinder |
| ID.Item.InfraredRangeFinder | Infrared Range Finder | 1200 | 1 | Utility.Type.Recon | 0 | 0 | - | RangeFinder |
| Id.Item.SmokeGrenade.White | M18 Smoke Grenade: White | 100 | 1 | Utility.Type.Offensive | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Yellow | M18  Signal Grenade: Alert | 50 | 1 | Utility.Type.Offensive | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Red | M18  Signal Grenade: Hostile | 50 | 1 | Utility.Type.Offensive | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Blue | M18  Signal Grenade: Friendly | 50 | 1 | Utility.Type.Offensive | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Green | M18  Signal Grenade: Supply Request | 50 | 1 | Utility.Type.Building | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Black | M18 Smoke Grenade: Black | 100 | 1 | Utility.Type.Offensive | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Orange | M18  Signal Grenade: Damaged Vehicle | 50 | 1 | Utility.Type.Offensive | 0 | 0 | - | SmokeGrenade |
| ID.Item.SmokeGrenade.Purple | M18  Signal Grenade: Landing Zone | 50 | 1 | Utility.Type.Building | 0 | 0 | - | SmokeGrenade |
| Id.Item.StimPen | Adrenaline Pen | 250 | 1 | Utility.Type.Medical | 1 | 0 | - | StimPen |
| ID.Item.RepairTool.Wrench.Standard | Wrench | 150 | 1 | Utility.Type.Vehicle | 0 | 0 | - | VehicleRepairTool |
| ID.Item.RepairTool.Drill.Light | Light Drill | 600 | 1 | Utility.Type.Vehicle | 1 | 0 | - | VehicleRepairTool |
| ID.Item.RepairTool.Drill.Heavy | Heavy Drill | 1300 | 1 | Utility.Type.Vehicle | 1 | 0 | - | VehicleRepairTool |

Per-unit cost for multi-quantity rows: Arrow `75 / 5 = 15`, Munitions, Build, Fuel and Spare-part supplies `10 / 50 = 0.2`. Explosive Arrow `150 / 1 = 150`.

---

## 4. Projectiles

Only three `WDProjectileData` assets exist in this plugin. Values are the raw export numbers. Speed and dimension units are not labelled in the export; the Unreal default is cm and cm/s, but that is an assumption.

| Caliber tag | Asset | Damage tag | Base dmg | Expl. radius | Effective expl. radius | Typical speed | Lifetime (s) | Mass | Length | Diameter | Drag value / curve row | Penetrates | Ricochet angle (deg) | Base suppression | Whiz travel / player dist | Range mult. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Item.Caliber.BatteryCharge | DA_BatteryCharge_ProjectileData | Meta.Damage.Bullet.556mm | 40.0 | - | - | 43700.0 | - | 0.0041 | 1.2696 | 0.57 | 1.26 / G7 (Boat Tail) | - | - | 0.25 | 800.0 / 700.0 | - |
| Item.Caliber.Arrow | DA_Arrow_Combat_ProjectileData | Meta.Damage.Bullet.Arrow | 77.0 | - | - | 64200.0 | 30.0 | 0.025 | 80.0 | 0.4 | 1.8 / G7 (Boat Tail) | True | 30.0 | 0.6 | 1500.0 / 1200.0 | - |
| Item.Caliber.Arrow.Explosive | DA_Arrow_Explosive_ProjectileData | Meta.Damage.Bullet.Arrow.Explosive | 150.0 | 400.0 | 200.0 | 18000.0 | 20.0 | 0.045 | 75.0 | 0.85 | 10.0 / GC (Cylinder) | False | 50.0 | 0.5 | 1500.0 / 1200.0 | 0.75 |

The explosive arrow exports `bShouldPenetrate = False` and has no penetration multipliers, so its `-` cells are genuinely absent. Drag curve row is `G7 (Boat Tail)` on the battery round and the standard arrow, and `GC (Cylinder)` on the explosive arrow. `Range mult.` is only exported on the explosive arrow (`EffectiveRangeMultiplier = 0.75`).

---

## 5. Action Definitions

Each `BHActionDefinition` / `WDActionDefinition` binds an action tag to a Blueprint action class and a set of context tags. Context tags are shown without the `Action.Context.` prefix. `Base` is the definition class (`BH` or `WD`).

| Folder | Asset | Action tag | Action class | Base | Context tags |
|---|---|---|---|---|---|
| Binoculars | DA_Action_Binoculars_ADS | Action.Binoculars.ADS | B_Action_Binoculars_ADS_C | WD | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_BuildTool_Dismantle | Action.BuildTool.Dismantle | B_Action_BuildTool_Dismantle_C | BH | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_BuildTool_PlaceSchematic | Action.BuildTool.PlaceSchematic | B_Action_BuildTool_PlaceSchematic_C | BH | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_BuildTool_Rotate | Action.BuildTool.Rotate | B_Action_BuildTool_Rotate_C | BH | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_BuildTool_SecondaryUse | Action.BuildTool.SecondaryUse | B_Action_BuildTool_TogglePlacement_C | BH | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_BuildTool_ToggleSnapping | Action.BuildTool.ToggleSnapping | B_Action_BuildTool_ToggleSnapping_C | BH | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_Buildable_Construct | Action.BuildBuildable.Construct | B_Action_Buildable_Construct_C | BH | Holdable, Weapon, TwoHanded |
| Buildables | DA_Action_Buildable_Place | Action.FOBPlacement.PrimaryUse | B_Action_Buildable_Place_C | WD | Holdable, TwoHanded |
| C4 | DA_Action_C4_Throw | Action.Throw.Primary.C4 | B_Action_C4_Throw_C | BH | Holdable, Weapon, TwoHanded |
| C4 | DA_Action_Trigger_Primary | Action.Trigger.Primary | B_Action_Trigger_C | BH | Holdable, Weapon, TwoHanded |
| CombatBow | DA_Action_BowDraw | Action.Weapon.Bow.Draw | B_Action_BowDraw_C | BH | Holdable, OneHanded, Weapon.Fire |
| CombatBow | DA_Action_BowDryFire | Action.Weapon.Bow.DryRire | B_Action_BowDryFire_C | BH | Holdable, Weapon, TwoHanded |
| CombatBow | DA_Action_BowRelease | Action.Weapon.Bow.Release | B_Action_BowRelease_C | BH | Holdable, OneHanded |
| CombatBow | DA_Action_BowReload | Action.Weapon.Bow.Reload | B_Action_BowReload_C | BH | Holdable, Weapon, TwoHanded |
| CombatBow | DA_Action_CancelDraw | Action.Weapon.Bow.Cancel | B_Action_CancelDraw_C | BH | Holdable, Weapon, OneHanded |
| CombatBow | DA_Action_BowFire | Action.Weapon.Fire.Bow | B_Action_BowFireTestNew_C | BH | Holdable, OneHanded, Weapon.Fire |
| Crowbar | DA_Action_Crowbar | Action.Crowbar.PrimaryUse | B_Action_Crowbar_C | BH | Holdable, TwoHanded, Weapon |
| Crowbar | DA_Action_ForceOpenDoor | Action.Item.ForceOpenDoor | B_Action_ForceOpenDoor_C | BH | Interaction, TwoHanded |
| Crowbar | DA_Action_ForceUnlockVehicle | Action.Item.ForceUnlockVehicle | B_Action_ForceUnlockVehicle_C | BH | Interaction, TwoHanded |
| Defibrillator | DA_Action_Defibrillator | Action.Defibrillator.PrimaryUse | B_Action_Defibrillator_C | WD | Holdable, TwoHanded, Interaction |
| Defibrillator | DA_Action_Defibrillator_Reload | Action.Defibrillator.Reload | B_Action_Reload_C | BH | Holdable, Weapon, TwoHanded |
| Enox | DA_Action_Enox_SecondaryUse | Action.Appliable.Enox.SecondaryUse | B_Action_Enox_Use_C | BH | Holdable, TwoHanded |
| Enox | DA_Action_Resuscitator | Action.Appliable.Resuscitator.PrimaryUse | B_Action_Resuscitator_C | BH | Holdable, Interaction, TwoHanded |
| FuelCanister | DA_Action_FuelCan_ReFill | Action.Appliable.FuelCan.Fill | B_Action_FuelCan_ReFill_C | BH | Holdable, TwoHanded, Interaction |
| FuelCanister | DA_Action_FuelCan_Refuel | Action.Appliable.FuelCan.Refuel | B_Action_FuelCan_Refuel_C | BH | Holdable, TwoHanded, Interaction |
| IED | DA_Action_IED_Place | Action.Placeable.PrimaryUse.IED | B_Action_IED_Place_C | BH | Holdable, Weapon, TwoHanded |
| IED | DA_Action_IED_Trigger | Action.IED.Trigger | B_Action_IED_Trigger_C | BH | Holdable, TwoHanded |
| Keycard | DA_Action_KeyCard | Action.Keycard.Use | B_Action_Use_KeyCard_C | BH | Holdable, OneHanded |
| MedKit | DA_Action_MedKit_PrimaryUse | Action.MedKit.PrimaryUse | B_Action_MedKit_MultiUse_C | BH | Holdable, Interaction, TwoHanded |
| MedKit | DA_Action_MedKit_SecondaryUse | Action.Appliable.MedKit.SecondaryUse | B_Action_MedKit_SecondaryUse_C | BH | Holdable, Interaction, TwoHanded |
| RangeFinder | DA_Action_RangeFinder_ADS | Action.RangeFinder.ADS | B_Action_RangeFinder_ADS_C | WD | Holdable, Weapon, TwoHanded |
| StimPen | DA_Action_StimPen_PrimaryUse | Action.Appliable.StimPen.PrimaryUse | B_Action_StimPen_C | BH | Holdable, Interaction, TwoHanded |
| StimPen | DA_Action_StimPen_SecondaryUse | Action.Appliable.StimPen.SecondaryUse | B_Action_StimPen_C | BH | Holdable, TwoHanded |
| VehicleRepairTool | DA_Action_VehicleRepairTool | Action.VehicleRepairTool.PrimaryUse | B_Action_VehicleRepairTool_C | BH | Holdable, Interaction, TwoHanded |
| VehicleRepairTool | DA_Action_VehicleRepairTool_Continuous | Action.VehicleRepairTool.ContinuousUse | B_Action_VehicleRepairTool_Continuous_C | BH | Holdable, Interaction, TwoHanded |
| VehicleRepairTool | DA_Action_VehicleRepairTool_Reload | Action.VehicleRepairTool.Reload | B_Action_VehicleRepairTool_Reload_C | BH | Holdable, Weapon, TwoHanded |

---

## 6. Buildables

### 6.1 Build tools and what they can place

Each hammer is a `WDBuildableDataTableRow` table. A buildable can only be placed by a tool that lists it.

| Tool table | Count | Buildables |
|---|---|---|
| LargeHammer | 17 | CamoNetTent, TankTrap, BarbedWire, SandbagWall, Radio, HBlock, TallHBlock, Door, Gate, HBlockQuadWall, BremmerWall, Bunker, CrowsNest, AirRaidShelter, RefuelStation, RepairStation, HotzoneMagnet |
| MediumHammer | 10 | CamoNetTent, TankTrap, BarbedWire, SandbagWall, Radio, HBlock, TallHBlock, Door, Gate, HBlockQuadWall |
| SmallHammer | 6 | CamoNetTent, TankTrap, BarbedWire, SandbagWall, Radio, HBlock |

Vendor and inventory tie-in: Small Hammer `100` (2x1 footprint), Medium Hammer `800` (2x3), Large Hammer `2400` (4x2). The hammer tier is therefore a count of placeable buildables, not a separate build cost. The per-buildable material cost is not in this folder (see section 11).

### 6.2 Buildable geometry and build stages

`Progress` is `RequiredBuildingProgress` per stage. `Stage bbox` is the stage bounding box in export units (XY from `Max-Min`, Z height from `Max.Z-Min.Z`). The FOB has a spawner but no stages file here.

| Buildable folder | Spawner class | Stages | Progress per stage | Stage bbox (XY x Z) |
|---|---|---|---|---|
| AirRaidShelter | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 750.0 x 750.0 x 450.0 |
| BarbedWire | B_Buildable_BarbedWire_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 300.0 x 148.1 |
| BarrierDoor | B_BuildablePrefab_Door_Top_C | 1 | 1.0 | 150.0 x 150.0 x 10.0 |
| BremmerWall | B_Buildable_BremmerWall_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 150.0 x 509.2 |
| Bunker | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 600.0 x 600.0 x 300.0 |
| CamoNetTent | B_Buildable_CamoNetTent_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 231.6 x 417.7 x 97.3 |
| CrowsNest | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 600.0 x 600.0 x 760.0 |
| HBlock | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 150.0 x 150.0 |
| HBlock_Gate_6x2 | B_Buildable_Gate_Right_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 600.0 x 450.0 |
| HBlock_QuadWall | B_Buildable_HBlock_QuadWall_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 600.0 x 311.7 |
| Hotzone_Magnet | B_Buildable_HotzoneMagnet_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 450.0 x 600.0 x 2183.8 |
| Radio | B_Buildable_Radio_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 300.0 x 180.0 |
| RefuelStation | B_BuildableRefuelStation_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 300.6 x 300.0 x 240.1 |
| RepairStation | B_BuildableRepairStation_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 300.0 x 300.0 x 116.8 |
| SandbagWall | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 300.0 x 33.8 x 100.0 |
| TallHBlock | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 150.0 x 150.0 x 300.0 |
| TankTrap | B_Buildable_C | 5 | 0.0, 0.25, 0.5, 0.75, 1.0 | 220.0 x 220.0 x 200.0 |

### 6.3 Damage modifiers on buildables (`DT_GlobalDamage_BuildableData`)

Each buildable row holds a list of `DamageModificationEntries`. The matrix shows the `Amount` of the entry that matches a source damage tag only (no instigator or target requirement). Every shown entry uses operation `Percentage_Ongoing`. Negative is read as reduced damage and positive as increased damage. **This sign reading is inferred** from the amounts (e.g. `-80` on bullets and `+1400` on FOB rockets); the export does not state it.

| Buildable | Melee | Bullet | Bullet+HP | Bullet+AP | Rocket | Rocket 155mm | Cannon 30mm | Throwable | Entries |
|---|---|---|---|---|---|---|---|---|---|
| FOB | -80.0 | -80.0 | -60.0 | 35.0 | 1400.0 | -93.5 | -50.0 | -100.0 | 21 |
| Door | -80.0 | -85.0 | -50.0 | 100.0 | 650.0 | -95.0 | -50.0 | -100.0 | 21 |
| BarbedWire | -28.0 | -85.0 | -50.0 | 100.0 | 200.0 | -9.0 | -50.0 | -100.0 | 21 |
| AirRaidShelter | -10.0 | -80.0 | -60.0 | 80.0 | 45.0 | -86.0 | - | -100.0 | 16 |
| Bunker | -10.0 | -80.0 | -60.0 | 80.0 | 45.0 | -86.0 | - | -100.0 | 16 |
| CamoTent | -28.0 | -85.0 | -50.0 | 100.0 | 200.0 | -9.0 | -50.0 | -100.0 | 21 |
| CrowsNest | -10.0 | -80.0 | -60.0 | 80.0 | 45.0 | -86.0 | - | -100.0 | 16 |
| SmallHesco | -80.0 | -80.0 | -60.0 | 35.0 | 120.0 | -78.0 | -50.0 | -100.0 | 21 |
| HescoGate | -80.0 | -85.0 | -50.0 | 100.0 | 850.0 | -70.0 | -50.0 | -100.0 | 20 |
| QuadLargeHescoWall | 0.0 | -80.0 | -60.0 | 35.0 | 200.0 | -9.0 | - | -100.0 | 16 |
| BuildableHotzoneMagnet | -80.0 | -85.0 | -50.0 | 100.0 | 850.0 | -70.0 | -50.0 | -100.0 | 20 |
| RepairStation | -80.0 | -80.0 | -60.0 | 35.0 | 1500.0 | -95.0 | -50.0 | -100.0 | 19 |
| RefuelStation | -80.0 | -80.0 | -60.0 | 35.0 | 1500.0 | -95.0 | -50.0 | -100.0 | 19 |
| SandbagWall | -80.0 | -85.0 | -50.0 | 100.0 | 650.0 | -9.0 | -50.0 | -100.0 | 20 |
| LargeHesco | -80.0 | -80.0 | -60.0 | 35.0 | 80.0 | -73.2 | -50.0 | -100.0 | 21 |
| TankTrap | -80.0 | -85.0 | -50.0 | 100.0 | 450.0 | -55.0 | -50.0 | -100.0 | 19 |
| Radio | 70.0 | -85.0 | -50.0 | 100.0 | 1000.0 | -9.0 | 100.0 | -100.0 | 21 |
| BremmerWall | -80.0 | -80.0 | -60.0 | 35.0 | 250.0 | -72.0 | -50.0 | -100.0 | 21 |

Each row also has a Throwable and Explosive/Blunt entry plus a catch-all `any` entry with operation `None` and amount `0`. Entries with instigator or target requirements are excluded from the matrix and are not decoded.

### 6.4 Forward Operating Base ruleset

| Buildable | FOB limit |
|---|---|
| RefuelStation | 1 |
| RepairStation | 1 |
| Radio | 4 |

### 6.5 Destruction definitions

| Kind | Asset | SaveID | Chunks | Required meshes |
|---|---|---|---|---|
| Definition | D_BuildableDoor | 4A3D41E9-44BC5FE1-C5584BAE-88E50EC5 | 1 | 1 |
| Definition | D_Decorator_Door_Gate_Left | 28EDB69F-42227366-D0A23898-D63440B1 | - | - |
| Definition | D_Decorator_Door_Gate_Right | 588C807F-4E85AF89-19293588-34A5B324 | - | - |
| Definition | D_Door_Gate_Left | DF456376-41B9DD3E-684DFF91-8345DA3C | 2 | 2 |
| Definition | D_Door_Gate_Right | 484BCB47-41111B48-EA2F34B6-48C855EF | 2 | 2 |

---

## 7. Inventory Footprints

Grid size from `BHInventoryFragment_CustomShape.Dimensions` (X by Y cells) and `MaxStackSize` from `BHInventoryFragment_Stackable`. Items without a row have no footprint in this folder.

| Folder | Asset | Footprint / stack |
|---|---|---|
| Armor | ID_GhillieArmor | 5 x 4 |
| Armor | ID_GhillieArmorDry | 5 x 4 |
| Armor | ID_GhillieHelmet | 2 x 2 |
| Armor | ID_GhillieHelmetDry | 2 x 2 |
| Armor | ID_HeavyArmor | 4 x 5 |
| Armor | ID_HeavyHelmet | 2 x 2 |
| Armor | ID_LightArmor | 3 x 4 |
| Armor | ID_LightHelmet | 2 x 2 |
| Armor | ID_MediumArmor | 3 x 4 |
| Armor | ID_MediumHelmet | 2 x 2 |
| Armor | ID_SuperHeavyArmor | 4 x 5 |
| Armor | ID_SuperHeavyHelmet | 2 x 2 |
| Battery | ID_Battery | no Dimensions value exported |
| Battery | ID_Battery_Charge | stack 100 |
| Battery | ID_LrgBattery | 1 x 2 |
| Buildables | ID_BuildToolSupply | no Dimensions value exported |
| Buildables | ID_ForwardOperatingBase | 2 x 3 |
| Buildables | ID_FuelSupplies | no Dimensions value exported |
| Buildables | ID_LargeHammer | 4 x 2 |
| Buildables | ID_MediumHammer | 2 x 3 |
| Buildables | ID_MuntionsSupplies | no Dimensions value exported |
| Buildables | ID_SmallHammer | 2 x 1 |
| Buildables | ID_SparePartsSupplies | no Dimensions value exported |
| C4 | ID_C4_Explosive | 1 x 2 |
| CombatBow | ID_Arrow_Combat | 1 x 3 |
| CombatBow | ID_Arrow_Explosive | 3 x 1 |
| Crowbar | ID_Crowbar | 3 x 1 |
| Enox | ID_Enox_Standard | no Dimensions value exported |
| Enox | ID_Resuscitator | 1 x 2 |
| Enox | ID_Resuscitator_Standard | 1 x 2 |
| IED | ID_IED_Explosive | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Black | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Blue | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Green | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Orange | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Purple | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Red | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_White | no Dimensions value exported |
| SmokeGrenade | ID_SmokeGrenade_Yellow | no Dimensions value exported |
| StimPen | ID_StimPen | no Dimensions value exported |

---

## 8. Meta Skill Effects

| Folder | Row | Effect class(es) | Skill key |
|---|---|---|---|
| C4 | Meta.Role.Support.IncreadedDetonatorRange | GE_Weapons_DetonatorRangeMultiplier_C | Meta.Skill.Item |
| PrototypeMaskedScopes | Meta.Role.Recon.ColdBlooded | GE_Spotting_CustomDepthStencilValue_C | Meta.Skill.Character |

---

## 9. Music Tapes

Nine tapes. Each has a `BHEntityData_UI` row and a vendor row. All nine are priced at 100 and sold in the `Vendor.Category.Vehicle.Music` subcategory.

| Row tag | Track (as named in the entity row) | Price |
|---|---|---|
| Id.Item.MusicTape.01 | - | 100 |
| Id.Item.MusicTape.02 | - | 100 |
| Id.Item.MusicTape.03 | - | 100 |
| Id.Item.MusicTape.04 | - | 100 |
| Id.Item.MusicTape.05 | - | 100 |
| Id.Item.MusicTape.06 | - | 100 |
| Id.Item.MusicTape.07 | - | 100 |
| Id.Item.MusicTape.08 | - | 100 |
| Id.Item.MusicTape.09 | - | 100 |

---

## 10. How the Values Combine

- **Buying:** the vendor `Price` is charged once per purchase and grants `Qty` units. Per-unit cost is `Price / Qty`.
- **Placement:** a hammer lists the buildables it may place (section 6.1). The FOB ruleset then caps some buildables per FOB (section 6.4). The per-buildable material cost is not in this plugin.
- **Damage on buildables:** for a given hit, the matching entries in section 6.3 apply. How several matching entries stack (additive or multiplicative) is not decoded, so no combined multiplier is given.

---

## 11. Still Not Pulled / Limitations

- **Build costs.** `WDActorBuildSpawner` and `BuildingStagesDefinition` carry no material cost. If a cost field exists, it is in an asset class outside this folder.
- **Damage modifier requirements.** Entries with instigator, target or hit-location requirements are not decoded. Their meaning and priority order are unknown.
- **`LevelToUnlock`.** Stored on vendor variations (values 0 or 1). The system that reads it is not in this folder, so its effect is unconfirmed.
- **Sign and units.** The damage sign (section 6.3) and projectile speed and length units are inferred, not stated.
- **Audio, animation, crosstalk and most UI widget data.** Counted in section 1 but not decoded. Firing audio, animation sets and HUD tracker layouts are not summarised.
- **Placeholder assets.** `Injector` has only a `GameFeatureData` shell with no properties. `Landmine` has a `GameFeatureData` with an asset scan for `BH.Item` and no item data.
- **Mortar, Phalanx, Talon 9K-SAM, Loudspeaker.** These buildables have roster rows here but no hammer, spawner or stages data in this folder.

