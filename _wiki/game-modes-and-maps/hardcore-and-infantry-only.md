---
title: "Hardcore and Infantry Only"
parent: "Game Modes & Maps"
group: "Match rules"
description: "The saved Season 2 Hardcore and Infantry Only rule layers, and the limits of the current S3 config export."
---

# Hardcore and Infantry Only

| Hardcore and Infantry Only | |
|---|---|
| Type | Historical Season 2 King of the Hill rule layers |
| Hardcore | Removes aiming and status aids from the screen, no third person vehicle camera |
| Infantry Only | Removes 13 vehicle and emplacement packs |
| Server browser tags | Hardcore, Infantry Only |
| Internal name | KOTH_Hardcore, KOTH_InfantryOnly |
{: .wiki-infobox }

The lists below describe the saved Season 2 (CL516586) rule layers. The current S3 standalone-config export contains four definitions and neither variant file. That absence does not prove mode removal: the current mode includes, feature activation and server overrides still need to be traced. These lists must not be used as current S3 availability rules.

## Season 2 Hardcore

Hardcore takes away helpers that normal King of the Hill shows:

- No dynamic crosshair.
- The kill feed shows only your squad.
- No ammo count on the HUD.
- No health on the minimap.
- No quick slots.
- The player health bar and the alternative critical camera features are switched off.
- Vehicles cannot use the third person camera.

The files do not state any change to damage, health or weapons in Hardcore. All the listed changes are display and camera rules.

## Season 2 Infantry Only

Infantry Only is King of the Hill with the heavier and armed vehicle packs disabled:

| Removed | What it is |
|---|---|
| L2A6, SPH-2 and Flakpanzer Gepard | The tank bodies |
| T-72B3 | Main battle tank |
| Havoc | Attack helicopter |
| AH-6M [Miniguns] and AH-6R [Rockets] | The armed AH-6 helicopters |
| Z20 Lakota [Miniguns] | The armed Lakota |
| Humvee [Minigun] and Humvee [M249] | The armed Humvees |
| Kodiak [M249] | The armed Kodiak |
| Ural Defender [M249] | The armoured Ural with a machine gun |
| Wolf-110 [M2 Browning] | The armed Wolf |
| Talon 9K SAM, Vanguard CIWS and Stingray | Buildable anti-air and counter-rocket emplacements |

The historical disabled list does not include the unarmed Humvee, Kodiak, Ural, Wolf-110, Z20 Lakota or MH-6 packs. That alone does not establish that those vehicles can spawn: the active includes, vehicle eligibility consumer and server overrides are separate requirements, unresolved for S3.

## Other server options

The server browser also tags No Rebuy, No Return To Spawn, No Vault, No Player Looting, No Team Change, No Give Up and Reduced HUD. For those the game gives only the tag names, with no separate rule definition. See [Game Modes & Maps](../game-modes-and-maps.md).

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Vehicle Weapons](../vehicles/vehicle-weapons.md)

## Sources

- [Experience Configs](../../game-features/Wardogs_ExperienceConfigs_v1.md): every definition, the Hardcore flags and the Infantry Only list
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md)
- [Frontend data tables](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Saved Season 2 Hardcore rules](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/data/Wardogs/Config/Experiences/KOTH_Hardcore.json)
- [Saved Season 2 Infantry Only rules](https://github.com/Kiyogitpy/wardogs-data-docs/blob/8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b/data/Wardogs/Config/Experiences/KOTH_InfantryOnly.json)
