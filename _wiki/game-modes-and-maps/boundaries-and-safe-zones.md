---
title: "Boundaries and Safe Zones"
parent: "Game Modes & Maps"
group: "Maps"
description: "Where the play area ends and what happens if you leave it, plus how the spawn safe zones protect you, the spawn-area soccer pitch and the moving practice targets."
---

# Boundaries and Safe Zones

| Boundaries and Safe Zones | |
|---|---|
| **Play area edge** | |
| Edge | A rectangle per map, measured on the ground plane only (no height limit) |
| Warning | "Return to the Combat Area" with a countdown |
| Countdown on foot | 20 s |
| Countdown in a vehicle | 22 s (the game's default; the vehicle files do not change it) |
| When it runs out | The character dies (inferred for vehicles: they are destroyed) |
| Coming back in | The countdown runs down at the same speed |
| **Spawn safe zones** | |
| Shape | A box, one per team per spawn area |
| Size | 480 m, 640 m or 800 m on a side, 480 m tall (inferred) |
| Own team's zone | No damage, no building |
| Enemy team's zone | Counts as out of bounds: the same 20 s countdown |
{: .wiki-infobox }

The play area of each map is a large rectangle that is much bigger than the area where the Control Zone moves. Nothing blocks you from walking to its edge. Instead, a timer decides how long you may stay outside. The spawn safe zones sit well inside that rectangle and protect you from damage while you stand in your own team's zone. Distances on this page assume that the data's distance unit is centimetres, as on the map articles.

## The play area edge

Every map world stores a rectangle called the playable bounds, and switches the out-of-bounds rule on for all four main maps. The rectangle is measured left to right and front to back only. It has no height, so flying higher does not take you out of it.

| Map | Rectangle size | Gap from the zone area to the edge (west / east / south / north) |
|---|---|---|
| [Bakurani](bakurani.md) | 11.0 km by 11.0 km | 4.0 / 3.6 / 4.1 / 3.5 km |
| [Ozeti](ozeti.md) | 8.5 km by 7.8 km | 2.1 / 2.6 / 2.2 / 2.6 km |
| [Zestafona](zestafona.md) | 10.5 km by 9.2 km | 3.4 / 3.7 / 2.3 / 3.7 km |
| [Saburtulo](saburtulo.md) | 13.2 km by 13.2 km | 5.5 / 5.9 / 5.8 / 5.8 km |

The "zone area" here is the box around all the map's named zone regions plus 500 m, as used on the map articles. Saburtulo has no list of zone regions, so its box is a stand-in built from the tower positions and the zone object (inferred), and its gaps are less certain. The rectangle belongs to the world file, so it also applies to the other maps that share the world: [Bakurani Outskirts - Jutari](bakurani-outskirts-jutari.md) uses the same rectangle as Bakurani.

## What happens outside

- **Warning.** When you are outside the rectangle, the screen shows "Return to the Combat Area" in red, with a countdown timer under it. The message is on screen for about 5 seconds each time it appears, and the timer text is part of the on-foot screen and of every vehicle screen. The tactical map also has a picture for the out-of-bounds area (inferred from the names in its files).
- **Countdown.** On foot you have 20 seconds. The game's own default is 10 seconds, but the player character in the data is set to 20.
- **Coming back.** While you are inside the rectangle again, the timer counts down at the same speed it counted up. If you step out a second time, it continues from what is left rather than starting at zero (read from the game code, not timed in play).
- **When it runs out.** The character dies. No damage over time, no health drain and no other penalty was found in the data.
- **Vehicles.** Vehicles run the same check with the same rectangle. The default time limit in the game code is 22 seconds. When it runs out, the game calls something that looks like destroying the vehicle (inferred; the three vehicle files that carry the setting do not change the limit, and the effect was not traced further).
- **Enemy safe zone.** Standing in an enemy team's spawn safe zone counts as being out of bounds. The screen says "HOSTILE SAFE ZONE" and the same countdown runs, so staying there for the full time ends in death.
- **Sniper Showdown.** The mode adds the same out-of-bounds state when you are in neither the Control Zone nor the Hot Zone, so leaving both starts the 20-second countdown. See [Sniper Showdown](sniper-showdown.md).

## What is not at the edge

- **No walls.** The map files hold 218 invisible blocking volumes across the four worlds, but none of them is within 200 m of the rectangle edge. They stand inside the playable area.
- **No kill or pain volumes.** No volume that kills or hurts on contact is placed in the maps.
- **Fall limit.** A world-wide fall limit is set at 1,500 m below the map origin on Bakurani, Ozeti and Zestafona. The ground in the play areas of those three maps lies between about 1,000 m below and 250 m above the origin, so this is only a floor for falling through the world. Saburtulo sets none, so the engine default applies.
- **Height.** No height ceiling was found for infantry, ground vehicles or the fixed-wing aircraft. Helicopters lose lift as they climb. The data lists a rotor efficiency that drops to 0.65 at 200 m and 0.4 at 280 m for the Havoc, to 0.75 at 250 m and 0.45 at 325 m for the MH-6 and AH-6, and to 0.65 at 250 m and 0.4 at 350 m for the Z20 Lakota. That is a soft ceiling (reading from the names; how the efficiency is used between the points was not read).

## Spawn safe zones

Every team spawn area has one safe zone, an invisible box that belongs to that team. Each map has one per team spawn area.

| Map | Safe zones near the team spawn areas | Size of each |
|---|---|---|
| Bakurani | 6 | Three are 640 m by 640 m, three are 480 m by 480 m; all are 480 m tall |
| Ozeti | 3 | 480 m by 480 m, 480 m tall |
| Zestafona | 3 | 480 m by 480 m, 480 m tall |
| Saburtulo | 3 | 800 m by 800 m, 480 m tall |

The box size is the placed scale times the engine's default box size, because the data stores no box size of its own (inferred). Each zone sits 35 to 166 m from its spawn point and lies entirely inside the play rectangle, at least 1 km from the zone area. One Bakurani zone is 166 m from its spawn point, and one Ozeti zone is 155 m away, a little beyond the 150 m radius used on the map articles. Each zone belongs to one team and shows on the map and the minimap.

**What it does**

- **No damage in your own zone.** A player standing in their own team's safe zone takes no damage. The one exception in the code is damage of the vehicle-spawning type, which is the damage a vehicle does when it appears on top of someone (inferred from the name). This is read from the game code, not tested in play.
- **No building.** Structures cannot be placed in a safe zone or within 3 m of one, and mines and explosives cannot be placed in one. See [Building](../building.md).
- **Rewards.** Healing, refuelling and repairing a target in a safe zone earns no reward, and the transport-assist cash has a 0 modifier in a safe zone. Entering your safe zone after a successful logistics run pays a one-off reward (see [King of the Hill challenges](../progression-and-economy/king-of-the-hill-challenges.md)).
- **Spotting.** The binoculars, the monocular and the range finders list the three safe zone states in one of their tag lists. The meaning is not named in the data (inferred: targets standing in a safe zone cannot be spotted).
- **Vehicles.** Vehicles are repaired and refuelled by returning to your team's safe zone or a Forward Operating Base, according to the in-game tip, and the game's refuel code checks for your own safe zone. The data also stores a time that a vehicle may stay out of a safe zone before it is cleaned up when nobody uses it: 90 for the Havoc, 10 for the MH-6 and AH-6, and 30,000 for the stationary weapons (the unit is not named; seconds is inferred, and the code that uses it was not traced).

**What the data does not show**

- **Shooting.** No rule against firing weapons in a safe zone was found. Your own zone protects you, but no check on firing from it exists in the data or in the code that tests for the zone.
- **After you leave.** No protection timer, grace period or lingering effect was found. The protection depends on standing in the zone, so it ends when you leave (reading).
- **Enemies entering.** Apart from the out-of-bounds countdown above, the enemy gets no other penalty in the data.

## Soccer pitch

Most team spawn areas hold a small soccer pitch (15 are placed in the four world files, including some for other maps). The pitch is a box 40 m long, 30 m wide and 10 m high with a goal box at each end. Each goal is 1 m deep, 8 m wide and 3 m tall.

- **A real ball.** A ball sits at the middle of the pitch. If it leaves the pitch box for 3 seconds, it is put back in the middle. After a goal the ball is reset too, with a goal effect and a reset effect.
- **No score.** There is no scoreboard, team assignment or match end.
- **Reward.** The last player to touch the ball before a goal gets 50 points, and the last player who passed it to them gets 25. They are pre-lobby points, the same kind that [Hot Potato](hot-potato.md) pays, which turn into starting Cash when the match begins (cap of 5,000). The pitch is removed when the match starts, so goals cannot score after that. See [Pre-lobby](pre-lobby.md).
- **Challenges.** No challenge or reward row names the pitch.

## Moving practice targets

Each team spawn area holds 3 moving targets (45 are placed in the four world files, including some for other maps). Each target slides between two points, taking 15 to 25 seconds per crossing, and drops when it is hit.

- **Reward.** A hit that is not a melee blow or a fist pays pre-lobby points equal to the damage of the hit, rounded down. A melee hit makes the hit count as failed. Points go to the player who shot, and become starting Cash at match start like the soccer points. The targets are removed when the match starts.
- **Challenges.** No challenge or reward row names the targets.
- **Respawn.** A hit target falls in half a second and pops back up after a delay of 2 seconds.

## See also

- [Maps](maps.md)
- [Building](../building.md), for the placement checks near a safe zone
- [Pre-lobby](pre-lobby.md), for how the points become Cash
- [Hot Potato](hot-potato.md), for how pre-lobby points work
- [Sniper Showdown](sniper-showdown.md), for the out-of-bounds rule in that mode
- [Fuel and refueling](../vehicles/fuel-and-refueling.md)

## Sources

- [Maps and gym data](../../content/Wardogs_Maps_v2.md), section 13
- [Play-area boundaries and safe zone data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-boundaries.json)
- [Placed gameplay actors (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-gameplay-actors.json)
- [Round 68 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round68-boundaries.md)
- [Round 66 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round66-map-actors.md)
