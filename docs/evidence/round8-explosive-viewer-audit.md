---
title: Rocket and explosive vehicle viewer audit
nav_exclude: true
---

# Rocket impact and splash: native behavior versus the vehicle viewer

Audit date: 2026-10-19, installed CL516586. This compares the previously
reviewed offline native evidence with the viewer at commit `6213d969`.
It does not claim runtime validation or a completed explosion simulator.

## A surface impact does not imply two damage terms

The [projectile trace](round8-radial.md) establishes that a qualifying
exploding hit skips the direct-damage block at `0x6B729A3` / `0x6B729AA`.
The deferred handler `0x6B70E20` chooses the radial branch and passes the
source to `0x6F06540` at `0x6B71032`–`0x6B71077`. The branch instruction
was independently decoded again for this audit. The explosion predicate
includes radius, arming, the instance gate, and ricochet/penetration state
(`0x6B7224B`–`0x6B722C6`); the [camera-projectile gate
report](round8-exploding-gate.md) bounds a concrete gate mutation.

Therefore an armed rocket landing on the vehicle is not established as
direct projectile damage **plus** blast damage. “Direct hit” and “Splash”
can describe impact locations: on the vehicle or nearby. They must not
silently request two native damage branches at once. An unarmed or
otherwise nonexploding projectile requires the separate branch conditions.
Thrown explosives and Molotov have their own [actor
paths](round8-explosive-actors.md), rather than inheriting this conclusion
solely from a UI category.

## Current viewer gaps

| Area | Verified behavior and current limitation |
|---|---|
| Impact position | `setupPicking` in `assets/js/vehicle-viewer.js` uses `materialFromPoint` to select a material/slot. It does not establish a world-space explosion origin or a ground impact. |
| Accepted damage hits | Native overlap, sampling, LOS and component filtering select accepted hits. The viewer supplies one manual distance and applies damage to one selected section. A material/slot or its bounding-box centre is not an accepted native hit. |
| Component identity | The [vehicle pipeline §4.1](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md#41-order) retains one hit per component. Every radial application on that vehicle chooses its section from the first retained hit (`0x5320394`), while each hit supplies its own rule location and distance. Summing damage independently into each clicked/material section would disagree with that path. |
| Routing | [Vehicle §4.2](../../pipelines/Wardogs_VehicleDamagePipeline_v1.md#42-routing-semantics) identifies three section flags that skip pre, post or simultaneous routing for radial events. `_tools/damage_tables.py` exports route lists without those flags; JS `applySection` traverses the lists unconditionally. |
| Source context | Native projectile blast retains the weapon damage tag and projectile ID and adds `DamageType.Explosive` plus the radius tag. `vehicle_rule_factor` currently builds radial context from asset context/root and radius only. A concrete affected rule must be checked before assigning a numerical error; the generated factors do not establish full source parity. |
| Distance | Native distance is original explosion origin to accepted `ImpactPoint` or synthetic candidate point (`0x6F03983`–`0x6F039C7`). `syncBlast` still says it is untraced. The [Points-mode report](round8-radial-points-components.md) establishes first-unoccluded-point selection, not a universal closest-surface shortcut. |
| Falloff bounds | `blastAmount` preserves the native minimum floor and effective-radius branch priority. `syncBlast` instead promises no damage at the outer radius and caps its slider there. That wording ignores the minimum floor, and the cap cannot cover the Havoc data's effective radius greater than outer radius. Accepted-hit filtering still governs whether an application exists. |
| Repeated shots | `simHits` repeatedly damages one section. It does not gather an explosion or establish whole-vehicle rocket hits to destroy. |

The arithmetic of an individual falloff amount is not a complete
explosion model. Whole-vehicle results require the retained component
hits and their order, per-hit contexts/distances, the first-hit section
selection, and radial routing flags. Geometry published for display
cannot by itself prove parity with the game's collision and LOS queries.

The current catalog contains 15 blast-enabled projectile entries: 14 in
Rockets & launchers and the 40 mm grenade. Its `weapons` arrays are
supported-caliber associations, not established loaded-ammunition or
weapon-context bindings. Model `centres` are merged per slot material,
and the JSON has no corresponding component identity. Deduplicating by
slot would therefore risk collapsing separate native component hits;
counting materials as components would be equally unsupported.

## Agreed interaction scope

The user selected the vehicle viewer, clicks on the vehicle **and nearby
ground**, and **one shot against a fresh vehicle per click**. A visible
impact marker and blast extent should explain the selected location;
results should distinguish sampled damage applications from the section
health changes after routing. “Direct hit” denotes a surface impact and
“Splash” a nearby detonation.

## Implementation follow-up

The local viewer now implements that interaction as a **reference-pose
estimate**, not a reproduction of the live physics scene. It places an
armed detonation, shows the outer/effective-radius rings and sampled
contacts, and computes section/main-health changes from fresh health.
The old Direct impact / Blast at distance branch selector is removed.
Middle-button browser autoscroll is cancelled inside the model element;
its pointer controls and scrolling outside the viewer remain separate.

The data export now retains radial routing skip flags, the projectile ID
and Explosive context on projectile radial factors, and the six reviewed
actor contexts without adding inferred tags. Current vehicle modifier
rows have no weapon-tag, caliber-tag or Explosive-type requirements;
correcting those projectile tags changes no current numerical factors.
The actors have separate factors, including AT mine, C4 and Molotov's
initial burst. Molotov's sustained fire is excluded.

`_tools/vehicle_impact_metadata.py` joins placed GLB nodes to owned module
fragment exports by module, mesh and attachment, including wheel instance
indices. All **36 models** resolve with **zero ambiguous matches**, with
consistent grouping across shared variants. Wheel instances belonging to
one native component share a key; materials are not used as component IDs.

The native cloud was further decoded at `0x6EF63C0`: the default 50 cm
PointCloudRadius and one shell yield the origin plus six axis offsets and
eight diagonal offsets. SDK `FWDDamageValues.bPreferUpwardsTrace` at
`+0x31` controls the first-two swap (`0x6F00B96`–`0x6F00BAD`). Ten
catalog projectile records explicitly set it false; five omit it and
remain unknown. Actor preferences are also unknown in the reviewed
fixture. The preview uses ordinary order for unknown values and says so.
Native `0x6F0341D` / `0x6F03420` exempts cloud index 1 from the
origin-to-start pretrace; the preview preserves that exception.

The native candidate producer still depends on loaded body transforms,
overlap item/body arrays and shape sampling (`0x6EFD9C0`), which these
triangle GLBs do not encode. The preview instead samples published
surfaces and checks visibility against that displayed geometry. It uses
GLB component order for its first section. Alternative first choices
reuse those fixed sampled hits; their displayed examples are neither
exhaustive permutations nor bounds on actual game damage. The isolated
ground plane is at the model's lowest point and supplies placement, not
a reconstruction of terrain collision. Moving parts, missing geometry,
live overlap order and external occluders can change the result.

## Validation

- `python -I _tools/vehicle_impact_metadata.py`: 36 models, 0 unresolved matches.
- `node _tools/vehicle_impact_check.js`: 204 nodes, 156,447 triangles,
  62 fresh/out-of-range shots; falloff boundary/priority, radial routing
  skips, native cloud layout and component deduplication checks pass.
- `python -I _tools/vehicle_impact_browser_check.py --out <local-output>`:
  installed Edge harness passes surface/background clicks, keyboard ground
  placement, fresh-shot reset, actor selection, vehicle reset, clear,
  360 px overflow and middle-button default-cancellation checks.
- Desktop (1440 px) and mobile (360 px) screenshots were inspected. The
  harness uses deployed base-theme CSS and equivalent native nested CSS
  for the new rules; it is not a full Jekyll/Sass build.
- JavaScript syntax, links and whitespace checks pass. No game process,
  account, game service or runtime collision state was accessed.
