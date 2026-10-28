---
title: Backpacks
parent: "Equipment"
group: "Utility"
description: "The six standard backpacks and the Pouch: how many inventory slots each one adds, its grid and its price."
---

# Backpacks

| Backpacks | |
|---|---|
| ![Backpacks]({{ '/assets/img/icons/utility-3d/T_UI_Item_Backpack_Pouch_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Backpack, extra storage |
| Slots | 6 (Pouch) to 24 (Ruck Backpack) |
| **Use** | |
| Placement | Pouch: vertical placement only. Others: not stated |
| **Availability** | |
| Price | 0 (Pouch) to 1,600 cash (Ruck Backpack) |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.Pouch`, `Id.Item.SmallBackpack`, `Id.Item.BPAK_005`, `Id.Item.MediumBackpack`, `Id.Item.BPAK_006`, `Id.Item.LargeBackpack`, `Id.Item.BPAK_007` |
{: .wiki-infobox }

A backpack adds a grid of storage slots for items. The Pouch is free, and each bigger bag costs more and holds more slots. The bags with a sling, which also add a slot for a weapon or special item, are on the [Sling Backpacks](sling-backpacks.md) page.

## Overview

The standard backpacks differ in price, grid and slot count. The shop text gives the grid for each one. The Pouch is the only bag with a placement rule: it only allows vertical placement. The Halftrack Backpack also exists, but the shop hides it.

## How it works

| Backpack | Price (cash) | Grid | Slots | Weight (kg) |
|---|---:|---|---:|---:|
| Pouch | 0 | 3 x 2 (vertical placement only) | 6 | 0.3 |
| Scout Backpack | 350 | 4 x 2 | 8 | 0.5 |
| Field Backpack | 650 | 6 x 2 | 12 | 0.8 |
| Operator Backpack | 800 | 5 x 3 | 15 | 0.88 |
| Assault Backpack | 1,200 | 5 x 5 | 21 | 1.3 |
| Ruck Backpack | 1,600 | 6 x 4 | 24 | 1.5 |
| Halftrack Backpack (hidden in the shop) | 15,000 | 6 x 5 | 30 | 2.78 |

The weight is in kilograms. The game stores item weight as a whole number 1,000 times the kilogram figure, so the kilogram value here is derived from it. The game files draw some bags with a different grid shape from the shop text, for example the Scout Backpack. This page uses the shop text.

The Halftrack Backpack has no price in the shop and cannot be bought there. No vendor, loot table or unlock that gives it is known, so how it can be obtained is not known.

The standard backpacks have no other effect. The number of slots is the only stated benefit.

## Season 2 changes

No Season 2 change to the standard backpacks is listed.

## See also

- [Sling Backpacks](sling-backpacks.md), for the bags with a sling slot
- [Tac Vests](tac-vests.md), which add quick slots rather than storage
- [Parachutes](parachutes.md)
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock level, grids and slot counts, the hidden Halftrack Backpack, weights
- [Items (data)](../../content/Wardogs_Items_v2.md): backpack weights and grid shapes in the item data
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): no vendor, loot or unlock row (P38)
- [Round 43 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md)
