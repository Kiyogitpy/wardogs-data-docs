---
title: "Countermeasures and flares"
parent: "Vehicles"
group: "Reference"
description: "Which Wardogs vehicles carry flares or smoke, how many they get, how flares are meant to work against heat-seeking lock-on weapons, and how they are restocked."
---

# Countermeasures and flares

| Countermeasures and flares | |
|---|---|
| **General** | |
| Type | Mechanic |
| Applies to | Helicopters, the airplane and four tracked vehicles |
| Countermeasures | Flares (helicopters, airplane), Smoke (L2A6, T-72B3, Flakpanzer Gepard, M113 APC SV) |
| Fire key | V on keyboard, as the Fire Countermeasures action |
| **Availability** | |
| Flares price | 750 cash, unlock level 1 |
| Smoke price | 750 cash, unlock level 1 |
{: .wiki-infobox }

Countermeasures are launched from a vehicle to draw off or confuse incoming attacks. In Wardogs they are flares for aircraft and smoke for the L2A6. Each vehicle's stats sheet lists its countermeasure, and most ground vehicles list none.

## Overview

Flares are an anti-air countermeasure. The item text says a flare use "deploys 3x bursts of flares", but each press uses one flare (see Amounts and reloading). Smoke is a newer countermeasure that Season 2 added. It lays a sustained trail of smoke around the vehicle rather than a burst of flares.

## How it works

### Flares against lock-on weapons

The in-game tip says flares "can be used to momentarily prevent heat-seeking projectiles from locking onto your helicopter". The same tip set gives a second way to stay hidden from some launchers: "flying low stops certain launchers being able to lock on to your vehicle".

A search of the game client found no rule that makes a flare clear or break a missile lock, and no code found clears a lock while flares are active. In the client code read, a lock only decides whether a lock-on weapon can fire. A server-side effect is not ruled out. A missing rule in the client does not show that flares do nothing against lock-on; it means no such rule was found. The data does not say how a flare burst would change the lock of a particular launcher, or how long a lock would be broken. Missile lock against flares stays not confirmed. The Talon 9K-SAM is a fixed emplacement rather than a vehicle weapon, and the data does not say how flares interact with its targeting. See the [Talon 9K-SAM](../building/talon-9k-sam.md) article for the emplacement itself.

### Smoke

Smoke is a sustained countermeasure. A vehicle's smoke screen stays active for 16 seconds after it is fired, and the vehicle can use it again 90 seconds after that first use. The 6 seconds that appear in the smoke effect data are the look of the grenade-style smoke cloud (a 2 second fade in, a 2 second hold at full density and a 2 second fade out). They are not the screen's active time, and the data does not state how long a vehicle's cloud is drawn. The data does not say whether smoke affects lock-on weapons or how much.

### Amounts and reloading

Each flare-carrying vehicle has a starting count in the data, and each burst stays active for 3.5 seconds. The fixed-wing airplane starts with 3 flares, the Havoc with 2, the MH-6 and AH-6 family with 2, and the Z20 Lakota with 2. Each press of the countermeasure key uses one flare and then starts a 5 second cooldown before the next press. The "3x bursts" line is item text only; no number in the data is 3 bursts.

Flares are also an inventory item. The vehicle vendor sells them for 750 cash, one per purchase. A vehicle's flare count follows its inventory: buying or being given the item adds that many flares, and taking the item out removes them. What removes the item when you press the countermeasure key was not traced. Smoke charges follow the vehicle inventory in the same way (see the table notes below).

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
| [L2A6](l2a6.md) | Smoke | Not stated | Smoke screen active for 16 s, usable again after 90 s |
| [Flakpanzer Gepard](flakpanzer-gepard.md) | Smoke | 1 charge | Smoke screen active for 16 s, usable again after 90 s |
| [T-72B3](t-72b3.md) | Smoke | 1 charge | Smoke screen active for 16 s, usable again after 90 s |
| [M113 APC SV](m113-apc-sv.md) | Smoke | 255 charges | Smoke screen active for 16 s, usable again after 90 s |

The Flakpanzer Gepard, the T-72B3 and the M113 APC SV have a smoke countermeasure in their game systems data, like the L2A6 (one charge each on the Gepard and T-72B3, 255 on the M113). The charge counts are the starting values in the data. Smoke charges follow the vehicle inventory in the same way as flares: the smoke item must be added to the vehicle. The vehicle vendor sells smoke for 750 cash, one charge per purchase, the same as flares. The SPH-2 variant, the Kodiak, Humvee, Dune Buggy, Bobcat, Ural and Wolf-110 have none.

## Tips that follow from the numbers

- Flares are the only countermeasure for the helicopter and airplane group. The client code read has no flare check on the lock, so the game files do not show whether they stop a heat-seeking lock. Any such rule would sit elsewhere, and a server-side effect is not ruled out.
- A smoke screen is active for 16 seconds, then the vehicle must wait until 90 seconds after the first use before it can use smoke again. Use it as a short cover, and plan the next one around the 90 second wait.
- Because the airplane's flares are a fixed count of 3, use them when they matter most rather than as a routine.
- Each helicopter starts with 2 flares. Each press uses one and then waits 5 seconds before the next, so plan a flight around that count. The "3 bursts" in the item text is not a count.

## See also

- [Vehicle weapons](vehicle-weapons.md): the guns and launchers mounted on vehicles
- [Vehicle damage](vehicle-damage.md): how hits reach the vehicle
- [Talon 9K-SAM](../building/talon-9k-sam.md): a fixed anti-air emplacement
- [Vehicles](../vehicles.md): the full list of vehicles

## Sources

- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md): countermeasure items, prices and the smoke item
- [Vehicles Reference](../../content/Wardogs_Vehicles_v2.md): the airplane's countermeasure data and input change
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): countermeasure lists per vehicle
- [Smoke grenade effect data](../../content/Wardogs_GameplayCues_v2.md): the smoke screen timing
- [Frontend, Server and Test Data](../../content/Wardogs_DataTables_Frontend_v1.md): the in-game tips on flares and flying low
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md): prices and unlock levels
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): the 5 second flare cooldown, one flare per press and the smoke countermeasure on the Gepard, T-72B3 and M113.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the confirmation that restock and the lock-on effect are still not in the data.
- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the 16 second active window and 90 second cooldown of the vehicle smoke screen, and the lock-on interplay that stays open.
- [Round 36 combat evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-combat.md): starting flare counts, active time and range bands for each flare-carrying vehicle.
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the flare data and the search for a lock-on rule
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the flare cooldown and countermeasure readings
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): the flare and smoke inventory handlers and the flare vendor row
- [Round 46 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-b.md): wiki update notes for gear order, the Drill Rig zone speed, the lock and flare search, rocket guidance and placement rewards
