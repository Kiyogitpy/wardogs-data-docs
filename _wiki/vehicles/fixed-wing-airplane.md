---
title: "Fixed-wing airplane"
parent: "Vehicles"
group: "Aircraft"
description: "An unfinished two-seat airplane: it has a flight model but no damage zones, no shop listing, no name and no yard that places it."
---

# Fixed-wing airplane

| Fixed-wing airplane | |
|---|---|
| Type | Airplane |
| Seats | 2 (driver and one passenger seat) |
| Price | Not sold (no shop listing) |
| Unlock level | Not applicable |
| Main health | 150 HP listed, but hits cannot damage it |
| Top speed | Not stored (see Handling) |
| Mass | 10,000 kg |
| Rifle damage taken (derived) | 7.5% |
| Internal name | FWG_01 |
{: .wiki-infobox }

The fixed-wing airplane is the only fixed-wing aircraft in the data, and it looks like an unfinished vehicle. It has a full flight model with control surfaces, flaps, an airbrake and retractable landing gear, but no name, no shop listing, no unlock, no damage zones and no yard that places it. This article describes it by what it is.

## Overview

The airplane has two seats, a driver and one passenger. Its model still uses placeholder materials from a real-world jet. It was built far enough to fly, but the parts a player would meet in a match were never set up: nobody can buy or unlock it, it has no entry in the vehicle lists or kill rewards, and the data does not show whether a match ever places one.

## Stats

| Stat | Value |
|---|---|
| Max speed | Not stored (see Handling) |
| Fuel | Fuel tank and fuel-leak effects (see below) |
| Seats | 2 |
| Mass | 10,000 kg |
| Max engine thrust | 226,800 N |
| Countermeasures | Flares, 3 starting, active for 3.5 s |

## Armor and damage

The airplane lists 150 HP at start. The data gives threshold triggers on its main health at 90% and on its fuel tank at 90%, 50% and 0%. The fuel tank has three fuel-leak effects of 0.1, 0.4 and 0.5 per second. The leaks pair with the tank thresholds in order: 0.1 per second below 90%, 0.4 below 50% and 0.5 at 0%.

Every other armed or armored vehicle splits its body into damage zones, such as the hull, engine and fuel tank. The airplane has none: no zones and no hit boxes on its model. A bullet, rocket or explosion that hits it finds no zone to damage, so the data gives it no way to lose health from enemy fire. The 150 HP and the thresholds therefore have nothing feeding them, and no hit counts are listed. Its damage rules are copied from the Little Bird family (rifle rounds would do 7.5% of their damage), but with no zones they never apply.

Several weapons still list it as a valid lock-on target: the 9K333 Verba launcher and five emplaced weapons.

## Weapons and seats

The airplane has no weapons. It has two seats: a driver seat and an active passenger seat.

## Handling

- The data stores no top speed. The airplane's speed comes from its engine thrust (226,800 N), its mass (10,000 kg) and drag, not from a speed limit.
- The auto-trim table, which says what pitch trim the airplane needs at each speed, holds level flight at about 140 km/h at 10% throttle and about 430 km/h at full throttle, in the rows the data names for the first gear setting. Both are read from the auto-trim table, not stored as a speed limit.

- Control surfaces: elevators up to 40 degrees each, ailerons and rudders up to 20 degrees, flaps up to 18 degrees, and an airbrake that can extend.
- Retractable landing gear, with a nose wheel that steers up to 45 degrees.
- Main lift multiplier 0.4.
- Translational lift of 20% between 24 and 34 m/s.
- Max angular velocity limit is switched off in the data. The 83 deg/s value is stored but inactive.
- Ground effect strength is 0%, so it has no effect.

## Season 2 changes

- One health-threshold flag in its gameplay settings changed from true to false, and the export does not say what that flag controls.
- The flares button is renamed Fire Countermeasures. The key is the same (V on keyboard).

## Vehicle spawns

The airplane falls under the same general air tag as the helicopters. 20 of the 21 air vehicle yards accept any air vehicle, so their rules would allow it, while the ground and light yards list it as excluded. No yard and no map file names it, so the game files cannot show whether any build ever placed it. See [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md).

## See also

- [Vehicle damage](vehicle-damage.md)
- [MH-6](mh-6.md), which shares its damage rules
- [Vehicles](../vehicles.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [Vehicles (reference)](../../content/Wardogs_Vehicles_v2.md)
- [Fixed-wing flight model](../../game-features/Wardogs_FixedWingFlightModel_v1.md): curves, auto-trim table and the speed figures read from it
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the body mass of the airplane, in kilograms
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the airplane mass override value
- [Round 53 fixed-wing evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round53-fixed-wing.md): no damage zones, no shop or unlock, yard rules, lock-on lists
