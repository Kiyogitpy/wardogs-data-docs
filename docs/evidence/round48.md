# Round 48, agent RE48: the last two backlog items

Continues [round 47](round47.md) (items 2 and 3) and [round 46 B](round46-b.md) (item 4). Static review of CL516586 only; nothing was run, no devirtualization. RVAs are for `WardogsClient-Win64-Shipping.restored.exe`. Scratch: `E:/Reverse_Engineer/wardogs_analysis/round48/` (`cs.py`, `rs.py`, extractor dumps).

| # | Item | Status | One line |
|---|---|---|---|
| 1a | `RuntimeSources` fill order | FOUND (`0x46EBF30`) | filled in `DataSources` index order, one entry per enabled source |
| 1b | Row name the placement reward requests | ABSENT in the client (consumer not in this exe) | the registry type name `CashRewards` is not in the executable, so no client code requests `Id.Buildable.*` from it |
| 2 | Wheel state-change listener, `Values[state]` | FOUND (listener); `Values[state]` read ABSENT in the listener | the only bound listener is the instanced wheel **mesh** component; it applies visibility and two 0..1 values, not friction or radius |

## 1a. `RuntimeSources` is filled in `DataSources` order. FOUND (static disassembly and decompile)

- `UDataRegistry` vtable `0xA7838E0`, slot 114 (`+0x390`) is **`0x46EBF30`**, the refresh of the runtime source list. (The vtable also carries the teardown `0x46E6A40` at slot 89 and `0x46ECED0` at slot 90, which calls each source's slot `+0x2F0`.)
- `0x46EBF30` copies the old `RuntimeSources` (`+0x50`, count `+0x58`, 8-byte pointers) to a local array, sets the count to 0, then **loops `DataSources` (`+0x40`, count `+0x48`) from index 0 upward**. For every non-null entry it calls the source's vtable `+0x2E8` (slot 93) with the address of `RuntimeSources` (`a1 + 80`) as the output array. After the loop, old runtime sources that are no longer in the new list are shut down (their slots `+0x2D8` and `+0x320`).
- Slot 93 for the base source and for both `UDataRegistrySource_DataTable` (`0xA784828`) and `_CurveTable` (`0xA784F30`) is the same function **`0x46E5550`**: if the source's slot 89 (`+0x2C8`, at `0x178DF10` a plain read of byte `+0x28`) is true, it appends `this` to the output array; otherwise nothing. So each enabled data-table source adds itself once, in `DataSources` order. (What byte `+0x28` means is not named; the `DR_CashRewards` sources are in use, so it is set for them.)
- Round 47 saw the resolver `0x46ED100` read `RuntimeSources` by index. This round also read the per-id source map builder `0x46E8140` (slot 111): it walks `RuntimeSources` in index order and sets an id's source only when the slot is still empty (`if (!*slot)`), which is first source wins again.

Result: `RuntimeSources` order is `DataSources` order, so for a row name present in several of the `DR_CashRewards` tables the first table listed (Built, then Placed, then Placed in FOB) supplies the row. Reproduce: `python round40_veh/rdis.py 46e5550 100`, and the corpus decompile of `0x46EBF30` and `0x46E8140`.

## 1b. Which row name a placement reward requests. ABSENT in the client

Searched, all with a negative result:

- The string `CashRewards` (ANSI and UTF-16) is **not in the executable**, although the other registry type names are (`RewardFeed` 18 and 16 hits, `VendorData`, `MasteryDefinitions`, `GlobalDamageData`). So no client code names this registry type.
- It is not in any shipped `.ini` (`DefaultGame.ini` names `MasteryDataRegistryId`, `MetaTreesDataRegistryId`, `VendorDataRegistryId`, `LiveCurvesDataRegistryId`, `ChallengeRewardsDataRegistryId` and others, none for cash).
- `WdExtract findname` over all of `Wardogs/Content` and `Wardogs/Plugins`: the name `CashRewards` is in the name map of only the registry asset (with its 15 table packages), `DT_CashRewards` / `DT_AssistCashRewards` (as part of the asset name) and `Spotting` (a game-feature action that adds `DT_Reward_Cash_Spotting` to the `CashRewards` registry, client and server). No Blueprint or state tree builds a data registry id of that type. The Blueprint pattern for a registry read is `RegistryType` = a name constant and `ItemName` = a gameplay tag name (seen in `B_EventDefinition_Resource`, type `RewardFeed`); nothing equivalent exists for `CashRewards`.
- The client-visible cash path is different: `WDGameSettings` (`DefaultGame.ini`) points `ResourceRewardDataTables` (tag `Meta.Rewards.Resource.Cash`) to the plain table `DT_CashRewards`, `ResourceRewardMatchScoreDataTables` to `DT_Reward_Cash_EndGameFactionReward`, `AssistRewardDataTables` to `DT_AssistCashRewards` and `ResourceRewardModifiersDataTable` to `DT_CashRewardModifiers`. These hold `Meta.Progression.Resources.*` and `Meta.Rewards.Modifier.*` rows, not the `Id.Buildable.*` rows of the Built / Placed / Placed in FOB tables.

Conclusion: the three `Id.Buildable.*` cash tables are read by a consumer that is not in this client build (most likely the dedicated server, which was not available; the registry source and the Spotting action are flagged for both). Which table pays a placement therefore cannot be shown from the client. What is proven: the registry gives the first table in `DataSources` order (1a), so if a request for `Id.Buildable.X` or `Meta.Progression.Context.DefaultReward` carries only the row name, the **Built** table answers. Next step to settle it: the server binary, or one logged placement reward.

## 2. Wheel state-change listener. FOUND (listener); `Values[state]` not read by it

- The vehicle `+0x3C0` list belongs to `UMWheeledVehicleMovementComponent` (SDK pad at `0x3C0`, `AxleSystems` at `+0x6C0`). The broadcaster `0x5370A40` iterates it (16-byte entries: object pointer and serial) and calls each listener's vtable slot `+0x60` with `(wheel index, old state, new state)`; a false return marks a stale entry.
- Binder: **`0x5316430`** (creates the 0x30-byte object-method delegate and adds it to the list). It has exactly one caller, **`0x53303F0`** (itself called from `0x539ABB9`), a method of **`UInstancedWheelMeshComponent`** (vtable slots near `0x53362A0`). It stores a bool at `+0xA38` and two optional bytes (`+0xA39` with flag `+0xA3A`, `+0xA3B` with flag `+0xA3C`), then binds the handler **`0x5336DD0`** to `vehicle + 0x3C0`.
- Handler `0x5336DD0(this, index, old, new)` (index below the instance count at `+0x9F8`):
  - The two optional thresholds decide visibility: with `+0xA3C` set and `new >= [+0xA3B]` the instance is flagged (`0x533BAE0` writes the flag at record `+0x25` and refreshes the instance); the show / hide argument passed to `0x533B6F0` follows `new >= [+0xA39]` when `+0xA3A` is set.
  - `0x533BA20(this, index, a, b)` then stores two floats clamped to 0..1 in the 40-byte instance record (`+0x1C`, `+0x20`): **state 0 (intact) a = 0, b = 0; state 1 (damaged) a = 1.0, b = 0; state 2 (destroyed) a = 1.0, b = 1.0** (the 1.0 is the float at `0x9AADA28`). These are per-instance render values (custom data of the instanced mesh); the function then calls a vtable slot `+0xBB8` to refresh.
- So the damage-state response of the only listener is **visual**: wheel mesh instance visibility and two 0..1 custom values. It reads no friction, radius, stiffness or other wheel-asset field and has no indexed `Values[state]` load.
- The other consumer of the state change inside `0x5370A40` is `0x53AA370` per wheel record (round 47): it moves the mesh from resolved floats at record `+0x2D8..+0x310`; nothing state-indexed there either. `0x5316430` has one caller, so no second listener is bound through it. Not excluded: a listener added by another route.

Result for the data: the wheel asset's per-state arrays (intact, damaged, destroyed order) still have **no native reader found**: not in the change notification, not in the one listener, not in the per-wheel mesh move. They may be read at set-up (`0x5356470`, copies resolved floats) or by code outside the statically readable range; NATIVE and open. The wiki must not assign friction or radius effects to the damaged or destroyed state from this build. Next step: read `0x5356470` for a state index, or trace the record floats `+0x2D8..+0x310` across a state change (needs a run, not allowed here).

## Wiki updates

- Emplacement cash (Placed vs Placed in FOB): "the registry uses the first table that has the row name (Built first)" is now confirmed (the runtime source list is built in `DataSources` order). Add that the client contains no request for these tables (the registry type name is absent from the executable and from every asset except the registry itself and the Spotting add-on), so what is paid on placing is decided outside the client; state the Built, Placed and Placed in FOB amounts as table values, not as the confirmed payout.
- Vehicle wheel damage values: the wheel damage state is delivered to the wheel mesh component, which only hides or shows wheel instances and sets two render values (intact 0 / 0, damaged 1 / 0, destroyed 1 / 1); the physical effect of a damaged or destroyed wheel (friction, radius) is still not located.
