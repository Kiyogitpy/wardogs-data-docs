---
title: "Builder's Radio"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A support structure built with any hammer from 20 Build Supplies, with 1,000 HP, of which up to 4 can be placed in each base."
---

# Builder's Radio

| Builder's Radio | |
|---|---|
| **General** | |
| Category | Support structure |
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

The Builder's Radio is a support structure that any hammer can build. It registers with the Forward Operating Base and can be placed up to 4 times per base. Its exact function in play is not yet known.

## Overview

The Builder's Radio costs 20 Build Supplies and has 1,000 HP. It has no separate parts. Its entry in the data carries the Support role experience tag. The data does not say what the radio does for players.

The reward tables have no cash entry for the Builder's Radio.

## Building it

- **Cost:** 20 Build Supplies.
- **Hammers:** Small, Medium or Large.
- **Limit:** Up to 4 Builder's Radios per Forward Operating Base.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 8, 9, 9 and 9 weak spots. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

The data says the radio registers with the base, but what that does is not yet known. The data gives no effect for the radio beyond its health and how it takes damage.

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
