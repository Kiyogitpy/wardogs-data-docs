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
| Internal name | `DA_Buildable_HotzoneMagnet` |
{: .wiki-infobox }

The Drill Rig is the most expensive structure that a player can build with a hammer. It only works inside a placement zone within a control zone, and it runs on Fuel Supplies. Once started, it runs for a set time that depends on the fuel added to it, and while it runs it pulls the hot zone toward it.

## Overview

The Drill Rig costs 2,750 Build Supplies and has 2,500 HP. It has no separate parts.

Destroying an enemy Drill Rig pays 2,750 cash and 700 Role XP. It pays the same reward as the Hot Zone Magnet, because the Drill Rig is the buildable form of the magnet.

## Building it

- **Cost:** 2,750 Build Supplies, whichever hammer builds it. Nothing is charged at placement.
- **Hammers:** Large only.
- **Placement:** It must be inside a friendly Forward Operating Base radius, inside a placement zone, and that zone must be inside a control zone. Unlike most structures, it has no ladder check and no safe zone check.
- **Stack limit:** 0, so it cannot be placed on top of another buildable. Nothing can be placed on top of it either.
- **Build stages:** Five, at 0, 25, 50, 75 and 100% of progress. The earlier stages have 70, 79, 98 and 95 weak spots. A hammer hit on a weak spot adds more progress (see [Buildables](../building.md#weak-spots)).
- **Build time:** Estimated from the hits to build in the table below, one hit per swing (derived, not timed in play).

| Building it | Small hammer | Medium hammer | Large hammer |
|---|---:|---:|---:|
| Hits to build | cannot place | cannot place | 917 (about 809.7 s) |
| Hits to repair from zero health | 19 | 10 | 7 |
| Hits to dismantle (your own) | 17 | 13 | 10 |

Seconds are an estimate: one hammer hit per swing, 0.567 s per hit for the Small and Medium hammers and 0.883 s for the Large (derived from the use animation, not measured).

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

While it runs, the Drill Rig pulls the hot zone toward it. Once activated, the rig shrinks the hot zone to 0.6 of its width and length with the world default, which is 36 percent of the area. The rig's own setting lists 0.5 instead, but the code reads the world default, and which value a live server uses is not shown.

**Movement.** The hot zone moves toward the activated rig at a speed given in metres per second. The game's default for this is 3 m/s, which the code reads. The rig's own setting lists 5 m/s; whether that replaces the 3 m/s in play is not confirmed. The time to arrive is the distance in metres divided by the speed, and that time is added to how long the rig stays active. Derived example: a hot zone 300 m away takes 100 s at 3 m/s and 60 s at 5 m/s.

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

The counts below use the Drill Rig's own damage table, the same way as every other structure. The other structures' counts are in the [Buildables](../building.md#hits-to-destroy-point-blank-derived) article.

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

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): cost, health, stages, damage table, placement conditions, fuel settings and cash rewards
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md): the cost and fuel changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy for each source of damage.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): the rig's settings and placement checks
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
