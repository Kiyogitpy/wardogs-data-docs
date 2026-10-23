---
title: "Character (feature)"
redirect_from: ["/Wardogs_GameFeatures_Character_v2.html", "/Wardogs_GameFeatures_Character_v2"]
parent: "Player & Movement"
description: "What This Folder Holds, Packs"
---

# Wardogs — GameFeatures: Character
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/Character/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Character) — 2 JSON files, both under [`Kits/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Character/Kits).*

---

## 1. What This Folder Holds

Character kits. A kit is a GameFeature pack that loads an External Data Layer for one kit's content. Two kit folders exist.

| Kit | File | Contents |
|---|---|---|
| [`CKIT_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/CKIT_001/CKIT_001/Content/CKIT_001.json) | [`Kits/CKIT_001/CKIT_001/Content/CKIT_001.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/CKIT_001/CKIT_001/Content/CKIT_001.json) | GameFeatureData pack with a world-partition action adding `EDL_CKIT_001` |
| [`KIT_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/KIT_001/Content/KIT_001.json) | [`Kits/KIT_001/Content/KIT_001.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/KIT_001/Content/KIT_001.json) | GameFeatureData pack with no actions (empty) |

---

## 2. Packs

| Pack | Action | Data layer |
|---|---|---|
| [`CKIT_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/CKIT_001/CKIT_001/Content/CKIT_001.json) | `GameFeatureAction_AddWorldPartitionContent` | `EDL_CKIT_001` |
| [`KIT_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/KIT_001/Content/KIT_001.json) | none | none |

The [`CKIT_001`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Character/Kits/CKIT_001/CKIT_001/Content/CKIT_001.json) pack also scans `PrimaryAssetType: None` on `UObject` with no directories, so it adds no assets through the scan.

---

## 3. Still not pulled / limitations

- **Kit contents.** The `EDL_CKIT_001` layer's content (the character's cosmetic or gear set) is not in this folder. Kit assets are probably covered by the Skins or Items docs.
- **KIT_001.** Empty in this dump. Not explained.
- **Kit definitions.** How a kit is selected and mapped to a character is not in this folder.
