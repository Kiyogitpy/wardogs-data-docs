# Scope

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What this project covers and what it leaves out. Read with
[`INTENT.md`](INTENT.md).

This repository is a **data documentation project**: reference pages
for Wardogs' game data, the native code that reads it, and the
scripts that generate the pages.

## In scope

### Game data

- Cooked data assets in `Wardogs/Content/` and
  `Wardogs/Plugins/GameFeatures/`
- DataAsset and DataTable properties, curves and lookup tables
- Season-by-season changes
- Cross-references between related assets

### Code behind the data

- The UE class hierarchy from a Dumper-7 class dump, used to name
  fields and link assets to native classes
- Static analysis of the shipping executable in IDA, using the
  mappings described in [`../mappings/`](../mappings/), for native
  defaults and formulas the data does not hold ("how multipliers
  combine", "how damage resolves")

### Generators

- Scripts that turn a local export into the tables and JSON on the
  site (`_tools/`)
- The extractor that produces that export (`tools/`)

## Not published

- **Raw game exports** (`data/`) and the **class dump** (`sdk/raw/`).
  They are generated locally from an owned copy of the game. Pages
  cite assets by name and path.
- **Game binaries, pak files, keys and mapping files.**
- **Programs that act on a running game**: no loaders, injectors,
  memory readers or overlays.

## Out of scope

- Tools for gaining an advantage in online play
- Anything that runs against live matches with other players; any
  observation behind a page is done offline or in sessions no one
  else can join
- Asset extraction for use in other games or products
- Paid access of any kind: docs are CC BY-SA 4.0, code is MIT

## Security issues

A data project sometimes turns up something that looks like a
security problem in the game. Those are reported to the developer, not
published here. See [`../SECURITY.md`](../SECURITY.md).
