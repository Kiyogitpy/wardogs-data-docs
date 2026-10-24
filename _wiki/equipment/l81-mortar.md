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
| Flight-time data | 17 points in the game files (see Flight time) |
| **Building** | |
| Build cost | 600 Build Supplies |
| Health | 3,000 HP |
| Hammer | Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-mortar) |
| Internal name | STN_03 |
{: .wiki-infobox }

The L81 Mortar is a stationary emplacement that fires mortar rounds over short distances. It is built like the other stationary weapons, with a hammer, and it has a shorter reach than the [SPH-2](../vehicles/sph-2.md) artillery gun. For the long-range artillery system, see [Artillery](../game-mechanics/artillery.md).

## Overview

The mortar can hit targets from 132 m to 684 m away. It has one firing arc only, so each range has a single elevation setting. That setting is listed in mils for each range below. The game files also hold a range table for the shell, which is summarised under Flight time.

## Effects

### Weapon

The gun fires 120x800 mm shells in semi-automatic mode at 50 rounds/min. It reloads in 4.5 s and starts with 3 shells. A restock takes 150 Ammo Supplies. The data gives a windup time of 2.5 s before each shot.

### Range and elevation

The table gives the elevation in mils for each range on flat ground, as measured in game by the community calculator [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence). The calculator gives the range as 132 m to 684 m and the sight as 150 to 850 mils; the table is its mil values at every 50 m. The calculator reads between its rows in a straight line.

| Range (m) | Mils | | Range (m) | Mils |
|---:|---:|---|---:|---:|
| 150 | 831 | | 450 | 525 |
| 200 | 788 | | 500 | 461 |
| 250 | 740 | | 550 | 393 |
| 300 | 690 | | 600 | 315 |
| 350 | 638 | | 650 | 222 |
| 400 | 583 | | | |

Mils fall as range rises, so a longer shot needs a lower elevation setting. The shortest and longest shots, 132 m and 684 m, are outside the rows above.

### Flight time

The mortar's weapon data holds an artillery range table with 17 points. Each point pairs a firing setting in milliradians with the impact distance and the travel time of the shell. The export does not state the unit of the travel time, so the times below are read as seconds and should be checked in game.

- At the longest setting (-500 milliradians), the shell lands 684 m away after about 15.9 s.
- At 0 milliradians, it lands 340 m away after about 21.3 s.
- At 200 milliradians, it lands 132 m away after about 22.3 s.
- At the shortest impact in the table (300 milliradians), it lands 80 m away after about 22.0 s.

The table's milliradian values use a different scale from the mil values in the elevation table above, and the two have not been matched point for point. The table's shortest impact, 80 m, is also below the 132 m minimum given in the infobox, which comes from the community calculator. This article keeps both figures and does not choose between them.

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
- [wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator) by apollyon-sys (MIT licence): range, one-arc and mils table, measured in game
- [Mortar weapon extension data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/Weapons/WeaponExtensions/WE_STN_03_Heavy_MainBarrel.json): the 17-point artillery range table, reload, restock, windup and starting shells
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the mortar's rate and damage table
- [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost, restock, windup and damage table changes
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
