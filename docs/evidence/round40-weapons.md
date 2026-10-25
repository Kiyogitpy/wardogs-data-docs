# Round 40: weapons, hit registration and artillery backlog (round 39 NATIVE items)

GitHub-only page. Agent RE40-WEAP, continuing RE39-WEAP. Inputs: the restored executable (static disassembly with capstone), the decompiled corpus `decompiled_cl516586_20261017_mmvpuc__` (unreviewed decompiler output), the SDK headers, the cooked export in `data/`, and the round 8 Blueprint dump for the bow actions. Nothing was run. Evidence levels: **static disassembly**, **static decompiler output (unreviewed)**, **cooked data read**, **derived**.

Statuses: FOUND, NATIVE (open) with what was read and what remains, PROTECTED (code path enters the protection layer; entry RVA named). No item this round reached a protection-layer dispatch stub, so PROTECTED is 0; items marked "not advanced" ran out of the time-box (the open items that could not be reached by a direct static scan were not attacked). The earlier mention of dispatch stubs (round 39 item 5) is unchanged.

Reproduce:

```
python -I _tools/artillery_range_native.py --check     # item A5: native range function vs the SPH-2 table
python _tools/wiki_weapons.py && python _tools/wiki_calibers.py   # unchanged output, see "Generator"
```

Helper scripts (not in the repository): `round40_weap/dscan.py DISP lo hi` lists every non-RIP instruction in `.text` whose memory operand (or immediate in `dscan2.py`) equals a displacement, with read/write and the enclosing function; `near.py RVA` prints the decompiled function covering an address.

## Generator

`_tools/wiki_weapons.py` now appends " (class default)" to the rate when `weapon-damage.json` has `rpm_source` starting with `class_default` (PKM and Glock 17: 600). Running both generators over `_wiki/` produced no content change (only line-ending noise, discarded): the articles already read "600 rounds/min (class default)". Commit contains the generator edit only.

## Artillery (player value first)

| Item | Status | Value | RVA / source | Level |
|---|---|---|---|---|
| A5 SPH-2 table mrad vs dial | **FOUND** | The table's `Milliradians` are **dial mils**. The range function adds **16.808 mrad (0.963 degrees)** to the dial value before flying. Reproduces the 40 `ImpactDistance` rows with mean abs error 5.1 m (max 29 m), against 77 m without the term. | `SimulateImpactDistance` thunk `0x69A0900`, body `0x761D180`; constants `0x9AAFD68` (0.001), `0xB62DCCC` (0.016808); `_tools/artillery_range_native.py` | static disassembly + derived (fit to cooked table) |
| A1 mil convention of the dial | **FOUND (function side)** | Dial ticks print `SimulateImpactDistance(dial mil)`; true launch elevation = dial/1000 + 0.016808 rad. The pointer value `WeaponPitchBindable x pi/180 x 1000` is a true milliradian; its zero reference (hull or world) is set where the pitch property is written and was not located. | as A5; HUD side from round 36 | static disassembly |
| A6 zero of the sight's mil scale | **FOUND (range function), NATIVE (open) for the pointer** | In the range function, dial 0 = 16.808 mrad above the launch axis zero. Whether that offset is the barrel-versus-pivot geometry is not stated in the files (no source for the constant besides the literal). | `0x761D1FB`-`0x761D211` | static disassembly |
| A4 low arc needs 40 to 60 mil more than the high arc | **FOUND (derived)** | The function takes a start altitude, which the stored table does not. A 2,000 m low-arc shot needs 250 mils from 3 m, 224 from 50 m, 197 from 100 m (simulated), the size and sign of the calculator difference (about 50). The altitude the calculator used is not known. | `0x761D180` argument `xmm3`; simulation in `artillery_range_native.py` | derived |
| A3 does the Standard 155 mm fly with `DragModel.Value` 80 | **FOUND (derived)** | The function uses `Cd = Value x curve(v)` per shell (the table matches Value 2.5, the Expensive shell). With Value 80, 70 kg, 8.4 cm the same function reaches only about 810 m at its best elevation, so the Standard shell is a short-range round by its data. Whether the SPH-2 ever loads it was not traced. | `0x6BBA8A0` (drag lookup, speed x 0.01 into the curve) | derived |
| A7 how speed, mass, drag, thrust and lifetime enter the range function | **FOUND (range function), NATIVE (open) for the in-flight mover** | The range function uses `InitialBulletSpeed x 0.01` (`0x6BBD500`), `Diameter` (`+0x6C`), `Mass` (`+0x70`), `DragModel` (`+0x10`), air density and altitude from the caller; **no thrust, no wind, no `MaxProjectileLifetime`**. Gravity 9.8 m/s2, 10 ms step. | `0x761D180` | static disassembly |
| 13 (re-check) flight step length | **FOUND (addition)** | Native-stepped flight is 33 ms (round 23); the HUD and table range function is a separate **10 ms midpoint** integrator with g = 9.8. `SimulationFrameRate` is read at four sites (Projectile Flight section 3); no further consumer found this round. | `0x761D180` vs `0x6F3BCB7` | static disassembly |
| A2 hull pitch added to the commanded elevation | NATIVE (open) | Read: the range function takes the dial mil only; no hull pitch term. Where `WeaponPitchBindable` is written (turret pitch with or without hull) was not located. | `0x761D180` | static disassembly |
| A12 SPH-2 hull tilt and levelling | NATIVE (open) | Not advanced beyond A2. | | |
| A8 constructor defaults of artillery speed limits, drag, gravity scale | NATIVE (open) | Not advanced: the mover constructors were not found by vtable (`UWDArtilleryProjectileMove_VFT` `0xB6720E8`, slot 0 `0x76C7D70` is the destructor; slots 18-23 are shared engine stubs). | | |
| A9 `BP_155mm_Standard` / `Expensive` mover mode | NATIVE (open) | Not advanced. | | |
| A10 gravity override volumes | NATIVE (open) | Not advanced. | | |

## Hit registration

| Item | Status | Value | RVA / source | Level |
|---|---|---|---|---|
| IgnoreInstigatorVehicleTime (O-9) | NATIVE (open), with a **correction** | `inst+0x129` and `+0x28D` are **whiz-by presentation flags**, not the vehicle-ignore timer. `0x6F37750` sets `inst+0x129` when the bullet heads at another actor (dot of direction and bullet-minus-actor offset <= -0.8) that carries a gameplay tag; the consumer `0x6F3B0E0` needs `+0x129` set, `+0x25E` set and `+0x12A` clear, compares against projectile stats `+0x2D4` (`TravelDistanceWhizBy`) and `+0x2D8` (`DistanceToPlayerWhizBy`), and sets `+0x12A` when done. The stat `+0x2E4` is copied to spawn-request `+0xB0` (`0x6B8FD5A`); its default is 0; the only comparison found is the fire path `0x6B937D0`. No timing consumer found. | `0x6F37510`, `0x6F37750`, `0x6F3B0E0`, `0x6B8FD5A`, `0x699E1D5` | static decompiler output |
| O-6 array at `inst+0x130` | NATIVE (open) | Scan for displacement `0x130` in `0x6F00000`-`0x6F60000`: stores occur only in the instance copy routines (`0x6F29570`, `0x6F2B390`) and mixed code; no single array-append site identified. | `dscan.py 130` | static disassembly |
| O-7 `bIsHitScan` byte `+0x2DA` | NATIVE (open) | No instruction with displacement `0x2DA` in `0x6F00000`-`0x6F60000`; the byte is read elsewhere or through a computed offset. | `dscan.py 2da` | static disassembly |
| O-1 mover sweep, O-2 tapered capsules, O-4 `ServerTime` / fixed-tick fields, O-5 alignment, O-8 impact cue tags, O-10 `CustomHitResults` | NATIVE (open) | Not advanced. For O-4: the only `+0x18C` accesses in the projectile range are copy routines and the settings constructor (`0x6F2A770` stores 16 at settings `+0x18C`), none is the hit record writer. | | |
| 14/15 ricochet reflection, deflection and ratio gate | NATIVE (open) | Not advanced; still unreviewed pseudocode (round 25). | | |
| 51 explosive and radial hits ignore coverage | NATIVE (open) | Not advanced. | | |

## Weapon, spread and aim

| Item | Status | Value | RVA / source | Level |
|---|---|---|---|---|
| 34 `ZeroTable` (`+0xFF8`) | **FOUND (writer and unit)**, formula NATIVE (open) | Empty `TMap<int32,float>` made by the constructor `0x6B8E5A0` (`0x6B8E749`). `0x6B96820` loops zeroing ranges (stats low to high, step from `0x145E98870`, distance = range x 100 cm) and starts an **asynchronous predicted-path trace** per range with the launch speed `0x6BBD500` against the actors listed by `0x6BBD650`; the completion callback `0x6B8C8D0` stores the angle **in degrees** (radians x 57.29578) in `ZeroTable[range]`, plus two more maps at `+0x1048` and `+0x1098`. `GetZeroingAngles` `0x6B99190` returns a copy to Blueprint. So the zero angle is computed at run time from the game's own trace, not authored. The trace result function `0x6B95520` and the meaning of the two other maps were not read. | `0x6B8C8D0`, `0x6B96820`, `0x6B99190`, `0x6B8E749` | static decompiler output |
| 35 muzzle-speed scale `component+0x114` | **FOUND** | Only writer: the exposed function `SetInitialBulletSpeedModifier` `0x6B99A30`. Readers: spawn wrapper `0x6B959E0` (`InitialBulletSpeed x +0x114`) and the shot function `0x6B93610` (`0x6B9412B`). Callers found: Blueprint bow actions `B_Action_BowDraw.TryActivateFire` and `B_Action_BowFireTestNew.OnReleased`, passing `GetVelocityModifier` = `DrawVelocityCurve(draw alpha)`; `CF_DrawVelocityReleaseCurve` keys (0, 0.05, cubic) and (0.4, 1.0, linear); `FullDrawTime` 1.4 s (`ID_CombatBow` / `RangedBowData`); `MinDrawTime` omitted (default not read). No firearm caller found. How draw alpha is computed (`GetDrawAlpha`) was not read. | `0x6B99A30`, `0x6B959E0`, `0x6B9412B`; `round8_blueprint_type_recovery/dump-after/B_Action_BowDraw.json`; `data/.../CombatBow/.../CF_DrawVelocityReleaseCurve.json` | static disassembly + cooked data read |
| 31 aim sway in the view rotation (`+0x840`) | **FOUND (partial)** | Slot 264 is the pawn's view-rotation getter. For a controlled character it forwards (`0x41F5EB0` base, `0x528F470` mover character override) to the controller's slot 264 `GetPlayerViewPoint` (`0x42C8890`), which for a player controller with a camera manager returns the camera manager's view point. So the shot direction is the camera's final rotation. Whether weapon sway is added to the camera rotation, or only as an animation offset, is open. `bSpawnProjectileFromCameraWhenAds` not read. | `0x41F5EB0`, `0x528F470`, `0x42C8890` | static decompiler output |
| 26 sight ADS zoom to magnification, 27 sight multiplier (`+0x3D0`) | NATIVE (open) | Scanned reads of struct displacement `0x370` (`AdsZoomMultiplier`) as float in `0x6A00000`-`0x6F00000`: the only hit (`0x6AE408A`) is in an unrelated class (compares an interval against `+0x370`), not the sight data. FOV consumer not located. | `dscan.py 370` | static disassembly |
| 36 mounted and vehicle weapon spread (`+0x2BC`) | NATIVE (open) | Not advanced. | | |
| 40 per-shot bloom | NATIVE (open, negative) | Not advanced. | | |
| 56 aim assist `FBHAimAssistTargetData`, 57 pull modes per asset | NATIVE (open) | Not advanced. Vtables exist (`UBHAimAssistInputModifier` `0xB06D0A8`, `UBHAimAssistTargetManagerComponent` `0xB06D648`, `UWDAimAssistInputModifier` `0xB3D02F0`); the field reads were not traced. | | |
| 53-55 ammo packing (combine-loose map, tag parent search, extraction and load curves) | NATIVE (open) | Not advanced. | | |
| 49 speed scale after drag in the damage tables | NATIVE (open) | Not done. The range function in `artillery_range_native.py` is a verified drag integrator (Expensive shell) that could host it. | | |
| 5 rate-of-fire rewrite path | NATIVE (open) | No new evidence. | | |
| 23 obfuscated magazine floats | NATIVE (open) | Not advanced. | | |
| 37 `srand` seed | NATIVE (open) | No new evidence (round 39: seed comes from a platform call). | | |
| 38 frame `+0x270` echo; snapshot `0x6C9DB60` | NATIVE (open) | Not advanced. | | |

## Counts

The round 39 NATIVE backlog counted 36 items; split into separate sub-items it is 40.

| Status | Rows |
|---|---:|
| FOUND (including FOUND with a NATIVE part named) | 10: A5, A1, A6, A4, A3, A7, 13, 34, 35, 31 |
| NATIVE (open) | 30 (O-9 and 26/27 with partial readings) |
| PROTECTED | 0 (no item entered a protection-layer dispatch stub) |

Files changed: `docs/evidence/round40-weapons.md`; new `_tools/artillery_range_native.py`; `_tools/wiki_weapons.py`; `game-features/Wardogs_ArtilleryShellFlight_v1.md` (new section 5a); `pipelines/Wardogs_HitRegistration_v1.md` (whiz-by correction); `pipelines/Wardogs_WeaponSpread_v1.md` (ZeroTable, `+0x114`, view rotation).

## Wiki updates

- `_wiki/guides/aiming-the-sph-2.md` and `_wiki/game-mechanics/artillery.md` -> add: the in-game mil scale and the stored range table are the same function; the barrel's true elevation is 16.8 mrad (about 0.96 degrees) above the dial reading; the dial shows fewer mils at higher muzzle altitude (about 25 fewer at 50 m, 50 fewer at 100 m for a 2,000 m low-arc shot, simulated), which is why the community calculator and the stored table differ by 40 to 60 mils on the low arc; the stored table is for the Expensive shell (the Standard 155 mm round, drag value 80, would only reach about 810 m).
- `_wiki/game-mechanics/spread-and-recoil.md` (zeroing line) -> "weapon zero angles are not authored: the game measures them at run time with a trace for each zeroing range and stores them in degrees".
- `_wiki/weapons/bow.md` (if present) / `_wiki/weapons/attachments-sights-and-optics.md` -> no change. For a bow article: arrow launch speed is scaled by a draw curve (5 percent of full speed at the start of the draw, full speed once the draw alpha reaches 0.4; full draw time 1.4 s).
- `_wiki/game-mechanics/hit-registration.md` -> remove any statement that links a projectile's "ignore the shooter's vehicle" setting to the bullet's heading test; that test drives the whiz-by sound/effect, not the vehicle ignore.
- Nothing else changes: `_wiki/weapons/pkm.md`, `ggx-17.md` already read "600 rounds/min (class default)"; the generator keeps it by `rpm_source`.
