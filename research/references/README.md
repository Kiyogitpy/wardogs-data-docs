# Pass C Tooling — Index

All tool references used in the Wardogs/Elytra Pass C attempt.

## Tool Inventory

| Tool | Purpose | Vendor | Local docs |
|---|---|---|---|
| **HyperDbg v0.24** | Hypervisor-based debugger (EPT hooks) | HyperDbg team (TU Graz adjacent) | `hyperdbg/` |
| **kdmapper** | BYOVD manual-map loader | TheCruZ | `kdmapper/` |
| **iqvw64e.sys** | Vulnerable Intel driver (exploit primitive) | Intel (2013) | `byovd/` |
| **BootViewer / logdump** | Measured-boot verifier | TheCruZ | `bootviewer/` |
| **cdb.exe** | Windows kernel debugger (minidump analysis) | Microsoft (Windows Debuggers) | n/a (standard) |
| **CUE4Parse** | Unreal Engine pak reader | FModel team | (used in Pass A) |

## Vendor Clusters

Observation worth noting: **TheCruZ** authored both kdmapper AND
BootViewer. The security-tool and attestation-audit tools in Pass C's
chain come from the same author.

TheCruZ's GitHub has one more tool worth knowing about:
`mouse-input-detection` — not needed for Pass C but relevant to anticheat
research generally.

## Dependency Graph (what calls what)

```
RUNBOOK.md (Pass C orchestration)
  │
  ├─► prep_hyperdbg.ps1
  │     └─► bcdedit / registry edits
  │
  ├─► BootViewer\logdump.exe        (verify prep)
  │
  ├─► probe_hv.py                   (CPUID.1:ECX[31] check)
  │
  ├─► load_hyperdbg_full.bat
  │     ├─► patch_hyperkd_names.py  (3 binary patches)
  │     │     ├─► reads hyperkd.sys
  │     │     ├─► randomizes device name
  │     │     ├─► clears DO_DEVICE_INITIALIZING
  │     │     └─► syncs libhyperdbg.dll
  │     │
  │     └─► kdmapper.exe (patched)
  │           ├─► embedded iqvw64e.sys
  │           ├─► NtLoadDriver iqvw64e
  │           ├─► ioctl 0x80862007 memmove primitive
  │           ├─► maps 6 modules in order:
  │           │     hyperevade.dll
  │           │     hyperlog.dll
  │           │     kdserial.dll
  │           │     hypertrace.dll
  │           │     hyperhv.dll
  │           │     hyperkd_patched_<random>.sys
  │           └─► NtUnloadDriver iqvw64e
  │
  ├─► hyperdbg-cli.exe
  │     ├─► libhyperdbg.dll (patched)
  │     │     ├─► .connect local
  │     │     └─► load vmm             ← dies here on 12th+ gen Intel
  │     │                                 (issue 323 MTRR regression)
  │     └─► IOCTL to \\.\HyperDbg<random>
  │
  └─► capture.hds  (if load vmm ever succeeded)
        ├─► !epthook2 hyperhv API
        ├─► printf + poi() per hit
        └─► output parsed by parse_capture.py
```

## File Layout

```
E:\Reverse_Engineer\references\
  README.md                              (this file)
  
  hyperdbg\
    README.md                            (top-level HyperDbg overview)
    docs_index.md                        (full docs tree)
    operation_modes.md                   (VMI vs Debugger vs Transparent)
    load_command.md                      (load vmm/kd/trace reference)
    local_debugging.md                   (.connect local flow)
    build_install.md                     (DSE/VBS requirements)
    faq_processor_support.md             (Intel-only; hybrid CPU note)
    vt_x_concepts.md                     (VMM/VMCS/VMX terminology)
    unsafe_behavior.md                   (VMX-root scripting constraints)
    connection_internals.md              (VMI IOCTL vs serial)
    issue_323_mtrr_breakage.md          **the actual Pass C root cause**
    our_crash_analysis.md                (minidump decode)
    kdmapper_path_findings.md            (all 8 patches explained)
    research_papers_summary.md          (CCS'22 + TRM + 1st-ed design)
  
  kdmapper\
    README.md                            (tool overview + Pass C patches)
  
  byovd\
    iqvw64e_cve_2015_2291.md             (vulnerability + exploit primitive)
  
  bootviewer\
    README.md                            (measured-boot verifier)
```

## Shortcut Links to Critical Reads

If someone picks this up fresh, read in this order:
1. `hyperdbg/README.md` — big picture
2. `hyperdbg/issue_323_mtrr_breakage.md` — why Pass C stopped
3. `hyperdbg/kdmapper_path_findings.md` — resume protocol
4. `hyperdbg/our_crash_analysis.md` — exact crash decode

Then as needed:
5. `kdmapper/README.md` — if touching the loader
6. `byovd/iqvw64e_cve_2015_2291.md` — if the Intel driver gets blocked
7. `bootviewer/README.md` — if attestation checks matter
