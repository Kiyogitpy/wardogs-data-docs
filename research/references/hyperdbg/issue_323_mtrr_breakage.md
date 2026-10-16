# Issue 323 — MTRR Breakage on Modern Intel (the actual root cause)
Source: https://github.com/HyperDbg/HyperDbg/issues/323
Fetched: 2026-10-16

## TL;DR

HyperDbg's `load vmm` makes modern Intel systems (12th gen / Alder Lake
and newer) hang or BSOD. Known upstream bug. Fix exists in a fork but
is not merged. **Our Pass C hit this exact bug.**

## Original Report (sjzbwdiy, Nov 25 2023)

Bisected failure to commit `4f0d0dc3bf3686772a58ebe85221dc3374be8188`.

Reproduction:
```
git checkout 4f0d0dc3bf3686772a58ebe85221dc3374be8188
hyperdbg-cli.exe
.connect local
load vmm
# → unresponsive hyperdbg-cli.exe
```

Earlier commits in the chain also showed the issue, with slight
variations (unresponsive VM vs unresponsive CLI).

## Maintainer Response (SinaKarvandi, Nov 26 2023)

> I think the problem is with the changes we made to MTRRs. I
> experienced the same problem sometimes, but couldn't find a
> deterministic way of reproducing the error.
>
> I try to see whether I can understand the problem from the source
> code or not, otherwise, we'll probably have to revert to previous
> MTRR changes.

Also noted: *"Unfortunately, each update to SDK, WDK, or even visual
studio breaks the compilations. I experienced the same issue a lot
these years."*

## Second Independent Bisect (Mattiwatti, 2024)

Different reporter, different symptom (entire system unresponsive, hard
poweroff required), but bisected to:
`bf6370d5a3d35bb7aeb16ce0d45fd77fda7bcca0`

The MTRR map change in that commit broke on their system.

Mattiwatti's fix: https://github.com/Mattiwatti/HyperDbg/commit/580907e2790e4ed6ce2275721c4b782f68df3711

Commit message: *"EPT: do not ignore default or WB type MTRRs in
EptBuildMtrrMap()"*

**This fix is NOT merged into mainline HyperDbg as of v0.24
(2026-09-22).** Pass C's crash matches Mattiwatti's symptom
(system BSOD on load vmm on modern Intel).

## Confirmed Affected Systems (from issue comments)

| System | CPU | Report |
|---|---|---|
| MSI Katana 15 B13VGK (Windows 11 22H2) | i9-13900H (13th gen Raptor Lake) | luist, Jan 2024 |
| Various builds | Alder Lake, Raptor Lake | sjzbwdiy, xmaple555, Suicolen |
| **Pass C target (our box)** | **Alder Lake family 6 model 0xA7 (12th gen)** | **Oct 2026** |

All share: hybrid P+E core architecture, 12th gen or newer Intel,
`load vmm` BSOD or hang.

## Build Workaround (for future attempts)

To build HyperDbg with Mattiwatti's fix cherry-picked:

```bash
# Clone with submodules
git clone --recursive https://github.com/HyperDbg/HyperDbg.git
cd HyperDbg

# Base from v0.24 release
git checkout v0.24

# Pull in Mattiwatti's fix
git remote add mattiwatti https://github.com/Mattiwatti/HyperDbg.git
git fetch mattiwatti
git cherry-pick 580907e2790e4ed6ce2275721c4b782f68df3711

# Build (needs VS2026 + latest SDK + WDK)
# Open hyperdbg.sln in VS, build Release|x64
# Output in bin/release/
```

Resulting `hyperkd.sys` + `hyperhv.dll` should then be drop-in
replacements for our kdmapper manual-map chain. All Pass C bins
(prep_hyperdbg.ps1, kdmapper patches, patch_hyperkd_names.py) remain
valid as long as the device-name string hyperkd.sys hardcodes is still
`\Device\HyperDbgDebuggerDevice` (unchanged in the fix commit).

## Alternative Workaround (not yet tested)

Downgrade HyperDbg to pre-`bf6370d` version. The issue tracker suggests
anything before that commit works on modern Intel. Trade-off: lose any
features added after `bf6370d`.

For Pass C specifically, we only need `!epthook2` which has been stable
since v0.9 or earlier, so downgrade is viable.

## Pass C Specific Signature Match

Our crash:
- STOP 0x1E (KMODE_EXCEPTION_NOT_HANDLED)
- STATUS_PRIVILEGED_INSTRUCTION (0xC0000096)
- Crash RIP: hyperhv.dll + 0x1B00 (`RDMSR` instruction)
- Caller: hyperhv.dll + 0x12B81, passed `ECX = 0x200` (IA32_MTRR_PHYSBASE0)
- Context: mid-`VmxOn` initialization, inside MTRR map build

**MTRR map build + hybrid CPU + 12th gen = textbook issue 323.**

## Related Issues to Watch

- `#648` — "Fix DRIVER_IRQL_NOT_LESS_OR_EQUAL when reading registers on
  a manually-halted core" (closed Jul 2026, merged)
- `#604` — "Add transparent platform identity and timing handling"
  (closed Sep 2026)
- `#694` — "pool manager lost allocation requests and lock held across
  allocations" (closed Oct 2026)

None of these address the specific MTRR regression. Issue 323 itself
is marked closed but may be regression-tested in future releases.
