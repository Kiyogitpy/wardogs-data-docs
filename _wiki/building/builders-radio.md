---
redirect_from: ["/wiki/equipment/builders-radio/"]
title: "Builder's Radio"
parent: "Building"
group: "Structures"
description: "A music radio built with any hammer from 20 Build Supplies, with 1,000 HP. Up to 4 can be placed in each base, and it has seven stations."
---

# Builder's Radio

| Builder's Radio | |
|---|---|
| ![Builder's Radio]({{ '/assets/img/icons/buildables/T_UI_Buidable_Radio.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Category | Music radio |
| Hammer | Small, Medium, Large |
| **Building** | |
| Build cost | 20 Build Supplies |
| Build time | 40 hits Small (22.7 s), 20 hits Medium (11.3 s), 14 hits Large (12.4 s). Derived from the hammer swing timing, not timed in play. |
| Health | 1,000 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | +70% |
| Grenades | +500% |
| Rockets | +1,000% |
| C4 | +400% |
| IEDs | +800% |
| Internal name | [`DA_Buildable_Radio`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/Radio/DA_Buildable_Radio.json) |
{: .wiki-infobox }

The Builder's Radio is a music radio that any hammer can build. It has a power switch and seven stations. It counts toward the limit of four radios per Forward Operating Base.

## Overview

The Builder's Radio costs 20 Build Supplies and has 1,000 HP. It has no separate parts. It carries the Support role experience tag.

Destroying an enemy Builder's Radio pays 20 cash and 10 Role XP.

## Building it

- **Cost:** 20 Build Supplies, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Small, Medium or Large.
- **Limit:** Up to 4 Builder's Radios per Forward Operating Base. Each radio counts toward the base's limit.
- **Placement:** It must be inside a friendly Forward Operating Base radius. It cannot be placed within 1 m of a ladder, nor within 3 m of a safe zone or while standing in one.
- **Stack limit:** 6.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 8, 9, 9 and 9 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | 40 (about 22.7 s) | 20 (about 11.3 s) | 14 (about 12.4 s) |
| Hits to repair from zero health | 31 | 16 | 11 |
| Hits to dismantle (your own) | 7 | 5 | 4 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

The hits assume normal hits, not weak-spot hits. See [Buildables](../building.md#building) for how the hit amounts work.

## What it does

The Builder's Radio plays music. Its power switch turns the radio on and off, and each of the seven station buttons picks a station. Changing the station changes the music that plays. It has no other effect beyond its health and how it takes damage.

Its registration with the base only affects the limit of four radios per base. Nothing else is tied to it, such as supply drops or spawns.

## Durability

The radio is weak to explosives. Rockets do 11 times their normal damage, and grenades do 6 times.

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | +70% | 1.7 times |
| Grenades | +500% | 6 times |
| Rockets | +1,000% | 11 times |
| C4 | +400% | 5 times |
| IEDs | +800% | 9 times |

The table below gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Builder's Radio | 1,000 | 239 | 75 | 1 | 1 | 1 | 1 |

## Season 2 changes

- No Season 2 change to the Builder's Radio's cost or health is listed.
- The Gepard's 35 mm cannon went from x0.25 to x0.20 of its damage (67 hits to destroy became 84, derived). The T-72B3's 125 mm shell and the 20 mm cannon are unchanged.

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Refuel and Repair Stations](refuel-and-repair-stations.md): the other structures with a per-base limit
- [Forward Operating Base](forward-operating-base.md): the base that limits the radio

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage table, placement limits and the support role tag
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): how the percentage changes are applied (section 6)
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the buildable changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): the radio, placement checks and the FOB limit
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source (stacked damage entries, IED and the M67 as a rocket) and the build time estimates.
