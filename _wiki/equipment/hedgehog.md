---
title: "Hedgehog"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A tank trap obstacle built with any hammer from 22 Build Supplies, with 4,500 HP and a high cash reward for destroying an enemy one."
---

# Hedgehog

| Hedgehog | |
|---|---|
| **General** | |
| Category | Cover and obstruction |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 22 Build Supplies |
| Build time | Not yet known |
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

The Hedgehog costs 22 Build Supplies and has 4,500 HP. It has no separate parts. The export names it "TankTrap" internally and "Hedgehog" in the game, so this article uses "Hedgehog".

The reward tables give 100 cash for placing a Hedgehog and 250 cash for destroying an enemy one.

## Building it

- **Cost:** 22 Build Supplies.
- **Hammers:** Small, Medium or Large.
- **Placement:** The Hedgehog is one of the four small structures. It does not need a friendly base radius, but it cannot be placed inside an enemy base radius. It also passes a safe zone check and a ladder bounds check, whose tests are not yet known.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 3, 5, 6 and 7 weak spots. What the weak spots do is not yet known.
- **Build time:** Not yet known.

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

The data does not say how many hits a Hedgehog takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Hedgehog | 4,500 | 1072 | 90 | 6 | 3 |

## Season 2 changes

The Season 2 data lists no change to the Hedgehog's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage structures
- [Hesco Walls](hesco-walls.md): the other high-health barriers

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage row, placement conditions and cash rewards
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
