---
title: Drills
parent: "Equipment"
group: "Utility"
description: "The Light and Heavy Drills: the battery-powered vehicle repair tools, with the Heavy Drill as the fastest repair on the list."
---

# Drills

| Drills | |
|---|---|
| ![Drills]({{ '/assets/img/icons/utility-3d/t_ui_icon_drill_medium.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Repair tool, specialist item |
| Repairs | Vehicles |
| Power | Batteries |
| **Use** | |
| Repair speed | Light: moderate. Heavy: fastest |
| Repair per application | 14.5 vehicle health (both) |
| Repair rate | Light 19.3 per second (every 0.75 s); Heavy 29 per second (every 0.5 s) |
| Battery use | 1 charge per use stored for both; actual S3 charging behavior unverified |
| **Availability** | |
| Price | 600 (Light), 1,300 cash (Heavy) |
| Unlock level | 1 (shop) |
| **Data** | |
| Internal name | `ID.Item.RepairTool.Drill.Light`, `ID.Item.RepairTool.Drill.Heavy` |
{: .wiki-infobox }

The Light and Heavy Drills are the battery-powered repair tools for vehicles. They repair faster than the [Wrench](wrench.md), but they need [Batteries](batteries.md) to work. The Heavy Drill is the fastest repair tool in the shop.

## Overview

The shop text says the Light Drill has a moderate repair speed and the Heavy Drill the fastest. Both require batteries. Both drills repair 14.5 vehicle health per application and draw the same battery use. The Heavy Drill applies its repair every 0.5 seconds and the Light Drill every 0.75 seconds, which is where the gap in speed comes from.

## How it works

- Using a drill repairs a vehicle. The use continues until the drill's power is spent or the vehicle is full.
- Earlier CL516586 analysis found no reader for the listed 1.25 battery use per second. The repair action spends 1 battery charge for each repair swing that lands (a Battery holds 100 charges, a High Capacity Battery 250). That historical code read cannot exclude a per-second drain in S3. The current battery and repair-action consumers must be traced before treating swing-only charging as current behavior. See [Batteries](batteries.md).
- Both have a reload action. It swaps in a fresh battery from the drill's single battery slot.
- Each drill has a melee value: 5 for the Light Drill and 10 for the Heavy Drill.
- The Light Drill repairs 14.5 health every 0.75 seconds (about 19.3 per second). The Heavy Drill repairs 14.5 health every 0.5 seconds (29 per second). The drills have no durability value.

| Drill | Price (cash) | Weight (kg) | Grid | Melee value |
|---|---:|---:|---|---:|
| Light Drill | 600 | 1.5 | 2 x 2 | 5 |
| Heavy Drill | 1,300 | 6.9 | 3 x 2 | 10 |

The S3 weight fields store 1.5 for the Light Drill and 6.9 for the Heavy Drill directly; these exports do not require division by 1,000.

## Season 2 changes

No Season 2 change to the drills is listed.

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
