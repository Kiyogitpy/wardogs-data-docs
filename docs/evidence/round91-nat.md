# Round 91, teammate nat: small native traces (V5-09 to V5-13)

GitHub-only page. Static reading of the restored executable (`WardogsClient-Win64-Shipping.restored.exe`, capstone and pefile) and the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__` (unreviewed decompiler output; all addresses are RVAs). Nothing entered the Elytra layer; the game was not run. Everything below is a static reading, not confirmed at runtime. Helper scripts are the round 88 set (`q.py` body lookup, `scan.py` displacement scan, `disa.py` disassembly).

## Status

| Item | Status | Result |
|---|---|---|
| V5-09 FOB spacing geometry | FOUND | See section 1. A pair of point-in-oriented-box tests with half-size 4,200 units (42 m) on all three axes, run in both directions. Not a sphere. |
| V5-10 placeable reach 400 and angle 30 | FOUND | Consumers are in the placeable item extension class code at `0x6C8B660` (angle) and `0x6C8BC30` (reach); round 88 scanned the wrong range (`0x85C0000`-`0x8600000`). 30 is degrees of surface slope, 400 is centimetres of trace reach. Section 2. |
| V5-11 `CombineAmmo` order | FOUND | Low list index is the target (load factor `+0x68`, map `+0x218`), high index is the source (extract factor `+0x6C`, map `+0x1C8`). Section 3. |
| V5-12 input to action-tag mapping | NOT LOCATED (native contract FOUND) | The mapping from input tag to the action that is started is Blueprint logic not present in the exports; the native hooks are read. Section 4. |
| V5-13 EQS parameter table | FOUND (data) | Generator `_tools/ai_eqs_table.py`, block in `game-features/Wardogs_GameFeatures_AI_v2.md` section 9.1. Section 5. |

## 1. V5-09 FOB spacing (`0x85FDBE0`)

`this` (`r13`) is the FOB subsystem (`UWDForwardOperatingBaseSubsystem`): array of deployed FOBs at `+0x50`, count `+0x58`; second array at `+0x68`, count `+0x70`. Constructor `0x85E0810` stores `+0x88` = 2000.0, `+0x8C` = 200.0, `+0x90` = 200.0, `+0x94` = 20.0, `+0x98` = 20.0 (floats `0x44FA0000`, `0x43480000`, `0x43480000`, `0x41A00000`, `0x41A00000`). Arguments: `rdx` = candidate location (3 doubles), `r8` = candidate rotator.

1. `0x4529050` returns the world; `0x45C4DC0` is the net-mode getter (returns 3 for a client, 2 for a listen server, 0/1 otherwise; it reads the "listen" URL option). Net mode 3 jumps to the second loop (`0x85FDDF1`).
2. Normal loop (`0x85FDC4C`..`0x85FDDEA`): for every entry of the `+0x50` array that is valid and has byte `+0x1B0 != 1`, take its component at `+0xC8`, then that component's `+0x1C0` data (location doubles at `+0x230`, `+0x240`), the rotator from `0x3A95220` (derived from the quaternion at `+0x210`), and `M = 2 * [this+0x88] + [this+0x8C]` = 4,200. Build an FBox: min = location - M, max = location + M on all axes, valid byte set (`movups`/`subpd`/`addpd` at `0x85FDD2D`-`0x85FDD5E`).
3. Test A (`0x85FDD63`): `0x6C26B80(box, rotator, candidate location)`. `0x6C26B80` (read from its disassembly) takes the box centre and half-extents, un-rotates the point by the rotator with a rotation matrix and returns true only when every local coordinate satisfies `-half < c < half` (strict `comisd` pairs at `0x6C26E0E`-`0x6C26E42`). True refuses the placement.
4. Test B (`0x85FDDD0`): the same function with a box of half-size M around the candidate location, the candidate rotator (`r14`) and the existing FOB's location as the point. True refuses.
5. No overlap for all entries returns 1 (`0x85FDDEA`). Any hit returns 0 (`0x85FE0FC`).
6. Second loop (net mode 3): iterates `[this+0x68]` in 16-byte elements; each element holds a pointer to an array of 12-byte weak pointers (`+0x10`, count `+0x18`). It takes the first live actor, finds a component by class, reads a flag byte (component `+0x1B0` or `+0x80`; value 1 skips) and runs the same two tests with the component's location (`0x5402A90`) and rotator (`0x5402B30`), M from the same two fields.

Reading: a new FOB is refused when its position lies inside the 84 m cube (half-size 42 m) around an existing FOB, measured along that FOB's own axes and including height, or when the existing FOB lies inside the cube around the candidate. A cube, not a sphere: the horizontal refusal reaches about 59.4 m on a diagonal; a candidate more than 42 m above or below is allowed. Rotation is the FOB's yaw, so the square follows its orientation.

The safe-zone (300 units) and ladder (100 units) tests are not in this function: they are the Blueprint `B_SafeZonePlacementCondition` and the native sphere `WDWithinLadderBoundsPlacementCondition`, already described in Buildables 14.4. The wrapper `0x85FE4D0` reports the failure with the tag at `qword_14D3E6ED0`.

Not located: readers of subsystem `+0x90`, `+0x94`, `+0x98`. A scan of `0x85E0000`-`0x8602000` for those displacements finds only the constructors (`0x85E0810`, and other classes at `0x85E0960`, `0x85E0CE0`). `0x85EDD60` is a second reader of `+0x88` and `+0x8C` (the same `2 * a + b` margin, with a role-3 owner check and the same box function); its purpose was not read further.

## 2. V5-10 placeable reach and angle

Fields: `UWDItemExtensionData_Placeable` `+0x48` `MaxPlacementDistance`, `+0x4C` `MaxPlacementAngle`, `+0x50` `bCanPlaceOnOtherPlaceable`, `+0x58` `PlacementCollisionSize`, `+0x70` `PlaceableClass`, `+0xAC` `BlockedReason`, `+0xB8` `BlockedActorClasses`. Route that worked: the extension component's own class code. The vtable `UWDItemExtension_Placeable_VFT` (aliases table) overrides slots 0, 61, 128, 129, 131, 165 and 166 with `0x6C8xxxx` functions, so the class code is `0x6C89000`-`0x6C8E000`. A displacement scan of that range for `0x48`, `0x4C` finds:

- `0x6C8A7F0` (data class constructor): `+0x48` = `0x437A0000` = 250.0, `+0x4C` = `0x42340000` = 45.0, `+0x50` = `0x01010101`. So the shipped values 400 and 30 are data overrides of class defaults 250 and 45.
- `0x6C8BC30` (the preview trace, `a2` is a 256-byte FHitResult it zeroes): gets the view point from the pawn (virtual slot at `+1824`), the placeable class default object via `PlaceableClass` (`+0x70` = `v11+112`) and its bounds extent (`0x3A...` helper `0x143DC0880`). Trace length = `MaxPlacementDistance` (`v11+72`) + 2 * bounds extent X; end = start + direction * length. The trace collects three objects into an ignore list (the placeable actor, the pawn and one more object taken from `a1+264`; exact identities not decoded). The trace runs through `0x143CAB670` (line trace by channel with an ignore list).
- `0x6C8B660` (validation, returns bool): after the preview trace it computes `acos(clamp(hit.ImpactNormal.Z, -1, 1)) * 57.295776` (FHitResult `+0x68`, `0x6C8B831`-`0x6C8B849`, `acosf` at `0x98F814C`), i.e. the angle in degrees between the surface normal and straight up, and compares it to `MaxPlacementAngle` (`comiss xmm0, [r15+0x4C]`, `ja` at `0x6C8B85B`). Above the limit, or when the extra overlap test `0x6C8C950` (uses the collision size `+0x58`) fails, the blocked reason tag at `+0xAC` is reported. The angle test runs only when the hit component blocks the Visibility channel (the call through the component vtable `+0x5E8` with argument 3 must return 2). Other tests in the same function, read from the decompiler output but not decoded in detail: a check against `+0x50` (`bCanPlaceOnOtherPlaceable`), a loop over the array at `+0xB8` (`BlockedActorClasses`) against the hit actor, and a final call (`0x1477222C0`, with the data's `+112` field) that decides the remaining result.

So 30 means 30 degrees of slope (surface at most 30 degrees from level; the IED's 180 disables the test) and 400 means 400 centimetres of reach from the view point (plus the placeable's size allowance). `CanPlace` (UFunction) has no reflection thunk in the corpus; `0x6C8B660` is the best candidate for its body (inference: same class, takes the placement data and a hit result, returns a bool, and notifies listeners at `a1+240`).

Why round 88 failed: it searched `0x85C0000`-`0x8600000` (buildable placement) and the conditions list; the item extension code sits at `0x6C8xxxx`, found by taking the vtable slot overrides of `UWDItemExtension_Placeable_VFT`.

## 3. V5-11 `CombineAmmo`

`CombineAmmo` is `0x6B554B0` (round 41 name; large function, decompiler output saved in the work folder). The loop at `0x6B554B0` lines around the second call of `0x6B5E500`:

- Two indices `i` (starts 0) and `j` (starts count - 1) walk 248-byte item entries of one operation group; entry `i` = `v130`, entry `j` = `v131`. The loop runs while `i < j`.
- Capacity: `v135 = [item data of entry i + 136]` (the item's cap). Target rounds: `v138[6]` (`+24` of the per-item record of entry i). Source rounds: `*v145` (`+24` of entry j's record).
- If target rounds >= capacity, `i` advances. If source rounds <= 0, `j` decrements. Otherwise `n = min(source rounds, capacity - target rounds)`.
- `0x6B5E500(inventory, tag, n, 1, extractData = entry j's magazine data, loadData = entry i's magazine data)`. In the helper: `if (a4 && data asset valid)`: extract term = `curve(+0x1C8 map by tag, else +0x30 default at n)` x `0x6C3B040(extractData)` (the `+0x6C` factor); load term = `curve(+0x218 map by tag, else +0xB8 at n)` x `0x6C3B070(loadData)` (the `+0x68` factor); result = load + extract. The asset is `[inventory + 0xB20]`.
- After the call: `target[6] += n` and `source -= n` (`0x6B554B0` lines `v306[6] += v146; *v305 -= v146`).
- The first call site (line 794) passes `a4 = 0` and no extract data, so only the load term with the target magazine's `+0x68` factor is used (a path without a source magazine; which operation it serves was not read).

So: source = high index (extract map `+0x1C8`, factor `+0x6C`), target = low index (load map `+0x218`, factor `+0x68`). Curves are read at `n` (the rounds moved in that step).

## 4. V5-12 input to action

Native pieces (SDK offsets from `BHActionSystem_classes.hpp`):

- `UBHGameplayAction`: `OnInputTriggered` multicast delegate at `+0x28`, `InputMappingContext` at `+0x50`, `ActionTag` `+0x58`, `ActionDefinition` `+0x60`.
- `UBHGameplayAsyncAction_WaitForInput` (`WaitForInput(action, tag, bool)`): constructor `0x5249FF0` zeroes `+104`/`+112`, stores the null tag at `+120` and `0` at `+128`; vtable `UBHGameplayAsyncAction_WaitForInput_VFT`. The activation function `0x5250200` (referenced by a pointer at `.rdata 0xAAD1710`) resolves the owner action from `+56`, binds the node's `OnInputTriggered` function (looked up by the string `&ThisClass::OnInputTriggered`) as a delegate, and appends it to the action's array at `action+40` (16-byte entries, count at `+48`); on a client (net mode 3, via `0x45C4DC0`) with the flag byte set it calls `0x5252660`.
- The UFunction thunk `reg_OnInputTriggered_52694E0` (the node's `OnInputTriggered(tag)`): if the received tag equals the stored tag (`a1[15]`) it clears `+104` and calls virtual slot 89 (`+712`), the `Triggered` broadcast.
- Input side: `BHInputAction` has `InputTag` at `+0x78`; `BHEnhancedInputComponent::SimulateInputKeyBP(tag, type)` exists for synthetic input.

What was not found: the code that decides which action tag to start for which input tag. The action base class has no table; the character's input functions in the SDK are UI only (`InputInventoryOpened`, `InputMapOpened` and so on); the action Blueprint classes (`B_Action_*`) and the character Blueprint are not part of the data export (only the `DA_Action_*` definitions are), so a mapping kept in a Blueprint graph cannot be read. The native caller of `TryActivateAction` for movement was not located in the time-box. Status NOT LOCATED, not PROTECTED.

What can be said from names, **Derived**: 12 of the 98 input actions have a same-suffix action tag (`Jump`, `Crouch`, `Prone`, `Sprint`, `Lean`, `Lean.Left`, `Lean.Right`, `MoveDirectional`, `Focus`, `SlowWalk`, `Appliable.PrimaryUse`, `Appliable.SecondaryUse`). Default keys come from the `DefaultKeyMappings` of [`IMC_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_Player.json) and [`IMC_PlayerAiming`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_PlayerAiming.json) (Space/A jump, C crouch, Left Ctrl prone, Left Shift sprint with a Released trigger, Q/E lean in [`IMC_Player`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_Player.json) with bumpers in [`IMC_PlayerAiming`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/IMC_PlayerAiming.json), W/A/S/D move, Left Shift/left stick focus while aiming). The table is in ItemActions 9.1.

## 5. V5-13 EQS parameters

No new extraction: `assets/data/ai-eqs.json` (round 41) already resolves every query. New generator `_tools/ai_eqs_table.py` (stdlib; `--write`, `--check`) writes the per-option parameter table into `game-features/Wardogs_GameFeatures_AI_v2.md` section 9.1 (22 queries, 25 options). There is no `_tools/pipeline_registry.json` on this branch, so the new script is listed in the report instead.

## Files changed

`game-features/Wardogs_Buildables_v1.md`, `game-features/Wardogs_FireAndUtility_v1.md`, `game-features/Wardogs_AmmoPacking_v1.md`, `content/Wardogs_ItemActions_v1.md`, `game-features/Wardogs_GameFeatures_AI_v2.md`, `_wiki/building.md`, `_wiki/building/forward-operating-base.md`, `_wiki/equipment/claymore.md`, `_wiki/equipment/fire-smoke-and-flash.md`, `_wiki/ammunition/ammo-packing.md`, `_tools/ai_eqs_table.py`, this page.
