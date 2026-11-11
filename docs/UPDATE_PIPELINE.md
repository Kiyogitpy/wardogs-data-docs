# Patch update pipeline

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What to run when a Wardogs update lands, to turn the new build into refreshed site data. This is a GitHub-only
runbook, not a site page. The tool is [`_tools/update_pipeline.py`](../_tools/update_pipeline.py); its registry of
every `_tools` script is [`_tools/pipeline_registry.json`](../_tools/pipeline_registry.json).

## Before a new season

1. Run `python -I _tools/update_pipeline.py preflight`. It must exit 0. Exit 5 names each missing input. It also checks
   that the Season 1 and Season 2 exports `season_diff.py` compares (`season1_export`, `season2_export`) each hold
   [`Wardogs/Content`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content).
2. Check the AES key file holds the key of the new build. Preflight only checks that the file exists.
3. Keep the Season 2 export (`season2_export`, `E:/wardogs_builds/s2-cl516586/data` by default) and the Season 1 export
   (`season1_export`, `E:/wardogs_builds/season1/data`). `regen` compares them; with either one missing or empty it stops
   before it changes anything, because `season_diff.py` would otherwise rewrite the Season 2 Changes data as "everything removed".
4. If the engine or pak version moved, CUE4Parse may need an update. `tools/cuedump/Program.cs` hard-codes
   `GAME_UE5_7`.
5. Change `SEASON` in [`jenkins/patch-watch.Jenkinsfile`](../jenkins/patch-watch.Jenkinsfile) (see
   [Running it from Jenkins](#running-it-from-jenkins)).

A rehearsal of `diff --old season1 --new s2-cl516586` followed by regen was done on 2026-11-01. See
[Acceptance test](#acceptance-test-the-current-site-from-the-current-paks).

## The short version

```
python -I _tools/update_pipeline.py status                          # is a new build installed?
python -I _tools/update_pipeline.py run --label s3-<steam buildid> --assets
```

`run` takes a manifest of the installed paks, extracts the whole export with CueDump and the WdExtract passes,
diffs it against the previous export, adds a worktree on branch `update-<label>`, regenerates the site there
(first against the old export, committed as a baseline, then against the new one), runs every check and writes
its reports. It ends with the commands to review and merge. It never runs the game, never touches the main
checkout and never pushes.

What it cannot do: **make a usmap**. If the new build changed the class layouts the extraction stops with a stale-usmap
message (see [Stale usmap](#stale-usmap)) and you regenerate the usmap with Dumper-7 yourself. If the export came out
far smaller than the baseline, it stops with a truncated-export message (see [Truncated export](#truncated-export)).

## What you need on the machine

| Item | Default (`environment` in the registry) | Override |
|---|---|---|
| Game paks | `E:/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks` | `WD_PIPELINE_PAKS` |
| AES key file (one hex line; never printed or committed) | `E:/WardogsConversion/CueDump/aes.txt` | `WD_PIPELINE_AES_KEY_FILE` |
| Export usmap (CueDump) | `mappings/5.7.4-516586+++Wardogs+Live-Wardogs.deobfuscated.v2.export.usmap` in the lead's checkout | `WD_PIPELINE_USMAP_CUEDUMP` |
| `normal-order.usmap` (WdExtract) | `E:/Reverse_Engineer/wardogs_analysis/round8_propertybags_20261019/normal-order.usmap` | `WD_PIPELINE_USMAP_WDEXTRACT` |
| WdExtract | `E:/Reverse_Engineer/wardogs_analysis/round76_icons/bin/WdExtract.exe` | `WD_PIPELINE_WDEXTRACT_EXE` |
| Oodle DLL (passed to WdExtract) | `E:/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks/oo2core_9_win64.dll` | `WD_PIPELINE_OO2CORE` |
| CUE4Parse checkout (builds `tools/cuedump`; needed only when CueDump must be rebuilt, see below) | `E:/WardogsConversion/CUE4Parse/CUE4Parse/CUE4Parse.csproj` (commit `0415fe2`) | `WD_PIPELINE_CUE4PARSE_PROJECT` |
| Season 2 export (`season_diff.py` in regen; needs [`Wardogs/Content`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content)) | `E:/wardogs_builds/s2-cl516586/data` | `WD_PIPELINE_SEASON2_EXPORT` |
| Season 1 export (`season_diff.py` in regen; needs [`Wardogs/Content`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content)) | `E:/wardogs_builds/season1/data` | `WD_PIPELINE_SEASON1_EXPORT` |
| .NET SDK 10, Python 3.13 (stdlib only) | on PATH | |
| Output root | `E:/wardogs_builds` | `WD_PIPELINE_BUILDS_ROOT` |
| `sdk/raw` (Dumper-7 SDK headers; `spread_recoil_tables.py` reads `WDGame_structs.hpp`) | the lead's checkout | `WD_PIPELINE_SDK_RAW` |

Any key can also go in a JSON file passed as `--config FILE` (before the sub-command). The extractor binary used for the
`data/` export is **built from `tools/cuedump`** into `<root>/_bin/cuedump` (about 5 s). `CueDump.sources.sha256` next to the
exe holds the SHA-256 of `Program.cs` and `CueDump.csproj` (line endings ignored); `extract` rebuilds only when the sources no
longer match it, never because of file times (a fresh clone or worktree is always newer). An exe with no hash file is accepted
as it is: `extract` records the current hash and says so. So the CUE4Parse checkout is needed only for the first build or after
a change to those two files. The older binary under `E:/WardogsConversion/CueDump/bin` is an earlier build with hard-coded
paths; do not use it.

The usmap behind the current `data/` is the **v2 export usmap** (`...deobfuscated.v2.export.usmap`, see
[`mappings/README.md`](../mappings/README.md#data-and-the-v2-usmap)). It reproduces the checked-in export byte for byte.

## Step by step

Each step is a sub-command; `run` chains them. Labels name a build, for example `s2` or `s3-26000000`.

| Step | Command | Writes | Measured |
|---|---|---|---|
| 0. Inputs | `preflight [--step extract\|regen\|run]` | nothing | a path check only |
| 1. Is there a new build? | `status [--against LABEL]` | nothing; exit code 10 when the paks differ from the last manifest of a build whose extraction passed (a label whose `extract-meta.json` says `usmap-stale` or `export-shrunk` is skipped) | under 1 s |
| 2. Fingerprint | `snapshot --label L` | `<root>/L/manifest.json`: name, size and SHA-256 of every `.pak`, `.utoc`, `.sig` and `.dll`, and size plus first and last 4 MiB of every `.ucas`; the Steam build id | 0.7 s (files were in the OS cache; a cold disk reads about 2 GB) |
| 3. Extract | `extract --label L --assets` | `<root>/L/data/` (the CueDump export plus the curated config files and `DefaultGame.excerpt.ini`), `<root>/L/wdextract/` (file list, GE dump, icon PNGs), `extract-meta.json`, `extract.log` | about 105 s: CueDump 89 s (66,550 packages, 6,830 exported), config and passes about 15 s |
| 4. Diff | `diff --old A --new B [--full]` | `<root>/B/patch-diff.md` and `.json`: added, removed and changed assets, counts and top changed fields per site area, hashed-name noise; `review-pages.md` and `.json`; `--full` also runs `season_diff.py --write` into `<root>/B/season-diff/` | about 27-60 s for the Season 1 to Season 2 change set; `--full` is much longer |
| 5. Regenerate | `regen --data <root>/L/data --repo <worktree> [--allow-shrink]` | the mirror of the export in the worktree's `data/`, the site files, `regen-report.md` and `.json`, `hashed-names.json` | about 3 min (one pass), 5 min with `--passes 2` |
| All | `run --label L [--old A] [--assets] [--full]` | everything above in a worktree `<root>/L/worktree` on branch `update-L` | 481 s end to end when nothing changed (extract 79 s, diff 3 s, baseline regen 202 s, regen 196 s); the final regen then reported 0 changed files |

`extract`, `regen` and `run` run `preflight` first. Preflight only checks paths: it never reads the key file. It checks the
inputs `extract` needs (`paks`, `aes_key_file`, `usmap_cuedump`, `usmap_wdextract`, `wdextract_exe`, `oo2core`, `builds_root`,
and `cue4parse_project` only when CueDump has to be rebuilt). `--step regen` checks `season2_export` and `season1_export`,
each of which must hold [`Wardogs/Content`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content) (a regen that skips `season_diff` with `--skip` or `--only` does not need them).
`run` checks all of these plus `sdk_raw`. Without `--step`, `preflight` checks what `run` needs.
When something is missing it prints one line per input, with the registry key and the `WD_PIPELINE_` name to set:

```
PREFLIGHT FAILED (run): 2 required input(s) missing, nothing was run.
  aes_key_file       <path>  (missing; set WD_PIPELINE_AES_KEY_FILE or pass --config FILE)
```

### Exit codes

| Code | Meaning |
|---|---|
| 0 | OK. `status` exits 0 when no new build is installed. `run` also exits 0 when the paks match the last extracted build |
| 1 | A generator failed (regen, run). Other commands that stop with an error message also exit 1 |
| 3 | Extraction not trustworthy (extract, run): a stale usmap, canary values missing or of the wrong type, or a truncated export (including CueDump stopping because too few containers mounted). The `status` field of `extract-meta.json` says which (`usmap-stale` or `export-shrunk`) |
| 4 | A check failed (regen, run) |
| 5 | Preflight: a machine input is missing. Nothing was run (regen and run included) |
| 6 | `regen` could not start, so nothing was regenerated: not a data export, the mirror was refused (see [Notes for maintainers](#notes-for-maintainers)), or the worktree is the main checkout or belongs to another repository. `run` stops on 5 and 6 |
| 10 | `status`: a new build is installed |

Run `audit` any time: it fails when a script in `_tools/` is missing from the registry.

### Files in `<root>/<label>/`

```
manifest.json         the fingerprint
data/                 the CueDump export (JSON plus the curated config files); regen mirrors it into the worktree's tracked data/
data_progress.log     CueDump's log: CUE4Parse warnings and per-package errors (deleted before each CueDump run, so an old log is never read)
wdextract/            files/files.txt, ge/, icons/, config/raw/ (the full DefaultGame.ini is here; never commit it)
extract-meta.json     timings, warnings/errors, the gate's measured counts, canary results, number of hashed property names, config files copied
patch-diff.md/.json   what the patch changed in the data
review-pages.md/.json the pages to review by hand after the patch (written by diff)
regen-report.md/.json what the regeneration changed on the site
hashed-names.json     hard-coded hashed names the export lacks (written by regen)
worktree/             the update-<label> branch (run only)
```

## What to read

1. **`patch-diff.md`** answers "what did the game change". Added assets are new items, vehicles or tables to document;
   the by-area table gives the top changed fields (a damage or price change shows up as `...Damage`, `...Cost`).
   Changed files are ranked by distinct changed fields, with array indices folded (`Heights[*]`). Files that differ only
   in hashed property names are counted apart as rename-only. Files that do not parse (a truncated export) have their own
   section and are not compared. The *property-name noise* line gives the number of distinct hashed tokens
   (`_aaaa...`) that appear, disappear or are renamed: a usmap name change, not a game change. A large number there
   after an update means new fields the usmap cannot name yet (names come from Dumper-7 and `WdExtract deobfuscate`).
2. **`review-pages.md`** is the to-do list for hand-edited wiki prose after a patch. `regen` never changes that prose.
   It lists the pages that name a changed or removed asset, hand-written pages first. Direct hits come first, wiki
   articles before reference pages. Indirect hits are wiki articles that cite a reference page naming the asset:
   "likely" when a line naming the asset also holds the article's title or internal name, "weaker" otherwise.
   Historical change-log pages have their own section, and generated pages come last. `run` writes it only when there
   is an earlier build to diff against.
3. **`regen-report.md`** answers "what does the site now say differently".
   - *Generator failures / Check failures*: fix these first. They are grouped by error, so one cause is one line; the
     per-script list follows. On main today every check passes (0 known failures).
     `verify_round25.py` treats four documented REFUTED wordings (`round25-verification.md`) as expected.
   - *Real changes*: `git diff --ignore-cr-at-eol --stat`. Line-ending-only rewrites are restored automatically.
   - *Possible silent parser breakage* and *Files that lost content*: a generator that parses other pages'
     Markdown (list in the report) may have matched nothing. The history rewrite once unlinked `` [`DA_x`](...) ``
     rows and two parsers silently produced empty output; a regen that shrinks a file is the signal.
   - *Changed in the second pass* (only with `--passes 2`): a generator reads another's output and ran too early; reorder
     it in the registry.
   - *Hard-coded hashed names missing from this export*: `hashed_names_check.py` lists hashed property names that
     `_tools` scripts hard-code but the export lacks. A new usmap can rename them, and a script that reads a renamed name
     fails. This is a warning only; the full list is in `hashed-names.json`. The Season 2 export lacks 14 of the 67 on
     purpose: `bp_defaults.py` (10 Blueprint dump names), `spread_recoil_tables.py` (2 SDK dump names) and
     `spray_patterns.py` (2 Season 1 bipod names, kept for the legacy export). They are listed with a reason in
     `hashed_names_expected_missing` in the registry. The report lists only the misses that are not in that list, and
     shows the allowlisted ones as a count (`1 (+14 expected, allowlisted in the registry)`) with their reasons below.
     A new miss means a new usmap rename. Add a name to the list only after checking why the export lacks it.
   - *Generators without a check mode*, and *Not refreshed by regen*: see below.
4. **`coverage-census.json`** in the same folder: asset families under `data/` that no published page names. After a
   patch it is the list of new things to write up.
5. **Canary values** (`_tools/canary_values_check.py`, values in `_tools/canary_values.json`): 25 values the site already
   publishes (weapons, a vehicle, the SPH-2 table, prices, reward formulas, movement). `extract` checks them on the fresh
   export. A value that is missing or of the wrong type stops the extract with exit 3 (`usmap-stale`). A changed value only
   prints a warning. `regen` runs `--check` as a checker, so a real balance patch shows as a check failure (exit 4) until
   you have reviewed the change and run `python -I _tools/canary_values_check.py --accept`. `--accept` writes nothing
   while a canary is missing or of the wrong type.

### Reviewing and merging

```
cd <root>/<label>/worktree
git log --oneline -3                              # baseline commit (hand-edit drift) then your review
git diff --ignore-cr-at-eol --stat                # the patch's changes only (baseline already committed)
python -I _tools/check_links.py                   # 0 broken
git add -A && git commit -m "Update to build <label>: regenerated site data"
cd <main checkout> && git merge update-<label>
```

`data/` is tracked, so `git add -A` also commits the new raw JSON. The report shows it as one line, `data/: +A -R ~C`
(counted by git, new directories file by file). `regen` prints the mirror twice: the tracked JSON counts (what git will see)
and the raw copy counts, which also include the ignored non-JSON config files. When it adds that some files differ from
`data/` only by letter case (`Audio/Wavs` against `Audio/WAVs`), a case-insensitive checkout does not see the new spelling;
commit it with `git -c core.ignorecase=false add -A data`. `regen` only reports this.

The **baseline commit** matters. Some pages were edited by hand inside generated blocks after their last
generation, and some generators are ahead of their committed output (see the acceptance test below). Running the
generators once against the *old* export first puts that drift in its own commit, so the second diff holds only what
the patch changed. If the baseline commit is not what you want to keep, `git revert` it or drop it from the merge.

## Stale usmap

Symptoms (printed by `extract`, exit code 3, data kept for inspection): CueDump exits non-zero after it exported (with no
`data/` it is a [truncated export](#truncated-export) instead); CUE4Parse "did not read
correctly" warnings above the baseline of 0; packages errored above the baseline of 0; no `DONE.` line; a canary value
missing or of the wrong type (status `usmap-stale`). Measured with a deliberately wrong usmap (the 507 closed-beta one):
9 packages errored.

The pipeline will not fix this and does not run the game. Yourself:

1. Run the new build with Dumper-7 (`E:/Reverse_Engineer/tools/Dumper-7`) to get the SDK and a fresh `.usmap`
   (see [`sdk/README.md`](../sdk/README.md) and [`mappings/README.md`](../mappings/README.md)).
2. Restore property names the way `mappings/README.md` describes (`WdExtract deobfuscate --names ... --sdk sdk/raw`,
   then the export-usmap fills), and rebuild `normal-order.usmap` if the property-bag recovery changed
   ([`tools/cue4parse_extractor/README.md`](../tools/cue4parse_extractor/README.md)).
3. Point the pipeline at the new maps (`WD_PIPELINE_USMAP_CUEDUMP`, `WD_PIPELINE_USMAP_WDEXTRACT`) and re-run
   `extract --label L --force`. When the extraction is clean, update `baseline` in the registry.
4. Put the new SDK in `sdk/raw` (and `WD_PIPELINE_SDK_RAW`). `spread_recoil_tables.py` reads it.
5. After a usmap change that only renames properties, `_tools/check_data_renames.py --base <rev>` proves no values moved.

Even when CUE4Parse reads without warnings, a patch that adds properties shows up as new hashed names
(`extract` prints how many are not in the previous export). They still read correctly; they just have no name yet.

## Truncated export

`extract` exits 3 and writes status `export-shrunk` to `extract-meta.json` when the export is far smaller than the
baseline. It checks four things:

- exported files, or packages read, more than 1% below the baseline (`cuedump_exported_files`, `cuedump_packages`);
- JSON bytes under `data/` more than 5% below `cuedump_exported_bytes` (the [`Wardogs/Config`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Config) files are not counted);
- fewer containers mounted than `cuedump_mounted_vfs`, once that key is set;
- containers that did not mount, as CueDump reports them. This check is **inert**: CueDump does not print the `Unmounted`
  line yet, and `extract` honours it only once CueDump does.

The likeliest cause is a **rotated AES key**: containers encrypted with the new key do not mount, so their packages
drop out of the export. CueDump itself stops with exit 1 ("Only N containers mounted - wrong key or unsupported format")
when fewer than 10 containers mount, before it creates `data/` or writes its log, so there are no counts to compare.
`extract` treats that case, and any CueDump failure that left no `data/` behind, as a truncated export (status
`export-shrunk`, the key message). A CueDump failure after it exported stays a usmap problem. `extract` deletes the label's
`data_progress.log` before it runs CueDump, so a log from an earlier run is never taken for this run's.

What to do:

1. Recover the key for this build and put it in the key file (`WD_PIPELINE_AES_KEY_FILE`). The recovery steps are in
   local notes, not in this repo. Never print or commit the key.
2. Check that the Paks folder is complete: Steam has finished the update.
3. Run `extract --label L --force` again.
4. Only if the build really removed that much content, change the matching key in `baseline`.

The data written under `<root>/L/data/` is kept for inspection and must not go to the site.

Baseline keys in `_tools/pipeline_registry.json`:

| Key | Baseline | Gate |
|---|---|---|
| `cuedump_exported_files` | 6,830 | more than 1% fewer exported files fails |
| `cuedump_packages` | 66,550 | more than 1% fewer packages read fails |
| `cuedump_exported_bytes` | 337,079,676 | more than 5% fewer bytes fails |
| `cuedump_mounted_vfs` | 32 | fewer mounted containers fails; skipped when `null` |
| `cuedump_warnings`, `cuedump_errored` | 0 | more than this means a stale usmap (see above) |

`cuedump_mounted_vfs` is the `Mounted N vfs` count of the clean run on build 5.7.4-516586 (32). After a patch that changes
the number of containers, copy `gate.measured.mounted` from a clean run's `extract-meta.json` into it.

## What regen does not refresh

`regen` runs the 78 core generators in the order of the registry. Most read only `data/` and committed JSON;
`season_diff.py` also reads the Season 1 export and the pinned Season 2 export (preflight and `regen` require both). Everything else is listed in every report.

| Needs | Scripts | How |
|---|---|---|
| WdExtract output the pipeline makes | `item_icons.py` (the `icons` pass: `list`, `textures`, `build`), GE values (`ge` pass: `list GE_`, `dump`, `ge_summary.py` -> `assets/data/ge-values.json`, byte-identical to the committed file) | `extract --assets`, then regen picks them up |
| WdExtract dumps made by hand | `ai_detection`, `ai_eqs`, `pve_scenario_data` (round 36 dump), `r41_misc_data`, `r42_modes_data`, `vehicle_spawns` (round 41/42/51 dumps), `bp_defaults` (Blueprint dump named by its specs), `statetree_outline` (`list ST_Challenges`, `dump`), `shell_actors`, `scope_reticles`, `map_images`, `vehicle_models`, `infantry_model` | each script's docstring and the evidence note it cites give the `WdExtract` modes; run them in the regen worktree with `data/` pointing at the new export |
| The model chain (round 86) | `object_models.py` (regen runs only its `--check`), `vehicle_models.py` | the steps are in `chains` in the registry and in [`round86-models.md`](evidence/round86-models.md#regenerate): `all list ""` -> `object_models.py --plan` -> `collision` and `physics` -> `object_models.py`; the vehicle `plan` / `mesh` / `finish` cycle per vehicle; Node.js for the glTF-Transform compression |
| The restored executable | `hit_registration_check`, `native_defaults_check`, `projectile_flight_check`, `artillery_range_native`, `ida_claim_*`, `rva_status`, `vehicle_hit_location_check`; the constants encoded in `movement_tables.py` (NATIVE table), `weapon_stats_defaults.py`, `economy_tables.py` (StateTree byte values), `r45_vehicle_defaults.py`, `mode_rules.py` | after a patch the exe changes: re-restore it, re-run the checks, and re-read the constants. A changed value in `data/` does not change these |
| The Season 1 export and the Season 2 pin | `season_diff.py` runs in regen against the Season 1 export (`season1_export`, `WD_PIPELINE_SEASON1_EXPORT`, `E:/wardogs_builds/season1/data`) and the pinned Season 2 export (`season2_export`, `WD_PIPELINE_SEASON2_EXPORT`), not against `data/`, so regen reproduces the committed Season 2 Changes data at any later build. It exits non-zero when either side has no JSON files, so a missing export cannot turn into an "everything removed" rewrite. `Wardogs/Config/**` JSON is skipped because the S1 export has none; one S1 file, [`Kavkazi_Bakurani_KOTH_01.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Maps/PSOWarming/Kavkazi_Bakurani_KOTH_01.json), is truncated at 615 KiB and reported as not compared. `spray_patterns.py` is manual tier: it hard-codes Season 2 as `data/`, so regen does not run it | a new build's season diff is not written by regen: use `diff --old A --new B --full` |
| Not regenerated on purpose | `ge_values.py` | its page was edited by hand after the last generation; running it deletes the edits. Regenerate `ge-values.json` through the `ge` pass and edit the page |

Some pages are generated from the **whole doc tree**, not only `data/` (the residual-gap pages `misc_gameplay_tables`,
`weapon_misc_tables`, `vehicle_asset_tables`, `pve_settings_tables`, and the `datatable_catalog` "Documented in" column).
Their output changes whenever any page names an asset, so a regen shows diffs there that are not patch changes.

## Publishing a Season or patch diff page

The Season 2 Changes pages are built from `_tools/season_diff.py` output plus hand-written headline sections.
For a new patch:

1. `python -I _tools/update_pipeline.py diff --old A --new B --full` gives `<root>/B/season-diff/` (`index.json` and one
   file per site area; the same format as `assets/data/season-diff/`). It is deterministic and pairs moved/renamed assets.
2. Copy that folder to `assets/data/season-diff-<label>/` in the update worktree.
3. Copy `season-2-changes/` to `<label>-changes/` and point every browser at the new folder:
   `data-sd-base="{{ '/assets/data/season-diff-<label>/' | relative_url }}"` (in `all-changes.md` and the landing
   page's `data-sd-totals`). The browser JavaScript is `assets/js/season-diff.js`; it needs no change.
4. Write the headline sections by hand from `patch-diff.md` and the area JSON (the Season 2 pages show the pattern),
   with `parent:` and `description:` front matter and the style in [`WIKI_STYLE.md`](WIKI_STYLE.md).
5. `python -I _tools/check_links.py`.

`season_diff.py` carries two Season 1 specific tables (`GIT_RENAMES`, `REJECTED`); they pair nothing in a new patch and
are harmless. Its noise rules (hashed names, swapped keys, shifted references) apply unchanged.

## Acceptance test: the current site from the current paks

Run on 2026-10-27 against the installed build (Steam build id 25937608, CL 516586), branch `r87-pipe` merged with
main `82b99ed2`:

| Step | Result |
|---|---|
| `extract --label now --assets` | 103 s. 66,550 packages, 6,830 exported, 0 warnings, 0 errors. **All 6,830 JSON files are byte-identical to the checked-in `data/`** |
| config copy | 63 files. Eight `Config/Tags` files and `DefaultGameplayTags.ini` differ from the lead's `data/`, and two tag files are new (see below) |
| `ge` pass | 341 effects; `ge_summary.json` byte-identical to `assets/data/ge-values.json` |
| `icons` pass | 647 textures extracted in 7 s; `item_icons.py build` leaves `assets/img/icons` and `item-icons.json` unchanged (PNG output deterministic) |
| `regen` | 73 generators and 53 checks, 0 failures; 205 s for one pass (a two-pass run took 301 s and no file changed in pass 2, so the registry order is stable). 166 files were rewritten with LF over CRLF and restored; 6 files really differ from main (below) |

After the follow-up fixes the regeneration of main produces **no differences**. What was behind the earlier diffs, all
fixed at the source: two page parsers the history rewrite broke (`zone_rewards.py`, `wiki_calibers.py`); a hand edit
inside a generated block (the Molotov native-constant note, now in `explosive_tables.py`); `infantry-hitboxes.json`
and the four doc-tree pages (`DataTables`, `MiscGameplayAssets`, `WeaponMisc`, `VehicleAssets`) regenerated because
their generators were ahead of the committed output; `source_data_tree` / `data_tree` ids (git tree of an untracked
`data/`) now keep the last recorded value instead of writing `HEAD:data`/`unknown`; `season_diff.py` no longer lists the
34 `Wardogs/Config/Experiences/*.json` files as added. The lead's [`data/Wardogs/Config`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Config) was the Season 1 copy; the paks
hold Season 2 tags (`FireCountermeasures`, `SquadTags.ini`, `MetaWagerGameplayTags.ini`), and generator output did not change.

The residual-gap pages are fixpoints now, but they change whenever a page starts naming one of their assets; that is
expected and the baseline commit of `run` absorbs it.

No extractor nondeterminism was found: JSON, PNG and generated output are stable across runs. Line endings: generators write LF over
CRLF checkouts; the report restores such files (`git diff --ignore-cr-at-eol`).

**2026-11-01 rehearsal (Season 1 to Season 2 change set).** The rehearsal ran `diff --old season1 --new s2-cl516586`
and then regen. It found three blockers, all fixed since. Regen refused a tracked `data/` (it junctioned it; it now
mirrors the export into the worktree's `data/`). Five scripts failed to import under `python -I` (they now put their
own folder on `sys.path`; `_tools/test_isolated_imports.py` checks this). `season_diff.py` would have overwritten the
Season 2 data (it is now pinned to `season2_export`).

## Running it from Jenkins

[`jenkins/patch-watch.Jenkinsfile`](../jenkins/patch-watch.Jenkinsfile) runs `status` every 3 hours and, when a new build
is installed, `run --label <season>-<buildid> --assets`, for example `s2-26000000` (or the `LABEL` parameter). The
season prefix is `SEASON` in the Jenkinsfile: change it when a new season starts. It runs on the lead's PC through a Jenkins
agent labelled `wardogs` and calls the main checkout's `update_pipeline.py`, so the `update-<label>` branch lands in the
main checkout as with a manual run. The Jenkins server, the agent and the job definition live in the
[`jenkins-demo`](https://github.com/Kiyogitpy/jenkins-demo) repo (`scripts/windows-agent.ps1`, `jenkins/casc.yaml`).

| Situation | Build result |
|---|---|
| Wardogs is running, Steam is still updating (`StateFlags` not 4), or `status` exits 0 | not built; the reason is the build description |
| `run` exits 0 | success: review and merge the branch as above |
| `run` exits 1 or 4 with a `regen-report.md` | unstable: generators or checks failed |
| `run` exits 3 | failed. The job reads `status` in `extract-meta.json` for the description and the message: `usmap-stale` ("stale usmap": regenerate the usmap), `export-shrunk` ("truncated export": fix the key first), anything else "extraction not trustworthy". After the fix the next 3-hourly run retries by itself: `status` skips a label whose extraction failed, and `extract` replaces that label's failed `data/` without `--force`. To run it at once: `run --label <label> --assets --force` |
| `run` exits 5 (preflight: a machine input is missing; nothing ran) | failed ("machine inputs missing"). Run `preflight`, fix what it names, then rebuild |
| `run` exits 6 (regen could not start) | failed. Read the message in the log (mirror refused, wrong worktree) |

`patch-diff.md`, `regen-report.md` and `extract-meta.json` are archived on the build. The job never pushes and never
starts or stops the game.

## Notes for maintainers

- **Cleaning up**: `clean --label L` removes a `run` worktree safely. It removes the `sdk/raw` junction first (link only)
  if one is still there, checks its target survives, then runs `git worktree remove` without `--force`. Git refuses
  while the worktree has uncommitted changes, so commit the mirrored `data/` first. The branch is deleted only when it is
  merged. Never use `rm -rf` or `--force` on a worktree while the `sdk/raw` junction is in place.
- **Adding a generator**: add one entry to `scripts` in `_tools/pipeline_registry.json` (`class`, `tier`, `write` and `check`
  argument lists, `inputs`). Order matters only when one generator reads another's output: put the producer first.
  `update_pipeline.py audit` fails for a script that is not in the registry.
- Generators read `<repo>/data` by path. `regen` therefore makes the worktree's tracked `data/` an exact copy of the
  export: it copies new and changed files and deletes files the export no longer has. It also links `sdk/raw` for the same
  run and removes the link at the end. It refuses (exit 6, nothing changed) to run in the main checkout, in a worktree of
  another repository (the worktree must share the script's git common dir), when the export holds fewer than 90% of the
  JSON files `data/` has (an empty or truncated export would empty `data/`; `--allow-shrink` overrides it for a build that
  really removed that much), and when a link inside `data/` would make a copy land outside it.
- `run` commits the baseline only when the baseline regen wrote its `regen-report.json` in this run (exit 1 alone also means
  generators failed after a normal start), and diffs only against labels whose extraction passed.
- `--passes 2` re-runs everything and reports files that changed in the second pass; use it after adding generators.
- The pipeline is Windows-first (junctions through `mklink /J`); on other systems it falls back to symlinks.
- Secrets: the AES key is only ever read by the extractor from its file. `DefaultGame.ini` is not copied into `data/`; only
  the whitelisted excerpt is (`default_game_ini.py --extract`). The raw `wdextract/config/` folder holds the full file: keep it out of the repo.
