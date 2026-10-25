---
title: "Refuel and Repair Stations"
parent: "Equipment"
group: "Emplacements and buildables"
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
| Build time | Not yet known |
| Health | 1,600 HP each |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +50% |
| Rockets | +1,500% |
| C4 | +600% |
| IEDs | +1,000% (Repair Station); no single entry (Refuel Station) |
| Internal name | `DA_Buildable_RefuelStation`, `DA_Buildable_RepairStation` |
{: .wiki-infobox }

The Refuel Station and the Repair Station are vehicle service structures that only the Large Hammer can build. The Refuel Station uses Fuel Supplies and the Repair Station uses Mechanical Supplies. Each can be placed once per Forward Operating Base. They take much more rocket and C4 damage than most structures.

## Overview

Both stations cost 200 Build Supplies and have 1,600 HP. Neither has separate parts.

The Refuel Station works with Fuel Supplies, and the Repair Station works with Mechanical Supplies. The item text for each says it is needed to refuel or repair vehicles, and that it needs a friendly base radius to use. Both stations store the same repair speed figure, 13.33. It is the structure's own hammer repair-speed multiplier, not a vehicle repair rate (see [Repair and vehicle parts](../vehicles/repair-and-vehicle-parts.md)).

The reward tables have no cash entry for either station.

## Building it

- **Cost:** 200 Build Supplies each, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Large only.
- **Limit:** One Refuel Station and one Repair Station per Forward Operating Base. Each counts toward the base's limit.
- **Placement:** Each must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 100.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The Refuel Station has 15, 14, 27 and 14 weak spots in its first four stages. The Repair Station has 16, 16, 16 and 15. A hammer hit on a weak spot adds more progress (see [Buildables](buildables.md#weak-spots)).
- **Build time:** Not published in seconds.

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | cannot place | 134 |
| Hits to repair from zero health | 31 | 16 | 11 |
| Hits to dismantle (your own) | 11 | 8 | 7 |

The Large Hammer is the only one that can place a station. The repair and dismantle hits for the other hammers are what their hits do; the data does not check them for this structure. The build count assumes normal hits, and hitting weak spots brings it down. The repair hits are for a finished station; the repair multiplier is 13.3.

## What it does

The stations refuel and repair vehicles in the Forward Operating Base radius. Each has a Fast and a Max restock:

| Station | Restock | Amount per restock | Time | Cost | Supplies per restock |
|---|---|---:|---:|---:|---:|
| Refuel Station | Fast | 5% of the tank | 3 s | 75 cash | 5 Fuel Supplies |
| Refuel Station | Max | up to 100% of the tank | 9 s | 1,500 cash | 5 Fuel Supplies |
| Repair Station | Fast | 5% of health | 3 s | 100 cash | 5 Mechanical Supplies |
| Repair Station | Max | up to 100% of health | 9 s | 2,000 cash | 5 Mechanical Supplies |

The times are the stored values. Whether a Max restock is shorter when the tank or health is nearly full is not known. The Refuel Station has a refuel start and stop sound, and the Repair Station has a repair start and stop sound.

## Durability

| Source | Refuel Station | Repair Station |
|---|---:|---:|
| Bullets | -80% | -80% |
| Melee | -80% | -80% |
| Grenades | +50% | +50% |
| Rockets | +1,500% | +1,500% |
| C4 | +600% | +600% |
| IEDs | no single entry | +1,000% |

Rockets do 16 times their normal damage to either station. The Refuel Station has no single IED entry in the data, so the IED damage it takes is not yet known from this table. The hits either station takes to destroy are derived in the table below. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Refuel Station | 1,600 | 286 | 11 | 1 | 1 |
| Repair Station | 1,600 | 286 | 11 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to either station's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Utility Items](utility-items.md): the Fuel Supplies and Mechanical Supplies that the stations use
- [Vehicle damage](../vehicles/vehicle-damage.md): how vehicles take damage, for the vehicles these stations serve

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, damage rows, placement limits, the repair multiplier and the item descriptions
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md): the names of the FOB supply containers, including Fuel Supplies and Mechanical Supplies
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): restock amounts, times and costs for both stations, and the derived hits to destroy.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
