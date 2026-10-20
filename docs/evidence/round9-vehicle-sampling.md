---
title: Round 9 vehicle sampling coverage
nav_exclude: true
---

# Authored sampling across 18 vehicle models

Offline CL-516586 continuation, verified 2026-10-20. The viewer now uses
authored socket/bounds candidates for **18 of 36 physical models**, up from
four. This includes all seven published tracked models, six rotary models and
five stationary models. The original SPW/Gepard fixture entries are unchanged.
The [Round 9 register](../ROUND9_STATUS.md) separates this coverage from
unresolved native scene-query parity.

## Inputs and native policy

Fresh exports cover 121 static assets and 35 skeletal meshes with zero failed
loads. Exact `DamageQuerySocket` FName forms, including numbered instances,
produce candidates; decorative or differently prefixed socket names do not.
The integrated fixture has **88 represented components, 727 socket points
and 45 bounds fallback points**. Components with authored matching sockets
cannot silently use a zero-socket bounds fallback.

Source placement uses fresh reference bones/sockets, serialized component
transforms and raw render-mesh ExtendedBounds/socket locations. It does not
derive candidate points from compressed GLB node matrices. Reference-matrix
exports round to five decimal places in glTF units; this is source export
precision, not exact native floating-point reconstruction. All 204 source
node/variant bounds checks agree with the published pose within 0.573 mm.
Shared model variants have identical source rows, bounds and points.

The native vehicle interface policy was checked for tracked, rotary, wheeled,
stationary, loudspeaker and airplane families. The Points routine calls
`IWDDamageable +0x50` at `0x6EFDA24–0x6EFDA2B`; the inspected family tables
select `0xD356F0` (`mov al,1; ret`). This continues candidate traversal while
retaining the nearest accepted hit. The separate `+0x48` hook returns false
and controls first-actor-hit collapse; those flags must not be conflated.
Each candidate's cloud-start search still stops at its first successful start.

Artillery, Heavy and T-72 initially had an ambiguous tag/fragment-name join.
The native attach-query constructor `0x50E09B0` writes mode 1 (ComponentTag),
with Explicit socket mode. Static and skeletal component settings construct
that query through `0x50E0B90`. Resolver `0x50EBDE0` calls
`ComponentHasTag` (`0x3CA1660`) for that mode; the latter compares ComponentTags
at `+0x70/+0x78`, not fragment keys. The real turret skeleton is tagged
TurretSkeleton; the mounted gun's similarly named fragment is tagged
MountedMachineGun. Unique native tag matching resolves the three placements
without modifying the published models or choosing an arbitrary first parent.

The generator accepts complete additional published models, verifies source
and GLB hashes, exact component identity and matching raw socket counts, and
rejects partial model sampling. Eighteen models containing instanced wheels
remain on the display sampler: aggregate component bounds, instance/Item
filters and same-component retention need their own derivation. Several
visible wheels must not be treated as independent native components.

## T-72 rear-engine and splash reports

The user's rear-engine report reproduces with authored T-72 points. At
display impact `(0, 1.2, -3.554555)` m and MAAWS backoff 12.7 cm, a straight
trace from the detonation to either upper contact hits the engine first.
The accepted upper traces instead start at cloud index 1, **50 cm above**
the detonation. Native `0x6F0341D` exempts this index from the origin-to-start
pretrace. The preview finds three contacts but only two unique damage tags:
Engine and MainBody. The two upper MainBody contacts do not both apply damage.
The reference result is 636.2625 main-health loss; this is not an in-game
measurement or proof that the collision acceptance is correct.

The MAAWS scalar itself is full base amount 100 through 4 m, then linear to
zero at 10 m: 83.3333 at 5 m, 50 at 7 m and 16.6667 at 9 m. The existing
native trace also selects different Inner/Outer damage-rule factors. Distance
is from the original detonation to the accepted contact, not the alternate
trace start or vehicle centre. The [radial trace](round8-radial.md#amount-radius-tag-and-distance)
records the exact formula and instruction range.

A controlled rear-ground comparison reproduces increasing total damage:
318.13125 main loss near the hull versus 443.40606 at a point 4 m farther
back. The near shot accepts only Engine; the farther shot additionally
accepts MainBody. Each contact's amount follows the decreasing scalar, but
the extra application raises the total. Authored points alone do not remove
this result. **Contact/occlusion parity remains open.** Do not label this a
falloff fix or force total splash damage below every direct-hit result.

## Verification and restart

- All-model MAAWS: 36 models, 204 nodes, 156,447 triangles, 312 catalog shots
  and 62 fresh/out-of-range checks passed with the final 18-model fixture.
- All 22 explosive sources: 6,864 shots passed with the first 15-model fixture;
  the final three additions were then covered by a 704-shot all-source tracked
  check. The unchanged Gepard is included in that targeted rerun.
- Routing: all 23 profiles and 339 fresh section applications passed.
- Source audit: 33 variants, 154 unique slots, zero mismatches.
- Installed Edge harness: all 23 profile legends, 154 routing descriptions,
  Gepard/SPW checks, 30 mm, middle mouse and 360 px checks passed. It uses
  deployed theme CSS with local assets, not a full local Jekyll build.

Artifacts remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round9_vehicle_sampling_20261019/`.
`final-summary-v2.json` is the restart index. No game, server, debugger session
or analysis database was opened. Root independently rechecked the native
family table targets and eight attachment functions against executable bytes.

| Artifact | SHA-256 |
|---|---|
| `candidate-sampling-fixture-v2.json` | `93b6d9172d72c0b2a9512704f4918dc5a6b7a4879319e6e7e4e774606c1cb4ba` |
| `native-family-sampling-policy-v1.json` | `a28e5d550513e6055a2974f9501f129ad661a7428208eeb2425af22fcc7a9401` |
| `native-attachment-source-policy-v1.json` | `3a7ca721261ffc2547e58d65e8db675756ed4cb1295cc2b269e67891f97e77f3` |
| `source-pose-bounds-check-v2.json` | `e505152dad65ed80c8af65827c7276f4a8aaf255be3a70bffea8e0ad9e164a55` |

Reports: `all-source-preview-check-v1.json`,
`new-tracked-all-source-check-v2.json`, `all-model-maaws-check-v2.json`,
`source-audit-v1.json`, `browser-v2/`, `root-attachment-byte-review-v1.json`,
`t72-trace-review-v1.json`, `t72-trace-review-v2.json`,
`t72-falloff-review-v1.json` and `t72-falloff-review-v2.json`.

Published triangles still approximate overlap and complex Visibility traces.
Missing bodies, collision flags, Item filtering, terrain, active/deployed state,
pose and native overlap order can change accepted contacts and the first
section. Neither source-pose agreement nor these software checks establishes
live numerical parity or future-build support.
