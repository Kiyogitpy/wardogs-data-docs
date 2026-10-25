# Research Tooling

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Research instrumentation used to produce the data documentation
in this repository.

## Tooling table

| Tool | Purpose | Status |
|---|---|---|
| [`cue4parse_extractor/`](cue4parse_extractor/README.md) | CUE4Parse exporter (WdExtract): GE effect values and Blueprint bytecode | Packaged. The older pipeline behind `data/*.json` is still in the author's workspace |
| [`../_tools/`](../_tools/) | Python scripts that turn the exports into doc tables and pages | In use |
| [Dumper-7](https://github.com/Encryqed/Dumper-7) | Generates the C++ SDK, `.usmap`, `.idmap` and GObjects dumps from the running game | External; local copy at `E:/Reverse_Engineer/tools/Dumper-7` (built 2026-10-23) |
| [IDAExecFunctionsImporter](https://github.com/Fischsalat/IDAExecFunctionsImporter) | IDA plugin that imports the Dumper-7 SDK and idmap into a database | External; local copy at `E:/Reverse_Engineer/tools/IDAExecFunctionsImporter`, installed in IDA 9.3 |
| `cross_ref_builder/` | Produces cross-reference indexes between docs | TBD |
| `ida_scripts/` | IDA Python scripts for repeatable analysis passes | TBD |

These are the tools that produce the public data documentation.
They're being migrated from the author's local workspace to this
public location.

## Related

- Methodology: [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md)
- Scope: [`../docs/SCOPE.md`](../docs/SCOPE.md)
- Security disclosure: [`../SECURITY.md`](../SECURITY.md)
