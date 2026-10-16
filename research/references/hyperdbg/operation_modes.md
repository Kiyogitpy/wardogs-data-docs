# HyperDbg Operation Modes
Source: https://docs.hyperdbg.org/using-hyperdbg/prerequisites/operation-modes
Fetched: 2026-10-16

HyperDbg operates in **three** different modes:

## 1. VMI Mode (Virtual Machine Introspection) — DEFAULT

**This is what Pass C uses.** The basic mode for local and remote debugging.

- Required for both local AND remote debugging (always-on).
- Offers "conventional debugging experience":
  - Debugging/halting/stepping USER-MODE applications: fully supported.
  - **Breaking into the debugger from KERNEL-mode: NOT available in VMI mode.**
  - Step-instruction in KERNEL-mode: NOT available in VMI mode.
- Scripts + custom codes work in both user-mode and kernel-mode.
- Works for local debugging via `.connect local`.
- Works for remote debugging via TCP (not serial).

**Implication for Pass C**: VMI mode is enough for our use case because we
don't need to pause/step kernel instructions — we just want EPT execute
hooks that fire on each ChaCha20 call and dump state via a script. No
kernel-mode break required.

## 2. Debugger Mode

For full kernel debugging with pause/step support.

- Requires a SEPARATE target machine (VM or physical) + serial connection.
- CANNOT be used for local debugging.
- Connection is OVER SERIAL (slow — docs recommend VMI mode via TCP for
  anything that doesn't need pause/step).
- Setup: WinDbg attached to debuggee first (to disable DSE+PatchGuard),
  then HyperDbg attaches via serial.

## 3. Transparent Mode

Hypervisor-presence hiding, orthogonal to the other modes.

- Enabled via `!hide` command, disabled via `!unhide`.
- Makes HyperDbg "transparent from anti-debugging and anti-hypervisor
  methods" — hides CPUID[1].ECX[31] hypervisor-present bit, cpuid vendor
  leaf 0x40000000, RDTSC timing anomalies, etc.
- Does NOT guarantee 100% transparency ("substantially harder" is the
  wording).
- Can be used in BOTH VMI mode AND Debugger mode.

**Elytra concern**: Elytra's `lighthouse_driver.sys` has 7 vmlaunch + 749
vmread instructions. If Elytra does CPUID / RDTSC-timing hypervisor
probes, Transparent Mode is what we'd need. Our Pass A string sweep of
`packer0` didn't surface explicit hypervisor-detection plaintext, but
Pass A only decoded 12 scalar inline-string stubs — more could be hidden
in deeper decode layers.

## Which mode for which task?

| Goal | Mode |
|---|---|
| ChaCha20 state capture via EPT hook (Pass C) | **VMI** |
| Pause-and-step kernel exploit development | Debugger |
| Any of the above while fingerprinting-resistant | add Transparent |
