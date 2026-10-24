---
title: "Refuel and Repair Stations"
parent: "Equipment"
group: "Emplacements and buildables"
description: "Two vehicle service stations built with the Large Hammer from 200 Build Supplies each, with 1,600 HP, one of each allowed per Forward Operating Base."
---

# Refuel and Repair Stations

| Refuel and Repair Stations | |
|---|---|
| **General** | |
| Category | Vehicle service station |
| Hammer | Large |
| **Building** | |
| Build cost | 200 Build Supplies each |
| Build time | Not yet known |
| Health | 1,600 HP each |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +50% |
| Rockets | +1,500% |
| C4 | +600% |
| IEDs | +1,000% (Repair Station); no single entry (Refuel Station) |
| Internal name | `DA_Buildable_RefuelStation`, `DA_Buildable_RepairStation` |
{: .wiki-infobox }

The Refuel Station and the Repair Station are vehicle service structures that only the Large Hammer can build. The Refuel Station uses Fuel Supplies and the Repair Station uses Mechanical Supplies. Each can be placed once per Forward Operating Base. They take much more rocket and C4 damage than most structures.

## Overview

Both stations cost 200 Build Supplies and have 1,600 HP. Neither has separate parts.

The Refuel Station works with Fuel Supplies, and the Repair Station works with Mechanical Supplies. The item text for each says it is needed to refuel or repair vehicles, and that it needs a friendly base radius to use. The data gives the Repair Station and the Refuel Station the same repair speed multiplier of 13.33. What that number does in play is not yet known.

The reward tables have no cash entry for either station.

## Building it

- **Cost:** 200 Build Supplies each.
- **Hammers:** Large only.
- **Limit:** One Refuel Station and one Repair Station per Forward Operating Base.
- **Placement:** Each must be inside a friendly Forward Operating Base radius. They also pass a ladder bounds check and a safe zone check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The Refuel Station has 15, 14, 27 and 14 weak spots in its first four stages. The Repair Station has 16, 16, 16 and 15. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

The data says the stations refuel and repair vehicles. The refuel and repair rates are not yet known, so how fast a vehicle is serviced is also not yet known. The Refuel Station has a refuel start and stop sound, and the Repair Station has a repair start and stop sound.

## Durability

| Source | Refuel Station | Repair Station |
|---|---:|---:|
| Bullets | -80% | -80% |
| Melee | -80% | -80% |
| Grenades | +50% | +50% |
| Rockets | +1,500% | +1,500% |
| C4 | +600% | +600% |
| IEDs | no single entry | +1,000% |

Rockets do 16 times their normal damage to either station. The Refuel Station has no single IED entry in the data, so the IED damage it takes is not yet known from this table. The data does not say how many hits either station takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Season 2 changes

The Season 2 data lists no change to either station's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Utility Items](utility-items.md): the Fuel Supplies and Mechanical Supplies that the stations use
- [Vehicle damage](../vehicles/vehicle-damage.md): how vehicles take damage, for the vehicles these stations serve

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, damage rows, placement limits, the repair multiplier and the item descriptions
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md): the names of the FOB supply containers, including Fuel Supplies and Mechanical Supplies
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
