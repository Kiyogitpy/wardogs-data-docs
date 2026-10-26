---
title: "Pre-lobby"
parent: "Game Modes & Maps"
group: "Game modes"
description: "The waiting time before a King of the Hill match: the ways to earn pre-lobby points, how the points turn into starting Cash, and what ends the wait."
---

# Pre-lobby

| Pre-lobby | |
|---|---|
| What it is | The wait in your team's spawn area before a match starts |
| Where it is used | King of the Hill (the only mode that turns it on in the game files) |
| Points to Cash | 1 point = 1 Cash, paid when the match starts |
| Most you can bank | 5,000 points |
| Free points | 150 when you arrive, then 250 every 60 seconds |
| Ways to earn more | Hot Potato, the soccer pitch, the moving practice targets |
| Minimum time in the lobby to be paid | 15 seconds |
{: .wiki-infobox }

While a match is filling up, players wait in their team's spawn area. The game gives them things to do and counts what they earn as pre-lobby points. When the match starts, the points are paid out as extra starting Cash.

## How points become Cash

- **Rate.** One point is one Cash. There is no multiplier.
- **Timing.** The whole amount is paid in one go at the moment the match starts. It is added to your normal starting Cash, not instead of it (see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)).
- **Cap.** You can bank at most 5,000 points. Anything above that is lost.
- **Discount.** At the same moment you get a first-purchase discount tag, which the economy settings use for a price cut on your first buy (see [Shops](../progression-and-economy/shops.md)).
- **Time in the lobby.** You are only paid if you have been in the lobby for at least 15 seconds when the match starts. Points that would arrive in your first 15 seconds are refused. This is read from the game code, not seen in play.
- **Late arrivals.** A player who joins when the lobby is already full or already declared ready does not get the arrival points and is not paid. A player who joins a match that is already running has no pre-lobby at all.

## Where points come from

| Source | Points |
|---|---|
| Arriving in the lobby | 150, once |
| Waiting | 250 every 60 seconds (only counts if the lobby lasts that long) |
| [Hot Potato](hot-potato.md) pass | 10 times the pass multiplier: 10, 20, 30 and so on |
| Soccer goal | 50 to the last player to touch the ball |
| Soccer assist | 25 to the last player who passed it to the scorer |
| Moving practice target | The damage of your hit, rounded down. Melee blows and fists do not count |

These are the only sources in the game files. The pitch and the targets are described in [Boundaries and Safe Zones](boundaries-and-safe-zones.md). The game's text and sounds for the awards know exactly three reasons: the potato, shooting and soccer.

## How long it lasts

The lobby ends in two steps. First the match waits for enough players: the settings ask for 60 players and give it up to 10 seconds. If that does not fill, a ready-up step of up to 5 seconds needs at least 9 players (see [King of the Hill](king-of-the-hill.md)). How those clocks start was not traced, so the real length of the wait is not known from the game files, and a server owner can set other values.

Points stop being accepted when the lobby is declared ready, or once 60 or more players are in it. After that, new points are refused. Because of this, the 250-points-per-minute award only matters if the wait runs past a minute (inferred).

## What happens at match start

- The soccer pitch, with its ball, and the moving practice targets are removed from the spawn areas. Goals and target hits cannot score once the match has begun.
- The Hot Potato mini-game switches off. Whether a potato you are still holding is taken away was not checked; its fuse ends the chain anyway.
- Your pre-lobby points are paid as Cash (above).
- Nothing in the pre-lobby code moves you, heals you or changes your inventory. What the match itself does to players when it begins was not traced.

## See also

- [Hot Potato](hot-potato.md)
- [Boundaries and Safe Zones](boundaries-and-safe-zones.md), for the soccer pitch and the practice targets
- [King of the Hill](king-of-the-hill.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Shops](../progression-and-economy/shops.md)

## Sources

- [Round 69 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round69-prelobby.md)
- [Round 68 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round68-boundaries.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
