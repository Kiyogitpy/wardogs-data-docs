---
title: "Skills"
parent: "Progression & Economy"
description: "The six roles and their 62 skills: what each skill changes in play, from faster aiming to longer tac-sprints and lower fuel use."
---

# Skills

| Skills | |
|---|---|
| Roles | Infantry (17 skills), Recon (17), Support (12), Medic (4), Pilot (6), Driver (6) |
| Total | 62 skills |
| Unlock level and cost | Not yet known (see below) |
| Internal name | Role skill tables (one per role, plus four plugin tables) |
{: .wiki-infobox }

Each role has its own skill set. A skill tweaks one part of play: how fast a weapon comes up, how far a player moves while aiming, how much recoil a weapon kicks, or how much fuel a vehicle uses. The skills are the role-level side of progression, alongside [role mastery XP](cash-and-rewards.md#role-mastery-xp).

## Overview

A skill is stored as a set of effects. Each effect changes one value, such as aiming time or recoil, by a multiplier. The strength of the multiplier grows with the skill's rank. The data stores that growth as a curve for each skill. Lower aim-time multipliers mean faster aiming, for example.

Skill unlock levels and costs are not in the sources. The skill tree layout exists, but the tree that links skills to unlock levels does not list them, so the level and cost of each rank are not yet known.

## How it works

- **Where a skill applies.** Each skill applies to one of several slots: an item, a vehicle, the character, a held item, a supply crate you drop, or a player you revive.
- **Strength.** Most effects multiply a value by the skill's current strength. The strength is set by the skill's curve.
- **Curve example.** The Driver's time-to-aim curve steps from 1.0 down to 0.6 across its ranks, so a higher rank aims faster. The data does not state which curve key is which rank, so this reading is inferred.
- **Grants.** Three skills unlock an ability rather than changing a number: sprint-breaching doors (Infantry), lockpicking (Recon) and a sniper-kill focus refresh (Recon).

## Skills by role

### Infantry (17)

- **Aiming.** Faster time to aim down sights with assault rifles and with SMGs. Faster aiming movement with assault rifles and with SMGs.
- **Recoil.** Less horizontal and less vertical recoil with assault rifles and with SMGs.
- **Weapon handling.** Faster return to fire with assault rifles and SMGs after sprinting, ladders or vaults. Faster weapon switching to assault rifles and SMGs.
- **Movement.** Faster crouch and prone movement. Faster tac-sprint stamina recovery, a longer tac-sprint, and faster stamina recovery while crouched or prone. A faster unarmed sprint.
- **Other.** Sprint-breaching through doors.

### Recon (17)

- **Aiming.** Faster time to aim down sights with sniper rifles and with marksman rifles. Faster aiming movement with both.
- **Recoil.** Less horizontal and vertical recoil with sniper rifles and with marksman rifles.
- **Handling.** Faster return to fire with sniper and marksman rifles. Faster switching to sidearms, and to sniper and marksman rifles.
- **Spotting.** Enemies take longer to spot you. Enemies you spot stay spotted longer.
- **Other.** Lockpicking enemy locked vehicles, buildables and fortifications. Infrared visibility reduction (a one-time unlock). A sniper-rifle kill refreshes focus (a one-time unlock).

### Support (12)

- **Aiming.** Faster time to aim down sights with LMGs and with shotguns. Faster aiming movement with LMGs and with shotguns.
- **Recoil.** Less horizontal and vertical recoil with LMGs and with shotguns.
- **Handling.** Faster return to fire with LMGs and shotguns. Faster weapon switching with LMGs and shotguns.
- **Other.** Longer C4 detonator range (a one-time unlock).

### Medic (4)

- **Medical items.** Faster switching to medical items. A medkit has more uses before it runs out.
- **After a revive.** The medic gets a short sprint-speed boost after reviving a teammate. The revived teammate also gets a short sprint-speed boost.

### Pilot (6)

- **Air vehicles.** Faster time to aim down sights on a mounted machine gun in an air vehicle. Less horizontal and vertical recoil on that gun. Lower fuel use in air vehicles. Less impact damage to an air vehicle.
- **Supply crates.** A supply crate you drop as a pilot takes more damage before it breaks.

### Driver (6)

- **Ground vehicles.** The same set as the Pilot skills, for ground vehicles and their mounted guns: faster aiming on the gun, less recoil, lower fuel use, less impact damage.
- **Supply crates.** A supply crate you drop as a driver takes more damage before it breaks.

## Numbers

The data stores each skill's per-rank values in curve tables. This page does not quote them. The skill tables in the progression data page have the full values.

## Tips that follow from the numbers

- Infantry and Recon have the most skills (17 each). Support has 12, and the rest have 4 to 6.
- Several skills are one-time unlocks: infrared reduction and sniper focus refresh (Recon), and detonator range (Support).
- Skills that change aiming speed apply by weapon class (assault rifle, SMG, LMG, shotgun, sniper, marksman). A skill helps only the class it names.

## Season 2 changes

The sources list no Season 2 changes to the skill tables. Season 2 did change the role unlock tree, with cash costs and level gates changed for many items. Those changes are in the Season 2 Rewards & Unlocks page.

## See also

- [Cash and Rewards](cash-and-rewards.md), including the role mastery XP curve
- [Challenges](challenges.md)
- [Shops](shops.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the skill tables
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
