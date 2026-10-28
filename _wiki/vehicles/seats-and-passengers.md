---
title: "Seats and passengers"
parent: "Vehicles"
group: "Reference"
description: "How many seats each Wardogs vehicle has, what the driver, pilot, gunner and passenger seats do, how seated players are protected from gunfire on helicopters and how Season 2 changed that, and how to get in and out."
---

# Seats and passengers

| Seats and passengers | |
|---|---|
| **General** | |
| Type | Mechanic |
| Applies to | Every player vehicle |
| Seat roles | Driver or pilot, gunner, active passenger, passive passenger |
| Seat switching | F1 to F12 by default, not instant |
| **Protection** | |
| Seated protection | Helicopters and the Humvee family, in the data |
| Season 2 change | Little Bird family halved, Z20 Lakota added |
{: .wiki-infobox }

Every vehicle has a set of seats, and each seat has a role. The driver or pilot steers and flies. A gunner works a mounted weapon. Passengers ride along. Seated players also take a reduced share of gunfire damage on some vehicles, set by the seat-protection rules.

## Overview

The seat count on each vehicle's stats sheet is the number listed for it. The seat setups sometimes differ in number, which the tables below note. A vehicle with a mounted gun has a gunner seat for that gun.

## How it works

### Seat roles

Seats have four named roles. Every seat is one of them:

- **Driver or pilot.** Steers the vehicle or flies it. The in-game tip says the driver or pilot navigates the battlefield.
- **Gunner.** Works a mounted weapon. The in-game tip says gunners track targets.
- **Active passenger.** A passenger seat listed as active.
- **Passive passenger.** A passenger seat listed as passive, as used on the M113 APC SV.

Only these names are given. Only the M113 APC SV's nine rear seats are passive passengers; every other passenger seat is active. The two roles differ only in their input and animation, and the passive seats use a different pose.

### Getting in, switching and leaving

- **Enter.** Approach the vehicle and use the interaction prompt for Enter Vehicle.
- **Switch seats.** Seats are chosen with F1 to F12 by default. The in-game tip says switching is not instant and takes a moment.
- **Exit.** Open the interaction menu and press and hold the Exit Vehicle option. Leaving a moving vehicle can hurt you: the damage depends on the speed in km/h when you leave, and is applied on landing. There is no damage at 40 km/h or below, 40 at 50 km/h, 85 at 60 km/h and 100 at 75 km/h and above, with a straight line between those points. The minimum speed for damage is not in the exported data.
- **Unlock.** Purchased vehicles start locked. The owner can unlock them for a squad or for everyone, and teammates cannot enter until they are unlocked.

Ejecting a player from a vehicle is not described.

### Seat protection

Seats set a reduction for seated players against two main groups of arms: small and medium arms, and high-calibre arms. A value of -25 means the seated player takes 75% of the damage, which is 25% protection. A value of -90 means the player takes 10% of the damage.

Seat protection is listed only for these vehicles:

| Vehicle group | Small and medium arms | High-calibre arms | Season 2 |
|---|---|---|---|
| Little Bird family ([MH-6](mh-6.md), [AH-6M [Miniguns]](ah-6m-miniguns.md), [AH-6R [Rockets]](ah-6r-rockets.md)) | -50% in Season 1, -25% in Season 2 | -20% in Season 1, -15% in Season 2 | Halved |
| Venom helicopter | -50% in Season 1, -25% in Season 2 | -20% in Season 1, -15% in Season 2 | Halved |
| [Z20 Lakota](z20-lakota.md) and [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md) | None in Season 1, -25% in Season 2 | None in Season 1, -15% in Season 2 | Added |
| [Havoc](havoc.md) | -90% | -50%, plus -60% in a third group the data labels only as Special | Unchanged |
| Humvee family ([Humvee](humvee.md), [Minigun](humvee-minigun.md), [M249](humvee-m249.md)) | -70% | -40% | Unchanged |

The Season 2 values are the ones shown now. The Season 2 notes say the Havoc and Humvee rows did not change. No seat protection is listed for the other vehicles, including the Kodiak, Ural, Wolf-110, Bobcat, Dune Buggy, M113, the tanks and the airplane.

### Season 2 changes

- The Little Bird family's seat protection was halved: 50% to 25% against small and medium arms, and 20% to 15% against high-calibre arms.
- The Z20 Lakota gained a seat rule of 25% against small and medium arms and 15% against high-calibre arms.
- The Havoc and Humvee rules did not change.

### Parachutes and jumping

The Basic and Sport parachutes are single-use items that a player deploys by hand after a long fall. The data gives a fall of 400 (unit not stated) before a parachute can open. The vehicle data gives no parachute to any aircraft: the parachute belongs to the on-foot character, so a helicopter or the airplane has none. Opening a parachute needs the parachute item in your inventory, a parachute that is not already open, and enough clear space below you while you fall. You can cut a parachute only while it is open. See the [Parachutes](../equipment/parachutes.md) article.

## Numbers

Seat counts and roles for every drivable vehicle. Sort by seats with the header.

| Vehicle | Seats | Roles (as the data gives them) |
|---|---:|---|
| [Havoc](havoc.md) | 2 | Pilot and gunner |
| [MH-6](mh-6.md) | 6 | Pilot and five passenger seats, four of them outside the cabin |
| [AH-6M [Miniguns]](ah-6m-miniguns.md) | 2 | Driver and one active passenger |
| [AH-6R [Rockets]](ah-6r-rockets.md) | 2 | Driver and one active passenger |
| [Z20 Lakota](z20-lakota.md) | 13 | Pilot and passengers, 11 passengers in the shop text |
| [Z20 Lakota [Miniguns]](z20-lakota-miniguns.md) | 13 | Pilot, two gunners (one per minigun) and passengers |
| [Fixed-wing airplane](fixed-wing-airplane.md) | 2 | Driver and one passenger |
| [SPH-2](sph-2.md) | 3 | Driver and gunner, 2 seat setups |
| [L2A6](l2a6.md) | 3 | Two hull seats and a turret gunner |
| [Flakpanzer Gepard](flakpanzer-gepard.md) | 2 | Driver and gunner |
| [T-72B3](t-72b3.md) | 3 | Two hull seats (driver and mounted machine gun) and a turret gunner |
| [M113 APC SV](m113-apc-sv.md) | 10 | Driver and nine passive passengers |
| [Bobcat](bobcat.md) | 2 | Driver and passenger |
| [Kodiak](kodiak.md) | 4 | Driver and three active passengers |
| [Kodiak [Pickup]](kodiak-pickup.md) | 6 | Driver, three inside passengers and two in the bed |
| [Kodiak [M249]](kodiak-m249.md) | 5 | Driver, passengers and the ring turret |
| [Humvee](humvee.md) | 4 | Driver and three active passengers |
| [Humvee [Minigun]](humvee-minigun.md) | 5 | Driver, one gunner at the minigun and three passengers, 4 on one stats sheet |
| [Humvee [M249]](humvee-m249.md) | 5 | Driver, passengers and the ring turret |
| [Dune Buggy](dune-buggy.md) | 3 | Driver and two passengers |
| [Ural](ural.md) | 3 | Driver and two passengers |
| [Ural Defender](ural-defender.md) | 3 | Driver and two passengers |
| [Ural Defender [M249]](ural-defender-m249.md) | 3 | Driver, passengers and the M249 mount, 5 seat setups in the seat data |
| [Wolf-110](wolf-110.md) | 4 | Driver and three active passengers |
| [Wolf-110 [M2 Browning]](wolf-110-m2-browning.md) | 5 | Driver, passengers and the M2 Browning ring turret |

Some vehicles have more seat setups in the seat data than seats on the stats sheet. The Ural Defender [M249] and Humvee [Minigun] are the clearest remaining cases, so their counts are shown as the data gives them. The Pickup's six seats are now resolved: the driver, three passengers inside and two passengers in the bed.

## Tips that follow from the numbers

- On a Little Bird, a seated player takes 75% of small and medium arms damage in Season 2. In Season 1 the seated player took 50%.
- On a Havoc, a seated player takes 10% of small and medium arms damage. That is the strongest seat protection.
- The Z20 Lakota gets seat protection for the first time in Season 2, with 25% against small and medium arms.
- A vehicle with no seat protection listed, such as the Kodiak or the Ural, has no seat reduction.
- The in-game tip says the passenger list shows who has a parachute.
- The Havoc, M113 APC SV, Flakpanzer Gepard, SPH-2, L2A6 and T-72B3 are flagged as seating players of one faction only. No other vehicle sets that flag. With it set, the enter check only lets a player in when the vehicle belongs to the player's faction or is neutral, and every player already seated must match the vehicle's faction.

## See also

- [Vehicle damage](vehicle-damage.md): how hits reach the vehicle and its occupants
- [Vehicle weapons](vehicle-weapons.md): the guns that gunner seats use
- [Repair and vehicle parts](repair-and-vehicle-parts.md): what happens to the vehicle while seated players are inside
- [Vehicles](../vehicles.md): the full list of vehicles

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the rules for opening and cutting a parachute
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): seat counts per stats sheet
- [Vehicles Game Feature](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md): seat setups and roles
- [Vehicle Parts and Handling](../../game-features/Wardogs_VehicleHandling_v1.md): seat names
- [Vehicle Config Fields](../../game-features/Wardogs_VehicleConfigFields_v1.md): the same-faction-only occupant flag, abandoned-vehicle lifetime and ramming settings per vehicle
- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): the seat protection table and how it applies
- [Damage Pipeline](../../pipelines/Wardogs_DamagePipeline_v2.md): the seat reduction step
- [Frontend, Server and Test Data](../../content/Wardogs_DataTables_Frontend_v1.md): the in-game vehicle tips
- [Season 2 Changes: Damage and Combat](../../season-2-changes/damage-combat-systems.md)
- [Season 2 Changes: Vehicles](../../season-2-changes/vehicles.md)
- [Round 39 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-vehicles-explosives.md): Seat counts and the aircraft parachute question.
- [Round 40 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md): the same topics, with the round 40 values where they differ.
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
