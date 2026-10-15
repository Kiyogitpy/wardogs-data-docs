---
title: "Character (feature)"
parent: "Game Features"
---

# Wardogs — GameFeatures: Character (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/Character/` — 2 JSON files, both under `Kits/`.*

---

## 1. What This Folder Holds

Character kits. A kit is a GameFeature pack that loads an External Data Layer for one kit's content. Two kit folders exist.

| Kit | File | Contents |
|---|---|---|
| `CKIT_001` | `Kits/CKIT_001/CKIT_001/Content/CKIT_001.json` | GameFeatureData pack with a world-partition action adding `EDL_CKIT_001` |
| `KIT_001` | `Kits/KIT_001/Content/KIT_001.json` | GameFeatureData pack with no actions (empty) |

---

## 2. Packs

| Pack | Action | Data layer |
|---|---|---|
| `CKIT_001` | `GameFeatureAction_AddWorldPartitionContent` | `EDL_CKIT_001` |
| `KIT_001` | none | none |

The `CKIT_001` pack also scans `PrimaryAssetType: None` on `UObject` with no directories, so it adds no assets through the scan.

---

## 3. Still not pulled / limitations

- **Kit contents.** The `EDL_CKIT_001` layer's content (the character's cosmetic or gear set) is not in this folder. Kit assets are probably covered by the Skins or Items docs.
- **KIT_001.** Empty in this dump. Not explained.
- **Kit definitions.** How a kit is selected and mapped to a character is not in this folder.
