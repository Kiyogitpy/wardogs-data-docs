---
title: "FactoryInvestment (feature)"
redirect_from: ["/Wardogs_GameFeatures_FactoryInvestment_v2.html", "/Wardogs_GameFeatures_FactoryInvestment_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Recipe Registry, Upgrade Values"
---

# Wardogs — GameFeatures: FactoryInvestment
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/FactoryInvestment/` — 2 JSON files. The Factory 01 investment is in the FactoryInvestment_01 doc.*

---

## 1. What This Folder Holds

The shared factory-investment base: the upgrade-value curve table that every factory investment reads from, and the recipe registry that factory packs add to.

| File | Type | Role |
|---|---|---|
| `Content/FactoryInvestment.json` | GameFeatureData + registry action | Registers the factory recipe registry |
| `Content/Data/CT_Factory_UpgradeValues.json` | CurveTable | Upgrade values by level |

---

## 2. Recipe Registry

| Item | Value |
|---|---|
| Registry | `DR_FactoryRecipes` at `/FactoryInvestment/Data/DR_FactoryRecipes` |
| Preload in editor | true |

The registry asset `DR_FactoryRecipes` is referenced but is not in this folder. The Factory 01 pack adds its recipe table into this registry.

---

## 3. Upgrade Values (`CT_Factory_UpgradeValues`)

Three rows. Each row is a curve with a constant interpolation mode; the key time is the upgrade level.

| Row | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
|---|---|---|---|---|---|
| `QueueSize` | 5 | 10 | 15 | 20 | 20 |
| `SlotAmount` | 1 | 2 | 3 | 4 | 5 |
| `StorageSize` | 5 | 10 | 15 | 20 | 20 |

Every row has `DefaultValue` 3.4028235e+38 (the float maximum). Pre- and post-infinity extrapolation is constant, so a level above 5 holds the last value.

The Factory 01 investment reads these rows through its upgrade entries (see the FactoryInvestment_01 doc).

---

## 4. Still not pulled / limitations

- **What the rows mean in game.** `QueueSize` is most likely the production queue length and `SlotAmount` the number of slots, but the dump does not say so. Inferred from names and the Factory 01 use.
- **Recipe registry.** `DR_FactoryRecipes` itself is not in this folder.
- **Units.** Values are unitless counts in the export.
