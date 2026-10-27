# Patch update pipeline

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What to run when a Wardogs update lands, to turn the new build into refreshed site data. This is a GitHub-only
runbook, not a site page. The tool is [`_tools/update_pipeline.py`](../_tools/update_pipeline.py); its registry of
every `_tools` script is [`_tools/pipeline_registry.json`](../_tools/pipeline_registry.json).

## The short version

```
python -I _tools/update_pipeline.py status                          # is a new build installed?
python -I _tools/update_pipeline.py run --label s3-<steam buildid> --assets
```

`run` takes a manifest of the installed paks, extracts the whole export with CueDump and the WdExtract passes,
diffs it against the previous export, adds a worktree on branch `update-<label>`, regenerates the site there
(first against the old export, committed as a baseline, then against the new one), runs every check and writes
two reports. It ends with the commands to review and merge. It never runs the game, never touches the main
checkout and never pushes.

What it cannot do: **make a usmap**. If the new build changed the class layouts the extraction stops with a stale-usmap
message (see [Stale usmap](#stale-usmap)) and you regenerate the usmap with Dumper-7 yourself.

## What you need on the machine

| Item | Default (`environment` in the registry) | Override |
|---|---|---|
| Game paks | `E:/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks` | `WD_PIPELINE_PAKS` |
| AES key file (one hex line; never printed or committed) | `E:/WardogsConversion/CueDump/aes.txt` | `WD_PIPELINE_AES_KEY_FILE` |
| Export usmap (CueDump) | `mappings/5.7.4-516586+++Wardogs+Live-Wardogs.deobfuscated.v2.export.usmap` in the lead's checkout | `WD_PIPELINE_USMAP_CUEDUMP` |
| `normal-order.usmap` (WdExtract) | `E:/Reverse_Engineer/wardogs_analysis/round8_propertybags_20261019/normal-order.usmap` | `WD_PIPELINE_USMAP_WDEXTRACT` |
| WdExtract | `E:/Reverse_Engineer/wardogs_analysis/round76_icons/bin/WdExtract.exe` | `WD_PIPELINE_WDEXTRACT_EXE` |
| CUE4Parse checkout (builds `tools/cuedump`) | `E:/WardogsConversion/CUE4Parse/CUE4Parse/CUE4Parse.csproj` (commit `0415fe2`) | `WD_PIPELINE_CUE4PARSE_PROJECT` |
| .NET SDK 10, Python 3.13 (stdlib only) | on PATH | |
| Output root | `E:/wardogs_builds` | `WD_PIPELINE_BUILDS_ROOT` |
| `sdk/raw` (Dumper-7 SDK headers; `spread_recoil_tables.py` reads `WDGame_structs.hpp`) | the lead's checkout | `WD_PIPELINE_SDK_RAW` |

Any key can also go in a JSON file passed as `--config FILE` (before the sub-command). The extractor binary used for the
`data/` export is **built from `tools/cuedump`** into `<root>/_bin/cuedump` the first time (about 5 s). The older binary under
`E:/WardogsConversion/CueDump/bin` is an earlier build with hard-coded paths; do not use it.

The usmap behind the current `data/` is the **v2 export usmap** (`...deobfuscated.v2.export.usmap`, see
[`mappings/README.md`](../mappings/README.md#data-and-the-v2-usmap)). It reproduces the checked-in export byte for byte.

## Step by step

Each step is a sub-command; `run` chains them. Labels name a build, for example `s2` or `s3-26000000`.

| Step | Command | Writes | Measured |
|---|---|---|---|
| 1. Is there a new build? | `status [--against LABEL]` | nothing; exit code 10 when the paks differ from the last manifest | under 1 s |
| 2. Fingerprint | `snapshot --label L` | `<root>/L/manifest.json`: name, size and SHA-256 of every `.pak`, `.utoc`, `.sig` and `.dll`, and size plus first and last 4 MiB of every `.ucas`; the Steam build id | 0.7 s (files were in the OS cache; a cold disk reads about 2 GB) |
| 3. Extract | `extract --label L --assets` | `<root>/L/data/` (the CueDump export plus the curated config files and `DefaultGame.excerpt.ini`), `<root>/L/wdextract/` (file list, GE dump, icon PNGs), `extract-meta.json`, `extract.log` | about 105 s: CueDump 89 s (66,550 packages, 6,830 exported), config and passes about 15 s |
| 4. Diff | `diff --old A --new B [--full]` | `<root>/B/patch-diff.md` and `.json`: added, removed and changed assets, counts and top changed fields per site area, hashed-name noise; `--full` also runs `season_diff.py --write` into `<root>/B/season-diff/` | 7 s for the 6,830-file export; `--full` is much longer |
| 5. Regenerate | `regen --data <root>/L/data --repo <worktree>` | the site files, `regen-report.md` and `.json` | about 3 min (one pass), 5 min with `--passes 2` |
| All | `run --label L [--old A] [--assets] [--full]` | everything above in a worktree `<root>/L/worktree` on branch `update-L` | 481 s end to end when nothing changed (extract 79 s, diff 3 s, baseline regen 202 s, regen 196 s); the final regen then reported 0 changed files |

Run `audit` any time: it fails when a script in `_tools/` is missing from the registry.

### Files in `<root>/<label>/`

```
manifest.json         the fingerprint
data/                 the export the generators read (a junction target; never committed)
data_progress.log     CueDump's log: CUE4Parse warnings and per-package errors
wdextract/            files/files.txt, ge/, icons/, config/raw/ (the full DefaultGame.ini is here; never commit it)
extract-meta.json     timings, warnings/errors, number of hashed property names, config files copied
patch-diff.md/.json   what the patch changed in the data
regen-report.md/.json what the regeneration changed on the site
worktree/             the update-<label> branch (run only)
```

## What to read

1. **`patch-diff.md`** answers "what did the game change". Added assets are new items, vehicles or tables to document;
   the by-area table gives the top changed fields (a damage or price change shows up as `...Damage`, `...Cost`).
   The *property-name noise* line counts properties that appear or disappear as hashed tokens
   (`_aaaa...`): a usmap name change, not a game change. A large number there after an update means new fields
   the usmap cannot name yet (names come from Dumper-7 and `WdExtract deobfuscate`).
2. **`regen-report.md`** answers "what does the site now say differently".
   - *Generator failures / Check failures*: fix these first. `verify_round25.py` and `weapon_attributes.py --check`
     fail on main today (documented in the registry as `known_fail`, listed separately, not counted).
   - *Real changes*: `git diff --ignore-cr-at-eol --stat`. Line-ending-only rewrites are restored automatically.
   - *Possible silent parser breakage* and *Files that lost content*: a generator that parses other pages'
     Markdown (list in the report) may have matched nothing. The history rewrite once unlinked `` [`DA_x`](...) ``
     rows and two parsers silently produced empty output; a regen that shrinks a file is the signal.
   - *Changed in the second pass* (only with `--passes 2`): a generator reads another's output and ran too early; reorder
     it in the registry.
   - *Generators without a check mode*, and *Not refreshed by regen*: see below.
3. **`coverage-census.json`** in the same folder: asset families under `data/` that no published page names. After a
   patch it is the list of new things to write up.

### Reviewing and merging

```
cd <root>/<label>/worktree
git log --oneline -3                              # baseline commit (hand-edit drift) then your review
git diff --ignore-cr-at-eol --stat                # the patch's changes only (baseline already committed)
python -I _tools/check_links.py                   # 0 broken
git add -A && git commit -m "Update to build <label>: regenerated site data"
cd <main checkout> && git merge update-<label>
```

The **baseline commit** matters. Some pages were edited by hand inside generated blocks after their last
generation, and some generators are ahead of their committed output (see the acceptance test below). Running the
generators once against the *old* export first puts that drift in its own commit, so the second diff holds only what
the patch changed. If the baseline commit is not what you want to keep, `git revert` it or drop it from the merge.

## Stale usmap

Symptoms (printed by `extract`, exit code 3, data kept for inspection): CueDump exits non-zero; CUE4Parse "did not read
correctly" warnings above the baseline of 0; packages errored above the baseline of 0; no `DONE.` line. Measured with a
deliberately wrong usmap (the 507 closed-beta one): 9 packages errored.

The pipeline will not fix this and does not run the game. Yourself:

1. Run the new build with Dumper-7 (`E:/Reverse_Engineer/tools/Dumper-7`) to get the SDK and a fresh `.usmap`
   (the project procedure is in [`docs/METHODOLOGY.md`](METHODOLOGY.md) and [`mappings/README.md`](../mappings/README.md)).
2. Restore property names the way `mappings/README.md` describes (`WdExtract deobfuscate --names ... --sdk sdk/raw`,
   then the export-usmap fills), and rebuild `normal-order.usmap` if the property-bag recovery changed
   ([`tools/cue4parse_extractor/README.md`](../tools/cue4parse_extractor/README.md)).
3. Point the pipeline at the new maps (`WD_PIPELINE_USMAP_CUEDUMP`, `WD_PIPELINE_USMAP_WDEXTRACT`) and re-run
   `extract --label L --force`. When the extraction is clean, update `baseline` in the registry.
4. Put the new SDK in `sdk/raw` (and `WD_PIPELINE_SDK_RAW`). `spread_recoil_tables.py` reads it.
5. After a usmap change that only renames properties, `_tools/check_data_renames.py --base <rev>` proves no values moved.

Even when CUE4Parse reads without warnings, a patch that adds properties shows up as new hashed names
(`extract` prints how many are not in the previous export). They still read correctly; they just have no name yet.

## What regen does not refresh

`regen` runs the 73 generators whose only input is `data/` (plus committed JSON), in the order of the registry. Everything
else is listed in every report.

| Needs | Scripts | How |
|---|---|---|
| WdExtract output the pipeline makes | `item_icons.py` (the `icons` pass: `list`, `textures`, `build`), GE values (`ge` pass: `list GE_`, `dump`, `ge_summary.py` -> `assets/data/ge-values.json`, byte-identical to the committed file) | `extract --assets`, then regen picks them up |
| WdExtract dumps made by hand | `ai_detection`, `ai_eqs`, `pve_scenario_data` (round 36 dump), `r41_misc_data`, `r42_modes_data`, `vehicle_spawns` (round 41/42/51 dumps), `bp_defaults` (Blueprint dump named by its specs), `statetree_outline` (`list ST_Challenges`, `dump`), `shell_actors`, `scope_reticles`, `map_images`, `vehicle_models`, `infantry_model` | each script's docstring and the evidence note it cites give the `WdExtract` modes; run them in the regen worktree with `data/` pointing at the new export |
| The model chain (round 86) | `object_models.py` (regen runs only its `--check`), `vehicle_models.py` | the steps are in `chains` in the registry and in [`round86-models.md`](evidence/round86-models.md#regenerate): `all list ""` -> `object_models.py --plan` -> `collision` and `physics` -> `object_models.py`; the vehicle `plan` / `mesh` / `finish` cycle per vehicle; Node.js for the glTF-Transform compression |
| The restored executable | `hit_registration_check`, `native_defaults_check`, `projectile_flight_check`, `artillery_range_native`, `ida_claim_*`, `rva_status`, `vehicle_hit_location_check`; the constants encoded in `movement_tables.py` (NATIVE table), `weapon_stats_defaults.py`, `economy_tables.py` (StateTree byte values), `r45_vehicle_defaults.py`, `mode_rules.py` | after a patch the exe changes: re-restore it, re-run the checks, and re-read the constants. A changed value in `data/` does not change these |
| The Season 1 export (`E:/r22/s1/data`, no longer on disk) | `season_diff.py`, `spray_patterns.py`, `round55_s2_damage_diff.py` | use `diff --full` between the two builds instead |
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

Differences from main after the regeneration, each explained (the first two rows are fixed in this branch and no longer differ):

| File | Why |
|---|---|
| `Config/Tags/*.ini`, `DefaultGameplayTags.ini` (in `data/`, not on the site) | the lead's `data/Wardogs/Config` is the Season 1 copy (modified 16 Oct; `season_diff.py` documents "Config/*.ini was kept from Season 1"). The paks hold the Season 2 files (for example `Input.NamedActions.Vehicle.FireCountermeasures` instead of `FireFlares`, two new tag files `SquadTags.ini` and `MetaWagerGameplayTags.ini`). No generator output changes |
| `assets/data/zone-rewards.json`, `_wiki/ammunition/{308-win,7-62x39mm,9x19mm}.md` | **real bugs on main, fixed in this branch.** `zone_rewards.py` found each cash table by a heading ``...DT_Reward_Cash_X.json``; the history rewrite removed the link and `.json`, so a regeneration silently dropped all 12 cash tables. `wiki_calibers.py` looked for rows starting `\| [ID_MAGZ`; unlinked rows lost the "Season 2 changes adds N magazine items" line. Both parsers now accept both forms and reproduce the committed files |
| `assets/data/infantry-hitboxes.json` (14 lines) | `source_data_tree` becomes `HEAD:data` (it is a git tree id of `data/`, which is no longer tracked; ignored by the report), and every explosive's `damage_values` gains `bPreferUpwardsTrace`: the generator is ahead of the committed JSON |
| `game-features/Wardogs_Explosives_v1.md` (1 line) | a hand edit inside a generated block (the Molotov `BaseFuseTime` row's note about the native `bCanBeCooked` constant) is overwritten by the generator. Pre-existing drift. (`Wardogs_FireAndUtility_v1.md` showed the same kind of drift before main's round 86 updated its generator.) |
| `content/Wardogs_DataTables_v1.md`, `Wardogs_MiscGameplayAssets_v1.md`, `Wardogs_WeaponMisc_v1.md`, `Wardogs_VehicleAssets_v1.md` | generated from the whole doc tree (see above): pages written after their last generation now name assets those pages list as "unnamed" (`DA_CharacterModifierState_Critical`, `CF_DrawVelocityReleaseCurve`) or add a "Documented in" link. Pre-existing drift |

No extractor nondeterminism was found: JSON, PNG and generated output are stable across runs. Line endings: generators write LF over
CRLF checkouts; the report restores such files (`git diff --ignore-cr-at-eol`).

## Notes for maintainers

- **Adding a generator**: add one entry to `scripts` in `_tools/pipeline_registry.json` (`class`, `tier`, `write` and `check`
  argument lists, `inputs`). Order matters only when one generator reads another's output: put the producer first.
  `update_pipeline.py audit` fails for a script that is not in the registry.
- Generators read `<repo>/data` by path. `regen` therefore swaps the `data` junction of a **linked worktree** to the export
  and puts it back; it refuses to run in the main checkout. It also links `sdk/raw` for the same run.
- `--passes 2` re-runs everything and reports files that changed in the second pass; use it after adding generators.
- The pipeline is Windows-first (junctions through `mklink /J`); on other systems it falls back to symlinks.
- Secrets: the AES key is only ever read by the extractor from its file. `DefaultGame.ini` is not copied into `data/`; only
  the whitelisted excerpt is (`default_game_ini.py --extract`). The raw `wdextract/config/` folder holds the full file: keep it out of the repo.
