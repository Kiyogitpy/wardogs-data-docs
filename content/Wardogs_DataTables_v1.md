---
title: "Data Tables"
has_children: true
redirect_from: ["/Wardogs_DataTables_v1.html", "/Wardogs_DataTables_v1"]
parent: "Data Tables & Tags"
description: "Index of all 766 data tables, grouped by row struct, with row counts and where each lives"
---

# Wardogs: Data Tables Catalog
*Every `DataTable` export under `data/`, listed by row struct, with generic expanded tables for the gameplay structs that have no page of their own. Built by [`_tools/datatable_catalog.py`](../_tools/datatable_catalog.py) (`--write` is idempotent).*

> **Labels.** **Data** = read from an exported table. **Derived** = grouping, counts and the "Documented in" column, computed by the generator. Nothing here was checked in-game, and this page does not say what the game does with a row; for that follow the "Documented in" links.

**How to read it.** The index lists all 766 tables, grouped by row struct (largest struct first). The line under each struct heading says where its rows are expanded:

- **Expanded in** a child page below: generic one-row-per-line tables, same for every struct.
- **Expanded on** an existing page: a dedicated generator already tabulates those rows, so they are not repeated.
- **Index only**: another page this round expands the struct (vendor data, entity UI data, buildables, damageable entities, seat names, currencies, cosmetics, skills and curves, tag-to-text).
- **UI widget table, not expanded**: styling and layout rows for widgets (rich text, crosshairs, trackers, icons, radial wheels, popups, indicators, notifications, pings, interaction context).
- **Audio table, skipped**: the Audio folder tables.

"Documented in" lists the doc pages that name the table (hand-written or generated). "not named" means no page mentions the table name; it may still be covered under a different heading.

## Expanded pages

- [Economy and Rewards](Wardogs_DataTables_Economy_v1.md)
- [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md)
- [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md)
- [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md)

## Index

<!-- datatable_catalog index -->
#### BHEntityData_UI

211 table(s), 751 rows, 211 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_EntityData_Ext_Emotes` | 6 | `GF/Emotes/Season01_EmotesData/Data` | [emotes](../_wiki/progression-and-economy/emotes.md), [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md), [Wardogs_GameFeatures_Emotes_v2](../game-features/Wardogs_GameFeatures_Emotes_v2.md) (+1) |
| `DT_EntityData_Ext_FGRP_006` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_006/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_007` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_007/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_008` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_008/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_009` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_009/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_010` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_010/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_011` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_012` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_012/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_013` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_014` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_014/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_015` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_015/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_016` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_016/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_017` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_017/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_018` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_018/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_FGRP_019` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_019/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_FGRP_020` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_020/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_Flares` | 1 | `GF/Vehicles/Flares/Data` | [round39-vehicles-explosives](../docs/evidence/round39-vehicles-explosives.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_LMG_02` | 2 | `GF/Weapons/LMG/LMG_02/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_002` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_002/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_003` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_003/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_004` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_004/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_005` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_005/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_006` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_006/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_008` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_008/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_011` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_012` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_012/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_024` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_024/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_026` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_026/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_034` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_034/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_043` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_043/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_046` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_046/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_051` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_051/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MAGZ_052` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_052/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_053` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_053/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_054` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_054/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_055` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_055/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_056` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_056/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_057` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_057/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_059` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_059/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_060` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_060/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_061` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_061/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_062` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_062/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_063` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_063/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_064` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_064/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_065` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_065/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_066` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_066/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MAGZ_067` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_067/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MAGZ_068` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_068/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MAGZ_069` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_069/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MAGZ_070` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_070/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MAGZ_071` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_071/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MK22` | 2 | `GF/Weapons/Sniper/MK22/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_MUZL_013` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_014` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_014/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_019` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_019/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_020` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_020/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_022` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_022/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_023` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_023/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_024` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_024/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_025` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_025/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_027` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_027/MUZL_027/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_028` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_028/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_029` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_029/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_030` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_030/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_031` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_031/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_032` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_032/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_037` | 2 | `GF/Weapons/Attachments/Muzzle/MUZL_037/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_038` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_038/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_039` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_039/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_040` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_040/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_041` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_041/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_044` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_044/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_045` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_045/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_046` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_046/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_047` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_047/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_048` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_048/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_049` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_049/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_050` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_050/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_051` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_051/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_052` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_052/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_053` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_053/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_054` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_054/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_055` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_055/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_056` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_056/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_057` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_057/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_058` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_058/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_059` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_059/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_060` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_060/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_061` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_061/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_062` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_062/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_MUZL_067` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_067/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MUZL_068` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_068/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MUZL_069` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_069/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MUZL_070` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_070/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MUZL_071` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_071/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_MUZL_072` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_072/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_Pistol_02` | 1 | `GF/Weapons/Pistols/Pistol_02/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_SGHT_009` | 1 | `GF/Weapons/Attachments/Sights/SGHT_009/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_011` | 1 | `GF/Weapons/Attachments/Sights/SGHT_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_013` | 1 | `GF/Weapons/Attachments/Sights/SGHT_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_016` | 1 | `GF/Weapons/Attachments/Sights/SGHT_016/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_023` | 1 | `GF/Weapons/Attachments/Sights/SGHT_023/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_024` | 1 | `GF/Weapons/Attachments/Sights/SGHT_024/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_025` | 1 | `GF/Weapons/Attachments/Sights/SGHT_025/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_026` | 1 | `GF/Weapons/Attachments/Sights/SGHT_026/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_027` | 1 | `GF/Weapons/Attachments/Sights/SGHT_027/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_028` | 1 | `GF/Weapons/Attachments/Sights/SGHT_028/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_029` | 1 | `GF/Weapons/Attachments/Sights/SGHT_029/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_030` | 1 | `GF/Weapons/Attachments/Sights/SGHT_030/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_031` | 1 | `GF/Weapons/Attachments/Sights/SGHT_031/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_032` | 1 | `GF/Weapons/Attachments/Sights/SGHT_032/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_033` | 1 | `GF/Weapons/Attachments/Sights/SGHT_033/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_034` | 1 | `GF/Weapons/Attachments/Sights/SGHT_034/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_036` | 1 | `GF/Weapons/Attachments/Sights/SGHT_036/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_037` | 1 | `GF/Weapons/Attachments/Sights/SGHT_037/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SGHT_038` | 1 | `GF/Weapons/Attachments/Sights/SGHT_038/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_SGHT_039` | 1 | `GF/Weapons/Attachments/Sights/SGHT_039/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_SGHT_040` | 1 | `GF/Weapons/Attachments/Sights/SGHT_040/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_SMG_03` | 1 | `GF/Weapons/SMG/SMG_03/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_SR_04` | 2 | `GF/Weapons/Sniper/SR_04/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_SV98` | 2 | `GF/Weapons/Platforms/WEPN_008/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_SVDM` | 2 | `GF/Weapons/DMR/SVDM/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_Ext_VehicleSmoke` | 1 | `GF/Vehicles/VehicleSmoke/Data` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_Ext_WEPN_017` | 1 | `GF/Weapons/Platforms/WEPN_017/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_WEPN_026` | 1 | `GF/Weapons/Platforms/WEPN_026/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_027` | 1 | `GF/Weapons/Platforms/WEPN_027/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_028` | 1 | `GF/Weapons/Platforms/WEPN_028/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_029` | 1 | `GF/Weapons/Platforms/WEPN_029/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_030` | 1 | `GF/Weapons/Platforms/WEPN_030/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_031` | 1 | `GF/Weapons/Platforms/WEPN_031/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_WEPN_032` | 1 | `GF/Weapons/Platforms/WEPN_032/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_033` | 1 | `GF/Weapons/Platforms/WEPN_033/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_034` | 1 | `GF/Weapons/Platforms/WEPN_034/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_WEPN_035` | 1 | `GF/Weapons/Platforms/WEPN_035/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_EntityData_Ext_WEPN_036` | 1 | `GF/Weapons/Platforms/WEPN_036/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_Ext_WEPN_037` | 1 | `GF/Weapons/Platforms/WEPN_037/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_UI_Battery` | 2 | `GF/Items/Battery/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Buildables` | 36 | `GF/Items/Buildables/Data` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_AT_Mine` | 1 | `GF/Items/AT_mine/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Armor` | 16 | `GF/Items/Armor/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Binoculars` | 1 | `GF/Items/Binoculars/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_C4` | 1 | `GF/Items/C4/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_C4Explosive` | 1 | `GF/Items/C4/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Claymore` | 1 | `GF/Items/Claymore/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_CombatBow` | 3 | `GF/Items/CombatBow/Data/DataTable` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Crowbar` | 1 | `GF/Items/Crowbar/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Defibrillator` | 1 | `GF/Items/Defibrillator/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Enox` | 3 | `GF/Items/Enox/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_FuelCanister` | 1 | `GF/Items/FuelCanister/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_HotPotato` | 1 | `GF/HotPotato/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_IED` | 2 | `GF/Items/IED/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_MedKit` | 1 | `GF/Items/MedKit/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_Molotov` | 1 | `GF/Items/Molotov/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_EntityData_UI_Ext_Parachutes` | 2 | `GF/Parachutes/Content` | [Wardogs_GameFeatures_Parachutes_v2](../game-features/Wardogs_GameFeatures_Parachutes_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_RangeFinder` | 3 | `GF/Items/RangeFinder/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_SmokeGrenade` | 8 | `GF/Items/SmokeGrenade/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_StimPen` | 1 | `GF/Items/StimPen/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Ext_VehicleRepairTool` | 3 | `GF/Items/VehicleRepairTool/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Garage` | 2 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_GarageMarket_SupplyCrates` | 8 | `GF/Vehicles/SupplyCrates/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_GoldExchange` | 1 | `UI/Features/Frontend/GoldExchange/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |
| `DT_EntityData_UI_Items` | 296 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [round40-vehicles-explosives](../docs/evidence/round40-vehicles-explosives.md), [Wardogs_AttachmentsPlatforms_v1](../game-features/Wardogs_AttachmentsPlatforms_v1.md) (+2) |
| `DT_EntityData_UI_Keycards` | 6 | `GF/Items/Keycard/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Misc` | 1 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_TNK01` | 12 | `GF/Vehicles/TNK_01/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_TNK04` | 6 | `GF/Vehicles/TNK_04/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_VehicleAmmo` | 5 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_ROT_02` | 5 | `GF/Vehicles/ROT_02/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_ROT_03` | 1 | `GF/Vehicles/ROT_03/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_ROT_03_WeaponVariants` | 6 | `GF/Vehicles/ROT_03_WeaponVariants/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_ROT_04` | 1 | `GF/Vehicles/ROT_04/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_Vehicles_ROT_04_MachineGun` | 3 | `GF/Vehicles/ROT_04_MachineGun/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_SPW_01` | 3 | `GF/Vehicles/SPW_01/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_STN_01` | 2 | `GF/Vehicles/STN_01/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_STN_02` | 2 | `GF/Vehicles/STN_02/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_STN_03` | 2 | `GF/Vehicles/STN_03/DataTable` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_STN_04` | 1 | `GF/Vehicles/STN_04/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_STN_05` | 3 | `GF/Vehicles/STN_05/DataTable` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_STN_06` | 2 | `GF/Vehicles/STN_06/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_Vehicles_WHL_01` | 1 | `GF/Vehicles/WHL_01/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_02` | 2 | `GF/Vehicles/WHL_02/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_02_RingTurret` | 3 | `GF/Vehicles/WHL_02_RingTurret/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_Vehicles_WHL_05_Humvee` | 1 | `GF/Vehicles/WHL_05/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_05_Minigun` | 3 | `GF/Vehicles/WHL_05_Minigun/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_05_RingTurret` | 3 | `GF/Vehicles/WHL_05_RingTurret/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_06_DuneBuggy` | 1 | `GF/Vehicles/WHL_06/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_07_ArmouredBattle` | 3 | `GF/Vehicles/WHL_07_ArmouredBattle/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_07_Ural` | 2 | `GF/Vehicles/WHL_07/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_EntityData_UI_Vehicles_WHL_08` | 1 | `GF/Vehicles/WHL_08/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_Vehicles_WHL_08_RingTurret` | 2 | `GF/Vehicles/WHL_08_RingTurret/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_EntityData_UI_Wagers` | 1 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_01` | 1 | `GF/Items/MusicTapes/MusicTape_01/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_02` | 1 | `GF/Items/MusicTapes/MusicTape_02/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_03` | 1 | `GF/Items/MusicTapes/MusicTape_03/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_04` | 1 | `GF/Items/MusicTapes/MusicTape_04/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_05` | 1 | `GF/Items/MusicTapes/MusicTape_05/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_06` | 1 | `GF/Items/MusicTapes/MusicTape_06/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_07` | 1 | `GF/Items/MusicTapes/MusicTape_07/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_08` | 1 | `GF/Items/MusicTapes/MusicTape_08/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_09` | 1 | `GF/Items/MusicTapes/MusicTape_09/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_Entity_UI_MusicTape_11` | 1 | `GF/Items/MusicTapes/MusicTape_11/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_Gunsmith_EntityData_UI_DecalTextures` | 5 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Gunsmith_EntityData_UI_PaintMaskTextures` | 4 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Gunsmith_EntityData_UI_PaintMasteryTextures` | 6 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Gunsmith_EntityData_UI_ReticleTextures` | 17 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_InteractionContext_ForwardOperatingBase` | 4 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_InteractionContexts` | 70 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_InteractionContexts_ForceOpenDoor` | 1 | `GF/Items/Crowbar/Data/Interaction` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_InteractionContexts_HotZoneMagnet` | 3 | `GF/WorldFeatures/HotZoneMagnet/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_InteractionContexts_Lockpicking` | 1 | `GF/Vehicles/Lockpicking/Data/Interaction` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_InteractionContexts_Lootable` | 2 | `GF/WorldFeatures/Lootable/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |

#### WDChallengeRewardDefinition

7 table(s), 486 rows, 7 named in docs. Expanded on [Challenges](../game-features/Wardogs_Challenges_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ChallengeRewards_EndOfMatch` | 5 | `Meta/Challenges` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_ChallengeRewards_SessionEvents_Buildables` | 47 | `GF/Rewards/BuildableRewards/Rewards` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [round38-building-data](../docs/evidence/round38-building-data.md), [round42-econ-buildables](../docs/evidence/round42-econ-buildables.md) (+3) |
| `DT_ChallengeRewards_SessionEvents_Crowbar` | 1 | `GF/Items/Crowbar/Rewards` | [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_ChallengeRewards_SessionEvents_HotZoneMagnet` | 3 | `GF/WorldFeatures/HotZoneMagnet/Data/Challenges` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [round38-building-data](../docs/evidence/round38-building-data.md), [round42-econ-buildables](../docs/evidence/round42-econ-buildables.md) (+1) |
| `DT_ChallengeRewards_SessionEvents_Shared` | 298 | `Meta/Challenges` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md) (+11) |
| `DT_ChallengeRewards_SessionEvents_Spotting` | 130 | `GF/Spotting/Data/Challenges` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [round42-econ-buildables](../docs/evidence/round42-econ-buildables.md), [round61-open-questions](../docs/evidence/round61-open-questions.md) (+3) |
| `DT_ChallengeRewards_TeamOffence` | 2 | `GF/TeamOffence/Challenges` | [round42-econ-buildables](../docs/evidence/round42-econ-buildables.md), [round43-econ-buildables](../docs/evidence/round43-econ-buildables.md), [round88-nb](../docs/evidence/round88-nb.md) (+1) |

#### BHUserSettingDataTableRow

8 table(s), 390 rows, 6 named in docs. Expanded on [Settings and Inputs](../content/Wardogs_SettingsAndInputs_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Itemsmith_Flair_Settings` | 2 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| `DT_Settings_Accessibility` | 30 | `GameMechanics/Settings/Accessibility` | [round84-census-v4](../docs/evidence/round84-census-v4.md) |
| `DT_Settings_Audio` | 22 | `GameMechanics/Settings/Audio` | not named |
| `DT_Settings_Controls` | 121 | `GameMechanics/Settings/Controls` | [round84-census-v4](../docs/evidence/round84-census-v4.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |
| `DT_Settings_Extra` | 1 | `GameMechanics/Settings/Extras` | not named |
| `DT_Settings_General` | 25 | `GameMechanics/Settings/General` | [round40-modes-ai-other](../docs/evidence/round40-modes-ai-other.md), [round58-open-questions](../docs/evidence/round58-open-questions.md), [round84-census-v4](../docs/evidence/round84-census-v4.md) (+1) |
| `DT_Settings_Keybindings` | 146 | `GameMechanics/Settings/Keybindings` | [round90-census-v5](../docs/evidence/round90-census-v5.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |
| `DT_Settings_Video` | 43 | `GameMechanics/Settings/Video` | [round84-census-v4](../docs/evidence/round84-census-v4.md) |

#### WDUIGameplayTagToTextTableRow

18 table(s), 375 rows, 18 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Ext_GameplayTagToText_Calibers` | 1 | `GF/Items/CombatBow/Data/DataTable` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Ammunition` | 14 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Archetypes` | 16 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Calibers` | 31 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Categories` | 112 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |
| `DT_GameplayTagToText_Components` | 7 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Damage` | 9 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_EventLog` | 6 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_InventorySlots` | 37 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Itemsmith` | 36 | `GF/Itemsmith/UI/Data` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md), [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| `DT_GameplayTagToText_PlayerStates` | 5 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Prompts` | 4 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Roles` | 13 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_SceneNames` | 38 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_ServerTags` | 24 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_TeamOffence` | 7 | `GF/TeamOffence/UI/Data` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Tooltips` | 10 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| `DT_GameplayTagToText_Tutorials` | 5 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |

#### WDVariantRewardLookupRow

16 table(s), 333 rows, 16 named in docs. Expanded on [Reward Lookup (Session Events)](../content/Wardogs_RewardLookup_SessionEvents_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_RewardLookup_SessionEvent_BuildableDestroyed` | 36 | `GF/Rewards/BuildableRewards/Rewards/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [round42-econ-buildables](../docs/evidence/round42-econ-buildables.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) (+1) |
| `DT_RewardLookup_SessionEvent_DestroySupplyCrate` | 10 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_DestroyVehicle` | 34 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [round53-fixed-wing](../docs/evidence/round53-fixed-wing.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) (+1) |
| `DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist` | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist` | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist` | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_DestroyVehicleSection` | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_HealPlayer` | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist` | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist` | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_RepairVehicle` | 3 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_RevivePlayer` | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist` | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist` | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_RewardLookup_SessionEvent_Spotting_Added` | 51 | `GF/Spotting/Data/Challenges/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) (+1) |
| `DT_RewardLookup_SessionEvent_Spotting_Removed` | 51 | `GF/Spotting/Data/Challenges/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [player-movement](../season-2-changes/player-movement.md) |

#### WDVendorData

206 table(s), 328 rows, 206 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_AttachmentMarket` | 17 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |
| `DT_Ext_VendorData_MusicTape_01` | 1 | `GF/Items/MusicTapes/MusicTape_01/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_Ext_VendorData_MusicTape_02` | 1 | `GF/Items/MusicTapes/MusicTape_02/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_03` | 1 | `GF/Items/MusicTapes/MusicTape_03/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_04` | 1 | `GF/Items/MusicTapes/MusicTape_04/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_05` | 1 | `GF/Items/MusicTapes/MusicTape_05/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_06` | 1 | `GF/Items/MusicTapes/MusicTape_06/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_07` | 1 | `GF/Items/MusicTapes/MusicTape_07/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_08` | 1 | `GF/Items/MusicTapes/MusicTape_08/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_09` | 1 | `GF/Items/MusicTapes/MusicTape_09/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_Ext_VendorData_MusicTape_11` | 1 | `GF/Items/MusicTapes/MusicTape_11/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_GarageMarket_SupplyCrates` | 8 | `GF/Vehicles/SupplyCrates/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_GearMarket` | 13 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round43-econ-buildables](../docs/evidence/round43-econ-buildables.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) (+1) |
| `DT_UtilityMarket` | 3 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket` | 0 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorVehicles` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) (+1) |
| `DT_VehicleMarket_ROT_02` | 1 | `GF/Vehicles/ROT_02/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_ROT_03` | 1 | `GF/Vehicles/ROT_03/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket_ROT_03_WeaponVariants` | 2 | `GF/Vehicles/ROT_03_WeaponVariants/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_ROT_04` | 1 | `GF/Vehicles/ROT_04/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket_ROT_04_MachineGun` | 1 | `GF/Vehicles/ROT_04_MachineGun/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_TNK_01` | 3 | `GF/Vehicles/TNK_01/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_TNK_04` | 1 | `GF/Vehicles/TNK_04/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_01` | 1 | `GF/Vehicles/WHL_01/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket_WHL_02` | 2 | `GF/Vehicles/WHL_02/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket_WHL_02_RingTurret` | 1 | `GF/Vehicles/WHL_02_RingTurret/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_05_Humvee` | 1 | `GF/Vehicles/WHL_05/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket_WHL_05_Minigun` | 1 | `GF/Vehicles/WHL_05_Minigun/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_05_RingTurret` | 1 | `GF/Vehicles/WHL_05_RingTurret/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_06_DuneBuggy` | 1 | `GF/Vehicles/WHL_06/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VehicleMarket_WHL_07_ArmouredBattle` | 1 | `GF/Vehicles/WHL_07_ArmouredBattle/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_07_Ural` | 2 | `GF/Vehicles/WHL_07/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_08` | 1 | `GF/Vehicles/WHL_08/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleMarket_WHL_08_RingTurret` | 1 | `GF/Vehicles/WHL_08_RingTurret/DataTables` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VendorData_Ext_AR_02` | 1 | `GF/Weapons/Platforms/WEPN_002/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_AT_Mine` | 1 | `GF/Items/AT_mine/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_Armor` | 14 | `GF/Items/Armor/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_Battery` | 2 | `GF/Items/Battery/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_Binoculars` | 1 | `GF/Items/Binoculars/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_Buildables` | 8 | `GF/Items/Buildables/Data` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_C4` | 2 | `GF/Items/C4/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_Claymore` | 1 | `GF/Items/Claymore/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_CombatBow` | 3 | `GF/Items/CombatBow/Data/DataTable` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_Crowbar` | 1 | `GF/Items/Crowbar/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_DMR_01` | 1 | `GF/Weapons/Platforms/WEPN_007/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_Defibrillator` | 1 | `GF/Items/Defibrillator/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_Enox` | 3 | `GF/Items/Enox/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_FGRP_006` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_006/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_007` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_007/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_008` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_008/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_009` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_009/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_010` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_010/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_011` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_012` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_012/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_013` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_014` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_014/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_015` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_015/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_016` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_016/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_017` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_017/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_FGRP_018` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_018/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_019` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_019/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_FGRP_020` | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_020/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_Flares` | 1 | `GF/Vehicles/Flares/Data` | [round39-vehicles-explosives](../docs/evidence/round39-vehicles-explosives.md), [round45-b](../docs/evidence/round45-b.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_FuelCanister` | 1 | `GF/Items/FuelCanister/Data` | [round59-open-questions](../docs/evidence/round59-open-questions.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_IED` | 1 | `GF/Items/IED/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_002` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_002/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_003` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_003/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_004` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_004/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_005` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_005/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_006` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_006/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_008` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_008/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_011` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_012` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_012/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_024` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_024/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_026` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_026/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_034` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_034/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_043` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_043/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_046` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_046/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_051` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_051/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MAGZ_052` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_052/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_053` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_053/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_054` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_054/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_055` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_055/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_056` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_056/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_057` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_057/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_059` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_059/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_060` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_060/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_061` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_061/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_062` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_062/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_063` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_063/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_064` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_064/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_065` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_065/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_066` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_066/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MAGZ_067` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_067/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MAGZ_068` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_068/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MAGZ_069` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_069/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MAGZ_070` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_070/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MAGZ_071` | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_071/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_013` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_014` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_014/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_019` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_019/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_020` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_020/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_022` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_022/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_023` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_023/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_024` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_024/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_025` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_025/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_027` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_027/MUZL_027/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_028` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_028/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_029` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_029/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_030` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_030/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_031` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_031/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_032` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_032/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_037` | 2 | `GF/Weapons/Attachments/Muzzle/MUZL_037/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_038` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_038/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_039` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_039/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_040` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_040/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_041` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_041/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_044` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_044/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_045` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_045/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_046` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_046/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_047` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_047/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_048` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_048/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_049` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_049/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_050` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_050/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_051` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_051/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_052` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_052/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_053` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_053/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_054` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_054/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_055` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_055/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_056` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_056/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_057` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_057/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_058` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_058/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_059` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_059/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_060` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_060/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_061` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_061/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_062` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_062/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_MUZL_067` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_067/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_068` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_068/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_069` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_069/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_070` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_070/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_071` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_071/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MUZL_072` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_072/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_MedKit` | 1 | `GF/Items/MedKit/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_Molotov` | 1 | `GF/Items/Molotov/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_Parachutes` | 2 | `GF/Parachutes/Content` | [round40-medical-movement](../docs/evidence/round40-medical-movement.md), [Wardogs_GameFeatures_Parachutes_v2](../game-features/Wardogs_GameFeatures_Parachutes_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) (+1) |
| `DT_VendorData_Ext_Pistol_02` | 1 | `GF/Weapons/Pistols/Pistol_02/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_RangeFinder` | 3 | `GF/Items/RangeFinder/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_SGHT_009` | 1 | `GF/Weapons/Attachments/Sights/SGHT_009/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_SGHT_023` | 1 | `GF/Weapons/Attachments/Sights/SGHT_023/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_SmokeGrenade` | 8 | `GF/Items/SmokeGrenade/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_StimPen` | 1 | `GF/Items/StimPen/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md) |
| `DT_VendorData_Ext_VehicleRepairTool` | 3 | `GF/Items/VehicleRepairTool/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_VendorData_Ext_VehicleSmoke` | 1 | `GF/Vehicles/VehicleSmoke/Data` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VendorData_Ext_WEPN_017` | 1 | `GF/Weapons/Platforms/WEPN_017/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_WEPN_026` | 1 | `GF/Weapons/Platforms/WEPN_026/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Ext_WEPN_027` | 1 | `GF/Weapons/Platforms/WEPN_027/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_WEPN_028` | 1 | `GF/Weapons/Platforms/WEPN_028/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_WEPN_029` | 1 | `GF/Weapons/Platforms/WEPN_029/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_WEPN_030` | 1 | `GF/Weapons/Platforms/WEPN_030/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_WEPN_035` | 1 | `GF/Weapons/Platforms/WEPN_035/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Ext_WEPN_036` | 1 | `GF/Weapons/Platforms/WEPN_036/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Launcher_04` | 1 | `GF/Weapons/Launchers/Launcher_04/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Weapon_LMG_02` | 2 | `GF/Weapons/LMG/LMG_02/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_MK22` | 2 | `GF/Weapons/Sniper/MK22/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Weapon_MP43` | 1 | `GF/Weapons/Shotgun/MP43/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Weapon_MP9` | 1 | `GF/Weapons/Platforms/WEPN_014/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_Mosin` | 1 | `GF/Weapons/Platforms/WEPN_017/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_RFB` | 1 | `GF/Weapons/DMR/RFB/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_RPG7` | 1 | `GF/Weapons/Launchers/RPG7/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_SMG_03` | 2 | `GF/Weapons/SMG/SMG_03/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Weapon_SR_04` | 2 | `GF/Weapons/Sniper/SR_04/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_SV98` | 2 | `GF/Weapons/Platforms/WEPN_008/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Weapon_SVDM` | 2 | `GF/Weapons/DMR/SVDM/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_VendorData_Weapon_WEPN_031` | 1 | `GF/Weapons/Platforms/WEPN_031/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_WEPN_034` | 1 | `GF/Weapons/Platforms/WEPN_034/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_VendorData_Weapon_WEPN_037` | 1 | `GF/Weapons/Platforms/WEPN_037/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponMarket` | 37 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round39-vehicles-explosives](../docs/evidence/round39-vehicles-explosives.md), [Wardogs_AttachmentsPlatforms_v1](../game-features/Wardogs_AttachmentsPlatforms_v1.md) (+3) |
| `DT_WeaponVendor_EXT_AR_03` | 1 | `GF/Weapons/Platforms/WEPN_003/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_EXT_AR_04` | 1 | `GF/Weapons/Platforms/WEPN_004/Data` | [round61-open-questions](../docs/evidence/round61-open-questions.md), [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_EXT_LMG_01` | 1 | `GF/Weapons/Platforms/WEPN_009/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_EXT_Launcher_01` | 1 | `GF/Weapons/Platforms/WEPN_012/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_EXT_Launcher_02` | 1 | `GF/Weapons/Platforms/WEPN_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_EXT_SMG_01` | 1 | `GF/Weapons/Platforms/WEPN_006/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_Ext_AR_01` | 1 | `GF/Weapons/Platforms/WEPN_001/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_MUZL_012` | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_012/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_SGHT_011` | 1 | `GF/Weapons/Attachments/Sights/SGHT_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_013` | 1 | `GF/Weapons/Attachments/Sights/SGHT_013/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_016` | 1 | `GF/Weapons/Attachments/Sights/SGHT_016/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_024` | 1 | `GF/Weapons/Attachments/Sights/SGHT_024/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_025` | 1 | `GF/Weapons/Attachments/Sights/SGHT_025/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_026` | 1 | `GF/Weapons/Attachments/Sights/SGHT_026/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_027` | 1 | `GF/Weapons/Attachments/Sights/SGHT_027/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_028` | 1 | `GF/Weapons/Attachments/Sights/SGHT_028/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_029` | 1 | `GF/Weapons/Attachments/Sights/SGHT_029/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_030` | 1 | `GF/Weapons/Attachments/Sights/SGHT_030/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_031` | 1 | `GF/Weapons/Attachments/Sights/SGHT_031/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_032` | 1 | `GF/Weapons/Attachments/Sights/SGHT_032/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_034` | 1 | `GF/Weapons/Attachments/Sights/SGHT_034/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_036` | 1 | `GF/Weapons/Attachments/Sights/SGHT_036/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponVendor_SGHT_038` | 1 | `GF/Weapons/Attachments/Sights/SGHT_038/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_SGHT_039` | 1 | `GF/Weapons/Attachments/Sights/SGHT_039/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendor_SGHT_040` | 1 | `GF/Weapons/Attachments/Sights/SGHT_040/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponVendore_EXT_Shotgun_01` | 1 | `GF/Weapons/Platforms/WEPN_011/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponsVendor_EXT_Pistol_01` | 1 | `GF/Weapons/Platforms/WEPN_010/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| `DT_WeaponsVendor_EXT_TAR21` | 1 | `GF/Weapons/Platforms/WEPN_005/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponsVendor_EXT_WEPN_032` | 1 | `GF/Weapons/Platforms/WEPN_032/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_WeaponsVendor_EXT_WEPN_033` | 1 | `GF/Weapons/Platforms/WEPN_033/Data` | [Wardogs_ItemShop_v1](../game-features/Wardogs_ItemShop_v1.md), [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |

#### WDRainSpotEntry

1 table(s), 304 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_RainSpots` | 304 | `Audio/Environment` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md) |

#### WDRewardFeedActionDataTableRow

10 table(s), 159 rows, 9 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdrewardfeedactiondatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ChallengesFeedActions` | 68 | `UI/Features/HUD/RewardFeed/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [round57-open-questions](../docs/evidence/round57-open-questions.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |
| `DT_ChallengesFeedActions_Building` | 12 | `GF/Rewards/BuildableRewards/Rewards` | [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| `DT_ChallengesFeedActions_Crowbar` | 1 | `GF/Items/Crowbar/Rewards` | [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_ChallengesFeedActions_Spotting` | 3 | `GF/Spotting/Data/UI/RewardFeed` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| `DT_ControlZoneRewardFeedActions` | 12 | `GF/ControlZone/UI/RewardFeed/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |
| `DT_RewardFeedActions` | 52 | `UI/Features/HUD/RewardFeed/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_RewardFeedActions_HotZoneMagnet` | 3 | `GF/WorldFeatures/HotZoneMagnet/Data/UI/RewardFeed` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| `DT_RewardFeedActions_Spotting` | 3 | `GF/Spotting/Data/UI/RewardFeed` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| `DT_RewardFeedActions_TeamOffence` | 1 | `GF/TeamOffence/Data/UI/RewardFeed` | not named |
| `DT_TippingReward` | 4 | `UI/Features/HUD/Tipping/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDMetaTreeNodeData_UI

1 table(s), 131 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetatreenodedata_ui).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CharacterSkillNodes_Data` | 131 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [round36-econ](../docs/evidence/round36-econ.md), [round39-medical-movement](../docs/evidence/round39-medical-movement.md) (+3) |

#### WDCustomRewardTableRow

16 table(s), 128 rows, 16 named in docs. Expanded on [Buildables](../game-features/Wardogs_Buildables_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Reward_Cash_BuildableBuilt` | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable` | [round38-building-data](../docs/evidence/round38-building-data.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Reward_Cash_BuildablePlaced` | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Reward_Cash_BuildablePlacedInFOB` | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Reward_Cash_ControlZoneReward` | 12 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| `DT_Reward_Cash_DeployableDestroyed` | 25 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Reward_Cash_DeployedSupplyCrate` | 6 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| `DT_Reward_Cash_EndGameFactionReward` | 4 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [round48](../docs/evidence/round48.md) |
| `DT_Reward_Cash_Heal` | 8 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Heal` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| `DT_Reward_Cash_HotZoneMagnet` | 8 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [round38-building-data](../docs/evidence/round38-building-data.md), [round66-map-actors](../docs/evidence/round66-map-actors.md) (+3) |
| `DT_Reward_Cash_PlayerKill` | 3 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/KillScore` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [index](../index.md) |
| `DT_Reward_Cash_Refuel` | 1 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| `DT_Reward_Cash_Repair` | 4 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| `DT_Reward_Cash_Revive` | 6 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Revive` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| `DT_Reward_Cash_Spotting` | 4 | `GF/Spotting/Data/Rewards` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [round48](../docs/evidence/round48.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| `DT_Reward_Cash_VehicleDestroyed` | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [game-modes-maps](../season-2-changes/game-modes-maps.md) |
| `DT_Reward_Cash_VehicleTransport` | 3 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |

#### WDUITaggedIconRow

8 table(s), 128 rows, 4 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CaliberModifiers_TaggedIcons` | 6 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_Calibers_TaggedIcons` | 34 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_DamageTypes_TaggedIcons` | 3 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_EventLog_TaggedIcons` | 2 | `UI/Features/DeathRecap/Widgets/HealthReport/Data` | not named |
| `DT_Ext_Caliber_TaggedIcons_Arrow` | 2 | `GF/Items/CombatBow/Data/DataTable` | not named |
| `DT_Ext_FuelLocations_TaggedIcons` | 1 | `GF/Items/FuelCanister/Data` | not named |
| `DT_Ext_RepairLocations_TaggedIcons` | 17 | `GF/Items/VehicleRepairTool/Data/UI/SpatialTrackers` | not named |
| `DT_TaggedIcons` | 63 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIFlairBasicPaintType

2 table(s), 120 rows, 2 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Itemsmith_Flair_BasicPaint` | 60 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| `DT_Itemsmith_Flair_CamoBasicPaint` | 60 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |

#### WDImpulseResonanceEntry

1 table(s), 116 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ImpulseResonance` | 116 | `Audio/Environment` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md) |

#### WDLoadingScreenTips

1 table(s), 110 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdloadingscreentips).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_LoadingScreenTips` | 110 | `UI/Features/Frontend/LoadingScreen/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |

#### WDChallengeDefinition

9 table(s), 108 rows, 9 named in docs. Expanded on [Challenges](../game-features/Wardogs_Challenges_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Challenges_SessionEvents_Buildables` | 11 | `GF/Rewards/BuildableRewards/Rewards` | [buildable-challenges](../_wiki/progression-and-economy/buildable-challenges.md), [round42-econ-buildables](../docs/evidence/round42-econ-buildables.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) (+1) |
| `DT_Challenges_SessionEvents_Crowbar` | 1 | `GF/Items/Crowbar/Rewards` | [crowbar-challenges](../_wiki/progression-and-economy/crowbar-challenges.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [items-equipment](../season-2-changes/items-equipment.md) |
| `DT_Challenges_SessionEvents_KOTH` | 60 | `GF/Challenges_KOTH/Content` | [king-of-the-hill-challenges](../_wiki/progression-and-economy/king-of-the-hill-challenges.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| `DT_Challenges_SessionEvents_KOTH_HotZoneMagnet` | 3 | `GF/WorldFeatures/HotZoneMagnet/Data/Challenges` | [hot-zone-magnet-challenges](../_wiki/progression-and-economy/hot-zone-magnet-challenges.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| `DT_Challenges_SessionEvents_KOTH_Spotting` | 2 | `GF/Spotting/Data/Challenges` | [spotting-challenges](../_wiki/progression-and-economy/spotting-challenges.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) (+1) |
| `DT_Challenges_SessionEvents_Shared` | 10 | `Meta/Challenges` | [achievements](../_wiki/progression-and-economy/achievements.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md) (+3) |
| `DT_Challenges_SessionEvents_TeamOffence` | 2 | `GF/TeamOffence/Challenges` | [team-offence-challenges](../_wiki/progression-and-economy/team-offence-challenges.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [game-modes-maps](../season-2-changes/game-modes-maps.md) |
| `DT_PassiveMissionChallenges` | 15 | `Meta/Missions` | [passive-missions](../_wiki/progression-and-economy/passive-missions.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+4) |
| `DT_WagerChallenges` | 4 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) (+1) |

#### WDUIInteractionContextDataTableRow

7 table(s), 98 rows, 5 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InteractionContextData` | 86 | `UI/Data/Interaction` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_InteractionContextData_ForceOpenDoor` | 1 | `GF/Items/Crowbar/Data/Interaction` | not named |
| `DT_InteractionContextData_ForwardOperatingBase` | 4 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_InteractionContextData_HotZoneMagnet` | 3 | `GF/WorldFeatures/HotZoneMagnet/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| `DT_InteractionContextData_Lockpicking` | 1 | `GF/Vehicles/Lockpicking/Data/Interaction` | not named |
| `DT_InteractionContextData_Lootable` | 2 | `GF/WorldFeatures/Lootable/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| `DT_InteractionContextData_StrikeDisarm_01` | 1 | `GF/PvE/Scenarios/StrikeDisarm_01/Content` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |

#### WDRewardTableRow

2 table(s), 81 rows, 2 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdrewardtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Rewards` | 78 | `GameMechanics/Gamemode/Data` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round38-building-data](../docs/evidence/round38-building-data.md) (+1) |
| `DT_Rewards_Spotting` | 3 | `GF/Spotting/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |

#### WDVoxBase

1 table(s), 81 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_VoxData` | 81 | `Audio/Vox/General` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md), [SDK](../docs/gap_resolution/SDK.md) |

#### WDUITrackerDataTableRow

20 table(s), 75 rows, 15 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Editor_TrackerData_ControlZoneRegions` | 1 | `GF/ControlZoneRegions/Data` | [Wardogs_GameFeatures_ControlZoneRegions_v2](../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md) |
| `DT_Editor_TrackerData_WorldDisplay` | 4 | `UI/Tools/WorldDisplay/Data` | not named |
| `DT_TrackerData_Map_Buildables` | 4 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_TrackerData_Map_ControlZone` | 1 | `GF/ControlZone/UI/Trackers/MapTrackers/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |
| `DT_TrackerData_Map_HotPotato` | 1 | `GF/HotPotato/Data/UI` | not named |
| `DT_TrackerData_Map_HotZoneMagnet` | 2 | `GF/WorldFeatures/HotZoneMagnet/Data/UI/MapTrackers` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| `DT_TrackerData_Map_Scenario` | 2 | `GF/PvE/Scenarios/BaseScenario/UI/Trackers` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| `DT_TrackerData_Map_SmokeGrenade` | 1 | `GF/Items/SmokeGrenade/UI/Trackers/MapTrackers/Data` | [round39-vehicles-explosives](../docs/evidence/round39-vehicles-explosives.md) |
| `DT_TrackerData_Map_SniperShowdown` | 3 | `GF/Experiences/SniperShowdown/UI` | [Wardogs_GameFeatures_Experiences_v2](../game-features/Wardogs_GameFeatures_Experiences_v2.md) |
| `DT_TrackerData_Map_Spotting` | 1 | `GF/Spotting/Data/UI/Tracker/Map/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| `DT_TrackerData_Minimap` | 17 | `UI/Features/HUD/Minimap/Widgets/Trackers/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_GameFeatures_Deathmatch_v2](../game-features/Wardogs_GameFeatures_Deathmatch_v2.md), [Wardogs_GameFeatures_ShootingRange_v2](../game-features/Wardogs_GameFeatures_ShootingRange_v2.md) |
| `DT_TrackerData_Minimap_Scenario` | 2 | `GF/PvE/Scenarios/BaseScenario/UI/Trackers` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| `DT_TrackerData_Minimap_SmokeGrenade` | 1 | `GF/Items/SmokeGrenade/UI/Trackers/MapTrackers/Data` | not named |
| `DT_TrackerData_Spatial` | 13 | `UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_TrackerData_Spatial_Buildables` | 1 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_TrackerData_Spatial_Scenario` | 1 | `GF/PvE/Scenarios/BaseScenario/UI/Trackers` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| `DT_TrackerData_Spatial_SmokeGrenade` | 1 | `GF/Items/SmokeGrenade/UI/Trackers/SpatialTrackers/Data` | not named |
| `DT_TrackerData_Spatial_Spotting` | 1 | `GF/Spotting/Data/UI/Tracker/Spatial/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| `DT_TrackerData_TacticalMap` | 17 | `UI/Features/Map/Widgets/Trackers/Data` | not named |
| `DT_Trackers_ControlZone_Spatial` | 1 | `GF/ControlZone/UI/Trackers/SpatialTrackers/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |

#### WDSceneDataTableRow

14 table(s), 68 rows, 12 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdscenedatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_DeathmatchSceneData_Match` | 1 | `GF/Deathmatch/UI/Scene` | [round8-loadout-deathmatch](../docs/evidence/round8-loadout-deathmatch.md), [Wardogs_GameFeatures_Deathmatch_v2](../game-features/Wardogs_GameFeatures_Deathmatch_v2.md) |
| `DT_SceneData_DefaultPvEScenario` | 1 | `GF/PvE/Scenarios/BaseScenario/UI` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| `DT_SceneData_Frontend` | 28 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_SceneData_Frontend_Gunsmith` | 1 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| `DT_SceneData_Frontend_Itemsmith` | 1 | `GF/Itemsmith/UI/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| `DT_SceneData_Frontend_Vehiclesmith` | 1 | `GF/Vehiclesmith/Data` | [Wardogs_GameFeatures_Vehiclesmith_v2](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) |
| `DT_SceneData_Match` | 25 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_SceneData_Match_Buildables` | 1 | `GF/Items/Buildables/Data/UI/FobRefuelRepair` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_SceneData_Match_STN_05` | 1 | `GF/Vehicles/STN_05/Data/UI` | not named |
| `DT_SceneData_Match_ShootingRange` | 1 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_GameFeatures_ShootingRangeTutorial_v2](../game-features/Wardogs_GameFeatures_ShootingRangeTutorial_v2.md), [Wardogs_GameFeatures_ShootingRange_v2](../game-features/Wardogs_GameFeatures_ShootingRange_v2.md) (+1) |
| `DT_SceneData_Match_SniperShowdown` | 1 | `GF/Experiences/SniperShowdown/UI` | [Wardogs_GameFeatures_Experiences_v2](../game-features/Wardogs_GameFeatures_Experiences_v2.md) |
| `DT_SceneData_Match_SupplyCrates` | 1 | `GF/Vehicles/SupplyCrates/UI/Data` | not named |
| `DT_SceneData_Match_Wagers` | 1 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |
| `DT_SceneData_Shared` | 4 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDMetaSkillEffectsTaggedTableRow

10 table(s), 62 rows, 10 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_DriverSkills` | 6 | `Meta/CharacterSkills` | [driver](../_wiki/progression-and-economy/driver.md), [round42-vehicles-explosives](../docs/evidence/round42-vehicles-explosives.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_InfantrySkills` | 17 | `Meta/CharacterSkills` | [assault](../_wiki/progression-and-economy/assault.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_MedicSkills` | 4 | `Meta/CharacterSkills` | [medic](../_wiki/progression-and-economy/medic.md), [round39-medical-movement](../docs/evidence/round39-medical-movement.md), [Wardogs_Medical_v1](../game-features/Wardogs_Medical_v1.md) (+1) |
| `DT_PilotSkills` | 6 | `Meta/CharacterSkills` | [pilot](../_wiki/progression-and-economy/pilot.md), [round42-vehicles-explosives](../docs/evidence/round42-vehicles-explosives.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_ReconSkills` | 13 | `Meta/CharacterSkills` | [recon](../_wiki/progression-and-economy/recon.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Skills_C4` | 1 | `GF/Items/C4/Data/Skills` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Skills_Lockpicking` | 1 | `GF/Vehicles/Lockpicking/Data/Skills` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md), [Wardogs_GameplayEffectsPipeline_v1](../pipelines/Wardogs_GameplayEffectsPipeline_v1.md) |
| `DT_Skills_PrototypeMaskedScopes` | 1 | `GF/Items/PrototypeMaskedScopes/Data/Skills` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Skills_Spotting` | 2 | `GF/Spotting/Data/Skills` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_SupportSkills` | 11 | `Meta/CharacterSkills` | [support](../_wiki/progression-and-economy/support.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |

#### WDDamageableEntityTableRow

26 table(s), 54 rows, 26 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_GlobalDamage_ArmorData` | 4 | `GameMechanics/DamageSystem/DamageDataTables` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round25-armor-coverage](../docs/evidence/round25-armor-coverage.md), [round25-verification](../docs/evidence/round25-verification.md) (+9) |
| `DT_GlobalDamage_BuildableData` | 20 | `GF/Items/Buildables/Data` | [round55-s2-infantry-damage](../docs/evidence/round55-s2-infantry-damage.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [Wardogs_GameFeatures_Items_v2](../game-features/Wardogs_GameFeatures_Items_v2.md) (+1) |
| `DT_GlobalDamage_InfantryData` | 1 | `GameMechanics/DamageSystem/DamageDataTables` | [README](../README.md), [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md) (+14) |
| `DT_GlobalDamage_SupplyCrate` | 5 | `GF/Vehicles/SupplyCrates/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| `DT_GlobalDamage_VehicleData` | 1 | `GameMechanics/DamageSystem/DamageDataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [round52-explosives-vs-vehicles](../docs/evidence/round52-explosives-vs-vehicles.md), [Wardogs_Explosives_v1](../game-features/Wardogs_Explosives_v1.md) (+5) |
| `DT_GlobalDamage_VehicleData_ROT_02` | 1 | `GF/Vehicles/ROT_02/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_ROT_03` | 1 | `GF/Vehicles/ROT_03/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_ROT_04` | 1 | `GF/Vehicles/ROT_04/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_SPW_01` | 1 | `GF/Vehicles/SPW_01/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_STN_01` | 1 | `GF/Vehicles/STN_01/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_STN_02` | 1 | `GF/Vehicles/STN_02/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_STN_03` | 1 | `GF/Vehicles/STN_03/DataTable` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_STN_04` | 1 | `GF/Vehicles/STN_04/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_STN_05` | 1 | `GF/Vehicles/STN_05/DataTable` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_STN_06` | 1 | `GF/Vehicles/STN_06/DataTables` | [Wardogs_VehicleDamagePipeline_v1](../pipelines/Wardogs_VehicleDamagePipeline_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_TNK_01` | 3 | `GF/Vehicles/TNK_01/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_TNK_04` | 1 | `GF/Vehicles/TNK_04/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [Wardogs_VehicleDamagePipeline_v1](../pipelines/Wardogs_VehicleDamagePipeline_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_01` | 1 | `GF/Vehicles/WHL_01/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_02` | 1 | `GF/Vehicles/WHL_02/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_05_Humvee` | 1 | `GF/Vehicles/WHL_05/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_05_Minigun` | 1 | `GF/Vehicles/WHL_05_Minigun/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_05_RingTurret` | 1 | `GF/Vehicles/WHL_05_RingTurret/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy` | 1 | `GF/Vehicles/WHL_06/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_07_Ural` | 1 | `GF/Vehicles/WHL_07/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_08` | 1 | `GF/Vehicles/WHL_08/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_GlobalDamage_VehicleData_WHL_08_RingTurret` | 1 | `GF/Vehicles/WHL_08_RingTurret/DataTables` | [Wardogs_VehicleDamagePipeline_v1](../pipelines/Wardogs_VehicleDamagePipeline_v1.md), [vehicles](../season-2-changes/vehicles.md) |

#### WDLootableDataTable

2 table(s), 54 rows, 2 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdlootabledatatable).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_LootableDataTable` | 52 | `GF/WorldFeatures/Lootable/Data` | [round84-census-v4](../docs/evidence/round84-census-v4.md), [round85-loot](../docs/evidence/round85-loot.md), [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) (+1) |
| `DT_LootableDataTable_VIPEscort_01` | 2 | `GF/PvE/Scenarios/VIPEscort_01/Content` | [round36-ai](../docs/evidence/round36-ai.md), [round59-open-questions](../docs/evidence/round59-open-questions.md), [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) (+2) |

#### WDWagerConditionDefinition

1 table(s), 50 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwagerconditiondefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_WagerConditions` | 50 | `Meta/Wagers` | [wagers](../_wiki/progression-and-economy/wagers.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+2) |

#### WDResourceRewardTableRow

1 table(s), 49 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdresourcerewardtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CashRewards` | 49 | `GameMechanics/Gamemode/Data` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round38-building-data](../docs/evidence/round38-building-data.md) (+3) |

#### WDUIRadialWheelSlotTypeTableRow

10 table(s), 46 rows, 6 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_RadialWheelSlotType_BuildToolData` | 22 | `GF/Items/Buildables/Data/BuildTool` | [round90-census-v5](../docs/evidence/round90-census-v5.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_RadialWheelSlotType_BuildToolData` | 1 | `GF/Vehicles/STN_01/BuildableData` | [round90-census-v5](../docs/evidence/round90-census-v5.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_RadialWheelSlotType_BuildToolData` | 1 | `GF/Vehicles/STN_06/BuildableData` | [round90-census-v5](../docs/evidence/round90-census-v5.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_RadialWheelSlotType_BuildToolData_STN_04` | 1 | `GF/Vehicles/STN_04/BuildableData` | not named |
| `DT_RadialWheelSlotType_EquipmentData` | 7 | `UI/Features/RadialWheel/Data/EquipmentWheel` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_RadialWheelSlotType_Vehicles` | 9 | `UI/Features/RadialWheel/Data/Vehicles` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_RadialWheelSlotType_VoiceChatData` | 2 | `UI/Features/RadialWheel/Data/VoiceChat` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_STN_02_RadialWheelSlotType_BuildToolData` | 1 | `GF/Vehicles/STN_02/BuildableData` | not named |
| `DT_STN_03_RadialWheelSlotType_BuildToolData` | 1 | `GF/Vehicles/STN_03/BuildableData` | not named |
| `DT_STN_05_RadialWheelSlotType_BuildToolData` | 1 | `GF/Vehicles/STN_05/BuildableData` | not named |

#### WDBuildableDataTableRow

9 table(s), 44 rows, 9 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Buildables_LargeHammer` | 19 | `GF/Items/Buildables/Data/LargeHammer` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Buildables_MediumHammer` | 12 | `GF/Items/Buildables/Data/MediumHammer` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Buildables_STN_04` | 1 | `GF/Vehicles/STN_04/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_Buildables_STN_06` | 1 | `GF/Vehicles/STN_06/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_Buildables_SmallHammer` | 7 | `GF/Items/Buildables/Data/SmallHammer` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_STN_01_Buildable_Data` | 1 | `GF/Vehicles/STN_01/Data` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_STN_02_Buildable_Data` | 1 | `GF/Vehicles/STN_02/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_STN_03_Buildable_Data` | 1 | `GF/Vehicles/STN_03/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_STN_05_Buildable_Data` | 1 | `GF/Vehicles/STN_05/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |

#### WDUITooltipDataTableRow

4 table(s), 39 rows, 4 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_TooltipData` | 34 | `UI/Features/Tooltips/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_TooltipData_Buildables` | 1 | `GF/Items/Buildables/Data/UI/Tooltips` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_TooltipData_HotZoneMagnet` | 2 | `GF/WorldFeatures/HotZoneMagnet/Data/UI/MapTrackers` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| `DT_TooltipData_Wagers` | 2 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDEventFeedActionDataTableRow

2 table(s), 37 rows, 2 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdeventfeedactiondatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_EventFeedTypes` | 34 | `UI/Features/HUD/EventFeed/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_EventFeedTypes_SniperShowdown` | 3 | `GF/Experiences/SniperShowdown/UI` | [Wardogs_GameFeatures_Experiences_v2](../game-features/Wardogs_GameFeatures_Experiences_v2.md) |

#### WDCosmeticData

10 table(s), 36 rows, 10 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Bobblehead_Faction_Cosmetics` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Faction/Data` | [vehicle-skins](../_wiki/progression-and-economy/vehicle-skins.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Bobblehead_Grenade_Cosmetics` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Grenade/Data` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Bobblehead_HeavyHelmet_Cosmetics` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_HeavyHelmet/Data` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Bobblehead_Warpup_Cosmetics` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Warpup/Data` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Cosmetics_Debug` | 0 | `Meta/Cosmetics` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Cosmetics_FactionLogo` | 3 | `GF/Skins/FactionLogo_SkinsData/Data` | [weapon-skins](../_wiki/progression-and-economy/weapon-skins.md), [Wardogs_GameFeatures_Skins_v2](../game-features/Wardogs_GameFeatures_Skins_v2.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Cosmetics_Season01_Emotes` | 3 | `GF/Emotes/Season01_EmotesData/Data` | [emotes](../_wiki/progression-and-economy/emotes.md), [season-01-cosmetics](../_wiki/progression-and-economy/season-01-cosmetics.md), [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md) (+3) |
| `DT_Cosmetics_Season01_Skins` | 17 | `GF/Skins/Season01_SkinsData/Data` | [season-01-cosmetics](../_wiki/progression-and-economy/season-01-cosmetics.md), [vehicle-skins](../_wiki/progression-and-economy/vehicle-skins.md), [weapon-skins](../_wiki/progression-and-economy/weapon-skins.md) (+4) |
| `DT_Cosmetics_Season02_Skins` | 8 | `GF/Skins/Season02_SkinsData/Data` | [vehicle-skins](../_wiki/progression-and-economy/vehicle-skins.md), [weapon-skins](../_wiki/progression-and-economy/weapon-skins.md), [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md) (+4) |
| `DT_Cosmetics_Taxi` | 1 | `GF/Taxi_SkinsData/Data` | [vehicle-skins](../_wiki/progression-and-economy/vehicle-skins.md), [Wardogs_GameFeatures_Taxi_SkinsData_v2](../game-features/Wardogs_GameFeatures_Taxi_SkinsData_v2.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |

#### RichImageRow

5 table(s), 35 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CustomEmojis` | 3 | `UI/Features/HUD/Chatbox/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_MapImageStyle` | 20 | `UI/Features/Map/Widgets/TacticalMap/Data` | not named |
| `DT_RichImg_Style_EventLog` | 2 | `UI/Features/DeathRecap/Widgets/Log/Data` | not named |
| `DT_RichTextImg_FactionIcon` | 3 | `UI/Shared/RichTextDecorator` | not named |
| `DT_TooltipEmojis` | 7 | `UI/Features/Tooltips/Widgets/TooltipItems/Data` | not named |

#### WDUIPingAction

5 table(s), 35 rows, 4 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_PingActions_Emotes` | 10 | `UI/Features/PingWheel/Data/Actions/Emote` | not named |
| `DT_PingActions_Orders` | 5 | `UI/Features/PingWheel/Data/Actions/Orders` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_PingActions_Request` | 10 | `UI/Features/PingWheel/Data/Actions/Requests` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_PingActions_Social` | 5 | `UI/Features/PingWheel/Data/Actions/Social` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_PingActions_Squad` | 5 | `UI/Features/PingWheel/Data/Actions/Squad` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### FVehiclePropEntry

1 table(s), 29 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#fvehiclepropentry).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_VehiclePropList` | 29 | `Environment/Blueprints/VehiclePropTooling` | [Wardogs_Environment_v2](../content/Wardogs_Environment_v2.md), [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [round89-env](../docs/evidence/round89-env.md) (+1) |

#### WDEmoteData

1 table(s), 27 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdemotedata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_EmoteData` | 27 | `GameMechanics/Actions/Character` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [Wardogs_ItemActions_v1](../content/Wardogs_ItemActions_v1.md), [round45-b](../docs/evidence/round45-b.md) (+1) |

#### WDGoldMarketItemTableRow

1 table(s), 27 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdgoldmarketitemtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_GoldMarket` | 27 | `Meta/Collection` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md), [round53-fixed-wing](../docs/evidence/round53-fixed-wing.md) (+2) |

#### WDBoneDamageModifierData

1 table(s), 20 rows, 1 named in docs. Expanded on [All Vehicles Stats and Damage](../content/Wardogs_AllVehicles_Stats_Damage_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InfantryData_BoneDamageModifiers` | 20 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [damage](../docs/evidence/damage.md), [round39-weapons](../docs/evidence/round39-weapons.md) (+4) |

#### WDDeathmatchWeaponData

1 table(s), 20 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wddeathmatchweapondata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_DeathmatchWeaponSelect` | 20 | `GF/Deathmatch/Data` | [ROUND8_STATUS](../docs/ROUND8_STATUS.md), [round8-loadout-deathmatch](../docs/evidence/round8-loadout-deathmatch.md), [round8-loadout-initialization](../docs/evidence/round8-loadout-initialization.md) (+1) |

#### WDUIActionSoundTableRow

1 table(s), 20 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_UIAudioData` | 20 | `UI/Data/Audio` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDExperienceServerBrowserTagRow

1 table(s), 19 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdexperienceserverbrowsertagrow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ExperienceServerBrowserTags` | 19 | `UI/Data/ServerBrowser` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [round61-open-questions](../docs/evidence/round61-open-questions.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |

#### WDUIMaterialTrackerDataTableRow

3 table(s), 19 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_MaterialTrackerSettingsData` | 15 | `UI/Data/Trackers` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_MaterialTrackerSettingsData_Buildables` | 3 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_MaterialTrackerSettingsData_Spotting` | 1 | `GF/Spotting/Data/UI/Tracker/Optimization/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |

#### WDLiveCurveTableRow

10 table(s), 18 rows, 10 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Challenges_Curves_BuildableDestroyedAssist` | 1 | `GF/Rewards/BuildableRewards/Rewards/CurveTables` | [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_DestroyVehicle` | 1 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_DestroyVehicleAssist` | 1 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_EndOfMatch` | 2 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_HealPlayer` | 2 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_PlayerDelivered` | 1 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_PlayerKill` | 3 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Challenges_Curves_PurchaseFromSupplyCrate` | 3 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md), [rewards-unlocks](../season-2-changes/rewards-unlocks.md) |
| `DT_Challenges_Curves_VehicleAirborne` | 1 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Progression_v1](../game-features/Wardogs_Progression_v1.md) |
| `DT_Meta_RewardScalingCurves` | 3 | `Meta/Rewards` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round85-loot](../docs/evidence/round85-loot.md) (+1) |

#### WDUIPopupTypeDataTableRow

3 table(s), 18 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_PopupTypes_Features` | 14 | `UI/Features/Popups/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_PopupTypes_Generic` | 3 | `UI/Features/Popups/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_PopupTypes_Itemsmith` | 1 | `GF/Itemsmith/UI/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |

#### WDUITaggedWidgetParamsRow

3 table(s), 18 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_LootedComponentTypes` | 4 | `UI/Features/Inventory_2_0/Widgets/InventoryComponent/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| `DT_LootedComponentTypes_FOB` | 1 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_SettingTypeUIData` | 13 | `UI/Features/Settings/Widgets/SettingValue/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIScopeReticleType

1 table(s), 17 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ScopeReticleTypes` | 17 | `UI/Features/HUD/ScopeReticle/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [round84-procedural-reticles](../docs/evidence/round84-procedural-reticles.md) |

#### RichTextStyleRow

10 table(s), 15 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_MapTextStyle` | 1 | `UI/Features/Map/Widgets/TacticalMap/Data` | not named |
| `DT_RichText_StyleRows_CustomEmojis` | 1 | `UI/Features/HUD/Chatbox/Data` | not named |
| `DT_RichText_StyleRows_CustomEmojisInHighlighted` | 1 | `UI/Features/HUD/Chatbox/Data` | not named |
| `DT_RichText_StyleRows_TooltipEmojis` | 1 | `UI/Features/Tooltips/Widgets/TooltipItems/Data` | not named |
| `DT_RichText_StyleRows_TooltipEmojis_Small` | 1 | `UI/Features/Tooltips/Widgets/TooltipItems/Data` | not named |
| `DT_RichText_Style_ActionLabel` | 2 | `UI/Features/Frontend/Shared/Text` | not named |
| `DT_RichText_Style_EventFeed` | 2 | `UI/Features/HUD/EventFeed/Widgets/EventFeedEntry/Data` | not named |
| `DT_RichText_Style_EventLog` | 3 | `UI/Features/DeathRecap/Widgets/Log/Data` | not named |
| `DT_RichText_Style_InfoPopup` | 1 | `UI/Features/Popups/Widgets/Data` | not named |
| `DT_RichText_Style_Photosensitivity` | 2 | `UI/Features/Frontend/Photosensitivity/Data` | not named |

#### WDPostProcessEffect

5 table(s), 15 rows, 5 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_AlternativeCriticalCamera` | 1 | `GF/AlternativeCriticalCamera/Content` | [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [CROSS_REF](../docs/gap_resolution/CROSS_REF.md), [Wardogs_GameFeatures_AlternativeCriticalCamera_v2](../game-features/Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md) |
| `DT_PostProcessEffects` | 11 | `VFX/Postprocess` | [Wardogs_VFX_v2](../content/Wardogs_VFX_v2.md), [round39-medical-movement](../docs/evidence/round39-medical-movement.md), [round84-census-v4](../docs/evidence/round84-census-v4.md) (+1) |
| `DT_PostProcessEffects_FOB` | 1 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_PostProcessEffects_Molotov` | 1 | `GF/Items/Molotov/Data` | [Wardogs_FireAndUtility_v1](../game-features/Wardogs_FireAndUtility_v1.md), [weapons-ammo](../season-2-changes/weapons-ammo.md) |
| `DT_PostProcessEffects_StimPen` | 1 | `GF/Items/StimPen/Data` | [round84-census-v4](../docs/evidence/round84-census-v4.md) |

#### WDUIUserSettingDisplayDataTableRow

1 table(s), 15 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduiusersettingdisplaydatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Settings_DisplayData` | 15 | `UI/Features/Settings/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDServerBrowserRegionData

1 table(s), 14 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdserverbrowserregiondata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_OnlineRegions` | 14 | `UI/Features/Frontend/FindMatch/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |

#### WDArchetypeCaliberDamageModifierData

1 table(s), 12 rows, 1 named in docs. Expanded on [All Vehicles Stats and Damage](../content/Wardogs_AllVehicles_Stats_Damage_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InfantryData_ArchetypeCaliberModifiers` | 12 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [GOBJECTS_DAMAGE_ANALYSIS](../docs/GOBJECTS_DAMAGE_ANALYSIS.md), [round55-s2-infantry-damage](../docs/evidence/round55-s2-infantry-damage.md) (+3) |

#### WDAssistanceRequestData

1 table(s), 12 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdassistancerequestdata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_AssistanceRequests` | 12 | `GameMechanics/Communication/AssistanceRequests` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDCosmeticSetData

1 table(s), 12 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdcosmeticsetdata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CosmeticSets_Debug` | 12 | `Meta/Cosmetics` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [rewards-unlocks](../season-2-changes/rewards-unlocks.md) |

#### WDMusicState

1 table(s), 12 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_MusicSystem` | 12 | `Audio/Music` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md) |

#### WDUIDeploymentBoardRejectionTableRow

2 table(s), 12 rows, 2 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduideploymentboardrejectiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_DeploymentRejectionReasons` | 11 | `UI/Features/DeploymentBoard/Data` | [round75-open-questions](../docs/evidence/round75-open-questions.md) |
| `DT_DeploymentRejectionReasons_ControlZone` | 1 | `GF/ControlZone/UI/DeploymentBoard` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |

#### WDUIServerBrowserMapTextureTableRow

1 table(s), 12 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduiserverbrowsermaptexturetablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ServerBrowserMapTexture` | 12 | `UI/Features/Frontend/FindMatch/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |

#### WDUISquadIntentTableRow

1 table(s), 12 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduisquadintenttablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_SquadIntents` | 12 | `UI/Features/ContextDrawer/Tabs/Party/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [data-tables-tags](../season-2-changes/data-tables-tags.md) |

#### WDVehicleSeatNameOverrideRow

9 table(s), 12 rows, 9 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_VehicleSeatOverrides_ROT_02` | 1 | `GF/Vehicles/ROT_02/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_ROT_03` | 3 | `GF/Vehicles/ROT_03/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_ROT_04` | 2 | `GF/Vehicles/ROT_04/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_STN_01` | 1 | `GF/Vehicles/STN_01/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_STN_02` | 1 | `GF/Vehicles/STN_02/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_STN_03` | 1 | `GF/Vehicles/STN_03/DataTable` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_STN_04` | 1 | `GF/Vehicles/STN_04/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_STN_05` | 1 | `GF/Vehicles/STN_05/DataTable` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_VehicleSeatOverrides_STN_06` | 1 | `GF/Vehicles/STN_06/DataTables` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md), [vehicles](../season-2-changes/vehicles.md) |

#### WDAutomatedTestServerProfile

1 table(s), 11 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdautomatedtestserverprofile).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ServerTestingProfiles` | 11 | `Tests/LoadTests/Data` | [Wardogs_Tests_v2](../content/Wardogs_Tests_v2.md), [round40-modes-ai-other](../docs/evidence/round40-modes-ai-other.md), [round41-modes-ai-other](../docs/evidence/round41-modes-ai-other.md) |

#### WDUIVehicleCrosshairDataTableRow

8 table(s), 11 rows, 8 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_VehicleCrosshair_ROT02` | 2 | `GF/Vehicles/ROT_02/DataTables` | [round84-census-v4](../docs/evidence/round84-census-v4.md), [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md) |
| `DT_VehicleCrosshair_STN01` | 0 | `GF/Vehicles/STN_01/DataTables` | [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md) |
| `DT_VehicleCrosshair_STN06` | 0 | `GF/Vehicles/STN_06/DataTables` | [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md), [vehicles](../season-2-changes/vehicles.md) |
| `DT_VehicleCrosshair_STN_02` | 1 | `GF/Vehicles/STN_02/DataTables` | [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md) |
| `DT_VehicleCrosshair_STN_03` | 1 | `GF/Vehicles/STN_03/DataTable` | [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md) |
| `DT_VehicleCrosshair_STN_05` | 1 | `GF/Vehicles/STN_05/DataTable` | [round61-open-questions](../docs/evidence/round61-open-questions.md), [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md) |
| `DT_VehicleCrosshair_TNK01` | 4 | `GF/Vehicles/TNK_01/DataTables` | [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md) |
| `DT_VehicleCrosshair_TNK04` | 2 | `GF/Vehicles/TNK_04/DataTables` | [Wardogs_VehicleTurretControls_v1](../game-features/Wardogs_VehicleTurretControls_v1.md), [vehicles](../season-2-changes/vehicles.md) |

#### WDVehicleSeatDamageReductionData

1 table(s), 11 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdvehicleseatdamagereductiondata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InfantryData_VehicleSeatDamageReduction` | 11 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [damage](../docs/evidence/damage.md), [round53-fixed-wing](../docs/evidence/round53-fixed-wing.md) (+3) |

#### WDAchievementDefinition

1 table(s), 10 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdachievementdefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Achievements` | 10 | `Meta/Achievements` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) (+1) |

#### WDReticleAssetInfo

1 table(s), 10 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Gunsmith_Reticles` | 10 | `GF/Gunsmith/UI/ReticleNodeFocus/Data` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |

#### WDUIPopupOptionDataTableRow

2 table(s), 10 rows, 2 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_GunsmithPopupOptions` | 5 | `GF/Gunsmith/UI/Data/Popups` | [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [CROSS_REF](../docs/gap_resolution/CROSS_REF.md), [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| `DT_VehiclesmithPopupOptions` | 5 | `GF/Vehiclesmith/UI/Scene/Data` | [Wardogs_GameFeatures_Vehiclesmith_v2](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) |

#### WDAssistResourceRewardTableRow

1 table(s), 9 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdassistresourcerewardtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_AssistCashRewards` | 9 | `GameMechanics/Gamemode/Data` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round48](../docs/evidence/round48.md), [round68-boundaries](../docs/evidence/round68-boundaries.md) |

#### WDResourceRewardModifierTableRow

1 table(s), 9 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdresourcerewardmodifiertablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CashRewardModifiers` | 9 | `GameMechanics/Gamemode/Data` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round48](../docs/evidence/round48.md) |

#### WDMetaTreeTableRow

1 table(s), 7 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetatreetablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_MetaTree_Roles` | 7 | `Meta/CharacterSkills` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_TreeRewardTrack_PlatformMastery_v1](../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md), [LOADOUT_BUILDER_HANDOFF](../docs/LOADOUT_BUILDER_HANDOFF.md) (+6) |

#### WDUILevelTableRow

1 table(s), 7 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduileveltablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_LevelIcons` | 7 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDAmmoTypeEffectivenessData

1 table(s), 6 rows, 1 named in docs. Expanded on [All Vehicles Stats and Damage](../content/Wardogs_AllVehicles_Stats_Damage_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InfantryData_AmmoTypeEffectivenessPen` | 6 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round42-modes-ai-other](../docs/evidence/round42-modes-ai-other.md), [Wardogs_DamagePipeline_v2](../pipelines/Wardogs_DamagePipeline_v2.md) |

#### WDFactoryRecipe

1 table(s), 6 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdfactoryrecipe).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Factory01_Recipes` | 6 | `GF/FactoryInvestment_01/Data` | [Wardogs_GameFeatures_FactoryInvestment_01_v2](../game-features/Wardogs_GameFeatures_FactoryInvestment_01_v2.md), [rewards-unlocks](../season-2-changes/rewards-unlocks.md) |

#### WDFlairMaskInfo

1 table(s), 6 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Itemsmith_Flair_Masks` | 6 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |

#### WDMetaMasteryDefinitionTableRow

1 table(s), 6 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetamasterydefinitiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_RoleMasteryDefinitions` | 6 | `Meta/Levels/Roles` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_TreeRewardTrack_PlatformMastery_v1](../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md) (+3) |

#### WDPlacementUiTextRecord

3 table(s), 6 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ControlZone_PlacementDisplayTexts` | 1 | `GF/ControlZone/UI` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |
| `DT_ForwardOperatingBase_PlacementDisplayTexts` | 2 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| `DT_PlacementDisplayTexts` | 3 | `UI/Features/HUD/Placement/Data` | [round68-boundaries](../docs/evidence/round68-boundaries.md) |

#### FToolFont

1 table(s), 5 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ToolsTextAppearance` | 5 | `Tools/_EditorUILibrary/_Core/Font` | [Wardogs_Tools_v2](../content/Wardogs_Tools_v2.md) |

#### GrassLayerInfo

1 table(s), 5 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_GrassSettings` | 5 | `Environment/PCG/Runtime` | [Wardogs_Environment_v2](../content/Wardogs_Environment_v2.md) |

#### WDAmmoModifierTableRow

1 table(s), 5 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdammomodifiertablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_AmmoModifiers` | 5 | `GameMechanics/DamageSystem` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round39-weapons](../docs/evidence/round39-weapons.md), [round84-census-v4](../docs/evidence/round84-census-v4.md) (+3) |

#### WDPlayerIdentityRow

1 table(s), 5 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdplayeridentityrow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_PlayerIdentities` | 5 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIScoreboardStatTableRow

1 table(s), 5 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduiscoreboardstattablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ScoreboardStats_Default` | 5 | `UI/Features/Scoreboard/Widgets/Scoreboard/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDAutomatedTestClientProfile

1 table(s), 4 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdautomatedtestclientprofile).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ClientTestingProfiles` | 4 | `Tests/LoadTests/Orchestrators/RandomScatter/Data` | [Wardogs_Tests_v2](../content/Wardogs_Tests_v2.md), [round40-modes-ai-other](../docs/evidence/round40-modes-ai-other.md), [round41-modes-ai-other](../docs/evidence/round41-modes-ai-other.md) |

#### WDDevMenuMapsDataTableRow

3 table(s), 4 rows, 2 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wddevmenumapsdatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_DevMenuMaps` | 2 | `UI/Features/Frontend/DevMenu/Data` | not named |
| `DT_Gunsmith_DevMenuMaps` | 1 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| `DT_Vehiclesmith_DevMenuMaps` | 1 | `GF/Vehiclesmith/Data` | [Wardogs_GameFeatures_Vehiclesmith_v2](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) |

#### WDFactionDataTableRow

1 table(s), 4 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdfactiondatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_FactionData` | 4 | `GameMechanics/Gamemode/Data` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round84-census-v4](../docs/evidence/round84-census-v4.md) |

#### WDPingTypeData

1 table(s), 4 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdpingtypedata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_PingTypes` | 4 | `GameMechanics/Communication/Pings` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [player-movement](../season-2-changes/player-movement.md) |

#### WDUIInteractionContextStateDataTableRow

1 table(s), 4 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InteractionContextStateData` | 4 | `UI/Data/Interaction` | not named |

#### WDUIVendorType

1 table(s), 4 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_VendorTypes` | 4 | `UI/Features/Vendor/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDVehicleSlotPartRow

4 table(s), 4 rows, 4 named in docs. Expanded on [Vehicle Handling](../game-features/Wardogs_VehicleHandling_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Bobblehead_Faction_SlotParts` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Faction/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_Bobblehead_Grenade_SlotParts` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Grenade/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_Bobblehead_HeavyHelmet_SlotParts` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_HeavyHelmet/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| `DT_Bobblehead_Warpup_SlotParts` | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Warpup/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |

#### WDWagerActionDefinition

1 table(s), 4 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwageractiondefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_WagerActions` | 4 | `Meta/Wagers` | [wagers](../_wiki/progression-and-economy/wagers.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+3) |

#### WDClientHotConfigTableRow

1 table(s), 3 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdclienthotconfigtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ClientHotConfigs` | 3 | `Meta/ClientHotConfigs` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md), [rewards-unlocks](../season-2-changes/rewards-unlocks.md) |

#### WDControlZoneContributionModifierTableRow

1 table(s), 3 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdcontrolzonecontributionmodifiertablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ControlZoneContributionModifiers` | 3 | `GF/ControlZone/ControlZone/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |

#### WDMissionDefinition

1 table(s), 3 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdmissiondefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_PassiveMissions` | 3 | `Meta/Missions` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [rewards-unlocks](../season-2-changes/rewards-unlocks.md) |

#### WDUIRadialWheelTableRow

2 table(s), 3 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_RadialWheelTypeDatas` | 2 | `UI/Features/RadialWheel/Data` | not named |
| `DT_RadialWheelType_BuildToolData` | 1 | `GF/Items/Buildables/Data/BuildTool` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |

#### WDCurrencyDefinition

1 table(s), 2 rows, 1 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_CurrenciesDefinitions` | 2 | `Meta/CurrencyDefinitions` | [currencies](../_wiki/progression-and-economy/currencies.md), [Wardogs_Maps_v2](../content/Wardogs_Maps_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+5) |

#### WDUIIndicatorTableRow

1 table(s), 2 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Indicators` | 2 | `UI/Features/HUD/DamageIndicator/Data` | not named |

#### WDUIInteractableComponentStateDataTableRow

1 table(s), 2 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_InteractableComponentStateData` | 2 | `UI/Data/Interaction` | not named |

#### WDUIPopupButtonDataTableRow

1 table(s), 2 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_PopupButtons` | 2 | `UI/Features/Popups/Widgets/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### BHGameplayEffectTaggedTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#bhgameplayeffecttaggedtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Meta_ResourceEffects` | 1 | `Meta/Resources/Effects` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### SDUINotificationDataRow

1 table(s), 1 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_Notifications` | 1 | `UI/Features/HUD/RewardFeed/Data` | not named |

#### WDExchangeDefinitionTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdexchangedefinitiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_ExchangeDefinitions` | 1 | `Meta/ExchangeDefinitions` | [currencies](../_wiki/progression-and-economy/currencies.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+1) |

#### WDMetaSeasonDefinitionTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetaseasondefinitiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_SeasonDefinitions` | 1 | `Meta` | [season-01-cosmetics](../_wiki/progression-and-economy/season-01-cosmetics.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md) (+2) |

#### WDMockInvestmentItemTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdmockinvestmentitemtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_MockInvestments` | 1 | `Meta/MockInvestments` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [rewards-unlocks](../season-2-changes/rewards-unlocks.md) |

#### WDRewardDefinition

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdrewarddefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_DemoRewards` | 1 | `Meta/Challenges/Demo` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDUIInputActionDataTableRow

1 table(s), 1 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_UIInputActionData` | 1 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDWagerObjectiveCatalogDefinition

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwagerobjectivecatalogdefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_WagerObjectiveCatalog` | 1 | `Meta/Wagers` | [wagers](../_wiki/progression-and-economy/wagers.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+2) |

#### WDWagerPricingDefinition

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwagerpricingdefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| `DT_WagerPricing` | 1 | `Meta/Wagers` | [wagers](../_wiki/progression-and-economy/wagers.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [round36-econ](../docs/evidence/round36-econ.md) (+1) |
<!-- /datatable_catalog -->
