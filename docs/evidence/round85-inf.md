# Round 85 (teammate inf): movement, medical and weapon-extension fields

GitHub-only page. Items V4-02, V4-04, V4-05, V4-08, V4-09, V4-10, V4-19 of the census backlog v4. Static analysis only: the JSON exports under `data/` and the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__` (unreviewed decompiler output; all addresses are RVAs). Nothing entered the Elytra protection layer.

Reproduce: `python -I _tools/weapon_ranged_fields.py --check`, `python -I _tools/aim_assist_tables.py --check`, `python -I _tools/movement_tables.py --check`, `python -I _tools/check_links.py`.

## Status

| Item | Status | Result |
|---|---|---|
| V4-02 speed combination | FOUND (one residual) | Order and product-vs-sum read from `0x52867F0`, `0x5291720`, `0x6DC1000`, `0x6DC1050`, `0x6DC10F0`; PlayerMovement section 1d. Residual: the writer of the mode float `+168` (constructor sets 1.0 at `0x5283BB0`; no other writer in the ground-mode ranges), and which effects are active at once (needs a running game) |
| V4-04 MedKit fields | ABSENT (already documented) | `HealSelfAmount` 35, `HealSelfDuration` 5, `HealSelfDurabilityCost` 25 and `UsageRateMultiplierAttribute` are in `game-features/Wardogs_Medical_v1.md` (heal table and usage-rate rows) and `_wiki/equipment/medical-items.md` under plain-English names. No change |
| V4-05 `MaxPelletCount`, `MaxConsecutiveFullRefundedSubsteps` | FOUND | Pellet normaliser `0x6C25660`; sub-step loop `0x6F3CB80`. HitRegistration table rows and O-11 updated |
| V4-08 ranged-weapon fields | FOUND | New generator and page `content/Wardogs_RangedWeaponFields_v1.md`: 38 ranged items and 24 crosshair overrides, row by row. Readers of the fields (rechamber, sight offsets, blend targets) not traced |
| V4-09 aim assist | FOUND (partial native) | New generator and page `content/Wardogs_AimAssistCurves_v1.md`: 16 curves with keys, per-class curve map, target-score fields, formula from `0x6763510`, native defaults from `0x6760E9E`. Residual: five of the seven unnamed floats unmatched, the argument of `TargetWeightCurve`, body of `0x43AAA8D0` |
| V4-10 mantle, climb, fall, ground | FOUND, mostly pre-existing | All named fields were already tabled under their curve names in `Wardogs_MoverTesting_v2.md` section 4 (the census counted field names). Added: stance transition times, base-velocity flags, `bUseForwardOnlyLeftAndRight`. Jump height and mantle reach: ABSENT (no gravity value in the exported data; searched [`data/Wardogs/Config`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Config) and `Content/MoverTesting`) |
| V4-19 weapon curve gaps | FOUND | The seven `CurveFloat` objects are five bipod camera-offset curves and two ADS curves; the [`MAGZ_002`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Magazines/MAGZ_002/Content/MAGZ_002.json) hidden prices are per-ammunition-type prices (all 33 magazines tabled); `TransferTime` on [`Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Launcher_04.json) is 3.5 s. Reader of the fragment and of the bipod curves not traced |

## V4-02: ground speed

Evidence chain (vtable slots confirmed from the corpus `aliases` table):

- Velocity tick `0x52867F0` (BH ground mode): calls slot 142 (`+1136`, max speed) and slot 143 (`+1144`, min speed). Aux input state bytes: `+8` sprint, `+9` tactical sprint, `+10` slow walking (`bIsSlowWalking`), `+20` slow-walk setting. `v40 = clamp(|stick|, 0, 1)`. Sprint or tactical sprint: speed = max. Else if `v40 >= 1`: with the slow-walk flag, the map `SlowWalkSpeedSettings` (data `+216`, lookup `0x143BD5570` keyed by the byte at aux `+20`) gives speed = `(max - min) * scale + min`; without the flag, max. Else speed = `(max - min) * v40 + min`. The result multiplies the unit direction.
- Slot 142 BH `0x5291720`: stance speed (`MaxSpeedModifier` of the current stance, blended previous to current), then, only when the current stance byte is 2 (Stand) and the aux pointer is set: sprint flag times slot 144, tactical flag times slot 145, otherwise times the mode float `+168`; any other stance times `+168`.
- WD override slot 142 `0x6DC1000` = the `0x5291720` result times the attribute evaluator at WD mode `+272` (`0x52301F0`). Slot 144 `0x6DC1050` = base `0x5291A90` (`SprintMaxSpeedScale`, data `+0x130`) times evaluator `+304`. Slot 145 `0x6DC10F0` = base `0x5291FD0` times evaluator `+320`. Slot 146 `0x6DC10A0` = base `0x5291DC0` (`MaxStopSpeed`, data `+0x54`) times evaluator `+336`. Slot 143 (`0x52923C0`, reads data `+0x50` = `MinSpeed`) has no WD override (the corpus lists `UWDMoverMode_GroundMovement_VFT::slot_143` = `0x52923C0`), so the minimum speed is not scaled by effects.
- Evaluator tags: `+272` is `Attribute.Gameplay.Movement.MaxSpeedMultiplier` (registration function `0x128C490`, global `qword_14D36B3F8`, used in `0x6DC1230`). `+304` and `+320` follow the sprint and tactical sprint multipliers per round 40; their tag registrations are not in the corpus (the registrar functions are missing), so `+336` is named only by the data it multiplies (`MaxStopSpeed`).
- Mode float `+168`: initialised to `1065353216` (1.0) by the constructor `0x5283BB0`. Scans of `0x5280000-0x52C0000` and `0x6D00000-0x6E00000` for float stores to `+168` found only that store.
- Effect arithmetic: `GE_ADS` `Movement.MaxSpeedMultiplier` x compound 0.5, weight classes x compound 0.95 / 0.875 / 0.8 / 0.8, Ghillie 0.95, bow draw 0.9; the skill effects `GE_Player_MaxSpeedMultiplier_Aiming` and `_Covert` are plain Multiply with a SetByCaller value. Current value = the formula in GameplayEffectsPipeline 4.4, so compound factors multiply and plain multipliers add their offsets first.

## V4-05: consumers

- `MaxPelletCount`: `ProjectileSystemSettings` sits at `+0x458` of `UWDGameSettings`, so the field is at `+0x5E4` (1508). `0x6C25660` reads `*(int *)(0x6C03540() + 1508)` and computes `P = clamp(N / Max, 0, 1) * (a5 * a3[0])` (ammunition factor times choke factor), with a guard for `Max` of 0 (0 when `N < Max`, else 1). The loop runs `N` times; a random number above `P` gives an outer-cone pellet, otherwise an inner-cone pellet. `N` is not capped.
- `MaxConsecutiveFullRefundedSubsteps`: `UWDProjectileSubsystem` copies the settings (`0x6F37C00` calls `0x6F2C180(subsystem+672, settings+1112)`), so the field is at subsystem `+1088`. `0x6F3CB80` runs sub-step `0x6F3C060` in a loop on the remaining time `v16`; when the change of `v16` is at most 1e-8 the counter `v17` is incremented, otherwise reset; `++v17 > *(a1+1088)` sets `v16 = 0`. `SimulationFrameRate` is read at `+1092` (`0x6F2C450`, `0x6F342B0`, `0x6F3D740`), not followed further.

## V4-09: aim assist

- Score in `0x6763510` (target collection, 160-byte records; settings pointer `a3`): `score = w_prev * a3[+1064] + (viewDot * a3[+1068] - a3[+1072]) + (1 - dist / range) * a3[+1076] + (rendered ? a3[+1080] : 0)`. Settings offsets 1064-1080 are `TargetScore_AssistWeight/ViewDot/ViewDotOffset/ViewDistance/RenderedRecently` (SDK `0x428-0x438`). `range` is `TargetRange` (settings `+288`) divided by the FOV factor from `0x146762FE0` (only when `bFOVReticleScaling`). Candidates with view dot not above 0 are skipped. The list is trimmed when the count exceeds `a3[+1056]` (`MaxNumberOfTargets`).
- Defaults (constructor `0x6760E9E`): `MaxNumberOfTargets` 6, `+1060` (`ReticleDepth`) 3000, AssistWeight 10, ViewDot 50, ViewDotOffset 40, ViewDistance 0.25, RenderedRecently 1000, `StrengthScale` 1, `MinAssistWeight` 0.25, floats at `0x3B8/0x3BC/0x3C0/0x3C4/0x3C8` = 0.25, 0.25, 0.6, 1.0, 0.25.
- Weight update `0x6766850`: per record `+108 = clamp(curve(...), 0, 1)` from `TargetWeightCurve` (`settings+328`), normalised by the sum, floored at `+1096` (`MinAssistWeight`); `+104` is a fade value moved by the frame time.
- `0x6765BF0` (pull): uses `+948` (0x3B4) in `min(v / x, 10)`, `+952/+956` (0x3B8/0x3BC) as thresholds, and `+1084` (`StrengthScale`).
- Not resolved: native `0x43AAA8D0` (rendered test; no decompiled body), the evaluation argument of `TargetWeightCurve`, and the use of `0x3B0`, `0x3C0`, `0x3C4`, `0x3C8` and `0x3B4` beyond the above.

## Search notes (ABSENT items)

- Gravity: a case-insensitive search for "gravity" over [`data/Wardogs/Config`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Config) and `Content/MoverTesting` found nothing.
- MedKit: [`ID_MedKit_Standard.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/MedKit/Content/Data/ID_MedKit_Standard.json) has `WDItemExtensionData_MedKit` with `UsageRateMultiplierAttribute`, `HealSelfAmount` 35, `HealSelfDuration` 5, `HealSelfDurabilityCost` 25; every value appears on the Medical page.
