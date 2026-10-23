---
title: "Spread and Recoil"
parent: "Game Mechanics"
description: "How each shot's direction is chosen, why aiming down sights removes hip spread, how movement and stance widen the cone, and how recoil moves the aim."
---

# Spread and Recoil

| Spread and recoil | |
|---|---|
| Spread when fully aimed | 0 (no hip spread) |
| Spread from firing | None: firing does not widen the cone |
| Spread from moving | Yes, scales with speed and stance |
| Recoil | Kicks the view after each shot; does not widen the cone |
| Buckshot | 8 pellets per shell |
{: .wiki-infobox }

No shot in Wardogs goes exactly where the crosshair points. Each shot is sent in a random direction inside a small cone around the aim, and the size of that cone depends on how the player is aiming, moving and standing. Recoil is a separate effect: it moves the view after a shot, so the next shots start from a different point.

## Overview

Two things decide where a shot goes. The first is the **spread cone**, which is always centred on the aim point and changes with how you move and aim. The second is **recoil**, which pushes the aim up or sideways after each shot and so changes where the next shots are aimed. Firing does not make the spread grow over a burst, so a long burst does not get wider by itself.

## How it works

- **Aiming down sights removes hip spread.** Once the weapon is fully aimed down the sights, the hip spread is zero. Partly aimed counts as hip fire at full value.
- **Moving widens the cone.** Hip spread scales with your speed compared with a reference speed for your stance. Standing and running make the cone widest, lying prone keeps it narrowest.
- **Stance matters.** Prone and crouch give smaller spread than standing for the same speed.
- **Air.** A shot fired while airborne uses a separate spread value. Its size is not yet known.
- **Attachments.** Bipods, muzzle devices and foregrips change the spread. Their multipliers are listed below.
- **Recoil is applied after the shot.** The bullet leaves along the view as it was before that shot's kick. Earlier kicks have already moved the view, and they are part of the next shot's aim.
- **Shotguns.** Each buckshot shell fires 8 pellets. Each pellet has its own random direction inside a cone, and the pellets all land at a small spread around the aim.

## Numbers

Hip spread in degrees (half-angle), from standing still to full speed. Full speed is the reference speed for the stance: 4.0 m/s standing, 2.5 m/s crouched and 0.5 m/s prone.

| Weapon class | Stand | Crouch | Prone |
|---|---|---|---|
| Assault rifle, DMR, LMG, pistol, shotgun | 3 to 6 | 2 to 4 | 1.5 to 3 (rifle), 1 to 2 (others) |
| SMG | 2 to 4 | 1.5 to 3 | 1 to 2 |
| Sniper | 4 to 7 | 3 to 6 | 2 to 4 |
| Bow | 1 to 2 | 0.5 to 1 | 0.5 |

The PKM uses the sniper values. Fully aimed, all of these are 0.

Attachment multipliers on the spread:

| Attachment | Multiplier |
|---|---|
| Bipod, mounted | 0.45 |
| Bipod, unfolded | 1.15 |
| Muzzle devices | 0.88 to 0.99 |
| Foregrips | 0.76 to 0.94 |

Shotgun pellet spread for the two shotguns in the data: the outer edge of the M500's pellet cone is about 1.6 degrees from the centre, and the MP43's about 1.9 degrees. Both add a random shift to the centre of the pattern, up to 2 degrees on the M500 and 3 degrees on the MP43.

## Tips that follow from the numbers

- **Aim down sights for accuracy.** Aiming removes the hip spread entirely, which is 3 to 7 degrees on a standing player.
- **Crouch or go prone before a long shot.** Standing still, crouching cuts a rifle's hip spread from 3 to 2 degrees, and going prone cuts it to 1.5 degrees.
- **Stopping helps the cone shrink.** Spread depends on your current speed, so a player who stops quickly gets back to the smaller cone.
- **Bursts do not get wider.** Because firing does not add bloom, the 5th shot of a burst has the same spread as the 1st, as long as speed and stance stay the same.
- **Recoil moves the aim, it does not widen the cone.** Compensate for the kick by moving the crosshair back, not by expecting a wider spread.
- **Bipods help a lot.** A mounted bipod cuts spread to 45% of its base.

## Recoil figures

Recoil patterns (the points that set each shot's kick) are different for each weapon. Season 2 changed recoil patterns on four weapons, including the SKS and SVD. Every weapon's recoil and camera-kick values are listed row by row on [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md).

## What is not yet known

- The spread value used while airborne.
- Whether the aim sway changes the centre of the shot.

## See also

- [Ballistics](ballistics.md)
- [Health and Damage](health-and-damage.md)
- [Movement](movement.md)
- [Beginner's Guide](../guides/beginners-guide.md)

## Sources

- [Weapon Spread, Accuracy and Shot Direction](../../pipelines/Wardogs_WeaponSpread_v1.md)
- [Weapon Spread and Recoil Data](../../content/Wardogs_WeaponSpreadRecoilData_v1.md)
- [Season 2 weapons changes](../../season-2-changes/weapons-ammo.md) (recoil patterns)
