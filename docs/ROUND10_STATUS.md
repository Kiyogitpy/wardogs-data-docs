---
title: Round 10 status
nav_exclude: true
---

# All-vehicle explosive continuation

The [Round 11 continuation](ROUND11_STATUS.md) acquires collision resources
across all variant assemblies and corrects equal-distance actor-hit sorting.
Native scene-query parity remains open.

Checkpoint: 2026-10-20, starting from `51559177`. The user's instruction was to
extend the T-72 contact, occlusion and falloff review across every vehicle and
explosive type. This pass covers all **36 published models and 22 exported
explosive sources**. It does not close the entire project backlog.

| Track | Result |
|---|---|
| Authored sampling | 36/36 models; 204 nodes; 1,131 socket targets and 143 bounds targets |
| Shared instanced wheels | 78 instances in 18 native components; per-instance points/Item identity and aggregate angle bounds recovered |
| Points cloud gate | Corrected fixed 10 degrees to native 90/180 bounds-sphere policy |
| Contact order | Per-target gathering, actor float-distance sort, native component swap filter, then hit-location tag dedup |
| Explosive defaults | All 22 LOS/preference settings traced; nine prior false choices corrected |
| Broad verification | 28,600 direct/splash scenarios; 2,364 query comparisons; 6,864 existing shot contracts; 339 routing cases |
| Native scene-query parity | Open: displayed geometry, overlap/filter state, poses, terrain, equal-distance ordering and partial wheel remapping remain estimates |

The [integration audit](evidence/round10-vehicle-blast-audit.md) explains why
some farther blasts can still do more damage: authored radius factors,
different contacts and depletion-conditioned routing all contribute. No
universal direct-hit-versus-splash clamp was added. The
[native sampling proof](evidence/round10-native-vehicle-sampling.md) supersedes
the earlier 10-degree/per-component-minimum/GLB-order assumptions.

Reproduce with new external output paths:

```powershell
python -I _tools/vehicle_impact_metadata.py
node _tools/vehicle_blast_audit.js --report '<new-audit.json>'
node _tools/vehicle_impact_check.js --report '<new-contracts.json>'
python -I _tools/vehicle_data_audit.py --expect-variants 33 --report '<new-source-audit.json>'
python -I _tools/vehicle_impact_browser_check.py --out '<new-browser-directory>' --no-screenshots
```

Generator inputs are local hash-bound evidence; the restart recipes live in
`E:/Reverse_Engineer/wardogs_analysis/round10_vehicle_ism_20261020/README.md`.
The broad audit records source hashes and refuses existing report outputs.
STN_05 remains geometry-less; FWG remains unsupported. Molotov sustained fire
is excluded from point-detonation estimates. Existing extractor changes,
`_tools/content.md` and `graphify-out/` stay outside this publication batch.
