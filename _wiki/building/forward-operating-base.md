---
redirect_from: ["/wiki/equipment/forward-operating-base/"]
title: "Forward Operating Base"
parent: "Building"
group: "Structures"
description: "The base that players place to anchor building, costing 7,500 cash and 30 Build Supplies to place, with 15,000 HP."
---

# Forward Operating Base

| Forward Operating Base | |
|---|---|
| **General** | |
| Category | Base |
| Hammer | None (placed from its own item) |
| **Building** | |
| Build cost | 30 Build Supplies |
| Shop price | 7,500 cash |
| Build time | Instant |
| Health | 15,000 HP |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +200% |
| Rockets | +1,400% |
| C4 | +1,250% |
| IEDs | +5,000% |
| Internal name | `DA_Buildable_FOB`, item `ID_ForwardOperatingBase` |
{: .wiki-infobox }

The Forward Operating Base, or FOB, is the anchor for most other structures. Most structures must be placed inside its radius. It has 15,000 HP, the most of any structure in the data, and it is placed from its own item rather than a hammer. It also holds items and resources for players to use.

## Overview

The FOB costs 7,500 cash in the shop, and its Build Supplies cost is 30. Its item description reads: needed to build larger structures, can hold items and resources for players to use, and provides a radius in which players can build.

Each faction has its own FOB model in the data.

Destroying an enemy FOB pays 2,500 cash and 500 Role XP, plus up to 7,500 more cash that depends on the supplies the FOB holds (the full bonus at 25,000 supplies). Hacking an enemy FOB pays 1,000 cash.

## Building it

- **Cost:** 7,500 cash from the shop. Its Build Supplies cost is 30, and nothing is charged at placement.
- **Hammer:** None. The FOB is placed from its own item.
- **Placement:** It cannot be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder. A new FOB also cannot be placed within about 42 m of another FOB. The exact shape of that check is not decoded.
- **Build time:** Instant. The FOB has no build stages.
- **Repair and dismantle:** The data gives hammer figures for the FOB: 30 hits (Small), 15 (Medium) or 10 (Large) to repair from zero health, and 100, 75 or 60 hits to dismantle your own. Whether a hammer can work on a FOB is not confirmed, so these are shown for reference only. Dismantling gives no supplies back, as far as the data shows.
- **Stack limit:** 1.
- **Limits:** Each FOB allows one Refuel Station, one Repair Station and up to four Builder's Radios. See the [Refuel and Repair Stations](refuel-and-repair-stations.md) and [Builder's Radio](builders-radio.md) articles.
- **Interactions:** Players can use the FOB's access interaction. A tap on keyboard or a hold on gamepad lets players use it, and several players can do so at once. Hacking takes a hold of 30 seconds by one player. The data says the hacking result is sent to the server. The rewards for hacking are on the [Rewards page](../../game-features/Wardogs_GameFeatures_Rewards_v2.md).

## What it does

The FOB anchors the building radius. Most structures must be inside a friendly FOB radius to be placed, and the FOB limits the number of Refuel Stations, Repair Stations and Builder's Radios. The FOB also holds supplies for players, and the data lists sounds for depositing Ammo, Build, Fuel and Mechanical Supplies.

The client game files hold no spawn data tied to the FOB, so nothing in them shows that it is a spawn point. The server side is not excluded by the data, so whether players can spawn at a FOB is not known.

## Durability

The FOB has the most exposure to explosives of any structure. Its IED entry multiplies IED damage by 51, and its rocket entry multiplies rocket damage by 15.

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -80% | 20% |
| Melee | -80% | 20% |
| Grenades | +200% | 3 times |
| Rockets | +1,400% | 15 times |
| C4 | +1,250% | 13.5 times |
| IEDs | +5,000% | 51 times |

The FOB's data has a flag named "do not take damage". No code in the game files reads it, so it appears to be unused data. The table below assumes the FOB takes damage like any other structure. Its health is 15,000, the value in its data asset, which is applied when the FOB is spawned. The table gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Forward Operating Base | 15,000 | 2,679 | 834 | 5 | 10 | 5 | 1 |

## Season 2 changes

- The Season 2 data lists no change to the Forward Operating Base's cost or health.
- The Vanguard CIWS 20 mm cannon went from full damage to x0.80 (250 hits to destroy became 313, derived). The T-72B3's 125 mm shell does x1.35 of the damage it did: 7 hits to destroy became 5 (derived).

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Drill Rig](drill-rig.md): a structure that must be placed inside a base radius
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, damage row, placement conditions, limits and the vendor and reward tables
- [Item actions](../../content/Wardogs_ItemActions_v1.md): the FOB placement action, which is separate from the hammer actions
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md): the names of the FOB supply containers
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
- [Round 44 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round44-econ-buildables.md)
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
