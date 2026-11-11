# Round 93: stale landing-dip statement (G7)

## Question and disposition

The Status Effects wiki attributed an approximately 0.6 second weapon dip to landing. The maintained Player Movement reference instead associates [`CRV_LandGunBob`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_LandGunBob.json) with `WalkGunBobRotation` and leaves the final animation consumer unresolved.

**Disposition: corrected documentation claim; not full reconstruction of gun-bob behavior.** The wiki now distinguishes landing sway from the unrelated curve's key range and links the reference. It no longer assigns that range to a landing-dip duration.

## Source identity

- Document baseline: public `db8172c4306af86e1373b29ab2f4df10430fe08f`, build `++Wardogs+Live-CL-516586`.
- Native corpus identity and caveats: [Decompilation corpus](../DECOMPILATION_CORPUS.md); source executable SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
- Existing local cooked export: `round40_med/pw/B_WDMoverPlayerCharacter.json` (historical round path, now retained under the private workspace's organized rounds). SHA-256 `f36bbf5c1977cf6044f73589b9344747d0e0c871f07f5bd9f4ea0f627e7ec312`.
- Published [curve export](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Player/PlayerCharacter/Curves/CRV_LandGunBob.json), SHA-256 `88b9fc547bb99a17cdef4ec617defc24605d4047df1f1de2439a5e44228b9035`.

## Asset observations rechecked

The existing cooked export's `Default__B_WDMoverPlayerCharacter_C` properties assign `WalkGunBobRotation` to `/Game/GameMechanics/Player/PlayerCharacter/Curves/CRV_LandGunBob.0`. There is no serialized `JumpLandGunBob` override in that class default. Absence of an override alone does not establish the inherited value or all run-time behavior.

The curve's authored Z property has keys at 0, 0.123736 and 0.586312, with values 0, -4.816915 and 0.002061. Those data establish keys and their range, not when an animation evaluates the curve or the units of its output. The asset name is not proof of a landing trigger.

This agrees with [Round 92, section 4](round92-movement-camera.md#4-crv_landgunbob-still-open), which found no native reader of the relevant pawn fields in its examined consumer searches and explicitly withdrew the landing interpretation. This pass independently re-read the asset assignment and keys; it does not present that earlier native-search scope as a new exhaustive proof.

## Verification

- Parsed the retained export stream with JSON records separated at `--- export:` headers; found the named class default and exact property assignment.
- Parsed the published curve export and re-read its authored keys; computed both asset hashes from the retained file bytes.
- Added a narrow prose regression guard in `tests/test_verification_claims.py`. It failed on the original wiki assertion (one failure, exit 1) and passed after the correction (one test, exit 0).
- No target was executed, no memory was acquired, and no runtime timing was measured.

## Remaining boundary

The final animation/Blueprint consumer, its input clock and output unit remain unresolved. Only `IKFootTrace` contains a `ScriptBytecode` payload in the retained pawn export; that export therefore does not provide a complete animation-graph reconstruction. Closing the stale public claim is not evidence that all gun-bob behavior is known.
