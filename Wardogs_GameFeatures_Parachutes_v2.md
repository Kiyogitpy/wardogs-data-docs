---
title: "Parachutes (feature)"
parent: "Game Features"
---

# Wardogs — Parachutes Game Feature Reference
*Extracted from cooked game data ([`Wardogs/Plugins/GameFeatures/Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Parachutes), 7 JSON files, all parsed). Build `++Wardogs+Live-CL-516586`, UE 5.7.*

> **What this is:** two parachute items (Basic and Sport), each with a movement profile, a vendor listing, UI text, and an inventory definition. The plugin registers its vendor and UI rows through two data registry sources.

---

## Season 02 update (2026-10-15)

- Basic and Sport `MinFallHeightBeforeAbleToParachute`: 100 → 400.
- Sport `PullUpDragAcceleration`: 825 → 400.
- Both profiles gained `VerticalDragCoefficient` (1.75), `OpenDuration` (2.0) and `MinHeightOpenParachuteFromGround` (1000).
- Vendor price: Basic 100 → 500, Sport 1,000 → 700.

---

## 1. Plugin Inventory

| Asset | Type | Role |
|---|---|---|
| [`Content/DA_ParachuteMovement_Basic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DA_ParachuteMovement_Basic.json) | `WDParachuteData` | Basic movement profile |
| [`Content/DA_ParachuteMovement_Sport`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DA_ParachuteMovement_Sport.json) | `WDParachuteData` | Sport movement profile |
| [`Content/ID_Parachute_Basic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/ID_Parachute_Basic.json) | `BHInventoryItemDefinition` (7 exports) | Basic inventory item |
| [`Content/ID_Parachute_Sport`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/ID_Parachute_Sport.json) | `BHInventoryItemDefinition` (7 exports) | Sport inventory item |
| [`Content/DT_VendorData_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_VendorData_Ext_Parachutes.json) | `DataTable` (`WDVendorData`, 2 rows) | Vendor listings |
| [`Content/DT_EntityData_UI_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_EntityData_UI_Ext_Parachutes.json) | `DataTable` (`BHEntityData_UI`, 2 rows) | Name, description, icons |
| [`Content/Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/Parachutes.json) | `GameFeatureData` + 2 `GameFeatureAction_DataRegistrySource` | Plugin root |

Item and movement IDs: `Id.Item.Parachute.Basic`, `Id.Item.Parachute.Sport`.

---

## 2. Movement Profiles (`WDParachuteData`)

Fields not listed for a profile are absent from its export (see section 8).

| Property | Basic | Sport | Notes |
|---|---|---|---|
| `ParachutingFloorTraceDistance` | 1,000,000 | 1,000,000 | Downward trace length |
| `HorizontalDragCoefficient` | 1.0 | **1.1** | |
| `HorizontalMaxSpeed` | not exported | **2,200** | |
| `VerticalMaxSpeed` | not exported | **3,000** | |
| `HorizontalAcceleration` | 300 | **250** | |
| `GliderAcceleration` | 0 | **1,000** | |
| `PullUpDragAcceleration` | 0 | **400** | |
| `TurnAcceleration` | 60 | **40** | |
| `PitchSpeed` | 1.0 | **1.6** | |
| `RollSpeed` | 1.0 | not exported | |
| `MinPitch` / `MaxPitch` | -40 / 20 | -40 / 20 | |
| `MaxRoll` | 30 | 30 | |
| `SwingForceMultiplier` | 5.0 | **4.0** | |
| `MaxPullUpStamina` | 0 | not exported | |
| `PullUpStaminaUsagePerSecond` | 0 | **50** | |
| `PullUpStaminaRegenPerSecond` | 0 | **30** | |
| `MinFallHeightBeforeAbleToParachute` | 400 | 400 | Unit not stated (likely cm) |
| `VerticalDragCoefficient` | 1.75 | 1.75 | |
| `OpenDuration` | 2.0 | 2.0 | |
| `MinHeightOpenParachuteFromGround` | 1000 | 1000 | |
| `VelocityDamageLookup` | [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) | same | Damage vs fall velocity |
| `VelocityDamageType` | `WDFallDamageType` | same | |

Reading the difference: the Basic chute has no pull-up stamina, no glide, no pull-up drag and no max speed caps. Sport adds all of them, with a stamina bar that drains at 50/s and regenerates at 30/s.

---

## 3. Inventory Items

| Field | Basic ([`ID_Parachute_Basic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/ID_Parachute_Basic.json)) | Sport ([`ID_Parachute_Sport`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/ID_Parachute_Sport.json)) |
|---|---|---|
| `ItemId` | `Id.Item.Parachute.Basic` | `Id.Item.Parachute.Sport` |
| `DisplayName` | "Parachute" | "Parachute" |
| `ItemContext` | `Inventory.Slot.Traversal`, `Item.Parachute`, `Item.Context.Equippable`, `Item.Archetype.Parachute` | same |
| Weight | **2.5** | **9.0** |
| Inventory shape | 3 x 2 | 3 x 2 |
| Parachute data | [`DA_ParachuteMovement_Basic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DA_ParachuteMovement_Basic.json) | [`DA_ParachuteMovement_Sport`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DA_ParachuteMovement_Sport.json) |
| Audio data asset | [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json) | [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json) |

### Fragments (both items)

| Fragment | Settings |
|---|---|
| `BHInventoryFragment_UserInterface` | (none) |
| `BHInventoryFragment_Weight` | Weight as above |
| `BHInventoryFragment_Droppable` | Dropped mesh: Basic `Backpack_SM_Temp`, Sport `Backpack_SM`; rotation (Pitch 0, Yaw 90, Roll 10); override relative location (-4, 0, -25); override box extent (15, 16, 22) |
| `WDInventoryFragment_Audio` | [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json) |
| `BHInventoryFragment_CustomShape` | Dimensions 3 x 2 |
| `WDInventoryFragment_Parachute` | `ParachuteData` -> the matching movement profile |

Both drop a backpack-style mesh (the Basic one is the `_Temp` variant). The movement profile is what distinguishes them in play.

---

## 4. Vendor Listings ([`DT_VendorData_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_VendorData_Ext_Parachutes.json))

| Row | Price | Amount per purchase | Level to unlock | Lifetime buy limit | Vendor category | Shown in vendor |
|---|---|---|---|---|---|---|
| `Id.Item.Parachute.Basic` | **500** | 1 | 0 | 0 (no limit) | `Vendor.Category.Gear.Traversal` (variation); `Vendor.Category.Utility` (row) | yes |
| `Id.Item.Parachute.Sport` | **700** | 1 | 0 | 0 (no limit) | `Vendor.Category.Gear.Traversal` (variation); `Vendor.Category.Utility` (row) | yes |

Both rows have no unlock requirements (`UnlockRequiredItems` empty) and are not faction-specific. Both use purchase event `Audio.Event.UI.InGame.Vendor.Purchase` and vendor audio [`ID_Vest_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Vest_Audio.json), which is not a parachute sound. That looks like a copy-over.

---

## 5. UI Text and Icons ([`DT_EntityData_UI_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_EntityData_UI_Ext_Parachutes.json))

| Row | Friendly name | Description | Icon |
|---|---|---|---|
| `Id.Item.Parachute.Basic` | "Basic Parachute" | "- Single Use / - Must be manually Deployed / - Cannot be Controlled" | `T_UI_Icon_Parachute_Basic` |
| `Id.Item.Parachute.Sport` | "Sport Parachute" | "- Single Use / - Must be manually Deployed / - Can be Controlled" | `T_UI_Icon_Parachute_Sport` |

Both rows use category `None` and XP tags `None`. Each carries subtitle, description and flavour tooltip layouts; the subtitle is "Traversal".

Flavour text:
- Sport: "Reduces fall damage when deployed. Gives the player greater control for evading enemy fire and steering to a landing point."
- Basic: "Reduced Fall damage when deployed"

---

## 6. Game Feature Registration ([`Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/Parachutes.json))

| Action | Registry | Table |
|---|---|---|
| `GameFeatureAction_DataRegistrySource_0` | `VendorData` | [`DT_VendorData_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_VendorData_Ext_Parachutes.json) |
| `GameFeatureAction_DataRegistrySource_1` | `EntityData_UI` | [`DT_EntityData_UI_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_EntityData_UI_Ext_Parachutes.json) |

Both are client and server sources with asset priority 0. No curve tables are added.

---

## 7. How Values Combine

- **Fall damage:** a fall only lets you open a parachute above 400 (the minimum fall height). Velocity damage is read from [`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json), which lives outside this plugin, so the exact damage at a given speed is not in this dump.
- **Sport stamina:** the pull-up action costs 50 stamina per second (`PullUpStaminaUsagePerSecond`) and regenerates at 30 per second when not in use. The Basic profile's stamina values are 0, so it cannot pull up.
- **Sport speed:** horizontal speed caps at 2,200 and vertical at 3,000. Glide adds 1,000 acceleration; pull-up drag adds 400 when active.

---

## 8. Still Not Pulled / Limitations

- **[`CRV_ParachutePunishment_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_ParachutePunishment_Damage.json) curve values** are not in this plugin. Only the reference is here.
- **Absent movement fields.** Several Basic fields (max speeds, roll speed) and Sport fields (max pull-up stamina) are not exported. The runtime default is not known from the dump.
- **Unit for `MinFallHeightBeforeAbleToParachute` and the speed values** is not stated in the export.
- **Plugin root scan rules.** The `GameFeatureData` [`Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/Parachutes.json) has `PrimaryAssetTypesToScan` but was not extracted here.
- **Audio assets.** [`ID_Backpack_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Backpack_Audio.json), [`ID_Vest_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Player/Item/Data/ID_Vest_Audio.json) and the purchase event are referenced by name only.
- **Other registries.** Only the vendor and entity-UI registries are registered. Any other parachute-related table was not seen in this plugin.
