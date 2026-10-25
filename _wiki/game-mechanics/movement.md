---
title: "Movement"
parent: "Game Mechanics"
description: "Walking, sprinting and tactical sprinting speeds for each stance, the stamina that limits them, and how falls, landings and parachutes hurt."
---

# Movement

| Movement | |
|---|---|
| Walk, standing | 4.3 m/s |
| Walk, crouched | 2.7 m/s |
| Walk, prone | 0.8 m/s |
| Sprint, standing | 6.1 m/s |
| Tactical sprint, standing | 6.6 m/s |
| Jump | Costs 50 of a 150 stamina pool |
{: .wiki-infobox }

Movement in Wardogs is set by your stance, your gear and the stamina you have left. Standing is the default. Crouching and going prone are slower but make you harder to hit with spread. Sprinting and tactical sprinting are faster but use stamina. This article gives the numbers. [Spread and Recoil](spread-and-recoil.md) explains how movement affects accuracy.

## Overview

A player walks at a base speed of 5.4 m/s, and each stance scales that speed. Sprinting and tactical sprinting multiply the standing speed further. Stamina limits how often you can change stance, jump and tactical sprint. Falling from height or landing hard causes damage, and a parachute changes the rules for dropping from height.

## How it works

- **Speed by stance.** Standing walks at 80% of the base speed, crouched at 50%, and prone at 15%. Sprinting is 1.42 times the standing speed, and tactical sprinting is 1.55 times. Both apply only while standing: crouching and going prone cannot sprint.
- **Direction.** Walking backwards or sideways is 70% of the stance speed.
- **Aiming down sights** halves your movement speed.
- **Acceleration.** The speed builds up at a rate set per stance: 7 standing, 12 crouched and 19 prone, in the units of the movement data. Deceleration per stance is not known.
- **Field of view.** The first-person field of view defaults to 106. A tactical sprint widens it briefly (by 5 on the base player pawn and 10 on the in-game pawn, derived from the curve).
- **Shared keys.** The same key does different things in different modes. Space deploys the parachute while falling and jumps off a ladder. Shift slides down a ladder and fast-swims. G drags a body.
- **Using a medical item** halves your movement speed while you use it.
- **Weight class.** Your gear sets a speed scale: Light 95%, Medium 87.5%, and Heavy and Super heavy 80% of the normal speed.
- **Slopes.** Ground speed changes slightly on slopes, by up to 10% at the steepest value in the data.
- **Tactical sprint.** It drains stamina at 20 per second and needs at least 20% stamina to start. After a sprint, the player waits 0.8 s before sprinting again, or 0.6 s after a tactical sprint.
- **Plain sprint.** No stamina cost for plain sprinting was found in the data. Only tactical sprint is limited by stamina.
- **Swimming.** Swimming speed is capped at 250 in the movement data, and a fast swim doubles that cap to 500 while draining 20 stamina per second. The data does not state the unit; if it is centimetres per second, that is 2.5 m/s, or 5 m/s when fast swimming (derived). In the water the speed builds up at 4000 and stops at 500 (same unit).
- **Stance changes.** Each change costs stamina from a pool of 100. Standing costs 20 and crouching 30 to change into, and going prone costs 50. The pool refills at 50 per second with no delay.
- **Jumping.** A jump costs 50 stamina from a pool of 150. The pool refills at 50 per second, and you can jump again after 0.05 s.
- **Leaning.** You can lean up to 30 degrees to the left and 35 degrees to the right. Leaning takes 0.55 s and coming back up takes 0.35 s.

Time to change stance:

| From | To | Time |
|---|---|---:|
| Standing | Crouched | 0.3 s |
| Crouched | Prone | 0.4 s |
| Prone | Crouched | 0.5 s |
| Crouched | Standing | 0.3 s |

## Numbers

Speed by stance, from the base walk speed of 5.4 m/s:

| Stance | Walk | Sprint | Tactical sprint |
|---|---:|---:|---:|
| Standing | 4.3 m/s | 6.1 m/s | 6.6 m/s |
| Crouched | 2.7 m/s | none (no sprint) | none (no sprint) |
| Prone | 0.8 m/s | none (no sprint) | none (no sprint) |

Ladder speeds:

| Action | Speed |
|---|---:|
| Climb up, maximum | 1.6 m/s |
| Climb down, maximum | 1.6 m/s |
| Climb up or down, minimum | 0.4 m/s |
| Slide down | 3.2 m/s |

Falls, landings and parachutes:

| Item | Value |
|---|---|
| Terminal fall speed | 53 m/s |
| Air control while falling | 20% |
| Landing damage starts | Fall speed 6.7 m/s (0 damage) |
| Landing damage, 100 | Fall speed 8.8 m/s |
| Landing damage, 200 | Fall speed 10.8 m/s |
| Parachute landing damage, 100 | Fall speed 17 m/s (was 11.1 m/s in Season 1) |
| Parachute, minimum fall before opening | 4 m (was 1 m in Season 1) |
| Parachute, minimum height to open above ground | 10 m (new in Season 2) |
| Parachute open time | 2 s (new in Season 2) |

The fall speeds above assume the data's curve units are centimetres per second. The data does not confirm this.

Leaving a moving vehicle can also hurt you. The damage ramps from 0 to 100 as the vehicle's speed input rises from 40 to 75; the unit of that input is not confirmed.

## Tips that follow from the numbers

- **Prone is the slowest stance.** At 0.8 m/s it is for holding a position, not for moving.
- **Stance changes are cheap.** The stance pool refills at 50 per second with no delay, so switching stance a few times in a fight rarely runs you out of stamina.
- **Tactical sprint is the stamina-limited sprint.** It drains 20 stamina per second, so it is best used for short bursts of speed.
- **Heavy gear slows you down.** A Heavy or Super heavy player moves at 80% of the normal speed, compared with 95% for Light gear.
- **Land softly.** The data starts landing damage at a fall speed of 6.7 m/s, and reaches 100 damage at 8.8 m/s.
- **Parachutes open higher now.** Season 2 raised the minimum fall before a parachute can be used from 1 m to 4 m, and added a 10 m minimum height to open it above the ground.

## Not yet known

- The deceleration of each stance, and how the acceleration units map to metres per second.
- What the slow-walk setting multiplies in play.
- How much stamina a plain sprint uses, if any.

## See also

- [Spread and Recoil](spread-and-recoil.md)
- [Downed and Revive](downed-and-revive.md)
- [Health and Damage](health-and-damage.md)

## Sources

- [Player Movement Numbers](../../content/Wardogs_PlayerMovement_v1.md)
- [Gameplay Effect Values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md) (aiming, medical and weight-class multipliers)
- [Season 2 player and movement changes](../../season-2-changes/player-movement.md) (parachutes)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
