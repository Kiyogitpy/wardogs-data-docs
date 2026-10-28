---
title: Pilot Helmet
parent: "Equipment"
group: "Armor"
description: "Vehicle-use helmet: 30% head damage reduction, halves vehicle sound in a helicopter seat, highlights target vehicles. Not sold in the shop."
---

# Pilot Helmet

| Pilot Helmet | |
|---|---|
| ![Pilot Helmet]({{ '/assets/img/icons/vendor-gear/T_UI_Gear_PilotHelmet.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Helmet |
| Slot | Helmet |
| Weight | 1 kg |
| **Protection** | |
| Damage reduction | 30% |
| Body parts covered | Head |
| Durability | 180 |
| **Availability** | |
| Price | Not sold (hidden in the shop; a price of 6,400 cash is listed) |
| Unlock | Not applicable |
| **Reference** | |
| Internal name | `ID_PilotHelmet` (item `Id.Item.PilotHelmet`) |
{: .wiki-infobox }

The Pilot Helmet protects the head with a 30% reduction, the same as the [Level 1 Helmet](level-1-helmet.md). It also has two vehicle effects: it muffles vehicle audio and highlights target vehicles. The shop marks it as hidden, so it is not sold in the shop.

## Overview

The Item Shop describes the Pilot Helmet as "Low Damage Reduction" and lists the two vehicle effects. The shop files it under "Vehicle Use" rather than "Armor". It is still an armor item, and it goes in the Helmet slot.

The weight is not listed, so the game's default of 1 applies. For all the vests and helmets, see [Body Armor](body-armor.md).

## Protection

The Pilot Helmet reduces damage to the head by 30%. It covers the head only, not the neck. It has 180 durability.

With M4 full-metal-jacket rounds, a head hit does 65.8 HP with no helmet and 46.1 HP with the Pilot Helmet. That is the same as with the Level 1 Helmet.

| Helmet | Damage reduction | Body parts covered | Durability |
|---|---:|---|---:|
| [Level 1 Helmet](level-1-helmet.md) | 30% | Head | 80 |
| [Level 2 Helmet](level-2-helmet.md) | 40% | Head | 100 |
| [Level 3 Helmet](level-3-helmet.md) | 50% | Head and neck | 180 |
| [Level 4 Helmet](level-4-helmet.md) | 60% | Head and neck | 200 |
| **Pilot Helmet** | 30% | Head | 180 |
| [Tank Helmet](tank-helmet.md) | 55% | Head and neck | 180 |

Each hit on a covered body part takes durability from the piece. For an ordinary bullet the game code removes 0.4 times the incoming damage, and the piece breaks when durability reaches 0 (from the game code; the game itself was not run to confirm it). Wear does not weaken protection: all four durability stages give the same reduction, so a worn piece protects as well as a new one until it breaks.

## Vehicle effects

The helmet has two states, and the game switches between them by where you sit.

- **In a helicopter pilot or gunner seat.** Vehicle sound is turned down to about half volume (a setting of 0.50, which is about 6 dB quieter) and passed through a low-pass filter set to 0.4, which dulls the high tones. Both changes fade in and out over 0.1 s.
- **Anywhere else.** The helmet muffles everything instead, a little: a low-pass setting of 0.45 on other players' gunfire, bullet whiz-by, impacts, vehicles, footsteps, ambience, dialogue and rain, and 0.5 on your own weapon. The volume is not changed.

The filter settings run from 0 (most muffled) to 1 (not muffled), as far as the names of the audio controls show. The files hold only that setting, not the frequency it works out to, so how dull it sounds in Hz is not known (inferred).

The target highlight has no strength setting. The game code that draws the on-screen target markers checks whether the helmet is in its helicopter state, and only then does it scan for targets (inferred from the code; the game was not run). So the highlight is on or off, not a number.

The Tank Helmet uses the same system for tracked vehicles; see [Tank Helmet](tank-helmet.md).

## Season 2 changes

The Pilot Helmet did not change in Season 2.

## See also

- [Body Armor](body-armor.md)
- [Tank Helmet](tank-helmet.md), a vehicle-use helmet with more reduction
- [Level 1 Helmet](level-1-helmet.md), the helmet with the same reduction
- [Armor (mechanic)](../game-mechanics/armor.md)
- [Choosing Ammo](../guides/choosing-ammo.md)

## Sources

- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): price (hidden), reduction, durability, covered body parts and effects
- [Items data](../../content/Wardogs_Items_v2.md): item id
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): M4 damage by body part with and without armor
- [Weapon damage locations data](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-locations.json): covered body parts and reduction per armor item
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): category names
- [Body Armor](body-armor.md): the overview of all armor
- [Round 40 medical, armour and movement evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): durability per piece, the armour damage rule and the helmet weights
