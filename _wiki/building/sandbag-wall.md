---
redirect_from: ["/wiki/equipment/sandbag-wall/"]
title: "Sandbag Wall"
parent: "Building"
group: "Structures"
description: "A low cover wall built with any hammer from 15 Build Supplies, with 735 HP."
---

# Sandbag Wall

| Sandbag Wall | |
|---|---|
| ![Sandbag Wall]({{ '/assets/img/icons/other-buildables-sandbagwall/T_UI_Buildable_SandbagWall.png' | relative_url }}){: .wiki-infobox-img } | |
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
| Internal name | `DA_Buildable_SandbagWall` |
{: .wiki-infobox }

The Sandbag Wall is a low cover wall that any of the three hammers can build. It is cheap and has 735 HP. Bullets do little to it, but rockets, C4 and IEDs do much more damage than they do to most other walls.

## Overview

The Sandbag Wall costs 15 Build Supplies and has 735 HP. It has no separate parts. It is one of the small structures, so it can be placed without a Forward Operating Base radius, as explained under [Building it](#building-it).

Destroying an enemy Sandbag Wall pays 15 cash and 5 Role XP.

## Building it

- **Cost:** 15 Build Supplies, whichever hammer builds it. Nothing is charged at placement. See [Building](../building.md) for how Build Supplies are bought.
- **Hammers:** Small, Medium or Large.
- **Placement:** The Sandbag Wall is one of the four small structures (with the [Barbed Wire](barbed-wire.md), [Recon Tent](recon-tent.md) and [Hedgehog](hedgehog.md)). It does not need a friendly base radius, but it cannot be placed inside an enemy base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 100.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 14, 12, 10 and 8 weak spots, in that order. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | 30 (about 17.0 s) | 15 (about 8.5 s) | 10 (about 8.8 s) |
| Hits to repair from zero health | 30 | 15 | 10 |
| Hits to dismantle (your own) | 5 | 4 | 3 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The hits assume normal hits, not weak-spot hits. See [Buildables](../building.md#building) for how the hit amounts work.

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

These are the entries that match one source on its own. The data also has entries for particular ammunition and calibers, which this table does not show. The table below gives the hits it takes to destroy, for each source.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sandbag Wall | 735 | 175 | 55 | 2 | 1 | 1 | 1 |

## Season 2 changes

- The Season 2 data lists no change to the Sandbag Wall's cost or health.
- The Vanguard CIWS 20 mm cannon went from full damage to x0.20 (13 hits to destroy became 62, derived). The T-72B3's 125 mm shell does half the damage it did: 1 hit to destroy became 2 (derived).

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Wood base](wood-base.md): a structure with the same health and damage numbers
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage walls

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable damage table changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
