# Intel VT-x Basic Concepts
Source: https://docs.hyperdbg.org/tips-and-tricks/considerations/basic-concepts-in-intel-vt-x
Fetched: 2026-10-16

Most definitions derived from Intel Software Developer's Manual, Vol 3C.

## Core Concepts

| Term | Definition |
|---|---|
| **VMM** | Virtual Machine Monitor. Acts as host, full control of CPUs + memory + interrupts + I/O. HyperDbg itself IS a VMM. |
| **Guest Software** | Each VM is a guest software environment. In HyperDbg's VMI mode, "the guest" is the already-running Windows OS. |
| **VMX Root Operation** | Ring -1. VMM runs here. |
| **VMX Non-Root Operation** | Where guest software runs. |
| **VMX Transitions** | Transitions between root and non-root. |
| **VM Entries** | Transition INTO non-root (host → guest). |
| **VM Exits** | Transition OUT OF non-root (guest → host). |
| **EPT (Extended Page Table)** | Second-level address translation. Maps guest-physical → host-physical. **HyperDbg uses EPT extensively** for hooks. |
| **VMCS (Virtual Machine Control Structure)** | Per-VCPU data structure that holds guest state + host state + control fields. Managed by VMM. |

## VMCS Logical Groups (6)

1. **Guest-state area** — processor state saved on VM exits, loaded on VM entries.
2. **Host-state area** — processor state loaded on VM exits (so VMM has clean state).
3. **VM-execution control fields** — control guest execution (which instructions cause exits).
4. **VM-exit control fields** — control WHAT happens on exits.
5. **VM-entry control fields** — control entries into guest.
6. **VM-exit information fields** — read-only, describe why/how an exit happened.

## VMX Instructions

| Instruction | Purpose |
|---|---|
| `INVEPT` | Invalidate translations derived from EPT |
| `INVVPID` | Invalidate translations based on VPID |
| `VMCALL` | Call to VM Monitor (from guest) |
| `VMCLEAR` | Clear VMCS |
| `VMFUNC` | Invoke VM function |
| `VMLAUNCH` | Launch VM (first time) |
| `VMRESUME` | Resume VM (subsequent) |
| `VMPTRLD` | Load VMCS pointer |
| `VMPTRST` | Store VMCS pointer |
| `VMREAD` | Read VMCS field |
| `VMWRITE` | Write VMCS field |
| `VMXOFF` | Leave VMX operation |
| `VMXON` | Enter VMX operation |

**Pass C crash context:**
- `RDMSR` (not strictly a VMX instruction) at hyperhv.dll + 0x1B00 raised #GP.
- On modern Intel with VMX enabled, some MSRs are "VMX-controlled":
  reading them requires VMX root mode. If hyperhv's init read a
  VMX-controlled MSR BEFORE finalizing VMXON, we'd get #GP.
- The specific MSR (`0x200` / `IA32_MTRR_PHYSBASE0`) is NOT VMX-controlled
  on standard CPUs. On Alder Lake E-cores, MTRR access during cold init
  from an IPI dispatch has documented quirks.

## Life Cycle of a VMM (per Intel SDM)

1. VMM boots → executes `VMXON` → enters VMX root operation.
2. VMM configures VMCS fields for a guest VCPU.
3. VMM executes `VMLAUNCH` → guest starts executing in VMX non-root.
4. Guest executes until it triggers a VM-exit condition.
5. CPU saves guest state to VMCS, loads host state from VMCS, control returns to VMM.
6. VMM services the exit, then executes `VMRESUME` → back to step 4.
7. Eventually VMM executes `VMXOFF` → leaves VMX operation entirely.

HyperDbg's VMI mode: step 1-3 happens at `load vmm`, then it's an
infinite loop of 4-6 for the duration of the session, step 7 happens
at `unload vmm`.

## VMX Non-Root Operation Restrictions (relevant to script engine)

Operations in VMX non-root (guest = Windows) that cause mandatory
VM-exits:
- `CPUID` (always exits — this is how HyperDbg hides hypervisor presence)
- `RDTSC` (optionally exits — control bit)
- `RDMSR`/`WRMSR` on controlled MSRs (optional)
- `IN`/`OUT` (optional, per-port)
- `MOV CR0`/`MOV CR3`/`MOV CR4` (optional, per-register)
- Any VMX instruction (`VMCALL` only legal in guest)
- Page faults (optionally)

HyperDbg's `!epthook2` leverages EPT permissions to trigger VM-exits on
specific physical pages, without needing any of the above.
