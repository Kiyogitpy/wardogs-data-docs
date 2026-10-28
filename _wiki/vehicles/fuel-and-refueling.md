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
| Refuel rate | Refuel Station: Fast 5% in 3 s, Max up to 100% in 9 s. Canister: 2.0 units per 0.75 s |
{: .wiki-infobox }

Every driven vehicle has a fuel tank with a capacity and a fuel economy number. The vendor labels the economy number "L/KM", litres per kilometre, so a higher number means the vehicle burns more fuel for each kilometre. The capacity is labelled "L", litres. This article shows both numbers as the vendor lists them. The fuel tank also has its own health, which is covered in [Repair and vehicle parts](repair-and-vehicle-parts.md).

## Overview

A vehicle's fuel is set by its vendor stats. Fuel is refilled in three ways: a [40L Fuel Canister](../equipment/fuel-canister.md) carried by a player, a [Refuel Station](../building/refuel-and-repair-stations.md) built inside a Forward Operating Base, or [Fuel Supplies](../equipment/supplies.md) delivered to that station.

## How it works

### Running out of fuel

When a vehicle's fuel reaches zero, the server stops its engine. A stopped engine cannot be restarted while the tank is empty, so refuel first. This comes from a static reading of the start check (the game was not run to test it): the check passes only once the tank holds fuel again.

### How fuel is used up

The tank drains only while the engine is running, and the game works it out on the host or server, not on each player's PC. Driving at speed, the drain is the speed in km/h divided by 3,600 and by the vehicle's kilometres-per-litre figure, in litres per second. When a car or truck is stopped or crawling at 1 km/h or less, the drain switches to the engine speed (RPM) divided by 3,600 and by a second figure per vehicle, so an idling engine still burns a little. Tracked vehicles and the airplane use no fuel while stopped or crawling at 1 km/h or less. A leak drains fuel even with the engine off. This is a static reading of the code; the game was not run to test it.

### Fuel leaks

Fuel tank damage makes the tank leak fuel, and the leak rate steps up as the tank loses health. On the fixed-wing airplane the tank leaks 0.1 per second below 90 percent tank health, 0.4 per second below 50 percent and 0.5 per second when the tank is destroyed. Other vehicles use their own steps. The heavy tanks reach 3.0 per second when destroyed, and the MH-6 and AH-6 family leak 0.1 per second below 10 percent and 0.75 per second when destroyed.

Most vehicles set their first leak step at 90 or 80 percent of fuel tank health, a second at 50 or 55 percent and a third at 0 percent when the tank is destroyed. The fuel tank also takes extra damage from some weapons, as explained in [Vehicle damage](vehicle-damage.md).

### Refueling

- **Fuel Canister.** A 40L Fuel Canister costs 150 cash and has 40 durability. The shop's 25 fuel per use is not what the refuel action uses. The action adds 2.0 fuel every 0.75 s. It is used until the can is empty or the vehicle is full. Canisters are filled for cash at world refuel points, see [Fuel Canister](../equipment/fuel-canister.md).
- **Refuel Station.** Built with the Large Hammer for 200 Build Supplies, with 1,600 HP. Only one can stand in each Forward Operating Base. It takes Fuel Supplies and must be inside the FOB radius to be used.
- **Fuel Supplies.** Sold for 10 cash per lot of 50. A Fuel Supply Pallet costs 400 cash. The Refuel Station needs them to work.
- **Refuel at base.** The in-game tip says vehicles can be refuelled by returning to your faction's safe zone or a FOB, and that this is not free.

The Refuel Station has a Fast and a Max restock. Fast restocks 5% of the tank in 3 s for 75 cash. Max restocks up to a full tank in 9 s. A Max restock charges only for what the tank receives: the listed cash cost is scaled by the share of the tank restored and rounded up to a multiple of 50 (1,500 cash for a full tank), and the Fuel Supplies used are the item's cost times the amount restored. A nearly full tank costs little, though the restock most likely still takes its full 9 s (inferred), and a restock cannot give more fuel than the FOB has in stock. The [Refuel and Repair Stations](../building/refuel-and-repair-stations.md) page has the full figures. A vehicle with an empty tank has its engine stopped, as described above.

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
| [Fixed-wing airplane](fixed-wing-airplane.md) | No stats sheet in the data | No stats sheet in the data |
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

A higher fuel economy number means more fuel used per kilometre, which is worse (the vendor label is litres per kilometre). It equals one divided by the vehicle's kilometres-per-litre figure, so the range on a full tank is capacity times that figure: about 19.5 km for the Humvee and 29 km for the Havoc (derived). Driving burns fuel in proportion to speed; see [Vehicle Config Fields](../../game-features/Wardogs_VehicleConfigFields_v1.md#5-fuel-settings-fuelsettings-in-each-gameplaysystems-asset). The tracked and heavy vehicles have the highest numbers and the Bobcat the lowest. The number is the vendor's listed stat; how the engine itself spends fuel in play was not traced. The fixed-wing airplane has no vendor stats.

Season 2 changed no fuel capacity or fuel economy value.

## Tips that follow from the numbers

- The Bobcat has the smallest capacity, 18. One Fuel Canister use adds 25, so one use is more than its whole tank, if the two use the same unit.
- The Flakpanzer Gepard has the highest fuel economy number, 10.0, which means the thirstiest listed use of fuel per kilometre. Plan fuel from the vehicle's own article, not from this column alone.
- The fuel tank is also a weak point for attackers. On the Humvee, bullets to the fuel tank take an extra 400%, so it is the fastest route to destroy that vehicle. See [Vehicle damage](vehicle-damage.md).

## See also

- [Repair and vehicle parts](repair-and-vehicle-parts.md): fuel tank and other part health, and repairing
- [Vehicle damage](vehicle-damage.md): how hits reach the fuel tank
- [Fuel Canister](../equipment/fuel-canister.md) and [Refuel and Repair Stations](../building/refuel-and-repair-stations.md)
- [Supplies](../equipment/supplies.md): Fuel Supplies and Mechanical Supplies

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles Reference](../../content/Wardogs_Vehicles_v2.md): the airplane's fuel leak and threshold settings
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md): vendor stats and fuel health triggers
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Buildables](../../game-features/Wardogs_Buildables_v1.md): the Refuel Station and its supplies
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md): Fuel Canister and supply prices
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): Refuel Station restock rates and the Fuel Canister's timed refuel step.
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Empty-tank engine stop, fuel leak steps and canister refuel rate.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the empty-tank restart block and the Refuel Max charge rule.
