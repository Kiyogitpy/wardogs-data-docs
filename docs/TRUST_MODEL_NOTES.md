---
title: Trust model notes (static analysis, unconfirmed)
nav_exclude: true
---

# Trust model notes

Evidence level for everything below: static-analysis image (`analysis_with_filtered_partial_unwind.exe`) plus the older restored image; virtualized dispatch not removed; capstone/pefile reading only; no runtime observation.

## From the hit-registration teammate (round 23 B)

1. `bClientPredictive` defaults to true: the native `FWDProjectileStats` constructor stores 1 (`0x699E212`). The 17 explicit cooked values are all false (rockets, artillery, missiles, drone). Every other round omits the field and so defaults to true (9mm, 5.45, 5.56, 7.62 variants, .50 Cal, 12g, buckshot, arrows and others).
2. Hit handler `0x6B73E90` branches on net mode (3 = client, derived from `0x3CAB0A0` `GetNetMode`). On a client, a projectile with the flag set and a local controller forwards its `FWDProjectileHitData` via `Server_ValidateClientHit` (sender `0x69E86F0`, call sites `0x6B740D9`, `0x6B74D6E`) and does not build damage itself. On the server it builds damage via `0x6B725B0` and `0x6B717C0`, skipping when `!IsServerOwned && !controllerIsLocal && bClientPredictive` (`0x6B74251`-`0x6B74271`). So for a remote client's predictive bullet the server's own simulation does not apply damage.
3. `Server_ValidateClientHit` implementation (vtable slot `0x500` of `UWDProjectileProxyComponent` = `0x6B74770`) looks like a 17-byte leaf that only frees `HitData.CustomHitResults` (`+0x100`) and returns; exec thunk `0x69E93E0` copies the 0x238-byte record from the wire. CAVEAT: the bytes at `0x6B74761`-`0x6B7476F` look like prologue fragments and `0x6B74781` onward decodes as nonsense; identical in both images. May be a protection-layer artifact. Treat as unconfirmed.
4. No consumer found for `ValidClientProjectileHitData` (`inst+0x2F8`) or `bFailedHitValidation` (`inst+0x310`) in `0x6B00000-0x6BD0000`, `0x6F20000-0x6F50000`, `0x76C0000-0x76E2000`. `Client_ValidateClientHit_Response` (`0x6B72370`) only walks a global listener list.
5. Client-supplied fields, if the server accepts the forwarded record: the `FHitResult` (impact point, bone, component, physical material), `ImpactVelocity`, `SimulationData` (elapsed time, seed, hit count, history bitmaps), `ProjectileOrigin` (feeds distance falloff).
6. No lag compensation found: `AutoProxyFixedTickInfo` and `FromToPct` are initialised to -1 in `0x6F353F0`; no writer, no rewind code.

## From the spread teammate (round 23 A)

7. For a single bullet the client draws the random cone direction (fresh CRT `rand()` per shot), rounds it to 16-bit pitch/yaw, and sends it in a 0x28-byte record (`Server_FireProjectile` `0x6B97900`); the server re-runs the shared executor `0x6B93610` with seed -1 and does not redraw. For shotguns the record carries the pellet seed (`Server_FireBuckshotProjectile` `0x6B97820`). No check of the received direction against the cone was found in `0x6B97900`, `0x6B97820` or `0x6B93610`. Whether the server limits it elsewhere (for example in hit validation) is open.

## What would confirm or refute

- Runtime test with a forged hit on a predictive projectile, and whether the server re-simulates from the seed. NOT to be run against the live game (Elytra kernel-level anti-cheat; terms of service). Only an owned, isolated, permitted setup would be acceptable.
- Devirtualizing or reading the true body of `0x6B74770` (item 3 may be a stub artifact).
- A search for any server-side use of the received direction/hit record beyond the three scanned ranges.

## Where the public docs stand

The public pages (`pipelines/Wardogs_HitRegistration_v1.md`, `pipelines/Wardogs_WeaponSpread_v1.md`) were scrubbed of items 1-7: they name the RPC pair (already visible in the public SDK dump) and the fire-record layout, and say server-side handling is not documented.

## Smoke authority, round 26 A (2026-10-23, static analysis only, unconfirmed)

Verdict: smoke volume geometry and sight blocking are CLIENT-SIDE; the server never builds a smoke volume. Nothing server-side reads smoke.

- Volume actor `AWDSmokeGrenadeVFXActor` (ctor `0x869C200`) has no `bReplicates` store and no `GetLifetimeReplicatedProps`; `SmokeVolume`/`Pawns` carry no Net flag. `BP_SmokeGrenadeVFX.Setup` calls `SetPoints` only for non-signal smokes (`SmokeType != 1`: White, Black), building the sphere-trace point list locally and pushing it to Niagara.
- Volume is registered via `0x869BED0` into `UWDSightBlockerSubsystem` (`0x6F4B100` class getter). Its `ShouldCreateSubsystem` (vtable slot 86, `0x6F4FDC0`) returns false on a dedicated server (`0x45C4DC0`), so smoke registration does nothing there. Subsystem exists for listen server, standalone, client.
- The explode cue that spawns the VFX actor is suppressed on a dedicated server (`UWDGameplayCueManager` slot 93 `0x4C55DB0` returns true when net mode == 1, unless a global byte overrides it; override not resolved).
- `AWDSmokeGrenadeAfterEffect` (`B_WorldSmokeGrenade_*`, ctor `0x869BFF0`) IS server-spawned and replicated (`or [actor+0x63],0x10`): `OwnerEntityTag` (+0x2C0) and a server-time float (+0x2C8), probably InitialOnly. Spawned in `AWDSmokeGrenade` Auth_Explode (slot 237, `0x869C640`) behind Role==Authority; non-authority computes a late-join start offset from GameState server time.
- Only consumer of the registered volume: aim-assist target manager (`0x6D820B0`, via eligibility override `0x6D81EB0`) via query `0x6F4E2D0`. This is local-controller aim assist, so smoke affects only the local client's target acquisition. `Pawns` list (`UpdatePawnsInBoundingBox` `0x869E420`, `UpdatePawnsInSmoke` `0x869F600`) has no native caller; result discarded at `0x869F765`.
- No smoke GameplayEffect or stealth/status tag in cooked data. Only tags: GameplayCue.SmokeGrenade.Explode, GameplayCue.Vehicle.Countermeasures.Smoke, ID.Item.SmokeGrenade._, Audio._.
- Throw/fuse (partial, not completed in round 26 A): `B_Action_ThrowExplosive_C.ThrowOrExplodeExplosive` runs only when IsDedicatedServer || IsStandalone and takes launch params from the server's `GetActorEyesViewPoint`; `StartFuseTimer` (`0x6CAF200`) is Authority-only and its handler calls Auth_Explode. So the server owns throw and fuse.
- Implication: a modified client skipping the volume or blocker registration would only change that client's aim assist and visuals. Smoke is not a server authority concern in the sense of hiding players from server-side checks.
- Open: GC_SmokeGrenade_Explode BP not dumped; trace channel TraceTypeQuery11 mapping; AfterEffect dormancy/NetUpdate (`0x3AA4150`, `0x3AA3C40`, `0x3AA3A50`); map tracker registration `0x53FFBF0`; other BPs calling UpdatePawnsIn\*. Round 26 B covers throw path and LOS.

## Smoke authority, round 26 B (throw path and LOS; static analysis only, unconfirmed)

Confirms and extends round 26 A. Verdict: throw, fuse and explosion are SERVER-authoritative; the smoke cloud as experienced is built locally on each machine; smoke changes no server-side gameplay outcome.

- No Server*/Client* RPC exists for throw, fuse or explode. Origin = server pawn `GetActorEyesViewPoint` + throw offset; velocity = throw curve + server `GetVelocity` influence; fuse = server `BaseFuseTime` (smoke 3.0) and timer. Client contributes only input timing and its normal view rotation. `B_Action_ThrowExplosive` spawns only if IsDedicatedServer || IsStandalone (deferred spawn -> `InitializeForThrow` -> finish -> `OnThrowRelease` `0x6CABE60`); `AWDGrenade::OnThrowRelease` (`0x6CAF180`) calls `StartFuseTimer` (`0x6CAF200`, Authority-only; callback `0x6CAE0C0` -> explode virtual slot 237). No client fuse timer.
- Replicated on `AWDExplosive` (`0x6CAA4D0`, push-model): `ThrowInfo` (+0x318), `ExplosionInfo` (+0x340), `ExplosiveAttachData`, instigator PlayerState. Smoke/grenade classes add no Net fields. Clients simulate canister physics locally; explosion cue gated by `ExplosionCueTimeoutTolerance`.
- Explode virtual `0x6CA80E0` (server only) builds blast/damage via `0x6CA8D20`, which returns early when NetMode==Client. Smoke override `0x869C640` (Authority) spawns `B_WorldSmokeGrenade_*` (AfterEffect, InitialLifeSpan 175 s), copies velocities, sets OwnerEntityTag. `Multicast_ExplodeInstantaneous` (reliable multicast, thunk `0x6CAD0C0`) exists; callers on the smoke path not traced.
- AfterEffect `BeginPlay` (`0x869CA10`) runs everywhere: server stores world time; clients compute start offset and run local cue `GameplayCue.SmokeGrenade.Explode`; server also registers `Trackers.Type.SmokeGrenade` (UI map tracker, call `0x1453FFBF0`). The cue presumably spawns `BP_SmokeGrenadeVFX`, which runs local traces and registers a local sight blocker (inferred from SDK; cue BP not dumped).
- Sight blocker (`UWDSightBlockerSubsystem`): query `0x6F4E2D0` has exactly one caller (`0x6D821E1`, aim-assist target manager virtual slot 161 `0x6D820A0`, threshold +0xE0 default 100). No AI perception, spotting, minimap, damage or hit-registration consumer. Producers: smoke VFX actor and `AWDSmokeTrailBlockerActor` (vehicle countermeasure smoke, 12 s, size 750; segments registered via `0x76A2FA0`).
- Smoke trace channel = `ETraceTypeQuery` 10, derived (UE ini ordering) as `VisibilityNoPawn` (`ECC_GameTraceChannel16`); reading of Block-by-default for profiles is an inference. Cloud shaped by local traces only. No smoke GE/tag affecting stealth/visibility/lock in `DefaultGameplayTags.ini`. GameState `OverrideAimAssistStrengthMultiplier` (Net) exists, so aim-assist strength is a server-replicated setting.
- Not determined: whether vehicle missile lock-on/homing consults smoke (no native caller in vehicle code, vehicle smoke is a separate system with `Server_FireSmoke`); dedicated-server cue suppression override byte; GC_SmokeGrenade_Explode contents; AI sight traces.
- Runtime test (offline or self-hosted only, never the live game; Elytra): server logs of Role/ThrownServerTime/ExplodeServerTime; replication debug of grenade and AfterEffect; dedicated-server run to confirm no cue/VFX/blocker; aim-assist with local smoke altered; vehicle lock-on versus vehicle smoke.
