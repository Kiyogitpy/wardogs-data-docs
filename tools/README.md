# Research Tooling

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Research instrumentation used to produce the data documentation
in this repository.

## Public tooling (in this directory)

| Tool | Purpose | Status |
|---|---|---|
| `cue4parse_extractor/` | CUE4Parse wrapper that produces `data/*.json` from `.pak` files | TBD — pipeline exists in author's workspace, not yet packaged |
| `doc_generators/` | Python scripts that turn JSON exports into reference MDs | TBD |
| `cross_ref_builder/` | Produces cross-reference indexes between docs | TBD |
| `ida_scripts/` | IDA Python scripts for repeatable analysis passes | TBD |

These are the tools that produce the public data documentation.
They're being migrated from the author's local workspace to this
public location.

## Private tooling (referenced, not committed)

Some research instrumentation is held outside this repository
because it has misuse potential — specifically, kernel-mode
primitives that read / write arbitrary process memory. See
[`../CLAUDE.md`](../CLAUDE.md) and [`../docs/SCOPE.md`](../docs/SCOPE.md)
for the scope posture.

### Pass D kernel agent

**Purpose:** verify static-RE hypotheses against live memory on
the author's own machine.

**Architecture:**
- Minimal kernel driver (~6 KB) loaded via kdmapper (BYOVD against
  iqvw64e CVE-2015-2291)
- Exposes four IOCTLs: PING, READ_MEM, WRITE_MEM, GET_MODULE_BASE
- Uses `MmCopyVirtualMemory` to bypass Elytra's handle stripping
- No hooks, no persistent presence, no network, no overlay
- Dies on reboot (never persists)

**What it does NOT do:**
- Register `ObCallbacks`, `CreateProcessNotify`, or `LoadImageNotify`
- Set DR0-DR3 hardware breakpoints
- Patch bytes in the game's `.text` section
- Create any debug object or attach debug port
- Expose any functionality beyond observation and single-shot writes
  for hypothesis verification

**Why private:** the four IOCTLs that make Pass D a research tool
could also be the primitive layer for cheat development. Keeping
the agent source + loader binary in the author's local workspace
reduces the chance of casual misuse. Architecture, threat model,
and detection surface are all documented publicly.

**Public artifacts:** architectural write-up and threat model will
land here under `pass_d/architecture.md` and `pass_d/threat_model.md`
once sanitized. The source stays local.

### kdmapper (patched build)

The author's patched build of
[TheCruZ/kdmapper](https://github.com/TheCruZ/kdmapper) with
multi-module support, `IoCreateDriver` dispatch, and ASCII
sanitization. Base tool is public and well-known; the patches
are specific to loading HyperDbg's module chain (Pass C — which
didn't work on the author's hardware; see
`../research/references/hyperdbg/`).

Patches documented at
`../research/references/kdmapper/README.md`.

## Research references archive

Full prior-work archive on debugger-attach vectors against
Elytra-protected processes:

- `../research/wardogs_analysis/DEBUGGER_ATTACHMENT_REPORT.md`
  — 5-vector merged research report, 484 lines, covers KDNET, HyperDbg,
  DMA, usermode-stealth, and tooling pipeline
- `../research/references/hyperdbg/` — HyperDbg docs archive +
  our crash analysis + resume protocol
- `../research/references/kdmapper/` — kdmapper + BYOVD background
- `../research/references/byovd/` — CVE-2015-2291 details
- `../research/references/bootviewer/` — measured-boot verifier

The research archive is in the author's workspace at
`E:\Reverse_Engineer\references\`; it will be migrated here as
individual pieces are sanitized for public release.

## Threat model

For any kernel-mode tooling in this project, the threat model
assumes:

- The author owns the hardware and the game
- Target process is Wardogs on the author's own PC
- No distribution to third parties
- No network component
- No persistence across reboot
- Observation is primary; write operations are only for
  single-shot hypothesis verification

Public threat-model docs will land under `pass_d/threat_model.md`
once the Pass D architectural write-up is sanitized for release.

## Related

- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Scope: [`../docs/SCOPE.md`](../docs/SCOPE.md)
- Security disclosure: [`../SECURITY.md`](../SECURITY.md)
