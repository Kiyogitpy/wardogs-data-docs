---
title: "Hot Zone Magnet Towers"
parent: "Game Modes & Maps"
group: "Maps"
description: "How the numbered towers on the King of the Hill maps are captured, how the secret code works, and how a correct code pulls the Hot Zone to a tower."
---

# Hot Zone Magnet Towers

| Hot Zone Magnet Towers | |
|---|---|
| **General** | |
| Towers per map | Bakurani 5, Ozeti 4, Zestafona 3, Saburtulo 5 |
| Mode | King of the Hill |
| **Capturing** | |
| Capture | Hold the use key for 10 s, within 2.5 m |
| Capturers at once | One player per tower |
| Reward range | 80 m around the tower |
| **The magnet** | |
| Code length | One digit per tower |
| Wrong codes before a lock | 3 |
| Keypad lock | 30 s |
| Hot Zone stays at the tower | 180 s |
| Recharge afterwards | 900 s |
{: .wiki-infobox }

Every King of the Hill map has a few numbered towers near the middle of the play area. A team captures towers to learn a secret code, then types the whole code on a tower keypad. A correct code turns that tower into a magnet: the Hot Zone is pulled to it and stays for a while, and every tower goes on cooldown afterwards. The numbers on this page were read from the game, not timed in play. Where a rule is read from the game's code and not from a fixed table, the text says "inferred".

## Overview

- The towers are numbered. Players see them as "Tower 1", "Tower 2" and so on, and a running magnet shows as "Drill 1 active" and so on on the tower screens and the map.
- Bakurani and Saburtulo have 5 towers, Ozeti 4 and Zestafona 3. Where each one stands is on the map articles: [Bakurani](bakurani.md#where-the-towers-stand), [Ozeti](ozeti.md#where-the-towers-stand), [Zestafona](zestafona.md#where-the-towers-stand) and [Saburtulo](saburtulo.md#where-the-towers-stand).
- The towers are the map's own version of the [Drill Rig](../building/drill-rig.md), which players build with a hammer. Both pull the Hot Zone toward them.

## Capturing a tower

- **How.** Walk up to the tower and hold the use key for 10 seconds, within 2.5 m. The game lists it as a hold, so the capture does not finish if you let go early (inferred from the hold type). Only one player can capture a tower at a time.
- **Who.** A player on any team can capture a tower that their own team does not already hold. The game refuses the capture while that tower is cooling down and while a magnet is running.
- **Neutral and hostile.** A neutral tower belongs to no team. A hostile tower belonged to another team at the moment you took it. The game notes the tower's owner just before the capture takes effect and passes it to the reward, and the reward treats the tower as hostile whenever that owner is any team at all. There is no other test: it does not compare distances, scores or how long the other team held the tower.
- **Reward.** Players on the capturing team who are within 80 m of the tower, and are neither dead nor critically wounded, are paid. The base amounts are in [Hot Zone Magnet Challenges](../progression-and-economy/hot-zone-magnet-challenges.md): 250 cash for a neutral tower and more for a hostile one. If the same player is paid for the same tower again within 180 s of the last payout, each earlier payout in that window cuts the new one by 25 percent, down to nothing at the fifth; the window is renewed by each payout.

## The secret code

- **What it is.** The server picks one random digit from 0 to 9 for each tower when the match starts. The whole code therefore has as many digits as there are towers: 5 on Bakurani, 4 on Ozeti, 3 on Zestafona and 5 on Saburtulo.
- **What a team sees.** A team learns the digit of every tower it holds. On a map with 4 or more towers the tower screen shows the digits the team knows and blanks for the rest. On a map with fewer than 4 towers (Zestafona) it shows nothing until the team holds every tower, and the screen says "All towers required for code" (inferred from the game's code and that screen text).
- **When it changes.** A new code is drawn after each magnet's recharge ends, and every tower goes back to neutral at the same moment (read from the game code; a map-specific override of the reset was not ruled out). The game's code runs the same reset when the match starts.

## Typing the code

- **The keypad.** Each tower has a keypad with the keys 0 to 9, Clear and Enter. Each key press takes a 0.3 s tap, within 2.5 m.
- **Where it works.** The keypad works on a tower that is not locked, not cooling down, and while no magnet runs.
- **Wrong codes.** Three wrong codes on one tower lock that tower's keypad for 30 seconds. After the lock ends the count starts again. The base game sets the lock at 5 s, and the shipped tower sets it to 30 s.

## The magnet

When the whole code is right:

- **Hot Zone.** The Hot Zone moves to that tower at 3 m per second and shrinks to 0.6 of its width and length, which is 36 percent of its area. It stays for 180 s. Walking time adds to how long it stays, as it does for the [Drill Rig](../building/drill-rig.md#what-it-does).
- **Towers.** Every tower switches to the activating team's colour while the magnet runs (inferred).
- **Cooldown.** After the magnet ends, all towers go on a 900 s recharge. The map shows "Cooling down" with a countdown on each tower. Players cannot capture a tower or type a code until the recharge ends.
- **Reward.** The cash table pays 5,000 for activating the magnet. The challenge reward pays 2,500 cash and 500 Role XP to players in range. See [Hot Zone Magnet Challenges](../progression-and-economy/hot-zone-magnet-challenges.md). The game does not say which player the 5,000 goes to; the activator is the likely one.
- **Switching it off.** Towers cannot be switched off early by default (inferred from a switch that is off by default).

## What is not known

- Which player the 5,000 activation cash goes to is not stated.
- The numbers above come from the game's settings. A live server could change them.

## See also

- [Hot Zone Magnet Challenges](../progression-and-economy/hot-zone-magnet-challenges.md)
- [Drill Rig](../building/drill-rig.md)
- [Control Zone](control-zone.md)
- [King of the Hill](king-of-the-hill.md)

## Sources

- [World features: Hot Zone Magnet data](../../game-features/Wardogs_GameFeatures_WorldFeatures_v2.md)
- [Maps and gym data](../../content/Wardogs_Maps_v2.md), section 12
- [Tower positions and map extents (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/map-magnets-extents.json)
- [Round 67 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round67-maps.md)
- [Round 45 evidence: the Hot Zone pull](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round45-b.md)
- [Round 92 evidence: the hostile test, the reset and the repeat payout](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round92-modes-economy.md)
