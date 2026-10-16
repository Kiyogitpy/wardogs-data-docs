# HyperDbg Local Reference Archive — Pass C Research
Collected: 2026-10-16  (Wardogs/Elytra bypass attempt)
Target: HyperDbg v0.24.0 (build 20260922.1644)
Platform: Windows 10 22H2 Build 19041, Intel Alder Lake family 6 model 0xA7

## WHY THIS ARCHIVE EXISTS

Pass C of the Wardogs ChaCha20 extraction project tried to use HyperDbg
as a type-1 hypervisor to install EPT execute hooks on runtime.dll's
AVX-512 ChaCha20 variants. The approach went through five layers of
unexpected failure before hitting a known upstream bug (see issue 323).

This folder caches the HyperDbg docs + source references + issue tracker
findings so we don't re-fetch them if we return to this work.

## TABLE OF CONTENTS

| File | What it contains |
|---|---|
| `docs_index.md` | Full docs llms.txt tree (every HyperDbg doc URL) |
| `operation_modes.md` | VMI vs Debugger vs Transparent mode primer |
| `load_command.md` | `load vmm/kd/trace/all` command reference |
| `local_debugging.md` | `.connect local` + `load vmm` canonical flow |
| `build_install.md` | DSE/VBS/testsigning requirements |
| `faq_processor_support.md` | Known processor limits + VT-x requirements |
| `vt_x_concepts.md` | VMM/VMCS/VMX terminology |
| `unsafe_behavior.md` | VMX-root constraints (what you can't do inside a vmexit) |
| `connection_internals.md` | How CLI talks to driver (serial for KD, IOCTL for VMI) |
| `issue_323_mtrr_breakage.md` | **KEY**: known `load vmm` crash root cause |
| `our_crash_analysis.md` | Our specific crash + mapping bases + bugcheck decode |
| `kdmapper_path_findings.md` | What our 5-layer manual-map journey discovered |

## KEY TAKEAWAYS

1. **HyperDbg is architected for SCM-based driver loads.** Manual-map via
   kdmapper is NOT a supported configuration. Every assumption Windows
   normally handles for SCM-loaded drivers (DO_DEVICE_INITIALIZING flag
   clear, CR4.VMXE setup via IPI, hybrid-core MSR handling) has to be
   patched into either our side (kdmapper) or theirs (hyperkd.sys bin).

2. **Known upstream bug (issue 323) on modern Intel (12th+ gen).**
   Commit `bf6370d5` changed EPT MTRR handling in a way that breaks on
   hybrid CPUs. Mattiwatti's fork has fix commit `580907e2` that resolves
   it. HyperDbg maintainer SinaKarvandi confirmed the MTRR regression but
   hasn't merged the fix.

3. **VMI mode (what we want) requires:**
   - Intel VT-x enabled in BIOS
   - DSE disabled (testsigning OR trust-stored cert OR kdmapper manual-map)
   - VBS/HVCI off (otherwise Hyper-V owns VT-x)
   - `.connect local` opens device, `load vmm` activates VMX

4. **Expected successful `load vmm` output (per docs):**
   ```
   HyperDbg> load vmm
   loading the vmm driver
   current processor vendor is : GenuineIntel
   virtualization technology is vt-x
   vmx operation is supported by your processor
   vmm module is running...
   ```

5. **Our crash matched issue 323's symptoms** — unresponsive/BSOD after
   `load vmm` on 12th+ gen Intel. The root cause is upstream, not our
   patching.

## PATHS FORWARD (recorded for next attempt)

Option A — Fork HyperDbg at bf6370d^ (pre-regression), rebuild:
   `git clone --recursive https://github.com/HyperDbg/HyperDbg.git`
   `git checkout bf6370d5a3d35bb7aeb16ce0d45fd77fda7bcca0^`
   Build with latest VS2026 + WDK, use the resulting hyperkd.sys through
   our kdmapper chain. Still needs manual-map patches but skips MTRR bug.

Option B — Use Mattiwatti's fix: pull PR branch, cherry-pick 580907e2,
   rebuild against v0.24 base.

Option C — Pivot to hvpp (single-sys, manual-map friendly) — reset
   expectations, start fresh.

Option D — Pivot entirely away from hypervisor-based capture.
   BYOVD hardware breakpoints via Intel iqvw64e primitives: write DR0,
   install #DB IDT handler, capture in handler. No HV, no VMLAUNCH, no
   MTRR concerns. Trade-off: hardware BPs are classically detectable,
   but Elytra's known tripwires (testsigning, kdnet) don't include DR
   register sweeps.
