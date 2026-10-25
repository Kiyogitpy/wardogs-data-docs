# Round 38: building data (buildables, placement, Drill Rig, Radio, cash rows, FOB spawn)

Scope: eight open items from [`game-features/Wardogs_Buildables_v1.md`](../../game-features/Wardogs_Buildables_v1.md) (every "not traced"), read from cooked data, Blueprint bytecode, the Dumper-7 headers in `sdk/raw` and the decompiled native code. Evidence level for everything below: cooked data read and static disassembly; nothing was run. Excluded on purpose (another round): the build-time and cost arithmetic and the FOB `DoNotTakeDamage` tag in native code.

Results are in section 14 of the Buildables page and in `assets/data/buildable-semantics.json` (`python -I _tools/buildable_semantics.py`, `--check` asserts the key values).

## Method and reproduction

- Extractor: the round 36 AI agent's rebuilt exe `E:/Reverse_Engineer/wardogs_analysis/round36_ai/bin/WdExtract.exe` (the `list` mode sees only `.uasset`; the package list used was the existing `round36_ai/all/files.txt`). Dumps in `E:/Reverse_Engineer/wardogs_analysis/round38_data/d1/` (`dump` mode of the packages named below; Blueprint bytecode included). Helper scripts there (not committed): `bc.py` (bytecode printer), `ld.py` (multi-document loader), `stages.py`, `nat.py` / `g.py` (query the decompiled corpus), `cash_rows.txt`.
- Packages dumped: `Items/Buildables/Content/Data/Buildables/` `B_SafeZonePlacementCondition`, `B_WithinLadderBoundsPlacementCondition`, `B_ActorReplacingBuildable`, `B_ActorSpawningBuildable`, `B_Buildable`, `B_CriticalHitSpot`, `B_CriticalHitSpotDecalComponent`, the Door, Bunker, Crows Nest and Gate `...ActorReplacing` classes, `Radio/B_Radio*`, `Radio/B_Buildable_Radio`, `Radio/B_Radio_AudioHandler`, the Radio interaction contexts, `Hotzone_Magnet/*`, the FOB classes; `WorldFeatures/HotZoneMagnet/Content/Data/B_HotZoneMagnet*`; `UI/StringTables/STRINGS_HotZone`; `CashRewardsDataTable/DR_CashRewards`.
- Native: decompiled corpus `decompiled_cl516586_20261017_mmvpuc__/corpus.sqlite` (RVAs below are image-relative). The executable's protected parts were not touched.

## 1. `bOverridesFinalStage` and the `...ActorReplacing` spawners

Status: **FOUND (data) / NATIVE (the swap itself)**.

- The six flagged definitions (`DA_Buildable_AirRaidShelter`, `_Door`, `_Bunker`, `_CrowsNest`, `_Gate`, `_HBlock_QuadWall`) are exactly the six whose spawner base class derives from `WDActorReplacingBuildable` (SDK: `AB_Buildable_AirRaidShelter_C`, `AB_Buildable_Bunker_C`, `AB_Buildable_CrowsNestActorReplacing_C`, `AB_Buildable_Door_ActorReplacing_C`, `AB_Buildable_Gate_ActorReplacing_C`, `AB_Buildable_HBlock_QuadWall_C` all derive from `AB_ActorReplacingBuildable_C`). The other structures derive from `AB_ActorSpawningBuildable_C` or are `B_Buildable_C`. The `...ActorReplacing` Blueprints contain no functions or logic (CDO only); `WDActorReplacingBuildable` adds one native property, `BoundingBox`.
- In the stage files, the last stage of each flagged definition carries `ActorToSpawn` entries (separate buildable prefabs) in `MeshToPlacements`; `_tools/buildable_semantics.py` lists them (`finalStageSpawnedActors`). Non-flagged multi-stage structures have none. The composite pieces are single-stage data assets (`DA_Buildable_Bunker_Floor`, `_Roof`, `DA_Buildable_CrowsNest_*`, `DA_Buildable_AirRaidShelter_Floor/_Ceiling`, `DA_Buildable_Gate_Left/_Right`).
- The placement rule per mesh uses `EWDPlacementRules` (0 PreviewAndFinal, 1 PreviewOnly, 2 FinalOnly, 3 FinalOnlyWithFoundations). The Door's preview-only mesh is the one with the Door actor; the Gate's ramp is `FinalOnly`.
- Native default of the flag: false (`UWDBuildableDataAsset` constructor `0x8585020`, store at offset 0x290).
- Not read: the native function that performs the swap. "At completion the sub-actors replace the preview meshes" is **Derived** from names and data.

## 2. `MaxStack` and `PlacementFlags`

Status: **FOUND (enum), NATIVE (reader read)**.

- Enum `EWDPlacementFlags` (sdk/raw/BuildablesRuntime_structs.hpp): None 0, AllowRotation 1, CanBeBuiltOn 2, CanPlaceVertically 4, CanPlaceOnBuildables 8, Default 11.
- Constructor `0x8585020`: `PlacementFlags` (+0x12C) = 11, `MaxStack` (+0x10C) = 2, `StackCheckOffset` (+0x108) = 10.0, `MaxHealth` = 4000.
- Reader `sub_1485C5390` (RVA `0x85C5390`, the snap-on-top check): `(GetPlacementFlags(newAsset) & 8) == 0` fails (reason tag `qword_14D3E6F80`); `sub_1485889A0(target)` = `(targetAsset+0x12C) & 2` fails (`..F88`); the target's data asset must also pass two tag checks against `newAsset+80` (EntityTag) and the target's tag; `target progress >= 1.0` else `..F90`; `StackHeight(target) + 1 <= *(newAsset+268)` (MaxStack) else `..F98`; the resulting support height `<= placementData+76` (SupportHeightLimit 1,500) else `..FB0` (with a debug string "NewSupportHeight: >%.2fcm").
- Data: PlacementFlags serialized 9 on 14 assets, 1 on the FOB, absent on 23 (native 11); MaxStack serialized values 0, 1, 4, 5, 6, 100, unset = 2 (table in the JSON). The existing page said "9 for almost every structure"; that counted only serialized values and is corrected.
- Not found: a reader of bit 4 (CanPlaceVertically; no asset sets it) and bit 1 (AllowRotation, presumably the rotate action); the direction of the two tag lists at +0x130 / +0x150.

## 3. Weak spots (critical-hit spots)

Status: **FOUND**. They are a hammer build-amount bonus.

- `WDItemExtensionData_CriticalHitSpotManager` on each hammer item (`ID_SmallHammer`, `ID_MediumHammer`, `ID_LargeHammer`): `BuildAmountWhenTargetIsHit` 3 / 5 / 8 against `BuildAmount` 0.5 / 1 / 1.5; `CriticalHitSpotMaxDistanceAwayFromPlayerView` 290 / 290 / 340; `...MaxDegreesFacingAwayFromCameraAtSpawn` 135; unnamed floats 0.5 and 20.0 and an int 1; colours `FFCF02` / `FFEFD1`. Native defaults for the rest (ctor `0x85E0960`): `BuildAmountPerSecondWhenTargetIsTracked` 4.0, speed 30, rotation lerp 0.02, distance requirement squared 4, relocation mode EyeLine (`EWDCriticalHitSpotRelocationMode`: Roam 0, EyeLine 1), life span 0, spawn delay 0.
- `B_CriticalHitSpot`: Actor, `Box` collision profile Custom with every channel Ignore (including WDProjectile and WDMeleeHit), a `B_CriticalHitSpotDecalComponent` (material `M_CriticalHitSpotDecal`, size 6.4 x 12.8 x 12.8), `ReceiveTick` only calls `DrawDebugSphere(25)`. `UserConstructionScript` sets the box extent from the decal size.
- `UWDItemExtension_BuildBuildable.RequestCriticalHit(Buildable, bool)` is the RPC; `UWDItemExtension_BuildBuildable.CriticalHitSpotManager` holds the manager.
- No damage row, GE or reward references weak spots (`grep -ri "CriticalSpot\|CriticalHit" data/ assets/data/` finds only stage files, buildable data assets and hammer items).
- `bUsesCriticalHitSpots` native default true (`0x311`); false on Barbed Wire, Recon Tent and the part assets.

## 4. `SafeZonePlacementCondition`, `WithinLadderBoundsPlacementCondition`

Status: **FOUND**.

- `B_SafeZonePlacementCondition_C` (parent `WDPlacementConditionBase`): CDO `MinDistanceToSafezone` = 300.0. `IsSatisfied` bytecode: `IsValid(Instigator)`; cast to the gameplay-tag interface; `HasAnyMatchingGameplayTags([State.Location.SafeZone.Alpha, .Bravo, .Charlie, .Hostile])` -> out reason tag `UI.Interactions.PlacementWarnings.InSafeZone`, return false; else `GetAllActorsOfClass(B_SafeZone)`; for each, `TriggerVolume.GetClosestPointOnCollision(SpawnTransform.Location)` and if `<= MinDistanceToSafezone` -> reason tag InSafeZone, false; end true.
- `B_WithinLadderBoundsPlacementCondition_C` (parent native `WDWithinLadderBoundsPlacementCondition`): CDO `BlockRadius` = 100.0. The class VFT `UWDWithinLadderBoundsPlacementCondition_VFT` differs from `UWDPlacementConditionBase_VFT` in slot 0 and slot 86; slot 86 is `sub_147725250` (RVA `0x7725250`), a sphere overlap (shape type 2, radius `this+40` = BlockRadius, trace tag `WDLadderPlacementCheck`) that returns false with a reason tag if any overlapped actor is a `WDMoverLadder` (class `/Script/WDGame.WDMoverLadder`, resolved via `sub_146DC92B0`).
- Unit: Unreal units (cm).

## 5. Builder's Radio

Status: **FOUND**. A music radio.

- `B_Radio` (parent `WDBuildableSpawnedActor`) has `WDWorldInteractableComponent` with `InteractionContextsDisplayOrder` Power, Station1..Station7; `B_Radio_InteractionContext_TogglePower` (station number 0 <-> previous) and `..._ChangeStation_1..7` (set the number) call `B_Radio_AudioHandler.Change Station Num`; the handler replicates `Curr Station Num` / `Prev Station Num` (push model, RepNotify), triggers the audio component parameter `Play` and sets a "Next Song Timer". `B_Radio_World` is the same as a plain world actor; `B_WDWorldRadioSpawnComponent_PreLobby` spawns it in the pre-lobby.
- `bRegisterWithFOB` (native default false) is set on Radio, Refuel Station and Repair Station only. The FOB component (`WDForwardOperatingBaseComponent`) keeps `TrackedBuildablesCount` (replicated, per tag) and a `WDFOBRulesetData.LimitFOBBuildables` map; placement condition `WDLimitedByFOBCondition` enforces it (limits 1 / 1 / 4). Nothing else was found tied to registration (no spawn, call, supply drop or UI).

## 6. Drill Rig "magnet"

Status: **FOUND (settings, units Derived) / NATIVE (zone movement)**.

- `DA_Buildable_HotzoneMagnet` (`WDBuildableHotZoneMagnetDataAsset`): InitialDelay 15, Recharge 900, MinimumFuel 2,000, DurationPerFuel 0.03, MaxFuel 10,000, Cost 2,750, MaxHealth 2,500; others at native defaults (ctor `0x85E05D0`): ActivateInteractionDuration 10, ActivateInteractionRange 200, FuelInteractionRange 200, ActivatedHotZoneMagnetSpeed 5.0, SizeMultiplier (0.5, 0.5, 1.0); default MaxFuel 1,000, recharge 300, min fuel 200, per fuel 0.3, initial delay 10 (all overridden by the asset); actor `HotZoneTowerRewardRange` 2,500 (ctor `0x85E6C90`).
- Units: timers in seconds (BP `UpdateMagnetCooldown` divides current by total cooldown; `UpdateMagnetDuration` uses `GetActiveHotZoneMagnetDuration` current/total/target); run time = fuel x 0.03 s (60 s at the 2,000 minimum, 300 s at full 10,000). Fuel is the FOB's Fuel Supplies (`FuelSuppliesResourceItemTag` `Id.Item.FuelSupplies`; `OnFOBItemSlotUpdated`; strings "FOB REQUIRED", "MIN FUEL").
- The world magnet: `HotZoneMagnetRuntime.WDHotZoneMagnetGameStateComponent` (CDO in `B_HotZoneMagnetGameStateComponent`: `TowerControlRechargeDuration` 900, `ActivatedHotZoneMagnetDuration` 180; native ctor `0x8566570`: recharge 150, duration 120, speed 3.0, size multiplier (0.6, 0.6, 1.0)). Methods `OnHotZoneMagnetTowerActivated(towerNumber, current, total, NewLocation, ...)`, `GetControlZone`, `GetHotZoneCacheExtents`, `GetIsHotZoneMagnetAtLocation`. `B_HotZoneMagnet` (tower + keypad, `HotZoneMagnetCodeAttemptsTimePenalty` 30) and the data coordinator `Code`. STRINGS_HotZone: "TOWER 0{0}", "ALL TOWERS REQUIRED FOR CODE", "ENTER CODE", "DRILL ACTIVE". Client function `sub_148571F80` (RVA `0x8571F80`) picks the magnet in a 22.5 degree cone (cos 0.9238795) and multiplies the control zone cache extents by the size multiplier at `this+248`.
- Reward rows: `DT_Reward_Cash_HotZoneMagnet` MagnetActivated 5,000, MagnetDestroyed 150 (instigator 200), CapturedTower 250 (hostile 1,000); `DT_ChallengeRewards_SessionEvents_HotZoneMagnet`: TowerCaptured formula with BaseReward 250, MagnetActivated 2,500 (+500 XP), MagnetDeactivated 2,500.
- Not read: the native logic that moves and resizes the zone; which speed/size pair a rig activation uses.

## 7. Cash and XP rows; Placed vs Placed-in-FOB selection

Status: **ABSENT (rows), NATIVE (selection)**.

- The three tables `DT_Reward_Cash_BuildableBuilt`, `...Placed`, `...PlacedInFOB` have the same 11 row names: `Meta.Progression.Context.DefaultReward` plus HBlock, TallHBlock, Gate, FOB, HBlockQuadWall, Mortar, BarbedWire, TankTrap, AirRaidShelter, Bunker. No row for MistralAA (Talon 9K-SAM), Phalanx (Vanguard CIWS), Loudspeaker, STN_05 (Stingray), MGNest, WoodBase or Shelter in these tables, in `DT_CashRewards`, in `DT_ChallengeRewards_SessionEvents_Buildables` or in the lookup registries (`grep` over `data/` for the tags and names finds only vehicle, spotting and destroy rows).
- Default rows: Built base 1 (owner 0.5, friendly 1), Placed base 1 (owner 1, friendly -1), PlacedInFOB base 1 (owner 0, friendly -1). Whether an unlisted id falls back to it is native.
- Selection: `DR_CashRewards` (`DataRegistry`, `RegistryType` CashRewards, `ItemStruct` WDCustomRewardTableRow) has 15 `DataRegistrySource_DataTable` sources in this order: BuildableBuilt, BuildablePlaced, BuildablePlacedInFOB, ControlZoneReward, DeployableDestroyed, DeployedSupplyCrate, EndGameFactionReward, Heal, HotZoneMagnet, PlayerKill, Refuel, Repair, Revive, VehicleDestroyed, VehicleTransport. Because the three buildable tables share row names, stock Unreal first-source-wins would resolve every id to the Built row; whether the game uses a different lookup is not shown by the data. No other asset names the tables (`findname` finds them only in the registry), and the native consumer was not located.
- Visible per-placement reward in data: `ST_Challenges_SessionEvents_Buildable_SchematicPlaced` listens for `WDSchematicPlacedInFOBMessage` (tag `Event.StateTree.SchematicPlaced`), adds `Challenges.Context.Instigator.InControlZone` / `InHotZone`, calculates `Challenges.Rewards.Buildables.SchematicPlaced` (`DefaultValue * InstigatorZoneModifier`, DefaultValue 10, HotZoneFactor 2, ControlZoneFactor 1, no XP resource) and grants the tag `Meta.Progression.Resources.MatchScore.SchematicPlacedInFOBScore` (`DT_Rewards` ResourceValue 5; `DT_CashRewards` RewardAmount 5, +5 additive in a hot zone).

## 8. Is the FOB a spawn point?

Status: **ABSENT in the client data** (server side not excluded).

- FOB Blueprints (`B_ForwardOperatingBase`, `B_ForwardOperatingBaseComponent`, `B_Buildable_ForwardOperatingBase_Manticore`, `B_PlacementBuildable_ForwardOperatingBase_Manticore`) contain only `WDBuildable_ActorSpawnLocation` (anchor for sub-actors) and `SpawnSystemAttached` (VFX). `WDForwardOperatingBaseComponent` members: supplies, damage state, state, owner player state, `PlayersInFOBRange`, `TrackedBuildablesCount`, `DespawnDelayAfterDestroyed`, `FuelConsumptionRate`; no spawn data.
- Spawn system classes (`WDSpawnManager` with `FactionTag`, `SpawnQueryPoints`; `WDSpawnVolume` with faction tag and allowed/disallowed objects; `WDSpawnQueryPoint`; `WDPlayerSpawnManagerComponent` empty) have no FOB reference. `grep` for spawn tags in `data/`: `Trackers.Type.Spawn` (spawn board trackers), `Vehicle.Variant.Land.Tracked.SpawnVehicle.*` (spawn transport vehicle), `Challenges.Context.Instigator.InSpawnVehicle`; none tied to the FOB. FOB texts (tutorial, tooltip, loading tips, placement warnings) mention claiming territory, supplies, repair and refuel; none mention respawn.

## Wiki updates

- `_wiki/equipment/builders-radio.md` -> function: "exact function in play is not yet known" / "data does not say what the radio does" -> a music radio with a power toggle and seven stations; registering only counts it toward the 4-per-FOB limit. Placement checks: "ladder bounds and safe zone checks, whose tests are not yet known" -> no ladder within 1 m (100 units) of the spot, and not within 3 m (300 units) of any safe zone or while inside one. Weak spots: "what the weak spots do is not yet known" -> hammer build bonus (3 / 5 / 8 build amount on a weak-spot hit against 0.5 / 1 / 1.5).
- `_wiki/equipment/drill-rig.md` -> add: run time = fuel x 0.03 s (60 s at the 2,000 minimum, 300 s at 10,000 full), 15 s start delay, 900 s recharge, activation is a 10 s hold within 2 m, fuel comes from the FOB; the rig is the buildable version of the map's hot zone magnet and draws the hot zone toward it (movement itself not read). Remove "ladder bounds check and safe zone check, whose tests are not yet known": the Drill Rig lists neither (only FOB radius, placement zone and control zone). Weak spots line -> hammer bonus.
- `_wiki/equipment/forward-operating-base.md` -> "does not say whether the FOB acts as a spawn point ... not yet known" -> no spawn data tied to the FOB in the client files; the FOB is a claim, supply and build-radius point. "safe zone check and ladder bounds check" tests -> same wording as above.
- `_wiki/equipment/hammers.md`, `_wiki/equipment/buildables.md` (stages and weak spots, near "the hit that lands on a weak spot adds more") -> add that weak spots are hammer-only (bullets and melee cannot hit them), move between positions on the structure, and the factors are 6 (Small), 5 (Medium) and 5.3 (Large); Barbed Wire and Recon Tent do not show weak spots even though their stage files list positions.
- All structure articles with "weak spots ... is not yet known" lines (`barbed-wire`, `bremer-wall`, `bunker`, `door`, `gate`, `hedgehog`, `hesco-walls`, `indirect-fire-shelter`, `recon-tent`, `recon-tower`, `refuel-and-repair-stations`, `sandbag-wall`, `shelter`, `wood-base`) -> replace with the hammer-bonus statement; for Barbed Wire and Recon Tent say the weak spots are switched off.
- `_wiki/equipment/bunker.md`, `door.md`, `gate.md`, `recon-tower.md`, `indirect-fire-shelter.md`, `hesco-walls.md` (Hesco Wall = quad wall) -> add: the finished structure is made of separate parts (list in section 14.1 of the Buildables page), each with its own health.
- `_wiki/equipment/buildables.md` and each structure's placement note -> "ladder bounds check": no ladder within 1 m; "safe zone check": not within 3 m of a safe zone (and not while in one); stacking: a structure can be placed on top of another only if the lower one is complete and allows it, up to its stack limit (Barbed Wire, Recon Tent, Sandbag Wall, Tank Trap, stations: 100; Hesco Block 5; MG Nest 5; Wood base 4; Radio and most stationary weapons 6; FOB, Gate, Shelter, Bremer Wall, Indirect Fire Shelter 1; Recon Tower parts, Drill Rig 0).
- Reward notes for the Talon 9K-SAM, Loudspeaker, Vanguard CIWS, Stingray, MG Nest, Wood base and Shelter that say "no cash row" stay valid; add that the reward tables have a one-cash default row and that placing a schematic in a FOB pays a flat 5 cash resource (+5 in a hot zone) for every structure.
