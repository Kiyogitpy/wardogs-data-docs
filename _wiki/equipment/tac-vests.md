---
title: Tac Vests
parent: "Equipment"
group: "Utility"
description: "The three Tac Vests: how many quick slots each one unlocks, how much it speeds reloading and switching, and what each costs."
---

# Tac Vests

| Tac Vests | |
|---|---|
| ![Tac Vests]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Utility_SmallWebbing_Textured_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Vest, quick slots |
| Extra quick slots | 2 (Small), 4 (Medium), 6 (Large) |
| Storage | None added |
| **Use** | |
| Reload speed | Minor (Small), moderate (Medium), strong (Large) increase |
| Utility equip and holster speed | Same steps as reload speed |
| **Availability** | |
| Price | 100 (Small), 250 (Medium), 400 cash (Large) |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.SmallTacVest`, `Id.Item.MediumTacVest`, `Id.Item.LargeTacVest` |
{: .wiki-infobox }

The Tac Vest is a piece of gear that unlocks quick slots and speeds up reloading and switching to utility items. It is not body armor, and it has no damage reduction. The three sizes differ in price and in how many quick slots they open.

## Overview

Each vest is one step up from the last. The Small Tac Vest is the cheapest and opens two quick slots. The Large Tac Vest opens all of them. None of the vests adds storage, so storage still comes from a [backpack](backpacks.md).

## How it works

| Vest | Price (cash) | Weight (kg) | Quick slots unlocked (shop text) | Reload and utility speed (shop text, multiplier from the data) |
|---|---:|---:|---|---|
| Small Tac Vest | 100 | 0.82 | 5 and 6 | minor increase (x1.02) |
| Medium Tac Vest | 250 | 1.65 | 5 to 8 | moderate increase (x1.05) |
| Large Tac Vest | 400 | 3.6 | all | strong increase (x1.08) |

The weights are in kilograms, the unit the game shows for item weight.

The shop describes the speed gains only in words, but the equipped effect of each vest has the numbers. It multiplies reload speed, utility equip speed and utility holster speed by the same amount: 1.02 for the Small Tac Vest, 1.05 for the Medium and 1.08 for the Large.

For armor that protects against damage, see [Body Armor](body-armor.md).

## Season 2 changes

No Season 2 change to the Tac Vests is listed.

## See also

- [Backpacks](backpacks.md), for storage
- [Body Armor](body-armor.md), for protection

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock level, shop text
- [Items (data)](../../content/Wardogs_Items_v2.md): extra quick slots and weights in the item data
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): the Tac-Vest slot name
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
