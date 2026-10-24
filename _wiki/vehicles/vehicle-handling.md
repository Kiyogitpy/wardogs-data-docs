---
title: "Vehicle handling"
parent: "Vehicles"
group: "Reference"
description: "Top speed, torque, gearing, steering, braking and maximum incline for each Wardogs vehicle, and what the handling curves mean for how a vehicle drives."
---

# Vehicle handling

| Vehicle handling | |
|---|---|
| **General** | |
| Type | Mechanic |
| Applies to | Wheeled, tracked and rotary vehicles |
| Units | Mostly not labelled in the data (shown as stored) |
| **Data** | |
| Acceleration time | Not yet known |
| Curves | [Vehicle Curves](../../game-features/Wardogs_VehicleCurves_v1.md) |
{: .wiki-infobox }

Handling is how a vehicle moves: how fast it goes, how hard the engine pulls at each speed, how far the wheels turn, and how it slows down. The data stores these as numbers and curves, and the wiki shows them as stored. The data does not label most units, so the numbers are relative values unless a field names its unit, such as the steering angle in degrees.

## Overview

Each vehicle has a top speed from its vendor stats. Its drive comes from a torque curve (the engine's pull at each RPM), a set of gear ratios, a torque split between the axles, and a brake setup. Steering and speed limits come from separate curves. Helicopters and the airplane use a different flight setup, and the data for it is much larger than this table covers.

## How it works

### Speed, torque and gears

The torque curve is the engine's pull at each engine speed. A peak of 475 at 5,500 means the engine pulls hardest at 5,500 RPM on that vehicle. Gears multiply that pull. A low first gear (a big ratio) gives more push when starting, and a high top gear gives more speed.

The data does not store a 0 to top speed time, so acceleration is shown here only through the torque and first gear numbers. The actual acceleration time is not yet known.

### Steering

Each wheeled axle has a steering angle in degrees, and the front wheels steer. The steering curves in the data limit how far the wheel can turn as speed changes. The curves page reads these as less steering lock at higher speed. That reading is an inference from the curve shapes, not a confirmed rule.

Tracked vehicles do not steer with wheels. They have a steering input response (how quickly the steer input rises and falls), which is the same on every tracked vehicle in the data.

### Braking

- **Brake torque** is set per axle, front and rear. A higher number brakes harder on that axle.
- **Hand brake** is a separate value for the parking brake.
- **ABS** and **ASR** (traction control) are stored for the wheeled vehicles. They are the anti-lock and wheel-spin assists. What each does in detail is not decoded.
- **Brake force** is stored for some tracked vehicles. Tracked vehicles also have a brake curve that ties braking to speed, which reaches its top value at 800.

### Maximum incline

Only tracked vehicles store a maximum incline in the handling data, at 50 degrees for each of them. The wheeled vehicles and helicopters do not store one in the handling tables, so their maximum incline is not yet known.

### Torque split

On wheeled vehicles, the torque split sets how much of the engine's pull goes to the front axle and how much to the rear. The Dune Buggy sends 85% to the rear, and the Humvee sends 60% to the rear. Some vehicles do not store a split.

### Season 2 changes

- **Humvee torque share.** The front share fell from 0.7 to 0.4, and the rear share rose from 0.3 to 0.6.
- **Humvee torque curve.** The curve starts higher, at 1,200 instead of 850, and falls to 400 at 3,750 RPM, down from 650 at 4,000 RPM.
- **Dune Buggy rear brakes.** The rear brake torque fell from 16,000 to 13,000 on the first value, and from 12,000 to 9,000 on the second.

## Numbers

### Wheeled vehicles

Sort by any column with the header.

| Vehicle | Max speed (as stored) | Mass (as stored) | Peak torque (at RPM) | First gear | Torque split front / rear | Steer, front (deg) | Brake torque front / rear | Hand brake | Max incline (deg) |
|---|---:|---:|---|---:|---|---:|---|---:|---|
| [Bobcat](bobcat.md) | 75 | 250 | 33 at 5,000 | 4.2 | 0.6 / 0.4 | 35 | 1,800 / 1,250 | 8 | Not yet known |
| [Kodiak](kodiak.md) | 154 | 2,750 | 475 at 5,500 | 6.0 | Not set | 30 | 8,000 / 14,000 | 50 | Not yet known |
| [Kodiak [Pickup]](kodiak-pickup.md) | 154 | 2,750 | 475 at 5,500 | 6.0 | Not set | 30 | 8,000 / 14,000 | 50 | Not yet known |
| [Kodiak [M249]](kodiak-m249.md) | 154 | 2,750 | 475 at 5,500 | 6.0 | Not set | 30 | 8,000 / 14,000 | 50 | Not yet known |
| [Humvee](humvee.md) | 113.2 | 7,250 | 475 at 5,500 | 3.6 | 0.4 / 0.6 | 35 | 8,000 / 35,000 | 80 | Not yet known |
| [Humvee [Minigun]](humvee-minigun.md) | 113.2 | 7,250 | 475 at 5,500 | 3.6 | 0.4 / 0.6 | 35 | 8,000 / 35,000 | 80 | Not yet known |
| [Humvee [M249]](humvee-m249.md) | 113.2 | 7,250 | 475 at 5,500 | 3.6 | 0.4 / 0.6 | 35 | 8,000 / 35,000 | 80 | Not yet known |
| [Dune Buggy](dune-buggy.md) | 130 | 550 | 475 at 5,500 | 4.8 | 0.15 / 0.85 | 40 | 4,000 / 13,000 | 50 | Not yet known |
| [Ural](ural.md) | 79 | 10,000 | 900 at 1,200 | 5.62 | Not set | 30 | 20,000 / 38,000 | 50 | Not yet known |
| [Ural Defender](ural-defender.md) | 79 | 10,000 | 900 at 1,200 | 5.62 | Not set | 30 | 20,000 / 38,000 | 50 | Not yet known |
| [Ural Defender [M249]](ural-defender-m249.md) | 79 | 10,000 | 900 at 1,200 | 5.62 | Not set | 30 | 20,000 / 38,000 | 50 | Not yet known |
| [Wolf-110](wolf-110.md) | 129 | 3,200 | 1,500 at 1,650 | 3.7 | 0.3 / 0.7 | 35 | 5,500 / 9,000 | 80 | Not yet known |
| [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md) | 129 | 3,200 | 1,500 at 1,650 | 3.7 | 0.3 / 0.7 | 35 | 5,500 / 9,000 | 80 | Not yet known |

The Ural's brake torque is listed for its three axles, with 38,000 on both the middle and rear axles. The Ural's torque curve has a scale of 2, so its numbers are larger than the other trucks' at the same RPM.

### Tracked vehicles

| Vehicle | Max speed (as stored) | Peak torque (at RPM) | Gears | Brake force | Max incline (deg) |
|---|---:|---|---:|---:|---:|
| [M113 APC SV](m113-apc-sv.md) | 71 | 2,500 at 1,200 | 10 | 14 | 50 |
| [SPH-2](sph-2.md) | 65 | 1,800 at 1,400 | 10 | Not set | 50 |
| [L2A6](l2a6.md) | 65 | 1,800 at 1,400 | 10 | Not set | 50 |
| [Flakpanzer Gepard](flakpanzer-gepard.md) | 65 | 1,800 at 1,400 | 7 | 30 | 50 |
| [T-72B3](t-72b3.md) | 60 | 1,800 at 1,400 | 10 | Not set | 50 |

The tank torque curves are the same for the SPH-2, L2A6, Gepard and T-72B3, and the M113 has its own curve. Tracked vehicles store a second engine curve with a peak of 1,400 at 1,911 RPM, which the data does not say is used alongside the first.

### Helicopters

| Vehicle | Max speed (as stored) | Mass (as stored) |
|---|---:|---:|
| [Havoc](havoc.md) | 400 | 7,500 |
| [MH-6](mh-6.md) | 350 | 722 |
| [AH-6M [Miniguns]](ah-6m-miniguns.md) | 350 | 722 |
| [AH-6R [Rockets]](ah-6r-rockets.md) | 350 | 722 |
| [Z20 Lakota](z20-lakota.md) | 445 | 9,500 |

Helicopters have a drag coefficient of 0.006 on every variant. Their steering, braking and torque values are not in the handling tables. The MH-6's mass of 722 is far below its collision mass of 1,200, and the data does not label the unit, so the two numbers cannot be compared directly.

## Tips that follow from the numbers

- The Dune Buggy is the lightest car at 550 mass and sends 85% of its torque to the rear. It has the widest front steering angle of the wheeled vehicles at 40 degrees.
- The Ural has the heaviest mass in the wheeled group at 10,000, but also the largest first gear (5.62) and a torque peak of 900 at 1,200 RPM, so it has strong pull from low speed.
- The Wolf-110 has the largest torque peak of the wheeled vehicles, 1,500 at 1,650 RPM, with a top speed of 129.
- Since Season 2 the Humvee sends 60% of its torque to the rear axle, so its rear wheels do most of the pulling.
- The tracked vehicles all share a 50 degree maximum incline in the data.

## See also

- [Vehicle Curves](../../game-features/Wardogs_VehicleCurves_v1.md): every curve, its keys and which vehicle uses it
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md): the full per-variant drivetrain, suspension and brake tables
- [Repair and vehicle parts](repair-and-vehicle-parts.md): tyre and track states, which change how a vehicle drives
- [Vehicles](../vehicles.md): the full list of vehicles

## Sources

- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Curves](../../game-features/Wardogs_VehicleCurves_v1.md)
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): top speed and mass
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicles Reference](../../content/Wardogs_Vehicles_v2.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
