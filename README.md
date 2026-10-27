# Wardogs Data Docs

[![Repo](https://img.shields.io/badge/repo-Kiyogitpy%2Fwardogs--data--docs-blue?logo=github)](https://github.com/Kiyogitpy/wardogs-data-docs)
[![Site](https://img.shields.io/badge/pages-live-brightgreen)](https://kiyogitpy.github.io/wardogs-data-docs/)
[![License](https://img.shields.io/badge/license-CC--BY--SA--4.0%20%2F%20MIT-lightgrey)](LICENSE)

Reference documentation for the game data of **Wardogs** (Bulkhead, published by Team17,
UE 5.7, build `++Wardogs+Live-CL-516586`): the numbers, tables, curves
and rules behind weapons, vehicles, items, progression, game modes and
maps, read from the game's cooked data and tied to the engine classes
that use it.

- **Live site:** <https://kiyogitpy.github.io/wardogs-data-docs/>
- **Repository:** <https://github.com/Kiyogitpy/wardogs-data-docs>
- **How the data is read:** [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)
- **What the docs cover:** [`docs/INTENT.md`](docs/INTENT.md) · [`docs/SCOPE.md`](docs/SCOPE.md)

---

## What's in this repo

| Path | Contents |
|---|---|
| `content/`, `game-features/`, `plugins/`, `pipelines/` | Per-category reference docs (weapons, vehicles, items, game mechanics, UI, maps, meta, and more) |
| `season-2-changes/` | Season 1 → Season 2 changes |
| `_wiki/` | Player-facing wiki pages |
| `assets/data/` | Generated JSON behind the site's tables and viewers |
| `_tools/` | Python generators that build the tables and JSON from a local export |
| `tools/` | The C# extractor (CUE4Parse) and its notes |
| `mappings/` | Notes on the `.usmap` / `.idmap` mappings (the map files themselves are not committed) |
| `sdk/` | Notes and a package index for the Dumper-7 class dump (the dump itself is not committed) |
| `docs/` | Methodology, units, evidence notes per research round |
| `_includes/`, `_layouts/`, `_sass/` | Jekyll theme for the GitHub Pages site |

### What is not in this repo

The raw game exports (`data/`) and the Dumper-7 header dump (`sdk/raw/`)
are generated locally from an owned copy of the game and are not
published: they are the game's own material. The docs cite assets by
name and path (for example
`Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_InfantryData.json`), so anyone with the game can
produce the same files with the extractor in `tools/` and check a value.

## How it was built

1. **Extract.** CUE4Parse reads the game's `.pak`/`.utoc` files and writes each
   cooked asset as JSON ([`tools/`](tools/)).
2. **Map the code.** Dumper-7, run once against the author's own local
   copy of the game, produces the UE class hierarchy (classes, properties,
   offsets). It names the fields in the cooked data and connects assets
   to the native classes that read them.
3. **Read the binary.** Static analysis of the shipping executable in IDA
   fills in native defaults and formulas that the data does not hold
   (how multipliers combine, how damage resolves).
4. **Generate.** The scripts in [`_tools/`](_tools/) turn the local
   export into the tables and JSON on the site, so a new game build
   is a rerun, not a rewrite.

Apart from that one class dump, the work reads files on disk and an
offline binary; nothing runs against online matches. Details in
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Target build

| Attribute | Value |
|---|---|
| Game | Wardogs |
| Developer / publisher | Bulkhead / Team17 |
| Engine | Unreal Engine 5.7 |
| Build | `++Wardogs+Live-CL-516586` |
| Platform | PC (Steam AppID 1867240) |
| Season | Season 02 (data as of 2026-10-15) |

## Contributing

Corrections and new data pages are welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md). If you find something that looks
like a security problem in the game, report it to the developer rather
than in a public issue; [`SECURITY.md`](SECURITY.md) says how.

## Attribution

- **Wardogs** © Bulkhead Ltd, published by Team17
- **Unreal Engine 5.7** © Epic Games
- Community tooling: CUE4Parse, FModel, Dumper-7, IDA Pro

This is an unofficial fan project, not affiliated with or endorsed by
Bulkhead or Team17.

## License

- **Documentation** (`*.md` files, data analysis, methodology):
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code** (`_tools/`, `tools/`, site scripts): MIT License
- **Game names, values and asset names** quoted in the docs belong to
  their owners and are quoted for reference and commentary.

Full text in [`LICENSE`](LICENSE).
