---
title: "All Changes"
parent: "Season 2 Changes"
nav_order: 99
description: "Full Season 1 to Season 2 change browser: every asset and property, before and after, filterable by area, status and text."
---

# All Changes

{{ page.description }}

Deep links work: `#area=vehicles&q=Humvee` opens an area with a text filter, and `&s=modified,added` limits the status. Add `&noise=0` to show noise-only assets.

The text filter matches asset names and paths, property paths (including `ExportName::` prefixes and `[Key=Value]` parts) and values. Percentages are relative to the absolute Season 1 value and the sign follows the change (-0.055 to -0.0255 is +53.6%); no percentage is shown when Season 1 was 0 (or a denormal value close to 0).

Some properties have no known name in either export, and the two seasons give them different placeholder names. When each side has exactly one such property of the same shape, the two are compared and the row is marked **matched by position**; treat those rows as likely, not certain.

<div class="sd" id="sd" data-sd-browser data-sd-base="{{ '/assets/data/season-diff/' | relative_url }}" data-gh="https://github.com/Kiyogitpy/wardogs-data-docs/blob/main/data/" markdown="0">
  <p class="sd-note">Loading changes…</p>
</div>

<noscript><p>The change browser needs JavaScript. The source data is in <code>assets/data/season-diff/</code>.</p></noscript>

<script src="{{ '/assets/js/season-diff.js' | relative_url }}?v={{ site.time | date: '%s' }}" defer></script>
