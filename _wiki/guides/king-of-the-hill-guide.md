---
title: "King of the Hill Guide"
parent: "Guides"
description: "How to win King of the Hill: the 100 point rule, capturing the zone and its moving Hot Zone, spawn areas and vehicles on the four main maps, and what each zone action pays."
---

# King of the Hill Guide

King of the Hill (KOTH) is the main team mode. Three factions fight over a Control Zone, and the Hot Zone inside it pays more than the rest of the zone. This guide gives the practical numbers for the four main maps: Bakurani, Ozeti, Zestafona and Saburtulo. Each figure comes from the linked wiki article, so check there for the full rules. Kenya has its own article, [Kenya (Africa layout)](../game-modes-and-maps/unnamed-africa-layout.md).

## How a match is won

- The first team to reach 100 points wins. There is no time limit.
- A point is added every 22 seconds. The example server file uses 24 seconds.
- The wiki does not say which actions add points, so the timer is the only point rule it lists.
- The lobby needs 60 players and waits up to 10 seconds for them. If that does not fill, a 5 second ready-up step needs at least 9 players.
- A team may have at most 2 more players than the smallest team. The game's default leaves this lock off, and the example server file turns it on.
- The server sets the player cap, from 60 to 100 players.

See [King of the Hill](../game-modes-and-maps/king-of-the-hill.md) for the full rules.

## Capturing and holding the zone

- Players capture the zone by standing in it with their side.
- Only living players add to a capture. A critically wounded or dead player adds nothing.
- The Hot Zone is a smaller cylinder in the centre of the Control Zone.
- On the four main maps, the Hot Zone is placed at the start and then moves about every 25 s. Its default speed is 1.0, and the speed table runs from 0.75 to 2.0.
- On Bakurani, Ozeti and Zestafona, the Hot Zone moves to a region drawn at random by weight. The region just used gives away half its weight, so it is unlikely to come up again at once.
- The zone can appear in several spots. The server rotation can name one for a map. Without a name, one spot is drawn by weight, and a spot with weight 0 is only used when it is named.
- Players cannot place or deploy items outside a Control Zone. The game shows "location not in a Control Zone".
- The on-screen status shows the zone as waiting to start, contested or controlled.

| Map | Control Zone | Hot Zone | Placements | Zone regions |
|---|---|---|---:|---:|
| Bakurani | 500 m across, 170 m tall | 85 m across, 170 m tall | 3 | 60 |
| Ozeti | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | 55 |
| Zestafona | 500 m across, 500 m tall | 85 m across, 850 m tall | 4 | 56 |
| Saburtulo | 550 m across, 150 m tall | 85 m across, 150 m tall | 4 | Not in the data |

Sources: [Control Zone](../game-modes-and-maps/control-zone.md), [Zone Layouts](../game-modes-and-maps/zone-layouts.md).

## Spawning and vehicles

### Spawn areas

- Each match uses three spawn areas, one per side. Each area has a vehicle deployment board, several vehicle yards and an infantry spawn area.
- A player's first spawn is in their faction's spawn area. The game picks a random start point in that area. If the point is taken, it moves to the next free one.
- The wiki does not confirm which spawn area a player gets on maps other than Bakurani.

| Map (entry) | Lonestar | Valkyra | Manticore |
|---|---|---|---|
| Bakurani (first entry) | Baghi | Khevuli | Chuta |
| Bakurani (second entry) | Sanavi | Rachuri | Tavarshi |
| Ozeti | Granada | Barcelona | Malaga |
| Zestafona | Boston | Austin | Chicago |
| Saburtulo | Kuzminki | Rostokino | Ramenki |

### Deployment boards and vehicle yards

Every entry has 3 deployment boards, one per side.

| Map (entry) | Vehicle yards (ground / air / light) | Vehicle slots |
|---|---|---:|
| Bakurani (first entry) | 13 (7 / 3 / 3) | 67 |
| Bakurani (second entry) | 12 (6 / 3 / 3) | 72 |
| Ozeti | 13 (7 / 3 / 3) | 74 |
| Zestafona | 12 (7 / 2 / 3), plus one extra air yard | 61, plus 7 |
| Saburtulo | 11 (6 / 2 / 3), plus one extra air yard | 68, plus 9 |

The yards for each side:

| Map (entry) | Side | Spawn area | Board | Ground / air / light yards | Vehicle slots |
|---|---|---|---|---:|---:|
| Bakurani (first) | Lonestar | Baghi | Lonestar version | 3 / 1 / 1 | 25 |
| Bakurani (first) | Valkyra | Khevuli | Valkyra version | 1 / 1 / 1 | 21 |
| Bakurani (first) | Manticore | Chuta | Manticore version | 3 / 1 / 1 | 21 |
| Bakurani (second) | Lonestar | Sanavi | Lonestar version | 2 / 1 / 1 | 23 |
| Bakurani (second) | Valkyra | Rachuri | Valkyra version | 2 / 1 / 1 | 25 |
| Bakurani (second) | Manticore | Tavarshi | Manticore version | 2 / 1 / 1 | 24 |
| Ozeti | Lonestar | Granada | Lonestar version | 2 / 1 / 1 | 22 |
| Ozeti | Valkyra | Barcelona | Valkyra version | 2 / 1 / 1 | 25 |
| Ozeti | Manticore | Malaga | Manticore version | 3 / 1 / 1 | 27 |
| Zestafona | Lonestar | Boston | Lonestar version | 2 / 0 / 1 | 15 |
| Zestafona | Valkyra | Austin | Valkyra version | 2 / 1 / 1 | 22 |
| Zestafona | Manticore | Chicago | Manticore version | 3 / 1 / 1 | 24 |
| Saburtulo | Lonestar | Kuzminki | Manticore version | 2 / 0 / 1 | 17 |
| Saburtulo | Valkyra | Rostokino | Valkyra version | 2 / 1 / 1 | 25 |
| Saburtulo | Manticore | Ramenki | Lonestar version | 2 / 1 / 1 | 26 |

The Kuzminki and Ramenki boards look swapped in the data. Which team gets which spawn vehicle in a match is not known. The yards allow vehicle families, not single vehicles, and the data does not say how many vehicles a yard holds.

### Vehicle limits

- A player may own at most 2 spawned vehicles at a time.
- After a player deploys onto a spawn vehicle, the deployment board's cooldown is 600 s. This is the stored value, and its start trigger was not traced.
- The deployment board's built-in respawn timers are 300 s, or 60 s for a losing side. They most likely time the side's spawn vehicle (inferred from their names). The data gives no return time for the other yard vehicles.

For which vehicles to use against which targets, see the [Vehicle Guide](vehicle-guide.md) and the [Anti-Vehicle Guide](anti-vehicle-guide.md).

Sources: [Maps](../game-modes-and-maps/maps.md), [Bakurani](../game-modes-and-maps/bakurani.md), [Ozeti](../game-modes-and-maps/ozeti.md), [Zestafona](../game-modes-and-maps/zestafona.md), [Saburtulo](../game-modes-and-maps/saburtulo.md).

## Building a forward base

The Forward Operating Base (FOB) costs 7,500 cash in the shop and 30 Build Supplies. It has 15,000 HP, is placed from its own item, and has no build time. Most structures must be placed inside its radius. A new FOB cannot be placed within about 42 m of another FOB. Destroying an enemy FOB pays 2,500 cash. The King of the Hill spawn manager has no FOB step.

Read [Forward Operating Base](../building/forward-operating-base.md) for the full figures, and [Building a Base](building-guide.md) for what to build around it.

## Earning in King of the Hill

Zone events pay these base amounts:

| Event | Base cash |
|---|---|
| Control Zone contested, owned or not owned | 150 each |
| Entering the Control Zone (first time in a life) | 100 |
| Hot Zone contested, owned or not owned | 600 each |
| Entering the Hot Zone | 0 |
| Activating the Hot Zone Magnet | 5,000 |
| Capturing a hostile tower | 1,000 |
| Capturing a neutral tower | 250 |
| Spawn vehicle reaching the Control Zone | 3,000 |

- A Hot Zone event pays 600, four times the 150 for a Control Zone event.
- A kill in the Hot Zone counts with a weight of 10. A kill in the Control Zone counts with a weight of 5. A kill in the enemy's own Hot Zone counts with a weight of 4, and in the enemy's own Control Zone with a weight of 2.
- A Hot Zone Magnet, once active, makes kills in the Hot Zone pay the highest multiplier in the game. Capturing towers also counts.
- Each repeat kill on the same player pays 24% less, up to four repeats.
- Revives in a zone are multiplied by 1.2 to 2.0.
- Challenge rewards: a player kill pays 300 cash and 250 Role XP, a defibrillator revive 600 cash and 250 Role XP, and a Bandage heal 200 cash and 80 Role XP. These are base amounts from the challenge table. The cash tables list other bases for the same actions, and the wiki does not know which set a match pays. See [King of the Hill Challenges](../progression-and-economy/king-of-the-hill-challenges.md).
- End of match: the top three factions get a flat 200, 150 and 100 cash. They also get 0.30, 0.25 and 0.20 times the match cash. In Season 2, the Lonestar faction gets an extra 10,000 cash. The other two factions get nothing from that bonus.

Sources: [Cash and Rewards](../progression-and-economy/cash-and-rewards.md), [King of the Hill](../game-modes-and-maps/king-of-the-hill.md).

## Tips by map

### Bakurani

- The Default placement has weight 2, and Farmland and Lumberyard have weight 1 each. When the rotation does not name one, Default is twice as likely.
- Sunflowers House, West Forest Pylon and Hillside Top have weight 5, so the Hot Zone is much more likely to move there.
- In the first entry, the Khevuli (Valkyra) area has one ground yard, while Baghi and Chuta have three each.

### Ozeti

- Farmland has weight 0 and is used only when the rotation names it. Default, Church and River have weight 1 each.
- Of the 55 regions, 54 have weight 1 and only Tower 2 has weight 0. A region just used gives away half its weight, so it is unlikely to come up again at once.
- The Malaga (Manticore) area has a third ground yard. It has the most vehicle slots of the three areas, at 27.

### Zestafona

- The Hot Zone is 850 m tall, against a 500 m tall Control Zone. The data does not say whether that is intended.
- Small Factory has weight 0 and is used only when the rotation names it.
- The Boston (Lonestar) area has no air yard of its own. The Lonestar side uses one extra air yard outside the spawn areas, which the wiki infers belongs to the base map.

### Saburtulo

- Hospital is the only placement drawn at random, since it has weight 1. Bazaar, River and Hillside have weight 0 and are used only when named.
- The wiki has no region list for this map, so where the zone can sit beyond its four placements is not known.
- Besides its three spawn areas, Saburtulo has one more air yard. The map article places it in the Rostokino area and tags it for the Lonestar side.

## See also

- [King of the Hill](../game-modes-and-maps/king-of-the-hill.md)
- [Control Zone](../game-modes-and-maps/control-zone.md)
- [Zone Layouts](../game-modes-and-maps/zone-layouts.md)
- [Maps](../game-modes-and-maps/maps.md)
- [King of the Hill Challenges](../progression-and-economy/king-of-the-hill-challenges.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Forward Operating Base](../building/forward-operating-base.md)
- [Making Money](making-money.md)
- [Vehicle Guide](vehicle-guide.md)
- [Anti-Vehicle Guide](anti-vehicle-guide.md)

## Sources

- [Experiences (KOTH and Sniper Showdown)](../../game-features/Wardogs_GameFeatures_Experiences_v2.md)
- [ControlZone game feature](../../game-features/Wardogs_GameFeatures_ControlZone_v2.md)
- [Vehicle Spawns](../../game-features/Wardogs_VehicleSpawns_v1.md)
- [Mode rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/mode-rules.json)
- [Zone rewards data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-rewards.json)
- [Zone selection rules (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/zone-selection.json)
- [Vehicle spawn data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/vehicle-spawns.json)
