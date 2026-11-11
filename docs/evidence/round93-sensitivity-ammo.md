# Round 93: mouse sensitivity and ammo-packing units

Static follow-up to [round 80](round80-mouse-sensitivity.md), [round 41](round41-weapons.md) and [round 92](round92-weapons.md). This note resumes retained function excerpts rather than restarting the survey. No game, live memory, driver or configuration operations were performed. RVAs refer to the restored CL-516586 image identified in [DECOMPILATION_CORPUS](../DECOMPILATION_CORPUS.md): SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`, image base `0x140000000`. Decompiled types and argument lists are not authoritative; the decisive offsets, argument forwarding and clock writes below were checked against assembly, with selected windows independently decoded from that image.

## Disposition

| Gap | Disposition | What is established / still missing |
|---|---|---|
| **G1: display/store mapping** | **Closed-static, with a precision correction** | The numeric setting uses an affine, clamped range conversion with display-increment quantization. Maximum really defaults to 1.0. The formula is not an unquantized identity. |
| **G1: actual degrees per physical mouse count** | **Open; the published `0.07 × S` is not established** | Native selection distinguishes raw key values from axis-massaged values. The traced Enhanced Input mapping takes the former. This defeats the argument that a `BaseInput.ini` sensitivity of 0.07 automatically establishes that factor on this path. It does **not** by itself prove a replacement physical-count calibration. |
| **G4: unit of the curve-derived operation duration** | **Closed-static for the traced native duration contract** | Curve output becomes an operation duration without conversion, then a timer delay in the same units as the world's seconds clock. No gameplay timing measurement is needed to establish this unit. Exact observed completion time and alternate execution branches remain separate. |

These are per-obligation dispositions, not blanket closure of mouse handling or inventory behavior.

## G1 — the numeric setting bridge

### Asset → native parameters

The `UserSettings.Controls.Mouse.Sensitivity` row of [`DT_Settings_Controls`](../../data/Wardogs/Content/GameMechanics/Settings/Controls/DT_Settings_Controls.json) selects [`DA_Setting_Controls_Sensitivity`](../../data/Wardogs/Plugins/BHFramework/Content/Settings/Controls/DA_Setting_Controls_Sensitivity.json). Its parameters are Minimum 0.1, Default 0.4, `bMaskValue=true`, DisplayMinimum 0.1, DisplayMaximum 2.0 and Increment 0.01; Maximum is omitted.

The native numeric-data constructor `0x4E1F680` settles the omitted maximum directly: the write at `0x4E1F6A9` puts float 1.0 at object `+0x34`, i.e. parameters `Maximum` at `+0x04`. The same constructor initializes Minimum 0, Default 0, mask false, DisplayMinimum 0, DisplayMaximum 1, Increment 0.1 and FractionalDigits 2. The asset overrides the fields it serializes. This replaces round 80's inference about Maximum from unrelated settings.

`UBHUserSettingNumeric` initialization `0x4E3B8B0` obtains the selected numeric data, copies the parameters from data `+0x30` into setting `+0x1A0` through `0x4E23930`, and chooses stored versus display bounds using `bMaskValue` (`0x4E3BB48–0x4E3BB6C`). The offset meanings are corroborated by `FBHNumericSettingParams` in the SDK; they are also independently consistent with the constructor writes.

### Selection → display → edited value

The native numeric view model supplies both directions, not merely a generic engine convention:

- `0x73EB120` binds a numeric setting to view-model `+0x260`.
- `0x73EAE80` calls parameter getter `0x38C2830` (setting `+0x1A0`), selects display endpoints when the mask is set (`0x73EAF35–0x73EAF6F`), and constructs the stored and displayed range pairs at view-model `+0x268` and `+0x278`.
- `0x73EB1A0` reads the current stored value, calls `0x53841A0` from the stored range to the displayed range, rounds to the display increment, and stores the display value at view-model `+0x288`.
- `0x73EB4E0` quantizes the edited display value, calls the same helper with the two ranges reversed, and passes the resulting stored value to `0x4E43630`. That function writes the numeric value state at `+0x58` and notifies listeners when it changes. This is the native setting-value bridge; it is not a claim about the contents of a particular user's saved configuration.
- `0x53841A0` computes the clamped affine mapping. Its small-denominator branch handles a degenerate source range. The sensitivity ranges here are nondegenerate.

For this asset, before quantization:

```
d = 0.1 + clamp((S - 0.1) / 0.9, 0, 1) × 1.9
S = 0.1 + clamp((d - 0.1) / 1.9, 0, 1) × 0.9
```

For positive sensitivity values the display quantization is `0.01 × floor((d + 0.005) / 0.01)`, subject to ordinary floating-point rounding. `0x4E3B8B0` also normalizes both the default and current numeric value by mapping to the display range, quantizing, and mapping back (`0x4E3BB6C–0x4E3BD61`). It therefore matters whether “default 0.4” means the serialized asset value or the normalized numeric value state.

| Case | Derived result |
|---|---|
| Serialized S = 0.4, affine projection only | d = 0.733333… |
| That projection after the native 0.01 display increment | d = 0.73 |
| Inverse conversion of display 0.73 | S ≈ 0.398421052632 |
| Inverse conversion of display 1.00 | S ≈ 0.526315789474 |

Thus “the asset default is 0.4 and displays about 0.73” is appropriate. “The edited display value 0.73 is exactly stored 0.4” is not. No on-screen observation is claimed.

## G1 — why 0.07 is not yet a physical-count calibration

### A concrete native selection invariant

Round 80 found `Sensitivity=0.07` in the shipped base input config but explicitly did not prove its selection by Enhanced Input. The resumed trace reaches the relevant producer and consumer:

| Stage | Native evidence | Result |
|---|---|---|
| Input events accumulate values | `0x458D1C0` | Event float `+0x2C` is accumulated into key-state data, including the component accumulation used to construct vector keys. |
| Per-frame key values are assembled | `0x4583020`, especially `0x45831B4–0x4583204` | Accumulated components are copied into the key record's raw vector at `+0x18`. |
| Axis properties are evaluated separately | `0x458334B–0x45833F4` | Virtual slot 100 (`+0x320`) computes the scalar massaged value; slot 99 (`+0x318`) computes the vector massaged value. Their results go to record `+0x30`, not `+0x18`. Here the assembly's `rbx` already points at record `+0x18`; its additional `+0x18` destination is record `+0x30`. |
| The configured axis sensitivity lives on that massaging path | `0x4590360`, `0x45905F0`; property-cache initializer `0x4574D60` | The axis-property sequence performs dead-zone/exponent/sensitivity/inversion work; the scalar/vector routines multiply by the cached sensitivity. |
| Shipped input-class selection | `UBHEnhancedPlayerInput` vtable, slots 90, 91, 92, 99, 100 | Same-image pointers select `0x4CE3520`, `0x4CE2FB0`, `0x4CEB340`, `0x45905F0`, `0x4590360`, respectively. This is not an assumed inherited override. |
| Enhanced mapping fetch | `0x4CE3FC0`, decisive `0x4CE4053` | Looks up the key record and returns **record +0x18**, not record +0x30. |
| Enhanced mapping consumption | `0x4CEB340` → `0x4CEC530` → `0x4CDF7D0` | The mapping processor fetches that raw vector, constructs the action value, and applies the mapping's modifier list. `0x4CDF7D0` walks that list and dispatches via `0x4CE91D0`. |

The normal input-processing dispatch at `0x4593B21` calls virtual slot 90, whose `UBHEnhancedPlayerInput` target `0x4CE3520` calls `0x4583020` at `0x4CE393E`. The next dispatch at `0x4593B3C` calls slot 91. This provides a real producer/selection bridge rather than relying on adjacent function names. Some exported function boundaries are fragments: `0x4CE351F` is not a usable decompilation of the entry at `0x4CE3520`; the retained direct disassembly is used instead.

A counterexample at this **native key-state boundary** is enough to reject the old justification: if raw X is 1 and the massaged X is 0.07, `0x4CE3FC0` still supplies 1 to the Enhanced mapping modifier list. Computing 0.07 in the massaging routine does not make it the selected value. This is a source-derived boundary example, not an emulated or observed physical mouse movement.

### Shipped mapping and explicit limits

[`IMC_PlayerController`](../../data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IMC_PlayerController.json) maps `Mouse2D` to [`IA_Look`](../../data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Look.json) with `WDApplyAxisConfig_0`. The mapping does not serialize a Scalar modifier supplying 0.07. `0x6BF2B70` selects the default/state axis-setting lists; `0x6BF0090` and `0x6BF0260` apply the named sensitivity setting by multiplication. This confirms the named-setting stage already described in round 80, not the missing physical-count scale.

Do **not** replace the old table with `S degrees/count` solely from this result. The precise remaining obligations are:

1. Bind physical mouse deltas through the platform/viewport event producer into the `0x458D1C0` event values and composite `Mouse2D` state, including any earlier scaling/smoothing. The resumed trace establishes the key-state boundary, not that upstream calibration.
2. Bind the shipped [`IA_Look`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Look.json)/input tag to the controller callback and finish the action-level modifier selection. [`IA_Look`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Inputs/PlayerController/IA_Look.json) serializes a `WDAimAssistInputModifier`; its shared native implementation `0x67646F0` has conditional transform and passthrough branches. Its mere name does not prove mouse passthrough. The controller handler `0x6D4F700` and FOV helper `0x6D4DEB0` are retained, but do not supply the missing upstream calibration or establish all these gates by themselves.
3. Complete the final input-to-view consumer proof if publishing a universal degrees-per-physical-count number. Round 80 itself left its callback binding and final rotation integration inferred.

**Integration recommendation:** keep the now-native display/store rule, including quantization. Withdraw or explicitly quarantine the `0.07 × S` hip/ADS formulas, absolute cm/360 table and 4x absolute-distance example pending those edges. A config entry plus a plausible-looking cm/360 is not substitute evidence. The relative FOV calculation is a separate claim; this note does not retract or re-verify its whole derivation.

## G4 — curves become seconds on the native timer clock

### Producer → selected curve → duration record

The shipped [`DA_InventoryMagPackingData`](../../data/Wardogs/Content/GameMechanics/Inventory/InventoryMagPacking/DA_InventoryMagPackingData.json) selects the curve families. Two previously inferred details now have positive native evidence:

- `0x6C2F100` tries the caliber tag, then its parent repeatedly. `0x6C26830` selects a valid external curve at runtime-curve `+0x80` before the inline rich curve. An inline key does not override a valid external asset.
- `0x6C47420` uses the load map `+0x218` / fallback `+0xB8` for magazine loading, and the combine-loose map `+0x268` / fallback `+0x140` for loose-ammo combination. At `0x6C476DD–0x6C476E8` the bounded integer round count is converted to float and evaluated. The load branch multiplies its selected curve by the magazine's load factor. Both branches pass the resulting float as the duration to `0x677E290` (`0x6C47860`, `0x6C47962`), without a unit conversion.

`0x6B5E500` supplies the two-term magazine-transfer duration: extract curve `+0x1C8` / fallback `+0x30` times the source factor `+0x6C`, plus load curve `+0x218` / fallback `+0xB8` times target factor `+0x68`. The two getters `0x6C3B040` and `0x6C3B070` read those factor offsets, returning 1 when the magazine data is unavailable. `CombineAmmo` `0x6B554B0` forwards the resulting float into the same constructor (`0x6B5618E`, `0x6B56B3B` and `0x6B5747E`). This note does not rename magazine-transfer combination as loose-ammo combination: they are distinct curve selections.

Constructor `0x677E290` stores the supplied float unchanged in operation `+0x10`. Queue insertion `0x679BF70` copies that field unchanged. Queue start `0x67A2520` records world `+0x840` as the start clock at manager `+0x1F8`, then calls virtual slot 168 with the selected operation. The base slot is `0x679B810`. The Wardogs override `0x6C30C90` has validation/special handling and a branch calling that base scheduler. Those gates must not be erased when describing observed operation completion.

### Duration → deadline → seconds clock

The unit proof is the following complete arithmetic bridge for the selected timed native branch:

1. **Duration argument.** `0x679B810` tests operation `+0x10`. Nonpositive values complete immediately. Positive values become the delay argument to `0x3AB8810`, with completion callback `0x678EF30`. The direct loads/stores at `0x679B885–0x679B895` establish the forwarding; there is no multiply/divide by 1,000, frame rate or round count here.
2. **Wrapper ABI.** The decompiler renders `0x3AB8810`'s arguments incorrectly. Assembly at `0x3AB89DE` loads the caller's stack duration into `xmm3`; `0x3AB89F4` calls `0x4552A20`. That thunk transfers to the actual timer-setup body at `0x4552780`. Do not treat the decompiler's uninitialized integer temporary as the delay.
3. **Deadline arithmetic.** The timer body preserves `xmm3` as its float rate, stores it at `0x4552865`, chooses the supplied initial delay or that rate, converts float to double at `0x4552947`, and adds timer internal time `+0x140` at `0x4552954` for an active timer. Pending timers hold the same relative delay until promotion. No unit conversion occurs in either case.
4. **Timer advancement.** `0x455CDB0` advances internal time `+0x140` by its incoming float delta and compares deadline against that time. Pending promotion adds internal time to the saved relative deadline. Its separate performance-counter/millisecond calculation is a callback-processing budget, **not** a conversion of operation duration.
5. **Actual clock source.** In the world tick's recovered native body, the same `xmm6` delta is added to world `+0x840` at `0x40881BD–0x40881C5` and passed to this world's timer manager at `0x408894A–0x4088950`, through the same timer-manager getter `0x45C0110` used by `0x679B810`.
6. **Seconds identity.** Reflected registration aliases `GetTimeSeconds` and `GetGameTimeInSeconds` identify wrapper `0x3F2AB40`; its result is the double at world `+0x840`. Thus the timer delta and deadlines are in the same seconds units as the native exposed world clock, not arbitrary curve units. This is a joined clock read/write and call-argument proof, not inference from a float name.

**Invariant:** for this native timed branch, a curve-derived duration D is D seconds of timer advancement, driven by the world's game-time delta. The native callback becomes eligible once that deadline is exceeded; it is not a promise of exactly D wall-clock seconds from a UI click.

### What this closes, and what it does not

The output unit can be documented as **seconds (native timer-clock trace)** rather than “seconds inferred from curve ranges.” For example, the 5.56 mm load curve at 100 rounds is 30.25; applying factor 0.6 gives a derived duration of **18.15 seconds** under that selection. This is calculated from asset keys and native arithmetic, not measured play.

No further gameplay observation is required merely to establish the seconds unit. Still not established here: exact wall-clock completion, pause/time-dilation effects in a particular session, queue delay, animation/network gates, special per-round/next-tick branches, Blueprint overrides or server behavior. `0x6C2EF60` can partition a duration into chunk intervals; dimensional division by the number of chunks preserves seconds but does not itself prove total observed latency. The unknown packing-asset scalars at `+0x2B8`, `+0x2BC`, `+0x2C0`, `+0x2C4` remain the separate round-92 question.

**Integration recommendation:** update the unit caveat in the [wiki](../../_wiki/ammunition/ammo-packing.md) and [technical page](../../game-features/Wardogs_AmmoPacking_v1.md) to distinguish statically established seconds from unmeasured gameplay timing. Also correct the wiki's wording that loose-ammo combination necessarily adds the extract and load terms: the traced loose-ammo branch selects its own combine-loose curve.

## Verification and retained evidence

Private evidence remains in the existing `published_data_verification/sensitivity-ammo/` investigation folder; no raw corpus was copied into this public-facing note. Existing batch1–9 logs and function excerpts were retained. New targeted queries are in `resume-batch10.log` through `resume-batch12.log`; the new native-byte receipts are `resume-native.txt` and `resume-native-manifest.json`.

Actual local checks:

- New indexed function queries: **exit 0** for batches 10, 11 and 12. One requested fragment entry (`0x4E2DBD0`) was absent; no result is invented for it or needed for the numeric mapping proof above.
- `py -3.13 resume_probe.py`: **exit 0**; rehashed the restored image, checked indexed query selection and decoded **23 bounded windows** from that image. Unwind records are recorded as boundary context, not assumed complete C++ function boundaries.
- `py -3.13 verify_resume.py`: **exit 0**; verified **23 window hashes**, **96 retained excerpt hashes**, **10 exact instruction anchors**, **5 same-image input vtable targets**, a negative control for the competing `+0x30` fetch, and labelled display/rounding/curve arithmetic controls. These counts describe checks, not a semantic-coverage denominator. No target code was executed or emulated.
- The first instruction-anchor check failed because the verifier transcribed slot `+0x320` as `+0x300`; its expected bytes were corrected against the retained assembly and the final run passed. This was a verifier error, not evidence of an input-code change.
- Plain name equality on this SQLite database caused scans/timeouts: the name index uses `COLLATE NOCASE`. Adding that collation to the retained query helper produces `USING INDEX idx_functions_name`; corpus databases remained read-only. The initial uncollated work timed out at 300 seconds and a diagnosis attempt at 60 seconds. No interrupted writer was rerun over old excerpts for cleaner receipts.
- The default tool interpreter lacked `pefile`; the already installed Python 3.13 analysis interpreter supplied the dependencies. An initial full PE parse timed out; the successful probe uses `fast_load` and reads the exception directory directly. These are tooling limits, not missing native code or gameplay failures.

Only this evidence note and files in the owned private investigation directory were changed. Shared wiki pages, gap ledgers, indexes and unrelated worktree edits were left for parent integration; no commit or push was made.

## G1 continuation — device predicate, callback and rotation consumer

This additive continuation preserves the original dispositions and line ranges above. **Physical-count calibration is still open, not replaced by a new absolute scale.** It does close previously inferred downstream edges and identifies the concrete device/state conditions that an eventual calibration must specify. This is static evidence, not an observed mouse trial.

### The action modifier's mouse condition is now identified

The same-image `UWDAimAssistInputModifier` vtable at `0xB3D02F0`, slot 86, selects `0x67646F0`. That body calls `0x4D73FE0`, whose class selector `0x4D70C40` explicitly identifies `CommonInputSubsystem`. Getter `0x3B1F240` reads its byte `+0x91`; the SDK identifies this as `CurrentInputType`, with MouseAndKeyboard = 0 and Gamepad = 1.

At `0x6764788–0x676478F`, a valid subsystem whose type is **not 1** branches to the unchanged-value return at `0x6764A02`. Therefore a valid subsystem reporting MouseAndKeyboard selects passthrough. This is a positive native predicate, not an inference from the modifier's name. Conversely, a missing/invalid subsystem is allowed into the transform path, as is Gamepad, subject to further owner/filter/settings gates. A Mouse2D key does not itself force this subsystem state: mixed-device state and absent-subsystem behavior must not be silently treated as mouse passthrough.

### The input tag really binds the retained callback

Native tag initializer `0x12840B0` associates `Input.NamedActions.Player.Look` with the tag global used by `0x6D4EB80`. That setup function supplies the address of `0x6D4F700` at `0x6D4EC16` and calls binding helper `0x53B50C0` at `0x6D4EC4D`, with event byte 1. The helper resolves the tag through `0x4D06310` → `0x4D062C0`, constructs the binding and appends it to the input-component binding list. The shipped IA_Look asset carries that exact tag.

Thus the callback identity is no longer merely inferred. Binding still requires a valid input component and a successful action lookup. This continuation does not establish the complete initialized tag-map population, active-context priority, action-instance modifier-list construction or per-frame delegate firing for a particular session.

### The callback feeds rotation input, then a gated camera consumer

The handler's assembly is essential: its decompilation omits floating-point arguments at the virtual calls. After obtaining the FOV factor at `0x6D4FC2F`, assembly multiplies the action X/Y components and supplies float arguments to virtual offsets `+0xD48` and `+0xD40` at `0x6D4FC58` and `0x6D4FC87`. Same-image `AWDPlayerController` vtable pointers select:

- `0x42B43E0` for yaw: accumulates into controller `+0x540`;
- `0x42B3F40` for pitch: accumulates into controller `+0x538`.

Both honor an ignore-input predicate at virtual offset `+0x880`. Both also test `InputSettings +0x48` bit 6, identified by the SDK as `bEnableLegacyInputScales`. When clear, the extra legacy multiplier is 1; when set, they use controller `InputYawScale` or `InputPitchScale`. The retained shipped `DefaultInput.ini` explicitly sets `bEnableLegacyInputScales=False`. That is a shipped configuration selection, not proof of a user's effective configuration or the compiled constructor default. In addition, `0x6D4F700` has an earlier input-suppression return and a separate conditional scale feeding these calls; this continuation does not erase either by calling the handler a universal FOV-only multiplier.

The selected update-rotation slot 390 is `0x6D56BF0`, which calls base `0x42E3490` only when controller byte `+0xB38` is zero. The base copies the accumulated rotation input, obtains control rotation, and passes both to camera-manager virtual slot 276. For `AWDPlayerCameraManager` that slot is `0x6D3FA80`: it can first route through `0x6E8BB40`, then calls base `0x42D46B0`, and can apply an additional post-transform. The base permits camera modifiers before adding the three delta components directly to the rotation and then normalizing/limiting it. Finally `0x42E3490` calls controller slot 246, whose same-image target `0x3DD1BC0` writes control rotation at `+0x330/+0x340` after finite/range/change checks.

This establishes an actual callback → rotation accumulator → selected update → camera integration → control-rotation write chain. It also supplies a concrete reason not to publish an unconditional physical-count-to-final-view constant: suppression, update inhibition, camera modification and angular limits can change or eliminate the result. Vehicle/alternate camera contexts are not silently covered by the ordinary-player asset.

### Platform counts: a positive prefix, with the remaining join explicit

Windows input processing `0x19AF7B0` obtains `RAWINPUT` through `GetRawInputData` and passes its mouse payload to `0x19B1670`. For the relative branch (mouse flags bit 0 clear), that helper copies the two signed deltas from payload `+0x0C/+0x10` unchanged. The absolute branch instead performs screen-coordinate conversion and recenter/delta logic: it is not interchangeable with relative mouse counts.

`0x19A2130` carries the selected integer deltas into immediate or deferred message records at `+0x30/+0x34`. The message body entered at `0x19ADE10` supplies those integers to its installed handler at virtual offset `+0x78`, call site `0x19AE3A8`. No sensitivity multiplication occurs in this relative-input prefix.

**The remaining upstream join is not proved here:** the installed handler target and routed viewport event must be connected to the viewport's accumulated mouse values, the InputKey event at `0x458D1C0`, and the selected composite Mouse2D state. The retained viewport producer independently emits MouseX/MouseY events from integer accumulators through `0x3F48C10`, but their equality to the preceding platform deltas has not been established. Nor has intervening smoothing/scaling been excluded. These are unresolved static edges, not evidence that the relevant source bytes are absent or that live access is required.

### Verification and handoff boundary

`py -3.13 count_native.py` completed with exit 0: restored-image SHA-256 matched; 12 bounded native windows and six same-image vtable targets were checked, including the platform raw-handler dispatch and the callback's yaw/pitch dispatches. Private `count-native.json` and `count-native.txt` retain the exact windows. `count_trace.py` uses indexed `COLLATE NOCASE` queries with read-only immutable databases and does not overwrite existing excerpts. Newly retrieved bodies are retained as individual JSON files with batch logs. These checks verify source identity and selected edges, not complete initialized-path coverage.

The exact original report bytes were preserved privately before this append (SHA-256 `98d03f3e1824c772060d0d3bbe8e0977f3a9bce63e79ed0c254684bd351f8e9c`). No UI/ammo conclusion was reopened. **G1 remains partial:** mouse-state aim-assist passthrough and the callback/rotation-consumer identities have positive evidence; the physical-count/viewport join and initialized action selection remain necessary before publishing degrees/count or cm/360.
