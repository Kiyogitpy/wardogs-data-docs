---
title: "Builder's Radio"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A music radio built with any hammer from 20 Build Supplies, with 1,000 HP. Up to 4 can be placed in each base, and it has seven stations."
---

# Builder's Radio

| Builder's Radio | |
|---|---|
| **General** | |
| Category | Music radio |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 20 Build Supplies |
| Build time | Not yet known |
| Health | 1,000 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | +70% |
| Grenades | +500% |
| Rockets | +1,000% |
| C4 | +400% |
| IEDs | +800% |
| Internal name | `DA_Buildable_Radio` |
{: .wiki-infobox }

The Builder's Radio is a music radio that any hammer can build. It has a power switch and seven stations. It counts toward the limit of four radios per Forward Operating Base.

## Overview

The Builder's Radio costs 20 Build Supplies and has 1,000 HP. It has no separate parts. Its entry in the data carries the Support role experience tag.

The reward tables have no cash entry for the Builder's Radio. They do have a one-cash default row, which may or may not apply to structures that are not listed; the data does not confirm it.

## Building it

- **Cost:** 20 Build Supplies, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Small, Medium or Large.
- **Limit:** Up to 4 Builder's Radios per Forward Operating Base. Each radio counts toward the base's limit.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 1 m of a ladder, nor within 3 m of a safe zone or while standing in one.
- **Stack limit:** 6.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 8, 9, 9 and 9 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](buildables.md#weak-spots)).
- **Build time:** Not published in seconds.

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | 40 | 20 | 14 |
| Hits to repair from zero health | 31 | 16 | 11 |
| Hits to dismantle (your own) | 7 | 5 | 4 |

The hits assume normal hits, not weak-spot hits. See [Buildables](buildables.md#building) for how the hit amounts work.

## What it does

The Builder's Radio plays music. Its power switch turns the radio on and off, and each of the seven station buttons picks a station. Changing the station changes the music that plays. The data gives it no other effect beyond its health and how it takes damage.

Its registration with the base only affects the limit of four radios per base. The data shows nothing else tied to it, such as supply drops or spawns.

## Durability

The radio is weak to explosives. Rockets do 11 times their normal damage, and grenades do 6 times.

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | +70% | 1.7 times |
| Grenades | +500% | 6 times |
| Rockets | +1,000% | 11 times |
| C4 | +400% | 5 times |
| IEDs | +800% | 9 times |

The data does not say how many hits a Builder's Radio takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Builder's Radio | 1,000 | 239 | 2 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to the Builder's Radio's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Refuel and Repair Stations](refuel-and-repair-stations.md): the other structures with a per-base limit
- [Forward Operating Base](forward-operating-base.md): the base that limits the radio

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement limits and the support role tag
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): the radio, placement checks and the FOB limit
