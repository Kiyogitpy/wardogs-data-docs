---
title: "Bremer Wall"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A large wall built only with the Large Hammer, from 32 Build Supplies in Season 2, with 6,500 HP."
---

# Bremer Wall

| Bremer Wall | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Large |
| **Building** | |
| Build cost | 32 Build Supplies (15 in Season 1) |
| Build time | Not yet known |
| Health | 6,500 HP |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +50% |
| Rockets | +250% |
| C4 | +280% |
| IEDs | +350% |
| Internal name | `DA_Buildable_BremmerWall` |
{: .wiki-infobox }

The Bremer Wall has 6,500 HP, the most of any wall in the data, and only the Large Hammer can build it. Bullets and melee do 20% of their normal damage to it.

## Overview

The Bremer Wall costs 32 Build Supplies and has 6,500 HP. It has no separate parts.

The reward tables have no cash entry for the Bremer Wall.

## Building it

- **Cost:** 32 Build Supplies. In Season 1 it cost 15.
- **Hammers:** Large only.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 15, 20, 15 and 19 weak spots. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

The Bremer Wall is cover and an obstacle. The data gives it no effect beyond its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -80% | 20% |
| Melee | -80% | 20% |
| Grenades | +50% | 1.5 times |
| Rockets | +250% | 3.5 times |
| C4 | +280% | 3.8 times |
| IEDs | +350% | 4.5 times |

The data does not say how many hits the Bremer Wall takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Bremer Wall | 6,500 | 1161 | 44 | 13 | 7 |

## Season 2 changes

- Build cost went from 15 to 32 Build Supplies.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Hesco Walls](hesco-walls.md): the smaller barriers
- [Hedgehog](hedgehog.md): another high-health barrier

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row and placement conditions
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost change
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
