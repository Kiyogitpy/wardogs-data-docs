---
title: Round 9 underbarrel activation boundary
nav_exclude: true
---

# Underbarrel: the shipped default activation path is unbound

Offline CL-516586 research, 2026-10-19. The named
`IA_Weapon_ToggleAncillaryFire` / **H** mapping does not have an executable
binding through the verified M4/default weapon-input configuration. The
test launcher supplies attachment data, but no replacement input extension
or action. No underbarrel firing component, owner or projectile source tag
is established. Assigning either the attachment id or the host weapon's
damage tag to a hypothetical shot remains unsupported.

This is a positive trace of a named shipped activation path, not a claim
that every possible native or dynamically modified path is absent. It gives
the original weapon-tag question a scoped disposition: **unsupported for
the shipped test attachment through the verified default input path**.

## Actual host and attachment configuration

Fresh cooked exports of `/Game/Items/ItemExtensionDefaults/B_DefaultWeaponInputData`,
`/WEPN_002/Data/ID_M4`, and `/UnderbarrelGrenadeLauncher/Data/GrenadeLauncher`
each completed with `ok=1 fail=0`, mounting 32 VFSs / 149,124 files.

The M4's `WDInventoryFragment_ItemActor.ExtensionDataFragments` explicitly
selects its instanced `B_DefaultWeaponInputData_C_0`. Its template is
`Default__B_DefaultWeaponInputData_C`; that class directly derives from
native `WDItemExtensionData_Input`. The default selects `IMC_BaseWeapon`,
whose H mapping was established in [Round 8](round8-ancillary-sights.md).
The host has an `Item.Attachment.Underbarrel` container: its BlockPriority
filter allows that context and blocks `Item.Attachment.Bipod.Attached`.
The launcher's sole item-context tag is `Item.Attachment.Underbarrel`.
This establishes a concrete host configuration to inspect; it is not a
runtime attachment or successful firing observation.

The default contains all 12 configured `InputBehaviors` entries. They cover
reload, secondary-use press/release, melee bash, primary use, cycle sights,
cycle fire mode, increase/decrease zeroing, inspect, fold bipod and mount
bipod. Its one alias maps `CycleSightsKeyboard` to `CycleSights`. The M4
instance replaces the behavior map with 14 entries, adding primary-use
release and discard reload. It inherits that one alias. Neither map nor
alias contains `ToggleAncillaryFire`. The ordinary primary-use behavior
positively selects `Action.Weapon.Fire`.

The launcher's complete `DataFragments` array has six entries: user
interface, attachment, gunsmith, subslot support, itemsmith camera, and
audio. It contains no ItemActor fragment, input extension data or action
extension. Its ancillary attachment has empty `AppliedEffects` and
`AppliedCharacterEffects`, null `AnimationSet`, and no attached/detached
audio event. Thus none of those configured additions supplies a binding.
Its `WeaponStats` reference remains data, not proof of a firing owner.

## Native binding and lookup

These claims were independently checked against restored executable
instructions, including the small resolver omitted from the corpus.

| Stage | Exact evidence |
|---|---|
| Select the extension's own data | `0x4BD0D20` returns extension `+0xE0`; setup and callback pass it through native Input-data cast `0x6C74730` |
| Empty native baseline | Constructor `0x6C763C0` clears the InputBehaviors map at `0x6C763FE`–`0x6C76431`, aliases at `0x6C76437`–`0x6C76473`, and Actions at `0x6C764BB`–`0x6C764F7`; omitted cooked maps do not conceal native default bindings |
| Bind configured behaviors | Setup `0x6C7AC30` enumerates `InputBehaviors +0x58` starting at `0x6C7B342`; it resolves each configured input tag and trigger event, then calls binding helper `0x6C745F0` at `0x6C7B481` |
| Bind configured aliases | The following setup loop enumerates the alias map at `+0xA8`, obtains the target behavior's trigger events, and calls the same binding helper at `0x6C7B74D` |
| Resolve an incoming behavior | Callback `0x6C7C410` reads the `BHInputAction.InputTag +0x78` at `0x6C7C47A` and calls `0x6C78F90` at `0x6C7C481` |
| Exact lookup, including aliases | `0x6C78F90` first looks in data `+0x58`; on a miss it looks in `+0xA8`, then looks up that alias value in `+0x58`. Calls are at `0x6C78FAB`, `0x6C78FC4`, `0x6C78FD5`; missing/invalid entries return null at `0x6C79001`–`0x6C7900D` |
| Exact tag comparison | Map helper `0x4D053E0` compares the complete tag identity at `0x4D05446`; this is not a parent-tag fallback |
| Third, direct Actions route | Setup also enumerates `Actions +0x148`. At `0x6C7B953`–`0x6C7B995` it loads each `FWDActionSetup.InputAction`, reads its InputTag `+0x78`, resolves the input action and binds it. Both the default and M4 omit Actions, inheriting the verified empty native baseline |
| Action admission | `0x6C7CDE0` looks up the requested action in `Actions +0x148` at `0x6C7CE9A`–`0x6C7CEAC`; a miss returns the literal reason `Action doesn't exist inside Actions map` |

The resolver's complete unwind range is `0x6C78F90`–`0x6C7900E`
(exclusive end, `0x7E` bytes). This makes the conclusion stronger than a
search for the ancillary spelling: the configured sources and the actual
lookup/registration rules are known. The H mapping alone supplies none of
the required entries for this path.

As a separate coverage cross-check, all 87 serialized `InputBehaviors`
maps in the checked-in data exports were decoded without JSON errors:
40 `B_DefaultWeaponInputData_C` instances and 47 native
`WDItemExtensionData_Input` objects. None has an ancillary key. This is
bounded to the exported data corpus, not every cooked Blueprint class or
possible runtime edit. The fresh default, M4 and launcher exports carry the
concrete configuration proof above.

## Complete attachment primary vtables

The ancillary primary table at `0xB364600` has three contiguous executable
entries: deleting destructor `0x6C41D20`, addition callback `0x6C42240`,
and removal callback `0x6C422B0`. Its next QWORD, at `+0x18`, is literal
`0x405`, not another code pointer. The base table at `0xB130890` likewise
has three entries: destructor `0x69A18D0` and those same two callbacks;
its next QWORD is null.

The complete ancillary destructor (`0x6C41D20`–`0x6C41D9D`) destroys
container storage and conditionally frees the `0x148`-byte object. The base
destructor uses size `0x50`. There is no further ancillary-specific firing
slot in this primary table. The two shared callbacks' generic audio and
animation behavior was already established in Round 8. This closes the
previously unexamined primary-vtable lead without inferring a weapon owner.

## Provenance and limits

Read-only corpus:
`E:/Reverse_Engineer/wardogs_analysis/decompiled_cl516586_20261017_mmvpuc__/corpus.sqlite`.
Restored executable SHA-256:
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
No game process, server, service, debugger session or IDA database was opened.

New raw exports, summaries and disassembly are retained outside the checkout
under `E:/Reverse_Engineer/wardogs_analysis/round9_underbarrel_20261019/`:
`binding_summary.json`, `cooked_default/`, `cooked_m4/`,
`cooked_attachment/`, `input_binding_disasm.txt`,
`input_helpers_disasm.txt`, and `vtables_and_constructors.txt`.
The setup range is `0x6C7AC30`–`0x6C7BA54` (`0xE24` bytes), callback
`0x6C7C410`–`0x6C7C58D` (`0x17D`), native data constructor
`0x6C763C0`–`0x6C7652A` (`0x16A`), and action admission
`0x6C7CDE0`–`0x6C7DAF1` (`0xD11`).
The callback's corpus/unwind end includes one trailing `0x48` byte after
its return instruction: Capstone decodes `0x17C` bytes through exclusive
`0x6C7C58C`. The other four reported ranges decode to their listed ends.
`verify_evidence.py` rechecks the executable digest, table entries, cooked
configuration counts and these decoding boundaries; `verification.json`
records its successful assertions and the raw export digests.

This evidence does not establish arbitrary alternate native creation,
external mutation of configured maps, another host's behavior, future
build support, or a successful ancillary shot. If a concrete alternate
activation/factory path appears, preserve its component owner through
`IWDWeaponOwner +0x70` into projectile-record writer `0x6B72030` before
assigning a source weapon tag.
