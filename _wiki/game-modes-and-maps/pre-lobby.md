---
title: "Pre-lobby"
parent: "Game Modes & Maps"
group: "Game modes"
description: "The waiting time before a King of the Hill match: the ways to earn pre-lobby points, how the points turn into starting Cash, and what ends the wait."
---

# Pre-lobby

S3 seeding now supplies a few **free unarmed vehicles per team**, and **all vehicles are cleared when the match starts**, according to the [official Season 3 patch notes](https://store.steampowered.com/news/app/1867240/view/688648135317127221). This is an announced change beyond the bounded historical subscriber search below; it does not establish that player inventories are also cleared.

| Pre-lobby | |
|---|---|
| What it is | The wait in your team's spawn area before a match starts |
| Where it is used | King of the Hill (the only mode that turns it on in the game files) |
| Historical points-to-Cash path | CL516586: 1 point = 1 Cash at match start; S3 consumer unverified |
| Stored starting Cash | 10,000 in the current currency table; current initialization/persistence unresolved |
| Historical point cap | 5,000 in the CL516586 analysis |
| Historical arrival/wait awards | CL516586: 150 on arrival, then 250 every 60 seconds |
| Ways to earn more | Hot Potato, the soccer pitch, the moving practice targets |
| Historical payment eligibility | CL516586 trace: 15 seconds; S3 consumer unverified |
{: .wiki-infobox }

While a match is filling up, players wait in their team's spawn area. The game gives them things to do and counts what they earn as pre-lobby points. The CL516586 analysis traced conversion of pre-lobby points into extra Cash at match start; that conversion and its eligibility conditions have not been re-established for S3.

## Historical CL516586 point conversion

- **Rate.** One point is one Cash. There is no multiplier.
- **Timing.** The whole amount is paid in one go at the moment the match starts. It is added to your normal starting Cash, not instead of it (see [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)).
- **Cap.** You can bank at most 5,000 points. Anything above that is lost.
- **Discount.** At the same moment you get a first-purchase discount tag, which the economy settings use for a price cut on your first buy (see [Shops](../progression-and-economy/shops.md)).
- **Time in the lobby.** You are only paid if you have been in the lobby for at least 15 seconds when the match starts. Points that would arrive in your first 15 seconds are refused. This is read from the game code, not seen in play.
- **Late arrivals.** A player who joins when the lobby is already full or already declared ready does not get the arrival points and is not paid. A player who joins a match that is already running has no pre-lobby at all.

## Historical CL516586 point sources

| Source | Points |
|---|---|
| Arriving in the lobby | 150, once |
| Waiting | 250 every 60 seconds (only counts if the lobby lasts that long) |
| [Hot Potato](hot-potato.md) pass | 10 times the pass multiplier: 10, 20, 30 and so on |
| Soccer goal | 50 to the last player to touch the ball |
| Soccer assist | 25 to the last player who passed it to the scorer |
| Moving practice target | The damage of your hit, rounded down. Melee blows and fists do not count |

These are the sources identified by the earlier pre-lobby investigation; that search does not exclude other current producers. The pitch and the targets are described in [Boundaries and Safe Zones](boundaries-and-safe-zones.md). The game's text and sounds for the awards know exactly three reasons: the potato, shooting and soccer.

## Stored wait settings and historical timer behavior

The current config stores two wait stages. In the CL516586 trace, each countdown started only once its condition was met (see [King of the Hill](king-of-the-hill.md)).

1. **Player count.** The match waits until 60 players have been placed on a team. Until then this step has no time limit at all. When the 60th player is on a team, a 10 second countdown starts.
2. **Ready-up.** This step needs at least 9 players and every one of them ready. When that holds, a 5 second countdown starts.

So the wait has no fixed length: it lasts as long as it takes to fill the lobby, plus about 15 seconds of countdown once it is full and ready. A lobby that is already full when the step begins starts its countdown at once. A server owner can set other counts and times. The game's code also has a pause flag on the server that holds the countdown while it is set; what sets it was not found.

Points stop being accepted when the lobby is declared ready, or once 60 or more players are in it. After that, new points are refused. Because the wait for players has no time limit, the 250-points-per-minute award can pay out for as long as the lobby stays open and unfilled; in a lobby that fills in under a minute it never fires.

## Match-start behavior traced for CL516586

- The soccer pitch, with its ball, and the moving practice targets are removed from the spawn areas. Goals and target hits cannot score once the match has begun.
- The Hot Potato mini-game switches off. Whether a potato you are still holding is taken away was not checked; its fuse ends the chain anyway.
- Your pre-lobby points are paid as Cash (above).
- No teleport was found among the CL516586 MatchState.Playing subscribers examined in round 70. That bounded search does not establish whether S3 moves the player.
- The same historical subscriber search found no health restore or inventory clear; it did not cover every callee or establish S3 behavior. Current gear, ammunition and inventory persistence remain unresolved.
- The other things that switch on with the start are the zone and its music, the on-screen match display, refunds and call-for-help requests, which only work once the match is playing. This subscriber inventory does not exclude player changes in untraced callees.

### Starting Cash

The current currency table stores 10,000 Cash, and sanitized game-mode settings store OverrideStartingCash=-1. Neither field establishes current initialization, first-login balance or persistence. CL516586 analysis described mode overrides of 3,000 for Strike and Disarm and 2,000 for VIP Escort, profile-based persistent cash, and pre-lobby awards at match start. Those native consumers and any other S3 starting-Cash producers remain unresolved.

## See also

- [Hot Potato](hot-potato.md)
- [Boundaries and Safe Zones](boundaries-and-safe-zones.md), for the soccer pitch and the practice targets
- [King of the Hill](king-of-the-hill.md)
- [Cash and Rewards](../progression-and-economy/cash-and-rewards.md)
- [Shops](../progression-and-economy/shops.md)

## Sources

- [Round 70 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round70-maps-matchstart.md)
- [Match start data (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/match-start.json)
- [Round 69 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round69-prelobby.md)
- [Round 92 evidence: how the wait clocks start](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round92-modes-economy.md)
- [Round 68 evidence](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round68-boundaries.md)
- [Round 40 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-modes-ai-other.md)
- [Round 39 modes, AI and other gaps (evidence)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round39-modes-ai-other.md)
- [Default game settings (JSON)](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/assets/data/default-game-ini.json)
