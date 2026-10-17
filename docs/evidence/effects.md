# Gameplay effects evidence: RVA status

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

This page records how strong the evidence is for each native address that
[GameplayEffectsPipeline](../../Wardogs_GameplayEffectsPipeline_v1.md)
cites. It follows the method of the
[damage evidence page](damage.md#3-rva-status-table) and does not restate
the effect rules. Nothing here is a runtime observation: no game was run
and no process or service was contacted. No claim is made about server
authority, prediction or exploitability; security questions go through
[SECURITY.md](../../SECURITY.md).

All addresses are **file RVAs in the restored executable**
`WardogsClient-Win64-Shipping.restored.exe` (SHA-256
`a5c3db10…0cc37`, image base `0x140000000`). The binary, map, corpus and
their hashes are listed in
[damage evidence §1](damage.md#1-binary-identity-and-hashes). The rules for
what counts as evidence are those of
[damage evidence §2.5](damage.md#25-rules-for-what-counts-as-evidence).

## 1. Method

The method is the one on the [vehicle evidence page](vehicles.md#1-method):

1. Every `0x` token in
   [`Wardogs_GameplayEffectsPipeline_v1.md`](../../Wardogs_GameplayEffectsPipeline_v1.md)
   at `main` `479c6c1` was extracted, and values below `0x100000`
   (record offsets such as `+0x378`, class sizes, enum values) were
   dropped. That left **36 RVAs**.
2. Each RVA was tagged with its citing section and the doc's line numbers
   at `479c6c1`.
3. `corpus.sqlite` was queried read-only for the exact `functions` row,
   `traits`, the enclosing row, direct calls and aliases. Bodies were
   searched for `JUMPOUT`, `__asm` and Hex-Rays warnings, and empty
   nullsub rows were flagged.
4. The first instructions at every RVA were decoded from the restored
   executable (`pefile`, Capstone 5.0.7, read-only) to check that each
   row starts on a real entry.
5. RVAs without a usable body were checked against the round-2 and
   round-3 verifier ledgers (r2/r3 row IDs; local working files) and the
   [damage evidence table](damage.md#table), and disassembled for this
   page where neither covered them.
6. Every status that is not a plain corpus body went to an independent
   verifier as claims EV-1 to EV-22, shared with the vehicle page. The
   verifier confirmed all 22 claims and both pages' counts, and recorded
   EV-21 (`0x766727F`) as a citation error in the doc.

Re-run the corpus part with `python -I` from the repository root
([`_tools/rva_status.py`](../../_tools/rva_status.py)):

```text
python -I _tools/rva_status.py Wardogs_GameplayEffectsPipeline_v1.md --rev 479c6c1 --exe
```

The status key is the one on the
[vehicle evidence page](vehicles.md#status-key).

## 2. Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 27 (1 with a Hex-Rays warning) |
| `[exe]` | 9 (1 of them a misaligned citation) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **36** |

Every cited address is in `.text`, and none is itself a GObjects fact.
The GObjects-backed values sit next to them: for example the actor's
`Role` byte (`+0x170`, GObjects `[00000170] ByteProperty Role` in
`Actor`), which the role check `0x3CA8630` returns.

## 3. Table

Sections are GameplayEffectsPipeline sections; `L` numbers are its lines
at `479c6c1`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x3CA8630` | Component role check: returns the owner's `Role` | §5 (L284) | `[exe]`: no functions row; see notes |
| `0x4C45DC0` | Cue call made by the revive handler | §6 (L300) | `corpus body` |
| `0x5219AB0` | Predicted apply, `ClientInstigated` branch | §5 (L287) | `corpus body` |
| `0x5219C70` | Predicted apply, other branch | §5 (L289) | `corpus body` |
| `0x521B800` | Reflected `ServerApplyEffect` thunk | §1.2 (L86) | `corpus body` |
| `0x5227F20` | `ApplyEffect` | §1.2 (L81), §5 (L283) | `corpus body` |
| `0x522A800` | Default evaluator lambda | §4.2 (L211) | `corpus body` |
| `0x522B7D0` | Stack scaling | §4.2 (L200), §8 (L322) | `corpus body` |
| `0x522C4F0` | Dirty-attribute flush | §4.2 (L209), §4.3 (L222), §8 (L316) | `corpus body` |
| `0x522E5C0` | Combining function | §4.2 (L208), §4.4 (L253), §8 (L316) | `corpus body` |
| `0x522E960` | Scalar evaluator | §4.2 (L192) | `corpus body` |
| `0x522F8F0` | `FindOrAddAttribute` | §1.2 (L84), §4.3 (L221) | `corpus body` |
| `0x5230770` | Stack count | §8 (L322) | `corpus body` |
| `0x52311D0` | Adds a delta and calls `SetAttributeBaseValue` | §1.2 (L85), §4.3 (L243), §8 (L321) | `[exe]`: no functions row (r2 HP-10, r3 V-6) |
| `0x5233C00` | Replication receive handler | §4.1 (L170), §4.3 (L221) | `corpus body` |
| `0x5236070` | `ServerApplyEffect` target after the check | §1.2 (L86) | `corpus body` |
| `0x5236230` | `ServerApplyEffect` check | §1.2 (L86) | `corpus body` |
| `0x5236990` | Registers a base-value hook | §4.3 (L226) | `[exe]`: no functions row (r3 V-6) |
| `0x5236AF0` | `SetAttributeBaseValue` | §1.2 (L85), §4.3 (L219) | `[exe]`: no functions row (r2 HP-10, HP-14b; r3 V-6) |
| `0x5236C70` | Registers a current-value hook | §4.3 (L228) | `[exe]`: no functions row (r3 V-6) |
| `0x5236DE0` | Convenience wrapper over `SetAttributeBaseValue` | §4.3 (L246) | `corpus body` |
| `0x5236E50` | Base-value setter: hook, store, replication push | §1.2 (L85), §4.3 (L216) | `[exe]`: no aligned row (`0x5236E4A`); damage evidence table, r3 EV-9 |
| `0x5237050` | Current-value setter | §4.2 (L211), §4.3 (L228) | `[exe]`: no functions row (r3 EM-2) |
| `0x52382E0` | Pushes base and current into `AttributeReplication` | §4.3 (L218) | `[exe]`: row has `JUMPOUT`; see notes |
| `0x523A560` | Library `ModifyBase` | §1.3 (L94), §4.3 (L220) | `corpus body` |
| `0x523AB10` | Library `SetBase` | §1.3 (L95), §4.3 (L220) | `corpus body` |
| `0x533A750` | Vehicle health hook: clamp to `[0, MaxHealth]` | §4.3 (L233) | `corpus body`, flagged: Hex-Rays warning ([vehicle notes](vehicles.md#4-notes-on-particular-rows)) |
| `0x6B81CE0` | Character `Attribute.Gameplay.Health` handle and hook registration (vitality slot 159) | §4.3 (L235) | `corpus body` |
| `0x6B82520` | Vitality base damage: the health write | §4.3 (L244) | `corpus body` |
| `0x6B83360` | Reflected `Auth_Heal` | §4.3 (L245) | `corpus body` |
| `0x6B83560` | Reflected `ResetHealth` | §4.3 (L246) | `corpus body` |
| `0x6C66540` | Reflected `Auth_DecreaseContainerAmount` | §4.3 (L247) | `corpus body` |
| `0x6E75620` | Revive handler (character slot 323) | §4.3 (L248), §6 (L300) | `corpus body` |
| `0x7665D60` | Vehicle-side caller of `0x52311D0` | §8 (L321) | `corpus body` |
| `0x7666070` | Vehicle fuel hook registration (fuel component slot 126) | §4.3 (L236) | `corpus body` |
| `0x766727F` | Vehicle-side caller of `0x52311D0` | §8 (L321) | `[exe]`, misaligned: the entry is `0x7667280` (`Auth_RefillFuel`); see notes |

## 4. Notes on particular rows

- **`0x766727F` (misaligned citation).** The corpus row at `0x766727F` is
  `nullsub_2057` with empty pseudocode: the byte is a lone `ret`. The real
  entry is `0x7667280` (`mov [rsp+8], rbx`). It is registered as
  `WDVehicleFuelComponent::Auth_RefillFuel`, and its corpus row failed
  with "Candidate entry lies inside another function at RVA `0x766727F`".
  The exec thunk reads a float parameter, and when it is above 0 calls
  `0x52311D0` on the component's `+0x138` handle (`0x766735E`). The
  corpus body `0x7665D60` makes the same call (`0x7665D7F`). The
  verifier's replacement for the E-6 citation (EV-21) is "(`0x7665D60`,
  and the `Auth_RefillFuel` exec thunk `0x7667280`; the corpus row
  `0x766727F` is an empty nullsub one byte early)". This page does not
  change the doc.
- **`0x3CA8630`.** No functions row; it is a leaf with no `.pdata` entry
  of its own:
  `mov rax, [rcx+0xC8]; test rax, rax; je; movzx eax, byte [rax+0x170]; ret`.
  It returns the owner's `Role`, and 0 when there is no owner. `+0x170` is
  `Actor.Role` in GObjects; the component's owner pointer at `+0xC8` is
  not reflected. The corpus records 242 direct calls to it.
- **`0x52382E0`.** The row is `decompiled_with_jumps` and its body
  contains `JUMPOUT`, so it is not a corpus body. The instructions copy
  the record's base (`+0x28`) and current (`+0x30`) values into the
  replicated item (stride `0x38`, item `+0x18`/`+0x20`; `0x52382FF`,
  `0x5238312`) and mark the item dirty. They then call the role check
  `0x3CA8630` and, for role 3, tail-jump to `0x2480AB0` (`0x523836A`).
  The callers are the base setter (`0x5236F85`) and the current-value
  setter (`0x5237183`).
- **`0x533A750`.** See the
  [vehicle page](vehicles.md#4-notes-on-particular-rows): the body has a
  "may be wrong" warning, and the clamp was reproduced from the
  instructions (r3 V-6).
- **Ledger-backed `[exe]` rows.** `0x52311D0`, `0x5236990`, `0x5236AF0`,
  `0x5236C70`, `0x5236E50` and `0x5237050` were reproduced from the
  instructions in round 2 or 3 (or on the damage evidence page). This
  page only confirmed that they still have no usable row.

## 5. Open items

- E-2, E-3 and E-5 to E-7 stay open in
  [GameplayEffectsPipeline §8](../../Wardogs_GameplayEffectsPipeline_v1.md#8-open-questions).
  A status table settles where the code is, not what the fields mean.
