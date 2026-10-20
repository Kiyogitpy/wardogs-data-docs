---
title: Vehicle class and radial-hook coverage
nav_exclude: true
---

# CL-516586 vehicle class and radial-hook coverage

This is a static class/dispatch audit, not a collision or runtime parity test. The current `assets/data/vehicle-hitboxes.json` contains 23 display records and 32 variant names. Those variants use the 20 `ModularVehiclePlatform` exports under `data/Wardogs/Plugins/GameFeatures/Vehicles/`. One further exported platform, `data/Wardogs/Content/Vehicles/Platforms/Air/VP_FWG_01.json`, is outside that viewer catalog, bringing the inspected platform set to 21 and the typed variant set to 33. No boat or watercraft platform appears among these 21 exports; the audit therefore makes no claim about an unexported boat.

| Platform exports | Implementation class and native parent | Viewer variants |
| --- | --- | ---: |
| `VP_ROT_02`, `VP_ROT_03`, `VP_ROT_04` | `/Script/WDGame.WDRotaryVehicle` → `BHRotaryVehiclePawn` → `BHBaseVehiclePawn` | 6 |
| `VP_SPW` | `/SPW_01/Blueprints/B_SPW.B_SPW_C` → `WDTrackedVehicle` → `BHTrackedVehiclePawn` → `BHBaseVehiclePawn` | 3 |
| `VP_TNK_01_AntiAir`, `VP_TNK_01_Artillery`, `VP_TNK_01_Heavy`, `VP_TNK_04` | `/TNK_01/Blueprints/B_TNK_01.B_TNK_01_C` → `WDTrackedVehicle` → `BHTrackedVehiclePawn` → `BHBaseVehiclePawn` | 4 |
| `VP_STN_01`, `02`, `03`, `05`, `06` | `/Script/WDGame.WDStationaryVehicle` → `MStationaryVehicle` → `BHBaseVehiclePawn` | 5 |
| `VP_STN_04` | `/Script/STN_04.WDStationaryVehicle_Loudspeaker` → `WDStationaryVehicle` → `MStationaryVehicle` → `BHBaseVehiclePawn` | 1 |
| `VP_WHL_01`, `02`, `05`, `06_DuneBuggy`, `07`, `08` | `/Script/WDGame.WDWheeledVehiclePawn` → `MWheeledVehiclePawn` → `BHBaseVehiclePawn` | 13 |
| `VP_FWG_01` (outside viewer) | `/Game/Vehicles/Pawns/Air/Airplane/FWG_01/B_FWG_01.B_FWG_01_C` → `WDAirplaneVehicle` → `BHAirplaneVehiclePawn` → `BHBaseVehiclePawn` | 1 outside viewer |

`ImplementationClass` is at each platform JSON's first export, e.g. `VP_SPW.json:9–12`, `VP_TNK_01_AntiAir.json:9–12`, `VP_ROT_02.json:9–12`, `VP_WHL_02.json:9–12`, `VP_STN_04.json:9–12`, and `VP_FWG_01.json:9–12`. Inheritance is independently declared in `sdk/raw/WDGame_classes.hpp:9015,9161,13097,46853,61924`, `sdk/raw/Mechanized_classes.hpp:493,631,4595,4642,4721,4763`, `sdk/raw/STN_04_classes.hpp:20`, and `sdk/raw/B_SPW_classes.hpp:21`.

Cooked Blueprint verification from the owned CL-516586 paks: `B_SPW.json` has `SuperStruct=WDTrackedVehicle` and only one `Function` export (`OnRep_Faction`); `B_TNK_01.json` has the same super and no `Function` exports; `B_FWG_01.json` has `SuperStruct=WDAirplaneVehicle` and only `ExecuteUbergraph_B_FWG_01` and `ReceiveTick` Function exports. None declares a radial filter, `TakeDamage`, or radial damage override. These are bounded export observations: Blueprint event/tick side effects or data-selected components can still affect state. All three BP exports contain `WDVehicleDamageModelComponent` objects.

Fresh dump provenance: `E:/Reverse_Engineer/wardogs_analysis/round8_vehicle_class_audit_20261019/spw/B_SPW.json` SHA-256 `3cb23dfa6cb2446a699848ceb578c2f6ad8efb0a917a5ed57d74e2d5875cc82e`; `E:/Reverse_Engineer/wardogs_analysis/round8_gepard_audit_20261019/B_TNK_01.json` SHA-256 `8f219338b32ed83ef6af05b4813c256047810cc5aafde6dd4b0d6e8cade4f8f4`; `E:/Reverse_Engineer/wardogs_analysis/round8_vehicle_class_audit_20261019/B_FWG_01.json` SHA-256 `fc1e80b062026fd4ad82c04ec571e991933ca77c1081dd734a5d3f7b1788b3a1`. Dumped with existing WdExtract and the installed 32 mounted VFS; key passed by file path only. No target process was run.

Native dispatch check against read-only `decompiled_cl516586_20261017_mmvpuc__/corpus.sqlite` `aliases`: the radial target filter is the *same function RVA `6C2A790`* in every listed native class family (vtable slots tracked 373, rotary 376, wheeled 381, stationary/loudspeaker 372, airplane 373). The adjacent vtable entry is `1563050` in all of them. The damage dispatch entries are also identical across all six native families: vtable slot 214 `53D6530` (`TakeDamage` path) and slot 215 `3A9B0E0` (radial damage handler). The relevant inherited vehicle interface therefore has no observed class-specific native override at these entrypoints for these implementations. This does **not** establish identical final health: platform/part data select damage model sections, rules, routing and collision components, while physics overlap and LOS queries remain runtime-dependent. In particular, the generated viewer records have different routing arrays and radial-skip flags; do not replace those with one shared vehicle constant.
