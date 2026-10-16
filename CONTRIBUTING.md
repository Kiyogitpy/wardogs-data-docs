# Contributing

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Thanks for your interest. This repository is a defensive-research
documentation project — see [`CLAUDE.md`](CLAUDE.md) and
[`docs/SCOPE.md`](docs/SCOPE.md) before contributing.

## What contributions are welcome

### ✅ Data documentation improvements

- New per-category reference docs that follow the existing
  `Wardogs_<Category>_v<N>.md` pattern
- Corrections to existing docs (missing values, unit errors, wrong
  cross-references)
- Links from one doc to another where cross-references are missing
- "How Values Combine" section expansions when you can confirm from
  static disassembly or SDK structure (cite the function RVA or
  SDK class)

### ✅ SDK and mapping improvements

- Updated UEDumper outputs matching a new game build
- IDA mapping (`.idmap`) refreshes for new builds
- SDK class ↔ data doc cross-reference additions

### ✅ Tooling for the research pipeline

- Parsers, extractors, cross-reference generators
- IDA Python scripts for repeatable analysis tasks
- CUE4Parse configuration improvements
- Test data for the parsers

### ✅ Methodology and framing docs

- Scope clarifications
- Methodology refinements
- Threat model updates for the research instrumentation

## What contributions are NOT welcome

### ❌ Cheat-adjacent code

- ESP overlay implementations
- Aimbot or triggerbot logic
- Networked distribution of research tooling
- Automated gameplay-modifying scripts
- Any tool whose output is "undetected in-game advantage"

### ❌ Public security findings before coordinated disclosure

Any security-relevant finding (server trust, replication,
serialization, validator gaps, etc.) goes through
[`SECURITY.md`](SECURITY.md), not a public PR.

### ❌ Workaround removal of the game's protection layer for distribution

Documenting how the protection layer works at an architectural level: fine. Publishing a one-click bypass
tool that would let others cheat: not fine. The distinction is in
`CLAUDE.md`.

## PR workflow

1. Fork and branch from `main`
2. Make your change
3. For doc changes: ensure the "Still Not Pulled / Limitations"
   section at the bottom of the doc stays accurate (either resolve
   the item you address, or leave it)
4. For code changes: ensure the research-tooling threat model still
   applies (see `tools/README.md` if the tool is in scope)
5. Open the PR with a clear description of what you changed and why
6. The author will review and merge

## Build and dev

The docs render via Jekyll + GitHub Pages. Local preview:

```bash
# Install bundler + jekyll (one-time)
gem install bundler jekyll

# Build + serve
bundle install
bundle exec jekyll serve
# → http://localhost:4000
```

Data parsing / regeneration workflow lives in
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Code of conduct

Keep it civil, keep it technical, keep it on-topic. The project is
small enough that there's no formal CoC yet, but the above still
applies:

- No harassment of Embark, their employees, or any other party
- No doxxing, no personal attacks
- Technical disagreement is fine; keep it to the technical content

## Questions

Open a GitHub Discussion or issue for anything non-security.
Security goes through [`SECURITY.md`](SECURITY.md).
