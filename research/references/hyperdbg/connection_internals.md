# HyperDbg Connection Internals
Source: https://docs.hyperdbg.org/design/debugger-internals/kernel-debugger/connection
Fetched: 2026-10-16

## Current (v0.24) Transport Options

| Mode | Transport | Used by |
|---|---|---|
| **VMI (local)** | IOCTL to `\\.\HyperDbgDebuggerDevice` | `.connect local` (what Pass C uses) |
| **VMI (remote)** | TCP over network | `.listen` + remote `.connect <ip>` |
| **Debugger** | Serial port (kdserial) | Pause/step kernel on separate target |

Per docs: *"Currently, the only way to communicate with the kernel
debugger is over the serial port. For future versions, we will add
other IRQL-compatible mechanisms to communicate."*

That's for **Debugger mode** specifically. VMI mode uses IOCTL even
locally (confirmed by our RE of libhyperdbg.dll's `CreateFile` + 
`DeviceIoControl` call sites).

## Serial-Mode Internals (not what we use, but informative)

> We used **kdserial** from Windows SDK to connect to the debuggee. The
> connection over the serial port is initialized from the user-mode
> controller of HyperDbg.
>
> First, we let Windows to initialize the serial port from standard
> entry points like `CreateFile`. After that, we set the baud-rate and
> timeout details. We let Windows initialize the handle because this
> way, we make sure that Windows won't give the handle of this device
> to any other application and no other application is able to send
> anything over this port.
>
> Instead of this, we use the interrupt-mode of the serial device in
> the user-mode. This way, whenever the debugger needs to pause the
> debuggee, first it sends a request, and as it's in interrupt-mode,
> then Windows notifies the user-mode application about the new request
> from the debugger.
>
> If the request is valid, then the user-mode application sends an
> IOCTL to the kernel, and from that IOCTL, we execute a VMCALL to
> enter all cores to the vmx-root mode.
>
> In vmx-root mode, we halt all cores, and as the IF flag of RFLAGS is
> cleared, so no interrupt is allowed and this way, we halt all the
> cores and check for a new command from the debugger in polling mode.

Key insight: **serial comms are inner-loop just for `pause` events in
Debugger mode. All other commands (hooks, memory reads, script runs)
flow through IOCTLs regardless of mode.**

## VMI Mode Internals (what we care about)

Not explicitly documented at this URL, but inferable from code RE:

1. **CLI startup**: `hyperdbg-cli.exe` loads `libhyperdbg.dll`.
2. **`.connect local`**: libhyperdbg's command handler calls
   `CreateFileW(L"\\\\.\\HyperDbgDebuggerDevice", ...)`.
3. **Our Pass C patch**: libhyperdbg's hardcoded device name was in-place
   patched to a random suffix at file offset 0x36BE34 to match our
   kdmapper-mapped hyperkd.sys.
4. **`load vmm`**: libhyperdbg calls `DebuggerInstallDriver()` (SCM
   create+start). We patched the `jne` at 0x6158E to `jmp` so the
   install failure doesn't abort.
5. After the (bypassed) install, libhyperdbg calls `CreateFile` AGAIN
   on `\\.\HyperDbgDebuggerDevice` (we patched this one too, same
   suffix), then `DeviceIoControl` with the VMM-launch IOCTL.
6. hyperkd.sys's `IRP_MJ_DEVICE_CONTROL` handler receives the IOCTL,
   validates it, calls hyperhv.dll's `VmxOn` function sequence.
7. `VmxOn` sets `CR4.VMXE`, allocates VMXON region, executes `VMXON`,
   builds VMCS for each core via `KeIpiGenericCall`, calls `VMLAUNCH`.
8. **Where Pass C died**: step 7's `KeIpiGenericCall` dispatched to a
   core that failed `RDMSR` on `IA32_MTRR_PHYSBASE0` → BSOD.

## IOCTL Enumeration (from our RE of libhyperdbg.dll)

Found by scanning for `FF 15` IAT calls to `DeviceIoControl` and the
immediates passed as IOCTL codes. 67 `DeviceIoControl` call sites total.

HyperDbg's IOCTL codes are of form `CTL_CODE(0xDEE, func, method, access)`
where `0xDEE` is HyperDbg's custom device-type identifier.

We did not fully enumerate which IOCTL is "load vmm activate" — our
attempts at direct IOCTL dispatch from Python didn't get far because:
1. The IOCTL requires specific input buffers (not just a trigger).
2. hyperhv.dll's init code (which the IOCTL triggers) is what crashes
   on hybrid CPUs. Direct IOCTL wouldn't help.

For a future attempt, see HyperDbg's SDK IOCTL reference:
https://docs.hyperdbg.org/using-hyperdbg/sdk/ioctl
