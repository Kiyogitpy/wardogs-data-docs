---
title: Vehicle blast and section-viewer fixes
nav_exclude: true
---

# Vehicle viewer corrections, 2026-10-19

Build CL-516586. The viewer separates sampled physical contacts from damage
applications. Native radial code at `0x6F06B10`–`0x6F06B13` skips a repeated
nonempty hit-location tag on the same actor. The first encountered tag wins;
empty tags remain separate. Hull, turret and barrel contacts sharing MainBody
therefore do not each cause another MainBody health application.

Routing can target other health sections. Gepard's MainBody pre-route sends
5% to FuelTank while MainBody is alive. Its front-hull MAAWS regression has
five sampled component contacts, one application, 267.9 main-health loss
and 14.1 FuelTank loss routed from Main health. No FuelTank material contact
is accepted in that fixture. These are offline preview results, not gameplay
measurements. The UI identifies routed loss separately; its existing display
formatter rounds 267.9 to 268.

Section colors now use complete health-section tags, distinguishing left/right
tracks, individual wheels and main/tail rotors. Parts sharing a health section
share its color. All 16 current section tags have distinct palette entries.

Variant discovery includes nested `Variants/Air` and STN_05's `Varient`
directory. STN_05 now exposes its health/slot data with a no-model fallback;
impact placement stays disabled there. The fixed-wing variant has no health
sections or slot map and remains unsupported. Blast availability follows an
authored positive radius, exposing 30 mm cannon splash without enabling
explosion controls for ordinary bullets.

## Verification

- Full offline coverage: 6,864 placements across 36 models and 22 explosive
  sources, plus 339 fresh section-routing applications.
- Push check: all 36 models loaded, 312 MAAWS catalog placements and 62
  fresh/out-of-range checks passed, including the front-Gepard regression.
- Installed Edge: 23 profile legends, distinct computed section colors,
  154 slot routing descriptions, 30 mm impact controls, fresh-shot behavior,
  no-model fallback, 360 px overflow and viewer-only middle-button handling.
- Source/export audit: 33 source variants; 32 represented by 23 profiles;
  zero export mismatches. One unsupported fixed-wing definition is explicit.
- Syntax and whitespace checks pass. Browser validation uses local assets
  with deployed theme CSS; it is not a full local Jekyll build.

The viewer remains a reference-pose estimate. Native candidate generation,
registered collision shapes, incoming projectile velocity, terrain and overlap
order are separate research boundaries. These fixes do not claim exact
blast-collision parity.
