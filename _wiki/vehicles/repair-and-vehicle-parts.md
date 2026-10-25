---
title: "Repair and vehicle parts"
parent: "Vehicles"
group: "Reference"
description: "The damageable parts of each Wardogs vehicle with their health, what happens when a tyre, engine, fuel tank, track or rotor breaks, and how to repair them with a Wrench, a repair drill or a Repair Station."
---

# Repair and vehicle parts

| Repair and vehicle parts | |
|---|---|
| **General** | |
| Type | Mechanic |
| Applies to | Every player vehicle |
| Health unit | HP |
| **Repair** | |
| Hand repair | Wrench, Light drill, Heavy drill (10 HP per Wrench use; 14.5 HP per drill use) |
| Base repair | Repair Station (Fast: 5% in 3 s; Max: up to 100% in 9 s) |
{: .wiki-infobox }

A vehicle has one main health pool, plus separate pools for some parts: the engine, the fuel tank, the wheels or tracks, and on helicopters the rotors. The main health decides whether the vehicle is destroyed. The part pools decide what breaks and when. How hits reach each part is covered in [Vehicle damage](vehicle-damage.md).

## Overview

Parts with their own health are the engine, fuel tank, wheels (or tracks on tanks and the M113), and the main and tail rotors on helicopters. The airplane has no separate pools. Its 150 HP starts as one body pool.

## How it works

### Damageable parts

- **Engine.** Its own health pool. It has effect triggers at fixed health percentages.
- **Fuel tank.** Its own health pool. Its triggers and the leak effect are covered in [Fuel and refueling](fuel-and-refueling.md). An empty tank stops the engine, and the engine cannot be restarted until the tank is refuelled (static reading, not checked in play).
- **Tyres (wheeled vehicles).** Each wheel has its own pool, usually 75 HP.
- **Tracks (tanks, the M113).** Each track has its own pool, usually 125 HP.
- **Rotors (helicopters).** A main rotor and a tail rotor, each with its own pool.
- **Radar (M113).** A separate part with 100 HP.

### Tyres

A tyre has three states in the data:

1. **Intact.**
2. **Damaged** (deflated) when the wheel's health falls to 55% of its maximum or below. A 75 HP tyre deflates at about 41 HP or less. Season 1 used 50%, and Season 2 raised it to 55% on every wheeled axle.
3. **Destroyed** when the wheel's health reaches zero.

A deflated tyre keeps its wheel on the ground but uses a different collision shape. A destroyed tyre is replaced by a damaged-wheel model. The data stores a tyre radius for each state (on the Dune Buggy 0.45 m, 0.345 m and 0.26 m). The code that applies these per-state values was not found: in the code read, the damage state itself only shows or hides wheel meshes and sets two visual values ([round 48 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round48.md)). A deflated tyre also adds 1.5 of wheel drag, cuts grip by 0.35 friction, pulls the steering toward the damaged side (0.125) and adds 0.05 braking. The data does not say how the smaller radius of a deflated or destroyed tyre affects the car beyond the collision shape.

### Health triggers

Parts have effect triggers at fixed percentages of their health. The data lists where each trigger sits. Most effects are not decoded in the data, so the wiki does not say exactly what each one does. Where the data is clear, it is stated below.

- **Main body.** Triggers at 55%, 25% and 10% on most ground vehicles and helicopters.
- **Engine.** Triggers at 20% on the Bobcat, at 55% on the SPH-2, L2A6, Gepard and Humvee [M249], and at 0% on all of them.
- **Fuel tank.** Triggers at 90% and 80%, 55%, and 0% on several vehicles. The Little Bird family uses 10% and 0%. When the fuel tank is hit, the tank leaks fuel at a rate that rises as its health falls; the steps are in [Fuel and refueling](fuel-and-refueling.md#fuel-leaks).
- **Tracks.** A track has an effect above 55% and is dead at 0%.
- **Wheels.** Triggers at 55% and 0% on the wheeled vehicles.
- **Rotors.** The Havoc's main and tail rotors have triggers at 55% and 0%. The data sets rotor triggers only for the Havoc.
- **Radar.** On the M113, triggers at 55%, 25% and 0%.
- **Turret stabilisation.** On the SPH-2, L2A6 and T-72B3, the turret's stabilisation is switched off below 25% main health. The data marks that point as the one where stabilisation is no longer permitted.

A non-main part that reaches zero is marked destroyed, and the vehicle keeps going. Only the main health at zero destroys the vehicle.

### Season 2 changes

- The tyre deflate threshold rose from 50% to 55% on every wheeled axle (the Humvee, Kodiak, Dune Buggy, Ural and Bobcat axles, among others).
- The data lists no Season 2 change to the health pools of the engine, fuel tank, tracks or rotors.

## Numbers

Health pools per vehicle, as stored in the data. Sort by any column with the header. "Not listed" means the data sets no separate pool for that part.

| Vehicle | Main health (HP) | Engine (HP) | Fuel tank (HP) | Wheels or tracks (HP each) | Rotors (HP, main / tail) |
|---|---:|---:|---:|---|---|
| [Havoc](havoc.md) | 800 | 200 | 200 | Front wheels 100 | 400 / 300 |
| [MH-6](mh-6.md) | 400 | 200 | 200 | None | 400 / 300 |
| [AH-6M [Miniguns]](ah-6m-miniguns.md) | 400 | 200 | 200 | None | 400 / 300 |
| [AH-6R [Rockets]](ah-6r-rockets.md) | 400 | 200 | 200 | None | 400 / 300 |
| [Z20 Lakota](z20-lakota.md) | 600 | 200 | 200 | None | 400 / 300 |
| [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md) | 600 | 200 | 200 | None | 400 / 300 |
| [Fixed-wing airplane](fixed-wing-airplane.md) | 150 at start | Not listed | Not listed | None | None |
| [M113 APC SV](m113-apc-sv.md) | 1,000 | Not listed | 100 | Tracks 125, radar 100 | None |
| [SPH-2](sph-2.md) | 650 | 150 | 100 | Tracks 125 | None |
| [L2A6](l2a6.md) | 800 | 150 | 150 | Tracks 125, hull zone 350 | None |
| [Flakpanzer Gepard](flakpanzer-gepard.md) | 800 | 150 | 150 | Tracks 125 | None |
| [T-72B3](t-72b3.md) | 750 | 150 | 150 | Tracks 125 | None |
| [Bobcat](bobcat.md) | 200 | 200 | 100 | Wheels 75 | None |
| [Kodiak](kodiak.md) | 400 | 400 | 400 | Wheels 75 | None |
| [Kodiak [Pickup]](kodiak-pickup.md) | 400 | 400 | 400 | Wheels 75 | None |
| [Kodiak [M249]](kodiak-m249.md) | 400 | 400 | 400 | Wheels 75 | None |
| [Humvee](humvee.md) | 500 | 400 | 400 | Wheels 75 | None |
| [Humvee [Minigun]](humvee-minigun.md) | 500 | 400 | 400 | Wheels 75 | None |
| [Humvee [M249]](humvee-m249.md) | 500 | 400 | 400 | Wheels 75 | None |
| [Dune Buggy](dune-buggy.md) | 400 | 400 | 300 | Wheels 75 | None |
| [Ural](ural.md) | 700 | 400 | 400 | Six wheels 75 | None |
| [Ural Defender](ural-defender.md) | 700 | 400 | 400 | Six wheels 75 | None |
| [Ural Defender [M249]](ural-defender-m249.md) | 700 | 400 | 400 | Six wheels 75 | None |
| [Wolf-110](wolf-110.md) | 500 | 400 | 400 | Wheels 75 | None |
| [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md) | 500 | 400 | 400 | Wheels 75 | None |

### Repair tools and stations

| Repair option | Repairs | Per use | Speed | Cost |
|---|---|---:|---|---|
| [Wrench](../equipment/wrench.md) | All vehicles | 10 HP | 0.68 s (about 14.7 HP per second) | 180 cash |
| [Light repair drill](../equipment/drills.md) | Vehicles | 14.5 HP | 0.75 s (about 19.3 HP per second) | 600 cash |
| [Heavy repair drill](../equipment/drills.md) | Vehicles | 14.5 HP | 0.5 s (29 HP per second) | 1,300 cash |
| [Refuel and Repair Stations](../building/refuel-and-repair-stations.md) | Vehicles in the FOB radius | Fast: 5%; Max: up to 100% | Fast: 3 s; Max: 9 s | Fast: 100 cash; Max: 2,000 cash. Building a station costs 200 Build Supplies |

Each repair tool is used until it is empty or the target is full. Each tool repairs a fixed amount per application: 10 HP for the Wrench and 14.5 HP for each drill, at the rates in the table. A Repair Station uses Mechanical Supplies, which cost 10 cash per lot of 50. A full restock uses 5 of them. A Max restock is charged only for the share of health it restores: the 2,000 cash price is the full-health price, scaled down for a partial repair and rounded up to a multiple of 50 (static reading of the restock code, not checked in play). The station's stored 13.33 figure is the structure's own hammer repair-speed multiplier. Every buildable has one, and most are the structure's Build Supplies cost divided by 15. It is not a vehicle repair rate.

The in-game tips say that high impact damage zones on a vehicle can be repaired with repair tools, and that returning to base for repairs is not free.

## Tips that follow from the numbers

- A Humvee tyre deflates at about 41 HP, which is 55% of its 75 HP. Any tyre damage past that point changes the tyre's state, so a deflated tyre is the first warning.
- Tanks take little rifle damage, and their tracks have 125 HP each. The data sets a track trigger at 55%, but not what it does.
- At 10 HP per Wrench use, the Humvee's 500 HP would take 50 uses to restore from zero, about 34 seconds of repair (derived).
- The in-game tip says a rotor blade breaks if it hits an object, so flying close to terrain or other aircraft puts the rotors at risk.

## See also

- [Vehicle damage](vehicle-damage.md): how hits reach each part
- [Fuel and refueling](fuel-and-refueling.md): the fuel tank and refilling
- [Vehicle handling](vehicle-handling.md): how wheel and track state affects movement, where the data says so
- [Wrench](../equipment/wrench.md), [Drills](../equipment/drills.md) and [Supplies](../equipment/supplies.md)

## Sources

- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- - [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the empty-tank restart block and the Max repair charge rule
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md): health pools and health triggers
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md): wheel radius states
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): the tyre states and deflate threshold
- [Buildables](../../game-features/Wardogs_Buildables_v1.md): the Repair Station
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md) and [Item Actions](../../content/Wardogs_ItemActions_v1.md): repair tool amounts and prices
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): Repair Station restock rates and the stored 13.33 multiplier.
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Wrench and drill repair per application and rate, tyre deflation and fuel-tank leak steps.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the Wrench and drill timings and the fuel-tank health steps.
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
