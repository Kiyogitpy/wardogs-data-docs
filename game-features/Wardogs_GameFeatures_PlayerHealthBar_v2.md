---
title: "Player Health Bar"
redirect_from: ["/Wardogs_GameFeatures_PlayerHealthBar_v2.html", "/Wardogs_GameFeatures_PlayerHealthBar_v2"]
parent: "Player & Movement"
description: "The player's own health bar on the HUD: one widget under a health tag and the view settings for armour."
---

# Wardogs — GameFeatures: PlayerHealthBar
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/PlayerHealthBar/` — 2 JSON files.*

---

## 1. What This Folder Holds

The player's own health bar on the HUD. A small pack: a GameFeatureData that adds one HUD widget under a health tag, and a view-data asset that sets how the bar shows armour.

| File | Type | Role |
|---|---|---|
| `Content/PlayerHealthBar.json` | GameFeatureData + widget actions | Adds the health widget (6 exports: 1 pack, 1 action, 4 instances) |
| `Content/Data/DA_PlayerHealthBar.json` | `WDUIPlayerHealthBarData` | Armour display setting |

---

## 2. HUD Widget

| Item | Value |
|---|---|
| Tag | `UI.HUD.Element.Health` |
| Widget | `W_PlayerHealthBar` (under `/PlayerHealthBar/Data/`) |
| Widget instances | 4 (`WDGameFeatureAction_AddWidgetElements_Instance_0` to `_3`), with no properties in the export |

---

## 3. Data

| Field | Value |
|---|---|
| `ArmorUnequippedOpacity` | 0.3 |

The name suggests the armour segment is shown at 30% opacity when no armour is equipped. This is inferred from the field name; the widget is not in this folder.

---

## 4. Still not pulled / limitations

- **Instance data.** The four widget instances export with no properties, so their placement and layer values are not known.
- **Bar behaviour.** How the bar maps health to fill is in the widget blueprint, not in this folder.
- **Armour states.** Only the unequipped opacity is set here. Other armour states are in the widget.
