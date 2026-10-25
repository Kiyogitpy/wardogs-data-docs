---
redirect_from: ["/wiki/equipment/indirect-fire-shelter/"]
title: "Indirect Fire Shelter"
parent: "Building"
group: "Structures"
description: "A large multi-part shelter built only with the Large Hammer from 200 Build Supplies in Season 2, with 5,000 HP and a floor and ceiling."
---

# Indirect Fire Shelter

| Indirect Fire Shelter | |
|---|---|
| **General** | |
| Category | Multi-part structure |
| Hammer | Large |
| **Building** | |
| Build cost | 200 Build Supplies (100 in Season 1) |
| Build time | 134 hits Large (about 118.3 s). Derived from the hammer swing timing, not timed in play. |
| Health | 5,000 HP |
| **Damage** | |
| Bullets | -80% |
| Melee | -10% |
| Grenades | -50% |
| Rockets | +45% |
| C4 | +50% |
| IEDs | +200% |
| Internal name | `DA_Buildable_AirRaidShelter`, with parts `DA_Buildable_AirRaidShelter_Floor` and `DA_Buildable_AirRaidShelter_Ceiling` |
{: .wiki-infobox }

The Indirect Fire Shelter is a large shelter with a floor and a ceiling. Only the Large Hammer can build it. It has 5,000 HP and takes the same damage as the [Bunker](bunker.md). It is a different structure from the [Shelter](shelter.md).

## Overview

The Indirect Fire Shelter costs 200 Build Supplies and has 5,000 HP. Its two parts, the floor and the ceiling, each cost 10 Build Supplies and have 2,250 HP.

Destroying an enemy Indirect Fire Shelter pays 200 cash and 50 Role XP.

## Building it

- **Cost:** 200 Build Supplies for the shelter, whichever hammer builds it. Each part costs 10 Build Supplies. The data does not say whether the part costs add to the 200. Nothing is charged at placement.
- **Hammers:** Large only.
- **Placement:** The shelter must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 1.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 26, 40, 72 and 86 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Parts:** When the shelter is finished, it turns into separate parts: a floor, a ceiling, and Hesco Blocks around them. Each part is its own buildable with its own health. The floor and ceiling each have 2,250 HP. This is Derived from the stage data (see [Buildables](../building.md#building)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | cannot place | 134 (about 118.3 s) |
| Hits to repair from zero health | 60 | 30 | 20 |
| Hits to dismantle (your own) | 34 | 25 | 20 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The Large Hammer is the only one that can place the shelter. The repair and dismantle hits for the other hammers are what their hits do; the data does not check them for this structure. The build count assumes normal hits, and hitting weak spots brings it down.

## What it does

The shelter is a large structure with a floor and a ceiling. The data does not describe what a player can do inside it. Its effect in play is its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -80% | 20% |
| Melee | -10% | 90% |
| Grenades | -50% | 50% |
| Rockets | +45% | 1.45 times |
| C4 | +50% | 1.5 times |
| IEDs | +200% | 3 times |

The table below gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Indirect Fire Shelter | 5,000 | 893 | 278 | 33 | 35 | 27 | 12 |
| Floor or ceiling | 2,250 | 402 | 125 | 15 | 16 | 12 | 5 |

## Season 2 changes

- Build cost went from 100 to 200 Build Supplies. The data lists this change for the main shelter only.
- The build-stage mesh bounds of the ceiling changed. The data does not say what that means in play.

## See also

- [Shelter](shelter.md): a different, medium-cost shelter
- [Bunker](bunker.md) and [Recon Tower](recon-tower.md): the structures with the same damage numbers
- [Buildables](../building.md): costs, hammers and placement for every structure

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, parts, stages, damage row, placement conditions and cash rewards
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost and mesh changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
