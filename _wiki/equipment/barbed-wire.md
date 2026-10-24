---
title: "Barbed Wire"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A small wire obstacle built with any hammer from 7 Build Supplies, with the lowest health of any structure at 250 HP."
---

# Barbed Wire

| Barbed Wire | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 7 Build Supplies |
| Build time | Not yet known |
| Health | 250 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -28% |
| Grenades | +0% |
| Rockets | +200% |
| C4 | +150% |
| IEDs | +400% |
| Internal name | `DA_Buildable_BarbedWire` |
{: .wiki-infobox }

Barbed Wire is a cheap wire obstacle that any hammer can build. It costs 7 Build Supplies and has 250 HP, the lowest health of any structure in the data. It takes more melee damage than most walls, and only 15% of bullet damage gets through.

## Overview

Barbed Wire costs 7 Build Supplies and has 250 HP. It has no separate parts.

The reward tables give 10 cash for placing Barbed Wire and 75 cash for destroying an enemy one.

## Building it

- **Cost:** 7 Build Supplies.
- **Hammers:** Small, Medium or Large.
- **Placement:** Barbed Wire is one of the four small structures. It does not need a friendly base radius, but it cannot be placed inside an enemy base radius. It also passes a safe zone check and a ladder bounds check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 10, 11, 11 and 11 weak spots. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

Barbed Wire is an obstacle. The data gives it no effect beyond its health and how it takes damage.

## Durability

A change of -28% means 72% of the melee damage gets through. The other numbers follow the same reading as in the [Sandbag Wall](sandbag-wall.md#durability) article.

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -28% | 72% |
| Grenades | +0% | 100% |
| Rockets | +200% | 3 times |
| C4 | +150% | 2.5 times |
| IEDs | +400% | 5 times |

Barbed Wire's 250 HP is the lowest of any structure. The data does not say how many hits it takes to destroy, so that number is not yet known.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Barbed Wire | 250 | 60 | 3 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to Barbed Wire's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Recon Tent](recon-tent.md) and [Hedgehog](hedgehog.md): the other small structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
