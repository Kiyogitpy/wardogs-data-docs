---
title: "Recon Tent"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A small camouflage tent built with any hammer from 7 Build Supplies, with 300 HP."
---

# Recon Tent

| Recon Tent | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 7 Build Supplies |
| Build time | Not yet known |
| Health | 300 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -28% |
| Grenades | +0% |
| Rockets | +200% |
| C4 | +150% |
| IEDs | +500% |
| Internal name | `DA_Buildable_CamoNetTent` |
{: .wiki-infobox }

The Recon Tent is a small tent that any hammer can build. It costs 7 Build Supplies and has 300 HP. Its damage numbers are close to those of [Barbed Wire](barbed-wire.md), except that it has more health and takes more IED damage.

## Overview

The Recon Tent costs 7 Build Supplies and has 300 HP. It has no separate parts.

The reward tables give 75 cash for destroying an enemy Recon Tent. They give no cash for placing one.

## Building it

- **Cost:** 7 Build Supplies.
- **Hammers:** Small, Medium or Large.
- **Placement:** The Recon Tent is one of the four small structures. It does not need a friendly base radius, but it cannot be placed inside an enemy base radius. It also passes a safe zone check and a ladder bounds check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The data gives 5, 0, 6 and 29 weak spots for the first four stages. The second stage has none. What the weak spots do is not yet known.
- **Build time:** Not yet known.

## What it does

The Recon Tent is cover. The data gives it no effect beyond its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -28% | 72% |
| Grenades | +0% | 100% |
| Rockets | +200% | 3 times |
| C4 | +150% | 2.5 times |
| IEDs | +500% | 6 times |

The data does not say how many hits a Recon Tent takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Recon Tent | 300 | 72 | 3 | 1 | 1 |

## Season 2 changes

The Season 2 data lists no change to the Recon Tent's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Barbed Wire](barbed-wire.md): the other small wire and cover structure

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
