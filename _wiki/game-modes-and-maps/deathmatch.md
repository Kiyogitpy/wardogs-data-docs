---
title: "Deathmatch"
parent: "Game Modes & Maps"
group: "Game modes"
description: "Team deathmatch: pick one of 20 weapons before each spawn, with health regeneration and a loadout that comes with ammo."
---

# Deathmatch

| Deathmatch | |
|---|---|
| Type | Team deathmatch |
| Teams | Two teams |
| Objective | Kills, not zones |
| Win condition | 75 kills or 30 minutes, whichever comes first |
| Maps | Not named in the data |
| Server browser label | Deathmatch |
| Internal name | Deathmatch (experience) |
{: .wiki-infobox }

Deathmatch is a team-versus-team mode with no zone. Before each spawn, players choose a weapon from a list of 20. Players regenerate health and get ammunition for their chosen weapon.

## Overview

The server browser lists Deathmatch as a mode, but the data gives it no map name. Deathmatch is the only mode in the sources with two factions rather than three.

## Rules and objectives

- **Match flow.** A match starts with the world loading, then a ready-up stage, then play, then the post-match screen. The ready-up stage is named in the data, but the exact trigger that starts the match is not in the sources.
- **Weapon select.** Before each spawn, the player picks one of 20 weapons. The list is:

  AK74, M4, SKS, KH-2002, A-91, GGX 17, M500, AMP-9, SV98, PP-19 Vityaz, Judge, PKM, M249 SAW, MK22, MGL-40, BMR-308, AMR 50, SVD, T-21, Super-45.

  Each entry uses the weapon's normal name and icon.
- **Health.** Players regenerate after 10 s without damage: 5 health per tick, up to full health. The amount comes from the game code; the tick interval of 1 s is derived from the component's setting.
- **Ammunition.** Choosing a weapon gives you that weapon and four magazines. How many rounds start loaded is not in the data.
- **Spawning.** You respawn at the spawn point furthest from all enemies. The choice is made by the game's code, not by a data table.
- **Teams and win condition.** Two teams, Lonestar and Valkyra. Players choose their team; the server places nobody automatically. A team-balance lock can be switched on to refuse a team switch that would leave the target team 2 or more players larger than the smallest team. It is off by default. The mode ends when a side reaches a score limit of 75 kills, or when the 30 minute time limit runs out. How many players each side may have is a server setting. Whether kills are counted per team or per player is not confirmed.

## Rewards

Deathmatch has no mode-specific reward table in the sources. Kill cash applies: a default player kill pays a base of 250 cash, and the per-kill calculator adjusts it for streaks, revenge and friendly fire. See [Cash and Rewards](../progression-and-economy/cash-and-rewards.md).

## See also

- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Challenges](../progression-and-economy/challenges.md)
- [King of the Hill](king-of-the-hill.md), the three-team zone mode
- [Maps](maps.md)

## Sources

- [Deathmatch game feature](../../game-features/Wardogs_GameFeatures_Deathmatch_v2.md)
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Frontend data tables (server browser list)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Season 2 changes: Game Modes & Maps](../../season-2-changes/game-modes-maps.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Mode rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/mode-rules.json)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
- [Round 45 B evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md): wiki update notes and data findings for this article
