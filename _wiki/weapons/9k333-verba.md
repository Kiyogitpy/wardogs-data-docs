---
title: "9K333 Verba"
parent: "Weapons"
group: "Launchers"
description: "The 9K333 Verba launcher: fire rate, damage by body part, range falloff, ammunition, attachments and Season 2 changes."
---

# 9K333 Verba

| 9K333 Verba | |
|---|---|
| ![9K333 Verba]({{ '/assets/img/icons/vendor-weapons/T_UI_Vendor_WEPN_025.png' | relative_url }}){: .wiki-infobox-img } | |
| **General** |  |
| Class | Launcher |
| Caliber | None (explosive) |
| Fire modes | Semi-automatic |
| **Performance** |  |
| Fire rate | 100 rounds/min |
| Muzzle velocity | 20 m/s |
| Effective range | 1000 m |
| Standard magazine | None, the chamber holds 1 (72mm) |
| **Availability** |  |
| Vendor price | 800 |
| Vendor level field | 1 |
| Stored role levels | Support 8 |
| Internal name | Launcher_04 |
{: .wiki-infobox }

The 9K333 Verba is a [launcher](../weapons.md#launchers) in Wardogs that fires explosive rounds rather than bullets. Its fire rate is 100 rounds/min. It fires only while locked on to a target (2 s to lock, 0.25 s delay), and it can lock on to helicopters and the airplane only, so it cannot be used against ground vehicles.

Launchers fire explosive rounds rather than bullets. The muzzle velocity is the launch speed. The rocket has its own thrust after launch, so its speed in flight is higher than this.

## Damage

The damage data pages do not compute body-part damage for launchers. The data treats the shot as an explosion; see [Weapon Damage](../../game-features/Wardogs_WeaponDamage_v1.md).

## Time to kill

Time to kill is not computed for launchers: the data treats the shot as an explosion.

## Recoil and spread

The recoil figures below use current S3 source settings with the historical calculation and omitted-field defaults; current native equivalence is unverified. Spread figures use the exported settings and historical calculation/default assumptions; current native spread behavior remains unverified.

Each bullet leaves the barrel in a random direction inside a cone around the point you aim at. Hip fire uses a wide cone that grows when you move. Aiming down the sights uses a very narrow one. Every shot also pushes the view up and to the side, following the weapon's recoil pattern.

**Spread**

| Situation | Still | Moving at full speed |
|---|---|---|
| Standing, hip fire | 2.0° | 4.0° |
| Crouching, hip fire | 1.5° | 3.0° |
| Prone, hip fire | 1.0° | 2.0° |
| In the air, hip fire | 10.0° | 10.0° |
| Aimed down sights | 0.0286° | 0.0286° |

Cone half-angles in degrees: a bullet can land up to that far from the aim point. At 100 m, standing hip fire has a radius of 3.5 m when still and 7.0 m at full speed; aimed, it is 0.05 m. Half of the shots land within half that radius.

The data leaves the accuracy value out for this weapon. The model assumes the historical default of 1 mrad (a full cone angle; the aimed row is half of it, in degrees).

- The historical spread model has no per-shot bloom or recovery timer. The earlier reader search does not establish their absence from S3.
- The model assumes the historical hip-spread easing time constant of about 0.04 s; the S3 default and consumer are unverified.
- The 10° in-air row uses the historical native default. An omitted S3 field does not verify that default.
- The historical model uses only aimed spread at full aim (blend exactly 1.0) and hip spread while partly aimed. The current branch has not been verified.
- In that model, "full speed" means 4 m/s standing, 2.5 m/s crouching and 0.5 m/s prone; interpolation is linear. These are historical model assumptions.
- The figures are before attachments, which can change spread (see [Attachments](../attachments.md)).

**S3-input recoil model**

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

[Current recoil settings](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Data/DA_Launcher_04_Stats.json).

Archived Season 1 → 2 history (separate from the S3 model above): Season 2 did not change the recoil pattern.

The [historical Weapon Spray Viewer](https://kiyogitpy.github.io/wardogs-data-docs/pipelines/spray-viewer.html) retains Season 1/2 data; it does not show this S3 snapshot.

## Ammunition

Launchers do not use the bullet types on the [Ammunition](../ammunition.md) page.

## Attachments

Slots on this weapon: Muzzle, Sight, Underbarrel. See [Attachments](../attachments.md) for what each part changes.

## Cost and unlocking

- Vendor price: 800. The data pages do not decode the currency, so the price is shown as a plain number.
- Vendor level field: 1; this is distinct from role unlocking.
- Stored role levels: Support 8. These listed prerequisites do not establish every active mode/vendor gate.

## Season 2 changes

The Season 2 changes page lists no changes for this weapon.

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
- [Current role unlock nodes](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/economy.json): stored tree levels, separate from vendor level fields
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): launcher speeds and ranges, magazines, default rate
