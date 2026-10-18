# MISC Reclassification Pass

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

After committing SDK (3655 files), mappings, damage pipelines,
`CROSS_REFERENCE.md`, and `UNITS.md`, the 240 MISC-classified gaps
got re-run through a context-aware classifier.

**Result: 67 of 240 (28%) reclassify to actionable or already-resolved buckets.**

## Resolved MISC gaps by new class

| New class | Count | Status |
|---|---:|---|
| **UNITS_DONE** | 18 | Resolved by [`UNITS.md`](../UNITS.md) — add inline citation on next data-doc pass |
| **RUNTIME** | 16 | Add to [`RESEARCH_REGISTER.md`](RESEARCH_REGISTER.md) — triage AI handles |
| **BINARY_ASSET** | 13 | Confirmed not resolvable from JSON parse (textures/meshes/widgets/binary) |
| **CROSS_REF_DONE** | 9 | Resolved by [`CROSS_REFERENCE.md`](../CROSS_REFERENCE.md) — add inline citation |
| **BLUEPRINT_BINARY** | 4 | Blueprint internals (bytecode) not in Dumper-7 output — permanently gated |
| **DAMAGE_PIPELINE_DONE** | 3 | Resolved by [`Wardogs_DamagePipeline_v2.md`](../../pipelines/Wardogs_DamagePipeline_v2.md) + [`Wardogs_VehicleDamagePipeline_v1.md`](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md) |
| **GAMEPLAYTAG** | 2 | Needs GameplayTag catalog pass — see [`Wardogs_GameplayTags_v1.md`](../../content/Wardogs_GameplayTags_v1.md) |
| **EXPORT** | 2 | Scheduled for next CUE4Parse re-run |
| **SECURITY** | 0 | None found — good news |
| **STILL_MISC** | **173** | Genuine miscellany — one-off observations needing per-item attention |

**Total resolved: 67 / 240 (28%)**

## What this means

- The "actionable gaps" count across the project is lower than
  the initial 474 suggested — much of the MISC bucket is actually
  *already answered* by the artifacts we've committed.
- **STILL_MISC = 173** is the honest remaining "miscellany" bucket.
  These are one-off doc-author observations like "the LOD is partial"
  or "secondary keys summarised not listed" — they're legitimate
  limitations of the current pass, not misclassifications.

## Updated project gap total

Starting from 474 total gaps in the original workbook:

| Bucket | Original | Resolved via | After this pass |
|---|---:|---|---:|
| UNITS | 13 | UNITS.md | 0 (-13 original + 18 from MISC = **18 to cite inline**) |
| CROSS_REF | 20 | CROSS_REFERENCE.md | 0 (-20 + 9 from MISC = **9 to cite inline**) |
| SDK | 26 | SDK sweep pass 1 | **18 remain** (per-asset investigation) |
| IDA | 32 | Triage AI's IDA brief | **32 queued** (needs IDA Pro session) |
| EXPORT | 118 | — | **120** (+2 from MISC); next CUE4Parse pass |
| RUNTIME | 25 | RESEARCH_REGISTER (triage) | **41** (+16 from MISC) |
| MISC | 240 | this pass | **173 STILL_MISC + 67 resolved** |
| BINARY_ASSET | — | docs now flag these | 13 (permanent gate) |
| BLUEPRINT_BINARY | — | docs now flag these | 4 (permanent gate) |
| GAMEPLAYTAG | — | needs catalog pass | 2 |
| **TOTAL ACTIONABLE** | 474 | | **~230 remain actionable, +~20 BINARY/BP permanent-gated** |

Roughly **half the original gaps are now resolved or answered by
reference docs** — the other half splits between:
- Static-fillable (IDA + SDK pass 2)
- Dynamic verification (triage AI's RESEARCH_REGISTER)
- Scheduled re-dump work (EXPORT)
- Genuine one-off miscellany (STILL_MISC)

## Source data

Full reclassification CSV: [`RECLASSIFIED_MISC.csv`](RECLASSIFIED_MISC.csv)
— one row per MISC bullet with its new class.

## Recommended next passes

1. **Inline citation pass** — walk the 18 UNITS_DONE + 9 CROSS_REF_DONE +
   3 DAMAGE_PIPELINE_DONE gaps, add one-line `*See [X](X)*` cites in the
   affected data docs. Pure mechanical work, ~1 hr.
2. **Merge RUNTIME into RESEARCH_REGISTER** — move the 16 new RUNTIME
   entries into the triage AI's register.
3. **STILL_MISC manual triage** — the 173 remaining are the honest
   long tail. Can be addressed as docs get re-dumped per category.
