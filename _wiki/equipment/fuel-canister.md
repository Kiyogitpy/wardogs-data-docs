---
title: "40L Fuel Canister"
parent: "Equipment"
group: "Utility"
description: "The 40 L Fuel Canister: a 150 cash fuel can that refuels vehicles at about 2.7 fuel per second, with 40 durability."
---

# 40L Fuel Canister

| Fuel Canister | |
|---|---|
| ![40L Fuel Canister]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Utility_FuelCan_Textured_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Logistics, specialist item, vehicle fuel |
| Size | 40 L |
| Weight | 5 kg |
| Durability | 40 |
| **Use** | |
| Fuel per use | 25 (shop figure; see Overview) |
| Refuel rate | 2.0 every 0.75 s (about 2.7 per second) |
| Uses | Fill the can, or refuel a vehicle |
| **Availability** | |
| Price | 150 cash |
| Unlock level | 0 |
| **Data** | |
| Internal name | `Id.Item.FuelCan` (the 20 L version in the data is `ID_FuelCan_20L`) |
{: .wiki-infobox }

The 40 L Fuel Canister is the portable fuel supply for vehicles. It holds 40 L and can refuel a vehicle. The shop text says it is used for refueling vehicles.

## Overview

The canister is sold for 150 cash and has 40 durability. The shop lists 25 fuel per use, but that figure is not what the refuel action uses. The action adds 2.0 fuel every 0.75 seconds, about 2.7 per second. The game files also list a 20 L version. The Item Shop does not sell that version, and nothing else in the data hands it out: the 20 L item has no item name of its own (it carries only the generic item tag), so no shop row, loot table or starting kit can point at it. Players cannot get it in the game as shipped (inferred; it looks like an unfinished item).

## How it works

The canister has two uses, both of which continue until the canister is empty or the target is full.

- **Fill** adds fuel to the canister from a world refuel point, a fuel pump placed in the world. The pump charges cash for each step of fuel, at its price per litre. Pumps flagged as free in spawn areas do not charge in safe zones. The Refuel Station at a base does not fill canisters.
- **Refuel** adds fuel to a vehicle in 2.0 unit steps every 0.75 s, which is 2.67 units per second. A full 40 L can empties in about 15 s (derived). The 20 L version adds 1.0 every 1.5 s, about 30 s for a full can (derived), but players cannot obtain it (inferred).

Refueling stations at a Forward Operating Base use Fuel Supplies, which are described on the [Supplies](supplies.md) page.

## Season 2 changes

No Season 2 change to the Fuel Canister is listed.

## See also

- [Supplies](supplies.md), including Fuel Supplies
- [Utility Items](utility-items.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price, unlock level, shop text, weight, durability and fuel value
- [Item Actions](../../content/Wardogs_ItemActions_v1.md): the fill and refuel uses and the use-until-empty rule
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): fuel pump behaviour and the Fuel Canister's timed refuel step.
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Canister refuel step (2.0 per 0.75 s).
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
- [Round 59 open questions evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round59-open-questions.md): why the 20 L version cannot be obtained.
