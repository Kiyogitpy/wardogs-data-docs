# Gap resolution — RUNTIME

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Gaps where the data doc's statement is **inferred from reading, not confirmed from execution**: 'likely', 'presumably', 'unverified', 'actual order', 'runtime behavior'. 25 total across the project.

## Resolution strategy

**Two-track approach:**

1. **Static resolution (preferred first)** — many RUNTIME gaps can be resolved by **close reading of the SDK + IDA disassembly** without actually running the game. The classifier flagged them as runtime because the doc author hedged, but the answer may be deterministic from static inspection.

2. **Dynamic verification (Pass D)** — only when static analysis is genuinely ambiguous. Pass D agent reads a specific VA during a controlled test (see [`../../pass_d/docs/next_session_runbook.md`](../../pass_d/docs/next_session_runbook.md) once ready). This is deferred to next physical-access session.

## Register format

Each entry below should be moved to [`RESEARCH_REGISTER.md`](RESEARCH_REGISTER.md) with:
- **Evidence source:** which SDK file / data asset / IDA function could resolve it statically
- **Next step:** either `STATIC — <specific action>` or `PASS_D — <specific IOCTL + VA>` or `DEFER — <reason>`
- **Status:** `OPEN` / `IN_PROGRESS` / `RESOLVED` / `DEFERRED`

## Catalogue

### [Wardogs_Audio_v2.md](Wardogs_Audio_v2.html)

- **Still not pulled / limitations** — _**Curve units.** Time and value units for the 42 curves are not stored. Distances in UE units are assumed to be centimetres but not verified._
- **Still not pulled / limitations** — _**Event tag to asset mismatch.** Around 40 events have a tag that does not match the asset name. Runtime lookup by tag is inferred, not verified._

### [Wardogs_Characters_v2.md](Wardogs_Characters_v2.html)

- **5. Still Not Pulled / Limitations** — _**Kawaii runtime settings.** The constraint stiffness and damping are not in these assets. Only the bone pairs and compliance type are recorded._

### [Wardogs_Environment_v2.md](Wardogs_Environment_v2.html)

- **16. Still not pulled / limitations** — _**North America fluid states** ([`DA_Flux_NorthAmerica_000`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Environment/Water/FluidFlux/NorthAmerica/DA_Flux_NorthAmerica_000.json) to `_013`, 14 assets) have no matching height grid in this dump and no `EncodeVelocityMax`. Their runtime role is unclear._

### [Wardogs_GameFeatures_AccountWatermark_v2.md](Wardogs_GameFeatures_AccountWatermark_v2.html)

- **4. Still not pulled / limitations** — _**Runtime text.** The formatted text comes from the string table at runtime._

### [Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md](Wardogs_GameFeatures_AlternativeCriticalCamera_v2.html)

- **5. How Values Combine** — _[`CriticalFadeCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AlternativeCriticalCamera/Content/CriticalFadeCurve.json) and the 30-second `FadeTime` on the darken modifier control how the screen darkens. Priority 126 on the darken modifier is the highest priority in this set. Higher priority is assumed to win; not verified._
- **6. Still not pulled / limitations** — _**Offset units.** The offsets are in the export's native units (Unreal cm is assumed, not confirmed)._

### [Wardogs_GameFeatures_Challenges_KOTH_v2.md](Wardogs_GameFeatures_Challenges_KOTH_v2.html)

- **6. Limitations** — _The meaning of `Challenges.Context.*` tags is inferred from their names. Their runtime values were not checked._

### [Wardogs_GameFeatures_ControlZoneRegions_v2.md](Wardogs_GameFeatures_ControlZoneRegions_v2.html)

- **8. Limitations** — _**Weight meaning is not confirmed.** The files say what the weights are (default and per-alternator) but not how the game uses them to pick zones. The statement that weight 5.0 is "more likely" is an inference from the usual meaning of a selection weight._

### [Wardogs_GameFeatures_Experiences_v2.md](Wardogs_GameFeatures_Experiences_v2.html)

- **4. How Values Combine** — _Each experience is a self-contained mode. KOTH uses the control-zone runtime. SniperShowdown uses its own runtime and also a control zone with a seeker component._

### [Wardogs_GameFeatures_FactoryInvestment_01_v2.md](Wardogs_GameFeatures_FactoryInvestment_01_v2.html)

- **7. Still not pulled / limitations** — _**Recipe duration.** 10.0 is the value in the export; its unit (seconds assumed) is not stated._

### [Wardogs_GameFeatures_FactoryInvestment_v2.md](Wardogs_GameFeatures_FactoryInvestment_v2.html)

- **4. Still not pulled / limitations** — _**What the rows mean in game.** `QueueSize` is most likely the production queue length and `SlotAmount` the number of slots, but the dump does not say so. Inferred from names and the Factory 01 use._

### [Wardogs_GameFeatures_Parachutes_v2.md](Wardogs_GameFeatures_Parachutes_v2.html)

- **8. Still Not Pulled / Limitations** — _**Absent movement fields.** Several Basic fields (max speeds, roll speed) and Sport fields (max pull-up stamina) are not exported. The runtime default is not known from the dump._

### [Wardogs_GameFeatures_PerformanceCaptures_v2.md](Wardogs_GameFeatures_PerformanceCaptures_v2.html)

- **5. Still not pulled / limitations** — _**Units.** Unit scale is assumed._

### [Wardogs_GameFeatures_Rewards_v2.md](Wardogs_GameFeatures_Rewards_v2.html)

- **7. Limitations** — _**Runtime inputs are unknown.** `BuildProgress`, `BuildCost`, `BuildAmount`, `CashSpent`, `BuildSuppliesDeposited`, `LastVictimCount` and `LastVictimCountMax` are read from the event at runtime. Their ranges are not stored here._
- **7. Limitations** — _**The assist path is inferred.** No `BuildableDestroyed.Assist` calculator row exists (section 3c). The assist credit is assumed to flow through `AssistCurve` and `AssistScalar`._

### [Wardogs_GameFeatures_ShootingRangeTutorial_v2.md](Wardogs_GameFeatures_ShootingRangeTutorial_v2.html)

- **6. Still not pulled / limitations** — _**Units.** Seat offsets are in native units (cm assumed)._

### [Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md](Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.html)

- **8. How Values Combine** — _**Damage:** no damage value is in this plugin. Damage is presumably on the 40mm projectile, which is outside this dump._

### [Wardogs_Plugin_BHFramework_v2.md](Wardogs_Plugin_BHFramework_v2.html)

- **7. How Values Combine** — _Each setting's effective value is the player's saved choice, or the default if none is saved. Discrete settings with a dynamic default pick their default from the hardware or platform at runtime._
- **8. Still not pulled / limitations** — _**Dynamic defaults.** How the dynamic default is picked for display, resolution, device and upscaling is in the runtime code._

### [Wardogs_UI_v2.md](Wardogs_UI_v2.html)

- **16. Still not pulled / limitations** — _**Field meanings not confirmed:** `ZOrder` direction (higher drawn on top is inferred from values), `RemovalTime` and `Duration` units (seconds assumed for the 10 values, but not stated), `EntryDuration` units, the `Stalk*` spatial fields, `Actions=[N]` on ping assets, `bIsWorkInProgress` (not shown on every asset), and the `RuleSets` evaluation order._

### [Wardogs_Vehicles_v2.md](Wardogs_Vehicles_v2.html)

- **13. Still Not Pulled / Limitations** — _**Default-valued fields are omitted** from exports. Where a property is missing (for example `Basic`-class fields), the runtime default is not known from the dump._

### [Wardogs_Weapons_v2.md](Wardogs_Weapons_v2.html)

- **5. How Values Combine** — _**Aim sway (likely):** the class speed curve, the horizontal and vertical movement curves, and the `AimSwayData` multipliers (crouch, prone, camera offset, no-focus speed) appear to feed one sway offset. The combination method is unknown._
- **5. How Values Combine** — _**Recoil (likely):** `RecoilPattern` gives per-shot X/Y offsets, `RandomDeviationDegree` adds random deviation, and the post-pattern yaw and pitch ranges add random kick afterwards. `RecoilPatternResetTime` probably controls when the pattern restarts._
- **5. How Values Combine** — _**Distance falloff (SKS):** `DistanceDamageFalloffCurve` is a multiplier indexed by distance. The falloff times are presumably in the same units as `InitialBulletSpeed`._
