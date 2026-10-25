---
redirect_from: ["/wiki/equipment/wood-base/"]
title: "Wood base"
parent: "Building"
group: "Structures"
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
| Build time | 30 hits Small (17.0 s), 15 hits Medium (8.5 s), 10 hits Large (8.8 s). Derived from the hammer swing timing, not timed in play. |
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

Destroying an enemy Wood base pays 15 cash and 5 Role XP. The placement rewards for a structure placed inside a base are a flat 5 cash (10 in a hot zone). The data also has Built, Placed and Placed in FOB reward tables, and the game's lookup takes the first table that has a matching row (Built is checked first). But no code in the game client asks for these rows, so which amount is actually paid for a placement is decided outside the client, most likely by the game's servers; this structure has no row of its own in any of them (see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md) and the [round 48 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round48.md)).

## Building it

- **Cost:** 15 Build Supplies, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Small, Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 4.
- **Build stages:** Five, at 0, 20, 45, 70 and 100% of progress. The earlier stages have 16, 14 and 47 weak spots, and the 70% stage has 56. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | 30 (about 17.0 s) | 15 (about 8.5 s) | 10 (about 8.8 s) |
| Hits to repair from zero health | 30 | 15 | 10 |
| Hits to dismantle (your own) | 5 | 4 | 3 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The hits assume normal hits, not weak-spot hits. See [Buildables](../building.md#building) for how the hit amounts work.

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

The table below gives the hits it takes to destroy, for each source.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Wood base | 735 | 175 | 55 | 2 | 1 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to the Wood base's cost or health.

## See also

- [Buildables](../building.md): costs, hammers and placement for every structure
- [Sandbag Wall](sandbag-wall.md): the structure with the same health and damage numbers
- [Barbed Wire](barbed-wire.md): the small structures that do not need a base radius

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row and placement conditions
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
