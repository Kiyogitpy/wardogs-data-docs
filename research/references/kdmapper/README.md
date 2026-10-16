# kdmapper — Local Reference
Source: https://github.com/TheCruZ/kdmapper  (3,153 stars)
Fetched: 2026-10-16

## What It Is

> KDMapper is a simple tool that exploits iqvw64e.sys Intel driver to
> manually map non-signed drivers in memory

**Author**: TheCruZ (141 commits; same author as BootViewer)
**License**: MIT
**Language**: C++
**Tested range**: Windows 10 1607 through Windows 11 25H2 build 26200.8875

## How It Works (High-Level)

1. Drops embedded `iqvw64e.sys` (Intel Ethernet diagnostics, signed by
   Intel in 2013, CVE-2015-2291 vulnerable).
2. Loads it via `NtLoadDriver` (not SCM `StartService` — leaves fewer
   traces).
3. Uses CVE-2015-2291's `memmove` primitive via IOCTL `0x80862007`
   subcode `0x33` to get arbitrary kernel R/W.
4. Allocates kernel pool for the target driver via indirect NtAllocVM
   or direct ExAllocatePool calls.
5. Copies the target driver into pool, resolves imports, applies
   relocations, fixes stack cookies.
6. Executes the target driver's `DriverEntry` via hijacked
   `NtAddAtom` syscall (chosen because NtAddAtom is universally
   available but rarely called by legit code).
7. Unloads `iqvw64e.sys` via `NtUnloadDriver`.
8. Scrubs forensic artifacts (see "Features" below).

## Features (verbatim from README)

- Works with /GS- compiled drivers (no stack-cookie dependency)
- Hooks **NtAddAtom** which exists everywhere and is rarely called
- Clears **MmUnloadedDrivers**
- Clears **PiDDBCacheTable**
- Clears **g_KernelHashBucketList**
- Clears **WdFilter RuntimeDriverList / RuntimeDriverCount / RuntimeDriverArry**
  (Windows Defender's loaded-driver list)
- Uses `NtLoadDriver` / `NtUnloadDriver` for less traces (vs SCM)
- Prevents load if `\Device\Nal` exists (prevents BSOD from double-mapping)
- Header section skipped while copying driver to kernel (saves ~0x1000
  bytes per driver, makes artifact harder to recover from a dump)
- Modifiable params before driver entry call
- Optional PDB-offset-based build via `SymbolsFromPDB` project — adapts
  to new Windows updates by parsing target ntoskrnl.pdb

## Parameters

```
kdmapper <path-to-sys> [options]

--copy-header               Keep driver header in mapped image (we need
                              this for multi-module loads so later maps
                              can resolve imports from earlier siblings).
--free                      Auto-unmap allocated memory after driver
                              entry returns.
--indPages                  Map in independent allocated pages (instead
                              of one contiguous pool allocation).
--PassAllocationPtr         Pass the allocation ptr as first param to
                              DriverEntry.

[PDB offset build only:]
--offsetsPath "<path>"      Use custom offsets.ini (default ./offsets.ini).
--dontUpdateOffsets         Skip offset refresh (risky if Windows updated).
```

## Pass C Patches (what we modified)

Our custom build is in `E:\Reverse_Engineer\tools\kdmapper\`. Diff from
upstream `master`:

### 1. Multi-module command line (`main.cpp`)
- Accept multiple positional `.sys/.dll` args as `driver_paths` vector.
- Auto-force `--copy-header` when `size() >= 2` so companion DLLs retain
  their export tables for sibling resolution.
- Loop through drivers in dependency order (user supplies order).

### 2. Cross-module sibling resolver (`kdmapper.cpp`)
- Added `std::unordered_map<std::string, ULONG64> g_extra_modules`
  (basename → mapped kernel VA).
- Register each mapped module post-success.
- In `ResolveImports`, after `GetKernelModuleAddress()` returns 0,
  consult `g_extra_modules` before giving up.

### 3. Entry-point zero skip (`kdmapper.cpp`)
- When `nt_headers->OptionalHeader.AddressOfEntryPoint == 0`, skip
  the DriverEntry call entirely and return the mapped base. Companion
  DLLs (hyperlog.dll, hyperhv.dll, hyperevade.dll, etc.) all have
  EP=0 — calling base+0 executes the PE header, BSOD.

### 4. Export-RVA threshold (`intel_driver.cpp`)
- Original: `if (function_table[ordinal] <= 0x1000) return 0;`
- Patched: `if (function_table[ordinal] < 0x100) return 0;`
- hyperevade.dll's first export sits at RVA exactly 0x1000, hitting
  the original guard.

### 5. IoCreateDriver dispatch path (`kdmapper.cpp` + `include/kdmapper.hpp`)
- Added `bool g_use_io_create_driver` global.
- When set, resolve `IoCreateDriver` via
  `intel_driver::GetKernelModuleExport(ntoskrnlAddr, "IoCreateDriver")`.
- Allocate single pool chunk containing `UNICODE_STRING` header + 
  wide-char buffer `L"\\Driver\\HyperDbgM"`.
- Call `IoCreateDriver(&unistr, DriverEntry)` instead of raw
  `CallKernelFunction(entry, 0, 0)`.
- In `main.cpp`: enable only for `size() > 1 && idx + 1 == size()`
  (last module in multi-file load).

### 6. ASCII sanitization (all .cpp + .hpp)
- Original source contained U+2014/2013/2192/2190 (em-dash, en-dash,
  arrows) in log strings. `std::wcout` sets failbit on these when
  active code page is standard, SILENTLY dropping ALL subsequent log
  output — made debugging the above fixes very hard.
- Replaced all with ASCII equivalents.

## Resulting Binary

- Path: `E:\Reverse_Engineer\tools\kdmapper\kdmapper.exe`
- Size: 158,208 bytes (vs upstream's ~150 KB)
- Hash: shifts per build (expected for a BYOVD tool, resists signature
  bans)

## Pass C Usage

```bat
kdmapper.exe ^
  hyperevade.dll ^
  hyperlog.dll ^
  kdserial.dll ^
  hypertrace.dll ^
  hyperhv.dll ^
  hyperkd_patched_<suffix>.sys
```

Order is dependency topological:
1. hyperevade (no imports) — leaf
2. hyperlog (ntoskrnl only) — leaf
3. kdserial (ntoskrnl + HAL) — leaf
4. hypertrace (ntoskrnl only) — leaf
5. hyperhv (ntoskrnl + HAL + hyperevade) — needs #1
6. hyperkd.sys (ntoskrnl + hyperlog + hyperhv + kdserial + hypertrace)
    — needs #2 #3 #4 #5

## Related Loaders (Alternative Options)

If TheCruZ/kdmapper gets detected or we need variety:

| Loader | Vulnerable driver | Notes |
|---|---|---|
| **kdmapper** (TheCruZ) | iqvw64e.sys (CVE-2015-2291) | What we use |
| **drvmap** (not51) | iqvw64e.sys (same) | Older, simpler |
| **PsKDbgCtrl** | gdrv.sys (Gigabyte CVE-2018-19320) | Different driver family |
| **manual-mapper-rust** | varies | Rust implementation |
| **capcom-rookit-loader** | Capcom.sys (CVE-2016-7246) | Classic, well-signatured |

All share the BYOVD pattern. iqvw64e has the longest unrevoked validity
(signed 2013, still trusted in 2026). The LOLDrivers project
(https://www.loldrivers.io/) tracks all known BYOVD-abusable drivers.

## Detection Vectors (what defenders look for)

1. **File presence**: Sysmon Event ID 6 (driver loaded) with
   `iqvw64e.sys` is a huge BYOVD smoking gun.
2. **Device object `\Device\Nal`**: kdmapper's own guard, defenders scan
   for it too.
3. **PiDDBCacheTable fingerprint**: pre-cleanup state visible to
   kernel-mode AV.
4. **Hash blocklist**: HVCI blocks iqvw64e by hash on modern Windows.
5. **ETW `Microsoft-Windows-Kernel-General` driver-load events**.
6. **MmUnloadedDrivers scan**: if cleaning is incomplete, residue shows.

Pass C's constraint: Elytra doesn't block kdmapper usage per se (user
intel), but DOES have a kernel DLL-load filter on WardogsClient itself
(blocks LoadLibrary from unexpected modules into the game process).
That's a USER-mode detection, orthogonal to kdmapper's kernel detection
surface.
