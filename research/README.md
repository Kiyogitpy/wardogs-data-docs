# Research archive

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Technical research notes supporting the reverse-engineering work
behind this project. These are the author's working notes and
curated external references — kept here so later sessions don't
have to re-derive what's already known.

## Structure

```
research/
├── README.md                       — this file
└── references/
    ├── README.md                   — references archive index
    ├── hyperdbg/                   — HyperDbg documentation + crash analysis
    │   ├── README.md
    │   ├── docs_index.md
    │   ├── operation_modes.md
    │   ├── load_command.md
    │   ├── local_debugging.md
    │   ├── build_install.md
    │   ├── faq_processor_support.md
    │   ├── vt_x_concepts.md
    │   ├── unsafe_behavior.md
    │   ├── connection_internals.md
    │   ├── issue_323_mtrr_breakage.md
    │   ├── our_crash_analysis.md
    │   ├── kdmapper_path_findings.md
    │   └── research_papers_summary.md
    ├── kdmapper/
    │   └── README.md               — kdmapper + BYOVD background
    ├── byovd/
    │   └── iqvw64e_cve_2015_2291.md — the specific driver vulnerability used
    └── bootviewer/
        └── README.md               — measured-boot verifier notes
```

## Why these specific topics

Each archive directory maps to a research question that came up
during the project's reverse-engineering work:

### `hyperdbg/`

HyperDbg is a cutting-edge hypervisor-based debugger
(VT-x + EPT). The project evaluated it as a possible primitive for
observing the game process below the anti-cheat layer. The archive
documents:

- How HyperDbg operates (VMI vs full-kernel mode)
- Why it was ultimately **not viable on this project's hardware**
  (Alder Lake + specific MTRR regressions documented in upstream
  issue 323)
- The specific crash signature observed and its root cause
- The resume protocol if a future session wants to retry on
  different hardware

### `kdmapper/`

kdmapper is a well-known BYOVD manual-mapper used to load unsigned
kernel drivers via a signed-but-vulnerable driver (iqvw64e). It
is **the loader used by the current primary research path**
(Pass D). The archive documents the author's patched build and
compatibility notes.

### `byovd/`

Deep-dive on **CVE-2015-2291** — the specific Intel driver
vulnerability (`iqvw64e.sys`) that kdmapper exploits. This is a
decade-old, Intel-acknowledged, widely-public vuln; it is included
here for context on how BYOVD loaders work and why this particular
one has held up for RE/research use.

### `bootviewer/`

TheCruZ's measured-boot verifier. Not currently in use but
documented as an alternative primitive to kdmapper's BYOVD approach
if that path ever gets closed.

## Scope and posture

The research in this archive follows the same posture as the rest
of the project (see [`../CLAUDE.md`](../CLAUDE.md)):

- **Defensive research** — documenting mechanisms, not building
  tools to attack others
- **Owner-operated** — all live-fire testing on the author's own
  hardware with the author's own purchased copies of software
- **Standard RE commentary** — the hypervisor and BYOVD topics
  covered here are extensively discussed in public security
  literature (CCS'22 HyperDbg paper, PWN2OWN write-ups, Pavel
  Yosifovich's Windows internals work, etc.)

The project **does not publish** working exploit chains built from
these primitives. The notes are reference material for understanding
how the research instrumentation operates.

## For contributors

If you add research notes:

- Put them in a topic subdirectory under `references/`
- Prefix with a README that explains why the topic is relevant to
  this project
- Keep attribution clean: cite primary sources (research papers,
  official docs) over secondary coverage
- Flag anything that would be security-sensitive if published
  (go through [`../SECURITY.md`](../SECURITY.md))

## Related

- Project scope: [`../docs/SCOPE.md`](../docs/SCOPE.md)
- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Tooling: [`../tools/`](../tools/)
