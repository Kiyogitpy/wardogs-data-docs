---
title: "Artillery"
parent: "Game Mechanics"
description: "How SPH-2 artillery fire works: reading map coordinates, working out distance and bearing, mils, the low and high arcs, a firing table, and what the game data does and does not settle."
---

# Artillery

| Artillery | |
|---|---|
| **General** | |
| Gun | SPH-2 155 mm cannon (L52 cannon) |
| Shells | 155mm HE Shell, Expensive and Standard |
| Launch speed | 300 m/s |
| Barrel elevation | 2° to 80° |
| Sight setting | 20 to 1,390 mils |
| **Range** | |
| Minimum range | 780 m |
| Longest measured range | 2,629 m (measured in game) |
| Stats sheet "effective range" | 10,000 m (not the real reach) |
{: .wiki-infobox }

Artillery in Wardogs is a long-range fire mission. The SPH-2 fires 155 mm shells at a point on the map that you cannot see from the gun, so you work out an elevation and a bearing from map coordinates, set them on the gun, and read the impact. This article explains each step and gives the firing table. The table is for the SPH-2; the [L81 Mortar](../equipment/l81-mortar.md) is a separate, shorter-range emplacement. For a walk-through of firing, see [Aiming the SPH-2](../guides/aiming-the-sph-2.md).

## Overview

The SPH-2 can hit any range from 780 m to about 2,629 m, but only with the right elevation for that range. Every range from about 1,181 m up can be reached by a low arc (flat and fast) or a high arc (steep and slow), so the arc is a choice you make.

### Where these numbers come from

- The gun's stats, the shell masses and drag values, the launch speed and the 40 s flight limit are read from the game's data files.
- The firing table's mils, the arcs and the 780 m and 2,629 m limits were measured in game by the community calculator [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys. The map readout and sight instrument figures were measured on the game screen by the [CV Artillery Computer](https://github.com/Kiyogitpy/cv-artillery-computer).
- Flight times, high-arc heights, the tilt comparison and the miss figures are estimates worked out from the game's flight data with a flight simulator. The simulator's median miss against 87 real logged shots was about 59 m, so treat these as estimates.

## How it works

### Map coordinates, distance and bearing

The big map shows the cursor position as two numbers, for example "x98.99 y50.77". One map unit is 100 m, so the two decimals are metres: x 98.99 is 9,899 m east and y 50.77 is 5,077 m north. The x value grows to the east and the y value grows to the north.

To find the distance and bearing between your gun and the target:

- **Distance** is the straight line between the two points: the square root of (dx² + dy²), multiplied by 100 m.
- **Bearing** is the angle clockwise from north, found with atan2(dx, dy).

Worked example. The gun is at x 10.00, y 20.00. The target is at x 22.00, y 36.00.

- dx = 22 − 10 = 12 units, dy = 36 − 20 = 16 units.
- Distance = √(12² + 16²) = √400 = 20 units, which is **2,000 m**.
- Bearing = atan2(12, 16) = **36.9°** from north.

The calculator and the CV Artillery Computer do this sum for you. The terrain on the maps covers a square 163.84 map units (16.384 km) on a side.

### Mils

The gun's elevation scale is in mils. The best fit with the real impacts is a true milliradian, where 1 mil is 0.0573° and 1,000 mils is 57.3°. Two other mil systems, the NATO scale (6,400 per circle) and the Warsaw Pact scale (6,000 per circle), fit the impacts worse.

### Low and high arcs

Every range from about 1,181 m to 2,629 m can be hit two ways:

- The **low arc** uses about 20 to 600 mils. The shell is flat and fast.
- The **high arc** uses about 610 to 1,390 mils. The shell is steep and slow.

The two arcs meet at the longest range, 2,629 m, at about 600 to 620 mils.

Between 780 m and 1,181 m only the high arc reaches. The low arc's lowest setting, 20 mils, already lands at 1,181 m.

Two rules matter in practice:

- On the **low arc, more mils means further**.
- On the **high arc, more mils means shorter**. A higher setting throws the shell up and it comes down closer.

### The firing table

The table gives the elevation in mils for each range on flat ground. The mils come from the community calculator's table. The flight-time and apex columns are estimates from the flight simulator and are rounded. A dash means there is no value for that cell.

| Range (m) | Low arc (mils) | Low-arc flight, est. (s) | High arc (mils) | High-arc flight, est. (s) | High-arc top, est. (m) |
|---:|---:|---:|---:|---:|---:|
| 800 | - | - | 1,386 | - | - |
| 900 | - | - | 1,363 | ~37 | ~1,650 |
| 1,000 | - | - | 1,340 | ~37 | ~1,630 |
| 1,100 | - | - | 1,316 | ~36 | ~1,620 |
| 1,200 | 24 | ~6 | 1,291 | ~36 | ~1,600 |
| 1,300 | 43 | ~6 | 1,266 | ~36 | ~1,580 |
| 1,400 | 63 | ~7 | 1,240 | ~36 | ~1,560 |
| 1,500 | 84 | ~8 | 1,213 | ~35 | ~1,530 |
| 1,600 | 105 | ~9 | 1,185 | ~35 | ~1,500 |
| 1,700 | 128 | ~9 | 1,155 | ~35 | ~1,470 |
| 1,800 | 152 | ~10 | 1,124 | ~34 | ~1,440 |
| 1,900 | 178 | ~11 | 1,092 | ~34 | ~1,400 |
| 2,000 | 206 | ~12 | 1,057 | ~33 | ~1,350 |
| 2,100 | 237 | ~13 | 1,019 | ~32 | ~1,300 |
| 2,200 | 271 | ~15 | 977 | ~32 | ~1,240 |
| 2,300 | 312 | ~16 | 931 | ~31 | ~1,170 |
| 2,400 | 358 | ~18 | 877 | ~30 | ~1,090 |
| 2,500 | 421 | ~20 | 811 | ~28 | ~970 |
| 2,600 | 522 | - | 708 | - | - |

Reading the table:

- Near the top of the range, a small change in mils moves the low-arc shell a long way. From 2,500 m to 2,600 m is about 100 mils.
- At mid range the low arc needs much less change. From 1,500 m to 1,600 m is 21 mils (84 to 105).
- The high arc stays in the air for 30 s or more. The low arc is in the air for about 6 to 20 s. A moving target is a low-arc job. A shell that must clear a wall or a ridge is a high-arc job.

### Height difference and hull tilt

The table assumes the target is at the same height as the gun. A target higher or lower than the gun lands the shell short or long.

- The calculator has a height correction for the low arc. Its high-arc height correction is experimental and off by default.
- The CV Artillery Computer uses terrain heights for the same correction. Three logged shots at targets about 100 m higher landed within about 20 m.
- Shots fired without a known height difference overshot by about 70 m on average.

Hull tilt also changes where the shell lands. In the simulator's comparison against real shots, adding the hull's pitch to the elevation setting halved the median miss, from 59 m to 34 m. This suggests that the elevation is measured from the tilted hull, so park the SPH-2 level or correct for the slope. The game's handling of tilt is not confirmed.

### How consistent the gun is

The gun itself is very consistent. Repeated shots with the same setting landed within about 4 m of each other, with a worst case of 12 m. If a shot misses, the setting is the likely cause, not randomness.

### The shell's flight

Two shells exist for the SPH-2. Both are the "155mm HE Shell" in the game.

| Shell | Mass | Drag value | Camera | Notes |
|---|---:|---:|---|---|
| Expensive | 19 kg | 2.5 | Follows the shell in flight | The SPH-2 starts with this shell |
| Standard | 70 kg | 80 | None | With the game's flight maths it cannot fly further than about 815 m (estimated) |

The Expensive camera follows the shell, then detaches and zooms out after a while, with a 4 s fade.

All shells launch at 300 m/s and fall under gravity of 9.8 m/s². Air drag slows them a great deal. Without drag, the same launch would carry the shell about 9 km. With drag, the Expensive shell tops out near 2.6 km (simulator estimate). A shell disappears after 40 s of flight.

The longest flat-ground shot the simulator found with the Expensive shell is about 2,580 m, fired at about 37° (about 645 mils). It takes about 24 s, peaks at about 728 m and lands at about 113 m/s.

The stats sheet gives the SPH-2 gun an "effective range" of 10,000 m. That is not the real reach. The longest range measured in game is 2,629 m.

## Tips that follow from the numbers

- **Use the bearing tape, not the compass box.** The compass box at the top shows a whole-degree number that the CV Artillery Computer measured at about 1.3° less than the bearing tape. Aim with the tape.
- **Fire a sighting shot, then correct.** Mark where the shell lands on the map and compare it with the target. On the low arc, add mils to go further. On the high arc, add mils to go shorter.
- **Watch the Expensive shell's camera.** It shows the landing point, which is the fastest way to find your error.
- **Correct for height.** If the target is much higher or lower than the gun, use the height correction in the calculator or the CV Artillery Computer.

## What is not known

- How the game handles hull tilt. The simulator's result suggests the elevation is measured from the tilted hull, but this is not confirmed.
- The high-arc height correction. The calculator's version is experimental and off by default.
- The effect of wind. The simulator uses flat ground and no wind, and its median miss against 87 logged real shots was about 59 m. Treat the simulator's flight times and apex heights as estimates.
- Why the stats sheet gives 10,000 m as the effective range when the measured reach is 2,629 m.
- Where the Standard shell fits in play. The game's flight maths say it cannot fly the measured ranges, so this article does not cover it further.

## See also

- [SPH-2](../vehicles/sph-2.md)
- [Aiming the SPH-2](../guides/aiming-the-sph-2.md)
- [L81 Mortar](../equipment/l81-mortar.md)
- [Ballistics](ballistics.md)

## Sources

- [Artillery shell flight data](../../game-features/Wardogs_ArtilleryShellFlight_v1.md): shell masses, drag values, camera
- [Projectile flight: drag and gravity](../../pipelines/Wardogs_ProjectileFlight_v1.md)
- [All vehicles: stats and damage](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [SPH-2](../vehicles/sph-2.md)
- [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence): firing table, arcs, ranges and height correction
- [CV Artillery Computer](https://github.com/Kiyogitpy/cv-artillery-computer) (MIT licence): map coordinates, compass and bearing readings, and terrain height correction
- [shell_sim.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/shell_sim.py): flight simulator for the flight times, apex heights and miss estimates
- [Round 21 artillery range check](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round21-artillery-range-check.md): the comparison against 87 logged shots
