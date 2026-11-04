---
title: Round 93 — recovered AI controller hearing configuration
nav_exclude: true
---

# G5 companion: the selected controller's hearing sense

This closes the missing cooked class-default assignment named at the end of the [vehicle-emitter continuation](round93-ai-rewards.md#g5-continuation--vehicle-producerconfigconsumer-route-recovered). It is static configuration evidence for CL-516586, not an observation that a live AI received an event.

## Recovered source and identity

A fresh offline package listing located `/WDAIPvEAICore/BP_CoreAIController` at [`Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BP_CoreAIController`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BP_CoreAIController.json). WdExtract decoded that exact package from the mounted game files with the existing corrected mappings; it reported `dump: ok=1 fail=0`. No game process, live memory or network replay was used.

The [published raw controller export](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/BP_CoreAIController.json) preserves the extractor's bytes: 40,586 bytes, 37 exports, SHA-256 `529fabbb38fe30e52a676cf3c149845497828fab800e82cd792e71ab072d3b37`.

The native emitter/consumer evidence remains bound to the restored executable SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`; see [corpus conventions](../DECOMPILATION_CORPUS.md). Export identity is separate from proof of a native caller or an observed server instance.

## Exact selection and object binding

- The tracked [DefaultAIPreset](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/DefaultAIPreset.json) selects `AIControllerClass = /WDAIPvEAICore/BP_CoreAIController.BP_CoreAIController_C`. This is not an arbitrary unreferenced controller package.
- In the recovered controller, `Default__BP_CoreAIController_C.PerceptionComponent` points to export `.30`, `WDAIPerceptionComponent` named `AIPerception`.
- That component's `HearingSense` is `Class'AISense_Hearing'` from `/Script/AIModule`. Its `SensesConfig` array contains export `.1`, `AISenseConfig_Hearing_3`.
- The hearing configuration's outer points back to component `.30`; its `HearingRange` is `100000.0` and `MaxAge` is `30.0`. The perception component sets `HearingRangeMultiplier = 0.05`.

These explicit references close the previously absent exported assignment of the sense identity used by the native Wardogs hearing branch. They do not infer class selection merely from a package name or native default.

## What this does not establish

The base configuration does not make engine/horn/destruction defaults unconditional detection radii. The traced component is installed server-only by the AI feature; valid feature activation, event attribution, perception/listener eligibility, affiliation and range gates still apply. A particular live vehicle or AI variant may have different settings. No timer activation, actual successful hearing, alert transition or live server override was observed.

The corrected wiki separates the native maximum-range defaults, actual event producers and accepted-stimulus detection-rate calculations. Generator metadata in `r42-modes.json` records the conditional compiled contract without changing its earlier numeric values.

## Verification

Parent checks compared the published raw bytes to the fresh extraction, checked the CDO -> perception -> hearing configuration links and preset controller reference, and reran the native vehicle-noise verifier (40 checks, exit 0). A regression test first rejected the missing controller export, then passed against the recovered one. Another guard first rejected the stale missing-emitter wiki statement, then passed after the event contract was integrated across the wiki and generator/data metadata. These regression tests protect the documented bindings; they do not substitute for the cited native event/consumer evidence.

The round-42 generator was rerun using its maintained private `round42_modes` and `round39_modes/cfgc` inputs. Restoring the effective config input location reproduced the old generated file exactly before the change; after the metadata addition, `--check` passed and comparison excluding only the two new metadata keys confirmed every prior key/value was unchanged.
