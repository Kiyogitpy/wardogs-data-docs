# Build & Install (DSE/VBS/testsigning requirements)
Source: https://docs.hyperdbg.org/getting-started/build-and-install
Fetched: 2026-10-16

## Software requirements for BUILDING

- Visual Studio Community/Enterprise/Professional 2026
- Windows SDK (latest)
- Windows Driver Kit (latest)
- Build may break with older SDK/WDK — upgrade before building.

Clone with `--recursive`:
```
git clone --recursive https://github.com/HyperDbg/HyperDbg.git
```

## Pre-run Requirements

Three independent gates must open before `load vmm` succeeds:

### 1. Intel VT-x enabled in BIOS

Vendor-specific (F2 / Delete / ESC during boot). Look for
"Virtualization" / "VT-x" / "Intel VT" in BIOS Security or Advanced tabs.

If disabled, HyperDbg prints "vmx is not supported" during
`load vmm`.

### 2. Driver Signature Enforcement DISABLED

Four documented options (choose one):

#### Option A — Attach WinDbg at boot (RECOMMENDED by HyperDbg docs)
Uses kdnet.exe from Windows SDK. WinDbg disables both DSE AND
PatchGuard. All PatchGuard-detectable HyperDbg features
(`!syscall`, `!sysret`) remain usable.

**ELYTRA TRIPWIRE**: Our bench memory notes that kdnet is flagged
by Elytra. Not usable for Pass C.

#### Option B — Advanced Startup F7 ("Temporarily Disable DSE")
Hold Shift + Restart → Troubleshoot → Advanced options → Startup
Settings → Restart → F7.

- Only lasts until next reboot.
- PatchGuard remains ACTIVE, so some HyperDbg features break.
- No boot-level flag like testsigning (which Elytra tripwires).

#### Option C — testsigning on
```
bcdedit /set testsigning on
```
**ELYTRA TRIPWIRE**: user intel confirmed Elytra fingerprints this
BCD flag. Not usable for Pass C.

#### Option D — EfiGuard (3rd-party)
Bootkit that disables DSE + PatchGuard without WinDbg attach.
Unknown Elytra detection status (haven't checked).

### 3. VBS/HVCI/Device Guard OFF

HyperDbg and VBS are BOTH ring -1 hypervisors — they conflict.

```powershell
# bcdedit way
bcdedit /set hypervisorlaunchtype off

# Registry way (what our prep_hyperdbg.ps1 does)
HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard:
  EnableVirtualizationBasedSecurity = 0 (DWORD)
  RequirePlatformSecurityFeatures   = 0 (DWORD)
HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity:
  Enabled = 0 (DWORD)
  Locked  = 0 (DWORD)
```

Also disable Windows features:
- Virtual Machine Platform
- Windows Hypervisor Platform
- Hyper-V (if enabled)
- Windows Subsystem for Linux (WSL1 is fine, WSL2 isn't)

### 4. (optional for Device Guard systems) Disable System Guard

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\SystemGuard
  Enabled = 0 (DWORD)
```

Convenience .reg file:
https://github.com/HyperDbg/starting-hyperdbg-scripts/blob/main/device-guard/disable-system-guard.reg

Reversal .reg file:
https://github.com/HyperDbg/starting-hyperdbg-scripts/blob/main/device-guard/enable-system-guard.reg

## What Our prep_hyperdbg.ps1 Does

Matches docs steps 3 + bcdedit from step 3, intentionally SKIPS step 2
(testsigning per Elytra constraint). This leaves DSE enabled, which is
why we needed the kdmapper manual-map chain.

## Pass C Compromise Table

| Requirement | Normal approach | Pass C approach (Elytra constraint) |
|---|---|---|
| VT-x | BIOS flag | Same (unchanged) |
| DSE off | testsigning / kdnet | kdmapper manual-map via iqvw64e BYOVD |
| VBS off | prep_hyperdbg.ps1 | Same |
| Hyper-V off | prep_hyperdbg.ps1 | Same |
