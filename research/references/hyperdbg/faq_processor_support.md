# FAQ — Processor Support
Source: https://docs.hyperdbg.org/getting-started/faq
Fetched: 2026-10-16

## Intel-Only (as of v0.24)

> The current version of HyperDbg only supports Intel x64 processors.
> You cannot run it on an AMD processor or an ARM processor. This is
> mainly because HyperDbg heavily uses VT-x which is an Intel-based
> technology, but future versions will support other processors as well.

Future AMD-SVM support is planned per the roadmap but not available in
v0.24.

## Processor Generation Requirements

> Your processor should at least support Intel Extended Page Table
> (A.K.A. EPT), which is introduced on Nehalem Microarchitecture, but
> most of the functionalities are working on Intel's 4th or later
> generation; so, the previous processors might have undefined behaviors
> with some of the functionalities of HyperDbg.
>
> Even though most of the functionalities are supported on the 4th
> generation of Intel Processors but still some minor functionalities
> need newer processors. **It's recommended to use a Skylake (6th
> generation) processor or newer processors to support all
> functionalities.**

## Hybrid CPU (12th gen Alder Lake / 13th gen Raptor Lake / later)

**NOT MENTIONED IN FAQ. This is where issue 323 lives.**

Modern Intel hybrid CPUs have asymmetric cores:
- **P-cores (Performance)** — full VT-x + MSR support, like older Intel
- **E-cores (Efficient)** — reduced instruction set, some MSRs raise #GP

HyperDbg's VMM init uses `KeIpiGenericCall` to dispatch VmxOn to all
cores simultaneously. If an E-core gets the init first and tries to read
a P-core-only MSR (via `RDMSR`), it faults.

**Pass C crash matched this signature exactly:**
- Crash: hyperhv.dll + 0x1B00 (`RDMSR` wrapper)
- Caller passed `ECX = 0x200` (`IA32_MTRR_PHYSBASE0`)
- Faulting CPU: Alder Lake (family 6 model 0xA7)
- Bugcheck: STOP 0x1E with STATUS_PRIVILEGED_INSTRUCTION

Even though `IA32_MTRR_PHYSBASE0` IS defined on E-cores per Intel SDM
Vol 4, actual hardware behavior on hybrid parts has well-documented
inconsistencies — specifically around MTRR fixed-range regions and when
MTRR state is initialized per-core.

## OS Support

> No, the current version is only limited to Windows; however, one of
> our top priorities is to port HyperDbg on Linux

Windows-only in v0.24. Our target (Wardogs on Windows 10) is natively
supported.

## Known System Instability Vectors

(From our research + issue tracker, not FAQ)

1. **Kernel structure modification via custom scripts** — explicit docs
   warning.
2. **VMX root mode "unsafe" API usage** — see unsafe_behavior.md.
3. **MTRR regression on 12th+ gen Intel** — issue 323.
4. **Nested virtualization conflicts** — don't run inside VMware/Hyper-V
   guest without matching nested-virt config.
