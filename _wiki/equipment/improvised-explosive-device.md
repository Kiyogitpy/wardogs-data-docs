---
title: Improvised Explosive Device
parent: "Equipment"
group: "Explosives and throwables"
description: "The Improvised Explosive Device: a placed charge that a player sets off with a trigger; the historical model has a 3 s delay and no identified range limit."
---

# Improvised Explosive Device

| Improvised Explosive Device | |
|---|---|
| ![Improvised Explosive Device]({{ '/assets/img/icons/utility-3d/T_UI_Vendor_IED2.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Lethal, placed explosive with a remote trigger |
| How it is used | Placed on the ground, then set off with its trigger |
| Historical fuse model | 3 s after trigger; current S3 consumer unresolved |
| **Blast** | |
| Damage at centre | 300 HP |
| Full damage out to | 4 m |
| No damage beyond | 8 m |
| Minimum blast damage | 60 HP |
| Thrown contact | 10 HP |
| Remote range | No limit found in the historical trace; S3 unverified |
| **Availability** | |
| Price | 300 cash |
| Shop unlock level | 0 |
| Required items | None |
| Internal name | `Id.Item.IED.Trigger` (trigger), `Id.Item.IED.Explosive` (charge) |
{: .wiki-infobox }

The Improvised Explosive Device is a placed charge with a long-range trigger. The player places it, then presses the trigger once the target is close enough to be caught by the blast. The historical model has no identified remote-range limit and starts its blast at 300 damage, the same as the AT Mine; current activation remains unverified.

## Overview

The Improvised Explosive Device is sold as a Lethal, Quick Slot item. The shop text says it can only be used once. The trigger allows one placed IED at a time.

The IED uses a C4-style detonation, so a blast from another C4 or IED sets it off. See [C4 Charge](c4-charge.md).

## How it works

**Placing.** The IED is placed on the ground. It cannot be placed in a safe zone (Alpha, Bravo, Charlie or the hostile safe zone), and it has no set placement distance.

**Historical trigger model.** The examined path starts a 3 s delay before detonation. The historical trace found no distance limit; that is not a verified S3 network or activation guarantee.

**Chain reactions.** Another C4 or IED blast sets it off.

## Default controls

Held, the IED uses the left mouse button (right trigger on a gamepad) for its main use, the right mouse button (left trigger) for its secondary use, and I to inspect. These are defaults and can be rebound in the control settings.

## Damage

### To players

The historical CL516586 actor-input model starts at 300 damage through 4 m, then falls linearly with a 60-damage floor inside 8 m; it cuts to zero at 8 m. These are starting amounts before hit filtering and damage rules, not guaranteed HP loss. Examples:

- At 5 m: 225 HP
- At 7.5 m: 60 HP
- At 8 m and beyond: nothing

Armor reduces this damage by body part. See [Body Armor](body-armor.md).

### To vehicles

The table gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Treat these as a guide, because blasts near several parts can count more than once.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 2 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 1 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 3 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 2 |

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 3 announcement

The charge weight changed from 1.5 kg to 2.7 kg; the separate trigger changed from 1.5 kg to 0.2 kg. On controller, detonation was corrected to a hold interaction rather than an uncontrollable toggle.

Source: [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). These are developer-announced changes; saved fields and historical models below do not independently verify the current binary consumer.

## Season 2 changes

No Season 2 change to the Improvised Explosive Device, or to its price, is listed.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [C4 Charge](c4-charge.md), the charge the IED's detonation is based on
- [AT Mine](at-mine.md)
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): trigger delay, placement and detonation rules
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price, description and unlock level
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): IED actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Misc Gameplay Assets: item inputs](../../content/Wardogs_MiscGameplayAssets_v1.md): section 7a, the default keys
