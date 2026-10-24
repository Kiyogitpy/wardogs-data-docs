---
title: "Drill Rig"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A fuel-powered rig built with the Large Hammer from 2,750 Build Supplies in Season 2, with 2,500 HP, that runs only on Fuel Supplies inside a placement zone."
---

# Drill Rig

| Drill Rig | |
|---|---|
| **General** | |
| Category | Fuel-powered rig |
| Hammer | Large |
| **Building** | |
| Build cost | 2,750 Build Supplies (2,250 in Season 1) |
| Build time | Not yet known |
| Health | 2,500 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -80% |
| Grenades | +0% |
| Rockets | +850% |
| C4 | +500% |
| IEDs | +1,500% |
| Internal name | `DA_Buildable_HotzoneMagnet` |
{: .wiki-infobox }

The Drill Rig is the most expensive structure that a player can build with a hammer. It only works inside a placement zone within a control zone, and it runs on Fuel Supplies. Once started, it works for a set run time that depends on the fuel added to it.

## Overview

The Drill Rig costs 2,750 Build Supplies and has 2,500 HP. It has no separate parts.

The reward tables give 3,000 cash for destroying an enemy Drill Rig. They give no cash for placing one.

## Building it

- **Cost:** 2,750 Build Supplies.
- **Hammers:** Large only.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It must also be inside a placement zone, and that zone must be inside a control zone. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 70, 79, 98 and 95 weak spots. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

After it is placed, the Drill Rig has a start delay of 15 (probably seconds). It needs fuel to run. Fuel Supplies are added to it through an interaction, and it holds up to 10,000 fuel.

| Setting | Value |
|---|---:|
| Delay after placing | 15 (the data does not state the unit) |
| Minimum fuel to run | 2,000 |
| Maximum fuel | 10,000 |
| Run time per fuel unit | 0.03 (the data does not state the unit) |
| Recharge duration | 900 (the data does not state the unit) |

Each fuel unit buys 0.03 of run time, which is probably seconds. The run time for a full tank is therefore not yet known in seconds. What the rig does to the hot zone is not yet known.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +850% | 9.5 times |
| C4 | +500% | 6 times |
| IEDs | +1,500% | 16 times |

The data does not say how many hits the Drill Rig takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Season 2 changes

- Build cost went from 2,250 to 2,750 Build Supplies.
- Minimum fuel to run went from 1,500 to 2,000.
- Maximum fuel went from 7,500 to 10,000.
- Run time per fuel unit went from 0.05 to 0.03.

The recharge duration of 900 is not listed as changed.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Utility Items](utility-items.md): the Fuel Supplies that the rig runs on
- [Forward Operating Base](forward-operating-base.md): the base that the rig must be placed inside

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions, fuel settings and cash rewards
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the cost and fuel changes
