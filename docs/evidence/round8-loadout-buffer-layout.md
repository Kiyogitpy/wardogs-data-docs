---
title: Round 8 vendor buffer application
nav_exclude: true
---

# Two native paths copy buffer state into pawn inventory

Offline CL516586 SDK, corpus and restored executable evidence identifies
two concrete buffer-to-pawn inventory copy paths. Executable SHA-256 is
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
The first three sections describe `Server_CommitVendorBufferLayout`;
the purchase-result callback is described separately below. Both follow
the [ApplyLoadout buffer-request investigation](round8-loadout.md).
No target process was executed.

## RPC and inventory identities

The reflected `Server_CommitVendorBufferLayout` exec at `0x69C0090`
dispatches through virtual `+0x518` at `0x69C00A8`. Economy slot 163
is `0x6B32A10`, which tail-jumps to `0x6B290C0`.
The helper requires a valid `WDPlayerState` owner and owner Role **3**
at `0x6B2912B` (Authority), plus valid controller and inventory objects.

Source getter `0x3661150` at `0x6B291A0` returns controller `+0x8A0`,
SDK `BufferStorageInventoryComponent`. The target is resolved from the
owner's pawn at `+0x330` through `0x6C1AFF0` at `0x6B291AF`.
That helper checks the pawn's class, then **tail-jumps** at `0x6C1B033`
to `0x53CAE20`, whose complete body returns pawn `+0x758`:
SDK `PlayerInventoryComponent`. The class check alone does not identify
the helper's returned object; its final getter does.

## Pending-cart and quantity gates

Before copying, the helper examines each buffer slot's replicated
additional data. `0x6B293A4` calls `0x6B2F050`, which finds exact type
`WDFragmentReplicatedData_CartPending` through getter `0x69C5E40` and
sums its `Amount +0x00`. A positive per-slot sum branches out at
`0x6B293AB`; it optionally calls `0x6B28CA0` before returning.
That path does not reach the layout copy.

With no positive pending amount, `0x6B2941E` and `0x6B2942A` call
`0x6B29FE0` for the buffer and pawn inventories. This builds summaries
keyed by each slot's last DataStack tag, accumulating its stack quantities.
Predicate `0x6B30800` first requires equal map-entry counts
(`0x6B30823`), then an equal value for every matching key
(`0x6B30936`–`0x6B3094E`). It returns true at `0x6B30976` only after
those checks. This is aggregate tag/quantity equality, not full metadata
or slot-path equality.

## Actual inventory copy

On equality, `0x6B29449` calls the target inventory's virtual `+0x4F8`
with the buffer as its source argument. The player-inventory constructor
installs vtable `0xB304E00`; slot 159 at `0xB3052F8` points to
`0x6B57910`. For a valid player-inventory source, its authority branch
runs WD equipment preparation `0x6B63B70` at `0x6B579B8`, then calls
the inherited copy routine `0x678BFB0` at `0x6B579C3`.

The base routine copies `ContainerSetup +0xE0` and `OccupancyMap +0x430`
and reconciles `InventoryMap +0x390` against the source. It inserts
source-only records through `0x6775730` at `0x678C73D` and removes
destination-only records through `0x679E4B0` at `0x678C870`, with slot
change handling and owner references updated. The derived routine also
reconciles WD equipment state. A follow-up `0x6B31A70` is called at
`0x6B29452`. These decisive call instructions, target pointers, getters
and map offsets were independently decoded.

This establishes conditional replacement of layout/state from buffer to
pawn inventory while aggregate stack tags and quantities already match.
It does not prove an arbitrary preset can introduce different equipment,
identify a saved-preset store, establish normal first-spawn provisioning,
or connect a particular UI event to this RPC. Its ordering against other
UI operations remains unproved.

## Purchase-result callback applies buffer state without the equality gate

The [verified Server_PurchaseLoadout continuation](round8-loadout-rebuy.md#conditional-inventory-derived-loadout-writer)
reaches `0x6B26D00`. It requires result byte **1** at `0x6B26D19`,
valid player-state/controller/inventory objects and a passing cash-availability
test at `0x6B26E04`. Helper `0x6D672F0` compares an integer-converted
result price against the player's available attribute amount. Native
initializer `0x128B090` identifies tag `0xD36B340` as
`Attribute.Meta.Currency.Cash`. The helper is an availability check;
it does not itself deduct currency.

The callback obtains the pawn inventory through `0x6C1AFF0` at
`0x6B26E19` and buffer inventory through `0x3661150` at `0x6B26E3C`.
It gathers **buffer** records at `0x6B26E87` and builds the loadout
from them at `0x6B26EBF`. The authority-gated economy `+0x218`
capture block ends before the actual inventory application.
At `0x6B26F6C`, it calls the pawn inventory's same virtual `+0x4F8`,
passing the buffer as source. Thus the inventory-state copy described
above also supplies a concrete purchase-result application path.

After the copy, `0x6B26F7C` and `0x6B26F8B` call `0x6B26260` on
pawn and buffer respectively. That helper filters exact
`WDFragmentReplicatedData_CartPending` entries from slots' replicated
additional data and writes changed slots through `0x67A0890`
at `0x6B26717`; it does not empty either inventory. Pawn follow-up
`0x6B31A70` runs at `0x6B26F93`. The source/destination registers,
copy and cleanup calls were independently decoded.

This callback has **no `0x6B30800` aggregate-equality gate**. Its local
order is buffer-loadout capture, buffer-to-pawn state copy, then pending-cart
cleanup. It can therefore apply buffer contents without the explicit
layout-commit RPC's matching-quantity precondition. The result code's
named meaning, a custom saved-preset store, and ordering relative to normal
spawn defaults remain unproved; those limits do not erase the verified copy.
