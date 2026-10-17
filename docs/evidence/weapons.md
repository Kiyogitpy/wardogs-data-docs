# Weapons evidence: RVA status

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page records how strong the evidence is for each native address that
[Weapons](../../Wardogs_Weapons_v2.md) cites. All of them are in its
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
   [`Wardogs_Weapons_v2.md`](../../Wardogs_Weapons_v2.md) at `main`
   `e057d26` was extracted, and values below `0x100000` (component
   offsets such as `+0xFF0` and `+0x408`) were dropped. That left
   **17 RVAs**, all in §5a and §5b.
2. Each RVA was tagged with its citing section and the doc's line numbers
   at `e057d26`.
3. `corpus.sqlite` was queried read-only for the exact `functions` row,
   `traits`, the enclosing row, direct calls and aliases. Bodies were
   searched for `JUMPOUT`, `__asm` and Hex-Rays warnings, and empty
   nullsub rows were flagged.
4. The first instructions at every RVA were decoded from the restored
   executable (`pefile`, Capstone 5.0.7, read-only) to check that each
   row starts on a real entry. Fifteen RVAs are `.pdata` starts with a
   normal prologue. The other two are covered in the notes.
5. The weapons doc was not covered by the round-2 to round-4 ledgers or
   the [damage evidence table](damage.md#table), so every RVA without a
   usable body was disassembled for this page. The direct callers of
   every cited RVA were also found in the executable by scanning for
   `E8`/`E9` and RIP-relative operands, and compared with the corpus
   `calls` table.
6. The statuses that are not a plain corpus body, and the flagged body,
   are claims EV-W1 to EV-W4 (notes below) for the round-5 independent
   verifier.

Re-run the corpus part with `python -I` from the repository root
([`_tools/rva_status.py`](../../_tools/rva_status.py)):

```text
python -I _tools/rva_status.py Wardogs_Weapons_v2.md --rev e057d26 --exe
```

The script's section column prints the heading text ("5a. Recoil") for
these two sections, because it only shortens numeric headings to `§N`.

The status key is the one on the
[vehicle evidence page](vehicles.md#status-key).

## 2. Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 15 (1 with Hex-Rays warnings) |
| `[exe]` | 2 (1 behind a misaligned row, 1 leaf with no row) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **17** |

Every cited address is in `.text`, and none is itself a GObjects fact.
The GObjects-backed values sit next to them. In `WDWeaponBehaviorComponent`
the dump has `[000000E0] EnumProperty AimSwayMode`,
`[00000100] FloatProperty MinFocusInterpRequiredForRecoilReduction` and
`[0000049C] FloatProperty MaxFocusEnergy`. The constructor `0x6B84E80`
sets them to 0, 80.0 and 10.0. The shot counter (`UWDWeaponComponent`
`+0xFF0`), `IsAiming` (`+0x3E0`) and the stabilization timer (`+0x408`)
are not reflected properties; those offsets rest on the instructions only.

## 3. Table

Sections are Weapons sections; `L` numbers are its lines at `e057d26`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x42CD0B0` | `APlayerController` vtable slot 254 (the doc's `IsLocalController`), reached by a virtual call from `0x6B96C20` | §5a (L234) | `corpus body`; no direct calls, see notes |
| `0x699E6C0` | `FWDWeaponStats` constructor: the native defaults behind the recoil table's † | §5a (L249) | `corpus body` |
| `0x6B84E80` | `UWDWeaponBehaviorComponent` constructor: component defaults, `AimSwayMode` | §5b (L298) | `corpus body` |
| `0x6B85D30` | Focus cut, focus drain and `ViewKickMagnitudeMultiplier`; called from the fire routine (`0x6B9438D`) | §5a (L240) | `corpus body` |
| `0x6B87260` | Pattern wrap: rebuilds the two deviation curves | §5b (L311) | `[exe]`: no row of its own; the enclosing row `0x6B8725D` is an empty nullsub; see notes |
| `0x6B88310` | Stops focus when the energy runs out | §5b (L300) | `corpus body` |
| `0x6B884D0` | Aim sway and focus energy tick | §5b (L298) | `corpus body`, flagged: Hex-Rays warnings; see notes |
| `0x6B891F0` | `UWDWeaponBehaviorComponent` slot 131 (`TickComponent`): calls `0x6B89A20` (`0x6B8920C`) and `0x6B884D0` (`0x6B8922B`) | §5a (L244) | `corpus body` |
| `0x6B89A20` | Kick playback step; calls `0x6B89BB0` (`0x6B89B4C`) | §5a (L244) | `corpus body` |
| `0x6B89BB0` | Kick playback: curve deltas, pitch limits, recovery | §5a (L244) | `corpus body` |
| `0x6B8E5A0` | `UWDWeaponComponent` constructor: shot counter `+0xFF0` = −1 | §5a (L234) | `corpus body` |
| `0x6B93610` | Fire routine | §5a (L234) | `corpus body` |
| `0x6B95C50` | Per-shot kick: pattern point or post-pattern ranges | §5a (L235) | `corpus body` |
| `0x6B96C20` | Local-player gate | §5a (L234) | `corpus body` |
| `0x6B97550` | Pattern reset: shot counter back to −1 | §5a (L234) | `[exe]`: no functions row, no `.pdata` entry; see notes |
| `0x6C979A0` | Recoil-multiplier getter, `UWDItemExtension_RangedWeapon` slot 196 | §5a (L238) | `corpus body` |
| `0x6C989A0` | Recoil-multiplier getter, `UWDItemExtension_RangedWeapon` slot 197 | §5a (L238) | `corpus body` |

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

### Other addresses in these notes

The other addresses in the notes are call sites, callees and anchors
that were read for this page; the weapons doc does not cite them, and they
are not part of the counts. The callees are `0x6B86480`, `0x3E0DF10`,
`0x3DFF510`, `0x3AB8810`, `0x6BBD5B0`, `0x3A9B050`, `0x3A97B50` and
`0x3EAA8F0`. `0x6BBD5E0`, the stance accessor, is checked by round 5
as part of §5b.

## 5. Open items

- §5a and §5b have not been verified claim by claim. Round 5 checks them
  separately. A status table settles where the code is, not what it does.
- The stabilization timer (`+0x408`, `AdsStabilizeCooldownRate`), the
  weapon-model sway and the `Weapon` sway mode stay open in
  [Weapons §5b](../../Wardogs_Weapons_v2.md#5b-aim-sway-and-focus-energy).
