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

Artillery in Wardogs is a long-range fire mission. The SPH-2 fires 155 mm shells at a point on the map that you cannot see from the gun, so you work out an elevation and a bearing from map coordinates, set them on the gun, and read the impact. This article explains each step and gives the firing table. The table is for the SPH-2; the [L81 Mortar](../building/l81-mortar.md) is a separate, shorter-range emplacement. For a walk-through of firing, see [Aiming the SPH-2](../guides/aiming-the-sph-2.md).

## Overview

The SPH-2 can hit any range from 780 m to about 2,629 m, but only with the right elevation for that range. Every range from about 1,181 m up can be reached by a low arc (flat and fast) or a high arc (steep and slow), so the arc is a choice you make.

### Where these numbers come from

- The gun's stats, the shell masses and drag values, the launch speed and the 40 s flight limit are read from the game's data files.
- The gun's own range table is in the game files: for each elevation setting it lists where the shell lands and how long it takes. This article calls it the game table, and its elevations are in milliradians (mrad). It gives the travel times in the firing table below.
- The "dial" mils are the settings read off the sight's MIL scale in game. They were measured by the community calculator [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys and checked against logged impacts. The map readout and sight instrument figures were measured on the game screen by the [CV Artillery Computer](https://github.com/Kiyogitpy/cv-artillery-computer).
- High-arc heights, the tilt comparison and the miss figures are estimates worked out from the game's flight data with a flight simulator. The simulator's median miss against 87 real logged shots was about 59 m, so treat these as estimates.

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

The barrel's true elevation is the dial reading plus 16.8 mrad (about 0.96 degrees). The game's range code adds this offset before the shell flies, so the dial values in the tables are the ones to set on the gun.

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

The table gives, for each range on flat ground, the dial setting to use and the game table's own figures. **Dial these numbers: the "dial" columns.** They were measured on the in-game MIL scale and checked against logged impacts, while the game table's elevations do not match the dial (see below). The travel times come from the game table. The top-of-arc column is an estimate from the flight simulator. A dash means there is no value for that cell.

| Range (m) | Low arc: dial (mils) | Low arc: game table (mrad) | Low arc: travel time (s) | High arc: dial (mils) | High arc: game table (mrad) | High arc: travel time (s) | High-arc top, est. (m) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 800 | - | 42 | 3.4 | 1,386 | 1,384 | 36.9 | - |
| 900 | - | 53 | 4.0 | 1,363 | 1,360 | 36.7 | about 1,650 |
| 1,000 | - | 64 | 4.5 | 1,340 | 1,337 | 36.6 | about 1,630 |
| 1,100 | - | 77 | 5.1 | 1,316 | 1,313 | 36.4 | about 1,620 |
| 1,200 | 24 | 91 | 5.7 | 1,291 | 1,287 | 36.1 | about 1,600 |
| 1,300 | 43 | 106 | 6.4 | 1,266 | 1,262 | 35.9 | about 1,580 |
| 1,400 | 63 | 121 | 7.1 | 1,240 | 1,236 | 35.6 | about 1,560 |
| 1,500 | 84 | 139 | 7.8 | 1,213 | 1,209 | 35.3 | about 1,530 |
| 1,600 | 105 | 157 | 8.6 | 1,185 | 1,180 | 35.0 | about 1,500 |
| 1,700 | 128 | 177 | 9.4 | 1,155 | 1,149 | 34.5 | about 1,470 |
| 1,800 | 152 | 199 | 10.3 | 1,124 | 1,118 | 34.1 | about 1,440 |
| 1,900 | 178 | 224 | 11.2 | 1,092 | 1,084 | 33.6 | about 1,400 |
| 2,000 | 206 | 251 | 12.2 | 1,057 | 1,048 | 33.0 | about 1,350 |
| 2,100 | 237 | 282 | 13.4 | 1,019 | 1,009 | 32.4 | about 1,300 |
| 2,200 | 271 | 316 | 14.6 | 977 | 965 | 31.6 | about 1,240 |
| 2,300 | 312 | 358 | 16.0 | 931 | 915 | 30.6 | about 1,170 |
| 2,400 | 358 | 409 | 17.6 | 877 | 857 | 29.4 | about 1,090 |
| 2,500 | 421 | 480 | 19.8 | 811 | 777 | 27.7 | about 970 |
| 2,600 | 522 | 619 | 23.7 | 708 | - | - | - |

How the game table and the dial compare:

- On the **low arc**, the game table's elevation is higher than the dial setting for the same range, by 45 to 97 mils (about 50 in the middle of the range, 97 at 2,600 m). The gap is largest at the short end and at the very top of the range.
- On the **high arc**, the game table is slightly lower than the dial, by 2 to 5 mils over most of the range and by up to 34 mils at 2,500 m.
- The gap is not a fixed shift on the SPH-2. The sight and the stored table use the same range function, but the sight gives it the altitude of the gun above sea level (as far as the code shows), while the table matches a start about 3 m high. Because the firing altitude is an input, the mils for a range depend on how high the gun sits. Simulated, a 2,000 m low-arc shot needs 250 mils fired from 3 m, 224 from 50 m and 197 from 100 m. This altitude effect is why the community calculator's dial readings and the stored table differ by 40 to 60 mils on the low arc. The altitude the calculator used is not known. The game table also lists settings the dial cannot reach: its low arc starts at 20 mrad for 600 m, but the dial's lowest setting, 20 mils, already lands at 1,181 m, and its high arc runs to 1,400 mrad for 700 m, while the dial stops at 1,390 mils (780 m).
- The game's travel times fit the flight maths at the game table's own elevation. On the high arc the simulator is within 0.1 to 0.4 s of the game (under 2 percent). On the low arc the game takes 0.5 to 1.6 s longer than the simulator, and the simulator lands 18 to 283 m short of the game table's range at the same elevation. The high-arc fit is good and the low-arc fit is loose, especially at the shortest ranges.

Reading the table:

- Near the top of the range, a small change in mils moves the low-arc shell a long way. From 2,500 m to 2,600 m is about 100 mils.
- At mid range the low arc needs much less change. From 1,500 m to 1,600 m is 21 mils (84 to 105).
- The high arc stays in the air for 28 to 37 s. The low arc is in the air for about 5 to 24 s (5.7 s at 1,200 m, 19.8 s at 2,500 m). A moving target is a low-arc job. A shell that must clear a wall or a ridge is a high-arc job.

### Height difference and hull tilt

The table assumes the target is at the same height as the gun. A target higher or lower than the gun lands the shell short or long.

- The calculator has a height correction for the low arc. Its high-arc height correction is experimental and off by default.
- The CV Artillery Computer uses terrain heights for the same correction. Three logged shots at targets about 100 m higher landed within about 20 m.
- Shots fired without a known height difference overshot by about 70 m on average.

Hull tilt may change where the shell lands, and no game code that corrects for it was found. The MIL pointer reads the turret's own elevation relative to the hull, not the angle above the horizon; the two are equal only on level ground. The range function that the game uses for the dial takes only the dial value and adds no hull pitch, and no place where the game does add it was found. In the simulator's comparison against real shots (an estimate), adding the hull's pitch to the elevation setting halved the median miss, from 59 m to 34 m. So park the SPH-2 level, or add the hull's pitch to the setting by hand on a slope. The SPH-2 also has a stabilized state that it can enter only when it is almost stopped and on a slope of 20 degrees or less; switching it on takes 2.0 s. It does not level the barrel, and the data does not say whether it changes the hull's pitch, so a slope may still change the shot.

### Stabilizing the hull

The SPH-2 hull has a stabilized state. Entering it takes 2.0 s and leaving it takes 1.0 s. The game allows stabilizing only when the vehicle is almost stopped (speed at most 0.1, no unit given) and the ground under it is at most 20 degrees steep. While the hull is stabilized it cannot move, and the gun cannot fire while the state is changing. A hard enough impact (an impulse of at least 200,000, no unit given) takes the hull out of the stabilized state. The stabilized state does not level the barrel, so a slope still changes the shot.

### How consistent the gun is

The gun itself is very consistent. Repeated shots with the same setting landed within about 4 m of each other, with a worst case of 12 m. If a shot misses, the setting is the likely cause, not randomness.

### The shell's flight

Two shells exist for the SPH-2. Both are the "155mm HE Shell" in the game.

| Shell | Mass | Drag value | Camera | Notes |
|---|---:|---:|---|---|
| Expensive | 19 kg | 2.5 | Follows the shell in flight | The SPH-2 starts with this shell |
| Standard | 70 kg | 80 | None | With the game's flight maths it cannot fly further than about 810 m (estimated) |

The Expensive camera follows the shell, then detaches and zooms out after a while, with a 4 s fade.

The Expensive shell can also be steered after it leaves the barrel, but only sideways: vertical input is ignored (a static reading of the shell's settings). Each tick, the steering input is scaled by 0.02. The Standard shell has no steering. The stored range table was computed for the Expensive shell.

All shells launch at 300 m/s and fall under gravity of 9.8 m/s². Air drag slows them a great deal. Without drag, the same launch would carry the shell about 9 km. With drag, the Expensive shell tops out near 2.6 km (simulator estimate). A shell disappears after 40 s of flight.

The longest flat-ground shot the simulator found with the Expensive shell is about 2,580 m, fired at about 37° (about 645 mils). It takes about 24 s (the game table gives 23.7 s for 2,600 m), peaks at about 728 m and lands at about 113 m/s.

The stats sheet gives the SPH-2 gun an "effective range" of 10,000 m. That is not the real reach. The longest range measured in game is 2,629 m.

## Tips that follow from the numbers

- **Use the bearing tape, not the compass box.** The compass box at the top shows a whole-degree number that the CV Artillery Computer measured at about 1.3° less than the bearing tape. Aim with the tape.
- **Fire a sighting shot, then correct.** Mark where the shell lands on the map and compare it with the target. On the low arc, add mils to go further. On the high arc, add mils to go shorter.
- **Watch the Expensive shell's camera.** It shows the landing point, which is the fastest way to find your error.
- **Correct for height.** If the target is much higher or lower than the gun, use the height correction in the calculator or the CV Artillery Computer.

## What is not known

- The source of the 16.8 mrad offset. The 16.8 mil offset has no known source other than its stored value. The dial values are the ones measured in game and checked against impacts, so use them.
- Why the game table's low-arc travel times run 0.5 to 1.6 s longer than the flight maths gives at the same elevation, while the high-arc times agree.

- Whether the game adds hull pitch anywhere in the shot. None of the code paths read so far does; the simulator's comparison is an estimate, not a measurement in game.
- The high-arc height correction. The calculator's version is experimental and off by default.
- The effect of wind. The simulator uses flat ground and no wind, and its median miss against 87 logged real shots was about 59 m. Treat the simulator's apex heights as estimates.
- Why the stats sheet gives 10,000 m as the effective range when the measured reach is 2,629 m.
- Where the Standard shell fits in play. The game's flight maths say it cannot fly the measured ranges, so this article does not cover it further.

## See also

- [SPH-2](../vehicles/sph-2.md)
- [Aiming the SPH-2](../guides/aiming-the-sph-2.md)
- [L81 Mortar](../building/l81-mortar.md)
- [Ballistics](ballistics.md)

## Sources

- [Artillery shell flight data](../../game-features/Wardogs_ArtilleryShellFlight_v1.md): shell masses, drag values, camera and the range tables
- [Projectile flight: drag and gravity](../../pipelines/Wardogs_ProjectileFlight_v1.md)
- [All vehicles: stats and damage](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [SPH-2](../vehicles/sph-2.md)
- [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence): dial settings, arcs, ranges and height correction
- [CV Artillery Computer](https://github.com/Kiyogitpy/cv-artillery-computer) (MIT licence): map coordinates, compass and bearing readings, and terrain height correction
- SPH-2 weapon data: the game table (elevation, impact distance, travel time)
- [artillery_range_tables.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/artillery_range_tables.py): prints the game tables and compares them with the dial readings and the simulator
- [shell_sim.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/shell_sim.py): flight simulator for the apex heights and miss estimates
- [Round 21 artillery range check](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round21-artillery-range-check.md): the comparison against 87 logged shots
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): how the SPH-2 sight labels its mil marks, and the mil scale.
- [Round 40 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-weapons.md): mil offset (16.8 mrad), dial versus range table, firing altitude, Expensive shell
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the dial's pitch reference (corrected in round 46), the SPH-2 stabilized state and the Expensive shell's steering
- [Round 45 wiki evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-a.md): the Expensive shell steers sideways only, input scaled by 0.02 per tick
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
