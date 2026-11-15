---
redirect_from: ["/wiki/equipment/drill-rig/"]
title: "Drill Rig"
parent: "Building"
group: "Structures"
description: "A fuel-powered rig built with the Large Hammer from 2,750 Build Supplies in Season 2, with 2,500 HP, that runs on Fuel Supplies and pulls the hot zone toward it while it runs."
---

# Drill Rig

| Drill Rig | |
|---|---|
| ![Drill Rig]({{ '/assets/img/icons/other-shared-textures/T_UI_WorkInProgress.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Category | Fuel-powered rig |
| Hammer | Large |
| **Building** | |
| Build cost | 2,750 Build Supplies (2,250 in Season 1) |
| Build time | 917 hits Large (about 809.7 s). Derived from the hammer swing timing, not timed in play. |
| Health | 2,500 HP |
| **Damage** | |
| Bullets | -85% |
| Melee | -80% |
| Grenades | +0% |
| Rockets | +850% |
| C4 | +500% |
| IEDs | +1,500% |
| Internal name | [`DA_Buildable_HotzoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/Buildables_HotZoneMagnet/Content/Data/DA_Buildable_HotzoneMagnet.json) |
{: .wiki-infobox }

The Drill Rig is the most expensive structure that a player can build with a hammer. It only works inside a placement zone within a control zone, and it runs on Fuel Supplies. Once started, it runs for a set time that depends on the fuel added to it, and while it runs it pulls the hot zone toward it.

## Overview

The Drill Rig costs 2,750 Build Supplies and has 2,500 HP. It has no separate parts.

Destroying an enemy Drill Rig pays 2,750 cash and 700 Role XP. It pays the same reward as the Hot Zone Magnet, because the Drill Rig is the buildable form of the magnet.

## Building it

- **Cost:** 2,750 Build Supplies. The zero placement charge in the earlier model is a native-default assumption: the S3 export omits the placement-cost field.
- **Hammers:** Large only.
- **Placement:** It must be inside a friendly Forward Operating Base radius, inside a placement zone, and that zone must be inside a control zone. Unlike most structures, it has no ladder check and no safe zone check.
- **Stack limit setting:** 0. The earlier placement interpretation forbids stacking the rig or building on top of it; the current native placement checks have not been verified.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 70, 79, 98 and 95 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | cannot place | 917 (about 809.7 s) |
| Hits to repair from zero health | 19 | 10 | 7 |
| Hits to dismantle (your own) | 17 | 13 | 10 |

The hit counts apply the CL516586 building formula with build-cost scale 1 and normal hits. Seconds additionally assume one hit per swing: 0.567 s for Small and Medium and 0.883 s for Large, derived from the use animation. The S3 native building consumer and live cost scale have not been verified.

The Drill Rig is Large only, so the Small and Medium columns for building say "cannot place". The repair and dismantle hits are what each hammer's hit does; they are not checked for this structure. The build count assumes normal hits. The rig's build factor is 2, so each Large Hammer hit counts double: 3 build amount instead of 1.5. Hitting its weak spots brings the count down.

## What it does

The Drill Rig is the buildable version of the map's hot zone magnet. It needs Fuel Supplies from the Forward Operating Base to run, and it holds up to 10,000 fuel.

After it is placed, the rig waits 15 s before it can start. Starting it is a hold of 10 s within 2 m. It needs at least 2,000 fuel to run. Each fuel unit buys 0.03 s of run time, so the run time is 60 s with the minimum fuel and 300 s with a full tank. The rig then recharges for 900 s before it can run again. The seconds are **derived** from the numbers and timers.

| Setting | Value |
|---|---:|
| Delay after placing | 15 s (Derived) |
| Hold to start | 10 s, within 2 m (Derived) |
| Minimum fuel to run | 2,000 (60 s of run time, Derived) |
| Maximum fuel | 10,000 (300 s of run time, Derived) |
| Run time per fuel unit | 0.03 s (Derived) |
| Recharge after a run | 900 s (Derived) |

The earlier CL516586 activation path pulled the hot zone toward the rig using its own inherited defaults: half the cached width and length, with unchanged height. That is 25% of the original planar area. The separate world magnet default of 0.6 width and length was not the pair selected by that rig path. These size and speed defaults are not explicitly stored in the S3 rig export; their current native initialization and activation consumer have not been verified.

**Movement in CL516586.** The earlier native path used a speed parameter of 5 m/s to calculate travel time: centre distance in metres divided by speed. That travel time was added to the fuel-derived active duration. An optional curve could shape the interpolation, so this is not a claim of constant instantaneous velocity. Derived historical example: 300 m gives a 60 s travel duration at that default. The cooked rig binding and native code supporting this finding belong to CL516586, not the S3 hotfix; see [Round 93 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round93-rig-lifetime.md#1-g2--the-rig-has-a-separate-activation-caller).

## Durability

| Source | Change | Share of damage that gets through |
|---|---:|---:|
| Bullets | -85% | 15% |
| Melee | -80% | 20% |
| Grenades | +0% | 100% |
| Rockets | +850% | 9.5 times |
| C4 | +500% | 6 times |
| IEDs | +1,500% | 16 times |

For how the percentages combine, see the [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md#6-arithmetic).

## Hits to destroy (point blank, derived)

The counts below use the Drill Rig's S3 stored damage table under the earlier native arithmetic: point-blank full damage, every matching source rule applied, no falloff or repair. They assume the rig's stored damage rules are active; current activation and native compatibility have not been verified. The other structures' counts are in the [Buildables](../building.md#hits-to-destroy-point-blank-derived) article.

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Drill Rig | 2,500 | 596 | 186 | 3 | 3 | 2 | 1 |

## Season 2 changes

- Build cost went from 2,250 to 2,750 Build Supplies.
- Minimum fuel to run went from 1,500 to 2,000.
- Maximum fuel went from 7,500 to 10,000.
- Run time per fuel unit went from 0.05 to 0.03.
- The Vanguard CIWS 20 mm cannon went from full damage to x0.135, and the T-72B3's 125 mm shell does x0.80 of the damage it did.
- The recharge duration of 900 is not listed as changed.

## See also

- [Building](../building.md): costs, hammers and placement for every structure
- [Utility Items](../equipment/utility-items.md): the Fuel Supplies that the rig runs on
- [Forward Operating Base](forward-operating-base.md): the base that the rig must be placed inside
- [Hot Zone Magnet Towers](../game-modes-and-maps/hot-zone-magnet-towers.md): the numbered towers on each map that pull the Hot Zone with a code

## Season 3 update

The [official Season 3 notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) reduce Hot Zone Magnet spotted-target kill rewards from 1,650 to 1,500 cash and from 225 to 200 XP; these are separate from direct destruction rewards. A new kickback rewards depositing fuel into a FOB when it activates a drill, with no amount stated. Limited Mode excludes the Drill Rig.

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage table, placement conditions, fuel settings and cash rewards
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the cost and fuel changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): the rig's settings and placement checks
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
