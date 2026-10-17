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
| `findname <path prefix> <text>` | `<out>/findname.txt`: packages under the prefix whose name map contains the text (IoStore imports are hashed, so this finds names an asset uses, not who references it) |

**`--names <usmap>`** (any mode) borrows property names and array element
types from an unobfuscated usmap for every struct whose layout matches this
build's property for property. The closed-beta usmap
(`507_Wardogs_ClosedBeta.usmap`, an older build) restores about 43,500
hashed or `Unknown` properties in about 10,600 structs; structs that changed
between builds are left alone. With it, skeletal meshes and physics assets
decode too. Like the live usmap, it stays local and is never committed.
Checked: a GE re-dump with `--names` is byte-identical to the published export.

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
