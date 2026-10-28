---
title: "Compound Bow"
parent: "Weapons"
group: "Bows"
description: "The Compound Bow: a draw-and-release weapon with Broadhead and Rambo Explosive arrows, its price, damage, range and Season 2 changes."
---

# Compound Bow

| Compound Bow | |
|---|---|
| ![Compound Bow]({{ '/assets/img/icons/weapons-3d-session/T_UI_Weapon_Bow_BC.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** | |
| Class | Bow |
| Ammunition | Broadhead Arrow, Rambo Explosive Arrow |
| Fire modes | Semi-automatic (draw, then release) |
| Weight | 1.3 kg |
| Inventory size | 6x2 |
| **Performance** | |
| Arrow speed | 160 m/s (Season 2) |
| Arrow damage | 77 (Broadhead), 150 blast (Rambo Explosive) |
| Full draw | 1.4 s |
| **Availability** | |
| Price | 1,350 cash |
| Unlock level | 0 in the shop; Recon level 16 in the role tree |
| Internal name | `Id.Item.CombatBow` |
{: .wiki-infobox }

The Compound Bow is a draw-and-release weapon. It is sold in the item shop, not in the weapon shop, and the data gives it its own ammunition: the Broadhead Arrow and the Rambo Explosive Arrow. It is the only bow in the game.

## Overview

The primary use button (left mouse button, or the right trigger on a gamepad) draws it, and letting go releases the arrow. A second action cancels a draw. Drawing is not instant: the item data gives a full draw of 1.4 s, and the speed the arrow leaves at depends on how far the draw has gone.

It appears on the weapon shop list without any statistics. The stats are in the item data, which is why it has no spray pattern or damage table like the rifles do.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Semi-automatic |
| Fire rate | 90 rounds/min as stored (the draw sets the real pace) |
| Arrow speed | 160 m/s in Season 2 (65,000 in Season 1, assuming the stored unit is cm/s: 650 m/s) |
| Full draw | 1.4 s |
| Release speed | Starts at 5% of full speed and reaches 100% as the draw builds (the draw unit is not stated; the curve ends at 0.4) |
| Weight | 1.3 kg |
| Inventory size | 6x2 |

## Damage

Both arrows use their own damage type, listed here as the data states.

| Arrow | Base damage | Speed | Flight time limit | Mass |
|---|---:|---:|---:|---:|
| Broadhead Arrow | 77 | 152 m/s | 14 s | 0.029 |
| Rambo Explosive Arrow | 150 (blast) | 180 m/s | 20 s | 0.045 |

The speeds assume the stored unit is cm/s, as the weapon's speed does. The Broadhead Arrow's shop text says it is effective against unarmored targets.

**Range falloff.** The bow keeps full damage out to 100 m (assuming the stored unit is cm), then loses damage in a straight line until it does none at 500 m. The far end of the stored curve (1,200 m) kept 20% damage in Season 1 and keeps none in Season 2.

**Armor.** Arrows do x0.90 against Heavy vests and Heavy helmets and x0.66 against Super heavy ones. Light and Medium gear does not reduce arrow damage. See [Armor](../game-mechanics/armor.md). The Broadhead Arrow has a penetration multiplier of 0.5 in Season 2 (0.03 in Season 1) and a ricochet angle of 30 degrees.

**Rambo Explosive Arrow.** This arrow explodes on impact: 150 HP at the centre, full damage out to 2 m and none beyond 4 m. It is listed with the other explosives in [Grenades and Explosives](../equipment/grenades-and-explosives.md#launcher-and-bow-rounds).

## Recoil and spread

Standing, the bow's hip spread runs from 1 to 2 (degrees, as the spread page gives them), crouched from 0.5 to 1 and prone it is 0.5. Fully aimed, spread is 0. See [Spread and recoil](../game-mechanics/spread-and-recoil.md). The bow uses the sniper rifle aim-down-sights camera curve.

## Ammunition

| Arrow | Shop price | Stack | Inventory size |
|---|---:|---|---|
| Broadhead Arrow | 75 cash for 5 | Up to 10 | 1x3 |
| Rambo Explosive Arrow | 150 cash (hidden in the shop) | Up to 3 | 3x1 |

The Rambo Explosive Arrow's vendor row is hidden, so the shop does not list it, even though it has a price. The bow's standard magazine appears in the attachment data as "Combat Bow Standard Mag", with no weapon attached and no stat change. See [Magazines](../attachments/magazines.md).

## Attachments

No attachments are listed for the bow.

## Cost and unlocking

- **Item shop:** 1,350 cash, unlock level 0.
- **Recon role tree:** the Compound Bow unlocks at Recon level 16 for 150,000 cash, together with the Arrow at 0 cost. See [Recon](../progression-and-economy/recon.md).

## Season 2 changes

- Price rose from 800 to 1,350 cash.
- Arrow launch speed fell from 650 m/s to 160 m/s (the bow) and from 642 m/s to 152 m/s (the Broadhead Arrow, as stored).
- Arrows last 14 s in flight instead of 30 s.
- Penetration rose from 0.03 to 0.5. The arrow is also thicker (diameter 0.4 to 0.65) and drags harder.
- The far end of the range falloff curve (1,200 m) went from 20% damage to none.
- Arrows lose damage against Heavy and Super heavy gear (x0.90 and x0.66); Season 1 had no cut.
- The Recon tree cost rose from 125,000 to 150,000 cash.

## See also

- [Grenades and Explosives](../equipment/grenades-and-explosives.md)
- [Armor](../game-mechanics/armor.md)
- [Recon](../progression-and-economy/recon.md)
- [Weapons](../weapons.md)

## Sources

- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md): the bow and arrow rows, price, size and draw time
- [Items Game Feature](../../game-features/Wardogs_GameFeatures_Items_v2.md): the arrow projectile data
- [Explosives](../../game-features/Wardogs_Explosives_v1.md): the Rambo Explosive Arrow blast
- [Weapon Miscellany](../../game-features/Wardogs_WeaponMisc_v1.md): the draw input and release curve
- [Season 2 Changes: Items and Equipment](../../season-2-changes/items-equipment.md)
- [Season 2 Changes: Rewards and Unlocks](../../season-2-changes/rewards-unlocks.md)
- Bow stats asset
