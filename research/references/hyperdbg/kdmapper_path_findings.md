# kdmapper + HyperDbg Manual-Map Path Findings
Session: 2026-10-16  (Pass C, Wardogs/Elytra project)

## Why Manual-Map (not SCM install)

Elytra tripwires we're forced to work around:
- `bcdedit /set testsigning on` — flagged (user intel)
- KDNET at boot — flagged (user bench memory)
- Secure Boot off at BIOS — not tested but likely flagged

These rule out ALL conventional HyperDbg install paths per
their docs:
1. ❌ WinDbg attach (kdnet) — flagged
2. ❌ Temporary F7 DSE disable — survives one boot, hyperkd.sys needs
   test-cert trust which has similar flagging risk
3. ❌ `testsigning on` — flagged
4. ❌ EfiGuard — bootkit, extremely risky

Remaining: **manual-map via BYOVD** (kdmapper + iqvw64e). No boot flags,
no SCM entries, no persistent cert store additions.

## HyperDbg's Kernel-Side Dependency Graph

v0.24 ships hyperkd.sys with FIVE companion kernel-mode DLLs:

```
hyperkd.sys  (entry: DriverEntry @ RVA 0x15510)
  ├─ hyperlog.dll     (imports: ntoskrnl only;         entry = 0)
  ├─ hyperhv.dll      (imports: ntoskrnl + HAL + hyperevade; entry = 0)
  │     └─ hyperevade.dll  (imports: NONE — pure export stub; entry = 0)
  ├─ kdserial.dll     (imports: ntoskrnl + HAL;        entry = 0)
  └─ hypertrace.dll   (imports: ntoskrnl;              entry = 0)
```

Only hyperkd.sys has a real DriverEntry. The companions are pure
export-table modules — they expose functions but don't initialize
themselves on load.

**Mapping order (dependencies first):**
1. hyperevade.dll
2. hyperlog.dll
3. kdserial.dll
4. hypertrace.dll
5. hyperhv.dll (depends on hyperevade — our resolver handles)
6. hyperkd.sys (depends on hyperlog + hyperhv + kdserial + hypertrace)

## kdmapper Patches Needed

### Multi-module command line
Original kdmapper only accepts one `.sys` on command line. We added
loop support in `main.cpp`.

### Cross-module import resolution
When mapping hyperhv.dll, its imports from hyperevade.dll must resolve
to the already-mapped hyperevade.dll's exports. Added
`g_extra_modules` map (basename → kernel VA) + fallback in
`ResolveImports` after `GetKernelModuleAddress` returns 0.

### Forced copy-header for multi-file
`destroyHeader=false` is needed so later modules can read earlier
modules' export tables. kdmapper's default destroys headers to save
~0x1000 bytes per module — we force it off for multi-file loads.

### Entry-point zero skip
Companion DLLs have `AddressOfEntryPoint = 0`. Default kdmapper would
call base+0 which is the DOS header → random code → BSOD. Added
explicit skip when EP=0.

### Export RVA threshold lowered
`GetKernelModuleExport` had a defensive check:
`if (function_table[ordinal] <= 0x1000) return 0;` (treated as
"invalid"). hyperevade.dll's first export sits at RVA exactly 0x1000.
Changed threshold to `< 0x100` which excludes only header-region
RVAs.

### IoCreateDriver path
Default kdmapper calls `CallKernelFunction(entry, 0, 0)` — passes NULL
DriverObject. HyperDbg's hyperkd.sys expects a valid DriverObject
because its `DriverEntry` calls `IoCreateDevice` early. Added global
`g_use_io_create_driver` flag; when set, invoke
`IoCreateDriver(unistr, entry)` so Windows fabricates a proper
DriverObject for us. Only enabled for the last module in multi-file
loads (hyperkd.sys).

## hyperkd.sys Binary Patches Needed

### Device name randomization
hyperkd.sys hardcodes `\Device\HyperDbgDebuggerDevice` and
`\DosDevices\HyperDbgDebuggerDevice` at file offsets 0x19040 and 0x19080.
When re-running kdmapper after a prior failed load left orphans in
`\Device\`, the new DriverEntry hits STATUS_OBJECT_NAME_COLLISION.
Patcher rewrites the trailing `DebuggerDevice` substring in both strings
to a random 14-char token per run.

### DO_DEVICE_INITIALIZING clear
hyperkd.sys's DriverEntry sets `DO_BUFFERED_IO` (bit 2) via
`OR [DeviceObject->Flags], 4` at file offset 0x14A08. It never clears
`DO_DEVICE_INITIALIZING` (bit 7) — Windows normally does this
automatically after `NtLoadDriver` returns, but `IoCreateDriver` doesn't.
Without it, every `CreateFile` on the device returns
STATUS_DEVICE_DOES_NOT_EXIST (`ERROR_DEV_NOT_EXIST` 0x1B1).

Patcher replaces 9 bytes (`OR + CALL thunk`) with
`OR + AND BYTE[flags], 0x7F + NOP` (9 bytes exactly). Sacrifices the
jump-thunk call to what's probably a logging import.

## libhyperdbg.dll Binary Patches Needed

### Device name sync
libhyperdbg.dll hardcodes `\\.\HyperDbgDebuggerDevice` as ASCII at file
offset 0x36BE34. Patcher restores from `.bak_passc` backup each run,
then overwrites the 14-char `DebuggerDevice` suffix with the current
random token. Keeps the CLI's `CreateFile` calls aligned with
hyperkd.sys's dynamic device name.

### SCM install bypass
`load vmm` command handler calls `DebuggerInstallDriver` (SCM-based
`CreateService` + `StartService`). This fails DSE because hyperkd.sys's
test-cert signature isn't trusted. After the install call, the code
checks `test al,al; jne .success` at file offset 0x6158C-E.
Patcher changes byte at 0x6158E from `0x75` (jne) to `0xEB` (unconditional
jmp). Install failure becomes irrelevant — control flow proceeds to the
VMM activation IOCTL path.

## What Our 8-Patch Chain Produced

After reboot + prep_hyperdbg.ps1 + load_hyperdbg_full.bat succeeded:

```
HyperDbg> .connect local
local debugging (vmi-mode)

HyperDbg> load vmm
loading the vmm module
err, failed loading driver              ← normal SCM failure, bypassed
...                                      
virtualization technology is vt-x       ← we reached this via jne→jmp
vmx operation is supported by your processor
err, CreateFile failed (1b1)            ← before DO_DEVICE_INITIALIZING fix
                                          OR
                                        → BSOD (after that fix, hitting
                                          issue 323 MTRR regression)
```

## Residual Blockers

1. **Issue 323 MTRR regression** — unfixable in binary patching.
   Requires HyperDbg source rebuild with `580907e2` cherry-picked.

2. **Hybrid CPU IPI dispatch** — HyperDbg's assumptions about per-core
   state at `KeIpiGenericCall` time don't hold on Alder/Raptor Lake.
   Fix is in the same `580907e2` patch range.

3. **E-core MSR quirks** — some MSRs that work on P-cores raise #GP
   on E-cores. Hardest to fix in binary; the proper fix is per-core
   feature detection, which HyperDbg does per-core but the detection
   itself can fail during cold init.

## Files to Preserve

```
E:\Reverse_Engineer\tools\kdmapper\
  kdmapper.exe                           (patched build, hash-shifted)
  kdmapper\main.cpp                      (modified, see 'Pass C' comments)
  kdmapper\kdmapper.cpp                  (modified)
  kdmapper\intel_driver.cpp              (modified)
  kdmapper\include\kdmapper.hpp          (modified)

E:\Reverse_Engineer\tools\HyperDbg-v0.24\release\
  libhyperdbg.dll                        (patched - device name + jne→jmp)
  libhyperdbg.dll.bak_passc              (unmodified backup)
  hyperkd.sys                            (original - patcher re-reads
                                            per-run so patches are
                                            applied to a temp copy)

E:\Reverse_Engineer\wardogs_analysis\pass_c\hyperdbg\
  patch_hyperkd_names.py                 (THE patcher - all 3 patches)
  load_hyperdbg_full.bat                 (6-module kdmapper invocation)
  prep_hyperdbg.ps1                      (Hyper-V/VBS off, no testsigning)
  undo_prep.ps1                          (restore companion)
  probe_hv.py                            (CPUID-based HV presence check)
  probe_paths.py                         (device path open probe)
  probe_multiopen.py                     (second-handle test)
  objns_scan.py                          (NT namespace enumeration)
  capture.hds                            (EPT hook script for 3 RVAs)
  teardown.hds                           (hook removal)
  parse_capture.py                       (log → CSV, Pass B shape)
  test_parse.py                          (parser validation, SYNTH test)
  RUNBOOK.md                             (walk-through doc)
```

## Resume Protocol

If/when revisiting Pass C with a fixed HyperDbg build:

1. `cd E:\Reverse_Engineer\tools`
2. `git clone --recursive https://github.com/HyperDbg/HyperDbg.git hyperdbg-src`
3. `cd hyperdbg-src && git checkout v0.24`
4. `git remote add mattiwatti https://github.com/Mattiwatti/HyperDbg.git`
5. `git fetch mattiwatti`
6. `git cherry-pick 580907e2790e4ed6ce2275721c4b782f68df3711`
7. Build in VS2026 → Release|x64
8. Copy `bin\release\hyperkd.sys`, `hyperhv.dll`, `hyperlog.dll`,
   `hyperevade.dll`, `kdserial.dll`, `hypertrace.dll`,
   `libhyperdbg.dll`, `hyperdbg-cli.exe` into
   `E:\Reverse_Engineer\tools\HyperDbg-v0.24-patched\release\`
9. Update `load_hyperdbg_full.bat` to point at the new path
10. Make a `.bak_passc` of the new `libhyperdbg.dll`
11. Reboot (post prep_hyperdbg.ps1 if not already done)
12. Verify no HV (probe_hv.py)
13. Run `load_hyperdbg_full.bat *>&1 | Tee-Object kdmap_run.log`
14. Launch hyperdbg-cli, `.connect local`, `load vmm`
15. Expected: "vmm module is running..."
16. From another elevated PS: probe_hv.py should show HyperDbg vendor
17. Launch Wardogs via Steam, main menu
18. Checkpoint B: probe_hv.py AGAIN, confirm no vendor change
19. `.script capture.hds` in HyperDbg CLI
20. Play → log fills with HIT lines
21. Teardown + parse_capture.py → CSV
