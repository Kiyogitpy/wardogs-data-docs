---
title: "Dune Buggy"
parent: "Vehicles"
group: "Cars and trucks"
description: "Light three-seat buggy with a rear-biased drive and no weapons, sold for 1,500 cash."
---

# Dune Buggy

| Dune Buggy | |
|---|---|
| Type | Buggy (ATV) |
| Seats | 3 |
| Price | 1,500 cash |
| Unlock level | 0 |
| Main health | 400 HP |
| Top speed | 130 (as stored) |
| Rifle damage taken (derived) | 10% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-dunebuggy) |
| Internal name | WHL_06 |
{: .wiki-infobox }

The Dune Buggy is a light three-seat buggy with a mass of 550 and a top speed of 130. It is rear-wheel biased and has no weapons.

## Overview

The Dune Buggy is sold in the vehicle vendor under land transport, for 1,500 cash, and unlocks at level 0. Its shop description calls it a rapid three-seat wheeled vehicle.

## Stats

| Stat | Value |
|---|---|
| Max speed | 130 (as stored) |
| Fuel capacity | 68 (as stored) |
| Fuel economy | 5.0 (as stored) |
| Seats | 3 |
| Mass | 550 (as stored, unit not stated) |
| Countermeasures | Not stated |

## Armor and damage

Main health is 400 HP. The buggy has separate health for its engine (400 HP), fuel tank (300 HP) and each wheel (75 HP).

Rifle rounds do 10% of their damage against the hull, the highest share of any truck or SUV. The fuel tank takes an extra 200% from bullets.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 286 | 84 through the fuel tank |
| 7.62×54 mm rifle | 182 | 54 through the fuel tank |
| .308 Win | 324 | 95 through the fuel tank |
| .50 cal | 89 | 26 through the fuel tank |
| 20×102 mm cannon | 27 | None found |
| 30 mm cannon | 10 | None found |

## Weapons and seats

The Dune Buggy has no weapons. Its three seats are a driver and two passengers.

## Handling

- Driving assists: lean up to 15 degrees and pitch up to 20 degrees, with drift values of 1 at the front and 1 at the rear. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Mass 550, with hand brake 50 and front steering of 40 degrees.
- Torque split heavily toward the rear: 0.15 to the front and 0.85 to the rear.
- Engine idle 800 RPM, with a torque scale of 0.35.

## Season 2 changes

- A new 125 mm rocket rule adds +250%.
- Rear brake torque fell from 16,000 to 13,000, and the second rear brake value fell from 12,000 to 9,000, so the rear brakes are weaker.
- The wheel deflation threshold rose from 0.5 to 0.55 on both axles.
- Price is unchanged at 1,500.

## See also

- [Bobcat](bobcat.md), another light wheeled vehicle
- [Humvee](humvee.md), a heavier SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
