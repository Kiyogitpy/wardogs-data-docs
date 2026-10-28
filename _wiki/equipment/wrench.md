---
title: Wrench
parent: "Equipment"
group: "Utility"
description: "The Wrench: the cheapest vehicle repair tool, a slow hand repair for any vehicle, with durability 600."
---

# Wrench

| Wrench | |
|---|---|
| ![Wrench]({{ '/assets/img/icons/utility-3d/T_UI_Item_Repair_1_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Repair tool, quick slot |
| Repairs | All vehicles |
| Speed | Slow |
| **Use** | |
| Repair rate | 10 vehicle health every 0.68 s (about 14.7 per second) |
| Durability | 600 (vehicle health it can repair) |
| **Availability** | |
| Price | 180 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `ID.Item.RepairTool.Wrench.Standard` |
{: .wiki-infobox }

The Wrench is the basic hand tool for repairing vehicles. It can repair any vehicle, but more slowly than the [Drills](drills.md). It needs no batteries, and it sits in the quick slots.

## Overview

The shop text describes the Wrench as a tool for manually repairing all vehicles at a slow repair speed. It is the cheapest of the three repair tools. The Wrench is the slowest of the repair tools: about 14.7 vehicle health per second, against 19.3 for the Light Drill and 29 for the Heavy Drill.

## How it works

- Each application repairs 10 vehicle health every 0.68 seconds, about 14.7 per second.
- The use continues until the Wrench is empty or the vehicle is full.
- Durability 600 is the amount of vehicle health the Wrench can repair. A full Wrench restores 600 health in about 41 seconds (60 applications).

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
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Repair per application, rate and durability meaning.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
