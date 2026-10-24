---
title: "Fuel and refueling"
parent: "Vehicles"
group: "Reference"
description: "How much fuel each vehicle carries, how its fuel economy is listed, how a fuel tank gets hit, and how to refuel with a Fuel Canister, a Refuel Station or Fuel Supplies."
---

# Fuel and refueling

| Fuel and refueling | |
|---|---|
| **General** | |
| Type | Mechanic |
| Applies to | Every player vehicle with a fuel tank |
| Refuel options | Fuel Canister, Refuel Station |
| **Data** | |
| Fuel unit | Not labelled in the data (shown as stored) |
| Refuel rate | Not yet known |
{: .wiki-infobox }

Every driven vehicle has a fuel tank with a stored capacity and a stored fuel economy number. The data does not label the units, so this article shows them as stored and does not convert them to litres or kilometres. The fuel tank also has its own health, which is covered in [Repair and vehicle parts](repair-and-vehicle-parts.md).

## Overview

A vehicle's fuel is set by its vendor stats. Fuel is refilled in three ways: a [40L Fuel Canister](../equipment/fuel-canister.md) carried by a player, a [Refuel Station](../equipment/refuel-and-repair-stations.md) built inside a Forward Operating Base, or [Fuel Supplies](../equipment/supplies.md) delivered to that station.

## How it works

### Running out of fuel

The data does not say what happens when a vehicle's fuel reaches zero, such as whether the engine stops or how quickly. That is not yet known.

### Fuel leaks

The fuel tank has its own health and effect triggers. On the fixed-wing airplane, the fuel tank has three leak effects of 0.1, 0.4 and 0.5 per second. The data does not say which health threshold uses which leak rate. Other vehicles' fuel leak effects are not decoded in the data.

Fuel tank health triggers sit at 90% (and 80%), 55% and 0% on several vehicles, and at 10% and 0% on the Little Bird family. What each trigger does is not fully decoded. The fuel tank also takes extra damage from some weapons, as explained in [Vehicle damage](vehicle-damage.md).

### Refueling

- **Fuel Canister.** A 40L Fuel Canister costs 150 cash and has 40 durability. Each use adds 25 fuel. It is used until the can is empty or the vehicle is full.
- **Refuel Station.** Built with the Large Hammer for 200 Build Supplies, with 1,600 HP. Only one can stand in each Forward Operating Base. It takes Fuel Supplies and must be inside the FOB radius to be used.
- **Fuel Supplies.** Sold for 10 cash per lot of 50. A Fuel Supply Pallet costs 400 cash. The Refuel Station needs them to work.
- **Refuel at base.** The in-game tip says vehicles can be refuelled by returning to your faction's safe zone or a FOB, and that this is not free.

The refuel rate of the Refuel Station is not in the data, so how long a refill takes is not yet known.

## Numbers

Fuel capacity and fuel economy for every drivable vehicle, from the vendor stats. Sort by either column with the header.

| Vehicle | Fuel capacity (as stored) | Fuel economy (as stored) |
|---|---:|---:|
| [Havoc](havoc.md) | 130 | 4.4 |
| [MH-6](mh-6.md) | 105 | 4.4 |
| [AH-6M [Miniguns]](ah-6m-miniguns.md) | 105 | 4.4 |
| [AH-6R [Rockets]](ah-6r-rockets.md) | 105 | 4.4 |
| [Z20 Lakota](z20-lakota.md) | 120 | 4.4 |
| [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md) | 120 | 4.4 |
| [Fixed-wing airplane](fixed-wing-airplane.md) | Not yet known | Not yet known |
| [SPH-2](sph-2.md) | 105 | 8.0 |
| [L2A6](l2a6.md) | 110 | 8.0 |
| [Flakpanzer Gepard](flakpanzer-gepard.md) | 110 | 10.0 |
| [T-72B3](t-72b3.md) | 110 | 8.5 |
| [M113 APC SV](m113-apc-sv.md) | 100 | 5.7 |
| [Bobcat](bobcat.md) | 18 | 2.2 |
| [Kodiak](kodiak.md) | 50 | 2.9 |
| [Kodiak [Pickup]](kodiak-pickup.md) | 50 | 2.9 |
| [Kodiak [M249]](kodiak-m249.md) | 50 | 2.9 |
| [Humvee](humvee.md) | 65 | 3.3 |
| [Humvee [Minigun]](humvee-minigun.md) | 65 | 3.3 |
| [Humvee [M249]](humvee-m249.md) | 65 | 3.3 |
| [Dune Buggy](dune-buggy.md) | 68 | 5.0 |
| [Ural](ural.md) | 85 | 4.0 |
| [Ural Defender](ural-defender.md) | 85 | 4.0 |
| [Ural Defender [M249]](ural-defender-m249.md) | 85 | 4.0 |
| [Wolf-110](wolf-110.md) | 60 | 4.0 |
| [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md) | 60 | 4.0 |

The data does not say whether a higher fuel economy number means better or worse fuel use, so the table does not rank vehicles on it. The fixed-wing airplane has no stats sheet in the data.

Season 2 changed no fuel capacity or fuel economy value in the data.

## Tips that follow from the numbers

- The Bobcat has the smallest stored capacity, 18. One Fuel Canister use adds 25, so one use is more than its whole tank, if the two use the same stored unit.
- The Flakpanzer Gepard has the highest fuel economy number, 10.0, but the data does not say which way is better. Plan fuel from the vehicle's own article, not from this column alone.
- The fuel tank is also a weak point for attackers. On the Humvee, bullets to the fuel tank take an extra 400%, so it is the fastest route to destroy that vehicle. See [Vehicle damage](vehicle-damage.md).

## See also

- [Repair and vehicle parts](repair-and-vehicle-parts.md): fuel tank and other part health, and repairing
- [Vehicle damage](vehicle-damage.md): how hits reach the fuel tank
- [Fuel Canister](../equipment/fuel-canister.md) and [Refuel and Repair Stations](../equipment/refuel-and-repair-stations.md)
- [Supplies](../equipment/supplies.md): Fuel Supplies and Mechanical Supplies

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles Reference](../../content/Wardogs_Vehicles_v2.md): the airplane's fuel leak and threshold data
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md): vendor stats and fuel health triggers
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Buildables](../../game-features/Wardogs_Buildables_v1.md): the Refuel Station and its supplies
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md): Fuel Canister and supply prices
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
