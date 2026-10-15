# Wardogs — GameFeatures: AccountWatermark (v2)
*Extracted from cooked game data (UE 5.7 export JSON, read-only dump). Source folder: `Plugins/GameFeatures/AccountWatermark/` — 2 JSON files (`Content/AccountWatermark.json` with 151 exports, and `Content/Data/DA_AccountWatermark.json`).*

---

## 1. What This Folder Holds

An on-screen account watermark: a widget that shows the account's identifying text on screen, placed at randomised positions. The pack registers one persistent widget and 149 widget instances.

---

## 2. Widget Setup

| Item | Value |
|---|---|
| Persistent widget | `W_AccountWatermark` |
| Layer | `EWDWidgetLayer::Tooltip` |
| Z-order | 255 |
| Widget instances | 149 (`WDGameFeatureAction_AddWidgetElements_Instance_0` to `_148`), exported with no properties |

The 149 instances are probably placement slots (inferred). Their individual positions are not in the export.

---

## 3. Data (`DA_AccountWatermark`)

| Field | Value |
|---|---|
| `RandomizePositionRate` | 5.0 |
| `FormattingString` | `STRINGS_Watermarks` → key `Account.Watermark` |

`RandomizePositionRate` is the value that moves the watermark. Its unit and meaning are inferred from the name only (5.0 is likely a rate in seconds or per-second; not confirmed).

The formatting string points at the `Account.Watermark` entry in the watermark string table. The source-string value is empty in the export, so the text is filled from the table at runtime.

---

## 4. Still not pulled / limitations

- **Instance positions.** The 149 instances export with no data. Their positions and sizes are not known.
- **Randomisation unit.** `RandomizePositionRate` is not confirmed.
- **Runtime text.** The formatted text comes from the string table at runtime.
