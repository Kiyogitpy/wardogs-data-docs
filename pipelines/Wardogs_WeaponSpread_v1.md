---
title: "Weapon Spread, Accuracy and Shot Direction"
redirect_from: ["/Wardogs_WeaponSpread_v1.html", "/Wardogs_WeaponSpread_v1"]
parent: "Damage & Combat Systems"
description: "How each shot's direction is derived from the aim: zeroing, accuracy cone, movement-driven hip spread, the random cone, shotgun pellets, replication and recoil order"
---

# Wardogs — Weapon spread, accuracy and shot direction

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

How the firing direction of one shot is derived from the player's aim: where the
aim comes from, the zeroing tilt, the cone angle (accuracy plus movement-driven
hip spread), how a random point in that cone is drawn, how shotgun pellets are
placed, what the server receives, and whether recoil is applied before or after.

**Short answer.**

- The shot starts from the **view rotation** at the muzzle position (§3). A **zeroing pitch** is added (§4).
- A **cone half-angle** is added around that direction: `0.5 × accuracy angle` (a few hundredths of a degree) plus a **hip spread** of 1 to 7 degrees that depends on stance and speed and is exactly **0 when the aim blend is 1.0** (fully aimed) (§5, §6).
- The direction is drawn with the engine's `FRandomStream::VRandCone` (an elliptical-cone routine; here a circle), seeded fresh for every shot from the C runtime `rand()` (§7).
- The result is **rounded to 16-bit pitch and yaw** and packed into a fire record; only the shotgun record carries a seed (§9).
- **No per-shot bloom exists in the spread state.** The spread value only follows movement, stance, air and aim blend, smoothed at 25 per second (§6). Firing does not raise it.
- Recoil is applied **after** the projectile is spawned, so a shot is not moved by its own kick; earlier kicks already moved the view and are part of the aim (§10).

Build: `++Wardogs+Live-CL-516586` · Engine: UE 5.7 · Native addresses are file
RVAs (image base `0x140000000`).

**Evidence level: static-analysis image; virtualized dispatch not removed.**
Everything below was read with capstone and pefile from the flat executables;
the decompilation corpus and the IDA database were not used. The
static-analysis image was byte-compared against the older reference image
(`WardogsClient-Win64-Shipping.restored.exe`) for every function cited (§13):
all are byte-identical except `0x6B956B0` and `0x1670B80`, which begin with a
protection-layer dispatch stub in the analysis image and were read from the
reference image, as
[IDA claim exposure](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/IDA_CLAIM_EXPOSURE.md)
prescribes. No game was run and no process was observed: **no runtime
confirmation exists**. Anything not statically resolvable is labelled open (§14).

| Label | Meaning |
|---|---|
| **Native** | Read from instructions or `.rdata` constants in the executable; RVA cited |
| **Data** | Read from the cooked export under `data/` |
| **SDK** | Class or struct layout from `sdk/raw` |
| **Derived** | Arithmetic on Native and Data facts only |
| **Inferred** | Role deduced from how the code uses a field; not named anywhere |

---

## 1. Summary of the model

For one shot (client side, `0x6B94700`):

```
Q0      = view rotation at the muzzle socket position            (§3)
Z       = ZeroTable[range] + atan2(h, 100·range) · 180/π         degrees, 0 if range ≤ 0   (§4)
Q1      = Q0 ⊗ Quat(Pitch = Z)                                   zeroing, local pitch
F0      = Q1.RotateVector(1,0,0)
θ       = 0.5 · A · Mw · Mc  +  (pellets ≤ 1 ? S·π/180 : 0)      cone half-angle, radians   (§5)
        A  = WeaponAccuracy in radians (MOA × 2.909e-4, mrad × 1e-3)
        Mw = Weapon.AccuracyMultiplier, Mc = Character.WeaponAccuracyMultiplier
        S  = hip spread in degrees, ext+0x3AC                    (§6)
F       = VRandCone(F0, θ)  with a stream seeded by rand()        (§7)
Rot     = quantise16(ToOrientationRotator(F))                    pitch, yaw only   (§8)
```

Hip spread state, updated every tick of the weapon's item extension (`0x6C9FEE0`):

```
x       = clamp(|v_xy| / vref[stance], 0, 1)                     vref = {Prone 50, Crouch 250, Stand 400} cm/s
target  = 0                                      if aim blend == 1.0
        = InAirHipFireSpread (10° default)       if airborne
        = SpreadMultiplier · Value · CT_Weapon_Spread[row(stance)](x)   otherwise
S'      = S + (target − S) · clamp(25·dt, 0, 1)                  (FInterpTo; set to 0 at once when aim blend == 1.0)
```

---

## 2. The stats and data fields

| Field | Where | Offset | Meaning for spread |
|---|---|---|---|
| `WeaponAccuracy.AccuracyType` | `FWDWeaponStats` (SDK `FWDWeaponAccuracy`) | `+0x0` | 0 `MinutesOfAngle`, 1 `Milliradians`. **Native default is 1** (constructor `0x699E6C0`: `mov byte [rcx],1`), so an asset that omits it is in milliradians |
| `WeaponAccuracy.AccuracyValue` | same | `+0x4` | Full cone angle in that unit; default 1.0. Getter `0x6BBD3D0` converts to radians: MOA × `0.000290888`, mrad × `0.001`, other types 0 |
| `RandomDeviationDegree` | same | `+0xCE0` | **Recoil only** (rotates the recoil pattern, §10); not read by the shot-direction code |
| `ShotgunData` | same | `+0xD40` (0x60 bytes) | Pellet pattern (§11) |
| `InitialBulletSpeed` | same | `+0xDA0` | Muzzle speed; getter `0x6BBD500`. Not a spread input |
| `SpreadValues` (stance → `FBHScalableFloat`) | `WDItemExtensionData_RangedWeapon` | `+0xA8` | Hip spread curve per stance: `Value` × row of [`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json) |
| `InAirHipFireSpread` | same | `+0x1DC` | Spread while airborne, degrees. **Native default 10.0** (immediate `0x41200000` stored at `0x6C9102D` in the data constructor); only [`GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) sets it (10.0) |
| `bDoesWeaponUseSpread`, `SpreadValue` | `WDVehicleWeaponExtensionDataAsset` | `+0x88`, `+0x90` | Vehicle weapon extensions: spread = `Value` x curve row at level 0, eased toward at 25 per second by `0x764BED0`, zero in full ADS; stored at actor `+0x440` (§14 item 6) |
| `NumberOfPellets`, `AmmunitionFactor` | `FWDProjectileStats` in the projectile data | `+0x18C`, `+0x190` | Pellet count and a choke scale |
| `MaxPelletCount` | `UWDGameSettings.ProjectileSystemSettings` | settings `+0x5E4` | Pellet normaliser (§11); value not in the export |
| `Attribute.Gameplay.Weapon.SpreadMultiplier` | weapon item attributes | tag global `0xD36EBB0` | Multiplies the hip spread target |
| `Attribute.Gameplay.Weapon.AccuracyMultiplier` | weapon item attributes | tag global `0xD36EBB8` | Multiplies the accuracy cone |
| `Attribute.Gameplay.Character.WeaponAccuracyMultiplier` | character attributes | tag global `0xD37E8C0` | Multiplies the accuracy cone |
| `Attribute.Gameplay.Weapon.Length` | weapon item attributes | tag global `0xD36EBC0` | Not a spread input (interface slot `+0xC8`, default 80) |

Tag strings were read from the static initialisers that load them at `0x12AB10B` (AccuracyMultiplier),
`0x12AB56B` (SpreadMultiplier), `0x12AB6AB` (Length) and `0x12CB33B` (WeaponAccuracyMultiplier).

---

## 3. Where the aim comes from

**Native.** `UWDWeaponComponent` vtable slot `+0x578` is start-fire (`0x6B980A0`),
which arms the timer whose body is `0x6B94700` (`Timer_FireWeapon`). That body asks the
`IWDWeaponOwner` interface (obtained from the component's outer through `0x1921820`) for the
projectile spawn transform:

- For a held weapon the owner is `UWDItemExtension_RangedWeapon`; its interface sits at ext `+0xF0` with vtable `0xB389AB8`. Slot `+0x18` is `GetProjectileSpawnTransform` = `0x6C987A0`. It takes the **muzzle socket world transform** (`0x6C97DD0`) and, when the owning character passes a predicate (`0x6E70B10`; Inferred: locally controlled), **replaces its rotation with the character's view rotation** (character virtual `+0x840`, then `FRotator::Quaternion` `0x166D220`). Translation and scale stay those of the socket.
- Slot `+0x20` (`GetProjectileSpawnTransforms`, array) is the empty-array stub `0x15B8F80` for a held weapon, so `0x6B94700` takes the single-transform branch (`0x6B90780`, which post-processes the transform with `0x6B90890`, a function that includes a trace; not decoded, §14). A weapon that returns several transforms (vehicle weapons) rolls an independent cone for each, with its own `rand()` seed, but the same half-angle.

So the aim direction is the **camera/view rotation at the moment the timer fires**. Because the view
rotation is where recoil is applied (§10), earlier kicks are already in it.

---

## 4. Zeroing tilt

**Native** (`0x6B90610`, called from `0x6B94700` with the spawn transform):

```
base = ZeroTable[ComponentZeroingRange]                    0x6B956B0, TMap<int32,float> at component +0xFF8
if range ≤ 0: return base                                  range at component +0xF8C, constructor value −1
h    = (EyePoint − transform.Translation) · transform.UpVector
Z    = base + atan2(h, 100·range) · 57.29578               atan2 = 0x15AE590
```

`EyePoint` is the first output of a character virtual (`+0x720`) and the check `0x6E70B70` must pass;
otherwise `Z = base`. **Inferred:** `h` is the height of the eye above the bore along the muzzle's up axis (cm),
so the bore is tilted up by the angle at which the bullet's straight line meets the sight line at `range` metres.
The rotation is composed as `Q1 = Q0 ⊗ Quat(Pitch=Z)` (Hamilton product with the spawn rotation first; read from the
shuffle sequence at `0x6B94AD4`–`0x6B94B84`), so `Z` is a pitch about the weapon's own right axis. How `ZeroTable` is filled is open (§14);
`0x6B956B0` is the function that begins with a dispatch stub in the analysis image and was read from the reference image.

---

## 5. The cone half-angle

**Native** (`0x6B94BB9`–`0x6B94C14`):

```
accuracy_rad = 0x6BBD3D0(stats at component +0x140)             (§2)
mult         = 0x6C974E0 = Weapon.AccuracyMultiplier (default 1) × Character.WeaponAccuracyMultiplier (default 1)
cone_acc     = 0x6B95630 = accuracy_rad × mult                  (interface slot +0xC0 supplies mult)
S_deg        = interface slot +0xA8 = GetSpreadAngle            (0x3CD6240: movss xmm0,[this+0x2BC] = ext +0x3AC)
θ            = 0.5 · cone_acc  +  (NumberOfPellets > 1 ? 0 : S_deg · 0.0174533)
```

`NumberOfPellets` is read from the projectile data's stats (`0x6BBA900` returns the possibly ammo-modified
`FWDProjectileStats`; `+0x18C`). **A multi-pellet round ignores the hip spread curve completely**; its spread comes from `ShotgunData` (§11).
The accuracy angle is treated as a full cone angle (the `0.5` turns it into a half-angle); the spread is already a half-angle.
While that listener list is non-empty, `θ` is also stored in degrees in the per-shot result at frame `+0x270` as `max(0, 0.5·accuracy_deg + S_deg)`
(`0x6B93FD7`–`0x6B9408A`); its consumer is not traced (§14).

**Data.** Accuracy half-angles run from 0.003 degrees (SR_04; the bow is 0) to 0.57 degrees (MMGL); a typical rifle is 0.02 to 0.04 degrees
(table in §12). The only cooked effect on either accuracy multiplier is `GE_MMGL_RotaryPassengerSway`
(`Character.WeaponAccuracyMultiplier` ×c 2.5). No cooked effect changes `Weapon.AccuracyMultiplier`.

---

## 6. Hip spread state: movement, stance, air, aim blend

**Native.** `UWDItemExtension_RangedWeapon` has a virtual `Tick(float)` (primary vtable `0xB389290`, slot `+0x6D0` = `0x6C9E7D0`). After the base tick (`0x3CB6400`) it calls
`UpdateSpread` = **`0x6C9FEE0`** with `dt` in `xmm1`. Steps:

1. Resolve the owning character (`0x675CDB0`); return if it is invalid or its virtual `+0x818` is false (a predicate on the machine that simulates the weapon; name open).
2. Fetch the ranged-weapon data asset (`0x4BD0D20`).
3. **Aim blend.** `0x6E6E260` returns the weapon behaviour component's aim blend (`+0x3E4`, read by `0x6B86240`; the blend that [Weapons §5b](../content/Wardogs_Weapons_v2.md) describes). If it **equals 1.0 exactly** (`ucomiss` / `je`), spread is set to **0** at once (`0x6CA01A8`) and nothing else is evaluated. A partly aimed weapon (0 < blend < 1) is treated as hip fire at full value.
4. **Airborne** (`0x5296290`: mover component virtual `+0xD8`): `target = data.InAirHipFireSpread` (`+0x1DC`). **`SpreadMultiplier` is not applied** on this path.
5. Otherwise, **grounded**:
   - `stance` = `0x5293150`: the mover's stance byte (`Prone 0`, `Crouch 1`, `Stand 2`; value 3 maps to 2; 2 if no mover).
   - `v` = length of the 2D velocity returned by character virtual `+0x360`.
   - `vref` = `{50, 250, 400}[stance]` (cm/s). The three floats `0x42480000`, `0x437A0000`, `0x43C80000` are stored by the static initialiser at `0x6CA01F7` into an array whose pointer is at `0xCEC1528` (count at `0xCEC1530`); an index of 3 or more uses 400. If `|vref| ≤ 1e-8` the ratio is 0 or 1 by comparison.
   - `x = clamp(v / vref, 0, 1)`.
   - `curve = SpreadValues[stance].GetValueAtLevel(x)` = `Value × CT_Weapon_Spread[row](x)` (`FBHScalableFloat` `0x48AA830`; every cooked `Value` is 1.0). Stored at ext `+0x3B0`.
   - `target = SpreadMultiplier × curve` (`0x6C97710`: attribute `0xD36EBB0`, default 1.0 when the item has no attribute container). Stored back at ext `+0x3B0`.
6. `S' = FInterpTo(S, target, dt, 25.0)` (`0x5384040`; the `25.0` constant is `0x41C80000` at `0x9BAB148`):
   `S' = S + (target − S) · clamp(25·dt, 0, 1)`. A step of 1/60 s closes 41.7 % of the gap; the time constant is 0.04 s. Stored at ext `+0x3AC`.

The two stored values (`+0x3AC` current, `+0x3B0` target) are also copied, with `+0x378`, into a state record by the function at `0x6C9DB60` (a prediction/sync snapshot; Inferred).
**Quirk (Derived):** if the stance has no entry in `SpreadValues`, step 5 skips the lookup, so `+0x3B0` keeps its previous value and is multiplied by `SpreadMultiplier` again every tick. All 37 weapons have all three stances, so this is not reached in the shipped data.

**Not found.** Nothing in this routine reads the stamina, suppression, damage-taken or fire state, and nothing in the item-extension code
range (`0x6C80000`–`0x6CA2000`) other than `UpdateSpread` writes `+0x3AC`/`+0x3B0`. In particular **there is no per-shot bloom and no recovery
timer**: after the last shot the value is already at its movement target, and it moves only when speed, stance, air or aim blend change (§14 for the limits of this scan).
The one cooked path from combat state into the cone is an effect on `Character.WeaponAccuracyMultiplier` (§5).

### Hip spread curves ([`CT_Weapon_Spread`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json), degrees, X = speed ratio 0 → 1, linear)

| Class | Stand | Crouch | Prone |
|---|---|---|---|
| AR, DMR, LMG, Pistol, Shotgun | 3 → 6 | 2 → 4 | 1.5 → 3 (AR) or 1 → 2 (others) |
| SMG, Launcher | 2 → 4 | 1.5 → 3 | 1 → 2 |
| Sniper | 4 → 7 | 3 → 6 | 2 → 4 |
| Bow | 1 → 2 | 0.5 → 1 | 0.5 → 0.5 |
| MountedMachineGun | 1 → 2 (single row) | | |
| StableMountedMachineGun | 0.5 → 1 (single row) | | |

Source: [`CT_Weapon_Spread.json`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Weapons/Curves/CT_Weapon_Spread.json) (29 rows).
Every infantry weapon uses its own class for all three stances (§12). The PKM ([`LMG_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/LMG_02.json)) uses the Sniper rows.

---

## 7. The random distribution

**Native** (`0x3FD4FA0`, called at `0x6B94C3C`). This is the engine routine
`FRandomStream::VRandCone(Dir, HorizontalHalfAngle, VerticalHalfAngle)`, called with both angles equal to `θ`:

```
Seed'  = Seed · 196314165 + 907633515  (mod 2^32)         constants 0x0BB38435, 0x3619636B
FRand  = float((Seed' >> 9) | 0x3F800000) − 1.0            uniform in [0, 1)
U = FRand;  V = FRand                                      two draws, U first
Theta  = 2π · U
Phi0   = acos(clamp(2V − 1, −1, 1))
Cone   = sqrt(1 / ((sin Theta / H)² + (cos Theta / Vt)²))  = θ for H = Vt = θ
Phi    = fmod(Phi0, Cone)                                  0x15B50A0
R1     = Dir rotated by Phi° about DirRight (0x16706F0, Phi × 57.29578)
Result = normalise(R1 rotated by Theta° about Dir)         (Theta° = U × 360)
```

If `θ ≤ 0` the routine returns `Dir` normalised (`0x3FD52F5`), so a weapon with zero accuracy and zero hip spread (the bow when aimed) fires exactly along `F0`.

**Derived distribution.** `Phi0` is uniform on the sphere, and the `fmod` folds it into `[0, θ)`. For the small `θ` used here (≤ 7 degrees, a fold count above 25) the folded density is flat to better than 0.1 %: **the radius from the aim point is uniform in angle, not in area.** The probability of landing within angle `r` is `r/θ`; half of all shots land inside `θ/2`, which is a quarter of the cone's area. The pattern is centre-heavy (area density ∝ 1/r), not a uniform disc and not Gaussian. There is no rejection sampling.

**RNG and seed.** The stream is a local `FRandomStream` (`InitialSeed` and `Seed` at `+0`/`+4`) created inside `0x6B94700` and filled with one value of the C runtime `rand()` (`ucrtbase!rand` through the IAT slot `0x9A28EC8`; `0x6B94B89`), **a new seed for every shot** (and for every muzzle transform). `srand` has a single direct call site (`0x46CF6E8`), so the game thread's `rand()` state is seeded once at start-up (the seed value is not traced; open). The stream is not an engine global, is not derived from the shot id, and is not shared between shots.
Recoil uses the same CRT `rand()` ([Weapons §5a](../content/Wardogs_Weapons_v2.md)), so the two draws are not correlated by design.

---

## 8. Quantisation and the final direction

**Native** (`0x6B94C41`–`0x6B94C59`, `0x6B93610`):

- `F` (a vector) → `FVector::ToOrientationRotator` (`0x1676A00`): `Pitch = atan2(z, √(x²+y²))`, `Yaw = atan2(y, x)`, in degrees, **roll 0**. `0x1676910` (`ToOrientationQuat`) rebuilds the quaternion `Q` for the next muzzle.
- `0x76DFB20` compresses the rotator: each of pitch and yaw becomes `RoundToInt(angle × 65536/360) & 0xFFFF`; yaw is the high 16 bits, pitch the low 16 bits. `0x76E0810` decompresses it (`× 0.0054931640625`). The shot is then fired **with the decompressed rotator**, so the client and the server use the same, quantised direction.
- The angular step is 360/65536 = **0.00549 degrees (0.096 mrad)**. This is comparable to the accuracy half-angle of the most precise weapons (0.003 to 0.02 degrees), so for aimed shots the quantisation noise is of the same size as the accuracy cone.
- The projectile subsystem builds the velocity as `Rotator.Vector() × speed` (`0x6F1DDC0`: `0x16793E0` then a multiply by the speed from `0x6BBD500`). The spawn wrapper `0x6B96580` receives `InitialBulletSpeed × component+0x114` (`0x6B959E0`; `+0x114` is 1.0 from the constructor `0x6B8E5A0`). Where that factor is applied is open (§14). Flight after launch is in [Projectile flight](Wardogs_ProjectileFlight_v1.md).

---

## 9. Client, server and replication

**Native.**

- The client path is `0x6B94700` (compose direction, `rand()` seed) → `0x6B93610(component, shotId, &location, &rotator, seed, …)`. `shotId` is a process-wide counter incremented by `0x76E0800`.
- `0x6B93610` is shared by client and server. It quantises the rotator (§8), spawns the projectile(s) through `0x6B96580`, appends a **0x28-byte record** to the outgoing list, then (for a local controller) computes and queues the recoil kick (`0x6B95C50`, §10). Record layout, read from the two writers and the two server readers: `+0x00` location (3 doubles), `+0x18` packed rotator (u32), `+0x1C` pellet seed (i32, **−1 if the round has one projectile**), `+0x20` shot id (u32), `+0x24` flag (u8).
- RPCs: `Server_FireProjectile(uint32 firingSequence, uint16, FAutoProxyFixedTickInfo, TArray<record>)` (exec `0x6B996D0`, implementation vtable `+0x510` = `0x6B97900`) and `Server_FireBuckshotProjectile` (exec `0x6B99530`, implementation `0x6B97820`). Both first call `0x3CAB0A0` (a check on the component at `+0xC8`; not decoded) and take the refuse path `0x6B92180` when it is non-zero. Each record is decompressed (`0x76E0810`) and passed to `0x6B93610`: **`0x6B97900` passes seed −1; `0x6B97820` passes the record's `+0x1C` seed.**
- `UpdateSpread` is gated by the character predicate in §6 step 1. `0x6B93610` reads `GetSpreadAngle` again only to fill the `+0x270` echo (§5), and only while a global listener list (`0xCEB6D70`) is non-empty.

---

## 10. Interaction with recoil

**Native.** In `0x6B93610` the order is: build the transform → (client) cone → quantise → **spawn** (`0x6B96580`) → **recoil** (`0x6B95C50`, only for a local `WDPlayerController`, `0x6B96C20`). The kick is queued and applied to the view over the following frames by the tick ([Weapons §5a](../content/Wardogs_Weapons_v2.md)).

- A shot is fired along the view as it is **before** its own kick. Kicks from earlier shots are already added to the control rotation, so recoil moves the **centre** of the next cone; it does not change the cone size.
- Recoil does not feed the spread state: `UpdateSpread` never reads it, and `RandomDeviationDegree` is a recoil field (the angle by which a recoil-pattern point is rotated), not a bullet-dispersion field.
- Whether the aim-sway offset (`WeaponBehaviorComponent` aim sway) is part of the view rotation read at `0x6C98834` is open (§14). The cooked sway effects (`Character.AimSway*`, `WeaponSway.*`) are separate attributes and do not touch the accuracy attributes.

---

## 11. Multi-pellet rounds (shotgun)

**Native.** When `NumberOfPellets > 1` (`0x6B93BDB`, `0x6B940C1`), `0x6B93610` copies `ShotgunData` (`0x6BBD5D0`: stats `+0xD40`), replaces it by an attachment-supplied copy if `0x6B98980` returns one (a choke attachment; Inferred), and calls the pellet generator **`0x6C25660`**(out array, aim direction, ShotgunData, `N`, `AmmunitionFactor`, seed). The aim direction is the one from §5 (a tiny accuracy cone, no hip spread). The generator is deterministic given the seed:

```
Seed0 = seed;   stream: Seed' = Seed·196314165 + 907633515,  FRand = float((Seed'>>9)|0x3F800000) − 1
A, B     = outer half-angles (deg): bSeparateOuterConeHalfAngles ? (OuterConeHorizontalHalfAngle, OuterConeVerticalHalfAngle)
                                                                 : (OuterConeHalfAngle, OuterConeHalfAngle)
I        = InnerConeHalfAngleMultiplier
(Rh, Rv) = per-shot random limits: bSeparateRandomConeHalfAnglesRanges ? (lerp(HRange, r2), lerp(VRange, r1))
                                                                     : (lerp(Range, r1), same value)       lerp(range, r) = min + (max − min)·r
Centre   = VRandCone(Dir, min(A(1−I), Rh)·π/180, min(B(1−I), Rv)·π/180)          one centre per shot
P        = clamp(N / MaxPelletCount, 0, 1) · AmmunitionFactor · ChokeFactor
for each of N pellets:
    r = FRand
    if r > P :  pellet = VRandCone(Dir,    A·π/180,   B·π/180)                    outer pellet
    else     :  pellet = VRandCone(Centre, I·A·π/180, I·B·π/180)                  inner (choked) pellet
```

`MaxPelletCount` is `UWDGameSettings.ProjectileSystemSettings` `+0x18C` (settings `+0x5E4`, read through `0x6C03540`); its value is **16** (packed `DefaultGame.ini`, [Hit Registration §4.6](Wardogs_HitRegistration_v1.md)). With `N` = 8 pellets (7mm Buckshot) and `AmmunitionFactor` 0.8: M500 `P` = 0.5 x 0.8 x 0.5 = **0.20**, MP43 `P` = 0.5 x 0.8 x 0.35 = **0.14**. The M500 choke attachments carry their own `ShotgunData` (`bOverrideShotgunData` true): Improved Cylinder Choke ([`ID_MUZL_044`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_044/Content/Data/ID_MUZL_044.json)) choke 0.65, outer half-angle 1.36 degrees, random limit 0 to 1.75, inner multiplier 0.55, so `P` = 0.26; Full Choke ([`ID_MUZL_045`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Attachments/Muzzle/MUZL_045/Content/Data/ID_MUZL_045.json)) choke 0.85, outer 0.95 degrees, random limit 0 to 1.55, inner multiplier 0.6, so `P` = 0.34. The 54 other muzzle devices that have the field set it to false. The inner cone always fits inside the outer cone, because the centre may move only `A(1−I)`.
Each pellet then goes to `0x6B96580` with speed `InitialBulletSpeed × component+0x114`; the id of every spawned pellet is collected for the RPC.

**Data.** Native defaults (constructor `0x699E6C0`): `ChokeFactor` 0.8, outer half-angle 10 degrees (horizontal and vertical 10), inner multiplier 0.5, random ranges (0, 0). `7mm Buckshot` has `NumberOfPellets` 8 and `AmmunitionFactor` 0.8; the rifled slug has no pellet count (one projectile). Cooked shotguns are in §12: M500 ([`DA_M12G_Stats`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_011/Content/Data/DA_M12G_Stats.json): choke 0.5, outer 1.56 degrees, random limit 0 to 2 degrees, inner multiplier default 0.5) and MP43 (choke 0.35, outer 1.85 degrees, random limit 0 to 3, inner 0.6). The Judge has no `ShotgunData` block, so it uses the defaults if its ammunition has more than one pellet.

---

## 12. The cooked values per weapon

Generated by [`_tools/spread_table.py`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/_tools/spread_table.py) from `data/`
(`python _tools/spread_table.py --write`). `†` marks a value the asset omits, taken from the native default
(the accuracy **unit** is the omitted field and the value is cooked; [`GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) and [`Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Launcher_04.json) have no `WeaponAccuracy` block, so both unit and value are the defaults, 1 mrad). Hip half-angle is `S` before
`SpreadMultiplier`; the cone also carries the accuracy half-angle (column 3). Attachment multipliers are not applied.

<!-- spread_table -->
| Weapon | Accuracy | Accuracy half-angle (°) | Curve class | Hip half-angle, Stand: still → full speed (°) | Crouch | Prone | Shotgun data |
|---|---|---:|---|---|---|---|---|
| `A91` | 1.5 mrad† | 0.0430 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| `AK74M` | 0.825 mrad† | 0.0236 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| `CGM4` | 2.5 mrad† | 0.0716 | Launcher | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`CombatBow`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/CombatBow.json) | 0 mrad† | 0.0000 | Bow | 1 → 2 | 0.5 → 1 | 0.5 → 0.5 | — |
| `Glock17` | 3.49 mrad† | 0.1000 | Pistol | 3 → 6 | 2 → 4 | 1 → 2 | — |
| [`GrenadeLauncher`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/UnderbarrelGrenadeLauncher/Content/Data/GrenadeLauncher.json) | 1 mrad† | 0.0286 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| `Judge` | 3.49 mrad† | 0.1000 | Pistol | 3 → 6 | 2 → 4 | 1 → 2 | — |
| `KH2002` | 1.5 mrad† | 0.0430 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| [`Launcher_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/Launcher_04/Content/Launcher_04.json) | 1 mrad† | 0.0286 | Launcher | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`LMG_02`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/LMG/LMG_02/Content/LMG_02.json) | 2.5 mrad† | 0.0716 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | — |
| `M249` | 4.3 mrad† | 0.1232 | LMG | 3 → 6 | 2 → 4 | 1 → 2 | — |
| `M4` | 0.84 mrad† | 0.0241 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| `M500` | 1.5 mrad† | 0.0430 | Shotgun | 3 → 6 | 2 → 4 | 1 → 2 | choke 0.5, outer 1.56°, inner ×0.5, centre jitter 0…2° |
| [`MK22`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/MK22/Content/MK22.json) | 0.16 mrad† | 0.0046 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | — |
| `MMGL` | 20 mrad† | 0.5730 | Launcher | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`MP43`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Shotgun/MP43/Content/MP43.json) | 3.08 mrad† | 0.0882 | Shotgun | 3 → 6 | 2 → 4 | 1 → 2 | choke 0.35, outer 1.85°, inner ×0.6, centre jitter 0…3° |
| [`MP9`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/MP9/Content/MP9.json) | 2.1 mrad† | 0.0602 | SMG | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`RFB`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/RFB/Content/RFB.json) | 0.69 mrad† | 0.0198 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| [`RPG7`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Launchers/RPG7/Content/RPG7.json) | 3 mrad† | 0.0859 | Launcher | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| `SKS` | 0.73 MOA | 0.0061 | DMR | 3 → 6 | 2 → 4 | 1 → 2 | — |
| [`SMG_03`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/SMG/SMG_03/Content/SMG_03.json) | 1.3 mrad† | 0.0372 | SMG | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`SR_04`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Sniper/SR_04/Content/SR_04.json) | 0.11 mrad† | 0.0032 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | — |
| `SV98` | 0.56 mrad† | 0.0160 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | — |
| [`SVDM`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/DMR/SVDM/Content/SVDM.json) | 0.45 mrad† | 0.0129 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | zeroed (choke 0, outer 0) |
| `TAR21` | 0.87 mrad† | 0.0249 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| `Vector` | 2 mrad† | 0.0573 | SMG | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`WEPN_017`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_017/Content/WEPN_017.json) | 0.78 mrad† | 0.0223 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | — |
| [`WEPN_026`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_026/Content/WEPN_026.json) | 2 mrad† | 0.0573 | Pistol | 3 → 6 | 2 → 4 | 1 → 2 | — |
| [`WEPN_027`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_027/Content/WEPN_027.json) | 0.84 MOA | 0.0070 | Pistol | 3 → 6 | 2 → 4 | 1 → 2 | — |
| [`WEPN_028`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_028/Content/WEPN_028.json) | 1.16 mrad† | 0.0332 | SMG | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`WEPN_029`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_029/Content/WEPN_029.json) | 0.73 mrad† | 0.0209 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| [`WEPN_030`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_030/Content/WEPN_030.json) | 0.58 mrad† | 0.0166 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| [`WEPN_031`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_031/Content/WEPN_031.json) | 1.3 mrad† | 0.0372 | SMG | 2 → 4 | 1.5 → 3 | 1 → 2 | — |
| [`WEPN_032`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_032/Content/WEPN_032.json) | 2 mrad† | 0.0573 | Pistol | 3 → 6 | 2 → 4 | 1 → 2 | — |
| [`WEPN_033`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_033/Content/WEPN_033.json) | 1.5 mrad† | 0.0430 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| [`WEPN_034`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_034/Content/WEPN_034.json) | 0.73 mrad† | 0.0209 | DMR | 3 → 6 | 2 → 4 | 1 → 2 | zeroed (choke 0, outer 0) |
| [`WEPN_035`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_035/Content/WEPN_035.json) | 1.5 mrad† | 0.0430 | Sniper | 4 → 7 | 3 → 6 | 2 → 4 | — |
| [`WEPN_036`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_036/Content/WEPN_036.json) | 0.73 mrad† | 0.0209 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | — |
| [`WEPN_037`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Weapons/Platforms/WEPN_037/Content/WEPN_037.json) | 0.58 mrad† | 0.0166 | AR | 3 → 6 | 2 → 4 | 1.5 → 3 | zeroed (choke 0, outer 0) |
<!-- /spread_table -->

**Worked example.** AK74M (`0.825 mrad†`, class AR), standing, no attachments, moving at 200 cm/s:
`x = 200/400 = 0.5`, `S = 3 + 0.5·(6−3) = 4.5` degrees, accuracy half-angle `0.5·0.825e-3 rad = 0.0236` degrees, so
`θ = 4.52` degrees; at 100 m the radius of the cone is `100 m · tan 4.52° ≈ 7.9 m`, and half of the shots land within about 3.9 m. Standing still it is `3.02` degrees. With the grip `GE_FGP_02`
(`SpreadMultiplier` ×c 0.83) moving: `4.5 · 0.83 = 3.74` degrees. Fully aimed (aim blend 1.0): `θ = 0.0236` degrees, which is about 4 quantisation steps (§8): about 4 cm at 100 m.
A bipod-mounted `GE_FGP_04_BipodState` weapon: ×c 0.45; unfolded: ×c 1.15.

### Modifier summary (Data: [GE values](Wardogs_GameplayEffect_Values_v1.md), 341 cooked effects)

| Attribute | Cooked modifiers | Operation | Range |
|---|---|---|---|
| `Weapon.SpreadMultiplier` | 92 (foregrips, muzzle devices, bipod states) | MultiplyCompound | 0.45 (bipod mounted) to 1.15 (bipod unfolded); muzzle devices 0.88 to 0.99; foregrips 0.76 to 0.94 |
| `Weapon.AccuracyMultiplier` | 0 | | all weapons at the base value 1 |
| `Character.WeaponAccuracyMultiplier` | 1 (`GE_MMGL_RotaryPassengerSway`) | MultiplyCompound | ×2.5 |
| Stamina, suppression, damage taken | no modifier reaches spread or accuracy | | |

The stance multipliers inside `StanceGameplayEffects` act on recoil, not on spread ([Weapons §5a](../content/Wardogs_Weapons_v2.md)); the stance enters the spread only through the `SpreadValues` row (§6).
Final per-weapon attribute values are on [Weapon Attributes](../content/Wardogs_WeaponAttributes_v1.md).

---

## 13. Function table

All RVAs are file RVAs. "Same" means byte-identical in the static-analysis image.

| RVA | Role | Analysis image |
|---|---|---|
| `0x6B980A0` | `UWDWeaponComponent` start-fire (vtable `+0x578`) | same |
| `0x6B94700` | `Timer_FireWeapon` body: aim, zeroing, cone, `rand()` seed | same |
| `0x6B93610` | per-shot executor shared by client and server: quantise, spawn, record, recoil | same |
| `0x6B90610` | zeroing angle `Z` | same |
| `0x6B956B0` | `ZeroTable[range]` lookup | **differs**: dispatch stub; read from the reference image |
| `0x6B95630` | accuracy cone `accuracy_rad × mult` | same |
| `0x6B959E0` | `InitialBulletSpeed × component+0x114` | same |
| `0x6B90780`, `0x6B90890` | single-transform branch; transform post-processing (trace; not decoded) | same |
| `0x6BBD3D0` | `FWDWeaponAccuracy` to radians (MOA `0x3998825B`, mrad `0x3A83126F`) | same |
| `0x6BBA900` | projectile stats lookup with ammo modifier tag (cache, entry stride `0x328`) | same |
| `0x6BBD500`, `0x6BBD420`, `0x6BBD5D0` | getters: `InitialBulletSpeed`, `EffectiveRange × 100`, `ShotgunData` | same |
| `0x6C25660` | shotgun pellet generator | same |
| `0x6C9E7D0` | ranged-weapon item extension `Tick` (primary vtable `0xB389290` `+0x6D0`) | same |
| `0x6C9FEE0` | **`UpdateSpread`** | same |
| `0x3CD6240` | `GetSpreadAngle` (interface slot `+0xA8`; also in three other vtables) | same |
| `0x6C974E0` | accuracy multiplier (interface slot `+0xC0`) | same |
| `0x6C987A0` | `GetProjectileSpawnTransform` (interface slot `+0x18`) | same |
| `0x6C98290` | `GetProjectileData` (interface slot `+0x90`) | same |
| `0x6C97710` | item attribute getter with default | same |
| `0x3FD4FA0` | `FRandomStream::VRandCone` (elliptical) | same |
| `0x1670B80` | `FQuat::RotateVector` | **differs**: dispatch stub; read from the reference image |
| `0x1676910`, `0x1676A00` | `ToOrientationQuat`, `ToOrientationRotator` | same |
| `0x16793E0`, `0x166D220` | `FRotator::Vector`, `FRotator::Quaternion` | same |
| `0x76DFB20`, `0x76E0810`, `0x76E0800` | rotator compress, decompress, shot-id counter | same |
| `0x6B97900`, `0x6B97820` | `Server_FireProjectile`, `Server_FireBuckshotProjectile` implementations | same |
| `0x6B996D0`, `0x6B99530` | their exec thunks | same |
| `0x5384040` | `FInterpTo` | same |
| `0x48AA830` | `FBHScalableFloat::GetValueAtLevel` | same |
| `0x6E6E260`, `0x6B86240` | aim blend (`+0x3E4`) | same |
| `0x5296290`, `0x5293150` | airborne test, stance byte | same |
| `0x699E6C0` | `FWDWeaponStats` constructor (defaults) | same |
| `0x6F1DDC0` | velocity from rotator and speed | same |

---

## 14. What is open

1. **`MaxPelletCount`** is 16 (`DefaultGame.ini` `ProjectileSystemSettings`, [Hit Registration §4.6](Wardogs_HitRegistration_v1.md)); resolved in round 39. With 8 pellets and `AmmunitionFactor` 0.8, `P = 8/16 x 0.8 x ChokeFactor` = 0.20 on the M500 (choke 0.5), 0.14 on the MP43 (choke 0.35), 0.26 with the Improved Cylinder Choke and 0.34 with the Full Choke on the M500 (§11).
2. **Aim sway and the shot.** Round 41: closed. Round 40 showed the shot direction is the camera manager's final rotation (character virtual `+0x840` -> controller `GetPlayerViewPoint` `0x42C8890`). The aim-sway code (Weapons v2 §5a step 5) writes the per-frame sway change times `PlayerCameraOffsetMultiplier` into the **controller rotation** (`0x6D54190`) in `Camera` mode, the native default (no cooked weapon sets `AimSwayMode`), so sway **is** in the view rotation and therefore in the shot direction. In `Weapon` mode only the weapon attach-point offset moves (animation), not the aim. `bSpawnProjectileFromCameraWhenAds` is false on 25 stats assets and not set on the rest.
3. **Per-shot bloom.** None found. The negative result covers writers of ext `+0x3AC`/`+0x3B0` in the item-extension code range and the single writer `UpdateSpread`; a store elsewhere in the 100 MB image was not excluded, and Blueprint-driven attribute changes were not traced. Round 41: no bloom-like field exists in the SDK (`WDGame_classes.hpp`, `WDGame_structs.hpp`: no match for bloom, spread increment, per-shot spread or consecutive shots); the only per-shot cooked key found in the weapon and item assets is `FocusEnergyReductionPerShot` (focus energy, not spread); the whole weapon attribute set (`Attribute.Gameplay.Weapon.*`, 12 attributes) has no per-shot term. Treated as **absent**.
4. **Replication details.** Only the wire record layout and seed handling are described here (§9); anything beyond that is not covered.
5. **`ZeroTable`** (component `+0xFF8`). Round 41: the completion callback `0x6B8C8D0` copies the trace result (`0x6B95520` is only the result's copy constructor: success flag `+8`, then a 0x320-byte path record at `+0x20`), and stores `ZeroTable[range] = degrees(atan2(-d, 100 x range))` with `d` the double at result `+0x68` (the path record's field at `+0x48`; read as the vertical offset of the predicted path at that range, in cm, negative when the bullet has dropped; the field name is not resolved). The same `d` is stored as a float in the map at `+0x1048` (keyed by range), and the angle again in the map at `+0x1098`, keyed by the pair (ammunition tag, range) via `0x6B8CA20` and `GetTypeHash`. `atan2` is `0x15AE680`. So the zero angle for a range is the angle of the line from the muzzle to the point where the game's own predicted path lands, which is what a gun needs to be raised by to hit there. Open: which structure holds `d`.
6. **Vehicle and mounted weapons.** Closed in round 42. Both actor classes implement the same weapon-owner interface at actor `+0x2B8`, and `GetSpreadAngle` is its slot 21 (`+0xA8`). `AWDVehicleWeaponExtension`: slot `0x7646C90` returns 0 unless the data asset has `bDoesWeaponUseSpread` (`+0x88`), else the float at actor `+0x440`; the updater `0x764BED0` (every tick, from `0x764A780`) sets it to 0 when the operator's ADS blend (`UWDWeaponBehaviorComponent +0x3E4`) is exactly 1.0, otherwise moves it toward `SpreadValue` (data asset `+0x90`, level 0) by `clamp(dt x 25, 0, 1)` of the gap each tick. `AWDMountedWeapon`: slot 21 is `0x15B83B0` (`return 0.0`), so its native spread is always 0. The infantry updater `0x6C9FEE0` is not theirs. Evidence: [round 42](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round42-weapons.md). Earlier round 41 assumption (float at actor `+0x574`) was wrong.
7. **Character virtuals** `+0x360` (2D velocity), `+0x720` (eye point), `+0x818` (gate), `+0x840` (view rotation) are named by role only.
8. **Frame `+0x270` echo** (`θ` in degrees). Round 41: the loop at `0x6B94480` in the shot function `0x6B93610` calls virtual slot `+0x60` on every registered listener of the global list `0xCEB6D70`, passing the frame; the listeners are registered by **`UWDAnybrainSubsystem`** (list references in `0x6DF3430`, `0x6DF4AB0`, and its vtable slots 87 and 88 `0x6E00470` / `0x6DFEB50`). So the echo is a per-shot report to the Anybrain subsystem, not a gameplay input (the subsystem's purpose was not read). The snapshot `0x6C9DB60` is a block inside the 3 KB function `0x6C9D170`; it packs `+0x360`, `+0x370`, `+0x378`, the stance byte and the two spread values into a record; the consumer of that record was not found.
9. **`component+0x114`** (muzzle-speed scale, default 1.0). Round 40: the only writer is the exposed function `SetInitialBulletSpeedModifier` (`0x6B99A30`); the readers are the spawn wrapper `0x6B959E0` and the shot function `0x6B93610` (`0x6B9412B`). The callers found are the bow actions `B_Action_BowDraw.TryActivateFire` and `B_Action_BowFireTestNew.OnReleased`, which pass `DrawVelocityCurve(draw alpha)`: the [`CombatBow`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/CombatBow.json) curve [`CF_DrawVelocityReleaseCurve`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Items/CombatBow/Content/Data/Curves/CF_DrawVelocityReleaseCurve.json) runs from 0.05 at 0 to 1.0 at 0.4 (`FullDrawTime` 1.4 s). No firearm Blueprint was found calling it.
10. **AI shooters** (`AIWeaponData`, `AEB_EnemyAccuracyScaling`) were not traced; they may use a different direction path. Round 39: `AEB_EnemyAccuracyScaling` is an audio-event behaviour (`EnemyAccuracyScaling_Vehicle` in the vehicle weapon fire events), not an accuracy value. `AIWeaponData` on 12 stats assets holds `MinAIRange`, `MaxAIRange` (150 to 650) and `ShootCountOfBurst` (1 to 8) only; no AI spread value exists ([round 36 AI](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/evidence/round36-ai.md)).
11. **`srand` seed.** Round 41: closed. `0x46CF6AA`-`0x46CF6E8`: unless the command line carries `-Deterministic`, `-UseFixedTimeStep` or `-FixedSeed` (wide strings at `0xA77A640`, `0xA77A660`, `0xA77A68E`), both seeds are `QueryPerformanceCounter` low dwords (IAT `0x9A27628`, two calls): the first goes to the C runtime `srand` (IAT `0x9A28ED0`), the second to the engine seeder `0x15C48B0`. With one of those flags both are the fixed value in `r15d` (the register is zero in the usual start-up; not verified). So the seed is not a constant.
12. **Cooked effects only.** Attribute changes made at runtime by Blueprint or by effects outside the 341 exported ones are not visible.
13. **Runtime check.** Nothing here was observed running; the equations are static readings.

Related: [Weapons §5a recoil](../content/Wardogs_Weapons_v2.md), [Game Features: Weapons](../game-features/Wardogs_GameFeatures_Weapons_v2.md),
[Weapon Attributes](../content/Wardogs_WeaponAttributes_v1.md), [Projectile flight](Wardogs_ProjectileFlight_v1.md),
[Damage Pipeline](Wardogs_DamagePipeline_v2.md), [Combat Data Flow](Wardogs_CombatDataFlow_v1.md),
[Units](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/docs/UNITS.md).
