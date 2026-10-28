---
title: "Dune Buggy"
parent: "Vehicles"
group: "Cars and trucks"
description: "Light three-seat buggy with a rear-biased drive and no weapons, sold for 1,500 cash."
---

# Dune Buggy

| Dune Buggy | |
|---|---|
| ![Dune Buggy]({{ '/assets/img/icons/vehicles/T_UI_Icon_Vehicle_DuneBuggy_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
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

**Steering and pedal tuning.** The data stores steer sensitivity 1.25, steer input gravity 2, throttle sensitivity 1.75 and brake sensitivity 1.25. Its steer-speed multiplier falls from 1.5 to 1 as the input rises. The game does not label the units. (see [Vehicle handling](vehicle-handling.md#driving-input-tuning) for how these settings work).

- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. The wheel data stores a radius, friction and brake value for each state. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- A new 125 mm rocket rule adds +250%.
- Rear brake torque fell from 16,000 to 13,000, and the second rear brake value fell from 12,000 to 9,000, so the rear brakes are weaker.
- The wheel deflation threshold rose from 0.5 to 0.55 on both axles.
- Price is unchanged at 1,500.

## Vehicle spawns

The Dune Buggy is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family, not each variant, so which variant appears in a slot is not in the data (inferred). A match offers it in 7 of the 7 ground yards on Ozeti, 5 or 6 of the 7 or 6 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. The data gives no vehicle count or respawn timer per yard. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Bobcat](bobcat.md), another light wheeled vehicle
- [Humvee](humvee.md), a heavier SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the wheeled steering and pedal tuning for this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
