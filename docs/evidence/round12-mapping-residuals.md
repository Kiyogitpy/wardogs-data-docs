---
title: Round 12 mapping residuals
nav_exclude: true
---

# Round 12: mapping residuals (53 unknown types, 2,690 hashed names)

Track 3 of round 12. It re-opens the two open items in
[ROUND8_STATUS](../ROUND8_STATUS.md) (extraction and maintenance) and
[WHAT_IS_LEFT](../WHAT_IS_LEFT.md) section 2.5, using only local, offline
inputs. No game run, no usmap committed, `data/` not re-exported. Labels:
**Data**, **Native**, **Derived**. Starting map: the verified final map of the
[property-bag recovery](round8-propertybag-types.md), 3,046,707 bytes, SHA-256
`277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380`
(`round8_propertybags_20261019/wardogs.recovered.usmap` in the analysis directory).

## Results

| Item | Before | Finding | After, if the lead applies it |
|---|---:|---|---:|
| Unknown element types | 53 in 36 owners | All 53 have one complete candidate type from a native `PCGSettings` layout (**Derived**, not hash-proven) | 0 |
| Hashed names | 2,690 | **45** occurrences, 18 tokens, proven from cooked Blueprint `ChildProperties` plus the token-length rule (**Data**) | 2,645 |
| `data/` keys renamed | | **0**: none of the 18 tokens occurs in `data/` | 0 |

The type fills are a lead decision. The name renames rest on the same kind of
evidence as the v2 pairing: a real name from the build's own data, the length
check against the token, and one token to one name.

## 1. The 53 unknown element types

Source of the candidates (**Derived**): the live map already types the native
PCG settings classes completely. A generated `PropertyBag_*` owner is built by
the native initializer `0x64982A0` from the fields of a `PCGSettings`
descendant, excluding `PCGSettings` itself (**Native**, see the
[property-bag evidence](round8-propertybag-types.md)). So the bag repeats the
class's ordered field list, and its array element types should equal the
class's.

Join rule used (each condition must hold):

1. The bag's ordered property names and static-array sizes equal one native
   class's fields. Order: the class's own fields first, then each super class
   up to, not including, `PCGSettings`. A class `MapProperty` may be dropped,
   because the native generator drops value-type-zero descriptors
   (`0x18136C1`-`0x1813755`).
2. Every already-typed bag slot agrees with that class (kind, struct, enum
   name, element types). Enum underlying width is ignored; the bag stores a
   byte, the class a wider integer.
3. All classes that match this way give the same element type for the slot.

Outcome: **36 of 36** owners match (35 directly; `PropertyBag_be19fd2c3e64390d`
after dropping `EnumValueToPinLabelMapping`, shared by `PCGSwitchSettings` and
`PCGMultiSelectSettings`). **53 of 53** slots get exactly one complete type; no
slot has disagreeing candidates. 47 slots have one matching class, 4 have two,
1 has three and 1 has six (the six share an inherited field and give the same
type). The `SoftObject` rows carry no target class, because the usmap has none.

Why this is not marked proven:

- The earlier descriptor-hash joins (native class candidates, serialized
  `PCGGraph`, `PCGGraphInstance`, `DefaultValues.PropertyBag`) matched none of
  the 36 owners, so there is **no hash-level owner binding**. The native bag
  pointer is transient; its hash need not match a serialized bag.
- **No typed-array control exists.** Across the other bag owners, 135 match a
  class layout; 128 agree on every known slot. The 7 that differ differ only in
  an enum name (`Operation`), because several sibling classes share a layout and
  the bag belongs to one of them. This shows an owner can be ambiguous among
  siblings, but every sibling gives the same element type for these 53 slots.
  None of the controls is an array slot that was `Unknown`, so "bag arrays equal
  class arrays" rests on the native construction path, not on a measured array
  match.
- The SDK dumper prints these slots as `TArray<FNone_>` and the GObjects dump
  lists fields without inner types, so neither helps. The executable holds no
  property-name strings (a search for the PCG field names found none), so the
  native `FArrayPropertyParams` tables cannot be found by name. Matching them by
  class offset is an untried route.

Table (class candidates alphabetical; `+N more` share the layout):

| Owner | Slot | Property | Resolved element type | Native class layout candidates |
|---|---:|---|---|---|
| `PropertyBag_1487c074c62ee71a` | 1 | `PropertyOverrideDescriptions` | `struct PCGObjectPropertyOverrideDescription` | PCGApplyOnActorSettings |
| `PropertyBag_1487c074c62ee71a` | 2 | `PostProcessFunctionNames` | `Name` | PCGApplyOnActorSettings |
| `PropertyBag_1585cbada2e199af` | 6 | `PropertyOverrideDescriptions` | `struct PCGObjectPropertyOverrideDescription` | PCGCreateTargetActor |
| `PropertyBag_1585cbada2e199af` | 7 | `PostProcessFunctionNames` | `Name` | PCGCreateTargetActor |
| `PropertyBag_209db8d5615f7a92` | 0 | `PointsToCreate` | `struct PCGPoint` | PCGCreatePointsSettings |
| `PropertyBag_2318d64182fb9807` | 5 | `AttributeSelectors` | `struct PCGAttributePropertyInputSelector` | PCGExportSelectedAttributesSettings |
| `PropertyBag_27f26af0ed720151` | 0 | `ObjectPathsToExtract` | `struct SoftObjectPath` | PCGGetPropertyFromObjectPathSettings |
| `PropertyBag_3bab74d7a3c7be2e` | 7 | `ModulesInfo` | `struct PCGSubdivisionSubmodule` | PCGDuplicateCrossSectionsSettings |
| `PropertyBag_3ef02d9f582ee539` | 9 | `ExpectedPins` | `Name` | PCGDataFromActorSettings +5 more |
| `PropertyBag_44e717d4e08315ef` | 0 | `AttributeSelectors` | `struct PCGAttributePropertyInputSelector` | PCGAttributeRemoveDuplicatesSettings |
| `PropertyBag_60d0a20ea57c4ba0` | 6 | `ThreadCountInputPinLabels` | `Name` | PCGCustomHLSLSettings |
| `PropertyBag_60d0a20ea57c4ba0` | 7 | `InputPins` | `struct PCGPinProperties` | PCGCustomHLSLSettings |
| `PropertyBag_60d0a20ea57c4ba0` | 8 | `OutputPins` | `struct PCGPinPropertiesGPU` | PCGCustomHLSLSettings |
| `PropertyBag_60e2e02e7a30aea2` | 4 | `PostProcessFunctionNames` | `Name` | PCGSpawnSplineSettings |
| `PropertyBag_60e2e02e7a30aea2` | 5 | `PropertyOverrideDescriptions` | `struct PCGObjectPropertyOverrideDescription` | PCGSpawnSplineSettings |
| `PropertyBag_65262dcdfc7785f5` | 3 | `DynamicInputPinProperties` | `struct PCGPinProperties` | PCGOuterIntersectionSettings |
| `PropertyBag_654f55450ad44868` | 0 | `DynamicInputPinProperties` | `struct PCGPinProperties` | PCGGatherSettings +2 more |
| `PropertyBag_6d761ca594eea4c2` | 10 | `ExpectedPins` | `Name` | PCGGetLandscapeSettings |
| `PropertyBag_7a739a740fa3a036` | 0 | `SelectedGrassTypes` | `String` | PCGGenerateGrassMapsSettings,PCGGenerateLandscapeTexturesSettings |
| `PropertyBag_8233530be97d0918` | 5 | `Criteria` | `struct PCGSelectGrammarCriterion` | PCGSelectGrammarSettings |
| `PropertyBag_8cd2c9521e9f1f96` | 0 | `Pins` | `struct PCGPinProperties` | PCGSaveDataAssetSettings |
| `PropertyBag_914ca296294cbc7b` | 0 | `StaticMeshes` | `SoftObject` | PCGGetStaticMeshResourceDataSettings |
| `PropertyBag_95101e0cb9e76227` | 10 | `ExpectedPins` | `Name` | PCGGetDynamicMeshDataSettings |
| `PropertyBag_99e0bababb68fde` | 1 | `Pins` | `struct PCGPinProperties` | PCGLoadDataAssetSettings |
| `PropertyBag_99e0bababb68fde` | 8 | `DefaultAttributeOverrides` | `String` | PCGLoadDataAssetSettings |
| `PropertyBag_9fe9c9fc5886f542` | 3 | `SkinnedMeshComponentPropertyOverrides` | `struct PCGObjectPropertyOverrideDescription` | PCGSkinnedMeshSpawnerSettings |
| `PropertyBag_9fe9c9fc5886f542` | 6 | `PostProcessFunctionNames` | `Name` | PCGSkinnedMeshSpawnerSettings |
| `PropertyBag_a2f4eb827fdd2ae` | 0 | `Pins` | `struct PCGPinProperties` | PCGGraphInputOutputSettings |
| `PropertyBag_a2f4eb827fdd2ae` | 2 | `CustomPins` | `struct PCGPinProperties` | PCGGraphInputOutputSettings |
| `PropertyBag_a34ad9027767ee88` | 0 | `PostSpawnFunctionNames` | `Name` | PCGSpawnActorSettings |
| `PropertyBag_a34ad9027767ee88` | 5 | `TagsToAddOnActors` | `Name` | PCGSpawnActorSettings |
| `PropertyBag_a34ad9027767ee88` | 7 | `SpawnedActorPropertyOverrideDescriptions` | `struct PCGObjectPropertyOverrideDescription` | PCGSpawnActorSettings |
| `PropertyBag_b216dc8b4f3f20a` | 0 | `PartitionAttributeSelectors` | `struct PCGAttributePropertyInputSelector` | PCGMetadataPartitionSettings |
| `PropertyBag_b7705f2fc3f226cf` | 1 | `DynamicInputPinProperties` | `struct PCGPinProperties` | PCGMergeSettings |
| `PropertyBag_b91efdd543605541` | 2 | `OverrideMaterials` | `SoftObject` | PCGStaticMeshToDynamicMeshSettings |
| `PropertyBag_be19fd2c3e64390d` | 2 | `IntOptions` | `int32` | PCGMultiSelectSettings,PCGSwitchSettings |
| `PropertyBag_be19fd2c3e64390d` | 4 | `StringOptions` | `String` | PCGMultiSelectSettings,PCGSwitchSettings |
| `PropertyBag_be19fd2c3e64390d` | 6 | `CachedPinLabels` | `Name` | PCGMultiSelectSettings,PCGSwitchSettings |
| `PropertyBag_c4285d290d6e93b1` | 0 | `PointKeyAttributes` | `struct PCGAttributePropertyInputSelector` | PCGApplyHierarchySettings |
| `PropertyBag_c4285d290d6e93b1` | 1 | `ParentKeyAttributes` | `struct PCGAttributePropertyInputSelector` | PCGApplyHierarchySettings |
| `PropertyBag_c6e7610ba669bbbe` | 11 | `ModulesInfo` | `struct PCGSubdivisionSubmodule` | PCGSubdivideSplineSettings |
| `PropertyBag_c96ce6bb861bd207` | 5 | `StaticMeshComponentPropertyOverrides` | `struct PCGObjectPropertyOverrideDescription` | PCGStaticMeshSpawnerSettings |
| `PropertyBag_c96ce6bb861bd207` | 9 | `PostProcessFunctionNames` | `Name` | PCGStaticMeshSpawnerSettings |
| `PropertyBag_cf5d09ff7ccda82a` | 7 | `AttributesToMerge` | `struct PCGAttributePropertyOutputNoSourceSelector` | PCGCollapsePointsSettings |
| `PropertyBag_e62add25bfeae12e` | 2 | `DynamicInputPinProperties` | `struct PCGPinProperties` | PCGUnionSettings |
| `PropertyBag_ed3dc2a06345ee71` | 3 | `PostProcessFunctionNames` | `Name` | PCGSpawnSplineMeshSettings |
| `PropertyBag_ed3dc2a06345ee71` | 5 | `SplineMeshOverrideDescriptions` | `struct PCGObjectPropertyOverrideDescription` | PCGSpawnSplineMeshSettings |
| `PropertyBag_ed3dc2a06345ee71` | 6 | `SplineMeshParamsOverride` | `struct PCGObjectPropertyOverrideDescription` | PCGSpawnSplineMeshSettings |
| `PropertyBag_ed3dc2a06345ee71` | 7 | `SplineMeshComponentOverride` | `struct PCGObjectPropertyOverrideDescription` | PCGSpawnSplineMeshSettings |
| `PropertyBag_ef18a43aeed05598` | 1 | `ModulesInfo` | `struct PCGSubdivisionSubmodule` | PCGSubdivisionBaseSettings |
| `PropertyBag_f016b94fced84e6a` | 7 | `PostProcessFunctionNames` | `Name` | PCGCreateSplineSettings |
| `PropertyBag_f08d71a110dc1aa4` | 13 | `ModulesInfo` | `struct PCGSubdivisionSubmodule` | PCGSubdivideSegmentSettings |
| `PropertyBag_fa90aa0ddec3194e` | 1 | `PostProcessFunctionNames` | `Name` | PCGSpawnDynamicMeshSettings |

## 2. The 2,690 hashed name occurrences

Counts come from a parsed inventory of the final map (909 owners, 2,391
distinct tokens; 197 tokens appear in more than one owner) compared with the
closed-beta donor map, the only donor with real names.

| Bucket (by donor evidence) | Occurrences | Recoverable? |
|---|---:|---|
| A. Owner absent from the closed beta | 1,128 | No donor; needs new evidence |
| D. Beta owner present, beta slot is also hashed | 1,095 | No donor name |
| C. Beta slot holds a different-length name | 192 | Slot alignment unreliable; no inference |
| E. Beta owner present, no beta property at the slot | 177 | No donor |
| B1. Beta name at the slot, already used by another property of the live struct | 91 | Refused (one-to-one) |
| B2. Beta name at the slot, length and type match, name unused | 7 | Not proven; see below |

These sum to 2,690 (1,128 + 1,095 + 192 + 177 + 91 + 7). After the Blueprint
pass (section 3) 45 are named, leaving 2,645 (A 1,085, D 1,093, C 192, E 177,
B1 91, B2 7).

By module (SDK header `// Class Pkg.Name` of the owner, 2,645 remaining):
`WDGame` 1,898 (72%), `Mechanized` 143, `BuildablesRuntime` 84, `WDWeather` 69,
`AOVolumeBaker` 55, generated property bags 37, `SniperShowdownRuntime` 34,
`GaeaCustomTerrainRuntime` 28, `ServerSeedingRuntime` 22, `TeamOffenceRuntime`
22, `BHMover` 21, `BHDestruction` 19, `MolotovRuntime` 18, `SpottingRuntime` 17,
40 other modules 178. Largest owners: `WDUIVendorPanelData_Wagers` 67,
`WDUIVendorPanelWidget_Wagers` 57, `WDCameraProjectile` 48,
`WDUIVendorPanelViewModel_Wagers` 39; owners with "Wager" in the name hold 467
occurrences. By type: 660 struct, 476 float, 408 object, 293 bool, 203 text,
157 int. By the name length the token encodes: 55 are 8 or shorter, 700 are
9-14, 1,890 are 15 or longer.

Why most stay hashed. The hash is not a standard function: a fresh test of
FNV-1, FNV-1a, djb2, sdbm, MurmurHash64A and XXH64 (UTF-8, lower-cased, UTF-16,
lower-cased UTF-16) against 300 of the 31,815 known token-to-name pairs matched
none. The runtime itself uses the hashed names (the GObjects dump has 15,024
hashed lines) and the SDK prints the same tokens. The length check alone (a
chance match of roughly one in ten for names of 9-14 letters) cannot prove a
candidate. Only real-name evidence from the build's own data can name a token.

The 7 bucket-B2 candidates, none accepted:

| Owner[slot] | Beta name | Why it is not accepted |
|---|---|---|
| `Material[63]`, `[64]` | `bUsedWithMorphTargets` | Two live tokens compete for one beta name; the one-to-one rule refuses both |
| `Material[74]`, `[75]` | `bUsedWithNanite` | Same |
| `WDWeaponStats[15]` | `bFirstFocalPlane` | Documented withdrawal: the SDK gives that name to `WDSightData[29]` ([mappings README](../../mappings/README.md)) |
| `WDVehicleSeatNameOverrideRow[0]` | `SeatIndexToText` | Live type is `TMap<uint8, FWDSeatOverrideData>`; the name implies a text value, so the beta field may differ. Not proven either way |
| `WDUIScoreboardItemWidget[2]` | `ScoreboardListView` | SDK type is `UHorizontalBox*`; the name implies a list view. Not proven either way |

## 3. What is proven: names from cooked Blueprint classes

Cooked `UBlueprintGeneratedClass` exports keep serialized `ChildProperties`
with real FNames, even where the usmap token is hashed (**Data**; read with
CUE4Parse from the installed paks, the same source as the
[Blueprint type recovery](round8-mapping-gaps.md)). The 30 hashed `_C`
occurrences, in 20 Blueprint owners, were checked against their packages. A slot
is accepted when:

- the cooked field count equals the owner's property count;
- every non-hashed property has the same name (ASCII case-insensitive) at the
  same ordinal;
- the field kind at the hashed ordinal equals the usmap kind;
- the real name has the length the token encodes.

Result: **30 of 30** slots pass, giving **18 tokens** with one name each, no
token with two names and no name with two tokens. `GC_Weapon_Fire_C` has one
unrelated neighbour whose cooked kind is `FClassProperty` where the usmap says
`ObjectProperty`; the rule ignores neighbour kinds, so it does not matter.
`B_Action_StimPen_C` carries a number suffix: the token
`_aaaaligppledmpcaeifph_0` and cooked `DecayAmount_0` agree (base length 11).

A token means one name everywhere, so the same 18 tokens also rename **15**
occurrences in other owners (mostly `WDUI*` view models and widgets). The tool
skips a rename if the struct already has a property with that name; no skip
occurred. Total **45 occurrences** (30 `_C` and 15 other).

| Token | Name | Length | Source `_C` owners | Other owners renamed |
|---|---|---:|---:|---|
| `_aaaamiekmphilgcdjfchh` | `ChargesToUse` | 12 | 1 | - |
| `_aaaaogcgncolkcfaadaac` | `ControlledPawn` | 14 | 1 | - |
| `_aaaajfoolbmbaaoimkehn` | `CountText` | 9 | 3 | `WDUIWagerObjectiveRowViewModel`, `WDUIWagerObjectiveTileRowViewModel` |
| `_aaaaligppledmpcaeifph_0` | `DecayAmount_0` | 11 | 1 | - |
| `_aaaajohejeacbaoneileo` | `FadeCurve` | 9 | 1 | - |
| `_aaabdhfnnclknogoeefak` | `InstigatorCharacter` | 19 | 7 | - |
| `_aaaailhcgejjojlpkklck` | `OddsText` | 8 | 2 | `WDUIWagerObjectiveRowViewModel`, `WDUIWagerObjectiveTileRowViewModel`, `WDUIWagerStatusActionRowViewModel`, `WDUIWagerStatusActionRowWidget`, `WDUIWagerStatusConditionRowViewModel`, `WDUIWagerStatusConditionRowWidget`, `WDUIWagerTileTooltipData`, `WDUIWagerTileTooltipViewModel`, `WDUIWagerTileTooltipWidget` |
| `_aaabdoojgfidofmeahoke` | `ProjectileSubSystem` | 19 | 1 | - |
| `_aaaanhocpdppoeffojflj` | `QueueProgress` | 13 | 1 | `WDUIServerQueueViewModel` |
| `_aaabbgdfgljpaemakdmcf` | `ReceiptActionText` | 17 | 1 | `WDUIVendorPanelViewModel_Wagers` |
| `_aaaamaeclijfglinemook` | `RepairAmount` | 12 | 1 | - |
| `_aaaamcnhlonpgicmioknh` | `ServerIDText` | 12 | 1 | `WDUIServerIDViewModel` |
| `_aaaapbnnoiiepommdkgeo` | `TargetCharacter` | 15 | 4 | - |
| `_aaaapcpkipenbedenmabm` | `TimeInQueueText` | 15 | 1 | `WDUIServerQueueViewModel` |
| `_aaabecacichpebfehdiaf` | `TotalInteractionTime` | 20 | 1 | - |
| `_aaaanjgbdlhihabdjacil` | `VehicleWeapon` | 13 | 1 | - |
| `_aaaalbdcopgdhancoiafn` | `VelocityMax` | 11 | 1 | - |
| `_aaaalodbhomkodcpaecnc` | `VelocityMin` | 11 | 1 | - |

Effect on `data/`: none of these 18 tokens occurs in any `data/**/*.json` file
(Blueprint exports use the package's own property tags, not the usmap), so zero
keys change. The change is to the usmap only.

## 4. Regeneration steps (not run on `data/`)

Tools: `WdExtract recover-bp-names <new.usmap>` (new, `BlueprintNames.cs`) and
`WdExtract recover-pcg-layout-types <new.usmap>` (new, `PcgLayoutTypes.cs`),
documented in [`tools/cue4parse_extractor/README.md`](../../tools/cue4parse_extractor/README.md).
Both refuse an existing output path. Build the extractor with
`dotnet build -c Release -p:CUE4ParseProject=<CUE4Parse.csproj> --artifacts-path <fresh dir>`.

1. Names (needs the paks and key path; the key is never printed):
   `WdExtract <Paks> <keyfile> <final map> <outDir> <Paks>\oo2core_9_win64.dll recover-bp-names <names.usmap>`.
   Measured: **45 renamed**, hashed 2,690 to **2,645**; log
   `_blueprint_names_log.txt`.
2. Types (map only, no paks; `-` fills the unused arguments):
   `WdExtract - - <names.usmap> <outDir> - recover-pcg-layout-types <final.usmap>`.
   Measured: **53 filled across 36 owners**, 0 unknown remain; log
   `_pcg_layout_types_log.txt`. Run alone on the starting map it gives the same
   53 fills; a replay on its own output fills 0.
3. Chained result: **3,046,679 bytes**, SHA-256
   `9831826a4d61392be0fc11213ab1b57883943fafc98ccd151241a5df6914daeb`. A parsed
   comparison with the starting map finds exactly **45 name changes, 53 type
   changes, 0 other differences** (21,216 structs and 3,222 enums on both sides).
4. Prove no data changed: re-export the packages that use the 36 bag owners and
   the 32 renamed owners with both maps, then run
   `python -I _tools/check_data_renames.py`; it fails on any value change.
   Expected effect on `data/`: no key or value changes (no token occurs there,
   and CUE4Parse skips property-bag payloads). If the lead declines the type
   fills, run step 1 only.
5. Update `mappings/README.md`: hashed count 2,690 to 2,645 and, if step 2 is
   accepted, unknown count 53 to 0.

Verified here: both steps ran on the real paks and map and the outputs read
back through CUE4Parse. Nothing under `data/` or `mappings/` was written. The
re-export in step 4 was not run.

## 5. Still open

- 2,645 hashed names still need real-name evidence. Other cooked sources with
  real names are untested.
- The hash function is unknown. The 31,815 known pairs could test a custom or
  keyed hash; this round tested only six common functions.
- The type fills are layout-derived, not hash-bound. A serialized descriptor
  with the owners' hashes, or the native `FArrayPropertyParams` tables matched
  by class offset, would prove them.
