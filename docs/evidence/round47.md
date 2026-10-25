# Round 47, agent RE47: closing the open native items of round 46 B

Continues [round 46 B](round46-b.md). Static review of CL516586 only; nothing was run, no devirtualization. RVAs are for `WardogsClient-Win64-Shipping.restored.exe`. Scratch: `E:/Reverse_Engineer/wardogs_analysis/round47/` (`gscan.py`, `mscan.py`, `q.py`, disassembly dumps).

| # | Item | Status | One line |
|---|---|---|---|
| 1 | Guidance field reader | FOUND (`0x6F2E620`); `LockOnTime` not read by projectile code | steering constant and max turn are read in one function, gated by thrust |
| 2 | `DR_CashRewards` resolution | FOUND (rule), hedged on source order | first source wins; a shared row name resolves to the Built table |
| 3 | Wheel `Values[state]` read | NATIVE (open), narrowed | no direct indexed read exists; the state change is delivered to listeners |
| 4 | Deathmatch first team | FOUND (default), hedged | a new player gets the "unassigned" tag, no team |
| 5 | Smoke containment `0x869D740` | FOUND (no side effect) | pure bool test; the caller discards the result |

## 1. Projectile guidance consumer. FOUND (static disassembly)

Mover input producer `0x76D8A00` (slot 98 of `UWDProjectileMove`, shared by the artillery and glide movers) looks up the projectile's runtime record in the projectile subsystem and its `FWDProjectileStats` (`stats`), sums gravity (`0x6F2E4B0`), drag (`0x6F2E240`) and further force terms (`0x6F30680`, `0x6F30280`), then:

- `0x6F307C0` (the thrust predicate: `bShouldThrust` at stats `+0x219`, record fuel `+0x38 > 0`, and `ThrustStartDelay` at stats `+0x2B4` elapsed) must be true; only then `0x6F2E620` (guidance and thrust direction) runs. **Guidance therefore only acts while the motor is thrusting.**
- `0x6F2E620` starts with `cmp byte [stats+0x158], 0` (`bGuidedProjectile`); it returns the unchanged direction when the flag is off or there is no target actor. The target is the weak pointer held in the projectile record (`+0xF8`, flag byte `+0x100`), i.e. the target handed to the projectile at spawn.
- `NearMissExtentMultiplier` (stats `+0x168, +0x170, +0x178`, doubles) scales the target's bounding extents (`0x6F2EA1D` to `0x6F2EA8C`): it builds the near-miss box around the target.
- **`ProportionalNavigationConstant`** (`+0x15C`) is multiplied at `0x6F2F272` with an angle (radians converted to degrees with 57.2958 at `0x6F2F483`) between the missile heading and the line to the target; the product is the commanded turn.
- **`MaxTurnAngle`** (`+0x160`, degrees) is the cap: `0x6F2F48C minss turn, [stats+0x160]` after the 57.2958 conversion. No delta-time factor appears in this term, so it reads as a per-simulation-step cap in degrees (hedge: the step length was not read). The result rotates the direction (axis-angle helper `0x16706F0`).
- **`LockOnTime`** (`+0x164`): no read in the projectile code (`0x6F2E620`, mover tick `0x76D9110`, producer `0x76D8A00`). Not shown to be used by the projectile; the lock timer that does exist is `FWDLockOnTargetingData.LockOnTime`, a separate struct.

Meaning for the data: the 72mm rocket (constant 30, max turn 10) steers harder than the 70mm (max turn 1.0, constant unset so the native default), and both only steer while thrusting. Reproduce: `python round40_veh/rdis.py 6f2e620 4400` and grep `0x15c`, `0x160`, `0x158`.

## 2. `DR_CashRewards` resolution. FOUND (rule); source order assumed

- The cache map at registry `+0xA8` holds one holder per id (104 bytes, created by `0x46E4E00` when a request is first made; state byte `+0x20`: 1 pending, 2 loaded, 4 failed; attempt index `+0x24`). It is keyed by id, so there is no per-source entry to overwrite. The **inserter is `0x46E4E00` (via `0x46E1080`)**, and it adds only when `0x46E1630` does not already find the id.
- Which source supplies the holder is decided by the resolver `0x46ED100` (vtable slot 103): it loops `RuntimeSources` (`+0x50`, count `+0x58`) **in index order**, asks each source for the item's availability (source vtable `+0x2B8`), appends `(source index, name)` for every source that has it, and stops after the first source reporting status 5. `0x46E9B80` (slot 113) takes the source at the holder's attempt index; on success (state 2) it stores the item and stops; only a failure advances to the next source. The cached read `0x46E8CC0` uses list index 0.
- So **the first source in `RuntimeSources` order that has the row name wins; later sources with the same name are never read** (not last-wins). The `DR_CashRewards` sources have a `PreloadTable`, so they are available at once.
- `DataSources` order in the cooked asset: Built, Placed, Placed in FOB, then the other tables. The three buildable tables share the ten `Id.Buildable.*` names plus `Meta.Progression.Context.DefaultReward`. Built carries base 1.0 for every row; Placed and Placed in FOB carry the real bases (FOB 1000, Bunker and Air Raid Shelter 500, Gate and Mortar 300, Tall H-Block 200, H-Block and Tank Trap 100, Barbed Wire 10) and differ from each other in `OwnerModifier` (Placed 1.0, in FOB 0.0) and a few other modifier fields.
- Consequence if the registry id is just the row name (the id has no source selector): a placement reward resolves to the **Built** table (base 1) and the Placed / Placed in FOB rows are shadowed. Not shown: that `RuntimeSources` is filled in `DataSources` order (stock behaviour; the filler was not located in `0x46E0000-0x46F4000`), and which ids the placement code requests. Next step if it matters: find the `RuntimeSources` filler, or log one placement.

## 3. Wheel `Values[state]` read. NATIVE (open), narrowed

- Scans for a state-indexed load (scale 4) at any wheel-asset field offset (0x34 to 0x144) over `0x4F00000-0x5A00000` found none, so there is no direct `Values[state]` instruction in that range; access goes through helpers or per-state copies.
- The state change is only a notification: `0x5370A40` stores the new byte and calls every listener of the delegate at vehicle `+0x3C0` (vtable `+96`, with old and new state), then `0x53AA370` only moves the mesh using already-resolved wheel floats (`+0x2D8`, `+0x2E4`, `+0x2F0`, `+0x310`). Per-wheel records are `0x670` bytes; set-up `0x5356470` copies resolved floats from a 0x68-byte per-wheel config row into them.
- **Next step:** find the listener added to the vehicle `+0x3C0` delegate (the wheel-state response) and read its vtable slot `+96`; the `Values[state]` read should be there.

## 4. Deathmatch first team. FOUND (default), hedged

The per-player pass `0x6D974D0` (post-login loop over players) chooses, in order: if the player's current team is valid (`0x6D8F0B0`) keep it (`0x6D8F2C0`); else if the experience tag list contains the auto-assign tag, flag `+0x5AD` is set and `0x6D8F950` assigns; else if the first-faction tag is present, flag `+0x5AE` is set and `0x6D8EF10` assigns the first faction in the game state's list whose tag is not the "unassigned" tag; **otherwise (the Deathmatch case, both ini flags off) the player is given the unassigned tag (`qword_14D3717D0`), i.e. no team**, and picks Alpha or Bravo afterwards. So the server shows no team first: a new player has none until chosen. Hedge: the two experience tags were not resolved to names, and what the join screen highlights is UI, not read.

## 5. Smoke containment `0x869D740`. FOUND (no side effect)

Decompiled (`0x869D738` is the same code behind an obfuscation stub): the function reads the point list (array of 4 doubles, count `+8`, centre `+0x10` to `+0x20`, radius `+0x60`), builds a box from the pawn position and direction buffers (`0x1670B80` is a rotation-to-vector helper writing locals) and returns **true when the swept box lies inside the smoke**: inside the bounding sphere (radius minus the first float), or inside any one of the per-point cubes (half-size `(|p| - first float) / 2`). It writes only local variables; the owner argument is unused. The caller `0x869F765` ignores the result. **No side effect; the call changes no state.**

## Wiki updates

- Rocket launcher (70mm / 72mm) and anti-air lock: guided rockets steer only while the motor is thrusting; steering strength is the navigation constant (72mm 30) times the angle to the target, capped by max turn (72mm 10 degrees, 70mm 1 degree; per simulation step); the near-miss box scales the target's size; the 2 s lock-on time is not used by the projectile itself.
- Emplacement cash (Placed vs Placed in FOB): "which source is cached first is not known" -> the registry uses the first table that has the row name (Built first), so shared names resolve to the Built table's 1-cash row; the Placed and Placed in FOB amounts are shadowed unless the game requests a different name (not verified).
- Deathmatch and factions: "how a new player is placed is not known" -> the server leaves a new player without a team until they choose Alpha or Bravo.
- Smoke grenade: no hidden side effect in the containment test; it is a pure inside-the-smoke check.
- Vehicle wheel damage values: unchanged (intact, damaged, destroyed order); the state-indexed read is still not located.
