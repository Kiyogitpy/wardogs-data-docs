---
title: "Infantry Combat Guide"
parent: "Guides"
description: "Practical advice for fighting on foot: moving, shooting accurately, armor and time to kill, shooting through cover, suppression, aim assist, and going down and getting revived."
---

# Infantry Combat Guide

This guide covers fighting on foot. Each section gives the practical numbers and links to the mechanics article that explains the rule in full. Where a figure was worked out from the game's code and not tested in play, the guide says so.

## Moving

Your stance sets your speed. Standing is the normal stance. Crouching and going prone are slower.

| Stance | Walk | Sprint | Tactical sprint |
|---|---:|---:|---:|
| Standing | 4.3 m/s | 6.1 m/s | 6.6 m/s |
| Crouched | 2.7 m/s | No sprint | No sprint |
| Prone | 0.8 m/s | No sprint | No sprint |

- Only a standing player can sprint. If you need speed, stand up first.
- Aiming down sights halves your movement speed. Using a medical item also halves it while the item is in use.
- Your gear sets a speed scale. Light gear keeps 95% of normal speed, Medium 87.5%, and Heavy and Super heavy 80%.
- Walking backwards or sideways is 70% of the speed for your stance.

**Starting and stopping.** From a standstill you reach full walking speed in about 0.14 s standing, 0.08 s crouched and 0.04 s prone. Stopping from a standing walk takes about 0.4 s. These times are derived from the movement code and were not timed in play. Friction is the same in every stance, so crouching does not stop you faster.

**Stance changes.** Standing to crouched takes 0.3 s. Crouched to prone takes 0.4 s. Prone to crouched takes 0.5 s. Crouched to standing takes 0.3 s.

**Slow walk.** The slow-walk setting sets your walking speed between a minimum of 0.8 m/s and the top speed for your stance. Slow, Moderate and Fast give about 1.5, 2.2 and 2.9 m/s standing, and about 1.2, 1.6 and 1.9 m/s crouched. Prone barely changes. Sprinting ignores slow walk. These figures are derived from the movement code and were not tested in play.

**Stamina.**

- A plain sprint costs no stamina. After a sprint you wait 0.8 s before sprinting again.
- A tactical sprint drains 20 stamina per second. It needs at least 20% stamina to start, and you wait 0.6 s after it ends. Use it in short bursts.
- Changing stance costs stamina from a pool of 100. Standing costs 20, crouching 30 and going prone 50. The pool refills at 50 per second with no delay, so a few stance changes in a fight rarely empty it.
- A jump costs 50 stamina from a pool of 150. The pool refills at 50 per second.

## Shooting accurately

Two things move your shots. **Spread** sends each shot into a small random cone around the crosshair. **Recoil** kicks the view after each shot, so the next shots start from a new aim point.

**Spread.** Spread depends on your speed. The wiki takes your speed as a share of the full speed for your stance: 4.0 m/s standing, 2.5 m/s crouched and 0.5 m/s prone. The share is capped at 1. Standing still gives 0, and full speed or faster gives the widest cone.

- Every normal walk is at or above those full speeds (4.3, 2.7 and 0.8 m/s). So any normal walk gives the widest hip spread for your stance. A slow walk gives a smaller cone. This follows from the numbers above.
- Aiming down sights removes hip spread completely. Fully aimed, spread is 0.
- Hip spread is in degrees (half-angle), from standing still to full speed:

| Weapon class | Stand | Crouch | Prone |
|---|---:|---:|---:|
| Assault rifle, DMR, LMG, pistol, shotgun | 3 to 6 | 2 to 4 | 1.5 to 3 (rifle), 1 to 2 (others) |
| SMG | 2 to 4 | 1.5 to 3 | 1 to 2 |
| Sniper | 4 to 7 | 3 to 6 | 2 to 4 |

- Standing still, crouching cuts a rifle's hip spread from 3 to 2 degrees. Going prone cuts it to 1.5 degrees.
- A shot fired while airborne uses 10 degrees (half-angle) for every weapon.
- Firing does not add spread. The fifth shot of a burst has the same spread as the first, if your speed and stance do not change.
- Attachments change spread. A mounted bipod is 0.45 times the base spread and an unfolded one 1.15 times. Muzzle devices give 0.88 to 0.99 times. Foregrips give 0.76 to 0.94 times. See [Choosing Attachments](choosing-attachments.md).

**Recoil.** Recoil moves the aim. It does not widen the cone. Correct for it by moving the crosshair back, not by expecting more spread.

**Sway.** In the default camera mode, weapon sway is added to the view, and the bullet leaves along that view. So sway moves your shots, not only the picture. A higher-magnification sight steadies sway more. This comes from the game's code and was not tested in play.

## Damage, armor and time to kill

Each body part has a base multiplier. The head is 1.00, the neck 0.75, the upper torso 1.10, the middle torso 1.00, the lower torso 0.95 and the pelvis 0.90. The thigh and upper arm are 0.60, the lower arm and calf 0.50, and the hand and foot 0.30. Each weapon class has its own figure for each part, so the same hit does different damage with different guns. Use the [Health and Damage](../game-mechanics/health-and-damage.md) page for the full result.

**Headshots and limbs.** The M4 with full metal jacket and no armor shows the gap:

| Hit | Damage per hit | Hits to kill |
|---|---:|---:|
| Head | 65.8 | 2 |
| Upper torso | 27.3 | 4 |
| Thigh or upper arm | 15.1 | 7 |
| Hand or foot | 7.6 | 14 |

Aim high. Head and neck hits matter most, and hands and feet are a poor target.

**Armor.** Vests cover the torso and reduce damage by 30% (Light), 40% (Medium), 50% (Heavy) or 60% (Super heavy). Helmets cover the head and reduce damage by the same four amounts, plus 30% for the Pilot helmet and 55% for the Tank helmet. The Super heavy vest also covers the pelvis and upper arm. The Heavy, Super heavy and Tank helmets also cover the neck. Hands, lower arms, thighs, calves and feet get no armor. A headshot into a vest still does full head damage.

The M4 to the upper torso shows what each vest level costs you:

| Armor | Damage per hit | Hits to kill |
|---|---:|---:|
| None | 27.3 | 4 |
| Light vest | 19.1 | 6 |
| Medium vest | 16.4 | 7 |
| Heavy vest | 13.6 | 8 |
| Super heavy vest | 10.9 | 10 |

**Ammo.** Hollow point is for unarmored targets. Against a Super heavy vest, the M4 does 1.5 with hollow point, 10.9 with full metal jacket and 14.0 with armor-piercing. For the full comparison, see [Choosing Ammo](choosing-ammo.md).

**Teammates.** A bullet that hits a teammate does half damage. A Large Hammer hit does 70% less.

**Time to kill.** The table below is from [Weapon Comparison](../weapons/weapon-comparison.md). It uses upper-torso hits at 100 m with full metal jacket. A Level 3 vest cuts upper-torso damage by 50%, the same figure the armor page gives for a Heavy vest.

| Weapon | Shots, no armor | Time to kill, no armor | Shots, Level 3 vest | Time to kill, Level 3 vest |
|---|---:|---:|---:|---:|
| M4 | 4 | 0.23 s | 8 | 0.53 s |
| M14 | 3 | 0.17 s | 5 | 0.34 s |
| MK22 | 1 | 0.00 s | 2 | 1.30 s |
| Deagle | 2 | 0.22 s | 3 | 0.45 s |

These times assume every shot hits and ignore reload, spread and recoil. Real fights take longer. Damage falls with distance on most weapons, so check [Ballistics](../game-mechanics/ballistics.md) for long shots.

## Shooting through cover

**Flesh never ricochets.** A bullet that hits a person does not bounce off them. Walls, doors and props can stop, bounce or pass a bullet.

**Ricochet chance** depends on the surface material. Here are some common surfaces:

| Surface | Ricochet chance |
|---|---:|
| Ice | 80% |
| Metal | 45% |
| Concrete | 35% |
| Wood | 30% |
| Brick | 25% |
| Plaster | 20% |
| Glass | 10% |
| Snow | 3% |
| Sand, fabric, paper | 2% |

A head-on hit has its chance cut to 8% of the listed value. A hit at 80 to 90 degrees to the surface keeps 92% (both from the game's code, not tested in play).

**Penetration** depends on the ammo:

| Ammo | Penetration |
|---|---:|
| Armor-piercing | 1.8 |
| Armor-piercing tracer | 1.76 |
| Full metal jacket and tracer | 1.0 |
| Hollow point | 0.1 |

**Thickness and angle.** When a bullet hits a solid object, the game checks for an exit within about 2 m. If there is no exit, the bullet cannot pass. A steeper angle makes the surface look thicker, so a shallow hit has to pass more material. The wiki cannot give a thickness for a particular wall, door or prop, because thickness is measured from the object when you shoot.

**Density.** The denser side of a surface counts. Concrete is 8.5, solid metal 7.0, brick 5.2, plaster 3.0, wood 2.56, plastic 1.3 and rubber 0.7. Higher numbers are harder to pass.

**After a pass.** A bullet that passes through leaves slower. It does less damage at its next hit, in proportion to the speed it has left.

**Ricochet direction.** A bounce is not a mirror reflection. The new direction is random within a cone of up to 40 degrees around the surface normal, and most bounces leave steeper than a mirror would send them. This is derived from the game's code.

Tips:

- Armor-piercing is the choice for passing through cover. Hollow point almost never passes through anything.
- Shooting at ice is unreliable, because most bullets bounce.
- Glass rarely bounces a bullet, but a bullet slows after passing through it.

## Suppression

Suppression is a screen effect and camera shake. It does not change your aim, spread, recoil, sway or walking speed. The game's code reads it only for those two effects, and this was not tested in play.

- Each hit near you raises a suppression strength between 0 and 1. Close shots matter more.
- The screen effect uses the same screen layer as damage. It blurs and darkens the view and fades colour. It fades at 0.4 of its rate. The concussive variant fades at 0.1 and lasts 2 s.
- Nearby fire shakes the camera for 0.5 s. Backblast and concussion shake is stronger, and it is followed by a 2 s darkening.
- Heavy helmets cut suppression to a 0.32 multiplier and super-heavy helmets to 0.2. This is read as the share left, and it was not tested in play.
- A Tank Helmet removes suppression entirely while you are a driver or gunner in a tracked vehicle.
- Two Medic skills change suppression, but their values are not known.

How strong the blur looks at a given strength is not known.

## Aim assist

Aim assist pulls your aim toward enemies inside a reticle. It is a pull, not an automatic aim. The wiki's figures are the stored settings, not values checked in play.

- **Pull modes:** All, movement only, look only and off. Each weapon class sets one mode for hip fire and one for aiming down sights.
- **Targets:** up to 8 are counted at once.
- **Range:** assault rifles and LMGs 300 m, SMGs and shotguns 200 m, snipers 400 m and melee 8 m. Pistols have no range set and use the default mode, All. The wiki stores ranges in game units, which it reads as centimetres (inferred).
- **Strength:** the pull and slow rates are 10 in and 8 out, set for every class except the launchers in Season 2. A higher rate reaches full strength sooner (inferred).

**Launchers have none.** The RPG-7, 9K333 Verba, MGL-40 and MAAWS have aim assist off in both modes. Aim them yourself.

**Smoke.** A target inside an M18 Smoke Grenade cloud probably gets no pull. This is a static reading of the code and was not tested in play.

How strong the pull feels in play has not been measured.

## Going down and getting revived

At 0 HP you are downed, not dead. Health stops falling. The bleed-out timer is the only clock. Outside Deathmatch, no health comes back on its own, so you need a revive or a healing item.

- **Bleed-out timer:** starts at 360 s and drains at half speed, so you last about 720 s (12 minutes) unless helped.
- **Giving up:** ends the wait in 1.5 s. Choose it only when no help is coming.
- **Calling for help:** you can call for help once every 5 s.
- **Revive by hand:** a teammate holds for 20 s with no equipment. You return at 10 HP.
- **Defibrillator:** revives instantly to 35 HP after a 4 s charge. It needs a battery. A downed player cannot use one.
- **Resuscitator:** revives to 10 HP. It is a single use, and the whole use takes about 4 s (derived).
- **Medical Bag:** revives to 50 HP and costs 10 durability.
- **Going down again after a revive:** the timer is at least 30 s, which is about 60 s at half drain.

**No Value Kill.** If an enemy revives you with a resuscitator, you get a 60 s effect. Killing you during it pays 1% of the normal cash and no Role XP. Assists on you pay no Role XP, the kill feed shows "No Value Kill", and wagers do not count the kill. The effect does not change your health or movement. Do not count on cash for a player an enemy has just revived.

## See also

- [Movement](../game-mechanics/movement.md)
- [Spread and Recoil](../game-mechanics/spread-and-recoil.md)
- [Health and Damage](../game-mechanics/health-and-damage.md)
- [Armor](../game-mechanics/armor.md)
- [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md)
- [Status Effects](../game-mechanics/status-effects.md)
- [Aim Assist](../game-mechanics/aim-assist.md)
- [Ballistics](../game-mechanics/ballistics.md)
- [Downed and Revive](../game-mechanics/downed-and-revive.md)
- [Weapon Comparison](../weapons/weapon-comparison.md)
- [Choosing Ammo](choosing-ammo.md)
- [Choosing Attachments](choosing-attachments.md)
- [Beginner's Guide](beginners-guide.md)
