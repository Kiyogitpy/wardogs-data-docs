---
title: M67 Frag Grenade
parent: "Equipment"
group: "Explosives and throwables"
description: "The M67 Frag Grenade: a thrown blast grenade with a 4 second fuse, 100 HP at its centre and 10 m of reach."
---

# M67 Frag Grenade

| M67 Frag Grenade | |
|---|---|
| ![M67 Frag Grenade]({{ '/assets/img/icons/utility-3d/T_UI_Vendor_Grenade2.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Type | Lethal, thrown (quick slot) |
| How it is used | Thrown. Can be cooked (held before throwing). Throwing one back never applies as shipped (from the game code, not tested in play) |
| Fuse | 4 s after the throw |
| **Blast** | |
| Damage at centre | 100 HP |
| Full damage out to | 5 m |
| No damage beyond | 10 m |
| Minimum blast damage | 10 HP |
| Thrown contact | 10 HP |
| **Availability** | |
| Price | 200 cash |
| Shop unlock level | 1 |
| Required items | None |
| Internal name | `Id.Item.M67Grenade` |
{: .wiki-infobox }

The M67 Frag Grenade is the standard hand grenade. It is thrown, goes off 4 seconds later, and does up to 100 HP to everyone close to the blast. Its damage stops at 10 m. Throwing a live one back never applies as shipped; see Fuse.

## Overview

The M67 is the basic blast throwable in the item shop. It sits in the quick slot and is listed as a lethal item. The Gold M67 inherits the M67 and has no shop listing. It has the same 4 second fuse, so the same rule against throwing it back applies to it (from the game code, not tested in play).

For the blast numbers of every other explosive, see [Grenades and Explosives](grenades-and-explosives.md).

## How it works

**Fuse.** The grenade goes off 4 s after it is thrown. Holding it before the throw (cooking) is allowed, so a player can shorten the time left before it lands. **Throwing one back never applies as shipped.** From the game code, not tested in play: a grenade can be thrown back only while more than 5 s of its fuse is left, and the M67's fuse is 4 s at most, so the check always fails. Molotovs and smoke grenades cannot be thrown back at all.

**Throw.** Three throws are listed:

| Throw | Speed | Notes |
|---|---:|---|
| Overarm (primary) | 25 m/s (2,500 cm/s) | The longest throw |
| Underarm (secondary) | 14 m/s (1,400 cm/s) | Short range |
| Back throw | 18 m/s (1,800 cm/s) | Third throw action in the data; never applies as shipped (see Fuse) |

**Contact.** A grenade that hits something before it goes off does 10 HP of thrown-contact damage.

**Friendly fire.** The damage tables reduce friendly fire only for infantry bullets (-50 %) and large hammers (-70 %). Explosives and fire have no friendly-fire reduction in the tables. Any limit on hitting teammates with this item would have to come from the item itself or from native code, which the game files do not show.

## Damage

### To players

The blast does its full 100 HP from the centre out to 5 m. Beyond 5 m the damage falls in a straight line to zero at 10 m. Examples:

- At 5 m: 100 HP
- At 7.5 m: 50 HP
- At 10 m and beyond: nothing

Body armor reduces this damage by body part. See [Body Armor](body-armor.md). The numbers here are before armor.

### To vehicles

The table gives the number of centre hits a vehicle needs to lose its main health. This assumes one blast hitting the main section. Blasts near several parts of a vehicle can count more than once, so treat these as a guide.

| Vehicle | Main health | Centre hits to destroy |
|---|---:|---:|
| [MH-6](../vehicles/mh-6.md) | 400 HP | 1 |
| [Humvee](../vehicles/humvee.md) | 500 HP | 2 |
| [T-72B3](../vehicles/t-72b3.md) | 750 HP | 7 |
| [M113 APC SV](../vehicles/m113-apc-sv.md) | 1000 HP | 6 |

Against armour the plain frag grenade is weak. Its table entry is -60 % on the tanks, -15 to -45 % on the Humvee family, the Ural, the Kodiak and the Wolf-110, -20 % on the Havoc and +50 % on the Little Bird. Where an entry also needs the inner blast radius, the table marks it (+Inner); this page does not model that part.

See [Vehicle damage](../vehicles/vehicle-damage.md) for how vehicles take damage in general.

## Season 2 changes

No Season 2 change to the M67 Frag Grenade is listed.

## See also

- [Grenades and Explosives](grenades-and-explosives.md), the overview of thrown and placed explosives
- [C4 Charge](c4-charge.md), a remote-detonated charge with a larger blast
- [Improvised Explosive Device](improvised-explosive-device.md)
- [Body Armor](body-armor.md)
- [Vehicle damage](../vehicles/vehicle-damage.md)

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the armour readings for the frag grenade and the throw-back caveat
- [Explosives Reference](../../game-features/Wardogs_Explosives_v1.md): blast damage, radius, falloff, fuse and vehicle hit counts
- [Fire, Smoke and Mines](../../game-features/Wardogs_FireAndUtility_v1.md): throw speeds and throw actions
- [Item Shop for Non-Weapon Items](../../game-features/Wardogs_ItemShop_v1.md): name, price, unlock level and shop text
- [Explosive actor defaults](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/explosive-actors.json): thrown actor values
- [Vehicle damage pipeline](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md): how explosives are scaled against vehicles
- [Items and Equipment changes, Season 2](../../season-2-changes/items-equipment.md): the Season 2 check
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): the M67 throw-back check and its fuse time, and the Gold M67 entry
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the throw-back gate and the M67 fuse values
