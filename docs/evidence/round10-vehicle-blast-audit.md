---
title: Round 10 all-vehicle explosive audit
nav_exclude: true
---

# All vehicles and explosive sources

Verified offline on 2026-10-20 against frozen CL-516586. The viewer now uses
complete authored sampling inputs for **36/36 published physical models**
and verified trace preferences for **22/22 explosive sources**: 16 projectile
calibers and six thrown/placed explosives. This corrects shared sampling and
contact-selection errors; it does not establish live collision parity.

The [native sampling report](round10-native-vehicle-sampling.md) supplies the
instruction-level proof. The [coverage summary](round10-vehicle-blast-coverage.json)
records each model/source sweep, input hashes and the remaining exclusions.
The [active checkpoint](../ROUND10_STATUS.md) records scope and restart steps.

## Corrected shared behavior

| Previous behavior | Corrected reference model |
|---|---|
| Eighteen instanced-wheel models used display-surface targets | All 36 models have complete hash-bound authored inputs. Per-instance wheel targets retain Item identity; 78 instances still belong to 18 shared native components. |
| Fixed 10-degree cloud-angle threshold | Default Points uses 90 degrees outside the component bounds sphere and 180 inside. The first two cloud indices are angle-exempt. |
| Selected each component's independently nearest accepted contact | Gather per-target accepted hits, sort the actor array by float Distance, apply native swap-removal of duplicate components, then deduplicate nonempty hit-location tags. |
| First section followed GLB component order | The first filtered actor hit is distance-derived; equal-distance order and live scene-query membership remain uncertain. |
| Eleven omitted trace preferences were unknown and simulated false | Native defaults plus cooked overrides resolve all 22 preferences: nine true and thirteen false. Nine previous simulation choices change. |

Every sampled target still tries the native cloud starts in order, with its
first successful start ending that target's search. Origin-to-start traces
share their tested/blocked cache. **Cloud index 1 remains exempt from that
pretrace**; it is the raised start for preference=false and the original
origin for preference=true. Removing the exemption to force an occlusion
outcome would contradict the traced code. Other vehicle components cannot
count as the requested component: all six reviewed vehicle families disable
the same-owner acceptance shortcut.
The superseded surface/corner sampler is removed; missing or partial authored
inputs now stop estimation instead of selecting a fallback model.

## Explosive settings and falloff

The projectile default is established through `UWDProjectileData` constructor
`0x6BB97B0` → stats constructor `0x699DEE0`; instruction `0x699DF4A` writes
both LOS/preference bytes true. The generator applies that inherited default
only to the verified export class; explicit cooked values win.

Actor DamageValues constructor `0x6BB9850` writes those bytes true at
`0x6BB9888`. C4 explicitly overrides preference false and IED inherits C4.
Frag, AT mine, Claymore and Molotov retain true. Five artillery projectile
records also inherit true; the other eleven projectiles explicitly use false.
Caller `0x6F00B96` reads the actual preference and forwards it to cloud builder
`0x6EF63C0`. All 22 reviewed sources have LOS enabled and share the default
global Points selector; these are not separate per-weapon occlusion modes.

Raw falloff agrees with the [native piecewise formula](round8-radial.md#amount-radius-tag-and-distance).
MAAWS stays at base amount through 4 m, then decreases linearly to zero at
10 m. Other sources have different slopes and minimum floors. The unusual
122 mm Havoc record has EffectiveRadius 600 cm greater than Radius 300 cm;
the native effective-radius branch takes priority, and overlap/accepted-hit
range still bounds which contacts exist. Do not normalize its authored data.

**Total main-health damage need not decrease with blast distance.** The sweep
distinguishes additional/lost accepted locations, a changed first section,
changed rule factors, a different accepted contact and changed routing phases.
There are **114 exported 40 mm factor pairs where Outer exceeds Inner**; for example,
SPW 40 mm uses `[0.24, 1.2]`. A falling raw amount can therefore cross into a
higher final rule factor. That behavior must not be “fixed” by clamping splash
below direct-hit damage.

A separate Ural/Claymore case holds its application locations and first
section fixed yet rises from 39.80185 to 41.70760 main loss. Its wheel has
75 HP, Pre 25% while alive and Post 25% when depleted. The nearer sequence
depletes the wheel on its second application, so the third takes only Post.
The farther sequence leaves 3.19433 HP: the third takes Pre, consumes that
remainder and then takes Post. Independent sequential arithmetic reproduces
both totals. This is a routing-phase consequence, not increasing raw falloff.

## Verification

- Broad direct/splash sweep: **28,600 scenarios**, 36 models × all 22 sources,
  with four approach sides, two heights and ground placements spanning the
  effective/outer radii where the model supplies a surface anchor.
- **2,364 indexed-versus-original geometry queries** agree on triangle,
  position and distance. The offline spatial index reuses the viewer's exact
  triangle routines; it does not substitute native physics or change the UI's
  collision geometry.
- Existing contracts: **6,864 catalog shots**, 62 fresh/out-of-range checks and
  **339 fresh section applications** pass. New regressions cover the 90/180
  gate, actor sort/swap behavior, unique native wheel components and all 22
  source preferences. The former per-component-minimum Gepard regression was
  corrected to the native swap-filter order.
- Source audit: 33 variants, 154 distinct slots, zero mismatches. Browser:
  23 profile legends, 154 routing descriptions, Gepard/SPW routing, 30 mm,
  middle mouse and desktop/mobile checks pass.

The final broad sweep has **1,089 outward damage increases**. Each has an
identified reference-model contact/rule/routing change; none is flagged as an
unexplained scalar/routing increase. These are diagnostic observations, not
1,089 game bugs or proof that every contact matches the game.

Reports and native evidence remain outside the checkout:
`round10_vehicle_blast_audit_20261020/`, `round10_vehicle_ism_20261020/`,
`round10_los_audit_20261020/` and `round10_arithmetic_audit_20261020/` under
`E:/Reverse_Engineer/wardogs_analysis/`. The broad report includes exact input
hashes. Root rechecked all 21 raw native-policy spans; independent review
matched all 204 emitted sampling records to the fixture.

## Remaining boundaries

STN_05 has damage/routing data but no published collision geometry, so it
cannot receive an impact sweep. FWG has no established health/slot definition
and remains unsupported. Those exceptions are recorded rather than counted as
geometry passes. Missing registered bodies, live collision flags, terrain,
moving/deployed poses, backface/initial-overlap semantics and equal-distance
sorting can still alter contacts. Partial tyre destruction/remapping is not
modeled; wheel fixtures describe homogeneous intact or all-destroyed states.

Actor-source placement selects a **detonation centre**, not a physical actor
spawn or trigger simulation. AT mine's authored 50 cm upward explosion offset
must not be applied a second time to an already selected detonation centre.
Molotov here covers only the initial burst; sustained fire is a separate path.
No game process, server, debugger session or IDA database was opened.
