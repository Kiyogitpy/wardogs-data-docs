---
title: "Shelter"
parent: "Equipment"
group: "Emplacements and buildables"
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
| Build time | Not yet known |
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

The reward tables have no cash entry for the Shelter.

## Building it

- **Cost:** 250 Build Supplies.
- **Hammers:** Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. Each of the first four stages has 24 weak spots. What the weak spots do is not yet known.
- **Build time:** Not yet known.

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

The data does not say how many hits the Shelter takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Shelter | 2,250 | 402 | 15 | 9 | 4 |

## Season 2 changes

The Season 2 data lists no change to the Shelter's cost or health.

## See also

- [Indirect Fire Shelter](indirect-fire-shelter.md): a different, larger shelter
- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Hesco Walls](hesco-walls.md): structures that a Medium Hammer can also build

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
