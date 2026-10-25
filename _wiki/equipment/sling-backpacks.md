---
title: Sling Backpacks
parent: "Equipment"
group: "Utility"
description: "The three backpacks with a sling: the Medium Backpack and Sling, the Gunner Backpack and the Arsenal Backpack, with their extra slots and prices."
---

# Sling Backpacks

| Sling Backpacks | |
|---|---|
| **General** | |
| Type | Backpack with sling slots |
| Sling slots | 1 (Medium and Gunner), 2 (Arsenal) |
| **Use** | |
| Extra carry | One weapon or special item (Medium); equipment (Gunner, Arsenal) |
| **Availability** | |
| Price | 1,400 (Medium, hidden in the shop), 2,400 (Gunner), 4,000 cash (Arsenal) |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.MediumSlingBackpack`, `Id.Item.LargeSlingBackpack`, `Id.Item.ExtraLargeSlingBackpack` |
{: .wiki-infobox }

A sling backpack is a bag that also has a sling slot, which holds one more item outside the bag grid. There are three of them. The Medium Backpack and Sling is hidden in the shop, so it cannot be bought there.

## Overview

The sling slots are for weapons or special items. The shop text describes the Medium Backpack and Sling as adding storage plus a sling for an additional weapon or special item. The Gunner and Arsenal backpacks add slots for additional equipment.

## How it works

| Backpack | Price (cash) | Grid | Slots | Sling | Weight (kg) |
|---|---:|---|---:|---|---:|
| Medium Backpack and Sling (hidden in the shop) | 1,400 | not given in the shop text (3 x 5 in the item data) | not given | 1 weapon or special item | 4.0 |
| Gunner Backpack and Sling | 2,400 | 6 x 4 | 24 | 1 equipment slot | 1.5 |
| Arsenal Backpack and 2 Slings | 4,000 | 6 x 4 | 24 | 2 equipment slots | 1.5 |

The item data gives the Medium Backpack and Sling a weapon slot that holds one item. It gives the Arsenal Backpack two sling slots, each holding one item. The weights are in kilograms, the unit the game shows for item weight.

The item data gives the Medium Backpack and Sling a much higher weight (4.0) than the plain Medium Backpack (0.88). The sources do not explain the difference.

## Season 2 changes

No Season 2 change to the sling backpacks is listed in the data.

## See also

- [Backpacks](backpacks.md), for the standard bags
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock level, shop text, the hidden Medium Backpack and Sling, weights
- [Items (data)](../../content/Wardogs_Items_v2.md): sling slot layout and weights in the item data
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): checked for changes
