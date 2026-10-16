# Local Debugging (VMI Mode)
Source: https://docs.hyperdbg.org/getting-started/attach-to-hyperdbg/local-debugging
Fetched: 2026-10-16

> If you want to debug your local machine without any remote physical
> machine or nested virtualization (like VMware Workstation, VirtualBox,
> Hyper-V, etc.), you should use local debugging.

## Caveats (quoted from docs)

> Generally, you can use most of the features of HyperDbg. Still, you
> should be cautious because if you unintentionally change any operating
> system's kernel structure that you did not suppose to, then a BSOD
> will happen.

> Some features like a break to the debugger and step kernel-mode
> instructions are not possible in local debugging; however, you can use
> these features for user-mode apps without any limitation. Of course,
> you can use almost all the kernel-mode features.

For Pass C, "most kernel-mode features" includes `!epthook2` which is
all we need for the ChaCha20 capture.

## Canonical Expected Flow (from docs)

```
HyperDbg> .connect local
local debugging (vmi-mode)

HyperDbg> load vmm
loading the vmm driver
current processor vendor is : GenuineIntel
virtualization technology is vt-x
vmx operation is supported by your processor
vmm module is running...
```

**Where our Pass C diverged:**

Attempt 1 (before patches, SCM install):
```
HyperDbg> load vmm
loading the vmm module
err, failed loading driver
unable to install KD driver
failed to install or load the driver
```
→ DSE rejection of unsigned driver.

Attempt 2 (with `jne→jmp` + `DO_DEVICE_INITIALIZING` clear patches):
```
HyperDbg> load vmm
loading the vmm module
err, failed loading driver                   ← install step was skipped by our patch
...
virtualization technology is vt-x
vmx operation is supported by your processor
err, CreateFile failed (1b1)                 ← device open rejected
```
→ `ERROR_DEV_NOT_EXIST` fixed by DO_DEVICE_INITIALIZING clear patch.

Attempt 3 (with the clear patch active):
→ **BSOD during VMM init** (hyperhv.dll + 0x1B00, RDMSR #GP on Alder Lake)
→ Matches known issue 323 symptoms.

## Why Issue 323 Hits Us Specifically

Multiple reporters on issue 323 had systems failing `load vmm` on:
- i9-13900H (13th gen)
- Our host: Alder Lake family 6 model 0xA7 (12th gen)

HyperDbg maintainer SinaKarvandi commented: *"I think the problem is with
the changes we made to MTRRs. I experienced the same problem sometimes,
but couldn't find a deterministic way of reproducing the error."*

Mattiwatti bisected to commit `bf6370d` and submitted fix `580907e`
("EPT: do not ignore default or WB type MTRRs in EptBuildMtrrMap()").

**Our build (v0.24, released 2026-09-22) is AFTER the regression and
BEFORE the fix was merged.** Confirming this is the root cause would
need rebuilding HyperDbg with Mattiwatti's fix cherry-picked.
