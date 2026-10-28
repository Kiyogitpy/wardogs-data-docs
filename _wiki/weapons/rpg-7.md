---
title: "RPG-7"
parent: "Weapons"
group: "Launchers"
description: "The RPG-7 launcher: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# RPG-7

| RPG-7 | |
|---|---|
| ![RPG-7]({{ '/assets/img/icons/vendor-weapons/T_UI_Vendor_WEPN_022.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** |  |
| Class | Launcher |
| Caliber | None (explosive) |
| Fire modes | Semi-automatic |
| **Performance** |  |
| Fire rate | 100 rounds/min |
| Muzzle velocity | 100 m/s |
| Effective range | 300 m |
| Standard magazine | None, the chamber holds 1 (93mm) |
| **Availability** |  |
| Vendor price | 1800 |
| Unlock level | 1 |
| Internal name | RPG7 |
{: .wiki-infobox }

The RPG-7 is a [launcher](../weapons.md#launchers) in Wardogs that fires explosive rounds rather than bullets. Its fire rate is 100 rounds/min.

Launchers fire explosive rounds rather than bullets.

## Damage

The damage data pages do not compute body-part damage for launchers. The data treats the shot as an explosion; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).

## Time to kill

Time to kill is not computed for launchers: the data treats the shot as an explosion.

## Recoil and spread

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 2.0° | 4.0° |
| Crouching, hip fire | 1.5° | 3.0° |
| Prone, hip fire | 1.0° | 2.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.0859° | 0.0859° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 3.5 m when still and 7.0 m at full speed; aimed, it is 0.15 m. Half of the shots land within half that radius.

Accuracy is 3 mrad, a full cone angle; the aimed row is half of it, in degrees.

- The data has no per-shot bloom and no recovery timer: nothing found in the spread data makes firing widen the spread, and spread changes only with speed, stance, being in the air and aiming. This comes from reading the game files, not from testing in game.
- Hip spread eases toward its new value with a time constant of about 0.04 s (a native default found by static reading).
- The 10° in-air figure is a native default found by static reading; only the grenade launcher's data sets it, to the same 10°.
- At full aim (aim blend exactly 1.0) hip spread is set to zero, so only the aimed row applies. A partly aimed weapon counts as hip fire.
- "Full speed" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; between still and that speed the hip spread is a straight line.
- The figures are before attachments, which can change spread (see [Attachments](../attachments.md)).

**Recoil**

| Measure | Value |
|---|---|
| Shots in the recoil pattern | none, each shot kicks at random |
| Random kick per shot | up 1.00° to 2.00°, sideways -1.00° to 1.00° |
| Climb after 10 shots | 15.0° up |
| Climb after 30 shots | 45.0° up |
| Average climb per shot over 30 shots | 1.50° up |
| Sideways drift after 30 shots | none |
| Pattern resets after | 0.5 s without firing |
| Vertical kick crouching / prone, compared with standing | 1.00× / 1.00× |
| Default-loadout recoil multiplier, vertical / horizontal | 1 / 1 |

Climb and drift figures are computed from the pattern points, before the recoil multiplier. This weapon has no authored pattern, so the climb figures use the middle of its random range.

Season 2 did not change the recoil pattern.

To see the whole pattern as a picture, open the [Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) and pick the RPG-7 in the viewer.

## Ammunition

Launchers do not use the bullet types on the [Ammunition](../ammunition.md) page.

## Attachments

Slots on this weapon: Sight. See [Attachments](../attachments.md) for what each part changes.

## Cost and unlocking

- Vendor price: 1800. The data pages do not decode the currency, so the price is shown as a plain number.
- Unlock level: 1.

## Season 2 changes

- Vendor price: 2,000 to 1,800

## See also

- [Weapons](../weapons.md)
- [Ammunition](../ammunition.md)
- [Attachments](../attachments.md)
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
- [weapon-damage-falloff.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-damage-falloff.json): falloff curves, also used for the time to kill table
- [weapon-capacity.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/weapon-capacity.json): muzzle speed, effective range, chamber and magazine
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate
