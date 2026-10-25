---
title: "Building a Base"
parent: "Guides"
description: "Build Supplies and the three hammers, why the Forward Operating Base comes first, what each structure costs and how much health it gives, how many hits each takes to build and to destroy, and the stationary emplacements compared."
---

# Building a Base

Players build walls, stations and emplacements with hammers, and every structure costs Build Supplies. Most structures must sit inside a friendly Forward Operating Base radius, so the base is the first thing to place. This guide covers the tools and supplies, what to build first and why, how the stationary emplacements compare, and how quickly each structure falls to the four damage sources the wiki derives. Each figure links to the article it comes from.

## Hammers and Build Supplies

Each hammer builds a set of structures, and the larger hammers do more progress per hit ([Hammers](../equipment/hammers.md), [Buildables](../building.md#overview)).

| Hammer | Price (cash) | Build per hit | Build on a weak spot | Structures it can place |
|---|---:|---:|---:|---:|
| Small | 100 | 0.5 | 3 | 7 |
| Medium | 800 | 1 | 5 | 12 |
| Large | 2,400 | 1.5 | 8 | 19 |

Every hammer spends Build Supplies. Build Supplies sell in lots of 50 for 10 cash ([Supplies](../equipment/supplies.md)).

### Tips that follow from the numbers

- **Same supplies, fewer hits.** A bigger hammer does not change what a structure costs in Build Supplies. It only changes how many hits it takes. A Sandbag Wall takes 30 hits with the Small Hammer, 15 with the Medium and 10 with the Large ([Buildables](../building.md#building)).
- **Hit the weak spots to build 5 to 6 times faster.** A hit on a weak spot adds 3, 5 or 8 build progress (Small, Medium, Large) instead of 0.5, 1 or 1.5. Only a hammer can hit a weak spot, because bullets cannot. Barbed Wire and Recon Tent have their weak spots switched off ([Buildables](../building.md#weak-spots)).
- **Weak spots are about building, not damage.** No damage entry in the data uses them, so a structure does not take more damage because it has them.
- **Repair with the big hammer.** On a finished structure, each hit restores health at the hammer's build amount times the structure's repair multiplier, and the repair uses Build Supplies too. The Large Hammer needs fewer repair hits than the Small one for every structure in the data (see each article's "Building it" table).

## How many hits to build

Each hit adds the hammer's build amount divided by the structure's Build Supplies cost to its progress. The table gives the hits to finish each structure, with normal hits only. Seconds are an estimate, shown in brackets: one hammer hit per swing takes 0.567 s with the Small and Medium hammers and 0.883 s with the Large, derived from the use animation and not measured in play.

| Structure | Build Supplies | Small hits | Medium hits | Large hits |
|---|---:|---:|---:|---:|
| Barbed Wire | 7 | 4 (about 2.3 s) | 2 (about 1.1 s) | 2 (about 1.8 s) |
| Recon Tent | 7 | 4 (about 2.3 s) | 2 (about 1.1 s) | 2 (about 1.8 s) |
| Sandbag Wall | 15 | 30 (about 17.0 s) | 15 (about 8.5 s) | 10 (about 8.8 s) |
| Wood base | 15 | 30 (about 17.0 s) | 15 (about 8.5 s) | 10 (about 8.8 s) |
| Hesco Block (Small) | 15 | 30 (about 17.0 s) | 15 (about 8.5 s) | 10 (about 8.8 s) |
| Builder's Radio | 20 | 40 (about 22.7 s) | 20 (about 11.3 s) | 14 (about 12.4 s) |
| Hedgehog | 22 | 44 (about 24.9 s) | 22 (about 12.5 s) | 15 (about 13.2 s) |
| Hesco Block (Large) | 22 | cannot place | 22 (about 12.5 s) | 15 (about 13.2 s) |
| Hesco Wall | 75 | cannot place | 75 (about 42.5 s) | 50 (about 44.1 s) |
| Shelter | 250 | cannot place | 250 (about 141.8 s) | 167 (about 147.5 s) |
| Door | 80 | cannot place | 80 (about 45.4 s) | 54 (about 47.7 s) |
| Gate | 200 | cannot place | 200 (about 113.4 s) | 134 (about 118.3 s) |
| Bremer Wall | 32 | cannot place | cannot place | 22 (about 19.4 s) |
| Bunker, Recon Tower, Indirect Fire Shelter | 200 | cannot place | cannot place | 134 (about 118.3 s) |
| Refuel and Repair Stations | 200 | cannot place | cannot place | 134 (about 118.3 s) |
| Drill Rig | 2,750 | cannot place | cannot place | 917 (about 809.7 s) |

The Forward Operating Base has no hits: it is placed at once from its own item. Each structure's article has the repair and dismantle hits too.


- The Large Hammer is the only hammer that places the Bunker, Recon Tower, Indirect Fire Shelter, Bremer Wall, Drill Rig, Refuel Station and Repair Station ([Buildables](../building.md#overview)). Buy it if the base needs any of these.
- The Large Hammer gives three times the build progress per hit of the Small Hammer (1.5 against 0.5) for 24 times the price (2,400 against 100). Derived from the table above.
- The Small Hammer, at 100 cash, builds Barbed Wire (7 Build Supplies), Sandbag Wall (15), Wood base (15) and Hesco Block (Small) (15) ([Hammers](../equipment/hammers.md), [Buildables](../building.md#overview)).

## The Forward Operating Base comes first

The Forward Operating Base (FOB) is the anchor for building. It is placed from its own item rather than a hammer, costs 7,500 cash in the shop and has a Build Supplies cost of 30 (nothing is charged at placement), and has 15,000 HP, the most of any structure ([Forward Operating Base](../building/forward-operating-base.md)).

- **Radius.** Most structures must be placed inside a friendly FOB radius. The exceptions are Barbed Wire, Recon Tent, Sandbag Wall and Hedgehog ([Buildables](../building.md#use-and-timing)). A new FOB also cannot be placed within about 42 m of another one.
- **Limits.** Each FOB allows one Refuel Station, one Repair Station and up to four Builder's Radios ([Forward Operating Base](../building/forward-operating-base.md#building-it)).
- **Exposure.** The FOB takes 51 times normal IED damage, 15 times rocket damage and 13.5 times C4 damage, the largest multipliers of any structure ([Forward Operating Base](../building/forward-operating-base.md#durability)).

### Tips that follow from the numbers

- Because most structures need the FOB radius, place the FOB before any wall or station. The small structures are the only ones that can go down without one.
- The FOB takes 51 times normal IED damage, more than any other structure in the damage table, so IEDs are its most damaging source in the data ([Forward Operating Base](../building/forward-operating-base.md#durability)).
- Destroying an enemy FOB pays the attacker 2,500 cash plus up to 7,500 by its supplies, and hacking one pays 1,000 ([Cash and Rewards](../progression-and-economy/cash-and-rewards.md#spotting-supply-crates-and-buildables)).

## What to build first

The table lists every structure with its Build Supplies cost and health. The last column is derived here by dividing health by Build Supplies, as a rough measure of health bought per supply.

| Structure | Build Supplies | Health (HP) | Hammers | HP per Build Supply (derived) |
|---|---:|---:|---|---:|
| Barbed Wire | 7 | 250 | S, M, L | 35.7 |
| Recon Tent | 7 | 300 | S, M, L | 42.9 |
| Sandbag Wall | 15 | 735 | S, M, L | 49.0 |
| Wood base | 15 | 735 | S, M, L | 49.0 |
| Hesco Block (Small) | 15 | 1,600 | S, M, L | 106.7 |
| Builder's Radio | 20 | 1,000 | S, M, L | 50.0 |
| Hedgehog | 22 | 4,500 | S, M, L | 204.5 |
| Hesco Block (Large) | 22 | 2,250 | M, L | 102.3 |
| Hesco Wall | 75 | 4,600 | M, L | 61.3 |
| Shelter | 250 | 2,250 | M, L | 9.0 |
| Door | 80 | 2,200 | M, L | 27.5 |
| Gate | 200 | 5,320 | M, L | 26.6 |
| Bremer Wall | 32 | 6,500 | L | 203.1 |
| Bunker | 200 | 5,000 | L | 25.0 |
| Recon Tower | 200 | 5,000 | L | 25.0 |
| Indirect Fire Shelter | 200 | 5,000 | L | 25.0 |
| Refuel Station | 200 | 1,600 | L | 8.0 |
| Repair Station | 200 | 1,600 | L | 8.0 |
| Drill Rig | 2,750 | 2,500 | L | 0.9 |
| Forward Operating Base | 30 | 15,000 | Own item | 500.0 |

Sources for these numbers: [Buildables](../building.md#structures), with each structure's article: [Barbed Wire](../building/barbed-wire.md), [Recon Tent](../building/recon-tent.md), [Sandbag Wall](../building/sandbag-wall.md), [Wood base](../building/wood-base.md), [Hesco Walls](../building/hesco-walls.md), [Builder's Radio](../building/builders-radio.md), [Hedgehog](../building/hedgehog.md), [Shelter](../building/shelter.md), [Door](../building/door.md), [Gate](../building/gate.md), [Bremer Wall](../building/bremer-wall.md), [Bunker](../building/bunker.md), [Recon Tower](../building/recon-tower.md), [Indirect Fire Shelter](../building/indirect-fire-shelter.md), [Refuel and Repair Stations](../building/refuel-and-repair-stations.md), [Drill Rig](../building/drill-rig.md).

### Tips that follow from the numbers

- **Walls for the price.** The Hesco Block (Small) and the Sandbag Wall both cost 15 Build Supplies, but the Hesco has 1,600 HP against 735. The damage table makes the Hesco the sturdier of the two in every column of the hits table below, so it is the better buy at the same cost ([Hesco Walls](../building/hesco-walls.md), [Sandbag Wall](../building/sandbag-wall.md)).
- **Most health per supply.** The Hedgehog (4,500 HP for 22 Build Supplies) and the Bremer Wall (6,500 HP for 32) give the most health per supply of any wall or barrier, about 200 HP per Build Supply each ([Hedgehog](../building/hedgehog.md), [Bremer Wall](../building/bremer-wall.md)).
- **Least health per supply.** The Drill Rig gives 0.9 HP per Build Supply and the Shelter 9. The Shelter needs the Medium or Large Hammer and the Drill Rig needs the Large Hammer, so buy them for their function, not their health ([Drill Rig](../building/drill-rig.md), [Shelter](../building/shelter.md)).
- **Stations are fragile for their cost.** The Refuel and Repair Stations cost 200 Build Supplies for 1,600 HP, which is 8 HP per supply. A rocket or a C4 charge destroys either one in a single hit ([Refuel and Repair Stations](../building/refuel-and-repair-stations.md#hits-to-destroy-point-blank-derived)).
- **Season 2 raised several costs.** The Bremer Wall went from 15 to 32 Build Supplies, the Door from 22 to 80, the Bunker from 100 to 200 and the Drill Rig from 2,250 to 2,750 ([Buildables](../building.md#season-2-changes)).

## Stationary emplacements

Six stationary weapons are buildable. Five are built with the Large Hammer and the Loudspeaker with the Medium or Large Hammer ([Buildables](../building.md#overview)).

| Emplacement | Build Supplies | Health (HP) | Gun and ammunition | Restock | What the data says it counters |
|---|---:|---:|---|---|---|
| [L81 Mortar](../building/l81-mortar.md) | 600 | 3,000 | 120x800 mm shells, 132 to 684 m | 150 Ammo Supplies | Targets are not listed. Its range table runs 132 to 684 m |
| [Talon 9K-SAM](../building/talon-9k-sam.md) | 650 | 3,000 | 72 mm heavy machine gun, 1,000 m effective | 200 Ammo Supplies | Targets are not listed. Lock-on takes 2.0 s |
| [Stingray](../building/stingray.md) | 650 | 3,000 | UAV drone projectile, lock-on | 900 Mechanical Supplies and 5,000 cash | Air vehicles only: the Little Bird family, the Havoc and the fixed-wing airplane |
| [MG Nest](../building/mg-nest.md) | 650 | 1,800 when finished (3,000 under construction) | .50 cal tracer machine gun | 200 Ammo Supplies for 60 rounds | Targets are not listed. 600 rounds/min, 1,000 m range, 8 s reload |
| [Vanguard CIWS](../building/vanguard-ciws.md) | 1,200 | 5,000 | 20x102 mm cannon, 1,800 rounds/min, 1,000 m | 250 Ammo Supplies for 500 rounds | Targets are not listed |
| [Loudspeaker](../building/loudspeaker.md) | 200 | 1,000 | No weapon in the data | Not applicable | Not applicable |

Restock costs at the Supplies lot price of 10 cash per 50 are derived: 200 Ammo Supplies is about 40 cash, 250 is 50 cash and 150 is 30 cash ([Supplies](../equipment/supplies.md)).

### Tips that follow from the numbers

- **Only the Stingray has a target list in the data.** It is air-only, so it is the only emplacement here whose role is stated. For the other guns, the data gives the range, rate or lock-on time but not the targets, so this guide does not say what they counter.
- **Health and price.** The Vanguard CIWS has the most health (5,000) and costs 1,200 Build Supplies, 1.85 times the 650 of the Talon, Stingray and MG Nest (derived). The L81 Mortar is the cheapest gun at 600 Build Supplies, with 3,000 HP, the same as the Talon and Stingray.
- **The MG Nest is the weakest finished emplacement.** It has 1,800 HP when finished, and the 3,000 HP figure applies only while it is under construction ([MG Nest](../building/mg-nest.md#health)).
- **The Stingray has the largest restock.** It needs 900 Mechanical Supplies and 5,000 cash each time, while the other guns restock with Ammo Supplies only ([Stingray](../building/stingray.md#overview)).
- **Restock cost is a running cost.** The restocks above add up over a match, so budget for them along with the build cost ([Making Money](making-money.md#restocks-for-stationary-weapons)).

## How fast each structure falls

The derived table below gives the hits needed to destroy each structure with six sources: an M4 with 5.56 mm full metal jacket (28 base damage per hit), a .50 cal full metal jacket (90), a 120 mm rocket (150), an M67 frag grenade (100, which counts as a rocket against structures), a C4 charge (250) and an IED (300). Matching damage entries are stacked, so a rocket is not counted at its base damage alone. Each figure assumes every shot lands at point blank for full damage, with no falloff, so real fights differ ([Buildables](../building.md#hits-to-destroy-point-blank-derived)).

| Structure | HP | M4 5.56 mm FMJ | .50 cal FMJ | 120 mm rocket | M67 frag grenade | C4 charge | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Barbed Wire | 250 | 60 | 19 | 1 | 1 | 1 | 1 |
| Recon Tent | 300 | 72 | 23 | 1 | 1 | 1 | 1 |
| Sandbag Wall | 735 | 175 | 55 | 2 | 1 | 1 | 1 |
| Wood base | 735 | 175 | 55 | 2 | 1 | 1 | 1 |
| Builder's Radio | 1,000 | 239 | 75 | 1 | 1 | 1 | 1 |
| Hesco Block (Small) | 1,600 | 286 | 89 | 4 | 8 | 2 | 1 |
| Refuel Station or Repair Station | 1,600 | 286 | 89 | 1 | 1 | 1 | 6 |
| Hesco Block (Large) | 2,250 | 402 | 125 | 7 | 13 | 4 | 2 |
| Shelter | 2,250 | 402 | 125 | 7 | 13 | 4 | 2 |
| Door | 2,200 | 524 | 163 | 4 | 3 | 3 | 1 |
| Hesco Wall | 4,600 | 822 | 256 | 21 | 16 | 8 | 4 |
| Hedgehog | 4,500 | 1,072 | 334 | 8 | 9 | 6 | 3 |
| Gate | 5,320 | 1,267 | 395 | 5 | 6 | 2 | 1 |
| Bremer Wall | 6,500 | 1,161 | 362 | 11 | 19 | 7 | 5 |
| Bunker, Recon Tower or Indirect Fire Shelter | 5,000 | 893 | 278 | 33 | 35 | 27 | 12 |
| Drill Rig | 2,500 | not in the data | not in the data | not in the data | not in the data | not in the data | not in the data |
| Forward Operating Base | 15,000 | 2,679 | 834 | 5 | 10 | 5 | 1 |

Parts of larger structures, such as a Door's top section or a Bunker's floor, have less health and take fewer hits. Each structure's article gives its parts.

### Tips that follow from the numbers

- **Explosives finish the cheap structures.** One C4 charge destroys the Barbed Wire, Recon Tent, Sandbag Wall, Wood base, Builder's Radio, and the Refuel and Repair Stations. One 120 mm rocket does the same, except the Sandbag Wall and Wood base, which take 2, against 175 M4 hits.
- **Small arms are slow.** The Gate (1,267 M4 hits), the Hedgehog (1,072) and the Bremer Wall (1,161) need the most rifle hits of the large structures. Against M67 grenades, the Bunker family takes 35 hits, the most of any non-FOB structure.
- **Rockets are the Gate's and the Door's weak point.** The Gate takes 850% more rocket damage than normal and the Door 650% more, so they need 5 and 4 hits from a 120 mm rocket, against 1,267 and 524 M4 hits ([Gate](../building/gate.md), [Door](../building/door.md)).
- **Against the FOB, C4 and rockets are the fast routes.** The FOB needs 5 rocket hits and 5 C4 charges, against 2,679 M4 hits ([Forward Operating Base](../building/forward-operating-base.md#hits-to-destroy-point-blank-derived)).
- **Emplacements are not in the hits table.** The derived hits cover structures only. The emplacements are compared by health alone in the table above.

## See also

- [Building](../building.md): costs, health, placement and damage for every structure
- [Hammers](../equipment/hammers.md) and [Supplies](../equipment/supplies.md)
- [Forward Operating Base](../building/forward-operating-base.md)
- [Grenades and Explosives](../equipment/grenades-and-explosives.md): the explosives that damage structures
- [Making Money](making-money.md): cash costs of restocks and repairs
- [Beginner's Guide](beginners-guide.md): combat basics

## Sources

- [Building](../building.md)
- [Hammers](../equipment/hammers.md)
- [Supplies](../equipment/supplies.md)
- [Forward Operating Base](../building/forward-operating-base.md)
- Structures: [Barbed Wire](../building/barbed-wire.md), [Recon Tent](../building/recon-tent.md), [Sandbag Wall](../building/sandbag-wall.md), [Wood base](../building/wood-base.md), [Hesco Walls](../building/hesco-walls.md), [Builder's Radio](../building/builders-radio.md), [Hedgehog](../building/hedgehog.md), [Shelter](../building/shelter.md), [Door](../building/door.md), [Gate](../building/gate.md), [Bremer Wall](../building/bremer-wall.md), [Bunker](../building/bunker.md), [Recon Tower](../building/recon-tower.md), [Indirect Fire Shelter](../building/indirect-fire-shelter.md), [Refuel and Repair Stations](../building/refuel-and-repair-stations.md), [Drill Rig](../building/drill-rig.md)
- Emplacements: [L81 Mortar](../building/l81-mortar.md), [Talon 9K-SAM](../building/talon-9k-sam.md), [Stingray](../building/stingray.md), [MG Nest](../building/mg-nest.md), [Vanguard CIWS](../building/vanguard-ciws.md), [Loudspeaker](../building/loudspeaker.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md), for the cash paid for destroying an enemy FOB and for placing one
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the Drill Rig settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): structure hit counts for every listed source, the IED entries and the build time estimates
- [Round 44 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round44-econ-buildables.md)
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
