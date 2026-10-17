# cue4parse_extractor (WdExtract)

Offline static export of cooked Wardogs assets with
[CUE4Parse](https://github.com/FabianFG/CUE4Parse). It reads the game's own
`.pak`/`.utoc` files; it never runs the game or contacts a service. This is
the tool behind [`assets/data/ge-values.json`](../../assets/data/ge-values.json)
(the [Gameplay Effect Values](../../Wardogs_GameplayEffect_Values_v1.md) page)
and the Blueprint bytecode in
[DamagePipeline §7](../../Wardogs_DamagePipeline_v2.md#7-custom-operations).

## You need

- .NET SDK 10
- A CUE4Parse checkout. FabianFG/CUE4Parse at commit `0415fe2` (2026-10-14) is
  known to work with this build. By default the project expects it at
  `../../../CUE4Parse` (next to this repository's folder); otherwise pass
  `-p:CUE4ParseProject=<path to CUE4Parse.csproj>`.
- Your own installed copy of the game: the `Paks` folder and its
  `oo2core_9_win64.dll`.
- The build's usmap (`5.7.4-516586+++Wardogs+Live-Wardogs.usmap`) and the pak AES
  key in a one-line text file. Neither is in this repository; `.gitignore` keeps
  `aes.*` and `*.usmap` out if you store them in the checkout.

## Build

```
dotnet build -c Release -p:CUE4ParseProject=<path>\CUE4Parse\CUE4Parse.csproj
```

## Run

```
WdExtract <Paks> <keyfile> <usmap> <out> <Paks>\oo2core_9_win64.dll <mode> [args] [--names <usmap>]
```

| Mode | Writes |
|---|---|
| `list GE_` | `<out>/files.txt`: every package whose name starts with the prefix |
| `schema BHGameplay` | `<out>/usmap_schema.json`: usmap layouts whose name contains the text |
| `dump <files.txt or package paths>` | `<out>/<name>.json` per package: all exports, Blueprint bytecode included; failures in `_failures.txt` |
| `deobfuscate <out.usmap> --names <donor.usmap> [--sdk <sdk/raw>]` | A deobfuscated copy of `<usmap>`: names and element types restored from the donor, then (with `--sdk`) from this build's SDK headers, then the hand patches; read back through CUE4Parse to check it. No paks or key are read (pass `-` for those arguments). Log in `<out>/_deobfuscate_log.txt` |
| `findname <path prefix> <text>` | `<out>/findname.txt`: packages under the prefix whose name map contains the text (IoStore imports are hashed, so this finds names an asset uses, not who references it) |

**`--names <usmap>`** (any mode) borrows property names and array element
types from an unobfuscated usmap, by the same rules as `deobfuscate` (see
[`mappings/README.md`](../../mappings/README.md#how-deobfuscated-it-is)).
Simpler: generate the deobfuscated usmap once and pass it as `<usmap>`:

```
WdExtract - - mappings\5.7.4-516586+++Wardogs+Live-Wardogs.usmap out - deobfuscate ^
  mappings\5.7.4-516586+++Wardogs+Live-Wardogs.deobfuscated.v2.usmap ^
  --names mappings\old-deobfuscated-507-ClosedBeta.usmap --sdk sdk\raw
```

**`--sdk <dir>`** (`deobfuscate` only) aligns each usmap struct with its declaration in the
Dumper-style SDK headers of this build (`sdk/raw/*_classes.hpp`, `*_structs.hpp`). The pass pairs
properties only between anchors where both sides agree on count, type, static-array size and token
length. It corrects closed-beta names where fields were reordered between builds, and withdraws a
donor name when the SDK gives that name to another token. The log lines start with `sdk`; the
method and counts are in [`mappings/README.md`](../../mappings/README.md#how-deobfuscated-it-is).
Without `--sdk` the output is the v1 file, byte for byte.

The donor is the closed-beta usmap (`mappings/old-deobfuscated-507-ClosedBeta.usmap`,
an older build, not obfuscated). With the result, skeletal meshes, physics assets
and data tables decode too. Keep both usmaps in `mappings/`; they are gitignored
and never committed. Checked: all 341 GE assets re-dumped with the deobfuscated
usmap are byte-identical to the published export.

`dump` first restores usmap property names that are hashed in this build and
array types the usmap leaves as `Unknown`, by property index against the SDK
headers in `sdk/raw/` and UE's declaration order: `BHGameplayEffect.Modifiers`,
`GameplayTagQuery.TagDictionary` / `QueryTokenStream`, and for static meshes
`StaticMaterials`, `Sockets`, `AssetUserData`, `ComplexCollisionMesh` and
`StaticMaterial.MaterialSlotName` (without these a static mesh's render data
fails to load). What it changed is
written to `_usmap_patches.txt`.

## Post-processing

- `python -I ge_summary.py <out> <out>/files.txt <summary dir>` turns GE dumps
  into `ge_summary.json` (copy it to `assets/data/ge-values.json`) and a
  markdown overview. Then run `python _tools/ge_values.py` from the repository
  root.
- `python -I kismet_listing.py <dump>.json <listing>.txt` prints a Blueprint's
  bytecode one statement per line with byte offsets.

## Reproduce the GE export

```
WdExtract <Paks> <keyfile> <usmap> out <Paks>\oo2core_9_win64.dll list GE_
WdExtract <Paks> <keyfile> <usmap> out\ge_raw <Paks>\oo2core_9_win64.dll dump out\files.txt
python -I ge_summary.py out\ge_raw out\files.txt out
```

Checked on 2026-10-17: 341 packages, and a re-dump matched the published
export byte for byte.
