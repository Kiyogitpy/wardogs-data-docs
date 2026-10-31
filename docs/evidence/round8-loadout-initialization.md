---
title: Round 8 player inventory initialization
nav_exclude: true
---

# Inventory container defaults at component registration

Static CL516586 evidence from `WardogsClient-Win64-Shipping.restored.exe`
(SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`)
and the matching raw SDK. Addresses below are executable RVAs. This is a
component-default path, distinct from the purchase-data-gated
`Server_ApplyLoadout` continuation in [round8-loadout.md](round8-loadout.md).

## Player component reaches the base hook

The `UWDPlayerInventoryComponent` registration override at `0x6B53E20`
calls `UBHInventoryComponent`'s registration hook `0x6787B20` directly
at native `0x6B53E44`, with the component pointer still in `rcx`
(`0x6B53E41`); the base hook then calls `UActorComponent`'s hook
`0x3C9DAB0` at `0x6787B35`. This establishes that the player subclass
does execute the base container-default logic before its own additional
registration work. The separate inherited component-initialization hook
`0x6795B80` calls engine `0x3CAB090` at `0x6795BA2` and populates
runtime container slots from `ContainerSetup` through `0x6775570` at
`0x6795D66` and `0x679620A`. These are distinct lifecycle hooks; the
examined calls do not by themselves establish the complete first-spawn
ordering of initialization, registration and subsequent loadout requests.

## Source rows and grant arguments

The SDK places `UBHInventoryComponent.ContainerSetup` at component
`+0xE0` as a `TArray` of `FBHContainerSetup`, whose stride is `0x110`.
Within each setup, `DefaultItems` is a gameplay-tag container at
`+0xE0`, while `DefaultContainerItems` is a separate `TArray` at
`+0x100` of 16-byte `FBHDefaultItem` rows. Each row has `Item` at
`+0x00` and optional `Amount` at `+0x08` (set flag `+0x0C`). The base
hook reads the setup count at component `+0xE8` (`0x6787BC9`) and the
per-setup default-row pointer/count at `0x6787DB5`/`0x6787DBC`.

After resolving an owner (`component+0xD0` or `0x3CA8F70`), the base hook
requires a valid actor at `component+0xC8` whose `AActor.Role` at
`+0x170` equals `3`, SDK `ENetRole::ROLE_Authority`
(`0x6787B8C`–`0x6787BB1`). This is an authority-role gate, which also
permits standalone authority. For each nonempty `DefaultContainerItems` row it resolves the
item definition (`0x6787E2F`–`0x6787E5B`) and checks that it is valid.
The requested count starts at one. If the row's optional amount is set,
native `0x6787E7B`–`0x6787E87` takes the integer at row `+0x08`;
otherwise the typed item-data lookup at `0x6787E97`–`0x6787EFA`
may replace the count with `BHInventoryFragment_Stackable.MaxStackSize`
at `+0x38`. The class getter `0x6772790` registers the literal
`BHInventoryFragment_Stackable`, and the SDK names that integer field;
the native type/validity checks precede the read at `0x6787EFA`.

At `0x6788016`, the base hook calls `0x6783880`, the native
`UBHInventoryComponent::AddItemToContainer` implementation, passing
the setup container path, row item, context byte `2`, requested count,
rotation `0`, and final Boolean `false` (`0x6787FF6`–`0x6788016`). SDK enum
`EBHItemAdditionContext` names value `2` **Bought**. It repeats while
the returned remaining count decreases, stopping when no progress is
made. `0x6783880` validates the item and container support. On its
path without a valid enclosing item (`0x67761F0`), it enumerates
candidate slots and calls the native item creator `0x6784010` at
`0x6783B77`; its other branch calls `0x6785430`, which tries existing
slot paths. Thus `0x6784010` is reachable when configured container-default
rows are present, but it is not the only branch for every item.

This identifies a direct configuration-to-inventory insertion mechanism
in the normal player component's base hook. A fresh cooked export of
`/Game/MoverTesting/B_WDMoverPlayerCharacter` identifies its
`PlayerInventoryComp` as `WDPlayerInventoryComponent` (export 84), also
referenced by the player CDO's `PlayerInventoryComponent` property.
That component export contains no serialized `ContainerSetup` override.
The [native constructor trace below](#native-setup-behind-the-absent-cooked-override)
finds thirteen inherited setup rows with empty default-item arrays.
Later provisioning still needs to be followed. Nor does this show whether
a saved `FWDLoadout` later replaces inserted items. The normal first-spawn
item list and request ordering therefore remain open.

## Concrete mode-specific BeginPlay grant

The fresh cooked Blueprint `/SniperShowdown/Data/B_SniperShowdown_LoadoutComponent`
inherits `ActorComponent`. Its CDO's `ItemsToStartWith` contains
`Id.Item.SmallBackpack` and `Id.Item.Glock17`. `ReceiveBeginPlay` invokes
its Ubergraph at bytecode offset 408. That graph gets its owner (408),
casts to `WDMoverPlayerCharacter` (428), calls `GetPlayerInventory` (503),
and checks the result with `IsValid` (545). Failed cast/validity branches
exit (493/574).

The successful branch loops through `ItemsToStartWith` and calls
`BHInventoryComponent::AddItemToInventory` at bytecode offset 79 with
each tag, context `1` (**Looted**), amount `1`, slot-search option `2`
(**IgnoreStorageSlots**), and a null final inventory-component argument.
The returned count is unused. These arguments follow the SDK function
signature and enums; bytecode offsets here are not executable RVAs.
The graph contains no authority guard, so this is a conditional
mode-specific attempt to grant two items, not evidence for a universal
server-side spawn loadout or for successful insertion on every invocation.

The extractor mounted the installed CL516586 packages and dumped both
packages without failures on 2026-10-19, using the existing export usmap.
Raw JSON and package lists remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_spawn_loadout_20261019/`.
Only reviewed facts are recorded here. Native call sites `0x6B53E44`
and `0x6788016` were independently decoded from executable bytes.

## Native setup behind the absent cooked override

The absent `ContainerSetup` property in player export 84 does **not**
mean that the component starts with zero setups. The native
`UWDPlayerInventoryComponent` constructor `0x6B4D940` calls the
`UBHInventoryComponent` constructor `0x677F6E0` at `0x6B4D962`.
The base constructor zeros the setup-array pointer and count/capacity
at component `+0xE0/+0xE8` (`0x677F720`, `0x677F73D`). The derived
constructor then calls `0x6B51A20` **13 times** from `0x6B4E760`
through `0x6B4EEC9`, each time with `component+0xE0`. That helper
increments the array count, advances by the `FBHContainerSetup`
stride `0x110`, and constructs one setup with `0x6B4A9D0`
(`0x6B51A4F`–`0x6B51A69`). The derived constructor assigns each
new setup an identifier and filter, so the native baseline has 13
configured container setups.

The setup constructor zeros both `DefaultItems`' tag arrays at setup
`+0xE0/+0xE8` and `+0xF0/+0xF8`, and `DefaultContainerItems` at setup
`+0x100/+0x108` (`0x6B4AAEE`, `0x6B4AAF5`, with `rbx` equal to
setup `+0x18`). The thirteen append sequences assign identifiers,
filter tags, and separate lookup maps but show no direct write to a
setup's `DefaultContainerItems` pointer or count. Thus these native
constructor rows contain **no default item rows at construction**.
The player cooked component template has no serialized override for
this array. A later runtime writer or external provisioning path has
not been excluded. In particular, reaching the base `OnRegister`
grant mechanism does not establish that the normal player receives
any item from these constructor rows at first spawn.

## Runtime slot initialization is not a default-item source

The shared inventory vtable slot 126 resolves to `0x6795B80` for
`BHInventoryComponent`, `WDPlayerInventoryComponent` and
`WDStorageVaultComponent`. This method reads the configured setup count
at component `+0xE8` (`0x6795BB2`) and array pointer at `+0xE0`
(`0x6795BD0`). It derives each setup's slot count from its mode/capacity,
builds slot paths, and inserts runtime records through `0x6775570`
into `InventoryMap +0x390` (first insertion setup at `0x6795D5F`).
The SDK names that map and the setup fields; the setup stride remains
`0x110`. Later code also creates private-slot paths from separate setup data.

This identifies another consumer of the thirteen configured containers.
The examined method builds runtime slot records and copies support rules;
it does not establish a later writer of their `DefaultContainerItems` or
an ordinary first-spawn item source. The player registration hook's separate
`bSpawnItemActors` branch concerns item actors, not proof that these
constructor-empty default arrays acquire items. A nearby add-to-container
route through `0x6D0C120` and `0x6CFE8E0` is reached from known purchase
processing; it is not independent spawn evidence. These findings leave the
later provisioning boundary open rather than treating configured slots as
granted equipment.

The separate [Deathmatch native handler](round8-loadout-deathmatch.md)
attempts to grant a supplied item and four magazines from its default tag
data. A native weapon-selection button callback now supplies its item tag
through the component's RPC delegate. Its `DeathmatchWeaponsData` registry
now resolves to [`DT_DeathmatchWeaponSelect`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Deathmatch/Content/Data/DT_DeathmatchWeaponSelect.json), and the component's registration
requests its selection scene according to the PreMatch/Playing.Deathmatch
state checks. Automatic item granting at spawn remains unproved; this is
another mode-specific route,
not a source for the universal starting-item list.

## Economy pawn setup and existing-slot metadata

Economy registration `0x6B29D50` binds the named `OnPawnSet` delegate
on owner storage `+0x320`, then immediately processes the current pawn:
`0x6B29EC6` loads owner `+0x330`, `0x6B29ECD` zeros the old-pawn
argument, and `0x6B29ED6` calls handler `0x6B30390`. This establishes
an initial-current-pawn setup call, not first-ever spawn ordering.
The handler binds inventory events through `0x6B352B0`, calls setup
helper `0x6B2F490`, and replaces old/new pawn event bindings.

The new-pawn callback `0x6B30680` updates existing loadout metadata.
Its nonzero third argument clears flag `economy+0x230` and returns.
The other branch requires that flag clear, `+0x1E0` nonzero, valid
resolved objects and nonempty gathered inventory records. It walks
the existing slot array at `+0x218`, count `+0x220`, stride `0x48`
(`0x6B30762`–`0x6B307AF`). Each slot's `ItemId +0x0C` is passed to
`0x6B5D150` at `0x6B3079C`; the result is stored in `QuickSlotTag +0x3C`
at `0x6B307A4`. The SDK names both fields. It marks replication field
4 at `0x6B307BE` and sets `+0x230` at `0x6B307D1`.

These independently decoded instructions identify a metadata refresh,
not an item-add operation. Setup helper `0x6B2F490` also installs a
callback through `0x6B2F470`/`0x69BE220`. Its reflected target is
`Client_NotifyVaultConsumeError`: initializer `0x124EE20` loads that
UTF-16 literal at `0xB161700` and initializes name global `0xD359008`
at `0x124EE27`; the wrapper resolves that global before ProcessEvent.
The SDK marks it a reliable native client RPC taking an integer error
code. This identifies a notification binding; its concrete receiver-side
body was not identified. No absence of transitive provisioning is inferred
from these event-binding and metadata-update bodies.

## Bounded cooked grant-import census

A fresh case-insensitive script-import scan for `AddItemToInventory`,
`AddItemToContainer` and `Auth_AddItemSlot` loaded all **107,181** mounted
packages and resolved all **1,230,571** script imports, with **zero failures**
and exit code **0**. Fifteen `WDWeaponOwner` imports serve as a positive
control. The only six matches import
`/Script/BHInventory.BHInventoryComponent:AddItemToInventory`:

| Package suffix | Context identified by asset path |
|---|---|
| [`TargetDummy/B_TargetDummy`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/WorldInteractable/Objects/EnvironmentalObjects/TargetDummy/B_TargetDummy.json) | Target dummy |
| `InteractionContexts/WIC_InteractionContext_DeployablePickUp` | Deployable pickup |
| `InteractionContexts/WIC_InteractionContext_ThrowablePickUp` | Throwable pickup |
| `Experiences/SniperShowdown/Content/Data/B_SniperShowdown_LoadoutComponent` | Separate mode loadout, examined above |
| `Items/CombatBow/Content/Data/Interaction/WIC_SpawnableProjectilePickUpInteractionContext` | Projectile pickup |
| `ShootingRangeTutorial/Content/Stages/B_ShootingRangeTutorial_Stage_EnterDeathBox` | Tutorial stage |

There are no matching serialized imports for the other two API names.
Imports identify dependencies, not executed grants or first-spawn timing.
This census does not cover native calls, dynamically selected functions,
or provisioning through other APIs, and does not establish a universal
starting-item source. Exact package paths, copied probe source, stdout,
structured totals, exit status and TSVs remain outside the repo under
`E:/Reverse_Engineer/wardogs_analysis/round8_grant_imports_20261019/`.
