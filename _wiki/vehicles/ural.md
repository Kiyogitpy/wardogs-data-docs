---
title: "Ural"
parent: "Vehicles"
group: "Cars and trucks"
description: "Heavy three-seat truck with no weapons and the heaviest mass of the wheeled vehicles, sold for 5,000 cash."
---

# Ural

| Ural | |
|---|---|
| Type | Truck |
| Seats | 3 |
| Price | 5,000 cash |
| Unlock level | 0 |
| Main health | 700 HP |
| Top speed | 79 (as stored) |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-ural/WHL_07_Default) |
| Internal name | WHL_07 (default variant) |
{: .wiki-infobox }

The Ural is a large truck with a mass of 10,000, the heaviest wheeled vehicle in the data. It has six wheels, a three-seat cab and no weapons. It is the base model of the Ural family, which also includes the [Ural Defender](ural-defender.md) and the [Ural Defender [M249]](ural-defender-m249.md).

## Overview

The Ural is sold in the vehicle vendor under land transport, for 5,000 cash, and unlocks at level 0. Its shop description calls it a large multi-capacity wheeled transport vehicle.

## Stats

| Stat | Value |
|---|---|
| Max speed | 79 (as stored) |
| Fuel capacity | 85 (as stored) |
| Fuel economy | 4.0 (as stored) |
| Seats | 3 |
| Mass | 10,000 (as stored, unit not stated) |
| Countermeasures | Not stated |

## Armor and damage

Main health is 700 HP. The Ural has separate health for its engine (400 HP), fuel tank (400 HP) and each of its six wheels (75 HP).

Rifle rounds do 5% of their damage against the hull. The fuel tank takes an extra 350% from bullets.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 1,000 | 175 through the fuel tank |
| 7.62×54 mm rifle | 637 | 112 through the fuel tank |
| .308 Win | 1,778 | 311 through the fuel tank |
| .50 cal | 312 | 55 through the fuel tank |
| 20×102 mm cannon | 94 | None found |
| 30 mm cannon | 12 | None found |

## Weapons and seats

The Ural has no weapons. Its three seats are a driver and two passengers.

## Handling

- Driving assists: drift values of 2.5 at the front and 30 at the rear. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Mass 10,000, hand brake 50, ABS 15 with a minimum speed of 35, and traction control 45, as stored.
- Front steering of 30 degrees.
- Six-speed gearbox with a first gear ratio of 5.62, the longest first gear of the wheeled vehicles.
- Torque peak 900 at 1,200 RPM, with a torque scale of 2.0 and an idle of 650 RPM.

**Steering and pedal tuning.** The data stores steer input gravity 2 and throttle sensitivity 1. Its steer-speed multiplier falls from 1.4 to 0.5 as the input rises. The game does not label the units. (see [Vehicle handling](vehicle-handling.md#driving-input-tuning) for how these settings work).

- Steering sensitivity is not stored; the game default of 5.0 applies.
- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. The wheel data stores a radius, friction and brake value for each state. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- The 35×228 mm cannon rule changed from -65% to -87.5%, so cannon hits from that calibre now do less damage.
- A new 125 mm rocket rule adds +75%.
- The wheel deflation threshold rose from 0.5 to 0.55 on the front, middle and rear axles.
- Price is unchanged at 5,000.

## See also

- [Ural Defender](ural-defender.md) and [Ural Defender [M249]](ural-defender-m249.md), the armored variants
- [Humvee](humvee.md), a lighter SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the wheeled steering and pedal tuning for this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
