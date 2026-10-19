# Round 8 mapping gap audit

## Findings

**Latest checkpoint (2026-10-19):** the independent cooked-package recovery
now fills **162** of the established export map's **215** unknown array types
(83 Blueprint and 79 RigVM), leaving **53** unknown types across **36**
generated property-bag owners. The final map is **3,046,707 bytes** with SHA-256
`277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380`;
the **2,690 hashed-name** count is unchanged. The 53 remaining slots appear
PCG-related, but no exact PCG descriptor-to-owner match is established yet.
See the [property-bag recovery evidence](round8-propertybag-types.md).

A parsed inventory of the recovered map places the 2,690 hashed property
occurrences across 909 owners. Only 30 occurrences belong to `_C` owners;
the remaining 2,660 are elsewhere. This inventory does not recover their
names. Its raw records remain outside the repository under
`round8_propertybags_20261019/name-inventory/` in the analysis directory.

The documented v2 remainder is reproducible from files currently present. Running the local `tools/cue4parse_extractor/bin/Release/net10.0/WdExtract.exe` in `deobfuscate` mode with only the live map, the closed-beta donor, and `sdk/raw` produced **46,935 → 2,698 hashed names** and **5,550 → 451 unknown array element types**. Its log reports **21,213** SDK struct matches, **13,853** paired segments, and **44** rejected segments (**43 type**, **1 length**). The output is 3,045,675 bytes and SHA-256 `73d98a6bfccf6124822182d0c0c02103044e6d412fb7039c7c75c07bcc5c6a01`, identical to the documented v2 map. The command used `- -` for the unused pak/key arguments; deobfuscation returns before either is accessed.

Reachable mapping inputs in `mappings/` are the live obfuscated map, the build-507 closed-beta donor, v1, v2, v2 export, and a ZIP containing only v1. `sdk/raw/` contains 2,150 class/struct header files matching the tool's input pattern. The only other usmap filenames found in the analysis tree were copies of the live map and the same build-507 beta donor. No newer standalone unobfuscated donor is present. In particular, the documented dump-derived `E:/Wardogs_DataDump_v3/UsmapFromDump/new.usmap` is absent, and no mapping deobfuscation log is present in `mappings/`.

The available `5.7.4-516586+++Wardogs+Live-Wardogs.deobfuscated.v2.export.usmap` is an existing richer output, documented as v2 plus **236 element types** and **8 names across 6 tokens** from that absent dump map. It is evidence already embodied in a local map, not an independent newer donor. The checked-in extractor source (`Program.cs`, 2026-10-18) supports `--types` and `--fill-names`, but the prebuilt executable is dated 2026-10-17. Invoking its fill flags with the export map as donor produced the ordinary v2 hash and no `export` log entries, so this executable cannot replay those fills. The code's existing `ExportFill` path compares same-named structs and exact property slots; it may apply the export map's embedded information to v2, but this was not verified with a current build.

## Current-source fill verification

Built the checked-in source against the documented CUE4Parse checkout at `E:/WardogsConversion/CUE4Parse/` using `dotnet build --artifacts-path` into a fresh `%TEMP%` directory; neither repository `bin/obj` nor map files were overwritten. Build succeeded with 0 errors (the dependency build emitted existing NuGet vulnerability and compiler warnings). Running that new executable with the same live map, beta donor and SDK, and the available v2 export map as both `--types` and `--fill-names` reproduced the export exactly: **46,935 → 2,690 hashed names**, **5,550 → 215 unknown types**, with **236 types filled** and **8 properties across 6 unique tokens named**. The output was 3,046,162 bytes and SHA-256 `737d11016b9bc77242c6fcf64b35bfc0a72eabb226b68d00c786f75e59ab3ba8`, identical to the existing v2 export map. Its eight entries are `CaptureHeight`, `MeshPath`, `SupplyCrateValue` (two properties), `IconImage`, `TotalFOBSupplies` (two), and `NumberOfAssisters`.

At this historical checkpoint, the checked-in fill implementation replayed the six remaining export-map tokens and 236 types using the already-present export map. That left 2,690 hashed property occurrences and 215 unknown types. The report did not identify the six export-map tokens with the README's separate description of six SDK-unpaired leftovers. Later package-metadata recovery independently filled 162 of those 215 types; the dump-derived donor remains absent, but is no longer the only type-recovery path.

## Initial cooked-Blueprint recovery checkpoint, 2026-10-19

An exact inventory of the export map's 215 unresolved slots exposed another
independent source. Cooked Blueprint class exports retain serialized
`UStruct.ChildProperties`, including each `FArrayProperty.Inner` field.
CUE4Parse reads these FFields directly from the package archive; it does
not infer them from the usmap's unknown inner type. Referenced struct names
come from the field's serialized package index. This supplies evidence
without the missing dump-derived donor for the matching Blueprint slots.

The new `WdExtract recover-bp-types <new.usmap>` mode matches a unique
package basename to the `_C` owner, locates that exact generated-class
export, and requires an exact property-name and static-array-dimension
match. It accepts only fully resolved element metadata, with referenced
structs/enums present in the map. Known types and names are preserved.
Inconsistent expanded static-array slots are refused. An existing output
map is refused, with exclusive `CreateNew` output creation; the input is never
replaced. Its audit log identifies each source package and filled slot.

Against the unchanged v2 export input, the pass recovers **81** array
element types across **46** Blueprint owners, reducing **215 → 134**
unknown slots. Examples are `AEB_SetAudioParameters_C.Parameters` →
`AudioParameter`, `AEB_VehiclePerspective_C.ContextTags` → `GameplayTag`,
and `B_Action_Appliable_Base_C.LocalGameplayEffects` →
`BHGameplayEffectLocalHandle`. These are exact reflected field matches,
not deductions from the property names.

Validation against the matching installed packages:

- A separate parsed-map comparison found exactly the 81 candidate type
  changes, with identical owner/property sets, names, indices, static array
  sizes, superclass/layout information, other types and enums. Each map
  static size matched the cooked field's `ArrayDim`.
- The output reads back through CUE4Parse. Recovery replay fills zero slots
  and produces identical bytes. Output size **3,046,390** bytes; SHA-256
  `7860a184b27444e8852db636e29b86eb97fc747f1d9242210819521dffafc0e0`.
- Fresh exports of all **46** affected packages succeed under both maps:
  **46/0** before and **46/0** after, with byte-identical JSON exports.
- Attempting an existing output returns 1 and leaves its hash unchanged.
  The original v2 export retains SHA-256 `737d1101…3ba8`.
- The existing `deobfuscate --sdk --types --fill-names` route was rerun
  after the writer change and still produces that exact established
  v2 export hash, with 2,690 hashed names and 215 unknown types.

No checked-in data, established usmap or prebuilt executable was replaced.
Isolated build artifacts, new maps, raw package exports and logs
remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_blueprint_type_recovery_20261019/`;
the independent candidate probe and exact-slot inventory are in neighboring
`round8_blueprint_type_probe_20261019/` and `round8_mapping_residual_20261019/`.
The reproducible mode is implemented in
`tools/cue4parse_extractor/BlueprintTypes.cs` and wired through `Program.cs`.

At the intermediate 134-slot checkpoint, the remainder contained 132
generated `PropertyBag_*` entries and two case-only Blueprint name misses
(`B_Action_Melee_C[5]` and `B_WDItemExtension_ItemMelee_C[6]`). A later
guarded case-resolution pass used the complete ordered owner layout and
closed those two misses; see the recovery evidence for the regression
boundary. The hashed-name remainder remains **2,690**.

The current 53 unknowns are all in **36** generated property-bag owners.
Their member names suggest PCG-related bags. A full-package scan of exact
PCG graph/graph-instance exports found no residual-owner matches in 294
nonempty serialized bags, with zero read failures. Native settings-derived
candidates reproduced eight already-typed bags but none of these 36 owners.
No additional type fill is claimed; a different descriptor source or proved
owner binding is needed before continuing recovery.
The separate RigVM pass has already recovered 79 array types by matching
serialized descriptors and target-verified bag hashes. Full current methods,
hash evidence, and validation are in the
[property-bag recovery evidence](round8-propertybag-types.md).

## Conclusion and next step

The 2,698/451 v2 baseline and 2,690/215 established export remain
reproducible. Independent package evidence now supplies **162** type fills,
leaving **2,690 hashed names / 53 unknown types** in the verified final map.
The remaining fields belong to 36 generated property-bag owners; PCG is a
candidate source, not a resolved join. The absent `new.usmap` still prevents
independently reproducing that historical donor. The 44 SDK segment
rejections and uncertain overlap of six export tokens with six SDK-unpaired
leftovers are unchanged.

Evidence: [`mappings/README.md`](../../mappings/README.md), [`tools/cue4parse_extractor/README.md`](../../tools/cue4parse_extractor/README.md), `tools/cue4parse_extractor/Program.cs` (`SdkNames.Apply`, `ExportFill.Types`, `ExportFill.Names`), the reachable map filenames and hashes, and the read-only `deobfuscate` runs described above. No AES/key contents were opened.
