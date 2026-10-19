---
title: Round 8 Deathmatch loadout RPC
nav_exclude: true
---

# Deathmatch loadout item and magazine attempts

Static CL516586 evidence from `WardogsClient-Win64-Shipping.restored.exe`
(SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`),
the matching SDK, and reviewed cooked Deathmatch assets. Addresses are
executable RVAs. This is a Deathmatch Game Feature path, not evidence of a
universal first-spawn or saved-preset grant.

The cooked `/Deathmatch/Deathmatch` feature's `GameFeatureAction_AddComponents`
adds `WDDeathmatchWeaponSelectionComponent` and
`WDLoadoutAmmoGenerationComponent` to `WDMoverPlayerCharacter`, with both
client and server component flags set. This registration depends on that
feature's activation. The SDK exposes
`WDLoadoutAmmoGenerationComponent.Server_SetupLoadoutByTag` with an `ItemTag`
reference and `AWDPlayerStateSession* PlayerState` argument
([class](../../sdk/raw/DeathmatchRuntime_classes.hpp#L372),
[parameters](../../sdk/raw/DeathmatchRuntime_parameters.hpp#L29)).

The reflected function trampoline `0x84966B0` dispatches through virtual
offset `+0x4F8`. The component constructor at `0x848B6A2` installs
vtable `0xBA278D0`, whose `+0x4F8` entry is `0x8495620`. In this
native handler, a non-null, live `PlayerState` is required. It obtains
a pawn reference through `0x42C83D0` and `+0x2F8`, requires that pawn
to be a live `WDMoverPlayerCharacter` (`0x8495669`–`0x8495694`),
and gets its `PlayerInventoryComponent` through the pawn's `+0x758`
getter `0x53CAE20` (`0x84956A2`). The SDK also places that player
inventory pointer at `+0x758`.

With a valid inventory, `0x84956E4` calls native
`UBHInventoryComponent::AddItemToInventory` (`0x6783E30`) using the
supplied `ItemTag`, addition context `2` (**Bought**), amount **1**,
slot-search option `0` (**All**), and a null final inventory-component
argument. The handler then looks up the
item definition (`0x6791030` at `0x84956EF`), obtains its setup data,
and searches for the tag registered as `Item.Attachment.Magazine`
(registration `0x129E190`, lookup `0x84957E7`). The lookup searches
the resolved item's `BHInventoryFragment_SubSlotSupport.Containers`
array (`0x67762D0`, `0x6790750`). If a matching `FBHContainerSetup`
exists, it reads the first tag from that setup's `DefaultItems`
container at `+0xE0` when nonempty (`0x84957F5`–`0x8495805`), otherwise
uses a zero-valued tag (`0x849580A`–`0x8495811`). It calls
`AddItemToInventory` again with context **Bought**, amount **4**,
search option **All**, and a null final component at `0x849582A`.
The second tag's concrete identity
depends on the selected item data. The handler does not use the first
add's return value to gate the later lookup, so these are attempts,
not proof of successful grants.

The Deathmatch weapon-selection component's `OnRegister` hook
`0x8490790` binds `0x8495F50`, which reaches the weapon-select scene.
The selection-to-RPC path is traced below. The full cooked script-import
audit found no import of `Server_SetupLoadoutByTag`; this native path
explains how a UI selection can invoke it. No inference about the
normal player loadout follows from this mode-specific handler.

The feature asset was freshly exported without failures on 2026-10-19;
raw JSON remains outside the repo under
`E:/Reverse_Engineer/wardogs_analysis/round8_spawn_loadout_20261019/deathmatch/`.
Both inventory call sites and the `DefaultItems` offset were independently
checked against original executable instructions and the matching SDK.

## Weapon-selection click callback reaches the RPC

The `WDUIDeathmatchWeaponSelectItemWidget` has `SelectionButton` at
`+0x548` and `WeaponSelectItemViewModel` at `+0x550` in the SDK. Its
virtual slot 161 points to `0x84941B0`; after validating those objects,
this function registers callback `0x8494AA0` on the button's
`+0x1460` delegate through `0x250B310` at native `0x8494254`.
The original native button path now identifies `+0x1460` as the click event.
`UWDUIButton` vtable slot 183 resolves to `0x756E790`, whose call at
`0x756E826` reaches CommonButtonBase's corresponding implementation
`0x4DB4150`. That base function broadcasts `this+0x1460` through the
native multicast helper at `0x4DB4188`–`0x4DB418F`, then separately broadcasts
the SDK-named `OnButtonBaseClicked` at `this+0x4B0`. The reflected
`HandleButtonClicked` thunk `0x4DD62A0` dispatches slot 168 (`+0x540`);
its handler `0x4DAAD40` calls slot 183 (`+0x5B8`) on the click path and
handles selection state separately. Local CommonUI source labels the
slot-183 operation `NativeOnClicked` and its event `OnClicked`; native
instructions establish the target's exact broadcast offset. This resolves
the earlier SDK-only ambiguity, since the SDK omits the `UWDUIButton`
definition and leaves this native event in opaque padding.

The traced route is therefore click-to-RPC, not evidence that merely
selecting a list entry fires it. An automatic or programmatic click at pawn
spawn has not been established.

At `0x8494AE1`–`0x8494B25`, the callback resolves and validates a
`WDUIDeathmatchWeaponSelectItemListEntry` from the view model. It
obtains an `AWDPlayerStateSession` through `0x6FC4AF0` (`0x8494B33`;
the helper checks class getter `0x69DCFD0`) and validates that state's
`+0x330` pawn reference as `WDMoverPlayerCharacter`. Through that
character's component-finding virtual call and class getter
`0x8488C70` (`0x8494B9F`–`0x8494BCE`), it obtains the
`WDLoadoutAmmoGenerationComponent`. It then packs
`*(list entry+0x28)` and the player state into the RPC argument pair
and broadcasts the component's `+0xE0` delegate through `0x18FCDB0`
at `0x8494BE6`–`0x8494C00`. That generic broadcaster dispatches a
bound `UFunction` with `UObject::ProcessEvent` virtual `+0x260`.
The component's registration override `0x8490B30` binds the named
`&ThisClass::Server_SetupLoadoutByTag` function into this `+0xE0`
delegate array (`0x8490B91`–`0x8490C4F`). This establishes a
conditional clicked-entry tag-to-RPC path; whether a particular invocation
passes network validation and inserts an item remains unobserved.

## Component registration requests the selection scene

The registration path's state and scene keys have native tag registrations:

| Global | Tag | Initializer / registration call |
|---|---|---|
| `0xD2D2AE0` | `MatchState.PreMatch` | `0x11DD840` / `0x11DD8B6` |
| `0xD3E27E0` | `MatchState.Playing.Deathmatch` | `0x14FDF80` / `0x14FDFF6` |
| `0xD3E2628` | `UI.Scene.Deathmatch.WeaponSelect` | `0x14FE0C0` / `0x14FE136` |

At `0x84907D4`–`0x84907EF`, `OnRegister` tests the PreMatch key through
`0x4D672B0`, which searches the match-state component's `ActiveStates`
at `+0x100`. When active, it registers callback `0x8495F50` for
Playing.Deathmatch through `0x4D62FD0` (`0x84908A2`–`0x84908C3`).
That helper also invokes the supplied delegate immediately if the requested
state is already active (`0x4D63000`–`0x4D6302A`), then stores the callback
in the map at `+0x120`. When PreMatch is inactive, registration calls
`0x8495F50` directly at `0x8490925`. These branches require the earlier
valid match-state component check; they do not run unconditionally on
every client or pawn.

The callback validates its pawn owner, controller type and resolved UI
object. It loads the WeaponSelect scene tag at `0x8495FF3`, then invokes
the UI object's virtual `+0x538` at `0x849601F`. The freshly exported
`/Deathmatch/UI/Scene/DT_DeathmatchSceneData_Match` has that exact row/tag,
selecting `W_DeathmatchWeaponSelectScene_C` and native
`WDUIDeathmatchWeaponSelectViewModel`. The feature's
`GameFeatureAction_DataRegistrySource_0` adds this table to
`UISceneData_Match`. The scene export succeeds **1/0**; raw output is in
the `scene/` directory beneath the registry analysis path below. Native
tag literals, registration branches and scene call were independently
checked from executable bytes.

This establishes the conditional registration/state-to-scene request.
It does not establish an automatic selection-button event or item grant,
nor resolve normal-player saved-preset ordering.

## Row source and registry binding

The scene entry builder `0x8495360` iterates a view-model collection
at `+0xE0`, creates `WDUIDeathmatchWeaponSelectItemListEntry` objects,
and copies each source record's `+0x08` gameplay tag into the entry's
`+0x28` at native `0x84954DD`–`0x84954E1`. The SDK names the `+0x08`
field `FBHGameplayTaggedTableRow.Tag`; `FWDDeathmatchWeaponData`
inherits that row type and has the variation array at `+0x10`.
The view model's initializer `0x8493E30` calls table lookup
`0x84938A0` at `0x8493FDE`. The lookup retrieves a table through
`0x46E9680` using global lookup key `0xD3E27B8` (`0x84938E6`),
checks the `WDDeathmatchWeaponData` row type, and collects rows.
Its completion chain `0x8492B10` -> `0x8491490` -> `0x848AE60`
updates the view-model collection at `+0xE0` (write at `0x848AF75`),
which the scene builder later reads.

### Exact registry-to-table binding

The key's native initializer `0x14FE480` loads the UTF-16 literal
`DeathmatchWeaponsData` at `0xBA243A0`, targets global `0xD3E27B8`
at `0x14FE487`, and tailcalls the eight-byte name initializer
`0x1725770`. The lookup loads this same global at `0x84938DF`.
`0x46E9680` searches the subsystem's sorted registry map at `+0x30`
using that eight-byte registry-type key and returns the entry's pointer
value (`0x46E968B`–`0x46E96C0`). The separate registered
`GetPossibleDataRegistryIdList` path at `0x46EF2E0` searches the same
map with a `FDataRegistryType` key. Local UE5.7
`DataRegistrySubsystem.cpp:211–220` corroborates the `GetRegistryForType`
operation; native instructions establish the target's lookup.

A fresh mounted-package export of
`/Deathmatch/Data/DataRegistry/DR_DeathmatchWeaponsData` has exactly
that `RegistryType`, `ItemStruct=WDDeathmatchWeaponData`, and one
`DataRegistrySource_DataTable` source. Both its `SourceTable` soft path
and `PreloadTable` reference select
`/Deathmatch/Data/DT_DeathmatchWeaponSelect`. This establishes the exact
configured registry-to-table binding. The table has 20 `Id.Item.*` rows,
including AK74M, M4 and Glock17; those are menu-source records, not items
automatically granted together.

The packed `DefaultGame.ini` scans `/Deathmatch/Data/DataRegistry`.
The earlier empty listing was a command-scope mistake: `WdExtract list`
matches a filename prefix, not a package-directory prefix. Listing
`DR_DeathmatchWeaponsData` finds the registry package above. Its fresh
dump reports **1 success / 0 failures**. The initializer and lookup
instructions, literal bytes and registry export were independently checked.
Raw listing and export remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_deathmatch_registry_20261019/`.

Registry availability, feature activation and precise menu-population
conditions remain conditional. The static source binding, registration/state
trigger for the scene request, and a populated entry's tag-to-RPC handoff
are established. An automatic selection event or first-spawn item grant
has not been established.
