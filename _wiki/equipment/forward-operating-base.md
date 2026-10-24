---
title: "Forward Operating Base"
parent: "Equipment"
group: "Emplacements and buildables"
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

The reward tables give 1,000 cash for placing a FOB and 5,000 cash for destroying an enemy one.

## Building it

- **Cost:** 7,500 cash from the shop. Its Build Supplies cost is 30. The data does not yet show when those supplies are taken.
- **Hammer:** None. The FOB is placed from its own item.
- **Placement:** It must pass the FOB placement check, a safe zone check and a ladder bounds check. The FOB's own placement rules beyond these checks are not yet known.
- **Build time:** Instant. The FOB has no build stages.
- **Limits:** Each FOB allows one Refuel Station, one Repair Station and up to four Builder's Radios. See the [Refuel and Repair Stations](refuel-and-repair-stations.md) and [Builder's Radio](builders-radio.md) articles.
- **Interactions:** Players can use the FOB's access interaction. A tap on keyboard or a hold on gamepad lets players use it, and several players can do so at once. Hacking takes a hold of 30 seconds by one player. The data says the hacking result is sent to the server. The rewards for hacking are on the [Rewards page](../../game-features/Wardogs_GameFeatures_Rewards_v2.md).

## What it does

The FOB anchors the building radius. Most structures must be inside a friendly FOB radius to be placed, and the FOB limits the number of Refuel Stations, Repair Stations and Builder's Radios. The FOB also holds supplies for players, and the data lists sounds for depositing Ammo, Build, Fuel and Mechanical Supplies.

The data does not say whether the FOB acts as a spawn point. If it does, that comes from another feature, and that feature is not yet known from this data.

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

The data sets a field called "do not take damage" on the FOB. How that field works with the damage numbers above and its 15,000 HP is not yet known. The data does not say how many hits the FOB takes to destroy, so that number is not yet known. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Season 2 changes

The Season 2 data lists no change to the Forward Operating Base's cost or health.

## See also

- [Buildables](buildables.md): costs, hammers and placement for every structure
- [Drill Rig](drill-rig.md): a structure that must be placed inside a base radius
- [Grenades and Explosives](grenades-and-explosives.md): the explosives that damage structures

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, damage row, placement conditions, limits and the vendor and reward tables
- [Item actions](../../content/Wardogs_ItemActions_v1.md): the FOB placement action, which is separate from the hammer actions
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md): the names of the FOB supply containers
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
