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
| Acceleration time | Not stored in the data |
| Curves | [Vehicle Curves](../../game-features/Wardogs_VehicleCurves_v1.md) |
{: .wiki-infobox }

Handling is how a vehicle moves: how fast it goes, how hard the engine pulls at each speed, how far the wheels turn, and how it slows down. The data stores these as numbers and curves, and the wiki shows them as stored. The data does not label most units, so the numbers are relative values unless a field names its unit, such as the steering angle in degrees.

## Overview

Each vehicle has a top speed from its vendor stats. Its drive comes from a torque curve (the engine's pull at each RPM), a set of gear ratios, a torque split between the axles, and a brake setup. Steering and speed limits come from separate curves. Helicopters and the airplane use a different flight setup, and the data for it is much larger than this table covers.

## How it works

### Speed, torque and gears

The torque curve is the engine's pull at each engine speed. A peak of 475 at 5,500 means the engine pulls hardest at 5,500 RPM on that vehicle. Gears multiply that pull. A low first gear (a big ratio) gives more push when starting, and a high top gear gives more speed. Tracked vehicles use the same kind of torque curve against engine RPM, with the curve running up to 5,000 RPM. The torque values carry no unit label.

In a wheeled vehicle's gear list, the last ratio is the reverse gear, applied in the opposite direction (confirmed in the game code). The other entries are the forward gears, in order. The Bobcat's list, 4.2, 2.8, 1.9, 1.5, 1.3 and 6, therefore gives five forward gears with a reverse ratio of 6.0. The Humvee's list ends in 3.6, which is its reverse, so it also has five forward gears. Tracked vehicles read their list differently: the entry with a ratio of 0 is neutral, so they have 1 reverse and 3 forward gears (see the tracked section below).

The data does not store a 0 to top speed time, so acceleration is shown here only through the torque and first gear numbers. The game files hold no acceleration time to read.

### Steering

Each wheeled axle has a steering angle in degrees, and the front wheels steer. The steering curves in the data limit how far the wheel can turn as speed changes. The curves page reads these as less steering lock at higher speed. That reading is an inference from the curve shapes, not a confirmed rule.

Tracked vehicles do not steer with wheels. They have a steering input response (how quickly the steer input rises and falls), which is the same on every tracked vehicle in the data.

### Driving input tuning

Each wheeled vehicle has its own input settings, which shape how the controls respond before the physics runs. The game does not label their units, so the figures are shown as stored.

- **Steering sensitivity** scales the steer input: 2.5 on the Humvee, 1.3 on the Bobcat and 1.25 on the Dune Buggy. The Kodiak, Ural and Wolf-110 store none, so they use the game default of 5.0 (see Game defaults below).
- **Steer input gravity** is how fast the steering returns to centre when you release it. It is 1 on the Bobcat, 2.6 on the Wolf-110 and 2 on the Humvee, Dune Buggy, Ural and Kodiak.
- **Steering deadzone and steering assist** are stored only for the Bobcat (a deadzone of 0.05 and an assist of 20). The other wheeled vehicles store no dead zone, so they use the game default of 0.01 and no assist.
- **Throttle and brake sensitivity** shape the pedals. Throttle is 2 on the Humvee and Bobcat, 1.75 on the Dune Buggy, 1.5 on the Wolf-110 and 1 on the Ural. Brake is 6.5 on the Humvee and Wolf-110, the highest values stored, 1.25 on the Dune Buggy and 1 on the Bobcat.
- **Steer speed and steer limit curves** make steering lighter at speed. On every wheeled vehicle that stores them the steer-speed multiplier falls as the input rises. On the Bobcat it stays at 2.5 up to 41.5 and falls to 1 by 75, and its steering limit falls from 100 to 80. The input unit is not stated.
- **Engagement curves** map pedal travel to throttle, brake and clutch. On most vehicles these are straight lines over the full travel, with the clutch held at zero for the first tenth of travel. On the Humvee and Wolf-110 the brake is already at full by a tenth of travel.

The tracked, rotary and airplane controls store only input mapping and prompt lists, so the data has no tuning numbers for them.

(Source: round 41 data, see [Vehicle Inputs and Explosive Effects](../../game-features/Wardogs_VehicleInputsAndExplosiveEffects_v1.md), section 1.)

### Braking

- **Brake torque** is set per axle, front and rear. A higher number brakes harder on that axle.
- **Hand brake** is a separate value for the parking brake.
- **ABS** and **ASR** (traction control) are stored for the wheeled vehicles. They are the anti-lock and wheel-spin assists. What each does in detail is not decoded.
- **Brake force** is stored for some tracked vehicles. Tracked vehicles also have a brake curve that ties braking to speed, which reaches its top value at 800.

### Maximum incline

Only tracked vehicles store a maximum incline in the handling data, at 50 degrees for each of them. The wheeled vehicles and helicopters have no maximum incline in the handling tables, so the data stores none for them.

### Torque split

On wheeled vehicles, the torque split sets how much of the engine's pull goes to the front axle and how much to the rear. The Dune Buggy sends 85% to the rear, and the Humvee sends 60% to the rear. Some vehicles do not store a split; for those the game default is 0.5 to the front and 0.5 to the rear.

### Game defaults

When an asset does not store a field, the game uses the value its class constructor writes. A missing field is the default, not zero. The defaults that matter for the blank cells in this article are below. They are the game's values, not stored in each vehicle's data.

| Field | Game default | Used by |
|---|---|---|
| Idle RPM | 1,000 | All three Kodiak versions |
| Torque scale | 1.0 | Bobcat, Humvee |
| Steering sensitivity | 5.0 | Kodiak, Ural, Wolf-110 |
| Steer dead zone | 0.01 | Wheeled vehicles that store none |
| Axle torque share | 0.5 front, 0.5 rear | Kodiak, Ural |
| Track mass | 600 | Tracked vehicles |
| Sprocket mass | 64 | Tracked vehicles |

The boost switch is off in the defaults and in every asset, so no vehicle boosts. The stored boost value does have a path: when the switch is on and the boost input is held, the engine's torque scale is replaced by the boost value, and goes back to the normal scale when the input is released. With the switch off in every vehicle, the stored boost values never take effect.

### Driving and flight assists

Arcade assists correct the vehicle on its own. The data stores their settings, and the values below are shown as stored.

- **Humvee and Wolf-110.** The two share the same assist settings: anti-roll 40 on both axles and a full-recovery speed of 120.
- **Kodiak.** A drift assist with 5 at the front and 60 at the rear, and a full-recovery speed of 200.
- **Ural.** Drift values of 2.5 at the front and 30 at the rear.
- **Dune Buggy.** Lean up to 15 degrees and pitch up to 20 degrees, with drift values of 1 at the front and 1 at the rear.
- **Helicopters.** All three helicopters (Havoc, MH-6 family and Z20 Lakota) limit their climb rate to 36 km/h, hold a hover when the collective is released, and set the collective to minus 1 on the ground. The Havoc alone also levels pitch and roll at low speed and resets pitch and roll to zero on the ground.
- **Havoc switched-off assists.** Four Havoc assists are stored as disabled: the sink-rate limit, the yaw reset on the ground, the roll drag-overshoot prevention and the roll input damping.
- **Tyre models.** The Bobcat, the Kodiak (and Pickup) and the Ural name a simple tyre model in the data. The Humvee, Dune Buggy and Wolf-110 name none.

### Season 2 changes

- **Humvee torque share.** The front share fell from 0.7 to 0.4, and the rear share rose from 0.3 to 0.6.
- **Humvee torque curve.** The curve starts higher, at 1,200 instead of 850, and falls to 400 at 3,750 RPM, down from 650 at 4,000 RPM.
- **Dune Buggy rear brakes.** The rear brake torque fell from 16,000 to 13,000 on the first value, and from 12,000 to 9,000 on the second.

## Numbers

### Wheeled vehicles

Sort by any column with the header.

| Vehicle | Max speed (as stored) | Mass (as stored) | Peak torque (at RPM) | First gear | Torque split front / rear | Steer, front (deg) | Brake torque front / rear | Hand brake | Max incline (deg) |
|---|---:|---:|---|---:|---|---:|---|---:|---|
| [Bobcat](bobcat.md) | 75 | 250 | 33 at 5,000 | 4.2 | 0.6 / 0.4 | 35 | 1,800 / 1,250 | 8 | Not stored |
| [Kodiak](kodiak.md) | 154 | 2,750 | 475 at 5,500 | 6.0 | 0.5 / 0.5 (default) | 30 | 8,000 / 14,000 | 50 | Not stored |
| [Kodiak [Pickup]](kodiak-pickup.md) | 154 | 2,750 | 475 at 5,500 | 6.0 | 0.5 / 0.5 (default) | 30 | 8,000 / 14,000 | 50 | Not stored |
| [Kodiak [M249]](kodiak-m249.md) | 154 | 2,750 | 475 at 5,500 | 6.0 | 0.5 / 0.5 (default) | 30 | 8,000 / 14,000 | 50 | Not stored |
| [Humvee](humvee.md) | 113.2 | 7,250 | 475 at 5,500 | 3.6 | 0.4 / 0.6 | 35 | 8,000 / 35,000 | 80 | Not stored |
| [Humvee [Minigun]](humvee-minigun.md) | 113.2 | 7,250 | 475 at 5,500 | 3.6 | 0.4 / 0.6 | 35 | 8,000 / 35,000 | 80 | Not stored |
| [Humvee [M249]](humvee-m249.md) | 113.2 | 7,250 | 475 at 5,500 | 3.6 | 0.4 / 0.6 | 35 | 8,000 / 35,000 | 80 | Not stored |
| [Dune Buggy](dune-buggy.md) | 130 | 550 | 475 at 5,500 | 4.8 | 0.15 / 0.85 | 40 | 4,000 / 13,000 | 50 | Not stored |
| [Ural](ural.md) | 79 | 10,000 | 900 at 1,200 | 5.62 | 0.5 / 0.5 (default) | 30 | 20,000 / 38,000 | 50 | Not stored |
| [Ural Defender](ural-defender.md) | 79 | 10,000 | 900 at 1,200 | 5.62 | 0.5 / 0.5 (default) | 30 | 20,000 / 38,000 | 50 | Not stored |
| [Ural Defender [M249]](ural-defender-m249.md) | 79 | 10,000 | 900 at 1,200 | 5.62 | 0.5 / 0.5 (default) | 30 | 20,000 / 38,000 | 50 | Not stored |
| [Wolf-110](wolf-110.md) | 129 | 3,200 | 1,500 at 1,650 | 3.7 | 0.3 / 0.7 | 35 | 5,500 / 9,000 | 80 | Not stored |
| [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md) | 129 | 3,200 | 1,500 at 1,650 | 3.7 | 0.3 / 0.7 | 35 | 5,500 / 9,000 | 80 | Not stored |

The Ural's brake torque is listed for its three axles, with 38,000 on both the middle and rear axles. The Ural's torque curve has a scale of 2, so its numbers are larger than the other trucks' at the same RPM.

### Tracked vehicles

| Vehicle | Max speed (as stored) | Peak torque (at RPM) | Gear entries (as stored) | Brake force | Max incline (deg) |
|---|---:|---|---:|---:|---:|
| [M113 APC SV](m113-apc-sv.md) | 71 | 2,500 at 1,200 | 10 | 14 | 50 |
| [SPH-2](sph-2.md) | 65 | 1,800 at 1,400 | 10 | Not set | 50 |
| [L2A6](l2a6.md) | 65 | 1,800 at 1,400 | 10 | Not set | 50 |
| [Flakpanzer Gepard](flakpanzer-gepard.md) | 65 | 1,800 at 1,400 | 7 | 30 | 50 |
| [T-72B3](t-72b3.md) | 60 | 1,800 at 1,400 | 10 | Not set | 50 |

The gear column counts the entries in the first, older gear list stored for each tracked vehicle. The game does not use that list while driving (see the engine curves below). The gear list it does use is shorter: the M113, SPH-2, L2A6 and Flakpanzer Gepard all use 5 entries (5, 0, 8, 6, 2.65), and the T-72B3 uses 5 entries (5, 0, 8, 6, 3.6). The entry with a ratio of 0 is neutral. The entries before it are reverse, so these tracked vehicles have one reverse gear (ratio 5) and three forward gears (8, 6, then 2.65 or 3.6), and the vehicle starts in the first forward gear. For the wheeled vehicles the last entry is reverse.

The tank torque curves are the same for the SPH-2, L2A6, Gepard and T-72B3, and the M113 has its own curve. Tracked vehicles store a second engine curve with a peak of 1,400 at 1,911 RPM. This second curve is the one the game reads while driving: it is evaluated at the engine's current RPM and multiplied by the vehicle's torque multiplier. No use of the first curve was found, so the peak torque and gear columns above describe stored data that the tracked vehicles do not appear to use (inferred, a copy of that data at start-up was not ruled out).

### Helicopters

| Vehicle | Max speed (as stored) | Body mass (kg) |
|---|---:|---:|
| [Havoc](havoc.md) | 400 | 7,500 |
| [MH-6](mh-6.md) | 350 | 722 |
| [AH-6M [Miniguns]](ah-6m-miniguns.md) | 350 | 722 |
| [AH-6R [Rockets]](ah-6r-rockets.md) | 350 | 722 |
| [Z20 Lakota](z20-lakota.md) | 445 | 9,500 |

Helicopters have a drag coefficient of 0.006 on every variant. Their steering, braking and torque values are not in the handling tables. The aircraft body masses are in kilograms (the airplane's is 10,000 kg). The MH-6's mass of 722 kg is far below its collision mass of 1,200, whose unit the data does not label, so the two numbers cannot be compared directly. The vehicle vendor labels top speeds in km/h, so the helicopter speeds above are km/h.

## Tips that follow from the numbers

- The Dune Buggy is the lightest full-size car at 550 mass (only the Bobcat is lighter, at 250) and sends 85% of its torque to the rear. It has the widest front steering angle of the wheeled vehicles at 40 degrees.
- The Ural has the heaviest mass in the wheeled group at 10,000, a long first gear (5.62, second only to the Kodiak's 6.0) and a torque peak of 900 at 1,200 RPM, so it has strong pull from low speed.
- The Wolf-110 has the largest torque peak of the wheeled vehicles, 1,500 at 1,650 RPM, with a top speed of 129.
- Since Season 2 the Humvee sends 60% of its torque to the rear axle, so its rear wheels do most of the pulling.
- The tracked vehicles all share a 50 degree maximum incline in the data.

## See also

- [Vehicle Curves](../../game-features/Wardogs_VehicleCurves_v1.md): every curve, its keys and which vehicle uses it
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md): the full per-variant drivetrain, suspension and brake tables
- [Repair and vehicle parts](repair-and-vehicle-parts.md): tyre and track states, which change how a vehicle drives
- [Vehicles](../vehicles.md): the full list of vehicles

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the driving input tuning and the tracked torque curve range
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Curves](../../game-features/Wardogs_VehicleCurves_v1.md)
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): top speed and mass
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicles Reference](../../content/Wardogs_Vehicles_v2.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Driving and flight assist settings, tyre models and wheeled incline.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
