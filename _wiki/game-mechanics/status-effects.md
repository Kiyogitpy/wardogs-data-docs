---
title: "Status Effects"
parent: "Game Mechanics"
description: "The conditions a player can feel in Wardogs: downed and bleed-out, burning, suppression, spotting, medical buffs, falls, and movement penalties, with their numbers."
---

# Status Effects

| Status effects | |
|---|---|
| Covers | Downed, bleed-out, burning, suppression, spotting, medical buffs, falls, weight and movement penalties |
| Damage over time | None. Bleeding is the downed timer, not health loss |
| Health regeneration | None outside Deathmatch (none found in the game code) |
{: .wiki-infobox }

A status effect is a temporary condition that changes how a player fights or moves. Some come from being hit, some from items, and some from the gear a player carries. Most are stored as gameplay effects with a multiplier, such as "movement at half speed", and the values in the data page for those effects are the source for the numbers below. Where a trigger or length is not in the data, it is marked as not yet known.

## Effect table

| Effect | Cause | What it does | Duration | Numbers |
|---|---|---|---|---|
| Downed | Health reaches 0 | Cannot fight; waits for a revive | Bleed-out timer | Timer 360 s, drains at 0.5 per second |
| Bleed-out | Downed timer running | Player dies and respawns at Headquarters | Ends when timer hits 0 | At least 30 s after a revive; 1.5 s after giving up |
| Burning | Standing in Molotov fire | Fire damages players; screen goes blurred and dark | Fire lasts 45 s; burning ends on leaving the fire | 15 damage every 0.4 s |
| Suppression | Enemy fire near you | Screen effect; strength set per bullet class, no movement effect found | Screen effect fades at 0.4 of its rate (concussive 0.1, lasts 2 s) | Base values 0.2 to 0.9 by bullet class; heavy helmets 0.32 and super-heavy helmets 0.2 as a suppression multiplier (read as the share left; not tested) |
| Spotted | You spot an enemy | Enemy shows to your team on the mini and tactical maps | Infantry 30 s, kept up to 180 s; vehicles 60 to 90 s; bases up to 3,600 s | Spot on infantry takes 0.5 s; spot marker fades over 3.0 s |
| Adrenaline | Using an Adrenaline Pen | Unlimited tactical sprint, lighter equipment class | 60 s | Camera field of view x1.05 |
| Medical use | Using a medical item | Move at half speed while using it | While using | Speed x0.5 |
| Enox boost | Using Enox | Extra health that drains over time | Until the pool is empty (40 s for a full pool) | Pool of 40 health, loses 5 health every 5 s |
| Revive sprint boost | Reviving, or being revived by, a teammate | Faster sprint | 5 s | Speed x1.2 at skill level 2, x1.4 at level 4 |
| Revived by an enemy | A resuscitator used on a player of the other faction | No effect on the player; killing them pays almost nothing | 60 s | Kill cash x0.01, no Role XP |
| Fall landing | Landing hard | Damage | Once per landing | 0 at input 670, 100 at 875, 200 at 1,080 |
| Landing and action sway | Jump, landing, vault, mantle, stance change, end of tactical sprint | Weapon sway changes briefly | 2 s to 15 s | Jump 2 s, landing 10 s, mantle 10 s, vault 5 s, stance 5 s, tactical sprint end 15 s |
| Heavy load | Equipment weight class | Slower, slower to aim and jump | While equipped | Heavy speed x0.8, super heavy jump x0.65 |
| Aiming | Aiming down sights | Move at half speed | While aiming | Speed x0.5 |
| Ghillie suit | Body suit and headwear both worn | Slower, quicker to aim, more sway | While worn | Aim time x0.8, aim sway x1.15 |
| Barbed wire slow | Standing inside a barbed wire | Movement cut to 7.5% of normal speed | Not set in the data | Speed x0.075 |
| Door breach | Breaching a door | Movement ramps down and back up | 0.8 s | Ramp curve, not a fixed number |
| Tinnitus | Nearby explosions and backblast | Audio only: a low-pass mix | About 1.2 s (1 s hold, 0.1 s fades; derived) | Tank Helmet removes it, per the shop text |

## Downed

When health reaches 0 the player is downed. They cannot fight, and their health does not fall any further. The only clock is the bleed-out timer. Teammates can revive them by hand (a 20 s hold with no equipment) or with a defibrillator, Medical Bag or resuscitator. See [Downed and Revive](downed-and-revive.md) for the revive numbers.

## Bleeding and bleed-out

In Wardogs, "bleeding" means the bleed-out timer. There is no damage over time: the data shows that a downed player loses no health while bleeding out, and no item cures a bleed. The timer starts at 360 s and drains at 0.5 per second in the normal state, so a player lasts about 720 s unless helped. Giving up switches the drain to 240 per second, which ends the wait in about 1.5 s. A player who was revived and goes down again starts with at least 30 s, which lasts about 60 s at the normal drain. When the timer reaches zero the player bleeds out and respawns at Headquarters.

## Burning

Molotov fire creates a fire area that lasts 45 s. A player standing in it takes 15 damage each time the fire ticks, which happens every 0.4 s. That is 37.5 health per second, derived from those two values, while in the fire. A burning screen effect blurs and darkens the view and desaturates the colours over about half a second. The effect ends when the player leaves the fire area. The fire is credited to the player who threw the Molotov, and the damage tables give fire no friendly-fire reduction. So a player's own fire and a teammate's fire read as hurting at full strength (a reading of the tables, not tested in play). Vehicles in the fire lose 5 health per second.

## Suppression

Enemy bullets that pass near a player add suppression. Each weapon has a suppression value and a distance falloff, so close shots matter more. Each bullet class has a suppression value in the game data, from 0.2 for small pistol rounds to 0.9 for 120 mm and larger rounds, and it falls off with distance. The screen effect fades at 0.4 of its rate, and the concussive variant at 0.1, lasting 2 s. No movement effect from suppression was found. The data does list three things that reduce it. Heavy helmets carry a suppression multiplier of 0.32 and super-heavy helmets 0.2, which reads as cutting suppression to 32% and 20% (a reading of the effect data, not tested in play). The Tank Helmet removes it entirely while the wearer is a driver or gunner in a tracked vehicle. Two Medic skills change it (less suppression, and faster healing while suppressed), but their values are not in the data. See [Body Armor](../equipment/body-armor.md) for the helmets.

## Spotted

Spotting an enemy with binoculars shows that enemy to your teammates on the mini and tactical maps and in the world. A spot marker fades over 3.0 s on the spatial tracker, and the on-screen spotting overlay fades 1.0 s after the spot. A spot on infantry takes 0.5 s, and the spot fades over 30 s and is kept up to 180 s. Vehicles stay spotted for 60 to 90 s, and bases and buildings up to 3,600 s. The Recon skills multiply the spotted time and the spotting duration by 1.2 at level 2 and 1.4 at level 4. The data has no separate "marked" state: spotting is the marking. See [Spotting](spotting.md).

## Adrenaline

The Adrenaline Pen heals nothing. It gives unlimited tactical sprint for 60 s and lowers the equipment weight class by one step while active. The camera view widens slightly (x1.05) and that is ignored while the player is downed. A second pen used during the 60 s keeps one stack and restarts the 60 s (derived from the effect's default settings). Each player can carry up to three.

## Medical use

Using any medical item (bandage, First Aid Kit, Medical Bag, Adrenaline Pen, resuscitators) halves movement speed while the item is in use. The data sets no fixed duration for this, so it lasts while the action runs.

## Enox boost

Enox adds 40 health as a decaying pool. Every 5 s the pool loses 5 health, or what is left of it, so a full pool is gone after 40 s. The amount and period are read from the game code; the game was not run to time it.

## Revive sprint boost

After a Medic revives a teammate, the Medic gets a faster sprint and tactical sprint, and the revived teammate gets the same boost. Each lasts 5 s. The speed multiplier depends on the skill level: x1.2 at level 2 and x1.4 at level 4.

## Falling and landing

A hard landing causes damage that rises with fall speed. The data curve gives 0 damage at input 670, 100 at 875 and 200 at 1,080, which reads as fall speeds of 6.7, 8.8 and 10.8 m/s (the unit of this curve is presumed to be centimetres per second, as for the parachute curve). The output is presumed to be health, but this is not checked. Parachute landings use a separate curve that starts at 6.95 m/s and reaches 100 at 17 m/s. A landing also briefly changes weapon sway and dips the weapon, for about 0.6 s.

## Movement sway

Jumping, landing, mantling, vaulting, changing stance and ending a tactical sprint each change weapon sway for a short time. The lengths are listed in the table. The sway changes are multipliers, so the size of the change depends on the player's current weight class.

## Heavy load

Equipment weight class changes movement and aim. Light and medium loads lower speed and regeneration slightly. Heavy and super-heavy loads lower speed (x0.8) and jump height, and lengthen the time to lean and unlean (x1.5). Heavy loads also slow aiming down sights (x1.15 for heavy and x1.17 for super heavy). Lighter tactical vests raise reload and equip speed by 2% to 8%.

## Aiming and the Ghillie suit

Aiming down sights halves movement speed. Wearing a Ghillie suit and Ghillie headwear together makes the player slightly slower (x0.95) but quicker to aim (aim time x0.8), and it adds more weapon sway (x1.15).

## Barbed wire, door breach and tinnitus

Barbed wire has an effect that sets movement to 7.5% of normal speed. It is applied to anyone standing inside a built barbed wire, and it has no set duration of its own (see [Barbed Wire](../building/barbed-wire.md#what-it-does)). A door breach slows movement during a 0.8 s ramp. Tinnitus is an audio state. Nearby explosions and backblast trigger it. It is a low-pass audio mix that holds for about 1 s, with 0.1 s fades, so it lasts about 1.2 s in total (derived). The Tank Helmet removes it, according to the shop text.

## Not yet known

- How the suppression values turn into what a player sees in play; the game was not run.
- Whether a rule outside the damage tables switches friendly fire off for fire.

## See also

- [Downed and Revive](downed-and-revive.md)
- [Health and Damage](health-and-damage.md)
- [Spotting](spotting.md)
- [Movement](movement.md)
- [Medical Items](../equipment/medical-items.md)
- [Body Armor](../equipment/body-armor.md)

## Sources

- [Medical and Healing](../../game-features/Wardogs_Medical_v1.md)
- [Fire, Smoke, Throwing and Mine Triggers](../../game-features/Wardogs_FireAndUtility_v1.md)
- [Spotting game feature](../../game-features/Wardogs_GameFeatures_Spotting_v2.md)
- [Player movement](../../content/Wardogs_PlayerMovement_v1.md)
- [Gameplay Effect Values](../../pipelines/Wardogs_GameplayEffect_Values_v1.md)
- [Gameplay effect values (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/ge-values.json)
- [Spotting, suppression and status data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/medical-status-r39.json)
- [Frontend data tables (in-game tips)](../../content/Wardogs_DataTables_Frontend_v1.md)
- [Item Shop](../../game-features/Wardogs_ItemShop_v1.md)
- [Round 39 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-medical-movement.md): heal timing, skill rows, durability costs and status effects
- [Round 40 medical evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-medical-movement.md): revive health, decay, armour and critical state values
