# Round 92: game modes and economy open items, read from the DeepExtract corpus (R92-MODES)

Static analysis only. Nothing was run and no protected code was touched. Source: the IDA 9.5 DeepExtract corpus of the restored CL-516586 executable (see [Decompilation corpus](../DECOMPILATION_CORPUS.md)), read as Hex-Rays text and as assembly. Addresses are file RVAs. "Instruction RVA" means the address of the single instruction that carries the test. Class layouts come from the SDK headers; state tree bindings come from the cooked `ST_*` assets, which do carry their property binding tables (the round 67 note that they were "not decoded" is corrected below).

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | How the game decides a tower is hostile, and what reaches the reward | Resolved (corrected) | The capture handler posts the tower's owner from before the change as `PreviousFaction`. The tree adds the Hostile tag when that tag is not equal to the empty tag. |
| 2 | Do towers return to neutral when a recharge ends | Resolved (native path); Blueprint override not readable | The recharge-end callback sends every tower `OnMatchStateActivated(true)`, whose native body writes the empty tag into the tower's faction component. |
| 3 | How the lobby wait clocks start | Resolved | Both clocks start only when their readiness signal fires. Before it the state has no time limit. |
| 4 | Out-of-bounds limit for vehicles and stationary weapons | Resolved | Unit is seconds of game time; the vehicle tick adds the frame time and, at the limit on the server, forces the vehicle's health below zero. |
| 5 | Unit and consumer of `InactivityLifetimeOutSafeZone` | Still open | The client copies the value and never reads it back; no game code that this build holds reads it, so which program uses it, and for what, is not known. Native default 300.0 found. |
| 6 | Vehicle repair and refuel in the safe zone or FOB | Still open | No client code heals or refuels a vehicle for standing in a safe zone. A native `WDVehicleRefuelStation` volume exists but no placed instance or Blueprint is in the exports. |
| 7a | How repeated rewards drop through `LastVictimCount` | Resolved | `Resolve Repeat Action Count` counts earlier rewards for the same target inside a rolling cooldown window and hands the count to `Calculate Reward`. |
| 7b | The "repeat cooldown 0 s" figure | Corrected | The tree literal is 0 and is overwritten by a node that returns a native constant of 180 s. |
| 7c | A reward tag with no formula row | Resolved | `Calculate Reward` returns Failed, the tree goes back to its root state and nothing is granted. |
| 7d | Several events for one kill | Still open (Blueprint or data) | No native code names `Event.StateTree.PlayerKill` or any assist event tag. |
| 7e | Self-referencing inverted `PlayerKill` prerequisite | Still open | The condition type is `WDChallengeCompletedCondition`; its native test was not located. |
| 7f | Raisers of the session events, `Grant Reward` and `Calculate Reward` inputs other than the repeat count | Blueprint-only or not asked | Not native for the event tags; left as they were. |

## 1. The hostile tower test

### Method

The capture finishes in the interaction context's completion handler `0x8570B60` (vtable slot 91 of `UWDHotZoneMagnetInteractionContext`). It reads the tower's current faction tag with `0x856CA00` (call at instruction RVA `0x8570CBC`; the tower's faction component is at `+728`, and a tower without a component returns the static empty tag), reads the interactor's faction with `0x6E6EB00` (call `0x8570CCF`), and fills a `WDHotZoneMagnetInteractionEvent`. Its SDK layout is `PreviousFaction` (+0), `InteractingFaction` (+8), `HotZoneMagnet` (+0x10), `Interactor` (+0x18). The event is posted at instruction RVA `0x8570D84`. Only after that does the handler write the interactor's faction into the tower (`0x146B38880` called at `0x8570DB7`). So `PreviousFaction` is the owner from before the capture.

The access check that lets a capture start is `0x8567F70` (slot 100 of the same class). It refuses when the tower's faction tag equals the interactor's faction (compare at `0x8568012`), when it equals the native cooldown tag (compare at `0x8568018`), or when the game state's active tower number is not `0xFF`, which is the "no magnet running" value (compare at `0x856802E`). So a capture never starts on a tower the capturer's team already holds, and `PreviousFaction` is therefore either the empty tag or another team.

The decision itself is in the cooked tree [`ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_TowerCaptured`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/WorldFeatures/HotZoneMagnet/Content/Data/Challenges/ST_Challenges_SessionEvents_KOTH_HotZoneMagnet_TowerCaptured.json). The asset holds a full `PropertyBindings` table (41 source structs, 42 path bindings, 23 copy batches). Reading it:

- The state "Add Hostile Tower To Context" has one enter condition, a `Tag Equal Condition`. `TagA` is bound to the event payload's `PreviousFaction`. `TagB` is the literal `None` (the empty tag). `bInvert` is true. The state adds `Challenges.Context.HotZoneMagnet.Hostile`.
- So the tower counts as hostile when `PreviousFaction` is not equal to the empty tag, and as neutral when it is.
- The native test of this condition type is the vtable entry `0x6CBD4C0` (the function that starts at `0x6CBD4B5`). It loads the instance data at context `+0x158`, tests `bInvert` at `+0x10` (instruction `0x6CBD4C7`), and compares the two 8-byte tag values for exact equality (`0x6CBD4D1` with invert, `0x6CBD4D8` without). It is a plain name compare, not a hierarchical tag match.
- Of the event payload the tree binds only `Interactor`, `HotZoneMagnet` and `PreviousFaction`. `InteractingFaction` is not read by this tree.

Who is paid, from the same bindings: the first enter condition group requires the rewardee to be inside the tower range (`WDStateTreeActorInTowerRange` with the tower from the event), to carry neither `State.Player.Vitality.Critical` nor `State.Player.Vitality.Dead`, and to have the same faction as the interactor (a `Tag Equal Condition` between the faction of the rewardee's pawn and the faction of the event's `Interactor`, not inverted). The state "Add Instigator To Context" has an `Object Equals` condition that compares the rewardee's player state with the player state of the `Interactor`, so only the capturer gets the Instigator tag.

The cash and XP amounts per tag are still data; the Hostile tag is what the reward row's `HostileModifier` option keys on.

### Result

The round 67 line "the comparison sits in unbound state-tree property bindings, so the exact test is inferred" is corrected: the bindings are in the asset and the test is "previous owner is not the empty tag".

## 2. Towers back to neutral

### Method

`0x856D9A0` (game state component, authority) is the reset and code generation function. For every registered tower it calls the tower's `OnMatchStateActivated(true)`. It is reached from the component's own `OnMatchStateActivated` thunk `0x8575440` through `0x85710A0` and `0x8571BE0` (match start), from the recharge timer callback `0x8570430` (recharge end), and from the deactivation function `0x8570080` in its immediate-reset form. In the normal form `0x8570080` clears the towers to the cooldown tag and arms the recharge timer with `TowerControlRechargeDuration` scaled by the world time dilation. The callback tests authority before it calls `0x856D9A0`.

The tower's `OnMatchStateActivated` is virtual slot 240 of `AWDHotZoneMagnet` (`0x8571360`, body from the instruction at `0x8571360`). On the authority copy (role byte `+0x170` equals 3) it writes the static empty tag (`qword_14D2692F8`, a global that is never assigned and is used throughout as "no faction") into the tower's faction component (`+0x2D8` is the component pointer in the SDK layout; the call is the tail jump at `0x857138C`).

The cooldown state is a different tag: `0x856A060` writes the native tag `qword_14D3E5248` into every tower when the magnet ends. That tag is registered in `0x15065E0` under the name `Meta.Alignment.Faction.Null` (module `HotZoneMagnetRuntime`). So during the recharge a tower is not empty but "Faction.Null", and the capture access check refuses it (item 1). When the recharge callback runs, the tower returns to the empty tag, which the hostile test reads as neutral.

### Caveat

`0x856D9A0` chooses the call path from the declaring class of the function it finds on the tower: a native class gets the direct virtual call, anything else goes through `ProcessEvent`. If the cooked Blueprint `B_HotZoneMagnet` declares its own `OnMatchStateActivated`, that override runs instead and may or may not call the native body. The Blueprint's function list is not in the exports, so this is the one thing not read.

## 3. How the lobby wait clocks start

### Method

`BHMatchState` has `ElapsedTime` (+0x40), `MaxTime` (+0x44) and `bInfinite` (+0x48, config). The match state component's update (`0x4D6D7C0`) calls virtual slot 88 of each active state and marks the state finished when it returns false. The base implementation `0x4D6D700` adds the frame time to `ElapsedTime`, returns true if `bInfinite`, and otherwise returns true while `MaxTime` is above 0 and above `ElapsedTime`.

`WDMatchState_PreMatch_WaitingForPlayerCount` overrides slot 88 at `0x6D70840`: it tests a byte at `+0x90`. While that byte is 0 the function returns true at once (instruction `0x6D70849`) and `ElapsedTime` is never advanced. Only the `OnAllPlayersReady` handler (`0x6D70190`) sets the byte (instruction `0x6D7019D`). After that the call goes to `0x6D6F950`, which holds the clock (returns true without adding time) while a flag at `+0xD8` of the `WDServerLifecycleSubsystem` is set, and otherwise runs the base tick. The `+0xD8` flag has no name in the SDK and its writer was not followed.

The signal comes from `0x6D6FFB0`: it counts the state's tracked players whose ready entry is set and compares the count with the configured minimum (60 for this state in the shipped settings, see [round 40](round40-modes-ai-other.md)) or with a console variable when that is zero or higher. On reaching it, it raises the game state's "all players ready" delegate (`0x6DA3BB0`). An entry is "ready" when the player's faction is not the ignored default faction (handlers `0x6D70880` and `0x6D70B20`), that is, once the player is on a team. The state start `0x6D6FC10` evaluates the players already present, so a lobby that is already full raises the signal at once.

`WDMatchState_PreMatch_WaitingForReadyUp` is built the same way with its own flag at `+0x84` (override at `0x6D71C70`, flag set by `0x6D714E0` at instruction `0x6D714ED`, the 5 s clock). Its signal is raised by `0x6D71DC0` when the number of tracked players is at least the minimum (9 in the shipped settings) and every tracked player's ready flag is set; the flag changes on each ready-state change.

### Result

The 10 s and 5 s are countdowns that start when the readiness condition is met, not waits that start with the state. The first state has no upper bound in time: it lasts until enough players are on a team. The second lasts until at least 9 players are present and all of them are ready. Total wait after both conditions hold: about 15 s (10 plus 5), not counting the world-load state before them.

Not read: how a player marks themselves ready (the client request for the ready state). `bInfinite` is false in the shipped settings as far as the config summary shows (round 40 lists only the count and `MaxTime`); if a server set it, the clocks would never end.

## 4. The out-of-bounds limit for vehicles and stationary weapons

### Method

`UWDVehicleGameplaySystemsComponent` tick (slot 131, `0x7687980`) calls `0x7687BB0` with the frame time passed in `xmm1`. In `0x7687BB0`:

- The vehicle's position is tested against the playable rectangle and against the hostile safe zone tag, as round 68 described.
- `CurrentOutOfBoundsTime` (`+0x250`) grows by the frame time while out (instruction `0x7687D70`) and is compared with `OutOfBoundsTimeLimit` (`+0x238`) at `0x7687D7D`. The unit is therefore seconds of game time.
- The constructor stores the default limit as the float 22.0 (`mov dword ptr [rdi+238h], 41B00000h` at instruction `0x766B2B1` in the component constructor `0x766B080`).
- At the limit, on the authority copy only (`0x767B6A0` tests the role byte equals 3), `0x7674AE0` runs.
- `0x7674AE0` calls `0x53288B0` on the vehicle's health component (`+1944`), passing an instigator object that `0x7674B90` supplies when there is one. `0x53288B0` looks up the `Attribute.Gameplay.Health` attribute, and if it is above 0 it sets it to the most negative float, and if the value is now at or below 0 it runs the component's zero-health handler (vtable `+1296`).
- Going back in, the counter runs down at the same speed and is zeroed below 0, as for characters.

Stationary weapons use the same vehicle gameplay-systems data asset type ([round 90](round90-census-v5.md): `DA_GameplaySystems_STN_*`), so they carry the same component. This was read from the data asset type, not from a placed emplacement.

### Result

The vehicle limit counts in seconds and ends in the vehicle losing all its health on the server, which is the vehicle's normal destruction path. The wiki's "destroyed (inferred)" becomes read.

## 5. `InactivityLifetimeOutSafeZone`

The component constructor `0x766B080` stores 300.0 (`0x43960000`) at `+0x75C` (instruction `0x766B3DF`). The data asset value is copied into that field at `0x767BC40`. A scan of the assembly of the vehicle module range (`0x7600000` to `0x7700000`) for loads of `+0x75C` finds only those two functions, and a text search of the decompiled files for float reads at `+1884` finds only the copy. Nothing in the client executable reads the value, so the unit and the removal action live in code that this build does not hold, and which program that is, is not known. Status: still open; the native default 300.0 is new, and the name `InactivityLifetimeOutSafeZone` still suggests seconds only by guess.

## 6. Vehicle repair and refuel in the safe zone or at a FOB

- The own-safe-zone test `0x6E71010` has these callers: the damage gate `0x6B17DC0`, the refuel source context `0x7728BFB`, `0x7729020`, `0x8638850`, `0x86388F0`, `0x6B53580`, `0x6E6BD70`, `0x6E7A840` and `0x77705A0`. None of them heals or refuels a vehicle.
- The refuel source context (`0x7728C00`, slot 100 of `UWDItemRefuelInteractionContext`) lets a player fill a Fuel Canister at a world fuel point: it refuses an empty source, and allows the fill when the player is in their own safe zone and the source is flagged free in spawn, or when the player has the cash for one update. This repeats round 36 and round 66.
- A native actor class `AWDVehicleRefuelStation` exists: a box with a faction tag and the fields `HealthPerUpdate`, `RefuelSpeed`, `PassiveRefuelSpeed`, `RefillPerUpdate` and `PricePerLitre`. Its overlap handlers `0x7622890` (begin) and `0x7622C20` (end, through `0x7621490`) add a vehicle whose faction matches to the station's overlap set and the station to a list on the vehicle's gameplay-systems component (`0x7686A40`). The class dump holds only its default object, no Blueprint subclass, and none of the exported maps places one, so this round cannot say it is the safe zone service the in-game tip describes.
- The FOB side is the built Refuel Station and Repair Station (the pawn buildable manager request `Server_RequestRefuelOrRepair`, `0x85D5C80`, was not read this round).

Status: still open. The tip text is still the only statement that a safe zone repairs and refuels.

## 7. Challenges page items

### 7a. `LastVictimCount`

The task `Resolve Repeat Action Count` has its enter function at `0x6CC26D0` (the entry after the stubs that follow `GetInstanceDataType` in the vtable at `0xB13C470`). Its instance data is `Target` (+0), `Cooldown` (+8), a property reference to the tracker (+0xC) and a reference to the output `RepeatCount` (+0xE). The function:

1. Sets `RepeatCount` to 0 (instruction `0x6CC272F`).
2. If `Cooldown` is 0 or less (compare at `0x6CC2776`), empties the tracker and finishes with Succeeded. `RepeatCount` stays 0.
3. Otherwise reads the world time, walks the tracker's map of weak actor pointers and removes entries whose actor is gone or whose last time is older than `Cooldown`.
4. Looks up (or adds) the entry for `Target`. `RepeatCount` becomes the entry's previous count, the entry's count goes up by one (`inc` at `0x6CC29B4`) and its time is set to now.

So the count is the number of earlier rewards for the same target by the same tree instance inside a rolling window in which each new reward renews the entry's time. The tracker is a tree parameter (`VictimTracker`), so it is per player and per tree.

`Calculate Reward` (enter function `0x6CC11D0`, the same slot of the vtable at `0xB13B980`) takes its `Inputs` array (+0x138, entries of a name and a float) into its variable map before it calls the expression evaluator (`0x6CC9930`, call at `0x6CC1B7A`). The tree's `Inputs[0]` is named `LastVictimCount` and its value is bound to the state parameter `RepeatCount` of "Populate Context" (binding batch 6), which is the property reference that `Resolve Repeat Action Count` writes its `RepeatCount` output to. The tracker reference points to the tree parameter `VictimTracker`. This replaces the default 0 that the builder `0x861DB00` registers on the other reward paths. For Tower Captured the data supplies `LastVictimCountMax` 4 and `LastVictimReductionModifier` 0.25, so a payout to the same player for the same target inside the window is cut by 25 percent per earlier payout, to nothing at the fifth.

### 7b. The cooldown is 180 s

All 25 trees that hold a `Get Repeat Actions Cooldown` node store `RepeatActionsCooldown` 180.0. The node's native execute function (the entry after the stubs in the struct's vtable at `0xB2A08B0`; body at `0x6CBE700`) writes the constant 180.0 (`mov dword ptr [rax], 43340000h` at `0x6CBE707`) into its output, so the value does not come from the data. The binding copies it into the `Cooldown` input of `Resolve Repeat Action Count`. The literal `Cooldown: 0.0` in the task's own instance data is only the unbound default. The challenge page's statement that the stored cooldown "is 0 everywhere" is wrong in that sense and is corrected there. The generated tables on that page still print "repeat cooldown 0 s"; their generator [`_tools/challenge_tables.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/challenge_tables.py) reads the task literal and was outside this round's files.

### 7c. A reward tag with no formula row

`0x6CC11D0` looks the reward tag (instance `+0x130`) up in the registry whose type global is `qword_14D358128`. If the lookup fails, or an expression reports an error, every exit path returns status 3, which is Failed (final `mov al, 3` at `0x6CC1CD4`). In the Tower Captured tree the state "Calculate Reward" has an `OnStateSucceeded` transition to "Update Reward XP Tags" and an `OnStateFailed` transition to the root, so a Failed task skips "Grant Reward" and the tree waits for the next event. Nothing is paid and nothing else is logged on that path. This confirms the page's reading that tags without a row cannot pay. The 44 tree and tag pairs listed there are therefore dead ends unless a row is added at run time.

### 7d. Several events for one kill

No native string holds `Event.StateTree.PlayerKill`, `Event.StateTree.DestroyVehicle` or any assist variant (the only `Event.StateTree.*` string in the executable is `Event.StateTree.WagerActionConfirmed`, a native tag registration). The raisers are Blueprint graphs or data. Blueprint-only; left open.

### 7e. The inverted self-prerequisite

The `Prerequisites` field is an `FWDMetaPrerequisiteQuery`, a world condition query over the schema `WDMetaPrerequisiteSchema`. The single condition in the `PlayerKill` row has the fields `ChallengeId` and `bInvert`, which fits `WDChallengeCompletedCondition` (SDK: `ChallengeId` at `+0x10`). Read literally, the row is available while `PlayerKill` is not completed. The native test of that condition was not located (the vtable of the condition struct could not be found from its struct registration), so the meaning of "completed" for a challenge that never completes is still open.

### 7f. Left alone

Which Blueprints raise the session events, the `Grant Reward` task, the effect of auto-activate set to no, the order in which several trees listening to related events fire, and whether the cash tables under `CashRewardsDataTable` feed `Calculate Reward` (the registry named above is read, but which tables register into it is not shown by the code) were not settled.

## Wiki updates

- `_wiki/game-modes-and-maps/hot-zone-magnet-towers.md`: the hostile rule, the refusal rule, the reset to neutral, the repeat payout rule; two "what is not known" bullets removed.
- `_wiki/progression-and-economy/hot-zone-magnet-challenges.md`: the hostile rule and the repeat payout rule, same wording as the tower page.
- `_wiki/game-modes-and-maps/pre-lobby.md`: the length of the wait.
- `_wiki/game-modes-and-maps/boundaries-and-safe-zones.md`: vehicle out-of-bounds effect and unit; what is known about the abandoned-vehicle time and the safe zone service.
- `game-features/Wardogs_Challenges_v1.md`: hand-written notes only (the generated tables are untouched): the join by tag, the repeat count and the 180 s cooldown, the missing-row behaviour, the event raisers, the prerequisite, and section 11.

## Open after this round

- The Blueprint `B_HotZoneMagnet` override of `OnMatchStateActivated` (item 2).
- The writer and meaning of the server lifecycle flag that pauses the lobby clocks (item 3), and how a player becomes ready.
- The consumer and unit of `InactivityLifetimeOutSafeZone` (item 5), and what repairs and refuels a vehicle in a safe zone (item 6).
- The native test of `WDChallengeCompletedCondition`, the event raisers, and which tables feed the reward registry (item 7).
