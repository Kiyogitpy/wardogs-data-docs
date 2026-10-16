# VMX-Root "Unsafe" Behavior (Script Engine Constraints)
Source: https://docs.hyperdbg.org/tips-and-tricks/considerations/the-unsafe-behavior
Fetched: 2026-10-16

Critical for anyone writing capture.hds scripts for `!epthook2`.

## What "Safe" / "Unsafe" means

> It's so tricky to manage code in the VMX root-mode. As HyperDbg gives
> you the ability to run your custom assembly code in all modes of
> execution, you should avoid doing some "**unsafe**" behavior that
> leads to system instability.

When an `!epthook2` fires, the script runs in **VMX root mode** on the
VMM side (not inside the guest). The constraints are strict.

## Things we must NEVER do inside a script action

### 1. No NT APIs with IRQL limitations

> You should never use an NT API in the VMX-root if it has IRQL
> limitations. Make sure that you use only those APIs that are marked
> with (**ANY LEVEL**) in MSDN. For example, calling
> **ExAllocatePoolTag** will halt the system most of the time. Also,
> sometimes it's observed that even "**ANY LEVEL**" functions led to a
> system fault.

Script engine built-ins (`print`, `printf`, `poi`, `db`-like reads) are
engineered to be VMX-root-safe. Custom codes via `code { ... }` are not.

### 2. No paged memory access

> You should not access a paged pool while you're executing in the VMX
> root-mode. If you access these pages and the page is paged out, it'll
> result in a system halt or crash.

Reason: interrupts + exceptions are masked in VMX-root. A page-fault
exception can't be delivered → system halt.

**Pass C implication**: when we do `poi(@rcx)` on Wardogs's ChaCha20
buffer, if that buffer happens to be paged out at hook-fire time, we
crash. Mitigation: on physical hardware with 32GB+ RAM, paged-out
state is rare for actively-used buffers, but not impossible.

### 3. CR3 is wrong by default

> When you're executing in the VMX-root, your **cr3** view of memory is
> the **SYSTEM** process (**pid=4**)'s view of memory. If you want to
> access another process memory, you should change the **cr3** by
> yourself and return to system **cr3** immediately. Otherwise, you
> won't let the HyperDbg return gracefully, and you'll see BSOD.

**MAJOR Pass C implication**: our `!epthook2` fires on runtime.dll which
is mapped INTO Wardogs's process address space. When the hook triggers,
our script runs with SYSTEM's CR3, NOT Wardogs's CR3.

The hooked address `runtime.dll + 0xD7C030` resolves to a user-space
VA (around `0x200000000 + 0xD7C030 = 0x200D7C030`). SYSTEM process
doesn't have this VA mapped — our `poi(@rcx)` on user-space addresses
will fault or read garbage.

**Fix**: use `.process /i wardogsclient-win64-shipping.exe` BEFORE
running the capture.hds script. This switches HyperDbg's logical process
context so script memory reads use Wardogs's CR3. (Already in our
capture.hds — docs confirm this is the right primitive.)

Alternative scripting primitive: HyperDbg's `.pagein` meta-command
brings a page into RAM before access.

### 4. Direct user-mode code access from VMX-root

> Do not directly access user mode codes from the VMX-root mode. It is
> because user-mode codes are located on paged memory, and there are
> two problems here. First, you need to find the **cr3** of the user,
> and it's not the process **cr3** because, for **KPTI** mitigation of
> **Meltdown**, **cr3** of user space is different from kernel **cr3**.
> It's also observed that accessing a user-mode memory (even if it's
> recently executed) causes a system crash. The problem is solved if
> you inject a **#PF** to the guest with that address.

So reading `[rcx]` where rcx is user-space inside a VMX-root script is
NOT just a CR3 switch — need to use the KPTI shadow CR3 OR inject a
page fault into the guest and let Windows swap it in first.

HyperDbg's script engine built-ins (`poi`, `db`) handle this internally
when `.process /i` was used first. Our capture.hds uses only built-ins,
so this is handled.

## Safe Memory Access Primitives

### In commands (interactive)

- Read VA memory: `db`, `dc`, `dd`, `dq`, `dw`, `da`, `dds`, `dps`, `dqs`
- Edit VA memory: `eb`, `ed`, `eq`
- Reference: https://docs.hyperdbg.org/commands/debugging-commands/d

### In scripts (automated)

- Memory read keywords: `poi(addr)`, `hi(addr)`, `low(addr)`, etc.
- Memory edit functions: `eb(addr, val)`, `ed(addr, val)`, `eq(addr, val)`
- Reference: https://docs.hyperdbg.org/commands/scripting-language/assumptions-and-evaluations

### Page-in on demand

- Interactive: `.pagein <addr>` meta-command
- Reference: https://docs.hyperdbg.org/commands/meta-commands/.pagein

## When memory read "fails" even on a valid address

> Sometimes, addresses that you try to access are valid but HyperDbg is
> not able to read or modify the address and keeps showing a message
> that the address is invalid. This is mainly because the address is
> paged out and is not available in RAM. Or in some cases, the address
> is actually available in the RAM but the operating system didn't make
> it present for the current process's memory layout.
>
> In order to solve that, we could use the `.pagein` command to bring
> the pages into the RAM and make it available for both the process and
> HyperDbg.

## Pass C capture.hds Audit

Current script uses:
- `printf("fmt: %llx\n", @rcx)` — safe (VMX-root-compatible logger)
- `poi(@rcx)` — safe when `.process /i` set correctly
- `.process /i wardogsclient-win64-shipping.exe` — correct primitive

Script does NOT use:
- `code { ... }` custom assembly — would be unsafe risk
- Any ExAllocatePool-style calls — not available in script engine anyway
- Manual CR3 switch — not needed, `.process` handles it

Audit result: capture.hds is VMX-root safe assuming the mapping chain
could actually VMLAUNCH (which it can't, per issue 323).
