---
title: Round 8 generator native-failure investigation
nav_exclude: true
---

# Ordinary Python regeneration remains intermittent

The reviewed outputs and their numerical checks pass, but ordinary regeneration
is not a reliable gate on the installed Windows CPython 3.13.7. This is a
generator-process investigation, separate from the offline Wardogs executable
research. No game process was launched or attached.

## Current observations

- Installed interpreter: CPython 3.13.7, tag `bcee1c3`, MSC 1944, AMD64,
  standard GIL build. No active Python trace/profile hook was reported.
- Earlier ordinary runs failed with `3221225477` (`0xC0000005`); passing
  runs, including two ordinary `--write` runs, were also recorded.
- In the latest bounded comparison, ten ordinary subprocesses running
  `python -I -S -X faulthandler _tools/infantry_tables.py --explosives`
  returned zero. Run 11 returned `3221226505` (`0xC0000409`) with empty
  stderr. This records the native exit code, not a diagnosed exception
  subcode or a proven stack-buffer fault.
- Thirty CDB-launched runs of that same command returned normally. Ten more
  CDB runs with `_NO_DEBUG_HEAP=1` also returned normally. Instrumented
  success does not establish why the uninstrumented process fails.
- Eleven ProcDump-launched runs exited normally and produced no dump. The
  monitor's own `4294967294` exit means its requested dump count was not
  reached; its logs separately report target exit `0x00000000`.
- A focused evaluator probe completed 12,000 calls, and a separate real-data
  zone-encoding probe completed 370 calls. Neither is a reproducer.
- A later ordinary `--write` failed with a child exit of 1 in
  `--actor-explosives`; its parent exception did not include captured child
  stderr. Both output files remained byte-identical. A subsequent run passed.
  This failure cannot be equated with the native exit codes without the
  missing child diagnostic.

The `-I -S` failure does not require site initialization or third-party
site packages. It does not by itself isolate the fault to a particular
CPython subsystem, rule-evaluation expression, installed binary, OS component
or hardware condition. No matching upstream defect was established.

A read-only Windows Application-log check on 2026-10-19 found six
Application Error events (ID 1000) and eight Windows Error Reporting events
(ID 1001) within the preceding two days, but none matching the Python
process. The Application log was enabled and readable. This supplies no
faulting-module or exception-stack evidence; it neither diagnoses the
failures nor establishes that they were ordinary Python exceptions.

## Reproduction and retained evidence

The bounded-run logs are local, outside the repository:
`E:/Reverse_Engineer/wardogs_analysis/round8_python_native_20261018_232949/`.
`plain11.stderr.txt` is deliberately empty; the exit status is recorded above.
CDB logs are `trial1.log` through `trial30.log` and
`no_debug_heap1.log` through `no_debug_heap10.log`. ProcDump stdout contains
UTF-16 monitor text interleaved with UTF-8 target output; the saved `.bin`
files preserve those original bytes. No crash dump was captured.

CDB was the existing Windows Kits x64 executable. Its commands enabled
access-violation and `0xC0000409` breaks before continuing, then requested
exception/register/stack information. No native fault occurred in those runs.
The existing x86 ProcDump executable was invoked directly: the PATH shim
points at an absent `procdump64.exe`. Its license was already accepted;
no installation or postmortem-debugger registration was performed.

## Diagnostic fix

`write_docs()` now emits a failed child's captured stderr before re-raising
the original `CalledProcessError`. Previously that diagnostic was hidden by
the parent's default exception display. No retry or alternative evaluator
was added. `_tools/infantry_regen_check.py` failed before the fix and passes
after it: a later child failure reports stderr while leaving both generated
files unchanged, including a previously successful table block.

One ordinary regeneration after this diagnostic fix returned zero, reported
nine tables unchanged, and left both generated files byte-identical. This is
a passing run, not proof that the intermittent native failures are repaired.

## Remaining boundary

No runtime workaround, runtime upgrade or cause claim is justified by
these results. The successful traced-snapshot rendering creates reviewable
artifacts but does not repair ordinary regeneration. A native fault capture
or a controlled comparison against a clean interpreter is the next useful
discriminator; repeated successful debugger runs alone do not close this gate.
The proposed separate same-version clean-interpreter comparison has not
been performed. Project rules require approval for a runtime change, and
that approval has not been supplied. Existing-runtime static and diagnostic
work can continue independently; this input blocks that comparison only.
