# Round 59: seven open wiki questions (R59-RE)

Static analysis only. Nothing was run. Evidence levels: cooked data read (JSON under `data/` and `assets/data/`), Blueprint dump read (extractor `dump`), static disassembly and decompiled-corpus reading (RVAs, image base 0x140000000). Extractor output and helper scripts are under `E:/Reverse_Engineer/wardogs_analysis/round59_re/` (`lo/` Lootable component dump, `f6a68df0.c` and `lootable_*.c` decompiler extracts, `scan.py`, `riprefs.py`, `dec.py`). Method as in rounds 57 and 58. No protected (virtualized) code was devirtualized; code behind the protection layer was not read.

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | Who reads the helicopter "can be locked on to" flag | ABSENT (no reader in the client; flag unused) | Nothing reads it. Flares neither stop a new lock nor drop an existing one. |
| 2 | Does the flare lure apply to the Stingray drone | FOUND (no) | The drone is a player-flown camera projectile with no guidance data; the lure only exists inside the guided-missile guidance function. |
| 3 | VIP Escort revive clock | FOUND | The 10 s clock starts when the VIP enters the critical (downed) state and nothing cancels it. A VIP disconnect does not fail the mission (it re-picks a VIP). |
| 4 | How loot spawns are chosen | FOUND (logic); ABSENT (VIP Escort marker positions) | Markers named after table rows; chance roll per marker; weighted item pick; sub-items placed with a grid query. |
| 5a | Part costs vs total | FOUND | Total = the structure's own `Cost` only. Parts are not added. |
| 5b | Mesh-bounds changes | FOUND (values); NATIVE (consumer not located) | Roof box 750 to 1,158 cm long; shelter ceiling box slightly smaller. |
| 5c | Breach effect | FOUND (kind); NATIVE (spawn trigger not located) | A Niagara particle system plus a spawn offset; no gameplay number. |
| 6 | 20 L fuel canister | ABSENT | The 20 L item has the generic item tag `Id.Item`; no row can reference it. |
| 7 | KOTH reward set that pays | SERVER | The client holds both sets; the cash registry has no client reader, and challenge rewards are forwarded to a backend handler. |

## 1. Reader of `CanBeLockedOnTo`

Round 58 found `AWDRotaryVehicle` slot 397 `0x76B63B0` returning `not bFlaresActive` (airplane: always true) and the exec thunk `0x7662010`, but no caller.

What was checked:

- **Native callers of the interface.** Every native use of `IWDTargetableInterface` needs its class getter `0x7661760`, which caches the class in the cell `0xD3B0F18` (rip-relative scan `riprefs.py 0xD3B0F18` finds only the getter itself). The getter's callers (corpus `calls` table plus `rxref.py 7661760`) are the guidance function `0x6F2E620`, `0x6F30860`, `0x6F35340`, `0x6F37510`, and the interface wrappers `0x76619C0`, `0x7661A30`, `0x7661AA0`, `0x7661B10`, `0x7661C20`, `0x7661D00`, `0x7661F10`. The wrappers that exist cover CanBeTargeted, threshold distance, clear-when-close, near-miss box, target location and should-follow. **There is no wrapper for `CanBeLockedOnTo`**; the interface offset `+0x38` is called only inside the exec thunk (`0x7662031`), which is the Blueprint VM entry. `0x6F35340` and `0x6F37510` call only the CanBeTargeted wrapper.
- **The lock-on code.** `UWDAction_Ads` (`B_Action_Ads`, `B_Action_Vehicle_Weapon_Ads`) runs the lock through the virtual at `0x6A68A30` (slot 95), which calls `0x6A68DF0` (target list `WDLockOnTargets`, per-target progress map, add and remove helpers `0x6A66A60`, `0x6A68B60`, `0x6A68BE0`, `0x6A68CF0`). Its only vtable calls are on the action and its component (offsets 288, 296, 312, 344, 1848); it never loads the interface class. The candidate filter `BP_CanTarget` is a Blueprint hook that only compares the target with `TargetingHardDeckLimit` and the weapon stats (round 42).
- **Blueprints.** No cooked asset and no Blueprint dump contains the name `CanBeLockedOnTo` (data grep; round 58 findname: 0 packages).

Result: the flag has no reader in the statically readable client code. It is unused data. So flares do not stop a new lock and do not drop one. Evidence: static disassembly, not run. Caveat: code behind the protection layer is not read, so the wiki keeps "inferred".

Page: `_wiki/vehicles/countermeasures-and-flares.md`.

## 2. Stingray drone and flares

- `DA_Drone_ProjectileData` (`STN_05/Data/Projectile`) has no `GuidanceData` block, while the three guided projectile assets (`DA_72mm_ProjectileData`, `DA_70mm_ProjectileData`, `DA_DebugHomingRocketData`, `assets/data/r46-guidance.json`) set `bGuidedProjectile`. The drone sets `bActorHandlesProjectileMovement` and `bShouldTakeViewTarget`.
- `BP_Drone_Projectile` (`round41_veh/d1/BP_Drone_Projectile.json`) is a camera projectile with a first-person camera, mouse steer sensitivity, and the input context `IMC_Drone_Projectile` with `IA_Drone_Projectile_Steer`, `_Boost` and `_Brake`. It has no homing reference (0 hits for Homing). Its `Targeting` tags are lock-on cues.
- The lure (`ShouldFollowTarget`, `GetTargetLocation`, clear-when-close) is reached only from the guidance function `0x6F2E620` (round 58).

Result: no, the lure does not apply to the drone (FOUND). Inferred part: that an unset `bGuidedProjectile` is false (the 72 mm, 70 mm and debug assets are the only ones that set it, and ordinary bullets are not guided).

Pages: `_wiki/building/stingray.md`, `_wiki/guides/anti-vehicle-guide.md`.

## 3. VIP Escort revive clock

Quest graph `Q_VIPEscort_01` (`round36_ai/dump`, `quest_graphs.txt`): node 5 plays `SQ_RandomPlayerMarkedForDeath`. The sub-quest has two exits, read from the pin names in the dump:

- `Player Died` (pin 11, from `WaitForCharacterToEnterVitalityState`, required state `State.Player.Vitality.Critical`) leads to node 13 (fail voice-over), then node 14 `WaitForDuration` 10.0 s, then node 8 `CompleteScenario` (failed). Nodes 13 and 14 have no input from any revive or cancel node, and node 14's only output is node 8.
- `Marked Player Disconnected` (pin 10, `WaitForPlayerDisconnect`) leads to the reroute nodes 6 and 7 and back into node 5. So a disconnect **re-runs the pick** (`AddComponentToRandomPlayer`) and does not fail the mission. This corrects the old wiki line that a disconnect fails the mission.

The Critical state is the downed state (`downed-and-revive.md`: at 0 HP the player enters the critical state, bleed-out timer 360 s). So the VIP going down starts a fixed 10 s clock that a revive does not cancel; the usual bleed-out time is irrelevant. FOUND (Blueprint quest graph read). The extraction success path runs in parallel.

Pages: `_wiki/game-modes-and-maps/vip-escort.md`, `_wiki/guides/pve-guide.md`, `_wiki/guides/faq.md`.

## 4. How loot spawns are chosen

Classes (SDK `LootableRuntime_*`): `UWDLootableComponent` (properties `MinEnvQueryScore`, `LootableDataTable`, `LootableEnvQuery`, `LootableActor`), `AWDLootable`, row `FWDLootableDataTable` (`ItemsToSpawn` entries with `ItemTag`, `ItemAmount`, `ItemSpawnWeight` and sub-items; `SpawnChance`, `bSpawnByDefault`, `bSpawnByPoints`, `InitialSpawnTime`, `InitialSpawnPoints`, `bCanRespawn`, `RespawnTime`, `bNeverSelectPreviousItem`, `bSpawnInsideControlZoneOnly`). `B_LootableComponent_C` is an empty Blueprint (dump `round59_re/lo/B_LootableComponent.json`: CDO and class only), so all logic is native.

- **Which marker gets which row.** `OnMatchStateActivated` (`0x855EF40`) calls `0x855CCA0`. On the server (`+0x170 == 3`) it walks the owning marker actor's tag array (`owner + 0x1F0`, count `+0x1F8`), looks each tag up as a row name in the `WDLootableDataTable` (find-row `0x43E51E90`) and keeps the matching row. If the row's `bSpawnInsideControlZoneOnly` (row `+0x38`) is false it spawns at once (`0x8559E50` creates the `AWDLootable` at the marker's transform, root transform `owner + 0x1C0 + 0x210`); if true it waits for the control-zone state (compare against row `+0x39` and a delegate re-entering `0x855CCA0`).
- **Chance.** `AWDLootable` roll `0x855B6A0`: `RandRange(1, (int)(200 / SpawnChance + 0.5) >> 1) == 1`; 100 always passes (`RandRange(1,1)`). On failure with `bCanRespawn` it re-arms a timer for `RespawnTime`.
- **Which item.** `0x855E6B0`: sums `ItemSpawnWeight` (entry `+0x1C`, 32-byte entries) over all entries except, with `bNeverSelectPreviousItem`, the one chosen last; draws `rand() / 32768 x sum`; picks the first entry whose running sum reaches it. Chosen tag, sub-item list and amount are copied to the actor (`+0x308`, `+0x310`, `+0x320`).
- **Sub-items** (for example the SV98 magazine). `0x855D940` handles the EQS result: keeps items whose score is at least `MinEnvQueryScore`, picks a random item (with the sub-item chance), random yaw 0 to 360, and spawns the sub-item there. The query `EQS_FindSubLootableLocation` is a simple grid (80 cm, spacing 40 cm), a distance test 40 to 180 cm and a visibility trace.
- **Not read:** `bSpawnByPoints` and `InitialSpawnPoints` (no reader found in the component functions above; their meaning stays open).

VIP Escort rows (`DT_LootableDataTable_VIPEscort_01`): `Lootable.VIPEscort01.Fuelcan100` (Fuel Canister x1, chance 100, no respawn) and `Lootable.VIPEscort01.AK` (SV98 x1 plus magazine, chance 100, respawn 10 s). Both have `bSpawnInsideControlZoneOnly` false, so both spawn at match start. Marker actors tagged `Lootable.VIPEscort01.*` do not exist in the 65 cooked VIP Escort cells (round 36), so the positions are ABSENT from the data held. Status: FOUND (selection logic, static disassembly), ABSENT (positions).

Pages: `_wiki/game-modes-and-maps/vip-escort.md`, `pve-scenarios.md`, `_wiki/guides/pve-guide.md`.

## 5. Building

### 5a. Part costs

`GetTotalBuildCost` (`0x8593FB0`, core `0x858D1D0`) is `max(1, floor(abs(Cost x S) + 0.5))` on the asset's own `Cost` (`+0x5C`); it reads no child assets (disassembly: only `[rbx+0x5C]`). Callers: `0x858CCA0`, `0x858D280`, `0x85F1F20` (hit arithmetic), `0x85F23C0` (prediction), `0x85929D0` (repair). The parent buildable's supplies are spent over its hits from the parent's `Cost` (round 38). The parts (for example `DA_Buildable_Bunker_Floor`, Cost 10) are separate data assets that the parent spawns as sub-actors at completion (`bOverridesFinalStage`, round 38); no sum is made. Check: Gate parts 3 x 85 = 255 against 200; Door 2 x 22 = 44 against 80; Bunker, shelter and tower parts 20, 20 and 30 against 200. FOUND (static). A part's own cost most likely applies to repairing that part alone (the repair function takes the actor's own data asset): inferred.

### 5b. Mesh-bounds changes (Season 2, `assets/data/season-diff/items-equipment.json`)

- `DA_Buildable_Bunker_Roof`: `MeshLocalBoundingBox` (per build stage) and `FinalStageBoundingBox` X min -382.3 to -441.6, X max 367.4 to 716.6, Y min -366.1 to -367.4, Y max 367.7 to 382.2, Z min -215.5 to -224.4, Z max 110.4 to 110.7 (cm). Long side 749.7 cm to 1,158.2 cm. `DA_Buildable_Bunker_Roof_Stages`: all 16 snap points Z 75 to 97.
- `DA_Buildable_AirRaidShelter_Ceiling`: X min -354.4 to -352.3, X max 356.9 to 355.9, Z max 17.6 to 9.2.
- `DA_Buildable_AirRaidShelter_Stages` stage 5 box zeroed (invalid) and hesco placements changed (not part of the open sentence).

What reads the boxes: `BuildingStagesDefinition.BoundingBox` is copied into the spawner actor's `BoundingBox` by `B_ActorSpawningBuildable`; `UWDBuildableDataAsset.FinalStageBoundingBox` is at `+0x258`. No reader of `+0x258` was found in `0x8500000..0x8700000` (skip-data scan). The placement validation has `BuildableBoundingBoxExtentComparingLeeway`, and `Server_TryPlaceBuildable` takes an `FBox`. So the consumer is NATIVE, not located; the wiki says "most likely the space used for placement checks (inferred)".

### 5c. Breach effect

`DA_Buildable_Door_DoorOnly` and `DA_Buildable_Gate_Left/_Right` set the soft Niagara reference at data-asset `+0x328` (`/Buildables/VFX/NS_BuildableDoorBreach`, `NS_BuildableGateBreach`) and a vector at `+0x360` (Door: 0, -75, 0). Only the constructor (`0x858538C`, `0x85853E9`) touches those offsets in `0x8570000..0x8630000`; no Blueprint references the properties. A Niagara system is a particle effect, and the data asset has no damage or physics field beside it. FOUND (kind: visual effect with a spawn offset); the spawn trigger is NATIVE, not located (assumed to be the part's destruction, as the earlier wiki text had it). The infantry "door breach" status effect (0.8 s movement ramp) belongs to sprint-breaching a world door and is unrelated.

Pages: `_wiki/building/bunker.md`, `door.md`, `gate.md`, `indirect-fire-shelter.md`, `recon-tower.md`.

## 6. 20 L fuel canister

`ID_FuelCan_20L` (`Items/FuelCanister/Content/Data`) has `ItemId` = `Id.Item` (the generic root tag) while `ID_FuelCan_40L` has `Id.Item.FuelCan`; every `Id.Item.FuelCan*` string in `data`, `assets` and `sdk` is exactly `Id.Item.FuelCan`. `DT_VendorData_Ext_FuelCanister` has one row, `Id.Item.FuelCan`. The only references to the 20 L asset name are its own file, the season diff and earlier docs: no shop row, vehicle kit, loot table or quest names it. Everything in the game addresses items by tag, so nothing can grant it. ABSENT (searched `data/`, `assets/data/`, `sdk/raw/`, the VIP loot table). Its values: 20 durability, `MaxAmount` 20, `UpdateTime` 1.5, `UpdateAmount` 1.0. Page: `_wiki/equipment/fuel-canister.md`.

## 7. King of the Hill reward set

- Challenge rows: `DT_ChallengeRewards_SessionEvents_Shared` (kill 300 / 250). The KOTH state trees compute them with the `Calculate Reward` and `Grant Reward` tasks (`FWDSessionEventsCalculateRewardTask`, `FWDSessionEventsGrantRewardTask`; the instance data holds a `UWDPlayerChallengeComponent` and `RewardResources`), and the component forwards results to the challenge-rewards backend handler classes (`UWDChallengeRewardsBackendDataHandler`, `UOnlineChallengeRewardsDataMarshaler`, vtables `0xB3F5A50`, `0xAD077D0`). So the challenge base is a number the game computes, but the credit is made by the backend (inferred from the class names; the handlers were not decompiled).
- Cash tables: `DR_CashRewards` (15 tables, first table wins, round 48) has no named consumer in the client; the string `CashRewards` is absent from the executable and from every asset but the registry (round 48). `WDGameSettings` points `ResourceRewardDataTables` to `DT_CashRewards` (`Meta.Progression.Resources.*` rows), not to the `DT_Reward_Cash_*` tables.

Both sets exist in the client files; which one a match credits cannot be shown from the client, and the crediting is done by the server and backend. Status SERVER. Pages: `_wiki/game-modes-and-maps/king-of-the-hill.md`, `_wiki/progression-and-economy/king-of-the-hill-challenges.md`, `_wiki/guides/king-of-the-hill-guide.md`.

## Wiki updates

- `_wiki/vehicles/countermeasures-and-flares.md`: flag has no reader; flares neither stop nor drop a lock (inferred).
- `_wiki/building/stingray.md`, `_wiki/guides/anti-vehicle-guide.md`: drone is not a guided missile; flares do not pull it.
- `_wiki/game-modes-and-maps/vip-escort.md`, `_wiki/guides/pve-guide.md`, `_wiki/guides/faq.md`, `_wiki/game-modes-and-maps/pve-scenarios.md`: a revive does not stop the 10 s clock; a disconnect re-picks the VIP; loot markers.
- `_wiki/building/bunker.md`, `door.md`, `gate.md`, `indirect-fire-shelter.md`, `recon-tower.md`: parts not added; box changes; breach is a visual effect.
- `_wiki/equipment/fuel-canister.md`: the 20 L version cannot be obtained.
- `_wiki/game-modes-and-maps/king-of-the-hill.md`, `_wiki/progression-and-economy/king-of-the-hill-challenges.md`, `_wiki/guides/king-of-the-hill-guide.md`: the server decides.
