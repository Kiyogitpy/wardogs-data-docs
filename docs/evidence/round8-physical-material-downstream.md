---
title: Round 8 physical material downstream consequences
nav_exclude: true
---

# Physical material: penetration, velocity and later damage

Static CL-516586 research, 2026-10-18. The existing read-only corpus,
restored executable and SDK were used, with important arithmetic, field
loads, branches and stores independently decoded from the executable.
Packed configuration was read from the existing offline extraction at
`E:/Reverse_Engineer/wardogs_analysis/round8_config_20261018/extracted`.
No game, service or runtime session was used. Only this new report was
written by this pass.

## Conclusion

Physical material affects whether a projectile can obtain an exit hit,
its penetration capacity, post-penetration velocity and penetration
history tags. Those velocity changes can reduce damage at a **later**
impact through the existing impact-speed damage scale. The current
impact event preserves the velocity before its own exit response.

For the named head/body materials, packed settings give both
`SurfaceType17` and `SurfaceType3` a penetration exit-speed modifier of
zero and a ricochet probability of zero. Their density can still differ:
PM_Head exports 0.2, while PM_Body inherits 1.0. Both appear in the
penetration history ignore list, which suppresses the history bitmap
marker after a successful penetration; it does not skip the preceding
velocity change.

There is no demonstrated extra health multiplier selected directly by
17 versus 3 in the traced bullet amount calculation. This is a bounded
conclusion about that calculation and its reviewed inputs, not a claim
that every actor override or custom damage system ignores physical
material. `FHitResult` still carries the material to downstream hooks.

## 1. From material to penetration result

The earlier [physical-material investigation](round8-collision.md)
establishes `0x6F2F740` → exit query `0x6F2FC20` and material response:
Disabled rejects exit calculation, Planar synthesizes an exit using
thickness, and Default uses body geometry. On success, the entry/exit
materials' Density values are read at `+0x3C`, with the maximum passed
to `0x6F2FB30` (`0x6F2FAB8`–`0x6F2FAED`). This pass follows the result
rather than treating it as an effects-only value.

The unreflected result block has the following demonstrated fields:

| Offset | Writer / use |
|---|---|
| `+0` | Entry-to-exit thickness returned by `0x6F2FC20`; Planar also applies `WDGameSettings.PlanarSurfaceThicknessScale` |
| `+4` | Thickness divided by `cosf(angle)`, `0x6F2FB57`–`0x6F2FB64` |
| `+8` | Angle supplied by `0x6F2F740`, `0x6F2FB4D` |
| `+0xC` | Capacity-like penetration distance calculated below, `0x6F2FBFE` |
| `+0x10` | Capacity divided by thickness, `0x6F2FC03`–`0x6F2FC07` |
| `+0x18` | Exit `FHitResult` copied by `0x6F2F740` |
| `+0x118` | Actor damageable-interface override flag copied by `0x6F2F740` |

Let `T` be thickness, `v` the impact speed in stored cm/s, `d` the
projectile Diameter (stats `+0x6C`), `m` its Mass (`+0x70`), `E` its
`PenetrationEffectivenessMultiplier +0x208`, `rho` the maximum material
density and `c = cosf(angle)`. The reviewed arithmetic is:

```text
effectiveThickness = T / c
capacity = (v * 0.01 * m * c * E)
           / (max(rho, 0.001) * 0.099999994 * d*d)
effectiveness = capacity / T
```

Capacity/effectiveness remain zero if the denominator or absolute `T`
fails the small-positive check. These names describe the observed
calculation; they do not assert real-world units for authored diameter
or mass. Diameter is squared directly; no pi factor appears here.
The math import thunks independently resolve as `acos` (`0x98F8146`)
and `cosf` (`0x98F8164`). Machine arithmetic is at
`0x6F2FB77`–`0x6F2FC07`.

The configured `ImpactIgnoreAngleClasses` includes `WDMoverCharacter`
and `WDTargetDummy`; the class test in `0x6F2F740` sets this angle to
zero (`0x6F2FA76`) for matching hit actors. This is distinct from the
physical-material history ignore list below.

## 2. Actual continuation and velocity write

Impact processing `0x6F36F40` calls the penetration calculation at
`0x6F372A3`. It may attempt ricochet through `0x6F36600`; the actual
penetration application is `0x6F36190`, called at `0x6F3733E`.

`0x6F36190` requires the exit hit's blocking bit. Unless the actor
override flag is set, it also requires `capacity > effectiveThickness`
and `T >= 0.01` (`0x6F361B2`–`0x6F361F3`). It resolves the projectile's
ammo-modified stats and the **entry material's** `SurfaceType +0x60`.
This type keys `PenetrationPhysMatExitSpeedModifiers` in subsystem
`+0x2D0`; absent entries use zero (`0x6F362C4`–`0x6F362E5`).

Let `p` be projectile `PenetrationExitSpeedMultiplier +0x20C`, and `s`
that surface-map value. Before random deflection, the component-wise
velocity update is:

```text
fraction = T / max(capacity, 1e-8)
surfaceAndProjectileFactor = clamp(1 - 0.5*(p+s), 0, 1)
newVelocity = oldVelocity * (1-fraction) * surfaceAndProjectileFactor
```

The named `PenetrationExitSpeedMultiplier` therefore participates in
this expression; it is not simply multiplied into velocity by itself.
The `1-fraction` term is not independently clamped in these instructions.
Do not assume the forced-penetration path obeys the ordinary positive
capacity gate.

Exact anchors: ratio `0x6F36294`–`0x6F362B3`; stats/surface combination
`0x6F362FB`–`0x6F36324`; clamp `0x6F36328` / `0x6F36333`; velocity
stores `0x6F36359` onward at instance `+0x20`, `+0x28`, `+0x30`.
If a nonzero vector remains, the function moves the projectile just
beyond the exit point, applies a random angular deflection and rebuilds
the velocity with the retained speed. It returns penetration success.
This pass establishes the speed arithmetic and continuation; it does
not re-derive the random deflection distribution or every subsequent
simulation termination condition.

## 3. Packed values for SurfaceType17 and SurfaceType3

`Wardogs/Config/DefaultGame.ini`, section
`[/Script/WDGame.WDGameSettings]`, line 303 supplies:

| Setting | SurfaceType3 | SurfaceType17 |
|---|---:|---:|
| `PenetrationPhysMatExitSpeedModifiers` | 0 | 0 |
| `PhysMatRicochetProbabilities` | 0 | 0 |
| `PhysMatRicochetRestitutionCoefficient` | 1–1 | 1–1 |

`0x6F37F12`–`0x6F37F25` resolves `WDGameSettings` and copies its
`ProjectileSystemSettings +0x458` to subsystem `+0x2A0` through
`0x6F2C180`. Thus the config property and consuming subsystem map are
connected. The packed extraction has one occurrence of the named
`ProjectileSystemSettings` property; this is not a runtime settings
snapshot or proof against later mutation.

The zero surface entries do not imply zero total speed loss. The
thickness/capacity term and projectile `p` still apply. Likewise,
restitution 1–1 is not an independent ricochet chance; the probability
map supplies zero for these surfaces in the reviewed settings.

## 4. Flesh ignore list affects history, not the completed velocity write

The same config property explicitly lists
`/Game/Environment/_Global/PhysicalMaterials/PM_Body.PM_Body` and
`.../PM_Head.PM_Head` in `PenetrationPhysMatIgnoreList`.

After `0x6F36190` succeeds, `0x6F36F40` checks that list (subsystem
`+0x2C0`) against the hit material: list read `0x6F3736C`, soft-reference
comparison `0x6F37406`, match branch `0x6F37421` → `0x6F37500`.
The match sets the eighth argument to `0x6F353F0` false. That function
still records `bPenetrated`, but writes the penetration bitmap only
when both penetration succeeded and this eighth argument is true
(`0x6F354F7`–`0x6F35516`).

The existing damage source builder uses the previous-hit penetration
bitmap to add `Kinetic.Impact.Penetration`. Accordingly this ignore
list can suppress that later history tag even though the physical
penetration response and velocity loss occurred. It is not a material
penetration-capacity bypass and does not make flesh transparent to the
speed calculation.

## 5. Current-hit versus later-hit health amount

`0x6F36F40` computes the impact-time velocity and snapshots it before
calling the exit-response functions (`0x6F36FE1`–`0x6F36FF1`). It
passes the snapshot to hit builder `0x6F353F0` at `0x6F37477`.
The builder copies it into `FWDProjectileHitData.ImpactVelocity +0x128`
(`0x6F35717`–`0x6F3573C`), while separately retaining the mutated
post-impact location/velocity when ricochet or penetration succeeded.

The direct bullet amount builder reads the **ImpactVelocity** vector,
not `PostImpactVelocity`: `0x6B72A7F`–`0x6B72AB5` takes its length;
`0x6B72AB9` calls speed scaler `0x6C255B0`; `0x6B72ACB` multiplies
the starting amount. The scaler uses the existing reference speed and
clamps the speed ratio to 0–1. Distance scaling, target armor hooks,
bone/context rules and health application then have their existing
roles; see [Damage §7.6](../../pipelines/Wardogs_DamagePipeline_v2.md#76-the-bullet-event).

Therefore this impact's exit-speed loss is not substituted into this
same impact's speed scale. A projectile continuing with the updated
instance velocity can reach a later impact at a lower speed, reducing
that later starting amount when the ratio falls below one. The
material history ignore list does not undo the velocity write.

No direct `SurfaceType3`/`17` health scalar was found in this concrete
amount-building chain: its demonstrated scalars are speed, distance
and the subsequent rule/hook path. That does not establish a universal
negative about every Blueprint, damageable override, custom hit or
future material consumer. No numeric damage-through-flesh prediction
is supplied without actual entry/exit geometry, ammo-modified stats
and effective actor/body state.
