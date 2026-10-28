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
| Mouse sensitivity | Default 0.4 (stored; the slider shows about 0.73), shown range 0.1 to 2 |
| Field of view | Default 90, range 60 to 120 |
| Vehicle third-person field of view | Default 85, range 60 to 110 |
| **Internal name** | IA_* input actions, DA_Setting_* settings |
{: .wiki-infobox }

This article lists the default controls for infantry, vehicles and building, and the settings that change how the game feels to play: aim, field of view and the HUD. The defaults come from the game itself. The numbers were read from the game's code and have not been checked in the game, so a value in the options menu may differ from the one listed here.

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

Each control also has a gamepad default. The full list, including gamepad and flight stick (HOTAS) defaults, is on the [Settings and Input Actions](../../content/Wardogs_SettingsAndInputs_v1.md) data page.

## Settings

Each setting has a default. Some have an exact range; where no range is known, the table says so.

### Aim and sensitivity

| Setting | Default | Range or options |
|---|---|---|
| Sensitivity | 0.4 (stored; the slider shows about 0.73) | 0.1 to 2 (shown range) |
| Vertical axis multiplier | 1 | 0.01 to 5 |
| Aim down sight (FOV) | Affected | Affected or Independent |
| Sensitivity scaling mode | Relative | Relative or Legacy |
| Sensitivity scaling transition | ADS Transition | While Transitioning, ADS Transition, Transition Finished or Instant |
| Monitor matching distance | 100 | Not known |
| Bipod deployment | Automatic | Automatic or Manual |
| Sprint | Toggle | Hold or Toggle |
| Gamepad steady aim | Hold | Hold or Toggle |
| Gamepad crouch | Toggle | Toggle only |
| Gamepad ADS multiplier | 0.5 | 0.01 to 5 |
| Gamepad horizontal sensitivity | 4 | Stored 1 to 7, shown 1 to 10 |
| Gamepad vertical sensitivity | 3 | Stored 1 to 7, shown 1 to 10 |
| Look acceleration multiplier | 1.5 | 1.2 to 5 |
| Look acceleration curve | Standard | Standard, Linear or Aggressive |
| Look acceleration threshold | 0.9 | Not known |
| Look acceleration pitch weight | 0.2 | Not known |
| Gamepad response curve | Standard | Linear, Standard, Classic or Dynamic |
| Slow walk speed | Slow | Slow, Moderate or Fast |

Two different gamepad curve settings exist: the look acceleration curve (Standard, Linear or Aggressive, with its own threshold, pitch weight and max multiplier) and the gamepad response curve (Linear, Standard, Classic or Dynamic). The game does not show how the two relate.

#### Mouse sensitivity formula

This is derived from the game's code and settings files, not measured on screen. It covers mouse look on foot (hip fire and aiming down sights); vehicles use other multipliers.

**Slider to stored value.** The Sensitivity slider is a rescaled value. The game stores a number from 0.1 to 1.0 and the slider shows it stretched to 0.1 to 2. With S for the stored value and d for the number the slider shows:

- S = 0.1 + (d - 0.1) x 0.4737 (that is 0.9 / 1.9)
- The default stored value is 0.4, which the slider shows as about 0.73.

**Hip fire.** The view turns by the same amount left and right and up and down:

- degrees per mouse count = 0.07 x S

The 0.07 is the standard Unreal mouse scale from the game's input settings. The legacy 2.5 look scale is switched off, so nothing else is multiplied in. Mouse acceleration is off at its default of 0; if it is raised, each frame's movement is raised to the power 1 plus the acceleration value (0 to 0.05), which makes small movements slower than large ones.

**Worked values (800 DPI).** One 360 degree turn takes 360 / (degrees per count) counts, which is 360 / (degrees per count) / DPI x 2.54 centimeters of mouse travel.

| Slider shows | Stored S | Degrees per count | Counts per 360 | cm per 360 at 800 DPI |
|---|---|---|---|---|
| 0.1 | 0.100 | 0.0070 | 51,429 | 163.3 |
| 0.4 | 0.242 | 0.0169 | 21,242 | 67.4 |
| 0.5 | 0.289 | 0.0203 | 17,766 | 56.4 |
| 0.73 (default) | 0.400 | 0.0280 | 12,857 | 40.8 |
| 1.0 | 0.526 | 0.0368 | 9,771 | 31.0 |
| 1.5 | 0.763 | 0.0534 | 6,739 | 21.4 |
| 2.0 | 1.000 | 0.0700 | 5,143 | 16.3 |

At other DPI values scale the last column by 800 / DPI.

**Aiming down sights.** While aiming, two more factors multiply the hip value:

- degrees per count = 0.07 x S x (ADS multiplier setting, default 1) x R

R narrows the turn rate as the view zooms in. With the default Relative scaling mode, on a 16:9 screen and with Monitor matching distance at its default of 100, R is simply the aimed field of view divided by your normal field of view. In general R = atan(k x tan(aimed FOV / 2)) / atan(k x tan(FOV / 2)), where k is the Monitor matching distance divided by 100, times the screen's width to height ratio divided by 16/9. The Legacy mode uses the plain tangent ratio, tan(aimed FOV / 2) / tan(FOV / 2), which turns slower still. The aimed field of view is the one described under the Aim down sight setting below (72 degrees or your field of view, divided by the sight's magnification). The Sensitivity scaling transition setting decides how much of R applies while the sight is coming up: ADS Transition (default) applies it in proportion to how far the sight has come up, While Transitioning applies all of it as soon as aiming starts, Transition Finished applies it only once the sight is fully up, and Instant applies it while the aim button is held. Hip fire is not scaled.

**Example: a 4x scope at the default settings.** The normal field of view is 90 and a 4x sight starts from 72, so the aimed field of view is 18 degrees and R = 18 / 90 = 0.2. At the default stored value that is 0.028 x 0.2 = 0.0056 degrees per count, or about 204 cm per 360 at 800 DPI (the hip value is 40.8). On a 21:9 screen R is about 0.22, and in Legacy mode about 0.16. A 2x sight in Affected mode gives R = 0.5, and a 10x scope gives 0.08.

Two parts are inferred from how Unreal Engine normally behaves rather than read in the game's own code: that the 0.07 mouse scale is applied to the mouse in the game's input path, and the exact rule that stretches the stored value to the slider. If the first were wrong, every turn rate above would be 14 times faster. A separate Vertical axis multiplier setting exists, but no code that applies it to mouse look was found, so the figures above treat it as 1.

### Field of view and view model

The character's first-person camera is built with a field of view of 106, while the Field of view setting below defaults to 90. The game copies the setting onto the camera when it applies the player's field of view, so the 90 (or whatever the slider says) is the normal view you see and the 106 is only the asset's starting value (derived from the camera code, not checked on screen). The Third-person field of view setting is used the same way in vehicles.

| Setting | Default | Range or options |
|---|---|---|
| Field of view | 90 | 60 to 120 |
| Third-person field of view (vehicles) | 85 | 60 to 110 |
| Weapon view model scale | 0.3333 (stored) | Shown 1 to 10 in steps of 1 |

### Vehicles and helicopters

| Setting | Default | Range or options |
|---|---|---|
| Ground vehicle multiplier | 0.5 | 0.01 to 2 |
| Vehicle weapon sensitivity | 1 | Not known |
| Transmission type | Automatic | Automatic or Sequential |
| Helicopter mouse pitch, roll and yaw sensitivity | 50 each | 1 to 100 |
| Helicopter mouse swipe left and right | Roll | Roll, Yaw or Disabled |
| Helicopter mouse swipe up and down | Pitch | Pitch or Disabled |

### HUD and information

| Setting | Default | Range or options |
|---|---|---|
| HUD visibility preset | Dynamic | Always On, Dynamic, Off or Custom |
| Quick slots | Dynamic | Always On, Dynamic or Off |
| Nameplate background opacity | Not known | Not known |
| Killfeed filter | Show All | Show All, Show Squad Only, Show Self Only or Show Squad and Proximity |
| Brightness | 2.2 (stored) | Shown 50 to 150 |

Video and quality options (upscaling, resolution scale, DLSS, FSR and similar) are set in the game but are not covered here. Two numbers worth knowing are:

- **Texture streaming memory.** The texture streaming pool depends on the texture quality level: 1,280 MB at level 0, 2,048 MB at level 1, 3,072 MB at level 2 and 6,144 MB at level 3. These are the configured pool sizes for each level.
- **Languages.** The game has text for 15 languages: English, German, Spanish, French, Italian, Japanese, Korean, Polish, Portuguese, Brazilian Portuguese, Russian, Turkish, Ukrainian, Simplified Chinese and Traditional Chinese.

Audio and language settings are covered on the [Settings and Input Actions](../../content/Wardogs_SettingsAndInputs_v1.md) page.

## Tips that follow from the settings

- Sprint is set to Toggle by default, so Left Shift switches sprinting on and off rather than being held.
- Aim down sight (FOV) is set to Affected by default. With Affected, the aimed field of view starts from your field of view setting, so changing the slider also changes the scope view. With Independent, the aimed field of view always starts from a fixed 72 degrees, and the slider no longer changes the scope view. The aimed view is that base divided by the sight's magnification, so a 2.5x sight gives 36 degrees from the default 90. Even in Affected mode, a sight of 3.25x or more also starts from 72 degrees, as the setting's own description says ("below 3.25x"), so a 4x sight gives 18 degrees. For a variable-zoom scope the test uses its highest magnification. Because the angle is divided, the real picture magnification against the normal view is the tangent of half the normal angle divided by the tangent of half the aimed angle: a 4x sight on the default 90 gives 18 degrees, which is about 6.3 times the normal size, and a 2.5x sight gives 36 degrees, about 3.1 times. The sights page lists this effective magnification for every sight, derived from the camera code and not measured on screen. These rules come from the camera code and were not checked on screen; that the 72 degree rule belongs to this setting is inferred from the code, not traced. See [Sights and optics](../attachments/sights-and-optics.md).
- **Chat distances.** Proximity chat reaches 1,500 and team chat 10,000 (units not stated). The chat history keeps the last 250 messages.

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
- [Round 46 A evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round46-a.md): wiki update notes and data findings for this article
