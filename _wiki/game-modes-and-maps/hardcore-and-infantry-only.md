---
title: "Hardcore and Infantry Only"
parent: "Game Modes & Maps"
group: "Match rules"
description: "The two King of the Hill server variants: Hardcore strips the HUD helpers, Infantry Only removes armed vehicles and emplacements."
---

# Hardcore and Infantry Only

| Hardcore and Infantry Only | |
|---|---|
| Type | Server variants of King of the Hill |
| Hardcore | Removes aiming and status aids from the screen, no third person vehicle camera |
| Infantry Only | Removes 13 vehicle and emplacement packs |
| Server browser tags | Hardcore, Infantry Only |
| Internal name | KOTH_Hardcore, KOTH_InfantryOnly |
{: .wiki-infobox }

Hosts can run King of the Hill with one of two rule variants. Both appear as tags in the server browser. The game files name what each variant changes, so this page lists exactly that.

## Hardcore

Hardcore takes away helpers that normal King of the Hill shows:

- No dynamic crosshair.
- The kill feed shows only your squad.
- No ammo count on the HUD.
- No health on the minimap.
- No quick slots.
- The player health bar and the alternative critical camera features are switched off.
- Vehicles cannot use the third person camera.

The files do not state any change to damage, health or weapons in Hardcore. All the listed changes are display and camera rules.

## Infantry Only

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

The unarmed Humvee, Kodiak, Ural, Wolf-110, Z20 Lakota and MH-6 are not on the removed list. They are separate vehicle packs that the mode does not switch off, and the Infantry Only rule itself is only a label for the server browser: no game code reads it to block vehicles (inferred from the code; the game was not run). Nothing in the game files stops the unarmed vehicles from spawning in Infantry Only, so they most likely still can, unless the server removes them.

## Other server options

The server browser also tags No Rebuy, No Return To Spawn, No Vault, No Player Looting, No Team Change, No Give Up and Reduced HUD. For those the game files give only the tag names, with no separate rule definition. See [Game Modes & Maps](../game-modes-and-maps.md).

## See also

- [King of the Hill](king-of-the-hill.md)
- [Control Zone](control-zone.md)
- [Vehicle Weapons](../vehicles/vehicle-weapons.md)

## Sources

- [Experience Configs](../../game-features/Wardogs_ExperienceConfigs_v1.md): every definition, the Hardcore flags and the Infantry Only list
- [Tag display text](../../content/Wardogs_TagDisplayText_v1.md)
- [Frontend data tables](../../content/Wardogs_DataTables_Frontend_v1.md)
- KOTH_Hardcore.json
- KOTH_InfantryOnly.json
