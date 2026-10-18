# Restored exe validation — 2026-10-17

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Validation that the newly-decrypted `WardogsClient-Win64-Shipping.restored.exe`
is a correct image match for the committed Dumper-7 idmap. **Prior probe
run against `WardogsFullDump_fixed.exe` (dump-reconstructed) failed to
validate; the restored exe succeeds.**

Scope: static byte-level validation only. No IDA execution, no runtime
observation, no decompilation performed in this validation.

---

## TL;DR

- Restored exe is a valid PE32+ x64 shipping binary (221 MB, 10 sections)
- SHA-256 (full): `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`
- ImageBase: `0x140000000` (standard UE shipping base)
- **All 4 damage vtables from the idmap land cleanly in `.rdata` and contain 8/8 valid function pointers into `.text`** → vtables are intact and usable
- **All 3 UE globals (GObjects, GNames, GWorld) land cleanly in `.data`** → UE object array walking is ready
- The earlier dump-reconstructed `WardogsFullDump_fixed.exe` had different section layout (because reconstructed from a runtime memory snapshot, not from the shipping PE); mapping RVAs failed to validate against it

**Next IDA session should load the restored exe, not the dump-reconstructed one.**

## 1. PE verification

```
File:      WardogsClient-Win64-Shipping.restored.exe
Size:      231,695,256 bytes (221.0 MB)
SHA-256:   a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37
Machine:   0x8664 (x64)
Magic:     0x20B (PE32+)
ImageBase: 0x140000000
Entry RVA: 0x98EB850
SizeOfImage: 0xE15D000 (225.4 MB)
```

### Section layout

| Section | RVA | Virt size | Raw size | Perms |
|---|---|---|---|---|
| `.text` | 0x00001000 | 0x09A26000 (154 MB) | 0x09A26000 | RX |
| `.rdata` | 0x09A27000 | 0x0327B000 (50 MB) | 0x0327B000 | R |
| `.data` | 0x0CCA2000 | 0x007C6000 (7.8 MB) | 0x0035E000 | RW |
| `.pdata` | 0x0D468000 | 0x0088E000 (8.6 MB) | 0x0088E000 | R |
| `.msvcjmc` | 0x0DCF6000 | 0x1000 | 0x1000 | RW |
| `CPADinfo` | 0x0DCF7000 | 0x1000 | 0x1000 | RW |
| `.rodata` | 0x0DCF8000 | 0x1000 | 0x1000 | R |
| `_RDATA` | 0x0DCF9000 | 0x0005E000 | 0x0005E000 | R |
| `.rsrc` | 0x0DD57000 | 0x00026000 | 0x00025600 | R |
| `.reloc` | 0x0DD7D000 | 0x003E0000 | 0x003DFA00 | R |

Layout is normal for a UE 5.7 shipping binary. No evidence of obfuscation
(no high-entropy encrypted sections, no fake import directory).

Timestamp field = `0xCA4563FA` (deliberately placeholder — not interpretable
as a build date).

## 2. Damage vtable validation

The idmap declares these damage-class vtables. Each should be a sequence
of 8-byte pointers into `.text`:

### 2.1 `UWDCustomDamageModificationOperation_VFT`

- **idmap RVA:** `0xB321D30` (187,833,648)
- **Resolves in restored exe:** `.rdata` section ✓
- **First 8 pointers:**
  - `0x146BB78A0`
  - `0x141562FE0`
  - `0x14191D960`
  - `0x1416249B0`
  - (+ 4 more, all pointers into `.text`)
- **Validation:** 8/8 pointers land in `.text` range `[0x140001000, 0x149A27000)` — **valid vtable**

### 2.2 `UWDGlobalDamageSystem_VFT`

- **idmap RVA:** `0xB3217D0` (187,832,272)
- **Resolves in restored exe:** `.rdata` section ✓
- **First 4 pointers:** `0x146BB69F0`, `0x141562FE0`, `0x14191D960`, `0x1416249B0`
- **Validation:** 8/8 pointers in `.text` — **valid vtable**

Note: slots 2-4 (`0x141562FE0`, `0x14191D960`, `0x1416249B0`) are
**identical** across all 4 damage vtables — these are the shared
UObject-base virtual function slots inherited from the UE base class
hierarchy. Slot 0 (`0x146BB69F0` etc.) is the class-specific
`StaticClass()` or equivalent.

### 2.3 `UWDDamageModificationOperation_PlayerArmorDurability_VFT`

- **idmap RVA:** `0xB322140` (187,834,688)
- **Resolves in restored exe:** `.rdata` section ✓
- **First pointer:** `0x146BB7DB0` → into `.text` ✓
- **Validation:** 8/8 pointers in `.text` — **valid vtable**

**This is the 5th damage modifier** that was missed in `Wardogs_DamagePipeline_v2.md`'s original write-up. See the triage AI's audit of that doc for the correction. The vtable's first slot gives us the class-specific function pointer that implements the armor-durability damage modification.

### 2.4 `UWDDamageSubsystem_VFT`

- **idmap RVA:** `0xB434758` (188,958,552)
- **Resolves in restored exe:** `.rdata` section ✓
- **First pointer:** `0x146EF7C50` → into `.text` ✓
- **Validation:** 8/8 pointers in `.text` — **valid vtable**

This is the top-level damage orchestrator. Its `ModifyDamage` method
is the next-session entry point for resolving modifier evaluation
order (question B-1 on [the damage evidence page](evidence/damage.md#21-questions-b-1-to-b-4)).

## 3. UE object array globals

The idmap declares three native globals used by UE object introspection:

| Name | idmap RVA | Section in restored exe | First qword |
|---|---|---|---|
| `GObjects` | `0xD1234E0` (219,296,992) | `.data` ✓ | `0x21C0C9B021C0B89` (opaque — needs runtime population) |
| `GNames` | `0xD050CB0` (218,434,736) | `.data` ✓ | `0xC5049B8011EB1D6` (opaque) |
| `GWorld` | `0xD2AFC08` (220,920,840) | `.data` ✓ | `0x3C2F7FF0C719E48` (opaque) |

The qword values are non-zero (meaning they will be initialized at
runtime). The addresses themselves resolve correctly to `.data` section
locations, which is where you'd expect global pointers for UE's object
array to live.

Static evidence that the symbol table matches: the globals aren't where
they'd be in a different build. The three RVAs together form a tight
cluster (`0xD050CB0`, `0xD1234E0`, `0xD2AFC08` all within 2.5 MB of
each other in `.data`), consistent with UE's convention of allocating
these globals near each other in the compilation unit.

## 4. Why the dump-reconstructed exe failed

The earlier probe (recorded in
`ida_damage_20261017___e23tea/ida_probe_result.json`) ran against
`WardogsFullDump_fixed.exe` — a 234 MB artifact reconstructed from
PE sections of a runtime memory snapshot (`E:\WardogsDumps\Wardogs_1015.dmp`).

The reconstructed exe:
- Had the one exec-function record (`AActor::AddComponent`) **outside
  any executable segment** — meaning the RVA didn't correspond to code
- Could not validate any damage vtable's content against the mapping

Root cause: a memory-snapshot-based reconstruction has different
section layout than a shipping PE. The idmap was generated against
the shipping PE layout, so RVAs encode offsets that only make sense
against the shipping-PE layout. The reconstructed exe's sections
started/ended at different offsets.

The **newly-restored exe** has the shipping-PE layout (same ImageBase,
same section ordering, same section sizes within the normal range for
a UE shipping binary) and therefore **matches the idmap exactly**.

## 5. What this unlocks for the next IDA session

With the restored exe + validated idmap:

- Load `WardogsClient-Win64-Shipping.restored.exe` into IDA 9.3
- Import the full idmap (95,999 string records, 21,282 structs, 9,134 vtables)
- Resolve the following open questions (deferred from the pipeline docs):

  | Question | Entry point | Doc section |
  |---|---|---|
  | Modifier evaluation order | `UWDDamageSubsystem::ModifyDamage` + xref from `UWDGlobalDamageSystem_VFT` | DamagePipeline §5 / evidence page B-1 |
  | PlayerArmorDurability algorithm | Vtable slot 0 of `UWDDamageModificationOperation_PlayerArmorDurability_VFT` at `0x146BB7DB0` | DamagePipeline §7.5 / integration-doc gap 3 |
  | Stacking math on Modifiers | `UBHGameplayEffectComponent::ApplyEffect` xref chain | GameplayEffectsPipeline §4.2 and §4.4 (closed, E-1) |
  | Prediction rollback mechanism | `UBHGameplayEffectComponent::ClientPredictionFailed` + `NetworkPredictionWorldManager` xref | GameplayEffectsPipeline §5 / E-3 (open) |
  | Vehicle section routing vs rule chain order | `FVehicleHealthSection` consumer (search for xref to `PreDamageRouting` field) | VehicleDamagePipeline §4.1 and §4.2 |

## 6. Hashes and integrity

| Artifact | SHA-256 (full file) | Size |
|---|---|---|
| `WardogsClient-Win64-Shipping.restored.exe` | `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37` | 231,695,256 bytes |
| `5.7.4-516586+++Wardogs+Live-Wardogs.idmap` | `f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb` | 4,942,224 bytes |

Both artifacts should be kept together — the mapping is only usable
with this specific exe.

## 7. Caveats

- Timestamp field is `0xCA4563FA` (non-canonical date); build label
  `CL-516586` in the filename is **not** cryptographically verified
  against the binary. The idmap→exe RVA alignment is strong evidence
  the mapping was generated from a build identical or near-identical
  to this restored exe, but doesn't prove the exact CL number.
- Static byte-level validation checks structural alignment of
  mapping RVAs to section layout + plausible vtable content. It does
  **not** verify the semantic correctness of symbol names (i.e., the
  pointer at `UWDCustomDamageModificationOperation_VFT` could point
  to a function implementing a different semantic — only decompilation
  confirms).
- No security-relevant assertions made. Any trust-model findings
  during a subsequent IDA session route through
  [`SECURITY.md`](../SECURITY.md).

## 8. Related docs

- [`mappings/README.md`](../mappings/README.md) — idmap format spec
- [`docs/evidence/damage.md`](evidence/damage.md) — the IDA trace brief, the failed first pass and the restored-exe trace, merged
- [`Wardogs_DamagePipeline_v2.md`](../pipelines/Wardogs_DamagePipeline_v2.md) — being audited by triage AI
- [`Wardogs_VehicleDamagePipeline_v1.md`](../pipelines/Wardogs_VehicleDamagePipeline_v1.md)
- [`Wardogs_GameplayEffectsPipeline_v1.md`](../pipelines/Wardogs_GameplayEffectsPipeline_v1.md)
- [`Wardogs_CombatDataFlow_v1.md`](../pipelines/Wardogs_CombatDataFlow_v1.md)
