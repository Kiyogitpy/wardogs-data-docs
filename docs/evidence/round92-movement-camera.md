# Round 92: movement curves, camera setting, damage-taken handler, fuel drain and the saved-preset hypothesis (R92-MOVE)

Static analysis only. Nothing was run and no protected code was touched. Evidence: the DeepExtract corpus of the restored CL-516586 executable (IDA 9.5 with Hex-Rays; pseudocode and assembly for every function), read function by function by RVA, with tricky reads (comparisons, float constants, struct offsets) checked in the assembly. Names of reflected functions, vtable slots and class layouts come from the older corpus, the SDK headers and the exported data. RVAs are relative to the image base `0x140000000`. No pseudocode or assembly is reproduced here; behavior is described in words with RVAs.

## Statuses

| # | Question | Status | Answer in one line |
|---|---|---|---|
| 1 | Unit of the vehicle-exit damage curve input | Corrected | The input is the vehicle speed in km/h (cm/s times 0.036), not m/s. Found in round 46, re-read here; the Player Movement page still carried the old guess. |
| 2 | Look-acceleration curves: which one is used where | Resolved (three sub-values still open) | Only the gamepad look handler uses them, picked by the gamepad "Curve" setting through a table in the player controller. The curve input is seconds of sustained stick deflection past a delay. The delay, the per-curve extra time and the asset-to-type pairing are Blueprint values that are not in the export. |
| 3 | Ladder animation curves: consumer | Resolved | They are the `LadderTransitionCurves` entries of the ladder climbing data asset, read per transition type by the ladder mode's transition step. Input is elapsed time over the entry's duration (0 to 1). |
| 4 | `CRV_LandGunBob`: consumer and unit of Z | Still open | The Blueprint assigns it to the pawn's `WalkGunBobRotation`. No native function reads that field; the consumer is Blueprint or animation-graph code, which the corpus does not hold. |
| 5 | Slow walk against aim-down-sights and weight slowdowns | Resolved | Not a product. Aiming and weight lower the top speed first; slow walk then blends between the fixed minimum speed and that lowered top speed. |
| 6 | Does the 72 degree rule belong to the Aim down sight (FOV) setting | Resolved | Yes. The setting's saved choice, the 72 degree constant and the 3.25x test are read in one helper; the setting's description names the same limit. |
| 7 | Role of the sixth hit-location caller (`AWDMoverPlayerCharacter` slot 330, `0x6E830E0`) | Resolved | It is the player character's damage-taken handler. The hit-location lookup labels a `WDEvent_CharacterDamage` event; it changes no damage value. |
| 8 | How the engine spends fuel in play | Resolved (already described; stale sentence fixed) | The drain formula in "How fuel is used up" is confirmed in this corpus. The "was not traced" sentence in the table section contradicted it and is replaced. |
| 9 | Saved-preset hypothesis (`docs/ROUND8_STATUS.md`) | Still open | No client-side preset store exists beyond the storage vault. The item stays unticked; its text now records the new census. |

## 1. Vehicle-exit damage curve input is km/h

Method: followed the exit chain from the seat-exit function to the landing handler.

- Seat-exit function `0x5333CA0`: when a state byte of 3 is set at `+0x170` of the object at operator `+200` (round 46 read it as the authority role) and the vehicle is not in the excluded state (`0x53C9CF0`), it copies the vehicle config's `VehicleExitDamageCurve` into the operator component's exit cache and calls the vehicle's speed getter, virtual slot 313 (`0x53CAE30`), storing the result at cache `+0xF8` (call `0x5334657`, store `0x533465D`).
- Speed getter `0x53CAE30`: the length of the velocity vector in cm/s multiplied by the double `0.035999998` (cm/s to km/h). The same getter is shared by every vehicle pawn class (its vtable slot 313).
- Landing handler `0x5334C90`: compares the stored speed with the minimum speed for damage at cache `+0xE4` (compare `0x5334D8E`; below it the cache is cleared), reads the curve at the stored speed (`0x5334DB0`, `UCurveFloat::GetFloatValue` `0x3E0DA70`), floors the result at 0 and rounds it, and applies the config's exit damage type through the pawn's damage virtual.

Result: with `CRV_ExitVehiclePunishment_Damage` (40 -> 0, 50 -> 40, 60 -> 85, 75 -> 100) leaving a vehicle at 40 km/h or less does no damage, 50 km/h does 40, 60 km/h does 85 and 75 km/h does 100. Values beyond the last key were not checked. The class defaults of `MinVehicleSpeedForDamage` are not in the export (round 46).

## 2. Look-acceleration curves

Method: the controller field that holds the curve table (`TMap<EWDLookAccelerationCurveType, UCurveFloat*>`, `AWDPlayerController +0x9E8`, from the SDK) was searched for in the controller code range; the only reader is the look-input handler `0x6D4F700`. The reflected `InputLook` is `0x6D59160` and calls it (the controller's slot 163, `0x6D55D10`, also does).

What the handler does, in order:

1. Needs the possessed pawn (`+0x2F8`) and a non-zero input vector.
2. Gate (all three must hold): the gamepad look-acceleration setting is on (getter `0x6EB1F30`, call `0x6D4F8E6`), the game's gamepad-in-use flag is set (`0x6C04740`, call `0x6D4F8F7`; the hold and toggle input settings use the same flag to pick their gamepad variants, `0x6EB1160`), and the pawn is not seated in a vehicle (seat link `0x53CAE80` and seat test `0x5332580`, `0x6D4F90B` to `0x6D4F923`).
3. Curve type: byte from the settings (`0x6EB19D0`; enum Standard 0, Linear 1, Aggressive 2), looked up in the controller table (walk from `0x6D4F9B5`).
4. Raw stick deflection from the two look axes (`0x42C75C0`, call `0x6D4FA6A`). The magnitude is compared with the magnitude-threshold setting (`0x6EB1970`, compare `0x6D4FAA1`); below it the hold timer (`+0xA3C`) and stored direction (`+0xA40`) are cleared (`0x6D4FBF0`).
5. Above the threshold: if a direction was stored and its dot product with the current direction is under the controller's direction threshold (`+0xA38`, compare `0x6D4FB13`), the timer is cleared (`0x6D4FB19`) and the new direction stored. Then the world frame time (world `+0x864`, the same field `GetWorldDeltaSeconds` `0x3F2B170` reads at `0x3F2B1F4`; loaded at `0x6D4FA2B`) is added to the timer (`0x6D4FB30`).
6. Cap and delay: the timer is capped at (delay + extra) and stored back, where the delay is the controller float `+0x9E0` and the extra comes from a per-curve-type table at `+0xA58` (16-byte entries, key byte, float at `+4`; `0x6D4FB42` to `0x6D4FBBC`). Only when the capped timer is above the delay (`0x6D4FBB9`) is the curve read, at (timer minus delay) (`0x6D4FBCD`).
7. Multiplier m = 1 + (Max multiplier - 1) x curve value, with Max multiplier from `0x6EB1990` (`0x6D4FBD8` to `0x6D4FBEE`). The horizontal look axis is multiplied by m (call `0x6D4FC58`); the vertical axis by 1 + (m - 1) x Pitch weight (Pitch weight from `0x6EB19B0`; `0x6D4FC61` to `0x6D4FC87`). The settings getters `0x6EB1970`, `0x6EB1990`, `0x6EB19B0`, `0x6EB19D0` and `0x6EB1F30` each pick a value or its alternate by a flag byte next to it; which alternate that is was not followed.

So the time axis of the three curves is seconds of sustained stick deflection beyond the delay. The controller constructor `0x6D43C70` sets the delay to 0.5 s (`0x6D43F5B`), zeroes the direction threshold (`0x6D43F92`) and leaves the extra-time table empty (`0x6D43FB2`).

Still open: the controller Blueprint's values for the delay, the direction threshold and the per-curve extra times are not in the export (the controller Blueprint class defaults are not dumped). With an empty extra-time table the cap equals the delay and the curve is never read, so the Blueprint must fill it; its values decide the real time to the full multiplier. The pairing of the three assets (`CRV_LookAcceleration`, `_Linear`, `_Aggressive`) to the three types is also in that Blueprint table; by name it is Standard, Linear, Aggressive (assumed, not read). Keys in the page text such as "reaches full at 0.6 s" are curve times, measured from the end of the delay.

## 3. Ladder animation curves

Method: the ladder data class is `UBHLadderClimbingData` (SDK `BHMover_classes.hpp`): `LadderTransitionCurves[9]` at `+0x178`, each entry a (curve, double duration) pair of 16 bytes. The cooked asset `DA_LadderClimbingMovement` fills entries 1 to 4. Callers of the vector-curve read `0x3E11A50` were listed and the ones inside the mover code checked.

- Entries: 1 (enter from bottom) and 3 (enter from air) use `CRV_LMF_Ladder_ClimbOntoAnimation`, 0.25 s; 2 (enter from top) uses `CRV_LMF_Ladder_ClimbOntoFromTopAnimation`, 0.75 s; 4 (exit at top) uses `CRV_LMF_Ladder_ClimbOffAtTopAnimation`, 1.0 s. Types 5 to 8 (the other exits) have no curve.
- Consumer: the ladder mode's transition step `0x52CE150`, called from `0x52C4C70` (call `0x52C4DEE`). It casts the mode data to the ladder data class (class getter `0x52B1320`, name string "BHLadderClimbingData"), indexes by the transition type byte of the current step (`0x52CE327` to `0x52CE32F`, duration at `0x52CE34E`), and checks the curve is alive and the duration above 0 (`0x52CE35B`).
- With a curve: input = elapsed / duration, held between 0 and 1 (`0x52CE3B1` to `0x52CE3E2`; elapsed is counted in milliseconds, so the code scales by 0.001 over the duration), read as a vector (`0x52CE3EA`); position = start + curve x (target - start), per axis (the three channels scale X, Y and Z). Without a curve (null at `0x52CE33A`) or with a duration of 0 or less (`0x52CE35F`) the code jumps to `0x52CE55F` and the whole move is applied in one step.
- The Z channel of the from-top entry reaches 1.25, so that entry overshoots the target height before settling.

## 4. `CRV_LandGunBob` (still open)

- Data: the cooked pawn Blueprint (`B_WDMoverPlayerCharacter`) assigns the curve to `WalkGunBobRotation` (class offset `+0xCC0`), not to `JumpLandGunBob` (`+0xCE8`), which the Blueprint leaves unset. The scale field `WalkGunBobRotationScale` (`+0xCC8`) has the class default 1.0.
- Native search: functions in the whole executable that touch both `+0xCC0` and `+0xCC8`, and both `+0xCE8` and `+0xCF8`, were listed and each candidate in the character, controller, camera and animation code ranges was checked. The only reader or writer of the pawn's fields among them is the pawn constructor `0x6E7D050` (defaults written at `0x6E7D2E0` to `0x6E7D374`: scale 1.0, jump-landing scale range 0 to 2.75, jump-landing speed range -250 to -1600, and others). The other hits are other classes (stores into their own `+0xCC0`).
- The callers of the vector-curve read (`0x3E11A50`, `0x3E11560`) are: the vaulting and traversal modes (`0x52C5F60`), the ladder step (`0x52CE150`), a stance modifier (`0x6E99C40`), the critical-state camera modifier (`0x6E8F430`), two further functions in the character-modifier and mover-mode code that read curve structures embedded in themselves (`0x6E98070`, `0x6DBDE80`), an animation-instance function that reads curves embedded in the instance (`0x6A80880`), and generic engine code. None reads the pawn's gun-bob curve.
- Conclusion: the consumer is not in native code. It is in the pawn Blueprint or in the animation graph (property access), neither of which is in the corpus. The unit of Z is therefore still unknown; the property name says "Rotation", so degrees are likely but not read.
- The generated table in the Player Movement page glosses this curve as a "weapon dip after landing". That gloss is not supported: the assignment is the walk gun-bob rotation, and the landing curve slot is empty.

## 5. Slow walk, aim down sights and weight

Method: read the ground-mode velocity function `0x52867F0` in the assembly, and the two speed getters it calls through the mode vtable.

- Top speed comes from slot 142 (vtable offset `0x470`, call `0x5286C8C`); the minimum from slot 143 (offset `0x478`, calls `0x5286CF1` and `0x5286D2F`, base function `0x52923C0`).
- The WD override of slot 142 is `0x6DC1000`: the base function `0x5291720` (base speed times the stance modifier and the sprint factors) multiplied by the player's `Movement.MaxSpeedMultiplier` attribute (evaluated at the mode `+272`). That attribute already contains the aim-down-sights effect (0.5) and the weight class (0.8 for Heavy). The minimum speed is not multiplied by the attribute.
- Blend: for a stick under full deflection, speed = (top - min) x stick + min (`0x5286CC3` to `0x5286CFF`); at full deflection with slow walk on, speed = (top - min) x share + min, where the share (0.2, 0.4 or 0.6) comes from the slow-walk settings table (`0x5286D0D` to `0x5286D44`); with slow walk off the speed is the top speed. No clamp follows. Sprint skips the blend.
- Derived: standing top speed 428.8 cm/s. Slow, Moderate, Fast: plain 149.8, 219.5, 289.3; with aiming down sights (top 214.4) 106.9, 133.8, 160.6; with a Heavy load (top 343.0) 132.6, 185.2, 237.8; with both (top 171.5) 98.3, 116.6, 134.9 (cm/s). A plain product of the plain slow-walk speed and the slowdowns would give 74.9 for Slow with aiming.
- Not claimed on the wiki: when the top speed falls below the 80 cm/s minimum (for example prone with aiming down sights, 40.2 cm/s), the same formula puts the slow-walk speed above the plain walk speed. A later velocity clamp was not searched for, so this stays out of the wiki.

## 6. The 72 degree rule and the Aim down sight (FOV) setting

Method: followed the aimed-angle helper to its inputs.

- Helper `0x6C29420` (arguments: mode byte, zoom test value, magnification, incoming field of view): when the magnification is not about 0, the base angle is 72.0 (constant loaded at `0x6C29441`) if the mode byte is 1 (compare `0x6C29433`) or the zoom test value is 3.25 or more (compare `0x6C29438`), otherwise the incoming field of view; the result is the base divided by the magnification (`0x6C29449`).
- The camera modifier `UWDAttachmentsCameraModifier::ModifyCamera` (`0x76E9F90`) calls it (calls `0x76EA403`, `0x76EA43C`). The mode byte comes from the player controller (`0x6D4DBA0`, controller `+0x968`); the zoom test value from the weapon behaviour component (`+0x3E0 + 0x14 = +0x3F4`, getters `0x6B86300`, `0x23808C0`).
- Controller `+0x968` is a cached copy of the user setting `AimingFovMode` (`UWDUserSettings +0x546`, or `+0x547` when the flag at `+0x548` is set; getter `0x6EB1220`), stored by `0x6D51CE0` (store `0x6D51D0E`). Enum `EWDAimingFovMode`: Affected 0, Independent 1. The same helper is called by the sensitivity function `0x6D4DEB0` (round 80).
- The setting's description in `DT_Settings_General` reads: Affected is based on the Field of View setting "at low magnification levels (below 3.25x)", Independent "always based on a base Field of View constant". The code and the text agree: Independent forces 72 at any zoom, and in Affected mode 72 applies from 3.25x up.

## 7. `AWDMoverPlayerCharacter` slot 330 (`0x6E830E0`)

- Slot 330 of the character vtables: base `0x6E71AD0` (`AWDMoverCharacter`), player override `0x6E830E0`. Its virtual callers: the reflected `WDMoverCharacter::OnDamageTaken` (`0x6E7AC10`, call `0x6E7ADC7`, which unpacks the damage-event argument), `0x6E73E30` (slot 339, which re-fires a stored event after a time check), `0x6D74820` and `0x7704620`. The database lists the function from `0x6E830DC` (a 4-byte stub in front), so Hex-Rays gives no pseudocode for it; the assembly was read.
- The override: on the authority side it first runs a server-side step that works from the event's instigator (`0x6E829C0`, call `0x6E83181`; read only in part); it gathers the damage event's hit data (`0x6A78030`, `0x6A780A0`, `0x6E7CFC0`); it looks the hit location up with `0x6F01BB0` using the damage subsystem's data (`0x6EF2010`, `0x4528CE0`; call `0x6E83677`) and stores the returned tag in the payload; it builds a payload with the event tag from `0x6B15EA0` (the registered event name `WDEvent_CharacterDamage`) and dispatches it (`0x4D49E50`, call `0x6E836A9`); then, on the authority side and when a tag check passes, it hands the event to a helper reached through the pawn's controller link (`0x6B0B380`, call `0x6E83725`), calls a virtual of a pawn component (`0x6E6EBA0`) with two tags and the damage amount (`[event + 4]`, call `0x6E83767`), and finally calls the base handler (`0x6E83770`).
- It never writes to the damage event it receives, and it does not use the remap functions (`0x6F01530`, `0x6BB8D40`). The lookup therefore only labels the event; no damage value comes from it. The dispatcher `0x4D49E50` and the receivers of the event were not read.

## 8. How the engine spends fuel

Re-read in this corpus; the existing description holds.

- Tick `0x7666FA0`: runs only where the vehicle's role byte is 3 (authority); skips when the component's off flag (`+308`) is set; the engine part of the drain is added only when the vehicle's engine-running byte is set (`0x53C9D00`, byte `+2185`); adds the stored leak value times the frame time even with the engine off; subtracts the sum from the fuel attribute (`0x52311D0`) when it is above 0.0001.
- Engine part `0x7665DB0`: above the idle speed threshold (`+280`, class default 1.0 km/h) the rate is speed in km/h / 3600 / km-per-litre (`+276`); at or below it the rate is engine RPM / 3600 / RPM-per-litre (`+284`) (the vehicle's RPM virtual, slot 298), then multiplied by the boost multiplier (`+296`) when the vehicle's boost virtual (slot 296) is true, and by a fuel-usage multiplier (cached value `+380` when set, otherwise an attribute) (`0x7665E22` to `0x7665E67`). The speed is the same km/h getter as in section 1 (slot 313).
- Wiki change: the sentence "how the engine itself spends fuel in play was not traced" contradicted the page's own "How fuel is used up" section and is replaced by a pointer to it. The Refuel Station sentence "the restock most likely still takes its full 9 s (inferred)" is outside this topic and was not examined.

## 9. Saved-preset hypothesis

Method: (a) the string literals of every function that has any (33,389 of the 987,571) were scanned for loadout, preset, favourite and save-game names; (b) the reflected types of the older corpus were listed for save, stash, vault, profile, persistence and loadout names; (c) the callers of the Unreal save-game functions were listed.

- (a) Hits: the vendor purchase tags (`Vendor.Purchase.Context.Loadout`, `UI.Action.Feature.Vendor.Purchase.AddToLoadout`, `UI.Action.Feature.Vendor.Purchase.Loadout`, `Progression.Resources.MatchScore.Purchased.Loadout`), `Wager.Behavior.RequireLoadoutCost`, the scene tag `UI.Scene.Frontend.Loadouts`, `Tutorials.BuyingYourLoadout`, the Deathmatch `Server_SetupLoadoutByTag` binding, the Itemsmith favourite action (`Itemsmith.Actions.Persistent.Favourite`, paint favourites), and unrelated presets (video quality, gamepad dead zones, minimap zoom, DLSS, audio and engine files).
- (b) Types: `FWDLoadout`, `FWDLoadoutSlot`, `FWDLoadoutStack`, `FWDLoadoutApplyResult` (vendor cart and apply result); `FWDStorageVault*` and the `FPragma_PlayerData_*Vault*` request types (the storage vault); the other 88 `FPragma_PlayerData_*` request and data types, leaving out vault and response types (currencies, XP, mastery, wager cooldowns, collection items, equipped collection items, one-time grants, reports) hold no loadout or preset record.
- (c) The writer behind `SaveGameToSlot` (`0x3F209B0`) has only the reflected thunk (`0x3F2F880`) and an engine function without recorded callers (`0x3F18839`) as callers; the loader (`0x3F0DDE0`) is called from `0x3EDB280` (no recorded callers), the thunk (`0x3F2BFF0`) and the Enhanced Input local-player subsystem (`0x4CE8730`, called from `0x4CE7390`). The existence check (`0x3EFE290`) is called from game code only by the automation orchestrator component (`0x866E4F0`) and functions next to it, not by a loadout feature.
- Conclusion: no client-side preset store exists beyond the storage vault, which is a server-held vault with import, not a named preset. The item stays open and unticked; anything held only on the backend is invisible to client code.

## Wiki updates

- `content/Wardogs_PlayerMovement_v1.md`: vehicle-exit input unit (km/h); gun bob and look-acceleration paragraphs; ladder curve consumer; open items; change-log row. The generated curve table (block `curves`, from `_tools/movement_tables.py`) still carries the old text for three rows; suggested replacement text for the generator is in the hand-off note: exit curve "Damage on leaving a vehicle; input is the vehicle speed in km/h"; gun bob "Vector curve; only the Z channel has keys: walk gun-bob rotation (pawn `WalkGunBobRotation`), consumer not in native code"; look acceleration rows "... gamepad look ramp; input is seconds of stick deflection past the controller's delay".
- `_wiki/game-mechanics/movement.md`: the slow-walk bullet now says aiming and weight lower the top speed before the slow-walk blend, with worked speeds; Sources gets this page.
- `_wiki/game-mechanics/controls-and-settings.md`: the "inferred" sentence about the 72 degree rule is replaced; Sources gets this page.
- `content/Wardogs_GameMechanics_v2.md`: section 2b role of the sixth caller; change-log row.
- `_wiki/vehicles/fuel-and-refueling.md`: stale "was not traced" sentence replaced; Sources gets this page.
- `docs/ROUND8_STATUS.md`: saved-preset item text extended; not ticked.
