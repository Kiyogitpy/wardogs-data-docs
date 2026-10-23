---
title: "FactoryInvestment 01 (feature)"
redirect_from: ["/Wardogs_GameFeatures_FactoryInvestment_01_v2.html", "/Wardogs_GameFeatures_FactoryInvestment_01_v2"]
parent: "Game Modes & Maps"
description: "What This Folder Holds, Investment Definition, Production Lines, Recipes"
---

# Wardogs — GameFeatures: FactoryInvestment_01
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: [`Plugins/GameFeatures/FactoryInvestment_01/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01) — 3 JSON files.*

---

## Season 02 update (2026-10-15)

- `Id.Item.AK74M` ProductionCost: 1280 → 640.
- `Id.Item.MP9` ProductionCost: 720 → 1100.
- `Id.Item.Vector` ProductionCost: 2080 → 4480.

Full before/after list: [Season 2 Changes → Game Modes & Maps]({{ '/season-2-changes/game-modes-maps.html' | relative_url }}).

---

## 1. What This Folder Holds

The first factory investment (investment ID `Id.Investment.Factory01`; the display name begins "Zaystev Foun…" in the source). It sets three production lines, the recipes they can make, the costs, and the upgrade values that control queue size and storage.

| File | Type | Role |
|---|---|---|
| [`Content/FactoryInvestment_01.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01/Content/FactoryInvestment_01.json) | GameFeatureData + registry action | Adds the recipe table into `FactoryRecipes` |
| [`Content/Data/DA_FactoryInvestment_01.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01/Content/Data/DA_FactoryInvestment_01.json) | `WDFactoryInvestment` (+ `WDInvestmentDefinition`) | Lines, upgrades, and the investment definition |
| [`Content/Data/DT_Factory01_Recipes.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01/Content/Data/DT_Factory01_Recipes.json) | DataTable (`WDFactoryRecipe`) | Six recipes |

---

## 2. Investment Definition (`WDInvestmentDefinition`)

| Field | Value |
|---|---|
| ID | `Id.Investment.Factory01` |
| DisplayName | Localised; the source string starts "Zaystev Foun…" (truncated in the dump) |
| PurchaseCost | `Attribute.Meta.Currency.Cash` ×200 |
| Type | `EWDInvestmentType::Passive` |
| MapIcon | a `T_UI_Icon_FiringMode_*` texture path |

The investment is passive: it runs once bought, with no active use.

---

## 3. Production Lines

| Line | Available recipes |
|---|---|
| Line 1 | `Id.Item.AK74M`, `Id.Item.M4` |
| Line 2 | `Id.Item.Vector`, `Id.Item.MP9` |
| Line 3 | `Id.Item.4xElcanSpectr`, `Id.Item.EotechHoloSight` |

Each line can make only the two recipes listed for it.

---

## 4. Recipes ([`DT_Factory01_Recipes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment_01/Content/Data/DT_Factory01_Recipes.json))

All six share the same timing and discount.

| Recipe | ProductionCost | RecipeDuration | ProductionDiscount | Override cost |
|---|---|---|---|---|
| `Id.Item.AK74M` | 640 | 10.0 | 20.0 | false |
| `Id.Item.M4` | 2240 | 10.0 | 20.0 | false |
| `Id.Item.MP9` | 1100 | 10.0 | 20.0 | false |
| `Id.Item.Vector` | 4480 | 10.0 | 20.0 | false |
| `Id.Item.4xElcanSpectr` | 640 | 10.0 | 20.0 | false |
| `Id.Item.EotechHoloSight` | 496 | 10.0 | 20.0 | false |

`bOverrideProductionCost` is false on every row, so the cost shown is the row's own value. The discount of 20.0 is most likely a percent (inferred from the name, not confirmed).

The recipes are weapons and optics. Lines 1 and 2 hold weapons (AK74M, M4 on line 1; Vector, MP9 on line 2). Line 3 holds optics (4xElcanSpectr, EotechHoloSight).

---

## 5. Upgrades

Four upgrade entries. Each has a value and a curve from the base [`CT_Factory_UpgradeValues`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/FactoryInvestment/Content/Data/CT_Factory_UpgradeValues.json) table in the FactoryInvestment doc.

| Upgrade tag | Curve row | Value |
|---|---|---|
| `Meta.Investment.Upgrade.Factory.ProductionLineOneQueueSize` | `QueueSize` | 1.0 |
| `Meta.Investment.Upgrade.Factory.ProductionLineTwoQueueSize` | `QueueSize` | 1.0 |
| `Meta.Investment.Upgrade.Factory.ProductionLineThreeQueueSize` | `QueueSize` | 1.0 |
| `Meta.Investment.Upgrade.Factory.StorageSize` | `StorageSize` | 1.0 |

The `Value` of 1.0 is the starting upgrade level. The curve turns that level into the actual queue or storage size (for example, level 1 gives a queue of 5 and storage of 5, per the curve table).

---

## 6. How Values Combine

- The investment costs 200 cash. What it unlocks at purchase is not stated in this folder.
- Each production line's queue size is read from `QueueSize` at its upgrade level (inferred from the row names): 5 at level 1, rising to 20 at level 4.
- Storage size is read from `StorageSize` the same way (inferred).
- Recipe cost is `ProductionCost`, with a 20% discount where `ProductionDiscount` applies. How the discount is applied is not in this folder.

---

## 7. Still not pulled / limitations

- **Discount meaning.** Whether `ProductionDiscount` 20.0 is a percent, and how it applies, is not confirmed.
- **Recipe duration.** 10.0 is the value in the export; its unit (seconds assumed) is not stated.
- **Icons and strings.** The display name and the map icon are localised or texture references; not resolved here.
  - **See [`docs/CROSS_REFERENCE.md`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/CROSS_REFERENCE.md)** for the project-wide cross-reference index of where referenced assets are defined.
- **Factory world content.** The factory's world layer and buildings are not in this folder.
- **Source-string names.** The DisplayName is taken from the localised source string as-is.
