---
title: "SPH-2"
parent: "Vehicles"
group: "Armored vehicles"
description: "Tracked artillery vehicle that fires 155 mm shells from a long-range turret, with a camera that follows the shell in flight."
---

# SPH-2

| SPH-2 | |
|---|---|
| **General** | |
| Type | Artillery armored vehicle |
| Seats | 3 on the stats sheet (2 seat setups in the seat data) |
| Price | 8,000 cash |
| Unlock level | 1 |
| **Gun** | |
| Main gun | L52 cannon, 155 mm |
| Shell | 155mm HE Shell |
| Range | 780–2,629 m (measured) |
| Elevation | 20–1,390 mils |
| Reload | 25.0 s |
| Travel time | about 5.5–24 s low arc, 28–37 s high arc (game table) |
| **Durability** | |
| Main health | 650 HP |
| Top speed | 65 (as stored) |
| Rifle damage taken (derived) | 0% |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-tracked-tnk-01-artillery) |
| Internal name | TNK_01 (artillery variant) |
{: .wiki-infobox }

The SPH-2 is a tracked artillery vehicle built for long-range indirect fire. Its 155 mm cannon reaches from 780 m to about 2.6 km, and the gunner aims it from the map and the gun sight's bearing tape and MIL scale rather than by direct sight. The gunner works the turret from inside.

## Overview

The SPH-2 is sold in the vehicle vendor under land artillery, for 8,000 cash, and unlocks at level 1. It shares its tracks, suspension and rifle protection with the other tracked tanks in the family.

## The gun

The SPH-2 fires 155 mm shells from an L52 cannon. There are two kinds of shell, Expensive and Standard, and the vehicle starts with 10 Expensive and no Standard. The Expensive shell (19 kg) carries a camera that follows it in flight: the view stays with the shell, then detaches after a while and zooms out, with a 4 s fade. Only the Expensive shell can be steered after firing. The Standard shell (70 kg) has no camera, and the game's flight maths put its longest flight at about 810 m (simulator estimate), so it cannot produce the long ranges.

Shells leave the barrel at 300 m/s and disappear after 40 s of flight. The barrel elevates from 2° to 80°, and the sight's MIL dial sets the elevation within the range shown in the infobox.

The stats sheet gives the gun an "effective range" of 10,000 m. That is not the real reach: the longest measured shot is 2,629 m (measured in game by the community calculator). Air drag is the reason. With drag, the Expensive shell tops out near 2.6 km; without drag the same launch would throw it about 9 km (simulator estimate).

Ranges from about 1,181 m to 2,629 m can be hit on a low arc (20 to about 600 mils, flat and fast, about 5.5 to 24 s in the air) or a high arc (about 610 to 1,390 mils, steep and slow, 28 to 37 s in the air). The travel times come from the gun's range table in the game files. Between 780 m and 1,181 m only the high arc reaches.

A short table of the firing solutions on flat ground. The mils are the settings to dial on the sight's MIL scale, measured in game. The game's own range table lists different elevations for the same ranges (45 to 97 mils higher on the low arc, up to 34 mils lower on the high arc). The reason is that the sight does not read that table's distances. It works out each mil mark's distance with a live simulation from your firing altitude, so the table and the dial are two different calculations. The barrel's true elevation is the dial reading plus 16.8 mrad (about 0.96 degrees). Simulated, a 2,000 m low-arc shot needs 250 mils from 3 m, 224 from 50 m and 197 from 100 m, so the altitude explains part of the gap:

| Range (m) | Low arc (mils) | High arc (mils) |
|---:|---:|---:|
| 1,200 | 24 | 1,291 |
| 1,600 | 105 | 1,185 |
| 2,000 | 206 | 1,057 |
| 2,400 | 358 | 877 |
| 2,600 | 522 | 708 |

The full table, with the game table's elevations, the travel times and the high-arc apex, is on the [Artillery](../game-mechanics/artillery.md) page.

## Aiming

Aiming is done from the map and the gun sight, not by eye. The [Aiming the SPH-2](../guides/aiming-the-sph-2.md) guide covers the bearing tape, compass box, MIL scale, tilt dial, minimap and map readout, and how to turn them into a fire mission. The most useful tip: aim with the bearing tape, not the compass box, because the box reads about 1.3° lower than the tape.

## Stats

| Stat | Value |
|---|---|
| Max speed | 65 (as stored) |
| Fuel capacity | 105 (as stored) |
| Fuel economy | 8.0 (as stored) |
| Seats | 3 (stats sheet) |
| Max incline | 50 degrees |
| Countermeasures | Not stated for this variant |

## Armor and damage

Main health is 650 HP. The SPH-2 has separate health for its engine (150 HP), fuel tank (100 HP) and each track (125 HP).

Rifle rounds do no damage to the tank, so rifle fire cannot destroy it. Cannon rounds do work:

| Ammunition | Hits to destroy |
|---|---:|
| 5.56 mm, 7.62×54 mm, .308 Win, .50 cal | Cannot be destroyed |
| 20×102 mm cannon | 254 |
| 30 mm cannon | 39 |

## Weapons and seats

| Weapon | Type | Rate | Effective range | Reload | Starting ammunition |
|---|---|---:|---:|---:|---:|
| L52 Cannon (155 mm artillery) | Artillery | 50 rounds/min | 10,000 m | 25.0 s | 10 Expensive, 0 Standard |

The Expensive 155 mm shell has a camera that follows the round in flight. The Standard shell has no camera. The data does not list machine guns for this variant.

The stats sheet gives 3 seats, but the seat data has two setups: a driver and a gunner in the turret.

## Handling

- Tracked drive with a top speed of 65 and a maximum incline of 50 degrees.
- Track rebound damping is shared across the tank family.
- Steering input rises at 40 and falls at 80, as stored.
- Stabilized state: the hull takes 2.0 s to stabilize and 1.0 s to release. It must be almost stopped, on ground at most 20 degrees steep, to start. It cannot move while stabilized, and the gun cannot fire while the state changes. The stabilized state does not level the barrel.

**Engine torque.** The torque curve is set against engine RPM up to 5,000 in the tracked drive data, and the torque values carry no unit label. See [Vehicle handling](vehicle-handling.md) for the other tracked numbers.

## Season 2 changes

- A new 125 mm rocket rule adds +15%.
- Track rebound damping rose from 12,000 to 17,000 across the tank family.
- The vehicle item is wider in inventory (width 4 to 6).
- Price is unchanged at 8,000.

## See also

- [Artillery](../game-mechanics/artillery.md), the full firing table and flight data
- [Aiming the SPH-2](../guides/aiming-the-sph-2.md), reading the gun sight and the map
- [L81 Mortar](../equipment/l81-mortar.md), the fixed mortar emplacement for shorter range
- [L2A6](l2a6.md) and [Flakpanzer Gepard](flakpanzer-gepard.md), the other tanks of this family
- [T-72B3](t-72b3.md), a separate tank
- [Vehicle damage](vehicle-damage.md)

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Artillery Shell Flight Data](../../game-features/Wardogs_ArtilleryShellFlight_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [wardogs-calculator by apollyon-sys (MIT)](https://github.com/apollyon-sys/wardogs-calculator), measured in game: maximum range, minimum range, and the firing table mils
- [CV Artillery Computer by Kiyogitpy (MIT)](https://github.com/Kiyogitpy/cv-artillery-computer), measured on the game screen at 2560x1440: gun sight instruments and map readout
- [SPH-2 weapon data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_01/Content/Weapons/WeaponExtensions/Artillery/WE_TNK_01_Artillery.json), from the game files: the range table with travel times
- [Round 21 artillery range check](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round21-artillery-range-check.md), estimated: the high-arc apex and the flight simulator's miss against real shots
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): how the SPH-2 sight labels its mil marks, and the mil scale.
- [Round 40 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-weapons.md): mil offset (16.8 mrad) and firing altitude
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the dial's world pitch, the SPH-2 stabilized state and the Expensive shell's steering
