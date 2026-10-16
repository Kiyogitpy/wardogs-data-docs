# Units Reference

> **Project:** [`Kiyogitpy/wardogs-data-docs`](https://github.com/Kiyogitpy/wardogs-data-docs) · [Live site](https://kiyogitpy.github.io/wardogs-data-docs/)

Authoritative unit mapping for data values in Wardogs. Resolves the
UNITS gap bucket (13 bullets across the project — see
[`gap_resolution/UNITS.md`](gap_resolution/UNITS.md)).

**Rule:** when a data doc exports a numeric value without a unit
suffix, assume the UE 5.7 default for that property type. The
canonical mapping is below.

**Exception:** Wardogs uses explicit unit suffixes (`_mps`, `_kmh`,
`_deg`, `_m`) on **some** vehicle stat fields. When present, the
suffix wins over the default.

---

## 1. Distances

| UE context | Unit | Notes |
|---|---|---|
| World coordinates (`FVector`, `FTransform`) | **Unreal Units (UU) = cm** | 1 UU ≡ 1 cm by UE 5 default; projects can rescale but Wardogs does not |
| Weapon `EffectiveRange` | **metres** | **Note: differs from UU default** — inferred from `EffectiveRange: 1000.0` matching real-world .50 BMG effective range (~1000 m). The weapon stat schema treats this as a human-readable range in metres, not UU |
| Bullet speed `InitialBulletSpeed` | **cm/s (UU/s)** | Inferred from `89000.0` ≈ 890 m/s for .50 BMG; matches cm/s convention |
| Attenuation / audio distance | **cm (UU)** | UE audio engine default |
| Camera distance | **cm (UU)** | |
| Field `*_m` suffix (vehicle stats) | **metres** | Explicit override |

## 2. Speeds

| UE context | Unit |
|---|---|
| `Velocity`, `MovementSpeed` default | **cm/s (UU/s)** |
| Vehicle `*_mps` suffix | **m/s** (explicit) |
| Vehicle `*_kmh` suffix | **km/h** (explicit) |
| Bullet speed | cm/s (see §1) |
| Angular velocity | degrees/second |

**Conversion:** `cm/s × 0.01 = m/s`; `m/s × 3.6 = km/h`.

## 3. Angles

| Context | Unit |
|---|---|
| Blueprint-exposed `UProperty` (`FRotator`, `UPROPERTY` floats representing angles) | **degrees** |
| `*_deg` suffix | **degrees** (explicit) |
| Camera FOV | degrees |
| Internal physics / math | radians (but these are rarely in data exports) |

## 4. Time

| Context | Unit |
|---|---|
| All `float` time values in data exports | **seconds** |
| Curve `Time` axis (unless noted otherwise) | **seconds** — see exception below |

**Curve time-axis exception:** some curves use the `Time` axis as a
**distance** (not time). Known cases:

- [`Wardogs_Plugin_BHAimAssist_v2.md`](Wardogs_Plugin_BHAimAssist_v2.md) — aim-assist curves use `Time` as distance in cm (key values 150 to 30000 → 1.5m to 300m range)
- Weapon falloff curves (`CF_*_ADS_Curve`, falloff curves) — `Time` axis represents distance in metres (falloff over range)

When a curve's `Time` key values are large (>10) and the curve is
named for distance context (ADS, falloff, aim-assist), it's a
**distance curve** not a time curve.

## 5. Mass / weight

| Context | Unit |
|---|---|
| Vehicle `Mass` | **kg** (UE physics default) |
| Item `Weight` (0.08 to 42.0 range) | **in-game weight unit** — not kg; appears to be a gameplay-specific scalar used for loadout limits, not a physical kg value |
| Projectile `Mass` | kg (UE physics) |

The item Weight scalar is a game-balance value, not a physics value.
Loadout limits (per-slot and total) use the same unit. Treat it as
"relative" until the loadout cap mechanics expose the ceiling.

## 6. Light intensity

| UE light type | Unit (default) |
|---|---|
| `DirectionalLight.Intensity` | **lux** (illuminance) |
| `PointLight.Intensity` / `SpotLight.Intensity` | depends on `IntensityUnits`: `Unitless`, `Candelas`, `Lumens`, `EV` |
| Sun / sky | lux (DirectionalLight) |

When the data doc shows a sun `Intensity` field without unit, assume
**lux** (DirectionalLight default). Reference:
[Wardogs_Environment_v2.md](Wardogs_Environment_v2.md) sky system.

## 7. Damage

| Context | Unit |
|---|---|
| `Health`, `MaxHealth`, `Damage` amounts | **HP points** (abstract game unit) |
| Damage modifier `Amount` (operation `Percentage_Ongoing`) | **percentage change** — not raw HP. `-95` means "reduce to 5%"; `+200` means "amplify to 300%" |
| `DamageIncrease` fields (environmental hazards) | **multiplicative scalar** (unitless) |

Full damage pipeline documented in
[`Wardogs_DamagePipeline_v1.md`](Wardogs_DamagePipeline_v1.md) and
[`Wardogs_VehicleDamagePipeline_v1.md`](Wardogs_VehicleDamagePipeline_v1.md).

## 8. Physics / simulation

| Context | Unit |
|---|---|
| `DragArea` | **m²** (UE physics default) |
| `Gravity` | cm/s² (UE physics default) |
| `Friction` | unitless scalar |
| Simulation `Iteration` counter | unitless integer (bake/simulation step index) |

## 9. UI / coordinates

| Context | Unit |
|---|---|
| Screen coordinates in UMG widgets | pixels (resolution-dependent — see `DesignTimeScale`) |
| Normalized UV coordinates | 0.0 to 1.0 |

## 10. Fuel economy

| Context | Unit |
|---|---|
| Vehicle `FuelCapacity` | litres (inferred, unlabelled) |
| Vehicle `FuelEconomy` | **not labelled** — could be km/l, l/km, or an abstract scalar |

The FuelEconomy unit is a known open question. Inferred candidates:
- `km/l` — higher number = more efficient (matches values 2–8 range for military vehicles)
- `l/100km` — higher number = less efficient (inverted gameplay)

Needs confirmation from a UI-visible display or in-game test.

---

## When this reference is wrong

If gameplay testing shows a unit doesn't match this reference,
**that is a security-adjacent finding** — a client-server unit
mismatch is a serializer vulnerability class. Route through
[`SECURITY.md`](../SECURITY.md) if you suspect that pattern.

Otherwise, open an issue with the specific property + the observation
that contradicts the reference, and this doc will be corrected.

---

## Doc citation pattern

Each data doc that previously flagged a UNITS gap should cite this
reference inline, like:

```markdown
- **Units.** <field name> is in <unit per docs/UNITS.md §N>.
```

See [`gap_resolution/UNITS.md`](gap_resolution/UNITS.md) for the
13 specific gaps and which §N they resolve to.
