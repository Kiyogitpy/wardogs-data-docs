---
title: "M113 APC SV"
parent: "Vehicles"
group: "Armored vehicles"
description: "Ten-seat tracked armored personnel carrier that rifle fire cannot destroy, sold under three faction names as a spawn vehicle."
---

# M113 APC SV

| M113 APC SV | |
|---|---|
| ![M113 APC SV]({{ '/assets/img/icons/other-trackers-textures/T_UI_MapTracker_SpawnVehicle.png' | relative_url }}){: .wiki-infobox-img } | |
| Type | Armored personnel carrier (spawn vehicle) |
| Seats | 10 (driver and 9 passengers) |
| Price | Not sold (no shop listing in the data) |
| Unlock level | Not applicable |
| Main health | 1,000 HP |
| Top speed | 71 (as stored) |
| Rifle damage taken (derived) | 0% on hull and tracks |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#land-tracked-leopard-spawn-spw-01) |
| Internal name | SPW_01 (Lonestar, Manticore and Valkyra faction versions) |
{: .wiki-infobox }

The M113 APC SV is a ten-seat tracked armored personnel carrier. It comes in three faction versions, Lonestar, Manticore and Valkyra, which share the same numbers in the data. It carries no weapons.

## Overview

The M113 APC SV is listed in the entity text table under the names Lonestar, Manticore and Valkyra, each described as a 10-seat tracked vehicle. The data has no shop row for it. Players get one at the side's deployment board in the spawn area (see Vehicle spawns below).

Its smoke countermeasure has 255 starting charges in the data. Smoke charges follow the vehicle inventory in the same way as flares: the smoke item must be added to the vehicle. The vehicle vendor sells smoke for 750 cash, one charge per purchase, the same as flares.

## Stats

| Stat | Value |
|---|---|
| Max speed | 71 (as stored) |
| Fuel capacity | 100 (as stored) |
| Fuel economy | 5.7 (as stored) |
| Seats | 10 |
| Max incline | 50 degrees |
| Countermeasures | Smoke (255 charges; screen active for 16 s, usable again after 90 s) |

## Armor and damage

Main health is 1,000 HP. The APC has separate health for its fuel tank (100 HP), each track (125 HP) and its radar (100 HP).

Rifle rounds do no damage to the hull and tracks, so rifle fire cannot destroy it. Cannon rounds do work:

| Ammunition | Hits to destroy |
|---|---:|
| 5.56 mm, 7.62×54 mm, .308 Win, .50 cal | Cannot be destroyed |
| 20×102 mm cannon | 366 |
| 30 mm cannon | 51 |

## Weapons and seats

The M113 APC SV has no weapons. It has ten seats: a driver and nine passenger seats.

## Handling

- Tracked drive with a top speed of 71 and a maximum incline of 50 degrees.
- The three faction versions share one configuration.

**Engine torque.** The torque curve is set against engine RPM up to 5,000 in the tracked drive data, and the torque values carry no unit label. See [Vehicle handling](vehicle-handling.md) for the other tracked numbers.

## Season 2 changes

- A new 125 mm rocket rule adds -10%.
- The 20×102 mm cannon rule changed from -60% to -84%, so cannon hits from that calibre now do less damage.
- Track rebound damping rose from 12,000 to 17,000.

## Vehicle spawns

Each side's spawn area has a deployment board that places this vehicle in the side's own version (Lonestar, Manticore or Valkyra): 3 boards per match on [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md) and [Saburtulo](../game-modes-and-maps/saburtulo.md). Players deploy onto it from the board. Each board has 4 to 6 vehicle slots. In the Saburtulo data the Lonestar and Manticore boards sit in each other's spawn areas, and a few other mismatches between board and yard tags exist (see [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md)). The board does not put the APC out until one side has reached a score of 20; before that it reads "Inactive Vehicle: Min Required Game Score: 20". A destroyed APC returns after 300 s, or after 60 s if the board's side is losing, meaning the best other side is ahead of it by 15 score points or more at the moment the APC is lost. The board shows the time left ("Spawn Vehicle will respawn in ..."). These timers time this APC only; a server setting can scale them (the base scale is 1). After a player deploys onto the APC, that player has a 600 s cooldown on that board ("Deployment on cooldown ..."). The numbers are the game's built-in defaults and the board Blueprint, read from the game's code.

The board shows one reason at a time, the first that applies in this order:

| Message on the board | When it shows |
|---|---|
| Spawn Vehicle will respawn in ... | The respawn countdown is running |
| Inactive Vehicle: Min Required Game Score: 20 | There is no live APC and no side has a score of 20 yet |
| No Active Spawn Vehicle | There is no APC |
| Spawn Vehicle Radar Destroyed : Awaiting Repairs | The APC's radar health reached zero; it clears when the radar is repaired to 55 percent of its maximum |
| Spawn vehicle is not in the control zone | The Control Zone rules report the APC outside the zone |
| Spawn vehicle is moving | The APC is moving at 10 km/h or more |
| No available seat | Every seat is taken |

The "moving" message looks like a warning only, because the deploy check still accepts a player when it is the reason (read from the game's code, not seen in play). A message about too little vehicle health exists in the text table, but no rule in the game uses it, and the 30 percent health value stored on the board is never read. A player who is on cooldown, or who has not yet entered the control zone ("MAP OFFLINE... ENTER ZONE FOR DATA"), sees that message instead of the moving or seat messages.

## See also

- [T-72B3](t-72b3.md), another tracked vehicle
- [Vehicle damage](vehicle-damage.md)

## Sources

- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md): which maps place this vehicle
- [Round 75 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round75-open-questions.md): the deployment board's messages, timers and cooldown read from the game's code
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the smoke screen's 16 s active window and 90 s cooldown, and the other round 41 vehicle readings
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
