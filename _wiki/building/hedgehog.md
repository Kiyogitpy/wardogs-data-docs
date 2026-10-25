---
redirect_from: ["/wiki/equipment/hedgehog/"]
title: "Hedgehog"
parent: "Building"
group: "Structures"
description: "A heavy obstacle built with any hammer from 22 Build Supplies, with 4,500 HP and 20 cash for destroying an enemy one."
---

# Hedgehog

| Hedgehog | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 22 Build Supplies |
| Build time | 44 hits Small (24.9 s), 22 hits Medium (12.5 s), 15 hits Large (13.2 s). Derived from the hammer swing timing, not timed in play. |
| Health | 4,500 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -80% |
| Grenades | -50% |
| Rockets | +450% |
| C4 | +500% |
| IEDs | +1,000% |
| Internal name | `DA_Buildable_TankTrap` |
{: .wiki-infobox }

The Hedgehog is an obstacle that any hammer can build. It costs 22 Build Supplies and has 4,500 HP. Grenades do half their normal damage to it, but rockets, C4 and IEDs do a lot more.

## Overview

The Hedgehog costs 22 Build Supplies and has 4,500 HP. It has no separate parts.

Destroying an enemy Hedgehog pays 20 cash and 5 Role XP.

## Building it

- **Cost:** 22 Build Supplies, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Small, Medium or Large.
- **Placement:** The Hedgehog is one of the four small structures. It does not need a friendly base radius, but it cannot be placed inside an enemy base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 100.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 3, 5, 6 and 7 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | 44 (about 24.9 s) | 22 (about 12.5 s) | 15 (about 13.2 s) |
| Hits to repair from zero health | 30 | 15 | 10 |
| Hits to dismantle (your own) | 30 | 23 | 18 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The hits assume normal hits, not weak-spot hits. See [Buildables](../building.md#building) for how the hit amounts work.

## What it does

The Hedgehog is an obstacle. The data gives it no effect beyond its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | -50% | 50% |
| Rockets | +450% | 5.5 times |
| C4 | +500% | 6 times |
| IEDs | +1,000% | 11 times |

The table below gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hedgehog | 4,500 | 1,072 | 334 | 8 | 9 | 6 | 3 |

## Season 2 changes

- The Season 2 data lists no change to the Hedgehog's cost or health.
- The T-72B3's 125 mm shell does x0.70 of the damage it did: 6 hits to destroy became 8 (derived). The cannons are unchanged.

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage structures
- [Hesco Walls](hesco-walls.md): the other high-health barriers

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
