---
title: "Damage & Combat Systems changes"
parent: "Season 2 Changes"
nav_order: 2
description: "Bone damage modifiers, global damage tables and demolition rules: 9 assets added, 16 modified with real changes, 143 property changes."
---

# Damage & Combat Systems changes

Damage tables, combat rules and demolition rule sets: what changed between Season 1 and Season 2.

- **Added:** 9 assets
- **Removed:** 0 assets
- **Modified with real changes:** 16 assets (11 more are noise-only: renamed keys, swapped key names or shifted references from the different Season 1 export, not listed)
- **Moved:** 0 assets
- **Property changes:** 143 in modified and moved assets
- **Removed properties:** 0 values in 0 removed assets
## Headline changes

### Infantry bone damage modifiers (70 values)

Rows are weapon class and hit location. Shown: the 30 largest changes by percentage (values that start at 0 are listed first). The other 40 values are in the browser.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Neck | 2.5 | 0.98 | −1.52 (−60.8%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Torso.Upper | 1.3 | 0.57 | −0.73 (−56.2%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Pelvis | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Arm.Upper | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Arm.Lower | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Arm.Hand | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Leg.Thigh | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Leg.Calf | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Leg.Foot | 1.0 | 0.47 | −0.53 (−53.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Torso.Middle | 1.3 | 0.62 | −0.68 (−52.3%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Artillery · Torso.Upper | 1.8 | 0.885 | −0.915 (−50.8%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Heavy · Torso.Upper | 1.8 | 0.885 | −0.915 (−50.8%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Head | 2.5 | 1.25 | −1.25 (−50.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Minigun · Torso.Lower | 1.3 | 0.65 | −0.65 (−50.0%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Artillery · Torso.Middle | 1.8 | 0.97 | −0.83 (−46.1%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Artillery · Torso.Lower | 1.8 | 0.97 | −0.83 (−46.1%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Heavy · Torso.Middle | 1.8 | 0.97 | −0.83 (−46.1%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Heavy · Torso.Lower | 1.8 | 0.97 | −0.83 (−46.1%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Head | 3.2 | 4.2667 | +1.0667 (+33.3%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Neck | 3.2 | 4.2667 | +1.0667 (+33.3%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Torso.Upper | 1.8 | 2.4 | +0.6 (+33.3%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Torso.Middle | 1.45 | 1.9333 | +0.4833 (+33.3%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Torso.Lower | 1.45 | 1.9333 | +0.4833 (+33.3%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Pelvis | 1.3 | 1.7333 | +0.4333 (+33.3%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Artillery · Head | 3.2 | 2.35 | −0.85 (−26.6%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Artillery · Neck | 3.2 | 2.35 | −0.85 (−26.6%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Heavy · Head | 3.2 | 2.35 | −0.85 (−26.6%) |
| DT_InfantryData_BoneDamageModifiers | Vehicle.Turret.Heavy · Neck | 3.2 | 2.35 | −0.85 (−26.6%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Arm.Upper | 1.2 | 1.5 | +0.3 (+25.0%) |
| DT_InfantryData_BoneDamageModifiers | Sniper · Arm.Lower | 1.2 | 1.5 | +0.3 (+25.0%) |

Added weapon entry: `Vehicle.Turret.STN_06` (no Season 1 value).

Added weapon entry: `HMG.MWSY_001` (no Season 1 value).

[All 72 bone damage modifier changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=damage-combat-systems&q=BoneDamageModifiers)

### Global damage tables (28 rows)

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_GlobalDamage_ArmorData | Armor · Entry 3 | — | Percentage_Ongoing, Amount 28.0 | added |
| DT_GlobalDamage_ArmorData | Helmet · Entry 3 | — | Percentage_Ongoing, Amount 28.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 6 | — | Percentage_Ongoing, Amount 0.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 26 | — | Percentage_Ongoing, Amount -10.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 27 | — | Percentage_Ongoing, Amount -34.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 29 | — | Percentage_Ongoing, Amount 0.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 30 | — | Percentage_Ongoing, Amount -10.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 31 | — | Percentage_Ongoing, Amount -34.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 41 | — | Percentage_Ongoing, Amount 0.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 89 · OutModification.Amount | -13.0 | -30.0 | −17.0 (−130.8%) |
| DT_GlobalDamage_InfantryData | Infantry · Entry 106 | — | Percentage_Ongoing, Amount -30.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 109 | — | Percentage_Ongoing, Amount -50.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 115 | — | Percentage_Ongoing, Amount -50.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 118 | — | Percentage_Ongoing, Amount -30.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 119 | — | Percentage_Ongoing, Amount -30.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 124 | — | Percentage_Ongoing, Amount -15.6 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 125 | — | Percentage_Ongoing, Amount -12.5 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 126 | — | Percentage_Ongoing, Amount -6.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 127 | — | Percentage_Ongoing, Amount -7.7 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 128 | — | Percentage_Ongoing, Amount -10.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 129 | — | Percentage_Ongoing, Amount -12.5 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 130 | — | Percentage_Ongoing, Amount -10.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 131 | — | Percentage_Ongoing, Amount -20.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 136 | — | Percentage_Ongoing, Amount -20.0 | added |
| DT_GlobalDamage_InfantryData | Infantry · Entry 25 | present | — | removed |
| DT_GlobalDamage_InfantryData | Infantry · Entry 113 | present | — | removed |
| DT_GlobalDamage_InfantryData | Infantry · Entry 114 | present | — | removed |
| DT_GlobalDamage_InfantryData | Infantry · Entry 116 | present | — | removed |

[All 28 global damage changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=damage-combat-systems&q=GlobalDamage)

### Vehicle seat damage reduction (12 changes)

Seated players in ROT_01 and Littlebird helicopters get half the protection from small and medium arms (−50% → −25%) and less from high-calibre arms (−20% → −15%). The new ROT_04 rows use the Season 2 values. The Havoc and Humvee rows are unchanged.

The reduction field has no readable name, and its hashed name differs between the two seasons' exports. These rows are matched by position, and the browser marks them that way.

| Asset | Property | Season 1 | Season 2 | Change |
|---|---|---|---|---|
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.ROT_01.Default · Small, Medium arms | -50.0 | -25.0 | +25.0 (+50.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.ROT_01.Default · High arms | -20.0 | -15.0 | +5.0 (+25.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.ROT_01.MountedMachineGuns · Small, Medium arms | -50.0 | -25.0 | +25.0 (+50.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.ROT_01.MountedMachineGuns · High arms | -20.0 | -15.0 | +5.0 (+25.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.Littlebird.Default · Small, Medium arms | -50.0 | -25.0 | +25.0 (+50.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.Littlebird.Default · High arms | -20.0 | -15.0 | +5.0 (+25.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.Littlebird.RocketPods · Small, Medium arms | -50.0 | -25.0 | +25.0 (+50.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.Littlebird.RocketPods · High arms | -20.0 | -15.0 | +5.0 (+25.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.Littlebird.MountedMachineGuns · Small, Medium arms | -50.0 | -25.0 | +25.0 (+50.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.Littlebird.MountedMachineGuns · High arms | -20.0 | -15.0 | +5.0 (+25.0%) |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.ROT_04.Default | — | Small, Medium -25.0; High -15.0 | added |
| DT_InfantryData_VehicleSeatDamageReduction | Air.Rotary.ROT_04.MountedMachineGuns | — | Small, Medium -25.0; High -15.0 | added |

[All 12 vehicle seat damage changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=damage-combat-systems&q=VehicleSeatDamage)

### Demolition rule sets and other changes (31 rows)

Most of these are object references and rule indexes. The full list is in the browser.

| Asset | Op | Property | Season 1 | Season 2 |
|---|---|---|---|---|
| BH_Demolition_RS_AirVehicles | added | Properties.PermittedVehicles[6] | — | Vehicle.Variant.Air.Rotary.ROT_04.MountedMachineGuns |
| BH_Demolition_RS_AirVehicles | added | Properties.PermittedVehicles[7] | — | Vehicle.Variant.Air.Rotary.ROT_04.Default |
| BH_Demolition_RS_Everything | changed | Name | BHDemolitionRule_Or_0 | BHDemolitionRule_Or_1 |
| BH_Demolition_RS_Everything | changed | Flags | RF_Public \| RF_Transactional \| RF_WasLoaded \| RF_LoadComplet | RF_Transactional \| RF_WasLoaded \| RF_LoadCompleted |
| BH_Demolition_RS_Everything | changed | Properties.Rules[0].ObjectName | BHDemolitionRule_Ruleset'BH_Demolition_RS_Everything:BHDemol | BHDemolitionRule_Ruleset'BH_Demolition_RS_Everything:BHDemol |
| BH_Demolition_RS_Everything | changed | Properties.Rules[1].ObjectName | BHDemolitionRule_Ruleset'BH_Demolition_RS_Everything:BHDemol | BHDemolitionRule_Ruleset'BH_Demolition_RS_Everything:BHDemol |
| BH_Demolition_RS_Everything | added | Properties.Rules[2] | — | {"ObjectName": "BHDemolitionRule_Ruleset'BH_Demolition_RS_Ev |
| BH_Demolition_RS_Everything | changed | Flags | RF_Public \| RF_Transactional \| RF_WasLoaded \| RF_LoadComplet | RF_WasLoaded \| RF_LoadCompleted |
| BH_Demolition_RS_Everything | changed | Outer.ObjectName | BHDemolitionRule_Or'BH_Demolition_RS_Everything:BHDemolition | BHDemolitionRule_Or'BH_Demolition_RS_Everything:BHDemolition |
| BH_Demolition_RS_Everything | changed | Flags | RF_Public \| RF_Transactional \| RF_WasLoaded \| RF_LoadComplet | RF_WasLoaded \| RF_LoadCompleted |
| BH_Demolition_RS_Everything | changed | Outer.ObjectName | BHDemolitionRule_Or'BH_Demolition_RS_Everything:BHDemolition | BHDemolitionRule_Or'BH_Demolition_RS_Everything:BHDemolition |
| BH_Demolition_RS_Everything | added | BHDemolitionRule_Ruleset_2 | — | {"Type": "BHDemolitionRule_Ruleset", "Name": "BHDemolitionRu |
| BH_Demolition_RS_Everything | changed | Properties.Rule.ObjectName | BHDemolitionRule_Or'BH_Demolition_RS_Everything:BHDemolition | BHDemolitionRule_Or'BH_Demolition_RS_Everything:BHDemolition |
| BH_Demolition_RS_LargeAndMediumWheeledVehicles | added | Properties.PermittedVehicles[10] | — | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| BH_Demolition_RS_LargeAndMediumWheeledVehicles | added | Properties.PermittedVehicles[11] | — | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| BH_Demolition_RS_LargeWheeledVehicles | added | Properties.PermittedVehicles[9] | — | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| BH_Demolition_RS_LargeWheeledVehicles | added | Properties.PermittedVehicles[10] | — | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| BH_Demolition_RS_TrackedVehicles | added | Properties.PermittedVehicles[7] | — | Vehicle.Variant.Land.Tracked.TNK_04.Default |
| BH_Demolition_RS_WheeledVehicles | added | Properties.PermittedVehicles[11] | — | Vehicle.Variant.Land.Wheeled.WHL_08.Default |
| BH_Demolition_RS_WheeledVehicles | added | Properties.PermittedVehicles[12] | — | Vehicle.Variant.Land.Wheeled.WHL_08.MachineGun |
| DA_Demolition_Bollard_Metal_01 | added | ucture/Road_Signs/SM_RoadBollard_White.SM_RoadBollard_White] | — | {"Key": "StaticMesh'/Game/Environment/Transport_Infrastructu |
| DA_Demolition_Bushes_Flora | changed | Properties.DemolitionRuleSet.ObjectName | BHDemolitionRuleset'BH_Demolition_RS_Everything' | BHDemolitionRuleset'BH_Demolition_RS_EverythingAndMolotov' |
| DA_Demolition_Bushes_Flora | changed | Properties.DemolitionRuleSet.ObjectPath | /Game/Demolition/RuleSets/BH_Demolition_RS_Everything.3 | /Game/Demolition/RuleSets/BH_Demolition_RS_EverythingAndMolo |
| DA_Demolition_Fences_Concrete_01 | added | all_Plaster_Residential_01a.SM_Wall_Plaster_Residential_01a] | — | {"Key": "StaticMesh'/Game/Environment/Props/Walls_and_Fences |
| DA_Demolition_Fences_Concrete_01 | added | ial_01_Pillar_01a.SM_Wall_Plaster_Residential_01_Pillar_01a] | — | {"Key": "StaticMesh'/Game/Environment/Props/Walls_and_Fences |
| DA_Demolition_Fences_Wood_01_A | changed | Properties.DemolitionRuleSet.ObjectName | BHDemolitionRuleset'BH_Demolition_RS_LargeAndMediumVehiclesA | BHDemolitionRuleset'BH_Demolition_RS_LargeAndMediumVehiclesE |
| DA_Demolition_Fences_Wood_01_A | changed | Properties.DemolitionRuleSet.ObjectPath | /Game/Demolition/RuleSets/BH_Demolition_RS_LargeAndMediumVeh | /Game/Demolition/RuleSets/BH_Demolition_RS_LargeAndMediumVeh |
| DA_Demolition_Fences_Wood_01_B | changed | Properties.DemolitionRuleSet.ObjectName | BHDemolitionRuleset'BH_Demolition_RS_LargeAndMediumVehiclesA | BHDemolitionRuleset'BH_Demolition_RS_LargeAndMediumVehiclesE |
| DA_Demolition_Fences_Wood_01_B | changed | Properties.DemolitionRuleSet.ObjectPath | /Game/Demolition/RuleSets/BH_Demolition_RS_LargeAndMediumVeh | /Game/Demolition/RuleSets/BH_Demolition_RS_LargeAndMediumVeh |
| DA_Demolition_Saplings | changed | Properties.DemolitionRuleSet.ObjectName | BHDemolitionRuleset'BH_Demolition_RS_Everything' | BHDemolitionRuleset'BH_Demolition_RS_EverythingAndMolotov' |
| DA_Demolition_Saplings | changed | Properties.DemolitionRuleSet.ObjectPath | /Game/Demolition/RuleSets/BH_Demolition_RS_Everything.3 | /Game/Demolition/RuleSets/BH_Demolition_RS_EverythingAndMolo |

[All 31 demolition changes →]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=damage-combat-systems&q=Demolition)

## New in Season 2 (9 assets)

| Asset | Type | Identification |
|---|---|---|
| DA_Demolition_Fences_Metal_03 | BHDemolitionDataAsset | 1 exports |
| DA_Demolition_RM_Fence_Metal_Residential_03_01_A | BHDemolitionRemnantMeshesAsset | 1 exports |
| DA_Demolition_RM_Fences_Plaster_Residential_01_A | BHDemolitionRemnantMeshesAsset | 1 exports |
| DA_Demolition_RM_Fences_Plaster_Residential_Pillar_01_A | BHDemolitionRemnantMeshesAsset | 1 exports |
| BH_Demolition_RS_Buildables | BHDemolitionRuleset | 2 exports |
| BH_Demolition_RS_EverythingAndMolotov | BHDemolitionRuleset | 6 exports |
| BH_Demolition_RS_LargeAndMediumVehiclesExplosionsAndBuildables | BHDemolitionRuleset | 4 exports |
| BH_Demolition_RS_Molotov | BHDemolitionRuleset | 2 exports |
| DT_InfantryData_ArchetypeCaliberModifiers | DataTable | 1 exports |

## Removed in Season 2 (0 assets)

None.

## Moved in Season 2 (0 assets)

None.

## See also

- [Game mechanics, Season 02 update]({{ '/content/Wardogs_GameMechanics_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Demolition, Season 02 update]({{ '/content/Wardogs_Demolition_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Destruction, Season 02 update]({{ '/content/Wardogs_Destruction_v2.html' | relative_url }}#season-02-update-2026-10-15)
- [Vehicle stats and damage, Season 02 update]({{ '/content/Wardogs_AllVehicles_Stats_Damage_v1.html' | relative_url }}#season-02-update-2026-10-15)
- [Ammo game feature, Season 02 update]({{ '/game-features/Wardogs_GameFeatures_Ammo_v2.html' | relative_url }}#season-02-update-2026-10-15)
