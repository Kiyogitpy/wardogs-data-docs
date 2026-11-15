---
redirect_from: ["/wiki/equipment/forward-operating-base/"]
title: "Forward Operating Base"
parent: "Building"
group: "Structures"
description: "The base that players place to anchor building, costing 7,500 cash, with stored build cost 30, placement cost 0 and health 15,000 HP."
---

# Forward Operating Base

| Forward Operating Base | |
|---|---|
| ![Forward Operating Base]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Utility_FOB_Textured_512x512_TEMP.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Category | Base |
| Hammer | None (placed from its own item) |
| **Building** | |
| Build cost | 30 Build Supplies |
| Shop price | 7,500 cash |
| Build time | Instant |
| Stored health | 15,000 HP; S3 initialization unverified |
| **Damage** | |
| Bullets | -80% |
| Melee | -80% |
| Grenades | +200% |
| Rockets | +1,400% |
| C4 | +1,250% |
| IEDs | +5,000% |
| Internal name | [`DA_Buildable_FOB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/Buildables/ForwardOperatingBase/DA_Buildable_FOB.json), item [`ID_ForwardOperatingBase`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables/Content/Data/ForwardOperatingBase/ID_ForwardOperatingBase.json) |
{: .wiki-infobox }

The Forward Operating Base, or FOB, is the anchor for most other structures. Most structures must be placed inside its radius. Its asset stores 15,000 HP, the most of any structure, and it is placed from its own item rather than a hammer. It also holds items and resources for players to use.

## Overview

The FOB costs 7,500 cash in the shop, and its Build Supplies cost is 30. Its item description reads: needed to build larger structures, can hold items and resources for players to use, and provides a radius in which players can build.

Each faction has its own FOB model.

Destroying an enemy FOB pays 2,500 cash and 500 Role XP, plus up to 7,500 more cash that depends on the supplies the FOB holds (the full bonus at 25,000 supplies). Hacking an enemy FOB pays 1,000 cash.

## Building it

- **Cost:** 7,500 cash from the shop. Its Build Supplies cost is 30, and its stored PlacementCost is 0; the S3 charging path has not been verified.
- **Hammer:** None. The FOB is placed from its own item.
- **Placement (historical CL516586 checks):** It could not be placed within 3 m of a safe zone or while standing in one, and not within 1 m of a ladder. The historical check also rejected a new FOB placed within about 42 m of another FOB. The check is a square box rather than a circle: a new FOB is refused when it is under 42 m from an existing one along both horizontal directions of that FOB (so up to about 59 m on a diagonal) and within 42 m in height, and the same test is run with the roles swapped. This is a historical static reading of CL516586 code, not a verified S3 placement boundary.
- **Build time:** Instant. The FOB has no build stages.
- **Repair and dismantle:** Hammer figures for the FOB are: 30 hits (Small), 15 (Medium) or 10 (Large) to repair from zero health, and 100, 75 or 60 hits to dismantle your own. Whether a hammer can work on a FOB is not confirmed, so these are shown for reference only. Dismantling gives no supplies back, as far as is known.
- **Stack limit:** 1.
- **Limits:** Each FOB allows one Refuel Station, one Repair Station and up to four Builder's Radios. See the [Refuel and Repair Stations](refuel-and-repair-stations.md) and [Builder's Radio](builders-radio.md) articles.
- **Interactions:** Players can use the FOB's access interaction. A tap on keyboard or a hold on gamepad lets players use it, and several players can do so at once. Hacking takes a hold of 30 seconds by one player. The hacking result is sent to the server. The rewards for hacking are on the [Rewards page](../../game-features/Wardogs_GameFeatures_Rewards_v2.md).

## What it does

The FOB anchors the building radius. Most structures must be inside a friendly FOB radius to be placed, and the FOB limits the number of Refuel Stations, Repair Stations and Builder's Radios. The FOB also holds supplies for players, and there are sounds for depositing Ammo, Build, Fuel and Mechanical Supplies.

The earlier CL516586 client-data search found no FOB respawn association. That historical negative search does not establish S3 client or server spawning behavior; whether players can spawn at a FOB remains unresolved.

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

The S3 asset retains the name `Buildable.Damage.DoNotTakeDamage`. The earlier CL516586 investigation found no reader in its searched paths; it did not exclude every indirect read and does not establish that the field is unused in S3. The table below assumes the FOB takes damage like any other structure. Its data asset stores 15,000 HP. Applying that value at spawn was traced in CL516586 (round 45 C); the equivalent S3 initialization has not been traced. The table gives the hits it takes to destroy, for each source. For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, .50 cal FMJ 90, 120 mm rocket 150, M67 frag grenade 100 (it counts as a rocket against structures), C4 charge 250, IED 300. Each figure is the number of hits needed after every matching damage entry is applied.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Forward Operating Base | 15,000 | 2,679 | 834 | 5 | 10 | 5 | 1 |

## Season 2 changes

- No Season 2 change to the Forward Operating Base's cost or health is listed.
- The Vanguard CIWS 20 mm cannon went from full damage to x0.80 (250 hits to destroy became 313, derived). The T-72B3's 125 mm shell does x1.35 of the damage it did: 7 hits to destroy became 5 (derived).

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Drill Rig](drill-rig.md): a structure that must be placed inside a base radius
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage structures

## Season 3 update

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) reduce the spotted-FOB kill reward from 250 to 200 XP. This is a spotting reward, distinct from the destruction reward above. Pallets outside a friendly FOB pay less, and lower-value crates pay rewards scaled to their contents. Fuel deposited into a FOB that activates a drill earns a new kickback; no amount is specified.

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
