---
title: Round 8 frontend loadout assets
nav_exclude: true
---

# Frontend Loadouts assets do not identify a saved-preset source

Six installed CL516586 packages under
`/Game/UI/Features/Frontend/Loadouts/` were freshly exported offline on
2026-10-19, with zero failures: `DA_LoadoutsScene`, `W_LoadoutsScene`,
`DA_InventoryComponent_Loadouts`, `W_InventoryComponent_Loadouts`,
`W_Loadout`, and `W_Button_Loadout`. The last four were followed from
the scene/data references. This is a bounded cooked-asset inspection,
not a claim about all native UI behavior.

A separate native comparison covers the 107 indexed virtual slots of
`UWDUILoadoutsViewModel` (vtable `0xB49F588`) and its
`UWDUISceneViewModel` base (`0xB453E10`). Original pointer bytes match
for slots 1–106; only destructor slot 0 differs (`0x709F700` versus
`0x6FA5970`). The subclass SDK adds an inventory-viewmodel pointer at
`+0xD0`; `WDUILoadoutsData` supplies inventory-viewmodel parameters at
`+0xD0`, and `WDUILoadoutEntry` adds no reflected fields. This comparison
finds no subclass-specific virtual preset-population routine. Inherited
factory behavior, nonvirtual helpers and external entry providers remain
outside that result; the SDK's empty entry layout is not proof that the
feature is absent.

A subsequent native scene trace covers the substantive overrides of
`UWDUILoadoutsScene` (vtable `0xB49EC40`): slots 161 (`0x709E350`)
and 167 (`0x709E5E0`). After checking the scene context and list widget
at `+0x5B8`, slot 161 obtains the list model and sets a loop count of
**five** at `0x709E413`. Each iteration obtains the
`WDUILoadoutEntry` class (`0x709E740`), constructs an object through
`0x1931130` at `0x709E448`, and adds it to the list through
`0x38A9030` at `0x709E472`. The decrement/back-edge is at
`0x709E477` / `0x709E47B`. No preset payload is assigned in that loop;
the registered entry size is 40 bytes, the base UObject size. The scene
then initializes the inventory display; slot 167 connects the inventory
viewmodel and widget at `+0x5C0`. This is consistent with placeholder
entries and a generic inventory display, an interpretation rather than
proof that a preset feature is absent elsewhere.

`DA_LoadoutsScene.InventoryComponentViewModelParams` selects
`WDUIInventoryComponentViewModel` with `DA_InventoryComponent_Loadouts`.
That data asset configures `WDUIContainerGridViewModel_Vendor` for
primary, specialist and sidearm slots, fallback slots/containers, and
backpack/vest containers. Its overview data and backpack layout reuse
Vendor overview assets. These are inventory display configurations;
they do not declare a saved-loadout payload or persistence source.

`W_LoadoutsScene` has an empty `OnDataContextChanged` graph apart from
event dispatch/return. Its list uses generic list/list-entry viewmodels,
`SelectionMode=None`, and `W_Loadout` as its entry widget. The latter
contains `W_Button_Loadout`, whose caption is "Loadout". Neither entry
nor button supplies package-specific Blueprint bytecode. The list's
selection mode does not establish that focus or button interaction is
impossible.

`W_InventoryComponent_Loadouts.OnDataContextChanged` binds inventory
viewmodel properties to the widgets: backpack capacity visibility/text,
missing-backpack visibility, value text, occupied storage slots and
storage capacity. No select/apply/save operation appears in these six
packages' examined graphs. The native scene path above extends that
inspection; generic base widgets and packages outside this subtree remain
outside the cooked-graph negative finding.

A targeted persistence audit also finds no concrete equipment-preset
definition in the available WDGame, PragmaSDK and OnlineSubsystemPragma
SDK declarations. `FWDLoadout` contains slots, without a preset name or
save metadata; the mapped current-economy and session owners are already
covered by the [rebuy](round8-loadout-rebuy.md) and
[restore](round8-loadout-restore.md) traces. Searches for
`Loadout`, `EquipmentPreset`, `EquipmentTemplate` and `SavedPreset` in
the two Pragma SDK packages yield no matching declaration. The offline
filename inventory supplies no standalone player-profile/loadout protocol
schema; the available `usmap_schema.json` files describe the reverse
mapping format. The inspected `*_PlayerData.json` assets are pawn-data
assets pointing to pawn classes, not account stores.

This does not rule out backend persistence. In
`sdk/raw/PragmaSDK_structs.hpp`, `FPragma_PlayerData_PlayerData` exposes
`Entities` and `Version` (around line 5035), while
`FPragma_PlayerData_Entity` exposes an entity name, instance ID and
components (around line 2178). `FPragma_PlayerData_ComponentWithId`
wraps `SerializedComponent` (around line 9042), and its
`FPragma_PragmaAny` has a numeric type and serialized bytes (around
line 1842). The dumped entity arrays have unresolved element types, so
these declarations alone do not prove a particular typed component
relationship. They leave room for custom backend payloads whose schema
is unavailable here. No game service or account data was accessed.

The saved-preset question is an **uncorroborated handoff hypothesis**:
the user has not identified an observed feature, and these audited build
surfaces supply no concrete feature/store to trace. Reopen the hypothesis
on a specific UI action, persistence schema or native consumer; do not
assign replacement-versus-defaults behavior before then. The separate
[rejoin snapshot restoration](round8-loadout-restore.md) and
[Deathmatch selection callback](round8-loadout-deathmatch.md) establish
different concrete mechanisms; neither should be renamed a frontend
saved-preset implementation.

Raw exports and the package list remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_frontend_loadouts_20261019/`.
