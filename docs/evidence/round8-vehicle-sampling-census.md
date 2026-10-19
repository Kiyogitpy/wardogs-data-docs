---
title: Vehicle blast sampling input census
nav_exclude: true
---

# Vehicle blast sampling input census

A fresh offline pass loaded **all 121 distinct static-mesh package references** selected by the 33 exported vehicle variants, including six assets used only by destroyed wheels. The final pass has **zero failed package loads**. Across those assets it found 802 sockets matching the traced damage-query name. Twenty-three variants reference at least one matching socket, nine have none, and `FWG_01_Default` has no static components in this assembly census. These are input-availability results, not verified in-game damage results.

The source enumeration uses `damage_tables.variants()` and `assemble()`, `vehicle_models.components()`, and both intact and destroyed `wheel_components()` states. It includes enabled module static fragments and destructible static entries, including entries that are not registered for damage. Therefore a socket being present does not prove that its component participates in a particular blast. Skeletal chassis bodies, active profiles, attachment transforms, overlap ordering and pose require separate checks.

## Exact matching and failed-load handling

The recovered sampler compares the `DamageQuerySocket` FName comparison index; numeric name suffixes remain eligible. This census uses full-string `DamageQuerySocket(?:_[0-9]+)?`. Of 818 exported socket records, 802 match. The other 16 include eight `DamageQuerySocket_Wheel`/`DamageQuerySocket_Wheel_1` records, plus muzzle, attachment, turret and seat sockets. A shared prefix does not make those names match the recovered comparison index.

The existing mesh exporter reads sockets before skipping an input that lacks an exportable collision mesh. Eighteen such successful skips therefore still supply socket evidence. In contrast, a failed package load never establishes zero sockets. The first attempt used unresolved mount paths and failed; a second attempt exposed three case-sensitive STN_01 paths. The successful final pass uses exact mounted paths returned by `list AA_`, changing only `ComplexPRoxy` to the observed `ComplexProxy`. All failed attempts remain preserved separately.

## Every source variant

Static assets and socket counts are counted once per distinct reference within each variant, across the included wheel states. Shared assets recur across variants; these table totals are not unique global totals or a count of runtime blast applications. A variant with sockets can also contain components requiring the bounds fallback.

| Variant | Distinct static assets | Matching sockets | Result |
|---|---:|---:|---|
| `FWG_01_Default` | 0 | 0 | No static components |
| `Attack_ROT_02` | 12 | 21 | Sockets present |
| `ROT_03_Default` | 8 | 16 | Sockets present |
| `ROT_03_MachineGuns` | 10 | 16 | Sockets present |
| `ROT_03_RocketPods` | 11 | 16 | Sockets present |
| `ROT_04_Default` | 8 | 114 | Sockets present |
| `ROT_04_MountedMachineGuns` | 8 | 114 | Sockets present |
| `SPW_01` | 9 | 0 | No matching sockets |
| `SPW_02` | 7 | 0 | No matching sockets |
| `SPW_03` | 8 | 0 | No matching sockets |
| `STN_01` | 3 | 0 | No matching sockets |
| `STN_02` | 3 | 0 | No matching sockets |
| `STN_03` | 2 | 0 | No matching sockets |
| `STN_04` | 1 | 0 | No matching sockets |
| `STN_05` | 1 | 0 | No matching sockets |
| `STN_06` | 4 | 0 | No matching sockets |
| `TNK_01_AntiAir` | 5 | 89 | Sockets present |
| `TNK_01_Artillery` | 6 | 96 | Sockets present |
| `TNK_01_Heavy` | 7 | 98 | Sockets present |
| `TNK_04` | 4 | 147 | Sockets present |
| `WHL_01_Default` | 3 | 7 | Sockets present |
| `WHL_02_Default` | 3 | 24 | Sockets present |
| `WHL_02_Pickup` | 3 | 22 | Sockets present |
| `WHL_02_SUV_RingTurret` | 6 | 24 | Sockets present |
| `WHL_05_Humvee_Default` | 3 | 26 | Sockets present |
| `WHL_05_Humvee_RingMinigun` | 4 | 25 | Sockets present |
| `WHL_05_Humvee_RingTurret` | 4 | 25 | Sockets present |
| `WHL_06_DuneBuggy_Default` | 3 | 19 | Sockets present |
| `WHL_07_Battle` | 9 | 8 | Sockets present |
| `WHL_07_Default` | 6 | 8 | Sockets present |
| `WHL_07_ArmouredBattle` | 12 | 8 | Sockets present |
| `WHL_08_Default` | 3 | 33 | Sockets present |
| `WHL_08_RingTurret` | 5 | 33 | Sockets present |

## What reaches the viewer

The [SPW continuation](round8-spw-collision-inputs.md) implements authored bounds candidates for the three SPW models. The [Gepard continuation](round8-gepard-sampling-viewer.md) adds its 89 placed damage-query sockets. Other models still use sampled display surfaces. The new census makes additional authored inputs available for placement and sampler verification; it does not silently enable unverified socket coordinates or declare the other vehicles accurate.

The next implementation needs to place matching mesh-local sockets using source reference transforms, retain component bounds for the native angle gate, and select the nearest accepted hit after the per-candidate cloud traces. Each supported model must have complete, identity-bound inputs. Query filtering, registered scene bodies and actual component order remain separate from the candidate coordinates.

## Restart and provenance

All detailed reports, raw exports and diagnostic scripts remain outside the repository under:

`E:/Reverse_Engineer/wardogs_analysis/round8_all_vehicle_static_sampling_20261019`

| Artifact | SHA-256 |
|---|---|
| `socket_availability_result_v3.json` | `ae4781d49162758e2e80590af9067c2b041767290339e958b7f3006aa2cf8bac` |
| `source_census_v2.json` | `69e454aab6602ce8158533fdb46f63fbfb5003ec2304966f3515a48c3e07e409` |
| `render-static-full-inputs-v3.txt` | `cbfd68a5f524562a9a147ec8805dc22c472afe34cea9369579c3a5a9d099963a` |
| `mesh-v3/manifest.json` | `c241980da36b0b23a73a83aa7619499a2475e2126e7ce677672d780d9bb97096` |
| `mesh-v3/_failures.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The input census and export were independently checked against these hashes, all 121 asset records, the 33 variant classifications and the socket-name filter. The exporter is the existing CL-516586 investigation build at `round8_gepard_explosive_collision_20261019/tool-artifacts/bin/WdExtract/debug/WdExtract.exe`; the key was supplied only by its file path. No target process, game service or IDA database was opened. This pass does not establish support for a future asset build.
