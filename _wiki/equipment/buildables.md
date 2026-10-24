---
title: Buildables
parent: "Equipment"
group: "Emplacements and buildables"
description: "Everything players can build with hammers: Build Supplies cost, health, which hammer builds it, placement rules and how each damage type affects it."
---

# Buildables

| Buildables | |
|---|---|
| Structures | 32 definitions, including the parts of larger structures |
| Hammers | Small, Medium, Large |
| Stationary weapons | 6, built with the Large Hammer (Medium for the Loudspeaker) |
| Cost | Build Supplies |
| Health range | 250 HP (Barbed Wire) to 15,000 HP (Forward Operating Base) |
{: .wiki-infobox }

Players build structures such as walls, doors, bunkers and stations with a hammer. The hammer's size decides which structures it can build. Each structure costs Build Supplies, has a health value, and takes damage from weapons and explosives in its own way. Most structures must be placed inside a Forward Operating Base radius, so the base comes first.

## Overview

Each hammer builds a set of structures:

| Hammer | Shop cash | Build speed (shop text) | Can build |
|---|---:|---|---|
| Small Hammer | 100 | Slow | Barbed Wire, Recon Tent, Builder's Radio, Hesco Block (Small), Sandbag Wall, Hedgehog, Wood base |
| Medium Hammer | 800 | Moderate | Door, Gate, Hesco Wall, Hesco Block (Large), Shelter, and the parts of these |
| Large Hammer | 2,400 | Fast | Every structure above, plus Bremer Wall, Bunker, Recon Tower, Indirect Fire Shelter, Drill Rig, Refuel Station and Repair Station |

The Large Hammer is the only hammer that can place the Bunker, Recon Tower, Indirect Fire Shelter, Bremer Wall, Drill Rig, Refuel Station and Repair Station. The stationary weapons, listed below, are built with the Large Hammer, and the Loudspeaker can also be built with the Medium Hammer.

The export gives no display name for the Shelter and the Wood base, so this page uses the plain names "Shelter" and "Wood base".

### Structures

Parts of a larger structure, such as a floor or a roof, are placed with their parent and cannot be picked on their own. They are shown on the parent's row.

| Structure | Build Supplies | Health (HP) | Hammers | Parts |
|---|---:|---:|---|---|
| Sandbag Wall | 15 | 735 | S, M, L | |
| Wood base | 15 | 735 | S, M, L | |
| Barbed Wire | 7 | 250 | S, M, L | |
| Recon Tent | 7 | 300 | S, M, L | |
| Hedgehog | 22 | 4,500 | S, M, L | |
| Hesco Block (Small) | 15 | 1,600 | S, M, L | |
| Builder's Radio | 20 | 1,000 | S, M, L | |
| Hesco Block (Large) | 22 | 2,250 | M, L | |
| Hesco Wall | 75 | 4,600 | M, L | |
| Shelter | 250 | 2,250 | M, L | |
| Door | 80 | 2,200 | M, L | Door-only section 22 / 500 HP; top section 22 / 500 HP |
| Gate | 200 | 5,320 | M, L | Left and right halves 85 / 5,320 HP each; ramp 85 / 6,500 HP |
| Bremer Wall | 32 | 6,500 | L | |
| Bunker | 200 | 5,000 | L | Floor and roof 10 / 2,250 HP each |
| Recon Tower | 200 | 5,000 | L | Base floor, first floor and roof 10 / 2,250 HP each |
| Indirect Fire Shelter | 200 | 5,000 | L | Floor and ceiling 10 / 2,250 HP each |
| Refuel Station | 200 | 1,600 | L | |
| Repair Station | 200 | 1,600 | L | |
| Drill Rig | 2,750 | 2,500 | L | |
| Forward Operating Base | 30 | 15,000 | own item | Shop price 7,500 cash; placed from its own item, not a hammer |

Stationary weapons are built like structures, with the same placement rules:

| Stationary weapon | Build Supplies | Health (HP) | Hammers |
|---|---:|---:|---|
| Talon 9K-SAM | 650 | 3,000 | L |
| Vanguard CIWS | 1,200 | 5,000 | L |
| L81 Mortar | 600 | 3,000 | L |
| Loudspeaker | 200 | 1,000 | M, L |
| Stingray | 650 | 3,000 | L |
| MG Nest | 650 | 3,000 | L |

### Individual emplacements

Each stationary weapon has its own article, with its gun, ammunition, restock and Season 2 changes:

- [Talon 9K-SAM](talon-9k-sam.md): heavy mounted machine gun, 72 mm rounds
- [Vanguard CIWS](vanguard-ciws.md): automatic 20x102 mm cannon
- [L81 Mortar](l81-mortar.md): 120x800 mm shells, with an elevation table and flight data
- [Loudspeaker](loudspeaker.md): no weapon in the data
- [Stingray](stingray.md): UAV ammunition
- [MG Nest](mg-nest.md): .50 cal tracer rounds

## Effects

### Damage by source

Each structure has a damage row that changes how much damage each source does to it. The table shows the change for each source. A change of -85% means 15% of the damage is left. A change of +650% means the damage is multiplied by 7.5. A plus sign means more damage.

| Structure | HP | Melee | Bullets | Grenades | Rockets | C4 | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sandbag Wall | 735 | -80% | -85% | +0% | +650% | +200% | +500% |
| Hesco Block (Small) | 1,600 | -80% | -80% | +50% | +120% | +220% | +500% |
| Hesco Wall | 4,600 | +0% | -80% | +0% | +200% | +150% | +400% |
| Barbed Wire | 250 | -28% | -85% | +0% | +200% | +150% | +400% |
| Bunker | 5,000 | -10% | -80% | -50% | +45% | +50% | +200% |
| Recon Tower | 5,000 | -10% | -80% | -50% | +45% | +50% | +200% |
| Door | 2,200 | -80% | -85% | +0% | +650% | +200% | +800% |
| Gate | 5,320 | -80% | -85% | +0% | +850% | +1,000% | +2,000% |
| Hedgehog | 4,500 | -80% | -85% | -50% | +450% | +500% | +1,000% |
| Drill Rig | 2,500 | -80% | -85% | +0% | +850% | +500% | +1,500% |
| Builder's Radio | 1,000 | +70% | -85% | +500% | +1,000% | +400% | +800% |
| Forward Operating Base | 15,000 | -80% | -80% | +200% | +1,400% | +1,250% | +5,000% |

Plain reading: a Bunker takes about a fifth of the bullet damage, and rockets do their normal damage plus 45%. Rockets, C4 and IEDs multiply the damage to most structures. The Forward Operating Base is the most exposed to IEDs, at +5,000%, which is 51 times the normal damage. These are the damage entries that match one source on its own. Other entries, for particular weapons and ammunition, can also apply, so these figures are a first estimate. The data does not yet show how many hits each structure takes to destroy.

The full table for every structure is on the [Buildables](../../game-features/Wardogs_Buildables_v1.md) data page.

One field of the Forward Operating Base's data is set to "do not take damage". How that interacts with its 15,000 HP is not yet known.

### Build stages

A structure is built in stages from 0 to 100%, and each stage shows a new part of the structure. Most multi-stage structures have five stages, at 0, 25, 50, 75 and 100%. The Door uses 0, 30, 60, 80 and 100%, and the Wood base 0, 20, 45, 70 and 100%. Parts such as floors and roofs have only one stage. Earlier stages have weak spots, which are shown as marked points on the half-built structure. What the weak spots do is not yet known.

## Use and timing

### Building

Building needs Build Supplies and a hammer. Each hammer swing adds progress, and the hit that lands on a weak spot adds more:

| Hammer | Build amount per hit | Build amount on a weak spot | Season 2 weak-spot amount |
|---|---:|---:|---|
| Small | 0.5 | 3 | not listed as changed |
| Medium | 1 | 5 | 6 became 5 |
| Large | 1.5 | 8 | 10 became 8 |

These are the amounts the data gives for each hit. How they add up to a finished structure is not yet known, so how long a full build takes is also not yet known. The shop text describes the hammers as slow, moderate and fast. Dismantling works at 150, 200 and 250 per second for the small, medium and large hammer.

### Placement

- The build point must be within 6 m of the player.
- Most structures must be placed inside a friendly Forward Operating Base radius. The exceptions are the small structures: Barbed Wire, Recon Tent, Sandbag Wall and Hedgehog. Those cannot be placed inside an enemy base radius.
- Builder's Radio: up to 4 per Forward Operating Base.
- Refuel Station and Repair Station: 1 per Forward Operating Base each.
- Drill Rig: only inside a placement zone within a control zone.
- The rules for placing the Forward Operating Base itself are not yet known.

### Drill Rig

The Drill Rig needs fuel to run. After placement it waits 15 s before it can start. It needs at least 2,000 fuel to run, each fuel unit buys 0.03 of run time, and it holds up to 10,000 fuel. The data gives a recharge time of 900 for the rig. The data does not state the units for these values, so the run time per fuel unit is not yet known in seconds.

What the Drill Rig does to the hot zone is not yet known.

### Refuel and repair

The Refuel Station and Repair Station work with Fuel Supplies and Mechanical Supplies. Their refuel and repair rates are not yet known.

## Cost

The cost column in the Structures table is the Build Supplies cost. The data does not yet show exactly when Build Supplies are taken, at placement or while building. Build Supplies cost 10 cash each in the shop and are sold in lots of 50.

Hammers cost 2,400 cash (Large), 800 (Medium) and 100 (Small). The Forward Operating Base costs 7,500 cash.

## Season 2 changes

The following build costs changed in Season 2:

| Structure | Season 1 | Season 2 |
|---|---:|---:|
| Indirect Fire Shelter | 100 | 200 |
| Bremer Wall | 15 | 32 |
| Bunker | 100 | 200 |
| Recon Tower | 100 | 200 |
| Door | 22 | 80 |
| Gate | 85 | 200 |
| Drill Rig | 2,250 | 2,750 |

The Drill Rig's fuel values changed too: the minimum fuel to run went from 1,500 to 2,000, the maximum fuel from 7,500 to 10,000, and the run time per fuel unit from 0.05 to 0.03.

Several entries in the buildable damage table changed by 5 to 17 percentage points. The Season 2 data does not say which structures they apply to.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), for the explosives that damage structures
- [Fire, Smoke and Flash](fire-smoke-and-flash.md), for the Molotov fire
- [Utility Items](utility-items.md), for the Fuel and Mechanical Supplies, and the Light and Heavy Drills
- [Vehicles data page](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md), for the vehicles that the Refuel and Repair Stations serve
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): costs, health, stages, damage rows, placement rules and the Drill Rig settings
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): hammer prices, build speed text and supply prices
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): build cost, hammer and damage row changes
