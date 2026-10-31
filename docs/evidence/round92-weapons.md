# Round 92: weapons, attachments and ammunition, open items re-read in the DeepExtract corpus

Static analysis only. Nothing was run and no protected function was touched. Source: the DeepExtract export of the same restored CL-516586 executable (see [DECOMPILATION_CORPUS](../DECOMPILATION_CORPUS.md)), read as pseudocode and checked against the assembly for every offset and constant cited. RVAs are relative to the image base. The older corpus supplied reflected names, vtable slots and class layouts only. No Blueprint bytecode for the weapon, animation or camera Blueprints is available, so every item whose last step is Blueprint is left open with that reason.

## Statuses

| # | Item | Status | One-line answer |
|---|---|---|---|
| 1 | `FireAnimBlendTargets`, `BufferedFireAnimBlendTime` consumers | Resolved | Read by the extension shot handler `0x6C9C000` and the action-event handler `0x6CA1840`; they build an item animation message whose target byte is a four-bit mask (`0x6C6FB20`). |
| 2a | How the camera applies the iron-sight camera offset and sight position offset (native part) | Resolved | The first-person animation instance copies them (`0x6A80880`, `0x6A80060`, `0x6A89880`, `0x6A89A90`); a sight can override the camera offset. |
| 2b | What uses those animation-instance fields | Still open | No native reader of `SightCameraOffset`; the use is in the animation Blueprint. |
| 3 | Reader of the `WDInventoryFragment_TransferTime` fragment | Resolved | `0x6C4F5C0` replaces the rule default with the fragment value; with a second item that has its own fragment, it takes the larger of that and the value held. |
| 4 | Camera code reading the bipod `CameraLocationFOVOffsetCurve` | Still open | The curve is copied into three bipod state objects; no native function evaluates it. |
| 5 | How the vendor applies per-ammunition magazine prices | Resolved (with a correction) | A purchase names a variation; that row's own price is charged and its ammunition pattern is granted. A variation is a pre-loaded magazine. |
| 6 | `TimeAfterFireToRechamber` consumer | Still open | No native read of `+0x290` among the functions that fetch the data block. |
| 7 | Order modifiers apply across the weapon and its attachments | Still open | A run-time sequence; the Override evaluator re-confirmed. No value depends on it. |
| 8 | Native use of the unused slot archetypes `MountLeft`, `MountRight`, `MountTop`, `MountUnder` | Resolved (not used) | The four tag globals are referenced only by their registration and exit-time destructors. |
| 9 | Do the other parts act through code (the part model) | Still open (data layout settled) | Barrel, grip, handguard, stock and underbarrel data are the bare base struct; the part model itself is in the item actor. |
| 10 | Bool `+0x2B8`, int `+0x2BC`, float `+0x2C0` of the mag packing asset | Still open (defaults found) | Defaults are true, 1 and 0.08; no reader found. |
| 11 | M4 grip fixed-zero recoil: replaces or multiplies | Resolved | Replaces; the evaluator `0x522E5C0` returns an active Override and ignores every other modifier. |

## 1. Fire animation blend settings (resolved)

Class layout: `WDItemExtensionData_RangedWeapon` holds `FireAnimBlendTimeCurve` at `+0x148`, `FireAnimBlendTargets` at `+0x1D0`, `FireAnimBlendOption` at `+0x1D4` and `BufferedFireAnimBlendTime` at `+0x1D8`. The weapon extension reaches the data block through the base item-extension field (`+0xE0`), and native code that wants it checks the class (class getter `0x6C8EAD0`). The 24 functions that call that getter, and the 9 callers of the item-data getter `0x6A7E0E0`, were searched for reads of those offsets.

- `0x6C9C000` (extension vtable slot 201, entered through the interface sub-object, so its `this` is the extension plus `0xF0`) evaluates the curve at `data + 0x148` (`0x6C9C2C1` loads the address, the evaluator is `0x6C26830`, call at `0x6C9C2D7`). The input is the owner's clock (a double at owner `+0x840`) minus the last-shot stamp held in the weapon component (`+0xFE8`, written by the fire function `0x6B93610` at `0x6B94597`). Whether the stamp is already updated for the current shot when this handler runs was not traced, so the input may be the time since the previous shot or close to 0. A result above 0 is used.
- Otherwise, or in addition, the buffered value held in the extension at `+0x3C4` is used: `0x6C9C29B` compares it with 0, and `0x6C9C2A8` clears it and jumps to the send path. So 0 means off.
- `0x6CA1840` (`OnWeaponFireActionEvent`) writes `+0x3C4` from the data `+0x1D8` (load `0x6CA197C`) when the action event type is 4 (`BufferQueued`) and clears it for type 5 (`BufferCancelled`). The event-type enum is in the older corpus.
- Send path: `0x6C9C2E1` loads the low byte of `FireAnimBlendTargets`, `0x6C9C2F1` stores the constant 3 as the blend option (the engine `EAlphaBlendOption` value 3 is `Sinusoidal`), and the message is broadcast with the `WDItemAnimationMessage` struct (getter `0x69C8AD0`, broadcast `0x4D49E50`, call `0x6C9C33C`). The message default for the target byte is 15.
- `FireAnimBlendOption` (`+0x1D4`): the only function found reading a byte at `+0x1D4` in the weapon code (`0x6C14180`) is a copy of a different struct. No reader among the fetchers above, so the data value is not what is sent.
- Receiver: the Holdable extension registers a listener for the message in `0x6C6FF40` (vtable slot 159) with callback `0x6C6E3D0`. The callback branches on stop (`+0x38`), jump (`+0x40`) and a blend time below 0 (`+0x60`, uses default blending), otherwise calls `0x6C6FB20` with the blend struct (`+0x58`) and the target byte (`+0x68`).
- `0x6C6FB20` tests the mask against four animation slots of the message: bit 4 (`a2[3]`, the first-person item montage, applied to the weapon component field `+0x100`), bit 8 (`a2[4]`, third-person item, `+0x108`), bit 1 (`a2[1]`, first-person player) and bit 2 (`a2[2]`, third-person player). A slot whose bit is clear gets the default blend (a blend time of -1). The slot order follows `FWDItemAnimation` (first-person player, third-person player, first-person item, third-person item); the first-person or third-person identity of the mesh behind each call is read from that order, not from the mesh classes.

Result: 5 (AK74, Galil) blends the first-person animations; 10 (AMR 50, Compound Bow, MK22, Mosin Nagant, SV98) blends the third-person ones. Not checked: that the curve key is seconds (assumed from the clock).

## 2. Sight offsets (native part resolved, final use open)

Class layout: the first-person animation instance has `SightCameraOffset` at `+0x1228`, and the weapon animation base has `SightPositionOffset` at `+0xC20` and `GripPositionOffset` at `+0xC68`. The data block holds `SightPositionOffset` `+0x240`, `GripPositionOffset` `+0x258`, `IronSightCameraOffset` `+0x270`.

- `0x6A80880` (per-frame update, taking the frame time) loads the three doubles of `IronSightCameraOffset` (`0x6A80BD8`) and stores them at instance `+0x1228` (`0x6A80BF0`). `0x6A80060` (vtable slot 117) does the same on item change (`0x6A801CE`, `0x6A801D8`).
- Later in `0x6A80880`, when the sight struct flag `+0x30` (`bOverrideSightCameraOffset`) is set, the offset is replaced by `(0, v, 0)`: `v` comes from the sight's per-weapon map (struct `+0x38`, keyed by the weapon's item tag) or the default `+0x34` (`0x6A81512` to `0x6A81531`, store `0x6A8153C`). The same branch also overwrites the instance's ADS transition block (`+0xF90`, store `0x6A8154A`). The struct field names come from the SDK layout of `FWDSightData`.
- `SightPositionOffset`: `0x6A89880` copies data `+0x240` (`0x6A8990A`, load `0x6A89919`) into instance `+0xC20` (store `0x6A8991F`) when a sight is attached; `0x6A89A90` repeats it on attachment replication. A non-zero byte at extension `+0x150` replaces the Y part (`0x6A89951`). `0x6A81D10` (vtable slot 121) subtracts it from socket-derived vectors (`0x6A82139`, `0x6A82142`, `0x6A8214B`) and stores `SightAttachmentOffset` (`+0x13B0`) and `RootToSightOffset` (`+0x13C8`).
- `GripPositionOffset`: `0x6A88D20` (weapon animation vtable slot 100) copies data `+0x258` (`0x6A88FB2`) to `+0xC68` (`0x6A88FB9`).
- Open: scans of `[reg+0x1228]` and `[reg+0x13B0]`/`[reg+0x13C8]` in RVA `0x6000000` to `0x7900000` find only writers. The camera modifier chain (`0x76E9F90`, the attachments camera modifier) does not read the offsets. So the final use is in the animation Blueprint; that is why 2b stays open.

## 3. Transfer time fragment (resolved)

The fragment class is `WDInventoryFragment_TransferTime` (64 bytes, `TransferTime` at `+0x38`; class getter `0x69C6960`); the transfer rule has `DefaultTransferTime` at `+0x28`. The rule's native body is vtable slot 86 (`0x6C4F5C0`). It loads the rule value (`0x6C4F9E7`), fetches the fragment of the first item with `0x6C4F1C0` and overwrites the time with the fragment's `+0x38` (`0x6C4FA1D`). When the operation has a second item (flag at operation `+0x32`) and that item has a `WDInventoryFragment_TransferTime`, the larger of its `TransferTime` and the value already held (the first item's fragment time, or the rule default if the first item has none) is used (`maxss` at `0x6C4FA63`). If the second item has no fragment, the value is unchanged. The result is passed as the time argument of `0x677E290`. So the fragment replaces, not adds to, the default.

## 4. Bipod camera curve (still open)

The bipod attachment struct (`FWDBipodAttachmentData`) holds `CameraLocationFOVOffsetCurve` at `+0x60`. Native copies exist in the bipod character modifier (`0x6E94FB0`, call `0x6E95164` into the state at `+0x190`), the bipod mover mode (`0x6DBC390`, call `0x6DBC52D`) and `0x6DC47A0` (curve to `+0x130`). The type check for bipod data (getter `0x69A0F80`) has seven callers (`0x6C9F6E0`, `0x6DBC390`, `0x6DC47A0`, `0x6E94FB0`, `0x6E961F0`, `0x71828F0`, `0x7189EC0`); none evaluates a curve. The direct calls in the bipod modifier and mover-mode vtable slots were scanned for calls to the curve evaluators (`0x6C26830`, `0x3E0DA70`, `0x3E0F4A0`, `0x3E07720`) with no hit. The camera-lock modifiers (slot 92, `0x6E96D90`, calling `0x6E979B0`; curve read at `0x6E97D65`) do evaluate curves, but from a normalised progress value, so they are probably lock-easing curves and not `CameraLocationFOVOffsetCurve`; the curve's source in that function was not traced. The curve evaluation at `0x6DBE2C0` (`0x6DBDE80`, called from the mover mode's slot 99) takes a clamped progress value (not a field of view in degrees), so it is a different curve. None of the seven callers appears to be a camera modifier class (vtable slot 89 list in the older corpus). Conclusion: the evaluation is not in the native bipod classes; likely the control rig or animation Blueprint. Not proven.

## 5. Vendor prices per ammunition type (resolved, corrected)

The magazine vendor rows are `FWDVendorItemVariationData` (416 bytes): `Price` at `+0xE0`, `Amount` `+0xE4`, `bShowInVendor` `+0x188`, `CustomData` (an instanced struct) at `+0x178`. For magazines the custom data is `FWDMagazineItemVariationCustomData`, whose `MagazinePackingData` has a pattern quantity and a list of (ammunition type tag, quantity), for example 30 rounds of `Id.Item.9mm.Tracer`.

- The purchase handler `0x762E0A0` takes the variation tag from the request, finds the row with `0x6BCDB20`, and charges that row's `Price` times a factor read at `+0x39C` of an object it holds (load `0x762E3B8`, `mulss` at `0x762E3CB`, converted to an integer for the affordability call).
- The item grant path (`0x6BD6DB0`, `0x739FE50`) type-checks the custom data against the magazine struct (getter `0x6BE7630`) and, when the pattern list is not empty, expands it with `0x6BED650` into the magazine plus ammunition entries: each pattern entry's quantity is capped by the pattern quantity and by the magazine's capacity.
- Correction: the page text said the non-standard rows are "prices for loading that ammunition type". They are the prices of the magazine bought already loaded with that type; the standard row is the one shown in the vendor list. Not traced: whether the vendor UI shows the other rows (they have `bShowInVendor` false) or where the price factor at `+0x39C` is set.

## 6. Rechamber delay (still open)

`bRequiresRechamberAfterFire` (`+0x28D`) is read in `0x6CA0A70` (extension vtable slot 191, test at `0x6CA0B7E`; the function calls `0x6C93590` only when the flag is false and a tag test passes, so it is a gate, not the rechamber timer). `TimeAfterFireToRechamber` (`+0x290`) has no read in the 24 fetchers of the data block or the 9 callers of `0x6A7E0E0`. The timer that starts the rechamber is not in native code that fetches this block.

## 7. Modifier order across the weapon and its attachments (still open)

The evaluator `0x522E5C0`: the Override list is checked first (`0x522E5E2` to `0x522E5EC`); an active entry returns its magnitude at `0x522E74E` and the sums and product are never reached. Elements are appended in application order (`0x5227C20`) and removed by swapping the last into the freed slot (`0x52357B0`). The replay of attachments on replication walks the array in order (`0x6C9A330`, calling `0x6C9D170` per slot). The sequence in which sub-slots receive their items on the server follows the sub-slot update messages, which depend on equip history. No static order exists to read, and no computed value depends on it (no two parts that fit together override one attribute). Nothing in `_tools/` or the tables needs a change.

## 8. Unused slot archetypes (resolved: not used)

`Item.Attachment.MountLeft`, `MountRight`, `MountTop` and `MountUnder` are registered by `0x129E230`, `0x129E2D0`, `0x129E370`, `0x129E410` (tag globals at `0xD36C260`, `0xD36C268`, `0xD36C278`, `0xD36C270`). A scan of the whole `.text` for references to those four globals found only the registrations and the exit-time destructors (`0x99F8BB0`, `0x99F8BC0`, `0x99F8BD0`, `0x99F8BE0`). The neighbouring slot tags are read by many functions (32 functions in the weapon and animation range `0x6000000` to `0x7900000` reference the sight or bipod tag at `0xD36C280` or `0xD36C2A8`). The tag names occur only in the four registrations. Not excluded: a tag built from a string at run time.

## 9. Part model (data layout settled, model open)

The older corpus gives the attachment data struct sizes: base `FWDBaseAttachmentData` 80 bytes (type tag, two effect lists, two flags, animation set, two audio events); barrel, grip, handguard, stock and underbarrel 80 bytes each (no extra field); muzzle 192, magazine 112, sight 160, bipod 376. So the five plain part types carry nothing that native code could read beyond the base fields. What a part does with its mesh belongs to the item actor and its Blueprint, not in the corpus. Item weight, grid and tag reads for attachments were not searched.

## 10. Mag packing asset scalars (still open)

The constructor of `UWDInventoryMagPackingData` (`0x69CB4A0`) sets `+0x2B8` = 1 (`0x69CB5B0`), `+0x2BC` = 1 (`0x69CB5B7`), `+0x2C0` = 0x3DA3D70A, that is 0.08 (`0x69CB5C1`), and `+0x2C4` = 12 (`0x69CB5CB`). The shipped asset stores 48 at `+0x2C4` and the others stay at their defaults. The asset is held by the inventory component (`+0xB20`); every function that loads that pointer or calls its getter `0x6B52180` was checked for reads of these four offsets, with none. The class getter `0x69C9150` has no native caller. The readers may be in Blueprint or in a callee that receives the pointer as an argument; the meaning stays unknown.

## 11. M4 grip recoil (resolved)

The effect (index 91 in the exported effect values) carries `HorizontalRecoilMultiplier` and `VerticalRecoilMultiplier` with the `Override` operation and value 0. `0x522E5C0` handles Override by returning the first active entry's magnitude and skipping the other operations (see 7). So the grip replaces the recoil multipliers: foregrip, muzzle and stance multipliers are ignored while the grip is fitted. This confirms what the calculator already does (`=` Override in the tool). Not measured: the in-game recoil.

## Wiki updates

- [`content/Wardogs_RangedWeaponFields_v1.md`](../../content/Wardogs_RangedWeaponFields_v1.md): rechamber delay (reader search), sight offsets (native copies, sight override), fire blend settings (consumer, mask), bipod curves (copies, no native evaluator), magazine price points (variation = pre-loaded magazine), transfer time (replaces).
- [`content/Wardogs_WeaponAttributes_v1.md`](../../content/Wardogs_WeaponAttributes_v1.md): section 5 and Override order note, change-log row dated 2026-10-31.
- [`game-features/Wardogs_AttachmentsPlatforms_v1.md`](../../game-features/Wardogs_AttachmentsPlatforms_v1.md): "Unexplained and not traced": part model, unused slot archetypes, source/target pointer to the Ammo Packing page.
- [`game-features/Wardogs_AmmoPacking_v1.md`](../../game-features/Wardogs_AmmoPacking_v1.md): limitations bullet for the four scalars (defaults and reader search).
- [`_wiki/attachments/grips.md`](../../_wiki/attachments/grips.md): the M4 grip replaces rather than multiplies.

For the lead (not edited, generated): `_tools/ammo_packing_tables.py` line 104 still emits "meaning not traced" for the `+0x2C4` row; it could point to the limitations bullet.
