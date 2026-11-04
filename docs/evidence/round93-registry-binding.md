# Round 93: buildable destruction-assist registry binding (G6)

## Disposition

**G6 is closed-static for the documented fraction producer and configured assist calculation/grant path.** This note supplies the exact registry-name-to-table join left conditional in [Round 93 AI/rewards](round93-ai-rewards.md#g6--native-fraction-and-decoded-assist-pipeline). It supersedes only that report's missing-registry qualification; its authority, validity, challenge-running, queue and outcome limits remain applicable. No live reward or backend persistence was observed.

## Newly recovered source

The existing offline WdExtract tool decoded the cooked package `/BuildableRewards/Rewards/LookupRegistries/DR_SessionEvent_BuildableDestroyed` using the retained corrected mapping. The export was copied byte-for-byte, without reformatting, to [DR_SessionEvent_BuildableDestroyed.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/Rewards/LookupRegistries/DR_SessionEvent_BuildableDestroyed.json).

Export SHA-256: `d66ab5b98ffea6caeec9bbe5105cddd1b4e995cf2b5e49b2bc2749266f93f6b0`; 1,799 bytes. This file is the extractor's JSON array format, not a header-separated export stream. Neither format is evidence of corruption.

Its two exports establish:

| Edge | Exact exported value |
|---|---|
| Registry type | `Challenges.SessionEvents.DestroyedBuildable` |
| Registry item struct | `WDVariantRewardLookupRow` |
| Registry `DataSources` entry | This package's export `.1`, `DataRegistrySource_DataTable_0` |
| Source outer | This package's registry export `.0` |
| Source table | `/BuildableRewards/Rewards/LookupRegistries/Tables/DT_RewardLookup_SessionEvent_BuildableDestroyed.DT_RewardLookup_SessionEvent_BuildableDestroyed` |
| Preloaded table reference | The same lookup table, export `.0` |

That registry type is exactly the assist StateTree lookup task's configured name. [BuildableRewards.json](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Rewards/BuildableRewards/Content/BuildableRewards.json) registers this exact registry object. This is a positive source binding, not a name-similarity guess.

## Joined static contract

Read with the primary native/task evidence in [Round 93 AI/rewards](round93-ai-rewards.md):

1. Authority-side buildable damage maintains per-assister tracked damage. The destruction path invokes assist-history pruning, itself settings/object-validity gated; it does not establish that every expired entry is removed in every state.
2. The destruction producer `0x858EED0`, division at `0x858F646`, writes **retained assister damage / current vitality MaxHealth** into `WDBuildableDestroyedAssistEvent.DamageFraction`, with zero for the near-zero denominator branch. This is not a proved clamp to 0–1 or a guarantee of actual lifetime health loss.
3. The auto-activate assist challenge references the decoded assist StateTree. Its event/state/calculator bindings carry `DamageFraction`, assist context, lookup selection and the calculated resource list.
4. The newly exported registry resolves the tree's exact registry type to the actual variant lookup table. The 36 variant lookup targets match the 36 destruction calculator row keys.
5. Those cash definitions select the damage-fraction curve and scalar 1 for assist context. The 36 role-XP definitions use a separate `BaseReward` selector with an `AssistReward` alternative and other context-dependent alternatives; they do not use the cash fraction curve. Native selector evaluation at `0x6CCEB50` is ordered: earlier matching friendly/tank alternatives take precedence.
6. The mapped native lookup, calculation and grant tasks supply the configured resource list to the authority-gated player-state attribute-grant route. A separate `.Assist` calculator row is not required; the assist tree selects the ordinary destroyed-variant row with assist context.

Static feature/challenge configuration and compiled gates are evidenced. Successful dynamic asset acquisition, a running challenge in a particular match, actual event delivery, account credit and persistence remain runtime observations, not claims made by this contract.

## Identity and verification

- Native image identity: CL-516586 restored executable SHA-256 `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`; the parent re-ran the three research verifiers and native task-ownership checker successfully. Exact results are retained privately in `published_data_verification/evidence/parent-native-verification_01.json`.
- Registry extraction: process exit 0, parser summary `ok=1 fail=0`; no parser errors. Exact command uses a key-file path, never embeds a key in public prose.
- Fresh extraction of the associated lookup table, calculator table and BuildableRewards feature: exit 0, `ok=3 fail=0`. All three parsed export sequences are semantically identical to the existing published JSON, binding the newly recovered registry to the documented source set rather than an assumed matching build label.
- Raw registry copy: source and destination bytes exactly equal; SHA-256 checked.
- Regression guard first failed because the registry export was missing, then passed against the recovered type/source-table links. These guards preserve the artifact contract; they are not a live payout test.
- Private source/command/semantic-comparison receipts remain under `published_data_verification/registry-binding/`. No game execution, memory acquisition, driver/service/boot change, remote write, commit or push was performed.
