# Round 79: sight zoom data to the 3.25 test and the effective magnification

Static analysis only (disassembly with capstone over the restored executable, the decompiled corpus, cooked JSON). Nothing was run. RVAs are image-base-relative. Nothing here is behind the protection layer (no PROTECTED items); where a step was not traced it says so.

## 1. How the sight's zoom data reaches the weapon extension (FOUND)

Class: the ranged-weapon item extension (`UWDItemExtension_RangedWeapon`, the object whose attribute-changed handlers are `0x6C99E52` and `0x6C9A902`).

**The copy.** The sight-change function `0x6C9E190` builds a local copy of the sight data struct (0x418 bytes; `VariableZoomData` at struct `+0x358`, `AdsZoomMultiplier` at `+0x370`). The source is a data-table row looked up by the sight id stored at extension `+0x440` (`0x6C168F0`), or, when the lookup fails, the cached map entry at extension `+0x438`, taking its struct at entry `+0x88` (`0x6C9E4C6` to `0x6C9E4D9`, copier `0x6C442A0`; with nothing found the struct is zero-filled, size `0x418` at `0x6C9E4E0`). Then:

```
6C9E4F4: cmp byte ptr [rbp+0x308], 0      ; struct +0x358 = bCanVariableZoom
6C9E4FB: je  6C9E51D
6C9E4FD: movups xmm0, [rbp+0x308]         ; true: copy the 0x18 byte FWDVariableZoomData
6C9E504: movsd  xmm1, [rbp+0x318]
6C9E50C: movups [rdi+0x44C], xmm0         ; extension +0x44C..+0x464
6C9E513: movsd  [rdi+0x45C], xmm1
6C9E51D: ... build a zero block ...
6C9E548: movups [rdi+0x44C], xmm1         ; false: all zero (bCan 0, Min 0, Max 0, steps 0)
6C9E557: movss  xmm0, [rbp+0x320]         ; struct +0x370 = AdsZoomMultiplier
6C9E562: movss  [rdi+0x3D4], xmm0         ; initial zoom ramp target
```

So the copy happens **only when `bCanVariableZoom` is true**. For a fixed sight the whole `+0x44C` block is zeroed and the stored ZoomMultiplierMin and Max are never used. The reset path does the same zeroing (`0x6C9D998` to `0x6C9D9A0`).

Layout at `+0x44C`: `+0x44C` bCanVariableZoom, `+0x450` Min, `+0x454` Max, `+0x458` mouse step, `+0x45C` controller step, `+0x460` interp time. The zoom actions are gated on `+0x44C` by the check function `0x6C92D50` (`cmp byte [rdi+0x44C]` at `0x6C92E73`), so zoom input does nothing on a fixed sight.

**What `+0x454` holds.** Max for a variable sight (6, 9 or 10 in the data); **0 for every fixed sight**, including those whose JSON stores 4 and 8, 3 and 6, or 3.5.

**What the 3.25 test uses.** Both handlers pass `max([entry + 0x3F8], [this + 0x454])` to `0x6B879E0`, which stores weapon-component `+0x3F4` (`0x6C99E29` to `0x6C99E52`, `0x6C9A8ED` to `0x6C9A902`). The map entries are 0x4B8 bytes (`imul rdx, rax, 0x4B8` in the lookup `0x6C96FB0`) and the sight struct sits at entry `+0x88` (`0x6C9E4D2`), so entry `+0x3F8` = struct `+0x370` = **the sight's stored `AdsZoomMultiplier`** (static data), not the eased runtime multiplier. Round 62 took it for the runtime multiplier; the offset arithmetic (0x88 + 0x370 = 0x3F8) says it is the struct field. Inferred from offsets; the entry was not otherwise typed. The test value is therefore:

- fixed sight: the stored `AdsZoomMultiplier` (Max is 0);
- variable sight: `max(stored AdsZoomMultiplier, Max)`; in the data this is at least 6, so every variable scope uses 72 degrees over its whole range.

No sight in the data lands on a different side of 3.25 between the stored `AdsZoomMultiplier` and the zoom its effect applies, so the wiki's "fixed magnification" reading gives the same answers.

**What drives the aimed field of view.** The camera modifier (round 46) uses weapon-component `+0x3F8`, the eased value of base `+0x3F0` times the focus bonus. Base `+0x3F0` is written by `0x6B87960`, called by the attribute handlers (the AdsZoomMultiplier attribute, which each sight's gameplay effect sets with an Override) and by the zoom ramp interpolator `0x6C9EEC0`. The ramp (extension `+0x3D0` current, `+0x3D4` target, `+0x3D8` user offset) takes target = attribute value + offset (`0x6C9EEC0`: `v12 = attr + a1[2]`); the zoom in, out and cycle handlers (`0x6C947F0`, `0x6C99560`, `0x6C9ECB0`) change the offset and clamp `+0x3D4` to `[Min, Max]` (`0x6C94847` to `0x6C94883`). So:

- fixed sight: aimed magnification = the AdsZoomMultiplier attribute (the effect's value); the test uses the struct field;
- variable sight: starts at the attribute value, which in the data equals ZoomMultiplierMin on all six variable sights (6-10x MRAD and MOA 6, 3-6x Scope 3, LPVO 3, Frontier 2.5, ART II 3), then moves within Min to Max. The struct `AdsZoomMultiplier` of those scopes (10, 10, 6, 6, 10, 3) is not where they start; it is the initial ramp placeholder (`0x6C9E562`) and the 3.25 test input.

Not traced: the first evaluation of `0x6C9EEC0` after attach (its caller chain), so "starts at the attribute value" is read from the interpolator and the data, not from a traced first frame. Status: FOUND for the copy and its gate; FOUND (inferred from offsets) for the test input; the ramp start is partly inferred.

**Correction to the premise.** The 6-10x MRAD and MOA scopes (`ID_10xScope`, `ID_10xScopeMoa`, `Content/Items/Attachments/Sights/10x_Scope`) do carry the zoom fields: bCanVariableZoom true, Min 6, Max 10, `AdsZoomMultiplier` 10. They are variable scopes and the attribute value 6 is their starting zoom.

Data (cooked JSON; can zoom / Min / Max / stored AdsZoomMultiplier / zoom the effect sets):

- Variable: 6-10x MRAD and MOA true 6 10 10 / 6; 3-6x Scope true 3 6 6 / 3; 1x-6x LPVO Short Dot true 3 6 6 / 3; Frontier 2.5x-10x true 2.5 10 10 / 2.5; Leatherwood ART II true 3 9 3 / 3.
- Fixed with stored Min and Max: Spitfire 3X false 4 8 3 / 3; Tricon false 4 8 1.5 / 1.5; CQ-2x false 4 8 2 / 2; 3x Tactical Prism false 4 8 3 / 3; 4x Combat Prism false 4 8 4 / 4 (reflex 1.2); 4x Elcan Spectr false 4 8 4 / 4 (reflex 1.2); PGO-7 false 4 8 2.8 / 2.8; 6x Precision false 3 6 6 / 6; 6x Marksman false 3 6 6 / 6 (reflex 1.2); PU 91/30 false 3.5 3.5 3.5 / 3.5.
- Reflex and holographic sights store 1.2 or 1.5 and the effect applies 1.2.

## 2. Normal view: 106 or 90 (FOUND, static)

`DA_PlayerCharacterComponents` (`WDFirstPersonCameraComponent_0`) has `FieldOfView` 106 and no first-person field of view override, so 106 is the camera component's starting value. The user setting (`BHUserSettings +0x26C`, override `+0x270` when flag `+0x274`; getter `0x4E38F20`) is applied in two ways:

- `0x6D3F9E0` and `0x6D3F7A0` store it into the player camera manager's `DefaultFOV` (`+0x2D0`);
- `0x6E84600` (call at `0x6E846C8`) calls virtual slot 200 (`+0x640`) of its camera object with the setting as the float argument. Slot 200 of the first-person camera component vtable `0xB2FAD78` is `0x394B1C0`, which is `movss [rcx+0x270], xmm1`: `SetFieldOfView`. So the setting overwrites the 106 at runtime.

So the normal unaimed view is the Field of view setting (default 90); 106 is the data default that gets replaced. Open: when `0x6E84600` runs (on possess and on setting change is assumed), and that its object is the first-person camera was read from the vtable slot, not traced from its callers. The weapon view model is drawn separately (`0x6C725E0` writes a fixed 90.0, constant `0x42B40000`, into the weapon FOV material parameter collection), so the view model does not use the 106 either. The wiki treats 90 as the normal view.

## 3. Effective magnification table (derived)

`effective = tan(90 / 2) / tan((base / m) / 2)` with `base` 72 when the test value is 3.25 or more, else 90; `m` the zoom the effect applies (variable scopes at both ends of Min to Max). Round 46: the camera step divides the angle (no tangent correction), so the aimed angle is `base / m`. Default settings (Field of view 90, Affected), full aim, no focus bonus. Derived from camera code, not measured on screen.

| Sight | Magnification m | Base angle | Aimed angle | Effective |
|---|---:|---:|---:|---:|
| 1x-6x LPVO Short Dot (at its high end) | 6 | 72 | 12 | 9.51 |
| 1x-6x LPVO Short Dot (at its low end) | 3 | 72 | 24 | 4.7 |
| 2.5x Combat Optic | 2.5 | 90 | 36 | 3.08 |
| 3-6x Scope (at its high end) | 6 | 72 | 12 | 9.51 |
| 3-6x Scope (at its low end) | 3 | 72 | 24 | 4.7 |
| 3x Tactical Prism Scope | 3 | 90 | 30 | 3.73 |
| 4x Combat Prism Scope with Reflex (reflex mode) | 1.2 | 72 | 60 | 1.73 |
| 4x Combat Prism Scope with Reflex (scope mode) | 4 | 72 | 18 | 6.31 |
| 4x Elcan Spectr (reflex mode) | 1.2 | 72 | 60 | 1.73 |
| 4x Elcan Spectr (scope mode) | 4 | 72 | 18 | 6.31 |
| 4x Hybrid | 4 | 72 | 18 | 6.31 |
| 6-10x Scope MOA (at its high end) | 10 | 72 | 7.2 | 15.89 |
| 6-10x Scope MOA (at its low end) | 6 | 72 | 12 | 9.51 |
| 6-10x Scope MRAD (at its high end) | 10 | 72 | 7.2 | 15.89 |
| 6-10x Scope MRAD (at its low end) | 6 | 72 | 12 | 9.51 |
| 6x Marksman Scope + Reflex (reflex mode) | 1.2 | 72 | 60 | 1.73 |
| 6x Marksman Scope + Reflex (scope mode) | 6 | 72 | 12 | 9.51 |
| 6x Precision Rifle Scope | 6 | 72 | 12 | 9.51 |
| CantedIrons | 2 | 90 | 45 | 2.41 |
| CGM4 Scope | 1.2 | 90 | 75 | 1.3 |
| Compact P-1 Red Dot | 1.2 | 90 | 75 | 1.3 |
| Compact T-2 Red Dot | 1.2 | 90 | 75 | 1.3 |
| CQ-2x Prism Combat Scope | 2 | 90 | 45 | 2.41 |
| Four Reticle Reflex | 1.2 | 90 | 75 | 1.3 |
| Frontier 2.5x-10x Precision Scope (at its high end) | 10 | 72 | 7.2 | 15.89 |
| Frontier 2.5x-10x Precision Scope (at its low end) | 2.5 | 72 | 28.8 | 3.89 |
| Holographic Sight | 1.2 | 90 | 75 | 1.3 |
| Kobra Reflex | 1.2 | 90 | 75 | 1.3 |
| Leatherwood ART II (at its high end) | 9 | 72 | 8 | 14.3 |
| Leatherwood ART II (at its low end) | 3 | 72 | 24 | 4.7 |
| Mini Reflex Sight | 1.2 | 90 | 75 | 1.3 |
| MMGL Sight | 1.2 | 90 | 75 | 1.3 |
| OKP 7 Reflex | 1.2 | 90 | 75 | 1.3 |
| PGO-7 | 2.8 | 90 | 32.1 | 3.47 |
| PU 91/30 Scope | 3.5 | 72 | 20.6 | 5.51 |
| Spitfire 3X | 3 | 90 | 30 | 3.73 |
| Tricon 1.5x Compact Prism Scope | 1.5 | 90 | 60 | 1.73 |
| Vektor Frenix-X Micro Reflex Sight | 1.2 | 90 | 75 | 1.3 |

Combo sights keep the 72 degree start in reflex mode because the test input does not depend on the mode: the reflex view is 60 degrees (1.73x), not 75 degrees (1.30x). Status: FOUND (arithmetic on FOUND inputs). ABSENT: any measured on-screen value (the game was not run).

## 4. Europe minimap row (FOUND)

`DA_UI_Europe` stores `SizeX` 32,768, so the table row was a faithful copy of the stored field. The decoded texture `T_UI_Europe_VT` is 16,384 x 16,384 px (round 78 decode, size read with Pillow). The row now reads "32,768 stored; the texture file is 16,384" and the derived note says the implied 49.8 units per pixel does not match the file (99.6 with 16,384). File: `content/Wardogs_UI_v2.md`.

## Wiki updates

- `_wiki/attachments/sights-and-optics.md`: new "Effective magnification" section with the table; the non-zooming sight sentence now says the stored minimum and maximum are ignored.
- `_wiki/game-mechanics/controls-and-settings.md`: view model paragraph (the setting overwrites the 106); effective magnification explanation under the aiming mode note.
