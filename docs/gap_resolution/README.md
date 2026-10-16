# Gap resolution

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Each top-level data doc has a "Still Not Pulled / Limitations"
section listing what the doc couldn't resolve. This directory
groups those gaps by **what tool fills them**, so the resolution
work can be prioritized and parallelized.

## Buckets

| Bucket | Count | Fill mechanism | Status |
|---|---:|---|---|
| [UNITS](UNITS.md) | 13 | Author a one-page units reference, cite from each doc | Ready to work |
| [CROSS_REF](CROSS_REF.md) | 20 | Add markdown links between docs where references exist | Ready to work |
| [SDK](SDK.md) | 26 | Resolve hashed/unnamed names via `../sdk/raw/` | Ready — SDK committed |
| [IDA](IDA.md) | 32 | Static disassembly using `../mappings/` | Ready — mappings committed |
| EXPORT | 118 | Re-run CUE4Parse with better config | Scheduled for next data refresh |
| [RUNTIME](RUNTIME.md) | 25 original entries | Review exports and consumers before bounded runtime verification | Triaged — see register for evidence and next steps |
| MISC | 240 | Needs reclassification | Lower priority |

**Original classifier total: 474 entries.** These counts preserve the source
classification; they are not a count of confirmed open questions or required
runtime tests. The RUNTIME register records reclassifications separately.

## Prioritization

1. **UNITS** first — cheapest wins, mostly single-line patches, writes one shared reference the whole project cites
2. **CROSS_REF** next — mechanical linking work, high value per minute
3. **SDK** — requires reading SDK files per gap, but SDK is already committed
4. **IDA** — slowest per gap but highest-information output; produces formula documentation
5. **EXPORT** — bulk re-run of the data extraction pipeline
6. **RUNTIME** — follow the [triage register](RUNTIME.md), resolving static and
   export questions before selecting an isolated observation session

## Source data

Full gap classifier output: `../../pass_d/docs/gap_index_v2.csv`
(local to the author's research workspace, outside this checkout). The
[RUNTIME register](RUNTIME.md) preserves all 25 runtime-classified entries
with source line numbers and a source-file hash so that this subset can be
reviewed without the external CSV.
