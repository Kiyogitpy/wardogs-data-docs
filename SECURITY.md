# Security Policy — Responsible Disclosure

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

## Posture

This repository documents **Wardogs** (Bulkhead, published by Team17) as a
defensive-research exercise. It is a documentation project: the
published output is the markdown reference docs, mappings, and SDK
dumps in this repository — not tooling.

The research produces two kinds of output:

1. **Public data documentation** — the markdown reference docs in
   this repository.
2. **Private security findings** — issues in the game's trust model,
   serialization, replication, or state validation that are reported
   privately to the responsible vendor before any public mention. These are
   not published here until coordinated disclosure completes.

This document describes the disclosure process for the second kind.

## What counts as a security finding here

A finding is in-scope for responsible disclosure when it affects:

- **Server trust assumptions** — e.g., gameplay math that assumes
  client-side values are honest where they shouldn't be
- **Replication exploits** — properties that leak or desync in ways
  that could enable advantage
- **Serializer bugs** — unit mismatches, overflow, OOB access in
  gameplay message handling
- **Validator gaps** — gameplay effects / abilities missing
  server-side authorization checks
- **Account / inventory impact** — anything affecting player
  identity, cosmetics ownership, progression state
- **Service disruption** — crash, hang, or amplification vectors
  from client inputs

Not in scope for disclosure (handled publicly in the data docs):

- Balance observations (DPS numbers, time-to-kill, weapon stats)
- Non-security code behavior documentation
- Public engine-architecture notes

## Disclosure process

When a finding is identified:

1. **Document privately** in `_findings/_private/` (gitignored).
   Include:
   - Technical description with reproduction steps
   - Affected game version and platform
   - Assessed severity (CVSS v3.1 or similar framework)
   - Suggested mitigation if obvious
   - Date identified

2. **Report to the responsible vendor** via their security channel
   (Bulkhead/Team17 for game logic and trust-model issues; Embark
   for Elytra anti-cheat issues):
   - **Primary:** the security contact listed on the vendor's site (if
     published) or the Steam store page support contact
   - **Secondary:** Steam support security form
   - **If no response in 7 days:** retry via a different channel

3. **Coordinated disclosure window** — the industry standard is
   90 days from report to public disclosure. This project adopts:
   - **90 days by default**
   - **Extended on request** for genuinely complex fixes
   - **Shortened if the issue is being actively exploited** in
     the wild (coordinated with the vendor)

4. **Post-remediation**:
   - Finding moves from `_findings/_private/` to
     `_findings/disclosed/`
   - Public write-up added, crediting the vendor's fix
   - CVE requested where applicable

## What this repo will NEVER publish

- **Working exploit code** for any disclosed or undisclosed finding
- **Live memory offsets** usable as a cheat recipe without the
  surrounding documentation context (specific actor base + health
  offset in a self-contained script, for example)
- **Account-takeover primitives** of any kind
- **Payment / monetization bypass** techniques
- **Any finding before coordinated disclosure window ends**, unless
  the vendor explicitly approves earlier publication

## Reporting a security issue you've found via this repo

If you found a Wardogs security issue by reading the docs here (good!
that's one of the intended outcomes), please:

1. **Do NOT open a public issue or PR describing it** on this
   repository.
2. **Email the project author privately** (contact in GitHub profile)
   so we can coordinate disclosure to the vendor.
3. **Alternatively, report directly to the vendor** via their security
   channel and leave this repo out of it entirely.

Either path is fine. The goal is "The vendor hears about it before the
internet does."

## Scope boundary — documentation vs tooling

This repository publishes documentation only: game data, trust model,
and static code behavior. It does not publish tooling. Specifically
out of scope for this repo:

- Runtime agents, memory-access primitives, loaders, or injectors
- User-ready tooling that would let others gain unfair advantage in
  live play
- Concrete bypasses of the game's protection layer
- Any artifact that would serve as a plug-and-play cheat loader

Documentation and RE commentary at the "how it works" level is what
this repo ships. It produces reference material, not programs.

## Credit

Security findings disclosed via this project are credited to the
reporter in the public write-up (post-remediation). If you want to
remain anonymous, say so when reporting.
