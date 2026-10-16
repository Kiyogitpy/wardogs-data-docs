# HyperDbg Documentation Index (snapshot of llms.txt)
Fetched: 2026-10-16 from https://docs.hyperdbg.org/llms.txt

## Entry Points

- **Readme**: https://docs.hyperdbg.org/readme.md
- **Quick Start**: https://docs.hyperdbg.org/getting-started/quick-start.md
- **FAQ**: https://docs.hyperdbg.org/getting-started/faq.md
- **Build & Install**: https://docs.hyperdbg.org/getting-started/build-and-install.md

## Attach to HyperDbg

- https://docs.hyperdbg.org/getting-started/attach-to-hyperdbg.md
- Remote: https://docs.hyperdbg.org/getting-started/attach-to-hyperdbg/debug.md
- **Local (our target)**: https://docs.hyperdbg.org/getting-started/attach-to-hyperdbg/local-debugging.md
- Start a process: https://docs.hyperdbg.org/getting-started/attach-to-hyperdbg/start-process.md
- Attach to running process: https://docs.hyperdbg.org/getting-started/attach-to-hyperdbg/attach-process.md

## Prerequisites & Modes

- Prerequisites: https://docs.hyperdbg.org/using-hyperdbg/prerequisites.md
- **Operation Modes (VMI/Debugger/Transparent)**: https://docs.hyperdbg.org/using-hyperdbg/prerequisites/operation-modes.md
- Conditions: https://docs.hyperdbg.org/using-hyperdbg/prerequisites/how-to-create-a-condition.md
- Actions: https://docs.hyperdbg.org/using-hyperdbg/prerequisites/how-to-create-an-action.md
- Signatures: https://docs.hyperdbg.org/using-hyperdbg/prerequisites/signatures.md

## Debugging Modes

- User-mode: https://docs.hyperdbg.org/using-hyperdbg/user-mode-debugging.md
  - Principles: https://docs.hyperdbg.org/using-hyperdbg/user-mode-debugging/principles.md
  - Examples/basics: https://docs.hyperdbg.org/using-hyperdbg/user-mode-debugging/examples/basics.md
  - Events: https://docs.hyperdbg.org/using-hyperdbg/user-mode-debugging/examples/events.md
  - SYSCALL/SYSRET: https://docs.hyperdbg.org/using-hyperdbg/user-mode-debugging/examples/events/getting-results-of-a-system-call.md
- Kernel-mode: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging.md
  - Principles: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/principles.md
  - Beginning: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/beginning/connecting-to-hyperdbg.md
  - Setting Breakpoints: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/basics/setting-breakpoints-and-stepping-instructions.md
  - Memory ops: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/basics/displaying-and-editing-and-searching-memory.md
  - Registers: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/basics/showing-and-modifying-registers-and-flags.md
  - .process / .thread: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/basics/switching-to-a-specific-process-or-thread.md
  - Hooks: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/events/hooking-any-function.md
  - SYSCALL interception: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/events/intercepting-all-syscalls.md
  - Monitor hooks: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/events/monitoring-accesses-to-structures.md
  - Special insns (rdtsc, pmc, io): https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/events/triggering-special-instructions.md
  - Exceptions/interrupts/MSRs: https://docs.hyperdbg.org/using-hyperdbg/kernel-mode-debugging/examples/events/identifying-system-behavior.md

## SDK (Programmatic Interface)

- https://docs.hyperdbg.org/using-hyperdbg/sdk.md
- Events: https://docs.hyperdbg.org/using-hyperdbg/sdk/events.md
- Conditions: https://docs.hyperdbg.org/using-hyperdbg/sdk/events/conditions.md
- Actions: https://docs.hyperdbg.org/using-hyperdbg/sdk/events/actions.md
- **IOCTL interface**: https://docs.hyperdbg.org/using-hyperdbg/sdk/ioctl.md
- Event registration via IOCTL: https://docs.hyperdbg.org/using-hyperdbg/sdk/ioctl/event-registration.md

## Debugging Commands (core)

- `?` evaluate/execute: https://docs.hyperdbg.org/commands/debugging-commands/eval.md
- `~` select core: https://docs.hyperdbg.org/commands/debugging-commands/core.md
- `a` assemble: https://docs.hyperdbg.org/commands/debugging-commands/a.md
- **`load` modules**: https://docs.hyperdbg.org/commands/debugging-commands/load.md
- `unload` modules: https://docs.hyperdbg.org/commands/debugging-commands/unload.md
- `status`: https://docs.hyperdbg.org/commands/debugging-commands/status.md
- `events`: https://docs.hyperdbg.org/commands/debugging-commands/events.md
- `p` step-over: https://docs.hyperdbg.org/commands/debugging-commands/p.md
- `t` step-in: https://docs.hyperdbg.org/commands/debugging-commands/t.md
- `i` instrumentation step: https://docs.hyperdbg.org/commands/debugging-commands/i.md
- `gu` step-out: https://docs.hyperdbg.org/commands/debugging-commands/gu.md
- `r` registers: https://docs.hyperdbg.org/commands/debugging-commands/r.md
- `bp` set breakpoint: https://docs.hyperdbg.org/commands/debugging-commands/bp.md
- `bl` list breakpoints: https://docs.hyperdbg.org/commands/debugging-commands/bl.md
- `be` enable breakpoints: https://docs.hyperdbg.org/commands/debugging-commands/be.md
- `bd` disable breakpoints: https://docs.hyperdbg.org/commands/debugging-commands/bd.md
- `bc` clear breakpoints: https://docs.hyperdbg.org/commands/debugging-commands/bc.md

## Design Internals

- **Overview**: https://docs.hyperdbg.org/design/debugger-internals.md
- Events/Conditions/Actions: https://docs.hyperdbg.org/design/debugger-internals/{events,conditions,actions}.md
- Kernel Debugger: https://docs.hyperdbg.org/design/debugger-internals/kernel-debugger.md
- Design Perspective: https://docs.hyperdbg.org/design/debugger-internals/kernel-debugger/design-perspective.md
- **Connection**: https://docs.hyperdbg.org/design/debugger-internals/kernel-debugger/connection.md

## VMM Module Features

- https://docs.hyperdbg.org/design/features/vmm-module.md
- NMI control: https://docs.hyperdbg.org/design/features/vmm-module/control-over-nmis.md
- Message tracing: https://docs.hyperdbg.org/design/features/vmm-module/vmx-root-mode-compatible-message-tracing.md
- `!epthook` design: https://docs.hyperdbg.org/design/features/vmm-module/design-of-epthook.md
- **`!epthook2` design** (what we need): https://docs.hyperdbg.org/design/features/vmm-module/design-of-epthook2.md
- `!monitor` design: https://docs.hyperdbg.org/design/features/vmm-module/design-of-monitor.md
- `!syscall / !sysret`: https://docs.hyperdbg.org/design/features/vmm-module/design-of-syscall-and-sysret.md

## Tips & Tricks

- Considerations index: https://docs.hyperdbg.org/tips-and-tricks/considerations
- **VT-x basics**: https://docs.hyperdbg.org/tips-and-tricks/considerations/basic-concepts-in-intel-vt-x.md
- VMX root vs non-root: https://docs.hyperdbg.org/tips-and-tricks/considerations/vmx-root-mode-vs-vmx-non-root-mode.md
- **"Unsafe" behavior**: https://docs.hyperdbg.org/tips-and-tricks/considerations/the-unsafe-behavior.md
- Script engine in VMX non-root: https://docs.hyperdbg.org/tips-and-tricks/considerations/script-engine-in-vmx-non-root-mode.md
- Transparent mode: https://docs.hyperdbg.org/tips-and-tricks/considerations/transparent-mode.md
- Switch process layout (CR3): https://docs.hyperdbg.org/tips-and-tricks/misc/switch-to-new-process-layout.md
- Instant events: https://docs.hyperdbg.org/tips-and-tricks/misc/instant-events.md
- Message overflow: https://docs.hyperdbg.org/tips-and-tricks/misc/message-overflow.md

## Research & Papers

- Landing: https://research.hyperdbg.org/
- Kernel Debugger Design: https://research.hyperdbg.org/debugger/kernel-debugger-design/
  - 1st Edition PDF: https://research.hyperdbg.org/assets/documents/kernel-debugger-design-1st-edition.pdf
- VM-exit Transparency: https://research.hyperdbg.org/debugger/transparency.html
- **CCS'22 Paper (arXiv)**: https://arxiv.org/abs/2207.05676
- Reversing Machine (CCS'25): https://arxiv.org/abs/2405.00298
- Awesome list: https://github.com/HyperDbg/awesome
- Command map (classic ↔ HyperDbg): https://hyperdbg.github.io/commands-map/

## Repositories

- Main: https://github.com/HyperDbg/HyperDbg
- Releases: https://github.com/HyperDbg/HyperDbg/releases
- Scripts: https://github.com/HyperDbg/scripts
- Starting scripts (device-guard regs): https://github.com/HyperDbg/starting-hyperdbg-scripts
- Mattiwatti's fork with MTRR fix: https://github.com/Mattiwatti/HyperDbg

## Community (for asking questions)

- Discord: https://discord.gg/anSPsGUtzN
- Telegram: https://t.me/HyperDbg
- Matrix: https://matrix.to/#/#hyperdbg-discussion:matrix.org
- Issues: https://github.com/HyperDbg/HyperDbg/issues

## Tutorial Material

- OST2 course (preferred): https://ost2.fyi/Dbg3301
- YouTube playlist: https://www.youtube.com/playlist?list=PLUFkSN0XLZ-kF1f143wlw8ujlH2A45nZY
- "Hypervisor From Scratch" (background): https://rayanfam.com/tutorials
