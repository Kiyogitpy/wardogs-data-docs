---
title: Round 8 projectile explosion gate mutations
nav_exclude: true
---

# The unnamed explosion gate has a camera-projectile writer

Static CL-516586 investigation of restored executable SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
Only original-file instruction decoding and the read-only corpus were used.
No game process was run.

The [earlier writer trace](round8-radial.md#bexploding-writer-found-one-unnamed-gate-remains)
established that instance byte `+0x101` participates in `bExploding` and
defaults true. A bounded instruction scan of the 414 indexed functions at
RVA `0x6F20000`–`0x6F50000` found a concrete mutator:

- `0x6F391F0` resolves the projectile instance through `0x6F34110` and
  stores its bool argument at instance `+0x101` (`0x6F39204`). The lookup
  validates the handle/index/occupied bit and returns an 800-byte instance
  in the subsystem's instance storage, matching the SDK size `0x320`.
- `0x76CFEB0` calls the mutator at `0x76D02A7` and `0x76D0476`.
  Its caller `0x76CE670` has native alias `AWDCameraProjectile` slot 163.
  The first call supplies a camera-projectile acquisition bool; the second supplies
  false (`xor r8d,r8d` at `0x76D0470`).
- Independently decoded `0x76D026F`–`0x76D02A7` establish the first bool:
  if actor float `+0x44C > 0`, require actor `+0x5C8 >= +0x44C`;
  otherwise use candidate bool `r13b`. Handle getter `0x74F72E0` supplies
  the instance handle. The SDK field at `+0x44C` remains hashed.

Before testing that threshold, helper `0x76C88C0` updates `+0x5C8`.
For a retained candidate it resets accumulation when the candidate actor
changes, adds the supplied float interval and clamps at `+0x44C`.
Without the candidate it accumulates loss time at `+0x5CC`, then decays
`+0x5C8` using actor `+0x450` after a threshold selected from `+0x454`
or `+0x458`.

Independent original-executable review confirms that the supplied interval
is the actor-tick float: `0x76CE68B` preserves the incoming `xmm1`,
`0x76CE9A9` passes it to `0x76CFEB0`, `0x76CFEDD` preserves it there,
and `0x76D025D` passes it in `xmm3` to `0x76C88C0`. For finite ordinary
values, let L be actor `+0x44C`, T `+0x5C8`, Q loss time `+0x5CC`,
dt that interval, and c the current candidate bool. The helper implements:

```text
if c:
    if candidate != retained weak actor: T = 0
    retain candidate weak actor
    Q = 0
    T = min(T + dt, L)
else:
    Q += dt
    grace = actor[0x458] if L > 0 and T >= L else actor[0x454]
    if Q >= grace:
        T = max(T - dt * actor[0x450], 0)
        if T <= 0: clear retained weak actor
gate = (T >= L) if L > 0 else c
```

Machine anchors are `0x76C8900–0x76C894A` for the retained-candidate
branch and `0x76C8950–0x76C89C5` for loss, grace and decay. The gate is
tested after this update. Thus when L is positive, temporary loss of the
current candidate does not necessarily disable explosion immediately:
T can remain at L during the configured grace interval. Hashed property
names remain hashed; these labels describe arithmetic roles.

The candidate's final acceptance is also independently bounded. The loop
casts candidate actors to `BHBaseVehiclePawn` (class getter `0x53CAB60`),
calls `0x76CAB80`, and requires all three result bytes `+0x10/+0x11/+0x12`
(`0x76D0215–0x76D022A`). It takes the first passing candidate, setting
`r13b=1` at `0x76D023B`. The helper's first flag is distance from the
supplied origin to the actor's colliding-bounds origin <= actor `+0x448`
(`0x76CAC55–0x76CACDD`). Its second flag accepts either the computed
center direction angle <= actor `+0x444`, or intersection of the forward
segment of length `+0x448` with the actor bounds (`0x76CADC2–0x76CAF05`).
Its third flag requires no blocking Visibility trace from the supplied
origin to the bounds origin, with the projectile, candidate and related
actors added to the ignore query (`0x76CB09A–0x76CB0E8`). The three flags
start false. This verifies range, angular/bounds and LOS conditions; the
earlier broadphase callback `0x76C95C0 -> 0x76C76F0 -> 0x76C95D0` still
has additional eligibility filtering whose complete gameplay interpretation
is not assigned here. Do not call this an unconditional proximity fuse for
all nearby actors.

The scan also saw byte `+0x101` in tick function `0x6F3D740`, but that
access is on a different queued-record layout. Equal offsets do not prove
that it mutates the same instance field, so it is not counted as an
instance writer here. Copy constructors and the original default remain
separate from this demonstrated mutator.

The writer, instance identity, threshold/decay arithmetic and this camera
path's final geometric acceptance have now been independently reviewed.
It is safe to close the concrete writer/known-camera-mutation question.
The bounded scan does not prove these are every possible writer throughout
the executable, and the broadphase's remaining eligibility predicates are
not a universal gameplay activation specification. Preserve those limits
when combining this result with the original `bExploding` expression.
