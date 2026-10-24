---
title: "Bunker"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A large multi-part structure built only with the Large Hammer from 200 Build Supplies in Season 2, with 5,000 HP and a floor and roof."
---

# Bunker

| Bunker | |
|---|---|
| **General** | |
| Category | Multi-part structure |
| Hammer | Large |
| **Building** | |
| Build cost | 200 Build Supplies (100 in Season 1) |
| Build time | Not yet known |
| Health | 5,000 HP |
| **Damage** | |
| Bullets | -80% |
| Melee | -10% |
| Grenades | -50% |
| Rockets | +45% |
| C4 | +50% |
| IEDs | +200% |
| Internal name | `DA_Buildable_Bunker`, with parts `DA_Buildable_Bunker_Floor` and `DA_Buildable_Bunker_Roof` |
{: .wiki-infobox }

The Bunker is a large structure that only the Large Hammer can build. It has 5,000 HP and two parts, a floor and a roof. It takes less grenade damage than most structures, and rockets, C4 and IEDs still do more damage to it than normal.

## Overview

The Bunker costs 200 Build Supplies and has 5,000 HP. Its parts are the floor and the roof. Each part costs 10 Build Supplies and has 2,250 HP.

The Bunker, the [Recon Tower](recon-tower.md) and the [Indirect Fire Shelter](indirect-fire-shelter.md) are the three large multi-part structures. They share the same damage numbers.

The reward tables give 500 cash for placing a Bunker and 1,400 cash for destroying an enemy one.

## Building it

- **Cost:** 200 Build Supplies for the Bunker. Each part costs 10 Build Supplies. The data does not say whether the part costs add to the 200.
- **Hammers:** Large only.
- **Placement:** The Bunker must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known. The floor and roof parts need a friendly base radius and a ladder bounds check.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 29, 39, 60 and 99 weak spots. What the weak spots do is not yet known.
- **Parts:** The floor and roof are placed with the Bunker. Each has one stage, so it appears complete when placed. Each uses the same damage numbers as the Bunker.
- **Build time:** Not yet known.

## What it does

The Bunker is a shelter with a floor and a roof. The data does not describe what a player can do inside it. Its effect in play is its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -80% | 20% |
| Melee | -10% | 90% |
| Grenades | -50% | 50% |
| Rockets | +45% | 1.45 times |
| C4 | +50% | 1.5 times |
| IEDs | +200% | 3 times |

The data does not say how many hits the Bunker takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Bunker | 5,000 | 893 | 100 | 23 | 14 |
| Bunker floor or roof | 2,250 | 402 | 45 | 11 | 6 |

## Season 2 changes

- Build cost went from 100 to 200 Build Supplies. The data lists this change for the main Bunker only.
- The roof's build-stage mesh bounds changed. The data does not say what that means in play.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Recon Tower](recon-tower.md) and [Indirect Fire Shelter](indirect-fire-shelter.md): the structures with the same damage numbers
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, parts, stages, damage row, placement conditions and cash rewards
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost and mesh changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
