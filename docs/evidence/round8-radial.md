---
title: Round 8 radial damage evidence
nav_exclude: true
---

# Round 8: radial damage, static investigation

Research date: 2026-10-18. Build CL-516586. The original restored executable was read offline; SHA-256 recorded by the existing corpus is `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`. No game process, service or IDA database was opened. Findings below combine narrow reads of the existing read-only corpus with independent Capstone disassembly of the executable. They describe native paths, not observed gameplay.

## Findings and closure

**2026-10-19 correction:** a retained component hit is not necessarily a
separate damage application. `0x6F06540` also maintains an actor-keyed set
of selected hit-location tags; a later contact with the same nonempty tag
branches past event creation/application at `0x6F06B13`. The
[vehicle follow-up](round8-explosive-viewer-audit.md#correction-hit-location-deduplication-and-routed-fuel-damage)
records the raw instruction checks and Gepard reproduction. Earlier
per-component wording describes contact filtering only.

The [point-mode/component follow-up](round8-radial-points-components.md)
supersedes this pass's alternate-mode and unnamed-selector gaps: the routine
previously called voxelized is shipped **Points**, the native default.
All three modes reach the same original-origin distance writer. Exact
component state after Mutable/attachment changes remains open.

| Question | Result |
|---|---|
| Starting blast amount and falloff | Confirmed, including minimum floor and branch priority |
| Inner versus Outer tag | Closed: Inner iff gathered `Distance <= EffectiveExplosiveRadius`; Outer otherwise |
| Distance reference | Closed for the ordinary/native point and disc gather: blast origin to accepted hit `ImpactPoint`, or origin to candidate point for a synthetic accepted hit |
| Source context on exploding projectile blast | Closed: stats context, weapon damage tag and projectile ID survive; Explosive and radius are appended |
| Exact components that actually receive a given blast | Partly resolved: overlap/eligibility/LOS/component filtering traced; the exact loaded component/body set and alternate voxel mode remain open |
| `bExploding` writer | Found and machine-verified; one additional unnamed instance flag's producer remains open |

## Amount, radius tag and distance

At `0x6F06540`, the per-hit loop reads `FHitResult.Distance` at hit `+0x8`. Instructions `0x6F06792–0x6F06831` confirm this ordered computation, where B is BaseDamage, E EffectiveExplosiveRadius, R ExplosiveRadius, F ExplosiveDamageFallOff and M MinimumExplosiveDamage:

```text
if d <= E: amount = B; radius = Inner
else:
    radius = Outer
    if d >= R: amount = 0
    else:
        t = clamp((d-R)/(E-R), 0, 1)
        amount = B * ((1-F) + F*t)
amount = max(amount, M)
```

The existing small-denominator branch is also confirmed: for `abs(E-R) <= 1e-8`, t is 1 when d >= E, else 0. The E branch takes priority; do not describe the R cutoff as unconditional when E > R. The minimum floor applies even after the zero branch. This is a linear curve, not a power exponent. Instructions `0x6F0686D–0x6F06884` select global `0xD36A498` when the Inner boolean is set, otherwise `0xD36A4A0`, then append the selected tag to the copied source context. Initializers `0x127A650` and `0x127A6F0`, independently disassembled, bind these globals to the ASCII strings at `0xB348050` (`Meta.Damage.Explosive.Radius.Inner`) and `0xB348078` (`Meta.Damage.Explosive.Radius.Outer`).

The distance producer is the real function at `0x6F03720`; the corpus incorrectly starts its row at `0x6F0371F` and emits an empty `nullsub_2026`. That pseudocode cannot establish its behavior. Machine instructions `0x6F03983–0x6F039C7` subtract the original blast origin at gather-context `+0x40` from the selected point, square and sum XYZ, take the square root and write a float to hit `+0x8`. Ordinary accepted collision hits supply hit `ImpactPoint` (`+0x28`), as seen at `0x6F03A7B–0x6F03A8A`. The special accepted target-root path uses the candidate point (`rsi`) at `0x6F03983`; synthetic hits use the candidate point too (`0x6F03A99–0x6F03B64`, constructor `0x3EAF060` sets both Location and ImpactPoint). Thus d is not inherently actor-center distance, component-center distance, or distance to the closest capsule surface. Which point wins depends on the gather's sampling and collision result.

The disc mode helper `0x6EF72C0` changes a trace start by projecting/clamping a point to a disc, then invokes the same `0x6F03720`. Its distance write still uses the original origin stored in the gather context, not the temporary trace start. The nearest accepted sample may replace a prior sample in `0x6EF70D0`: machine `0x6EF7115–0x6EF711E` compares stored versus new hit `Distance` and keeps the smaller value for that sample slot.

SDK anchors: `sdk/raw/WDGame_structs.hpp`, `FWDDamageValues` near line 3724; `sdk/raw/Engine_structs.hpp`, `FHitResult` (Distance +0x8, Location +0x10, ImpactPoint +0x28). All geometric units here are engine centimetres.

## Source context: the viewer's W = 1 assumption is not established

The radial routine copies the complete supplied `FWDDamageEntityData` (`0x6F06580–0x6F065F6`), including entity tag, context container and CauseEntityTag. It conditionally appends its damage-type argument (`0x6F065EF–0x6F06635`), then appends the radius tag per hit. It does not reconstruct context solely from projectile asset defaults.

The exploding-projectile route supplies an already enriched source:

- `0x6B72808–0x6B72848`: copy projectile stats entity/context; overwrite CauseEntityTag from weapon slot `+0x1C`; append slot `+0x10` weapon damage tag.
- `0x6B7284D–0x6B728B3`: conditional ricochet/penetration history tags.
- `0x6B728B8–0x6B728F6`: append the projectile asset's ProjectileId when nonempty.
- `0x6B729A3–0x6B729AA`: a true hit `bExploding` branches past the direct-damage block. DamageType.Projectile (`0x6B729D1–0x6B729E6`) and arming-delay ExplosiveBlunt (`0x6B729EB–0x6B72A0A`) are appended only in that skipped block.
- `0x6B717C0` copies this event into the deferred record and copies hit bExploding to deferred `+0x2D8` (corpus lines 198–225). `0x6B70E20` selects the radial branch for that flag. Machine `0x6B71032–0x6B71077` passes deferred `SourceEntityData` at `+0x60` into `0x6F06540`.
- The damage-type argument is `0xD36A800`, initialized as `Meta.Damage.DamageType.Explosive` by `0x127A150`.

Consequently this projectile blast preserves the weapon tag and projectile/caliber ID, adds Explosive and Radius, and does not add Projectile or ExplosiveBlunt on this route. Existing custom tags in input context are retained. This does not claim that every other caller, especially thrown explosives and Blueprint calls, supplies the same weapon tags.

The effective bone factor is conditional on the event conversion and target hook, not merely context presence. The radial builder starts with an empty hit-location tag for ordinary characters; vehicle section lookup can fill it. `0x6EF8DE0` can derive a hit-location from `HitResult.BoneName` only on its empty-target-entity branch. The armor investigation found that ordinary valid armor definitions are removed from the hook's removal set, so no filtered target-root copy is needed and bone fallback remains available; unresolved/incompatible armor-family tags can instead cause a root copy and suppress that fallback. This conditional detail is cross-investigator evidence and should be independently checked by the integrating reviewer. Do not preserve a universal blast W=1 assertion merely because the old investigation had not traced weapon context; do not replace it with a universal assertion that every radial hit has a valid bone tag either.

## Gather and component eligibility

Call chain: `0x6F06540 -> 0x6F01E50 -> 0x6EFFDC0`, followed by `IWDDamageable` hit-array filtering at `0x6F06715–0x6F06723` and per-hit evaluation.

Confirmed native criteria and sampling:

1. `0x6EFFDC0` obtains the world and performs a spherical overlap with ExplosiveRadius. Machine `0x6EFFED5–0x6EFFFBA` sets shape kind 2 and radius, and passes collision channel 3 to `0x3CAD6D0`. SDK `Engine_structs.hpp:512` identifies channel 3 as `ECC_Visibility`. The caller's actor ignore list is put into the query first (`0x6EFFEB2`). An optional additional overlap path is controlled by global `0xCED1164`; this was not fully resolved.
2. Overlap actor and component references must resolve and be valid. The actor's class must implement `WDDamageable`; nonimplementers are skipped (corpus `0x6EFFDC0` lines 431–460; machine check ending `0x6F00316–0x6F0031A`). Component records are grouped per actor/component, retaining overlap body/item indices.
3. Components can expose `DamageQuerySocket` sample transforms. The name global `0xD380AE0` is initialized by machine `0x12DE0C0–0x12DE0CE` from ASCII `DamageQuerySocket` at `0xB433708`; gather compares against it at `0x6F00425`. The comparison tests the FName comparison index. The component socket enumeration loop uses 12-byte descriptors and requests transforms through the component's virtual interface.
4. Ordinary gather `0x6EFC4A0` handles skinned meshes, skeletal body indices, instanced static meshes, socket samples and generic components separately. Class getters `0x3D559C0`, `0x3D518D0`, `0x3A39990` name those first three classes. A skeletal component without socket samples uses overlap body indices and body transforms (`0x6EFC4A0`, corpus lines 241–294); sockets use their transform positions. Generic fallback first uses the component bounds origin (`component+0x130`; corpus lines 485–488) and can add shape-based samples. The exact shape sampling list is not fully rederived here.
5. Accepted hits in `0x6F03720` are gated by trace result, radius and ownership/component checks. The ordinary collision branch checks original-origin-to-ImpactPoint <= R, then that hit Component matches the sampled component (with a target-root exception controlled by a flag), and, where supplied, Item matches the overlap item (`0x6F039D8–0x6F03A75`). A synthetic fallback requires its skip-LOS/config flag (`0x6F03A8F–0x6F03A93`). The additional target-root path at `0x6F0379F–0x6F039D1` verifies ownership and radius before synthesizing a candidate-point hit.
6. `DamageSystemSettings.ActorClassesToIgnoreInLOSCheck` at settings `+0x358` and `ActorClassesToIgnoreAttachParentOcclusion` at `+0x368` influence visibility/parent handling. `ActorClassesToSkipLOSCheck` at `+0x348` is inspected in `0x6EF8680`. These are SDK-named fields; their concrete configured class lists were not acquired here.
7. Character filter `0x6E6DCC0` rejects the array for a protected occupied seat; otherwise `0x6C2A790` normally retains one valid hit per component. The generic filter can alternatively retain only the first hit when its interface predicate returns true. This investigation did not enumerate the exact instantiated character component set or all interface override predicates.

The ordinary and disc paths are sufficient to identify the distance producer. An alternate voxelized path `0x6EFD9C0`, selected by the gather mode/global and generated samples, has not been checked for every possible hit-distance writer. The reflected bCheckLOS parameter versus all internal flags also needs a focused parameter trace; do not infer every flag from its name. Therefore close the basic gather mechanism, but retain an explicit limit on exact runtime body/component enumeration and alternate-mode equivalence.

## `bExploding`: writer found, one unnamed gate remains

Follow-up found a [camera-projectile gate mutator](round8-exploding-gate.md).
Its candidate semantics remain under review; the expression below stays valid.

`FWDProjectileHitData.bExploding` is byte `+0x18A` (SDK near line 5223). Writer `0x6B721B0` is called by `0x6B73E90` at `0x6B73EED`, before the event-building call at `0x6B742D8`. Machine instructions `0x6B7224B–0x6B722C6` establish:

```text
bExploding = false
if resolvedStats.ExplosiveRadius > 0:
    bExploding =
        (!stats.bHasArmingDelay ||
         instance.ElapsedTime >= float(stats.ArmingDelay - 0.0001f))
        && instance.byte_0x101
        && !hit.bRicocheted
        && !hit.bPenetrated
```

The subtraction happens in single precision before comparison against the double ElapsedTime (`instance+0x290`). The flag is reset before the stats validity/radius checks. `instance+0x101` is in SDK padding. Its default writer is established: constructor `0x6B8E100`, instruction `0x6B8E23C`, writes the word `0x0101` to instance `+0x100`, making both bytes `+0x100` and `+0x101` true. Copy routines `0x6B8D830` and `0x6B8EFF0` preserve byte `+0x101`. Its semantic name and every possible later mutation have not been established. Thus the unnamed gate defaults true, but arming plus an explosive radius is not the entire expression. This closes “what native function writes bExploding” and most of its expression, not every condition under which a particular launcher explodes.

## Suggested integration changes

Update Damage §1.1 with verified distance references, Inner/Outer initializers and the source-context propagation above; preserve the gather limits. Update §7.6 with `0x6B721B0` and the exact bExploding expression, keeping unnamed `instance+0x101` open. In `_tools/infantry_tables.py`, close stale `radial-amount`, replace `radial-context` with the caller-specific facts, and narrow `radial-split`/`exploding-hit` to the remaining concrete unknowns. The generator should model the retained source context, and use a bone multiplier only under its explicitly stated hit-location assumptions. Keep total damage across gathered components unmodelled until the actual component/hit set is supplied.

## Independent armor cross-check

The critical claims in `round8-armor.md` were independently checked against executable instructions, not just that report. The radial caller passes an empty explicit tag and a pointer to zero at `0x6F06BA6–0x6F06BBA`. In the general hook, `0x6B536B6–0x6B536F8` leaves the location-present boolean false for those inputs; `0x6B537E9–0x6B537EC` therefore jumps over both coverage arrays. `0x6B537BB` adds each armor-family tag to the removal container; an accepted valid definition reaches removal at `0x6B538E2`. Removal helper `0x395F230` shifts the remaining tags and decrements Num at `0x395F28F`. Only a nonempty remainder causes the target entity copy at `0x6B53919–0x6B5393D`.

The converter's tested value is confirmed to be the initial target entity tag: `0x6EF9070–0x6EF907F` copies event `+0x28` to the local tested at `0x6EF90B9`. A nonempty value bypasses fallback. When empty, successful target discovery followed by an empty explicit location reaches the bone lookup at `0x6EF91A1–0x6EF91B3`. Thus an all-valid-equipment model can retain the actual mapped per-bone multiplier, including its weapon row; that is conditional on a valid mapped bone and normal target discovery, not a promise for synthetic unmapped hits or invalid equipment tags.

The armor calculation is separate: `0x6B53107` loads the original amount, `0x6B53117–0x6B5312C` passes the original source entity to a new event builder, and `0x6B5314F–0x6B5315D` evaluates that new event with bool 0. Builder `0x6BB4F18–0x6BB4F1B` installs the selected armor tag as its target root. This armor-table evaluation must not be multiplied into the character's health amount.

Generator implications verified: preserve weapon/caliber plus Explosive on projectile blasts; retain mapped bone factors under the stated valid-equipment assumption; and evaluate each retained armor/helmet context tag at every modeled Infantry hit location on the radial path, without filtering by that item's Covers list. Health rules' own hit-location requirements still apply. Multi-piece combinations must be evaluated together through the rule evaluator, not assumed to equal a product of independently displayed item factors. Invalid/unresolved armor tags and unmapped bones remain explicit limits.

## Independent explosive-actor cross-check

The requested numeric/inheritance/context claims in [round8-explosive-actors.md](round8-explosive-actors.md) and `assets/data/explosive-actors.json` were independently checked against the original executable and the fresh local JSON exports. No contradiction was found in this scope. This check does not independently close the Molotov fire timer/patch geometry or all Blueprint detonation control flow.

The explosive constructor call at `0x6CA7A79–0x6CA7ABF` and landmine call at `0x772124F–0x77212F0` read the same five constants: S=100 (`0x9AC21F0`), R=1000 (`0x9AADAE8`), m=30 (`0x9AD4830`), E=500 (`0x9BD1C74`), F=0.5 (`0x9AC3D40`). The independently disassembled `0x6BB9850` stores those parameters at struct `+0/+4/+8/+0xC/+0x10`. Frag's fresh CDO overrides only m=10/F=1 among those values; grenade constructor `0x6CADC90` calls the base at `0x6CADCAA` without replacing them. Claymore omits m/F, and AT mine omits F, so their inherited values in the fixture are correct. C4 explicitly supplies all five values. The IED class's JSON `Super` points to `B_ThrowableC4_C`; its CDO overrides S/R/E/m to 300/800/400/60 and omits F, correctly inheriting C4's 1.

Frag's two distinct tags are also confirmed: `0x6CADD8A–0x6CADD96` supplies global `0xD36A728` to the component tag setter, while `0x6CADD9B–0x6CADDA9` stores global `0xD36A488` as actor DamageTag. Their initializer string references at `0x127A8EB` and `0x127A7AB` resolve directly in the original executable to `Meta.Damage.Grenade` and `Meta.Damage.Explosive.Rocket.60mm`, respectively. Frag's fresh CDO overrides neither.

The empty initial component context is backed by native construction, rather than inferred only from omitted JSON. `0x6B18C80` zeroes entity storage at component `+0xE0/+0xF0/+0x100`, then copies default container `0xD269300` into context `+0xE8` at `0x6B18CED`. That original-executable 32-byte container is zero, including explicit-tag Num at `+8` and cached-parent Num at `+0x18`. Copy helper `0x3955370` resets destination counts and copies only source counts. Narrow corpus checks found the two low-address static-initializer references (`0x12E5840`, `0x151F880`) copying this container as a source into other globals; no destination-form reference was found. Native C4/grenade constructor changes use `0x6B18E70`, independently confirmed to write only source root `+0xE0`; the Molotov constructor chain adds no component-context write. All six fresh damage-component exports serialize either a root-tag override only or no override (frag), with no Context override.

Native blast construction copies that component context, then appends actor DamageTag (`0x6CA8DDD–0x6CA8E1F`) and supplies Explosive type at radial call `0x6CA91ED`. Independent reads of the mine/Claymore Blueprint listings confirm their distinct supplied type tags: ATMine's own tag versus DamageType.Explosive. Thus the fixture lists match the explicit default contexts before the dynamic Inner/Outer addition. This is a class-default/native-path result; external runtime mutations are not excluded.

Source SHA-256 values were computed locally during this independent check. Fresh JSON files remain in `E:/Reverse_Engineer/wardogs_analysis/round8_explosives_20261018`; only hashes and findings are recorded here.

| Source | SHA-256 |
|---|---|
| Original restored executable | `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37` |
| `B_FragGrenade.json` | `010e15972a86a24bdd27bdb9eff7257537430d3dd8b4b7f28fc97131f63524e4` |
| `B_ThrowableC4.json` | `88f47bae96b0f78ba29bda7d5b25f02375a9139d323221e87b1a1bac59985c1c` |
| `B_ThrowableIED.json` | `06a41b8ae99ef4e0fdf1719a630dbae3ff5908ad7ae2ea4cf656afee089a4ce6` |
| `B_AT_Mine.json` | `d97b88847e1af368ae55b44c3aa958581e5e08f823d5620c77209ee3396c6b0c` |
| `B_Claymore.json` | `342ee0b221ca985e1c2afe94bc8c48135deb147e3cf8c69b0b3b93e183addeeb` |
| `B_Molotov.json` | `c7ba5f8f8d2ad3e4c252bf4a938e70332f376b9e19272680c8fa8dbc17d89c08` |
