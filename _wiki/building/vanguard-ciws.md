---
redirect_from: ["/wiki/equipment/vanguard-ciws/"]
title: "Vanguard CIWS"
parent: "Building"
group: "Emplacements"
description: "A buildable stationary emplacement with a fast automatic 20x102 mm cannon, built with a Large Hammer from 1,200 Build Supplies."
---

# Vanguard CIWS

| Vanguard CIWS | |
|---|---|
| ![Vanguard CIWS]({{ '/assets/img/icons/buildables/T_UI_Buidable_Phalanx.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Stationary emplacement |
| **Weapon** | |
| Gun | 20x102 mm cannon |
| Fire mode | Automatic |
| Rate | 1,800 rounds/min |
| Effective range | 1,000 m |
| Reload | 3.0 s |
| Windup | 1.5 s |
| Starting ammunition | 500 rounds |
| Restock | 250 Ammo Supplies for 500 rounds |
| **Building** | |
| Build cost | 1,200 Build Supplies |
| Health | 5,000 HP |
| Hammer | Large Hammer |
| 3D hitboxes | [Open in the viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/vehicle-viewer.html#stationary-phalanx) |
| Internal name | STN_02 |
{: .wiki-infobox }

The Vanguard CIWS is a stationary emplacement with an automatic 20x102 mm cannon. It fires at 1,800 rounds/min, the fastest rate of the stationary guns. It is built with a Large Hammer from 1,200 Build Supplies and has 5,000 HP, the most health of the stationary weapons listed on the Buildables page.

## Overview

Destroying an enemy Vanguard CIWS pays 1,200 cash and 300 Role XP.

The Vanguard starts with 500 rounds and fires them in automatic bursts. A windup time of 1.5 s comes before the gun reaches full speed. It is listed on the [Building](../building.md) page with the other stationary weapons.

## Effects

### Weapon

The cannon has a rate of 1,800 rounds/min and an effective range of 1,000 m. Its reload time is 3.0 s. The game data also gives a bullet speed for the gun, but the export does not state its unit, so this article does not convert it.

The emplacement starts with 500 rounds. A restock takes 250 Ammo Supplies and gives 500 rounds.

## Use and timing

The Vanguard uses the same placement rules as the other stationary weapons: it is built with a Large Hammer, and its placement conditions check the Forward Operating Base bounds, a ladder check (not within 1 m of a ladder) and a safe zone check (not within 3 m of a safe zone or while standing in one). The [Building](../building.md) page describes these rules.

At 1,800 rounds/min, a full 500-round magazine lasts 16.7 s of continuous fire (derived: 500 rounds at 30 rounds per second). The reload after that takes 3.0 s. The figure assumes the gun never stops firing; it is not a measured time in play.

## Destroying it

The Vanguard CIWS has 5,000 HP. Explosives that burst within their inner radius take this many hits to destroy it: MAAWS 7, RPG-7 7, IED 1, C4 3, M67 frag 7. The counts are worked out from the damage rules, not timed in play, and assume full health with no repair. See the [Anti-Vehicle Guide](../guides/anti-vehicle-guide.md#emplacements).

## Cost

| Item | Value |
|---|---|
| Build Supplies | 1,200 |
| Health | 5,000 HP |
| Hammer | Large Hammer |

The Build Supplies cost is not a cash price. Build Supplies are bought in the shop, as the [Building](../building.md) page explains.

## Season 2 changes

- Build cost went from 1,500 to 1,200 Build Supplies.
- The bullet speed of the cannon went from 85,000 to 110,000 in the game's units.
- Two damage entries were added to the emplacement's damage table: one for 125 mm rocket hits (amount -20) and one for 20x102 mm cannon hits (amount -70). The amounts use the same units as the other entries in the [vehicle damage](../vehicles/vehicle-damage.md) table.

## See also

- [Building](../building.md): Build Supplies costs, health and hammers for every structure and stationary weapon
- [Talon 9K-SAM](talon-9k-sam.md), [Stingray](stingray.md), [MG Nest](mg-nest.md), [Loudspeaker](loudspeaker.md) and [L81 Mortar](l81-mortar.md): the other stationary emplacements
- [Vehicle weapons](../vehicles/vehicle-weapons.md): the guns mounted on vehicles

## Sources

- [Buildables](../../game-features/Wardogs_Buildables_v1.md): Build Supplies cost, health, hammer and placement conditions
- [All vehicles stat and damage sheet](../../content/Wardogs_AllVehicles_Stats_Damage_v1.md): the cannon's rate, fire mode, effective range and damage table
- [Items and equipment changes, Season 2](../../season-2-changes/items-equipment.md) and [Vehicles changes, Season 2](../../season-2-changes/vehicles.md): cost, bullet speed and damage table changes
- Vanguard weapon extension data: reload, restock and starting ammunition
- [Vehicle hitboxes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-hitboxes.json): the 3D hitbox set used by the viewer link
- [Round 38 building evidence, native](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-native.md): the build, repair and dismantle arithmetic
- [Round 38 building evidence, data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round38-building-data.md): weak spots, placement checks and the buildable settings
- [Round 42 buildables and economy evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-econ-buildables.md): the reward and hit-count rows used on this page.
