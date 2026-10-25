---
title: "Season 1 Cosmetics"
parent: "Progression & Economy"
group: "Cosmetics"
description: "Every Season 1 cosmetic: three skin sets and three emotes, their Gold Bar prices, and what the data says about how they were earned."
---

# Season 1 Cosmetics

| Season 1 Cosmetics | |
|---|---|
| Skin sets | Black and Gold (1 row), Digital Wood (4 rows), Two-Tone Desert (12 rows) |
| Emotes | 3 |
| Priced | 19 of 20 rows on the Gold Market, 5 to 15 Gold Bars each |
| Reward track | None in the data. The season schedule is a server value |
| Currency | Gold Bars, sold on the Gold Market |
| Internal name | Season 1 cosmetic tables and the Season 1 season definition table (`DT_Cosmetics_Season01_Skins`, `DT_Cosmetics_Season01_Emotes`, `DT_SeasonDefinitions`) |
{: .wiki-infobox }

Season 1 added three skin sets and three emotes. Every Season 1 cosmetic that has a price is sold on the Gold Market. The data does not say when a Season 1 cosmetic could be obtained, because there is no season reward track and the season schedule is a server value.

## Overview

The list below is the full Season 1 cosmetic set from the data. Each row is one item, vehicle or emote in one set. Prices come from the Gold Market table. The three faction logos and the bobbleheads are not in the Season 1 cosmetic table, so they are covered on [Weapon Skins](weapon-skins.md) and [Vehicle Skins](vehicle-skins.md).

## Season 1 list

| Cosmetic | Type | Skin set | Price (Gold Bars) | How it was earned |
|---|---|---|---|---|
| AK74 | Weapon skin | Black and Gold | Not sold | No Gold Market listing and no price in the data |
| GGX 17 | Weapon skin | Digital Wood | 5 | Gold Market |
| M4 | Weapon skin | Digital Wood | 10 | Gold Market |
| SV98 | Weapon skin | Digital Wood | 10 | Gold Market |
| Sport parachute | Parachute skin | Digital Wood | 15 | Gold Market |
| A-91 | Weapon skin | Two-Tone Desert | 5 | Gold Market |
| AMP-9 | Weapon skin | Two-Tone Desert | 10 | Gold Market |
| AMR 50 | Weapon skin | Two-Tone Desert | 15 | Gold Market |
| Bobcat | Vehicle skin | Two-Tone Desert | 5 | Gold Market |
| Bushmaster M17S | Weapon skin | Two-Tone Desert | 5 | Gold Market |
| Dune Buggy | Vehicle skin | Two-Tone Desert | 10 | Gold Market |
| Humvee | Vehicle skin | Two-Tone Desert | 10 | Gold Market |
| KH-2002 | Weapon skin | Two-Tone Desert | 5 | Gold Market |
| M249 SAW | Weapon skin | Two-Tone Desert | 15 | Gold Market |
| M4 | Weapon skin | Two-Tone Desert | 10 | Gold Market |
| M500 | Weapon skin | Two-Tone Desert | 10 | Gold Market |
| MH-6 | Vehicle skin | Two-Tone Desert | 15 | Gold Market |
| Rock Paper Scissors | Emote | No set | 5 | Gold Market |
| Middle Finger | Emote | No set | 5 | Gold Market |
| Shh | Emote | No set | 5 | Gold Market |

The 19 Gold Market rows are worth 170 Gold Bars in total: 16 skins worth 155, and 3 emotes worth 15.

## How they were earned

- **Gold Market.** This is the only purchase route the data shows. Gold Bars are covered in [Currencies](currencies.md).
- **No reward track.** The client's season definition has a current season number of 1 and an empty list of season levels. The season's dates and names come from the server. No level, date or achievement unlocks a Season 1 cosmetic in the data.
- **AK74 Black and Gold.** This is the one Season 1 weapon skin with no Gold Market row. The data gives it no price, so it can only come from a server grant, which the client data does not show.

## Season 2 changes

Season 1 rows are unchanged in Season 2, and none was removed. Season 2 adds a Little Bird (MH-6) row to the Black and Gold set and a Havoc row to Two-Tone Desert. It also gives the sets look settings for more weapons, which are not sold as rows. It also added the Chocolate Chip set. See [Weapon Skins](weapon-skins.md) and [Vehicle Skins](vehicle-skins.md).

## See also

- [Cosmetics](cosmetics.md)
- [Weapon Skins](weapon-skins.md)
- [Vehicle Skins](vehicle-skins.md)
- [Emotes](emotes.md)
- [Currencies](currencies.md)

## Sources

- [Season 1 cosmetic unlocks](../../content/Wardogs_Season01_CosmeticUnlocks_v1.md)
- [Skins (feature)](../../game-features/Wardogs_GameFeatures_Skins_v2.md)
- [Emotes (feature)](../../game-features/Wardogs_GameFeatures_Emotes_v2.md)
- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the Gold Market prices
- [Data tables: Economy and Rewards](../../content/Wardogs_DataTables_Economy_v1.md), the Gold Market table
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 42 economy and buildables evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): no price for cosmetics not on the market (P19)
