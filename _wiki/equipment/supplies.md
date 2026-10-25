---
title: Supplies
parent: "Equipment"
group: "Utility"
description: "Ammo, Fuel, Mechanical and Build Supplies: the resources that rearm, refuel, repair and build at a Forward Operating Base, with their price per lot of 50."
---

# Supplies

| Supplies | |
|---|---|
| **General** | |
| Type | Logistics, resource |
| Stack | 50 per item |
| Weight | 0.02 to 0.03 each (unit not stated) |
| **Use** | |
| Ammo Supplies | Reloads buildable weapons |
| Fuel Supplies | Refuels vehicles at a Refuel Station |
| Mechanical Supplies | Repairs vehicles at a Repair Station |
| Build Supplies | Needed to build with a hammer |
| **Availability** | |
| Price | 10 cash per lot of 50 (all four) |
| Unlock level | 1 (shop data) |
| **Data** | |
| Internal name | `Id.Item.MunitionsSupplies`, `Id.Item.FuelSupplies`, `Id.Item.SparePartsSupplies`, `Id.Item.BuildToolSupply` |
{: .wiki-infobox }

Supplies are the resources that a Forward Operating Base (FOB) and its stations use. The three FOB supplies need the FOB radius to be used. Build Supplies are what [Hammers](hammers.md) spend to build structures.

## Overview

Each supply is sold in lots of 50 for 10 cash, which is 0.2 cash per unit. The lot is the purchase amount, and each item stacks to 50 in the inventory.

## How it works

| Supply | Used for | Where it is used |
|---|---|---|
| Ammo Supplies | Reloads buildable weapons. An MG Nest turns FOB ammo supplies into rounds when reloaded | Inside the FOB radius |
| Fuel Supplies | Refuels vehicles | At a Refuel Station, inside the FOB radius |
| Mechanical Supplies | Repairs vehicles | At a Repair Station, inside the FOB radius |
| Build Supplies | Builds all buildable structures, and pays for repairs | With any hammer, while building. Nothing is charged at placement |

The structures on the [Buildables](../../game-features/Wardogs_Buildables_v1.md) page each have a supply cost. That cost is the total Build Supplies the structure uses up, whichever hammer builds it. The supplies are used a little with each hit, so a finished structure has used its whole cost. Nothing is charged at placement, as far as the data shows.

Repairs use Build Supplies too, and any not needed are returned. Dismantling a structure gives no Build Supplies back, as far as the data shows. See [Buildables](buildables.md#repair-and-dismantle).

### Supply pallets

Pallets for the same four resources are sold by the vehicle Garage vendor, not the Item Shop. Each costs 400 cash. The shop text advises delivering them to the FOB, and says they are destroyed by high-speed impacts (about 90 m of free fall at most).

| Pallet | Price (cash) |
|---|---:|
| Build Supply Pallet | 400 |
| Ammo Supply Pallet | 400 |
| Fuel Supply Pallet | 400 |
| Mechanical Supply Pallet | 400 |

## Season 2 changes

No Season 2 change to the supplies is listed in the data.

## See also

- [Hammers](hammers.md), which spend Build Supplies
- [Fuel Canister](fuel-canister.md)
- [Wrench](wrench.md), for hand repairs without supplies
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): prices, lot size, unlock level, shop text, weights, and the pallet prices
- [Buildables](../../game-features/Wardogs_Buildables_v1.md): supply uses and Build Supplies rules
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the use rules for supplies
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
