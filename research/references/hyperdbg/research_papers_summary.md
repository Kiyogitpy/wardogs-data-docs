# HyperDbg Research Papers — Local Summary
Fetched: 2026-10-16

## Primary Papers

### 1. HyperDbg: Reinventing Hardware-Assisted Debugging (CCS 2022)

- **arXiv**: https://arxiv.org/abs/2207.05676 (extended version, 2022-05-29)
- **PDF**: https://arxiv.org/pdf/2207.05676
- **Authors**: Karvandi, Gholamrezaei, Monfared, Meghdadizanjani, Abbassi,
  Amini, Mortazavi, Gorgin, Rahmati, Schwarz (TU Graz contribution)
- **Venue**: ACM CCS 2022

**Abstract summary:**

HyperDbg is a hypervisor-assisted debugger designed around three
non-negotiables: transparency, speed, stealthiness. Where WinDbg/GDB run
at ring 0, HyperDbg runs at ring -1 using VT-x + extended page tables.
Key empirical results from the paper:

- **Transparency**: 10,853 malware samples tested; HyperDbg analyzed
  22% more than WinDbg, 26% more than x64dbg. Zero of 13 tested packers
  detected HyperDbg's presence.
- **Performance**: step-in 2.98x faster than WinDbg; conditional-break
  1319x faster; syscall recording 2018x faster. The scripting engine
  runs IN VMX root mode (no context switch to user-mode for every
  action), which drives these numbers.
- **Features demonstrated**: 0-day analysis, structure reconstruction,
  software performance profiling, code-coverage analysis.

**Architecture (from paper's §3):**

Three action types trigger on each event:
1. **Break** — pause all cores (NOT available in VMI/local mode).
2. **Script** — run VMX-root-compatible script to read/modify memory,
   registers, parameters without breaking. HUGE performance edge.
3. **Custom Codes** — run user assembly whenever event fires.

Two operation modes:
1. **VMI mode** — local or remote introspection without pause/step on
   kernel. (This is Pass C's mode.)
2. **Debugger mode** — remote only, over serial, full pause+step.

**Case study highlighted**: analysis of _Pitou_ bootkit (bypasses UAC,
privilege-escalates, infects MBR). Modern Windows still vulnerable per
the paper. HyperDbg's VMX-root transparency let the authors trace Pitou
without the bootkit noticing.

### 2. The Reversing Machine (TRM) — Reconstructing Memory Assumptions (2024)

- **arXiv**: https://arxiv.org/abs/2405.00298 (2024-05-01)
- **PDF**: https://arxiv.org/pdf/2405.00298
- **Author**: Monfared, Saleh Khalaj (same TU Graz group)
- **Venue**: Submitted CCS 2025

**One-liner**: Uses HyperDbg's primitives (EPT hooks, VMX-root scripting)
to extract COMPLETE memory traces in both user and kernel space, then
reconstructs OS structures and detects rootkits.

**Key empirical result**: TRM speeds up manual reverse engineering of
kernel structures by 75% on average vs purely manual IDA/Ghidra work.

**Why it matters for Pass C**: TRM is the proof-of-concept that HyperDbg's
EPT hook + script engine combo is viable for OUR exact use case —
dumping memory state on each call to a monitored function. Pass C's
`capture.hds` is basically a mini-TRM for ChaCha20 state.

## Secondary Paper (Design Doc)

### Kernel Debugger Design in HyperDbg (1st Edition, July 2022)

- **URL**: https://research.hyperdbg.org/debugger/kernel-debugger-design/
- **PDF**: https://research.hyperdbg.org/assets/documents/kernel-debugger-design-1st-edition.pdf

Internal design doc, more implementation-focused than the arXiv paper.

**Key section: NMI Controller Bits in VMX**

HyperDbg uses NMIs (Non-Maskable Interrupts) extensively for multi-core
coordination. Three control bits matter:

1. **NMI-Exiting (Pin-Based VM-Execution Controls)**
   - If = 0: NMI arrives in VMX non-root → delivered to guest via guest's
     IDT.
   - If = 1: NMI causes VM-exit → VMM handles it. HyperDbg sets this to
     1 so it can halt all cores from any single core by self-NMI'ing.

2. **Virtual NMIs** — controls whether vNMI delivery is tracked.
3. **NMI-Window-Exiting** — causes VM-exit when guest is ready to receive
   an NMI (used for timing-critical delivery).

**How HyperDbg uses NMIs:**

When the user hits Ctrl+C in VMI mode:
- CLI sends IOCTL to driver.
- Driver issues `KeIpiGenericCall(SelfNmi)` → each core NMI's itself.
- Each core's NMI handler VM-exits (because NMI-Exiting=1).
- VMM takes control on every core simultaneously.
- VMM polls for new commands while all cores halted.
- Resume via `VMRESUME` on each core.

This is the "halt all cores" primitive. Even in VMI mode, HyperDbg can
pause ALL guest activity instantly without using Windows's own IPI
mechanisms (which could be hooked by malware).

**Relevance to Pass C**:

Our `capture.hds` doesn't halt cores — EPT hooks fire asynchronously
per core. The NMI machinery is more relevant if we extended to breaking
into HyperDbg's CLI after capture (not needed for a one-shot ChaCha20
state dump).

## Research Group's Broader Agenda

TU Graz / HyperDbg team's research line (from the paper references):
- Hypervisor-based debuggers (HyperDbg)
- Memory-trace-based malware detection (TRM)
- Hardware-assisted information flow analysis
- Transparent debugging benchmarks

They explicitly contrast against:
- WinDbg (ring 0, detectable by any ring 0 malware)
- x64dbg (user-mode, trivially detectable)
- IDA Pro (dynamic debugging is user-mode)
- Hidden ptrace-style approaches (Linux only, still ring 0)

The pitch of HyperDbg's whole research line: **"If malware runs at ring 0,
your debugger must run at ring -1 to see it fairly."**

## Reading Order for Future Deep-Dive

1. `research_paper_summary.md` (this file) — orientation
2. `kernel-debugger-design-1st-edition.pdf` (local copy TBD) — internals
3. CCS'22 paper (full) — formal evaluation + benchmarks
4. HyperDbg source `hyperhv/` directory — actual VMX setup code
5. HyperDbg source `hyperdbg-cli/` — command parser + IOCTL layer
6. HyperDbg source `libhyperdbg/` — user-mode library (what Pass C
   patched)
