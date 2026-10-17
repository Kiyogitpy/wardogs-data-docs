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
   at `main` `e057d26` was extracted, and values below `0x100000`
   (record offsets such as `+0x378`, class sizes, enum values) were
   dropped. That left **53 RVAs**. The page was first built at `479c6c1`
   (36 RVAs). Round 4's corrections added 18, and `0x5230770` is no
   longer cited.
2. Each RVA was tagged with its citing section and the doc's line numbers
   at `e057d26`.
3. `corpus.sqlite` was queried read-only for the exact `functions` row,
   `traits`, the enclosing row, direct calls and aliases. Bodies were
   searched for `JUMPOUT`, `__asm` and Hex-Rays warnings, and empty
   nullsub rows were flagged.
4. The first instructions at every RVA were decoded from the restored
   executable (`pefile`, Capstone 5.0.7, read-only) to check that each
   row starts on a real entry.
5. RVAs without a usable body were checked against the round-2 to
   round-4 verifier ledgers (r2/r3/r4 row IDs; local working files) and the
   [damage evidence table](damage.md#table), and disassembled for this
   page where neither covered them.
6. At `479c6c1`, every status that is not a plain corpus body went to an
   independent verifier as claims EV-1 to EV-22, shared with the vehicle
   page. The verifier confirmed all 22 claims and both pages' counts, and
   recorded EV-21 (`0x766727F`) as a citation error in the doc. The 18
   RVAs added at `e057d26` are round-5 claims for the same verifier; their
   four `[exe]` statuses rest on round-4 ledger rows.

Re-run the corpus part with `python -I` from the repository root
([`_tools/rva_status.py`](../../_tools/rva_status.py)):

```text
python -I _tools/rva_status.py Wardogs_GameplayEffectsPipeline_v1.md --rev e057d26 --exe
```

The status key is the one on the
[vehicle evidence page](vehicles.md#status-key).

## 2. Status counts

| Status | RVAs |
|---|---:|
| `corpus body` | 40 (1 with a Hex-Rays warning) |
| `[exe]` | 13 (1 of them a misaligned citation) |
| `GObjects` | 0 |
| vtable/data | 0 |
| `unverified` | 0 |
| **Total** | **53** |

Every cited address is in `.text`, and none is itself a GObjects fact.
The GObjects-backed values sit next to them: for example the actor's
`Role` byte (`+0x170`, GObjects `[00000170] ByteProperty Role` in
`Actor`), which the role check `0x3CA8630` returns.

## 3. Table

Sections are GameplayEffectsPipeline sections; `L` numbers are its lines
at `e057d26`.

| RVA | Role | Cited in | Verification status |
|---|---|---|---|
| `0x3CA8630` | Component role check: returns the owner's `Role` | §5 (L288) | `[exe]`: no functions row; see notes |
| `0x4C45DC0` | Cue call made by the revive handler | §6 (L308) | `corpus body` |
| `0x5219AB0` | Predicted apply, `ClientInstigated` branch | §5 (L291) | `corpus body` |
| `0x5219C70` | Predicted apply, other branch | §5 (L293) | `corpus body` |
| `0x521B800` | Reflected `ServerApplyEffect` thunk | §1.2 (L86) | `corpus body` |
| `0x521FDE0` | Hook-map emplace; called from `0x5223670` | §4.3 (L242) | `corpus body` |
| `0x5223670` | Hook-map insert; no direct call in the corpus (see notes) | §4.3 (L242) | `corpus body` |
| `0x5227F20` | `ApplyEffect` | §1.2 (L81), §5 (L287) | `corpus body` |
| `0x522A800` | Default evaluator lambda | §4.2 (L211) | `corpus body` |
| `0x522B1B0` | Clamps `Stacks` to `[1, MaxStacks]` (`MaxStacks` 0 = 65535) | §1.2 (L81) | `[exe]`: no functions row (r4 WA-5) |
| `0x522B7D0` | Stack scaling | §4.2 (L200) | `corpus body` |
| `0x522C4F0` | Dirty-attribute flush | §4.2 (L209), §4.3 (L222), §8 (L350) | `corpus body` |
| `0x522CB40` | Re-checks and updates the `OngoingRequirements` flag `+0x150` (E-7) | §8 (L356) | `corpus body` |
| `0x522E5C0` | Combining function | §4.2 (L208), §4.4 (L258), §8 (L350) | `corpus body` |
| `0x522E960` | Scalar evaluator | §4.2 (L192) | `corpus body` |
| `0x522F8F0` | `FindOrAddAttribute` | §1.2 (L84), §4.3 (L221) | `corpus body` |
| `0x52311D0` | Adds a delta and calls `SetAttributeBaseValue` | §1.2 (L85), §4.3 (L248), §8 (L355) | `[exe]`: no functions row (r2 HP-10, r3 V-6) |
| `0x52313E0` | Predicted stack change: pending delta `+0x3C` and the removal key set `+0xF8` (E-7) | §8 (L356) | `[exe]`: no functions row (r4 WA-9) |
| `0x52317F0` | The only reader of the stacking policies | §5 (L297), §7.1 (L338) | `corpus body` |
| `0x5231DA0` | Lowers the pending predicted stack delta `+0x3C` (E-7) | §8 (L356) | `corpus body` |
| `0x52330B0` | Sets `+0x150` when `OngoingRequirements` are not met (E-7) | §8 (L356) | `[exe]`: no functions row (r4 WA-8) |
| `0x5233C00` | Replication receive handler | §4.1 (L170), §4.3 (L221) | `corpus body` |
| `0x5236070` | `ServerApplyEffect` target after the check | §1.2 (L86) | `corpus body` |
| `0x5236230` | `ServerApplyEffect` check | §1.2 (L86) | `corpus body` |
| `0x5236990` | Registers a base-value hook | §4.3 (L226) | `[exe]`: no functions row (r3 V-6) |
| `0x5236AF0` | `SetAttributeBaseValue` | §1.2 (L85), §4.3 (L219) | `[exe]`: no functions row (r2 HP-10, HP-14b; r3 V-6) |
| `0x5236C70` | Registers a current-value hook | §4.3 (L228) | `[exe]`: no functions row (r3 V-6) |
| `0x5236DE0` | Convenience wrapper over `SetAttributeBaseValue` | §4.3 (L251) | `corpus body` |
| `0x5236E50` | Base-value setter: hook, store, replication push | §1.2 (L85), §4.3 (L216) | `[exe]`: no aligned row (`0x5236E4A`); damage evidence table, r3 EV-9 |
| `0x5237050` | Current-value setter | §4.2 (L211), §4.3 (L228) | `[exe]`: no functions row (r3 EM-2) |
| `0x52382E0` | Pushes base and current into `AttributeReplication` | §4.3 (L218) | `[exe]`: row has `JUMPOUT`; see notes |
| `0x523A560` | Library `ModifyBase` | §1.3 (L94), §4.3 (L220) | `corpus body` |
| `0x523AB10` | Library `SetBase` | §1.3 (L95), §4.3 (L220) | `corpus body` |
| `0x533A750` | Vehicle health hook: clamp to `[0, MaxHealth]` | §4.3 (L233) | `corpus body`, flagged: Hex-Rays warning ([vehicle notes](vehicles.md#4-notes-on-particular-rows)) |
| `0x6B17D20` | Character health hook (`UWDCharacterVitalityComponent` slot 161): clamp to `[0, MaxHealth + MaxOverhealHealth + MaxDecayHealth]`, at least 1 while `bInvincible` | §4.3 (L237) | `corpus body` |
| `0x6B81CE0` | Character `Attribute.Gameplay.Health` handle and hook registration (vitality slot 159) | §4.3 (L235) | `corpus body` |
| `0x6B82520` | Vitality base damage: the health write | §4.3 (L249) | `corpus body` |
| `0x6B83270` | Base health hook (`UWDVitalityComponent` slot 161): clamp to `[0, MaxHealth]` | §4.3 (L238) | `corpus body` (a leaf with no `.pdata` entry) |
| `0x6B83360` | Reflected `Auth_Heal` | §4.3 (L250) | `corpus body` |
| `0x6B83560` | Reflected `ResetHealth` | §4.3 (L251) | `corpus body` |
| `0x6C66540` | Reflected `Auth_DecreaseContainerAmount` | §4.3 (L252) | `corpus body` |
| `0x6C692E0` | `WDItemExtension_GameplayEffects` `OnRegister` (slot 110): installs `DefaultAttributes` | §7.1 (L331) | `corpus body` |
| `0x6C9A420` | `OnStanceChanged`: applies the stance preset (`AuthorityOnly`) | §7.1 (L336) | `corpus body` |
| `0x6C9AFB0` | `WDItemExtension_RangedWeapon` slot 159: installs its `DefaultAttributes` with overwrite off | §7.1 (L331) | `corpus body` |
| `0x6C9D170` | Attachment refresh; the only caller of `0x6C9F1A0` and `0x6C9E190` | §7 (L323) | `corpus body` |
| `0x6C9E190` | Applies the selected sight's effects | §7 (L320), §8 (L354) | `corpus body` |
| `0x6C9F1A0` | Applies an attachment's `AppliedEffects` on equip | §7 (L319), §8 (L354) | `corpus body` |
| `0x6C9F6E0` | Bipod unfolded effect list (`FWDBipodAttachmentData` `+0x138`) | §7.1 (L335) | `corpus body` |
| `0x6E75620` | Revive handler (character slot 323) | §4.3 (L253), §6 (L308) | `corpus body` |
| `0x7665D60` | Vehicle-side caller of `0x52311D0` | §8 (L355) | `corpus body` |
| `0x7666070` | Vehicle fuel hook registration (fuel component slot 126) | §4.3 (L239) | `corpus body` |
| `0x766727F` | Vehicle-side caller of `0x52311D0` | §8 (L355) | `[exe]`, misaligned: the entry is `0x7667280` (`Auth_RefillFuel`); see notes |
| `0x7667280` | `Auth_RefillFuel` exec thunk (the real entry behind `0x766727F`) | §8 (L355) | `[exe]`: row failed; the enclosing row `0x766727F` is an empty nullsub (r4 EV-21) |

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
  `0x766727F` is an empty nullsub one byte early)". Corrected in the
  doc with that text, so the doc now cites both addresses. `0x7667280`
  is `[exe]` for the same reason as `0x766727F`: its own row failed and
  the enclosing row is empty.
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
- **`0x5223670`.** The body is decompiled cleanly, but the corpus has no
  direct call to it. Its only callers are the two hook registrars,
  `0x5236990` (call at `0x5236A28`) and `0x5236C70` (`0x5236D08`). They
  have no functions row, so the corpus has no calls rows for those sites
  (r3 V-6, r4 WA-7). It calls the emplace `0x521FDE0`.
- **`0x6B83270`.** A leaf with no `.pdata` entry of its own, so it needs
  no unwind data. The corpus body is the whole function,
  `fmaxf(fminf(*(float *)(a1 + 0x134), a3), 0)`, which matches the
  instructions (`minss`, `maxss` with 0, `ret`). It is
  `UWDVitalityComponent` slot 161.
- **Ledger-backed `[exe]` rows.** `0x52311D0`, `0x5236990`, `0x5236AF0`,
  `0x5236C70`, `0x5236E50` and `0x5237050` were reproduced from the
  instructions in round 2 or 3 (or on the damage evidence page). The
  entries `0x522B1B0`, `0x52313E0` and `0x52330B0` were reproduced in
  round 4 (r4 WA-5, WA-9, WA-8). This page only confirmed that they still
  have no usable row and start on a `.pdata` entry with a normal
  prologue.
- **`0x5230770`.** The stack-count function was cited at `479c6c1` (§8,
  as a `corpus body`) and is no longer cited.

## 5. Open items

- E-2, E-3 and E-6 stay open in
  [GameplayEffectsPipeline §8](../../Wardogs_GameplayEffectsPipeline_v1.md#8-open-questions).
  A status table settles where the code is, not what the fields mean.
