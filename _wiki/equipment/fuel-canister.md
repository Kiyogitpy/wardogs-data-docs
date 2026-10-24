---
title: Fuel Canister
parent: "Equipment"
group: "Utility"
description: "The 40 L Fuel Canister: a 150 cash fuel can that refuels vehicles, with 40 durability and 25 fuel per use."
---

# Fuel Canister

| Fuel Canister | |
|---|---|
| **General** | |
| Type | Logistics, specialist item, vehicle fuel |
| Size | 40 L |
| Weight | 5 (unit not stated) |
| Durability | 40 |
| **Use** | |
| Fuel per use | 25 |
| Uses | Fill the can, or refuel a vehicle |
| **Availability** | |
| Price | 150 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `Id.Item.FuelCan` (the 20 L version in the data is `ID_FuelCan_20L`) |
{: .wiki-infobox }

The 40 L Fuel Canister is the portable fuel supply for vehicles. It holds 40 L and can refuel a vehicle. The shop text says it is used for refueling vehicles.

## Overview

The canister is sold for 150 cash and has 40 durability. Each use adds 25 fuel. The item data also lists a 20 L version. The Item Shop does not sell that version, so whether it can be obtained is not yet known.

## How it works

The item data gives the canister two uses, both of which continue until the canister is empty or the target is full.

- **Fill** adds fuel to the canister. The sources do not say where the fuel comes from, so that is not yet known.
- **Refuel** adds fuel to a vehicle.

Refueling stations at a Forward Operating Base use Fuel Supplies, which are described on the [Supplies](supplies.md) page.

## Season 2 changes

No Season 2 change to the Fuel Canister is listed in the data.

## See also

- [Supplies](supplies.md), including Fuel Supplies
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock level, shop text, weight, durability and fuel value
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the fill and refuel uses and the use-until-empty rule
