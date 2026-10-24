---
title: "Recon Tower"
parent: "Equipment"
group: "Emplacements and buildables"
description: "A large multi-part tower built only with the Large Hammer from 200 Build Supplies in Season 2, with 5,000 HP and three parts."
---

# Recon Tower

| Recon Tower | |
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
| Internal name | `DA_Buildable_CrowsNest`, with parts `DA_Buildable_CrowsNest_BaseFloor`, `DA_Buildable_CrowsNest_FirstFloor` and `DA_Buildable_CrowsNest_Roof` |
{: .wiki-infobox }

The Recon Tower is a large tower built from a base floor, a first floor and a roof. Only the Large Hammer can build it. It has 5,000 HP and takes the same damage as the [Bunker](bunker.md).

## Overview

The Recon Tower costs 200 Build Supplies and has 5,000 HP. Its three parts each cost 10 Build Supplies and have 2,250 HP. The export gives no display name for the parts, so they are described here as parts of the tower.

The reward tables have no cash entry for placing a Recon Tower. They give 1,400 cash for destroying an enemy one.

## Building it

- **Cost:** 200 Build Supplies for the tower. Each part costs 10 Build Supplies. The data does not say whether the part costs add to the 200.
- **Hammers:** Large only.
- **Placement:** The tower must be inside a friendly Forward Operating Base radius. It also passes a ladder bounds check and a safe zone check, whose tests are not yet known. The parts need a friendly base radius and a ladder bounds check.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 27, 47, 41 and 41 weak spots. What the weak spots do is not yet known.
- **Parts:** The base floor, first floor and roof are placed with the tower. Each has one stage. Each uses the same damage numbers as the tower.
- **Build time:** Not yet known.

## What it does

The data does not describe what a player can do on the tower. Its effect in play is its health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -80% | 20% |
| Melee | -10% | 90% |
| Grenades | -50% | 50% |
| Rockets | +45% | 1.45 times |
| C4 | +50% | 1.5 times |
| IEDs | +200% | 3 times |

The data does not say how many hits the Recon Tower takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Recon Tower | 5,000 | 893 | 100 | 23 | 14 |
| Recon Tower floor or roof | 2,250 | 402 | 45 | 11 | 6 |

## Season 2 changes

- Build cost went from 100 to 200 Build Supplies. The data lists this change for the main tower only.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Bunker](bunker.md) and [Indirect Fire Shelter](indirect-fire-shelter.md): the structures with the same damage numbers

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, parts, stages, damage row, placement conditions and cash rewards
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost change
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
