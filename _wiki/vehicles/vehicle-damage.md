---
title: "Vehicle damage"
parent: "Vehicles"
group: "Reference"
description: "How hits, explosions and part damage work on Wardogs vehicles, and which parts decide whether a vehicle is destroyed."
---

# Vehicle damage

| Vehicle damage | |
|---|---|
| Type | Mechanic |
| Applies to | Every player vehicle |
| Health unit | HP |
{: .wiki-infobox }

Vehicles take damage through the same rule set that infantry use, but the result goes to parts of the vehicle instead of one health bar. A helicopter has main health plus separate health for its engine, fuel tank, rotors and tail. When the main health reaches zero, the vehicle is destroyed.

## How it works

1. **The rules change the damage.** Each hit has a type: a bullet, a cannon shell, a rocket, a grenade or an explosion. A rule's percentage multiplies the damage. A rule of -95% leaves 5% of the damage, and +400% gives five times the damage. Several rules can match one hit, and they multiply. A rifle round, for example, has the general bullet rule and its own caliber rule, and both apply.
2. **The hit location decides which part takes it.** Each part has its own health. A hit to the engine uses the engine's health, a hit to a wheel uses that wheel's health, and so on.
3. **Some parts pass damage on.** While a part still stands, some parts send a share of their damage to another part. The Flakpanzer Gepard's main body sends 5% of each hit to its fuel tank while it is intact. The L2A6's hull has a tougher zone that sends 40% of its damage to the main health while the zone stands. Once that zone is destroyed, the remainder goes to the main health.
4. **Losing a part does not always end the fight.** When a non-main part runs out, the game marks it destroyed and the vehicle keeps going. Parts also have threshold triggers at fixed percentages of their health. The data lists those triggers, such as fuel leaks on the airplane, but does not decode every effect.
5. **The main health decides the outcome.** At zero the vehicle is destroyed.
6. **Explosions count differently.** A blast is treated as an explosion, not as a direct hit, so it meets its own rules. Rocket and grenade rules often have a separate line for the inner radius, and those lines are much larger on many vehicles. One explosion also counts once per part. If several contacts land on the same part, only the first counts.
7. **Some rules add instead of multiply.** A few rules add a fixed amount, and the order in which rules apply matters for them. Damage never drops below zero.

## Numbers

The table gives the share of rifle damage (5.56 mm, full power, direct hit to the hull) that gets through. It is worked out from each vehicle's rules.

| Vehicle type | Rifle damage taken (derived) |
|---|---|
| Tanks (SPH-2, L2A6, Flakpanzer Gepard, T-72B3) | 0% |
| M113 APC SV | 0% on hull and tracks |
| Helicopters | 5% to 7.5% |
| Trucks and SUVs | 2.5% to 5% |
| Bobcat | 7.5% |
| Dune Buggy | 10% |

For destruction counts, the wiki derives hit counts by simulating full-power, point-blank hits on the main health of each vehicle from the damage rules (derived, not measured in game). The Havoc takes about 1,143 hits of 5.56 mm rifle fire to the hull, or 643 hits through its left front wheel, which is the faster route. Each vehicle article has its own table.

Some rules are large. On the Havoc, a rocket that bursts within the inner radius is multiplied by five. On the Humvee, bullets to the fuel tank get an extra 400% on top of the base rule.

## Tips that follow from the numbers

- Tanks do not take rifle fire. Use rockets, explosives or cannon rounds against them.
- Against trucks and SUVs, rifle fire does best on the fuel tank and wheels. The Humvee's fuel tank takes an extra 400% from bullets, and the Humvee [Minigun]'s wheels take an extra 800%.
- On helicopters the tail and rotor parts are the weak points. The Z20 Lakota goes down through its tail rotor in 429 rifle hits, against 858 hits to the body.
- A rocket that bursts close to a helicopter does far more damage than a direct hit on most helicopters, so a near miss can matter.
- One explosion counts once per part, so spreading a blast across several parts on one vehicle does not multiply the hits on any one part.

## See also

- [Vehicles](../vehicles.md)
- [Havoc](havoc.md) and [Z20 Lakota](z20-lakota.md), as examples of helicopter damage
- [Humvee](humvee.md), as an example of a truck with fuel-tank and wheel weak points
- [L2A6](l2a6.md), as an example of a tank with a tougher hull zone
- [Grenades and Explosives](../equipment/grenades-and-explosives.md)
- [Weapons](../weapons.md)

## Sources

- [Vehicle Damage Pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [All-Vehicle Stat & Damage Sheets](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md)
- [Vehicles (feature)](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Vehicle parts and handling](../../game-features/Wardogs_VehicleHandling_v1.md)
