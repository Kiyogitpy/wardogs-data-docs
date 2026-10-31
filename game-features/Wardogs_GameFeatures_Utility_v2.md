---
title: "Utility"
redirect_from: ["/Wardogs_GameFeatures_Utility_v2.html", "/Wardogs_GameFeatures_Utility_v2"]
parent: "Engine & Tooling Data"
description: "Thin packs for consumables, deployables, throwables and tools, each adding one external data layer of world content."
---

# Wardogs — GameFeatures: Utility
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/Utility/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Utility) — 13 JSON files.*

---

## 1. What This Folder Holds

Utility is a set of thin GameFeature packs. Each pack is one consumable, deployable, throwable or tool, and each one does only one thing: it adds an External Data Layer (EDL) that holds the item's world content. The items' gameplay data lives in the Items and Weapons folders, which other docs cover.

| Metric | Value |
|---|---|
| Files | 13 |
| GameFeatureData packs | 13 |
| Actions per pack | 1 `GameFeatureAction_AddWorldPartitionContent` (12 packs) or none ([`THRW_007`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Throwables/THRW_007/Content/THRW_007.json)) |
| Data layers referenced | 12 |

---

## 2. Packs and Data Layers

| Category | Pack | Data layer (EDL) |
|---|---|---|
| Consumables | [`CONS_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Consumables/CONS_001/Content/CONS_001.json) | `EDL_CONS_001` |
| Consumables | [`CONS_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Consumables/CONS_002/Content/CONS_002.json) | `EDL_CONS_002` |
| Consumables | [`CONS_003`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Consumables/CONS_003/Content/CONS_003.json) | `EDL_CONS_003` |
| Deployables | [`DPLY_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Deployables/DPLY_001/Content/DPLY_001.json) | `EDL_DPLY_001` |
| Deployables | [`DPLY_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Deployables/DPLY_002/Content/DPLY_002.json) | `EDL_DPLY_002` |
| Deployables | [`DPLY_003`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Deployables/DPLY_003/Content/DPLY_003.json) | `EDL_DPLY_003` |
| Throwables | [`THRW_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Throwables/THRW_001/Content/THRW_001.json) | `EDL_THRW_001` |
| Throwables | [`THRW_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Throwables/THRW_002/Content/THRW_002.json) | `EDL_THRW_002` |
| Throwables | [`THRW_007`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Throwables/THRW_007/Content/THRW_007.json) | none (empty pack) |
| Tools | [`TOOL_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Tools/TOOL_001/Content/TOOL_001.json) | `EDL_TOOL_001` |
| Tools | [`TOOL_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Tools/TOOL_002/Content/TOOL_002.json) | `EDL_TOOL_002` |
| Tools | [`TOOL_003`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Tools/TOOL_003/Content/TOOL_003.json) | `EDL_TOOL_003` |
| Tools | [`TOOL_004`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Tools/TOOL_004/Content/TOOL_004.json) | `EDL_TOOL_004` |

Each pack is a single GameFeatureData asset plus its action. The EDL name matches the pack name with an `EDL_` prefix.

---

## 3. How It Is Used

- Loading a pack activates its data layer, which brings the item's world content into the level.
- Packs are split by category so they can be loaded per item rather than all at once.
- [`THRW_007`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Utility/Throwables/THRW_007/Content/THRW_007.json) has no action or data layer in this dump. It may be a placeholder or a throwable whose content is provided elsewhere. Not confirmed.

---

## 4. Still not pulled / limitations

- **Layer contents.** The EDL assets themselves are not in this folder, so what each layer contains is not shown.
- **Item linkage.** The mapping from a pack to the item tag (for example `Id.Item.*`) is not in this folder. It is in the Items and Weapons data.
- **THRW_007.** Not explained by the dump.
