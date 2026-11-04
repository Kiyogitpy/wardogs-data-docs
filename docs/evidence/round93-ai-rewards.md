---
title: Round 93 — AI vehicle noise and buildable destruction assists
nav_exclude: true
---

# Round 93: G5 AI vehicle-noise emitters / G6 buildable destruction assists

Static review of the retained CL-516586 native and cooked-data artifacts. Nothing was run in the game. This report does not establish live activation, a server configuration or an observed payout.

## Disposition

| Gap | Result | What is established | Remaining edge |
|---|---|---|---|
| **G5: vehicle engine / horn / destruction → AI hearing** | **closed-static**, conditional compiled path | Actual vehicle events, selected DWORD-cached ranges, engine/horn timers, attributed destruction, hearing delivery/storage and Wardogs consumption are joined in the continuation below. The [recovered selected controller](round93-ai-controller-config.md) explicitly assigns AISense_Hearing. | Feature/component/timer activation, eligible attribution and listeners, final per-variant settings and positive live detection remain unobserved. Defaults are not unconditional detection radii. |
| **G6: buildable destruction assist** | **closed-static**, configured path | Retained damage/current MaxHealth producer, StateTree inputs, variant calculator selection and native grant route are joined. The [recovered registry](round93-registry-binding.md) closes the exact registry-ID → table binding. Cash uses its assist fraction curve; role XP has an ordered context selector with an AssistReward alternative, not unconditional AssistReward selection. | Feature/challenge activation, successful dynamic registry acquisition, actual credit and persistence remain unobserved; authority, validity and failure gates remain part of the contract. |

“Closed-static” means that the specified compiled/data edge was reviewed, not that a match executed it. Historical discovery sections and worker-stage result labels below retain their earlier search scope; the current table, G5 continuation and linked companions supersede their missing-emitter/missing-registry/missing-controller qualifications. The reviewed pre-integration snapshots are preserved privately, not silently rewritten as historical proof. Independent semantic review accepted these bounded static paths with the role-XP selection and local age-check wording corrections incorporated here.

## Sources and identity

Native addresses below are **RVAs**, image base `0x140000000`. The restored executable was freshly hashed during this review:

- SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`.
- Size: 231,695,256 bytes.
- Corpus conventions and limits: [DECOMPILATION_CORPUS.md](../DECOMPILATION_CORPUS.md).

The native source reference `C<group>:<lines>` means the local, unpublished file
`deepextract_cl516586/extracted_code/WardogsClient-Win64-Shipping.restored_exe/WardogsClient-Win64-Shipping.restored_exe_standalone_group_<group>.cpp`, at the stated line range. These are analysis outputs, not original game source. Selected assembly and PE metadata were checked where pseudocode obscured arguments or entry boundaries. Raw decompilation is not included in this report.

Asset references below use this checkout prefix:

[`data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content).

The private evidence directory is the existing `published_data_verification/ai-rewards` investigation. Earlier extracts and receipts were retained. New checks and selected-source hashes are in `verification.json`, `source-manifest.json` and `task-ownership-verified.json` there.

## G5 — a real generic bridge, but no vehicle trigger closure

### Configuration is not the event

[Round 42, R3](round42-modes-ai-other.md#r3-which-events-create-hearing-stimuli) left the vehicle emitters unresolved. Its constructor result is reproduced by the retained body at **RVA `0x5300B10`**, `C34343:179–312`: engine 10,000, horn 50,000 and destroyed-vehicle 80,000 world-distance units. The SDK identifies the fields as `AIEngineLoudnessMaxRange`, `AIHornLoudnessMaxRange` and `AIVehicleDestroyedLoudnessMaxRange` at `+0x2A0`, `+0x2A4`, `+0x2A8` (`CppSDK/SDK/Mechanized_classes.hpp:114–116`). The familiar 100/500/800 m wording is a conversion of those configured ranges, not a recovered trigger radius in operation.

The retained `vehicle-offset-search.json` searches a particular pseudocode shape: float dereferences at decimal offsets 672/676/680 in unnamed functions at VA >= `0x144000000`. That is a candidate search, **not** an exhaustive use-def analysis. It misses other access widths, address calculations, named functions and indirect/reflected consumers. The resumed review did not establish a vehicle-config reader among those candidates. This does not establish universally absent behavior, server ownership or dead configuration.

### Why direct-call-only negatives were insufficient

A compiled actor-noise route exists independently of a direct call to the Blueprint-facing `ReportNoiseEvent` helper:

1. Actor noise code calls the process-global noise delegate through vtable displacement `+0x58` (retained actor body at RVA `0x3A9BB1C`, relevant instruction range **`0x3A9BBEC–0x3A9BC1C`**; Blueprint-facing actor wrapper at `0x3AB1110`). The exported actor body has entry-boundary/pseudocode limitations; the indirect call and argument setup were checked in its retained assembly rather than inferred from its abbreviated pseudocode.
2. **`0x48879F0`**, `C29337:464–496`, constructs a callback object containing **`0x4880F10`** and passes it to **`0x3AA38A0`**, `C22810:204–265`, which replaces that global delegate.
3. The callback object's vtable at RVA **`0xA308300`**, slot 11, points to actual entry **`0x3A7EE20`**. Its instructions load the stored callback at object `+0x18`, rearrange the actor-noise arguments and jump to it. The containing export starts earlier (`C22736:223–233`); its misleading predecessor loop is **not** the callback entry. The selected entry bytes were checked against the PE.
4. **`0x4880F10`**, `C29323:310–374`, constructs the hearing event and calls **`0x4871600`**. That function obtains the hearing sense's instance and calls **`0x4887980`**, `C29337:438–455`, which appends an event to the sense queue and schedules an update.

This closes a **generic compiled emission bridge**, conditional on delegate installation and valid world/perception objects. It does **not** show that a vehicle calls actor noise, or which loudness/max-range values it passes. It also does not by itself show a Wardogs AI consuming that vehicle event. The retained Wardogs hearing-strength calculation **`0x8870350`**, `C59888:199–280`, reads perceived-target motion and the weapon firing-sequence flag; it is not evidence that the three vehicle ranges reach this consumer.

**Publication consequence:** keep the three distances labelled *configured*. Do not replace that qualification with “vehicles are heard up to these distances,” and do not replace the missing emitter with “there is no vehicle hearing.” The exact next static obligation is a vehicle event caller/reader joined through the bridge (or another emitter) to the relevant AI perception update.

## G6 — native fraction and decoded assist pipeline

### 1. The fraction is produced by buildable damage/destruction code

This is no longer an inference from the curve's name or key domain.

- `UWDBuildableComponent` owns `VitalityComponent` at `+0x110` and `TrackedDamageData` at `+0x290` (`CppSDK/SDK/BuildablesRuntime_classes.hpp:1473–1519`).
- **`0x858FF60`**, `C58473:1–361`, handles positive damage on the authority-side path. It updates the per-assister tracked entry: initializes its scalar from damage-context `CurrentDamage`, or adds the current amount to the existing scalar, and refreshes its timestamp. `CurrentDamage` is the float at context `+0` (`CppSDK/SDK/WDGame_structs.hpp:4956–4968`).
- **`0x8588A10`** prunes tracked entries for invalid assisters or expired assist time. The destruction routine calls it before walking the map. Consequently the numerator is **retained tracked damage**, not an unqualified lifetime damage total.
- **`0x858EED0`**, `C58471:1–454`, walks eligible tracked assisters during destruction. It excludes the final instigator's player state, requires a valid controller/player state and a matching recorded/current faction, and requires a valid event subsystem. It then writes:

  **`DamageFraction = retained assister damage / current VitalityComponent.MaxHealth`**, or zero when the denominator's absolute value is at most the native near-zero threshold (`1e-8`).

  The decisive division is in the retained assembly at **RVA `0x858F646`**; the corresponding producer/payload construction is `C58471:333–389`.
- **`0x6B81CD0`**, `C46185:163–169`, returns the vitality float at `+0x134`, identified as `MaxHealth` by `CppSDK/SDK/WDGame_classes.hpp:3126–3147`.
- The destruction code packages this value as **`WDBuildableDestroyedAssistEvent`**, whose type getter is **`0x8576800`**, `C58420:449–465`, and sends targeted and untargeted events through **`0x4D49E50`**. SDK payload fields: `CppSDK/SDK/BuildablesRuntime_structs.hpp:152–168`.

This is not a proven clamp to `[0,1]`, division by total damage from all players, or the fraction of *remaining* health removed. The inspected producer divides accumulated `CurrentDamage`, not a separately measured health-loss counter. Healing, repeat damage, history expiry and other damage-path rules must not be silently replaced with a “percentage of original health actually removed” guarantee.

### 2. The StateTree has an explicit event → calculator binding

Asset: [ST_Challenges_SessionEvents_Buildable_BuildableDestroyed_Assist.json](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/ST_Challenges_SessionEvents_Buildable_BuildableDestroyed_Assist.json).

The listener specifies payload type `WDBuildableDestroyedAssistEvent` and tag `Event.StateTree.BuildableDestroyed.Assist` (lines **1788–1818**). The event transition matches that payload type/tag; the source properties and handles, not just display names, connect:

| Source | Destination / purpose |
|---|---|
| Event `DamageFraction` | State parameter `DamageFraction` (binding 5; source lines **4618–4660**) |
| State parameter `DamageFraction` | `Calculate Reward.Inputs[0].Value`, variable name `DamageFraction` (binding 36; lines **5438–5497**) |
| State parameters `BuildingProgress`, `TotalFOBSupplies` | Calculator variables `BuildProgress`, `TotalFOBSupplies` (bindings 37/38) |
| Lookup task `RewardTag` | Calculator `RewardTag` (binding 35) |
| State parameter `ContextTags` | Calculator and grant contexts; a property reference also lets context tasks mutate the same container |
| Calculator `RewardResources` | Grant `RewardResources` (binding 46); property reference 1 lets the XP-tag update task modify the calculated resource list before grant |

The unconditional assist-context task adds **`Challenges.Context.Assist.BuildableDamage`** (lines **3289–3310**). The lookup instance specifies registry **`Challenges.SessionEvents.DestroyedBuildable`**, filter **`Id.Buildable`** and no fallback reward tag (lines **3371–3389**). The task sequence is lookup → successful calculation → XP-tag update → grant; failed lookup/calculation transitions return to the root. Object-equality conditions scope the assister to the current challenge owner. The grant's `RewardTag` is separately bound from a state parameter; it is **not** the lookup's calculator-selection tag. Resource-list flow, rather than confusing those two tags, establishes the calculation-to-grant handoff.

The private decoded bindings are checked against the original export, including both property-reference paths. No Blueprint decompilation or StateTree execution is claimed.

### 3. Native ownership of the three key tasks is resolved

The shared `sub_...` name was not treated as unique ownership. For each task the PE metadata was joined from the reflected type name to its struct-ops allocator, constructor, installed vtable and entry slot. Fresh image-bound receipts retain those joins.

| Reflected task | Struct metadata RVA | Constructor RVA | Vtable RVA | Entry slot 5 / native behavior |
|---|---|---|---|---|
| `WDSessionEventsGetRewardTagFromRegistryTask` | `0xCE98720` | `0x69A66D0` | `0xB13BB20` | **`0x6CC1DC0`**, `C46793:53–149`: resolves context property reference, filters context tags, queries the named registry, checks row type and writes output `RewardTag` |
| `WDSessionEventsCalculateRewardTask` | `0xCE984A0` | `0x69A8280` | `0xB13B978` | **`0x6CC11D0`**, `C46792:1–563`: queries the reward definition, builds named inputs, evaluates each resource and produces the resource list |
| `WDSessionEventsGrantRewardTask` | `0xCE98540` | `0x69A7C50` | `0xB13B9C8` | **`0x6CC2080`**, `C46793:208–468`: converts/scales finite resource values and calls the reward-grant implementation |

SDK layouts independently match the accessed fields (`CppSDK/SDK/WDGame_structs.hpp:7297–7341,7389–7404,7483–7503`). The formerly interrupted getters `0x69ABD20` / `0x69ABD50` were recovered from `C45247:443–472` and independently queried from the read-only database.

The event listener's registered callback **`0x4D48030`** forwards the typed event and configured StateTree tag through **`0x4D1BAE0`** → **`0x4D35230`**, which queues the StateTree event under its running/queue-capacity checks (`C31556:98–144`, `C31607:303–360`). A registered listener and running challenge remain prerequisites; queue submission is not an observed transition.

### 4. Shared destruction rows carry assist-specific calculation

Sources:

- [DT_RewardLookup_SessionEvent_BuildableDestroyed](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_BuildableDestroyed.json), lines **14–303**.
- [DT_ChallengeRewards_SessionEvents_Buildables](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_ChallengeRewards_SessionEvents_Buildables.json), e.g. lines **935–985,1149–1177**.
- [assist curve](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/CurveTables/CRV_Challenges_Curves_BuildableDestroyedAssist_DamageFraction.json), lines **9–34**.

Programmatic comparison finds **36** variant lookup rows, whose reward-tag target set equals the **36** destruction calculator row keys. There is no need for a separately named destruction-assist calculator row to express assist behavior:

- All **36 cash resources** select `DamageAssistCurve` for `AssistCurve` and `DamageAssistScalar` for `AssistScalar` when the assist-context tag matches.
- `DamageAssistCurve` explicitly names **`DamageFraction`** as `ScalingValueInput`, with live-curve tag `LiveCurves.Challenges.SessionEvents.BuildableDestroyedAssist.DamageFraction`.
- `DamageAssistScalar` is literal **1.0** in those cash definitions. The two-key linear curve returns its input within the configured 0–1 interval. This is not proof that the producer always supplies that interval.
- The **36 role-XP resources are different**: they use a `BaseReward` selector with an `AssistReward` alternative and do not use `DamageFraction` / `AssistCurve`. Do not generalize cash's fraction multiplier to all XP. For example, the FOB role-XP expression and assist selector are at lines **1281–1285,1474–1495,1556–1570**; ordinary structure role-XP also includes its own `BuildProgress` factor.

The native evaluator **`0x6CCEB50`**, `C46816:1–593`, resolves selected variables. Its scaling-value arm obtains the named input, queries `LiveCurves`, checks the curve row/object and evaluates it through **`0x3E0DA70`** (`C46816:363–402`). **`0x6CC9F40`** chooses the matching conditional/default expression, and **`0x6CCD310`**, `C46813:1–616`, evaluates compiled instructions. These are executable consumers of the configured curve/expression, not merely names in the asset.

The grant task calls **`0x6CBA0A0`**, which prepares resource changes and dispatches the session player-state grant virtual at `+0x848`. The mapped implementation **`0x6DAAF90`**, `C47245:17–65`, calls **`0x6D61EE0`**, `C47104:154–406`; that path checks authority, aggregates resource changes and calls **`0x6D683E0`**, `C47117:1–89`, into attribute handling. Its ordinary branch supplies a numeric delta to actual entry **`0x52312F0`** (containing export `C33940:366–409`); assembly preserves the floating argument that the pseudocode omits. This establishes the native grant route and its gates, not persistence to a backend or a successful account credit.

### 5. Activation evidence and the remaining registry qualification

[BuildableRewards.json](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/BuildableRewards.json), lines **12–17,32–88**, references the destruction registry asset and configures challenge, reward and live-curve table sources for client and server. The current [challenge definitions table](../../data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/DT_Challenges_SessionEvents_Buildables.json) has **11 rows**, including the assist definition at lines **145–208**, `bAutoActivate: true`, and the exact assist StateTree reference. The older rewards-page statement that this table has zero rows is not true of the inspected current export.

However, the registry object [`DR_SessionEvent_BuildableDestroyed`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/DR_SessionEvent_BuildableDestroyed.json) is referenced but not itself present in the inspected JSON exports. Matching table names and target sets do not establish that the tree's exact registry name is backed by that table in an active registry. Recovering that registry object's ID/source configuration is the concrete remaining static join. Live feature availability, prerequisite success, registry acquisition, listener execution and payout success remain unmeasured.

## Corrections supported for parent integration

No wiki/reference page was changed by this work unit.

1. **AI page:** retain “configured” on 100/500/800 m; vehicle-event emission and AI delivery are still open. Do not infer absence from a failed field-reader/direct-call search.
2. **Rewards §6:** replace “input unnamed / most likely damage fraction” with the source-bound retained-damage divided by vitality `MaxHealth` producer and explicit StateTree input binding. Retain the denominator/eligibility/range qualifications above.
3. **Rewards §7:** the assist path is no longer merely assumed from `AssistCurve` names. It explicitly reuses variant destruction rows, and calculated resources feed grant; cash and role XP have different assist formulas. Overall activation/registry resolution remains conditional.
4. **Rewards §7:** the current challenge table contains 11 definitions, including an auto-activate assist tree reference. StateTree bindings/states are readable here; the blanket “does not decode their states” limitation is stale for this inspected tree, not disproved for every tree.

## Verification and limits

Actual local executions, with exit codes:

| Check | Result |
|---|---|
| `python -B verify_task_ownership.py` | **0**; freshly hashed the PE and independently recovered all three type → constructor → vtable → entry joins |
| `python -B verify_ai_rewards.py` | **0**; **23** named checks, including equality of five retained StateTree sections to the source, decisive bindings/property references, an intentionally wrong fraction-binding negative control, full lookup/calculator key-set comparison, 36 cash and 36 role-XP resource checks, selected PE bytes and query-plan verification |
| `python -B resume_db.py ...` | **0**; read-only immutable database retrieval; exact `COLLATE NOCASE` matches the actual name index and produces indexed `SEARCH`, not a covering-index `SCAN` |
| Initial unmodified helper's two-name query | **124**, timed out after 120 seconds; no behavioral negative inferred. Both getters were subsequently recovered from existing CPP and queried successfully by the corrected indexed route. |
| Optional Capstone import | **1**, package absent in that interpreter; no installation made. Existing corpus assembly plus selected PE bytes were used instead. |

Verifier development also exposed two rejected assumptions: applying the cash assist formula to every resource (role XP uses its own selector), and expecting a different equivalent REX prefix on the callback jump. Both failed checks are recorded privately; final claims use the observed resource separation and actual bytes. Missing exact exported names for interior native entries were retained as boundary issues, not treated as missing implementations.

These checks verify saved data/metadata and selected compiled edges. They are not a runtime replay, whole-program proof, exhaustive vehicle-reader search, backend-persistence test or a guarantee of payout amount. Scope was restricted to this report and the existing private investigation directory; no source corpus, live target, driver, service, configuration, shared ledger or wiki was modified, and nothing was committed or pushed.


## G5 continuation — vehicle producer/config/consumer route recovered

This append-only continuation supersedes the **missing vehicle emitter/config reader** disposition above. **G5's compiled event → selected configuration → actor-noise → perception-storage → Wardogs hearing-consumer path is now closed-static, with explicit eligibility and configuration gates.** This is not an observation of a running match, proof of feature activation, or a universal 100/500/800 m detection guarantee. The original report and its G6 findings are preserved unchanged.

### Actual component and selected configuration

The missing reader is **`UWDVehicleDetectabilityComponent`**, not the vehicle constructor. The [WDAIPvEAICore feature asset](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/AI/WDAIPvEAICore/Content/WDAIPvEAICore.json), lines **91–102**, adds this component to `/Script/Mechanized.BHBaseVehiclePawn` with **`bServerComponent: true`, `bClientComponent: false`**. This is positive server-side installation configuration, not an inference from failing to find client callers. Activation remains a prerequisite.

Its initialization at **RVA `0x8869A80`**, `C59876:369–447`, validates/casts its owner as the vehicle pawn and obtains that pawn's actual `VehicleConfig` through **`0x53CB340`**. The getter reads pawn **`+0xA78`**, agreeing with `Mechanized_classes.hpp:548`. It then performs the following **DWORD copies**:

| Selected vehicle-config field | Cached component field | Emission using that cached field |
|---|---|---|
| `+0x2A0` / `AIEngineLoudnessMaxRange` | `+0xF0` | Engine timer entry `0x8873CB0` |
| `+0x2A4` / `AIHornLoudnessMaxRange` | `+0xF4` | Horn timer entry `0x8873F80` |
| `+0x2A8` / `AIVehicleDestroyedLoudnessMaxRange` | `+0xF8` | Destruction callback `0x8875970` |

These integer-width copies explain why the earlier float-dereference scan missed the reader. The component constructor **`0x8864B60`** also initializes those cached fields to **10,000 / 50,000 / 80,000**; a valid selected vehicle config replaces them during initialization. Thus the fields are genuinely used as emission max-range arguments. Their defaults are still not proof of every vehicle variant's overridden or live values, and later changes to a config object are not shown to refresh this initialization-time cache.

The PE independently confirms component vtable **`0xBC3A9D8`**, slot 128 → `0x8869A80`, slot 129 → cleanup `0x886BE30`. Initialization binds the engine/horn reflected delegates at pawn **`+0x670` / `+0x680`** and the destruction native multicast at **`+0x6E0`**. Cleanup removes those bindings and clears the two timers.

### The events really reach the emitters

| Event | Recovered compiled route |
|---|---|
| **Engine starts/stops** | `0x53D6070` / `0x53D6440` write pawn `bIsEngineRunning` at `+0x889` on their authority branch, then invoke vtable slot 321. Base implementation **`0x53D08A0`** broadcasts that boolean through pawn `+0x670`. Rotary/wheeled overrides **`0x53D0910` / `0x53D0970`** explicitly call the base broadcast. The component's reflected callback resolves to **`0x8875A70`**, which starts a looping timer when true and clears it when false. |
| **Horn state changes** | **`0x53D5360`** writes `bIsHornActive` at pawn `+0x918` when the vehicle is not destroyed, then calls **`0x53D09C0`**; its first operation broadcasts the boolean through `+0x680`. The component callback **`0x8875B50`** starts/clears the horn timer. The replicated-state wrapper **`0x53DDDC0`** also routes to `0x53D09C0`. The gameplay-cue/audio branch is separate from this initial delegate broadcast. |
| **Vehicle destruction with damage attribution** | The depleted-value destruction branch in **`0x532F730`** calls **`0x53D8E20`**, which broadcasts its damage-instigator/controller and damage-causer arguments through pawn `+0x6E0`. Initialization bound component callback **`0x8875970`** there. This callback reads cached `+0xF8` and calls actor noise. The replicated destroyed-state path **`0x53D0DC0`** broadcasts null attribution arguments; that does **not** pass this callback's non-null/validity checks and therefore does not establish a second destruction stimulus. |

Source ranges: engine start/stop `C34740:164–252,411–442`; engine/horn broadcasts `C34730:1–27,91–271`; damage/destruction `C34434:1–96`, `C34745:354–392`; component callbacks `C59898:352–390,398–430,438–469`.

The timer targets were another export-boundary trap. Actual PE entries **`0x8873CB0`** and **`0x8873F80`** are each a load of component `+0xF0` or `+0xF4` into the floating argument followed by a jump to **`0x887EC80`**, `C59917:295–368`. Nearest-preceding exported pseudocode is unrelated and was not used as their implementation.

### Exact emission arguments and attribution

The shared engine/horn emitter **`0x887EC80`** resolves the vehicle's seat component (getter **`0x53CAE20`**, pawn `+0x758`), obtains its candidate actors through **`0x532BF30`**, and selects the **first valid candidate**. The candidate builder includes seated/unseated occupants and eligible occupancy-history entries (`0x532B9F0`, `0x53259B0`, `0x532C150`); it is not simply “the driver,” and the emitter does not loop over all candidates to emit one event each.

At actor-noise call **`0x887ED7F` → `0x3A9BB20`**:

- noise-making actor **and** instigator are the selected candidate actor;
- location is the vehicle root-component location (or the compiled fallback if there is no root);
- **loudness is `1.0`**;
- **max range is the selected cached engine or horn range**;
- the tag argument is zero/default.

No valid candidate means no emission on this route. This attribution explains why looking only for the vehicle itself as the perceived actor would miss the connection.

At destruction call **`0x8875A48` → `0x3A9BB20`**, the noise-making actor is the **damage causer**, instigator is the damage-instigator controller's pawn (`+0x2F8`), location is the destroyed vehicle's location, loudness is **`1.0`**, max range is component **`+0xF8`**, and tag is zero/default. The callback requires valid non-null controller and damage-causer objects. These argument assignments, including floating arguments omitted by pseudocode, were checked in retained assembly and PE bytes.

### Beyond submission: delivery and Wardogs consumption

The calls above enter the already recovered indirect actor-noise bridge at actual entry `0x3A9BB20`, through the installed global delegate and hearing event constructor, to sense event queue **`0x4887980`**. The continuation follows that queue rather than stopping at submission:

1. **Hearing update `0x488E140`**, `C29350:154–447`, consumes the sense's event array. It checks enabled hearing, listener distance against the listener's hearing range scaled by loudness, positive event max-range scaled by loudness, and affiliation. It builds the hearing stimulus with the event's attributed actor/location and appends a delayed-delivery record to the perception system. Therefore an event max-range is a cap in a gated pipeline, not an unconditional detection radius.
2. **`0x4878650`**, `C29308:1–118`, drains due delayed records, resolves their listener and attributed actor, marks the listener for processing, and calls actual entry **`0x4888470`**. Its PE instructions append to the listener's stimulus queue at **`+0x168`**, count **`+0x170`**. Perception-system tick **`0x488C6A0`** invokes hearing update through sense vtable **`+0x2F0`**, performs delayed delivery, then calls **`0x48858E0`** on marked listeners.
3. **`0x48858E0`**, `C29334:1–519`, consumes that listener queue and creates/updates its attributed-actor perception information at **`+0x118`**, with per-sense stimulus records. This closes queue delivery into the same storage later read by Wardogs, subject to object validity and the ordinary stimulus-processing gates.
4. **`UWDAIPerceptionComponent`** vtable **`0xBC38D40`**, slot 131 → **`0x887CAE0`**, calls **`0x8876C80`**, `C59901:1–413`. This walks inherited perception information at **`+0x118`**, requires its hostile/valid-target, valid-sense-ID, positive-strength and non-invalid-age checks in addition to inherited perception-processing gates, and compares stimulus sense identity against configured **`HearingSense` at `+0x238`**. The matching hearing branch calls **`0x8876A40`**, `C59900:249–336`. The local instructions at `0x8876ED6–0x8876EF0` reject the invalid sense ID, nonpositive strength and age at or above the FLT_MAX invalid-age sentinel; they do not locally compare age with `ExpirationAge` or prove that every retained record is unexpired.
5. That Wardogs hearing consumer reads stimulus source/listener locations, the hearing sense configuration and **`HearingRangeMultiplier` (`+0x22C`)**, obtains target detectability, calls the previously recovered movement/firing-strength function **`0x8870350`**, and stores the resulting hearing value through **`0x8861ED0`** in its per-target/per-sense map at **`+0x1D0`**. `0x8870350` alone was not vehicle proof; the newly recovered producer, attribution, queue/storage and sense-selection joins provide the missing connection. A submitted noise need not yield a positive final Wardogs score.

**Remaining boundary, not silently promoted:** this is a conditional compiled route, not a live hearing test. The feature must be active, the component initialized, engine/horn timers serviced, eligible attribution present, and a valid hearing listener configured. The parent subsequently recovered the selected controller's exact cooked `HearingSense` and sense-config assignment in the [controller companion](round93-ai-controller-config.md); that earlier missing-export qualification is closed. Every vehicle variant's final overrides, active live components/listeners and successful detection remain unobserved. The former unknown native vehicle caller and config reader are no longer missing.

### Continuation verification

All new raw excerpts, PE disassembly, scoped scans, source maps and checks are private in `published_data_verification/ai-rewards`; no raw decompilation is published here. The exact pre-append report is preserved as `g5-report-before.md` with its hash in `g5-report-preservation.json`.

- **`py -3.13 -B verify_g5_vehicle.py`: exit 0, 40 checks.** Fresh image SHA-256 matches the identity above; read-only indexed DB retrieval matches ten retained decisive bodies; actual PE vtable slots, tiny timer entries, loudness constants, field selection, event dispatch, delayed delivery, perception-store join, Wardogs hearing branch and server-only component configuration pass. A deliberately swapped engine/horn offset is rejected.
- `resume_db.py` and the bounded delegate scan completed with **exit 0**. Missing exact exported names for the timer stubs/reflected wrappers were retained as export limitations; actual entry bytes or the separately labelled old alias/body corpus supplied the missing boundaries.
- The new verifier initially exited **1** twice because its textual anchors used an older export's temporary variable name and an extra parenthesis. Both mismatches were checked against the current source and corrected; they were not failed behavioral tests. Capstone is available in the selected Python 3.13 environment; no package installation was performed.

Only this appendix and the owned private directory were changed. No G6 research/integration, shared ledger/wiki edits, source-corpus writes, live target activity, commits or pushes were performed.
