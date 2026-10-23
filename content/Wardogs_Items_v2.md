---
title: "Items"
redirect_from: ["/Wardogs_Items_v2.html", "/Wardogs_Items_v2"]
parent: "Items & Equipment"
description: "How an Item Is Built, Attachments, Clothing and Equipment, Consumables and Medical Items"
---

# Wardogs — Items Reference
*Extracted from cooked game data exported to JSON, source [`Wardogs/Content/Items/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items) (259 files). Every number below comes from the exported properties; anything the dump does not contain is marked as such.*

> **Shop and entity data for non-weapon items** (armor, helmets, vests, backpacks, medical items, throwables, explosives, tools, vehicle items; price, unlock level, buy limit, description, weight and key stats) is in [Item Shop](../game-features/Wardogs_ItemShop_v1.md). Weapon parts are in [Weapon Shop](../game-features/Wardogs_WeaponShop_v1.md).

> **How the files are structured:** each `.json` file is not one object. It holds several export blocks, each starting with a `--- export: <Kind> / <Name> ---` header followed by its own JSON object. Across the category there are 1,401 blocks: 230 `UPrimaryDataAsset` roots (the items and assets people actually use), 1,142 `UObject` sub-objects (the "fragments" each item points to), 26 `UCurveFloat`, 2 `UCurveTable`, and 1 `UDataAsset`. A primary item lists its fragments in `DataFragments`; the fragment blocks in the same file hold the values.

---

## Season 02 update (2026-10-15)

- **New ammo:** `125x570mm` (1 round, grid 3x2, max stack 5, weight 24.0), with a new vehicle turret that accepts it.
- **New vehicle weapons (4):** [`ID_MountedMachineGun_TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_04/ID_MountedMachineGun_TNK_04.json) (50Cal, stack 60), [`ID_VehicleTurretMachineGun_TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_04/ID_VehicleTurretMachineGun_TNK_04.json) (762x54mm, stack 150), [`ID_VehicleTurret_TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/TNK_04/ID_VehicleTurret_TNK_04.json) (125x570mm, stack 1), and [`ID_WHL_08_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Vehicles/Weapons/WHL_08/ID_WHL_08_RingTurret.json) (50Cal, stack 60).
- **Removed:** no items or files were removed.
- **Stack overrides:** 30mm gains a `Vehicle.Storage` override of 200. The .50 Cal tracer gains `Vehicle.Storage` and `Type.Vehicle` at 50. The 762x54mm tracer variants gain both overrides at 150.
- **Ammo context:** 84mm and 93mm no longer carry `Item.Context.ForceToStorage`.
- **Vehicle items:** 20 items gain `Item.Context.MovementBlocked`.
- **Aim assist, reticles:** AR inner reticle width 1900 -> 900, AR reticle depth 60000 -> 30000, SMG reticle depth 40000 -> 20000, SR reticle depth 20000 -> 40000.
- **Aim assist, range:** LMG target range 50000 -> 30000, Shotgun 15000 -> 20000, SR gains 40000.
- **Aim assist, pull and slow:** PullLerp and SlowLerp rates become 10 / 8 for every class except RPG (were 30 / 12 for PullLerp, and 6 / 5 or 5 / 5 for SlowLerp). PullInnerStrengthHip becomes 1.0 for every class that sets it (was 1.4 to 4.0). PullInnerStrengthAds becomes 2.0 for AR, LMG, Pistol, SMG, SR and Shotgun (was 4.0 to 6.0).
- **Aim assist, rotation:** PullMaxRotationRate becomes 90 for AR, LMG, SMG, SR and Shotgun (was 120 or 135).
- **Aim assist, removed keys:** `PullOuterStrengthHip`, `SlowInnerStrengthHip` and `SlowMinRotationRate` are gone for most classes. SR no longer sets `PullMode`, and Melee no longer sets `PullModeADS`.
- **Aim assist, curves:** hipfire pull and slow curves for most classes now point to `_Default` curves (section 9).
- **Counts:** 259 files, 230 primary assets, 193 item definitions (was 254, 225, 188).

---

## 1. Inventory Summary

| Folder | Primary assets | Main type(s) | Notes |
|---|---|---|---|
| [`Resources/Ammo`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Resources/Ammo) | 98 (94 items) | BHInventoryItemDefinition | Every caliber and round variant, plus 3 audio assets and 1 debug projectile |
| `Attachments/Magazines` | 23 | BHInventoryItemDefinition | Magazines, drums, and internal cylinders/boxes (internal ones have no gunsmith entry) |
| `Vehicles/Weapons` | 16 | BHInventoryItemDefinition | Vehicle turrets, mounted MGs, helicopter cannon/rocket pods |
| [`Clothing/Backpacks`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Clothing/Backpacks) | 10 | BHInventoryItemDefinition | Storage bags, pouch, and sling variants |
| `Attachments/Sights` | 8 | BHInventoryItemDefinition | Optics, iron sights |
| [`Attachments/Muzzle_Devices`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Attachments/Muzzle_Devices) | 7 | BHInventoryItemDefinition | Suppressors and brakes |
| `Weapons/AR` | 5 | BHInventoryItemDefinition | Components only (barrels, grip, handguard, stock) |
| `Attachments/Foregrips` | 4 | BHInventoryItemDefinition | Foregrips and the Grip Pod bipod |
| [`Vehicles/Storage`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Vehicles/Storage) | 4 | BHInventoryItemDefinition | Vehicle cargo containers |
| `Weapons/Pistol` | 4 | BHInventoryItemDefinition | Pistol components |
| [`Clothing/Vests`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Clothing/Vests) | 3 | BHInventoryItemDefinition | Tac vests (quick-slot providers) |
| `Weapons/SMG` | 3 | BHInventoryItemDefinition | SMG components |
| [`Consumables/Bandage`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Consumables/Bandage) | 2 items + 4 support | BHInventoryItemDefinition, BHAnimationSet, WDAudioData | Bandage and IFAK |
| [`Throwable/Grenades`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Throwable/Grenades) | 2 items + 3 support | BHInventoryItemDefinition, BHAnimationSet, WDAudioData | M67 frag and gold variant |
| [`Weapons/Launcher`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Weapons/Launcher) | 2 items + 2 anim sets | BHInventoryItemDefinition | Two artillery/tank barrel test items |
| [`Attachments/Grips`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Attachments/Grips), `Handguards`, `Stocks` | 1 each | BHInventoryItemDefinition | Single components |
| [`Placeables/AmmoCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Placeables/AmmoCrate) | 1 | BHInventoryItemDefinition | Ammo Crate |
| `Weapons/Fists` | 1 item + 2 support | BHInventoryItemDefinition, BHAnimationSet, WDAudioData | Unarmed |
| `Weapons/LMG` | 1 | BHInventoryItemDefinition | LMG barrel component |
| [`Attachments/Archetypes`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Attachments/Archetypes) | 12 | WDAttachmentArchetype | Slot-type definitions (bone, tag) |
| [`Attachments/Utilities`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Attachments/Utilities) | 1 | BHAnimationSet | Grip Pod animation set |
| `Weapons/` (root) | 8 aim-assist settings + 1 filter | BHAimAssistSettingsData, BHAimAssistFilterData | One per weapon class |
| [`Resources/Ammo/Curves`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Resources/Ammo/Curves), [`Throwable/Curves`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Throwable/Curves), `Weapons/Curves` | 28 | CurveFloat, CurveTable | See section 11 |

**Totals:** 193 item definitions (`BHInventoryItemDefinition`), 230 primary assets in all, 259 files. 

---

## 2. How an Item Is Built (Fragment Model)

An item is a `BHInventoryItemDefinition` with an `ItemId` tag, `ItemContext` tags, a `DisplayName`, and a `DataFragments` array. Each fragment is a separate block that supplies one aspect of the item:

| Fragment type | Key properties | Blocks in dump | What it controls |
|---|---|---|---|
| `BHInventoryFragment_Weight` | `Weight` | 56 (47 with a value) | Carry weight. Unit not stated in dump. |
| `BHInventoryFragment_Stackable` | `MaxStackSize`, `MaxStackSizeOverrides` (keyed by slot/type tag) | 94 | Inventory stack limit, with per-slot overrides |
| `BHInventoryFragment_CustomShape` | `Dimensions` (X, Y) | 149 | Inventory grid footprint. X and Y read as columns and rows (not verified in-game). |
| `BHInventoryFragment_Droppable` | `DroppedMesh`, `RelativeRotation`, `MaterialOverrides`, box/offset overrides | 146 | World drop appearance |
| `BHInventoryFragment_UserInterface` | `bIsVisibleOnEquippedUI`, `DisplayedItems`, `bDisplayIncludeAllSlots` | 155 | Inventory and equipped-UI display |
| `BHInventoryFragment_SubSlotSupport` | `Containers[]` (see below) | 62 | Child-slot storage: magazines in weapons, ammo in vehicles, pockets in packs |
| `WDInventoryFragment_Attachment` | `AttachmentData` (type tag, applied GEs, removable flag, reload rate) | 54 | Gunsmith attachment behaviour |
| `WDInventoryFragment_Gunsmith` | `ItemType` | 55 | Whether the item appears in the gunsmith (`EWDGunsmithItemType::Attachment`) |
| `WDInventoryFragment_Projectile` | `ProjectileData` (object reference) | 94 | Links an ammo item to its `WDProjectileData` asset |
| `WDInventoryFragment_Audio` | `AudioDataAsset` | 155 | Pickup and handling sounds |
| `WDInventoryFragment_ItemActor` | `ExtensionDataFragments[]` | 8 | Groups the extension blocks for a holdable/consumable |
| `WDInventoryFragment_QuickSlots` | `NumberOfAddedQuickSlots` | 3 | Extra quick slots granted by equipment |
| `WDInventoryFragment_EquippedEffects` | `AppliedEffects` | 3 | Gameplay effects applied while worn |
| `WDItemsmithDataFragment_CameraData` | `CameraParams` | 3 | Gunsmith preview camera |

### 2a. Sub-slot container fields (`BHInventoryFragment_SubSlotSupport.Containers[]`)

| Field | Meaning (as observed) |
|---|---|
| `ContainerIdentifier` | Tag for the slot family. Most backpack containers have `None` here. Attachment slots use `Item.Attachment.*` or `Item.Ammo` / `Inventory.Slot.Vehicle.Storage`. |
| `Filter.SupportFilter` | `AllowList`, `BlockList`, `BlockPriority` or `AllowPriority` (the last is unused in data). Decides which items may enter. |
| `Filter.AllowedSubSlotContext` | Context tags that pass the filter (e.g. `Item.Caliber.556mm`) |
| `GridSize` | Size of that container in grid cells (X x Y) |
| `MaxSlotAmountStackSize` | **Capacity for magazines.** Magazine names match this value exactly (30 RND = 30, 75 RND drum = 75, 200 RND box = 200, 130 RND = 130). Applied to vehicle ammo slots as well. |
| `DefaultItems`, `DefaultContainerItems` | Items added when the item is created with defaults (`0x6784010`). `DefaultContainerItems` wins: `DefaultItems` is used only when `DefaultContainerItems` is empty, so the M4 Standard Mag loads `Id.Item.556mm.Tracer`. Each `DefaultContainerItems` entry is added with its `Amount` if set, else `MaxSlotAmountStackSize` when > 0, else the item's `MaxStackSize`, else 1. |

### 2b. Item definition flags seen

| Field | Values in dump |
|---|---|
| `ItemContext` | Ammo items carry `Item.Ammo` (93) and `Item.Context.ForceToStorage` (91). Equippable items carry `Item.Context.Equippable` (33). Attachments carry `Item.Attachment.<slot>`. |
| `Item.Ammo.Type.*` | `FMJ.Tracer` (28), `HollowPoint` (12), `HollowPoint.Tracer` (12), `ArmorPiercing` (11), `ArmorPiercing.Tracer` (11) |
| `DisplayName.SourceString` | Present on 179 of 193 items. The 14 without one are all attachment or weapon-component parts (3 attachment grips/handguards/stocks and 11 weapon components). |

---

## 3. Attachments

### 3a. Attachment Archetypes ([`Attachments/Archetypes`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Attachments/Archetypes))

Twelve `WDAttachmentArchetype` assets define each slot's `AttachmentId` tag, the skeletal bone it attaches to, and (in two cases) a bone offset.

| Archetype | AttachmentId | Bone | Category | Bone offset |
|---|---|---|---|---|
| DA_BarrelAttachmentArchetype | Item.Attachment.Barrel | barrel_Attach | Component | - |
| DA_GripAttachmentArchetype | Item.Attachment.Grip | grip_Attach | Component | - |
| DA_HandguardAttachmentArchetype | Item.Attachment.Handguard | handguard_Attach | Component | (0, -3, 3) |
| DA_MagazineAttachmentArchetype | Item.Attachment.Magazine | mag01_Attach | - | - |
| DA_MountLeftAttachmentArchetype | Item.Attachment.MountLeft | leftRail_Attach | - | - |
| DA_MountRightAttachmentArchetype | Item.Attachment.MountRight | rightRail_Attach | - | - |
| DA_MountTopAttachmentArchetype | Item.Attachment.MountTop | topRail_Attach | - | - |
| DA_MountUnderAttachmentArchetype | Item.Attachment.MountUnder | bottomRail_Attach | - | - |
| DA_MuzzleAttachmentArchetype | Item.Attachment.Muzzle | muzzle_Attach | - | - |
| DA_SightAttachmentArchetype | Item.Attachment.Sight | sight_Attach | - | - |
| DA_StockAttachmentArchetype | Item.Attachment.Stock | stock_Attach | Component | - |
| DA_UnderbarrelAttachmentArchetype | Item.Attachment.Underbarrel | underbarrel_Attach | - | (0, 2.5, 0) |

Attachment categories on the item side (`AttachmentData.AttachmentType`, 54 items): Magazine 19, Sight 8, Muzzle 7, Grip 6, Barrel 5, Handguard 4, Stock 4, Bipod 1 (the Grip Pod).

Across the 54 attachment items, `bCanBeRemovedInGame` is `True` on 34 and `False` on 20. `bDiscardWhenEmptyOnReload` is `False` on all 54.

### 3b. Magazines (`Attachments/Magazines`, 23 items)

Capacity is taken from the magazine's `MaxSlotAmountStackSize` (section 2a).

| Asset | Display | Weight | Capacity | Grid | Caliber | Gunsmith |
|---|---|---|---|---|---|---|
| ID_556STANAG_Mag_Standard | STANAG 30 RND Magazine | 0.53 | 30 | 1x2 | 556mm | Yes |
| ID_A91_Mag_Standard | A91 Standard Mag | - | 30 | 1x2 | 556mm | Yes |
| ID_AK74M_Mag_Standard | AK74 30 RND Magazine | 0.55 | 30 | 1x2 | 545mm | Yes |
| ID_AK74M_Mag_Extended | AK74 60 RND Magazine | 0.93 | 60 | 1x3 | 545mm | Yes |
| ID_AK74M_Mag_75rnd | AK74 75 RND Drum Magazine | 2.08 | 75 | 2x2 | 545mm | Yes |
| ID_AK74M_Mag_Plum_130rnd | AK74-M Extended Mag | - | 130 | 1x2 | 545mm | No |
| ID_AR_Mag_Extended | AR Extended Mag | - | 45 | 1x2 | 545mm | Yes |
| ID_Glock17_Mag_Standard | GGX 17 RND Magazine | 0.28 | 17 | - | 9mm | Yes |
| ID_Glock17_Mag_Extended | Glock 17 Extended Mag | - | 30 | 2x1 | 9mm | Yes |
| ID_KH2002_Mag_Standard | KH2002 Standard Mag | - | 30 | 1x2 | 556mm | Yes |
| ID_KH2002_Mag_Extended | KH2002 Extended Mag | - | 45 | 1x2 | 556mm | Yes |
| ID_M4_Mag_Standard | M4 Standard Mag | - | 30 | 1x2 | 556mm | Yes |
| ID_M4_Mag_Extended | M4 Extended Mag | - | 45 | 1x2 | 556mm | Yes |
| ID_STANAG_Mag_Extended90rd | M4 Extended Mag (90 rd) | - | 90 | 1x2 | 556mm | No |
| ID_TAR21_Mag_Standard | TAR21 Standard Mag | - | 30 | 1x2 | 556mm | Yes |
| ID_M249_Mag_Standard | M249 200 RND Box | 3.14 | 200 | 2x3 | 556mm | Yes |
| ID_SKS_Mag_Extended | SKS Extended Mag | - | 20 | 1x2 | 762mm | Yes |
| ID_SKS_Mag_Internal | SKS Internal Mag | - | 10 | - | 762mm | No |
| ID_Mosin_Mag_Extended10rd | SV98 Extended Mag | - | 10 | 1x2 | 762x54mm | No |
| ID_Mosin_Mag_Extended20rd | SV98 Extended Mag | - | 20 | 1x2 | 762x54mm | No |
| ID_Judge_Mag_Internal | Judge Bullet Cylinder | - | 6 | - | 45Colt | No |
| ID_M12G_Mag_Internal | M500 Internal Mag | - | 6 | - | 12g | No |
| ID_MMGL_Mag_Internal | MMGL Internal Mag | - | 6 | - | 40mm | No |

Notes: "Internal" magazines have no gunsmith entry and no grid. Two different items are both labelled "M4 Extended Mag" ([`ID_M4_Mag_Extended`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Attachments/Magazines/AR/ID_M4_Mag_Extended.json) at 45 and [`ID_STANAG_Mag_Extended90rd`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Attachments/Magazines/AR/STANAG_Mag_Drum_90rd/ID_STANAG_Mag_Extended90rd.json) at 90), and the two SV98 mags share one name. Display names are not unique keys; use the asset name.

### 3c. Optics and Muzzle Devices

| Asset | Display | Weight | Grid | Category |
|---|---|---|---|---|
| ID_10xScope | 6-10x Scope MRAD | 0.98 | 3x1 | Sight |
| ID_10xScopeMoa | 6-10x Scope MOA | 0.98 | 3x1 | Sight |
| ID_4xElcanSpectr | 4x Elcan Spectr | 0.66 | 2x1 | Sight |
| ID_4xHybrid | 4x Hybrid | - | 2x1 | Sight |
| ID_6xScope | 3-6x Scope | - | 2x1 | Sight |
| ID_OPT_08 | 2.5x Combat Optic | 0.4 | 2x1 | Sight |
| ID_EotechHoloSight | Holographic Sight | 0.25 | - | Sight |
| ID_CantedIrons | CantedIrons | - | - | Sight |
| ID_MZL_04 | GOL Multi-Caliber Suppressor | 0.75 | 1x2 | Muzzle |
| ID_MZL_05 | SG Multi-Caliber Suppressor | 0.6 | 1x2 | Muzzle |
| ID_MZL_06 | 12 Gauge Suppressor | 0.8 | 1x2 | Muzzle (has gunsmith camera data) |
| ID_MZL_08 | Hexagon 762 Suppressor | 0.55 | 1x2 | Muzzle |
| ID_MZL_09 | PBS-4 Suppressor | 0.8 | 1x2 | Muzzle |
| ID_MZL_10 | TGP-A Suppressor 5.45 | 0.7 | 1x2 | Muzzle |
| ID_PWSCQB74 | CQB 74 Brake | 0.22 | - | Muzzle |

### 3d. Foregrips, Grips, Handguards, Stocks

| Asset | Display | Weight | Category | Notes |
|---|---|---|---|---|
| ID_FGP_02 | TDG Vertical Foregrip | 0.13 | Grip | - |
| ID_FGP_03 | AFG Angled Foregrip | 0.08 | Grip | - |
| ID_FGP_04 | Grip Pod | 0.26 | Bipod | Grid 1x2; uses [`AnimSet_FGP_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Attachments/Utilities/Bipod/AnimSet_FGP_04.json) (Attachments/Utilities) |
| ID_RK6_Grip | RK6 Tactical Foregrip | 1.05 | Grip | - |
| ID_AK74MIMIEGGrip | (no display) | - | Grip | ItemId `ID.Item.AK74MIMIEGGrip` |
| ID_ZenitHandguard | (no display) | - | Handguard | Child slot accepts `Item.Attachment.Underbarrel` (BlockPriority) |
| ID_ZenitStock | (no display) | - | Stock | - |

### 3e. Weapon Components (test and in-development)

These are the sub-parts a weapon is built from. The base weapon definitions (e.g. the M4 receiver) are **not** in this folder (see section 12).

| Folder | Components |
|---|---|
| `Weapons/AR` | ID_AR_01_BRL_02 (barrel, muzzle child slot), ID_AR_02_BRL_01 (barrel), ID_AR_02_GRP_05 (grip), ID_AR_02_HGD_04 "LVOA Handguard" (underbarrel child slot), ID_AR_02_STK_04 (stock) |
| `Weapons/SMG` | ID_SMG_01_BRL_03 (barrel), ID_SMG_01_HGD_01 (handguard), ID_RS2Stock "RS2 Slim" (stock, ItemId `ID.Item.SMG_01_STK_05`) |
| `Weapons/Pistol` | ID_Pistol_01_BRL_07 (barrel), ID_Pistol_01_GRP_01 (grip), ID_Pistol_01_HGD_02 (handguard), ID_Pistol_01_STK_01 (stock) |
| `Weapons/LMG` | ID_LMG_01_BRL_06 (barrel) |

---

## 4. Clothing and Equipment

### 4a. Backpacks and Pouch ([`Clothing/Backpacks`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Clothing/Backpacks), 10 items)

Container grid is listed as `X x Y` cells, and `Filter` is shown where present. "Sling" variants add a weapon-slot container (BlockPriority on Primary, Secondary, Sidearm, Specialist) with capacity 1.

| Asset | Display | Weight | Item grid | Containers (grid, filter) |
|---|---|---|---|---|
| ID_Pouch | Pouch | 0.3 | 3x2 | 3 x 1x2 (BlockList) |
| ID_SmallBackpack | Small Backpack | 0.5 | 2x4 | 1 x 2x4 |
| ID_MediumBackpack | Medium Backpack | 0.88 | 3x5 | 1 x 3x5 |
| ID_MediumSlingBackpack | Medium Backpack + Sling | 4.0 | 3x5 | 2x5 weapon-slot (BlockPriority, cap 1) + 3x5 |
| ID_LargeBackpack | Large Backpack | 1.5 | 4x6 | 1 x 4x6 |
| ID_LargeSlingBackpack | Large Backpack + Sling | 1.5 | 4x6 | 2x5 weapon-slot (cap 1) + 4x6 |
| ID_ExtraLargeSlingBackpack | Large Backpack + 2 Slings | 1.5 | 5x6 | 2x5 (cap 1) + 4x6 + 1x2 (cap 1) |
| ID_BPAK_005 | Field Backpack | 0.8 | 3x3 | 3 x 2x2 |
| ID_BPAK_006 | Assault Backpack | 1.3 | 3x5 | 1x3, 3x5, 1x3 |
| ID_BPAK_007 | Halftrack Backpack | 2.78 | 3x3 | 1x5, 4x5, 1x5 |

Note: Medium Backpack + Sling reads 4.0 weight against 0.88 for the plain Medium. The sling variants' weight is far higher than the bag alone; the dump does not explain why.

### 4b. Tac Vests ([`Clothing/Vests`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Clothing/Vests), 3 items)

| Asset | Display | Weight | Grid | Extra quick slots | Equipped effect |
|---|---|---|---|---|---|
| ID_SmallTacVest | Small Tac Vest | 0.82 | 4x3 | 2 | GE_Item_SmallTacVest_C |
| ID_MediumTacVest | Medium Tac Vest | 1.65 | 4x3 | 4 | GE_Item_MediumTacVest_C |
| ID_LargeTacVest | Large Tac Vest | 3.6 | 4x3 | 6 | GE_Item_LargeTacVest_C |

Vests give no container of their own; their capacity comes from the quick-slot count.

---

## 5. Consumables and Medical Items

| Property | Bandage ([`ID_Bandage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Consumables/Bandage/ID_Bandage.json)) | Individual First Aid Kit ([`ID_SuperBandage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Consumables/Bandage/ID_SuperBandage.json)) |
|---|---|---|
| Display | Bandage | Individual First Aid Kit |
| ItemId | Id.Item.Bandage | Id.Item.SuperBandage |
| Weight | 0.08 | 0.16 |
| Max stack | 5 | Not set |
| Grid | not set (default) | not set (default) |
| Heal (Attribute.Gameplay.Health) | **+35** per use, applied as delta | **+100** per use, applied as delta |
| Continuous use | `bContinuousUse` = True | Not extracted |
| Context tags | Appliable.Context.HealSelf, Appliable.Context.HealFriendly | Not extracted |
| Applied effect | GE_UseAppliable_C | GE_UseAppliable_C |
| Primary use tag | Action.Appliable.PrimaryUse | Not extracted |
| Secondary use | Action.Appliable.Bandage.SecondaryUse, requires State.Player.Injured and State.Player.Vitality.Alive | Action.Appliable.Bandage.SecondaryUse (same requirements, not fully extracted) |
| Holdable mesh | SK_Bandage_Long (material MI_Bandage_Long) | SK_Medkit_SuperBandage |
| Animation set | AnimSet_Bandage | AnimSet_SuperBandage |
| Audio | ID_Bandage_Audio | ID_IFAK_Audio |
| Spatial tracker | Applies only to friendlies (`bShouldOnlyApplyToFriendly` = True); checks WorldGrid.Layer.Character | Same class, same friendly-only setting |

Input behaviour is shared: the primary-use input (`Input.NamedActions.Appliable.PrimaryUse`) maps to `WDItemInputBehavior_ActivateAppliableAction` with `Action.Appliable.Bandage.PrimaryUse`, secondary use maps to `...SecondaryUse`, and the completion action is bound to the same two uses. Inspection (`Action.Item.Inspect`) is bound on the item too. The shared key set is [`IMC_Appliable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/ItemExtensionDefaults/IMC_Appliable.json) (section 11).

Other consumable item (not decoded further): [`Placeables/AmmoCrate/ID_AmmoCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Placeables/AmmoCrate/ID_AmmoCrate.json) (2x2 grid, a `WDItemExtensionData_Placeable` with collision size, placeable class and init data). Those three values are present in the dump but were not extracted.

---

## 6. Throwables ([`Throwable/Grenades`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Throwable/Grenades))

| Asset | Display | Weight | ThrowableClass | Throw velocity | Resource used |
|---|---|---|---|---|---|
| ID_M67Grenade | M67 Frag Grenade | 0.4 | B_FragGrenade | 2500 | Id.Item.M67Grenade x1 |
| ID_M67Grenade_Gold | Golden Grenade | - | B_GoldFragGrenade | 2200 | Id.Item.GoldM67Grenade x1 |

Both throws use `Action.Throw.Primary`. Pitch and velocity curves: [`CRV_ThrowPitch_Overarm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Throwable/Curves/CRV_ThrowPitch_Overarm.json), [`CRV_ThrowPitch_OverarmStrong`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Throwable/Curves/CRV_ThrowPitch_OverarmStrong.json), [`CRV_ThrowPitch_Underarm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Throwable/Curves/CRV_ThrowPitch_Underarm.json) (pitch), and [`CRV_ThrowVelocity_OverarmStrong`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Throwable/Curves/CRV_ThrowVelocity_OverarmStrong.json), [`CRV_ThrowVelocity_Underarm`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Throwable/Curves/CRV_ThrowVelocity_Underarm.json) (velocity). `DropSpawnOffset` is (0, 0, -40) on the M67. The gold variant has no `Weight` property. Its drop and throw data share the M67 audio ([`ID_M67Grenade_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Throwable/Grenades/M67_Grenade/ID_M67Grenade_Audio.json)). Full throw action fields (VelocityCurve reference, bUseConsistentVelocity) are present in the dump but only partly decoded here.

---

## 7. Ammunition ([`Resources/Ammo`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Resources/Ammo))

### 7a. Calibers

Max stack is the inventory stack limit (`MaxStackSize`). Overrides apply to a slot tag (vehicle storage, vehicle type). Grid is the item footprint. Caliber rows: 98 primary assets in the folder (94 items, 3 audio assets, 1 debug projectile).

| Caliber folder | Variants | Display | Max stack | Overrides | Grid | Projectile asset |
|---|---|---|---|---|---|---|
| 120x570mm | 1 | 120x570mm | 5 | - | 3x2 | DA_120x570mm_ProjectileData |
| 120x800mm | 1 | 120x800mm | 10 | - | 3x2 | DA_120x800mm_Standard_ProjectileData |
| 122mm | 1 | 122mm | 3 | - | 6x2 | DA_122mm_ProjectileData |
| 125x570mm | 1 | 125x570mm | 5 | - | 3x2 | DA_125x570mm_ProjectileData |
| 12Guage | 5 | 12g, 7mm Buckshot, Rifled Slug | 24 | - | 2x1 | DA_12g_RifledSlug, DA_7mmBuckshot |
| 155mm | 6 | 155mm, 155mm Standard (+SB), 155mm Expensive (+SB), 155mm (SB) | 10 (SB Expensive: 30) | - | 3x2 | DA_155mm_Standard, DA_155mm_Expensive (+SB variants) |
| 20x102mm | 1 | 20x102mm | 100 | - | 2x2 | DA_20x102mm |
| 308 | 6 | .308 (+T, AP, AP T, HP, HP T) | 40 | Vehicle.Storage 150 | 2x1 | DA_308Winchester_ProjectileData |
| 30mm | 1 | 30mm | 200 | Vehicle.Storage 200 | not set | DA_30mm_ProjectileData |
| 338NormaMagnum | 6 | .338 Winchester (+AP, HP, tracer variants) | 30 | - | 2x1 | DA_338Norman_ProjectileData |
| 35x228mm | 1 | 35x228mm | 75 | - | 2x2 | DA_35x228mm_ProjectileData |
| 40mm | 1 | 40mm | 1 | - | 2x1 | DA_40mm_ProjectileData |
| 45ACP | 6 | .45 ACP (+AP, HP) | 60 | - | 2x1 | DA_45ACP_ProjectileData |
| 45Colt | 6 | .45 Colt (+AP, HP, tracer) | 30 | - | not set | DA_45Colt_ProjectileData |
| 50AE | 6 | .50 AE (+AP, HP, tracer) | 30 | - | 2x1 | DA_50AE_ProjectileData |
| 50Cal | 6 | .50 Cal (+AP, HP, tracer) | 20 (AP variants 30) | Tracer: Vehicle.Storage 50, Type.Vehicle 50 | 2x1 | DA_50Cal_ProjectileData |
| 545mm | 6 | 5.45mm (+AP, HP, tracer) | 80 | - | 2x1 | DA_545mm_ProjectileData |
| 556mm | 6 | 5.56mm (+AP, HP, tracer) | 80 | Vehicle.Storage 150 | 2x1 | DA_556mm_ProjectileData |
| 70mm | 1 | 70mm | not set | - | 3x1 | DA_70mm_ProjectileData |
| 72mm | 1 | 72mm | not set | - | 2x1 | DA_72mm_ProjectileData |
| 762mm | 6 | 7.62mm (+AP, HP, tracer) | 60 | - | 2x1 | DA_762mm_ProjectileData |
| 762x51mm | 6 | 7.62x51mm | 100 | Type.Vehicle 150 | 2x1 | DA_762x51mm_ProjectileData |
| 762x54mm | 6 | 7.62x54mm (+AP, HP, tracer) | 40 | Tracer variants: Vehicle.Storage 150, Type.Vehicle 150 | 2x1 | DA_762x54mm_ProjectileData |
| 84mm | 1 | 84mm | not set | - | 2x1 | DA_84mm_ProjectileData |
| 93mm | 1 | 93mm | not set | - | 3x1 | DA_93mm_ProjectileData |
| 9mm | 6 | 9mm (+AP, HP, tracer) | 100 (some 80) | - | 2x1 | DA_9mm_ProjectileData |
| DebugHomingRocket | 2 | RocketTesting 84mm | 99 | - | not set | DA_DebugHomingRocketData (see 7c) |
| Rockets | 1 | (no display) | not set | - | not set | not set |

Variant naming: the base round has no suffix, and the others add `_ArmorPiercing`, `_HollowPoint`, and `_Tracer`. Items with `Sandbox` in the ItemId (e.g. `ID.Item.155mm.Sandbox`, [`ID_155mm_SB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/155mm/ID_155mm_SB.json)) are test variants.

Weight (`BHInventoryFragment_Weight`) is set on only a handful of rounds: 120x570mm 24.0, 125x570mm 24.0, 35x228mm 1.56, 40mm 0.28, 155mm Expensive 42.0. The rest have no weight property. The unit is not stated.

### 7b. Ammo Item Data

Each round is a `BHInventoryItemDefinition` with a `BHInventoryFragment_Stackable`, a `WDInventoryFragment_Projectile` (pointing to a `WDProjectileData` in `GameMechanics`), a `WDInventoryFragment_Audio`, and a `CustomShape`. The projectile asset is **outside** this folder, so ballistics for ordinary rounds are not in this category.

### 7c. The One Decoded Projectile ([`DA_DebugHomingRocketData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/DebugHomingRocket/DA_DebugHomingRocketData.json))

| Field | Value |
|---|---|
| ProjectileId | Item.Caliber.84mm |
| BaseDamage | 47 |
| Damage tag | Meta.Damage.Bullet.545mm |
| Length / Diameter / Mass | 37 / 4 / 1 |
| Drag model | [`CT_Projectile_DragCoefficients`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/Curves/CT_Projectile_DragCoefficients.json) row "GC (Cylinder)" |
| Typical speed / thrust speed | 100000 / 20000 |
| Max lifetime / total fuel / burn rate | 20 s / 100 / 1.0 |
| Guidance | Guided, MaxTurnAngle 2.0 |
| Tracer chance / penetration | 1.0 / False |
| Gravity | Not affected |

---

## 8. Vehicle Items

### 8a. Vehicle Cargo ([`Vehicles/Storage`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Vehicles/Storage))

| Asset | Display | Container slot | Container grid | Filter |
|---|---|---|---|---|
| ID_VehicleStorageSmall | Small Vehicle Storage | Inventory.Slot.Vehicle.Storage | 1x1 | BlockList (none) |
| ID_VehicleStorageMedium | Medium Vehicle Storage | Inventory.Slot.Vehicle.Storage | 1x1 | BlockList (none) |
| ID_VehicleStorageIntermediate | Intermediate Vehicle Storage | Inventory.Slot.Vehicle.Storage | 4x2 | BlockList (none) |
| ID_VehicleStorageLarge | Large Vehicle Storage | Inventory.Slot.Vehicle.Storage | 1x1 | BlockList (Item.Ammo) |

The Large storage refuses ammo. Its container is listed as 1x1 in the dump, which is unexpected for a large bin; treat the grid as reported.

### 8b. Vehicle Weapons and Turrets (`Vehicles/Weapons`, 16 items)

Each turret item is a `BHInventoryItemDefinition` with a `BHInventoryFragment_SubSlotSupport` whose single container accepts one caliber (AllowList on `Item.Ammo` plus `Item.Caliber.*`). The stack value is the container's `MaxSlotAmountStackSize`, which reads as the ammo capacity for that mount (interpretation, see section 2a).

| Asset | Display | Ammo caliber | Stack |
|---|---|---|---|
| ID_Heavy_MountedMachineGun | Machine Gun (Heavy tank MG) | 556mm | 150 |
| ID_Humvee_RingTurret | Machine Gun (Humvee ring) | 556mm | 150 |
| ID_Ural_Turret | Machine Gun (Ural) | 556mm | 150 |
| ID_VehicleRingTurret | Machine Gun | 556mm | 150 |
| ID_VehicleTurretMachineGun | Machine Gun | 308Win | 150 |
| ID_VehicleHelicopterCannon | Machine Gun (helicopter cannon) | 30mm | 150 |
| ID_VehicleHelicopterRockets | Rockets | 122mm | 12 |
| ID_VehicleHelicopterRockets_ROT_03 | Rockets (ROT_03) | 122mm | 6 |
| ID_VehicleTurretAntiair | Anti-Air Turret | 35x228mm | 150 |
| ID_VehicleTurretArtillery | Artillery Turret | 155mm | 1 |
| ID_VehicleTurretArtillery_SB | Artillery Turret (sandbox) | 155mm | 1 |
| ID_VehicleTurretHeavy | Heavy Turret | 120x570mm | 1 |
| ID_MountedMachineGun_TNK_04 | Machine Gun | 50Cal | 60 |
| ID_VehicleTurretMachineGun_TNK_04 | Machine Gun | 762x54mm | 150 |
| ID_VehicleTurret_TNK_04 | Heavy Turret | 125x570mm | 1 |
| ID_WHL_08_RingTurret | Machine Gun | 50Cal | 60 |

### 8c. Launcher Test Barrels ([`Weapons/Launcher`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Weapons/Launcher))

| Asset | Display | Weight | Notes |
|---|---|---|---|
| ID_ArtilleryBarrelTest | Artillery Barrel Test | 50 | Ranged-weapon extension: default `Attribute.Gameplay.Weapon.AimTime` 0.5, damage tag `Meta.Damage.Weapon.Vehicle.Turret.Artillery`, weapon stats asset [`DA_ArtilleryBarrelTest_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/ArtilleryBarrelTest/Data/DA_ArtilleryBarrelTest_Stats.json) (not in dump) |
| ID_TankBarrelTest | Tank Barrel Test (ItemId Id.Item.LeapordBarrel) | 50 | Chamber and muzzle child slots, AllowList |

These two are the only items with a `WDItemExtensionData_RangedWeapon`, and their stats are in an external asset.

### 8d. Fists (`Weapons/Fists`)

ID_Fists (ItemId Id.Item.Fists). Melee damage tag `Meta.Damage.Utility.Fists`. Player effect `GE_Player_Fists`. Input context [`IMC_Fists`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IMC_Fists.json). Animation set [`AnimSet_Fists`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Fists/AnimSet_Fists.json). Aim-assist extension references [`DA_AimAssistSettings_Melee`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/DA_AimAssistSettings_Melee.json) and [`DA_AimAssistFilter`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/DA_AimAssistFilter.json). The two test barrels in section 8c carry the same extension type.

---

## 9. Aim Assist (`Weapons/DA_AimAssistSettings_*`)

Eight weapon-class settings and one shared filter. Values are as stored, with no units given. Blank means the key is absent for that class.

| Key | Filter | AR | LMG | Melee | Pistol | RPG | SMG | SR | Shotgun |
|---|---|---|---|---|---|---|---|---|---|
| TargetRange | 30000 | 30000 | 30000 | 800 | - | 0 | 20000 | 40000 | 20000 |
| AssistInnerReticleWidth | - | 900 | 900 | 24 | 300 | 0 | 600 | 1200 | 600 |
| AssistInnerReticleHeight | - | 720 | 720 | 19.2 | 240 | 0 | 480 | 960 | 480 |
| AssistOuterReticleWidth | - | 2700 | 2700 | 72 | 900 | 0 | 1800 | 3600 | 1800 |
| AssistOuterReticleHeight | - | 2160 | 2160 | 57.6 | 720 | 0 | 1440 | 2880 | 1440 |
| TargetingReticleWidth | - | 2700 | 2700 | 72 | 900 | 0 | 1800 | 3600 | 1800 |
| TargetingReticleHeight | - | 2160 | 2160 | 57.6 | 720 | 0 | 1440 | 2880 | 1440 |
| ReticleDepth | - | 30000 | 30000 | 800 | 10000 | 0 | 20000 | 40000 | 20000 |
| MaxNumberOfTargets | - | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| MinAssistWeight | - | 0.125 | 0.125 | 0.125 | 0.125 | 0.125 | 0.125 | 0.125 | 0.125 |
| SensitivityScaleADS | - | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 1.0 | 1.0 | 1.0 |
| PullInnerStrengthHip | - | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 1.0 | 0 | 1.0 |
| SlowOuterStrengthAds | - | 0.3 | 0.3 | 0 | 0.3 | 0 | 0.3 | 0.2 | 0.3 |
| PullInnerStrengthAds | - | 2.0 | 2.0 | 0 | 2.0 | 0 | 2.0 | 2.0 | 2.0 |
| PullOuterStrengthHip | - | - | - | - | - | 0 | - | 0 | - |
| SlowInnerStrengthHip | - | - | - | 0.36 | - | 0 | - | 0 | - |
| PullOuterStrengthAds | - | 1.0 | 1.0 | 0 | 1.0 | 0 | 1.0 | 1.0 | 1.0 |
| SlowInnerStrengthAds | - | 0.6 | 0.6 | 0 | 0.6 | 0 | 0.6 | 0.4 | 0.6 |
| SlowOuterStrengthHip | - | 0.3 | 0.3 | 0.19 | 0.3 | 0 | 0.3 | 0 | 0.3 |
| PullLerpInRate / OutRate | - | 10 / 8 | 10 / 8 | 10 / 8 | 10 / 8 | 0 | 10 / 8 | 10 / 8 | 10 / 8 |
| SlowLerpInRate / OutRate | - | 10 / 8 | 10 / 8 | 10 / 8 | 10 / 8 | 0 | 10 / 8 | 10 / 8 | 10 / 8 |
| PullMaxRotationRate | - | 90 | 90 | 90 | 90 | - | 90 | 90 | 90 |
| SlowMinRotationRate | - | - | - | - | - | - | - | - | - |
| PullMode | - | - | - | - | - | Off | - | - | - |
| PullModeADS | - | - | - | - | - | Off | - | - | - |
| TargetWeightCurve | - | C_AimAssistTargetWeightCurve (shared) | | | | | | | |

Curves referenced per class (values not in this category): the hipfire `PullStrengthDistanceCurve` and `SlowStrengthDistanceCurve` now point to the shared [`C_AimAssistPullStrengthDistanceCurve_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Default.json) and [`C_AimAssistSlowStrengthDistanceCurve_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurve_Default.json) for AR, LMG, Melee, Pistol, SMG and Shotgun. The ADS variants stay per class, and SR keeps its `_Sniper` curves. Every class except RPG now uses [`C_AimAssistReticleEdgeFalloff_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistReticleEdgeFalloff_Default.json) for its reticle edge falloff. The SR uses [`C_AimAssistPullStrengthDistanceCurve_Sniper`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistPullStrengthDistanceCurve_Sniper.json) for ADS. Two curve names have a missing underscore: [`C_AimAssistSlowStrengthDistanceCurvePistol_ADS`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurvePistol_ADS.json) and [`C_AimAssistSlowStrengthDistanceCurveShotgun_ADS`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/BHAimAssist/Content/AimAssist/C_AimAssistSlowStrengthDistanceCurveShotgun_ADS.json). These are the names as stored.

The RPG setting is zero across most fields, and RPG has `PullMode` set to `Off`. SR no longer sets `PullMode`, and Melee no longer sets `PullModeADS`. Whether assist is intentionally disabled for those classes cannot be confirmed from the dump.

Other settings: `bFOVReticleScaling` is False for every class that sets it. `bApplySlowing`, `bUseDynamicSlow`, and `bApplyStrafePullScale` appear only on the RPG and are False. Every class sets `MaxNumberOfTargets` = 8.

---

## 10. Placed and Other Items

| Asset | Display | Grid | Notes |
|---|---|---|---|
| ID_AmmoCrate | Ammo Crate | 2x2 | Placeable with collision size, placeable class and init data (values not extracted) |

---

## 11. Curves, Curve Tables, and Shared Input

| Group | Count | Assets |
|---|---|---|
| Throw curves ([`Throwable/Curves`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Throwable/Curves)) | 5 CurveFloat | CRV_ThrowPitch_Overarm (4 keys), CRV_ThrowPitch_OverarmStrong (4), CRV_ThrowPitch_Underarm (8), CRV_ThrowVelocity_OverarmStrong (3), CRV_ThrowVelocity_Underarm (4) |
| ADS curves ([`Weapons/Curves/ADS`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Weapons/Curves/ADS)) | 6 CurveFloat | CF_Animation_ADSIn_Curve, CF_Animation_ADSIn_Linear, CF_Animation_ADSOut_Curve, CF_Animation_ADSOut_Linear, CF_Animation_ADSIn_WEPN_029_Curve, and one more not listed in this pass |
| Aim sway (`Weapons/Curves/AimSway/*`) | 15 CurveFloat | Per-class sway multipliers ([`CRV_WeaponAnimSwayMultiplier_AR_Harsh`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/AimSway/AR/CRV_WeaponAnimSwayMultiplier_AR_Harsh.json), `_AR_Moderate`, `_Bow`, `_DMR_Harsh`, `_LMG_Harsh`, `_Launcher`, `_SMG`, `_Shotgun`, and others), plus [`CF_AimSway_Stabilization_PlayerSpeed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/AimSway/CF_AimSway_Stabilization_PlayerSpeed.json) and `_SR` |
| Curve tables | 2 | [`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json) (`Weapons/Curves`), with rows per stance: `Launcher.Stand`, `Launcher.Crouch`, `Launcher.Prone`. [`CT_Projectile_DragCoefficients`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/Curves/CT_Projectile_DragCoefficients.json) ([`Resources/Ammo/Curves`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Resources/Ammo/Curves)), with rows such as "GC (Cylinder)". |
| Input mapping | 1 | [`IMC_Appliable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/ItemExtensionDefaults/IMC_Appliable.json) (UDataAsset; primary-use, secondary-use and inspect keys for consumables) |

---

## 12. Combining Values

- **Magazine rounds available** = the magazine's container `MaxSlotAmountStackSize` (section 2a). Ammo stacks inside the magazine's container and is limited by that container's allow list (the caliber tag).
- **Inventory stack size for a round** = `MaxStackSize`, unless the slot tag is listed in `MaxStackSizeOverrides`. For ammo, `Vehicle.Storage` and `Type.Vehicle` override to 150 on the 308, 556mm, 762x51mm and 762x54mm tracer lines, and to 50 on the .50 Cal tracer. The 30mm round overrides `Vehicle.Storage` to 200.
- **Carry weight** = `BHInventoryFragment_Weight.Weight` (unit not stated). Items with no weight property have no value in the dump, so their total cannot be read from this category.
- **Attachment on a weapon** = the attachment's `AttachmentType` tag must match a weapon child slot's `ContainerIdentifier`, and the attachment's bone comes from its archetype (section 3a).
- **Aim assist per shot** = the weapon-class settings (section 9) combined with the class's distance curves; the curve values are outside this category.

---

## 13. Still Not Pulled / Limitations

- **Base weapon definitions are absent.** `Weapons/AR` holds only components. The receiver and full gun items (M4, AK74-M, Glock 17, Vector, M249, and so on) are not in this folder, so per-weapon fire rate, damage, and recoil are not here.
- **Weapon stats and projectile ballistics are external.** `WDWeaponStatsData` (e.g. [`DA_ArtilleryBarrelTest_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/RocketLauncher/ArtilleryBarrelTest/Data/DA_ArtilleryBarrelTest_Stats.json)) and every `WDProjectileData` except [`DA_DebugHomingRocketData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/DebugHomingRocket/DA_DebugHomingRocketData.json) live in other folders, so damage and velocity for ordinary rounds are not in this category.
- **Weight unit not stated.** The dump gives values (0.08 to 42.0) without a unit. Assume it is the game's internal weight unit until confirmed.
  - **See [`docs/UNITS.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md)** for the project-wide units reference (UE 5.7 defaults + Wardogs-specific suffixes).
- **Weight missing on most items.** Only 47 of 193 items have a weight value. The other items carry the fragment but no property, so the default is unknown.
- **Grid orientation not confirmed.** `CustomShape.Dimensions` and `GridSize` are read as X x Y. Whether X is columns or rows is not verified.
- **Magazine capacity is an inference.** `MaxSlotAmountStackSize` on a magazine container matches the magazine's name in every case checked, but the dump does not label it as capacity.
- **Unnamed property keys omitted.** Keys of the form `_aaa…` (21 letters a–p; `_aaa..._$HEX$_$N$` before 2026-10-18; several per aim-assist asset and a few on containers) are internal and were skipped. Their meaning is unknown.
  - **SDK (2026-10-16):** aim-assist asset classes live in [`BHAimAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/BHAimAssist_structs.hpp). Key resolved types:
    - [`EBHAimAssistPullMode`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/BHAimAssist_structs.hpp) enum (5 values): `All = 0`, `MovementOnly = 1`, `LookOnly = 2`, `Off = 3`, `EBHAimAssistPullMode_MAX = 4` — this is the enum behind any "pull mode" field in aim-assist exports
    - [`FBHAimAssistTargetOptions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/BHAimAssist_structs.hpp) struct (0x30 bytes): `AssociatedTags` (`FGameplayTagContainer`) + `bIsActive` (bool) + padding
    - [`FBHAimAssistTargetData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/sdk/raw/BHAimAssist_structs.hpp) struct (0xA0 bytes): Dumper-7 was unable to resolve any inner field names — remains opaque via static means
  - Per-asset `_aaa…` keys are Blueprint-generated property names that even Dumper-7 could not symbolicate against; resolving each would require per-asset context.
- **Display names missing on 14 items.** Some have no `DisplayName`, and where a `DisplayName` exists only the `SourceString` is shown; the localization table is not dumped.
- **Holdable and placeable details not decoded.** Holdable mesh, animation and crosshair fields are only partly summarised. The ammo crate's placeable class and init data were not extracted.
- **Full throw and consumable action data.** The `AppliableActionData` and `ThrowActions` arrays are present but only partly decoded (required states, velocity curve references).
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Aim-assist RPG and SR zeros.** Several fields are 0 or absent for RPG and SR. The dump does not say whether those classes are intentionally unassisted.
- **Vehicle container sizes.** The Large Vehicle Storage container is reported as 1x1 with an ammo block. The dump does not say whether that matches the in-game footprint.

## Resources and ammunition

The `Resources` folder holds 94 item definitions, almost all ammunition, plus 5 support assets (3 audio data assets, one projectile data asset and one curve table) that are not items and have no row. The table lists each item definition with its tag, display name, stack size, inventory shape, weight, caliber and vendor price where the data sets them.

**Data** (generated from the JSON; `—` means the value is not in the export, not zero):

<!-- resource_tables items -->
| Asset | Folder | Item tag | Display name | Kind | Max stack | Inventory (X x Y) | Weight | Caliber tag | Vendor price |
|---|---|---|---|---|---|---|---|---|---|
| `ID_120x570mm` | Ammo/120x570mm | `ID.Item.120x570mm` | 120mm HEAT-MP Shell | ammo | 5 | 3 x 2 | 24 | Item.Caliber.120x570mm | 210 |
| `ID_120x800mm` | Ammo/120x800mm | `Id.Item.120x800mm` | 81mm | ammo | 10 | 3 x 2 | — | Item.Caliber.120x800mm | 600 |
| `ID_122mm` | Ammo/122mm | `Id.Item.122mm` | 122mm HE Rocket | ammo | 3 | 6 x 2 | — | Item.Caliber.122mm | 450 |
| `ID_125x570mm` | Ammo/125x570mm | `ID.Item.125x570mm` | 125mm HEAT-MP Shell | ammo | 5 | 3 x 2 | 24 | Item.Caliber.125x570mm | 210 |
| `ID_12g` | Ammo/12Guage | `Id.Item.12g` | 12g | ammo | 24 | 2 x 1 | — | Item.Caliber.12g | — |
| `ID_7mmBuckshot` | Ammo/12Guage/7mmBuck | `Id.Item.12g.7mmBuck` | 12g 7mm Buckshot  | ammo | 24 | 2 x 1 | — | Item.Caliber.12g | 60 |
| `ID_12g_RifledSlug` | Ammo/12Guage/Slug | `Id.Item.12g.RifledSlug` | 12g Rifled Slug | ammo | 24 | 2 x 1 | — | Item.Caliber.12g | 200 |
| `ID_155mm` | Ammo/155mm | `ID.Item.155mm` | 155mm HE Shell | ammo | — | 3 x 2 | — | Item.Caliber.155mm | 200 |
| `ID_155mm_Expensive` | Ammo/155mm | `ID.Item.155mm.Expensive` | 155mm HE Shell | ammo | — | 3 x 2 | 42 | Item.Caliber.155mm.Expensive | 120 |
| `ID_155mm_Expensive_SB` | Ammo/155mm | `ID.Item.155mm.Expensive.Sandbox` | 155mm Expensive (SB) | ammo | 30 | 3 x 2 | — | Item.Caliber.155mm.Expensive | 600 |
| `ID_155mm_SB` | Ammo/155mm | `ID.Item.155mm.Sandbox` | 155mm (SB) | ammo | 10 | 3 x 2 | — | Item.Caliber.155mm | 600 |
| `ID_155mm_Standard` | Ammo/155mm | `ID.Item.155mm.Standard` | 155mm HE Shell | ammo | 10 | 3 x 2 | — | Item.Caliber.155mm.Standard | 120 |
| `ID_155mm_Standard_SB` | Ammo/155mm | `ID.Item.155mm.Standard.Sandbox` | 155mm Standard (SB) | ammo | 10 | 3 x 2 | — | Item.Caliber.155mm.Standard | 600 |
| `ID_20x102mm` | Ammo/20x102mm | `Id.Item.20x102mm` | 20x102mm | ammo | 100 | 2 x 2 | — | Item.Caliber.20x102mm | 600 |
| `ID_308` | Ammo/308 | `Id.Item.308Win` | .308 Win  | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.308Win | 40 |
| `ID_308_ArmorPiercing` | Ammo/308 | `Id.Item.308Win.ArmorPiercing` | .308 Win Armor Piercing (AP) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.308Win | 180 |
| `ID_308_ArmorPiercing_Tracer` | Ammo/308 | `Id.Item.308Win.ArmorPiercing.Tracer` | .308 Win Armor Piercing (AP) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.308Win | 180 |
| `ID_308_HollowPoint` | Ammo/308 | `Id.Item.308Win.HollowPoint` | .308 Win  | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.308Win | 70 |
| `ID_308_HollowPoint_Tracer` | Ammo/308 | `Id.Item.308Win.HollowPoint.Tracer` | .308 Win Flesh Damage (HP) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.308Win | 70 |
| `ID_308_Tracer` | Ammo/308 | `Id.Item.308Win.Tracer` | .308 Win Standard (FMJ) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.308Win | 40 |
| `ID_30mm` | Ammo/30mm | `Id.Item.30mm` | 30mm HE Cannon | ammo | 50 (overrides: Inventory.Slot.Vehicle.Storage 200) | 2 x 2 | — | Item.Caliber.30mm | 500 |
| `ID_338Nor_ArmorPiercing` | Ammo/338NormaMagnum | `Id.Item.338Nor.ArmourPiercing` | .338 AP | ammo | 30 | 2 x 1 | — | Item.Caliber.338Nor | — |
| `ID_338Nor_HollowPoint` | Ammo/338NormaMagnum | `Id.Item.338Nor.HollowPoint` | .338 HP | ammo | 30 | 2 x 1 | — | Item.Caliber.338Nor | — |
| `ID_338Nor_HollowPoint_Tracer` | Ammo/338NormaMagnum | `Id.Item.338Nor.HollowPoint.Tracer` | .338 HP (T) | ammo | 30 | 2 x 1 | — | Item.Caliber.338Nor | — |
| `ID_338Nor_Tracer` | Ammo/338NormaMagnum | `Id.Item.338Nor.Tracer` | .338 (T) | ammo | 30 | 2 x 1 | — | Item.Caliber.338Nor | — |
| `ID_338Norm_ArmorPiercing_Tracer` | Ammo/338NormaMagnum | `Id.Item.338Nor.ArmourPiercing.Tracer` | .338 AP (T) | ammo | 30 | 2 x 1 | — | Item.Caliber.338Nor | — |
| `ID_338NormaMagnum` | Ammo/338NormaMagnum | `Id.Item.338Nor` | .338 | ammo | 30 | 2 x 1 | — | Item.Caliber.338Nor | — |
| `ID_35x228mm` | Ammo/35x228mm | `ID.Item.35x228mm` | 35x228mm Anti-Air Cannon | ammo | 75 | 2 x 2 | 1.56 | Item.Caliber.35x228mm | 200 |
| `ID_40mm` | Ammo/40mm | `Id.Item.40mm` | 40mm  | ammo | 1 | 2 x 1 | 0.28 | Item.Caliber.40mm | 100 |
| `ID_45ACP` | Ammo/45ACP | `Id.Item.45ACP` | .45 ACP | ammo | 60 | 2 x 1 | — | Item.Caliber.45ACP | 10 |
| `ID_45ACP_ArmorPiercing` | Ammo/45ACP | `Id.Item.45ACP.ArmorPiercing` | .45 ACP Armor Piercing (AP) | ammo | 60 | 2 x 1 | — | Item.Caliber.45ACP | 20 |
| `ID_45ACP_ArmorPiercingTracer` | Ammo/45ACP | `Id.Item.45ACP.ArmorPiercing.Tracer` | .45 ACP Armor Piercing (AP) | ammo | 60 | 2 x 1 | — | Item.Caliber.45ACP | 20 |
| `ID_45ACP_HollowPoint` | Ammo/45ACP | `Id.Item.45ACP.HollowPoint` | .45 ACP Flesh Damage (HP) | ammo | 60 | 2 x 1 | — | Item.Caliber.45ACP | 15 |
| `ID_45ACP_HollowPointTracer` | Ammo/45ACP | `Id.Item.45ACP.HollowPoint.Tracer` | .45 ACP Flesh Damage (HP) | ammo | 60 | 2 x 1 | — | Item.Caliber.45ACP | 15 |
| `ID_45ACP_Tracer` | Ammo/45ACP | `Id.Item.45ACP.Tracer` | .45 ACP Standard (FMJ) | ammo | 60 | 2 x 1 | — | Item.Caliber.45ACP | 10 |
| `ID_45Colt` | Ammo/45Colt | `Id.Item.45Colt` | .45 Colt | ammo | 30 | — | — | Item.Caliber.45Colt | 33 |
| `ID_45Colt_ArmorPiercing` | Ammo/45Colt | `Id.Item.45Colt.ArmorPiercing` | .45 Colt Armor Piercing (AP) | ammo | 30 | — | — | Item.Caliber.45Colt | 66 |
| `ID_45Colt_ArmorPiercing_Tracer` | Ammo/45Colt | `Id.Item.45Colt.ArmorPiercing.Tracer` | .45 Colt Armor Piercing (AP) | ammo | 30 | — | — | Item.Caliber.45Colt | 66 |
| `ID_45Colt_HollowPoint` | Ammo/45Colt | `Id.Item.45Colt.HollowPoint` | .45 Colt Flesh Damage (HP) | ammo | 30 | — | — | Item.Caliber.45Colt | 50 |
| `ID_45Colt_HollowPoint_Tracer` | Ammo/45Colt | `Id.Item.45Colt.HollowPoint.Tracer` | .45 Colt Flesh Damage (HP) | ammo | 30 | — | — | Item.Caliber.45Colt | 50 |
| `ID_45Colt_Tracer` | Ammo/45Colt | `Id.Item.45Colt.Tracer` | .45 Colt Standard (FMJ) | ammo | 30 | — | — | Item.Caliber.45Colt | 33 |
| `ID_50AE` | Ammo/50AE | `Id.Item.50AE` | 50AE | ammo | 30 | 2 x 1 | — | Item.Caliber.50AE | 20 |
| `ID_50AE_ArmorPiercing` | Ammo/50AE | `Id.Item.50AE.ArmorPiercing` | 50AE Armor Piercing (AP) | ammo | 30 | 2 x 1 | — | Item.Caliber.50AE | 90 |
| `ID_50AE_ArmorPiercing_Tracer` | Ammo/50AE | `Id.Item.50AE.ArmorPiercing.Tracer` | 50AE Armor Piercing (AP) | ammo | 30 | 2 x 1 | — | Item.Caliber.50AE | 90 |
| `ID_50AE_HollowPoint` | Ammo/50AE | `Id.Item.50AE.HollowPoint` | 50AE Flesh Damage (HP) | ammo | 30 | 2 x 1 | — | Item.Caliber.50AE | 35 |
| `ID_50AE_HollowPoint_Tracer` | Ammo/50AE | `Id.Item.50AE.HollowPoint.Tracer` | 50AE Flesh Damage (HP) | ammo | 30 | 2 x 1 | — | Item.Caliber.50AE | 35 |
| `ID_50AE_Tracer` | Ammo/50AE | `Id.Item.50AE.Tracer` | 50AE Standard (FMJ) | ammo | 30 | 2 x 1 | — | Item.Caliber.50AE | 20 |
| `ID_50Cal` | Ammo/50Cal | `Id.Item.50Cal` | .50Cal | ammo | 20 | 2 x 1 | — | Item.Caliber.50Cal | 250 |
| `ID_50Cal_ArmorPiercing` | Ammo/50Cal | `Id.Item.50Cal.ArmorPiercing` | .50 Cal AP | ammo | 30 | 2 x 1 | — | Item.Caliber.50Cal | 500 |
| `ID_50Cal_ArmorPiercing_Tracer` | Ammo/50Cal | `Id.Item.50Cal.ArmorPiercing.Tracer` | .50 Cal AP (T) | ammo | 30 | 2 x 1 | — | Item.Caliber.50Cal | 500 |
| `ID_50Cal_HollowPoint` | Ammo/50Cal | `Id.Item.50Cal.HollowPoint` | .50 Cal HP | ammo | 30 | 2 x 1 | — | Item.Caliber.50Cal | 375 |
| `ID_50Cal_HollowPoint_Tracer` | Ammo/50Cal | `Id.Item.50Cal.HollowPoint.Tracer` | .50 Cal HP (T) | ammo | 30 | 2 x 1 | — | Item.Caliber.50Cal | 375 |
| `ID_50Cal_Tracer` | Ammo/50Cal | `Id.Item.50Cal.Tracer` | .50Cal Standard (FMJ) | ammo | 20 (overrides: Inventory.Slot.Vehicle.Storage 50, Inventory.Type.Vehicle 50) | 2 x 1 | — | Item.Caliber.50Cal | 250 |
| `ID_545mm` | Ammo/545mm | `Id.Item.545mm` | 5.45x39mm | ammo | 80 | 2 x 1 | — | Item.Caliber.545mm | 15 |
| `ID_545mm_ArmorPiercing` | Ammo/545mm | `Id.Item.545mm.ArmorPiercing` | 5.45mm Armor Piercing (AP) | ammo | 80 | 2 x 1 | — | Item.Caliber.545mm | 40 |
| `ID_545mm_ArmorPiercing_Tracer` | Ammo/545mm | `Id.Item.545mm.ArmorPiercing.Tracer` | 5.45mm Armor Piercing (AP) | ammo | 80 | 2 x 1 | — | Item.Caliber.545mm | 40 |
| `ID_545mm_HollowPoint` | Ammo/545mm | `Id.Item.545mm.HollowPoint` | 5.45mm Flesh Damage (HP) | ammo | 80 | 2 x 1 | — | Item.Caliber.545mm | 25 |
| `ID_545mm_HollowPoint_Tracer` | Ammo/545mm | `Id.Item.545mm.HollowPoint.Tracer` | 5.45mm Flesh Damage (HP) | ammo | 80 | 2 x 1 | — | Item.Caliber.545mm | 25 |
| `ID_545mm_Tracer` | Ammo/545mm | `Id.Item.545mm.Tracer` | 5.45mm Standard (FMJ) | ammo | 80 | 2 x 1 | — | Item.Caliber.545mm | 15 |
| `ID_556mm` | Ammo/556mm | `Id.Item.556mm` | 5.56x45mm | ammo | 80 (overrides: Inventory.Slot.Vehicle.Storage 150) | 2 x 1 | — | Item.Caliber.556mm | 15 |
| `ID_556mm_ArmorPiercing` | Ammo/556mm | `Id.Item.556mm.ArmorPiercing` | 5.56mm Armor Piercing (AP) | ammo | 80 (overrides: Inventory.Slot.Vehicle.Storage 150) | 2 x 1 | — | Item.Caliber.556mm | 40 |
| `ID_556mm_ArmorPiercing_Tracer` | Ammo/556mm | `Id.Item.556mm.ArmorPiercing.Tracer` | 5.56mm Armor Piercing (AP) | ammo | 80 (overrides: Inventory.Slot.Vehicle.Storage 150) | 2 x 1 | — | Item.Caliber.556mm | 40 |
| `ID_556mm_HollowPoint` | Ammo/556mm | `Id.Item.556mm.HollowPoint` | 5.56mm Flesh Damage (HP) | ammo | 80 (overrides: Inventory.Slot.Vehicle.Storage 150) | 2 x 1 | — | Item.Caliber.556mm | 25 |
| `ID_556mm_HollowPoint_Tracer` | Ammo/556mm | `Id.Item.556mm.HollowPoint.Tracer` | 5.56mm Flesh Damage (HP) | ammo | 80 (overrides: Inventory.Slot.Vehicle.Storage 150) | 2 x 1 | — | Item.Caliber.556mm | 25 |
| `ID_556mm_Tracer` | Ammo/556mm | `Id.Item.556mm.Tracer` | 5.56mm Standard (FMJ) | ammo | 80 (overrides: Inventory.Slot.Vehicle.Storage 150) | 2 x 1 | — | Item.Caliber.556mm | 15 |
| `ID_70mm` | Ammo/70mm | `ID.Item.70mm` | 70mm | ammo | — | 3 x 1 | — | Item.Caliber.70mm | — |
| `ID_72mm` | Ammo/72mm | `Id.Item.72mm` | 72mm | ammo | — | 2 x 1 | — | Item.Caliber.72mm | 600 |
| `ID_762mm` | Ammo/762mm | `Id.Item.762mm` | 7.62x39mm | ammo | 60 | 2 x 1 | — | Item.Caliber.762mm | 40 |
| `ID_762mm_ArmorPiercing` | Ammo/762mm | `Id.Item.762mm.ArmorPiercing` | 7.62mm Armor Piercing (AP) | ammo | 60 | 2 x 1 | — | Item.Caliber.762mm | 150 |
| `ID_762mm_ArmorPiercing_Tracer` | Ammo/762mm | `Id.Item.762mm.ArmorPiercing.Tracer` | 7.62mm Armor Piercing (AP) | ammo | 60 | 2 x 1 | — | Item.Caliber.762mm | 150 |
| `ID_762mm_HollowPoint` | Ammo/762mm | `Id.Item.762mm.HollowPoint` | 7.62mm Flesh Damage (HP) | ammo | 60 | 2 x 1 | — | Item.Caliber.762mm | 90 |
| `ID_762mm_HollowPoint_Tracer` | Ammo/762mm | `Id.Item.762mm.HollowPoint.Tracer` | 7.62mm Flesh Damage (HP) | ammo | 60 | 2 x 1 | — | Item.Caliber.762mm | 90 |
| `ID_762mm_Tracer` | Ammo/762mm | `Id.Item.762mm.Tracer` | 7.62mm Standard (FMJ) | ammo | 60 | 2 x 1 | — | Item.Caliber.762mm | 40 |
| `ID_762x51mm` | Ammo/762x51mm | `Id.Item.762x51mm` | 7.62x51mm | ammo | 100 (overrides: Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x51mm | 300 |
| `ID_762x51mm_ArmorPiercing` | Ammo/762x51mm | `Id.Item.762x51mm.ArmorPiercing` | 7.62x51mm Armor Piercing (AP) | ammo | 100 (overrides: Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x51mm | — |
| `ID_762x51mm_ArmorPiercing_Tracer` | Ammo/762x51mm | `Id.Item.762x51mm.ArmorPiercing.Tracer` | 7.62x51mm Armor Piercing (AP) | ammo | 100 (overrides: Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x51mm | 250 |
| `ID_762x51mm_HollowPoint` | Ammo/762x51mm | `Id.Item.762x51mm.HollowPoint` | 762x51mm Flesh Damage (HP) | ammo | 100 (overrides: Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x51mm | — |
| `ID_762x51mm_HollowPoint_Tracer` | Ammo/762x51mm | `Id.Item.762x51mm.HollowPoint.Tracer` | 762x51mm Flesh Damage (HP) | ammo | 100 (overrides: Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x51mm | — |
| `ID_762x51mm_Tracer` | Ammo/762x51mm | `Id.Item.762x51mm.Tracer` | 7.62x51mm Standard (FMJ) | ammo | 100 (overrides: Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x51mm | 200 |
| `ID_762x54mm` | Ammo/762x54mm | `Id.Item.762x54mm` | 7.62x54mm | ammo | 40 | 2 x 1 | — | Item.Caliber.762x54mm | 30 |
| `ID_762x54mm_ArmorPiercing` | Ammo/762x54mm | `Id.Item.762x54mm.ArmorPiercing` | 7.62x54mm Armor Piercing (AP) | ammo | 40 | 2 x 1 | — | Item.Caliber.762x54mm | 90 |
| `ID_762x54mm_ArmorPiercing_Tracer` | Ammo/762x54mm | `Id.Item.762x54mm.ArmorPiercing.Tracer` | 7.62x54mm Armor Piercing (AP) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x54mm | 90 |
| `ID_762x54mm_HollowPoint` | Ammo/762x54mm | `Id.Item.762x54mm.HollowPoint` | 7.62x54mm Flesh Damage (HP) | ammo | 40 | 2 x 1 | — | Item.Caliber.762x54mm | 55 |
| `ID_762x54mm_HollowPoint_Tracer` | Ammo/762x54mm | `Id.Item.762x54mm.HollowPoint.Tracer` | 7.62x54mm Flesh Damage (HP) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x54mm | 55 |
| `ID_762x54mm_Tracer` | Ammo/762x54mm | `Id.Item.762x54mm.Tracer` | 7.62x54mm Standard (FMJ) | ammo | 40 (overrides: Inventory.Slot.Vehicle.Storage 150, Inventory.Type.Vehicle 150) | 2 x 1 | — | Item.Caliber.762x54mm | 30 |
| `ID_84mm` | Ammo/84mm | `Id.Item.84mm` | 84mm | ammo | — | 2 x 1 | 3.5 | Item.Caliber.84mm | 200 |
| `ID_93mm` | Ammo/93mm | `Id.Item.93mm` | 93mm | ammo | — | 3 x 1 | 2.6 | Item.Caliber.93mm | 200 |
| `ID_9mm` | Ammo/9mm | `Id.Item.9mm` | 9x19mm | ammo | 80 | 2 x 1 | — | Item.Caliber.9mm | 10 |
| `ID_9mm_ArmorPiercing` | Ammo/9mm | `Id.Item.9mm.ArmorPiercing` | 9mm Armor Piercing (AP) | ammo | 100 | 2 x 1 | — | Item.Caliber.9mm | 20 |
| `ID_9mm_ArmorPiercing_Tracer` | Ammo/9mm | `Id.Item.9mm.ArmorPiercing.Tracer` | 9mm Armor Piercing (AP) | ammo | 100 | 2 x 1 | — | Item.Caliber.9mm | 20 |
| `ID_9mm_HollowPoint` | Ammo/9mm | `Id.Item.9mm.HollowPoint` | 9mm Flesh Damage (HP) | ammo | 100 | 2 x 1 | — | Item.Caliber.9mm | 15 |
| `ID_9mm_HollowPoint_Tracer` | Ammo/9mm | `Id.Item.9mm.HollowPoint.Tracer` | 9mm Flesh Damage (HP) | ammo | 100 | 2 x 1 | — | Item.Caliber.9mm | 15 |
| `ID_9mm_Tracer` | Ammo/9mm | `Id.Item.9mm.Tracer` | 9mm Standard (FMJ) | ammo | 100 | 2 x 1 | — | Item.Caliber.9mm | 10 |
| `ID_DebugHomingRocket_Ammo` | Ammo/DebugHomingRocket | `Id.Item.DebugHomingRocketAmmo` | RocketTesting 84mm | ammo | 99 | — | — | Item.Caliber.84mm | — |
<!-- /resource_tables -->

*Source: [`Wardogs/Content/Items/Resources/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Resources) (99 `.json`, 94 item definitions). Display names from [`Wardogs/Content/UI/Data/Entities/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/UI/Data/Entities) and prices from the vendor tables under [`NPCs/Vendor/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor). Generated by `_tools/resource_tables.py`.*

---

*Source files: [`Wardogs/Content/Items/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items) (259 `.json`).*

## Change log

| Date | Change |
|---|---|
| 2026-10-18 | `data/` re-exported with the v2 usmap (names only; values unchanged): the aim-assist rows in §9 and the Season 02 notes use the corrected `Pull`/`Slow` `Inner`/`Outer` `Hip`/`Ads` names. The values did not move; the first export had put the wrong names on them. |
| 2026-10-22 | Linked the new [Item Shop](../game-features/Wardogs_ItemShop_v1.md) page (shop and entity tables for every non-weapon item, generated by `_tools/item_shop_tables.py`). |
| 2026-10-22 | Added the Resources and ammunition section: one row per item definition in `Items/Resources/`, generated by `_tools/resource_tables.py`. |
| 2026-10-18 | Round-6 verifier corrections: `SupportFilter` has a fourth mode, `AllowPriority` (unused in data); `DefaultItems` is used only when `DefaultContainerItems` is empty (`0x6784010`), so the M4 Standard Mag loads `Id.Item.556mm.Tracer`. |
