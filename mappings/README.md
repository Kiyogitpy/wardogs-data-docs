# Mappings — IDA + usmap

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Compiled-binary mappings that let community tooling resolve names
and offsets inside the shipped Wardogs client.

## What's here

| File | Size | Purpose |
|---|---:|---|
| `5.7.4-516586+++Wardogs+Live-Wardogs.idmap` | 4.9 MB | IDA Pro name map — one line per named address |
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

Plain-text, one entry per line:

```
<address> <name>
<address> <name>
...
```

Produced by exporting the IDA Pro Names list on a loaded game
binary. Addresses are preferred-base relative — when the binary
loads at `0x200000000` (its ImageBase), the addresses in this file
are relative to that.

Import into a fresh IDA session via the `Names` window → `Import...`
or an IDA Python script that iterates lines and calls
`idc.set_name(ea, name)`.

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
- `.idmap` is a prerequisite for productive static RE on the shipped
  binary — raw IDA without this gives you nothing but mangled Rtti
  class names

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

```python
# IDA Python - run from File > Script File...
import idc
idmap = r"<path to>\5.7.4-516586+++Wardogs+Live-Wardogs.idmap"
with open(idmap) as f:
    for line in f:
        parts = line.strip().split(None, 1)
        if len(parts) != 2: continue
        try:
            ea = int(parts[0], 16)
            idc.set_name(ea, parts[1], idc.SN_NOWARN | idc.SN_NOCHECK)
        except ValueError:
            continue
print("Done.")
```

## Refresh policy

The mappings are tied to the exact build (`CL-516586`). A patch
that changes properties, classes, or enum values requires:

1. Fresh UEDumper run → new `.usmap`
2. Fresh IDA export → new `.idmap`
3. Rename the files with the new build CL
4. Commit alongside the previous build's files (so old data in
   `data/` can still be parsed with the old mapping)

## Attribution

- `.usmap` format: community spec, implementations across OutTheShade
  UnrealMappingsDumper, FModel, CUE4Parse
- `.idmap` is a vendored IDA export convention — plain text, no spec
  needed
- Generation details for this build: see
  [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)

## Related

- SDK: [`../sdk/`](../sdk/) — class declarations derived from these mappings
- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Tools: [`../tools/`](../tools/)
