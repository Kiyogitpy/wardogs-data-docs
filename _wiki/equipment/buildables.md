---
title: Buildables
parent: "Equipment"
group: "Emplacements and buildables"
description: "Everything players can build with hammers: Build Supplies cost, health, which hammer builds it, placement rules and how each damage type affects it."
---

# Buildables

| Buildables | |
|---|---|
| Structures | 32 definitions, including the parts of larger structures |
| Hammers | Small, Medium, Large |
| Stationary weapons | 6, built with the Large Hammer (Medium for the Loudspeaker) |
| Cost | Build Supplies |
| Health range | 250 HP (Barbed Wire) to 15,000 HP (Forward Operating Base) |
{: .wiki-infobox }

Players build structures such as walls, doors, bunkers and stations with a hammer. The hammer's size decides which structures it can build. Each structure costs Build Supplies, has a health value, and takes damage from weapons and explosives in its own way. Most structures must be placed inside a Forward Operating Base radius, so the base comes first.

## Overview

Each hammer builds a set of structures:

| Hammer | Shop cash | Build speed (shop text) | Can build |
|---|---:|---|---|
| Small Hammer | 100 | Slow | Barbed Wire, Recon Tent, Builder's Radio, Hesco Block (Small), Sandbag Wall, Hedgehog, Wood base |
| Medium Hammer | 800 | Moderate | Door, Gate, Hesco Wall, Hesco Block (Large), Shelter, and the parts of these |
| Large Hammer | 2,400 | Fast | Every structure above, plus Bremer Wall, Bunker, Recon Tower, Indirect Fire Shelter, Drill Rig, Refuel Station and Repair Station |

The Large Hammer is the only hammer that can place the Bunker, Recon Tower, Indirect Fire Shelter, Bremer Wall, Drill Rig, Refuel Station and Repair Station. The stationary weapons, listed below, are built with the Large Hammer, and the Loudspeaker can also be built with the Medium Hammer.

The export gives no display name for the Shelter and the Wood base, so this page uses the plain names "Shelter" and "Wood base".

### Structures

Parts of a larger structure, such as a floor or a roof, are placed with their parent and cannot be picked on their own. They are shown on the parent's row.

| Structure | Build Supplies | Health (HP) | Hammers | Parts |
|---|---:|---:|---|---|
| Sandbag Wall | 15 | 735 | S, M, L | |
| Wood base | 15 | 735 | S, M, L | |
| Barbed Wire | 7 | 250 | S, M, L | |
| Recon Tent | 7 | 300 | S, M, L | |
| Hedgehog | 22 | 4,500 | S, M, L | |
| Hesco Block (Small) | 15 | 1,600 | S, M, L | |
| Builder's Radio | 20 | 1,000 | S, M, L | |
| Hesco Block (Large) | 22 | 2,250 | M, L | |
| Hesco Wall | 75 | 4,600 | M, L | |
| Shelter | 250 | 2,250 | M, L | |
| Door | 80 | 2,200 | M, L | Door-only section 22 / 500 HP; top section 22 / 500 HP |
| Gate | 200 | 5,320 | M, L | Left and right halves 85 / 5,320 HP each; ramp 85 / 6,500 HP |
| Bremer Wall | 32 | 6,500 | L | |
| Bunker | 200 | 5,000 | L | Floor and roof 10 / 2,250 HP each |
| Recon Tower | 200 | 5,000 | L | Base floor, first floor and roof 10 / 2,250 HP each |
| Indirect Fire Shelter | 200 | 5,000 | L | Floor and ceiling 10 / 2,250 HP each |
| Refuel Station | 200 | 1,600 | L | |
| Repair Station | 200 | 1,600 | L | |
| Drill Rig | 2,750 | 2,500 | L | |
| Forward Operating Base | 30 | 15,000 | own item | Shop price 7,500 cash; placed from its own item, not a hammer |

Stationary weapons are built like structures, with the same placement rules:

| Stationary weapon | Build Supplies | Health (HP) | Hammers |
|---|---:|---:|---|
| Talon 9K-SAM | 650 | 3,000 | L |
| Vanguard CIWS | 1,200 | 5,000 | L |
| L81 Mortar | 600 | 3,000 | L |
| Loudspeaker | 200 | 1,000 | M, L |
| Stingray | 650 | 3,000 | L |
| MG Nest | 650 | 3,000 while under construction (1,800 once finished; see [MG Nest](mg-nest.md)) | L |

### Individual emplacements

Each stationary weapon has its own article, with its gun, ammunition, restock and Season 2 changes:

- [Talon 9K-SAM](talon-9k-sam.md): heavy mounted machine gun, 72 mm rounds
- [Vanguard CIWS](vanguard-ciws.md): automatic 20x102 mm cannon
- [L81 Mortar](l81-mortar.md): 120x800 mm shells, with an elevation table and flight data
- [Loudspeaker](loudspeaker.md): no weapon in the data
- [Stingray](stingray.md): UAV ammunition
- [MG Nest](mg-nest.md): .50 cal tracer rounds

### Individual structures

Each structure below has its own article, with its cost, placement, damage numbers and Season 2 changes. Variants that differ only in size or parts share one article.

- [Sandbag Wall](sandbag-wall.md): low cover wall, 735 HP
- [Wood base](wood-base.md): cover structure with the same numbers as the Sandbag Wall, placed inside a base radius
- [Barbed Wire](barbed-wire.md): the lowest-health structure, 250 HP
- [Recon Tent](recon-tent.md): small tent, 300 HP
- [Hedgehog](hedgehog.md): tank trap, 4,500 HP
- [Hesco Walls](hesco-walls.md): the Small and Large Hesco Blocks and the Hesco Wall
- [Bremer Wall](bremer-wall.md): the most health of any wall, 6,500 HP
- [Door](door.md) and [Gate](gate.md): closeable barriers with parts
- [Bunker](bunker.md), [Recon Tower](recon-tower.md) and [Indirect Fire Shelter](indirect-fire-shelter.md): large multi-part structures
- [Shelter](shelter.md): a single-piece shelter, 2,250 HP
- [Refuel and Repair Stations](refuel-and-repair-stations.md): vehicle service structures, one of each per base
- [Builder's Radio](builders-radio.md): support structure, up to 4 per base
- [Drill Rig](drill-rig.md): fuel-powered rig for the hot zone
- [Forward Operating Base](forward-operating-base.md): the base that anchors most building

## Effects

### Damage by source

Each structure has a damage row that changes how much damage each source does to it. The table shows the change for each source. A change of -85% means 15% of the damage is left. A change of +650% means the damage is multiplied by 7.5. A plus sign means more damage.

| Structure | HP | Melee | Bullets | Grenades | Rockets | C4 | IED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sandbag Wall | 735 | -80% | -85% | +0% | +650% | +200% | +500% |
| Hesco Block (Small) | 1,600 | -80% | -80% | +50% | +120% | +220% | +500% |
| Hesco Wall | 4,600 | +0% | -80% | +0% | +200% | +150% | +400% |
| Barbed Wire | 250 | -28% | -85% | +0% | +200% | +150% | +400% |
| Bunker | 5,000 | -10% | -80% | -50% | +45% | +50% | +200% |
| Recon Tower | 5,000 | -10% | -80% | -50% | +45% | +50% | +200% |
| Door | 2,200 | -80% | -85% | +0% | +650% | +200% | +800% |
| Gate | 5,320 | -80% | -85% | +0% | +850% | +1,000% | +2,000% |
| Hedgehog | 4,500 | -80% | -85% | -50% | +450% | +500% | +1,000% |
| Drill Rig | 2,500 | -80% | -85% | +0% | +850% | +500% | +1,500% |
| Builder's Radio | 1,000 | +70% | -85% | +500% | +1,000% | +400% | +800% |
| Forward Operating Base | 15,000 | -80% | -80% | +200% | +1,400% | +1,250% | +5,000% |

Plain reading: a Bunker takes about a fifth of the bullet damage, and rockets do their normal damage plus 45%. Rockets, C4 and IEDs multiply the damage to most structures. The Forward Operating Base is the most exposed to IEDs, at +5,000%, which is 51 times the normal damage. These are the damage entries that match one source on its own. Other entries, for particular weapons and ammunition, can also apply, so these figures are a first estimate. The hits each structure takes to destroy are derived in the table below.

The full table for every structure is on the [Buildables](../../game-features/Wardogs_Buildables_v1.md) data page.

One field of the Forward Operating Base's data is set to "do not take damage". How that interacts with its 15,000 HP is not yet known.

### Build stages

A structure is built in stages from 0 to 100%, and each stage shows a new part of the structure. Most multi-stage structures have five stages, at 0, 25, 50, 75 and 100%. The Door uses 0, 30, 60, 80 and 100%, and the Wood base 0, 20, 45, 70 and 100%. Parts such as floors and roofs have only one stage. Earlier stages have weak spots, which are shown as marked points on the half-built structure; a hammer hit on one adds more progress (see [Weak spots](#weak-spots)).

In the multi-part structures (Bunker, Door, Gate, Recon Tower, Indirect Fire Shelter and Hesco Wall), the last stage hands over to the finished parts. Each part is its own buildable with its own health, so a finished Bunker is several pieces, not one. This is **Derived** from the stage data.

## Use and timing

### Building

Building needs Build Supplies and a hammer. Each hammer hit adds progress: a normal hit adds the hammer's build amount divided by the structure's Build Supplies cost, so a structure takes fewer hits from a bigger hammer. A hit on a weak spot adds more (see [Weak spots](#weak-spots)):

| Hammer | Build amount per hit | Build amount on a weak spot | Season 2 weak-spot amount |
|---|---:|---:|---|
| Small | 0.5 | 3 | not listed as changed |
| Medium | 1 | 5 | 6 became 5 |
| Large | 1.5 | 8 | 10 became 8 |

The number of hits to build, repair or dismantle each structure is in its article, in a "Building it" table, for each hammer. The total Build Supplies to finish a structure is its cost, whichever hammer builds it. Build Supplies are used up a little with each hit, so a finished structure has taken its full cost. Nothing is charged when the structure is placed.

Some structures change the hit amount: Barbed Wire and Recon Tent count a hit 3.5 times as much, the Drill Rig 2 times and the Vanguard CIWS 1.25 times. The hit counts in the articles already include this.

The shop text describes the hammers as slow, moderate and fast. The time one hit takes in play is not published, so build time in seconds is not given.

### Repair and dismantle

- **Repair:** on a finished structure, a hammer hit restores health instead of adding progress. It restores the hammer's build amount times the structure's repair multiplier. Repairing uses Build Supplies too, and any supplies not needed are returned. The repair multiplier differs by structure: 1 for most walls, 6.7 for the Bunker, Recon Tower and Indirect Fire Shelter, 13.3 for the Refuel and Repair Stations and 150 for the Drill Rig. Each article gives its repair hit count.
- **Dismantle:** a hammer hit on your own structure does 150 (Small), 200 (Medium) or 250 (Large) damage. The data also sets half of that for a structure owned by someone else (the modifier name is read as "hostile"; this is inferred). Dismantling gives no Build Supplies back, as far as the data shows.
- **Unfinished structures:** damage removes build progress in proportion to the structure's maximum health. At zero progress the structure is destroyed.

### Weak spots

Weak spots are marked points on a structure that is being built. They only matter for building, and only for hammers:

- A hammer hit on a weak spot adds the larger build amount: 3, 5 or 8 for the Small, Medium and Large hammer, instead of 0.5, 1 or 1.5. That is 6, 5 and 5.3 times the normal hit, so a weak-spot hit builds about 5 to 6 times faster.
- Bullets and melee hits cannot hit a weak spot, because the spot ignores them.
- A spot is only offered when it is close to you: within 2.9 m of your view for the Small and Medium hammer, and 3.4 m for the Large hammer. The spots relocate on the structure as you build; how the next spot is chosen is not confirmed.
- Weak spots have nothing to do with damage. No damage entry uses them, so a structure does not take more damage from a bullet or rocket because of its weak spots.
- Barbed Wire and Recon Tent have their weak spots switched off, so every hit on them adds the normal amount.

The hit counts in the structure articles assume every hit is a normal hit, and the repair and dismantle counts also ignore weak spots. Hitting weak spots brings the build count down. The repair and dismantle counts are derived from the hit amounts, not checked in play, and for a hammer that cannot place a structure they still show what that hammer's hit does.

### Placement

- The build point must be within 6 m of the player.
- Most structures must be placed inside a friendly Forward Operating Base radius. The exceptions are the small structures: Barbed Wire, Recon Tent, Sandbag Wall and Hedgehog. Those cannot be placed inside an enemy base radius.
- Safe zone: most structures cannot be placed within 3 m of a safe zone, and a player standing in a safe zone cannot place one at all. The articles say which structures have this check.
- Ladder: most structures cannot be placed within 1 m of a ladder. The Drill Rig has no ladder or safe zone check.
- Stacking: a structure can be placed on top of another buildable only if the one below is finished and allows it, and the stack can only be as high as the structure's stack limit. The limits are given per structure: 100 for the Barbed Wire, Recon Tent, Sandbag Wall, Hedgehog and stations, 6 for the Builder's Radio and most stationary weapons, 1 for the Forward Operating Base, Shelter and Gate, and 0 (no stacking) for the Recon Tower and the Drill Rig.
- Builder's Radio: up to 4 per Forward Operating Base. It counts toward that limit.
- Refuel Station and Repair Station: 1 per Forward Operating Base each.
- Drill Rig: only inside a placement zone within a control zone.
- The rules for placing the Forward Operating Base itself are not yet known.

### Drill Rig

The Drill Rig is the buildable form of the map's hot zone magnet. It needs fuel to run. After placement it waits 15 s before it can start. It needs at least 2,000 fuel to run, each fuel unit buys 0.03 s of run time, and it holds up to 10,000 fuel. The run time is therefore 60 s at the minimum and 300 s on a full tank. The recharge after a run is 900 s. Starting it is a 10 s hold within 2 m. These seconds are **Derived**: the data gives the numbers, and the timers in the Blueprints use them as seconds.

While it runs, the Drill Rig pulls the hot zone toward it. How the zone moves is not confirmed.

### Refuel and repair

The Refuel Station and Repair Station work with Fuel Supplies and Mechanical Supplies. Each has a Fast restock (5% in 3 s, for 75 or 100 cash) and a Max restock (up to 100% in 9 s, for 1,500 or 2,000 cash), using 5 supplies per restock. See [Refuel and Repair Stations](refuel-and-repair-stations.md).

## Cost

The cost column in the Structures table is the Build Supplies cost, and it is the total a structure uses up, whichever hammer builds it. Build Supplies are used while the structure is built, not when it is placed. Build Supplies are sold in lots of 50 for 10 cash a lot (0.2 cash per unit).

Hammers cost 2,400 cash (Large), 800 (Medium) and 100 (Small). The Forward Operating Base costs 7,500 cash.

## Hits to destroy (point blank, derived)

Derived from each source's base damage and the damage table. It is not a count from play: each figure assumes every shot lands at point blank for full damage, with no falloff and no other rules, so real fights can differ. Base damage used: M4 5.56 mm FMJ 28, M67 frag grenade 100, 120 mm rocket 150, C4 charge 250. Parts of larger structures (floors, roofs, door sections) have less health and take fewer hits. Each structure's article gives its parts.

| Structure | HP | M4 5.56 mm FMJ | M67 frag grenade | 120 mm rocket | C4 charge |
|---|---:|---:|---:|---:|---:|
| Barbed Wire | 250 | 60 | 3 | 1 | 1 |
| Recon Tent | 300 | 72 | 3 | 1 | 1 |
| Sandbag Wall | 735 | 175 | 8 | 1 | 1 |
| Wood base | 735 | 175 | 8 | 1 | 1 |
| Hedgehog | 4,500 | 1072 | 90 | 6 | 3 |
| Hesco Block (Small) | 1,600 | 286 | 11 | 5 | 2 |
| Builder's Radio | 1,000 | 239 | 2 | 1 | 1 |
| Hesco Block (Large) | 2,250 | 402 | 15 | 9 | 4 |
| Hesco Wall | 4,600 | 822 | 46 | 11 | 8 |
| Shelter | 2,250 | 402 | 15 | 9 | 4 |
| Door | 2,200 | 524 | 22 | 2 | 3 |
| Gate | 5,320 | 1267 | 54 | 4 | 2 |
| Bremer Wall | 6,500 | 1161 | 44 | 13 | 7 |
| Bunker, Recon Tower or Indirect Fire Shelter | 5,000 | 893 | 100 | 23 | 14 |
| Refuel Station or Repair Station | 1,600 | 286 | 11 | 1 | 1 |
| Drill Rig | 2,500 | 596 | 25 | 2 | 2 |
| Forward Operating Base | 15,000 | 2679 | 50 | 7 | 5 |

## Season 2 changes

The following build costs changed in Season 2:

| Structure | Season 1 | Season 2 |
|---|---:|---:|
| Indirect Fire Shelter | 100 | 200 |
| Bremer Wall | 15 | 32 |
| Bunker | 100 | 200 |
| Recon Tower | 100 | 200 |
| Door | 22 | 80 |
| Gate | 85 | 200 |
| Drill Rig | 2,250 | 2,750 |

The Drill Rig's fuel values changed too: the minimum fuel to run went from 1,500 to 2,000, the maximum fuel from 7,500 to 10,000, and the run time per fuel unit from 0.05 to 0.03.

Several entries in the buildable damage table changed by 5 to 17 percentage points. The Season 2 data does not say which structures they apply to.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), for the explosives that damage structures
- [Fire, Smoke and Flash](fire-smoke-and-flash.md), for the Molotov fire
- [Utility Items](utility-items.md), for the Fuel and Mechanical Supplies, and the Light and Heavy Drills
- [Vehicles data page](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md), for the vehicles that the Refuel and Repair Stations serve
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): costs, health, stages, damage rows, placement rules and the Drill Rig settings
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): hammer prices, build speed text and supply prices
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): build cost, hammer and damage row changes
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): derived hits to destroy and the stationary weapons' health.
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
