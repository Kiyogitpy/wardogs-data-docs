---
title: Round 8 rejoin inventory and loadout restoration
nav_exclude: true
---

# Rejoin restoration is distinct from saved-preset selection

Static CL-516586 SDK, corpus and original executable inspection identifies a
concrete inventory/loadout persistence path. It copies current player-state
data into a duplicate and later restores it. No game process was executed.

## Named native setting and duplicate source

Native registration `0x12BE410` supplies the name
`WD.Player.EnablePlayerRestoreInventory` (`0xB3DA430`) and help text describing
inventory snapshot restoration for rejoining (`0xB3DA3C0`). Instruction
`0x12BE423` passes the address of boolean `0xCEC9878`; its initial executable
byte is 1. This is the static initial setting, not an assertion that config
or later runtime changes cannot alter it.

The freshly extracted packed `Wardogs/Config/DefaultEngine.ini:314` also sets
`WD.Player.EnablePlayerRestoreInventory=1`. Its SHA-256 is
`77412ce15622d61548a9b4298cc5202c55205723bb5993b0fe106b16b3592aba`.
Thus the inspected shipped config agrees with the native enabled default;
later overrides and a particular client's runtime state remain conditional.

Player-session vtable slot 252 points to `0x6DAD330`. Its first call
(`0x6DAD33A`) reaches the parent at `0x6D655E0`, which calls the base
player-state function `0x42C26E0`. The base creates a new same-class actor
and dispatches property copying: original instructions `0x42C2742` and
`0x42C275F` implement the spawn and virtual copy calls. This matches the
`APlayerState::Duplicate()` role in the local UE 5.7.4 source
(`Engine/Private/PlayerState.cpp:372`); that different source CL is supporting
context, while the game instructions establish the observed operations.

The session override checks the restore setting at `0x6DAD4F7`; false skips
the inventory-copy block. With the setting enabled and the other validity
checks satisfied, it copies the snapshot at `+0x5F0` to the new session.
At `0x6DAD5A4`, helper `0x6DA8200` looks up
`/Script/WDGame.WDEconomyComponent` through component lookup slot 231.
Getter `0x1CC7300` is exactly `lea rax,[rcx+0x1E8]; ret`; it addresses the
second array inside `FWDPurchaseHistory` (component `+0x1D8`, inner `+0x10`). That array is copied
into duplicate session `+0x640`. Getter `0x6B2F0C0` is exactly
`lea rax,[rcx+0x218]; ret`; the copy at `0x6DAD622`–`0x6DAD689` transfers that
component's `FWDLoadout.Slots` into duplicate session `+0x650`, using 0x48-byte
entries. Thus this session loadout comes from the current economy component,
not an identified custom saved-preset store.

## Restore RPC and metadata replacement

The SDK declares parameterless `AWDPlayerStateSession::Server_RestoreInventory`
as a private, reliable server RPC. Its reflected thunk at `0x69E1390` dispatches
through the object's vtable `+0x8A0` (slot 276), whose implementation is
`0x6DB0920`.

The implementation passes the session's `InventorySnapshot +0x5F0` to
`0x6B63070` at `0x6DB09B5`, then clears/releases the snapshot. After further
processing, it again looks up the economy component through `0x6DA8200`.
At `0x6DB0A84` it calls `0x6B29C30(component, session+0x640, session+0x650)`.

Original instructions in `0x6B29C30` assign the supplied array into the
purchase-history subfield `+0x1E8` and the separate anonymous array `+0x208`,
and assign the supplied loadout into component `+0x218`
via `0x6B25700`. The SDK identifies `+0x218` as its replicated `FWDLoadout`.
This proves replacement of that component's loadout metadata in this restore
path. That metadata assignment alone does not clear equipment; the separate
snapshot-map operation below does replace the target inventory map. The
session's temporary arrays at `+0x640/+0x650` are
then cleared/released by `0x6DB0A89` onward.

The snapshot call at `0x6DB09B5` also establishes map replacement on the
inventory component itself. In `0x6B63070`, the destination is
`component+0x390` (`0x6B630A0`), which the SDK identifies as
`UBHInventoryComponent.InventoryMap`. The restore caller obtains this target
through `0x53CAE20`, whose raw instructions return pawn `+0x758`; the SDK
identifies that field as `AWDMoverPawn.PlayerInventoryComponent`
(`WDGame_classes.hpp:14001`), of type `UWDPlayerInventoryComponent`.
The helper returns early when snapshot dwords `+0x08` and `+0x34` are equal
(`0x6B63082`–`0x6B6308E`), and skips assignment when source and destination
are the same address (`0x6B630AF`–`0x6B630B2`). On the distinct-map copy path,
the routine calls `0x678D830` on that
map with the snapshot entry count (`0x6B630CD`–`0x6B630D6`). That helper first
destroys the existing element range through `0x678CEA0` (`0x678D83A`–
`0x678D845`), resets/resizes the map storage, and the caller rebuilds entries
from the snapshot. The 0x110-byte entry stride matches the key plus
`FBHItemSlot` value layout; the SDK places `FBHItemSlot.OwningInventory` at
value offset `+0xF0` (`BHInventory_structs.hpp:296-302`). The observed native
path therefore replaces `InventoryMap` from the snapshot, rather than merely
merging snapshot entries into the old map. Later per-slot processing invokes
component virtuals, including the callback at `0x6B63582` through vtable
offset `+0x568` (slot 173). Its full callback effects beyond map copying have
not been reviewed here.

## Client initialization and the restore request

The session's vtable slot 241 is `0x6DAB640`, which first calls its parent
`0x6D62920`. The corresponding base player-state implementation at
`0x42BBF10` dispatches `SetOwner(C)`; the local UE source identifies that base
operation as `APlayerState::ClientInitialize(AController*)`
(`Engine/Private/PlayerState.cpp:175`). This source cross-check identifies the
role; the original instructions below establish the actual game flow.

With the restore CVar enabled (`0x6DAB6D8`), the session creates a delegate
whose callback is `0x6DAB950` (`0x6DAB775`–`0x6DAB77C`) and a condition object
with vtable `0xB3DB980`. Its predicate slot points to `0x6DAD280`. The supplied
controller is retained in the condition. The world helper `0x6A78110` obtains
`BHUtils.BHAwaitSubsystem` (class registration `0x472B820`), and
`0x6DAB8E6` submits the delegate/condition through `0x472EC10`, storing its
handle at session `+0x660`. The subsystem can execute a ready condition or
retain it for later processing; this is not a fixed-delay claim.

The predicate requires a valid controller and its pawn at `+0x2F8`
(`Engine_classes.hpp:14051`), a valid `AWDMoverPawn` class match, and a valid
player inventory component. It then compares that component's
`ActiveQuickSlot +0x5A0` (`WDGame_classes.hpp:3254`) with shared sentinel
`0xD2692F8` and succeeds only when they differ (`0x6DAD30A`–`0x6DAD318`).
This is a specific readiness predicate, not proof that every spawn-grant task
or replication operation has completed.

Callback `0x6DAB950` clears the handle at `+0x660`, then tail-jumps to
`0x69DF600` at `0x6DAB99A`. That wrapper resolves FName global `0xD35B0C0`,
whose initializer `0x12527C0` supplies `Server_RestoreInventory`, and invokes
the reflected function through `ProcessEvent` (`vtable+0x260`). Thus the
observed initialization/wait callback invokes the named server RPC via
`ProcessEvent`; the server
implementation still performs its own pawn/component validity checks.

## Boundary

This names the rejoin setting, identifies the duplicate's loadout source,
and connects a client initialization/wait callback to the restore RPC,
player inventory-map replacement, and component metadata replacement.
Later per-slot/server processing prevents treating the map-copy operation
as proof of every final physical item or container state.
It does not establish a custom saved-preset source, an initial
spawn default-grant hook, or ordering of those operations against defaults.
The separate [apply-loadout purchase classifier](round8-loadout.md) and
[cooked-import audit](round8-loadout-imports.md) must not be conflated with it.

SDK field anchors: `WDGame_classes.hpp:9995` (economy loadout),
`:15967-15969` (session snapshot, auxiliary array, loadout), and `:16014`
(restore RPC); `WDGame_functions.cpp:20835-20848` supplies the RPC flags.
Important offsets and call edges above were checked directly in the restored
executable, SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
