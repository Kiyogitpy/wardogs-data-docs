---
title: Spawn vehicle collision sampling inputs
nav_exclude: true
---

# Spawn vehicle collision sampling inputs

Fresh offline exports cover the SPW_01, SPW_02 and SPW_03 source assemblies, all 20 unique render static meshes, their 19 complex-collision meshes, four skeletal meshes and two shared skeleton packages. No static-mesh sockets were observed in the fresh pass. The radar render meshes have very small authored bounds despite their much larger displayed CC geometry. These facts provide inputs for testing native damage candidate sampling; they do not establish an explosion damage result or justify substituting a new gameplay model without further checks.

Exported geometry, cooked payloads and detailed acquisition metadata remain outside this repository at:

`E:/Reverse_Engineer/wardogs_analysis/round8_spw_explosive_20261019`

## Acquisition and coverage

| Output under the evidence root | Scope and result |
|---|---|
| `dump-v2/`, `inputs-v2.txt`, `dump-v2.log` | 44 packages, 44 successful, zero failed |
| `dump-followup/`, `followup-inputs.txt`, `dump-followup.log` | Six Lonestar CC packages discovered from fresh render-mesh references, six successful, zero failed |
| `dump-skeletons/`, `skeleton-package-inputs.txt`, `dump-skeletons.log` | Two distinct skeleton packages, two successful, zero failed |
| `socket-mesh/manifest.json`, `render-static-full-inputs.txt`, `socket-mesh.log` | All 20 render static meshes inspected; 19 CC meshes exported, interior skipped for lacking a CC reference, zero failures, zero positive static socket entries |
| `skeleton-mesh/manifest.json`, `skeleton-inputs.txt`, `skeleton-mesh.log` | Four skeletal meshes; reference bones and resolved mesh/skeleton sockets; zero failures |
| `cooked-v1/collision.json`, `collision-inputs.txt`, `collision-v1.log` | All 39 render/CC static meshes; 39 BodySetups, 39 cooked payloads, zero skipped, zero failed |
| `source-assemblies.json` | Enabled source-fragment mesh rows for all three assembled variants, including complete serialized row properties |
| `sampling-inputs.json` | Compact per-variant module/fragment/child identity, attachments, transforms, collision settings and property presence; all 39 static bounds/body flags/AggGeom counts/payload references |

The 39 cooked payloads total 1,622,914 bytes and have 39 distinct SHA-256 values. Their internal Chaos layout has **not** been decoded or validated by this acquisition task. Gepard decoder support must not be assumed to extend to these resources.

The preserved first attempt in `dump/` and `dump.log` used short mounted asset paths and reported ten successful and 34 failed packages. The corrected inputs use full `Wardogs/.../Content/...` provider paths; `dump-v2/` is the successful replacement acquisition. No earlier files were overwritten. Across the successful dump directories, 52 distinct packages were exported.

## Source assemblies and exact mesh references

All three variants use platform `/SPW_01/Platforms/VP_SPW` and base static meshes `/SPW_01/StaticMeshes/SM_SPW_Body` and `/SPW_01/StaticMeshes/SM_SPW_Interior`. The body references `/SPW_01/ComplexCollision/CC_SPW`; the interior has no `ComplexCollisionMesh` property.

| Variant | Radar part | Unique radar render meshes | Static component occurrences |
|---|---|---:|---:|
| `/SPW_01/Variants/VV_SPW_01` | `/SPW_01/Parts/VP_SPW_Radar` | 7 | 15 |
| `/SPW_01/Variants/VV_SPW_02` | `/SPW_01/Parts/VP_SPW_Radar_Manticore` | 5 | 11 |
| `/SPW_01/Variants/VV_SPW_03` | `/SPW_01/Parts/VP_SPW_Radar_Lonestar` | 6 | 13 |

The 39 component occurrences include repeated use of the same mesh for ordinary and `.Deployed` destructible mesh tags, plus one interior occurrence per variant. They are source settings, not a count of simultaneously active runtime components. The assembly resolver found no missing source modules.

Each radar render mesh below has a fresh `ComplexCollisionMesh` reference to the same basename prefixed with `CC_`, in the same directory. Package input lists contain their full provider paths.

| Directory below `/SPW_01/ComplexCollision/` | Exact render mesh basenames |
|---|---|
| [`Valkyra/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Audio/Convo/Valkyra) | `SPW_01_Antenna`, `SPW_01_Base`, `SPW_01_Flap_01`, `SPW_01_Flap_02`, `SPW_01_Flap_03`, `SPW_01_Rotator`, `SPW_01_RotatorCore` |
| [`Manticore/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Manticore) | `SPW_02_Antenna`, `SPW_02_Base`, `SPW_02_Rotator_01`, `SPW_02_Rotator_02`, `SPW_02_Rotator_03` |
| [`Lonestar/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/PvE/Scenarios/BaseScenario/Content/AIConfigs/Lonestar) | `SPW_03_Antenna`, `SPW_03_Base`, `SPW_03_Flap_01`, `SPW_03_Flap_02`, `SPW_03_Rotator_01`, `SPW_03_Rotator_02` |

For example, the exact Lonestar antenna pair is `/SPW_01/ComplexCollision/Lonestar/SPW_03_Antenna` and `/SPW_01/ComplexCollision/Lonestar/CC_SPW_03_Antenna`. The static-mesh package files under `dump-v2/` and `dump-followup/` retain material slots, CC references and BodySetup metadata.

## Sockets, placement and authored settings

The older SPW_01/02 manifests contain `staticMeshSockets: {}`. That field alone was not treated as proof of absence. The fresh existing `MeshMode` inspected `UStaticMesh.Sockets` for every exact render static input and emitted no positive entries, with zero failures. All 39 successfully dumped SM/CC packages also contain no `StaticMeshSocket` exports. No `DamageQuery` socket was observed on the 20 render static meshes.

CUE4Parse's `UStaticMesh.WriteJson` does not emit its native `Sockets` array, so a dump's missing `Sockets` JSON field is not the socket-count evidence. The fresh mesh-mode pass is the direct accessor check. Its implementation only emits positive socket entries and filters unresolved/null socket objects; the accompanying absence of socket exports and clean failures file supports the zero-observed result. This report does not invent raw array counts that the exporter did not record.

The chassis skeletal mesh is `/SPW_01/SkeletalMeshes/SK_SPW_Base`. The three radar skeletal meshes are `/Game/Environment/Props/Military/Spawn_Boards/Radars/SK_SPW_01_Radar`, `SK_SPW_02_Radar` and `SK_SPW_03_Radar`. All radar meshes reference the same `/Game/Environment/Props/Military/Spawn_Boards/Radars/SKEL_SPW_Radar` skeleton, which has no socket exports. The chassis references `/Game/Vehicles/MasterSkeletons/SKEL_Treaded_Base`.

`dump-skeletons/SKEL_Treaded_Base.json` explicitly defines `body_RadarSocket` on `body_J`, with relative location UE centimetres `(7.423977, 0.000134, 194.99997)`; rotation is omitted. The fresh chassis entry in `skeleton-mesh/manifest.json` already resolves this under **`sockets`**, with `source: "skeleton"`, `boneFound: true`, component-space glTF translation approximately `(0, 2.46832, 0.07424)` metres and identity rotation. Looking only in that entry's `bones` array or only at mesh-owned socket exports misses it.

The body and interior attach to chassis `body_J`. Radar pieces use chassis `body_RadarSocket`, radar bones such as `root_J`, and `RadarDeployedPivot`; exact per-occurrence queries and relative transforms are retained in `sampling-inputs.json`. `MVF_DeployStateCollision` settings from each radar module are also retained there. The creation, pose and activation of `RadarDeployedPivot` remain unresolved; a stowed reference-pose fixture must not treat that component as an established identity transform.

The serialized settings distinguish the following cases:

| Component | Raw settings |
|---|---|
| Body | `MVCT_QueryProxy`; `Flags` omitted; complex-surface registration field omitted |
| Interior | `MVCT_QueryProxy`, explicit `Flags: 0`, `bHitEvents: false`, `bRegisterComplexSurface: false` |
| All 33 radar static occurrences | `MVCT_QueryProxy`, explicit `Flags: 3`, `bRegisterComplexSurface: true`; per-occurrence profile, attachment and physics-mode fields retained |
| Radar skeletal destructible entry | Explicit `MVCT_Profile`, `Profile: NoCollision`, `Flags: 3`, `bRegisterComplexSurface: false` |

The exact-build SDK `sdk/raw/ModularVehicles_structs.hpp:104` names collision flag positions `MVCF_Visible=0` and `MVCF_Damagable=1`; the stored settings field is a uint8 mask. Raw mask `3` must be distinguished from enum value `3`. This acquisition does not recover effective collision-channel responses, complex-trace masks, shape activation or constructor defaults for omitted properties. In particular, an omitted body mask is not recorded as zero. Interior exclusion from complex-surface registration also does not establish that it cannot occlude a different query.

## Bounds differences relevant to candidate sampling

All bounds below are local UE centimetres, before component placement. `cooked-v1/collision.json.staticMeshes` retains parsed `RenderData.Bounds`, explicitly serialized `ExtendedBounds`, and any explicitly present bounds extensions. Do not replace a render component's authored bounds with its CC display-mesh bounding box.

| Render asset | Explicit `ExtendedBounds.Origin` | `ExtendedBounds.BoxExtent` | Sphere radius |
|---|---|---|---:|
| `SM_SPW_Body` | `(5.454605, -0.00006866455, 111.40069)` | `(375.49048, 176.17606, 122.32296)` | 414.60734564832006 |
| `SM_SPW_Interior` | `(-0.85769653, 0.7534256, 100.671555)` | `(344.4237, 146.38385, 98.05881)` | 373.1614266239759 |
| Every one of the 18 unique radar render meshes | Origin field omitted in the serialized struct | `(5.97278, 5.97278, 0.0000009730894)` | 8.446786803032293 |

The omitted radar origin is preserved as absent in the raw metadata, rather than silently inserted by this report. Resolving the struct's zero origin for a fixture is a separate, explicit default interpretation. The radar bounds are nearly planar and about 12 centimetres across, radically smaller than the displayed radar collision surfaces. Bounds-origin candidate points can therefore differ substantially from a nearest-surface or CC-corner sampling proxy, even when the visible collision model is correctly assembled.

The render body also differs between bound sources: `RenderData.Bounds.Origin` is `(6.627365, -1.6878204, 109.32597)` and its extent is `(379.5185, 178.01015, 125.795364)`. Neither is identical to its authored `ExtendedBounds` above.

The `CC_SPW` asset has parsed zero origin/extent in both bound sources, while its explicitly serialized `ExtendedBounds.SphereRadius` is approximately `1.0514644122014444e21`. This unusual raw value must not be substituted for the render body's bounds or interpreted as an established runtime radius. SM body and CC body each have one authored convex element and 357,480-byte cooked payloads, but their payload hashes differ; equal size is not a geometry-equivalence check.

These are concrete candidate differences to test against the native bounds fallback. No damage amount, visibility outcome or first-section ordering was inferred from them. Appropriate follow-up fixtures must keep coordinate units, component transforms, incoming trace offsets, angle selection, complex pretraces and deployed state explicit.

## Reproduction and provenance

The executable used is `E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/tool-artifacts/bin/WdExtract/debug/WdExtract.exe`. It was not rebuilt during this acquisition. The target is the frozen Wardogs CL-516586 asset set; no game or server was run.

For a fresh destination, the successful command shape is:

```powershell
$spwTool = 'E:/Reverse_Engineer/wardogs_analysis/round8_gepard_explosive_collision_20261019/tool-artifacts/bin/WdExtract/debug/WdExtract.exe'
$spwPaks = 'E:/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks'
$spwMap = 'E:/Reverse_Engineer/wardogs_analysis/round8_propertybags_20261019/wardogs.recovered.usmap'
& $spwTool $spwPaks 'E:/WardogsConversion/CueDump/aes.txt' $spwMap '<new-output-directory>' "$spwPaks/oo2core_9_win64.dll" dump '<absolute-input-list>'
```

Use `inputs-v2.txt`, `followup-inputs.txt` or `skeleton-package-inputs.txt` for their respective dumps; `mesh` with `render-static-full-inputs.txt` or `skeleton-inputs.txt` for the two manifest passes; and `collision` with `collision-inputs.txt` for collision metadata and payload export. Use new directories: collision output refuses existing metadata/payload targets, while dump/mesh modes are not overwrite-safe. The key is consumed by the existing tool from the named path; its contents were neither inspected nor included in evidence.

| Artifact | SHA-256 |
|---|---|
| Executable | `c7df9e2d61b2b83b2d8ea3416cee6c4b2e9efded2cf4c93986bd33c47eed9e7f` |
| Recovered usmap | `277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380` |
| `cooked-v1/collision.json` | `83937717970a0e886cb470a70cb7233c75c4ecf0b43176cc53e511892f1ee613` |
| `socket-mesh/manifest.json` | `c1565150153e936f96e9d8f110d7caa9e6861b092ff163f5c2afce9264c34e63` |
| `skeleton-mesh/manifest.json` | `13a5e00f00f0b9be263ffec80aeff946cd44444877869f68dced41e50bb2c232` |
| `source-assemblies.json` | `61282828797ce52c52d3ca2a84dfc538a69c9dfb6bbaa18cb45a30b415737084` |
| `sampling-inputs.json` | `82bbd51e757bf7d3808b79ec248c989aed9108be0dcccfee3ddec92cd9db3ac3` |
| `dump-skeletons/SKEL_Treaded_Base.json` | `8c0edc63297e391c00d3a72ff1c9874f0b6a1959879ffc76aae9bceb17fe2ce9` |
| `dump-skeletons/SKEL_SPW_Radar.json` | `6c43e9a28f81a618b3a64c963347c94c8dbeaf11a1040695025655c6326f2e21` |

The compact JSON report also records hashes for the exact input lists. The acquisition itself did not change viewer behavior. The implementation continuation below consumes a compact, hash-bound sampling fixture; it does not claim game parity.

## Bounds-based viewer continuation

The viewer previously chose nearest displayed surfaces and CC-box corners as candidate targets. In a controlled front-body MAAWS shot that admitted both MainBody and Radar contacts, the two distinct location tags produced two applications to the first hit's Main section: **722 main damage and 38 routed FuelTank damage**. The extra application was not a second direct-hit event. Native downstream section selection remains the first component hit; changing every contact to its own section would contradict the traced branch.

Fresh no-socket evidence permits the native bounds-origin fallback for the three SPW models. `_tools/vehicle-impact-sampling.json` binds all **21 represented components (8/6/7)** to exact GLB hashes, source render meshes, placed bounds origins and source evidence hashes. Placement includes the chassis `body_RadarSocket` from the shared skeleton. Interior and unresolved deployed components are excluded. The generator requires complete model coverage and preserves the shared-variant comparison.

The initial SPW branch used one authored bounds point per represented component,
a 10-degree angle assumption, the shared tested/blocked cloud cache and exact
trace starts. The [Round 10 trace](round10-native-vehicle-sampling.md) corrects
that gate to 90/180 degrees and supplies actor sorting plus swap filtering.
Moving a start a small distance inside the hull can bypass a surface obstruction;
the authored branch does not apply that display-sampler offset. Visibility and
initial overlap still use published triangles; live scene bodies, Item state
and pose remain unresolved.

The armed projectile path separately backs the blast origin away from the impact by half the projectile length. In the frozen PE, `0x6B717C0` retains ImpactVelocity at deferred-record `+0x2E8`, `0x6B70F27` normalizes it, and `0x6B70F73`–`0x6B70FD3` calculates `ImpactPoint - 0.5 * Length * SafeNormal(ImpactVelocity)`. The generator now exports this distance for the 16 positive-radius projectile entries. MAAWS is **12.7 cm**. The viewer assumes the incoming direction runs from the current camera to the selected point, states that assumption beside the result, and centres the blast marker on the resulting detonation point. Placed explosive actors retain the selected point. This approximates a shot direction; it does not simulate projectile travel or arming time.

With the corrected candidates and an explicit front-to-back MAAWS direction at centreline display height 1 m, all three SPW variants retain one MainBody application: **361 main damage, 19 routed FuelTank damage, Radar still 100**. Browser clicks on all three models reproduce the same rounded main damage. These are fresh-health reference shots, not proof of in-game shots to destruction.

The user reports roughly **four MAAWS hits to the spawn vehicle main body**. The exported main health is 1,000; three ideal 361-damage shots would exhaust that pool, so this observation remains a parity gap. No four-shot calibration is applied.

Track involvement is a concrete conditional explanation. A side shot at display height 0.5 m selects Tracks.Left in all three reference models. With one 380-raw application, the fresh track absorbs 125; its radial simultaneous copy is disabled, and only 50% of the remaining 255 routes to Main. Main's 5% pre-route then sends 6.375 to FuelTank and leaves **121.125 main damage**. One such track-first shot followed by three fixed 380-raw main applications exhausts main health on shot four; it is still at 156.875 after shot three. These are routing examples, not evidence that a main-first explosion separately damages tracks. The native first-component section behavior still applies, and the visibly clicked material can differ from the accepted blast contact.

`root-track-routing-probe.json` records 48 reference placements across the three variants plus explicit repeated-routing examples. It also exposes a remaining limitation: some low front/rear shots on SPW_02/03 still accept a Radar application. These cases are not closed or relabeled as correct. Missing interior occluders, runtime pose, cooked query behavior and overlap order remain candidates for further work.

SPW's critical threshold of 100 and bleed-out timer of 15 seconds are a separate lifecycle lead. `critical-lifecycle-review.json` (SHA-256 `865757e649da37e1f5c1f0afd51b5ab1e76fa0e579e645a081a2de64defb80be`) binds the frozen PE and exact bytes for six functions. Authority Tick `0x7687980` checks the critical tag, pauses shortly after repair, decrements the configured countdown and calls `0x7674AE0` when expired. Repair `0x76888B0` clears the critical tag above the threshold. The forced-zero helper `0x53288B0` requires existing positive main health. The regular damage callback that enters critical state remains unresolved: no third-shot reset/clamp or fourth finishing-shot requirement is established.

Validation artifacts under the external root:

| Artifact | Result |
|---|---|
| `root-impact-offset-check.json` | 36 models, 204 nodes, 156,447 triangles; 312 MAAWS placement checks and 62 fresh/out-of-range checks passed; 339 section-routing checks passed |
| `root-spw-all-sources-offset.json` | All three SPW models, 22 explosive sources, 594 placements passed |
| `root-source-audit-offset.json` | All 33 source variants audited, zero export mismatches; FWG unsupported source and existing geometry omissions remain explicit |
| `browser-root-final/` harness run | All three SPW front clicks, detonation/impact labels, Gepard routed fuel regression, 23 vehicle legends, 154 slot routing panels, 30 mm controls and 360-pixel layout passed |

The browser harness serves local assets with deployed theme CSS; it does not replace a Jekyll build. Publication is recorded in Git history. The earlier viewer fixes were published as `bdf5d8a2`; publication and in-game accuracy are separate checks.

## Follow-up verification after `7a53decf`

The initial sampling and detonation changes were pushed as `7a53decf`; its GitHub Pages build and deployment passed. Further checks keep the low-hit contacts open:

- **Interior occlusion is not an eligible fix.** Adding the decoded interior removes several extra radar contacts in a conditional visibility probe. However, its authored QueryProxy flags are zero. Packed `DefaultGame.ini` lines 682–684 maps flag bit 0 to Visibility, Camera and GameTraceChannel1. Native `0x50E66C0` and `0x50E6950` set the configured channels to Block for a set flag and Ignore for an unset flag; `0x50E6BD0` applies this mask after the profile. Thus an interior Visibility blocker would contradict the recovered settings.
- **Triangle culling alone does not resolve the issue.** Nineteen CC meshes match their fresh GLBs, with 2,059 triangles opposite in winding after the coordinate reflection. Correctly transformed one-sided tests preserve or worsen several low-shot radar contacts. The body cooked payloads have a separately validated geometric prefix; their complete decoder runs stop at nonfinite UV data. No complete body-payload decode is claimed. The reproduced low-shot path uses cloud index 1, which starts 0.5 m above the blast and skips the origin-to-start pretrace. That start can lie inside the sloped hull. Missing chassis query geometry and runtime state remain open.
- **Load-time bounds replacement is unproved.** Native `0x44BE3F0` can rebuild ExtendedBounds from render data plus positive/negative extensions. The decoded StaticMesh PostLoad candidate `0x44CC530` has no direct call to it; the only other explicit caller in the indexed corpus is `0x8DC8940`, whose sequence resembles the different-build local Interchange import helper. Local UE PostLoad recomputation is editor-gated. This bounded check does not establish an unconditional shipping-load overwrite or exclude inlined/indirect mutations; it supplies no reason to replace the authored SPW bounds fixture.
- **Critical entry does not itself reset health.** The callback bound at `0x767BA46–6F` adds the critical tag when current Main health is at most the configured threshold. WD slot 162 calls base `0x532F730` at `0x6B8050E`. The base broadcasts the callback (`0x532F752–771`), reads current health (`0x532F79B–7BC`), and on nonpositive Main health continues through the depletion delegate and owner path (`0x532F7FA–82B` → `0x53D8E20`). Critical tag entry alone therefore does not establish a fourth finishing-shot requirement. Effective attribute modifiers and actual shot contacts remain separate uncertainties.

The contact counter now says **not reached**, because it includes candidates rejected by distance or angle as well as blocked traces. Calling every such result occluded implied a visibility test that might never have run. The browser harness rechecked all three SPW front hits and their labels, all 23 legends and 154 routing panels, Gepard fuel routing, 30 mm controls and the 360-pixel layout.

Restart artifacts under the external SPW evidence root:

| Artifact | SHA-256 |
|---|---|
| `low-hit-visibility-review-v1.json` | `d6af4e6407ed635c8bdd900b947531fa1fbba2cd2392839ba40ffafa23b5b8ba` |
| `root-bounds-lifecycle-review.json` | `d79491b99c9cdde6964edbdd772925754acea734518fe751de7f26090b8a4789` |
| `critical-entry-zero-review.md` | `9935fff87ceb699c597101b2b939794920276d1d6a1e9ac2d5318af12cee787b` |

The visibility report points to the interior and culling probe scripts, raw instruction checks, payload decoder and per-mesh comparisons. No damage factors or collision blockers were changed to fit the reported four-shot result.
