---
title: "TCX-SPR"
parent: "Weapons"
group: "Marksman rifles"
description: "The TCX-SPR marksman rifle: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# TCX-SPR

| TCX-SPR | |
|---|---|
| **General** |  |
| Class | Marksman rifle |
| Caliber | [7.62x39mm](caliber-7-62x39mm.md) |
| Fire modes | Fully automatic and semi-automatic |
| **Performance** |  |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 700 m/s |
| Effective range | 400 m |
| Standard magazine | TCX-SPR 28 RND Magazine |
| **Availability** |  |
| Vendor price | 3200 |
| Unlock level | 1 |
| Internal name | WEPN_037 |
{: .wiki-infobox }

The TCX-SPR is a marksman rifle chambered in 7.62x39mm. It fires fully automatic and semi-automatic at 800 rounds/min. Its standard magazine is the TCX-SPR 28 RND Magazine.

## Overview

Marksman rifles are the DMR class in the weapon data. Most are semi-automatic rifles.

It takes the bullet types described on the [Ammunition](ammunition.md) page: Standard (FMJ), Flesh Damage (HP), Armor Piercing (AP). Each has a tracer version.

## Stats

| Stat | Value |
|---|---|
| Fire modes | Fully automatic and semi-automatic |
| Fire rate | 800 rounds/min |
| Muzzle velocity | 700 m/s |
| Effective range | 400 m |

## Damage

Figures are for Standard (FMJ) at point blank range, per hit, against a character without armor.

**By body part (no armor)**

| Body part | Damage |
|---|---|
| Head | 70.3 |
| Neck | 52.7 |
| Upper torso | 29.1 |
| Middle torso | 29.0 |
| Upper arm | 16.2 |
| Thigh | 16.2 |

**Armor (torso and head hits)**

| Armor class | Torso | Head |
|---|---|---|
| No armor | 29.1 | 70.3 |
| Light | 20.4 | 49.2 |
| Medium | 17.5 | 42.2 |
| Heavy | 14.6 | 35.2 |
| Super heavy | 11.7 | 28.1 |

**Range falloff (upper torso, no armor)**

| Distance | Damage |
|---|---|
| 0 m | 29.1 |
| 50 m | 29.1 |
| 100 m | 29.1 |
| 200 m | 29.1 |
| 300 m | 29.1 |
| 400 m | 29.1 |
| 600 m | 19.7 |
| 800 m | 13.2 |
| 1000 m | 7.9 |

**Upper torso, no armor, by ammo type**

| Ammo | Damage per hit |
|---|---|
| Standard (FMJ) | 29.1 |
| Flesh Damage (HP) | 58.3 |
| Armor Piercing (AP) | 23.3 |

See [Ammunition](ammunition.md) for how each type does against armor, and [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md) for the full tables.

## Recoil and spread

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 3.0° | 6.0° |
| Crouching, hip fire | 2.0° | 4.0° |
| Prone, hip fire | 1.5° | 3.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.0166° | 0.0166° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 5.2 m when still and 10.5 m at full speed; aimed, it is 0.03 m. Half of the shots land within half that radius.

Accuracy is 0.58 mrad, a full cone angle; the aimed row is half of it, in degrees.

- The data has no per-shot bloom and no recovery timer: nothing found in the spread data makes firing widen the spread, and spread changes only with speed, stance, being in the air and aiming. This comes from reading the game files, not from testing in game.
- Hip spread eases toward its new value with a time constant of about 0.04 s (a native default found by static reading).
- The 10° in-air figure is a native default found by static reading; only the grenade launcher's data sets it, to the same 10°.
- At full aim (aim blend exactly 1.0) hip spread is set to zero, so only the aimed row applies. A partly aimed weapon counts as hip fire.
- "Full speed" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; between still and that speed the hip spread is a straight line.
- The figures are before attachments, which can change spread (see [Attachments](attachments.md)).

**Recoil**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | 30 |
| Kick on the first shot | 1.07° up |
| Climb after 10 shots | 15.9° up |
| Climb after 30 shots | 45.8° up |
| Average climb per shot over 30 shots | 1.53° up |
| Sideways drift after 30 shots | 0.2° right |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 0.85× / 1.00× |
| Default-loadout recoil multiplier, vertical / horizontal | 1 / 1 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. The game turns each authored kick by up to 14° per shot, so the real sideways drift varies from burst to burst. After shot 30 each kick is random inside the post-pattern range.

The Season 1 data has no entry for this weapon, so there is nothing to compare.

To see the whole pattern as a picture, open the [Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) and pick the TCX-SPR in the viewer.

## Ammunition

Ammo types for this weapon: Standard (FMJ), Standard (FMJ) with tracer, Flesh Damage (HP), Flesh Damage (HP) with tracer, Armor Piercing (AP), Armor Piercing (AP) with tracer. See [Ammunition](ammunition.md).

## Attachments

Slots on this weapon: Barrel, Grip, Handguard, Magazine, Sight, Stock, Underbarrel. See [Attachments](attachments.md) for what each part changes.

Default parts: magazine (SIG Spear Standard Mag), grip (Sig Spear Standard Pistol Grip), stock (Sig Spear Standard Stock), barrel (Sig Spear Standard Barrel).

## Cost and unlocking

- Vendor price: 3200. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

The Season 2 changes page lists no changes for this weapon.

## See also

- [Weapons](../weapons.md)
- [Ammunition](ammunition.md)
- [Attachments](attachments.md)
- [Choosing Ammo](../guides/choosing-ammo.md)
- [Ballistics](../game-mechanics/ballistics.md)
- [Health and Damage](../game-mechanics/health-and-damage.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)

## Sources

- [Weapon Shop and Parts](../../game-features/Wardogs_WeaponShop_v1.md): price, unlock level, default magazine
- [Infantry Weapon Stats](../../content/Wardogs_InfantryWeapons_Stats_v1.md): fire rate and fire modes
- [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md): body-part, armor and falloff numbers
- [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md): spread and recoil inputs
- [Weapon Spread pipeline](../../pipelines/Wardogs_WeaponSpread_v1.md): how the aim cone and hip spread are computed
- [Spray Patterns Gallery](../../game-features/Wardogs_SprayPatterns_v1.md): recoil patterns, Season 1 and Season 2
- [weapon-spread-recoil.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-spread-recoil.json): accuracy and hip spread curves
- [spray-patterns.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/spray-patterns.json): recoil pattern points, Season 1 and Season 2
- [Season 2 Changes: Weapons & Ammo](../../season-2-changes/weapons-ammo.md)
- [Tag Display Text](../../content/Wardogs_TagDisplayText_v1.md): caliber and ammo names
- [weapon-loadouts.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-loadouts.json): names, slots and effects
- [weapon-damage.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage.json): body-part and armor damage
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): falloff curves
- [weapon-capacity.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-capacity.json): muzzle speed, effective range, chamber and magazine
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate
