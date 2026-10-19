---
title: Round 8 loadout cooked-import audit
nav_exclude: true
---

# Loadout callers: cooked script-import boundary

The installed CL-516586 packages were inspected offline with a task-local
typed CUE4Parse probe. No game process or service was used. The extractor
consumed the AES key by path; no key value or raw package export is included.

## Coverage and results

The provider mounted 32 VFSs containing 149,124 files. All 107,181 mounted
`.uasset`/`.umap` entries loaded as IoPackages, with zero failures. The probe
visited all 1,230,571 script-import slots and resolved every slot to its
canonical object path. Matching was case-insensitive for `Loadout` or
`Preset` within `/Script/WDGame.` and `/Script/BHInventory.` paths.

There were 18 matching import slots:

| Imported role | Slots |
|---|---:|
| Sky `SetPreset` | 1 |
| Gamepad discrete-setting preset classes/default objects | 6 |
| Wager condition requiring loadout cost | 1 |
| UI meta-tree preset classes/default objects | 4 |
| Frontend loadouts scene/data classes/default objects | 4 |
| Vendor `BindLoadoutPurchasableEventBinding` | 2 |

No matching Loadout/Preset import names `Server_ApplyLoadout`,
`Server_PurchaseLoadout`, or an obvious saved-loadout selector. A function
named solely `Server_RestoreInventory` is outside this keyword filter.
The resolved paths do
include native functions (`WDSky:SetPreset` and the vendor binding), so the
scan is not limited to class imports. The independent exact-name positive
control found 15 `WDWeaponOwner` import slots, matching the earlier audit.

The loadouts scene/data imports belong to `W_LoadoutsScene` and
`DA_LoadoutsScene`. Vendor binding imports belong to `W_VendorSummary` and
`W_VendorSummary_Overview`. They establish native UI dependencies, not a
saved-preset representation or a call to the apply-loadout RPC.

A targeted SDK cross-check also leaves the preset source unidentified:
`WDUILoadoutsScene` declares a list view at `+0x5B8` and inventory widget
at `+0x5C0`; `WDUILoadoutEntry` adds no fields to `UObject`;
`WDUILoadoutsData` holds `InventoryComponentViewModelParams` at `+0xD0`;
and `WDUILoadoutsViewModel` holds an inventory-component viewmodel pointer
at `+0xD0`. None declares a named saved-preset collection or select/apply
method. These reflected layouts do not exclude private native state or
Blueprint/delegate behavior.

An expanded pass then removed the WDGame/BHInventory namespace restriction
and searched `Loadout`/`Preset` across all `/Script/` imports. Coverage and
positive-control counts remained identical, with zero failures. Its **751**
matching slots were dominated by audio presets. Only eight import slots contained
`Loadout`: seven WDGame loadout-related slots listed above and
`MoneyManRuntime.WDMoneyManComponent:GetCostOfLoadout` in
`BP_MoneyManComponent`. No import named
`DeathmatchRuntime.WDLoadoutAmmoGenerationComponent:Server_SetupLoadoutByTag`
was found. Its [native trace](round8-loadout-deathmatch.md) now connects
a weapon-selection button callback to item and magazine grant attempts;
its registry-to-source-table binding and conditional match-state-to-scene
request are also established. An automatic selection event or item grant
at spawn remains unproved.
An import negative does not make it unreachable. This expanded probe's
source, artifacts, TSV and log remain outside the repo under
`E:/Reverse_Engineer/wardogs_analysis/round8_allscript_loadout_20261019/`.

## Boundary and next action

A second pass used exact API-name terms `AddItemToInventory`,
`AddItemToContainer`, `AddItemToSlot`, and `Auth_AddItemSlot` over the
same 107,181 packages and 1,230,571 resolved script-import slots, again
with zero failures. Seven matching slots belong to the target dummy,
deployable pickup, throwable pickup, CombatBow projectile pickup, IED
interaction, shooting-range death-box tutorial, and SniperShowdown
loadout component. Six import `AddItemToInventory`; the IED interaction
imports `AddItemToSlot`. There is no matching explicit import of the
other two searched API names. This is import coverage, not an exhaustive
search of native or reflected inventory writers.

Fresh bytecode review of the SniperShowdown component identifies an
actual mode-specific BeginPlay grant attempt for a small backpack and
Glock, documented in [component initialization](round8-loadout-initialization.md).
It does not establish the universal player-spawn defaults or their
ordering against an apply-loadout request. The second pass's full TSV
is retained in the external probe directory's `item-add-output/`.

The negative loadout-RPC checks rule out explicit script-import entries for
those named RPCs in the inspected packages. They do not exclude native callers, runtime reflection, delegates,
or a Blueprint calling a different native entry point that subsequently
applies a loadout. It therefore does not establish spawn grant ordering or
saved-preset replacement semantics.

The concrete independent SDK lead is `AWDPlayerStateSession`: a private
`InventorySnapshot` map at `+0x5F0`, a private `FWDLoadout` at `+0x650`, and
the parameterless `Server_RestoreInventory` RPC. These declarations do not
say what source that RPC restores. The subsequent [native restore trace](round8-loadout-restore.md)
follows that implementation to a rejoin snapshot and component-backed
loadout copy, without establishing a custom saved-preset source.
The subsequent [frontend asset audit](round8-loadout-frontend.md) examines
six Loadouts-path packages and finds inventory UI configuration/bindings,
without identifying preset save/apply logic in their graphs.

Probe source, isolated build artifacts, scan log and complete result/failure
TSVs remain outside the repository under
`E:/Reverse_Engineer/wardogs_analysis/round8_loadout_importscan_20261019/`.
The project was built against the existing CUE4Parse checkout using
`dotnet build --artifacts-path`; no repository binaries or maps were replaced.
The summary facts above are the publishable artifact.
