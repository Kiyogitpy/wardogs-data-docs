# Pass C Crash Analysis — Full Decode
Session: 2026-10-16  (Pass C attempt on Wardogs/Elytra)

## Final Crash

Bugcheck:
```
STOP 0x1E (KMODE_EXCEPTION_NOT_HANDLED)
Arg1: ffffffffc0000096  (STATUS_PRIVILEGED_INSTRUCTION)
Arg2: ffff8b0ed1011b00  (fault address)
Arg3: 0000000000000000
Arg4: 0000000000000000
```

Stack:
```
nt!KeBugCheckEx
nt!KiDispatchException+0x142ec3
nt!KiExceptionDispatch+0x12c
nt!KiGeneralProtectionFault+0x32f    ← Windows's #GP handler
0xffff8b0ed1011b00                     ← fault site
0xffff8b0ed1022b81                     ← caller return address
```

Register-spilled onto stack (CPUID output from init path):
- `000b0671` — CPUID.1.EAX (family 6, model 0xA7, stepping 1)
- `bfebfbff` — CPUID.1.EDX (standard features)
- `7ffafbbf` — CPUID.1.ECX (SSE42, AVX, etc.)
- `18800800` — CPUID.0.EAX (max basic leaf = 0x18 = Alder Lake range)

## Address Decode (crash RIP → source instruction)

From kdmap_run.log, hyperhv.dll's mapped base: `0xFFFF8B0ED1010000`

Crash offset into hyperhv.dll: `0x1B00`
Caller return offset: `0x12B81`

### At hyperhv.dll + 0x1B00 (file offset 0xF00 in hyperhv.dll)

Hex: `0f 32 48 c1 e2 20 48 0b c2 c3`
Disasm:
```
0F 32                 RDMSR            ← CRASHED HERE
48 C1 E2 20           shl rdx, 32
48 0B C2              or rax, rdx
C3                    ret
```

This is a 10-byte `__readmsr` wrapper function. First instruction is
`RDMSR` which reads the MSR identified by `ECX` into `EDX:EAX`.

### At hyperhv.dll + 0x1B10 (next function, for context)

```
0F 33                 WRMSR
48 C1 E2 20           shl rdx, 32
48 0B C2              or rax, rdx
C3                    ret
```

`__writemsr` wrapper. Same shape.

### At hyperhv.dll + 0x1B20

```
0F 31                 RDTSC
...
```

`__rdtsc` wrapper.

### At hyperhv.dll + 0x1B30

```
4C 8B C1              mov r8, rcx
0F 01 F9              RDTSCP
...
```

`__rdtscp` wrapper.

So RVA 0x1B00..0x1B40 is a cluster of MSR/TSC intrinsic wrappers.
`RDMSR` is the first.

### Caller at hyperhv.dll + 0x12B40 (file offset 0x11F40)

Function prologue (32 bytes):
```
48 89 5C 24 18        mov [rsp+0x18], rbx
57                    push rdi
48 83 EC 20           sub rsp, 0x20
B9 00 02 00 00        mov ecx, 0x200          ← MSR 0x200 = IA32_MTRR_PHYSBASE0
E8 BC F1 FE FF        call <helper function>  ← indirectly reaches RDMSR
48 8B F8              mov rdi, rax
48 89 44 24 38        mov [rsp+0x38], rax
48 85 C0              test rax, rax
75 ???                jnz ???
```

The caller sets `ecx = 0x200` (= `IA32_MTRR_PHYSBASE0`) and calls a
helper that ultimately runs `RDMSR` at hyperhv + 0x1B00.

**MSR 0x200 is IA32_MTRR_PHYSBASE0** — part of the variable MTRR range
registers (Intel SDM Vol 4, §2.1 "Table of MSRs"). This is a per-CPU
MSR that holds the base physical address + memory type for the first
variable MTRR range.

MSR 0x200 is defined on all Intel P6+ CPUs (since 1995). Reading it
should NOT raise #GP on normal operation.

## Why #GP on IA32_MTRR_PHYSBASE0?

The caller function at RVA 0x12B40 is HyperDbg's `EptBuildMtrrMap()`
or a close equivalent — it walks the variable MTRR registers to build
an EPT memory-type map.

On an UP CPU, this just works. On a hybrid 12th+ gen Intel part, there
are several documented quirks:

1. **MTRR state isn't fully initialized on E-cores until after a specific
   boot phase.** If `KeIpiGenericCall` dispatches this to an E-core
   before the kernel finishes per-core MTRR init, `RDMSR 0x200` can
   raise #GP(0).

2. **Hyper-V/VBS virtualization leaves some MSRs trapped.** If
   `prep_hyperdbg.ps1`'s "Hyper-V off" change didn't take fully
   effect (BootViewer may lag), MSR reads could still be intercepted.

3. **Intel's errata E013** on Alder Lake / Raptor Lake: certain MTRR
   reads during VMX enter can race with pending IPI handling and
   abort with #GP.

4. **HyperDbg's specific regression (issue 323)**: the `bf6370d`
   commit changed MTRR map build logic in a way that reads MSRs
   without first checking their enable bits via `IA32_MTRRCAP (0xFE)`,
   which can fault on parts where the standard assumption doesn't hold.

The exact root cause of #GP on MSR 0x200 can't be determined from a
minidump alone — would need live debugging. **But matched against
issue 323 symptoms, (4) is the overwhelming likelihood.**

## Our Patches That Got Us This Far

Chronological list of fixes applied before this final crash:

### 1. kdmapper multi-module support
- File: `E:\Reverse_Engineer\tools\kdmapper\kdmapper\main.cpp`
- Change: accept multiple `.sys/.dll` on command line, map in dependency
  order, register each in `g_extra_modules` for cross-module import
  resolution.

### 2. kdmapper EP=0 skip
- File: `kdmapper.cpp` (in `MapDriver`)
- Change: when `AddressOfEntryPoint == 0`, skip CallKernelFunction
  (companion DLLs like hyperlog/hyperhv have EP=0; calling base+0 would
  execute the PE header → crash).

### 3. kdmapper export-RVA threshold
- File: `intel_driver.cpp` (in `GetKernelModuleExport`)
- Change: `if (function_table[function_ordinal] < 0x100)` instead of
  `<= 0x1000`. Allows hyperevade.dll's first export at RVA 0x1000 to
  resolve.

### 4. kdmapper IoCreateDriver path
- Files: `kdmapper.hpp`, `kdmapper.cpp`, `main.cpp`
- Change: for the last module in multi-file load, dispatch DriverEntry
  via `IoCreateDriver("\\Driver\\HyperDbgM", entry)` instead of raw
  CallKernelFunction. Gives hyperkd.sys a valid DriverObject so its
  internal `IoCreateDevice` call succeeds.

### 5. hyperkd.sys randomized device names
- File (bundle): `patch_hyperkd_names.py` → produces patched copy
- Change: in-place rewrite of UTF-16 strings at file offsets 0x19040 /
  0x19080 to use a random 14-char suffix per run. Avoids namespace
  collisions in `\Device\` and `\DosDevices\`.

### 6. hyperkd.sys DO_DEVICE_INITIALIZING clear
- File: patched inline by `patch_hyperkd_names.py`
- Change: at file offset 0x14A08 in hyperkd.sys's DriverEntry, replace
  `OR [rax+0x30], 4; call <log-thunk>` (9 bytes) with
  `OR [rax+0x30], 4; AND BYTE[rax+0x30], 0x7F; NOP` (same 9 bytes).
  This clears bit 7 (DO_DEVICE_INITIALIZING) which `NtLoadDriver`
  normally clears post-DriverEntry but `IoCreateDriver` doesn't.

### 7. libhyperdbg.dll device-name sync
- File: patched inline by `patch_hyperkd_names.py`
- Change: restore libhyperdbg.dll from `.bak_passc` backup, replace
  ASCII suffix at file offset 0x36BE3C+ with current random suffix.

### 8. libhyperdbg.dll `jne → jmp` install bypass
- File: patched inline by `patch_hyperkd_names.py`
- Change: byte at file offset 0x6158E changed from `0x75` (jne short)
  to `0xEB` (jmp short). Makes `load vmm` ignore the SCM install failure
  and proceed to the VMM activation IOCTL path.

## What's Left To Try

(Also captured in `README.md` option list.)

1. **Rebuild HyperDbg with Mattiwatti's `580907e2` patch cherry-picked.**
   Fixes the MTRR regression. All 8 of our patches above still apply.
   Estimated effort: 1-2 hours (clone, build env setup, cherry-pick,
   build, replace release/ binaries).

2. **Downgrade HyperDbg to pre-`bf6370d`.** Older version doesn't have
   the regression. Lose any features added since (`!epthook2` is older
   than this, so unaffected). Patches 1-8 need re-verification against
   the older build.

3. **Pivot to hvpp or HyperPlatform-based custom HV.** Clean start.
   None of our patches carry over, but no manual-map architecture
   assumptions to fight.

4. **Pivot to BYOVD hardware breakpoints.** Different approach entirely.
   DR0 write via vulnerable Intel driver + #DB IDT handler. No hypervisor
   involved, no MTRR concerns.

5. **Shelve for today.** All work preserved. Resume from this document.
