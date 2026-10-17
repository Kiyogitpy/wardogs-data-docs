---
title: "Battle-Pass Track & Platform Mastery Rewards"
parent: "Content"
---

# Wardogs — TreeRewardTrack & Platform Mastery Reward Reference
*Extracted from the game's data assets. Covers the battle-pass/progression-tree UI data assets and the cross-role Platform Mastery reward data asset.*

> **Finding:** [`DA_TreeRewardTrack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrack/Data/DA_TreeRewardTrack.json), [`DA_TreeRewardTrackCard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardCard/Data/DA_TreeRewardTrackCard.json), and [`DA_TreeRewardTrackPanel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrackPanel/Data/DA_TreeRewardTrackPanel.json) are **UI structure/template assets** — view-model class bindings, localized string-table text (labels like "{Cost} to Unlock", "Completed"), and icon tags. They do **not** contain the actual per-level cosmetic/item unlock schedule (which item unlocks at which level/cost). **Follow-up resolved:** the actual Season 1 cosmetic content list lives in [`DT_Cosmetics_Season01_Skins`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Skins/Season01_SkinsData/Content/Data/DT_Cosmetics_Season01_Skins.json) and [`DT_Cosmetics_Season01_Emotes`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Plugins/GameFeatures/Emotes/Season01_EmotesData/Content/Data/DT_Cosmetics_Season01_Emotes.json) (`Plugins/GameFeatures/{Skins,Emotes}/Season01_*Data/Content/Data/`) — see `Wardogs_Season01_CosmeticUnlocks_v1.md`. The level/XP *gating* for the track itself (`DT_SeasonDefinitions.SeasonDefinitions`) is an **empty array** in this build — the season-number→date/XP-bracket schedule has not been authored yet in this closed-beta build; only `CurrentSeasonNumber: 1` is set.

---

## Season 02 update (2026-10-15)

- [`DA_TreeRewardTrack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrack/Data/DA_TreeRewardTrack.json) `RewardTextFormat`: key `4CBAAE17…` → `TreeRewardTrack.RewardTextFormat`; table `STRINGS_Progression` is now set as its `TableId`.
- [`DA_TreeRewardTrackPanel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrackPanel/Data/DA_TreeRewardTrackPanel.json) `XPTextFormat` and `LockedLevelXPTextFormat`: keys `206BF79D…` → `TreeRewardTrackPanel.XPTextFormat` and `7D5C8577…` → `TreeRewardTrackPanel.LockedLevelXPTextFormat`; both now reference `STRINGS_Progression`.
- Source strings are unchanged.

---

## 1. [`DA_TreeRewardTrackCard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardCard/Data/DA_TreeRewardTrackCard.json) (`WDUIUnlockTreeData`)

### 1a. Package
- **Package:** `Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardCard/Data/DA_TreeRewardTrackCard.uasset`

### 1b. Values

```json
{
  "IconTag": {
    "TagName": "UI.Icon.Vendor"
  },
  "DefaultTypeText": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.DefaultItemType",
    "SourceString": "Item //",
    "LocalizedString": "Item //"
  },
  "UnlockedText": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.Unlocked",
    "SourceString": "Completed",
    "LocalizedString": "Completed"
  },
  "UnlockCurrencyFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.Format.UnlockCurrency",
    "SourceString": "{Cost} to Unlock",
    "LocalizedString": "{Cost} to Unlock"
  }
}
```

---

## 2. [`DA_TreeRewardTrack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrack/Data/DA_TreeRewardTrack.json) (`WDUITreeRewardTrackData`)

### 2a. Package
- **Package:** `Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrack/Data/DA_TreeRewardTrack.uasset`

### 2b. Values

```json
{
  "RewardTrackPanelViewModelParams": {
    "ViewModelClass": {
      "AssetPathName": "/Script/WDGame.WDUITreeRewardTrackPanelViewModel",
      "SubPathString": ""
    },
    "Data": {
      "AssetPathName": "/Game/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrackPanel/Data/DA_TreeRewardTrackPanel.DA_TreeRewardTrackPanel",
      "SubPathString": ""
    }
  },
  "UnlocksDescriberEntryViewModelParams": {
    "ViewModelClass": {
      "AssetPathName": "/Script/WDGame.WDUIUnlocksTreeNodeViewModel",
      "SubPathString": ""
    },
    "Data": {
      "AssetPathName": "/Game/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardCard/Data/DA_TreeRewardTrackCard.DA_TreeRewardTrackCard",
      "SubPathString": ""
    }
  },
  "LevelUnlockedTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.LevelUnlocks",
    "SourceString": "// Level {Level} Unlockable Items",
    "LocalizedString": "// Level {Level} Unlockable Items"
  },
  "LevelRequiredTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.Format.LevelRequired",
    "SourceString": "Level {Level} Required",
    "LocalizedString": "Level {Level} Required"
  },
  "XPRequiredTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.Format.ExperienceRequired",
    "SourceString": "{Experience}XP Required",
    "LocalizedString": "{Experience}XP Required"
  },
  "FallbackRewardTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.NoRewards",
    "SourceString": "No Rewards Available",
    "LocalizedString": "No Rewards Available"
  },
  "RewardTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "TreeRewardTrack.RewardTextFormat",
    "SourceString": "{CurrentRewards}/{MaxRewards} Items Unlocked",
    "LocalizedString": "{CurrentRewards}/{MaxRewards} Items Unlocked"
  }
}
```

---

## 3. [`DA_TreeRewardTrackPanel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrackPanel/Data/DA_TreeRewardTrackPanel.json) (`WDUITreeRewardTrackPanelData`)

### 3a. Package
- **Package:** `Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrackPanel/Data/DA_TreeRewardTrackPanel.uasset`

### 3b. Values

```json
{
  "UnlockCardViewModelParams": {
    "ViewModelClass": {
      "AssetPathName": "/Script/WDGame.WDUIUnlocksTreeNodeViewModel",
      "SubPathString": ""
    },
    "Data": {
      "AssetPathName": "/Game/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardCard/Data/DA_TreeRewardTrackCard.DA_TreeRewardTrackCard",
      "SubPathString": ""
    }
  },
  "RoleLevelViewModelParams": {
    "ViewModelClass": {
      "AssetPathName": "/Script/WDGame.WDUIRoleLevelViewModel",
      "SubPathString": ""
    },
    "Data": {
      "AssetPathName": "/Game/UI/Shared/Widgets/Meta/Data/DA_RoleLevelData.DA_RoleLevelData",
      "SubPathString": ""
    }
  },
  "FadedOutOpacity": 0.8,
  "ActiveText": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.Active",
    "SourceString": "Unlocked",
    "LocalizedString": "Unlocked"
  },
  "UnlockedText": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "Text.Unlocked",
    "SourceString": "Completed",
    "LocalizedString": "Completed"
  },
  "XPTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "TreeRewardTrackPanel.XPTextFormat",
    "SourceString": "{CurrentLevelXP}/{MaxLevelXP}XP",
    "LocalizedString": "{CurrentLevelXP}/{MaxLevelXP}XP"
  },
  "LockedLevelXPTextFormat": {
    "TableId": "/Game/UI/StringTables/Frontend/STRINGS_Progression.STRINGS_Progression",
    "Key": "TreeRewardTrackPanel.LockedLevelXPTextFormat",
    "SourceString": "{RequiredLevelXP}XP",
    "LocalizedString": "{RequiredLevelXP}XP"
  },
  "RewardTextFormat": {
    "Namespace": "",
    "Key": "10B5F07C4E1365129450999616F2CAB9",
    "SourceString": "{CurrentRewards}/{MaxRewards}",
    "LocalizedString": "{CurrentRewards}/{MaxRewards}"
  },
  "_aaabdnldffopfccceenbo_$DB355EF522244D1E$_$19$": {
    "R": 1.0,
    "G": 1.0,
    "B": 1.0,
    "A": 0.65,
    "Hex": "A6FFFFFF"
  },
  "SelectedTextColor": {
    "R": 0.73791,
    "G": 0.533276,
    "B": 0.042311,
    "A": 1.0,
    "Hex": "DFC13A"
  }
}
```

---

## 4. [`DA_UI_PlatformMastery_RewardData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_RewardData.json) (`WDUIPlatformMasteryRewardData`)

### 4a. Package
- **Package:** `Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_RewardData.uasset`

### 4b. Values

```json
{
  "LockedTextColor": {
    "R": 0.2,
    "G": 0.2,
    "B": 0.2,
    "A": 1.0,
    "Hex": "7C7C7C"
  },
  "LockedItemImageColor": {
    "R": 0.0,
    "G": 0.0,
    "B": 0.0,
    "A": 1.0,
    "Hex": "000000"
  },
  "UnselectedBorderColor": {
    "R": 0.3,
    "G": 0.3,
    "B": 0.3,
    "A": 1.0,
    "Hex": "959595"
  },
  "IconType": {
    "TagName": "UI.Icon.Gunsmith"
  },
  "_aaabejkombelopgfdkigh_$9AEC14BEF653A867$_$20$": {
    "TableId": "/Game/UI/StringTables/STRINGS_TooltipDescriptions.STRINGS_TooltipDescriptions",
    "Key": "TooltipDescription.RoleXP.Formatting",
    "SourceString": "\r\nREWARDS {Emoji} {RoleName} XP",
    "LocalizedString": "\r\nREWARDS {Emoji} {RoleName} XP"
  }
}
```

---

## 5. How the values combine

- **Shared card:** [`DA_TreeRewardTrack`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrack/Data/DA_TreeRewardTrack.json) and [`DA_TreeRewardTrackPanel`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardTrackPanel/Data/DA_TreeRewardTrackPanel.json) both point at [`DA_TreeRewardTrackCard`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Progression/Widgets/Widgets/TreeRewardCard/Data/DA_TreeRewardTrackCard.json) (as `UnlockCardViewModelParams` in the panel). The card's cost text (`{Cost} to Unlock`), icon tag and "Completed" state are the shared template for the cards the track shows. Which rows use it is not stated in these assets.
- **Two "unlocked" labels:** the panel's `ActiveText` (key `Text.Active`) reads "Unlocked", and its `UnlockedText` (key `Text.Unlocked`) reads "Completed". The card uses the same `Text.Unlocked` key for its "Completed" text.
- **Progress strings:** the panel formats XP as `{CurrentLevelXP}/{MaxLevelXP}XP` for the current level and `{RequiredLevelXP}XP` for locked levels. The track supplies "Level {Level} Required", "{Experience}XP Required" and "No Rewards Available" as alternative text. Which of these shows in which state is not stated in the assets.
- **Season gating:** the level/XP thresholds that gate the track are not in these assets. See the Finding above.
- **Mastery reward data:** colours, icon tag (`UI.Icon.Gunsmith`) and the `{Emoji} {RoleName} XP` tooltip format are the only fields. It does not list rewards.

---

## 6. Still not pulled / limitations

- **Per-level cosmetic schedule:** not in these assets. The Season 1 cosmetic content list is in `Wardogs_Season01_CosmeticUnlocks_v1.md`; its "Honest gap" note explains that `DT_SeasonDefinitions.SeasonDefinitions` is empty in this build, so which battle-pass level unlocks which item has not been authored yet.
- **Mastery rewards:** no per-role reward entries appear in [`DA_UI_PlatformMastery_RewardData`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/UI/Features/Frontend/Mastery/Platforms/Data/DA_UI_PlatformMastery_RewardData.json) as extracted here.
- **Hashed keys:** several keys (for example `10B5F07C…`, `_aaabdnld…`) are not localization keys: none of the 121 `STRINGS_*` tables pulled contain them. They look like Blueprint property names. Their meaning is not resolved in this doc.
- **Localized text:** the asset listing has no other-locale copies of the string tables, so only the source strings exist in this data.
