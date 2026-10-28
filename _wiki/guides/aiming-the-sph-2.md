---
title: "Aiming the SPH-2"
parent: "Guides"
description: "How to read the SPH-2's gun-sight instruments (map readout, minimap, bearing tape, compass box, MIL scale and tilt dial), run a fire mission step by step, and correct your aim after a miss."
---

# Aiming the SPH-2

The SPH-2 is only as accurate as the numbers you put on its gun. The gun-sight gives you six instruments for that: the map cursor readout, the minimap, the bearing tape, the compass box, the MIL scale and the tilt dial. Each one shows a different number, and they are not equally precise. This guide explains what each instrument shows and how precise it is, then walks through a fire mission and how to correct a miss. For the gun itself, see the [SPH-2](../vehicles/sph-2.md) article. For the shell's flight and the full firing table, see [Artillery](../game-mechanics/artillery.md).

## The instruments

The table gives the short version. The numbers below it are measured on the game screen; see [Sources](#sources) for where each one comes from.

| Instrument | Where | Shows | Precision |
|---|---|---|---|
| Map cursor readout | Beside the crosshair on the big map | Position as x and y, in map units | 0.01 unit (1 m) |
| Minimap | Bottom-left corner of the screen, and in the gun sight | Terrain around your vehicle, north up | About 1.48 m per screen pixel at 1440p |
| Bearing tape | Scale across the top of the gun sight | Compass bearing of the gun | 3° ticks, read to 0.1° |
| Compass box | Top centre of the gun sight | Whole-degree heading | Whole degrees, and about 1.3° low |
| MIL scale | Sliding scale on the right of the gun sight | Elevation in mils | 10 mil ticks |
| Tilt dial | Bottom of the gun and driver views | Hull pitch and roll, and turret angle | About 7° per pitch tick (rough) |

### Map cursor readout

The map cursor readout is the line of text beside the crosshair on the big map. It reads as `x98.99 y50.77`. One map unit is 100 m, so the two decimal places are metres. Read `x98.99` as 9,899 m east and `y50.77` as 5,077 m north. The readout is the most precise number in the whole sight: it is accurate to 0.01 unit, which is 1 m.

Use it for: getting the exact x and y of your gun and of the target, which you need for distance and bearing.

### Minimap

The minimap is the square in the bottom-left corner of the screen. It is north up, and your vehicle icon sits at its centre. It is also shown inside the SPH-2 gun sight. At 2560x1440 one screen pixel of the minimap is about 1.48 m. The icon points toward the barrel end: its long axis, away from the black dot, is the hull's compass heading. That heading matches the compass within 2°.

Use it for: seeing the ground between you and the target, and for checking that the hull faces the way you think it does.

### Bearing tape

The bearing tape is the scale across the top of the gun sight. It reads "225 240 255" and so on, and bearings grow to the right. There is a tick every 3°. Every fifth tick is long and labelled, at each multiple of 15°. The bearing directly under the centre of the sight is where the gun points, and you can read it to a tenth of a degree.

Use it for: traversing the gun onto a bearing. This is the instrument to aim with.

### Compass box

The compass box is the whole-degree number at the top centre of the gun sight, for example `353 N`. It reads about 1.3° less than the bearing tape. The difference was measured at 1.28° over 23 frames. Ten shots aimed by the compass box landed about 1.3° to the right of the target.

Use it for: a quick check of your general direction. Do not use it to aim a shot. Aim with the bearing tape.

### MIL scale

The MIL scale is the sliding scale on the right of the gun sight. It is labelled "50 mils", "60 mils" and so on, with a thousands comma from "1,000 mils". There is a tick every 10 mils. The elevation set on the gun is the value on the dashed centre line. A tick above the centre line is a lower mil value, and a tick below it is a higher one. The barrel's true elevation is the dial reading plus 16.8 mrad (about 0.96 degrees). The game adds this offset itself, so you set the dial value and add nothing.

Use it for: setting the elevation from the firing table. The value on the dashed centre line is what the gun will fire at.

The MIL scale reads the turret's own elevation relative to the hull, not the angle above the horizon. On level ground the hull and the horizon agree, so the two are the same there. On a slope the scale does not include the hull's tilt, and no place where the game adds the hull's pitch to the mil value was found.

### Tilt dial

The tilt dial is a tank icon between two scales of seven ticks, at the bottom of the gun and driver views. The two triangles outside the scales move up and down together with the hull's pitch: when the nose tips up, the triangles move up. The angle of the bars shows the roll. One tick of pitch is about 7°. This figure was measured on one slope, so treat it as a rough guide. The dial also shows the turret angle relative to the hull. The hull heading is the sight bearing minus the turret angle.

Use it for: checking how far the hull is tilted, so you can correct the elevation for it (see [Correcting your aim](#correcting-your-aim)).

## Fire mission step by step

1. **Read your position and the target's.** Open the big map and move the cursor onto your vehicle icon. Write down the x and y from the map cursor readout. Then move the cursor onto the target and write down its x and y.

2. **Work out the distance and the bearing.** Take the differences in x and y (target minus gun). The distance in metres is the straight line between the two points, multiplied by 100. The bearing is the angle clockwise from north. You can work this out by hand, or use one of the [tools](#tools).

   For example, a gun at x 10.00 y 20.00 and a target at x 22.00 y 36.00 gives dx = 12 and dy = 16. The distance is 20 units, which is 2,000 m. The bearing is 36.9°.

3. **Choose the arc.** Every range from about 1,181 m to 2,629 m can be hit two ways. The low arc is flat and fast, between 20 and about 600 mils. The high arc is steep and slow, between about 610 and 1,390 mils. Use the low arc if the target can move or you need the shell to arrive quickly. Use the high arc to clear a wall, a ridge or other cover. Between 780 m and 1,181 m only the high arc reaches the target.

4. **Stabilize the hull, if you can.** Stabilizing takes 2.0 s and releasing it takes 1.0 s. The hull must be almost stopped (speed at most 0.1) on ground at most 20 degrees steep to stabilize. While stabilized the hull cannot move, and the gun cannot fire while the state changes. A hard enough impact releases it.

5. **Traverse to the bearing.** In the gun view, turn the turret until the centre of the bearing tape reads your bearing. Use the bearing tape, not the compass box.

6. **Set the elevation.** Look up the mils for your range in the "dial" columns of the firing table on the [Artillery](../game-mechanics/artillery.md) article (not the game table's mrad columns, which are a different list), then set the MIL scale's centre line to that value. Some sample rows:

   | Range (m) | Low arc (mils) | High arc (mils) |
   |---:|---:|---:|
   | 1,000 | - | 1,340 |
   | 1,500 | 84 | 1,213 |
   | 2,000 | 206 | 1,057 |

   If the target is higher or lower than your gun, or the hull is tilted, correct the setting as described below.

7. **Fire, then watch the shell.** With the Expensive shell, the camera follows the round in flight. Mark where it lands on the map and compare the crater with the target. The same table gives the travel time: about 12 s at 2,000 m on the low arc, about 33 s on the high arc. The Expensive shell can also be steered in flight with a small input (scaled to 0.02). The Standard shell cannot be steered.

8. **Adjust.** On the low arc, more mils means the shell lands further. On the high arc, more mils means the shell lands shorter. Change the setting by a little at a time and fire again.

## Correcting your aim

Use the Expensive shell's camera to see where the shell lands. Watch it fall, then find the crater on the map. Compare the crater with the target and work out how far off it is and in which direction. Most misses have one of three causes.

- **Height difference.** The firing table assumes the target is at the same height as the gun. A target higher or lower than the gun makes the shell land short or long. The community calculator has a height correction table for the low arc, and the CV Artillery Computer uses terrain heights to apply it. For a target about 100 m higher, three logged shots landed within about 20 m. Correct for height if you can, or move so that you fire at a similar height.

- **Hull tilt.** The MIL pointer is measured from the hull, and no place where the game adds the hull's pitch to the elevation was found, so on a slope the setting may not account for the tilt. In a comparison of real impacts, adding the hull's pitch from the tilt dial to the elevation halved the median miss, from 59 m to 34 m. This is an estimate from a flight simulator, not a measurement in game, but it suggests the tilt dial is worth checking before you fire and the hull's pitch worth correcting by hand. The simplest fix is to park the vehicle level. Stabilizing the hull does not level the barrel.

- **Firing altitude.** The mils for a range depend on how high the gun sits above sea level. Simulated, a 2,000 m low-arc shot needs 250 mils fired from 3 m, 224 from 50 m and 197 from 100 m. A gun on high ground can therefore need tens of mils less than a table measured at another height. The altitude the community table was measured at is not known.
- **Aiming by the compass box.** The compass box reads about 1.3° less than the bearing tape. A shot aimed by the box lands about 1.3° to the side. Aim with the bearing tape, and you remove that error.

The gun itself is very consistent. Repeat shots with the same setting landed within about 4 m of each other, and never more than 12 m apart. If your shots keep landing in the same place, the setting is wrong, not the gun, so adjust the setting rather than repeating the shot.

## Tools

- **wardogs-calculator** by apollyon-sys is a community calculator for the SPH-2 and the L81 Mortar. It gives the mils for a range and a height correction table for the low arc. It is released under the MIT licence. Source: [github.com/apollyon-sys/wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator).
- **CV Artillery Computer** is a community project by Kiyogitpy that reads the game screen and works out the firing solution. It only reads the screen. It never presses keys and never moves the mouse. It is released under the MIT licence. Source: [github.com/Kiyogitpy/cv-artillery-computer](https://github.com/Kiyogitpy/cv-artillery-computer).

## Where these numbers come from

Numbers in this guide come from four kinds of source.

- **Screen measurements (CV Artillery Computer).** The instrument readings (map readout precision, minimap scale, bearing tape ticks and the 1.28° compass box offset, MIL scale ticks, the tilt dial's tick size) were measured on the game screen at 2560x1440 by the [CV Artillery Computer](https://github.com/Kiyogitpy/cv-artillery-computer). The pixel values, such as 1.48 m per minimap pixel, depend on resolution and may differ on another screen.
- **Measured in game (wardogs-calculator).** The firing table (mils for each range, the two arcs, the 780 m minimum and the 2,629 m longest range) and the height correction table were measured in game by the [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys.
- **Source.** The gun's range table (the travel times, and an elevation for each range that does not match the dial settings, for a reason not known), the stats sheet (50 rounds/min, 25.0 s reload, 10,000 m stated effective range, starting ammunition), the shell's name and variants, the launch speed, gravity and the 40 s flight limit come from the game. See [Artillery shell flight](../../game-features/Wardogs_ArtilleryShellFlight_v1.md), [Projectile flight](../../pipelines/Wardogs_ProjectileFlight_v1.md), [All vehicles stats and damage](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md) and the [SPH-2](../vehicles/sph-2.md) article.
- **Simulator estimates.** The high-arc top height, the drag figures and the hull tilt comparison (59 m median miss falling to 34 m) are estimates worked out with a flight simulator, [shell_sim.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/shell_sim.py), on flat ground with no wind. The simulator's median miss against 87 real logged shots was about 59 m. The full write-up is in the [round 21 range check](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round21-artillery-range-check.md).

The stats sheet gives an effective range of 10,000 m, but the longest shot measured in game reaches 2,629 m. The real reach is the measured figure.

## See also

- [Artillery](../game-mechanics/artillery.md)
- [L81 Mortar](../building/l81-mortar.md)
- [SPH-2](../vehicles/sph-2.md)
- [Spotting](../game-mechanics/spotting.md)

## Sources

- [Artillery shell flight data](../../game-features/Wardogs_ArtilleryShellFlight_v1.md)
- [Projectile flight](../../pipelines/Wardogs_ProjectileFlight_v1.md)
- [All vehicles stats and damage](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Artillery](../game-mechanics/artillery.md)
- [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence)
- [CV Artillery Computer](https://github.com/Kiyogitpy/cv-artillery-computer) (MIT licence)
- [shell_sim.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/shell_sim.py)
- [Round 21 artillery range check](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round21-artillery-range-check.md)
- [Round 40 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-weapons.md): mil offset (16.8 mrad) and firing altitude
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): the dial's pitch reference (corrected in round 46), the SPH-2 stabilized state and the Expensive shell's steering
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
