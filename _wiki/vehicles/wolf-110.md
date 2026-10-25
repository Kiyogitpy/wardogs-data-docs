---
title: "Wolf-110"
parent: "Vehicles"
group: "Cars and trucks"
description: "Four-seat SUV added in Season 2, with the strongest torque curve of the wheeled vehicles, sold for 2,200 cash."
---

# Wolf-110

| Wolf-110 | |
|---|---|
| Type | SUV |
| Seats | 4 (driver and 3 passengers) |
| Price | 2,200 cash |
| Unlock level | 0 |
| Main health | 500 HP |
| Top speed | 129 (as stored) |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-whl-08-default) |
| Internal name | WHL_08 (default variant) |
{: .wiki-infobox }

The Wolf-110 is a four-seat SUV added in Season 2. It has no weapons. Its engine has the largest torque curve of the wheeled vehicles in the data.

## Overview

The Wolf-110 is sold in the vehicle vendor under land transport, for 2,200 cash, and unlocks at level 0. It was added in Season 2. Its ring-turret version is the [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md).

## Stats

| Stat | Value |
|---|---|
| Max speed | 129 (as stored) |
| Fuel capacity | 60 (as stored) |
| Fuel economy | 4.0 (as stored) |
| Seats | 4 |
| Mass | 3,200 (as stored, unit not stated) |
| Countermeasures | Not stated |

## Armor and damage

Main health is 500 HP. The Wolf-110 has separate health for its engine (400 HP) and fuel tank (400 HP). The data does not give health pools for its wheels.

Rifle rounds do 5% of their damage against the hull. Hits to a wheel can destroy the vehicle faster than hits to the body.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 715 | 204 through the left front wheel |
| 7.62×54 mm rifle | 455 | 130 through the left front wheel |
| .308 Win | 889 | 254 through the left front wheel |
| .50 cal | 223 | 63 through the left front wheel |
| 20×102 mm cannon | 53 | None found |
| 30 mm cannon | 13 | None found |

## Weapons and seats

The Wolf-110 has no weapons. Its four seats are a driver and three active passengers.

## Handling

- Driving assists: anti-roll 40 on both axles and a full-recovery speed of 120, the same as the Humvee. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Mass 3,200, hand brake 80, ABS 40 with a minimum speed of 22, and traction control 55, as stored.
- Front steering of 35 degrees.
- Torque split of 0.3 to the front and 0.7 to the rear.
- Torque peak of 1,500 at 1,650 RPM, the largest of the wheeled vehicles' torque curves in the data.
- Engine idle 700 RPM.

**Steering and pedal tuning.** The data stores steer input gravity 2.6, throttle sensitivity 1.5 and brake sensitivity 6.5, and the brake reaches full at a tenth of pedal travel. The game does not label the units. (see [Vehicle handling](vehicle-handling.md#driving-input-tuning) for how these settings work).

- Steering sensitivity is not stored; the game default of 5.0 applies.
- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. The wheel data stores a radius, friction and brake value for each state. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- Added in Season 2 with a price of 2,200 cash.
- Its own torque curve, braking and clutch curves, and collision damage curves were added in Season 2.

## See also

- [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md), the ring-turret version
- [Humvee](humvee.md) and [Kodiak](kodiak.md), similar SUVs
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
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
