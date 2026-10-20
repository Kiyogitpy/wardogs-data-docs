---
title: Round 9 integration audit
nav_exclude: true
---

# Round 9 integration audit — 2026-10-19

Read-only integration audit of the 17 Round-8 research entries marked closed in `docs/WHAT_IS_LEFT.md` §2.4 and `docs/ROUND8_STATUS.md`. The only code/data gates run were existing checkers. This audit does not repeat native analysis and does not claim runtime parity.

| Closed topic | Evidence and integration surface | Audit result |
|---|---|---|
| Radial amount/falloff, Center/Disc/Points, Inner/Outer | `docs/evidence/round8-radial-points-components.md`, `round8-radial.md`; `_tools/infantry_tables.py` emits `radial.rings` into `assets/data/infantry-hitboxes.json`; `pipelines/infantry-viewer.md` documents the rule and `assets/js/infantry-viewer.js` expands compact factors. | Present; checker covers the generated tables and decoder regression. |
| Projectile blast context and retained weapon/caliber tags | `docs/evidence/round8-radial.md`; `infantry_tables.py` builds projectile `source_context` and radial entries; JSON is rendered through the same viewer source model. | Present; no stale propagation found. |
| Six explosive actor defaults and detonation paths | `docs/evidence/round8-explosive-actors.md`; `assets/data/explosive-actors.json` is read by `infantry_tables.py`, which emits viewer source rows into `infantry-hitboxes.json`; viewer pipeline labels trigger and Molotov-patch limits. | Present; data and generator connection confirmed by source. |
| Armor-hook paths, including general hook and melee's discarded return | `docs/evidence/round8-armor.md`, `round8-melee.md`; `_tools/infantry_tables.py` `verified()` publishes the bounded path statement and viewer source `why` text retains assumptions. | Present as documented/static behavior; final durability writes remain explicitly outside the claim. |
| Armor-table evaluation as a separate armor-target event | `docs/evidence/round8-armor.md`; `infantry_tables.py` separates armor-event explanation from health-event factors in viewer source metadata and the damage pipeline documentation. | Present; no claim that queued work equals final durability mutation. |
| Vehicle weapon-extension tag provenance | `docs/evidence/round8-weapon-context.md`; `infantry_tables.py` includes vehicle-extension weapon items; `pipelines/Wardogs_VehicleDamagePipeline_v1.md` and `infantry-viewer.md` carry the tag/context boundary. | Present; configured root and appended projectile context are distinguished. |
| Character melee amount, source/context, no-bone event and armor processing | `docs/evidence/round8-melee.md`; `infantry_tables.py` `melee_items()` and source construction publish `other-melee-*` rows in `infantry-hitboxes.json`. | Present; missing bone/location and ignored armor return are preserved in `why`/verified text. |
| Normal on-foot/seated back-blast source and formulas | `docs/evidence/round8-backblast.md`; `weapon_attributes.py` retains per-weapon back-blast data; `infantry_tables.py` emits foot/seated viewer rows; `infantry-viewer.md` lists the synthetic seated-hit boundary. | Present; self-damage is kept separate. |
| Occupant-damage start amounts, source tags and synthetic hits | `docs/evidence/round8-occupants.md`; `infantry_tables.py` emits the vehicle-occupant source rows and provenance in `infantry-hitboxes.json`. | Present; no bone/location remains explicit. |
| Normal player radial component set and Mutable association | `docs/evidence/round8-radial-mutable-topology.md`, `round8-radial-points-components.md`; `infantry_tables.py` `verified()` and viewer source explanations state per-component retention, normal one-mesh setup and conditions. | Present with the documented normal-setup and runtime-mutation limits. |
| `bExploding` expression/default and camera-projectile gate mutation | `docs/evidence/round8-exploding-gate.md`; `infantry_tables.py` emits the bounded static gate in its verified rows; `pipelines/infantry-viewer.md` carries it as a source limitation. | Present; traced mutation is scoped, not claimed exhaustive. |
| Actor-impact overlap/substep formula and four thrown defaults | `docs/evidence/round8-impact.md`; `infantry_tables.py` emits `other-actor-impact` plus thrown contact sources; matching JSON and viewer table preserve formula inputs and bypass boundary. | Present; passed the infantry checker. |
| Helmet compiled selection, native merge policy and normal mesh resolution | `docs/evidence/round8-helmet.md`; verified viewer model uses the selected physics asset/body mapping, while `infantry_tables.py` states conditional runtime parameters and default resolution in `verified()`. | Present; actual runtime parameters and later mutations remain conditional. |
| Tapered-capsule query construction | `docs/evidence/round8-tapered-query.md`; `pipelines/infantry-viewer.md` distinguishes authored tapered display from native mean-radius straight query capsule. | Present; approximation is explicit in the viewer. |
| Static character-mesh profile/config channel responses | `docs/evidence/round8-config.md`; `infantry_tables.py` reports the profile in verified rows and the viewer pipeline describes the static profile boundary. | Present; shape registration and later runtime changes are not inferred. |
| Physical-material penetration and later-hit effects | `docs/evidence/round8-physical-material-downstream.md`; `infantry_tables.py` and `infantry-hitboxes.json` preserve the bounded direct-health conclusion and its limitations; damage pipeline evidence links the downstream trace. | Present; no extra direct SurfaceType health scalar is claimed. |
| Named caliber loading associations | `docs/evidence/round8-weapon-context.md`; `weapon_attributes.py` consumes loaded item/projectile associations and emits `weapon-loadouts.json`; calculator UI uses `assets/js/loadout-eval.js`. | Present; current JS/Python parity passed after running in an external mirror with the source data tree hash restored. |

The 18th entry was excluded from this 17-entry integration audit. The subsequent
[underbarrel investigation](round9-underbarrel.md) establishes a scoped
unsupported disposition on the shipped M4/default-input path. Its data-only
viewer source remains flagged; no shot tag was fabricated. Broad MAAWS/live
parity and other unchecked Round-8 items remain outside these 17 closures.

## Gates run

- `python -I _tools/infantry_tables.py --check`: **962 passed, 0 mismatches**.
- `node _tools/infantry_viewer_check.js`: **42 rings and 132 armor factors passed**.
- `python -I _tools/check_links.py`: **0 broken links**.
- `node --check assets/js/infantry-viewer.js` and `node --check assets/js/loadout-eval.js`: both passed.
- `python -I _tools/weapon_attributes.py --check`: **1,752 passed, 0 mismatches** in an external mirror. The checker rewrites its vectors when Node is available, so no check was run against the repository copy. The mirror's data tree hash was verified equal to `git rev-parse HEAD:data` (`a93c4f5d6bfc85e4230e3135edc19329e2c32669`); regenerated JSON matched the repository JSON after CRLF normalization.

`python -I _tools/infantry_regen_check.py` subsequently passed its one regression
test: a mocked later child failure preserves diagnostics and existing outputs.
This does not exercise ordinary multi-process regeneration or resolve its
documented intermittent Python child-process crash.

This audit initially inspected the existing integration surfaces without editing
them. The continuation updates the bounded underbarrel wording in its generator,
generated metadata, viewer documentation and research register.
