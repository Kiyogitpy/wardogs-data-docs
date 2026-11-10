# Native Array Inner metadata — CL516586

All 34 fields requested in [issue #4](https://github.com/Kiyogitpy/wardogs-data-docs/issues/4) have native registration evidence: **31 StructProperty, one IntProperty and two FloatProperty**. The [metadata export](native-array-inner-cl516586.json) retains exact owner/property identifiers, qualified struct names, record linkage, hashes and limitations.

These are direct compiled-in descriptors. No old-donor type fills or SDK `TArray<FNone_>` declarations were used as Inner evidence. For hashed fields, the binary name hash matches the issue token exactly. For readable fields, the owner/member offset comes from the exact canonical idmap and the native name length agrees; this does not claim a plaintext-name hash inversion.

## Source and build identity

The retained Steam manifest records build **25937608**, CL **516586**. The original usmap hash is `8fe8d2b8e6e3c496d7a32f52d2b9cb94ecd1ae71ee2bc091ea97ecddf1cc6207`; the canonical idmap hash is `f4b2942331061187454b625821f8a6119b267551d22dc1cabbdf1a4f3ee1afdb`.

The restored executable is `a5c3db107c29bfd92c3b5f317033f698a0c3a84dad712f32990ae302b4f0cc37`. Every selected native record and resolver/name dependency agrees byte-for-byte at its recorded RVA with the independently reconstructed memory image `925998359846a8b07d01ab70ce79e4be801d14ee7558bd9a7e5675ffa6967884`. Its retained reconstruction receipt binds it to the preserved shipped image `1090559a81a9dda972f86c3d1c13577b747fa337d91ee300f70ad07f1900fea1`.

**Provenance limit:** the historical reconstruction used conditional guest fixtures and was not rerun in this task. The original third-party restored-image producer/recipe and original Dumper-7 producer commit remain unknown. Selected-range agreement is not a whole-executable provenance or runnability guarantee. The new decoder is uncommitted; its source hash and repository baseline are recorded explicitly instead of inventing a tool commit.

## Direct record linkage

The native property builder consumes its pointer array in reverse. Array dispatch consumes exactly one preceding descriptor recursively as Inner. Struct descriptors reference a resolver whose native registration params identify the struct and `/Script/` package. Primitive dispatch was traced to the native `FIntProperty` and `FFloatProperty` field-class names. The export includes each owner parameter block, pointer-array index, Array/Inner descriptor pair and struct resolver/parameter block as file RVAs.

## Recovered fields

| Owner/property | Inner |
| --- | --- |
| `NiagaraSystem._aaaaokkekonalookipena` | `/Script/Niagara.NiagaraEmitterHandle` |
| `SkeletalMesh._aaaamokfccjfgfaagkalp` | `/Script/Engine.SkeletalMeshSourceModel` |
| `StaticMesh.StaticMaterials` | `/Script/Engine.StaticMaterial` |
| `WDAutomatedTestClientProfile._aaaapnghcaefkcjpidkkn` | `/Script/WDGame.WDAutomatedTestInput` |
| `WDChallengeDefinition.Rewards` | `/Script/WDGame.WDReward` |
| `StateTreeReference._aaabblfhomhcablpcafje` | `/Script/CoreUObject.Guid` |
| `WDRewardCalculatorCompiledExpression._aaaaminlajpfohiefcapn` | `/Script/WDGame.WDRewardCalculatorInstruction` |
| `WDDamageableEntityTableRow._aaabjamopmbiblfggnbbj` | `/Script/WDGame.WDDamageModificationEntry` |
| `WDDeathmatchWeaponData._aaabkbjahhefhcbbfnikb` | `/Script/DeathmatchRuntime.WDDeathmatchWeaponVariationData` |
| `LootableData._aaaamgelanhbjfogonmop` | `/Script/LootableRuntime.LootableItemSpawnData` |
| `WDMetaMasteryDefinitionTableRow.LevelDefinitions` | `/Script/WDGame.WDMetaLevelDefinition` |
| `WDMetaSkillEffectsData._aaaamdfihkhbhmleilblo` | `/Script/WDGame.WDMetaSkillEffectPresetData` |
| `WDMetaTreeTableRow.Nodes` | `/Script/WDGame.WDMetaTreeNodeData` |
| `WDMissionDefinition.Challenges` | `/Script/GameplayTags.GameplayTag` |
| `WDMockInvestmentItemTableRow.ActiveInvestmentIds` | `/Script/GameplayTags.GameplayTag` |
| `WDPostProcessEffect._aaaaobmlacemogiinmkif` | `/Script/WDGame.WDPostProcessProgress` |
| `WDPostProcessEffect._aaaccbacmddgfjdaipmpg` | `/Script/CoreUObject.InstancedStruct` |
| `WDRainSpotEntry._aaaanahobnpmkphmpcdgh` | `/Script/WDGame.WDRainLocalEmitter` |
| `WDRewardResourceDefinition._aaaajolkekdchpijcmgll` | `/Script/WDGame.WDRewardResourceModifier` |
| `WDRewardFeedActionDataTableRow.ConditionalExpressions` | `/Script/WDGame.WDRewardFeedActionConditionData` |
| `WDRewardTableRow._aaaanepakckidoddhnopj` | `IntProperty` |
| `WDSceneDataTableRow._aaaakflggmgofcfhobngi` | `/Script/CoreUObject.InstancedStruct` |
| `WDSceneDataTableRow._aaabaolmglmbdpcnpijff` | `/Script/CoreUObject.InstancedStruct` |
| `WDSceneDataTableRow._aaabbklldbhcoflhgmeek` | `/Script/CoreUObject.InstancedStruct` |
| `RichCurve.Keys` | `/Script/Engine.RichCurveKey` |
| `WDUIInteractionContextDataTableRow._aaacfhpjlmfimkcmfkcji` | `/Script/WDGame.WDUIInteractionContextActionConditionData` |
| `WDUIVendorType._aaaamkpdnojbndcdnlldn` | `/Script/WDGame.WDUIButtonParameters` |
| `WDVehicleSeatDamageReductionData._aaabcpelbmpimhadngldm` | `/Script/WDGame.WDVehicleSeatDamageSourceEntry` |
| `WDVehicleSlotPartRow.Selectors` | `/Script/CoreUObject.InstancedStruct` |
| `WDVendorData._aaabeopgecgeeooodlllf` | `/Script/WDGame.WDVendorItemVariationData` |
| `WDWagerActionDefinition.Odds` | `FloatProperty` |
| `WDWagerConditionDefinition._aaaajmjanbcelolelfcda` | `/Script/CoreUObject.InstancedStruct` |
| `WDWagerObjectiveCatalogDefinition.Objectives` | `/Script/WDGame.WDWagerPrebuiltObjective` |
| `WDWagerPricing.LivesOdds` | `FloatProperty` |

## Verification and remaining limits

The complete ordered 34-field cohort was checked against the original usmap (`08ff` in each slot), canonical-idmap decoded member records, native owner/type records and independent-image bytes. Negative controls reject omitted, duplicated and reordered fields, wrong owner/type/list/offset metadata, broken native pointers and changed descriptor bytes.

A separate, local-only usmap changes exactly these 34 Inner descriptors. All original names, slot indices and static dimensions are preserved. CUE4Parse independently reads all 34 recovered Inner types and retains all 21,216 original type owners. Supplemental usmap SHA-256: `6cda31b36ab64750fc04b2fd52a0ccd748c0593471f7d2c0409fce6393b87157`. Binary mappings remain local under the repository policy.

No package extraction, game execution, process attachment, live reflection acquisition or runtime/server behavior was tested. Unknown types outside these 34 fields are unchanged. This is metadata recovery for the documented frozen build, not a claim of complete mapping recovery or future-build support.
