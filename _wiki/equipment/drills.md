---
title: Drills
parent: "Equipment"
group: "Utility"
description: "The Light and Heavy Drills: the battery-powered vehicle repair tools, with the Heavy Drill as the fastest repair on the list."
---

# Drills

| Drills | |
|---|---|
| **General** | |
| Type | Repair tool, specialist item |
| Repairs | Vehicles |
| Power | Batteries |
| **Use** | |
| Repair speed | Light: moderate. Heavy: fastest |
| Repair per application | 14.5 vehicle health (both) |
| Repair rate | Light 19.3 per second (every 0.75 s); Heavy 29 per second (every 0.5 s) |
| Battery use | 1.25 per second (both, item data; unit not stated) |
| **Availability** | |
| Price | 600 (Light), 1,300 cash (Heavy) |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `ID.Item.RepairTool.Drill.Light`, `ID.Item.RepairTool.Drill.Heavy` |
{: .wiki-infobox }

The Light and Heavy Drills are the battery-powered repair tools for vehicles. They repair faster than the [Wrench](wrench.md), but they need [Batteries](batteries.md) to work. The Heavy Drill is the fastest repair tool in the shop.

## Overview

The shop text says the Light Drill has a moderate repair speed and the Heavy Drill the fastest. Both require batteries. Both drills repair 14.5 vehicle health per application and draw the same battery use. The Heavy Drill applies its repair every 0.5 seconds and the Light Drill every 0.75 seconds, which is where the gap in speed comes from.

## How it works

- Using a drill repairs a vehicle. The use continues until the drill's power is spent or the vehicle is full.
- Both drills draw 1.25 battery per second in use, according to the item data. The unit is not stated.
- Both have a reload action in the data. What it reloads is not yet known.
- The item data gives each drill a melee value: 5 for the Light Drill and 10 for the Heavy Drill.
- The Light Drill repairs 14.5 health every 0.75 seconds (about 19.3 per second). The Heavy Drill repairs 14.5 health every 0.5 seconds (29 per second). The drills have no durability value in the data.

| Drill | Price (cash) | Weight (kg) | Grid | Melee value |
|---|---:|---:|---|---:|
| Light Drill | 600 | 1.5 | 2 x 2 | 5 |
| Heavy Drill | 1,300 | 6.9 | 3 x 2 | 10 |

The weights are in kilograms. The game stores item weight as a whole number 1,000 times the kilogram figure, so the kilogram value here is derived from it.

## Season 2 changes

No Season 2 change to the drills is listed in the data.

## See also

- [Batteries](batteries.md), which power the drills
- [Wrench](wrench.md), the slow hand repair tool
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, unlock levels, shop text, weights, grids and melee values
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the repair, reload and use-until-empty rules
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Drill repair per application and rate.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
- [Round 43 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md)
