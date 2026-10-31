# Round 46, agent B: closing the open native items of round 45

Continues [round 45 B](round45-b.md). Static review of CL516586 only; nothing was run, no devirtualization. RVAs are for `WardogsClient-Win64-Shipping.restored.exe` (SHA-256 `a5c3db10...0cc37`), read from the decompiled corpus and capstone disassembly. Scratch: `E:/Reverse_Engineer/wardogs_analysis/round46_b/` (`dscan.py`, `fscan.py`, `wscan.py`, `dc.py`). New data: [`assets/data/r46-guidance.json`](../../assets/data/r46-guidance.json) (tool `_tools/r46_guidance_data.py`).

| # | Item | Status | One line |
|---|---|---|---|
| 1 | Gear order, `GearRatios`, `bUseAutoReverse` | FOUND | last entry is the reverse gear (applied negatively); forward gears = count - 1 |
| 2 | Lock-on vs flares, `UProjectileMovementComponent +0x1B4` | FOUND (no such path), NATIVE (guidance consumer) | WD projectiles do not use that component; the lock only gates firing; new guided-projectile data found |
| 3 | Drill Rig zone movement speed | FOUND | speed is metres per second; transition time = distance / speed |
| 4 | `DR_CashRewards` source resolution | NATIVE (open), narrowed | one resolved-id cache; source order given; the cache writer was not read |
| 5 | Wheel `Values[state]` read | NATIVE (open) | not attempted this round |
| 6 | Smoke containment consumer `0x869D738` | NATIVE (open), narrowed | single caller chain; outputs not read |
| 7 | Deathmatch first team shown | NATIVE (open) | not attempted this round |

## 1. Gear order. FOUND (static disassembly)

The Mechanized wheeled component (`UMWheeledVehicleMovementComponent`) holds the transmission system at `+0x560` (`FMWheeledVehicleTransmissionSystem`, 0x90 bytes).

- **Copy from the asset.** The set-up function `0x536F210` copies the asset's `TransmissionData` (asset `+0x58..0xA7`) into the component: `bUseAutoReverse` (asset `+0x59`) to `+0x569` (system `+0x9`), the `GearRatios` array (asset `+0x88`) by array copy `0x17B4920` to component `+0x590` (system `+0x30`), and `FinalGearRatio` to `+0x5A0`.
- **Derived table.** `0x53A26C0` (called with the system as `this`) sets `maxGear = count - 1` (system `+0x74`; `GetMaxGear` returns it through `0x5363DF0`) and fills a per-gear table (system `+0x58`) from the ratio list. In its loop (`0x53A2850` to `0x53A28C6`) index `i < count - 1` uses `GearRatios[i]`, and **index `count - 1` uses `-GearRatios[count - 1]`** (the sign bit is flipped with `xorps`). So the list is: forward gears 1 to `count - 1` in order, then the **last entry is the reverse ratio, applied negatively**.
- **Gear update.** `0x5395B90` (system update): a gear `g` above 0 and below the max reads table entry `g - 1`; gear -1 is reverse. `bUseAutoReverse` (system `+0x9`) is tested at `0x5395C99`: with it on, the system switches between gear 1 and reverse using the vehicle's signed speed against a threshold (system `+0x20`) and the requested direction (`+0x78`). The exact threshold reading is not given here.

Result for the data: the cooked list WHL_01 `4.2, 2.8, 1.9, 1.5, 1.3, 6` means five forward gears and a reverse ratio of 6.0; the native default list `3.0, 5.0` is one forward gear (3.0) and reverse 5.0. The tracked class's own `GearRatios` (`+0xF0` of the tracked data) was not read. Reproduce: `python round40_veh/rdis.py 53a26c0 700` and `python round46_b/dc.py 536f210`.

## 2. Lock-on versus flares. FOUND (no engine homing path), NATIVE (guidance consumer)

- **The `+0x1B4` question has no WD writer to find.** Wardogs projectiles are `AWDProjectile` actors moved by a `UBHMoverComponent` with `UWDProjectileMove`, `UWDArtilleryProjectileMove`, `UWDGlideProjectileMove` (it has `MaxTurnRateDeg`) or `UWDTVGuidedProjectileMove` modes. The only WD class derived from the engine `UProjectileMovementComponent` is `UWDDroppedItemMovementComponent` (dropped items). A scan of the WD code range (`0x6000000` to `0x8C00000`) for `or [reg+0x150], 0x80` (the `bIsHomingProjectile` bit) found none. So the engine `HomingTargetComponent` is not how missiles home here.
- **What `HomingTarget` does.** `WDItemExtension_RangedWeapon +0x148` is read by the Blueprint `B_Action_WeaponFire.BP_CanActivate` (cooked bytecode, `WdExtract dump`; the package name table also contains `HomingTarget` in no other Blueprint): the weapon can fire only when `IsValid(RangedWeaponExtension.HomingTarget)`, the target's owner is valid and `CanFireWeaponWithLockOn` is true (the native getter `0x6CA0FC0` is a plain byte read of extension `+0x548`); otherwise `HandleDryFireEffects` runs. So **the lock gates the trigger**; this Blueprint does not pass the target to the projectile.
- **Flares.** `bFlaresActive` (`+0x791`) is set at `0x766EF2E` and cleared at `0x76794C3`; the reads are in `0x767A0B0`, `0x6EAFD52` and `0x6EB2132`. Nothing found clears `HomingTarget`, `bIsLockedOnTo` or the lock lists when flares are active. Flares therefore have **no confirmed effect on the lock in the client code read** (a server-side effect is not excluded, and the guidance consumer below was not located).
- **New data (guided projectiles).** `FWDProjectileStats.GuidanceData` (`FWDProjectileGuidance`: `bGuidedProjectile`, `ProportionalNavigationConstant`, `MaxTurnAngle`, `LockOnTime`, `NearMissExtentMultiplier`) is stored by three cooked projectile assets (`assets/data/r46-guidance.json`): [`DA_72mm_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/72mm/DA_72mm_ProjectileData.json) guided, proportional-navigation constant **30**, max turn angle **10**, lock-on time **2 s**, speed 45,000 cm/s, life 50 s, arming delay 0.13 s; [`DA_70mm_ProjectileData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/GameMechanics/Inventory/Equipment/Caliber/70mm/DA_70mm_ProjectileData.json) guided, max turn angle **1.0** only, speed 22,400, life 100 s; [`DA_DebugHomingRocketData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Items/Resources/Ammo/DebugHomingRocket/DA_DebugHomingRocketData.json) guided, max turn angle 2.0. The native code that reads these (proportional navigation in the mover or the projectile subsystem) was **not located**: a scan for the four guidance offsets (`+0x158` to `+0x164` of the stats) hits more than 60 struct-copy and property functions that cannot be told apart statically. **Next step:** follow the stats copy from the `UWDProjectileSubsystem` spawn path, or list the vtable of `UWDProjectileMove`.

## 3. Drill Rig zone movement. FOUND (static disassembly)

Round 45 found no reader of the speed because the load is inside the activation handler. The speed float (`+0xF0` of `WDHotZoneMagnetGameStateComponent`, native 3.0) is loaded at `0x8567734` (authority handler `0x85674A0`) and `0x8572386` (client `0x8571F80`) and passed through `0x856FE50` and `0x85731A0` to **`0x776DDD0`**, the control-zone component's relocation function. There:

- the target location is stored (`+1704`), the relocating flag (`+1696`) is set, the extents (`+1424`) take the size-multiplied extents, and the **speed is stored at control-zone component `+1348` (`0x544`), clamped to at least 0.01** (a speed argument of 0 keeps the previous value);
- `0x776D890` computes the transition time (`+1340`) as **distance(current centre, target) x 0.01 / speed**: the distance is in Unreal units (1 unit = 1 cm), the factor 0.01 gives metres, so **the speed is metres per second** and the result is seconds;
- `0x776DDD0` returns that time and `0x85731A0` **adds it to the activation total** (`+0x1AC` of the world component), so a longer trip lengthens the active period by the travel time.

So the zone is brought to the rig at 3 m/s with the native world pair; the rig asset's 5.0 would apply only if the asset pair is copied into the world component, which was not traced (both handlers read the world component). The per-tick interpolation of the centre (state `+1336` and `+1344`) was not read; the formula above is the proven part.

## 4. `DR_CashRewards` source resolution. NATIVE (open), narrowed

- Data: the `DataSources` order is Built (0), **Placed (1), Placed in FOB (2)**, ControlZoneReward (3), DeployableDestroyed (4), DeployedSupplyCrate (5), EndGameFactionReward (6), Heal (7), HotZoneMagnet (8), PlayerKill (9), Refuel (10), Repair (11), Revive (12), VehicleDestroyed (13), VehicleTransport (14), plus a `MetaDataRegistrySource_DataTable`. `RuntimeSources` is at registry `+0x50/+0x58` (`UDataRegistry`, vtable `0xA7838E0`).
- Native: the cached-item lookup is a **single map keyed by the resolved id**, not a per-source search. `0x46E8BA0` (vtable slot at `+864`, called by the Blueprint wrapper `0x46EEE20`) resolves the id (virtual `+824`), looks it up in one cache map (registry `+0xA8`, 48-byte entries) and returns the one cached holder. So when two sources carry the same row name, **the source that wrote the cache entry wins**, which depends on the acquire order, not on the lookup. The loop over `RuntimeSources` that writes the cache was not read (`0x46E9180` combines per-source availability; `0x46E8DC0` filters sources by a virtual id; neither is the writer).
- Not closed. **Next step:** find the writer of the cache map (callers that insert into registry `+0xA8`) and whether it skips an id that already has an entry (first source wins) or overwrites it (last wins). WD native code does not choose between the tables (round 45).

## 5. Wheel `Values[state]` read. NATIVE (open)

Not attempted this round. Unchanged from round 45 item 1.

## 6. Smoke containment `0x869D738`. NATIVE (open), narrowed

`0x869D740` has one caller, `0x869F765` in `UpdatePawnsInSmoke` (`0x869F600`), made per pawn with the point list (`this+0x2E8`), two output buffers (`[rsp+0x40]`, `[rsp+0x80]`), two floats and the pawn's owner from `0x3A99480`; `0x869D738` has no direct caller (it is an interior label of `0x869D740`). The outputs are not read after the call, so any effect must be a side effect inside `0x869D740` through the owner argument. Not traced further.

## 7. Deathmatch first team shown. NATIVE (open)

Not attempted this round. Unchanged from round 45 item 17.

## Wiki updates

- Vehicle handling (gear ratios): "last wheeled ratio is reverse" (inferred) -> **confirmed**: the last entry of `GearRatios` is the reverse gear, applied negatively; forward gears = entries - 1 (WHL_01 has 5 forward gears and reverse 6.0; the default list is 1 forward gear 3.0 and reverse 5.0).
- Drill Rig (hot zone magnet): "drawn toward it at the configured speed" (read from names) -> **proven**: speed is metres per second, travel time = distance in metres / speed, and that time is added to the active duration; native world speed 3.0 (rig asset 5.0, not shown to apply).
- Anti-air lock-on and flares: no flare check on the lock exists in the client code read; the lock only allows the weapon to fire (valid target and lock flag); missile steering comes from projectile data, not from the engine homing component.
- Rocket launcher projectiles (70mm / 72mm): add guidance data: 72mm guided, proportional-navigation constant 30, max turn angle 10, lock-on time 2 s; 70mm guided, max turn angle 1.0 (other fields unset).
- Emplacement cash (Placed vs Placed in FOB): still open; the sentence "stock Unreal returns the first source that has the id" should read "which source is cached first is not known" until item 4 is closed.
