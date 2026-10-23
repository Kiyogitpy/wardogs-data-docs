---
title: "WDAutomation (feature)"
redirect_from: ["/Wardogs_GameFeatures_WDAutomation_v2.html", "/Wardogs_GameFeatures_WDAutomation_v2"]
parent: "Engine & Tooling Data"
description: "What This Folder Holds, Primary Asset Scan"
---

# Wardogs — GameFeatures: WDAutomation
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/WDAutomation/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/WDAutomation) — 1 JSON file ([`Content/WDAutomation.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WDAutomation/Content/WDAutomation.json)).*

---

## 1. What This Folder Holds

The automation pack. It registers the `WDAutomationLogicSequence` primary asset type so that logic-sequence assets can be found and loaded. It adds no components and no actions. The folder itself has no asset other than the GameFeatureData.

---

## 2. Primary Asset Scan

| Setting | Value |
|---|---|
| PrimaryAssetType | `WDAutomationLogicSequence` |
| AssetBaseClass | `WDAutomationLogicSequence` (WDAutomationRuntime) |
| bHasBlueprintClasses | true |
| bIsEditorOnly | false |
| Directory | `/WDAutomation/AutomationLogicSequences` |

---

## 3. Still not pulled / limitations

- **Logic sequences.** The sequences themselves are not in this dump. The scan points to a directory that is not part of this folder.
- **Purpose.** The dump does not say what the sequences automate (test scripting, scripted scenarios, or both).
