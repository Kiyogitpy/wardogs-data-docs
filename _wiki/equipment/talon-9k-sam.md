---
title: "Talon 9K-SAM"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A buildable stationary emplacement with a heavy mounted machine gun, built with a Large Hammer from 650 Build Supplies."
---

# Talon 9K-SAM

| Talon 9K-SAM | |
|---|---|
| **General** | |
| Type | Stationary emplacement |
| **Weapon** | |
| Gun | Heavy mounted machine gun |
| Ammunition | 72 mm |
| Fire mode | Semi-automatic |
| Rate | 100 rounds/min |
| Effective range | 1,000 m |
| Reload | 5.0 s |
| Starting ammunition | 1 |
| **Building** | |
| Build cost | 650 Build Supplies |
| Health | 3,000 HP |
| Hammer | Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-mistral) |
| Internal name | STN_01 |
{: .wiki-infobox }

The Talon 9K-SAM is a stationary emplacement that players build with a Large Hammer. Its weapon is a heavy mounted machine gun that fires 72 mm rounds in single shots. Its name points to an anti-air role. The data also gives it lock-on timings (see Targeting), but it does not list the targets it can lock onto, so this article does not say what it targets.

## Overview

Destroying an enemy Talon 9K-SAM pays 650 cash and 175 Role XP.

The Talon is built from 650 Build Supplies and has 3,000 HP. It is one of six stationary weapons listed on the [Buildables](buildables.md) page, and it is placed with the same rules as the other stationary weapons.

## Effects

### Weapon

The gun fires 100 rounds/min in semi-automatic mode, which is one shot per trigger pull. The data lists an effective range of 1,000 m. The game data gives a reload time of 5.0 s and a starting count of 1 round. The gun is restocked with Ammo Supplies, and a full restock takes 200 of them. The data does not store how many rounds one restock gives, so the engine default of one round is used (derived).

### Targeting

The data gives the emplacement 2.0 s to lock onto a target, and a 0.5 s delay after the lock before it fires. In the client code read, a lock only decides whether a lock-on weapon can fire. The data does not link flares to it (see [Countermeasures and flares](../vehicles/countermeasures-and-flares.md)).

## Use and timing

The Talon uses the same placement rules as the other stationary weapons: it is built with a Large Hammer, and its placement conditions check the Forward Operating Base bounds, a ladder check (not within 1 m of a ladder) and a safe zone check (not within 3 m of a safe zone or while standing in one). The [Buildables](buildables.md) page describes these rules for every structure.

The data does not say how many hits the emplacement takes to destroy in play, beyond its 3,000 HP.

## Cost

| Item | Value |
|---|---|
| Build Supplies | 650 |
| Health | 3,000 HP |
| Hammer | Large Hammer |

The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the [Buildables](buildables.md) page explains.

## Season 2 changes

- Build cost went from 1,000 to 650 Build Supplies.
- Reload went from 2.0 s to 5.0 s.
- The restock needed went from 50 to 200 Ammo Supplies.
- The gamepad rotation sensitivity for the gun went from 30 to 100.
- Two damage entries were added to the emplacement's damage table: one for 125 mm rocket hits (amount +50) and one for 20x102 mm cannon hits (amount -70). The amounts use the same units as the other entries in the [vehicle damage](../vehicles/vehicle-damage.md) table.

## See also

- [Buildables](buildables.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Vanguard CIWS](vanguard-ciws.md), [Stingray](stingray.md), [MG Nest](mg-nest.md), [Loudspeaker](loudspeaker.md) and [L81 Mortar](l81-mortar.md): the other stationary emplacements
- [Vehicle weapons](../vehicles/vehicle-weapons.md): the guns mounted on vehicles

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): Build Supplies cost, health, hammer and placement conditions for the stationary weapons
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the gun's rate, fire mode, effective range and damage table
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md) and [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost, reload, restock and damage table changes
- [Talon weapon extension data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/Weapon/WeaponExtensions/WE_STN_01_Heavy_MountedMachineGun.json): reload, restock and ammunition
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): lock-on timings for the Talon.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
