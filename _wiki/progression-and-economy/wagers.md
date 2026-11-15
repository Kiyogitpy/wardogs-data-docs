---
title: "Wagers"
parent: "Progression & Economy"
group: "Challenges"
description: "The S3 / 0.3 snapshot's 11 wager actions, 90 conditions, retained count ranges, stored odds and unresolved categories."
---

# Wagers

**Unavailable in Season 3: the Wager Vendor has been removed.** The [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221) say it is returning to development after exploit concerns and a redesign that weakened its intended rewards. The tables below document retained configuration only; they are not current offers or advice for earning cash.

The current saved snapshot contains **11 actions, 90 conditions and 52 objective-catalog entries**. The saved Season 2 table had four actions and 50 conditions. The kill-count maximum rises from **25 to 50**, and the revive-count maximum from **50 to 75**. The official removal establishes availability; retained unlock and settlement settings do not override it.

The stored stake range is **2,500–100,000 cash**, with a **5,000,000 cash payout cap**. All eleven actions store an **86,400-second (24-hour) cooldown**; the export does not establish its runtime scope. These are configuration values, not independently verified server behavior.

## Current actions

Retained configuration; the vendor is removed.

Ranges show minimum–maximum (default). Odds are the first and last entries of each stored count table; the full per-count lists remain in the [economy JSON](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json).

| Action | Count (default) | Stored odds range | Saved rules |
|---|---|---|---|
| Kills | 1–50 (1) | 1.001–1.5018 | Enemy players only; Not a player an enemy revived; Repeats on the same player don't count |
| Players Delivered | 1–20 (1) | 1.001–1.0771 | Drop off in or within 100m of the Control Zone; Spawn vehicles don't count; Counts once your passenger survives the drop-off |
| Revives | 1–75 (5) | 1.001–1.4147 | Teammates only; Not a player downed by a teammate or by themselves; Repeats on the same player don't count |
| Vehicles Destroyed | 1–20 (1) | 1.001–1.1479 | An enemy must be driving it; An enemy must have bought it |
| Drill Towers Activated | 1–3 (1) | 1.5–2.5 | You must enter the code yourself |
| FOBs Hacked | 1–3 (1) | 1.5–2.5 | You must complete the hack yourself |
| Freefall Kill | 1–1 (1) | 1.5–1.5 | Bail out of a helicopter you're piloting; Kill an enemy player while in freefall; Kills caused by destroying a helicopter don't count |
| Freefall Helicopter Kill | 1–1 (1) | 1.5–1.5 | Bail out of a helicopter you're piloting; Destroy an enemy helicopter with an RPG or MAAWS while in freefall; The enemy helicopter must be piloted and in the air |
| Freefall Recovery | 1–1 (1) | 1.5–1.5 | Bail out of a helicopter you're piloting; Destroy an enemy helicopter with an RPG or MAAWS while in freefall; Then get back into the pilot seat of your helicopter while it's still in the air; Don't land or open your parachute first |
| Spawn Radars Destroyed | 1–2 (1) | 1.5–2 | You must destroy the radar yourself |
| Supply Pallets Delivered | 1–4 (1) | 1.2–1.8 | You must drop the pallet off your vehicle yourself; Counts when the pallet is fully unloaded, by you or a teammate |

The rules summarize saved challenge conditions and descriptions. They do not prove current event filtering or that every action is offered in every mode.

## Current conditions

Retained configuration; these conditions are not current offers.

**All 90 categories are unresolved:** the current rows lack the former Category field. No nearby tag is substituted. A missing required-action list means **not specified in this export**, rather than proven applicability to every action. Lists that are present are retained below.

| Condition | Category | Stored required actions | Odds |
|---|---|---|---|
| No Spend | Unknown | Not specified in export | 1.1 |
| Deathwish | Unknown | Not specified in export | 10 |
| Time Limit | Unknown | Not specified in export | 4 |
| No Vehicles | Unknown | Not specified in export | 3 |
| No Resupply | Unknown | Kills | 2 |
| With {Entity} | Unknown | Kills | 1.01 |
| With {Entity} | Unknown | Kills | 1.3 |
| With {Entity} | Unknown | Kills | 1.05 |
| With {Entity} | Unknown | Kills | 1.45 |
| With {Entity} | Unknown | Kills, Spawn Radars Destroyed | 1.4 |
| With {Entity} | Unknown | Kills | 1.3 |
| Using HP Ammo | Unknown | Kills | 1.15 |
| Using AP Ammo | Unknown | Kills | 1.1 |
| With Headshot | Unknown | Kills | 1.2 |
| Tank Destroyed | Unknown | Vehicles Destroyed | 1.6 |
| {Entity} Destroyed | Unknown | Vehicles Destroyed | 1.7 |
| {Entity} Destroyed | Unknown | Vehicles Destroyed | 1.5 |
| {Entity} Destroyed | Unknown | Vehicles Destroyed | 1.4 |
| {Entity} Destroyed | Unknown | Vehicles Destroyed | 1.45 |
| With Resuscitator | Unknown | Revives | 1.1 |
| With {Entity} | Unknown | Revives | 1.025 |
| With {Entity} | Unknown | Revives | 1.05 |
| To Control Zone | Unknown | Players Delivered | 1.15 |
| To Hot Zone | Unknown | Players Delivered | 1.25 |
| In Air Vehicle | Unknown | Players Delivered | 1.1 |
| In Ground Vehicle | Unknown | Players Delivered | 1.05 |
| In {Entity} | Unknown | Players Delivered | 1.2 |
| In {Entity} | Unknown | Players Delivered | 1.15 |
| In {Entity} | Unknown | Players Delivered | 1.15 |
| In {Entity} | Unknown | Players Delivered | 1.025 |
| In {Entity} | Unknown | Players Delivered | 1.2 |
| In {Entity} | Unknown | Players Delivered | 1.01 |
| With Vehicle Impact | Unknown | Kills | 1.075 |
| With Only 1 Mag | Unknown | Kills | 1.2 |
| With Tank | Unknown | Vehicles Destroyed | 1.1 |
| With {Entity} | Unknown | Vehicles Destroyed | 1.15 |
| With {Entity} | Unknown | Vehicles Destroyed | 1.15 |
| While Moving Above 50 kph | Unknown | Vehicles Destroyed | 1.1 |
| 50 m From Teammates | Unknown | Revives | 1.1 |
| With No Weapons | Unknown | Revives | 1.15 |
| With 5 Tapes in the Vehicle | Unknown | Players Delivered | 1.005 |
| In Control Zone | Unknown | Kills, Revives | 1 |
| In Hot Zone | Unknown | Kills, Revives, Vehicles Destroyed | 1.1 |
| While Wearing No Armor | Unknown | Kills, Revives | 1.15 |
| With a $20k Loadout | Unknown | Kills, Revives, Vehicles Destroyed | 1.05 |
| With No Bandages | Unknown | Kills, Revives | 1.15 |
| While Under 50 HP | Unknown | Kills, Revives | 1.2 |
| With {Entity} | Unknown | Kills | 1.3 |
| With Magic Hands | Unknown | Revives | 1.1 |
| With {Entity} | Unknown | Kills | 1.3 |
| While Wearing Level 3 or 4 Armor | Unknown | Kills, Revives | 1.15 |
| With Any Gun | Unknown | Kills | 1.01 |
| With Backblast | Unknown | Kills | 1.45 |
| {Value}+ Digits Guessed | Unknown | Drill Towers Activated | 1.5 |
| {Value}+ Drill Towers | Unknown | Drill Towers Activated | 1 |
| With SMG, Assault Rifle Or Shotgun | Unknown | Kills | 1.01 |
| Within {Value} Seconds | Unknown | Not specified in export | 1.5 |
| With {Entity} | Unknown | Vehicles Destroyed | 1.15 |
| {Value} Kills With One Bullet | Unknown | Kills | 1.5 |
| {Value} Kills In One Explosion | Unknown | Kills | 2 |
| {Value} Vehicles In One Explosion | Unknown | Vehicles Destroyed | 2 |
| Without A Miss | Unknown | Kills, Vehicles Destroyed | 1.5 |
| {Value} Per Drone | Unknown | Kills, Vehicles Destroyed | 3 |
| In FOB | Unknown | Kills, Revives | 1.1 |
| In Enemy FOB | Unknown | Kills, Revives | 1.25 |
| In FOB With {Value}+ Supplies | Unknown | Kills, Revives | 1.65 |
| In Enemy FOB With {Value}+ Supplies | Unknown | Kills, Revives | 1.875 |
| Helicopter Destroyed | Unknown | Vehicles Destroyed | 1.5 |
| With Artillery Shell | Unknown | Vehicles Destroyed | 1.3 |
| {Value}+ Teammates In FOB | Unknown | FOBs Hacked | 1.5 |
| Alone | Unknown | FOBs Hacked | 1.25 |
| No Enemy Buildables Destroyed | Unknown | Not specified in export | 1.2 |
| With RPG or MAAWS | Unknown | Freefall Helicopter Kill, Freefall Recovery | 1.01 |
| Without Taking Damage | Unknown | Not specified in export | 1.2 |
| Without Being Spotted | Unknown | Not specified in export | 1.2 |
| Without Being Locked On | Unknown | Not specified in export | 1.2 |
| Never Repairing | Unknown | Not specified in export | 1.2 |
| Without Healing Yourself | Unknown | Not specified in export | 1.2 |
| In {Entity} | Unknown | Players Delivered | 1.01 |
| {Value} In One Trip | Unknown | Players Delivered | 2 |
| Without Reloading | Unknown | Kills | 1.5 |
| With Artillery Shell | Unknown | Kills | 1.3 |
| Without A Miss | Unknown | Kills | 1.5 |
| Perfect Quick Reloads | Unknown | Not specified in export | 1.2 |
| Without Returning To Spawn | Unknown | Not specified in export | 1.2 |
| Target In Control Zone | Unknown | Kills | 1.15 |
| Target In Hot Zone, You Outside | Unknown | Kills | 1.25 |
| Target In Hot Zone | Unknown | Kills | 1.2 |
| Without Damaging Your Team | Unknown | Not specified in export | 1.2 |
| Stolen From The Enemy | Unknown | Supply Pallets Delivered | 2 |

## Current objective catalog

All 52 saved rows are listed, including test-looking names. The saved flag is shown literally; its meaning and whether a row is offered to a player are not established. It is not a public/unlocked classification.

| Stored objective ID | Action | Count | Odds | Stored conditions | Saved flag |
|---|---|---|---|---|---|
| Hammertime | Kills | 10 | 1.37 | With {Entity}, In Control Zone | true |
| Thor | Kills | 18 | 1.61 | With {Entity}, In Hot Zone | true |
| Juggernaut | Kills | 25 | 1.97 | With {Entity}, In Hot Zone, While Wearing Level 3 or 4 Armor | true |
| Spinmerightround | Kills | 15 | 1.43 | With {Entity}, In Control Zone | true |
| Naturalborndrillers | Kills | 20 | 1.64 | With {Entity}, In Hot Zone | true |
| Twobirds | Kills | 1 | 1.5 | {Value} Kills With One Bullet, In Control Zone | true |
| Railgun | Kills | 1 | 2 | {Value} Kills With One Bullet, In Control Zone | true |
| Boomer | Kills | 1 | 2.9 | {Value} Kills In One Explosion, With {Entity}, In Control Zone | true |
| Boring | Kills | 5 | 1.02 | With Any Gun, In Control Zone | true |
| Headhunter | Kills | 10 | 1.27 | With Any Gun, With Headshot, In Control Zone | true |
| Executioner | Kills | 25 | 1.45 | With Any Gun, With Headshot, In Control Zone | true |
| Hotstuff | Kills | 10 | 1.15 | In Hot Zone | true |
| Hothead | Kills | 10 | 1.39 | In Hot Zone, With Headshot | true |
| Voyeur | Kills | 10 | 1.57 | Target In Hot Zone, You Outside, With Headshot | true |
| Roadrage | Kills | 10 | 1.13 | With Vehicle Impact, In Control Zone | true |
| Nurse | Revives | 5 | 1.001 | In Control Zone | true |
| Doctorgood | Revives | 30 | 1.13 | In Control Zone | true |
| Prayer | Revives | 50 | 1.51 | With Magic Hands, In Hot Zone | true |
| Schoolrun | Players Delivered | 3 | 1.001 | None stored | true |
| Hotdrop | Players Delivered | 8 | 1.27 | To Hot Zone | true |
| Thewholeteam | Revives | 33 | 1.26 | With Magic Hands, In Control Zone | true |
| Backwardsman | Kills | 1 | 1.45 | With Backblast, In Control Zone | true |
| Hesbehindyou | Kills | 1 | 1.6 | With Backblast, In Hot Zone | true |
| Dontstandthere | Kills | 1 | 3.19 | {Value} Kills In One Explosion, With Backblast, In Hot Zone | true |
| Matingcall | Drill Towers Activated | 1 | 1.5 | None stored | true |
| Hacker | FOBs Hacked | 1 | 1.5 | None stored | true |
| Slotmachine | Drill Towers Activated | 1 | 2.25 | {Value}+ Digits Guessed, {Value}+ Drill Towers | true |
| Minuteman | Kills | 6 | 1.7 | Within {Value} Seconds, In Hot Zone, With SMG, Assault Rifle Or Shotgun | true |
| Rush | Kills | 12 | 1.78 | Within {Value} Seconds, In Hot Zone, With SMG, Assault Rifle Or Shotgun | true |
| Deathfromabove | Vehicles Destroyed | 1 | 2.3 | {Value} Vehicles In One Explosion, With {Entity} | true |
| Droningon | Vehicles Destroyed | 3 | 1.73 | With {Entity}, Without A Miss | true |
| Specialdelivery | Vehicles Destroyed | 2 | 3.45 | With {Entity}, {Value} Per Drone | true |
| Resusthefob | Revives | 10 | 1.24 | With Resuscitator, In FOB | true |
| Getup | Revives | 15 | 1.44 | With Resuscitator, In Enemy FOB | true |
| Allyourbasearebelongtous | Revives | 20 | 2.22 | With Resuscitator, In Enemy FOB With {Value}+ Supplies | true |
| Overkill | Vehicles Destroyed | 1 | 1.95 | Helicopter Destroyed, With Artillery Shell | true |
| Sneaky | FOBs Hacked | 1 | 1.88 | Alone | true |
| Swarm | FOBs Hacked | 1 | 2.25 | {Value}+ Teammates In FOB | true |
| Theyjustletusin | FOBs Hacked | 1 | 2.7 | {Value}+ Teammates In FOB, No Enemy Buildables Destroyed | true |
| Quake | Freefall Kill | 1 | 2 | None stored | true |
| SlamDunk | Freefall Helicopter Kill | 1 | 4 | With RPG or MAAWS | true |
| Rendezook | Freefall Recovery | 1 | 8 | With RPG or MAAWS | true |
| Stealthrun | Players Delivered | 4 | 2.16 | To Hot Zone, Without Taking Damage, Without Being Spotted, Without Being Locked On | true |
| Hitandrun | Kills | 25 | 1.55 | With Vehicle Impact, Never Repairing, In Control Zone | true |
| Desmonddoss | Revives | 50 | 1.74 | With Magic Hands, In Hot Zone, With No Weapons | true |
| Itsonlyafleshwound | Revives | 75 | 2.36 | With Magic Hands, In Hot Zone, With No Weapons, Without Healing Yourself | true |
| Battlebus | Players Delivered | 1 | 2.53 | {Value} In One Trip, To Hot Zone, In {Entity} | true |
| Alldrillernofiller | Kills | 10 | 2.25 | With {Entity}, In Hot Zone, Without Reloading | true |
| Brucelee | Spawn Radars Destroyed | 2 | 2.8 | With {Entity} | true |
| Heavyrain | Kills | 50 | 4.85 | Target In Control Zone, With Artillery Shell, Without A Miss, Perfect Quick Reloads, Without Returning To Spawn | true |
| Cannonball | Kills | 1 | 3.75 | {Value} Kills In One Explosion, With Artillery Shell, Target In Hot Zone, Without Damaging Your Team | true |
| Carjacker | Supply Pallets Delivered | 2 | 2.8 | Stolen From The Enemy | true |

## Payout limits and unknowns

The pricing table stores a multi-objective bonus step of 0.25 and lives-odds values 1.009, 1.003, 1.002 and 1.001. How these values combine with conditions and the payout cap, and how deaths, disconnection or partial completion are settled, remain unverified. The 411 unlock nodes elsewhere in the current economy output do not establish a wager's server unlock rule.

The [historical Season 2 article](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/_wiki/progression-and-economy/wagers.md) retains the earlier four-action/category interpretation. It is not used to fill the current missing categories. See [the S2→S3 notes](../patch-notes/season-3.md).

## Sources and related pages

- [Current economy JSON](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json)
- [Challenges and session events](../../game-features/Wardogs_Challenges_v1.md)
- [Achievements](achievements.md)
- [Currencies](currencies.md)
- [S2→S3 reward differences](../../season-3-changes/rewards-unlocks.md)
