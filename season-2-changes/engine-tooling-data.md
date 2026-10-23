---
title: "Engine & Tooling Data changes"
parent: "Season 2 Changes"
nav_order: 10
description: "Engine & Tooling Data: 20 assets added, 3 removed, 140 modified with real changes, 1 moved. Mostly UI widget data; a high ping kick feature and wagers UI are new."
---

# Engine & Tooling Data changes

Season 1 to Season 2 changes for this area, from the area diff file. Audio and UI widget assets are counted only. Every change in this area is in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=engine-tooling-data), where each asset and property can be filtered.

| Measure | Count |
|---|---:|
| Assets added | 20 |
| Assets removed | 3 |
| Assets modified with real changes | 140 |
| Assets moved | 1 |
| Noise-only modified assets (skipped, no real change) | 85 |
| Property changes | 1,056 (changed 86, added 617, removed 353); 41 further entries are on the removed assets |

## Gameplay-relevant changes

- High ping kick: a new `HighPingKick` game feature (GameFeatureData) is added.
- Wagers: 8 UI assets for the wager HUD, receipt, status, toast, vendor panel and objective selector are added. The wager data itself is in `Meta/Wagers` (see the rewards page).
- Vehicle countermeasures: `DA_VehicleCountermeasure` moved from the flares folder to the countermeasures folder (UI data).

Other added assets are listed by folder below. Audio and UI are counted in the next table.

## Audio and UI (counts only)

| Class | Added | Modified with real changes | Noise-only | Removed | Browse |
|---|---:|---:|---:|---:|---|
| Audio | 0 | 1 | 0 | 0 | [audio changes]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=engine-tooling-data&q=CrosstalkAudioEvent) |
| UI widgets | 19 | 137 | 84 | 3 | [ui widgets changes]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=engine-tooling-data&q=UI) |

1 moved asset (ui class, count only): `DA_VehicleCountermeasure` moved from `Wardogs/Content/UI/Features/HUD/Vehicles/NEWHUD/Flares/Data/DA_VehicleFlares.json` → `Wardogs/Content/UI/Features/HUD/Vehicles/NEWHUD/Countermeasures/Data/DA_VehicleCountermeasure.json`. Browse it in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=engine-tooling-data&q=DA_VehicleCountermeasure).

## Added in Season 2 (gameplay and visual assets)

| Folder | Type | Added assets |
|---|---|---|
| `Plugins/GameFeatures/HighPingKick/Content` | GameFeatureData (1) | `HighPingKick` |

Total in this table: 1 asset. Audio and UI added assets are counted above and are not listed.

## Removed in Season 2


3 removed asset(s) are UI widget data (count only). Browse them in the [change browser]({{ '/season-2-changes/all-changes.html' | relative_url }}#area=engine-tooling-data&q=UI).

## See also

- [UI]({{ '/content/Wardogs_UI_v2.html' | relative_url }}#season-02-update)
- [External assets]({{ '/content/Wardogs_ExternalAssets_v2.html' | relative_url }}#season-02-update)

