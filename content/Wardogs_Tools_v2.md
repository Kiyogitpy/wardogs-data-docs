---
title: "Tools"
redirect_from: ["/Wardogs_Tools_v2.html", "/Wardogs_Tools_v2"]
parent: "Engine & Tooling Data"
description: "File Map, Text Styles"
---

# Wardogs: Tools Data Reference
*Extracted from cooked game data ([`Wardogs/Content/Tools`](https://github.com/Kiyogitpy/wardogs-data-docs/tree/main/data/Wardogs/Content/Tools), 1 file). Editor UI text styles, not gameplay data.*

> **Scope:** one editor-UI text-style table. It is used by the editor tooling and does not affect the game.

---

## 1. File Map

| File | Row struct | Rows |
|---|---|---|
| _EditorUILibrary/_Core/Font/DT_ToolsTextAppearance.json | FToolFont (user-defined struct) | 5 |

---

## 2. Text Styles ([`DT_ToolsTextAppearance`](https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/Wardogs/Content/Tools/_EditorUILibrary/_Core/Font/DT_ToolsTextAppearance.json))

| Style row | Enum entry | Font asset | Typeface | Size | Colour |
|---|---|---|---|---|---|
| Header | NewEnumerator0 | Font_Industry | Medium | 12 | #FFFFFF |
| Subheader | NewEnumerator1 | Font_Industry | Demi | 10 | #FFFFFF |
| LabelHeavy | NewEnumerator2 | Font_Industry | Medium | 10 | #FFFFFF |
| LabelLight | NewEnumerator3 | Font_Industry | Regular | 10 | #FFFFFF |
| Log | NewEnumerator5 | Font_Industry | Light | 8 | #D6D6D6 |

All five styles use the same font asset, `Font_Industry`, with outline size 0 and no font material override. Only the typeface, size and colour change. Colours are white (`#FFFFFF`) for four styles and light grey (`#D6D6D6`) for `Log`.

---

## 3. Still Not Pulled / Limitations

- **The enum `EToolFonts` is not in this dump.** The enum entries are shown as exported (`NewEnumerator0`, `1`, `2`, `3`, `5`). Entry `4` is absent from the table, and its meaning cannot be checked.
- **The row names are the only labels.** Which editor widgets use each style is not in the data.
- **The font asset itself** (`Font_Industry`) is not in this folder.

