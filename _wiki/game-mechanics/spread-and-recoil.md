---
title: "Spread and Recoil"
parent: "Game Mechanics"
description: "How each shot's direction is chosen, the historical model in which aiming down sights removes hip spread, how movement and stance widen the cone, and how recoil moves the aim."
---

# Spread and Recoil

| Spread and recoil | |
|---|---|
| Fully aimed hip spread | Historical CL516586 model: 0; S3 consumer unresolved |
| Spread from firing | No bloom found in the historical examined path; S3 unresolved |
| Spread from moving | Historical model: scales with speed and stance; S3 consumer unresolved |
| Recoil | Historical model: view kick after each shot, separate from hip spread |
| Buckshot | 8 pellets per shell |
{: .wiki-infobox }

In the documented CL516586 shot-direction model, nonzero spread chooses a random direction in a cone around the aim. Cone size depends on aiming, movement and stance; zero hip spread is a separate branch. Recoil moves the view after the shot. Those consumer rules have not been independently re-established for S3.

## Overview

The historical model separates the **spread cone** around the aim from **recoil**, which moves that aim for later shots. The examined historical path did not add spread from firing. This is not evidence that every current S3 firing path lacks bloom.

## How it works

- **Historical ADS branch.** The CL516586 consumer returns zero hip spread only at full aim; partial aim uses the hip-fire contribution. Current S3 branch behavior is unresolved.
- **Moving widens the cone in the historical model.** Hip spread scales with speed compared with a reference speed for the stance. Standing and running make the cone widest, lying prone keeps it narrowest.
- **Saved stance curves differ.** Prone and crouch generally have lower endpoint values; applying them to movement assumes the historical consumer.
- **Air.** The historical CL516586 consumer/default model uses a separate 10-degree airborne half-angle; that default is not reverified for every S3 weapon. That historical airborne branch bypasses the stance and speed multipliers; S3 parity is unresolved.
- **Historical aim-sway path.** In the examined CL516586 default camera mode, the sway of the weapon as you aim is added to the view's rotation, and the bullet leaves along that view. So sway changes where the shot goes, not only what the camera shows. Sway is divided by the sight's magnification, so a higher-magnification sight steadies it (see [Sights and Optics](../attachments/sights-and-optics.md)). No override was found in that historical review; current weapon-mode coverage is unresolved.
- **Historical vehicle-mounted path.** The CL516586 trace eases vehicle spread at about 25 per second and returns zero hip spread at full ADS; plain mounted weapons had no separate contribution in that examined path. Neither the defaults nor those branch rules are verified S3 behavior.
- **Attachments.** Bipods, muzzle devices and foregrips change the spread. Their multipliers are listed below.
- **Historical zeroing model.** The examined consumer computes zero angles at runtime. At each zeroing range it predicts the bullet's drop over that distance and stores the angle that drop implies, in degrees, for each ammunition type (derived from the game's code).
- **Historical recoil ordering.** The examined CL516586 path uses the view before the current kick; earlier kicks affect later shots. Current S3 ordering is unresolved.
- **Shotguns.** Each buckshot shell fires 8 pellets. Each pellet has its own random direction inside a cone, and the pellets all land at a small spread around the aim. Part of the pattern is a tight inner cluster: about 20 percent of pellets on the M500 and 14 percent on the MP43 (derived), rising to 26 and 34 percent on the M500 with the Improved Cylinder and Full Choke.

## Numbers

Current saved spread-curve endpoints are below. Degrees (half-angle), normalized speed, and reference speeds of 4.0/2.5/0.5 m/s follow the historical standing/crouched/prone consumer model; those bindings remain conditional for S3.

| Weapon class | Stand | Crouch | Prone |
|---|---|---|---|
| Assault rifle, DMR, LMG, pistol, shotgun | 3 to 6 | 2 to 4 | 1.5 to 3 (rifle), 1 to 2 (others) |
| SMG | 2 to 4 | 1.5 to 3 | 1 to 2 |
| Sniper | 4 to 7 | 3 to 6 | 2 to 4 |
| Bow | 1 to 2 | 0.5 to 1 | 0.5 |

The PKM uses the sniper values. The historical shot-direction model makes these hip-spread contributions zero at full aim; the current S3 consumer has not been reverified.

The game stores these as one spread curve for each class and stance (29 curves in all, including the mounted machine guns and the stable mount). Each curve is a straight line from input 0 to input 1, and the stored numbers carry no unit. The degree reading above comes from the spread pipeline page, not from this table. In the historical consumer model, the 0 to 1 input is current speed as a share of the reference speed for the stance (4.0 m/s standing, 2.5 m/s crouched, 0.5 m/s prone), capped at 1: 0 when you are still, 1 at full speed or faster. The historical vehicle path uses the first point (input 0); current vehicle consumers are unresolved.

Attachment multipliers on the spread:

| Attachment | Multiplier |
|---|---|
| Bipod, mounted | 0.45 on Grip Pod, SV98, SKS, SVD and Pro Tilt; 1.0 on PKM, M249, Evo-3 Ultra and M14 |
| Bipod, unfolded | 1.15 |
| Muzzle devices | 0.88 to 0.99 |
| Foregrips | 0.76 to 0.94 |

Shotgun pellet spread for the two shotguns: the outer edge of the M500's pellet cone is about 1.6 degrees from the centre, and the MP43's about 1.9 degrees. Both add a random shift to the centre of the pattern, up to 2 degrees on the M500 and 3 degrees on the MP43.

## Tips conditional on the historical consumer model

- **Full ADS:** the historical branch removes hip spread; this advice depends on that branch remaining applicable in S3.
- **Stance in the historical model:** at rest, the current rifle curve endpoints give 3 degrees standing, 2 crouched and 1.5 prone if the historical consumer still applies.
- **Stopping in the historical model:** lower speed selects a smaller cone from the stance curve. The current S3 speed-to-spread binding remains unresolved.
- **Burst spread:** the historical no-bloom model predicts equal cone size on shots 1 and 5 at equal stance and speed. Current S3 firing consumers remain unresolved.
- **Recoil compensation:** the historical model treats view kick separately from cone size; it does not establish every S3 recoil/spread interaction.
- **Check the bipod.** Five mounted bipod effects store spread ×0.45; the PKM, M249, Evo-3 Ultra and M14 effects store ×1.0. Their recoil modifiers still differ.

## Recoil figures

Recoil patterns (the points that set each shot's kick) are different for each weapon. Season 2 changed recoil patterns on four weapons, including the SKS and SVD. Every weapon's recoil and camera-kick values are listed weapon by weapon on [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md).

## Spread in the air

The historical CL516586 path uses an in-air hip-spread value of 10 degrees; current S3 default and consumer parity remain unresolved. The historical review found an explicit 10-degree grenade-launcher value and a branch that skipped the weapon spread multiplier; neither finding is a complete current-weapon census. The historical search found no per-shot bloom setting in the examined path; it does not establish absence across current S3 code.

## See also

- [Ballistics](ballistics.md)
- [Health and Damage](health-and-damage.md)
- [Movement](movement.md)
- [Beginner's Guide](../guides/beginners-guide.md)
- [Weapon attachments](../attachments.md)

## Season 3 announcement

The TCX-SPR has less full-auto climb and less lateral drift. A separate fix makes prone fire use the appropriate recoil rather than standing recoil. No percentage reduction is announced; retained Season 2 spray paths are historical, not current TCX-SPR predictions.

Source: [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). These are developer-announced changes; saved fields and historical models below do not independently verify the current binary consumer.

## Sources

- [Round 41 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-vehicles-explosives.md): the stored spread curve rows per class and stance (unit not published in the curve table)
- [Weapon Spread, Accuracy and Shot Direction](../../pipelines/Wardogs_WeaponSpread_v1.md)
- [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md)
- [Season 2 weapons changes](../../season-2-changes/weapons-ammo.md) (recoil patterns)
- [Round 39 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-weapons.md): air spread, pellet clusters
- [Round 40 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-weapons.md): zero angles measured at run time
- [Round 41 weapon evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round41-weapons.md): sway in the shot direction, zero angles from the predicted drop, and no per-shot bloom field
- [Round 42 weapons evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md): vehicle-mounted gun spread, its easing rate and the zero in aim-down-sights
- [Round 42 vehicles and explosives evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-vehicles-explosives.md): the vehicle weapon spread path
