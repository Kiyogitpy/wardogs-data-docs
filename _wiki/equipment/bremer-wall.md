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

Destroying an enemy Bremer Wall pays 30 cash and 10 Role XP.

## Building it

- **Cost:** 32 Build Supplies, whichever hammer builds it. In Season 1 it cost 15. Nothing is charged at placement.
- **Hammers:** Large only.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 1.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 15, 20, 15 and 19 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](buildables.md#weak-spots)).
- **Build time:** Not published in seconds.

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | cannot place | 22 (about 19.4 s) |
| Hits to repair from zero health | 44 | 22 | 15 |
| Hits to dismantle (your own) | 44 | 33 | 26 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The Large Hammer is the only one that can place the Bremer Wall. The repair and dismantle hits for the other hammers are what their hits do; the data does not check them for this structure. The build count assumes normal hits.

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

The table below gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bremer Wall | 6,500 | 1,161 | 362 | 11 | 19 | 7 | 5 |

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
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
