---
title: "Kodiak [Pickup]"
parent: "Vehicles"
group: "Cars and trucks"
description: "Six-seat pickup version of the Kodiak SUV with no weapons, sold for 3,000 cash."
---

# Kodiak [Pickup]

| Kodiak [Pickup] | |
|---|---|
| ![Kodiak Pickup]({{ '/assets/img/icons/vehicles-3d/T_UI_Vehicle_Kodiak_Pickup.png' | relative_url }}){: .wiki-infobox-img } | |
| Type | Pickup |
| Seats | 6 (driver, three inside passengers and two in the bed) |
| Price | 3,000 cash |
| Unlock level | 0 |
| Main health | 400 HP |
| Top speed | 154 (as stored) |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-wheeled-patriot-kodiak/WHL_02_Pickup) |
| Internal name | WHL_02 (pickup variant) |
{: .wiki-infobox }

The Kodiak [Pickup] is the pickup version of the [Kodiak](kodiak.md). It has a larger seating layout, six seats in its vendor stats, and no weapons.

## Overview

The Kodiak [Pickup] is sold in the vehicle vendor under land transport, for 3,000 cash, and unlocks at level 0. Its shop description lists six seats.

## Stats

| Stat | Value |
|---|---|
| Max speed | 154 (as stored) |
| Fuel capacity | 50 (as stored) |
| Fuel economy | 2.9 (as stored) |
| Seats | 6 |
| Mass | 2,750 (as stored, unit not stated) |
| Countermeasures | Not stated |

The six seats are the driver, three passengers inside and two passengers in the bed. The two bed seats are exterior seats.

## Armor and damage

Main health is 400 HP, with the same engine, fuel tank and wheel health as the [Kodiak](kodiak.md). Its rifle protection and destruction counts are the same as the base Kodiak's:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 572 | 143 through the left front wheel |
| 7.62×54 mm rifle | 364 | 91 through the left front wheel |
| .308 Win | 712 | 178 through the left front wheel |
| .50 cal | 178 | 45 through the left front wheel |
| 20×102 mm cannon | 39 | None found |
| 30 mm cannon | 8 | None found |

## Weapons and seats

The pickup has no weapons. Its seats are the driver, three inside passengers and two in the bed.

## Handling

Handling matches the base Kodiak: mass 2,750, hand brake 50, front steering of 30 degrees, and the same engine and transmission.

**Steering and pedal tuning.** The pickup uses the same input set as the Kodiak, which is set to steer input gravity 2 and no other sensitivity values. The game does not label the units. (see [Vehicle handling](vehicle-handling.md#driving-input-tuning) for how these settings work).

- No steering sensitivity is set; the game default of 5.0 applies.
- **Tyre states.** Each tyre has three states: intact; damaged (deflated), at or below 55% of the wheel's health; and destroyed, at 0. Each state sets a wheel radius, friction and brake value. [Repair and vehicle parts](repair-and-vehicle-parts.md) covers what each state does.

## Season 2 changes

- The vehicle item changed size in inventory (height 4 to 3).
- The wheel deflation threshold rose from 0.5 to 0.55 on both axles.
- A new 125 mm rocket rule adds +250% to the Kodiak damage rules, which this variant shares.
- Price is unchanged at 3,000.

## Vehicle spawns

The Kodiak [Pickup] is placed by the ground vehicle yards of all four main maps: [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). The yards list the vehicle family (Kodiak, Kodiak [M249] and Kodiak [Pickup]), not each variant, so which variant appears in a slot is not known (inferred). A match offers it in all 7 ground yards on Ozeti, 6 or 7 of the 6 or 7 on Bakurani, 7 of 7 on Zestafona and 6 of 6 on Saburtulo. No vehicle count or respawn timer per yard is known. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Kodiak](kodiak.md), the base model
- [Kodiak [M249]](kodiak-m249.md), the machine gun variant
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
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and findings for this article
