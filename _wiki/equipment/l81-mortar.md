---
title: "L81 Mortar"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A buildable mortar emplacement with one firing arc and a range of 132 to 684 m, built with a Large Hammer from 600 Build Supplies."
---

# L81 Mortar

| L81 Mortar | |
|---|---|
| **General** | |
| Type | Stationary mortar emplacement |
| Arcs | One |
| **Range** | |
| Minimum range | 132 m |
| Maximum range | 684 m |
| Travel time | 15.9 to 22.4 s (game table) |
| **Building** | |
| Build cost | 600 Build Supplies |
| Health | 3,000 HP |
| Hammer | Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-mortar) |
| Internal name | STN_03 |
{: .wiki-infobox }

The L81 Mortar is a stationary emplacement that fires mortar rounds over short distances. It is built like the other stationary weapons, with a hammer, and it has a shorter reach than the [SPH-2](../vehicles/sph-2.md) artillery gun. For the long-range artillery system, see [Artillery](../game-mechanics/artillery.md).

## Overview

The mortar can hit targets from 132 m to 684 m away. It has one firing arc only, so each range has a single elevation setting. The setting to dial for each range, and the game's own range table with travel times, are in the table below.

## Effects

### Weapon

The gun fires 120x800 mm shells in semi-automatic mode at 50 rounds/min. It reloads in 4.5 s and starts with 3 shells. A restock takes 150 Ammo Supplies. The data gives a windup time of 2.5 s before each shot.

### Range and elevation

The game files hold a range table for the mortar: 17 rows, each giving a firing elevation in milliradians (mrad), the distance the shell lands at and its travel time. The "dial" column is the setting on the sight's MIL scale as measured in game by the community calculator [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence); the calculator gives the dial range as 150 to 850 mils. **Dial the numbers in the "dial" column.** The calculator reads between its rows in a straight line.

| Range (m) | Dial (mils) | Game table (mrad) | Travel time (s) |
|---:|---:|---:|---:|
| 684 | 150 | -500 | 15.9 |
| 661 | 200 | -450 | 16.6 |
| 637 | 248 | -400 | 17.2 |
| 609 | 300 | -350 | 17.9 |
| 578 | 350 | -300 | 20.0 |
| 545 | 400 | -250 | 19.0 |
| 510 | 449 | -200 | 19.5 |
| 470 | 500 | -150 | 20.0 |
| 430 | 549 | -100 | 20.5 |
| 385 | 600 | -50 | 20.9 |
| 340 | 649 | 0 | 21.2 |
| 290 | 700 | 50 | 21.6 |
| 240 | 749 | 100 | 21.9 |
| 187 | 800 | 150 | 22.1 |
| 132 | 850 | 200 | 22.3 |
| 110 | 900 | 250 | 22.4 |
| 80 | 950 | 300 | 22.0 |

Mils fall as range rises, so a longer shot needs a lower elevation setting. A shell is in the air for 16 to 22 s: the longer the shot, the shorter the flight, which is the opposite of the SPH-2 low arc. The data stores the travel times as plain numbers, and they are read here as seconds.

### How the game table and the dial compare

At the same range, the dial setting is the game table's elevation plus 650, to within 2 mils, on every one of the 17 rows. The two lists therefore agree on the shape of the mortar's range curve and differ by a fixed shift. Why the scales are shifted by 650 is not known. Because the match is so close, the two should not be counted as two independent measurements.

The travel time in the -300 mrad row (20.0 s) breaks the pattern of its neighbours (17.9 s before it, 19.0 s after), and is probably a data oddity. The cause is not known.

### Minimum range

The game table goes down to 80 m. The calculator gives 132 m as the minimum range. The two fit together this way: 132 m is the row at 850 mils, the end of the mortar's dial range (150 to 850 mils). The game table has two more rows beyond that stop, 110 m at 900 mils and 80 m at 950 mils on the dial scale, which the measured dial does not reach. Whether the mortar can actually fire at those settings is not known, so treat 132 m as the shortest range you can set.

## Season 2 changes

- Build cost went from 150 to 600 Build Supplies.
- The restock needed went from 75 to 150 Ammo Supplies.
- The windup time went from 0.85 s to 2.5 s.
- Two damage entries were added to the mortar's damage table: one for 20x102 mm cannon hits (amount -70) and one for 125 mm rocket hits (amount -50). The amounts use the same units as the other entries in the [vehicle damage](../vehicles/vehicle-damage.md) table.

## Cost

| Item | Value |
|---|---|
| Build Supplies | 600 |
| Health | 3,000 HP |
| Hammer | Large Hammer |

The Build Supplies cost is taken from the [Buildables](buildables.md) article, which lists the stationary weapons with their Build Supplies, health and hammer. The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the Buildables article explains.

## See also

- [Artillery](../game-mechanics/artillery.md): how the SPH-2 fires, with its arcs and firing table
- [Buildables](buildables.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Talon 9K-SAM](talon-9k-sam.md), [Vanguard CIWS](vanguard-ciws.md), [Stingray](stingray.md), [MG Nest](mg-nest.md) and [Loudspeaker](loudspeaker.md): the other stationary emplacements
- [SPH-2](../vehicles/sph-2.md)
- [Aiming the SPH-2](../guides/aiming-the-sph-2.md)

## Sources

- [Buildables](buildables.md): build cost, health and hammer (stationary weapons table)
- [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence): range, one arc and dial settings, measured in game
- [artillery_range_tables.py](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/artillery_range_tables.py): prints the table and compares it with the dial readings
- [Mortar weapon extension data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/Weapons/WeaponExtensions/WE_STN_03_Heavy_MainBarrel.json): the 17-row range table (mrad, impact distance, travel time), reload, restock, windup and starting shells
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the mortar's rate and damage table
- [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost, restock, windup and damage table changes
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
