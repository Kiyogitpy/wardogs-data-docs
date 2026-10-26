# Round 69: the pre-lobby, how its points become Cash, and the round 68 open items (R69-RE)

Static analysis only. Nothing was run. Evidence levels: static decompile (the corpus `corpus.sqlite` bodies, the restored exe read with capstone), cooked data read (extractor dumps and the placed-cell dumps of round 68), SDK headers, config (`DefaultGame.ini`). Scripts and raw output are under `E:/Reverse_Engineer/wardogs_analysis/round69_re/` (outside the repository): `q.py` (alias lookup), `fn.py` (function body from the corpus), `xr.py` (rip-relative references), `cellflag.py` (placed pitch and target flag), `f1.txt` to `f6.txt` (bodies of the functions named below), `veh/` (vehicle package searches). Status words follow the round 36 brief: FOUND, NATIVE, SERVER, ABSENT, PROTECTED. Nothing sat behind the protection layer, so there are no PROTECTED rows. Addresses are RVAs (image base 0x140000000).

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Conversion rate | FOUND | 1 point = 1 Cash. At match start the whole pending amount is sent as one Cash award (`Attribute.Meta.Currency.Cash`), no multiplier. It adds to the normal starting Cash; it does not replace it. |
| 1b | Cap | FOUND | Pending points are clamped to 0 to 5,000 on every addition (so at most 5,000 Cash). |
| 1c | When | FOUND | The server pays when the match state `MatchState.Playing` begins. It needs the player to have been in the lobby at least 15 s (see 3c) and the first award to have been granted. |
| 1d | Setting values | FOUND | Native defaults only: first award 150, cap 5,000, periodic 250 every 60 s, join grace 15 s, lobby-full count 60. The Blueprint subclass sets only the discount tag; no config section overrides them. |
| 2a | Sources and amounts | FOUND | First award 150 (once); periodic 250 per 60 s; Hot Potato pass 10 x multiplier; soccer goal 50 and assist 25; practice-target hit = truncated damage. No other writer exists in data or code. |
| 3a | Pre-lobby length | NATIVE / SERVER | The configured waits are 10 s (player count, 60 needed) and 5 s (ready-up, 9 needed). What starts those clocks was not traced, so the real length is not fixed by the client files. |
| 3b | What ends point earning | FOUND | The "all players ready" signal, or the lobby holding 60 or more players. After either, new points are refused. |
| 4 | Reset at match start | FOUND (partial) / NATIVE | The soccer pitch, the practice targets, the Hot Potato components and the seeding component remove themselves at match start. Nothing in these classes resets position, health or inventory. What the match-state change does to the players themselves was not traced. |
| 5a | Vehicle out-of-bounds limit override | ABSENT | The three vehicle Blueprints that carry the component (`B_FWG_01`, `B_SPW`, `B_TNK_01`) leave its settings empty, so the native default 22 s stands. No other vehicle Blueprint carries the component (section 6). |
| 5b | Soccer goals after match start | ABSENT (by construction) | The pitch is removed when the match starts, and the award handler refuses points once the lobby is closed. |
| 5c | Practice target pop-up delay | FOUND | `PopUpDelay` = 2.0 s (native default; the Blueprint and the 45 placed targets do not change it). |

## 1. Conversion to Cash (1a to 1d)

Component: `WDServerSeedingPreLobbyComponent` (native, `ServerSeedingRuntime`), added to every `WDPlayerStateSession` by the `ServerSeeding` game feature as `B_ServerSeedingPreLobbyComponent_C`. The King of the Hill experience lists the `ServerSeeding` feature; the other experiences do not ([round39](round39-modes-ai-other.md)). Raw: `f1.txt`, `f2.txt`, `f3.txt`.

Constructor `0x863D6A0` (defaults, offsets in the component): `+0xE0` first award 150, `+0xE4` cap 5000, `+0xE8` periodic interval float 60.0, `+0xEC` periodic award 250, `+0xF0` float 15.0, `+0xF4` int 60. The runtime state is `+0x118` pending points, `+0x148` "closed" flag and `+0x149` "first award given" flag. The Blueprint subclass `B_ServerSeedingPreLobbyComponent_C` (raw `round39_modes/ss/`) sets only the tag list `Vendor.Discount.FirstPurchase`. A search of the staged `DefaultGame.ini` and the other ini files for seeding, pre-lobby and potato found no override.

Award handler `0x8641460` (called for every award event and for the periodic award): runs only for the component's own player, only when `0x863EB70` is true (the join grace passed, section 3c) and `0x863EAC0` is false (the lobby is not closed, section 3b). Then `pending = clamp(pending + Amount, 0, 5000)`; if the value changed it notifies the client (`WDPreGameLobbyPendingAwardChangedMessage`, a UI message).

First award `0x86422E0`: if the "first award given" flag is clear and the lobby is not closed, it adds the first award (150) the same way, clamped, and sets the flag. It runs when the component starts (`0x863ECC0`) and again from the handler.

Payout `0x8640D40`, reached through `OnMatchStarted` (thunk `0x8642770`): needs the first-award flag, pending greater than 0 and the join grace passed. It builds one currency award with the tag global `0xD36B340`, named by `round68_re/holder.py` as `Attribute.Meta.Currency.Cash`, and the amount equal to the pending value (`+0x118`), sends it to the player's pawn, and adds the Blueprint tag list (`Vendor.Discount.FirstPurchase`) to the player ([round40](round40-modes-ai-other.md) R4). There is no multiplication or division, so the rate is 1:1. The Cash goes in as an award, so it comes on top of the normal starting Cash (10,000 in the economy data; `OverrideStartingCash` is -1 in `DefaultGame.ini`, meaning the currency default).

Trigger: `0x863ECC0` (component start, server only) asks the game state whether the tag global `0xD2D2AC8` (`MatchState.Playing`) is already set. If it is not, it binds `OnMatchStarted` to the message for that tag, binds `OnAllPlayersReady`, grants the first award and arms the periodic timer. If it is already set (a player joining a match in progress) it does none of that, so there is nothing to pay. Evidence: static decompile of `0x863ECC0`.

## 2. Sources of pre-lobby points (2a)

Everything that adds points does so through the `WDPreGameLobbyAwardEvent` message (player state, amount, reason tag) or through the component's own first and periodic awards. The reason tags are `UI.ServerSeeding.RewardReason.Potato`, `.Shooting` and `.Soccer` (and a text key `.Default`); `DA_ServerSeedingEntry` maps each to a line of text and a sound, so these three are the only reasons the interface knows. A search of the executable for references to the three tag strings found no native writer. `B_HotPotatoComponent`, `B_WDSoccerField` and `B_MovingTarget` are the Blueprint writers.

| Source | Amount | Evidence |
|---|---|---|
| First award | 150, once per player, when the lobby component starts | `0x86422E0`, ctor `+0xE0` |
| Periodic award | 250 every 60.0 s while the lobby is open | `0x863EA30` (timer armed in `0x863ECC0` from `+0xE8`) |
| Hot Potato pass | 10 x the pass multiplier (`5 * (multiplier * 2)`), reason Potato; the multiplier starts at 1 and adds 1 per pass | [round39](round39-modes-ai-other.md), `hp/B_HotPotatoComponent.json` |
| Soccer goal | 50 to the last player to touch the ball; 25 to the last assister; reason Soccer | [round68](round68-boundaries.md) |
| Practice target hit | truncated damage of the hit, reason Shooting; melee and fists do not count | [round68](round68-boundaries.md) |

The first award and every event amount pass through the same clamp, so the total can never exceed 5,000. Negative amounts would be clamped at 0 too, but no source writes one ([round65](round65-open-questions.md)).

## 3. Duration (3a to 3c)

3a. The experiences' match states for King of the Hill are `WaitingForWorldLoad`, `WaitingForPlayerCount`, a ready-up step, `Playing_KOTH` and `PostMatch`. `DefaultGame.ini`: player count `MinimumRequiredPlayers` 60 and `MaxTime` 10.0; `ReadyUpKOTH` `MinimumRequiredPlayers` 9 and `MaxTime` 5.0 ([round40](round40-modes-ai-other.md)). The state base class (`BHMatchState`) has `ElapsedTime` (+0x40) and `MaxTime` (+0x44). The place where `MaxTime` is compared with `ElapsedTime` was searched for and not found among the pre-match functions, so how the 10 s and 5 s clocks start (at the state start, or once the minimum count is reached) is NATIVE, not traced. The server owner may set other values (SERVER). Consequence for the awards: with a lobby of 15 s join grace, 10 s and 5 s, the periodic 60 s award can only fire if the lobby lasts that long; this is a reading, not a measurement.

3b. What ends point earning. `OnAllPlayersReady` (thunk `0x8642750`) sets the closed flag (`+0x148`) for the component. The signal comes from the game state's "all players ready" delegate, which the player-count and ready-up match states raise through `0x6D6FFB0` when the number of ready players (players whose faction is not the ignored default faction) reaches the required count (60, or 9 for the ready-up step; a console variable can override it). The closed test `0x863EAC0` is also true when the game state's player count (`PlayerArray` size at `+0x2D8`) is 60 or more. So points are refused from the moment the lobby is full or declared ready. A player who joins when the lobby is already full or closed gets no first award and so no payout. Evidence: static decompile of `0x863EAC0`, `0x8642750`, `0x6D6FFB0`.

3c. Join grace. `0x863EB70` is true only when the server world time is at least the player's `StartTime` (`APlayerState+0x2C4`, the join time in seconds) plus 15.0 (`0x8640600`). Both the award handler and the payout use it. A player who has been in the lobby less than 15 s when the match starts is paid nothing, and points earned in the first 15 s are refused (the first award is added directly, but the payout still waits for the grace). Reading of `0x863EB70`, `0x8640600`; not seen in play.

## 4. What resets at match start (4)

FOUND, all on the server, all from the same pattern: the object subscribes to the message for `MatchState.Playing` when it starts, or acts at once if the state is already playing.

- Soccer pitch (`WDSoccerField`): `0x76FFEF0` (begin play). If its flag at `+0x2E0` is set, it calls `Destroy` on itself when the match is playing, or when the message arrives. The flag's native default is true (`0x76FF990` stores `0x0101` at `+0x2E0`), the Blueprint class and the 15 placed fields do not change it. So the pitch and its ball disappear at match start.
- Practice targets (`WDTarget` and `WDMovingTarget`): `0x6A6F310`, same pattern with the flag at `+0x2F8` (native default false, `0x69F04F0`). All 45 placed `B_MovingTarget_C` set it true (`cellflag.py`), so the targets are destroyed at match start. Their end-of-play handler `0x6A6F590` just drops the subscription.
- Hot Potato: `OnMatchStarted` on `WDHotPotatoComponent` and `WDHotPotatoSpawnComponent` (thunk `0x863BA40`) destroys the component. The component code uses the same "not yet playing" test. Whether a potato item still held is removed from the inventory is not traced (the potato's own explosion path removes it when the fuse ends, [round65](round65-open-questions.md)).
- Server seeding: pays out, then calls the component's base `DestroyComponent` (vtable slot 149 of `UActorComponent`, `0x3CA4210`), reading from the call at the end of `0x8640D40`.
- World radio spawn (Buildables): `0x8610DC0` clears a timer and destroys the component; mentioned because it uses the same hook.

Nothing in these classes sets a player position, health or inventory. Whether the match state itself respawns or heals players at the change to playing was searched for in the pre-match classes only: the Playing tag has about 80 references in the executable (list in `xr_playing.txt`), none of which was followed beyond the objects above. That part is NATIVE, not traced. Players keep the Cash they earned: the payout is a normal award.

## 5. Open items from round 68

- 5b. Soccer goals after match start: the pitch actor destroys itself when the match starts (section 4), so no goal can score after that. ABSENT by construction. Even if a ball existed, the award handler refuses points once the lobby is closed (3b). Round 68's "not traced" is settled.
- 5c. Practice target pop-up delay: `AWDMovingTarget::PopUpDelay` at `+0x30C`, constructor `0x69D5EB0` stores `0x40000000`, which is 2.0. `B_MovingTarget_C` has no override in its class defaults and none of the 45 placed instances sets it (`cellflag.py`). The Blueprint pop-up path waits `PopUpDelay` with a Delay node (bytecode names `PopUpDelay` next to `KismetSystemLibrary:Delay`, twice). `bPopUpHandledExternally` is false by default. So a hit target pops back up after 2.0 s plus its 0.5 s fall (reading).

## 6. Vehicle out-of-bounds limit override (5a)

`UWDVehicleGameplaySystemsComponent` has `OutOfBoundsTimeLimit` at `+0x238` (native default 22.0, constructor store `0x766B2B1`, [round68](round68-boundaries.md)). The extractor `findname` search for the component's object name `VehicleGameplaySystemsComponent` over `Wardogs/Content/Vehicles` and `Wardogs/Plugins/GameFeatures/Vehicles` (which holds the SPW, TNK, WHL and ROT feature folders) matched only `B_FWG_01`, `B_SPW` and `B_TNK_01` (`veh/findname.txt`, `veh/fn_plugins.txt`). The class defaults of the component in those three, dumped in round 40 (`round40_veh/d1/`), have an empty property list: no `OutOfBoundsTimeLimit` and no other override. So the Blueprint override is ABSENT and the vehicle limit is 22 s for these vehicles. For the wheeled and rotary vehicles no pawn Blueprint carrying the component was found by that search, so they also use the native default (reading: a vehicle class that the search could not see would be the exception; `findname` reads the package name table, which holds object names but not unversioned property names, so the check for a set value was done on the dumps, not on the search).

## Reproduce

`python -I fn.py 0x8641460 0x8640D40 0x863ECC0 0x86422E0 0x863EAC0 0x863EB70 0x8640600 0x6D6FFB0 0x76FFEF0 0x6A6F310 0x69D5EB0`; `python -I q.py "%ServerSeedingPreLobby%"`; `python -I xr.py 0xD2D2AC8` (references to the `MatchState.Playing` tag holder); `python -I cellflag.py`; tag holders named with `round68_re/holder.py 0xD2D2AC8 0xD36B340 0xD3724C8` (`MatchState.Playing`, `Attribute.Meta.Currency.Cash`, `MatchState.PreMatch.WaitingForPlayers`).

## Wiki updates

- New `_wiki/game-modes-and-maps/pre-lobby.md`.
- `_wiki/game-modes-and-maps/hot-potato.md`: Rewards paragraph points to the Pre-lobby article; 1:1 conversion and the 15 s grace.
- `_wiki/game-modes-and-maps/boundaries-and-safe-zones.md`: pitch and targets are removed at match start; pop-up delay 2 s; vehicle limit line.
- `_wiki/game-modes-and-maps/king-of-the-hill.md`, `_wiki/progression-and-economy/cash-and-rewards.md`: link to Pre-lobby.
- `docs/evidence/round68-boundaries.md`: open items marked settled.
