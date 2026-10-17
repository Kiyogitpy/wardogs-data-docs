# Gap resolution — IDA (static RE)

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Gaps that need **static disassembly of the game binary** to answer — typically 'how does this formula combine', 'what order are modifiers applied', 'what's the stacking rule'. 32 total across the project.

The sole IDA map is
`E:/Reverse_Engineer/wardogs_analysis/IDAMappings/5.7.4-516586+++Wardogs+Live-Wardogs.idmap`.
See the [mapping policy](../../mappings/README.md); use that file directly.

Resolution workflow per gap:

1. Load `WardogsClient-Win64-Shipping.exe` into IDA
2. Read the sole external `.idmap` above with a compatible binary-v2 importer; validate selected records against the image before applying them
3. Open the SDK class file for the asset involved (from `../sdk/raw/`)
4. Find the UFunction that reads the asset (xref the FName hash)
5. Follow the function body; document the formula or ordering
6. Update the data doc's 'How Values Combine' section with the finding

## Catalog

### [Wardogs_AllVehicles_Stats_Damage_v1.md](Wardogs_AllVehicles_Stats_Damage_v1.html)

- **6. Still not pulled / limitations**  →  _**Priority order:** with every `PriorityIndex` at -1, the order applied when several entries match is not shown._
- **6. Still not pulled / limitations**  →  _**Tag definitions:** the tag names and their hierarchy are in the config files; see [Wardogs_GameplayTags_v1.md](../../Wardogs_GameplayTags_v1.md). How a requirement tag matches its child tags is engine logic and is not in those files._

### [Wardogs_Demolition_v2.md](Wardogs_Demolition_v2.html)

- **6. How Values Combine**  →  _**Which hits can demolish (likely):** a demolition asset's ruleset is tested against the incoming damage source (explosion rules) or the colliding vehicle (vehicle rules). A match appears to permit demolition. The export does not state the trigger logic._

### [Wardogs_Destruction_v2.md](Wardogs_Destruction_v2.html)

- **5. How Values Combine**  →  _The two curves are independent, one-input functions. Combining them with each other or with other systems is not shown in the export._

### [Wardogs_Developers_v2.md](Wardogs_Developers_v2.html)

- **3. Still Not Pulled / Limitations**  →  _**The demolition component and its instances are not in this dump.** The meshes, the destruction logic and the collision profile definition itself are outside this folder._

### [Wardogs_GameFeatures_AI_v2.md](Wardogs_GameFeatures_AI_v2.html)

- **10. How Values Combine**  →  _Each test has a `TestPurpose` (`Filter`, `Score`, or both) and a `TestOrder`. Filters run first; scoring tests then combine._

### [Wardogs_GameFeatures_Challenges_KOTH_v2.md](Wardogs_GameFeatures_Challenges_KOTH_v2.html)

- **6. Limitations**  →  _Per-state logic (the actual calculation in `Calculate Reward`) is compiled StateTree bytecode. This doc names states and tags but does not decode the expressions._

### [Wardogs_GameFeatures_Deathmatch_v2.md](Wardogs_GameFeatures_Deathmatch_v2.html)

- **8. Still not pulled / limitations**  →  _**Spawn logic.** `B_DeathmatchSpawner` is a Blueprint and is not decoded._

### [Wardogs_GameFeatures_Emotes_v2.md](Wardogs_GameFeatures_Emotes_v2.html)

- **5. Still Not Pulled / Limitations**  →  _**Emote trigger and playback logic** (what runs when an emote is used) is not decoded._

### [Wardogs_GameFeatures_Items_v2.md](Wardogs_GameFeatures_Items_v2.html)

- **11. Still Not Pulled / Limitations**  →  _**Damage modifier requirements.** Entries with instigator, target or hit-location requirements are not decoded. Their meaning and priority order are unknown._

### [Wardogs_GameFeatures_PvE_v2.md](Wardogs_GameFeatures_PvE_v2.html)

- **8. Still not pulled / limitations**  →  _**Scenario logic.** How quest objectives and the `ScenarioData` values drive the mission flow is in BP and runtime code, not in this folder._

### [Wardogs_GameFeatures_Vehicles_v2.md](Wardogs_GameFeatures_Vehicles_v2.html)

- **15. Still not pulled / Limitations**  →  _**Vendor stat widgets.** `W_VehicleVendor_Stat_*` widget objects (Seats, MaxSpeed, FuelCapacity, FuelEconomy, CounterMeasures, Weapons) are referenced by each stats asset but their display logic is not decoded._

### [Wardogs_GameFeatures_WDAutomation_v2.md](Wardogs_GameFeatures_WDAutomation_v2.html)

- **3. Still not pulled / limitations**  →  _**Logic sequences.** The sequences themselves are not in this dump. The scan points to a directory that is not part of this folder._

### [Wardogs_GameFeatures_Weapons_v2.md](Wardogs_GameFeatures_Weapons_v2.html)

- **10. Still not pulled / limitations**  →  _**`WDItemInputBehavior_ActivateAction`** exports with empty payloads, so the action logic is not visible._

### [Wardogs_GameFeatures_WorldFeatures_v2.md](Wardogs_GameFeatures_WorldFeatures_v2.html)

- **6. Still not pulled / limitations**  →  _**StateTree logic.** The three challenge StateTrees and the full set of state nodes are summarised, not decoded. Triggers and conditions are not confirmed._

### [Wardogs_GameMechanics_v2.md](Wardogs_GameMechanics_v2.html)

- **15. Still Not Pulled / Limitations**  →  _**Operation semantics.** `Percentage_Ongoing` is the operation name on the modification entries. Its exact formula (additive, multiplicative, applied per tick or once) is not decoded._

### [Wardogs_GameplayCues_v2.md](Wardogs_GameplayCues_v2.html)

- **4. Still Not Pulled / Limitations**  →  _**The shared VFX Blueprint (`PDA_SmokeGrenade`) is not in this dump.** Its logic, the particle systems and the emitter settings are unknown._

### [Wardogs_GameplayTags_v1.md](Wardogs_GameplayTags_v1.html)

- **4. Still not pulled / limitations**  →  _**Matching rules:** how a requirement tag matches its child tags, and how tags are applied at runtime, are engine logic and are not in these files._

### [Wardogs_Maps_v2.md](Wardogs_Maps_v2.html)

- **9. Still Not Pulled / Limitations**  →  _**Blueprint logic.** [`B_MovingTarget`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/Gyms/Range/Assets/B_MovingTarget.json) exports its function names, variables, and components, but not the graph nodes. The time-to-target formula and the damage response are not_

### [Wardogs_Meta_v2.md](Wardogs_Meta_v2.html)

- **11. How Values Combine**  →  _**Unlock:** a node's cash cost is paid once. The node unlocks when the role level meets the node's `MinLevel`. The export gives one prerequisite per node, so no AND or OR logic between prerequisites is visible here._
- **11. How Values Combine**  →  _**Reward scaling:** the scaling curves are evaluated against their input (player count, match score, cash or XP earned) and multiply the base reward. The base values and the full formula are in the rewards doc._

### [Wardogs_MoverTesting_v2.md](Wardogs_MoverTesting_v2.html)

- **8. Still Not Pulled / Limitations**  →  _**Blueprint and referenced-only assets.** `B_CharacterModifier_IgnoreLookInput_C` and `B_CameraModifier_HeavyBreathing_C` are blueprints, so their logic is not in the export. Montage choosers (`CHT_*`), animations (`A_TP_*`), gameplay effects (`GE_*`), and the `BHFloatModifier_Operation` sub-objects_
- **8. Still Not Pulled / Limitations**  →  _**Query expansion.** The `AutoDescription` strings are the readable form of each state query. The encoded `QueryTokenStream` was not decoded, so the descriptions are the source of truth for the logic in this doc._

### [Wardogs_Plugin_BHAimAssist_v2.md](Wardogs_Plugin_BHAimAssist_v2.html)

- **6. How Values Combine**  →  _The **ADS vs Default** split means the assist strength is selected by the curve set the game code uses. The selection rule is not in this export._
- **7. Still not pulled / limitations**  →  _**Code path.** Which code reads each curve, and how the reticle and target inputs are normalised, is not in this folder._

### [Wardogs_Plugin_BHFramework_v2.md](Wardogs_Plugin_BHFramework_v2.html)

- **8. Still not pulled / limitations**  →  _**Setting consumers.** Which code reads each setting is not in this folder._

### [Wardogs_RewardLookup_SessionEvents_v1.md](Wardogs_RewardLookup_SessionEvents_v1.html)

- **19. Still not pulled / limitations**  →  _**Formula variables:** literal values (`KillStreakValue`, `ControlZoneFactor`, `HotZoneFactor` and most others) are defined inside each row. Runtime game values (`LastVictimCount`, `KillStreak`, `CrewCount`, the event's base reward from the cash tables) and the `LiveCurves` scaling curves are not; t_

### [Wardogs_Significance_v2.md](Wardogs_Significance_v2.html)

- **6. How Values Combine**  →  _**Timing** comes from the settings row for the chosen level: `TickRate` (how often it ticks), `SignificanceUpdateRate` (how often significance is re-evaluated) and `LocationUpdateRate` (how often its location is refreshed). The combination is not stated in the export._
- **7. Still Not Pulled / Limitations**  →  _**The level-selection rule** (distance threshold or FOV check first, and whether it is hysteresis-based) is not in the export._

### [Wardogs_Tests_v2.md](Wardogs_Tests_v2.html)

- **4. Still Not Pulled / Limitations**  →  _**Orchestrator and test-function blueprints are not in this dump.** The `B_Default`, `B_SoloTest` and `B_AutoTestFunc_*` logic (how clients are spawned and scattered) is not available._

### [Wardogs_VFX_v2.md](Wardogs_VFX_v2.html)

- **10. How Values Combine**  →  _**Muzzle flash, per shot:** weapon flash recipe (section 4c) provides the base size, lifetime, and gas. Its default muzzle attachment (section 4b) applies the device multipliers (`Flash Size Multiplyer 1P`, `Gas Side Scale`, and so on). The ammo override (section 4a) can then replace color and spark_

### [Wardogs_Vehicles_v2.md](Wardogs_Vehicles_v2.html)

- **11. How Values Combine**  →  _**Airplane lift:** the export lists each surface's area (`SurfaceArea_m`), incidence and the lift coefficient curve, plus `MainLiftMultiplier` 0.4. How these combine in the solver is not in the export. Control inputs move surfaces by the deflection values in section 4b, up to the per-airfoil max (fo_
