---
title: Gepard authored blast sampling in the viewer
nav_exclude: true
---

# Gepard authored blast sampling in the viewer

The Gepard viewer now uses its **89 authored damage-query sockets** across five static components, replacing its sampled display-surface targets. The three SPW variants keep their authored bounds fallback. Other models retain the display-surface approximation; the [roster census](round8-vehicle-sampling-census.md) records which additional source inputs are available.

This improves reference-pose candidate sampling. It does not establish parity with the game's registered collision bodies, skeletal chassis participation, moving parts, scene occluders or overlap ordering. Visibility still uses the published triangle geometry.

## Source inputs and placement

The fixture is `_tools/vehicle-impact-sampling.json`. Its Gepard entry binds the exact published GLB SHA-256, node/component/module/fragment identity, source render mesh and each raw StaticMesh dump hash. Model-level evidence pins the source reference transforms and the fresh all-vehicle socket manifest.

| Component | Matching sockets |
|---|---:|
| MainBody | 59 |
| TurretSpin | 14 |
| TurretPitch | 10 |
| Barrel_L | 3 |
| Barrel_R | 3 |
| Total | 89 |

Each socket's mesh-local RelativeLocation is transformed by its source component's reference-pose matrix in Unreal centimetres, then converted to display metres as `(-Y, Z, X) / 100`. Component bounds origins are transformed separately for the angle gate. Quantized GLB node matrices are not used to place these native inputs. The generator verifies the matching socket count against the raw mesh's socket references and refuses incomplete or mismatched model coverage.

## Candidate acceptance

The tracked native branch sorts candidates by distance from the original blast origin, tries cloud starts in order for each candidate, and continues across candidates after an acceptance. It retains the nearest accepted impact for that component (`0x6EF70D0`, continuation `0x6EF7950`). The preview now implements that continuation for authored points. The first successful cloud start ends that candidate's search; it does not end the whole component search.

The previously recovered 10-degree component-bounds angle gate, shared tested/blocked pretrace cache, cloud-index-1 exemption, original-origin radius/falloff and actor-plus-location-tag deduplication remain in use. The [SPW report](round8-spw-collision-inputs.md) records their source boundaries and detonation backoff.

A regression uses a front centreline shot at display height 1 m with 12.7 cm MAAWS detonation backoff. Keeping only the first accepted candidate gives approximately 31.8 cm for MainBody and 193.7 cm for TurretSpin. Continuing to the nearest accepted hit gives approximately **10.76 cm and 173.88 cm** respectively. These are distances from the blast origin to accepted contacts, not projectile travel distances. Both remain inside MAAWS's inner radius in this fixture; the distinction still matters for contact placement and falloff in other configurations.

The front MAAWS fixture retains five exposed MainBody-tag contacts, deduplicated into **one application**, with **267.9 main damage and 14.1 FuelTank damage routed from Main**. No physical FuelTank surface contact is accepted. The browser displays rounded main damage of 268 and identifies the authored socket sampling mode.

## Validation and restart

- Generator: 36 models, zero unresolved component mappings; only the Gepard model's generated metadata changed.
- All 36 model variants: 312 MAAWS placements and 62 fresh/out-of-range checks passed; 339 section-routing cases passed.
- Gepard: all 22 explosive sources, 198 placements passed, including native-socket coverage and nearest-contact regressions.
- Browser: Gepard's authored mode and routed fuel loss, three SPW front shots, all 23 vehicle legends and 154 routing panels, 30 mm controls, middle-button handling and 360-pixel layout passed.
- Source audit: all 33 source variants checked, zero export mismatches. Unsupported FWG source data and existing geometry omissions remain explicit.

Reports remain under `E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019`:

| Artifact | Purpose |
|---|---|
| `gepard-reference-inputs.json` | Source matrices and reference bounds; SHA-256 `1245052a39bbd904e9beef415c597504e4210f9581cd4fc7246c4f310d6b37e1` |
| `gepard_socket_probe.js`, `gepard-socket-probe.json` | Independent conditional socket/query reconstruction against decoded cooked triangles |
| `all-vehicle-authored-gepard-84mm.json` | All-model MAAWS regression results |
| `source-audit-authored-gepard.json` | Source/export comparisons |
| `browser-authored-gepard/` harness run | Browser interaction and label checks |

The browser harness serves local assets with deployed theme CSS; the publication build is a separate check. No game process or service was run. Damage factors were not adjusted to fit observed rocket counts, and the remaining SPW low-shot radar contacts are not closed by this Gepard change.
