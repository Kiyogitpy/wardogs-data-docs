---
title: "King of the Hill Challenges"
parent: "Progression & Economy"
group: "Challenges"
description: "The 60 King of the Hill event challenges: kills, revives, heals, vehicles, supply crates, tips and zone play, with the base cash and role XP each pays."
---

# King of the Hill Challenges

| King of the Hill Challenges | |
|---|---|
| **General** | |
| Kind | Event rewards, paid each time the event happens |
| Challenges | 60 |
| Auto-activate | 59 of 60 |
| Internal name | DT_Challenges_SessionEvents_KOTH |
{: .wiki-infobox }

The King of the Hill set is the largest challenge category, with 60 rows. Each row is one event, or one assist version of an event, and pays when it happens. Most pay cash and role XP to the player who did the action, and smaller shares to the players who helped.

## Overview

The 60 rows cover player kills, revives, heals, vehicle kills, vehicle sections, supply crates, zone entry, tips, air time and fly-through bonuses, and a few other events. Many rows come in groups: a base event, then a crew, logistic, revive, FOB-supplied or supply crate version.

## How it works

- **No target.** These challenges have no number to reach. The matching rule pays each time its event happens.
- **Assist versions.** An assist row pays a player who helped. A crew row pays the pilot, driver or gunner of a vehicle that took part.
- **Friendly events.** Several rows list a friendly value of 0, so they pay nothing when the event is friendly.
- **Auto-activate.** All rows start automatically except Supply Pallet Dropped.
- **Amounts.** The cash and role XP columns show the base amount of each reward row. These are the shared challenge reward rows that the challenges of every mode use. They differ from the cash tables on [Cash and Rewards](cash-and-rewards.md), which give other bases for the same actions (a default kill 250, a defibrillator revive 1,000, a Bandage heal 400), and the game server, not the files on your PC, decides which set a match pays out. The zone, kill-streak and last-victim terms then multiply the base (see [Cash and Rewards](cash-and-rewards.md)). Smaller amounts in the same rule are assist, owner or friendly shares.
- **No row.** The reward table has no entry for that reward, so the event pays nothing from it.
- **Not in data.** No base amount was found for that reward in the sources, so its amount is not yet known.
- **Duplicate name.** The data has two rows named Vehicle Destroyed Assist Revive Assist. One is the revive assist and the other is the FOB-supplied assist.

## Challenges

| Challenge | What earns it | Cash (base) | Role XP (base) |
|---|---|---|---|
| Player Kill | Award resources to (or take from) a player when they kill another player. | 300 | 250 |
| Player Kill Crew Assist | Award resources to (or take from) a crew player when their pilot/driver/gunner kills another player. | Calculated share of the kill | 100 |
| Player Kill Logistic Assist | Logistic credit for a player kill. | 300 | 250 |
| Player Kill Revive Assist | Revive credit for a player kill. | 300 | 250 |
| Player Kill FOB Supplied Assist | FOB-supplied credit for a player kill. | 300 | 250 |
| Player Kill Supply Crate Assist | Award resources to the player who sold the damage causer. | Not in data | Not in data |
| Player Kill Assist | Award resources to (or take from) a player when they assisted in the death of another player. | 300 | 250 |
| Player Kill Assist Crew Assist | Award resources to (or take from) a crew player when their pilot/driver/gunner assists in the death of another player. | Not in data | Not in data |
| Player Kill Assist Logistic Assist | Logistic credit on a player kill assist. | 300 | 250 |
| Player Kill Assist Revive Assist | Revive credit on a player kill assist. | 300 | 250 |
| Player Kill Assist FOB Supplied Assist | FOB-supplied credit on a player kill assist. | 300 | 250 |
| Player Kill Assist Supply Crate Assist | Award resources to the player who sold the damage causer. | Not in data | Not in data |
| Revive Player | Award resources to a player when they revive another player. | 600 (500 with a Resuscitator) | 250 |
| Revive Player Logistic Assist | Logistic credit for a revive. | 400 | 200 |
| Revive Player Revive Assist | Revive credit for a revive. | 400 | 200 |
| Revive Player Supply Crate Assist | Award resources to the player who sold the revive causer. | Not in data | Not in data |
| Revive Player Contributor | Award resources to a player when they're mid-process of reviving another player. | 400 | 200 |
| Heal Player | Award resources to a player when they heal another player. | 200 with a bandage | 80 |
| Heal Player Logistic Assist | Logistic credit for a heal. | Not in data | 25 |
| Heal Player Revive Assist | Revive credit for a heal. | Not in data | 25 |
| Heal Player Supply Crate Assist | Award resources to the player who sold the heal causer. | Not in data | Not in data |
| Destroy Vehicle | Award resources to a player when they destroy a vehicle. | 250 (Kodiak) to 7,000 (Havoc) | 150 (Kodiak) to 750 (heavy tank) |
| Destroy Vehicle Crew Assist | Award resources to a crew player when their pilot/driver/gunner destroys a vehicle. | Calculated share of the kill | 250 |
| Destroy Vehicle Logistic Assist | Logistic credit for a vehicle destroyed. | 400 | 200 |
| Destroy Vehicle Revive Assist | Revive credit for a vehicle destroyed. | 400 | 200 |
| Destroy Vehicle FOB Supplied Assist | FOB-supplied credit for a vehicle destroyed. | 400 | 200 |
| Destroy Vehicle Supply Crate Assist | Award resources to the player who sold the damage causer. | Not in data | 50 |
| Destroy Vehicle Assist | Award resources to players who assisted in the destruction of a vehicle by damaging it. | Not in data | Not in data |
| Destroy Vehicle Assist Crew Assist | Award resources to crew players whos pilot/driver/gunner assisted in the destruction of a vehicle by damaging it. | Not in data | 250 |
| Vehicle Destroyed Assist Logistic Assist | Logistic credit on a vehicle kill assist. | 400 | 200 |
| Vehicle Destroyed Assist Revive Assist | Revive credit on a vehicle kill assist. | 400 | 200 |
| Vehicle Destroyed Assist Revive Assist | Revive credit on a vehicle kill assist. | 400 | 200 |
| Vehicle Destroyed Assist Supply Crate Assist | Award resources to the player who sold the damage causer. | Not in data | 50 |
| Destroy Vehicle Section | Award resources to a player when they destroy a vehicle section. | 0 (no base amount) | 0 |
| Destroy Vehicle Section Crew Assist | Award resources to a crew player when their pilot/driver/gunner destroys a vehicle section. | Not in data | 125 |
| Destroy Vehicle Section Logistic Assist | Logistic credit for a vehicle section destroyed. | 400 | 200 |
| Destroy Vehicle Section Revive Assist | Revive credit for a vehicle section destroyed. | 400 | 200 |
| Destroy Vehicle Section Supply Crate Assist | Award resources to the player who sold the damage causer. | Not in data | 50 |
| Destroy Vehicle Section Assist | Award resources to players who assisted in the destruction of a vehicle section by damaging it. | Not in data | Not in data |
| Destroy Vehicle Section Assist Crew Assist | Award resources to a crew player when their pilot/driver/gunner assists in destroying a vehicle section. | Not in data | 125 |
| Destroy Vehicle Section Assist Logistic Assist | Logistic credit on a vehicle section assist. | 400 | 200 |
| Destroy Vehicle Section Assist Revive Assist | Revive credit on a vehicle section assist. | 400 | 200 |
| Destroy Vehicle Section Assist Supply Crate Assist | Award resources to the player who sold the damage causer. | Not in data | 50 |
| Zone Entry | Award resources to a player when entering the zone. | No row | No row |
| Destroy Throwable | Award resources or take them when the player destroys a throwable | 100 | 75 |
| Refuel Vehicle | Award resources to a player when they refuel a vehicle. | 15 | 15 |
| Deploy On Vehicle | Award resources when a player is deployed on a vehicle | 50 | No row |
| Deploy a Supply Crate | Award resources when a player deploys a supply crate | 0 | 0 |
| Supply Pallet Dropped | Award resources when a player deploys a supply pallet | 0 | 0 |
| Repair Vehicle | Award resources to a player when they repair another vehicle. | 5 (wrench) to 15 (heavy drill) | 2.5 (wrench) to 10 (heavy drill) |
| Purchase From Supply Crate | Award resources to a player when they purchase from a supply crate. | Not in data | Not in data |
| Destroy a Supply Crate | Award resources when a player destroys a supply crate. | 150 | 150 |
| Deliver Teammate to Zone | Delivering a teammate to the zone. The data gives no description. | 100 | 12.5 |
| Survived Trip | A passenger survives the trip. | 500 | 100 |
| Safe Zone Entered after successful logistics run | Entering the safe zone after a successful logistics run. | 500 | 100 |
| Send & Receive Tip | Remove resources from one player and give it to another when they tip. | Tip amount (a game value) | No row |
| Send & Receive Pre Tip | Remove resources from one player and give it to another after they pre tip. | Tip amount (a game value) | No row |
| Vehicle Air Time Bonus | Award resources to the vehicle driver after a long duration of air time. | Not in data | Not in data |
| Vehicle Fly Through Bonus | Award resources to the vehicle pilot after flying through a fly through trigger | Not in data | Not in data |
| Test Reward | A test entry. The data gives no goal. | Not in data | Not in data |

## Season 2 changes

- The table went from no rows to 60 rows in the Season 02 update.
- Vehicle destroyed rewards now split by variant. For example, the Kodiak has separate Default, Machine Gun and Pickup rewards. See the [challenge data page](../../game-features/Wardogs_Challenges_v1.md) for the list.
- Destroy-vehicle-section rows now grant reward tags. Before this change they granted none.

## See also

- [Challenges](challenges.md), the overview of every challenge category
- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md)
- [Hot Zone Magnet Challenges](hot-zone-magnet-challenges.md)
- [Spotting Challenges](spotting-challenges.md)
- [Cash and Rewards](cash-and-rewards.md)

## Sources

- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md), section 6 for the reward tags and base values
- [King of the Hill challenge feature](../../game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- KOTH challenge table (JSON)
- Shared session-event reward formulas (JSON)
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
