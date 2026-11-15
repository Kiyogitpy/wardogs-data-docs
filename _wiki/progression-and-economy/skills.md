---
title: "Skills"
parent: "Progression & Economy"
group: "Roles and mastery"
description: "The six roles and their 62 skills: their configured effects, from faster aiming to longer tac-sprints and lower fuel use."
---

# Skills

| Skills | |
|---|---|
| Roles | Assault (17 skills), Recon (17), Support (12), Medic (4 with numbers, 23 nodes), Pilot (6), Driver (6) |
| Total | 62 skills |
| Unlock level and cost | Not supplied by the reviewed skill-effect/curve exports; current upgrade consumer unresolved |
| Internal name | Role skill tables (one per role, plus four plugin tables) |
{: .wiki-infobox }

Each role has its own skill set. A saved skill row configures an intended effect on how fast a weapon comes up, how far a player moves while aiming, how much recoil a weapon kicks, or how much fuel a vehicle uses. The skills are the role-level side of progression, alongside [role mastery XP](cash-and-rewards.md#role-mastery-xp).

## Roles

- [Assault](assault.md): 17 skills for assault rifles and SMGs, plus movement and door breaching
- [Recon](recon.md): 17 skills for sniper and marksman rifles, spotting and infrared visibility
- [Support](support.md): 12 skills for LMGs and shotguns, plus C4 detonator range
- [Medic](medic.md): 4 skills for medical items and sprint boosts after a revive
- [Pilot](pilot.md): 6 skills for air vehicles and dropped supply crates
- [Driver](driver.md): 6 skills for ground vehicles and dropped supply crates

## Overview

A skill is stored as a set of effects. Effects reference attributes, application tags and, where applicable, curves. Their presence does not establish current activation. Multiplier and level interpretations below follow the CL516586 analysis unless explicitly described as stored fields; current consumers have not been matched.

Skills are not part of the role unlock tree. The current tree lists 411 nodes across the six role trees and Wardog tree, with stored level requirements and cash costs (see the Unlocks table on each role page), and none of them is a skill. The skill tree screen shows 130 nodes, but only 62 of them have a skill effect. The other 68 have no effect mapping in the reviewed exports; this does not exclude another consumer. These skill-effect and curve exports supply no per-level unlock costs. Current skill-point earning, spending and upgrade consumers remain unresolved (see [Currencies](currencies.md)).

## How it works

- **Where a skill applies.** The effect rows name application slots: an item, a vehicle, the character, a held item, a supply crate you drop, or a player you revive.
- **Skill level.** The CL516586 round 45 trace used the node upgrade level as curve Time; it did not establish the first-unlock byte or server increment. The current curves store Linear keys at Time 0, 2, 3, 4 (or 0, 2, 4), starting at value 1. Applying that interpolation and magnitude through an S3 native consumer remains unverified.
- **Curve example.** The Assault aim-down-sights time curves are 1, 0.8, 0.7 and 0.6 at levels 0, 2, 3 and 4, which models faster aiming if the historical level and multiplier interpretation applies.
- **Grants.** Three stored rows reference ability-grant effects rather than numeric curves: sprint-breaching doors (Assault), lockpicking (Recon) and a sniper-kill focus refresh (Recon).

## Configured effects by role

### Assault (17)

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
- **After a revive.** Self and Teammate rows reference sprint-speed curves, but both store Meta.Skill.Revive.Target. Current recipient routing and boost application remain unresolved.

### Pilot (6)

- **Air vehicles.** Faster time to aim down sights on a mounted machine gun in an air vehicle. Less horizontal and vertical recoil on that gun. Lower fuel use in air vehicles. Less impact damage to an air vehicle.
- **Supply crates.** The Pilot supply-crate slot references a health effect with stored curve values 1.0, 1.2 and 1.4 at Time 0, 2 and 4. Crate-creation application was traced for CL516586, not re-established for S3.

### Driver (6)

- **Ground vehicles.** The same set as the Pilot skills, for ground vehicles and their mounted guns: faster aiming on the gun, less recoil, lower fuel use, less impact damage.
- **Supply crates.** The Driver supply-crate slot references the same health effect and curve values as Pilot. Crate-creation application was traced for CL516586, not re-established for S3.

## Numbers

The game stores each skill's values as curves over skill levels. This page does not quote them. The skill tables in the progression data page have the full values.

## Interpreting the saved mappings

- Assault and Recon have the most skills (17 each). Support has 12, and the rest have 4 to 6.
- Several skills are one-time unlocks: infrared reduction and sniper focus refresh (Recon), and detonator range (Support).
- Skills that change aiming speed apply by weapon class (assault rifle, SMG, LMG, shotgun, sniper, marksman). The saved filter names the intended class; current application is unverified.

## Season 2 changes

The sources list no Season 2 changes to the skill tables. Season 2 did change the role unlock tree, with cash costs and level gates changed for many items. Those changes are in the Season 2 Rewards & Unlocks page.

## See also

- [Cash and Rewards](cash-and-rewards.md), including the role mastery XP curve
- [Challenges](challenges.md)
- [Shops](shops.md)
- [Medical Items](../equipment/medical-items.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)

## Sources

- [Progression tables](../../game-features/Wardogs_Progression_v1.md), including the skill tables
- [Rewards and progression](../../Wardogs_Rewards_and_Progression_v2.md)
- [Season 2 changes: Rewards & Unlocks](../../season-2-changes/rewards-unlocks.md)
- [Round 36 economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-econ.md)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the supply crate durability skill for pilots and drivers
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the supply crate durability skill and how it is applied to dropped crates
- [Round 45 C, FOB health, build messages, skill curve and destruction evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-c.md)
