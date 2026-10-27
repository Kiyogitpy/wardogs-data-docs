# Contributing

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Thanks for your interest. This repository documents Wardogs' game
data. See [`docs/SCOPE.md`](docs/SCOPE.md) before contributing.

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

### ✅ Class and mapping notes

- Notes on classes and fields from a newer game build
- SDK class ↔ data doc cross-reference additions

Raw exports, class dumps and mapping files are not committed; cite
assets and classes by name instead.

### ✅ Tooling for the research pipeline

- Parsers, extractors, cross-reference generators
- IDA Python scripts for repeatable analysis tasks
- CUE4Parse configuration improvements
- Test data for the parsers

### ✅ Methodology docs

- Scope clarifications
- Methodology refinements

## What contributions are NOT welcome

### ❌ Code that acts on a running game

Overlays, aim or input automation, memory readers, loaders, or
anything else meant for an advantage in online play.

### ❌ Raw game files

Pak files, keys, raw exports or class dumps. Cite the asset or class
by name and path instead.

### ❌ Open security issues

A possible security problem in the game goes to the developer, not a
public PR. See [`SECURITY.md`](SECURITY.md).

## PR workflow

1. Fork and branch from `main`
2. Make your change
3. For doc changes: ensure the "Still Not Pulled / Limitations"
   section at the bottom of the doc stays accurate (either resolve
   the item you address, or leave it)
4. For generator changes: rerun the script and commit the regenerated
   page or JSON with it
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

- No harassment of Bulkhead, Team17, their employees, or any other party
- No doxxing, no personal attacks
- Technical disagreement is fine; keep it to the technical content

## Questions

Open a GitHub Discussion or issue for anything non-security.
Security goes through [`SECURITY.md`](SECURITY.md).
