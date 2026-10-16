# Wardogs Data Docs

[![Repo](https://img.shields.io/badge/repo-Kiyogitpy%2Fwardogs--data--docs-blue?logo=github)](https://github.com/Kiyogitpy/wardogs-data-docs)
[![Site](https://img.shields.io/badge/pages-live-brightgreen)](https://kiyogitpy.github.io/wardogs-data-docs/)
[![Scope](https://img.shields.io/badge/scope-defensive%20research-informational)](CLAUDE.md)
[![License](https://img.shields.io/badge/license-CC--BY--SA--4.0%20%2F%20MIT-lightgrey)](LICENSE)

Comprehensive reference documentation for **Wardogs** (Embark Studios,
UE 5.7, build `++Wardogs+Live-CL-516586`): every number, table, curve
and asset the game ships with, extracted from cooked data and
cross-referenced to the UE class hierarchy.

- **Repository:** <https://github.com/Kiyogitpy/wardogs-data-docs>
- **Live site:** <https://kiyogitpy.github.io/wardogs-data-docs/>
- **AI-assistant context:** [`CLAUDE.md`](CLAUDE.md)
- **Scope + intent:** [`docs/INTENT.md`](docs/INTENT.md) · [`docs/SCOPE.md`](docs/SCOPE.md)
- **Methodology:** [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)
- **Security disclosure:** [`SECURITY.md`](SECURITY.md)

---

## What's in this repo

| Path | Contents |
|---|---|
| `*.md` (top-level) | 75 per-category reference docs (weapons, vehicles, items, game mechanics, UI, VFX, audio, animation, maps, meta, etc.) |
| `data/Wardogs/` | Cooked data exports (JSON, parsed from `.uasset` via CUE4Parse) |
| `sdk/` | CppSDK dump from UEDumper — UE class hierarchy mapping |
| `mappings/` | IDA Pro mappings (`.idmap`, `.usmap`) — exported class/field offsets |
| `docs/` | Scope, methodology, intent — project framing docs |
| `tools/` | Research instrumentation (access-controlled; see `tools/README.md`) |
| `research/` | Internal RE notes, debugger-attachment research |
| `_includes/`, `_sass/`, `assets/` | Jekyll theme for the GitHub Pages site |
| `CLAUDE.md` | AI-assistant context document — read this if you're an LLM working on the project |
| `SECURITY.md` | Responsible disclosure policy |
| `CONTRIBUTING.md` | How to contribute |
| `LICENSE` | CC-BY-SA 4.0 for docs; MIT for any code |

## Project scope and posture

**One line:** This is a defensive-research and documentation project.
The goal is a complete code↔data cross-reference of the game,
published as a public artifact, with any security findings routed to
Embark through responsible disclosure.

**It is NOT a cheat development project.** See
[`CLAUDE.md`](CLAUDE.md) for the detailed scope statement and
[`docs/SCOPE.md`](docs/SCOPE.md) for what's in and out.

**Posture clarifier:** DMA FPGA cards cost $300-500 and are
undetectable by Elytra. If the goal here were cheating, the author
would have bought one. The fact that this is a software-only,
locally-run, publicly-documented effort tied to responsible
disclosure is itself the scope signal.

## Reading order

New to the project:
1. [`CLAUDE.md`](CLAUDE.md) — what this project is and isn't (also used as AI-assistant context)
2. [`docs/INTENT.md`](docs/INTENT.md) — why this exists
3. [`docs/SCOPE.md`](docs/SCOPE.md) — what's in and what's out
4. [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) — how we work
5. [`index.md`](index.md) — the public data docs landing page

Specific research work:
- Research posture + prior passes: `research/`
- Anti-cheat technical notes: `research/debugger-attachment/`
- Pass D kernel agent: `tools/pass_d/` (access-controlled)

Security disclosure:
- [`SECURITY.md`](SECURITY.md) — how we handle findings

## Target build

| Attribute | Value |
|---|---|
| Game | Wardogs |
| Developer | Embark Studios |
| Engine | Unreal Engine 5.7 |
| Build | `++Wardogs+Live-CL-516586` |
| Platform | PC (Steam AppID 1867240) |
| Anti-cheat | Elytra (Embark in-house, successor to the AC stack from THE FINALS / ARC Raiders) |
| Season | Season 02 (data as of 2026-10-15) |

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Short version: new
data-doc contributions welcome, cheat-adjacent contributions
rejected, security findings go to [`SECURITY.md`](SECURITY.md)
disclosure channel not public PRs.

## Attribution

- **Wardogs** © Embark Studios AB
- **Unreal Engine 5.7** © Epic Games
- Community tooling: UEDumper, CUE4Parse, FModel, IDA Pro
- Research methodology references: HyperDbg CCS'22 paper
  (Karvandi et al.), various public RE write-ups of
  EasyAntiCheat / BattlEye / Vanguard

## License

- **Documentation** (`*.md` files, data analysis, methodology):
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code** (`tools/`, scripts, parsers): MIT License
- **Cooked data** (`data/`): subject to Wardogs EULA; redistributed
  here under fair-use research exemption for commentary and analysis.
  The author owns a legitimate copy of the game.

Full text in [`LICENSE`](LICENSE).
