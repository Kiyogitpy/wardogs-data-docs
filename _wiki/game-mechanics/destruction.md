---
title: "Destruction"
parent: "Game Mechanics"
description: "What can be knocked down in the world, which explosives and vehicles can bring each kind down, and what the game data does and does not say about health."
---

# Destruction

| Destruction | |
|---|---|
| **Scope** | |
| Destructible props | 39 kinds: fences, walls, bollards, road signs, lamp posts, telephone poles, bushes and saplings |
| Building pieces | 63 wall, roof, floor, balcony and stair pieces are set up to break into debris |
| Street objects | 23 meshes (signs, poles, benches, bins, a traffic cone) have no break-apart piece in the data |
| **Demolition** | |
| Brought down by | Explosives (by size), vehicles (by type) and some player-built structures |
| Health | None in the game files for world props |
| **Internal name** | DA_NormalBuilding_MeshToPrefabLookup, DA_AnonymousBuilding_MeshToPrefabLookup, DA_Demolition_* |
{: .wiki-infobox }

The world of Wardogs can be damaged. Fences, walls, signs and other props can be brought down by explosions and vehicles, and a broken prop can leave a remnant behind. This article explains which kinds of object can break, which hits can break them, and what the game data says about the numbers. Where the data does not settle a question, the article says so.

## Overview

Destruction covers three kinds of object:

- **Building pieces.** The walls, roofs, floors, balconies, stairs and apartment corridor pieces of residential buildings. Each has a break-apart piece set up in the data, so the building can come apart into debris.
- **Demolition props.** The fences, walls, bollards, signs, poles, bushes and trees that can be demolished by a set of named damage sources. Each prop has a rule set that decides what can bring it down.
- **Street objects.** Road signs, telephone poles, lamp posts, benches, bins and a traffic cone. The data lists them for destruction, but none has a break-apart piece, so the data does not show how they break.

Player-built structures such as walls, doors and bunkers are a separate system with their own health. They are covered on the [Building](../building.md) page.

## How it works

A prop breaks when a hit comes from a source its rule set allows. The sources fall into three kinds:

- **Explosions, by size.** Small explosions are grenades, the 40 mm grenade, [C4 charges](../equipment/c4-charge.md), [claymores](../equipment/claymore.md) and [improvised explosive devices](../equipment/improvised-explosive-device.md). Medium explosions are rockets. Large explosions are [anti-tank mines](../equipment/at-mine.md), landmines, explosions from destroyed vehicles, 30 mm cannon shells and 120 mm rockets. A rule that allows all explosions accepts all three sizes.
- **Vehicles, by type.** Helicopters and airplanes, tracked vehicles such as tanks and the [M113 APC SV](../vehicles/m113-apc-sv.md), and wheeled vehicles such as the [Humvee](../vehicles/humvee.md), [Kodiak](../vehicles/kodiak.md), [Ural](../vehicles/ural.md), [Bobcat](../vehicles/bobcat.md) and [Dune Buggy](../vehicles/dune-buggy.md). Some rules count only the larger wheeled vehicles.
- **Other sources.** [Molotov](../equipment/molotov.md) fire counts only for bushes and saplings. Player-built structures count for some props. The data holds the rule for this, but not its details.

The table groups the props by what can bring them down.

| Props | What can bring them down |
|---|---|
| Chain-link and barbed-wire fences, metal sheets, small metal fences, metal structures, bollards, road signs and the newer wooden fence (type 02) | Any explosion, any vehicle, and player-built structures |
| Bushes and saplings | Any explosion, any vehicle, player-built structures, and Molotovs |
| Wooden fences (type 01), the Season 2 metal fence, lamp posts, telephone poles and telephone cable | Any explosion, and helicopters, airplanes, tracked vehicles and the larger wheeled vehicles. The wooden fences also count player-built structures |
| Brick walls, concrete fences and the large metal road sign | Large explosions and tracked vehicles |
| Concrete barriers, concrete fences, metal fences, ornamental fences and metal fence supports | Medium and large explosions, and tracked vehicles |

Small explosions never break the last two rows, and helicopters and airplanes never break them either. That is why the brick and concrete walls need a large explosion or a tank.

When a prop breaks, it can leave a **remnant**: a set of pieces that stays on the ground. The data has 19 remnant sets. Road signs and the metal signage are the only props that also spawn a separate remnant actor.

Season 2 added one new metal fence, which the larger explosions and larger vehicles break. It also changed the rules for the wooden fences, the bushes and the saplings. See the [Season 2 Patch Notes](../patch-notes/season-2.md) for the full list.

## Numbers

| Rule | Value |
|---|---|
| Minimum distance from a small explosion | 300 |
| Minimum distance from a medium explosion | 400 |
| Minimum distance from a large explosion | 500 |
| Minimum distance from a Molotov | 300 |
| Demolition props | 39 |
| Force threshold, building pieces | 1,200 |
| Force threshold, decorative pieces | 400 |
| Remnant sets | 19 |

The minimum distances are attached to each explosion rule in the data. The data does not give their unit or confirm what they do, so they are shown as the raw values.

A collision that can break a building piece or a decorative piece has to pass a force threshold: 1,200 for building pieces and 400 for decorative pieces. Damage from a type the data flags for destruction ignores these thresholds and breaks the piece whatever the force. Each is multiplied by 1,000 before the check, so the real thresholds are 1,200,000 and 400,000 in an internal value (speed times a scale). The game does not name a unit for it, so the thresholds are shown as raw values.

Two curves in the data rank destructible buildings by how much the player is looking at them. They do not change damage or what breaks. The game uses them to decide which nearby buildings to refresh first, so the ones that are close and in front of you are updated before the rest. A building's score is the angle curve value plus the distance curve value (the angle score is boosted while you look through a scope, and the distance is counted as shorter by the scope's zoom).

- The angle curve is the angle in degrees between where you are looking and the building. It starts at 0.7 straight ahead, falls to 0.2 at 90 degrees, and reaches 0 at 100 degrees.
- The distance curve is 1.0 up to 2,000, falls to 0.5 at 50,000 and to 0.1 at 75,000. The distance is in the game's length unit, which is probably centimetres (20 m, 500 m and 750 m); the unit itself is not stated (inferred).
- What the refresh itself changes on a building was not traced.

World props and building pieces hold no health, hit count or fall time in the game files. The building pieces carry only a debris look and, for one piece, an indestructible flag. A piece breaks when a hit passes the force thresholds above, so there is no health to state.

## Wreck explosions

When a vehicle or a fixed gun is destroyed, it plays an explosion picked for its type. The game files name 14 explosion sequences. The table shows which one each kind of wreck uses. Exact timing and look are on the [VFX page](../../content/Wardogs_VFX_v2.md).

| Destroyed | Explosion |
|---|---|
| Helicopters: [Z20 Lakota](../vehicles/z20-lakota.md) and the [Huey](../vehicles/huey.md) | Helicopter |
| [Havoc](../vehicles/havoc.md) | Havoc |
| [MH-6](../vehicles/mh-6.md) and its AH-6 variants | Little Bird |
| [Fixed-wing airplane](../vehicles/fixed-wing-airplane.md) and the PzH 2000 self-propelled howitzer | Tank |
| [Kodiak](../vehicles/kodiak.md), the [Humvee](../vehicles/humvee-m249.md) machine gun variant and the [Wolf 110](../vehicles/wolf-110.md) | Kodiak |
| [Dune Buggy](../vehicles/dune-buggy.md) | Dune Buggy |
| [Ural](../vehicles/ural.md) and the [Ural Defender](../vehicles/ural-defender.md) | Ural |
| [Talon 9K SAM](../building/talon-9k-sam.md), [Vanguard CIWS](../building/vanguard-ciws.md), [L81 Mortar](../building/l81-mortar.md) and [Loudspeaker](../building/loudspeaker.md) | Each has its own |
| 155 mm shells, Standard and Expensive | 155 mm shell |
| [Improvised Explosive Device](../equipment/improvised-explosive-device.md) | Improvised Explosive Device |
| [Forward operating base](../building/forward-operating-base.md) | Destroyed base |

Vehicles not in this table, such as the [T-72B3](../vehicles/t-72b3.md), use one general explosion recipe from the game files instead of a named sequence. This is read from the data; how it looks in play was not checked.

## Tips that follow from the numbers

- Grenades and charges can break the light props, such as the chain-link and metal fences and the lamp posts and telephone poles. They cannot break brick walls, concrete fences or concrete barriers. For those, use a large explosion or a tank.
- Helicopters and airplanes can break the light fences, bushes, lamp posts and poles, but not the brick walls, concrete fences, concrete barriers or metal fences in the last two rows.
- Bushes and saplings react to the widest range of sources, including Molotovs. Keep this in mind when you plan cover around them.

## See also

- [Building](../building.md): player-built structures, their health and what damages them
- [Vehicle damage](../vehicles/vehicle-damage.md): how vehicles take damage
- [Penetration and Ricochet](penetration-and-ricochet.md): what happens when a bullet hits a surface

## Sources

- [Destruction reference](../../content/Wardogs_Destruction_v2.md)
- [Demolition reference](../../content/Wardogs_Demolition_v2.md)
- [Demolition assets (row level)](../../content/Wardogs_DemolitionAssets_v1.md)
- [Buildables](../../game-features/Wardogs_Buildables_v1.md)
- [Season 2 changes: world, visuals and audio](../../season-2-changes/world-visuals-audio.md)
- [VFX (explosion sequences)](../../content/Wardogs_VFX_v2.md)
- [Round 42 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-modes-ai-other.md): which explosion sequence each destroyed item uses
- [Round 43 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round43-econ-buildables.md)
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
