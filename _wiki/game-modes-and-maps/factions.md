---
title: "Factions"
parent: "Game Modes & Maps"
group: "World"
description: "The three factions in the game data, Lonestar, Valkyra and Manticore, and what each one changes: vehicle versions, logos, the Forward Operating Base, and the Season 2 end-of-match bonus."
---

# Factions

| Factions | |
|---|---|
| **Overview** | |
| Factions | 3: Lonestar, Valkyra and Manticore |
| Used in | King of the Hill, Shooting Range, PvE Scenarios and Hot Potato (Deathmatch has two) |
| Faction versions | M113 APC SV (three), spawn vehicles, bobbleheads, supply crates |
| **Rewards** | |
| Season 2 end-of-match bonus | 10,000 cash for Lonestar only |
| Placement bonus | Same for every faction |
| **Internal name** | Meta.Alignment.Faction.Alpha, Bravo, Charlie and Default |
{: .wiki-infobox }

Wardogs has three factions: Lonestar, Valkyra and Manticore. A match sets up its teams from these factions, and the factions decide which vehicle versions, cosmetics and rewards a player sees. The game data gives the names, a few concrete differences and the rewards. The data gives each faction a colour and a signature rifle. What each faction stands for is not in the data.

## Overview

The data ties each faction to its own Forward Operating Base model, its end-of-match bonus and its Hot Potato item.

| Faction | Faction logo (cosmetic) | Season 2 end-of-match bonus |
|---|---|---|
| Lonestar | [Bushmaster M17S](../weapons/bushmaster-m17s.md) | 10,000 cash |
| Valkyra | [A-91](../weapons/a-91.md) | None |
| Manticore (also the default faction) | [KH-2002](../weapons/kh-2002.md) | None |

The default faction in the data uses the Manticore Forward Operating Base, so Manticore is the fallback when no faction is set.

## What differs between factions

- **Vehicles.** The [M113 APC SV](../vehicles/m113-apc-sv.md) comes in three faction versions, Lonestar, Manticore and Valkyra. They share the same numbers. The data also lists a spawn vehicle for each faction in the vehicle rules.
- **Forward Operating Base.** Each faction has its own Forward Operating Base model, and the data gives each one its own placement. The health and cost numbers are shared, so the data shows no faction-specific numbers for it. See the [Forward Operating Base](../building/forward-operating-base.md) page.
- **Supply crates.** Free supply crates have a skin for each faction, chosen by the faction. The skins differ in appearance, and the data does not show any difference in contents.
- **Bobbleheads.** Vehicle bobbleheads have a version for each faction, chosen by the faction selectors. See [Cosmetics](../progression-and-economy/cosmetics.md).
- **Faction logos.** Each faction has a logo cosmetic on one weapon, listed in the table above. The data gives these no price.
- **Hot Potato.** The mode has one item for each faction. See [Hot Potato](hot-potato.md).
- **AI in PvE missions.** The AI configurations in the data are for Lonestar and Manticore. The Lonestar squad has a rifleman and a sniper. The Manticore squad has a rifleman, a machine gunner and a marksman. The data lists no AI configuration for Valkyra. In the VIP Escort mission the player's faction is Valkyra. See [PvE Scenarios](pve-scenarios.md).
- **Voice-over.** Dialogue sets are tagged by faction. The data has Lonestar equipment and garage dialogue, and Valkyra vehicle dialogue. What the lines say is not in the sources.

## Rewards

- **Placement bonus.** At the end of a match, every faction is ranked and paid the same placement bonus: 200 cash for first, 150 for second and 100 for third, with the same XP multipliers for all. See [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).
- **Season 2 bonus.** Lonestar gets a flat 10,000 cash at the end of a match. Valkyra and Manticore get nothing from this row.

## How factions are assigned

- King of the Hill and the Shooting Range use three factions. The data says three teams are set up at the start of a match.
- Deathmatch has two factions, the only mode in the sources with two.
- Sniper Showdown is free-for-all. The game prepares a pool of 100 single-player factions and puts each joining player on the one with the fewest members.

## What is not known

- **What each faction is.** The data gives each faction a name, a colour and a logo: Lonestar is blue, Valkyra red and Manticore green. The game files hold no backstory or roleplay identity for them.
- **Signature rifles.** Each faction's signature rifle is free for that faction (the pairing is in the economy settings; the check that matches the buyer's faction was not decoded, so the rule is read from the setting's name): Lonestar has the [Bushmaster M17S](../weapons/bushmaster-m17s.md), Valkyra the [A-91](../weapons/a-91.md) and Manticore the [KH-2002](../weapons/kh-2002.md). The economy settings set the price of each to 0% for its own faction (see [Shops](../progression-and-economy/shops.md)). The data gives no separate price for the other factions. The data lists no other weapon or gear differences, which is not proof that none exist.
- **Joining a faction.** In Deathmatch, players choose between Lonestar and Valkyra themselves; the server places nobody automatically. Team-size locking is off by default. When it is on, a switch is refused if the target team would end up 2 or more players larger than the smallest team. King of the Hill creates three factions.

## See also

- [King of the Hill](king-of-the-hill.md) and [Control Zone](control-zone.md): modes with three factions
- [Cosmetics](../progression-and-economy/cosmetics.md): faction logos, bobbleheads and skins
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md): placement and Season 2 bonus values

## Sources

- [Rewards and progression data](../../Wardogs_Rewards_and_Progression_v2.md), section 10
- [Buildables](../../game-features/Wardogs_Buildables_v1.md), section 8
- [Skins](../../game-features/Wardogs_GameFeatures_Skins_v2.md)
- [Vehicles](../../game-features/Wardogs_GameFeatures_Vehicles_v2.md)
- [Demolition reference](../../content/Wardogs_Demolition_v2.md), vehicle rules
- [Game features: AI](../../game-features/Wardogs_GameFeatures_AI_v2.md)
- [Gameplay tags](../../content/Wardogs_GameplayTags_v1.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
- [Round 44 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round44-econ-buildables.md)
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
