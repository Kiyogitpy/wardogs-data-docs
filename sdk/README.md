# CppSDK — UE Class Hierarchy

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Generated UE class hierarchy for Wardogs CL-516586, extracted via
Dumper-7. This bridges the per-category reference docs (which document
*data*) and the game binary (which contains *code* that consumes the
data).

## Status

The dump itself (3653 files across 1807 packages, 70 MB, under `raw/`) is
generated locally and **not committed**: it describes the game's own code.
This folder keeps the notes and the package index.

- `raw/` — raw Dumper-7 output (one `.hpp` / `.cpp` per package), local only
- [`INDEX.md`](INDEX.md) — package index by category

## What's here

Each package produces up to four files:

| File | Contents |
|---|---|
| `<Package>_classes.hpp` | Class declarations: inheritance chain, properties, method prototypes |
| `<Package>_parameters.hpp` | Parameter structs for `UFunction` invocation (used by IDA when reversing calls) |
| `<Package>_structs.hpp` | Package-local `USTRUCT` definitions |
| `<Package>_functions.cpp` | Function stubs annotated with offsets (metadata, not executable) |

## By category

| Category | Packages | Files |
|---|---:|---:|
| Other | 950 | 1931 |
| Vehicles | 252 | 416 |
| UI | 120 | 194 |
| Blueprint | 47 | 162 |
| AI | 66 | 153 |
| Weapons | 77 | 147 |
| UE Core | 53 | 138 |
| Characters | 103 | 115 |
| UE Engine | 37 | 97 |
| Audio | 34 | 94 |
| Rendering | 27 | 79 |
| Animation | 17 | 49 |

See [`INDEX.md`](INDEX.md) for the full package list.

## How this fills gaps in the data docs

The data docs' "Still Not Pulled / Limitations" sections list many
items like *"first flag column has no name"* — these are hashed
Blueprint property names that the SDK resolves to their actual
symbolic names.

Resolution workflow (per data doc):

1. Identify the SDK package that owns the DataAsset class the doc covers
2. Open `<Package>_classes.hpp` and find the property matching the
   hashed name in the data doc
3. Replace the hashed reference in the data doc with the SDK's
   symbolic name
4. Add a backlink from the SDK file to the data doc

The gap-resolution pass covering the SDK bucket is tracked in
[`../docs/gap_resolution/SDK.md`](../docs/gap_resolution/SDK.md).

## Generation methodology

The class dump stays local. Generation steps:

1. Launch the game locally (author's own hardware, author's own copy)
2. Load Dumper-7 into the process
3. Dumper-7 walks `GUObjectArray` and `GNames` to produce the C++ headers
4. Validate against known offsets from `.idmap` in `../mappings/`
5. Keep the generated headers under `sdk/raw/` (gitignored)

## Build target

| Attribute | Value |
|---|---|
| Game | Wardogs |
| Engine | Unreal Engine 5.7 |
| Build | `++Wardogs+Live-CL-516586` |
| Season | Season 02 (data as of 2026-10-15) |
| SDK generated | 2026-10-15 |
| Generator | Dumper-7 (`5.7.4-516586+++Wardogs+Live` in the `SDK.hpp` header) |

## Related

- Data reference docs (what the SDK structures contain at runtime):
  all `../Wardogs_*.md` files at the repo root
- IDA mappings (what the compiled binary looks like):
  [`../mappings/`](../mappings/)
- Extraction and update pipeline:
  [`../docs/UPDATE_PIPELINE.md`](../docs/UPDATE_PIPELINE.md)
