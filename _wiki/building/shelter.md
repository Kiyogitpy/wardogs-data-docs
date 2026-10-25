---
redirect_from: ["/wiki/equipment/shelter/"]
title: "Shelter"
parent: "Building"
group: "Structures"
description: "A shelter built with a Medium or Large Hammer from 250 Build Supplies, with 2,250 HP."
---

# Shelter

| Shelter | |
|---|---|
| **General** | |
| Category | Shelter |
| Hammer | Medium, Large |
| **Building** | |
| Build cost | 250 Build Supplies |
| Build time | 250 hits Medium (141.8 s), 167 hits Large (147.5 s). Derived from the hammer swing timing, not timed in play. |
| Health | 2,250 HP |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +50% |
| Rockets | +80% |
| C4 | +150% |
| IEDs | +300% |
| Internal name | `DA_Buildable_Shelter` |
{: .wiki-infobox }

The Shelter is a single-piece shelter that a Medium or Large Hammer can build. It costs 250 Build Supplies, the most of any structure that a Medium Hammer can build, and it has 2,250 HP. It is a different structure from the [Indirect Fire Shelter](indirect-fire-shelter.md).

## Overview

The Shelter costs 250 Build Supplies and has 2,250 HP. It has no separate parts. The export gives no display name for it, so this article uses the plain name "Shelter".

Destroying an enemy Shelter pays 250 cash and 65 Role XP. The placement rewards for a structure placed inside a base are a flat 5 cash (10 in a hot zone) in the placement settings, while the reward calculator lists 10 cash for a placed schematic (20 in a hot zone); the two have not been reconciled. The data also has Built, Placed and Placed in FOB reward tables, and the game's lookup takes the first table that has a matching row (Built is checked first). But no code in the game client asks for these rows, so which amount is actually paid for a placement is decided outside the client, most likely by the game's servers; this structure has no row of its own in any of them (see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md) and the [round 48 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round48.md)).

## Building it

- **Cost:** 250 Build Supplies, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 1.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. Each of the first four stages has 24 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | 250 (about 141.8 s) | 167 (about 147.5 s) |
| Hits to repair from zero health | 500 | 250 | 167 |
| Hits to dismantle (your own) | 15 | 12 | 9 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The hits assume normal hits, not weak-spot hits. The Small Hammer cannot place the Shelter, so its build column says so, but the repair and dismantle figures are what its hit does and are not checked in play. See [Buildables](../building.md#building) for how the hit amounts work.

## What it does

The data does not describe its use in play beyond its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -80% | 20% |
| Melee | -80% | 20% |
| Grenades | +50% | 1.5 times |
| Rockets | +80% | 1.8 times |
| C4 | +150% | 2.5 times |
| IEDs | +300% | 4 times |

The table below gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shelter | 2,250 | 402 | 125 | 7 | 13 | 4 | 2 |

## Season 2 changes

The Season 2 data lists no change to the Shelter's cost or health.

## See also

- [Indirect Fire Shelter](indirect-fire-shelter.md): a different, larger shelter
- [Buildables](../building.md): costs, hammers and placement for every structure
- [Hesco Walls](hesco-walls.md): structures that a Medium Hammer can also build

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
