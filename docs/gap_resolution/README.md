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
| RUNTIME | 25 | Verify static conclusions via Pass D | Deferred — requires physical access |
| MISC | 240 | Needs reclassification | Lower priority |

**Total gaps catalogued: 474**

## Prioritization

1. **UNITS** first — cheapest wins, mostly single-line patches, writes one shared reference the whole project cites
2. **CROSS_REF** next — mechanical linking work, high value per minute
3. **SDK** — requires reading SDK files per gap, but SDK is already committed
4. **IDA** — slowest per gap but highest-information output; produces formula documentation
5. **EXPORT** — bulk re-run of the data extraction pipeline
6. **RUNTIME** — Pass D hypothesis-verification runs, requires physical-access session

## Source data

Full gap classifier output: `../../pass_d/docs/gap_index_v2.csv`
(local to the author's workspace; not in repo yet because it's
derived data and would duplicate the per-bucket pages here).
