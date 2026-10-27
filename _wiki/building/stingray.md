---
redirect_from: ["/wiki/equipment/stingray/"]
title: "Stingray"
parent: "Building"
group: "Emplacements"
description: "A buildable stationary emplacement whose ammunition is listed as UAV, built with a Large Hammer from 650 Build Supplies."
---

# Stingray

| Stingray | |
|---|---|
| ![Stingray]({{ '/assets/img/icons/other-tacticalmap-textures/T_UI_MapTracker_Phalanx.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Stationary emplacement |
| **Weapon** | |
| Gun | Main barrel |
| Ammunition | UAV (drone projectile) |
| Fire mode | Semi-automatic |
| Rate | 50 rounds/min |
| Effective range | 10,000 m (stats sheet; not the real reach) |
| Range table | 80 to 697 m (in the files; nothing reads it) |
| Reload | None (0.0 s; 1.0 s start and end delay) |
| Starting ammunition | 0 |
| Restock | 900 Mechanical Supplies and 5,000 cash, per drone |
| Lock-on | Air vehicles only; 2.0 s to lock, fires 0.5 s after lock |
| **Building** | |
| Build cost | 650 Build Supplies |
| Health | 3,000 HP |
| Hammer | Large Hammer |
| Internal name | STN_05 |
{: .wiki-infobox }

The Stingray is a buildable stationary emplacement with a main barrel that fires UAV projectiles. The game lists its ammunition as "UAV", so it appears to be a drone launcher, though the data does not describe the projectile in plain words. It is built with a Large Hammer from 650 Build Supplies and has 3,000 HP.

## Overview

The Stingray starts with no ammunition and needs a restock before it can fire. The restock takes 900 Mechanical Supplies (the Spare Parts supply) and 5,000 cash, the largest restock of the stationary weapons in the data. The match interface has a drone reload screen for this emplacement.

## Effects

### Weapon

The barrel is listed at 50 rounds/min in semi-automatic mode, with an effective range of 10,000 m. The barrel has no reload step: its reload time is 0.0 s. It has a 1.0 s start delay and a 1.0 s end delay.

The data does not give a windup time or a bullet speed that this article can check against play.

### Targeting

The Stingray is a lock-on weapon. Its target list covers air vehicles only, including the Little Bird family, the Havoc and the fixed-wing airplane. It takes 2.0 s to lock onto a target, and it fires 0.5 s after the lock. The lock only decides whether the weapon can fire. A target's flares do not clear it. The flare pull works only on guided missiles, and the Stingray's drone is not one of them: it is a camera projectile that the player flies with steer, boost and brake inputs, and its data sets no guidance. So flares do not pull the drone off course (read from the game's data and code, not tested in play; see [Countermeasures and flares](../vehicles/countermeasures-and-flares.md)).

### Range table

The "effective range" of 10,000 m on the stats sheet is not the real reach. The game files hold a range table for the barrel, the same kind of table the [L81 Mortar](l81-mortar.md) and the [SPH-2](../vehicles/sph-2.md) have. It has 17 rows. Each pairs a firing elevation in milliradians (mrad) with the distance the shot lands at and its travel time, and the table's shape is the mortar's. It should not be read as the Stingray's reach: the mortar's and the SPH-2's aiming displays read their tables, but the Stingray has no such display, and no Blueprint or other game file reads this one (inferred; code that reads data in a way the files do not show was not excluded). The weapon fires a drone, not a shell on a fixed arc.

| Range (m) | Game table (mrad) | Travel time (s) |
|---:|---:|---:|
| 697 | -500 | 15.9 |
| 677 | -450 | 16.6 |
| 654 | -400 | 17.2 |
| 629 | -350 | 17.9 |
| 600 | -300 | 20.0 |
| 568 | -250 | 19.0 |
| 535 | -200 | 19.5 |
| 498 | -150 | 20.0 |
| 458 | -100 | 20.5 |
| 417 | -50 | 20.9 |
| 372 | 0 | 21.2 |
| 325 | 50 | 21.6 |
| 275 | 100 | 21.9 |
| 224 | 150 | 22.1 |
| 170 | 200 | 22.3 |
| 113 | 250 | 22.4 |
| 80 | 300 | 22.0 |

The table is laid out like the L81 Mortar's: the same elevations (-500 to 300 mrad) and exactly the same travel times, but the Stingray lands 13 to 38 m further from -500 to 200 mrad (697 m against 684 m at the longest setting, 372 m against 340 m at 0 mrad). The two tables come together at the end: 3 m apart at 250 mrad and both 80 m at 300 mrad. The table gives no dial settings, and none are known for the Stingray, so a dial value for a given range is not known. The out-of-pattern travel time at -300 mrad (20.0 s) is also in the mortar's table. The travel times are read as seconds. Why the distances are longer is not stated in any file. As nothing reads the table, the most likely reading is that it is a copy of the mortar's table with its distances adjusted by hand and left unused (inferred).

### Drone projectile

Each shot is a drone that flies out and detonates. Its collision box is about 93 by 92 by 38 cm, and its camera has a 50 degree field of view. The drone deals 120 damage in its blast, with a 10 m outer radius and a 5 m effective radius, a minimum explosive damage of 15 and a falloff of 0.45 between them. It also deals 100 blunt damage. The drone arms 0.1 s after launch. Its typical speed is 150 m/s, and under thrust it reaches 220 m/s. The data gives a maximum lifetime of 500 without a unit.

Explosives against the Stingray's own damage entries: C4 does +300 % and IED +400 % (the table's amounts; the frag grenade entry is +0 %). Other entries on the same row apply too. See [Vehicle inputs and explosive effects](../../game-features/Wardogs_VehicleInputsAndExplosiveEffects_v1.md), section 4.

## Use and timing

The Stingray uses the same placement rules as the other stationary weapons: it is built with a Large Hammer, and its placement conditions check the Forward Operating Base bounds, a ladder check (not within 1 m of a ladder) and a safe zone check (not within 3 m of a safe zone or while standing in one). The [Building](../building.md) page describes these rules.

Because the emplacement starts with no ammunition, the first use in a match depends on a restock. One restock gives one drone (derived: the data does not write a drone count per restock, so the engine's default of one is used). The Stingray has no reload step: its reload time is 0.0 s, with a 1.0 s delay at the start and at the end. The restock is a purchase scene ("Purchase Stingray"), and how long that scene lasts in play is not stored in the files.

## Destroying it

The Stingray has 3,000 HP. Explosives that burst within their inner radius take this many hits to destroy it: MAAWS 4, RPG-7 4, IED 2, C4 3, M67 frag 4. The counts are worked out from the damage rules, not timed in play, and assume full health with no repair. See the [Anti-Vehicle Guide](../guides/anti-vehicle-guide.md#emplacements).

## Cost

| Item | Value |
|---|---|
| Build Supplies | 650 |
| Health | 3,000 HP |
| Hammer | Large Hammer |

The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the [Building](../building.md) page explains.

## Season 2 changes

- Build cost went from 150 to 650 Build Supplies, the largest change of any stationary weapon.
- One damage entry was added to the emplacement's damage table for 125 mm rocket hits (amount -50), and another for 20x102 mm cannon hits (amount -70). The amounts use the same units as the other entries in the [vehicle damage](../vehicles/vehicle-damage.md) table.

## See also

- [Building](../building.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Artillery](../game-mechanics/artillery.md): how the SPH-2 fires, for comparison
- [Talon 9K-SAM](talon-9k-sam.md), [Vanguard CIWS](vanguard-ciws.md), [MG Nest](mg-nest.md), [Loudspeaker](loudspeaker.md) and [L81 Mortar](l81-mortar.md): the other stationary emplacements

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the drone projectile numbers and the explosive entries for the Stingray
- [Vehicle inputs and explosive effects (round 41 data)](../../game-features/Wardogs_VehicleInputsAndExplosiveEffects_v1.md): input tuning, drone projectile and explosive rows
- [Buildables](../../game-features/Wardogs_Buildables_v1.md): Build Supplies cost, health, hammer and placement conditions
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the barrel's rate, fire mode, effective range and damage table
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): the UAV ammunition name
- [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost and damage table changes
- Stingray weapon data: restock, ammunition and the 17-row range table (mrad, impact distance, travel time)
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): lock-on timings, the restock cost and the drone count.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
