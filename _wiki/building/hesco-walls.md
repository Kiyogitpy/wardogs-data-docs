---
redirect_from: ["/wiki/equipment/hesco-walls/"]
title: "Hesco Walls"
parent: "Building"
group: "Structures"
description: "Three Hesco barriers, the Small and Large Hesco Blocks and the Hesco Wall, built with a hammer from 15 to 75 Build Supplies, with 1,600 to 4,600 HP."
---

# Hesco Walls

| Hesco Walls | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Small, Medium or Large, by variant |
| **Building** | |
| Build cost | 15 to 75 Build Supplies, by variant |
| Build time | Small Block: 30 hits Small (17.0 s), 15 hits Medium (8.5 s), 10 hits Large (8.8 s). Large Block: 22 hits Medium (12.5 s), 15 hits Large (13.2 s). Hesco Wall: 75 hits Medium (42.5 s), 50 hits Large (44.1 s). Derived from the hammer swing timing, not timed in play. |
| Health | 1,600 to 4,600 HP, by variant |
| **Damage** | |
| Bullets | -80% (all three) |
| Melee | -80% to +0% |
| Grenades | +0% to +50% |
| Rockets | +80% to +200% |
| C4 | +150% to +220% |
| IEDs | +300% to +500% |
| Internal name | `DA_Buildable_HBlock`, `DA_Buildable_TallHBlock`, `DA_Buildable_HBlock_QuadWall` |
{: .wiki-infobox }

The Hesco Walls are three barriers: the Small Hesco Block, the Large Hesco Block and the Hesco Wall. The Small Block is the cheapest and weakest, and the Hesco Wall is the most expensive and has the most health. Each has its own cost, health and damage numbers, so they are listed in tables below.

## Overview

| Variant | Hammers | Build Supplies | Health (HP) | Cash for placing | Cash for destroying an enemy one |
|---|---|---:|---:|---:|---:|
| Hesco Block (Small) | Small, Medium, Large | 15 | 1,600 | 100 | 100 |
| Hesco Block (Large) | Medium, Large | 22 | 2,250 | 200 | 100 |
| Hesco Wall | Medium, Large | 75 | 4,600 | 500 | 125 |

## Building it

- **Cost:** See the table above. The cost is the same whichever hammer builds it, and nothing is charged at placement.
- **Hammers:** The Small Hesco Block can be built with any hammer. The Large Block and the Hesco Wall need a Medium or Large Hammer.
- **Placement:** All three must be inside a friendly Forward Operating Base radius. None can be placed within 3 m of a safe zone or while standing in one, or within 1 m of a ladder.
- **Stack limit:** 5 for the Small Block, 2 for the Large Block and the Hesco Wall.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress, for each variant. The Small Block has 5, 16, 16 and 16 weak spots at the first four stages. The Large Block has 6, 24, 24 and 32. The Hesco Wall has 8, 31, 34 and 69. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Parts:** The Hesco Wall is made of several blocks. When it is finished, it turns into separate Large Hesco Blocks, each with its own health. This is Derived from the stage data (see [Buildables](../building.md#building)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small Block | Large Block | Hesco Wall |
|---|---:|---:|---:|
| Hits to build | 30 (Small, about 17.0 s), 15 (Medium, about 8.5 s), 10 (Large, about 8.8 s) | 22 (Medium, about 12.5 s), 15 (Large, about 13.2 s) | 75 (Medium, about 42.5 s), 50 (Large, about 44.1 s) |
| Hits to repair from zero health | 30 / 15 / 10 | 15 (Medium), 10 (Large) | 15 (Medium), 10 (Large) |
| Hits to dismantle (your own) | 11 / 8 / 7 | 12 (Medium), 9 (Large) | 23 (Medium), 19 (Large) |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The columns for the Small Block read Small / Medium / Large hammer. The other two are Medium and Large only. The build counts assume normal hits, and hitting weak spots brings them down.

## What it does

The Hesco Walls are cover and obstacles. The data gives them no effect beyond their health and how they take damage. The reward tables pay cash for placing and destroying them, as the table above shows.

## Durability

| Source | Small Block | Large Block | Hesco Wall |
|---|---:|---:|---:|
| Bullets | -80% | -80% | -80% |
| Melee | -80% | -80% | +0% |
| Grenades | +50% | +50% | +0% |
| Rockets | +120% | +80% | +200% |
| C4 | +220% | +150% | +150% |
| IEDs | +500% | +300% | +400% |

For the Large Block, rockets do 1.8 times their normal damage, and IEDs do 4 times. For the Hesco Wall, rockets do 3 times and IEDs do 5 times. The full reading of the percentages is in the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic). These are the entries that match one source on its own, so they are a first estimate.

The table below gives the hits it takes to destroy, for each source.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hesco Block (Small) | 1,600 | 286 | 89 | 4 | 8 | 2 | 1 |
| Hesco Block (Large) | 2,250 | 402 | 125 | 7 | 13 | 4 | 2 |
| Hesco Wall | 4,600 | 822 | 256 | 21 | 16 | 8 | 4 |

## Season 2 changes

The Season 2 data lists no change to the cost or health of any Hesco variant.

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Bremer Wall](bremer-wall.md): the largest wall in the data
- [Hedgehog](hedgehog.md): another high-health barrier
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage rows, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
