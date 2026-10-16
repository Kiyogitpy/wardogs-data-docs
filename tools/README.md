# Research Tooling

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Research instrumentation used to produce the data documentation
in this repository.

## Tooling table

| Tool | Purpose | Status |
|---|---|---|
| `cue4parse_extractor/` | CUE4Parse wrapper that produces `data/*.json` from `.pak` files | TBD — pipeline exists in author's workspace, not yet packaged |
| `doc_generators/` | Python scripts that turn JSON exports into reference MDs | TBD |
| `cross_ref_builder/` | Produces cross-reference indexes between docs | TBD |
| `ida_scripts/` | IDA Python scripts for repeatable analysis passes | TBD |

These are the tools that produce the public data documentation.
They're being migrated from the author's local workspace to this
public location.

## Related

- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Scope: [`../docs/SCOPE.md`](../docs/SCOPE.md)
- Security disclosure: [`../SECURITY.md`](../SECURITY.md)
