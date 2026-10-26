---
title: "Kodiak"
parent: "Vehicles"
group: "Cars and trucks"
description: "Four-seat SUV with a driver and three passengers and no weapons, the base model of the Kodiak family."
---

# Kodiak

| Kodiak | |
|---|---|
| ![Kodiak]({{ '/assets/img/icons/vehicles-3d/T_UI_Vehicle_Kodiak_Default.png' | relative_url }}){: .wiki-infobox-img } | |
| Type | SUV |
| Seats | 4 (driver and 3 passengers) |
| Price | 2,500 cash |
| Unlock level | 0 |
| Main health | 400 HP |
| Top speed | 154 (as stored) |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-patriot-kodiak) |
| Internal name | WHL_02 (default variant) |
{: .wiki-infobox }

The Kodiak is a four-seat SUV with no weapons. It is the base model of the Kodiak family, which also includes the [Kodiak [Pickup]](kodiak-pickup.md) and the [Kodiak [M249]](kodiak-m249.md).

## Overview

The Kodiak is sold in the vehicle vendor under land transport, for 2,500 cash, and unlocks at level 0. Its shop description lists four seats and optional logistics crates.

## Stats

| Stat | Value |
|---|---|
| Max speed | 154 (as stored) |
| Fuel capacity | 50 (as stored) |
| Fuel economy | 2.9 (as stored) |
| Seats | 4 |
| Mass | 2,750 (as stored, unit not stated) |
| Countermeasures | Not stated |

## Armor and damage

Main health is 400 HP. The Kodiak has separate health for its engine (400 HP), fuel tank (400 HP) and each wheel (75 HP).

Rifle rounds do 5% of their damage against the hull. Bullets that hit a wheel can destroy the vehicle faster than hits to the body.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 572 | 143 through the left front wheel |
| 7.62×54 mm rifle | 364 | 91 through the left front wheel |
| .308 Win | 712 | 178 through the left front wheel |
| .50 cal | 178 | 45 through the left front wheel |
| 20×102 mm cannon | 39 | None found |
| 30 mm cannon | 8 | None found |

## Weapons and seats

The Kodiak has no weapons. It has four seats: a driver and three active passengers.

## Handling

- Driving assists: a drift assist with 5 at the front and 60 at the rear, and a full-recovery speed of 200. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Mass 2,750, hand brake 50, and front steering of 30 degrees.
- ABS 30 with a minimum speed of 35, and traction control 55, as stored.
- Engine torque curve runs from 0 to 9,000 RPM, with a torque scale of 0.6, as stored.

**Steering and pedal tuning.** The data stores steer input gravity 2 and no other sensitivity values for this input set. The game does not label the units. (see [Vehicle handling](vehicle-handling.md#driving-input-tuning) for how these settings work).

- Idle RPM is not stored; the game default of 1,000 applies. Steering sensitivity is not stored either; the game default of 5.0 applies.
- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. The wheel data stores a radius, friction and brake value for each state. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- The wheel deflation threshold rose from 0.5 to 0.55 on the front and rear axles.
- A new 125 mm rocket rule adds +250%.
- The vehicle item changed size in inventory (height 4 to 3).
- Price is unchanged at 2,500.

## Vehicle spawns

The Kodiak is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family (Kodiak, Kodiak [M249] and Kodiak [Pickup]), not each variant, so which variant appears in a slot is not in the data (inferred). A match offers it in all 7 ground yards on Ozeti, 6 or 7 of the 6 or 7 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. The data gives no vehicle count or respawn timer per yard. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Kodiak [Pickup]](kodiak-pickup.md) and [Kodiak [M249]](kodiak-m249.md), the variants
- [Humvee](humvee.md), a larger SUV
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the wheeled steering and pedal tuning for this vehicle
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
