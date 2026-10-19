# Round 8 evidence: loadout defaults and open damage tags

Static, offline review of the CL-516586 corpus and `sdk/raw`; no runtime or service was used. Corpus lookups were read-only. The decompiler marks the relevant native bodies as unreviewed, so call edges support the call-path observations below, not a semantic name for the enclosing routines.

## Default loadout path

**Current boundary:** both Cash and StorageVault branches of `Server_ApplyLoadout` can reach the purchase-data-gated defaults continuation through validated vendor request/tasks. StorageVault consumes available vault quantities and falls back to Cash for shortfalls. The post-grant path updates purchase history and dispatches `Client_ConfirmPurchase`. These observations do not establish a normal spawn hook or custom saved-preset replacement order. The separate [rejoin restore](round8-loadout-restore.md) rebuilds the player inventory map and restores metadata from duplicated session state; the [cooked-import audit](round8-loadout-imports.md) supplies no explicit loadout-RPC caller. Earlier corpus-only negative caller checks below are historical.

The subsequent [component initialization trace](round8-loadout-initialization.md)
identifies a separate player registration hook that grants configured container
defaults through `AddItemToContainer`. The player Blueprint has no serialized
`ContainerSetup` override; native construction supplies thirteen setups with
empty default-item arrays. Later provisioning and first-spawn ordering remain
unresolved. A cooked SniperShowdown component separately attempts
two configured item grants on BeginPlay. Neither finding proves custom
saved-preset replacement.

**Executable follow-up:** the missing corpus edge is now recovered. Actual
instruction `0x6BCC83D` calls `0x6BD5860`. Its enclosing function
`0x6BCC7B0`–`0x6BCC9C6` is present in the executable exception directory
but absent from the corpus function table. It checks a copied result byte
against 1 before calling the defaults routine. Exact calls
`0x6BDCFD5` and tail jump `0x6BDC414` reach this missing function from
`0x6BDCF70` and `0x6BDC3C0`. Independently decoded instructions verify
these edges; they are not inferred from byte patterns alone.

`0x6BDCF70` checks a lifetime monitor and result state before dispatch;
its error branch says the lifetime monitor could not be pinned. This is
consistent with a continuation wrapper, but does not identify the spawn
entry or saved-preset ordering. Earlier corpus-only negative caller checks
below are superseded by these recovered executable edges, not by a claim
that the top-level caller is solved.

- `sub_146BD5860` (`0x6BD5860`) has a direct call to `sub_146784010` (`0x6784010`) at `0x6BD604C`. The callee is the same default-loadout helper described in [Weapon Attributes, choices](../../content/Wardogs_WeaponAttributes_v1.md#choices-this-page-makes) (native defaults, including recursive defaults for attachment sub-slots). The corpus lists `0x6BD5860` as a caller of `0x6784010`.
- The corpus has no direct caller row or alias for `0x6BD5860`. It therefore confirms a function that invokes the defaults helper, but does not identify the top-level spawn caller or independently establish that this routine runs only at spawn. Keep the caller and spawn wording open.
- A saved loadout representation exists: `FWDLoadout` contains `Slots` (`sdk/raw/WDGame_structs.hpp`, `FWDLoadout`), and `FWDLoadoutSlot` carries item/variation tags and slot indices. `WDEconomyComponent::Server_ApplyLoadout` accepts an `FWDLoadout` and is declared `NetServer` (`sdk/raw/WDGame_classes.hpp` and `sdk/raw/WDGame_functions.cpp`). This proves an apply-loadout RPC shape, not that a saved preset replaces spawn defaults. The conditional purchase path from this RPC to `0x6BD5860` is traced below; ordering/overwrite behavior remains unproved.

**Conclusion:** `0x6BD5860` calls the defaults helper on the concrete conditional purchase route traced below. A normal spawn caller and whether a saved preset replaces, supplements, or precedes defaults remain unresolved.

### Bounded caller and RPC cross-check

I scanned the restored executable's `.rdata` as a read-only mapped section
for the exact 64-bit VA `0x146BD5860` (RVA `0x6BD5860`). The section spans
RVA `0x09A27000` for `0x0327B000` raw bytes; there are **zero exact QWORD
hits**. This gives no static `.rdata` pointer-table neighborhood to attribute.
The scan does not rule out references in other sections or computed/indirect
dispatch. The corpus still has no direct-call edge or alias identifying a
top-level caller; that is bounded graph evidence, not proof the routine is
unreachable.

The entire corpus body for `0x6BD5860` reads a multi-field object through
`a1`: offsets `0x00`, `0x08`, `0x10`, `0x18`, `0x20`, `0x28`, `0x38`,
`0x40`, and `0x48` are used as pointers/counts/metadata; it also passes
`a1 + 8` and `a3` to `0x6BE18C0`. At `0x6BD604C` it calls
`0x6784010` with a further slot/context pointer. The signature and accessed
layout do not match `FWDLoadout` (a single `Slots` TArray, size 0x10) or the
`Server_ApplyLoadout` RPC parameters. The anonymized body does not identify
the concrete type behind `a1`, so do not assign it to a particular owning
class from these offsets alone.

`UWDEconomyComponent` in `sdk/raw/WDGame_classes.hpp` has one replicated
`FWDLoadout` field at component offset `0x218` and an anonymous replicated
`TArray<FNone_>` at `0x208`; its stripped SDK name/type does not identify that
array as saved presets. `FWDLoadout.Slots` is the only array in the struct;
its `FWDLoadoutSlot` entries carry parent/container/item indices, item and
variation tags, stack data, count/capacity, rotation, and quick-slot tag.
This establishes a loadout payload and replicated loadout state, but no
specific saved-preset source or default-replacement behavior.

The corpus alias at `0x69BFF50` is the reflected registration pair
`WDGame.WDEconomyComponent.Server_ApplyLoadout`. Its body performs reflected
parameter setup and an indirect virtual dispatch at byte offset `0x538`; it
does not call `0x6BD5860` or `0x6784010`. This identifies the dispatch point,
not its order relative to spawn defaults. The target implementation is
resolved below. Keep the indirect caller and concrete type/owner for
`0x6BD5860`, preset source, and replacement ordering open.

### `Server_ApplyLoadout` implementation slot

The reflected thunk's indirect dispatch at `a1` vtable byte offset `0x538`
is slot `167`. The narrow alias query
`aliases WHERE owner='UWDEconomyComponent_VFT' AND slot=167` resolves it to
`0x6B31B80` (`UWDEconomyComponent_VFT::slot_167`). That body accepts
`(component, FWDLoadout*, int32, bool)`, matching the SDK RPC parameter
layout. It passes the first argument's `FWDLoadout.Slots` TArray to
`0x6CEA3B0`; `0x6CEA480` iterates its `0x48`-byte entries and passes each to
`0x6CEA6B0` for per-slot validation/classification. The handler then builds
transaction/result arrays, consults current purchase-history entries at
component offsets `0x1D8`/`0x1E0`, and hands those arrays to follow-up helpers
including `0x69BE130` and `0x6B30C70`.

I found no explicit clear/reset of existing inventory containers in the
handler body, nor a direct write of a replacement `FWDLoadout` into the
component's replicated field at `0x218`. It passes a computed list through
wrapper `0x69BE130`, now identified as **Client_LoadoutQueued**, rather than
an unnamed economy-specific virtual operation. The name global `0xD359000`
is initialized at `0x124EE00` from UTF-16 literal `Client_LoadoutQueued`
at `0xB1613C8` (destination load `0x124EE07`). The wrapper resolves that
name at `0x69BE1C6`–`0x69BE1D0` and marshals its array argument through
`UObject::ProcessEvent +0x260` at `0x69BE1EA`. The SDK declares this
array-argument RPC reliable, NetClient and Const; original bytes and literal
independently confirm its identity. Its native receiver is now resolved
below; concrete delegate subscribers and transaction fulfillment remain separate.
The handler's
direct call graph contains no `0x6BD5860` or `0x6784010` call. Therefore this
RPC is now linked to its native implementation, but it still does not prove
whether a saved preset replaces, supplements, or precedes spawn defaults.
Keep the exact overwrite semantics open rather than treating the per-slot
transaction handling as a reset.

### Client_LoadoutQueued receiver broadcasts to delegates

The reflected exec at `0x69BEE80` calls virtual `+0x530` at
`0x69BEEF8`. Economy vtable slot 166 (`0xB16A478`) points to
`0x6B2B090`; both instructions and pointer were independently checked.
That receiver broadcasts the Requests array through a delegate-instance
collection at component `+0x158`: it locks the list, walks its
`0x10`-byte records backward and calls virtual `+0x60` at `0x6B2B129`.
Failed/empty instances request cleanup; after unlocking, virtual `+0x28`
at `0x6B2B17A` participates in the removal/compaction pass.

This matches the local UE 5.7 multicast `Broadcast`/`ExecuteIfSafe`
pattern; that different CL corroborates the interpretation. The second
virtual call is a compaction predicate, not a second queued-request event.
The target receiver has no direct purchase/grant call. One concrete
subscriber is now traced: vendor-panel registration `0x749F060` obtains
the player-state economy pointer through getter `0x6D334A0`
(`PlayerState.EconomyComponent +0x408`, SDK-confirmed), then binds
economy `+0x158` to `0x749E6C0` at `0x749F0ED`.

That callback copies `0x48`-byte queued requests at `0x749E7BF` and
tail-jumps to `0x74927D0` at `0x749E8B8`. It walks inventory records
and calls `0x7492DA0` at `0x7492CBB`; that helper correlates
CartPending metadata and updates matching queued requests'
`WDCartPurchaseSources` through `0x6B1E5E0` at `0x7492E95`.
These decisive instructions were independently decoded. This establishes
request/cart-source reconciliation by a vendor-panel subscriber, not an
automatic purchase trigger. Other subscribers and transitive effects remain
outside that result; the broadcast is not established as UI-only.

### Apply-loadout transaction behavior (bounded follow-up)

The handler's request-building per-slot branch constructs an 80-byte request,
sets its requested amount from the slot result, adds three context tags
(including the confirmed `Vendor.Purchase.Type.Cart` tag), and populates
`FWDPurchaseRequestData` plus another additional-data record. It appends
the request to a local array. Before constructing it, the handler subtracts
matching amounts already queued in that array and matching purchase-history
amounts at component `+0x1D8`/`+0x1E0`; when the requested amount exceeds
the resulting allowance, it records a result and skips that request. These
are request and accounting operations, not an explicit inventory clear,
removal, or move. The request array is converted to 72-byte records for
`0x69BE130` and then passed to `0x6B30C70`, which groups requests and
dispatches them through `0x6B31540` to the vendor interface. The latter
reads `FWDPurchaseRequestData` and calls the vendor's virtual `+0x10`.

Original-executable instructions (restored EXE SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`) confirm the decisive
edges: `0x6B3248B`/`0x6B324A6`/`0x6B324C1` add the request tags,
`0x6B324CD` and `0x6B32535` obtain its additional-data records,
`0x6B325A6`–`0x6B325D1` append to the local 80-byte array,
`0x6B326E1` calls `0x69BE130`, and `0x6B328D0` calls `0x6B30C70`.
The second additional-data record is now identified as `WDItemRequestData`:
`0x6B1E740` looks up or creates that reflected type through `0x69C2560`.
At `0x6B32542`–`0x6B3254D`, the handler copies the computed slot path
into its `Destination.Path +0x08`; `0x6B32559`–`0x6B32572` assigns the
weak inventory pointer at `Destination +0x00`, and `0x6B3257F` copies
rotation to `+0x18`.

That inventory is the controller's **BufferStorageInventoryComponent**.
The handler obtains/checks a `WDPlayerController` at `0x6B31C2F`–`0x6B31C73`,
calls getter `0x3661150` at `0x6B31CDA`, and retains its result at
`[rbp-0x68]`. The getter returns controller `+0x8A0`, named in the SDK
as `BufferStorageInventoryComponent`. The later weak-pointer assignment
loads this same saved value at `0x6B32559`. These instructions were
independently decoded. Thus the per-slot requests built by this RPC target
the buffer inventory; their conditional vendor insertion is not itself a
pawn-equipment grant. Later purchase submission and occupied-slot behavior
remain distinct questions.

The per-slot classifier `0x6CEA6B0` invokes `0x6CE9F10` at
`0x6CEAA9B`. Although the corpus has no body for `0x6CE9F10`, direct
disassembly of the executable shows its behavior. It returns status codes
`0`–`10` for selection and availability outcomes. Its quantity callback
is `0x6CEA140` through the fixed leaf `0x445C210` (`mov eax, r9d; ret`),
which returns the count from the current 12-byte slot/stack entry. The
inventory lookup callback `0x6B2A300` calls `0x6CE9CF0`, which writes a
small status/count result after checking a candidate existing item and
location. Its count helper `0x67912B0` sums the `+0x08` integers of
12-byte entries in the existing item's stack array. When lookup status is
`1`, `0x6CE9F10` subtracts that existing count from the requested count
at `0x6CEA063`. A nonpositive
remainder returns status `7` or `10`; zero/no item and other validation
branches return their own nonzero statuses. The success path writes the
selected item ID to the temporary 464-byte result at `+0x08`, writes the
remaining count to `+0x1C8` at `0x6CEA120`, and returns status `0`.
`0x6CEA6B0` stores that status at result `+0x1CC`; the apply handler skips
nonzero status records and uses `+0x1C8` as the subsequent request amount.
This is a purchase quantity/classification path; the classifier's direct
writes target its result record, with no direct inventory clear, removal,
or move. The event dispatch in `0x69BE130` and the concrete vendor route
below do not establish full replacement semantics or an order relative to
normal spawn defaults.

### Concrete cash-purchase bridge from apply-loadout

The former indirect vendor boundary can be resolved for `AWDVendor`.
Executable instructions `0x6D695F0`/`0x6D695F7` install its main vtable
at RVA `0xB3C4F88`, and `0x6D69616`/`0x6D6961D` install the secondary
`IWDVendorInterface` vtable at RVA `0xB3C5750` into object `+0x2C0`.
That five-entry table has `0x6D6BB00` at `+0x10` and `0x6D6BF70` at
`+0x20`. The base interface's corresponding pure-virtual stubs name these
methods `IWDVendorInterface::ProcessRequest` and
`IWDVendorInterface::ValidateEntityRequest` in the binary. Thus the
validation and processing calls at `0x6B3168C` and `0x6B3169F` in
`0x6B31540` dispatch to these concrete `AWDVendor` methods when the
resolved vendor has that vtable.

`0x6D6BB00` resolves a nonnull context from the owning vendor and calls
`0x6BE2190` at `0x6D6BBB2`. That routine resolves
`FWDPurchaseRequestData` and dispatches
its purchase-type tag: `qword_14D369618` calls `0x6BE1C50` at
`0x6BE22DF`, while `qword_14D369628` calls the storage-vault branch
`0x6BE1F80` at `0x6BE22FB`. Executable tag registrations
`0x12724B0` and `0x1272550` identify these globals as
`Vendor.Purchase.Type.Cash` and `Vendor.Purchase.Type.StorageVault`,
respectively (native string/destination instructions at
`0x12724CB`/`0x1272519` and `0x127256B`/`0x12725B9`).
`Server_ApplyLoadout` writes that type to
`FWDPurchaseRequestData+0x08` at `0x6B3251C`: Cash when Boolean `a4`
is false, StorageVault when true. It separately adds the Cart tag to the
request's context at `0x6B324A6`; Cart alone does not select Cash.

For a valid Cash request, `0x6BE1C50` calls `0x6BD0080` at `0x6BE1D83`
with its task-state field initialized to zero. The task builder installs
vtable RVA `0xB334240` at `0x6BD05CE`/`0x6BD05D5`; its slot 1 is
`0x6BDE1F0`. That callback calls `0x6BDC540` at `0x6BDE22D`, which
tail-jumps to `0x6BCC9D0` at `0x6BDC594` after the lifetime check.
The already verified `0x6BCCA5D` call from that continuation reaches
`0x6BD6440`, then `0x6BE1A40` and the successful `0x6BCC7B0`
continuation reach `0x6BD5860` and its defaults-helper call
`0x6784010` at `0x6BD604C`.

This establishes a **conditional** `Server_ApplyLoadout` Cash-request
route to the defaults helper through the concrete `AWDVendor` interface.
It requires vendor/request validation, purchase permission, task success,
and the state-1 continuation; it does not imply every loadout request
executes the helper. The visible route queues a purchase for a count
shortfall and has no explicit global inventory clear or move before that
continuation. It still does not identify a saved preset source, a normal
spawn event, or an overwrite order relative to normal spawn defaults.

The insertion destination is request-selected. At `0x6BD5B32`, helper
`0x6BCDA60` finds `WDItemRequestData` in request AdditionalData (type
getter `0x69C2560`). The continuation pins that data's first weak pointer
at `0x6BD5B4A`, checks validity and calls `0x6795480` at `0x6BD5B74`.
The SDK identifies the first field as
`Destination.InventoryComponentWeak`. That pinned component is passed as
`rcx` to the insertion/default helper at `0x6BD604C`, or the alternate
insertion route `0x6783C10` at `0x6BD60A9`. The returned placed count is
compared with the requested count at `0x6BD60B0`; a mismatch reaches
shortfall helper `0x6BD9090` at `0x6BD60D0`. These instructions were
independently decoded. This identifies a conditional request-directed add,
not an inherently fixed pawn/vault destination or whole-equipment replacement.

### Recovered caller is an item-request continuation

The earlier “no caller” statement for `0x6BD5860` is superseded by executable
instructions. An exact `E8` scan and `.pdata` bounds put the sole direct call
at `0x6BCC83D` in `0x6BCC7B0`–`0x6BCC9C6`. The call runs only when the
copied result-state byte equals `1` (`cmp` at `0x6BCC828`). Its input is the
context at the continuation object's `+0x40`; after construction, that
context's first pointer is the object passed as `a1` to `0x6BE1A40`, followed
by copied entity-request fields. `0x6BE1A40` calls task constructor
`0x6BCF9F0` at `0x6BE1B8C` with result-state `0`, selecting its graph-task
branch: the task vtable at RVA `0xB3342F0` has `0x6BDE110` at slot 1.
`0x6BDE110` calls `0x6BDC3C0` on the captured context (`a1+0xA8`), and
`0x6BDC3C0` tail-dispatches to `0x6BCC7B0` at `0x6BDC414`. This is the
concrete registration/dispatch route for the observed state-0 constructor.
The constructor's state-3 branch instead installs vtable `0xB3342A8`, whose
`+0x30` entry is `0x6BDCF70`; that wrapper also calls `0x6BCC7B0` at
`0x6BDCFD5`, but **is not** the branch selected by `0x6BE1A40`'s state-0
argument. These are request-continuation edges, not a spawn registration.

`0x6BE1A40` accepts an object pointer and a request whose `+0x28`
amount must be nonzero; its first virtual call at object vtable `+0x180`
must return nonnull. It then resolves the request, prepares a task and
copies the object into its callback context. The concrete class of that
object is not established by this call alone. The purchase path
`0x6BD6440` calls `0x6BE1A40` at native sites `0x6BD6908` and
`0x6BD6BBE`, passing the first object pointer in its request context.
That function explicitly resolves `FWDPurchaseRequestData` from the
`FWDEntityRequest.AdditionalData` field (`0x6B1E4D0`), verifies the weak
vendor as `AWDVendor` (`0x6D6B260`), obtains the player economy component,
and emits “Cannot purchase item” errors. This is direct evidence of an item
purchase caller, not evidence that the object is always a vendor or that the
same defaults routine is restricted to spawn. A second request branch at
`0x762E0A0` calls the thin `0x6BE1690` wrapper into `0x6BE1A40` after
purchase-data and cost checks.

The sibling continuations reinforce the request-processing context. Exact
calls `0x6BCCA5D` (`0x6BCC9D0`–`0x6BCCBE6`) and `0x6BCCC92`
(`0x6BCCBF0`–`0x6BCCDA8`) invoke `0x6BD6440` purchase handling and
`0x6BD6DB0` storage-vault-item handling respectively, with the same
result-state comparison. In the reflected `UWDEconomyComponent` RPC chain,
`Server_ProcessEntityRequests` thunk `0x69C00B0` dispatches slot 173
(`0x6B32A20`), which builds request records and hands them to
`0x6B30C70`/`0x6B31540`. The latter resolves
`FWDPurchaseRequestData.Vendor`, checks `WDVendorInterface`, and invokes
interface virtual `+0x10` on the vendor. The exact implementation edge from
that indirect call through concrete `AWDVendor` Cash processing to
`0x6BE1A40` is established above. This is a gated branch; it does not make
every entity request a purchase or a defaults-helper invocation.

**Revised boundary:** native defaults are applied on the successful
continuation of this entity-request flow; the evidence does not identify it
as a spawn hook. No examined edge establishes a saved-preset source or an
overwrite order relative to defaults.

### Purchase-data gate on the recovered defaults call

The route is more specific than an arbitrary entity-request continuation.
At the start of `0x6BD5860`, the request at `a1+0x08` is passed to
`0x6BE18C0`. That helper first calls `0x6B1E4D0` to resolve
`FWDPurchaseRequestData`; if resolution fails, it returns null.
`0x6BD5860` then immediately returns an error on that null result, before
its later `0x6784010` call at `0x6BD604C`. Thus the **observed call to the
native defaults helper requires purchase request data**. This is a
necessary gate, not proof that every purchase grants every default.

The two control tags in this same routine also have concrete executable
registrations: `0x1272410` assigns `qword_14D369620` the tag
`Vendor.Purchase.Type.Cart`, and `0x12722D0` assigns
`qword_14D369640` `Vendor.Purchase.Context.Restock`. `0x6BD5860`
tests both tags in its request-tag arrays before choosing its later
handling branches. These tag identities, the purchase-data gate and the
explicit purchase caller `0x6BD6440` jointly characterize the recovered
continuation as purchase processing. The concrete bridge above links
`Server_ApplyLoadout` to this continuation for validated Cash requests.
No inspected path links a normal spawn event or saved-preset selection to
the defaults call. A distinct spawn-time defaults call may exist, but this
purchase continuation does not establish one or its overwrite order.

## Vehicle and underbarrel weapon tags

**Superseded for vehicles:** the later
[weapon-context trace](round8-weapon-context.md) proves the vehicle
extension-to-projectile tag path. The paragraph below records the earlier
boundary; only underbarrel ownership remains open.

The damage evidence generator still marks both paths not traced in [`_tools/infantry_tables.py`](../../_tools/infantry_tables.py#L397): vehicle `WE_*` assets carry `DamageEntityData.Tag` values in `Meta.Damage.Weapon.*`, while `GrenadeLauncher.json` has no such weapon tag. The missing native link is whether those values are placed in the hit's source context in the same way as infantry weapon tags. Do not present the cooked tags alone as proof that the vehicle bone-damage rows or an underbarrel weapon row are selected.

## Caliber parent matching

**Superseded for the generator's named cases:** the later
[normal-reload and projectile-association trace](round8-weapon-context.md#follow-up-normal-reload-and-named-projectile-associations)
closes `caliber-parent-match`. Normal reload uses the destination container's
exact-id or parent-aware context filter; the loaded item supplies the projectile
asset. The generator retains the supported slug, artillery and STN_03
associations and removes four prefix-only candidates. It no longer presents
tag-name prefix matching as runtime proof. Universal `SupportedCaliber`
admission remains outside that closure, separate from the archetype-modifier
parent fallback documented in [GameMechanics](../../content/Wardogs_GameMechanics_v2.md) §2j.

## Suggested doc edits

The later [Rebuy trace](round8-loadout-rebuy.md) connects the Rebuy Last
Loadout button to `Server_ApplyLoadout` using current economy `FWDLoadout`.
It separately identifies `Server_ProcessRebuy`, which reads current economy
purchase history/loadout state. A named-preset source and replacement
ordering are not established by either route.

- In [Weapon Attributes §5](../../content/Wardogs_WeaponAttributes_v1.md#5-not-traced), state that `0x6BD5860` calls `0x6784010` (call site `0x6BD604C`) on a purchase-data-gated success continuation. Its normal-spawn role remains unproven. Retain the saved-preset question until a native path establishes ordering or replacement.
- The later weapon-context trace closes vehicle tag provenance; keep underbarrel ownership and universal `SupportedCaliber` admission open.

### StorageVault branch of `Server_ApplyLoadout`

The Boolean-true request type at `0x6B3247F` reaches the same concrete
`AWDVendor` interface as Cash, but `0x6BE2190` calls `0x6BE1F80` at
`0x6BE22FB`. After its player-state check, `0x6BE1F80` calls the
state-zero graph-task builder `0x6BD0710` at `0x6BE2084`. The installed
vtable RVA `0xB333EC0` has callback `0x6BDE2D0` in slot 1; that calls
`0x6BDC6C0`, whose live-object branch jumps to `0x6BCCBF0` (native jump
`0x6BDC714`). The latter requires result state `1` at `0x6BCCC71`
before calling the StorageVault processor `0x6BD6DB0` at `0x6BCCC92`.
This establishes the selected task route, with its state and lifetime
gates, from the Boolean-true RPC request.

`0x6BD6DB0` resolves the request's `FWDPurchaseRequestData` through
`0x6B1E4D0`; missing data errors out. It obtains the current player's
controller through `0x42C8580`, then calls `0x6B1E590` at `0x6BD7080`.
The latter passes the `UWDStorageVaultComponent` class from getter
`0x6CF5370` to controller virtual `+0x738`. Its registration at `0x6CF5387`
names `/Script/WDGame.WDStorageVaultComponent`; the SDK identifies that type
as a `UBHInventoryComponent` subclass and the controller's corresponding
property at `+0x8D8`. Slot 231 resolves to inherited actor component lookup
`0x3A93090`, which checks candidate component classes before returning a
match or null; it is not an untyped inventory accessor. This does not prove
the returned pointer equals the named field in every mutated actor state.
The request entity/quantity
forms 20-byte rows, either directly or through variation helper
`0x6BED650`. Rows are initially tagged StorageVault. `0x6BE2930`
(called at `0x6BD7229`) queries stack count with `0x679BC80` against the
returned inventory object and splits any amount unavailable there into a
Cash-tagged row. For each remaining positive StorageVault row,
`0x6BD726C` calls `0x6CFFDD0` with the row's entity and quantity; that
routine walks matching inventory stacks and calls `0x679E570` to consume
them. A failed consume switches the row to Cash at `0x6BD7275`–`0x6BD727C`.
The revised row list is copied into request additional data through
`0x6B1E5E0`.

Only Cash rows contribute to the computed currency charge at
`0x6BD6DB0`'s `0x6BE0FF0` call. On the insufficient-currency branch,
`0x6BD740C` calls `0x6CFEC30` for positive StorageVault rows; that
function removes matching entries from the inventory object's internal
tracking array at `+0x6D0`, so this branch is cleanup, not a global
loadout clear. On the continuing path, `0x6BD75A2` calls `0x6BE1A40`
with the prepared request. Its successful state-one continuation reaches
`0x6BD5860` and the defaults helper `0x6784010`, as traced above.
`0x6BD773C` also creates a later task through `0x6BCF340`; its callback
(`0x6BDE090` → `0x6BDC230` → `0x6BCC5B0`) is a separate downstream
boundary, and this trace does not assign it replacement semantics.

The observed StorageVault path sources per-entity counts from a player
inventory accessor, consumes available quantities, and falls back to Cash
for a shortfall or failed consume. Its requests can conditionally reach the
same defaults helper as Cash. No inspected operation clears the whole
equipment inventory or identifies a saved-preset source or ordering
relative to normal spawn defaults.

### StorageVault post-grant callback

The state-zero `0x6BCF340` task installed at `0x6BD773C` has vtable RVA
`0xB333BF0`, whose slot 1 is `0x6BDE090`. That callback reaches
`0x6BDC230` and its live-object jump to `0x6BCC5B0`. Native
`0x6BCC632` calls `0x6BD54B0` with the captured StorageVault request
context and the inner grant result, then `0x6BCC6A6` publishes the
result of `0x6BD54B0`. This is a downstream result callback for the
`0x6BE1A40` grant task, not a separate entry from the loadout RPC.

`0x6BD54B0` requires grant result state `1` and a true result byte at
`result+0x20` for its successful branch (native `0x6BD54EA`–`0x6BD5507`).
On failure it iterates its 20-byte StorageVault rows and calls
`0x6CFEC30` with each entity/quantity to remove the earlier inventory
tracking entries (`0x6BD5700`–`0x6BD5717`); it also runs the recorded
resource-refund and failure-event paths. On success, it calls
`0x6B2B6E0` on the resolved economy component at `0x6BD5573`.
`0x6B2B6E0` writes the component's `+0x233` flag when the request lacks
the Cart tag, may signal an event, then calls `0x6B28970` at
`0x6B2B7C3`. The latter inserts or updates 40-byte entries beginning
at component `+0x1D8`, which the SDK identifies as
`UWDEconomyComponent.PurchaseHistory`. It does **not** write the SDK's
`FWDLoadout` field at `+0x218`. After that, original instructions
`0x6B2B7E5` tail-jump to unindexed `0x69BDD30`; that function constructs
an event and calls a virtual method at economy-component vtable `+0x260`
(`0x69BDD82`–`0x69BDD8C`). The concrete implementation of that virtual
call is resolved in the following subsection as the purchase-confirmation
RPC; its recipient behavior remains separate from this native wrapper.

The callback also computes a value from StorageVault-tagged rows via
`0x6BD95F0` and increments a separate returned component's `+0x118`
integer through `0x6BE4B00`, subject to `result-context+0x74` being
false and a positive value. Its final optional call to `0x6CFF080`
is guarded by the tag `Vendor.Purchase.Mode.Immediate` in the request
or purchase-data tag arrays (`0x6BD562D`–`0x6BD5677`; tag registration
`0x1272375`–`0x12723E6`). `0x6CFF080` contains an
`OnlineServerPlayerDataInterface` persistence path for the vault data;
it is not evidence of equipment-slot clearing. The examined
`Server_ApplyLoadout` handler explicitly adds the type, Cart and one
other context tag, but no Immediate tag at its `0x6B32460`–`0x6B324B0`
construction site. Neither this callback nor the verified history
writer establishes child/subslot application or replacement of spawn
defaults. The named confirmation dispatch below does not establish the
eventual client recipient's effects.

### Resolved tail dispatch: purchase confirmation RPC

The `0x69BDD30` boundary above is a reflected call, not an unidentified
economy-specific virtual operation. Original instructions first initialize
and copy an `FWDEntityRequest` into a stack parameter buffer
(`0x69BDD50`/`0x69BDD5D`), then store the incoming `xmm2` float at
buffer `+0x48` (`0x69BDD6C`). The SDK's
`WDEconomyComponent_Client_ConfirmPurchase` parameter struct has exactly
`Request` at `+0x00` (size `0x48`) and `ItemPaidPrice` at `+0x48`.
`0x69BDD62` loads FName global RVA `0xD358FE0`, whose initializer
`0x124ED80` passes the literal `Client_ConfirmPurchase` to the FName
constructor at `0x1725770`. `0x69BDD72` calls `0x18FEA90`, whose
missing-function path says `Failed to find function %s in %s`; its
returned `UFunction*` becomes `rdx`, while `r8` is the parameter buffer
and `rcx` remains the economy component. The virtual call at
`0x69BDD8C` through `vtable+0x260` is therefore `ProcessEvent` for
`UWDEconomyComponent::Client_ConfirmPurchase`, matching the SDK's
`NetClient` declaration and generated wrapper.

This resolves the prior unknown tail: after the purchase-history write,
the visible native path sends purchase confirmation with the request and
paid price. It does not add a server-side equipment clear, child/subslot
application, or saved-loadout replacement operation. The client RPC's
eventual recipient behavior is a separate question; this wrapper alone
does not prove its UI or inventory effects.

### Other indexed calls to the item/defaults helper

Three additional game-side callers of `0x6784010` are
`0x6BE7670`, `0x6BE8A40`, and `0x6BE9BE0`; their native call instructions
are `0x6BE801C`, `0x6BE928A`, and `0x6BEA025`. Their examined paths use
purchase data, vendor/item context, and Cart/Restock handling. These are
additional request-processing variants, not recovered normal-spawn edges.
They occupy slots 3/6/9 of dispatch table `0xB334CB0`. Its vptr-setting
constructor at `0x6BEAC10` is referenced by a registration record, but its
exact owning type and indirect factory caller have not been established.
Nearby vendor-variation names are supporting context, not a type binding.
The generic BHInventory add-item/container callers remain a separate
upstream route; these checks do not establish every caller of the helper.
