---
title: "Vehicle Skins"
parent: "Progression & Economy"
group: "Cosmetics"
description: "Every vehicle skin, the MH-6 taxi skin and the bobbleheads, with Gold Bar prices and how each is unlocked."
---

# Vehicle Skins

| Vehicle Skins | |
|---|---|
| Skin sets | Two-Tone Desert, Black and Gold, Taxi |
| Vehicle skins | 6 priced rows, plus 1 taxi skin and 4 bobbleheads with no price |
| Currency | Gold Bars, sold on the Gold Market |
| Internal name | Vehicle skin tables and the taxi skin data ([`DT_Cosmetics_Season01_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/DT_Cosmetics_Season01_Skins.json), [`DT_Cosmetics_Season02_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season02_SkinsData/Content/Data/DT_Cosmetics_Season02_Skins.json), [`DT_Cosmetics_Taxi`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Taxi_SkinsData/Content/Data/DT_Cosmetics_Taxi.json), [`DT_Bobblehead_Faction_Cosmetics`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/BobbleHeads/Bobblehead_Faction/Content/Data/DT_Bobblehead_Faction_Cosmetics.json)) |
{: .wiki-infobox }

A vehicle skin repaints a vehicle with a pattern and colour set. Most vehicle skins are bought on the Gold Market for 5 to 30 Gold Bars. The taxi skin and the bobbleheads have no price.

## Overview

The table below lists each vehicle skin sold on the Gold Market, sorted by vehicle. The MH-6 (Little Bird) has three skins, one in each set, so it appears three times.

## Vehicle skins

| Vehicle | Skin set | Season | Price (Gold Bars) | How it unlocks |
|---|---|---|---|---|
| Bobcat | Two-Tone Desert | Season 1 | 5 | Gold Market |
| Dune Buggy | Two-Tone Desert | Season 1 | 10 | Gold Market |
| Havoc | Two-Tone Desert | Season 2 | 15 | Gold Market |
| Humvee | Two-Tone Desert | Season 1 | 10 | Gold Market |
| MH-6 | Black and Gold | Season 2 | 30 | Gold Market (see the note below) |
| MH-6 | Two-Tone Desert | Season 1 | 15 | Gold Market |
| MH-6 | Taxi | Not stated | Not sold | No price |

The Gold Market prices are 6 vehicle skins worth 85 Gold Bars in total.

The MH-6 Black and Gold skin is the most expensive vehicle skin, at 30 Gold Bars. Its Gold Market entry is a single hero tile. It carries an expiry timestamp of 31 December 2026, with the setting for no end time, and its tile shows a countdown. Whether the skin leaves the market on that date is decided by the server; the game only stores the date.

## Taxi skin

The taxi skin is for the MH-6 (Little Bird). It is the only taxi cosmetic. It works by swapping materials on the helicopter rather than changing its shape. The list of material swaps is in the game but is not expanded here. The game gives the taxi skin no price and no Gold Market row, so it is not known how a player gets it.

## Bobbleheads

Bobbleheads are vehicle cosmetics that fit a vehicle slot. The game has four of them. None has a Gold Market price, and it is not known how they are unlocked.

| Bobblehead | Price (Gold Bars) | How it unlocks |
|---|---|---|
| Faction | Not sold | Not known |
| Grenade | Not sold | Not known |
| Helmet | Not sold | Not known |
| A fourth bobblehead | Not sold | Not known (the game gives it no display name) |

The game gives the bobbleheads no vehicle filter, so they are not limited to particular vehicles. Bobbleheads sit on a soft spring with no damping, so they keep swinging after a jolt. This comes from the animation setup and has not been checked in play.

## Cost and unlocking

- **Gold Market.** Every priced vehicle skin is a Gold Market entry, bought with Gold Bars. Gold Bars are covered in [Currencies](currencies.md).
- **Look on other vehicles.** Digital Wood and Chocolate Chip also set how their looks appear on other vehicles, such as the Kodiak, Ural and Humvee variants. The game does not list those as sold skins, and it does not say whether a player can apply them.
- **No level gate.** The game does not tie any vehicle skin to a level, and there is no season reward track. Server grants are the only route outside the Gold Market. See [Season 1 Cosmetics](season-01-cosmetics.md).

## Season 2 changes

- The Havoc attack helicopter gets a Two-Tone Desert skin for 15 Gold Bars.
- The Little Bird (MH-6) gets a Black and Gold skin for 30 Gold Bars.

## See also

- [Weapon Skins](weapon-skins.md)
- [Cosmetics](cosmetics.md)
- [Currencies](currencies.md)
- [MH-6](../vehicles/mh-6.md), [Havoc](../vehicles/havoc.md), [Bobcat](../vehicles/bobcat.md), [Dune Buggy](../vehicles/dune-buggy.md), [Humvee](../vehicles/humvee.md)

## Sources

- [Skins](../../game-features/Wardogs_GameFeatures_Skins_v2.md)
- [Taxi skins data](../../game-features/Wardogs_GameFeatures_Taxi_SkinsData_v2.md)
- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the cosmetic table and the bobblehead slot tables
- [Meta: currency and Gold Market](../../content/Wardogs_Meta_v2.md)
- [Data tables: Economy and Rewards](../../content/Wardogs_DataTables_Economy_v1.md), the Gold Market table
- [Season 1 cosmetic unlocks](../../content/Wardogs_Season01_CosmeticUnlocks_v1.md)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): expiry (P18) and skins with no price or unlock (P19)
