# Research Tooling

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Research instrumentation used to produce the data documentation
in this repository.

## Tooling table

| Tool | Purpose | Status |
|---|---|---|
| [`cue4parse_extractor/`](cue4parse_extractor/README.md) | CUE4Parse exporter (WdExtract): GE effect values and Blueprint bytecode | Packaged. The older pipeline behind `data/*.json` is still in the author's workspace |
| [`../_tools/`](../_tools/) | Python scripts that turn the exports into doc tables and pages | In use |
| `cross_ref_builder/` | Produces cross-reference indexes between docs | TBD |
| `ida_scripts/` | IDA Python scripts for repeatable analysis passes | TBD |

These are the tools that produce the public data documentation.
They're being migrated from the author's local workspace to this
public location.

## Related

- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Scope: [`../docs/SCOPE.md`](../docs/SCOPE.md)
- Security disclosure: [`../SECURITY.md`](../SECURITY.md)
