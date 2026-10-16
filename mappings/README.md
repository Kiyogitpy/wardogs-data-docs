# Mappings — IDA + usmap

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Compiled-binary mappings that let community tooling resolve names
and offsets inside the shipped Wardogs client.

## Authoritative IDA map

The only IDA map for this project is the user-supplied file:

`E:/Reverse_Engineer/wardogs_analysis/IDAMappings/5.7.4-516586+++Wardogs+Live-Wardogs.idmap`

Size: 4,942,224 bytes. SHA-256:
`f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb`.

Use this file directly. The byte-identical checkout and temporary analysis
copies were removed on 2026-10-17. Do not retain duplicate or alternative
`.idmap` files for this project. This is a local workstation path, not a
download bundled with the documentation. The `.usmap` below serves cooked
asset extraction and remains a separate input.

## What's here

| File | Size | Purpose |
|---|---:|---|
| `5.7.4-516586+++Wardogs+Live-Wardogs.usmap` | 1.1 MB | UE class/property metadata used by CUE4Parse / FModel |

## Build identity

| Attribute | Value |
|---|---|
| Game | Wardogs |
| Engine version | 5.7.4 |
| Changelist | 516586 |
| Full build string | `++Wardogs+Live-Wardogs` |
| Target binary | `WardogsClient-Win64-Shipping.exe` |

## File formats

### `.idmap` — IDA name mapping

The authoritative external artifact is **Dumper-7 binary mapping version 2**, with
magic byte `0xD7`, a packed header, string data, and typed record sections.
It is not an IDA Names-window text export. See the upstream
[layout](https://github.com/Encryqed/Dumper-7/blob/main/Dumper/Generator/Public/Generators/IDAMappingLayouts.h)
and [generator](https://github.com/Encryqed/Dumper-7/blob/main/Dumper/Generator/Private/Generators/IDAMappingGenerator.cpp).

The 2026-10-17 read-only decoder validated its section boundaries and
string references. It contains 3,225 enum records, 21,282 structure/class
records, 3 globals, 9,134 vtables, and **one native exec-function record**:
`AActor::AddComponent`. Do not interpret this file as comprehensive native
function coverage. Its exec-function record stores an RVA; the analysis
image base and build correspondence must be established independently.

The [initial damage IDA results](../docs/DAMAGE_IDA_RESULTS.md) record the
failure to validate locations against an older reconstructed PE. The later
[restored-input trace](../docs/DAMAGE_IDA_RESTORED.md) used selected validated
vtable labels from this map. Format validity alone does not establish a
mapping-to-image match.

### `.usmap` — UE class/property metadata

Binary format produced by the community UEDumper fork
([OutTheShade/UnrealMappingsDumper](https://github.com/OutTheShade/UnrealMappingsDumper))
or similar tools. Encodes:

- Class → parent class chain
- Class → property list (name, type, offset, size, flags)
- Enum → value list

Used by:

- **CUE4Parse** — resolves hashed property names when deserializing
  `.uasset` files
- **FModel** — same, for interactive browsing
- **UEDumper** — can import to seed a fresh dump

## How this fits the pipeline

```
.uasset (cooked) ──┐
                   ├─> CUE4Parse ──> data/*.json ──> reference docs
.usmap ────────────┘
                                                              ▲
                                                              │
                                                     cross-ref
                                                              │
.idmap ───────> IDA Pro ──> static RE ─────> formula docs ────┘
```

Short version:

- `.usmap` is a prerequisite for parsing newer UE5 cooked data where
  property names are no longer stored in the asset itself
- `.idmap` supplies type/vtable names for static RE; native registration
  strings and code remain useful where the map has limited coverage

## Usage with CUE4Parse

```csharp
var provider = new DefaultFileProvider(
    "C:/Program Files (x86)/Steam/steamapps/common/Wardogs/Wardogs/Content/Paks",
    SearchOption.AllDirectories,
    new VersionContainer(EGame.GAME_UE5_7));

// Load the usmap - required for 5.7+ cooked assets
provider.MappingsContainer = new FileUsmapTypeMappingsProvider(
    "mappings/5.7.4-516586+++Wardogs+Live-Wardogs.usmap");

provider.Initialize();
provider.SubmitKey(new FGuid(0, 0, 0, 0), new FAesKey("<derived AES key>"));

// Now provider.LoadPackage(...) works for cooked assets
```

## Usage with IDA Pro

Use the authoritative external path above with a reader/importer compatible
with the binary version, then validate
the selected records against the matching offline image before applying
names or types to an owned analysis database. Do not parse this artifact
as text or add an assumed image base to every field. The restored-input
pass applied selected checked labels to an owned database; a working full
importer is not claimed. Reading the canonical map directly does not
require copying it beside each analysis database.

## Refresh policy

The mappings are build-specific (`CL-516586`). Preserve the `.usmap` needed
to parse the existing exports. Do not generate, substitute or archive
additional IDA maps under the project's single-map policy. If a later
binary no longer matches the authoritative map, record the mismatch;
changing the designated map requires an explicit user instruction.

## Attribution

- `.usmap` format: community spec, implementations across OutTheShade
  UnrealMappingsDumper, FModel, CUE4Parse
- `.idmap` format: Dumper-7's published binary mapping layout, linked above
- Generation details for this build: see
  [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)

## Related

- SDK: [`../sdk/`](../sdk/) — class declarations derived from these mappings
- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Tools: [`../tools/`](../tools/)
