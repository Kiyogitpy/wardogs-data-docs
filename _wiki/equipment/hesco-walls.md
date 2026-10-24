---
title: "Hesco Walls"
parent: "Equipment"
group: "Emplacements and buildables"
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
| Build time | Not yet known |
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

The game's UI name table gives all three the text "HBlock". This article uses the Hesco names from the asset list instead.

## Building it

- **Cost:** See the table above.
- **Hammers:** The Small Hesco Block can be built with any hammer. The Large Block and the Hesco Wall need a Medium or Large Hammer.
- **Placement:** All three must be inside a friendly Forward Operating Base radius. They also pass a ladder bounds check and a safe zone check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress, for each variant. The Small Block has 5, 16, 16 and 16 weak spots at the first four stages. The Large Block has 6, 24, 24 and 32. The Hesco Wall has 8, 31, 34 and 69. What the weak spots do is not yet known.
- **Build time:** Not yet known.

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

The data does not say how many hits any Hesco variant takes to destroy, so that number is not yet known.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Hesco Block (Small) | 1,600 | 286 | 11 | 5 | 2 |
| Hesco Block (Large) | 2,250 | 402 | 15 | 9 | 4 |
| Hesco Wall | 4,600 | 822 | 46 | 11 | 8 |

## Season 2 changes

The Season 2 data lists no change to the cost or health of any Hesco variant.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Bremer Wall](bremer-wall.md): the largest wall in the data
- [Hedgehog](hedgehog.md): another high-health barrier
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage rows, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
