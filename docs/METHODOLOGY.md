# Methodology

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How the data documentation and reverse engineering work gets done.

## Pipeline overview

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Shipped game   │   │  Game binary    │   │  Running game   │
│  .pak / .ucas   │   │  .exe          │   │  (local only)   │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
   CUE4Parse               UEDumper +             Pass D agent
   extraction              IDA Pro + .usmap       (BYOVD kernel R/W)
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  JSON exports   │   │  CppSDK +       │   │  Hypothesis     │
│  (data/*.json)  │   │  function RVAs  │   │  verification   │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └──────────┬──────────┴──────────┬──────────┘
                    │                     │
         ┌──────────▼──────────┐  ┌───────▼──────────┐
         │  Python parsers +   │  │  IDA Python +    │
         │  cross-ref builders │  │  manual RE       │
         └──────────┬──────────┘  └───────┬──────────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                     ┌─────────────────┐
                     │  Markdown docs  │
                     │  (this repo)    │
                     └─────────────────┘
```

## Toolchain

### Static data extraction

| Tool | Purpose | Output |
|---|---|---|
| **CUE4Parse** (.NET 10 SDK) | Read `.pak` / `.ucas` + decrypt + decode .uasset | `data/**/*.json` |
| **retoc** (Rust) | Zen-to-legacy pak conversion | Intermediate paks |
| **FModel** | Interactive asset browser (manual exploration) | ad-hoc |
| **UEDumper** | Live dump of UE class hierarchy from running game | `sdk/*.h/.cpp` |
| **IDA Pro** | Static disassembly of the shipping binary | `.i64` project + exports |
| **.usmap** | Serialized class/property metadata | Companion to CUE4Parse |

### Parsing and doc generation

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Primary parser language |
| **Jinja2** | Doc template rendering (where used) |
| **Jekyll** | GitHub Pages static site generation |

### Live hypothesis verification

| Tool | Purpose |
|---|---|
| **kdmapper** (patched build in `tools/kdmapper/`) | BYOVD manual-map loader via iqvw64e |
| **Pass D agent** (`tools/pass_d/`) | Kernel-mode cross-process R/W primitive |
| **cdb.exe** / **WinDbg** | Minidump post-mortem analysis |

### Research references

| Doc | Covers |
|---|---|
| `research/references/hyperdbg/` | HyperDbg documentation archive |
| `research/references/kdmapper/` | kdmapper + BYOVD background |
| `research/references/byovd/` | CVE-2015-2291 (iqvw64e) exploit primitive |
| `research/references/bootviewer/` | Measured-boot verifier |
| `research/wardogs_analysis/DEBUGGER_ATTACHMENT_REPORT.md` | Full prior-work archive on debugger-attach vectors |

## Working method per doc

Each per-category reference doc (e.g., `Wardogs_Weapons_v2.md`)
follows the same production flow:

1. **Pick a scope** — one `Content/` or `Plugins/GameFeatures/`
   folder, bounded set of asset classes
2. **Extract JSON** — CUE4Parse pass on the chosen folder
3. **Parse** — Python script that reads the JSON and extracts
   structural facts (what asset class, which properties, which
   references)
4. **Cross-reference** — build table of related assets (vendor
   rows that reference this asset, GEs that modify its properties,
   etc.)
5. **Static RE** — identify which functions in the game binary
   read these assets at runtime (via IDA + known FName hashes)
6. **Formula documentation** — for each "How Values Combine"
   question, trace the function body in IDA, document the formula
7. **Hypothesis verification** (Pass D, only when static RE is
   ambiguous) — read one specific VA during a controlled test,
   confirm the behavior matches the disasm
8. **"Still Not Pulled / Limitations" section** — document what
   you couldn't resolve, in what form, so future passes can target
   it precisely

## Season-diff process

The game patches regularly. Each patch:

1. Re-run CUE4Parse against the new build
2. Diff the resulting JSON against the previous build's JSON
3. Classify changes:
   - **Numeric** (value changed) → note in `Season XX update` section
   - **Structural** (new field, new asset class) → may need SDK
     refresh, possibly a new doc section
   - **Removed** (asset gone) → note removal
4. UEDumper + IDA refresh if structure changed
5. Update affected docs' top sections, keep the `v2` version
   number (bump to `v3` only for major structural rewrites)

## Documentation style

- **Raw values preferred** — the export says 73500, so the doc
  says 73500. Unit inference is called out explicitly ("probably
  cm/s").
- **"Unverified" and "inferred" are first-class words** — any
  value whose meaning isn't in the export itself gets labeled.
- **No speculation presented as fact** — "likely" and
  "presumably" are the honest words when the formula isn't
  verified.
- **Cross-links are heavy** — a doc that mentions `DT_X` links to
  `DT_X.json`; a doc that mentions a related doc links to it.
- **"Still Not Pulled / Limitations"** at the bottom of every doc
  — nothing is complete, and the gaps are the roadmap.

## Reproducibility

Everything in `data/*.json` should be reproducible by anyone with
their own copy of the game via:

```
# Clone a fresh checkout
git clone https://github.com/Kiyogitpy/wardogs-data-docs.git
cd wardogs-data-docs

# Set up CUE4Parse with the game's AES key
# (See README for key - obtained via retoc from local game install)
dotnet run --project tools/cue4parse_extractor -- \
  --paks "C:/Program Files (x86)/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks" \
  --out "./data" \
  --key "<your_locally_derived_aes_key>"
```

The parse scripts in `tools/` turn the JSON into the markdown docs.

## When static RE is enough vs. when you need Pass D

**Static is enough when:**

- The question is "what are the values in this asset" (CUE4Parse
  answers)
- The question is "what's the SDK structure of this class" (UEDumper
  answers)
- The question is "which function reads this asset" (IDA xref answers)
- The question is "what does the function do" (IDA disasm answers)

**Pass D is needed when:**

- The function body in IDA has branches you can't resolve statically
  (e.g., behavior depends on a GEnabled flag set at runtime)
- You want to confirm a static conclusion against a live value
- An asset's binary data (height grids, Houdini caches) needs decoding
  against the runtime decoder in-memory

Pass D is a verification tool, not a primary research tool. Most docs
are built without ever running the game.
