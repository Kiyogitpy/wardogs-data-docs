---
title: Round 8 armor and hit-location registration
nav_exclude: true
---

# Round 8: armor hooks, armor rows and hit-location registration

Static CL-516586 research, 2026-10-18. Checked the read-only corpus against
instructions in the restored executable (SHA-256
`a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`),
SDK declarations and cooked JSON. No game execution, attachment, service
access, IDA database access, key-file reading or upload was used.

## Results and closure status

This bounded armor pass initially left melee open. The subsequent
[cooked melee trace](round8-melee.md) resolves that row and explains why
the returned armor-event copy is ignored before health evaluation.

| Question | Result | Status |
|---|---|---|
| Armor hook outside direct projectiles | Radial and both back-blast paths call a second, general armor hook. Thrown contact and character actor-impact bodies do not call either armor hook. | Confirmed for the named bodies; melee still open |
| Armor table on a character hit | A separate armor-target event is evaluated inside the hook. Its target tag is the armor/helmet tag. These rows do not join the health event's Infantry group. | Confirmed |
| `ClassToHitLocations` registration | Configured soft class/asset pairs are loaded, then inserted into `ClassToHitLocations_Loaded` by `0x6F03C40`. | Mechanism and the two disjoint shipped keys confirmed; see packed-config follow-up |
| Helmet physics merge | Not investigated in this bounded pass. | Open |

## Two different armor hooks

`IWDDamageable`'s character interface table is `0xB40C038`. Its slot 4
(`+0x20`) is `0x6E6E170`, which calls inventory
`Auth_GetArmorDamageEvent` (`0x6B52A40`) at `0x6E6E1AD`. Slot 3
(`+0x18`) is `0x6E74A20`, which tail-jumps at `0x6E74A3C` to
`0x6B53580`. The latter implements the general operation exposed as
`BP_TryDamageArmorSimple`: registration entry `0x6B67870`, whose corpus
body is filed under the misaligned `0x6B67866` row. The SDK declares it at
`sdk/raw/WDGame_classes.hpp:3286`.

| Source path | Instruction evidence | Armor processing |
|---|---|---|
| Projectile direct/custom impacts, `0x6B725B0` | Interface `+0x20` calls at `0x6B72DF1` and `0x6B73327`; health `ModifyDamage` at `0x6B72FA2` / `0x6B733C6` | Projectile-specific `Auth_GetArmorDamageEvent`; existing exploding-hit exclusion still applies |
| Radial, `0x6F06540` | Interface `+0x18` at `0x6F06BBA`, then `ModifyDamage` at `0x6F06BCC` | General hook |
| On-foot back-blast, `0x6F042A0` | Interface `+0x18` at `0x6F0525B`, then `ModifyDamage` at `0x6F0526C` | General hook; checked in the exe because corpus body failed |
| Seated back-blast, `0x6F06EB0` | Interface `+0x18` at `0x6F07681`, then `ModifyDamage` at `0x6F07695` | General hook |
| Thrown-object contact, `0x6CA8730` | Builder at `0x6CA895C`, interface allow check `+0x30` at `0x6CA896E`, then `ModifyDamage` at `0x6CA8986` | Neither armor hook appears between event creation and evaluation |
| Character actor-impact, `0x6E72D90` | Builder at `0x6E730C3`, `ModifyDamage` with bool 1 at `0x6E730D5` | Neither armor hook on this path; its earlier `+0x18` call at `0x6E72DD7` belongs to a different interface and is not armor processing |
| Melee | Not traced here | Open |

The corpus lists only two native wrappers and the reflected exec as
direct callers of `Auth_GetArmorDamageEvent`: character `0x6E6E170`,
target dummy `0x6A6FC00` and reflected `0x6B671D0` (misaligned corpus row
`0x6B671CF`). This direct-call inventory alone does not rule out
Blueprint callers.

### Coverage differs between the hooks

The projectile hook resolves the actual hit bone and keeps the first
covering armor piece in target-context order, as already documented in
[DamagePipeline §7.6](../../pipelines/Wardogs_DamagePipeline_v2.md#76-the-bullet-event).

The general hook (`0x6B53580`) accepts an explicit hit-location tag and a
bone-name pointer. It resolves the bone only when the explicit tag is
empty and the supplied bone is nonempty (`0x6B536B6`–`0x6B536E0`, lookup
call `0x6B536CE`). A nonempty bone that fails lookup causes an early
return. An explicit/resolved location is written to event `+0x1A0` if
that field is empty (`0x6B5370C`–`0x6B53715`).

With a location it accepts every valid covering piece, rather than only
the first. With both inputs empty it skips the coverage tests completely
(`0x6B537E9`–`0x6B537EC` branch over the `CoveredHitLocations` checks at
`0x6B53807`–`0x6B5384C`).

**Radial and both back-blast callers supply empty location and bone
inputs.** For example radial `0x6F06BA6`–`0x6F06BB6` loads the empty tag,
points `r8` at a zeroed qword, then calls slot 3. The equivalent ranges
are `0x6F05241`–`0x6F0525B` and `0x6F0766B`–`0x6F07681`. Thus these
calls do not use the hit bone to restrict armor coverage. Every accepted
equipped armor/helmet piece gets a separate armor event, via
`0x6B53B65`, followed by the queue operation at `0x6B53B70`.

### Conditional hit-location fallback

Do not infer the health event's final hit location solely from the
general hook's empty inputs. That hook builds a **removal** container:
it adds every armor-family context tag, removes each accepted valid tag
at `0x6B538E2`, and copies/filters the actor entity into the event only
when the removal container is nonempty (`0x6B53919`–`0x6B5393D`).
`0x395F2A0` is a removal helper: underlying `0x395F230` shifts elements
and decrements the array count. If every armor tag resolves to an
accepted piece, this container becomes empty and no entity copy occurs.

Builder `0x6BB4D30` initializes the target entity tag empty and copies the
explicit hit-location argument into event `+0x1A0` at `0x6BB4E67`.
Converter `0x6EF8DE0` loads that hit-location field at `0x6EF90A2`.
Its bone fallback is conditional: a prepopulated target entity tag skips
the whole target-discovery/bone-lookup path (`0x6EF90B9`–`0x6EF90BE`).
When the target entity is initially empty, it discovers that entity and,
if the explicit location is empty, calls `0x6F01BB0` with the event's
raw hit bone (`+0x180`) at `0x6EF91B3`. The selected location is stored
into `FWDModifyDamageData.HitLocation` (`+0xBC`) at `0x6EF9299`.

Consequently, normal valid equipment can retain all armor tags on a
radial hit while the evaluator independently obtains the hit location
from its bone. An unresolved armor-family tag can instead make the
general hook populate the target entity early, suppressing that later
fallback. This is a conditional static path, not an observed gameplay
result; no unconditional claim that radial hits always lack a hit
location is justified.

## Armor table: a separate evaluation

Both hooks call `0x6B53000`. It constructs a new target entity using the
selected armor tag (`0x6BB4CD0`), builds a separate event through
`0x6BB4EB0`, and evaluates it with `ModifyDamage` bool 0 at `0x6B5315D`.
The new starting amount is the original event's amount, loaded at
`0x6B53107`.

The armor-event builder writes the selected tag into target entity
`+0x28` (`0x6BB4F18`–`0x6BB4F1B`), initializes its context empty and
copies the original source entity (`0x6BB4F48`–`0x6BB4F77`). Thus the
collector's target-root walk (`0x6BB6A60`, reads input `+0x58`) visits
the armor/helmet leaf and parents, rather than Infantry. The positive
result becomes `FWDArmorDamageEvent.Amount` (constructor real entry
`0x6BB4C30`, corpus row `0x6BB4C2F`; SDK struct at
`sdk/raw/WDGame_structs.hpp:5028`). The general hook queues it directly;
the projectile wrapper carries it in event `AdditionalData` for the
later slot-5 queue hook (`0x6E74970`, queue call `0x6E74A00`).

The cooked
[`DT_GlobalDamage_ArmorData`](../../data/Wardogs/Content/GameMechanics/DamageSystem/DamageDataTables/DT_GlobalDamage_ArmorData.json)
has four rows and 29 entries. All use `Percentage_Ongoing` and category
Armor; all hit-location and instigator requirements are empty. The
following indices are zero-based **within each armor-table row**, not
the Infantry table's global entry numbers.

| Rows | Index | Source requirements (all required) | Amount |
|---|---:|---|---:|
| Armor and Helmet | 0 | Bullet + HollowPoint | -30 |
| Armor and Helmet | 1 | Bullet + ArmorPiercing | +30 |
| Armor and Helmet | 2 | Bullet | -60 |
| Armor and Helmet | 3 | Bullet + Arms.High + Weapon.Sniper | +28 |
| Armor and Helmet | 4 | Explosive | -85 |
| Armor and Helmet | 5 | Bullet + Armor.Penetrate | 0 |
| Armor only | 6 | DamageType.Melee | -50 |
| Armor only | 7 | none; target-context requirement Armor.Ghillie | -10000 |
| Helmet only | 6 | none; target-context requirement Helmet.Ghillie | -1000 |
| Armor / Helmet | 8 / 7 | Bullet.12g.7mmBuckshot | -80 |
| Armor.Ghillie and Helmet.Ghillie | 0–5 | Bullet; Explosive; Cannon; DamageType.Impact; DamageType.Melee; unconditional (one entry each) | -100 each |

Names in this table omit the `Meta.Damage.` prefix. Multiple matching
entries multiply in this **armor event** using the existing evaluator;
they are not additional multipliers on the character's health event.
For example an ordinary bullet matches the parent row's -60 entry,
giving an armor-event amount of `0.4 × original amount`. This pass did
not trace the final inventory durability write, so the report establishes
evaluation and queuing, not the entire queue-consumption lifecycle.

## Hit-location map writer

SDK `UWDDamageSubsystem` declares config soft pairs at `+0xC0`, loaded
class and asset arrays at `+0xA0` / `+0xB0`, and the transient loaded map
at `+0x110` (`sdk/raw/WDGame_classes.hpp:44427`–`44430`).

Subsystem initialization `0x6F02260` iterates the config map and separates
its class and asset soft paths. It starts the two load requests and
their continuations at `0x6F02D08` / `0x6F02DFA`. Completion paths
`0x6EF2F70` and real entry `0x6EF30C0` (misaligned corpus row
`0x6EF30BD`) populate the loaded arrays and call `0x6F03C40` at
`0x6EF3085` and `0x6EF3202` respectively.

**The writer is `0x6F03C40`.** It requires both loaded-array counts
nonzero (`0x6F03C51`–`0x6F03C68`), iterates the original config pairs,
resolves the class soft pointer at pair `+0` (`0x6F03E16`) and asset at
pair `+0x28` (`0x6F03E8C`), validates their classes, then inserts the
resolved pair into subsystem `+0x110`: `lea rcx,[r15+0x110]` at
`0x6F03F05`, call to map emplacement `0x6EF26D0` at `0x6F03F0C`.

Reader `0x6F01BB0` uses this loaded map and class inheritance tests to
pick an asset, then `0x6BB8D00` does the exact raw bone-name lookup.
The map is not populated by hard-coded keys in this writer. The repository's
exported config omitted the assignment, but the later
[packed-config extraction](round8-config.md#classtohitlocations-entries-and-precedence)
found BHMoverPawn and WDTargetDummy pointing to the player hit-location
asset. Their inheritance branches do not overlap, so no shipped key
precedence contest arises. The writer mechanism and concrete pairs are
both now established.
