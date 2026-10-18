# Weapons evidence: RVA status

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page records how strong the evidence is for each native address that
[Weapons](../../content/Wardogs_Weapons_v2.md) cites. All of them are in its
recoil (§5a) and aim sway (§5b) sections. It follows the method of the
[damage evidence page](damage.md#3-rva-status-table) and does not restate
the recoil or sway rules. Nothing here is a runtime observation: no game
was run and no process or service was contacted. No claim is made about
server authority or exploitability; security questions go through
[SECURITY.md](../../SECURITY.md).

All addresses are **file RVAs in the restored executable**
`WardogsClient-Win64-Shipping.restored.exe` (SHA-256
`a5c3db10…0cc37`, image base `0x140000000`; the hash was recomputed for
this page). The binary, map, corpus and their hashes are listed in
[damage evidence §1](damage.md#1-binary-identity-and-hashes). The rules for
what counts as evidence are those of
[damage evidence §2.5](damage.md#25-rules-for-what-counts-as-evidence).

## 1. Method

The method is the one on the [vehicle evidence page](vehicles.md#1-method):

1. Every `0x` token in
   [`Wardogs_Weapons_v2.md`](../../content/Wardogs_Weapons_v2.md) at
   `770c47d4` (branch `r6/wpn`, the round-6 corrections) was extracted,
   and values below `0x100000` (component offsets such as `+0xFF0` and
   `+0x408`) were dropped. That left **42 RVAs**, in §2a, §5a and §5b.
   The page was first built at `e057d26` (17 RVAs); the round-5
   corrections (`0f16271`) added 16 and the round-6 corrections added 9,
   and neither removed any.
2. Each RVA was tagged with its citing section and the doc's line numbers
   at `770c47d4`.
3. `corpus.sqlite` was queried read-only for the exact `functions` row,
   `traits`, the enclosing row, direct calls and aliases. Bodies were
   searched for `JUMPOUT`, `__asm` and Hex-Rays warnings, and empty
   nullsub rows were flagged.
4. The first instructions at every RVA were decoded from the restored
   executable (`pefile`, Capstone 5.0.7, read-only) to check that each
   row starts on a real entry. Twenty-five RVAs are `.pdata` starts with
   a normal prologue, and `0x6B8AC90` is a leaf (the reflected
   `GetWallCollisionAlpha` thunk) with its own corpus row. The other
   seven are covered in the notes: four sit
   one to fifteen bytes after a misaligned `.pdata` start, two are leaves
   with no `.pdata` entry, and one is an engine leaf with no row. Of the
   nine RVAs added in round 6, three are `.pdata` starts with a normal
   prologue (`0x6B880D0`, `0x6C9A6A0`, and `0x6C99CB0`, which has no
   corpus row), two are leaves with no `.pdata` entry (`0x19A4A50`, which
   has a corpus row, and `0x6B879A0`, which has none), and four are
   addresses inside a function: the instruction range `0x6B95DD0` in
   `0x6B95C50`, and the call sites `0x763C845`, `0x763D073` and
   `0x8633CD4`.
5. The weapons doc was not covered by the round-2 to round-4 ledgers or
   the [damage evidence table](damage.md#table), so every RVA without a
   usable body was disassembled for this page. The direct callers of
   every cited RVA were also found in the executable by scanning for
   `E8`/`E9` and RIP-relative operands, and compared with the corpus
   `calls` table.
6. The statuses that are not a plain corpus body, and the flagged body,
   went to an independent verifier as claims EV-W1 to EV-W4 (notes
   below). The verifier re-ran the script and the disassembly and
   confirmed all four claims, the page's counts and every table row.
   The 16 RVAs added at `0f16271` come from the round-5 ledger rows
   T2-1, T2-4, T2-16 and T2-20 to T2-31, where the same verifier
   reproduced the instructions; their table rows say "verifier-confirmed
   round 5". The 9 RVAs added at `770c47d4` come from the round-6 ledger
   rows T2-1, T2-6 and T2-7, and `0x166D220` is now checked by T0-5;
   those rows say "verifier-confirmed round 6".

Re-run the corpus part with `python -I` from the repository root
([`_tools/rva_status.py`](../../_tools/rva_status.py)):

```text
python -I _tools/rva_status.py Wardogs_Weapons_v2.md --rev 770c47d4 --exe
```

The script's section column prints the heading text ("5a. Recoil") for
these sections, because it only shortens numeric headings to `§N`.

The status key is the one on the
[vehicle evidence page](vehicles.md#status-key).

## 2. Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 28 (1 with Hex-Rays warnings) |
| `[exe]` | 14 (4 behind a misaligned row, 3 leaves with no row, 2 engine helpers with no row, 1 `.pdata` start with no row, 4 addresses inside a function) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **42** |

Every cited address is in `.text`, and none is itself a GObjects fact.
The GObjects-backed values sit next to them. In `WDWeaponBehaviorComponent`
the dump has `[000000E0] EnumProperty AimSwayMode`,
`[00000100] FloatProperty MinFocusInterpRequiredForRecoilReduction` and
`[0000049C] FloatProperty MaxFocusEnergy`. The constructor `0x6B84E80`
sets them to 0, 80.0 and 10.0. The shot counter (`UWDWeaponComponent`
`+0xFF0`), `IsAiming` (`+0x3E0`) and the stabilization timer (`+0x408`)
are not reflected properties; those offsets rest on the instructions only.

## 3. Table

Sections are Weapons sections; `L` numbers are its lines at `770c47d4`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x1669260` | Jitter noise helper, named Perlin noise from call shape only; called twice from `0x6A7F070` | §5b (L327, L331) | `[exe]`: no functions row, no `.pdata` entry (a leaf); verifier-confirmed round 5 (T2-29, name inferred) |
| `0x166D220` | Rotator → quaternion: fmod 360, × π/360 (`0x9AD08F0`), sine/cosine of the half angles, four doubles out; called from `0x6A80880` (`0x6A813C9`, `0x6A814B1`, `0x6A819D4`) | §5b (L327, L331), change log (L358) | `[exe]`: no functions row; verifier-confirmed round 6 (T0-5) |
| `0x19A4A50` | `IWDWeaponOwner` default for slots 22/23 (`movss xmm0, [0x9AADA28]`, 1.0; `ret`), kept by the `AWDVehicleWeaponExtension` and `AWDMountedWeapon` sub-vtables (`0xB63E858`, `0xB6743F0`), so their weapons get recoil multiplier × 1 | §5b (L333) | `corpus body` (a shared stub; the corpus aliases name vehicle-pawn slot 309); no `.pdata` entry (a leaf); verifier-confirmed round 6 (T2-1) |
| `0x3D84130` | Called with the attach point and a rotator (`SetRelativeRotation` by call shape only) | §5b (L316, L331) | `[exe]`: no aligned row; the enclosing row `0x3D84121` is a misaligned `.pdata` start; verifier-confirmed round 5 (T2-16, T2-24) |
| `0x42CD0B0` | `APlayerController` vtable slot 254 (the doc's `IsLocalController`), reached by a virtual call from `0x6B96C20` | §5a (L236) | `corpus body`; no direct calls, see notes |
| `0x699E6C0` | `FWDWeaponStats` constructor: the native defaults behind the recoil table's † | §5a (L251) | `corpus body` |
| `0x6A7F070` | Sight-sway jitter: two noise calls per jitter, fading as the weapon stabilizes | §5b (L327) | `[exe]`: no aligned row; the enclosing row `0x6A7F06A` is a misaligned `.pdata` start; verifier-confirmed round 5 (T2-29) |
| `0x6A7F870` | `UWDFirstPersonAnimInstance` slot 101; jumps to `0x6A80880` (`0x6A7FBC8`) | §5b (L327) | `corpus body`; verifier-confirmed round 5 (T2-28) |
| `0x6A80880` | Weapon-model sway: builds `SightSwayTransform`; reads the `CurveVector` X / Y | §2a (L156), §5b (L327) | `corpus body`; verifier-confirmed round 5 (T2-28, T2-30) |
| `0x6B84540` | `FWDWeaponAimSwayData` constructor: native defaults | §5b (L325) | `corpus body`; verifier-confirmed round 5 (T2-20) |
| `0x6B84E80` | `UWDWeaponBehaviorComponent` constructor: component defaults, `AimSwayMode` native default | §5b (L302) | `corpus body` |
| `0x6B85D30` | Focus cut, focus drain and `ViewKickMagnitudeMultiplier`; called from the fire routine (`0x6B9438D`) | §5a (L242) | `corpus body` |
| `0x6B86470` | `WDHoldableEquipStateUpdated` listener: writes the equip byte `+0xC11` | §5b (L302) | `[exe]`: no functions row, no `.pdata` entry (a leaf); verifier-confirmed round 5 (T2-1) |
| `0x6B86860` | Binds the eleven sway attribute handles `+0xC18` … `+0xCC0` | §5b (L302) | `corpus body`; verifier-confirmed round 5 (T2-4) |
| `0x6B87260` | Pattern wrap: rebuilds the two deviation curves | §5b (L315) | `[exe]`: no row of its own; the enclosing row `0x6B8725D` is an empty nullsub; see notes |
| `0x6B879A0` | ADS time setter: `movss [rcx+0x3E8], xmm1; ret`; callers `0x6C9A880`, `0x6C99E00`, `0x763C845`, `0x763D073`, `0x8633CD4` | §5b (L335) | `[exe]`: no functions row, no `.pdata` entry (a leaf); verifier-confirmed round 6 (T2-6) |
| `0x6B880D0` | Focus start: adds `AdditionalFocusZoom` × 0.01 (`+0xBD0`) to the focus zoom `+0x3FC` (`0x6B8817A`–`0x6B88182`) | §5b (L335) | `corpus body`; the `+0x3FC` store verifier-confirmed round 6 (T2-7; the × 0.01 and the cooldown gate on the teammate's reading) |
| `0x6B88310` | Stops focus when the energy runs out; on focus end subtracts the same amount from `+0x3FC` (`0x6B88360`–`0x6B88364`) | §5b (L304, L335) | `corpus body`; the `+0x3FC` store verifier-confirmed round 6 (T2-7) |
| `0x6B884D0` | Aim sway and focus energy tick | §5b (L302, L317) | `corpus body`, flagged: Hex-Rays warnings; see notes |
| `0x6B88DD0` | Aim blend `+0x3E4`; called from `0x6B88F20` (`0x6B88F4C`) | §5b (L322) | `[exe]`: no aligned row; the enclosing row `0x6B88DCF` is a misaligned `.pdata` start; verifier-confirmed round 5 (T2-25) |
| `0x6B88F20` | Stabilization timer `+0x408` and the ADS FOV blend | §5b (L319, L323) | `corpus body`; verifier-confirmed round 5 (T2-21, T2-31) |
| `0x6B891F0` | `UWDWeaponBehaviorComponent` slot 131 (`TickComponent`): calls `0x6B89A20` (`0x6B8920C`), `0x6B88F20` (`0x6B89217`) and, when `+0xC11` is set, `0x6B884D0` (`0x6B8922B`) | §5a (L246), §5b (L302) | `corpus body`; the `+0xC11` gate verifier-confirmed round 5 (T2-1) |
| `0x6B89250` | Async muzzle trace | §5b (L329) | `corpus body`; verifier-confirmed round 5 (T2-26) |
| `0x6B89A20` | Kick playback step; calls `0x6B89BB0` (`0x6B89B4C`) | §5a (L246) | `corpus body` |
| `0x6B89BB0` | Kick playback: curve deltas, pitch limits, recovery, the `+0x3D0` total | §5a (L246, L247) | `corpus body`; `+0x3D0` verifier-confirmed round 5 (T1-26) |
| `0x6B8A2F0` | Async "WallCollision" sweep | §5b (L329) | `corpus body`; verifier-confirmed round 5 (T2-27) |
| `0x6B8A700` | Movement factor m `+0xC04` | §5b (L321) | `corpus body`; verifier-confirmed round 5 (T2-22) |
| `0x6B8AC90` | `GetWallCollisionAlpha`: reads `+0x41C` | §5b (L329) | `corpus body`; verifier-confirmed round 5 (T2-27) |
| `0x6B8E5A0` | `UWDWeaponComponent` constructor: shot counter `+0xFF0` = −1 | §5a (L236) | `corpus body` |
| `0x6B93610` | Fire routine | §5a (L236), §5b (L333) | `corpus body` |
| `0x6B95C50` | Per-shot kick: pattern point or post-pattern ranges | §5a (L237) | `corpus body` |
| `0x6B95DD0` | Fire path inside `0x6B95C50`: takes the weapon component's outer (`[rbp+0x20]`), asks it for `IWDWeaponOwner` (`0x6C2B390`, `0x1921820`) and calls slots 22/23 (`[rax+0xB0]` / `[rax+0xB8]`) | §5b (L333) | `[exe]`: an instruction range (`0x6B95DD0`–`0x6B95E07`) inside the corpus body `0x6B95C50`, not an entry; verifier-confirmed round 6 (T2-1) |
| `0x6B96C20` | Local-player gate | §5a (L236) | `corpus body` |
| `0x6B97550` | Pattern reset: shot counter back to −1 | §5a (L236) | `[exe]`: no functions row, no `.pdata` entry; see notes |
| `0x6C979A0` | Horizontal recoil-multiplier getter, `IWDWeaponOwner` interface slot 22 of `UWDItemExtension_RangedWeapon` (the corpus alias reads it as main-table slot 196) | §5a (L240) | `corpus body`; slot verifier-confirmed round 5 (T1-8) |
| `0x6C989A0` | Vertical recoil-multiplier getter, interface slot 23 (corpus alias slot 197) | §5a (L240) | `corpus body`; slot verifier-confirmed round 5 (T1-8) |
| `0x6C99CB0` | Ranged extension: handler for a change of `Attribute.Gameplay.Weapon.AimTime`; sets the ADS time from the current value, or 1.0 (`0x6C99DE1`–`0x6C99E00`, `call 0x6B879A0`) | §5b (L335) | `[exe]`: a `.pdata` start with a normal prologue and no functions row; verifier-confirmed round 6 (T2-6) |
| `0x6C9A6A0` | Ranged extension, on equip: looks up `AimTime` (`0xD36EBA8`) and sets the ADS time from its current value (`0x52301F0`), or 1.0 (`0x6C9A84C`–`0x6C9A880`, `call 0x6B879A0`) | §5b (L335) | `corpus body`; verifier-confirmed round 6 (T2-6) |
| `0x6D54190` | Camera-mode write of the new control rotation (role by call shape only) | §5b (L316, L331) | `corpus body`; the call verifier-confirmed round 5 (T2-16) |
| `0x763C845` | Vehicle-weapon call to the ADS time setter `0x6B879A0` | §5b (L335) | `[exe]`: a call site inside the corpus body `0x763C6C0`, not an entry; verifier-confirmed round 6 (T2-6) |
| `0x763D073` | Vehicle-weapon call to the ADS time setter `0x6B879A0` | §5b (L335) | `[exe]`: a call site inside the corpus body `0x763CE80`, not an entry; verifier-confirmed round 6 (T2-6) |
| `0x8633CD4` | Fifth call to the ADS time setter `0x6B879A0`; the caller is not identified | §5b (L335) | `[exe]`: a call site inside the corpus body `0x8633C40`, not an entry; verifier-confirmed round 6 (T2-6, caller not identified) |

## 4. Notes on particular rows

- **`0x6B87260` (EV-W1).** The corpus has no row at `0x6B87260`. The
  enclosing row `0x6B8725D` is `nullsub_1998` with empty pseudocode,
  because the executable's own `.pdata` entry starts three bytes early:
  decoded from `0x6B8725D`, the first instruction is `ret 0xC933`. The real
  entry is `0x6B87260` (`push rbx; push rbp; push rsi`, then
  `sub rsp, 0x78`). Both direct calls target it: `0x6B86819` in
  `0x6B86480`, and `0x6B88A88` in the sway tick `0x6B884D0`. The corpus
  `calls` table records the same two sites with the target `0x6B87260`.
  The instructions run two loops, one per movement curve. For each key,
  a loop takes `rand()` (the `api-ms-win-crt-utility` import, `0x6B8734C`
  and `0x6B873BB`), masks it with `0x7FFF` and scales it into a min/max
  pair read from the second argument (`+0x1A8`/`+0x1AC`, then
  `+0x1B0`/`+0x1B4`). It reads the key's time through `0x3E0DF10` and adds
  a key with that time and the random value through `0x3DFF510`
  (`0x6B87396`). The doc cites the true entry.
- **`0x6B97550` (EV-W2).** No functions row and no `.pdata` entry; it is a
  leaf that needs none. The whole function is
  `mov dword [rcx+0xFF0], 0xFFFFFFFF; ret`. Nothing calls it directly, so
  the corpus records no calls. Its only reference is
  `lea rax, [rip+0x3168]` at `0x6B943E1` inside the fire routine
  `0x6B93610`. There it is stored with a zero adjustment as a 16-byte
  member-function pointer and passed, with the handle at component
  `+0x1100`, to `0x3AB8810` (`0x6B94411`). The rate comes from
  `0x6BBD5B0` (`0x6B943CE`). Just before, the fire routine calls
  `0x6B85D30` (`0x6B9438D`) and stores the new counter at `+0xFF0`
  (`0x6B94399`).
- **`0x6B884D0` (EV-W3, warnings).** The pseudocode starts with "bad sp
  value at call has been detected" and "positive sp value has been
  detected, the output may be wrong!". The row itself is aligned: it is a
  `.pdata` start, the prologue reserves `0xF60` bytes (`0x6B884DC`), and
  the one epilogue releases the same amount (`0x6B88DC3`). The corpus row
  ends at `0x6B88DCE`, the end of the function's last `.pdata` chunk
  (`0x6B88DAB`–`0x6B88DCE`). These
  instruction anchors match what the doc cites:
  - the `IsAiming` byte `+0x3E0` (`0x6B885FD`, `0x6B88760`, `0x6B887CC`);
  - the stance accessor `0x6BBD5E0` (`0x6B887B1`);
  - the stabilization timer `+0x408` (`0x6B88825`);
  - the focus stop `0x6B88310` (`0x6B88656`);
  - the pattern wrap `0x6B87260` (`0x6B88A88`).

  Its one caller is `TickComponent` `0x6B891F0` (`0x6B8922B`). The sway
  arithmetic itself was not re-derived from the instructions for this
  page. That is round 5's §5b check, and it should not rest on the
  pseudocode alone.
- **`0x42CD0B0` (EV-W4).** The body is decompiled cleanly, but the
  `calls` table has no call to it, because it is reached only through the
  vtable. The gate `0x6B96C20` ends with `call qword [rax+0x7F0]`
  (`0x6B96C8F`), which is slot 254. Slot 254 of `AWDPlayerController_VFT`,
  `APlayerController_VFT` and five other controller vtables is
  `0x42CD0B0` (7 pointers in the executable). The body returns 1 at once
  when the byte at `+0x6D4` is set. Otherwise it calls `0x3A9B050`,
  `0x3A97B50` and `0x3EAA8F0`, and either sets `+0x6D4` and returns 1, or
  returns the byte or 0. That is the shape of a cached-flag
  `IsLocalController`, the name the doc uses; the helpers were not
  identified for this page.
- **Constructors.** `0x6B84E80` and `0x6B8E5A0` have no direct call and
  no pointer outside `.pdata` and the unwind data. They are identified by
  the vtable they store: `UWDWeaponBehaviorComponent_VFT` and
  `UWDWeaponComponent_VFT`. `0x6B8E5A0` calls `0x699E6C0` on its `+0x140`
  stats block (`0x6B8E65B`).
- **Direct callers.** The executable scan found the corpus `calls` rows
  for every cited RVA, plus two calls to `0x6B96C20` (`0x6B98B7E`,
  `0x6B98BC5`) in a `.pdata` chunk that starts at `0x6B98B40`. The corpus
  has no row covering that chunk, so it has no calls rows for those two
  sites. They do not change any status.

- **Round-5 misaligned rows (`0x6B88DD0`, `0x6A7F070`, `0x3D84130`).**
  Like `0x6B87260`, each starts a few bytes after a `.pdata` start that
  the corpus uses as its row. Decoded from the row, the first
  instructions are junk; decoded from the cited RVA, they are a normal
  prologue:
  - `0x6B88DCF` gives `add dword [rax+0x53], eax`; `0x6B88DD0` gives
    `push rbx; sub rsp, 0x70`. Its caller is `0x6B88F4C` in
    `0x6B88F20` (r5 T2-25).
  - `0x6A7F06A` gives `lodsd; ret`; `0x6A7F070` gives
    `mov rax, rsp; …; push rdi; sub rsp, 0x80`. It is called at
    `0x6A80F93` and `0x6A81209` in `0x6A80880` (r5 T2-29).
  - `0x3D84121` gives `mov [rsp+0x20], rax; push rsi; movsx …`;
    `0x3D84130` gives `mov rax, rsp; …; push rdi; sub rsp, 0xA0`. The
    sway tick calls it at `0x6B88C30` and `0x6B88D7B` (r5 T2-16, T2-24).
- **Leaves (`0x6B86470`, `0x1669260`).** Neither has a `.pdata` entry.
  `0x6B86470` is the whole function
  `cmp byte [rdx], 1; sete al; mov [rcx+0xC11], al; ret`; its one code
  reference is a `lea` at `0x6B866B2` in `0x6B86480`, which binds it to
  `WDHoldableEquipStateUpdated` (r5 T2-1). `0x1669260` starts
  `movaps xmm5, xmm0; lea rdx, [rip-…]; …; roundps`, an engine helper
  with many callers; the Perlin-noise name is inferred (r5 T2-29).
- **`0x166D220` (round 6, T0-5).** A `.pdata` start
  (`0x166D220`–`0x166D36F`) with a normal prologue
  (`push rbx; sub rsp, 0x80`) but no functions row. It reads three
  doubles (pitch and yaw at `+0`, roll at `+0x10`), takes them modulo 360
  (`divpd` by 360 at `0x9AD0930`, a truncating `roundpd`, `mulpd`,
  `subpd`), multiplies by π/360 (`0x9AD08F0`), calls `0x98EB1D0` twice for
  the sines and cosines of the half angles, and writes four doubles: UE's
  rotator → quaternion. The verifier's disassembly of `0x6A80880` shows
  three calls to it (`0x6A813C9`, `0x6A814B1`, `0x6A819D4`), the first
  just before the `SightSwayTransform` rotation is stored; the executable
  has 669 `E8`/`E9` sites to it, an engine helper. The doc now names it
  without the call-shape caveat.

### Other addresses in these notes

The other addresses in the notes are call sites, callees and anchors
that were read for this page; the weapons doc does not cite them, and they
are not part of the counts. The callees are `0x6B86480`, `0x3E0DF10`,
`0x3DFF510`, `0x3AB8810`, `0x6BBD5B0`, `0x3A9B050`, `0x3A97B50` and
`0x3EAA8F0`, plus `0x98EB1D0` and the constants `0x9AD0930` / `0x9AD08F0`
read by `0x166D220`. `0x6BBD5E0`, the stance accessor, was checked by round 5
as part of §5b (r5 T2-10). The round-5 call sites and anchors in the
notes above (`0x6B88F4C`, `0x6A80F93`, `0x6A81209`, `0x6B88C30`,
`0x6B88D7B`, `0x6B866B2`, `0x6A813C9`, `0x6A814B1`, `0x6A819D4`) are
not cited by the doc either.

## 5. Open items

- Round 5 checked §5a and §5b claim by claim, and round 6 closed four of
  the open items (T2-1, T2-2, T2-6, T2-7); the doc carries both rounds'
  corrections at `770c47d4`. A status table settles where the code is,
  not what it does.
- Still open in
  [Weapons §5b](../../content/Wardogs_Weapons_v2.md#5b-aim-sway-and-focus-energy):
  the sight-multiplier data path and the reader of `+0x3D0`. Blueprint
  implementers of `IWDWeaponOwner` were not searched, and the caller
  around `0x8633CD4` is not identified.
