# `load` Command Reference
Source: https://docs.hyperdbg.org/commands/debugging-commands/load
Fetched: 2026-10-16

Loads HyperDbg's drivers and kernel modules into the target system.

## Syntax

```
HyperDbg> load [ModuleName]
```

## Modules

| Module | Description |
|---|---|
| **`all`** | Loads all available modules |
| **`kd`** | Kernel module (parent module for all others) |
| **`vmm`** | Hypervisor-related capabilities (**what Pass C needs**) |
| **`trace`** | Intel LBR + Intel PT tracing capabilities |

- `kd` is the parent — any of (`vmm`, `trace`, etc.) auto-loads `kd` first.
- `vmm` is where EPT hooks live.

## Expected Success Output (local VMI mode)

```
HyperDbg> load vmm
loading the vmm driver
current processor vendor is : GenuineIntel
virtualization technology is vt-x
vmx operation is supported by your processor
vmm module is running...
```

**We got through "vmx operation is supported" then CreateFile(0x1B1) in
one attempt, and BSOD on the next.** Both symptoms match known
issue 323 on 12th+ gen Intel.

## Requirements (from docs)

- Intel VT-x enabled (BIOS)
- Intel EPT (SLAT) support — any Intel from Nehalem (2008) onward
- For `trace` module only: Intel PT + LBR

## SDK Equivalents

If driving programmatically from a custom app linked against libhyperdbg:

```c
INT hyperdbg_u_load_all_modules();      // "load all"
INT hyperdbg_u_load_vmm();              // "load vmm"
INT hyperdbg_u_load_kd_module();        // "load kd"
INT hyperdbg_u_load_hypertrace_module(); // "load trace"

// Separate: install the driver (SCM-level, not just vmm activation)
INT hyperdbg_u_install_kd_driver();
```

Note: `hyperdbg_u_install_kd_driver` is where the SCM `CreateService` /
`StartService` chain lives — this is the part our `jne → jmp` patch at
`libhyperdbg.dll + 0x6158E` bypassed.

## Access Rights

> The application that requests to load the kernel modules should have
> `SeDebugPrivilege` to obtain a handle, otherwise an `ACCESS_DENIED` is
> thrown.

**Interpretation**: elevated PS is sufficient (SeDebugPrivilege is granted
to Administrators by default). We verified this with our runs — we got
past the ACCESS_DENIED stage.

## Context-destroying Behavior

> This command will continue the debuggee for some time (in Debugger
> Mode). This means that you lose the current context (registers &
> memory) after executing this command.

Only relevant in Debugger Mode (remote target). Doesn't apply to VMI
local debugging.
