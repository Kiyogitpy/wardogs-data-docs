---
title: "Z20 Lakota"
parent: "Vehicles"
group: "Helicopters"
description: "Large 13-seat transport helicopter with no weapons, the helicopter with the most seats in the vehicle vendor."
---

# Z20 Lakota

| Z20 Lakota | |
|---|---|
| Type | Transport helicopter |
| Seats | 13 |
| Price | 7,400 cash |
| Unlock level | 0 |
| Main health | 600 HP |
| Top speed | 445 (as stored) |
| Mass | 9,500 kg |
| Rifle damage taken (derived) | 5% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#air-rotary-rot-04) |
| Internal name | ROT_04 (default variant) |
{: .wiki-infobox }

The Z20 Lakota is a large transport helicopter with 13 seats and no weapons. It has the most seats of any helicopter in the vehicle vendor, and it unlocks at level 0.

## Overview

The Z20 Lakota is sold in the vehicle vendor under air transport, for 7,400 cash. Its armed version is the [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md), which shares its airframe.

## Stats

| Stat | Value |
|---|---|
| Max speed | 445 (as stored) |
| Fuel capacity | 120 (as stored) |
| Fuel economy | 4.4 (as stored) |
| Seats | 13 |
| Mass | 9,500 kg |
| Countermeasures | Flares |

## Armor and damage

Main health is 600 HP. The helicopter has separate health for its engine (200 HP), fuel tank (200 HP), main rotor (400 HP) and tail rotor (300 HP).

Rifle rounds do 5% of their damage against the hull. The tail rotor is the weak point. Rifle fire destroys the helicopter after 858 hits to the body, or after 429 hits through the tail rotor.

Hits needed to destroy the main health. These counts are derived by simulating the damage rules with full-power, point-blank, standard (FMJ) hits; they are estimates from the data, not measured in game:

| Ammunition | Hits to destroy | Faster route |
|---|---:|---|
| 5.56 mm rifle | 858 | 429 through the tail rotor |
| 7.62×54 mm rifle | 546 | 273 through the tail rotor |
| .308 Win | 1,334 | 667 through the tail rotor |
| .50 cal | 267 | 134 through the tail rotor |
| 20×102 mm cannon | 167 | None found |
| 30 mm cannon | 24 | None found |

## Weapons and seats

The Z20 Lakota has no weapons. The seat with the pilot is labelled "Pilot". The data gives 13 seats on the stats sheet. The shop description says 11 passengers, which is one fewer than the 13 seats of the stats sheet.

## Handling

- Driving assists: the climb rate is limited to 36 km/h and the collective holds a hover when released; the collective resets to minus 1 on the ground. See [Vehicle handling](vehicle-handling.md#driving-and-flight-assists).

- Rotor radius 800, maximum lift coefficient 5.75, and translational lift of 25% between 24 and 34 m/s, as stored.
- Ground effect strength 30% with a 12 m falloff.
- The main rotor's operating RPM is 270 and its critical low RPM is 180.
- Maximum angular velocity 83 deg/s.

## Season 2 changes

- Price is unchanged at 7,400.
- The 35×228 mm cannon rule changed from -40% to -57.25%.
- A new 125 mm rocket rule adds +150%.
- The vehicle item is one step wider in inventory (width 4 to 5).
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## See also

- [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md), the armed version
- [Havoc](havoc.md) and [MH-6](mh-6.md), the other helicopters
- [Vehicle damage](vehicle-damage.md)

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the body mass of this aircraft, in kilograms
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the airplane and helicopter mass override values
