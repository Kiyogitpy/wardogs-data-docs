---
title: Every-vehicle explosive audit
nav_exclude: true
---

# Every-vehicle explosive audit, 2026-10-19

Build CL-516586. Every exported `ModularVehicleVariant` was inspected:
**33 source variants, 32 represented by 23 viewer profiles, one unsupported
fixed-wing definition**. This verifies source/export consistency and the
inherited native entrypoints; it does not establish gameplay collision parity.
The [machine-readable report](round8-vehicle-explosive-coverage.json) preserves
per-variant source paths, health sections, routing, omissions and findings.
The [native class audit](round8-vehicle-native-classes.md) covers all 21
exported platforms and their implementation families.

The pass found and corrected two export errors. STN_05 was missed because
its source directory is named `Varient`; it now appears as a table-only
profile. Nested [`Variants/Air`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Vehicles/Variants/Air) is also discovered, but FWG_01_Default has
no health sections or surface-slot mapping and remains explicitly unsupported.
Its inherited LittleBird damage tag is not a substitute for those definitions.
The 30 mm cannon's positive explosive radius was also hidden by a UI-category
filter. It now exposes its authored 300 cm blast/100 cm effective radius,
minimum 20 and falloff 1. Nonexplosive projectiles retain inspection controls.
The partial 20x102/35x228 blast structs omit an active outer radius; no active
blast is inferred from their effective-radius/falloff fields alone.

## Per-variant coverage

“Model present” means published display geometry exists. The omission count
covers registered source components missing from that geometry, not all native
physics bodies. Zero omissions does not establish collision completeness.
Skeletal bodies, transforms, query responses and overlap order remain separate
inputs for every model.

| Source variant | Data audit | Display geometry / omitted registered components |
|---|---|---|
| `FWG_01_Default` | Unsupported: no health/slot definition | No supported preview |
| `Attack_ROT_02` | Pass | Model present; 2 omitted |
| `ROT_03_Default` | Pass | Model present; 2 omitted |
| `ROT_03_MachineGuns` | Pass | Model present; 3 omitted |
| `ROT_03_RocketPods` | Pass | Model present; 3 omitted |
| `ROT_04_Default` | Pass | Model present; 1 omitted |
| `ROT_04_MountedMachineGuns` | Pass | Model present; 2 omitted |
| [`SPW_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/SPW_01/Content/SPW_01.json) | Pass | Model present; 0 omitted |
| `SPW_02` | Pass | Model present; 0 omitted |
| `SPW_03` | Pass | Model present; 0 omitted |
| [`STN_01`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_01/Content/STN_01.json) | Pass | Model present; 0 omitted |
| [`STN_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_02/Content/STN_02.json) | Pass | Model present; 0 omitted |
| [`STN_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_03/Content/STN_03.json) | Pass | Model present; 1 omitted |
| [`STN_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_04/Content/STN_04.json) | Pass | Model present; 0 omitted |
| [`STN_05`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_05/Content/STN_05.json) | Pass | No model; table only; 1 omitted |
| [`STN_06`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/STN_06/Content/STN_06.json) | Pass | Model present; 3 omitted |
| `TNK_01_AntiAir` | Pass | Model present; 0 omitted |
| `TNK_01_Artillery` | Pass | Model present; 1 omitted |
| `TNK_01_Heavy` | Pass | Model present; 1 omitted |
| [`TNK_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/TNK_04/Content/TNK_04.json) | Pass | Model present; 0 omitted |
| `WHL_01_Default` | Pass | Model present; 0 omitted |
| `WHL_02_Default` | Pass | Model present; 0 omitted |
| `WHL_02_Pickup` | Pass | Model present; 0 omitted |
| `WHL_02_SUV_RingTurret` | Pass | Model present; 2 omitted |
| `WHL_05_Humvee_Default` | Pass | Model present; 0 omitted |
| `WHL_05_Humvee_RingMinigun` | Pass | Model present; 0 omitted |
| `WHL_05_Humvee_RingTurret` | Pass | Model present; 0 omitted |
| `WHL_06_DuneBuggy_Default` | Pass | Model present; 0 omitted |
| `WHL_07_Battle` | Pass | Model present; 1 omitted |
| `WHL_07_Default` | Pass | Model present; 0 omitted |
| [`WHL_07_ArmouredBattle`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_07_ArmouredBattle/Content/WHL_07_ArmouredBattle.json) | Pass | Model present; 5 omitted |
| `WHL_08_Default` | Pass | Model present; 0 omitted |
| [`WHL_08_RingTurret`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Vehicles/WHL_08_RingTurret/Content/WHL_08_RingTurret.json) | Pass | Model present; 0 omitted |

## Verified and remaining boundaries

Source comparisons pass with **zero mismatches**: 174 per-variant section
instances, 207 routes, 234 slots, 7,488 direct factors, 3,744 radial factor
pairs and 1,404 actor factor pairs. These reuse the repository's source
interpreters; they are consistency checks, not an independent engine oracle.
Across the 23 profiles there are 113 section instances and 46 pre, 66 post,
22 simultaneous routes. All post routes are depleted-only; no route uses a
nondefault curve, registry or absolute-health setting. Twelve track section
instances skip simultaneous routing on radial events.

Native hit-location deduplication applies across these vehicle families.
The Heavy's Main and Body.StrongArea share MainBody, so section-name dedup
would still be wrong. The [Gepard correction](round8-explosive-viewer-audit.md#correction-hit-location-deduplication-and-routed-fuel-damage)
records the numerical regression and distinguishes routed FuelTank loss
from a FuelTank collision contact.

The 36 published GLBs pass structure/material/component-map checks. There
are **28 omitted registered components across 14 variants**, plus skeletal
components not represented by the display meshes. The report lists them;
none is silently treated as an exact explosion model. Raw BodySetup/Chaos
acquisition covers Gepard and SPW packages; Gepard's payloads are now
[decoded and checked against raw collision meshes](round8-gepard-chaos-decode.md).
SPW bounds, Gepard socket candidates and view-directed projectile backoff
are integrated in their linked continuations. The [Round 9 register](../ROUND9_STATUS.md)
tracks wider authored sampling coverage. Cooked scene-query behavior,
runtime pose and actual overlap/hit ordering still prevent a numerical
parity claim.

The historical pre-authored-sampling verification passed **6,864 placements across all 36 models
and 22 explosive sources**: 6,552 for the original 15 projectile/six actor
catalog, plus 312 for the newly exposed 30 mm source. Each model is checked
from surface directions, on nearby ground and outside the blast radius.
Checks cover unique application tags, resolved factors, fresh bounded
health and reconciliation of the routing ledger with section loss. The
23 current profiles also pass **339 fresh section applications** (small,
half-health and over-health input). STN_05 has no geometry to shoot, so
only its data, section routing and browser fallback are verified.

Restartable shot reports are outside the repo under
`E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/`:
`all-vehicle-preview-check.json` and `all-vehicle-30mm-check.json`.
The first run loaded the prior 22-profile catalog before STN_05 was added;
those existing vehicle definitions and original-source factors are unchanged.
The separate section/browser/source audits cover the current 23 profiles.

The installed Edge harness passes all 23 profile legends, unique computed
section colors and all 154 slot routing explanations. STN_05 shows its
fallback and disables impact placement. The front-Gepard 84 mm click shows
one application, four repeated contacts skipped and 14.1 routed FuelTank
loss. The underlying main loss is 267.9; the UI rounds it to 268. The 30 mm
impact smoke and nonexplosive-control checks also pass. The browser harness
uses deployed theme CSS with local assets, not a full local Jekyll build.

## Reproduction

- `python -I _tools/vehicle_data_audit.py --report <new-report.json> --expect-variants 33`
- `node _tools/vehicle_impact_check.js --report <new-report.json>`
- `node _tools/vehicle_impact_check.js --routing-only`
- `python -I _tools/vehicle_impact_browser_check.py --out <evidence-directory>`

The optional audit `--collision-metadata <collision.json>` links a local raw
BodySetup extraction without claiming that other models have that coverage.
Report writers refuse existing output files. No game process or service was
accessed. Initial viewer corrections were pushed as `bdf5d8a2`; subsequent
sampling and publication checkpoints are recorded in Git history and the
[active register](../ROUND9_STATUS.md).
