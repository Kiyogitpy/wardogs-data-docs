---
title: Wrench
parent: "Equipment"
group: "Utility"
description: "The Wrench: the cheapest vehicle repair tool, a slow hand repair for any vehicle, with durability 600."
---

# Wrench

| Wrench | |
|---|---|
| **General** | |
| Type | Repair tool, quick slot |
| Repairs | All vehicles |
| Speed | Slow |
| **Use** | |
| Repair per application | +5 vehicle health (item data) |
| Durability | 600 |
| **Availability** | |
| Price | 180 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.RepairTool.Wrench.Standard` |
{: .wiki-infobox }

The Wrench is the basic hand tool for repairing vehicles. It can repair any vehicle, but more slowly than the [Drills](drills.md). It needs no batteries, and it sits in the quick slots.

## Overview

The shop text describes the Wrench as a tool for manually repairing all vehicles at a slow repair speed. It is the cheapest of the three repair tools. The data gives the same repair amount for each repair tool, so the speed difference comes from the shop text, not from numbers.

## How it works

- Using the Wrench on a vehicle adds 5 vehicle health per application, according to the item data.
- The use continues until the Wrench is empty or the vehicle is full.
- Durability is 600 in the item data. What that number counts, such as uses or seconds, is not stated.
- The time for each application is not yet known.

The Wrench is different from the Mechanical Supplies. Those are the resource a Repair Station uses, as described on the [Supplies](supplies.md) page.

## Season 2 changes

| Item | Season 1 | Season 2 |
|---|---:|---:|
| Wrench price (cash) | 150 | 180 |

## See also

- [Drills](drills.md), for the faster repair tools
- [Supplies](supplies.md), for the Mechanical Supplies used by Repair Stations
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock level, shop text, durability and health value
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the repair use and the use-until-empty rule
- [Items and Equipment, Season 2](../../season-2-changes/items-equipment.md): price change
