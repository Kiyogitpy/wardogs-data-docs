---
title: "Gate"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A large closeable gate built with a Medium or Large Hammer from 200 Build Supplies in Season 2, with 5,320 HP and three parts."
---

# Gate

| Gate | |
|---|---|
| **General** | |
| Category | Closeable gate |
| Hammer | Medium, Large |
| **Building** | |
| Build cost | 200 Build Supplies (85 in Season 1) |
| Build time | Not yet known |
| Health | 5,320 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -80% |
| Grenades | +0% |
| Rockets | +850% |
| C4 | +1,000% |
| IEDs | +2,000% |
| Internal name | `DA_Buildable_Gate`, with parts `DA_Buildable_Gate_Left`, `DA_Buildable_Gate_Right` and `DA_Buildable_Gate_Ramp` |
{: .wiki-infobox }

The Gate is a closeable barrier made of two halves and a ramp. A Medium or Large Hammer can build it. Rockets, C4 and IEDs all do many times their normal damage to it.

## Overview

The Gate costs 200 Build Supplies and has 5,320 HP. Its parts are the left half, the right half and the ramp. Each half costs 85 Build Supplies and has 5,320 HP. The ramp costs 85 Build Supplies and has 6,500 HP.

The reward tables give 300 cash for placing a Gate and 500 cash for destroying an enemy one.

## Building it

- **Cost:** 200 Build Supplies for the Gate. The data does not say whether the part costs add to the 200.
- **Hammers:** Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known. The Gate's parts can sit on surfaces with a maximum angle of 10. The data does not state the unit, which is most likely degrees.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 21, 19, 39 and 40 weak spots. What the weak spots do is not yet known.
- **Parts:** The left half, right half and ramp are placed with the Gate. Each has one stage. Each uses the same damage numbers as the Gate.
- **Build time:** Not yet known.

## What it does

The Gate can be closed, and the data gives it a breach effect when it is destroyed. The data does not say what the breach does in play beyond that. The rest of its effect is health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +850% | 9.5 times |
| C4 | +1,000% | 11 times |
| IEDs | +2,000% | 21 times |

Rockets, C4 and IEDs multiply the Gate's damage far more than they do to most walls. The data does not say how many hits the Gate takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Gate, or each half | 5,320 | 1267 | 54 | 4 | 2 |
| Gate ramp | 6,500 | 1548 | 65 | 5 | 3 |

## Season 2 changes

- Build cost went from 85 to 200 Build Supplies. The data lists this change for the main Gate only.

## See also

- [Door](door.md): the smaller closeable structure
- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, parts, stages, damage row, placement conditions and cash rewards
- [Rewards](../../game-features/Wardogs_GameFeatures_Rewards_v2.md): the cash for closing a friendly base gate
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost change
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
