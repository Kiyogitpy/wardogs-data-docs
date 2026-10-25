---
title: "Cosmetics"
parent: "Progression & Economy"
group: "Unlocks"
description: "Skins, emotes and other cosmetics for Seasons 1 and 2, their Gold Bar prices, and what the data does and does not say about how they are unlocked."
---

# Cosmetics

| Cosmetics | |
|---|---|
| Kinds | Weapon and vehicle skins, emotes, parachute skin, faction logos, bobbleheads, taxi skin |
| Season 1 | Three skin sets (Black and Gold, Digital Wood, Two-Tone Desert) and three emotes |
| Season 2 | Adds a Chocolate Chip set, more skins and a Black and Gold Little Bird skin |
| Currency | Gold Bars, sold on the Gold Market |
| Unlock route | Gold Market purchase, and server grants. There is no season reward track, and the schedule is a server value |
| Internal name | Cosmetic data tables and skin assets |
{: .wiki-infobox }

Cosmetics change how weapons, vehicles, parachutes and emotes look. Skins repaint a weapon, vehicle or parachute with a pattern and colour set. Emotes are actions a player can perform. Most skins and emotes are priced in Gold Bars on the Gold Market.

## Overview

| Area | Items | Priced | Gold Bar range | Read more |
|---|---|---|---|---|
| Weapon skins | 18, plus 3 faction logos | 17 | 5 to 15 | [Weapon Skins](weapon-skins.md) |
| Vehicle skins | 7, including the taxi skin | 6 | 5 to 30 | [Vehicle Skins](vehicle-skins.md) |
| Parachute skin | 1 | 1 | 15 | Below |
| Emotes | 6 | 3 | 5 | [Emotes](emotes.md) |
| Season 1 | 20 | 19 | 5 to 15 | [Season 1 Cosmetics](season-01-cosmetics.md) |
| Gold Market total | 27 entries | 27 | 275 Gold Bars in all | [Currencies](currencies.md) |

The Gold Market sells 27 entries. Weapon and vehicle skins account for most of them. Faction logos, the taxi skin and the bobbleheads are not sold on the Gold Market and have no price in the data.

## How it works

- **Sets.** A skin set has one look, such as Digital Wood, and applies to several items. Two-Tone Desert has 12 Season 1 rows, Digital Wood has 4 and Black and Gold has 1. Season 2 adds rows and a new Chocolate Chip set.
- **Items.** The same weapon can appear in more than one set. The M4 has a Digital Wood skin and a Two-Tone Desert skin.
- **Emotes.** Each emote has a name and an action. Six emote entries exist. Shh, Rock Paper Scissors and Middle Finger have cosmetic rows with prices. Rock, Paper and Scissors have none.
- **Look only.** The data shows the pattern and colour of each set. It does not show how a skin looks on a model.
- **How a player gets one.** The client has two routes: buying it on the Gold Market with Gold Bars, and the backend granting items to a player. Items with no Gold Market row (such as the AK74 Black and Gold skin, the faction logos, the taxi skin and the bobbleheads) can only come from a grant, and the data does not show which grants are made.
- **No reward track.** The data has no battle pass and no season reward track, so no cosmetic is tied to a level. The season schedule is a server value and is not in the client data.

## Parachute skin and character looks

The data has no outfits or character skins. The only cosmetic a character carries is one parachute skin: the Sport parachute in the Digital Wood set, sold on the Gold Market for 15 Gold Bars. The gear shop lists the Sport parachute itself at 700 (see [Shops](shops.md)); the data does not say whether the parachute must be owned before its skin is bought, or how a character cosmetic is equipped in a match.

## Tips that follow from the numbers

- Emotes and several Season 1 skins cost 5 Gold Bars, the lowest listed price. Rock, Paper and Scissors have no price in the data.
- The most expensive listed cosmetic is the Black and Gold Little Bird (MH-6), at 30 Gold Bars. Its Gold Market entry carries an expiry date of 31 December 2026 in the data, with a countdown on the tile. Whether it leaves the market on that date is decided by the server; the game files only store the date.
- Most Season 2 skins cost 10 Gold Bars.
- The AK74 Black and Gold skin is not on the Gold Market, and the game files give it no price.

## Season 2 changes

- The Chocolate Chip set is new, with three weapon skins (M14, Evo-3 Ultra and TCX-SPR) at 10 Gold Bars each.
- The Black and Gold set gains a Little Bird skin for 30 Gold Bars. Two-Tone Desert gains Havoc, Mosin Nagant and Galil skins, and Digital Wood gains an M500 skin, at 10 to 15 Gold Bars each.
- Several existing skin settings change in Season 2, for example the wear threshold on ten Digital Wood settings went from 0.8 to 1.0. The skins themselves are not removed.

## More

- [Weapon Skins](weapon-skins.md): every weapon skin, grouped by weapon, with its price and how it unlocks
- [Vehicle Skins](vehicle-skins.md): every vehicle skin, the taxi skin and the bobbleheads
- [Emotes](emotes.md): all six emotes and their prices
- [Season 1 Cosmetics](season-01-cosmetics.md): the full Season 1 list and how it was earned
- [Currencies](currencies.md): Cash, Gold Bars and Intel, and the Gold Market

## See also

- [Shops](shops.md), where Gold Bar prices are listed alongside other shops
- [Cash and Rewards](cash-and-rewards.md)
- [Currencies](currencies.md)
- [Progression & Economy](../progression-and-economy.md)

## Sources

- [Season 1 cosmetic unlocks](../../content/Wardogs_Season01_CosmeticUnlocks_v1.md)
- [Skins (feature)](../../game-features/Wardogs_GameFeatures_Skins_v2.md)
- [Emotes (feature)](../../game-features/Wardogs_GameFeatures_Emotes_v2.md)
- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Gold Market prices
- [Taxi skins data](../../game-features/Wardogs_GameFeatures_Taxi_SkinsData_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): no Gold Market row and no price for cosmetics not on the market (P19)
