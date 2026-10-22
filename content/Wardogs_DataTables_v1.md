---
title: "Data Tables"
parent: "Content"
has_children: true
redirect_from: ["/Wardogs_DataTables_v1.html", "/Wardogs_DataTables_v1"]
---

# Wardogs: Data Tables Catalog
*Every `DataTable` export under [`data/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data), listed by row struct, with generic expanded tables for the gameplay structs that have no page of their own. Built by [`_tools/datatable_catalog.py`](../_tools/datatable_catalog.py) (`--write` is idempotent).*

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

211 table(s), 751 rows, 145 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_EntityData_Ext_Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Data/DT_EntityData_Ext_Emotes.json) | 6 | `GF/Emotes/Season01_EmotesData/Data` | [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md), [Wardogs_GameFeatures_Emotes_v2](../game-features/Wardogs_GameFeatures_Emotes_v2.md) |
| [`DT_EntityData_Ext_FGRP_006`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_006/Content/Data/DT_EntityData_Ext_FGRP_006.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_006/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_007`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_007/Content/Data/DT_EntityData_Ext_FGRP_007.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_007/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_008`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_008/Content/Data/DT_EntityData_Ext_FGRP_008.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_008/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_009`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_009/Content/Data/DT_EntityData_Ext_FGRP_009.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_009/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_010`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_010/Content/Data/DT_EntityData_Ext_FGRP_010.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_010/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_011/Content/Data/DT_EntityData_Ext_FGRP_011.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_012`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_012/Content/Data/DT_EntityData_Ext_FGRP_012.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_012/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_013/Content/Data/DT_EntityData_Ext_FGRP_013.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_014`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_014/Content/Data/DT_EntityData_Ext_FGRP_014.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_014/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_015`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_015/Content/Data/DT_EntityData_Ext_FGRP_015.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_015/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_016`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_016/Content/Data/DT_EntityData_Ext_FGRP_016.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_016/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_017`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_017/Content/Data/DT_EntityData_Ext_FGRP_017.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_017/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_018`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_018/Content/Data/DT_EntityData_Ext_FGRP_018.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_018/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_019`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/Data/DT_EntityData_Ext_FGRP_019.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_019/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_FGRP_020`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/Data/DT_EntityData_Ext_FGRP_020.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_020/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_Flares`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/Flares/Content/Data/DT_EntityData_Ext_Flares.json) | 1 | `GF/Vehicles/Flares/Data` | not named |
| [`DT_EntityData_Ext_LMG_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/Data/DT_EntityData_Ext_LMG_02.json) | 2 | `GF/Weapons/LMG/LMG_02/Data` | not named |
| [`DT_EntityData_Ext_MAGZ_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_002/Content/Data/DT_EntityData_Ext_MAGZ_002.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_002/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_003`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_003/Content/Data/DT_EntityData_Ext_MAGZ_003.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_003/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_004`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_004/Content/Data/DT_EntityData_Ext_MAGZ_004.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_004/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_005`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_005/Content/Data/DT_EntityData_Ext_MAGZ_005.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_005/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_006`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_006/Content/Data/DT_EntityData_Ext_MAGZ_006.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_006/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_008`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_008/Content/Data/DT_EntityData_Ext_MAGZ_008.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_008/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_011/Content/Data/DT_EntityData_Ext_MAGZ_011.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_012`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_012/Content/Data/DT_EntityData_Ext_MAGZ_012.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_012/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_024`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_024/Content/Data/DT_EntityData_Ext_MAGZ_024.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_024/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_026/Content/Data/DT_EntityData_Ext_MAGZ_026.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_026/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_034/Content/Data/DT_EntityData_Ext_MAGZ_034.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_034/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_043`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_043/Content/Data/DT_EntityData_Ext_MAGZ_043.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_043/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_046`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_046/Content/Data/DT_EntityData_Ext_MAGZ_046.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_046/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_051`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_051/Content/Data/DT_EntityData_Ext_MAGZ_051.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_051/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_052`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_052/Content/Data/DT_EntityData_Ext_MAGZ_052.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_052/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_053`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_053/Content/Data/DT_EntityData_Ext_MAGZ_053.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_053/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_054`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_054/Content/Data/DT_EntityData_Ext_MAGZ_054.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_054/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_055`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_055/Content/Data/DT_EntityData_Ext_MAGZ_055.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_055/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_056`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_056/Content/Data/DT_EntityData_Ext_MAGZ_056.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_056/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_057`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_057/Content/Data/DT_EntityData_Ext_MAGZ_057.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_057/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_059`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_059/Content/Data/DT_EntityData_Ext_MAGZ_059.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_059/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_060`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_060/Content/Data/DT_EntityData_Ext_MAGZ_060.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_060/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_061`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_061/Content/Data/DT_EntityData_Ext_MAGZ_061.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_061/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_062`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_062/Content/Data/DT_EntityData_Ext_MAGZ_062.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_062/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_063`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_063/Content/Data/DT_EntityData_Ext_MAGZ_063.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_063/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_064`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_064/Content/Data/DT_EntityData_Ext_MAGZ_064.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_064/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_065`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_065/Content/Data/DT_EntityData_Ext_MAGZ_065.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_065/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_066`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_066/Content/Data/DT_EntityData_Ext_MAGZ_066.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_066/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_067`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_067/Content/Data/DT_EntityData_Ext_MAGZ_067.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_067/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_068`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_068/Content/Data/DT_EntityData_Ext_MAGZ_068.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_068/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_069`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_069/Content/Data/DT_EntityData_Ext_MAGZ_069.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_069/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_070`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_070/Content/Data/DT_EntityData_Ext_MAGZ_070.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_070/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MAGZ_071`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_071/Content/Data/DT_EntityData_Ext_MAGZ_071.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_071/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MK22`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/MK22/Content/Data/DT_EntityData_Ext_MK22.json) | 2 | `GF/Weapons/Sniper/MK22/Data` | not named |
| [`DT_EntityData_Ext_MUZL_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_013/Content/Data/DT_EntityData_Ext_MUZL_013.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_014`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_014/Content/Data/DT_EntityData_Ext_MUZL_014.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_014/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_019`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_019/Content/Data/DT_EntityData_Ext_MUZL_019.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_019/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_020`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_020/Content/Data/DT_EntityData_Ext_MUZL_020.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_020/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_022`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_022/Content/Data/DT_EntityData_Ext_MUZL_022.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_022/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_023`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_023/Content/Data/DT_EntityData_Ext_MUZL_023.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_023/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_024`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_024/Content/Data/DT_EntityData_Ext_MUZL_024.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_024/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_025`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_025/Content/Data/DT_EntityData_Ext_MUZL_025.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_025/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_027/MUZL_027/Content/Data/DT_EntityData_Ext_MUZL_027.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_027/MUZL_027/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_028/Content/Data/DT_EntityData_Ext_MUZL_028.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_028/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_029/Content/Data/DT_EntityData_Ext_MUZL_029.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_029/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_030/Content/Data/DT_EntityData_Ext_MUZL_030.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_030/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_031/Content/Data/DT_EntityData_Ext_MUZL_031.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_031/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_032/Content/Data/DT_EntityData_Ext_MUZL_032.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_032/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_037`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_037/Content/Data/DT_EntityData_Ext_MUZL_037.json) | 2 | `GF/Weapons/Attachments/Muzzle/MUZL_037/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_038`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_038/Content/Data/DT_EntityData_Ext_MUZL_038.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_038/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_039`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_039/Content/Data/DT_EntityData_Ext_MUZL_039.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_039/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_040`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_040/Content/Data/DT_EntityData_Ext_MUZL_040.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_040/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_041`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_041/Content/Data/DT_EntityData_Ext_MUZL_041.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_041/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_044`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_044/Content/Data/DT_EntityData_Ext_MUZL_044.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_044/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_045`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_045/Content/Data/DT_EntityData_Ext_MUZL_045.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_045/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_046`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_046/Content/Data/DT_EntityData_Ext_MUZL_046.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_046/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_047`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_047/Content/Data/DT_EntityData_Ext_MUZL_047.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_047/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_048`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_048/Content/Data/DT_EntityData_Ext_MUZL_048.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_048/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_049`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_049/Content/Data/DT_EntityData_Ext_MUZL_049.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_049/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_050`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_050/Content/Data/DT_EntityData_Ext_MUZL_050.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_050/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_051`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_051/Content/Data/DT_EntityData_Ext_MUZL_051.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_051/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_052`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_052/Content/Data/DT_EntityData_Ext_MUZL_052.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_052/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_053`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_053/Content/Data/DT_EntityData_Ext_MUZL_053.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_053/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_054`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_054/Content/Data/DT_EntityData_Ext_MUZL_054.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_054/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_055`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_055/Content/Data/DT_EntityData_Ext_MUZL_055.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_055/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_056`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_056/Content/Data/DT_EntityData_Ext_MUZL_056.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_056/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_057`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_057/Content/Data/DT_EntityData_Ext_MUZL_057.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_057/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_058`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_058/Content/Data/DT_EntityData_Ext_MUZL_058.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_058/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_059`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_059/Content/Data/DT_EntityData_Ext_MUZL_059.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_059/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_060`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_060/Content/Data/DT_EntityData_Ext_MUZL_060.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_060/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_061`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_061/Content/Data/DT_EntityData_Ext_MUZL_061.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_061/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_062`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_062/Content/Data/DT_EntityData_Ext_MUZL_062.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_062/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_067`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_067/Content/Data/DT_EntityData_Ext_MUZL_067.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_067/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_068`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_068/Content/Data/DT_EntityData_Ext_MUZL_068.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_068/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_069`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_069/Content/Data/DT_EntityData_Ext_MUZL_069.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_069/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_070`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_070/Content/Data/DT_EntityData_Ext_MUZL_070.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_070/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_071`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_071/Content/Data/DT_EntityData_Ext_MUZL_071.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_071/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_MUZL_072`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_072/Content/Data/DT_EntityData_Ext_MUZL_072.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_072/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_Pistol_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Pistols/Pistol_02/Content/Data/DT_EntityData_Ext_Pistol_02.json) | 1 | `GF/Weapons/Pistols/Pistol_02/Data` | not named |
| [`DT_EntityData_Ext_SGHT_009`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_009/Content/Data/DT_EntityData_Ext_SGHT_009.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_009/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_011/Content/Data/DT_EntityData_Ext_SGHT_011.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_013/Content/Data/DT_EntityData_Ext_SGHT_013.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_016`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_016/Content/Data/DT_EntityData_Ext_SGHT_016.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_016/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_023`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_023/Content/Data/DT_EntityData_Ext_SGHT_023.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_023/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_024`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_024/Content/Data/DT_EntityData_Ext_SGHT_024.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_024/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_025`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_025/Content/Data/DT_EntityData_Ext_SGHT_025.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_025/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_026/Content/Data/DT_EntityData_Ext_SGHT_026.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_026/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_027/Content/Data/DT_EntityData_Ext_SGHT_027.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_027/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_028/Content/Data/DT_EntityData_Ext_SGHT_028.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_028/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_029/Content/Data/DT_EntityData_Ext_SGHT_029.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_029/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_030/Content/Data/DT_EntityData_Ext_SGHT_030.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_030/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_031/Content/Data/DT_EntityData_Ext_SGHT_031.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_031/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_032/Content/Data/DT_EntityData_Ext_SGHT_032.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_032/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_033`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_033/Content/Data/DT_EntityData_Ext_SGHT_033.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_033/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_034/Content/Data/DT_EntityData_Ext_SGHT_034.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_034/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_036`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_036/Content/Data/DT_EntityData_Ext_SGHT_036.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_036/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_037`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_037/Content/Data/DT_EntityData_Ext_SGHT_037.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_037/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_038`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_038/Content/Data/DT_EntityData_Ext_SGHT_038.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_038/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_039`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_039/Content/Data/DT_EntityData_Ext_SGHT_039.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_039/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SGHT_040`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_040/Content/Data/DT_EntityData_Ext_SGHT_040.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_040/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SMG_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/SMG_03/Content/Data/DT_EntityData_Ext_SMG_03.json) | 1 | `GF/Weapons/SMG/SMG_03/Data` | not named |
| [`DT_EntityData_Ext_SR_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/SR_04/Content/Data/DT_EntityData_Ext_SR_04.json) | 2 | `GF/Weapons/Sniper/SR_04/Data` | not named |
| [`DT_EntityData_Ext_SV98`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_008/Content/Data/DT_EntityData_Ext_SV98.json) | 2 | `GF/Weapons/Platforms/WEPN_008/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_SVDM`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/SVDM/Content/Data/DT_EntityData_Ext_SVDM.json) | 2 | `GF/Weapons/DMR/SVDM/Data` | not named |
| [`DT_EntityData_Ext_VehicleSmoke`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleSmoke/Content/Data/DT_EntityData_Ext_VehicleSmoke.json) | 1 | `GF/Vehicles/VehicleSmoke/Data` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_EntityData_Ext_WEPN_017`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_EntityData_Ext_WEPN_017.json) | 1 | `GF/Weapons/Platforms/WEPN_017/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_026/Content/Data/DT_EntityData_Ext_WEPN_026.json) | 1 | `GF/Weapons/Platforms/WEPN_026/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_027/Content/Data/DT_EntityData_Ext_WEPN_027.json) | 1 | `GF/Weapons/Platforms/WEPN_027/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_028/Content/Data/DT_EntityData_Ext_WEPN_028.json) | 1 | `GF/Weapons/Platforms/WEPN_028/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_029/Content/Data/DT_EntityData_Ext_WEPN_029.json) | 1 | `GF/Weapons/Platforms/WEPN_029/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_030/Content/Data/DT_EntityData_Ext_WEPN_030.json) | 1 | `GF/Weapons/Platforms/WEPN_030/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/DT_EntityData_Ext_WEPN_031.json) | 1 | `GF/Weapons/Platforms/WEPN_031/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_032/Content/Data/DT_EntityData_Ext_WEPN_032.json) | 1 | `GF/Weapons/Platforms/WEPN_032/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_033`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_033/Content/Data/DT_EntityData_Ext_WEPN_033.json) | 1 | `GF/Weapons/Platforms/WEPN_033/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/DT_EntityData_Ext_WEPN_034.json) | 1 | `GF/Weapons/Platforms/WEPN_034/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_035`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/Data/DT_EntityData_Ext_WEPN_035.json) | 1 | `GF/Weapons/Platforms/WEPN_035/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_036`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/DT_EntityData_Ext_WEPN_036.json) | 1 | `GF/Weapons/Platforms/WEPN_036/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_Ext_WEPN_037`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DT_EntityData_Ext_WEPN_037.json) | 1 | `GF/Weapons/Platforms/WEPN_037/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_EntityData_UI_Battery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/DT_EntityData_UI_Battery.json) | 2 | `GF/Items/Battery/Data` | not named |
| [`DT_EntityData_UI_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/DT_EntityData_UI_Buildables.json) | 36 | `GF/Items/Buildables/Data` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_EntityData_UI_Ext_AT_Mine`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/AT_mine/Content/Data/DT_EntityData_UI_Ext_AT_Mine.json) | 1 | `GF/Items/AT_mine/Data` | not named |
| [`DT_EntityData_UI_Ext_Armor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/DT_EntityData_UI_Ext_Armor.json) | 16 | `GF/Items/Armor/Data` | not named |
| [`DT_EntityData_UI_Ext_Binoculars`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Binoculars/Content/Data/DT_EntityData_UI_Ext_Binoculars.json) | 1 | `GF/Items/Binoculars/Data` | not named |
| [`DT_EntityData_UI_Ext_C4`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/C4/Content/Data/DT_EntityData_UI_Ext_C4.json) | 1 | `GF/Items/C4/Data` | not named |
| [`DT_EntityData_UI_Ext_C4Explosive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/C4/Content/Data/DT_EntityData_UI_Ext_C4Explosive.json) | 1 | `GF/Items/C4/Data` | not named |
| [`DT_EntityData_UI_Ext_Claymore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Claymore/Content/Data/DT_EntityData_UI_Ext_Claymore.json) | 1 | `GF/Items/Claymore/Data` | not named |
| [`DT_EntityData_UI_Ext_CombatBow`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataTable/DT_EntityData_UI_Ext_CombatBow.json) | 3 | `GF/Items/CombatBow/Data/DataTable` | not named |
| [`DT_EntityData_UI_Ext_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Data/DT_EntityData_UI_Ext_Crowbar.json) | 1 | `GF/Items/Crowbar/Data` | not named |
| [`DT_EntityData_UI_Ext_Defibrillator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Defibrillator/Content/Data/DT_EntityData_UI_Ext_Defibrillator.json) | 1 | `GF/Items/Defibrillator/Data` | not named |
| [`DT_EntityData_UI_Ext_Enox`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Enox/Content/Data/DT_EntityData_UI_Ext_Enox.json) | 3 | `GF/Items/Enox/Data` | not named |
| [`DT_EntityData_UI_Ext_FuelCanister`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/FuelCanister/Content/Data/DT_EntityData_UI_Ext_FuelCanister.json) | 1 | `GF/Items/FuelCanister/Data` | not named |
| [`DT_EntityData_UI_Ext_HotPotato`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/DT_EntityData_UI_Ext_HotPotato.json) | 1 | `GF/HotPotato/Data` | not named |
| [`DT_EntityData_UI_Ext_IED`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/IED/Content/Data/DT_EntityData_UI_Ext_IED.json) | 2 | `GF/Items/IED/Data` | not named |
| [`DT_EntityData_UI_Ext_MedKit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MedKit/Content/Data/DT_EntityData_UI_Ext_MedKit.json) | 1 | `GF/Items/MedKit/Data` | not named |
| [`DT_EntityData_UI_Ext_Molotov`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DT_EntityData_UI_Ext_Molotov.json) | 1 | `GF/Items/Molotov/Data` | not named |
| [`DT_EntityData_UI_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_EntityData_UI_Ext_Parachutes.json) | 2 | `GF/Parachutes/Content` | [Wardogs_GameFeatures_Parachutes_v2](../game-features/Wardogs_GameFeatures_Parachutes_v2.md) |
| [`DT_EntityData_UI_Ext_RangeFinder`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/DT_EntityData_UI_Ext_RangeFinder.json) | 3 | `GF/Items/RangeFinder/Data` | not named |
| [`DT_EntityData_UI_Ext_SmokeGrenade`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/SmokeGrenade/Content/Data/DT_EntityData_UI_Ext_SmokeGrenade.json) | 8 | `GF/Items/SmokeGrenade/Data` | not named |
| [`DT_EntityData_UI_Ext_StimPen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DT_EntityData_UI_Ext_StimPen.json) | 1 | `GF/Items/StimPen/Data` | not named |
| [`DT_EntityData_UI_Ext_VehicleRepairTool`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/VehicleRepairTool/Content/Data/DT_EntityData_UI_Ext_VehicleRepairTool.json) | 3 | `GF/Items/VehicleRepairTool/Data` | not named |
| [`DT_EntityData_UI_Garage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Garage.json) | 2 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EntityData_UI_GarageMarket_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/DataTables/DT_EntityData_UI_GarageMarket_SupplyCrates.json) | 8 | `GF/Vehicles/SupplyCrates/DataTables` | not named |
| [`DT_EntityData_UI_GoldExchange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/GoldExchange/Data/DT_EntityData_UI_GoldExchange.json) | 1 | `UI/Features/Frontend/GoldExchange/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EntityData_UI_Items`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Items.json) | 296 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EntityData_UI_Keycards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Keycard/Content/Data/DT_EntityData_UI_Keycards.json) | 6 | `GF/Items/Keycard/Data` | not named |
| [`DT_EntityData_UI_Misc`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_Misc.json) | 1 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EntityData_UI_TNK01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/DataTables/DT_EntityData_UI_TNK01.json) | 12 | `GF/Vehicles/TNK_01/DataTables` | not named |
| [`DT_EntityData_UI_TNK04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_EntityData_UI_TNK04.json) | 6 | `GF/Vehicles/TNK_04/DataTables` | not named |
| [`DT_EntityData_UI_VehicleAmmo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Entities/DT_EntityData_UI_VehicleAmmo.json) | 5 | `UI/Data/Entities` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EntityData_UI_Vehicles_ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_EntityData_UI_Vehicles_ROT_02.json) | 5 | `GF/Vehicles/ROT_02/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/DataTables/DT_EntityData_UI_Vehicles_ROT_03.json) | 1 | `GF/Vehicles/ROT_03/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_ROT_03_WeaponVariants`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/DataTables/DT_EntityData_UI_Vehicles_ROT_03_WeaponVariants.json) | 6 | `GF/Vehicles/ROT_03_WeaponVariants/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/DataTables/DT_EntityData_UI_Vehicles_ROT_04.json) | 1 | `GF/Vehicles/ROT_04/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_ROT_04_MachineGun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/DataTables/DT_EntityData_UI_Vehicles_ROT_04_MachineGun.json) | 3 | `GF/Vehicles/ROT_04_MachineGun/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_SPW_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/DataTables/DT_EntityData_UI_Vehicles_SPW_01.json) | 3 | `GF/Vehicles/SPW_01/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_STN_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/DataTables/DT_EntityData_UI_Vehicles_STN_01.json) | 2 | `GF/Vehicles/STN_01/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/DataTables/DT_EntityData_UI_Vehicles_STN_02.json) | 2 | `GF/Vehicles/STN_02/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/DataTable/DT_EntityData_UI_Vehicles_STN_03.json) | 2 | `GF/Vehicles/STN_03/DataTable` | not named |
| [`DT_EntityData_UI_Vehicles_STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/DataTables/DT_EntityData_UI_Vehicles_STN_04.json) | 1 | `GF/Vehicles/STN_04/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/DataTable/DT_EntityData_UI_Vehicles_STN_05.json) | 3 | `GF/Vehicles/STN_05/DataTable` | not named |
| [`DT_EntityData_UI_Vehicles_STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_EntityData_UI_Vehicles_STN_06.json) | 2 | `GF/Vehicles/STN_06/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_01.json) | 1 | `GF/Vehicles/WHL_01/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_02.json) | 2 | `GF/Vehicles/WHL_02/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_02_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02_RingTurret/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_02_RingTurret.json) | 3 | `GF/Vehicles/WHL_02_RingTurret/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_05_Humvee`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_05_Humvee.json) | 1 | `GF/Vehicles/WHL_05/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_05_Minigun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_05_Minigun.json) | 3 | `GF/Vehicles/WHL_05_Minigun/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_05_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_RingTurret/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_05_RingTurret.json) | 3 | `GF/Vehicles/WHL_05_RingTurret/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_06_DuneBuggy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_06_DuneBuggy.json) | 1 | `GF/Vehicles/WHL_06/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_07_ArmouredBattle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07_ArmouredBattle/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_07_ArmouredBattle.json) | 3 | `GF/Vehicles/WHL_07_ArmouredBattle/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_07_Ural`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_07_Ural.json) | 2 | `GF/Vehicles/WHL_07/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_08.json) | 1 | `GF/Vehicles/WHL_08/DataTables` | not named |
| [`DT_EntityData_UI_Vehicles_WHL_08_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/DataTables/DT_EntityData_UI_Vehicles_WHL_08_RingTurret.json) | 2 | `GF/Vehicles/WHL_08_RingTurret/DataTables` | not named |
| [`DT_EntityData_UI_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_EntityData_UI_Wagers.json) | 1 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |
| [`DT_Ext_Entity_UI_MusicTape_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_01/Content/Data/DT_Ext_Entity_UI_MusicTape_01.json) | 1 | `GF/Items/MusicTapes/MusicTape_01/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_02/Content/Data/DT_Ext_Entity_UI_MusicTape_02.json) | 1 | `GF/Items/MusicTapes/MusicTape_02/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_03/Content/Data/DT_Ext_Entity_UI_MusicTape_03.json) | 1 | `GF/Items/MusicTapes/MusicTape_03/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_04/Content/Data/DT_Ext_Entity_UI_MusicTape_04.json) | 1 | `GF/Items/MusicTapes/MusicTape_04/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_05/Content/Data/DT_Ext_Entity_UI_MusicTape_05.json) | 1 | `GF/Items/MusicTapes/MusicTape_05/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_06/Content/Data/DT_Ext_Entity_UI_MusicTape_06.json) | 1 | `GF/Items/MusicTapes/MusicTape_06/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_07`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_07/Content/Data/DT_Ext_Entity_UI_MusicTape_07.json) | 1 | `GF/Items/MusicTapes/MusicTape_07/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_08/Content/Data/DT_Ext_Entity_UI_MusicTape_08.json) | 1 | `GF/Items/MusicTapes/MusicTape_08/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_09`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_09/Content/Data/DT_Ext_Entity_UI_MusicTape_09.json) | 1 | `GF/Items/MusicTapes/MusicTape_09/Data` | not named |
| [`DT_Ext_Entity_UI_MusicTape_11`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/Data/DT_Ext_Entity_UI_MusicTape_11.json) | 1 | `GF/Items/MusicTapes/MusicTape_11/Data` | not named |
| [`DT_Gunsmith_EntityData_UI_DecalTextures`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_Gunsmith_EntityData_UI_DecalTextures.json) | 5 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_Gunsmith_EntityData_UI_PaintMaskTextures`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_Gunsmith_EntityData_UI_PaintMaskTextures.json) | 4 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_Gunsmith_EntityData_UI_PaintMasteryTextures`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_Gunsmith_EntityData_UI_PaintMasteryTextures.json) | 6 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_Gunsmith_EntityData_UI_ReticleTextures`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_Gunsmith_EntityData_UI_ReticleTextures.json) | 17 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_InteractionContext_ForwardOperatingBase`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/ForwardOperatingBase/DT_InteractionContext_ForwardOperatingBase.json) | 4 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_InteractionContexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_InteractionContexts.json) | 70 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_InteractionContexts_ForceOpenDoor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Data/Interaction/DT_InteractionContexts_ForceOpenDoor.json) | 1 | `GF/Items/Crowbar/Data/Interaction` | not named |
| [`DT_InteractionContexts_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DT_InteractionContexts_HotZoneMagnet.json) | 3 | `GF/WorldFeatures/HotZoneMagnet/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_InteractionContexts_Lockpicking`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/Lockpicking/Content/Data/Interaction/DT_InteractionContexts_Lockpicking.json) | 1 | `GF/Vehicles/Lockpicking/Data/Interaction` | not named |
| [`DT_InteractionContexts_Lootable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_InteractionContexts_Lootable.json) | 2 | `GF/WorldFeatures/Lootable/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |

#### WDChallengeRewardDefinition

7 table(s), 486 rows, 5 named in docs. Expanded on [Challenges](../game-features/Wardogs_Challenges_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ChallengeRewards_EndOfMatch`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_EndOfMatch.json) | 5 | `Meta/Challenges` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |
| [`DT_ChallengeRewards_SessionEvents_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json) | 47 | `GF/Rewards/BuildableRewards/Rewards` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| [`DT_ChallengeRewards_SessionEvents_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengeRewards_SessionEvents_Crowbar.json) | 1 | `GF/Items/Crowbar/Rewards` | not named |
| [`DT_ChallengeRewards_SessionEvents_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_HotZoneMagnet.json) | 3 | `GF/WorldFeatures/HotZoneMagnet/Data/Challenges` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_ChallengeRewards_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_ChallengeRewards_SessionEvents_Shared.json) | 298 | `Meta/Challenges` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md) (+3) |
| [`DT_ChallengeRewards_SessionEvents_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_ChallengeRewards_SessionEvents_Spotting.json) | 130 | `GF/Spotting/Data/Challenges` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_ChallengeRewards_TeamOffence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/DT_ChallengeRewards_TeamOffence.json) | 2 | `GF/TeamOffence/Challenges` | not named |

#### BHUserSettingDataTableRow

8 table(s), 390 rows, 1 named in docs. Expanded on [Settings and Inputs](../content/Wardogs_SettingsAndInputs_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Itemsmith_Flair_Settings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_Settings.json) | 2 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| [`DT_Settings_Accessibility`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Accessibility/DT_Settings_Accessibility.json) | 30 | `GameMechanics/Settings/Accessibility` | not named |
| [`DT_Settings_Audio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Audio/DT_Settings_Audio.json) | 22 | `GameMechanics/Settings/Audio` | not named |
| [`DT_Settings_Controls`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Controls/DT_Settings_Controls.json) | 121 | `GameMechanics/Settings/Controls` | not named |
| [`DT_Settings_Extra`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Extras/DT_Settings_Extra.json) | 1 | `GameMechanics/Settings/Extras` | not named |
| [`DT_Settings_General`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/General/DT_Settings_General.json) | 25 | `GameMechanics/Settings/General` | not named |
| [`DT_Settings_Keybindings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Keybindings/DT_Settings_Keybindings.json) | 146 | `GameMechanics/Settings/Keybindings` | not named |
| [`DT_Settings_Video`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Video/DT_Settings_Video.json) | 43 | `GameMechanics/Settings/Video` | not named |

#### WDUIGameplayTagToTextTableRow

18 table(s), 375 rows, 18 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Ext_GameplayTagToText_Calibers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataTable/DT_Ext_GameplayTagToText_Calibers.json) | 1 | `GF/Items/CombatBow/Data/DataTable` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Ammunition`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Ammunition.json) | 14 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Archetypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Archetypes.json) | 16 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Calibers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Calibers.json) | 31 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Categories`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Categories.json) | 112 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Components`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Components.json) | 7 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Damage`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Damage.json) | 9 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_EventLog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_EventLog.json) | 6 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_InventorySlots`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_InventorySlots.json) | 37 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_GameplayTagToText_Itemsmith.json) | 36 | `GF/Itemsmith/UI/Data` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md), [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| [`DT_GameplayTagToText_PlayerStates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_PlayerStates.json) | 5 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Prompts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Prompts.json) | 4 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Roles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Roles.json) | 13 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_SceneNames`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_SceneNames.json) | 38 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_ServerTags`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_ServerTags.json) | 24 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_TeamOffence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/UI/Data/DT_GameplayTagToText_TeamOffence.json) | 7 | `GF/TeamOffence/UI/Data` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Tooltips`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Tooltips.json) | 10 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |
| [`DT_GameplayTagToText_Tutorials`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/GameplayTagsToText/DT_GameplayTagToText_Tutorials.json) | 5 | `UI/Data/GameplayTagsToText` | [Wardogs_TagDisplayText_v1](../content/Wardogs_TagDisplayText_v1.md) |

#### WDVariantRewardLookupRow

16 table(s), 333 rows, 16 named in docs. Expanded on [Reward Lookup (Session Events)](../content/Wardogs_RewardLookup_SessionEvents_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_RewardLookup_SessionEvent_BuildableDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_BuildableDestroyed.json) | 36 | `GF/Rewards/BuildableRewards/Rewards/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| [`DT_RewardLookup_SessionEvent_DestroySupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroySupplyCrate.json) | 10 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_DestroyVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicle.json) | 34 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleFOBSuppliedAssist.json) | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleLogisticAssist.json) | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleReviveAssist.json) | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_DestroyVehicleSection`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_DestroyVehicleSection.json) | 28 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_HealPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer.json) | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_LogisticAssist.json) | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_HealPlayer_ReviveAssist.json) | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_RepairVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RepairVehicle.json) | 3 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_RevivePlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayer.json) | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerLogisticAssist.json) | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_RevivePlayerReviveAssist.json) | 6 | `GF/Challenges_KOTH/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_RewardLookup_SessionEvent_Spotting_Added`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Added.json) | 51 | `GF/Spotting/Data/Challenges/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_RewardLookup_SessionEvent_Spotting_Removed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_Spotting_Removed.json) | 51 | `GF/Spotting/Data/Challenges/LookupRegistries/Tables` | [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |

#### WDVendorData

206 table(s), 328 rows, 159 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_AttachmentMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_AttachmentMarket.json) | 17 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |
| [`DT_Ext_VendorData_MusicTape_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_01/Content/Data/DT_Ext_VendorData_MusicTape_01.json) | 1 | `GF/Items/MusicTapes/MusicTape_01/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_02/Content/Data/DT_Ext_VendorData_MusicTape_02.json) | 1 | `GF/Items/MusicTapes/MusicTape_02/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_03/Content/Data/DT_Ext_VendorData_MusicTape_03.json) | 1 | `GF/Items/MusicTapes/MusicTape_03/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_04/Content/Data/DT_Ext_VendorData_MusicTape_04.json) | 1 | `GF/Items/MusicTapes/MusicTape_04/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_05/Content/Data/DT_Ext_VendorData_MusicTape_05.json) | 1 | `GF/Items/MusicTapes/MusicTape_05/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_06/Content/Data/DT_Ext_VendorData_MusicTape_06.json) | 1 | `GF/Items/MusicTapes/MusicTape_06/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_07`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_07/Content/Data/DT_Ext_VendorData_MusicTape_07.json) | 1 | `GF/Items/MusicTapes/MusicTape_07/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_08/Content/Data/DT_Ext_VendorData_MusicTape_08.json) | 1 | `GF/Items/MusicTapes/MusicTape_08/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_09`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_09/Content/Data/DT_Ext_VendorData_MusicTape_09.json) | 1 | `GF/Items/MusicTapes/MusicTape_09/Data` | not named |
| [`DT_Ext_VendorData_MusicTape_11`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MusicTapes/MusicTape_11/Content/Data/DT_Ext_VendorData_MusicTape_11.json) | 1 | `GF/Items/MusicTapes/MusicTape_11/Data` | not named |
| [`DT_GarageMarket_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/DataTables/DT_GarageMarket_SupplyCrates.json) | 8 | `GF/Vehicles/SupplyCrates/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GearMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_GearMarket.json) | 13 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |
| [`DT_UtilityMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_UtilityMarket.json) | 3 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |
| [`DT_VehicleMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorVehicles/DT_VehicleMarket.json) | 0 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorVehicles` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md) |
| [`DT_VehicleMarket_ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_VehicleMarket_ROT_02.json) | 1 | `GF/Vehicles/ROT_02/DataTables` | not named |
| [`DT_VehicleMarket_ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/DataTables/DT_VehicleMarket_ROT_03.json) | 1 | `GF/Vehicles/ROT_03/DataTables` | not named |
| [`DT_VehicleMarket_ROT_03_WeaponVariants`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03_WeaponVariants/Content/DataTables/DT_VehicleMarket_ROT_03_WeaponVariants.json) | 2 | `GF/Vehicles/ROT_03_WeaponVariants/DataTables` | not named |
| [`DT_VehicleMarket_ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/DataTables/DT_VehicleMarket_ROT_04.json) | 1 | `GF/Vehicles/ROT_04/DataTables` | not named |
| [`DT_VehicleMarket_ROT_04_MachineGun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04_MachineGun/Content/DataTables/DT_VehicleMarket_ROT_04_MachineGun.json) | 1 | `GF/Vehicles/ROT_04_MachineGun/DataTables` | not named |
| [`DT_VehicleMarket_TNK_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/DataTables/DT_VehicleMarket_TNK_01.json) | 3 | `GF/Vehicles/TNK_01/DataTables` | not named |
| [`DT_VehicleMarket_TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_VehicleMarket_TNK_04.json) | 1 | `GF/Vehicles/TNK_04/DataTables` | not named |
| [`DT_VehicleMarket_WHL_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/DataTables/DT_VehicleMarket_WHL_01.json) | 1 | `GF/Vehicles/WHL_01/DataTables` | not named |
| [`DT_VehicleMarket_WHL_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/DataTables/DT_VehicleMarket_WHL_02.json) | 2 | `GF/Vehicles/WHL_02/DataTables` | not named |
| [`DT_VehicleMarket_WHL_02_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02_RingTurret/Content/DataTables/DT_VehicleMarket_WHL_02_RingTurret.json) | 1 | `GF/Vehicles/WHL_02_RingTurret/DataTables` | not named |
| [`DT_VehicleMarket_WHL_05_Humvee`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/DataTables/DT_VehicleMarket_WHL_05_Humvee.json) | 1 | `GF/Vehicles/WHL_05/DataTables` | not named |
| [`DT_VehicleMarket_WHL_05_Minigun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/DataTables/DT_VehicleMarket_WHL_05_Minigun.json) | 1 | `GF/Vehicles/WHL_05_Minigun/DataTables` | not named |
| [`DT_VehicleMarket_WHL_05_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_RingTurret/Content/DataTables/DT_VehicleMarket_WHL_05_RingTurret.json) | 1 | `GF/Vehicles/WHL_05_RingTurret/DataTables` | not named |
| [`DT_VehicleMarket_WHL_06_DuneBuggy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/DataTables/DT_VehicleMarket_WHL_06_DuneBuggy.json) | 1 | `GF/Vehicles/WHL_06/DataTables` | not named |
| [`DT_VehicleMarket_WHL_07_ArmouredBattle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07_ArmouredBattle/Content/DataTables/DT_VehicleMarket_WHL_07_ArmouredBattle.json) | 1 | `GF/Vehicles/WHL_07_ArmouredBattle/DataTables` | not named |
| [`DT_VehicleMarket_WHL_07_Ural`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/DataTables/DT_VehicleMarket_WHL_07_Ural.json) | 2 | `GF/Vehicles/WHL_07/DataTables` | not named |
| [`DT_VehicleMarket_WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/DataTables/DT_VehicleMarket_WHL_08.json) | 1 | `GF/Vehicles/WHL_08/DataTables` | not named |
| [`DT_VehicleMarket_WHL_08_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/DataTables/DT_VehicleMarket_WHL_08_RingTurret.json) | 1 | `GF/Vehicles/WHL_08_RingTurret/DataTables` | not named |
| [`DT_VendorData_Ext_AR_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_002/Content/Data/DT_VendorData_Ext_AR_02.json) | 1 | `GF/Weapons/Platforms/WEPN_002/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_AT_Mine`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/AT_mine/Content/Data/DT_VendorData_Ext_AT_Mine.json) | 1 | `GF/Items/AT_mine/Data` | not named |
| [`DT_VendorData_Ext_Armor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Armor/Content/Data/DT_VendorData_Ext_Armor.json) | 14 | `GF/Items/Armor/Data` | not named |
| [`DT_VendorData_Ext_Battery`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Battery/Content/Data/DT_VendorData_Ext_Battery.json) | 2 | `GF/Items/Battery/Data` | not named |
| [`DT_VendorData_Ext_Binoculars`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Binoculars/Content/Data/DT_VendorData_Ext_Binoculars.json) | 1 | `GF/Items/Binoculars/Data` | not named |
| [`DT_VendorData_Ext_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/DT_VendorData_Ext_Buildables.json) | 8 | `GF/Items/Buildables/Data` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_VendorData_Ext_C4`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/C4/Content/Data/DT_VendorData_Ext_C4.json) | 2 | `GF/Items/C4/Data` | not named |
| [`DT_VendorData_Ext_Claymore`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Claymore/Content/Data/DT_VendorData_Ext_Claymore.json) | 1 | `GF/Items/Claymore/Data` | not named |
| [`DT_VendorData_Ext_CombatBow`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataTable/DT_VendorData_Ext_CombatBow.json) | 3 | `GF/Items/CombatBow/Data/DataTable` | not named |
| [`DT_VendorData_Ext_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Data/DT_VendorData_Ext_Crowbar.json) | 1 | `GF/Items/Crowbar/Data` | not named |
| [`DT_VendorData_Ext_DMR_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_007/Content/Data/DT_VendorData_Ext_DMR_01.json) | 1 | `GF/Weapons/Platforms/WEPN_007/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_Defibrillator`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Defibrillator/Content/Data/DT_VendorData_Ext_Defibrillator.json) | 1 | `GF/Items/Defibrillator/Data` | not named |
| [`DT_VendorData_Ext_Enox`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Enox/Content/Data/DT_VendorData_Ext_Enox.json) | 3 | `GF/Items/Enox/Data` | not named |
| [`DT_VendorData_Ext_FGRP_006`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_006/Content/Data/DT_VendorData_Ext_FGRP_006.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_006/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_007`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_007/Content/Data/DT_VendorData_Ext_FGRP_007.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_007/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_008`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_008/Content/Data/DT_VendorData_Ext_FGRP_008.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_008/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_009`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_009/Content/Data/DT_VendorData_Ext_FGRP_009.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_009/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_010`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_010/Content/Data/DT_VendorData_Ext_FGRP_010.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_010/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_011/Content/Data/DT_VendorData_Ext_FGRP_011.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_012`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_012/Content/Data/DT_VendorData_Ext_FGRP_012.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_012/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_013/Content/Data/DT_VendorData_Ext_FGRP_013.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_014`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_014/Content/Data/DT_VendorData_Ext_FGRP_014.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_014/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_015`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_015/Content/Data/DT_VendorData_Ext_FGRP_015.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_015/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_016`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_016/Content/Data/DT_VendorData_Ext_FGRP_016.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_016/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_017`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_017/Content/Data/DT_VendorData_Ext_FGRP_017.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_017/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_018`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_018/Content/Data/DT_VendorData_Ext_FGRP_018.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_018/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_019`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_019/Content/Data/DT_VendorData_Ext_FGRP_019.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_019/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_FGRP_020`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Foregrips/FGRP_020/Content/Data/DT_VendorData_Ext_FGRP_020.json) | 1 | `GF/Weapons/Attachments/Foregrips/FGRP_020/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_Flares`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/Flares/Content/Data/DT_VendorData_Ext_Flares.json) | 1 | `GF/Vehicles/Flares/Data` | not named |
| [`DT_VendorData_Ext_FuelCanister`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/FuelCanister/Content/Data/DT_VendorData_Ext_FuelCanister.json) | 1 | `GF/Items/FuelCanister/Data` | not named |
| [`DT_VendorData_Ext_IED`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/IED/Content/Data/DT_VendorData_Ext_IED.json) | 1 | `GF/Items/IED/Data` | not named |
| [`DT_VendorData_Ext_MAGZ_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_002/Content/Data/DT_VendorData_Ext_MAGZ_002.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_002/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_003`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_003/Content/Data/DT_VendorData_Ext_MAGZ_003.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_003/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_004`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_004/Content/Data/DT_VendorData_Ext_MAGZ_004.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_004/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_005`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_005/Content/Data/DT_VendorData_Ext_MAGZ_005.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_005/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_006`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_006/Content/Data/DT_VendorData_Ext_MAGZ_006.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_006/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_008`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_008/Content/Data/DT_VendorData_Ext_MAGZ_008.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_008/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_011/Content/Data/DT_VendorData_Ext_MAGZ_011.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_012`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_012/Content/Data/DT_VendorData_Ext_MAGZ_012.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_012/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_024`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_024/Content/Data/DT_VendorData_Ext_MAGZ_024.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_024/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_026/Content/Data/DT_VendorData_Ext_MAGZ_026.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_026/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_034/Content/Data/DT_VendorData_Ext_MAGZ_034.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_034/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_043`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_043/Content/Data/DT_VendorData_Ext_MAGZ_043.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_043/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_046`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_046/Content/Data/DT_VendorData_Ext_MAGZ_046.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_046/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_051`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_051/Content/Data/DT_VendorData_Ext_MAGZ_051.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_051/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_052`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_052/Content/Data/DT_VendorData_Ext_MAGZ_052.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_052/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_053`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_053/Content/Data/DT_VendorData_Ext_MAGZ_053.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_053/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_054`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_054/Content/Data/DT_VendorData_Ext_MAGZ_054.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_054/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_055`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_055/Content/Data/DT_VendorData_Ext_MAGZ_055.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_055/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_056`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_056/Content/Data/DT_VendorData_Ext_MAGZ_056.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_056/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_057`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_057/Content/Data/DT_VendorData_Ext_MAGZ_057.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_057/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_059`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_059/Content/Data/DT_VendorData_Ext_MAGZ_059.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_059/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_060`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_060/Content/Data/DT_VendorData_Ext_MAGZ_060.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_060/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_061`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_061/Content/Data/DT_VendorData_Ext_MAGZ_061.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_061/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_062`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_062/Content/Data/DT_VendorData_Ext_MAGZ_062.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_062/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_063`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_063/Content/Data/DT_VendorData_Ext_MAGZ_063.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_063/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_064`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_064/Content/Data/DT_VendorData_Ext_MAGZ_064.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_064/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_065`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_065/Content/Data/DT_VendorData_Ext_MAGZ_065.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_065/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_066`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_066/Content/Data/DT_VendorData_Ext_MAGZ_066.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_066/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_067`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_067/Content/Data/DT_VendorData_Ext_MAGZ_067.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_067/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_068`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_068/Content/Data/DT_VendorData_Ext_MAGZ_068.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_068/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_069`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_069/Content/Data/DT_VendorData_Ext_MAGZ_069.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_069/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_070`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_070/Content/Data/DT_VendorData_Ext_MAGZ_070.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_070/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MAGZ_071`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_071/Content/Data/DT_VendorData_Ext_MAGZ_071.json) | 1 | `GF/Weapons/Attachments/Magazines/MAGZ_071/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_013/Content/Data/DT_VendorData_Ext_MUZL_013.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_014`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_014/Content/Data/DT_VendorData_Ext_MUZL_014.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_014/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_019`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_019/Content/Data/DT_VendorData_Ext_MUZL_019.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_019/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_020`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_020/Content/Data/DT_VendorData_Ext_MUZL_020.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_020/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_022`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_022/Content/Data/DT_VendorData_Ext_MUZL_022.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_022/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_023`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_023/Content/Data/DT_VendorData_Ext_MUZL_023.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_023/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_024`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_024/Content/Data/DT_VendorData_Ext_MUZL_024.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_024/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_025`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_025/Content/Data/DT_VendorData_Ext_MUZL_025.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_025/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_027/MUZL_027/Content/Data/DT_VendorData_Ext_MUZL_027.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_027/MUZL_027/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_028/Content/Data/DT_VendorData_Ext_MUZL_028.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_028/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_029/Content/Data/DT_VendorData_Ext_MUZL_029.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_029/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_030/Content/Data/DT_VendorData_Ext_MUZL_030.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_030/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_031/Content/Data/DT_VendorData_Ext_MUZL_031.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_031/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_032/Content/Data/DT_VendorData_Ext_MUZL_032.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_032/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_037`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_037/Content/Data/DT_VendorData_Ext_MUZL_037.json) | 2 | `GF/Weapons/Attachments/Muzzle/MUZL_037/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_038`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_038/Content/Data/DT_VendorData_Ext_MUZL_038.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_038/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_039`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_039/Content/Data/DT_VendorData_Ext_MUZL_039.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_039/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_040`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_040/Content/Data/DT_VendorData_Ext_MUZL_040.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_040/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_041`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_041/Content/Data/DT_VendorData_Ext_MUZL_041.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_041/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_044`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_044/Content/Data/DT_VendorData_Ext_MUZL_044.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_044/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_045`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_045/Content/Data/DT_VendorData_Ext_MUZL_045.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_045/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_046`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_046/Content/Data/DT_VendorData_Ext_MUZL_046.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_046/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_047`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_047/Content/Data/DT_VendorData_Ext_MUZL_047.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_047/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_048`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_048/Content/Data/DT_VendorData_Ext_MUZL_048.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_048/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_049`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_049/Content/Data/DT_VendorData_Ext_MUZL_049.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_049/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_050`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_050/Content/Data/DT_VendorData_Ext_MUZL_050.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_050/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_051`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_051/Content/Data/DT_VendorData_Ext_MUZL_051.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_051/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_052`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_052/Content/Data/DT_VendorData_Ext_MUZL_052.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_052/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_053`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_053/Content/Data/DT_VendorData_Ext_MUZL_053.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_053/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_054`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_054/Content/Data/DT_VendorData_Ext_MUZL_054.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_054/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_055`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_055/Content/Data/DT_VendorData_Ext_MUZL_055.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_055/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_056`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_056/Content/Data/DT_VendorData_Ext_MUZL_056.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_056/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_057`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_057/Content/Data/DT_VendorData_Ext_MUZL_057.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_057/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_058`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_058/Content/Data/DT_VendorData_Ext_MUZL_058.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_058/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_059`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_059/Content/Data/DT_VendorData_Ext_MUZL_059.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_059/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_060`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_060/Content/Data/DT_VendorData_Ext_MUZL_060.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_060/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_061`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_061/Content/Data/DT_VendorData_Ext_MUZL_061.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_061/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_062`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_062/Content/Data/DT_VendorData_Ext_MUZL_062.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_062/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_067`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_067/Content/Data/DT_VendorData_Ext_MUZL_067.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_067/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_068`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_068/Content/Data/DT_VendorData_Ext_MUZL_068.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_068/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_069`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_069/Content/Data/DT_VendorData_Ext_MUZL_069.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_069/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_070`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_070/Content/Data/DT_VendorData_Ext_MUZL_070.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_070/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_071`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_071/Content/Data/DT_VendorData_Ext_MUZL_071.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_071/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MUZL_072`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_072/Content/Data/DT_VendorData_Ext_MUZL_072.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_072/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_MedKit`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MedKit/Content/Data/DT_VendorData_Ext_MedKit.json) | 1 | `GF/Items/MedKit/Data` | not named |
| [`DT_VendorData_Ext_Molotov`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DT_VendorData_Ext_Molotov.json) | 1 | `GF/Items/Molotov/Data` | not named |
| [`DT_VendorData_Ext_Parachutes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Parachutes/Content/DT_VendorData_Ext_Parachutes.json) | 2 | `GF/Parachutes/Content` | [Wardogs_GameFeatures_Parachutes_v2](../game-features/Wardogs_GameFeatures_Parachutes_v2.md) |
| [`DT_VendorData_Ext_Pistol_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Pistols/Pistol_02/Content/Data/DT_VendorData_Ext_Pistol_02.json) | 1 | `GF/Weapons/Pistols/Pistol_02/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_RangeFinder`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/RangeFinder/Content/Data/DT_VendorData_Ext_RangeFinder.json) | 3 | `GF/Items/RangeFinder/Data` | not named |
| [`DT_VendorData_Ext_SGHT_009`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_009/Content/Data/DT_VendorData_Ext_SGHT_009.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_009/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_SGHT_023`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_023/Content/Data/DT_VendorData_Ext_SGHT_023.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_023/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_SmokeGrenade`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/SmokeGrenade/Content/Data/DT_VendorData_Ext_SmokeGrenade.json) | 8 | `GF/Items/SmokeGrenade/Data` | not named |
| [`DT_VendorData_Ext_StimPen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DT_VendorData_Ext_StimPen.json) | 1 | `GF/Items/StimPen/Data` | not named |
| [`DT_VendorData_Ext_VehicleRepairTool`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/VehicleRepairTool/Content/Data/DT_VendorData_Ext_VehicleRepairTool.json) | 3 | `GF/Items/VehicleRepairTool/Data` | not named |
| [`DT_VendorData_Ext_VehicleSmoke`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/VehicleSmoke/Content/Data/DT_VendorData_Ext_VehicleSmoke.json) | 1 | `GF/Vehicles/VehicleSmoke/Data` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_VendorData_Ext_WEPN_017`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_VendorData_Ext_WEPN_017.json) | 1 | `GF/Weapons/Platforms/WEPN_017/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_026/Content/Data/DT_VendorData_Ext_WEPN_026.json) | 1 | `GF/Weapons/Platforms/WEPN_026/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_027/Content/Data/DT_VendorData_Ext_WEPN_027.json) | 1 | `GF/Weapons/Platforms/WEPN_027/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_028/Content/Data/DT_VendorData_Ext_WEPN_028.json) | 1 | `GF/Weapons/Platforms/WEPN_028/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_029/Content/Data/DT_VendorData_Ext_WEPN_029.json) | 1 | `GF/Weapons/Platforms/WEPN_029/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_030/Content/Data/DT_VendorData_Ext_WEPN_030.json) | 1 | `GF/Weapons/Platforms/WEPN_030/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_035`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/Data/DT_VendorData_Ext_WEPN_035.json) | 1 | `GF/Weapons/Platforms/WEPN_035/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Ext_WEPN_036`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/Data/DT_VendorData_Ext_WEPN_036.json) | 1 | `GF/Weapons/Platforms/WEPN_036/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/DT_VendorData_Launcher_04.json) | 1 | `GF/Weapons/Launchers/Launcher_04/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_LMG_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/Data/DT_VendorData_Weapon_LMG_02.json) | 2 | `GF/Weapons/LMG/LMG_02/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_MK22`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/MK22/Content/Data/DT_VendorData_Weapon_MK22.json) | 2 | `GF/Weapons/Sniper/MK22/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_MP43`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Shotgun/MP43/Content/Data/DT_VendorData_Weapon_MP43.json) | 1 | `GF/Weapons/Shotgun/MP43/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_MP9`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_014/Content/Data/DT_VendorData_Weapon_MP9.json) | 1 | `GF/Weapons/Platforms/WEPN_014/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_Mosin`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/Data/DT_VendorData_Weapon_Mosin.json) | 1 | `GF/Weapons/Platforms/WEPN_017/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_RFB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/RFB/Content/Data/DT_VendorData_Weapon_RFB.json) | 1 | `GF/Weapons/DMR/RFB/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_RPG7`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/RPG7/Content/Data/DT_VendorData_Weapon_RPG7.json) | 1 | `GF/Weapons/Launchers/RPG7/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_SMG_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/SMG_03/Content/Data/DT_VendorData_Weapon_SMG_03.json) | 2 | `GF/Weapons/SMG/SMG_03/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_SR_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/SR_04/Content/Data/DT_VendorData_Weapon_SR_04.json) | 2 | `GF/Weapons/Sniper/SR_04/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_SV98`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_008/Content/Data/DT_VendorData_Weapon_SV98.json) | 2 | `GF/Weapons/Platforms/WEPN_008/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_SVDM`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/SVDM/Content/Data/DT_VendorData_Weapon_SVDM.json) | 2 | `GF/Weapons/DMR/SVDM/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_WEPN_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/Data/DT_VendorData_Weapon_WEPN_031.json) | 1 | `GF/Weapons/Platforms/WEPN_031/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_WEPN_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/Data/DT_VendorData_Weapon_WEPN_034.json) | 1 | `GF/Weapons/Platforms/WEPN_034/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_VendorData_Weapon_WEPN_037`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/Data/DT_VendorData_Weapon_WEPN_037.json) | 1 | `GF/Weapons/Platforms/WEPN_037/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment/DT_WeaponMarket.json) | 37 | `GameMechanics/WorldInteractable/NPCs/Vendor/VendorEquipment` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |
| [`DT_WeaponVendor_EXT_AR_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_003/Content/Data/DT_WeaponVendor_EXT_AR_03.json) | 1 | `GF/Weapons/Platforms/WEPN_003/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_EXT_AR_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_004/Content/Data/DT_WeaponVendor_EXT_AR_04.json) | 1 | `GF/Weapons/Platforms/WEPN_004/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_EXT_LMG_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_009/Content/Data/DT_WeaponVendor_EXT_LMG_01.json) | 1 | `GF/Weapons/Platforms/WEPN_009/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_EXT_Launcher_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_012/Content/Data/DT_WeaponVendor_EXT_Launcher_01.json) | 1 | `GF/Weapons/Platforms/WEPN_012/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_EXT_Launcher_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_013/Content/Data/DT_WeaponVendor_EXT_Launcher_02.json) | 1 | `GF/Weapons/Platforms/WEPN_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_EXT_SMG_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_006/Content/Data/DT_WeaponVendor_EXT_SMG_01.json) | 1 | `GF/Weapons/Platforms/WEPN_006/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_Ext_AR_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_001/Content/Data/DT_WeaponVendor_Ext_AR_01.json) | 1 | `GF/Weapons/Platforms/WEPN_001/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_MUZL_012`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_012/Content/Data/DT_WeaponVendor_MUZL_012.json) | 1 | `GF/Weapons/Attachments/Muzzle/MUZL_012/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_011`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_011/Content/Data/DT_WeaponVendor_SGHT_011.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_013`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_013/Content/Data/DT_WeaponVendor_SGHT_013.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_013/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_016`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_016/Content/Data/DT_WeaponVendor_SGHT_016.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_016/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_024`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_024/Content/Data/DT_WeaponVendor_SGHT_024.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_024/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_025`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_025/Content/Data/DT_WeaponVendor_SGHT_025.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_025/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_026/Content/Data/DT_WeaponVendor_SGHT_026.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_026/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_027/Content/Data/DT_WeaponVendor_SGHT_027.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_027/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_028/Content/Data/DT_WeaponVendor_SGHT_028.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_028/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_029/Content/Data/DT_WeaponVendor_SGHT_029.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_029/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_030/Content/Data/DT_WeaponVendor_SGHT_030.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_030/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_031/Content/Data/DT_WeaponVendor_SGHT_031.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_031/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_032/Content/Data/DT_WeaponVendor_SGHT_032.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_032/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_034/Content/Data/DT_WeaponVendor_SGHT_034.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_034/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_036`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_036/Content/Data/DT_WeaponVendor_SGHT_036.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_036/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_038`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_038/Content/Data/DT_WeaponVendor_SGHT_038.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_038/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_039`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_039/Content/Data/DT_WeaponVendor_SGHT_039.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_039/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendor_SGHT_040`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_040/Content/Data/DT_WeaponVendor_SGHT_040.json) | 1 | `GF/Weapons/Attachments/Sights/SGHT_040/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponVendore_EXT_Shotgun_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_011/Content/Data/DT_WeaponVendore_EXT_Shotgun_01.json) | 1 | `GF/Weapons/Platforms/WEPN_011/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponsVendor_EXT_Pistol_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_010/Content/Data/DT_WeaponsVendor_EXT_Pistol_01.json) | 1 | `GF/Weapons/Platforms/WEPN_010/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponsVendor_EXT_TAR21`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_005/Content/Data/DT_WeaponsVendor_EXT_TAR21.json) | 1 | `GF/Weapons/Platforms/WEPN_005/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponsVendor_EXT_WEPN_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_032/Content/Data/DT_WeaponsVendor_EXT_WEPN_032.json) | 1 | `GF/Weapons/Platforms/WEPN_032/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |
| [`DT_WeaponsVendor_EXT_WEPN_033`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_033/Content/Data/DT_WeaponsVendor_EXT_WEPN_033.json) | 1 | `GF/Weapons/Platforms/WEPN_033/Data` | [Wardogs_WeaponShop_v1](../game-features/Wardogs_WeaponShop_v1.md) |

#### WDRainSpotEntry

1 table(s), 304 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_RainSpots`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Environment/DT_RainSpots.json) | 304 | `Audio/Environment` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md) |

#### WDRewardFeedActionDataTableRow

10 table(s), 159 rows, 8 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdrewardfeedactiondatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ChallengesFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_ChallengesFeedActions.json) | 68 | `UI/Features/HUD/RewardFeed/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |
| [`DT_ChallengesFeedActions_Building`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengesFeedActions_Building.json) | 12 | `GF/Rewards/BuildableRewards/Rewards` | [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| [`DT_ChallengesFeedActions_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_ChallengesFeedActions_Crowbar.json) | 1 | `GF/Items/Crowbar/Rewards` | not named |
| [`DT_ChallengesFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_ChallengesFeedActions_Spotting.json) | 3 | `GF/Spotting/Data/UI/RewardFeed` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_ControlZoneRewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/RewardFeed/Data/DT_ControlZoneRewardFeedActions.json) | 12 | `GF/ControlZone/UI/RewardFeed/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |
| [`DT_RewardFeedActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_RewardFeedActions.json) | 52 | `UI/Features/HUD/RewardFeed/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_RewardFeedActions_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/RewardFeed/DT_RewardFeedActions_HotZoneMagnet.json) | 3 | `GF/WorldFeatures/HotZoneMagnet/Data/UI/RewardFeed` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_RewardFeedActions_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/RewardFeed/DT_RewardFeedActions_Spotting.json) | 3 | `GF/Spotting/Data/UI/RewardFeed` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_RewardFeedActions_TeamOffence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Data/UI/RewardFeed/DT_RewardFeedActions_TeamOffence.json) | 1 | `GF/TeamOffence/Data/UI/RewardFeed` | not named |
| [`DT_TippingReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Tipping/Data/DT_TippingReward.json) | 4 | `UI/Features/HUD/Tipping/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDMetaTreeNodeData_UI

1 table(s), 131 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetatreenodedata_ui).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CharacterSkillNodes_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_CharacterSkillNodes_Data.json) | 131 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDCustomRewardTableRow

16 table(s), 128 rows, 16 named in docs. Expanded on [Buildables](../game-features/Wardogs_Buildables_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Reward_Cash_BuildableBuilt`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable/DT_Reward_Cash_BuildableBuilt.json) | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_Reward_Cash_BuildablePlaced`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable/DT_Reward_Cash_BuildablePlaced.json) | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_Reward_Cash_BuildablePlacedInFOB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable/DT_Reward_Cash_BuildablePlacedInFOB.json) | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Buildable` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_Reward_Cash_ControlZoneReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective/DT_Reward_Cash_ControlZoneReward.json) | 12 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_DeployableDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable/DT_Reward_Cash_DeployableDestroyed.json) | 25 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_Reward_Cash_DeployedSupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable/DT_Reward_Cash_DeployedSupplyCrate.json) | 6 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Deployable` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_EndGameFactionReward`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective/DT_Reward_Cash_EndGameFactionReward.json) | 4 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Objective` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_Heal`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Heal/DT_Reward_Cash_Heal.json) | 8 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Heal` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet/DT_Reward_Cash_HotZoneMagnet.json) | 8 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_PlayerKill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/KillScore/DT_Reward_Cash_PlayerKill.json) | 3 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/KillScore` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [index](../index.md) |
| [`DT_Reward_Cash_Refuel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_Refuel.json) | 1 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_Repair`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_Repair.json) | 4 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_Revive`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Revive/DT_Reward_Cash_Revive.json) | 6 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Revive` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Rewards/DT_Reward_Cash_Spotting.json) | 4 | `GF/Spotting/Data/Rewards` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_Reward_Cash_VehicleDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_VehicleDestroyed.json) | 11 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Reward_Cash_VehicleTransport`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle/DT_Reward_Cash_VehicleTransport.json) | 3 | `GameMechanics/Gamemode/Data/CashRewardsDataTable/Vehicle` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |

#### WDUITaggedIconRow

8 table(s), 128 rows, 4 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CaliberModifiers_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_CaliberModifiers_TaggedIcons.json) | 6 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_Calibers_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_Calibers_TaggedIcons.json) | 34 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_DamageTypes_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_DamageTypes_TaggedIcons.json) | 3 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EventLog_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/DeathRecap/Widgets/HealthReport/Data/DT_EventLog_TaggedIcons.json) | 2 | `UI/Features/DeathRecap/Widgets/HealthReport/Data` | not named |
| [`DT_Ext_Caliber_TaggedIcons_Arrow`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/DataTable/DT_Ext_Caliber_TaggedIcons_Arrow.json) | 2 | `GF/Items/CombatBow/Data/DataTable` | not named |
| [`DT_Ext_FuelLocations_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/FuelCanister/Content/Data/DT_Ext_FuelLocations_TaggedIcons.json) | 1 | `GF/Items/FuelCanister/Data` | not named |
| [`DT_Ext_RepairLocations_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/VehicleRepairTool/Content/Data/UI/SpatialTrackers/DT_Ext_RepairLocations_TaggedIcons.json) | 17 | `GF/Items/VehicleRepairTool/Data/UI/SpatialTrackers` | not named |
| [`DT_TaggedIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_TaggedIcons.json) | 63 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIFlairBasicPaintType

2 table(s), 120 rows, 2 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Itemsmith_Flair_BasicPaint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_BasicPaint.json) | 60 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| [`DT_Itemsmith_Flair_CamoBasicPaint`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_CamoBasicPaint.json) | 60 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |

#### WDImpulseResonanceEntry

1 table(s), 116 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ImpulseResonance`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Environment/DT_ImpulseResonance.json) | 116 | `Audio/Environment` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md) |

#### WDLoadingScreenTips

1 table(s), 110 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdloadingscreentips).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_LoadingScreenTips`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/LoadingScreen/Data/DT_LoadingScreenTips.json) | 110 | `UI/Features/Frontend/LoadingScreen/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDChallengeDefinition

9 table(s), 108 rows, 9 named in docs. Expanded on [Challenges](../game-features/Wardogs_Challenges_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Challenges_SessionEvents_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_Challenges_SessionEvents_Buildables.json) | 11 | `GF/Rewards/BuildableRewards/Rewards` | [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| [`DT_Challenges_SessionEvents_Crowbar`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Rewards/DT_Challenges_SessionEvents_Crowbar.json) | 1 | `GF/Items/Crowbar/Rewards` | [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |
| [`DT_Challenges_SessionEvents_KOTH`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Challenges_KOTH/Content/DT_Challenges_SessionEvents_KOTH.json) | 60 | `GF/Challenges_KOTH/Content` | [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Challenges_KOTH_v2](../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md) |
| [`DT_Challenges_SessionEvents_KOTH_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_HotZoneMagnet.json) | 3 | `GF/WorldFeatures/HotZoneMagnet/Data/Challenges` | [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_Challenges_SessionEvents_KOTH_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Challenges/DT_Challenges_SessionEvents_KOTH_Spotting.json) | 2 | `GF/Spotting/Data/Challenges` | [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md), [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_Challenges_SessionEvents_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/DT_Challenges_SessionEvents_Shared.json) | 10 | `Meta/Challenges` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_RewardLookup_SessionEvents_v1](../content/Wardogs_RewardLookup_SessionEvents_v1.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |
| [`DT_Challenges_SessionEvents_TeamOffence`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/TeamOffence/Content/Challenges/DT_Challenges_SessionEvents_TeamOffence.json) | 2 | `GF/TeamOffence/Challenges` | [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |
| [`DT_PassiveMissionChallenges`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissionChallenges.json) | 15 | `Meta/Missions` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |
| [`DT_WagerChallenges`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerChallenges.json) | 4 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |

#### WDUIInteractionContextDataTableRow

7 table(s), 98 rows, 5 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InteractionContextData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Interaction/DT_InteractionContextData.json) | 86 | `UI/Data/Interaction` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_InteractionContextData_ForceOpenDoor`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Crowbar/Content/Data/Interaction/DT_InteractionContextData_ForceOpenDoor.json) | 1 | `GF/Items/Crowbar/Data/Interaction` | not named |
| [`DT_InteractionContextData_ForwardOperatingBase`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/ForwardOperatingBase/DT_InteractionContextData_ForwardOperatingBase.json) | 4 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_InteractionContextData_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/DT_InteractionContextData_HotZoneMagnet.json) | 3 | `GF/WorldFeatures/HotZoneMagnet/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_InteractionContextData_Lockpicking`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/Lockpicking/Content/Data/Interaction/DT_InteractionContextData_Lockpicking.json) | 1 | `GF/Vehicles/Lockpicking/Data/Interaction` | not named |
| [`DT_InteractionContextData_Lootable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_InteractionContextData_Lootable.json) | 2 | `GF/WorldFeatures/Lootable/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_InteractionContextData_StrikeDisarm_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/StrikeDisarm_01/Content/DT_InteractionContextData_StrikeDisarm_01.json) | 1 | `GF/PvE/Scenarios/StrikeDisarm_01/Content` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |

#### WDRewardTableRow

2 table(s), 81 rows, 2 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdrewardtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Rewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_Rewards.json) | 78 | `GameMechanics/Gamemode/Data` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |
| [`DT_Rewards_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/DT_Rewards_Spotting.json) | 3 | `GF/Spotting/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |

#### WDVoxBase

1 table(s), 81 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_VoxData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Vox/General/DT_VoxData.json) | 81 | `Audio/Vox/General` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md), [SDK](../docs/gap_resolution/SDK.md) |

#### WDUITrackerDataTableRow

20 table(s), 75 rows, 14 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Editor_TrackerData_ControlZoneRegions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZoneRegions/Content/Data/DT_Editor_TrackerData_ControlZoneRegions.json) | 1 | `GF/ControlZoneRegions/Data` | [Wardogs_GameFeatures_ControlZoneRegions_v2](../game-features/Wardogs_GameFeatures_ControlZoneRegions_v2.md) |
| [`DT_Editor_TrackerData_WorldDisplay`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Tools/WorldDisplay/Data/DT_Editor_TrackerData_WorldDisplay.json) | 4 | `UI/Tools/WorldDisplay/Data` | not named |
| [`DT_TrackerData_Map_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/DT_TrackerData_Map_Buildables.json) | 4 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_TrackerData_Map_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/MapTrackers/Data/DT_TrackerData_Map_ControlZone.json) | 1 | `GF/ControlZone/UI/Trackers/MapTrackers/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |
| [`DT_TrackerData_Map_HotPotato`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/HotPotato/Content/Data/UI/DT_TrackerData_Map_HotPotato.json) | 1 | `GF/HotPotato/Data/UI` | not named |
| [`DT_TrackerData_Map_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DT_TrackerData_Map_HotZoneMagnet.json) | 2 | `GF/WorldFeatures/HotZoneMagnet/Data/UI/MapTrackers` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_TrackerData_Map_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Map_Scenario.json) | 2 | `GF/PvE/Scenarios/BaseScenario/UI/Trackers` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| [`DT_TrackerData_Map_SmokeGrenade`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/SmokeGrenade/Content/UI/Trackers/MapTrackers/Data/DT_TrackerData_Map_SmokeGrenade.json) | 1 | `GF/Items/SmokeGrenade/UI/Trackers/MapTrackers/Data` | not named |
| [`DT_TrackerData_Map_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_TrackerData_Map_SniperShowdown.json) | 3 | `GF/Experiences/SniperShowdown/UI` | [Wardogs_GameFeatures_Experiences_v2](../game-features/Wardogs_GameFeatures_Experiences_v2.md) |
| [`DT_TrackerData_Map_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Map/Data/DT_TrackerData_Map_Spotting.json) | 1 | `GF/Spotting/Data/UI/Tracker/Map/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_TrackerData_Minimap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Minimap/Widgets/Trackers/Data/DT_TrackerData_Minimap.json) | 17 | `UI/Features/HUD/Minimap/Widgets/Trackers/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_GameFeatures_Deathmatch_v2](../game-features/Wardogs_GameFeatures_Deathmatch_v2.md), [Wardogs_GameFeatures_ShootingRange_v2](../game-features/Wardogs_GameFeatures_ShootingRange_v2.md) |
| [`DT_TrackerData_Minimap_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Minimap_Scenario.json) | 2 | `GF/PvE/Scenarios/BaseScenario/UI/Trackers` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| [`DT_TrackerData_Minimap_SmokeGrenade`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/SmokeGrenade/Content/UI/Trackers/MapTrackers/Data/DT_TrackerData_Minimap_SmokeGrenade.json) | 1 | `GF/Items/SmokeGrenade/UI/Trackers/MapTrackers/Data` | not named |
| [`DT_TrackerData_Spatial`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data/DT_TrackerData_Spatial.json) | 13 | `UI/Features/HUD/SpatialTrackers/Widgets/Trackers/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_TrackerData_Spatial_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/DT_TrackerData_Spatial_Buildables.json) | 1 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_TrackerData_Spatial_Scenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/Trackers/DT_TrackerData_Spatial_Scenario.json) | 1 | `GF/PvE/Scenarios/BaseScenario/UI/Trackers` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| [`DT_TrackerData_Spatial_SmokeGrenade`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/SmokeGrenade/Content/UI/Trackers/SpatialTrackers/Data/DT_TrackerData_Spatial_SmokeGrenade.json) | 1 | `GF/Items/SmokeGrenade/UI/Trackers/SpatialTrackers/Data` | not named |
| [`DT_TrackerData_Spatial_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Spatial/Data/DT_TrackerData_Spatial_Spotting.json) | 1 | `GF/Spotting/Data/UI/Tracker/Spatial/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_TrackerData_TacticalMap`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Widgets/Trackers/Data/DT_TrackerData_TacticalMap.json) | 17 | `UI/Features/Map/Widgets/Trackers/Data` | not named |
| [`DT_Trackers_ControlZone_Spatial`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/Trackers/SpatialTrackers/Data/DT_Trackers_ControlZone_Spatial.json) | 1 | `GF/ControlZone/UI/Trackers/SpatialTrackers/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |

#### WDSceneDataTableRow

14 table(s), 68 rows, 12 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdscenedatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_DeathmatchSceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/UI/Scene/DT_DeathmatchSceneData_Match.json) | 1 | `GF/Deathmatch/UI/Scene` | [round8-loadout-deathmatch](../docs/evidence/round8-loadout-deathmatch.md), [Wardogs_GameFeatures_Deathmatch_v2](../game-features/Wardogs_GameFeatures_Deathmatch_v2.md) |
| [`DT_SceneData_DefaultPvEScenario`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/UI/DT_SceneData_DefaultPvEScenario.json) | 1 | `GF/PvE/Scenarios/BaseScenario/UI` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |
| [`DT_SceneData_Frontend`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Frontend.json) | 28 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_SceneData_Frontend_Gunsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_SceneData_Frontend_Gunsmith.json) | 1 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_SceneData_Frontend_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_SceneData_Frontend_Itemsmith.json) | 1 | `GF/Itemsmith/UI/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |
| [`DT_SceneData_Frontend_Vehiclesmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_SceneData_Frontend_Vehiclesmith.json) | 1 | `GF/Vehiclesmith/Data` | [Wardogs_GameFeatures_Vehiclesmith_v2](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) |
| [`DT_SceneData_Match`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match.json) | 25 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_SceneData_Match_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/FobRefuelRepair/DT_SceneData_Match_Buildables.json) | 1 | `GF/Items/Buildables/Data/UI/FobRefuelRepair` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_SceneData_Match_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/Data/UI/DT_SceneData_Match_STN_05.json) | 1 | `GF/Vehicles/STN_05/Data/UI` | not named |
| [`DT_SceneData_Match_ShootingRange`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_ShootingRange.json) | 1 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md), [Wardogs_GameFeatures_ShootingRangeTutorial_v2](../game-features/Wardogs_GameFeatures_ShootingRangeTutorial_v2.md), [Wardogs_GameFeatures_ShootingRange_v2](../game-features/Wardogs_GameFeatures_ShootingRange_v2.md) |
| [`DT_SceneData_Match_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_SceneData_Match_SniperShowdown.json) | 1 | `GF/Experiences/SniperShowdown/UI` | [Wardogs_GameFeatures_Experiences_v2](../game-features/Wardogs_GameFeatures_Experiences_v2.md) |
| [`DT_SceneData_Match_SupplyCrates`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/UI/Data/DT_SceneData_Match_SupplyCrates.json) | 1 | `GF/Vehicles/SupplyCrates/UI/Data` | not named |
| [`DT_SceneData_Match_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Match_Wagers.json) | 1 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_SceneData_Shared`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Scenes/DT_SceneData_Shared.json) | 4 | `UI/Data/Scenes` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDMetaSkillEffectsTaggedTableRow

10 table(s), 62 rows, 2 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_DriverSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_DriverSkills.json) | 6 | `Meta/CharacterSkills` | not named |
| [`DT_InfantrySkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_InfantrySkills.json) | 17 | `Meta/CharacterSkills` | not named |
| [`DT_MedicSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MedicSkills.json) | 4 | `Meta/CharacterSkills` | not named |
| [`DT_PilotSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_PilotSkills.json) | 6 | `Meta/CharacterSkills` | not named |
| [`DT_ReconSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_ReconSkills.json) | 13 | `Meta/CharacterSkills` | not named |
| [`DT_Skills_C4`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/C4/Content/Data/Skills/DT_Skills_C4.json) | 1 | `GF/Items/C4/Data/Skills` | not named |
| [`DT_Skills_Lockpicking`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/Lockpicking/Content/Data/Skills/DT_Skills_Lockpicking.json) | 1 | `GF/Vehicles/Lockpicking/Data/Skills` | [Wardogs_GameplayEffectsPipeline_v1](../pipelines/Wardogs_GameplayEffectsPipeline_v1.md) |
| [`DT_Skills_PrototypeMaskedScopes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/PrototypeMaskedScopes/Content/Data/Skills/DT_Skills_PrototypeMaskedScopes.json) | 1 | `GF/Items/PrototypeMaskedScopes/Data/Skills` | not named |
| [`DT_Skills_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/Skills/DT_Skills_Spotting.json) | 2 | `GF/Spotting/Data/Skills` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |
| [`DT_SupportSkills`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_SupportSkills.json) | 11 | `Meta/CharacterSkills` | not named |

#### WDDamageableEntityTableRow

26 table(s), 54 rows, 24 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_GlobalDamage_ArmorData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_ArmorData.json) | 4 | `GameMechanics/DamageSystem/DamageDataTables` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [round8-armor](../docs/evidence/round8-armor.md), [Wardogs_GameFeatures_Ammo_v2](../game-features/Wardogs_GameFeatures_Ammo_v2.md) (+1) |
| [`DT_GlobalDamage_BuildableData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/DT_GlobalDamage_BuildableData.json) | 20 | `GF/Items/Buildables/Data` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md), [Wardogs_GameFeatures_Items_v2](../game-features/Wardogs_GameFeatures_Items_v2.md) |
| [`DT_GlobalDamage_InfantryData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json) | 1 | `GameMechanics/DamageSystem/DamageDataTables` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [damage](../docs/evidence/damage.md) (+2) |
| [`DT_GlobalDamage_SupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SupplyCrates/Content/DataTables/DT_GlobalDamage_SupplyCrate.json) | 5 | `GF/Vehicles/SupplyCrates/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_VehicleData.json) | 1 | `GameMechanics/DamageSystem/DamageDataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_DamagePipeline_v2](../pipelines/Wardogs_DamagePipeline_v2.md), [Wardogs_VehicleDamagePipeline_v1](../pipelines/Wardogs_VehicleDamagePipeline_v1.md) |
| [`DT_GlobalDamage_VehicleData_ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_02.json) | 1 | `GF/Vehicles/ROT_02/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_03.json) | 1 | `GF/Vehicles/ROT_03/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/DataTables/DT_GlobalDamage_VehicleData_ROT_04.json) | 1 | `GF/Vehicles/ROT_04/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_SPW_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/DataTables/DT_GlobalDamage_VehicleData_SPW_01.json) | 1 | `GF/Vehicles/SPW_01/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_STN_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/DataTables/DT_GlobalDamage_VehicleData_STN_01.json) | 1 | `GF/Vehicles/STN_01/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/DataTables/DT_GlobalDamage_VehicleData_STN_02.json) | 1 | `GF/Vehicles/STN_02/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/DataTable/DT_GlobalDamage_VehicleData_STN_03.json) | 1 | `GF/Vehicles/STN_03/DataTable` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/DataTables/DT_GlobalDamage_VehicleData_STN_04.json) | 1 | `GF/Vehicles/STN_04/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/DataTable/DT_GlobalDamage_VehicleData_STN_05.json) | 1 | `GF/Vehicles/STN_05/DataTable` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_GlobalDamage_VehicleData_STN_06.json) | 1 | `GF/Vehicles/STN_06/DataTables` | not named |
| [`DT_GlobalDamage_VehicleData_TNK_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/DataTables/DT_GlobalDamage_VehicleData_TNK_01.json) | 3 | `GF/Vehicles/TNK_01/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_GlobalDamage_VehicleData_TNK_04.json) | 1 | `GF/Vehicles/TNK_04/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md), [Wardogs_VehicleDamagePipeline_v1](../pipelines/Wardogs_VehicleDamagePipeline_v1.md) |
| [`DT_GlobalDamage_VehicleData_WHL_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_01/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_01.json) | 1 | `GF/Vehicles/WHL_01/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_WHL_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_02/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_02.json) | 1 | `GF/Vehicles/WHL_02/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_WHL_05_Humvee`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_Humvee.json) | 1 | `GF/Vehicles/WHL_05/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_WHL_05_Minigun`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_Minigun/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_Minigun.json) | 1 | `GF/Vehicles/WHL_05_Minigun/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_WHL_05_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_05_RingTurret/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_05_RingTurret.json) | 1 | `GF/Vehicles/WHL_05_RingTurret/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md) |
| [`DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_06/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_06_DuneBuggy.json) | 1 | `GF/Vehicles/WHL_06/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_WHL_07_Ural`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_07_Ural.json) | 1 | `GF/Vehicles/WHL_07/DataTables` | [Wardogs_AllVehicles_Stats_Damage_v1](../content/Wardogs_AllVehicles_Stats_Damage_v1.md), [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_WHL_08`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_08.json) | 1 | `GF/Vehicles/WHL_08/DataTables` | [Wardogs_GameFeatures_Vehicles_v2](../game-features/Wardogs_GameFeatures_Vehicles_v2.md) |
| [`DT_GlobalDamage_VehicleData_WHL_08_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/DataTables/DT_GlobalDamage_VehicleData_WHL_08_RingTurret.json) | 1 | `GF/Vehicles/WHL_08_RingTurret/DataTables` | not named |

#### WDLootableDataTable

2 table(s), 54 rows, 2 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdlootabledatatable).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_LootableDataTable`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/Lootable/Content/Data/DT_LootableDataTable.json) | 52 | `GF/WorldFeatures/Lootable/Data` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_LootableDataTable_VIPEscort_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/VIPEscort_01/Content/DT_LootableDataTable_VIPEscort_01.json) | 2 | `GF/PvE/Scenarios/VIPEscort_01/Content` | [Wardogs_GameFeatures_PvE_v2](../game-features/Wardogs_GameFeatures_PvE_v2.md) |

#### WDWagerConditionDefinition

1 table(s), 50 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwagerconditiondefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_WagerConditions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerConditions.json) | 50 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDResourceRewardTableRow

1 table(s), 49 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdresourcerewardtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewards.json) | 49 | `GameMechanics/Gamemode/Data` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDUIRadialWheelSlotTypeTableRow

10 table(s), 46 rows, 6 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_RadialWheelSlotType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/BuildTool/DT_RadialWheelSlotType_BuildToolData.json) | 22 | `GF/Items/Buildables/Data/BuildTool` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_RadialWheelSlotType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/BuildableData/DT_RadialWheelSlotType_BuildToolData.json) | 1 | `GF/Vehicles/STN_01/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_RadialWheelSlotType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DT_RadialWheelSlotType_BuildToolData.json) | 1 | `GF/Vehicles/STN_06/BuildableData` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_RadialWheelSlotType_BuildToolData_STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/BuildableData/DT_RadialWheelSlotType_BuildToolData_STN_04.json) | 1 | `GF/Vehicles/STN_04/BuildableData` | not named |
| [`DT_RadialWheelSlotType_EquipmentData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/EquipmentWheel/DT_RadialWheelSlotType_EquipmentData.json) | 7 | `UI/Features/RadialWheel/Data/EquipmentWheel` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_RadialWheelSlotType_Vehicles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/Vehicles/DT_RadialWheelSlotType_Vehicles.json) | 9 | `UI/Features/RadialWheel/Data/Vehicles` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_RadialWheelSlotType_VoiceChatData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/VoiceChat/DT_RadialWheelSlotType_VoiceChatData.json) | 2 | `UI/Features/RadialWheel/Data/VoiceChat` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_STN_02_RadialWheelSlotType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/BuildableData/DT_STN_02_RadialWheelSlotType_BuildToolData.json) | 1 | `GF/Vehicles/STN_02/BuildableData` | not named |
| [`DT_STN_03_RadialWheelSlotType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/BuildableData/DT_STN_03_RadialWheelSlotType_BuildToolData.json) | 1 | `GF/Vehicles/STN_03/BuildableData` | not named |
| [`DT_STN_05_RadialWheelSlotType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/BuildableData/DT_STN_05_RadialWheelSlotType_BuildToolData.json) | 1 | `GF/Vehicles/STN_05/BuildableData` | not named |

#### WDBuildableDataTableRow

9 table(s), 44 rows, 3 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Buildables_LargeHammer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/LargeHammer/DT_Buildables_LargeHammer.json) | 19 | `GF/Items/Buildables/Data/LargeHammer` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_Buildables_MediumHammer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/MediumHammer/DT_Buildables_MediumHammer.json) | 12 | `GF/Items/Buildables/Data/MediumHammer` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_Buildables_STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/BuildableData/DT_Buildables_STN_04.json) | 1 | `GF/Vehicles/STN_04/BuildableData` | not named |
| [`DT_Buildables_STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/BuildableData/DT_Buildables_STN_06.json) | 1 | `GF/Vehicles/STN_06/BuildableData` | not named |
| [`DT_Buildables_SmallHammer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/SmallHammer/DT_Buildables_SmallHammer.json) | 7 | `GF/Items/Buildables/Data/SmallHammer` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_STN_01_Buildable_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/Data/DT_STN_01_Buildable_Data.json) | 1 | `GF/Vehicles/STN_01/Data` | not named |
| [`DT_STN_02_Buildable_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/BuildableData/DT_STN_02_Buildable_Data.json) | 1 | `GF/Vehicles/STN_02/BuildableData` | not named |
| [`DT_STN_03_Buildable_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/BuildableData/DT_STN_03_Buildable_Data.json) | 1 | `GF/Vehicles/STN_03/BuildableData` | not named |
| [`DT_STN_05_Buildable_Data`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/BuildableData/DT_STN_05_Buildable_Data.json) | 1 | `GF/Vehicles/STN_05/BuildableData` | not named |

#### WDUITooltipDataTableRow

4 table(s), 39 rows, 4 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_TooltipData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Tooltips/Data/DT_TooltipData.json) | 34 | `UI/Features/Tooltips/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_TooltipData_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/Tooltips/DT_TooltipData_Buildables.json) | 1 | `GF/Items/Buildables/Data/UI/Tooltips` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_TooltipData_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/UI/MapTrackers/DT_TooltipData_HotZoneMagnet.json) | 2 | `GF/WorldFeatures/HotZoneMagnet/Data/UI/MapTrackers` | [Wardogs_GameFeatures_WorldFeatures_v2](../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md) |
| [`DT_TooltipData_Wagers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_TooltipData_Wagers.json) | 2 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDEventFeedActionDataTableRow

2 table(s), 37 rows, 2 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdeventfeedactiondatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_EventFeedTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Data/DT_EventFeedTypes.json) | 34 | `UI/Features/HUD/EventFeed/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_EventFeedTypes_SniperShowdown`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Experiences/SniperShowdown/Content/UI/DT_EventFeedTypes_SniperShowdown.json) | 3 | `GF/Experiences/SniperShowdown/UI` | [Wardogs_GameFeatures_Experiences_v2](../game-features/Wardogs_GameFeatures_Experiences_v2.md) |

#### WDCosmeticData

10 table(s), 36 rows, 5 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Bobblehead_Faction_Cosmetics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Faction/Content/Data/DT_Bobblehead_Faction_Cosmetics.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Faction/Data` | not named |
| [`DT_Bobblehead_Grenade_Cosmetics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Grenade/Content/Data/DT_Bobblehead_Grenade_Cosmetics.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Grenade/Data` | not named |
| [`DT_Bobblehead_HeavyHelmet_Cosmetics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_HeavyHelmet/Content/Data/DT_Bobblehead_HeavyHelmet_Cosmetics.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_HeavyHelmet/Data` | not named |
| [`DT_Bobblehead_Warpup_Cosmetics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Warpup/Content/Data/DT_Bobblehead_Warpup_Cosmetics.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Warpup/Data` | not named |
| [`DT_Cosmetics_Debug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Cosmetics/DT_Cosmetics_Debug.json) | 0 | `Meta/Cosmetics` | not named |
| [`DT_Cosmetics_FactionLogo`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/FactionLogo_SkinsData/Content/Data/DT_Cosmetics_FactionLogo.json) | 3 | `GF/Skins/FactionLogo_SkinsData/Data` | [Wardogs_GameFeatures_Skins_v2](../game-features/Wardogs_GameFeatures_Skins_v2.md) |
| [`DT_Cosmetics_Season01_Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Data/DT_Cosmetics_Season01_Emotes.json) | 3 | `GF/Emotes/Season01_EmotesData/Data` | [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md), [Wardogs_TreeRewardTrack_PlatformMastery_v1](../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md), [Wardogs_GameFeatures_Emotes_v2](../game-features/Wardogs_GameFeatures_Emotes_v2.md) |
| [`DT_Cosmetics_Season01_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/DT_Cosmetics_Season01_Skins.json) | 17 | `GF/Skins/Season01_SkinsData/Data` | [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md), [Wardogs_TreeRewardTrack_PlatformMastery_v1](../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md), [Wardogs_GameFeatures_Skins_v2](../game-features/Wardogs_GameFeatures_Skins_v2.md) |
| [`DT_Cosmetics_Season02_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Data/DT_Cosmetics_Season02_Skins.json) | 8 | `GF/Skins/Season02_SkinsData/Data` | [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md), [Wardogs_GameFeatures_Skins_v2](../game-features/Wardogs_GameFeatures_Skins_v2.md) |
| [`DT_Cosmetics_Taxi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/DT_Cosmetics_Taxi.json) | 1 | `GF/Taxi_SkinsData/Data` | [Wardogs_GameFeatures_Taxi_SkinsData_v2](../game-features/Wardogs_GameFeatures_Taxi_SkinsData_v2.md) |

#### RichImageRow

5 table(s), 35 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CustomEmojis`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DT_CustomEmojis.json) | 3 | `UI/Features/HUD/Chatbox/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_MapImageStyle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Widgets/TacticalMap/Data/DT_MapImageStyle.json) | 20 | `UI/Features/Map/Widgets/TacticalMap/Data` | not named |
| [`DT_RichImg_Style_EventLog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/DeathRecap/Widgets/Log/Data/DT_RichImg_Style_EventLog.json) | 2 | `UI/Features/DeathRecap/Widgets/Log/Data` | not named |
| [`DT_RichTextImg_FactionIcon`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Shared/RichTextDecorator/DT_RichTextImg_FactionIcon.json) | 3 | `UI/Shared/RichTextDecorator` | not named |
| [`DT_TooltipEmojis`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Tooltips/Widgets/TooltipItems/Data/DT_TooltipEmojis.json) | 7 | `UI/Features/Tooltips/Widgets/TooltipItems/Data` | not named |

#### WDUIPingAction

5 table(s), 35 rows, 4 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_PingActions_Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Emote/DT_PingActions_Emotes.json) | 10 | `UI/Features/PingWheel/Data/Actions/Emote` | not named |
| [`DT_PingActions_Orders`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Orders/DT_PingActions_Orders.json) | 5 | `UI/Features/PingWheel/Data/Actions/Orders` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_PingActions_Request`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Requests/DT_PingActions_Request.json) | 10 | `UI/Features/PingWheel/Data/Actions/Requests` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_PingActions_Social`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Social/DT_PingActions_Social.json) | 5 | `UI/Features/PingWheel/Data/Actions/Social` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_PingActions_Squad`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/PingWheel/Data/Actions/Squad/DT_PingActions_Squad.json) | 5 | `UI/Features/PingWheel/Data/Actions/Squad` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### FVehiclePropEntry

1 table(s), 29 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#fvehiclepropentry).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_VehiclePropList`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Blueprints/VehiclePropTooling/DT_VehiclePropList.json) | 29 | `Environment/Blueprints/VehiclePropTooling` | [Wardogs_Environment_v2](../content/Wardogs_Environment_v2.md), [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [SDK](../docs/gap_resolution/SDK.md) |

#### WDEmoteData

1 table(s), 27 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdemotedata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_EmoteData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Actions/Character/DT_EmoteData.json) | 27 | `GameMechanics/Actions/Character` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [Wardogs_ItemActions_v1](../content/Wardogs_ItemActions_v1.md) |

#### WDGoldMarketItemTableRow

1 table(s), 27 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdgoldmarketitemtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_GoldMarket`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Collection/DT_GoldMarket.json) | 27 | `Meta/Collection` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDBoneDamageModifierData

1 table(s), 20 rows, 1 named in docs. Expanded on [All Vehicles Stats and Damage](../content/Wardogs_AllVehicles_Stats_Damage_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InfantryData_BoneDamageModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_BoneDamageModifiers.json) | 20 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [damage](../docs/evidence/damage.md), [Wardogs_GameFeatures_Ammo_v2](../game-features/Wardogs_GameFeatures_Ammo_v2.md) (+1) |

#### WDDeathmatchWeaponData

1 table(s), 20 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wddeathmatchweapondata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_DeathmatchWeaponSelect`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DT_DeathmatchWeaponSelect.json) | 20 | `GF/Deathmatch/Data` | [ROUND8_STATUS](../docs/ROUND8_STATUS.md), [round8-loadout-deathmatch](../docs/evidence/round8-loadout-deathmatch.md), [round8-loadout-initialization](../docs/evidence/round8-loadout-initialization.md) (+1) |

#### WDUIActionSoundTableRow

1 table(s), 20 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_UIAudioData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Audio/DT_UIAudioData.json) | 20 | `UI/Data/Audio` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDExperienceServerBrowserTagRow

1 table(s), 19 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdexperienceserverbrowsertagrow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ExperienceServerBrowserTags`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/ServerBrowser/DT_ExperienceServerBrowserTags.json) | 19 | `UI/Data/ServerBrowser` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIMaterialTrackerDataTableRow

3 table(s), 19 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_MaterialTrackerSettingsData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Trackers/DT_MaterialTrackerSettingsData.json) | 15 | `UI/Data/Trackers` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_MaterialTrackerSettingsData_Buildables`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/DT_MaterialTrackerSettingsData_Buildables.json) | 3 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_MaterialTrackerSettingsData_Spotting`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Spotting/Content/Data/UI/Tracker/Optimization/Data/DT_MaterialTrackerSettingsData_Spotting.json) | 1 | `GF/Spotting/Data/UI/Tracker/Optimization/Data` | [Wardogs_GameFeatures_Spotting_v2](../game-features/Wardogs_GameFeatures_Spotting_v2.md) |

#### WDLiveCurveTableRow

10 table(s), 18 rows, 3 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Challenges_Curves_BuildableDestroyedAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/CurveTables/DT_Challenges_Curves_BuildableDestroyedAssist.json) | 1 | `GF/Rewards/BuildableRewards/Rewards/CurveTables` | [Wardogs_GameFeatures_Rewards_v2](../game-features/Wardogs_GameFeatures_Rewards_v2.md) |
| [`DT_Challenges_Curves_DestroyVehicle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_DestroyVehicle.json) | 1 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Challenges_Curves_DestroyVehicleAssist`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_DestroyVehicleAssist.json) | 1 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Challenges_Curves_EndOfMatch`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_EndOfMatch.json) | 2 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Challenges_Curves_HealPlayer`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_HealPlayer.json) | 2 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Challenges_Curves_PlayerDelivered`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_PlayerDelivered.json) | 1 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Challenges_Curves_PlayerKill`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_PlayerKill.json) | 3 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Challenges_Curves_PurchaseFromSupplyCrate`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_PurchaseFromSupplyCrate.json) | 3 | `Meta/Challenges/RewardData/CurveTables` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md) |
| [`DT_Challenges_Curves_VehicleAirborne`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/RewardData/CurveTables/DT_Challenges_Curves_VehicleAirborne.json) | 1 | `Meta/Challenges/RewardData/CurveTables` | not named |
| [`DT_Meta_RewardScalingCurves`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Rewards/DT_Meta_RewardScalingCurves.json) | 3 | `Meta/Rewards` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDUIPopupTypeDataTableRow

3 table(s), 18 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_PopupTypes_Features`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Data/DT_PopupTypes_Features.json) | 14 | `UI/Features/Popups/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_PopupTypes_Generic`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Data/DT_PopupTypes_Generic.json) | 3 | `UI/Features/Popups/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_PopupTypes_Itemsmith`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Data/DT_PopupTypes_Itemsmith.json) | 1 | `GF/Itemsmith/UI/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |

#### WDUITaggedWidgetParamsRow

3 table(s), 18 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_LootedComponentTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Inventory_2_0/Widgets/InventoryComponent/Data/DT_LootedComponentTypes.json) | 4 | `UI/Features/Inventory_2_0/Widgets/InventoryComponent/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |
| [`DT_LootedComponentTypes_FOB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/UI/DT_LootedComponentTypes_FOB.json) | 1 | `GF/Items/Buildables/Data/UI` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_SettingTypeUIData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Widgets/SettingValue/Data/DT_SettingTypeUIData.json) | 13 | `UI/Features/Settings/Widgets/SettingValue/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIScopeReticleType

1 table(s), 17 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ScopeReticleTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/ScopeReticle/Data/DT_ScopeReticleTypes.json) | 17 | `UI/Features/HUD/ScopeReticle/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### RichTextStyleRow

10 table(s), 15 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_MapTextStyle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Map/Widgets/TacticalMap/Data/DT_MapTextStyle.json) | 1 | `UI/Features/Map/Widgets/TacticalMap/Data` | not named |
| [`DT_RichText_StyleRows_CustomEmojis`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DT_RichText_StyleRows_CustomEmojis.json) | 1 | `UI/Features/HUD/Chatbox/Data` | not named |
| [`DT_RichText_StyleRows_CustomEmojisInHighlighted`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Chatbox/Data/DT_RichText_StyleRows_CustomEmojisInHighlighted.json) | 1 | `UI/Features/HUD/Chatbox/Data` | not named |
| [`DT_RichText_StyleRows_TooltipEmojis`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Tooltips/Widgets/TooltipItems/Data/DT_RichText_StyleRows_TooltipEmojis.json) | 1 | `UI/Features/Tooltips/Widgets/TooltipItems/Data` | not named |
| [`DT_RichText_StyleRows_TooltipEmojis_Small`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Tooltips/Widgets/TooltipItems/Data/DT_RichText_StyleRows_TooltipEmojis_Small.json) | 1 | `UI/Features/Tooltips/Widgets/TooltipItems/Data` | not named |
| [`DT_RichText_Style_ActionLabel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Shared/Text/DT_RichText_Style_ActionLabel.json) | 2 | `UI/Features/Frontend/Shared/Text` | not named |
| [`DT_RichText_Style_EventFeed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/EventFeed/Widgets/EventFeedEntry/Data/DT_RichText_Style_EventFeed.json) | 2 | `UI/Features/HUD/EventFeed/Widgets/EventFeedEntry/Data` | not named |
| [`DT_RichText_Style_EventLog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/DeathRecap/Widgets/Log/Data/DT_RichText_Style_EventLog.json) | 3 | `UI/Features/DeathRecap/Widgets/Log/Data` | not named |
| [`DT_RichText_Style_InfoPopup`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Widgets/Data/DT_RichText_Style_InfoPopup.json) | 1 | `UI/Features/Popups/Widgets/Data` | not named |
| [`DT_RichText_Style_Photosensitivity`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Photosensitivity/Data/DT_RichText_Style_Photosensitivity.json) | 2 | `UI/Features/Frontend/Photosensitivity/Data` | not named |

#### WDPostProcessEffect

5 table(s), 15 rows, 3 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_AlternativeCriticalCamera`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/DT_AlternativeCriticalCamera.json) | 1 | `GF/AlternativeCriticalCamera/Content` | [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [CROSS_REF](../docs/gap_resolution/CROSS_REF.md), [Wardogs_GameFeatures_AlternativeCriticalCamera_v2](../game-features/Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md) |
| [`DT_PostProcessEffects`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Postprocess/DT_PostProcessEffects.json) | 11 | `VFX/Postprocess` | [Wardogs_VFX_v2](../content/Wardogs_VFX_v2.md) |
| [`DT_PostProcessEffects_FOB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/ForwardOperatingBase/DT_PostProcessEffects_FOB.json) | 1 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_PostProcessEffects_Molotov`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Molotov/Content/Data/DT_PostProcessEffects_Molotov.json) | 1 | `GF/Items/Molotov/Data` | not named |
| [`DT_PostProcessEffects_StimPen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/StimPen/Content/Data/DT_PostProcessEffects_StimPen.json) | 1 | `GF/Items/StimPen/Data` | not named |

#### WDUIUserSettingDisplayDataTableRow

1 table(s), 15 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduiusersettingdisplaydatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Settings_DisplayData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Settings/Data/DT_Settings_DisplayData.json) | 15 | `UI/Features/Settings/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDServerBrowserRegionData

1 table(s), 14 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdserverbrowserregiondata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_OnlineRegions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/FindMatch/Data/DT_OnlineRegions.json) | 14 | `UI/Features/Frontend/FindMatch/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDArchetypeCaliberDamageModifierData

1 table(s), 12 rows, 1 named in docs. Expanded on [All Vehicles Stats and Damage](../content/Wardogs_AllVehicles_Stats_Damage_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InfantryData_ArchetypeCaliberModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_ArchetypeCaliberModifiers.json) | 12 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [GOBJECTS_DAMAGE_ANALYSIS](../docs/GOBJECTS_DAMAGE_ANALYSIS.md), [Wardogs_GameFeatures_Ammo_v2](../game-features/Wardogs_GameFeatures_Ammo_v2.md) (+1) |

#### WDAssistanceRequestData

1 table(s), 12 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdassistancerequestdata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_AssistanceRequests`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/AssistanceRequests/DT_AssistanceRequests.json) | 12 | `GameMechanics/Communication/AssistanceRequests` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDCosmeticSetData

1 table(s), 12 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdcosmeticsetdata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CosmeticSets_Debug`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Cosmetics/DT_CosmeticSets_Debug.json) | 12 | `Meta/Cosmetics` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDMusicState

1 table(s), 12 rows, 1 named in docs. Audio table, skipped.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_MusicSystem`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Audio/Music/DT_MusicSystem.json) | 12 | `Audio/Music` | [Wardogs_Audio_v2](../content/Wardogs_Audio_v2.md) |

#### WDUIDeploymentBoardRejectionTableRow

2 table(s), 12 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduideploymentboardrejectiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_DeploymentRejectionReasons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/DeploymentBoard/Data/DT_DeploymentRejectionReasons.json) | 11 | `UI/Features/DeploymentBoard/Data` | not named |
| [`DT_DeploymentRejectionReasons_ControlZone`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/DeploymentBoard/DT_DeploymentRejectionReasons_ControlZone.json) | 1 | `GF/ControlZone/UI/DeploymentBoard` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |

#### WDUIServerBrowserMapTextureTableRow

1 table(s), 12 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduiserverbrowsermaptexturetablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ServerBrowserMapTexture`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/FindMatch/Data/DT_ServerBrowserMapTexture.json) | 12 | `UI/Features/Frontend/FindMatch/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUISquadIntentTableRow

1 table(s), 12 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduisquadintenttablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_SquadIntents`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/ContextDrawer/Tabs/Party/Data/DT_SquadIntents.json) | 12 | `UI/Features/ContextDrawer/Tabs/Party/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDVehicleSeatNameOverrideRow

9 table(s), 12 rows, 0 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_VehicleSeatOverrides_ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_VehicleSeatOverrides_ROT_02.json) | 1 | `GF/Vehicles/ROT_02/DataTables` | not named |
| [`DT_VehicleSeatOverrides_ROT_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_03/Content/DataTables/DT_VehicleSeatOverrides_ROT_03.json) | 3 | `GF/Vehicles/ROT_03/DataTables` | not named |
| [`DT_VehicleSeatOverrides_ROT_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_04/Content/DataTables/DT_VehicleSeatOverrides_ROT_04.json) | 2 | `GF/Vehicles/ROT_04/DataTables` | not named |
| [`DT_VehicleSeatOverrides_STN_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/DataTables/DT_VehicleSeatOverrides_STN_01.json) | 1 | `GF/Vehicles/STN_01/DataTables` | not named |
| [`DT_VehicleSeatOverrides_STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/DataTables/DT_VehicleSeatOverrides_STN_02.json) | 1 | `GF/Vehicles/STN_02/DataTables` | not named |
| [`DT_VehicleSeatOverrides_STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/DataTable/DT_VehicleSeatOverrides_STN_03.json) | 1 | `GF/Vehicles/STN_03/DataTable` | not named |
| [`DT_VehicleSeatOverrides_STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/DataTables/DT_VehicleSeatOverrides_STN_04.json) | 1 | `GF/Vehicles/STN_04/DataTables` | not named |
| [`DT_VehicleSeatOverrides_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/DataTable/DT_VehicleSeatOverrides_STN_05.json) | 1 | `GF/Vehicles/STN_05/DataTable` | not named |
| [`DT_VehicleSeatOverrides_STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_VehicleSeatOverrides_STN_06.json) | 1 | `GF/Vehicles/STN_06/DataTables` | not named |

#### WDAutomatedTestServerProfile

1 table(s), 11 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdautomatedtestserverprofile).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ServerTestingProfiles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Tests/LoadTests/Data/DT_ServerTestingProfiles.json) | 11 | `Tests/LoadTests/Data` | [Wardogs_Tests_v2](../content/Wardogs_Tests_v2.md) |

#### WDUIVehicleCrosshairDataTableRow

8 table(s), 11 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_VehicleCrosshair_ROT02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/DataTables/DT_VehicleCrosshair_ROT02.json) | 2 | `GF/Vehicles/ROT_02/DataTables` | not named |
| [`DT_VehicleCrosshair_STN01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/DataTables/DT_VehicleCrosshair_STN01.json) | 0 | `GF/Vehicles/STN_01/DataTables` | not named |
| [`DT_VehicleCrosshair_STN06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/DataTables/DT_VehicleCrosshair_STN06.json) | 0 | `GF/Vehicles/STN_06/DataTables` | not named |
| [`DT_VehicleCrosshair_STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/DataTables/DT_VehicleCrosshair_STN_02.json) | 1 | `GF/Vehicles/STN_02/DataTables` | not named |
| [`DT_VehicleCrosshair_STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/DataTable/DT_VehicleCrosshair_STN_03.json) | 1 | `GF/Vehicles/STN_03/DataTable` | not named |
| [`DT_VehicleCrosshair_STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/DataTable/DT_VehicleCrosshair_STN_05.json) | 1 | `GF/Vehicles/STN_05/DataTable` | not named |
| [`DT_VehicleCrosshair_TNK01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/DataTables/DT_VehicleCrosshair_TNK01.json) | 4 | `GF/Vehicles/TNK_01/DataTables` | not named |
| [`DT_VehicleCrosshair_TNK04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/DataTables/DT_VehicleCrosshair_TNK04.json) | 2 | `GF/Vehicles/TNK_04/DataTables` | not named |

#### WDVehicleSeatDamageReductionData

1 table(s), 11 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdvehicleseatdamagereductiondata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InfantryData_VehicleSeatDamageReduction`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_VehicleSeatDamageReduction.json) | 11 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [damage](../docs/evidence/damage.md), [Wardogs_GameFeatures_Ammo_v2](../game-features/Wardogs_GameFeatures_Ammo_v2.md) (+1) |

#### WDAchievementDefinition

1 table(s), 10 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdachievementdefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Achievements`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Achievements/DT_Achievements.json) | 10 | `Meta/Achievements` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_Challenges_v1](../game-features/Wardogs_Challenges_v1.md) |

#### WDReticleAssetInfo

1 table(s), 10 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Gunsmith_Reticles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/ReticleNodeFocus/Data/DT_Gunsmith_Reticles.json) | 10 | `GF/Gunsmith/UI/ReticleNodeFocus/Data` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |

#### WDUIPopupOptionDataTableRow

2 table(s), 10 rows, 2 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_GunsmithPopupOptions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Popups/DT_GunsmithPopupOptions.json) | 5 | `GF/Gunsmith/UI/Data/Popups` | [CROSS_REFERENCE](../docs/CROSS_REFERENCE.md), [CROSS_REF](../docs/gap_resolution/CROSS_REF.md), [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_VehiclesmithPopupOptions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/UI/Scene/Data/DT_VehiclesmithPopupOptions.json) | 5 | `GF/Vehiclesmith/UI/Scene/Data` | [Wardogs_GameFeatures_Vehiclesmith_v2](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) |

#### WDAssistResourceRewardTableRow

1 table(s), 9 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdassistresourcerewardtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_AssistCashRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_AssistCashRewards.json) | 9 | `GameMechanics/Gamemode/Data` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDResourceRewardModifierTableRow

1 table(s), 9 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdresourcerewardmodifiertablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CashRewardModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_CashRewardModifiers.json) | 9 | `GameMechanics/Gamemode/Data` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDMetaTreeTableRow

1 table(s), 7 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetatreetablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_MetaTree_Roles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CharacterSkills/DT_MetaTree_Roles.json) | 7 | `Meta/CharacterSkills` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDUILevelTableRow

1 table(s), 7 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduileveltablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_LevelIcons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_LevelIcons.json) | 7 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDAmmoTypeEffectivenessData

1 table(s), 6 rows, 1 named in docs. Expanded on [All Vehicles Stats and Damage](../content/Wardogs_AllVehicles_Stats_Damage_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InfantryData_AmmoTypeEffectivenessPen`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_Helpers/DT_InfantryData_AmmoTypeEffectivenessPen.json) | 6 | `GameMechanics/DamageSystem/DamageDataTables/DT_Helpers` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [Wardogs_DamagePipeline_v2](../pipelines/Wardogs_DamagePipeline_v2.md) |

#### WDFactoryRecipe

1 table(s), 6 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdfactoryrecipe).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Factory01_Recipes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01/Content/Data/DT_Factory01_Recipes.json) | 6 | `GF/FactoryInvestment_01/Data` | [Wardogs_GameFeatures_FactoryInvestment_01_v2](../game-features/Wardogs_GameFeatures_FactoryInvestment_01_v2.md) |

#### WDFlairMaskInfo

1 table(s), 6 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Itemsmith_Flair_Masks`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Itemsmith/Content/UI/Flair/Data/DT_Itemsmith_Flair_Masks.json) | 6 | `GF/Itemsmith/UI/Flair/Data` | [Wardogs_GameFeatures_Itemsmith_v2](../game-features/Wardogs_GameFeatures_Itemsmith_v2.md) |

#### WDMetaMasteryDefinitionTableRow

1 table(s), 6 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetamasterydefinitiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_RoleMasteryDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Levels/Roles/DT_RoleMasteryDefinitions.json) | 6 | `Meta/Levels/Roles` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDPlacementUiTextRecord

3 table(s), 6 rows, 2 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ControlZone_PlacementDisplayTexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/UI/DT_ControlZone_PlacementDisplayTexts.json) | 1 | `GF/ControlZone/UI` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |
| [`DT_ForwardOperatingBase_PlacementDisplayTexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/ForwardOperatingBase/DT_ForwardOperatingBase_PlacementDisplayTexts.json) | 2 | `GF/Items/Buildables/Data/ForwardOperatingBase` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |
| [`DT_PlacementDisplayTexts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/Placement/Data/DT_PlacementDisplayTexts.json) | 3 | `UI/Features/HUD/Placement/Data` | not named |

#### FToolFont

1 table(s), 5 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ToolsTextAppearance`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Tools/_EditorUILibrary/_Core/Font/DT_ToolsTextAppearance.json) | 5 | `Tools/_EditorUILibrary/_Core/Font` | [Wardogs_Tools_v2](../content/Wardogs_Tools_v2.md) |

#### GrassLayerInfo

1 table(s), 5 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_GrassSettings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/PCG/Runtime/DT_GrassSettings.json) | 5 | `Environment/PCG/Runtime` | [Wardogs_Environment_v2](../content/Wardogs_Environment_v2.md) |

#### WDAmmoModifierTableRow

1 table(s), 5 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdammomodifiertablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_AmmoModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/DamageSystem/DT_AmmoModifiers.json) | 5 | `GameMechanics/DamageSystem` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md), [Wardogs_DamagePipeline_v2](../pipelines/Wardogs_DamagePipeline_v2.md) |

#### WDPlayerIdentityRow

1 table(s), 5 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdplayeridentityrow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_PlayerIdentities`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_PlayerIdentities.json) | 5 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDUIScoreboardStatTableRow

1 table(s), 5 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wduiscoreboardstattablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ScoreboardStats_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Scoreboard/Widgets/Scoreboard/Data/DT_ScoreboardStats_Default.json) | 5 | `UI/Features/Scoreboard/Widgets/Scoreboard/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDAutomatedTestClientProfile

1 table(s), 4 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdautomatedtestclientprofile).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ClientTestingProfiles`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Tests/LoadTests/Orchestrators/RandomScatter/Data/DT_ClientTestingProfiles.json) | 4 | `Tests/LoadTests/Orchestrators/RandomScatter/Data` | [Wardogs_Tests_v2](../content/Wardogs_Tests_v2.md) |

#### WDDevMenuMapsDataTableRow

3 table(s), 4 rows, 2 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wddevmenumapsdatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_DevMenuMaps`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/DevMenu/Data/DT_DevMenuMaps.json) | 2 | `UI/Features/Frontend/DevMenu/Data` | not named |
| [`DT_Gunsmith_DevMenuMaps`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Gunsmith/Content/UI/Data/Entities/DT_Gunsmith_DevMenuMaps.json) | 1 | `GF/Gunsmith/UI/Data/Entities` | [Wardogs_GameFeatures_Gunsmith_v2](../game-features/Wardogs_GameFeatures_Gunsmith_v2.md) |
| [`DT_Vehiclesmith_DevMenuMaps`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehiclesmith/Content/Data/DT_Vehiclesmith_DevMenuMaps.json) | 1 | `GF/Vehiclesmith/Data` | [Wardogs_GameFeatures_Vehiclesmith_v2](../game-features/Wardogs_GameFeatures_Vehiclesmith_v2.md) |

#### WDFactionDataTableRow

1 table(s), 4 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdfactiondatatablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_FactionData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/DT_FactionData.json) | 4 | `GameMechanics/Gamemode/Data` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDPingTypeData

1 table(s), 4 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#wdpingtypedata).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_PingTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Communication/Pings/DT_PingTypes.json) | 4 | `GameMechanics/Communication/Pings` | [Wardogs_GameMechanics_v2](../content/Wardogs_GameMechanics_v2.md) |

#### WDUIInteractionContextStateDataTableRow

1 table(s), 4 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InteractionContextStateData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Interaction/DT_InteractionContextStateData.json) | 4 | `UI/Data/Interaction` | not named |

#### WDUIVendorType

1 table(s), 4 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_VendorTypes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Vendor/Data/DT_VendorTypes.json) | 4 | `UI/Features/Vendor/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDVehicleSlotPartRow

4 table(s), 4 rows, 4 named in docs. Expanded on [Vehicle Handling](../game-features/Wardogs_VehicleHandling_v1.md).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Bobblehead_Faction_SlotParts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Faction/Content/Data/DT_Bobblehead_Faction_SlotParts.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Faction/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| [`DT_Bobblehead_Grenade_SlotParts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Grenade/Content/Data/DT_Bobblehead_Grenade_SlotParts.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Grenade/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| [`DT_Bobblehead_HeavyHelmet_SlotParts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_HeavyHelmet/Content/Data/DT_Bobblehead_HeavyHelmet_SlotParts.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_HeavyHelmet/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |
| [`DT_Bobblehead_Warpup_SlotParts`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Warpup/Content/Data/DT_Bobblehead_Warpup_SlotParts.json) | 1 | `GF/Vehicles/BobbleHeads/Bobblehead_Warpup/Data` | [Wardogs_VehicleHandling_v1](../game-features/Wardogs_VehicleHandling_v1.md) |

#### WDWagerActionDefinition

1 table(s), 4 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwageractiondefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_WagerActions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerActions.json) | 4 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDClientHotConfigTableRow

1 table(s), 3 rows, 1 named in docs. Expanded in [Frontend, Server and Test Data](Wardogs_DataTables_Frontend_v1.md#wdclienthotconfigtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ClientHotConfigs`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ClientHotConfigs/DT_ClientHotConfigs.json) | 3 | `Meta/ClientHotConfigs` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDControlZoneContributionModifierTableRow

1 table(s), 3 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdcontrolzonecontributionmodifiertablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ControlZoneContributionModifiers`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/ControlZone/Content/ControlZone/Data/DT_ControlZoneContributionModifiers.json) | 3 | `GF/ControlZone/ControlZone/Data` | [Wardogs_GameFeatures_ControlZone_v2](../game-features/Wardogs_GameFeatures_ControlZone_v2.md) |

#### WDMissionDefinition

1 table(s), 3 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdmissiondefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_PassiveMissions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/DT_PassiveMissions.json) | 3 | `Meta/Missions` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDUIRadialWheelTableRow

2 table(s), 3 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_RadialWheelTypeDatas`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/RadialWheel/Data/DT_RadialWheelTypeDatas.json) | 2 | `UI/Features/RadialWheel/Data` | not named |
| [`DT_RadialWheelType_BuildToolData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/BuildTool/DT_RadialWheelType_BuildToolData.json) | 1 | `GF/Items/Buildables/Data/BuildTool` | [Wardogs_Buildables_v1](../game-features/Wardogs_Buildables_v1.md) |

#### WDCurrencyDefinition

1 table(s), 2 rows, 0 named in docs. Index only (expanded on another page).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_CurrenciesDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/CurrencyDefinitions/DT_CurrenciesDefinitions.json) | 2 | `Meta/CurrencyDefinitions` | not named |

#### WDUIIndicatorTableRow

1 table(s), 2 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Indicators`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/DamageIndicator/Data/DT_Indicators.json) | 2 | `UI/Features/HUD/DamageIndicator/Data` | not named |

#### WDUIInteractableComponentStateDataTableRow

1 table(s), 2 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_InteractableComponentStateData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/Interaction/DT_InteractableComponentStateData.json) | 2 | `UI/Data/Interaction` | not named |

#### WDUIPopupButtonDataTableRow

1 table(s), 2 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_PopupButtons`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Popups/Widgets/Data/DT_PopupButtons.json) | 2 | `UI/Features/Popups/Widgets/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### BHGameplayEffectTaggedTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Combat, Vehicles and Scene Data](Wardogs_DataTables_Combat_v1.md#bhgameplayeffecttaggedtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Meta_ResourceEffects`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Resources/Effects/DT_Meta_ResourceEffects.json) | 1 | `Meta/Resources/Effects` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### SDUINotificationDataRow

1 table(s), 1 rows, 0 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_Notifications`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/HUD/RewardFeed/Data/DT_Notifications.json) | 1 | `UI/Features/HUD/RewardFeed/Data` | not named |

#### WDExchangeDefinitionTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdexchangedefinitiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_ExchangeDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/ExchangeDefinitions/DT_ExchangeDefinitions.json) | 1 | `Meta/ExchangeDefinitions` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDMetaSeasonDefinitionTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Meta Progression and Cosmetics](Wardogs_DataTables_Meta_v1.md#wdmetaseasondefinitiontablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_SeasonDefinitions`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/DT_SeasonDefinitions.json) | 1 | `Meta` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md), [Wardogs_Season01_CosmeticUnlocks_v1](../content/Wardogs_Season01_CosmeticUnlocks_v1.md), [Wardogs_TreeRewardTrack_PlatformMastery_v1](../content/Wardogs_TreeRewardTrack_PlatformMastery_v1.md) |

#### WDMockInvestmentItemTableRow

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdmockinvestmentitemtablerow).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_MockInvestments`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/MockInvestments/DT_MockInvestments.json) | 1 | `Meta/MockInvestments` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDRewardDefinition

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdrewarddefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_DemoRewards`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Challenges/Demo/DT_DemoRewards.json) | 1 | `Meta/Challenges/Demo` | [Wardogs_Rewards_and_Progression_v2](../Wardogs_Rewards_and_Progression_v2.md), [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDUIInputActionDataTableRow

1 table(s), 1 rows, 1 named in docs. UI widget table, not expanded.

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_UIInputActionData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Data/DT_UIInputActionData.json) | 1 | `UI/Data` | [Wardogs_UI_v2](../content/Wardogs_UI_v2.md) |

#### WDWagerObjectiveCatalogDefinition

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwagerobjectivecatalogdefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_WagerObjectiveCatalog`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerObjectiveCatalog.json) | 1 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |

#### WDWagerPricingDefinition

1 table(s), 1 rows, 1 named in docs. Expanded in [Economy and Rewards](Wardogs_DataTables_Economy_v1.md#wdwagerpricingdefinition).

| Table | Rows | Folder | Documented in |
|---|---|---|---|
| [`DT_WagerPricing`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Wagers/DT_WagerPricing.json) | 1 | `Meta/Wagers` | [Wardogs_Meta_v2](../content/Wardogs_Meta_v2.md) |
<!-- /datatable_catalog -->
