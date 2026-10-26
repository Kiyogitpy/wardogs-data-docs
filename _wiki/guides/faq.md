---
title: "Frequently Asked Questions"
parent: "Guides"
description: "Short answers to the questions players ask most about combat, armor, weapons, vehicles, building, modes, money and the AI, each with the number and the article that states it."
---

# Frequently Asked Questions

Short answers to the questions players ask most often. Each answer gives the number from the game data and links to the article that explains it. Where a figure is worked out from the data rather than timed in play, the answer says so, and where the data does not settle a question, the answer says that too.

## Combat and damage

**How much health do I have?** Every player starts with 100 HP. Health does not regenerate outside Deathmatch, so you heal with items and revives ([Health and Damage](../game-mechanics/health-and-damage.md)).

**How many hits kill me?** With the M4 and full metal jacket, an unarmored player dies to 2 headshots or 4 torso hits, 7 to 8 hits to an arm or thigh, and 14 hits to a hand or foot ([Beginner's Guide](beginners-guide.md)).

**Which body part matters most?** The head, then the neck. Hands and feet count the least ([Health and Damage](../game-mechanics/health-and-damage.md)).

**Does a headshot always kill?** Not with every gun. With the M4 it takes two headshots, but the MK22 sniper rifle does 192.0 to the head and 118.8 to the upper torso, so one hit kills an unarmored player in either place ([Health and Damage](../game-mechanics/health-and-damage.md), [MK22](../weapons/mk22.md)).

**Can my teammates hurt me?** Yes. A bullet that hits a teammate does half damage. The damage tables reduce friendly fire only for bullets and the Large Hammer, so grenades, mines, C4 and Molotov fire are not reduced ([Health and Damage](../game-mechanics/health-and-damage.md)).

**Do bullets lose damage at long range?** Yes. Most weapons follow a falloff curve, and many rifles reach 20% of full damage at 1,200 m. A bullet that has slowed also does less damage, and it is removed 10 s after it is fired ([Ballistics](../game-mechanics/ballistics.md)).

**Can bullets go through walls?** Some materials let a bullet through with less damage, and most bullets stop at the first solid surface. Armor-piercing penetrates best (1.8) and hollow point worst (0.1), but the per-material chances are not all known ([Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md)).

**How long does fire hurt me?** Molotov fire lasts 45 s and deals 15 damage every 0.4 s to anyone standing in it, about 37.5 HP per second (derived from those two values) ([Status Effects](../game-mechanics/status-effects.md)).

## Armor and healing

**Does armor cover my legs?** No. Thighs, calves, feet, hands and lower arms are never covered by armor. Only the Super heavy vest also covers the pelvis and upper arm ([Armor](../game-mechanics/armor.md)).

**How much damage does armor block?** Light armor (Level 1) blocks 30%, Medium (Level 2) 40%, Heavy (Level 3) 50% and Super heavy (Level 4) 60%. Vests cover the torso, and helmets cover the head ([Armor](../game-mechanics/armor.md), [Body Armor](../equipment/body-armor.md)).

**Does a helmet cover my neck?** Only the heavier helmets. The Heavy, Super heavy and Tank helmets cover the neck, and the Light and Medium helmets cover the head only ([Armor](../game-mechanics/armor.md)).

**Does armor wear out?** Each vest and helmet has durability. A hit takes durability from it, and the piece breaks at 0. The reduction stays the same through all four durability stages. This is read from the game code and was not confirmed in play ([Armor](../game-mechanics/armor.md)).

**How long does a bandage take?** About 5.2 s to use on yourself, and 4.8 s on a teammate. It restores 35 HP ([Downed and Revive](../game-mechanics/downed-and-revive.md), [Bandage](../equipment/bandage.md)).

**What is the Medical Bag for?** It heals you at 7 HP per second, or a teammate at 10 HP per second, and it can revive a downed player to 50 HP. While a bandage, First Aid Kit, Medical Bag, Adrenaline Pen or resuscitator is in use, your maximum movement speed is halved ([Medical Items](../equipment/medical-items.md), [Downed and Revive](../game-mechanics/downed-and-revive.md)).

**How long does a revive take?** A teammate holding a revive by hand needs 20 s with no equipment, and the revived player comes back at 10 HP. A Defibrillator needs a battery and a 4 s charge and restores 35 HP. The resuscitator takes about 4 s by derivation from the item data, but it has not been timed in play. A player revived by an enemy is a "No Value Kill" for 60 s: killing them pays almost no cash and no Role XP ([Downed and Revive](../game-mechanics/downed-and-revive.md), [Defibrillator](../equipment/defibrillator.md)).

**How long do I have when I am downed?** The bleed-out timer starts at 360 s and drains at half speed, so about 12 minutes unless you are helped. Giving up ends the wait in 1.5 s ([Downed and Revive](../game-mechanics/downed-and-revive.md)).

## Weapons and ammo

**Which ammo should I use on an unarmored player?** Hollow point. Against no armor it does about twice the damage of full metal jacket, so the M4 does 54.5 to the torso against 27.3 ([Choosing Ammo](choosing-ammo.md)).

**When is AP better than FMJ?** On rifles, from Medium armor up. Against a Medium vest the M4 does 16.6 with armor-piercing and 16.4 with full metal jacket, and against a Heavy vest 15.3 against 13.6. Pistols need Heavy armor, and the Deagle passes full metal jacket at Medium ([Choosing Ammo](choosing-ammo.md)).

**Is hollow point any good against armor?** No. Against a Light vest the M4 does 8.1 with hollow point and 19.1 with full metal jacket ([Choosing Ammo](choosing-ammo.md)).

**Do tracer rounds do more damage?** No. A tracer does the same damage as the plain round of the same type ([Choosing Ammo](choosing-ammo.md)).

**Which round does the most damage?** The AMR 50 with hollow point (listed as Flesh Damage) does 415.8 to the upper torso with no armor, the most of the rounds checked. Its full metal jacket round does 207.9 and its armor-piercing round 166.3 ([Choosing Ammo](choosing-ammo.md)).

## Vehicles

**Can rifles destroy a tank?** No. The SPH-2, Flakpanzer Gepard, T-72B3 and L2A6 take 0% damage from rifle rounds. Cannon fire or explosives are needed ([Vehicle Guide](vehicle-guide.md)).

**How many rifle rounds destroy a Humvee?** About 715 to the body, or 129 through the fuel tank. Both counts are derived at point blank with full metal jacket, not measured in play ([Vehicle Guide](vehicle-guide.md)).

**Do flares stop missiles?** They can pull a guided missile off its target. For the 3.5 seconds they burn, a missile that is between the minimum and maximum flare distance (5 to 300 m on the Havoc) aims at a flare point beside the helicopter instead, and gives up its target when it gets within about 100 m of that point. They do not clear a lock. This is read from the game's code, not tested in play ([Countermeasures and Flares](../vehicles/countermeasures-and-flares.md)).

**How do I refuel?** At a Refuel Station inside a Forward Operating Base. The Fast option restores 5% of the tank for 75 cash over 3 s, and the Max option restores up to 100% over 9 s. A Fuel Canister also refuels a vehicle ([Vehicle Guide](vehicle-guide.md), [Refuel and Repair Stations](../building/refuel-and-repair-stations.md)).

**How do I repair a vehicle in the field?** Use a Wrench, which repairs 10 HP per use for 180 cash. A Repair Station's Fast option restores 5% of health for 100 cash, but it only works inside the Forward Operating Base radius ([Vehicle Guide](vehicle-guide.md)).

**Do vehicle seats protect passengers?** Some do. A Havoc seat takes 10% of small and medium arms damage, a Humvee seat 30%, and a Little Bird seat 75% in Season 2. The data gives no seat protection for the Kodiak or the Ural ([Vehicle Guide](vehicle-guide.md), [Seats and Passengers](../vehicles/seats-and-passengers.md)).

**Why do I take damage when I jump out?** Damage depends on your speed when you leave. There is none at 40 km/h or below, 40 at 50 km/h, 85 at 60 km/h and 100 at 75 km/h and above ([Vehicle Guide](vehicle-guide.md), [Movement](../game-mechanics/movement.md)).

## Building

**What is a Forward Operating Base?** The anchor for building. Most structures must be placed inside its radius. It costs 7,500 cash in the shop and has 15,000 HP. Its data lists a Build Supplies cost of 30, but nothing is charged at placement ([Forward Operating Base](../building/forward-operating-base.md)).

**Which hammer builds a Bunker, and how many rockets kill one?** Only the Large Hammer builds a Bunker, for 200 Build Supplies and 134 hits. Rockets do 45% more damage to it, and about 33 120 mm rockets destroy it at point blank. That count is derived from the damage table, not measured in play ([Bunker](../building/bunker.md), [Buildables](../building.md)).

**What does the Drill Rig do?** It is a fuel-powered rig built with the Large Hammer for 2,750 Build Supplies, with 2,500 HP. It runs on Fuel Supplies and pulls the Hot Zone toward it, at 3 m/s by the game's default. The rig's own data lists 5 m/s, which is not confirmed ([Drill Rig](../building/drill-rig.md)).

**Do sandbags stop bullets?** A Sandbag Wall, with 735 HP, takes 15% of bullet damage. It takes 650% more from rockets and 500% more from IEDs ([Buildables](../building.md#damage-by-source), [Sandbag Wall](../building/sandbag-wall.md)).

**Where do I get Build Supplies?** From the Item Shop. Ammo, Fuel, Mechanical and Build Supplies all cost 10 cash for a lot of 50 ([Supplies](../equipment/supplies.md)).

**Can I take down a structure I built?** Yes. A hammer hit on your own structure does 150, 200 or 250 damage with the Small, Medium or Large hammer. The data finds no Build Supplies refund for dismantling ([Buildables](../building.md#repair-and-dismantle)).

## Modes and maps

**How do I win King of the Hill?** Be the first team to 100 points. A point is added every 22 s by default, and there is no time limit ([King of the Hill](../game-modes-and-maps/king-of-the-hill.md)).

**How do I win Deathmatch?** Reach 75 kills or play for 30 minutes, whichever comes first ([Deathmatch](../game-modes-and-maps/deathmatch.md)).

**Does the Hot Zone move?** On the standard maps it is placed at the start and moves about every 25 s. Kills and captures inside it pay more than in the outer zone ([Control Zone](../game-modes-and-maps/control-zone.md)).

**Do dead players help capture a zone?** No. Only a living player adds to a capture, and a critically wounded player adds nothing ([Control Zone](../game-modes-and-maps/control-zone.md)).

**Can I respawn in a PvE mission?** No. Every PvE mission uses the no-respawn rule, so a player who dies stays out for the rest of the mission ([PvE Scenarios](../game-modes-and-maps/pve-scenarios.md)).

**How does Sniper Showdown punish standing still?** If you stand within about 50 m of one spot for 90 s, you are revealed. A marker shows your position for 200 s, and a warning appears at 75 s ([Sniper Showdown](../game-modes-and-maps/sniper-showdown.md)).

**What is Team Offence?** A Season 2 system for teamkills. An offence opens a player ballot, and the players vote to punish, kick or forgive the offender. Each ballot lasts 180 s; then the server removes the voters who have not decided and counts the rest, and the offender is punished only if the punish votes pass half of the total vote weight ([Team Offence](../game-modes-and-maps/team-offence.md)).

## Money and progression

**How much cash do I start with?** You start with 10,000 cash in most modes (3,000 in Strike and Disarm, 2,000 in VIP Escort). In King of the Hill, points earned in the [pre-lobby](../game-modes-and-maps/pre-lobby.md) are paid on top as extra Cash, 1 for 1 up to 5,000, when the match starts. The loading-screen tip says cash carries over between matches, and a server setting, Persistent Progression, switches that on or off ([Currencies](../progression-and-economy/currencies.md)).

**How do I get Gold Bars?** Exchange cash at the Gold Exchange, which unlocks at Wardog level 35 for 150,000 cash. The server sets the rate and it changes over time, so the rate is not in the game files (the exchange table in the files is empty). Gold Bars buy cosmetics only ([Currencies](../progression-and-economy/currencies.md), [Making Money](making-money.md)).

**Can I buy Gold Bars with real money?** The client data has no Gold Bar pack, so it does not show whether they are sold for money ([Currencies](../progression-and-economy/currencies.md)).

**Why is my shop price lower?** Each price is multiplied by every discount that applies. A player at Wardog level 8 or below pays 50% of the price, a first purchase pays 90% (10% off), and a losing faction that trails by 40 points pays 80% (this condition is inferred from the setting's field names). Your faction's signature rifle is free, as read from the setting's name ([Shops](../progression-and-economy/shops.md)).

**Can I get a refund?** Yes. A refund pays 90% of the eligible amount, but it must be claimed within 20 score ticks ([Shops](../progression-and-economy/shops.md)).

**What is the biggest role payout for one action?** Destroying an enemy Havoc pays 6,000 cash for the Pilot role, the top vehicle payout in the role table on Making Money. Destroying an artillery tank also pays a 6,000 base, and the SPH-2 has a separate per-kill session value of 8,000 in Season 2. Destroying an enemy Forward Operating Base pays 2,500 plus up to 7,500 more depending on the supplies it holds, so no single figure is the biggest. A kill from artillery while standing in the open pays 5,000 for the Assault role, and destroying a heavy tank pays 5,000 for the Driver role ([Making Money](making-money.md), [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)).

**What is Intel for?** Passive missions pay 100 to 500 Intel per tier. The data has no shop price, unlock or exchange that uses it ([Currencies](../progression-and-economy/currencies.md), [Passive Missions](../progression-and-economy/passive-missions.md)).

## AI and PvE

**How far away can AI see me?** Sight is set to 2,000 m, but it builds up very slowly with distance. Hearing reaches 1,000 m, and gunfire is heard almost at once out to about 450 m. These timings are worked out from the perception code and were not tested in play ([AI Enemies](../game-modes-and-maps/ai-enemies.md)).

**Are AI soldiers tougher than players?** Their health is the same, 100 HP. Every soldier wears Level 1 Armor and a Level 1 Helmet, which cut damage by 30% to the body and the head ([PvE Guide](pve-guide.md), [AI Enemies](../game-modes-and-maps/ai-enemies.md)).

**How many M4 headshots kill an AI soldier?** Three, because a Level 1 Helmet cuts head damage by 30%. Two headshots give 92.2 damage (derived), which is under its 100 HP ([PvE Guide](pve-guide.md)).

**How many AI soldiers are in Strike and Disarm?** 53 Lonestar soldiers. 27 are on the map at the start, and 26 more arrive as a counter-attack when the laptop hack begins ([Strike and Disarm](../game-modes-and-maps/strike-and-disarm.md)).

**How long does the VIP have before the mission fails?** In VIP Escort the mission fails 10 s after the VIP goes down (reaches the critical state). A revive does not stop that clock, so a downed VIP means a lost mission. If the VIP disconnects, the game picks a new VIP instead ([VIP Escort](../game-modes-and-maps/vip-escort.md), [PvE Guide](pve-guide.md)).

**What does Hunter Killer include?** Its data is not finished. Its map layer holds only text labels and scenery, and it sets no soldiers, objectives, player faction or starting cash, so the game files have no answer for them ([Hunter Killer](../game-modes-and-maps/hunter-killer.md)).

## Sources

- [Health and Damage](../game-mechanics/health-and-damage.md), [Armor](../game-mechanics/armor.md), [Downed and Revive](../game-mechanics/downed-and-revive.md), [Ballistics](../game-mechanics/ballistics.md), [Penetration and Ricochet](../game-mechanics/penetration-and-ricochet.md), [Status Effects](../game-mechanics/status-effects.md), [Movement](../game-mechanics/movement.md)
- [Choosing Ammo](choosing-ammo.md), [Vehicle Guide](vehicle-guide.md), [PvE Guide](pve-guide.md), [Making Money](making-money.md), [Beginner's Guide](beginners-guide.md)
- [Bunker](../building/bunker.md), [Drill Rig](../building/drill-rig.md), [Forward Operating Base](../building/forward-operating-base.md), [Buildables](../building.md), [Supplies](../equipment/supplies.md)
- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md), [Deathmatch](../game-modes-and-maps/deathmatch.md), [Control Zone](../game-modes-and-maps/control-zone.md), [PvE Scenarios](../game-modes-and-maps/pve-scenarios.md), [Sniper Showdown](../game-modes-and-maps/sniper-showdown.md), [Team Offence](../game-modes-and-maps/team-offence.md), [AI Enemies](../game-modes-and-maps/ai-enemies.md), [Strike and Disarm](../game-modes-and-maps/strike-and-disarm.md), [VIP Escort](../game-modes-and-maps/vip-escort.md), [Hunter Killer](../game-modes-and-maps/hunter-killer.md)
- [Currencies](../progression-and-economy/currencies.md), [Shops](../progression-and-economy/shops.md), [Cash and Rewards](../progression-and-economy/cash-and-rewards.md), [Passive Missions](../progression-and-economy/passive-missions.md)
