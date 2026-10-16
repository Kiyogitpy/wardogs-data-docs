# Scope

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What this project does and doesn't cover. Read in conjunction with
[`INTENT.md`](INTENT.md).

This repository is a **documentation project**. It contains reference docs
for Wardogs' cooked data and static code paths, plus the mappings and SDK
dumps needed to read them. It is not a tooling repository: no runtime
agents, loaders, or instrumentation are published here.

## In scope

### Data documentation

- Every cooked data asset in `Wardogs/Content/` and
  `Wardogs/Plugins/GameFeatures/`
- Every property on every DataAsset / DataTable the game ships
- Every curve and lookup table
- Season-by-season diffs
- Cross-references between related assets

### Static reverse engineering

- Disassembly of `WardogsClient-Win64-Shipping.exe` using IDA Pro
  and the community `.idmap` / `.usmap` mappings documented in
  [`../mappings/`](../mappings/)
- CppSDK generation via UEDumper
- Function-level documentation of code paths that consume the
  documented data assets
- Formula documentation ("how multipliers combine", "how damage
  resolves", etc.) via static disassembly of an owned, offline image

All RE here is static: reading a binary and its mappings on disk. No
game process is executed or attached to for the documentation in this
repo.

### Security findings pipeline

- Private tracking of security-relevant findings
- Coordinated disclosure to Embark Studios
- Public write-up only after remediation (see
  [`../SECURITY.md`](../SECURITY.md))

## Out of scope — hard limits

### Tooling and instrumentation

- No runtime agents, memory-access primitives, loaders, or injectors
  are published in this repository
- Any private instrumentation used to produce or verify documentation
  stays out of this repo: single-operator, on the author's own
  hardware with an owned copy of the game, offline or in sessions where
  no other player can join or share the session
- This repo ships documentation, not programs

### Cheat tooling

- No ESP overlay (DirectX hook, WPF window, external renderer, ANY)
- No aimbot / triggerbot / aim correction applied to live input
- No wall-hack, no map hack, no radar
- No tool whose only use is in-game advantage over other players

### Distribution

- Nothing in this repo is packaged for general consumption
- No installer, no auto-updater, no one-click bypass
- Not shared on marketplaces, Discord cheat scenes, or similar

### Online multiplayer with real players

- Any observation that informs this documentation must run offline or
  in isolated sessions. Server-connected tutorials are permitted only
  when there is no possibility of other players joining or sharing the
  session.
- If that isolation is uncertain, do not proceed. Controlling a lobby
  alone does not establish isolation.
- There is no live-matchmaking exception, including read-only
  observation.

### Monetization

- No paid tier for "undetected cheats"
- No Patreon, no subscription, no commercial access control
- Documentation is CC-BY-SA 4.0 (free, with attribution)
- Code is MIT (free, open)

### Competing products

- Nothing extracted here goes into a competing game or engine
- No wholesale asset extraction for use in other projects
- Documentation is for understanding, not for cloning

## Soft limits — case-by-case

Some topics are judgment calls. Default posture:

### Memory offsets

- Documenting the UE actor structure with offsets (e.g.,
  `ACharacter.Health` is at offset `0x4B0` on CL-516586) is in
  scope — it's structural documentation
- Publishing a self-contained script that reads live memory from
  a specific offset without any surrounding context (plain
  cheat recipe) is out of scope

### Automation of RE tasks

- A script that parses cooked data or a static binary to help build
  the data docs: in scope
- A script that reads or acts on a live game process to produce
  in-game advantage: out of scope

## When in doubt

Ask: "If Embark's security team read this contribution tomorrow,
would they thank me or sue me?" If the answer isn't clearly
"thank me", route it through [`../SECURITY.md`](../SECURITY.md)
instead of publishing it.
