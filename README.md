# Wardogs Data Docs

[![Site](https://img.shields.io/badge/wiki-live-brightgreen)](https://kiyogitpy.github.io/wardogs-data-docs/)
[![License](https://img.shields.io/badge/docs-CC--BY--SA--4.0-blue)](LICENSE)
[![Code](https://img.shields.io/badge/code-MIT-blue)](LICENSE)

Game data, reference pages and a player wiki for **Wardogs**. This repository
includes the raw JSON asset exports, the scripts that read them, and the
generated data behind the site's tables and interactive tools.

**[Read the wiki](https://kiyogitpy.github.io/wardogs-data-docs/)** ·
**[Browse the data reference](https://kiyogitpy.github.io/wardogs-data-docs/reference/)** ·
**[Browse raw exports](data/)**

## What you'll find

- Weapon stats, damage calculations, penetration, spread and recoil.
- Vehicle stats, damage routing, hitboxes and collision viewers.
- Equipment, attachments, building, progression and the economy.
- Game modes, maps and Season 1 to Season 2 comparisons.
- Source asset paths and evidence notes for checking where a value came from.

The wiki explains the mechanics. The reference pages go into the underlying
fields, tables and formulas. Where a value is unknown or inferred, check the
page's evidence and limitations before treating it as an in-game result.

## Repository layout

| Path | Contents |
| --- | --- |
| [`_wiki/`](_wiki/) | Player wiki articles |
| [`content/`](content/), [`game-features/`](game-features/), [`plugins/`](plugins/) | Detailed game-data reference pages |
| [`pipelines/`](pipelines/) | Mechanics, calculations and interactive viewers |
| [`data/`](data/) | Raw JSON asset exports, retaining their original game paths |
| [`assets/data/`](assets/data/) | Generated JSON used by the site and its tools |
| [`season-2-changes/`](season-2-changes/) | Season 1 to Season 2 data comparisons |
| [`_tools/`](_tools/) | Generators, data checks and the update pipeline |
| [`tools/`](tools/) | CUE4Parse-based extraction tools and setup notes |
| [`docs/`](docs/) | Evidence notes, units, update instructions and wiki conventions |
| [`sdk/`](sdk/), [`mappings/`](mappings/) | Class and mapping documentation; dumps and binary mappings stay local |
| `_includes/`, `_layouts/`, `_sass/` | Jekyll site templates and styles |

## Working with the JSON

There are two kinds of data in the repository:

- **Raw exports in `data/`** preserve the extractor output. Their paths mirror
  the cooked assets, so an asset named in a reference page can be found here.
- **Site data in `assets/data/`** contains the generated records used by tables,
  calculators and viewers. Start here if you want the processed values.

Many raw `.json` files contain one or more JSON objects separated by export
headers:

```text
--- export: UDataTable / DT_GlobalDamage_InfantryData ---
```

These files are export streams, not a single JSON document. Split them at the
headers before parsing each object. The generators in [`_tools/`](_tools/)
handle this format; [`damage_tables.py`](_tools/damage_tables.py) is one example.
Files without export headers can be parsed as ordinary JSON.

The raw exports are tracked in Git. Game executables, pak files, AES keys,
binary mappings, the `sdk/raw/` class dump and non-JSON extracted files are not.

## How the reference is built

CUE4Parse reads the cooked assets from the game files. Class information from
a local Dumper-7 dump helps identify properties, while static analysis of the
shipping executable supplies native defaults and formulas missing from the
assets. The Python generators turn those inputs into reference tables and
site JSON.

For extraction requirements, configuration and the update procedure, see
[`docs/UPDATE_PIPELINE.md`](docs/UPDATE_PIPELINE.md). Regenerating everything
requires local inputs that are not included in a clone, including the game
files, the matching keys and mappings, and the SDK dump used by some generators.

## Documented build

| Attribute | Value |
| --- | --- |
| Game | Wardogs |
| Developer / publisher | Bulkhead / Team17 |
| Platform | PC, Steam AppID `1867240` |
| Engine | Unreal Engine 5.7 |
| Build | `++Wardogs+Live-CL-516586` |
| Season | Season 02 |

Values describe this build, not necessarily a later patch or a server-side
override. A stored asset value alone does not establish how it behaves in a match.

## Corrections and contributions

Found a wrong number or a missing explanation? Include the page, asset path,
game build and evidence for the correction. For generator changes, include the
updated output. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Report security findings through the channel in [`SECURITY.md`](SECURITY.md),
not a public issue.

## Credits and licensing

Wardogs is developed by Bulkhead and published by Team17. Unreal Engine belongs
to Epic Games. This is an unofficial fan project with no affiliation or
endorsement from those companies.

The workflow uses community tools including CUE4Parse, FModel and Dumper-7,
alongside IDA Pro.

Documentation and analysis are licensed under **CC BY-SA 4.0**; project code is
licensed under **MIT**. The game's assets and other third-party material are
not relicensed under those terms. See [`LICENSE`](LICENSE).
