# Round 68: play-area boundaries, spawn safe zones, soccer pitch and practice targets (R68-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (extractor `dump` of the four world packages, the actor Blueprints and the placed cells), static decompile (the corpus `corpus.sqlite`, the restored exe read with capstone), SDK headers. Method follows rounds 65 to 67 ([round66-map-actors.md](round66-map-actors.md), [round67-maps.md](round67-maps.md)). Scripts and raw output are under `E:/Reverse_Engineer/wardogs_analysis/round68_re/` (outside the repository): `getsz.py` (dump of the cells that hold safe zones, pitches, targets), `sz_an.py`, `sz_map2.py` (safe zone placement against the bounds), `ws.py` (world settings), `tags.py`, `xref.py`, `holder.py`, `dis.py`, `ctor.py` (restored-exe helpers: tag globals, references, constructor stores), `bcsum.py` (Blueprint bytecode summary), `build_json.py` (writes `assets/data/map-boundaries.json`). Status words follow the round 36 brief: FOUND, NATIVE, SERVER, ABSENT, PROTECTED. Nothing sat behind the protection layer in this round, so no PROTECTED rows.

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1a | Play-area rectangle per map | FOUND | `WDWorldSettings.PlayableBoundsExtent` (X and Y only) with `bUseOutOfBounds` true in all four worlds; 11.0 x 11.0, 8.52 x 7.75, 10.5 x 9.2, 13.2 x 13.2 km; the round 67 play box lies 2.1 to 5.9 km inside it. |
| 1b | Out-of-bounds timer and "Return to the Combat Area" | FOUND | Player timer limit 20 s (pawn Blueprint; native default 10 s); the timer runs up while outside the rectangle or while carrying the hostile safe zone tag, counts down at the same rate when back inside; the HUD shows the message (5 s) plus a mm:ss countdown. |
| 1c | Damage or death outside | FOUND (death), ABSENT (damage over time) | No effect drains health. At the limit the server kills the character (calls the death path that sets the Dead vitality tag; the callee body was not followed past that, so "kill" is the reading). Vehicles: same test, native default limit 22 s (Blueprint overrides not read), then a destroy-like call on the vehicle's health component (reading, callee not traced). |
| 1d | Kill volumes, blocking walls at the edge | ABSENT | No `KillZVolume`, pain or boundary actor in the cells. 218 `BlockingVolume`s exist but none lies within 200 m of the rectangle edge. World `KillZ` is -1,500 m in three worlds (terrain in the play boxes lies at -991 to +251 m); Saburtulo sets none. |
| 1e | Height ceiling for vehicles and aircraft | ABSENT (hard); FOUND (soft) | The out-of-bounds test is 2D, so there is no ceiling. Helicopters lose rotor efficiency with altitude (Havoc 40 m full, 200 m 0.65, 280 m 0.40; MH-6 and AH-6 75, 250 m 0.75, 325 m 0.45; Z20 50, 250 m 0.65, 350 m 0.40). The fixed-wing data holds no altitude limit. |
| 2a | Safe zone size and shape | FOUND (size inferred) | Box trigger (`B_SafeZone_C`, parent `WDSafeZoneVolume`), one per faction per spawn area. Placed scale 750 (480 m cube), 1000 (640 x 640 x 480 m, three in Bakurani) or 1250 (800 x 800 x 480 m, Saburtulo). The box extent is not stored, so the engine default half extent of 32 cm times scale is used (inferred). |
| 2b | Damage immunity | FOUND (static decompile, Derived) | A character standing in its own faction's safe zone takes no damage, unless the damage carries the type `Meta.Damage.DamageType.VehicleSpawning`. |
| 2c | No shooting | ABSENT | No weapon or fire check on the safe zone tags in data or in the 10 native callers of the own-safe-zone test. |
| 2d | No building | FOUND (known) | `B_SafeZonePlacementCondition` (3 m margin, or standing in one). Already on the building articles. |
| 2e | Vehicle rules | FOUND (partial) | Own-safe-zone test is used by the refuel interaction context and the damage path; the HUD tip says vehicles are repaired and refuelled by returning to the faction's safe zone. `InactivityLifetimeOutSafeZone` (Havoc 90, MH-6 and AH-6 10, stationary weapons 30,000) is stored; meaning of the unit and the consumer not traced. |
| 2f | Protection after leaving | ABSENT | No timer, grace period or lingering effect in the safe zone class (no effects arrays set), the tags, or the damage gate. The gate reads the tag, so protection ends when the tag is removed on exit (reading). |
| 2g | Enemy safe zone | FOUND | The other factions get `State.Location.SafeZone.Hostile` ("HOSTILE SAFE ZONE"), which the out-of-bounds timer counts as out of bounds: 20 s warning countdown, then death. |
| 2h | Other effects of the tags | FOUND | Heal (stim), refuel and repair rewards are 0 when the target is in a safe zone; transport-assist cash has a 0 modifier; observation items list the three safe zone tags in one tag list (meaning not named, inferred as "cannot spot"); a safe zone camera actor accompanies each zone. |
| 3a | Soccer pitch | FOUND | Real ball, goals, no scoreboard. Goal pays 50 pre-lobby points to the last toucher and 25 to the last assister (reason Soccer). Ball resets 3.0 s after leaving the pitch box or after a goal. |
| 3b | Moving practice targets | FOUND | Pay the truncated damage of each hit as pre-lobby points (reason Shooting), except melee and fists. |
| 3c | Challenges for targets or pitch | ABSENT | No challenge row, tag or session event names the pitch or the targets. |

## 1. Boundary rectangle (1a)

`AWDWorldSettings` (SDK `WDGame_classes.hpp` line 37638): `bUseOutOfBounds` at +0x6BC, `PlayableBoundsExtent` (`FBox2D`) at +0x6C0, `SeaLevelZ_CM`, `WorldInformation`. Read from the `WDWorldSettings` export of `Content/Maps/Worlds/<World>/<World>` (raw `w/<World>.json`, summary `worldsettings.json`). All values in cm.

| World (map) | Min X, Y | Max X, Y | bUseOutOfBounds | KillZ |
|---|---|---|---|---|
| Kavkazi (Bakurani) | -1,400,000, -1,700,000 | -300,000, -600,000 | true | -150,000 |
| Europe (Ozeti) | -1,042,343.4, -975,825.06 | -190,525.48, -201,000 | true | -150,000 |
| NorthAmerica (Zestafona) | -620,000, -600,000 | 430,000, 320,000 | true | -150,000 |
| Russia (Saburtulo) | -660,000, -660,000 | 660,000, 660,000 | true | not set |

The rectangle is a property of the world file, so it applies to every map that loads that world (Kavkazi also serves Jutari, Mindori and Tevza; the Jutari zone spot at about (-6,727, -11,171) m lies inside it). The Europe world also holds one `B_MapBounds_C` (spline actor with a material parameter collection, `WDMapBoundsActor`), a map-drawing helper; the other worlds have none. The tactical map widget has an out-of-bounds image, size and position binding (`W_TacticalMap`, `MI_UI_OutOfBounds`), so the map shades the area outside the rectangle (reading from the names).

Margins from the round 67 play box (zone regions plus 500 m; Saburtulo has a stand-in box) to the rectangle, W / E / S / N in m: Bakurani 4,033 / 3,634 / 4,075 / 3,477; Ozeti 2,146 / 2,571 / 2,174 / 2,628; Zestafona 3,370 / 3,670 / 2,272 / 3,682; Saburtulo 5,540 / 5,913 / 5,767 / 5,784. Every main-map safe zone centre lies inside the rectangle.

## 2. Timer and consequence (1b, 1c)

Character tick helper `0x6E78410` (reads `+0x830 CurrentOutOfBoundsTime` and `+0x9D8 OutOfBoundsTimeLimit` of `AWDMoverCharacter`; `+0x170` is the net role, 3 = authority):

1. World settings object found, `bUseOutOfBounds` read (`0x6C051F0`), rectangle taken from `+0x6C0` (`0x5360B60`).
2. The character's actor position (X, Y) is tested against the rectangle. Outside, or the ability system holding tag global `0xD36B8F0` (named by `holder.py` as `State.Location.SafeZone.Hostile`), sets "out".
3. On the authority copy, the tag global `0xD36B910` (`State.Location.OutOfBounds`) is added or removed (count +1 or -1) when the state changes.
4. Out: timer += delta; on the authority copy, when timer >= limit the helper `0x6E71400(char, 1, 0)` runs (it is the death path: it sets `State.Player.Vitality.Dead`, global `0xD36B808`) and the timer is reset to 0. In: if timer > 0 it counts down by delta and is zeroed when it goes below 0.

Limit values: native default 10.0 (constructor `0x6E67160`, store `0x6E67588`, [round17](round17-native-defaults.md)); `B_WDMoverPlayerCharacter` CDO 20.0 ([round40](round40-medical-movement.md) row 28), which is the pawn in play. HUD: `State.Location.OutOfBounds` in `DA_LocationContext`: "Return to the Combat Area", `bPermanent` false, `DisplayLength` 5.0, priority 127. `W_OutOfBoundsWarning` (view model `WDUIOutOfBoundsWarningViewModel`: `TimerText`, `bWantsToBeVisible`) shows the same text in red over a countdown text `00:00`. It is part of the on-foot HUD and all vehicle HUDs (`UI.HUD.Element.OutOfBounds`).

Vehicle tick `0x7687BB0` (`UWDVehicleGameplaySystemsComponent`, `+0x238 OutOfBoundsTimeLimit`, `+0x250 CurrentOutOfBoundsTime`): the same rectangle and hostile-tag test on the vehicle's owner ability system (`+1936`), same up and down counting, and at the limit `0x7674AE0`, which calls `0x1453288B0(health component (+1944), 0, instigator)`: a destroy-like call (reading; not traced). The limit is a constructor default (`mov dword ptr [rdi+0x238], 0x41B00000` at `0x766B2B1`, 22.0). The vehicle Blueprint dumps are not in the data folder, so a Blueprint override was not checked (NATIVE).

SERVER: both kill calls run only where the actor's net role is authority.

## 3. Kill volumes, edge walls, ceiling (1d, 1e)

- Classes searched in the 46,304 actor records of `act2_*.jsonl` and in the SDK: `KillZVolume` (engine class exists, no placed instance), `PainCausingVolume`, `WDMapBoundsActor` (one, Europe), `BlockingVolume` (Kavkazi 113, NorthAmerica 76, Russia 24, Europe 5), `WDAITetherVolume` (1), `BHServerStreamingVolume` (2), `B_FlyThroughTrigger_C` (9 / 16 / 17 / 0), `WDSpawnVolume`, `TriggerBox`. A script counted each against the rectangle: none of the blocking volumes lies within 200 m of an edge; they stand in the playable area.
- `KillZ` is -150,000 cm in Europe, Kavkazi and NorthAmerica; Russia has no value in its world settings.
- No height limit appears in the out-of-bounds code (X and Y only). Rotary flight assets (`BHRotaryFlightDataAsset`): `LowAltitude_m`, `HighAltitude_m`, `MaxAltitude_m`, `HighAltitudeRotorEfficiency`, `MaxAltitudeRotorEfficiency`: ROT_02 40 / 200 / 280, 0.65, 0.4; ROT_03 75 / 250 / 325, 0.75, 0.45; ROT_04 50 / 250 / 350, 0.65, 0.4. They describe a falling lift efficiency (reading from the names; the curve between the points was not read). Fixed wing `FWG_01`: no altitude field.

## 4. Safe zone (2a to 2h)

`B_SafeZone_C` CDO (raw `sz/B_SafeZone.json`): `TagsToApply` State.Location.SafeZone.Alpha (instances override it for Bravo and Charlie, the Alpha instances keep the default), `HostileTagsToApply` State.Location.SafeZone.Hostile, `FactionTag` per instance; `EffectsToApply` and `HostileEffectsToApply` empty. `TriggerVolume` is a `BoxComponent` with no stored extent; its collision ignores everything except Vehicle (overlap). The native parent `AWDSafeZoneVolume` keeps `InBoundsPlayerPawns` and `MinDistanceToBeInsideVolumeSquared` (the player test is native). Size: scale from the placed root component (`sz_instances.json`, `sz_by_map.json`): 21 safe zones in the four worlds; Bakurani 6 near its main spawn areas (3 at scale 1000, 3 at 750), Ozeti 3 (750), Zestafona 3 (750), Saburtulo 3 (1250). One Bakurani zone is 166 m from its spawn manager, outside the 150 m radius of round 66, which is why round 66 counted 5. Nearest spawn manager distance 35 to 154 m for the main areas. The gap between a main-area safe zone box and the play box is 1.0 km at the least (Ozeti 1,009 m, Bakurani 1,039 m); the nearest a zone box edge comes to the rectangle edge is 368 m (Ozeti), so all lie inside.

Damage gate (2b): `0x6B17DC0` (called from vtable slot 160 of `UWDCharacterVitalityComponent`, `0x6B17760`, which returns 0 damage when it fails): after the target-state checks, if `IsInOwnSafeZone` (`0x6E71010`: the character's ability system has the faction's safe zone tag, taken from the faction at `+268`) is true, the damage is allowed only when its type tag list holds `Meta.Damage.DamageType.VehicleSpawning` (tag global `0xD36A830`). Otherwise the damage is dropped. A second damage-side function (`0x6B53580`) returns early for a target in its own safe zone. Both are Derived from the decompile, not seen in play.

Other users of the own-safe-zone test: `0x7728C00` (slot 100 of `UWDItemRefuelInteractionContext`), `0x7729020`, `0x8638850`, the HUD tracker `0x77705A0`, and the virtual `IsInOwnSafeZone` on the character. No call reads it for a fire check.

Tag users in data: `DA_LocationContext` ("SAFE ZONE" permanent; "HOSTILE SAFE ZONE" 5 s), `DT_AssistCashRewards` (`SpawnTransportAssist` rows: modifier 0 under each safe zone tag), `DT_ChallengeRewards_SessionEvents_Shared` (`Challenges.Context.Target.InSafeZone`: `SafeZoneFactor` and `SafeZoneReward` 0.0 for `HealPlayer.StimPen` (default 100), `RefuelVehicle` (15), `RepairVehicle.Wrench.Standard` (2.5), `.Drill.Light` (5), `.Drill.Heavy` (10)), the spotting items (`ID_Binoculars_Standard`, `ID_Monocular`, `ID_RangeFinder_*`: unnamed tag list with the three safe zone tags), `B_SafeZonePlacementCondition`, `DT_PlacementDisplayTexts`. `Challenges.Rewards.SafeZoneEntered` pays 50 cash (existing wiki row). Sniper Showdown's `B_SniperShowdown_OOBComponent` adds the hostile tag when the player is in neither zone ([round39](round39-modes-ai-other.md)); with section 2 this is the Sniper Showdown out-of-bounds rule: 20 s countdown, then death. The "effect elsewhere (not traced)" of round 39 is this timer.

`B_SafeZoneCam_C`: a camera actor with tag `StartupCamera`, spring arm 3,750, camera pitch -85, ortho width 512, one per safe zone; used for the view while a player waits in the area (reading).

## 5. Soccer pitch and targets (3a to 3c)

`B_WDSoccerField_C` (raw `sz/B_WDSoccerField.json`, 15 placed: Kavkazi 6, Europe 3, NorthAmerica 3, Russia 3; no instance overrides, scale 1): `BoundsBox` extent 2000 x 1500 x 500 (a 40 x 30 x 10 m box), `GoalBoxA` and `GoalBoxB` extent 50 x 400 x 150 at x +/-1550, `BallSpawn` arrow, ball class `B_WDSoccerBall_C`, replicated `GoalBoxA?`. Ubergraph: leaving the bounds box starts `OutOfBoundsTimer` (3.0 s, then `ResetBall`); a ball in a goal box runs `OnGoal`: it reads `GetLastTouchingPlayer` and `GetLastAssistingPlayer`, broadcasts a `WDPreGameLobbyAwardEvent` for each (`Amount` 50 for the toucher, 25 for the assister, `ReasonTag` `UI.ServerSeeding.RewardReason.Soccer`), plays the goal cue (`GameplayCue.GameMode.Soccer.Goal`), then resets the ball (`GameplayCue.GameMode.Soccer.Reset`). No score variable, no team assignment. The pre-lobby award is the points that become starting Cash ([round40](round40-modes-ai-other.md) R4; cap 5,000). Whether the pitch awards also count after the match has started was not traced.

`B_MovingTarget_C` (raw `sz/B_MovingTarget.json`, 45 placed, 3 per spawn area, all with `MovingTarget?` true): health 1.0, `TimeToReachTargetRange` 15 to 25 (scaled by distance between the left and right move points), `DamageIncrease` 3.5 (unread), fall timeline 0.5 s. Damage event: melee damage fails the hit; otherwise, if the cause entity is not `Id.Item.Fists` or none, a `WDPreGameLobbyAwardEvent` with `Amount` = truncated `CurrentDamage` of the damage context and reason `UI.ServerSeeding.RewardReason.Shooting` is broadcast for the shooter's pawn. Hits only count while the target is up and has not been hit (`TakenDamage?`, `TargetDead?`). Delay before it pops back up not recovered.

Challenges (3c): searched `Challenges*` plug-ins, `Content/Meta`, `Wardogs_GameplayTags_v1.md` for MovingTarget, Soccer, RangeTarget, PreGameLobby: nothing in a challenge.

## Reproduce

`WdExtract dump` of the four world packages (`l2.txt`) and the four Blueprints (`l1.txt`); `python -I getsz.py`, `sz_an.py`, `sz_map2.py`, `ws.py`, `build_json.py`; decompile questions: `corpus.sqlite` bodies `0x6E78410`, `0x7687BB0`, `0x6B17DC0`; tag globals with `holder.py 0xD36B910 0xD36B8F0 0xD36B808 0xD36A830`.

## Wiki updates

- New `_wiki/game-modes-and-maps/boundaries-and-safe-zones.md`.
- `_wiki/game-modes-and-maps/sniper-showdown.md`, out-of-bounds line: "effect not in the data" -> the 20 s countdown then death.
- `_wiki/game-modes-and-maps/bakurani.md`, `ozeti.md`, `zestafona.md`, `saburtulo.md`: spawn-area paragraph gets the safe zone size and a link; new "Play area" line with the rectangle.
- `_wiki/game-modes-and-maps/hot-potato.md`: the soccer and shooting mini-games are the pitch and targets in the spawn areas; award values.
- `_wiki/game-modes-and-maps/maps.md`, `_wiki/building.md`: link to the new article.
