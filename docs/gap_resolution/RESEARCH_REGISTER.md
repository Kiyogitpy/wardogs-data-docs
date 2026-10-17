# Research Register — RUNTIME gaps

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Live tracking of the 25 RUNTIME-classified gaps from
[`RUNTIME.md`](RUNTIME.md). Each gap gets one row: evidence source,
proposed resolution path, status.

**Updated by:** collaborator triage pass (documentation only, no instrumentation)
**Target output:** one row per entry below moved from OPEN → RESOLVED or DEFERRED

## Status key

| Status | Meaning |
|---|---|
| `OPEN` | Not yet triaged |
| `TRIAGED` | Evidence source identified, resolution plan noted |
| `STATIC_IN_PROGRESS` | Being resolved via SDK+IDA, no game session needed |
| `STATIC_RESOLVED` | Resolved via static means — gap closed, doc patched |
| `DEFERRED_DYNAMIC` | Needs runtime verification; deferred to next physical-access session (dynamic tooling held local-only) |
| `DEFERRED` | Not actionable now (e.g., Season 03 data refresh needed) |
| `SECURITY_ROUTED` | Finding has security implications; routed to [`../../SECURITY.md`](../../SECURITY.md) disclosure flow |

## Register

| # | Doc | Section | Bullet (truncated) | Evidence source | Next step | Status |
|---|---|---|---|---|---|---|
| 1 | `Wardogs_Audio_v2.md` | Still not pulled / limitations | **Curve units.** Time and value units for the 42 curves are not stored. Distances in UE units are assumed to be centimet | TBD | TBD | OPEN |
| 2 | `Wardogs_Audio_v2.md` | Still not pulled / limitations | **Event tag to asset mismatch.** Around 40 events have a tag that does not match the asset name. Runtime lookup by tag i | TBD | TBD | OPEN |
| 3 | `Wardogs_Characters_v2.md` | 5. Still Not Pulled / Limitations | **Kawaii runtime settings.** The constraint stiffness and damping are not in these assets. Only the bone pairs and compl | TBD | TBD | OPEN |
| 4 | `Wardogs_Environment_v2.md` | 16. Still not pulled / limitations | **North America fluid states** ([`DA_Flux_NorthAmerica_000`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/da | TBD | TBD | OPEN |
| 5 | `Wardogs_GameFeatures_AccountWatermark_v2.md` | 4. Still not pulled / limitations | **Runtime text.** The formatted text comes from the string table at runtime. | TBD | TBD | OPEN |
| 6 | `Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md` | 5. How Values Combine | [`CriticalFadeCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Alterna | TBD | TBD | OPEN |
| 7 | `Wardogs_GameFeatures_AlternativeCriticalCamera_v2.md` | 6. Still not pulled / limitations | **Offset units.** The offsets are in the export's native units (Unreal cm is assumed, not confirmed). | TBD | TBD | OPEN |
| 8 | `Wardogs_GameFeatures_Challenges_KOTH_v2.md` | 6. Limitations | The meaning of `Challenges.Context.*` tags is inferred from their names. Their runtime values were not checked. | TBD | TBD | OPEN |
| 9 | `Wardogs_GameFeatures_ControlZoneRegions_v2.md` | 8. Limitations | **Weight meaning is not confirmed.** The files say what the weights are (default and per-alternator) but not how the gam | TBD | TBD | OPEN |
| 10 | `Wardogs_GameFeatures_Experiences_v2.md` | 4. How Values Combine | Each experience is a self-contained mode. KOTH uses the control-zone runtime. SniperShowdown uses its own runtime and al | TBD | TBD | OPEN |
| 11 | `Wardogs_GameFeatures_FactoryInvestment_01_v2.md` | 7. Still not pulled / limitations | **Recipe duration.** 10.0 is the value in the export; its unit (seconds assumed) is not stated. | TBD | TBD | OPEN |
| 12 | `Wardogs_GameFeatures_FactoryInvestment_v2.md` | 4. Still not pulled / limitations | **What the rows mean in game.** `QueueSize` is most likely the production queue length and `SlotAmount` the number of sl | TBD | TBD | OPEN |
| 13 | `Wardogs_GameFeatures_Parachutes_v2.md` | 8. Still Not Pulled / Limitations | **Absent movement fields.** Several Basic fields (max speeds, roll speed) and Sport fields (max pull-up stamina) are not | TBD | TBD | OPEN |
| 14 | `Wardogs_GameFeatures_PerformanceCaptures_v2.md` | 5. Still not pulled / limitations | **Units.** Unit scale is assumed. | TBD | TBD | OPEN |
| 15 | `Wardogs_GameFeatures_Rewards_v2.md` | 7. Limitations | **Runtime inputs are unknown.** `BuildProgress`, `BuildCost`, `BuildAmount`, `CashSpent`, `BuildSuppliesDeposited`, `Las | TBD | TBD | OPEN |
| 16 | `Wardogs_GameFeatures_Rewards_v2.md` | 7. Limitations | **The assist path is inferred.** No `BuildableDestroyed.Assist` calculator row exists (section 3c). The assist credit is | TBD | TBD | OPEN |
| 17 | `Wardogs_GameFeatures_ShootingRangeTutorial_v2.md` | 6. Still not pulled / limitations | **Units.** Seat offsets are in native units (cm assumed). | TBD | TBD | OPEN |
| 18 | `Wardogs_GameFeatures_UnderbarrelGrenadeLauncher_v2.md` | 8. How Values Combine | **Damage:** no damage value is in this plugin. Damage is presumably on the 40mm projectile, which is outside this dump. | Export: `Caliber/40mm/DA_40mm_ProjectileData.json` | Doc corrected (2026-10-17) | STATIC_RESOLVED |
| 19 | `Wardogs_Plugin_BHFramework_v2.md` | 7. How Values Combine | Each setting's effective value is the player's saved choice, or the default if none is saved. Discrete settings with a d | TBD | TBD | OPEN |
| 20 | `Wardogs_Plugin_BHFramework_v2.md` | 8. Still not pulled / limitations | **Dynamic defaults.** How the dynamic default is picked for display, resolution, device and upscaling is in the runtime  | TBD | TBD | OPEN |
| 21 | `Wardogs_UI_v2.md` | 16. Still not pulled / limitations | **Field meanings not confirmed:** `ZOrder` direction (higher drawn on top is inferred from values), `RemovalTime` and `D | TBD | TBD | OPEN |
| 22 | `Wardogs_Vehicles_v2.md` | 13. Still Not Pulled / Limitations | **Default-valued fields are omitted** from exports. Where a property is missing (for example `Basic`-class fields), the  | TBD | TBD | OPEN |
| 23 | `Wardogs_Weapons_v2.md` | 5. How Values Combine | **Aim sway (likely):** the class speed curve, the horizontal and vertical movement curves, and the `AimSwayData` multipl | TBD | TBD | OPEN |
| 24 | `Wardogs_Weapons_v2.md` | 5. How Values Combine | **Recoil (likely):** `RecoilPattern` gives per-shot X/Y offsets, `RandomDeviationDegree` adds random deviation, and the  | Native: fire routine `0x6B93610` → kick `0x6B95C50` → behavior component `0x6B85D30` → playback `0x6B89BB0`; [Weapons §5a](../../Wardogs_Weapons_v2.md#5a-recoil) | Doc corrected (2026-10-17) | STATIC_RESOLVED |
| 25 | `Wardogs_Weapons_v2.md` | 5. How Values Combine | **Distance falloff (SKS):** `DistanceDamageFalloffCurve` is a multiplier indexed by distance. The falloff times are pres | Native: projectile path `0x6B725B0` evaluates the curve with distance in cm; [DamagePipeline §7.6](../../Wardogs_DamagePipeline_v2.md#76-the-bullet-event) | Doc corrected (2026-10-17) | STATIC_RESOLVED |


## Notes for the triage pass

**Scope guard:** documentation only. No loader runs, no dynamic agent
load, no game-process attachment. See [`../SCOPE.md`](../SCOPE.md)
for scope posture.

**Preferred resolution order per gap:**

1. **Scan SDK for the referenced class/property.** Many "likely" and
   "presumably" statements become certain once the SDK confirms the type,
   access specifier, and `Net` replication flag.

2. **Scan data assets for configured values.** "Runtime behavior assumed"
   often resolves to "there's a DataTable row that defines it, I just hadn't
   found the file."

3. **Static IDA (if the game binary is available).** For questions about
   function logic, IDA + `.idmap` resolves most "actual behavior" questions
   without running anything.

4. **Mark as `DEFERRED_DYNAMIC`** only if 1–3 all fail and the question
   genuinely requires observing a running game. These accumulate for the
   next physical-access session's hypothesis-verification run.

5. **Mark as `SECURITY_ROUTED`** if a gap's resolution would expose a trust
   model issue (e.g., "the client sends X" vs "the server computes X"). Do
   not resolve publicly; route through [`../../SECURITY.md`](../../SECURITY.md).

**Avoid duplicating work the primary RE pipeline is doing.** As of this
writing the primary pipeline has already produced:
- [`../../Wardogs_DamagePipeline_v2.md`](../../Wardogs_DamagePipeline_v2.md)
  — damage pipeline, which pre-answers any RUNTIME gap tagged to damage
  modifiers.
- SDK + mappings committed at commit `c65e83d`.
- gap_resolution workbooks for UNITS / CROSS_REF / SDK / IDA.

Check each register row against those existing artifacts before
investigating further.

## When a gap is resolved

1. Update the Status column to `STATIC_RESOLVED`
2. Add a reference link to where the resolution landed (data doc patch,
   new reference doc, or SDK file)
3. If the resolution added or modified a data doc, note the commit hash
4. Keep the Evidence source + Next step cells filled even on RESOLVED
   entries so the audit trail is complete

## When all 25 are triaged

Open a PR against the main branch with the completed register. The
primary pipeline will then:
- Patch each affected data doc with the resolutions
- Move the resolved gaps out of the active workbook
- Re-run the classifier on the remaining MISC bucket (240 entries) with
  the new context — many MISC gaps will reclassify now that the SDK + damage
  pipeline doc exist.
