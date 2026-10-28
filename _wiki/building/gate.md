---
redirect_from: ["/wiki/equipment/gate/"]
title: "Gate"
parent: "Building"
group: "Structures"
description: "A large closeable gate built with a Medium or Large Hammer from 200 Build Supplies in Season 2, with 5,320 HP and three parts."
---

# Gate

| Gate | |
|---|---|
| ![Gate]({{ '/assets/img/icons/other-buildables-hblock-gate-6x2/t_ui_icon_hesco_gate.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Category | Closeable gate |
| Hammer | Medium, Large |
| **Building** | |
| Build cost | 200 Build Supplies (85 in Season 1) |
| Build time | 200 hits Medium (113.4 s), 134 hits Large (118.3 s). Derived from the hammer swing timing, not timed in play. |
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

Destroying an enemy Gate pays 200 cash and 50 Role XP. Its ramp pays 85 cash and 20 Role XP.

## Building it

- **Cost:** 200 Build Supplies for the Gate, whichever hammer builds it. The parts (85 Build Supplies each) are not added on top of the 200: three parts would come to 255, and the game charges only the 200 for the whole Gate. A part's own price most likely applies only when that part is repaired by itself (inferred). Nothing is charged at placement.
- **Hammers:** Medium or Large.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder. The Gate's parts can sit on surfaces with a maximum angle of 10. The unit is not stated, and is most likely degrees.
- **Stack limit:** 1.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 21, 19, 39 and 40 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Parts:** When the Gate is finished, it turns into separate parts: the left half, the right half and the ramp. Each is its own buildable with its own health: each half has 5,320 HP and the ramp has 6,500 HP. This is Derived from the stage data (see [Buildables](../building.md#building)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | 200 (about 113.4 s) | 134 (about 118.3 s) |
| Hits to repair from zero health | 71 | 36 | 24 |
| Hits to dismantle (your own) | 36 | 27 | 22 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The parts are not built on their own; they come with the finished Gate. Once separated, each half has 85 Build Supplies of cost and takes 10 repair hits from zero and 22 dismantle hits with the Large Hammer. The ramp, also 85 Build Supplies, takes 10 repair hits and 26 dismantle hits with the Large Hammer (Derived). The build count assumes normal hits, and hitting weak spots brings it down.

## What it does

The Gate can be closed, and it has a breach effect when it is destroyed. The breach is a visual particle effect that plays at the gate halves when they are destroyed; it has no damage, blast or other number attached. The rest of its effect is health and how it takes damage.

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +850% | 9.5 times |
| C4 | +1,000% | 11 times |
| IEDs | +2,000% | 21 times |

Rockets, C4 and IEDs multiply the Gate's damage far more than they do to most walls. The table below gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gate, or each half | 5,320 | 1,267 | 395 | 5 | 6 | 2 | 1 |
| Gate ramp | 6,500 | 1,548 | 482 | 6 | 7 | 3 | 2 |

## Season 2 changes

- Build cost went from 85 to 200 Build Supplies. This change applies to the main Gate only.
- The Gepard's 35 mm cannon went from x0.60 to x0.50 of its damage, and the Vanguard CIWS 20 mm cannon from full damage to x0.50. Hits to destroy the Gate at point blank (derived): 148 to 178 for the 35 mm cannon, 89 to 178 for the 20 mm cannon.
- The T-72B3's 125 mm shell does x0.80 of the damage it did: 4 hits to destroy became 5 (derived).

## See also

- [Door](door.md): the smaller closeable structure
- [Building](../building.md): costs, hammers and placement for every structure
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, parts, stages, damage row, placement conditions and cash rewards
- [Rewards](../../game-features/Wardogs_GameFeatures_Rewards_v2.md): the cash for closing a friendly base gate
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the build cost change
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
