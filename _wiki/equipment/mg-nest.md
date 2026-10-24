---
title: "MG Nest"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A buildable stationary machine gun firing .50 cal tracer rounds, built with a Large Hammer from 650 Build Supplies."
---

# MG Nest

| MG Nest | |
|---|---|
| **General** | |
| Type | Stationary emplacement |
| **Weapon** | |
| Gun | Mounted machine gun |
| Ammunition | .50 cal tracer |
| Rate | Not yet known |
| Effective range | Not yet known |
| Reload | 8.0 s |
| Starting ammunition | 60 rounds |
| Restock | 200 Ammo Supplies for 60 rounds |
| **Building** | |
| Build cost | 650 Build Supplies |
| Health | 1,800 HP (finished gun); 3,000 HP while under construction |
| Hammer | Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-mgnest) |
| Internal name | STN_06 |
{: .wiki-infobox }

The MG Nest is a buildable stationary machine gun that fires .50 cal tracer rounds. It is built with a Large Hammer from 650 Build Supplies. Its weapon is the only stationary gun in the data that uses the .50 cal round, and it is restocked in batches of 60 rounds.

## Overview

The MG Nest starts with 60 rounds and is restocked with Ammo Supplies. A restock takes 200 Ammo Supplies and gives 60 rounds. The data does not give the gun's rate of fire or effective range, so those are not yet known.

## Effects

### Weapon

The gun reloads in 8.0 s. The data gives no rate of fire and no effective range for the emplacement, so this article cannot say how quickly it fires or how far it reaches.

### Health

The finished MG Nest has 1,800 HP. Shots hit the gun as a vehicle, and its vehicle damage table gives it a pool of 1,800 HP. The Buildables data gives 3,000 HP to the build plot, the structure that exists while the gun is being built. So 3,000 is the health of the plot under construction, and 1,800 is the health of the finished gun. One small caveat: the step that carries the plot's health over to the finished gun was not fully read, so that link is not confirmed. The [vehicle damage](../vehicles/vehicle-damage.md) page explains how the damage table works.

## Use and timing

The MG Nest uses the same placement rules as the other stationary weapons: it is built with a Large Hammer, and its placement conditions check the Forward Operating Base bounds, a ladder-bounds rule and a safe-zone rule. The [Buildables](buildables.md) page describes these rules.

## Cost

| Item | Value |
|---|---|
| Build Supplies | 650 |
| Health | 1,800 HP (finished gun; see Health) |
| Hammer | Large Hammer |

The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the [Buildables](buildables.md) page explains.

## Season 2 changes

The Season 2 changes page lists no value changes for the MG Nest's build cost or its weapon.

## See also

- [Buildables](buildables.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Talon 9K-SAM](talon-9k-sam.md), [Vanguard CIWS](vanguard-ciws.md), [Stingray](stingray.md), [Loudspeaker](loudspeaker.md) and [L81 Mortar](l81-mortar.md): the other stationary emplacements
- [Vehicle weapons](../vehicles/vehicle-weapons.md): the machine guns mounted on vehicles

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): Build Supplies cost, health, hammer and placement conditions
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the damage table and its health value
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): the 1,800 HP value used by the damage system
- [MG Nest weapon extension data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/Weapons/WeaponExtensions/WE_STN_06_MountedMachineGun.json): reload, restock and ammunition
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): health of the finished MG Nest and of the build plot.
