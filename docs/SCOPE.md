# Scope

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

What this project does and doesn't cover. Read in conjunction with
[`../CLAUDE.md`](../CLAUDE.md) and [`INTENT.md`](INTENT.md).

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
  and public `.idmap` / `.usmap` community mappings
- CppSDK generation via UEDumper
- Function-level documentation of code paths that consume the
  documented data assets
- Formula documentation ("how multipliers combine", "how damage
  resolves", etc.) via static disassembly

### Anti-cheat architectural notes

- Public documentation of Elytra's architecture at the level of
  "which Windows mechanisms does it use" (handle stripping via
  `ObRegisterCallbacks`, direct syscalls, kernel driver loading
  via `ZwLoadDriver`, etc.)
- Same posture as public write-ups of EasyAntiCheat, BattlEye,
  Vanguard, Fairplay, FACEIT AC
- Detection-vector documentation at the architecture level

### Research instrumentation (private, single-operator)

- Kernel-mode cross-process memory read primitive (Pass D agent)
- Loader for the above (orchestrates kdmapper + IOCTLs)
- Threat model and runbook for the research tooling
- Used only on the author's own hardware with the author's own
  purchased copy of the game, in offline modes or custom lobbies

### Security findings pipeline

- Private tracking of security-relevant findings
- Coordinated disclosure to Embark Studios
- Public write-up only after remediation (see
  [`../SECURITY.md`](../SECURITY.md))

## Out of scope — hard limits

### Cheat tooling

- No ESP overlay (DirectX hook, WPF window, external renderer, ANY)
- No aimbot / triggerbot / aim correction applied to live input
- No wall-hack, no map hack, no radar
- No tool whose only use is in-game advantage over other players

### Distribution

- Research tooling (`tools/pass_d/`) is single-operator; **not**
  packaged for general consumption
- No installer, no auto-updater, no one-click bypass
- Not shared on marketplaces, Discord cheat scenes, or similar

### Online multiplayer with real players

- The research instrumentation is used in offline modes, tutorial
  content, or custom lobbies the author controls
- Not deployed against live matchmaking games with uninvolved
  third-party players
- If a research question requires live matchmaking (rare), the
  observation is read-only, bounded, and reported to Embark
  before any public write-up

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

- A script that polls a value to help build the data docs: in scope
- A script that polls values and acts on them to produce in-game
  advantage: out of scope

### Timing analysis

- "How does Elytra time its integrity checks" — in scope as public
  architectural research
- "Here's a timing window to inject code" with working exploit:
  out of scope (goes through disclosure)

## When in doubt

Ask: "If Embark's security team read this contribution tomorrow,
would they thank me or sue me?" If the answer isn't clearly
"thank me", route it through [`../SECURITY.md`](../SECURITY.md)
instead of publishing it.
