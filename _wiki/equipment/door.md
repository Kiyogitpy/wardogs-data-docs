---
title: "Door"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A closeable door built with a Medium or Large Hammer from 80 Build Supplies in Season 2, with 2,200 HP and two parts."
---

# Door

| Door | |
|---|---|
| **General** | |
| Category | Closeable door |
| Hammer | Medium, Large |
| **Building** | |
| Build cost | 80 Build Supplies (22 in Season 1) |
| Build time | Not yet known |
| Health | 2,200 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -80% |
| Grenades | +0% |
| Rockets | +650% |
| C4 | +200% |
| IEDs | +800% |
| Internal name | `DA_Buildable_Door`, with parts `DA_Buildable_Door_DoorOnly` and `DA_Buildable_Door_TopSegment` |
{: .wiki-infobox }

The Door is a closeable barrier that a Medium or Large Hammer can build. It has 2,200 HP. It is built with two extra parts, a door section and a top section, and it has a breach effect when it is destroyed.

## Overview

The Door costs 80 Build Supplies and has 2,200 HP. It is made of a door section and a top section, each costing 22 Build Supplies and having 500 HP.

The reward tables give 100 cash for destroying an enemy Door. They give no cash for building or placing one. Closing a friendly Forward Operating Base door pays cash too. The [Rewards page](../../game-features/Wardogs_GameFeatures_Rewards_v2.md) has the amount.

## Building it

- **Cost:** 80 Build Supplies for the Door, whichever hammer builds it. Each part costs 22 Build Supplies. The data does not say whether the part costs add to the 80. Nothing is charged at placement.
- **Hammers:** Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder.
- **Stack limit:** 2.
- **Build stages:** Five, at 0, 30, 60, 80 and 100% of progress. The earlier stages have 12, 11, 15 and 11 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](buildables.md#weak-spots)).
- **Parts:** When the Door is finished, it turns into separate parts: a door section that closes, and a top section. Each is its own buildable with 500 HP and uses the same damage numbers as the Door. This is Derived from the stage data (see [Buildables](buildables.md#building)).
- **Build time:** Not published in seconds.

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | 80 | 54 |
| Hits to repair from zero health | 80 | 40 | 27 |
| Hits to dismantle (your own) | 15 | 11 | 9 |

Each part on its own takes 15 repair hits from zero with the Medium Hammer or 10 with the Large Hammer, and 3 dismantle hits with the Medium Hammer or 2 with the Large Hammer (Derived). The build count assumes normal hits, and hitting weak spots brings it down.

## What it does

The Door can be closed, and the data gives it a breach effect when it is destroyed. The data does not say what the breach looks like or does in play beyond that. The rest of its effect is health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +650% | 7.5 times |
| C4 | +200% | 3 times |
| IEDs | +800% | 9 times |

The damage numbers for the Door also apply to its door section and top section. The data does not say how many hits the Door takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Door | 2,200 | 524 | 22 | 2 | 3 |
| Door-only or top section | 500 | 120 | 5 | 1 | 1 |

## Season 2 changes

- Build cost went from 22 to 80 Build Supplies. The data lists this change for the main Door only, not for its parts.

## See also

- [Gate](gate.md): the larger closeable structure
- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, parts, stages, damage row, placement conditions and cash rewards
- [Rewards](../../game-features/Wardogs_GameFeatures_Rewards_v2.md): the cash for closing a friendly base door
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost change
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
