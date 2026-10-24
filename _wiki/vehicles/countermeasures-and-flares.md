---
title: "Countermeasures and flares"
parent: "Vehicles"
group: "Reference"
description: "Which Wardogs vehicles carry flares or smoke, how many they get, how flares are meant to work against heat-seeking lock-on weapons, and what the data does not yet say about reloading."
---

# Countermeasures and flares

| Countermeasures and flares | |
|---|---|
| **General** | |
| Type | Mechanic |
| Applies to | Helicopters, the airplane and one tank |
| Countermeasures | Flares (helicopters, airplane), Smoke (L2A6) |
| Fire key | V on keyboard, as the Fire Countermeasures action |
| **Availability** | |
| Flares price | 750 cash, unlock level 1 |
| Smoke price | 750 cash, unlock level 1 |
{: .wiki-infobox }

Countermeasures are launched from a vehicle to draw off or confuse incoming attacks. In Wardogs they are flares for aircraft and smoke for the L2A6. Each vehicle's stats sheet lists its countermeasure, and most ground vehicles list none.

## Overview

Flares are an anti-air countermeasure. The item text says a flare use "deploys 3x bursts of flares". Smoke is a newer countermeasure that Season 2 added. It lays a sustained trail of smoke around the vehicle rather than a burst of flares.

## How it works

### Flares against lock-on weapons

The in-game tip says flares "can be used to momentarily prevent heat-seeking projectiles from locking onto your helicopter". The same tip set gives a second way to stay hidden from some launchers: "flying low stops certain launchers being able to lock on to your vehicle".

The data does not say how a flare burst changes the lock of a particular launcher, or how long the lock is broken. The Talon 9K-SAM is a fixed emplacement rather than a vehicle weapon, and the data does not say how flares interact with its targeting. See the [Talon 9K-SAM](../equipment/talon-9k-sam.md) article for the emplacement itself.

### Smoke

Smoke is a sustained countermeasure. A smoke screen is visible for 6 seconds in total: a 2 second fade in, a 2 second hold at full density, and a 2 second fade out. The data does not say whether smoke affects lock-on weapons or how much.

### Amounts and reloading

Each flare-carrying vehicle has a starting count in the data, and each burst stays active for 3.5 seconds. The fixed-wing airplane starts with 3 flares, the Havoc with 2, the MH-6 and AH-6 family with 2, and the Z20 Lakota with 2. The item text's "3 bursts per use" does not match these helicopter counts, and the data does not say how the two fit together. How flares are restocked is not yet known.

### Season 2 changes

Season 2 renamed the flares input to Fire Countermeasures. The key stays the same, and the flares item itself did not change. Smoke was added as a new countermeasure at 750 cash, unlock level 1.

## Numbers

| Vehicle | Countermeasure | Amount | Notes |
|---|---|---|---|
| [Havoc](havoc.md) | Flares | 2 starting | Active 3.5 s; range band 5 to 300 m |
| [MH-6](mh-6.md) | Flares | 2 starting | Active 3.5 s; range band 10 to 300 m |
| [AH-6M [Miniguns]](ah-6m-miniguns.md) | Flares | 2 starting | Active 3.5 s; range band 10 to 300 m |
| [AH-6R [Rockets]](ah-6r-rockets.md) | Flares | 2 starting | Active 3.5 s; range band 10 to 300 m |
| [Z20 Lakota](z20-lakota.md) | Flares | 2 starting | Active 3.5 s; range band 15 to 300 m |
| [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md) | Flares | 2 starting | Active 3.5 s; range band 15 to 300 m |
| [Fixed-wing airplane](fixed-wing-airplane.md) | Flares | 3 starting | Active for 3.5 seconds; no range band set |
| [L2A6](l2a6.md) | Smoke | Not stated | Sustained smoke trail, visible for 6 seconds |

The other vehicles list no countermeasure, or list "Not stated" for it. These include the SPH-2 (not stated for its variant), the Flakpanzer Gepard, the T-72B3, the M113 APC SV and every wheeled vehicle.

## Tips that follow from the numbers

- Flares are the only countermeasure for the helicopter and airplane group, so a helicopter pilot should treat them as the main defence against heat-seeking attacks.
- Smoke lasts 6 seconds in total, so a smoke screen is short. Use it as a short cover, not a long one.
- Because the airplane's flares are a fixed count of 3, use them when they matter most rather than as a routine.
- The data gives each helicopter 2 starting flares, while the item text says 3 bursts per use. Check the vehicle's own article before planning a long flight.

## See also

- [Vehicle weapons](vehicle-weapons.md): the guns and launchers mounted on vehicles
- [Vehicle damage](vehicle-damage.md): how hits reach the vehicle
- [Talon 9K-SAM](../equipment/talon-9k-sam.md): a fixed anti-air emplacement
- [Vehicles](../vehicles.md): the full list of vehicles

## Sources

- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md): countermeasure items, prices and the smoke item
- [Vehicles Reference](../../content/Wardogs_Vehicles_v2.md): the airplane's countermeasure data and input change
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): countermeasure lists per vehicle
- [Smoke grenade effect data](../../content/Wardogs_GameplayCues_v2.md): the smoke screen timing
- [Frontend, Server and Test Data](../../content/Wardogs_DataTables_Frontend_v1.md): the in-game tips on flares and flying low
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md): prices and unlock levels
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): starting flare counts, active time and range bands for each flare-carrying vehicle.
