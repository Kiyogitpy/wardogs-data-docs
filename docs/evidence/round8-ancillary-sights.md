---
title: Round 8 ancillary ownership and sight multiplier trace
nav_exclude: true
---

# Ancillary ownership and sight multipliers

Static CL-516586 research, 2026-10-18. The read-only decompilation corpus,
restored executable and local CppSDK were used. Important statements below
were independently checked against executable instructions with Capstone.
No game process, service, debugger session or IDA database was opened.
The verified sight path was also integrated into Weapons §5b.

## Underbarrel weapon tag: historical investigation

The [Round 9 continuation](round9-underbarrel.md) establishes a scoped
unsupported disposition for the shipped test attachment on the verified
M4/default-input path. Its selected input maps contain no ancillary binding;
the exact resolver returns null. The earlier negative searches below are
preserved as history, not the basis of that conclusion. An alternate firing
owner and shot tag remain unproved.

The actual ancillary `UWDWeaponComponent` creation and its `IWDWeaponOwner`
have still not been established. Consequently this investigation does not
assign either the attachment id or the ordinary host weapon's damage tag
to an underbarrel shot. The known projectile-record writer `0x6B72030`
cannot answer that question without the component's actual owner.

The bounded negative checks were:

- SDK-wide searches expose `FWDAncillaryAttachedWeaponData` (size `0x148`,
  stats pointer `+0x50`), but no class or callable API containing
  `Ancillary`. This is a naming search, not proof that the feature is absent.
- Native reflected struct getter `0x6C43790` registers
  `WDAncillaryAttachedWeaponData`; disassembly checks its lazy struct
  registration and global `0xD36D6B8`. The read-only corpus has no indexed
  caller to this getter. Searching executable sections for relative
  `E8`/`E9` byte candidates to it also returned zero. Indirect references,
  reflection and Blueprint bytecode remain possible.
- Corpus FTS queries for the struct name and its getter/global find only
  that registration; `ToggleAncillaryFire` and `AncillaryFire` have no
  indexed body hit. No absence claim about omitted functions follows.
- The previously exported normal fire and reload Blueprint listings in
  `round8_weapon_context_20261018` contain no `Ancillary`, `Underbarrel`
  or [`GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) spelling. The available action-asset listing has
  normal weapon, cycle-sight and vehicle actions, with no named ancillary
  action. These listings are bounded evidence, not an exhaustive cooked
  reference index.

### Native virtual lifecycle: generic callbacks, no ancillary factory

Following the reflected struct's dynamic construction resolves an
important path that a direct-call search misses. Struct registration
`0x6C459A0` uses descriptor `0xCEBE200`, whose C++-ops allocator is
`0x6C421C0`. It advertises size `0x148` and construct thunk
`0x6C42E40`, which jumps to actual ancillary constructor `0x6C44080`.
That constructor installs vtable `0xB364600` (`0x6C440AB`–`0x6C440B2`).
Its lifecycle methods at `+0x8` / `+0x10` are `0x6C42240` /
`0x6C422B0`. Both are the same methods used by base-attachment vtable
`0xB130890` (base constructor `0x6C41F80`).

The ranged extension's attachment-update function `0x6C9D170` obtains
the attachment fragment, validates its instanced struct against
`FWDBaseAttachmentData` through `0x6C904B0`, and makes these virtual
calls: removal at `0x6C9D6DE`–`0x6C9D6EB` dispatches `+0x10`; addition
at `0x6C9DCFF`–`0x6C9DD0C` dispatches `+0x8`. These are actual native
consumers of the polymorphic attachment data.

However, the two ancillary callbacks only use base fields. Addition
reads attached audio at `+0x40` and animation set at `+0x38`; removal
uses the attachment type `+0x8`, detached audio `+0x48` and animation
set `+0x38`. `0x6C45690` emits the audio event, while `0x6C43F60`
resolves `WDItemExtension_Animation`; `0x6C61040` / `0x6C613B0` add/remove
the animation set. The complete callback instructions were checked.
Neither reads ancillary `WeaponStats +0x50`, creates a weapon component
or supplies a different `IWDWeaponOwner`. The lifecycle path therefore
does not establish a functioning ancillary shot.

For comparison, the ordinary ranged extension really does create its
single exposed weapon component: primary vtable `0xB389548`, slot 110,
dispatches `0x6C99FA0`. It requests `WDWeaponComponent` and calls
`0x675BB50` at `0x6C99FFF`, then stores the result in extension `+0x128`
at `0x6C9A047`. The underlying `0x675BB80` supplies the extension as
the NewObject outer (`0x675BD43`) and registers the component. This
explains the ordinary owner relationship, but there is no ancillary
factory or second component in this callback. It must not be promoted
to evidence that the ancillary shot shares that owner.

### Cooked input and interface-reference search

The exported [`IMC_BaseWeapon`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IMC_BaseWeapon.json) maps [`IA_Weapon_ToggleAncillaryFire`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Weapons/Input/IA_Weapon_ToggleAncillaryFire.json) to
**H**, and the input action sets
`Input.NamedActions.HoldableItem.Weapon.ToggleAncillaryFire` with a
pressed trigger. That verifies the input mapping, not an executable
fire-action binding. A fresh `findname` query under
[`Wardogs/Content/GameMechanics`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/GameMechanics) for `Ancillary` finds only the settings
keybinding table.

Two broader offline `findname Wardogs ...` scans of the mounted cooked
packages find no name-map references to `WDAncillaryAttachedWeaponData`
or `WDWeaponOwner`. Outputs were retained outside the checkout in
`round8_ancillary_structrefs_20261019` and
`round8_weaponowner_bprefs_20261019`; the scoped input search is in
`round8_ancillary_bindings_20261019`. Each command mounted 32 VFSs /
149,124 files and reported zero matching packages for the two type
names. This finds no additional explicit Blueprint interface
implementer by name. It does not exclude inherited native implementers,
unversioned serialized type information or references absent from a
package's name map.

The later [global script-import and interface audit](round8-weaponowner-imports.md)
supersedes the name-map search's coverage limit. All 107,181 packages and
1,230,571 script imports were inspected, with every script import resolved
and no package failures. Fifteen packages import `WDWeaponOwner`, but none
of their class exports directly implements it; the sole ancillary-struct
importer is the data-only grenade-launcher asset. This still does not identify
an ancillary factory or firing consumer.

The remaining lead is a concrete consumer of the ancillary `WeaponStats`
field or an actual fire-action binding beyond the verified H mapping.

The native attachment-type tag provides another bounded search route.
Initializer `0x129E870` registers `Item.Attachment.Underbarrel` at
`0xD36C2A8`. A corpus search for that global finds 15 indexed functions,
including the initializer and ancillary constructor. The other references
were classified as bipod state, animation, camera/movement modifiers or UI;
none supplies a firing consumer or weapon-component factory in those bodies.
For the concrete update at `0x6C9F6E0`, independently decoded instructions
load the tag at `0x6C9F72F`, call attachment lookup `0x6C97840` at
`0x6C9F745`, and gate the result against getter `0x69A0F80` at
`0x6C9F76B`–`0x6C9F78E`. Its native literal is **WDBipodAttachmentData**,
not the ancillary struct. Thus an Underbarrel-tag reference alone is not
evidence of grenade-launcher behavior. This search covers indexed global
references, not every possible indirect/unindexed consumer.

The later [IoStore import audit](round8-weaponowner-imports.md) resolves
script imports directly, rather than relying on local name maps. Across
107,181 successfully loaded packages, only the grenade-launcher data asset
imports `WDAncillaryAttachedWeaponData`; it has no Blueprint class export.
This further bounds the missing consumer but does not prove native code
cannot access its data indirectly.

A separate read-only scan of executable RIP-relative pointer loads/stores
and addresses found references to the struct singleton `0xD36D6B8` only
inside getter `0x6C43790` (instructions `0x6C43794` / `0x6C437BB`).
Readable non-code sections contain no ASCII or UTF-16 spelling of
`ToggleAncillaryFire` / `AncillaryFire`, while both spellings of the struct
name are present. These bounded negative results do not turn the data-only
test attachment into a verified firing feature or justify assigning the
host weapon's damage tag to a hypothetical shot.

The native polymorphic attachment lifecycle is now traced and supplies
only generic audio/animation work. If another creation path is found,
preserve its component outer/owner through `IWDWeaponOwner +0x70` into
`0x6B72030`. The ordinary ranged extension's shared damage component
remains conditional evidence only; see [the previous owner trace](round8-weapon-context.md).

## Sight multiplier data path: resolved for native first-person sway

The two sight multipliers in [Weapons §5b](../../content/Wardogs_Weapons_v2.md#5b-aim-sway-and-focus-energy)
come from the selected sight's `FWDSightData.SightStabilizationOverrideMultipliers`.
The key is the first explicit tag in the held item's `ItemContext` that
matches the parent `Item.Archetype`. The map lookup itself is exact. Its
value contains translation at `+0` and rotation at `+4`.

This is an animation-side multiplier path. It does not select a damage
weapon tag, multiply projectile damage or change camera recoil. Despite
the field names mentioning a stabilization *curve*, each selected value
multiplies the already assembled translation or rotation sway vector,
after either the curve branch or its fallback branch. Thus it also scales
the preceding idle/offset contribution within that vector.

### Selected sight data

`0x6A80880` first resolves `HeldItemWeak` (anim instance `+0xC54`) and its
ranged extension (`0x6A77FC0`). It reads the sight entry of the anim
instance's `AttachmentMap +0x1740`, resolves that item definition through
`0x6790AF0`, obtains `WDInventoryFragment_Attachment`, and checks its
`FInstancedStruct` as `FWDSightAttachmentData` before retaining its data
pointer. SDK names and native registrations `0x6C41DA0` / `0x6C42430`
identify those two types. `0x129E730` identifies global `0xD36C280` as
`Item.Attachment.Sight`.

| Stage | Executable anchors and behavior |
|---|---|
| Resolve attached sight item | `0x6A80A33`–`0x6A80A7D`: `AttachmentMap +0x1740`, sight tag, map lookup, item-definition resolution |
| Validate attachment struct | `0x6A80A9D`–`0x6A80B4B`: attachment fragment class, struct pointer `+0x38`, data pointer `+0x40`, exact/inherited `WDSightAttachmentData` validation |
| Obtain current sight record | `0x6A80B61` calls `0x6C977B0(extension, output, attachmentData)` |
| Select attachment sight subrecord | `0x6C977C5`–`0x6C977E0`: exact FName lookup in attachment `SightsData +0x50`, using extension field `+0x440`, then copy `0x6C442A0` |
| Fallback if the attachment/key has no record | `0x6C977F3`–`0x6C9782A`: copy extension's cached socket record (`+0x438`) at record `+0x88`; otherwise construct default `FWDSightData` (size `0x418`) |

This is selection with fallback, not field-by-field merging. `0x6C168F0`
compares the complete FName key and returns the value of the matching
`SightsData` pair. The extension's cached socket entry is selected from
its FName map at `+0x3E8` by `0x6C96FB0`; initialization and attachment
updates assign `+0x440` and `+0x438` in `0x6C9AFB0` / `0x6C9D170`.
The complete timing and socket-cycling state machine was not re-derived
here; the consumer's selection and fallback are directly established.

### Archetype key and gates

`0x2F691E0` returns the held item's `ItemId +0x328`. The consumer resolves
the corresponding definition and filters its `ItemContext +0x38` using
the native parent `Item.Archetype` (`0xD36C410`). Registration
`0x129F4F0`, including the executable's ASCII string at `0xB352748`,
independently identifies this parent.

`0x395A040` walks the source's explicit tag array in order, retains tags
passing `0x395D260` and appends those original tags to the output. The
latter resolves the individual tag's cached container and calls
`0x395BE30` against the parent query container. The consumer chooses the
first resulting explicit tag (`0x6A80D38`–`0x6A80D49`), or an empty tag
if none exists. This does not select an arbitrary key by prefix from the
sight's multiplier map, and it does not combine several archetype rows.

| Gate/use | Executable anchors |
|---|---|
| Default both values to 1 | `0x6A80C92`–`0x6A80CB4`, `xmm13` translation and `xmm15` rotation |
| Require valid sight attachment data | `0x6A80D50`–`0x6A80D53` |
| Require selected record's `bOverrideWeaponSwayStabilizationData +0xE0` | `0x6A80D55`–`0x6A80D5C` |
| Exact key lookup in selected `SightStabilizationOverrideMultipliers +0xE8` | `0x6A80D5E`–`0x6A80D72`; helper `0x4D053E0` uses full 64-bit key equality at `0x4D05446` |
| Read translation / rotation | `0x6A80D74` / `0x6A80D79`: float `+0` / `+4` |
| Translation use and stabilization gate | `0x6A81007`–`0x6A81022`: if stabilization fraction is not positive, replace translation multiplier by 1; otherwise multiply both assembled coordinates |
| Rotation use and stabilization gate | `0x6A8127D`–`0x6A81298`: same gate and multiplication for rotation |

The stabilization fraction is the previously documented `1 - clamped
remaining/time` value, computed at `0x6A80E29`–`0x6A80E58`. The sight
multiplier is therefore inactive at fraction zero and active once the
fraction is positive; there is no additional interpolation of the sight
multiplier by that fraction in these instructions. Subsequent behavior
attributes, vector-length limits and smoothing still apply.

The valid attachment-data gate matters: although `0x6C977B0` can return
fallback socket/default sight data, missing or invalid `WDSightAttachmentData`
still leaves these two multipliers at 1 in this consumer. A missing exact
archetype row or a false override flag also leaves both at 1.

### Cooked examples

The reviewed export records corroborate meaningful, non-unit values:

| Sight asset / `SightsData` record | Override | Exact archetype key | Translation | Rotation |
|---|---|---|---:|---:|
| [`SGHT_034/Content/Data/ID_SGHT_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_034/Content/Data/ID_SGHT_034.json), record 0 | true | `Item.Archetype.Sniper` | 1.2 | 1.2 |
| [`SGHT_030/Content/Data/ID_SGHT_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_030/Content/Data/ID_SGHT_030.json), record 0 | true | `Item.Archetype.Sniper` | 1.3 | 1.3 |
| [`SGHT_030/Content/Data/ID_SGHT_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/SGHT_030/Content/Data/ID_SGHT_030.json), record 1 | false | empty map | 1 (fallback) | 1 (fallback) |
| [`/Game/Items/Attachments/Sights/10x_Scope/ID_10xScope`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Attachments/Sights/10x_Scope/ID_10xScope.json), record 0 | true | `Item.Archetype.Sniper` | 1.7 | 1.6 |

The SGHT assets are under
[`data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Sights); the legacy
10x asset is under [`data/Wardogs/Content/Items/Attachments/Sights/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Items/Attachments/Sights).
Only the selected socket record participates. These examples do not claim
that every weapon can equip each sight or that the legacy 10x asset is
selected in a shipping loadout.

## Reproduction and remaining boundaries

Use the read-only `corpus_q.py body` helper on `0x6A80880`, `0x6C977B0`,
`0x6C168F0`, `0x4D053E0`, `0x6C96FB0`, `0x129E730` and `0x129F4F0`.
The omitted engine helpers `0x395A040`, `0x395BAF0` and `0x395D260`
were read directly from the executable, together with the exact consumer
instruction ranges tabulated above. The auxiliary disassembler was run
with `python -I` against the restored executable; the target was never
executed. Cooked multi-export JSON was parsed per export, retaining only
the named scalar fields summarized here.

The native sight-multiplier source/selection/gating/use question can be
closed. The ancillary owner question and the separate reader of recoil
accumulator `+0x3D0` remain open. Neither is answered by this animation
trace. The global import audit above covers the mounted package set's explicit
script imports and direct interface references; arbitrary implementation
behavior outside the examined action listings remains untraced.

> **Round 19 re-verification.** Evidence level: static-analysis image; virtualized dispatch not removed. Function `0x395BE30` begins with a protection-layer dispatch stub in the static-analysis image (`mov reg,[rip+x]` then `jmp [reg+disp]` through a runtime-filled global table, so its target is not statically resolvable); the older reference image holds the plain body, and it is the explicit-or-cached-parent membership test described above. Classification: unaffected by the stub.
