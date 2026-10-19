---
title: Round 8 rebuy button and RPC sources
nav_exclude: true
---

# Rebuy Last Loadout submits the current economy loadout

Static CL516586 evidence traces the Rebuy Last Loadout button to
`Server_ApplyLoadout`, and separately identifies the history-based
`Server_ProcessRebuy` RPC. Neither trace identifies a standalone
saved-preset store or establishes
normal first-spawn ordering. No game or service was executed. Native RVAs
refer to the restored executable with SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.

## Cooked UI and native click route

The freshly exported
`/Game/UI/Features/Vendor/Widgets/InventoryComponent/W_InventoryComponent_Vendor_Overview`
contains `Button_Rebuy`, displaying **Rebuy Last Loadout** from string-table
key `Restock.RebuyHeader`. Its Ubergraph binds
`WDUIInventoryComponentViewModel.RebuyLoadoutVisibility` to that button's
visibility. The containing widget inherits native
`WDUIInventoryComponentWidget`. The button is a
`W_StyleGuide_Button_Main_Primary_C`, whose separately exported class
inherits native `WDUIButton`.

Neither the Rebuy instance nor that style asset serializes a Rebuy action
tag or click callback. Other widgets in the same package do contain action
data, including an inventory-sort prompt; those bindings do not belong to
Rebuy. The actual Rebuy click binding is native.

Inventory-widget vtable slot 161 resolves to `0x72AF560`. It reads the
SDK's `Button_Rebuy +0x660`, uses its `+0x1460` click event, and registers
callback `0x72A9070` with the widget's view model (`+0x528`) at
`0x72AF692`–`0x72AF6B2`. The event's native click identity is independently
established in the [Deathmatch button trace](round8-loadout-deathmatch.md).
The callback requires its eligibility/live-object checks and a nonempty
current economy loadout. Getter `0x6B2F0C0` addresses that component's
`FWDLoadout +0x218`; the callback obtains it at `0x72A90C6`, checks its
slot count at `0x72A90CE`, resolves the enclosing panel through `0x749C760`,
then passes the loadout to `0x749AAB0` (`0x72A9110`–`0x72A9120`).

At `0x749AB4D`, the latter calls wrapper `0x69BE380` with that loadout,
an integer derived from its slot/stack counts and a UI bindable Boolean.
The wrapper copies `0x48`-byte loadout slots into its RPC argument block,
resolves a function using name global `0xD359018` at `0x69BE42A`, and
dispatches `UObject::ProcessEvent` through virtual `+0x260` at `0x69BE458`.
The global's initializer `0x124EE60` loads UTF-16 literal
`Server_ApplyLoadout` at `0xB162AD0` and targets `0xD359018` at
`0x124EE67`. Native literal, binding, getter/callback and wrapper instructions
were independently checked. This resolves the click-to-**ApplyLoadout**
edge; it does not connect this button to `Server_ProcessRebuy`.

The immediate button source is the economy component's current loadout.
The [existing ApplyLoadout trace](round8-loadout.md) covers its conditional
Cash/StorageVault purchase continuation. A concrete producer of the current
field is traced below; initial population and other possible writers remain
separate questions. This does not establish a named preset or automatic
spawn grant.

Raw exports remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_rebuy_ui_20261019/`, in
`dumps/W_InventoryComponent_Vendor_Overview.json` and
`style-dump/W_StyleGuide_Button_Main_Primary.json`.

A separate exact `Rebuy` import audit covers all **107,181/107,181** mounted
IoStore packages and **1,230,571/1,230,571** resolved script imports,
with **zero failures** and **zero matching paths**. In particular it finds
no serialized `WDEconomyComponent:Server_ProcessRebuy` import. The earlier
Loadout/Preset filter did not cover this spelling; the new audit closes
that search gap without claiming the RPC is unreachable. Native callers,
dynamic dispatch and action routing are outside this import negative.
The scan retains 15 `WDWeaponOwner` script references as its positive control.
Copied probe source and TSV output remain outside the repo under
`E:/Reverse_Engineer/wardogs_analysis/round8_rebuy_imports_20261019/`.

## Conditional inventory-derived loadout writer

The button's `Server_ApplyLoadout` requests use
`WDItemRequestData.Destination` pointing to the controller's
`BufferStorageInventoryComponent`, as established in the
[request-construction trace](round8-loadout.md#apply-loadout-transaction-behavior-bounded-follow-up).
This identifies buffer staging on the verified per-slot add path, rather
than a direct pawn-equipment grant. It does not alone establish how a
later purchase submission is triggered.

A native purchase-task callback can write the current field from inventory
records. Task builder `0x6B211B0` reads
its fifth argument's discriminator at `+0x10` (`0x6B211ED`).
Discriminator **3** selects task mode 3 at `0x6B21213`–`0x6B21225`;
the mode-3 branch installs vtable `0xB2F9040` (`0x6B213C1`).
Discriminator 1 instead copies its mode from the result context, so the
mode-3 branch is not proved exclusive to discriminator 3. Callback slot 6 at
`0xB2F9070` points to `0x6B2D0F0`.
That callback calls `0x6B1DE60` at `0x6B2D14C`, which reaches
`0x6B26D00` at `0x6B1DEE6`. The pointer and call instructions were
independently checked.

The examined `Server_PurchaseLoadout` handler `0x6B33E30` calls this
builder at `0x6B34CE3`, but supplies discriminator **0**: it zeros
`r12d` at `0x6B34BA0`, stores it at `[rbp]` at `0x6B34BAB`, and passes
`&[rbp-0x10]` as the fifth argument. This call therefore does **not**
select the discriminator-3 callback above.

Instead, discriminator 0 sets `ebx=0` at `0x6B21264`, takes the non-3
branch at `0x6B21356` and non-4 branch at `0x6B214D3`, and constructs
a different task with vtable `0xB2F9088` at `0x6B217A0`–`0x6B217A7`.
It initializes the continuation through `0x6B24010` at `0x6B217DB`,
then submits the task through `0x157C320` at `0x6B21837`.
Vtable slot 1 (`0xB2F9090`) points to `0x6B2DEC0`, which calls
`0x6B2C870` at `0x6B2DEFA`. When its task state is not 2 and its
lifetime monitor can be pinned, that helper tail-jumps to `0x6B1DE60`
at `0x6B2C8C3`, reaching the same writer. These branch, pointer and
call instructions were independently checked. This is the conditional
purchase-to-writer route; the discriminator-3 route is not evidence for it.

The producer tests incoming result byte `+8 == 1` at `0x6B26D19`.
On its additionally gated object/operation path, it gathers buffer-inventory
records and invokes builder `0x6CE86A0` at `0x6B26EBF`. That builder
iterates/filter-checks `0xF8`-byte inventory records and yields loadout
slots; it does not simply copy the ApplyLoadout RPC's supplied array.
The producer then calls `0x46DBB20` at `0x6B26ECA`. This helper tests
the owner actor's role byte at `+0x170` against **3** (Authority), with
the owner read from component `+0xC8`. SDK Actor.Role and ENetRole agree
with those offsets/value.

On that authority branch, `0x6B26ED3`–`0x6B26F0E` releases the old
component `+0x218` slot array and transfers the builder result's pointer,
count and capacity into it, zeroing the moved-from array. It calls the
replication field marker with index **4** at `0x6B26F23`. The native
economy constructor initializes this array empty (`0x6B24FC5`–`0x6B24FCC`);
other verified assignments include rejoin restore and component-to-component
copy. These assignments and the conditional callback do not identify a separate
named-preset asset/store.

The handler obtains the result handle from `0x6BE0760` at `0x6B34B97`
and passes it as the builder's third argument. That operation walks
`0x48`-byte request records, calls `0x6BD0DA0` per record at `0x6BE08BC`,
combines handles through `0x6BD35E0` at `0x6BE0997`, and constructs
its final result through `0x6BD28C0` at `0x6BE0A38`. These call sites
and the `0x48` loop increment were checked in executable bytes; they
do not alone establish each request's inventory effects or completion order.

The continuation constructor stores this handle at context `+0x10`.
The callback passes that field to the wrapper, which dereferences it
and copies the tested result byte from its payload at `+0x20`;
the code's exact named meaning is unestablished. The same callback now
has a verified [buffer-to-pawn inventory copy](round8-loadout-buffer-layout.md#purchase-result-callback-applies-buffer-state-without-the-equality-gate)
at `0x6B26F6C`, after the loadout-capture block. It then removes pending-cart
metadata from both inventories. This establishes that local application
order; it does not establish ordering against normal spawn defaults or
that the current field always has this source.

## Purchase submission consumes selected buffer entries

`Server_PurchaseLoadout` also has a concrete removal path before its
`0x6BE0760` submission. With a nonempty selected-path list and valid
component, `0x6B34AF6` calls getter `0x3661150`, whose complete body
returns controller `+0x8A0`. The handler checks the controller against
the `WDPlayerController` class getter `0x6D40000`; the matching SDK
names `+0x8A0` as `BufferStorageInventoryComponent`.

The loop at `0x6B34B30`–`0x6B34B6B` passes each selected path to
`0x679E570` at `0x6B34B5F`, with amount from entry `+0x10`, removal
context **2** (SDK `Used`) and final Boolean false. The reflected
`RemoveItemFromSlot` thunk calls that same native function at `0x67AAEFF`.
Its path/amount records advance by `0x18` bytes. The instructions and
getter were independently decoded. This is selected buffer-slot removal,
not proof of clearing or replacing the pawn's equipped inventory. Complete
selection rules and downstream request effects remain separate questions.

The RPC's Requests parameter is not an established source of missing
destination data. Its validation dispatch uses economy vtable slot 170
(`0xB16A498`), pointing to `0x6B34E10`. That function's complete body is
`cmp dword ptr [rdx+8],0; sete al; ret`: it accepts only an empty
Requests array. The reflected thunk calls validation before implementation.
This gate and pointer were independently checked; the implementation's
selected buffer records are distinct from that empty incoming array.

The purchase handler's request construction differs from ApplyLoadout's
buffer-targeted construction. It initializes a fresh request through
`0x6BE49D0` at `0x6B345AD`; that constructor zeros AdditionalData at
`+0x30/+0x38`. The examined handler then adds `WDCartPurchaseSources`
through `0x6B1E5E0` at `0x6B3472A` and purchase data through
`0x6B1E930` at `0x6B34776`, with no direct `0x6B1E740`
item-destination constructor call in its decoded body. This construction
does not select an ordinary item-grant destination. The ordinary vendor insertion
branch separately requires `WDItemRequestData` at `0x6BD5B32`; a
cart-source record is not a substitute for that destination. The final
equipment application is now established separately: the result callback
copies buffer state into pawn inventory. It does not need to select that
target through an ordinary vendor item request. The full per-variation
transaction behavior remains outside this copy proof.

The separate [Server_CommitVendorBufferLayout path](round8-loadout-buffer-layout.md)
does identify a conditional buffer-to-pawn inventory layout/state copy.
It requires authority, no positive CartPending amount in buffer slots,
and equal last-DataStack-tag quantity summaries for buffer and pawn.
Its inventory copy inserts source-only paths and removes destination-only
paths. The purchase-result callback uses the same copy operation without
that matching-quantity gate, as detailed in the linked report. A custom
preset's storage and relationship to spawn defaults remain unproved.

## Reflected state holders

A parsed census of every primary reflected field in the verified recovered
map finds just two fields storing `WDLoadout`: the economy component's
current-loadout field and the session's snapshot field. The other matching
type references are `WDEconomyComponent.PurchaseHistory` and
`WDLoadout.Slots -> Array<WDLoadoutSlot>`. No additional mapped reflected
store using `WDLoadout`, `WDLoadoutSlot`, `WDPurchaseHistory` or
`WDRebuyItemOverride` appears. This census includes nested container types;
it does not cover RPC parameter metadata, nonreflected native storage or
preset data represented as another type. It therefore narrows known state
holders without proving a separate preset feature absent. Probe source,
build and `references.tsv` remain outside the repo under
`E:/Reverse_Engineer/wardogs_analysis/round8_rebuy_state_types_20261019/`.

## Separate history-based Rebuy RPC

The SDK also declares `WDEconomyComponent.Server_ProcessRebuy` as a reliable
native server RPC with a Boolean and an array reference. Its reflected
thunk `0x69C0160` calls virtual `+0x560` at `0x69C0228`. The economy
vtable at `0xB169F48` has target `0x6B32CD0` in slot 172, through the
pointer at `0xB16A4A8`. These instructions and pointer bytes were
independently checked.

The implementation checks the RPC array count against the second
purchase-history array's count at component `+0x1F0`; excess entries
take the exit path (`0x6B32EBA`–`0x6B32EC4`). Its input records have
stride `0xC`. Records with a nonzero first eight-byte tag and nonnegative
integer at `+8` enter a local tag-to-amount map
(`0x6B32F1E`–`0x6B32F58`). This matches the SDK layout of
`FWDRebuyItemOverride` (`VariationTag`, `Amount`), but stride and field
shape do not independently prove the RPC array's reflected inner type;
the generated signature still calls it `TArray<FNone_>`.

The handler traverses the current economy component's purchase-history
second array at `+0x1E8`, in `0x28`-byte rows, with tag and helper checks
before retaining records (`0x6B32F6D`–`0x6B3300D`). It supplies that
component's current `FWDLoadout` at `+0x218` to two builders: the source
addresses are formed at `0x6B3332D` and `0x6B3343A`, for
`0x6BE6060` and `0x6CEA480`. The SDK names `FWDPurchaseHistory` at
component `+0x1D8` and `FWDLoadout` at `+0x218`; the
[rejoin trace](round8-loadout-restore.md) independently identifies the
same live loadout and history data as snapshot metadata sources.

The Boolean chooses the request type: false selects
`Vendor.Purchase.Type.Cash` (`0xD369618`), true selects
`Vendor.Purchase.Type.StorageVault` (`0xD369628`), written at
`0x6B33842`–`0x6B33869`. These are the same registered purchase-mode
keys established in the [purchase trace](round8-loadout.md).

On the dispatch path, the handler zeros the **first purchase-history
array's count** at component `+0x1E0` (`0x6B33BE6`–`0x6B33C12`) and
calls existing request processor `0x6B30C70` at `0x6B33CAA`. This is a
history reset, not an inventory-map clear. No direct inventory clear or
loadout overwrite was identified in this handler; downstream transaction
fulfillment remains separate and this does not prove preservation or
replacement of every existing item.

### Local quantity planning is not physical inventory replacement

Planner `0x6BE6060` allocates one local integer per `0x48`-byte loadout slot.
It seeds each value from positive slot `Capacity +0x34`, otherwise helper
`0x6CE9110` (`0x6BE6100`–`0x6BE613D`), then subtracts clamped covered
quantities from that local array (`0x6BE66CD`–`0x6BE674A`). This is
history-adjusted quantity planning, not a demonstrated inventory-map write.
The second planner `0x6CEA480` iterates the same loadout slots and calls
`0x6CEA6B0` per slot (`0x6CEA63B`, stride increment `0x6CEA647`). Its
result records supply the amounts written into `0x50`-byte entity-request
rows at `Amount +0x28`. No zero-quantity skip has been established.

Request processor `0x6B30C70` resolves purchase data and submits transaction
work through `0x6B20B10` at `0x6B313D2`. No explicit inventory clear,
removal or move was identified in these planners or that processor.
Actual fulfillment through transaction/vendor callbacks remains downstream;
this bounded result does not establish complete merge/replacement behavior.

The explicit `Auth_ClearInventory` API supplies another bounded check.
Its reflected thunk `0x67A4BB0` calls native `0x6786390` at `0x67A4C38`.
The indexed direct callers are that thunk and tutorial paths `0x6F8BB10`
and `0x6F8BBC0` (tail calls at `0x6F8BBA7` and `0x6F8BC6C`); the
examined caller list has no ApplyLoadout/Rebuy/purchase caller. This is
not an exhaustive absence result: the verified [rejoin map replacement](round8-loadout-restore.md)
already demonstrates replacement through a different helper.

The button-to-ApplyLoadout buffer staging and conditional purchase-result
buffer-to-pawn state copy are established. The separate Server_ProcessRebuy caller,
other possible population paths and any named-preset storage/selection remain open. Neither route
establishes an automatic spawn grant or answers whether a custom preset
replaces spawn defaults.
