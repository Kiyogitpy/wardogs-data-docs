---
title: Round 8 generated property-bag type recovery
nav_exclude: true
---

# Exact RigVM descriptor hashes recover 79 more array types

Offline CL516586 package metadata and the restored executable establish an
independent source for generated property-bag schemas. This extends the
[Blueprint recovery](round8-mapping-gaps.md), without replacing an existing
map, executing the game, or relying on the absent dump-derived donor.
Executable SHA-256 is
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.

## Descriptor identity is native, not a field-name guess

The target's `UPropertyBag::GetOrCreateFromDescs` at `0x1813160` hashes
64-byte descriptors in array order (`0x18131D0`–`0x18132F0`). It appends
the 16 raw GUID bytes, one value-type byte, three container bytes, eight
little-endian property-flag bytes, and UTF-16LE text comprising the FName
and any referenced value object's full path, without a null terminator.
The three container bytes retain two type slots and their count.
The cooked path does not hash editor metadata. Reset/update/finalize use
the XXH3-64 path (`0x15F74C0`, `0x15FCE40` → `0x15FF3B0`,
`0x15E6390` → `0x15FECF0`). Native `0x181331C` formats
`PropertyBag_%llx` from the digest. Local UE5.7 source corroborates the
algorithm; the target instructions and exact generated-name matches
establish its applicability to this build.

The target registers `PropertyBagCustomVersion` **3** at `0x109F7C5`.
Its descriptor constructor writes property flags **1** at `+0x28`
(`0x18062CC`). CUE4Parse only reads serialized flags starting with version
4, leaving its .NET field at zero for these older descriptors. Using that
zero yields no matching bag identities. Restoring the native default
`CPF_Edit=1` reproduces existing owner hashes, including
`CR_Bipod`'s work bag `PropertyBag_50b8eeaec79703a5`.
This is a serialization-default correction for hashing, not a guessed type.

## Recovery and validation

`recover-rigvm-types <new.usmap>` reads the three supported native RigVM
export classes and their literal/default-work/default-debug memory bags.
It reconstructs each descriptor hash and requires an exact existing owner,
ordered property names, slot count, static dimensions and all already-known
types. Referenced structs/enums must exist in the map. Conflicting payloads
cancel that owner's staged fills. Versions newer than 3 are refused.
Only unknown array element types are changed; field names remain intact.

The scan loads **107,181/107,181** mounted packages, visits **36** target
exports and **68** nonempty bag instances, and reports **zero failures**.
It reproduces **19** unique existing owner hashes. **11** owners provide
**79** new array fills: **78** `Array<CachedRigElement>` fields and one
`Array<Array<ConstraintParent>>` field. Container nesting is preserved.
The 79-fill map has SHA-256
`af42545cb17df026ec6531498b5f42a0c9b2108713fa21763e0a22ccc85fe411`;
replay fills zero slots and produces identical bytes.

The separate Blueprint pass now also resolves the two `hitactor`/`HitActor`
fields through a unique ASCII case match plus the complete ordered owner
name/static-dimension layout. A changed neighboring field name blocks that
fallback in the regression fixture; folded-name equality alone is insufficient.
The existing unrelated `Effect` class/object type discrepancy is preserved.
The Blueprint pass therefore supplies **83** fills and RigVM supplies **79**:
**162 total**, reducing the established export's **215 → 53** unknown slots.

An independent parsed-map comparison verifies exactly those 162 type
changes and identical names, indices, dimensions, owner/superclass layouts,
other types and enums. Fresh exports of all **58** affected packages pass
under both established and recovered maps (**58/0** each), with byte-identical
JSON. CUE4Parse still skips property-bag value payloads; this export comparison
does not claim to validate decoded bag values. Type evidence is the serialized
descriptors and target-verified owner hash.

Both recovery orders produce the same **3,046,707-byte** final map, SHA-256
`277ba0cd32445ec5abb0f5842452316644dabc283c0f41ae91fa384a8fd20380`.
Blueprint replay also produces identical bytes. Original maps and checked-in
exports are unchanged. Recovery uses exclusive `CreateNew` output creation
and refuses an existing destination.
An independent source review found no actionable correctness bug in the
matching, conflict rejection or output guards. A separate rerun of the
162-change comparison and final SHA-256 check passed.

Raw data, isolated builds, candidate lists, comparisons, negative fixture
and new maps remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_propertybags_20261019/`.
The **53** unresolved slots belong to **36** other generated property-bag
owners; no exact supported descriptor join has yet been established for them.
Hashed-name remainder is still **2,690**.

## Remaining PCG candidates are not accepted fills

The native PCG initializer at `0x64982A0` walks fields declared by descendants
of `PCGSettings`, excluding fields owned by that base class. It constructs
descriptors at `0x64983A7`, calls the bag generator at `0x64983E7`, and stores
the result at settings offset `+0xB0`. The descriptor constructor supplies
zero GUIDs and flags 1. Native hash generation precedes removal of unsupported
value-type-zero descriptors (`0x18136C1`–`0x1813755`). A Map field can therefore
contribute to the hash while being absent from the resulting bag layout.

Thirty-five of the 36 remaining owners have ordered names matching native
PCG settings layouts. The other has the Switch/MultiSelect shape after
removal of `EnumValueToPinLabelMapping`. These are localization leads only:
a prototype using 171 fully described native-class candidates reproduces
**zero** remaining owner hashes. Against all 321 existing bag owners, the
same prototype reproduces eight already-typed bags, including
`PCGPointExtentsModifierSettings` and `PCGSplineSamplerSettings`; those
positive controls do not identify any unresolved owner. For example, five native
`PCGApplyOnActorSettings` fields reproduce the names and types of
`PropertyBag_1487c074c62ee71a`, but their zero-GUID descriptor hash differs.
No remaining field is filled from this name/layout correspondence. The native
settings bag pointer is transient and rebuilt during initialization; its
descriptor identity need not identify a serialized bag with the same layout.
Serialized PCG bag descriptors are a separate source to inspect for exact
identities.

The eight native controls have limited ordering coverage: seven contain
one descriptor and `PCGPointExtentsModifierSettings` contains two. For
the five-field `PCGApplyOnActorSettings` candidate, usmap key order agrees
with SDK offset order, but a target compiled field-registration table has
not been recovered. The target initializer starts from class
`ChildProperties +0x50` and advances via `FField.Next +0x18` before
constructing descriptors at `0x64983A7`. Local UE 5.7 construction code
explains how generated property-table order reaches that list; its
different CL does not prove this target's sequence. There is no evidence
that descriptor order causes the mismatch, and no reordering-based fill
is accepted. Target field-registration metadata would provide another
bounded source to check.

The existing `GObjects-Dump-WithProperties.txt` snapshot corroborates
the five class fields at lines 19361–19366 and the bag's corresponding
fields at 161743–161748. Its header identifies CL516586; SHA-256 is
`85f80d2f8c94b83f825f3010f1e1f7804484e4a6b1badca3347491591ab98f7e`.
Those rows contain field kinds, names, offsets and addresses, but not the
two arrays' inner types or descriptor GUIDs. The dump producer's traversal
order has not been tied to this snapshot, so display order alone does not
settle `FField.Next`. The file remains outside the repo at
`E:/Reverse_Engineer/wardogs_analysis/GObjects-Dump-WithProperties.txt`;
no additional fill follows from these rows.

A subsequent serialized probe loads **107,181/107,181** packages and examines
**1,810,214** IoStore exports. Its exact-class targets are 14 `PCGGraph`
exports and 446 `PCGGraphInstance` exports. It reads `UserParameters` and
`ParametersOverrides.Parameters`, capturing **300** bag paths: six empty
bags and **294** nonempty descriptor sets containing **864** descriptors.
All 568 non-null value-type object references resolve to paths. Another
160 target exports yield no bag row; the probe does not distinguish absent
properties from wrappers exposing no bag. There are **zero read failures**.
With the target's version-3 flag default,
the six empty bags reproduce the existing empty-bag owner
`PropertyBag_2d06800538d394c2`. No nonempty bag matches any of the 321 mapped
bag owners, and none matches the 36 unresolved owners. This bounds those
specific serialized graph/instance fields; it does not establish the absence
of other PCG descriptor sources. Probe source, summaries, descriptors and
hash results remain in the outside-repository `pcg-serialized-probe/`
directory beneath the analysis path above. The unresolved count stays 53.

A separate target-SDK-backed source is
`PCGMetadataSettingsBase.DefaultValues.PropertyBag`: the SDK exposes
`DefaultValues` at settings `+0x118` and the nested `PropertyBag` at
container `+0x50`. Local UE 5.7 source corroborates both as serialized
UPROPERTY fields; that different engine CL alone supplies no target types.
A fresh scan follows the target usmap's superclass chains for 18 mapped
classes including the base, loads all **107,181** packages and examines
**1,810,214** exports. It finds **102** target exports across six concrete
class paths: 46 omit `DefaultValues`, 23 contain it without `PropertyBag`,
and 33 yield nonempty singleton bags (**33 descriptors**). There are zero
malformed values, zero read failures and exit code 0.

The same target-validated descriptor hash yields **zero** matches against
all 321 mapped bag owners, including the 36 unresolved owners. No fills
are accepted. This bounds that exact nested field and mapped descendant
scope; it does not cover every PCG descriptor source. Probe source,
stdout/exit metadata, per-row hash results and descriptors remain outside
the repo at `E:/Reverse_Engineer/wardogs_analysis/round8_pcg_defaultvalues_20261019/`.
