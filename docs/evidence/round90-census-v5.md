# Round 90: census v5 (what is still workable)

Date: 2026-10-27. Branch `r90-cen`, script `_tools/coverage_census.py` (unchanged), main at `f4bd67f5`. Static only: the `data/` junction, the published pages, the earlier backlogs and evidence files. No game run, no executable work, no server. The ranked backlog for the next round is `E:/r38/shared/BACKLOG-v5.md` (same findings plus the cluster briefs).

## 1. Coverage at three levels, with deltas against v4

| Level | v4 (round 84) | v5 (now) | Delta |
|---|---|---|---|
| Asset names, all files | 6,377 of 6,892 (92.5%) | 6,377 of 6,894 (92.5%) | +2 files exported (two tag lists, below) |
| Asset names, data scope | 4,822 of 4,825 (99.9%) | 4,822 of 4,827 (99.9%) | 5 unnamed files, none a gameplay asset |
| Asset names, data, non-catalog Markdown page | 4,774 (98.9%) | 4,780 (99.0%) | +6 |
| Audio and UI widgets (out of scope) | 1,547 of 2,059 (75.1%) | 1,547 of 2,059 (75.1%) | 0 |
| Row names (631 DataTables, 3,257 testable rows) | 2,850 (87.5%) | 2,875 (88.3%) | +25 rows |
| Property names (435 export types, 2,295 distinct names) | 1,525 (66.4%) | 1,623 (70.7%) | +98 names |

Unnamed data files (5): [`DA_MF_AK74-M_Default`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/AttachmentMuzzleFlashData/DA_MF_AK74-M_Default.json) and [`DA_MuzzleFlash_AK74-M`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/VFX/Weapons/MuzzleFlashes/MuzzleFlashData/AssualtRifles/DA_MuzzleFlash_AK74-M.json) (muzzle flash, visual), `DefaultGame.excerpt.ini` (an excerpt on purpose), and the two new tag lists `Config/Tags/SquadTags.ini` and `Config/Tags/Meta/MetaWagerGameplayTags.ini`. The tags inside the two lists are already published (15 `Squad.*` tags in `Wardogs_GameplayTags_v1`, the wager tags in `Wardogs_DataTables_Economy_v1`); only the file names are not written down. Not a gap.

Row level: 382 rows are unmentioned in 21 tables. 349 are UI or animation ([`DT_FP_Mirroring`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Animation/Blueprints/Character/Layers/DT_FP_Mirroring.json) 147, `DT_Settings_*` 197, [`DT_Settings_Keybindings`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Settings/Keybindings/DT_Settings_Keybindings.json) 5) and out of scope. The other 33 are cosmetic or already published under another spelling: `DT_PostProcessEffects*` (screen effects), `DT_RadialWheelSlotType_BuildToolData` and tooltip tables (UI), [`DT_Reward_Cash_HotZoneMagnet`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Gamemode/Data/CashRewardsDataTable/HotZoneMagnet/DT_Reward_Cash_HotZoneMagnet.json) (all 8 rows are in the Buildables and Rewards pages under their resource-tag names `Meta.Progression.Resources.MatchScore.*`; the census tests the `Context` spelling), the FOB `DT_InteractionContext*` rows (interaction prompts), `FactionWinBonus` (named in `Wardogs_Meta_v2`), and [`CT_Projectile_DragCoefficients`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/Curves/CT_Projectile_DragCoefficients.json) `GS (Sphere)` and `RA4 (.22LR)` (labels written without the spaces and brackets). No row-level item is left.

## 2. Field level: the 672 unmentioned property names, by family

The census lists a name as unmentioned when it is not a whole token on any published page. For every one of the 202 export types that still has a miss, the pages were searched for the plain-English wording or the value, and the export was read for the value. Counts are names, rounded.

| Class | Names | What it is |
|---|---:|---|
| DOCUMENTED (false positive) | about 300 | Prose or generated tables use plain English or a curve name instead of the property name |
| WORKABLE | about 65 | 14 types where the value is in the export and on no page |
| CLOSED | about 305 | Cosmetic, camera, UI, AI plumbing, engine serialisation, procedural scatter, animation |

### DOCUMENTED, with the page that holds it

| Types | Where it is documented |
|---|---|
| `BHRotary/MWheeled/MTracked/BHAirplaneVehicleConfigDataAsset`, `BHAirplane/BHRotaryFlightDataAsset`, `MTrackedVehicleWheelData` (about 130 names) | `Wardogs_VehicleConfigFields_v1` (horn hold, ground trace, exit damage type and curve, drag), `Wardogs_FixedWingFlightModel_v1` section 4 (control influences, flaps, airbrake, throttle, gear), `Wardogs_VehicleControlAssists_v1`; gameplay cue tags are stated as cosmetic |
| `BHGroundMovementData`, `BHClimbingData`, `BHMantlingData`, `WDFallingData`, `BHVaultingData` | `Wardogs_MoverTesting_v2` section 4 ([`CRV_StanceSpeedStaminaMultiplier`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/CRV_StanceSpeedStaminaMultiplier.json), [`CRF_Falling_SurfaceAngleToAirControl`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/MoverTesting/Curves/Falling/CRF_Falling_SurfaceAngleToAirControl.json), push-off) and `Wardogs_PlayerMovement_v1` line 166. The transition curves are animation (CLOSED) |
| `WDItemExtensionData_MedKit` (8) | `Wardogs_Medical_v1` heal table (self 35 over 5 s, other 15 over 1.5 s) and usage-rate rows; round 85 V4-04 |
| `BH_PrototypeMaskedScopes_ExtensionData_C` (12) | Sights and Optics page, handheld block (round 89) |
| `PDA_Explosion_C`, `PDA_MuzzleFlash*`, `PDA_PhysicalMaterialResponse_C`, `PDA_VehicleProp_C` (about 85) | `Wardogs_FX_Field_Tables_v1` (round 89), column headings in plain English |
| `PDA_SmokeGrenade_C` (3) | `Wardogs_GameplayCues_v2` (Total Duration 6 s, Fade In Time 2 s) |
| `WDItemExtensionData_RangedWeapon` (2 of 4 names), `WDItemExtensionData_Holdable` crosshair names | `Wardogs_RangedWeaponFields_v1` (iron-sight camera offset, sight position offset, crosshair override) |
| `BHAimAssistSettingsData` ADS curves | `Wardogs_AimAssistCurves_v1` (`C_AimAssistPullStrengthDistanceCurve_*_ADS`) |
| `WDCustomInventoryOperationRule_Reload` | `Wardogs_GameMechanics_v2` reload rules (columns Context, Insert ammo type, Weapon slot) |
| `WDVehicleWeaponDataAsset` | `Wardogs_VehicleTurretControls_v1` (rotation sensitivity, limits) |
| `WDFactoryInvestment`, `WDMoverWeightData`, `WDFreeVehicleSpawnerDataAsset`, `WDDemolitionRule_Explosion`, `BHDemolitionDataAsset`, `BHRotaryVehicleSensorsDataAsset`, `WDItemExtensionData_BuildTool` (non-VFX names) | FactoryInvestment pages, MoverTesting weight classes, Vehicles_v2 free-spawner rules, Demolition_v2 ruleset table, VehicleHandling (altitude sensor), Buildables_v1 hammer table |
| Vehicle fragments (`MVF_Seats`, `WD_MVF_*` except the destruction invoker, `ModularVehicleSlot`) | Vehicle Assets and Vehicle Handling pages |

### WORKABLE (14 types; the value is in `data/` and on no page)

| Type | Names | Example values read | Item |
|---|---|---|---|
| `WDVehicleGameplayComponentsDataAsset` (23 assets) | `InactivitySettings`, `InventorySettings`, `LockSettings`, `PassengersCameraSettings` | `InactivityLifetimeOutSafeZone` 90 s on [`DA_GameplaySystems_ROT_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/ROT_02/Content/Data/DA_GameplaySystems_ROT_02.json); `bIsInventoryAccessible` true | V5-01 |
| `WDVehicleInteractionsDataAsset` (28) | `bAllowSameFactionOccupantsOnly` | true on 6 assets | V5-01 |
| `WD_MVF_DestructionInvokerFragment` (14 vehicles) | collision box, `DamageRecievedWhenChunkDestroyed`, `CounterForceMultiplier`, `VelocityOffsetMultiplier` | ROT_02: box 1000 x 300 x 180, 200, 0.0, 0.2 | V5-01 |
| `WDInventoryFragment_Armor` (14) | `DamageContextTag` | `Meta.Damage.Armor.Ghillie`, `Meta.Damage.Armor.Heavy`, helmet equivalents | V5-02 |
| `WDItemExtensionData_Throwable`, `_RangedWeapon`, `_RangedBow_C`, `_Appliable`, `_Keycard`, `BHInventoryFragment_Droppable`, `_SubSlotSupport` | `bDropOnInterrupt` (false on 14), `ItemToConsume` (C4, IED), `bDropAfterUse`, `FireChargeTime` 0.5, bow `TimeToWaitBeforeCompletion` 0.33, keycard alignment and number (faction; 1 or 2), `ThrowingForce` 300 | | V5-02 |
| `WDItemExtensionData_Placeable` (4) | `PlacementCollisionSize`, `PlaceableInitData`, `BlockedActorClasses`, `bCanPlaceOnOtherPlaceable`, `BlockedReason` | init health 1.0 on three, 100.0 on one; blocked by wheeled and tracked vehicles, or by players | V5-03 |
| `BH_FuelCan_ExtensionData_C`, `BH_VehicleRepairToolExtensionData_C` | `Trace Distance` 500, `ChargesToUse` 1 | | V5-03 |
| `WDItemExtensionData_BuildableDismantle`, `_CriticalHitSpotManager` | `DismantleTraceDistance` 275; spot distance 290 / 340 and 135 degrees | | V5-03 |
| `BH_SpottingExtensionData_C` | `TrackingBoundsDiameter` 350, `bShowDistance`, `bShowHitData` | | V5-03 |
| `WDBuildableDataAsset` | `FactionBuildableOverrides`, `PlacementClass` (FOB, per faction) | | V5-06 |

### CLOSED (about 305 names)

- Cosmetic or camera: `SkeletalMeshComponent`, `MVF_SkeletalMesh`, `MVF_StaticMesh`, `WDMutableCharacterComponent`, `WDItemExtensionData_Mutable`, `PDA_MicroBiome_C`, `PDA_MBCluster_C`, `PDA_MBScatter_C`, `PDA_SplinePCG_C`, `PDA_ClusterPCG_C`, `DA_GroundDetail_C`, `PDA_RVTD_C`, `PDA_LightSettings_C`, `BHExhaustDataAsset_C`, `CurveLinearColor*`, `CurveVector` channels, `MCameraShakeEvent`, `WDCameraModifier_*`, `WDCharacterModifier_*`, spring-arm assets, `WDFirstPersonCameraComponent`, `PoseSearch*`, `SkeletalMeshLODSettings`, `KawaiiPhysics*`, `WDRagdollMovementData`, holdable sprint blend rates and `AttachTransform`, ladder animation curves, `WDShootingRangeTutorialFlyByData`.
- UI and input: `WDUIRadialWheelSlotTypeDataAsset`, `WDUIBuildTool*`, `WDUIDeathmatchStatusData`, `BH_ExtensionData_MedicalPrompts_C`, `W_VehicleVendor_Stat_*`, `WDGameFeatureAction_AddWidgetElements`, `BHInputAction` flags, `Input*Modifier*`, `PlayerMappableInputConfig`, `BHAxisConfigDataAsset`, `WDAimAssistInputModifier`.
- Engine serialisation or test: `SCS_Node`, `SimpleConstructionScript`, `TimelineTemplate`, `BlueprintGeneratedClass`, `StateTree` frames, [`B_CheckTimeDiff_C`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/StateTrees/ST_Challenge_TimePlayed.json), [`B_GetTimeDiff_C`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/StateTrees/ST_Challenge_TimePlayed.json), [`B_GetUtcNow_C`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Meta/Missions/StateTrees/ST_Challenge_TimePlayed.json), [`B_TargetDummy_C`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/TargetDummy/B_TargetDummy.json) (debug dummy), `WDPerformanceCaptureWorldData`, `SmartObjectDefinition`, `WDGameplayBehaviorConfig_Action`, `BlackboardKeyType_*`.
- AI plumbing without a player number: 28 `EnvQuery*` generators and tests (`VerNum`, spacing, cone degrees), `WDAICharacterConfigData.ShootingConfigData`, influence maps. Kept as the optional item V5-13.
- Hashed names: 121 distinct `_aaa` property names sit in these 435 types (about 2,645 uses in the carried count). No plaintext oracle exists in the files (the format is decoded, no unsalted hash fits, the SDK dump carries the same hashes), so nothing can be named without the game or the protection layer. CLOSED.

## 3. Open phrases in published pages

Searched `content/`, `game-features/`, `pipelines/`, `plugins/`, `_wiki/`, `season-2-changes/`, `categories/` and the root pages. Line hits: "not yet known" 19, "not traced" 171, "not decoded" 68, "unknown" 23, "NOT LOCATED" 5, "unconfirmed" 14, "not resolved" 18, "not verified" 20, "still open" 7, "not located" 5, "not found" 15. Classified by topic, as in v4:

| Class | Lines | Detail |
|---|---|---|
| Stale, fixed this round | 10 | section 4 |
| Still open, backlog item | about 12 | V5-03 `Items_v2` 268 and 485 (ammo crate placeable); V5-08 `FixedWingFlightModel` 58 and 160 (drag area formula, trim row rule); V5-09 wiki `forward-operating-base` 46 and `building` 184 (FOB spacing shape); V5-10 `FireAndUtility` 207 (placeable reach and angle); V5-11 `AmmoPacking` 53 and wiki ammo-packing; V5-12 `ItemActions` section 9 (input binding); V5-05 `Medical_v1` 218 (Medical Bag steps); V5-04 `FireAndUtility` 52 (Molotov friendly and self damage) |
| Closed (SERVER, ABSENT, PROTECTED, needs a running game) | about 60 | skill unlock level and cost (wiki driver, pilot, recon, support), Medic skill magnitudes (`Medical_v1` 152-182), `BleedOutRevivePenaltyOffset` and `CriticalReviveHoldThreshold` (v3: no reader), hit settlement under latency, resuscitator time in play, FOB `DoNotTakeDamage`, build supplies refund and build time scale, HitRegistration O-3, O-8, O-12, O-13, smoke versus AI sight, "feel" claims in the wiki "Not yet known" sections, vehicle MG self pass-through, PvE names and rewards, Deathmatch regeneration tick body |
| Cosmetic, audio or UI, out of scope | about 70 | Audio_v2 notes, Itemsmith widget layouts, Skins textures, VFX leaf gradients, ExternalAssets chunk flags, Environment ground detail, PlayerMovement gun-bob consumer, camera fade priority |
| Method labels | rest | "Derived, no native proof" and similar labels; not open items |

## 4. Stale lines fixed (prose only, no numbers changed)

| File and place | Was | Now | Where it is settled |
|---|---|---|---|
| `game-features/Wardogs_FireAndUtility_v1.md`, fire patch size | "The total spread of the 15 patches is native and not decoded." | the patches are switched on by the field's spread speed (the `+0x2D0` row above) | [round 88 na](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round88-na.md) item 4 |
| `game-features/Wardogs_GameFeatures_Vehicles_v2.md`, restock note | "restock semantics and tag are not decoded" | only the five stationary weapons restock, from the FOB supply inventory; native default of 1 | [round 40](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round40-vehicles-explosives.md) R40-8 (round 85 hygiene had left this as open) |
| same file, limitations | rotary control assist conditions "not decoded" | tabled | `game-features/Wardogs_VehicleControlAssists_v1.md` |
| `game-features/Wardogs_VehicleHandling_v1.md` | "`DA_ArcadeControls_*` are not decoded" | tabled | same page |
| `game-features/Wardogs_GameFeatures_Items_v2.md`, damage on buildables | stacking "not decoded" | each `Percentage_Ongoing` entry adds a percentage of the running value, in selection order (infantry hit path); no combined multiplier given for buildables | `pipelines/Wardogs_DamagePipeline_v2.md` section 6 |
| same file, limitations | requirements "not decoded", priority "unknown" | matching rules | pipeline section 4 |
| `content/Wardogs_GameMechanics_v2.md` | `Percentage_Ongoing` formula "not decoded" | formula stated | pipeline section 6 |
| `game-features/Wardogs_GameFeatures_Challenges_KOTH_v2.md` | reward values "not resolved in this doc" | pointer to the formula-row item that follows | next bullet, round 88 nb |
| `game-features/Wardogs_Challenges_v1.md`, section 11 | "Nothing on this page is read from the game code" | pointer to the reward evaluator | [round 88 nb](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round88-nb.md) |
| `content/Wardogs_Maps_v2.md`, sight blockers | "what a sight blocker is for ... not decoded" | the one known caller of the sight-blocker query is the aim-assist target manager; whether this asset feeds it is not shown | `FireAndUtility_v1` "What smoke blocks" |

Left alone on purpose: `Items_v2` 268 and 485 (ammo crate placeable data, now V5-03).

## 5. Models

The pak listing (66,550 packages, `E:/r86/work/mdl/all/files.txt`) was searched again for gameplay meshes outside `Environment/` and [`ExternalAssets/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/ExternalAssets). Vehicles (23 ids with all variants), infantry (the player asset, which all non-vendor `SK_` presets name), the 32 buildables, 6 placed explosives, 6 crates, the FWG_01 airplane and the six stationary weapons are covered by round 86 with no gameplay-collision gap beyond what it recorded. Two gameplay object groups are not in the viewer:

- Interactable doors and smashable windows. [`GameMechanics/WorldInteractable/Objects/EnvironmentalObjects`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects) holds about 30 door decorator assets (`D_Interactable*`, breach and swing curves) and the `SmashableWindow` (`SM_BrokenWindow01_base`, nine `SM_VFX_WindowPiece*`). Their meshes are Environment kit pieces (for example `SM_Commercial_Door_01a_L/R`, `SM_Ind_Door_*`), so round 86 excluded them with the level kits. They block bullets and can be breached, so they are gameplay objects (V5-07).
- FOB faction mesh placement and the buildable foundations, plus the `BP_Drone_Projectile` (STN_05) Blueprint. Recorded as open in round 86; the Blueprint dumps under `E:/r86/work/bp` are the likely source (V5-06).

Everything else outside the viewer is level geometry (about 10,600 meshes under `Maps/Worlds/Europe` and `NorthAmerica`, plus the Environment and ExternalAssets kits), cosmetic VFX meshes, held-item meshes or editor meshes, and stays out of scope as recorded.

## 6. Verdict

Not everything is closed. Twelve items remain with a concrete path and some player or data value (seven static, five native), plus one optional low-value item. They are in `BACKLOG-v5.md` in four clusters. Everything else in the three coverage levels is documented, cosmetic, or closed by an earlier recorded reason.

## 7. Checks

- `python -I _tools/coverage_census.py --top 60 --json <scratch>`: figures in section 1.
- `python -I _tools/check_links.py`: 0 broken (after the prose fixes).
- Secrets grep on `git diff main...HEAD`: no hits (run before the final commit).
