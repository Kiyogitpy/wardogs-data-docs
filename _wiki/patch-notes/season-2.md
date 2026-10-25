---
title: "Season 2 Patch Notes"
parent: "Patch Notes"
description: "The gameplay changes in Season 2 compared with Season 1, grouped by weapons, vehicles, items, modes and progression."
---

# Season 2 Patch Notes

| Season 2 | |
|---|---|
| Update date | 2026-10-15 (Season 2 data) |
| Compared with | Season 1 |
| Scope | Gameplay-relevant changes only |
{: .wiki-infobox }

Season 2 changed the weapons, damage rules, vehicles, items, modes and progression. The notes below cover the changes that affect play. Cosmetic changes, renamed settings, shader and warm-up data, and audio changes are left out. The full lists are on the [Season 2 Changes](../../season-2-changes/all-changes.md) pages, linked at the end of each section.

**How these notes were made.** The game files were exported for Season 1 and for Season 2 and compared asset by asset. Renamed keys, swapped key names, moved files, and shader, audio and visual data were filtered out. The remaining value changes were kept when they affect play, and each was checked against the wiki article for that weapon, vehicle or item, so the names are the ones players see.

## Weapons

- **Base damage for .308 Winchester rounds fell from 60 to 45.** This applies to the FAL, BMR-308, M14, Evo-3 Ultra and MK22.
- **Base damage for 7.62x54 mm rounds fell from 55 to 44.** This applies to the SVD, SV98, Mosin Nagant and PKM.
- **Sniper rifles hit harder on the body.** Their multipliers for the head, neck, upper torso, middle torso and pelvis rose by about a third, and upper arms by a quarter. The sniper head multiplier went from 3.2 to 4.27.
- **Suppression values changed on many weapons.** Several weapons gained a suppression value, and others were adjusted. Examples: MK22 1.6, AMR 50 2.0, SV98 1.5, Mosin Nagant 1.5, Scout Rifle TD 1.5, M249 SAW 1.25, AK74 1.05, SKS 1.1, M4 0.95, PKM 0.9 (up from 0.45), SVD 0.8 (up from 0.4).
- **Aim assist curves were removed.** Sixteen curves for hip-fire and reticle-edge aim assist were removed across assault rifles, LMGs, pistols, shotguns, SMGs and melee.
- **Aim assist pulls and slows at a higher rate.** The pull and slow rates were set to 10 in and 8 out for every class except the RPG-7, which has no aim assist. The sniper reticle area was also widened.
- **Recoil patterns changed on four weapons,** including the SKS and SVD, with many of the pattern points moved. View kick was removed on the BMR-308, SKS and SVD, and rose on the MP5 from 1.1 to 1.15.
- **Sniper rifles cycle faster after a shot.** The time before the SV98 can rechamber fell from 0.3 s to 0.08 s, and the AMR 50's from 0.24 s to 0.2 s.
- **The Super-45 falls off with distance differently.** It gained two falloff points, at 100 m (0.4) and 150 m (0.3).
- **Combat bow changed.** Its launch speed fell from 650 m/s to 160 m/s, arrows last 14 s instead of 30 s, penetration rose from 0.03 to 0.5, and its price rose from 800 to 1350.
- **The MGL-40 fires slower.** Its muzzle velocity went from 100 m/s to 75 m/s.
- **Vendor prices changed.** Some of the largest moves: AK74 down from 1,600 to 800, T-21 up from 600 to 1,200, Super-45 up from 2,600 to 5,600, AMP-9 up from 900 to 1,375, AMR 50 up from 8,800 to 14,800, MP5 up from 1,500 to 1,800, and FAL down from 6,500 to 6,000.
- **Other weapon prices changed.** Deagle from 900 to 750, Galil from 2,200 to 2,000, GGX 18 from 800 to 1,000, MAAWS from 2,600 to 2,400, MGL-40 from 6,000 to 7,500, PKM from 4,500 to 4,100, RPG-7 from 2,000 to 1,800, BMR-308 from 6,000 to 6,250, and Scout Rifle TD from 1,100 to 1,200.
- **Attachment prices changed.** Most muzzle devices and foregrips got cheaper, for example the Birdcage Flash Hider from 900 to 600 and the BMR-308 Flash Hider from 1,280 to 930. The AR Multi-Caliber Suppressor rose from 400 to 1,200.
- **162 weapon and attachment assets were added,** including new barrels, foregrips and animation sets.

Full lists: [Weapons & Ammo changes](../../season-2-changes/weapons-ammo.md).

## Damage and armor

- **Heavy armor and Heavy helmets reduce less.** Reduction fell from 55% to 50%. Super heavy armor and Super heavy helmets fell from 65% to 60%. Light and Medium armor were not changed.
- **Seated vehicle protection changed on the Little Bird family helicopters and the Venom helicopter.** Passengers get half the protection against small and medium arms (from 50% to 25%) and less against high-calibre arms (from 20% to 15%).
- **A new seat rule covers the Z20 Lakota.** It gives 25% against small and medium arms and 15% against high-calibre arms.
- **Vehicle turret weapons do less damage to infantry** on most body parts. The Minigun's upper-torso multiplier fell from 1.3 to 0.57. The artillery and heavy tank turrets' upper-torso multiplier fell from 1.8 to 0.885.
- **Bushes and saplings react to Molotov fire.** A new metal fence type was also added, and larger explosions and larger vehicles can break it.

Full lists: [Damage & Combat Systems changes](../../season-2-changes/damage-combat-systems.md).

## Vehicles

- **Rocket and cannon damage rules were added.** A 125 mm rocket rule was added to 17 vehicle damage tables, and a 20×102 mm cannon rule to five stationary weapons.
- **Several vehicle damage rules changed.** The Humvee's default rule went from -67% to -85%, the Ural's from -65% to -87.5%, and the Havoc's changed from +87.5 to -46.0. Negative amounts reduce damage.
- **More vehicle damage rules changed.** One Little Bird damage rule went from -40% to -69.5%, one Z20 Lakota rule from -40% to -57.25%, the M113 APC SV's from -60% to -84%, and the Flakpanzer Gepard's and L2A6's from -75% to -85%. The Humvee [Minigun] turret went from -71% to -88%, and the Humvee [M249] turret from -69% to -86.5%.
- **Humvee drive split changed.** Front torque share fell from 70% to 40%, and rear rose from 30% to 60%. The Humvee's rear suspension was also re-tuned.
- **Tyre deflate threshold rose from 0.5 to 0.55** on most wheeled vehicles.
- **Handling changed on a few vehicles.** The Dune Buggy's rear brake torque fell from 16,000 to 13,000, and its second rear brake value from 12,000 to 9,000, so its rear brakes are weaker. The suspension rebound damping of the tanks and the M113 APC SV rose from 12,000 to 17,000.
- **Market prices rose on most armed vehicles.** Examples: Havoc 18,000 to 28,000, Humvee [Minigun] 4,500 to 10,000, Humvee [M249] 3,750 to 8,500, AH-6M [Miniguns] 7,000 to 12,000, AH-6R [Rockets] 12,500 to 18,800, Z20 Lakota [Miniguns] 8,000 to 15,000, Flakpanzer Gepard 10,000 to 14,000, L2A6 heavy tank 14,000 to 22,000, Kodiak [M249] 3,750 to 6,750, and Ural Defender 6,000 to 7,200.
- **Emplacement stats changed.** The Talon 9K-SAM reload went from 2.0 s to 5.0 s, and its restock from 50 to 200 ammo supplies. The L81 mortar's windup went from 0.85 s to 2.5 s, and its restock from 75 to 150 ammo supplies.
- **Two new vehicles were added:** the T-72B3 tracked tank and the Wolf-110, a wheeled vehicle with a machine-gun variant.

Full lists: [Vehicles changes](../../season-2-changes/vehicles.md).

## Items and equipment

- **Parachutes open later and from a higher height.** The minimum fall before a parachute can be used rose from 1 m to 4 m. A parachute can now only open at least 10 m above the ground, and takes 2 s to open.
- **Parachute prices changed.** The Basic Parachute rose from 100 to 500, and the Sport Parachute fell from 1,000 to 700.
- **Parachute landing damage reaches its maximum later.** Damage reaches 100 at a fall speed of 17 m/s, up from 11.1 m/s.
- **Medical items and equipment changed in price.** Medical Bag down from 2,000 to 1,800, standard resuscitator down from 500 to 425, Heavy armor up from 2,000 to 2,500, Super heavy armor up from 4,000 to 5,000, Heavy helmet up from 1,500 to 2,000, Super heavy helmet up from 3,000 to 4,500.
- **Optics changed in price.** Infrared rangefinder up from 1,200 to 3,200, rangefinder up from 400 to 1,450, monocular up from 150 to 350, and binoculars up from 75 to 180.
- **Other item prices changed.** Wrench up from 150 to 180, and Crowbar down from 1,100 to 885.
- **Crowbar durability rose from 5,000 to 7,000.**
- **Hammers build less per hit.** A Large Hammer's weak-spot build amount went from 10 to 8, and a Medium Hammer's from 6 to 5.
- **30 mm ammunition stacks to 50 instead of 200.**
- **Buildable costs fell.** Talon 9K-SAM from 1,000 to 650, Vanguard CIWS from 1,500 to 1,200.
- **Other buildable costs rose.** Build Supplies went up for the Indirect Fire Shelter and the Shelter (100 to 200 each), Bunker (100 to 200), Recon Tower (100 to 200), Door (22 to 80), Gate (85 to 200), Bremer Wall (15 to 32), Stingray (150 to 650), and L81 mortar (150 to 600). The Drill Rig went from 2,250 to 2,750, and its fuel values changed: minimum fuel to run from 1,500 to 2,000, maximum fuel from 7,500 to 10,000, and run time per fuel unit from 0.05 to 0.03.
- **Ammo suppression values changed** for most calibres, including 5.56 mm base suppression from 0.12 to 0.3 and 45 ACP from 0.075 to 0.15. Other examples: .308 Winchester from 0.9 to 0.65, .50 cal from 1.0 to 0.75, and .50 AE from 0.5 to 0.32.

Full lists: [Items & Equipment changes](../../season-2-changes/items-equipment.md).

## Modes and rewards

- **Team Offence was added as a new game mode,** with its own challenges and voting and punishment rules. [Hot Potato](../game-modes-and-maps/hot-potato.md) was also added: a pre-lobby mini-game with its own items, switched off by default, not a match mode. The shooting range also gained a tutorial, and Control Zone settings were added for Sniper Showdown and for the Africa and Russia layouts.
- **Cash for spotting and destroying some vehicles changed.** For the L2A6's artillery variant, the Season 1 amounts of 1,500 and 8,000 were replaced by 400 and 1,200. The data does not say which amount is for spotting and which for destroying. Talon 9K-SAM spotting went from 200 to 75, and destroying a Vanguard CIWS went from 1,500 to 725.
- **Spotting rewards fell for more vehicles.** The Flakpanzer Gepard's cash went from 5,000 to 2,100, and the Talon 9K-SAM's from 1,000 to 400. XP for the Mortar and the Talon roughly halved (for example from 125 to 60). The XP reward for spotting an AT Mine and a Claymore doubled, from 2.5 to 5.0. The cash factor for a spotted target killed by enemies fell from 0.5 to 0.25 for players and most vehicles.
- **Spotting pay range is unchanged.** Spotting still pays 15 to 275 cash, and destroying a spotted target 50 to 500.
- **Spotting challenges gained rows.** The calculator grew from 44 to 130 rows, with variant-level rows for each vehicle and new entries for buildables that scale with build progress.
- **Vehicle destroyed rewards cover the new vehicles.** Destroying the T-72B3 pays a base 5,000 cash.
- **Team kill tracking was removed** from the game feature data.

Full lists: [Game Modes & Maps changes](../../season-2-changes/game-modes-maps.md) and [Rewards & Unlocks changes](../../season-2-changes/rewards-unlocks.md).

## Movement

- **Minimum parachute height raised** (see Items and equipment).
- **Both parachutes gained a vertical drag of 1.75.**
- **Sport parachute pull-up drag acceleration fell from 825 to 400.**

Full lists: [Player & Movement changes](../../season-2-changes/player-movement.md).

## Progression

- **Role mastery XP changed for all six roles.** Levels 10 to 100 use the same new values for every role. Level 10 went from 35,000 XP to 25,000 XP, and level 50 from 1,500,000 XP to 1,150,000 XP.
- **Unlock costs changed on 54 items and vehicles.** Some rose sharply: the Humvee (Driver) from 25,000 to 75,000 cash, the Defibrillator (Medic) from 50,000 to 110,000, the AH-6M [Miniguns] (Pilot) from 50,000 to 125,000, and the GGX 17 (Wardog) from 5,000 to 15,000.
- **Level requirements changed on 118 unlocks,** and 50 unlocks were added while 19 were removed.
- **Challenge reward tables changed** for shared and buildable challenges. Destroying a Flakpanzer Gepard pays base cash 10,000 to 3,500, a Vanguard CIWS 3,000 to 1,200, a Talon 9K-SAM 2,000 to 650, and an L2A6 artillery variant 14,000 to 8,000. A Mortar pays 300 to 650. Destroying a Gate pays 500 to 200, and hacking a Forward Operating Base 2,500 to 1,000. Supply crate deploy cash was halved, for example 250 to 125 for a small crate. Some assist rewards are now split between the players who assisted, and buildable XP scales with build progress.

Full lists: [Rewards & Unlocks changes](../../season-2-changes/rewards-unlocks.md).

## See also

- [Health and Damage](../game-mechanics/health-and-damage.md)
- [Armor](../game-mechanics/armor.md)
- [Parachutes and falling](../game-mechanics/movement.md)
- [Spotting](../game-mechanics/spotting.md)

## Sources

- [Season 2 Changes: all changes](../../season-2-changes/all-changes.md)
- [Weapons & Ammo changes](../../season-2-changes/weapons-ammo.md)
- [Damage & Combat Systems changes](../../season-2-changes/damage-combat-systems.md)
- [Vehicles changes](../../season-2-changes/vehicles.md)
- [Items & Equipment changes](../../season-2-changes/items-equipment.md)
- [Game Modes & Maps changes](../../season-2-changes/game-modes-maps.md)
- [Player & Movement changes](../../season-2-changes/player-movement.md)
- [Rewards & Unlocks changes](../../season-2-changes/rewards-unlocks.md)
