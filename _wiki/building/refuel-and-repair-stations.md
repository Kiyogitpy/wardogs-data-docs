---
redirect_from: ["/wiki/equipment/refuel-and-repair-stations/"]
title: "Refuel and Repair Stations"
parent: "Building"
group: "Structures"
description: "Two vehicle service stations built with the Large Hammer from 200 Build Supplies each, with 1,600 HP, one of each allowed per Forward Operating Base."
---

# Refuel and Repair Stations

| Refuel and Repair Stations | |
|---|---|
| **General** | |
| Category | Vehicle service station |
| Hammer | Large |
| **Building** | |
| Build cost | 200 Build Supplies each |
| Build time | 134 hits Large (about 118.3 s). Derived from the hammer swing timing, not timed in play. |
| Health | 1,600 HP each |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +50% |
| Rockets | +1,500% |
| C4 | +600% |
| IEDs | +1,000% (Repair Station); +0% (Refuel Station) |
| Internal name | `DA_Buildable_RefuelStation`, `DA_Buildable_RepairStation` |
{: .wiki-infobox }

The Refuel Station and the Repair Station are vehicle service structures that only the Large Hammer can build. The Refuel Station uses Fuel Supplies and the Repair Station uses Mechanical Supplies. Each can be placed once per Forward Operating Base. They take much more rocket and C4 damage than most structures.

## Overview

Both stations cost 200 Build Supplies and have 1,600 HP. Neither has separate parts.

The Refuel Station works with Fuel Supplies, and the Repair Station works with Mechanical Supplies. The item text for each says it is needed to refuel or repair vehicles, and that it needs a friendly base radius to use. Both stations store the same repair speed figure, 13.33. It is the structure's own hammer repair-speed multiplier, not a vehicle repair rate (see [Repair and vehicle parts](../vehicles/repair-and-vehicle-parts.md)).

Destroying an enemy Refuel Station or Repair Station pays 200 cash and 50 Role XP each.

## Building it

- **Cost:** 200 Build Supplies each, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Large only.
- **Limit:** One Refuel Station and one Repair Station per Forward Operating Base. Each counts toward the base's limit.
- **Placement:** Each must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 100.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The Refuel Station has 15, 14, 27 and 14 weak spots in its first four stages. The Repair Station has 16, 16, 16 and 15. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | cannot place | 134 (about 118.3 s) |
| Hits to repair from zero health | 31 | 16 | 11 |
| Hits to dismantle (your own) | 11 | 8 | 7 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The Large Hammer is the only one that can place a station. The repair and dismantle hits for the other hammers are what their hits do; the data does not check them for this structure. The build count assumes normal hits, and hitting weak spots brings it down. The repair hits are for a finished station; the repair multiplier is 13.3.

## What it does

The stations refuel and repair vehicles in the Forward Operating Base radius. Each has a Fast and a Max restock:

| Station | Restock | Amount per restock | Time | Cost | Supplies per restock |
|---|---|---:|---:|---:|---:|
| Refuel Station | Fast | 5% of the tank | 3 s | 75 cash | 5 Fuel Supplies |
| Refuel Station | Max | up to 100% of the tank | 9 s | 1,500 cash | 5 Fuel Supplies |
| Repair Station | Fast | 5% of health | 3 s | 100 cash | 5 Mechanical Supplies |
| Repair Station | Max | up to 100% of health | 9 s | 2,000 cash | 5 Mechanical Supplies |

The times are the stored values. Whether a Max restock is shorter when the tank or health is nearly full is not known. The charge is different: a Max restock is charged for the share it restores. The cash cost in the table is the full-tank or full-health price, scaled by the share restored and rounded up to a multiple of 50. The supplies used are the item's cost times the amount restored, so a nearly full target costs little, and a restock cannot give more than the FOB has in stock. This is a static reading of the restock code (round 41), not checked in play. The Refuel Station has a refuel start and stop sound, and the Repair Station has a repair start and stop sound.

## Durability

| Source | Refuel Station | Repair Station |
|---|---:|---:|
| Bullets | -80% | -80% |
| Melee | -80% | -80% |
| Grenades | +50% | +50% |
| Rockets | +1,500% | +1,500% |
| C4 | +600% | +600% |
| IEDs | +0% (300 per hit) | +1,000% |

Rockets do 16 times their normal damage to either station. The Refuel Station has no IED entry of its own, so an IED does its base 300 damage to it: 6 IED hits destroy it. The Repair Station has its own IED entry (+1,000%), so 1 IED hit destroys it. The other hits either station takes to destroy are derived in the table below. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Refuel Station | 1,600 | 286 | 89 | 1 | 1 | 1 | 6 |
| Repair Station | 1,600 | 286 | 89 | 1 | 1 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to either station's cost or health.

## See also

- [Buildables](../building.md): costs, hammers and placement for every structure
- [Utility Items](../equipment/utility-items.md): the Fuel Supplies and Mechanical Supplies that the stations use
- [Vehicle damage](../vehicles/vehicle-damage.md): how vehicles take damage, for the vehicles these stations serve

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the Max restock charge rule (the supplies and cash scale with the amount restored)
- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, damage rows, placement limits, the repair multiplier and the item descriptions
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md): the names of the FOB supply containers, including Fuel Supplies and Mechanical Supplies
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): restock amounts, times and costs for both stations, and the derived hits to destroy.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
