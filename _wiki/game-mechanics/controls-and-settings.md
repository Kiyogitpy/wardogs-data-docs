---
title: "Controls and Settings"
parent: "Game Mechanics"
description: "Default keyboard and mouse controls grouped by movement, combat, vehicles, building, communication and menus, plus the gameplay settings that change aim, view and the HUD, with their defaults and ranges."
---

# Controls and Settings

| Controls and Settings | |
|---|---|
| **Controls** | |
| Default input | Keyboard and mouse (gamepad defaults are in the data, not listed here) |
| Changing keys | One action per key in each category |
| **Settings** | |
| Mouse sensitivity | Default 0.4, shown range 0.1 to 2 |
| Field of view | Default 90, range 60 to 120 |
| Vehicle third-person field of view | Default 85, range 60 to 110 |
| **Internal name** | IA_* input actions, DA_Setting_* settings |
{: .wiki-infobox }

This article lists the default controls for infantry, vehicles and building, and the settings that change how the game feels to play: aim, field of view and the HUD. The defaults come from the game data. The numbers were read from the data and have not been checked in the game, so a value in the options menu may differ from the one listed here.

## Controls

The keys below are the defaults for keyboard and mouse. Some keys do different things on foot, in a vehicle and in a menu, so the same key can appear in more than one table.

### Movement

| Action | Default key |
|---|---|
| Move | W, A, S, D |
| Jump, traverse, climb off a ladder | Space |
| Deploy parachute | Space |
| Crouch | C |
| Go prone | Left Ctrl |
| Sprint and tactical sprint (toggle) | Left Shift |
| Slow walk | Left Alt |
| Lean left and right | Q and E |
| Swim fast (toggle) | Left Shift |
| Cut parachute | C |
| Drag a body | G |
| Inspect the held item | I |

Some keys do different things in different modes. Space deploys the parachute while falling and jumps off a ladder. Shift slides down a ladder and fast-swims. G drags a body.

### Combat

| Action | Default key |
|---|---|
| Fire | Left mouse button |
| Aim down sight (secondary use) | Right mouse button |
| Throw (hold, then release) | Left or right mouse button |
| Reload | R |
| Melee bash | V |
| Change fire mode | B |
| Cycle sights | Z |
| Zero the sight up and down | Page Up and Page Down |
| Mount or fold the bipod | G |
| Toggle ancillary fire (secondary fire on weapons that have it) | H |
| Scope zoom in and out | Mouse wheel up and down |
| Next and previous item | Mouse wheel down and up |
| Quick slots 0 to 9 | 0 to 9 keys |
| Toggle hands | X |
| Equipment wheel | 4 |

### Vehicles

| Action | Default key |
|---|---|
| Throttle | W (up) and S (down) |
| Steering | A and D, or mouse left and right |
| Brake | S |
| Handbrake | Space |
| Airbrake | Space |
| Helicopter collective | Left Shift and Left Ctrl |
| Helicopter pitch and roll (cyclic) | W, A, S, D, or the mouse |
| Helicopter yaw (pedals) | E and Q |
| Airplane throttle up and down | X and Z |
| Airplane flaps extend and retract | Period and Comma |
| Airplane wheel brake | Left Ctrl |
| Horn | H |
| Aggressive mode | Left Shift |
| Gear up | G |
| Gears 1 to 6 and reverse | 1 to 6 and R |
| Change camera view | C |
| Zoom the camera in and out | Page Up and Page Down |
| Look left, right and back | Left arrow, right arrow and down arrow |
| Free look (hold) | Left Alt |
| Fire countermeasures (flares) | V |
| Deploy supply crate | G |
| Next and previous seat | 0 and 9 |
| Seats 1 to 12 | F1 to F12 |
| Fire vehicle weapon | Left mouse button or Space |
| Aim vehicle weapon | Right mouse button |
| Reload vehicle weapon | R |
| Change vehicle weapon | 1 to 6 |
| Cycle vehicle weapons | Z |
| Vehicle weapon fire mode | B |
| Cycle lock state | L |
| Open garage vendor | B |

### Building

Building uses the hammer and build tool.

| Action | Default key |
|---|---|
| Rotate the piece being placed | R |
| Toggle snapping | B |
| Dismantle (hold) | V |

### Communication

| Action | Default key |
|---|---|
| Push to talk, proximity chat | K |
| Push to talk, squad chat | J |
| Toggle voice chat from the scoreboard | U |
| Open chat | Enter |
| Ping wheel (hold) | Middle mouse button |
| Ping | Middle mouse button or Right Shift |

### Interaction and menus

| Action | Default key |
|---|---|
| Interact, loot and open a vehicle menu | F |
| Call for help while downed | E |
| Give up while downed | F |
| Downed: more information | B |
| Ready up | F5 |
| Scoreboard | L |
| Map (and toggle its zoom preset) | M and N |
| Inventory | Tab |
| Minimap zoom in and out | [ and ] |
| Pause menu | Escape or F10 |
| Tips | F1 |

Each control has a gamepad default in the data as well. The full list, including gamepad and flight stick (HOTAS) defaults, is on the [Settings and Input Actions](../../content/Wardogs_SettingsAndInputs_v1.md) data page.

## Settings

Each setting has a default. Some have an exact range; where the export does not give a range, the table says so.

### Aim and sensitivity

| Setting | Default | Range or options |
|---|---|---|
| Sensitivity | 0.4 | 0.1 to 2 (shown range) |
| Vertical axis multiplier | 1 | 0.01 to 5 |
| Aim down sight (FOV) | Affected | Affected or Independent |
| Sensitivity scaling mode | Relative | Relative or Legacy |
| Sensitivity scaling transition | ADS Transition | While Transitioning, ADS Transition, Transition Finished or Instant |
| Monitor matching distance | 100 | Not in export |
| Bipod deployment | Automatic | Automatic or Manual |
| Sprint | Toggle | Hold or Toggle |
| Gamepad steady aim | Hold | Hold or Toggle |
| Gamepad crouch | Toggle | Toggle only |
| Gamepad ADS multiplier | 0.5 | 0.01 to 5 |
| Gamepad horizontal sensitivity | 4 | Stored 1 to 7, shown 1 to 10 |
| Gamepad vertical sensitivity | 3 | Stored 1 to 7, shown 1 to 10 |
| Look acceleration multiplier | 1.5 | 1.2 to 5 |
| Look acceleration curve | Standard | Standard, Linear or Aggressive |
| Look acceleration threshold | 0.9 | Not in export |
| Look acceleration pitch weight | 0.2 | Not in export |
| Gamepad response curve | Standard | Linear, Standard, Classic or Dynamic |
| Slow walk speed | Slow | Slow, Moderate or Fast |

The gamepad look acceleration is a separate setting with three curves (Standard, Linear and Aggressive), a magnitude threshold, a pitch weight and a max multiplier. The data does not show how it relates to the gamepad response curve above.

### Field of view and view model

The character's first-person field of view is set to 106 in the pawn data, while the Field of view setting below defaults to 90. Which one applies in play was not checked, because the game was not run.

| Setting | Default | Range or options |
|---|---|---|
| Field of view | 90 | 60 to 120 |
| Third-person field of view (vehicles) | 85 | 60 to 110 |
| Weapon view model scale | 0.3333 (stored) | Shown 1 to 10 in steps of 1 |

### Vehicles and helicopters

| Setting | Default | Range or options |
|---|---|---|
| Ground vehicle multiplier | 0.5 | 0.01 to 2 |
| Vehicle weapon sensitivity | 1 | Not in export |
| Transmission type | Automatic | Automatic or Sequential |
| Helicopter mouse pitch, roll and yaw sensitivity | 50 each | 1 to 100 |
| Helicopter mouse swipe left and right | Roll | Roll, Yaw or Disabled |
| Helicopter mouse swipe up and down | Pitch | Pitch or Disabled |

### HUD and information

| Setting | Default | Range or options |
|---|---|---|
| HUD visibility preset | Dynamic | Always On, Dynamic, Off or Custom |
| Quick slots | Dynamic | Always On, Dynamic or Off |
| Nameplate background opacity | Not in export | Not in export |
| Killfeed filter | Show All | Show All, Show Squad Only, Show Self Only or Show Squad and Proximity |
| Brightness | 2.2 (stored) | Shown 50 to 150 |

Video and quality options (upscaling, resolution scale, DLSS, FSR and similar) are in the data but are not covered here. Audio and language settings are covered on the [Settings and Input Actions](../../content/Wardogs_SettingsAndInputs_v1.md) page.

## Tips that follow from the settings

- Sprint is set to Toggle by default, so Left Shift switches sprinting on and off rather than being held.
- Aim down sight (FOV) is set to Affected by default. With Affected, the aimed field of view follows your field of view setting at low magnification (below 3.25x). With Independent, the aimed field of view always uses a fixed base value.
- **Chat distances.** Proximity chat reaches 1,500 and team chat 10,000 (units not stated in the data). The chat history keeps the last 250 messages.

## See also

- [Movement](movement.md): the stances and sprint rules these keys control
- [Spread and Recoil](spread-and-recoil.md): what aiming changes in a shot
- [Artillery](artillery.md): the map and gun settings used for fire missions

## Sources

- [Settings and Input Actions](../../content/Wardogs_SettingsAndInputs_v1.md)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
