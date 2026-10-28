---
title: "Wagers"
parent: "Progression & Economy"
group: "Challenges"
description: "The four wager actions, how many of each a player can take on, the odds, the 50 conditions and the payout limits. Settlement is on the server."
---

# Wagers

| Wagers | |
|---|---|
| **General** | |
| Kind | Goals taken on with a stake |
| Actions | 4: kills, player deliveries, revives and destroyed occupied vehicles |
| Count per wager | Kills 1 to 25, deliveries 1 to 20, revives 1 to 50, vehicles 1 to 20 |
| **Stakes and payout** | |
| Stake | 2,500 to 100,000 cash |
| Payout cap | 5,000,000 cash |
| Cooldown | 24 hours (86,400 s) per action |
| Conditions | 50 optional conditions, each with odds |
| Settlement | On the server. The payout formula is not in the data |
| Internal name | DT_WagerActions, DT_WagerPricing, DT_WagerConditions, DT_WagerObjectiveCatalog |
{: .wiki-infobox }

A wager is a goal a player takes on with a stake of cash. The player picks how many of an action they will do, adds any conditions they want, and the odds rise with the difficulty. If the goal is reached the stake is paid out at the odds. The game gives the counts, odds, limits and conditions. It does not give the formula the server uses to settle a wager.

## Overview

| Wager | Goal | Count (default) |
|---|---|---|
| Get Kills | Get kills of enemy players inside the control zone | 1 to 25 (1) |
| Dropoff People | Deliver people to the control zone | 1 to 20 (1) |
| Revive Teammates | Revive teammates inside the control zone | 1 to 50 (5) |
| Destroy Occupied Vehicles | Destroy vehicles that an enemy is driving and that an enemy bought | 1 to 20 (1) |

## How it works

- **Not automatic.** The game marks wager challenges as not auto-activated, so a player takes one on by choice.
- **Count.** The player chooses the count on the slip. Each action has a range and a default, as in the table above.
- **Rules.** Each action has rules for what counts. Kills must be inside the control zone and against enemy players, and a player an enemy revived does not count. Revives must be inside the control zone and on teammates, and a player downed by a teammate or by themselves does not count. Deliveries do not count if a spawn vehicle carried the passenger, and count once the passenger survives the drop-off. Vehicles count only when an enemy is driving them and an enemy bought them. Repeats on the same player do not count for kills or revives.
- **Cooldown.** Each action has a cooldown of 86,400 seconds (24 hours). The game does not say whether the cooldown is per player, per wager or per match.
- **Deaths.** The slip allows a number of deaths for a wager, and each allowance carries its own small odds. The game lists four values (1.009, 1.003, 1.002 and 1.001). Which value goes with which number of deaths is inferred from the slip text, not stated.
- **Several objectives.** A slip can hold more than one objective. Each objective after the first adds 0.25 to the multi bonus. The slip text reads 1 + (objectives - 1) x 0.25, so two objectives give 1.25 and three give 1.5. The server settles the payout, so how this bonus combines with the odds is not known.
- **Unlock.** The Wardog level that unlocks wagers is a server rule, so it is not in the game.

## Odds

Odds rise by a small step with each count. The table gives the lowest and highest odds for each action. The full lists for every count are in [economy data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

| Action | Count | Odds at the lowest count | Odds at the highest count |
|---|---|---|---|
| Kills | 1 to 25 | 1.001 (1 to 3 kills) | 1.2004 (25 kills) |
| Player deliveries | 1 to 20 | 1.001 (1 to 5) | 1.0771 (20) |
| Revives | 1 to 50 | 1.001 (1 to 5) | 1.2498 (50) |
| Vehicles destroyed | 1 to 20 | 1.001 (1 to 3) | 1.1479 (20) |

## Conditions

A condition is an extra rule that a wager can carry. Each one multiplies the odds of the wager it is added to. The game lists 50 conditions. The table is sortable. The "Applies to" column shows the action a condition is tied to, or "Any action" when the game does not tie it to one.

Odds for the conditions run from 1.005 (5 tapes in the vehicle) to 10.0 (Deathwish). Time limit is 4.0, no vehicles is 3.0 and no resupply is 2.0. The server settles the payout, so the game does not say whether two conditions on one wager multiply together.

| Condition | Type | Applies to | Odds |
|---|---|---|---:|
| Deathwish | Rules | Any action | 10.0 |
| In control zone | Place | Any action | 1.15 |
| In hot zone | Place | Any action | 1.1 |
| No resupply | Loadout | Any action | 2.0 |
| No spend | Rules | Any action | 1.1 |
| No vehicles | Loadout | Any action | 3.0 |
| Time limit | Rules | Any action | 4.0 |
| While under 50 HP | Health | Any action | 1.2 |
| While wearing no armor | Loadout | Any action | 1.15 |
| With a $20k loadout | Loadout | Any action | 1.05 |
| With no bandages | Loadout | Any action | 1.15 |
| Using AP ammo | Ammo | Kills | 1.1 |
| Using HP ammo | Ammo | Kills | 1.15 |
| With AK74 | Weapon | Kills | 1.01 |
| With Judge | Weapon | Kills | 1.3 |
| With Scout Rifle TD | Weapon | Kills | 1.05 |
| With grenade | Utility | Kills | 1.45 |
| With headshot | Manner | Kills | 1.2 |
| With large hammer | Weapon | Kills | 1.3 |
| With light drill | Weapon | Kills | 1.3 |
| With only one magazine | Loadout | Kills | 1.2 |
| With punch | Weapon | Kills | 1.4 |
| With small hammer | Weapon | Kills | 1.3 |
| With vehicle impact | Weapon | Kills | 1.075 |
| In Blackhawk | Vehicle | Player delivery | 1.15 |
| In Bobcat | Vehicle | Player delivery | 1.2 |
| In Dune Buggy | Vehicle | Player delivery | 1.025 |
| In Kodiak | Vehicle | Player delivery | 1.15 |
| In Little Bird | Vehicle | Player delivery | 1.2 |
| In Ural | Vehicle | Player delivery | 1.01 |
| In air vehicle | Vehicle | Player delivery | 1.1 |
| In ground vehicle | Vehicle | Player delivery | 1.05 |
| To control zone | Place | Player delivery | 1.15 |
| To hot zone | Place | Player delivery | 1.25 |
| With 5 tapes in the vehicle | Vehicle | Player delivery | 1.005 |
| 50 m from teammates | Place | Revives | 1.1 |
| With defibrillator | Utility | Revives | 1.025 |
| With magic hands | Utility | Revives | 1.1 |
| With medkit | Utility | Revives | 1.05 |
| With no weapons | Loadout | Revives | 1.15 |
| With resuscitator | Utility | Revives | 1.1 |
| Artillery vehicle destroyed | Target vehicle | Vehicles destroyed | 1.4 |
| Blackhawk destroyed | Target vehicle | Vehicles destroyed | 1.5 |
| Havoc destroyed | Target vehicle | Vehicles destroyed | 1.7 |
| Little Bird with rockets destroyed | Target vehicle | Vehicles destroyed | 1.45 |
| Tank destroyed | Target vehicle | Vehicles destroyed | 1.6 |
| While moving above 50 kph | Manner | Vehicles destroyed | 1.1 |
| With Havoc | Weapon | Vehicles destroyed | 1.15 |
| With Little Bird rockets | Weapon | Vehicles destroyed | 1.15 |
| With tank | Weapon | Vehicles destroyed | 1.1 |

## Prebuilt objectives

The game holds a catalogue of prebuilt objectives. Five are public, with a fixed count and odds. Nine more carry a flag, and each has a condition set and higher odds. Whether the flagged objectives are offered to every player is not stated. Three further catalogue entries are test rows and are left out.

### Public objectives

| Objective | Action | Count | Odds | Conditions |
|---|---|---:|---:|---|
| Kills x3 | Kills | 3 | 1.001 | None |
| Kills x2 with headshot | Kills | 2 | 1.2012 | With headshot |
| Revives x2 | Revives | 2 | 1.001 | None |
| Player delivery x3 | Player delivery | 3 | 1.001 | None |
| Vehicle destroyed x1 | Vehicles destroyed | 1 | 1.001 | None |

### Flagged objectives

| Objective | Action | Count | Odds | Conditions |
|---|---|---:|---:|---|
| Hammertime, tier 1 | Kills | 10 | 1.5 | With small hammer, In hot zone |
| Hammertime, tier 2 | Kills | 20 | 1.64 | With small hammer, In hot zone |
| Hammertime, tier 3 | Kills | 25 | 1.72 | With large hammer, In hot zone |
| Medic Marathon, tier 1 | Revives | 30 | 1.37 | With magic hands, In hot zone |
| Medic Marathon, tier 2 | Revives | 40 | 1.44 | With magic hands, In hot zone |
| Medic Marathon, tier 3 | Revives | 50 | 1.51 | With magic hands, In hot zone |
| All Driller, No Filler, tier 1 | Kills | 15 | 1.57 | With light drill, In hot zone |
| All Driller, No Filler, tier 2 | Kills | 20 | 1.64 | With light drill, In hot zone |
| All Driller, No Filler, tier 3 | Kills | 25 | 1.72 | With light drill, In hot zone |

## Payout and settlement

- **Stake and odds.** The slip shows a total odds figure and a return. By the slip's own labels the return is the stake times the total odds (the exact formula is not read from the game), and the slip labels it "(capped)" when the cap applies. The cap is 5,000,000 cash.
- **Settlement.** Settlement runs on the server. The game has the odds, the cap and the stake limits, but not the formula that decides whether a wager pays and how much.
- **Decided by the server.** How deaths, leaving a match or completing only part of a slip affect a payout is settled on the server, so it is not in the game.

## Rewards

The game lists no XP or item reward for the four wager challenges. The cash payout is the return described above.

## Season 2 changes

- The wager system was added in the Season 02 update, with seven files under the wager folder: pricing, actions, challenges, conditions, an objective catalogue and two UI tables.
- Four wager challenges were added: passengers delivered, rewarded kills, rewarded revives and rewarded vehicles destroyed.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [Passive Missions](passive-missions.md)
- [Achievements](achievements.md)
- [Currencies](currencies.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- Wager challenge table (JSON)
- Wager pricing table (JSON)
- [Economy data: wagers](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json) (JSON)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
