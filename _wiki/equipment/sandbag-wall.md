---
title: "Sandbag Wall"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A low cover wall built with any hammer from 15 Build Supplies, with 735 HP."
---

# Sandbag Wall

| Sandbag Wall | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 15 Build Supplies |
| Build time | Not yet known |
| Health | 735 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -80% |
| Grenades | +0% |
| Rockets | +650% |
| C4 | +200% |
| IEDs | +500% |
| Internal name | `DA_Buildable_SandbagWall` |
{: .wiki-infobox }

The Sandbag Wall is a low cover wall that any of the three hammers can build. It is cheap and has 735 HP. Bullets do little to it, but rockets, C4 and IEDs do much more damage than they do to most other walls.

## Overview

The Sandbag Wall costs 15 Build Supplies and has 735 HP. It has no separate parts. It is one of the small structures, so it can be placed without a Forward Operating Base radius, as explained under [Building it](#building-it).

The reward tables give 100 cash for destroying an enemy Sandbag Wall. They give no cash for building or placing one.

## Building it

- **Cost:** 15 Build Supplies, whichever hammer builds it. Nothing is charged at placement. See [Buildables](buildables.md) for how Build Supplies are bought.
- **Hammers:** Small, Medium or Large.
- **Placement:** The Sandbag Wall is one of the four small structures (with the [Barbed Wire](barbed-wire.md), [Recon Tent](recon-tent.md) and [Hedgehog](hedgehog.md)). It does not need a friendly base radius, but it cannot be placed inside an enemy base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 100.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 14, 12, 10 and 8 weak spots, in that order. A hammer hit on a weak spot adds more progress (see [Buildables](buildables.md#weak-spots)).
- **Build time:** Not published in seconds.

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | 30 | 15 | 10 |
| Hits to repair from zero health | 30 | 15 | 10 |
| Hits to dismantle (your own) | 5 | 4 | 3 |

The hits assume normal hits, not weak-spot hits. See [Buildables](buildables.md#building) for how the hit amounts work.

## What it does

The Sandbag Wall is cover and an obstacle. The data gives it no effect beyond its health and how it takes damage.

## Durability

The table shows how much of each damage source reaches the wall. A change of -85% means 15% of the damage gets through. A change of +650% means the damage is multiplied by 7.5. The full reading is in the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +650% | 7.5 times |
| C4 | +200% | 3 times |
| IEDs | +500% | 6 times |

These are the entries that match one source on its own. The data also has entries for particular ammunition and calibers, which this table does not show. The data does not say how many hits a Sandbag Wall takes to destroy, so the number of rockets or bullets it needs is not yet known.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Sandbag Wall | 735 | 175 | 8 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to the Sandbag Wall's cost or health. Season 2 changed six values in three entries of the buildable damage table, but the data does not say which structures those entries affect.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Wood base](wood-base.md): a structure with the same health and damage numbers
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage walls

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable damage table changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
