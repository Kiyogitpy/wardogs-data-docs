---
title: Round 12 spawn and loadout provisioning census
nav_exclude: true
---

# What items a player has at spawn, and where each source sits

Static CL516586 evidence from `WardogsClient-Win64-Shipping.restored.exe`
(SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`),
the decompile corpus, the raw SDK and the exported `data/` tree. Addresses are
executable RVAs. Nothing was run. This page extends
[round8-loadout-initialization.md](round8-loadout-initialization.md) and
[round8-loadout.md](round8-loadout.md); it adds a bounded census of every
route that can put an item into an inventory. It does not say what the server
does at runtime.

## Short answer

| Question | Answer | Label |
|---|---|---|
| Does any data asset list starting items for the normal player? | No. `ContainerSetup` appears in no `data/` JSON, and the fresh cooked player Blueprint has no `Starting*`, `Default*Items` or item tags. | **Data** |
| Does the native player component carry default rows? | No. Thirteen setups are built with empty `DefaultContainerItems`. | **Native** (round 8) |
| Is there a generic GameFeature action that grants items to the player? | No. None of the 96 `AddComponents` rows in `data/` names a generic grant component. Two modes add their own (SniperShowdown, Deathmatch). | **Data** |
| So how does a normal-mode player get gear? | Through the purchase continuation (`Server_ApplyLoadout`), the vault/stash import and the rejoin restore. All are request-driven, not a fixed spawn list. | **Derived** |
| What is not closed? | Runtime writers reached only through Blueprint or virtual dispatch, and the real first-spawn timing. | not traced |

## 1. The data side has no spawn list

- `grep` over `data/` finds **0** files containing `"ContainerSetup"` and **0**
  containing `ItemsToStartWith`. (**Data**)
- `DefaultContainerItems` appears in **205** files: **416** arrays, **225**
  non-empty and **191** empty. Every one sits inside a
  `BHInventoryFragment_SubSlotSupport` of a `BHInventoryItemDefinition`. They
  describe what a created *item* holds (a magazine's ammo, a weapon's default
  sight), not what a *player* holds. (**Data**)
  See [Items §defaults](../../content/Wardogs_Items_v2.md) and
  [Weapon Attributes](../../content/Wardogs_WeaponAttributes_v1.md) for how
  `0x6784010` consumes them.
- The fresh cooked `B_WDMoverPlayerCharacter` dump contains no item tag
  (`Id.Item.`) and no `Starting*` or `Initial*` property apart from
  `StartingMovementMode`. (**Data**, external dump under
  `E:/Reverse_Engineer/wardogs_analysis/round8_spawn_loadout_20261019/player/`)

## 2. GameFeature actions that add components

All `GameFeatureAction_AddComponents` rows under
[`data/Wardogs/Plugins/GameFeatures`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures) were extracted: **96 rows**. Rows that
could grant items:

| Feature | Host | Component | Item grant? |
|---|---|---|---|
| SniperShowdown | `WDMoverPlayerCharacter` | `B_SniperShowdown_LoadoutComponent` (server only) | Yes, BeginPlay: `Id.Item.SmallBackpack`, `Id.Item.Glock17` ([round 8](round8-loadout-initialization.md#concrete-mode-specific-beginplay-grant)) |
| Deathmatch | `WDMoverPlayerCharacter` | `WDDeathmatchWeaponSelectionComponent`, `WDLoadoutAmmoGenerationComponent` | Selection-driven; see [Deathmatch](round8-loadout-deathmatch.md) |
| HotPotato | `WDGameFrameworkComponentReceiver` | `B_HotPotatoSpawnComponent` | Native adds one item to the *spawned throwable's* inventory (below), not to a player |
| Gunsmith | `WDPlayerController` | `WDGunsmithPlayerComponent` | `AddCustomItemToInventory` (below), user-built weapon |
| Buildables | `WDMoverPlayerCharacter` | `WDPawnBuildableManager` | Reaches the add chain; placement-related, not traced as spawn |
| KOTH | `WDGameModeSession` | `WDKOTHPlayerSpawnManagerComponent`, `WDItemRequirementsEvaluatorComponent` | Not in the grant call graph below |
| ShootingRange, Tutorial, BaseScenario, SniperShowdown | `WDGameModeSession` / `WDGameMode` | player spawn managers | Not in the grant call graph below |
| MoneyMan, Health regen, AI, skins, etc. | various | various | No add-chain path found |

(**Data** for the rows; the last column is **Native** call-graph reach.)

## 3. Native census of routes into the add chain

The item-creation chain is `0x6783880` (`AddItemToContainer`), `0x6784010`
(item creator), `0x6783F00` (add to slot path) and `0x6785430` (existing
slots). A backward walk over the corpus call table from these four
functions, up to five caller hops, found 87 functions. Those that are a vtable
entry or a registered reflected function resolve to the entries below.
Call-table edges are direct calls only; virtual and Blueprint dispatch are not
followed. (**Native**)

| Entry (RVA) | Owner | What it is | Spawn relevance |
|---|---|---|---|
| `0x6787B20` | `UBHInventoryComponent` vslot 128, called by the player and vault overrides (`0x6B53E20`, `0x6D00320`) | Registration hook, grants `DefaultContainerItems` setup rows (context 2) | Runs for the player, but the 13 setups are empty (round 8) |
| `0x67A3F20`, `0x67A3D10`, `0x67A4300` | `UBHInventorySubsystem` | Reflected `AddItemToInventory`, `AddItemToContainer`, `AddItemToSlot` | No native caller; reached only from Blueprint/other reflected calls. Serialized `AddItemToInventory` imports: 6 packages (round 8 census) |
| `0x6B50DC0` (exec wrapper `0x6B66F80`, vslot 195) | `UWDPlayerInventoryComponent::AddCustomItemToInventory(EBHItemAdditionContext, FWDModKitDetails)` | Adds a built weapon plus its attachment map | Only native caller: Gunsmith component `0x8664E40` (call site `0x86651F0`), which passes context byte 2 (Bought) in the decompile; not a spawn route |
| `0x6BD5860`, `0x6BE7670`, `0x6BE8A40`, `0x6BE9BE0`, economy slots 163/167 | economy component / subsystem | Purchase, cart, restock, rebuy continuations | Request-driven (round 8) |
| `0x6D678F0` (vslot 273 of `AWDPlayerState`, forwarded by `AWDPlayerStateFrontend` `0x6D84030`) via `0x6CFE100` | `UWDStorageVaultComponent` method | Imports stash records keyed `ITEMS` and `VEHICLES`, grid position, count and rotation (`"90"`, `"180"`, `"270"`) into the vault's setups; add call `0x6CFE759`, context 2 | Persisted vault load, not the pawn's loadout. See below |
| `0x7727130` | `UWDDepositPalletIntoFOBContext` vslot 91 | Deposit into an FOB container | Interaction |
| `0x6CAEDB0`, `0x855ED20`, `0x855D420`, `0x855B5E0`, `0x7741AB0`, `0x6D6B890`, `0x76213E0` | Interaction contexts: grenade throw-back, lootables, swap, vehicle restock, vendor | World interactions | Not spawn |
| `0x7626F70`, `0x7634D20`, `0x76384E0` | Vehicle supply container, crate, pallet | Supply stocking | Not spawn |
| `0x8495620` | `UWDLoadoutAmmoGenerationComponent` vslot 159 | Deathmatch ammo/loadout | Mode-specific |
| `0x8639660` -> `0x863B270` | `UWDHotPotatoSpawnComponent` vslot 128 | Spawns a throwable actor, resolves a component on it, adds item tag `component+0x100` with context 3 (**Restock**) at `0x863B507` | HotPotato mode, targets the throwable |
| `0x6D58A10` | `AWDPlayerController` vslot 652 = `Cmd_GiveItem` | Console command | Developer command; no claim on availability |
| `0x88801C0` (`OnBotMutableSetupFinalized`), `0x768B7D0` (`SetupWeaponStartingInventory`) | AI influence component; vehicle gameplay systems | Bot setup; vehicle weapon starting stock | Not the player |

The vault importer deserves one clarification. `0x6CFE100` reads the setup
array at component `+0xE0` (count `+0xE8`, stride `0x110`), so it uses the same
`ContainerSetup` layout as the player component. Its class getter `0x6CF5370`
is the literal `WDStorageVaultComponent` (`/Script/WDGame`). It is therefore
the stash loader, not an alternative player spawn list. The `0x6D678F0` caller
applies a multi-part state struct (`a2+16/96/176/256/272/352/448/528/616`);
the field meanings other than the `ITEMS` (`+448`) and `VEHICLES` (`+528`)
inputs are not traced, nor is the source of that struct.

## 4. Ordering

| Step | Claim | Label |
|---|---|---|
| Component registration (base hook `0x6787B20`) | Runs before any component's `BeginPlay`, because UE registers components before actor begin-play | **Derived** (engine lifecycle, not traced in the exe) |
| Registration grants nothing for the player | 13 constructor setups, no row writes | **Native** |
| GFA-added `B_SniperShowdown_LoadoutComponent` `BeginPlay` | Calls `AddItemToInventory` with context 1 and two tags | **Data** (bytecode) |
| Economy `OnPawnSet` | Binds and refreshes metadata, adds nothing (round 8) | **Native** |
| Rejoin restore | Rebuilds the player map from the duplicated session | **Native** (round 8) |
| Relative order of purchase, restore and mode grants on first spawn | Not established | not traced |

## What this does and does not establish

- It narrows the question: no data asset and no generic GameFeature action
  defines a universal starting kit. The only starting-item lists found in
  data are the SniperShowdown pair and item-internal defaults.
- It does not prove the absence of a runtime writer. Blueprint graphs not
  covered by the import census, virtual calls and engine `ProcessEvent`
  dispatch are outside the call table.
- A saved named-preset store has still not been found. The vault importer is
  the only persisted inventory-shaped loader seen in this census, and it
  targets the stash. Nothing here claims how the backend populates it.
- No server-authority, exploitability or availability claim is made. The
  authority gate at `0x6787B8C` (role 3) is recorded in round 8 only.

## Reproduction notes

- `data/` scans: `grep -rl` for `"ContainerSetup"`, `ItemsToStartWith`,
  `DefaultContainerItems`; a regex walk over `GameFeatureAction_AddComponents`
  `ComponentList` entries (96 rows).
- Corpus: backward BFS over `calls(target_function_rva -> caller_rva)` from the
  four chain seeds, depth 5, then a `.rdata`/`.data` scan for 8-byte pointers to
  each reached function, mapped to the nearest preceding `vtable` alias.
- Reflected names by `registration_pair` alias: `AddCustomItemToInventory`
  at `0x6B66F80`, `Cmd_GiveItem` at `0x6D58A10`.
