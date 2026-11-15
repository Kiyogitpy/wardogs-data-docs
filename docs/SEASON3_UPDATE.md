# S2 → S3 data update

The public snapshot uses S3 / 0.3 CL-533731 / hotfix 533689. Current `data/` contains 7,086 tracked JSON files: 7,082 CueDump outputs and four curated config exports. The baseline is the saved Season 2 tree at `8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b`, containing 6,866 JSON files. Historical original containers were not independently reparsed.

The current JSON data tree is `592912092880ffb3e02a5a8e9f5e4b6e79bc8116`, introduced by `ffa9ab68af7366650c23a77ea5574f7a742ee495`. The full extraction remains rejected with three UI errors and five warnings. Missing wager Categories, water-field associations and current native behavior remain unresolved. This is a bounded saved-data update with explicit gaps; the extraction acceptance baseline is unchanged.

## What readers can use

- [S3 notes](../_wiki/patch-notes/season-3.md), including caliber, damage-rule, buildable, wager and achievement changes.
- [Searchable S2→S3 comparison](../season-3-changes/all-changes.md), with separate old/current columns and ten areas.
- Current regenerated tables and calculators, retaining their native-model and geometry build limits.
- Current [achievement](../_wiki/progression-and-economy/achievements.md) and [wager](../_wiki/progression-and-economy/wagers.md) inventories. Unknown categories are not copied from S2.

The [S1→S2 dataset](../season-2-changes/all-changes.md) stays separate and byte-identical. Its source links pin the S2 revision, as do the historical curve links in the S3 notes.

## Reproduce the comparison

Use a fresh checkout containing only committed inputs. Local extraction directories can contain ignored configs outside the public Git snapshot. The comparator rejects extra files; never force-add private full configs to make a comparison pass.

```powershell
git worktree add --detach ../wardogs-s2-comparison 8d0d6a9a0a3a0a0170e7ff3929202a92a5b9c12b
python -I -B _tools/season3_diff.py --s2 ../wardogs-s2-comparison/data --s3 data --out assets/data/season3-diff --s2-manifest assets/data/season3-diff/manifest-s2.json --s3-manifest assets/data/season3-diff/manifest-s3.json --check
python -I -B _tools/test_season3_diff.py
node _tools/generator_source_links_check.js
```

Replace `--check` with `--write` only when deliberately regenerating this source-bound comparison. For a later build, preserve this dataset and create reviewed source manifests; changing a manifest does not validate a new mapping.

The manifests account for every public input path, raw SHA256 and size. `files.json` records complete file presence; `index.json` names each area artifact and its identity. Files pair by exact path, exports by full header and occurrence, and arrays by index. Duplicate keys, missing/extra/changed files and malformed JSON reject before writes. Internal renames and reference shifts remain literal differences, not inferred gameplay changes.

The generator and comparison JSON have pinned LF checkout rules so their source/artifact hashes remain reproducible on Windows and Linux.

Values larger than 1,024 serialized bytes use exact saved-source references, with side, file hash, export identity, JSON pointer, type, count, byte length and content hash. Small numeric changes remain inline, with exact literals where JavaScript cannot represent them precisely. Common-file field operations and file-only values have separate counts. Snapshot absence never proves game removal.

## Validation and outstanding work

Core regeneration exercised 78 generators and changed 149 generated files. Economy and water checks still fail their semantic obligations. Later damage, source-target, loadout Python/JavaScript parity, viewer, focused compatibility and comparison checks are recorded separately; they do not retroactively make the full run pass.

The private knowledge hub is separate from this public site, which GitHub Pages builds from the repository. Private ledgers, graphs, raw package captures, full config captures, decoder DLLs and local mapping binaries are excluded from publication.
