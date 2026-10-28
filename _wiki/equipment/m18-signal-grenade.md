---
title: M18 Signal Grenade
parent: "Equipment"
group: "Explosives and throwables"
description: "The six coloured M18 Signal Grenades: each releases a column of coloured smoke and adds a marker to the map."
---

# M18 Signal Grenade

| M18 Signal Grenade | |
|---|---|
| ![M18 Signal Grenade]({{ '/assets/img/icons/utility-3d/T_UI_Icon_Utility_Smoke_Textured_Yellow_512x512.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Tactical or logistics, thrown smoke with a map marker (quick slot) |
| Variants | Six colours: Alert, Hostile, Friendly, Damaged Vehicle, Supply Request, Landing Zone |
| How it is used | Thrown. Releases a column of coloured smoke and adds a marker to the map |
| Fuse | 3 s |
| **Cloud** | |
| Cloud length | 180 s for five colours; 64 s for Friendly |
| Effect on players | None in the data |
| **Availability** | |
| Price, each | 50 cash |
| Shop unlock level | 0 |
| Required items | None |
| Internal name | `ID.Item.SmokeGrenade.Yellow`, `.Red`, `.Blue`, `.Orange`, `.Green`, `.Purple` |
{: .wiki-infobox }

The M18 Signal Grenade releases a column of coloured smoke and adds a marker of the same meaning to the map. There are six colours, and each one has its own shop name and marker. They are cheap, and they are a way to call attention to a point on the map.

## Overview

The six signal grenades are sold for 50 cash each. Four are tactical (Alert, Hostile, Friendly and Damaged Vehicle), and two are logistics (Supply Request and Landing Zone).

| Shop name | Colour | Map marker | Category | Cloud length |
|---|---|---|---|---:|
| M18 Signal Grenade: Alert | Yellow | Alert | Tactical | 180 s |
| M18 Signal Grenade: Hostile | Red | Hostile | Tactical | 180 s |
| M18 Signal Grenade: Friendly | Blue | Friendly | Tactical | 64 s |
| M18 Signal Grenade: Damaged Vehicle | Orange | Damaged vehicle | Tactical | 180 s |
| M18 Signal Grenade: Supply Request | Green | Supply Request | Logistics | 180 s |
| M18 Signal Grenade: Landing Zone | Purple | Landing Zone | Logistics | 180 s |

The shop text says each one "adds a marker to the map". Each colour adds its marker through the deployable map tracker. It is not known who else can see the marker.

## How it works

**Throwing.** The signal grenades use the same two throws as the M18 Smoke Grenade. An overarm throw sends one at 20 m/s (2,000 cm/s). An underarm throw sends one at 12 m/s (1,200 cm/s).

**Fuse.** The smoke starts 3 s after it is thrown.

**Cloud.** The cloud lasts 180 s, except for the Friendly grenade, whose cloud lasts 64 s. Then it fades for 10 s before it is removed. A cloud that is already running when you arrive has lost the time it has already spent. The smoke stops at walls.

**Players in the cloud.** No game effect is applied through the smoke.

## Damage

The signal grenades do no damage. They have no blast and no thrown-contact damage in the game files.

## Season 2 changes

No Season 2 change to the signal grenades, or to their prices, is listed.

## See also

- [Fire, Smoke and Flash](fire-smoke-and-flash.md), the overview of fire, smoke and signal throwables
- [M18 Smoke Grenade](m18-smoke-grenade.md), the plain white and black smoke grenades
- [Molotov](molotov.md)

## Sources

- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): smoke asset durations, colours and throws
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): names, categories, prices and marker text
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
