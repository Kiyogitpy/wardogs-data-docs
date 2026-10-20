---
title: Round 9 status
nav_exclude: true
---

# Round 9: coverage and integration

Historical checkpoint. The [Round 10 continuation](ROUND10_STATUS.md) now
covers all 36 published models and 22 explosive sources, correcting the
angle, preference and contact-order assumptions recorded below.

This continuation starts at `e6eb7122`, after the reviewed SPW/Gepard viewer changes.
The original [Round 8 register](ROUND8_STATUS.md) now records 17 resolved entries
plus one scoped unsupported disposition. Pass 9 delivers the bounded integration
and coverage work below; the whole project backlog is not complete. All
executable and cooked-data research stays offline. Verification: 2026-10-20.

| Track | Status | Acceptance boundary |
|---|---|---|
| Remaining Round 8 item: underbarrel | Scoped unsupported | The shipped M4/default-input path has no ancillary firing binding; exact native lookup returns null. No hypothetical shot tag is assigned. [Evidence](evidence/round9-underbarrel.md). |
| Pass 8 integration verification | Passed within scope | All 17 resolved entries map to their evidence and applicable consumers; artifact and decoder checks pass. Runtime parity and intermittent ordinary regeneration are separate. [Audit](evidence/round9-integration-audit.md). |
| Vehicle sampling coverage | Extended from 4 to 18 of 36 models | Added 14 models using complete authored inputs; source identities, native family policy and attachment tags checked. Eighteen instanced-wheel models remain on the fallback sampler. [Evidence](evidence/round9-vehicle-sampling.md). |
| Remaining gameplay gaps | Open | Keep normal spawn/loadout provisioning and unsupported preset hypotheses separate from proven purchase/rejoin paths. |

Existing extractor and research changes in the working tree predate this pass. They are preserved; new work is reviewed within its own scope. Unknown `_tools/content.md` and `graphify-out/` are not part of this pass.

The user's T-72 rear-engine and stronger-splash reports reproduce even with
authored points. The linear falloff scalar passes; alternate trace origins and
an extra accepted location explain the preview's higher total. Native contact/
occlusion parity remains open and is the next focused correctness task. Do not
present this pass as a fix for those reports.

Checks: infantry **962/0**, radial decoder **42 rings / 132 armor factors**,
loadout **1,752/0** (external mirror), all-model MAAWS **312 shots**, all-source
coverage plus targeted tracked rerun, **339** fresh routing applications,
source audit **0 mismatches**, browser **23 profiles / 154 routes**, links
**0 broken**. One ordinary infantry regeneration passed on this continuation;
the prior intermittent child-process failure is not diagnosed or fixed.

The fresh [all-vehicle socket census](evidence/round8-vehicle-sampling-census.md) covers 121 package references across 33 source variants, with zero failed loads. That establishes input availability, not complete placement or native query parity for every model. Source-frame export precision, collision participation and moving/deployed state remain explicit boundaries.
