---
title: "Wood base"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A wood base structure built with any hammer from 15 Build Supplies, with 735 HP, placed inside a friendly base radius."
---

# Wood base

| Wood base | |
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
| Internal name | `DA_Buildable_WoodBase` |
{: .wiki-infobox }

The Wood base is a 735 HP structure that any hammer can build. It takes the same damage as the [Sandbag Wall](sandbag-wall.md), but unlike the Sandbag Wall it must be placed inside a friendly base radius.

## Overview

The Wood base costs 15 Build Supplies and has 735 HP. The export gives no display name for it, so this article uses the plain name "Wood base". It has no separate parts.

The reward tables have no cash entry for the Wood base.

## Building it

- **Cost:** 15 Build Supplies.
- **Hammers:** Small, Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check. What those two checks test is not yet known.
- **Build stages:** Five, at 0, 20, 45, 70 and 100% of progress. The earlier stages have 16, 14 and 47 weak spots, and the 70% stage has 56. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

The Wood base is cover and an obstacle. The data gives it no effect beyond its health and how it takes damage.

## Durability

The Wood base uses the same damage row as the Sandbag Wall. See [Sandbag Wall](sandbag-wall.md#durability) for the full reading.

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +650% | 7.5 times |
| C4 | +200% | 3 times |
| IEDs | +500% | 6 times |

The data does not say how many hits a Wood base takes to destroy, so that number is not yet known.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Wood base | 735 | 175 | 8 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to the Wood base's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Sandbag Wall](sandbag-wall.md): the structure with the same health and damage numbers
- [Barbed Wire](barbed-wire.md): the small structures that do not need a base radius

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row and placement conditions
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
