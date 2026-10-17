# Methodology

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How the data documentation and reverse engineering work gets done.

## Pipeline overview

```
┌─────────────────┐   ┌─────────────────┐
│  Shipped game   │   │  Game binary    │
│  .pak / .ucas   │   │  .exe          │
└────────┬────────┘   └────────┬────────┘
         │                     │
   CUE4Parse               UEDumper +
   extraction              IDA Pro + .usmap
         │                     │
         ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│  JSON exports   │   │  CppSDK +       │
│  (data/*.json)  │   │  function RVAs  │
└────────┬────────┘   └────────┬────────┘
         │                     │
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │  Python parsers +   │
         │  cross-ref builders │
         └──────────┬──────────┘
                    │
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

### Post-mortem analysis

| Tool | Purpose |
|---|---|
| **cdb.exe** / **WinDbg** | Minidump post-mortem analysis of local crashes |

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
7. **"Still Not Pulled / Limitations" section** — document what
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

Everything in `data/*.json` comes from the game's own cooked paks,
exported with a CUE4Parse pipeline and the build's usmap
(`5.7.4-516586+++Wardogs+Live-Wardogs.usmap`). That extractor still lives
in the author's workspace and is not packaged in this repository yet
(see [`tools/README.md`](../tools/README.md)), so the export itself
cannot be rerun from a fresh clone today. Anyone with their own copy of
the game can reproduce it with CUE4Parse or FModel and the same usmap.

**Keys and mappings stay local.** The pak AES key and the `.usmap` /
`.idmap` mappings are never committed. Keep them in the checkout's root
or `mappings/` if convenient; `.gitignore` excludes `aes.*`, `*.aes`,
`*.usmap` and `*.idmap`. Derive the key from your own installed copy of
the game. Both the key and the mappings belong to one build, so check
them again after a game patch.

**From data to docs.** The scripts in [`_tools/`](../_tools/) rebuild
generated parts of the docs from `data/` and `assets/data/`:

| Script | What it does |
|---|---|
| `damage_tables.py` | Infantry and vehicle damage tables (per-weapon damage, falloff, ammo × armor, vehicle caliber factors, hits to destroy). `--write` refreshes every marked table in the damage and vehicle docs |
| `ge_values.py` | The Gameplay Effect Values page, from `assets/data/ge-values.json` |
| `vehicle_tables.py` | Sections 3 and 4 of the all-vehicle stats page |
| `zone_rewards.py` | `assets/data/zone-rewards.json`: reward values with no zone, a zone and a priority zone, for the site's zone switch |
| `link_sources.py` | Links asset names in the docs to their source JSON |
| `check_links.py` | Fails on broken cross-references (files, anchors, `§` numbers) |

After a data update: rerun the generators, then `check_links.py`.

## Static-only is almost always enough

**Questions resolvable from static analysis alone:**

- "What are the values in this asset" → CUE4Parse answers
- "What's the SDK structure of this class" → UEDumper answers
- "Which function reads this asset" → IDA xref answers
- "What does the function do" → IDA disassembly + decompile answer

For the small set of residual questions where static disassembly
leaves branches ambiguous (behavior depends on a runtime-set flag,
etc.), the doc author annotates `**Unverified:**` and moves on. The
public documentation does not require dynamic verification to be
useful.
