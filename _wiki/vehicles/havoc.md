---
title: "Havoc"
parent: "Vehicles"
group: "Helicopters"
description: "Two-seat attack helicopter with a 30 mm autocannon and B-13 rocket pods, the most expensive air vehicle in the shop."
---

# Havoc

| Havoc | |
|---|---|
| Type | Combat helicopter |
| Seats | 2 (pilot and gunner) |
| Price | 28,000 cash |
| Unlock level | 0 |
| Main health | 800 HP |
| Top speed | 400 (as stored) |
| Mass | 7,500 kg |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#air-rotary-havoc) |
| Internal name | ROT_02 |
{: .wiki-infobox }

The Havoc is a two-seat attack helicopter. It carries a 30 mm autocannon and a pair of B-13 rocket pods, and it is the most expensive air vehicle in the vehicle vendor at 28,000 cash.

## Overview

The Havoc is listed in the vehicle vendor under air combat. The pilot flies it and the gunner works the weapons. It has flares for countermeasures.

## Stats

| Stat | Value |
|---|---|
| Max speed | 400 (as stored) |
| Fuel capacity | 130 (as stored) |
| Fuel economy | 4.4 (as stored) |
| Seats | 2 |
| Mass | 7,500 kg |
| Countermeasures | Flares |

## Armor and damage

Main health is 800 HP. The helicopter also has separate health for each of these parts:

| Part | Health (HP) |
|---|---:|
| Engine | 200 |
| Fuel tank | 200 |
| Main rotor | 400 |
| Tail rotor | 300 |
| Front landing wheels (each) | 100 |

Rifle rounds do 5% of their damage against the hull. A round that hits the fuel tank gets an extra 300% on top of that, so it does about a fifth of its full damage. Rocket blasts that burst within the inner radius are multiplied by five.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 1,143 | 643 through the left front wheel |
| 7.62×54 mm rifle | 728 | 410 through the left front wheel |
| .308 Win | 2,371 | 1,334 through the left front wheel |
| .50 cal | 356 | 200 through the left front wheel |
| 20×102 mm cannon | 182 | None found |
| 30 mm cannon | 42 | None found |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| 2A42 Autocannon (30 mm) | Cannon | 250 rounds/min | 600 m | 8.0 s | None |
| B-13 Rocket Pods (122 mm) | Rockets | 500 rounds/min | 1,000 m | 6.0 s | None |

The seats are a driver (pilot) seat and one gunner seat.

## Handling

- Driving assists: the climb rate is limited to 36 km/h, the collective holds a hover when released, and the pitch and roll level out at low speed. Four assists are stored as switched off: the sink-rate limit, the yaw reset on the ground, the roll drag-overshoot prevention and the roll damping. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Rotor radius 600, maximum lift coefficient 1.8, and stall angle 40 degrees, as stored.
- Translational lift of 20% between 24 and 34 m/s.
- Maximum angular velocity 83 deg/s.
- Ground effect falloff 12 m. No ground-effect strength is stored for this helicopter.

## Season 2 changes

- Price rose from 18,000 to 28,000 cash.
- The 35×228 mm cannon rule changed from +87.5% to -46%, so cannon hits from that calibre now do less damage.
- A new 125 mm rocket rule adds +150%.
- The vehicle item is one step wider in inventory (width 4 to 5).
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## See also

- [Vehicle damage](vehicle-damage.md)
- [MH-6](mh-6.md), [AH-6M [Miniguns]](ah-6m-miniguns.md) and [AH-6R [Rockets]](ah-6r-rockets.md), the smaller Little Bird family helicopters
- [Vehicles](../vehicles.md)

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the body mass of this aircraft, in kilograms
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the airplane and helicopter mass override values
